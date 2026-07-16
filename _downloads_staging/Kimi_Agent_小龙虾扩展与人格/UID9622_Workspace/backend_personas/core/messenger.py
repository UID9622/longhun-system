#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""人格间轻量消息路由，基于本地 JSONL 邮箱。
DNA: #龍芯⚡️2026-06-27-LONGHUN-SYSTEM-CORE-MESSENGER-v1.0
"""
import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


class Messenger:
    def __init__(self, mailbox_dir: Path):
        self.mailbox_dir = Path(mailbox_dir)
        self.inbox = self.mailbox_dir / "inbox.jsonl"
        self.lock = threading.Lock()
        self.mailbox_dir.mkdir(parents=True, exist_ok=True)

    def send(
        self,
        sender: str,
        recipient: str,
        event: str,
        payload: Dict[str, Any],
        require_ack: bool = False,
    ) -> str:
        msg_id = f"MSG-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"
        entry = {
            "id": msg_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sender": sender,
            "recipient": recipient,
            "event": event,
            "payload": payload,
            "ack": False,
        }
        with self.lock:
            with open(self.inbox, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return msg_id

    def recv(self, recipient: str, mark_ack: bool = True) -> List[Dict[str, Any]]:
        if not self.inbox.exists():
            return []
        with self.lock:
            lines = self.inbox.read_text(encoding="utf-8").splitlines()
            matched = []
            updated = []
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                except Exception:
                    continue
                if msg.get("recipient") == recipient and not msg.get("ack", False):
                    matched.append(msg)
                    if mark_ack:
                        msg["ack"] = True
                updated.append(msg)
            if mark_ack and matched:
                self.inbox.write_text(
                    "".join(json.dumps(m, ensure_ascii=False) + "\n" for m in updated),
                    encoding="utf-8",
                )
        return matched

    def broadcast(
        self, sender: str, event: str, payload: Dict[str, Any]
    ) -> str:
        return self.send(sender, "ALL", event, payload)
