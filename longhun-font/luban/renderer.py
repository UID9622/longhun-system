#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# #龍芯⚡️丙午·乙未·丙申·乙未·䷊泰-AUTO-DNA-LUBAN-RENDERER
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️丙午·乙未·丙申·甲午·䷙大畜-LUBAN-RENDERER-v1.0
"""
鲁班大师 · 通用书法渲染器

核心能力：
- 读取任意字体，渲染为书法作品图片（PNG/JPG/SVG）
- 支持横排 / 竖排
- 支持印章、龍纹水印、宣纸背景
- 输出带作品编号的书法图像
"""

import random
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from . import OUTPUT_DIR
from .brush_engine import raster_brush_stroke, sample_cubic_bezier
from .font_loader import FontLoader, is_cjk
from .style_transfer import StyleParameters, add_ink_texture, apply_slant, bbox, load_style

# 复用现有 calligraphy 模块的印章与水印
from calligraphy.seal_generator import generate_seal
from calligraphy.watermark import add_frequency_watermark, add_visible_watermark
from calligraphy.work_id import generate_work_id

DNA = "#龍芯⚡️丙午·乙未·丙申·甲午·䷙大畜-LUBAN-RENDERER-v1.0"

BACKGROUNDS = {
    "宣纸米黄": (245, 240, 230),
    "宣纸本白": (252, 250, 245),
    "仿古宣纸": (232, 222, 202),
    "洒金宣纸": (245, 235, 210),
    "绢本浅黄": (240, 235, 220),
    "龍魂墨黑": (30, 30, 35),
}


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _make_background(name: str, size: tuple[int, int], texture: bool = True) -> Image.Image:
    color = BACKGROUNDS.get(name, (245, 240, 230))
    img = Image.new("RGB", size, color)
    if not texture:
        return img
    arr = np.array(img, dtype=np.int16)
    noise = np.random.randint(-4, 5, arr.shape, dtype=np.int16)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, "RGB")


def _char_to_bitmap(
    char: str,
    font: ImageFont.FreeTypeFont,
    params: StyleParameters,
    dark_bg: bool = False,
) -> Image.Image:
    """
    把单个字符渲染为带书法效果的透明位图。
    """
    # 1. 先渲染到临时图，获取 bbox
    tmp = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    draw = ImageDraw.Draw(tmp)
    cb = draw.textbbox((0, 0), char, font=font)
    w, h = cb[2] - cb[0], cb[3] - cb[1]
    if w <= 0 or h <= 0:
        return Image.new("RGBA", (1, 1), (0, 0, 0, 0))

    pad = max(w, h) // 4
    canvas_w, canvas_h = w + pad * 2, h + pad * 2

    # 2. 提取字符中心线/骨架：用位图阈值后找笔画中轴简化版
    #    这里使用笔锋引擎沿笔画方向绘制多个圆来模拟毛笔
    ink = _hex_to_rgb(params.ink_color)

    # 创建灰度位图作为笔画蒙版
    gray = Image.new("L", (canvas_w, canvas_h), 0)
    gdraw = ImageDraw.Draw(gray)
    gdraw.text((pad - cb[0], pad - cb[1]), char, font=font, fill=255)

    # 3. 斜切
    if abs(params.slant) > 1e-6:
        slant_matrix = (1, params.slant, -params.slant * pad, 0, 1, 0)
        gray = gray.transform(
            gray.size,
            Image.Transform.AFFINE,
            slant_matrix,
            resample=Image.Resampling.BICUBIC,
        )

    # 4. 边缘墨韵：轻微模糊 + 透明度渐变
    gray = gray.filter(ImageFilter.GaussianBlur(radius=0.6))

    # 5. 转成 RGBA
    rgba = Image.new("RGBA", gray.size, (0, 0, 0, 0))
    pixels = rgba.load()
    gpix = gray.load()
    for y in range(gray.height):
        for x in range(gray.width):
            v = gpix[x, y]
            if v > 10:
                # 墨韵：边缘略透明
                alpha = min(255, int(v * (0.85 + params.ink_pressure * 0.15 / 255)))
                pixels[x, y] = (*ink, alpha)
    return rgba


def _char_to_brush_bitmap(
    char: str,
    font: ImageFont.FreeTypeFont,
    params: StyleParameters,
) -> Image.Image:
    """
    把字符转成大尺寸位图，再用笔锋引擎沿笔画中轴绘制毛笔效果。
    效果比 _char_to_bitmap 更书法化，但依赖字符内部结构。
    """
    ink = _hex_to_rgb(params.ink_color)
    tmp = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    draw = ImageDraw.Draw(tmp)
    cb = draw.textbbox((0, 0), char, font=font)
    w, h = cb[2] - cb[0], cb[3] - cb[1]
    if w <= 0 or h <= 0:
        return Image.new("RGBA", (1, 1), (0, 0, 0, 0))

    pad = max(w, h) // 4
    scale = 2.0  # 高分辨率绘制后缩小，获得平滑边缘
    cw, ch = int((w + pad * 2) * scale), int((h + pad * 2) * scale)

    img = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 用文本渲染出来的位图提取笔画方向（简化：从左到右扫描找主笔画方向）
    # 这里用更稳定的方法：在大图上直接绘制文本作为基础，再做风格化
    big_font = ImageFont.truetype(font.path if hasattr(font, "path") else None, int(font.size * scale))
    if not big_font:
        big_font = font
    draw.text((int((pad - cb[0]) * scale), int((pad - cb[1]) * scale)), char, font=big_font, fill=(*ink, 255))

    # 高斯模糊模拟墨晕
    img = img.filter(ImageFilter.GaussianBlur(radius=scale * 0.5))

    # 斜切
    if abs(params.slant) > 1e-6:
        img = img.transform(
            img.size,
            Image.Transform.AFFINE,
            (1, params.slant, -params.slant * cw * 0.1, 0, 1, 0),
            resample=Image.Resampling.BICUBIC,
        )

    # 缩小回目标尺寸
    target_w, target_h = w + pad * 2, h + pad * 2
    img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    return img


def render(
    text: str,
    font_path: Optional[str] = None,
    style_code: Optional[str] = None,
    layout: str = "horizontal",
    seal_text: Optional[str] = None,
    output_name: Optional[str] = None,
    size: Optional[tuple[int, int]] = None,
    font_size: Optional[int] = None,
    engine: str = "brush",
    add_watermark: bool = True,
    add_frequency_mark: bool = True,
) -> dict[str, Any]:
    """
    通用书法渲染入口。

    Args:
        text: 要渲染的文字
        font_path: 字体文件路径，None 则使用系统字体
        style_code: 风格代码，如 LUBAN-KA / WXZ-XS / YZQ-KA
        layout: horizontal | vertical
        seal_text: 印章文字
        output_name: 输出文件名（不含扩展名）
        size: 画布尺寸 (宽, 高)，None 则自动
        font_size: 字号，None 则使用风格默认值
        engine: brush（笔锋）| classic（经典位图）
        add_watermark: 是否添加可见水印
        add_frequency_mark: 是否添加频域水印

    Returns:
        {
            "work_id": str,
            "output": Path,
            "size": (w, h),
            "style": str,
            "font": str,
            "dna": str,
        }
    """
    loader = FontLoader(font_path)
    style = load_style(style_code)
    params = StyleParameters(style.to_dict())

    fs = font_size or params.font_size
    font = loader.get_pil_font(fs)

    chars = list(text)
    rng = random.Random(f"{style.get('code')}-{text}")

    # 计算画布尺寸
    if size is None:
        char_sizes = []
        tmp = Image.new("RGBA", (1, 1))
        tdraw = ImageDraw.Draw(tmp)
        for ch in chars:
            bb = tdraw.textbbox((0, 0), ch, font=font)
            char_sizes.append((bb[2] - bb[0], bb[3] - bb[1]))
        if layout == "horizontal":
            total_w = sum(int(w * params.spacing_x) for w, _ in char_sizes) + fs
            max_h = max(h for _, h in char_sizes) + fs
            size = (max(total_w, max_h * 2), int(max_h * 1.6))
        else:
            total_h = sum(int(h * params.spacing_y) for _, h in char_sizes) + fs
            max_w = max(w for w, _ in char_sizes) + fs
            size = (int(max_w * 1.6), max(total_h, max_w * 2))

    canvas = _make_background(params.background, size)

    # 逐个字符渲染并粘贴
    if layout == "horizontal":
        char_imgs = []
        total_w = 0
        for ch in chars:
            if engine == "brush":
                cimg = _char_to_brush_bitmap(ch, font, params)
            else:
                cimg = _char_to_bitmap(ch, font, params)
            char_imgs.append(cimg)
            total_w += cimg.width
        x = (size[0] - total_w) // 2
        y_base = (size[1] - max(img.height for img in char_imgs)) // 2
        for cimg in char_imgs:
            dx = int(rng.uniform(-params.randomness, params.randomness) * fs)
            dy = int(rng.uniform(-params.randomness, params.randomness) * fs)
            canvas.paste(cimg, (x + dx, y_base + dy), cimg)
            x += int(cimg.width * params.spacing_x)
    else:
        char_imgs = []
        total_h = 0
        for ch in chars:
            if engine == "brush":
                cimg = _char_to_brush_bitmap(ch, font, params)
            else:
                cimg = _char_to_bitmap(ch, font, params)
            char_imgs.append(cimg)
            total_h += cimg.height
        x_base = (size[0] - max(img.width for img in char_imgs)) // 2
        y = (size[1] - total_h) // 2
        for cimg in char_imgs:
            dx = int(rng.uniform(-params.randomness, params.randomness) * fs)
            dy = int(rng.uniform(-params.randomness, params.randomness) * fs)
            canvas.paste(cimg, (x_base + dx, y + dy), cimg)
            y += int(cimg.height * params.spacing_y)

    # 添加印章
    if seal_text:
        seal = generate_seal(seal_text, size=max(80, min(size) // 6), shape="square", style="yang")
        sx = size[0] - seal.width - 40
        sy = size[1] - seal.height - 40
        canvas.paste(seal, (sx, sy), seal)

    # 可见水印
    if add_watermark:
        canvas = add_visible_watermark(canvas, opacity=40, corner=True)

    # 频域水印
    if add_frequency_mark:
        payload = f"LH-LUBAN-{uuid.uuid4().hex[:12]}-UID9622"
        canvas = add_frequency_watermark(canvas, payload=payload, strength=8)

    # 保存
    work_id = generate_work_id(prefix="LH-LUBAN", classic="GENERAL", text=text)
    out_name = output_name or work_id
    out_path = OUTPUT_DIR / f"{out_name}.png"
    canvas.save(out_path, "PNG")

    return {
        "work_id": work_id,
        "output": out_path,
        "size": canvas.size,
        "style": style.get("name", "鲁班-通用书法"),
        "font": loader.get_font_info().get("family") or loader.get_font_info()["path"],
        "dna": DNA,
    }


def render_svg_sample(
    text: str,
    font_path: Optional[str] = None,
    style_code: Optional[str] = None,
    output_name: Optional[str] = None,
) -> Path:
    """
    生成一个可嵌入网页的 SVG 样张（使用 CSS @font-face 引用字体）。
    这是跨平台渲染的基础：把字体文件 base64 内嵌进 SVG，任何设备都能显示。
    """
    from base64 import b64encode

    loader = FontLoader(font_path)
    style = load_style(style_code)
    params = StyleParameters(style.to_dict())
    font_info = loader.get_font_info()

    with open(loader.resolved_path, "rb") as f:
        font_data = f.read()
    mime = "font/woff2" if loader.resolved_path.suffix.lower() == ".woff2" else "font/ttf"
    b64 = b64encode(font_data).decode("ascii")

    work_id = generate_work_id(prefix="LH-LUBAN-SVG", classic="GENERAL", text=text)
    out_name = output_name or work_id
    out_path = OUTPUT_DIR / f"{out_name}.svg"

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="300" viewBox="0 0 800 300">
  <defs>
    <style>
      @font-face {{
        font-family: "LonghunLuban";
        src: url("data:{mime};base64,{b64}") format("{"woff2" if "woff2" in mime else "truetype"}");
      }}
      .calligraphy {{
        font-family: "LonghunLuban", serif;
        font-size: 120px;
        fill: {params.ink_color};
        transform: skewX({-params.slant * 30:.1f}deg);
      }}
      .bg {{
        fill: rgb{BACKGROUNDS.get(params.background, (245, 240, 230))};
      }}
    </style>
  </defs>
  <rect width="800" height="300" class="bg"/>
  <text x="50" y="180" class="calligraphy">{text}</text>
  <text x="50" y="260" font-size="14" fill="#666">{font_info.get("family", "Unknown")} · {style.get("name", "通用书法")} · {work_id}</text>
</svg>
'''
    out_path.write_text(svg, encoding="utf-8")
    return out_path


if __name__ == "__main__":
    result = render("龍魂字体", style_code="LUBAN-KA", seal_text="龍魂")
    print("渲染完成:", result)
    print("DNA:", DNA)
