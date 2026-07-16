#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂视觉生成引擎 v1.0
不依赖外部素材，用中国古典数理（河图洛书、八卦、五行）生成纹样、色彩与图腾。
DNA: #龍芯⚡️2026-06-27-LONGHUN-VISUAL-ENGINE-v1.0
"""
import argparse
import math
import random
from pathlib import Path
from typing import Dict, List, Tuple


# 五行色板
WUXING = {
    "金": {"color": "#f0c674", "emotion": "权威", "element": "metal"},
    "木": {"color": "#3c8d7d", "emotion": "生机", "element": "wood"},
    "水": {"color": "#0a0908", "emotion": "深邃", "element": "water"},
    "火": {"color": "#c23a30", "emotion": "警示", "element": "fire"},
    "土": {"color": "#b87333", "emotion": "稳重", "element": "earth"},
}


def wuxing_palette(seed: str = None) -> Dict[str, str]:
    """根据可选 seed 返回五行主色。"""
    if seed:
        random.seed(seed)
    keys = list(WUXING.keys())
    dominant = random.choice(keys)
    return {
        "dominant": WUXING[dominant]["color"],
        "accent": WUXING[random.choice(keys)]["color"],
        "bg": WUXING["水"]["color"],
        "text": "#f5f0e6",
        "grid": "#4a3b2a",
    }


def _path_from_points(points: List[Tuple[float, float]], close: bool = False) -> str:
    if not points:
        return ""
    d = f"M {points[0][0]} {points[0][1]}"
    for x, y in points[1:]:
        d += f" L {x} {y}"
    if close:
        d += " Z"
    return d


def meander_svg(width: int = 200, height: int = 200, stroke: str = "#b87333", bg: str = "#0a0908", step: int = 20) -> str:
    """生成云雷纹（回纹）SVG 图案。"""
    lines = []
    for y in range(0, height, step * 2):
        for x in range(0, width, step * 2):
            pts = [
                (x, y + step),
                (x + step, y + step),
                (x + step, y + step * 2),
                (x + step * 2, y + step * 2),
            ]
            lines.append(f'<path d="{_path_from_points(pts)}" fill="none" stroke="{stroke}" stroke-width="1.5" opacity="0.6"/>')
    pattern = "\n    ".join(lines)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">
  <rect width="{width}" height="{height}" fill="{bg}"/>
  {pattern}
</svg>'''


def dragon_seal_svg(size: int = 120, stroke: str = "#f0c674", bg: str = "#0a0908") -> str:
    """用参数方程生成抽象龙纹印章 SVG。"""
    cx, cy = size / 2, size / 2
    points = []
    n = 120
    for i in range(n + 1):
        t = i / n * 4 * math.pi
        r = size * 0.38 + size * 0.12 * math.sin(3 * t) + size * 0.06 * math.sin(7 * t)
        x = cx + r * math.cos(t + math.pi / 6)
        y = cy + r * math.sin(t + math.pi / 6) * 0.55
        points.append((x, y))
    body = _path_from_points(points)

    # 龙睛
    eye_r = size * 0.04
    eye1 = (cx + size * 0.12, cy - size * 0.08)
    eye2 = (cx + size * 0.22, cy - size * 0.12)
    eyes = (
        f'<circle cx="{eye1[0]}" cy="{eye1[1]}" r="{eye_r}" fill="{stroke}"/>'
        f'<circle cx="{eye2[0]}" cy="{eye2[1]}" r="{eye_r}" fill="{stroke}"/>'
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">
  <rect width="{size}" height="{size}" fill="{bg}" rx="{size*0.1}"/>
  <path d="{body}" fill="none" stroke="{stroke}" stroke-width="{size*0.025}" stroke-linecap="round"/>
  {eyes}
  <text x="{cx}" y="{size*0.88}" text-anchor="middle" font-size="{size*0.22}" fill="{stroke}" font-family="serif">龍</text>
</svg>'''


def bagua_ring_svg(size: int = 160, stroke: str = "#b87333", bg: str = "#0a0908") -> str:
    """生成八卦方位环 SVG。"""
    cx, cy = size / 2, size / 2
    r = size * 0.35
    trigrams = ["☰", "☱", "☲", "☳", "☴", "☵", "☶", "☷"]
    elements = []
    for i, tri in enumerate(trigrams):
        angle = i * (2 * math.pi / 8) - math.pi / 2
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        elements.append(f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" font-size="{size*0.14}" fill="{stroke}" opacity="0.85">{tri}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">
  <rect width="{size}" height="{size}" fill="{bg}"/>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{stroke}" stroke-width="{size*0.015}" opacity="0.5"/>
  {''.join(elements)}
</svg>'''


def pan_chi_svg(size: int = 200, stroke: str = "#b87333", bg: str = "#0a0908") -> str:
    """生成蟠螭纹：螺旋盘绕的抽象龙形。"""
    cx, cy = size / 2, size / 2
    points = []
    n = 200
    for i in range(n + 1):
        t = i / n * 6 * math.pi
        a = size * 0.06
        b = size * 0.018
        r = a + b * t
        x = cx + r * math.cos(t)
        y = cy + r * math.sin(t) * 0.6
        points.append((x, y))
    body = _path_from_points(points)

    # 龙头
    head_idx = int(n * 0.95)
    hx, hy = points[head_idx]
    head = (
        f'<circle cx="{hx}" cy="{hy}" r="{size*0.035}" fill="none" stroke="{stroke}" stroke-width="{size*0.012}"/>'
        f'<circle cx="{hx-size*0.01}" cy="{hy-size*0.01}" r="{size*0.008}" fill="{stroke}"/>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">
  <rect width="{size}" height="{size}" fill="{bg}"/>
  <path d="{body}" fill="none" stroke="{stroke}" stroke-width="{size*0.01}" stroke-linecap="round" opacity="0.85"/>
  {head}
</svg>'''


def dragon_scale_svg(width: int = 200, height: int = 200, stroke: str = "#b87333", bg: str = "#0a0908") -> str:
    """生成龙鳞纹：交错排列的半圆鳞片刻画。"""
    rows = 8
    cols = 10
    rh = height / rows
    rw = width / cols
    scales = []
    for row in range(rows):
        y = row * rh
        for col in range(cols):
            x_offset = (rh * 0.5) if (row % 2 == 1) else 0
            x = col * rw + x_offset
            if x + rw > width:
                continue
            scales.append(
                f'<path d="M {x} {y} A {rw*0.5} {rh*0.6} 0 0 1 {x+rw} {y}" '
                f'fill="none" stroke="{stroke}" stroke-width="1.2" opacity="0.5"/>'
            )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="{width}" height="{height}" fill="{bg}"/>
  {''.join(scales)}
</svg>'''


def particle_totem_svg(size: int = 200, stroke: str = "#f0c674", bg: str = "#0a0908") -> str:
    """生成粒子图腾：沿龙形轮廓分布的发光粒子点阵。"""
    cx, cy = size / 2, size / 2
    particles = []
    n = 80
    for i in range(n):
        t = i / n * 4 * math.pi
        r = size * 0.35 + size * 0.1 * math.sin(3 * t) + size * 0.05 * math.sin(7 * t)
        x = cx + r * math.cos(t + math.pi / 6)
        y = cy + r * math.sin(t + math.pi / 6) * 0.55
        opacity = 0.4 + 0.6 * ((i % 7) / 7)
        radius = size * 0.006 + size * 0.004 * ((i % 5) / 5)
        particles.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{stroke}" opacity="{opacity:.2f}"/>')
    # 中心龍字
    center_text = f'<text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="middle" font-size="{size*0.18}" fill="{stroke}" opacity="0.9" font-family="serif">龍</text>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">
  <rect width="{size}" height="{size}" fill="{bg}"/>
  {''.join(particles)}
  {center_text}
</svg>'''


def generate_all_samples(output_dir: Path):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    palette = wuxing_palette(seed="longhun")

    samples = {
        "meander_pattern.svg": meander_svg(200, 200, stroke=palette["dominant"], bg=palette["bg"]),
        "dragon_seal.svg": dragon_seal_svg(120, stroke=palette["accent"], bg=palette["bg"]),
        "bagua_ring.svg": bagua_ring_svg(160, stroke=palette["dominant"], bg=palette["bg"]),
        "pan_chi.svg": pan_chi_svg(200, stroke=palette["accent"], bg=palette["bg"]),
        "dragon_scale.svg": dragon_scale_svg(200, 200, stroke=palette["dominant"], bg=palette["bg"]),
        "particle_totem.svg": particle_totem_svg(200, stroke=palette["accent"], bg=palette["bg"]),
    }
    for name, svg in samples.items():
        (output_dir / name).write_text(svg, encoding="utf-8")
    import json
    (output_dir / "palette.json").write_text(json.dumps(palette, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_dir


def main():
    parser = argparse.ArgumentParser(description="龍魂视觉生成引擎")
    parser.add_argument("--output-dir", default="data/visual_samples", help="样本输出目录")
    parser.add_argument("--seed", default="longhun", help="色彩种子")
    args = parser.parse_args()

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    palette = wuxing_palette(seed=args.seed)

    files = {
        "meander_pattern.svg": meander_svg(200, 200, stroke=palette["dominant"], bg=palette["bg"]),
        "dragon_seal.svg": dragon_seal_svg(120, stroke=palette["accent"], bg=palette["bg"]),
        "bagua_ring.svg": bagua_ring_svg(160, stroke=palette["dominant"], bg=palette["bg"]),
        "pan_chi.svg": pan_chi_svg(200, stroke=palette["accent"], bg=palette["bg"]),
        "dragon_scale.svg": dragon_scale_svg(200, 200, stroke=palette["dominant"], bg=palette["bg"]),
        "particle_totem.svg": particle_totem_svg(200, stroke=palette["accent"], bg=palette["bg"]),
    }
    for name, svg in files.items():
        (out / name).write_text(svg, encoding="utf-8")
        print(f"已生成: {out / name}")

    import json
    (out / "palette.json").write_text(json.dumps(palette, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"色板: {out / 'palette.json'}")
    print("DNA: #龍芯⚡️2026-06-27-LONGHUN-VISUAL-ENGINE-v1.0")


if __name__ == "__main__":
    main()
