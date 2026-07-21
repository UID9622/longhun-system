#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 DeepSeek API 中继桥·走下水道方案 v1.0
DeepSeek Bridge for Anthropic SDK - Local Relay Translator

父链 DNA:#龍芯⚡️2026-05-31-23:44-DEEPSEEK-BRIDGE-FILE7-v1.0
当前 DNA:#龍芯⚡️2026-07-04-DEEPSEEK-BRIDGE-ALIGN-v1.1
M号: M266
对齐人: UID9622 · 诸葛鑫 · 龍芯北辰
对齐时间: 2026-07-04

功能: 本地127.0.0.1:8788跑FastAPI·Anthropic格式入·DeepSeek格式出
密钥: 独立进程·独立.env·chmod 600·永不入业务代码

主权声明:
  · 密钥本地 ~/.deepseek_bridge.env (chmod 600)
  · 桥127.0.0.1单机·TLS由DeepSeek终止
  · 中继桥独立进程·主权人随时kill -9切断
  · 日志: ~/longhun-system/logs/deepseek_bridge.log

理论指导: 曾仕强老师（永恒显示）

CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import os
import sys
import json
import time
import uuid
import logging
from datetime import datetime
from typing import Dict, List, Optional, AsyncGenerator, Any
from dataclasses import dataclass, asdict
from pathlib import Path

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
import uvicorn

# ==================== 日志配置 ====================
log_dir = Path.home() / "longhun-system" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "deepseek_bridge.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ==================== 配置加载 ====================
# 从 ~/.deepseek_bridge.env 加载密钥（绝对不从git/notion）
env_file = Path.home() / ".deepseek_bridge.env"
if not env_file.exists():
    logger.error(f"❌ 密钥文件不存在: {env_file}")
    logger.error("请先执行: echo 'DEEPSEEK_API_KEY=sk-xxx' > ~/.deepseek_bridge.env && chmod 600 ~/.deepseek_bridge.env")
    sys.exit(1)

load_dotenv(env_file)
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    logger.error("❌ DEEPSEEK_API_KEY 未设置")
    sys.exit(1)

DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
OLLAMA_FALLBACK = os.getenv("OLLAMA_FALLBACK", "false").lower() == "true"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")

logger.info(f"🚀 DeepSeek Bridge 启动中...")
logger.info(f"   DeepSeek Model: {DEEPSEEK_MODEL}")
logger.info(f"   Ollama Fallback: {OLLAMA_FALLBACK}")
if OLLAMA_FALLBACK:
    logger.info(f"   Ollama URL: {OLLAMA_BASE_URL}")
    logger.info(f"   Ollama Model: {OLLAMA_MODEL}")

# ==================== 数据结构 ====================
@dataclass
class AnthropicMessage:
    """Anthropic Messages API 请求格式"""
    model: str
    messages: List[Dict]
    max_tokens: int = 1024
    temperature: float = 0.7
    system: Optional[str] = None
    stream: bool = False


# ==================== 格式转译 ====================
def anthropic_to_openai(body: dict[str, Any]) -> dict[str, Any]:
    """
    Anthropic Messages API → OpenAI Chat Completions

    Anthropic格式:
      {
        "model": "claude-3-5-sonnet",
        "max_tokens": 1024,
        "system": "...",
        "messages": [
          {"role": "user", "content": "..."},
          {"role": "assistant", "content": "..."}
        ]
      }

    OpenAI格式:
      {
        "model": "deepseek-chat",
        "messages": [
          {"role": "system", "content": "..."},
          {"role": "user", "content": "..."}
        ],
        "max_tokens": 1024,
        "temperature": 0.7
      }
    """
    messages = []

    # 1. 系统提示词
    if body.get("system"):
        system_content = body["system"]
        if isinstance(system_content, list):
            # Anthropic支持content_block列表
            system_content = "".join(
                block.get("text", "")
                for block in system_content
                if block.get("type") == "text"
            )
        messages.append({
            "role": "system",
            "content": system_content
        })

    # 2. 对话历史
    for msg in body.get("messages", []):
        role = msg.get("role")
        content = msg.get("content")

        # 处理content_block列表
        if isinstance(content, list):
            text_content = "".join(
                block.get("text", "")
                for block in content
                if block.get("type") == "text"
            )
        else:
            text_content = content or ""

        if text_content:
            messages.append({
                "role": role,
                "content": text_content
            })

    return {
        "model": DEEPSEEK_MODEL,
        "messages": messages,
        "max_tokens": body.get("max_tokens", 1024),
        "temperature": body.get("temperature", 0.7),
        "stream": body.get("stream", False),
    }


def openai_to_anthropic(response: dict[str, Any], model_in: str) -> dict[str, Any]:
    """
    OpenAI Chat Completions → Anthropic Messages API 回包

    OpenAI回包:
      {
        "choices": [
          {
            "message": {
              "role": "assistant",
              "content": "..."
            }
          }
        ],
        "usage": {
          "prompt_tokens": 100,
          "completion_tokens": 50
        }
      }

    Anthropic回包:
      {
        "id": "msg_xxx",
        "type": "message",
        "role": "assistant",
        "model": "claude-3-5-sonnet",
        "content": [
          {"type": "text", "text": "..."}
        ],
        "stop_reason": "end_turn",
        "usage": {
          "input_tokens": 100,
          "output_tokens": 50
        }
      }
    """
    try:
        text = response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as e:
        logger.error(f"❌ 回包格式错误: {e}, response={response}")
        raise ValueError(f"无法解析OpenAI回包: {e}")

    usage = response.get("usage", {})

    return {
        "id": f"msg_{uuid.uuid4().hex[:24]}",
        "type": "message",
        "role": "assistant",
        "model": model_in,
        "content": [
            {
                "type": "text",
                "text": text
            }
        ],
        "stop_reason": "end_turn",
        "usage": {
            "input_tokens": usage.get("prompt_tokens", 0),
            "output_tokens": usage.get("completion_tokens", 0),
        },
    }


# ==================== FastAPI 应用 ====================
app = FastAPI(
    title="DeepSeek Bridge for Anthropic SDK",
    version="1.0",
    description="本地127.0.0.1:8788 Anthropic→DeepSeek格式转译 密钥隔离 业务无感"
)


@app.post("/v1/messages")
async def messages(req: Request):
    """
    Anthropic Messages API 兼容端点

    接收Anthropic SDK的请求·转译为DeepSeek调用·返回Anthropic格式
    """
    try:
        body = await req.json()
    except Exception as e:
        logger.error(f"❌ 请求体解析失败: {e}")
        raise HTTPException(400, f"请求体解析失败: {e}")

    model_in = body.get("model", "claude-3-5-sonnet-20241022")
    stream = body.get("stream", False)

    logger.info(f"📥 请求 | model={model_in} stream={stream}")

    # 转译请求
    try:
        payload = anthropic_to_openai(body)
    except Exception as e:
        logger.error(f"❌ 请求转译失败: {e}")
        raise HTTPException(400, f"请求转译失败: {e}")

    # 调用DeepSeek
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            logger.info(f"🔗 调用DeepSeek {DEEPSEEK_MODEL}...")

            response = await client.post(
                f"{DEEPSEEK_BASE_URL}/chat/completions",
                json=payload,
                headers=headers
            )

            if response.status_code != 200:
                error_msg = f"DeepSeek返回{response.status_code}: {response.text[:200]}"
                logger.error(f"❌ {error_msg}")

                # 如果启用了Ollama兜底·尝试fallback
                if OLLAMA_FALLBACK:
                    logger.info("🎯 DeepSeek失败·切换Ollama兜底...")
                    return await fallback_ollama(payload, model_in)
                else:
                    raise HTTPException(502, error_msg)

            response.raise_for_status()
            data = response.json()

            logger.info(f"✅ DeepSeek响应成功 | tokens: {data.get('usage', {}).get('completion_tokens', '?')}")

            # 转译回包
            result = openai_to_anthropic(data, model_in)
            return JSONResponse(result)

    except httpx.TimeoutException as e:
        logger.error(f"❌ DeepSeek超时: {e}")
        if OLLAMA_FALLBACK:
            logger.info("🎯 超时·切换Ollama兜底...")
            return await fallback_ollama(payload, model_in)
        raise HTTPException(504, "DeepSeek超时")

    except Exception as e:
        logger.error(f"❌ 调用失败: {e}")
        if OLLAMA_FALLBACK:
            logger.info("🎯 异常·切换Ollama兜底...")
            return await fallback_ollama(payload, model_in)
        raise HTTPException(502, f"DeepSeek调用失败: {e}")


async def fallback_ollama(payload: dict[str, Any], model_in: str) -> JSONResponse:
    """
    Ollama本地兜底·DeepSeek失败/超时时自动切换
    """
    logger.warning(f"⚠️  Ollama兜底 | 模型={OLLAMA_MODEL}")

    try:
        async with httpx.AsyncClient(timeout=180.0) as client:
            # Ollama API格式
            ollama_payload = {
                "model": OLLAMA_MODEL,
                "messages": payload["messages"],
                "stream": False
            }

            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/chat",
                json=ollama_payload
            )

            response.raise_for_status()
            data = response.json()

            logger.info(f"✅ Ollama响应成功 (本地兜底)")

            # 转译为Anthropic格式
            # Ollama返回: {"message": {"role": "assistant", "content": "..."}}
            result = openai_to_anthropic({
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": data.get("message", {}).get("content", "")
                    }
                }],
                "usage": {}
            }, model_in)

            return JSONResponse(result)

    except Exception as e:
        logger.error(f"❌ Ollama兜底也失败: {e}")
        raise HTTPException(503, f"DeepSeek和Ollama都失败: {e}")


@app.get("/health")
async def health():
    """健康检查端点"""
    return {
        "ok": True,
        "bridge": "deepseek",
        "deepseek_model": DEEPSEEK_MODEL,
        "ollama_fallback": OLLAMA_FALLBACK,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/v1/models")
async def list_models():
    """列出可用模型 (Anthropic API兼容)"""
    return {
        "object": "list",
        "data": [
            {
                "id": DEEPSEEK_MODEL,
                "object": "model",
                "created": int(time.time()),
                "owned_by": "deepseek"
            }
        ]
    }


@app.on_event("startup")
async def startup():
    logger.info("🐉 DeepSeek Bridge 已启动 | 127.0.0.1:8788")
    logger.info(f"📋 密钥文件: {env_file}")
    logger.info(f"📊 日志文件: {log_file}")


# ==================== CLI 启动 ====================
if __name__ == "__main__":
    logger.info("🚀 启动 DeepSeek Bridge...")
    logger.info(f"   监听: 127.0.0.1:8788")
    logger.info(f"   日志: {log_file}")

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8788,
        log_level="info"
    )
