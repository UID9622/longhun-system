#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍智守 · 套路分析引擎
讀取 `~/longhun-system/logs/龍智守_套路识别日志.jsonl`，輸出：
  - 總識別次數
  - 各套路命中頻次
  - 各類別（詐騙/營銷套路/灰色話術）佔比
  - 最近命中記錄
  - 按時間段趨勢（可選）
用法：
  python3 龍智守_套路分析.py
  python3 龍智守_套路分析.py --top 10 --days 7
DNA: #龍芯⚡️丙午·甲午·乙亥·壬午·䷚颐-LONGZHI-SHOU-ANALYZER
"""

import argparse
import json
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

LOG_PATH = Path.home() / "longhun-system" / "logs" / "龍智守_套路识别日志.jsonl"


def _load_records(days: int | None = None) -> list[dict[str, Any]]:
    if not LOG_PATH.exists():
        return []
    records = []
    cutoff = datetime.now() - timedelta(days=days) if days else None
    with LOG_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                if cutoff:
                    ts = datetime.strptime(rec.get("timestamp", "")[:10], "%Y-%m-%d")
                    if ts < cutoff:
                        continue
                records.append(rec)
            except Exception:
                continue
    return records


def analyze(days: int | None, top: int) -> dict[str, Any]:
    records = _load_records(days)
    total = len(records)

    pattern_counter = Counter()
    category_counter = Counter()
    intent_counter = Counter()
    risk_counter = Counter()

    for rec in records:
        intent_counter[rec.get("intent", "unknown")] += 1
        risk_counter[rec.get("risk", "unknown")] += 1
        for p in rec.get("patterns", []):
            pattern_counter[f"{p['id']} {p['name']}"] += 1
            category_counter[p.get("category", "未知")] += 1

    return {
        "total_records": total,
        "time_range": f"最近 {days} 天" if days else "全部",
        "intents": dict(intent_counter.most_common()),
        "risks": dict(risk_counter.most_common()),
        "categories": dict(category_counter.most_common()),
        "top_patterns": dict(pattern_counter.most_common(top)),
        "recent_records": records[-5:],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="龍智守套路分析引擎")
    parser.add_argument("--days", type=int, help="只分析最近 N 天")
    parser.add_argument("--top", type=int, default=10, help="Top N 套路")
    args = parser.parse_args()

    result = analyze(args.days, args.top)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
