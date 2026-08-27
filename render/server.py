# DNA: #龍芯⚡️2026-08-25-RENDER-ENV-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""M75 渲染服务 · FastAPI REST (:8972) · 默认只绑 127.0.0.1（主权边界）。
原 :8766 与主权网关冲突（lh_sovereign_gateway.py 焊死占用），2026-08-25 迁至 :8972。"""

import argparse
import base64
import os
import threading

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

from .orchestrator import LHRenderOrchestrator


def _sanitize(obj):
    """递归清洗：bytes → data URL(base64)，保证 JSON 可序列化。"""
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_sanitize(v) for v in obj]
    if isinstance(obj, bytes):
        try:
            return "data:image/png;base64," + base64.b64encode(obj).decode()
        except Exception:
            return base64.b64encode(obj).decode()
    return obj

app = FastAPI(title="龍魂渲染服务 · M75", version="1.0.0")
_engine = LHRenderOrchestrator()
_lock = threading.Lock()


class RenderRequest(BaseModel):
    command: str


class BatchRequest(BaseModel):
    urls: list = []
    concurrency: int = 4
    interval: float = 0.5


@app.get("/render/health")
def health():
    return {"status": "healthy", "platform": "arm64" if os.uname().machine == "aarch64" else "local",
            "version": LHRenderOrchestrator.VERSION}


@app.get("/render/status")
def status():
    return _engine.status()


@app.post("/render/execute")
def execute(req: RenderRequest):
    with _lock:
        result = _engine.execute(req.command)
    if result["status"] in ("blocked",):
        return JSONResponse(_sanitize(result), status_code=403)
    if result["status"] == "error":
        return JSONResponse(_sanitize(result), status_code=400)
    return _sanitize(result)


@app.post("/render/batch")
def batch(req: BatchRequest):
    with _lock:
        results = _engine.batch(req.urls, req.concurrency, req.interval)
    return _sanitize({"status": "ok", "results": results})


def main():
    parser = argparse.ArgumentParser(prog="lh render server", description="M75 渲染服务")
    parser.add_argument("--host", default="127.0.0.1", help="绑定地址（默认 127.0.0.1 主权边界）")
    parser.add_argument("--port", type=int, default=8972)
    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")


if __name__ == "__main__":
    main()
