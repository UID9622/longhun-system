#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·8081 中樞門戶引擎 v1.0
功能：靜態文件服務 + DeepSeek API 代理 + 系統狀態聚合

DNA: #龍芯⚡️2026-04-05-PORTAL-ENGINE-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F1E3B8A4C6D0F2E4A6B8C0D2E4F6A8B0C2
創建者: UID9622 諸葛鑫（龍芯北辰）
確認碼: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

保存為: ~/longhun-system/bin/portal_engine_8081.py
用途: 讓 8081 端口成為系統中樞寶寶的引擎
"""

import os
import sys
import json
import asyncio
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# 加載環境變量
env_paths = [
    Path(__file__).parent / '.env',
    Path.home() / 'longhun-system' / '.env',
    Path.home() / '.cnsh' / '.env',
]
for env_path in env_paths:
    if env_path.exists():
        load_dotenv(env_path)
        break

import httpx
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

# ── 配置 ──
WEB_DIR = Path.home() / "longhun-system" / "web"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

if not DEEPSEEK_API_KEY:
    print("🔴 錯誤: 未找到 DEEPSEEK_API_KEY，請檢查 .env")
    sys.exit(1)

app = FastAPI(title="龍魂8081中樞門戶引擎", version="1.0")

# CORS：允許本地所有來源調用 API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ══════════════════════════════════════════════════════════
# API 路由（必須在 StaticFiles mount 之前定義）
# ══════════════════════════════════════════════════════════

@app.get("/")
async def root():
    """根路徑重定向到中樞工作台"""
    return RedirectResponse(url="/mvp_workbench_v6.1.html")


@app.post("/api/chat")
async def api_chat(request: Request):
    """
    系統中樞寶寶引擎 · DeepSeek API 代理
    接收 OpenAI 兼容格式，轉發到 DeepSeek
    """
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(DEEPSEEK_URL, headers=headers, json=body)
            response.raise_for_status()
            return JSONResponse(content=response.json(), status_code=response.status_code)
        except httpx.HTTPStatusError as e:
            return JSONResponse(
                content={"error": f"DeepSeek API error: {e.response.text}"},
                status_code=e.response.status_code
            )
        except httpx.RequestError as e:
            return JSONResponse(
                content={"error": f"Request failed: {str(e)}"},
                status_code=502
            )


@app.get("/api/status")
async def api_status():
    """聚合本地龍魂服務狀態"""
    services = {
        "龍魂主引擎_8000": "http://localhost:8000/health",
        "龍魂本地服務_8765": "http://localhost:8765",
        "CNSH64治理_9622": "http://localhost:9622/shield/status",
        "OpenWebUI_8080": "http://localhost:8080/health",
        "Ollama_11434": "http://localhost:11434/api/tags",
    }

    results = {}
    async with httpx.AsyncClient(timeout=5.0) as client:
        for name, url in services.items():
            try:
                resp = await client.get(url)
                results[name] = "online" if resp.status_code < 400 else f"http_{resp.status_code}"
            except Exception:
                results[name] = "offline"

    return {
        "portal": "online",
        "timestamp": datetime.now().isoformat(),
        "dna": "#龍芯⚡️2026-04-05-PORTAL-ENGINE-v1.0",
        "services": results
    }


@app.get("/api/models")
async def api_models():
    """返回本地可用的模型列表（OpenAI 兼容 /v1/models）"""
    return {
        "object": "list",
        "data": [
            {
                "id": "deepseek-chat",
                "object": "model",
                "owned_by": "deepseek"
            },
            {
                "id": "deepseek-coder",
                "object": "model",
                "owned_by": "deepseek"
            }
        ]
    }


@app.post("/api/memory/inject")
async def api_memory_inject(request: Request):
    """接收記憶片段，追加到本地 memory.jsonl"""
    try:
        data = await request.json()
        memory_file = Path.home() / "longhun-system" / "memory.jsonl"
        record = {
            "ts": datetime.now().isoformat(),
            "source": "portal_8081",
            "content": data.get("content", ""),
            "tags": data.get("tags", []),
            "dna": "#龍芯⚡️2026-04-05-PORTAL-MEMORY"
        }
        with open(memory_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return {"status": "ok", "message": "記憶已注入"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ══════════════════════════════════════════════════════════
# 靜態文件服務（掛載到根，作為 fallback）
# ══════════════════════════════════════════════════════════

app.mount("/", StaticFiles(directory=str(WEB_DIR), html=True), name="static")


# ══════════════════════════════════════════════════════════
# 啟動入口
# ══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("🐉 龍魂·8081 中樞門戶引擎 v1.0 啟動")
    print(f"   靜態目錄: {WEB_DIR}")
    print(f"   DeepSeek: 已配置")
    print(f"   DNA: #龍芯⚡️2026-04-05-PORTAL-ENGINE-v1.0")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8081)
