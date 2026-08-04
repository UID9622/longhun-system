#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·中孚-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║   🐉 龙魂·Bark 推送工具 v2.0 — 自建/官方双模式                            ║
║   Bark Send Tool · 仅发送 · 不审计不存储                                   ║
╠══════════════════════════════════════════════════════════════════════════╣
║   用途: 服务器cron脚本调用，仅做Bark HTTP推送                               ║
║   审计/存储由本地 lh_bark_dispatcher.py 完成                               ║
║   双模式: 设置 BARK_SERVER=http://IP:8080 使用自建，否则走官方 api.day.app   ║
╚══════════════════════════════════════════════════════════════════════════╝

用法:
    python3 executors/bark/bark_send.py "标题" "内容"
    echo "内容" | python3 executors/bark/bark_send.py "标题" --stdin

环境变量:
    BARK_KEY           — iOS设备Key (必须)
    BARK_SERVER        — 自建Bark服务器地址，如 http://华为云IP:8080
                         不设置则走官方 api.day.app
"""

import json
import os
import sys
import urllib.request

BARK_KEY = os.environ.get("BARK_KEY", "")
BARK_SERVER = os.environ.get("BARK_SERVER", "")

# 根据 BARK_SERVER 决定推送目标
if BARK_SERVER:
    BARK_URL = f"{BARK_SERVER}/push"  # 自建服务器 POST /push
else:
    BARK_URL = f"https://api.day.app/{BARK_KEY}"  # 官方 API


def send_bark(title: str, body: str, group: str = "龙魂系统", level: str = "info") -> bool:
    """发送Bark推送 · 自动适配自建/官方模式"""
    if not BARK_KEY and not BARK_SERVER:
        print("Error: BARK_KEY 或 BARK_SERVER 未配置", file=sys.stderr)
        return False

    if len(body) > 4000:
        body = body[:3900] + "\n\n... (截断)"

    payload_dict = {
        "title": title,
        "body": body,
        "group": group,
        "sound": "alarm",
        "autoCopy": True,
    }

    # 自建服务器支持更多字段
    if BARK_SERVER:
        payload_dict["level"] = level
        payload_dict["badge"] = 1

    payload = json.dumps(payload_dict, ensure_ascii=False).encode("utf-8")

    try:
        req = urllib.request.Request(
            BARK_URL,
            data=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("code") == 200
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return False


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Bark推送工具")
    parser.add_argument("title", help="推送标题")
    parser.add_argument("body", nargs="?", default="", help="推送内容")
    parser.add_argument("--stdin", action="store_true", help="从stdin读取内容")
    parser.add_argument("--group", default="龙魂系统", help="推送分组")
    args = parser.parse_args()

    body = args.body
    if args.stdin:
        stdin_content = sys.stdin.read().strip()
        if stdin_content:
            body = stdin_content

    if not body:
        print("Error: 需要推送内容", file=sys.stderr)
        sys.exit(1)

    success = send_bark(args.title, body, args.group)
    if success:
        print("✅ Bark推送成功")
    else:
        print("❌ Bark推送失败", file=sys.stderr)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
