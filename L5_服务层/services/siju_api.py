# ============================================================
# 龍魂四绝 · 开店决策 API（FastAPI）
# 文件：L5_服务层/services/siju_api.py
# DNA：#龍芯⚡️丙午·辛未·四绝-API-v1.0
#
# 接口：
#   POST /api/siju/analyze  {address, category, user_types, user_crowds, user_funds, radius}
#   GET  /api/siju/report/{dna_trace}
#   POST /api/siju/confirm  {dna_trace, confirm_code}
# 真实数据来自 siju_etl（高德），政策/风俗来自 siju_knowledge（LIB级+引用依据）
# 所有结论带 Provenance / Derivation，缺一项 report.validate() 报错（5条硬要求）
# ============================================================

import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from siju_decision import (
    DecisionReport, LocationAnalysis, UserProfile, LocalTaste,
    CompetitionAnalysis, Competitor, PolicyAnalysis, ScheduleAnalysis,
    Provenance, Derivation, DataSourceType, ReportStore,
)
from siju_knowledge import match_policy, match_custom
from siju_etl import run_etl

store = ReportStore()

app = FastAPI(title="龍魂四绝·开店决策API", version="2.1")


class AnalyzeReq(BaseModel):
    address: str
    category: str = "奶茶店"
    user_types: List[str] = []
    user_crowds: List[str] = []
    user_funds: List[str] = []
    radius: int = 3000


@app.post("/api/siju/analyze")
async def analyze(req: AnalyzeReq):
    dna = DecisionReport.make_dna("9622", req.category)
    now = datetime.now()

    # ---- 1. 真实数据 ETL（高德）----
    etl = run_etl(req.address, req.category, dna, city="", radius=req.radius)

    # ---- 2. 政策 / 风俗 匹配（LIB级，带引用依据）----
    pols = match_policy(req.user_types, req.user_crowds, req.user_funds)
    cus = match_custom(req.address)

    policy_models = []
    for p in pols:
        policy_models.append(PolicyAnalysis(
            policy_name=p["name"], policy_no=p["ref"][:20],
            issue_date="公开政策", applicable_scope=p["scope"],
            key_clauses=[p["item"]], impact_assessment=p["dept"],
            provenance=Provenance(
                source_type=DataSourceType.LONGHUN_LIB,
                source_url="龍魂政策库POLICY_LIB", fetch_time=now,
                reliability="medium", update_frequency="季度", dna_trace=dna,
                notes="LIB级·以官方最新发布为准", ref_policy=p["ref"]),
        ))

    sched_models = [ScheduleAnalysis(
        group_type=cus["name"], wake_time="—", work_start="—",
        lunch_duration=60, work_end="—", dinner_time="—", sleep_time="—",
        weekend_diff=cus["rest"], holiday_diff=cus["custom"],
        provenance=Provenance(
            source_type=DataSourceType.LONGHUN_LIB,
            source_url="龍魂风俗库CUSTOM_LIB", fetch_time=now,
            reliability="medium", update_frequency="季度", dna_trace=dna,
            notes=cus["taste"], ref_custom=cus["ref"]),
    )]

    # ---- 3. 四绝数据（真实/降级统一建模）----
    if etl["mode"] == "REAL":
        prov = Provenance(
            source_type=DataSourceType.PUBLIC_MAP,
            source_url="https://restapi.amap.com/v3/place/around",
            fetch_time=now, reliability="high", update_frequency="实时",
            dna_trace=dna, notes=etl["note"])
        comps = [Competitor(name=c["name"], distance=c["distance"],
                            avg_price=0.0, differentiation="—",
                            registry_ref="", review_ref="")
                 for c in etl["competitors"]]
        jinghe = CompetitionAnalysis(
            competitors=comps,
            provenance=prov,
            derivation_chain=[Derivation(
                raw_data=f"高德周边POI {len(comps)}家",
                formula="竞品数=高德周边搜索返回count",
                assumption=["高德数据完整"], confidence=0.7,
                limitation="未含未上图小店，可能低估")])
        dimai = LocationAnalysis(
            target_address=req.address,
            coordinates=(etl["location"]["lng"], etl["location"]["lat"]),
            district=etl["location"]["district"], street="—",
            provenance=prov,
            derivation_chain=[Derivation(
                raw_data=etl["location"], formula="坐标=高德地理编码",
                assumption=[], confidence=0.9, limitation="—")])
    else:
        # 降级：诚实标 INFERENCE
        prov = Provenance(
            source_type=DataSourceType.INFERENCE,
            source_url="本地推演·高德不可用", fetch_time=now,
            reliability="low", update_frequency="实时", dna_trace=dna,
            notes=etl["note"])
        jinghe = CompetitionAnalysis(
            competitors=[], provenance=prov,
            derivation_chain=[Derivation(
                raw_data="无", formula="占位", assumption=["高德不可用"],
                confidence=0.2, limitation=etl["note"])])
        dimai = LocationAnalysis(
            target_address=req.address, coordinates=(0, 0), district="—",
            street="—", provenance=prov,
            derivation_chain=[Derivation(
                raw_data="无", formula="占位", assumption=["高德不可用"],
                confidence=0.2, limitation=etl["note"])])

    renliu = UserProfile(provenance=prov, derivation_chain=[Derivation(
        raw_data="无", formula="占位", assumption=["需实地/传感器"],
        confidence=0.2, limitation="人流须本地WiFi探针或高德人流API")])
    kouwei = LocalTaste(provenance=prov, derivation_chain=[Derivation(
        raw_data=cus["name"], formula="口味=地域库匹配",
        assumption=["地域库为常识示例"], confidence=0.4,
        limitation=cus["basis"])])

    # ---- 4. 综合决策（基于风险画像加权，非保赚承诺）----
    comp_count = len(jinghe.competitors)
    real_data = etl["mode"] == "REAL"
    recommended = []
    risks = []
    if not real_data:
        # 降级模式：无真实竞品数据，绝不乐观下结论（诚信原则）
        recommended.append({"rank": 1, "category": "先实地勘测再定品类",
                             "reason": "高德未接入真实数据·竞品数未知",
                             "advantage": "避坑优先", "launch": "蹲点3天记早晚高峰人流"})
        risks.append({"type": "data", "level": "high", "probability": 1.0,
                      "description": etl["note"], "response": "换高德Web服务key后重跑ETL",
                      "trigger": "拿到真实周边POI"})
    elif comp_count >= 5:
        recommended.append({"rank": 1, "category": f"社区{cus['name']}轻食/饮品差异化",
                             "reason": "原品类高饱和", "advantage": "错位竞争",
                             "launch": "先快闪测试"})
    else:
        recommended.append({"rank": 1, "category": req.category,
                             "reason": "周边竞品空间尚可", "advantage": "刚需",
                             "launch": "小步快跑"})

    # ---- 5. 组装报告并校验（5条硬要求）----
    report = DecisionReport(
        dna_trace=dna, applicant="战友", apply_time=now, generate_time=now,
        dimai=dimai, renliu=renliu, kouwei=kouwei, jinghe=jinghe,
        policy_analysis=policy_models, schedule_analysis=sched_models,
        recommended=recommended,
        risks=risks,
        data_sources=[prov],
        related_protocols=["data_sovereignty", "knowledge_contribution",
                           "free_speech", "ethics_audit", "clause_cultural_respect"],
    )
    report.validate()  # 缺一条即抛错，前端据此提示
    report.confirm_code = report.generate_confirm_code()

    out = report.to_json()
    out["etl_mode"] = etl["mode"]
    out["etl_note"] = etl["note"]
    store.save(out)  # 本地持久化（不上云·数据主权）
    return out


@app.get("/api/siju/report/{dna_trace}")
async def get_report(dna_trace: str):
    payload = store.load(dna_trace)
    if not payload:
        raise HTTPException(status_code=404, detail=f"未找到报告 {dna_trace}（可能未生成或已清理）")
    return payload


@app.post("/api/siju/confirm")
async def confirm(dna_trace: str, confirm_code: str):
    payload = store.confirm(dna_trace, confirm_code)
    if not payload:
        raise HTTPException(status_code=404, detail=f"未找到报告 {dna_trace}")
    return {"dna_trace": dna_trace, "confirmed": payload["confirm"]["confirmed"],
            "confirm_code": payload["confirm"]["code"],
            "confirm_time": payload["confirm"].get("confirm_time"),
            "note": "报告已确认封存·本地持久化"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8799)
