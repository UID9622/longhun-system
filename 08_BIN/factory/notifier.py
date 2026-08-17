#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-FACTORY-NOTIFIER-UID9622
# 创建者: 诸葛鑫（UID9622）
"""
🐉 龍魂 · 通知告警 v1.0（v2.0 补全区块）
功能: 日志 / 文件 / Bark推送 / 飞书Webhook 多通道通知
安全: 敏感字段不落日志（自动 MELTDOWN），Bark Key 从环境变量读，不硬编码
"""

import json
import logging
import os
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from .generate_dna import generate_dna

# 敏感字段自动脱敏（五层黑洞 L4: 日志敏感字段 → ***MELTDOWN***）
SENSITIVE_KEYS = ["password", "token", "key", "secret", "private", "auth"]


def meltdown(data: Dict) -> Dict:
    """敏感字段脱敏"""
    cleaned = {}
    for k, v in data.items():
        if any(s in k.lower() for s in SENSITIVE_KEYS):
            cleaned[k] = "***MELTDOWN***"
        else:
            cleaned[k] = v
    return cleaned


class Notifier:
    """多通道通知器"""

    def __init__(self, log_path: Path = None):
        self.logger = logging.getLogger("longhun-factory")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s %(message)s"))
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        self.log_path = log_path

    def send(self, channel: str, title: str, message: str, level: str = "info",
             extra: Dict = None) -> Dict:
        """发送通知到指定通道"""
        dna = generate_dna("NOTIFY")
        result = {"dna": dna, "channel": channel, "status": "sent",
                  "timestamp": datetime.now().isoformat()}
        extra = meltdown(extra or {})

        try:
            if channel == "log":
                getattr(self.logger, level, self.logger.info)(f"{title}: {message}")
            elif channel == "file" and self.log_path:
                self.log_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self.log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps({"title": title, "message": message, "level": level,
                                        "extra": extra, "dna": dna,
                                        "ts": datetime.now().isoformat()}, ensure_ascii=False) + "\n")
            elif channel == "bark":
                bark_key = os.environ.get("BARK_KEY", "")
                if bark_key:
                    url = f"https://api.day.app/{bark_key}/{urllib.parse.quote(title)}"
                    urllib.request.urlopen(url, timeout=5)
                else:
                    result["status"] = "skipped"
                    result["message"] = "BARK_KEY 未配置，跳过"
            elif channel == "feishu":
                webhook = os.environ.get("FEISHU_WEBHOOK", "")
                if webhook:
                    payload = json.dumps({"msg_type": "text",
                                          "content": {"text": f"{title}\n{message}"}}).encode()
                    req = urllib.request.Request(webhook, data=payload,
                                                 headers={"Content-Type": "application/json"})
                    urllib.request.urlopen(req, timeout=5)
                else:
                    result["status"] = "skipped"
                    result["message"] = "FEISHU_WEBHOOK 未配置，跳过"
            else:
                result["status"] = "unknown_channel"
        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)[:200]

        return result

    def send_all(self, channels: List[str], title: str, message: str, level: str = "info",
                 extra: Dict = None) -> List[Dict]:
        """发送到多个通道"""
        return [self.send(c, title, message, level, extra) for c in channels]
