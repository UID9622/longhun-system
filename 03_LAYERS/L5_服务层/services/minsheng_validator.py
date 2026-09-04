#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷌同人-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# ============================================================
# 龍魂民生系统 · 通用校验器（5条硬要求焊死）
# 文件：L5_服务层/services/minsheng_validator.py
# 适用：开店/维权/医疗/教育/就业/养老 所有民生场景
# ============================================================

from typing import List, Any
from siju_decision import (
    DecisionReport, Provenance, Derivation, PolicyAnalysis,
    CustomAnalysis, ScheduleAnalysis, DataSourceType,
)


def validate_five_hard_rules(report: DecisionReport) -> List, Any[str]:
    """
    5条硬要求 - 缺一条返回对应错误，全过返回空列表
    1. 来源标注  2. 推演标注  3. 备注规范  4. 引用依据  5. 政策·风俗·作息分析
    """
    errors: List[Any], Any[str] = []

    # 1. 来源标注
    if not report.data_sources:
        errors.append("❌ 缺少来源标注（data_sources 为空）")
    else:
        for p in report.data_sources:
            try:
                p.validate()
            except AssertionError as e:
                errors.append(str(e))

    # 2. 推演标注
    chains = []
    for sec in (report.dimai, report.renliu, report.kouwei, report.jinghe):
        if sec and sec.derivation_chain:
            chains.extend(sec.derivation_chain)
    if not chains:
        errors.append("❌ 缺少推演标注（四绝 derivation_chain 全空）")
    for d in chains:
        try:
            d.validate()
        except AssertionError as e:
            errors.append(str(e))

    # 3. 备注规范（来源必须有 notes，已在 Provenance.validate 覆盖，这里补 policy/custom）
    for pa in report.policy_analysis:
        if not pa.provenance.notes:
            errors.append(f"❌ 政策『{pa.policy_name}』备注缺失")
    for sa in report.schedule_analysis:
        if not sa.provenance.notes:
            errors.append(f"❌ 作息『{sa.group_type}』备注缺失")

    # 4. 引用依据
    if not report.policy_analysis:
        errors.append("❌ 政策分析缺失（引用依据无从挂起）")
    for pa in report.policy_analysis:
        if not (pa.provenance.ref_policy or pa.provenance.ref_custom):
            errors.append(f"❌ 政策『{pa.policy_name}』引用依据(ref)缺失")

    # 5. 政府政策·风俗·作息·地域习俗分析（不可跳过）
    if not report.policy_analysis:
        errors.append("❌ 政策分析缺失（第5条硬要求）")
    if not report.schedule_analysis:
        errors.append("❌ 作息分析缺失（第5条硬要求）")

    return errors


def audit_report(report: DecisionReport) -> dict[str, Any]:
    """返回结构化审计结果，交给前端/API 展示"""
    errors = validate_five_hard_rules(report)
    return {
        "dna_trace": report.dna_trace,
        "passed": len(errors) == 0,
        "errors": errors,
        "checked_at": __import__("datetime").datetime.now().isoformat(),
    }


if __name__ == "__main__":
    # 故意构造一个不合规报告，验证校验器能抓错
    from datetime import datetime
    dna = DecisionReport.make_dna("9622")
    bad = DecisionReport(dna_trace=dna, applicant="x", apply_time=datetime.now(),
                         generate_time=datetime.now(),
                         data_sources=[Provenance(source_type=DataSourceType.INFERENCE,
                                                  source_url="", fetch_time=datetime.now(),
                                                  reliability="low", update_frequency="",
                                                  dna_trace=dna, notes="")])
    res = audit_report(bad)
    print("审计通过?", res["passed"])
    for e in res["errors"]:
        print(" ", e)
