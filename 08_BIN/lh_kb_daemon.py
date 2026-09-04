#!/usr/bin/env python3
# DNA: #龍芯⚡️2026-08-30-KB-DAEMON-v1.1-INCREMENTAL-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 · 知识库增量常驻守护 v1.1
──────────────────────────────────────────────
定时(launchd 每6h)检测 story_factory 新产出 → 幂等入库 train_merged + md 知识卡。
设计要点(节能协议):
  - 非空转: launchd 定时触发 --once，跑完即退，不常驻占 CPU
  - 增量: 仅入库内容指纹不在库中的新样本（幂等·与 feed/ingest 同一指纹键）
  - 静默: 无新产出 → 输出一行 `✅ 无新增`；有增量 → 一行统计
  - 审计: 状态写入 audit/kb_daemon_state.json（供巡检/仪表盘查询）

v1.1 工程审查修复(2026-08-30 P04鲁班 · 吸收 P00/P01 意见):
  - 幂等键 → 内容指纹(与 lh_asi_feed 同一键·去重逻辑唯一化)
  - 增量入库后重建 INDEX.md(全量·含所有域·P00 P0-4)
  - 路径基于 __file__ 推导项目根(不依赖 launchd WorkingDirectory)

⚠️ 并发约束(P01 #3)：本守护与手动 lh_kb_ingest.py 为同一写路径，当前无 flock 排它锁；
   请勿在手动 ingest 期间触发 daemon，避免 TOCTOU 双写窗口（对账工具 reconcile 规划中）。

用法:
    python3 08_BIN/lh_kb_daemon.py --once
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_BIN = str(Path(__file__).resolve().parent)
if _BIN not in sys.path:
    sys.path.insert(0, _BIN)

from lh_kb_common import content_fingerprint, existing_fingerprints, now_utc, rebuild_index

_ROOT = Path(_BIN).parent

STORY_DIR = _ROOT / "08_BIN" / "story_factory" / "output"
KB_ROOT = _ROOT / "11_DATA" / "knowledge_base"
TRAIN_MERGED = _ROOT / "11_DATA" / "bootstrap" / "train_merged.jsonl"
STATE_FILE = _ROOT / "audit" / "kb_daemon_state.json"


def _load_candidates() -> list:
    """收集 story_factory 全部产出（跨文件去重）"""
    from lh_kb_ingest import collect_story_sources
    return collect_story_sources()


def main() -> None:
    p = argparse.ArgumentParser(prog="lh_kb_daemon", description="知识库增量守护 v1.1")
    p.add_argument("--once", action="store_true", help="单次增量检测(launchd 调用)")
    p.add_argument("--force", action="store_true", help="忽略 state 强制检测")
    args = p.parse_args()

    # 状态节流：距上次成功检测 <1h 且非 force → 静默跳过
    if not args.force and STATE_FILE.exists():
        try:
            st = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            last = datetime.fromisoformat(st.get("last_run", ""))
            if (datetime.now(timezone.utc) - last).total_seconds() < 3600:
                print("✅ 无新增（1h 节流）")
                return
        except Exception:
            pass

    candidates = _load_candidates()
    if not candidates:
        print("✅ 无新增（无候选产出）")
        return

    existing = existing_fingerprints(TRAIN_MERGED)
    from lh_kb_ingest import to_train_record
    fresh = []
    seen = set()
    for i, s in enumerate(candidates):
        rec = to_train_record(s, "story", i)
        fp = content_fingerprint(rec)
        if fp in existing or fp in seen:
            continue
        seen.add(fp)
        fresh.append(rec)

    if not fresh:
        _write_state(0)
        print("✅ 无新增（幂等）")
        return

    # 全链路: 三保闸 → ASI 七闸 → 幂等入库 + md 卡
    from lh_triple_guard import check
    from lh_asi_feed import feed

    result = check(fresh)
    passed = result["passed"]
    if not passed:
        _write_state(0, note=f"三保闸拒 {len(fresh)}")
        print(f"🟡 新增候选 {len(fresh)} · 三保闸全拒")
        return

    feed_result = feed(passed, category="growth")
    if feed_result["status"] != "🟢":
        _write_state(0, note=f"七闸未过({feed_result['status']})")
        print(f"🟡 候选 {len(fresh)} · 七闸未过({feed_result['status']})")
        return

    n = feed_result.get("passed_cnt", 0)
    # md 知识卡（与 lh_kb_ingest 一致·只写实际入库 fresh）
    from lh_kb_ingest import to_md_card
    dom_dir = KB_ROOT / "story"
    dom_dir.mkdir(parents=True, exist_ok=True)
    written = 0
    for r in feed_result["passed"]:
        to_md_card(r, dom_dir / f"{r['id']}.md")
        written += 1
    rebuild_index(KB_ROOT)
    _write_state(written, note=f"新增入库 {n} · md卡 {written}")
    print(f"✅ 入库 {n} 条 · md卡 {written} 条")


def _write_state(added: int, note: str = "") -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    st = {
        "last_run": now_utc(),
        "added": added,
        "note": note,
        "total": _count_lines(TRAIN_MERGED),
    }
    STATE_FILE.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")


def _count_lines(p: Path) -> int:
    if not p.exists():
        return 0
    try:
        return len([l for l in p.read_text(encoding="utf-8").splitlines() if l.strip()])
    except Exception:
        return 0


if __name__ == "__main__":
    main()
