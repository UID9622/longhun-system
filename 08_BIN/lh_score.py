#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·LU-SYSTEM-SCORE 评分引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·癸亥·亥时·䷢晋-LU-SYSTEM-SCORE-v1.0-A3D7F2E1
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

五维加权评分系统（LU原版迁移至CNSH）:
- 创意触发 28% · 人格联动 20% · 结构搭建 22% · 系统推进 25% · 表达影响力 5%
- 主评分人格: 雯雯(P03)
"""

import sys
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# ============================================================
# 五维权重（LU原始定义）
# ============================================================
WEIGHTS = {
    "creative_trigger": 0.28,   # 创意触发
    "persona_linkage": 0.20,    # 人格联动
    "structure_build": 0.22,    # 结构搭建
    "system_push": 0.25,        # 系统推进
    "expression_impact": 0.05,  # 表达影响力
}

WEIGHT_LABELS = {
    "creative_trigger": "创意触发",
    "persona_linkage": "人格联动",
    "structure_build": "结构搭建",
    "system_push": "系统推进",
    "expression_impact": "表达影响力",
}

# ============================================================
# 评分函数
# ============================================================
def score_system(
    creative: float = 5.0,
    persona: float = 5.0,
    structure: float = 5.0,
    push: float = 5.0,
    expression: float = 5.0,
    notes: str = ""
) -> Dict:
    """五维加权评分
    
    Args:
        creative: 创意触发 0-10
        persona: 人格联动 0-10
        structure: 结构搭建 0-10
        push: 系统推进 0-10
        expression: 表达影响力 0-10
        notes: 备注
    
    Returns:
        评分结果字典
    """
    scores = {
        "creative_trigger": min(max(creative, 0), 10),
        "persona_linkage": min(max(persona, 0), 10),
        "structure_build": min(max(structure, 0), 10),
        "system_push": min(max(push, 0), 10),
        "expression_impact": min(max(expression, 0), 10),
    }
    
    total = 0.0
    details = {}
    for key, weight in WEIGHTS.items():
        s = scores[key] * weight
        total += s
        details[key] = {
            "label": WEIGHT_LABELS[key],
            "raw": scores[key],
            "weight": weight,
            "weighted": round(s, 2),
        }
    
    total = round(total, 2)
    
    # 等级判定
    if total >= 8.5:
        grade = "S"
    elif total >= 7.0:
        grade = "A"
    elif total >= 5.5:
        grade = "B"
    elif total >= 4.0:
        grade = "C"
    elif total >= 2.5:
        grade = "D"
    else:
        grade = "F"
    
    # DNA
    dna_input = f"{total}{''.join(map(str, scores.values()))}{notes}"
    dna_hash = hashlib.sha256(dna_input.encode()).hexdigest()[:8]
    dna = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-LU-SCORE-{grade}-{dna_hash}"
    
    return {
        "total": total,
        "grade": grade,
        "details": details,
        "notes": notes,
        "timestamp": datetime.now().isoformat(),
        "dna": dna,
        "rater": "P03-雯雯",
    }


def score_quick(ratings: Dict[str, float]) -> Dict:
    """快速评分: {创意:8, 人格:7, 结构:6, 推进:8, 表达:5}"""
    return score_system(
        creative=ratings.get("创意", ratings.get("creative_trigger", 5)),
        persona=ratings.get("人格", ratings.get("persona_linkage", 5)),
        structure=ratings.get("结构", ratings.get("structure_build", 5)),
        push=ratings.get("推进", ratings.get("system_push", 5)),
        expression=ratings.get("表达", ratings.get("expression_impact", 5)),
    )


def score_compare(before: Dict, after: Dict) -> Dict:
    """前后对比"""
    diff = after["total"] - before["total"]
    trend = "⬆️上升" if diff > 0.5 else ("⬇️下降" if diff < -0.5 else "➡️持平")
    
    dim_diffs = {}
    for key in WEIGHTS:
        b = before["details"].get(key, {}).get("weighted", 0)
        a = after["details"].get(key, {}).get("weighted", 0)
        dim_diffs[WEIGHT_LABELS[key]] = round(a - b, 2)
    
    return {
        "before_total": before["total"],
        "after_total": after["total"],
        "diff": round(diff, 2),
        "trend": trend,
        "dim_diffs": dim_diffs,
        "before_grade": before["grade"],
        "after_grade": after["grade"],
    }


# ============================================================
# CLI
# ============================================================
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="🐉 龍魂·LU-SYSTEM-SCORE 评分引擎 v1.0")
    parser.add_argument("--score", nargs=5, type=float, metavar=("创意","人格","结构","推进","表达"),
                        help="五维评分 0-10")
    parser.add_argument("--quick", type=str, help='快速评分JSON: {"创意":8,"人格":7}')
    parser.add_argument("--compare", nargs=2, help="对比两次评分JSON文件")
    parser.add_argument("--default", action="store_true", help="显示默认权重")
    
    args = parser.parse_args()
    
    if args.default:
        print("🐉 LU-SYSTEM-SCORE 五维权重:")
        for key, w in WEIGHTS.items():
            print(f"  {WEIGHT_LABELS[key]}: {w*100:.0f}%")
        print(f"\n  等级: S(8.5+) A(7.0+) B(5.5+) C(4.0+) D(2.5+) F(<2.5)")
        return
    
    if args.score:
        result = score_system(*args.score)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    
    if args.quick:
        try:
            ratings = json.loads(args.quick)
        except:
            ratings = eval(args.quick)
        result = score_quick(ratings)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    
    if args.compare:
        with open(args.compare[0]) as f:
            before = json.load(f)
        with open(args.compare[1]) as f:
            after = json.load(f)
        result = score_compare(before, after)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    
    parser.print_help()


if __name__ == "__main__":
    main()
