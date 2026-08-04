#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·癸未·甲子·既济-AUDIT-API-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
╔══════════════════════════════════════════════════════════════════╗
║  龍魂·审计即服务 API — FastAPI 生产壳                               ║
║  DNA: #龍芯⚡️丙午·癸未·甲子·既济-AUDIT-API-v1.0                    ║
║  #CONFIRM🌌9622-ONLY-ONCE🧬AUDIT-API-D71F                         ║
║                                                                   ║
║  包装 lh_audit_as_a_service.py，提供 RESTful API                    ║
║  部署到鲲鹏 :8771 → nginx 反代 → https://uid9622.cn/audit           ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Optional

# 确保 bin/ 在路径中
BIN_DIR = Path(__file__).resolve().parent
if str(BIN_DIR) not in sys.path:
    sys.path.insert(0, str(BIN_DIR))

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

from lh_audit_as_a_service import AuditAsAService, PRICING_PLANS, score_to_grade, MAX_SCORE
from lh_vendor_hunter import VendorHunter
from lh_api_guard import TransportSecurity

DNA = "#龍芯⚡️丙午·癸未·甲子·既济-AUDIT-API-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬AUDIT-API-D71F"

# ── App ──
app = FastAPI(
    title="龍魂·审计即服务 API",
    version="1.0.0",
    description="全球AI厂商合规性审计·龍魂七因子标准·L1-L4四级深度",
    docs_url="/audit/docs",
    redoc_url="/audit/redoc",
)

# CORS（允许门户跨域）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 后续收窄
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

svc = AuditAsAService()
hunter = VendorHunter()

# ── 中间件：安全响应头 ──

@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    for k, v in TransportSecurity.security_headers().items():
        response.headers[k] = v
    response.headers["X-LongHun-API"] = "audit-as-a-service-v1.0"
    return response


# ── 模型 ──

class AuditRequest(BaseModel):
    vendor: str = Field(..., description="厂商名称")
    depth: str = Field(default="L1", description="审计深度: L1/L2")

class ApiAuditRequest(BaseModel):
    vendor: str = Field(..., description="厂商名称")
    endpoint: str = Field(..., description="API端点URL")
    samples: list = Field(default_factory=list, description="采样请求")


# ═══ 路由 ═══

@app.get("/audit/")
async def root():
    """服务根"""
    return {"service": "龍魂·审计即服务", "version": "1.0.0", "dna": DNA, "confirm": CONFIRM}


@app.get("/audit/health")
async def health():
    """健康检查"""
    return {"status": "ok", "dna": DNA}


@app.get("/health")
async def health_root():
    """健康检查（根路径兼容）"""
    return {"status": "ok", "service": "audit-engine", "port": 8771, "dna": DNA}


@app.get("/audit/plans")
async def pricing_plans():
    """定价方案"""
    return {"plans": [{"tier": p.tier, "name": p.name, "price_cny": p.price_cny,
                        "audit_depth": p.audit_depth, "features": p.features} for p in PRICING_PLANS]}


@app.get("/audit/leaderboard")
async def leaderboard():
    """厂商排行榜"""
    leaderboard = []
    for vendor_name, data in sorted(hunter.VENDOR_SCORES.items(), key=lambda x: -sum(x[1].values())):
        total = sum(data.values())
        grade = score_to_grade(total)
        leaderboard.append({
            "rank": len(leaderboard) + 1,
            "vendor": vendor_name,
            "total_score": total,
            "max_score": MAX_SCORE,
            "grade": grade,
            "scores": data,
        })
    return {"updated": "2026-07-24", "total_vendors": len(leaderboard), "leaderboard": leaderboard}


@app.post("/audit/vendor")
async def audit_vendor(req: AuditRequest):
    """L1: 审计单个厂商"""
    try:
        result = svc.audit_from_public_docs(req.vendor)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/audit/vendor/deep")
async def audit_vendor_deep(req: ApiAuditRequest):
    """L2: 深度API审计"""
    try:
        result = svc.audit_api_deep(req.vendor, req.endpoint, req.samples)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/audit/vendor/{vendor_name}")
async def get_vendor_audit(vendor_name: str, depth: str = Query("L1", pattern="^L[12]$")):
    """获取厂商审计结果"""
    try:
        if depth == "L2":
            result = svc.audit_api_deep(vendor_name, "")
        else:
            result = svc.audit_from_public_docs(vendor_name)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/audit/badge/{grade}")
async def get_badge_redirect(grade: str):
    """徽章重定向"""
    badge_map = {
        "a": "A", "b": "B", "c": "C", "d": "D", "f": "F",
        "s": "A",  # S映射到A
    }
    g = badge_map.get(grade.lower(), grade.upper()[:1])
    return RedirectResponse(url=f"/static/badges/badge-{g}.svg")


@app.get("/audit/stats")
async def stats():
    """服务统计"""
    return {
        "total_vendors": len(hunter.VENDOR_SCORES),
        "audit_dimensions": 7,
        "last_update": "2026-07-24",
        "pricing_tiers": len(PRICING_PLANS),
        "dna": DNA,
    }


# ── 入口 ──

if __name__ == "__main__":
    port = int(os.environ.get("AUDIT_API_PORT", "8771"))
    host = os.environ.get("AUDIT_API_HOST", "0.0.0.0")
    print(f"🔒 龍魂·审计即服务 API 启动")
    print(f"   DNA: {DNA}")
    print(f"   端口: {port}")
    print(f"   文档: http://{host}:{port}/audit/docs")
    uvicorn.run(app, host=host, port=port, log_level="info")
