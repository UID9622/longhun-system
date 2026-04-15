#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂视频自动生成引擎 v1.0
DNA: #龍芯⚡️2026-04-03-VIDEO-GEN-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导：曾仕强老师（永恒显示）
作者：UID9622 诸葛鑫（龍芯北辰）
献礼：新中国成立77周年（1949-2026）· 丙午马年

职责：
  1. 读脚本 → 拆场景
  2. 每场景自动配风格 → 生成 ComfyUI prompt
  3. 调用 ComfyUI API 跑图
  4. 图 + 音频 → moviepy 合成 mp4
  5. 吐出成品，老大什么都不用管
"""

import json, os, sys, time, shutil, urllib.request, urllib.error
from pathlib import Path

# ── 路径配置 ───────────────────────────────────────
BASE       = Path.home() / "longhun-system"
COMFYUI    = Path.home() / "ComfyUI"
OUTPUT_DIR = BASE / "video_output"
TEMP_DIR   = BASE / "video_output" / "temp"
COMFY_URL  = "http://127.0.0.1:8188"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# ── 风格库（自动按场景匹配） ────────────────────────
STYLES = {
    "开场": {
        "desc": "墨底金字，极简，中国水墨，黑白对比",
        "prompt": "ink wash painting, black background, single chinese character, minimalist, dramatic lighting, 4k",
        "negative": "colorful, busy, western, photorealistic",
        "bg_color": (10, 10, 10),
        "text_color": (196, 26, 13),
    },
    "身份": {
        "desc": "军队剪影，山河壮阔，水墨风",
        "prompt": "silhouette of soldier, vast mountain landscape, ink wash style, dramatic, chinese painting, black and deep blue",
        "negative": "colorful, cartoon, anime",
        "bg_color": (8, 12, 20),
        "text_color": (200, 180, 140),
    },
    "为什么": {
        "desc": "五行符号，数字流动，神秘感",
        "prompt": "flowing numbers and chinese symbols, five elements, dark background, glowing particles, mystical, digital art",
        "negative": "bright, cartoon",
        "bg_color": (5, 5, 15),
        "text_color": (120, 180, 255),
    },
    "核心": {
        "desc": "朱砂红印记，龍字，强烈视觉冲击",
        "prompt": "chinese seal stamp, red cinnabar, dragon character, black background, powerful, traditional chinese art",
        "negative": "soft, pastel, western",
        "bg_color": (15, 5, 5),
        "text_color": (196, 26, 13),
    },
    "收尾": {
        "desc": "极简黑底白字，留白，禅意",
        "prompt": "minimal, black background, white space, zen, single element, peaceful",
        "negative": "busy, colorful, dramatic",
        "bg_color": (8, 8, 8),
        "text_color": (220, 215, 205),
    },
}

# ── 脚本定义（从 script_龍魂起源.html 提炼） ────────
SCRIPT_SCENES = [
    {
        "id": "开场",
        "style": "开场",
        "duration": 8,   # 秒
        "lines": ["我退伍那年，没有任何计划。", "就是觉得这个世界越来越快，但说人话的越来越少。"],
    },
    {
        "id": "身份",
        "style": "身份",
        "duration": 10,
        "lines": ["我不是程序员。我是当兵的。", "当兵教会我一件事——", "系统不对，再努力也白搭。"],
    },
    {
        "id": "为什么",
        "style": "为什么",
        "duration": 12,
        "lines": ["曾仕强老师讲过，中国人做事，讲的是天时地利人和。", "我就想，这套东西能不能装进一个系统？", "不是算命。是算势。"],
    },
    {
        "id": "核心",
        "style": "核心",
        "duration": 15,
        "lines": ["现在的AI，都在替你做决定。", "替你推荐，替你筛选，替你思考。", "你的脑子，慢慢就借出去了。",
                  "龍魂系统，我想做的，是反过来的事。", "让系统为你服务，而不是把你变成系统的燃料。"],
    },
    {
        "id": "收尾",
        "style": "收尾",
        "duration": 10,
        "lines": ["我没有很大的野心。", "就是想做一个普通人也能用得上的东西。", "祖国优先。普惠全球。技术为人民服务。", "就这样。"],
    },
]

# ── ComfyUI 可用性检测 ──────────────────────────────
def comfyui_online() -> bool:
    try:
        urllib.request.urlopen(f"{COMFY_URL}/system_stats", timeout=3)
        return True
    except Exception:
        return False

# ── 用 ComfyUI API 生成图片 ─────────────────────────
def gen_image_comfyui(prompt: str, negative: str, scene_id: str) -> Path | None:
    """调用 ComfyUI API (prompt queue) 生成一张图，返回本地路径"""
    workflow = {
        "3": {
            "class_type": "KSampler",
            "inputs": {
                "cfg": 7,
                "denoise": 1,
                "latent_image": ["5", 0],
                "model": ["4", 0],
                "negative": ["7", 0],
                "positive": ["6", 0],
                "sampler_name": "euler",
                "scheduler": "normal",
                "seed": int(time.time()) % 99999,
                "steps": 20,
            },
        },
        "4": {"class_type": "CheckpointLoaderSimple",
              "inputs": {"ckpt_name": _find_checkpoint()}},
        "5": {"class_type": "EmptyLatentImage",
              "inputs": {"batch_size": 1, "height": 768, "width": 1344}},
        "6": {"class_type": "CLIPTextEncode",
              "inputs": {"clip": ["4", 1], "text": prompt}},
        "7": {"class_type": "CLIPTextEncode",
              "inputs": {"clip": ["4", 1], "text": negative}},
        "8": {"class_type": "VAEDecode",
              "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
        "9": {"class_type": "SaveImage",
              "inputs": {"filename_prefix": f"longhun_{scene_id}", "images": ["8", 0]}},
    }

    payload = json.dumps({"prompt": workflow}).encode()
    req = urllib.request.Request(
        f"{COMFY_URL}/prompt", data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            prompt_id = result.get("prompt_id")
    except Exception as e:
        print(f"  ⚠️ ComfyUI 请求失败: {e}")
        return None

    # 轮询等待完成（最多120秒）
    print(f"  🎨 ComfyUI 生成中 ({scene_id})...", end="", flush=True)
    for _ in range(60):
        time.sleep(2)
        try:
            with urllib.request.urlopen(f"{COMFY_URL}/history/{prompt_id}", timeout=5) as r:
                hist = json.loads(r.read())
                if prompt_id in hist:
                    outputs = hist[prompt_id].get("outputs", {})
                    for node_out in outputs.values():
                        images = node_out.get("images", [])
                        if images:
                            img_info = images[0]
                            img_url = f"{COMFY_URL}/view?filename={img_info['filename']}&type=output"
                            out_path = TEMP_DIR / f"{scene_id}.png"
                            urllib.request.urlretrieve(img_url, out_path)
                            print(" ✅")
                            return out_path
        except Exception:
            pass
        print(".", end="", flush=True)
    print(" ⏱️ 超时")
    return None

def _find_checkpoint() -> str:
    ckpt_dir = COMFYUI / "models" / "checkpoints"
    if ckpt_dir.exists():
        files = list(ckpt_dir.glob("*.safetensors")) + list(ckpt_dir.glob("*.ckpt"))
        if files:
            return files[0].name
    return "v1-5-pruned-emaonly.ckpt"

# ── 纯色+文字备用帧（ComfyUI 不在线时） ───────────
def gen_image_fallback(scene: dict) -> Path:
    """用 Pillow 生成纯色背景+台词文字的备用帧"""
    from PIL import Image, ImageDraw, ImageFont

    style = STYLES[scene["style"]]
    bg    = style["bg_color"]
    fg    = style["text_color"]
    W, H  = 1344, 768

    img  = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(img)

    # 尝试加载系统中文字体
    font_paths = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Supplemental/Songti.ttc",
    ]
    font_large = font_small = None
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                font_large = ImageFont.truetype(fp, 52)
                font_small = ImageFont.truetype(fp, 28)
                break
            except Exception:
                pass
    if not font_large:
        font_large = font_small = ImageFont.load_default()

    # 场景标题
    draw.text((80, 60), scene["id"], font=font_small, fill=(80, 80, 80))

    # 台词居中
    lines = scene["lines"]
    y = H // 2 - (len(lines) * 70) // 2
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_large)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2, y), line, font=font_large, fill=fg)
        y += 75

    # 朱砂红底部装饰线
    draw.rectangle([(0, H - 4), (W, H)], fill=(196, 26, 13))

    out_path = TEMP_DIR / f"{scene['id']}_fallback.png"
    img.save(out_path)
    return out_path

# ── moviepy 合成 ────────────────────────────────────
def compose_video(scenes: list, img_paths: list, audio_path: str | None, out_name: str):
    from moviepy import ImageClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip

    clips = []
    for scene, img_path in zip(scenes, img_paths):
        if img_path and img_path.exists():
            clip = ImageClip(str(img_path)).with_duration(scene["duration"])
            clips.append(clip)
        else:
            print(f"  ⚠️ {scene['id']} 图片缺失，跳过")

    if not clips:
        print("❌ 没有可用素材，合成失败")
        return

    video = concatenate_videoclips(clips, method="compose")

    # 如果有配音
    if audio_path and os.path.exists(audio_path):
        audio = AudioFileClip(audio_path)
        # 音频比视频长就截断，短就用视频时长
        if audio.duration < video.duration:
            video = video.with_duration(audio.duration)
        else:
            audio = audio.subclipped(0, video.duration)
        video = video.with_audio(audio)

    out_path = OUTPUT_DIR / out_name
    video.write_videofile(
        str(out_path),
        fps=24,
        codec="libx264",
        audio_codec="aac",
        logger=None,
    )
    print(f"\n✅ 视频已生成: {out_path}")
    os.system(f'open "{out_path}"')

# ── 主入口 ──────────────────────────────────────────
def main():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  🎬 龍魂视频生成引擎 v1.0")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    audio_path = None
    # 检查是否有配音文件
    for ext in ["m4a", "mp3", "wav", "aac"]:
        candidate = BASE / f"voice_龍魂起源.{ext}"
        if candidate.exists():
            audio_path = str(candidate)
            print(f"  🎤 检测到配音: {candidate.name}")
            break
    if not audio_path:
        print("  🎤 未找到配音文件（放到 longhun-system/voice_龍魂起源.m4a 即可）")
        print("     → 先生成无声版，录完音再合成")

    # 检查 ComfyUI
    use_comfy = comfyui_online()
    if use_comfy:
        print("  🎨 ComfyUI 在线 → 使用 AI 生图")
    else:
        print("  🎨 ComfyUI 离线 → 使用文字备用帧")

    # 逐场景生成素材
    img_paths = []
    for scene in SCRIPT_SCENES:
        style = STYLES[scene["style"]]
        print(f"\n  📽️  场景: {scene['id']} ({scene['duration']}s) · 风格: {style['desc']}")

        if use_comfy:
            img = gen_image_comfyui(style["prompt"], style["negative"], scene["id"])
            if not img:
                print("     ↩️ ComfyUI 失败，降级用备用帧")
                img = gen_image_fallback(scene)
        else:
            img = gen_image_fallback(scene)

        img_paths.append(img)

    # 合成视频
    print("\n  🎞️  合成中...")
    ts = time.strftime("%Y%m%d_%H%M%S")
    compose_video(SCRIPT_SCENES, img_paths, audio_path, f"龍魂起源_{ts}.mp4")

    print(f"\n  DNA: #龍芯⚡️{ts}-VIDEO-龍魂起源-v1.0")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

if __name__ == "__main__":
    main()
