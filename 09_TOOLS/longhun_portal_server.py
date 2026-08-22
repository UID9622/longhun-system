#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂门户本地预览服务器 · 模拟 Nginx 代理
DNA: #龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-LONGHUN-PORTAL-SERVER-v1.0

行为：
  - 静态文件服务：portal/ 目录
  - 代理 /editor/* /docs* /openapi.json /static/* /api/v1/* → 127.0.0.1:18000
  - 默认端口 8777（与 README 一致）

启动：
  cd ~/longhun-system/portal
  python3 ../tools/longhun_portal_server.py
"""
from __future__ import annotations

import os
import sys
import urllib.parse
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PORT = int(os.environ.get("PORTAL_PORT", "8777"))
CNSH_API = os.environ.get("CNSH_API_URL", "http://127.0.0.1:18000")
PORTAL_ROOT = Path(__file__).resolve().parent.parent / "portal"
WEB_ROOT = Path(__file__).resolve().parent.parent / "web"
PAPERS_ROOT = Path(__file__).resolve().parent.parent / "papers"

PROXY_PREFIXES = ("/editor/", "/openapi.json", "/static/", "/api/v1/")
# /docs 精确代理到 Swagger UI；/docs/ 子路径优先尝试本地静态文件
SWAGGER_PATHS = ("/docs", "/docs/")


class Handler(SimpleHTTPRequestHandler):
    def _redirect(self, location: str, code: int = 302):
        self.send_response(code)
        # HTTP 头必须是 latin-1，中文路径需先 URL 编码
        safe_location = urllib.parse.quote(location, safe="/%")
        self.send_header("Location", safe_location)
        self.end_headers()

    def translate_path(self, path: str) -> str:
        # URL 解码 + 去掉查询参数
        decoded = urllib.parse.unquote(path).split("?")[0]
        # 1. CNSH API / editor / docs / static 仍走 portal 根或代理
        if decoded.startswith(PROXY_PREFIXES):
            return str(PORTAL_ROOT / decoded.lstrip("/"))
        # 2. /web/ 路径映射到 web/ 目录
        if decoded.startswith("/web/"):
            return str(WEB_ROOT / decoded[len("/web/"):].lstrip("/"))
        # 3. /portal/ 路径也映射到 portal/ 目录（兼容控制台相对路径）
        if decoded.startswith("/portal/"):
            return str(PORTAL_ROOT / decoded[len("/portal/"):].lstrip("/"))
        # 4. /papers/ 路径映射到 papers/ 目录
        if decoded.startswith("/papers/"):
            return str(PAPERS_ROOT / decoded[len("/papers/"):].lstrip("/"))
        # 5. 默认 portal 目录
        return str(PORTAL_ROOT / decoded.lstrip("/"))

    def _serve_file(self, file_path: Path):
        if not file_path.exists() or not file_path.is_file():
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")
            return
        self.send_response(200)
        # 简单 MIME
        suffix = file_path.suffix.lower()
        mime = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css",
            ".js": "application/javascript",
            ".json": "application/json",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".svg": "image/svg+xml",
            ".md": "text/markdown; charset=utf-8",
        }.get(suffix, "application/octet-stream")
        self.send_header("Content-Type", mime)
        # JSON 数据文件禁用缓存，避免配置更新后客户端仍用旧数据
        if suffix == ".json":
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
            self.send_header("Pragma", "no-cache")
        self.end_headers()
        if self.command != "HEAD":
            with open(file_path, "rb") as f:
                self.wfile.write(f.read())

    def _proxy(self, target_url: str):
        try:
            req = urllib.request.Request(
                target_url,
                headers={"Accept": self.headers.get("Accept", "*/*")},
                method=self.command,
            )
            # 转发请求体（POST/PUT）
            content_length = self.headers.get("Content-Length")
            if content_length:
                body = self.rfile.read(int(content_length))
                req.add_header("Content-Length", content_length)
                if self.headers.get("Content-Type"):
                    req.add_header("Content-Type", self.headers.get("Content-Type"))
            else:
                body = None

            with urllib.request.urlopen(req, data=body, timeout=30) as resp:
                self.send_response(resp.status)
                for k, v in resp.headers.items():
                    if k.lower() not in ("transfer-encoding", "content-encoding", "connection"):
                        self.send_header(k, v)
                self.end_headers()
                self.wfile.write(resp.read())
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            self.send_response(502)
            self.end_headers()
            self.wfile.write(f"Proxy error: {e}".encode())

    def _is_proxy_path(self, path: str) -> bool:
        decoded = urllib.parse.unquote(path.split("?")[0])
        if decoded in SWAGGER_PATHS:
            return True
        return path.startswith(PROXY_PREFIXES)

    def do_GET(self):
        path = urllib.parse.unquote(self.path.split("?")[0])
        # 控制台快捷入口
        if path in ("/console", "/console/"):
            self._redirect("/web/CNSH_龍魂操作台v4.0.html")
            return
        # /docs/ 子路径若存在本地静态文件则优先服务（避免与 Swagger 精确路径冲突）
        if path.startswith("/docs/"):
            file_path = Path(self.translate_path(self.path))
            if file_path.is_file():
                self._serve_file(file_path)
                return
        if self._is_proxy_path(self.path):
            self._proxy(f"{CNSH_API}{self.path}")
            return
        # 静态文件统一走 _serve_file，确保 JSON 等数据文件带缓存控制头
        file_path = Path(self.translate_path(self.path))
        if file_path.is_file():
            self._serve_file(file_path)
            return
        super().do_GET()

    def do_HEAD(self):
        path = urllib.parse.unquote(self.path.split("?")[0])
        if path in ("/console", "/console/"):
            self._redirect("/web/CNSH_龍魂操作台v4.0.html")
            return
        if path.startswith("/docs/"):
            file_path = Path(self.translate_path(self.path))
            if file_path.is_file():
                self._serve_file(file_path)
                return
        if self._is_proxy_path(self.path):
            self.send_response(200)
            self.end_headers()
            return
        file_path = Path(self.translate_path(self.path))
        if file_path.is_file():
            self._serve_file(file_path)
            return
        super().do_HEAD()

    def do_POST(self):
        if self._is_proxy_path(self.path):
            self._proxy(f"{CNSH_API}{self.path}")
            return
        super().do_POST()

    def log_message(self, fmt, *args):
        sys.stderr.write(f"[{self.log_date_time_string()}] {fmt % args}\n")


if __name__ == "__main__":
    print(f"🐉 龍魂门户服务器 · http://127.0.0.1:{PORT}")
    print(f"   静态根目录: {PORTAL_ROOT}")
    print(f"   CNSH API 代理: {CNSH_API}")
    print(f"   DNA: #龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-LONGHUN-PORTAL-SERVER-v1.0")
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止")
