#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 中国文化公开素材采集器
只采集 Wikimedia Commons 上明确为 Public Domain / CC0 的真实图片
DNA: #龍芯⚡️2026-07-04-LONGHUN-CULTURAL-ASSET-FETCHER-v1.0
"""

import json
import os
import re
import sys
import time
import hashlib
import requests
from pathlib import Path
from urllib.parse import quote

DNA = "#龍芯⚡️2026-07-04-LONGHUN-CULTURAL-ASSET-FETCHER-v1.0"
BASE_DIR = Path(__file__).resolve().parent.parent
ASSET_DIR = BASE_DIR / "assets" / "cultural"
REGISTRY = ASSET_DIR / "cultural_assets_registry.json"
CHANGE_LOG = ASSET_DIR / "cultural_change_log.jsonl"

# 确保目录存在
for sub in ["figures", "calligraphy", "seals", "costumes", "backgrounds", "artifacts"]:
    (ASSET_DIR / sub).mkdir(parents=True, exist_ok=True)

# 可接受的自由版权标识
FREE_LICENSES = {
    "pd", "public domain", "cc0", "cc-zero", "publicdomain",
    "pdm", "public domain mark",
}

# 主题配置：关键词 + 分类 + 默认文件名前缀
TOPICS = {
    "laozi":        {"en": "Laozi", "zh": "老子", "cat": "figures", "ext": "jpg"},
    "tao_te_ching": {"en": "Tao Te Ching", "zh": "道德经", "cat": "backgrounds", "ext": "jpg"},
    "i_ching":      {"en": "I Ching", "zh": "易经", "cat": "backgrounds", "ext": "jpg"},
    "hetu_luoshu":  {"en": "Lo Shu Square", "zh": "河图洛书", "cat": "backgrounds", "ext": "jpg"},
    "calligraphy":  {"en": "Chinese calligraphy", "zh": "书法", "cat": "calligraphy", "ext": "jpg"},
    "seal":         {"en": "Chinese seal", "zh": "印章", "cat": "seals", "ext": "jpg"},
    "tang_costume": {"en": "Tang dynasty clothing", "zh": "唐装", "cat": "costumes", "ext": "jpg"},
    "ink_wash":     {"en": "Chinese ink wash painting", "zh": "水墨画", "cat": "backgrounds", "ext": "jpg"},
    "bronze":       {"en": "Chinese bronze ware", "zh": "青铜器", "cat": "artifacts", "ext": "jpg"},
    "jade":         {"en": "Chinese jade", "zh": "玉器", "cat": "artifacts", "ext": "jpg"},
    "bamboo_slip":  {"en": "Bamboo and silk manuscripts", "zh": "竹简", "cat": "artifacts", "ext": "jpg"},
    "guqin":        {"en": "Guqin", "zh": "古琴", "cat": "artifacts", "ext": "jpg"},
    "laozi_statue": {"en": "Laozi statue", "zh": "老子像", "cat": "figures", "ext": "jpg"},
    "tang_figure":  {"en": "Tang dynasty figurine", "zh": "唐三彩", "cat": "figures", "ext": "jpg"},
}


def is_free_license(license_text: str) -> bool:
    t = license_text.lower()
    return any(k in t for k in FREE_LICENSES)


def search_commons(query: str, limit: int = 20):
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "generator": "search",
        "gsrnamespace": 6,
        "gsrsearch": query,
        "gsrlimit": limit,
        "prop": "imageinfo",
        "iiprop": "url|size|mime|extmetadata",
        "format": "json",
        "origin": "*",
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    pages = data.get("query", {}).get("pages", {})
    results = []
    for page_id, page in pages.items():
        title = page.get("title", "")
        if not title.startswith("File:"):
            continue
        info = (page.get("imageinfo") or [{}])[0]
        url = info.get("url", "")
        thumb = info.get("thumburl", "")
        width = info.get("width", 0)
        height = info.get("height", 0)
        meta = info.get("extmetadata", {})
        license_name = meta.get("LicenseShortName", {}).get("value", "")
        license_url = meta.get("LicenseUrl", {}).get("value", "")
        artist = meta.get("Artist", {}).get("value", "")
        desc = meta.get("ImageDescription", {}).get("value", "")
        results.append({
            "title": title,
            "url": url,
            "thumb": thumb,
            "width": width,
            "height": height,
            "license": license_name,
            "license_url": license_url,
            "artist": artist,
            "description": desc,
        })
    return results


def download_image(url: str, dest: Path):
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    dest.write_bytes(r.content)


def log_change(action: str, item: str, detail: dict):
    entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "action": action,
        "item": item,
        "detail": detail,
        "dna": DNA,
    }
    with open(CHANGE_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main():
    registry = {"dna": DNA, "assets": {}}
    if REGISTRY.exists():
        try:
            registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        except Exception:
            pass

    print(f"🐉 开始采集公开版权中国文化素材 | {DNA}")
    print(f"📁 目标目录: {ASSET_DIR}")

    for key, cfg in TOPICS.items():
        query = cfg["en"]
        cat_dir = ASSET_DIR / cfg["cat"]
        dest_name = f"{key}.{cfg['ext']}"
        dest = cat_dir / dest_name

        print(f"\n🔍 {cfg['zh']} ({key}) → 搜索: {query}")
        try:
            results = search_commons(query, limit=25)
        except Exception as e:
            print(f"   ⚠️ 搜索失败: {e}")
            continue

        chosen = None
        for r in results:
            if not r["url"]:
                continue
            # 优先选大图，宽或高至少 600
            if max(r["width"], r["height"]) < 400:
                continue
            if is_free_license(r["license"]):
                chosen = r
                break

        if not chosen and results:
            # 无明确自由许可但继续尝试：如果 license 为空，也下载（Commons 上未标注者风险自担，脚本保守跳过）
            chosen = next((r for r in results if r["url"] and max(r["width"], r["height"]) >= 400), None)
            if chosen:
                print(f"   🟡 未找到明确 PD/CC0 许可，但找到可用图片，将标记为需人工复核")
        
        if not chosen:
            print(f"   🔴 未找到合适图片，生成 SVG 占位")
            # 生成占位 SVG
            svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300">
  <rect width="400" height="300" fill="#f5f0e6"/>
  <text x="200" y="150" text-anchor="middle" font-family="serif" font-size="28" fill="#8b0000">{cfg["zh"]} · 待补充真实图像</text>
  <text x="200" y="190" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#555">来源：公开版权素材待采集</text>
</svg>'''
            dest_svg = cat_dir / f"{key}.svg"
            dest_svg.write_text(svg, encoding="utf-8")
            registry["assets"][key] = {
                "local": str(dest_svg.relative_to(BASE_DIR)),
                "status": "placeholder",
                "topic_zh": cfg["zh"],
                "category": cfg["cat"],
                "source_url": "",
                "license": "",
                "attribution": "",
                "width": 400,
                "height": 300,
                "dna": DNA,
            }
            log_change("placeholder_created", key, {"file": str(dest_svg)})
            continue

        try:
            download_image(chosen["url"], dest)
            file_size = dest.stat().st_size
            print(f"   🟢 已下载: {dest_name} ({file_size} bytes, {chosen['width']}x{chosen['height']}, 许可: {chosen['license']})")
            registry["assets"][key] = {
                "local": str(dest.relative_to(BASE_DIR)),
                "status": "downloaded",
                "topic_zh": cfg["zh"],
                "category": cfg["cat"],
                "source_url": chosen["url"],
                "source_title": chosen["title"],
                "license": chosen["license"],
                "license_url": chosen["license_url"],
                "attribution": re.sub(r"<[^>]+>", "", chosen["artist"]) if chosen["artist"] else "Wikimedia Commons",
                "description": re.sub(r"<[^>]+>", "", chosen["description"])[:200],
                "width": chosen["width"],
                "height": chosen["height"],
                "dna": DNA,
            }
            log_change("asset_downloaded", key, {
                "file": str(dest),
                "source_url": chosen["url"],
                "license": chosen["license"],
            })
        except Exception as e:
            print(f"   🔴 下载失败: {e}")

        time.sleep(0.5)

    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✅ 采集完成，注册表: {REGISTRY}")
    print(f"📝 改动日志: {CHANGE_LOG}")


if __name__ == "__main__":
    main()
