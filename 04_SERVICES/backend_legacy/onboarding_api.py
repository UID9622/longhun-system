#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂·AI 入口引导 API — 独立服务入口
DNA: #龍芯⚡️丙午·丙申·壬戌·亥时·䷲震-ONBOARDING-API-v1.0-DEPLOY-UID9622
创建者: 诸葛鑫（UID9622）

独立 FastAPI 服务：挂载 onboard_routes.py 的 /onboarding/* 路由。
部署目标: 鲲鹏 119.13.90.27 :8785 → nginx rewrite /api/onboarding/* → /onboarding/*
公网入口: https://uid9622.cn/api/onboarding/bootstrap

根因: onboard_routes.py 是孤儿路由（backend_legacy 骨架全是 auto_cannon 空占位），
无任何服务挂载 → 公网 404。本文件补上挂载，独立成服务，不动现有 9630/8777。
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from onboard_routes import router as onboard_router

app = FastAPI(
    title="龍魂·AI 入口引导 API",
    description="所有 AI 进入龍魂系统的统一入口 · 公网路径 /api/onboarding/*",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(onboard_router)


@app.get("/health")
async def health():
    """健康检查"""
    return {"ok": True, "service": "onboarding-api", "port": 8785}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8785)
