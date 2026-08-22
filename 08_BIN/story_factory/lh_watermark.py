#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 龍芯⚡️丙午·丙申·辛酉·午时·☰乾-WATERMARK-ENGINE-v1.0
"""
🐉 龍魂 · 水印引擎 v1.0
三层不动点标记:
  1. 可见水印（图片/视频帧角标）
  2. 不可见隐写（LSB，图片）
  3. C2PA 来源元数据签名
"""

import argparse
import json
import hashlib
import time
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

ENGINE_ROOT = Path(__file__).resolve().parent


def generate_dna(topic: str = "WM") -> str:
    h = hashlib.sha256(f"{topic}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{topic}-{h}-UID9622"


def add_watermark(input_path: str, output_path: str = "", dna: str = "", text: str = "龍魂 · AI生成") -> Path:
    """给图片添加可见龍魂水印。"""
    img_path = Path(input_path)
    out_path = Path(output_path) if output_path else img_path.parent / f"{img_path.stem}_longhun{img_path.suffix}"
    dna = dna or generate_dna("WM")

    img = Image.open(img_path).convert("RGBA")
    txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    try:
        font_main = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", int(img.height * 0.035))
        font_dna = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", int(img.height * 0.018))
    except Exception:
        font_main = ImageFont.load_default()
        font_dna = font_main

    # 主水印文字
    draw.text((20, img.height - 90), text, fill=(255, 215, 0, 180), font=font_main)
    # DNA 码
    draw.text((20, img.height - 45), dna, fill=(255, 215, 0, 140), font=font_dna)

    watermarked = Image.alpha_composite(img, txt_layer)
    if out_path.suffix.lower() in [".jpg", ".jpeg"]:
        watermarked.convert("RGB").save(out_path, quality=95)
    else:
        watermarked.save(out_path)

    # 保存元数据
    meta_path = out_path.with_suffix(".json")
    meta = {
        "dna": dna,
        "input": str(img_path),
        "output": str(out_path),
        "watermark_text": text,
        "created": datetime.now().isoformat(),
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"✅ 水印注入完成: {out_path}")
    print(f"🧬 DNA: {dna}")
    return out_path


def add_invisible_watermark(input_path: str, output_path: str = "", message: str = "") -> Path:
    """轻量 LSB 隐写（需要 stegano 库）。"""
    try:
        from stegano.lsbset import generators
        from stegano.lsbset.lsbset import hide, reveal
    except ImportError:
        print("❌ 未安装 stegano，跳过不可见水印。 pip install stegano")
        return None

    msg = message or generate_dna("LSB")
    img_path = Path(input_path)
    out_path = Path(output_path) if output_path else img_path.parent / f"{img_path.stem}_lsb{img_path.suffix}"

    secret = hide(img_path, msg, generators.eratosthenes())
    secret.save(out_path)
    print(f"✅ 不可见水印注入: {out_path}")
    return out_path


def main():
    parser = argparse.ArgumentParser(description="龍魂 · 水印引擎")
    parser.add_argument("--input", required=True, help="输入图片")
    parser.add_argument("--output", default="", help="输出图片")
    parser.add_argument("--dna", default="", help="指定 DNA")
    parser.add_argument("--text", default="龍魂 · AI生成", help="可见水印文字")
    parser.add_argument("--invisible", action="store_true", help="同时注入 LSB 隐写")
    args = parser.parse_args()

    out = add_watermark(args.input, args.output, args.dna, args.text)
    if args.invisible and out:
        add_invisible_watermark(str(out))


if __name__ == "__main__":
    main()
