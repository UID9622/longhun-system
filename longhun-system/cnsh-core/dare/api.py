"""
dare/api.py — 四敢品质 FastAPI 路由
/dare/*
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from .system import FourDareSystem, DARE_CODES, TAOIST_WEIGHTS

router = APIRouter(prefix="/dare", tags=["dare"])
_sys = FourDareSystem()

# ── 请求模型 ─────────────────────────────────────────────────────

class RecordReq(BaseModel):
    action_type: str
    weight:      Optional[float] = None
    context:     str = ""
    dna_trace:   str = ""
    user_id:     str = "uid9622"

# ── 路由 ─────────────────────────────────────────────────────────

@router.post("/record")
def record_dare(req: RecordReq):
    """记录一次四敢行为"""
    return _sys.record(
        action_type=req.action_type,
        weight=req.weight,
        context=req.context,
        dna_trace=req.dna_trace,
        user_id=req.user_id,
    )

@router.get("/score/{user_id}")
def get_score(user_id: str = "uid9622"):
    """获取四敢品质评分"""
    return _sys.calculate_score(user_id)

@router.get("/score")
def get_score_default():
    return _sys.calculate_score("uid9622")

@router.get("/yao/{user_id}")
def get_yao(user_id: str = "uid9622"):
    """六爻状态可视化"""
    return _sys.yao_status(user_id)

@router.get("/yao")
def get_yao_default():
    return _sys.yao_status("uid9622")

@router.get("/easter-eggs")
def get_easter_eggs():
    """道德经彩蛋触发状态"""
    return {"easter_eggs": _sys.get_easter_eggs("uid9622")}

@router.get("/catalog")
def get_catalog():
    """四敢定义说明"""
    return {
        "dare_codes":     DARE_CODES,
        "taoist_weights": TAOIST_WEIGHTS,
        "yao_map": {
            "初爻": "敢相信 (TRUST-INIT)",
            "二爻": "敢吃亏 (SACRIFICE)",
            "三爻": "敢说不服 (DISSENT)",
            "四爻": "敢公开审计 (AUDIT-OPEN)",
            "五爻": "四敢俱全 + 道德经彩蛋",
            "上爻": "通天大道资格",
        },
        "easter_egg_rules": [
            {"id": "shang_shan", "trigger": "全部>100", "reward": "上善若水"},
            {"id": "gu_wang",    "trigger": "吃亏>200 且 审计>150", "reward": "谷王"},
            {"id": "wu_wei",     "trigger": "不服>80 且 信任>80", "reward": "无为而无不为"},
        ],
    }
