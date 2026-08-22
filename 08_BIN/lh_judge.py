#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
⚖️ 龍魂·公正总裁 / 首席审计员 · 本地 CLI
DNA: #龍芯⚡️丙午·乙未·甲辰·庚午·䷔噬-JUDGE-CLI-v1.0

调用鲲鹏上的 longhun-judge API 服务。
默认 API: https://uid9622.cn/api/judge

用法:
  lh judge --content "有人说只有他能教某技术"
  lh judge --audit "某管理员试图删除审计记录"
  lh judge --health
"""

import argparse
import json
import urllib.request

API_BASE = "https://uid9622.cn/api/judge"


def call_api(endpoint: str, payload: dict):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        f"{API_BASE}{endpoint}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    global API_BASE
    parser = argparse.ArgumentParser(description="龍魂·公正总裁 CLI")
    parser.add_argument("--content", "-c", type=str, help="裁决/审计内容")
    parser.add_argument("--audit", "-a", action="store_true", help="以审计员身份处理")
    parser.add_argument("--judge", "-j", action="store_true", help="以总裁身份裁决（默认）")
    parser.add_argument("--health", action="store_true", help="检查 API 健康状态")
    parser.add_argument("--api", type=str, default=API_BASE, help="自定义 API 地址")
    args = parser.parse_args()

    API_BASE = args.api

    if args.health:
        req = urllib.request.Request(f"{API_BASE}/health", method="GET")
        with urllib.request.urlopen(req, timeout=60) as resp:
            print(json.dumps(json.loads(resp.read().decode("utf-8")), ensure_ascii=False, indent=2))
        return

    if not args.content:
        parser.print_help()
        return

    endpoint = "/audit" if args.audit else "/judge"
    result = call_api(endpoint, {"content": args.content})
    print(result.get("output", result))
    print(f"\n🧬 {result.get('dna', '')}")


if __name__ == "__main__":
    main()
