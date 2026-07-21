# ============================================================
# 🐉 龍魂计算内核 · Makefile
# DNA: #龍芯⚡️2026-07-13-COMPUTE-KERNELS-v1.1
#
# 支持架构:
#   x86_64 (Linux/macOS) → SIMD 汇编编译
#   ARM64 (Apple Silicon) → 纯 Python 回退 (无需 make)
# ============================================================

UNAME_S := $(shell uname -s)
UNAME_M := $(shell uname -m)

# 架构兼容检测
ifeq ($(UNAME_M),arm64)
    $(info 🍎 Apple Silicon (ARM64) 检测到 — SIMD内核仅限x86-64)
    $(info    纯 Python 回退自动启用，无需编译。)
    $(info    如需在x86-64机器编译: 将此目录复制到x86-64服务器执行 make)
    SKIP = 1
endif

ifeq ($(SKIP),1)
all:
	@echo "✅ 跳过编译 (ARM64) — 纯Python回退已就绪"
	@echo "   测试: python3 test_kernels.py"

clean:
	@rm -f kernels.o *.dylib *.so

.PHONY: all clean test
else

ifeq ($(UNAME_S),Darwin)
    # macOS x86_64
    AS = clang
    ASFLAGS = -c -x assembler-with-cpp -target x86_64-apple-macos
    LD = clang
    LDFLAGS = -shared -o liblh_kernels.dylib -lm
    TARGET = liblh_kernels.dylib
else
    # Linux x86_64
    AS = as
    ASFLAGS = --64
    LD = ld
    LDFLAGS = -shared -o liblh_kernels.so -lm
    TARGET = liblh_kernels.so
endif

all: $(TARGET)

kernels.o: kernels.s
	$(AS) $(ASFLAGS) -o kernels.o kernels.s

$(TARGET): kernels.o
	$(LD) $(LDFLAGS) kernels.o
	@echo "✅ 龍魂 SIMD 计算内核编译完成: $(TARGET)"
	@echo "   运行测试: python3 test_kernels.py"

clean:
	rm -f kernels.o $(TARGET)

test: $(TARGET)
	python3 test_kernels.py

endif

.PHONY: all clean test
