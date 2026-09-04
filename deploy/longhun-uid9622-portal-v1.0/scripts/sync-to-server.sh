#!/bin/bash
# 龍魂·本地→鲲鹏三入口同步 v2.0
# DNA: #龍芯⚡️丙午·丙申·壬戌·未时·䷔噬嗑-SYNC-SERVER-v2.0-FULL
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0（核心思想层）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 功能: 同步三入口门户文件到鲲鹏 /opt/longhun-system/portal/
# 安全: 只增量同步 3 个对象，禁用 --delete（不碰远端现有文件）

set -euo pipefail

SERVER_IP="${SERVER_IP:-119.13.90.27}"
SSH_KEY="${SSH_KEY:-$HOME/.ssh/longhun_kunpeng_ed25519}"
SSH_USER="${SSH_USER:-root}"
WEB_ROOT="/opt/longhun-system/portal"
LOCAL_PORTAL="$(cd "$(dirname "$0")/../portal" && pwd)"

RED='\033[0;31m'; GREEN='\033[0;32m'; NC='\033[0m'
log_info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

[[ -f "$SSH_KEY" ]] || { log_error "SSH 密钥不存在: $SSH_KEY（默认 ~/.ssh/longhun_kunpeng_ed25519）"; exit 1; }

log_info "同步 $LOCAL_PORTAL → $SSH_USER@$SERVER_IP:$WEB_ROOT"
log_info "目标: accessible.html / developer.html / common/"

# 仅同步三入口相关对象，--delete 已禁用（保护远端现有官网文件）
rsync -avz \
    -e "ssh -i $SSH_KEY -o StrictHostKeyChecking=no" \
    --exclude='.git' --exclude='.DS_Store' \
    "$LOCAL_PORTAL/accessible.html" "$LOCAL_PORTAL/developer.html" "$LOCAL_PORTAL/common/" \
    "$SSH_USER@$SERVER_IP:$WEB_ROOT/"

ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$SSH_USER@$SERVER_IP" \
    "chown -R www-data:www-data $WEB_ROOT/common && chmod -R 755 $WEB_ROOT/common"

log_info "同步完成"
echo "访问: https://uid9622.cn/accessible.html"
echo "DNA: #龍芯⚡️丙午·丙申·壬戌·未时·䷔噬嗑-SYNC-SERVER-v2.0-DONE"
