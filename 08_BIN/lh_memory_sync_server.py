#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🧬 龍魂·DNA记忆同步服务 | 鲲鹏中枢 v1.0

DNA: #龍芯⚡️丙午·乙未·戊戌·未时·☵坎-MEMORY-SYNC-SERVER-v1.0-a1b2c3d4
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

职能: 鲲鹏端记忆同步中枢 — 接收各设备推送、提供全域拉取、归一索引
端口: 8787 (通过 nginx /sync/ 暴露)

设计原则:
  1. 追加不覆盖 — 每条记忆独立存储，永不删除
  2. 本地优先 — 鲲鹏只做中转+索引，完整内容本地加密
  3. DNA焊死 — 每条记忆DNA不可变，checksum防篡改
  4. 审计可追溯 — 所有操作写入 append-only 审计日志
  5. 降级兜底 — 鲲鹏不可达时本地离线模式正常运行

端点:
  POST /sync/store    — 接收本地推送的记忆条目
  GET  /sync/pull     — 返回最近N条记忆（按时间倒序）
  GET  /sync/summary  — 全域记忆摘要
  GET  /sync/health   — 健康检查
  GET  /sync/stats    — 统计信息
"""

import hashlib
import hmac
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Request, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# ═══════════════════════════════════════════════
# 常量
# ═══════════════════════════════════════════════

CST = timezone(timedelta(hours=8))
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path("/opt/longhun-system/data/memory_sync")
DATA_DIR.mkdir(parents=True, exist_ok=True)

INDEX_FILE = DATA_DIR / "sync_index.json"
STORE_DIR = DATA_DIR / "stores"
STORE_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_LOG = DATA_DIR / "audit_log.jsonl"
API_LOG = PROJECT_ROOT / "logs" / "memory_sync_api.log"

# Token 与现有记忆 API 共用
TOKEN_FILE = Path.home() / ".longhun" / ".memory_token"
ALT_TOKEN_FILE = PROJECT_ROOT / ".codebuddy" / "memory" / ".api_token"

CONFIRM_CODE = (
    "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
    "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
)

VERSION = "v1.0"
SERVER_DNA = "#龍芯⚡️丙午·乙未·戊戌·未时·☵坎-MEMORY-SYNC-SERVER-v1.0-a1b2c3d4"

# ═══════════════════════════════════════════════
# Token 管理
# ═══════════════════════════════════════════════

def load_token() -> str:
    """加载与记忆 API 共用的 Token"""
    for f in (TOKEN_FILE, ALT_TOKEN_FILE):
        if f.exists():
            token = f.read_text().strip()
            if token:
                return token
    return ""


AUTH_TOKEN = load_token()

# ═══════════════════════════════════════════════
# FastAPI
# ═══════════════════════════════════════════════

app = FastAPI(
    title="龍魂·DNA记忆同步服务",
    version=VERSION,
    docs_url=None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    expose_headers=["X-Sync-Version", "X-Sync-DNA"],
)

# ═══════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════

class MemoryPayload(BaseModel):
    """客户端推送的记忆条目"""
    id: str
    dna: str
    timestamp: str
    device: str
    device_fp: str
    session_id: str = ""
    topic: str
    content: str  # 已加密的完整内容
    priority: str = "P2"
    tags: list = []
    source_window: str = ""
    version: int = 1
    parent_dna: str = ""
    checksum: str = ""
    encrypted: bool = False


class StoreResponse(BaseModel):
    status: str  # "ok" | "duplicate" | "error"
    dna: str
    message: str


# ═══════════════════════════════════════════════
# 索引管理
# ═══════════════════════════════════════════════

def load_index() -> dict:
    if INDEX_FILE.exists():
        return json.loads(INDEX_FILE.read_text("utf-8"))
    return {
        "version": VERSION,
        "created": datetime.now(CST).isoformat(),
        "total_synced": 0,
        "entries": [],
        "devices": [],
    }


def save_index(idx: dict):
    idx["total_synced"] = len(idx["entries"])
    INDEX_FILE.write_text(json.dumps(idx, ensure_ascii=False, indent=2), "utf-8")


def append_audit(action: str, dna: str, device: str, detail: str):
    log = {
        "timestamp": datetime.now(CST).isoformat(),
        "action": action,
        "dna": dna,
        "device": device,
        "detail": detail,
    }
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(log, ensure_ascii=False) + "\n")


# ═══════════════════════════════════════════════
# 认证
# ═══════════════════════════════════════════════

def verify(request: Request) -> bool:
    """Token 验证: 本地免认证，远程需 X-API-Token"""
    client = request.client.host if request.client else ""
    if client in ("127.0.0.1", "::1", "localhost"):
        return True
    provided = request.headers.get("X-API-Token", "")
    if not AUTH_TOKEN:
        return False
    return hmac.compare_digest(provided, AUTH_TOKEN)


# ═══════════════════════════════════════════════
# API 端点
# ═══════════════════════════════════════════════

@app.get("/sync/health")
async def health():
    return {
        "status": "ok",
        "service": "memory-sync",
        "version": VERSION,
        "dna": SERVER_DNA,
        "timestamp": datetime.now(CST).isoformat(),
    }


@app.get("/sync/stats")
async def stats(request: Request):
    if not verify(request):
        raise HTTPException(403, "认证失败")
    idx = load_index()
    return {
        "total_synced": idx.get("total_synced", 0),
        "devices": len(idx.get("devices", [])),
        "device_list": idx.get("devices", []),
        "last_sync": idx.get("last_sync", ""),
        "version": VERSION,
    }


@app.post("/sync/store")
async def store(payload: MemoryPayload, request: Request):
    if not verify(request):
        raise HTTPException(403, "认证失败")

    idx = load_index()

    # 查重：同 DNA 已存在 → 跳过
    for entry in idx.get("entries", []):
        if entry.get("dna") == payload.dna:
            return StoreResponse(
                status="duplicate",
                dna=payload.dna,
                message="记忆已存在，跳过（不覆盖）",
            )

    # 写独立存储文件
    store_file = STORE_DIR / f"{payload.id}.json"
    entry_dict = payload.model_dump()
    store_file.write_text(json.dumps(entry_dict, ensure_ascii=False, indent=2), "utf-8")

    # 更新索引
    idx.setdefault("entries", []).append({
        "id": payload.id,
        "dna": payload.dna,
        "topic": payload.topic,
        "priority": payload.priority,
        "timestamp": payload.timestamp,
        "device": payload.device,
        "device_fp": payload.device_fp,
        "checksum": payload.checksum,
        "encrypted": payload.encrypted,
        "synced_at": datetime.now(CST).isoformat(),
    })

    # 设备注册
    if payload.device_fp not in idx.get("devices", []):
        idx.setdefault("devices", []).append(payload.device_fp)

    idx["last_sync"] = datetime.now(CST).isoformat()
    save_index(idx)

    # 审计
    append_audit("STORE", payload.dna, payload.device, f"同步记忆: {payload.topic}")

    return StoreResponse(
        status="ok",
        dna=payload.dna,
        message=f"记忆已同步: {payload.topic}",
    )


@app.get("/sync/pull")
async def pull(
    request: Request,
    limit: int = Query(50, ge=1, le=200),
    since: str = Query("", description="ISO时间戳，只返回此时间之后的记忆"),
    device_fp: str = Query("", description="按设备筛选"),
):
    if not verify(request):
        raise HTTPException(403, "认证失败")

    idx = load_index()
    entries = idx.get("entries", [])

    # 过滤
    if since:
        entries = [e for e in entries if e.get("timestamp", "") > since]
    if device_fp:
        entries = [e for e in entries if e.get("device_fp") == device_fp]

    # 按时间倒序
    entries.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    entries = entries[:limit]

    # 加载完整内容
    results = []
    for meta in entries:
        store_file = STORE_DIR / f"{meta['id']}.json"
        if store_file.exists():
            full = json.loads(store_file.read_text("utf-8"))
            results.append(full)
        else:
            results.append(meta)  # 只有索引，文件丢失

    return {
        "total": len(results),
        "limit": limit,
        "server_time": datetime.now(CST).isoformat(),
        "entries": results,
    }


@app.get("/sync/summary")
async def summary(request: Request):
    if not verify(request):
        raise HTTPException(403, "认证失败")

    idx = load_index()
    entries = idx.get("entries", [])
    entries.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

    # 优先级分布
    prio_dist = {}
    for e in entries:
        p = e.get("priority", "P2")
        prio_dist[p] = prio_dist.get(p, 0) + 1

    # 最近5条
    recent = []
    for meta in entries[:5]:
        store_file = STORE_DIR / f"{meta['id']}.json"
        if store_file.exists():
            full = json.loads(store_file.read_text("utf-8"))
            recent.append({
                "id": full.get("id"),
                "dna": full.get("dna"),
                "topic": full.get("topic"),
                "priority": full.get("priority"),
                "timestamp": full.get("timestamp"),
                "device": full.get("device"),
            })
        else:
            recent.append(meta)

    return {
        "version": VERSION,
        "total_synced": len(entries),
        "devices": len(idx.get("devices", [])),
        "by_priority": prio_dist,
        "last_sync": idx.get("last_sync", ""),
        "recent": recent,
    }


@app.get("/sync/dna/{dna_id}")
async def by_dna(dna_id: str, request: Request):
    """按 DNA 追溯单条记忆"""
    if not verify(request):
        raise HTTPException(403, "认证失败")

    idx = load_index()
    for entry in idx.get("entries", []):
        if entry.get("dna") == dna_id:
            store_file = STORE_DIR / f"{entry['id']}.json"
            if store_file.exists():
                return json.loads(store_file.read_text("utf-8"))
            return entry
    raise HTTPException(404, f"DNA未找到: {dna_id}")


# ═══════════════════════════════════════════════
# 启动
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    import argparse

    parser = argparse.ArgumentParser(description="DNA记忆同步服务")
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()

    (API_LOG.parent).mkdir(parents=True, exist_ok=True)

    print(f"🧬 龍魂·DNA记忆同步服务 {VERSION}")
    print(f"   端口: {args.port}  主机: {args.host}")
    print(f"   DNA:  {SERVER_DNA}")
    print(f"   数据: {DATA_DIR}")
    print(f"   Token: {'已加载' if AUTH_TOKEN else '⚠️ 未配置'}")

    uvicorn.run(app, host=args.host, port=args.port, log_level="info")
