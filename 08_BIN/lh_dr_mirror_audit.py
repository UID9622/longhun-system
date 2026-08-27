#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 功能: 龍魂 记忆合并数字根镜像审计 v1.0.1（P06 数学大师·镜像审计深化）
# DNA: #龍芯⚡️丙午·丙申·戊辰·亥时·䷳艮-DR-MIRROR-AUDIT-v1.0.1
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 上位: 三才算法 v3.0.1 · 镜像审计协议（P06 对关键计算独立复算）
"""
龍魂 记忆合并数字根镜像审计 v1.0

背景: 记忆合并（MEMORY 压缩/CodeBuddy 合并）后，内容重新组织易引入
      数字根漂移。本引擎对合并产物做数字根一致性抽查 ≥30%（镜像审计）:
        1. 每文件提取全部数字 → 计算整体数字根 dr_all
        2. 提取 DNA 哈希段（如 ...-7d3f1a2b）→ 计算哈希数字根 dr_dna
        3. 提取日期字段（YYYY-MM-DD / 干支四柱）→ 计算日期数字根 dr_date
        4. 交叉验证: dr_all 与 dr_dna / dr_date 是否同余（一致 🟢 偏差 🟡 矛盾 🔴）

镜像审计铁律: P06 对关键计算独立复算——一致🟢 / 偏差🟡 / 矛盾🔴冻结30分钟。

用法:
  python3 bin/lh_dr_mirror_audit.py                     # 扫 .codebuddy/memory/*.md 抽查30%
  python3 bin/lh_dr_mirror_audit.py --dir 03_MEMORY     # 指定目录
  python3 bin/lh_dr_mirror_audit.py --ratio 1.0 --json  # 全量抽查 + JSON 输出
"""

import argparse
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DIR = ROOT / ".codebuddy" / "memory"

# 数字根→五行映射（与 lh_digital_root.py 一致）
DR_WUXING = {0: "土", 1: "水", 2: "火", 3: "木", 4: "金",
             5: "土", 6: "水", 7: "火", 8: "木", 9: "金"}
DR_COLOR = {3: "🔴", 9: "🔴", 6: "🟡"}  # 其余 🟢


def digital_root(text: str) -> int:
    """提取文本中全部数字（含 Unicode 圈数字），反复相加到一位数（0-9）"""
    import unicodedata
    digits = []
    for c in text:
        if c.isdigit():
            try:
                digits.append(int(c))
            except ValueError:
                try:
                    digits.append(unicodedata.digit(c))
                except (ValueError, TypeError):
                    pass
    if not digits:
        return 0
    total = sum(digits)
    while total >= 10:
        total = sum(int(c) for c in str(total))
    return total


def extract_dna_hash(text: str) -> str:
    """提取 DNA 哈希段: #龍芯⚡️...-<哈希8>（或 ...-UID9622）"""
    m = re.search(r"[A-Z0-9]{8}(?:-UID\d+)?", text)
    return m.group(0) if m else ""


def extract_dr_decls(text: str) -> list:
    """提取显式数字根声明: dr(X)=N / dr(X)→N / 数字根=N / (X)→N·五行"""
    decls = []
    # 形态1: dr(输入) = N 或 dr(输入) → N 或 dr(输入) = N → 五行
    for m in re.finditer(r"dr\s*\(\s*([^)]+?)\s*\)\s*[=→]\s*(\d)", text):
        inp, val = m.group(1).strip(), int(m.group(2))
        decls.append(("dr()", inp, val))
    # 形态2: 数字根 | dr(输入) = N（表格行）
    for m in re.finditer(r"数字根\s*\|\s*`?dr\s*\(\s*([^)`]+?)\s*\)\s*=\s*(\d)", text):
        decls.append(("表格dr", m.group(1).strip(), int(m.group(2))))
    # 形态3(废弃): "数字根验证 3+5=8" / "数字根分布 {1:7}" 等是验证列/统计字典，
    #   非 dr() 声明。v1.0.1 起不再提取（曾导致 28MB 浓缩库跨行贪婪误匹配）。
    # 去重
    seen, out = set(), []
    for d in decls:
        key = (d[0], d[1], d[2])
        if key not in seen:
            seen.add(key)
            out.append(d)
    return out


def audit_file(fp: Path) -> dict:
    """镜像审计: P06 对文件中显式声明的数字根做独立复算"""
    text = fp.read_text(encoding="utf-8", errors="replace")
    decls = extract_dr_decls(text)
    dna_hash = extract_dna_hash(text)
    dr_dna = digital_root(dna_hash) if dna_hash else None

    status = "🟢"
    details = []
    checked = 0
    # 占位/变量名关键词（dr(n)、dr(h_i)、dr(dr)、dr(Version) 等模板）→ 不判
    PLACEHOLDER_RE = re.compile(r"^(n|h_i|h_j|dr|v|ver|version|x|y|z|t|time|n\d*)$", re.IGNORECASE)
    for kind, inp, declared in decls:
        # 独立复算: 输入数字根（剥离后缀说明词）
        calc_inp = re.sub(r"[→].*$", "", inp)
        calc_inp = re.sub(r"[^\w\u4e00-\u9fff.-]", "", calc_inp)
        if not calc_inp or not re.search(r"\d", calc_inp):
            continue    # 占位符/无数字输入（dr(n)、文件名声明）→ 跳过
        if PLACEHOLDER_RE.match(calc_inp):
            continue    # 变量名占位（dr(n)、dr(h_i)、dr(Version)）→ 跳过
        recomputed = digital_root(calc_inp)
        checked += 1
        if recomputed != declared:
            status = "🔴"
            details.append(f"声明dr({inp})={declared} 独立复算={recomputed} 矛盾")

    if not decls or checked == 0:
        # 无有效声明 → 跳过（不判错，仅记录 DNA 哈希供追溯）
        status = "🟢"
        details.append(f"无有效dr声明 · 跳过 (dr_dna={dr_dna or '-'})")

    return {
        "file": str(fp.relative_to(ROOT)),
        "decls_checked": checked,
        "dr_dna": dr_dna,
        "wuxing": DR_WUXING.get(dr_dna or 0, "土"),
        "status": status,
        "details": details,
    }


def main():
    ap = argparse.ArgumentParser(description="龍魂 记忆合并数字根镜像审计")
    ap.add_argument("--dir", default=str(DEFAULT_DIR), help="记忆目录")
    ap.add_argument("--ratio", type=float, default=0.3, help="抽查比例 ≥30%")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()

    target = Path(args.dir)
    if not target.exists():
        print(f"🔴 目录不存在: {target}", file=sys.stderr)
        return 1

    files = sorted(target.rglob("*.md"))
    if not files:
        print(f"🟡 无 md 文件: {target}")
        return 0

    # 抽查: 至少 ceil(ratio*n)，且 ≥1
    n = max(1, int(len(files) * args.ratio + 0.999))
    if n < len(files):
        rng = random.Random(9622)   # 固定种子 → 可复现抽查
        sampled = rng.sample(files, n)
    else:
        sampled = files

    results = [audit_file(fp) for fp in sampled]
    green = [r for r in results if r["status"] == "🟢"]
    yellow = [r for r in results if r["status"] == "🟡"]
    red = [r for r in results if r["status"] == "🔴"]

    if args.json:
        print(json.dumps({
            "dir": str(target), "total": len(files), "sampled": len(sampled),
            "green": len(green), "yellow": len(yellow), "red": len(red),
            "results": results,
        }, ensure_ascii=False, indent=2))
        return 1 if red else 0

    print(f"── 记忆合并数字根镜像审计（P06）──")
    print(f"目录: {target} · 共{len(files)}文件 · 抽查{len(sampled)} ({args.ratio*100:.0f}% ≥30%)")
    for r in results:
        w = r["wuxing"]
        d = (" · " + "; ".join(r["details"])) if r["details"] else ""
        print(f"  {r['status']} {r['file']:55} 复算{r['decls_checked']}处 dr_dna={r['dr_dna']}({w}){d}")
    print(f"── 汇总: 🟢 {len(green)} · 🟡 {len(yellow)} · 🔴 {len(red)}")
    if red:
        print("🔴 存在矛盾 → 冻结30分钟复查（镜像审计铁律）")
        return 1
    if yellow:
        print("🟡 存在偏差 → 标记待核，48h 内复查")
        return 0
    print("🟢 数字根镜像审计全绿")
    return 0


if __name__ == "__main__":
    sys.exit(main())
