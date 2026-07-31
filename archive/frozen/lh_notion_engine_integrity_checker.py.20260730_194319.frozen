#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · Notion 引擎完整性检查器 v1.0
DNA: #龍芯⚡️丙午·丙申·癸酉·庚申·临-NOTION-ENGINE-INTEGRITY-CHECKER-v1.0-CFB92C9E
创建者: 诸葛鑫 (UID9622)
协议: CC BY-NC-SA 4.0
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

CST = timezone(timedelta(hours=8))

DNA = "#龍芯⚡️丙午·丙申·癸酉·庚申·临-NOTION-ENGINE-INTEGRITY-CHECKER-v1.0-CFB92C9E"
SCHEMA_VERSION = "1.0.0"

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "data" / "notion_sync" / "engines"
REGISTRY_FILE = OUTPUT_DIR / "engine_registry.json"
INTEGRITY_REPORT_FILE = OUTPUT_DIR / "integrity_report.json"
TESTS_DIR = ROOT / "tests"

# 项目 DNA 格式正则：以 #龍芯⚡️ 开头、含非空白标识、可选版本后缀
DNA_REGEX = re.compile(r"^#龍芯⚡️\S{3,}.*$")


def _now() -> str:
    return datetime.now(CST).isoformat()


def _log(msg: str, level: str = "INFO"):
    markers = {"INFO": "📋", "OK": "✅", "WARN": "🟡", "ERROR": "🔴", "SKIP": "⏭️", "CHECK": "🔍"}
    print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] {markers.get(level, 'ℹ️')} {msg}")


def _has_test_file(filepath: Path) -> bool:
    """检查是否存在对应的测试文件"""
    name = filepath.stem
    candidates = [
        TESTS_DIR / f"test_{name}.py",
        TESTS_DIR / f"{name}_test.py",
        filepath.parent / f"test_{name}.py",
        filepath.parent / f"{name}_test.py",
    ]
    return any(c.exists() for c in candidates)


def _check_header(content: str) -> Dict[str, Any]:
    """检查文件头是否包含 DNA / 创建者 / 协议三行"""
    head_lines = content.split("\n")[:30]
    head_text = "\n".join(head_lines).lower()

    has_dna = (
        any("dna:" in line.lower() or "dna " in line.lower() for line in head_lines)
        or any(re.search(r'#龍芯\S+', line) for line in head_lines)
    )
    has_creator = "创建者" in head_text or "creator" in head_text
    has_protocol = "协议" in head_text or "protocol" in head_text or "cc by-nc-sa" in head_text

    return {
        "has_dna": has_dna,
        "has_creator": has_creator,
        "has_protocol": has_protocol,
        "passed": has_dna and has_creator and has_protocol,
        "missing": [k for k, v in {
            "dna": has_dna,
            "creator": has_creator,
            "protocol": has_protocol,
        }.items() if not v],
    }


def _extract_dna(content: str) -> Optional[str]:
    """从文件头提取 DNA 字符串"""
    for line in content.split("\n")[:50]:
        m = re.search(r'DNA[:\s]+(#龍芯[^\n]+)', line)
        if m:
            return m.group(1).strip()
        # 兼容注释格式 # DNA: ...
        m2 = re.search(r'(#龍芯⚡️[^\n]+)', line)
        if m2:
            return m2.group(1).strip()
    return None


def check_engine(entry: Dict[str, Any]) -> Dict[str, Any]:
    """检查单个引擎条目的完整性"""
    result: Dict[str, Any] = {
        "id": entry.get("id"),
        "name": entry.get("name"),
        "path": entry.get("path"),
        "checks": {},
        "issues": [],
        "passed": True,
        "severity": "ok",
    }

    path_str = entry.get("path", "")
    filepath = ROOT / path_str
    dna_registered = entry.get("dna", "")
    description = entry.get("description", "")
    imports = entry.get("imports", [])
    functions = entry.get("functions", [])
    classes = entry.get("classes", [])

    # 1. DNA 格式检查
    dna_check: Dict[str, Any] = {"registered": dna_registered}
    if dna_registered and dna_registered != "未注册":
        dna_check["format_valid"] = bool(DNA_REGEX.match(dna_registered))
    else:
        dna_check["format_valid"] = False
        dna_check["reason"] = "未注册"
    result["checks"]["dna_format"] = dna_check
    if not dna_check["format_valid"]:
        result["issues"].append({
            "type": "dna_format",
            "severity": "critical",
            "message": f"DNA 格式无效或缺失: {dna_registered}",
        })
        result["severity"] = "critical"

    # 2. 文件头检查
    header_check: Dict[str, Any] = {"file_exists": filepath.exists()}
    if filepath.exists():
        try:
            content = filepath.read_text(encoding="utf-8")
            header_check.update(_check_header(content))
            # 交叉校验文件头 DNA 与注册表 DNA
            file_dna = _extract_dna(content)
            header_check["file_dna"] = file_dna
            header_check["dna_matches_registry"] = file_dna == dna_registered if file_dna else False
        except (UnicodeDecodeError, PermissionError):
            header_check["passed"] = False
            header_check["error"] = "无法读取文件"
    else:
        header_check["passed"] = False
        header_check["error"] = "源文件不存在"

    result["checks"]["file_header"] = header_check
    if not header_check.get("passed", False):
        result["issues"].append({
            "type": "file_header",
            "severity": "critical",
            "message": header_check.get("error", "文件头缺少 DNA/创建者/协议信息"),
        })
        result["severity"] = "critical"
    elif not header_check.get("dna_matches_registry", True):
        result["issues"].append({
            "type": "dna_mismatch",
            "severity": "critical",
            "message": "文件头 DNA 与注册表 DNA 不一致",
        })
        result["severity"] = "critical"

    # 3. 描述长度检查
    desc_len = len(description) if description else 0
    desc_check = {"length": desc_len, "min_required": 20}
    desc_check["passed"] = desc_len >= 20 and description != "（无描述）"
    result["checks"]["description"] = desc_check
    if not desc_check["passed"]:
        result["issues"].append({
            "type": "description",
            "severity": "warning",
            "message": f"描述过短 ({desc_len} 字符)，建议 >= 20 字符",
        })
        if result["severity"] == "ok":
            result["severity"] = "warning"

    # 4. 测试文件检查
    has_test = _has_test_file(filepath)
    test_check = {"has_test_file": has_test}
    result["checks"]["test_file"] = test_check
    if not has_test:
        result["issues"].append({
            "type": "test_file",
            "severity": "warning",
            "message": "未找到对应测试文件 (tests/test_*.py 或同级 test_*.py)",
        })
        if result["severity"] == "ok":
            result["severity"] = "warning"

    # 5. 孤立文件检查
    is_isolated = len(imports) == 0 and len(functions) == 0 and len(classes) == 0
    isolated_check = {
        "is_isolated": is_isolated,
        "imports_count": len(imports),
        "functions_count": len(functions),
        "classes_count": len(classes),
    }
    result["checks"]["isolated"] = isolated_check
    if is_isolated:
        result["issues"].append({
            "type": "isolated",
            "severity": "high",
            "message": "孤立文件：无 imports、functions、classes",
        })
        if result["severity"] not in ("critical",):
            result["severity"] = "high"

    # 综合判定
    result["passed"] = result["severity"] in ("ok", "warning")
    return result


def run_integrity_check(registry: Dict[str, Any]) -> Dict[str, Any]:
    """执行完整性检查"""
    _log("开始完整性检查...", "CHECK")

    engines = registry.get("engines", [])
    results: List[Dict[str, Any]] = []
    stats = {
        "total": len(engines),
        "passed": 0,
        "failed": 0,
        "critical": 0,
        "high": 0,
        "warning": 0,
        "ok": 0,
        "dna_format_invalid": 0,
        "header_missing": 0,
        "description_too_short": 0,
        "missing_test": 0,
        "isolated": 0,
    }

    for eng in engines:
        res = check_engine(eng)
        results.append(res)

        severity = res["severity"]
        stats[severity] += 1
        if res["passed"]:
            stats["passed"] += 1
        else:
            stats["failed"] += 1

        for issue in res["issues"]:
            if issue["type"] == "dna_format":
                stats["dna_format_invalid"] += 1
            elif issue["type"] == "file_header":
                stats["header_missing"] += 1
            elif issue["type"] == "description":
                stats["description_too_short"] += 1
            elif issue["type"] == "test_file":
                stats["missing_test"] += 1
            elif issue["type"] == "isolated":
                stats["isolated"] += 1

    report = {
        "dna": DNA,
        "version": SCHEMA_VERSION,
        "schema_version": SCHEMA_VERSION,
        "generated_at": _now(),
        "source_registry": registry.get("dna", "unknown"),
        "stats": stats,
        "results": results,
    }

    _log(
        f"检查完成: 通过 {stats['passed']} · 失败 {stats['failed']} · "
        f"关键 {stats['critical']} · 高 {stats['high']} · 警告 {stats['warning']}",
        "OK" if stats["failed"] == 0 else "WARN",
    )
    return report


def save_report(report: Dict[str, Any], dry_run: bool):
    """保存完整性报告"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if dry_run:
        _log(f"[DRY-RUN] 不写入文件: {INTEGRITY_REPORT_FILE}", "SKIP")
        return

    with open(INTEGRITY_REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    _log(f"已保存: {INTEGRITY_REPORT_FILE}", "OK")


def main():
    parser = argparse.ArgumentParser(description="龍魂 Notion 引擎完整性检查器")
    parser.add_argument("--registry", type=Path, default=REGISTRY_FILE,
                        help="输入注册表路径 (默认: data/notion_sync/engines/engine_registry.json)")
    parser.add_argument("--dry-run", action="store_true",
                        help="仅打印结果，不保存报告")
    args = parser.parse_args()

    print(f"\n{DNA}\n")

    if not args.registry.exists():
        _log(f"注册表不存在: {args.registry}", "ERROR")
        sys.exit(1)

    with open(args.registry, "r", encoding="utf-8") as f:
        registry = json.load(f)

    report = run_integrity_check(registry)

    print("\n📊 完整性统计:")
    print(f"  总数: {report['stats']['total']}")
    print(f"  通过: {report['stats']['passed']}")
    print(f"  失败: {report['stats']['failed']}")
    print(f"  关键问题: {report['stats']['critical']}")
    print(f"  高优先级: {report['stats']['high']}")
    print(f"  警告: {report['stats']['warning']}")
    print(f"\n🔍 详细问题:")
    print(f"  DNA 格式无效: {report['stats']['dna_format_invalid']}")
    print(f"  文件头缺失: {report['stats']['header_missing']}")
    print(f"  描述过短: {report['stats']['description_too_short']}")
    print(f"  缺少测试: {report['stats']['missing_test']}")
    print(f"  孤立文件: {report['stats']['isolated']}")

    save_report(report, args.dry_run)

    if report["stats"]["failed"] > 0:
        _log("检测到严重问题，退出码非零", "ERROR")
        sys.exit(1)

    _log("完成", "OK")


if __name__ == "__main__":
    main()
