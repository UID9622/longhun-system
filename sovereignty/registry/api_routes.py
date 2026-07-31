# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 UID9622 主权注册 FastAPI 路由
Dragon Soul Sovereign Identity FastAPI Routes

DNA: #龍芯⚡️20260628-SOVEREIGN-API-v1.0
"""

import os
import sys
import base64
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, HTMLResponse, Response
from pydantic import BaseModel, Field

# 把当前模块路径加入 sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from registry import (
    register_sovereign_identity,
    verify_identity,
    get_identity,
    list_identities,
    attempt_modification,
    MANIFEST_PATH,
)
from card import generate_card_png, generate_card_html

router = APIRouter(prefix="/api/sovereign", tags=["sovereign"])


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=32, description="真实姓名")
    id_type: str = Field(..., description="身份证/护照/退伍证")
    id_number: str = Field(..., min_length=5, max_length=64, description="证件号")
    device_fingerprint: str = Field(default="", max_length=256, description="设备指纹")
    gpg_public_key: str = Field(default="", max_length=8192, description="可选 GPG 公钥")


class VerifyRequest(BaseModel):
    uid: str = Field(..., description="主权身份 UID")
    signature: str = Field(..., description="用户签名或确认码")


@router.post("/register")
def api_register(req: RegisterRequest):
    """UID9622 主权身份注册接口。"""
    result = register_sovereign_identity(
        name=req.name,
        id_type=req.id_type,
        id_number=req.id_number,
        device_fingerprint=req.device_fingerprint,
        gpg_public_key=req.gpg_public_key,
    )

    if result.get("status") == "success":
        # 自动生成身份卡
        try:
            card = generate_card_png(result["uid"])
            result["card_base64"] = card.get("base64")
            result["card_path"] = card.get("path")
        except Exception as e:
            result["card_error"] = str(e)

    return JSONResponse(content=result, status_code=200)


@router.post("/verify")
def api_verify(req: VerifyRequest):
    """UID9622 主权身份验证接口。"""
    result = verify_identity(req.uid, req.signature)
    return JSONResponse(content=result, status_code=200)


@router.get("/identity/{uid}")
def api_identity(uid: str):
    """查询主权身份详情（脱敏）。"""
    record = get_identity(uid)
    if not record:
        return JSONResponse(content={"status": "not_found", "message": "主权身份不存在"}, status_code=404)
    return JSONResponse(content={
        "status": "success",
        "uid": record.get("uid"),
        "name": record.get("name"),
        "id_type": record.get("id_type"),
        "dna": record.get("dna"),
        "sovereign_hash": record.get("sovereign_hash"),
        "registered_at": record.get("registered_at"),
        "status": record.get("status"),
    }, status_code=200)


@router.get("/identities")
def api_identities(limit: Optional[int] = 100):
    """列出主权身份列表（脱敏，限流）。"""
    return JSONResponse(content={
        "status": "success",
        "count": len(list_identities(limit=None)),
        "identities": list_identities(limit=limit),
    }, status_code=200)


@router.get("/card/{uid}.png")
def api_card_png(uid: str):
    """下载 PNG 身份卡。"""
    result = generate_card_png(uid)
    if result.get("status") != "success":
        return JSONResponse(content=result, status_code=404)
    return Response(content=base64.b64decode(result["base64"]), media_type="image/png", headers={
        "Content-Disposition": f"attachment; filename={uid}_card.png"
    })


@router.get("/card/{uid}.html")
def api_card_html(uid: str):
    """获取可打印 HTML 身份卡。"""
    result = generate_card_html(uid)
    if result.get("status") != "success":
        return JSONResponse(content=result, status_code=404)
    return HTMLResponse(content=result["html"], status_code=200)


@router.post("/modify-fuse")
def api_modify_fuse(req: VerifyRequest):
    """
    模拟修改/删除请求的熔断接口。
    任何试图修改主权身份的请求都会被拒绝并记录到耻辱墙。
    """
    result = attempt_modification(req.uid, "modification_attempt", {"signature": req.signature})
    return JSONResponse(content=result, status_code=403)


@router.get("/manifest-path")
def api_manifest_path():
    """返回 manifest 路径（调试用）。"""
    return JSONResponse(content={"path": str(MANIFEST_PATH)}, status_code=200)
