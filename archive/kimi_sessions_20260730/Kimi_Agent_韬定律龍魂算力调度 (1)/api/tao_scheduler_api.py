#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·韬定律调度器 HTTP API v2.2
DNA: #龍芯⚡️丙午·乙未·辛酉·姤-TAO-LAW-INTEGRATED-v2.2

- FastAPI + uvicorn
- 默认 Unix socket: /tmp/lh_test/tao_scheduler.sock
- 可选 --host/--port 走 TCP
- 64 卦执行位默认落 SQLite（.db 后缀自动识别后端）
- 静态文件挂载 /static/tao-scheduler/ 提供 Web UI
"""

import argparse
import contextlib
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

# 把项目根目录加入 Python 路径，保证能 import engines
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engines.tao_scheduler import (
    DEFAULT_LAYER,
    GUA_MASTER,
    SIGNAL_RULES,
    AuditLog,
    GuaSlotManager,
    TaoScheduler,
    sha256_hex,
)

# ═══════════════════════════════════════════════════════════
# 全局状态（由 lifespan 初始化）
# ═══════════════════════════════════════════════════════════

SCHEDULER: Optional[TaoScheduler] = None
APP_VERSION = "2.2.0"


# ═══════════════════════════════════════════════════════════
# 配置模型
# ═══════════════════════════════════════════════════════════

class AppConfig:
    data_dir: Path = Path("/tmp/lh_test")
    slot_file: Optional[Path] = None
    log_file: Optional[Path] = None
    cred_dir: Optional[Path] = None
    unix_socket: Path = Path("/tmp/lh_test/tao_scheduler.sock")


CONFIG = AppConfig()


# ═══════════════════════════════════════════════════════════
# 生命周期
# ═══════════════════════════════════════════════════════════

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    global SCHEDULER
    CONFIG.data_dir.mkdir(parents=True, exist_ok=True)
    slot_file = CONFIG.slot_file or (CONFIG.data_dir / "gua_slots.db")
    log_file = CONFIG.log_file or (CONFIG.data_dir / "tao_audit.log")
    cred_dir = CONFIG.cred_dir or (CONFIG.data_dir / "etc")
    SCHEDULER = TaoScheduler(
        cred_dir=str(cred_dir),
        log_file=str(log_file),
        slot_file=str(slot_file),
    )
    yield
    # 关闭时无需显式动作；SQLite 连接由 GuaSlotManager 持有


app = FastAPI(
    title="龍魂·韬定律调度器 API",
    version=APP_VERSION,
    lifespan=lifespan,
)


# ═══════════════════════════════════════════════════════════
# 挂载静态文件：Web UI
# ═══════════════════════════════════════════════════════════

STATIC_DIR = ROOT / "portal"
if (STATIC_DIR / "tao-scheduler" / "index.html").exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ═══════════════════════════════════════════════════════════
# 请求/响应模型（用原生 dict，不依赖 pydantic 复杂模型）
# ═══════════════════════════════════════════════════════════

@app.get("/health")
def health():
    """健康检查与运行状态"""
    slot_count = 0
    log_lines = 0
    if SCHEDULER:
        slot_count = len(SCHEDULER.slots.slots)
        if SCHEDULER.audit.log_file.exists():
            log_lines = len(SCHEDULER.audit.log_file.read_text().strip().splitlines())
    return {
        "status": "ok",
        "version": APP_VERSION,
        "data_dir": str(CONFIG.data_dir),
        "slot_file": str(CONFIG.slot_file or CONFIG.data_dir / "gua_slots.db"),
        "log_file": str(CONFIG.log_file or CONFIG.data_dir / "tao_audit.log"),
        "slot_count": slot_count,
        "audit_log_lines": log_lines,
    }


@app.get("/config")
def config():
    """返回路由规则与卦位配置"""
    return {
        "signal_rules": [
            {"pattern": pat, "layer": layer} for pat, layer in SIGNAL_RULES
        ],
        "default_layer": DEFAULT_LAYER,
        "gua_master": {
            gua: {"layer": layer, "task_type": task}
            for gua, (layer, task) in GUA_MASTER.items()
        },
    }


@app.post("/schedule")
def schedule(payload: Dict):
    """提交任务并返回路由结果"""
    if SCHEDULER is None:
        raise HTTPException(status_code=503, detail="调度器尚未初始化")
    req = payload.get("request", "")
    if not isinstance(req, str) or not req:
        raise HTTPException(status_code=400, detail='请求体须包含非空字符串字段 "request"')
    result = SCHEDULER.schedule(req)
    return result


@app.get("/slots")
def list_slots():
    """返回全部 64 卦执行位状态"""
    if SCHEDULER is None:
        raise HTTPException(status_code=503, detail="调度器尚未初始化")
    return {"slots": list(SCHEDULER.slots.slots.values())}


@app.post("/slots/{addr}/freeze")
def freeze_slot(addr: str):
    """冻结指定执行位（P0：只解冻不删除）"""
    if SCHEDULER is None:
        raise HTTPException(status_code=503, detail="调度器尚未初始化")
    if addr not in SCHEDULER.slots.slots:
        raise HTTPException(status_code=404, detail=f"执行位不存在: {addr}")
    SCHEDULER.slots.freeze(addr)
    return {"addr": addr, "state": "frozen"}


@app.post("/slots/{addr}/release")
def release_slot(addr: str):
    """释放指定执行位"""
    if SCHEDULER is None:
        raise HTTPException(status_code=503, detail="调度器尚未初始化")
    if addr not in SCHEDULER.slots.slots:
        raise HTTPException(status_code=404, detail=f"执行位不存在: {addr}")
    SCHEDULER.slots.release(addr)
    return {"addr": addr, "state": "free"}


@app.get("/audit/chain")
def audit_chain(limit: int = Query(100, ge=1, le=10000)):
    """返回最近审计日志条目"""
    if SCHEDULER is None:
        raise HTTPException(status_code=503, detail="调度器尚未初始化")
    log_file = SCHEDULER.audit.log_file
    if not log_file.exists():
        return {"entries": [], "total": 0}
    lines = log_file.read_text().strip().splitlines()
    entries = []
    for line in lines[-limit:]:
        parts = line.rsplit(",", 1)
        if len(parts) == 2:
            payload, record_hash = parts
        else:
            payload, record_hash = line, ""
        fields = payload.split(",")
        if len(fields) >= 8:
            entries.append(
                {
                    "timestamp": fields[0],
                    "layer": fields[1],
                    "task_type_hash": fields[2],
                    "duration_sec": fields[3],
                    "energy_mj": fields[4],
                    "call_count": fields[5],
                    "route_priority": fields[6],
                    "prev_hash": fields[7],
                    "record_hash": record_hash,
                    "raw": line,
                }
            )
        else:
            entries.append({"raw": line})
    return {"entries": entries, "total": len(lines)}


@app.post("/audit/verify")
def audit_verify():
    """校验审计链完整性"""
    if SCHEDULER is None:
        raise HTTPException(status_code=503, detail="调度器尚未初始化")
    ok, breaks = SCHEDULER.audit.verify_chain()
    total = 0
    if SCHEDULER.audit.log_file.exists():
        total = len(SCHEDULER.audit.log_file.read_text().strip().splitlines())
    return {"intact": ok, "breaks": breaks, "total": total}


# ═══════════════════════════════════════════════════════════
# 统一异常处理
# ═══════════════════════════════════════════════════════════

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"内部错误: {exc}", "path": request.url.path},
    )


# ═══════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="龍魂·韬定律调度器 API v2.2")
    parser.add_argument("--data-dir", default="/tmp/lh_test", help="数据根目录（默认 /tmp/lh_test）")
    parser.add_argument("--slot-file", help="执行位状态文件（默认 <data-dir>/gua_slots.db）")
    parser.add_argument("--log-file", help="审计日志路径（默认 <data-dir>/tao_audit.log）")
    parser.add_argument("--cred-dir", help="凭证目录（默认 <data-dir>/etc）")
    parser.add_argument("--host", help="TCP 监听地址；若未指定则使用 Unix socket")
    parser.add_argument("--port", type=int, help="TCP 监听端口；默认 8788")
    parser.add_argument("--uds", default="/tmp/lh_test/tao_scheduler.sock", help="Unix socket 路径")
    args = parser.parse_args()

    CONFIG.data_dir = Path(args.data_dir)
    CONFIG.data_dir.mkdir(parents=True, exist_ok=True)
    if args.slot_file:
        CONFIG.slot_file = Path(args.slot_file)
    if args.log_file:
        CONFIG.log_file = Path(args.log_file)
    if args.cred_dir:
        CONFIG.cred_dir = Path(args.cred_dir)
    CONFIG.unix_socket = Path(args.uds)

    if args.host or args.port:
        host = args.host or "127.0.0.1"
        port = args.port or 8788
        print(f"[TAO-API] TCP 模式: http://{host}:{port}/")
        uvicorn.run(app, host=host, port=port, log_level="info")
    else:
        CONFIG.unix_socket.parent.mkdir(parents=True, exist_ok=True)
        # 清理旧 socket，避免 bind 失败
        if CONFIG.unix_socket.exists():
            CONFIG.unix_socket.unlink()
        print(f"[TAO-API] Unix socket 模式: {CONFIG.unix_socket}")
        print("[TAO-API] Web UI: http://<反向代理>/static/tao-scheduler/index.html")
        uvicorn.run(app, uds=str(CONFIG.unix_socket), log_level="info")


if __name__ == "__main__":
    main()
