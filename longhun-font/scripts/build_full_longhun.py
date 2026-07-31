#!/usr/bin/env python3
# 龍魂·LonghunFont 全量构建脚本 v2.0
# DNA: #龍芯⚡️丙午·乙申·FULLFONT-v2.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 目标：生成全 CJK 统一汉字区(20902字) + 拉丁/数字/符号 + 文化符号
# 直接算法生成，不依赖外部 LFS 文件

import json
import sys
import time
import os
from pathlib import Path
from datetime import datetime
from typing import Any

# 添加当前目录到 sys.path
sys.path.insert(0, str(Path(__file__).parent))

from glyph_generator import generate_skeleton, structure_of

DNA = "#龍芯⚡️丙午·乙申·FULLFONT-v2.0"

# --- 拉丁字母 + 数字 + 基础符号 ---
LATIN_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
BASIC_SYMBOLS = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
# 全角标点
FULLWIDTH_SYMBOLS = "，。！？；：""''（）【】《》—…～·、"

# 文化符号（Unicode PUA 映射用占位符）
CULTURE_SYMBOLS = {
    "☯": "太极",
    "☰": "乾",
    "☱": "兑",
    "☲": "离",
    "☳": "震",
    "☴": "巽",
    "☵": "坎",
    "☶": "艮",
    "☷": "坤",
    "金": "五行金",
    "木": "五行木",
    "水": "五行水",
    "火": "五行火",
    "土": "五行土",
    "甲": "天干甲",
    "乙": "天干乙",
    "丙": "天干丙",
    "丁": "天干丁",
    "戊": "天干戊",
    "己": "天干己",
    "庚": "天干庚",
    "辛": "天干辛",
    "壬": "天干壬",
    "癸": "天干癸",
    "子": "地支子",
    "丑": "地支丑",
    "寅": "地支寅",
    "卯": "地支卯",
    "辰": "地支辰",
    "巳": "地支巳",
    "午": "地支午",
    "未": "地支未",
    "申": "地支申",
    "酉": "地支酉",
    "戌": "地支戌",
    "亥": "地支亥",
    "春": "节气春",
    "夏": "节气夏",
    "秋": "节气秋",
    "冬": "节气冬",
    "日": "日月",
    "月": "日月",
    "星": "星宿",
    "龍": "龙魂",
    "魂": "龙魂",
    "中": "中国",
    "国": "中国",
    "制": "制造",
    "造": "制造",
}


def simple_latin_skeleton(code_point: int) -> list:
    """生成简单拉丁骨架（大写7笔画H型，小写略小）"""
    char = chr(code_point)
    if 'A' <= char <= 'Z':
        return [
            ["移动到", 200, 160], ["直线段", 200, 580],
            ["移动到", 200, 400], ["直线段", 500, 400],
            ["移动到", 500, 160], ["直线段", 500, 580],
            ["移动到", 200, 160], ["直线段", 500, 160],
            ["移动到", 200, 580], ["直线段", 500, 580],
        ]
    elif 'a' <= char <= 'z':
        return [
            ["移动到", 220, 200], ["直线段", 220, 500],
            ["移动到", 220, 360], ["直线段", 460, 360],
            ["移动到", 460, 200], ["直线段", 460, 500],
            ["移动到", 220, 500], ["直线段", 460, 500],
        ]
    elif '0' <= char <= '9':
        return [
            ["移动到", 180, 160], ["直线段", 180, 580],
            ["移动到", 520, 160], ["直线段", 520, 580],
            ["移动到", 180, 160], ["直线段", 520, 160],
            ["移动到", 180, 580], ["直线段", 520, 580],
            ["移动到", 180, 370], ["直线段", 520, 370],
        ]
    elif char == ' ':
        return []  # 空格无字形
    else:
        return [
            ["移动到", 260, 200], ["直线段", 260, 560],
            ["移动到", 440, 200], ["直线段", 440, 560],
        ]


def symbol_skeleton(char: str) -> list:
    """符号简单骨架"""
    code = ord(char)
    # 全角标点
    if 0x3000 <= code <= 0x303F or 0xFF00 <= code <= 0xFFEF:
        return [
            ["移动到", 250, 300], ["直线段", 450, 300],
            ["移动到", 250, 450], ["直线段", 450, 450],
        ]
    if char in FULLWIDTH_SYMBOLS:
        return [
            ["移动到", 280, 320], ["直线段", 480, 320],
            ["移动到", 350, 260], ["直线段", 350, 500],
        ]
    # 基础 ASCII 符号
    return [
        ["移动到", 260, 260], ["直线段", 440, 260],
        ["移动到", 260, 440], ["直线段", 440, 440],
    ]


def main():
    print(f"🐉 龍魂全量字体构建 v2.0")
    print(f"DNA: {DNA}")
    print()

    base_dir = Path(__file__).parent.parent
    output_dir = base_dir / "output"
    glyphs_dir = base_dir / "glyphs"
    output_dir.mkdir(exist_ok=True)
    glyphs_dir.mkdir(exist_ok=True)

    char_data = {}
    stats = {"cjk": 0, "latin": 0, "symbol": 0, "culture": 0}
    total_planned = 20902 + len(LATIN_CHARS) + len(BASIC_SYMBOLS) + len(FULLWIDTH_SYMBOLS) + len(CULTURE_SYMBOLS)

    print(f"📐 计划生成字符数: 约 {total_planned}")
    print(f"   - CJK 统一汉字 (U+4E00~U+9FFF): 20902 字")
    print(f"   - 拉丁/数字: {len(LATIN_CHARS)} 字")
    print(f"   - 基础符号: {len(BASIC_SYMBOLS)} 字")
    print(f"   - 全角标点: {len(FULLWIDTH_SYMBOLS)} 字")
    print(f"   - 文化符号: {len(CULTURE_SYMBOLS)} 字")
    print()

    # --- 阶段1: 生成全部 CJK 汉字 ---
    print("【阶段 1/4】生成 CJK 统一汉字 20902 字...")
    t_start = time.time()
    done = 0
    batch_start = time.time()

    for code in range(0x4E00, 0x9FFF + 1):
        char = chr(code)
        try:
            skeleton = generate_skeleton(char)
            char_data[char] = {
                "笔画路径_cnsh9622": skeleton,
                "结构": structure_of(char),
                "码位": code,
                "来源": "算法生成",
                "DNA": DNA,
            }
            stats["cjk"] += 1
        except Exception as e:
            # 某些极端罕见字可能生成失败，用简单骨架填充
            char_data[char] = {
                "笔画路径_cnsh9622": [
                    ["移动到", 120, 120], ["直线段", 480, 480],
                    ["移动到", 480, 120], ["直线段", 120, 480],
                    ["移动到", 120, 120], ["直线段", 480, 120],
                    ["移动到", 120, 480], ["直线段", 480, 480],
                ],
                "结构": "单一",
                "码位": code,
                "来源": "填充骨架",
                "DNA": DNA,
            }
            stats["cjk"] += 1

        done += 1
        if done % 1000 == 0:
            elapsed = time.time() - batch_start
            total_elapsed = time.time() - t_start
            rate = 1000 / elapsed if elapsed > 0 else 0
            eta = (20902 - done) / rate if rate > 0 else 0
            print(f"  {done}/{20902} ({done*100//20902}%) | 速度: {rate:.0f} 字/秒 | 已耗时: {total_elapsed:.0f}s | 预计剩余: {eta:.0f}s")
            batch_start = time.time()

    t_cjk = time.time() - t_start
    print(f"  ✅ CJK 完成: {stats['cjk']} 字 | 耗时: {t_cjk:.1f}s")

    # --- 阶段2: 生成拉丁字母/数字 ---
    print("\n【阶段 2/4】生成拉丁字母/数字...")
    for char in LATIN_CHARS:
        skeleton = simple_latin_skeleton(ord(char))
        char_data[char] = {
            "笔画路径_cnsh9622": skeleton,
            "结构": "拉丁",
            "码位": ord(char),
            "来源": "算法生成",
            "DNA": DNA,
        }
        stats["latin"] += 1
    print(f"  ✅ 拉丁/数字: {stats['latin']} 字")

    # --- 阶段3: 生成符号 ---
    print("\n【阶段 3/4】生成符号...")
    for char in BASIC_SYMBOLS:
        skeleton = symbol_skeleton(char)
        char_data[char] = {
            "笔画路径_cnsh9622": skeleton,
            "结构": "符号",
            "码位": ord(char),
            "来源": "算法生成",
            "DNA": DNA,
        }
        stats["symbol"] += 1

    for char in FULLWIDTH_SYMBOLS:
        skeleton = symbol_skeleton(char)
        char_data[char] = {
            "笔画路径_cnsh9622": skeleton,
            "结构": "全角标点",
            "码位": ord(char),
            "来源": "算法生成",
            "DNA": DNA,
        }
        stats["symbol"] += 1
    print(f"  ✅ 符号: {stats['symbol']} 字")

    # --- 阶段4: 文化符号 ---
    print("\n【阶段 4/4】生成文化符号...")
    for char, desc in CULTURE_SYMBOLS.items():
        # 这些是已有 CJK 汉字，重用其骨架
        if char in char_data:
            char_data[char]["文化属性"] = desc
            stats["culture"] += 1
        else:
            skeleton = generate_skeleton(char) if ord(char) >= 0x4E00 else [
                ["移动到", 200, 200], ["直线段", 500, 500],
                ["移动到", 200, 500], ["直线段", 500, 200],
            ]
            char_data[char] = {
                "笔画路径_cnsh9622": skeleton,
                "结构": "文化符号",
                "码位": ord(char),
                "来源": "算法生成",
                "DNA": DNA,
                "文化属性": desc,
            }
            stats["culture"] += 1
    print(f"  ✅ 文化符号: {stats['culture']} 字")

    # --- 构建 JSON 字元库 ---
    total_chars = sum(stats.values())
    print(f"\n📦 总计字符数: {total_chars}")
    print(f"📦 写入 JSON 字元库...")

    font_data = {
        "元数据": {
            "名称": "LonghunFont-Regular-Full",
            "版本": "v0020",
            "DNA追溯码": DNA,
            "创建时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "创建者": "UID9622 · 龍芯北辰",
            "许可证": "SIL Open Font License 1.1",
            "描述": "龍魂全量中文字体 · 20902 CJK 统一汉字",
            "统计": {
                "总字符数": total_chars,
                "CJK汉字": stats["cjk"],
                "拉丁数字": stats["latin"],
                "符号": stats["symbol"],
                "文化符号": stats["culture"],
            },
        },
        "字符集_cnsh9622": char_data,
    }

    json_path = glyphs_dir / "龍魂字元库_v0020_full_cjk.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(font_data, f, ensure_ascii=False, indent=2)
    json_size_mb = os.path.getsize(json_path) / (1024 * 1024)
    print(f"  ✅ JSON 字元库: {json_path}")
    print(f"  📏 文件大小: {json_size_mb:.1f} MB")

    # --- 构建 OTF ---
    print(f"\n🔨 构建 OTF 字体文件...")
    from build_font import build_otf

    otf_path = output_dir / "LonghunFont-Regular-v0020.otf"
    try:
        build_otf(str(json_path), str(otf_path))
        otf_size_mb = os.path.getsize(otf_path) / (1024 * 1024)
        print(f"  ✅ OTF 字体: {otf_path}")
        print(f"  📏 文件大小: {otf_size_mb:.1f} MB")
    except Exception as e:
        print(f"  ❌ OTF 构建失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

    # --- 摘要 ---
    print(f"\n{'='*60}")
    print(f"🐉 龍魂全量字体 v0020 构建完成")
    print(f"{'='*60}")
    print(f"  总字符数: {total_chars}")
    print(f"  CJK 统一汉字: {stats['cjk']} 字")
    print(f"  拉丁/数字:   {stats['latin']} 字")
    print(f"  符号:        {stats['symbol']} 字")
    print(f"  文化符号:    {stats['culture']} 字")
    print(f"  JSON: {json_path} ({json_size_mb:.1f} MB)")
    print(f"  OTF:  {otf_path} ({otf_size_mb:.1f} MB)")
    print(f"  DNA:  {DNA}")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
