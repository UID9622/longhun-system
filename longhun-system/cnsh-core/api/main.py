"""
CNSH-64 API Server · FastAPI
端口: 9622 (与龍魂系统一致)

v0.4.0 — 四敢品质系统 + LocalShield三层防御

Author: 诸葛鑫 (UID9622)
DNA: #ZHUGEXIN⚡️2026-03-23-API-SERVER-v1.0
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from datetime import datetime
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core import Event, Action, AuditColor
from governance.state_mapper import StateMapper
from governance.risk_engine import RiskEngine
from governance.ethics_engine import EthicsEngine
from governance.decision_engine import DecisionEngine
from security.dna_ledger.ledger import DNALedger
from dna_calendar.api import router as calendar_router
from registry.api    import router as registry_router
from projection.api  import router as projection_router
from dare.api        import router as dare_router
from shield.api      import router as shield_router
from persona.router  import router as persona_router
from runtime.parser  import parse_safe
from runtime.router  import dispatch as cnsh_dispatch
from mvp.api         import router as mvp_router

# 导入龍魂人格路由的洛书状态（三才流場 v5 实时同步）
import sys, time
_longhun_api = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "longhun_api")
if os.path.isdir(_longhun_api) and _longhun_api not in sys.path:
    sys.path.insert(0, _longhun_api)
try:
    from persona_router import LOSU
    from persona_router import now_cst
except Exception:
    LOSU = None
    def now_cst():
        from datetime import datetime, timezone, timedelta
        CST = timezone(timedelta(hours=8))
        return datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S CST")


# ─── 初始化 ─────────────────────────────────────────────
app = FastAPI(title="CNSH-64 Governance Engine", version="0.4.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)
app.include_router(calendar_router)
app.include_router(registry_router)
app.include_router(projection_router)
app.include_router(dare_router)
app.include_router(shield_router)
app.include_router(mvp_router)
app.include_router(persona_router)   # /persona/route + /persona/stats + /persona/fence-hit

# MVP v2.0 静态前端
_mvp_static = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mvp", "static")
app.mount("/mvp/static", StaticFiles(directory=_mvp_static, html=True), name="mvp_static")

# 静态文件：日历前端
_static = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dna_calendar", "static")
app.mount("/ui", StaticFiles(directory=_static, html=True), name="static")
state_mapper = StateMapper()
risk_engine  = RiskEngine()
ethics_engine = EthicsEngine()
decision_engine = DecisionEngine()
ledger       = DNALedger()


# ─── 请求模型 ────────────────────────────────────────────
class EventRequest(BaseModel):
    content:   str
    user_id:   str = "anonymous"
    metadata:  Dict = {}

class RiskRequest(BaseModel):
    R: float = 0.0
    U: float = 0.0
    I: float = 0.0

class AuditRequest(BaseModel):
    scores: List[float]


# ─── 路由 ────────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "system":  "CNSH-64 Governance Engine",
        "version": "0.4.0",
        "author":  "诸葛鑫 UID9622 · 龍魂系统",
        "status":  "🟢 运行中",
        "layers":  {
            "L1-L2": "✅ CNSH语法层 + 命令解析器",
            "L3":    "✅ 注册表 · 私域/公域边界",
            "L4":    "✅ 伦理熔断 + 风险引擎",
            "L5-L6": "✅ 日历时空胶囊 + 时间轴",
            "L7":    "✅ 元现实投影 · GPS去敏地球仪",
            "L8":    "✅ 四敢品质 · 六爻+道德经彩蛋",
            "L9":    "✅ LocalShield · 三层防御统一入口",
        },
        "ui": {
            "calendar":  "/ui/index.html",
            "timeline":  "/ui/timeline.html",
            "globe":     "/ui/globe.html",
            "mvp":       "/mvp/static/index.html",
        },
    }


# ─── CNSH 统一语法入口 ───────────────────────────────────────────

class CNSHRequest(BaseModel):
    cnsh:       str           # 原始CNSH指令字符串
    user_id:    str = "UID9622"
    session_id: str = ""

@app.post("/cnsh")
def execute_cnsh(req: CNSHRequest):
    """
    CNSH统一语法执行入口
    所有操作的唯一入口，不允许绕过
    """
    cmd, err = parse_safe(req.cnsh, user_id=req.user_id)
    if err:
        raise HTTPException(status_code=400, detail=f"CNSH语法错误: {err}")

    cmd.session_id = req.session_id

    try:
        result = cnsh_dispatch(cmd)
        return {
            "cmd":        cmd.full_cmd,
            "params":     cmd.params,
            "flags":      cmd.flags,
            "ext_id":     cmd.ext_id,
            "result":     result,
            "dna_trace":  cmd.dna_trace or "",
            "parsed":     cmd.summary(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/cnsh/help")
def cnsh_help():
    """CNSH语法帮助"""
    from runtime.router import dispatch as d
    from runtime.command import CNSHCommand
    fake = CNSHCommand(domain="SYSTEM", verb="HELP", params={}, flags=[], ext_id=None)
    return d(fake)


@app.post("/event")
def process_event(req: EventRequest):
    """完整事件处理流水线"""
    ts    = datetime.utcnow().isoformat()
    event = Event(content=req.content, user_id=req.user_id,
                  timestamp=ts, metadata=req.metadata)

    # 1. 状态映射
    composite = state_mapper.map(event)

    # 2. 风险评估（快速模式，从 metadata 取值）
    R = req.metadata.get("R", 0.2)
    U = req.metadata.get("U", 0.3)
    I = req.metadata.get("I", 0.1)
    risk_vec = risk_engine.quick_evaluate(R=R, U=U, I=I)

    # 3. 决策
    action = decision_engine.decide(risk_vec)

    # 4. 伦理检查
    eth_pass, blocked = ethics_engine.check(req.metadata)
    if not eth_pass:
        action = Action.BLOCK

    # 5. 三色审计
    audit_scores = req.metadata.get("audit_scores", [75, 80, 70, 72, 68, 85, 90, 78])
    color = decision_engine.tri_color_audit(audit_scores)

    # 6. 解释 + DNA
    explanation = decision_engine.explain(
        composite, risk_vec, action, color, eth_pass, blocked
    )
    hexagram = decision_engine.get_hexagram(composite)

    # 7. 写账本
    record = ledger.append(
        event_content   = req.content,
        composite_state = str(composite),
        action          = action.value,
        risk_score      = risk_vec,
        audit_color     = color.value,
        user_id         = req.user_id,
        metadata        = req.metadata,
    )

    return {
        "composite_state": str(composite),
        "hexagram":        hexagram,
        "risk_score":      risk_vec,
        "action":          action.value,
        "audit_color":     color.value,
        "ethical_pass":    eth_pass,
        "blocked_rules":   blocked,
        "explanation":     explanation,
        "dna_trace":       record.dna_trace,
    }


@app.post("/risk")
def evaluate_risk(req: RiskRequest):
    """独立风险评估接口"""
    score = risk_engine.quick_evaluate(R=req.R, U=req.U, I=req.I)
    action = decision_engine.decide(score)
    return {"risk_score": score, "decision": action.value}


@app.post("/audit")
def audit_scores(req: AuditRequest):
    """三色审计接口"""
    color = decision_engine.tri_color_audit(req.scores)
    return {
        "audit_color": color.value,
        "avg_score":   sum(req.scores) / len(req.scores) if req.scores else 0,
        "min_score":   min(req.scores) if req.scores else 0,
    }


@app.get("/dna/{user_id}")
def query_dna(user_id: str, limit: int = 20):
    """查询 DNA 账本"""
    records = ledger.query(user_id=user_id, limit=limit)
    return {"user_id": user_id, "count": len(records), "records": records}


@app.get("/ledger/verify")
def verify_ledger():
    """验证账本完整性"""
    ok = ledger.verify_integrity()
    return {"integrity": "🟢 完好" if ok else "🔴 已篡改", "verified": ok}


@app.get("/ethics/rules")
def list_ethics_rules():
    return {"rules": ethics_engine.list_rules()}


# ── 洛书引擎端点（三才流場 v5 实时同步）────────────────────────────────
@app.get("/loShu/ethics_status")
def loShu_ethics():
    """伦理置信度 · 三维灰度"""
    if LOSU:
        return LOSU.ethics_status
    return {"redConf": 0.0, "orangeConf": 0.0, "greenConf": 1.0, "fuse_count": 0, "total_routes": 0}


@app.get("/loShu/merkle_density")
def loShu_density():
    """Merkle节点密度 · 人格多样性 × 平均得分"""
    if LOSU:
        return {"density": LOSU.merkle_density, "timestamp": now_cst()}
    return {"density": 0.5, "timestamp": now_cst()}


@app.get("/loShu/audit_count")
def loShu_audit():
    """累计审计次数 · 留痕粒子价值熵基准"""
    if LOSU:
        return {"count": LOSU.audit_count, "persona_hits": LOSU._persona_hits, "timestamp": now_cst()}
    return {"count": 0, "persona_hits": {}, "timestamp": now_cst()}


@app.get("/loShu/shield_status")
def loShu_shield():
    """龍盾完整状态 · 包含四律 + 所有维度"""
    if LOSU:
        return LOSU.to_shield_status()
    return {"ethics": {}, "merkle_density": 0.5, "audit_count": 0, "persona_hits": {}, "uptime_seconds": 0, "timestamp": now_cst(), "dna": "#龍芯⚡️LOSHU-LIVE"}


@app.get("/loShu/seed")
def loShu_seed():
    """宇宙种子 · UID9622 唯一锚点"""
    return {
        "seed": 9622,
        "uid": "UID9622",
        "anchor": "唯一宇宙锚点",
        "creator": "诸葛鑫·龍芯北辰",
        "dna": "#龍芯⚡️SEED-9622",
        "timestamp": now_cst()
    }


@app.get("/loShu/anchors")
def loShu_anchors():
    """洛书九宫格坐标 · 三才定位基础"""
    return {
        "grid": [[4, 9, 2], [3, 5, 7], [8, 1, 6]],
        "center": 5,
        "seed": 9622,
        "positions": {
            "天": {"value": 9, "dir": "南", "element": "火"},
            "地": {"value": 1, "dir": "北", "element": "水"},
            "人": {"value": 5, "dir": "中", "element": "土"},
            "木": {"value": 3, "dir": "东", "element": "木"},
            "金": {"value": 7, "dir": "西", "element": "金"},
        },
        "dna": "#龍芯⚡️ANCHORS-9622",
        "timestamp": now_cst()
    }


@app.get("/loShu/entropy")
def loShu_entropy():
    """系统熵值 · 人格分布多样性指数"""
    import math
    from persona.router import _counts
    total = sum(_counts.values()) or 1
    probs = [c / total for c in _counts.values() if c > 0]
    entropy = -sum(p * math.log2(p) for p in probs) if probs else 0.0
    max_e = math.log2(len(_counts)) if len(_counts) > 1 else 1.0
    normalized = round(entropy / max_e, 4) if max_e > 0 else 0.0
    return {
        "entropy": round(entropy, 4),
        "normalized": normalized,
        "max_entropy": round(max_e, 4),
        "persona_distribution": dict(_counts),
        "interpretation": "人格多样·系统活跃" if normalized > 0.6 else "人格收敛·单一主导",
        "dna": "#龍芯⚡️ENTROPY-9622",
        "timestamp": now_cst()
    }


class TranslateRequest(BaseModel):
    content: str
    uid: str = "UID9622"


@app.post("/loShu/translate")
def loShu_translate(req: TranslateRequest):
    """洛书翻译引擎主入口 · 三才解析"""
    from persona.router import ROUTING_RULES, DEFAULT_PERSONA
    matched = None
    for rule in ROUTING_RULES:
        for kw in rule["keywords"]:
            if kw in req.content:
                matched = rule
                break
        if matched:
            break
    if not matched:
        matched = DEFAULT_PERSONA
    return {
        "input": req.content,
        "persona": matched.get("persona", "宝宝·温度"),
        "logic": matched.get("logic", ""),
        "sancai": {"天": "系统规则·边界", "地": "数据记忆·落地", "人": "意图情感·行动"},
        "seed": 9622,
        "dna": f"#龍芯⚡️TRANSLATE-9622",
        "timestamp": now_cst()
    }


# 流场染色状态（内存存储）
_flow_color_state: dict = {"hue": 180.0, "intensity": 0.5, "trigger": "default", "timestamp": ""}


class ColorizeRequest(BaseModel):
    hue: float = 180.0
    intensity: float = 0.5
    trigger: str = "manual"


@app.post("/flow/colorize")
def flow_colorize_push(req: ColorizeRequest):
    """向三才流场推送染色指令"""
    global _flow_color_state
    _flow_color_state = {
        "hue": max(0.0, min(360.0, req.hue)),
        "intensity": max(0.0, min(1.0, req.intensity)),
        "trigger": req.trigger,
        "timestamp": now_cst()
    }
    return {"status": "ok", "applied": _flow_color_state, "dna": "#龍芯⚡️COLORIZE-9622"}


@app.get("/flow/colorize")
def flow_colorize_state():
    """读取当前流场染色状态"""
    return _flow_color_state


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9622, log_level="info")
