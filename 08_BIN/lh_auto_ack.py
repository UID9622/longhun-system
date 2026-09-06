#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·癸未·戌时·䷙大畜-VULN-AUTO-ACK-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
lh_auto_ack.py — 龍魂漏洞扫描自动验收回执生成器 v1.0
用法:
    python3 08_BIN/lh_auto_ack.py <report.json>            # 打印回执到 stdout
    python3 08_BIN/lh_auto_ack.py <report.json> --write    # 打印 + 写入 07_AUDIT/{date}-auto-ack.md
被 lh_vuln_scanner.py scan 收口自动调用（output 存在时）。
"""
import json
import sys
import datetime
from pathlib import Path

# ══════════════════════════════════════════════════════════
DNA = "#龍芯⚡️丙午·丁酉·癸未·戌时·䷙大畜-VULN-AUTO-ACK-v1.0-UID9622"
CREATOR = "诸葛鑫（UID9622）"
OWNER = "诸葛鑫 | UID9622 · 龍芯北辰"
LICENSE = "# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)"
# ══════════════════════════════════════════════════════════

_AUDIT_DIR = Path(__file__).resolve().parent.parent / "07_AUDIT"


def generate_ack(report: dict) -> str:
    """从 vuln-scan 报告 JSON 生成验收回执文本（键名对齐 run_scan 实际输出）"""
    meta = report.get("_meta", {})
    summary = report.get("summary", {})

    date = (meta.get("scan_utc", "") or datetime.date.today().isoformat())[:10]
    version = meta.get("version", "?")
    files = meta.get("scanned_files", "?")
    dna = meta.get("dna", "?")
    algorithms = meta.get("algorithms", [])

    confirmed = summary.get("confirmed", "?")
    p0 = summary.get("p0_critical", "?")
    p1 = summary.get("p1_high", "?")
    p2 = summary.get("p2_medium", "?")
    fp = summary.get("false_positive", "?")
    likely_safe = summary.get("likely_safe", "?")
    candidates = summary.get("total_candidates", "?")

    algo_txt = " + ".join(algorithms) if isinstance(algorithms, list) and algorithms else "五算法"
    lines = [
        f"🟢 **自动验收回执 · {date}**",
        "",
        "| 项 | 值 |",
        "|---|---|",
        f"| 引擎版本 | `{version}` |",
        f"| 算法 | {algo_txt} |",
        f"| 扫描文件数 | {files} |",
        f"| 候选发现 | {candidates} |",
        f"| CONFIRMED | {confirmed} |",
        f"| P0 | {p0} |",
        f"| P1 | {p1} |",
        f"| P2 | {p2} |",
        f"| LIKELY_SAFE(右路降级) | {likely_safe} |",
        f"| FALSE_POSITIVE | {fp} |",
        "",
        f"引擎 DNA：{dna}",
        "",
        "> 回执由 08_BIN/lh_auto_ack.py 自动生成 · 详见 07_AUDIT/{date}-vuln-scan-report.json",
    ]
    return "\n".join(lines)


def write_ack_md(ack_text: str, report_path: Path) -> Path:
    """把回执 + 溯源文件头写入 07_AUDIT/{date}-auto-ack.md"""
    date = report_path.name.split("-")[0] if report_path else datetime.date.today().isoformat()
    if len(date) != 10 or date[4] != "-":
        date = datetime.date.today().isoformat()
    out = _AUDIT_DIR / f"{date}-auto-ack.md"
    header = "\n".join([
        f"DNA: #龍芯⚡️{date}-VULN-AUTO-ACK-UID9622",
        f"创建者: {CREATOR}",
        f"归属名: {OWNER}",
        f"协议: CC BY-NC-SA 4.0（核心思想层）",
        f"源报告: {report_path.name}",
        "",
        "",
    ])
    _AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    out.write_text(header + ack_text + "\n", encoding="utf-8")
    return out


def main() -> None:
    argv = sys.argv[1:]
    write = "--write" in argv
    argv = [a for a in argv if a != "--write"]
    if not argv:
        print(__doc__)
        sys.exit(2)
    report_path = Path(argv[0])
    report = json.loads(report_path.read_text(encoding="utf-8"))
    ack = generate_ack(report)
    print(ack)
    if write:
        out = write_ack_md(ack, report_path)
        print(f"\n✅ 回执已写入 {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
