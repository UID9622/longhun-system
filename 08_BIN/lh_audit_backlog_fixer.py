#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙酉·壬戌·亥时·䷬萃-AUDIT-BACKLOG-FIXER-v1.0-UID9622-8F2A1B3C
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 龍魂 · 审计积压修复脚本 v1.0

按审计积压分类结果，批量修复 07_AUDIT/ 下的待审记录：
  - 缺少 DNA → 生成新格式 DNA
  - 缺少 CONFIRM → 添加确认码
  - 旧时间戳格式 DNA → 升级为新格式

原则：不删除只冻结。修复前把原文件复制到 archive/frozen/07_AUDIT/。

用法:
  python3 08_BIN/lh_audit_backlog_fixer.py --dry-run
  python3 08_BIN/lh_audit_backlog_fixer.py

协议: CC BY-NC-SA 4.0 (思想层) · MulanPSL v2 (工程层)
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.longhun_core.dna_trace import generate_dna

# ═══════════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════════
PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUDIT_DIR = PROJECT_ROOT / "07_AUDIT"
REPORT_PATH = PROJECT_ROOT / "07_AUDIT" / "reports" / "audit_summary.json"
ARCHIVE_DIR = PROJECT_ROOT / "archive" / "frozen" / "07_AUDIT"
CONFIRM_MARK = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
DNA_NEW_RE = re.compile(r'#龍芯⚡️[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]·.*-.*-.*-[0-9A-F]{8}')
DNA_OLD_DATE_RE = re.compile(r'#龍芯⚡️\d{8}')
DNA_OLD_ISO_RE = re.compile(r'#龍芯⚡️\d{4}-\d{2}-\d{2}')


# ═══════════════════════════════════════════════════════
# 修复逻辑
# ═══════════════════════════════════════════════════════
def needs_fix(record: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """判断记录是否需要修复，返回 (是否修复, 问题列表)"""
    problems = []
    dna = record.get("dna", record.get("DNA", ""))

    if not dna:
        problems.append("missing_dna")
    elif DNA_OLD_DATE_RE.search(dna) or DNA_OLD_ISO_RE.search(dna):
        problems.append("old_timestamp")
    elif not DNA_NEW_RE.search(dna):
        problems.append("malformed_dna")

    has_confirm = CONFIRM_MARK in json.dumps(record, ensure_ascii=False)
    if not has_confirm:
        problems.append("missing_confirm")

    return bool(problems), problems


def fix_record(record: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    """修复单条记录，返回 (修复后记录, 修复动作列表)"""
    fixed = dict(record)
    actions = []
    dna = fixed.get("dna", fixed.get("DNA", ""))

    # 生成模块名：从 source 或 action 推断
    module = "AUDIT-RECORD"
    for key in ["action", "source", "type", "event"]:
        val = fixed.get(key)
        if val:
            module = str(val).upper().replace(" ", "-").replace("_", "-")[:40]
            break

    # 修复 DNA
    if not dna or DNA_OLD_DATE_RE.search(dna) or DNA_OLD_ISO_RE.search(dna) or not DNA_NEW_RE.search(dna):
        fixed["dna"] = generate_dna(module, "UID9622")
        actions.append("regenerated_dna")

    # 修复 CONFIRM
    content_text = json.dumps(fixed, ensure_ascii=False)
    if CONFIRM_MARK not in content_text:
        fixed["confirm"] = CONFIRM_MARK
        actions.append("added_confirm")

    return fixed, actions


# ═══════════════════════════════════════════════════════
# 文件处理
# ═══════════════════════════════════════════════════════
def archive_original(src: Path) -> Path:
    """把原文件复制到 archive/frozen/07_AUDIT/ 保持相对目录结构"""
    rel = src.relative_to(PROJECT_ROOT)
    dest = ARCHIVE_DIR / rel.name
    dest.parent.mkdir(parents=True, exist_ok=True)
    # 如果已存在同名归档，加时间戳后缀
    if dest.exists():
        dest = dest.with_suffix(f".{datetime.now():%Y%m%d_%H%M%S}{dest.suffix}")
    shutil.copy2(str(src), str(dest))
    return dest


def process_json_file(file_path: Path, dry_run: bool) -> Dict[str, Any]:
    """处理 JSON 文件"""
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"file": str(file_path), "status": "error", "error": str(e)}

    fixed_records = 0
    actions_counter = Counter()

    def fix_item(item):
        nonlocal fixed_records
        if not isinstance(item, dict):
            return item
        needs, _ = needs_fix(item)
        if needs:
            new_item, actions = fix_record(item)
            fixed_records += 1
            for a in actions:
                actions_counter[a] += 1
            return new_item
        return item

    if isinstance(data, list):
        new_data = [fix_item(item) for item in data]
    elif isinstance(data, dict):
        new_data = fix_item(data)
    else:
        return {"file": str(file_path), "status": "skip", "reason": "unsupported_json_type"}

    if dry_run:
        return {
            "file": str(file_path),
            "status": "dry-run",
            "fixed_records": fixed_records,
            "actions": dict(actions_counter),
        }

    archive_original(file_path)
    file_path.write_text(json.dumps(new_data, ensure_ascii=False, indent=2), encoding="utf-8")
    return {
        "file": str(file_path),
        "status": "fixed",
        "fixed_records": fixed_records,
        "actions": dict(actions_counter),
    }


def process_jsonl_file(file_path: Path, dry_run: bool) -> Dict[str, Any]:
    """处理 JSONL/LOG 文件"""
    fixed_records = 0
    actions_counter = Counter()
    new_lines = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        return {"file": str(file_path), "status": "error", "error": str(e)}

    for line in lines:
        line = line.strip()
        if not line:
            new_lines.append(line)
            continue
        try:
            item = json.loads(line)
            if isinstance(item, dict):
                needs, _ = needs_fix(item)
                if needs:
                    item, actions = fix_record(item)
                    fixed_records += 1
                    for a in actions:
                        actions_counter[a] += 1
            new_lines.append(json.dumps(item, ensure_ascii=False))
        except json.JSONDecodeError:
            # 非 JSON 行，保持原样
            new_lines.append(line)

    if dry_run:
        return {
            "file": str(file_path),
            "status": "dry-run",
            "fixed_records": fixed_records,
            "actions": dict(actions_counter),
        }

    archive_original(file_path)
    file_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    return {
        "file": str(file_path),
        "status": "fixed",
        "fixed_records": fixed_records,
        "actions": dict(actions_counter),
    }


def process_file(file_path: Path, dry_run: bool) -> Dict[str, Any]:
    if file_path.suffix == ".json":
        return process_json_file(file_path, dry_run)
    elif file_path.suffix in (".jsonl", ".log"):
        return process_jsonl_file(file_path, dry_run)
    return {"file": str(file_path), "status": "skip", "reason": "unsupported_extension"}


# ═══════════════════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂 · 审计积压修复脚本")
    parser.add_argument("--dry-run", "-d", action="store_true", help="干跑模式，不修改文件")
    parser.add_argument("--input-dir", "-i", type=str, default=str(AUDIT_DIR), help="审计目录")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        print(f"❌ 目录不存在: {input_dir}", file=sys.stderr)
        sys.exit(2)

    # 收集可处理文件
    files = []
    for ext in ["*.json", "*.jsonl", "*.log"]:
        files.extend(input_dir.rglob(ext))
    # 排除 reports 目录和签名文件
    files = [f for f in files if "reports" not in f.parts and not f.name.endswith(".asc")]

    print(f"🐉 审计积压修复（dry-run={args.dry_run}）")
    print(f"   待处理文件: {len(files)}")

    results = []
    total_fixed = 0
    total_actions = Counter()

    for f in sorted(files):
        result = process_file(f, args.dry_run)
        results.append(result)
        if result.get("status") in ("fixed", "dry-run"):
            total_fixed += result.get("fixed_records", 0)
            for a, c in result.get("actions", {}).items():
                total_actions[a] += c

    # 生成报告
    report = {
        "dna": generate_dna("AUDIT-BACKLOG-FIXER", "UID9622"),
        "confirm": CONFIRM_MARK,
        "timestamp": datetime.now().isoformat(),
        "dry_run": args.dry_run,
        "input_dir": str(input_dir),
        "total_files": len(files),
        "total_fixed_records": total_fixed,
        "actions": dict(total_actions),
        "results": results,
    }

    report_dir = input_dir / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"audit_fix_{datetime.now():%Y%m%d_%H%M%S}.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n📊 修复摘要")
    print(f"   处理文件: {len(files)}")
    print(f"   修复记录: {total_fixed}")
    print(f"   动作: {dict(total_actions)}")
    print(f"💾 报告: {report_path}")
    print(f"🧬 DNA: {report['dna']}")
    print(f"🔐 确认码: {CONFIRM_MARK}")


if __name__ == "__main__":
    main()
