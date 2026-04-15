"""
shield/api.py — LocalShield FastAPI 路由
/shield/*
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from .core import LocalShield
from dare.store import get_shield_logs

router = APIRouter(prefix="/shield", tags=["shield"])
_shield = LocalShield()

class ProcessReq(BaseModel):
    content: str
    action:  str = "PROCESS"

@router.post("/process")
def process_content(req: ProcessReq):
    """通过三层防御处理内容"""
    result = _shield.process(req.content, req.action)
    return {
        "reject":         result.reject,
        "reason":         result.reason,
        "dna_trace":      result.dna_trace,
        "ethical_score":  result.ethical_score,
        "sense_metadata": result.sense_metadata,
        "layer_logs":     result.layer_logs,
    }

@router.get("/status")
def get_status():
    """护盾状态"""
    return _shield.status()

@router.get("/logs/{dna_trace}")
def get_logs(dna_trace: str):
    """查看某个DNA追溯码的护盾日志"""
    logs = get_shield_logs(dna_trace)
    return {"dna_trace": dna_trace, "logs": logs, "count": len(logs)}
