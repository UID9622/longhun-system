#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
app_patch.py · app.py 补丁模块 v1.0
DNA: #龍芯⚡️2026-04-07-APP-PATCH-v1.0
作者: 诸葛鑫（UID9622）
用途: 补充缺失的API端点 + 修正HTML Content-Type
运行方式: python3 ~/longhun-system/app_patch.py
端口: 8001（不冲突主引擎8000）

接入的端点（API文档 v1.0）:
  GET  /health    → 健康检查
  GET  /status    → 系统状态（所有服务）
  GET  /memory    → 最近100条记忆
  GET  /knowledge → 知识库条目
  GET  /dna/list  → DNA码列表
  GET  /static/*  → 静态文件（HTML正确Content-Type）
  POST /chat      → 宝宝对话（X-UID: 9622）
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

BASE_DIR = Path.home() / "longhun-system"
MEMORY_FILE = BASE_DIR / "memory.jsonl"
LOGS_DIR = BASE_DIR / "logs"
STATIC_DIR = BASE_DIR / "static"
PORT = 8001

MIME = {
    '.html': 'text/html; charset=utf-8',
    '.css':  'text/css',
    '.js':   'application/javascript',
    '.json': 'application/json',
    '.svg':  'image/svg+xml',
    '.ttf':  'font/ttf',
    '.otf':  'font/otf',
    '.png':  'image/png',
    '.jpg':  'image/jpeg',
    '.ico':  'image/x-icon',
}

def read_memory(n=100):
    """读最近n条 memory.jsonl"""
    if not MEMORY_FILE.exists():
        return []
    lines = MEMORY_FILE.read_text(encoding='utf-8', errors='ignore').strip().split('\n')
    result = []
    for line in reversed(lines[-n*2:]):
        if not line.strip(): continue
        try:
            result.append(json.loads(line))
            if len(result) >= n: break
        except: pass
    return result

def get_dna_list():
    """从memory里提取所有DNA码"""
    mems = read_memory(500)
    dnas = set()
    for m in mems:
        for val in m.values():
            s = str(val)
            if '#龍芯⚡️' in s:
                for part in s.split('#龍芯⚡️')[1:]:
                    dna = '#龍芯⚡️' + part.split()[0].split('"')[0].split("'")[0]
                    dnas.add(dna)
    return sorted(dnas)

def check_port(port):
    """检查端口是否有服务"""
    import socket
    try:
        s = socket.socket()
        s.settimeout(0.5)
        s.connect(('127.0.0.1', port))
        s.close()
        return True
    except:
        return False

class PatchHandler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args): pass  # 静默日志

    def cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-UID')

    def json_ok(self, data):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.cors()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.cors()
        self.end_headers()

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path

        # ── 静态文件（HTML正确Content-Type）──
        if path.startswith('/static/') or path == '/' or path == '/portal':
            if path == '/' or path == '/portal':
                path = '/static/portal.html'
            file_path = BASE_DIR / path.lstrip('/')
            if file_path.exists() and file_path.is_file():
                ext = file_path.suffix.lower()
                mime = MIME.get(ext, 'application/octet-stream')
                body = file_path.read_bytes()
                self.send_response(200)
                self.send_header('Content-Type', mime)
                self.cors()
                self.end_headers()
                self.wfile.write(body)
            else:
                self.send_response(404)
                self.end_headers()
            return

        # ── /health ──
        if path == '/health':
            self.json_ok({
                "status": "ok",
                "engine": "龍魂·app_patch v1.0",
                "port": PORT,
                "dna": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-PATCH-v1.0",
                "ts": datetime.now().isoformat()
            })
            return

        # ── /status ──
        if path == '/status':
            ports = {8000: '龍魂引擎', 8080: 'Open WebUI', 8765: '旧服务', 9622: '龍魂API', 8001: '补丁服务'}
            services = {}
            for p, label in ports.items():
                services[str(p)] = {"label": label, "online": check_port(p)}
            mem_count = len(read_memory(1000))
            self.json_ok({
                "dna": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-STATUS",
                "ts": datetime.now().isoformat(),
                "uid": "UID9622",
                "services": services,
                "memory_count": mem_count,
                "base_dir": str(BASE_DIR),
            })
            return

        # ── /memory ──
        if path == '/memory':
            mems = read_memory(100)
            self.json_ok({
                "count": len(mems),
                "items": mems,
                "dna": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-MEMORY-READ"
            })
            return

        # ── /knowledge ──
        if path == '/knowledge':
            kb_path = BASE_DIR / "knowledge.db"
            if kb_path.exists():
                import sqlite3
                conn = sqlite3.connect(kb_path)
                rows = conn.execute("SELECT title,source,tags,timestamp FROM knowledge LIMIT 100").fetchall()
                conn.close()
                items = [{"title": r[0], "source": r[1], "tags": r[2], "ts": r[3]} for r in rows]
            else:
                items = []
            self.json_ok({"count": len(items), "items": items})
            return

        # ── /dna/list ──
        if path == '/dna/list':
            dnas = get_dna_list()
            self.json_ok({"count": len(dnas), "dnas": dnas})
            return

        # ── /sancai/weights ──
        if path == '/sancai/weights':
            h = datetime.now().hour
            # 天(乾)·地(坤)·人·随时间流动
            tian = round(0.35 + 0.05 * (1 if 6<=h<=12 else -1 if 18<=h<=24 else 0), 2)
            di   = round(0.35 - 0.03 * (1 if 12<=h<=18 else 0), 2)
            ren  = round(1.0 - tian - di, 2)
            self.json_ok({
                "天": tian, "地": di, "人": ren,
                "时辰": f"{h}时",
                "dna": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-SANCAI"
            })
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8', errors='ignore')

        # ── /chat （宝宝人格）──
        if path == '/chat':
            try:
                data = json.loads(body) if body else {}
                msg = data.get('message') or ''
                if not msg:
                    msgs = data.get('messages', [])
                    msg = next((m.get('content','') for m in msgs if m.get('role')=='user'), '')
                persona = data.get('persona', '宝宝')

                # 转发到8000主引擎
                import urllib.request
                payload = json.dumps({
                    "message": msg,
                    "persona": persona,
                    "uid": "UID9622"
                }).encode('utf-8')
                req8000 = urllib.request.Request(
                    'http://localhost:8000/chat',
                    data=payload,
                    headers={'Content-Type': 'application/json', 'X-UID': '9622'},
                    method='POST'
                )
                try:
                    with urllib.request.urlopen(req8000, timeout=20) as r:
                        upstream = json.loads(r.read().decode())
                        reply = upstream.get('reply', '')
                        if persona == '宝宝' and reply and not reply.startswith('🐱'):
                            reply = '🐱 ' + reply
                        self.json_ok({
                            "reply": reply,
                            "persona": persona,
                            "upstream": "8000",
                            "dna": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-CHAT-{persona}"
                        })
                        return
                except Exception:
                    pass

                # 8000挂了，宝宝本地兜底
                today = datetime.now().strftime('%Y-%m-%d')
                reply = f"🐱 收到「{msg[:40]}」，引擎8000离线，先跑：python3 ~/longhun-system/app.py\nDNA: #龍芯⚡️{today}-BAOBAO-LOCAL"
                self.json_ok({"reply": reply, "persona": "宝宝", "upstream": "local"})
            except Exception as e:
                self.json_ok({"error": str(e)})
            return

        self.send_response(404)
        self.end_headers()


def main():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🐱 宝宝补丁服务 · app_patch v1.0")
    print(f"DNA: #龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-APP-PATCH-v1.0")
    print(f"端口: {PORT}  (主引擎在8000，这是补充)")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  GET  http://localhost:{PORT}/          → 总控台")
    print(f"  GET  http://localhost:{PORT}/health    → 健康")
    print(f"  GET  http://localhost:{PORT}/status    → 所有服务状态")
    print(f"  GET  http://localhost:{PORT}/memory    → 最近100条记忆")
    print(f"  GET  http://localhost:{PORT}/knowledge → 知识库")
    print(f"  GET  http://localhost:{PORT}/dna/list  → DNA码列表")
    print(f"  GET  http://localhost:{PORT}/sancai/weights → 三才权重")
    print(f"  POST http://localhost:{PORT}/chat      → 宝宝对话")
    print(f"  GET  http://localhost:{PORT}/static/*  → 静态文件(HTML正确)")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    server = HTTPServer(("0.0.0.0", PORT), PatchHandler)
    print(f"🟢 宝宝在，等你叫\n")
    server.serve_forever()

if __name__ == '__main__':
    main()
