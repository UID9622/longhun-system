#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-KB-API-APP-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂·Notion 知识库引用架构 L4 — 独立 API 服务入口
================================================
DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-KB-API-APP-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（核心思想层）/ MulanPSL v2（工程实现层）

独立轻量 FastAPI 服务（默认 127.0.0.1:9633），仅承载 /api/kb/*：
  - 不动线上任何服务（3000 CNSH / 8777 / 8789 零改动）
  - nginx 只加一行 /api/kb/ 反代
  - 环境变量: NOTION_KB_INDEX / NOTION_TOKEN / KB_WEBHOOK_KEY（从 EnvironmentFile 注入）
"""
import sys
import os
from pathlib import Path

_SELF = Path(__file__).resolve().parent
if str(_SELF) not in sys.path:
    sys.path.insert(0, str(_SELF))

from fastapi import FastAPI

from kb_api_router import router as kb_router

app = FastAPI(title="🐉 龍魂·知识库 API（L4）", version="1.0")
app.include_router(kb_router)


@app.get("/health")
def health():
    return {"ok": True, "service": "longhun-kb-api", "sovereign": "UID9622"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=int(os.environ.get("KB_API_PORT", "9633")),
        log_level="info",
    )
