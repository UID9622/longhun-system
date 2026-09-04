#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·乙亥·巳时·䷝离-EXAMPLE-DEMO-PY-v1.0
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: AGPL-3.0-or-later
"""
🐉 longhun-cli 标准调用示例 — flow / health / bazi

用法:
  python3 examples/demo.py              # 模块内嵌调用（pip install longhun-cli 后）
  python3 examples/demo.py --cli        # 命令行调用（调用 lh 命令）
  python3 examples/demo.py --gateway    # HTTP 网关调用（需先起 lh api --daemon）
"""

import argparse
import json
import subprocess
import sys
import urllib.request

try:
    from longhun_cli.core import bazi, flow, health_basic

    HAS_MODULE = True
except ImportError:
    HAS_MODULE = False
    # 开发模式: 直接从源码目录导入
    sys.path.insert(0, "packaging/longhun_cli")
    try:
        from longhun_cli.core import bazi, flow, health_basic

        HAS_MODULE = True
    except ImportError:
        pass


def show(title: str, data: dict) -> None:
    """标准输出: 标题 + 可解析 JSON。"""
    print(f"\n=== {title} ===")
    print(json.dumps(data, ensure_ascii=False, indent=2))


def demo_module() -> None:
    """形态一: Python 模块内嵌（推荐·零依赖）。"""
    if not HAS_MODULE:
        sys.exit("❌ 未找到 longhun_cli 模块，请先 pip install longhun-cli 或到 packaging/longhun_cli 目录运行")
    show("flow · 流场计算", flow("龙魂对外首发"))
    show("health · 基础自检", health_basic())
    show("bazi · 八字排盘", bazi("1990-01-01", "08:00"))


def run_lh(args: list[str]) -> dict:
    """执行 lh 命令并解析 Node JSON。"""
    proc = subprocess.run(["lh", *args], capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(f"❌ lh {' '.join(args)} 失败 ({proc.returncode}): {proc.stderr}")
    return json.loads(proc.stdout)


def demo_cli() -> None:
    """形态二: 命令行调用。"""
    show("flow · 流场计算", run_lh(["flow", "龙魂对外首发", "--json"]))
    show("health · 基础自检", run_lh(["health", "--json"]))
    show("bazi · 八字排盘", run_lh(["bazi", "--date", "1990-01-01", "--time", "08:00", "--json"]))


def gateway_call(command: str, host: str = "127.0.0.1", port: int = 9622) -> dict:
    """形态三: HTTP 网关调用（标准库 urllib·零依赖）。"""
    req = urllib.request.Request(
        f"http://{host}:{port}/v1/lh",
        data=json.dumps({"command": command}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        body = json.loads(resp.read().decode())
    if body["result"]["code"] != 0:
        sys.exit(f"❌ 网关执行失败: {body['result']['stderr']}")
    return json.loads(body["result"]["stdout"])


def demo_gateway() -> None:
    """形态三: HTTP 网关调用（需先 lh api --daemon）。"""
    show("flow · 流场计算", gateway_call("flow 龙魂对外首发 --json"))
    show("health · 基础自检", gateway_call("health --json"))
    show("bazi · 八字排盘", gateway_call("bazi --date 1990-01-01 --time 08:00 --json"))


def main() -> None:
    ap = argparse.ArgumentParser(description="longhun-cli 标准调用示例")
    ap.add_argument("--cli", action="store_true", help="命令行调用形态")
    ap.add_argument("--gateway", action="store_true", help="HTTP 网关调用形态（需 lh api --daemon）")
    args = ap.parse_args()

    if args.cli:
        demo_cli()
    elif args.gateway:
        demo_gateway()
    else:
        demo_module()
    print("\n✅ 演示完成 · 全部输出为可解析 Node JSON")


if __name__ == "__main__":
    main()
