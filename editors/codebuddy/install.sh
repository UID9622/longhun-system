#!/bin/bash
# 龍魂 CodeBuddy 插件一键安装脚本
# DNA: #龍芯⚡️丙午·辛未·CODEBUDDY-PLUGINS-INSTALL-v1.0
# 用途: 编译并符号链接全部 6 个 MVP 插件到 CodeBuddy 扩展目录

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGINS_DIR="$SCRIPT_DIR"
# CodeBuddy CN 实际读取的扩展目录（非 ~/.codebuddy/extensions）
CODEBUDDY_EXT="$HOME/.codebuddycn/extensions"

echo "🐉 龍魂 CodeBuddy 插件安装"
echo "============================"
echo ""

# 确保 CodeBuddy 扩展目录存在
mkdir -p "$CODEBUDDY_EXT"

# 清理旧错误安装位置（~/.codebuddy/extensions 为误设路径）
OLD_EXT="$HOME/.codebuddy/extensions"
if [ -d "$OLD_EXT" ]; then
    echo "🧹 清理旧安装路径: $OLD_EXT"
    rm -rf "$OLD_EXT"
fi

PLUGINS=(
    "longhun-console"
    "cnsh-syntax"
    "audit-tracker"
    "model-router"
    "protocol-checker"
    "one-click-deploy"
)

# 扩展目录命名映射（publisher.name-version 格式）
declare -A EXT_NAMES=(
    ["longhun-console"]="uid9622.longhun-console-1.0.0"
    ["cnsh-syntax"]="uid9622.cnsh-syntax-2.0.0"
    ["audit-tracker"]="uid9622.longhun-audit-tracker-1.0.0"
    ["model-router"]="uid9622.longhun-model-router-1.0.0"
    ["protocol-checker"]="uid9622.longhun-protocol-checker-1.0.0"
    ["one-click-deploy"]="uid9622.longhun-one-click-deploy-1.0.0"
)

INSTALLED=0
FAILED=0

for plugin in "${PLUGINS[@]}"; do
    PLUGIN_DIR="$PLUGINS_DIR/$plugin"
    EXT_NAME="${EXT_NAMES[$plugin]}"
    echo "📦 安装: $plugin → $EXT_NAME"

    if [ ! -d "$PLUGIN_DIR" ]; then
        echo "   ⚠️  目录不存在，跳过"
        FAILED=$((FAILED + 1))
        continue
    fi

    cd "$PLUGIN_DIR"

    # 安装依赖
    if [ -f "package.json" ]; then
        npm install --silent 2>/dev/null || true
    fi

    # 编译
    if [ -f "tsconfig.json" ]; then
        npx tsc -p ./ 2>/dev/null || {
            echo "   ⚠️  编译失败，跳过"
            FAILED=$((FAILED + 1))
            continue
        }
    fi

    # 符号链接到 CodeBuddy 扩展目录（publisher.name-version 格式）
    TARGET="$CODEBUDDY_EXT/$EXT_NAME"
    if [ -L "$TARGET" ] || [ -d "$TARGET" ] || [ -f "$TARGET" ]; then
        rm -rf "$TARGET"
    fi
    ln -sf "$PLUGIN_DIR" "$TARGET"

    echo "   ✅ 已安装 → $TARGET"
    INSTALLED=$((INSTALLED + 1))
done

echo ""
echo "============================"
echo "✅ 成功: $INSTALLED  |  ❌ 失败: $FAILED"
echo ""
echo "安装目录: $CODEBUDDY_EXT"
echo ""
echo "⚠️  注意：必须重新加载窗口才能生效！"
echo "    按 Cmd+Shift+P → 输入: 重新加载窗口 (Reload Window)"
echo ""
echo "重启后："
echo "  • 侧边栏查看「龍魂控制台」"
echo "  • Cmd+Shift+P → 搜索「龍魂」查看所有命令"
echo ""
echo "DNA: #龍芯⚡️丙午·辛未·CODEBUDDY-PLUGINS-INSTALL-v1.0"
