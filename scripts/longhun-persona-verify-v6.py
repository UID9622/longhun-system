# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂人格验证服务 v6.0 — 训练状态 + 时间轴API
DNA: #龍芯⚡️丙午·辛未·PERSONA-VERIFY-v6.0

FastAPI 服务，端口 9623，提供:
  GET  /training/status     — 训练状态（面板每2秒轮询）
  GET  /training/timeline   — AI进化时间轴
  GET  /training/timeline/stats — 时间轴统计
  GET  /training/history    — 训练历史
  GET  /model/version       — 当前模型版本
  GET  /health              — 健康检查
"""

import json
import os
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

LONGHUN_ROOT = Path.home() / "longhun-system"
SCRIPTS_DIR = LONGHUN_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import importlib
TrainingMonitor = importlib.import_module('longhun-training-monitor').TrainingMonitor
TrainingHistory = importlib.import_module('longhun-training-monitor').TrainingHistory

DNA = "UID9622-ONLY-ONCE🧬LK9X-772Z"
CST = timezone(timedelta(hours=8))

app = FastAPI(
    title="龍魂人格验证服务 v6.0",
    description="训练状态 + AI进化时间轴 API",
    version="6.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _format_time(seconds: int) -> str:
    if seconds < 0:
        return "0s"
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m{seconds % 60}s"
    else:
        h = seconds // 3600
        m = (seconds % 3600) // 60
        return f"{h}h{m:02d}m"


def _format_datetime(ts: int) -> str:
    if not ts:
        return "-"
    return datetime.fromtimestamp(ts, CST).strftime("%Y-%m-%d %H:%M")


# ═══════════════════════════════════════════════════════
# 健康检查
# ═══════════════════════════════════════════════════════

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "longhun-persona-verify-v6",
        "dna": DNA,
        "timestamp": int(time.time()),
        "timestamp_str": _format_datetime(int(time.time())),
    }


# ═══════════════════════════════════════════════════════
# 模型版本
# ═══════════════════════════════════════════════════════

@app.get("/model/version")
async def model_version():
    return TrainingMonitor.get_model_version()


# ═══════════════════════════════════════════════════════
# 训练状态（面板轮询核心）
# ═══════════════════════════════════════════════════════

@app.get("/training/status")
async def training_status():
    """获取当前训练状态（面板每2秒轮询）"""
    status = TrainingMonitor.get_status()

    # 计算剩余时间
    if status.get("state") in ["preparing", "training", "validating", "switching"]:
        remaining = max(0, status.get("estimated_complete", 0) - int(time.time()))
        status["remaining_seconds"] = remaining
        status["remaining_formatted"] = _format_time(remaining)

    # 计算已用时间
    if status.get("started_at"):
        elapsed = int(time.time()) - status["started_at"]
        status["elapsed_seconds"] = elapsed
        status["elapsed_formatted"] = _format_time(elapsed)

    return status


# ═══════════════════════════════════════════════════════
# 训练历史
# ═══════════════════════════════════════════════════════

@app.get("/training/history")
async def training_history(limit: int = Query(default=10, le=50)):
    """获取训练历史（扫描完成标记文件）"""
    from longhun_training_monitor import MODEL_DIR as MD
    done_files = sorted(Path(MD).glob(".training_done_v*"), reverse=True)
    history = []
    for f in done_files[:limit]:
        try:
            data = json.loads(f.read_text())
            history.append(data)
        except Exception:
            pass

    return {
        "total": len(history),
        "history": history,
    }


# ═══════════════════════════════════════════════════════
# 时间轴
# ═══════════════════════════════════════════════════════

@app.get("/training/timeline")
async def training_timeline(limit: int = Query(default=20, le=100)):
    """获取AI模型进化时间轴"""
    timeline = TrainingHistory.get_timeline(limit=limit)

    formatted = []
    for item in timeline:
        evo = item.get("evolution", {})

        formatted.append({
            "version": item["version"],
            "badge": f"AIv{item['version']}",
            "trained_at": item["trained_at"],
            "trained_at_formatted": _format_datetime(item["trained_at"]),
            "metrics": {
                "accuracy": round(item["metrics"]["accuracy"] * 100, 1),
                "f1": round(item["metrics"]["f1"] * 100, 1),
                "samples": item["metrics"]["training_samples"],
                "samples_k": round(item["metrics"]["training_samples"] / 1000, 1),
                "duration_seconds": item["metrics"]["training_duration"],
                "duration_formatted": _format_time(item["metrics"]["training_duration"]),
            },
            "evolution": {
                "accuracy_delta": round(evo.get("accuracy_delta", 0) * 100, 2),
                "accuracy_trend": "up" if evo.get("accuracy_delta", 0) > 0 else "down" if evo.get("accuracy_delta", 0) < 0 else "flat",
                "samples_delta": evo.get("samples_delta", 0),
                "time_since_last": evo.get("time_since_last", 0),
                "time_since_last_formatted": _format_time(evo.get("time_since_last", 0)),
            },
            "trigger": item.get("trigger_reason", "unknown"),
            "dna": item.get("dna", DNA),
        })

    evolution_path = " → ".join([f"AIv{i['version']}" for i in formatted])
    stats = TrainingHistory.get_stats()

    return {
        "evolution_path": evolution_path,
        "total_versions": len(formatted),
        "stats": {
            "total_versions": stats["total_versions"],
            "best_accuracy": stats["best_accuracy"],
            "avg_accuracy": stats["avg_accuracy"],
            "total_samples_growth": stats["total_samples_growth"],
            "training_frequency_per_day": stats["training_frequency"],
        },
        "timeline": formatted,
        "latest": formatted[-1] if formatted else None,
    }


@app.get("/training/timeline/stats")
async def timeline_stats():
    """时间轴统计摘要"""
    return TrainingHistory.get_stats()


# ═══════════════════════════════════════════════════════
# 启动
# ═══════════════════════════════════════════════════════

@app.on_event("startup")
async def startup_check():
    """启动时检查残留训练状态"""
    print("🐉 龍魂人格验证服务 v6.0 启动中...")
    if TrainingMonitor.is_training():
        print("⚠️ 检测到训练进程运行中")
    else:
        status = TrainingMonitor.get_status()
        if status.get("state") in ["preparing", "training", "validating", "switching"]:
            print("🧹 清理残留训练状态")
            status_file = Path.home() / "longhun-system" / "models" / ".training_status"
            status_file.write_text(json.dumps({
                "state": "idle", "stage": "就绪",
                "dna": DNA, "progress": 0,
                "from_version": 0, "to_version": 0,
                "started_at": 0, "estimated_complete": 0,
                "completed_at": 0, "metrics": {}, "error": None,
            }))
    print(f"   DNA: {DNA}")
    print(f"   端口: 9623")


if __name__ == "__main__":
    uvicorn.run(
        "longhun_persona_verify_v6:app",
        host="0.0.0.0",
        port=9623,
        reload=False,
        log_level="info",
    )
