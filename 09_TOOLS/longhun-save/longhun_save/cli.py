#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·乙未·壬子·丙午·䷙大畜-SAVE-CLI-v1.0
# License: MulanPSL v2
"""longhun-save CLI 工具"""

import argparse
import json
import os
import subprocess
import sys
from .proxy import SaveProxy
from .router import RouteStrategy


def main():
    p = argparse.ArgumentParser(
        description="龍魂算力省钱代理 · AI API 智能路由",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  longhun-save start --port 8088
  longhun-save start --local http://localhost:11434/v1 qwen2.5:7b
  longhun-save start --cloud https://api.deepseek.com/v1 deepseek-v4-flash --key sk-xxx
  longhun-save stat --port 8088
  longhun-save test
        """
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    # start
    s = sub.add_parser("start", help="启动代理服务器")
    s.add_argument("--port", "-p", type=int, default=8088, help="监听端口")
    s.add_argument("--host", default="127.0.0.1", help="监听地址")
    s.add_argument("--local", nargs=2, action="append", default=[],
                   metavar=("URL", "MODEL"), help="添加本地模型（可多次）")
    s.add_argument("--cloud", nargs=2, action="append", default=[],
                   metavar=("URL", "MODEL"), help="添加云端模型（可多次）")
    s.add_argument("--key", "-k", action="append", default=[],
                   help="云端 API Key（与 --cloud 一一对应）")
    s.add_argument("--strategy", choices=["local_first", "local_only", "cloud_only", "smart"],
                   default="local_first", help="路由策略")
    s.add_argument("--cache-ttl", type=int, default=3600, help="缓存有效期（秒）")

    # stat
    st = sub.add_parser("stat", help="查看代理统计")
    st.add_argument("--port", "-p", type=int, default=8088, help="代理端口")

    # test
    sub.add_parser("test", help="运行自检")

    args = p.parse_args()

    if args.cmd == "test":
        print("🧪 运行自检...")
        tests = ["longhun_save.cache_engine", "longhun_save.stats", "longhun_save.proxy"]
        for t in tests:
            result = subprocess.run([sys.executable, "-m", t], capture_output=True, text=True,
                                    cwd=os.path.dirname(os.path.dirname(__file__)))
            print(result.stdout[-200:] if len(result.stdout) > 200 else result.stdout)
            if result.returncode != 0:
                print(result.stderr)
                sys.exit(1)
        print("🟢🟢🟢 全部自检通过")
        return

    if args.cmd == "stat":
        import httpx
        try:
            r = httpx.get(f"http://127.0.0.1:{args.port}/stats", timeout=5)
            r.raise_for_status()
            print(json.dumps(r.json(), ensure_ascii=False, indent=2))
        except Exception as e:
            print(f"🔴 无法连接代理 (127.0.0.1:{args.port}): {e}")
            sys.exit(1)
        return

    if args.cmd == "start":
        strategy_map = {
            "local_first": RouteStrategy.LOCAL_FIRST,
            "local_only": RouteStrategy.LOCAL_ONLY,
            "cloud_only": RouteStrategy.CLOUD_ONLY,
            "smart": RouteStrategy.SMART,
        }
        strategy = strategy_map.get(args.strategy, RouteStrategy.LOCAL_FIRST)

        proxy = SaveProxy(strategy=strategy, cache_ttl=args.cache_ttl)

        # 自动检测本地 Ollama
        auto_ollama = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        proxy.add_local(f"{auto_ollama}/v1", "qwen2.5:7b", name="auto:ollama")

        # 用户指定本地模型
        for url, model in args.local:
            proxy.add_local(url, model)

        # 用户指定云端模型
        for i, (url, model) in enumerate(args.cloud):
            api_key = args.key[i] if i < len(args.key) else ""
            proxy.add_cloud(url, model, api_key)

        proxy.start(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
