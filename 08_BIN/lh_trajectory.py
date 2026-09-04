#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·壬戌·亥时·䷏豫-TRAJECTORY-v1.0-7d3f1a2b
# 创建者: 诸葛鑫（UID9622）
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 三色: 🟢 轨迹视图落地 🟡 fork/replay 待实测 🔴 无
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂 · Trajectory 轨迹视图引擎 v1.0

对齐 DeepSeek Harness 的可追溯性哲学（append-only 轨迹 · 恢复/分叉/检索/回放），
落地为龍魂轨迹视图：

  1. show   —— 检索轨迹：读 audit_log.jsonl（append-only 主源）+ LCB 事件总线 SQLite
  2. fork   —— 分叉轨迹：从某时间点/DNA 复制轨迹快照，后续路径独立
  3. replay —— 回放轨迹：按模块/DNA 链把关联事件按时间正序串联重放

数据源:
  - 审计轨迹: longhun-system/audit_log.jsonl（每行 JSON · append-only）
  - 事件总线: ~/.longhun/event_bus/event_bus.db（events 表 · 时间/DNA/topic/payload）

用法:
  python3 bin/lh_trajectory.py show --last 10
  python3 bin/lh_trajectory.py show --module landing_engine --limit 5
  python3 bin/lh_trajectory.py fork --dna <前缀>  [--append 后续写入]
  python3 bin/lh_trajectory.py replay --module landing_engine
  python3 bin/lh_trajectory.py replay --dna 丙午
  或经统一入口: lh trajectory ...
"""
import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

PROJECT_DIR = Path(__file__).resolve().parent.parent
CONFIRM_MARK = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

AUDIT_LOG = PROJECT_DIR / "audit_log.jsonl"
EVENT_DB = Path.home() / ".longhun" / "event_bus" / "event_bus.db"
FORK_DIR = PROJECT_DIR / "logs" / "trajectories"


def _ts_sort_key(item: Dict[str, Any]) -> str:
    """轨迹时间排序键（容错：解析失败归最早）。"""
    ts = str(item.get("ts") or item.get("timestamp") or "")
    return ts


# ============================================================
# 轨迹存储（append-only 多源合并）
# ============================================================
class TrajectoryStore:
    """多源轨迹装载器：审计日志 + 事件总线，合并为统一轨迹条目。"""

    def __init__(self):
        self.entries: List[Dict[str, Any]] = []

    def load_audit(self, path: Path = AUDIT_LOG) -> int:
        """装载审计日志（每行 JSON）。"""
        if not path.exists():
            return 0
        n = 0
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    raw = json.loads(line)
                except Exception:
                    continue
                self.entries.append({
                    "ts": raw.get("timestamp", ""),
                    "src": "audit",
                    "module": raw.get("module", raw.get("context", {}).get("domain", "?"))
                              if isinstance(raw.get("context"), dict) else raw.get("module", "?"),
                    "action": raw.get("action", raw.get("reason", "record")),
                    "dna": raw.get("dna", ""),
                    "result": raw.get("result", raw.get("audit_mark", "")),
                    "details": str(raw.get("details", ""))[:200],
                })
                n += 1
        return n

    def load_lcb(self, db: Path = EVENT_DB, limit: int = 500) -> int:
        """装载 LCB 事件总线轨迹（events 表）。"""
        if not db.exists():
            return 0
        try:
            conn = sqlite3.connect(str(db))
            cur = conn.execute(
                "SELECT timestamp, dna, topic, source, event_type, payload, status "
                "FROM events ORDER BY id DESC LIMIT ?", (limit,)
            )
            rows = cur.fetchall()
            conn.close()
        except Exception:
            return 0
        for ts, dna, topic, source, etype, payload, status in rows:
            self.entries.append({
                "ts": ts,
                "src": "lcb",
                "module": f"lcb:{topic}",
                "action": etype or "event",
                "dna": dna or "",
                "result": status or "",
                "details": f"source={source} payload={str(payload)[:120]}",
            })
        return len(rows)

    def load_fork(self, path: Path) -> int:
        """装载分叉轨迹文件。"""
        return self.load_audit(path)

    def all_sorted(self) -> List[Dict[str, Any]]:
        return sorted(self.entries, key=_ts_sort_key)


# ============================================================
# 子命令实现
# ============================================================
def cmd_show(args: argparse.Namespace) -> int:
    store = TrajectoryStore()
    n1 = store.load_audit()
    n2 = store.load_lcb()
    entries = store.all_sorted()
    if args.module:
        entries = [e for e in entries if args.module in str(e["module"])]
    if args.dna:
        entries = [e for e in entries if args.dna in str(e["dna"])]
    if args.last is not None:
        entries = entries[-args.last:]
    else:
        entries = entries[-args.limit:]

    if args.json:
        print(json.dumps({"sources": {"audit": n1, "lcb": n2}, "entries": entries}, ensure_ascii=False, indent=1))
        return 0

    print(f"🐉 轨迹视图 | 审计 {n1} 条 + 事件总线 {n2} 条 → 展示 {len(entries)} 条")
    for i, e in enumerate(entries, 1):
        mark = "🟢" if str(e["result"]) in ("成功", "OK", "ok", "dispatched", "True") else "·"
        src = "📜" if e["src"] == "audit" else "🔀"
        print(f"  [{i:>3}] {src} {e['ts']} | {e['module']:<24} | {e['action']} {mark} | {str(e['dna'])[:52]}")
        if e["details"]:
            print(f"        ↳ {e['details'][:140]}")
    return 0


def cmd_fork(args: argparse.Namespace) -> int:
    """从某 DNA 前缀/时间点分叉：复制之前轨迹为独立快照。"""
    store = TrajectoryStore()
    store.load_audit()
    store.load_lcb()
    entries = store.all_sorted()

    cut_at = None
    if args.dna:
        for e in entries:
            if args.dna in str(e["dna"]):
                cut_at = e
                break
    elif args.at_time:
        cut_at = {"ts": args.at_time}

    if cut_at is None:
        print(f"⚠️ 未找到分叉点: dna={args.dna or ''} at_time={args.at_time or ''}", file=sys.stderr)
        return 2

    base_ts = str(cut_at.get("ts") or "")
    fork_entries = [e for e in entries if _ts_sort_key(e) <= base_ts] if base_ts else entries
    fork_dir = args.dir or FORK_DIR
    os.makedirs(fork_dir, exist_ok=True)
    fname = f"fork_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
    fpath = Path(fork_dir) / fname

    meta = {
        "fork_from_dna": str(cut_at.get("dna", "")),
        "fork_from_ts": base_ts,
        "fork_time": datetime.now().isoformat(),
        "entries": len(fork_entries),
        "append_only": True,
    }
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(json.dumps(meta, ensure_ascii=False) + "\n")
        for e in fork_entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    print(f"🛤️  轨迹分叉已创建: {fpath}")
    print(f"    分叉点: {base_ts} | dna={str(cut_at.get('dna',''))[:52]}")
    print(f"    快照 {len(fork_entries)} 条轨迹 | 后续写入用 --append（路径独立）")
    return 0


def cmd_replay(args: argparse.Namespace) -> int:
    """按模块/DNA 链重放轨迹：串联关联事件按时间正序回放。"""
    store = TrajectoryStore()
    store.load_audit()
    store.load_lcb()
    entries = store.all_sorted()
    if args.module:
        entries = [e for e in entries if args.module in str(e["module"])]
    if args.dna:
        entries = [e for e in entries if args.dna in str(e["dna"])]
    if args.limit and args.limit > 0:
        entries = entries[-args.limit:]
    if not entries:
        print("⚠️ 无匹配轨迹", file=sys.stderr)
        return 2

    ok = sum(1 for e in entries if str(e["result"]) in ("成功", "OK", "ok", "dispatched", "True"))
    span = ""
    if len(entries) > 1:
        span = f" | 跨度 {_ts_sort_key(entries[0])} → {_ts_sort_key(entries[-1])}"

    print(f"🔄 轨迹回放 | {len(entries)} 条 | 成功 {ok} | 失败 {len(entries) - ok}{span}")
    for i, e in enumerate(entries, 1):
        mark = "🟢" if str(e["result"]) in ("成功", "OK", "ok", "dispatched", "True") else "🔴"
        print(f"  [{i:>3}] {e['ts']} | {e['module']:<24} | {e['action']} {mark}")
        if args.verbose:
            print(f"        dna={e['dna']}")
            if e["details"]:
                print(f"        details={e['details'][:160]}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="🐉 龍魂 Trajectory 轨迹视图 v1.0（对齐 DeepSeek Harness 可追溯性）")
    sub = ap.add_subparsers(dest="cmd")

    p_show = sub.add_parser("show", help="检索轨迹")
    p_show.add_argument("--module", default="", help="按模块过滤")
    p_show.add_argument("--dna", default="", help="按 DNA 前缀过滤")
    p_show.add_argument("--limit", type=int, default=20)
    p_show.add_argument("--last", type=int, default=None)
    p_show.add_argument("--json", action="store_true")
    p_show.set_defaults(fn=cmd_show)

    p_fork = sub.add_parser("fork", help="从某 DNA/时间点分叉轨迹")
    p_fork.add_argument("--dna", default="", help="分叉点 DNA 前缀")
    p_fork.add_argument("--at-time", default="", help="分叉点时间（含该点之前）")
    p_fork.add_argument("--dir", default=None, help="分叉文件目录（默认 logs/trajectories/）")
    p_fork.set_defaults(fn=cmd_fork)

    p_rp = sub.add_parser("replay", help="按模块/DNA 链重放轨迹")
    p_rp.add_argument("--module", default="")
    p_rp.add_argument("--dna", default="")
    p_rp.add_argument("--limit", type=int, default=0, help="最多重放 N 条（默认全部）")
    p_rp.add_argument("--verbose", action="store_true")
    p_rp.set_defaults(fn=cmd_replay)

    args = ap.parse_args()
    if not getattr(args, "fn", None):
        ap.print_help()
        return 1
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
