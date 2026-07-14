#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂一键部署 · 图标与徽章生成器
生成 VS Code 扩展图标和 shields.io 风格徽章
DNA: #龍芯⚡️丙午·辛未·ONE-CLICK-DEPLOY-ART-v1.0
"""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "images"
OUT_DIR.mkdir(exist_ok=True)

# 龍魂色板
COLORS = {
    "bg": "#0a0514",          # 深紫黑背景
    "bg_card": "#1a0b2e",     # 卡片背景
    "gold": "#d4af37",        # 龍魂金
    "gold_light": "#f0d878",  # 亮金
    "red": "#c41e3a",         # 中国红
    "red_dark": "#8a1428",    # 暗红
    "text": "#e2e8f0",        # 主文字
    "dim": "#94a3b8",         # 次要文字
    "green": "#22c55e",       # 通过绿
    "blue": "#3b82f6",        # 信息蓝
}


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    x1, y1, x2, y2 = xy
    r = radius
    draw.pieslice([x1, y1, x1 + r * 2, y1 + r * 2], 180, 270, fill=fill)
    draw.pieslice([x2 - r * 2, y1, x2, y1 + r * 2], 270, 360, fill=fill)
    draw.pieslice([x1, y2 - r * 2, x1 + r * 2, y2], 90, 180, fill=fill)
    draw.pieslice([x2 - r * 2, y2 - r * 2, x2, y2], 0, 90, fill=fill)
    draw.rectangle([x1 + r, y1, x2 - r, y2], fill=fill)
    draw.rectangle([x1, y1 + r, x2, y2 - r], fill=fill)
    if outline:
        draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, outline=outline, width=width)


def make_icon(size=128, radius=22):
    """生成扩展主图标 PNG"""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    bg = hex_to_rgb(COLORS["bg"])
    # 背景：圆角矩形 + 微妙渐变
    draw_rounded_rect(draw, (0, 0, size, size), radius, fill=bg)
    # 内发光/渐变层
    for i in range(size // 2, 0, -2):
        alpha = int(12 - i * 12 / (size // 2))
        if alpha < 0:
            alpha = 0
        draw.ellipse(
            [size//2 - i, size//2 - i, size//2 + i, size//2 + i],
            outline=(212, 175, 55, alpha),
            width=1,
        )

    # 外圈金环
    cx, cy = size // 2, size // 2
    ring_r = size * 0.42
    draw.ellipse([cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r],
                 outline=hex_to_rgb(COLORS["gold"]), width=3)
    draw.ellipse([cx - ring_r + 4, cy - ring_r + 4, cx + ring_r - 4, cy + ring_r - 4],
                 outline=hex_to_rgb(COLORS["gold_light"]), width=1)

    # 尝试加载字体：优先用系统字体
    font_candidates = [
        "/System/Library/Fonts/PingFang.ttc",             # macOS 苹方
        "/System/Library/Fonts/STHeiti Light.ttc",        # macOS 黑体
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",   # Linux
        "C:/Windows/Fonts/simhei.ttf",                     # Windows 黑体
        "C:/Windows/Fonts/simsun.ttc",                     # Windows 宋体
    ]
    font_path = None
    for f in font_candidates:
        if os.path.exists(f):
            font_path = f
            break

    if font_path:
        font_big = ImageFont.truetype(font_path, int(size * 0.55))
        font_small = ImageFont.truetype(font_path, int(size * 0.16))
    else:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # 中心大字：龍
    text = "龍"
    bbox = draw.textbbox((0, 0), text, font=font_big)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = cx - tw // 2 - bbox[0]
    ty = cy - th // 2 - bbox[1] - size * 0.05
    # 文字阴影
    draw.text((tx + 2, ty + 2), text, font=font_big, fill=hex_to_rgb(COLORS["red_dark"]))
    draw.text((tx, ty), text, font=font_big, fill=hex_to_rgb(COLORS["gold"]))

    # 底部 UID
    uid_text = "9622"
    bbox2 = draw.textbbox((0, 0), uid_text, font=font_small)
    tw2, th2 = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
    draw.text((cx - tw2 // 2 - bbox2[0], int(size * 0.78)),
              uid_text, font=font_small, fill=hex_to_rgb(COLORS["gold_light"]))

    # 右上角小火箭箭头（部署意象）
    arrow_size = size * 0.18
    arrow_top = (int(size * 0.75), int(size * 0.22))
    arrow_left = (int(size * 0.65), int(size * 0.38))
    arrow_right = (int(size * 0.85), int(size * 0.38))
    draw.polygon([arrow_top, arrow_left, arrow_right], fill=hex_to_rgb(COLORS["red"]))
    # 火箭尾焰
    draw.polygon([
        (int(size * 0.70), int(size * 0.38)),
        (int(size * 0.80), int(size * 0.38)),
        (int(size * 0.75), int(size * 0.48)),
    ], fill=hex_to_rgb(COLORS["gold_light"]))

    return img


def make_badge(text_left, text_right, left_color, right_color, filename, height=32):
    """生成 shields.io 风格本地徽章 PNG"""
    # 估算宽度（每个中文字符约16px，英文8px，padding）
    left_px = len(text_left) * (10 if any(ord(c) > 127 for c in text_left) else 7) + 16
    right_px = len(text_right) * (10 if any(ord(c) > 127 for c in text_right) else 7) + 16
    total_w = left_px + right_px
    total_h = height

    img = Image.new("RGBA", (total_w, total_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    radius = 4
    # 左半
    draw_rounded_rect(draw, (0, 0, left_px, total_h), radius, fill=left_color)
    # 右半（覆盖左边圆角，通过矩形覆盖实现）
    draw.rectangle([left_px - radius, 0, total_w, total_h], fill=right_color)
    draw.pieslice([total_w - radius*2, 0, total_w, radius*2], 270, 360, fill=right_color)
    draw.pieslice([total_w - radius*2, total_h - radius*2, total_w, total_h], 0, 90, fill=right_color)
    # 中线
    draw.line([(left_px, 0), (left_px, total_h)], fill=hex_to_rgb("#0a0514"), width=1)

    # 字体
    font_candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "C:/Windows/Fonts/simhei.ttf",
    ]
    font_path = next((f for f in font_candidates if os.path.exists(f)), None)
    font = ImageFont.truetype(font_path, 12) if font_path else ImageFont.load_default()

    def draw_centered(text, x, w, color):
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((x + (w - tw) // 2 - bbox[0], (total_h - th) // 2 - bbox[1]),
                  text, font=font, fill=color)

    draw_centered(text_left, 0, left_px, "white")
    draw_centered(text_right, left_px, right_px, "white")

    img.save(OUT_DIR / filename)
    return img


def main():
    # 主图标
    icon = make_icon(128)
    icon.save(OUT_DIR / "icon.png")
    print(f"[OK] icon.png -> {OUT_DIR / 'icon.png'}")

    # 生成 SVG 矢量版（便于后续缩放）
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="128" height="128" viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{COLORS['bg']}"/>
      <stop offset="100%" stop-color="{COLORS['bg_card']}"/>
    </linearGradient>
  </defs>
  <rect width="128" height="128" rx="22" fill="url(#bg)"/>
  <circle cx="64" cy="64" r="54" fill="none" stroke="{COLORS['gold']}" stroke-width="3"/>
  <circle cx="64" cy="64" r="50" fill="none" stroke="{COLORS['gold_light']}" stroke-width="1"/>
  <text x="64" y="78" font-family="serif, 'Songti SC', 'SimSun', sans-serif" font-size="70" font-weight="bold" text-anchor="middle" fill="{COLORS['gold']}">龍</text>
  <text x="66" y="80" font-family="serif, 'Songti SC', 'SimSun', sans-serif" font-size="70" font-weight="bold" text-anchor="middle" fill="{COLORS['red_dark']}" opacity="0.4">龍</text>
  <text x="64" y="108" font-family="monospace" font-size="12" text-anchor="middle" fill="{COLORS['gold_light']}">9622</text>
  <polygon points="96,28 104,44 100,44 100,52 92,52 92,44 88,44" fill="{COLORS['red']}"/>
  <polygon points="92,52 100,52 96,62" fill="{COLORS['gold_light']}"/>
</svg>
'''
    (OUT_DIR / "icon.svg").write_text(svg_content, encoding="utf-8")
    print(f"[OK] icon.svg -> {OUT_DIR / 'icon.svg'}")

    # 本地徽章
    make_badge("龍魂", "v1.0.0", COLORS["bg_card"], COLORS["gold"], "badge-version.png")
    make_badge("License", "CC-BY-NC-SA-4.0", COLORS["bg_card"], COLORS["green"], "badge-license.png")
    make_badge("GPG", "A2D0...6D5F", COLORS["bg_card"], COLORS["red"], "badge-gpg.png")
    make_badge("Platform", "GitHub·Gitee·华为云", COLORS["bg_card"], COLORS["blue"], "badge-platform.png")
    make_badge("Contributors", "Welcome", COLORS["bg_card"], COLORS["green"], "badge-contributors.png")
    make_badge("Made with", "❤️ 中国", COLORS["bg_card"], COLORS["red"], "badge-made-in-china.png")
    print("[OK] 所有徽章已生成")


if __name__ == "__main__":
    main()
