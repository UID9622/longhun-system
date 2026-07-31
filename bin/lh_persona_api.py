# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-PERSONA-API-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# ╔══════════════════════════════════════════════════════════════╗
# ║  龍魂·人格路由 API v1.0                                      ║
# ║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-PERSONA-API-v1.0       ║
# ║  统一入口：请求 → 意图 → 人格 → 执行 → 审计                ║
# ╚══════════════════════════════════════════════════════════════╝
"""
龍魂人格路由 API — 把 longhun_persona_hub、PersonaRunner、RuyiRouter 焊成闭环。

端点:
  GET  /health           健康检查
  GET  /persona/list     列出可用人格
  POST /persona/route    根据任务路由到人格
  POST /persona/execute  直接执行指定人格

用法:
  python3 bin/lh_persona_api.py
  curl -X POST http://127.0.0.1:8779/persona/route -H "Content-Type: application/json" \
       -d '{"task":"检查这段代码有没有安全漏洞"}'
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional

# 确保能 import 到 engines/
SYSTEM_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SYSTEM_ROOT))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn

from engines.lh_persona_runner import PersonaRunner, PERSONA_MATRIX

DNA = "#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-PERSONA-API-v1.0"

# 降级链：P77 安全不可用 → S1 法律 → S2 数理 → S3 民生
FALLBACK_CHAIN = ["P77", "S1", "S2", "S3"]

app = FastAPI(title="龍魂人格路由 API", version="1.0.0")
runner = PersonaRunner(auto_boot=True)

# 日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | PERSONA-API | %(message)s",
)
logger = logging.getLogger(__name__)


class RouteRequest(BaseModel):
    task: str = Field(..., min_length=1, max_length=10000, description="用户任务描述")
    context: Dict[str, Any] = Field(default_factory=dict, description="额外上下文")
    require_security: bool = Field(default=False, description="是否强制安全人格先审")


class ExecuteRequest(BaseModel):
    persona_id: str = Field(..., description="人格 ID，如 P77、P04、S1")
    task: str = Field(..., min_length=1, max_length=10000, description="任务描述")
    context: Dict[str, Any] = Field(default_factory=dict, description="额外上下文")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "dna": DNA,
        "booted": runner._booted,
        "agents_online": len(runner._agents),
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/persona/list")
def list_personas():
    """列出所有人格及其在线状态。"""
    result = []
    for pid, meta in PERSONA_MATRIX.items():
        agent = runner._agents.get(pid)
        result.append({
            "id": pid,
            "name": meta.get("name", ""),
            "role": meta.get("role", ""),
            "layer": meta.get("layer", ""),
            "motto": meta.get("motto", ""),
            "online": agent is not None,
        })
    return {"personas": result, "total": len(result), "online": sum(1 for p in result if p["online"])}


def _route_by_task(task: str) -> Dict[str, Any]:
    """基于关键词的简单意图路由。"""
    task_lower = task.lower()
    rules = [
        (("安全", "漏洞", "攻击", "注入", "泄露", "密钥", "熔断"), "P77", "安全审计"),
        (("法律", "合规", "合同", "协议", "权利"), "S1", "合规审查"),
        (("数学", "算法", "洛书", "河图", "验证", "证明"), "S2", "数理审计"),
        (("人民", "老百姓", "民生", "维权", "群众"), "S3", "民生守护"),
        (("代码", "工程", "部署", "构建", "脚本"), "P04", "工程执行"),
        (("审计", "检查", "扫描", " patrol "), "P05", "审计监察"),
        (("命名", "翻译", "术语", "CNSH"), "P08", "命名规范"),
        (("设计", "UI", "视觉", "排版", "颜色"), "P11", "创意设计"),
        (("战略", "决策", "规划", "架构"), "P01", "战略推演"),
        (("部署", "发布", "上线", "运维"), "P14", "部署落地"),
    ]
    for triggers, pid, reason in rules:
        if any(t in task_lower for t in triggers):
            return {"primary": pid, "reason": reason, "triggers": [t for t in triggers if t in task_lower]}
    return {"primary": "P05", "reason": "默认审计兜底", "triggers": []}


def _execute_with_fallback(persona_id: str, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """执行人格，失败时按降级链切换。"""
    results = []
    chain = [persona_id] + [p for p in FALLBACK_CHAIN if p != persona_id]

    for pid in chain:
        if pid not in runner._agents:
            boot_result = runner.boot([pid])
            if not boot_result.get(pid):
                results.append({"persona": pid, "status": "not_bootable"})
                continue

        result = runner.dispatch(pid, task, **context)
        results.append({"persona": pid, "status": "executed", "result": result})

        if result.get("status") == "ok":
            return {
                "executed_persona": pid,
                "fallback_used": pid != persona_id,
                "fallback_chain": chain,
                "results": results,
                "success": True,
            }

    # 全部失败，返回最后结果
    return {
        "executed_persona": None,
        "fallback_used": True,
        "fallback_chain": chain,
        "results": results,
        "success": False,
    }


@app.post("/persona/route")
def route_persona(req: RouteRequest):
    """根据任务路由到最佳人格并执行。"""
    start = time.time()
    route = _route_by_task(req.task)
    primary = route["primary"]

    # 如果强制安全审计，先让 P77 过目
    if req.require_security and primary != "P77":
        primary = "P77"
        route["security_first"] = True

    execution = _execute_with_fallback(primary, req.task, req.context)

    return {
        "dna": DNA,
        "task": req.task,
        "route": route,
        "execution": execution,
        "duration_ms": round((time.time() - start) * 1000, 2),
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/persona/execute")
def execute_persona(req: ExecuteRequest):
    """直接执行指定人格。"""
    if req.persona_id not in PERSONA_MATRIX:
        raise HTTPException(status_code=404, detail=f"未知人格: {req.persona_id}")

    start = time.time()
    execution = _execute_with_fallback(req.persona_id, req.task, req.context)

    return {
        "dna": DNA,
        "requested_persona": req.persona_id,
        "execution": execution,
        "duration_ms": round((time.time() - start) * 1000, 2),
        "timestamp": datetime.now().isoformat(),
    }


def main():
    parser = None
    import argparse
    ap = argparse.ArgumentParser(description="龍魂人格路由 API")
    ap.add_argument("--host", default="127.0.0.1", help="监听地址")
    ap.add_argument("--port", type=int, default=8779, help="监听端口")
    args = ap.parse_args()

    logger.info(f"启动人格路由 API | {DNA} | {args.host}:{args.port}")
    uvicorn.run(app, host=args.host, port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
