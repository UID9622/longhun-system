#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
雯雯·技术整理师 P-AK-WENWEN
功能：文档扫描 / 智能分类 / 内容哈希去重 / 安全脱敏 / 报告生成
DNA: #WENWEN-AGENT-CONFIG-20251214-001
"""
import argparse
import json
import os
import shutil
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Set, Tuple

# 公共核心库
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import AuditMark, DNATracer, SecurityFilter, TelemetryCollector, hash_file, load_config, setup_logging, workspace_root


PERSONA_CODE = "WENWEN"
PERSONA_NAME = "雯雯·技术整理师 P-AK-WENWEN"
AGENT_DNA = "#WENWEN-AGENT-CONFIG-20251214-001"

CONFIG = load_config()
WORKSPACE = Path(CONFIG.get("workspace", workspace_root()))
LOG_FILE = Path(CONFIG.get("logs_dir", WORKSPACE / "logs")) / "wenwen.log"
DEFAULT_SCAN_DIR = WORKSPACE
DEFAULT_OUTPUT_DIR = WORKSPACE / "organized"
SUPPORTED = {".md", ".txt", ".json", ".py", ".sh", ".yaml", ".yml"}
MAX_SIZE = 10 * 1024 * 1024

CATEGORIES = {
    "人格系统": ["persona", "人格", "角色", "agent", "prompt", "性格", "mission"],
    "数据管理": ["database", "数据库", "data", "storage", "backup", "archive", "index", "query"],
    "技术实现": ["code", "implementation", "api", "python", "javascript", "deploy", "config", "docker"],
    "项目文档": ["readme", "plan", "roadmap", "requirement", "spec", "todo"],
}


def classify(filepath: Path, content: str) -> str:
    text = f"{filepath.name} {content[:2000]}".lower()
    scores = defaultdict(float)
    for cat, kws in CATEGORIES.items():
        for kw in kws:
            scores[cat] += text.count(kw.lower())
            if kw.lower() in filepath.name.lower():
                scores[cat] += 5
    if not scores or max(scores.values()) == 0:
        return "其他"
    return max(scores, key=scores.get)


def scan_files(scan_dir: Path) -> List[Path]:
    files = []
    for root, _, names in os.walk(scan_dir):
        # 避免扫描自身输出目录造成循环
        if Path(root).resolve() == DEFAULT_OUTPUT_DIR.resolve():
            continue
        for name in names:
            if name.startswith(".") or name.endswith("~"):
                continue
            p = Path(root) / name
            if p.suffix.lower() not in SUPPORTED:
                continue
            if p.stat().st_size > MAX_SIZE:
                continue
            files.append(p)
    return sorted(files)


def build_index(files: List[Path], auth_safe: bool) -> Tuple[List[Dict], Dict[str, List[Path]]]:
    records = []
    duplicates: Dict[str, List[Path]] = defaultdict(list)
    dna = DNATracer(PERSONA_CODE, AGENT_DNA)
    for f in files:
        raw = f.read_text(encoding="utf-8", errors="replace")
        content = SecurityFilter.sanitize(raw) if auth_safe else raw
        h = hash_file(f)
        duplicates[h].append(f)
        rec = dna.stamp(
            {
                "path": str(f),
                "size": f.stat().st_size,
                "sha256": h,
                "category": classify(f, content),
                "filename": f.name,
            },
            "FILE",
        )
        records.append(rec)
    return records, duplicates


def generate_report(records: List[Dict], duplicates: Dict[str, List[Path]], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    categories = defaultdict(list)
    for r in records:
        categories[r["category"]].append(r)

    dup_groups = [group for group in duplicates.values() if len(group) > 1]

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    report_path = output_dir / f"wenwen_report_{ts}.md"
    lines = [
        "# 雯雯·技术整理报告\n",
        f"- 生成时间: {datetime.now(timezone.utc).isoformat()}",
        f"- DNA: {AGENT_DNA}",
        f"- 扫描文件: {len(records)}",
        f"- 重复组: {len(dup_groups)}\n",
        "## 分类统计\n",
    ]
    for cat in sorted(categories):
        lines.append(f"### {cat} ({len(categories[cat])})")
        for r in categories[cat]:
            lines.append(f"- `{r['path']}` · {r['size']} bytes · `{r['sha256'][:16]}` · {r.get('dna_trace','')}")
        lines.append("")

    if dup_groups:
        lines.append("## 重复文件检测\n")
        for group in dup_groups:
            lines.append(f"- 哈希 `{hash_file(group[0])[:16]}...` 出现 {len(group)} 次:")
            for p in group:
                lines.append(f"  - {p}")
            lines.append("")
    else:
        lines.append("## 重复文件检测\n未发现重复文件。\n")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def generate_dedup_script(duplicates: Dict[str, List[Path]], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    script = output_dir / "dedup_script.sh"
    lines = ["#!/bin/bash", "# 雯雯生成的去重脚本，执行前请人工确认", ""]
    for group in duplicates.values():
        if len(group) <= 1:
            continue
        keep = group[0]
        for dup in group[1:]:
            lines.append(f"# rm -v '{dup}'  # 与 '{keep}' 重复")
    lines.append("")
    script.write_text("\n".join(lines), encoding="utf-8")
    script.chmod(0o755)
    return script


def generate_json_index(records: List[Dict], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    index_path = output_dir / "wenwen_index.json"
    index_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    return index_path


def disk_usage_percent(path: Path) -> float:
    try:
        st = os.statvfs(path)
        return (st.f_blocks - st.f_bavail) / st.f_blocks * 100
    except Exception:
        return 0.0


def main():
    parser = argparse.ArgumentParser(description=PERSONA_NAME)
    parser.add_argument("--scan-dir", default=str(DEFAULT_SCAN_DIR), help="扫描目录")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="输出目录")
    parser.add_argument("--auth-safe", action="store_true", help="启用敏感信息脱敏")
    parser.add_argument("--report", action="store_true", help="生成 Markdown 报告")
    parser.add_argument("--dedup", action="store_true", help="生成去重脚本")
    parser.add_argument("--verbose", action="store_true", help="详细日志")
    args = parser.parse_args()

    logger = setup_logging("wenwen", LOG_FILE, verbose=args.verbose)
    dna = DNATracer(PERSONA_CODE, AGENT_DNA)
    telemetry = TelemetryCollector(PERSONA_CODE, PERSONA_NAME, operation_type="ORGANIZE")
    logger.info(AuditMark.tag(AuditMark.PURPLE, PERSONA_NAME, "启动扫描"))

    try:
        scan_dir = Path(args.scan_dir).expanduser().resolve()
        output_dir = Path(args.output_dir).expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

        usage = disk_usage_percent(scan_dir)
        if usage > 80:
            logger.warning(AuditMark.tag(AuditMark.YELLOW, PERSONA_NAME, f"磁盘使用率 {usage:.1f}%，触发紧急整理"))

        files = scan_files(scan_dir)
        logger.info(AuditMark.tag(AuditMark.BLUE, PERSONA_NAME, f"扫描到 {len(files)} 个文件"))

        records, duplicates = build_index(files, args.auth_safe)
        dup_groups = [g for g in duplicates.values() if len(g) > 1]
        index_path = generate_json_index(records, output_dir)
        logger.info(AuditMark.tag(AuditMark.GREEN, PERSONA_NAME, f"索引已保存: {index_path}"))

        categories = defaultdict(list)
        for r in records:
            categories[r["category"]].append(r)

        if args.report:
            report_path = generate_report(records, duplicates, output_dir)
            logger.info(AuditMark.tag(AuditMark.GREEN, PERSONA_NAME, f"报告已保存: {report_path}"))

        if args.dedup:
            script_path = generate_dedup_script(duplicates, output_dir)
            logger.info(AuditMark.tag(AuditMark.YELLOW, PERSONA_NAME, f"去重脚本已生成: {script_path}"))

        op_dna = dna.generate("ORGANIZE")
        logger.info(AuditMark.tag(AuditMark.BLUE, PERSONA_NAME, f"整理完成 DNA: {op_dna}"))

        telemetry.set_metrics({
            "records": len(records),
            "duplicates": len(dup_groups),
            "categories": len(categories),
            "disk_usage": round(usage, 2),
        })
        telemetry.event("ORGANIZE_COMPLETE", {"dna": op_dna, "index": str(index_path)})
    except Exception as e:
        logger.error(AuditMark.tag(AuditMark.RED, PERSONA_NAME, f"运行失败: {e}"))
        telemetry.finish("error", {"error": str(e)})
        raise
    finally:
        if not telemetry._finished:
            telemetry.finish("success")


if __name__ == "__main__":
    main()
