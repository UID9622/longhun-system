#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
"""
龍魂系统 · 分布式注册中心 v2.0
DNA: #龍芯⚡️丙午·辛未·乙酉·卯时·讼-LH-REGISTRY-v2.0

功能：
- 接收各节点心跳（只存用量，不存内容）
- 全局统计：节点数、总存储、总请求
- 节点质量评分
- DNA签章验证
- 内存存储（生产环境可换Redis/PostgreSQL）

原则：
- 只传用量，不传内容
- DNA签章，透明审计
- 数据主权，本地保留
- 中国法律唯一准绳

用法:
    python3 registry_server.py --port 9623
"""

import json
import hashlib
import time
import argparse
from datetime import datetime, timezone, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from collections import defaultdict, OrderedDict

# ============ 龍魂DNA锚定 ============
DNA_ANCHOR = "#龍芯⚡️丙午·辛未·乙酉·卯时·讼-TRAIN-DATA-SOURCES-v2.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
CST = timezone(timedelta(hours=8))

# ============ 存储 ============
nodes: dict[str, Any] = {}                 # node_id → 最新心跳
node_history: dict[str, Any] = defaultdict(list)  # node_id → 历史记录 (最近100条)
node_audit_results: dict[str, Any] = {}    # node_id → 最新审计结果
NODE_TIMEOUT_SECONDS = 600       # 10分钟无心跳视为离线

# ============ 请求处理器 ============
class RegistryHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        """静默日志（生产环境可开启）"""
        pass

    def _cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-Node-ID, X-Auth-Token')

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path == "/health":
            self._respond(200, {
                "status": "ok",
                "registry": "longhun-registry-v2.0",
                "dna": DNA_ANCHOR[:40] + "...",
                "uptime_seconds": int(time.time() - START_TIME),
                "cst_time": datetime.now(CST).isoformat(),
            })

        elif self.path == "/nodes":
            online_nodes = self._get_online_nodes()
            offline_nodes = self._get_offline_nodes()
            self._respond(200, {
                "total_nodes": len(nodes),
                "online": len(online_nodes),
                "offline": len(offline_nodes),
                "nodes": {
                    nid: {
                        "last_seen": n.get("timestamp_iso", ""),
                        "metrics": n.get("metrics", {}),
                        "signature_valid": n.get("signature_valid", False),
                        "status": "online" if nid in online_nodes else "offline",
                    }
                    for nid, n in nodes.items()
                }
            })

        elif self.path == "/stats":
            total_storage = sum(
                n.get("metrics", {}).get("storage_used_gb", 0) for n in nodes.values()
            )
            total_requests = sum(
                n.get("metrics", {}).get("requests_handled", 0) for n in nodes.values()
            )
            total_crawls = sum(
                n.get("metrics", {}).get("crawl_sessions", 0) for n in nodes.values()
            )
            online = self._get_online_nodes()
            self._respond(200, {
                "total_nodes": len(nodes),
                "online_nodes": len(online),
                "total_storage_gb": round(total_storage, 2),
                "total_requests": total_requests,
                "total_crawl_sessions": total_crawls,
                "dna": DNA_ANCHOR[:40] + "...",
                "cst_time": datetime.now(CST).isoformat(),
            })

        elif self.path == "/audit":
            self._respond(200, {
                "total_audited": len(node_audit_results),
                "results": node_audit_results,
            })

        elif self.path.startswith("/node/"):
            node_id = self.path.split("/node/")[-1]
            if node_id in nodes:
                history = node_history.get(node_id, [])
                self._respond(200, {
                    "node_id": node_id,
                    "latest": nodes[node_id],
                    "history_count": len(history),
                    "recent_history": history[-5:],
                })
            else:
                self._respond(404, {"error": "node not found"})

        else:
            self._respond(404, {"error": "not found"})

    def do_POST(self):
        if self.path == "/heartbeat":
            content_len = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_len).decode('utf-8')

            try:
                data = json.loads(body)
                node_id = data.get("node_id", "unknown")

                # 验证签名
                sig = data.pop("signature", "")
                expected = hashlib.sha256(
                    (json.dumps(data, sort_keys=True, ensure_ascii=False) + DNA_ANCHOR + CONFIRM).encode()
                ).hexdigest()[:32]
                data["signature_valid"] = (sig == expected)
                data["received_at"] = datetime.now(CST).isoformat()

                # 存储
                nodes[node_id] = data
                node_history[node_id].append({
                    "timestamp": data.get("timestamp", 0),
                    "timestamp_iso": data.get("received_at", ""),
                    "metrics": data.get("metrics", {}),
                })

                # 只保留最近100条
                if len(node_history[node_id]) > 100:
                    node_history[node_id] = node_history[node_id][-100:]

                self._respond(200, {
                    "status": "received",
                    "node_id": node_id,
                    "nodes_online": len(self._get_online_nodes()),
                    "total_nodes": len(nodes),
                })

            except json.JSONDecodeError:
                self._respond(400, {"error": "invalid json"})
            except Exception as e:
                self._respond(500, {"error": str(e)[:50]})

        elif self.path == "/audit/report":
            content_len = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_len).decode('utf-8')
            try:
                data = json.loads(body)
                node_id = data.get("node_id", "unknown")
                node_audit_results[node_id] = {
                    "score": data.get("summary", {}).get("score", 0),
                    "passed": data.get("summary", {}).get("passed", 0),
                    "failed": data.get("summary", {}).get("failed", 0),
                    "audited_at": data.get("audited_at", ""),
                }
                self._respond(200, {"status": "received"})
            except Exception as e:
                self._respond(400, {"error": str(e)[:50]})

        else:
            self._respond(404, {"error": "not found"})

    def _respond(self, code, data):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self._cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode())

    def _get_online_nodes(self):
        """获取在线节点列表（10分钟内有心跳）"""
        now = time.time()
        online = {}
        for nid, n in nodes.items():
            ts = n.get("timestamp", 0)
            if now - ts < NODE_TIMEOUT_SECONDS:
                online[nid] = n
        return online

    def _get_offline_nodes(self):
        now = time.time()
        offline = {}
        for nid, n in nodes.items():
            ts = n.get("timestamp", 0)
            if now - ts >= NODE_TIMEOUT_SECONDS:
                offline[nid] = n
        return offline


START_TIME = time.time()


def main():
    parser = argparse.ArgumentParser(description="龍魂分布式注册中心 v2.0")
    parser.add_argument('--port', type=int, default=9623, help='监听端口 (默认: 9623)')
    parser.add_argument('--host', default='0.0.0.0', help='监听地址 (默认: 0.0.0.0)')
    args = parser.parse_args()

    print(f"🐉 龍魂注册中心 v2.0 启动")
    print(f"🐉 DNA: {DNA_ANCHOR}")
    print(f"🐉 {CONFIRM}")
    print(f"")
    print(f"📡 监听: {args.host}:{args.port}")
    print(f"📋 接口:")
    print(f"   GET  /health       健康检查")
    print(f"   GET  /nodes        节点列表 (在线/离线)")
    print(f"   GET  /stats        全局统计")
    print(f"   GET  /audit        审计结果汇总")
    print(f"   GET  /node/<id>    节点详情")
    print(f"   POST /heartbeat    接收心跳")
    print(f"   POST /audit/report 接收审计报告")
    print(f"")
    print(f"🐉 原则: 只存用量，不存内容 · DNA签章 · 透明审计")
    print(f"")

    server = HTTPServer((args.host, args.port), RegistryHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🐉 注册中心已停止")
        server.shutdown()


if __name__ == "__main__":
    main()
