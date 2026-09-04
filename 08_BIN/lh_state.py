#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·甲申·辛巳·亥时·䷋否-STATE-BUS-GLOBAL-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""🗄️ 全局状态总线 v1.0 — 龍魂系统统一状态源（2026-09-04·方案A1落地）

理念: 从「AI专用记忆」→「全局状态总线」。每执行一条 lh 命令自动更新
global_state.json（计数/last_command），聚合 lh session 的 active_task/pending
为系统统一状态视图；操作时间轴由 lh_timeline 承担（本引擎只负责状态层）。

数据: ~/.longhun/state/global_state.json
聚合: ~/.longhun/session_context.json（active_task/pending/decisions 为权威）
用法:
  lh state show|status       → 当前全局状态（聚合视图）
  lh state reset             → 重置状态（危险·需确认码二次确认）
  lh state _hook <cmd>       → 命令后置钩子（由 lh.py 调用·静默）
"""
import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path.home() / ".longhun"
STATE_DIR = ROOT / "state"
GLOBAL = STATE_DIR / "global_state.json"
SESSION = ROOT / "session_context.json"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

EMPTY = {
    "system_status": "running",
    "active_tasks": [],
    "last_command": "",
    "last_ts": "",
    "pending_items": [],
    "recent_decisions": [],
    "stats": {"total_commands": 0, "since": ""},
    "updated_at": "",
}


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def read_global() -> dict:
    """读 global_state.json·不存在自动建空模板（P0不删除只冻结·初始化零破坏）"""
    try:
        if GLOBAL.exists():
            d = json.loads(GLOBAL.read_text(encoding="utf-8"))
            if isinstance(d, dict):
                for k, v in EMPTY.items():
                    d.setdefault(k, v if isinstance(v, list) else v)
                return d
    except Exception:
        pass
    return dict(EMPTY)


def save_global(d: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    GLOBAL.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


def hook_update(command_name: str) -> dict:
    """执行后钩子: 命令计数 + last_command 更新（静默·永不抛错）"""
    d = read_global()
    st = d.setdefault("stats", {})
    st["total_commands"] = int(st.get("total_commands", 0)) + 1
    if not st.get("since"):
        st["since"] = _now_iso()
    if command_name:
        d["last_command"] = command_name
    d["last_ts"] = _now_iso()
    d["updated_at"] = _now_iso()
    save_global(d)
    return d


def _load_session() -> dict:
    try:
        if SESSION.exists():
            s = json.loads(SESSION.read_text(encoding="utf-8"))
            if isinstance(s, dict):
                return s
    except Exception:
        pass
    return {}


def aggregate() -> dict:
    """聚合视图: global_state + session（active_task/pending/decisions 以 session 为权威）"""
    g = read_global()
    s = _load_session()
    task = (s.get("active_task") or "").strip()
    pend = s.get("pending") or []
    decs = s.get("decisions") or []
    g["active_tasks"] = [{"name": task}] if task else []
    g["pending_items"] = pend
    g["recent_decisions"] = decs
    if s.get("last_ts"):
        g["last_ts"] = s.get("last_ts")
    g["session_task"] = task
    # 🧬 源码记忆概要（A2 code_memory · 2026-09-04）
    g["code_memory"] = {"repos": 0, "records": 0}
    cm = ROOT / "code_memory"
    if cm.exists():
        try:
            repos = [d for d in cm.iterdir() if d.is_dir()]
            g["code_memory"]["repos"] = len(repos)
            g["code_memory"]["records"] = sum(len(list(r.glob("*.json"))) for r in repos)
        except Exception:
            pass
    # 🌐 外部感知概要（A4 external · 2026-09-04）
    g["external"] = {"watched": 0, "snapshots": 0, "last_scan": ""}
    ex = ROOT / "external"
    if ex.exists():
        try:
            wf = ex / "watches.json"
            if wf.exists():
                w = json.loads(wf.read_text(encoding="utf-8"))
                g["external"]["watched"] = len(w) if isinstance(w, dict) else 0
            sp = ex / "snapshots"
            if sp.exists():
                g["external"]["snapshots"] = len(list(sp.glob("*.json")))
        except Exception:
            pass
    return g


def cmd_show() -> int:
    g = aggregate()
    print(json.dumps(g, ensure_ascii=False, indent=2))
    # 一行摘要（机器/人眼两用）
    n = g["stats"].get("total_commands", 0)
    print(f"\n  🗄️  状态: {g.get('system_status', 'running')} · 累计命令 {n} 条"
          f" · 最近: lh {g.get('last_command') or '—'}")
    if g.get("session_task"):
        print(f"  🧠  当前任务: {g['session_task'][:60]}")
    if g.get("pending_items"):
        print(f"  📋  待处理 {len(g['pending_items'])} 项")
    cm = g.get("code_memory") or {}
    ex = g.get("external") or {}
    if cm.get("records"):
        print(f"  🧬  源码记忆 {cm.get('records')} 条（{cm.get('repos')} 仓库）")
    if ex.get("watched"):
        print(f"  🌐  外部跟踪 {ex.get('watched')} 仓库 · 快照 {ex.get('snapshots')} 份")
    return 0


def cmd_reset() -> int:
    """危险操作: 需确认码二次确认（防误触）"""
    print("  ⚠️  重置全局状态将清零命令计数与 last_command 记录。")
    print("      session_context（当前任务/待办）不受影响。")
    ans = input("  请输入确认码以继续: ").strip()
    if ans != CONFIRM_CODE:
        print("  🔴 确认码不匹配·操作已取消")
        return 1
    d = read_global()
    d["system_status"] = "running"
    d["last_command"] = ""
    d["last_ts"] = ""
    d["stats"] = {"total_commands": 0, "since": _now_iso()}
    d["updated_at"] = _now_iso()
    save_global(d)
    print("  🟢 全局状态已重置")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(prog="lh state", description="全局状态总线")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("show", help="当前全局状态")
    sub.add_parser("status", help="=show")
    sub.add_parser("reset", help="重置（需确认码）")
    hook = sub.add_parser("_hook", help="命令后置钩子（lh.py 内部调用）")
    hook.add_argument("cmd_name", nargs="?", default="")
    args = ap.parse_args()
    if args.cmd in ("show", "status", None):
        return cmd_show()
    if args.cmd == "reset":
        return cmd_reset()
    if args.cmd == "_hook":
        hook_update(args.cmd_name or "")
        return 0
    print(f"  ❌ 未知子命令: {args.cmd}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
