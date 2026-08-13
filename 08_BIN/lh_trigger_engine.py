#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂工作流触发器引擎 v1.0
P3 · 文件变更 / 定时 / 事件 三类触发 · 跨技能事件链
DNA: #龍芯⚡️丙午·甲申·辛丑·坤卦-TRIGGER-ENGINE-v1.0-UID9622
"""

import argparse
import hashlib
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

HOME = Path.home()
LONGHUN_DIR = HOME / ".longhun"
TRIGGER_DIR = LONGHUN_DIR / "triggers"
TRIGGER_FILE = TRIGGER_DIR / "triggers.json"
TRIGGER_LOG = TRIGGER_DIR / "trigger_log.jsonl"
TRIGGER_PID = TRIGGER_DIR / "trigger_daemon.pid"
TRIGGER_LOG_FILE = TRIGGER_DIR / "trigger_daemon.log"

BUS_SCRIPT = Path(__file__).resolve().parent / "lh_event_bus.py"
WF_SCRIPT = Path(__file__).resolve().parent / "lh_workflow_engine.py"
GOV_SCRIPT = Path(__file__).resolve().parent / "lh_governed_exec.py"


def ensure_dirs():
    TRIGGER_DIR.mkdir(parents=True, exist_ok=True)


def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def load_json(path: Path) -> Any:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: Any):
    ensure_dirs()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def append_jsonl(path: Path, data: dict):
    ensure_dirs()
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def generate_trigger_id(t: dict) -> str:
    raw = f"{t['name']}:{t['type']}:{t.get('target','')}:{t.get('topic','')}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:8]


def builtin_triggers() -> List[dict]:
    return [
        {
            "id": "auto-discovery",
            "name": "技能索引自动刷新",
            "type": "interval",
            "enabled": True,
            "interval": 3600,
            "action": {
                "kind": "command",
                "cmd": "lh orchestrator discover",
            },
            "description": "每小时自动扫描技能目录，刷新 skill_index.json",
            "dna": "#龍芯⚡️丙午·甲申·辛丑·坤卦-TRIGGER-AUTO-DISCOVERY-UID9622",
        },
        {
            "id": "memory-guard",
            "name": "MEMORY.md 变更触发归档",
            "type": "file",
            "enabled": True,
            "target": str(LONGHUN_DIR.parent / "longhun-system" / ".codebuddy" / "memory" / "MEMORY.md"),
            "action": {
                "kind": "event",
                "topic": "file.changed",
                "payload": {"file": "{{target}}", "note": "MEMORY.md 已变更"},
            },
            "description": "MEMORY.md 修改后向事件总线发布 file.changed 事件",
            "dna": "#龍芯⚡️丙午·甲申·辛丑·坤卦-TRIGGER-MEMORY-GUARD-UID9622",
        },
        {
            "id": "workflow-chain-event",
            "name": "代码审查完成后触发发布链",
            "type": "event",
            "enabled": True,
            "topic": "workflow.code_review.completed",
            "action": {
                "kind": "workflow",
                "workflow": "publish",
                "message": "代码审查已通过，进入发布链",
            },
            "description": "跨技能事件链：code-review 工作流完成后自动触发 publish 工作流",
            "dna": "#龍芯⚡️丙午·甲申·辛丑·坤卦-TRIGGER-WORKFLOW-CHAIN-UID9622",
        },
    ]


def init_triggers():
    ensure_dirs()
    triggers = builtin_triggers()
    for t in triggers:
        if not t.get("id"):
            t["id"] = generate_trigger_id(t)
    data = {
        "version": "1.0",
        "generated_at": now_iso(),
        "triggers": triggers,
    }
    save_json(TRIGGER_FILE, data)
    print(f"🐉 已初始化 {len(triggers)} 个内置触发器")
    for t in triggers:
        print(f"   · {t['id']} [{t['type']}] {t['name']}")
    return 0


def load_triggers() -> List[dict]:
    data = load_json(TRIGGER_FILE)
    return data.get("triggers", [])


def log_trigger(trigger: dict, result: dict):
    append_jsonl(TRIGGER_LOG, {
        "timestamp": now_iso(),
        "trigger_id": trigger.get("id"),
        "trigger_name": trigger.get("name"),
        "trigger_type": trigger.get("type"),
        "action": trigger.get("action", {}),
        "result": result,
    })


def execute_action(trigger: dict, context: dict, dry_run: bool = False):
    action = trigger.get("action", {})
    kind = action.get("kind")
    if dry_run:
        print(f"      [dry-run] action={kind}")
        return {"status": "dry_run", "kind": kind}

    if kind == "command":
        cmd = render_template(action.get("cmd", ""), context)
        return run_command(cmd, trigger, context)
    elif kind == "workflow":
        wf = action.get("workflow", "")
        msg = render_template(action.get("message", ""), context)
        cmd = [sys.executable, str(WF_SCRIPT), "run", wf, "-m", msg]
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        return {
            "status": "success" if r.returncode == 0 else "failed",
            "returncode": r.returncode,
            "stdout": r.stdout.strip(),
            "stderr": r.stderr.strip(),
        }
    elif kind == "event":
        topic = render_template(action.get("topic", "trigger.event"), context)
        payload = action.get("payload", {})
        payload = {k: render_template(str(v), context) for k, v in payload.items()}
        r = subprocess.run(
            [sys.executable, str(BUS_SCRIPT), "publish",
             "--topic", topic, "--source", f"trigger:{trigger.get('id')}",
             "--type", "trigger_fired", "--payload", json.dumps(payload, ensure_ascii=False)],
            capture_output=True, text=True, encoding="utf-8", errors="ignore",
        )
        return {
            "status": "event_published" if r.returncode == 0 else "event_failed",
            "returncode": r.returncode,
            "stdout": r.stdout.strip(),
            "stderr": r.stderr.strip(),
        }
    else:
        return {"status": "unknown_kind", "kind": kind}


def render_template(s: str, context: dict) -> str:
    for k, v in context.items():
        s = s.replace(f"{{{{{k}}}}}", str(v))
    return s


def run_command(cmd: str, trigger: dict, context: dict) -> dict:
    # 走治理流水线包装
    gov_cmd = [
        sys.executable, str(GOV_SCRIPT),
        "--cmd", cmd,
        "--desc", f"触发器[{trigger.get('id')}] {trigger.get('name')}",
        "--uid", "UID9622",
        "--topic", "trigger.execution",
    ]
    r = subprocess.run(gov_cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return {
        "status": "success" if r.returncode == 0 else "failed",
        "returncode": r.returncode,
        "stdout": r.stdout.strip(),
        "stderr": r.stderr.strip(),
    }


# ─── 触发器执行 ───
def run_interval_trigger(trigger: dict, state: dict, dry_run: bool = False) -> dict:
    now = time.time()
    last = state.get("last_run", 0)
    interval = trigger.get("interval", 60)
    if now - last >= interval:
        context = {"trigger_id": trigger["id"], "trigger_name": trigger["name"], "now": now_iso()}
        result = execute_action(trigger, context, dry_run=dry_run)
        state["last_run"] = now
        log_trigger(trigger, result)
        return result
    return {"status": "skipped", "reason": "interval not reached"}


def run_file_trigger(trigger: dict, state: dict, dry_run: bool = False) -> dict:
    target = Path(render_template(trigger.get("target", ""), {}))
    if not target.exists():
        return {"status": "skipped", "reason": f"target not found: {target}"}
    mtime = target.stat().st_mtime
    last_mtime = state.get("last_mtime")
    if last_mtime is None:
        state["last_mtime"] = mtime
        return {"status": "init", "mtime": mtime}
    if mtime != last_mtime:
        context = {"trigger_id": trigger["id"], "trigger_name": trigger["name"], "target": str(target), "mtime": mtime}
        result = execute_action(trigger, context, dry_run=dry_run)
        state["last_mtime"] = mtime
        log_trigger(trigger, result)
        return result
    return {"status": "skipped", "reason": "no change"}


def run_event_trigger(trigger: dict, events: List[dict], dry_run: bool = False) -> List[dict]:
    results = []
    topic = trigger.get("topic")
    ev_type = trigger.get("event_type")
    processed_ids = []
    for ev in events:
        if topic and ev.get("topic") != topic:
            continue
        if ev_type and ev.get("event_type") != ev_type:
            continue
        context = {
            "trigger_id": trigger["id"],
            "trigger_name": trigger["name"],
            "event_id": ev.get("id"),
            "topic": ev.get("topic"),
            "event_type": ev.get("event_type"),
            "payload": ev.get("payload", ""),
        }
        result = execute_action(trigger, context, dry_run=dry_run)
        results.append(result)
        log_trigger(trigger, result)
        processed_ids.append(ev.get("id"))
    if processed_ids and not dry_run:
        mark_events_delivered(processed_ids)
    return results


def mark_events_delivered(event_ids: List[int]):
    db_path = LONGHUN_DIR / "event_bus" / "event_bus.db"
    if not db_path.exists():
        return
    try:
        import sqlite3
        conn = sqlite3.connect(str(db_path))
        now = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        for eid in event_ids:
            conn.execute("UPDATE events SET status='delivered' WHERE id=?", (eid,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"🔴 mark_events_delivered error: {e}", file=sys.stderr)


# ─── CLI ───
def cmd_init(args):
    return init_triggers()


def cmd_list(args):
    triggers = load_triggers()
    print(f"🐉 触发器列表 ({len(triggers)} 个)")
    for t in triggers:
        flag = "🟢" if t.get("enabled") else "⚪"
        print(f"  {flag} {t['id']} [{t['type']}] {t['name']}")
        print(f"      {t.get('description', '')}")
    return 0


def cmd_run(args):
    triggers = load_triggers()
    target = [t for t in triggers if t.get("id") == args.trigger_id]
    if not target:
        print(f"❌ 触发器不存在: {args.trigger_id}")
        return 1
    trigger = target[0]
    if not trigger.get("enabled"):
        print(f"🟡 触发器已禁用: {args.trigger_id}")
        return 0

    print(f"🐉 手动执行触发器: {trigger['name']} [{trigger['type']}]")
    state = {}
    if trigger["type"] == "interval":
        result = run_interval_trigger(trigger, state, dry_run=args.dry_run)
    elif trigger["type"] == "file":
        result = run_file_trigger(trigger, state, dry_run=args.dry_run)
    elif trigger["type"] == "event":
        # 从事件总线消费一条匹配事件
        events = fetch_events(trigger.get("topic"), trigger.get("event_type"), limit=1)
        results = run_event_trigger(trigger, events, dry_run=args.dry_run)
        result = results[0] if results else {"status": "skipped", "reason": "no matching event"}
    else:
        print(f"❌ 未知触发器类型: {trigger['type']}")
        return 1

    print(f"   结果: {result.get('status')}")
    if "stdout" in result and result["stdout"]:
        print(f"   stdout: {result['stdout'][:200]}")
    return 0


def fetch_events(topic: Optional[str], event_type: Optional[str], limit: int = 10) -> List[dict]:
    """直接从事件总线 SQLite 读取最近 pending 事件（不标记 delivered）"""
    db_path = LONGHUN_DIR / "event_bus" / "event_bus.db"
    if not db_path.exists():
        return []
    try:
        import sqlite3
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        sql = "SELECT * FROM events WHERE status='pending'"
        params = []
        if topic:
            sql += " AND topic=?"
            params.append(topic)
        if event_type:
            sql += " AND event_type=?"
            params.append(event_type)
        sql += " ORDER BY id DESC LIMIT ?"
        params.append(limit)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        return [
            {
                "id": r["id"],
                "topic": r["topic"],
                "event_type": r["event_type"],
                "source": r["source"],
                "payload": r["payload"],
                "status": r["status"],
            }
            for r in rows
        ]
    except Exception as e:
        print(f"🔴 fetch_events error: {e}", file=sys.stderr)
        return []


def cmd_daemon(args):
    """启动触发器守护进程"""
    ensure_dirs()
    pid = read_pid()
    if pid and is_running(pid):
        print(f"🟡 触发器守护进程已在运行 (PID {pid})")
        return 0

    log_fp = open(TRIGGER_LOG_FILE, "a", encoding="utf-8")
    proc = subprocess.Popen(
        [sys.executable, str(Path(__file__).resolve()), "_run_loop", "--interval", str(args.interval)],
        stdout=log_fp,
        stderr=subprocess.STDOUT,
        stdin=subprocess.DEVNULL,
        start_new_session=True,
    )
    write_pid(proc.pid)
    time.sleep(0.5)
    if proc.poll() is not None:
        print(f"🔴 守护进程启动后立即退出 (code {proc.returncode})")
        remove_pid()
        return 1
    print(f"🐉 触发器守护进程启动 (PID {proc.pid})")
    print(f"   日志: {TRIGGER_LOG_FILE}")
    return 0


def cmd_stop(args):
    pid = read_pid()
    if not pid or not is_running(pid):
        print("⚪ 触发器守护进程未运行")
        remove_pid()
        return 0
    try:
        os.kill(pid, signal.SIGTERM)
        for _ in range(50):
            if not is_running(pid):
                break
            time.sleep(0.1)
        if is_running(pid):
            os.kill(pid, signal.SIGKILL)
        remove_pid()
        print(f"🛑 触发器守护进程已停止 (PID {pid})")
        return 0
    except Exception as e:
        print(f"🔴 停止失败: {e}")
        return 1


def cmd_status(args):
    pid = read_pid()
    if not pid:
        print("⚪ 触发器守护进程未运行")
        return 0
    if is_running(pid):
        print(f"🟢 触发器守护进程运行中 (PID {pid})")
        return 0
    else:
        print(f"🔴 PID {pid} 不存在")
        remove_pid()
        return 1


def cmd_run_loop(args):
    """内部循环，被 daemon 调用"""
    triggers = load_triggers()
    state = {}
    print(f"🐉 触发器循环启动 · 轮询间隔 {args.interval}s · 共 {len(triggers)} 个触发器")
    while True:
        try:
            for trigger in triggers:
                if not trigger.get("enabled"):
                    continue
                tid = trigger["id"]
                st = state.setdefault(tid, {})
                if trigger["type"] == "interval":
                    run_interval_trigger(trigger, st)
                elif trigger["type"] == "file":
                    run_file_trigger(trigger, st)
                elif trigger["type"] == "event":
                    events = fetch_events(trigger.get("topic"), trigger.get("event_type"), limit=5)
                    if events:
                        run_event_trigger(trigger, events)
            time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n👋 触发器循环停止")
            break
    return 0


# ─── PID 工具 ───
def read_pid() -> Optional[int]:
    if not TRIGGER_PID.exists():
        return None
    try:
        return int(TRIGGER_PID.read_text().strip())
    except Exception:
        return None


def write_pid(pid: int):
    TRIGGER_PID.write_text(str(pid))


def remove_pid():
    if TRIGGER_PID.exists():
        TRIGGER_PID.unlink()


def is_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


# ─── 参数解析 ───
def build_parser():
    p = argparse.ArgumentParser(description="🐉 龍魂工作流触发器引擎 v1.0")
    sub = p.add_subparsers(dest="command")

    sub.add_parser("init", help="初始化内置触发器")
    sub.add_parser("list", help="列出触发器")

    run = sub.add_parser("run", help="手动执行触发器")
    run.add_argument("trigger_id", help="触发器 ID")
    run.add_argument("--dry-run", action="store_true")

    daemon = sub.add_parser("daemon", help="启动触发器守护进程")
    daemon.add_argument("--interval", type=int, default=10, help="轮询间隔秒")

    sub.add_parser("stop", help="停止触发器守护进程")
    sub.add_parser("status", help="查看触发器守护进程状态")

    loop = sub.add_parser("_run_loop", help=argparse.SUPPRESS)
    loop.add_argument("--interval", type=int, default=10)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 0
    ensure_dirs()
    handlers = {
        "init": cmd_init,
        "list": cmd_list,
        "run": cmd_run,
        "daemon": cmd_daemon,
        "stop": cmd_stop,
        "status": cmd_status,
        "_run_loop": cmd_run_loop,
    }
    return handlers[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
