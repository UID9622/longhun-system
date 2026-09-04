#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🛡️ P0焊死(2026-09-04·P72加封): 会话记忆引擎·源码修改须走三色治理v2.1 §十二门槛
# DNA: #龍芯⚡️2026-09-04-SESSION-MEMORY-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂·会话记忆自动恢复 v1.0 — lh session save|status|history|restore
需求1: 每次对话自动恢复上次完整状态·不重复解释上下文(老大 2026-09-04 指令)。
数据: ~/.longhun/session_context.json(当前) + ~/.longhun/session_history/*.json(快照·最多20)
结构: {active_task, last_command, last_ts, decisions[<=3], pending[], updated_by}
用法:
  lh session status            → 查看当前会话摘要(=自动恢复显示)
  lh session save [--task 当前任务] [--note 附注] [--decision 决策]
                [--todo +待办|-待办]      → 保存当前状态(AI 在任务变更/里程碑时调用)
  lh session history           → 列出历史快照
  lh session restore --id N    → 恢复指定历史快照为当前
  lh session clear [--all]     → 清空当前任务(--all 连快照一起)
自动接线(lh.py): 每次子命令执行后自动记录 last_command; 无参/交互入口打印恢复摘要;
CodeBuddy 启动清单读本文件 = 每次对话自动恢复。
"""
import json, sys, time, shutil
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.home() / ".longhun"
CUR = ROOT / "session_context.json"
HIST_DIR = ROOT / "session_history"
MAX_DECISIONS = 3
MAX_HISTORY = 20

EMPTY = {"active_task": "", "last_command": "", "last_ts": "",
         "decisions": [], "pending": [], "updated_by": ""}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load() -> dict:
    if CUR.exists():
        try:
            data = json.loads(CUR.read_text(encoding="utf-8"))
            for k, v in EMPTY.items():
                data.setdefault(k, v if not isinstance(v, list) else list(v))
            return data
        except Exception:
            return dict(EMPTY)
    return dict(EMPTY)


def _save(data: dict):
    ROOT.mkdir(parents=True, exist_ok=True)
    data["last_ts"] = _now()
    # 快照历史(滚动保留20份)
    HIST_DIR.mkdir(parents=True, exist_ok=True)
    snap = HIST_DIR / (time.strftime("%Y%m%d_%H%M%S") + ".json")
    snap.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    old = sorted(HIST_DIR.glob("*.json"))
    for f in old[:-MAX_HISTORY]:
        f.unlink(missing_ok=True)
    CUR.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return data


def _add_unique(items: list, item: str, cap: int) -> list:
    items = [x for x in items if x != item]
    items.insert(0, item)
    return items[:cap]


def cmd_status() -> int:
    d = _load()
    print("🐉 龍魂·会话记忆恢复摘要\n" + "=" * 46)
    if not d.get("active_task") and not d.get("pending") and not d.get("last_command"):
        print("  ℹ️  尚无会话状态。AI 可在任务里程碑执行: lh session save --task \"...\"")
        return 0
    task = d.get("active_task") or "—"
    print(f"  当前任务: {task}")
    if d.get("last_command"):
        print(f"  最后执行: lh {d.get('last_command')} · {d.get('last_ts','')[:19]}")
    if d.get("pending"):
        print("  待处理:")
        for p in d["pending"]:
            print(f"    • {p}")
    if d.get("decisions"):
        print("  最近决策:")
        for dec in d["decisions"]:
            print(f"    ◦ {dec[:100]}")
    print(f"  快照: {len(list(HIST_DIR.glob('*.json')) if HIST_DIR.exists() else [])} 份 (lh session history)")
    return 0


def cmd_save(argv: list) -> int:
    task = note = decision = ""
    todo = None  # '+'/'-'
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--task" and i + 1 < len(argv):
            task, i = argv[i + 1], i + 2
        elif a == "--note" and i + 1 < len(argv):
            note, i = argv[i + 1], i + 2
        elif a == "--decision" and i + 1 < len(argv):
            decision, i = argv[i + 1], i + 2
        elif a == "--todo" and i + 1 < len(argv):
            todo, i = argv[i + 1], i + 2
        else:
            i += 1
    d = _load()
    if task:
        d["active_task"] = task
    if decision:
        d["decisions"] = _add_unique(d.get("decisions", []), decision, MAX_DECISIONS)
    pend = d.get("pending", [])
    if todo:
        if todo.startswith("+"):
            pend = _add_unique(pend, todo[1:], 30)
        elif todo.startswith("-"):
            pend = [x for x in pend if x != todo[1:]]
        elif todo:
            pend = _add_unique(pend, todo, 30)
    d["pending"] = pend
    if note:
        d["updated_by"] = note
    _save(d)
    cmd_status()
    print("  ✅ 会话状态已保存")
    return 0


def cmd_history() -> int:
    if not HIST_DIR.exists():
        print("  ℹ️  无历史快照")
        return 0
    snaps = sorted(HIST_DIR.glob("*.json"))
    print(f"🐉 会话历史快照({len(snaps)}份)\n" + "=" * 46)
    for n, f in enumerate(snaps, 1):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        task = d.get("active_task") or "—"
        print(f"  [{n}] {f.stem} · {task[:60]}")
    print("\n  ⚡ 恢复指定快照: lh session restore --id N")
    return 0


def cmd_restore(argv: list) -> int:
    n = None
    if "--id" in argv:
        i = argv.index("--id")
        if i + 1 < len(argv):
            try:
                n = int(argv[i + 1])
            except ValueError:
                n = None
    if not n or not HIST_DIR.exists():
        print("  ❌ 用法: lh session restore --id N (编号见 lh session history)")
        return 1
    snaps = sorted(HIST_DIR.glob("*.json"))
    if not (1 <= n <= len(snaps)):
        print(f"  ❌ 编号 {n} 超出范围(1-{len(snaps)})")
        return 1
    d = json.loads(snaps[n - 1].read_text(encoding="utf-8"))
    d["updated_by"] = "restore"
    _save(d)
    cmd_status()
    print(f"  ✅ 已恢复快照 [{n}]")
    return 0


def cmd_clear(argv: list) -> int:
    all_flag = "--all" in argv
    if all_flag:
        for f in list(HIST_DIR.glob("*.json")) + [CUR]:
            f.unlink(missing_ok=True)
        print("  ✅ 会话状态与快照已全部清除")
    else:
        d = _load()
        d["active_task"] = ""
        _save(d)
        print("  ✅ 当前任务已清空")
    return 0


def main() -> int:
    argv = sys.argv[1:] or ["status"]
    cmd = argv[0]
    rest = argv[1:]
    if cmd == "status":
        return cmd_status()
    if cmd == "save":
        return cmd_save(rest)
    if cmd == "history":
        return cmd_history()
    if cmd == "restore":
        return cmd_restore(rest)
    if cmd == "clear":
        return cmd_clear(rest)
    print("用法: lh session status|save [--task|--note|--decision|--todo]|history|restore --id N|clear [--all]")
    return 1


if __name__ == "__main__":
    sys.exit(main())
