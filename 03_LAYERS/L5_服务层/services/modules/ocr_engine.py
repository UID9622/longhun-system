#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·同人-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
龍魂民生 · OCR识别引擎（真实·pytesseract + tesseract 5.5.2）

图片/扫描件 → 文字。支持中英文。
降级标注: tesseract 未安装时标 🔴 不可用。
DNA #龍魂⚡️丙午·辛未·OCR-v1
"""

import subprocess
import shutil

try:
    import pytesseract
    from PIL import Image
    import io
    HAVE = bool(shutil.which("tesseract"))
except Exception:
    HAVE = False


def ocr_image(img_bytes: bytes, lang: str = "chi_sim+eng") -> dict[str, Any]:
    if not HAVE:
        return {"capability": "degraded", "tier": "🔴红线",
                "text": "", "notes": "tesseract 未安装，OCR不可用"}
    try:
        im = Image.open(io.BytesIO(img_bytes))
        text = pytesseract.image_to_string(im, lang=lang)
        return {"capability": "real", "tier": "🟢真实(OCR)",
                "text": text, "lang": lang,
                "notes": "OCR识别结果，建议人工校对关键数字/姓名"}
    except Exception as e:
        return {"capability": "degraded", "tier": "🟡推演(OCR异常)",
                "text": "", "notes": f"OCR失败: {e}"}


if __name__ == "__main__":
    print("HAVE tesseract:", HAVE)
