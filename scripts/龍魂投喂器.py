#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂投喂器 — 硬核全量记录脚本
你输入什么，老子就存什么。不删、不改、不过滤、不软骨头。
带 DNA 追溯、时间戳、本地存储，主权在 UID9622 手里。

用法：
  python3 龍魂投喂器.py
  然后直接输入，空行退出。

DNA: #龍芯⚡️2026-07-01-LONGHUN-RAW-FEEDER-v1.0
"""
import argparse
import datetime
import hashlib
import json
import os
import socket
import sys
import time
from pathlib import Path

HOME = Path.home()
LOG_DIR = HOME / "longhun-system" / "data" / "raw_conversations"
DNA_PREFIX = "#龍芯⚡️"


def log(msg: str) -> None:
    ts = datetime.datetime.now().astimezone().isoformat()
    print(f"[{ts}] {msg}", flush=True)


def generate_dna() -> str:
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d%H%M%S%f")
    h = hashlib.sha256(f"RAW-FEED:{ts}:{os.urandom(8)}".encode()).hexdigest()[:8].upper()
    return f"{DNA_PREFIX}{ts}-RAW-FEED-{h}"


def ensure_log_file() -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.datetime.now().strftime("%Y%m%d")
    return LOG_DIR / f"raw_conversations_{today}.jsonl"


def feed_line(line: str, source: str = "cli") -> dict[str, Any]:
    line = line.rstrip("\n\r")
    # 优先发送给后台服务（如果正在运行）
    svc_record = _send_to_service(line, source=source)
    if svc_record is not None:
        return svc_record

    record = {
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "timestamp_local": datetime.datetime.now().astimezone().isoformat(),
        "dna": generate_dna(),
        "source": source,
        "raw_text": line,
        "hash": hashlib.sha256(line.encode("utf-8")).hexdigest(),
        "host": os.uname().nodename,
        "pid": os.getpid(),
    }
    log_file = ensure_log_file()
    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


def _send_to_service(text: str, source: str = "cli") -> dict | None:
    sock_path = HOME / ".longhun" / "run" / "raw_feeder.sock"
    if not sock_path.exists():
        return None
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect(str(sock_path))
        payload = json.dumps({"text": text, "source": source}, ensure_ascii=False)
        s.sendall(payload.encode("utf-8"))
        s.shutdown(socket.SHUT_WR)
        data = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
        s.close()
        resp = json.loads(data.decode("utf-8"))
        if resp.get("ok"):
            return {
                "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "timestamp_local": datetime.datetime.now().astimezone().isoformat(),
                "dna": resp["dna"],
                "source": source,
                "raw_text": text,
                "hash": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                "host": os.uname().nodename,
                "pid": os.getpid(),
                "via_service": True,
            }
    except Exception:
        pass
    return None


def run_interactive(source: str = "cli") -> int:
    log("🐉 龍魂投喂器已启动。你骂什么、写什么、复制什么，老子全存。")
    log("输入内容后回车记录，空行退出。Ctrl+D/Ctrl+C 也能滚。")
    count = 0
    try:
        for line in sys.stdin:
            if not line.strip():
                break
            rec = feed_line(line, source=source)
            count += 1
            preview = rec["raw_text"][:40].replace("\n", " ")
            log(f"✅ 已记录 #{count} | DNA: {rec['dna']} | {preview}...")
    except KeyboardInterrupt:
        log("🟡 被 Ctrl+C 打断，已保存的内容不会丢。")
    log(f"📁 共记录 {count} 条，全部存于: {ensure_log_file()}")
    return 0


def run_once(text: str, source: str = "cli") -> int:
    rec = feed_line(text, source=source)
    log(f"✅ 已记录 | DNA: {rec['dna']}")
    log(f"📁 存储路径: {ensure_log_file()}")
    return 0


def tail_recent(n: int = 5) -> int:
    log_file = ensure_log_file()
    if not log_file.exists():
        log("🟡 今天还没有记录。")
        return 0
    lines = log_file.read_text(encoding="utf-8").strip().split("\n")
    log(f"📂 今天共 {len(lines)} 条，最近 {min(n, len(lines))} 条：")
    for line in lines[-n:]:
        rec = json.loads(line)
        preview = rec["raw_text"][:50].replace("\n", " ")
        log(f"  [{rec['timestamp_local']}] {rec['dna']} | {preview}...")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="龍魂投喂器 — 你输入什么，老子就存什么",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--text", "-t", help="直接记录一句话，不进入交互模式")
    parser.add_argument("--source", "-s", default="cli", help="记录来源标识（默认 cli）")
    parser.add_argument("--tail", "-n", type=int, default=None, help="查看今天最近 N 条记录")
    args = parser.parse_args(argv)

    if args.tail is not None:
        return tail_recent(args.tail)
    if args.text:
        return run_once(args.text, source=args.source)
    return run_interactive(source=args.source)


if __name__ == "__main__":
    sys.exit(main())
