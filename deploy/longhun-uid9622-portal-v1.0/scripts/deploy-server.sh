#!/bin/bash
# 龍魂·uid9622.cn 三入口门户 · 鲲鹏服务器增量部署 v2.0
# DNA: #龍芯⚡️丙午·丙申·壬戌·未时·䷔噬嗑-DEPLOY-SERVER-v2.0-FULL
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0（核心思想层）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 功能: 三入口门户增量部署到鲲鹏(119.13.90.27)，不动现有官网配置
# 安全: 幂等检查 → 备份 → 增量location → nginx -t → reload → 公网验证 → 日志 → Bark回调
# 用法:
#   bash scripts/deploy-server.sh                # 默认鲲鹏
#   BARK_KEY=xxx bash scripts/deploy-server.sh   # 带回调通知
#   SERVER_IP=1.2.3.4 bash scripts/deploy-server.sh  # 指定服务器

set -euo pipefail

# ── 配置（环境变量可覆盖）──────────────────────────────
SERVER_IP="${SERVER_IP:-119.13.90.27}"
SSH_USER="${SSH_USER:-root}"
SSH_KEY="${SSH_KEY:-$HOME/.ssh/longhun_kunpeng_ed25519}"
REMOTE_ROOT="/opt/longhun-system/portal"
NGINX_INC="/etc/nginx/conf.d/longhun-apps-static.inc"
DEPLOY_TAG="3gates"
PORTAL_SRC="$(cd "$(dirname "$0")/../portal" && pwd)"
LOG_DIR="${LOG_DIR:-$HOME/longhun-system/logs}"
BARK_KEY="${BARK_KEY:-}"
BARK_SERVER="${BARK_SERVER:-https://api.day.app}"

# ── 颜色与日志 ──────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
TS="$(date +%Y%m%d-%H%M%S)"
LOG_FILE="$LOG_DIR/portal-deploy-$TS.log"
mkdir -p "$LOG_DIR"

log_info()  { echo -e "${GREEN}[INFO]${NC}  $(date '+%F %T') $1" | tee -a "$LOG_FILE"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $(date '+%F %T') $1" | tee -a "$LOG_FILE"; }
log_error() { echo -e "${RED}[ERROR]${NC} $(date '+%F %T') $1" | tee -a "$LOG_FILE"; }

# ── Bark 回调（部署完成通知）──────────────────────────
notify() {
    local title="$1" body="$2"
    [[ -z "$BARK_KEY" ]] && return 0
    local encoded
    encoded=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$body" 2>/dev/null || echo "$body")
    local resp code
    resp=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 \
        "$BARK_SERVER/$BARK_KEY/$title/$encoded?level=timeSensitive" 2>/dev/null) || code="000"
    code="${resp:-000}"
    log_info "Bark回调: HTTP $code (title=$title)"
}

# ── 步骤0: 前置检查 ─────────────────────────────────
log_info "=== 龍魂·三入口门户 鲲鹏部署 v2.0 ==="
log_info "目标: $SSH_USER@$SERVER_IP · 远端根: $REMOTE_ROOT"
log_info "日志: $LOG_FILE"
log_info "SSH密钥: $SSH_KEY"

[[ -f "$SSH_KEY" ]] || { log_error "SSH密钥不存在: $SSH_KEY"; notify "❌部署失败" "SSH密钥不存在"; exit 1; }
command -v scp >/dev/null || { log_error "缺少 scp"; exit 1; }

# ── 步骤1: 远端连通性 + 现状快照 ────────────────────
log_info "步骤1: 远端连通性检查..."
if ! ssh -i "$SSH_KEY" -o ConnectTimeout=10 -o StrictHostKeyChecking=no \
    "$SSH_USER@$SERVER_IP" "echo OK && hostname" >/dev/null 2>&1; then
    log_error "SSH 连接失败"
    notify "❌部署失败" "SSH连接失败 $SERVER_IP"
    exit 1
fi
log_info "SSH 连接成功"

ALREADY=$(
ssh -i "$SSH_KEY" -o ConnectTimeout=10 -o StrictHostKeyChecking=no \
    "$SSH_USER@$SERVER_IP" "grep -c '$DEPLOY_TAG\|accessible.html' $NGINX_INC 2>/dev/null || echo 0"
)
if [[ "${ALREADY:-0}" -gt 0 ]]; then
    log_warn "检测到已有三入口 location ($ALREADY 处)，跳过追加"
    SKIP_APPEND=1
else
    SKIP_APPEND=0
fi

# ── 步骤2: 同步文件 ─────────────────────────────────
log_info "步骤2: 同步三入口文件 → $REMOTE_ROOT"
scp -i "$SSH_KEY" -o StrictHostKeyChecking=no \
    "$PORTAL_SRC/accessible.html" "$PORTAL_SRC/developer.html" \
    "$SSH_USER@$SERVER_IP:$REMOTE_ROOT/" 2>>"$LOG_FILE" \
    && log_info "页面同步完成"
scp -i "$SSH_KEY" -o StrictHostKeyChecking=no -r \
    "$PORTAL_SRC/common" \
    "$SSH_USER@$SERVER_IP:$REMOTE_ROOT/" 2>>"$LOG_FILE" \
    && log_info "common 资源同步完成"

# ── 步骤3: 生成 nginx 增量 location ─────────────────
if [[ "$SKIP_APPEND" == "0" ]]; then
    log_info "步骤3: 生成 nginx 增量 location..."
    INC_FILE="/tmp/lh-${DEPLOY_TAG}-append-$TS.inc"
    cat > "$INC_FILE" <<EOF

    # ── 三入口门户 (deploy-server.sh v2.0 $TS) ──
    location = /accessible.html {
        alias $REMOTE_ROOT/accessible.html;
        default_type text/html;
        add_header X-Data-Sovereignty "China-HuaweiCloud-Kunpeng" always;
    }
    location = /developer.html {
        alias $REMOTE_ROOT/developer.html;
        default_type text/html;
        add_header X-Data-Sovereignty "China-HuaweiCloud-Kunpeng" always;
    }
    location /common/ {
        alias $REMOTE_ROOT/common/;
        add_header Cache-Control "public, max-age=86400";
        add_header X-Data-Sovereignty "China-HuaweiCloud-Kunpeng" always;
    }
EOF
    scp -i "$SSH_KEY" -o StrictHostKeyChecking=no \
        "$INC_FILE" "$SSH_USER@$SERVER_IP:/tmp/lh-${DEPLOY_TAG}-append.inc" 2>>"$LOG_FILE"
    rm -f "$INC_FILE"

    # ── 步骤4: 备份 → 追加 → 校验 → 重载 ────────────
    log_info "步骤4: 备份 nginx 配置..."
    ssh -i "$SSH_KEY" -o ConnectTimeout=10 -o StrictHostKeyChecking=no \
        "$SSH_USER@$SERVER_IP" "
        cp $NGINX_INC ${NGINX_INC}.bak-$DEPLOY_TAG-\$(date +%Y%m%d-%H%M%S) &&
        cat /tmp/lh-${DEPLOY_TAG}-append.inc >> $NGINX_INC &&
        rm -f /tmp/lh-${DEPLOY_TAG}-append.inc &&
        echo '--- 追加完成，校验 nginx ---' &&
        nginx -t &&
        systemctl reload nginx &&
        echo '--- nginx reload OK ---'
    " 2>&1 | tee -a "$LOG_FILE" | sed 's/^/  [远端] /'
    log_info "nginx 配置追加 + 校验 + reload 完成"
else
    log_info "步骤3-4: 已存在配置，跳过追加（幂等）"
fi

# ── 步骤5: 公网验证 ─────────────────────────────────
log_info "步骤5: 公网验证..."
RESULTS=""
for u in /accessible.html /developer.html /common/accessible.css /common/main.js /index.html; do
    code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "https://uid9622.cn$u" 2>/dev/null)
    RESULTS="$RESULTS $u=$code"
    log_info "   GET https://uid9622.cn$u → $code"
done

# ── 步骤6: 判定 + 回调 ─────────────────────────────
if echo "$RESULTS" | grep -qE '=000|=404|=5[0-9][0-9]'; then
    log_error "部署验证未全绿: $RESULTS"
    notify "❌三入口部署未全绿" "$RESULTS"
    exit 1
fi
log_info "✅ 部署验证全绿"
notify "✅三入口门户部署完成" "三入口+common+官网全部200"

log_info "=== 部署完成 ==="
log_info "DNA: #龍芯⚡️丙午·丙申·壬戌·未时·䷔噬嗑-DEPLOY-SERVER-v2.0-DONE"
echo ""
echo "🐉 三入口门户已上线:"
echo "   普通者:   https://uid9622.cn/"
echo "   无障碍:   https://uid9622.cn/accessible.html"
echo "   开发者:   https://uid9622.cn/developer.html"
echo "   部署日志: $LOG_FILE"
