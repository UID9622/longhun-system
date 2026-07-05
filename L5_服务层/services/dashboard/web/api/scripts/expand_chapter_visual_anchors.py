#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 中国文化章节视觉不动点扩展器
为 15 章注入 era、visual_theme、figure_image、background_image、seal_text、
font_family、attribution、immutable_points、change_log 等字段。
缺失的素材自动生成 SVG 占位图并注册。
DNA: #龍芯⚡️2026-07-04-LONGHUN-CHAPTER-ANCHORS-v1.0
"""

import json
import hashlib
import time
from pathlib import Path

DNA = "#龍芯⚡️2026-07-04-LONGHUN-CHAPTER-ANCHORS-v1.0"
BASE_DIR = Path(__file__).resolve().parent.parent
CHAPTER_FILE = BASE_DIR / "data" / "中国文化章节.json"
ASSET_DIR = BASE_DIR / "assets" / "cultural"
REGISTRY = ASSET_DIR / "cultural_assets_registry.json"
CHANGE_LOG = ASSET_DIR / "cultural_change_log.jsonl"

for sub in ["figures", "calligraphy", "seals", "costumes", "backgrounds", "artifacts"]:
    (ASSET_DIR / sub).mkdir(parents=True, exist_ok=True)


def ts():
    return time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime())


def new_dna(suffix):
    h = hashlib.sha256(f"{DNA}-{suffix}-{time.time()}".encode()).hexdigest()[:12].upper()
    return f"#龍芯⚡️{time.strftime('%Y-%m-%d')}-LONGHUN-CHAPTER-{suffix}-{h}"


def log_change(action, target, detail):
    entry = {
        "timestamp": ts(),
        "dna": DNA,
        "action": action,
        "target": target,
        "detail": detail
    }
    with open(CHANGE_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# SVG 占位图模板库（按章节需要新增）
EXTRA_SVGS = {
    "taiji_bg": {
        "zh": "太极图", "cat": "backgrounds",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <rect width="800" height="600" fill="#f7f3e8"/>
  <g transform="translate(400,300)">
    <circle r="150" fill="#f7f3e8" stroke="#1a1a1a" stroke-width="3"/>
    <path d="M0,-150 A75,75 0 0,1 0,0 A75,75 0 0,0 0,150 A150,150 0 0,1 0,-150 Z" fill="#1a1a1a"/>
    <circle cx="0" cy="-75" r="18" fill="#f7f3e8"/>
    <circle cx="0" cy="75" r="18" fill="#1a1a1a"/>
  </g>
  <text x="400" y="560" text-anchor="middle" font-family="serif" font-size="16" fill="#555">太极图占位 · 待替换为真实公开版权图像</text>
</svg>'''
    },
    "shanhai_bg": {
        "zh": "山海经", "cat": "backgrounds",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <rect width="800" height="600" fill="#f4efe6"/>
  <g opacity="0.2" fill="#4a2c0f">
    <path d="M100 450 Q250 350 400 420 T700 400 V600 H0 Z"/>
    <ellipse cx="200" cy="280" rx="60" ry="80"/>
    <ellipse cx="600" cy="240" rx="90" ry="50"/>
  </g>
  <text x="400" y="300" text-anchor="middle" font-family="serif" font-size="72" fill="#5a3a1a" opacity="0.6">山海</text>
  <text x="400" y="560" text-anchor="middle" font-family="serif" font-size="16" fill="#555">山海经神话地理占位 · 待替换</text>
</svg>'''
    },
    "huangdi": {
        "zh": "黄帝", "cat": "figures",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="500" viewBox="0 0 400 500">
  <rect width="400" height="500" fill="#f7f3e8"/>
  <g opacity="0.9">
    <ellipse cx="200" cy="140" rx="55" ry="65" fill="#3a2e24"/>
    <path d="M130 210 Q200 180 270 210 L290 430 Q200 460 110 430 Z" fill="#6b4e3d"/>
    <path d="M140 180 Q200 140 260 180" stroke="#2a2018" stroke-width="8" fill="none"/>
    <path d="M160 250 Q200 270 240 250" stroke="#d4c4a8" stroke-width="2" fill="none"/>
  </g>
  <text x="200" y="470" text-anchor="middle" font-family="serif" font-size="18" fill="#4a0000">黄帝 · 华夏人文始祖占位</text>
  <text x="200" y="40" text-anchor="middle" font-family="serif" font-size="13" fill="#555">待替换为真实公开版权画像</text>
</svg>'''
    },
    "zhuangzi": {
        "zh": "庄子", "cat": "figures",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="500" viewBox="0 0 400 500">
  <rect width="400" height="500" fill="#f7f3e8"/>
  <g opacity="0.85">
    <ellipse cx="200" cy="140" rx="52" ry="62" fill="#3a2e24"/>
    <path d="M135 210 Q200 190 265 210 L285 430 Q200 455 115 430 Z" fill="#5a6b7d"/>
    <path d="M120 230 Q200 260 280 230" stroke="#2a2018" stroke-width="3" fill="none"/>
  </g>
  <text x="200" y="470" text-anchor="middle" font-family="serif" font-size="18" fill="#4a0000">庄子 · 逍遥游占位</text>
  <text x="200" y="40" text-anchor="middle" font-family="serif" font-size="13" fill="#555">待替换为真实公开版权画像</text>
</svg>'''
    },
    "sunzi": {
        "zh": "孙子", "cat": "figures",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="500" viewBox="0 0 400 500">
  <rect width="400" height="500" fill="#f7f3e8"/>
  <g opacity="0.9">
    <ellipse cx="200" cy="140" rx="55" ry="62" fill="#3a2e24"/>
    <path d="M130 210 Q200 180 270 210 L290 430 Q200 460 110 430 Z" fill="#4a3a2a"/>
    <path d="M140 190 Q200 160 260 190" stroke="#2a2018" stroke-width="6" fill="none"/>
    <rect x="160" y="300" width="80" height="110" fill="#c4a76a" opacity="0.5"/>
  </g>
  <text x="200" y="470" text-anchor="middle" font-family="serif" font-size="18" fill="#4a0000">孙子 · 兵圣占位</text>
  <text x="200" y="40" text-anchor="middle" font-family="serif" font-size="13" fill="#555">待替换为真实公开版权画像</text>
</svg>'''
    },
    "zengshiqiang": {
        "zh": "曾仕强", "cat": "figures",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="500" viewBox="0 0 400 500">
  <rect width="400" height="500" fill="#f7f3e8"/>
  <g opacity="0.9">
    <ellipse cx="200" cy="140" rx="55" ry="62" fill="#3a2e24"/>
    <path d="M130 210 Q200 185 270 210 L285 430 Q200 455 115 430 Z" fill="#2f3a4a"/>
    <path d="M130 220 Q200 250 270 220" stroke="#2a2018" stroke-width="2" fill="none"/>
    <circle cx="200" cy="140" r="55" fill="#3a2e24" opacity="0.3"/>
  </g>
  <text x="200" y="470" text-anchor="middle" font-family="serif" font-size="18" fill="#4a0000">曾仕强 · 中国式管理占位</text>
  <text x="200" y="40" text-anchor="middle" font-family="serif" font-size="13" fill="#555">待替换为真实公开版权照片</text>
</svg>'''
    },
    "fuxi": {
        "zh": "伏羲", "cat": "figures",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="500" viewBox="0 0 400 500">
  <rect width="400" height="500" fill="#f7f3e8"/>
  <g opacity="0.9">
    <ellipse cx="200" cy="140" rx="58" ry="68" fill="#3a2e24"/>
    <path d="M125 210 Q200 175 275 210 L295 430 Q200 460 105 430 Z" fill="#5c4a3a"/>
    <path d="M130 180 Q200 140 270 180" stroke="#2a2018" stroke-width="7" fill="none"/>
    <path d="M160 240 L200 280 L240 240" stroke="#d4af37" stroke-width="3" fill="none"/>
  </g>
  <text x="200" y="470" text-anchor="middle" font-family="serif" font-size="18" fill="#4a0000">伏羲 · 画卦占位</text>
  <text x="200" y="40" text-anchor="middle" font-family="serif" font-size="13" fill="#555">待替换为真实公开版权画像</text>
</svg>'''
    },
    "chan_figure": {
        "zh": "达摩", "cat": "figures",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="500" viewBox="0 0 400 500">
  <rect width="400" height="500" fill="#f7f3e8"/>
  <g opacity="0.9">
    <ellipse cx="200" cy="140" rx="55" ry="62" fill="#3a2e24"/>
    <path d="M130 210 Q200 180 270 210 L290 430 Q200 460 110 430 Z" fill="#6b5a4a"/>
    <path d="M140 190 Q200 150 260 190" stroke="#2a2018" stroke-width="8" fill="none"/>
    <path d="M180 320 L220 320 L200 380 Z" fill="#4a3a2a" opacity="0.5"/>
  </g>
  <text x="200" y="470" text-anchor="middle" font-family="serif" font-size="18" fill="#4a0000">达摩 · 禅宗初祖占位</text>
  <text x="200" y="40" text-anchor="middle" font-family="serif" font-size="13" fill="#555">待替换为真实公开版权画像</text>
</svg>'''
    },
    "tea_ceremony": {
        "zh": "茶道", "cat": "figures",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="500" viewBox="0 0 400 500">
  <rect width="400" height="500" fill="#f7f3e8"/>
  <g>
    <ellipse cx="200" cy="380" rx="100" ry="25" fill="#d4c4a8" opacity="0.5"/>
    <path d="M140 380 Q200 340 260 380 L260 420 Q200 450 140 420 Z" fill="#2f5544"/>
    <path d="M170 330 L170 250" stroke="#5a3e1e" stroke-width="4"/>
    <ellipse cx="170" cy="240" rx="35" ry="15" fill="#8b6f3e"/>
    <path d="M190 360 Q220 340 240 360" stroke="#d4af37" stroke-width="2" fill="none"/>
  </g>
  <text x="200" y="470" text-anchor="middle" font-family="serif" font-size="18" fill="#4a0000">茶道 · 茶禅一味占位</text>
  <text x="200" y="40" text-anchor="middle" font-family="serif" font-size="13" fill="#555">待替换为真实公开版权图像</text>
</svg>'''
    },
    "seasons_bg": {
        "zh": "二十四节气", "cat": "backgrounds",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <rect width="800" height="600" fill="#f7f3e8"/>
  <g opacity="0.2" fill="none" stroke="#3a5a2a" stroke-width="2">
    <circle cx="400" cy="300" r="200"/>
    <line x1="400" y1="100" x2="400" y2="500"/>
    <line x1="200" y1="300" x2="600" y2="300"/>
    <line x1="258" y1="158" x2="542" y2="442"/>
    <line x1="542" y1="158" x2="258" y2="442"/>
  </g>
  <text x="400" y="300" text-anchor="middle" font-family="serif" font-size="60" fill="#3a5a2a" opacity="0.7">二十四节气</text>
  <text x="400" y="560" text-anchor="middle" font-family="serif" font-size="16" fill="#555">节气历法占位 · 待替换</text>
</svg>'''
    },
    "chan_bg": {
        "zh": "禅宗", "cat": "backgrounds",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <rect width="800" height="600" fill="#f4f1ea"/>
  <g opacity="0.15" fill="#1a1a1a">
    <circle cx="400" cy="300" r="180"/>
    <circle cx="400" cy="300" r="120"/>
    <circle cx="400" cy="300" r="60"/>
  </g>
  <text x="400" y="300" text-anchor="middle" font-family="serif" font-size="80" fill="#4a0000" opacity="0.7">禅</text>
  <text x="400" y="560" text-anchor="middle" font-family="serif" font-size="16" fill="#555">禅宗意境占位 · 待替换</text>
</svg>'''
    },
    "medical_bg": {
        "zh": "医道", "cat": "backgrounds",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <rect width="800" height="600" fill="#f7f3e8"/>
  <g opacity="0.2" stroke="#4a0000" stroke-width="2" fill="none">
    <circle cx="400" cy="300" r="150"/>
    <path d="M400 150 V450 M250 300 H550 M288 212 L512 388 M288 388 L512 212"/>
    <text x="400" y="310" text-anchor="middle" font-family="serif" font-size="40" fill="#4a0000" stroke="none">陰陽</text>
  </g>
  <text x="400" y="560" text-anchor="middle" font-family="serif" font-size="16" fill="#555">黄帝内经医道占位 · 待替换</text>
</svg>'''
    },
    "modern_bg": {
        "zh": "现代中式", "cat": "backgrounds",
        "svg": '''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <rect width="800" height="600" fill="#f7f3e8"/>
  <g opacity="0.12" fill="#1a1a1a">
    <rect x="100" y="100" width="600" height="400" rx="10"/>
  </g>
  <text x="400" y="300" text-anchor="middle" font-family="serif" font-size="60" fill="#4a0000" opacity="0.7">中國式管理</text>
  <text x="400" y="560" text-anchor="middle" font-family="serif" font-size="16" fill="#555">现代中式背景占位 · 待替换</text>
</svg>'''
    }
}


def write_svg(key, info):
    path = ASSET_DIR / info["cat"] / f"{key}.svg"
    path.write_text(info["svg"], encoding="utf-8")
    return path.relative_to(BASE_DIR).as_posix()


def load_registry():
    if REGISTRY.exists():
        return json.loads(REGISTRY.read_text(encoding="utf-8"))
    return {"assets": {}}


def save_registry(reg):
    reg["metadata"] = reg.get("metadata", {})
    reg["metadata"]["last_updated"] = ts()
    reg["metadata"]["dna"] = DNA
    REGISTRY.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")


# 章节视觉不动点配置
CHAPTER_CONFIG = {
    "sancai-369": {
        "era": "上古·先秦",
        "era_en": "Ancient China / Pre-Qin",
        "visual_theme": "河图洛书·九宫数理",
        "figure_image": "hetu_luoshu",
        "background_image": "hetu_luoshu",
        "seal_text": "三才",
        "font_family": "方正清刻本悦宋 / Noto Serif SC",
        "color_primary": "#4a0000",
        "color_secondary": "#d4af37",
        "attribution": "概念来源：《周易·说卦传》《黄帝内经》。占位图待替换为公开版权古籍图像。",
        "immutable_points": [
            "三才=天地人，不可替换为其他三分法",
            "配图使用河图洛书九宫格，不得使用西方几何图案",
            "印章文字固定为「三才」，篆书风格",
            "主色调：暗红（朱砂）+ 金（正色）"
        ]
    },
    "hetu-luoshu": {
        "era": "上古",
        "era_en": "Legendary Ancient",
        "visual_theme": "龙马负图·神龟载书",
        "figure_image": "hetu_luoshu",
        "background_image": "hetu_luoshu",
        "seal_text": "洛书",
        "font_family": "方正小篆体 / Noto Serif SC",
        "color_primary": "#2b0a0a",
        "color_secondary": "#c7bca5",
        "attribution": "概念来源：《周易·系辞上》。占位图待替换为公开版权河图洛书图像。",
        "immutable_points": [
            "河图为体，洛书为用，二者不可混为一谈",
            "洛书九宫纵横和必须等于15",
            "配图须保留黑白点阵/数字矩阵结构",
            "印章文字固定为「洛书」"
        ]
    },
    "taiji": {
        "era": "先秦",
        "era_en": "Pre-Qin",
        "visual_theme": "太极图·阴阳鱼",
        "figure_image": "taiji_bg",
        "background_image": "taiji_bg",
        "seal_text": "太极",
        "font_family": "方正隶变 / Noto Serif SC",
        "color_primary": "#1a1a1a",
        "color_secondary": "#f7f3e8",
        "attribution": "概念来源：《周易·系辞上》《太极图说》。占位图待替换为公开版权太极图图像。",
        "immutable_points": [
            "太极图必须为阴阳鱼标准形态，黑白各半",
            "阴阳眼位置不可调换（白鱼黑眼，黑鱼白眼）",
            "禁止将太极图美化为动漫风格",
            "印章文字固定为「太极」"
        ]
    },
    "yijing": {
        "era": "周·先秦",
        "era_en": "Zhou / Pre-Qin",
        "visual_theme": "六爻卦象·伏羲画卦",
        "figure_image": "fuxi",
        "background_image": "i_ching",
        "seal_text": "易",
        "font_family": "方正金文大篆 / Noto Serif SC",
        "color_primary": "#2b0a0a",
        "color_secondary": "#d4af37",
        "attribution": "概念来源：《周易》经文、伏羲画卦传说。占位图待替换为公开版权卦象/画像。",
        "immutable_points": [
            "六爻必须从下往上排列",
            "阳爻为不间断横线，阴爻为中间断开的两短横",
            "配图须使用中国传统卦象图式",
            "印章文字固定为「易」"
        ]
    },
    "daodejing": {
        "era": "春秋战国",
        "era_en": "Spring and Autumn / Warring States",
        "visual_theme": "老子像·道德经卷轴",
        "figure_image": "laozi",
        "background_image": "tao_te_ching",
        "seal_text": "道德",
        "font_family": "方正清刻本悦宋 / Noto Serif SC",
        "color_primary": "#2f5544",
        "color_secondary": "#d4af37",
        "attribution": "概念来源：《道德经》（老子）。占位图待替换为公开版权老子画像/敦煌写本图像。",
        "immutable_points": [
            "人物图须为传统老子形象（长须、宽袍、持简或骑牛），不可西化/动漫化",
            "背景使用绢本/竹简质感，不得使用现代几何背景",
            "核心章句使用竖排右至左排列",
            "印章文字固定为「道德」"
        ]
    },
    "shanhaijing": {
        "era": "先秦",
        "era_en": "Pre-Qin",
        "visual_theme": "山海经·神话地理图",
        "figure_image": "shanhai_bg",
        "background_image": "shanhai_bg",
        "seal_text": "山海",
        "font_family": "方正隶变 / Noto Serif SC",
        "color_primary": "#5a3a1a",
        "color_secondary": "#c4a76a",
        "attribution": "概念来源：《山海经》。占位图待替换为公开版权古代山海经图绘。",
        "immutable_points": [
            "配图须保留中国传统志怪图绘风格",
            "不得使用日本浮世绘或西方奇幻风格替代",
            "地理方位须符合《山海经》原文记述",
            "印章文字固定为「山海」"
        ]
    },
    "huangdineijing": {
        "era": "先秦至汉",
        "era_en": "Pre-Qin to Han",
        "visual_theme": "黄帝·阴阳五行医道",
        "figure_image": "huangdi",
        "background_image": "medical_bg",
        "seal_text": "内经",
        "font_family": "方正宋刻本秀楷 / Noto Serif SC",
        "color_primary": "#4a0000",
        "color_secondary": "#7fbfa3",
        "attribution": "概念来源：《黄帝内经》。占位图待替换为公开版权黄帝画像/医书图像。",
        "immutable_points": [
            "黄帝形象须为华夏人文始祖传统造型",
            "阴阳图须为标准太极阴阳，不可简化",
            "五行配五色固定：木青、火赤、土黄、金白、水黑",
            "印章文字固定为「内经」"
        ]
    },
    "zhuangzi": {
        "era": "战国",
        "era_en": "Warring States",
        "visual_theme": "庄子·逍遥游·鲲鹏",
        "figure_image": "zhuangzi",
        "background_image": "ink_wash",
        "seal_text": "逍遥",
        "font_family": "方正草書 / Noto Serif SC",
        "color_primary": "#2f3a4a",
        "color_secondary": "#d4af37",
        "attribution": "概念来源：《庄子》（庄周）。占位图待替换为公开版权庄子画像/水墨鲲鹏图。",
        "immutable_points": [
            "人物图为庄子传统形象，不得替换为现代人物",
            "鲲鹏意象可用水墨表现，但须为中国画风",
            "强调「逍遥」而非「自由」的西化翻译",
            "印章文字固定为「逍遥」"
        ]
    },
    "sunzibingfa": {
        "era": "春秋",
        "era_en": "Spring and Autumn",
        "visual_theme": "孙子·兵法竹简",
        "figure_image": "sunzi",
        "background_image": "bamboo_slip",
        "seal_text": "兵法",
        "font_family": "方正秦小篆 / Noto Serif SC",
        "color_primary": "#4a3a2a",
        "color_secondary": "#c4a76a",
        "attribution": "概念来源：《孙子兵法》（孙武）。占位图待替换为公开版权孙子画像/竹简图像。",
        "immutable_points": [
            "人物图为孙武传统形象，着春秋战袍",
            "背景使用竹简或帛书质感",
            "核心章句「上兵伐谋」等不得改写",
            "印章文字固定为「兵法」"
        ]
    },
    "zengshiqiang": {
        "era": "当代",
        "era_en": "Contemporary",
        "visual_theme": "曾仕强·中国式管理",
        "figure_image": "zengshiqiang",
        "background_image": "modern_bg",
        "seal_text": "圆通",
        "font_family": "方正楷体 / Noto Serif SC",
        "color_primary": "#2f3a4a",
        "color_secondary": "#d4af37",
        "attribution": "概念来源：曾仕强教授《中国式管理》《易经的奥秘》等。占位图待替换为公开版权照片。",
        "immutable_points": [
            "人物图须为曾仕强教授真实肖像（待替换）",
            "视觉风格保持现代中式，不混入日韩元素",
            "核心术语「圆通」须与「圆滑」严格区分",
            "印章文字固定为「圆通」"
        ]
    },
    "liushisigua": {
        "era": "周·先秦",
        "era_en": "Zhou / Pre-Qin",
        "visual_theme": "六十四卦·伏羲文王",
        "figure_image": "fuxi",
        "background_image": "i_ching",
        "seal_text": "六十四卦",
        "font_family": "方正金文大篆 / Noto Serif SC",
        "color_primary": "#2b0a0a",
        "color_secondary": "#d4af37",
        "attribution": "概念来源：《周易》六十四卦。占位图待替换为公开版权卦象图/画像。",
        "immutable_points": [
            "六十四卦排列须符合传统卦序（如文王卦序或先天卦序，页面须注明）",
            "每卦六爻绘制规范同易经章节",
            "不得随意改动卦名与卦象对应关系",
            "印章文字固定为「六十四卦」"
        ]
    },
    "chanzong": {
        "era": "南北朝至隋唐",
        "era_en": "Northern and Southern Dynasties to Tang",
        "visual_theme": "达摩·禅宗·不立文字",
        "figure_image": "chan_figure",
        "background_image": "chan_bg",
        "seal_text": "禅",
        "font_family": "方正行書 / Noto Serif SC",
        "color_primary": "#4a3a2a",
        "color_secondary": "#f4f1ea",
        "attribution": "概念来源：禅宗经典与公案。占位图待替换为公开版权达摩/禅宗图像。",
        "immutable_points": [
            "禅宗配图须为中国禅画风格，不得混入日本禅（Zen）商业符号",
            "达摩形象须为传统壁观/一苇渡江造型",
            "强调「不立文字」的宗风",
            "印章文字固定为「禅」"
        ]
    },
    "shufa": {
        "era": "全朝代（商周至今）",
        "era_en": "All Dynasties",
        "visual_theme": "书法·笔墨心法",
        "figure_image": "calligraphy",
        "background_image": "ink_wash",
        "seal_text": "書法",
        "font_family": "方正顏體 / 书体坊颜体",
        "color_primary": "#1a1a1a",
        "color_secondary": "#f7f3e8",
        "attribution": "概念来源：中国书法史（篆隶楷行草）。占位图待替换为公开版权书法作品图像。",
        "immutable_points": [
            "书法示例须使用真实书体，不得用艺术字冒充",
            "五种书体排序：篆、隶、楷、行、草",
            "强调「字如其人」的传统书论",
            "印章文字固定为「書法」"
        ]
    },
    "jieqi": {
        "era": "先秦定型·沿用至今",
        "era_en": "Pre-Qin codified, used ever since",
        "visual_theme": "二十四节气·太阳历",
        "figure_image": "seasons_bg",
        "background_image": "seasons_bg",
        "seal_text": "节气",
        "font_family": "方正清刻本悦宋 / Noto Serif SC",
        "color_primary": "#3a5a2a",
        "color_secondary": "#d4af37",
        "attribution": "概念来源：《淮南子·时则训》《礼记·月令》。占位图待替换为公开版权节气图像。",
        "immutable_points": [
            "二十四节气顺序固定，不可调换",
            "节气与公历日期对照须准确",
            "不得用西方四季划分替代中国节气",
            "印章文字固定为「节气」"
        ]
    },
    "chachan": {
        "era": "唐·宋",
        "era_en": "Tang / Song",
        "visual_theme": "茶道·茶禅一味",
        "figure_image": "tea_ceremony",
        "background_image": "ink_wash",
        "seal_text": "茶禪",
        "font_family": "方正楷体 / Noto Serif SC",
        "color_primary": "#2f5544",
        "color_secondary": "#d4af37",
        "attribution": "概念来源：中国茶文化、禅宗公案。占位图待替换为公开版权茶道图像。",
        "immutable_points": [
            "茶道须呈现中国茶法（唐煎茶/宋点茶/明清泡茶），不得用日本茶道替代",
            "核心术语「和敬清寂」须注明中国源流",
            "人物服饰须符合唐宋风格",
            "印章文字固定为「茶禪」"
        ]
    }
}


def main():
    data = json.loads(CHAPTER_FILE.read_text(encoding="utf-8"))
    reg = load_registry()
    assets = reg.setdefault("assets", {})

    # 生成额外占位图
    for key, info in EXTRA_SVGS.items():
        local_path = write_svg(key, info)
        if key not in assets:
            assets[key] = {
                "local": local_path,
                "status": "placeholder",
                "topic_zh": info["zh"],
                "category": info["cat"],
                "source_url": "",
                "license": "placeholder",
                "attribution": "龍魂占位生成器",
                "width": 800 if info["cat"] == "backgrounds" else 400,
                "height": 600 if info["cat"] == "backgrounds" else (500 if info["cat"] == "figures" else 400),
                "dna": DNA
            }
            log_change("生成占位素材", local_path, f"为章节视觉扩展新增 {key} 占位图")

    # 为每章注入不动点字段
    for ch in data["chapters"]:
        cid = ch["id"]
        cfg = CHAPTER_CONFIG.get(cid, {})
        if not cfg:
            continue

        figure_key = cfg["figure_image"]
        bg_key = cfg["background_image"]

        ch["era"] = cfg["era"]
        ch["era_en"] = cfg["era_en"]
        ch["visual_theme"] = cfg["visual_theme"]
        ch["figure_image"] = {
            "asset_key": figure_key,
            "local": assets.get(figure_key, {}).get("local", ""),
            "status": assets.get(figure_key, {}).get("status", "placeholder"),
            "alt": cfg["visual_theme"].split("·")[0] + "配图"
        }
        ch["background_image"] = {
            "asset_key": bg_key,
            "local": assets.get(bg_key, {}).get("local", ""),
            "status": assets.get(bg_key, {}).get("status", "placeholder"),
            "alt": cfg["visual_theme"].split("·")[-1] + "背景"
        }
        ch["seal_text"] = cfg["seal_text"]
        ch["font_family"] = cfg["font_family"]
        ch["color_primary"] = cfg["color_primary"]
        ch["color_secondary"] = cfg["color_secondary"]
        ch["attribution"] = cfg["attribution"]
        ch["immutable_points"] = cfg["immutable_points"]
        ch["visual_anchor_dna"] = new_dna(cid.upper())
        ch["change_log"] = [{
            "timestamp": ts(),
            "action": "注入视觉不动点字段",
            "dna": DNA,
            "note": f"为 {cid} 配置 era、visual_theme、figure_image、background_image、seal_text 等字段"
        }]

    # 更新 metadata
    data["metadata"]["version"] = "v1.1"
    data["metadata"]["updated_at"] = ts()
    data["metadata"]["visual_anchor_dna"] = DNA
    data["metadata"]["visual_chapters_count"] = len(data["chapters"])
    data["metadata"]["placeholder_assets_count"] = sum(1 for a in assets.values() if a.get("status") == "placeholder")
    data["metadata"]["real_assets_count"] = sum(1 for a in assets.values() if a.get("status") != "placeholder")

    CHAPTER_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    save_registry(reg)
    log_change("扩展章节数据", str(CHAPTER_FILE), f"为 {len(data['chapters'])} 章注入视觉不动点字段，当前占位素材 {data['metadata']['placeholder_assets_count']} 个")

    print(f"✅ 已扩展 {len(data['chapters'])} 章视觉不动点")
    print(f"🎨 占位素材总数: {len(assets)}，其中占位 {data['metadata']['placeholder_assets_count']} 个")
    print(f"📁 章节文件: {CHAPTER_FILE}")
    print(f"📁 注册表: {REGISTRY}")
    print(f"🧬 {DNA}")


if __name__ == "__main__":
    main()
