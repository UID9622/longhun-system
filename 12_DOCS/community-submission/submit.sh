#!/bin/bash
# 龍魂·社区提交脚本
# DNA: #龍芯⚡️2026-09-02-COMMUNITY-SUBMIT-v1.0-UID9622
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 用法: ./docs/community-submission/submit.sh

set -e

REPO="deepseek-ai/DeepSeek-V3"
TITLE="[Cross-Framework] Longhun Audit Dataset v2.0 — Mobile Extension"
BODY_FILE="docs/community-submission/ISSUE_BODY.md"

echo "🐉 龍魂·社区提交工具"
echo "======================"
echo "目标仓库: $REPO"
echo "标题: $TITLE"
echo ""

# 检查 gh CLI
if ! command -v gh &> /dev/null; then
    echo "❌ gh CLI 未安装，请先安装："
    echo "  brew install gh  # macOS"
    echo "  sudo apt install gh  # Linux"
    exit 1
fi

# 检查登录状态
if ! gh auth status &> /dev/null; then
    echo "⚠️  gh 未登录，请先执行："
    echo "  gh auth login"
    exit 1
fi

# 检查 body 文件
if [ ! -f "$BODY_FILE" ]; then
    echo "❌ 找不到 $BODY_FILE"
    exit 1
fi

# 确认提交
echo "即将提交 Issue："
echo "  标题: $TITLE"
echo "  内容预览（前5行）："
head -5 "$BODY_FILE"
echo ""
read -p "确认提交？(y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "已取消"
    exit 0
fi

# 提交 Issue（实测 #1622：第三方仓库无 dataset/audit 自定义 label，加 --label 会报 "could not add label" 终止，故不加）
echo "📡 提交中..."
gh issue create --repo "$REPO" --title "$TITLE" --body-file "$BODY_FILE"

echo "✅ 提交完成！"
echo "Issue 链接："
gh issue list --repo "$REPO" --state open --limit 1
