#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂9625·本地引擎·FastAPI 主入口
DNA: #龍芯⚡️2026-04-19-LOCAL-ENGINE-9625-v1.0
端口: 9625 · 只监听 127.0.0.1（外网不可达·主权安全）
原设计端口 9622 被 CNSH-64 治理引擎占用·改用旁路 9625

作者: 诸葛鑫（UID9622）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
理论指导: 曾仕强老师（永恒显示）

依赖: pip install fastapi uvicorn httpx python-dotenv
"""
import subprocess
import hashlib
import os
import sys
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

HOME = Path.home()
ENGINE_DIR = HOME / "longhun-system" / "engine"
MVP_DIR = ENGINE_DIR / "mvps"
MVP_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="龍魂9625引擎", version="1.0.0")

# CORS: 只允许 chrome-extension 和本地
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # chrome-extension:// 来源无法预匹配，本地CORS放开
    allow_methods=["*"],
    allow_headers=["*"],
)


def dna(payload: str) -> str:
    """生成 DNA 追溯码"""
    h = hashlib.sha256(
        f"{payload}|9622|{datetime.now().isoformat()}".encode()
    ).hexdigest()[:12]
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"#龍芯⚡️{ts}-ENGINE-{h}"


class TextIn(BaseModel):
    text: str = ""
    url: str = ""
    title: str = ""


class LuPipelineIn(BaseModel):
    """LU 一通百通流水线入参（CNSH 编辑器 / 浏览器接入）"""

    text: str = ""
    user_id: str = "guest"
    record_primary: bool = False


# ============ 健康检查 ============
@app.get("/")
def root():
    return {
        "service": "龍魂9625本地引擎",
        "version": "v1.0.0",
        "port": 9625,
        "endpoints": [
            "GET  /api/health",
            "POST /api/ethics/review",
            "POST /api/tongxin/translate",
            "POST /api/wuxing/analyze",
            "POST /api/errata/submit",
            "GET  /api/mcp/list",
            "POST /api/mcp/call",
            "POST /api/lu/pipeline",
            "GET  /api/lu/capabilities",
            "POST /api/chat",
            "POST /api/chat/local",
            "GET  /api/chat/history",
            "GET  /api/widget/list",
            "POST /api/widget/route",
            "GET  /api/widget/open/{name}",
            "GET  /api/roster/full",
            "GET  /api/demo/decision-receipt",
            "POST /api/demo/flow-smoke",
            "GET  /transparent-demo/README.md",
        ],
        "dna": dna("root"),
    }


@app.get("/api/health")
def health():
    return {
        "ok": True,
        "version": "v1.0.0",
        "port": 9625,
        "dna": dna("health"),
        "time": datetime.now().isoformat(),
    }


# ============ 伦理审查（调用 MVP 脚本） ============
@app.post("/api/ethics/review")
def ethics(inp: TextIn):
    mvp = MVP_DIR / "ethics_review_mvp.py"
    if mvp.exists():
        try:
            r = subprocess.run(
                [sys.executable, str(mvp)],
                capture_output=True, text=True, timeout=10
            )
            summary = r.stdout or r.stderr
        except Exception as e:
            summary = f"MVP 调用失败: {e}"
    else:
        # 占位：无 MVP 时给出基础审查框架
        summary = f"【伦理审查·占位版】\n输入长度: {len(inp.text)}\n来源: {inp.url or '剪贴板'}\n\n待接入 ethics_review_mvp.py"
    return {
        "title": "⚖️ 伦理审查",
        "color": "🟢",
        "summary": summary,
        "dna": dna(inp.text[:50]),
    }


# ============ 五行分析 ============
@app.post("/api/wuxing/analyze")
def wuxing(inp: TextIn):
    mvp = MVP_DIR / "longhun_wuxing_mvp.py"
    if mvp.exists():
        try:
            r = subprocess.run(
                [sys.executable, str(mvp)],
                capture_output=True, text=True, timeout=10
            )
            summary = r.stdout or r.stderr
        except Exception as e:
            summary = f"MVP 调用失败: {e}"
    else:
        summary = "【五行分析·占位】待接入 longhun_wuxing_mvp.py"
    return {
        "title": "🔥 五行八字",
        "color": "🟡",
        "summary": summary,
        "dna": dna("wuxing"),
    }


# ============ 通心译（占位·待 sancai_router.py 接入） ============
@app.post("/api/tongxin/translate")
def tongxin(inp: TextIn):
    return {
        "title": "🟡 通心译",
        "color": "🟢",
        "summary": f"原文:\n{inp.text[:200]}\n\n[六维路径待接入]",
        "dna": dna(inp.text),
    }


# ============ 记错本上报 ============
@app.post("/api/errata/submit")
async def errata(inp: TextIn):
    try:
        from notion_sync import push_errata
        res = await push_errata(
            text=inp.text,
            source_url=inp.url,
            source_title=inp.title,
        )
        return {
            "title": "📓 记错本",
            "color": "🟢",
            "summary": f"已上报·工单 {res.get('id', '未知')}",
            "notion_url": res.get("url"),
            "dna": dna(inp.text),
        }
    except Exception as e:
        return {
            "title": "📓 记错本",
            "color": "🟡",
            "summary": f"未上报 Notion（缺 NOTION_TOKEN 或 ERRATA_DB_ID）: {e}\n本地回退: {inp.text[:200]}",
            "dna": dna(inp.text),
        }


# ============ LU 系统流水线（CNSH 编辑器 / 浏览器接入） ============
@app.post("/api/lu/pipeline")
def lu_pipeline_run(inp: LuPipelineIn):
    from lu_pipeline import run_pipeline

    return run_pipeline(inp.user_id, inp.text, record_primary=inp.record_primary)


@app.get("/api/lu/capabilities")
def lu_capabilities_list():
    from lu_pipeline import list_capabilities_snapshot

    return {
        "ok": True,
        "dna": dna("lu-capabilities"),
        "capabilities": list_capabilities_snapshot(),
    }


# ============ MCP 协议桥 ============
@app.get("/api/mcp/list")
async def mcp_list():
    try:
        from mcp_bridge import list_tools
        return await list_tools()
    except Exception as e:
        return {"tools": [], "error": str(e)}


@app.post("/api/mcp/call")
async def mcp_call(req: Request):
    try:
        from mcp_bridge import call_tool
        body = await req.json()
        return await call_tool(body.get("tool"), body.get("args", {}))
    except Exception as e:
        return {"error": str(e)}


# ============ 对话窗（加载 chat 路由） ============
try:
    from chat import router as chat_router
    app.include_router(chat_router)
    _CHAT_OK = True
except Exception as e:
    print(f"⚠️  chat 模块加载失败·对话功能不可用: {e}")
    _CHAT_OK = False

# ============ Widget 路由（接 web-widgets/.dna/keyword_map.md） ============
try:
    from widget_router import router as widget_rt
    app.include_router(widget_rt)
    _WIDGET_OK = True
except Exception as e:
    print(f"⚠️  widget_router 加载失败: {e}")
    _WIDGET_OK = False

# ============ 桌面控制台（DNA 滑条 + 任务表） ============
_STATIC = ENGINE_DIR / "static"
if _STATIC.is_dir():
    app.mount("/static", StaticFiles(directory=str(_STATIC)), name="static")

try:
    from desktop_api import router as desktop_router
    app.include_router(desktop_router)
    _DESKTOP_OK = True
except Exception as e:
    print(f"⚠️  desktop_api 加载失败: {e}")
    _DESKTOP_OK = False

try:
    from cnsh_exec import router as cnsh_router
    app.include_router(cnsh_router)
    _CNSH_OK = True
except Exception as e:
    print(f"⚠️  cnsh_exec 加载失败: {e}")
    _CNSH_OK = False


@app.get("/")
def root():
    return RedirectResponse(url="/console")


@app.get("/console")
def console_page():
    return RedirectResponse(url="/static/console.html")


@app.on_event("startup")
def _startup_tasks():
    try:
        from defense.background_daemon import start_background
        if start_background():
            print("🛡️  护盾后台已启动（防御·松紧 normal·只防不攻）")
    except Exception as e:
        print(f"⚠️  护盾后台跳过: {e}")
    try:
        from task_runner import run_startup_queue
        results = run_startup_queue()
        if results and results[0].get("status") != "skipped":
            print(f"📋 开机任务: {len(results)} 条")
    except Exception as e:
        print(f"⚠️  开机任务跳过: {e}")

try:
    from defense_router import router as defense_router
    app.include_router(defense_router)
except Exception as e:
    print(f"⚠️  defense_router 加载失败: {e}")

try:
    from roster_router import router as roster_router
    app.include_router(roster_router)
    _ROSTER_OK = True
except Exception as e:
    print(f"⚠️  roster_router 加载失败: {e}")
    _ROSTER_OK = False

try:
    from demo_api import router as demo_router
    app.include_router(demo_router)
    _DEMO_OK = True
except Exception as e:
    print(f"⚠️  demo_api 加载失败: {e}")
    _DEMO_OK = False

_TRANSPARENT_DEMO = HOME / "longhun-system" / "public" / "transparent-demo"
if _TRANSPARENT_DEMO.is_dir():
    app.mount(
        "/transparent-demo",
        StaticFiles(directory=str(_TRANSPARENT_DEMO)),
        name="transparent-demo",
    )

_MVP_CONSOLE = (
    HOME / "longhun-system" / "00_main_control" / "操作台v3" / "components"
)
if _MVP_CONSOLE.is_dir():
    app.mount("/mvp", StaticFiles(directory=str(_MVP_CONSOLE)), name="mvp-console")


if __name__ == "__main__":
    print("""
🐉 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   龍魂9625·本地引擎 · v1.0.0
   端口: http://127.0.0.1:9625
   DNA:  #龍芯⚡️2026-04-19-LOCAL-ENGINE-9625-v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📜 主权承诺:
   ① 数据只在您本机 ~/longhun-system/engine/memory/
   ② API Key 只读 ~/longhun-system/engine/.env
   ③ 每次调用·DNA 自动签章·可完整追溯
   ④ curl /api/chat/export → 一键全量打包走人
   ⑤ launchctl unload → 引擎立即断电
   ⑥ 桌面控制台 → http://127.0.0.1:9625/console

 UID9622 · #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
    uvicorn.run(app, host="127.0.0.1", port=9625, log_level="info")
