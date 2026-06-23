#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️2026-06-23-LONGHUN-FONT-SEAL-v1.0
"""
印章生成器

支持：
- 方形/圆形印章
- 阳文（红底白字）/ 阴文（白底红字）
- 自定义印文、边款
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

DNA = "#龍芯⚡️2026-06-23-LONGHUN-FONT-SEAL-v1.0"

SEAL_RED = (178, 34, 34)  # 朱砂红
WHITE = (255, 255, 255)


def _find_font(size: int):
    """优先使用系统楷体/黑体，回退 LonghunFont。"""
    candidates = [
        "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/88d6cc32a907955efa1d014207889413890573be.asset/AssetData/Kaiti.ttc",
        "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/a304e3396d019087ab67af77f5e398977529007d.asset/AssetData/Libian.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        Path(__file__).parent.parent / "output" / "LonghunFont-Regular.otf",
        Path(__file__).parent.parent / "output" / "LonghunFont-Regular-v3.otf",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(str(p), size)
    raise RuntimeError("未找到可用中文字体")


def generate_seal(text: str, size: int = 200, shape: str = "square", style: str = "yang") -> Image.Image:
    """
    生成印章图片。

    Args:
        text: 印文，建议 1~4 字
        size: 输出尺寸（正方形）
        shape: "square" | "circle"
        style: "yang" 阳文（红底白字）| "yin" 阴文（白底红字）
    """
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    bg = SEAL_RED if style == "yang" else WHITE
    fg = WHITE if style == "yang" else SEAL_RED

    padding = size // 12
    if shape == "square":
        draw.rectangle([padding, padding, size - padding, size - padding], fill=bg, outline=fg, width=size // 40)
    elif shape == "circle":
        draw.ellipse([padding, padding, size - padding, size - padding], fill=bg, outline=fg, width=size // 40)
    else:
        raise ValueError(f"不支持印章形状: {shape}")

    # 字体大小
    font_size = size // 2 if len(text) <= 2 else size // 3
    font = _find_font(font_size)

    # 简单布局：2 字竖排，4 字 2x2
    chars = list(text)
    if len(chars) == 1:
        bbox = draw.textbbox((0, 0), chars[0], font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((size - w) // 2 - bbox[0], (size - h) // 2 - bbox[1]), chars[0], font=font, fill=fg)
    elif len(chars) == 2:
        # 竖排：上、下
        for i, ch in enumerate(chars):
            bbox = draw.textbbox((0, 0), ch, font=font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            y = size // 4 + i * (size // 2) - h // 2
            draw.text(((size - w) // 2 - bbox[0], y), ch, font=font, fill=fg)
    elif len(chars) == 4:
        # 2x2：从右到左、从上到下
        positions = [(size * 3 // 4, size // 4), (size // 4, size // 4),
                     (size * 3 // 4, size * 3 // 4), (size // 4, size * 3 // 4)]
        for ch, (cx, cy) in zip(chars, positions):
            bbox = draw.textbbox((0, 0), ch, font=font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text((cx - w // 2 - bbox[0], cy - h // 2 - bbox[1]), ch, font=font, fill=fg)
    else:
        # 其他字数横向居中
        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((size - w) // 2 - bbox[0], (size - h) // 2 - bbox[1]), text, font=font, fill=fg)

    return img


if __name__ == "__main__":
    seal = generate_seal("龍魂", size=256, shape="square", style="yang")
    out = Path(__file__).parent.parent / "output" / "calligraphy" / "seal_sample.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    seal.save(out)
    print(f"✅ 印章样例已保存: {out}")
    print(f"DNA: {DNA}")
