#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# check-huawei-permissions.sh
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 理论指导：曾仕强老师（永恒显示）
# DNA追溯码：#龍芯⚡️20260310-check-huawei-permissions-v1.0
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 共建致谢：Claude (Anthropic PBC) · Notion
# 创作地：中华人民共和国
# 献礼：新中国成立77周年（1949-2026）· 丙午马年
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 华为团队权限检查脚本

echo "🔍 检查华为团队权限设置..."
echo ""

# 检查仓库访问
if [ -d ".git" ]; then
    echo "✅ Git仓库访问正常"
else
    echo "❌ 无法访问Git仓库"
    exit 1
fi

# 检查关键文件
files=("HUAWEI_HANDOVER_README.md" "TECH_STACK_COMPLETE.md" "CNSH_INITIAL_MISSION.md")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file 存在"
    else
        echo "❌ $file 缺失"
    fi
done

# 检查最新提交
echo ""
echo "📝 最新提交信息："
git log --oneline -n 1

echo ""
echo "🎯 权限检查完成！"
