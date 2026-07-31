#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 中国文化视觉占位素材生成器
因当前网络无法访问 Wikimedia Commons，先生成高保真 SVG 占位图。
所有占位图均标注「待替换为真实公开版权图像」，并写入改动日志。
DNA: #龍芯⚡️2026-07-04-LONGHUN-CULTURAL-PLACEHOLDER-v1.0
"""

import json
import time
from pathlib import Path

DNA = "#龍芯⚡️2026-07-04-LONGHUN-CULTURAL-PLACEHOLDER-v1.0"
BASE_DIR = Path(__file__).resolve().parent.parent
ASSET_DIR = BASE_DIR / "assets" / "cultural"
REGISTRY = ASSET_DIR / "cultural_assets_registry.json"
CHANGE_LOG = ASSET_DIR / "cultural_change_log.jsonl"

for sub in ["figures", "calligraphy", "seals", "costumes", "backgrounds", "artifacts"]:
    (ASSET_DIR / sub).mkdir(parents=True, exist_ok=True)

PLACEHOLDERS = {
    "laozi": {
        "zh": "老子", "cat": "figures",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="500" viewBox="0 0 400 500">
  <defs><linearGradient id="paper" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#f7f3e8"/><stop offset="100%" stop-color="#e8e0d0"/></linearGradient></defs>
  <rect width="400" height="500" fill="url(#paper)"/>
  <g opacity="0.9">
    <ellipse cx="200" cy="140" rx="55" ry="65" fill="#3a2e24"/>
    <path d="M140 210 Q200 180 260 210 L280 420 Q200 450 120 420 Z" fill="#5c4a3a"/>
    <path d="M120 420 Q200 450 280 420" stroke="#2a2018" stroke-width="3" fill="none"/>
    <path d="M160 240 Q200 260 240 240" stroke="#d4c4a8" stroke-width="2" fill="none"/>
  </g>
  <text x="200" y="470" text-anchor="middle" font-family="serif" font-size="20" fill="#4a0000">老子 · 先秦思想家</text>
  <text x="200" y="40" text-anchor="middle" font-family="serif" font-size="14" fill="#555">占位图 · 待替换为真实公开版权画像</text>
</svg>'''
    },
    "tao_te_ching": {
        "zh": "道德经", "cat": "backgrounds",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <defs><radialGradient id="inkbg" cx="0.5" cy="0.5" r="0.8"><stop offset="0%" stop-color="#f9f6ef"/><stop offset="80%" stop-color="#e6e0d0"/><stop offset="100%" stop-color="#c7bca5"/></radialGradient></defs>
  <rect width="800" height="600" fill="url(#inkbg)"/>
  <g opacity="0.12" fill="#1a1a1a">
    <circle cx="150" cy="120" r="80"/><circle cx="650" cy="450" r="120"/>
    <path d="M0 500 Q400 450 800 520" stroke="#000" stroke-width="40" fill="none"/>
  </g>
  <text x="400" y="300" text-anchor="middle" font-family="serif" font-size="80" fill="#2b0a0a" opacity="0.85">道</text>
  <text x="400" y="560" text-anchor="middle" font-family="serif" font-size="16" fill="#444">道德经 · 水墨绢本质感占位 · 待替换</text>
</svg>'''
    },
    "i_ching": {
        "zh": "易经", "cat": "backgrounds",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <rect width="800" height="600" fill="#f4f1ea"/>
  <g stroke="#1a1a1a" stroke-width="4" stroke-linecap="round">
    <line x1="350" y1="150" x2="450" y2="150"/><line x1="350" y1="170" x2="450" y2="170"/><line x1="350" y1="190" x2="450" y2="190"/>
    <line x1="350" y1="220" x2="420" y2="220"/><line x1="430" y1="220" x2="450" y2="220"/>
    <line x1="350" y1="250" x2="450" y2="250"/><line x1="350" y1="270" x2="450" y2="270"/>
    <line x1="350" y1="300" x2="420" y2="300"/><line x1="430" y1="300" x2="450" y2="300"/>
    <line x1="350" y1="330" x2="450" y2="330"/><line x1="350" y1="350" x2="450" y2="350"/>
  </g>
  <text x="400" y="450" text-anchor="middle" font-family="serif" font-size="60" fill="#4a0000">易</text>
  <text x="400" y="560" text-anchor="middle" font-family="serif" font-size="16" fill="#555">易经 · 六爻卦象占位 · 待替换</text>
</svg>'''
    },
    "hetu_luoshu": {
        "zh": "河图洛书", "cat": "backgrounds",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <rect width="800" height="600" fill="#f7f3e8"/>
  <g transform="translate(400,300)" stroke="#3a0000" stroke-width="2" fill="none">
    <circle r="180"/><circle r="120"/><circle r="60"/>
    <line x1="-180" y1="0" x2="180" y2="0"/><line x1="0" y1="-180" x2="0" y2="180"/>
    <line x1="-127" y1="-127" x2="127" y2="127"/><line x1="-127" y1="127" x2="127" y2="-127"/>
  </g>
  <text x="400" y="560" text-anchor="middle" font-family="serif" font-size="16" fill="#555">河图洛书 · 九宫数理占位 · 待替换</text>
</svg>'''
    },
    "calligraphy": {
        "zh": "书法", "cat": "calligraphy",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">
  <rect width="600" height="400" fill="#f7f3e8"/>
  <g fill="#111" opacity="0.85">
    <path d="M150 120 Q180 110 200 140 Q210 180 180 200 Q140 210 130 180 Q120 150 150 120" />
    <path d="M250 100 Q280 90 300 130 L290 250 Q250 260 240 220 Z" />
    <path d="M350 110 Q390 100 410 150 L400 240 Q360 250 340 200 Z" />
    <path d="M450 130 Q490 120 510 170 L500 260 Q460 270 440 220 Z" />
  </g>
  <text x="300" y="340" text-anchor="middle" font-family="serif" font-size="22" fill="#4a0000">龍魂 · 书法占位</text>
  <text x="300" y="370" text-anchor="middle" font-family="serif" font-size="13" fill="#555">待替换为真实书法作品公开版权图像</text>
</svg>'''
    },
    "seal": {
        "zh": "印章", "cat": "seals",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300" viewBox="0 0 300 300">
  <rect width="300" height="300" fill="#f7f3e8"/>
  <rect x="50" y="50" width="200" height="200" rx="20" fill="#8b0000" opacity="0.9"/>
  <text x="150" y="175" text-anchor="middle" font-family="serif" font-size="110" fill="#f7f3e8" font-weight="bold">龍魂</text>
  <text x="150" y="270" text-anchor="middle" font-family="serif" font-size="14" fill="#555">印章占位 · 待替换为真实印蜕</text>
</svg>'''
    },
    "tang_costume": {
        "zh": "唐装", "cat": "costumes",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="600" viewBox="0 0 400 600">
  <rect width="400" height="600" fill="#f7f3e8"/>
  <g>
    <path d="M120 180 Q200 150 280 180 L300 500 Q200 540 100 500 Z" fill="#7a1f1f"/>
    <path d="M120 180 Q200 120 280 180" fill="#5c1212"/>
    <path d="M150 220 L250 220 L250 460 L150 460 Z" fill="#a84444" opacity="0.3"/>
    <circle cx="200" cy="240" r="12" fill="#d4af37"/>
    <circle cx="200" cy="300" r="12" fill="#d4af37"/>
    <circle cx="200" cy="360" r="12" fill="#d4af37"/>
  </g>
  <text x="200" y="560" text-anchor="middle" font-family="serif" font-size="18" fill="#4a0000">唐代服饰 · 圆领袍占位</text>
  <text x="200" y="40" text-anchor="middle" font-family="serif" font-size="13" fill="#555">待替换为真实唐代服饰公开版权图像</text>
</svg>'''
    },
    "ink_wash": {
        "zh": "水墨画", "cat": "backgrounds",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <rect width="800" height="600" fill="#f7f3e8"/>
  <g fill="#1a1a1a" opacity="0.15">
    <path d="M0 350 Q200 320 350 380 T600 360 T800 400 V600 H0 Z"/>
    <ellipse cx="200" cy="250" rx="80" ry="40"/>
    <ellipse cx="600" cy="200" rx="120" ry="60"/>
  </g>
  <g stroke="#1a1a1a" stroke-width="2" fill="none" opacity="0.3">
    <path d="M100 500 Q150 450 200 480 T300 470"/>
    <path d="M500 520 Q560 480 620 500 T750 490"/>
  </g>
  <text x="400" y="560" text-anchor="middle" font-family="serif" font-size="16" fill="#555">水墨山水占位 · 待替换</text>
</svg>'''
    },
    "bronze": {
        "zh": "青铜器", "cat": "artifacts",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">
  <defs><radialGradient id="bronze" cx="0.4" cy="0.4" r="0.8"><stop offset="0%" stop-color="#bfa880"/><stop offset="50%" stop-color="#6e5a3a"/><stop offset="100%" stop-color="#3a2e1c"/></radialGradient></defs>
  <rect width="400" height="400" fill="#f7f3e8"/>
  <path d="M100 120 Q200 80 300 120 V280 Q200 320 100 280 Z" fill="url(#bronze)"/>
  <path d="M130 160 Q200 140 270 160 V240 Q200 260 130 240 Z" fill="#4a3a24" opacity="0.4"/>
  <text x="200" y="360" text-anchor="middle" font-family="serif" font-size="18" fill="#4a0000">青铜器 · 鼎占位</text>
  <text x="200" y="40" text-anchor="middle" font-family="serif" font-size="13" fill="#555">待替换为真实青铜器公开版权图像</text>
</svg>'''
    },
    "jade": {
        "zh": "玉器", "cat": "artifacts",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">
  <defs><radialGradient id="jade" cx="0.4" cy="0.4" r="0.8"><stop offset="0%" stop-color="#d8f2e5"/><stop offset="50%" stop-color="#7fbfa3"/><stop offset="100%" stop-color="#3d6b55"/></radialGradient></defs>
  <rect width="400" height="400" fill="#f7f3e8"/>
  <circle cx="200" cy="200" r="120" fill="url(#jade)" stroke="#2f5544" stroke-width="3"/>
  <circle cx="200" cy="200" r="60" fill="none" stroke="#2f5544" stroke-width="2" opacity="0.5"/>
  <text x="200" y="360" text-anchor="middle" font-family="serif" font-size="18" fill="#2f5544">玉璧占位 · 待替换</text>
</svg>'''
    },
    "bamboo_slip": {
        "zh": "竹简", "cat": "artifacts",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">
  <rect width="600" height="400" fill="#e8e0d0"/>
  <g fill="#c4a76a" stroke="#8b6f3e" stroke-width="1">
    <rect x="50" y="80" width="40" height="240"/><rect x="100" y="80" width="40" height="240"/><rect x="150" y="80" width="40" height="240"/>
    <rect x="200" y="80" width="40" height="240"/><rect x="250" y="80" width="40" height="240"/><rect x="300" y="80" width="40" height="240"/>
    <rect x="350" y="80" width="40" height="240"/><rect x="400" y="80" width="40" height="240"/><rect x="450" y="80" width="40" height="240"/>
    <rect x="500" y="80" width="40" height="240"/>
  </g>
  <line x1="40" y1="140" x2="560" y2="140" stroke="#5a3e1e" stroke-width="3"/>
  <line x1="40" y1="280" x2="560" y2="280" stroke="#5a3e1e" stroke-width="3"/>
  <text x="300" y="360" text-anchor="middle" font-family="serif" font-size="16" fill="#4a0000">竹简占位 · 待替换</text>
</svg>'''
    },
    "guqin": {
        "zh": "古琴", "cat": "artifacts",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="250" viewBox="0 0 600 250">
  <rect width="600" height="250" fill="#f7f3e8"/>
  <path d="M60 80 Q300 60 540 80 L540 170 Q300 190 60 170 Z" fill="#3e2723" stroke="#1a1a1a" stroke-width="2"/>
  <line x1="120" y1="85" x2="120" y2="165" stroke="#d4af37" stroke-width="2"/>
  <line x1="180" y1="82" x2="180" y2="168" stroke="#d4af37" stroke-width="2"/>
  <line x1="240" y1="80" x2="240" y2="170" stroke="#d4af37" stroke-width="2"/>
  <line x1="300" y1="80" x2="300" y2="170" stroke="#d4af37" stroke-width="2"/>
  <line x1="360" y1="80" x2="360" y2="170" stroke="#d4af37" stroke-width="2"/>
  <line x1="420" y1="82" x2="420" y2="168" stroke="#d4af37" stroke-width="2"/>
  <line x1="480" y1="85" x2="480" y2="165" stroke="#d4af37" stroke-width="2"/>
  <circle cx="300" cy="125" r="15" fill="#1a1a1a"/>
  <text x="300" y="225" text-anchor="middle" font-family="serif" font-size="16" fill="#4a0000">古琴占位 · 待替换</text>
</svg>'''
    },
    "laozi_statue": {
        "zh": "老子像", "cat": "figures",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="500" viewBox="0 0 400 500">
  <rect width="400" height="500" fill="#f7f3e8"/>
  <g opacity="0.9">
    <ellipse cx="200" cy="130" rx="60" ry="70" fill="#555"/>
    <path d="M130 210 Q200 180 270 210 L290 430 Q200 460 110 430 Z" fill="#777"/>
    <path d="M130 210 Q200 240 270 210" stroke="#444" stroke-width="3" fill="none"/>
    <rect x="170" y="90" width="60" height="30" rx="10" fill="#ddd" opacity="0.3"/>
  </g>
  <text x="200" y="480" text-anchor="middle" font-family="serif" font-size="18" fill="#4a0000">老子像 · 石雕占位</text>
  <text x="200" y="40" text-anchor="middle" font-family="serif" font-size="13" fill="#555">待替换为真实公开版权雕像图像</text>
</svg>'''
    },
    "tang_figure": {
        "zh": "唐三彩", "cat": "figures",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="500" viewBox="0 0 400 500">
  <rect width="400" height="500" fill="#f7f3e8"/>
  <g>
    <ellipse cx="200" cy="120" rx="55" ry="60" fill="#c48a4a"/>
    <path d="M140 190 Q200 170 260 190 L280 420 Q200 450 120 420 Z" fill="#7a5c3a"/>
    <path d="M160 220 Q200 240 240 220" stroke="#f4d03f" stroke-width="3" fill="none"/>
    <circle cx="170" cy="320" r="20" fill="#2e86c1" opacity="0.7"/>
    <circle cx="230" cy="320" r="20" fill="#28b463" opacity="0.7"/>
  </g>
  <text x="200" y="480" text-anchor="middle" font-family="serif" font-size="18" fill="#4a0000">唐三彩俑占位</text>
  <text x="200" y="40" text-anchor="middle" font-family="serif" font-size="13" fill="#555">待替换为真实唐三彩公开版权图像</text>
</svg>'''
    },
}


def log_change(action, item, detail):
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
    registry = {"dna": DNA, "assets": {}, "note": "因网络无法访问 Wikimedia Commons，先生成 SVG 占位图。后续可运行 fetch_cultural_assets.py 替换为真实 PD/CC0 图像。"}

    for key, cfg in PLACEHOLDERS.items():
        cat_dir = ASSET_DIR / cfg["cat"]
        dest = cat_dir / f"{key}.svg"
        dest.write_text(cfg["svg"], encoding="utf-8")
        registry["assets"][key] = {
            "local": str(dest.relative_to(BASE_DIR)),
            "status": "placeholder",
            "topic_zh": cfg["zh"],
            "category": cfg["cat"],
            "source_url": "",
            "license": "placeholder",
            "attribution": "龍魂占位生成器",
            "width": 400,
            "height": 300,
            "dna": DNA,
        }
        log_change("placeholder_created", key, {"file": str(dest), "reason": "network_unreachable"})
        print(f"🎨 已生成占位: {cfg['zh']} → {dest}")

    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✅ 占位素材生成完毕")
    print(f"📁 注册表: {REGISTRY}")
    print(f"📝 改动日志: {CHANGE_LOG}")


if __name__ == "__main__":
    main()
