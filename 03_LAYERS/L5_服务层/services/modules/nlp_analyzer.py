#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷌同人-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂民生 · NLP条款抽取

按"第X条/第X款/数字."等模式切分合同文本为条款；提取关键金额/日期/甲方乙方。
纯规则，无外部依赖。
DNA #龍魂⚡️丙午·辛未·NLP-v1
"""

import re


def extract_clauses(text: str) -> list[Any]:
    """切分条款。返回 [{'no':'第1条','text':...}]"""
    if not text:
        return []
    # 按 第X条 / 第X款 / X. 切分
    parts = re.split(r"(?=(?:第[一二三四五六七八九十百〇0-9]+[条条款项])|(?:^\s*\d+[\.、])|(?:[一二三四五六七八九十]+、))",
                     text, flags=re.M)
    clauses = []
    for p in parts:
        p = p.strip()
        if len(p) < 4:
            continue
        m = re.match(r"(第[一二三四五六七八九十百〇0-9]+[条条款项]?)", p)
        no = m.group(1) if m else f"段{len(clauses)+1}"
        clauses.append({"no": no, "text": p})
    return clauses


def extract_money(text: str) -> list[Any]:
    return re.findall(r"(\d+(?:\.\d+)?)\s*(?:元|万元|万|千元)", text)


def extract_parties(text: str) -> dict[str, Any]:
    """粗略抽取甲方乙方。"""
    res = {"甲方": "", "乙方": "", "丙方": ""}
    for role in res:
        m = re.search(role + r"[：:：]?\s*([^\n，,。；;]{2,20})", text)
        if m:
            res[role] = m.group(1).strip()
    return res


if __name__ == "__main__":
    t = "第一条 押金不退。第二条 年化利率36%。第三条 最终解释权归甲方。"
    for c in extract_clauses(t):
        print(c["no"], c["text"][:20])
