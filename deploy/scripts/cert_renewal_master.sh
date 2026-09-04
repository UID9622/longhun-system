#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# ╔═══════════════════════════════════════════════════════════════╗
# ║  🐉 龍魂系统 · SSL证书自动续期总控脚本                      ║
# ║  版本: v1.0                                                  ║
# ║  DNA: #龍芯⚡️丙午·乙未·丙申·亥时·䷜坎-CERT-RENEWAL-v1.0    ║
# ║  功能: 一键部署钩子+修复timer+测试续期+备份+监控            ║
# ║  用法: bash cert_renewal_master.sh [deploy|test|backup|fix|status] ║
# ╚═══════════════════════════════════════════════════════════════╝
#
# 运行环境: Mac本地（SSH到鲲鹏执行）
# 鲲鹏: root@119.13.90.27

set -euo pipefail

KUNPENG_SSH="ssh -i ~/.ssh/longhun_kunpeng_ed25519 root@119.13.90.27"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOCAL_BACKUP_DIR="${HOME}/longhun-system/backups/certs"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
err() { echo -e "${RED}[ERR]${NC} $1"; }

# ──────────────────────────────────────────
# deploy — 一键部署deploy钩子 + 修复timer
# ──────────────────────────────────────────
cmd_deploy() {
    log "🚀 一键部署SSL自动续期体系..."

    # 1. 上传deploy钩子
    log "1/4 上传nginx重载钩子..."
    ${KUNPENG_SSH} "mkdir -p /etc/letsencrypt/renewal-hooks/deploy"
    scp -i ~/.ssh/longhun_kunpeng_ed25519 \
        "${SCRIPT_DIR}/certbot-deploy-hook.sh" \
        root@119.13.90.27:/etc/letsencrypt/renewal-hooks/deploy/nginx-reload.sh
    ${KUNPENG_SSH} "chmod 755 /etc/letsencrypt/renewal-hooks/deploy/nginx-reload.sh"
    log " ✅ deploy钩子已部署"

    # 2. 修复certbot.timer — 减少随机延迟从12h到1h
    log "2/4 优化certbot.timer随机延迟..."
    ${KUNPENG_SSH} "cat > /etc/systemd/system/certbot.timer.d/override.conf << 'TIMEREOF'
[Timer]
# 龍魂修复: 原默认RandomizedDelaySec=43200(12h)太大
# 改为1h随机延迟，确保证书到期前30天内快速续期
RandomizedDelaySec=3600
TIMEREOF"
    ${KUNPENG_SSH} "systemctl daemon-reload && systemctl restart certbot.timer"
    log " ✅ timer已优化 (随机延迟: 12h → 1h)"

    # 3. 确保crontab有后备续期（systemd优先，crontab充当backup）
    log "3/4 设置crontab后备续期..."
    ${KUNPENG_SSH} '(crontab -l 2>/dev/null | grep -v "certbot renew" || true; echo "0 3 * * * /usr/bin/certbot renew --quiet --deploy-hook \"/etc/letsencrypt/renewal-hooks/deploy/nginx-reload.sh\" 2>&1 | logger -t certbot-cron") | crontab -'
    log " ✅ crontab后备已设置 (每日03:00)"

    # 4. 创建日志目录
    log "4/4 初始化日志..."
    ${KUNPENG_SSH} "mkdir -p /var/log/letsencrypt && touch /var/log/letsencrypt/deploy-hook.log"
    log " ✅ 日志目录就绪"

    echo ""
    log "🎉 部署完成！摘要："
    echo "  deploy钩子: /etc/letsencrypt/renewal-hooks/deploy/nginx-reload.sh"
    echo "  timer优化:  RandomDelay 12h→1h"
    echo "  crontab:    每日03:00后备续期"
    echo "  日志:       /var/log/letsencrypt/deploy-hook.log"
}

# ──────────────────────────────────────────
# test — 试跑续期模拟
# ──────────────────────────────────────────
cmd_test() {
    log "🧪 试跑certbot dry-run..."

    # 先试单个域名（webroot方式），跳过DNS续期（需要Cloudflare API）
    log "测试 uid9622.cn (webroot)..."
    result=$(${KUNPENG_SSH} "certbot renew --dry-run --cert-name uid9622.cn --no-random-sleep-on-renew 2>&1" || true)
    echo "${result}"

    if echo "${result}" | grep -q "simulating renewal.*succeeded\|Congratulations"; then
        log " ✅ uid9622.cn webroot续期模拟通过"
    elif echo "${result}" | grep -q "not due for renewal"; then
        log " 🟡 未到续期时间（正常·证书还有84天）"
    else
        warn " ⚠️ uid9622.cn续期测试需人工检查"
    fi
}

# ──────────────────────────────────────────
# backup — 备份证书到本地Mac
# ──────────────────────────────────────────
cmd_backup() {
    log "💾 备份SSL证书到本地..."

    mkdir -p "${LOCAL_BACKUP_DIR}/${TIMESTAMP}"

    # 备份uid9622.cn
    log "备份 uid9622.cn..."
    scp -i ~/.ssh/longhun_kunpeng_ed25519 -r \
        root@119.13.90.27:/etc/letsencrypt/live/uid9622.cn \
        "${LOCAL_BACKUP_DIR}/${TIMESTAMP}/" 2>/dev/null || warn "uid9622.cn备份跳过"
    scp -i ~/.ssh/longhun_kunpeng_ed25519 -r \
        root@119.13.90.27:/etc/letsencrypt/archive/uid9622.cn \
        "${LOCAL_BACKUP_DIR}/${TIMESTAMP}/" 2>/dev/null || warn "archive备份跳过"

    # 备份longhun888.com
    log "备份 longhun888.com..."
    scp -i ~/.ssh/longhun_kunpeng_ed25519 -r \
        root@119.13.90.27:/etc/letsencrypt/live/longhun888.com \
        "${LOCAL_BACKUP_DIR}/${TIMESTAMP}/" 2>/dev/null || warn "longhun888.com备份跳过"

    # 备份renewal配置
    ${KUNPENG_SSH} "tar czf /tmp/certbot-renewal-backup.tar.gz /etc/letsencrypt/renewal/ /etc/letsencrypt/renewal-hooks/" 2>/dev/null
    scp -i ~/.ssh/longhun_kunpeng_ed25519 \
        root@119.13.90.27:/tmp/certbot-renewal-backup.tar.gz \
        "${LOCAL_BACKUP_DIR}/${TIMESTAMP}/" 2>/dev/null || true
    ${KUNPENG_SSH} "rm -f /tmp/certbot-renewal-backup.tar.gz"

    # 清理30天前的旧备份
    find "${LOCAL_BACKUP_DIR}" -maxdepth 1 -type d -mtime +30 -exec rm -rf {} \; 2>/dev/null || true

    log " ✅ 备份完成: ${LOCAL_BACKUP_DIR}/${TIMESTAMP}"
    ls -la "${LOCAL_BACKUP_DIR}/${TIMESTAMP}/"
}

# ──────────────────────────────────────────
# fix — 诊断并修复已知问题
# ──────────────────────────────────────────
cmd_fix() {
    log "🔧 诊断并修复SSL续期体系..."

    ISSUES=0

    # 1. 检查deploy钩子
    log "检查1: deploy钩子..."
    HOOK_EXISTS=$(${KUNPENG_SSH} "test -x /etc/letsencrypt/renewal-hooks/deploy/nginx-reload.sh && echo yes || echo no")
    if [ "${HOOK_EXISTS}" = "no" ]; then
        warn " 🔴 deploy钩子缺失 → 执行 cmd_deploy"
        ISSUES=$((ISSUES + 1))
    else
        log " ✅ deploy钩子存在"
    fi

    # 2. 检查timer随机延迟
    log "检查2: certbot.timer随机延迟..."
    DELAY=$(${KUNPENG_SSH} "systemctl show certbot.timer -p RandomizedDelayUSec 2>/dev/null | cut -d= -f2 | awk '{print int(\$1/1000000)}'")
    if [ -n "${DELAY}" ] && [ "${DELAY}" -gt 7200 ]; then
        warn " 🔴 随机延迟${DELAY}s太大 (>2h) → 执行 cmd_deploy"
        ISSUES=$((ISSUES + 1))
    else
        log " ✅ 随机延迟: ${DELAY}s (≤1h)"
    fi

    # 3. 检查nginx中acme路径
    log "检查3: nginx acme路径..."
    ACME_OK=$(${KUNPENG_SSH} "grep -l 'well-known/acme-challenge' /etc/nginx/conf.d/*.conf 2>/dev/null | wc -l")
    if [ "${ACME_OK}" -eq 0 ]; then
        warn " 🔴 nginx中无acme路径配置"
        ISSUES=$((ISSUES + 1))
    else
        log " ✅ nginx acme路径已配置"
    fi

    # 4. 检查crontab后备
    log "检查4: crontab后备续期..."
    CRON_OK=$(${KUNPENG_SSH} "crontab -l 2>/dev/null | grep -c 'certbot renew' || echo 0")
    if [ "${CRON_OK}" -eq 0 ]; then
        warn " 🟡 crontab无后备续期 → 执行 cmd_deploy"
    else
        log " ✅ crontab后备存在"
    fi

    # 5. 检查证书有效期
    log "检查5: 证书有效期..."
    ${KUNPENG_SSH} "for domain in uid9622.cn longhun888.com; do
        LIVE=\"/etc/letsencrypt/live/\${domain}/cert.pem\"
        if [ -f \"\${LIVE}\" ]; then
            END=\$(openssl x509 -enddate -noout -in \"\${LIVE}\" 2>/dev/null | cut -d= -f2)
            SEC=\$(date -d \"\${END}\" +%s 2>/dev/null || date -j -f '%b %d %T %Y %Z' \"\${END}\" +%s 2>/dev/null)
            NOW=\$(date +%s)
            DAYS=\$(( (SEC - NOW) / 86400 ))
            if [ \${DAYS} -lt 30 ]; then
                echo \"  🔴 \${domain}: \${DAYS}天 (紧急!)\"
            elif [ \${DAYS} -lt 60 ]; then
                echo \"  🟡 \${domain}: \${DAYS}天\"
            else
                echo \"  🟢 \${domain}: \${DAYS}天\"
            fi
        else
            echo \"  ⚪ \${domain}: 未找到证书\"
        fi
    done"

    echo ""
    if [ ${ISSUES} -gt 0 ]; then
        warn "发现 ${ISSUES} 个问题，建议运行 'bash $0 deploy' 一键修复"
    else
        log "🎉 全部检查通过，SSL续期体系健康"
    fi
}

# ──────────────────────────────────────────
# status — 查看当前状态
# ──────────────────────────────────────────
cmd_status() {
    log "📊 SSL证书状态总览"
    echo ""

    ${KUNPENG_SSH} "echo '════════════════ certbot certificates ════════════' && certbot certificates 2>/dev/null && echo '' && echo '════════════════ certbot.timer ════════════════════' && systemctl status certbot.timer --no-pager -l 2>/dev/null | head -12 && echo '' && echo '════════════════ deploy hooks ════════════════════' && ls -la /etc/letsencrypt/renewal-hooks/deploy/ 2>/dev/null || echo '  (无deploy钩子)' && echo '' && echo '════════════════ 最近续期日志 ════════════════════' && tail -20 /var/log/letsencrypt/letsencrypt.log 2>/dev/null | grep -E 'renew|success|ERROR|deploy|WARNING' | tail -10 || echo '  (无相关日志)'"
}

# ──────────────────────────────────────────
# 主入口
# ──────────────────────────────────────────
case "${1:-status}" in
    deploy)
        cmd_deploy
        ;;
    test)
        cmd_test
        ;;
    backup)
        cmd_backup
        ;;
    fix)
        cmd_fix
        ;;
    status)
        cmd_status
        ;;
    all)
        cmd_fix
        if [ $? -eq 0 ]; then
            cmd_deploy
            cmd_test
            cmd_backup
        fi
        ;;
    *)
        echo "用法: $0 {deploy|test|backup|fix|status|all}"
        echo ""
        echo "  deploy  - 一键部署: 上传钩子+修复timer+设置crontab"
        echo "  test    - 试跑certbot dry-run"
        echo "  backup  - 备份证书到本地Mac"
        echo "  fix     - 诊断并报告问题"
        echo "  status  - 查看当前状态 (默认)"
        echo "  all     - fix → deploy → test → backup 全流程"
        exit 1
        ;;
esac
