#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
龍魂系统 · 苹果日历联动脚本 v1.0
LongHun → Calendar.app → iCloud → iPhone
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DNA追溯码: #龍芯⚡️2026-03-20-苹果日历联动-v1.0
GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

创建者: UID9622 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）

工作原理:
  1. 读取 ~/longhun-system/tasks.json（任务源）
  2. 用 osascript 写入 Calendar.app
  3. iCloud 自动同步到 iPhone/iPad
  4. 已同步的任务记录到 synced_events.json（去重）

任务格式（tasks.json）:
  [
    {
      "id": "TASK-001",            # 唯一ID，用于去重
      "title": "任务标题",
      "date": "2026-03-21",        # YYYY-MM-DD
      "time": "09:00",             # HH:MM，可省略（默认全天）
      "duration": 60,              # 分钟，可省略（默认60）
      "note": "备注内容",           # 可省略
      "calendar": "工作",           # 可省略（默认 工作）
      "dna": "#龍芯⚡️..."          # 可省略
    }
  ]

用法:
  python3 longhun_calendar_sync.py              # 同步 tasks.json
  python3 longhun_calendar_sync.py --add        # 交互式添加单条任务
  python3 longhun_calendar_sync.py --list       # 列出已同步任务
  python3 longhun_calendar_sync.py --clear      # 清空同步记录（不删日历事件）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import json
import subprocess
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# ── 路径配置 ──────────────────────────────────────────────
BASE_DIR    = Path.home() / "longhun-system"
TASKS_FILE  = BASE_DIR / "tasks.json"
SYNCED_FILE = BASE_DIR / "logs" / "synced_events.json"
DEFAULT_CAL = "工作"   # 默认写入的日历名（iCloud 账号下）

# ── 工具函数 ──────────────────────────────────────────────

def load_tasks() -> list:
    if not TASKS_FILE.exists():
        print(f"[INFO] tasks.json 不存在，自动创建示例文件: {TASKS_FILE}")
        sample = [
            {
                "id": "TASK-001",
                "title": "龍魂系统每日复盘",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "time": "21:00",
                "duration": 30,
                "note": "检查 action_log / 看板更新 / Notion同步",
                "calendar": "工作",
                "dna": "#龍芯⚡️2026-03-20-每日复盘-v1.0"
            }
        ]
        TASKS_FILE.write_text(json.dumps(sample, ensure_ascii=False, indent=2))
        return sample
    return json.loads(TASKS_FILE.read_text())


def load_synced() -> dict:
    if not SYNCED_FILE.exists():
        return {}
    return json.loads(SYNCED_FILE.read_text())


def save_synced(synced: dict):
    SYNCED_FILE.parent.mkdir(parents=True, exist_ok=True)
    SYNCED_FILE.write_text(json.dumps(synced, ensure_ascii=False, indent=2))


def build_applescript(task: dict) -> str:
    """把一条任务转成 AppleScript"""
    title    = task["title"].replace('"', '\\"')
    note     = task.get("note", "").replace('"', '\\"')
    dna      = task.get("dna", "")
    cal_name = task.get("calendar", DEFAULT_CAL)
    duration = int(task.get("duration", 60))

    # 解析日期时间
    date_str = task["date"]           # YYYY-MM-DD
    time_str = task.get("time", "")   # HH:MM 或空
    all_day  = not time_str

    if time_str:
        dt_start = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        dt_end   = dt_start + timedelta(minutes=duration)
        # AppleScript 日期格式：YYYY/MM/DD HH:MM:SS
        as_start = dt_start.strftime("%Y/%m/%d %H:%M:%S")
        as_end   = dt_end.strftime("%Y/%m/%d %H:%M:%S")
        date_block = f'start date:date "{as_start}", end date:date "{as_end}"'
    else:
        # 全天事件
        dt_start = datetime.strptime(date_str, "%Y-%m-%d")
        as_start = dt_start.strftime("%Y/%m/%d 00:00:00")
        as_end   = (dt_start + timedelta(days=1)).strftime("%Y/%m/%d 00:00:00")
        date_block = f'start date:date "{as_start}", end date:date "{as_end}", allday event:true'

    full_note = f"{note}\nDNA: {dna}".strip() if dna else note

    script = f'''
tell application "Calendar"
    -- 确保目标日历存在，不存在则创建
    if not (exists calendar "{cal_name}") then
        make new calendar with properties {{name:"{cal_name}"}}
    end if
    tell calendar "{cal_name}"
        set newEvent to make new event with properties {{{date_block}, summary:"{title}", description:"{full_note}"}}
    end tell
    reload calendars
end tell
return "OK"
'''
    return script.strip()


def run_applescript(script: str) -> tuple[bool, str]:
    """执行 AppleScript，返回 (成功, 输出)"""
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        return True, result.stdout.strip()
    return False, result.stderr.strip()


# ── 核心同步逻辑 ──────────────────────────────────────────

def sync_tasks():
    tasks  = load_tasks()
    synced = load_synced()

    new_count = skip_count = fail_count = 0

    print(f"\n🐉 龍魂日历同步 · {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("─" * 50)

    for task in tasks:
        task_id = task.get("id", task["title"])

        if task_id in synced:
            print(f"  ⏭  跳过（已同步）: {task['title']}")
            skip_count += 1
            continue

        script  = build_applescript(task)
        ok, msg = run_applescript(script)

        if ok:
            synced[task_id] = {
                "title":   task["title"],
                "date":    task["date"],
                "synced_at": datetime.now().isoformat()
            }
            print(f"  ✅ 同步成功: {task['title']}  ({task['date']} {task.get('time','')})")
            new_count += 1
        else:
            print(f"  ❌ 同步失败: {task['title']}")
            print(f"     错误: {msg}")
            fail_count += 1

    save_synced(synced)

    print("─" * 50)
    print(f"  新增: {new_count}  跳过: {skip_count}  失败: {fail_count}")
    print(f"  iCloud 会在几秒内自动推送到 iPhone ✅")
    print()


# ── 交互式添加单条任务 ────────────────────────────────────

def add_task_interactive():
    print("\n🐉 龍魂日历 · 添加任务")
    print("─" * 40)

    title    = input("任务标题: ").strip()
    date_str = input("日期 (YYYY-MM-DD，回车=今天): ").strip()
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")

    time_str = input("时间 (HH:MM，回车=全天): ").strip()
    duration = input("时长(分钟，回车=60): ").strip() or "60"
    note     = input("备注 (可空): ").strip()
    cal_name = input(f"日历名 (回车='{DEFAULT_CAL}'): ").strip() or DEFAULT_CAL

    # 自动生成 ID 和 DNA
    ts    = datetime.now().strftime("%Y%m%d%H%M%S")
    dna   = f"#龍芯⚡️{ts}-{title[:8]}-v1.0"
    task_id = f"TASK-{ts}"

    task = {
        "id":       task_id,
        "title":    title,
        "date":     date_str,
        "note":     note,
        "calendar": cal_name,
        "dna":      dna
    }
    if time_str:
        task["time"]     = time_str
        task["duration"] = int(duration)

    # 写入 tasks.json
    tasks = load_tasks()
    tasks.append(task)
    TASKS_FILE.write_text(json.dumps(tasks, ensure_ascii=False, indent=2))
    print(f"\n  已追加到 tasks.json，开始同步...")

    # 直接同步这一条
    script  = build_applescript(task)
    ok, msg = run_applescript(script)

    if ok:
        synced = load_synced()
        synced[task_id] = {"title": title, "date": date_str, "synced_at": datetime.now().isoformat()}
        save_synced(synced)
        print(f"  ✅ 已写入日历「{cal_name}」，iCloud 自动同步到 iPhone")
        print(f"  DNA: {dna}")
    else:
        print(f"  ❌ 失败: {msg}")


# ── 列出已同步任务 ────────────────────────────────────────

def list_synced():
    synced = load_synced()
    if not synced:
        print("  暂无同步记录")
        return
    print(f"\n已同步 {len(synced)} 条任务：")
    print("─" * 50)
    for tid, info in synced.items():
        print(f"  [{info['date']}] {info['title']}  (ID: {tid})")
    print()


# ── 入口 ─────────────────────────────────────────────────

if __name__ == "__main__":
    args = sys.argv[1:]

    if "--add" in args:
        add_task_interactive()
    elif "--list" in args:
        list_synced()
    elif "--clear" in args:
        save_synced({})
        print("  同步记录已清空（日历事件不受影响）")
    else:
        sync_tasks()
