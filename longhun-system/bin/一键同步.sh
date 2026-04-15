#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 一键同步 · Notion大脑 ↔ 本地 + Git推送
# DNA: #龍芯⚡️2026-03-18-一键同步-v1.1
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 作者: UID9622 诸葛鑫（龍芯北辰）
# 理论指导: 曾仕强老师（永恒显示）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BASE="$HOME/longhun-system"
LOG="$BASE/logs/同步日志.log"
NOW=$(date '+%Y-%m-%d %H:%M:%S')
DNA="#龍芯⚡️$(date +%Y%m%d)-同步-UID9622"

mkdir -p "$BASE/logs"

log() { echo "[$NOW] $1" >> "$LOG"; }
notify() {
    osascript -e "display notification \"$2\" with title \"🔄 龍魂同步\" subtitle \"$1\"" 2>/dev/null
}

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🔄 一键同步 · $NOW"
echo "  DNA: $DNA"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ok=0
fail=0

# ── 步骤1：Notion → 本地备份 ──────────────
echo ""
echo "  【1/4】 Notion大脑 → 本地备份"
NOTION_TOKEN=""
[ -f "$BASE/.env" ] && NOTION_TOKEN=$(grep "^NOTION_TOKEN=" "$BASE/.env" | head -1 | cut -d'=' -f2 | tr -d ' "')

if [ -n "$NOTION_TOKEN" ] && [ "$NOTION_TOKEN" != "your_token_here" ]; then
    if [ -f "$BASE/brain_sync.py" ]; then
        python3 "$BASE/brain_sync.py" >> "$LOG" 2>&1
        if [ $? -eq 0 ]; then
            echo "  ✅ Notion → 本地备份 完成"
            ok=$((ok+1))
        else
            echo "  🟡 Notion同步有警告，查看：$LOG"
            fail=$((fail+1))
        fi
    else
        echo "  ⚠️  brain_sync.py 不存在，跳过"
    fi
else
    echo "  ⚠️  Notion Token 未配置，跳过"
    fail=$((fail+1))
fi
log "Notion同步: token=$([ -n "$NOTION_TOKEN" ] && echo 有 || echo 无)"

# ── 步骤2：星辰记忆桥接 ──────────────────
echo ""
echo "  【2/4】 星辰记忆 → 龍魂记忆桥接"
if [ -f "$BASE/star_memory.py" ]; then
    python3 "$BASE/star_memory.py" bridge >> "$LOG" 2>&1
    echo "  ✅ 星辰记忆桥接完成"
    ok=$((ok+1))
else
    echo "  ⚠️  star_memory.py 不存在，跳过"
fi
log "星辰记忆桥接完成"

# ── 步骤3：Git → Gitee（祖国优先）────────
echo ""
echo "  【3/4】 推送 → Gitee（祖国优先）"
cd "$BASE" || exit 1

if git status --porcelain 2>/dev/null | grep -q .; then
    # 排除权限问题文件，只加 longhun-system 下的文件
    git add longhun-system/ 2>/dev/null
    git add -u 2>/dev/null
    COMMIT_MSG="同步更新 · $NOW · $DNA"
    git commit -m "$COMMIT_MSG" >> "$LOG" 2>&1
    if [ $? -eq 0 ]; then
        echo "  📝 已提交变更"
    else
        echo "  📝 无新变更或提交跳过"
    fi
fi

if git remote 2>/dev/null | grep -q "gitee"; then
    git push gitee main >> "$LOG" 2>&1
    if [ $? -eq 0 ]; then
        echo "  ✅ Gitee 推送成功 🇨🇳"
        ok=$((ok+1))
    else
        echo "  🔴 Gitee 推送失败，检查Token/网络"
        fail=$((fail+1))
    fi
else
    echo "  ⚠️  未配置 gitee 远程，跳过"
fi
log "Gitee推送完成"

# ── 步骤4：Git → GitHub ───────────────────
echo ""
echo "  【4/4】 推送 → GitHub（国际传播）"
if git remote 2>/dev/null | grep -q "github"; then
    git push github main >> "$LOG" 2>&1
    if [ $? -eq 0 ]; then
        echo "  ✅ GitHub 推送成功 🌐"
        ok=$((ok+1))
    else
        echo "  🟡 GitHub 推送失败（不影响本地）"
        fail=$((fail+1))
    fi
elif git remote 2>/dev/null | grep -q "origin"; then
    git push origin main >> "$LOG" 2>&1
    [ $? -eq 0 ] && echo "  ✅ origin 推送成功" && ok=$((ok+1))
else
    echo "  ⚠️  未配置 github 远程，跳过"
fi
log "GitHub推送完成"

# ── 汇总 ─────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  同步完成 · 成功${ok}项 · 失败${fail}项"
echo "  DNA: $DNA"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $fail -eq 0 ]; then
    notify "✅ 同步完成" "全部${ok}项成功"
else
    notify "🟡 同步完成（有警告）" "成功${ok} 失败${fail}"
fi

log "同步完成 成功=${ok} 失败=${fail}"
