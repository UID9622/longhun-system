#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上帝之眼·守护者 P-AK-GUARDIAN
功能：文件完整性监控 / DNA 校验 / 红线规则 / 三色审计 / 审计看板
DNA: #GUARDIAN-AGENT-CONFIG-20251214-001
"""
import argparse
import json
import os
import re
import signal
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import AuditMark, DNATracer, TelemetryCollector, TricolorAudit, hash_file, load_config, setup_logging, workspace_root


PERSONA_CODE = "GUARDIAN"
PERSONA_NAME = "上帝之眼·守护者 P-AK-GUARDIAN"
AGENT_DNA = "#GUARDIAN-AGENT-CONFIG-20251214-001"

CONFIG = load_config()
WORKSPACE = Path(CONFIG.get("workspace", workspace_root()))
LOG_FILE = Path(CONFIG.get("logs_dir", WORKSPACE / "logs")) / "guardian.log"
DEFAULT_AUDIT = Path(CONFIG.get("audit_dir", WORKSPACE / "logs" / "audit"))
RULES_FILE = Path(__file__).parent / "rules.json"
BASELINE_FILE = Path(__file__).parent / ".file_baseline.json"

DNA_PATTERN = re.compile(r"^#[A-Z0-9_]+-[A-Z0-9_]+-CONFIG-\d{8}-\d{3}$")
_shutdown = threading.Event()


def load_rules(path: Path) -> Dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {
        "red_lines": [],
        "detection_patterns": {},
        "thresholds": {"complaint_trigger_count": 3},
        "monitoring_config": {"check_interval_seconds": 60, "excluded_patterns": []},
    }


def compile_excluded(patterns: List[str]):
    return [re.compile(p) for p in patterns]


def should_skip(path: Path, excluded: List[re.Pattern]) -> bool:
    s = str(path)
    return any(p.search(s) for p in excluded)


def collect_files(watch_dirs: List[Path], excluded: List[re.Pattern]) -> List[Path]:
    files = []
    for d in watch_dirs:
        if not d.exists():
            continue
        for root, _, names in os.walk(d):
            for name in names:
                if name.startswith(".") or name.endswith("~"):
                    continue
                p = Path(root) / name
                if should_skip(p, excluded):
                    continue
                files.append(p)
    return files


def load_baseline() -> Dict[str, str]:
    if BASELINE_FILE.exists():
        try:
            return json.loads(BASELINE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_baseline(baseline: Dict[str, str]):
    BASELINE_FILE.write_text(json.dumps(baseline, ensure_ascii=False, indent=2), encoding="utf-8")


def check_integrity(watch_dirs: List[Path], excluded: List[re.Pattern]) -> Tuple[List[str], List[str], List[str], List[str]]:
    current_files = collect_files(watch_dirs, excluded)
    current_hashes: Dict[str, str] = {}
    unchanged, new_files, modified, deleted = [], [], [], []
    baseline = load_baseline()

    for f in current_files:
        h = hash_file(f)
        rel = str(f.relative_to(WORKSPACE)) if str(f).startswith(str(WORKSPACE)) else str(f)
        current_hashes[rel] = h
        if rel not in baseline:
            new_files.append(rel)
        elif baseline[rel] != h:
            modified.append(rel)
        else:
            unchanged.append(rel)

    for rel in baseline:
        if rel not in current_hashes:
            deleted.append(rel)

    save_baseline(current_hashes)
    return unchanged, new_files, modified, deleted


def validate_dna(text: str) -> List[Tuple[str, bool]]:
    results = []
    for dna in re.findall(r"#[A-Z0-9_]+-[A-Z0-9_]+(?:-[A-Z0-9_]+)*-\d{8}-\d{3}", text):
        results.append((dna, bool(DNA_PATTERN.match(dna))))
    return results


def check_red_lines(text: str, rules: Dict) -> List[Dict]:
    triggers = []
    patterns = rules.get("detection_patterns", {})
    red_lines = {rl["pattern"]: rl for rl in rules.get("red_lines", []) if rl.get("enabled")}
    for pattern_name, regex_list in patterns.items():
        if pattern_name not in red_lines:
            continue
        for regex in regex_list:
            if re.search(regex, text, re.I):
                triggers.append({
                    "rule_id": red_lines[pattern_name]["id"],
                    "rule_name": red_lines[pattern_name]["name"],
                    "action": red_lines[pattern_name]["action"],
                    "matched_pattern": regex,
                })
    return triggers


def write_dashboard(audit: TricolorAudit, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    dashboard_path = output_dir / "guardian_dashboard.json"
    dashboard_path.write_text(json.dumps(audit.dashboard(), ensure_ascii=False, indent=2), encoding="utf-8")


def run_check(watch_dirs: List[Path], audit: TricolorAudit, rules: Dict, logger) -> Dict[str, int]:
    excluded = compile_excluded(rules.get("monitoring_config", {}).get("excluded_patterns", []))
    unchanged, new_files, modified, deleted = check_integrity(watch_dirs, excluded)

    for f in new_files:
        logger.warning(AuditMark.tag(AuditMark.YELLOW, PERSONA_NAME, f"新文件: {f}"))
        audit.yellow(PERSONA_NAME, "NEW_FILE", {"path": f})
    for f in modified:
        logger.error(AuditMark.tag(AuditMark.RED, PERSONA_NAME, f"完整性异常: {f}"))
        audit.red(PERSONA_NAME, "FILE_MODIFIED", {"path": f})
    for f in deleted:
        logger.error(AuditMark.tag(AuditMark.RED, PERSONA_NAME, f"文件缺失: {f}"))
        audit.red(PERSONA_NAME, "FILE_DELETED", {"path": f})

    # DNA validation in files
    for f in collect_files(watch_dirs, excluded):
        if f.suffix not in {".md", ".txt", ".json", ".py"}:
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        dna_results = validate_dna(text)
        for dna, valid in dna_results:
            if not valid:
                logger.error(AuditMark.tag(AuditMark.RED, PERSONA_NAME, f"DNA 格式异常: {dna} in {f}"))
                audit.red(PERSONA_NAME, "DNA_INVALID", {"path": str(f), "dna": dna})

        triggers = check_red_lines(text, rules)
        for t in triggers:
            action = "阻断" if t["action"] == "BLOCK" else "触发陪审团"
            logger.critical(AuditMark.tag(AuditMark.RED, PERSONA_NAME, f"触发红线 {t['rule_id']}: {t['rule_name']} -> {action}"))
            audit.red(PERSONA_NAME, "RED_LINE", {"rule": t["rule_id"], "path": str(f)})

    if not (new_files or modified or deleted):
        logger.info(AuditMark.tag(AuditMark.GREEN, PERSONA_NAME, "完整性检查通过"))
        audit.green(PERSONA_NAME, "CHECK_OK", {"unchanged": len(unchanged)})

    write_dashboard(audit, WORKSPACE / "data" / "guardian")
    return {
        "new_files": len(new_files),
        "modified": len(modified),
        "deleted": len(deleted),
        "unchanged": len(unchanged),
    }


def main():
    parser = argparse.ArgumentParser(description=PERSONA_NAME)
    parser.add_argument("--check", action="store_true", help="执行一次完整检查")
    parser.add_argument("--daemon", action="store_true", help="守护模式")
    parser.add_argument("--watch-dir", action="append", help="监控目录（可多次）")
    parser.add_argument("--audit-dir", default=str(DEFAULT_AUDIT), help="审计目录")
    parser.add_argument("--interval", type=int, default=60, help="检查间隔（秒）")
    parser.add_argument("--verbose", action="store_true", help="详细日志")
    args = parser.parse_args()

    logger = setup_logging("guardian", LOG_FILE, verbose=args.verbose)
    dna = DNATracer(PERSONA_CODE, AGENT_DNA)
    audit = TricolorAudit(Path(args.audit_dir))
    rules = load_rules(RULES_FILE)
    telemetry = TelemetryCollector(PERSONA_CODE, PERSONA_NAME, operation_type="CHECK")

    watch_dirs = [Path(d).expanduser().resolve() for d in args.watch_dir] if args.watch_dir else [WORKSPACE]

    logger.info(AuditMark.tag(AuditMark.PURPLE, PERSONA_NAME, "启动"))

    def handle_signal(signum, frame):
        logger.info(AuditMark.tag(AuditMark.YELLOW, PERSONA_NAME, f"收到信号 {signum}，准备退出"))
        _shutdown.set()

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    total_new = 0
    total_modified = 0
    total_deleted = 0
    total_red = 0
    total_yellow = 0

    try:
        while True:
            loop_metrics = run_check(watch_dirs, audit, rules, logger)
            op_dna = dna.generate("CHECK")
            logger.info(AuditMark.tag(AuditMark.BLUE, PERSONA_NAME, f"检查完成 DNA: {op_dna}"))

            # 从审计看板读取累计事件数
            dash = audit.dashboard()
            counts = dash.get("counts", {})
            total_red = counts.get("red", 0)
            total_yellow = counts.get("yellow", 0)

            total_new += loop_metrics.get("new_files", 0)
            total_modified += loop_metrics.get("modified", 0)
            total_deleted += loop_metrics.get("deleted", 0)

            telemetry.event("CHECK_LOOP", {"red": total_red, "yellow": total_yellow, "dna": op_dna})

            if not args.daemon:
                break
            if _shutdown.wait(args.interval):
                break

        telemetry.set_metrics({
            "new_files": total_new,
            "modified": total_modified,
            "deleted": total_deleted,
            "red_events": total_red,
            "yellow_events": total_yellow,
        })
    except Exception as e:
        logger.error(AuditMark.tag(AuditMark.RED, PERSONA_NAME, f"检查失败: {e}"))
        telemetry.finish("error", {"error": str(e)})
        raise
    finally:
        if not telemetry._finished:
            telemetry.finish("success")

    logger.info(AuditMark.tag(AuditMark.PURPLE, PERSONA_NAME, "退出"))


if __name__ == "__main__":
    main()
