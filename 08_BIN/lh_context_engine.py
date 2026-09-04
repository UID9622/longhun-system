#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·壬戌·申时·䷖剥-INDEX-CONTEXT-ENGINE-V1-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2
"""
龍魂 · 主动感知引擎（第1层 Context-Aware Sensing）
哲学①主动感知 → 无感捕获：当前文件/历史命令/对话内容
存储: ~/.longhun/index/context.json（本地优先）
用法:
  lh_context_engine.py capture <path>
  lh_context_engine.py session --input <text>
  lh_context_engine.py context [--json]
"""
import argparse, json, re
from datetime import datetime, timezone
from pathlib import Path

CTX_FILE = Path.home() / ".longhun" / "index" / "context.json"
EMPTY = {"version": "1.0", "sessions": [], "recent_files": []}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load() -> dict:
    if CTX_FILE.exists():
        try:
            return json.loads(CTX_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return EMPTY


def save(d):
    CTX_FILE.parent.mkdir(parents=True, exist_ok=True)
    CTX_FILE.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


def capture(path: str) -> dict:
    d = load()
    p = Path(path)
    entry = {"path": str(p), "name": p.name, "at": now_iso()}
    d["recent_files"] = [e for e in d["recent_files"] if e["path"] != str(p)]
    d["recent_files"].insert(0, entry)
    d["recent_files"] = d["recent_files"][:20]
    save(d)
    return entry


def add_session(text: str, source: str = "dialogue") -> int:
    d = load()
    d["sessions"].append({"text": text[:2000], "source": source, "at": now_iso()})
    if len(d["sessions"]) > 200:
        d["sessions"] = d["sessions"][-200:]
    save(d)
    return len(d["sessions"])


def get_context(top_k: int = 10) -> dict:
    d = load()
    recent = d.get("recent_files", [])
    words = re.findall(r"[A-Za-z0-9_\u4e00-\u9fff]+", " ".join(e["name"] for e in recent))
    keywords = [w for w in words if len(w) > 1][:10]
    return {
        "recent_files": recent[:top_k],
        "keywords": keywords,
        "session_count": len(d.get("sessions", [])),
        "last_session": d.get("sessions", [{}])[-1] if d.get("sessions") else None,
    }


def main():
    ap = argparse.ArgumentParser(description="龍魂主动感知引擎")
    ap.add_argument("cmd", choices=["capture", "session", "context"])
    ap.add_argument("arg", nargs="?", default="")
    ap.add_argument("--input", default="")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if args.cmd == "capture":
        e = capture(args.arg)
        print(f"👁️ 已感知: {e['name']} @ {e['at']}")
    elif args.cmd == "session":
        n = add_session(args.input or args.arg)
        print(f"💬 会话已记录 #{n}")
    elif args.cmd == "context":
        c = get_context()
        if args.json:
            print(json.dumps(c, ensure_ascii=False, indent=2))
        else:
            print("🔮 当前感知上下文:")
            for f in c["recent_files"]:
                print(f"  📄 {f['name']}")
            print(f"  🏷️ 关键词: {', '.join(c['keywords']) or '无'}")
            print(f"  💬 会话数: {c['session_count']}")


if __name__ == "__main__":
    main()
