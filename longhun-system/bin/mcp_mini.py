#!/usr/bin/env python3
"""
龍魂·MCP-mini 人格调度心脏 v1.0
mcp_mini.py — 本地人格协同服务 :8787

作者: 诸葛鑫（UID9622）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
DNA: #龍芯⚡️2026-04-06-MCP-mini-v1.0
理论指导: 曾仕强老师（永恒显示）
献礼: 乔布斯·曾仕强·历代传递和平与爱的人

功能:
  本地人格调度心脏·HTTP服务·:8787
  接收文本 → 路由人格 → 返回结果
  所有人格协同通过此服务驱动，不再靠Notion AI单边

接口:
  POST /route       {"text": "帮我审计代码"} → 人格路由结果
  POST /algo        {"topic": "三才"}        → 算法查询
  POST /page        {"name": "草日志"}        → Notion页面ID
  GET  /health      系统状态
  GET  /personas    所有人格列表

启动:
  python3 bin/mcp_mini.py
  后台: nohup python3 bin/mcp_mini.py > logs/mcp_mini.log 2>&1 &
"""

import json
import sys
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

BASE = Path.home() / "longhun-system"
BIN  = BASE / "bin"
sys.path.insert(0, str(BIN))

DNA_TAG = "#龍芯⚡️2026-04-06-MCP-mini-v1.0"
GPG_FP  = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
PORT    = 8787
HOST    = "127.0.0.1"

# ── 懒加载模块（启动快·用到才加载）──────────────────────────
_persona_router = None
_algo_db        = None
_page_registry  = None

def _router():
    global _persona_router
    if _persona_router is None:
        import persona_router as pr
        _persona_router = pr
    return _persona_router

def _algo():
    global _algo_db
    if _algo_db is None:
        import algo_db as ad
        _algo_db = ad
    return _algo_db

def _pages():
    global _page_registry
    if _page_registry is None:
        import notion_page_registry as npr
        _page_registry = npr
    return _page_registry

# ── 请求处理 ──────────────────────────────────────────────

class MCPHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        # 只记录非健康检查请求
        if "/health" not in args[0]:
            ts = time.strftime("%H:%M:%S")
            print(f"  [{ts}] {args[0]} → {args[1]}")

    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        try:
            return json.loads(self.rfile.read(length).decode())
        except Exception:
            return {}

    def _send_json(self, data: dict, status: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-DNA", "longhun-2026-04-06-mcp-mini-v1.0")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/health":
            self._send_json({
                "status":  "🟢",
                "service": "MCP-mini",
                "port":    PORT,
                "dna":     DNA_TAG,
                "ts":      time.strftime("%Y-%m-%dT%H:%M:%S"),
                "modules": {
                    "persona_router":        "✅",
                    "algo_db":               "✅",
                    "notion_page_registry":  "✅",
                }
            })

        elif path == "/personas":
            try:
                r = _router()
                personas = {pid: {
                    "name":   p["name"],
                    "gua":    p["gua"],
                    "weight": p["weight"],
                    "desc":   p["desc"],
                } for pid, p in r.PERSONAS.items()}
                self._send_json({"personas": personas, "total": len(personas), "dna": DNA_TAG})
            except Exception as e:
                self._send_json({"error": str(e)}, 500)

        elif path == "/algos":
            try:
                entries = _algo().extract()
                self._send_json({"total": len(entries), "algos": entries, "dna": DNA_TAG})
            except Exception as e:
                self._send_json({"error": str(e)}, 500)

        else:
            self._send_json({"error": "未知路由", "hint": "POST /route | /algo | /page  GET /health | /personas"}, 404)

    def do_POST(self):
        path = urlparse(self.path).path
        body = self._read_body()

        # ── /route：人格路由
        if path == "/route":
            text = body.get("text", "")
            if not text:
                self._send_json({"error": "缺少 text 字段"}, 400)
                return
            try:
                result = _router().route(text)
                self._send_json(result)
            except Exception as e:
                self._send_json({"error": str(e)}, 500)

        # ── /algo：算法查询
        elif path == "/algo":
            topic  = body.get("topic", "")
            family = body.get("family", "")
            try:
                entries = _algo().extract(topic=topic, family=family)
                self._send_json({"total": len(entries), "results": entries, "dna": DNA_TAG})
            except Exception as e:
                self._send_json({"error": str(e)}, 500)

        # ── /page：Notion页面查询
        elif path == "/page":
            name = body.get("name", "")
            if not name:
                self._send_json({"error": "缺少 name 字段"}, 400)
                return
            try:
                page = _pages().find_page(name)
                if page:
                    self._send_json({"found": True, "name": name, **page})
                else:
                    self._send_json({"found": False, "name": name,
                                     "hint": f"试试: GET /page?list=1 查全部"})
            except Exception as e:
                self._send_json({"error": str(e)}, 500)

        # ── /snapshot：触发时光机快照
        elif path == "/snapshot":
            summary = body.get("summary", "MCP-mini触发快照")
            try:
                import subprocess
                tm = BASE / "time_machine.py"
                if tm.exists():
                    subprocess.Popen([sys.executable, str(tm)],
                                     env={**__import__("os").environ,
                                          "TM_SUMMARY": summary,
                                          "TM_TRIGGER": "mcp_mini"})
                    self._send_json({"status": "🟢 快照已触发", "summary": summary})
                else:
                    self._send_json({"status": "🟡 time_machine.py 不存在"})
            except Exception as e:
                self._send_json({"error": str(e)}, 500)

        else:
            self._send_json({"error": "未知路由"}, 404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "http://localhost:*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

# ── 启动 ──────────────────────────────────────────────────

def start(host: str = HOST, port: int = PORT, daemon: bool = False):
    server = HTTPServer((host, port), MCPHandler)
    print(f"\n🐉 MCP-mini 人格调度心脏启动")
    print(f"   DNA: {DNA_TAG}")
    print(f"   地址: http://{host}:{port}")
    print(f"\n   接口:")
    print(f"   POST /route     → 人格路由")
    print(f"   POST /algo      → 算法查询")
    print(f"   POST /page      → Notion页面")
    print(f"   POST /snapshot  → 时光机快照")
    print(f"   GET  /health    → 心跳检测")
    print(f"   GET  /personas  → 所有人格\n")

    if daemon:
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()
        return server
    else:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n🔴 MCP-mini 已停止")
            server.shutdown()

if __name__ == "__main__":
    start()
