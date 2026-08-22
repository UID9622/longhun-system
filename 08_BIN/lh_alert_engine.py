#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 告警引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-ALERT-ENGINE-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
功能: 多渠道告警推送（Bark主力 + 飞书备用 + 钉钉可选 + 邮件兜底）
用法:
  lh 告警 --send "标题" "内容" [--level info|warn|error]
  lh 告警 --config          查看当前配置
  lh 告警 --test            测试所有通道
联动: lh_health_check.py（告警触发源）/ lh_engine_verify.py（状态数据源）
"""

import os
import sys
import json
import time
import hashlib
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Optional

# ── 配置路径 ──
CONFIG_DIR = Path.home() / ".longhun" / "config"
CONFIG_FILE = CONFIG_DIR / "alert_config.json"
DEDUP_DIR = Path.home() / ".longhun" / "alert_dedup"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
DEDUP_DIR.mkdir(parents=True, exist_ok=True)

# ── 默认配置 ──
DEFAULT_CONFIG: Dict = {
    "bark_key": os.environ.get("BARK_KEY", ""),
    "bark_server": os.environ.get("BARK_SERVER", ""),  # 自建Bark服务
    "feishu_webhook": os.environ.get("FEISHU_WEBHOOK", ""),
    "dingtalk_webhook": os.environ.get("DINGTALK_WEBHOOK", ""),
    "email": {
        "smtp_server": os.environ.get("SMTP_SERVER", ""),
        "smtp_port": int(os.environ.get("SMTP_PORT", "587")),
        "smtp_user": os.environ.get("SMTP_USER", ""),
        "smtp_password": os.environ.get("SMTP_PASSWORD", ""),
        "to": os.environ.get("ALERT_EMAIL", ""),
    },
    "dedup_minutes": 30,
    "max_retries": 2,
}

# ── 告警级别映射 ──
LEVEL_SYMBOLS = {"info": "🟢", "warn": "🟡", "error": "🔴", "critical": "⚫"}


def load_config() -> Dict:
    """加载配置（文件+环境变量合并）"""
    cfg = DEFAULT_CONFIG.copy()
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                saved = json.load(f)
            # 深度合并
            for k, v in saved.items():
                if k == "email" and isinstance(v, dict):
                    cfg["email"] = {**cfg["email"], **v}
                else:
                    cfg[k] = v
        except (json.JSONDecodeError, IOError):
            pass
    return cfg


def save_config(cfg: Dict):
    """保存配置到文件"""
    # 不保存敏感字段的默认值
    clean = {k: v for k, v in cfg.items() if v and v != DEFAULT_CONFIG.get(k)}
    with open(CONFIG_FILE, "w") as f:
        json.dump(clean, f, indent=2, ensure_ascii=False)


# ── 去重检查 ──
def is_duplicate(alert_key: str, dedup_minutes: int) -> bool:
    """检查告警是否在去重窗口内已发送"""
    h = hashlib.md5(alert_key.encode()).hexdigest()
    dedup_file = DEDUP_DIR / h
    if dedup_file.exists():
        try:
            last_ts = float(dedup_file.read_text().strip())
            elapsed = (time.time() - last_ts) / 60
            if elapsed < dedup_minutes:
                return True
        except (ValueError, IOError):
            pass
    return False


def mark_sent(alert_key: str):
    """标记告警已发送"""
    h = hashlib.md5(alert_key.encode()).hexdigest()
    (DEDUP_DIR / h).write_text(str(time.time()))


# ═══════════════════════════════════════════════════
#  渠道发送函数
# ═══════════════════════════════════════════════════

def send_bark(title: str, body: str, config: Dict) -> bool:
    """Bark推送（主力通道）"""
    bark_server = config.get("bark_server", "")
    bark_key = config.get("bark_key", "")

    if not bark_server and (not bark_key or bark_key == "xxxxxxxxxxxxxxxx"):
        return False

    try:
        # 自建模式
        if bark_server:
            url = f"{bark_server}/push"
            payload = json.dumps({
                "title": title,
                "body": body,
                "group": "龍魂系统",
                "sound": "alarm",
                "autoCopy": 1,
            }).encode("utf-8")
            req = urllib.request.Request(url, data=payload, method="POST",
                                          headers={"Content-Type": "application/json"})
        else:
            # 官方Bark API
            url = f"https://api.day.app/{bark_key}/{urllib.request.quote(title)}/{urllib.request.quote(body)}?sound=alarm"
            req = urllib.request.Request(url, method="GET")

        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception:
        return False


def send_feishu(title: str, body: str, webhook: str) -> bool:
    """飞书卡片推送（备用通道）"""
    if not webhook:
        return False
    try:
        payload = json.dumps({
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {"tag": "plain_text", "content": title},
                    "template": "red" if "🔴" in title else "yellow"
                },
                "elements": [
                    {"tag": "markdown", "content": body}
                ]
            }
        }).encode("utf-8")
        req = urllib.request.Request(webhook, data=payload, method="POST",
                                      headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception:
        return False


def send_dingtalk(title: str, body: str, webhook: str) -> bool:
    """钉钉Markdown推送"""
    if not webhook:
        return False
    try:
        payload = json.dumps({
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": f"### {title}\n\n{body}\n\n---\n🐉 龍魂系统 · {time.strftime('%Y-%m-%d %H:%M:%S')}"
            }
        }).encode("utf-8")
        req = urllib.request.Request(webhook, data=payload, method="POST",
                                      headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception:
        return False


def send_email(title: str, body: str, email_config: Dict) -> bool:
    """邮件推送（兜底通道）"""
    if not email_config.get("smtp_user") or not email_config.get("to"):
        return False
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.header import Header

        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = Header(title, "utf-8")
        msg["From"] = email_config["smtp_user"]
        msg["To"] = email_config["to"]

        server = smtplib.SMTP(email_config["smtp_server"], email_config["smtp_port"], timeout=10)
        server.starttls()
        server.login(email_config["smtp_user"], email_config["smtp_password"])
        server.sendmail(email_config["smtp_user"], [email_config["to"]], msg.as_string())
        server.quit()
        return True
    except Exception:
        return False


# ═══════════════════════════════════════════════════
#  主发送逻辑
# ═══════════════════════════════════════════════════

def send_alert(title: str, body: str, level: str = "info",
               skip_dedup: bool = False) -> List[str]:
    """
    多渠道发送告警。
    返回成功发送的通道名列表。
    """
    cfg = load_config()
    dedup_minutes = cfg.get("dedup_minutes", 30)

    # 去重检查
    alert_key = f"{level}|{title}"
    if not skip_dedup and is_duplicate(alert_key, dedup_minutes):
        return ["dedup-skipped"]

    sent = []
    max_retries = cfg.get("max_retries", 2)

    # 通道优先级: Bark > 飞书 > 钉钉 > 邮件
    channels = [
        ("Bark",     lambda: send_bark(title, body, cfg)),
        ("飞书",     lambda: send_feishu(title, body, cfg.get("feishu_webhook", ""))),
        ("钉钉",     lambda: send_dingtalk(title, body, cfg.get("dingtalk_webhook", ""))),
        ("Email",    lambda: send_email(title, body, cfg.get("email", {}))),
    ]

    for ch_name, send_func in channels:
        for attempt in range(max_retries):
            try:
                if send_func():
                    sent.append(ch_name)
                    break
                if attempt < max_retries - 1:
                    time.sleep(1)
            except Exception:
                if attempt < max_retries - 1:
                    time.sleep(1)

    if sent and "dedup-skipped" not in sent:
        mark_sent(alert_key)

    return sent


def test_all_channels():
    """测试所有已配置的通道"""
    cfg = load_config()
    print("🧪 告警通道连通性测试")
    print("=" * 50)

    tests = [
        ("Bark",   lambda: send_bark("🐉 龍魂·告警测试", "这是一条测试消息", cfg),
         bool(cfg.get("bark_key") or cfg.get("bark_server"))),
        ("飞书",   lambda: send_feishu("🐉 龍魂·告警测试", "这是一条测试消息", cfg.get("feishu_webhook", "")),
         bool(cfg.get("feishu_webhook"))),
        ("钉钉",   lambda: send_dingtalk("🐉 龍魂·告警测试", "这是一条测试消息", cfg.get("dingtalk_webhook", "")),
         bool(cfg.get("dingtalk_webhook"))),
        ("Email",  lambda: send_email("🐉 龍魂·告警测试", "这是一条测试消息", cfg.get("email", {})),
         bool(cfg.get("email", {}).get("smtp_user"))),
    ]

    for name, func, configured in tests:
        if not configured:
            print(f"  ⬜ {name}: 未配置（跳过）")
            continue
        try:
            ok = func()
            print(f"  {'✅' if ok else '🔴'} {name}: {'发送成功' if ok else '发送失败'}")
        except Exception as e:
            print(f"  🔴 {name}: 异常 - {e}")

    print("=" * 50)


# ═══════════════════════════════════════════════════
#  CLI入口
# ═══════════════════════════════════════════════════

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="🐉 龍魂·告警引擎 — 多渠道告警推送",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh 告警 --send "服务异常" "审计引擎无响应" --level error
  lh 告警 --config
  lh 告警 --test
  lh 告警 --set bark_key=your_key_here
        """
    )
    parser.add_argument("--send", nargs=2, metavar=("TITLE", "BODY"),
                        help="发送告警")
    parser.add_argument("--level", default="info",
                        choices=["info", "warn", "error", "critical"],
                        help="告警级别 (默认: info)")
    parser.add_argument("--config", action="store_true",
                        help="查看当前配置")
    parser.add_argument("--set", nargs="*", metavar="KEY=VALUE",
                        help="设置配置项 (如 bark_key=xxx)")
    parser.add_argument("--test", action="store_true",
                        help="测试所有已配置通道")
    parser.add_argument("--force", action="store_true",
                        help="跳过去重强制发送")

    args = parser.parse_args()

    if args.test:
        test_all_channels()
        return

    if args.config:
        cfg = load_config()
        # 脱敏显示
        safe = {}
        for k, v in cfg.items():
            if k in ("email",):
                safe[k] = {ek: ("***" if "password" in ek.lower() else ev)
                           for ek, ev in v.items()}
            elif "key" in k.lower() or "password" in k.lower() or "webhook" in k.lower():
                safe[k] = v[:8] + "***" if v else "(未设置)"
            else:
                safe[k] = v
        print(json.dumps(safe, indent=2, ensure_ascii=False))
        return

    if args.set:
        cfg = load_config()
        for item in args.set:
            if "=" not in item:
                print(f"⚠️ 忽略无效格式: {item} (需 KEY=VALUE)")
                continue
            k, v = item.split("=", 1)
            cfg[k] = v
        save_config(cfg)
        print("✅ 配置已更新")
        return

    if args.send:
        title, body = args.send
        sent = send_alert(title, body, args.level, skip_dedup=args.force)
        if sent:
            if "dedup-skipped" in sent:
                print("🟡 告警已被去重（短时间内已发送过），跳过")
            else:
                symbol = LEVEL_SYMBOLS.get(args.level, "🟢")
                print(f"{symbol} 告警已发送: {', '.join(sent)}")
        else:
            print("🔴 告警发送失败：无可用通道")
            print("   请配置 Bark Key: lh 告警 --set bark_key=your_key")
            print("   或飞书 Webhook: lh 告警 --set feishu_webhook=https://...")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
