#!/bin/bash
# DNA追溯码:#龍芯⚡️2026-07-25-LONGHUN-FONT-INSTALL-MACOS-v2.0
#
# 龙魂字体 macOS 安装器
# 将 龙魂字体-Regular.otf 安装到用户字体目录

set -e

FONT_SOURCE="output/龙魂字体-Regular.otf"
FONT_TARGET="${HOME}/Library/Fonts/龙魂字体-Regular.otf"

# 1. OS check
if [[ "$(uname -s)" != "Darwin" ]]; then
    echo "Error: 此安装器仅适用于 macOS。" >&2
    exit 1
fi

# 2. Font file check
if [[ ! -f "${FONT_SOURCE}" ]]; then
    echo "Error: 字体文件不存在: ${FONT_SOURCE}" >&2
    echo "请先运行优化脚本: python3 scripts/rename_and_optimize.py" >&2
    exit 1
fi

# 3. Install font
cp "${FONT_SOURCE}" "${FONT_TARGET}"
echo "已安装 龙魂字体-Regular.otf 到 ${FONT_TARGET}"

# 4. Clear font cache (optional; may require a reboot/logout to take full effect)
echo "清除字体缓存（可选步骤）..."
atsutil databases -remove 2>/dev/null || echo "注意: atsutil 缓存清除被跳过（非致命）。"

# 5. Success + DNA
echo ""
echo "✅ 龙魂字体安装成功。"
echo "DNA追溯码:#龍芯⚡️2026-07-25-LONGHUN-FONT-INSTALL-MACOS-v2.0"
