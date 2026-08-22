# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·万年历通知引擎 v1.0 —— 篡改警告/系统事件 → 标准 ICS 订阅源（苹果/鸿蒙日历通用）
DNA: #龍芯⚡️丙午·丙申·戊午·未时·䷐随-CALENDAR-FEED-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（核心思想层）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)  ← 工程实现层
"""

"""
功能：
  add    — 追加事件（🔴篡改 / 🟡差异 / 🟢例行），按 uid 去重
  ics    — 从事件库生成标准 RFC 5545 .ics（全天事件，保留 N 天）
  list   — 查看事件
  remove — 移除事件

数据目录（默认 ./calendar_data，可用环境变量 LH_CALENDAR_DIR 或 --data-dir 覆盖）：
  events.json  — 事件库（万年历页面 fetch 展示）
  longhun.ics  — 日历订阅源（苹果日历/鸿蒙日历 webcal:// 订阅）

事件去重指纹: (level + title + file) → 已存在则跳过（cron 每小时跑不刷屏）
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, date, timedelta, timezone

CAL_NAME = "龍魂预警日历"
CAL_DESC = "龍魂系统篡改警告与系统事件（UID9622 · 数据主权）"
LEVELS = {"🔴": 1, "🟡": 3, "🟢": 5}


def _data_dir(arg):
    d = arg or os.environ.get("LH_CALENDAR_DIR") or "calendar_data"
    os.makedirs(d, exist_ok=True)
    return d


def _load_events(dd):
    p = os.path.join(dd, "events.json")
    if os.path.exists(p):
        try:
            return json.loads(open(p, encoding="utf-8").read()).get("events", [])
        except Exception:
            return []
    return []


def _save_events(dd, events):
    with open(os.path.join(dd, "events.json"), "w", encoding="utf-8") as f:
        json.dump({"calendar": CAL_NAME, "updated": datetime.now().astimezone().isoformat(),
                   "events": events}, f, ensure_ascii=False, indent=2)


def add_event(dd, level, title, desc="", file="", keep_days=30):
    level = level if level in LEVELS else "🟢"
    events = _load_events(dd)
    # 去重指纹
    uid_base = hashlib.sha1(f"{level}|{title}|{file}".encode()).hexdigest()[:10]
    for ev in events:
        if ev.get("uid_base") == uid_base:
            return ev, False  # 已存在
    uid = f"lh-{uid_base}"
    ev = {
        "uid": uid,
        "uid_base": uid_base,
        "level": level,
        "priority": LEVELS[level],
        "title": title,
        "desc": desc,
        "file": file,
        "ts": datetime.now(timezone.utc).astimezone().isoformat(),
        "date": date.today().isoformat(),  # 事件发生日（日历全天事件用）
        "dna": _stamp_compact(),
    }
    events.insert(0, ev)
    # 保留最近 keep_days 天事件 + 上限 200
    cutoff = (date.today() - timedelta(days=keep_days)).isoformat()
    events = [e for e in events if e["date"] >= cutoff][:200]
    _save_events(dd, events)
    _gen_ics(dd, events)
    return ev, True


def _stamp_compact():
    try:
        for rel in ("bin", "08_BIN"):
            p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", rel, "lh_time_engine.py")
            if os.path.exists(p):
                sys.path.insert(0, os.path.dirname(p))
                from lh_time_engine import get_output_stamp
                return get_output_stamp().replace(" ", "_")[:40]
    except Exception:
        pass
    return f"#龍芯⚡️{date.today().isoformat()}"


def _fold(line: str):
    """RFC 5545 行折叠：>75 octets 用 CRLF+空格续行"""
    out, cur = [], ""
    for ch in line:
        cur += ch
        if len(cur.encode("utf-8")) >= 70:
            out.append(cur)
            cur = " "
    if cur.strip():
        out.append(cur)
    return "".join(out)


def _gen_ics(dd, events=None):
    events = events if events is not None else _load_events(dd)
    now = datetime.now(timezone.utc)
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//LongHun//Sovereign Calendar//CN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:{CAL_NAME}",
        f"X-WR-CALDESC:{CAL_DESC}",
        "X-PUBLISHED-TTL:PT1H",   # 订阅端每小时刷新
        "X-WR-TIMEZONE:Asia/Shanghai",
    ]
    for ev in events:
        d = ev["date"].replace("-", "")
        stamp = now.strftime("%Y%m%dT%H%M%SZ")
        summary = f"{ev['level']} {ev['title']}"
        desc = ev["desc"] or ""
        if ev["file"]:
            desc += f"\n涉及文件: {ev['file']}"
        desc += f"\nDNA: {ev['dna']}"
        # 转义
        summary = summary.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,")
        desc = desc.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")
        lines += [
            "BEGIN:VEVENT",
            f"UID:{ev['uid']}@longhun.uid9622.cn",
            f"DTSTAMP:{stamp}",
            f"DTSTART;VALUE=DATE:{d}",
            "DURATION:P1D",
            f"SUMMARY:{_fold(summary)}",
            f"DESCRIPTION:{_fold(desc)}",
            f"PRIORITY:{ev['priority']}",
            "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    body = "\r\n".join(lines) + "\r\n"
    with open(os.path.join(dd, "longhun.ics"), "w", encoding="utf-8") as f:
        f.write(body)
    return len(events)


def list_events(dd, limit=20):
    events = _load_events(dd)
    print(f"📅 {CAL_NAME} · 共 {len(events)} 条事件")
    for ev in events[:limit]:
        print(f"  {ev['level']} [{ev['date']}] {ev['title']}  ({ev['uid']})")
        if ev["file"]:
            print(f"      ↳ {ev['file']}")
    return events


def remove_event(dd, uid):
    events = _load_events(dd)
    new = [e for e in events if e["uid"] != uid]
    if len(new) == len(events):
        print(f"未找到事件: {uid}")
        return 1
    _save_events(dd, new)
    _gen_ics(dd, new)
    print(f"已移除 {uid} · 剩余 {len(new)} 条")
    return 0


def main():
    ap = argparse.ArgumentParser(description="🐉 龍魂·万年历通知引擎 v1.0")
    ap.add_argument("--data-dir", help="数据目录(默认 calendar_data 或 $LH_CALENDAR_DIR)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="追加事件")
    p_add.add_argument("--level", default="🟡", choices=["🔴", "🟡", "🟢"])
    p_add.add_argument("--title", required=True)
    p_add.add_argument("--desc", default="")
    p_add.add_argument("--file", default="")

    sub.add_parser("ics", help="重新生成 longhun.ics")
    sub.add_parser("list", help="查看事件")
    p_rm = sub.add_parser("remove", help="移除事件")
    p_rm.add_argument("uid")
    args = ap.parse_args()

    dd = _data_dir(getattr(args, "data_dir", None))
    if args.cmd == "add":
        ev, created = add_event(dd, args.level, args.title, args.desc, args.file)
        print(("✅ 新事件: " if created else "⏭️ 已存在(跳过): ") + f"{ev['level']} {ev['title']}")
        print(f"📄 ICS: {os.path.join(dd, 'longhun.ics')}")
    elif args.cmd == "ics":
        n = _gen_ics(dd)
        print(f"✅ longhun.ics 已生成 · {n} 条事件 · {os.path.join(dd, 'longhun.ics')}")
    elif args.cmd == "list":
        list_events(dd)
    elif args.cmd == "remove":
        sys.exit(remove_event(dd, args.uid))


if __name__ == "__main__":
    main()
