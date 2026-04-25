#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂对话窗·记忆核心
DNA: #龍芯⚡️2026-04-19-UNIFIED-CHAT-v1.0

三重记忆检索 + 三大脑路由（本地 Ollama / DeepSeek / Claude）
数据只在本机 memory.db，一键导出走人不留痕。
"""
import os
import json
import sqlite3
import hashlib
import tarfile
from datetime import datetime
from pathlib import Path

import httpx
from fastapi import APIRouter
from pydantic import BaseModel

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.expanduser("~/longhun-system/engine/.env"))
except ImportError:
    pass

MEM_DIR = Path.home() / "longhun-system" / "engine" / "memory"
MEM_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = MEM_DIR / "memory.db"


def _init_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS msgs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            dna TEXT,
            tags TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notion_idx(
            url TEXT PRIMARY KEY,
            title TEXT,
            content TEXT,
            updated TEXT
        )
    """)
    conn.commit()
    return conn


router = APIRouter()


class ChatIn(BaseModel):
    message: str
    mode: str = "auto"  # auto / local / claude / deepseek
    context_depth: int = 10


def dna(s: str) -> str:
    h = hashlib.sha256(
        f"{s}|9622|{datetime.now().isoformat()}".encode()
    ).hexdigest()[:12]
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"#龍芯⚡️{ts}-CHAT-{h}"


async def retrieve_memory(query: str, k: int = 10):
    """三重检索·L1热/L2语义/L3结构"""
    conn = _init_db()
    rows = conn.execute(
        "SELECT content, ts FROM msgs WHERE ts > datetime('now','-7 days') "
        "ORDER BY id DESC LIMIT ?",
        (k,),
    ).fetchall()
    conn.close()
    hot = [{"type": "热", "content": r[0], "ts": r[1]} for r in rows]
    # L2/L3 占位（装 sentence-transformers + faiss 后接入）
    return {"hot": hot, "semantic": [], "structural": []}


# ──────────────────────────────────────────────
# 三大脑
# ──────────────────────────────────────────────
async def call_deepseek(prompt: str) -> str:
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key:
        return "[未配置 DEEPSEEK_API_KEY]"
    try:
        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}"},
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
            return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[DeepSeek 调用失败: {e}]"


async def call_claude(prompt: str) -> str:
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        return "[未配置 ANTHROPIC_API_KEY]"
    try:
        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-sonnet-4-5",
                    "max_tokens": 2048,
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
            return r.json()["content"][0]["text"]
    except Exception as e:
        return f"[Claude 调用失败: {e}]"


async def call_ollama(prompt: str) -> str:
    """完全离线·本地 LLM"""
    try:
        async with httpx.AsyncClient(timeout=120) as c:
            r = await c.post(
                "http://127.0.0.1:11434/api/generate",
                json={
                    "model": os.getenv("OLLAMA_MODEL", "qwen2.5:7b"),
                    "prompt": prompt,
                    "stream": False,
                },
            )
            return r.json().get("response", "[Ollama 无响应]")
    except Exception as e:
        return f"[本地 Ollama 未启动: {e}·先 ollama serve + ollama run qwen2.5:7b]"


async def route_to_brain(message: str, memory: dict, mode: str) -> str:
    """三才路由：忠(红线)→孝(根)→义(协作)"""
    # 1. 忠·红线扫描（简版）
    redlines = ["删库跑路", "泄露他人隐私", "盗用他人"]
    if any(r in message for r in redlines):
        return "🔴 红线触发·拒绝处理。UID9622 一票否决。"

    # 2. 组装上下文
    ctx_lines = ["【您的记忆片段】"]
    for m in memory["hot"][:5]:
        ctx_lines.append(f"- [{m['ts']}] {m['content'][:100]}")
    ctx = "\n".join(ctx_lines)
    prompt = f"{ctx}\n\n【当前提问】\n{message}\n\n请以龍魂人格·带 DNA·三色审计·回复。"

    # 3. 路由
    if mode == "local":
        return await call_ollama(prompt)
    if mode == "claude":
        return await call_claude(prompt)
    if mode in ("deepseek", "auto"):
        return await call_deepseek(prompt)
    return "[路由失败]"


# ──────────────────────────────────────────────
# 端点
# ──────────────────────────────────────────────
@router.post("/api/chat")
async def chat(inp: ChatIn):
    conn = _init_db()
    ts = datetime.now().isoformat()
    # 1. 存用户消息
    conn.execute(
        "INSERT INTO msgs(ts, role, content, dna, tags) VALUES(?,?,?,?,?)",
        (ts, "user", inp.message, dna(inp.message), ""),
    )
    conn.commit()
    # 2. 检索 3. 路由
    mem = await retrieve_memory(inp.message, k=inp.context_depth)
    reply = await route_to_brain(inp.message, mem, inp.mode)
    # 4. 存回复
    conn.execute(
        "INSERT INTO msgs(ts, role, content, dna, tags) VALUES(?,?,?,?,?)",
        (datetime.now().isoformat(), "assistant", reply, dna(reply), inp.mode),
    )
    conn.commit()
    conn.close()
    return {
        "reply": reply,
        "mode": inp.mode,
        "memory_used": len(mem["hot"]),
        "dna": dna(reply),
        "color": "🟢",
    }


@router.get("/api/chat/history")
def history(limit: int = 50):
    conn = _init_db()
    rows = conn.execute(
        "SELECT ts, role, content, dna FROM msgs ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return {
        "msgs": [
            {"ts": r[0], "role": r[1], "content": r[2], "dna": r[3]}
            for r in rows
        ]
    }


@router.post("/api/chat/export")
def export_all():
    """一键全量导出·主权归您·随时走人"""
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    out = Path.home() / f"longhun-export-{ts}.tar.gz"
    with tarfile.open(out, "w:gz") as t:
        t.add(MEM_DIR, arcname="memory")
    return {
        "ok": True,
        "file": str(out),
        "msg": "一键导出·走人不留痕",
        "dna": dna("export"),
    }
