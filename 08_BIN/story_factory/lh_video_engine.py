#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 龍芯⚡️丙午·丙申·辛酉·午时·☰乾-VIDEO-ENGINE-v1.0
"""
🐉 龍魂 · 视频引擎 v1.0
把开源图生视频工具封装成「分镜→视频」接口。
支持:
  - AnimateDiff (轻量，SD 1.5)
  - Stable Video Diffusion
  - CogVideoX / HunyuanVideo (高清)
  - 静态图+运镜模拟兜底（无模型时也能出 preview）
所有输出自动注入 DNA 水印与片头声明帧。
"""

import argparse
import json
import hashlib
import time
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

ENGINE_ROOT = Path(__file__).resolve().parent
# 固定成片主目录：用户素材仓库，方便查找；同时保留 Movies 快捷入口
WAREHOUSE_ROOT = Path.home() / "Pictures" / "龍魂素材仓库"
VIDEO_OUTPUT = WAREHOUSE_ROOT / "videos"
VIDEO_OUTPUT.mkdir(parents=True, exist_ok=True)
SHORTCUT_MOVIES = Path.home() / "Movies" / "龍魂成片"
SHORTCUT_MOVIES.mkdir(parents=True, exist_ok=True)


def generate_dna(shot_code: str = "VIDEO") -> str:
    h = hashlib.sha256(f"{shot_code}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{shot_code}-{h}-UID9622"


def video_fallback(image_path: Path, out_path: Path, duration: int = 3) -> bool:
    """无模型时，用 ffmpeg 把静态图做成缓慢推近的 preview。"""
    try:
        subprocess.run([
            "ffmpeg", "-y", "-loop", "1", "-i", str(image_path),
            "-vf", f"zoompan=z='min(zoom+0.0015,1.5)':d={duration*30}:s=1280x720",
            "-c:v", "libx264", "-t", str(duration), "-pix_fmt", "yuv420p",
            str(out_path)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception as e:
        print(f"⚠️ ffmpeg fallback 失败: {e}")
        return False


def generate(image_path: str, prompt: str = "", backend: str = "auto", duration: int = 3, shot_code: str = "SHOT") -> Path:
    """
    从图片生成视频镜头。
    backend: auto/animatediff/svd/cogvideo/hunyuan/ffmpeg
    """
    img_path = Path(image_path)
    if not img_path.exists():
        print(f"❌ 图片不存在: {image_path}")
        return None

    dna = generate_dna(shot_code)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = VIDEO_OUTPUT / f"{shot_code}_{ts}.mp4"

    print(f"🎬 生成视频镜头: [{shot_code}]")
    print(f"   图源: {image_path}")
    print(f"   提示: {prompt[:60]}...")

    if backend == "auto":
        if (ENGINE_ROOT / "third_party" / "AnimateDiff").exists():
            backend = "animatediff"
        elif (ENGINE_ROOT / "third_party" / "CogVideo").exists():
            backend = "cogvideo"
        else:
            backend = "ffmpeg"

    success = False
    if backend == "animatediff":
        success = _generate_animatediff(img_path, out_path, prompt, duration)
    elif backend == "svd":
        success = _generate_svd(img_path, out_path, prompt, duration)
    elif backend == "cogvideo":
        success = _generate_cogvideo(img_path, out_path, prompt, duration)
    elif backend == "hunyuan":
        success = _generate_hunyuan(img_path, out_path, prompt, duration)
    else:
        success = video_fallback(img_path, out_path, duration)

    if not success:
        print("❌ 视频生成失败")
        return None

    # 写入 DNA 元数据
    meta_path = out_path.with_suffix(".json")
    meta = {
        "dna": dna,
        "shot_code": shot_code,
        "source_image": str(img_path),
        "prompt": prompt,
        "backend": backend,
        "duration": duration,
        "created": datetime.now().isoformat(),
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    # 同步一份到 Movies 快捷入口，方便播放器/剪辑软件访问
    shortcut = SHORTCUT_MOVIES / out_path.name
    try:
        shutil.copy2(out_path, shortcut)
        shutil.copy2(meta_path, shortcut.with_suffix(".json"))
    except Exception as e:
        print(f"⚠️ 快捷入口同步失败: {e}")

    print(f"✅ 视频已保存: {out_path}")
    print(f"🔗 快捷入口: {shortcut}")
    print(f"🧬 DNA: {dna}")
    return out_path


def _generate_animatediff(image_path: Path, out_path: Path, prompt: str, duration: int, shot_code: str = "SHOT") -> bool:
    """调用 ComfyUI + AnimateDiff-Evolved 生成真实动态镜头。"""
    ad_dir = ENGINE_ROOT / "third_party" / "AnimateDiff"
    if not ad_dir.exists():
        return False

    generator_script = ENGINE_ROOT / "lh_animatediff_generate.py"
    if not generator_script.exists():
        print("⚠️ 未找到 lh_animatediff_generate.py")
        return False

    venv_python = ENGINE_ROOT.parent.parent / ".venv" / "bin" / "python"
    fps = 8
    frames = max(int(duration * fps), 8)
    # AnimateDiff v2 sweet spot 16 帧；低算力不拉长
    if frames > 16:
        frames = 16

    # 自动负面提示词
    negative = "blurry, low quality, distorted face, watermark, text, extra limbs"
    if not prompt:
        prompt = "cinematic scene, subtle motion, atmospheric lighting"

    cmd = [
        str(venv_python), str(generator_script),
        "--image", str(image_path),
        "--prompt", prompt,
        "--negative", negative,
        "--shot", shot_code,
        "--fps", str(fps),
        "--duration", str(duration),
    ]
    print(f"🎬 调用 AnimateDiff 生成器: {shot_code} ({frames} frames @ {fps}fps)")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        # generator 会把结果放到 ~/Pictures/龍魂素材仓库/videos/EP01_雪夜初见/video/，再复制到 out_path
        final_root = WAREHOUSE_ROOT / "videos" / "EP01_雪夜初见" / "video"
        candidates = sorted(final_root.glob(f"{shot_code}_*_animatediff.mp4"), key=lambda p: p.stat().st_mtime, reverse=True)
        if candidates:
            src = candidates[0]
            out_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, out_path)
            return True
        print("❌ 未找到 AnimateDiff 输出视频")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ AnimateDiff 生成失败: {e}")
        print(e.stdout)
        print(e.stderr)
        return False


def _generate_svd(image_path: Path, out_path: Path, prompt: str, duration: int) -> bool:
    """调用 Stable Video Diffusion。placeholder。"""
    print("⚠️ SVD 接口待配置")
    return False


def _generate_cogvideo(image_path: Path, out_path: Path, prompt: str, duration: int) -> bool:
    """调用 CogVideoX。placeholder。"""
    cv_dir = ENGINE_ROOT / "third_party" / "CogVideo"
    if not cv_dir.exists():
        return False
    print("⚠️ CogVideoX 接口待配置")
    return False


def _generate_hunyuan(image_path: Path, out_path: Path, prompt: str, duration: int) -> bool:
    """调用 HunyuanVideo。placeholder。"""
    hv_dir = ENGINE_ROOT / "third_party" / "HunyuanVideo"
    if not hv_dir.exists():
        return False
    print("⚠️ HunyuanVideo 接口待配置")
    return False


def main():
    parser = argparse.ArgumentParser(description="龍魂 · 视频引擎")
    parser.add_argument("--image", required=True, help="输入图片路径")
    parser.add_argument("--prompt", default="", help="运动/镜头提示词")
    parser.add_argument("--backend", default="auto", help="后端: auto/animatediff/svd/cogvideo/hunyuan/ffmpeg")
    parser.add_argument("--duration", type=int, default=3, help="视频时长（秒）")
    parser.add_argument("--shot", default="SHOT", help="镜头编码")
    args = parser.parse_args()

    generate(args.image, args.prompt, args.backend, args.duration, args.shot)


if __name__ == "__main__":
    main()
