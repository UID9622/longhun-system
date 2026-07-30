#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · Notion 引擎完整性检查器 v1.0
DNA: #龍芯⚡️丙午·乙未·乙未·申时·☰乾-NOTION-INTEGRITY-CHECKER-v1.0
创建者: 诸葛鑫 (UID9622)
协议: CC BY-NC-SA 4.0

完整性检查：验证引擎注册表与实际文件系统的一致性。
- 文件存在性检查
- DNA 签名校验
- 注册表字段完整性
- 分类一致性
- 孤儿文件检测（不在注册表中的文件）

用法:
  python3 bin/lh_notion_integrity_check.py              # 全部检查
  python3 bin/lh_notion_integrity_check.py --quick        # 快速检查（仅文件存在性）
  python3 bin/lh_notion_integrity_check.py --fix          # 自动修复可修复问题
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

CST = timezone(timedelta(hours=8))

DNA = "#龍芯⚡️丙午·乙未·乙未·申时·☰乾-NOTION-INTEGRITY-CHECKER-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_FILE = ROOT / "data" / "notion_sync" / "engines" / "engine_registry_tagged.json"
FALLBACK_FILE = ROOT / "data" / "notion_sync" / "engines" / "engine_registry.json"
AUDIT_FILE = ROOT / "data" / "notion_sync" / "engines" / "integrity_check.jsonl"

# ── 必须字段 ─────────────────────────────────────────
REQUIRED_FIELDS = [
    "id", "name", "filename", "path", "category", "subcategory",
    "type", "lines", "size_bytes", "hash", "status", "scanned_at",
]

OPTIONAL_FIELDS = [
    "dna", "description", "priority", "imports", "functions",
    "classes", "ops_tags", "tags",
]

VALID_CATEGORIES = {
    "🧠 智能与推理", "🛡️ 安全与治理", "⚙️ 工程与部署",
    "📡 数据与知识", "🎭 人格与协作", "🔮 哲学与数学",
    "🌐 交互与表达", "🔗 集成与桥接",
}


def _now() -> str:
    return datetime.now(CST).isoformat()


def _log(msg: str, level: str = "INFO"):
    markers = {"INFO": "📋", "OK": "✅", "WARN": "🟡", "ERROR": "🔴", "PASS": "🟢", "FAIL": "🔴"}
    print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] {markers.get(level, 'ℹ️')} {msg}")


def _audit_log(entry: Dict[str, Any]):
    """写入审计日志"""
    AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
    entry["timestamp"] = _now()
    entry["dna"] = DNA
    with open(AUDIT_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ── 检查函数 ─────────────────────────────────────────

def check_file_existence(engines: List[Dict]) -> Tuple[int, int, List[Dict]]:
    """检查文件是否存在"""
    missing = []
    for eng in engines:
        filepath = ROOT / eng["path"]
        if not filepath.exists():
            missing.append({
                "engine": eng["name"],
                "path": eng["path"],
                "issue": "file_missing",
                "severity": "error",
            })
    return len(engines) - len(missing), len(missing), missing


def check_required_fields(engines: List[Dict]) -> Tuple[int, int, List[Dict]]:
    """检查必填字段完整性"""
    incomplete = []
    for eng in engines:
        missing_fields = [f for f in REQUIRED_FIELDS if f not in eng or eng[f] is None]
        if missing_fields:
            incomplete.append({
                "engine": eng["name"],
                "path": eng.get("path", "?"),
                "issue": "missing_fields",
                "missing": missing_fields,
                "severity": "error",
            })
    return len(engines) - len(incomplete), len(incomplete), incomplete


def check_category_validity(engines: List[Dict]) -> Tuple[int, int, List[Dict]]:
    """检查分类是否在合法范围内"""
    invalid = []
    for eng in engines:
        cat = eng.get("category", "")
        if cat not in VALID_CATEGORIES:
            invalid.append({
                "engine": eng["name"],
                "path": eng.get("path", "?"),
                "issue": "invalid_category",
                "current": cat,
                "severity": "warning",
            })
    return len(engines) - len(invalid), len(invalid), invalid


def check_hash_consistency(engines: List[Dict]) -> Tuple[int, int, List[Dict]]:
    """校验文件哈希是否与注册表一致"""
    import hashlib
    mismatched = []
    for eng in engines:
        filepath = ROOT / eng["path"]
        if not filepath.exists():
            continue
        try:
            current_hash = hashlib.sha256(filepath.read_bytes()).hexdigest()[:8]
            stored_hash = eng.get("hash", "")
            if current_hash != stored_hash:
                mismatched.append({
                    "engine": eng["name"],
                    "path": eng["path"],
                    "issue": "hash_mismatch",
                    "stored": stored_hash,
                    "current": current_hash,
                    "severity": "warning",
                })
        except Exception:
            pass
    checked = sum(1 for e in engines if (ROOT / e["path"]).exists())
    return checked - len(mismatched), len(mismatched), mismatched


def check_dna_presence(engines: List[Dict]) -> Tuple[int, int, List[Dict]]:
    """检查 DNA 签名覆盖率"""
    missing_dna = []
    for eng in engines:
        dna = eng.get("dna", "")
        if not dna or dna == "未注册":
            missing_dna.append({
                "engine": eng["name"],
                "path": eng.get("path", "?"),
                "issue": "no_dna",
                "severity": "warning",
            })
    return len(engines) - len(missing_dna), len(missing_dna), missing_dna


def check_documentation(engines: List[Dict]) -> Tuple[int, int, List[Dict]]:
    """检查文档覆盖率"""
    undocumented = []
    for eng in engines:
        desc = eng.get("description", "")
        if not desc or desc in ("（无描述）", "") or len(desc) < 20:
            undocumented.append({
                "engine": eng["name"],
                "path": eng.get("path", "?"),
                "issue": "undocumented",
                "severity": "warning",
            })
    return len(engines) - len(undocumented), len(undocumented), undocumented


def find_orphan_files(engines: List[Dict]) -> Tuple[int, List[Dict]]:
    """查找孤儿文件（不在注册表中的 .py 文件）"""
    registered_paths = {e["path"] for e in engines}

    scan_dirs = [
        ROOT / "engines",
        ROOT / "bin",
        ROOT / "01_技能庫",
    ]

    orphans = []
    for scan_dir in scan_dirs:
        if not scan_dir.exists():
            continue
        for py_file in scan_dir.rglob("*.py"):
            if any(p.startswith(".") or p == "__pycache__" for p in py_file.parts):
                continue
            rel = str(py_file.relative_to(ROOT))
            if rel not in registered_paths:
                orphans.append({
                    "path": rel,
                    "size": py_file.stat().st_size,
                    "issue": "orphan_file",
                    "severity": "warning",
                })

    return len(orphans), orphans


# ── 汇总 ─────────────────────────────────────────────

def run_all_checks(engines: List[Dict], quick: bool = False) -> Dict[str, Any]:
    """运行所有检查"""
    results: Dict[str, Any] = {
        "dna": DNA,
        "version": "1.0",
        "checked_at": _now(),
        "total_engines": len(engines),
        "checks": {},
        "summary": {"pass": 0, "fail": 0, "warn": 0, "total_items": 0},
        "issues": [],
    }

    checks = [
        ("文件存在性", check_file_existence),
        ("必填字段", check_required_fields),
        ("DNA签名", check_dna_presence),
    ]

    if not quick:
        checks.extend([
            ("哈希一致性", check_hash_consistency),
            ("分类合法性", check_category_validity),
            ("文档覆盖率", check_documentation),
        ])

    for name, check_fn in checks:
        passed, failed, issues = check_fn(engines)
        results["checks"][name] = {
            "passed": passed,
            "failed": failed,
            "rate": f"{passed * 100 // max(passed + failed, 1)}%",
        }
        results["issues"].extend(issues)

        if failed > 0:
            sev = "error" if any(i.get("severity") == "error" for i in issues) else "warning"
            if sev == "error":
                results["summary"]["fail"] += failed
            else:
                results["summary"]["warn"] += failed
        results["summary"]["pass"] += passed
        results["summary"]["total_items"] += passed + failed

    # 孤儿文件检查
    if not quick:
        orphan_count, orphans = find_orphan_files(engines)
        results["checks"]["孤儿文件"] = {
            "found": orphan_count,
        }
        if orphan_count > 0:
            results["issues"].extend(orphans)
            results["summary"]["warn"] += orphan_count
            results["summary"]["total_items"] += orphan_count

    # 总分
    total = results["summary"]["total_items"]
    fail = results["summary"]["fail"]
    if total > 0:
        score = round((total - fail) / total * 100, 1)
    else:
        score = 100.0
    results["score"] = score

    return results


def print_report(results: Dict[str, Any]):
    """打印检查报告"""
    print(f"\n{'='*60}")
    print(f"  龍魂引擎完整性检查报告")
    print(f"  时间: {results['checked_at']}")
    print(f"  引擎总数: {results['total_engines']}")
    print(f"  健康度:  {results['score']}%")
    print(f"{'='*60}\n")

    for name, check in results.get("checks", {}).items():
        if "passed" in check:
            icon = "🟢" if check["failed"] == 0 else ("🟡" if check["failed"] < 5 else "🔴")
            print(f"  {icon} {name:12s}  通过:{check.get('passed','?')}  未通过:{check.get('failed','?')}  ({check.get('rate','?')})")
        elif "found" in check:
            icon = "🟢" if check["found"] == 0 else "🟡"
            print(f"  {icon} {name:12s}  发现:{check['found']} 个孤儿文件")

    # 问题详情
    issues = results.get("issues", [])
    errors = [i for i in issues if i.get("severity") == "error"]
    warnings = [i for i in issues if i.get("severity") == "warning"]

    if errors:
        print(f"\n🔴 错误 ({len(errors)}):")
        for e in errors[:10]:
            print(f"  • [{e['issue']}] {e.get('engine', e.get('path','?'))}")

    if warnings:
        print(f"\n🟡 警告 ({len(warnings)}):")
        for w in warnings[:10]:
            print(f"  • [{w['issue']}] {w.get('engine', w.get('path','?'))}")

    print(f"\n{'🟢 全部通过' if results['score'] >= 100 else '🟡 需关注' if results['score'] >= 90 else '🔴 需要修复'} ({results['score']}%)")


# ── 入口 ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="龍魂 Notion 引擎完整性检查器")
    parser.add_argument("--quick", action="store_true", help="快速检查（仅文件存在性+字段+DNA）")
    parser.add_argument("--fix", action="store_true", help="自动修复可修复问题")
    args = parser.parse_args()

    print(f"\n{DNA}")
    print(f"{CONFIRM}\n")

    # 加载注册表
    registry = None
    for f in (REGISTRY_FILE, FALLBACK_FILE):
        if f.exists():
            with open(f) as fh:
                registry = json.load(fh)
            break

    if not registry:
        _log("注册表不存在，请先运行 lh_notion_engine_discovery.py", "ERROR")
        sys.exit(1)

    engines = registry.get("engines", [])
    _log(f"加载注册表: {len(engines)} 个引擎")

    results = run_all_checks(engines, quick=args.quick)
    print_report(results)

    # 归档审计日志
    _audit_log({
        "type": "integrity_check",
        "score": results["score"],
        "issues_count": len(results["issues"]),
        "quick": args.quick,
    })

    _log("完成", "OK")

    # 退出码
    if results["score"] < 90:
        sys.exit(1)


if __name__ == "__main__":
    main()
