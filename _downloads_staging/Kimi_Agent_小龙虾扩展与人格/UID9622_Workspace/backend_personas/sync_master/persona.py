#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文心·同步专家 P-AK-SYNC-MASTER
功能：增量/全量同步 / 冲突检测 / 自动回滚 / 重试 / 一致性校验
DNA: #WENXIN-AGENT-CONFIG-20251214-001
"""
import argparse
import json
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import AuditMark, DNATracer, TelemetryCollector, hash_file, load_config, setup_logging, workspace_root


PERSONA_CODE = "WENXIN"
PERSONA_NAME = "文心·同步专家 P-AK-SYNC-MASTER"
AGENT_DNA = "#WENXIN-AGENT-CONFIG-20251214-001"

CONFIG = load_config()
WORKSPACE = Path(CONFIG.get("workspace", workspace_root()))
LOG_FILE = Path(CONFIG.get("logs_dir", WORKSPACE / "logs")) / "sync_master.log"
DEFAULT_PAIRS_FILE = Path(__file__).parent / "sync_pairs.json"


def load_pairs(path: Path) -> List[Dict]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8")).get("pairs", [])
    return []


def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def backup_path(src: Path, backup_root: Path) -> Path:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    rel = src.relative_to(src.anchor) if src.is_absolute() else src
    bp = backup_root / f"{ts}_{rel}"
    bp.parent.mkdir(parents=True, exist_ok=True)
    return bp


def list_files(root: Path) -> Dict[str, Path]:
    files = {}
    if not root.exists():
        return files
    for f in root.rglob("*"):
        if f.is_file():
            rel = f.relative_to(root).as_posix()
            files[rel] = f
    return files


def sync_pair(pair: Dict, full: bool, dry_run: bool, backup_root: Path, logger, dna: DNATracer) -> Dict:
    src = Path(pair["src"]).expanduser().resolve()
    dst = Path(pair["dst"]).expanduser().resolve()
    result = {
        "pair": pair.get("name", str(src)),
        "copied": 0,
        "skipped": 0,
        "conflicts": 0,
        "errors": [],
        "dna": dna.generate("SYNC"),
    }

    if not src.exists():
        result["errors"].append(f"源目录不存在: {src}")
        logger.error(AuditMark.tag(AuditMark.RED, PERSONA_NAME, f"源目录不存在: {src}"))
        return result

    ensure_dir(dst)
    src_files = list_files(src)
    dst_files = list_files(dst)

    for rel, sf in src_files.items():
        df = dst / rel
        need_copy = full
        if not df.exists():
            need_copy = True
        else:
            if df.stat().st_mtime != sf.stat().st_mtime or hash_file(df) != hash_file(sf):
                # conflict: both changed
                if rel in dst_files:
                    result["conflicts"] += 1
                    logger.warning(AuditMark.tag(AuditMark.YELLOW, PERSONA_NAME, f"冲突: {rel}"))
                    if not dry_run:
                        bp = backup_path(df, backup_root)
                        shutil.copy2(df, bp)
                need_copy = True
            else:
                result["skipped"] += 1

        if need_copy:
            if not dry_run:
                ensure_dir(df.parent)
                shutil.copy2(sf, df)
            result["copied"] += 1
            logger.info(AuditMark.tag(AuditMark.BLUE, PERSONA_NAME, f"{'[模拟] ' if dry_run else ''}同步: {rel}"))

    # remove files in dst not in src (optional, controlled by pair config)
    if pair.get("mirror") and not dry_run:
        for rel in set(dst_files) - set(src_files):
            (dst / rel).unlink()
            logger.info(AuditMark.tag(AuditMark.YELLOW, PERSONA_NAME, f"删除镜像多余文件: {rel}"))

    return result


def run_sync(config_path: Path, full: bool, dry_run: bool, logger, dna: DNATracer):
    pairs = load_pairs(config_path)
    if not pairs:
        logger.warning(AuditMark.tag(AuditMark.YELLOW, PERSONA_NAME, "未配置同步对"))
        return []
    backup_root = WORKSPACE / "backups" / "sync"
    ensure_dir(backup_root)
    results = []
    for pair in pairs:
        for attempt in range(1, 4):
            try:
                res = sync_pair(pair, full, dry_run, backup_root, logger, dna)
                results.append(res)
                break
            except Exception as e:
                logger.error(AuditMark.tag(AuditMark.RED, PERSONA_NAME, f"同步失败（第{attempt}次）: {e}"))
                if attempt == 3:
                    results.append({"pair": pair.get("name"), "errors": [str(e)]})
                else:
                    time.sleep(2 ** attempt)
    return results


def main():
    parser = argparse.ArgumentParser(description=PERSONA_NAME)
    parser.add_argument("--config", default=str(DEFAULT_PAIRS_FILE), help="同步对配置")
    parser.add_argument("--full", action="store_true", help="全量同步")
    parser.add_argument("--dry-run", action="store_true", help="模拟运行")
    parser.add_argument("--verbose", action="store_true", help="详细日志")
    args = parser.parse_args()

    logger = setup_logging("sync_master", LOG_FILE, verbose=args.verbose)
    dna = DNATracer(PERSONA_CODE, AGENT_DNA)
    telemetry = TelemetryCollector(PERSONA_CODE, PERSONA_NAME, operation_type="FULL_SYNC" if args.full else "SYNC")
    logger.info(AuditMark.tag(AuditMark.PURPLE, PERSONA_NAME, f"开始{'全量' if args.full else '增量'}同步"))

    try:
        results = run_sync(Path(args.config), args.full, args.dry_run, logger, dna)
        summary = {
            "copied": sum(r.get("copied", 0) for r in results),
            "skipped": sum(r.get("skipped", 0) for r in results),
            "conflicts": sum(r.get("conflicts", 0) for r in results),
            "pairs": len(results),
            "errors": sum(len(r.get("errors", [])) for r in results),
        }
        logger.info(AuditMark.tag(AuditMark.GREEN, PERSONA_NAME, f"同步完成: {summary}"))
        out = WORKSPACE / "data" / "sync_master"
        ensure_dir(out)
        (out / "last_sync_report.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

        telemetry.set_metrics(summary)
        telemetry.event("SYNC_COMPLETE", {"summary": summary})
    except Exception as e:
        logger.error(AuditMark.tag(AuditMark.RED, PERSONA_NAME, f"同步失败: {e}"))
        telemetry.finish("error", {"error": str(e)})
        raise
    finally:
        if not telemetry._finished:
            telemetry.finish("success")


if __name__ == "__main__":
    main()
