#!/usr/bin/env python3
#龍芯⚡️2026-07-19-MAGDECL-LOOKUP-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂 · 磁偏角查询模块 v1.0
功能：根据经纬度、年份查询磁偏角（真北修正）。
策略：优先本地 lookup 表 → 可选 IGRF 模型/NOAA API。
DNA: #龍芯⚡️2026-07-19-MAGDECL-LOOKUP-v1.0
"""

import json
import math
import os
import urllib.request
from datetime import datetime
from pathlib import Path

# 预置中国部分城市磁偏角（西偏为负，单位度），基于 IGRF-13 2020 年代数据
PRESET = {
    "兰溪": {"lat": 29.21, "lon": 119.46, "decl": -4.8, "year": 2025, "source": "IGRF-13 estimate"},
    "诸葛八卦村": {"lat": 29.50, "lon": 119.20, "decl": -4.7, "year": 2025, "source": "IGRF-13 estimate"},
    "杭州": {"lat": 30.27, "lon": 120.15, "decl": -4.9, "year": 2025, "source": "IGRF-13 estimate"},
    "上海": {"lat": 31.23, "lon": 121.47, "decl": -5.0, "year": 2025, "source": "IGRF-13 estimate"},
    "北京": {"lat": 39.90, "lon": 116.41, "decl": -5.5, "year": 2025, "source": "IGRF-13 estimate"},
    "西安": {"lat": 34.27, "lon": 108.93, "decl": -3.8, "year": 2025, "source": "IGRF-13 estimate"},
    "成都": {"lat": 30.57, "lon": 104.07, "decl": -2.4, "year": 2025, "source": "IGRF-13 estimate"},
    "广州": {"lat": 23.13, "lon": 113.26, "decl": -2.8, "year": 2025, "source": "IGRF-13 estimate"},
    "深圳": {"lat": 22.54, "lon": 114.06, "decl": -2.7, "year": 2025, "source": "IGRF-13 estimate"},
}

CACHE_DIR = Path.home() / ".longhun" / "cache" / "magdecl"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def linear_interp(lat, lon, p1, p2, p3, p4):
    """四点双线性插值（单位：度）。p=(lat, lon, decl)"""
    x, y = lon, lat
    x1, x2 = p1[1], p2[1]
    y1, y2 = p1[0], p3[0]
    if x1 == x2 or y1 == y2:
        return p1[2]
    f11, f21 = p1[2], p2[2]
    f12, f22 = p3[2], p4[2]
    fx1 = f11 * (x2 - x) / (x2 - x1) + f21 * (x - x1) / (x2 - x1)
    fx2 = f12 * (x2 - x) / (x2 - x1) + f22 * (x - x1) / (x2 - x1)
    return fx1 * (y2 - y) / (y2 - y1) + fx2 * (y - y1) / (y2 - y1)


def decl_from_preset(lat, lon):
    """从预置点插值估算磁偏角。"""
    if not PRESET:
        return None
    pts = [(v["lat"], v["lon"], v["decl"]) for v in PRESET.values()]
    # 找最近的4个点做简单加权平均（按距离倒数）
    weights = []
    for plat, plon, pdecl in pts:
        d = math.hypot(lat - plat, lon - plon)
        if d < 1e-6:
            return pdecl
        weights.append((1.0 / (d + 0.1), pdecl))
    total_w = sum(w for w, _ in weights)
    return sum(w * d for w, d in weights) / total_w


def decl_from_noaa(lat, lon, year=None):
    """调用 NOAA 磁偏角 API（需联网）。失败返回 None。"""
    year = year or datetime.now().year
    url = f"https://www.ngdc.noaa.gov/geomag-web/calculators/calculateDeclination?lat1={lat}&lon1={lon}&resultFormat=json&startYear={year}"
    cache_file = CACHE_DIR / f"noaa_{lat:.4f}_{lon:.4f}_{year}.json"
    if cache_file.exists():
        try:
            return json.loads(cache_file.read_text(encoding="utf-8"))
        except Exception:
            pass
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        decl = data.get("result", [{}])[0].get("declination", None)
        if decl is not None:
            cache_file.write_text(json.dumps({"decl": float(decl), "year": year, "source": "NOAA"}, ensure_ascii=False), encoding="utf-8")
            return {"decl": float(decl), "year": year, "source": "NOAA API"}
    except Exception:
        pass
    return None


def estimate_decl(lat, lon, year=None, prefer_online=False):
    """
    综合估算磁偏角。
    默认使用本地预置表插值；prefer_online=True 则先尝试 NOAA API。
    """
    year = year or datetime.now().year
    if prefer_online:
        online = decl_from_noaa(lat, lon, year)
        if online:
            return online
    local = decl_from_preset(lat, lon)
    if local is not None:
        return {"decl": round(local, 2), "year": year, "source": "local preset interpolation", "note": "approximate"}
    return {"decl": None, "year": year, "source": "none", "error": "no data available"}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="磁偏角查询")
    parser.add_argument("--lat", type=float, default=29.50, help="纬度")
    parser.add_argument("--lon", type=float, default=119.20, help="经度")
    parser.add_argument("--year", type=int, default=datetime.now().year, help="年份")
    parser.add_argument("--online", action="store_true", help="优先联网查询NOAA")
    parser.add_argument("--city", type=str, help="城市名（如 兰溪、杭州）")
    args = parser.parse_args()

    if args.city and args.city in PRESET:
        p = PRESET[args.city]
        args.lat, args.lon = p["lat"], p["lon"]

    result = estimate_decl(args.lat, args.lon, args.year, prefer_online=args.online)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
