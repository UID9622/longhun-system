#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡2026-07-06-MEMORY-UNIFY-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
lh memory — 龍魂统一记忆入口

一句话搞定所有"记忆"相关的东西，不用猜该用哪个。

用法：
  lh memory                    # 一览所有记忆源状态
  lh memory search <关键词>    # 跨所有记忆源搜索
  lh memory star <标题> <内容> # 添加星辰记忆
  lh memory log <内容>         # 添加执行日志
  lh memory archive            # 列出 kimi 对话归档

DNA: #龍芯⚡2026-07-06-MEMORY-UNIFY-v1.0
"""

import argparse
import datetime
import json
import os
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 🛡️ P77 安全加固：SQL 表名白名单
# 所有动态拼接表名的 SQL 必须先过此校验
ALLOWED_SQLITE_TABLE_PATTERN = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
import re as _re


def _validate_table_name(tname: str) -> bool:
    """校验表名是否安全（仅允许字母数字下划线，防注入）"""
    return bool(_re.match(ALLOWED_SQLITE_TABLE_PATTERN, tname))


MEMORY_SOURCES = {
    "星辰记忆": {
        "path": ROOT / "memory-universe" / "星辰记忆.db",
        "type": "sqlite",
        "desc": "一世一双人·三生三世·星辰记忆 — 浪漫归档",
    },
    "AI核心记忆": {
        "path": ROOT / "brain" / "memories.db",
        "type": "sqlite",
        "desc": "协议·铁律·服务器状态 — AI 操作记忆",
    },
    "统一知识图谱": {
        "path": ROOT / "brain" / "unified_kg.db",
        "type": "sqlite",
        "desc": "节点+边 — 知识关系网络",
    },
    "Kimi对话归档": {
        "path": ROOT / "logs" / "kimi_session_archives",
        "type": "dir",
        "desc": "Kimi 对话压缩包",
    },
    "守护进程日志": {
        "path": ROOT / "agents" / "daemon_logs",
        "type": "dir",
        "desc": "心跳·审计·侦察兵情报",
    },
    "能力审计日志": {
        "path": ROOT / "capabilities" / "logs",
        "type": "dir",
        "desc": "能力审计+训练流水线",
    },
    "编辑器记忆": {
        "path": ROOT / "brain" / "editor_memory_archive",
        "type": "dir",
        "desc": "Cursor/VS Code 编辑器历史备份",
    },
    "执行记录": {
        "path": ROOT / "02_執行記錄",
        "type": "dir",
        "desc": "每日执行日志 markdown",
    },
}


def status():
    """一览所有记忆源状态"""
    print("╔══════════════════════════════════════════════════╗")
    print("║          🐉 龍魂统一记忆 · 状态一览              ║")
    print("╚══════════════════════════════════════════════════╝")
    print()

    for name, info in MEMORY_SOURCES.items():
        p = info["path"]
        exists = p.exists()
        icon = "🟢" if exists else "🔴"

        if info["type"] == "sqlite":
            try:
                db = sqlite3.connect(p)
                tables = db.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                ).fetchall()
                counts = {}
                for t in tables:
                    try:
                        counts[t[0]] = db.execute(
                            f'SELECT COUNT(*) FROM "{t[0]}"'
                        ).fetchone()[0]
                    except Exception:
                        counts[t[0]] = "?"
                db.close()
                detail = ", ".join(f"{t}={c}" for t, c in counts.items())
            except Exception:
                detail = "无法读取"
        else:
            try:
                items = list(p.iterdir())
                files = [f for f in items if f.is_file()]
                dirs = [f for f in items if f.is_dir()]
                detail = f"{len(files)} 文件, {len(dirs)} 子目录"
            except Exception:
                detail = "无法读取"

        print(f"  {icon} {name}")
        print(f"     {info['desc']}")
        print(f"     {detail}")
        print()

    # 快速统计
    print("---")
    print("快速统计：")
    total = 0
    for name, info in MEMORY_SOURCES.items():
        if info["type"] == "sqlite" and info["path"].exists():
            try:
                db = sqlite3.connect(info["path"])
                for row in db.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                ):
                    try:
                        total += db.execute(
                            f'SELECT COUNT(*) FROM "{row[0]}"'
                        ).fetchone()[0]
                    except Exception:
                        pass
                db.close()
            except Exception:
                pass

    kg = ROOT / "logs" / "kimi_session_archives"
    if kg.exists():
        total += len(list(kg.glob("*.zip")))

    print(f"  总计约 {total} 条记忆/日志/归档条目")


def search(keyword: str):
    """跨所有记忆源搜索"""
    print(f"🔍 搜索「{keyword}」...\n")

    found = 0
    for name, info in MEMORY_SOURCES.items():
        if info["type"] != "sqlite" or not info["path"].exists():
            continue
        try:
            db = sqlite3.connect(info["path"])
            tables = db.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
            for t in tables:
                tname = t[0]
                if not _validate_table_name(tname):
                    continue  # 🛡️ 表名不合法·跳过
                cols = [
                    c[1]
                    for c in db.execute(f'PRAGMA table_info("{tname}")').fetchall()
                ]
                # 搜索所有文本列
                for col in cols:
                    try:
                        rows = db.execute(
                            f'SELECT * FROM "{tname}" WHERE CAST({col} AS TEXT) LIKE ? LIMIT 10',
                            (f"%{keyword}%",),
                        ).fetchall()
                        if rows:
                            for row in rows:
                                found += 1
                                print(f"  📍 [{name}] {tname}.{col}")
                                # 找最长的文本字段展示
                                longest = max(
                                    (str(c) for c in row if str(c)),
                                    key=len,
                                    default="",
                                )
                                if len(longest) > 200:
                                    longest = longest[:200] + "..."
                                print(f"     {longest}")
                                print()
                    except Exception:
                        pass
            db.close()
        except Exception:
            pass

    # 搜索目录中的文本文件
    for name, info in MEMORY_SOURCES.items():
        if info["type"] != "dir" or not info["path"].exists():
            continue
        for f in info["path"].rglob("*"):
            if f.is_file() and f.suffix in (".md", ".json", ".jsonl", ".log", ".txt"):
                try:
                    content = f.read_text(encoding="utf-8", errors="ignore")
                    if keyword.lower() in content.lower():
                        found += 1
                        lines = content.split("\n")
                        for i, line in enumerate(lines):
                            if keyword.lower() in line.lower():
                                print(f"  📍 [{name}] {f.name}")
                                print(f"     {line.strip()[:200]}")
                                print()
                                break
                except Exception:
                    pass

    if found == 0:
        print(f"  ❌ 未找到「{keyword}」相关记录")
    else:
        print(f"  共找到 {found} 条记录")


def add_star(title: str, content: str):
    """添加星辰记忆"""
    sys.path.insert(0, str(ROOT / "memory-universe"))
    from importlib import import_module

    spec = import_module  # noqa
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "star", ROOT / "memory-universe" / "星辰记忆系统.py"
    )
    if spec is None or spec.loader is None:
        print("❌ 无法加载星辰记忆系统模块", file=sys.stderr)
        return
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    system = mod.星辰记忆系统()
    result = system.add(title, content)
    system.generate_page()
    print(f"✅ 星辰记忆已添加")
    print(f"   {json.dumps(result, indent=2, ensure_ascii=False)}")


def add_log(content: str):
    """添加执行日志到 02_執行記錄/"""
    today = datetime.date.today().isoformat()
    log_dir = ROOT / "02_執行記錄"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"{today}.md"

    now = datetime.datetime.now().strftime("%H:%M")
    dna_ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    dna = f"#龍芯⚡{dna_ts}-LOG-v1.0"

    entry = f"\n### {now} | {dna}\n\n{content}\n"

    if log_file.exists():
        existing = log_file.read_text(encoding="utf-8")
        if f"# {today}" not in existing:
            log_file.write_text(f"# {today}\n\n{entry}", encoding="utf-8")
        else:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(entry)
    else:
        log_file.write_text(f"# {today}\n\n{entry}", encoding="utf-8")

    print(f"✅ 日志已写入 {log_file}")


def list_archives():
    """列出 kimi 对话归档"""
    archive_dir = ROOT / "logs" / "kimi_session_archives"
    if not archive_dir.exists():
        print("❌ 无 kimi 对话归档")
        return

    archives = sorted(archive_dir.glob("*.zip"), key=os.path.getmtime, reverse=True)
    print(f"📦 Kimi 对话归档 ({len(archives)} 个)\n")
    for a in archives:
        size_kb = os.path.getsize(a) / 1024
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(a))
        print(f"  {a.name}")
        print(f"     {size_kb:.1f} KB | {mtime.strftime('%Y-%m-%d %H:%M')}")
    print()


def main():
    parser = argparse.ArgumentParser(description="龍魂统一记忆入口")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("status", help="一览所有记忆源状态")

    search_parser = sub.add_parser("search", help="跨所有记忆源搜索")
    search_parser.add_argument("keyword", help="搜索关键词")

    star_parser = sub.add_parser("star", help="添加星辰记忆")
    star_parser.add_argument("title", help="标题")
    star_parser.add_argument("content", help="内容")

    log_parser = sub.add_parser("log", help="添加执行日志")
    log_parser.add_argument("content", help="日志内容")

    sub.add_parser("archive", help="列出 kimi 对话归档")

    args = parser.parse_args()

    if args.command == "search":
        search(args.keyword)
    elif args.command == "star":
        add_star(args.title, args.content)
    elif args.command == "log":
        add_log(args.content)
    elif args.command == "archive":
        list_archives()
    else:
        status()


if __name__ == "__main__":
    main()
