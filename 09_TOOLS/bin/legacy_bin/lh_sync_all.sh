#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂 · 全系统同步脚本
# DNA: #龍芯⚡️丙午·乙未·壬午·丙午·䷳艮为山-SYNC-ALL-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#
# 一键同步到所有目的地:
#   1️⃣ 本地备份 (~/.龍魂/backups/)
#   2️⃣ Gitee 国内仓库
#   3️⃣ GitHub (可选)
#   4️⃣ GitCode (可选)
#   5️⃣ 鲲鹏服务器 (可选)
#   6️⃣ 官网 Portal (可选)
#   7️⃣ Notion (可选)
#
# 用法:
#   bash bin/lh_sync_all.sh              # 同步所有已配置目的地
#   bash bin/lh_sync_all.sh --skip-git   # 跳过 Git 推送
#   bash bin/lh_sync_all.sh --dry        # 预览模式
#   bash bin/lh_sync_all.sh --quick      # 快速模式: 备份+Gitee

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BIN_DIR="$ROOT/bin"
LOG_DIR="$HOME/.龍魂/logs"
SYNC_LOG="$LOG_DIR/sync_all_$(date '+%Y%m%d').log"

mkdir -p "$LOG_DIR"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; BLUE='\033[0;34m'; NC='\033[0m'

RESULTS_SUCCESS=()
RESULTS_FAIL=()
RESULTS_SKIP=()

log()  { echo -e "$(date '+%H:%M:%S') $*" | tee -a "$SYNC_LOG"; }
ok()   { log "${GREEN}✅${NC} $*"; RESULTS_SUCCESS+=("$*"); }
fail() { log "${RED}🔴${NC} $*"; RESULTS_FAIL+=("$*"); }
skip() { log "${YELLOW}⏭️${NC}  $*"; RESULTS_SKIP+=("$*"); }
step() { echo ""; log "${BLUE}═══ $* ═══${NC}"; }

DRY_RUN=false
QUICK_MODE=false
SKIP_GIT=false

for arg in "$@"; do
    case "$arg" in
        --dry|--dry-run) DRY_RUN=true ;;
        --quick) QUICK_MODE=true ;;
        --skip-git) SKIP_GIT=true ;;
    esac
done

# ═══════════════════════════════════════════
# 步骤 1: 本地备份
# ═══════════════════════════════════════════
step "1️⃣  本地备份"
BACKUP_DIR="$HOME/.龍魂/backups/sync_$(date '+%Y%m%d_%H%M%S')"
if $DRY_RUN; then
    skip "预览模式 — 跳过备份"
else
    mkdir -p "$BACKUP_DIR"
    
    # 核心配置
    cp "$ROOT/CONSTITUTION.md" "$BACKUP_DIR/" 2>/dev/null || true
    cp "$ROOT/AGENTS.md" "$BACKUP_DIR/" 2>/dev/null || true
    cp "$ROOT/CNSH-PROTOCOL.md" "$BACKUP_DIR/" 2>/dev/null || true
    cp "$ROOT/P0_ETERNAL_LOCK.md" "$BACKUP_DIR/" 2>/dev/null || true
    cp "$ROOT/MASTER_REGISTRY.md" "$BACKUP_DIR/" 2>/dev/null || true
    
    # 协议目录
    mkdir -p "$BACKUP_DIR/01_protocols"
    cp -r "$ROOT/01_protocols"/* "$BACKUP_DIR/01_protocols/" 2>/dev/null || true
    
    # 技能库
    mkdir -p "$BACKUP_DIR/01_技能庫"
    cp -r "$ROOT/01_技能庫"/* "$BACKUP_DIR/02_SKILLS/" 2>/dev/null || true
    
    # bin 脚本
    mkdir -p "$BACKUP_DIR/bin"
    cp -r "$ROOT/bin"/* "$BACKUP_DIR/bin/" 2>/dev/null || true
    
    # 知识图谱
    mkdir -p "$BACKUP_DIR/03_知識圖譜"
    cp -r "$ROOT/03_知識圖譜"/* "$BACKUP_DIR/03_KNOWLEDGE_GRAPH/" 2>/dev/null || true
    
    BACKUP_SIZE=$(du -sh "$BACKUP_DIR" 2>/dev/null | awk '{print $1}')
    ok "本地备份: $BACKUP_DIR ($BACKUP_SIZE)"
    
    # 清理30天前的同步备份
    find "$HOME/.龍魂/backups" -maxdepth 1 -type d -name "sync_*" -mtime +30 -exec rm -rf {} \; 2>/dev/null || true
fi

# ═══════════════════════════════════════════
# 步骤 2: Gitee 推送
# ═══════════════════════════════════════════
if $SKIP_GIT; then
    skip "跳过 Git 推送"
else
    step "2️⃣  Gitee 国内仓库"
    if git remote get-url gitee &>/dev/null; then
        if $DRY_RUN; then
            skip "预览模式 — 跳过推送"
        else
            cd "$ROOT"
            git fetch gitee main 2>/dev/null || true
            
            # 检查是否有东西要推
            AHEAD=$(git rev-list --count "gitee/main..main" 2>/dev/null || echo "0")
            if [[ "$AHEAD" == "0" ]] || [[ "$AHEAD" == "?" ]]; then
                skip "Gitee 已是最新 (无新提交)"
            else
                if git push gitee main:main 2>&1 | tee -a "$SYNC_LOG"; then
                    ok "Gitee 推送成功 ($AHEAD commits)"
                else
                    fail "Gitee 推送失败"
                fi
            fi
        fi
    else
        skip "Gitee remote 未配置"
    fi
fi

# ═══════════════════════════════════════════
# 步骤 3: GitCode 推送
# ═══════════════════════════════════════════
if ! $SKIP_GIT; then
    step "3️⃣  GitCode 仓库"
    if git remote get-url gitcode &>/dev/null; then
        if $DRY_RUN; then
            skip "预览模式 — 跳过推送"
        else
            cd "$ROOT"
            git fetch gitcode main 2>/dev/null || true
            AHEAD=$(git rev-list --count "gitcode/main..main" 2>/dev/null || echo "0")
            if [[ "$AHEAD" == "0" ]]; then
                skip "GitCode 已是最新"
            else
                git push gitcode main:main 2>&1 | tee -a "$SYNC_LOG" && \
                    ok "GitCode 推送成功" || fail "GitCode 推送失败"
            fi
        fi
    else
        skip "GitCode remote 未配置"
    fi
fi

# ═══════════════════════════════════════════
# 步骤 4: 鲲鹏服务器同步
# ═══════════════════════════════════════════
if ! $QUICK_MODE; then
    step "4️⃣  鲲鹏服务器同步"
    KUNPENG_SCRIPT="$ROOT/deploy/sync-to-kunpeng.sh"
    if [[ -f "$KUNPENG_SCRIPT" ]] && [[ -f "$ROOT/deploy/.kunpeng_config" ]]; then
        if $DRY_RUN; then
            skip "预览模式 — 跳过同步"
        else
            bash "$KUNPENG_SCRIPT" full 2>&1 | tee -a "$SYNC_LOG" && \
                ok "鲲鹏服务器同步成功" || fail "鲲鹏服务器同步失败"
        fi
    else
        skip "鲲鹏未配置 (缺少 deploy/.kunpeng_config)"
    fi
fi

# ═══════════════════════════════════════════
# 步骤 5: Notion 同步
# ═══════════════════════════════════════════
if ! $QUICK_MODE; then
    step "5️⃣  Notion 知识库同步"
    NOTION_SYNC="$ROOT/cnsh/core/notion/cnsh_notion_bridge.py"
    if [[ -f "$NOTION_SYNC" ]]; then
        if $DRY_RUN; then
            skip "预览模式 — 跳过同步"
        else
            python3 "$NOTION_SYNC" --sync 2>&1 | tee -a "$SYNC_LOG" && \
                ok "Notion 同步成功" || fail "Notion 同步失败"
        fi
    else
        skip "Notion 桥接脚本不存在"
    fi
fi

# ═══════════════════════════════════════════
# 结果汇总
# ═══════════════════════════════════════════
step "📊 同步结果汇总"
echo ""

printf "  ${GREEN}成功: %d${NC}\n" "${#RESULTS_SUCCESS[@]}"
for r in "${RESULTS_SUCCESS[@]}"; do
    echo "    ✅ $r"
done

printf "  ${RED}失败: %d${NC}\n" "${#RESULTS_FAIL[@]}"
for r in "${RESULTS_FAIL[@]}"; do
    echo "    🔴 $r"
done

printf "  ${YELLOW}跳过: %d${NC}\n" "${#RESULTS_SKIP[@]}"

echo ""
echo "  DNA: ${CYAN}#龍芯⚡️丙午·乙未·壬午·丙午·䷳艮为山-SYNC-ALL-v1.0${NC}"
echo "  日志: $SYNC_LOG"
echo ""

if [[ ${#RESULTS_FAIL[@]} -gt 0 ]]; then
    exit 1
fi
