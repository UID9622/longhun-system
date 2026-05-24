#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂本地同步器 v1.0 · 读 ~/.longhun/secrets.env · L3 公开层先试
DNA: #龍芯⚡2026-05-20-LONGHUN-SYNC-v1.0
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

SECRETS = Path.home() / ".longhun" / "secrets.env"
NOTION_API = "https://api.notion.com/v1/pages"

SYSTEM_INFO = {
    "os": platform.system(),
    "arch": platform.machine(),
    "hostname": platform.node(),
    "user": os.getenv("USER", "unknown"),
    "uid9622": "#ZHUGEXIN⚡2025-DEVICE-BIND-SOUL",
}


def load_secrets() -> dict[str, str]:
    if not SECRETS.is_file():
        raise SystemExit(f"❌ 缺 {SECRETS} · 先跑接单台任务#1")
    out: dict[str, str] = {}
    for line in SECRETS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def file_hash(path: str) -> str:
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
    except OSError:
        return ""
    return h.hexdigest()[:16]


def send_to_notion(
    token: str,
    database_id: str,
    event_type: str,
    file_path: str,
    info: str = "",
) -> bool:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    now = datetime.now().isoformat()
    data = {
        "parent": {"database_id": database_id},
        "properties": {
            "事件": {"title": [{"text": {"content": event_type}}]},
            "文件路径": {"rich_text": [{"text": {"content": file_path[:2000]}}]},
            "时间": {"date": {"start": now}},
            "系统": {
                "rich_text": [
                    {"text": {"content": json.dumps(SYSTEM_INFO, ensure_ascii=False)[:2000]}}
                ]
            },
            "文件哈希": {"rich_text": [{"text": {"content": file_hash(file_path)}}]},
            "备注": {"rich_text": [{"text": {"content": info[:2000]}}]},
        },
    }
    try:
        r = requests.post(NOTION_API, headers=headers, json=data, timeout=15)
        ok = r.status_code in (200, 201)
        print(f"[{event_type}] {file_path} → {'✅' if ok else '❌ ' + str(r.status_code)}")
        if not ok:
            print(r.text[:300])
        return ok
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, token: str, database_id: str) -> None:
        self.token = token
        self.database_id = database_id

    def on_modified(self, event):
        if not event.is_directory:
            send_to_notion(self.token, self.database_id, "修改", event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            send_to_notion(self.token, self.database_id, "新增", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            send_to_notion(self.token, self.database_id, "删除", event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            send_to_notion(
                self.token,
                self.database_id,
                "移动",
                event.src_path,
                info=f"→ {getattr(event, 'dest_path', '')}",
            )


def main() -> None:
    sec = load_secrets()
    token = sec.get("NOTION_TOKEN", "")
    db_id = sec.get("DB_PUB", "") or os.getenv("DB_PUB", "")
    watch_dir = os.path.expanduser(os.getenv("LONGHUN_WATCH", "~/longhun-pub"))

    if not token or not token.startswith("ntn_"):
        raise SystemExit("❌ secrets.env 里 NOTION_TOKEN 未填（须 ntn_ 开头）")
    if not db_id or len(db_id) < 20:
        raise SystemExit("❌ secrets.env 里 DB_PUB 未填（任务#2 建库后回填）")

    print("🐉 龍魂本地同步器 · L3 公开层")
    print(f"   监听: {watch_dir}")
    print(f"   DB_PUB: {db_id[:8]}…")
    os.makedirs(watch_dir, exist_ok=True)

    observer = Observer()
    observer.schedule(ChangeHandler(token, db_id), watch_dir, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n👋 停止")
    observer.join()


if __name__ == "__main__":
    main()
