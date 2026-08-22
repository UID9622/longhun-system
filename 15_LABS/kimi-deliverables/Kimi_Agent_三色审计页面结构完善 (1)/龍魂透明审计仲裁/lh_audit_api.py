# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-a93a3393
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""🐉 透明仲裁 FastAPI 服务壳（P1设计选型落地）
启动: python3 lh_audit_api.py  →  http://127.0.0.1:8970
端点:
  POST /audit   {question, engines?}  → 全链路报告(仲裁+摘要+归档+R值)
  GET  /chain/verify                  → 年轮链完整性
  GET  /health                        → 健康检查
FastAPI缺失时自动降级 stdlib http.server（断网可跑铁律）。
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
import asyncio, json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from transparent_audit_v2 import 全链路路由器, 本地龍魂引擎, 模拟云端引擎

默认引擎 = [本地龍魂引擎(),
          模拟云端引擎("kimi", "用户数据应保存于云端服务器，数据主权归用户所有。操作记录写入区块链。"),
          模拟云端引擎("deepseek", "用户数据应存储于本地终端，数据主权归属国家法律。操作记录存档于数据库。")]
路由器 = 全链路路由器(默认引擎, 超时=3.0)

def _清理(报告):
    r = dict(报告)
    if r.get("仲裁"):
        a = dict(r["仲裁"]); a.pop("_normed", None); a.pop("similarity_auxiliary", None)
        r["仲裁"] = a
    r.pop("回答", None)
    return r

try:
    from fastapi import FastAPI
    from pydantic import BaseModel
    import uvicorn

    app = FastAPI(title="龍魂·透明仲裁 API", version="2.0")

    class Q(BaseModel):
        question: str

    @app.post("/audit")
    async def audit(q: Q):
        return _清理(await 路由器.路由(q.question))

    @app.get("/chain/verify")
    def verify():
        return 路由器.史官.验链()

    @app.get("/health")
    def health():
        return {"status": "🟢", "engines": len(默认引擎)}

    if __name__ == "__main__":
        uvicorn.run(app, host="127.0.0.1", port=8970)

except ImportError:
    from http.server import HTTPServer, BaseHTTPRequestHandler

    class H(BaseHTTPRequestHandler):
        def _j(self, obj, code=200):
            b = json.dumps(obj, ensure_ascii=False).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers(); self.wfile.write(b)
        def do_GET(self):
            if self.path == "/health": self._j({"status": "🟢", "engines": len(默认引擎)})
            elif self.path == "/chain/verify": self._j(路由器.史官.验链())
            else: self._j({"error": "not found"}, 404)
        def do_POST(self):
            if self.path == "/audit":
                n = int(self.headers.get("Content-Length", 0))
                q = json.loads(self.rfile.read(n) or b"{}").get("question", "")
                self._j(_清理(asyncio.run(路由器.路由(q))))
            else: self._j({"error": "not found"}, 404)
        def log_message(self, *a): pass

    if __name__ == "__main__":
        print("⚠️ FastAPI未安装，降级stdlib模式 → http://127.0.0.1:8970")
        HTTPServer(("127.0.0.1", 8970), H).serve_forever()
