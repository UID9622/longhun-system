#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 行业痛点治理 API 服务
DNA: #龍芯⚡️丙午·丙申·丁酉·辛丑·䷹兑为泽-GOVERNANCE-API-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
License: MulanPSL v2

功能: 对外暴露 REST API，让外部系统调用八大痛点治理能力。
      默认监听 127.0.0.1:8781，鲲鹏 ARM64 原生。

端点:
  GET  /                    服务状态
  GET  /pain-points         八大痛点列表
  POST /assess              评估指定痛点
  POST /act                 执行治理动作
  POST /report              评估+执行联合报告
  GET  /dashboard           治理看板
  POST /all-assess          批量评估全部痛点
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from engines.lh_industry_governance import (
    ENGINE_DNA,
    SUBSYSTEMS,
    PAIN_POINT_MAP,
    GovernanceOrchestrator,
)

sys.path.insert(0, str(PROJECT_ROOT / "08_BIN"))
from lh_bilingual_router import BilingualCommandRouter
_bilingual_router = BilingualCommandRouter()

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # 类型检查时使用真实类型；运行时走下方 try/except
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    from uvicorn import run
    HAS_FASTAPI = True
else:
    try:
        from fastapi import FastAPI, HTTPException
        from pydantic import BaseModel
        from uvicorn import run
        HAS_FASTAPI = True
    except Exception:
        HAS_FASTAPI = False


def _is_known_pain_point(name: str) -> bool:
    if name in SUBSYSTEMS or name in PAIN_POINT_MAP:
        return True
    return _bilingual_router.resolve_pain_point(name) is not None


if HAS_FASTAPI:
    app = FastAPI(title="龍魂行业痛点治理 API", version="1.0")
    _orchestrator: Optional[GovernanceOrchestrator] = None

    def get_orchestrator() -> GovernanceOrchestrator:
        global _orchestrator
        if _orchestrator is None:
            _orchestrator = GovernanceOrchestrator()
        return _orchestrator

    class DispatchRequest(BaseModel):
        pain_point: str
        action: str = "assess"
        context: Dict[str, Any] = {}

    class ContextRequest(BaseModel):
        context: Dict[str, Any] = {}

    @app.get("/")
    def root():
        return {"dna": ENGINE_DNA, "status": "running"}

    @app.get("/pain-points")
    def pain_points():
        return {
            "dna": ENGINE_DNA,
            "pain_points": [
                {"id": sub_key, "name": pain_name, "description": SUBSYSTEMS[sub_key].pain_point}
                for pain_name, sub_key in PAIN_POINT_MAP.items()
            ],
        }

    @app.post("/assess")
    def assess(req: DispatchRequest):
        if not _is_known_pain_point(req.pain_point):
            raise HTTPException(status_code=400, detail=f"未知痛点: {req.pain_point}")
        return get_orchestrator().dispatch(req.pain_point, "assess", req.context)

    @app.post("/act")
    def act(req: DispatchRequest):
        if not _is_known_pain_point(req.pain_point):
            raise HTTPException(status_code=400, detail=f"未知痛点: {req.pain_point}")
        # /act 端点默认动作为 act；若显式传入其他动作（如中文别名）则解析后使用
        action = req.action if req.action and req.action != "assess" else "act"
        return get_orchestrator().dispatch(req.pain_point, action, req.context)

    @app.post("/report")
    def report(req: DispatchRequest):
        if not _is_known_pain_point(req.pain_point):
            raise HTTPException(status_code=400, detail=f"未知痛点: {req.pain_point}")
        return get_orchestrator().dispatch(req.pain_point, "report", req.context)

    @app.get("/dashboard")
    def dashboard():
        return get_orchestrator().dashboard()

    @app.post("/all-assess")
    def all_assess(req: ContextRequest):
        return get_orchestrator().all_assess()


def cli():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂行业痛点治理 API 服务")
    parser.add_argument("--host", default="127.0.0.1", help="监听地址")
    parser.add_argument("--port", type=int, default=8781, help="监听端口")
    args = parser.parse_args()

    if not HAS_FASTAPI:
        print("❌ 需要 fastapi + uvicorn，请安装: pip install 'longhun-system[server]'")
        sys.exit(1)

    print(f"🐉 治理 API 服务启动: http://{args.host}:{args.port}")
    run(app, host=args.host, port=args.port, log_level="warning")


if __name__ == "__main__":
    cli()

# ⛓️ 龍魂DNA接龍链 ──────────────────────────────
# DNA:V1|丙午·丙申·癸亥·辰时·䷗复|P04鲁班|创建|透明看板+双语路由封装|bhash:511167ea|chash:67151094|←GENESIS
# DNA:V2|丙午·丙申·癸亥·辰时·䷗复|P04鲁班|修改|治理API封装|bhash:227aa3a7|chash:d073ff51|←67151094
# ⛓️ 龍魂DNA接龍末端 ──────────────────────────────
