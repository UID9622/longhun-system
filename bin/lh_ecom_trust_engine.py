#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙未·丙申·申时·☱兑-ECOM-TRUST-ENGINE-V1.0.1-P0-1002819c
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
龍魂·电商信任重建数学建模引擎 v1.0.1
=====================================
E-Commerce Trust Rebuild Mathematical Model Engine

五模块：
  Module A — 信誉分引擎 (Reputation Score S ∈ [0,1000])
  Module B — 举报分级与反坐 (Report Classification & Counter-Report)
  Module C — 阶梯赔偿与悬赏 (Tiered Compensation & Bounty)
  Module D — 视频真实度核验 (Video Authenticity R ∈ [0,1])
  Module E — 信任摩擦系数 (Trust Friction τ)

锚定协议: 01_protocols/LH-ECOM-TRUST-REBUILD-v1.0.md
法条锚: 《消法》24/25/55条 · 《食安法》148条 · 《电子商务法》17/39条
测试向量: 12条 (第九章) · 全绿才算数
"""

import math
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional, Union
from dataclasses import dataclass, field
from enum import Enum


# ══════════════════════════════════════════════════════════════════
# 常量定义
# ══════════════════════════════════════════════════════════════════

# 承诺档 → 信誉加权系数 κ
COMMIT_TIER_KAPPA = {"G1": 1.0, "G2": 1.05, "G3": 1.1, "G4": 1.2}

# 承诺档 → 法定保证金等级
COMMIT_TIER_DEPOSIT = {"G1": "基础", "G2": "上浮", "G3": "上浮", "G4": "上浮"}

# 严重度权重 w
SEVERITY_WEIGHT = {"轻": 1, "中": 2, "重": 3}

# 赔偿档位 → (法定下限函数, 倍数, 法条引用)
COMPENSATION_TABLE = {
    "L1": {"min_func": lambda price: 0,          "multiplier": 0,  "law": "消法24条",  "desc": "退货退款+运费商家担"},
    "L2": {"min_func": lambda price: 500,         "multiplier": 3,  "law": "消法55条",  "desc": "退一赔三·不足500按500"},
    "L3": {"min_func": lambda price: 500,         "multiplier": 3,  "law": "消法55条+承诺", "desc": "退一赔三起步·可至5倍"},
    "L4": {"min_func": lambda price: 1000,        "multiplier": 10, "law": "食安法148条", "desc": "价款十倍·不足1000按1000"},
}

# 视频真实度权重
VIDEO_AUTH_WEIGHTS = {
    "filter":  0.25,  # 滤镜/美化检测
    "ai":      0.25,  # AI生成痕迹
    "staging": 0.20,  # 摆拍一致性
    "repro":   0.20,  # 参数可复测性
    "history": 0.10,  # 历史造假记录
}

# 半衰恢复参数
HALF_LIFE_DAYS = 180        # 180天
HALF_LIFE_RECOVERY = 0.50   # 恢复50%

# 悬赏参数
BOUNTY_RATIO = 0.10          # 赔偿金10%
BOUNTY_CAP = 5000            # 单笔上限5000元

# 信任摩擦目标阈值
TAU_TARGET = 0.005           # 目标 τ < 0.5%
TAU_WINDOW_DAYS = 90         # 滚动90天

# 信誉分边界
S_MIN, S_MAX, S_INIT = 0, 1000, 500


# ══════════════════════════════════════════════════════════════════
# 数据类型
# ══════════════════════════════════════════════════════════════════

class AuditMark(Enum):
    GREEN  = "🟢"
    YELLOW = "🟡"
    RED    = "🔴"

class ReportType(Enum):
    FUZZY     = "⚪ 模糊举报"
    EMPIRICAL = "🟡 实证候选"
    MALICIOUS = "🔴 恶意举报"

class VideoGrade(Enum):
    NORMAL    = "🟢 正常展示"
    WARNING   = "🟡 强制标注美化处理中"
    BANNED    = "🔴 下架整改+扣分"

class TrustLevel(Enum):
    GOOD   = "🟢"
    WARN   = "🟡"
    DANGER = "🔴"


@dataclass
class ScoreEvent:
    """信誉分事件"""
    event_type: str          # 事件类型
    delta: float             # 分数变化
    weight: float = 0        # 严重度权重（实证举报用）
    date: Optional[str] = None  # 发生日期 ISO格式
    desc: str = ""           # 描述

    def __post_init__(self):
        if self.date is None:
            self.date = datetime.now().strftime("%Y-%m-%d")


@dataclass
class DeductionRecord:
    """减分记录（用于半衰恢复）"""
    score: float             # 扣分值
    date: str                # 日期
    reason: str              # 原因
    recovered: bool = False  # 是否已恢复


@dataclass
class ReportResult:
    """举报处理结果"""
    report_type: ReportType
    audit: AuditMark
    score_delta: float
    feedback_pool: bool      # 是否进反馈池
    counter_report: bool     # 是否触发反坐
    details: str


@dataclass
class CompensationResult:
    """赔偿计算结果"""
    tier: str
    refund: float
    compensation: float
    total: float
    law: str
    disposition: str


@dataclass
class MerchantState:
    """商家状态"""
    merchant_id: str
    score: float = S_INIT
    commit_tier: str = "G1"
    score_events: List[ScoreEvent] = field(default_factory=list)
    deduction_records: List[DeductionRecord] = field(default_factory=list)
    empirical_reports: int = 0
    fuzzy_feedbacks: int = 0
    transactions_90d: int = 0
    disputes_90d: int = 0
    video_auth_score: float = 1.0
    audit_log: List[Tuple[str, str, str]] = field(default_factory=list)


# ══════════════════════════════════════════════════════════════════
# Module A: 信誉分引擎
# ══════════════════════════════════════════════════════════════════

def clamp(val: float, lo: float = 0.0, hi: float = 1000.0) -> float:
    """三才钳位：天/地/人边界"""
    return max(lo, min(hi, val))


def get_kappa(tier: str) -> float:
    """获取承诺加权系数"""
    return COMMIT_TIER_KAPPA.get(tier, 1.0)


def compute_score_delta(event_type: str, kappa: float = 1.0,
                        severity: str = "中") -> Tuple[float, str]:
    """
    计算单次增/减分 Δ

    返回: (delta, 说明)
    """
    if event_type == "如实描述抽检":
        d = 2 * kappa
        return d, f"如实描述抽检通过 +{d} (κ={kappa})"
    elif event_type == "主动赔付履约":
        d = 5 * kappa
        return d, f"主动赔付履约 +{d} (κ={kappa})"
    elif event_type == "连续30天零实证":
        d = 10 * kappa
        return d, f"连续30天零实证 +{d} (κ={kappa})"
    elif event_type == "承诺分级升档":
        d = 20 * kappa
        return d, f"承诺升档 +{d} (κ={kappa})"
    elif event_type == "实证举报":
        w = SEVERITY_WEIGHT.get(severity, 2)
        d = -20 * w
        return d, f"实证举报成立(严重度{severity},w={w}) {d}"
    elif event_type == "造假实锤":
        return -50, "视频/参数造假实锤 -50"
    elif event_type == "恶意举报反坐":
        return -30, "恶意举报反坐 -30"
    elif event_type == "模糊举报":
        return 0, "模糊举报→反馈池,不计分"
    elif event_type == "承诺升档":
        return 20, f"承诺升档 +20 (κ={kappa})"
    else:
        return 0, f"未知事件类型: {event_type}"


def apply_events(state: MerchantState,
                 events: List[Tuple[str, Optional[str]]]) -> MerchantState:
    """
    批量应用事件到商家状态
    事件格式: [(事件类型, 严重度或None), ...]
    返回更新后的状态
    """
    kappa = get_kappa(state.commit_tier)

    for evt_type, severity in events:
        d, desc = compute_score_delta(evt_type, kappa, severity or "中")
        new_score = clamp(state.score + d)

        se = ScoreEvent(
            event_type=evt_type,
            delta=d,
            weight=SEVERITY_WEIGHT.get(severity or "中", 0),
            desc=desc
        )
        state.score_events.append(se)

        # 记录减分事件（用于半衰恢复）
        if d < 0:
            state.deduction_records.append(DeductionRecord(
                score=abs(d), date=se.date, reason=evt_type
            ))

        # 计数器
        if evt_type == "实证举报":
            state.empirical_reports += 1
        elif evt_type == "模糊举报":
            state.fuzzy_feedbacks += 1

        state.score = round(new_score, 2)

    return state


# ══════════════════════════════════════════════════════════════════
# Module B: 举报分级与反坐
# ══════════════════════════════════════════════════════════════════

def classify_report(has_evidence: bool, has_order: bool, has_claim: bool,
                    device_cluster: bool = False,
                    evidence_faked: bool = False,
                    competitor_relation: bool = False) -> ReportResult:
    """
    举报分级（§4.2 判定流程）

    收单三要素: 证据附件 ∧ 订单号 ∧ 具体诉求
    恶意特征: 设备簇批量 ∨ 证据伪造 ∨ 竞争关系
    """
    # 恶意举报优先判定
    malicious_flags = sum([device_cluster, evidence_faked, competitor_relation])
    if malicious_flags >= 1:
        return ReportResult(
            report_type=ReportType.MALICIOUS,
            audit=AuditMark.RED,
            score_delta=-30,
            feedback_pool=False,
            counter_report=True,
            details=f"🔴 恶意举报→七因子核查+反坐-30+熔断 "
                    f"(设备簇={device_cluster}, 证据伪造={evidence_faked}, "
                    f"竞争关系={competitor_relation})"
        )

    # 实证判定
    if has_evidence and has_order and has_claim:
        return ReportResult(
            report_type=ReportType.EMPIRICAL,
            audit=AuditMark.YELLOW,
            score_delta=-20,  # 基准扣分（实际由严重度w决定）
            feedback_pool=False,
            counter_report=False,
            details="🟡 实证候选→立案核验(7天)·证据链完整"
        )

    # 模糊举报
    missing = []
    if not has_evidence: missing.append("证据附件")
    if not has_order: missing.append("订单号")
    if not has_claim: missing.append("具体诉求")
    return ReportResult(
        report_type=ReportType.FUZZY,
        audit=AuditMark.GREEN,
        score_delta=0,
        feedback_pool=True,
        counter_report=False,
        details=f"⚪ 模糊举报→反馈池,不计分不公示 (缺: {', '.join(missing)})"
    )


# ══════════════════════════════════════════════════════════════════
# Module C: 阶梯赔偿与悬赏
# ══════════════════════════════════════════════════════════════════

def compute_compensation(tier: str, price: float,
                         commit_multiplier: Optional[int] = None) -> CompensationResult:
    """
    阶梯赔偿计算（§4.3）
    赔偿 = max(法定下限, 价款 × 倍数 × 承诺系数)

    参数:
        tier: "L1"|"L2"|"L3"|"L4"
        price: 商品价款（元）
        commit_multiplier: 商家承诺倍数（L3用，可选）

    返回: CompensationResult
    """
    if tier not in COMPENSATION_TABLE:
        raise ValueError(f"未知赔偿档位: {tier}，应为 L1|L2|L3|L4")

    info = COMPENSATION_TABLE[tier]
    min_limit = info["min_func"](price)
    multiplier = info["multiplier"]

    # L1: 仅退款，无赔偿
    if tier == "L1":
        compensation = 0
    elif tier == "L3" and commit_multiplier:
        # L3: 取商家承诺倍数和法定3倍的最大值
        multiplier = max(info["multiplier"], commit_multiplier)
        compensation = max(min_limit, price * multiplier)
    else:
        compensation = max(min_limit, price * multiplier)

    total = price + compensation  # 退款 + 赔偿

    return CompensationResult(
        tier=tier,
        refund=price,
        compensation=compensation,
        total=total,
        law=info["law"],
        disposition=info["desc"]
    )


def compute_bounty(compensation: float, ratio: float = BOUNTY_RATIO,
                   cap: float = BOUNTY_CAP) -> float:
    """
    找茬悬赏计算（§4.4）
    悬赏 = min(上限, 赔偿金 × 比例)
    """
    return min(cap, round(compensation * ratio, 2))


# ══════════════════════════════════════════════════════════════════
# Module D: 视频真实度核验
# ══════════════════════════════════════════════════════════════════

def compute_video_authenticity(r_filter: float, r_ai: float,
                               r_staging: float, r_repro: float,
                               r_history: float) -> Tuple[float, str, AuditMark]:
    """
    视频真实度核验（§4.5）
    R = Σ w_i · r_i ∈ [0, 1]

    参数: 各项评分 ∈ [0,1]
    返回: (R值, 档位描述, 审计标记)
    """
    weights = VIDEO_AUTH_WEIGHTS
    R = (weights["filter"]  * r_filter +
         weights["ai"]      * r_ai +
         weights["staging"] * r_staging +
         weights["repro"]   * r_repro +
         weights["history"] * r_history)

    R = round(R, 3)

    if R >= 0.85:
        return R, VideoGrade.NORMAL.value, AuditMark.GREEN
    elif R >= 0.60:
        return R, VideoGrade.WARNING.value, AuditMark.YELLOW
    else:
        return R, VideoGrade.BANNED.value, AuditMark.RED


# ══════════════════════════════════════════════════════════════════
# Module E: 信任摩擦系数 & 半衰恢复
# ══════════════════════════════════════════════════════════════════

def compute_tau(disputes: int, transactions: int) -> Tuple[float, str, AuditMark]:
    """
    信任摩擦系数（§4.6）
    τ = 纠纷单数 / 成交单数（滚动90天）

    返回: (τ值, 描述, 审计标记)
    """
    if transactions == 0:
        return 0.0, "无成交数据", AuditMark.YELLOW

    tau = disputes / transactions

    if tau < TAU_TARGET:
        return tau, f"τ={tau:.4f} (<{TAU_TARGET}) 🟢 正常", AuditMark.GREEN
    elif tau < TAU_TARGET * 2:
        return tau, f"τ={tau:.4f} 🟡 接近阈值·关注", AuditMark.YELLOW
    else:
        return tau, f"τ={tau:.4f} 🔴 超阈值·触发审计", AuditMark.RED


def compute_half_life_recovery(state: MerchantState,
                               today: Optional[str] = None) -> Tuple[float, float]:
    """
    半衰恢复（§4.1d）
    减分满180天且无再犯 → 恢复50%

    无再犯判定：该笔扣分之后 180 天内无新增扣分记录。

    返回: (新分数, 回填分数)
    """
    if today is None:
        today = datetime.now().strftime("%Y-%m-%d")

    today_dt = datetime.strptime(today, "%Y-%m-%d")
    recovery = 0.0

    # 按日期排序，便于判断"再犯"
    sorted_records = sorted(state.deduction_records, key=lambda r: r.date)

    for i, rec in enumerate(sorted_records):
        if rec.recovered:
            continue

        rec_dt = datetime.strptime(rec.date, "%Y-%m-%d")
        days_passed = (today_dt - rec_dt).days
        if days_passed < HALF_LIFE_DAYS:
            continue

        # 检查再犯：该笔扣分之后 180 天内是否有其他扣分
        reoffended = False
        window_end = rec_dt + timedelta(days=HALF_LIFE_DAYS)
        for other in sorted_records:
            if other is rec:
                continue
            other_dt = datetime.strptime(other.date, "%Y-%m-%d")
            if rec_dt < other_dt <= window_end:
                reoffended = True
                break

        if not reoffended:
            rec.recovered = True
            recovery += rec.score * HALF_LIFE_RECOVERY

    new_score = clamp(state.score + recovery)
    state.score = round(new_score, 2)
    return round(new_score, 2), round(recovery, 2)


# ══════════════════════════════════════════════════════════════════
# 综合评估
# ══════════════════════════════════════════════════════════════════

def overall_assessment(state: MerchantState) -> Dict:
    """
    商家综合健康度评估
    返回多维度评语
    """
    assessments = {}

    # 信誉分健康度
    if state.score >= 700:
        assessments["信誉分"] = (AuditMark.GREEN, f"S={state.score} · 优秀")
    elif state.score >= 400:
        assessments["信誉分"] = (AuditMark.YELLOW, f"S={state.score} · 一般")
    else:
        assessments["信誉分"] = (AuditMark.RED, f"S={state.score} · 危险")

    # 实证举报比
    if state.transactions_90d > 0:
        report_ratio = state.empirical_reports / state.transactions_90d
        if report_ratio < 0.01:
            assessments["举报率"] = (AuditMark.GREEN, f"实证率{report_ratio:.3f} · 低")
        elif report_ratio < 0.05:
            assessments["举报率"] = (AuditMark.YELLOW, f"实证率{report_ratio:.3f} · 中")
        else:
            assessments["举报率"] = (AuditMark.RED, f"实证率{report_ratio:.3f} · 高")

    # 视频真实度
    if state.video_auth_score >= 0.85:
        assessments["视频"] = (AuditMark.GREEN, f"R={state.video_auth_score}")
    elif state.video_auth_score >= 0.60:
        assessments["视频"] = (AuditMark.YELLOW, f"R={state.video_auth_score}")
    else:
        assessments["视频"] = (AuditMark.RED, f"R={state.video_auth_score}")

    # 承诺档
    assessments["承诺"] = (AuditMark.GREEN,
                           f"{state.commit_tier}档 (κ={get_kappa(state.commit_tier)})")

    return assessments


# ══════════════════════════════════════════════════════════════════
# 12条测试向量（第九章）
# ══════════════════════════════════════════════════════════════════

def run_all_tests() -> Dict[str, Tuple[bool, str]]:
    """执行全部12条测试向量，返回逐条结果"""
    results = {}

    # ── T01: 初始商家 S=500 ──
    m = MerchantState(merchant_id="T01")
    results["T01"] = (m.score == 500, f"S={m.score} (期望500)")

    # ── T02: 实证举报成立(w=2) S−40 ──
    m = MerchantState(merchant_id="T02")
    apply_events(m, [("实证举报", "中")])
    results["T02"] = (m.score == 460, f"S={m.score} (期望460, Δ=-40)")

    # ── T03: 模糊举报10条 S不变 ──
    m = MerchantState(merchant_id="T03")
    for _ in range(10):
        apply_events(m, [("模糊举报", None)])
    results["T03"] = (m.score == 500 and m.fuzzy_feedbacks == 10,
                      f"S={m.score}, 反馈池={m.fuzzy_feedbacks} (期望S=500, 反馈+10)")

    # ── T04: G3档如实描述抽检 +2×1.1=+2.2 ──
    m = MerchantState(merchant_id="T04", commit_tier="G3")
    apply_events(m, [("如实描述抽检", None)])
    results["T04"] = (m.score == 502.2,
                      f"S={m.score} (期望502.2, Δ=+2×1.1=+2.2)")

    # ── T05: 减分满180天无再犯 恢复50% ──
    m = MerchantState(merchant_id="T05")
    apply_events(m, [("实证举报", "中")])  # -40, S=460
    # 手动把减分日期设为181天前
    old_date = (datetime.now() - timedelta(days=181)).strftime("%Y-%m-%d")
    m.deduction_records[0].date = old_date
    new_s, recovered = compute_half_life_recovery(m)
    expected = 460 + 20  # 40*0.5 = 20
    results["T05"] = (abs(new_s - expected) < 0.01 and abs(m.score - expected) < 0.01,
                      f"S={new_s}(state={m.score}), 回填={recovered} (期望S={expected}, 回填20)")

    # ── T06: 价款200元 L2欺诈 赔600+退200 ──
    c = compute_compensation("L2", 200)
    ok = (c.refund == 200 and c.compensation == 600 and c.total == 800)
    results["T06"] = (ok,
                      f"退款{c.refund}+赔偿{c.compensation}=总{c.total} "
                      f"(期望退200+赔600=800, min(500,200×3)=600)")

    # ── T07: 价款50元 L4食品 赔1000 ──
    c = compute_compensation("L4", 50)
    ok = (c.refund == 50 and c.compensation == 1000 and c.total == 1050)
    results["T07"] = (ok,
                      f"退款{c.refund}+赔偿{c.compensation}=总{c.total} "
                      f"(期望退50+赔1000=1050, min(1000,50×10)→1000)")

    # ── T08: 首个实证举报者 赔偿金600 悬赏60 ──
    bounty = compute_bounty(600)
    results["T08"] = (bounty == 60, f"悬赏={bounty}元 (期望600×10%=60)")

    # ── T09: 视频R=0.5 🔴下架 ──
    R, grade, mark = compute_video_authenticity(0.5, 0.5, 0.5, 0.5, 0.5)
    results["T09"] = (R == 0.5 and mark == AuditMark.RED,
                      f"R={R} → {grade} (期望R=0.5, 🔴下架)")

    # ── T10: 同设备簇批量举报 触发反坐 ──
    r = classify_report(has_evidence=True, has_order=True, has_claim=True,
                        device_cluster=True)
    results["T10"] = (r.report_type == ReportType.MALICIOUS and r.counter_report,
                      f"{r.details} (期望🔴恶意举报+反坐-30)")

    # ── T11: τ=0.3% 🟢正常 ──
    tau, desc, mark = compute_tau(3, 1000)
    results["T11"] = (tau == 0.003 and mark == AuditMark.GREEN,
                      f"{desc} (期望τ=0.003, 🟢正常)")

    # ── T12: G4档商家违约 按L3处置 ──
    c = compute_compensation("L3", 300, commit_multiplier=5)
    ok = (c.tier == "L3" and c.compensation >= 900)  # 300*3=900, 5倍=1500
    results["T12"] = (ok,
                      f"{c.tier}档: 退款{c.refund}+赔偿{c.compensation}=总{c.total} "
                      f"(期望L3处置·G4违约=承诺造假)")

    return results


def print_test_report(results: Dict[str, Tuple[bool, str]]) -> Tuple[int, int]:
    """打印测试报告，返回(通过数, 总数)"""
    print("\n" + "=" * 68)
    print("  龍魂·电商信任重建 数学建模引擎 — 12条测试向量验证")
    print("  DNA: #龍芯⚡️丙午·乙未·丙申·申时·☱兑-ECOM-TRUST-ENGINE-V1.0.1-P0-1002819c")
    print("=" * 68)

    passed = 0
    for tid in sorted(results.keys(), key=lambda x: int(x[1:])):
        ok, detail = results[tid]
        mark = "✅" if ok else "❌"
        if ok:
            passed += 1
        print(f"  {mark} {tid}: {detail}")

    total = len(results)
    print("-" * 68)
    all_green = passed == total
    status = "🟢 全绿通过！引擎就绪。" if all_green else f"🔴 {total-passed}条失败！"
    print(f"  结果: {passed}/{total} 通过  {status}")
    print("=" * 68 + "\n")
    return passed, total


# ══════════════════════════════════════════════════════════════════
# 主入口
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    results = run_all_tests()
    passed, total = print_test_report(results)

    if passed != total:
        exit(1)

    # 演示：完整商家生命周期
    print("━" * 68)
    print("  演示：G3档商家完整生命周期模拟")
    print("━" * 68)

    shop = MerchantState(merchant_id="DEMO-001", commit_tier="G3")
    print(f"  入驻: S={shop.score}, 承诺档={shop.commit_tier}, κ={get_kappa(shop.commit_tier)}")

    # 运营30天：5次抽检通过 + 3次主动赔付 + 连续30天零实证
    events_30d = [("如实描述抽检", None)] * 5 + [("主动赔付履约", None)] * 3 + [("连续30天零实证", None)]
    apply_events(shop, events_30d)
    print(f"  运营30天后: S={shop.score} (期望: 500+5×2.2+3×5.5+10×1.1=500+11+16.5+11=538.5)")

    # 遇到1次实证举报(w=中)
    apply_events(shop, [("实证举报", "中")])
    print(f"  实证举报后: S={shop.score} (期望: 538.5-40=498.5)")

    # 180天后恢复
    shop.deduction_records[-1].date = (datetime.now() - timedelta(days=181)).strftime("%Y-%m-%d")
    new_s, recovered = compute_half_life_recovery(shop)
    shop.score = new_s  # 将回填后的分数写回状态
    print(f"  180天半衰恢复: S={shop.score}, 回填={recovered} (40×0.5=20)")

    # 综合评估
    assessments = overall_assessment(shop)
    print(f"\n  综合评估:")
    for dim, (mark, desc) in assessments.items():
        print(f"    {mark.value} {dim}: {desc}")

    # 信任摩擦
    tau, desc, mark = compute_tau(shop.disputes_90d, shop.transactions_90d or 1000)
    print(f"    信任摩擦: {desc}")

    print("\n  数学建模引擎 v1.0 — 12/12 全绿 — 可部署 ✅\n")
