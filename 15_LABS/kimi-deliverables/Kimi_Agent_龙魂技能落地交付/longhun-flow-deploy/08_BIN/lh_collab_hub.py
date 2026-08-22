#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#龍芯⚡️丙午·丙申·己未·乙亥时·䷞旅-COLLAB-HUB-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# SPDX-License-Identifier: MulanPSL-2.0
"""
🐉 龍魂 · 协作中枢 v1.0
端口: 19622 (仅绑定 127.0.0.1)
对外路径: nginx /collab/api/* → 本服务 /* (修正8 双路由)
契约: GET /health → {"status":"ok","service":"collab-hub","dna":...}
      其余路径无 X-Dragon-DNA → 403 {"error":"P0协议要求: 缺少DNA追溯码"}
"""

import os
from datetime import datetime
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from lh_audit import CONFIRM, Historian, generate_dna, require_dna

SERVICE = "collab-hub"
SHARED_ROOT = Path(os.environ.get("LONGHUN_SHARED_ROOT", "/opt/longhun/shared"))

app = FastAPI(title="龍魂协作中枢", version="1.0.0")


@app.middleware("http")
async def p0_audit_middleware(request: Request, call_next):
    path = request.url.path
    if path == "/health":
        return await call_next(request)
    dna = require_dna(request.headers, SERVICE, path)
    if not dna:
        return JSONResponse(status_code=403,
                            content={"error": "P0协议要求: 缺少DNA追溯码"})
    response = await call_next(request)
    Historian.record("collab_request", dna, {
        "path": path, "method": request.method, "status": response.status_code,
    }, service=SERVICE)
    return response


@app.get("/health")
async def health():
    return {"status": "ok", "service": SERVICE, "dna": generate_dna("HEALTH")}


@app.get("/list")
async def list_files():
    """列出共享文件 (collab / handoffs / collaboration)。"""
    if not SHARED_ROOT.exists():
        return {"files": [], "dna": generate_dna("LIST")}
    files = []
    for f in SHARED_ROOT.rglob("*"):
        if f.is_file():
            st = f.stat()
            files.append({
                "name": f.name,
                "path": str(f.relative_to(SHARED_ROOT)),
                "size": st.st_size,
                "mtime": st.st_mtime,
            })
    return {"files": files, "count": len(files), "dna": generate_dna("LIST")}


@app.get("/status")
async def status():
    return {
        "service": SERVICE,
        "shared_root": str(SHARED_ROOT),
        "shared_root_exists": SHARED_ROOT.exists(),
        "timestamp": datetime.now().isoformat(),
        "confirm": CONFIRM,
        "dna": generate_dna("STATUS"),
    }


if __name__ == "__main__":
    try:
        SHARED_ROOT.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print(f"🟡 警告: 无法创建 {SHARED_ROOT} (deploy.sh 会以 root 创建), 以只读降级启动")
    uvicorn.run(app, host="127.0.0.1", port=19622)
