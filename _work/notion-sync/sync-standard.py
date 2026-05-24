#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂元字引擎 · 一键对齐同步工具 v1.0
sync-standard.py

【人格路由】☵坎+☷坤 · P03雯雯(审计) + P04文心(语义) + P08数据大师(分析)
【四步法】观复(扫全盘) → 知常(识别偏差) → 若水(生成报告) → 无不为(--apply修正)
【DNA】#龍芯⚡️2026-03-06-SYNC-STANDARD-v1.0
【原则】权重不变 · DNA格式不变 · 只对齐·不覆盖历史

用法:
  python3 sync-standard.py              # 扫描+报告（默认，不修改文件）
  python3 sync-standard.py --apply      # 扫描+报告+一键修正
  python3 sync-standard.py --dirs ~/longhun-system ~/Documents  # 指定目录
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# ───────────────────────────────────────────────
# 配置区
# ───────────────────────────────────────────────

BASE_DIR = Path.home() / "longhun-system"
ENGINE_FILE = BASE_DIR / "persona-engine.json"
MEMORY_FILE = BASE_DIR / "memory.jsonl"
REPORT_DIR = BASE_DIR

DEFAULT_SCAN_DIRS = [
    Path.home() / "longhun-system",
    Path.home() / "Documents",
    Path.home() / ".claude" / "skills" / "longhun",
]

SCAN_EXTENSIONS = {".md", ".txt", ".json", ".jsonl", ".py", ".sh", ".yaml", ".yml"}

SKIP_DIRS = {
    ".git", "__pycache__", "node_modules", ".venv", "persona_env",
    "stylegan3-main 2", "backups", "duplicates", ".Trash",
    "CNSH_备份_20260211",  # 备份目录不改
}

SKIP_FILES = {
    ".env", "sync-standard.py", "dna_checksum.txt",
    "persona-engine.json",  # 源头文件·不可被自身覆盖
    "CLAUDE.md",            # 引擎配置·遗留条目用于文档说明
}

MAX_FILE_SIZE = 2_000_000  # 2MB，超过跳过


# ───────────────────────────────────────────────
# 加载标准配置
# ───────────────────────────────────────────────

def load_engine(path: Path) -> dict:
    if not path.exists():
        print(f"[错误] 找不到引擎配置: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_replacements(engine: dict) -> Tuple[List[Tuple[re.Pattern, str]], Dict[str, str]]:
    """
    从 engine 构建两套替换规则：
    1. dna_patterns: DNA前缀旧→新
    2. id_map: 人格旧ID→新标准ID
    """
    dna_map: Dict[str, str] = engine.get("dna_legacy_map", {})
    id_map: Dict[str, str] = engine.get("legacy_id_map", {})

    # DNA前缀替换（旧⚡→新⚡，注意顺序：长的先匹配）
    dna_patterns: List[Tuple[re.Pattern, str]] = []
    for old, new in sorted(dna_map.items(), key=lambda x: -len(x[0])):
        escaped = re.escape(old)
        dna_patterns.append((re.compile(escaped), new))

    return dna_patterns, id_map


# ───────────────────────────────────────────────
# 文件扫描
# ───────────────────────────────────────────────

def iter_files(dirs: List[Path]):
    for base in dirs:
        if not base.exists():
            continue
        for root, subdirs, files in os.walk(base):
            root_path = Path(root)
            # 过滤跳过目录
            subdirs[:] = [d for d in subdirs if d not in SKIP_DIRS and not d.startswith(".")]
            for fname in files:
                fpath = root_path / fname
                if fname in SKIP_FILES:
                    continue
                if fpath.suffix.lower() not in SCAN_EXTENSIONS:
                    continue
                try:
                    if fpath.stat().st_size > MAX_FILE_SIZE:
                        continue
                except OSError:
                    continue
                yield fpath


def scan_file(
    fpath: Path,
    dna_patterns: List[Tuple[re.Pattern, str]],
    id_map: Dict[str, str],
) -> dict:
    """
    扫描单个文件，返回发现的问题列表和修正后内容。
    不写入磁盘。
    """
    try:
        text = fpath.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return {}

    original = text
    findings_dna: List[str] = []
    findings_id: List[str] = []

    # DNA前缀检查
    for pat, new_prefix in dna_patterns:
        matches = pat.findall(text)
        if matches:
            findings_dna.append(f"{matches[0]} → {new_prefix} (×{len(matches)})")
            text = pat.sub(new_prefix, text)

    # 人格ID检查（词边界匹配，避免误替换）
    for old_id, new_id in sorted(id_map.items(), key=lambda x: -len(x[0])):
        escaped = re.escape(old_id)
        pat = re.compile(r'(?<![#\w])' + escaped + r'(?![\w])')
        matches = pat.findall(text)
        if matches:
            findings_id.append(f"{old_id} → {new_id} (×{len(matches)})")
            text = pat.sub(new_id, text)

    changed = text != original
    return {
        "path": str(fpath),
        "changed": changed,
        "dna_issues": findings_dna,
        "id_issues": findings_id,
        "new_content": text if changed else None,
    }


# ───────────────────────────────────────────────
# 应用修正
# ───────────────────────────────────────────────

def apply_fix(result: dict) -> bool:
    if not result.get("changed"):
        return False
    fpath = Path(result["path"])
    # 原子写入
    tmp = fpath.with_suffix(fpath.suffix + ".sync_tmp")
    try:
        tmp.write_text(result["new_content"], encoding="utf-8")
        tmp.replace(fpath)
        return True
    except OSError as e:
        print(f"  [写入失败] {fpath}: {e}", file=sys.stderr)
        if tmp.exists():
            tmp.unlink()
        return False


# ───────────────────────────────────────────────
# 报告生成
# ───────────────────────────────────────────────

def build_report(results: List[dict], apply_mode: bool, elapsed: float) -> str:
    ts = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dna = f"#龍芯⚡️{dt.date.today()}-SYNC-REPORT-v1.0"
    mode = "✅ 已应用修正" if apply_mode else "📋 仅报告（未修改文件）"

    issues = [r for r in results if r.get("changed")]
    clean = [r for r in results if not r.get("changed") and r]

    lines = [
        f"# 龍魂元字引擎 · 对齐同步报告",
        f"",
        f"**时间:** {ts}",
        f"**模式:** {mode}",
        f"**DNA:** {dna}",
        f"**GPG:** A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
共建致谢：
  Claude (Anthropic PBC) · 技术协作与代码共创
  Notion · 知识底座与结构化存储
  没有你们，就没有龍魂系统的一切。
        f"**耗时:** {elapsed:.2f}s",
        f"",
        f"---",
        f"",
        f"## 统计",
        f"",
        f"| 项目 | 数量 |",
        f"|---|---|",
        f"| 扫描文件总数 | {len(results)} |",
        f"| 发现问题文件 | {len(issues)} |",
        f"| 无需修改文件 | {len(clean)} |",
        f"| DNA前缀问题 | {sum(len(r.get('dna_issues',[])) for r in results)} |",
        f"| 人格ID问题 | {sum(len(r.get('id_issues',[])) for r in results)} |",
        f"",
        f"---",
        f"",
    ]

    if issues:
        lines += [
            f"## 问题文件（{len(issues)} 个）",
            f"",
        ]
        for r in issues:
            rel = r["path"].replace(str(Path.home()), "~")
            lines.append(f"### `{rel}`")
            if r["dna_issues"]:
                lines.append(f"**DNA前缀:**")
                for issue in r["dna_issues"]:
                    lines.append(f"- {issue}")
            if r["id_issues"]:
                lines.append(f"**人格ID:**")
                for issue in r["id_issues"]:
                    lines.append(f"- {issue}")
            status = "✅ 已修正" if (apply_mode and r["changed"]) else "⚠️ 待修正（运行 --apply）"
            lines.append(f"**状态:** {status}")
            lines.append(f"")
    else:
        lines += ["## 全部对齐 🟢", "", "所有文件 DNA 格式和人格 ID 均已符合标准。", ""]

    lines += [
        f"---",
        f"",
        f"**【人格路由】** ☵坎 · P03雯雯 + P04文心 + P08数据大师",
        f"**【三色审计】** {'🟢 已修正' if apply_mode else ('🟡 发现问题·待修正' if issues else '🟢 无问题')}",
        f"**【DNA】** {dna}",
    ]

    return "\n".join(lines)


# ───────────────────────────────────────────────
# 写入 memory.jsonl
# ───────────────────────────────────────────────

def append_memory(results: List[dict], apply_mode: bool, report_path: str):
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    issues = [r for r in results if r.get("changed")]
    entry = {
        "timestamp": ts,
        "type": "sync_cycle",
        "tier": "TIER_2",
        "dna": f"#龍芯⚡️{dt.date.today()}-SYNC-CYCLE-v1.0",
        "event": "元字引擎对齐同步" + ("·已应用修正" if apply_mode else "·仅报告"),
        "operator": "UID9622",
        "personas": ["P03雯雯", "P04文心", "P08数据大师"],
        "stats": {
            "scanned": len(results),
            "issues_found": len(issues),
            "applied": apply_mode,
        },
        "report": report_path,
    }
    try:
        with open(MEMORY_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError as e:
        print(f"[警告] 无法写入 memory.jsonl: {e}", file=sys.stderr)


# ───────────────────────────────────────────────
# 主入口
# ───────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(
        description="龍魂元字引擎·一键对齐同步工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--apply", action="store_true",
                   help="实际修改文件（默认只报告不修改）")
    p.add_argument("--dirs", nargs="+", type=Path,
                   help="指定扫描目录（默认：~/longhun-system ~/Documents）")
    p.add_argument("--engine", type=Path, default=ENGINE_FILE,
                   help="persona-engine.json 路径")
    p.add_argument("--no-memory", action="store_true",
                   help="不写入 memory.jsonl")
    return p.parse_args()


def main():
    args = parse_args()
    start = dt.datetime.now()

    print(f"【P03雯雯+P04文心+P08数据大师 · 观复启动】")
    print(f"  引擎标准: {args.engine}")
    print(f"  模式: {'🔧 应用修正' if args.apply else '📋 仅扫描报告'}")
    print()

    # 加载标准
    engine = load_engine(args.engine)
    dna_patterns, id_map = build_replacements(engine)

    print(f"  DNA遗留映射: {len(engine.get('dna_legacy_map', {}))} 条")
    print(f"  人格ID映射: {len(id_map)} 条")
    print(f"  人格总数: P00-P{len(engine.get('personas', {}))-1 + 9}")
    print()

    # 确定扫描目录
    scan_dirs = args.dirs if args.dirs else DEFAULT_SCAN_DIRS
    print("【知常 · 扫描目录】")
    for d in scan_dirs:
        exists = "✅" if d.exists() else "⚠️ 不存在"
        print(f"  {exists} {d}")
    print()

    # 扫描
    print("【若水 · 扫描中...】")
    results = []
    count = 0
    for fpath in iter_files(scan_dirs):
        r = scan_file(fpath, dna_patterns, id_map)
        if r:
            results.append(r)
            count += 1
            if r.get("changed"):
                rel = str(fpath).replace(str(Path.home()), "~")
                print(f"  ⚠️  {rel}")
                for issue in r.get("dna_issues", []):
                    print(f"     DNA: {issue}")
                for issue in r.get("id_issues", []):
                    print(f"     ID:  {issue}")
        if count % 50 == 0 and count > 0:
            print(f"  ... 已扫描 {count} 个文件")

    print(f"\n  扫描完成: {count} 个文件")

    # 应用修正
    if args.apply:
        fixed = 0
        print("\n【无不为 · 应用修正】")
        for r in results:
            if r.get("changed"):
                if apply_fix(r):
                    fixed += 1
                    rel = r["path"].replace(str(Path.home()), "~")
                    print(f"  ✅ 已修正: {rel}")
        print(f"\n  修正完成: {fixed} 个文件")

    # 生成报告
    elapsed = (dt.datetime.now() - start).total_seconds()
    report_text = build_report(results, args.apply, elapsed)
    report_name = f"sync-report-{dt.date.today()}.md"
    report_path = REPORT_DIR / report_name

    try:
        report_path.write_text(report_text, encoding="utf-8")
        print(f"\n📋 报告已保存: {report_path}")
    except OSError as e:
        print(f"\n[警告] 报告写入失败: {e}", file=sys.stderr)
        report_path = Path("/tmp") / report_name
        report_path.write_text(report_text, encoding="utf-8")

    # 写入 memory.jsonl
    if not args.no_memory:
        append_memory(results, args.apply, str(report_path))
        print(f"🧬 已写入 memory.jsonl")

    # 输出DNA
    issues = [r for r in results if r.get("changed")]
    color = "🟢" if not issues else ("✅" if args.apply else "🟡")
    print(f"\n{color} 【DNA】#龍芯⚡️{dt.date.today()}-SYNC-{'APPLIED' if args.apply else 'REPORT'}-v1.0")
    print(f"   【三色审计】{'已修正' if (args.apply and issues) else ('发现问题' if issues else '全部对齐')}")
    print(f"   【人格路由】☵坎 P03雯雯+P04文心+P08数据大师")

    return 0 if not issues or args.apply else 1


if __name__ == "__main__":
    sys.exit(main())
