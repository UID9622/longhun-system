#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·壬戌·戊申·䷌同人-AI-MESH-BUS-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂 · AI互通总线（AI Mesh Bus）v1.0

所有 AI（Kimi / CodeBuddy / DeepSeek / 未来任何 AI）共用一个人话入口：
  lh bus bind <ai名>          AI 进门：注册身份 + 订阅互通主题 + 读最近消息
  lh bus post "<消息>"        干完活：往总线发一条互通消息（source=当前AI）
  lh bus read [--last N]      开工前：读最近互通消息（完整内容）
  lh bus status               总线健康
  lh bus agents               已注册的 AI 名单

底层复用 LCB 事件总线（08_BIN/lh_event_bus.py · SQLite ~/.longhun/event_bus/）
——不重造轮子。本层只做：身份注册 + 人话封装 + 完整读取。

协议: 01_protocols/LH-AI-MESH-BUS-v1.0.md
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HOME = Path.home()
PROJECT_DIR = HOME / "longhun-system"
EVENT_BUS_PY = PROJECT_DIR / "08_BIN" / "lh_event_bus.py"
MESH_DIR = HOME / ".longhun" / "ai_mesh"
AGENTS_FILE = MESH_DIR / "agents.json"
DB_PATH = HOME / ".longhun" / "event_bus" / "event_bus.db"
TOPIC = "ai.mesh"  # AI 互通统一主题
CONFIRM_MARK = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


def _load_agents() -> dict:
    if AGENTS_FILE.exists():
        try:
            return json.loads(AGENTS_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {"agents": {}, "current": None}
    return {"agents": {}, "current": None}


def _save_agents(data: dict):
    MESH_DIR.mkdir(parents=True, exist_ok=True)
    AGENTS_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def cmd_bind(args: argparse.Namespace):
    """AI 进门：注册身份 + 订阅互通主题 + 读最近消息"""
    ai_name = args.ai.strip()
    if not ai_name:
        print("❌ --ai 不能为空（如 kimi / codebuddy / deepseek）")
        sys.exit(2)

    data = _load_agents()
    data["agents"].setdefault(ai_name, {})
    data["agents"][ai_name]["last_seen"] = datetime.now().isoformat()
    data["agents"][ai_name]["status"] = "active"
    data["current"] = ai_name
    _save_agents(data)

    # 订阅互通主题（幂等）
    subprocess.run(
        [sys.executable, str(EVENT_BUS_PY), "subscribe",
         "--skill", ai_name, "--topic", TOPIC],
        capture_output=True, text=True,
    )

    print(f"🐉 [{ai_name}] 已注册为龍魂 AI 互通节点（主权在你·消息池在本地）")
    print(f"   身份: {AGENTS_FILE}")
    print(f"   总线: {DB_PATH} · 主题: {TOPIC}")
    cmd_read(argparse.Namespace(last=10, json=False))


def cmd_post(args: argparse.Namespace):
    """干完活：发一条互通消息"""
    ai_name = args.ai or _load_agents().get("current")
    if not ai_name:
        print("❌ 请先 lh bus bind <ai名> 注册，或用 --ai 指定来源")
        sys.exit(2)

    if not args.message:
        print("❌ 消息不能为空：lh bus post \"你干了什么\" --ai kimi")
        sys.exit(2)

    tags = [t.strip() for t in (args.tags or "").split(",") if t.strip()]
    files = [f.strip() for f in (args.files or "").split(",") if f.strip()]
    payload = json.dumps({
        "message": args.message,
        "tags": tags,
        "files": files,
        "dna": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-AI-MESH-{ai_name.upper()}",
    }, ensure_ascii=False)

    r = subprocess.run(
        [sys.executable, str(EVENT_BUS_PY), "publish",
         "--topic", TOPIC, "--source", ai_name,
         "--type", args.type, "--payload", payload],
        capture_output=True, text=True,
    )
    out = (r.stdout or "").strip() + (r.stderr or "").strip()
    print(out)
    if r.returncode == 0:
        print(f"📨 互通消息已入总线 | source={ai_name} | 其他AI开工前会读到")


def cmd_read(args: argparse.Namespace):
    """开工前：读最近互通消息（直连 SQLite·完整内容）"""
    if not DB_PATH.exists():
        print("📭 总线还没有消息（首次使用：lh bus bind <ai名> 注册）")
        return
    import sqlite3
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT id, timestamp, source, event_type, payload FROM events "
        "WHERE topic=? ORDER BY id DESC LIMIT ?",
        (TOPIC, args.last),
    ).fetchall()
    conn.close()

    if not rows:
        print("📭 总线暂无互通消息")
        return

    print(f"🐉 AI 互通总线 · 最近 {len(rows)} 条（开工前先读这里）")
    print("-" * 78)
    for r in reversed(rows):  # 旧→新
        try:
            payload = json.loads(r["payload"])
            msg = payload.get("message", r["payload"])
            tags = payload.get("tags") or []
            files = payload.get("files") or []
        except Exception:
            msg, tags, files = r["payload"], [], []
        print(f"[{r['id']}] {r['timestamp'][:19]} | {r['source']} | {r['event_type']}")
        print(f"    📌 {msg}")
        if tags:
            print(f"    🏷️  {' '.join('#' + t for t in tags)}")
        if files:
            print(f"    📄  {' · '.join(files)}")
        print("-" * 78)


def cmd_status(args: argparse.Namespace):
    """总线健康"""
    data = _load_agents()
    agents = data.get("agents", {})
    print("🐉 AI 互通总线状态")
    print(f"   主题: {TOPIC}")
    print(f"   已注册 AI: {len(agents)}")
    for name, info in agents.items():
        cur = " ← 当前" if name == data.get("current") else ""
        print(f"     - {name} | 最后活跃 {info.get('last_seen', '?')[:19]}{cur}")
    print(f"   消息库: {DB_PATH}")
    if DB_PATH.exists():
        import sqlite3
        conn = sqlite3.connect(str(DB_PATH))
        n = conn.execute(
            "SELECT COUNT(*) FROM events WHERE topic=?", (TOPIC,)
        ).fetchone()[0]
        conn.close()
        print(f"   互通消息总数: {n}")
    print(f"   确认码: {CONFIRM_MARK}")


def cmd_agents(args: argparse.Namespace):
    data = _load_agents()
    agents = data.get("agents", {})
    if not agents:
        print("📭 还没有 AI 注册。绑定：lh bus bind kimi / lh bus bind codebuddy")
        return
    for name, info in agents.items():
        cur = " ← 当前" if name == data.get("current") else ""
        print(f"  - {name} | 最后活跃 {info.get('last_seen', '?')[:19]}{cur}")


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂 AI互通总线")
    sub = parser.add_subparsers(dest="command")

    p_bind = sub.add_parser("bind", help="AI进门：注册身份+订阅+读最近消息")
    p_bind.add_argument("--ai", required=True, help="AI名: kimi/codebuddy/deepseek...")

    p_post = sub.add_parser("post", help="干完活发互通消息")
    p_post.add_argument("message", help="人话消息")
    p_post.add_argument("--ai", default=None, help="来源AI（缺省=当前绑定AI）")
    p_post.add_argument("--type", default="work_done", help="事件类型")
    p_post.add_argument("--tags", default="", help="逗号分隔标签")
    p_post.add_argument("--files", default="", help="逗号分隔本次产物路径")

    p_read = sub.add_parser("read", help="开工前读最近互通消息")
    p_read.add_argument("--last", type=int, default=10)

    sub.add_parser("status", help="总线健康")
    sub.add_parser("agents", help="已注册AI名单")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(2)
    globals()[f"cmd_{args.command}"](args)


if __name__ == "__main__":
    main()
