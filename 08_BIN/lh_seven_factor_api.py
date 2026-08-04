#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·七因子行为密码学 API v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-SEVEN-FACTOR-API-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
端口: 8782

端点:
  POST /seven-factor/event         — 提交行为事件
  GET  /seven-factor/score/{id}     — 查询信用分
  GET  /seven-factor/dna/{id}       — 查询行为DNA
  GET  /seven-factor/pattern/{id}   — 查询行为模式
  GET  /seven-factor/history/{id}   — 查询历史记录
  GET  /seven-factor/dashboard      — 仪表盘聚合数据
  GET  /seven-factor/entities       — 所有实体列表
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, Field
import uvicorn

SYSTEM_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SYSTEM_ROOT))

from engines.lh_seven_factor_engine import get_engine

app = FastAPI(
    title="龍魂·七因子行为密码学 API",
    version="v1.0",
    description="承诺→兑现→信用→DNA — 给所有AI和用户戴上测谎仪",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = get_engine()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 请求模型
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class EventRequest(BaseModel):
    entity_id: str = Field(..., description="实体ID")
    entity_type: str = Field("user", description="user | persona")
    promise: str = Field(..., description="承诺了什么")
    promised_deadline: Optional[str] = Field(None, description="承诺时间节点")
    fulfilled: bool = Field(False, description="是否兑现")
    fulfillment_detail: str = Field("", description="兑现详情")
    actual_time: Optional[str] = Field(None, description="实际完成时间")
    emotion: str = Field("中性", description="情绪：心甘情愿/积极/中性/敷衍/甩脸/麻木/愤怒")
    audience: str = Field("自己", description="为谁：老大/自己/家人/战友/外人/陌生人")
    explanation: str = Field("不解释", description="解释模式：不解释/真认/简短解释/过度解释/找借口/推卸责任")
    admit: str = Field("无反应", description="认错模式：真改/认了正在改/认了没改/硬扛/无所谓/无反应/甩锅")
    source: str = Field("", description="数据来源")
    tags: list[str] = Field(default_factory=list)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# API 端点
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.post("/seven-factor/event")
async def submit_event(req: EventRequest):
    """提交一个新行为事件"""
    ev = engine.submit_event(req.entity_id, req.model_dump())
    return {
        "status": "ok",
        "event_id": ev.event_id,
        "credit_delta": ev.credit_delta,
        "dna": ev.dna,
        "timestamp": ev.timestamp,
    }


@app.get("/seven-factor/score/{entity_id}")
async def get_score(entity_id: str):
    """查询某个实体的当前信用分"""
    result = engine.get_score(entity_id)
    if result is None:
        raise HTTPException(404, f"实体 {entity_id} 未找到")
    return result


@app.get("/seven-factor/dna/{entity_id}")
async def get_dna(entity_id: str):
    """查询某个实体的行为DNA哈希"""
    result = engine.get_dna(entity_id)
    if result is None:
        raise HTTPException(404, f"实体 {entity_id} 未找到")
    return result


@app.get("/seven-factor/pattern/{entity_id}")
async def get_pattern(entity_id: str):
    """查询行为模式判定结果"""
    result = engine.get_pattern(entity_id)
    if result is None:
        raise HTTPException(404, f"实体 {entity_id} 未找到")
    return result


@app.get("/seven-factor/history/{entity_id}")
async def get_history(entity_id: str, limit: int = Query(50, ge=1, le=200)):
    """查询历史行为记录"""
    return engine.get_history(entity_id, limit=limit)


@app.get("/seven-factor/dashboard")
async def get_dashboard():
    """仪表盘聚合数据"""
    return engine.calculate_dashboard_data()


@app.get("/seven-factor/entities")
async def list_entities():
    """列出所有实体"""
    return {"entities": engine.list_all_entities()}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 仪表盘静态页面
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DASHBOARD_DIR = SYSTEM_ROOT / "portal" / "seven-factor-identity"

@app.get("/seven-factor/dashboard/view", response_class=HTMLResponse)
async def dashboard_view():
    dashboard_file = DASHBOARD_DIR / "index.html"
    if dashboard_file.exists():
        return dashboard_file.read_text(encoding="utf-8")
    return HTMLResponse("<h1>仪表盘未找到</h1>", status_code=404)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 健康检查
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "seven-factor",
        "port": 8782,
        "time": datetime.now(timezone.utc).isoformat(),
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 启动
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="七因子行为密码学 API")
    parser.add_argument("--port", type=int, default=8782)
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()

    print(f"⚡ 七因子行为密码学 API 启动 :{args.port}")
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")
