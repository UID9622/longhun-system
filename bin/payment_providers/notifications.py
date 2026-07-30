#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-ACTIVATION-NOTIFICATIONS-v1.0
# 功能: 龍魂激活经济舱 · 到账通知（邮件 / 短信预留）

import os
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from pathlib import Path
from typing import Dict, Any
from datetime import datetime


def _load_credentials() -> Dict[str, Any]:
    """加载通知配置"""
    paths = [
        Path(os.path.expanduser("~/.longhun/config/payment_credentials.yaml")),
        Path(__file__).resolve().parents[2] / "config" / "payment_credentials.yaml",
        Path(__file__).resolve().parents[2] / "config" / "payment_credentials.yaml.example",
    ]
    for p in paths:
        if p.exists():
            try:
                import yaml
                with open(p, "r", encoding="utf-8") as f:
                    cfg = yaml.safe_load(f) or {}
                    return cfg.get("notifications", {})
            except Exception:
                pass
    return {}


CREDENTIALS = _load_credentials()


def _log_notify(message: str):
    log_dir = Path(os.path.expanduser("~/.longhun"))
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "notification.log"
    timestamp = datetime.now().isoformat()
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


def notify_payment_confirmed(order: Dict[str, Any]) -> Dict[str, Any]:
    """订单确认到账后触发通知"""
    results = {"email": False, "sms": False, "errors": []}

    # 邮件通知
    email_cfg = CREDENTIALS.get("email", {})
    if email_cfg.get("enabled"):
        try:
            results["email"] = _send_email(order, email_cfg)
        except Exception as e:
            results["errors"].append(f"email: {e}")
            _log_notify(f"邮件通知失败: {e}")

    # 短信通知（预留）
    sms_cfg = CREDENTIALS.get("sms", {})
    if sms_cfg.get("enabled"):
        try:
            results["sms"] = _send_sms(order, sms_cfg)
        except Exception as e:
            results["errors"].append(f"sms: {e}")
            _log_notify(f"短信通知失败: {e}")

    if not email_cfg.get("enabled") and not sms_cfg.get("enabled"):
        _log_notify("通知未启用，跳过")

    return results


def _send_email(order: Dict[str, Any], cfg: Dict[str, Any]) -> bool:
    """发送邮件通知"""
    smtp_host = cfg["smtp_host"]
    smtp_port = int(cfg.get("smtp_port", 465))
    smtp_ssl = bool(cfg.get("smtp_ssl", True))
    username = cfg["username"]
    password = cfg["password"]
    from_addr = cfg.get("from_addr", username)
    to_addr = cfg["to_addr"]
    subject_prefix = cfg.get("subject_prefix", "[龍魂激活舱]")

    subject = f"{subject_prefix} 到账确认 {order['order_id']}"
    body = f"""
龍魂激活经济舱 · 到账通知

订单号: {order['order_id']}
金额: {order['amount']} {order.get('currency', 'CNY')}
支付人: {order.get('name', '匿名')}
交易单号: {order.get('tx_id', '-')}
确认时间: {order.get('confirmed_at', '-')}
DNA: {order.get('dna', '-')}

本邮件由龍魂系统自动发送。
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = Header(from_addr, "utf-8")
    msg["To"] = Header(to_addr, "utf-8")
    msg["Subject"] = Header(subject, "utf-8")

    if smtp_ssl:
        server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=10)
    else:
        server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
        server.starttls()

    server.login(username, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

    _log_notify(f"邮件通知已发送: {to_addr} 订单={order['order_id']}")
    return True


def _send_sms(order: Dict[str, Any], cfg: Dict[str, Any]) -> bool:
    """发送短信通知（预留接口，需接入阿里云/腾讯云短信）"""
    provider = cfg.get("provider", "aliyun")
    to_phone = cfg.get("to_phone", "")
    if not to_phone:
        raise ValueError("未配置接收手机号 to_phone")

    # 这里只记录日志，真实发送需要接入对应 SDK
    _log_notify(
        f"短信通知待发送: {to_phone}  provider={provider} 订单={order['order_id']} "
        f"金额={order['amount']}"
    )
    # TODO: 接入 aliyun-python-sdk-dysmsapi 或 qcloudsms_python
    return True


def test_email() -> Dict[str, Any]:
    """测试邮件配置"""
    email_cfg = CREDENTIALS.get("email", {})
    if not email_cfg.get("enabled"):
        return {"success": False, "error": "邮件通知未启用"}
    try:
        _send_email(
            {
                "order_id": "TEST-00000000-00000000",
                "amount": "1.00",
                "currency": "CNY",
                "name": "测试用户",
                "tx_id": "TEST_TX_ID",
                "confirmed_at": datetime.now().isoformat(),
                "dna": "#龍芯⚡️测试-DNA",
            },
            email_cfg,
        )
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}
