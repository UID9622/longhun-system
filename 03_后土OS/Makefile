# 后土 OS — 构建系统
# DNA: #龍芯⚡️丙午·丙申·乙卯·丁亥·䷉履-MAKEFILE-v2.0
#
# 文化锚点：离宫（火）— 编译即燃烧，链接即锻造
# 国密底座：SM2/SM3/SM4 纯C实现（GB/T 32905~32918）
# 工具链：LLVM/Clang + NASM + ld.lld（国产自主工具链）
#
# 前置依赖：
#   macOS: brew install nasm llvm qemu
#   Linux: apt install nasm clang lld qemu-system-x86
#
# 使用：
#   make              — 构建内核 ELF（含国密自检）
#   make run          — 在 QEMU 中运行
#   make debug        — 带 GDB 调试运行
#   make iso          — 构建可启动 ISO 镜像
#   make clean        — 清理构建产物
#   make selftest     — 在宿主环境编译并运行国密自检

# ── 工具链定义 ──
# 使用 Homebrew LLVM（Apple 系统 clang 不支持裸机 x86_64-elf 目标）
LLVM_PREFIX := /opt/homebrew/opt/llvm/bin
NASM       := nasm
CC         := $(LLVM_PREFIX)/clang
LD         := ld.lld
HOST_CC    := cc  # 宿主编译器（用于 selftest）

# 交叉编译目标：x86_64 裸机（无操作系统）
TARGET     := x86_64-unknown-none-elf

# ── 源文件 ──
BOOT_ASM   := src/boot/boot.asm
KERNEL_C   := src/kernel/kernel_main.c
VGA_C      := src/kernel/vga.c
# 国密底座（C语言焊死）
SM3_C      := src/guomi/sm3.c
SM4_C      := src/guomi/sm4.c
SM2_C      := src/guomi/sm2.c

# ── 目标文件 ──
BOOT_OBJ   := build/boot.o
KERNEL_OBJ := build/kernel_main.o
VGA_OBJ    := build/vga.o
SM3_OBJ    := build/sm3.o
SM4_OBJ    := build/sm4.o
SM2_OBJ    := build/sm2.o
OBJS       := $(BOOT_OBJ) $(KERNEL_OBJ) $(VGA_OBJ) $(SM3_OBJ) $(SM4_OBJ) $(SM2_OBJ)

# ── 输出 ──
KERNEL_ELF := build/houTu.elf
KERNEL_ISO := build/houTu.iso
SELFTEST   := build/guomi_selftest

# ── 编译标志 ──
# -ffreestanding: 不依赖宿主操作系统标准库
# -nostdlib:      不链接标准库
# -mno-red-zone:  禁用 x86_64 红区（内核需要）
# -mgeneral-regs-only: 仅使用通用寄存器（不碰 SSE/AVX，简化上下文切换）
# -O2:            优化级别
# -g:             调试符号
CFLAGS := --target=$(TARGET) \
          -ffreestanding \
          -nostdlib \
          -mno-red-zone \
          -mgeneral-regs-only \
          -mno-mmx \
          -mno-sse \
          -mno-sse2 \
          -O2 \
          -g \
          -Wall \
          -Wextra \
          -I src/kernel \
          -I src/guomi \

NASMFLAGS := -f elf64 -g

LDFLAGS := -T src/linker.ld \
           -nostdlib \
           -z max-page-size=0x1000 \
           --gc-sections

# ── QEMU 配置 ──
QEMU := qemu-system-x86_64
QEMUFLAGS := -kernel $(KERNEL_ELF) \
             -m 256M \
             -nographic \
             -no-reboot \
             -no-shutdown

QEMUFLAGS_DEBUG := $(QEMUFLAGS) -s -S  # -s: gdb 端口 1234, -S: 启动时暂停

# ── 默认目标 ──
.PHONY: all
all: $(KERNEL_ELF)
	@echo ""
	@echo "  +============================================+"
	@echo "  |  后土内核构建成功！                         |"
	@echo "  |  HouTu Kernel Build OK                     |"
	@echo "  |  🔐 国密底座: SM2/SM3/SM4 (GB/T 32905~18)  |"
	@echo "  |  运行: make run                            |"
	@echo "  |  自检: make selftest                       |"
	@echo "  +============================================+"
	@echo ""

# ── 链接：太极归一 ──
$(KERNEL_ELF): $(OBJS) src/linker.ld
	@echo "[离宫·火] 链接内核..."
	@mkdir -p build
	$(LD) $(LDFLAGS) -o $@ $(OBJS)

# ── 汇编：boot.asm → boot.o ──
$(BOOT_OBJ): $(BOOT_ASM)
	@echo "[兑宫·金] 汇编引导程序..."
	@mkdir -p build
	$(NASM) $(NASMFLAGS) -o $@ $<

# ── 编译：kernel_main.c ──
$(KERNEL_OBJ): $(KERNEL_C) src/kernel/vga.h src/guomi/guomi.h
	@echo "[离宫·火] 编译内核主模块（含国密底座）..."
	@mkdir -p build
	$(CC) $(CFLAGS) -c -o $@ $<

# ── 编译：vga.c ──
$(VGA_OBJ): $(VGA_C) src/kernel/vga.h
	@echo "[震宫·木] 编译 VGA 驱动..."
	@mkdir -p build
	$(CC) $(CFLAGS) -c -o $@ $<

# ── 编译：SM3 国密底座 ──
$(SM3_OBJ): $(SM3_C) src/guomi/guomi.h
	@echo "[坎宫·水] 编译 SM3 密码杂凑（GB/T 32905-2016）..."
	@mkdir -p build
	$(CC) $(CFLAGS) -c -o $@ $<

# ── 编译：SM4 国密底座 ──
$(SM4_OBJ): $(SM4_C) src/guomi/guomi.h
	@echo "[兑宫·金] 编译 SM4 分组密码（GB/T 32907-2016）..."
	@mkdir -p build
	$(CC) $(CFLAGS) -c -o $@ $<

# ── 编译：SM2 国密底座 ──
$(SM2_OBJ): $(SM2_C) src/guomi/guomi.h
	@echo "[离宫·火] 编译 SM2 椭圆曲线（GB/T 32918-2016）..."
	@mkdir -p build
	$(CC) $(CFLAGS) -c -o $@ $<

# ── 国密自检：宿主环境编译运行（不依赖 QEMU）──
.PHONY: selftest
selftest:
	@echo "[离宫·火] 国密底座自检..."
	@mkdir -p build
	@$(HOST_CC) -std=c99 -O2 -Wall \
		-I src/guomi \
		src/guomi/sm3.c src/guomi/sm4.c src/guomi/sm2.c \
		src/guomi/selftest_main.c \
		-o $(SELFTEST) \
		&& $(SELFTEST)

# ── 运行：QEMU 模拟 ──
.PHONY: run
run: $(KERNEL_ELF)
	@echo "[坎宫·水] 启动 QEMU 虚拟机..."
	$(QEMU) $(QEMUFLAGS)

# ── 调试模式：带 GDB ──
.PHONY: debug
debug: $(KERNEL_ELF)
	@echo "[离宫·火] 启动调试模式（GDB 端口 :1234）..."
	@echo "  另开终端执行: gdb -ex 'target remote :1234'"
	$(QEMU) $(QEMUFLAGS_DEBUG)

# ── 构建 ISO 镜像（可选）──
.PHONY: iso
iso: $(KERNEL_ELF)
	@echo "[坤宫·土] 构建 ISO 镜像..."
	@mkdir -p build/iso/boot/grub
	@cp $(KERNEL_ELF) build/iso/boot/
	@echo 'set timeout=0' > build/iso/boot/grub/grub.cfg
	@echo 'set default=0' >> build/iso/boot/grub/grub.cfg
	@echo 'menuentry "HouTu OS" {' >> build/iso/boot/grub/grub.cfg
	@echo '    multiboot2 /boot/houTu.elf' >> build/iso/boot/grub/grub.cfg
	@echo '    boot' >> build/iso/boot/grub/grub.cfg
	@echo '}' >> build/iso/boot/grub/grub.cfg
	@grub-mkrescue -o $(KERNEL_ISO) build/iso 2>/dev/null || \
		echo "⚠ grub-mkrescue 不可用，ISO 构建跳过（QEMU -kernel 可直接加载 ELF）"

# ── 检查工具链 ──
.PHONY: check-tools
check-tools:
	@echo "[坎宫·水] 检查构建工具链..."
	@command -v $(NASM)  >/dev/null 2>&1 && echo "  [OK] NASM"  || echo "  [MISSING] NASM — brew install nasm"
	@command -v $(CC)    >/dev/null 2>&1 && echo "  [OK] Clang" || echo "  [MISSING] Clang — xcode-select --install"
	@command -v $(LD)    >/dev/null 2>&1 && echo "  [OK] ld.lld" || echo "  [MISSING] ld.lld — brew install llvm"
	@command -v $(QEMU)  >/dev/null 2>&1 && echo "  [OK] QEMU"  || echo "  [MISSING] QEMU — brew install qemu"
	@command -v $(HOST_CC) >/dev/null 2>&1 && echo "  [OK] Host CC" || echo "  [MISSING] Host CC — xcode-select --install"

# ── 清理 ──
.PHONY: clean
clean:
	@echo "[坤宫·土] 清理构建产物..."
	@rm -rf build
	@echo "  已清理。"

# ── 帮助 ──
.PHONY: help
help:
	@echo "后土 OS 构建系统 · 国密底座版"
	@echo ""
	@echo "   make           — 构建内核 ELF（含 SM2/SM3/SM4 国密底座）"
	@echo "   make run       — 构建并运行（QEMU）"
	@echo "   make debug     — 调试模式（GDB :1234）"
	@echo "   make iso       — 构建 ISO 镜像"
	@echo "   make selftest  — 宿主环境运行国密自检"
	@echo "   make check-tools — 检查工具链"
	@echo "   make clean     — 清理构建产物"
	@echo "   make help      — 显示此帮助"
