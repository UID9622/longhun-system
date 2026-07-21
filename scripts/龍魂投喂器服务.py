#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂投喂器服务 — 后台常驻，开机自启
监听 Unix Domain Socket，接收什么就存什么，不删不改不过滤。

DNA: #龍芯⚡️2026-07-01-LONGHUN-RAW-FEEDER-SERVICE-v1.0
"""
import datetime
import hashlib
import json
import os
import socket
import sys
import threading
from pathlib import Path

HOME = Path.home()
LOG_DIR = HOME / "longhun-system" / "data" / "raw_conversations"
RUN_DIR = HOME / ".longhun" / "run"
SOCK_PATH = RUN_DIR / "raw_feeder.sock"
DNA_PREFIX = "#龍芯⚡️"


def log(msg: str) -> None:
    ts = datetime.datetime.now().astimezone().isoformat()
    print(f"[{ts}] {msg}", flush=True)


def generate_dna() -> str:
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d%H%M%S%f")
    h = hashlib.sha256(f"RAW-FEED-SVC:{ts}:{os.urandom(8)}".encode()).hexdigest()[:8].upper()
    return f"{DNA_PREFIX}{ts}-RAW-FEED-SVC-{h}"


def ensure_log_file() -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.datetime.now().strftime("%Y%m%d")
    return LOG_DIR / f"raw_conversations_{today}.jsonl"


def feed(text: str, source: str = "socket") -> dict[str, Any]:
    record = {
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "timestamp_local": datetime.datetime.now().astimezone().isoformat(),
        "dna": generate_dna(),
        "source": source,
        "raw_text": text,
        "hash": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "host": os.uname().nodename,
        "pid": os.getpid(),
    }
    log_file = ensure_log_file()
    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


def handle_client(conn: socket.socket, addr: str) -> None:
    try:
        data = b""
        while True:
            chunk = conn.recv(65536)
            if not chunk:
                break
            data += chunk
        if not data:
            return
        try:
            payload = json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            payload = {"text": data.decode("utf-8", errors="replace")}
        text = payload.get("text", "")
        source = payload.get("source", "socket")
        if text:
            rec = feed(text, source=source)
            resp = {"ok": True, "dna": rec["dna"], "timestamp": rec["timestamp_local"]}
            log(f"✅ 已记录 | DNA: {rec['dna']} | {rec['raw_text'][:40]}...")
        else:
            resp = {"ok": False, "error": "empty text"}
        conn.sendall(json.dumps(resp, ensure_ascii=False).encode("utf-8"))
    except Exception as e:
        log(f"🔴 处理连接异常: {e}")
    finally:
        conn.close()


def start_service() -> int:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    if SOCK_PATH.exists():
        SOCK_PATH.unlink()

    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.bind(str(SOCK_PATH))
    s.listen(128)
    log(f"🐉 龍魂投喂器服务已启动，监听: {SOCK_PATH}")
    log("开机自动运行中，随时接收输入。")

    try:
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, str(addr)), daemon=True).start()
    except KeyboardInterrupt:
        log("🟡 服务被中断")
    finally:
        s.close()
        if SOCK_PATH.exists():
            SOCK_PATH.unlink()
    return 0


def main(argv: list[str] | None = None) -> int:
    return start_service()


if __name__ == "__main__":
    sys.exit(main())
