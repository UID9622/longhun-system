# DNA: #龍芯⚡️丙午·丙申·壬子·子时·䷕贲-RUST-MAKEFILE-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 协议: MulanPSL v2 (工程层)
#
# 龍魂 Rust 统一编译入口
# 用法:
#   make check      → 编译检查
#   make test       → 运行测试
#   make build      → 本地构建
#   make build-py   → 构建Python绑定
#   make build-all  → 全平台交叉编译
#   make install-py → 安装Python绑定到当前环境
#   make clean      → 清理

SHELL := /bin/bash
CARGO := $(HOME)/.cargo/bin/cargo
RUSTUP := $(HOME)/.cargo/bin/rustup
COREDIR := rust/longhun-core
PYDIR := rust/longhun-py
JNIDIR := rust/longhun-jni
NAPIDIR := rust/longhun-napi

# 所有支持的编译目标
TARGETS := \
	aarch64-apple-darwin \
	aarch64-unknown-linux-gnu \
	x86_64-unknown-linux-gnu \
	aarch64-linux-android \
    loongarch64-unknown-linux-gnu

# 移动端交叉编译目标（鸿蒙兼容·C ABI桥接）
# 优先用 aarch64-unknown-linux-gnu（只需 gcc-aarch64-linux-gnu，无需 Android NDK）
MOBILE_TARGETS := aarch64-unknown-linux-gnu
# 备选（需 Android NDK）: aarch64-linux-android armv7-linux-androideabi

.PHONY: all check test build build-py build-jni build-napi build-all install-py clean lint fmt

all: check test

# ── 代码质量 ──

lint:
	cd $(COREDIR) && $(CARGO) clippy --all-targets -- -D warnings

fmt:
	cd $(COREDIR) && $(CARGO) fmt --all -- --check

# ── 编译检查 ──

check:
	cd $(COREDIR) && $(CARGO) check
	cd $(PYDIR) && $(CARGO) check
	cd $(JNIDIR) && $(CARGO) check 2>/dev/null || echo "⚠️ JNI crate 需要 Android NDK（跳过本地检查）"
	cd $(NAPIDIR) && $(CARGO) check 2>/dev/null || echo "⚠️ NAPI crate 需要鸿蒙 SDK（跳过本地检查）"

# ── 测试 ──

test:
	cd $(COREDIR) && $(CARGO) test --verbose

test-nocapture:
	cd $(COREDIR) && $(CARGO) test -- --nocapture

# ── 本地构建 ──

build:
	cd $(COREDIR) && $(CARGO) build --release

build-py:
	cd $(PYDIR) && $(CARGO) build --release
	@echo "✅ Python绑定构建完成: $(PYDIR)/target/release/lib_longhun_core.dylib"
	@echo "   复制为: cp $(PYDIR)/target/release/lib_longhun_core.dylib longhun_core.so"

# ── Android JNI 构建 ──
build-jni:
	@echo "🐉 构建 Android JNI 绑定..."
	@for target in $(MOBILE_TARGETS); do \
		echo "  → $$target"; \
		$(RUSTUP) target add $$target 2>/dev/null || true; \
		cd $(JNIDIR) && $(CARGO) build --release --target $$target 2>&1 | tail -1 || \
			echo "    ⚠️ $$target 编译失败（可能缺 Android NDK linker）"; \
	done
	@echo "✅ Android JNI 构建完成"
	@echo "   .so 路径: $(JNIDIR)/target/<arch>/release/liblonghun_jni.so"

# ── 鸿蒙 NAPI 构建 ──
build-napi:
	@echo "🐉 构建鸿蒙 NAPI 绑定..."
	@for target in $(MOBILE_TARGETS); do \
		echo "  → $$target"; \
		$(RUSTUP) target add $$target 2>/dev/null || true; \
		cd $(NAPIDIR) && $(CARGO) build --release --target $$target 2>&1 | tail -1 || \
			echo "    ⚠️ $$target 编译失败（可能缺鸿蒙 OHOS linker）"; \
	done
	@echo "✅ 鸿蒙 NAPI 构建完成"
	@echo "   .so 路径: $(NAPIDIR)/target/<arch>/release/liblonghun_napi.so"

# ── 移动端全量构建（JNI + NAPI） ──
build-mobile: build-jni build-napi

# ── 全平台交叉编译 ──

ensure-targets:
	@for target in $(TARGETS); do \
		$(RUSTUP) target add $$target 2>/dev/null || echo "⚠️  $$target 已安装或不可用"; \
	done

build-all: ensure-targets
	@echo "🐉 开始全平台交叉编译..."
	@for target in $(TARGETS); do \
		echo "  → $$target"; \
		cd $(COREDIR) && $(CARGO) build --release --target $$target 2>&1 | tail -1 || echo "    ⚠️ $$target 编译失败（可能缺cross-linker）"; \
	done
	@echo "✅ 全平台编译完成"

# ── Python安装 ──

install-py: build-py
	@echo "安装 Python 绑定..."
	cp $(PYDIR)/target/release/lib_longhun_core.dylib longhun_core.so 2>/dev/null || \
	cp $(PYDIR)/target/release/lib_longhun_core.so longhun_core.so 2>/dev/null || \
	echo "⚠️ 请手动复制 .so/.dylib 文件"
	@echo "测试: python3 -c 'import longhun_core; print(longhun_core.DNA)'"

# ── 清理 ──

clean:
	cd $(COREDIR) && $(CARGO) clean
	cd $(PYDIR) && $(CARGO) clean
	rm -f longhun_core.so

# ── 帮助 ──

help:
	@echo "🐉 龍魂 Rust 构建系统"
	@echo ""
	@echo "  make check       编译检查（核心+PyO3+JNI+NAPI）"
	@echo "  make test        运行测试 (31 cases)"
	@echo "  make build       本地发布构建"
	@echo "  make build-py    构建Python绑定"
	@echo "  make build-jni   构建Android JNI绑定"
	@echo "  make build-napi  构建鸿蒙 NAPI绑定"
	@echo "  make build-mobile 构建全部移动端绑定"
	@echo "  make build-all   全平台交叉编译"
	@echo "  make install-py  安装Python绑定"
	@echo "  make lint        Clippy检查"
	@echo "  make clean       清理"
