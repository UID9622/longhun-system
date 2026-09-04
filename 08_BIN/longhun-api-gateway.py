#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙酉·丙寅·未时-KIMI-GATEWAY-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""龍魂 API 网关 - 提供 Kimi 记忆同步等本地端点。"""

import json
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI
import uvicorn


app = FastAPI(title="LongHun API Gateway")


def generate_dna() -> str:
    """生成 DNA 追溯码。"""
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-MEMORY-UID9622"


@app.get("/api/xiaoyi/ask")
async def xiaoyi_ask():
    """Kimi 记忆同步端点 - 返回本地记忆。"""
    mem_path = Path.home() / ".longhun" / "memory" / "latest_digest.json"
    if mem_path.exists():
        with open(mem_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "status": "empty",
        "dna": generate_dna(),
        "digest": "暂无记忆数据",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9622)
