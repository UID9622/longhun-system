# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂模型指挥调度系统 · Web 后端桥接服务
DNA: #龍芯⚡️2026-06-28-LONGHUN-COMMANDER-WEB-BRIDGE-v1.0

为前端官网提供 HTTP API，实际调度交给 ~/.龍魂/bin/lh-调度 执行。
端口：8000
"""

import json
import mimetypes
import subprocess
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

LH_DISPATCH = str(Path.home() / '.龍魂' / 'bin' / 'lh-调度')
HOST = '127.0.0.1'
PORT = 8000
DIST_DIR = Path(__file__).parent / 'dist'


def guess_type(path):
    return mimetypes.guess_type(str(path))[0] or 'application/octet-stream'


PUBLIC_DOCS_INDEX = Path.home() / '_work' / 'public_sources_index.json'


def load_public_docs():
    if not PUBLIC_DOCS_INDEX.exists():
        return []
    try:
        data = json.loads(PUBLIC_DOCS_INDEX.read_text(encoding='utf-8'))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def run_dispatch(args):
    try:
        result = subprocess.run(
            [LH_DISPATCH] + args,
            capture_output=True, text=True, timeout=300
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, '', str(e)


class CORSRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == '/health':
            self._set_headers()
            self.wfile.write(json.dumps({'ok': True, 'service': 'longhun-commander-web-bridge'}).encode())
            return

        # 静态文件服务（生产构建 dist/）
        if not path.startswith('/api/'):
            file_path = DIST_DIR / path.lstrip('/')
            if path == '/' or file_path.is_dir():
                file_path = DIST_DIR / 'index.html'
            if file_path.exists() and file_path.is_file():
                self._set_headers(200, guess_type(file_path))
                self.wfile.write(file_path.read_bytes())
                return

        if path == '/api/status':
            rc, out, err = run_dispatch(['状态'])
            self._send_text(rc, out, err)
            return

        if path == '/api/health':
            rc, out, err = run_dispatch(['健康'])
            self._send_text(rc, out, err)
            return

        if path == '/api/topology':
            rc, out, err = run_dispatch(['拓扑'])
            self._send_text(rc, out, err)
            return

        if path == '/api/stats':
            rc, out, err = run_dispatch(['统计'])
            self._send_text(rc, out, err)
            return

        if path == '/api/trace':
            dna = query.get('dna', [''])[0]
            if not dna:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': '缺少 dna 参数'}).encode())
                return
            rc, out, err = run_dispatch(['链路', dna])
            self._send_text(rc, out, err)
            return

        if path == '/api/public-docs':
            self._serve_public_docs()
            return

        if path == '/api/audit':
            self._serve_audit_report()
            return

        self._set_headers(404)
        self.wfile.write(json.dumps({'error': '未找到接口'}).encode())

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == '/api/dispatch':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'JSON 解析失败'}).encode())
                return

            task = data.get('task', '').strip()
            if not task:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': '任务不能为空'}).encode())
                return

            rc, out, err = run_dispatch([task])
            self._send_text(rc, out, err)
            return

        if path == '/api/auth/level':
            self._serve_auth_level()
            return

        self._set_headers(404)
        self.wfile.write(json.dumps({'error': '未找到接口'}).encode())

    def _serve_public_docs(self):
        docs = load_public_docs()
        self._set_headers(200, 'application/json')
        self.wfile.write(json.dumps({
            'ok': True,
            'dna': '#龍芯⚡️2026-06-28-PUBLIC-DOCS-LIST-v1.0',
            'count': len(docs),
            'docs': docs,
        }, ensure_ascii=False).encode())

    def _serve_audit_report(self):
        report_file = Path.home() / '_work' / 'self_audit_report.json'
        # Refresh report
        try:
            subprocess.run(
                [sys.executable, str(Path.home() / '_work' / 'self_audit_loop.py')],
                capture_output=True, text=True, timeout=120
            )
        except Exception:
            pass
        report = {}
        if report_file.exists():
            try:
                report = json.loads(report_file.read_text(encoding='utf-8'))
            except Exception:
                pass
        self._set_headers(200, 'application/json')
        self.wfile.write(json.dumps({
            'ok': bool(report),
            'dna': '#龍芯⚡️2026-06-28-LONGHUN-AUDIT-API-v1.0',
            'report': report,
        }, ensure_ascii=False).encode())

    def _serve_auth_level(self):
        try:
            body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
            data = json.loads(body.decode('utf-8')) if body else {}
        except Exception:
            data = {}
        factors = data.get('factors', [])
        score = min(7, max(0, len(factors)))
        if score == 0:
            level = 'visitor'
        elif score <= 2:
            level = 'citizen'
        elif score <= 4:
            level = 'developer'
        elif score <= 6:
            level = 'maintainer'
        else:
            level = 'guardian'
        feature_map = {
            'visitor': ['浏览公开文档', '查看模型广场'],
            'citizen': ['加入公开聊天室', '广场评论/点赞', '提交问题反馈'],
            'developer': ['调用 API / MCP', '下载 SDK', '提交 Pull Request', '使用开发者沙盒'],
            'maintainer': ['审核代码', '管理仓库权限', '查看审计日志', '发起补丁投票'],
            'guardian': ['参与治理提案', '授权仲裁', '运行监督节点', '发起公投'],
        }
        self._set_headers(200, 'application/json')
        self.wfile.write(json.dumps({
            'ok': True,
            'dna': '#龍芯⚡️2026-06-28-LONGHUN-7FACTOR-AUTH-API-v1.0',
            'score': score,
            'level': level,
            'features': feature_map.get(level, []),
        }, ensure_ascii=False).encode())

    def _send_text(self, rc, out, err):
        self._set_headers(200 if rc == 0 else 500, 'application/json')
        response = {
            'ok': rc == 0,
            'stdout': out,
            'stderr': err,
        }
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode())

    def log_message(self, format, *args):
        # 简化日志，不输出到 stderr
        pass


def main():
    server = HTTPServer((HOST, PORT), CORSRequestHandler)
    print(f"🐉 龍魂指挥调度 Web 桥接服务已启动: http://{HOST}:{PORT}")
    print(f"🧬 DNA: #龍芯⚡️2026-06-28-LONGHUN-COMMANDER-WEB-BRIDGE-v1.0")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止")


if __name__ == '__main__':
    main()
