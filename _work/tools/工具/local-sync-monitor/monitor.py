#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂草日志本地只读同步监控：拉取 Notion 页面块 → 拼文本 → SHA-256 → SQLite + JSONL + 快照。
不修改 Notion；不把 token 写进仓库。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv
from notion_client import Client

BASE_DIR = Path(__file__).resolve().parent


def load_config() -> dict[str, Any]:
    cfg_path = BASE_DIR / "config.yaml"
    with cfg_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_page_id_from_url(url: str) -> str:
    """从 Notion URL 取出 32 位 page id（无连字符）。"""
    url = url.strip().rstrip("/")
    part = url.split("/")[-1].split("?")[0].split("-")[-1]
    if len(part) == 32:
        return part
    raise ValueError(f"无法从 URL 解析页面 ID: {url}")


def to_uuid(page_id: str) -> str:
    page_id = page_id.replace("-", "").strip()
    if len(page_id) != 32:
        raise ValueError(f"页面 ID 长度应为 32: {page_id!r}")
    return (
        f"{page_id[0:8]}-{page_id[8:12]}-{page_id[12:16]}-"
        f"{page_id[16:20]}-{page_id[20:32]}"
    )


def rich_text_plain(rich: list[dict[str, Any]] | None) -> str:
    if not rich:
        return ""
    parts: list[str] = []
    for seg in rich:
        pt = seg.get("plain_text")
        if pt:
            parts.append(pt)
    return "".join(parts)


def block_to_line(block: dict[str, Any]) -> str:
    btype = block.get("type")
    if not btype:
        return ""
    payload = block.get(btype) or {}
    rich = payload.get("rich_text")
    text = rich_text_plain(rich)
    if btype.startswith("heading_"):
        level = btype.replace("heading_", "")
        return f"{'#' * int(level)} {text}\n"
    if btype == "bulleted_list_item":
        return f"- {text}\n"
    if btype == "numbered_list_item":
        return f"1. {text}\n"
    if btype == "to_do":
        chk = "x" if payload.get("checked") else " "
        return f"- [{chk}] {text}\n"
    if btype == "quote":
        return f"> {text}\n"
    if btype == "code":
        lang = payload.get("language") or ""
        return f"```{lang}\n{text}\n```\n"
    if btype in ("paragraph", "callout"):
        return f"{text}\n"
    if btype == "child_page":
        title = payload.get("title") or ""
        return f"[[子页面]] {title}\n"
    if btype == "divider":
        return "---\n"
    return f"[{btype}] {text}\n"


def collect_page_text(client: Client, block_id: str, lines: list[str]) -> None:
    cursor: str | None = None
    while True:
        kwargs: dict[str, Any] = {"block_id": block_id}
        if cursor:
            kwargs["start_cursor"] = cursor
        resp = client.blocks.children.list(**kwargs)
        for block in resp.get("results", []):
            lines.append(block_to_line(block))
            if block.get("has_children"):
                collect_page_text(client, block["id"], lines)
        if not resp.get("has_more"):
            break
        cursor = resp.get("next_cursor")


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS notion_log_sync (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page_url TEXT NOT NULL,
            pulled_at TEXT NOT NULL,
            content_sha256 TEXT NOT NULL,
            content_length INTEGER NOT NULL,
            changed INTEGER NOT NULL,
            status TEXT NOT NULL,
            dna TEXT,
            note TEXT
        );
        CREATE TABLE IF NOT EXISTS notion_log_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_time TEXT NOT NULL,
            event_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            page_url TEXT NOT NULL,
            message TEXT NOT NULL,
            content_sha256 TEXT,
            dna TEXT
        );
        """
    )
    conn.commit()


def last_hash(conn: sqlite3.Connection, page_url: str) -> str | None:
    row = conn.execute(
        "SELECT content_sha256 FROM notion_log_sync "
        "WHERE page_url = ? ORDER BY id DESC LIMIT 1",
        (page_url,),
    ).fetchone()
    return row[0] if row else None


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False) + "\n"
    with path.open("a", encoding="utf-8") as f:
        f.write(line)


def check_anchors(
    text: str, rules: dict[str, Any], conn: sqlite3.Connection, page_url: str, h: str
) -> None:
    now = datetime.now(timezone.utc).isoformat()
    for kw in rules.get("require_keywords", []):
        if kw not in text:
            conn.execute(
                "INSERT INTO notion_log_events "
                "(event_time, event_type, severity, page_url, message, content_sha256, dna) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    now,
                    "ANCHOR_MISSING",
                    "RED",
                    page_url,
                    f"缺失必备锚点或指纹片段: {kw[:48]}…",
                    h,
                    None,
                ),
            )
    for pair in rules.get("forbidden_replacements", []):
        fr = pair.get("from")
        to = pair.get("to")
        if fr and to and fr in text and to in text:
            conn.execute(
                "INSERT INTO notion_log_events "
                "(event_time, event_type, severity, page_url, message, content_sha256, dna) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    now,
                    "LONG_TO_SIMPLIFIED_TAMPER",
                    "RED",
                    page_url,
                    f"检测到「{fr}」与「{to}」同时出现，疑似简繁篡改混排",
                    h,
                    None,
                ),
            )
    conn.commit()


def run_once(cfg: dict[str, Any], token: str, page_uuid: str, page_url: str) -> int:
    client = Client(auth=token)
    lines: list[str] = []
    collect_page_text(client, page_uuid, lines)
    plain = "".join(lines)
    h = hashlib.sha256(plain.encode("utf-8")).hexdigest()
    length = len(plain.encode("utf-8"))

    db_path = BASE_DIR / cfg["local"]["db_path"]
    jsonl_path = BASE_DIR / cfg["local"]["jsonl_path"]
    snap_dir = BASE_DIR / cfg["local"]["snapshot_dir"]

    conn = sqlite3.connect(db_path)
    init_db(conn)
    prev = last_hash(conn, page_url)
    if prev is None:
        status = "initial"
        changed = 1
    elif prev == h:
        status = "unchanged"
        changed = 0
    else:
        status = "changed"
        changed = 1

    now = datetime.now(timezone.utc).isoformat()

    if status == "changed" or status == "initial":
        snap_dir.mkdir(parents=True, exist_ok=True)
        safe_ts = now.replace(":", "-").replace("+00:00", "Z")
        snap_name = f"{safe_ts}_{h[:16]}.md"
        snap_path = snap_dir / snap_name
        snap_path.write_text(plain, encoding="utf-8")

    conn.execute(
        "INSERT INTO notion_log_sync "
        "(page_url, pulled_at, content_sha256, content_length, changed, status, dna, note) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (page_url, now, h, length, changed, status, None, None),
    )
    conn.commit()

    check_anchors(plain, cfg.get("rules", {}), conn, page_url, h)

    append_jsonl(
        jsonl_path,
        {
            "pulled_at": now,
            "page_url": page_url,
            "content_sha256": h,
            "content_length": length,
            "status": status,
            "changed": bool(changed),
        },
    )
    conn.close()
    print(f"[OK] status={status} sha256={h} len={length}", flush=True)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="龍魂草日志 Notion 只读监控")
    parser.add_argument("--once", action="store_true", help="只执行一轮拉取")
    parser.add_argument("--watch", action="store_true", help="按 config 间隔循环拉取")
    args = parser.parse_args()
    if not args.once and not args.watch:
        parser.error("请指定 --once 或 --watch")

    load_dotenv(BASE_DIR / ".env")
    token = os.getenv("NOTION_TOKEN", "").strip()
    page_id_env = os.getenv("NOTION_LOG_PAGE_ID", "").strip()

    cfg = load_config()
    page_url = cfg["notion"]["log_page_url"]
    try:
        page_id = page_id_env or parse_page_id_from_url(page_url)
        page_uuid = to_uuid(page_id)
    except ValueError as e:
        print(f"[错误] {e}", file=sys.stderr)
        return 1

    if not token:
        print(
            "[错误] 未设置 NOTION_TOKEN。请复制 .env.example 为 .env 并本地填写；勿发给 AI。",
            file=sys.stderr,
        )
        return 1

    if args.once:
        return run_once(cfg, token, page_uuid, page_url)

    interval = int(cfg["notion"].get("poll_seconds", 300))
    print(f"[watch] 每 {interval} 秒拉取一次，Ctrl+C 结束", flush=True)
    while True:
        try:
            print("[watch] 正在拉取 Notion（大页面可能要几十秒，请稍候）…", flush=True)
            run_once(cfg, token, page_uuid, page_url)
        except Exception as e:
            print(f"[异常] {e}", file=sys.stderr)
            db_path = BASE_DIR / cfg["local"]["db_path"]
            jsonl_path = BASE_DIR / cfg["local"]["jsonl_path"]
            conn = sqlite3.connect(db_path)
            init_db(conn)
            now = datetime.now(timezone.utc).isoformat()
            conn.execute(
                "INSERT INTO notion_log_events "
                "(event_time, event_type, severity, page_url, message, content_sha256, dna) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    now,
                    "FETCH_ERROR",
                    "YELLOW",
                    page_url,
                    str(e),
                    None,
                    None,
                ),
            )
            conn.commit()
            conn.close()
            append_jsonl(
                jsonl_path,
                {"pulled_at": now, "page_url": page_url, "status": "error", "error": str(e)},
            )
        print(f"[watch] 已休眠 {interval} 秒，下一轮继续…", flush=True)
        time.sleep(interval)


if __name__ == "__main__":
    raise SystemExit(main())
