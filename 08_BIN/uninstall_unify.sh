#!/bin/bash
# 🐉 龍魂 · 卸载脚本（冻结式 · P0天条：不删除只冻结）
# DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-UNINSTALL-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 用法: bash bin/uninstall_unify.sh
# ⚠️ 本脚本不物理删除 ~/.longhun，而是改名冻结留档，可 --restore 恢复

echo "⚠️ 警告: 此操作将冻结所有龍魂互通配置（改名留档，不删除）"
echo "========================================"
read -p "确认卸载? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "❌ 已取消"
    exit 0
fi

# 冻结龍魂环境（改名 .frozen，不删除）
if [ -d ~/.longhun ]; then
    FROZEN=~/.longhun.frozen
    if [ -d "$FROZEN" ]; then
        FROZEN=~/.longhun.frozen_$(date +%Y%m%d_%H%M%S)
    fi
    mv ~/.longhun "$FROZEN"
    echo "🧊 已冻结 ~/.longhun → $FROZEN（恢复: lh unify --restore）"
else
    echo "⏭️ ~/.longhun 不存在，无需冻结"
fi

# 从Shell配置中移除
for FILE in ~/.zshrc ~/.bashrc ~/.bash_profile; do
    if [ -f "$FILE" ]; then
        sed -i '' '/source ~\/.longhun\/env.sh/d' "$FILE" 2>/dev/null || true
        echo "   ✅ 已从 $FILE 移除"
    fi
done

echo "✅ 卸载（冻结）完成"
echo "🐉丙午·亥时·䷖剥·🟢"
