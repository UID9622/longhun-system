#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂 · AnimateDiff 真实动态镜头生成器 v1.0
调用本地 ComfyUI + AnimateDiff-Evolved，把单张图变成带真实运动的短视频。
输出固定到 ~/Movies/龍魂成片/ 下，不再玩 zoompan。
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

FACTORY_DIR = Path(__file__).resolve().parent
COMFY_DIR = FACTORY_DIR / "third_party" / "ComfyUI"
INPUT_DIR = COMFY_DIR / "input"
OUTPUT_DIR = COMFY_DIR / "output"
VENV_PYTHON = Path.home() / "longhun-system" / ".venv" / "bin" / "python"

# 固定成片主目录：素材仓库 videos，同时同步到 Movies 快捷入口
WAREHOUSE_ROOT = Path.home() / "Pictures" / "龍魂素材仓库"
FINAL_ROOT = WAREHOUSE_ROOT / "videos"
SHORTCUT_MOVIES = Path.home() / "Movies" / "龍魂成片"


def generate_dna(shot_code: str = "ANIMATEDIFF") -> str:
    import hashlib
    h = hashlib.sha256(f"{shot_code}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{shot_code}-{h}-UID9622"


def build_workflow(image_name: str, prompt: str, negative_prompt: str, steps: int = 20, fps: int = 8, frames: int = 12) -> dict:
    """构建 ComfyUI AnimateDiff img2vid 工作流 JSON（适配新 API 节点）。"""
    return {
        "1": {
            "inputs": {"ckpt_name": "v1-5-pruned-emaonly.ckpt"},
            "class_type": "CheckpointLoaderSimple",
            "_meta": {"title": "Load Checkpoint"}
        },
        "2": {
            "inputs": {
                "model": ["1", 0],
                "model_name": "mm_sd_v15_v2.ckpt",
                "beta_schedule": "autoselect"
            },
            "class_type": "ADE_AnimateDiffLoaderGen1",
            "_meta": {"title": "AnimateDiff Loader"}
        },
        "3": {
            "inputs": {"image": image_name},
            "class_type": "LoadImage",
            "_meta": {"title": "Load Image"}
        },
        "3b": {
            "inputs": {
                "image": ["3", 0],
                "width": 384,
                "height": 384,
                "upscale_method": "lanczos",
                "crop": "center"
            },
            "class_type": "ImageScale",
            "_meta": {"title": "Scale to 512"}
        },
        "4": {
            "inputs": {
                "pixels": ["3b", 0],
                "vae": ["1", 2]
            },
            "class_type": "VAEEncode",
            "_meta": {"title": "VAE Encode"}
        },
        "4b": {
            "inputs": {
                "samples": ["4", 0],
                "amount": frames
            },
            "class_type": "RepeatLatentBatch",
            "_meta": {"title": f"Repeat to {frames} frames"}
        },
        "5": {
            "inputs": {"text": prompt, "clip": ["1", 1]},
            "class_type": "CLIPTextEncode",
            "_meta": {"title": "Positive Prompt"}
        },
        "6": {
            "inputs": {"text": negative_prompt, "clip": ["1", 1]},
            "class_type": "CLIPTextEncode",
            "_meta": {"title": "Negative Prompt"}
        },
        "7": {
            "inputs": {
                "model": ["2", 0],
                "seed": 9622,
                "steps": steps,
                "cfg": 7.5,
                "sampler_name": "euler_ancestral",
                "scheduler": "normal",
                "positive": ["5", 0],
                "negative": ["6", 0],
                "latent_image": ["4b", 0],
                "denoise": 0.72
            },
            "class_type": "KSampler",
            "_meta": {"title": "KSampler"}
        },
        "8": {
            "inputs": {
                "samples": ["7", 0],
                "vae": ["1", 2]
            },
            "class_type": "VAEDecode",
            "_meta": {"title": "VAE Decode"}
        },
        "9": {
            "inputs": {
                "images": ["8", 0],
                "fps": float(fps)
            },
            "class_type": "CreateVideo",
            "_meta": {"title": "Create Video"}
        },
        "10": {
            "inputs": {
                "video": ["9", 0],
                "filename_prefix": "video/animate",
                "format": "auto",
                "codec": "h264"
            },
            "class_type": "SaveVideo",
            "_meta": {"title": "Save Video"}
        }
    }


def wait_for_server(url: str, timeout: int = 120) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            urllib.request.urlopen(url, timeout=2)
            return True
        except Exception:
            time.sleep(1)
    return False


def find_latest_video() -> Path:
    """在 ComfyUI output 目录找最新的 mp4/webm。"""
    candidates = []
    for pattern in ["video/*.mp4", "video/*.webm", "*.mp4", "*.webm"]:
        candidates.extend(OUTPUT_DIR.glob(pattern))
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def generate(image_path: Path, prompt: str, negative_prompt: str, duration_sec: int = 3, shot_code: str = "SHOT", fps: int = 8) -> Path:
    """生成真实动态镜头并复制到固定成片目录。"""
    image_path = Path(image_path)
    if not image_path.exists():
        print(f"❌ 图片不存在: {image_path}")
        return None

    dna = generate_dna(shot_code)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_dir = FINAL_ROOT / "EP01_雪夜初见" / "video"
    final_dir.mkdir(parents=True, exist_ok=True)
    final_path = final_dir / f"{shot_code}_{ts}_animatediff.mp4"

    # 复制到 ComfyUI input
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    input_name = f"{shot_code}_{ts}.png"
    comfy_input = INPUT_DIR / input_name
    shutil.copy2(image_path, comfy_input)

    # 帧数由时长决定；AnimateDiff v2 甜点 16 帧，超过容易崩
    frames = min(max(int(duration_sec * fps), 8), 16)

    # 生成工作流
    workflow = build_workflow(input_name, prompt, negative_prompt, steps=12, fps=fps, frames=frames)
    workflow_file = FACTORY_DIR / f"workflow_{shot_code}_{ts}.json"
    with open(workflow_file, "w", encoding="utf-8") as f:
        json.dump(workflow, f, ensure_ascii=False, indent=2)

    print(f"🎬 真实动态镜头生成: [{shot_code}]")
    print(f"   图源: {image_path}")
    print(f"   提示: {prompt[:60]}...")
    print(f"   DNA: {dna}")

    # 启动 ComfyUI server
    server_url = "http://127.0.0.1:8188"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(COMFY_DIR)
    # 优先 MPS（Apple Silicon），回退 CPU；不碰 CUDA
    env["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

    server_cmd = [
        str(VENV_PYTHON), "main.py",
        "--listen", "127.0.0.1",
        "--port", "8188",
    ]
    print("🚀 启动 ComfyUI server (MPS/CPU 模式)...")
    server_log = FACTORY_DIR / f"comfy_server_{shot_code}_{ts}.log"
    server_proc = subprocess.Popen(
        server_cmd,
        cwd=str(COMFY_DIR),
        env=env,
        stdout=open(server_log, "w"),
        stderr=subprocess.STDOUT,
    )

    try:
        if not wait_for_server(server_url + "/system_stats", timeout=120):
            print("❌ ComfyUI server 启动超时")
            return None
        print("✅ ComfyUI server 就绪")

        # 提交工作流
        prompt_payload = {"prompt": workflow}
        req = urllib.request.Request(
            server_url + "/prompt",
            data=json.dumps(prompt_payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        print("📤 提交工作流...")
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        prompt_id = result.get("prompt_id")
        print(f"   prompt_id: {prompt_id}")

        # 轮询完成
        print("⏳ 等待生成完成（CPU 较慢，请耐心）...")
        for _ in range(1200):  # 最多等 20 分钟
            time.sleep(1)
            try:
                with urllib.request.urlopen(server_url + f"/history/{prompt_id}", timeout=10) as resp:
                    history = json.loads(resp.read().decode("utf-8"))
                if prompt_id in history and history[prompt_id].get("outputs"):
                    print("✅ 工作流执行完成")
                    break
            except Exception:
                pass
        else:
            print("❌ 等待生成超时")
            return None

        # 找到输出视频（历史完成后稍等文件落盘）
        out_video = None
        for _ in range(30):
            out_video = find_latest_video()
            if out_video and out_video.exists() and out_video.stat().st_size > 1024:
                break
            time.sleep(1)
        if not out_video or not out_video.exists():
            print("❌ 未找到输出视频")
            return None

        shutil.copy2(out_video, final_path)
        print(f"✅ 视频已保存: {final_path}")

        # 同步快捷入口
        try:
            shortcut_dir = SHORTCUT_MOVIES / "EP01_雪夜初见" / "video"
            shortcut_dir.mkdir(parents=True, exist_ok=True)
            shortcut = shortcut_dir / final_path.name
            shutil.copy2(final_path, shortcut)
            print(f"🔗 快捷入口: {shortcut}")
        except Exception as e:
            print(f"⚠️ 快捷入口同步失败: {e}")

        # 写元数据
        meta_path = final_path.with_suffix(".json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump({
                "dna": dna,
                "shot_code": shot_code,
                "source_image": str(image_path),
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "fps": fps,
                "frames": frames,
                "duration_sec": frames / fps,
                "backend": "animatediff_comfyui",
                "created": datetime.now().isoformat(),
            }, f, ensure_ascii=False, indent=2)

        return final_path

    finally:
        print("🛑 关闭 ComfyUI server...")
        server_proc.terminate()
        try:
            server_proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            server_proc.kill()


def main():
    parser = argparse.ArgumentParser(description="龍魂 · AnimateDiff 真实动态镜头生成")
    parser.add_argument("--image", required=True, help="输入图片路径")
    parser.add_argument("--prompt", default="", help="运动/内容提示词")
    parser.add_argument("--negative", default="blurry, low quality, distorted face, watermark", help="负面提示词")
    parser.add_argument("--duration", type=int, default=3, help="目标时长（秒），影响帧数")
    parser.add_argument("--fps", type=int, default=8, help="帧率")
    parser.add_argument("--shot", default="SHOT", help="镜头编码")
    args = parser.parse_args()

    generate(
        image_path=Path(args.image),
        prompt=args.prompt,
        negative_prompt=args.negative,
        duration_sec=args.duration,
        shot_code=args.shot,
        fps=args.fps
    )


if __name__ == "__main__":
    main()
