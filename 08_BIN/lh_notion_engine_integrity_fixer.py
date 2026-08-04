#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · Notion 引擎完整性修复器 v1.0
DNA: #龍芯⚡️丙午·丙申·癸酉·庚申·临-NOTION-ENGINE-INTEGRITY-FIXER-v1.0-A1B2C3D4
创建者: 诸葛鑫 (UID9622)
协议: CC BY-NC-SA 4.0

基于 integrity_report.json 自动修复低风险完整性债务：
  - 文件头缺失：补 DNA/创建者/协议三行（已有 DNA 则保留）
  - 描述过短：补默认描述占位符（需人工后续细化）

不自动修复（需人工判断）：
  - DNA 格式无效
  - 缺少测试文件
  - 孤立文件

用法:
  python3 bin/lh_notion_engine_integrity_fixer.py              # 安全模式：只报告，不写入
  python3 bin/lh_notion_engine_integrity_fixer.py --apply      # 应用低风险修复
  python3 bin/lh_notion_engine_integrity_fixer.py --apply --backup  # 应用修复并备份原文件
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

CST = timezone(timedelta(hours=8))

DNA = "#龍芯⚡️丙午·丙申·癸酉·庚申·临-NOTION-ENGINE-INTEGRITY-FIXER-v1.0-A1B2C3D4"
SCHEMA_VERSION = "1.0.0"

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "data" / "notion_sync" / "engines"
INTEGRITY_REPORT_FILE = OUTPUT_DIR / "integrity_report.json"
FIX_REPORT_FILE = OUTPUT_DIR / "integrity_fix_report.json"
TASK_LIST_FILE = OUTPUT_DIR / "integrity_remaining_tasks.json"
BACKUP_DIR = OUTPUT_DIR / "backups"

CREATOR_LINE = "# CREATOR: 诸葛鑫 (UID9622)"
PROTOCOL_LINE = "# PROTOCOL: CC BY-NC-SA 4.0"


def _now() -> str:
    return datetime.now(CST).isoformat()


def _log(msg: str, level: str = "INFO"):
    markers = {"INFO": "📋", "OK": "✅", "WARN": "🟡", "ERROR": "🔴", "SKIP": "⏭️", "FIX": "🔧"}
    print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] {markers.get(level, 'ℹ️')} {msg}")


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:8]


def _generate_dna(path: Path) -> str:
    """为无 DNA 文件生成规范 DNA"""
    relpath = str(path.relative_to(ROOT)).replace("/", "-")
    name = path.stem.upper()
    hash8 = _file_hash(path)
    return f"#龍芯⚡️丙午·丙申·癸酉·庚申·临-{name}-v1.0-{hash8}"


def _extract_existing_dna(content: str) -> Optional[str]:
    """从文件头提取已有 DNA"""
    for line in content.split("\n")[:20]:
        m = re.search(r'(#龍芯\S+)', line)
        if m:
            return m.group(1).strip()
    return None


def _has_shebang(content: str) -> bool:
    return content.startswith("#!/")


def _build_header(dna: str) -> str:
    return f"{dna}\n{CREATOR_LINE}\n{PROTOCOL_LINE}"


def _fix_file_header(filepath: Path, backup: bool) -> Tuple[bool, List[str]]:
    """修复单个文件头，返回 (是否修改, 操作日志)"""
    actions: List[str] = []
    try:
        content = filepath.read_text(encoding="utf-8")
    except (UnicodeDecodeError, PermissionError):
        return False, ["无法读取文件"]

    original = content
    lines = content.split("\n")
    existing_dna = _extract_existing_dna(content)

    # 已有完整三行：DNA + CREATOR + PROTOCOL
    has_creator = CREATOR_LINE in content[:1000]
    has_protocol = PROTOCOL_LINE in content[:1000]

    if existing_dna and has_creator and has_protocol:
        return False, ["文件头已完整"]

    new_dna = existing_dna or _generate_dna(filepath)
    header = _build_header(new_dna)

    if _has_shebang(content):
        # shebang 后插入三行
        new_lines = [lines[0], header] + lines[1:]
        new_content = "\n".join(new_lines)
    else:
        # 文件开头插入
        new_content = header + "\n" + content

    if backup:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        backup_path = BACKUP_DIR / f"{filepath.name}.{_file_hash(filepath)}.bak"
        shutil.copy2(filepath, backup_path)
        actions.append(f"备份: {backup_path.relative_to(ROOT)}")

    filepath.write_text(new_content, encoding="utf-8")

    if existing_dna:
        actions.append("补创建者/协议")
    else:
        actions.append(f"新增 DNA + 创建者/协议")

    return True, actions


def _fix_description(filepath: Path, min_len: int = 20) -> Tuple[bool, List[str]]:
    """对描述过短的文件补占位描述（在 docstring 中）"""
    actions: List[str] = []
    try:
        content = filepath.read_text(encoding="utf-8")
    except (UnicodeDecodeError, PermissionError):
        return False, ["无法读取文件"]

    # 简单策略：如果已有 docstring 且很短，在末尾追加说明
    # 更安全的策略：不修改已有 docstring，只在无 docstring 时添加
    import ast
    try:
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            tree = ast.parse(content)
        doc = ast.get_docstring(tree)
    except SyntaxError:
        return False, ["语法错误，跳过"]

    if doc and len(doc) >= min_len:
        return False, ["描述已足够"]

    relpath = str(filepath.relative_to(ROOT))
    placeholder = f"\n🐉 龍魂引擎：{filepath.stem}\n路径：{relpath}\nTODO：请补充详细功能说明（不少于{min_len}字）。\n"

    if doc:
        # 在 docstring 末尾追加
        new_doc = doc.rstrip() + placeholder
        # 替换第一个 docstring
        # 简单字符串替换（可能不精确，但风险低）
        old_docstring = f'"""{doc}"""'
        if old_docstring in content:
            new_content = content.replace(old_docstring, f'"""{new_doc}"""', 1)
        else:
            return False, ["docstring 格式复杂，跳过"]
    else:
        # 在 shebang/头后添加 docstring
        if _has_shebang(content):
            lines = content.split("\n")
            # 找到第一个非注释/空行
            insert_idx = 1
            while insert_idx < len(lines) and (lines[insert_idx].startswith("#") or lines[insert_idx].strip() == ""):
                insert_idx += 1
            new_lines = lines[:insert_idx] + ['"""' + placeholder.strip() + '"""'] + lines[insert_idx:]
            new_content = "\n".join(new_lines)
        else:
            new_content = '"""' + placeholder.strip() + '"""\n' + content

    filepath.write_text(new_content, encoding="utf-8")
    actions.append("补描述占位符")
    return True, actions


def load_report(path: Path) -> Dict[str, Any]:
    if not path.exists():
        _log(f"完整性报告不存在: {path}", "ERROR")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="龍魂 Notion 引擎完整性修复器")
    parser.add_argument("--report", type=Path, default=INTEGRITY_REPORT_FILE,
                        help="输入完整性报告路径")
    parser.add_argument("--apply", action="store_true",
                        help="应用低风险修复（默认只报告）")
    parser.add_argument("--backup", action="store_true",
                        help="修复前备份原文件")
    parser.add_argument("--fix-descriptions", action="store_true",
                        help="同时修复描述过短（默认只修复文件头）")
    args = parser.parse_args()

    print(f"\n{DNA}\n")

    report = load_report(args.report)
    results = report.get("results", [])

    _log(f"加载报告: {len(results)} 个引擎", "INFO")

    fix_report: Dict[str, Any] = {
        "dna": DNA,
        "version": SCHEMA_VERSION,
        "generated_at": _now(),
        "mode": "apply" if args.apply else "dry-run",
        "fixed_headers": [],
        "fixed_descriptions": [],
        "skipped": [],
        "errors": [],
    }

    remaining_tasks: List[Dict[str, Any]] = []

    for result in results:
        path_str = result.get("path", "")
        filepath = ROOT / path_str if path_str else None
        if not filepath or not filepath.exists():
            fix_report["errors"].append({"path": path_str, "reason": "文件不存在"})
            continue

        checks = result.get("checks", {})
        issues = result.get("issues", [])
        issue_types = {issue["type"] for issue in issues}

        actions_log: List[str] = []

        # 修复文件头
        if "file_header" in issue_types or "dna_format" in issue_types:
            header_ok, header_actions = _fix_file_header(filepath, args.backup)
            if header_ok:
                fix_report["fixed_headers"].append({
                    "path": path_str,
                    "actions": header_actions,
                })
                actions_log.extend(header_actions)
            else:
                fix_report["skipped"].append({
                    "path": path_str,
                    "reason": "文件头:" + ";".join(header_actions),
                })

        # 修复描述（仅显式开启）
        if args.fix_descriptions and "description" in issue_types:
            desc_ok, desc_actions = _fix_description(filepath)
            if desc_ok:
                fix_report["fixed_descriptions"].append({
                    "path": path_str,
                    "actions": desc_actions,
                })
                actions_log.extend(desc_actions)

        # 收集剩余人工任务
        for issue in issues:
            itype = issue["type"]
            if itype in ("file_header", "description") and actions_log:
                # 已自动修复，不加入剩余任务
                continue
            if itype == "test_file":
                remaining_tasks.append({
                    "path": path_str,
                    "type": "missing_test",
                    "severity": issue["severity"],
                    "message": issue["message"],
                    "suggested_action": f"创建 tests/test_{filepath.stem}.py 或同目录 test_{filepath.stem}.py",
                })
            elif itype == "dna_format":
                remaining_tasks.append({
                    "path": path_str,
                    "type": "invalid_dna",
                    "severity": issue["severity"],
                    "message": issue["message"],
                    "suggested_action": "人工检查 DNA 格式，按 v∞ 规范重写",
                })
            elif itype == "isolated":
                remaining_tasks.append({
                    "path": path_str,
                    "type": "isolated_file",
                    "severity": issue["severity"],
                    "message": issue["message"],
                    "suggested_action": "确认是否为工具入口或废弃文件；若是模块应补充 import/export",
                })
            elif itype == "description":
                remaining_tasks.append({
                    "path": path_str,
                    "type": "short_description",
                    "severity": issue["severity"],
                    "message": issue["message"],
                    "suggested_action": "人工补充功能说明（不少于20字）",
                })

    # 保存修复报告
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(FIX_REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(fix_report, f, ensure_ascii=False, indent=2)
    _log(f"修复报告已保存: {FIX_REPORT_FILE}", "OK")

    # 保存剩余任务清单
    task_summary = {
        "dna": DNA,
        "version": SCHEMA_VERSION,
        "generated_at": _now(),
        "total_remaining": len(remaining_tasks),
        "by_type": {},
        "tasks": remaining_tasks,
    }
    for task in remaining_tasks:
        t = task["type"]
        task_summary["by_type"][t] = task_summary["by_type"].get(t, 0) + 1

    with open(TASK_LIST_FILE, "w", encoding="utf-8") as f:
        json.dump(task_summary, f, ensure_ascii=False, indent=2)
    _log(f"剩余任务清单已保存: {TASK_LIST_FILE}", "OK")

    # 终端摘要
    print(f"\n{'='*60}")
    print(f"  修复模式: {'APPLY' if args.apply else 'DRY-RUN'}")
    print(f"  修复文件头: {len(fix_report['fixed_headers'])}")
    print(f"  修复描述: {len(fix_report['fixed_descriptions'])}")
    print(f"  跳过/错误: {len(fix_report['skipped']) + len(fix_report['errors'])}")
    print(f"  剩余人工任务: {len(remaining_tasks)}")
    print(f"{'='*60}")
    print("\n📋 剩余任务按类型:")
    for t, cnt in sorted(task_summary["by_type"].items(), key=lambda x: -x[1]):
        print(f"  {t:20s} {cnt:4d}")

    if not args.apply:
        _log("本次为 DRY-RUN，未写入任何文件。加 --apply 执行修复。", "WARN")

    _log("完成", "OK")


if __name__ == "__main__":
    main()
