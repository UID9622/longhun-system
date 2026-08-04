#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 业务引擎验证 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-ENGINE-VERIFY-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
功能: 验证所有已注册业务引擎的健康状态（本地端口+SSH鲲鹏端点）
用法: lh 引擎验证 [--json]
联动: lh_unified_console.py / lh_health_check.py / lh_alert_engine.py
"""

import sys
import json
import time
import urllib.request
import urllib.error
import socket
from typing import Dict, List, Optional

# ── 引擎注册表（Mac本地端口 + 鲲鹏远端端点） ──
# 与 COMMAND_INDEX.md 及 lh 端口状态 保持同步
ENGINES: Dict[str, Dict] = {
    # ── Mac 本地端口 ──
    "知识中枢":          {"port": 8766, "path": "/health"},
    "天线八闸":          {"port": 8769, "path": "/health"},
    "审计引擎":          {"port": 8771, "path": "/health"},
    "流场融合桥接":      {"port": 8777, "path": "/health"},
    "记忆服务":          {"port": 8779, "path": "/health"},
    "安全网关":          {"port": 8848, "path": "/health"},
    "主权验证":          {"port": 8799, "path": "/health"},
    "搜索网关":          {"port": 9631, "path": "/health"},
    "Ollama推理":        {"port": 11434, "path": "/api/tags"},
    # ── Mac 可能运行的额外端口 ──
    "天线八闸备用":      {"port": 8770, "path": "/health"},
    "量子卦象":          {"port": 9000, "path": "/health"},
    "量子卦象备用":      {"port": 9001, "path": "/health"},
    "搜索备用":          {"port": 9632, "path": "/health"},
    # ── 鲲鹏远端服务 (SSH隧道可达) ──
    "审计引擎(鲲鹏)":    {"host": "119.13.90.27", "port": 8771, "path": "/health"},
    "流场引擎(鲲鹏)":    {"host": "119.13.90.27", "port": 8776, "path": "/health"},
    "记忆API(鲲鹏)":     {"host": "119.13.90.27", "port": 8773, "path": "/health"},
    "搜索引擎(鲲鹏)":    {"host": "119.13.90.27", "port": 9631, "path": "/health"},
    "天线八闸(鲲鹏)":    {"host": "119.13.90.27", "port": 8769, "path": "/health"},
    "量子API(鲲鹏)":     {"host": "119.13.90.27", "port": 9000, "path": "/health"},
}


def check_engine(name: str, config: Dict) -> Dict:
    """单引擎健康检查，返回 {name, status, url, code?, error?}"""
    host = config.get("host", "127.0.0.1")
    port = config["port"]
    path = config.get("path", "/health")
    url = f"http://{host}:{port}{path}"

    result = {"name": name, "status": "🔴", "url": url}

    # 先 TCP 端口探测（比 HTTP 更快发现端口未监听）
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        if sock.connect_ex((host, port)) != 0:
            result["error"] = f"端口 {port} 无响应"
            return result
    except Exception as e:
        result["error"] = f"TCP连接异常: {e}"
        return result
    finally:
        if sock:
            sock.close()

    # HTTP 健康端点探测
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "LongHun-EngineVerify/1.0"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            result["code"] = resp.status
            if resp.status == 200:
                result["status"] = "🟢"
            else:
                result["status"] = "🟡"
    except urllib.error.HTTPError as e:
        result["status"] = "🟡"
        result["code"] = e.code
        result["error"] = f"HTTP {e.code}"
    except urllib.error.URLError as e:
        result["status"] = "🔴"
        result["error"] = f"HTTP不可达: {e.reason}"
    except Exception as e:
        result["status"] = "🔴"
        result["error"] = str(e)[:80]

    return result


def verify_all(quiet: bool = False) -> Dict:
    """全量引擎验证，返回汇总Dict"""
    results = []
    for name, config in ENGINES.items():
        r = check_engine(name, config)
        results.append(r)
        time.sleep(0.05)  # 防冲击

    total = len(results)
    green = sum(1 for r in results if r["status"] == "🟢")
    yellow = sum(1 for r in results if r["status"] == "🟡")
    red = sum(1 for r in results if r["status"] == "🔴")

    summary = {
        "total": total,
        "green": green,
        "yellow": yellow,
        "red": red,
        "timestamp": time.time(),
        "engines": results,
    }

    if not quiet:
        _print_report(summary)

    return summary


def _print_report(summary: Dict):
    """终端友好输出"""
    print("╔══════════════════════════════════════════════════╗")
    print("║        🔍 龍魂 · 业务引擎验证报告                 ║")
    print("╠══════════════════════════════════════════════════╣")
    print(f"  🟢 可用: {summary['green']:2d}   🟡 异常: {summary['yellow']:2d}   🔴 不可用: {summary['red']:2d}   📊 总计: {summary['total']}")
    print("╠══════════════════════════════════════════════════╣")

    # 分组输出
    for r in summary["engines"]:
        if r["status"] == "🔴":
            err = r.get("error", "unknown")
            print(f"  🔴 {r['name']:<16s} {r['url']:<45s} {err}")
    for r in summary["engines"]:
        if r["status"] == "🟡":
            print(f"  🟡 {r['name']:<16s} {r['url']:<45s} HTTP {r.get('code', '?')}")
    for r in summary["engines"]:
        if r["status"] == "🟢":
            print(f"  🟢 {r['name']:<16s} {r['url']}")

    print("╚══════════════════════════════════════════════════╝")

    # 健康度百分比
    health_pct = (summary["green"] / summary["total"] * 100) if summary["total"] > 0 else 0
    bar_len = 20
    filled = int(bar_len * health_pct / 100)
    bar = "█" * filled + "░" * (bar_len - filled)
    print(f"  健康度: [{bar}] {health_pct:.0f}%")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·业务引擎验证")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    parser.add_argument("--engine", "-e", help="指定引擎名（模糊匹配）")
    args = parser.parse_args()

    if args.engine:
        # 模糊匹配单引擎
        matched = None
        for name in ENGINES:
            if args.engine in name:
                matched = name
                break
        if matched:
            r = check_engine(matched, ENGINES[matched])
            if args.json:
                print(json.dumps(r, ensure_ascii=False, indent=2))
            else:
                print(f"  {r['status']} {r['name']} → {r['url']}")
                if "error" in r:
                    print(f"     {r['error']}")
        else:
            print(f"❌ 未找到引擎: {args.engine}")
            print(f"   可用引擎: {', '.join(ENGINES.keys())}")
            sys.exit(1)
    else:
        summary = verify_all()
        if args.json:
            print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
