#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 龍魂 ollama Host 头反代 v1.0
# DNA: #龍芯⚡️2026-08-25-OLLAMA-HOST-PROXY-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 作用: 隧道 ollama.longhun888.com → 127.0.0.1:11435 → 转发 127.0.0.1:11434
#       发往上游时 Host 头自动为 127.0.0.1:11434，绕开 ollama DNS-rebinding 防护(403)
# 支持: 流式 SSE（/api/generate /api/chat 的 stream 模式）
"""使用: python3 tools/ollama_host_proxy.py [listen_port] [upstream_port]"""

import http.server
import http.client
import sys

LISTEN_HOST = "127.0.0.1"
UPSTREAM_HOST = "127.0.0.1"
LISTEN_PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 11435
UPSTREAM_PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 11434

SKIP_REQ_HEADERS = {"host", "content-length", "connection", "transfer-encoding", "accept-encoding"}
SKIP_RES_HEADERS = {"transfer-encoding", "connection", "content-length"}


class ProxyHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _proxy(self):
        try:
            length = int(self.headers.get("Content-Length", 0) or 0)
            body = self.rfile.read(length) if length else None

            headers = {k: v for k, v in self.headers.items() if k.lower() not in SKIP_REQ_HEADERS}
            conn = http.client.HTTPConnection(UPSTREAM_HOST, UPSTREAM_PORT, timeout=600)
            conn.request(self.command, self.path, body=body, headers=headers)
            resp = conn.getresponse()

            self.send_response(resp.status, resp.reason)
            for k, v in resp.getheaders():
                if k.lower() not in SKIP_RES_HEADERS:
                    self.send_header(k, v)
            if resp.chunked:
                self.send_header("Transfer-Encoding", "chunked")
            else:
                self.send_header("Content-Length", str(resp.length))
            self.end_headers()

            # 流式转发（chunked SSE）
            if resp.chunked:
                while True:
                    line = resp.fp.readline()
                    if line == b"":
                        break
                    self.wfile.write(line)
                    size = int(line.strip().split(b";")[0], 16)
                    if size == 0:
                        self.wfile.write(resp.fp.readline())
                        break
                    self.wfile.write(resp.fp.read(size))
                    self.wfile.write(resp.fp.readline())
            else:
                remaining = resp.length
                while remaining > 0:
                    data = resp.read(min(65536, remaining))
                    if not data:
                        break
                    self.wfile.write(data)
                    remaining -= len(data)
            self.wfile.flush()
            conn.close()
        except Exception as e:
            try:
                self.send_response(502)
                self.end_headers()
                self.wfile.write(str(e).encode())
            except Exception:
                pass

    do_GET = do_POST = do_PUT = do_DELETE = do_HEAD = do_OPTIONS = do_PATCH = _proxy

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    srv = http.server.ThreadingHTTPServer((LISTEN_HOST, LISTEN_PORT), ProxyHandler)
    print(f"🟢 ollama Host 反代 {LISTEN_HOST}:{LISTEN_PORT} → {UPSTREAM_HOST}:{UPSTREAM_PORT}")
    srv.serve_forever()
