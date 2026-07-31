# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂 · 个人数据主权雷达 API v3.0
DNA: #龍芯⚡️丙午·乙未·戊戌·亥时·☰乾-DATA-RADAR-API-v3.0-TRIPLE-AI
创建者: 诸葛鑫（UID9622）· 协议: CC BY-NC-SA 4.0
端口: 8788
端点:
  GET  /api/radar/status        — 雷达总状态
  GET  /api/radar/scan?mode=X   — 触发扫描
  GET  /api/radar/p0            — P0协议清单
  GET  /api/breaker/status      — 熔断器状态
  POST /api/breaker/arm         — 一键熔断
  POST /api/breaker/disarm      — 解除熔断
  POST /api/breaker/toggle      — 单条切换
  GET  /api/ai/status           — AI模式状态（含三后端健康）
  POST /api/ai/switch           — 切换AI模式
  POST /api/ai/chat             — 真实对话（Ollama→Kimi→DeepSeek三后端）
  GET  /api/ai/history          — 对话记录
  GET  /api/ai/health           — 三后端健康检查
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# 添加项目根路径
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from engines.lh_data_radar import DataRadarScanner, DNA as RADAR_DNA
from engines.lh_privacy_breaker import PrivacyCircuitBreaker, DNA as BREAKER_DNA
from engines.lh_offline_ai import OfflineAISwitch, DNA as AI_DNA

# ═══ 常量 ═══
DNA = "#龍芯⚡️丙午·乙未·戊戌·亥时·☰乾-DATA-RADAR-API-v3.0-TRIPLE-AI"
CREATOR = "诸葛鑫（UID9622）"
PORT = 8788

# ═══ FastAPI 实例 ═══
app = FastAPI(
    title="龍魂·个人数据主权雷达",
    description="老百姓的数据主权驾照——你的数据，你自己说了算。v3.0三后端AI升级",
    version="3.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══ 静态文件 ═══
STATIC_DIR = PROJECT_ROOT / "portal"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")


# ═══ 首页重定向 ═══
@app.get("/", response_class=HTMLResponse)
async def root():
    """首页 → 数据主权雷达"""
    html_path = PROJECT_ROOT / "portal" / "data-radar" / "index.html"
    if html_path.exists():
        return HTMLResponse(html_path.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>龍魂·个人数据主权雷达</h1><p>前端文件未找到</p>")


@app.get("/status")
async def global_status():
    """全局状态汇总"""
    try:
        radar = get_radar()
        breaker = get_breaker()
        ai = get_ai()
        return {
            "service": "龍魂·个人数据主权雷达",
            "version": "1.0.0",
            "dna": DNA,
            "radar": radar.get_status(),
            "breaker": breaker.get_status(),
            "ai": ai.get_status(),
        }
    except Exception as e:
        return {"status": "degraded", "error": str(e)}


# 引擎实例（懒加载）
_radar: DataRadarScanner = None
_breaker: PrivacyCircuitBreaker = None
_ai_switch: OfflineAISwitch = None


def get_radar() -> DataRadarScanner:
    global _radar
    if _radar is None:
        _radar = DataRadarScanner()
    return _radar


def get_breaker() -> PrivacyCircuitBreaker:
    global _breaker
    if _breaker is None:
        _breaker = PrivacyCircuitBreaker()
    return _breaker


def get_ai() -> OfflineAISwitch:
    global _ai_switch
    if _ai_switch is None:
        _ai_switch = OfflineAISwitch()
    return _ai_switch


# ═══ 请求模型 ═══

class BreakerAction(BaseModel):
    biometric_verified: bool = Field(default=True, description="是否通过生物特征验证")


class BreakerToggle(BaseModel):
    target: str = Field(..., description="目标规则名称，如'位置追踪'")
    armed: bool = Field(..., description="true=切断, false=恢复")
    biometric_verified: bool = Field(default=True)


class AISwitchRequest(BaseModel):
    mode: str = Field(..., description="local / cloud / hybrid")
    biometric_verified: bool = Field(default=True)


class AIChatRequest(BaseModel):
    message: str = Field(..., description="用户输入内容")
    backend: str = Field(default="auto", description="auto/local/cloud/hybrid")
    context: list = Field(default=[], description="历史对话")


@app.get("/api/radar/status")
async def radar_status():
    """雷达总状态 — 包含最近扫描汇总"""
    radar = get_radar()
    return radar.get_status()


@app.get("/api/radar/scan")
async def radar_scan(mode: str = Query("quick", description="quick / deep / continuous")):
    """触发一次扫描"""
    if mode not in ("quick", "deep", "continuous"):
        raise HTTPException(400, "mode 必须是 quick / deep / continuous")
    radar = get_radar()
    report = radar.scan(mode)
    return report


@app.get("/api/radar/p0")
async def radar_p0():
    """P0协议清单（给前端状态栏用）"""
    radar = get_radar()
    return radar.get_p0_protocols()


# ═══ 熔断器 ═══

@app.get("/api/breaker/status")
async def breaker_status():
    """熔断器当前状态"""
    breaker = get_breaker()
    return breaker.get_status()


@app.post("/api/breaker/arm")
async def breaker_arm(body: BreakerAction):
    """一键熔断 — 物理级切断所有数据收集"""
    breaker = get_breaker()
    proof = breaker.arm_all(biometric_proof=body.biometric_verified)
    if not proof.all_success and not body.biometric_verified:
        raise HTTPException(403, "需要生物特征验证")
    return proof.to_dict()


@app.post("/api/breaker/disarm")
async def breaker_disarm(body: BreakerAction):
    """解除熔断"""
    breaker = get_breaker()
    proof = breaker.disarm_all(biometric_proof=body.biometric_verified)
    if not proof.all_success and not body.biometric_verified:
        raise HTTPException(403, "需要生物特征验证")
    return proof.to_dict()


@app.post("/api/breaker/toggle")
async def breaker_toggle(body: BreakerToggle):
    """单条规则切换"""
    breaker = get_breaker()
    result = breaker.toggle_single(body.target, body.armed, body.biometric_verified)
    return result


@app.get("/api/breaker/audit")
async def breaker_audit(limit: int = Query(20)):
    """熔断操作审计记录"""
    breaker = get_breaker()
    return breaker.get_audit_log(limit)


# ═══ 离线AI（v2.0 双后端·真推理）═══

@app.get("/api/ai/status")
async def ai_status():
    """AI模式当前状态（含三后端健康）"""
    ai = get_ai()
    status = ai.get_status()
    # 追加三后端健康状态
    try:
        import asyncio
        health = asyncio.run(ai.triple_health())
        status["triple_backend"] = health
    except Exception:
        status["triple_backend"] = {"status": "unknown", "local": "unknown", "kimi": "unknown", "deepseek": "unknown"}
    return status


@app.get("/api/ai/health")
async def ai_health():
    """三后端健康检查"""
    ai = get_ai()
    import asyncio
    return await ai.triple_health()


@app.post("/api/ai/switch")
async def ai_switch_mode(body: AISwitchRequest):
    """切换AI运行模式"""
    ai = get_ai()
    result = ai.switch_mode(body.mode, biometric_proof=body.biometric_verified)
    if not result["success"]:
        raise HTTPException(400, result.get("error", "切换失败"))
    return result


@app.post("/api/ai/chat")
async def ai_chat(body: AIChatRequest):
    """真实AI对话 — Ollama→Kimi→DeepSeek三后端降级"""
    ai = get_ai()
    result = await ai.chat(body.message, backend=body.backend, context=body.context)
    return result


@app.get("/api/ai/history")
async def ai_history(limit: int = Query(20)):
    """对话记录"""
    ai = get_ai()
    return ai.get_chat_history(limit)


# ═══ 启动 ═══

if __name__ == "__main__":
    print(f"🐉 龍魂·个人数据主权雷达 API v3.0 · 三后端")
    print(f"   DNA: {DNA}")
    print(f"   端口: {PORT}")
    print(f"   前端: http://127.0.0.1:{PORT}/static/data-radar/")
    print(f"   API:  http://127.0.0.1:{PORT}/api/radar/status")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
