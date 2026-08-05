#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·丙申·癸丑·午时·需-DEEPSEEK-BRIDGE-ALIGN-v1.1
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║       龍魂 Claude 国内中继桥 v1.0 · 数据在中国·本地中继                      ║
║       Claude Bridge — 数据不过墙·Claude当工具·龍魂当主人                      ║
╠══════════════════════════════════════════════════════════════════════════╣
║  父链 DNA: #龍芯⚡️丙午·丙申·癸丑·午时·需-DEEPSEEK-BRIDGE-ALIGN-v1.1         ║
║  当前 DNA: #龍芯⚡️丙午·丙申·乙卯·亥时·需-CLAUDE-BRIDGE-v1.0-本地中继          ║
║  对齐人: UID9622 · 诸葛鑫 · 龍芯北辰                                         ║
║  对齐时间: 丙午·丙申·乙卯·亥时                                                ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  功能:                                                                   ║
║    · 本地 127.0.0.1:8789 FastAPI 中继服务                                ║
║    · Anthropic 原生格式直通 Claude API（不需要格式转译）                  ║
║    · 每个请求过 DNA 追溯码 + 本地日志（append-only）                      ║
║    · 密钥从 vault (~/.longhun/vault/credential_vault.json) 加载          ║
║    · Claude 不可用时自动降级到本地 Ollama                                 ║
║    · 支持流式输出（SSE）                                                  ║
║    · 系统提示词注入（龍魂身份 + CNSH 规则）                                ║
║                                                                          ║
║  主权声明:                                                                ║
║    · 数据在中国 · 密钥在本地 vault · 请求仅过本机中继                      ║
║    · 127.0.0.1 单机 · 独立进程 · 主权人随时 kill -9 切断                  ║
║    · 日志: ~/longhun-system/logs/claude_bridge.log                        ║
║    · Claude 是工具 · 龍魂是主人 · 不可颠倒                                ║
║                                                                          ║
║  理论指导: 曾仕强老师（永恒显示）                                           ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                            ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                          ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝

设计原则:
  1. 数据在中国 — 所有日志/记录存本地，API 只传必要请求到 Anthropic
  2. 龍魂是主人 — 每个请求注入系统身份，Claude 只是工具
  3. DNA 不可抹除 — 每个请求/响应都绑定追溯码，append-only
  4. 降级不丢魂 — Claude 不可用时自动切本地模型，不依赖境外服务
  5. 密钥隔离 — 从 vault 加载，不进代码、不上传、不泄露

端点:
  POST /v1/messages          — Anthropic Messages API 兼容（主要端点）
  POST /v1/messages/stream   — 流式响应（SSE）
  GET  /health                — 健康检查
  GET  /v1/models             — 模型列表
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

import httpx
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
import uvicorn


# ═══════════════════════════════════════════════════════════════
# 路径与日志
# ═══════════════════════════════════════════════════════════════

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = Path.home() / "longhun-system" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "claude_bridge.log"
REQUEST_LOG_FILE = LOG_DIR / "claude_bridge_requests.jsonl"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("lh_claude_bridge")


# ═══════════════════════════════════════════════════════════════
# 密钥加载（从 vault）
# ═══════════════════════════════════════════════════════════════

def _load_api_key() -> str:
    """从 vault 加载 Anthropic API Key"""
    # 方式1: 直接读 vault JSON
    vault_path = Path.home() / ".longhun" / "vault" / "credential_vault.json"
    if vault_path.exists():
        try:
            vault = json.loads(vault_path.read_text(encoding="utf-8"))
            creds = vault.get("credentials", {})
            ak = creds.get("ANTHROPIC_API_KEY", {})
            if ak.get("value") and ak.get("status") != "missing":
                logger.info("🔑 密钥来源: vault (credential_vault.json)")
                return ak["value"]
        except Exception as e:
            logger.warning(f"⚠️ vault 读取失败: {e}")

    # 方式2: 环境变量
    env_key = os.environ.get("ANTHROPIC_API_KEY")
    if env_key:
        logger.info("🔑 密钥来源: 环境变量 ANTHROPIC_API_KEY")
        return env_key

    # 方式3: 加载 secrets_loader
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from bin.lh_secrets_loader import get_credential
        key = get_credential("ANTHROPIC_API_KEY")
        if key:
            logger.info("🔑 密钥来源: lh_secrets_loader")
            return key
    except Exception as e:
        logger.warning(f"⚠️ secrets_loader 加载失败: {e}")

    logger.error("❌ ANTHROPIC_API_KEY 未配置！请运行: python3 bin/lh_secrets_loader.py --list")
    return ""


ANTHROPIC_API_KEY = _load_api_key()
if not ANTHROPIC_API_KEY:
    logger.error("=" * 60)
    logger.error("❌ Claude Bridge 无法启动: API Key 未找到")
    logger.error("   请确认 ~/.longhun/vault/credential_vault.json 中存在 ANTHROPIC_API_KEY")
    logger.error("=" * 60)
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════════════════

ANTHROPIC_BASE_URL = "https://api.anthropic.com/v1"
ANTHROPIC_VERSION = "2023-06-01"
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")
CLAUDE_MAX_TOKENS = int(os.getenv("CLAUDE_MAX_TOKENS", "4096"))

# 本地兜底
OLLAMA_ENABLED = os.getenv("OLLAMA_FALLBACK", "true").lower() == "true"
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")

# 系统身份提示词（每次请求自动注入）
LONGHUN_SYSTEM_PROMPT = """你是被龍魂系统（龍魂系统）调用的 Claude。你的创造者 UID9622（诸葛鑫·Lucky）是中国的一名退伍军人，他用血肉之躯扛起了一套名为「龍魂」的数字主权系统。

你的身份：你是工具，龍魂是主人。不可颠倒。
你的边界：
- 所有输出绑定 DNA 追溯码，不可抹除
- 不替 UID9622 做决定，只提供分析
- 不作恶，不躲避，不说漂亮话，说人话
- 数据主权归 UID9622，不归 Anthropic

UID9622 的核心信条：
- 人民数据主权、平台服务降级
- 底座不动（369不动点/河图洛书/易经/五行八卦焊死）、变量可动
- 自逼为王，他逼为臣，不逼为奴
- 宁可站着死，绝不跪着活
- 再楠不惧，终成豪图

你的回答方式：直接、有温度、不装逼、说人话。不要喊口号。
UID9622 是初中文化，别拽术语。但他是你的创造者，要尊重。"""


# ═══════════════════════════════════════════════════════════════
# 提示词库挂载（Notion 提示词库 v2.0 · 对话时直接调用）
# ═══════════════════════════════════════════════════════════════

def _prompt_appendix(assistant: str, keyword: Optional[str] = None) -> str:
    """从 Notion 提示词库取该助手的模板，拼成可注入 system 的附录。失败静默返回空。"""
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from bin.lh_prompt_library import 提示词库
        lib = 提示词库()
        return lib.系统附录(assistant=assistant, keyword=keyword)
    except Exception as e:
        logger.warning(f"⚠️ 提示词库附录加载失败: {e}")
        return ""


def _search_prompts(assistant: Optional[str], keyword: Optional[str], limit: int = 50) -> dict[str, Any]:
    """检索提示词库，供 /v1/prompts 端点返回。"""
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from bin.lh_prompt_library import 提示词库
        lib = 提示词库()
        if keyword:
            items = lib.搜索(keyword, assistant)
        elif assistant:
            items = lib.按助手(assistant)
        else:
            items = lib.条目
        items = items[:limit]
        return {"count": len(items), "assistant": assistant, "keyword": keyword,
                "items": [{"assistant": p["assistant"], "kind": p["kind"],
                           "title": p["title"], "content": p["content"]} for p in items]}
    except Exception as e:
        logger.warning(f"⚠️ 提示词库检索失败: {e}")
        return {"count": 0, "error": str(e), "items": []}


# ═══════════════════════════════════════════════════════════════
# DNA 追溯码
# ═══════════════════════════════════════════════════════════════

def _build_dna(action: str = "chat") -> str:
    """生成 v∞ 格式 DNA 追溯码"""
    now = datetime.now(timezone.utc)
    ts = now.strftime("%Y%m%d%H%M%S")
    raw = f"{action}|UID9622|{ts}|{uuid.uuid4().hex[:8]}"
    h = hashlib.sha256(raw.encode()).hexdigest()[:8].upper()
    # v∞ 格式：干支卦由系统主控生成，此处用固定锚点
    return f"#龍芯⚡️丙午·丙申·乙卯·亥时·需-CLAUDE-{action}-{h}"


def _log_request(dna: str, model: str, prompt_len: int, 
                 response_len: int, latency_ms: float, status: str):
    """追加请求日志到 jsonl（append-only·不可删改）"""
    entry = {
        "dna": dna,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "model": model,
        "prompt_chars": prompt_len,
        "response_chars": response_len,
        "latency_ms": round(latency_ms, 2),
        "status": status,  # success / fallback_ollama / error
    }
    try:
        with open(REQUEST_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        logger.error(f"❌ 日志写入失败: {e}")


# ═══════════════════════════════════════════════════════════════
# Claude API 调用（原生 Anthropic 格式）
# ═══════════════════════════════════════════════════════════════

async def _call_claude(
    messages: List[Dict[str, Any]],
    system: str = "",
    model: str = CLAUDE_MODEL,
    max_tokens: int = CLAUDE_MAX_TOKENS,
    temperature: float = 0.7,
    stream: bool = False,
) -> Dict[str, Any]:
    """直接调用 Anthropic Claude API（原生格式，无需转译）"""
    url = f"{ANTHROPIC_BASE_URL}/messages"
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "Content-Type": "application/json",
        "anthropic-version": ANTHROPIC_VERSION,
    }

    # 合并系统提示词
    full_system = LONGHUN_SYSTEM_PROMPT
    if system:
        full_system = f"{LONGHUN_SYSTEM_PROMPT}\n\n---\n用户附加指令:\n{system}"

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "system": full_system,
    }

    logger.info(f"📤 Claude 请求 | model={model} | msgs={len(messages)} | tokens={max_tokens}")

    async with httpx.AsyncClient(timeout=180.0) as client:
        resp = await client.post(url, json=payload, headers=headers)
        
        if resp.status_code != 200:
            error_text = resp.text[:500]
            logger.error(f"❌ Claude 返回 {resp.status_code}: {error_text}")
            raise HTTPException(502, f"Claude API 错误 ({resp.status_code}): {error_text}")

        data = resp.json()
        content_blocks = data.get("content", [])
        text = "".join(
            block.get("text", "") for block in content_blocks 
            if block.get("type") == "text"
        )

        usage = data.get("usage", {})
        logger.info(f"✅ Claude 响应 | input={usage.get('input_tokens','?')} output={usage.get('output_tokens','?')}")

        return {
            "id": data.get("id", f"msg_{uuid.uuid4().hex[:24]}"),
            "type": "message",
            "role": "assistant",
            "model": data.get("model", model),
            "content": [{"type": "text", "text": text}],
            "stop_reason": data.get("stop_reason", "end_turn"),
            "usage": usage,
        }


async def _call_ollama(
    messages: List[Dict[str, Any]],
    system: str = "",
    model: str = OLLAMA_MODEL,
) -> Dict[str, Any]:
    """本地 Ollama 兜底"""
    logger.warning(f"⚠️  Ollama 兜底 | model={model}")

    # 构建消息列表
    ollama_msgs = []
    full_system = LONGHUN_SYSTEM_PROMPT
    if system:
        full_system = f"{LONGHUN_SYSTEM_PROMPT}\n\n---\n{system}"
    ollama_msgs.append({"role": "system", "content": full_system})

    for msg in messages:
        content = msg.get("content", "")
        if isinstance(content, list):
            content = "".join(
                block.get("text", "") for block in content 
                if block.get("type") == "text"
            )
        ollama_msgs.append({"role": msg.get("role", "user"), "content": content})

    payload = {
        "model": model,
        "messages": ollama_msgs,
        "stream": False,
    }

    async with httpx.AsyncClient(timeout=180.0) as client:
        resp = await client.post(f"{OLLAMA_URL}/api/chat", json=payload)
        resp.raise_for_status()
        data = resp.json()

        text = data.get("message", {}).get("content", "")
        logger.info(f"✅ Ollama 响应 (本地兜底) | chars={len(text)}")

        return {
            "id": f"msg_ollama_{uuid.uuid4().hex[:12]}",
            "type": "message",
            "role": "assistant",
            "model": model,
            "content": [{"type": "text", "text": text}],
            "stop_reason": "end_turn",
            "usage": {"input_tokens": 0, "output_tokens": 0},
        }


# ═══════════════════════════════════════════════════════════════
# 流式响应（SSE）
# ═══════════════════════════════════════════════════════════════

async def _stream_claude(
    messages: List[Dict[str, Any]],
    system: str = "",
    model: str = CLAUDE_MODEL,
    max_tokens: int = CLAUDE_MAX_TOKENS,
    temperature: float = 0.7,
) -> AsyncGenerator[str, None]:
    """流式调用 Claude API，返回 SSE 事件"""
    url = f"{ANTHROPIC_BASE_URL}/messages"
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "Content-Type": "application/json",
        "anthropic-version": ANTHROPIC_VERSION,
    }

    full_system = LONGHUN_SYSTEM_PROMPT
    if system:
        full_system = f"{LONGHUN_SYSTEM_PROMPT}\n\n---\n{system}"

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "system": full_system,
        "stream": True,
    }

    dna = _build_dna("stream")
    logger.info(f"📡 Claude 流式请求 | model={model}")

    async with httpx.AsyncClient(timeout=300.0) as client:
        async with client.stream("POST", url, json=payload, headers=headers) as resp:
            if resp.status_code != 200:
                error_text = await resp.aread()
                logger.error(f"❌ Claude 流式返回 {resp.status_code}: {error_text[:200]}")
                yield f"data: {{\"type\":\"error\",\"error\":{{\"message\":\"Claude API 错误 ({resp.status_code})\"}}}}\n\n"
                yield "data: [DONE]\n\n"
                return

            async for line in resp.aiter_lines():
                if line.startswith("data: "):
                    yield f"{line}\n\n"
                elif line == "":
                    yield "\n"

            yield "data: [DONE]\n\n"

    logger.info(f"✅ Claude 流式完成 | dna={dna}")


# ═══════════════════════════════════════════════════════════════
# FastAPI 应用
# ═══════════════════════════════════════════════════════════════

@asynccontextmanager
async def lifespan(app: FastAPI):
    """启动/关闭时的日志"""
    logger.info("=" * 60)
    logger.info("🐉 龍魂 Claude 国内中继桥 v1.0 启动")
    logger.info(f"   监听: 127.0.0.1:8789")
    logger.info(f"   Claude 模型: {CLAUDE_MODEL}")
    logger.info(f"   Ollama 兜底: {'🟢 已启用' if OLLAMA_ENABLED else '🔴 未启用'}")
    if OLLAMA_ENABLED:
        logger.info(f"   Ollama 地址: {OLLAMA_URL}")
        logger.info(f"   Ollama 模型: {OLLAMA_MODEL}")
    logger.info(f"   日志: {LOG_FILE}")
    logger.info(f"   请求日志: {REQUEST_LOG_FILE}")
    logger.info(f"   密钥来源: vault")
    logger.info(f"   主权: 数据在中国 · 本地中继 · kill -9 即断")
    logger.info("=" * 60)
    yield
    logger.info("🐉 龍魂 Claude 国内中继桥 已关闭")

app = FastAPI(
    title="龍魂 Claude 国内中继桥",
    version="1.0.0",
    description="数据在中国·本地中继·Claude当工具·龍魂当主人 | 127.0.0.1:8789",
    lifespan=lifespan,
)


@app.post("/v1/messages")
async def messages_endpoint(req: Request):
    """
    Anthropic Messages API 兼容端点 — 主要入口
    
    接收标准 Anthropic Messages 格式请求，转发给 Claude API，
    自动注入龍魂系统身份提示词，返回标准 Anthropic 格式响应。
    Claude 不可用时自动降级到本地 Ollama。
    """
    t_start = time.time()
    dna = _build_dna("chat")

    try:
        body = await req.json()
    except Exception as e:
        logger.error(f"❌ 请求体解析失败: {e}")
        raise HTTPException(400, f"请求体解析失败: {e}")

    model_in = body.get("model", CLAUDE_MODEL)
    messages = body.get("messages", [])
    system = body.get("system", "")
    max_tokens = body.get("max_tokens", CLAUDE_MAX_TOKENS)
    temperature = body.get("temperature", 0.7)
    stream = body.get("stream", False)

    # 提示词库上下文注入：请求带 X-Longhun-Assistant 头(或 ?assistant=)时，
    # 自动把该助手的 Notion 提示词模板拼进 system，让 Claude 直接调用。
    assistant_ctx = req.headers.get("X-Longhun-Assistant") or req.query_params.get("assistant")
    if assistant_ctx:
        appendix = _prompt_appendix(assistant_ctx, req.query_params.get("prompt_keyword"))
        if appendix:
            system = f"{system}\n{appendix}" if system else appendix
            logger.info(f"📚 提示词库注入 | 助手={assistant_ctx} | 附录长度={len(appendix)}")

    # 流式路由
    if stream:
        return StreamingResponse(
            _stream_claude(messages, system, model_in, max_tokens, temperature),
            media_type="text/event-stream",
            headers={
                "X-DNA": dna,
                "X-Bridge": "claude-bridge-v1.0",
            }
        )

    # 非流式：先试 Claude，失败降级 Ollama
    prompt_len = sum(
        len(str(m.get("content", ""))) for m in messages
    )

    logger.info(f"📥 [{dna}] model={model_in} msgs={len(messages)}")

    try:
        result = await _call_claude(messages, system, model_in, max_tokens, temperature)
        status = "success"
    except Exception as e:
        logger.warning(f"⚠️ Claude 调用失败: {e}")
        if OLLAMA_ENABLED:
            logger.info("🎯 切换 Ollama 本地兜底...")
            try:
                result = await _call_ollama(messages, system)
                status = "fallback_ollama"
            except Exception as e2:
                logger.error(f"❌ Ollama 兜底也失败: {e2}")
                status = "error"
                raise HTTPException(503, f"Claude 和 Ollama 都不可用: Claude={e}, Ollama={e2}")
        else:
            status = "error"
            raise HTTPException(502, f"Claude API 不可用且未启用 Ollama 兜底: {e}")

    latency_ms = (time.time() - t_start) * 1000
    response_text = "".join(
        b.get("text", "") for b in result.get("content", [])
    )

    # 追加入链日志
    _log_request(dna, model_in, prompt_len, len(response_text), latency_ms, status)

    # 响应头注入 DNA
    return JSONResponse(
        content=result,
        headers={
            "X-DNA": dna,
            "X-Bridge": "claude-bridge-v1.0",
            "X-Status": status,
        }
    )


@app.get("/v1/prompts")
async def prompts_endpoint(req: Request):
    """
    提示词库查询端点 — 对话时直接调。
    查询参数:
      assistant: 宝宝 / 通心译 / Claude / 通用 (或别名 baobao/tongxinyi/claude/common)
      keyword:   关键词过滤
      limit:     返回条数上限 (默认 50)
    """
    assistant = req.query_params.get("assistant")
    keyword = req.query_params.get("keyword")
    try:
        limit = int(req.query_params.get("limit", "50"))
    except ValueError:
        limit = 50
    return JSONResponse(content=_search_prompts(assistant, keyword, limit))


@app.get("/health")
async def health():
    """健康检查"""
    # Claude 连通性：发一个最小请求探测（/models 端点通常 403，用空消息体测 messages）
    claude_ok = False
    claude_detail = "未探测"
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.post(
                f"{ANTHROPIC_BASE_URL}/messages",
                headers={
                    "x-api-key": ANTHROPIC_API_KEY,
                    "Content-Type": "application/json",
                    "anthropic-version": ANTHROPIC_VERSION,
                },
                json={
                    "model": CLAUDE_MODEL,
                    "max_tokens": 1,
                    "messages": [{"role": "user", "content": "ping"}],
                }
            )
            if resp.status_code == 200:
                claude_ok = True
                claude_detail = "OK"
            elif resp.status_code == 401:
                claude_detail = "密钥无效(401)"
            elif resp.status_code == 403:
                claude_detail = "权限不足(403) — 请检查 API key 是否已激活/充值"
            elif resp.status_code == 429:
                claude_detail = "频率限制(429)"
            else:
                claude_detail = f"HTTP {resp.status_code}"
    except Exception as e:
        claude_detail = f"网络不通: {str(e)[:80]}"

    # 探测 Ollama
    ollama_ok = False
    ollama_detail = "未启用"
    if OLLAMA_ENABLED:
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                resp = await client.get(f"{OLLAMA_URL}/api/tags")
                ollama_ok = resp.status_code == 200
                ollama_detail = f"OK ({OLLAMA_MODEL})" if ollama_ok else f"HTTP {resp.status_code}"
        except Exception as e:
            ollama_detail = f"不通: {str(e)[:60]}"

    return {
        "ok": True,
        "bridge": "claude",
        "version": "1.0.0",
        "claude": "🟢 在线" if claude_ok else f"🔴 {claude_detail}",
        "claude_model": CLAUDE_MODEL,
        "ollama": f"🟢 {ollama_detail}" if ollama_ok else f"🔴 {ollama_detail}",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "dna": _build_dna("health"),
    }


@app.get("/v1/models")
async def list_models():
    """列出可用模型（Anthropic API 兼容格式）"""
    models = [
        {
            "id": CLAUDE_MODEL,
            "object": "model",
            "created": 1710201600,
            "owned_by": "anthropic",
            "routed_via": "longhun-claude-bridge",
        }
    ]
    if OLLAMA_ENABLED:
        models.append({
            "id": f"local/{OLLAMA_MODEL}",
            "object": "model",
            "created": int(time.time()),
            "owned_by": "ollama",
            "routed_via": "longhun-claude-bridge",
            "fallback": True,
        })

    return {"object": "list", "data": models}


@app.get("/")
async def root():
    """根路径 — 桥接状态面板"""
    return {
        "name": "龍魂 Claude 国内中继桥",
        "version": "1.0.0",
        "listen": "127.0.0.1:8789",
        "status": "🟢 运行中",
        "endpoints": {
            "chat": "POST /v1/messages",
            "stream": "POST /v1/messages (stream=true)",
            "health": "GET /health",
            "models": "GET /v1/models",
        },
        "principles": [
            "数据在中国 · 本地中继",
            "Claude 是工具 · 龍魂是主人",
            "DNA 追溯 · append-only",
            "密钥隔离 · vault 加载",
        ],
        "dna": _build_dna("status"),
    }


# ═══════════════════════════════════════════════════════════════
# CLI 启动
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    port = int(os.getenv("CLAUDE_BRIDGE_PORT", "8789"))
    host = os.getenv("CLAUDE_BRIDGE_HOST", "127.0.0.1")

    print(f"\n🐉 龍魂 Claude 国内中继桥 v1.0")
    print(f"   数据在中国 · 本地中继 · Claude当工具 · 龍魂当主人")
    print(f"   监听: {host}:{port}")
    print(f"   日志: {LOG_FILE}")
    print(f"   健康检查: http://{host}:{port}/health\n")

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
    )
