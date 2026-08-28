#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#龍芯⚡️丙午·丙申·丙辰·巳时·䷄需-WEB-SERVER-v2.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
龍魂 Web 门户服务器 v2.0
DNA: #龍芯⚡️丙午·丙申·丙辰·巳时·䷄需-WEB-SERVER-v2.0

功能：
- 挂载 portal/index.html 作为主页（:8777）
- 挂载 web/ 下所有静态页面
- 挂载 web/reports/ 报告展厅
- API 代理到后端 :9622
- 健康检查端点
- WebSocket 代理
"""

import logging
import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

logger = logging.getLogger("longhun.web_server")

# 项目根路径（本脚本位于 08_BIN/ 下，向上两级为项目根）
ROOT = Path(__file__).resolve().parent.parent
PORTAL_DIR = ROOT / "portal"
WEB_DIR = ROOT / "web"
REPORTS_DIR = WEB_DIR / "reports"

# 后端 API 地址
API_URL = os.environ.get("LONGHUN_API_URL", "http://127.0.0.1:9622")

app = FastAPI(
    title="龍魂 Web 门户 v2.0",
    description="龍魂系统 · 统一 Web 入口 · longhun888.com",
    version="2.0.0",
    docs_url=None,
    redoc_url=None,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═══════════════════════════
# 静态文件挂载
# ═══════════════════════════

# Web 子页面（/web/xxx.html）
if WEB_DIR.exists():
    app.mount("/web", StaticFiles(directory=str(WEB_DIR), html=True), name="web")

# 报告展厅
if REPORTS_DIR.exists():
    app.mount("/reports", StaticFiles(directory=str(REPORTS_DIR), html=True), name="reports")

# 字体
font_dir = ROOT / "字体"
if font_dir.exists():
    app.mount("/fonts", StaticFiles(directory=str(font_dir)), name="fonts")

# 资源文件
assets_dir = ROOT / "assets"
if assets_dir.exists():
    app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")


# ═══════════════════════════
# 路由
# ═══════════════════════════

@app.get("/")
async def home():
    """主页 → portal/index.html"""
    index_path = PORTAL_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return JSONResponse({"ok": True, "name": "龍魂 Web 门户", "version": "2.0.0"})


@app.get("/health")
async def health():
    """健康检查"""
    return {
        "ok": True,
        "service": "龍魂 Web 门户 v2.0",
        "api_backend": API_URL,
        "static_dirs": {
            "portal": str(PORTAL_DIR),
            "web": str(WEB_DIR),
            "reports": str(REPORTS_DIR),
        }
    }


@app.get("/api/{path:path}")
async def proxy_api(path: str):
    """API 代理说明（实际由 Nginx 反向代理处理）"""
    return JSONResponse({
        "ok": True,
        "message": f"API 请求应代理到后端 {API_URL}/api/{path}",
        "backend": API_URL,
        "note": "生产环境由 Nginx 反向代理处理，开发环境请在浏览器中直接访问后端",
    })


# ═══════════════════════════
# 启动
# ═══════════════════════════

if __name__ == "__main__":
    port = int(os.environ.get("LONGHUN_WEB_PORT", "8777"))
    host = os.environ.get("LONGHUN_WEB_HOST", "0.0.0.0")

    logger.info("🐉 龍魂 Web 门户 v2.0 启动")
    logger.info("   地址: http://%s:%s", host, port)
    logger.info("   后端: %s", API_URL)
    logger.info("   门户: %s", PORTAL_DIR)
    logger.info("   Web:  %s", WEB_DIR)
    logger.info("   报告: %s", REPORTS_DIR)

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
    )
