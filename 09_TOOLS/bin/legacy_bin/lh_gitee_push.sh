#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂 · Gitee 国内仓库同步推送
# DNA: #龍芯⚡️丙午·乙未·壬午·丙午·䷳艮为山-GITEE-PUSH-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#
# 用法:
#   bash bin/lh_gitee_push.sh              # 推送到 gitee (默认)
#   bash bin/lh_gitee_push.sh --dry        # 预览变更
#   bash bin/lh_gitee_push.sh --force      # 强制推送
#   bash bin/lh_gitee_push.sh --tag v1.0   # 推送并打标签
#
# 前置: git remote gitee 已配置
#   git remote add gitee git@gitee.com:uid9622_admin/longhun-system-core.git

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'
log()  { echo -e "$(date '+%H:%M:%S') $*"; }
ok()   { log "${GREEN}✅${NC} $*"; }
warn() { log "${YELLOW}⚠️${NC}  $*"; }
fail() { log "${RED}🔴${NC} $*"; exit 1; }

REMOTE="${GITEE_REMOTE:-gitee}"
BRANCH="${GITEE_BRANCH:-main}"

# ── 检查 remote 是否存在 ──
check_remote() {
    if ! git remote get-url "$REMOTE" &>/dev/null; then
        fail "Gitee remote '$REMOTE' 未配置"
        echo ""
        echo "  添加方法:"
        echo "    git remote add gitee git@gitee.com:uid9622_admin/longhun-system-core.git"
        echo ""
    fi
    local url
    url=$(git remote get-url "$REMOTE")
    log "📍 Gitee remote: ${CYAN}${url}${NC}"
}

# ── 敏感文件审计 ──
audit_sensitive() {
    log "🔍 敏感文件审计..."
    local sensitive=0
    local patterns=(
        "*.pem" "*.key" "*.asc" "*.gpg" "*.pfx" "*.p12"
        ".env" ".env.*" "*.secret" "*.token" "credentials*"
        "*.master_key" "*.password" "*.htpasswd"
    )

    for pattern in "${patterns[@]}"; do
        local found
        found=$(git ls-files --cached --others --exclude-standard -- "$pattern" 2>/dev/null | head -5)
        if [[ -n "$found" ]]; then
            while IFS= read -r f; do
                warn "敏感文件: $f"
                sensitive=1
            done <<< "$found"
        fi
    done

    if [[ $sensitive -eq 1 ]]; then
        warn "存在敏感文件，推送前请确认已脱敏"
        echo "  .gitignore 中应排除以上文件"
    else
        ok "敏感文件审计通过"
    fi
}

# ── 检查分支状态 ──
check_status() {
    log "📊 Git 状态检查..."
    
    local current_branch
    current_branch=$(git branch --show-current)
    log "  当前分支: $current_branch"

    local ahead behind
    ahead=$(git rev-list --count "${REMOTE}/${BRANCH}..${BRANCH}" 2>/dev/null || echo "?")
    behind=$(git rev-list --count "${BRANCH}..${REMOTE}/${BRANCH}" 2>/dev/null || echo "?")

    if [[ "$ahead" != "?" ]] && [[ "$ahead" -gt 0 ]]; then
        log "  📤 领先远程: ${ahead} commits"
    fi
    if [[ "$behind" != "?" ]] && [[ "$behind" -gt 0 ]]; then
        warn "  📥 落后远程: ${behind} commits (建议先 pull)"
    fi

    local dirty
    dirty=$(git status --porcelain | wc -l | tr -d ' ')
    if [[ "$dirty" -gt 0 ]]; then
        warn "  未提交变更: ${dirty} 个文件"
    else
        ok "  工作区干净"
    fi
}

# ── 执行推送 ──
do_push() {
    local force="${1:-}"
    local tag="${2:-}"

    log "🚀 推送到 Gitee..."
    git fetch "$REMOTE" "$BRANCH" 2>/dev/null || true

    local push_args=()
    [[ "$force" == "true" ]] && push_args+=("--force")

    if git push "${push_args[@]}" "$REMOTE" "$BRANCH:$BRANCH"; then
        ok "推送成功 → $REMOTE/$BRANCH"
    else
        fail "推送失败"
    fi

    # 推送标签
    if [[ -n "$tag" ]]; then
        log "🏷️  创建标签: $tag"
        git tag -a "$tag" -m "龍魂 Gitee 发布 $tag · $(date '+%Y-%m-%d')"
        git push "$REMOTE" "$tag"
        ok "标签 $tag 已推送"
    fi

    # 推送所有标签
    git push "$REMOTE" --tags 2>/dev/null || true
}

# ── 变更摘要 ──
show_diff_summary() {
    log "📝 变更摘要 (vs $REMOTE/$BRANCH):"
    local base
    base=$(git merge-base HEAD "${REMOTE}/${BRANCH}" 2>/dev/null || echo "")
    if [[ -z "$base" ]]; then
        warn "  无法比较（远程无共同祖先）"
        return
    fi

    git diff --stat "$base..HEAD" 2>/dev/null | tail -20 || true
    echo ""
    git log --oneline "$base..HEAD" 2>/dev/null | head -10 || true
}

# ── 主入口 ──
main() {
    echo ""
    echo -e "${CYAN}🐉 龍魂 · Gitee 国内仓库同步${NC}"
    echo -e "${CYAN}══════════════════════════════${NC}"
    echo ""

    local mode="${1:-push}"
    local force_flag=""
    local tag=""

    case "$mode" in
        --dry|dry|--preview|preview)
            check_remote
            check_status
            show_diff_summary
            audit_sensitive
            log "🔍 预览模式 — 未执行推送"
            ;;

        --force|--force-push|force)
            check_remote
            audit_sensitive
            check_status
            do_push "true" "$tag"
            ;;

        --tag)
            tag="${2:-}"
            check_remote
            audit_sensitive
            check_status
            do_push "" "$tag"
            ;;

        push|sync|--sync|"")
            check_remote
            audit_sensitive
            check_status
            do_push "" "$tag"
            ;;

        *)
            echo "用法: bash bin/lh_gitee_push.sh [push|--dry|--force|--tag v1.0]"
            ;;
    esac

    echo ""
    log "DNA: ${CYAN}#龍芯⚡️丙午·乙未·壬午·丙午·䷳艮为山-GITEE-PUSH-v1.0${NC}"
}

main "$@"
