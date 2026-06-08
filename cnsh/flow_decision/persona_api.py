#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂人格 API 路由系统
DNA: #龍芯⚡️2026-06-09-PERSONA-API-v1.0
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import json

app = FastAPI(title="龍魂人格 API", version="1.0")

# 14 个人格定义
PERSONAS = {
    "P00": {"name": "文心", "role": "战略核心", "trigram": "巽☴", "layer": "L0"},
    "P01": {"name": "诸葛亮", "role": "战略推演", "trigram": "乾☰", "layer": "L1"},
    "P02": {"name": "龍芯", "role": "执行核心", "trigram": "震☳", "layer": "L1"},
    "P03": {"name": "雯雯", "role": "隐私卫士", "trigram": "坤☷", "layer": "L2"},
    "P05": {"name": "上帝之眼", "role": "监管审计", "trigram": "坎☵", "layer": "L2"},
    "P06": {"name": "数学大师", "role": "逻辑分析", "trigram": "艮☶", "layer": "L2"},
    "P13": {"name": "姜子牙", "role": "九宫派位", "trigram": "离☲", "layer": "L3"},
    "P14": {"name": "吕蒙", "role": "辅助执行", "trigram": "兑☱", "layer": "L3"},
    "P15": {"name": "乔前辈", "role": "档案管理", "trigram": "巽☴", "layer": "L3"},
    "P72": {"name": "龍盾", "role": "安全防护", "trigram": "坎☵", "layer": "L4"},
    # 五大本地人格
    "K01": {"name": "雯雯", "role": "承载包容·文档整理师", "trigram": "坤☷", "layer": "本地"},
    "K02": {"name": "侦察兵", "role": "止静观察·信息猎手", "trigram": "艮☶", "layer": "本地"},
    "K03": {"name": "守护者", "role": "危机应对·安全卫士", "trigram": "坎☵", "layer": "本地"},
    "K04": {"name": "宝宝", "role": "文明光明·构建师", "trigram": "离☲", "layer": "本地"},
    "K05": {"name": "文心", "role": "柔顺协调·同步专家", "trigram": "巽☴", "layer": "本地"},
}

@app.get("/personas/list")
def list_personas():
    return {"count": len(PERSONAS), "personas": PERSONAS}

@app.get("/personas/{pid}")
def get_persona(pid: str):
    if pid not in PERSONAS:
        raise HTTPException(status_code=404, detail=f"人格 {pid} 未定义")
    return PERSONAS[pid]

@app.post("/personas/route")
def route_task(task: str, layer: Optional[str] = None):
    """根据任务类型和层级路由到对应人格"""
    candidates = [p for p in PERSONAS.values() if layer is None or p["layer"] == layer]
    return {"task": task, "routed_to": candidates[:3]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9001)
