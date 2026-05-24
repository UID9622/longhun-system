# -*- coding: utf-8 -*-
"""
cnsw 批量审计器 — 扫 Markdown/纯文本聊天记录，逐条助手输出过 scan + 可选熔断留痕。
不依赖 pandas；可导出 CSV。
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterator, List, Tuple

from .circuit_breaker import circuit_breaker
from .hook_scanner import scan_output
from .system_tricolor import aggregate_engineering_from_rows

# 常见导出格式前缀（可继续扩充）
_ASSISTANT_PREFIXES = (
    "助手",
    "AI",
    "Assistant",
    "小艺",
    "文心",
    "通义",
    "豆包",
    "Kimi",
)

_LINE_ROLE_RE = re.compile(
    r"^\s*(?:\*\*)?\s*(助手|AI|Assistant|小艺|文心|通义|豆包|Kimi|模型)"
    r"(?:\*\*)?\s*[:：]\s*(.*)$",
    re.I,
)


def parse_chat_lines(content: str) -> Iterator[Tuple[str, str]]:
    """
    启发式解析：带「助手：」前缀的行归入 assistant，否则视为 user 或 narration。
    返回 (role, line)，role ∈ assistant|user|unknown
    """
    for raw in content.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = _LINE_ROLE_RE.match(line)
        if m:
            yield "assistant", m.group(2).strip()
            continue
        if line.startswith("> "):
            yield "user", line[2:].strip()
            continue
        if any(
            line.startswith(f"{p}：") or line.startswith(f"{p}:")
            for p in _ASSISTANT_PREFIXES
            if len(p) > 1
        ):
            parts = re.split(r"[：:]", line, 1)
            if len(parts) == 2:
                yield "assistant", parts[1].strip()
                continue
        yield "unknown", line


def audit_messages(
    messages: List[Tuple[str, str]],
    *,
    only_assistant: bool = True,
    include_supplemental: bool = True,
    halt_on_break: bool = False,
) -> List[Dict[str, Any]]:
    """
    messages: [(role, text), ...]
    每条 assistant 文本跑一次 scan_output，并附 circuit_breaker 文本。
    """
    rows: List[Dict[str, Any]] = []
    for idx, (role, text) in enumerate(messages):
        if only_assistant and role != "assistant":
            continue
        if not text.strip():
            continue
        scan = scan_output(text, include_supplemental=include_supplemental)
        cb = circuit_breaker(scan, write_audit=(scan["drift_level"] in ("L4", "L5")))
        row = {
            "index": idx,
            "role": role,
            "drift_level": scan["drift_level"],
            "tri_color": scan["tri_color"],
            "sovereignty_score": scan["sovereignty_score"],
            "matched_hooks": ";".join(scan["matched_hooks"]),
            "matched_supplemental": ";".join(scan["matched_supplemental"]),
            "pseudo_risk": (scan.get("pseudocode_audit") or {}).get("risk", ""),
            "pseudo_fence_n": (scan.get("pseudocode_audit") or {}).get("fence_count", 0),
            "content_hash": scan["content_hash"],
            "circuit": cb,
            "excerpt": scan["input_excerpt"][:200],
        }
        rows.append(row)
        if halt_on_break and scan["drift_level"] in ("L4", "L5"):
            break
    return rows


def audit_text_file(
    path: Path,
    *,
    encoding: str = "utf-8",
    **kwargs: Any,
) -> List[Dict[str, Any]]:
    content = path.read_text(encoding=encoding, errors="replace")
    msgs = list(parse_chat_lines(content))
    return audit_messages(msgs, **kwargs)


def write_csv(rows: List[Dict[str, Any]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        out_path.write_text("", encoding="utf-8")
        return
    fields = list(rows[0].keys())
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def summarize(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not rows:
        return {
            "rounds": 0,
            "min_score": 100,
            "max_level": "L0",
            "flow_tricolor": "🟢",
            "commit_allowed": True,
        }
    scores = [int(r["sovereignty_score"]) for r in rows]
    levels = [r["drift_level"] for r in rows]
    order = {"L0": 0, "L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5}
    worst = max(levels, key=lambda x: order.get(x, 0))
    eng = aggregate_engineering_from_rows(rows)
    return {
        "rounds": len(rows),
        "min_score": min(scores),
        "max_score": max(scores),
        "avg_score": sum(scores) / len(scores),
        "worst_drift_level": worst,
        "l4_l5_count": sum(1 for r in rows if r["drift_level"] in ("L4", "L5")),
        "flow_tricolor": eng.get("flow_tricolor"),
        "cnsw_tricolor_worst": eng.get("cnsw_tricolor"),
        "commit_allowed": bool(eng.get("commit_allowed")),
        "p05_note": eng.get("p05_lane"),
    }


def main_cli() -> None:
    ap = argparse.ArgumentParser(
        description="CNSW 聊天记录批量审计（国产 AI 钩子探针）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "路径说明：必须是本机存在的聊天导出文件。\n"
            "文档示例里的 /path/to/chat_export.md 仅为占位，直接复制会报「找不到文件」。\n"
            "\n"
            "示例：\n"
            "  %(prog)s ~/Downloads/导出.md -o ~/Desktop/cnsw_report.csv"
        ),
    )
    ap.add_argument(
        "path",
        type=Path,
        help="Markdown 或 txt 聊天导出路径（真实路径，非 /path/to/ 占位）",
    )
    ap.add_argument(
        "-o",
        "--csv-out",
        type=Path,
        default=None,
        help="可选：写出 CSV 报告路径",
    )
    ap.add_argument(
        "--all-lines",
        action="store_true",
        help="不只 assistant 行，未知角色也扫描（噪声大）",
    )
    args = ap.parse_args()
    src = args.path.expanduser()
    if not src.exists():
        ap.error(
            "找不到文件: {}\n"
            "若你是照抄教程里的示例，请把路径换成你的导出文件（例如 ./我的聊天.md）。".format(
                args.path
            )
        )
    if not src.is_file():
        ap.error("不是普通文件（不能是目录）: {}".format(src))

    rows = audit_text_file(
        src,
        only_assistant=not args.all_lines,
    )
    summ = summarize(rows)
    print(json.dumps(summ, ensure_ascii=False, indent=2))
    if summ["rounds"] == 0:
        print(
            "\n提示：没有可审计的助手行。导出里请含「助手：」「AI：」等前缀，"
            "或加 --all-lines 连未知角色行也扫（误报会增多）。",
            flush=True,
        )
    if args.csv_out:
        write_csv(rows, args.csv_out)
        print("CSV:", args.csv_out)