# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ============================================================
# 龍魂四绝 · 开店决策系统 v2.1 (真落地版)
# 文件：L5_服务层/services/siju_decision.py
# DNA追溯码：#龍芯⚡️丙午·辛未·四绝-KAIDIAN-DECISION-v2.1
# 君子协议：数据本地处理，不上传云端；决策权归用户
#
# 本模块把"5条硬要求"焊进类结构：
#   1. 来源标注  -> 每个字段经 Provenance(source_url/notes) 约束
#   2. 推演标注  -> 每个结论经 Derivation(formula/confidence) 约束
#   3. 备注规范  -> Provenance.notes 强制非空
#   4. 引用依据  -> Provenance.ref_policy / ref_custom 强制
#   5. 政府政策·风俗·作息·地域习俗分析 -> 独立模块，validate() 缺则报错
# ============================================================

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Literal, Any
from datetime import datetime
from enum import Enum
import hashlib
import re
import os
import json
import sqlite3
from pathlib import Path


# ============================================================
# P0 焊死底座：数据主权与追溯
# ============================================================

class DataSourceType(Enum):
    PUBLIC_MAP = "public_map"               # 高德/百度/腾讯地图API
    PUBLIC_REGISTRY = "public_registry"      # 国家企业信用信息公示系统
    PUBLIC_CENSUS = "public_census"          # 统计局年鉴/普查
    PUBLIC_POLICY = "public_policy"          # 政府公开政策文件
    USER_CONTRIBUTION = "user_contribution"  # 用户自愿贡献
    LOCAL_SENSOR = "local_sensor"            # 本地WiFi探针（匿名）
    HISTORICAL_CASE = "historical_case"      # 历史案例库
    LONGHUN_LIB = "longhun_lib"              # 龍魂内置示例库（政策/风俗）
    INFERENCE = "inference"                  # 纯推演（无真实数据）


@dataclass
class Provenance:
    """数据来源追溯 - P0焊死。每个字段必须有。"""
    source_type: DataSourceType
    source_url: str               # 来源标注（URL/文件路径/API名）
    fetch_time: datetime          # 抓取时间
    reliability: Literal["high", "medium", "low"]
    update_frequency: str
    dna_trace: str                # DNA追溯码
    notes: str = ""               # 备注规范（强制非空）
    ref_policy: str = ""          # 引用政策/法规依据
    ref_custom: str = ""          # 引用风俗/地域习俗依据

    def validate(self) -> bool:
        assert self.source_url, "❌ 来源URL不能为空（来源标注缺失）"
        assert self.notes, "❌ 备注不能为空（备注规范缺失）"
        assert self.dna_trace.startswith("#龍魂"), "❌ DNA格式错误"
        # 政策类必须带引用依据（第4条硬要求）
        if self.source_type in (DataSourceType.PUBLIC_POLICY, DataSourceType.LONGHUN_LIB):
            assert self.ref_policy or self.ref_custom, "❌ 政策/风俗类必须有引用依据(ref)"
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_type": self.source_type.value,
            "source_url": self.source_url,
            "fetch_time": self.fetch_time.isoformat(),
            "reliability": self.reliability,
            "update_frequency": self.update_frequency,
            "dna_trace": self.dna_trace,
            "notes": self.notes,
            "ref_policy": self.ref_policy,
            "ref_custom": self.ref_custom,
        }


@dataclass
class Derivation:
    """推演标注 - 每个结论必须有（第2条硬要求）。"""
    raw_data: Any                  # 原始数据
    formula: str                   # 计算公式/推演逻辑
    assumption: List[str]          # 前提假设
    confidence: float              # 置信度0-1
    limitation: str                # 局限性说明
    reviewer: str = "龍魂算法·三才权重模型"
    review_time: datetime = field(default_factory=datetime.now)

    def validate(self) -> bool:
        assert self.formula, "❌ 推演公式不能为空（推演标注缺失）"
        assert 0 <= self.confidence <= 1, "❌ 置信度必须在0-1之间"
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "raw_data": str(self.raw_data),
            "formula": self.formula,
            "assumption": self.assumption,
            "confidence": self.confidence,
            "limitation": self.limitation,
            "reviewer": self.reviewer,
            "review_time": self.review_time.isoformat(),
        }


# ============================================================
# 政府政策·风俗·作息·地域习俗分析（独立模块，不可跳过）
# ============================================================

@dataclass
class PolicyAnalysis:
    """政府扶持政策分析"""
    policy_name: str
    policy_no: str
    issue_date: str
    applicable_scope: str
    key_clauses: List[str]
    impact_assessment: str
    provenance: Provenance

    def to_dict(self) -> Dict[str, Any]:
        return {
            "policy_name": self.policy_name, "policy_no": self.policy_no,
            "issue_date": self.issue_date, "applicable_scope": self.applicable_scope,
            "key_clauses": self.key_clauses, "impact_assessment": self.impact_assessment,
            "provenance": self.provenance.to_dict(),
        }


@dataclass
class CustomAnalysis:
    """风俗/地域习俗分析"""
    custom_type: Literal["festival", "diet", "lifestyle", "taboo", "other"]
    custom_name: str
    region: str
    timing: str
    behavior_pattern: str
    business_impact: str
    risk_warning: str
    provenance: Provenance

    def to_dict(self) -> Dict[str, Any]:
        return {
            "custom_type": self.custom_type, "custom_name": self.custom_name,
            "region": self.region, "timing": self.timing,
            "behavior_pattern": self.behavior_pattern,
            "business_impact": self.business_impact,
            "risk_warning": self.risk_warning,
            "provenance": self.provenance.to_dict(),
        }


@dataclass
class ScheduleAnalysis:
    """作息分析"""
    group_type: str
    wake_time: str
    work_start: str
    lunch_duration: int
    work_end: str
    dinner_time: str
    sleep_time: str
    weekend_diff: str
    holiday_diff: str
    provenance: Provenance

    def to_dict(self) -> Dict[str, Any]:
        return {
            "group_type": self.group_type, "wake_time": self.wake_time,
            "work_start": self.work_start, "lunch_duration": self.lunch_duration,
            "work_end": self.work_end, "dinner_time": self.dinner_time,
            "sleep_time": self.sleep_time, "weekend_diff": self.weekend_diff,
            "holiday_diff": self.holiday_diff,
            "provenance": self.provenance.to_dict(),
        }


# ============================================================
# 一绝 · 地脉
# ============================================================

@dataclass
class LocationAnalysis:
    target_address: str
    coordinates: tuple[Any, ...]
    district: str
    street: str
    residential_pct: float = 0.0
    office_pct: float = 0.0
    industrial_pct: float = 0.0
    school_pct: float = 0.0
    hospital_pct: float = 0.0
    commercial_pct: float = 0.0
    other_pct: float = 0.0
    morning_rush: Dict[str, Any] = field(default_factory=dict)
    noon_rush: Dict[str, Any] = field(default_factory=dict)
    afternoon: Dict[str, Any] = field(default_factory=dict)
    evening_rush: Dict[str, Any] = field(default_factory=dict)
    night: Dict[str, Any] = field(default_factory=dict)
    late_night: Dict[str, Any] = field(default_factory=dict)
    bus_stops: List[Dict] = field(default_factory=list)
    metro_stations: List[Dict] = field(default_factory=list)
    parking: List[Dict] = field(default_factory=list)
    planned_changes: List[Dict] = field(default_factory=list)
    provenance: Optional[Provenance] = None
    derivation_chain: List[Derivation] = field(default_factory=list)

    def validate(self) -> bool:
        total = sum([self.residential_pct, self.office_pct, self.industrial_pct,
                     self.school_pct, self.hospital_pct, self.commercial_pct, self.other_pct])
        assert abs(total - 100) < 0.01, f"❌ 占比总和必须100，当前={total:.1f}"
        assert self.provenance is not None, "❌ 地脉必须有来源追溯"
        self.provenance.validate()
        return True


# ============================================================
# 二绝 · 人流
# ============================================================

@dataclass
class UserProfile:
    weekday_profiles: List[Dict] = field(default_factory=list)
    weekend_profiles: List[Dict] = field(default_factory=list)
    holiday_patterns: List[Dict] = field(default_factory=list)
    heatmap_data: Optional[Dict] = None
    provenance: Optional[Provenance] = None
    derivation_chain: List[Derivation] = field(default_factory=list)

    def validate(self) -> bool:
        assert self.provenance is not None
        self.provenance.validate()
        return True


# ============================================================
# 三绝 · 口味（含作息/地域习俗）
# ============================================================

@dataclass
class LocalTaste:
    spiciness: Literal["none", "mild", "medium", "hot"] = "mild"
    spiciness_pct: float = 0.0
    flavor_pref: Literal["light", "rich", "sweet_sour", "savory"] = "savory"
    flavor_pct: float = 0.0
    temperature_pref: Literal["hot", "room", "cold"] = "hot"
    temp_pct: float = 0.0
    format_pref: Literal["dine_in", "delivery", "takeout"] = "dine_in"
    format_pct: float = 0.0
    avg_check: tuple[Any, ...] = (0.0, 0.0)
    dining_freq: int = 0
    delivery_ratio: float = 0.0
    dine_style: Literal["fast", "casual", "formal"] = "fast"
    queue_tolerance: int = 0
    repurchase_rate: float = 0.0
    lifestyle: Dict[str, Any] = field(default_factory=dict)
    local_customs: List[CustomAnalysis] = field(default_factory=list)
    provenance: Optional[Provenance] = None
    derivation_chain: List[Derivation] = field(default_factory=list)

    def validate(self) -> bool:
        assert self.provenance is not None
        self.provenance.validate()
        return True


# ============================================================
# 四绝 · 竞合
# ============================================================

@dataclass
class Competitor:
    name: str
    distance: int
    status: Literal["good", "average", "poor"] = "average"
    avg_price: float = 0.0
    saturation: Literal["saturated", "space"] = "space"
    differentiation: str = ""
    registry_ref: str = ""
    review_ref: str = ""


@dataclass
class CompetitionAnalysis:
    competitors: List[Competitor] = field(default_factory=list)
    top3_analysis: List[Dict] = field(default_factory=list)
    opportunity_matrix: List[Dict] = field(default_factory=list)
    provenance: Optional[Provenance] = None
    derivation_chain: List[Derivation] = field(default_factory=list)

    def validate(self) -> bool:
        assert self.provenance is not None
        self.provenance.validate()
        return True


# ============================================================
# 综合决策报告
# ============================================================

@dataclass
class DecisionReport:
    dna_trace: str
    applicant: str
    apply_time: datetime
    generate_time: datetime
    version: str = "2.1"
    audit_status: Literal["auto", "manual", "rejected"] = "auto"

    dimai: Optional[LocationAnalysis] = None
    renliu: Optional[UserProfile] = None
    kouwei: Optional[LocalTaste] = None
    jinghe: Optional[CompetitionAnalysis] = None

    policy_analysis: List[PolicyAnalysis] = field(default_factory=list)
    schedule_analysis: List[ScheduleAnalysis] = field(default_factory=list)

    not_recommended: List[Dict] = field(default_factory=list)
    cautious: List[Dict] = field(default_factory=list)
    recommended: List[Dict] = field(default_factory=list)
    innovative: List[Dict] = field(default_factory=list)

    risks: List[Dict] = field(default_factory=list)
    startup_cost: Dict[str, Any] = field(default_factory=dict)
    monthly_cost: Dict[str, Any] = field(default_factory=dict)
    break_even: Dict[str, Any] = field(default_factory=dict)
    sensitivity: List[Dict] = field(default_factory=list)

    action_items: List[Dict] = field(default_factory=list)
    system_log: List[Dict] = field(default_factory=list)
    related_protocols: List[str] = field(default_factory=list)
    data_sources: List[Provenance] = field(default_factory=list)

    confirmed: bool = False
    confirmed_by: Optional[str] = None
    confirm_time: Optional[datetime] = None
    confirm_code: Optional[str] = None

    @staticmethod
    def make_dna(uid: str, apply_type: str = "开店") -> str:
        base = f"{uid}{apply_type}{datetime.now().isoformat()}"
        h = hashlib.sha256(base.encode()).hexdigest()[:8]
        return f"#龍魂⚡️{datetime.now().strftime('%Y%m%d')}-{apply_type}-{h}"

    def generate_confirm_code(self) -> str:
        base = f"{self.dna_trace}{self.applicant}{datetime.now().isoformat()}"
        return f"#CONFIRM🌌{hashlib.sha256(base.encode()).hexdigest()[:8]}-ONLY-ONCE🧬"

    def validate(self) -> bool:
        """完整校验 - 5条硬要求缺一项即报错"""
        assert self.dna_trace, "❌ DNA追溯码缺失"
        # 第1/3条：来源标注 + 备注规范
        assert self.data_sources, "❌ 缺少数据来源（来源标注）"
        for p in self.data_sources:
            p.validate()
        # 第2条：推演标注
        chains = (self.dimai.derivation_chain if self.dimai else []) + \
                 (self.renliu.derivation_chain if self.renliu else []) + \
                 (self.kouwei.derivation_chain if self.kouwei else []) + \
                 (self.jinghe.derivation_chain if self.jinghe else [])
        assert chains, "❌ 缺少推演标注（derivation_chain 为空）"
        for d in chains:
            d.validate()
        # 第4条：引用依据（政策分析必须带 ref）
        assert self.policy_analysis, "❌ 政策分析缺失"
        for pa in self.policy_analysis:
            assert pa.provenance.ref_policy or pa.provenance.ref_custom, \
                f"❌ 政策『{pa.policy_name}』缺引用依据"
        # 第5条：政府政策·风俗·作息·地域习俗分析 不可跳过
        assert self.schedule_analysis, "❌ 作息分析缺失（第5条硬要求）"
        return True

    def to_json(self) -> Dict[str, Any]:
        return {
            "meta": {"dna_trace": self.dna_trace, "applicant": self.applicant,
                     "version": self.version, "audit_status": self.audit_status},
            "data_sources": [p.to_dict() for p in self.data_sources],
            "policy_analysis": [p.to_dict() for p in self.policy_analysis],
            "schedule_analysis": [s.to_dict() for s in self.schedule_analysis],
            "decision": {"not_recommended": self.not_recommended,
                         "cautious": self.cautious, "recommended": self.recommended,
                         "innovative": self.innovative},
            "risks": self.risks, "cost": self.startup_cost,
            "actions": self.action_items,
            "confirm": {"confirmed": self.confirmed, "code": self.confirm_code},
        }

    # to_html 由 L5 现有 kaidian/index.html 前端渲染；后端仅提供 JSON 桥接。
    # 若需服务端渲染，可在 templates/siju_report.html 实现，此处返回提示。


# ============================================================
# 报告持久化（SQLite·本地·不上云·数据主权）
# ============================================================

REPORT_DB = Path(__file__).resolve().parent / "data" / "siju_reports.db"


class ReportStore:
    """决策报告本地持久层。按 DNA 追溯码存取，确认即封存。"""

    def __init__(self, db: Path = REPORT_DB):
        self.db = db
        os.makedirs(self.db.parent, exist_ok=True)
        conn = sqlite3.connect(self.db)
        conn.execute('''CREATE TABLE IF NOT EXISTS reports (
            dna TEXT PRIMARY KEY,
            payload TEXT,
            confirmed INTEGER DEFAULT 0,
            confirm_code TEXT,
            confirm_time TEXT,
            created TEXT)''')
        conn.commit()
        conn.close()

    def save(self, report_json: Dict[str, Any]) -> None:
        dna = report_json["meta"]["dna_trace"]
        conn = sqlite3.connect(self.db)
        conn.execute(
            'INSERT OR REPLACE INTO reports (dna, payload, created) VALUES (?,?,?)',
            (dna, json.dumps(report_json, ensure_ascii=False), datetime.now().isoformat()))
        conn.commit()
        conn.close()

    def load(self, dna: str) -> Optional[Dict]:
        conn = sqlite3.connect(self.db)
        row = conn.execute(
            'SELECT payload, confirmed, confirm_code, confirm_time FROM reports WHERE dna=?',
            (dna,)).fetchone()
        conn.close()
        if not row:
            return None
        payload = json.loads(row[0])
        payload.setdefault("confirm", {})["confirmed"] = bool(row[1])
        if row[2]:
            payload["confirm"]["code"] = row[2]
        if row[3]:
            payload["confirm"]["confirm_time"] = row[3]
        return payload

    def confirm(self, dna: str, confirm_code: str) -> Optional[Dict]:
        conn = sqlite3.connect(self.db)
        row = conn.execute('SELECT 1 FROM reports WHERE dna=?', (dna,)).fetchone()
        if not row:
            conn.close()
            return None
        conn.execute(
            'UPDATE reports SET confirmed=1, confirm_code=?, confirm_time=? WHERE dna=?',
            (confirm_code, datetime.now().isoformat(), dna))
        conn.commit()
        conn.close()
        return self.load(dna)


# ============================================================
# 通用民生模板基类（按 Kimi 意向焊死，便于扩展维权/医疗等）
# ============================================================

class LonghunMinshengTemplate:
    """所有民生场景继承：开店/维权/医疗/教育/就业/养老"""
    SERVICE_TARGET = "老百姓"
    LEGAL_FRAMEWORK = "中国法律"
    DATA_SOVEREIGNTY = "用户本地存储，不上传"
    ANTI_EXPLOITATION = "不为资本服务"
    CREATOR_RIGHT = "UID9622不可剥夺"

    def build_report(self, *args, **kwargs) -> DecisionReport:
        raise NotImplementedError("子类必须实现 build_report")


if __name__ == "__main__":
    # 自检：构造一个最小合法报告，验证5条硬要求校验器
    dna = DecisionReport.make_dna("9622")
    prov = Provenance(
        source_type=DataSourceType.INFERENCE,
        source_url="本地推演·无真实数据源",
        fetch_time=datetime.now(),
        reliability="low",
        update_frequency="实时",
        dna_trace=dna,
        notes="纯推演，非真实数据，须实地验证",
    )
    der = Derivation(raw_data="无", formula="占位推演", assumption=["无真实数据"],
                     confidence=0.3, limitation="未接入地图/人口API")
    rep = DecisionReport(
        dna_trace=dna, applicant="测试", apply_time=datetime.now(),
        generate_time=datetime.now(),
        dimai=LocationAnalysis(target_address="测试", coordinates=(0, 0), district="x", street="y",
                               provenance=prov, derivation_chain=[der]),
        renliu=UserProfile(provenance=prov, derivation_chain=[der]),
        kouwei=LocalTaste(provenance=prov, derivation_chain=[der]),
        jinghe=CompetitionAnalysis(provenance=prov, derivation_chain=[der]),
        policy_analysis=[PolicyAnalysis(
            policy_name="小微企业减税", policy_no="财税〔2019〕13号",
            issue_date="2019", applicable_scope="小微企业",
            key_clauses=["年应纳税所得额≤300万部分减按25%计入"],
            impact_assessment="降低初期税负",
            provenance=Provenance(source_type=DataSourceType.LONGHUN_LIB,
                                   source_url="龍魂政策库POLICY_LIB", fetch_time=datetime.now(),
                                   reliability="medium", update_frequency="季度", dna_trace=dna,
                                   notes="以官方最新发布为准", ref_policy="财税〔2019〕13号"))],
        schedule_analysis=[ScheduleAnalysis(
            group_type="白领", wake_time="7:30", work_start="9:00", lunch_duration=60,
            work_end="18:00", dinner_time="18:30", sleep_time="23:00",
            weekend_diff="睡懒觉", holiday_diff="返乡",
            provenance=Provenance(source_type=DataSourceType.LONGHUN_LIB,
                                   source_url="龍魂风俗库CUSTOM_LIB", fetch_time=datetime.now(),
                                   reliability="medium", update_frequency="季度", dna_trace=dna,
                                   notes="通用作息，以实地为准", ref_custom="clause_cultural_respect"))],
        data_sources=[prov],
    )
    rep.validate()
    print("✅ 5条硬要求校验通过 | DNA:", dna)
    print("✅ confirm_code:", rep.generate_confirm_code())
