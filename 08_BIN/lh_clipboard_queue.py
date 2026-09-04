#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
🐉 龍魂·剪贴板离线加密缓存队列 v1.0
======================================
DNA: #龍芯⚡️丙午·丙申·辛酉·辰时·䷜蹇-CLIPBOARD-QUEUE-V1.0-P1

代理离线时，把已加密的剪贴板 payload 暂存到本地 SQLite，恢复连接后批量上传。
队列中只保存加密后的内容，不保存明文。

用法:
  from lh_clipboard_queue import ClipQueue
  q = ClipQueue()
  q.enqueue(encrypted_payload, source="macos_clipboard")
  for payload in q.dequeue(batch_size=10):
      await send_to_hub(payload)
"""

import json
import sqlite3
import threading
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

CST = timezone(timedelta(hours=8))

DEFAULT_DB_PATH = Path.home() / ".longhun" / "cache" / "clipboard_queue.db"


class ClipQueue:
    """线程安全的 SQLite 离线缓存队列。"""

    def __init__(self, db_path: Optional[Path] = None, max_retry: int = 3):
        self.db_path = db_path or DEFAULT_DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.max_retry = max_retry
        self._lock = threading.Lock()
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(str(self.db_path), check_same_thread=False) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS clipboard_queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    payload TEXT NOT NULL,
                    source TEXT,
                    topic TEXT,
                    tags TEXT,
                    created_at TEXT NOT NULL,
                    retry_count INTEGER DEFAULT 0
                )
                """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_clipboard_queue_created
                ON clipboard_queue(created_at)
                """
            )
            conn.commit()

    def enqueue(
        self,
        payload: Dict[str, Any],
        source: Optional[str] = None,
        topic: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> int:
        """把一条待发送的加密 payload 入队，返回队列长度。"""
        with self._lock:
            with sqlite3.connect(str(self.db_path), check_same_thread=False) as conn:
                conn.execute(
                    "INSERT INTO clipboard_queue (payload, source, topic, tags, created_at) VALUES (?, ?, ?, ?, ?)",
                    (
                        json.dumps(payload, ensure_ascii=False),
                        source,
                        topic,
                        json.dumps(tags or [], ensure_ascii=False),
                        datetime.now(CST).isoformat(),
                    ),
                )
                conn.commit()
                cur = conn.execute("SELECT COUNT(*) FROM clipboard_queue")
                return cur.fetchone()[0]

    def dequeue(self, batch_size: int = 50) -> List[Dict[str, Any]]:
        """取出最多 batch_size 条待发送记录（按 FIFO）。"""
        with self._lock:
            with sqlite3.connect(str(self.db_path), check_same_thread=False) as conn:
                cur = conn.execute(
                    "SELECT id, payload, source, topic, tags, retry_count FROM clipboard_queue "
                    "ORDER BY created_at ASC, id ASC LIMIT ?",
                    (batch_size,),
                )
                rows = cur.fetchall()
                result = []
                for row in rows:
                    id_, payload_json, source, topic, tags_json, retry = row
                    payload = json.loads(payload_json)
                    if source and "source" not in payload:
                        payload["source"] = source
                    if topic and "topic" not in payload:
                        payload["topic"] = topic
                    if tags_json:
                        tags = json.loads(tags_json)
                        if tags and "tags" not in payload:
                            payload["tags"] = tags
                    result.append({
                        "id": id_,
                        "payload": payload,
                        "retry_count": retry,
                    })
                return result

    def ack(self, ids: List[int]) -> None:
        """确认发送成功，删除对应记录。"""
        if not ids:
            return
        with self._lock:
            with sqlite3.connect(str(self.db_path), check_same_thread=False) as conn:
                placeholders = ",".join("?" * len(ids))
                conn.execute(f"DELETE FROM clipboard_queue WHERE id IN ({placeholders})", ids)
                conn.commit()

    def nack(self, ids: List[int]) -> None:
        """发送失败，增加重试计数；超过 max_retry 则丢弃。"""
        if not ids:
            return
        with self._lock:
            with sqlite3.connect(str(self.db_path), check_same_thread=False) as conn:
                conn.execute(
                    f"UPDATE clipboard_queue SET retry_count = retry_count + 1 WHERE id IN ({','.join('?' * len(ids))})",
                    ids,
                )
                conn.execute(
                    f"DELETE FROM clipboard_queue WHERE id IN ({','.join('?' * len(ids))}) AND retry_count > ?",
                    ids + [self.max_retry],
                )
                conn.commit()

    def size(self) -> int:
        with self._lock:
            with sqlite3.connect(str(self.db_path), check_same_thread=False) as conn:
                cur = conn.execute("SELECT COUNT(*) FROM clipboard_queue")
                return cur.fetchone()[0]

    def clear(self) -> int:
        """清空队列，返回删除数量。"""
        with self._lock:
            with sqlite3.connect(str(self.db_path), check_same_thread=False) as conn:
                cur = conn.execute("DELETE FROM clipboard_queue")
                conn.commit()
                return cur.rowcount
