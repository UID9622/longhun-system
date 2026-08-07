#!/bin/bash
# DNA: #龍芯⚡️丙午·丙申·壬子·丑时·䷖剥-BUILD-DEPLOY-HARMONY-v1.0-UID9622
# 確認碼: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 分層許可: 工程層 MulanPSL v2
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
#
# 🐉 龍魂鸿蒙插件生态 · 一键编译部署
# 
# 流程:
#   Step 1/5: Rust NAPI/JNI 交叉编译 → .so
#   Step 2/5: 复制 .so 到各插件 libs/arm64-v8a/
#   Step 3/5: hvigorw 构建 HAP（需 DevEco Studio）
#   Step 4/5: GPG 签章全部产物
#   Step 5/5: 可选 → 同步到鲲鹏

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
RUST_DIR="$PROJECT_ROOT/rust"
PLUGINS_DIR="$PROJECT_ROOT/harmonyos/plugins"
OUTPUT_DIR="$PLUGINS_DIR/output"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log()   { echo -e "${GREEN}[$(date +%H:%M:%S)]${NC} $1"; }
warn()  { echo -e "${YELLOW}[$(date +%H:%M:%S)] ⚠️  $1${NC}"; }
error() { echo -e "${RED}[$(date +%H:%M:%S)] 🔴 $1${NC}"; }

echo ""
echo "🐉 =========================================="
echo "🐉  龍魂鸿蒙插件生态 · 一键编译部署"
echo "🐉  DNA: #龍芯⚡️丙午·丙申·壬子·丑时·䷖剥"
echo "🐉  时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "🐉 =========================================="
echo ""

# ═══════════════════════════════════════════════
# Step 1: Rust 交叉编译
# ═══════════════════════════════════════════════

log "Step 1/5: Rust 交叉编译 NAPI + JNI..."

# 目标: aarch64-unknown-linux-gnu（ARM64 Linux, C ABI 桥接, 鸿蒙兼容）
# NAPI crate 通过 C ABI 桥接，不依赖鸿蒙 SDK 头文件
# 无需 Android NDK — 只需 gcc-aarch64-linux-gnu 交叉编译器
RUST_TARGET="aarch64-unknown-linux-gnu"
RUST_TARGET_DIR="$RUST_DIR/target/$RUST_TARGET/release"

check_cross_compiler() {
    if command -v aarch64-linux-gnu-gcc &>/dev/null; then
        log "  aarch64 交叉编译器: $(which aarch64-linux-gnu-gcc)"
        return 0
    elif dpkg -l gcc-aarch64-linux-gnu &>/dev/null 2>&1; then
        log "  aarch64 交叉编译器: 已安装"
        return 0
    else
        warn "  gcc-aarch64-linux-gnu 未安装 — 尝试安装..."
        if command -v apt &>/dev/null; then
            apt-get install -y -qq gcc-aarch64-linux-gnu 2>&1 | tail -1 && return 0
        elif command -v yum &>/dev/null; then
            yum install -y gcc-aarch64-linux-gnu 2>&1 | tail -1 && return 0
        elif command -v brew &>/dev/null; then
            brew install aarch64-elf-gcc 2>&1 | tail -1 && return 0
        fi
        return 1
    fi
}

have_cross=false
if check_cross_compiler; then
    have_cross=true
fi

# 安装 Rust target
log "  安装 Rust 交叉编译 target: $RUST_TARGET..."
rustup target add "$RUST_TARGET" 2>/dev/null || true

if $have_cross; then
    log "  编译 longhun-core (核心库)..."
    cd "$RUST_DIR/longhun-core"
    cargo build --release --target "$RUST_TARGET" 2>&1 | tail -3 || warn "  longhun-core 编译失败"
    
    log "  编译 longhun-napi (鸿蒙 NAPI · C ABI桥接)..."
    cd "$RUST_DIR/longhun-napi"
    cargo build --release --target "$RUST_TARGET" 2>&1 | tail -3 || warn "  NAPI 编译失败"
    
    log "  编译 longhun-jni (Android JNI · C ABI桥接)..."
    cd "$RUST_DIR/longhun-jni"
    cargo build --release --target "$RUST_TARGET" 2>&1 | tail -3 || warn "  JNI 编译失败"
else
    warn "  跳过 Rust 交叉编译（无交叉编译器）— 将使用现有 .so 或 Mock"
    if [ "$(uname -m)" = "x86_64" ] && [ -f "/usr/bin/aarch64-linux-gnu-gcc" ]; then
        warn "  检测到鲲鹏环境 — 交叉编译器已存在，重新尝试..."
        cd "$RUST_DIR/longhun-napi" && cargo build --release --target "$RUST_TARGET" 2>&1 | tail -3
        cd "$RUST_DIR/longhun-jni" && cargo build --release --target "$RUST_TARGET" 2>&1 | tail -3
    fi
fi

# 本地测试
log "  Rust 核心库测试..."
cd "$RUST_DIR/longhun-core"
cargo test 2>&1 | tail -5 || warn "  部分测试未通过"

echo ""

# ═══════════════════════════════════════════════
# Step 2: 复制 .so 到插件目录
# ═══════════════════════════════════════════════

log "Step 2/5: 复制 .so 到插件 libs/ 目录..."

# 优先从 workspace target 目录找，其次从子项目目录
if [ -f "$RUST_TARGET_DIR/liblonghun_napi.so" ]; then
    NAPI_SO="$RUST_TARGET_DIR/liblonghun_napi.so"
    JNI_SO="$RUST_TARGET_DIR/liblonghun_jni.so"
else
    NAPI_SO="$RUST_DIR/longhun-napi/target/$RUST_TARGET/release/liblonghun_napi.so"
    JNI_SO="$RUST_DIR/longhun-jni/target/$RUST_TARGET/release/liblonghun_jni.so"
fi

copy_so() {
    local src="$1"
    local dest="$2"
    if [ -f "$src" ]; then
        cp "$src" "$dest"
        log "  ✅ $(basename $src) → $dest"
    else
        warn "  ⏭️ $(basename $src) 不存在（跳过）"
    fi
}

# 插件1 核心服务 — 需要 NAPI .so
copy_so "$NAPI_SO" "$PLUGINS_DIR/01-core-service/libs/arm64-v8a/liblonghun_napi.so"

# 插件6 跨设备同步 — 可选 NAPI
copy_so "$NAPI_SO" "$PLUGINS_DIR/06-cross-device-sync/libs/arm64-v8a/liblonghun_napi.so"

echo ""

# ═══════════════════════════════════════════════
# Step 3: Hvigor 构建 HAP
# ═══════════════════════════════════════════════

log "Step 3/5: Hvigor 构建 HAP..."

mkdir -p "$OUTPUT_DIR"

check_hvigor() {
    if command -v hvigorw &>/dev/null; then
        return 0
    elif [ -f "$PLUGINS_DIR/01-core-service/hvigorw" ]; then
        return 0
    else
        return 1
    fi
}

if check_hvigor; then
    log "  Hvigor 已就绪，开始构建..."
    for plugin_dir in "$PLUGINS_DIR"/0* "$PLUGINS_DIR"/1*; do
        if [ -d "$plugin_dir" ]; then
            plugin_name=$(basename "$plugin_dir")
            log "  构建 $plugin_name..."
            cd "$plugin_dir"
            if hvigorw assembleHap --mode module 2>&1 | tail -2; then
                log "    ✅ $plugin_name 构建成功"
                # 复制产物
                find . -name "*.hap" -exec cp {} "$OUTPUT_DIR/" \; 2>/dev/null || true
            else
                warn "    ⚠️ $plugin_name 构建失败（可能需要 DevEco Studio）"
            fi
        fi
    done
else
    warn "  Hvigor 未安装 — 跳过 HAP 构建"
    warn "  请用 DevEco Studio 打开 harmonyos/plugins/ 目录手动构建"
fi

echo ""

# ═══════════════════════════════════════════════
# Step 4: GPG 签章
# ═══════════════════════════════════════════════

log "Step 4/5: GPG 签章全部产物..."

cd "$PROJECT_ROOT"
python3 bin/lh_gpg_sign.py sign harmonyos/plugins/ 2>&1 | grep -E "(✅|❌)" || warn "  GPG签名可能需要密钥"

echo ""

# ═══════════════════════════════════════════════
# Step 5: 可选 — 同步鲲鹏
# ═══════════════════════════════════════════════

log "Step 5/5: 同步鲲鹏..."

SYNC_FLAG="$PROJECT_ROOT/.longhun_skip_kunpeng_sync"
if [ -f "$SYNC_FLAG" ]; then
    warn "  检测到跳过标记 .longhun_skip_kunpeng_sync — 跳过鲲鹏同步"
else
    if [ -f "$PROJECT_ROOT/deploy/sync-to-kunpeng.sh" ]; then
        log "  同步 harmonyos/ 到鲲鹏..."
        bash "$PROJECT_ROOT/deploy/sync-to-kunpeng.sh" harmonyos/plugins/ 2>&1 | tail -3 || warn "  鲲鹏同步失败（可能网络不通）"
    else
        warn "  同步脚本不存在，跳过"
    fi
fi

echo ""

# ═══════════════════════════════════════════════
# 总结
# ═══════════════════════════════════════════════

echo "🐉 =========================================="
echo "🐉  构建部署完成"
echo "🐉 =========================================="
echo ""

log "产物目录: $OUTPUT_DIR"
ls -la "$OUTPUT_DIR" 2>/dev/null || warn "  (无 HAP 产物 — 需 DevEco Studio 构建)"

log "插件目录: $PLUGINS_DIR"
log "插件总数: $(ls -d $PLUGINS_DIR/0* $PLUGINS_DIR/1* 2>/dev/null | wc -l | tr -d ' ')"

log "Rust .so 文件:"
find "$PLUGINS_DIR" -name "*.so" -exec ls -lh {} \; 2>/dev/null || warn "  (无 .so — 需 Android NDK 编译)"

echo ""
log "下一步（手动）:"
log "  1. DevEco Studio 打开 harmonyos/plugins/ → 构建 HAP"
log "  2. 连接鸿蒙设备 → 安装 HAP"
log "  3. 启动 01-core-service → 验证 IPC 连接"
log "  4. 安装其他插件 → 测试 Super Device"
echo ""
log "🐉 丙午·丑时·䷖剥·🟡"
