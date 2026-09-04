#!/bin/bash
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
#龍芯⚡️丙午·丙申·己未·乙亥时·䷞旅-DEPLOY-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# SPDX-License-Identifier: MulanPSL-2.0
# ==============================================================================
# 🐉 龍魂 · 流量拓扑一键部署 (幂等 · 前置检查 · 备份 · trap 自动回滚 · 两段式证书)
# 目标平台: Ubuntu 22.04+ (arm64/x86_64 通用)
# 用法: sudo ./deploy.sh
# 环境变量: DOMAIN(默认uid9622.cn) CERT_EMAIL SKIP_DNS=1(跳过DNS断言)
# ==============================================================================

set -euo pipefail

DOMAIN="${DOMAIN:-uid9622.cn}"
CERT_EMAIL="${CERT_EMAIL:-admin@${DOMAIN}}"
PKG_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TS="$(date +%Y%m%d_%H%M%S)"
BACKUP_ROOT="/var/backups/longhun"
BACKUP_DIR="${BACKUP_ROOT}/${TS}"
VENV="/opt/longhun-system/venv"
SYS_DIR="/opt/longhun-system"
DEPLOY_OK=0

log()  { echo "[龍魂] $*"; }
warn() { echo "[龍魂] 🟡 警告: $*" >&2; }
die()  { echo "[龍魂] 🔴 失败: $*" >&2; exit 1; }

# ---------- trap: 失败自动回滚 (修正11) ----------
on_error() {
    local lineno="$1"
    echo "" >&2
    echo "[龍魂] 🔴 部署在第 ${lineno} 行失败, 触发自动回滚..." >&2
    if [ -f "${BACKUP_DIR}/manifest.txt" ]; then
        # 恢复 nginx 配置
        [ -f "${BACKUP_DIR}/nginx.conf" ] && cp -f "${BACKUP_DIR}/nginx.conf" /etc/nginx/nginx.conf
        if [ -f "${BACKUP_DIR}/sites-available-longhun" ]; then
            cp -f "${BACKUP_DIR}/sites-available-longhun" /etc/nginx/sites-available/longhun
        else
            rm -f /etc/nginx/sites-enabled/longhun /etc/nginx/sites-available/longhun
        fi
        # 恢复 systemd 单元
        for u in longhun-api longhun-collab longhun-bridge; do
            if [ -f "${BACKUP_DIR}/${u}.service" ]; then
                cp -f "${BACKUP_DIR}/${u}.service" "/etc/systemd/system/${u}.service"
            fi
        done
        systemctl daemon-reload || true
        if command -v nginx >/dev/null 2>&1 && nginx -t >/dev/null 2>&1; then
            systemctl reload nginx 2>/dev/null || systemctl restart nginx 2>/dev/null || true
            echo "[龍魂] 已恢复旧配置并重载 nginx" >&2
        else
            echo "[龍魂] 旧配置已恢复 (nginx 未重载, 请人工检查: nginx -t)" >&2
        fi
    else
        echo "[龍魂] 无可用备份 (首次部署在备份前失败), 请检查上方错误输出" >&2
    fi
    echo "[龍魂] 手动回滚: sudo ${PKG_DIR}/rollback.sh" >&2
    exit 1
}
trap 'on_error $LINENO' ERR

# ---------- 0. root 权限 ----------
[ "$(id -u)" -eq 0 ] || die "请使用 root 权限运行: sudo $0"

log "🐉 龍魂 · 一键部署开始 (备份目录: ${BACKUP_DIR})"
echo "========================================"

# ---------- 1. 前置检查 ----------
log "1/12 前置检查..."

# 1.1 端口占用 (允许本系统已部署的服务占用 = 幂等重跑)
check_port() {
    local port="$1" allow_pat="$2"
    local line
    line="$(ss -tlnp 2>/dev/null | grep -E ":${port} " || true)"
    if [ -n "$line" ] && ! grep -qE "${allow_pat}" <<<"$line"; then
        die "端口 ${port} 被非龍魂进程占用: ${line}"
    fi
}
check_port 80   'nginx'
check_port 443  'nginx'
check_port 8970 'python'
check_port 19622 'python'
check_port 18799 'python'
log "    端口检查通过 (80/443/8970/19622/18799)"

# 1.2 磁盘空间 (≥500MB)
avail_mb="$(df -Pm / | awk 'NR==2{print $4}')"
[ "${avail_mb}" -ge 500 ] || die "磁盘可用空间不足 500MB (当前 ${avail_mb}MB)"
log "    磁盘可用 ${avail_mb}MB"

# 1.3 Python ≥ 3.10 (Ubuntu 22.04 默认 3.10)
python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' \
    || die "Python 版本需 ≥ 3.10 (当前: $(python3 -V 2>&1))"
log "    $(python3 -V)"

# 1.4 DNS 解析断言 (修正12; 沙箱/内网可 SKIP_DNS=1 跳过)
if [ "${SKIP_DNS:-0}" != "1" ]; then
    if command -v dig >/dev/null 2>&1; then
        dns_ip="$(dig +short A "${DOMAIN}" | tail -1)"
        pub_ip="$(curl -s --max-time 5 https://api.ipify.org || curl -s --max-time 5 https://ifconfig.me || true)"
        if [ -z "${dns_ip}" ]; then
            die "DNS 未解析: ${DOMAIN} 无 A 记录 (可用 SKIP_DNS=1 跳过)"
        fi
        if [ -n "${pub_ip}" ] && [ "${dns_ip}" != "${pub_ip}" ]; then
            die "DNS 断言失败: ${DOMAIN} → ${dns_ip}, 本机公网 ${pub_ip} (可用 SKIP_DNS=1 跳过)"
        fi
        log "    DNS 断言通过: ${DOMAIN} → ${dns_ip}"
    else
        warn "dig 不可用, 安装 dnsutils 后再执行 DNS 断言 (本次跳过)"
    fi
else
    warn "SKIP_DNS=1, 跳过 DNS 解析断言"
fi

# ---------- 2. 安装依赖包 ----------
log "2/12 安装系统依赖..."
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq nginx certbot python3-certbot-nginx \
    python3-venv python3-pip curl dnsutils logrotate >/dev/null

# ---------- 3. 备份 (时间戳目录 + manifest, 修正11) ----------
log "3/12 备份现有配置 → ${BACKUP_DIR}"
mkdir -p "${BACKUP_DIR}"
{
    echo "timestamp=${TS}"
    echo "domain=${DOMAIN}"
    echo "files:"
} > "${BACKUP_DIR}/manifest.txt"
backup_file() {  # $1=源路径 $2=备份名
    if [ -f "$1" ]; then
        cp -a "$1" "${BACKUP_DIR}/$2"
        echo "  $2  <-  $1  sha256=$(sha256sum "$1" | cut -d' ' -f1)" >> "${BACKUP_DIR}/manifest.txt"
    else
        echo "  $2  <-  $1  (不存在, 首次部署)" >> "${BACKUP_DIR}/manifest.txt"
    fi
}
backup_file /etc/nginx/nginx.conf nginx.conf
backup_file /etc/nginx/sites-available/longhun sites-available-longhun
backup_file /etc/systemd/system/longhun-api.service longhun-api.service
backup_file /etc/systemd/system/longhun-collab.service longhun-collab.service
backup_file /etc/systemd/system/longhun-bridge.service longhun-bridge.service
backup_file /etc/cron.d/longhun cron.d-longhun
backup_file /etc/logrotate.d/longhun logrotate-longhun
log "    manifest: ${BACKUP_DIR}/manifest.txt"

# ---------- 4. 创建全部目录 (修正13, SPEC修正3) ----------
log "4/12 创建目录..."
mkdir -p /var/www/longhun /var/www/certbot
mkdir -p /opt/longhun/shared/{collab,handoffs,collaboration}
mkdir -p /opt/longhun/audit
mkdir -p /var/log/longhun
mkdir -p "${SYS_DIR}/08_BIN"
chown -R www-data:www-data /var/www/longhun /var/www/certbot /opt/longhun/shared /opt/longhun/audit
chmod 755 /var/log/longhun

# ---------- 5. 部署后端代码 + venv 依赖 (PEP668, 修正23) ----------
log "5/12 部署后端代码 + venv..."
install -m 0644 "${PKG_DIR}/08_BIN/"*.py "${SYS_DIR}/08_BIN/"
install -m 0755 "${PKG_DIR}/08_BIN/lh_health_check.sh" /usr/local/bin/lh_health_check.sh
install -m 0644 "${PKG_DIR}/requirements.txt" "${SYS_DIR}/requirements.txt"
# 正式干支 DNA 生成器 (SPEC: DNA 一律由生成器算法生成)
# 修正29: 生成器随包携带 (bin/lh_dna_generator.py), 安装到 /opt/longhun-system/bin/;
# 三服务 systemd 单元 Environment=PYTHONPATH=/opt/longhun-system/bin 保证可 import
[ -f "${PKG_DIR}/bin/lh_dna_generator.py" ] || die "包内缺少 bin/lh_dna_generator.py (正式干支 DNA 生成器)"
mkdir -p "${SYS_DIR}/bin"
install -m 0644 "${PKG_DIR}/bin/lh_dna_generator.py" "${SYS_DIR}/bin/"
if [ ! -x "${VENV}/bin/python" ]; then
    python3 -m venv "${VENV}"
fi
"${VENV}/bin/pip" install --quiet --upgrade pip
"${VENV}/bin/pip" install --quiet -r "${SYS_DIR}/requirements.txt"
log "    venv: ${VENV} ($( "${VENV}/bin/python" -V ))"

# ---------- 6. 前端首页 ----------
log "6/12 部署前端首页..."
install -m 0644 "${PKG_DIR}/var_www/index.html" /var/www/longhun/index.html
chown www-data:www-data /var/www/longhun/index.html

# ---------- 7. sysctl / limits (修正15: 无 ip_local_port_range; conntrack arm64 🟡容错) ----------
log "7/12 内核参数与资源限制..."
install -m 0644 "${PKG_DIR}/conf/sysctl/99-longhun.conf" /etc/sysctl.d/99-longhun.conf
install -m 0644 "${PKG_DIR}/conf/limits/99-longhun.conf" /etc/security/limits.d/99-longhun.conf
sysctl -p /etc/sysctl.d/99-longhun.conf >/dev/null \
    || warn "部分 sysctl 项写入失败 (鲲鹏 arm64 conntrack 可写性待验🟡), 不影响主流程"

# ---------- 8. systemd ×3 (Restart=always, 禁止 nohup 裸奔) ----------
log "8/12 安装 systemd 服务..."
for u in longhun-api longhun-collab longhun-bridge; do
    install -m 0644 "${PKG_DIR}/systemd/${u}.service" "/etc/systemd/system/${u}.service"
done
systemctl daemon-reload
systemctl enable longhun-api longhun-collab longhun-bridge >/dev/null 2>&1 || true
systemctl restart longhun-api longhun-collab longhun-bridge

# ---------- 9. nginx 配置: 临时文件 → nginx -t → 原子替换 (修正1/12) ----------
log "9/12 部署 nginx 配置 (两段式证书)..."
write_nginx_main() {
    install -m 0644 "${PKG_DIR}/conf/nginx/nginx.conf" /etc/nginx/.nginx.conf.longhun.tmp
    mv -T /etc/nginx/.nginx.conf.longhun.tmp /etc/nginx/nginx.conf   # rename 原子替换
}
# 修正28: http2 指令版本自适应 (焊死)
#   nginx ≥ 1.25.1 才支持独立指令 `http2 on;`; stock apt nginx
#   (Ubuntu22.04=1.18 / 24.04=1.24 / Debian12=1.22) 只认 legacy 参数式
#   `listen 443 ssl http2;`。站点配置中的 @LISTEN_443@ token 在此替换。
nginx_supports_http2_directive() {
    # 解析 `nginx -v` 输出 (stderr): "nginx version: nginx/1.24.0 (Ubuntu)"
    local ver major minor patch
    ver="$(nginx -v 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || true)"
    [ -n "${ver}" ] || return 1   # 解析失败 → 走 legacy 分支 (全版本兼容, 最保守)
    major="${ver%%.*}"; rest="${ver#*.}"
    minor="${rest%%.*}"; patch="${rest#*.}"
    if [ "${major}" -gt 1 ] || \
       { [ "${major}" -eq 1 ] && [ "${minor}" -gt 25 ]; } || \
       { [ "${major}" -eq 1 ] && [ "${minor}" -eq 25 ] && [ "${patch}" -ge 1 ]; }; then
        return 0
    fi
    return 1
}
render_listen_443() {
    # 输出替换 @LISTEN_443@ 的最终行 (保持 4 空格缩进)
    # 注意: stdout 仅允许输出配置行 (被 $() 捕获), 日志一律走 stderr
    if nginx_supports_http2_directive; then
        log "    nginx $(nginx -v 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1) ≥ 1.25.1 → http2 on; 独立指令" >&2
        printf '    listen 443 ssl;\n    listen [::]:443 ssl;\n    http2 on;\n'
    else
        warn "nginx < 1.25.1 → legacy 写法 listen 443 ssl http2; (deprecated 告警🟡但兼容 stock nginx)"
        printf '    # 🟡 legacy http2 参数式 (nginx < 1.25.1; nginx -t 会提示 deprecated, 属预期)\n    listen 443 ssl http2;\n    listen [::]:443 ssl http2;\n'
    fi
}
write_site_full() {
    install -m 0644 "${PKG_DIR}/conf/nginx/sites-available/longhun" \
        /etc/nginx/sites-available/.longhun.tmp
    # 域名自适应 (默认 uid9622.cn 时为空操作)
    sed -i "s/uid9622\.cn/${DOMAIN}/g" /etc/nginx/sites-available/.longhun.tmp
    # 修正28: 在写入正式路径前替换 @LISTEN_443@ token, 保证 nginx -t 验证的是最终形态
    local listen_lines
    listen_lines="$(render_listen_443)"
    # 仅替换独立 token 行 (注释中提及 token 名的行不动)
    awk -v repl="${listen_lines}" \
        '{ if ($0 ~ /^[[:space:]]*@LISTEN_443@[[:space:]]*$/) { print repl } else { print } }' \
        /etc/nginx/sites-available/.longhun.tmp > /etc/nginx/sites-available/.longhun.tmp.2
    if grep -qE '^[[:space:]]*@LISTEN_443@[[:space:]]*$' /etc/nginx/sites-available/.longhun.tmp.2; then
        die "@LISTEN_443@ token 替换失败, 拒绝写入未渲染配置"
    fi
    mv -T /etc/nginx/sites-available/.longhun.tmp.2 /etc/nginx/sites-available/.longhun.tmp
    mv -T /etc/nginx/sites-available/.longhun.tmp /etc/nginx/sites-available/longhun
}
write_site_stage1() {
    # 第一段: 证书不存在时的 80-only 临时配置 (完整配置, 非占位符)
    cat > /etc/nginx/sites-available/.longhun.tmp <<'STAGE1EOF'
#龍芯⚡️丙午·丙申·己未·乙亥时·䷞旅-SITE-STAGE1-v1.0-UID9622
# 第一段临时配置: 仅 80 端口, 用于 certbot webroot 首次签发; 签发成功后由
# deploy.sh 自动替换为完整 443 配置 (conf/nginx/sites-available/longhun)。
server {
    listen 80;
    listen [::]:80;
    server_name uid9622.cn www.uid9622.cn;

    location ^~ /.well-known/acme-challenge/ {
        root /var/www/certbot;
        default_type text/plain;
        try_files $uri =404;
    }

    location = /health {
        access_log off;
        default_type text/plain;
        return 200 "🐉 龍魂系统运行正常(stage1-80only)\n";
    }

    location / {
        root /var/www/longhun;
        try_files $uri $uri/ /index.html;
        index index.html;
    }
}
STAGE1EOF
    sed -i "s/uid9622\.cn/${DOMAIN}/g" /etc/nginx/sites-available/.longhun.tmp
    mv -T /etc/nginx/sites-available/.longhun.tmp /etc/nginx/sites-available/longhun
}

ln -sfn /etc/nginx/sites-available/longhun /etc/nginx/sites-enabled/longhun
rm -f /etc/nginx/sites-enabled/default
write_nginx_main

CERT_FILE="/etc/letsencrypt/live/${DOMAIN}/fullchain.pem"
if [ -f "${CERT_FILE}" ]; then
    log "    证书已存在, 直接部署 443 全配置"
    write_site_full
else
    log "    证书不存在 → 第一段: 80-only 临时配置"
    write_site_stage1
    nginx -t
    systemctl reload nginx 2>/dev/null || systemctl restart nginx
    log "    运行 certbot webroot 签发 (${DOMAIN}, www.${DOMAIN})..."
    if certbot certonly --webroot -w /var/www/certbot \
        -d "${DOMAIN}" -d "www.${DOMAIN}" \
        --agree-tos -m "${CERT_EMAIL}" --non-interactive; then
        log "    证书签发成功 → 第二段: 切换 443 全配置"
        write_site_full
    else
        warn "certbot 签发失败 (DNS/安全组/80入向待验🟡), 保持 80-only 配置; 修复后重跑 deploy.sh 自动切 443"
    fi
fi

nginx -t   # 最终配置语法验证; 失败 → trap 自动回滚
systemctl enable nginx >/dev/null 2>&1 || true
systemctl restart nginx

# ---------- 10. /etc/cron.d/longhun (修正10: 不用 crontab - 覆盖式) ----------
log "10/12 写入 /etc/cron.d/longhun..."
cat > /etc/cron.d/longhun <<'CRONEOF'
#龍芯⚡️丙午·丙申·己未·乙亥时·䷞旅-CRON-v1.0-UID9622
# SPDX-License-Identifier: MulanPSL-2.0
# 龍魂定时任务: 证书续期 + 后端健康巡检 (修正10: 独立文件, 不清空既有 crontab)
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# 每日 03:00 certbot 续期, 成功则 reload nginx
0 3 * * * root /usr/bin/certbot renew --quiet --post-hook "systemctl reload nginx" >/dev/null 2>&1

# 每 5 分钟后端健康巡检, 异常记录到 /var/log/longhun/health_check.log
*/5 * * * * root /usr/local/bin/lh_health_check.sh >> /var/log/longhun/health_check.log 2>&1
CRONEOF
chmod 0644 /etc/cron.d/longhun

# ---------- 11. logrotate (修正13/23) ----------
log "11/12 写入 logrotate..."
cat > /etc/logrotate.d/longhun <<'LOGROTATEEOF'
#龍芯⚡️丙午·丙申·己未·乙亥时·䷞旅-LOGROTATE-v1.0-UID9622
# SPDX-License-Identifier: MulanPSL-2.0
/var/log/longhun/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 root adm
    sharedscripts
    postrotate
        systemctl reload rsyslog >/dev/null 2>&1 || true
    endscript
}
LOGROTATEEOF
chmod 0644 /etc/logrotate.d/longhun

# ---------- 12. 部署后验证 ----------
log "12/12 部署后验证..."
sleep 2
/usr/local/bin/lh_health_check.sh || warn "部分后端服务未就绪, 请查看 journalctl -u longhun-api 等"

DEPLOY_OK=1
trap - ERR

echo ""
echo "✅ 龍魂部署完成"
echo "========================================"
echo "nginx:    $(systemctl is-active nginx)"
echo "api:      $(systemctl is-active longhun-api)  (:8970)"
echo "collab:   $(systemctl is-active longhun-collab) (:19622)"
echo "bridge:   $(systemctl is-active longhun-bridge) (:18799)"
echo "备份:     ${BACKUP_DIR} (manifest.txt)"
echo ""
echo "== 验证命令清单 =="
echo "  1) nginx -t"
echo "  2) curl -s http://127.0.0.1:8970/health   # 含 dna 字段"
echo "  3) curl -s http://127.0.0.1:19622/health"
echo "  4) curl -s http://127.0.0.1:18799/health"
echo "  5) curl -s -o /dev/null -w '%{http_code}\n' https://${DOMAIN}/api/test          # 无DNA → 403"
echo "  6) curl -s -H 'X-Dragon-DNA: #龍芯⚡️test-xxxx-UID9622' https://${DOMAIN}/api/test"
echo "  7) curl -sI https://${DOMAIN}/ | grep -i x-longhun                              # 主权头齐全"
echo "  8) python3 ${SYS_DIR}/08_BIN/lh_audit.py                                        # 审计链自检"
echo "  9) tail -3 /opt/longhun/audit/audit.jsonl                                       # prev_hash 链"
echo " 10) systemctl status longhun-api longhun-collab longhun-bridge --no-pager"
echo " 11) ss -tlnp | grep -E ':(80|443|8970|19622|18799) '"
echo " 12) sudo ${PKG_DIR}/rollback.sh                                                  # 需要回滚时"
