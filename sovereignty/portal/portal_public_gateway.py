# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂数字身份公开网关 · 安全暴露入口 v1.0

作用：
  让国家数字身份认证入口（:8444）可以安全地给公网陌生人使用，
  但把“签发身份”等敏感接口锁死，只允许本机或带管理令牌调用。

核心规则：
  ✅ 公开：网页、主权宣言、/verify 验证、/api/info、/health
  🔒 受限：/issue（签发）、/register（服务商注册）等只能本机或管理员访问
  🔴 其他路径默认拒绝，防止把内部 AI/知识库接口误暴露

部署建议：
  1. 身份入口本身只监听 127.0.0.1:8444（不要直接绑 0.0.0.0）
  2. 本网关监听 0.0.0.0:8443
  3. Nginx / Caddy 反代域名 443 → 8443，并配 HTTPS

DNA: #龍芯⚡️2026-06-25-LONGHUN-PORTAL-PUBLIC-GATEWAY-v1.0
"""

import os
import json
import http.client
from http.server import BaseHTTPRequestHandler, HTTPServer

# 上游：国家数字身份入口
TARGET_HOST = os.getenv("PORTAL_TARGET_HOST", "127.0.0.1")
TARGET_PORT = int(os.getenv("PORTAL_TARGET_PORT", "8444"))

# 网关监听端口
GATEWAY_PORT = int(os.getenv("PORTAL_GATEWAY_PORT", "8443"))

# 管理令牌：如果设了，外网带对 X-LongHun-Admin-Token 也能调用受限接口
# 建议用随机字符串：python3 -c "import secrets; print(secrets.token_hex(32))"
ADMIN_TOKEN = os.getenv("PORTAL_ADMIN_TOKEN", "")

# 公开路径（任何人可访问）
PUBLIC_PATHS = {
    "/",
    "/developer.html",
    "/health",
    "/api/info",
    "/api/docs",
}

# 公开前缀
PUBLIC_PREFIXES = (
    "/static/",
)


class PortalGatewayHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[PORTAL-GW:{GATEWAY_PORT}] {self.address_string()} - {format % args}")

    def _remote_ip(self):
        return self.client_address[0]

    def _is_local(self):
        return self._remote_ip() in ("127.0.0.1", "::1")

    def _has_admin_token(self):
        if not ADMIN_TOKEN:
            return False
        return self.headers.get("X-LongHun-Admin-Token") == ADMIN_TOKEN

    def _is_authorized(self):
        """本机或持有管理令牌视为授权"""
        return self._is_local() or self._has_admin_token()

    def _is_public_path(self):
        p = self.path
        if p in PUBLIC_PATHS:
            return True
        for prefix in PUBLIC_PREFIXES:
            if p.startswith(prefix):
                return True
        return False

    def _send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _proxy(self, method):
        # 安全检查
        if not self._is_public_path() and not self._is_authorized():
            self._send_json(403, {
                "error": "该接口不对外公开",
                "note": "如需管理，请从本机访问或携带 X-LongHun-Admin-Token",
                "tricolor": "🔴",
                "dna": "#龍芯⚡️20260625-GATEWAY-FORBIDDEN"
            })
            return

        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length) if content_length > 0 else None

            conn = http.client.HTTPConnection(TARGET_HOST, TARGET_PORT, timeout=15)
            headers = {k: v for k, v in self.headers.items() if k.lower() != "host"}
            conn.request(method, self.path, body=body, headers=headers)
            resp = conn.getresponse()
            resp_body = resp.read()

            self.send_response(resp.status)
            for k, v in resp.getheaders():
                kl = k.lower()
                if kl in ("transfer-encoding", "content-length"):
                    continue
                self.send_header(k, v)
            self.send_header("Content-Length", str(len(resp_body)))
            self.end_headers()
            self.wfile.write(resp_body)
            conn.close()
        except Exception as e:
            self._send_json(502, {
                "error": "上游身份入口不可用",
                "detail": str(e),
                "tricolor": "🔴"
            })

    def do_GET(self):
        if self.path == "/health":
            self._send_json(200, {
                "status": "ok",
                "gateway": "longhun-portal-public-gateway",
                "upstream": f"http://{TARGET_HOST}:{TARGET_PORT}",
                "public_paths": list(PUBLIC_PATHS),
                "dna": "#龍芯⚡️2026-06-25-LONGHUN-PORTAL-PUBLIC-GATEWAY-v1.0"
            })
            return
        self._proxy("GET")

    def do_HEAD(self):
        self._proxy("HEAD")

    def do_POST(self):
        self._proxy("POST")

    def do_PUT(self):
        self._proxy("PUT")

    def do_DELETE(self):
        self._proxy("DELETE")


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", GATEWAY_PORT), PortalGatewayHandler)
    print("🐉 龍魂数字身份公开网关已启动")
    print(f"   监听: http://0.0.0.0:{GATEWAY_PORT}")
    print(f"   上游: http://{TARGET_HOST}:{TARGET_PORT}")
    print(f"   管理令牌: {'已启用' if ADMIN_TOKEN else '未启用（仅本机可调受限接口）'}")
    print(f"   DNA: #龍芯⚡️2026-06-25-LONGHUN-PORTAL-PUBLIC-GATEWAY-v1.0")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[PORTAL-GW] 已停止")
