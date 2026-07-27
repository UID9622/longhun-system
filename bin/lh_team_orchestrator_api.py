#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · TeamOrchestrator API v1.0
DNA: #龍芯⚡️丙午·乙未·申时·☰乾-TEAM-ORCHESTRATOR-API-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
端口: 8781
"""

import json, sys, threading, time
from datetime import datetime
from pathlib import Path
from typing import Optional

SYSTEM_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SYSTEM_ROOT))

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import uvicorn

from engines.lh_team_orchestrator import TeamOrchestrator, RunStatus, FORMATION_MODES, FORMATION_ALIASES

app = FastAPI(
    title="龍魂 TeamOrchestrator API",
    version="v2.0",
    description="21人格军团指挥中枢 · 协同作战API",
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"],
                   allow_headers=["*"], expose_headers=["*"])

orch = TeamOrchestrator()
orch.enable_bootstrap()  # 默认开启自举
start_time = datetime.now()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 请求/响应模型
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ExecuteRequest(BaseModel):
    task: str
    formation: str = "encirclement"
    auto_decompose: bool = True

class FormationRegisterRequest(BaseModel):
    name: str
    icon: str = "🔧"
    desc: str = ""
    personas: dict = {}
    mode: str = "chain"
    strategy: str = ""
    max_duration: int = 600

class BootstrapRequest(BaseModel):
    enabled: bool

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# API ENDPOINTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.get("/")
def root():
    return {
        "service": "龍魂 TeamOrchestrator API",
        "version": "v2.0",
        "agents": orch.agent_count,
        "uptime_seconds": int((datetime.now() - start_time).total_seconds()),
        "endpoints": {
            "POST /orchestrator/execute":            "执行一次团队协作",
            "GET /orchestrator/status/{task_id}":    "查询任务进度",
            "GET /orchestrator/after-action/{task_id}": "获取战后复盘报告",
            "GET /orchestrator/formations":          "列出所有可用军阵模式",
            "POST /orchestrator/formation/register": "注册新军阵",
            "GET /orchestrator/status":              "系统状态",
            "GET /orchestrator/history":             "历史战役列表",
            "POST /orchestrator/decompose":          "任务拆解(不执行)",
            "POST /bootstrap/toggle":                "开/关数据自举",
            "GET /bootstrap/status":                 "自举池状态",
        }
    }

@app.get("/health")
def health():
    return {"status": "ok", "agents": orch.agent_count,
            "uptime_seconds": int((datetime.now() - start_time).total_seconds())}

# ── 执行协作 ──

@app.post("/orchestrator/execute")
def execute_team(req: ExecuteRequest):
    """执行一次团队协作"""
    try:
        run = orch.execute(req.task, req.formation,
                          auto_decompose=req.auto_decompose)
        return JSONResponse({
            "task_id": run.run_id,
            "status": run.status.value,
            "task": run.task,
            "formation": run.formation or run.team_name,
            "audit": run.audit,
            "results_count": len(run.results),
            "after_action": run.after_action.dna if run.after_action else None,
        })
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))

# ── 任务进度 ──

@app.get("/orchestrator/status/{task_id}")
def get_task_status(task_id: str):
    """查询任务进度"""
    result = orch.get_task_status(task_id)
    if result is None:
        raise HTTPException(404, f"任务 {task_id} 未找到")
    return result

# ── 战后复盘 ──

@app.get("/orchestrator/after-action/{task_id}")
def get_after_action(task_id: str):
    """获取战后复盘报告"""
    report = orch.get_after_action(task_id)
    if report is None:
        raise HTTPException(404, f"复盘报告 {task_id} 未找到")
    return report

# ── 军阵模式 ──

@app.get("/orchestrator/formations")
def list_formations():
    """列出所有可用军阵模式"""
    return {
        "total": len(FORMATION_MODES),
        "aliases": dict(FORMATION_ALIASES),
        "formations": orch.list_formations(),
    }

@app.post("/orchestrator/formation/register")
def register_formation(req: FormationRegisterRequest):
    """注册新军阵"""
    result = orch.register_formation(
        name=req.name, icon=req.icon, desc=req.desc,
        personas=req.personas, mode=req.mode, strategy=req.strategy,
        max_duration=req.max_duration,
    )
    if not result["ok"]:
        raise HTTPException(400, result["error"])
    return result

# ── 系统状态 ──

@app.get("/orchestrator/status")
def system_status():
    """系统状态报告"""
    return orch.status_report()

# ── 历史 ──

@app.get("/orchestrator/history")
def list_history(limit: int = Query(20, ge=1, le=200)):
    """历史战役列表"""
    history = orch._history[-limit:]
    return [{
        "run_id": h.run_id,
        "team": h.team_name,
        "formation": h.formation,
        "task": h.task,
        "status": h.status.value,
        "audit": h.audit,
        "after_action_dna": h.after_action.dna if h.after_action else None,
        "start_time": h.start_time,
        "end_time": h.end_time,
    } for h in reversed(history)]

# ── 任务拆解(预览) ──

class DecomposeRequest(BaseModel):
    task: str
    formation: str = "encirclement"

@app.post("/orchestrator/decompose")
def preview_decompose(req: DecomposeRequest):
    """预览任务拆解结果（不执行）"""
    subtasks = orch._decomposer.decompose(req.task, req.formation)
    return {
        "task": req.task,
        "formation": req.formation,
        "subtask_count": len(subtasks),
        "subtasks": [{
            "sid": s.sid,
            "persona": s.persona,
            "priority": s.priority,
            "tier": s.tier,
            "objective": s.objective,
            "deliverable": s.deliverable,
        } for s in subtasks],
    }

# ── 数据自举 ──

@app.post("/bootstrap/toggle")
def toggle_bootstrap(req: BootstrapRequest):
    """开/关数据自举"""
    if req.enabled:
        orch.enable_bootstrap()
        return {"bootstrap": "enabled"}
    else:
        orch.disable_bootstrap()
        return {"bootstrap": "disabled"}

@app.get("/bootstrap/status")
def bootstrap_status():
    """自举池状态"""
    bs = orch._get_bootstrap() if orch._bootstrap else None
    result = {"active": orch.bootstrap_active}
    if bs:
        result.update({
            "pending_count": bs.capture.pending_count() if bs.capture else 0,
            "pool_size": bs.pool.count() if bs.pool else 0,
            "last_capture": bs.capture.last_capture if bs.capture else None,
        })
    return result

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 仪表盘
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PORTAL_DIR = SYSTEM_ROOT / "portal" / "team-orchestrator"
if PORTAL_DIR.exists():
    app.mount("/dashboard", StaticFiles(directory=str(PORTAL_DIR), html=True), name="dashboard")
    @app.get("/dashboard", response_class=HTMLResponse)
    async def dashboard():
        index = PORTAL_DIR / "index.html"
        return index.read_text(encoding="utf-8") if index.exists() else "Dashboard not found"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 启动
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    import argparse
    pp = argparse.ArgumentParser(description="TeamOrchestrator API")
    pp.add_argument("--port", type=int, default=8781)
    pp.add_argument("--host", default="0.0.0.0")
    pp.add_argument("--reload", action="store_true")
    args = pp.parse_args()

    print(f"╔══════════════════════════════════════════╗")
    print(f"║  龍魂 TeamOrchestrator API v2.0         ║")
    print(f"║  端口: {args.port} · 军阵: 5种 · 人格: {orch.agent_count}  ║")
    print(f"║  自举: {'✅ 开启' if orch.bootstrap_active else '⏸️ 暂停'}                  ║")
    print(f"╚══════════════════════════════════════════╝")

    uvicorn.run(app, host=args.host, port=args.port, reload=args.reload,
                log_level="info")
