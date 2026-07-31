#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 Notion 下载自动轮转器

自动把 P1→P4 按 chunk 跑完，每 chunk 后自动更新索引、缺失报告、画廊。
老大授权，一键后台，无需人工干预。

DNA: #龍芯⚡️2026-06-23-NOTION-ORCHESTRATOR-v1.0
"""
from __future__ import annotations

import pathlib
import re
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta

HOME = pathlib.Path.home()
ROOT = pathlib.Path("/Users/zuimeidedeyihan/longhun-system")
DB_PATH = HOME / ".longhun" / "notion_pages" / "notion_pages.db"
LOG_PATH = HOME / ".longhun" / "notion_pages" / "orchestrator.log"
CHUNK_SIZE = 80
MAX_BLOCKS = 500
PHASES = ["P1", "P2", "P3", "P4"]
CST = timezone(timedelta(hours=8))


def now_iso() -> str:
    return datetime.now(CST).isoformat()


def log(msg: str) -> None:
    line = f"[{now_iso()}] {msg}"
    print(line)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def run(cmd: list[str], timeout: int | None = 3600) -> int:
    log(f"RUN {' '.join(cmd)}")
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if proc.stdout:
        for line in proc.stdout.splitlines():
            log(f"  OUT {line}")
    if proc.stderr:
        for line in proc.stderr.splitlines():
            log(f"  ERR {line}")
    log(f"  EXIT {proc.returncode}")
    return proc.returncode


def count_pending_in_index(phase: str) -> int:
    """通过 downloader 的 dry-run 统计该阶段剩余页数。"""
    try:
        proc = subprocess.run(
            [sys.executable, "scripts/notion_downloader.py", "--phase", phase, "--dry-run"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=120,
        )
        # 解析输出，例如 "阶段 P2: 共 500 页待处理（索引总计 2404）"
        for line in proc.stdout.splitlines():
            if "共" in line and "页待处理" in line:
                m = re.search(r"共\s*(\d+)\s*页待处理", line)
                if m:
                    return int(m.group(1))
        return 0
    except Exception as e:
        log(f"Index count error: {e}")
        return 0


def update_artifacts() -> None:
    log("--- update artifacts ---")
    run([sys.executable, "scripts/longhun_kb.py", "index", "--force"], timeout=300)
    run([sys.executable, "scripts/notion_missing_report.py"], timeout=300)
    run([sys.executable, "scripts/longhun_kb.py", "gallery"], timeout=300)
    run([sys.executable, "scripts/notion_knowledge_graph.py"], timeout=300)


def run_phase(phase: str) -> None:
    log(f"\n========== PHASE {phase} ==========")
    while True:
        pending = count_pending_in_index(phase)
        log(f"{phase} pending in index: {pending}")
        if pending <= 0:
            log(f"{phase} done.")
            break
        limit = min(CHUNK_SIZE, pending)
        rc = run(
            [
                sys.executable,
                "scripts/notion_downloader.py",
                "--phase",
                phase,
                "--limit",
                str(limit),
                "--max-blocks",
                str(MAX_BLOCKS),
            ],
            timeout=7200,
        )
        update_artifacts()
        if rc != 0:
            log(f"{phase} chunk returned {rc}, will retry next iteration.")


def main() -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    log("=" * 50)
    log("Orchestrator started")
    log(f"DNA: #龍芯⚡️2026-06-23-NOTION-ORCHESTRATOR-v1.0")

    # 先同步一次当前状态
    update_artifacts()

    for phase in PHASES:
        run_phase(phase)

    log("\n========== ALL PHASES DONE ==========")
    update_artifacts()
    log("Orchestrator finished.")


if __name__ == "__main__":
    main()
