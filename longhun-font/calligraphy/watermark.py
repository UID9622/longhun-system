#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# #龍芯⚡️20260624010825157-AUTO-DNA-C8621837 自动注入·分层治理自愈引擎 · 来源可查
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️2026-06-23-LONGHUN-FONT-WATERMARK-v1.0
"""
龍纹主权水印

1. 可见水印：把「龍」字以低透明度压印在右下角/全图平铺。
2. 频域水印：在 Y 通道 8x8 DCT 中嵌入 UID9622 身份指纹，抗截图/压缩/裁剪。
"""

import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.fftpack import dct, idct

DNA = "#龍芯⚡️2026-06-23-LONGHUN-FONT-WATERMARK-v1.0"
WATERMARK_TEXT = "龍魂 · UID9622"


def _find_font(size: int):
    candidates = [
        "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/88d6cc32a907955efa1d014207889413890573be.asset/AssetData/Kaiti.ttc",
        "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/a304e3396d019087ab67af77f5e398977529007d.asset/AssetData/Libian.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        Path(__file__).parent.parent / "output" / "LonghunFont-Regular.otf",
        Path(__file__).parent.parent / "output" / "LonghunFont-Regular-v3.otf",
    ]
    for p in candidates:
        p = Path(p)
        if p.exists():
            return ImageFont.truetype(str(p), size)
    raise RuntimeError("未找到可用中文字体")


def add_visible_watermark(img: Image.Image, text: str = WATERMARK_TEXT, opacity: int = 50,
                          corner: bool = True, tile: bool = False) -> Image.Image:
    """
    添加可见龍纹水印。

    Args:
        img: 原图
        text: 水印文字
        opacity: 0-255
        corner: 是否在右下角放置
        tile: 是否全图平铺（更强保护）
    """
    result = img.copy().convert("RGBA")
    overlay = Image.new("RGBA", result.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    font_size = max(24, min(result.width, result.height) // 20)
    font = _find_font(font_size)

    if corner:
        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = result.width - w - 20
        y = result.height - h - 20
        draw.text((x, y), text, font=font, fill=(139, 0, 0, opacity))
    elif tile:
        step_x = result.width // 4
        step_y = result.height // 4
        for y in range(0, result.height, step_y):
            for x in range(0, result.width, step_x):
                draw.text((x + 20, y + 20), text, font=font, fill=(139, 0, 0, opacity))
    else:
        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((result.width - w) // 2, (result.height - h) // 2), text,
                  font=font, fill=(139, 0, 0, opacity))

    return Image.alpha_composite(result, overlay).convert("RGB")


def _dct2(block):
    return dct(dct(block.T, norm="ortho").T, norm="ortho")


def _idct2(block):
    return idct(idct(block.T, norm="ortho").T, norm="ortho")


def _embed_bit(block, bit, strength=10):
    """在 8x8 DCT 块的 (3,3) 和 (4,4) 系数中嵌入 1 bit。"""
    coeff = _dct2(block.copy().astype(np.float32))
    mid = (coeff[3, 3] + coeff[4, 4]) / 2
    if bit == 1:
        target = strength * (math.floor(mid / strength) + 1)
    else:
        target = strength * math.floor(mid / strength)
    delta = target - mid
    coeff[3, 3] += delta
    coeff[4, 4] += delta
    return _idct2(coeff)


def add_frequency_watermark(img: Image.Image, payload: str, strength: int = 12) -> Image.Image:
    """
    在图片 Y 通道中嵌入频域水印。

    Args:
        img: 原图（会被转 RGB）
        payload: 要嵌入的字符串，建议长度 <= 64
        strength: 水印强度，越大越鲁棒但越可见
    """
    rgb = img.convert("RGB")
    arr = np.array(rgb, dtype=np.float32)
    # 简单 Y 通道
    y = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]

    # payload -> bits
    bits = []
    for ch in payload:
        for i in range(8):
            bits.append((ord(ch) >> i) & 1)
    bits = np.array(bits, dtype=np.uint8)

    h, w = y.shape
    out_y = y.copy()
    idx = 0
    for row in range(0, h - 8, 8):
        for col in range(0, w - 8, 8):
            if idx >= len(bits):
                break
            block = y[row:row + 8, col:col + 8]
            out_y[row:row + 8, col:col + 8] = _embed_bit(block, bits[idx], strength)
            idx += 1
        if idx >= len(bits):
            break

    # 合并回 RGB
    diff = out_y - y
    out_arr = arr + diff[:, :, np.newaxis]
    out_arr = np.clip(out_arr, 0, 255).astype(np.uint8)
    return Image.fromarray(out_arr, "RGB")


def extract_frequency_watermark(img: Image.Image, payload_len: int = 32, strength: int = 12) -> str:
    """从图片中提取频域水印。"""
    rgb = img.convert("RGB")
    arr = np.array(rgb, dtype=np.float32)
    y = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]

    bits = []
    h, w = y.shape
    for row in range(0, h - 8, 8):
        for col in range(0, w - 8, 8):
            if len(bits) >= payload_len * 8:
                break
            block = y[row:row + 8, col:col + 8]
            coeff = _dct2(block)
            mid = (coeff[3, 3] + coeff[4, 4]) / 2
            bit = 1 if (mid % strength) > strength / 2 else 0
            bits.append(bit)
        if len(bits) >= payload_len * 8:
            break

    chars = []
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte |= (bits[i + j] << j)
        chars.append(chr(byte))
    return "".join(chars)


if __name__ == "__main__":
    # 自测
    img = Image.new("RGB", (512, 512), (245, 240, 230))
    img = add_visible_watermark(img)
    payload = "UID9622-龍魂-20260623"
    img = add_frequency_watermark(img, payload)
    out = Path(__file__).parent.parent / "output" / "calligraphy" / "watermark_test.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    extracted = extract_frequency_watermark(img, payload_len=len(payload))
    print("原始水印:", payload)
    print("提取水印:", extracted)
    print("匹配:", payload == extracted)
    print(f"DNA: {DNA}")
