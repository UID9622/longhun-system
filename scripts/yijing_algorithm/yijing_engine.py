#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 易经64卦推演引擎 · 可执行版
依据：python易经算法实现.pdf + ichingshifa 64卦数据库补全
核心逻辑与 PDF 一致：SHA256 起卦 → 互卦 → 变卦 → 节气加权 → 五行分析 → 太极三才综合判断

DNA: #龍芯⚡️2026-06-29-YIJING-ENGINE-EXEC-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
from __future__ import annotations
import hashlib
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# ═════════ 载入数据 ═════════
_DATA_PATH = Path(__file__).with_name("yijing_data.json")
with open(_DATA_PATH, "r", encoding="utf-8") as _f:
    _RAW = json.load(_f)

HEXAGRAMS: Dict[str, dict[str, Any]] = _RAW["HEXAGRAMS"]
HEXAGRAM_BY_ID: Dict[int, dict[str, Any]] = {v["id"]: v for v in HEXAGRAMS.values()}
SOLAR_TERMS: Dict[str, float] = _RAW["SOLAR_TERMS"]
WUXING_RELATION: Dict[str, Dict[str, str]] = _RAW["WUXING_RELATION"]

# ═════════ 文化 DNA ═════════
CULTURAL_DNA = {
    "origin": "𝌆𝌇𝌈𝌉𝌊𝌋𝌌𝌍",
    "creator": "🚀 Lucky | UID9622",
    "timestamp": "2025-11-24",
    "heritage": "五千年易经智慧",
    "signature": hashlib.sha256("易经64卦推演引擎-Lucky-2025".encode("utf-8")).hexdigest()[:16],
}


def verify_cultural_dna() -> Dict[str, Any]:
    expected = hashlib.sha256("易经64卦推演引擎-Lucky-2025".encode("utf-8")).hexdigest()[:16]
    if CULTURAL_DNA["signature"] != expected:
        print("⚠️ 警告：文化DNA已被篡改")
    return CULTURAL_DNA


def print_cultural_dna() -> None:
    print("=" * 60)
    print("🧬 易经64卦推演引擎")
    print(f"📜 文化印记：{CULTURAL_DNA['origin']}")
    print(f"👤 创建者：{CULTURAL_DNA['creator']}")
    print(f"📅 创建日期：{CULTURAL_DNA['timestamp']}")
    print(f"🏛️ 文化传承：{CULTURAL_DNA['heritage']}")
    print(f"🔐 数字签名：{CULTURAL_DNA['signature']}")
    print("=" * 60)
    print()


# ═════════ 1. 起卦算法 ═════════
def generate_hexagram(input_text: str, timestamp: float | None = None) -> Dict[str, Any]:
    """
    生成本卦
    input_text: 用户问题或意念
    timestamp: 时间戳（默认当前时间）
    """
    if timestamp is None:
        timestamp = time.time()

    creator_mark = "Lucky-UID9622-易经算法"
    seed = f"{input_text}{timestamp}{creator_mark}".encode("utf-8")
    hash_value = hashlib.sha256(seed).hexdigest()

    # 生成6个爻（0=阴爻，1=阳爻），binary[0] 为顶爻
    lines = []
    for i in range(6):
        byte_value = int(hash_value[i * 2:(i + 1) * 2], 16)
        lines.append(1 if byte_value > 127 else 0)

    # 确定变爻（老阴、老阳）
    change_lines = []
    for i in range(6):
        byte_value = int(hash_value[i * 2 + 12:(i + 1) * 2 + 12], 16)
        if byte_value < 64 or byte_value > 191:
            change_lines.append(i)

    binary = "".join(map(str, lines))
    return {
        "lines": lines,
        "change_lines": change_lines,
        "binary": binary,
        "hexagram_id": binary_to_id(binary),
    }


def binary_to_id(binary: str) -> int:
    """将二进制爻象转换为卦序号（1-64）。"""
    return int(binary, 2) + 1


def id_to_binary(hex_id: int) -> str:
    return format(hex_id - 1, "06b")


# ═════════ 2. 互卦与变卦 ═════════
def derive_mutual_hexagram(original_lines: List[int]) -> Dict[str, Any]:
    """
    推演互卦：取 2-5 爻构成新的上下卦。
    注意：original_lines[0] 为顶爻。
    """
    # 取 2、3、4 爻为下卦（索引 1,2,3）
    lower = original_lines[1:4]
    # 取 3、4、5 爻为上卦（索引 2,3,4）
    upper = original_lines[2:5]
    mutual_lines = upper + lower
    binary = "".join(map(str, mutual_lines))
    return {
        "lines": mutual_lines,
        "binary": binary,
        "hexagram_id": binary_to_id(binary),
    }


def derive_changed_hexagram(original_lines: List[int], change_lines: List[int]) -> Dict[str, Any]:
    """推演变卦：将变爻阴阳互换。"""
    changed_lines = original_lines.copy()
    for pos in change_lines:
        changed_lines[pos] = 1 - changed_lines[pos]
    binary = "".join(map(str, changed_lines))
    return {
        "lines": changed_lines,
        "change_lines": change_lines,
        "binary": binary,
        "hexagram_id": binary_to_id(binary),
    }


# ═════════ 3. 节气加权 ═════════
def get_solar_term_weight(timestamp: float) -> float:
    """根据时间计算最近的节气权重（PDF 简化版）。"""
    dt = datetime.fromtimestamp(timestamp)
    month, day = dt.month, dt.day

    solar_terms_dates = {
        (2, 4): "立春", (2, 19): "雨水",
        (3, 6): "惊蛰", (3, 21): "春分",
        (4, 5): "清明", (4, 20): "谷雨",
        (5, 6): "立夏", (5, 21): "小满",
        (6, 6): "芒种", (6, 21): "夏至",
        (7, 7): "小暑", (7, 23): "大暑",
        (8, 8): "立秋", (8, 23): "处暑",
        (9, 8): "白露", (9, 23): "秋分",
        (10, 8): "寒露", (10, 23): "霜降",
        (11, 7): "立冬", (11, 22): "小雪",
        (12, 7): "大雪", (12, 22): "冬至",
        (1, 6): "小寒", (1, 20): "大寒",
    }

    current_term = None
    min_diff = 365
    for (m, d), term in solar_terms_dates.items():
        diff = abs((month - m) * 30 + (day - d))
        if diff < min_diff:
            min_diff = diff
            current_term = term

    return SOLAR_TERMS.get(current_term, 1.0)


# ═════════ 4. 五行分析 ═════════
def analyze_wuxing(original_hex: Dict[str, Any], changed_hex: Dict[str, Any]) -> Dict[str, Any]:
    """分析五行相生相克关系。"""
    original_element = HEXAGRAMS[original_hex["binary"]]["element"]
    changed_element = HEXAGRAMS[changed_hex["binary"]]["element"]

    is_sheng = WUXING_RELATION["生"].get(original_element) == changed_element
    is_ke = WUXING_RELATION["克"].get(original_element) == changed_element

    if is_sheng:
        trend = "顺势而行，事半功倍"
        score = 0.8
    elif is_ke:
        trend = "逆势而动，需化解阻碍"
        score = 0.3
    else:
        trend = "平和之象，稳步推进"
        score = 0.5

    return {
        "original_element": original_element,
        "changed_element": changed_element,
        "is_sheng": is_sheng,
        "is_ke": is_ke,
        "trend": trend,
        "score": score,
    }


# ═════════ 5. 卦辞爻辞解析 ═════════
def interpret_hexagram(hex_data: Dict[str, Any]) -> Dict[str, Any]:
    """解析卦象。"""
    info = HEXAGRAMS.get(hex_data["binary"], {})
    return {
        "name": info.get("name", "未知"),
        "gua_ci": info.get("meaning", ""),
        "interpretation": info.get("tuan", info.get("meaning", "")),
        "yao_ci": info.get("yao_ci", []),
        "fortune": info.get("fortune", 0.5),
    }


# ═════════ 6. 太极三才综合判断 ═════════
def taiji_judgment(original_hex: Dict[str, Any], mutual_hex: Dict[str, Any], changed_hex: Dict[str, Any], solar_weight: float) -> Dict[str, Any]:
    """太极三才综合判断。"""
    original_interp = interpret_hexagram(original_hex)
    changed_interp = interpret_hexagram(changed_hex)
    wuxing_result = analyze_wuxing(original_hex, changed_hex)

    # 人道：变爻具体分析
    change_lines_analysis = []
    for pos in original_hex["change_lines"]:
        yao_text = original_interp["yao_ci"][pos] if pos < len(original_interp["yao_ci"]) else "无爻辞"
        change_lines_analysis.append({
            "position": pos + 1,
            "text": yao_text,
            "is_auspicious": "吉" in yao_text or "利" in yao_text,
        })

    # 三才权重
    gua_ci = original_interp["gua_ci"]
    tian_score = 0.7 if ("吉" in gua_ci or "亨" in gua_ci) else 0.4
    di_score = wuxing_result["score"]
    ren_score = sum(1 for x in change_lines_analysis if x["is_auspicious"]) / max(len(change_lines_analysis), 1)

    # 综合分数（加入节气权重）
    final_score = (tian_score * 0.4 + di_score * 0.3 + ren_score * 0.3) * solar_weight

    if final_score > 0.7:
        judgment = "🟢 大吉 - 诸事顺遂，可大胆行动"
    elif final_score > 0.5:
        judgment = "🟢 小吉 - 稍有阻碍，谨慎可行"
    elif final_score > 0.3:
        judgment = "🟡 中平 - 平常之象，守正待时"
    elif final_score > 0.1:
        judgment = "🔴 小凶 - 有险阻，宜三思而行"
    else:
        judgment = "🔴 大凶 - 诸事不宜，应当止步"

    return {
        "judgment": judgment,
        "score": round(final_score, 4),
        "details": {
            "tian_dao": {"score": tian_score, "text": original_interp["interpretation"]},
            "di_dao": {"score": di_score, "text": wuxing_result["trend"]},
            "ren_dao": {"score": ren_score, "changes": change_lines_analysis},
        },
        "advice": generate_advice(final_score, wuxing_result),
    }


def generate_advice(score: float, wuxing_result: Dict[str, Any]) -> str:
    """生成行动建议。"""
    if score > 0.6:
        return f"当前形势有利，{wuxing_result['trend']}，可积极推进计划。"
    elif score > 0.3:
        return f"形势中平，{wuxing_result['trend']}，宜稳健行事，观察时机。"
    else:
        return f"当前不利，{wuxing_result['trend']}，建议暂缓行动，等待转机。"


# ═════════ 7. 完整推演流程 ═════════
def complete_divination(question: str, timestamp: float | None = None) -> Dict[str, Any]:
    """完整易经推演流程。"""
    if timestamp is None:
        timestamp = time.time()

    original_hex = generate_hexagram(question, timestamp)
    mutual_hex = derive_mutual_hexagram(original_hex["lines"])
    changed_hex = derive_changed_hexagram(original_hex["lines"], original_hex["change_lines"])
    solar_weight = get_solar_term_weight(timestamp)

    original_interp = interpret_hexagram(original_hex)
    mutual_interp = interpret_hexagram(mutual_hex)
    changed_interp = interpret_hexagram(changed_hex)

    wuxing_result = analyze_wuxing(original_hex, changed_hex)
    final_judgment = taiji_judgment(original_hex, mutual_hex, changed_hex, solar_weight)

    return {
        "cultural_dna": CULTURAL_DNA,
        "algorithm_author": "🚀 Lucky | UID9622",
        "creation_date": "2025-11-24",
        "cultural_heritage": "中华易经五千年智慧",
        "question": question,
        "timestamp": timestamp,
        "solar_weight": solar_weight,
        "hexagrams": {
            "original": {
                "id": original_hex["hexagram_id"],
                "name": original_interp["name"],
                "oracle": HEXAGRAMS[original_hex["binary"]].get("oracle", ""),
                "interpretation": original_interp,
            },
            "mutual": {
                "id": mutual_hex["hexagram_id"],
                "name": mutual_interp["name"],
                "interpretation": mutual_interp,
            },
            "changed": {
                "id": changed_hex["hexagram_id"],
                "name": changed_interp["name"],
                "interpretation": changed_interp,
            },
        },
        "wuxing": wuxing_result,
        "judgment": final_judgment,
    }


# ═════════ 自检 ═════════
def selftest() -> None:
    print_cultural_dna()
    print("=" * 60)
    print("🐉 易经推演引擎自检")
    print("=" * 60)

    # 起卦可复现
    h1 = generate_hexagram("test", 1782710383.0)
    h2 = generate_hexagram("test", 1782710383.0)
    assert h1 == h2, "相同输入应产生相同卦象"
    print(f"[1] 起卦可复现：binary={h1['binary']} id={h1['hexagram_id']}  ✅")

    # 互卦/变卦结构正确
    mutual = derive_mutual_hexagram(h1["lines"])
    changed = derive_changed_hexagram(h1["lines"], h1["change_lines"])
    assert len(mutual["lines"]) == 6 and len(changed["lines"]) == 6
    print(f"[2] 互卦={mutual['binary']} 变卦={changed['binary']}  ✅")

    # 节气权重
    sw = get_solar_term_weight(1782710383.0)
    assert 0.0 < sw <= 2.0
    print(f"[3] 节气权重={sw}  ✅")

    # 五行分析
    wx = analyze_wuxing(h1, changed)
    assert wx["score"] in (0.3, 0.5, 0.8)
    print(f"[4] 五行：{wx['original_element']} → {wx['changed_element']} ({wx['trend']})  ✅")

    # 完整推演
    result = complete_divination("UID9622 龍魂系统未来走势如何？", 1782710383.0)
    assert "judgment" in result
    print(f"[5] 完整推演：本卦={result['hexagrams']['original']['name']} "
          f"综合分={result['judgment']['score']}  ✅")

    print("=" * 60)
    print("🟢 易经推演引擎自检通过")
    print("   DNA: #龍芯⚡️2026-06-29-YIJING-ENGINE-EXEC-v1.0")
    print("=" * 60)


if __name__ == "__main__":
    selftest()
