#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH·如意 API 服务 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-RUYI-API-v1.0

FastAPI服务 - 如意指令的HTTP入口。
端口: 8778 (Mac) / 8778 (鲲鹏)

端点:
  POST /api/ruyi/execute     - 提交CNSH指令并执行
  POST /api/ruyi/parse       - 仅解析指令
  POST /api/ruyi/migrate     - 代码迁移分析
  GET  /api/ruyi/status      - 服务状态
  GET  /api/ruyi/history     - 历史记录
  GET  /api/ruyi/syntax-help - 语法帮助

🐉 心意所指·万物皆成
"""

import json
import os
import sys
import time
import hashlib
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# 路径设置
_BIN_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_DIR = os.path.dirname(_BIN_DIR)
sys.path.insert(0, _PROJECT_DIR)
sys.path.insert(0, os.path.join(_PROJECT_DIR, "engines"))

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel, Field

from lh_ruyi_parser import RuyiTask, RuyiTaskAction, parse_ruyi_command, RuyiParser
from lh_ruyi_router import RuyiRouter, RuyiExecutionReport, MemoryContext, TaskStatus
from lh_ruyi_migration import RuyiMigrationEngine, MigrationReport, migrate_code


# ─── Pydantic 模型 ────────────────────────────────────

class ExecuteRequest(BaseModel):
    command: str = Field(..., description="CNSH·如意指令文本", min_length=1)
    context: Dict[str, Any] = Field(default_factory=dict, description="额外上下文")

class ExecuteResponse(BaseModel):
    dna: str
    task_name: str
    status: str
    audit_mark: str
    route_results: List[Dict[str, Any]] = []
    migration_report: Optional[Dict[str, Any]] = None
    memory_loaded: bool = False
    duration_ms: float = 0.0
    message: str = ""

class ParseResponse(BaseModel):
    task: Dict[str, Any]
    valid: bool = True
    errors: List[str] = Field(default_factory=list)

class MigrateRequest(BaseModel):
    source_code: str = Field(..., description="源代码")
    source_lang: str = Field("python", description="源语言")
    target_lang: str = Field("javascript", description="目标语言")
    source_path: str = Field("", description="源文件路径")
    target_path: str = Field("", description="目标文件路径")

class MigrateResponse(BaseModel):
    report: Dict[str, Any]
    markdown: str = ""

class StatusResponse(BaseModel):
    service: str = "CNSH·如意 API"
    version: str = "v1.0"
    status: str = "running"
    memory_connected: bool = False
    uptime_seconds: float = 0.0
    total_executions: int = 0
    last_execution: str = ""

class SyntaxHelpResponse(BaseModel):
    syntax: Dict[str, Any]
    examples: List[str]


# ─── 应用初始化 ────────────────────────────────────────

app = FastAPI(
    title="CNSH·如意 API",
    description="龍魂体系 · 多AI任务编排引擎 · 心意所指万物皆成",
    version="1.0.0",
    docs_url="/api/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化引擎（记忆API URL/Token可通过环境变量配置）
_memory_api_url = os.environ.get("MEMORY_API_URL", "http://127.0.0.1:8771/v1/memory")
_memory_api_token = os.environ.get("MEMORY_API_TOKEN") or os.environ.get("LH_MEMORY_TOKEN")
router = RuyiRouter(
    memory_api_url=_memory_api_url,
    memory_api_token=_memory_api_token,
    work_dir=Path(_PROJECT_DIR),
)
# 启动时预加载记忆上下文
try:
    router.load_memory()
except Exception as e:
    print(f"[⚠️] 启动时记忆加载失败: {e}")
migration_engine = RuyiMigrationEngine()
start_time = time.time()
execution_count = 0
last_execution_time = ""


# ─── 中间件 ────────────────────────────────────────────

@app.middleware("http")
async def add_dna_header(request: Request, call_next):
    """每个响应加DNA追踪头"""
    response = await call_next(request)
    dna = hashlib.sha256(f"{request.url}{time.time()}".encode()).hexdigest()[:12]
    response.headers["X-Ruyi-DNA"] = urllib.parse.quote(f"#龍芯⚡️RUYI-API-{dna}", safe="")
    response.headers["X-Ruyi-Version"] = "v1.0"
    return response


# ─── 路由 ──────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def root():
    """API根路径 - 返回简单HTML说明"""
    return """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head><meta charset="UTF-8"><title>CNSH·如意 API</title>
    <style>
      body { font-family: -apple-system, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; background: #0a0a0a; color: #e0c68c; }
      h1 { color: #d4a843; }
      a { color: #d4a843; }
      code { background: #1a1a1a; padding: 2px 6px; border-radius: 3px; }
      .endpoint { margin: 10px 0; padding: 10px; background: #111; border-left: 3px solid #d4a843; }
    </style></head>
    <body>
      <h1>🐉 CNSH·如意 API v1.0</h1>
      <p>龍魂体系 · 多AI任务编排引擎</p>
      <div class="endpoint"><strong>POST</strong> <code>/api/ruyi/execute</code> — 执行如意指令</div>
      <div class="endpoint"><strong>POST</strong> <code>/api/ruyi/parse</code> — 仅解析指令</div>
      <div class="endpoint"><strong>POST</strong> <code>/api/ruyi/migrate</code> — 代码迁移分析</div>
      <div class="endpoint"><strong>GET</strong> <code>/api/ruyi/status</code> — 服务状态</div>
      <div class="endpoint"><strong>GET</strong> <code>/api/ruyi/history</code> — 执行历史</div>
      <div class="endpoint"><strong>GET</strong> <code>/api/ruyi/syntax-help</code> — 语法帮助</div>
      <p style="margin-top:30px;opacity:0.5">DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-RUYI-API-v1.0</p>
    </body></html>"""


@app.post("/api/ruyi/execute", response_model=ExecuteResponse)
async def execute_command(req: ExecuteRequest):
    """
    执行CNSH·如意指令。

    接收格式:
    ```json
    {
      "command": "定义 任务 \\"生成登录页\\"\\n则 CodeBuddy 生成 前端页面",
      "context": {}
    }
    ```
    """
    global execution_count, last_execution_time

    try:
        # 1. 确保记忆加载
        if not router.memory or not router.memory.loaded:
            router.load_memory()

        # 2. 解析
        task = parse_ruyi_command(req.command)

        # 3. 执行
        report = router.route(task)

        execution_count += 1
        last_execution_time = datetime.now().isoformat()

        # 4. 构造响应
        return ExecuteResponse(
            dna=report.dna,
            task_name=task.task_name,
            status=report.status,
            audit_mark=report.audit_mark,
            route_results=report.route_results,
            migration_report=report.migration_report,
            memory_loaded=report.memory_loaded,
            duration_ms=report.duration_ms,
            message=f"任务「{task.task_name}」执行完成 · 审计{report.audit_mark}",
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"指令解析失败: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"执行失败: {e}")


@app.post("/api/ruyi/parse", response_model=ParseResponse)
async def parse_command(req: ExecuteRequest):
    """仅解析指令，不执行"""
    errors = []
    try:
        task = parse_ruyi_command(req.command)
        return ParseResponse(task=task.to_dict(), valid=True, errors=errors)
    except ValueError as e:
        errors.append(str(e))
        return ParseResponse(task={}, valid=False, errors=errors)


@app.post("/api/ruyi/migrate", response_model=MigrateResponse)
async def analyze_migration(req: MigrateRequest):
    """代码迁移分析"""
    try:
        report = migration_engine.analyze_and_migrate(
            source_code=req.source_code,
            source_lang=req.source_lang,
            target_lang=req.target_lang,
            source_path=req.source_path,
            target_path=req.target_path,
        )
        return MigrateResponse(
            report=report.to_dict(),
            markdown=report.to_markdown(),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"迁移分析失败: {e}")


@app.get("/api/ruyi/status", response_model=StatusResponse)
async def get_status():
    """服务状态"""
    mem_connected = bool(router.memory and router.memory.loaded)
    return StatusResponse(
        memory_connected=mem_connected,
        uptime_seconds=time.time() - start_time,
        total_executions=execution_count,
        last_execution=last_execution_time,
    )


@app.get("/api/ruyi/history")
async def get_history(limit: int = 10):
    """执行历史"""
    history = router._execution_history[-limit:]
    return {
        "count": len(history),
        "items": [h.to_dict() for h in reversed(history)],
    }


@app.get("/api/ruyi/syntax-help", response_model=SyntaxHelpResponse)
async def get_syntax_help():
    """CNSH·如意语法帮助"""
    return SyntaxHelpResponse(
        syntax={
            "关键词": ["定义", "任务", "设", "为", "则", "最后", "转移", "至", "并"],
            "AI角色": ["CodeBuddy (鲁班·工程)", "Kimi (画师·设计)", "华云道 (织女·渲染)"],
            "动作": ["生成", "优化", "检测", "转移", "渲染", "修复", "搭建"],
            "结构": "定义 任务 → 设 属性 → 则 分派 → 最后 转移",
        },
        examples=[
            '定义 任务 "生成用户登录页"\n设 风格 为 "简约商务风"\n设 技术栈 为 ["React", "TypeScript"]\n则 CodeBuddy 生成 前端页面\n则 Kimi 优化 视觉风格\n最后 转移 代码 至 华云道 渲染',
            '定义 任务 "修复支付bug"\n设 技术栈 为 Python, FastAPI\n则 CodeBuddy 修复 支付回调逻辑\n则 CodeBuddy 检测 变量冲突',
            '定义 任务 "Python转JavaScript"\n则 CodeBuddy 转移 Python脚本 至 JavaScript\n则 CodeBuddy 检测 变量映射',
        ],
    )


# ─── 启动 ──────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("RUYI_PORT", 8778))
    host = os.environ.get("RUYI_HOST", "0.0.0.0")

    print(f"""
    ╔══════════════════════════════════════════════╗
    ║   🐉 CNSH·如意 API v1.0                      ║
    ║   端口: {port}                                  ║
    ║   文档: http://{host}:{port}/api/docs            ║
    ║   入口: http://{host}:{port}                     ║
    ║   DNA:  #龍芯⚡️丙午·RUYI-API-v1.0            ║
    ╚══════════════════════════════════════════════╝
    """)

    uvicorn.run(app, host=host, port=port, log_level="info")
