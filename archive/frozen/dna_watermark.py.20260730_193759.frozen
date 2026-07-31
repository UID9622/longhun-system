#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-DNA_WATERMARK-v1.0-e90c2e75
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂·DNA图片水印工具
依赖: Pillow (仅此库，环境已装)
功能: 给图片加半透明龍魂DNA追溯码水印，保留原作者信息可选。

用法:
    python3 dna_watermark.py <input_image> <output_image> [--dna "DNA码"] [--author "原作者"]
"""
import sys
import argparse
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

DEFAULT_DNA = "#ZHUGEXIN⚡️" + datetime.now().strftime("%Y-%m-%d") + "-IMAGE-001"

def load_font(size):
    """加载系统中文字体，失败回退默认。"""
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for c in candidates:
        try:
            return ImageFont.truetype(c, size)
        except Exception:
            continue
    return ImageFont.load_default()

def add_dna_watermark(input_path, output_path, dna_code, author=None):
    img = Image.open(input_path).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # 水印文字
    lines = [f"🐉 {dna_code} | UID9622"]
    if author:
        lines.append(f"原图: {author}")
    text = "  ·  ".join(lines)

    # 字号随图宽自适应
    font_size = max(16, int(img.width / 45))
    font = load_font(font_size)

    # 测量文本宽度（兼容旧版PIL无getlength）
    try:
        tw = int(draw.getlength(text, font=font))
    except Exception:
        tw = len(text) * font_size

    margin = 12
    x = margin
    y = img.height - font_size - margin

    # 半透明黑底衬托，保证任意背景可读
    draw.rectangle([x - 6, y - 4, x + tw + 6, y + font_size + 4], fill=(0, 0, 0, 110))
    # 白字半透明
    draw.text((x, y), text, fill=(255, 255, 255, 170), font=font)

    img.convert("RGB").save(output_path)
    return f"已添加DNA水印: {output_path}"

def main():
    ap = argparse.ArgumentParser(description="龍魂DNA图片水印")
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--dna", default=DEFAULT_DNA)
    ap.add_argument("--author", default=None, help="原图作者/来源(保留署名)")
    args = ap.parse_args()
    print(add_dna_watermark(args.input, args.output, args.dna, args.author))

if __name__ == "__main__":
    main()
