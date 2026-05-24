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

from typing import Any, Dict, List, Optional

import httpx
from fastapi import APIRouter
from pydantic import BaseModel, Field

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


class LocalChatIn(BaseModel):
    """POST /api/chat/local — 直连 Ollama /api/chat（多轮），不经过三大脑路由。"""

    messages: Optional[List[Dict[str, Any]]] = None
    message: str = ""
    stream: bool = False
    dna_assemble: bool = Field(
        default=False,
        description="true 时按 user_dna_profile 重组知识切片注入上下文（放大强项·不打乱思路）",
    )
    model: Optional[str] = Field(
        default=None,
        description="覆盖 LONGHUN_OLLAMA_MODEL / OLLAMA_MODEL，例如 longhun-9622",
    )


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
    """完全离线·本地 LLM（单轮 generate，供 mode=local 旧路径）"""
    model = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
    try:
        async with httpx.AsyncClient(timeout=120) as c:
            r = await c.post(
                "http://127.0.0.1:11434/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                },
            )
            return r.json().get("response", "[Ollama 无响应]")
    except Exception as e:
        return f"[本地 Ollama 未启动: {e}·先 ollama serve；模型 {model}]"


OLLAMA_CHAT_URL = "http://127.0.0.1:11434/api/chat"


@router.post("/api/chat/assemble")
def chat_assemble(body: Dict[str, Any]):
    """仅做 DNA 切片重组 + 决策链，不调模型。"""
    from dna_slice_router import assemble_slices

    q = str(body.get("query") or body.get("message") or "").strip()
    if not q:
        return {"ok": False, "error": "query 不能为空"}
    out = assemble_slices(q, max_slices=body.get("max_slices"))
    out["dna"] = dna("dna-assemble")
    return out


@router.post("/api/chat/local")
async def chat_local(inp: LocalChatIn):
    """
    龍魂本地对话：Ollama /api/chat（支持 messages 多轮）。
    不写入 memory.db（与 /api/chat 解耦）；需要落库可再调用 /api/chat 或后续加开关。
    """
    if inp.stream:
        return {
            "ok": False,
            "error": "9625 当前只封装 stream=false；流式请直接 POST 127.0.0.1:11434/api/chat",
        }
    assemble_meta: Optional[Dict[str, Any]] = None
    msgs = inp.messages
    if not msgs:
        if not (inp.message or "").strip():
            return {"ok": False, "error": "messages 或 message 至少填一个"}
        user_text = inp.message.strip()
        if inp.dna_assemble:
            from dna_slice_router import assemble_slices

            assemble_meta = assemble_slices(user_text)
            prefix = assemble_meta.get("context_prefix") or ""
            if prefix:
                user_text = f"{prefix}\n\n---\n\n【你的问题·按你节奏回答·勿替你做主】\n{user_text}"
        msgs = [{"role": "user", "content": user_text}]
    model = (
        (inp.model or "").strip()
        or os.getenv("LONGHUN_OLLAMA_MODEL", "").strip()
        or os.getenv("OLLAMA_MODEL", "qwen2.5:7b").strip()
    )
    try:
        async with httpx.AsyncClient(timeout=300.0) as c:
            r = await c.post(
                OLLAMA_CHAT_URL,
                json={"model": model, "messages": msgs, "stream": False},
            )
    except Exception as e:
        return {"ok": False, "error": f"连不上 Ollama: {e}", "hint": "先执行: ollama serve"}
    if r.status_code != 200:
        return {
            "ok": False,
            "error": r.text or "Ollama 非 200",
            "status_code": r.status_code,
        }
    try:
        data = r.json()
    except Exception as e:
        return {"ok": False, "error": f"解析 Ollama 响应失败: {e}", "raw": r.text[:500]}
    msg = data.get("message") or {}
    content = (msg.get("content") or "").strip()
    if not content:
        return {"ok": False, "error": "Ollama 返回空 content", "raw": data}
    tag = dna("ollama-local-chat")
    signed = f"{content}\n\n{tag}\n#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
    out: Dict[str, Any] = {
        "ok": True,
        "model": data.get("model", model),
        "message": {"role": "assistant", "content": signed},
        "done": data.get("done", True),
        "dna": tag,
    }
    if assemble_meta:
        out["dna_assemble"] = {
            "slices": assemble_meta.get("slices"),
            "decision_chain": assemble_meta.get("decision_chain"),
            "mode": assemble_meta.get("mode"),
        }
    return out


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
