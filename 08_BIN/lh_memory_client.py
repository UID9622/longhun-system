#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-MEMORY-CLIENT-v1.1-SECURE
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# 职能: AI 记忆加载客户端 — 任何 AI 启动时调用此脚本加载记忆
"""
龍魂·AI 记忆加载客户端 v1.1

用途: 所有 AI 会话启动时调用，从统一记忆 API 加载记忆。
      支持本地/远程两种模式。

安全: Token 从以下来源静默加载（优先级从高到低）:
  1. 环境变量 $LH_MEMORY_TOKEN（推荐）
  2. ~/.longhun/.memory_token 文件
  3. 项目内 .codebuddy/memory/.api_token 文件
  🔴 禁止在命令行明文出示 Token

用法:
  # 本机 AI（默认 127.0.0.1:8771，无需 Token）
  python3 bin/lh_memory_client.py

  # 远程 AI（Token 从环境变量读取）
  export LH_MEMORY_TOKEN="<your_token>"
  python3 bin/lh_memory_client.py --host 119.13.90.27 --port 8773

  # 只输出身份焊死块
  python3 bin/lh_memory_client.py --identity

  # 搜索记忆
  python3 bin/lh_memory_client.py --search "训练"

  # 输出原始 markdown（适合注入 AI 上下文）
  python3 bin/lh_memory_client.py --raw

  # JSON 输出（机器可读）
  python3 bin/lh_memory_client.py --json
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

# 默认 API 地址
DEFAULT_HOST = os.environ.get("LH_MEMORY_HOST", "127.0.0.1")
DEFAULT_PORT = int(os.environ.get("LH_MEMORY_PORT", "8771"))
DEFAULT_TOKEN = os.environ.get("LH_MEMORY_TOKEN", "")

# 🔥 v1.1 Token 加载链（优先级递减）:
#   1. $LH_MEMORY_TOKEN 环境变量
#   2. ~/.longhun/.memory_token 文件
#   3. .codebuddy/memory/.api_token 项目文件
MEMORY_TOKEN_PATH = os.path.expanduser("~/.longhun/.memory_token")
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TOKEN_FILE = PROJECT_ROOT / ".codebuddy" / "memory" / ".api_token"

# 按优先级静默加载
if not DEFAULT_TOKEN:
    try:
        if os.path.exists(MEMORY_TOKEN_PATH):
            with open(MEMORY_TOKEN_PATH, "r") as f:
                DEFAULT_TOKEN = f.read().strip()
    except Exception:
        pass

if not DEFAULT_TOKEN and TOKEN_FILE.exists():
    DEFAULT_TOKEN = TOKEN_FILE.read_text().strip()


def api_get(host: str, port: int, path: str, token: str = "") -> dict:
    """调用记忆 API"""
    url = f"http://{host}:{port}{path}"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "LongHun-Memory-Client/1.0")
    req.add_header("Accept", "application/json")
    if token:
        req.add_header("X-API-Token", token)

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            content_type = resp.headers.get("Content-Type", "")
            data = resp.read().decode("utf-8")
            if "application/json" in content_type:
                return json.loads(data)
            else:
                return {"raw": data, "content_type": content_type}
    except urllib.error.HTTPError as e:
        print(f"🔴 API 错误: {e.code} - {e.reason}", file=sys.stderr)
        body = e.read().decode("utf-8", errors="replace")
        print(f"   响应: {body[:500]}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"🔴 连接失败: {e.reason}", file=sys.stderr)
        print(f"   请确认记忆 API 已启动: python3 bin/lh_memory_api.py", file=sys.stderr)
        sys.exit(1)


def format_sections(data: dict) -> str:
    """格式化输出记忆节 — AI 友好"""
    sections = data.get("sections", {})
    if not sections:
        return "🟡 无记忆数据"

    lines = []
    lines.append("=" * 60)
    lines.append(f"🐉 龍魂统一记忆 · v{data.get('version', '?')} · {len(sections)} 节")
    lines.append(f"   DNA: {data.get('dna', '')}")
    lines.append(f"   加载时间: {data.get('loaded_at', '')}")
    lines.append("=" * 60)

    # 按节号排序
    def sort_key(k):
        try:
            return int(k.lstrip("§").split(".")[0])
        except ValueError:
            return 99

    for sec_name in sorted(sections.keys(), key=sort_key):
        content = sections[sec_name]
        # 取前10行作为摘要
        content_lines = content.split("\n")
        preview = "\n".join(content_lines[:10])
        if len(content_lines) > 10:
            preview += f"\n   ... (共 {len(content_lines)} 行)"
        lines.append(f"\n{'─' * 40}")
        lines.append(f"  {sec_name}")
        lines.append(f"{'─' * 40}")
        lines.append(preview)

    lines.append(f"\n{'=' * 60}")
    lines.append("🐉 记忆加载完毕。本会话以上述记忆为准。")
    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="龍魂·AI 记忆加载客户端 — 所有 AI 统一入口",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_memory_client.py                    # 加载完整记忆
  python3 bin/lh_memory_client.py --identity         # 只输出身份块
  python3 bin/lh_memory_client.py --search "训练超参"  # 搜索
  python3 bin/lh_memory_client.py --raw              # 原始 markdown
  python3 bin/lh_memory_client.py --json             # JSON 输出
  python3 bin/lh_memory_client.py --host 119.13.90.27 --port 8770 --token xxx  # 远程
        """
    )
    parser.add_argument("--host", default=DEFAULT_HOST, help=f"API 主机 (默认: {DEFAULT_HOST})")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"API 端口 (默认: {DEFAULT_PORT})")
    parser.add_argument("--token", default="", help="API Token (优先用 $LH_MEMORY_TOKEN 环境变量，禁止在脚本/日志中明文出示)")
    parser.add_argument("--identity", action="store_true", help="只输出身份焊死块")
    parser.add_argument("--search", type=str, default="", help="搜索关键词")
    parser.add_argument("--section", type=str, default="", help="获取指定节 (如 §1, 4)")
    parser.add_argument("--raw", action="store_true", help="输出原始 MEMORY.md")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    parser.add_argument("--health", action="store_true", help="健康检查")
    parser.add_argument("--anchors", action="store_true", help="获取锚清单")

    args = parser.parse_args()

    # 自动获取 token（优先级: 环境变量/文件/命令行）
    token = args.token or DEFAULT_TOKEN or ""

    # 路由到对应端点
    try:
        if args.health:
            data = api_get(args.host, args.port, "/v1/memory/health", token)
            print(json.dumps(data, ensure_ascii=False, indent=2) if args.json else json.dumps(data, ensure_ascii=False))

        elif args.identity:
            data = api_get(args.host, args.port, "/v1/memory/identity", token)
            if args.json:
                print(json.dumps(data, ensure_ascii=False, indent=2))
            else:
                print("=" * 60)
                print("🔥 龍魂·身份焊死块")
                print("=" * 60)
                for key, val in data.items():
                    if key not in ("raw",):
                        print(f"  {key}: {val}")
                print("=" * 60)

        elif args.search:
            data = api_get(args.host, args.port, f"/v1/memory/search?q={args.search}", token)
            if args.json:
                print(json.dumps(data, ensure_ascii=False, indent=2))
            else:
                print(f"\n🔍 搜索: '{args.search}' — {data.get('total_hits', 0)} 条结果\n")
                for r in data.get("results", []):
                    print(f"  [{r['section']}] L{r['line_num']}: {r['match_line']}")
                print()

        elif args.section:
            data = api_get(args.host, args.port, f"/v1/memory/section/{args.section}", token)
            print(data.get("content", str(data)))

        elif args.raw:
            data = api_get(args.host, args.port, "/v1/memory/raw", token)
            raw = data.get("raw", str(data))
            print(raw)

        elif args.anchors:
            data = api_get(args.host, args.port, "/v1/memory/anchors", token)
            print(data.get("content", str(data)))

        elif args.json:
            data = api_get(args.host, args.port, "/v1/memory", token)
            print(json.dumps(data, ensure_ascii=False, indent=2))

        else:
            # 默认：加载完整记忆·格式化输出
            data = api_get(args.host, args.port, "/v1/memory", token)
            output = format_sections(data)
            print(output)

    except KeyboardInterrupt:
        print("\n中断")
        sys.exit(0)
    except Exception as e:
        print(f"🔴 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
