#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
"""
龍魂系统 · 节点心跳上报器 v2.0
DNA: #龍芯⚡️丙午·辛未·乙酉·卯时·讼-NODE-HEARTBEAT-v2.0

功能：
- 每5分钟向注册中心上报心跳
- 只传用量（请求数、存储、运行时间），不传内容
- 内容存在证明（哈希，不传内容）
- DNA签章验证
- 自动发现本地数据源变化

原则：
- 只传用量，不传内容
- DNA签章，透明审计
- 数据主权，本地保留

用法:
    python3 node_heartbeat.py                          # 默认间隔300秒
    python3 node_heartbeat.py --interval 60            # 60秒间隔
    python3 node_heartbeat.py --registry http://IP:9623  # 指定注册中心
"""

import os
import sys
import json
import time
import hashlib
import socket
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    from urllib.request import Request, urlopen
    from urllib.error import URLError, HTTPError
except ImportError:
    from urllib2 import Request, urlopen, URLError, HTTPError

# ============ 龍魂锚定 ============
NODE_ID = os.environ.get("LONGHUN_NODE_ID", f"LH-{socket.gethostname()}-{os.getpid()}")
NODE_DNA = os.environ.get("LONGHUN_NODE_DNA",
    hashlib.sha256(NODE_ID.encode()).hexdigest()[:16])
REGISTRY_URL = os.environ.get("LONGHUN_REGISTRY_URL", "http://localhost:9623")
DNA_ANCHOR = os.environ.get("LONGHUN_DNA_ANCHOR",
    "#龍芯⚡️丙午·辛未·乙酉·卯时·讼-TRAIN-DATA-SOURCES-v2.0")
CONFIRM = os.environ.get("LONGHUN_CONFIRM",
    "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")

CST = timezone(timedelta(hours=8))
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


# ============ 工具函数 ============

def get_folder_size_mb(path: Path) -> float:
    """获取目录大小（MB）"""
    if not path.exists():
        return 0.0
    total = 0
    try:
        for entry in path.rglob('*'):
            if entry.is_file():
                total += entry.stat().st_size
    except Exception:
        pass
    return round(total / (1024 * 1024), 2)


def count_files(path: Path, pattern: str = "*") -> int:
    """统计文件数量"""
    if not path.exists():
        return 0
    try:
        return len(list(path.glob(pattern)))
    except Exception:
        return 0


def get_system_uptime() -> int:
    """获取系统运行时间（秒）"""
    try:
        import subprocess
        result = subprocess.run(['sysctl', '-n', 'kern.boottime'],
                               capture_output=True, text=True)
        # Mac: { sec = 1234567890, usec = 0 }
        import re
        match = re.search(r'sec\s*=\s*(\d+)', result.stdout)
        if match:
            boot_time = int(match.group(1))
            return int(time.time() - boot_time)
    except Exception:
        pass
    return 0


def sign_payload(payload: dict[str, Any]) -> str:
    """DNA签章"""
    content = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(
        (content + DNA_ANCHOR + CONFIRM).encode()
    ).hexdigest()[:32]


# ============ 心跳收集 ============

def collect_metrics() -> dict[str, Any]:
    """收集本节点用量指标（不传内容）"""
    data_dir = PROJECT_ROOT / "data"
    sources_dir = data_dir / "sources"
    fetched_dir = sources_dir / "fetched"
    cleaned_dir = sources_dir / "cleaned"
    train_dir = sources_dir / "train"

    # 统计各类数据
    fetched_files = count_files(fetched_dir, "*.json")
    cleaned_files = count_files(cleaned_dir, "*.json")
    train_files = count_files(train_dir, "*.jsonl")

    return {
        "fetched_sessions": fetched_files,
        "cleaned_sessions": cleaned_files,
        "train_data_files": train_files,
        "storage_total_mb": (
            get_folder_size_mb(fetched_dir) +
            get_folder_size_mb(cleaned_dir) +
            get_folder_size_mb(train_dir)
        ),
        "protocol_files": count_files(PROJECT_ROOT / "01_protocols", "*.md"),
        "skill_files": count_files(PROJECT_ROOT / "01_技能庫", "*.py"),
        "hostname": socket.gethostname(),
        "python_version": sys.version.split()[0],
        "uptime_seconds": get_system_uptime(),
    }


def send_heartbeat(registry_url: str | None = None) -> bool:
    """发送心跳到注册中心"""
    url = registry_url or REGISTRY_URL
    metrics = collect_metrics()

    payload = {
        "node_id": NODE_ID,
        "node_dna": NODE_DNA,
        "timestamp": int(time.time()),
        "timestamp_iso": datetime.now(CST).isoformat(),
        "metrics": metrics,

        # 内容存在证明（哈希，不传内容）
        "content_proof": {
            "protocols_hash": hashlib.sha256(
                str(list((PROJECT_ROOT / "01_protocols").glob("*.md"))).encode()
            ).hexdigest()[:16] if (PROJECT_ROOT / "01_protocols").exists() else "",
        },

        "dna_anchor": DNA_ANCHOR[:40] + "...",
    }

    payload["signature"] = sign_payload(payload)

    try:
        req = Request(
            f"{url}/heartbeat",
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'LongHunNode/2.0',
                'X-Node-ID': NODE_ID,
            }
        )
        with urlopen(req, timeout=10) as resp:
            if resp.getcode() == 200:
                response = json.loads(resp.read().decode())
                online = response.get("nodes_online", 0)
                total = response.get("total_nodes", 0)
                now = datetime.now(CST).strftime('%H:%M:%S')
                print(f"[{now}] 🐉 心跳 ✅ | 节点: {NODE_ID[:20]}... | "
                      f"在线: {online}/{total} | 存储: {metrics['storage_total_mb']}MB")
                return True
    except HTTPError as e:
        print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] ⚠️  上报失败 HTTP {e.code}")
    except URLError as e:
        print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] ⚠️  连接失败: {str(e.reason)[:50]}")
    except Exception as e:
        print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] ⚠️  失败: {str(e)[:50]}")

    return False


def main():
    parser = argparse.ArgumentParser(description="龍魂节点心跳上报器 v2.0")
    parser.add_argument('--registry', help=f'注册中心地址 (默认: {REGISTRY_URL})')
    parser.add_argument('--interval', type=int, default=300, help='心跳间隔秒数 (默认: 300)')
    parser.add_argument('--once', action='store_true', help='仅发送一次心跳')
    parser.add_argument('--node-id', help='自定义节点ID')
    args = parser.parse_args()

    global NODE_ID
    if args.node_id:
        NODE_ID = args.node_id

    registry_url = args.registry or REGISTRY_URL

    print(f"🐉 龍魂节点心跳器 v2.0")
    print(f"🐉 节点ID: {NODE_ID}")
    print(f"🐉 节点DNA: {NODE_DNA}")
    print(f"🐉 注册中心: {registry_url}")
    print(f"🐉 项目: {PROJECT_ROOT}")
    print(f"🐉 原则: 只传用量，不传内容")
    print()

    if args.once:
        send_heartbeat(registry_url)
        return

    print(f"⏱️  心跳间隔: {args.interval}秒")
    print()

    while True:
        send_heartbeat(registry_url)
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
