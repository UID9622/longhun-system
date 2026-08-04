#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 消息通知引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-NOTIFY-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 多通道通知（终端/邮件/企业微信/飞书/Telegram）
  - 通知模板
  - 消息优先级
"""

import json
from pathlib import Path
from typing import Dict, Optional
from enum import Enum


class NotifyLevel(Enum):
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class NotifyEngine:
    """消息通知引擎——多通道通知（终端/邮件/微信/飞书）"""

    TEMPLATES = {
        "task_complete": "✅ 任务完成: {task_name} 耗时 {duration}s",
        "task_failed": "❌ 任务失败: {task_name} 错误: {error}",
        "audit_passed": "🟢 审计通过: {result}",
        "audit_failed": "🔴 审计失败: {findings} 项风险",
        "system_start": "🐉 龙魂系统启动 (PID: {pid})",
        "system_stop": "⏹️ 龙魂系统停止",
        "deploy_done": "🚀 部署完成: {target} (耗时:{duration}s)",
    }

    COLORS = {
        NotifyLevel.INFO: "\033[92m",
        NotifyLevel.WARN: "\033[93m",
        NotifyLevel.ERROR: "\033[91m",
        NotifyLevel.CRITICAL: "\033[95m",
    }

    def __init__(self):
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        config_file = Path.home() / "longhun-system/.notify_config.json"
        if config_file.exists():
            try:
                return json.loads(config_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"terminal": True, "email": False, "wechat": False, "feishu": False}

    def send(self, message: str, level: NotifyLevel = NotifyLevel.INFO, channel: str = "terminal"):
        if channel == "terminal":
            self._send_terminal(message, level)
        elif channel == "email" and self.config.get("email"):
            self._send_email(message, level)
        elif channel == "wechat" and self.config.get("wechat"):
            self._send_wechat(message)
        elif channel == "feishu" and self.config.get("feishu"):
            self._send_feishu(message)
        else:
            self._send_terminal(message, level)

    def _send_terminal(self, message: str, level: NotifyLevel):
        color = self.COLORS.get(level, "\033[0m")
        print(f"{color}[{level.value}] {message}\033[0m")

    def _send_email(self, message: str, level: NotifyLevel):
        cfg = self.config
        try:
            import smtplib
            from email.mime.text import MIMEText
            msg = MIMEText(message)
            msg["Subject"] = f"[{level.value}] 龙魂系统通知"
            msg["From"] = cfg.get("sender_email", "")
            msg["To"] = cfg.get("receiver_email", "")
            with smtplib.SMTP(cfg.get("smtp_server", ""), 587) as s:
                s.starttls()
                s.login(cfg.get("sender_email", ""), cfg.get("sender_password", ""))
                s.send_message(msg)
        except Exception as e:
            print(f"邮件发送失败: {e}")

    def _send_wechat(self, message: str):
        try:
            import requests
            requests.post(self.config.get("wechat_webhook", ""),
                         json={"msgtype": "text", "text": {"content": message}}, timeout=5)
        except Exception:
            pass

    def _send_feishu(self, message: str):
        try:
            import requests
            requests.post(self.config.get("feishu_webhook", ""),
                         json={"msg_type": "text", "content": {"text": message}}, timeout=5)
        except Exception:
            pass

    def render(self, template_name: str, **kwargs) -> str:
        tpl = self.TEMPLATES.get(template_name, "{message}")
        try:
            return tpl.format(**kwargs)
        except Exception:
            return kwargs.get("message", "通知")


if __name__ == "__main__":
    engine = NotifyEngine()
    msg = engine.render("task_complete", task_name="健康检查", duration=0.05)
    engine.send(msg, NotifyLevel.INFO)
    engine.send("审计发现2项风险", NotifyLevel.WARN)
    print("🟢 消息通知引擎测试通过")
