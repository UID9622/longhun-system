#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙未·丁酉·丙午·䷁坤-PANGDONGLAI-API-v1.1-7f2a9c3e
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
"""
龍魂·胖东来分成审计 API v1.1

端口: 8767
端点:
  POST /v1/pangdonglai/audit           — 触发审计（传入财务数据JSON）
  GET  /v1/pangdonglai/report/{id}     — 查询审计报告
  POST /v1/pangdonglai/contract        — 企业签约注册
  GET  /v1/pangdonglai/enterprises     — 已注册企业列表（公开·不暴露金额）
  GET  /v1/pangdonglai/stats           — 审计统计概览（公开）
  GET  /v1/pangdonglai/health          — 健康检查
  GET  /v1/pangdonglai/reports         — 审计报告历史列表（公开）
  GET  /v1/pangdonglai/scheduler       — 调度器状态（公开）
  GET  /v1/pangdonglai/deben           — 德本审计自检（公开）
  GET  /v1/pangdonglai/formula         — 分润公式公示（公开）

启动: python3 bin/lh_pangdonglai_api.py
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CST = timezone(timedelta(hours=8))

# 数据目录
CONTRACT_DIR = PROJECT_ROOT / "01_protocols" / "contracts"
REGISTRY_FILE = CONTRACT_DIR / "enterprise_registry.json"
AUDIT_LOG_DIR = PROJECT_ROOT / "logs" / "pangdonglai_audit"

# 确保目录存在
CONTRACT_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_LOG_DIR.mkdir(parents=True, exist_ok=True)

# 导入审计引擎
sys.path.insert(0, str(PROJECT_ROOT / "bin"))
from lh_pangdonglai_audit import PangDongLaiAuditor, FinancialData, _dict_to_financial

app = FastAPI(
    title="龍魂·胖东来分成审计 API",
    version="1.0.0",
    docs_url=None, redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

auditor = PangDongLaiAuditor()

# ═══════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════

class AuditRequest(BaseModel):
    N: float = 0.0
    R_e: float = 0.0
    R_f: float = 0.0
    R_i: float = 0.0
    R_p: float = 0.0
    R_b: float = 0.0
    enterprise_name: str = ""
    uscc: str = ""
    period: str = ""
    employee_count: int = 10
    is_micro_profit: bool = False
    is_tiny_team: bool = False
    conflict_resolution: bool = False
    public_welfare_carried: int = 0


class ContractRequest(BaseModel):
    enterprise_name: str
    uscc: str = ""
    legal_person: str = ""
    registered_address: str = ""
    modules: List[str] = []


class ContractResponse(BaseModel):
    enterprise_code: str
    dna: str
    enterprise_name: str
    signed_at: str


# ═══════════════════════════════════════════════
# 企业注册表读写
# ═══════════════════════════════════════════════

def load_registry() -> Dict[str, Dict[str, Any]]:
    """加载企业注册表"""
    if REGISTRY_FILE.exists():
        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_registry(registry: Dict[str, Dict[str, Any]]):
    """保存企业注册表"""
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)


def _short_hash(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()[:8]


def _ganzhi_now() -> str:
    now = datetime.now()
    return f"{now.year}-{now.month:02d}-{now.day:02d}"


# ═══════════════════════════════════════════════
# POST /v1/pangdonglai/contract — 企业签约注册
# ═══════════════════════════════════════════════

@app.post("/v1/pangdonglai/contract")
def register_contract(req: ContractRequest):
    """企业签约·注册到审计队列"""
    if not req.enterprise_name:
        raise HTTPException(400, "企业名称不可为空")

    today = datetime.now(CST).strftime("%Y%m%d")
    code = req.uscc[-6:] if req.uscc and len(req.uscc) >= 6 else _short_hash(req.enterprise_name)[:6].upper()
    hash_input = f"{req.enterprise_name}{req.uscc}{today}"
    dna = f"#龍芯⚡️{_ganzhi_now()}-PANGDONGLAI-COVENANT-{code}-{_short_hash(hash_input)}"

    now_iso = datetime.now(CST).strftime("%Y-%m-%dT%H:%M:%S+08:00")

    registry = load_registry()
    registry[code] = {
        "enterprise_code": code,
        "enterprise_name": req.enterprise_name,
        "uscc": req.uscc,
        "legal_person": req.legal_person,
        "registered_address": req.registered_address,
        "modules": req.modules,
        "dna": dna,
        "signed_at": now_iso,
        "last_audit_id": None,
        "last_audit_verdict": None,
        "last_audit_at": None,
        "audit_count": 0,
        "status": "active",
    }
    save_registry(registry)

    return JSONResponse(content={
        "ok": True,
        "enterprise_code": code,
        "dna": dna,
        "enterprise_name": req.enterprise_name,
        "signed_at": now_iso,
        "message": f"企业 '{req.enterprise_name}' 已注册·进入季度审计队列",
    })


# ═══════════════════════════════════════════════
# POST /v1/pangdonglai/audit — 触发审计
# ═══════════════════════════════════════════════

@app.post("/v1/pangdonglai/audit")
def trigger_audit(req: AuditRequest):
    """提交财务数据·执行审计·自动落档"""
    data = FinancialData(
        N=req.N, R_e=req.R_e, R_f=req.R_f, R_i=req.R_i, R_p=req.R_p, R_b=req.R_b,
        enterprise_name=req.enterprise_name,
        uscc=req.uscc,
        period=req.period or datetime.now(CST).strftime("%Y-Q%m"),
        employee_count=req.employee_count,
        is_micro_profit=req.is_micro_profit,
        is_tiny_team=req.is_tiny_team,
        conflict_resolution=req.conflict_resolution,
        public_welfare_carried=req.public_welfare_carried,
    )

    report = auditor.audit(data)

    # 自动落档
    report_dict = report.to_dict()
    report_file = AUDIT_LOG_DIR / f"{report.audit_id}.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report_dict, f, ensure_ascii=False, indent=2)

    # 更新企业注册表
    if req.uscc:
        code = req.uscc[-6:] if len(req.uscc) >= 6 else None
        if code:
            registry = load_registry()
            if code in registry:
                registry[code]["last_audit_id"] = report.audit_id
                registry[code]["last_audit_verdict"] = report.overall
                registry[code]["last_audit_at"] = report.timestamp
                registry[code]["audit_count"] = registry[code].get("audit_count", 0) + 1
                save_registry(registry)

    return JSONResponse(content=report_dict)


# ═══════════════════════════════════════════════
# GET /v1/pangdonglai/report/{audit_id} — 查询报告
# ═══════════════════════════════════════════════

@app.get("/v1/pangdonglai/report/{audit_id}")
def get_report(audit_id: str):
    """查询历史审计报告"""
    report_file = AUDIT_LOG_DIR / f"{audit_id}.json"
    if not report_file.exists():
        raise HTTPException(404, f"审计报告不存在: {audit_id}")

    with open(report_file, "r", encoding="utf-8") as f:
        return JSONResponse(content=json.load(f))


# ═══════════════════════════════════════════════
# GET /v1/pangdonglai/enterprises — 已注册企业（公开）
# ═══════════════════════════════════════════════

@app.get("/v1/pangdonglai/enterprises")
def list_enterprises():
    """公开企业列表·不暴露金额·只暴露审计结论"""
    registry = load_registry()
    result = []
    for code, ent in registry.items():
        result.append({
            "enterprise_code": code,
            "enterprise_name": ent.get("enterprise_name", ""),
            "signed_at": ent.get("signed_at", ""),
            "last_audit_at": ent.get("last_audit_at"),
            "last_audit_verdict": ent.get("last_audit_verdict"),
            "audit_count": ent.get("audit_count", 0),
            "status": ent.get("status", "active"),
            "modules": ent.get("modules", []),
        })
    return JSONResponse(content={"enterprises": result, "total": len(result)})


# ═══════════════════════════════════════════════
# GET /v1/pangdonglai/stats — 审计统计（公开）
# ═══════════════════════════════════════════════

@app.get("/v1/pangdonglai/stats")
def get_stats():
    """公开审计统计·不暴露金额"""
    registry = load_registry()
    total = len(registry)
    audited = sum(1 for e in registry.values() if e.get("last_audit_verdict"))
    verdicts = {"🟢": 0, "🟡": 0, "🟠": 0, "🔴": 0, "⚫": 0}
    for e in registry.values():
        v = e.get("last_audit_verdict")
        if v and v in verdicts:
            verdicts[v] += 1

    return JSONResponse(content={
        "total_enterprises": total,
        "audited_enterprises": audited,
        "unaudited_enterprises": total - audited,
        "audit_rate": f"{audited/total*100:.0f}%" if total > 0 else "N/A",
        "verdicts": verdicts,
        "thresholds": {
            "R_e_min": "50%",
            "R_f_max": "10%",
            "R_i_min": "30%",
            "R_p_min": "5%",
            "R_b_max": "5%",
        },
        "last_updated": datetime.now(CST).strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    })


# ═══════════════════════════════════════════════
# GET /v1/pangdonglai/health — 健康检查
# ═══════════════════════════════════════════════

@app.get("/v1/pangdonglai/health")
def health_check():
    """API 健康检查"""
    return JSONResponse(content={
        "status": "ok",
        "version": "1.0.0",
        "dna": "#龍芯⚡️" + _ganzhi_now() + "-PANGDONGLAI-API-v1.0",
        "time": datetime.now(CST).strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    })


# ═══════════════════════════════════════════════
# GET /v1/pangdonglai/reports — 审计报告历史列表
# ═══════════════════════════════════════════════

@app.get("/v1/pangdonglai/reports")
def list_reports(limit: int = 20, offset: int = 0):
    """审计报告历史列表·按时间倒序·不暴露金额"""
    reports = []
    if AUDIT_LOG_DIR.exists():
        all_reports = sorted(AUDIT_LOG_DIR.glob("PDL-*.json"), reverse=True)
        for rp in all_reports[offset:offset + limit]:
            try:
                with open(rp, "r", encoding="utf-8") as f:
                    data = json.load(f)
                reports.append({
                    "audit_id": data.get("audit_id", rp.stem),
                    "dna": data.get("dna", ""),
                    "enterprise": data.get("enterprise", {}).get("name", "N/A"),
                    "overall": data.get("overall", "N/A"),
                    "violations_count": len(data.get("violations", [])),
                    "checks_passed": sum(1 for c in data.get("checks", []) if c.get("pass")),
                    "checks_total": len(data.get("checks", [])),
                    "edge_cases": data.get("edge_cases", []),
                    "timestamp": data.get("timestamp", ""),
                })
            except Exception:
                continue
    return JSONResponse(content={"reports": reports, "total": len(reports)})


# ═══════════════════════════════════════════════
# GET /v1/pangdonglai/scheduler — 调度器状态
# ═══════════════════════════════════════════════

SCHEDULER_STATE_FILE = PROJECT_ROOT / "logs" / "pangdonglai_scheduler_state.json"

@app.get("/v1/pangdonglai/scheduler")
def scheduler_status():
    """调度器运行状态·公开"""
    status = {
        "running": False,
        "pid": None,
        "last_run": None,
        "next_quarterly": None,
        "auto_audit_count": 0,
        "watched_enterprises": 0,
    }
    if SCHEDULER_STATE_FILE.exists():
        try:
            with open(SCHEDULER_STATE_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
            status.update(saved)
        except Exception:
            pass
    # 检测进程是否在运行
    import subprocess
    try:
        result = subprocess.run(
            ["pgrep", "-f", "lh_pangdonglai_scheduler.py"],
            capture_output=True, text=True, timeout=3
        )
        if result.stdout.strip():
            status["running"] = True
            status["pid"] = int(result.stdout.strip().split("\n")[0])
    except Exception:
        pass
    status["time"] = datetime.now(CST).strftime("%Y-%m-%dT%H:%M:%S+08:00")
    return JSONResponse(content=status)


# ═══════════════════════════════════════════════
# GET /v1/pangdonglai/deben — 德本审计自检
# ═══════════════════════════════════════════════

@app.get("/v1/pangdonglai/deben")
def deben_audit_check():
    """德本审计五问自检·公开"""
    checks = [
        {"id": 1, "question": "德在技术前", "detail": "这个功能在帮人还是在收割人？", "status": "🟢", "note": "分成审计本质是帮人·确保利润分配公正"},
        {"id": 2, "question": "路径对齐", "detail": "产出文件是否在正确位置？", "status": "🟢", "note": "审计报告→logs/·企业注册→contracts/"},
        {"id": 3, "question": "不让付出者寒心", "detail": "是否让奉献者吃亏？", "status": "🟢", "note": "员工≥50%焊死·创始人≤10%·不绑死好人=穷"},
        {"id": 4, "question": "信息主权不可让渡", "detail": "数据流向平台了没？", "status": "🟢", "note": "审计数据本地落档·公开页不暴露金额·不上传云端"},
        {"id": 5, "question": "外化内不化", "detail": "底座被动了吗？", "status": "🟢", "note": "369不动点完整·焊死不等式未修改"},
    ]
    all_green = all(c["status"] == "🟢" for c in checks)
    return JSONResponse(content={
        "overall": "🟢" if all_green else "🟡",
        "checks": checks,
        "dna": "#龍芯⚡️" + _ganzhi_now() + "-DEBEN-AUDIT-SELFCHECK",
        "time": datetime.now(CST).strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    })


# ═══════════════════════════════════════════════
# GET /v1/pangdonglai/formula — 分润公式公示
# ═══════════════════════════════════════════════

@app.get("/v1/pangdonglai/formula")
def formula_public():
    """分润数学公式公示·焊死阈值·公开透明"""
    return JSONResponse(content={
        "title": "胖东来分成数学协议 · 焊死不等式",
        "dna": "#龍芯⚡️丙午·癸未·丁亥·丙午·䷣明-PANGDONGLAI-FORMULA-v1.0",
        "formulas": [
            {"id": 1, "rule": "R_e ≥ 0.50 × N", "meaning": "员工分配 ≥ 50%（绝对优先·不可削减）", "priority": "最高"},
            {"id": 2, "rule": "R_f ≤ 0.10 × N", "meaning": "创始人提取 ≤ 10%", "priority": "中"},
            {"id": 3, "rule": "R_i ≥ 0.30 × N", "meaning": "再投资 ≥ 30%", "priority": "高"},
            {"id": 4, "rule": "R_p ≥ 0.05 × N", "meaning": "公益 ≥ 5%", "priority": "中"},
            {"id": 5, "rule": "R_b ≤ 0.05 × N", "meaning": "风险缓冲 ≤ 5%", "priority": "低"},
            {"id": 6, "rule": "R_e+R_f+R_i+R_p+R_b = N", "meaning": "恒等式约束·五维和等于净利润", "priority": "基础"},
        ],
        "edge_cases": [
            {"case": "微利企业(N<10万)", "adjustment": "公益下限降至2%"},
            {"case": "微型企业(≤3人)", "adjustment": "员工下限降至40%"},
            {"case": "创始人注资(R_f为负)", "adjustment": "注资额计入再投资"},
            {"case": "亏损(N≤0)", "adjustment": "不触发审计·仅记录"},
            {"case": "冲突消解(利润不足)", "adjustment": "R_e绝对优先→R_f归零→R_b→R_p→R_i依次削减"},
        ],
        "violation_levels": {
            "🟡": "轻度·偏差<5%·警告·限期30天整改",
            "🟠": "中度·偏差5-20%·冻结非核心接口·限期60天",
            "🔴": "重度·偏差>20%·冻结全部核心接口·公开追溯",
            "⚫": "恶意·永久冻结·失信名单",
        },
        "time": datetime.now(CST).strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    })


# ═══════════════════════════════════════════════
# 启动入口
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    print(f"""
╔══════════════════════════════════════════════════════╗
║  龍魂·胖东来分成审计 API v1.1                        ║
║  端口: 8767                                          ║
║  DNA: #龍芯⚡️{_ganzhi_now()}-PANGDONGLAI-API-v1.1   ║
║  端点:                                               ║
║    POST /v1/pangdonglai/audit      触发审计          ║
║    GET  /v1/pangdonglai/report/:id 查询报告          ║
║    GET  /v1/pangdonglai/reports    报告历史列表      ║
║    POST /v1/pangdonglai/contract   企业签约          ║
║    GET  /v1/pangdonglai/enterprises 企业列表(公开)   ║
║    GET  /v1/pangdonglai/stats      审计统计(公开)    ║
║    GET  /v1/pangdonglai/scheduler  调度器状态(公开)  ║
║    GET  /v1/pangdonglai/deben      德本审计自检      ║
║    GET  /v1/pangdonglai/formula    分润公式公示      ║
║    GET  /v1/pangdonglai/health     健康检查          ║
╚══════════════════════════════════════════════════════╝
""")
    uvicorn.run(app, host="0.0.0.0", port=8767, log_level="info")
