#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
lh_pangdonglai_audit — 龍魂·胖东来分成审计执行器 v1.0

自动读取企业财报数据，按五维不等式逐条校验，生成三色审计报告。
违约自动分级（🟡🟠🔴⚫），支持JSON/终端表格/HTML三种输出。

DNA: #龍芯⚡️丙午·癸未·丁亥·丙午·䷣明-PANGDONGLAI-AUDIT-EXEC-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

用法:
  python3 bin/lh_pangdonglai_audit.py audit --data audit_data.json     # 审计JSON数据
  python3 bin/lh_pangdonglai_audit.py audit --values 100 50 5 31 9 5  # 直接传值
  python3 bin/lh_pangdonglai_audit.py audit --stdin                    # 从stdin读JSON
  python3 bin/lh_pangdonglai_audit.py test                             # 跑一遍测试向量
  python3 bin/lh_pangdonglai_audit.py rules                            # 显示不等式规则
  python3 bin/lh_pangdonglai_audit.py report --id PDL-2026-Q3-001     # 查看历史报告
"""

import argparse
import json
import math
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUDIT_LOG_DIR = PROJECT_ROOT / "logs" / "pangdonglai_audit"

# ============================================================
# 常量定义
# ============================================================

# 不等式焊死阈值
THRESHOLDS = {
    "R_e_min": 0.50,   # 员工分配 ≥ 50%
    "R_f_max": 0.10,   # 创始人提取 ≤ 10%
    "R_i_min": 0.30,   # 再投资 ≥ 30%
    "R_p_min": 0.05,   # 公益 ≥ 5%
    "R_b_max": 0.05,   # 风险缓冲 ≤ 5%
}

# 边缘案例特殊阈值
EDGE_THRESHOLDS = {
    "micro_enterprise_N_ceiling": 100000,    # 微利企业上限（10万元）
    "micro_enterprise_R_p_min": 0.02,        # 微利企业公益下限降至2%
    "tiny_team_size": 3,                     # 微型企业人数阈值
    "tiny_team_R_e_min": 0.40,               # 微型企业员工下限降至40%
    "public_welfare_carry_forward": 2,        # 公益最多结转期数
}

# 违约分级
VIOLATION_LEVELS = {
    "light":  {"threshold": 0.05, "mark": "🟡", "label": "轻度", "action": "警告·限期30天整改"},
    "medium": {"threshold": 0.20, "mark": "🟠", "label": "中度", "action": "冻结非核心接口·限期60天"},
    "severe": {"threshold": 1.00, "mark": "🔴", "label": "重度", "action": "冻结全部核心接口·公开追溯"},
    "malicious": {"threshold": float("inf"), "mark": "⚫", "label": "恶意", "action": "永久冻结·失信名单"},
}


class AuditMark(Enum):
    GREEN = "🟢"
    YELLOW = "🟡"
    ORANGE = "🟠"
    RED = "🔴"
    BLACK = "⚫"


# ============================================================
# 数据模型
# ============================================================

@dataclass
class FinancialData:
    """企业财务数据"""
    N: float = 0.0       # 净利润
    R_e: float = 0.0     # 员工分配
    R_f: float = 0.0     # 创始人提取
    R_i: float = 0.0     # 再投资
    R_p: float = 0.0     # 公益
    R_b: float = 0.0     # 风险缓冲
    employee_count: int = 10       # 员工数
    enterprise_name: str = ""      # 企业名称
    uscc: str = ""                 # 统一社会信用代码
    period: str = ""               # 审计期间（如 2026-Q3）
    is_micro_profit: bool = False  # 是否微利企业
    is_tiny_team: bool = False     # 是否微型企业
    conflict_resolution: bool = False  # 是否冲突消解场景（利润不足·R_f/R_b/R_p已被削至0）
    public_welfare_carried: int = 0  # 公益已结转期数

    def total(self) -> float:
        return self.R_e + self.R_f + self.R_i + self.R_p + self.R_b

    def validate_sum(self) -> Tuple[bool, float]:
        """恒等式校验 R_e+R_f+R_i+R_p+R_b = N"""
        t = self.total()
        diff = abs(t - self.N)
        return diff < 0.01, diff  # 1分钱容差


@dataclass
class CheckResult:
    """单条检查结果"""
    rule: str
    expected: float
    actual: float
    ratio: float
    pass_: bool
    mark: str
    detail: str = ""


@dataclass
class AuditReport:
    """审计报告"""
    audit_id: str
    dna: str
    enterprise: Dict[str, str]
    financials: Dict[str, float]
    checks: List[Dict[str, Any]] = field(default_factory=list)
    overall: str = "🟢"
    violations: List[Dict[str, Any]] = field(default_factory=list)
    edge_cases: List[str] = field(default_factory=list)
    timestamp: str = ""
    auditor_dna: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "dna": self.dna,
            "enterprise": self.enterprise,
            "financials": self.financials,
            "checks": self.checks,
            "overall": self.overall,
            "violations": self.violations,
            "edge_cases": self.edge_cases,
            "timestamp": self.timestamp,
            "auditor_dna": self.auditor_dna,
        }


# ============================================================
# 审计核心引擎
# ============================================================

class PangDongLaiAuditor:
    """胖东来分成审计器"""

    def __init__(self):
        self.thresholds = THRESHOLDS.copy()
        self.edge_thresholds = EDGE_THRESHOLDS.copy()

    def audit(self, data: FinancialData) -> AuditReport:
        """执行完整审计"""
        audit_id = f"PDL-{data.period or datetime.now().strftime('%Y-Q%m')}-{_short_hash(str(data.N))}"
        dna = f"#龍芯⚡️{_ganzhi_now()}-PANGDONGLAI-AUDIT-{_short_hash(audit_id)}"

        report = AuditReport(
            audit_id=audit_id,
            dna=dna,
            enterprise={"name": data.enterprise_name, "uscc": data.uscc, "period": data.period or "N/A"},
            financials={"N": data.N, "R_e": data.R_e, "R_f": data.R_f, "R_i": data.R_i, "R_p": data.R_p, "R_b": data.R_b},
            timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            auditor_dna="#龍芯⚡️丙午·癸未·丁亥·丙午·䷣明-PANGDONGLAI-AUDIT-v1.0",
        )

        # 前置检查：亏损不审
        if data.N <= 0:
            report.edge_cases.append(f"企业亏损(N={data.N})·不触发分成审计·仅记录")
            report.overall = "🟡"
            report.checks.append({"rule": "前置条件: N > 0", "expected": "> 0", "actual": data.N, "ratio": None, "pass": True, "mark": "🟡", "detail": "亏损·免审"})
            return report

        # 边缘案例：微利企业调整公益下限
        effective_thresholds = self.thresholds.copy()
        if data.N < self.edge_thresholds["micro_enterprise_N_ceiling"] or data.is_micro_profit:
            effective_thresholds["R_p_min"] = self.edge_thresholds["micro_enterprise_R_p_min"]
            report.edge_cases.append(f"微利企业(N={data.N}<10万)·公益下限降至{effective_thresholds['R_p_min']*100:.0f}%")

        # 边缘案例：微型企业调整员工下限
        if data.employee_count <= self.edge_thresholds["tiny_team_size"] or data.is_tiny_team:
            effective_thresholds["R_e_min"] = self.edge_thresholds["tiny_team_R_e_min"]
            report.edge_cases.append(f"微型企业(员工{data.employee_count}人≤{self.edge_thresholds['tiny_team_size']})·员工下限降至{effective_thresholds['R_e_min']*100:.0f}%")

        # 边缘案例：公益结转
        if data.public_welfare_carried > 0:
            report.edge_cases.append(f"公益已结转{data.public_welfare_carried}期·上限{self.edge_thresholds['public_welfare_carry_forward']}期")

        # 处理负R_f（创始人注资）→ 计入R_i
        actual_R_f = data.R_f
        actual_R_i = data.R_i
        has_founder_injection = data.R_f < 0
        if has_founder_injection:
            actual_R_i += abs(data.R_f)
            actual_R_f = 0.0
            report.edge_cases.append(f"创始人注资补亏{abs(data.R_f):.2f}元·计入再投资·R_f审计值设为0")

        # 冲突消解场景：利润不足时 R_f/R_b/R_p 已被依法削减至0
        is_conflict = data.conflict_resolution
        if is_conflict:
            report.edge_cases.append("冲突消解场景·利润不足·R_f/R_b/R_p已依法削减·仅核验R_e优先级")

        # ── 逐条不等式校验 ──
        checks = []

        # 1. R_e ≥ R_e_min × N
        r_e_min = effective_thresholds["R_e_min"] * data.N
        checks.append(self._check("R_e ≥ {:.0f}%×N".format(effective_thresholds["R_e_min"] * 100),
                                   r_e_min, data.R_e, data.N, is_lower_bound=True))

        # 2. R_f ≤ R_f_max × N
        r_f_max = effective_thresholds["R_f_max"] * data.N
        checks.append(self._check("R_f ≤ {:.0f}%×N".format(effective_thresholds["R_f_max"] * 100),
                                   r_f_max, actual_R_f, data.N, is_lower_bound=False))

        # 3. R_i ≥ R_i_min × N
        r_i_min = effective_thresholds["R_i_min"] * data.N
        checks.append(self._check("R_i ≥ {:.0f}%×N".format(effective_thresholds["R_i_min"] * 100),
                                   r_i_min, actual_R_i, data.N, is_lower_bound=True))

        # 4. R_p ≥ R_p_min × N
        r_p_min = effective_thresholds["R_p_min"] * data.N
        rp_check = self._check("R_p ≥ {:.0f}%×N".format(effective_thresholds["R_p_min"] * 100),
                                r_p_min, data.R_p, data.N, is_lower_bound=True)
        if is_conflict and data.R_p == 0:
            rp_check.mark = "🟡"
            rp_check.pass_ = True
            rp_check.detail = "冲突消解·公益已依法削减至0"
        checks.append(rp_check)

        # 5. R_b ≤ R_b_max × N
        r_b_max = effective_thresholds["R_b_max"] * data.N
        rb_check = self._check("R_b ≤ {:.0f}%×N".format(effective_thresholds["R_b_max"] * 100),
                                r_b_max, data.R_b, data.N, is_lower_bound=False)
        if is_conflict and data.R_b == 0:
            rb_check.mark = "🟡"
            rb_check.pass_ = True
            rb_check.detail = "冲突消解·风险缓冲已依法削减至0"
        elif rb_check.mark == "🔴":
            rb_check.mark = "🟡"
            rb_check.detail = "风险缓冲超额·超额部分视为再投资或需说明用途"
        checks.append(rb_check)

        # 6. 恒等式约束
        sum_ok, sum_diff = data.validate_sum()
        if has_founder_injection or is_conflict:
            # 创始人注资/冲突消解场景：允许恒等式偏差
            sum_ok = True
            sum_diff = 0.0
        sum_check = CheckResult(
            rule="R_e+R_f+R_i+R_p+R_b = N",
            expected=data.N,
            actual=data.total(),
            ratio=data.total() / data.N if data.N != 0 else 0,
            pass_=sum_ok,
            mark="🟢" if sum_ok else "🟡",
            detail="恒等式满足" if sum_ok else f"偏差{sum_diff:.2f}元",
        )
        checks.append(sum_check)

        # ── 汇总判定 ──
        report.checks = [{
            "rule": c.rule,
            "expected": round(c.expected, 2),
            "actual": round(c.actual, 2),
            "ratio": round(c.ratio, 4),
            "pass": c.pass_,
            "mark": c.mark,
            "detail": c.detail,
        } for c in checks]

        violations = [c for c in report.checks if not c["pass"]]
        report.violations = violations

        if not violations:
            report.overall = "🟢"
        elif len(violations) == 1:
            severity = self._classify_violation(violations[0])
            level_map = {"malicious": "⚫", "severe": "🔴", "medium": "🟠", "light": "🟡"}
            report.overall = level_map.get(severity, "🟡")
        else:
            # 多项违约取最严重 + 升一级处罚
            severities = [self._classify_violation(v) for v in violations]
            severity_order = {"light": 0, "medium": 1, "severe": 2, "malicious": 3}
            max_sev = max(severities, key=lambda s: severity_order.get(s, 0))
            # 升级：多项违约自动升一级
            upgraded = {"light": "medium", "medium": "severe", "severe": "malicious", "malicious": "malicious"}
            final = upgraded.get(max_sev, max_sev)
            level_map = {"malicious": "⚫", "severe": "🔴", "medium": "🟠", "light": "🟡"}
            report.overall = level_map.get(final, "🟡")

        return report

    def _check(self, rule: str, expected: float, actual: float, N: float, is_lower_bound: bool) -> CheckResult:
        """执行单条不等式检查"""
        ratio = actual / N if N != 0 else 0

        if is_lower_bound:
            pass_ = actual >= expected - 0.01  # 1分钱容差
        else:
            pass_ = actual <= expected + 0.01

        if pass_:
            mark = "🟢"
            detail = "通过"
        else:
            deviation = abs(actual - expected)
            deviation_pct = deviation / N if N != 0 else 1.0
            if deviation_pct > 0.20:
                mark = "🔴"
            elif deviation_pct > 0.05:
                mark = "🟠"
            else:
                mark = "🟡"
            direction = "不足" if is_lower_bound else "超出"
            detail = f"{direction}{deviation:.2f}元(偏差{deviation_pct*100:.1f}%)"

        return CheckResult(rule=rule, expected=expected, actual=actual, ratio=ratio, pass_=pass_, mark=mark, detail=detail)

    def _classify_violation(self, check: Dict[str, Any]) -> str:
        """对单条违约进行分级"""
        ratio = check.get("ratio", 0)
        expected_ratio = _extract_expected_ratio(check.get("rule", ""))
        if expected_ratio is None:
            return "light"
        deviation = abs(ratio - expected_ratio)
        if deviation > 0.20:
            return "severe"
        elif deviation > 0.05:
            return "medium"
        return "light"


# ============================================================
# 辅助函数
# ============================================================

def _extract_expected_ratio(rule: str) -> Optional[float]:
    """从规则字符串提取期望比例"""
    import re
    m = re.search(r'(\d+)%', rule)
    if m:
        return int(m.group(1)) / 100
    return None


def _short_hash(s: str) -> str:
    """8位短哈希"""
    import hashlib
    return hashlib.sha256(s.encode()).hexdigest()[:8]


def _ganzhi_now() -> str:
    """返回当前干支简写（年·月·日）"""
    now = datetime.now()
    return f"{now.year}-{now.month:02d}-{now.day:02d}"


def load_data_from_json(filepath: str) -> FinancialData:
    """从JSON文件加载财务数据"""
    with open(filepath, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return _dict_to_financial(raw)


def load_data_from_args(values: List[float], name: str = "", period: str = "") -> FinancialData:
    """从命令行参数列表构建财务数据"""
    keys = ["N", "R_e", "R_f", "R_i", "R_p", "R_b"]
    d = {}
    for k, v in zip(keys, values):
        d[k] = float(v)
    d["enterprise_name"] = name
    d["period"] = period
    return _dict_to_financial(d)


def _dict_to_financial(d: Dict[str, Any]) -> FinancialData:
    return FinancialData(
        N=float(d.get("N", 0)),
        R_e=float(d.get("R_e", 0)),
        R_f=float(d.get("R_f", 0)),
        R_i=float(d.get("R_i", 0)),
        R_p=float(d.get("R_p", 0)),
        R_b=float(d.get("R_b", 0)),
        employee_count=int(d.get("employee_count", 10)),
        enterprise_name=str(d.get("enterprise_name", "")),
        uscc=str(d.get("uscc", "")),
        period=str(d.get("period", "")),
        is_micro_profit=bool(d.get("is_micro_profit", False)),
        is_tiny_team=bool(d.get("is_tiny_team", False)),
        conflict_resolution=bool(d.get("conflict_resolution", False)),
        public_welfare_carried=int(d.get("public_welfare_carried", 0)),
    )


# ============================================================
# 输出格式化
# ============================================================

def format_table(report: AuditReport) -> str:
    """终端彩色表格输出"""
    lines = []
    lines.append("")
    lines.append("╔══════════════════════════════════════════════════════╗")
    lines.append("║   龍魂·胖东来分成审计报告                              ║")
    lines.append("╠══════════════════════════════════════════════════════╣")
    lines.append(f"║ 审计ID: {report.audit_id:<44s}║")
    lines.append(f"║ 企业:   {report.enterprise.get('name','N/A'):<44s}║")
    lines.append(f"║ 期间:   {report.enterprise.get('period','N/A'):<44s}║")
    lines.append(f"║ 时间:   {report.timestamp:<44s}║")
    lines.append(f"║ DNA:    {report.dna:<44s}║")
    lines.append("╠══════════════════════════════════════════════════════╣")

    # 财务数据
    fin = report.financials
    lines.append("║ 净利润 N  = {:>10.2f} 元                          ║".format(fin["N"]))
    lines.append("║ 员工分配 R_e = {:>8.2f} 元  ({:.1f}%)                ║".format(fin["R_e"], fin["R_e"]/fin["N"]*100 if fin["N"] else 0))
    lines.append("║ 创始人提取 R_f = {:>6.2f} 元  ({:.1f}%)                ║".format(fin["R_f"], fin["R_f"]/fin["N"]*100 if fin["N"] else 0))
    lines.append("║ 再投资 R_i = {:>8.2f} 元  ({:.1f}%)                ║".format(fin["R_i"], fin["R_i"]/fin["N"]*100 if fin["N"] else 0))
    lines.append("║ 公益 R_p = {:>8.2f} 元  ({:.1f}%)                ║".format(fin["R_p"], fin["R_p"]/fin["N"]*100 if fin["N"] else 0))
    lines.append("║ 风险缓冲 R_b = {:>6.2f} 元  ({:.1f}%)                ║".format(fin["R_b"], fin["R_b"]/fin["N"]*100 if fin["N"] else 0))
    lines.append("╠══════════════════════════════════════════════════════╣")

    # 检查项
    lines.append("║ 逐项审计:                                            ║")
    for c in report.checks:
        status = "✅" if c["pass"] else "❌"
        lines.append(f"║  {c['mark']} {c['rule']:<38s} {status} ║")
        if c.get("detail") and c["detail"] not in ("通过", "恒等式满足"):
            lines.append(f"║     → {c['detail']:<46s}║")

    # 边缘案例
    if report.edge_cases:
        lines.append("╠══════════════════════════════════════════════════════╣")
        lines.append("║ 边缘案例:                                            ║")
        for ec in report.edge_cases:
            lines.append(f"║  → {ec:<48s}║")

    # 违规
    if report.violations:
        lines.append("╠══════════════════════════════════════════════════════╣")
        lines.append("║ ⚠️  违规项:                                          ║")
        for v in report.violations:
            lines.append(f"║  {v['mark']} {v['rule']}: 实际{v['actual']:.2f} vs 期望{v['expected']:.2f} ║")

    # 总结
    lines.append("╠══════════════════════════════════════════════════════╣")
    overall_label = {"🟢": "✅ 全部通过", "🟡": "⚠️  轻度违规·警告", "🟠": "⚠️  中度违规·冻结非核心", "🔴": "🚫 重度违规·全冻结", "⚫": "⛔ 恶意违规·永久封禁"}
    lines.append(f"║ 总判定: {report.overall} {overall_label.get(report.overall, ''):<38s}║")
    lines.append("╚══════════════════════════════════════════════════════╝")
    return "\n".join(lines)


def format_html(report: AuditReport) -> str:
    """HTML格式审计报告"""
    fin = report.financials
    N = fin["N"] if fin["N"] else 1

    def pct(v): return f"{v/N*100:.1f}%"

    check_rows = ""
    for c in report.checks:
        status = "✅" if c["pass"] else "❌"
        detail_html = f'<br><small style="color:#888">{c["detail"]}</small>' if c.get("detail") and c["detail"] not in ("通过", "恒等式满足") else ""
        check_rows += f"""
        <tr style="background:{'#e8f5e9' if c['pass'] else '#ffebee'}">
            <td>{c['mark']}</td>
            <td>{c['rule']}</td>
            <td>{c['expected']:,.2f}</td>
            <td>{c['actual']:,.2f}</td>
            <td>{pct(c.get('ratio',0)*N or 0)}</td>
            <td>{status}{detail_html}</td>
        </tr>"""

    edge_html = "".join(f"<li>{ec}</li>" for ec in report.edge_cases) if report.edge_cases else "<li>无</li>"
    violation_html = "".join(f"<li>{v['mark']} {v['rule']}: 实际{v['actual']:,.2f} vs 期望{v['expected']:,.2f}</li>" for v in report.violations) if report.violations else "<li>无</li>"

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>胖东来分成审计报告 - {report.audit_id}</title>
<style>
body {{ font-family: "PingFang SC","Microsoft YaHei",sans-serif; max-width:900px; margin:40px auto; padding:20px; color:#1a1a1a; }}
h1 {{ color:#c41e3a; border-bottom:2px solid #c41e3a; padding-bottom:8px; }}
.dna {{ background:#f5f5f5; border-left:3px solid #c41e3a; padding:10px; font-family:monospace; font-size:11px; margin:10px 0; }}
.summary {{ display:flex; gap:20px; margin:20px 0; }}
.card {{ flex:1; background:#fafafa; border:1px solid #ddd; border-radius:8px; padding:16px; text-align:center; }}
.card .value {{ font-size:28px; font-weight:bold; color:#c41e3a; }}
.card .label {{ font-size:12px; color:#888; margin-top:4px; }}
table {{ border-collapse:collapse; width:100%; margin:16px 0; }}
th,td {{ border:1px solid #ddd; padding:10px; text-align:left; }}
th {{ background:#c41e3a; color:#fff; }}
.overall {{ font-size:48px; text-align:center; margin:20px 0; }}
.footer {{ margin-top:40px; padding-top:16px; border-top:1px solid #eee; font-size:11px; color:#888; }}
</style>
</head>
<body>
<h1>龍魂·胖东来分成审计报告</h1>
<div class="dna">审计ID: {report.audit_id}<br>DNA: {report.dna}<br>企业: {report.enterprise.get('name','N/A')} | 期间: {report.enterprise.get('period','N/A')}<br>时间: {report.timestamp}</div>

<div class="summary">
  <div class="card"><div class="value">{N:,.0f}</div><div class="label">净利润 N（元）</div></div>
  <div class="card"><div class="value">{pct(fin['R_e'])}</div><div class="label">员工分配比例</div></div>
  <div class="card"><div class="value">{pct(fin['R_f'])}</div><div class="label">创始人提取比例</div></div>
  <div class="card"><div class="value">{pct(fin['R_i'])}</div><div class="label">再投资比例</div></div>
  <div class="card"><div class="value">{pct(fin['R_p'])}</div><div class="label">公益比例</div></div>
</div>

<div class="overall">{report.overall}</div>

<h2>逐项审计</h2>
<table>
<tr><th>标记</th><th>不等式</th><th>期望值</th><th>实际值</th><th>比例</th><th>结果</th></tr>
{check_rows}
</table>

<h2>边缘案例</h2><ul>{edge_html}</ul>

<h2>违规项</h2><ul>{violation_html}</ul>

<div class="footer">
龍魂·胖东来分成审计引擎 v1.0 | {report.auditor_dna}<br>
创建者: 诸葛鑫（UID9622） | 协议: CC BY-NC-SA 4.0 | 数据主权归企业·审计链仅存哈希
</div>
</body>
</html>"""


# ============================================================
# 测试向量
# ============================================================

TEST_VECTORS = [
    {
        "name": "标准案例（全通过）",
        "data": FinancialData(N=1_000_000, R_e=500_000, R_f=50_000, R_i=310_000, R_p=90_000, R_b=50_000,
                              enterprise_name="测试企业A", period="2026-Q3"),
        "expected": "🟢",
    },
    {
        "name": "违约案例（双项违规）",
        "data": FinancialData(N=1_000_000, R_e=300_000, R_f=150_000, R_i=350_000, R_p=150_000, R_b=50_000,
                              enterprise_name="测试企业B", period="2026-Q3"),
        "expected": "🔴",
    },
    {
        "name": "亏损免审",
        "data": FinancialData(N=-100_000, R_e=0, R_f=0, R_i=0, R_p=0, R_b=0,
                              enterprise_name="亏损企业C", period="2026-Q3"),
        "expected": "🟡",
    },
    {
        "name": "冲突消解（利润不足）",
        "data": FinancialData(N=800_000, R_e=400_000, R_f=0, R_i=400_000, R_p=0, R_b=0,
                              enterprise_name="利润不足企业D", period="2026-Q3",
                              conflict_resolution=True),
        "expected": "🟢",
    },
    {
        "name": "创始人注资补亏",
        "data": FinancialData(N=1_000_000, R_e=500_000, R_f=-100_000, R_i=500_000, R_p=50_000, R_b=50_000,
                              enterprise_name="注资企业E", period="2026-Q3"),
        "expected": "🟢",
    },
    {
        "name": "微利企业（调整公益下限）",
        "data": FinancialData(N=50_000, R_e=25_000, R_f=2_500, R_i=17_500, R_p=2_500, R_b=2_500,
                              enterprise_name="微利企业F", period="2026-Q3", is_micro_profit=True),
        "expected": "🟢",
    },
    {
        "name": "微型企业（调整员工下限）",
        "data": FinancialData(N=500_000, R_e=200_000, R_f=50_000, R_i=175_000, R_p=50_000, R_b=25_000,
                              enterprise_name="微型企业G", period="2026-Q3", employee_count=3),
        "expected": "🟢",
    },
]


def run_tests() -> bool:
    """运行所有测试向量"""
    auditor = PangDongLaiAuditor()
    all_pass = True
    print("\n═══════════════════════════════════════════")
    print("  胖东来分成审计 · 测试向量验证")
    print("═══════════════════════════════════════════\n")
    for i, tv in enumerate(TEST_VECTORS, 1):
        report = auditor.audit(tv["data"])
        ok = report.overall == tv["expected"]
        status = "✅" if ok else "❌"
        print(f"{status} 测试{i}: {tv['name']}")
        print(f"   期望: {tv['expected']}  实际: {report.overall}  {'匹配' if ok else '不匹配!'}")
        if not ok:
            all_pass = False
            for v in report.violations:
                print(f"   违规: {v['mark']} {v['rule']}")
        print()
    print(f"{'✅ 全部通过!' if all_pass else '❌ 存在失败!'}  ({len(TEST_VECTORS)}个测试向量)\n")
    return all_pass


# ============================================================
# 命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="龍魂·胖东来分成审计执行器 v1.0")
    sub = parser.add_subparsers(dest="command")

    # audit 子命令
    audit_p = sub.add_parser("audit", help="执行审计")
    audit_p.add_argument("--data", help="财务数据JSON文件路径")
    audit_p.add_argument("--values", nargs=6, type=float, metavar=("N","R_e","R_f","R_i","R_p","R_b"),
                         help="直接传入6个数值: N R_e R_f R_i R_p R_b")
    audit_p.add_argument("--stdin", action="store_true", help="从stdin读取JSON")
    audit_p.add_argument("--name", default="", help="企业名称")
    audit_p.add_argument("--period", default="", help="审计期间")
    audit_p.add_argument("--output", "-o", choices=["table","json","html"], default="table", help="输出格式")
    audit_p.add_argument("--save", action="store_true", help="保存审计报告到文件")

    # test 子命令
    sub.add_parser("test", help="运行测试向量")

    # rules 子命令
    sub.add_parser("rules", help="显示不等式规则")

    # report 子命令
    report_p = sub.add_parser("report", help="查看历史审计报告")
    report_p.add_argument("--id", help="审计报告ID")

    args = parser.parse_args()

    if args.command == "audit":
        auditor = PangDongLaiAuditor()

        # 加载数据
        if args.stdin:
            raw = json.loads(sys.stdin.read())
            data = _dict_to_financial(raw)
        elif args.values:
            data = load_data_from_args(args.values, name=args.name, period=args.period)
        elif args.data:
            data = load_data_from_json(args.data)
        else:
            print("❌ 请提供 --data/--values/--stdin 之一", file=sys.stderr)
            sys.exit(1)

        # 执行审计
        report = auditor.audit(data)

        # 输出
        if args.output == "json":
            print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
        elif args.output == "html":
            print(format_html(report))
        else:
            print(format_table(report))

        # 保存
        if args.save:
            AUDIT_LOG_DIR.mkdir(parents=True, exist_ok=True)
            report_file = AUDIT_LOG_DIR / f"{report.audit_id}.json"
            with open(report_file, "w", encoding="utf-8") as f:
                json.dump(report.to_dict(), f, ensure_ascii=False, indent=2)
            print(f"\n📁 报告已保存: {report_file}")

    elif args.command == "test":
        ok = run_tests()
        sys.exit(0 if ok else 1)

    elif args.command == "rules":
        print("""
╔══════════════════════════════════════════════════════╗
║       龍魂·胖东来分成数学协议 — 焊死不等式          ║
╠══════════════════════════════════════════════════════╣
║  R_e ≥ 0.50 × N   员工分配 ≥ 50%（绝对优先）        ║
║  R_f ≤ 0.10 × N   创始人提取 ≤ 10%                  ║
║  R_i ≥ 0.30 × N   再投资 ≥ 30%                      ║
║  R_p ≥ 0.05 × N   公益 ≥ 5%                         ║
║  R_b ≤ 0.05 × N   风险缓冲 ≤ 5%                     ║
╠══════════════════════════════════════════════════════╣
║  恒等式: R_e + R_f + R_i + R_p + R_b = N            ║
╠══════════════════════════════════════════════════════╣
║  边缘案例调整:                                       ║
║  · 微利企业(N<10万): 公益下限降至2%                  ║
║  · 微型企业(≤3人): 员工下限降至40%                   ║
║  · 创始人注资(R_f为负): 计入再投资                   ║
║  · 亏损(N≤0): 不触发审计                             ║
╚══════════════════════════════════════════════════════╝
冲突消解优先级（利润不足时）:
  1. R_e 绝对优先·不可削减
  2. R_f 自动归零
  3. R_b 削减至0
  4. R_p 削减至0
  5. R_i 最后削减
""")

    elif args.command == "report":
        if not args.id:
            # 列出已有报告
            if AUDIT_LOG_DIR.exists():
                reports = sorted(AUDIT_LOG_DIR.glob("PDL-*.json"))
                if reports:
                    print(f"共 {len(reports)} 份审计报告:\n")
                    for r in reports:
                        print(f"  {r.stem}")
                else:
                    print("暂无审计报告")
            else:
                print("暂无审计报告")
        else:
            report_file = AUDIT_LOG_DIR / f"{args.id}.json"
            if report_file.exists():
                with open(report_file, "r", encoding="utf-8") as f:
                    report = json.load(f)
                print(json.dumps(report, ensure_ascii=False, indent=2))
            else:
                print(f"❌ 报告不存在: {args.id}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
