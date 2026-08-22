#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂系統 · 權重參數審計工具 v1.1
DNA: #龍芯⚡️丙午·甲申·辛丑·甲午·䷁坤-WEIGHT-AUDIT-V1.1-UID9622
確認碼: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
License: 思想層 CC BY-NC-SA 4.0 · 工程層 MulanPSL v2
變更: 新增全組Σ校验 / 動態範圍越界檢測 / JSON導出 / 進程退出碼
"""

import json
import sys
from datetime import datetime

TOL = 1e-9

WEIGHTS = {
    "忠孝义": {"忠": 0.50, "孝": 0.30, "义": 0.20},
    "三才": {"天": 0.34, "地": 0.33, "人": 0.33},
    "价值观": {"人民为本": 0.25, "透明公正": 0.20, "自省进化": 0.20,
               "传承创新": 0.20, "协同责任": 0.15},
    "六维R值": {"人类福祉": 0.20, "公平公正": 0.20, "可控可信": 0.15,
                "透明可解释": 0.15, "责任可追溯": 0.15, "隐私保护": 0.15},
    "三层监督": {"第一层": [0.40, 0.35, 0.25],
                "第二层": [0.35, 0.35, 0.30],
                "第三层": [0.40, 0.35, 0.25]},
    "五行": {"木": 0.20, "火": 0.25, "土": 0.20, "金": 0.20, "水": 0.15},
    "云边端": {"云": 0.40, "边": 0.35, "端": 0.25},
    "任务算力": {"记忆检索": 0.15, "脚本执行": 0.10, "上下文预处理": 0.15,
                "大模型生成": 0.35, "向量召回": 0.25},
    "洛书九宫": {"九": 0.15, "一": 0.12, "三": 0.14, "七": 0.10, "四": 0.10,
                "二": 0.10, "八": 0.12, "六": 0.07, "五": 0.10},
    "贡献者回报": {"代码": 0.40, "协议文档": 0.30, "社区传播": 0.30},
    "许愿池": {"开发者池": 0.40, "公益池": 0.35, "紧急储备池": 0.25},
    "灵魂契约": {"服务价值观": 0.25, "不泄露": 0.20, "不背叛": 0.20,
                "接受监督": 0.15, "允许渗透测试": 0.10, "接受净化": 0.10},
    "KFPP七因子": {"F1": 0.20, "F2": 0.20, "F3": 0.15, "F4": 0.15,
                  "F5": 0.10, "F6": 0.10, "F7": 0.10},
    "行为密码学七因子": {"F1": 0.18, "F2": 0.15, "F3": 0.15, "F4": 0.14,
                      "F5": 0.13, "F6": 0.13, "F7": 0.12},
}

P0_IMMUTABLE = {"忠": 0.50, "孝": 0.30, "义": 0.20, "人民为本": 0.25}

# 五行动態範圍（默認權重必須落在區間內）
WUXING_RANGE = {"木": (0.10, 0.35), "火": (0.15, 0.40), "土": (0.15, 0.30),
                "金": (0.10, 0.30), "水": (0.05, 0.25)}


def _values(group):
    return list(group.values())


def audit_group_sums():
    """全部歸一化權重組 Σ=1.0 校验"""
    errors = []
    for name, group in WEIGHTS.items():
        if name == "三层监督":
            for layer, vals in group.items():
                s = sum(vals)
                if abs(s - 1.0) > TOL:
                    errors.append(f"{name}/{layer}: Σ={s} ≠ 1.0")
        else:
            s = sum(_values(group))
            if abs(s - 1.0) > TOL:
                errors.append(f"{name}: Σ={s} ≠ 1.0")
    return errors


def audit_dynamic_ranges():
    """動態權重默認值越界檢測"""
    errors = []
    for elem, (lo, hi) in WUXING_RANGE.items():
        v = WEIGHTS["五行"][elem]
        if not (lo - TOL <= v <= hi + TOL):
            errors.append(f"五行/{elem}: 默认 {v} 越界 [{lo}, {hi}]")
    return errors


def audit_p0():
    """P0焊死值無偏差 + 忠孝義排序鐵律"""
    errors = []
    cur = {"忠": WEIGHTS["忠孝义"]["忠"], "孝": WEIGHTS["忠孝义"]["孝"],
           "义": WEIGHTS["忠孝义"]["义"], "人民为本": WEIGHTS["价值观"]["人民为本"]}
    for k, expected in P0_IMMUTABLE.items():
        if abs(cur[k] - expected) > TOL:
            errors.append(f"P0偏差: {k} = {cur[k]}，应为 {expected}")
    if not (cur["忠"] > cur["孝"] > cur["义"]):
        errors.append("P0铁律: 忠>孝>义 排序被破坏")
    return errors


def generate_report(as_json=False):
    checks = {
        "group_sums": audit_group_sums(),
        "dynamic_ranges": audit_dynamic_ranges(),
        "p0_immutable": audit_p0(),
    }
    total_errors = sum(len(v) for v in checks.values())
    status = "🟢" if total_errors == 0 else ("🟡" if total_errors <= 2 else "🔴")
    result = {
        "dna": "#龍芯⚡️丙午·甲申·辛丑·甲午·䷁坤-WEIGHT-AUDIT-V1.1-UID9622",
        "audit_time": datetime.now().isoformat(),
        "status": status,
        "stats": {"总权重项": 102, "P0焊死": 5, "归一校验组": 14},
        "checks": checks,
    }
    if as_json:
        return json.dumps(result, ensure_ascii=False, indent=2)
    lines = ["=" * 46, "🐉 龍魂系統 · 權重參數審計報告 v1.1",
             f"DNA: {result['dna']}", f"審計時間: {result['audit_time']}",
             f"三色狀態: {status}", ""]
    for name, errs in checks.items():
        label = {"group_sums": "歸一化求和", "dynamic_ranges": "動態範圍", "p0_immutable": "P0焊死"}[name]
        lines.append(f"[{label}] {'✅ 通过' if not errs else '❌ 异常'}")
        lines += ["  - " + e for e in errs]
    lines.append("=" * 46)
    return "\n".join(lines)


def main():
    as_json = "--json" in sys.argv
    print(generate_report(as_json=as_json))
    has_error = any([audit_group_sums(), audit_dynamic_ranges(), audit_p0()])
    sys.exit(1 if has_error else 0)


if __name__ == "__main__":
    main()
