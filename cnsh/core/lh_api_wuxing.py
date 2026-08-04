#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·五行计算器API入口 v3.2
FastAPI统一路由·连接五行计算器核心
DNA:#龍芯⚡️2026-06-04-API-WUXING-FILE1-v3.2
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # type: ignore[import-untyped]
from pydantic import BaseModel
from datetime import datetime
from typing import Any, Dict
import json
import sys
import os

# 导入计算器核心模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'wuxing_calculator'))
from calculator import (  # type: ignore[import-untyped]
    龍魂五行计算器_v2, 生成节点, 计算数字根,
    天干五行表, 地支五行表, 五行相生, 五行相克,
    完整链路分析, 生成补益建议
)

# 引入五行计算优化模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'wuxing'))
from wuxing_calc_optimizations import (  # type: ignore[import-untyped]
    robust_digital_root,
    compute_hedge_index_h,
    cv_balance_score,
)

app = FastAPI(
    title="龍魂·五行计算器 API",
    description="CNSH中文编程·五行相生相克分析",
    version="3.3"
)

# 跨域配置（🛡️ P77修复：白名单替代通配符）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8766", "http://127.0.0.1:8766"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-DNA-TRACE"],
)

# 数据模型
class 四柱输入(BaseModel):
    年天干: str
    年地支: str
    月天干: str
    月地支: str
    日天干: str
    日地支: str
    时天干: str
    时地支: str

class 文本输入(BaseModel):
    文本: str
    标题: str = "未命名"
    类型: str = "text"

class 健康检查(BaseModel):
    状态: str
    时间: str
    版本: str

# 健康检查端点
@app.get("/health", response_model=健康检查)
async def 健康检查端点():
    """系统健康检查"""
    return {
        "状态": "🟢 正常",
        "时间": datetime.now().isoformat(),
        "版本": "3.2"
    }

# 四柱分析端点
@app.post("/calculate/sizu")
async def 四柱分析(输入: 四柱输入):
    """四柱五行分析"""
    try:
        结果 = 龍魂五行计算器_v2(
            输入.年天干, 输入.年地支,
            输入.月天干, 输入.月地支,
            输入.日天干, 输入.日地支,
            输入.时天干, 输入.时地支
        )
        return {
            "状态": "🟢 成功",
            "数据": 结果,
            "时间戳": datetime.now().isoformat(),
            "DNA": "#龍芯⚡️2026-06-04-API-SIZU-v3.2"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"计算错误: {str(e)}")

# 文本节点生成端点
@app.post("/generate/node")
async def 生成流场节点(输入: 文本输入):
    """生成流场节点"""
    try:
        节点 = 生成节点(
            输入.文本,
            title=输入.标题,
            raw_type=输入.类型
        )
        return {
            "状态": "🟢 成功",
            "节点": 节点,
            "时间戳": datetime.now().isoformat(),
            "DNA": "#龍芯⚡️2026-06-04-API-NODE-v3.2"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"生成错误: {str(e)}")

# 数字根分析端点（鲁棒数字根）
@app.get("/analyze/digital-root/{文本}")
async def 数字根分析(文本: str):
    """分析数字根和对应五行（支持全角/中文数字/负数/小数）"""
    try:
        dr = robust_digital_root(文本)
        五行映射 = {1:"水",2:"火",3:"木",4:"金",5:"土",6:"水",7:"火",8:"木",9:"金",0:"土"}
        五行 = 五行映射[dr]

        # 三色审计
        if dr in [3,9]:
            审计 = "🔴"
        elif dr == 6:
            审计 = "🟡"
        else:
            审计 = "🟢"

        return {
            "文本": 文本,
            "数字根": dr,
            "五行": 五行,
            "审计": 审计,
            "说明": "鲁棒数字根→五行映射·三色审计判定"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"分析错误: {str(e)}")

# 五行相生相克查询端点
@app.get("/query/relations/{五行}")
async def 五行关系查询(五行: str):
    """查询五行的相生相克关系"""
    if 五行 not in ["金", "木", "水", "火", "土"]:
        raise HTTPException(status_code=400, detail="无效的五行")

    return {
        "五行": 五行,
        "相生": 五行相生.get(五行),
        "相克": 五行相克.get(五行),
        "说明": f"{五行}生{五行相生.get(五行)}·{五行相克.get(五行)}克{五行}"
    }

# 批量链路分析端点
@app.post("/analyze/circuit")
async def 链路分析(得分数据: Dict[str, Any]):
    """完整链路分析"""
    try:
        结果 = 完整链路分析(得分数据)
        return {
            "状态": "🟢 成功",
            "链路健康度": 结果["链路健康度"],
            "总体状态": 结果["状态"],
            "预警信息": 结果["断链预警"],
            "时间戳": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"分析错误: {str(e)}")

# 五行对冲指数 H 端点
@app.post("/analyze/hedge")
async def 对冲指数分析(得分数据: Dict[str, Any]):
    """计算五行对冲指数 H（自学习权重）"""
    try:
        scores = 得分数据.get("scores", {})
        # 补齐默认分量
        restraint = scores.get("克制衡分", 0.5)
        relief = scores.get("疏导分", 0.5)
        supplement = scores.get("补益分", 0.5)
        balance = scores.get("均衡指数", cv_balance_score(得分数据.get("五行得分", scores)))
        health = scores.get("链路健康度", 0.5)

        result = compute_hedge_index_h(
            restraint_score=restraint,
            relief_score=relief,
            supplement_score=supplement,
            balance_score=balance,
            health_score=health,
        )
        return {
            "状态": "🟢 成功",
            "对冲指数H": result["对冲指数H"],
            "三色": result["三色"],
            "action": result["action"],
            "分项": result["分项"],
            "权重": result["权重"],
            "时间戳": datetime.now().isoformat(),
            "DNA": "#龍芯⚡️2026-06-26-API-HEDGE-v3.3",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"计算错误: {str(e)}")

# API文档自定义
@app.get("/")
async def 文档():
    """龍魂五行计算器API文档"""
    return {
        "名称": "龍魂·五行计算器 API v3.2",
        "描述": "CNSH中文编程·天干地支·五行相生相克",
        "端点": {
            "GET /health": "系统健康检查",
            "POST /calculate/sizu": "四柱五行分析",
            "POST /generate/node": "生成流场节点",
            "GET /analyze/digital-root/{文本}": "数字根分析（鲁棒）",
            "GET /query/relations/{五行}": "五行关系查询",
            "POST /analyze/circuit": "链路分析",
            "POST /analyze/hedge": "五行对冲指数 H（自学习权重）"
        },
        "DNA": "#龍芯⚡️2026-06-26-API-WUXING-v3.3",
        "版本": "3.3"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
