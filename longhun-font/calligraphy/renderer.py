# #龍芯⚡️20260624010825157-AUTO-DNA-F43722E7 自动注入·分层治理自愈引擎 · 来源可查
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️2026-06-23-LONGHUN-FONT-RENDERER-v1.0
"""
书法渲染引擎

输入文字 + 选择书法样式 → 输出带印章、龙纹水印、作品编号的高清书法图片。
"""

import json
import math
import random
from pathlib import Path
from typing import Optional

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .work_id import generate_work_id
from .watermark import add_visible_watermark, add_frequency_watermark
from .seal_generator import generate_seal

DNA = "#龍芯⚡️2026-06-23-LONGHUN-FONT-RENDERER-v1.0"

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output" / "calligraphy"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BACKGROUNDS = {
    "宣纸米黄": (245, 240, 230),
    "宣纸本白": (252, 250, 245),
    "仿古宣纸": (232, 222, 202),
    "洒金宣纸": (245, 235, 210),
    "绢本浅黄": (240, 235, 220),
}

# 字元库缓存
_glyph_library = None


def _load_glyph_library():
    global _glyph_library
    if _glyph_library is None:
        lib_path = BASE_DIR / "glyphs" / "龍魂字元库_v0019_龍纹书法版.json"
        with open(lib_path, "r", encoding="utf-8") as f:
            _glyph_library = json.load(f)["字符集_cnsh9622"]
    return _glyph_library


def _load_fallback_font(fallback_path: str, size: int):
    if fallback_path and Path(fallback_path).exists():
        return ImageFont.truetype(fallback_path, size)
    # 通用回退
    candidates = [
        "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/88d6cc32a907955efa1d014207889413890573be.asset/AssetData/Kaiti.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/PingFang.ttc",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    raise RuntimeError("未找到可用中文字体")


def _stroke_line_to_polygon(p1, p2, width):
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1
    length = (dx ** 2 + dy ** 2) ** 0.5
    if length < 1e-6:
        return []
    ux = -dy / length
    uy = dx / length
    hw = width / 2
    return [
        (x1 + ux * hw, y1 + uy * hw),
        (x2 + ux * hw, y2 + uy * hw),
        (x2 - ux * hw, y2 - uy * hw),
        (x1 - ux * hw, y1 - uy * hw),
    ]


def _path_to_contours(strokes, stroke_width):
    """把笔画路径转换为闭合轮廓列表（视图坐标）。"""
    contours = []
    current_point = None
    for s in strokes:
        if not isinstance(s, dict):
            continue
        t = s["类型"]
        if t == "移动到":
            current_point = tuple(s["坐标"])
        elif t == "直线段":
            end = tuple(s["终点"])
            if current_point is None:
                continue
            poly = _stroke_line_to_polygon(current_point, end, stroke_width)
            if poly:
                contours.append(poly)
            current_point = end
        elif t == "三次曲线":
            p1, p2, p3 = [tuple(p) for p in s["控制点"]]
            if current_point is None:
                continue
            poly = _stroke_line_to_polygon(current_point, p3, stroke_width)
            if poly:
                contours.append(poly)
            current_point = p3
    return contours


def _char_bbox(contours):
    xs = [p[0] for c in contours for p in c]
    ys = [p[1] for c in contours for p in c]
    if not xs:
        return (0, 0, 600, 600)
    return (min(xs), min(ys), max(xs), max(ys))


def _render_text_with_fallback(canvas, draw, text, style, layout, font_size):
    """使用系统回退字体 + 样式变换渲染文字。"""
    params = style["parameters"]
    slant = params.get("slant", 0.0)
    randomness = params.get("randomness", 0.02)
    spacing_x = params.get("spacing_x", 1.1)
    spacing_y = params.get("spacing_y", 1.2)
    ink_color = params.get("ink_color", "#1a1a1a")
    fallback_font = style.get("fallback_font")

    font = _load_fallback_font(fallback_font, font_size)
    chars = list(text)
    random.seed(f"{style['code']}-{text}")
    size = canvas.size

    if layout == "horizontal":
        char_data = []
        total_width = 0
        for ch in chars:
            bbox = draw.textbbox((0, 0), ch, font=font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            char_data.append((ch, w, h))
            total_width += int(w * spacing_x)
        x = (size[0] - total_width) // 2
        y_base = size[1] // 2 - font_size // 3
        for ch, w, h in char_data:
            dx = int(random.uniform(-randomness, randomness) * font_size)
            dy = int(random.uniform(-randomness, randomness) * font_size)
            char_img = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
            cd = ImageDraw.Draw(char_img)
            cb = cd.textbbox((0, 0), ch, font=font)
            cd.text((20 - cb[0], 20), ch, font=font, fill=ink_color)
            if abs(slant) > 1e-6:
                char_img = char_img.transform(
                    char_img.size,
                    Image.Transform.AFFINE,
                    (1, slant, -slant * 20, 0, 1, 0),
                    resample=Image.Resampling.BICUBIC,
                )
            canvas.paste(char_img, (x + dx, y_base + dy), char_img)
            x += int(w * spacing_x)
    else:
        char_data = []
        total_height = 0
        for ch in chars:
            bbox = draw.textbbox((0, 0), ch, font=font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            char_data.append((ch, w, h))
            total_height += int(h * spacing_y)
        x_base = size[0] // 2 - font_size // 3
        y = (size[1] - total_height) // 2
        for ch, w, h in char_data:
            dx = int(random.uniform(-randomness, randomness) * font_size)
            dy = int(random.uniform(-randomness, randomness) * font_size)
            char_img = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
            cd = ImageDraw.Draw(char_img)
            cb = cd.textbbox((0, 0), ch, font=font)
            cd.text((20 - cb[0], 20), ch, font=font, fill=ink_color)
            if abs(slant) > 1e-6:
                char_img = char_img.transform(
                    char_img.size,
                    Image.Transform.AFFINE,
                    (1, 0, 0, slant, 1, -slant * 20),
                    resample=Image.Resampling.BICUBIC,
                )
            canvas.paste(char_img, (x_base + dx, y + dy), char_img)
            y += int(h * spacing_y)


def _draw_char(canvas, draw, contours, ink_color, x, y, scale, slant):
    """在画布上绘制一个字符轮廓。"""
    if not contours:
        # 缺字：画占位方框
        draw.rectangle([x, y, x + int(600 * scale), y + int(600 * scale)],
                       outline=ink_color, width=2)
        return

    # 计算字框以便居中
    bb = _char_bbox(contours)
    cx = (bb[0] + bb[2]) / 2
    cy = (bb[1] + bb[3]) / 2

    for contour in contours:
        pts = []
        for px, py in contour:
            # 居中后缩放
            sx = (px - cx) * scale
            sy = (py - cy) * scale
            # 斜切
            sx += slant * sy
            pts.append((x + sx, y + sy))
        if len(pts) >= 3:
            draw.polygon(pts, fill=ink_color)


def load_style(style_code: str) -> dict:
    """加载书法样式配置。"""
    styles_dir = Path(__file__).parent / "styles"
    for p in styles_dir.glob("*.json"):
        with open(p, "r", encoding="utf-8") as f:
            style = json.load(f)
            if style.get("code") == style_code or p.stem == style_code:
                return style
    raise ValueError(f"未找到书法样式: {style_code}")


def list_styles() -> list:
    """列出所有可用样式。"""
    styles = []
    styles_dir = Path(__file__).parent / "styles"
    for p in sorted(styles_dir.glob("*.json")):
        with open(p, "r", encoding="utf-8") as f:
            style = json.load(f)
            styles.append({
                "code": style["code"],
                "name": style["name"],
                "category": style["category"],
                "era": style["era"],
            })
    return styles


def _background(name: str, size: tuple) -> Image.Image:
    color = BACKGROUNDS.get(name, (245, 240, 230))
    img = Image.new("RGB", size, color)
    # 轻微纹理：随机噪点模拟宣纸纤维
    arr = np.array(img, dtype=np.uint8)
    noise = np.random.randint(-3, 4, arr.shape, dtype=np.int16)
    arr = np.clip(arr.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, "RGB")


def render(text: str, style_code: str = "YZQ-KA",
           layout: str = "horizontal", seal_text: Optional[str] = None,
           classic: str = "GENERAL", output_name: Optional[str] = None,
           size: Optional[tuple] = None,
           font_size: Optional[int] = None) -> dict:
    """
    渲染书法作品。

    Args:
        text: 正文内容
        style_code: 样式代码
        layout: horizontal | vertical
        seal_text: 印章文字，默认无
        classic: 典籍代码，用于作品编号
        output_name: 输出文件名（不含扩展名）
        size: 画布尺寸 (宽, 高)，默认自动
        font_size: 强制字号，覆盖样式默认值
    """
    style = load_style(style_code)
    params = style["parameters"]

    font_size = font_size or params.get("font_size", 220)
    slant = params.get("slant", 0.0)
    randomness = params.get("randomness", 0.02)
    spacing_x = params.get("spacing_x", 1.1)
    spacing_y = params.get("spacing_y", 1.2)
    ink_color = params.get("ink_color", "#1a1a1a")
    bg_name = params.get("background", "宣纸米黄")
    stroke_width = params.get("stroke_width", 24)

    chars = list(text)
    random.seed(f"{style_code}-{text}")  # 可复现的随机

    # 加载字元库
    glyph_lib = _load_glyph_library()

    # 预计算每个字符的轮廓与字框
    char_contours = []
    cell_size = 600  # 字元库视图框
    for ch in chars:
        if ch not in glyph_lib:
            char_contours.append(None)
            continue
        strokes = glyph_lib[ch]["笔画路径_cnsh9622"]
        contours = _path_to_contours(strokes, stroke_width)
        char_contours.append(contours)

    # 自动画布
    if size is None:
        char_count = len(text)
        if layout == "horizontal":
            width = max(800, int(char_count * font_size * spacing_x * 1.2))
            height = int(font_size * spacing_y * 1.8)
        else:
            width = int(font_size * spacing_x * 1.6)
            height = max(800, int(char_count * font_size * spacing_y * 1.2))
        size = (width, height)

    canvas = _background(bg_name, size)
    draw = ImageDraw.Draw(canvas)

    # 优先使用回退系统字体（当前 LonghunFont 骨架仍为占位方块）
    if style.get("fallback_font"):
        _render_text_with_fallback(canvas, draw, text, style, layout, font_size)
    else:
        # 字符缩放比例
        scale = font_size / cell_size

        # 计算排版尺寸
        char_bboxes = []
        for contours in char_contours:
            if contours:
                bb = _char_bbox(contours)
                char_bboxes.append((bb[2] - bb[0], bb[3] - bb[1]))
            else:
                char_bboxes.append((cell_size, cell_size))

        if layout == "horizontal":
            total_width = sum(int(w * spacing_x * scale) for w, _ in char_bboxes)
            x_cursor = (size[0] - total_width) // 2
            y_base = size[1] // 2 - int(font_size * 0.45)
            for ch, contours, (cw, ch_h) in zip(chars, char_contours, char_bboxes):
                dx = int(random.uniform(-randomness, randomness) * font_size)
                dy = int(random.uniform(-randomness, randomness) * font_size)
                _draw_char(canvas, draw, contours, ink_color,
                           x_cursor + dx, y_base + dy, scale, slant)
                x_cursor += int(cw * spacing_x * scale)

        elif layout == "vertical":
            total_height = sum(int(h * spacing_y * scale) for _, h in char_bboxes)
            x_base = size[0] // 2 - int(font_size * 0.45)
            y_cursor = (size[1] - total_height) // 2
            for ch, contours, (cw, ch_h) in zip(chars, char_contours, char_bboxes):
                dx = int(random.uniform(-randomness, randomness) * font_size)
                dy = int(random.uniform(-randomness, randomness) * font_size)
                _draw_char(canvas, draw, contours, ink_color,
                           x_base + dx, y_cursor + dy, scale, slant)
                y_cursor += int(ch_h * spacing_y * scale)

        else:
            raise ValueError(f"不支持布局: {layout}")


    # 印章
    if seal_text:
        seal_size = min(size) // 5
        seal = generate_seal(seal_text, size=seal_size, shape="square", style="yang")
        if layout == "horizontal":
            sx = size[0] - seal_size - 40
            sy = size[1] - seal_size - 40
        else:
            sx = size[0] - seal_size - 40
            sy = size[1] - seal_size - 40
        canvas.paste(seal, (sx, sy), seal)

    # 龙纹可见水印
    canvas = add_visible_watermark(canvas, opacity=60, corner=True)

    # 频域水印
    payload = f"UID9622|{style_code}|{classic}|{DNA}"
    canvas = add_frequency_watermark(canvas, payload, strength=12)

    # 作品编号
    work_id = generate_work_id(
        style["category_code"],
        style["artist_code"],
        text,
        classic
    )

    if output_name is None:
        output_name = f"{work_id}"
    out_path = OUTPUT_DIR / f"{output_name}.png"
    canvas.save(out_path, dpi=(300, 300))

    return {
        "work_id": work_id,
        "style": style["name"],
        "text": text,
        "layout": layout,
        "output": str(out_path),
        "size": size,
        "dna": DNA,
    }


if __name__ == "__main__":
    print("可用样式:")
    for s in list_styles():
        print(f"  {s['code']}: {s['name']} ({s['era']})")

    result = render("自强不息", style_code="YZQ-KA", seal_text="龍魂", classic="YIJING")
    print("\n渲染结果:")
    for k, v in result.items():
        print(f"  {k}: {v}")
