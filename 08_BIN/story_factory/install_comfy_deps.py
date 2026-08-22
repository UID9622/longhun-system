# DNA: #龍芯⚡️丙午·丙申·戊辰·丙辰·䷸巽为风-CODE-补DNA-cdab1438
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂 · ComfyUI/AnimateDiff 安全依赖安装器
保护项目 venv 已有的 torch 2.13.0 / transformers，跳过 CUDA/macOS 不兼容包。
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
TOOLS_DIR = FACTORY_DIR / "third_party"
COMFY_DIR = TOOLS_DIR / "ComfyUI"
AD_DIR = TOOLS_DIR / "AnimateDiff"

# 保护已有环境：这些包不降级/不重装
PROTECT = {"torch", "torchvision", "torchaudio", "transformers", "diffusers", "accelerate"}
# macOS 上编译不了或需要 CUDA 的包
PLATFORM_SKIP = {"xformers", "decord", "triton", "triton-mlir", "flash-attn"}


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

        if pkg_name in PROTECT:
            try:
                installed = get_version(req.name)
                print(f"✅ 保护 {req.name} {installed}，跳过 {line}")
                skipped.append(f"{line} （已有 {installed}）")
                continue
            except Exception:
                pass  # 未安装则走正常安装

        try:
            installed = get_version(req.name)
            if Version(installed) in req.specifier:
                print(f"✅ {req.name} {installed} 已满足 {line}")
                continue
            else:
                if pkg_name in PROTECT:
                    print(f"⚠️ 保护 {req.name} {installed}，跳过 {line}")
                    skipped.append(f"{line} （已有 {installed}）")
                    continue
                print(f"⚠️ {req.name} {installed} 与 {line} 冲突，但非保护包，尝试升级")
        except Exception:
            pass

        to_install.append(line)

    failed = []
    if to_install:
        print(f"📦 安装: {to_install}")
        result = subprocess.run([sys.executable, "-m", "pip", "install"] + to_install)
        if result.returncode != 0:
            failed.extend(to_install)
    else:
        print("✅ 无需安装额外依赖")

    return to_install, skipped, failed


def main():
    print("🐉 龍魂 · ComfyUI/AnimateDiff 安全依赖安装")
    print(f"平台: {platform.system()} {platform.machine()}")
    print(f"Python: {sys.version}")
    try:
        print(f"torch: {get_version('torch')}")
    except Exception as e:
        print(f"torch: 未安装 ({e})")

    for name, req_path in [
        ("ComfyUI", COMFY_DIR / "requirements.txt"),
        ("AnimateDiff", AD_DIR / "requirements.txt"),
    ]:
        print(f"\n=== {name} ===")
        installed, skipped, failed = smart_install(req_path)
        if skipped:
            print("⏭️ 跳过:")
            for s in skipped:
                print(f"   - {s}")
        if failed:
            print("❌ 失败:")
            for f in failed:
                print(f"   - {f}")

    print("\n✅ 安全依赖安装完成")


if __name__ == "__main__":
    main()
