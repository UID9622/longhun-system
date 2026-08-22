#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷌同人-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂P0 · 照片EXIF元数据提取

能力: 真实(Pillow getexif)。提取 DateTimeOriginal/DateTimeDigitized/Make/Model/GPSInfo/
ImageSize/Software/Orientation/ColorSpace/Compression/UserComment 等。
'Software'字段出现 = 被编辑过(重要红线信号)。
返回: {"capability","tier","exif":{...},"edited_flag":bool,"notes"}
DNA #龍魂⚡️丙午·辛未·P0-EXIF-v1
"""

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def extract_exif(img_bytes: bytes) -> dict[str, Any]:
    res = {"capability": "real", "tier": "🟢真实(EXIF)",
           "exif": {}, "gps": {}, "edited_flag": False, "notes": ""}
    try:
        im = Image.open(__import__("io").BytesIO(img_bytes))
        exif = im.getexif()
        if not exif:
            res["tier"] = "🟡推演(无EXIF)"
            res["notes"] = "图像无EXIF元数据(可能已剥离/截图/非相机直出)"
            res["exif"] = {"ImageSize": f"{im.size[0]}x{im.size[1]}", "Format": im.format}
            return res
        for tag, val in exif.items():
            name = TAGS.get(tag, tag)
            # 截断超长值
            sval = str(val)
            if len(sval) > 200:
                sval = sval[:200] + "..."
            res["exif"][name] = sval
            if name in ("Software", "ProcessingSoftware"):
                res["edited_flag"] = True
        # GPS 子目录
        try:
            gps = exif.get_ifd(0x8825)
            for tag, val in gps.items():
                res["gps"][GPSTAGS.get(tag, tag)] = str(val)
        except Exception:
            pass
        res["exif"]["ImageSize"] = f"{im.size[0]}x{im.size[1]}"
        if res["edited_flag"]:
            res["tier"] = "🟡推演(检出编辑软件·疑似被编辑)"
            res["notes"] = "EXIF含Software字段，图像很可能经过编辑软件处理"
    except Exception as e:
        res["capability"] = "degraded"
        res["tier"] = "🔴红线"
        res["notes"] = f"EXIF提取失败: {e}"
    return res
