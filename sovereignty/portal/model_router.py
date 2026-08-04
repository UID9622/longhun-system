#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂模型路由 · LongHun Model Router

本地模型优先，云端能力降级：
  Ollama (localhost:11434) → Kimi API → Azure OpenAI

DNA:#龍芯⚡️2026-06-19-LONGHUN-MODEL-ROUTER-v1.0
"""

import os
import time
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api", tags=["models"])

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")

DEFAULT_LOCAL_MODEL = os.getenv("OLLAMA_DEFAULT_MODEL", "qwen2.5")


def _dna(prefix: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")[:-3]
    h = uuid.uuid4().hex[:12].upper()
    return f"#龍芯⚡️{ts}-{prefix}-{h}"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ChatRequest(BaseModel):
    messages: List[Dict[str, str]] = Field(..., min_length=1)
    provider: str = "auto"  # auto | local | deepseek
    model: Optional[str] = None
    privacy: str = "normal"  # normal | strict
    temperature: float = 0.7
    max_tokens: int = 1024


class EmbedRequest(BaseModel):
    input: str
    provider: str = "auto"  # auto | local
    model: Optional[str] = None


def probe_ollama() -> Dict[str, Any]:
    start = time.time()
    try:
        r = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        r.raise_for_status()
        data = r.json()
        models = [m.get("name", m.get("model")) for m in data.get("models", [])]
        latency = int((time.time() - start) * 1000)
        return {
            "name": "Ollama 本地模型",
            "provider": "local",
            "status": "online",
            "latency_ms": latency,
            "models": models or [DEFAULT_LOCAL_MODEL],
            "privacy": "local",
        }
    except Exception as e:
        return {
            "name": "Ollama 本地模型",
            "provider": "local",
            "status": "offline",
            "latency_ms": None,
            "models": [DEFAULT_LOCAL_MODEL],
            "privacy": "local",
            "error": str(e)[:120],
        }


def probe_deepseek() -> Dict[str, Any]:
    if not DEEPSEEK_API_KEY:
        return {
            "name": "DeepSeek API",
            "provider": "deepseek",
            "status": "offline",
            "latency_ms": None,
            "models": ["deepseek-chat", "deepseek-reasoner"],
            "privacy": "cloud",
            "error": "DEEPSEEK_API_KEY not configured",
        }
    start = time.time()
    try:
        r = requests.get(
            f"{DEEPSEEK_BASE_URL}/models",
            headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
            timeout=8,
        )
        r.raise_for_status()
        data = r.json()
        models = [m.get("id") for m in data.get("data", [])]
        latency = int((time.time() - start) * 1000)
        return {
            "name": "DeepSeek API",
            "provider": "deepseek",
            "status": "online",
            "latency_ms": latency,
            "models": models or ["deepseek-chat"],
            "privacy": "cloud",
        }
    except Exception as e:
        return {
            "name": "DeepSeek API",
            "provider": "deepseek",
            "status": "offline",
            "latency_ms": None,
            "models": ["deepseek-chat"],
            "privacy": "cloud",
            "error": str(e)[:120],
        }


def _ollama_default_model() -> str:
    try:
        r = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        data = r.json()
        models = [m.get("name", m.get("model")) for m in data.get("models", [])]
        return models[0] if models else DEFAULT_LOCAL_MODEL
    except Exception:
        return DEFAULT_LOCAL_MODEL


def chat_ollama(messages: List[Dict[str, str]], model: Optional[str], temperature: float, max_tokens: int) -> Dict[str, Any]:
    model = model or _ollama_default_model()
    body = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature, "num_predict": max_tokens},
    }
    r = requests.post(f"{OLLAMA_HOST}/api/chat", json=body, timeout=120)
    r.raise_for_status()
    data = r.json()
    reply = data.get("message", {}).get("content", "")
    return {"provider": "local", "model": model, "reply": reply}


def chat_deepseek(messages: List[Dict[str, str]], model: Optional[str], temperature: float, max_tokens: int) -> Dict[str, Any]:
    model = model or "deepseek-chat"
    body = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    r = requests.post(
        f"{DEEPSEEK_BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json",
        },
        json=body,
        timeout=120,
    )
    r.raise_for_status()
    data = r.json()
    reply = data["choices"][0]["message"]["content"]
    return {"provider": "deepseek", "model": model, "reply": reply}


@router.get("/models")
def list_models():
    """列出所有可用模型及其状态"""
    return {
        "dna": _dna("MODELS"),
        "timestamp": _now(),
        "providers": [probe_ollama(), probe_deepseek()],
    }


@router.get("/models/status")
def models_status():
    """返回简化模型状态"""
    return {
        "dna": _dna("MODEL-STATUS"),
        "timestamp": _now(),
        "providers": [probe_ollama(), probe_deepseek()],
    }


@router.post("/chat")
def chat(req: ChatRequest):
    """统一对话入口，自动按策略选择模型"""
    start = time.time()
    dna = _dna("CHAT")

    local_status = probe_ollama()
    deepseek_status = probe_deepseek()

    if req.provider not in ("auto", "local", "deepseek"):
        raise HTTPException(
            status_code=403,
            detail={
                "status": "error",
                "dna": dna,
                "timestamp": _now(),
                "message": f"provider '{req.provider}' 已被禁用，当前仅支持 auto/local/deepseek",
            },
        )

    order = []
    if req.provider == "local":
        order = [("local", local_status)]
    elif req.provider == "deepseek":
        order = [("deepseek", deepseek_status)]
    else:  # auto
        if req.privacy == "strict":
            # 隐私严格模式：只用本地
            order = [("local", local_status)]
        else:
            order = [
                ("local", local_status),
                ("deepseek", deepseek_status),
            ]

    errors = []
    for name, status in order:
        if status["status"] != "online":
            errors.append(f"{name}: not online")
            continue
        try:
            if name == "local":
                result = chat_ollama(req.messages, req.model, req.temperature, req.max_tokens)
            elif name == "deepseek":
                result = chat_deepseek(req.messages, req.model, req.temperature, req.max_tokens)
            result["latency_ms"] = int((time.time() - start) * 1000)
            result["dna"] = dna
            result["timestamp"] = _now()
            result["strategy"] = req.provider
            result["privacy"] = req.privacy
            return {"status": "ok", **result}
        except Exception as e:
            errors.append(f"{name}: {str(e)[:120]}")

    raise HTTPException(
        status_code=503,
        detail={
            "status": "error",
            "dna": dna,
            "timestamp": _now(),
            "message": "所有可用模型均调用失败",
            "errors": errors,
        },
    )


@router.post("/embed")
def embed(req: EmbedRequest):
    """统一嵌入入口，本地优先"""
    start = time.time()
    dna = _dna("EMBED")

    local_status = probe_ollama()
    if local_status["status"] == "online":
        model = req.model or _ollama_default_model()
        try:
            r = requests.post(
                f"{OLLAMA_HOST}/api/embeddings",
                json={"model": model, "prompt": req.input},
                timeout=60,
            )
            r.raise_for_status()
            data = r.json()
            return {
                "status": "ok",
                "provider": "local",
                "model": model,
                "embedding": data.get("embedding", []),
                "latency_ms": int((time.time() - start) * 1000),
                "dna": dna,
                "timestamp": _now(),
            }
        except Exception as e:
            pass  # fall through

    raise HTTPException(
        status_code=503,
        detail={
            "status": "error",
            "dna": dna,
            "timestamp": _now(),
            "message": "无可用嵌入模型",
        },
    )
