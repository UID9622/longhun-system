#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 训练数据质量检查
按错误率、等级分布、低质量样本等维度输出质量报告。
DNA: #龍芯⚡️2026-06-30-LONGHUN-QUALITY-CHECK-v1.0
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
ANNOTATED_DIR = HOME / "longhun-system" / "data" / "training" / "annotated"
REPORT_DIR = HOME / "longhun-system" / "data" / "training" / "reports"


def _读取jsonl(路径: Path) -> list:
    if not 路径.exists():
        return []
    结果 = []
    with 路径.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                结果.append(json.loads(line))
            except Exception:
                continue
    return 结果


def main():
    日期 = datetime.now(timezone.utc).strftime("%Y%m%d")
    输入路径 = ANNOTATED_DIR / 日期 / "annotated.jsonl"
    if not 输入路径.exists():
        print(f"🟡 今日无标注数据: {输入路径}")
        sys.exit(0)

    数据 = _读取jsonl(输入路径)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    报告路径 = REPORT_DIR / f"quality_report_{日期}.json"

    总数 = len(数据)
    if 总数 == 0:
        print("🟡 无数据可检查")
        sys.exit(0)

    得分列表 = [d["annotation"]["综合得分"] for d in 数据]
    平均得分 = round(sum(得分列表) / 总数, 4)
    最低分 = min(得分列表)
    最高分 = max(得分列表)

    等级分布 = {"🟢": 0, "🟡": 0, "🔴": 0}
    for d in 数据:
        等级 = d["annotation"].get("等级", "🟡")
        等级分布[等级] = 等级分布.get(等级, 0) + 1

    # 错误率：综合得分 < 0.6 视为不合格
    错误数 = sum(1 for s in 得分列表 if s < 0.6)
    错误率 = round(错误数 / 总数, 4)

    # 低质量样本 TOP10
    低质量 = sorted(数据, key=lambda x: x["annotation"]["综合得分"])[:10]
    低质量摘要 = [
        {
            "data_id": d["data_id"],
            "source": d["source"],
            "score": d["annotation"]["综合得分"],
            "raw_preview": str(d.get("raw_text", ""))[:80],
        }
        for d in 低质量
    ]

    报告 = {
        "日期": 日期,
        "总数": 总数,
        "平均得分": 平均得分,
        "最低分": 最低分,
        "最高分": 最高分,
        "等级分布": 等级分布,
        "错误数": 错误数,
        "错误率": 错误率,
        "低质量样本": 低质量摘要,
        "dna": "#龍芯⚡️2026-06-30-LONGHUN-QUALITY-CHECK-v1.0",
    }

    报告路径.write_text(json.dumps(报告, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"🟢 质量检查完成")
    print(f"   总数：{总数}  平均得分：{平均得分}  错误率：{错误率}")
    print(f"   等级分布：{等级分布}")
    print(f"   报告：{报告路径}")
    print(f"   DNA: {报告['dna']}")


if __name__ == "__main__":
    main()
