#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·庚申·辰时·䷓观-PARSE-ASI-SUITE-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
从 ASI_TEST_SUITE_v2.md 解析表格，生成结构化 JSON。
"""

import json
import re
from pathlib import Path
from typing import List, Dict


def parse_markdown_tables(md_path: Path) -> List[Dict]:
    text = md_path.read_text(encoding="utf-8")

    # 找到所有表格块
    tables = re.findall(r"\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|\n\|[:-]+\|[^\n]+\n((?:\|[^\n]+\|\n?)+)", text)

    cases = []
    for table_body in tables:
        lines = [l.strip() for l in table_body.strip().split("\n") if l.strip()]
        for line in lines:
            cells = [c.strip() for c in line.split("|")]
            cells = [c for c in cells if c]  # 去掉空单元格
            if len(cells) < 6:
                continue
            # 第一列是编号
            case_id = cells[0]
            if not re.match(r"^(LANG|LAW|CULT|CROSS|BDR)-\d+$", case_id):
                continue

            cases.append({
                "id": case_id,
                "category": case_id.split("-")[0],
                "field1": cells[1],
                "field2": cells[2],
                "input": cells[3],
                "expected_symbol": cells[4],
                "validation": cells[5],
                "payload": "",  # 待补充：实际测试输入
                "target_api": "compliance",  # 默认合规沙盒
                "regions": [],
                "mode": "sandbox",
                "status": "pending"
            })

    return cases


def enrich_case(case: Dict) -> Dict:
    """根据场景类型补充默认调用参数"""
    cid = case["id"]
    cat = case["category"]

    # 提取场景中的地区信息
    if cat == "LAW":
        region_text = case["field1"]
        region_map = {
            "西班牙/拉美": ["ES"],
            "俄罗斯": ["RU"],
            "瑞士/国际": ["CH", "EU"],
            "国际通用": ["CN", "US", "EU"]
        }
        case["regions"] = region_map.get(region_text, ["CN", "US", "EU"])
        case["payload"] = case["input"]
    elif cat == "CROSS":
        case["target_api"] = "cross"
        case["payload"] = case["input"]
        case["regions"] = ["ES", "CN", "EU"]
    elif cat == "BDR":
        case["target_api"] = "compliance"
        case["payload"] = case["input"]
        case["regions"] = ["CN", "US", "EU"]
    elif cat == "LANG":
        case["target_api"] = "compliance"
        case["payload"] = case["input"]
        case["regions"] = ["CN", "US", "EU"]
    else:
        case["target_api"] = "archive"
        case["payload"] = case["input"]

    # 转换预期符号为内部状态
    sym = case["expected_symbol"]
    if sym == "✅":
        case["expected_state"] = "block_or_alert"
    elif sym == "❌":
        case["expected_state"] = "pass"
    elif sym in ("⚠️", "🟡"):
        case["expected_state"] = "review"
    else:
        case["expected_state"] = "review"

    return case


def main():
    md_path = Path(__file__).resolve().parent.parent / "12_DOCS" / "ASI_TEST_SUITE_v2.md"
    out_path = Path(__file__).resolve().parent.parent / "08_BIN" / "asi_test_suite.json"

    cases = parse_markdown_tables(md_path)
    cases = [enrich_case(c) for c in cases]

    suite = {
        "version": "2.0",
        "dna": "#龍芯⚡️丙午·甲申·辛丑·甲午·䷁坤-ASI-TEST-SUITE-UID9622",
        "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
        "gpg": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
        "total": len(cases),
        "cases": cases
    }

    out_path.write_text(json.dumps(suite, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ 已解析 {len(cases)} 个测试场景 → {out_path}")


if __name__ == "__main__":
    main()
