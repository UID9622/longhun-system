# DNA: #龍芯⚡️丙午·丙申·甲子·癸酉·䷪夬-CODE-补DNA-e9247ce6
#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂 · 透明审计AI Hub API v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
多模型统一对话 · 全链路透明审计 · 实时计费 · DNA追溯

DNA: #龍芯⚡️丙午·丙申·己酉·庚午·䷐随-AI-HUB-API-v1.0-8f2a1c6e
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

核心价值:
  - 一个入口，调用 ChatGPT / Claude / Kimi / DeepSeek / 混元
  - 每次对话全量审计：模型/延迟/token数/费用/DNA追溯
  - 实时计费透视：精确到每次调用的费用明细
  - 数据主权标识：数据流向中国境内/境外明确标注
  - 自动审计报告生成

启动方式:
  python3 bin/lh_ai_hub_api.py --port 8778
  lh ai-hub

API 端点:
  POST /api/ai-hub/chat          — 对话（支持流式）
  POST /api/ai-hub/compare       — 多模型对比
  GET  /api/ai-hub/models        — 可用模型列表+状态
  GET  /api/ai-hub/stats         — 用量统计
  GET  /api/ai-hub/history       — 对话历史
  GET  /api/ai-hub/audit-report  — 审计报告
  GET  /api/ai-hub/health        — 健康检查
"""

import os
import sys
import json
import time
import uuid
import hashlib
import sqlite3
import logging
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any, List

# ─── 路径设置 ───
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "bin"))

DNA = "#龍芯⚡️丙午·丙申·己酉·庚午·䷐随-AI-HUB-API-v1.0-8f2a1c6e"
VERSION = "1.0.0"

# ─── 日志 ───
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "ai_hub_api.log"),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger("lh_ai_hub")

# ─── 审计数据库 ───
AUDIT_DIR = PROJECT_ROOT / "audit"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_DB = AUDIT_DIR / "ai_hub_audit.db"

# ─── 模型定价 (USD/1M tokens, 输入/输出) ───
MODEL_PRICING = {
    "claude":    {"input": 3.00,  "output": 15.00, "currency": "USD", "sovereignty": "🇺🇸 境外"},
    "deepseek":  {"input": 0.14,  "output": 0.28,  "currency": "USD", "sovereignty": "🇨🇳 境内"},
    "kimi":      {"input": 0.60,  "output": 0.60,  "currency": "CNY", "sovereignty": "🇨🇳 境内"},
    "openai":    {"input": 0.15,  "output": 0.60,  "currency": "USD", "sovereignty": "🇺🇸 境外"},
    "hunyuan":   {"input": 0.004, "output": 0.012, "currency": "CNY", "sovereignty": "🇨🇳 境内"},
    "ollama":    {"input": 0.0,   "output": 0.0,   "currency": "FREE", "sovereignty": "🏠 本地"},
}

# ─── 模型元信息 ───
MODEL_META = {
    "claude":   {"name": "Claude 3.5 Sonnet", "vendor": "Anthropic", "type": "cloud", "max_tokens": 4096},
    "deepseek": {"name": "DeepSeek Chat", "vendor": "深度求索", "type": "cloud", "max_tokens": 4096},
    "kimi":     {"name": "Kimi (Moonshot v1)", "vendor": "月之暗面", "type": "cloud", "max_tokens": 4096},
    "openai":   {"name": "GPT-4o Mini", "vendor": "OpenAI", "type": "cloud", "max_tokens": 4096},
    "hunyuan":  {"name": "混元 Lite", "vendor": "腾讯云", "type": "cloud", "max_tokens": 4096},
    "ollama":   {"name": "龍魂本地模型", "vendor": "Ollama/MLX", "type": "local", "max_tokens": 4096},
}

# ─── 试运行 ───
try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False
    logger.warning("⚠️ httpx 未安装，云端模型不可用（pip3 install httpx）")

try:
    from fastapi import FastAPI, HTTPException, Query
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse, StreamingResponse
    import uvicorn
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False
    logger.warning("⚠️ FastAPI/uvicorn 未安装（pip3 install fastapi uvicorn）")

try:
    from pydantic import BaseModel, Field
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False
    BaseModel = object

# ═══════════════════════════════════════════════════════
# 数据库
# ═══════════════════════════════════════════════════════

def init_db():
    """初始化审计数据库"""
    conn = sqlite3.connect(str(AUDIT_DB))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id TEXT UNIQUE NOT NULL,
            dna TEXT NOT NULL,
            session_id TEXT,
            model_provider TEXT NOT NULL,
            model_name TEXT NOT NULL,
            messages_json TEXT NOT NULL,
            response_text TEXT,
            prompt_tokens INTEGER DEFAULT 0,
            completion_tokens INTEGER DEFAULT 0,
            total_tokens INTEGER DEFAULT 0,
            estimated_cost_usd REAL DEFAULT 0.0,
            latency_ms REAL DEFAULT 0,
            task_type TEXT DEFAULT 'general',
            sovereignty TEXT DEFAULT 'unknown',
            status TEXT DEFAULT 'pending',
            error_message TEXT,
            user_agent TEXT,
            client_ip TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            metadata_json TEXT DEFAULT '{}'
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_log(created_at)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_audit_session ON audit_log(session_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_audit_model ON audit_log(model_provider)")
    conn.execute("PRAGMA journal_mode=WAL")
    conn.commit()
    conn.close()
    logger.info(f"✅ 审计数据库已初始化: {AUDIT_DB}")

def save_audit(entry: Dict[str, Any]):
    """保存审计记录"""
    try:
        conn = sqlite3.connect(str(AUDIT_DB))
        conn.execute("""
            INSERT INTO audit_log 
            (request_id, dna, session_id, model_provider, model_name, messages_json,
             response_text, prompt_tokens, completion_tokens, total_tokens,
             estimated_cost_usd, latency_ms, task_type, sovereignty, status, error_message,
             user_agent, client_ip, metadata_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entry["request_id"], entry["dna"], entry.get("session_id"),
            entry["model_provider"], entry["model_name"],
            json.dumps(entry.get("messages", []), ensure_ascii=False),
            entry.get("response_text"), entry.get("prompt_tokens", 0),
            entry.get("completion_tokens", 0), entry.get("total_tokens", 0),
            entry.get("estimated_cost_usd", 0.0), entry.get("latency_ms", 0),
            entry.get("task_type", "general"), entry.get("sovereignty", "unknown"),
            entry.get("status", "success"), entry.get("error_message"),
            entry.get("user_agent", ""), entry.get("client_ip", ""),
            json.dumps(entry.get("metadata", {}), ensure_ascii=False)
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"审计写入失败: {e}")

def get_stats(days: int = 7) -> Dict[str, Any]:
    """获取用量统计"""
    conn = sqlite3.connect(str(AUDIT_DB))
    conn.row_factory = sqlite3.Row
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    
    # 总计
    total = conn.execute(
        "SELECT COUNT(*) as c, SUM(total_tokens) as t, SUM(estimated_cost_usd) as cost FROM audit_log WHERE status='success' AND created_at >= ?",
        (cutoff,)
    ).fetchone()
    
    # 按模型
    by_model = conn.execute("""
        SELECT model_provider, COUNT(*) as c, SUM(total_tokens) as t, 
               AVG(latency_ms) as avg_latency, SUM(estimated_cost_usd) as cost
        FROM audit_log WHERE status='success' AND created_at >= ?
        GROUP BY model_provider ORDER BY c DESC
    """, (cutoff,)).fetchall()
    
    # 按天
    by_day = conn.execute("""
        SELECT DATE(created_at) as day, COUNT(*) as c, SUM(total_tokens) as t
        FROM audit_log WHERE status='success' AND created_at >= ?
        GROUP BY day ORDER BY day
    """, (cutoff,)).fetchall()
    
    # 今日
    today = datetime.now().strftime("%Y-%m-%d")
    today_row = conn.execute(
        "SELECT COUNT(*) as c, SUM(total_tokens) as t, SUM(estimated_cost_usd) as cost FROM audit_log WHERE status='success' AND DATE(created_at)=?",
        (today,)
    ).fetchone()
    
    conn.close()
    
    return {
        "period_days": days,
        "total_requests": total["c"] or 0,
        "total_tokens": total["t"] or 0,
        "total_cost_usd": round(total["cost"] or 0, 6),
        "today_requests": today_row["c"] or 0,
        "today_tokens": today_row["t"] or 0,
        "today_cost_usd": round(today_row["cost"] or 0, 6),
        "by_model": [dict(r) for r in by_model],
        "by_day": [dict(r) for r in by_day],
    }

def build_dna() -> str:
    """生成DNA追溯码"""
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    h = hashlib.sha256(f"{ts}{uuid.uuid4()}".encode()).hexdigest()[:8]
    return f"#龍芯⚡️{ts}-AI-HUB-{h}"

def estimate_cost(provider: str, input_tokens: int, output_tokens: int) -> float:
    """估算费用(USD)"""
    pricing = MODEL_PRICING.get(provider, {"input": 0, "output": 0})
    if pricing["currency"] == "CNY":
        rate = 0.14  # 1 CNY ≈ 0.14 USD
        return round((input_tokens * pricing["input"] + output_tokens * pricing["output"]) / 1_000_000 * rate, 6)
    elif pricing["currency"] == "FREE":
        return 0.0
    else:
        return round((input_tokens * pricing["input"] + output_tokens * pricing["output"]) / 1_000_000, 6)

def count_tokens_approx(text: str) -> int:
    """简易token计数（中文≈1.5x, 英文≈4 char/token）"""
    if not text:
        return 0
    cn_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    en_chars = len(text) - cn_chars
    return int(cn_chars * 1.5 + en_chars / 4)

# ═══════════════════════════════════════════════════════
# AI 调用引擎
# ═══════════════════════════════════════════════════════

def call_ai_gateway(messages: List[Dict], provider: str = None, 
                    task_type: str = "general", temperature: float = 0.7,
                    system: str = "") -> Dict[str, Any]:
    """
    调用AI网关（统一入口）
    支持: claude, deepseek, kimi, openai, hunyuan, ollama
    """
    if HAS_HTTPX:
        from bin.lh_ai_gateway import chat, classify_task, ROUTE_TABLE, TaskType, _get_api_key, MODEL_CONFIGS, _call_openai_format, _call_claude_format
        from bin.lh_ai_gateway import ROUTE_TABLE as RT
        
        task_map = {"code": TaskType.CODE, "cn": TaskType.CHINESE_CHAT, "translate": TaskType.TRANSLATE,
                     "analyze": TaskType.ANALYZE, "creative": TaskType.CREATIVE, "math": TaskType.MATH, "general": TaskType.GENERAL}
        tt = task_map.get(task_type, TaskType.GENERAL)
        
        if provider and provider in ["claude", "deepseek", "kimi", "openai"]:
            result = chat(messages=messages, task_type=tt, temperature=temperature, system=system)
            result["provider_used"] = result.get("routed_via", provider)
        else:
            result = chat(messages=messages, task_type=tt, temperature=temperature, system=system)
            result["provider_used"] = result.get("routed_via", "auto")
        return result
    else:
        # 降级：直接HTTP调用
        return _call_direct(messages, provider or "deepseek", temperature)

def _call_direct(messages: List[Dict], provider: str, temperature: float = 0.7) -> Dict[str, Any]:
    """直接HTTP调用（降级模式）"""
    import urllib.request, urllib.error
    
    configs = {
        "deepseek": {"url": "https://api.deepseek.com/v1/chat/completions", "model": "deepseek-v4-flash", "key_env": "DEEPSEEK_API_KEY"},
        "kimi": {"url": "https://api.moonshot.cn/v1/chat/completions", "model": "moonshot-v1-8k", "key_env": "KIMI_API_KEY"},
        "openai": {"url": "https://api.openai.com/v1/chat/completions", "model": "gpt-4o-mini", "key_env": "OPENAI_API_KEY"},
    }
    
    if provider not in configs:
        provider = "deepseek"
    
    config = configs[provider]
    api_key = os.environ.get(config["key_env"])
    if not api_key:
        raise ValueError(f"❌ {provider} API Key 未配置")
    
    payload = json.dumps({
        "model": config["model"],
        "messages": messages,
        "max_tokens": 4096,
        "temperature": temperature,
    }).encode()
    
    req = urllib.request.Request(config["url"], data=payload, headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    })
    
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            return {
                "content": data["choices"][0]["message"]["content"],
                "model": config["model"],
                "provider": provider,
                "provider_used": provider,
                "usage": data.get("usage", {}),
                "dna": build_dna(),
            }
    except Exception as e:
        raise RuntimeError(f"API 调用失败: {e}")

# ═══════════════════════════════════════════════════════
# FastAPI 应用
# ═══════════════════════════════════════════════════════

def create_app() -> "FastAPI":
    """创建 FastAPI 应用"""
    if not HAS_FASTAPI or not HAS_PYDANTIC:
        raise ImportError("需要 fastapi 和 pydantic: pip3 install fastapi uvicorn pydantic")
    
    app = FastAPI(
        title="龍魂·透明审计AI Hub",
        description="多模型统一对话 · 全链路透明审计 · 实时计费 · DNA追溯",
        version=VERSION,
        docs_url="/api/ai-hub/docs",
        redoc_url="/api/ai-hub/redoc",
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # ─── Pydantic 模型 ───
    class ChatRequest(BaseModel):
        message: str = Field(..., description="用户消息")
        session_id: Optional[str] = Field(None, description="会话ID")
        provider: Optional[str] = Field(None, description="指定模型: claude/deepseek/kimi/openai")
        task_type: Optional[str] = Field("general", description="任务类型: code/cn/translate/analyze/creative/math/general")
        temperature: Optional[float] = Field(0.7, ge=0, le=2)
        system: Optional[str] = Field("", description="系统提示词")
        stream: Optional[bool] = Field(False, description="流式输出")
    
    class CompareRequest(BaseModel):
        message: str = Field(..., description="对比问题")
        providers: List[str] = Field(["deepseek", "kimi"], description="要对比的模型列表")
        temperature: Optional[float] = Field(0.7)
    
    # ─── 端点 ───
    
    @app.get("/api/ai-hub/health")
    async def health():
        """健康检查"""
        return {
            "status": "ok",
            "version": VERSION,
            "dna": DNA,
            "timestamp": datetime.now().isoformat(),
        }
    
    @app.get("/api/ai-hub/models")
    async def list_models():
        """列出可用模型及状态"""
        models = []
        for key, meta in MODEL_META.items():
            pricing = MODEL_PRICING.get(key, {})
            # 检查API key
            available = False
            if key == "ollama":
                available = True
            elif HAS_HTTPX:
                try:
                    from bin.lh_ai_gateway import _get_api_key
                    available = bool(_get_api_key(key))
                except:
                    available = False
            models.append({
                "id": key,
                "name": meta["name"],
                "vendor": meta["vendor"],
                "type": meta["type"],
                "available": available,
                "pricing": pricing,
                "max_tokens": meta["max_tokens"],
            })
        return {"models": models, "total_available": sum(1 for m in models if m["available"])}
    
    @app.post("/api/ai-hub/chat")
    async def chat_endpoint(req: ChatRequest):
        """对话端点（全链路审计）"""
        request_id = uuid.uuid4().hex[:12]
        dna = build_dna()
        t0 = time.time()
        
        messages = [{"role": "user", "content": req.message}]
        if req.system:
            messages = [{"role": "system", "content": req.system}] + messages
        
        try:
            result = call_ai_gateway(
                messages=messages,
                provider=req.provider,
                task_type=req.task_type or "general",
                temperature=req.temperature or 0.7,
                system=req.system or "",
            )
            latency = (time.time() - t0) * 1000
            
            usage = result.get("usage", {})
            input_tokens = usage.get("prompt_tokens", usage.get("input_tokens", count_tokens_approx(req.message)))
            output_tokens = usage.get("completion_tokens", usage.get("output_tokens", count_tokens_approx(result.get("content", ""))))
            total_tokens = usage.get("total_tokens", input_tokens + output_tokens)
            
            provider_used = result.get("provider_used", result.get("provider", req.provider or "auto"))
            cost = estimate_cost(provider_used, input_tokens, output_tokens)
            
            # 保存审计
            audit_entry = {
                "request_id": request_id,
                "dna": dna,
                "session_id": req.session_id,
                "model_provider": provider_used,
                "model_name": result.get("model", ""),
                "messages": messages,
                "response_text": result.get("content", ""),
                "prompt_tokens": input_tokens,
                "completion_tokens": output_tokens,
                "total_tokens": total_tokens,
                "estimated_cost_usd": cost,
                "latency_ms": round(latency, 2),
                "task_type": req.task_type or "general",
                "sovereignty": MODEL_PRICING.get(provider_used, {}).get("sovereignty", "unknown"),
                "status": "success",
            }
            save_audit(audit_entry)
            
            return {
                "request_id": request_id,
                "dna": dna,
                "content": result.get("content", ""),
                "model": result.get("model", ""),
                "provider": provider_used,
                "transparency": {
                    "tokens": {
                        "input": input_tokens,
                        "output": output_tokens,
                        "total": total_tokens,
                    },
                    "cost_usd": cost,
                    "latency_ms": round(latency, 2),
                    "sovereignty": MODEL_PRICING.get(provider_used, {}).get("sovereignty", "unknown"),
                    "routing": {
                        "task_type": req.task_type or "general",
                        "provider_used": provider_used,
                    },
                },
            }
        except Exception as e:
            latency = (time.time() - t0) * 1000
            audit_entry = {
                "request_id": request_id,
                "dna": dna,
                "session_id": req.session_id,
                "model_provider": req.provider or "auto",
                "model_name": "",
                "messages": messages,
                "status": "error",
                "error_message": str(e),
                "latency_ms": round(latency, 2),
                "task_type": req.task_type or "general",
            }
            save_audit(audit_entry)
            logger.error(f"❌ 对话失败 [{request_id}]: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/api/ai-hub/compare")
    async def compare_endpoint(req: CompareRequest):
        """多模型对比端点"""
        request_id = uuid.uuid4().hex[:12]
        results = []
        total_cost = 0
        
        for provider in req.providers:
            t0 = time.time()
            dna = build_dna()
            try:
                result = call_ai_gateway(
                    messages=[{"role": "user", "content": req.message}],
                    provider=provider,
                    task_type="general",
                    temperature=req.temperature or 0.7,
                )
                latency = (time.time() - t0) * 1000
                usage = result.get("usage", {})
                input_tokens = usage.get("prompt_tokens", count_tokens_approx(req.message))
                output_tokens = usage.get("completion_tokens", count_tokens_approx(result.get("content", "")))
                cost = estimate_cost(provider, input_tokens, output_tokens)
                total_cost += cost
                
                results.append({
                    "provider": provider,
                    "model": result.get("model", ""),
                    "content": result.get("content", ""),
                    "dna": dna,
                    "tokens": {"input": input_tokens, "output": output_tokens, "total": input_tokens + output_tokens},
                    "cost_usd": cost,
                    "latency_ms": round(latency, 2),
                    "sovereignty": MODEL_PRICING.get(provider, {}).get("sovereignty", "unknown"),
                    "status": "success",
                })
            except Exception as e:
                results.append({
                    "provider": provider,
                    "status": "error",
                    "error": str(e),
                    "latency_ms": round((time.time() - t0) * 1000, 2),
                })
        
        return {
            "request_id": request_id,
            "question": req.message,
            "results": results,
            "total_cost_usd": round(total_cost, 6),
        }
    
    @app.get("/api/ai-hub/stats")
    async def stats_endpoint(days: int = Query(7, ge=1, le=90)):
        """用量统计"""
        return get_stats(days)
    
    @app.get("/api/ai-hub/history")
    async def history_endpoint(
        session_id: Optional[str] = Query(None),
        limit: int = Query(20, ge=1, le=100),
        offset: int = Query(0, ge=0),
    ):
        """对话历史"""
        conn = sqlite3.connect(str(AUDIT_DB))
        conn.row_factory = sqlite3.Row
        
        if session_id:
            rows = conn.execute(
                "SELECT * FROM audit_log WHERE session_id=? ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (session_id, limit, offset)
            ).fetchall()
            total = conn.execute("SELECT COUNT(*) FROM audit_log WHERE session_id=?", (session_id,)).fetchone()[0]
        else:
            rows = conn.execute(
                "SELECT * FROM audit_log ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (limit, offset)
            ).fetchall()
            total = conn.execute("SELECT COUNT(*) FROM audit_log").fetchone()[0]
        
        conn.close()
        
        history = []
        for r in rows:
            d = dict(r)
            d["messages"] = json.loads(d.get("messages_json", "[]"))
            del d["messages_json"]
            history.append(d)
        
        return {"history": history, "total": total, "limit": limit, "offset": offset}
    
    @app.get("/api/ai-hub/audit-report")
    async def audit_report_endpoint(days: int = Query(7, ge=1, le=90)):
        """生成审计报告"""
        stats = get_stats(days)
        
        conn = sqlite3.connect(str(AUDIT_DB))
        conn.row_factory = sqlite3.Row
        
        # 错误率
        errors = conn.execute(
            "SELECT COUNT(*) as c FROM audit_log WHERE status='error' AND created_at >= ?",
            ((datetime.now() - timedelta(days=days)).isoformat(),)
        ).fetchone()["c"]
        
        # 平均延迟
        avg_lat = conn.execute(
            "SELECT AVG(latency_ms) as a FROM audit_log WHERE status='success' AND created_at >= ?",
            ((datetime.now() - timedelta(days=days)).isoformat(),)
        ).fetchone()["a"] or 0
        
        # 主权分布
        sov = conn.execute("""
            SELECT sovereignty, COUNT(*) as c FROM audit_log 
            WHERE created_at >= ? GROUP BY sovereignty
        """, ((datetime.now() - timedelta(days=days)).isoformat(),)).fetchall()
        
        conn.close()
        
        error_rate = errors / max(1, stats["total_requests"]) * 100
        domestic = sum(s["c"] for s in sov if "境内" in (s["sovereignty"] or ""))
        overseas = sum(s["c"] for s in sov if "境外" in (s["sovereignty"] or ""))
        
        return {
            "report_id": build_dna(),
            "generated_at": datetime.now().isoformat(),
            "period_days": days,
            "summary": stats,
            "quality": {
                "success_rate": round(100 - error_rate, 2),
                "error_rate": round(error_rate, 2),
                "avg_latency_ms": round(avg_lat, 2),
            },
            "sovereignty": {
                "domestic_pct": round(domestic / max(1, domestic + overseas) * 100, 1),
                "overseas_pct": round(overseas / max(1, domestic + overseas) * 100, 1),
            },
            "recommendations": _generate_recommendations(stats, error_rate, avg_lat),
        }
    
    return app

def _generate_recommendations(stats: Dict, error_rate: float, avg_lat: float) -> List[str]:
    """生成智能建议"""
    recs = []
    if error_rate > 5:
        recs.append(f"⚠️ 错误率 {error_rate:.1f}%，建议检查API密钥配置")
    if avg_lat > 5000:
        recs.append(f"⚠️ 平均延迟 {avg_lat:.0f}ms 偏高，考虑切换更快的模型")
    cost = stats.get("total_cost_usd", 0)
    if cost > 10:
        recs.append(f"💰 累计费用 ${cost:.4f}，建议启用本地Ollama降低云端调用")
    # 检查境内占比
    if stats.get("total_requests", 0) > 0:
        recs.append("✅ 建议优先使用境内模型（DeepSeek/Kimi/混元）保护数据主权")
    if not recs:
        recs.append("✅ 系统运行正常，各项指标健康")
    return recs

# ═══════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="龍魂·透明审计AI Hub API")
    parser.add_argument("--port", type=int, default=8778, help="监听端口 (默认8778)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="监听地址")
    parser.add_argument("--reload", action="store_true", help="开发热重载")
    
    args = parser.parse_args()
    
    init_db()
    
    if not HAS_FASTAPI:
        logger.error("需要 FastAPI: pip3 install fastapi uvicorn pydantic")
        sys.exit(1)
    
    logger.info(f"🐉 龍魂·透明审计AI Hub API v{VERSION}")
    logger.info(f"   端口: {args.port}")
    logger.info(f"   审计数据库: {AUDIT_DB}")
    logger.info(f"   API文档: http://localhost:{args.port}/api/ai-hub/docs")
    
    app = create_app()
    uvicorn.run(app, host=args.host, port=args.port, reload=args.reload, log_level="info")

if __name__ == "__main__":
    main()
