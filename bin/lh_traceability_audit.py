#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·AI可追溯性审计协议执行器 v1.0
对应协议: 01_protocols/LH-UID9622-...-AI-Traceability-Audit-Protocol-v1.0.md
职能: DNA生成/校验、七因子行为密码学、信用评分、模式识别、三色审计。
DNA: #LongHun⚡️BingWu·GuiWei·JiaZi·ZiShi·䷾JiJi-AI-TRACEABILITY-AUDIT-v1.0
"""

import argparse
import hashlib
import json
import math
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
DNA = "#LongHun⚡️BingWu·GuiWei·JiaZi·ZiShi·䷾JiJi-AI-TRACEABILITY-AUDIT-v1.0"

TIAN_GAN = "甲乙丙丁戊己庚辛壬癸"
DI_ZHI = "子丑寅卯辰巳午未申酉戌亥"
SHI_CHEN = ["子时", "丑时", "寅时", "卯时", "辰时", "巳时",
            "午时", "未时", "申时", "酉时", "戌时", "亥时"]

HEXAGRAMS = {
    "乾": "䷀", "坤": "䷁", "屯": "䷂", "蒙": "䷃", "需": "䷄", "讼": "䷅",
    "师": "䷆", "比": "䷇", "小畜": "䷈", "履": "䷉", "泰": "䷊", "否": "䷋",
    "同人": "䷌", "大有": "䷍", "谦": "䷎", "豫": "䷏", "随": "䷐", "蛊": "䷑",
    "临": "䷒", "观": "䷓", "噬嗑": "䷔", "贲": "䷕", "剥": "䷖", "复": "䷗",
    "无妄": "䷘", "大畜": "䷙", "颐": "䷚", "大过": "䷛", "坎": "䷜", "离": "䷝",
    "咸": "䷞", "恒": "䷟", "遁": "䷠", "大壮": "䷡", "晋": "䷢", "明夷": "䷣",
    "家人": "䷤", "睽": "䷥", "蹇": "䷦", "解": "䷧", "损": "䷨", "益": "䷩",
    "夬": "䷪", "姤": "䷫", "萃": "䷬", "升": "䷭", "困": "䷮", "井": "䷯",
    "革": "䷰", "鼎": "䷱", "震": "䷲", "艮": "䷳", "渐": "䷴", "归妹": "䷵",
    "丰": "䷶", "旅": "䷷", "巽": "䷸", "兑": "䷹", "涣": "䷺", "节": "䷻",
    "中孚": "䷼", "小过": "䷽", "既济": "䷾", "未济": "䷿",
}

DOMAIN_HEXAGRAM = {
    "CODEBUDDY": "乾", "GOVERNANCE": "乾", "CONSTITUTION": "乾", "RULES": "乾", "NAMING": "乾",
    "TRUST": "兑", "ECOM": "兑", "REGISTER": "兑",
    "AUDIT": "离", "MATH": "离", "DASHBOARD": "离", "STATE": "离", "TEST": "离",
    "SECURITY": "震", "GUARD": "震", "MINOR": "震", "ALARM": "震", "DNA": "震", "MELTDOWN": "震",
    "PERSONA": "巽", "ROUTE": "巽", "DEPLOY": "巽", "TRAIN": "巽", "MODEL": "巽",
    "ENGINE": "坎", "CRAWLER": "坎", "STREAM": "坎", "SYNC": "坎", "TAIJI": "坎",
    "SOVEREIGNTY": "艮", "PRIVACY": "艮", "GATE": "艮",
    "ARCHIVE": "坤", "BACKUP": "坤", "MEMORY": "坤", "DATA": "坤",
}


def _now_cst() -> datetime:
    return datetime.now(timezone(timedelta(hours=8)))


def _stem_branch(dt: datetime) -> Tuple[str, str, str]:
    y, m, d, h = dt.year, dt.month, dt.day, dt.hour
    year_gan = TIAN_GAN[(y - 4) % 10]
    year_zhi = DI_ZHI[(y - 4) % 12]
    # 简化月干支：以年干支推正月，再平推
    month_gan = TIAN_GAN[((y - 4) % 10 + 2 + m) % 10]
    month_zhi = DI_ZHI[(2 + m) % 12]  # 寅月为正月
    # 日干支简化公式
    yy = y % 100
    base = ((yy + 7) * 5 + 15 + (yy + 19) // 4) % 60
    month_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0):
        month_days[2] = 29
    day_of_year = sum(month_days[:m]) + d
    seq = (base + day_of_year) % 60
    day_gan = TIAN_GAN[(seq - 1) % 10]
    day_zhi = DI_ZHI[(seq - 1) % 12]
    shichen = SHI_CHEN[((h + 1) // 2) % 12]
    return f"{year_gan}{year_zhi}", f"{month_gan}{month_zhi}", f"{day_gan}{day_zhi}", shichen


def _choose_hexagram(module: str) -> str:
    for key, hx in DOMAIN_HEXAGRAM.items():
        if key in module.upper():
            return hx
    # 默认按哈希选
    idx = int(hashlib.sha256(module.encode()).hexdigest(), 16) % 64
    return list(HEXAGRAMS.keys())[idx]


def generate_dna(module: str, action: str, version: str = "V1.0") -> str:
    dt = _now_cst()
    year, month, day, shichen = _stem_branch(dt)
    hx = _choose_hexagram(module)
    hx_symbol = HEXAGRAMS[hx]
    body = f"{year}·{month}·{day}·{shichen}·{hx_symbol}{hx}-{module}-{action}-{version}"
    base = f"#LongHun⚡️{body}|{dt.isoformat()}"
    hash8 = hashlib.sha256(base.encode("utf-8")).hexdigest()[:8]
    return f"#LongHun⚡️{body}-{hash8}"


def validate_dna(dna: str) -> Dict:
    # 允许干支、时辰为中文；卦象为符号+中文；模块/动作/版本为ASCII
    pattern = r"^#LongHun⚡️([\u4e00-\u9fff]+)·([\u4e00-\u9fff]+)·([\u4e00-\u9fff]+)·([\u4e00-\u9fff]+)·([䷀-䷿][\u4e00-\u9fff]+)-([A-Z][A-Z0-9-]*)-([A-Z][A-Z0-9-]*)-(V\d+\.\d+)-([a-f0-9]{8})$"
    m = re.match(pattern, dna)
    checks = {
        "prefix": dna.startswith("#LongHun⚡️"),
        "regex": m is not None,
        "hexagram": False,
        "version": False,
        "hash8": False,
    }
    if m:
        hex_part = m.group(5)
        checks["hexagram"] = any(hex_part.startswith(v) for v in HEXAGRAMS.values())
        ver = m.group(8)
        checks["version"] = re.match(r"V\d+\.\d+", ver) is not None
        checks["hash8"] = len(m.group(9)) == 8
    valid = all(checks.values())
    return {"valid": valid, "checks": checks, "dna": dna}


# ── 七因子行为密码学 ──
FACTOR_WEIGHTS = {
    "P": 0.15, "F": 0.20, "T": 0.10, "E": 0.15,
    "C": 0.05, "R": 0.10, "A": 0.15, "X": 0.05, "Y": 0.05,
}


def _factor_value(label: str, value) -> float:
    if label == "F":
        return 1.0 if value == "Fulfilled" else (0.5 if value == "Partial" else 0.0)
    if label == "T":
        return 1.0 if value < 0 else max(0.0, 1.0 - 0.1 * value)
    if label == "E":
        return {"Willing": 1.0, "Genuine": 0.9, "Perfunctory": 0.5,
                "Resentful": 0.2, "Numb": 0.2, "Indifferent": 0.3}.get(value, 0.5)
    if label == "C":
        return 1.0 if value > 0 else 0.5
    if label == "R":
        return max(0.0, 1.0 - value * 0.2)
    if label == "A":
        return {"Partner": 1.5, "Family": 1.2, "Self": 1.0,
                "Outsider": -1.0, "Public": -1.0}.get(value, 1.0)
    if label == "X":
        return {"Genuine": 1.0, "Silent": 0.7, "Indifferent": 0.4,
                "OverExplain": 0.3}.get(value, 0.5)
    if label == "Y":
        return {"Changed": 1.0, "Resisted": 0.3, "Indifferent": 0.2,
                "NoResponse": 0.0}.get(value, 0.5)
    if label == "P":
        return 1.0 if value == "HasPromise" else 0.6
    return 0.5


def compute_credit(seven_factors: Dict[str, any]) -> Dict:
    """单事件信用评分"""
    f = _factor_value("F", seven_factors.get("F", "Unfulfilled"))
    t_raw = seven_factors.get("T", 0)
    if t_raw < 0:
        time_bonus = 1.5
    else:
        time_bonus = max(0.1, 1.0 - 0.3 * t_raw)
    e = _factor_value("E", seven_factors.get("E", "Numb"))
    c = _factor_value("C", seven_factors.get("C", 0))
    r = max(0.0, 1.0 - seven_factors.get("R", 0) * 0.5)
    a = _factor_value("A", seven_factors.get("A", "Self"))
    score = f * time_bonus * e * c * r * a
    score = max(-10.0, min(10.0, score))
    return {
        "score": round(score, 4),
        "factors": seven_factors,
        "components": {
            "fulfillment": f, "time_bonus": time_bonus,
            "emotion": e, "cost": c, "repeat_penalty": r, "audience": a,
        },
    }


def detect_pattern(seven_factors: Dict[str, any]) -> str:
    f = seven_factors.get("F", "")
    x = seven_factors.get("X", "")
    y = seven_factors.get("Y", "")
    z = seven_factors.get("Z", 0.0)
    a = seven_factors.get("A", "")
    if f == "Unfulfilled" and x == "OverExplain":
        return "MODE-DefensiveDefaulter"
    if f == "Fulfilled" and a in ("Outsider", "Public"):
        return "MODE-ExternalTrustSpender"
    if f == "Unfulfilled" and y == "Indifferent":
        return "MODE-InternalDestroyer"
    if isinstance(z, (int, float)) and z > 2:
        return "MODE-Fluctuating"
    return "MODE-StableDisciplined"


def tri_color_audit(score: float) -> str:
    if score >= 0.85:
        return "🟢"
    if score >= 0.6:
        return "🟡"
    return "🔴"


def seven_factor_confidence(factors: List[float]) -> Dict:
    weights = [0.25, 0.15, 0.15, 0.15, 0.10, 0.12, 0.08]
    conf = 1.0
    for f, w in zip(factors, weights):
        conf *= max(0.01, f) ** w
    return {"confidence": round(conf, 4), "weights": weights}


def _self_test():
    print("=" * 50)
    print("龍魂·AI可追溯性审计协议执行器自检")
    print("=" * 50)

    dna = generate_dna("AUDIT", "TEST", "V1.0")
    print(f"  生成DNA: {dna}")
    v = validate_dna(dna)
    assert v["valid"], v
    print("  ✅ DNA 生成与校验通过")

    bad = validate_dna("#LongHun⚡️BadDNA")
    assert not bad["valid"]
    print("  ✅ 非法DNA被拒绝")

    factors = {
        "P": "HasPromise", "F": "Fulfilled", "T": -2,
        "E": "Willing", "C": 120, "R": 0,
        "A": "Partner", "X": "Genuine", "Y": "Changed", "Z": 1.0,
    }
    credit = compute_credit(factors)
    print(f"  信用评分: {credit['score']} {tri_color_audit(credit['score'])}")
    pattern = detect_pattern(factors)
    print(f"  行为模式: {pattern}")

    conf = seven_factor_confidence([0.9, 0.8, 0.85, 0.7, 0.9, 0.8, 0.75])
    print(f"  七因子置信度: {conf['confidence']}")

    print("🟢 可追溯性审计自检全部通过")


def main():
    parser = argparse.ArgumentParser(description="龍魂·AI可追溯性审计协议执行器")
    parser.add_argument("--self-test", action="store_true", help="自检")
    parser.add_argument("--generate-dna", metavar="MODULE", help="生成DNA")
    parser.add_argument("--action", default="ACTION", help="DNA动作")
    parser.add_argument("--version", default="V1.0", help="版本")
    parser.add_argument("--validate-dna", metavar="DNA", help="校验DNA")
    parser.add_argument("--credit", help="七因子JSON文件或字符串")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    args = parser.parse_args()

    if args.self_test:
        _self_test()
        return

    if args.generate_dna:
        dna = generate_dna(args.generate_dna, args.action, args.version)
        print(dna)
    elif args.validate_dna:
        r = validate_dna(args.validate_dna)
        print(json.dumps(r, ensure_ascii=False, indent=2))
    elif args.credit:
        data = json.loads(Path(args.credit).read_text(encoding="utf-8") if Path(args.credit).exists() else args.credit)
        r = compute_credit(data)
        r["pattern"] = detect_pattern(data)
        r["color"] = tri_color_audit(r["score"])
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
