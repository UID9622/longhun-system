# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂万年历 · 主系统集成入口
DNA: #龍芯⚡️2026-06-28-LONGHUN-CALENDAR-CLI-v1.0
"""
import argparse
import json
import os
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import sqlite3
from calendar_core import LongHunCalendar
from context_manager import ContextManager
from notion_logger import LongHunLogger, ActionType


def get_calendar():
    base = Path.home() / ".longhun" / "calendar-context-logger" / "calendar"
    base.mkdir(parents=True, exist_ok=True)
    return LongHunCalendar(base_path=str(base))


def cmd_status(args):
    cal = get_calendar()
    status = cal.status()
    print("🐉 龍魂万年历 · 系统状态")
    print(f"  系统: {status['system']['name']} v{status['system']['version']} | UID {status['system']['uid']}")
    print(f"  运行时间: {status['system']['uptime_human']}")
    print(f"  总会话数: {status['sessions']['total']} | 活跃上下文: {status['sessions']['active_contexts']}")
    print(f"  总任务数: {status['tasks']['total']}")
    print(f"  DNA链长度: {status['dna_chain_length']}")
    sync = cal.get_sync_status()
    print(f"  Notion待同步: {sync['pending']} | 失败: {sync['failed']}")


def cmd_enter(args):
    cal = get_calendar()
    result = cal.enter(args.task_type, " ".join(args.text), skill_hint=args.skill)
    print(f"✅ 入口处理完成")
    print(f"  DNA: {result['dna_code']}")
    print(f"  时间: {result['timestamp_human']}")
    print(f"  路由技能: {result['routed_skill']['name']} ({result['routed_skill']['id']})")
    print(f"  上下文ID: {result['context_id']}")
    if result.get('ai_response'):
        print(f"  AI响应: {result['ai_response']['response'][:120]}...")


def cmd_demo(args):
    cal = get_calendar()
    # demo() in calendar_core is module-level; call it directly
    import calendar_core
    calendar_core.demo()


def cmd_context(args):
    mgr = ContextManager()
    if args.sub == "status":
        print(json.dumps(mgr.get_status(), ensure_ascii=False, indent=2))
    elif args.sub == "create":
        ctx = mgr.create_context(args.topic)
        print(f"创建上下文: {ctx.context_id}")
    elif args.sub == "list":
        sessions = mgr.list_contexts()
        print(f"共有 {len(sessions)} 个会话")
        for s in sessions[-10:]:
            print(f"  {s.get('context_id')} | {s.get('topic')} | {s.get('state')}")
    else:
        print(mgr.status())


def cmd_logger(args):
    db_path = Path.home() / ".longhun" / "calendar-context-logger" / "action_log.db"
    logger = LongHunLogger(db_path=str(db_path), enable_auto_sync=False)
    if args.sub == "recent":
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            "SELECT timestamp_ms, action_type, description, dna_trace FROM action_records ORDER BY timestamp_ms DESC LIMIT ?",
            (args.limit,),
        )
        rows = cur.fetchall()
        conn.close()
        print(f"最近 {len(rows)} 条记录:")
        for r in rows:
            ts = r["timestamp_ms"] // 1000
            t = __import__("datetime").datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
            print(f"  [{t}] {r['action_type']} | {r['description'][:60]} | {r['dna_trace'][:20]}")
    elif args.sub == "log":
        atype = ActionType[args.action_type] if args.action_type in ActionType.__members__ else ActionType.USER_INPUT
        logger.log(
            action_type=atype,
            description=args.description,
            context_data=json.loads(args.meta or "{}"),
        )
        print("✅ 已记录")
    else:
        stats = logger.get_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="龍魂万年历 · 系统唯一入口",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        示例:
          lh-calendar status
          lh-calendar enter code "帮我写快速排序"
          lh-calendar context list
          lh-calendar logger recent --limit 5
        """),
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="查看系统状态")

    p_enter = sub.add_parser("enter", help="通过万年历入口进入系统")
    p_enter.add_argument("task_type", choices=["code", "analysis", "chat", "creative", "quick", "task"])
    p_enter.add_argument("text", nargs="+", help="用户输入")
    p_enter.add_argument("--skill", help="强制指定技能ID")

    sub.add_parser("demo", help="运行完整演示")

    p_ctx = sub.add_parser("context", help="上下文管理器")
    p_ctx.add_argument("sub", nargs="?", default="status", choices=["status", "create", "list"])
    p_ctx.add_argument("--topic", default="默认话题")

    p_log = sub.add_parser("logger", help="Notion记录器")
    p_log.add_argument("sub", nargs="?", default="stats", choices=["stats", "recent", "log"])
    p_log.add_argument("--limit", type=int, default=10)
    p_log.add_argument("--action-type", default="USER_INPUT")
    p_log.add_argument("--description", default="手动记录")
    p_log.add_argument("--meta", help="JSON 元数据")

    args = parser.parse_args(argv)
    handlers = {
        "status": cmd_status,
        "enter": cmd_enter,
        "demo": cmd_demo,
        "context": cmd_context,
        "logger": cmd_logger,
    }
    return handlers[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
