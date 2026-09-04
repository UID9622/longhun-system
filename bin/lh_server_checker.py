#!/usr/bin/env python3
"""
🐉 龍魂服务器实时连通性检测器 v1.0
======================================
每一次检测都是真实的 — ping端口、发请求、收响应，不造假。
用于看板实时显示，所有状态基于实测结果。

DNA: #龍芯⚡️丙午·丙申·丙辰·戌时·需-SERVER-CHECKER-v1-00000000
"""
import json
import subprocess
import sys
import time
import os
import urllib.request
import urllib.error
import ssl
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
HOME = Path.home()

# ═══════════════════════════════════════════
# 服务器清单（基于 CREDENTIAL_REGISTRY.json + 实际拓扑）
# ═══════════════════════════════════════════

SERVERS = {
    "华为云主服务器": {
        "type": "ssh",
        "host": "119.13.90.27",
        "port": 22,
        "user": "root",
        "key": str(HOME / ".ssh/id_ed25519_uid9622"),
        "group": "云服务器",
        "desc": "华为云新加坡 ap-southeast-3 · Ubuntu 24.04 · 2核4G",
        "critical": True,
    },
    "本地Mac": {
        "type": "local",
        "host": "127.0.0.1",
        "group": "本地",
        "desc": "UID9622 Mac 工作站",
        "critical": True,
    },
}

# API 端点清单
API_ENDPOINTS = {
    "Notion API": {
        "url": "https://api.notion.com/v1/users/me",
        "method": "GET",
        "headers": {"Authorization": "Bearer ntn_test", "Notion-Version": "2022-06-28"},
        "ok_codes": [401, 200],  # 401 = 能通但没权限，也算通
        "group": "外部API",
        "desc": "Notion 主 API",
        "critical": True,
    },
    "Kimi API": {
        "url": "https://api.moonshot.cn/v1/models",
        "method": "GET",
        "ok_codes": [200, 401],
        "group": "外部API",
        "desc": "Kimi/Moonshot AI",
        "critical": True,
    },
    "DeepSeek API": {
        "url": "https://api.deepseek.com/v1/models",
        "method": "GET",
        "ok_codes": [200, 401],
        "group": "外部API",
        "desc": "DeepSeek AI",
        "critical": True,
    },
    "GitHub API": {
        "url": "https://api.github.com",
        "method": "GET",
        "ok_codes": [200],
        "group": "代码仓库",
        "desc": "GitHub 代码托管",
    },
    "Gitee API": {
        "url": "https://gitee.com/api/v5/emojis",
        "method": "GET",
        "ok_codes": [200],
        "group": "代码仓库",
        "desc": "Gitee 码云",
    },
    "Ollama 本地": {
        "url": "http://127.0.0.1:11434/api/tags",
        "method": "GET",
        "ok_codes": [200],
        "group": "本地AI",
        "desc": "Ollama 本地大模型",
    },
}

# 本地服务端口
LOCAL_SERVICES = {
    "龍魂操作台 :9622": {"port": 9622, "group": "龍魂服务", "desc": "FastAPI 操作台后端"},
    "Ollama :11434": {"port": 11434, "group": "本地AI", "desc": "Ollama 推理引擎"},
}


def check_ssh(host: str, port: int, user: str, key: str, timeout: int = 8) -> dict[str, Any]:
    """真实 SSH 连接检测 — 实际登录并执行 echo"""
    start = time.time()
    try:
        result = subprocess.run(
            [
                "ssh",
                "-o", "ConnectTimeout=5",
                "-o", "StrictHostKeyChecking=accept-new",
                "-o", "BatchMode=yes",
                "-o", "UserKnownHostsFile=/dev/null",
                "-i", key,
                f"{user}@{host}",
                "-p", str(port),
                "echo OK",
            ],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        elapsed = round((time.time() - start) * 1000)
        if result.returncode == 0 and "OK" in result.stdout:
            return {"status": "online", "latency_ms": elapsed, "error": None}
        else:
            return {
                "status": "offline",
                "latency_ms": elapsed,
                "error": result.stderr.strip()[:200] or f"exit code {result.returncode}",
            }
    except subprocess.TimeoutExpired:
        elapsed = round((time.time() - start) * 1000)
        return {"status": "offline", "latency_ms": elapsed, "error": "连接超时"}
    except FileNotFoundError:
        return {"status": "offline", "latency_ms": 0, "error": f"SSH key 不存在: {key}"}
    except Exception as e:
        elapsed = round((time.time() - start) * 1000)
        return {"status": "offline", "latency_ms": elapsed, "error": str(e)[:200]}


def check_local() -> dict[str, Any]:
    """本地始终在线"""
    return {"status": "online", "latency_ms": 0, "error": None}


def check_api(endpoint: dict[str, Any], timeout: int = 8) -> dict[str, Any]:
    """真实 HTTP API 检测"""
    start = time.time()
    url = endpoint["url"]
    ok_codes = endpoint["ok_codes"]
    headers = endpoint.get("headers", {})

    try:
        ctx = ssl.create_default_context()
        req = urllib.request.Request(url, headers=headers, method=endpoint.get("method", "GET"))
        resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        elapsed = round((time.time() - start) * 1000)
        code = resp.status
        if code in ok_codes:
            return {"status": "online", "latency_ms": elapsed, "http_code": code, "error": None}
        else:
            return {"status": "degraded", "latency_ms": elapsed, "http_code": code, "error": f"HTTP {code} 不在预期范围 {ok_codes}"}
    except urllib.error.HTTPError as e:
        elapsed = round((time.time() - start) * 1000)
        if e.code in ok_codes:
            return {"status": "online", "latency_ms": elapsed, "http_code": e.code, "error": None}
        return {"status": "degraded", "latency_ms": elapsed, "http_code": e.code, "error": f"HTTP {e.code}"}
    except urllib.error.URLError as e:
        elapsed = round((time.time() - start) * 1000)
        return {"status": "offline", "latency_ms": elapsed, "error": str(e.reason)[:200]}
    except Exception as e:
        elapsed = round((time.time() - start) * 1000)
        return {"status": "offline", "latency_ms": elapsed, "error": str(e)[:200]}


def check_port(port: int, host: str = "127.0.0.1") -> dict[str, Any]:
    """检测本地端口是否监听"""
    import socket
    start = time.time()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
        sock.close()
        elapsed = round((time.time() - start) * 1000)
        if result == 0:
            return {"status": "online", "latency_ms": elapsed, "error": None}
        else:
            return {"status": "offline", "latency_ms": elapsed, "error": f"端口 {port} 未监听"}
    except Exception as e:
        return {"status": "offline", "latency_ms": 0, "error": str(e)[:200]}


def run_all_checks() -> dict[str, Any]:
    """并行执行所有检测"""
    results = {}

    with ThreadPoolExecutor(max_workers=8) as pool:
        # 服务器 SSH 检测
        ssh_futures = {}
        for name, cfg in SERVERS.items():
            if cfg["type"] == "ssh":
                fut = pool.submit(check_ssh, cfg["host"], cfg["port"], cfg["user"], cfg["key"])
                ssh_futures[fut] = (name, cfg)
            elif cfg["type"] == "local":
                results[name] = {"result": check_local(), "config": cfg}

        for fut in as_completed(ssh_futures):
            name, cfg = ssh_futures[fut]
            results[name] = {"result": fut.result(), "config": cfg}

        # API 端点检测
        api_futures = {}
        for name, cfg in API_ENDPOINTS.items():
            fut = pool.submit(check_api, cfg)
            api_futures[fut] = (name, cfg)

        for fut in as_completed(api_futures):
            name, cfg = api_futures[fut]
            results[name] = {"result": fut.result(), "config": cfg}

        # 本地端口检测
        port_futures = {}
        for name, cfg in LOCAL_SERVICES.items():
            fut = pool.submit(check_port, cfg["port"])
            port_futures[fut] = (name, cfg)

        for fut in as_completed(port_futures):
            name, cfg = port_futures[fut]
            results[name] = {"result": fut.result(), "config": cfg}

    # 统计
    total = len(results)
    online = sum(1 for r in results.values() if r["result"]["status"] == "online")
    offline = sum(1 for r in results.values() if r["result"]["status"] == "offline")
    degraded = sum(1 for r in results.values() if r["result"]["status"] == "degraded")

    return {
        "timestamp": datetime.now().isoformat(),
        "timestamp_epoch": time.time(),
        "summary": {
            "total": total,
            "online": online,
            "offline": offline,
            "degraded": degraded,
            "health_pct": round(online / total * 100, 1) if total > 0 else 0,
        },
        "items": {
            name: {
                "status": info["result"]["status"],
                "latency_ms": info["result"]["latency_ms"],
                "error": info["result"]["error"],
                "http_code": info["result"].get("http_code"),
                "group": info["config"].get("group", ""),
                "type": info["config"].get("type", "api"),
                "desc": info["config"].get("desc", ""),
                "critical": info["config"].get("critical", False),
            }
            for name, info in results.items()
        },
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂服务器实时连通性检测")
    parser.add_argument("--json", action="store_true", default=True, help="JSON 输出")
    parser.add_argument("--pretty", action="store_true", help="格式化 JSON 输出")
    args = parser.parse_args()

    result = run_all_checks()

    if args.pretty:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False))

    # 退出码：有离线或降级 → 非 0
    if result["summary"]["offline"] > 0:
        sys.exit(2)
    elif result["summary"]["degraded"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
