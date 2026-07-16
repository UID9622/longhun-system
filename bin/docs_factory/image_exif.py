#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·图片元数据(EXIF)提取 + 反向溯源登记
依赖: Pillow (已装)
功能: 提取相机/时间/GPS等元数据，输出溯源清单，便于保留原作者与来源。

用法:
    python3 image_exif.py <image> [--json]
"""
import sys
import argparse
import json
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def _deg(v):
    """将GPS分数元组转十进制度。"""
    try:
        d = v[0][0] / v[0][1]
        m = v[1][0] / v[1][1]
        s = v[2][0] / v[2][1]
        return d + m / 60.0 + s / 3600.0
    except Exception:
        return None

def extract(image_path):
    img = Image.open(image_path)
    exif = img._getexif()
    meta = {"file": image_path, "size": img.size, "mode": img.mode}
    if not exif:
        meta["exif"] = "无EXIF数据"
        return meta
    out = {}
    gps = {}
    for tid, val in exif.items():
        name = TAGS.get(tid, str(tid))
        if name == "GPSInfo":
            for gk, gv in val.items():
                gps[GPSTAGS.get(gk, str(gk))] = gv
        else:
            out[name] = str(val)
    if gps:
        lat = _deg(gps.get("GPSLatitude")) if gps.get("GPSLatitudeRef") else None
        if lat is not None and gps.get("GPSLatitudeRef") == "S":
            lat = -lat
        lon = _deg(gps.get("GPSLongitude")) if gps.get("GPSLongitudeRef") else None
        if lon is not None and gps.get("GPSLongitudeRef") == "W":
            lon = -lon
        if lat and lon:
            out["GPS"] = f"{lat:.6f}, {lon:.6f}"
    meta["exif"] = out
    return meta

def main():
    ap = argparse.ArgumentParser(description="龍魂图片EXIF提取")
    ap.add_argument("image")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    m = extract(args.image)
    if args.json:
        print(json.dumps(m, ensure_ascii=False, indent=2))
    else:
        print(f"文件: {m['file']}")
        print(f"尺寸: {m['size']}  模式: {m['mode']}")
        print("--- EXIF ---")
        data = m["exif"]
        if isinstance(data, str):
            print(data)
        else:
            for k, v in data.items():
                print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
