#!/bin/bash
# 后土 OS — 工具链一键安装脚本
# DNA: #龍芯⚡️丙午·丙申·甲寅·甲戌·坎-SETUP-TOOLCHAIN-v1.0
#
# 用法: bash setup.sh
# 自动安装 NASM + LLVM(ld.lld) + QEMU

set -e

echo "======================================"
echo "  后土 OS · 工具链安装"
echo "======================================"
echo ""

# 检查 Homebrew
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew 未安装，请先安装："
    echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

install_if_missing() {
    local pkg="$1"
    local desc="$2"
    if brew list "$pkg" &>/dev/null; then
        echo "  ✅ $desc 已安装"
    else
        echo "  📦 安装 $desc..."
        HOMEBREW_NO_AUTO_UPDATE=1 brew install "$pkg" && echo "  ✅ $desc 安装完成"
    fi
}

echo "[坎宫·水] 安装构建工具..."
echo ""

install_if_missing "nasm" "NASM (x86 汇编器)"
install_if_missing "llvm"  "LLVM (含 ld.lld 链接器)"
install_if_missing "qemu"  "QEMU (x86 虚拟机)"

echo ""
echo "======================================"
echo "  安装完成！验证工具链："
echo "======================================"
echo ""

nasm -v 2>/dev/null && echo "  ✅ NASM $(nasm -v 2>&1 | head -1)"
clang --version 2>/dev/null | head -1 && echo "  ✅ Clang"
ld.lld --version 2>/dev/null && echo "  ✅ ld.lld"
qemu-system-x86_64 --version 2>/dev/null | head -1 && echo "  ✅ QEMU"

echo ""
echo "工具链就绪。运行以下命令构建并启动后土内核："
echo ""
echo "  cd 03_后土OS"
echo "  make        # 构建"
echo "  make run    # 在 QEMU 中运行"
echo ""
echo "======================================"
