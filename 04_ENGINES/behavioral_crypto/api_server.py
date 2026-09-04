#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂·行為密碼學主權API服務器 v2.0
DNA: #龍芯⚡️丙午·甲申·丁酉·丙午·䷳艮-BCM-API-V2.0-UID9622
License: MulanPSL v2

REST API 端點:
  POST /api/v2/bcm/extract      — 提取七因子行為指紋
  POST /api/v2/bcm/verify        — 驗證行為指紋
  GET  /api/v2/bcm/experiment    — 運行實驗（異步）
  GET  /api/v2/bcm/status        — 引擎狀態
  GET  /api/v2/bcm/sovereignty   — 主權驗證信息

每個響應攜帶:
  - X-LongHun-DNA: 請求追溯碼
  - X-LongHun-Audit: 三色審計標記
  - X-LongHun-Sovereignty: 主權簽名
  - X-LongHun-Timestamp: 時間戳

啟動: uvicorn 04_ENGINES.behavioral_crypto.api_server:app --host 0.0.0.0 --port 8775
"""

import hashlib
import json
import time
import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, List

from fastapi import FastAPI, HTTPException, Request, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse, StreamingResponse
from pydantic import BaseModel, Field
import asyncio

import sys
import os

# 確保專案根和 04_ENGINES 在路徑中
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _project_root)
sys.path.insert(0, os.path.join(_project_root, "04_ENGINES"))

from behavioral_crypto.seven_factor_model import (
    SevenFactorEngine,
    quick_fingerprint,
    verify_fingerprint,
    SOVEREIGN_ANCHOR,
    FACTOR_DEFINITIONS,
)
from behavioral_crypto.experiment_runner import (
    ExperimentRunner,
    ATTACK_LEVELS,
    CORPUS_TYPES,
)
from behavioral_crypto.visualizer import Visualizer

# ============================================================
# API 配置
# ============================================================
API_TITLE = "龍魂·行為密碼學主權API"
API_VERSION = "2.0.0"
API_PORT = 8775

app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    docs_url="/api/v2/bcm/docs",
    redoc_url="/api/v2/bcm/redoc",
    openapi_url="/api/v2/bcm/openapi.json",
)

# CORS（只允許境內和本地）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://uid9622.cn", "http://localhost:*", "http://127.0.0.1:*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*", "X-LongHun-DNA", "X-LongHun-Audit", "X-LongHun-Sovereignty"],
)
app.add_middleware(GZipMiddleware, minimum_size=500)

# 全局引擎實例
engine = SevenFactorEngine()
experiment_runner: Optional[ExperimentRunner] = None
latest_experiment_summary: Optional[Dict] = None


# ============================================================
# Pydantic 模型
# ============================================================

class ExtractRequest(BaseModel):
    text: str = Field(..., description="待提取指紋的文本", min_length=10)
    author_id: str = Field(default="UID9622", description="作者ID")
    update_profile: bool = Field(default=False, description="是否更新作者畫像")

class VerifyRequest(BaseModel):
    text: str = Field(..., description="待验证的文本", min_length=10)
    author_id: str = Field(default="UID9622", description="作者ID")
    threshold: float = Field(default=0.30, ge=0.0, le=1.0, description="驗證閾值")

class ExperimentRequest(BaseModel):
    num_docs: int = Field(default=50, ge=10, le=500, description="文檔數量")
    seed: int = Field(default=42, ge=0, description="隨機種子")


# ============================================================
# 主權中間件
# ============================================================

@app.middleware("http")
async def sovereignty_middleware(request: Request, call_next):
    """所有響應注入主權標頭"""
    request_dna = request.headers.get("X-LongHun-DNA", "")
    request_id = str(uuid.uuid4())[:8]
    
    # 生成請求 DNA（ASCII-safe for HTTP headers）
    ts = datetime.now(timezone.utc)
    dna_ascii = f"LongHun-BCM-API-{ts.strftime('%Y%m%d')}-{request_id}"
    
    # 調用
    response = await call_next(request)
    
    # 注入主權標頭（ASCII-safe）
    response.headers["X-LongHun-DNA"] = dna_ascii
    response.headers["X-LongHun-Sovereignty"] = "LONGHUN-CONFIRM-9622"
    response.headers["X-LongHun-Timestamp"] = ts.isoformat()
    response.headers["X-LongHun-Jurisdiction"] = "CN"
    response.headers["X-LongHun-Encryption"] = "SM3-SM4"
    response.headers["Access-Control-Expose-Headers"] = (
        "X-LongHun-DNA, X-LongHun-Audit, X-LongHun-Sovereignty, "
        "X-LongHun-Timestamp, X-LongHun-Jurisdiction, X-LongHun-Encryption"
    )
    
    return response


# ============================================================
# API 端點
# ============================================================

@app.get("/api/v2/bcm/health")
async def health_check():
    """健康檢查"""
    return {
        "status": "healthy",
        "service": "behavioral-crypto",
        "version": API_VERSION,
        "engine_status": "active",
        "total_extractions": len(engine.extraction_log),
        "sovereignty": "CN",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/v2/bcm/status")
async def engine_status():
    """引擎狀態詳情"""
    return {
        "service": "behavioral-crypto-v2",
        "version": API_VERSION,
        "engine": engine.get_stats(),
        "factor_definitions": {
            fid: {"name": f["name"], "weight": f["weight"], "forge_difficulty": f["forge_difficulty"]}
            for fid, f in FACTOR_DEFINITIONS.items()
        },
        "attack_levels": {
            level: {"name": a["name"], "expected_retention": a["expected_retention"]}
            for level, a in ATTACK_LEVELS.items()
        },
        "sovereignty": SOVEREIGN_ANCHOR,
    }


@app.get("/api/v2/bcm/sovereignty")
async def sovereignty_info():
    """主權驗證信息"""
    return {
        "service": "behavioral-crypto",
        "owner": SOVEREIGN_ANCHOR["owner"],
        "uid": SOVEREIGN_ANCHOR["uid"],
        "gpg": SOVEREIGN_ANCHOR["gpg"],
        "confirm": SOVEREIGN_ANCHOR["confirm"],
        "jurisdiction": SOVEREIGN_ANCHOR["jurisdiction"],
        "encryption": SOVEREIGN_ANCHOR["encryption"],
        "license_engineering": "MulanPSL v2",
        "license_thought": "CC BY-NC-SA 4.0",
        "data_policy": "境內存儲·端側加密·雲上密文·不出境",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/api/v2/bcm/extract")
async def extract_fingerprint(req: ExtractRequest):
    """
    提取七因子行為指紋
    
    成功響應: {dna, composite_score, audit_mark, factors: [...]}
    """
    try:
        if req.update_profile:
            engine.update_author_profile(req.author_id, req.text)
        
        fp = engine.extract(req.text, req.author_id)
        result = fp.to_dict()
        
        # 審計標記（ASCII-safe for header）
        audit = fp.audit_mark
        audit_ascii = "GREEN" if audit == "🟢" else "YELLOW" if audit == "🟡" else "RED"
        
        return JSONResponse(
            content=result,
            headers={"X-LongHun-Audit": audit_ascii},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"提取失敗: {str(e)}")


@app.post("/api/v2/bcm/verify")
async def verify_fingerprint_endpoint(req: VerifyRequest):
    """
    驗證行為指紋
    
    響應: {verified: bool, score, threshold, warnings, recommendation}
    """
    try:
        fp_dict = quick_fingerprint(req.text, req.author_id)
        result = verify_fingerprint(fp_dict, req.threshold)
        result["fingerprint"] = fp_dict
        result["sovereignty"] = SOVEREIGN_ANCHOR
        
        audit = "GREEN" if result["verified"] else "YELLOW"
        
        return JSONResponse(
            content=result,
            headers={"X-LongHun-Audit": audit},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"驗證失敗: {str(e)}")


@app.get("/api/v2/bcm/experiment/run")
async def run_experiment(
    num_docs: int = Query(default=50, ge=10, le=500),
    seed: int = Query(default=42, ge=0),
):
    """
    異步運行攻擊模擬實驗
    
    響應: {experiment_id, summary: {...}}
    結果緩存到 latest_experiment_summary
    """
    global experiment_runner, latest_experiment_summary
    
    experiment_runner = ExperimentRunner(num_docs=num_docs, seed=seed)
    
    # 在線程池中運行
    loop = asyncio.get_event_loop()
    results = await loop.run_in_executor(None, experiment_runner.run_full_experiment)
    summary = experiment_runner.generate_summary()
    
    latest_experiment_summary = {"summary": summary, "results": results}
    
    return {
        "status": "completed",
        "experiment_id": summary["experiment_id"],
        "total_tests": summary["total_results"],
        "overall_retention": summary["overall_avg_retention"],
        "summary": summary,
        "sovereignty": SOVEREIGN_ANCHOR,
    }


@app.get("/api/v2/bcm/experiment/latest")
async def get_latest_experiment():
    """獲取最近一次實驗結果"""
    if latest_experiment_summary is None:
        return {
            "status": "no_data",
            "message": "尚未運行任何實驗。請調用 GET /api/v2/bcm/experiment/run?num_docs=50",
            "hint": "GET /api/v2/bcm/experiment/run?num_docs=50",
        }
    
    return {
        "status": "available",
        "experiment_id": latest_experiment_summary["summary"]["experiment_id"],
        "summary": latest_experiment_summary["summary"],
    }


@app.get("/api/v2/bcm/experiment/report")
async def get_experiment_report():
    """獲取 HTML 實驗報告"""
    if latest_experiment_summary is None:
        return HTMLResponse(
            content="<h2 style='color:#d4a843;text-align:center;margin-top:100px'>尚未運行實驗，請先調用 /api/v2/bcm/experiment/run</h2>"
        )
    
    viz = Visualizer()
    html = viz.generate_html_report(
        latest_experiment_summary["summary"],
        latest_experiment_summary["results"][:50],
    )
    return HTMLResponse(content=html)


@app.get("/api/v2/bcm/factors")
async def get_factor_definitions():
    """獲取七因子定義"""
    return {
        "factors": [
            {
                "id": fid,
                "name": f["name"],
                "name_en": f["name_en"],
                "weight": f["weight"],
                "description": f["description"],
                "forge_difficulty": f["forge_difficulty"],
                "retention_under_attack": f["retention_under_attack"],
                "icon": f["icon"],
            }
            for fid, f in FACTOR_DEFINITIONS.items()
        ],
        "sovereignty": SOVEREIGN_ANCHOR,
    }


# ============================================================
# 主入口
# ============================================================
if __name__ == "__main__":
    import uvicorn
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  🐉 龍魂·行為密碼學主權API v{API_VERSION}
║  DNA: #龍芯⚡️丙午·甲申·丁酉·丙午·䷳艮-BCM-API-V2.0
║══════════════════════════════════════════════════════════════║
║  📡 端口: {API_PORT}
║  📖 API文檔: http://localhost:{API_PORT}/api/v2/bcm/docs
║  📊 實驗報告: http://localhost:{API_PORT}/api/v2/bcm/experiment/report
║  🏛️ 主權: {SOVEREIGN_ANCHOR['confirm']}
║══════════════════════════════════════════════════════════════║
║  端點:
║  POST /api/v2/bcm/extract       — 提取七因子指紋
║  POST /api/v2/bcm/verify        — 驗證行為指紋
║  GET  /api/v2/bcm/experiment/run — 運行攻擊模擬實驗
║  GET  /api/v2/bcm/status         — 引擎狀態
║  GET  /api/v2/bcm/sovereignty    — 主權驗證
║  GET  /api/v2/bcm/factors        — 因子定義
╚══════════════════════════════════════════════════════════════╝
""")
    
    uvicorn.run(app, host="0.0.0.0", port=API_PORT, log_level="info")
