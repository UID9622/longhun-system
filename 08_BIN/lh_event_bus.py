#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙戌·乙丑·卯时·䷯井-EVENT-BUS-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 龍魂中枢事件总线（LongHun Central Bus, LCB）v1.0

为龍魂技能生态提供统一的事件发布/订阅/消费能力，
是自动迭代飞轮的基础设施。

用法:
    # 发布事件
    python3 08_BIN/lh_event_bus.py publish --topic skill.execution \
        --source lh-iron-law --type check_completed \
        --payload '{"verdict":"🟢","file":"x.md"}'

    # 订阅事件
    python3 08_BIN/lh_event_bus.py subscribe --skill longhun-audit \
        --topic skill.execution --type check_completed

    # 消费事件（技能主动拉取）
    python3 08_BIN/lh_event_bus.py consume --skill longhun-audit --limit 10

    # 监听模式（守护进程）
    python3 08_BIN/lh_event_bus.py listen --skill longhun-audit \
        --handler 'python3 08_BIN/lh_audit_react.py'

    # 查看事件流
    python3 08_BIN/lh_event_bus.py list --topic skill.execution --limit 20

协议: CC BY-NC-SA 4.0 (思想层) · MulanPSL v2 (工程层)
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.longhun_core.dna_trace import generate_dna

CONFIRM_MARK = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

DATA_DIR = Path.home() / ".longhun" / "event_bus"
DB_PATH = DATA_DIR / "event_bus.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    dna TEXT NOT NULL,
    topic TEXT NOT NULL,
    source TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload TEXT NOT NULL,
    payload_hash TEXT NOT NULL UNIQUE,
    status TEXT DEFAULT 'pending'
);

CREATE INDEX IF NOT EXISTS idx_events_topic ON events(topic);
CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_status ON events(status);
CREATE INDEX IF NOT EXISTS idx_events_source ON events(source);

CREATE TABLE IF NOT EXISTS subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill TEXT NOT NULL,
    topic TEXT NOT NULL,
    event_type TEXT,
    priority INTEGER DEFAULT 50,
    created_at TEXT NOT NULL,
    UNIQUE(skill, topic, event_type)
);

CREATE TABLE IF NOT EXISTS deliveries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    skill TEXT NOT NULL,
    delivered_at TEXT,
    result TEXT,
    FOREIGN KEY (event_id) REFERENCES events(id)
);
"""

import sqlite3


def _init_db() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


def _payload_hash(topic: str, source: str, event_type: str, payload: str) -> str:
    raw = f"{topic}:{source}:{event_type}:{payload}:{datetime.now().strftime('%Y%m%d%H')}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]


def cmd_publish(args: argparse.Namespace):
    conn = _init_db()
    payload = args.payload
    if not payload.startswith("{"):
        # treat as file path
        p = Path(payload)
        if p.exists():
            payload = p.read_text(encoding="utf-8")
        else:
            print(f"❌ payload 不是 JSON 且文件不存在: {payload}", file=sys.stderr)
            sys.exit(2)

    # validate json
    try:
        json.loads(payload)
    except Exception as e:
        print(f"❌ payload 不是合法 JSON: {e}", file=sys.stderr)
        sys.exit(2)

    ph = _payload_hash(args.topic, args.source, args.type, payload)
    dna = generate_dna("EVENT-BUS", "UID9622")
    now = datetime.now().isoformat()

    try:
        conn.execute(
            "INSERT INTO events (timestamp, dna, topic, source, event_type, payload, payload_hash) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (now, dna, args.topic, args.source, args.type, payload, ph),
        )
        conn.commit()
        print(f"✅ 事件已发布 | topic={args.topic} | type={args.type} | hash={ph}")
    except sqlite3.IntegrityError:
        print(f"⏭️ 幂等跳过 | hash={ph}")
    finally:
        conn.close()


def cmd_subscribe(args: argparse.Namespace):
    conn = _init_db()
    now = datetime.now().isoformat()
    conn.execute(
        """INSERT INTO subscriptions (skill, topic, event_type, priority, created_at)
           VALUES (?, ?, ?, ?, ?)
           ON CONFLICT(skill, topic, event_type) DO UPDATE SET priority=excluded.priority""",
        (args.skill, args.topic, args.type, args.priority, now),
    )
    conn.commit()
    conn.close()
    type_str = args.type or "*"
    print(f"✅ 订阅已注册 | skill={args.skill} | topic={args.topic} | type={type_str}")


def _events_to_dict(events: List[sqlite3.Row]) -> List[Dict[str, Any]]:
    out = []
    for ev in events:
        d = {
            "id": ev["id"],
            "topic": ev["topic"],
            "event_type": ev["event_type"],
            "source": ev["source"],
            "payload": ev["payload"],
            "status": ev["status"],
        }
        # 兼容旧表可能没有 timestamp 字段
        try:
            d["timestamp"] = ev["timestamp"]
        except IndexError:
            pass
        out.append(d)
    return out


def cmd_consume(args: argparse.Namespace):
    conn = _init_db()
    cursor = conn.cursor()

    # find subscriptions for skill
    cursor.execute("SELECT topic, event_type FROM subscriptions WHERE skill=?", (args.skill,))
    subs = cursor.fetchall()
    if not subs:
        if args.json:
            print(json.dumps({"error": f"{args.skill} 没有注册订阅"}, ensure_ascii=False))
        else:
            print(f"⚠️ {args.skill} 没有注册订阅")
        conn.close()
        return

    events: List[sqlite3.Row] = []
    for topic, event_type in subs:
        if event_type and event_type != "*":
            cursor.execute(
                "SELECT * FROM events WHERE topic=? AND event_type=? AND status='pending' ORDER BY id LIMIT ?",
                (topic, event_type, args.limit),
            )
        else:
            cursor.execute(
                "SELECT * FROM events WHERE topic=? AND status='pending' ORDER BY id LIMIT ?",
                (topic, args.limit),
            )
        events.extend(cursor.fetchall())

    # dedup by id
    seen = set()
    unique_events = []
    for ev in events:
        if ev["id"] not in seen:
            seen.add(ev["id"])
            unique_events.append(ev)

    unique_events = unique_events[: args.limit]

    for ev in unique_events:
        cursor.execute(
            "INSERT INTO deliveries (event_id, skill, delivered_at) VALUES (?, ?, ?)",
            (ev["id"], args.skill, datetime.now().isoformat()),
        )
        cursor.execute("UPDATE events SET status='delivered' WHERE id=?", (ev["id"],))

    conn.commit()
    conn.close()

    if args.json:
        print(json.dumps(_events_to_dict(unique_events), ensure_ascii=False))
        return

    print(f"🐉 {args.skill} 消费 {len(unique_events)} 条事件\n")
    for ev in unique_events:
        print(f"  [{ev['id']}] {ev['topic']}/{ev['event_type']} from {ev['source']}")
        print(f"      payload: {ev['payload'][:120]}")


def cmd_listen(args: argparse.Namespace):
    conn = _init_db()
    cursor = conn.cursor()
    cursor.execute("SELECT topic, event_type FROM subscriptions WHERE skill=?", (args.skill,))
    subs = cursor.fetchall()
    if not subs:
        print(f"❌ {args.skill} 没有订阅，无法监听", file=sys.stderr)
        conn.close()
        sys.exit(2)

    print(f"🐉 {args.skill} 开始监听事件总线（每 {args.interval} 秒轮询，Ctrl+C 停止）")
    try:
        while True:
            # reuse consume logic without printing counts
            for topic, event_type in subs:
                if event_type:
                    cursor.execute(
                        "SELECT * FROM events WHERE topic=? AND event_type=? AND status='pending' ORDER BY id LIMIT ?",
                        (topic, event_type, args.limit),
                    )
                else:
                    cursor.execute(
                        "SELECT * FROM events WHERE topic=? AND status='pending' ORDER BY id LIMIT ?",
                        (topic, args.limit),
                    )
                events = cursor.fetchall()
                for ev in events:
                    # mark delivered
                    cursor.execute(
                        "INSERT INTO deliveries (event_id, skill, delivered_at) VALUES (?, ?, ?)",
                        (ev["id"], args.skill, datetime.now().isoformat()),
                    )
                    cursor.execute("UPDATE events SET status='delivered' WHERE id=?", (ev["id"],))
                    conn.commit()
                    # invoke handler if given
                    if args.handler:
                        env = os.environ.copy()
                        env["LCB_EVENT_ID"] = str(ev["id"])
                        env["LCB_TOPIC"] = ev["topic"]
                        env["LCB_TYPE"] = ev["event_type"]
                        env["LCB_SOURCE"] = ev["source"]
                        env["LCB_PAYLOAD"] = ev["payload"]
                        try:
                            result = subprocess.run(
                                args.handler,
                                shell=True,
                                env=env,
                                capture_output=True,
                                text=True,
                                timeout=120,
                            )
                            res = {"returncode": result.returncode, "stdout": result.stdout[:500], "stderr": result.stderr[:500]}
                        except Exception as e:
                            res = {"error": str(e)}
                        cursor.execute(
                            "UPDATE deliveries SET result=? WHERE event_id=? AND skill=?",
                            (json.dumps(res, ensure_ascii=False), ev["id"], args.skill),
                        )
                        conn.commit()
                    else:
                        print(f"  [{ev['id']}] {ev['topic']}/{ev['event_type']} | {ev['payload'][:80]}")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n🛑 监听停止")
    finally:
        conn.close()


def cmd_list(args: argparse.Namespace):
    conn = _init_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM events WHERE 1=1"
    params = []
    if args.topic:
        sql += " AND topic=?"
        params.append(args.topic)
    if args.type:
        sql += " AND event_type=?"
        params.append(args.type)
    if args.status:
        sql += " AND status=?"
        params.append(args.status)
    sql += " ORDER BY id DESC LIMIT ?"
    params.append(args.limit)

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    print(f"🐉 事件流（共 {len(rows)} 条）\n")
    print(f"{'ID':<6} {'TOPIC':<22} {'TYPE':<22} {'SOURCE':<18} {'STATUS':<10} {'PAYLOAD'}")
    print("-" * 110)
    for r in rows:
        payload = r["payload"][:60] + "..." if len(r["payload"]) > 60 else r["payload"]
        print(f"{r['id']:<6} {r['topic']:<22} {r['event_type']:<22} {r['source']:<18} {r['status']:<10} {payload}")
    conn.close()


def cmd_dispatch(args: argparse.Namespace):
    """四种分发模式：emit / waterfall / parallel / serial。

    emit     —— 广播：发布事件 + 每个订阅者各执行一次 handler（结果互不影响）
    waterfall—— 瀑布：订阅者按 priority 排队，前一个 handler 输出注入下一个输入
    parallel —— 并行：所有订阅者 handler 同时执行，等全部
    serial   —— 串行：按 priority 排队依次执行
    """
    conn = _init_db()
    cursor = conn.cursor()

    # 1. 发布事件（append-only 轨迹）
    payload = args.payload
    if not payload.startswith("{"):
        p = Path(payload)
        if p.exists():
            payload = p.read_text(encoding="utf-8")
        else:
            print(f"❌ payload 不是 JSON 且文件不存在: {payload}", file=sys.stderr)
            conn.close()
            sys.exit(2)
    try:
        json.loads(payload)
    except Exception as e:
        print(f"❌ payload 不是合法 JSON: {e}", file=sys.stderr)
        conn.close()
        sys.exit(2)

    ph = _payload_hash(args.topic, args.source, args.type, payload)
    dna = generate_dna("EVENT-BUS", "UID9622")
    now = datetime.now().isoformat()
    try:
        cur = conn.execute(
            "INSERT INTO events (timestamp, dna, topic, source, event_type, payload, payload_hash, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (now, dna, args.topic, args.source, args.type, payload, ph, "dispatched"),
        )
        event_id = cur.lastrowid
        conn.commit()
        print(f"✅ 事件已发布 | topic={args.topic} | type={args.type} | hash={ph} | mode={args.mode}")
    except sqlite3.IntegrityError:
        print(f"⏭️ 幂等跳过 | hash={ph}")
        conn.close()
        return

    # 2. 找到订阅者（按 priority 排序）
    if args.type:
        cursor.execute(
            "SELECT DISTINCT skill, priority FROM subscriptions WHERE topic=? AND (event_type=? OR event_type='*') ORDER BY priority",
            (args.topic, args.type),
        )
    else:
        cursor.execute(
            "SELECT DISTINCT skill, priority FROM subscriptions WHERE topic=? ORDER BY priority",
            (args.topic,),
        )
    subs = cursor.fetchall()
    conn.close()

    if not subs:
        print(f"⚠️ 无订阅者 | topic={args.topic}（事件已存档，后续 consume/listen 可拉取）")
        return
    if not args.handler:
        print(f"ℹ️ 无 --handler，仅存档（订阅者: {', '.join(s['skill'] for s in subs)}）")
        return

    env_base = {
        "LCB_EVENT_ID": str(event_id),
        "LCB_TOPIC": args.topic,
        "LCB_TYPE": args.type,
        "LCB_SOURCE": args.source,
        "LCB_DISPATCH_MODE": args.mode,
    }
    skills = [s["skill"] for s in subs]

    def _run_one(skill: str, inp: Optional[str], timeout: float) -> tuple:
        """执行单个订阅者 handler，返回 (skill, returncode, stdout, stderr)。"""
        env = os.environ.copy()
        env.update(env_base)
        env["LCB_SKILL"] = skill
        env["LCB_PAYLOAD"] = payload
        if inp is not None:
            env["LCB_WATERFALL_INPUT"] = inp
        try:
            result = subprocess.run(
                args.handler,
                shell=True,
                env=env,
                input=inp,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            return (skill, result.returncode, result.stdout[:800], result.stderr[:400])
        except subprocess.TimeoutExpired:
            return (skill, -1, "", "timeout")
        except Exception as e:
            return (skill, -2, "", str(e))

    results = []
    if args.mode == "waterfall":
        # 前一个 stdout 注入下一个 stdin
        stream = payload
        for skill in skills:
            skill, rc, out, err = _run_one(skill, stream, args.timeout)
            results.append({"skill": skill, "rc": rc, "stdout": out, "stderr": err})
            stream = out if out.strip() else stream
        final = stream
    elif args.mode == "parallel":
        outs: Dict[str, Any] = {}
        threads = []
        for skill in skills:
            t = threading.Thread(target=lambda s=skill: outs.update({s: _run_one(s, None, args.timeout)}))
            threads.append(t)
            t.start()
        for t in threads:
            t.join(args.timeout + 2)
        results = [{"skill": s, "rc": outs.get(s, (s, -3, "", "timeout"))[1],
                    "stdout": outs.get(s, (s, -3, "", "timeout"))[2],
                    "stderr": outs.get(s, (s, -3, "", "timeout"))[3]} for s in skills]
        final = payload
    elif args.mode == "serial":
        for skill in skills:
            skill_name, rc, out, err = _run_one(skill, None, args.timeout)
            results.append({"skill": skill_name, "rc": rc, "stdout": out, "stderr": err})
        final = payload
    else:  # emit 广播
        for skill in skills:
            skill_name, rc, out, err = _run_one(skill, None, args.timeout)
            results.append({"skill": skill_name, "rc": rc, "stdout": out, "stderr": err})
        final = payload

    if args.json:
        print(json.dumps({"event_id": event_id, "mode": args.mode, "results": results}, ensure_ascii=False))
        return
    print(f"🐉 分发完成 | mode={args.mode} | 订阅者 {len(skills)} 个")
    for r in results:
        mark = "🟢" if r["rc"] == 0 else "🔴"
        print(f"  {mark} {r['skill']:<20} rc={r['rc']}")
        if r["stdout"].strip():
            print(f"      → {r['stdout'].strip()[:150]}")
    if args.mode == "waterfall":
        print(f"  最终输出: {final[:200]}")


def cmd_stats(args: argparse.Namespace):
    conn = _init_db()
    cursor = conn.cursor()
    cursor.execute("SELECT status, COUNT(*) FROM events GROUP BY status")
    status_counts = dict(cursor.fetchall())
    cursor.execute("SELECT skill, COUNT(*) FROM subscriptions GROUP BY skill")
    subs = dict(cursor.fetchall())
    conn.close()
    print("📊 事件总线统计")
    print(f"   总事件: {sum(status_counts.values())}")
    for st, c in status_counts.items():
        print(f"   - {st}: {c}")
    print(f"   订阅者: {len(subs)}")
    for sk, c in subs.items():
        print(f"      {sk}: {c} 条订阅")


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂中枢事件总线 LCB")
    sub = parser.add_subparsers(dest="command", help="子命令")

    p_pub = sub.add_parser("publish", help="发布事件")
    p_pub.add_argument("--topic", required=True)
    p_pub.add_argument("--source", required=True)
    p_pub.add_argument("--type", required=True)
    p_pub.add_argument("--payload", required=True, help="JSON 字符串或 JSON 文件路径")

    p_sub = sub.add_parser("subscribe", help="注册订阅")
    p_sub.add_argument("--skill", required=True)
    p_sub.add_argument("--topic", required=True)
    p_sub.add_argument("--type", default=None)
    p_sub.add_argument("--priority", type=int, default=50)

    p_con = sub.add_parser("consume", help="消费事件")
    p_con.add_argument("--skill", required=True)
    p_con.add_argument("--limit", type=int, default=10)
    p_con.add_argument("--json", action="store_true", help="输出 JSON 数组")

    p_listen = sub.add_parser("listen", help="监听模式（守护进程）")
    p_listen.add_argument("--skill", required=True)
    p_listen.add_argument("--handler", default=None, help="事件触发时执行的命令（通过环境变量接收事件）")
    p_listen.add_argument("--interval", type=float, default=5.0)
    p_listen.add_argument("--limit", type=int, default=10)
    p_listen.add_argument("--json", action="store_true", help="handler 调用时使用 JSON 环境变量")

    p_list = sub.add_parser("list", help="查看事件流")
    p_list.add_argument("--topic", default=None)
    p_list.add_argument("--type", default=None)
    p_list.add_argument("--status", default=None)
    p_list.add_argument("--limit", type=int, default=20)

    sub.add_parser("stats", help="统计")

    p_disp = sub.add_parser("dispatch", help="分发事件（emit/waterfall/parallel/serial 四种模式）")
    p_disp.add_argument("--topic", required=True)
    p_disp.add_argument("--source", required=True)
    p_disp.add_argument("--type", required=True)
    p_disp.add_argument("--payload", required=True, help="JSON 字符串或 JSON 文件路径")
    p_disp.add_argument("--mode", default="emit", choices=["emit", "waterfall", "parallel", "serial"])
    p_disp.add_argument("--handler", default=None, help="订阅者执行命令（waterfall 时前一个 stdout 注入下一个 stdin）")
    p_disp.add_argument("--timeout", type=float, default=30.0)
    p_disp.add_argument("--json", action="store_true", help="输出 JSON 数组")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(2)

    globals()[f"cmd_{args.command}"](args)


if __name__ == "__main__":
    main()
