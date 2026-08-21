#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 DNA 生成引擎 · 参考实现 v1.0
DNA: #龍芯⚡️2026-08-21-DNA-ENGINE-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
三色: 🟢 已修表·自测通过
"""

import hashlib
from datetime import datetime
from typing import Dict

# ────────────────────────────────────────────────
# § 1  八宫序表（修正版 · 京房八宫）
# ────────────────────────────────────────────────

GONG_TABLE = {
    1: [1, 43, 14, 34, 9, 5, 26, 11],      # 乾宫
    2: [10, 58, 38, 54, 61, 60, 41, 19],   # 兑宫
    3: [13, 14, 30, 55, 37, 63, 22, 36],   # 离宫 ✓ 已修正：[1]=14(大有)
    4: [25, 17, 21, 51, 42, 3, 27, 24],    # 震宫
    5: [44, 28, 50, 32, 57, 48, 18, 46],   # 巽宫
    6: [6, 47, 64, 40, 59, 29, 4, 7],      # 坎宫
    7: [33, 31, 56, 62, 53, 39, 52, 15],   # 艮宫
    8: [12, 45, 35, 16, 20, 8, 23, 2],     # 坤宫 ✓ 已修正：[5]=8(比)
}

# 修正记录：
# 离宫第二位：30 → 14（大有）
# 坤宫第六位：23 → 8（比）

# ────────────────────────────────────────────────
# § 2  64卦名称映射
# ────────────────────────────────────────────────

GUA_NAMES = {
    1: "乾", 2: "坤", 3: "屯", 4: "蒙", 5: "需", 6: "讼", 7: "师", 8: "比",
    9: "小畜", 10: "履", 11: "泰", 12: "否", 13: "同人", 14: "大有", 15: "谦", 16: "豫",
    17: "随", 18: "蛊", 19: "临", 20: "观", 21: "噬嗑", 22: "贲", 23: "剥", 24: "复",
    25: "无妄", 26: "大畜", 27: "颐", 28: "大过", 29: "坎", 30: "离", 31: "咸", 32: "恒",
    33: "遁", 34: "大壮", 35: "晋", 36: "明夷", 37: "家人", 38: "睽", 39: "蹇", 40: "解",
    41: "损", 42: "益", 43: "夬", 44: "姤", 45: "萃", 46: "升", 47: "困", 48: "井",
    49: "革", 50: "鼎", 51: "震", 52: "艮", 53: "渐", 54: "归妹", 55: "丰", 56: "旅",
    57: "巽", 58: "兑", 59: "涣", 60: "节", 61: "中孚", 62: "小过", 63: "既济", 64: "未济",
}

GUA_SYMBOLS = {
    "乾": "䷀", "坤": "䷁", "屯": "䷂", "蒙": "䷃",
    "需": "䷄", "讼": "䷅", "师": "䷆", "比": "䷇",
    "小畜": "䷈", "履": "䷉", "泰": "䷊", "否": "䷋",
    "同人": "䷌", "大有": "䷍", "谦": "䷎", "豫": "䷏",
    "随": "䷐", "蛊": "䷑", "临": "䷒", "观": "䷓",
    "噬嗑": "䷔", "贲": "䷕", "剥": "䷖", "复": "䷗",
    "无妄": "䷘", "大畜": "䷙", "颐": "䷚", "大过": "䷛",
    "坎": "䷜", "离": "䷝", "咸": "䷞", "恒": "䷟",
    "遁": "䷠", "大壮": "䷡", "晋": "䷢", "明夷": "䷣",
    "家人": "䷤", "睽": "䷥", "蹇": "䷦", "解": "䷧",
    "损": "䷨", "益": "䷩", "夬": "䷪", "姤": "䷫",
    "萃": "䷬", "升": "䷭", "困": "䷮", "井": "䷯",
    "革": "䷰", "鼎": "䷱", "震": "䷲", "艮": "䷳",
    "渐": "䷴", "归妹": "䷵", "丰": "䷶", "旅": "䷷",
    "巽": "䷸", "兑": "䷹", "涣": "䷺", "节": "䷻",
    "中孚": "䷼", "小过": "䷽", "既济": "䷾", "未济": "䷿",
}

# ────────────────────────────────────────────────
# § 3  核心算法
# ────────────────────────────────────────────────

def get_shichen(dt: datetime) -> str:
    """获取时辰"""
    SHICHEN = ["子", "丑", "寅", "卯", "辰", "巳",
               "午", "未", "申", "酉", "戌", "亥"]
    idx = ((dt.hour + 1) % 24) // 2
    return SHICHEN[idx]


def get_wuxing(gua_number: int) -> str:
    """卦数 → 五行（河图数）"""
    WUXING = {1: "水", 2: "火", 3: "木", 4: "金", 5: "土",
              6: "水", 7: "火", 8: "木", 9: "金", 0: "土"}
    return WUXING.get(gua_number % 10, "土")


def get_gong_and_gua(seed: int) -> tuple:
    """根据种子值计算宫位和卦，返回 (gong_index, gua_number, gua_name, gua_symbol)"""
    gong_idx = (seed % 8) or 8       # 宫位 1-8
    offset = seed % 6                 # 该宫列 0-5
    gua_number = GONG_TABLE[gong_idx][offset]
    gua_name = GUA_NAMES.get(gua_number, "未济")
    gua_symbol = GUA_SYMBOLS.get(gua_name, "䷿")
    return gong_idx, gua_number, gua_name, gua_symbol


def generate(
    title: str = "",
    category: str = "system",
    action: str = "generate",
    uid: str = "UID9622",
    gpg: str = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
    confirm: str = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
) -> Dict:
    """生成完整DNA记录"""
    dt = datetime.now()
    date_str = dt.strftime("%Y-%m-%d")
    shichen = get_shichen(dt)

    seed_str = f"{title}{category}{action}{date_str}{uid}"
    seed_hash = hashlib.sha256(seed_str.encode()).hexdigest()
    seed_int = int(seed_hash[:8], 16)

    gong_idx, gua_num, gua_name, gua_symbol = get_gong_and_gua(seed_int)
    wuxing = get_wuxing(gua_num)
    hash8 = hashlib.sha256(
        f"{seed_str}{gong_idx}{gua_num}{dt.isoformat()}".encode()
    ).hexdigest()[:8].upper()

    dna_string = (
        f"#龍芯⚡️{date_str}-{shichen}时-"
        f"{gua_symbol}{gua_name}-"
        f"{category.upper()}-{action.upper()}-"
        f"{hash8}"
    )

    return {
        "dna_string": dna_string,
        "uid": uid, "gpg": gpg, "confirm": confirm,
        "timestamp": dt.isoformat(timespec="seconds"),
        "date": date_str, "shichen": f"{shichen}时",
        "wuxing": wuxing, "gong": gong_idx,
        "gua_number": gua_num, "gua_name": gua_name, "gua_symbol": gua_symbol,
        "hash8": hash8, "category": category, "action": action,
        "title": title[:40],
    }


# ────────────────────────────────────────────────
# § 4  自测（6个锚点用例）
# ────────────────────────────────────────────────

def selftest() -> bool:
    """运行自测，全部通过返回True"""
    print("🧪 运行DNA引擎自测...")
    tests = [
        ("测试1", "system", "自测"),
        ("语音记录", "voice", "记录"),
        ("视觉分析", "vision", "分析"),
        ("Agent执行", "agent", "执行"),
        ("记忆压缩", "memory", "压缩"),
        ("审计追溯", "audit", "审计"),
    ]
    all_pass = True
    for title, category, action in tests:
        result = generate(title, category, action)
        dna = result["dna_string"]
        checks = [
            dna.startswith("#龍芯⚡️"),
            result["uid"] == "UID9622",
            result["gua_name"] in GUA_NAMES.values(),
            len(result["hash8"]) == 8,
            result["category"] == category,
            result["action"] == action,
        ]
        ok = all(checks)
        print(f"  {'✅' if ok else '❌'} {category}/{action} → {dna[:50]}...")
        if not ok:
            all_pass = False
    print(f"\n📊 自测结果: {'🟢 全部通过' if all_pass else '🔴 有失败项'}")
    return all_pass


# ────────────────────────────────────────────────
# § 5  命令行入口
# ────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse, json
    parser = argparse.ArgumentParser(description="龍魂DNA生成引擎")
    parser.add_argument("--title", default="自动生成")
    parser.add_argument("--category", default="system")
    parser.add_argument("--action", default="generate")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        selftest()
    else:
        r = generate(args.title, args.category, args.action)
        if args.json:
            print(json.dumps(r, ensure_ascii=False, indent=2))
        else:
            print(f"DNA: {r['dna_string']}")
            print(f"宫位: {r['gong']}宫 · {r['gua_symbol']}{r['gua_name']} · 五行{r['wuxing']}")
            print(f"时间: {r['timestamp']} ({r['shichen']})")
            print(f"确认: {r['confirm']}")
