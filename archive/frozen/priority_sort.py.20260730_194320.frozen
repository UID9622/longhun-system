#!/usr/bin/env python3
"""
龍魂三色审计优先级排序器
DNA: #龍芯⚡️-PRIORITY-SORT-v1.0
"""
import argparse, json, sys
from dataclasses import dataclass

WEIGHTS = {
    "blocker": 0.40,
    "risk": 0.30,
    "impact": 0.20,
    "urgency": 0.10,
}

COLOR_ORDER = {"🔴": 0, "🟡": 1, "🟢": 2}


def score_task(task: dict) -> float:
    total = 0.0
    for key, weight in WEIGHTS.items():
        total += task.get(key, 0) * weight
    return round(total, 2)


def color_for_score(score: float) -> str:
    # 任务优先级阈值：阻塞/高风险任务标红，常规任务标绿
    if score >= 70:
        return "🔴"
    if score >= 40:
        return "🟡"
    return "🟢"


def label_for_color(color: str) -> str:
    return {
        "🔴": "立即执行（最高优先级）",
        "🟡": "其次执行（中等优先级）",
        "🟢": "延后执行（最低优先级）",
    }.get(color, "未知")


def sort_tasks(tasks: list[dict]) -> list[dict]:
    for t in tasks:
        t["score"] = score_task(t)
        t["color"] = color_for_score(t["score"])

    return sorted(
        tasks,
        key=lambda x: (COLOR_ORDER[x["color"]], -x["score"]),
    )


def render(tasks: list[dict]) -> str:
    lines = ["## 龍魂三色优先级排序\n", f"**DNA**: #龍芯⚡️-PRIORITY-SORT\n"]

    from itertools import groupby

    sorted_tasks = sort_tasks(tasks)
    grouped = {
        color: list(items)
        for color, items in groupby(sorted_tasks, key=lambda x: x["color"])
    }

    for color in ["🔴", "🟡", "🟢"]:
        group = grouped.get(color, [])
        if not group:
            continue
        lines.append(f"\n### {color} {label_for_color(color)}")
        for idx, t in enumerate(group, 1):
            lines.append(f"{idx}. **{t.get('name', '未命名任务')}** — 综合得分 `{t['score']}`")
            lines.append(
                f"   - 阻塞度: {t.get('blocker', 0)} | "
                f"风险度: {t.get('risk', 0)} | "
                f"影响面: {t.get('impact', 0)} | "
                f"紧迫度: {t.get('urgency', 0)}"
            )
            if t.get("note"):
                lines.append(f"   - 💡 {t['note']}")

    lines.append("\n---")
    lines.append("\n**执行建议**: 按 🔴 > 🟡 > 🟢 顺序推进，同色任务按得分从高到低执行。")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="LongHun three-color priority sorter")
    parser.add_argument("--tasks", required=True, help="JSON array of task objects")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of markdown")
    args = parser.parse_args()

    try:
        tasks = json.loads(args.tasks)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    sorted_tasks = sort_tasks(tasks)

    if args.json:
        print(json.dumps(sorted_tasks, ensure_ascii=False, indent=2))
    else:
        print(render(tasks))


if __name__ == "__main__":
    main()
