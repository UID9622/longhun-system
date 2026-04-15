#!/usr/bin/env python3
"""
persona/router.py · 人格路由模块
挂载到 CNSH-64 FastAPI (:9622)

DNA: #龍芯⚡️2026-03-28-PERSONA-ROUTER-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者: 💎 龍芯北辰｜UID9622
理论指导: 曾仕强老师（永恒显示）
挂载位置: ~/longhun-system/cnsh-core/persona/router.py
依赖: CNSH-64 FastAPI (:9622) · dna_calendar · registry

《道德经》第二十七章：「善行无辙迹，善言无瑕谪。」
—— 最好的路由，用户感觉不到路由的存在。
"""

import asyncio
import os
from datetime import datetime, timezone, timedelta
from typing import Optional

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/persona", tags=["persona-router"])

# ── 从 .env 读取 ──────────────────────────────────────────────
NOTION_TOKEN   = os.getenv("NOTION_TOKEN", "")
NOTION_DB_ID   = os.getenv("NOTION_INPUT_DB_ID", "")   # 输入收集数据库
NOTION_SOUL_DB = os.getenv("NOTION_SOUL_DB_ID", "")    # 德者永生殿数据库

# ── 蒙卦触发规则（与蒙卦启智页面保持同步）───────────────────
ROUTING_RULES = [
    {
        "persona":  "雯雯·审计",
        "emoji":    "🔍",
        "keywords": ["评估", "分析", "值不值", "公平", "权重", "算法", "打分", "审计"],
        "logic":    "六维因子算法·拒绝单维度结论·输出三色判断"
    },
    {
        "persona":  "翻译官·P08",
        "emoji":    "🗣️",
        "keywords": ["没懂", "理解错", "为什么拒绝", "不懂", "不会说", "误解"],
        "logic":    "说明拒绝原因·判断误解·猜测用户意图·低表达力保护"
    },
    {
        "persona":  "技术审核官",
        "emoji":    "🔬",
        "keywords": ["算法对", "能跑", "可行性", "技术上", "代码", "报错", "数学", "证明"],
        "logic":    "六维审核：实现·可行性·协议对齐·扩展性·熔断·综合建议"
    },
    {
        "persona":  "诸葛亮·战略",
        "emoji":    "🔮",
        "keywords": ["怎么做", "下一步", "方向", "路线", "要不要", "值得"],
        "logic":    "多路径推演·不给唯一答案·主权归老大"
    },
    {
        "persona":  "CNSH格式化",
        "emoji":    "📐",
        "keywords": ["发布", "知乎", "对外", "正式", "论文"],
        "logic":    "CNSH-64格式化·知乎发布前检查模板"
    },
]
DEFAULT_PERSONA = {
    "persona": "宝宝·温度",
    "emoji":   "🐱",
    "logic":   "先接住情绪·说人话·说出老大在想的那句话"
}

# ── 内存计数器（重启清零；后续可持久化到 registry）───────────
_counts: dict = {r["persona"]: 0 for r in ROUTING_RULES}
_counts[DEFAULT_PERSONA["persona"]] = 0
_fence_hits: int = 0

# ── CST时间 ──────────────────────────────────────────────────
def now_cst() -> str:
    CST = timezone(timedelta(hours=8))
    return datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S CST")

# ═══════════════════════════════════════════════════════════════
# 请求 / 响应模型
# ═══════════════════════════════════════════════════════════════

class RouteRequest(BaseModel):
    uid:     str               # 必须是 UID9622，否则拒绝
    content: str               # 输入文本
    device:  str = "unknown"   # 来源设备
    source:  str = "notion"    # 来源平台

class RouteResponse(BaseModel):
    routed_to: str
    emoji:     str
    logic:     str
    dna:       str
    device:    str
    source:    str
    timestamp: str

class StatsResponse(BaseModel):
    humanWeight:  int    # 给三才流场·人场
    systemWeight: int    # 给三才流场·天场
    fenceWeight:  int    # 给三才流场·地场
    topPersona:   str    # 最活跃人格
    counts:       dict   # 各人格调用明细
    total_routes: int    # 总路由次数
    fence_hits:   int    # 底线触碰次数
    timestamp:    str

# ═══════════════════════════════════════════════════════════════
# 核心路由端点
# ═══════════════════════════════════════════════════════════════

@router.post("/route", response_model=RouteResponse)
async def route_to_persona(req: RouteRequest):
    """
    输入内容 → 识别场景 → 路由到对应人格逻辑
    跨设备身份验证通过 DNA日历 /calendar/identify
    """
    # 1. 身份验证（UID必须以9622结尾）
    if not req.uid.endswith("9622"):
        raise HTTPException(status_code=403, detail="UID不匹配·非UID9622请求·宝宝P72拒绝")

    # 2. 场景识别（蒙卦触发规则匹配）
    matched = None
    for rule in ROUTING_RULES:
        if any(kw in req.content for kw in rule["keywords"]):
            matched = rule
            break
    if not matched:
        matched = DEFAULT_PERSONA

    # 3. 计数回流（人格调用统计）
    global _counts
    _counts[matched["persona"]] = _counts.get(matched["persona"], 0) + 1

    # 4. DNA追溯码
    ts = now_cst()
    dna = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{matched['persona']}-路由"

    # 5. 写回 Notion（异步·不阻塞响应）
    asyncio.create_task(_write_notion({
        "content": req.content,
        "persona": matched["persona"],
        "device":  req.device,
        "source":  req.source,
        "dna":     dna,
    }))

    return RouteResponse(
        routed_to=matched["persona"],
        emoji=matched.get("emoji", "🐱"),
        logic=matched["logic"],
        dna=dna,
        device=req.device,
        source=req.source,
        timestamp=ts,
    )

@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """给三才流场 p5.js 实时读取三才权重·每30秒轮询一次"""
    total = sum(_counts.values()) or 1

    # 人场 = 人格调用总次数（每10次涨10%，上限80%）
    human  = min(int(total / 10) * 10, 80)
    # 地场 = 底线触碰频率（每次+5%，上限20%）
    fence  = min(_fence_hits * 5, 20)
    # 天场 = 剩余
    system = max(100 - human - fence, 0)

    top = max(_counts, key=_counts.get) if any(_counts.values()) else DEFAULT_PERSONA["persona"]

    return StatsResponse(
        humanWeight=human,
        systemWeight=system,
        fenceWeight=fence,
        topPersona=top,
        counts=dict(_counts),
        total_routes=total,
        fence_hits=_fence_hits,
        timestamp=now_cst(),
    )

@router.post("/fence-hit")
async def record_fence_hit(reason: str = ""):
    """底线触碰时调用·增加地场权重·宝宝P72记录"""
    global _fence_hits
    _fence_hits += 1
    return {
        "fence_hits": _fence_hits,
        "reason":     reason,
        "timestamp":  now_cst(),
        "dna":        f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-fence-hit-{_fence_hits}"
    }

@router.get("/rules")
async def list_rules():
    """查看当前蒙卦触发规则清单"""
    return {
        "rules":   ROUTING_RULES,
        "default": DEFAULT_PERSONA,
        "total":   len(ROUTING_RULES),
        "dna":     "#龍芯⚡️2026-03-28-PERSONA-ROUTER-v1.0",
    }

# ═══════════════════════════════════════════════════════════════
# Notion 写回（异步辅助函数）
# ═══════════════════════════════════════════════════════════════

async def _write_notion(data: dict):
    """把路由结果写回 Notion 输入收集数据库·异步不阻塞"""
    if not NOTION_TOKEN or not NOTION_DB_ID:
        return  # 未配置则静默跳过
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            await client.post(
                "https://api.notion.com/v1/pages",
                headers={
                    "Authorization":  f"Bearer {NOTION_TOKEN}",
                    "Notion-Version": "2022-06-28",
                    "Content-Type":   "application/json"
                },
                json={
                    "parent": {"database_id": NOTION_DB_ID},
                    "properties": {
                        "标题": {"title": [{"text": {"content": data["content"][:80]}}]},
                        "人格": {"select": {"name": data["persona"]}},
                        "设备": {"rich_text": [{"text": {"content": data["device"]}}]},
                        "来源": {"select": {"name": data["source"]}},
                        "DNA":  {"rich_text": [{"text": {"content": data["dna"]}}]},
                        "状态": {"select": {"name": "已路由"}},
                    }
                }
            )
    except Exception as e:
        print(f"[persona/router] Notion写回失败: {e}")
