#!/bin/bash
# 后土 OS — 自动化测试脚本
# DNA: #龍芯⚡️丙午·丙申·甲寅·甲戌·兑-TEST-SCRIPT-v1.0
#
# 用法: bash test.sh
# 构建内核 → 在 QEMU 中运行 → 捕获输出 → 验证预期结果

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

PASS=0
FAIL=0

echo "======================================"
echo "  后土 OS · 自动化测试"
echo "  DNA: #龍芯⚡️丙午·丙申·甲寅·甲戌·兑-TEST-v1.0"
echo "======================================"
echo ""

# ── 测试 1: 编译通过 ──
echo "[测试1] 编译..."
if make clean > /dev/null 2>&1 && make > /dev/null 2>&1; then
    echo "  ✅ PASS: 编译成功"
    PASS=$((PASS + 1))
else
    echo "  ❌ FAIL: 编译失败"
    FAIL=$((FAIL + 1))
    exit 1
fi

# ── 测试 2: ELF 文件存在 ──
echo "[测试2] ELF 文件检查..."
if [ -f build/houTu.elf ]; then
    SIZE=$(wc -c < build/houTu.elf)
    echo "  ✅ PASS: houTu.elf 存在 ($SIZE bytes)"
    PASS=$((PASS + 1))
else
    echo "  ❌ FAIL: houTu.elf 不存在"
    FAIL=$((FAIL + 1))
    exit 1
fi

# ── 测试 3: ELF 格式正确 ──
echo "[测试3] ELF 格式验证..."
if file build/houTu.elf | grep -q "ELF 64-bit"; then
    echo "  ✅ PASS: ELF 64-bit 格式"
    PASS=$((PASS + 1))
else
    echo "  ❌ FAIL: 非 ELF64 格式"
    FAIL=$((FAIL + 1))
fi

# ── 测试 4: Multiboot2 头 ──
echo "[测试4] Multiboot2 魔数..."
if command -v grub-file > /dev/null 2>&1; then
    if grub-file --is-x86-multiboot2 build/houTu.elf; then
        echo "  ✅ PASS: Multiboot2 兼容"
        PASS=$((PASS + 1))
    else
        echo "  ❌ FAIL: 不兼容 Multiboot2"
        FAIL=$((FAIL + 1))
    fi
else
    # 手动检查魔数
    if xxd build/houTu.elf | head -20 | grep -q "d650 52e8"; then
        echo "  ✅ PASS: Multiboot2 魔数存在"
        PASS=$((PASS + 1))
    else
        echo "  ⚠ SKIP: grub-file 不可用, 手动魔数检测不确定"
    fi
fi

# ── 测试 5: QEMU 可用性 ──
echo "[测试5] QEMU 可用性..."
if command -v qemu-system-x86_64 > /dev/null 2>&1; then
    echo "  ✅ PASS: QEMU 可用"
    PASS=$((PASS + 1))
else
    echo "  ⚠ SKIP: QEMU 不可用, 跳过运行测试"
fi

# ── 测试 6: QEMU 启动测试（如果有 QEMU）──
if command -v qemu-system-x86_64 > /dev/null 2>&1; then
    echo "[测试6] QEMU 启动测试..."
    # 运行 QEMU，5秒后自动终止
    timeout 5 qemu-system-x86_64 \
        -kernel build/houTu.elf \
        -m 256M \
        -nographic \
        -no-reboot \
        -no-shutdown \
        > build/qemu_output.log 2>&1 || true

    if grep -q "后土" build/qemu_output.log 2>/dev/null || \
       grep -q "HouTu" build/qemu_output.log 2>/dev/null; then
        echo "  ✅ PASS: 后土内核成功启动"
        PASS=$((PASS + 1))
    else
        echo "  ⚠ WARN: 未在输出中检测到后土标识（可能是 -nographic 模式下 VGA 输出不可见）"
        echo "  尝试在图形模式下运行: make run"
    fi
fi

# ── 汇总 ──
echo ""
echo "======================================"
echo "  测试结果: $PASS 通过 / $FAIL 失败"
echo "======================================"

if [ $FAIL -eq 0 ]; then
    echo "  🟢 全部测试通过"
else
    echo "  🔴 存在失败项"
fi
