#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·己未·乙亥时·䷒临-CHAT-BRIDGE-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# SPDX-License-Identifier: MulanPSL-2.0
"""
🐉 龍魂 · 对话桥接 v1.0
端口: 18800 (仅绑定 127.0.0.1), Ollama SSE 代理
修正14: httpx.AsyncClient 异步流式 + timeout=180s + raise_for_status + 异常兜底,
        不再用同步 requests 阻塞 event loop。
契约: GET /health → {"status":"ok","service":"chat-bridge","dna":...}
      POST /api/v1/chat → SSE 流; 无 X-Dragon-DNA → 403
模型: longhun-v4.1.4:latest 为自定义模型名, 真机须先执行:
      ollama create longhun-v4.1.4 -f <Modelfile>   (修正26)
      🟡 鲲鹏 arm64 无 CUDA, 纯 CPU 推理延迟/内存指标待真机回填。
"""

import json

import httpx
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse

from lh_audit import Historian, generate_dna, require_dna

SERVICE = "chat-bridge"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
DEFAULT_MODEL = "longhun-v4.1.4:latest"  # 须先 ollama create (修正26)
OLLAMA_TIMEOUT = httpx.Timeout(180.0, connect=10.0)  # 修正14: 显式超时

app = FastAPI(title="龍魂对话桥接", version="1.0.0")


@app.middleware("http")
async def p0_audit_middleware(request: Request, call_next):
    path = request.url.path
    if path == "/health":
        return await call_next(request)
    dna = require_dna(request.headers, SERVICE, path)
    if not dna:
        return JSONResponse(status_code=403,
                            content={"error": "P0协议要求: 缺少DNA追溯码"})
    response = await call_next(request)
    Historian.record("chat_request", dna, {
        "path": path, "method": request.method, "status": response.status_code,
    }, service=SERVICE)
    return response


@app.get("/health")
async def health():
    return {"status": "ok", "service": SERVICE, "dna": generate_dna("HEALTH")}


@app.post("/api/v1/chat")
@app.post("/api/v1/chat/")
async def chat(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    model = data.get("model", DEFAULT_MODEL)
    req_dna = request.headers.get("x-dragon-dna", "")

    async def sse_stream():
        # 修正22: DNA 含 uuid4 随机段, 每条流独立可追溯
        dna = generate_dna("CHAT")
        yield f"data: {json.dumps({'dna': dna}, ensure_ascii=False)}\n\n"
        try:
            async with httpx.AsyncClient(timeout=OLLAMA_TIMEOUT) as client:
                async with client.stream(
                    "POST", OLLAMA_URL,
                    json={"model": model, "prompt": prompt, "stream": True},
                ) as resp:
                    resp.raise_for_status()
                    async for line in resp.aiter_lines():
                        if line:
                            yield f"data: {line}\n\n"
        except httpx.TimeoutException:
            # 异常兜底: SSE 错误事件, 不抛栈给客户端
            yield ("data: " + json.dumps(
                {"error": "ollama_timeout", "message": "推理超时(180s)", "dna": dna},
                ensure_ascii=False) + "\n\n")
        except httpx.HTTPStatusError as exc:
            yield ("data: " + json.dumps(
                {"error": "ollama_http_error", "status": exc.response.status_code,
                 "message": "Ollama 返回错误 (模型可能未 ollama create)", "dna": dna},
                ensure_ascii=False) + "\n\n")
        except Exception as exc:  # 连接失败等兜底
            yield ("data: " + json.dumps(
                {"error": "ollama_unavailable", "message": str(exc)[:200], "dna": dna},
                ensure_ascii=False) + "\n\n")
        yield "data: [DONE]\n\n"

    Historian.record("chat_invoke", req_dna or generate_dna("CHAT-REQ"),
                     {"model": model, "prompt_len": len(prompt)}, service=SERVICE)
    return StreamingResponse(sse_stream(), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=18800)
