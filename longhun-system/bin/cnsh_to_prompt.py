#!/usr/bin/env python3
"""
龍魂CNSH提示詞轉換器 · ComfyUI接口
DNA: #龍芯⚡️2026-03-29-ComfyUI-本地引擎搭建-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
作者: 诸葛鑫（UID9622）
理論指導: 曾仕強老師（永恒顯示）

用法:
  python3 cnsh_to_prompt.py "自在性感·薄紗·金色光影·真人感"
  python3 cnsh_to_prompt.py --negative "自在性感·薄紗"   # 輸出反向詞
  python3 cnsh_to_prompt.py --memory "星辰摘要文字"       # 注入星辰記憶摘要
"""

import sys
import json
import argparse
from pathlib import Path

# ── CNSH關鍵字 → 英文提示詞映射表（可持續擴充）
CNSH_POSITIVE_MAP: dict[str, str] = {
    # 姿態風格
    "自在性感": "relaxed sensual pose, confident body language, natural expression, comfortable in skin",
    "自在": "natural relaxed pose, effortless grace",
    "性感": "sensual alluring, confident pose",
    "優雅": "elegant posture, refined grace",
    "慵懶": "languid relaxed, lying casually, dreamy expression",

    # 服裝面料
    "薄紗": "sheer chiffon fabric, translucent draping, flowing sheer material, gossamer",
    "蕾絲": "delicate lace trim, intricate lace details, lace lingerie",
    "薄紗蕾絲": "sheer lace fabric, see-through lace overlay, delicate translucent lace",
    "絲綢": "silk fabric, lustrous smooth silk, satin sheen",
    "棉麻": "cotton linen, natural fabric texture, breathable material",

    # 光影
    "金色光影": "golden hour lighting, warm sunlight, soft backlight, volumetric golden light",
    "柔光": "soft diffused lighting, gentle shadows, flattering light",
    "逆光": "backlit silhouette, rim light, glowing edges",
    "窗邊光": "window light, natural indoor lighting, soft side light",
    "暗調": "low key lighting, dramatic shadows, moody atmosphere",

    # 皮膚質感
    "真人感": "ultra realistic, photorealistic, natural skin texture, real pores, lifelike",
    "自然皮膚": "natural skin tone, realistic skin imperfections, warm skin undertone, visible pores",
    "瓷肌": "porcelain smooth skin, flawless complexion, luminous skin",
    "健康膚色": "healthy warm skin tone, natural tan, sun-kissed skin",

    # 畫面質量
    "高清": "8k resolution, ultra high definition, sharp details",
    "電影感": "cinematic composition, film grain, movie still",
    "攝影感": "photographic, DSLR quality, professional photography",
    "立體感": "3D depth, dramatic shadows, strong contrast, dimensional",
    "景深": "bokeh background, shallow depth of field, subject in focus",

    # 固定臉相關
    "參考臉固定": "consistent face, same person, face preservation, identity consistent",
    "固定臉": "face consistent, preserve facial features, same identity",

    # 星辰記憶接口（預留，動態注入）
    "星辰記憶": "__MEMORY_INJECTION__",
}

CNSH_NEGATIVE_BASE = (
    "cartoon, anime, painting, illustration, sketch, "
    "plastic skin, doll-like, overly smooth, waxy skin, "
    "stiff pose, awkward pose, unnatural position, "
    "overexposed, blown out highlights, "
    "nsfw text, watermark, signature, username, "
    "deformed hands, extra fingers, missing fingers, "
    "blurry, low quality, jpeg artifacts, "
    "multiple people, duplicate, clone"
)


def cnsh_to_prompt(cnsh_input: str, memory_context: str = "") -> dict[str, str]:
    """
    CNSH語法 → ComfyUI正向+反向提示詞

    Args:
        cnsh_input: 用·分隔的CNSH關鍵字，如 "自在性感·薄紗·金色光影"
        memory_context: 星辰記憶壓縮摘要（可選，直接注入提示詞）

    Returns:
        {"positive": "...", "negative": "...", "dna": "..."}
    """
    keywords = [k.strip() for k in cnsh_input.split("·") if k.strip()]
    english_parts = []
    unknown = []

    for kw in keywords:
        if kw in CNSH_POSITIVE_MAP:
            val = CNSH_POSITIVE_MAP[kw]
            if val == "__MEMORY_INJECTION__":
                if memory_context:
                    english_parts.append(memory_context)
                else:
                    print(f"⚠️  星辰記憶關鍵字已識別，但未傳入 --memory 內容", file=sys.stderr)
            else:
                english_parts.append(val)
        else:
            unknown.append(kw)
            # 未知關鍵字直接當英文詞附加（容錯）
            english_parts.append(kw)

    if unknown:
        print(f"⚠️  未識別CNSH關鍵字（已直接附加，建議擴充映射表）: {unknown}", file=sys.stderr)

    # 注入星辰記憶（如果傳入但沒用關鍵字觸發）
    if memory_context and "星辰記憶" not in keywords:
        english_parts.insert(0, memory_context)

    positive = "1woman, " + ", ".join(english_parts) + ", best quality, masterpiece"
    negative = CNSH_NEGATIVE_BASE

    from datetime import datetime
    dna = f"#龍芯⚡️UID9622-PROMPT-{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    return {
        "positive": positive,
        "negative": negative,
        "dna": dna,
        "source_cnsh": cnsh_input,
    }


def main():
    parser = argparse.ArgumentParser(
        description="龍魂CNSH提示詞轉換器 · UID9622"
    )
    parser.add_argument("cnsh", help="CNSH關鍵字，用·分隔，例如: 自在性感·薄紗·金色光影·真人感")
    parser.add_argument("--memory", default="", help="星辰記憶壓縮摘要，直接注入正向提示詞")
    parser.add_argument("--json", action="store_true", help="輸出JSON格式（給程序調用）")
    args = parser.parse_args()

    result = cnsh_to_prompt(args.cnsh, args.memory)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 60)
        print(f"🐉 龍魂CNSH提示詞轉換器 | {result['dna']}")
        print("=" * 60)
        print(f"\n【正向提示詞】\n{result['positive']}")
        print(f"\n【反向提示詞】\n{result['negative']}")
        print(f"\n【CNSH源碼】{result['source_cnsh']}")
        print("=" * 60)


if __name__ == "__main__":
    main()
