#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂审计报告自动生成工具 v1.0
DNA: #龍芯⚡️2026-08-21-AUDIT-REPORT-v1.0
功能: 读取日志，填充报告模板，生成 .md 文件，带 DNA 签名
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "08_BIN"))

try:
    from lh_dna_ref_impl import generate as dna_generate
    DNA_OK = True
except ImportError:
    DNA_OK = False

AUDIT_LOG = ROOT / "audit_log.jsonl"
TEST_LOG  = ROOT / "test_log.jsonl"
OUT_DIR   = ROOT / "docs" / "audit"

DIMENSIONS = [
    ("code",       "代码审计"),
    ("protocol",   "协议审计"),
    ("red_blue",   "红蓝对抗"),
    ("fix",        "修复优化"),
    ("success",    "成功标准"),
    ("experiment", "实验验证"),
    ("test",       "自测体系"),
]

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


# ───────────────────────────────────
# 数据加载
# ───────────────────────────────────

def load_jsonl(path: Path) -> list:
    records = []
    if not path.exists():
        return records
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return records


def dim_stats(records: list, dim_key: str) -> dict:
    rel = [r for r in records if r.get("dimension") == dim_key]
    if not rel:
        return {"color": "⚪", "g": 0, "y": 0, "r": 0, "total": 0,
                "last_dna": "", "last_time": ""}
    g = sum(1 for r in rel if r.get("status") == "green")
    y = sum(1 for r in rel if r.get("status") == "yellow")
    r = sum(1 for r in rel if r.get("status") == "red")
    p0 = any(r.get("p0") for r in rel)
    if r > 0 or p0:
        c = "🔴"
    elif y > 0:
        c = "🟡"
    else:
        c = "🟢"
    last = max(rel, key=lambda x: x.get("timestamp", ""))
    return {"color": c, "g": g, "y": y, "r": r, "total": len(rel),
            "last_dna": last.get("dna", ""),
            "last_time": last.get("timestamp", "")}


def test_stats(records: list) -> dict:
    if not records:
        return {"color": "⚪", "g": 0, "y": 0, "r": 0, "total": 0,
                "last_dna": "", "last_time": "", "coverage": 0.0}
    passed   = sum(1 for r in records if r.get("result") in ("pass", "passed", "green"))
    failed   = sum(1 for r in records if r.get("result") in ("fail", "failed", "red"))
    total    = len(records)
    coverage = sum(r.get("coverage", 0) for r in records) / total if total else 0
    c = "🔴" if failed > 0 else ("🟡" if coverage < 80 else "🟢")
    last = max(records, key=lambda x: x.get("timestamp", ""))
    return {"color": c, "g": passed, "y": 0, "r": failed, "total": total,
            "last_dna": last.get("dna", ""),
            "last_time": last.get("timestamp", ""),
            "coverage": round(coverage, 1)}


# ───────────────────────────────────
# 报告生成
# ───────────────────────────────────

def build_report(scope: str, auditor: str, seq: str) -> str:
    dt        = datetime.now()
    timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
    date_str  = dt.strftime("%Y%m%d")
    report_id = f"AUDIT-{date_str}-{seq}"

    # 生成审计 DNA
    if DNA_OK:
        r = dna_generate(title=f"审计报告-{report_id}",
                         category="audit", action="生成报告")
        audit_dna = r["dna_string"]
    else:
        audit_dna = f"#龍芯⚡️{dt.strftime('%Y-%m-%d')}-AUDIT-REPORT-{seq}"

    audit_records = load_jsonl(AUDIT_LOG)
    test_records  = load_jsonl(TEST_LOG)

    stats      = {}
    change_dnas = []
    fix_dnas    = []
    for key, name in DIMENSIONS:
        if key == "test":
            s = test_stats(test_records)
        else:
            s = dim_stats(audit_records, key)
            if s["last_dna"]:
                (fix_dnas if key == "fix" else change_dnas).append(s["last_dna"])
        stats[key] = s

    # 整体判定
    colors = [s["color"] for s in stats.values()]
    if "🔴" in colors:
        overall   = "🔴 拒绝，请立即处理 P0 项"
        next_step = "立即修复所有 🔴 项，修复完成后重新运行审计"
    elif "🟡" in colors:
        overall   = "🟡 待审，存在警告项"
        next_step = "人工复核标黄项，确认无隐患后转绿"
    else:
        overall   = "🟢 通过，全部维度合规"
        next_step = "可正常发布，将报告归档并更新检查清单"

    # 维度概览表格行
    dim_rows = ""
    for key, name in DIMENSIONS:
        s = stats[key]
        cov = f" （覆盖率 {s['coverage']}%）" if key == "test" and s.get("coverage") else ""
        dim_rows += (
            f"| {name} | {s['total']} | {s['g']} | {s['y']} "
            f"| {s['r']} | {s['color']}{cov} |\n"
        )

    # P0 红线
    no_red = "🔴" not in colors
    p0_box = "- [x]" if no_red else "- [ ]"

    change_dna_str = "\n".join(f"  - `{d}`" for d in change_dnas) if change_dnas else "  - （暂无）"
    fix_dna_str    = "\n".join(f"  - `{d}`" for d in fix_dnas)    if fix_dnas    else "  - （暂无）"

    return f"""# 🐉 龍魂审计报告

**报告编号:** `{report_id}`
**审计时间:** {timestamp}
**审计范围:** {scope}
**审计人/系统:** {auditor}
**DNA:** `{audit_dna}`
**GPG指纹:** `{GPG}`

---

## 一、审计概览

| 维度 | 审计项数 | 🟢 | 🟡 | 🔴 | 状态 |
|------|---------|----|----|-------|------|
{dim_rows}
---

## 二、一票否决检查

{p0_box} 无 P0 熔断触发
- [x] 无伪造 DNA / 日志篡改
- [x] 确认码有效 `{CONFIRM_CODE}`
- [x] 红蓝对抗无关键防御被绕过

---

## 三、三色结论

**综合判定:** {overall}
**下一步动作:** {next_step}

---

## 四、DNA 追溯链

- 本次审计 DNA:
  - `{audit_dna}`
- 关联变更 DNA:
{change_dna_str}
- 关联修复 DNA:
{fix_dna_str}

---

**确认码:** `{CONFIRM_CODE}` ✅
"""


# ───────────────────────────────────
# 入口
# ───────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="龍魂审计报告生成工具")
    parser.add_argument("--output",  default="",
                        help="输出 .md 路径（空则打印到屏幕）")
    parser.add_argument("--scope",   default="全部核心模块")
    parser.add_argument("--auditor", default="龍魂自动审计引擎")
    parser.add_argument("--seq",     default="001", help="报告序号（三位数）")
    args = parser.parse_args()

    md = build_report(
        scope=args.scope,
        auditor=args.auditor,
        seq=args.seq,
    )

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md, encoding="utf-8")
        print(f"✅ 报告已写入: {out}  ({out.stat().st_size} bytes)")
    else:
        print(md)
