#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 三才算法命名合规检查工具 v1.0
Sancai Algorithm Naming Compliance Checker

检查 bin/ 下所有脚本是否标注了对应的 Sancai.* 命名空间。

用法：
  python3 bin/lh_sancai_naming_check.py --audit       # 审计所有脚本
  python3 bin/lh_sancai_naming_check.py --report      # 生成合规报告
  python3 bin/lh_sancai_naming_check.py --verify-international  # 验证国际对照

DNA: #龍芯⚡️丙午·辛未·乙酉·亥时·䷾既济-SANCAI-NAMING-CHECK-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent
DNA = "#龍芯⚡️丙午·辛未·乙酉·亥时·䷾既济-SANCAI-NAMING-CHECK-v1.0"

# ── 旧命名 → Sancai.* 新命名 映射表 ──
NAMING_MAP: Dict[str, str] = {
    # 天层核心
    "digital_root": "Sancai.Tian.Core.DigitalRoot",
    "dr(": "Sancai.Tian.Core.DigitalRoot",
    "计算数字根": "Sancai.Tian.Core.DigitalRoot",
    "数字根": "Sancai.Tian.Core.DigitalRoot",

    # 天层密码学
    "hash_chain": "Sancai.Tian.Crypto.DNAHashChain",
    "dna_hash": "Sancai.Tian.Crypto.DNAHashChain",
    "DNA哈希链": "Sancai.Tian.Crypto.DNAHashChain",
    "behavioral_crypto": "Sancai.Tian.Crypto.BehavioralCrypto",
    "行为密码学": "Sancai.Tian.Crypto.BehavioralCrypto",
    "conf =": "Sancai.Tian.Crypto.BehavioralCrypto",

    # 天层时间
    "time_decay": "Sancai.Tian.Time.Decay",
    "时间衰减": "Sancai.Tian.Time.Decay",
    "alpha_calib": "Sancai.Tian.Time.AlphaCalibration",
    "α校准": "Sancai.Tian.Time.AlphaCalibration",

    # 地层治理
    "三色审计": "Sancai.Di.Governance.TriColorAudit",
    "tri_color": "Sancai.Di.Governance.TriColorAudit",
    "risk_audit": "Sancai.Di.Governance.TriColorAudit",
    "Risk =": "Sancai.Di.Governance.TriColorAudit",
    "conservation_score": "Sancai.Di.Governance.ConservationScore",
    "守恒分数": "Sancai.Di.Governance.ConservationScore",
    "decision_path": "Sancai.Di.Governance.DecisionPath",
    "决策路径": "Sancai.Di.Governance.DecisionPath",
    "minimal_chain": "Sancai.Di.Governance.MinimalChain",
    "最小执行链": "Sancai.Di.Governance.MinimalChain",

    # 地层伦理
    "sovereignty_index": "Sancai.Di.Ethics.SovereigntyIndex",
    "主权指数": "Sancai.Di.Ethics.SovereigntyIndex",
    "SI =": "Sancai.Di.Ethics.SovereigntyIndex",
    "generalized_add": "Sancai.Di.Ethics.GeneralizedAdd",
    "广义加法": "Sancai.Di.Ethics.GeneralizedAdd",

    # 地层五行
    "wuxing_vector": "Sancai.Di.Wuxing.VectorMapping",
    "五行向量": "Sancai.Di.Wuxing.VectorMapping",
    "W(x)": "Sancai.Di.Wuxing.VectorMapping",
    "five_element": "Sancai.Di.Wuxing.RootMapping",
    "五行映射": "Sancai.Di.Wuxing.RootMapping",
    "hedge_index": "Sancai.Di.Wuxing.HedgeIndex",
    "五行对冲": "Sancai.Di.Wuxing.HedgeIndex",
    "cosine_sim": "Sancai.Di.Core.CosineSimilarity",
    "余弦相似": "Sancai.Di.Core.CosineSimilarity",

    # 人层人格
    "persona_superposition": "Sancai.Ren.Persona.Superposition",
    "人格叠加": "Sancai.Ren.Persona.Superposition",
    "bra_ket": "Sancai.Ren.Persona.Superposition",
    "persona_contribution": "Sancai.Ren.Persona.Contribution",
    "人格贡献": "Sancai.Ren.Persona.Contribution",
    "PC =": "Sancai.Ren.Persona.Contribution",
    "seven_dim": "Sancai.Ren.Persona.SevenDimBonus",
    "七维覆盖": "Sancai.Ren.Persona.SevenDimBonus",
    "activity_color": "Sancai.Ren.Persona.ActivityColor",
    "活跃度": "Sancai.Ren.Persona.ActivityColor",

    # 人层价值
    "contribution": "Sancai.Ren.Value.Contribution",
    "贡献值": "Sancai.Ren.Value.Contribution",
    "C = R": "Sancai.Ren.Value.Contribution",
    "weighted_utility": "Sancai.Ren.Value.WeightedUtility",
    "权重效用": "Sancai.Ren.Value.WeightedUtility",
    "V(P)": "Sancai.Ren.Value.WeightedUtility",
    "ete_translation": "Sancai.Ren.Value.ETE_Translation",
    "通心译": "Sancai.Ren.Value.ETE_Translation",
    "creator_royalty": "Sancai.Ren.Value.CreatorRoyalty",
    "创作收益": "Sancai.Ren.Value.CreatorRoyalty",

    # 人层伦理
    "human_bias": "Sancai.Ren.Ethics.HumanBias",
    "人性偏置": "Sancai.Ren.Ethics.HumanBias",
    "H_人性": "Sancai.Ren.Ethics.HumanBias",
}


def audit_scripts(verbose: bool = True) -> Dict:
    """审计 bin/ 下所有 Python 脚本的命名合规性"""
    results = {
        "total": 0,
        "has_sancai_ref": 0,
        "has_old_naming": 0,
        "missing": [],
        "details": [],
    }

    for py_file in sorted((ROOT / "bin").glob("lh_*.py")):
        results["total"] += 1
        try:
            content = py_file.read_text(encoding="utf-8")
        except Exception:
            continue

        # 检查是否有 Sancai.* 引用
        has_sancai = "Sancai." in content or "三才算法" in content
        if has_sancai:
            results["has_sancai_ref"] += 1

        # 检查是否有旧命名但无新命名
        old_matches = []
        for old_name, new_name in NAMING_MAP.items():
            if old_name in content and new_name not in content:
                old_matches.append((old_name, new_name))

        if old_matches and not has_sancai:
            results["has_old_naming"] += 1
            results["missing"].append({
                "file": str(py_file.relative_to(ROOT)),
                "old_names": [m[0] for m in old_matches[:5]],
                "suggested_sancai": [m[1] for m in old_matches[:5]],
            })

        if has_sancai:
            results["details"].append({
                "file": str(py_file.relative_to(ROOT)),
                "status": "✅ 已标注 Sancai.*",
            })
        elif old_matches:
            results["details"].append({
                "file": str(py_file.relative_to(ROOT)),
                "status": f"⚠️ 含旧命名 {len(old_matches)} 处·未标注 Sancai.*",
            })
        else:
            results["details"].append({
                "file": str(py_file.relative_to(ROOT)),
                "status": "— 无关脚本",
            })

    return results


def verify_international_mapping() -> Dict:
    """验证国际算法对照表完整性"""
    # 从标准文档中提取对照表
    standard_file = ROOT / "01_protocols" / "LH-SANCAI-ALGORITHM-UNIFIED-STANDARD-v3.0.md"
    if not standard_file.exists():
        return {"error": "标准文档未找到", "file": str(standard_file)}

    content = standard_file.read_text(encoding="utf-8")

    # 提取国际对照表条目
    international_pairs = []
    in_table = False
    header_passed = False
    for line in content.split("\n"):
        if "国际算法兼容对照表" in line:
            in_table = True
            header_passed = False
            continue
        if in_table and line.startswith("|") and "|" in line[1:]:
            parts = [p.strip() for p in line.split("|")]
            # 跳过表头和分隔行
            if not header_passed:
                if "国际算法" in line or "---" in line or "年份" in line:
                    header_passed = True
                    continue
            if header_passed and len(parts) >= 5:
                intl_name = parts[1]
                sancai_name = parts[2] if len(parts) > 2 else ""
                f_id = parts[3] if len(parts) > 3 else ""
                if intl_name and intl_name not in ("国际算法", "年份·作者", "------", ""):
                    international_pairs.append({
                        "international": intl_name,
                        "sancai": sancai_name,
                        "f_id": f_id,
                    })
        elif in_table and not line.startswith("|") and line.strip():
            if header_passed:
                in_table = False

    # 检查每对是否有对应的公式定义
    verified = []
    for pair in international_pairs:
        f_id = pair["f_id"]
        sancai_name = pair["sancai"]
        has_formula = False
        if f_id:
            has_formula = f"F{f_id}" in content or f_id in content
        verified.append({
            **pair,
            "formula_exists": has_formula,
        })

    return {
        "total_pairs": len(international_pairs),
        "pairs": verified,
        "all_verified": all(v["formula_exists"] for v in verified if v["f_id"]),
    }


def generate_report(audit_results: Dict, intl_results: Dict):
    """生成合规报告"""
    print(f"\n{'='*70}")
    print(f"🐉 三才算法命名合规报告 v1.0")
    print(f"DNA: {DNA}")
    print(f"{'='*70}")

    # 审计摘要
    print(f"\n📊 bin/ 脚本审计")
    print(f"{'─'*40}")
    print(f"  总脚本数: {audit_results['total']}")
    print(f"  已标注 Sancai.*: {audit_results['has_sancai_ref']}")
    print(f"  含旧命名未标注: {audit_results['has_old_naming']}")
    coverage = audit_results['has_sancai_ref'] / max(audit_results['total'], 1) * 100
    print(f"  覆盖率: {coverage:.0f}%")

    if audit_results["missing"]:
        print(f"\n⚠️ 需标注的脚本 (前10):")
        for item in audit_results["missing"][:10]:
            print(f"  {item['file']}")
            for i, old in enumerate(item["old_names"][:3]):
                print(f"    ↳ '{old}' → {item['suggested_sancai'][i]}")

    # 国际对照
    if "total_pairs" in intl_results:
        print(f"\n🌐 国际算法对照")
        print(f"{'─'*40}")
        print(f"  对照对数: {intl_results['total_pairs']}")
        all_ok = intl_results.get("all_verified", False)
        print(f"  全部验证: {'✅' if all_ok else '⚠️ 部分未验证'}")

    # 整体评级
    print(f"\n{'─'*40}")
    if coverage >= 80:
        print(f"  🟢 命名合规评级: 良好")
    elif coverage >= 50:
        print(f"  🟡 命名合规评级: 需改进")
    else:
        print(f"  🔴 命名合规评级: 急需统一")
    print(f"{'='*70}\n")


def main():
    parser = argparse.ArgumentParser(description="🐉 三才算法命名合规检查工具 v1.0")
    parser.add_argument("--audit", action="store_true", help="审计所有 bin/ 脚本")
    parser.add_argument("--report", action="store_true", help="生成合规报告")
    parser.add_argument("--verify-international", action="store_true", help="验证国际对照表")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")

    args = parser.parse_args()

    if not any([args.audit, args.report, args.verify_international]):
        args.report = True

    audit_results = {}
    intl_results = {}

    if args.audit or args.report:
        audit_results = audit_scripts(verbose=not args.json)

    if args.verify_international or args.report:
        intl_results = verify_international_mapping()

    if args.json:
        output = {
            "audit": audit_results,
            "international": intl_results,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    elif args.report:
        generate_report(audit_results, intl_results)
    elif args.audit:
        generate_report(audit_results, intl_results)
    elif args.verify_international:
        print(json.dumps(intl_results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
