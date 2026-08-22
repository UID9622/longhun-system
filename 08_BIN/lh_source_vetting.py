#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂·数据源头校验器 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·庚午·䷝离为火-源头校验-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：任何数据进系统前，先过本源审查。
核心理念：人永远是1 — 数据只是后面的0，没有1，再多的0也没意义。

底座铁律落地执行层——不再是文档里一句话，是可执行的代码。
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# ──── 常量 ────
CST = timezone(timedelta(hours=8))
DNA_ROOT = "#龍芯⚡️丙午·乙未·甲辰·庚午·䷝离为火-源头校验-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SCORE_THRESHOLD = 80  # 低于80分 = 拒绝或人工复核

# ──── 源头校验检查表（五问·覆盖利益对齐全维度）────
SOURCE_CHECKLIST: Dict[str, Dict[str, Any]] = {
    "利益对齐": {
        "问题": "这个数据源/模型最初是为了服务谁的利益？",
        "必须回答": ["使用者", "公众", "长期福祉", "老百姓", "用户利益"],
        "禁止回答": ["股东回报", "季度利润", "参与度", "留存率", "DAU", "MAU", "广告收入"],
    },
    "核心指标": {
        "问题": "核心指标是否与那个利益真正对齐？",
        "必须回答": ["生活改善", "知识传递", "能力提升", "解决问题", "真实需求"],
        "禁止回答": ["转化率", "点击量", "停留时间", "GMV", "漏斗", "拉新"],
    },
    "利益冲突": {
        "问题": "这个设计中有没有内嵌的利益冲突？",
        "必须回答": ["无", "已公开披露", "透明"],
        "禁止回答": ["商业机密", "不方便说", "内部决策"],
    },
    "修改权限": {
        "问题": "谁有权修改这个系统的目标函数？",
        "必须回答": ["独立监督机构", "用户代表", "公开审议", "社区治理"],
        "禁止回答": ["内部产品经理", "单方面决定", "老板拍板"],
    },
    "监督机制": {
        "问题": "修改需要经过谁的同意？",
        "必须回答": ["独立评审", "公示期", "可申诉", "审计"],
        "禁止回答": ["内部流程", "上级批准", "无需审批"],
    },
}


def _now() -> str:
    return datetime.now(CST).isoformat()


def _dna_hash(candidates: str) -> str:
    """生成 16 位追溯哈希。"""
    return hashlib.sha256(candidates.encode("utf-8")).hexdigest()[:16]


def _audit_dir() -> Path:
    """审计日志目录: ~/.longhun/audit/"""
    p = Path.home() / ".longhun" / "audit"
    p.mkdir(parents=True, exist_ok=True)
    return p


def check_source(source_name: str, source_description: str, source_origin: str) -> dict:
    """
    对数据源进行源头校验。

    返回:
        {
            "passed": bool,
            "failures": [{项, 问题, 原因}],
            "score": int (0-100),
            "warnings": [{项, 原因}],
        }
    """
    failures: List[Dict[str, str]] = []
    warnings: List[Dict[str, str]] = []
    passed_count = 0
    total_count = len(SOURCE_CHECKLIST)

    text = f"{source_name} {source_description} {source_origin}"

    for key, item in SOURCE_CHECKLIST.items():
        # 检查「禁止回答」
        banned_hits = [w for w in item["禁止回答"] if w.lower() in text.lower()]
        # 检查「必须回答」
        required_hits = [w for w in item["必须回答"] if w.lower() in text.lower()]

        if banned_hits:
            failures.append({
                "项": key,
                "问题": item["问题"],
                "原因": f"包含禁止词: {banned_hits}",
            })
        elif not required_hits:
            # 没有禁止词但也没有必须词 → 警告（不是硬失败，但需要人工复核）
            warnings.append({
                "项": key,
                "问题": item["问题"],
                "原因": f"未包含必须词: {item['必须回答']}",
            })
            passed_count += 0.5  # 警告项给半分
        else:
            passed_count += 1

    # 存在硬失败 → 直接拒绝
    has_hard_fail = len(failures) > 0
    passed = not has_hard_fail
    score = int((passed_count / total_count) * 100)

    return {
        "passed": passed,
        "failures": failures,
        "warnings": warnings,
        "score": score,
        "source_name": source_name,
    }


def audit_source(source_name: str, description: str, origin: str) -> dict:
    """执行审计并记录到审计链。"""
    result = check_source(source_name, description, origin)

    timestamp = _now()
    dna = f"#龍芯⚡️{datetime.now(CST).strftime('%Y%m%d')}-源头校验-{_dna_hash(f'{source_name}{timestamp}{result['score']}')}"

    # 写入审计日志（append-only）
    audit_log = _audit_dir() / "source_vetting.jsonl"
    record = {
        **result,
        "timestamp": timestamp,
        "dna": dna,
        "source_origin": origin,
        "description": description,
    }
    with open(audit_log, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    result["dna"] = dna
    result["timestamp"] = timestamp
    return result


def _print_report(result: dict) -> None:
    """格式化打印校验报告。"""
    width = 60
    print(f"\n{'='*width}")
    print(f"🔍 龍魂源头校验报告: {result['source_name']}")
    print(f"{'='*width}")

    status = "✅ 通过" if result["passed"] else "❌ 拒绝"
    print(f"状态: {status}")
    print(f"本源分: {result['score']}/100")
    print(f"DNA: {result.get('dna', '')}")

    if result.get("failures"):
        print(f"\n🚫 硬性未通过项（必须修复）:")
        for f in result["failures"]:
            print(f"  ▸ {f['项']}: {f['问题']}")
            print(f"    原因: {f['原因']}")

    if result.get("warnings"):
        print(f"\n🟡 警告项（建议人工复核）:")
        for w in result["warnings"]:
            print(f"  ▸ {w['项']}: {w['问题']}")
            print(f"    原因: {w['原因']}")

    print(f"{'='*width}\n")


def check_before_distill(source_name: str, source_desc: str, source_origin: str, threshold: int = SCORE_THRESHOLD) -> bool:
    """
    蒸馏前先过源头校验。任何蒸馏操作必须调用此函数。

    参数:
        source_name: 数据源名称（如 "DeepSeek-R1"）
        source_desc: 数据源描述
        source_origin: 来源/版权方
        threshold: 本源分阈值（默认80）

    返回:
        True = 通过，可蒸馏
        False = 拒绝，禁止蒸馏
    """
    result = audit_source(source_name, source_desc, source_origin)

    if not result["passed"]:
        print(f"\n❌ 蒸馏拒绝：源头校验未通过")
        print(f"   数据源: {source_name}")
        print(f"   本源分: {result['score']}/{threshold}")
        print(f"   硬性失败项:")
        for f in result.get("failures", []):
            print(f"     ▸ {f['项']}: {f['原因']}")
        return False

    if result["score"] < threshold:
        print(f"\n🟡 蒸馏警告：本源分 {result['score']} 低于 {threshold} 分阈值")
        print(f"   数据源: {source_name}")
        print(f"   建议: 人工复核后再决定是否蒸馏")
        for w in result.get("warnings", []):
            print(f"     ▸ {w['项']}: {w['原因']}")
        print("   ⚠️  继续执行需人工确认（设置环境变量 LH_DISTILL_FORCE=1 跳过警告）")
        if os.environ.get("LH_DISTILL_FORCE") != "1":
            return False

    print(f"✅ 源头校验通过: {source_name} · 本源分 {result['score']}/100 · DNA {result.get('dna', '')}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="龍魂数据源头校验器 — 人永远是1",
        epilog=f"{DNA_ROOT}\n{CONFIRM}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--source", required=True, help="数据源名称")
    parser.add_argument("--desc", required=True, help="数据源描述")
    parser.add_argument("--origin", required=True, help="数据来源/版权方")
    parser.add_argument("--json", action="store_true", help="以JSON格式输出")
    parser.add_argument("--threshold", type=int, default=SCORE_THRESHOLD, help=f"本源分阈值（默认{SCORE_THRESHOLD}）")
    args = parser.parse_args()

    result = audit_source(args.source, args.desc, args.origin)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _print_report(result)

    # 退出码：未通过 → 1，警告但通过 → 0，通过 → 0
    if not result["passed"]:
        sys.exit(1)
    if result["score"] < args.threshold:
        print(f"🟡 警告：本源分 {result['score']} 低于阈值 {args.threshold}，建议人工复核后决定是否继续。\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
