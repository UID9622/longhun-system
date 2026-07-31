# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·DNA生成与验证API v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-DNA-API-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
端口: 8783

端点:
  POST /dna/generate       — 生成DNA追溯码+双标识
  POST /dna/verify         — 验证文本DNA
  GET  /dna/trace/{code}   — 追溯DNA链路
  GET  /dna/stats          — 生成/验证统计
  POST /dna/verify-url     — 验证在线内容
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
import uvicorn

SYSTEM_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SYSTEM_ROOT))

from engines.lh_dual_labeler import get_labeler
from bin.lh_dna_verifier import DNAVerifier
from bin.lh_dna_generator import generate_dna, compute_full_dna

app = FastAPI(
    title="龍魂·DNA生成与验证 API",
    version="v1.0",
    description="给所有AI内容打上不可伪造的出生证明",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

labeler = get_labeler()
verifier = DNAVerifier()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 请求模型
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class GenerateRequest(BaseModel):
    text: str = Field(..., description="AI生成的原始内容")
    model_name: str = Field("CodeBuddy", description="模型名称")
    model_version: str = Field("v1.0", description="模型版本")
    user_id: str = Field("UID9622", description="用户ID（脱敏）")
    action: str = Field("GENERATE", description="动作标签")
    parent_dna: str = Field("", description="父级DNA（如果基于其他AI内容生成）")
    extra_meta: Optional[dict] = Field(None, description="额外元数据")


class VerifyRequest(BaseModel):
    text: str = Field(..., description="待验证文本")


class VerifyUrlRequest(BaseModel):
    url: str = Field(..., description="待验证URL")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# API 端点
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.post("/dna/generate")
async def generate(req: GenerateRequest):
    """为AI生成内容生成DNA追溯码和双标识"""
    # 用传入参数生成DNA
    dna_code = compute_full_dna(
        action=req.action,
        version=f"{req.model_name}-{req.model_version}",
        text=req.text,
    )

    # 嵌入双标识
    labeled_text = labeler.embed(
        req.text,
        dna_code,
        model=f"{req.model_name}-{req.model_version}",
        user=req.user_id,
        extra_meta=req.extra_meta,
    )

    # 内容哈希
    import hashlib
    content_hash = hashlib.sha256(req.text.encode()).hexdigest()[:16]

    return {
        "status": "ok",
        "dna_code": dna_code,
        "labeled_text": labeled_text,
        "content_hash": content_hash,
        "has_visible": True,
        "has_invisible": True,
        "parent_dna": req.parent_dna if req.parent_dna else None,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/dna/verify")
async def verify(req: VerifyRequest):
    """验证文本的DNA完整性和真实性"""
    result = verifier.verify_text(req.text, source="api")
    return result


@app.post("/dna/verify-url")
async def verify_url(req: VerifyUrlRequest):
    """验证在线内容的DNA"""
    result = verifier.verify_url(req.url)
    if "error" in result:
        raise HTTPException(400, result["error"])
    return result


@app.get("/dna/trace/{dna_code:path}")
async def trace(dna_code: str):
    """根据DNA码追溯生成链路"""
    result = verifier.trace(dna_code)
    return result


@app.get("/dna/stats")
async def stats():
    """DNA生成/验证统计"""
    return verifier.stats()


@app.get("/dna/health")
async def health():
    return {
        "status": "ok",
        "service": "dna-api",
        "port": 8783,
        "time": datetime.now(timezone.utc).isoformat(),
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 仪表盘
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.get("/dna/dashboard", response_class=HTMLResponse)
async def dashboard():
    dashboard_file = SYSTEM_ROOT / "portal" / "dna-identity" / "index.html"
    if dashboard_file.exists():
        return dashboard_file.read_text(encoding="utf-8")
    return HTMLResponse("<h1>DNA仪表盘未找到</h1>", status_code=404)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 启动
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="DNA生成与验证API")
    parser.add_argument("--port", type=int, default=8783)
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()

    print(f"🧬 DNA生成与验证API 启动 :{args.port}")
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")
