# DNA: #龍芯⚡️丙午·丙申·戊辰·丙辰·䷸巽为风-CODE-补DNA-9ea655a3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂 · MeloTTS 安全依赖安装器
保护项目 venv 已有的 torch 2.13.0 / torchaudio / transformers，不降级。
"""
import sys
import subprocess
import platform
from pathlib import Path
from packaging.requirements import Requirement
from packaging.version import Version

try:
    from importlib.metadata import version as get_version
except ImportError:
    from importlib_metadata import version as get_version

FACTORY_DIR = Path(__file__).resolve().parent
MELO_DIR = FACTORY_DIR / "third_party" / "MeloTTS"
REQ_FILE = MELO_DIR / "requirements.txt"

# 保护已有环境：这些包不降级/不重装
PROTECT = {"torch", "torchvision", "torchaudio", "transformers", "diffusers", "accelerate", "librosa", "numpy", "scipy", "scikit-learn"}
# macOS 上编译不了或需要 CUDA 的包
PLATFORM_SKIP = {"xformers", "decord", "triton", "triton-mlir", "flash-attn"}
# fugashi 需要系统 MeCab；中文场景下通过 patch 懒加载日语 tokenizer 来规避
OPTIONAL_SKIP = {"fugashi", "unidic"}


def smart_install(req_file: Path) -> tuple[list[str], list[str], list[str]]:
    """返回 (installed, skipped, failed)"""
    if not req_file.exists():
        return [], [], [f"文件不存在: {req_file}"]

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

        pkg_name = req.name.lower()
        if pkg_name in PLATFORM_SKIP:
            skipped.append(f"{line} （macOS/CUDA 平台跳过）")
            continue
        if pkg_name in OPTIONAL_SKIP:
            skipped.append(f"{line} （中文TTS可选，跳过）")
            continue

        # 保护核心包：torch/transformers/numpy 等不降级
        if pkg_name in PROTECT:
            try:
                installed = get_version(req.name)
                print(f"✅ 保护 {req.name} {installed}，跳过 {line}")
                skipped.append(f"{line} （已有 {installed}）")
                continue
            except Exception:
                # 未安装：装最新版，不 pinned 老版（避免 numpy/librosa 降级）
                print(f"📦 {req.name} 未安装，改安装最新版（避免 {line} 降级依赖）")
                to_install.append(req.name)
                continue

        try:
            installed = get_version(req.name)
            if Version(installed) in req.specifier:
                print(f"✅ {req.name} {installed} 已满足 {line}")
                continue
            print(f"⚠️ {req.name} {installed} 与 {line} 冲突，尝试升级")
        except Exception:
            pass

        to_install.append(line)

    failed = []
    if to_install:
        print(f"\n📦 安装: {to_install}")
        result = subprocess.run([sys.executable, "-m", "pip", "install"] + to_install)
        if result.returncode != 0:
            failed.extend(to_install)
    else:
        print("✅ 无需安装额外依赖")

    return to_install, skipped, failed


def download_unidic():
    """下载 unidic 字典（MeloTTS 日语支持需要；中文可选）。"""
    import os
    print("\n📚 下载 unidic 字典...")
    # 使用 HF 镜像加速
    env = os.environ.copy()
    if "HF_ENDPOINT" not in env:
        env["HF_ENDPOINT"] = "https://hf-mirror.com"
    result = subprocess.run(
        [sys.executable, "-m", "unidic", "download"],
        env=env,
    )
    if result.returncode != 0:
        print("⚠️ unidic 下载失败，可手动下载后重试")
        return False
    return True


def restore_numpy():
    """某些依赖（gruut/g2p_en）会间接把 numpy 降到 1.x，恢复它。"""
    try:
        import numpy as np
        if int(np.__version__.split(".")[0]) < 2:
            print(f"\n🔄 numpy 被降级到 {np.__version__}，恢复至 2.x...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "numpy>=2.0.2"])
            if result.returncode == 0:
                print("✅ numpy 恢复完成")
            else:
                print("⚠️ numpy 恢复失败")
    except Exception as e:
        print(f"⚠️ 检查 numpy 失败: {e}")


def main():
    import os
    print("🐉 龍魂 · MeloTTS 安全依赖安装")
    print(f"平台: {platform.system()} {platform.machine()}")
    print(f"Python: {sys.version}")
    try:
        print(f"torch: {get_version('torch')}")
    except Exception as e:
        print(f"torch: 未安装 ({e})")

    installed, skipped, failed = smart_install(REQ_FILE)
    if skipped:
        print("\n⏭️ 跳过:")
        for s in skipped:
            print(f"   - {s}")
    if failed:
        print("\n❌ 失败:")
        for f in failed:
            print(f"   - {f}")

    restore_numpy()

    # 应用中文懒加载补丁
    print("\n🔧 应用 MeloTTS 中文懒加载补丁...")
    patch_script = FACTORY_DIR / "patch_melotts_for_zh.py"
    if patch_script.exists():
        subprocess.run([sys.executable, str(patch_script)])

    print("\n✅ MeloTTS 安全依赖安装完成")


if __name__ == "__main__":
    main()
