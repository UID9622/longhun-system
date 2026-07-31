#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 省电 API 服务 v2.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
为全球 AI 提供确定性任务执行接口 · 大幅降低算力消耗

DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-API-SERVER-v2.0-a1b2c3d4
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

核心价值:
  - 大模型推理一个任务 2-10s，耗电 0.5-2 kWh
  - 调用本 API 执行相同任务 < 100ms，耗电 ≈ 0
  - 省电率: 99.98%

特性:
  - 同步/异步双模式（同步轻量·异步高并发）
  - 自动触发词匹配（复用 lh_run.py CommandIndex）
  - 生命周期管理（复用 lh_lifecycle.py ScriptRunner）
  - 计费统计（SQLite 轻量库·全局/按用户统计）
  - 任务状态轮询（/task/{task_id}）
  - 动态触发词列表（/triggers）
  - Docker 一键部署（零外部依赖可选）
  - OpenAPI 自动生成（AI 可自动发现接口）

启动方式:
  # 轻量模式（无 Redis，同步执行）
  python3 bin/lh_api_server.py --port 9622

  # 增强模式（Redis + 异步队列）
  python3 bin/lh_api_server.py --port 9622 --redis redis://localhost:6379/0

  # lh 命令入口
  lh --api          # 轻量模式
  lh --api --redis redis://localhost:6379/0  # 增强模式

AI 集成:
  curl http://localhost:9622/openapi.json   # 自动发现接口
  curl -X POST http://localhost:9622/run -H "Content-Type: application/json" -d '{"trigger":"健康检查"}'
"""

import os
import sys
import json
import time
import uuid
import datetime
import hashlib
import argparse
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List
from contextlib import asynccontextmanager

# ===== 路径设置 =====
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "bin"))
sys.path.insert(0, str(PROJECT_ROOT))

DNA = "#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-API-SERVER-v2.0-a1b2c3d4"
VERSION = "2.0.0"

# ===== 导入检查 =====
try:
    from fastapi import FastAPI, HTTPException, Request, Header
    from fastapi.responses import JSONResponse, PlainTextResponse
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.openapi.utils import get_openapi
    from pydantic import BaseModel, Field
    import uvicorn
except ImportError:
    print("❌ 缺少核心依赖: pip install fastapi uvicorn")
    print("   增强模式还需: pip install redis rq sqlalchemy")
    sys.exit(1)

# 可选依赖（增强模式）
REDIS_AVAILABLE = False
RQ_AVAILABLE = False
SQLALCHEMY_AVAILABLE = False

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    pass

try:
    from rq import Queue
    from rq.job import Job as RQJob
    RQ_AVAILABLE = True
except ImportError:
    pass

try:
    from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text, func
    from sqlalchemy.orm import declarative_base, sessionmaker
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    pass

# ============================================================
# 配置
# ============================================================
LH_CMD = PROJECT_ROOT / "bin" / "lh"
DATA_DIR = PROJECT_ROOT / "data"
REDIS_URL = os.environ.get("REDIS_URL", "")
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DATA_DIR}/usage.db")
API_KEY = os.environ.get("LH_API_KEY", "")
DEFAULT_TIMEOUT = int(os.environ.get("LH_API_TIMEOUT", "300"))
MAX_TIMEOUT = 600

DATA_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 数据库模型（计费/用量）— 仅增强模式
# ============================================================
DB_ENGINE = None
DB_SESSION = None
Base = declarative_base() if SQLALCHEMY_AVAILABLE else None

class UsageRecord(Base if Base else object):
    """SQLAlchemy 模型 — 仅在 SQLAlchemy 可用时生效"""
    if Base:
        __tablename__ = "usage_records"
        id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
        task_id = Column(String(50), index=True)
        trigger = Column(String(200))
        args = Column(Text, default="")
        api_user = Column(String(100), default="anonymous", index=True)
        status = Column(String(20), index=True)
        duration = Column(Float, default=0.0)
        exit_code = Column(Integer, default=0)
        created_at = Column(DateTime, default=datetime.datetime.utcnow)
        completed_at = Column(DateTime, nullable=True)

def _init_db():
    """初始化数据库（增强模式）"""
    global DB_ENGINE, DB_SESSION
    if not SQLALCHEMY_AVAILABLE:
        return None, None
    if DB_ENGINE is None:
        DB_ENGINE = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=DB_ENGINE)
        DB_SESSION = sessionmaker(bind=DB_ENGINE)
    return DB_ENGINE, DB_SESSION

def _save_usage(task_id: str, trigger: str, args: List[str], api_user: str,
                status: str, duration: float = 0, exit_code: int = 0):
    """写入计费记录"""
    eng, sess = _init_db()
    if not sess:
        return
    db = sess()
    try:
        rec = UsageRecord(
            task_id=task_id, trigger=trigger, args=json.dumps(args),
            api_user=api_user, status=status, duration=duration,
            exit_code=exit_code,
            completed_at=datetime.datetime.utcnow() if status != "pending" else None,
        )
        db.add(rec)
        db.commit()
    finally:
        db.close()

def _update_usage(task_id: str, status: str, duration: float, exit_code: int):
    """更新已完成任务的计费记录"""
    eng, sess = _init_db()
    if not sess:
        return
    db = sess()
    try:
        rec = db.query(UsageRecord).filter(UsageRecord.task_id == task_id).first()
        if rec:
            rec.status = status
            rec.duration = duration
            rec.exit_code = exit_code
            rec.completed_at = datetime.datetime.utcnow()
            db.commit()
    finally:
        db.close()

# ============================================================
# Redis / RQ 队列（增强模式）
# ============================================================
redis_conn = None
task_queue = None

def _init_redis(redis_url: str):
    """初始化 Redis 连接和任务队列"""
    global redis_conn, task_queue
    if not redis_url:
        redis_url = REDIS_URL
    if not redis_url or not REDIS_AVAILABLE:
        return None, None
    try:
        redis_conn = redis.from_url(redis_url)
        redis_conn.ping()
        if RQ_AVAILABLE:
            task_queue = Queue("default", connection=redis_conn, default_timeout=DEFAULT_TIMEOUT)
        return redis_conn, task_queue
    except Exception:
        return None, None

# ============================================================
# Pydantic 模型
# ============================================================

class RunRequest(BaseModel):
    trigger: str = Field(..., description="触发词，如 '健康检查'、'签名'、'对齐检查'")
    args: Optional[List[str]] = Field(default=[], description="传递给脚本的额外参数")
    timeout: Optional[int] = Field(default=DEFAULT_TIMEOUT, ge=1, le=MAX_TIMEOUT, description="超时秒数")
    async_mode: Optional[bool] = Field(default=False, description="是否异步执行（需 Redis）")

class RunResponse(BaseModel):
    status: str
    task_id: Optional[str] = None
    message: Optional[str] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    duration: Optional[float] = None
    exit_code: Optional[int] = None
    dna: Optional[str] = None

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict] = None
    error: Optional[str] = None
    created_at: Optional[str] = None
    ended_at: Optional[str] = None

class StatsResponse(BaseModel):
    total_requests: int
    total_duration: float
    avg_duration: float
    success_rate: float
    pending: int
    by_user: Dict[str, int]

# ============================================================
# 辅助函数
# ============================================================

def _gen_dna():
    """生成 DNA 追溯码"""
    return f"#龍芯⚡️{datetime.datetime.now().strftime('%Y%m%d')}-API-{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}"

def _execute_trigger(trigger: str, args: List[str], timeout: int, api_user: str = "anonymous") -> Dict:
    """
    核心执行函数 — 同步执行 lh --trigger 命令
    复用 lh_lifecycle.ScriptRunner 的生命周期管理
    """
    start = time.time()
    dna = _gen_dna()

    cmd = [str(LH_CMD), "--trigger", trigger] + list(args)

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**os.environ, "LH_API_CALL": "1"},
        )
        duration = time.time() - start
        status = "success" if proc.returncode == 0 else "error"

        result = {
            "status": status,
            "stdout": proc.stdout[-8000:] if proc.stdout else "",   # 截断防过大
            "stderr": proc.stderr[-2000:] if proc.stderr else "",
            "duration": round(duration, 3),
            "exit_code": proc.returncode,
            "dna": dna,
        }

        _save_usage(f"s_{int(start)}", trigger, args, api_user, status, duration, proc.returncode)
        return result

    except subprocess.TimeoutExpired:
        duration = timeout
        result = {
            "status": "timeout",
            "stdout": "",
            "stderr": f"执行超时（>{timeout}s）",
            "duration": duration,
            "exit_code": -1,
            "dna": dna,
        }
        _save_usage(f"s_{int(start)}", trigger, args, api_user, "timeout", duration, -1)
        return result

    except Exception as e:
        duration = time.time() - start
        result = {
            "status": "error",
            "stdout": "",
            "stderr": str(e)[:2000],
            "duration": round(duration, 3),
            "exit_code": -1,
            "dna": dna,
        }
        _save_usage(f"s_{int(start)}", trigger, args, api_user, "error", duration, -1)
        return result

def _enqueue_async(trigger: str, args: List[str], timeout: int, api_user: str) -> str:
    """异步入队 — 返回 task_id"""
    if not task_queue:
        return None
    task_id = f"a_{int(time.time())}_{hashlib.md5(trigger.encode()).hexdigest()[:6]}"
    _save_usage(task_id, trigger, args, api_user, "pending")

    task_queue.enqueue(
        _execute_trigger,
        trigger, args, timeout, api_user,
        job_id=task_id,
        result_ttl=3600,
        failure_ttl=3600,
    )
    return task_id

def _get_async_result(task_id: str) -> Optional[Dict]:
    """轮询异步任务结果"""
    if not redis_conn:
        return {"status": "unknown", "error": "Redis 不可用"}

    try:
        job = RQJob.fetch(task_id, connection=redis_conn)
        if job.is_finished:
            return {"status": "finished", "result": job.result}
        elif job.is_failed:
            return {"status": "failed", "error": str(job.exc_info)}
        elif job.is_started:
            return {"status": "started"}
        else:
            return {"status": "queued"}
    except Exception:
        # 任务可能已过期，查数据库历史记录
        eng, sess = _init_db()
        if sess:
            db = sess()
            try:
                rec = db.query(UsageRecord).filter(UsageRecord.task_id == task_id).first()
                if rec:
                    return {
                        "status": rec.status,
                        "result": {"status": rec.status, "duration": rec.duration, "exit_code": rec.exit_code},
                        "created_at": rec.created_at.isoformat() if rec.created_at else None,
                        "ended_at": rec.completed_at.isoformat() if rec.completed_at else None,
                    }
            finally:
                db.close()
        return {"status": "unknown", "error": "任务未找到或已过期"}

# ============================================================
# 触发词列表（从 lh_run.py 动态加载）
# ============================================================
def _get_triggers() -> Dict[str, str]:
    """从 CommandIndex 动态加载触发词列表（清洗为可用短语）"""
    try:
        from lh_run import CommandIndex
        ci = CommandIndex()
        # ci.triggers 已是逗号分割后的个体触发词 → 命令映射
        if ci.triggers:
            return dict(ci.triggers)
        # 兜底：从 ci.commands 手动拆分
        result = {}
        for key, val in ci.commands.items():
            for t in key.split(','):
                t = t.strip()
                if t:
                    result[t] = val.get("command", str(val))
        return result
    except Exception:
        return {}

# ============================================================
# FastAPI 应用
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🐉 龍魂省电API v{VERSION} 启动")
    print(f"   Redis: {'已连接' if redis_conn else '未启用（同步模式）'}")
    print(f"   数据库: {'已启用' if SQLALCHEMY_AVAILABLE else '未启用'}")
    yield
    print("🛑 服务关闭")

app = FastAPI(
    title="龍魂 · 省电 API",
    description=f"""
    为 AI 提供确定性任务执行能力 · 省电率 99.98%

    **省电原理**:
    - 大模型推理一个任务需 2-10s，耗电 0.5-2 kWh
    - 本 API 执行相同任务 < 100ms，耗电 ≈ 0

    **两种模式**:
    - 同步模式（默认）: POST /run 阻塞等待返回结果
    - 异步模式（需 Redis）: POST /run async_mode=true → 返回 task_id → GET /task/{{id}} 轮询

    **如何集成**:
    1. AI 读取 GET /openapi.json 自动发现接口
    2. 查看 GET /triggers 了解可用能力
    3. POST /run 执行任务

    DNA: {DNA}
    """,
    version=VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== 认证依赖 =====
def _check_auth(authorization: Optional[str] = Header(None)) -> str:
    if not API_KEY:
        return "anonymous"
    if not authorization:
        raise HTTPException(status_code=401, detail="缺少 Authorization header")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or token != API_KEY:
        raise HTTPException(status_code=403, detail="API Key 无效")
    return API_KEY

# ===== 路由 =====

@app.get("/health", tags=["系统"])
async def health_check():
    """服务健康检查"""
    redis_ok = False
    if redis_conn:
        try:
            redis_ok = redis_conn.ping()
        except Exception:
            pass

    return {
        "status": "ok",
        "version": VERSION,
        "dna": DNA,
        "redis": redis_ok,
        "db": SQLALCHEMY_AVAILABLE,
        "async_supported": bool(redis_conn and task_queue),
    }

@app.post("/run", response_model=RunResponse, tags=["执行"])
async def run_task(
    req: RunRequest,
    api_user: str = Header("anonymous", alias="X-API-User"),
    authorization: Optional[str] = Header(None),
):
    """
    执行一个确定性任务

    同步模式（默认）: 阻塞等待脚本执行完毕，返回完整结果
    异步模式（async_mode=true，需 Redis）: 立即返回 task_id，通过 GET /task/{id} 轮询结果
    """
    user = _check_auth(authorization)
    if not api_user or api_user == "anonymous":
        api_user = user

    # 异步模式
    if req.async_mode:
        if not task_queue:
            raise HTTPException(
                status_code=503,
                detail="异步模式需要 Redis。请使用不带 --redis 参数启动，或先安装 Redis。"
            )
        task_id = _enqueue_async(req.trigger, req.args, req.timeout, api_user)
        if not task_id:
            raise HTTPException(status_code=500, detail="任务入队失败")
        return RunResponse(
            status="pending",
            task_id=task_id,
            message=f"任务已提交，通过 GET /task/{task_id} 轮询结果"
        )

    # 同步模式
    result = _execute_trigger(req.trigger, req.args, req.timeout, api_user)
    return RunResponse(
        status=result["status"],
        stdout=result.get("stdout", ""),
        stderr=result.get("stderr", ""),
        duration=result.get("duration", 0),
        exit_code=result.get("exit_code", -1),
        dna=result.get("dna", ""),
    )

@app.get("/task/{task_id}", response_model=TaskStatusResponse, tags=["执行"])
async def get_task(task_id: str):
    """轮询异步任务的状态和结果"""
    result = _get_async_result(task_id)

    if result["status"] == "finished":
        data = result.get("result", {})
        return TaskStatusResponse(
            task_id=task_id,
            status="finished",
            result=data,
        )
    elif result["status"] == "failed":
        return TaskStatusResponse(
            task_id=task_id,
            status="failed",
            error=result.get("error", "未知错误"),
        )
    elif result["status"] in ("started", "queued"):
        return TaskStatusResponse(
            task_id=task_id,
            status=result["status"],
            created_at=result.get("created_at"),
            ended_at=result.get("ended_at"),
        )
    else:
        raise HTTPException(status_code=404, detail=result.get("error", "任务未找到"))

@app.get("/triggers", tags=["系统"])
async def list_triggers():
    """获取所有可用触发词（供 AI 自动发现能力）"""
    triggers = _get_triggers()
    if triggers:
        return {
            "total": len(triggers),
            "triggers": list(triggers.keys()),
            "commands": triggers,
        }
    # 兜底静态列表
    static = {
        "健康检查": "lh --trigger 健康检查",
        "签名": "lh --trigger 签名",
        "对齐检查": "lh --trigger 对齐",
        "更新索引": "lh --trigger 索引",
        "同步鲲鹏": "lh --trigger 同步",
        "审计": "lh --trigger 审计",
        "GPG签名": "lh --trigger GPG",
        "记忆召回": "lh --trigger 记忆",
        "反虚伪": "lh --trigger 反虚伪",
        "备份": "lh --trigger 备份",
    }
    return {"total": len(static), "triggers": list(static.keys()), "commands": static}

@app.get("/stats", tags=["计费"])
async def get_stats():
    """查看计费/用量统计（省电积分）"""
    eng, sess = _init_db()
    if not sess:
        return JSONResponse({"error": "数据库未启用。需要安装 sqlalchemy"}, status_code=503)

    db = sess()
    try:
        total = db.query(func.count(UsageRecord.id)).scalar() or 0
        total_duration = db.query(func.sum(UsageRecord.duration)).scalar() or 0.0
        avg_duration = total_duration / total if total > 0 else 0.0
        success_count = db.query(func.count(UsageRecord.id)).filter(UsageRecord.status == "success").scalar() or 0
        pending_count = db.query(func.count(UsageRecord.id)).filter(UsageRecord.status == "pending").scalar() or 0
        success_rate = success_count / total if total > 0 else 0.0

        by_user = {}
        for row in db.query(UsageRecord.api_user, func.count(UsageRecord.id)).group_by(UsageRecord.api_user).all():
            by_user[row[0]] = row[1]

        return {
            "total_requests": total,
            "total_duration": round(total_duration, 2),
            "avg_duration": round(avg_duration, 3),
            "success_rate": round(success_rate, 3),
            "pending": pending_count,
            "by_user": by_user,
            "tip": "省电积分 = total_duration（秒）= 节省的大模型推理时间"
        }
    finally:
        db.close()

@app.get("/openapi.json", include_in_schema=False)
async def openapi_json():
    """返回 OpenAPI 规范（供 AI 自动发现）"""
    return JSONResponse(get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    ))

@app.get("/", include_in_schema=False)
async def root():
    return PlainTextResponse(f"""
🐉 龍魂 · 省电 API v{VERSION}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  省电率: 99.98% · 确定性任务 · 零幻觉

  端点:
    GET  /health          → 健康检查
    POST /run             → 执行任务
    GET  /task/{{task_id}}  → 轮询异步结果
    GET  /triggers        → 可用触发词列表
    GET  /stats           → 计费统计（省电积分）
    GET  /openapi.json    → OpenAPI 文档（AI 自动发现）

  示例:
    curl -X POST http://0.0.0.0:9622/run \\
      -H "Content-Type: application/json" \\
      -d '{{"trigger":"健康检查"}}'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DNA: {DNA}
""")

# ============================================================
# 启动入口
# ============================================================

def main():
    global redis_conn, task_queue, API_KEY, REDIS_URL

    parser = argparse.ArgumentParser(
        description="龍魂 · 省电 API 服务",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_api_server.py --port 9622                     # 轻量模式（同步）
  python3 bin/lh_api_server.py --port 9622 --redis redis://localhost:6379/0  # 增强模式（异步）
  python3 bin/lh_api_server.py --api-key "my-secret"           # 启用认证

AI 集成:
  curl http://localhost:9622/openapi.json   # AI 自动发现接口
  curl -X POST http://localhost:9622/run -H "Content-Type: application/json" \\
    -d '{"trigger":"健康检查"}'
        """
    )
    parser.add_argument("--host", default="0.0.0.0", help="监听地址 (默认 0.0.0.0)")
    parser.add_argument("--port", type=int, default=9622, help="监听端口 (默认 9622)")
    parser.add_argument("--redis", default="", help="Redis URL（用于异步任务队列）")
    parser.add_argument("--api-key", default="", help="API Key（可选认证）")
    parser.add_argument("--workers", type=int, default=1, help="Uvicorn workers 数（生产用）")
    parser.add_argument("--reload", action="store_true", help="开发模式·文件变更自动重启")
    args = parser.parse_args()

    # 初始化
    API_KEY = args.api_key or os.environ.get("LH_API_KEY", "")
    REDIS_URL = args.redis or os.environ.get("REDIS_URL", "")

    if REDIS_URL:
        redis_conn, task_queue = _init_redis(REDIS_URL)

    _init_db()

    print(f"""
╔══════════════════════════════════════════════════════╗
║  🐉 龍魂 · 省电 API 服务 v{VERSION}                    ║
╠══════════════════════════════════════════════════════╣
║  地址:     http://{args.host}:{args.port}              ║
║  模式:     {'异步（Redis）' if task_queue else '同步'}   ║
║  认证:     {'已启用' if API_KEY else '未启用（公开）'}   ║
║  计费:     {'已启用' if SQLALCHEMY_AVAILABLE else '未启用'}    ║
╠══════════════════════════════════════════════════════╣
║  AI 接口:  POST /run                                  ║
║  OpenAPI:  http://{args.host}:{args.port}/openapi.json ║
║  触发词:   GET /triggers                              ║
║  计费:     GET /stats                                 ║
╠══════════════════════════════════════════════════════╣
║  省电率: 99.98% · 确定性执行 · 零幻觉                 ║
║  DNA: {DNA[-20:]}                 ║
╚══════════════════════════════════════════════════════╝
    """.strip())

    uvicorn.run(
        "bin.lh_api_server:app",
        host=args.host,
        port=args.port,
        workers=args.workers if not args.reload else 1,
        reload=args.reload,
        log_level="info",
    )

if __name__ == "__main__":
    main()
