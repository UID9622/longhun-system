#!/bin/bash
# ═══════════════════════════════════════════════════════════
# 龍魂·Git历史密钥清理脚本 v2.0
# DNA: #龍芯⚡️丙午·乙未·癸未·亥时-CLEAN-TOKEN-v2.0
# ═══════════════════════════════════════════════════════════
# 用途: 从 git 历史中清除泄露的 Telegram Bot Token
# 用法: bash bin/lh_clean_token.sh
# ⚠️  此操作会重写全部提交历史，所有commit hash会变
# ⚠️  执行后必须 force push 到所有远端
# ═══════════════════════════════════════════════════════════

set -e

cd "$(dirname "$0")/.."
echo "🐉 龍魂·Git历史密钥清理 v2.0"
echo "=============================="
echo ""

# 0. 检查磁盘空间（至少需要 500MB）
FREE_MB=$(df -m /System/Volumes/Data 2>/dev/null | tail -1 | awk '{print $4}')
if [ "$FREE_MB" -lt 500 ]; then
    echo "❌ 磁盘空间不足！当前可用: ${FREE_MB}MB，需要至少 500MB"
    echo ""
    echo "请先清理空间："
    echo "  # 清理 pip 缓存"
    echo "  rm -rf ~/Library/Caches/pip"
    echo "  # 清理 npm 缓存"
    echo "  rm -rf ~/.npm/_cacache"
    echo "  # 清理 Xcode 缓存"
    echo "  rm -rf ~/Library/Developer/Xcode/DerivedData"
    echo "  # 清理 ~/.cache"
    echo "  rm -rf ~/.cache/*"
    echo ""
    exit 1
fi

# 1. 确认当前分支
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "当前分支: $BRANCH"
echo ""

# 2. 检查工作区 —— 只允许 memory/ 和少量已知文件的改动
DIRTY=$(git status --porcelain)
if [ -n "$DIRTY" ]; then
    # 只允许特定文件的未提交改动
    ALLOWED_PATTERNS=".codebuddy/memory/ docs/ bin/lh_clean_token.sh cnsh/core/ai_tools/longhu_sentinel_bot/README.md"
    DISALLOWED=$(echo "$DIRTY" | grep -vE "$(echo "$ALLOWED_PATTERNS" | sed 's/ /|/g')" || true)
    if [ -n "$DISALLOWED" ]; then
        echo "❌ 检测到不允许的未提交改动（stash 或先提交它们）："
        echo "$DISALLOWED" | head -20
        echo ""
        echo "共 $(echo "$DISALLOWED" | wc -l | tr -d ' ') 个文件。请先处理："
        echo "  git stash push -m 'pre-token-clean' -- 被改动的文件..."
        echo "或"
        echo "  git add <文件> && git commit -m 'pre-clean snapshot'"
        exit 1
    fi
    echo "⚠️  检测到允许的未提交改动，先提交..."
    git add .codebuddy/memory/ docs/ bin/lh_clean_token.sh cnsh/core/ai_tools/longhu_sentinel_bot/README.md 2>/dev/null || true
    git commit -m "pre-clean: token scrub snapshot" || true
    echo ""
fi

# 3. 确认要清理的token
TOKEN_PATTERN="8643060944:AAFa-bQT1GyP4Ry32iYJc7Cnrkg0hMPA1l4"
REPLACEMENT="REDACTED_USE_ENV_VAR_TELEGRAM_BOT_TOKEN"

echo "🔍 搜索历史中的 token..."
HIT_COUNT=$(git log --all --oneline -S "$TOKEN_PATTERN" 2>/dev/null | wc -l | tr -d ' ')
echo "   发现 $HIT_COUNT 个commit包含此token"
echo ""

if [ "$HIT_COUNT" -eq 0 ]; then
    echo "✅ 历史中已无此token，无需清理"
    exit 0
fi

# 4. 清理 —— 使用 index-filter（比 tree-filter 快10倍，不碰工作区）
echo "🧹 开始清理git历史 (index-filter 模式)..."
export FILTER_BRANCH_SQUELCH_WARNING=1

# 先备份原始refs
BEFORE=$(git rev-parse HEAD)

git filter-branch --force --index-filter '
    # 对指定目录下的文件做token替换
    for f in cnsh/core/ai_tools/longhu_sentinel_bot/sentinel_bot.py \
             cnsh/core/ai_tools/longhu_sentinel_bot/telegram_handler.py \
             cnsh/core/ai_tools/longhu_sentinel_bot/token_manager.py; do
        old_hash=$(git ls-files -s "$f" 2>/dev/null | awk "{print \$2}")
        if [ -n "$old_hash" ]; then
            new_hash=$(git cat-file -p "$old_hash" | sed "s|8643060944:AAFa-bQT1GyP4Ry32iYJc7Cnrkg0hMPA1l4|REDACTED_USE_ENV_VAR_TELEGRAM_BOT_TOKEN|g" | git hash-object -w --stdin)
            mode=$(git ls-files -s "$f" 2>/dev/null | awk "{print \$1}")
            git update-index --cacheinfo "$mode" "$new_hash" "$f"
        fi
    done
' -- "$BRANCH"

echo ""
echo "✅ 历史已清理"
echo ""

# 5. 清理备份refs（节省空间）
echo "🧹 清理 filter-branch 备份..."
git for-each-ref --format="%(refname)" refs/original/ | xargs -r git update-ref -d 2>/dev/null || true
git reflog expire --expire=now --all 2>/dev/null || true
git gc --prune=now 2>/dev/null || true
echo ""

# 6. 验证
REMAINING=$(git log --all --oneline -S "$TOKEN_PATTERN" 2>/dev/null | wc -l | tr -d ' ')
echo "🔍 验证: 残留 $REMAINING 个commit"
echo ""

if [ "$REMAINING" -gt 0 ]; then
    echo "⚠️  仍有残留，请手动检查"
    git log --all --oneline -S "$TOKEN_PATTERN"
else
    echo "✅ 历史中已完全清除token"
fi

echo ""
echo "═════════════════════════════════════════════════════════"
echo "⚠️  下一步操作："
echo "═════════════════════════════════════════════════════════"
echo ""
echo "1. ⚠️  立即去 Telegram @BotFather 撤销此token:"
echo "   /revoke    (选择 LongHun_Sentinel_Bot)"
echo "   生成新token后用环境变量设置:"
echo "   export TELEGRAM_BOT_TOKEN='你的新token'"
echo ""
echo "2. 强制推送到所有远端:"
echo "   git push origin $BRANCH --force"
echo "   git push gitee $BRANCH --force"
echo "   git push gitcode $BRANCH --force"
echo ""
echo "3. 通知所有协作者重新clone仓库"
echo ""
echo "═════════════════════════════════════════════════════════"
