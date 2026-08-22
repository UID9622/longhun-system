#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════
# 龍魂硬核创作库 · 公开只读 API（零三方依赖·http.server）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 部署: 鲲鹏 uid9622.cn → /api/v1/creations* （nginx 反代 127.0.0.1:8767）
# DNA: #龍芯⚡️丙午·丙申·癸亥·戊午·䷚颐-CREATIONS-API-v1.0-UID9622
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ═══════════════════════════════════════════════════════════
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse, unquote

PORT = int(os.environ.get("CREATIONS_API_PORT", "8767"))
PROJECT_ROOT = Path(os.environ.get("LH_ROOT", "/opt/longhun-system"))
CREATIONS_DIR = PROJECT_ROOT / "portal" / "creations"
INDEX_FILE = PROJECT_ROOT / "portal" / "data" / "creations_index.json"

CORS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "*",
}


def load_index() -> dict:
    if not INDEX_FILE.exists():
        return {"creations": [], "meta": {}}
    try:
        return json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {"creations": [], "meta": {}}


def safe_slug(slug: str):
    if not slug or "/" in slug or "\\" in slug or ".." in slug:
        return None
    return slug


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        for k, v in CORS.items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        for k, v in CORS.items():
            self.send_header(k, v)
        self.end_headers()

    def do_GET(self):
        path = unquote(urlparse(self.path).path)
        # GET /api/v1/creations （兼容尾部斜杠）
        if path in ("/api/v1/creations", "/api/v1/creations/", "/v1/creations", "/v1/creations/"):
            data = load_index()
            creations = data.get("creations", [])
            return self._send(200, {
                "ok": True,
                "count": len(creations),
                "meta": data.get("meta", {}),
                "creations": creations,
            })
        # GET /api/v1/creations/{slug}
        prefix = "/api/v1/creations/"
        if path.startswith(prefix):
            slug = safe_slug(path[len(prefix):])
            if not slug:
                return self._send(400, {"ok": False, "error": "无效的创作标识"})
            data = load_index()
            creation = next((c for c in data.get("creations", []) if c.get("slug") == slug), None)
            if not creation:
                return self._send(404, {"ok": False, "error": "创作 %s 不存在" % slug})
            md = PROJECT_ROOT / creation.get("path", "")
            content = md.read_text(encoding="utf-8") if md.exists() else ""
            return self._send(200, {"ok": True, "creation": dict(creation, content=content)})
        # health
        if path in ("/health", "/api/v1/creations/health"):
            return self._send(200, {"ok": True, "service": "creations-api", "creations_dir": str(CREATIONS_DIR)})
        return self._send(404, {"ok": False, "error": "not found"})

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    CREATIONS_DIR.mkdir(parents=True, exist_ok=True)
    print("🐉 龍魂创作库API v1.0 → :%s | dir=%s" % (PORT, CREATIONS_DIR))
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
