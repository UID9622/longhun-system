#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env bash
# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  🐉 龍魂·支付锚定取证引擎 · 鲲鹏部署脚本 v1.0                               ║
# ║  Deploy: 本地Mac → 华为云鲲鹏ECS + OBS不可删除备份                         ║
# ╠══════════════════════════════════════════════════════════════════════════╣
# ║  DNA: #龍芯⚡️2026-07-12-PAY-ANCHOR-KUNPENG-DEPLOY-v1.0                    ║
# ║  目标: 华为 TaiShan 200 · 鲲鹏920 · openEuler / Ubuntu 24.04              ║
# ║  架构: ARM64 · Python 3.10+                                               ║
# ║  铁律:                                                                     ║
# ║    数据持久化 — 锚定数据写入 /data/longhun/pay-anchor (独立数据盘)           ║
# ║    不可删除 — 上传后 OBS WORM 锁定 + 本地同步保护                            ║
# ║    双重备份 — 华为云 OBS 北京主区 + 广州灾备 (≥500km)                        ║
# ║    自动同步 — cron 每10分钟本地→鲲鹏增量同步                                  ║
# ║    健康监控 — systemd 自动重启 + Bark 实时推送                                ║
# ║    主权声明 — 所有数据存储在中国境内·受中国法律保护                             ║
# ╚══════════════════════════════════════════════════════════════════════════╝
#
# 用法:
#   bash deploy/pay-anchor/deploy-pay-anchor-kunpeng.sh setup     # 首次部署
#   bash deploy/pay-anchor/deploy-pay-anchor-kunpeng.sh sync      # 增量同步
#   bash deploy/pay-anchor/deploy-pay-anchor-kunpeng.sh status    # 查看状态
#   bash deploy/pay-anchor/deploy-pay-anchor-kunpeng.sh verify    # 验证完整性
#   bash deploy/pay-anchor/deploy-pay-anchor-kunpeng.sh obs-backup # OBS 不可删除备份
#   bash deploy/pay-anchor/deploy-pay-anchor-kunpeng.sh obs-report # OBS 状态报告

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CONFIG_FILE="${PROJECT_ROOT}/deploy/.kunpeng_config"
SERVICE_NAME="longhun-pay-anchor"
DEPLOY_PATH=""
PORT="9623"

# ─── 颜色 ───
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

log()  { echo -e "$(date '+%H:%M:%S') $*"; }
ok()   { log "${GREEN}✅${NC} $*"; }
warn() { log "${YELLOW}⚠️${NC}  $*"; }
fail() { log "${RED}🔴${NC} $*"; exit 1; }
info() { log "${CYAN}▶${NC}  $*"; }
header() { echo -e "\n${BOLD}${CYAN}$*${NC}"; }

# ─── 加载配置 ───
load_config() {
    if [[ -f "$CONFIG_FILE" ]]; then
        source "$CONFIG_FILE"
        DEPLOY_PATH="${KUNPENG_DEPLOY_PATH:-/opt/longhun-system}"
        ok "已加载鲲鹏配置"
    else
        fail "请先配置鲲鹏连接: bash deploy/connect-kunpeng.sh config"
    fi
}

# ─── SSH 命令 ───
ssh_kunpeng() {
    ssh -p "${KUNPENG_SSH_PORT}" -i "${KUNPENG_KEY}" \
        -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10 \
        "${KUNPENG_USER}@${KUNPENG_MGMT_IP}" "$@"
}

# ═══════════════════════════════════════════════════════════
# 步骤 1: 第一次部署
# ═══════════════════════════════════════════════════════════

do_setup() {
    header "🐉 支付锚定·鲲鹏部署"

    # ── 1.1 连接测试 ──
    info "1/7 测试连接..."
    if ! ssh_kunpeng "echo ok" &>/dev/null; then
        fail "无法连接鲲鹏 ${KUNPENG_MGMT_IP}，请检查 SSH 配置"
    fi
    ok "SSH 连接正常"

    # ── 1.2 创建鲲鹏端目录结构 ──
    info "2/7 创建目录结构..."
    ssh_kunpeng "bash -s" << 'ENDSSH'
# 主部署目录
mkdir -p /opt/longhun-system/bin
mkdir -p /opt/longhun-system/deploy/pay-anchor
mkdir -p /opt/longhun-system/deploy/auto_sync

# 持久数据盘（独立挂载 /data）
PAY_ANCHOR_DATA="/data/longhun/pay-anchor"
mkdir -p "${PAY_ANCHOR_DATA}/anchors"       # 锚定包 JSON
mkdir -p "${PAY_ANCHOR_DATA}/legal-logs"    # 法律查档日志
mkdir -p "${PAY_ANCHOR_DATA}/dna-registry"  # DNA 登记册
mkdir -p "${PAY_ANCHOR_DATA}/merkle"        # Merkle 链索引
mkdir -p "${PAY_ANCHOR_DATA}/snapshots"     # 定期快照

# 知识矩阵路径
mkdir -p /opt/longhun-system/articles/pay-anchor-records
mkdir -p /opt/longhun-system/L7_数据层

# 应用日志
mkdir -p /var/log/longhun/pay-anchor

# 权限
chown -R longhun:longhun /data/longhun 2>/dev/null || true
chown -R longhun:longhun /opt/longhun-system 2>/dev/null || true
chown -R longhun:longhun /var/log/longhun/pay-anchor 2>/dev/null || true
chmod 750 /data/longhun/pay-anchor

echo "✅ 目录结构已创建"
ENDSSH

    # ── 1.3 同步引擎文件 ──
    info "3/7 同步引擎文件..."
    rsync -avz --progress \
        -e "ssh -p ${KUNPENG_SSH_PORT} -i ${KUNPENG_KEY} -o StrictHostKeyChecking=accept-new" \
        "${PROJECT_ROOT}/bin/lh_pay_anchor_forensic.py" \
        "${PROJECT_ROOT}/bin/lh_obs_immutable_backup.py" \
        "${PROJECT_ROOT}/bin/lh_dna_sovereignty_bridge.py" \
        "${PROJECT_ROOT}/bin/lh_unified_dna_registry.py" \
        "${KUNPENG_USER}@${KUNPENG_MGMT_IP}:${DEPLOY_PATH}/bin/" \
        && ok "引擎文件同步完成"

    # 同步 crypto-stack
    info "   同步 crypto-stack..."
    ssh_kunpeng "mkdir -p ${DEPLOY_PATH}/crypto-stack/src"
    rsync -avz \
        -e "ssh -p ${KUNPENG_SSH_PORT} -i ${KUNPENG_KEY} -o StrictHostKeyChecking=accept-new" \
        "${PROJECT_ROOT}/crypto-stack/src/l1_physical.py" \
        "${KUNPENG_USER}@${KUNPENG_MGMT_IP}:${DEPLOY_PATH}/crypto-stack/src/" \
        && ok "crypto-stack 同步完成"

    # ── 1.4 安装 Python 依赖 ──
    info "4/7 安装 Python 依赖..."
    ssh_kunpeng "bash -s" << 'ENDSSH'
if command -v pip3 &>/dev/null; then
    pip3 install obs esdk-obs-python 2>/dev/null || true
fi
echo "✅ 依赖检查完成"
ENDSSH

    # ── 1.5 部署 systemd 服务 ──
    info "5/7 部署 systemd 服务..."
    ssh_kunpeng "bash -s" <<ENDSSH
cat > /etc/systemd/system/${SERVICE_NAME}.service << 'SERVICEEOF'
[Unit]
Description=龍魂·支付锚定取证引擎
Documentation=https://uid9622.cn
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=longhun
Group=longhun
WorkingDirectory=/opt/longhun-system
Environment=PYTHONUNBUFFERED=1
Environment=LONGHUN_ENV=production
Environment=PAY_ANCHOR_DATA=/data/longhun/pay-anchor
Environment=ANCHOR_API_PORT=${PORT}
ExecStart=/usr/bin/python3 /opt/longhun-system/bin/lh_pay_anchor_forensic.py serve --port ${PORT} --data-dir /data/longhun/pay-anchor
ExecReload=/bin/kill -HUP \$MAINPID
Restart=always
RestartSec=10
StartLimitBurst=5
StartLimitIntervalSec=60
StandardOutput=append:/var/log/longhun/pay-anchor/api.log
StandardError=append:/var/log/longhun/pay-anchor/api_error.log
LimitNOFILE=65536
MemoryMax=1G
CPUQuota=200%

[Install]
WantedBy=multi-user.target
SERVICEEOF

systemctl daemon-reload
systemctl enable ${SERVICE_NAME}
echo "✅ systemd 服务已配置"
ENDSSH

    # ── 1.6 配置 OBS 备份 cron ──
    info "6/7 配置 OBS 自动备份..."
    ssh_kunpeng "bash -s" << 'ENDSSH'
OBS_BACKUP_SCRIPT="/opt/longhun-system/deploy/pay-anchor/obs-auto-backup.sh"

cat > "${OBS_BACKUP_SCRIPT}" << 'CRONEOF'
#!/bin/bash
# 📦 龍魂·OBS 自动备份（不可删除）
# 每小时将锚定数据同步到华为云OBS
LOG="/var/log/longhun/pay-anchor/obs_backup.log"

{
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 📦 OBS备份启动"
    
    # 上传新增锚定包
    cd /opt/longhun-system
    for f in /data/longhun/pay-anchor/anchors/*.json; do
        if [ -f "\$f" ]; then
            python3 bin/lh_obs_immutable_backup.py upload --file "\$f" --type pay-anchor --region primary 2>&1
        fi
    done
    
    # 上传法律查档日志
    for f in /data/longhun/pay-anchor/legal-logs/*.jsonl; do
        if [ -f "\$f" ]; then
            python3 bin/lh_obs_immutable_backup.py upload --file "\$f" --type legal-log --region primary 2>&1
        fi
    done
    
    # 上传DNA登记册
    REGISTRY="/opt/longhun-system/L7_数据层/dna_registry_index.json"
    if [ -f "\$REGISTRY" ]; then
        python3 bin/lh_obs_immutable_backup.py upload --file "\$REGISTRY" --type dna-registry --region primary 2>&1
    fi
    
    # 每天凌晨3点做一次跨区域灾备
    HOUR=\$(date +%H)
    if [ "\$HOUR" = "03" ]; then
        python3 bin/lh_obs_immutable_backup.py cross-region-sync 2>&1
    fi
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ OBS备份完成"
} >> "\$LOG" 2>&1
CRONEOF

chmod +x "${OBS_BACKUP_SCRIPT}"

# 添加 cron（每小时）
CRON_JOB="0 * * * * /bin/bash ${OBS_BACKUP_SCRIPT}"
(crontab -l 2>/dev/null | grep -v "${OBS_BACKUP_SCRIPT}"; echo "${CRON_JOB}") | crontab -

echo "✅ OBS 自动备份已配置（每小时 + 每天凌晨3点跨区域灾备）"
ENDSSH

    # ── 1.7 启动服务 ──
    info "7/7 启动服务..."
    ssh_kunpeng "systemctl restart ${SERVICE_NAME}" || true
    sleep 2
    ssh_kunpeng "systemctl status ${SERVICE_NAME} --no-pager -l" || true
    ok "部署完成!"

    # ── 打印摘要 ──
    header "📋 部署摘要"
    echo ""
    echo "  服务:     ${SERVICE_NAME} (端口 ${PORT})"
    echo "  设备:     华为云鲲鹏 ${KUNPENG_MGMT_IP}"
    echo "  数据盘:   /data/longhun/pay-anchor/ (独立持久化)"
    echo "  备份:     华为云 OBS 北京主区 + 广州灾备 (≥500km)"
    echo "  不可删除: ✅ WORM + Merkle 链 + 版本控制"
    echo "  主权:     存储在中国境内华为云·受中国法律保护"
    echo ""
    echo "  监控:"
    echo "    systemctl status ${SERVICE_NAME}"
    echo "    tail -f /var/log/longhun/pay-anchor/api.log"
    echo ""
    echo "  OBS 备份:"
    echo "    bash deploy/pay-anchor/deploy-pay-anchor-kunpeng.sh obs-backup"
    echo "    bash deploy/pay-anchor/deploy-pay-anchor-kunpeng.sh obs-report"
    echo ""
}

# ═══════════════════════════════════════════════════════════
# 增量同步（日常更新引擎代码）
# ═══════════════════════════════════════════════════════════

do_sync() {
    header "🔄 增量同步→鲲鹏"

    # 同步核心引擎文件
    FILES=(
        "bin/lh_pay_anchor_forensic.py"
        "bin/lh_obs_immutable_backup.py"
        "bin/lh_dna_sovereignty_bridge.py"
        "bin/lh_unified_dna_registry.py"
        "crypto-stack/src/l1_physical.py"
        "L7_数据层/dna_registry.jsonl"
        "L7_数据层/dna_registry_index.json"
        "articles/pay-anchor-records/"
    )

    for f in "${FILES[@]}"; do
        if [[ -e "${PROJECT_ROOT}/${f}" ]]; then
            rsync -avz \
                -e "ssh -p ${KUNPENG_SSH_PORT} -i ${KUNPENG_KEY} -o StrictHostKeyChecking=accept-new" \
                "${PROJECT_ROOT}/${f}" \
                "${KUNPENG_USER}@${KUNPENG_MGMT_IP}:${DEPLOY_PATH}/${f}" 2>&1 | tail -1
        fi
    done

    # 重启服务使其生效
    info "重启服务..."
    ssh_kunpeng "systemctl restart ${SERVICE_NAME}" || true
    ok "同步+重启完成"
}

# ═══════════════════════════════════════════════════════════
# 状态查看
# ═══════════════════════════════════════════════════════════

do_status() {
    header "📊 支付锚定·鲲鹏状态"

    echo ""
    echo "── 服务状态 ──"
    ssh_kunpeng "systemctl status ${SERVICE_NAME} --no-pager -l" 2>&1 || true

    echo ""
    echo "── 数据存储 ──"
    ssh_kunpeng "bash -s" << 'ENDSSH'
echo "持久数据盘:"
du -sh /data/longhun/pay-anchor/ 2>/dev/null || echo "  (未挂载)"
echo ""
echo "锚定包: $(ls /data/longhun/pay-anchor/anchors/*.json 2>/dev/null | wc -l) 条"
echo "法律日志: $(ls /data/longhun/pay-anchor/legal-logs/*.jsonl 2>/dev/null | wc -l) 条"
echo "DNA登记: $(ls /opt/longhun-system/L7_数据层/dna_registry.jsonl 2>/dev/null && wc -l < /opt/longhun-system/L7_数据层/dna_registry.jsonl || echo 0) 条"
echo ""
echo "最近5条锚定:"
ls -lt /data/longhun/pay-anchor/anchors/*.json 2>/dev/null | head -5 || echo "  (无记录)"
ENDSSH

    echo ""
    echo "── API 端点 ──"
    ssh_kunpeng "curl -s http://localhost:${PORT}/health 2>/dev/null || echo '  (服务未响应)'"
    echo ""
}

# ═══════════════════════════════════════════════════════════
# OBS 备份 & 报告
# ═══════════════════════════════════════════════════════════

do_obs_backup() {
    header "📦 华为云 OBS 不可删除备份"
    ssh_kunpeng "cd ${DEPLOY_PATH} && python3 bin/lh_obs_immutable_backup.py report" 2>&1 || true
}

do_obs_report() {
    header "📋 不可删除备份状态报告"
    ssh_kunpeng "cd ${DEPLOY_PATH} && python3 bin/lh_obs_immutable_backup.py report" 2>&1 || true
}

# ═══════════════════════════════════════════════════════════
# 验证完整性
# ═══════════════════════════════════════════════════════════

do_verify() {
    header "🔍 验证数据完整性"

    echo ""
    echo "── 本地 Merkle 链 ──"
    ssh_kunpeng "cd ${DEPLOY_PATH} && python3 bin/lh_obs_immutable_backup.py verify --type pay-anchor" 2>&1 || true

    echo ""
    echo "── DNA 登记册 ──"
    ssh_kunpeng "cd ${DEPLOY_PATH} && python3 -c \"
import json
from pathlib import Path
idx = json.loads(Path('L7_数据层/dna_registry_index.json').read_text())
print(f'索引条目: {idx.get(\\\"count\\\", 0)}')
entries = idx.get('entries', [])
pay = [e for e in entries if e.get('type') == 'PAY-ANCHOR']
print(f'支付锚定: {len(pay)} 条')
print(f'总类型: {set(e.get(\\\"type\\\", \\\"?\\\") for e in entries)}')
\"" 2>&1 || true

    echo ""
    echo "── 锚定包数量匹配检查 ──"
    ssh_kunpeng "bash -s" << 'ENDSSH'
ANCHORS=$(ls /data/longhun/pay-anchor/anchors/*.json 2>/dev/null | wc -l)
ARTICLES=$(ls /opt/longhun-system/articles/pay-anchor-records/*.md 2>/dev/null | wc -l)
echo "锚定包 JSON: ${ANCHORS}"
echo "知识矩阵 MD:  ${ARTICLES}"
if [ "${ANCHORS}" -eq "${ARTICLES}" ]; then
    echo "✅ 数量一致"
else
    echo "⚠️ 数量不一致 (差 $((ANCHORS - ARTICLES)))"
fi
ENDSSH
}

# ═══════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════

main() {
    load_config

    case "${1:-}" in
        setup|deploy)
            do_setup
            ;;
        sync|update)
            do_sync
            ;;
        status|check)
            do_status
            ;;
        obs-backup|backup)
            do_obs_backup
            ;;
        obs-report|report)
            do_obs_report
            ;;
        verify|check-integrity)
            do_verify
            ;;
        *)
            echo "🐉 龍魂·支付锚定·鲲鹏部署"
            echo ""
            echo "用法:"
            echo "  bash deploy/pay-anchor/deploy-pay-anchor-kunpeng.sh setup      首次部署"
            echo "  bash deploy/pay-anchor/deploy-pay-anchor-kunpeng.sh sync       增量同步"
            echo "  bash deploy/pay-anchor/deploy-pay-anchor-kunpeng.sh status     查看状态"
            echo "  bash deploy/pay-anchor/deploy-pay-anchor-kunpeng.sh verify     验证完整性"
            echo "  bash deploy/pay-anchor/deploy-pay-anchor-kunpeng.sh obs-backup OBS不可删除备份"
            echo "  bash deploy/pay-anchor/deploy-pay-anchor-kunpeng.sh obs-report 备份状态报告"
            ;;
    esac
}

main "$@"
