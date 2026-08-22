#!/bin/bash
# 🐉 龍魂 · 故事工厂 · 开源工具链一键安装脚本
# DNA: #龍芯⚡️丙午·丙申·辛酉·巳时·䷀乾-STORY-TOOLS-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -e

FACTORY_DIR="$(cd "$(dirname "$0")" && pwd)"
TOOLS_DIR="$FACTORY_DIR/third_party"
mkdir -p "$TOOLS_DIR"

# ============================================================
# 优先使用项目虚拟环境（.venv），避免污染系统 Python
# ============================================================
PROJECT_VENV="$FACTORY_DIR/../../.venv"
if [ -f "$PROJECT_VENV/bin/pip" ]; then
    PYTHON_BIN="$PROJECT_VENV/bin/python3"
    PIP_BIN="$PROJECT_VENV/bin/pip"
    echo "✅ 检测到项目虚拟环境: $PROJECT_VENV"
else
    PYTHON_BIN="python3"
    PIP_BIN="pip"
    echo "⚠️  未检测到项目虚拟环境，将使用系统 Python: $(which python3)"
fi

echo "🐉 龍魂故事工厂 · 开源工具链安装"
echo "=================================="
echo ""
echo "本脚本仅克隆仓库并安装 Python 依赖。大型模型文件需要额外下载。"
echo ""

# ============================================================
# 辅助函数：智能安装 requirements
# 规则：
#   1. 已安装且版本满足 → 跳过
#   2. 已安装但版本冲突 → 跳过（不破坏现有 torch/transformers/diffusers）
#   3. macOS 平台不兼容包（xformers/decord/triton）→ 跳过
#   4. 安装失败不致命，记录到 failed 列表
# ============================================================
safe_pip_install() {
    local req_file="$1"
    if [ ! -f "$req_file" ]; then
        echo "⚠️  未找到 requirements: $req_file，跳过"
        return 0
    fi
    echo "🔧 智能检测依赖冲突（保护现有 torch/transformers/diffusers 环境）..."
    $PYTHON_BIN - "$req_file" <<'PY'
import sys, subprocess, platform
from packaging.requirements import Requirement
from packaging.version import Version

try:
    from importlib.metadata import version as get_version
except ImportError:
    from importlib_metadata import version as get_version

req_file = sys.argv[1]
system = platform.system()
# macOS 上无 CUDA，这些包原生编译不了或需要特定环境
platform_skip = {"xformers", "decord", "triton", "triton-mlir"}

with open(req_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

to_install = []
skipped = []
for raw in lines:
    line = raw.strip()
    if not line or line.startswith("#"):
        continue
    try:
        req = Requirement(line)
    except Exception as e:
        skipped.append(f"{line} （解析失败: {e}）")
        continue
    pkg_name = req.name
    if system == "Darwin" and pkg_name.lower() in platform_skip:
        skipped.append(f"{line} （macOS 平台跳过）")
        continue
    try:
        installed = get_version(pkg_name)
    except Exception:
        installed = None
    if installed:
        try:
            if Version(installed) in req.specifier:
                print(f"✅ {pkg_name} {installed} 已满足 {line}")
                continue
            else:
                print(f"⚠️  {pkg_name} {installed} 与 {line} 冲突，跳过（保护现有环境）")
                skipped.append(f"{line} （已有 {installed}）")
                continue
        except Exception as e:
            print(f"⚠️  无法比较 {pkg_name} 版本: {e}，跳过 {line}")
            skipped.append(f"{line} （版本比较失败）")
            continue
    to_install.append(line)

failed = []
if to_install:
    print("📦 安装剩余依赖:", " ".join(to_install[:10]), "..." if len(to_install) > 10 else "")
    result = subprocess.run([sys.executable, "-m", "pip", "install"] + to_install)
    if result.returncode != 0:
        failed.extend(to_install)
else:
    print("✅ 无需安装额外依赖")

if skipped:
    print("")
    print("⏭️  以下依赖已跳过（不影响主线工具链）：")
    for s in skipped:
        print(f"   - {s}")
if failed:
    print("")
    print("❌ 以下依赖安装失败（可后续手动处理）：")
    for f in failed:
        print(f"   - {f}")
PY
}

# ============================================================
# 1. ComfyUI
# ============================================================
if [ -d "$TOOLS_DIR/ComfyUI" ]; then
    echo "✅ ComfyUI 已存在，跳过"
else
    echo "📦 安装 ComfyUI..."
    git clone https://github.com/comfyanonymous/ComfyUI.git "$TOOLS_DIR/ComfyUI"
    cd "$TOOLS_DIR/ComfyUI"
    $PIP_BIN install -r requirements.txt
    cd "$FACTORY_DIR"
fi

# ============================================================
# 2. IPAdapter Plus
# ============================================================
if [ -d "$TOOLS_DIR/ComfyUI/custom_nodes/ComfyUI_IPAdapter_plus" ]; then
    echo "✅ IPAdapter Plus 已存在，跳过"
else
    echo "📦 安装 IPAdapter Plus..."
    git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus.git \
        "$TOOLS_DIR/ComfyUI/custom_nodes/ComfyUI_IPAdapter_plus"
fi

# ============================================================
# 3. AnimateDiff
# ============================================================
if [ -d "$TOOLS_DIR/AnimateDiff" ]; then
    echo "✅ AnimateDiff 已存在，跳过"
else
    echo "📦 克隆 AnimateDiff..."
    git clone https://github.com/guoyww/AnimateDiff.git "$TOOLS_DIR/AnimateDiff"
    if [ "$(uname)" = "Darwin" ]; then
        echo "🍎 macOS  detected：AnimateDiff 原生运行需要 CUDA/xformers，已占位克隆，不安装依赖。"
        echo "   图生视频请走 ComfyUI 工作流，或 Linux/CUDA 环境再执行安全安装。"
    else
        cd "$TOOLS_DIR/AnimateDiff"
        safe_pip_install requirements.txt
        cd "$FACTORY_DIR"
    fi
fi

# ============================================================
# 4. GPT-SoVITS
# ============================================================
if [ -d "$TOOLS_DIR/GPT-SoVITS" ]; then
    echo "✅ GPT-SoVITS 已存在，跳过"
else
    echo "📦 克隆 GPT-SoVITS..."
    git clone https://github.com/RVC-Boss/GPT-SoVITS.git "$TOOLS_DIR/GPT-SoVITS"
    if [ "$(uname)" = "Darwin" ]; then
        echo "🍎 macOS detected：GPT-SoVITS 原生运行需要 CUDA 与大量编译依赖，已占位克隆，不安装依赖。"
        echo "   语音合成当前走系统 say / ffmpeg 兜底，或 Linux/CUDA 环境再执行安全安装。"
    else
        cd "$TOOLS_DIR/GPT-SoVITS"
        safe_pip_install requirements.txt
        cd "$FACTORY_DIR"
    fi
fi

# ============================================================
# 5. Pillow（素材索引/水印必需）
# ============================================================
echo "📦 安装 Pillow..."
$PIP_BIN install Pillow

# ============================================================
# 6. C2PA Python SDK
# ============================================================
echo "📦 安装 C2PA Python SDK..."
$PIP_BIN install c2pa-python

# ============================================================
# 7. 轻量隐写
# ============================================================
echo "📦 安装 stegano..."
$PIP_BIN install stegano

echo ""
echo "=================================="
echo "✅ 龍魂故事工厂工具链安装完成"
echo ""
echo "下一步："
echo "  1. 下载 Stable Diffusion 基础模型到 third_party/ComfyUI/models/"
echo "  2. 下载 IPAdapter FaceID 模型到 third_party/ComfyUI/models/ipadapter/"
echo "  3. 运行: python3 lh_story_factory.py init <项目名>"
echo ""
echo "🧬 DNA: #龍芯⚡️丙午·丙申·辛酉·巳时·䷀乾-STORY-TOOLS-UID9622"
echo "=================================="
