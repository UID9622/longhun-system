#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
from __future__ import annotations
"""
从 ichingshifa 数据包提取 64 卦信息，生成 yijing_data.json
供 python易经算法实现.pdf 中的算法使用。

DNA: #龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-YIJING-DATA-BUILD-v1.0
"""
import json
import pickle
import sys
from pathlib import Path

# 优先使用项目内 venv
VENV = Path(__file__).resolve().parents[3] / "_work" / "venv_iching"
PKG = VENV / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages" / "ichingshifa"
if not PKG.exists():
    # fallback：当前环境
    import ichingshifa
    PKG = Path(ichingshifa.__file__).parent

DATA_PKL = PKG / "data.pkl"
OUT = Path(__file__).with_name("yijing_data.json")

# 标准八卦五行（二进制由上到下）
TRIGRAM_ELEMENT = {
    "111": "金",  # 乾
    "110": "金",  # 兑
    "101": "火",  # 离
    "100": "木",  # 巽
    "001": "木",  # 震
    "010": "水",  # 坎
    "011": "土",  # 艮
    "000": "土",  # 坤
}

# 24 节气权重（取自 PDF 原文）
SOLAR_TERMS = {
    "立春": 1.1, "雨水": 1.05, "惊蛰": 1.15, "春分": 1.0,
    "清明": 0.95, "谷雨": 1.05, "立夏": 1.2, "小满": 1.1,
    "芒种": 1.15, "夏至": 1.25, "小暑": 1.1, "大暑": 1.2,
    "立秋": 0.9, "处暑": 0.85, "白露": 0.8, "秋分": 1.0,
    "寒露": 0.75, "霜降": 0.7, "立冬": 0.6, "小雪": 0.65,
    "大雪": 0.55, "冬至": 0.5, "小寒": 0.55, "大寒": 0.6,
}

WUXING_RELATION = {
    "生": {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"},
    "克": {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"},
}


def code_to_bin(code: str) -> str:
    """ichingshifa 的 6/7/8/9 编码转 0/1，7/9 为阳，6/8 为阴。"""
    return "".join("1" if c in "79" else "0" for c in code)


def fortune_score(name: str, gua_ci: str, yao_texts: list[Any]) -> float:
    """基于卦辞/爻辞吉/凶关键词的简单吉凶评分。"""
    text = gua_ci + "".join(yao_texts)
    good = sum(text.count(w) for w in ["吉", "利", "亨", "无咎", "元亨利贞", "贞吉"])
    bad = sum(text.count(w) for w in ["凶", "悔", "吝", "厉", "灾", "咎", "血"])
    score = 0.5 + (good - bad) * 0.08
    return max(0.1, min(0.95, score))


def build():
    data = pickle.load(open(DATA_PKL, "rb"))
    sfg = data["數字排六十四卦"]
    desc = data["易經卦爻詳解"]

    # 建立 0/1（ichingshifa 的 bottom-to-top）→ 卦名 映射
    bin_to_name = {}
    for codes, name in sfg.items():
        for code in codes:
            b = code_to_bin(code)
            if b not in bin_to_name:
                bin_to_name[b] = name

    hexagrams = {}
    for i in range(64):
        pdf_bin = format(i, "06b")          # 本算法采用 top-to-bottom
        lib_bin = pdf_bin[::-1]              # ichingshifa 使用 bottom-to-top
        name = bin_to_name.get(lib_bin, "未知")

        upper = pdf_bin[:3]
        element = TRIGRAM_ELEMENT.get(upper, "土")

        d = desc.get(name, {})
        # d[0] 为卦辞，d[1..6] 为初爻到上爻（bottom->top），d[7] 为彖
        gua_ci = d.get(0, "")
        yao_bottom_top = [d.get(j, "") for j in range(1, 7)]
        yao_top_bottom = list(reversed(yao_bottom_top))  # 与 pdf_bin 索引对齐

        score = fortune_score(name, gua_ci, yao_bottom_top)

        hexagrams[pdf_bin] = {
            "id": i + 1,
            "name": name,
            "binary": pdf_bin,
            "element": element,
            "oracle": "",           # 甲骨文符号留空，保持文化标识可扩展
            "meaning": gua_ci,
            "tuan": d.get(7, ""),
            "keywords": [],
            "fortune": round(score, 4),
            "advice": "见机行事，守正待时。",
            "yao_ci": yao_top_bottom,
        }

    payload = {
        "HEXAGRAMS": hexagrams,
        "SOLAR_TERMS": SOLAR_TERMS,
        "WUXING_RELATION": WUXING_RELATION,
        "TRIGRAM_ELEMENT": TRIGRAM_ELEMENT,
        "meta": {
            "source": "ichingshifa data.pkl + PDF 节气权重表",
            "count": len(hexagrams),
            "dna": "#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-YIJING-DATA-BUILD-v1.0",
        },
    }
    json.dump(payload, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"已生成 {OUT}，共 {len(hexagrams)} 卦")


if __name__ == "__main__":
    build()
