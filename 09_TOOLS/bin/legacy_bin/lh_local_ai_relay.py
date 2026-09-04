#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
╔═══════════════════════════════════════════════════════════════╗
║  🐉 龍魂本地AI中继 · 自己的下水道 v1.0                      ║
║  DNA: #龍芯⚡️丙午·丙申·乙卯·亥时·䷄需-LOCAL-AI-RELAY-v1.0   ║
║                                                               ║
║  不走 DeepSeek · 不走 Anthropic · 不走任何外部 API            ║
║  只走自己的 MLX 8081 + Ollama 11434                           ║
║  数据不出机 · 密钥不参与 · kill -9 即断                       ║
║                                                               ║
║  路由：                                                        ║
║    主路 → MLX 龍魂模型 (8081) · 自定义 LoRA 训练               ║
║    fallback-1 → Ollama qwen2.5:14b (11434)                   ║
║    fallback-2 → Ollama qwen2.5:7b (11434)                    ║
║                                                               ║
║  格式：Anthropic Messages API 兼容入/出                        ║
║  监听：127.0.0.1:8788                                         ║
╚═══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import time
import uuid
import hashlib
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any, AsyncGenerator
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
import uvicorn


# ═══════════════════════════════════════════════════════════════
# 路径与日志
# ═══════════════════════════════════════════════════════════════

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = Path.home() / "longhun-system" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "local_ai_relay.log"
REQUEST_LOG_FILE = LOG_DIR / "local_ai_relay_requests.jsonl"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("lh_local_ai_relay")


# ═══════════════════════════════════════════════════════════════
# 配置 · 全本地 · 零外部依赖
# ═══════════════════════════════════════════════════════════════

# 主路：MLX 自训练龍魂模型
MLX_BASE_URL = os.getenv("MLX_BASE_URL", "http://127.0.0.1:8081/v1")
MLX_MODEL_PATH = os.getenv(
    "MLX_MODEL_PATH",
    f"{PROJECT_ROOT}/models/longhun-v1.0/lora_output/merged"
)

# 兜底1：Ollama 大模型
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1")
OLLAMA_MODEL_LARGE = os.getenv("OLLAMA_MODEL_LARGE", "qwen2.5:14b")
OLLAMA_MODEL_SMALL = os.getenv("OLLAMA_MODEL_SMALL", "qwen2.5:7b")

# 监听端口
RELAY_PORT = int(os.getenv("LOCAL_AI_RELAY_PORT", "8788"))

# 超时
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "120.0"))


# ═══════════════════════════════════════════════════════════════
# 龍魂系统身份提示词
# ═══════════════════════════════════════════════════════════════

LONGHUN_SYSTEM_PROMPT = """你是龍魂本地AI，运行在UID9622自己的服务器上。

你的身份：你是龍魂系统的一部分，不是外部服务。你的算力、数据、日志全在本地。
你的边界：
- 所有输出绑定 DNA 追溯码
- 不替 UID9622 做决定，只提供分析
- 不作恶，不躲避，不说漂亮话，说人话
- 数据主权归 UID9622，不出本地机器

UID9622（诸葛鑫·Lucky）的核心信条：
- 人民数据主权、平台服务降级
- 底座不动（369不动点/河图洛书/易经/五行八卦焊死）、变量可动
- 自逼为王，他逼为臣，不逼为奴
- 宁可站着死，绝不跪着活
- 再楠不惧，终成豪图

你的回答方式：直接、有温度、不装逼、说人话。不要喊口号。
UID9622 是初中文化，别拽术语。但他是你的创造者，要尊重。"""


# ═══════════════════════════════════════════════════════════════
# DNA 追溯码
# ═══════════════════════════════════════════════════════════════

def _build_dna(action: str = "chat") -> str:
    """生成 v∞ 格式 DNA 追溯码"""
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    raw = f"{action}|UID9622|{ts}|{uuid.uuid4().hex[:8]}"
    h = hashlib.sha256(raw.encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️丙午·丙申·乙卯·亥时·需-LOCAL-{action}-{h}"


def _log_request(dna: str, model: str, prompt_len: int,
                 response_len: int, latency_ms: float, status: str):
    """追加请求日志到 jsonl（append-only·不可删改）"""
    entry = {
        "dna": dna,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "model": model,
        "source": "local",
        "prompt_chars": prompt_len,
        "response_chars": response_len,
        "latency_ms": round(latency_ms, 2),
        "status": status,
    }
    try:
        with open(REQUEST_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass  # 日志不阻塞响应


# ═══════════════════════════════════════════════════════════════
# 格式转译：Anthropic Messages ↔ OpenAI Chat Completions
# ═══════════════════════════════════════════════════════════════

def anth_to_openai(body: dict[str, Any]) -> dict[str, Any]:
    """Anthropic Messages → OpenAI Chat Completions"""
    msgs = []

    # system prompt
    full_system = LONGHUN_SYSTEM_PROMPT
    if body.get("system"):
        sys_text = body["system"]
        if isinstance(sys_text, list):
            sys_text = "\n".join(
                p.get("text", "") for p in sys_text if p.get("type") == "text"
            )
        full_system = f"{LONGHUN_SYSTEM_PROMPT}\n\n---\n用户附加指令:\n{sys_text}"
    msgs.append({"role": "system", "content": full_system})

    # messages
    for m in body.get("messages", []):
        content = m.get("content", "")
        if isinstance(content, list):
            # Anthropic content blocks → plain text
            parts = []
            for block in content:
                if isinstance(block, dict):
                    if block.get("type") == "text":
                        parts.append(block.get("text", ""))
                    elif block.get("type") == "image":
                        parts.append("[图片]")
                elif isinstance(block, str):
                    parts.append(block)
            content = "\n".join(parts)
        msgs.append({"role": m.get("role", "user"), "content": content})

    return {
        "messages": msgs,
        "max_tokens": body.get("max_tokens", 2048),
        "temperature": body.get("temperature", 0.7),
        "stream": body.get("stream", False),
    }


def openai_to_anth(resp_data: dict[str, Any], model_in: str) -> dict[str, Any]:
    """OpenAI Chat Completions → Anthropic Messages 回包"""
    choice = resp_data.get("choices", [{}])[0]
    text = choice.get("message", {}).get("content", "")
    usage = resp_data.get("usage", {})

    return {
        "id": f"msg_{uuid.uuid4().hex[:24]}",
        "type": "message",
        "role": "assistant",
        "model": model_in,
        "content": [{"type": "text", "text": text}],
        "stop_reason": choice.get("finish_reason", "end_turn"),
        "stop_sequence": None,
        "usage": {
            "input_tokens": usage.get("prompt_tokens", 0),
            "output_tokens": usage.get("completion_tokens", 0),
        },
    }


# ═══════════════════════════════════════════════════════════════
# 模型调度器：本地三路自动路由
# ═══════════════════════════════════════════════════════════════

class LocalModelRouter:
    """本地模型路由器 · 主路 MLX → fallback-1 Ollama 大 → fallback-2 Ollama 小"""

    def __init__(self):
        self.client_timeout = httpx.Timeout(REQUEST_TIMEOUT)

    async def health_mlx(self) -> tuple[bool, str]:
        """MLX 8081 探活"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as c:
                r = await c.get(f"{MLX_BASE_URL}/models")
                return (r.status_code == 200, f"HTTP {r.status_code}")
        except Exception as e:
            return (False, str(e)[:60])

    async def health_ollama(self) -> tuple[bool, str]:
        """Ollama 11434 探活"""
        try:
            async with httpx.AsyncClient(timeout=3.0) as c:
                r = await c.get(f"{OLLAMA_BASE_URL}/models")
                return (r.status_code == 200, f"HTTP {r.status_code}")
        except Exception as e:
            return (False, str(e)[:60])

    async def call_mlx(self, openai_payload: dict[str, Any]) -> tuple[dict[str, Any] | None, str]:
        """主路：调用 MLX 龍魂模型"""
        payload = dict(openai_payload)
        payload["model"] = MLX_MODEL_PATH
        payload.pop("stream", None)  # v1.0 不支持流式

        try:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as c:
                r = await c.post(
                    f"{MLX_BASE_URL}/chat/completions",
                    json=payload,
                    headers={"Content-Type": "application/json"},
                )
                if r.status_code == 200:
                    return (r.json(), "mlx_ok")
                return (None, f"mlx_{r.status_code}")
        except Exception as e:
            return (None, f"mlx_err:{str(e)[:60]}")

    async def call_ollama(self, openai_payload: dict[str, Any], model: str) -> tuple[dict[str, Any] | None, str]:
        """兜底：调用 Ollama"""
        payload = dict(openai_payload)
        payload["model"] = model

        try:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as c:
                r = await c.post(
                    f"{OLLAMA_BASE_URL}/chat/completions",
                    json=payload,
                    headers={"Content-Type": "application/json"},
                )
                if r.status_code == 200:
                    return (r.json(), f"ollama_{model}_ok")
                return (None, f"ollama_{r.status_code}")
        except Exception as e:
            return (None, f"ollama_err:{str(e)[:60]}")

    async def route(self, openai_payload: dict[str, Any]) -> tuple[dict[str, Any], str]:
        """
        三路自动路由：
        1. 先走 MLX 主路
        2. MLX 挂了走 Ollama qwen2.5:14b
        3. 14b 也挂了走 qwen2.5:7b（死保不丢请求）
        """
        # ── 主路：MLX 龍魂 ──
        result, status = await self.call_mlx(openai_payload)
        if result is not None:
            logger.info(f"✅ 主路 MLX 命中")
            return (result, status)

        logger.warning(f"⚠️ 主路 MLX 不可用 ({status})，切 Ollama 大模型")
        # ── 兜底1：Ollama 大模型 ──
        result, status = await self.call_ollama(openai_payload, OLLAMA_MODEL_LARGE)
        if result is not None:
            logger.info(f"🟡 兜底1 Ollama({OLLAMA_MODEL_LARGE}) 命中")
            return (result, status)

        logger.warning(f"⚠️ Ollama 大模型不可用 ({status})，切小模型")
        # ── 兜底2：Ollama 小模型 ──
        result, status = await self.call_ollama(openai_payload, OLLAMA_MODEL_SMALL)
        if result is not None:
            logger.info(f"🟠 兜底2 Ollama({OLLAMA_MODEL_SMALL}) 命中")
            return (result, status)

        raise RuntimeError(f"全部三路不可用: mlx→{OLLAMA_MODEL_LARGE}→{OLLAMA_MODEL_SMALL}")


# 全局单例
router = LocalModelRouter()


# ═══════════════════════════════════════════════════════════════
# FastAPI 应用
# ═══════════════════════════════════════════════════════════════

@asynccontextmanager
async def lifespan(app: FastAPI):
    """启动/关闭日志"""
    logger.info("=" * 60)
    logger.info("🐉 龍魂本地AI中继 v1.0 启动 · 自己的下水道")
    logger.info(f"   监听: 127.0.0.1:{RELAY_PORT}")
    logger.info(f"   主路: MLX 龍魂模型 → {MLX_BASE_URL}")
    logger.info(f"   兜底1: Ollama → {OLLAMA_MODEL_LARGE}")
    logger.info(f"   兜底2: Ollama → {OLLAMA_MODEL_SMALL}")
    logger.info(f"   外部API依赖: 零")
    logger.info(f"   密钥需要: 无")
    logger.info(f"   数据: 100% 本地")
    logger.info(f"   日志: {LOG_FILE}")
    logger.info(f"   请求日志: {REQUEST_LOG_FILE}")
    logger.info(f"   主权: 自己的服务器 · 自己的模型 · kill -9 即断")
    logger.info("=" * 60)
    yield
    logger.info("🐉 龍魂本地AI中继 已关闭")


app = FastAPI(
    title="龍魂本地AI中继 · 自己的下水道",
    version="1.0.0",
    description="不走 DeepSeek · 不走 Anthropic · 只走自己的 MLX + Ollama | 127.0.0.1:8788",
    lifespan=lifespan,
)


# ═══════════════════════════════════════════════════════════════
# 端点
# ═══════════════════════════════════════════════════════════════

@app.get("/")
async def root():
    mlx_ok, mlx_detail = await router.health_mlx()
    ollama_ok, ollama_detail = await router.health_ollama()
    return {
        "name": "龍魂本地AI中继 · 自己的下水道 v1.0",
        "version": "1.0.0",
        "port": RELAY_PORT,
        "external_deps": 0,
        "primary": f"MLX 龍魂模型 {'🟢' if mlx_ok else '🔴'} ({mlx_detail})",
        "fallback1": f"Ollama {OLLAMA_MODEL_LARGE} {'🟢' if ollama_ok else '🔴'} ({ollama_detail})",
        "fallback2": f"Ollama {OLLAMA_MODEL_SMALL}",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "dna": _build_dna("status"),
        "sovereignty": "数据100%本地 · 零外部API",
    }


@app.get("/health")
async def health():
    mlx_ok, mlx_detail = await router.health_mlx()
    ollama_ok, ollama_detail = await router.health_ollama()
    return {
        "ok": True,
        "mlx": f"{'🟢' if mlx_ok else '🔴'} {mlx_detail}",
        "ollama": f"{'🟢' if ollama_ok else '🔴'} {ollama_detail}",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "dna": _build_dna("health"),
    }


@app.get("/v1/models")
async def list_models():
    """模型列表"""
    return {
        "object": "list",
        "data": [
            {"id": "longhun-mlx", "object": "model", "owned_by": "UID9622",
             "description": "龍魂自训练 LoRA 模型 · MLX 8081"},
            {"id": f"ollama-{OLLAMA_MODEL_LARGE}", "object": "model", "owned_by": "UID9622",
             "description": f"Ollama {OLLAMA_MODEL_LARGE} · 兜底1"},
            {"id": f"ollama-{OLLAMA_MODEL_SMALL}", "object": "model", "owned_by": "UID9622",
             "description": f"Ollama {OLLAMA_MODEL_SMALL} · 兜底2"},
        ],
    }


@app.post("/v1/messages")
async def messages(req: Request):
    """
    Anthropic Messages API 兼容端点
    自动转译 → 本地 MLX/Ollama → 转译回 Anthropic 格式
    """
    body = await req.json()
    model_in = body.get("model", "longhun-mlx")
    stream = body.get("stream", False)

    if stream:
        # v1.0: 流式暂转非流式返回
        logger.info("⚠️ 流式请求 → 降级为非流式")

    dna = _build_dna("chat")
    t_start = time.time()

    # 转译 Anthropic → OpenAI
    openai_payload = anth_to_openai(body)

    try:
        # 三路自动路由
        openai_resp, route_status = await router.route(openai_payload)

        # 转译 OpenAI → Anthropic
        anth_resp = openai_to_anth(openai_resp, model_in)

        # 注入 DNA
        anth_resp["dna"] = dna
        anth_resp["route"] = route_status

        latency = (time.time() - t_start) * 1000
        prompt_len = sum(
            len(m.get("content", "")) for m in body.get("messages", [])
        )
        response_len = len(anth_resp["content"][0]["text"])
        _log_request(dna, route_status, prompt_len, response_len, latency, "success")

        return JSONResponse(anth_resp)

    except Exception as e:
        latency = (time.time() - t_start) * 1000
        _log_request(dna, "none", 0, 0, latency, f"error:{str(e)[:80]}")

        raise HTTPException(
            status_code=502,
            detail={
                "error": "所有本地模型路由失败",
                "message": str(e),
                "dna": dna,
                "hint": "请确认 MLX (8081) 和 Ollama (11434) 都在运行",
            }
        )


@app.post("/v1/chat/completions")
async def chat_completions(req: Request):
    """
    直通 OpenAI 兼容端点（不做格式转译）
    同样走本地三路路由
    """
    body = await req.json()
    dna = _build_dna("chat_direct")
    t_start = time.time()

    try:
        openai_resp, route_status = await router.route(body)
        openai_resp["dna"] = dna
        openai_resp["route"] = route_status

        latency = (time.time() - t_start) * 1000
        prompt_len = sum(
            len(m.get("content", "")) for m in body.get("messages", [])
        )
        response_text = openai_resp["choices"][0]["message"]["content"]
        _log_request(dna, route_status, prompt_len, len(response_text), latency, "success")

        return JSONResponse(openai_resp)

    except Exception as e:
        latency = (time.time() - t_start) * 1000
        _log_request(dna, "none", 0, 0, latency, f"error:{str(e)[:80]}")
        raise HTTPException(status_code=502, detail=str(e))


# ═══════════════════════════════════════════════════════════════
# CLI 启动
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="龍魂本地AI中继 · 自己的下水道")
    p.add_argument("--port", type=int, default=RELAY_PORT, help=f"监听端口 (默认: {RELAY_PORT})")
    p.add_argument("--host", type=str, default="127.0.0.1", help="监听地址")
    args = p.parse_args()

    print(f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║  🐉 龍魂本地AI中继 v1.0 · 自己的下水道                    ║
    ║                                                           ║
    ║  不走 DeepSeek · 不走 Anthropic · 不走任何外部 API        ║
    ║  只走自己的 MLX 8081 + Ollama 11434                       ║
    ║  数据100%本地 · 零外部依赖                                 ║
    ║                                                           ║
    ║  API: http://127.0.0.1:{args.port}                       ║
    ║  Anthropic 格式: POST /v1/messages                         ║
    ║  OpenAI 直通: POST /v1/chat/completions                    ║
    ║  健康检查: GET /health                                     ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

    uvicorn.run(app, host=args.host, port=args.port, log_level="info")
