#!/bin/bash
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
#龍芯⚡️丙午·丙申·己未·乙亥时·䷞旅-DEPLOY-FLOW-INCREMENTAL-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# SPDX-License-Identifier: MulanPSL-2.0
# ==============================================================================
# 🐉 流量拓扑交付包 · 生产增量部署 (不覆盖现有 nginx/服务)
# 适用: 鲲鹏生产环境 (Ubuntu 24.04) 已运行完整 uid9622.cn 主站
# 功能:
#   1. venv 创建 + 依赖安装 (若 venv 不存在)
#   2. 后端代码 → /opt/longhun-system/08_BIN/ (不改动现有文件, 只 install 交付包)
#   3. systemd 单元 ×3 → longhun-flow-api/collab/bridge (flow 前缀, 不覆盖生产)
#   4. nginx: 独立 conf.d 片段 (zone/upstream/map, flow_ 前缀)
#      + 增量 location 合并进主站 443 server 块 (备份→合并→nginx -t→reload, 失败回滚)
#   5. 不覆盖: nginx.conf / sites-available/longhun / /var/www/longhun/index.html
#      / /etc/cron.d/longhun(无) / /etc/logrotate.d/longhun(已存在, 保留)
# 用法: sudo ./deploy-flow-incremental.sh
# ==============================================================================

set -euo pipefail

PKG_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TS="$(date +%Y%m%d_%H%M%S)"
SYS_DIR="/opt/longhun-system"
VENV="${SYS_DIR}/venv"
MAIN_CONF="/etc/nginx/conf.d/nginx-uid9622.cn.conf"
BK="/var/backups/longhun/flow-incremental-${TS}"
DEPLOY_OK=0

log()  { echo "[龍魂] $*"; }
warn() { echo "[龍魂] 🟡 警告: $*" >&2; }
die()  { echo "[龍魂] 🔴 失败: $*" >&2; exit 1; }

# ---------- trap: 失败自动回滚 ----------
on_error() {
    local lineno="$1"
    echo "" >&2
    echo "[龍魂] 🔴 增量部署在第 ${lineno} 行失败, 触发自动回滚..." >&2
    if [ -d "${BK}" ]; then
        # 恢复主站配置
        if [ -f "${BK}/nginx-uid9622.cn.conf" ]; then
            cp -f "${BK}/nginx-uid9622.cn.conf" "${MAIN_CONF}"
            echo "[龍魂] 已恢复主站 nginx 配置" >&2
        fi
        # 恢复 systemd 单元 (若已安装)
        for u in longhun-flow-api longhun-flow-collab longhun-flow-bridge; do
            if [ -f "${BK}/${u}.service" ]; then
                cp -f "${BK}/${u}.service" "/etc/systemd/system/${u}.service"
            fi
        done
        systemctl daemon-reload || true
        if command -v nginx >/dev/null 2>&1 && nginx -t >/dev/null 2>&1; then
            systemctl reload nginx 2>/dev/null || systemctl restart nginx 2>/dev/null || true
            echo "[龍魂] 已恢复并重载 nginx" >&2
        fi
    fi
    echo "[龍魂] 手动回滚: sudo ${PKG_DIR}/rollback.sh" >&2
    exit 1
}
trap 'on_error $LINENO' ERR

# ---------- 0. root ----------
[ "$(id -u)" -eq 0 ] || die "请使用 root: sudo $0"

log "🐉 流量拓扑 · 生产增量部署开始 (备份: ${BK})"
mkdir -p "${BK}"

# ---------- 1. 前置检查 (只查交付包三端口) ----------
log "1/8 前置检查..."
check_port() {
    local port="$1" allow_pat="$2"
    local line
    line="$(ss -tlnp 2>/dev/null | grep -E ":${port} " || true)"
    if [ -n "$line" ] && ! grep -qE "${allow_pat}" <<<"$line"; then
        die "端口 ${port} 被非预期进程占用: ${line}"
    fi
}
check_port 8970  'python'
check_port 19622 'python'
check_port 18800 'python'
log "    端口检查通过 (8970/19622/18800)"

avail_mb="$(df -Pm / | awk 'NR==2{print $4}')"
[ "${avail_mb}" -ge 300 ] || die "磁盘不足 300MB"
log "    磁盘可用 ${avail_mb}MB"

# ---------- 2. venv ----------
log "2/8 venv 准备..."
mkdir -p "${SYS_DIR}/08_BIN" "${SYS_DIR}/bin"
if [ ! -x "${VENV}/bin/python" ]; then
    python3 -m venv "${VENV}"
    log "    venv 已创建"
else
    log "    venv 已存在"
fi
"${VENV}/bin/pip" install --quiet --upgrade pip

# ---------- 3. 后端代码 ----------
log "3/8 部署后端代码..."
install -m 0644 "${PKG_DIR}/08_BIN/"*.py "${SYS_DIR}/08_BIN/"
install -m 0755 "${PKG_DIR}/08_BIN/lh_health_check.sh" /usr/local/bin/lh_health_check.sh
install -m 0644 "${PKG_DIR}/requirements.txt" "${SYS_DIR}/requirements.txt"
[ -f "${PKG_DIR}/bin/lh_dna_generator.py" ] && \
    install -m 0644 "${PKG_DIR}/bin/lh_dna_generator.py" "${SYS_DIR}/bin/"
"${VENV}/bin/pip" install --quiet -r "${SYS_DIR}/requirements.txt"
log "    venv: $( "${VENV}/bin/python" -V )"

# ---------- 4. systemd ×3 (flow 前缀) ----------
log "4/8 安装 systemd 服务 (flow 前缀)..."
for u in longhun-flow-api longhun-flow-collab longhun-flow-bridge; do
    src="${PKG_DIR}/systemd/${u}.service"
    [ -f "${src}" ] || die "缺少 ${src}"
    # 备份现有 (若存在)
    [ -f "/etc/systemd/system/${u}.service" ] && \
        cp -a "/etc/systemd/system/${u}.service" "${BK}/${u}.service"
    install -m 0644 "${src}" "/etc/systemd/system/${u}.service"
done
systemctl daemon-reload
systemctl enable longhun-flow-api longhun-flow-collab longhun-flow-bridge >/dev/null 2>&1 || true
systemctl restart longhun-flow-api longhun-flow-collab longhun-flow-bridge

# ---------- 5. nginx 增量 (zone/upstream/map 独立片段) ----------
log "5/8 部署 nginx 增量片段 (conf.d/longhun-flow-incremental.conf)..."
cp -a "${MAIN_CONF}" "${BK}/nginx-uid9622.cn.conf"
install -m 0644 "${PKG_DIR}/conf/nginx/longhun-flow-incremental.conf" \
    /etc/nginx/conf.d/longhun-flow-incremental.conf

# ---------- 6. 合并增量 location 进主站 443 server 块 ----------
log "6/8 合并增量路由进主站 443 server 块..."
# 定位主站 443 server 块: 找 "listen 443" 起始行到下一个匹配的 "}" 结束行
# 精确做法: 在 443 server 块最后一个 location 之后、"}" 之前插入
# 用 awk 在文件最后闭合处插入 (主站文件末尾即 443 server 块结尾)
LOC_BLOCK=$(cat <<'LOCEOF'

    # ════════════════════════════════════════════════════
    # 流量拓扑交付包 · 增量路由 (flow_* zone/upstream 见 conf.d 片段)
    # ════════════════════════════════════════════════════
    location = /auth/verify {
        internal;
        proxy_pass http://flow_longhun_api/auth/verify;
        proxy_pass_request_body off;
        proxy_set_header Content-Length "";
        proxy_set_header X-Original-URI $request_uri;
        proxy_set_header X-Dragon-DNA $http_x_dragon_dna;
        proxy_connect_timeout 5s;
        proxy_read_timeout 5s;
    }

    location = /health/flow {
        access_log off;
        default_type text/plain;
        return 200 "🐉 龍魂流量拓扑运行正常\n";
    }

    location /collab/api/ {
        limit_req zone=flow_api_limit burst=20 nodelay;
        proxy_pass http://flow_longhun_collab/;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Dragon-DNA $http_x_dragon_dna;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    location /handoffs/ {
        auth_request /auth/verify;
        alias /opt/longhun/shared/handoffs/;
        autoindex on;
        autoindex_exact_size off;
        autoindex_localtime on;
        charset utf-8;
        limit_except GET HEAD { deny all; }
        add_header Cache-Control "no-store" always;
    }

    location /protocols/ {
        auth_request /auth/verify;
        alias /opt/longhun/shared/collaboration/;
        autoindex on;
        autoindex_exact_size off;
        autoindex_localtime on;
        charset utf-8;
        limit_except GET HEAD { deny all; }
        add_header Cache-Control "no-store" always;
    }

    location = /chat {
        auth_request /auth/verify;
        limit_req zone=flow_chat_limit burst=10 nodelay;
        proxy_pass http://flow_longhun_bridge/api/v1/chat;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Dragon-DNA $http_x_dragon_dna;
        proxy_connect_timeout 120s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
        proxy_buffering off;
    }

    location /chat/ {
        auth_request /auth/verify;
        limit_req zone=flow_chat_limit burst=10 nodelay;
        proxy_pass http://flow_longhun_bridge/api/v1/chat/;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Dragon-DNA $http_x_dragon_dna;
        proxy_connect_timeout 120s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
        proxy_buffering off;
    }
LOCEOF
)

# 幂等: 若已含标记则跳过合并
if grep -q '流量拓扑交付包 · 增量路由' "${MAIN_CONF}"; then
    log "    已包含增量路由标记, 跳过合并 (幂等)"
else
    # 合并: 精确插入到 uid9622.cn 主站 443 server 块 (62-439行) 内,
    # 绝不插到 api.uid9622.cn (444-516行) 或 80 重定向块。
    # block 通过环境变量传入, 避免 heredoc 被 python 解释器消费导致空 block。
    export FLOW_LOC_BLOCK="${LOC_BLOCK}"
    python3 - "${MAIN_CONF}" <<'PYEOF'
import os, sys
conf = sys.argv[1]
block = os.environ.get('FLOW_LOC_BLOCK', '')
if not block:
    print("ERROR: FLOW_LOC_BLOCK 为空, 不执行合并", file=sys.stderr)
    sys.exit(1)
with open(conf, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. 定位 uid9622.cn 主站 server_name 行 (排除 api.uid9622.cn)
target = None
for i, ln in enumerate(lines):
    if 'server_name' in ln and 'uid9622.cn' in ln and 'api.uid9622.cn' not in ln:
        target = i
        break
if target is None:
    print("未找到 uid9622.cn 主站 server_name", file=sys.stderr)
    sys.exit(1)

# 2. 往回找最近的 "server {" 起始行
start = target
while start >= 0 and lines[start].strip() != 'server {':
    start -= 1
if start < 0:
    print("未找到 server { 起始行", file=sys.stderr)
    sys.exit(1)

# 3. 花括号配对, 找该 server 块的结束 "}"
depth = 0
end = -1
for j in range(start, len(lines)):
    depth += lines[j].count('{') - lines[j].count('}')
    if depth == 0 and j > start:
        end = j
        break
if end == -1:
    print("未找到 server 块配对 }", file=sys.stderr)
    sys.exit(1)

# 4. 在结束 "}" 之前插入增量路由
new_lines = lines[:end] + [block] + lines[end:]
with open(conf, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print(f"已合并增量路由到 uid9622.cn 主站块 (起始行{start+1}, 结束行{end+1})")
PYEOF
    nginx -t
    systemctl reload nginx 2>/dev/null || systemctl restart nginx
    log "    nginx -t 通过, 已 reload"
fi

# ---------- 7. 验证 ----------
log "7/8 部署后验证..."
sleep 2
echo "--- 服务状态 ---"
for u in longhun-flow-api longhun-flow-collab longhun-flow-bridge; do
    st="$(systemctl is-active "$u" 2>/dev/null || echo unknown)"
    echo "  $u: $st"
done
echo "--- 端口监听 ---"
ss -tlnp 2>/dev/null | grep -E ':(8970|19622|18800) ' || echo "  (无监听)"
echo "--- 后端健康 ---"
curl -s --max-time 5 http://127.0.0.1:8970/health || echo "  api 未就绪"
echo ""
curl -s --max-time 5 http://127.0.0.1:19622/health || echo "  collab 未就绪"
echo ""
curl -s --max-time 5 http://127.0.0.1:18800/health || echo "  bridge 未就绪"
echo ""
echo "--- nginx -t ---"
nginx -t

DEPLOY_OK=1
trap - ERR

echo ""
echo "✅ 龍魂流量拓扑 · 增量部署完成"
echo "========================================"
echo "systemd: longhun-flow-api(:8970) / longhun-flow-collab(:19622) / longhun-flow-bridge(:18800)"
echo "nginx:   主站未覆盖, 增量路由已合并 (/chat /collab/api/ /handoffs/ /protocols/)"
echo "备份:    ${BK}"
echo "验证:    curl -s https://uid9622.cn/health/flow"
echo "         curl -s https://uid9622.cn/collab/api/"
echo "回滚:    sudo ${PKG_DIR}/rollback.sh"
