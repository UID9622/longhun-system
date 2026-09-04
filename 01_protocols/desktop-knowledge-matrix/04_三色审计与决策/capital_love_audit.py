# P0焊死: 本文件为龍魂体系P0级文档·不可修改·不可绕过（上位文档 LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md）
# License: CC BY-NC-SA 4.0（核心思想层·代码层为 MulanPSL v2·详见 LH-LAYERED-LICENSE-v1.0）
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ 龍魂资本愛之审计引擎 · Capital Love Audit Engine v1.0
DNA: #龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-CAPITAL-LOVE-AUDIT-ENGINE-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

依据: L8_治理层/governance/CAPITAL_LOVE_AUDIT_PROTOCOL.md (CLAP v1.0)

任务:
  1. 对资本实体执行愛之七维审计评分
  2. 自动判定准入资格（🟢/🟡/🟠/🔴）
  3. 结果写入审计日志（append-only jsonl）
  4. 对不达标的实体生成冻结/禁入指令
  5. 支持人工复核召

用法:
  python capital_love_audit.py --audit entity.json      # 审计单个实体
  python capital_love_audit.py --report                  # 生成本季度报告
  python capital_love_audit.py --list-banned             # 列禁入名单
  python capital_love_audit.py --check entity_id         # 检查特定实体
"""

import json
import os
import sys
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ============================================================
# 配置
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
AUDIT_ROOT = Path(__file__).resolve().parent

DNA = "#龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-CAPITAL-LOVE-AUDIT-ENGINE-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"

AUDIT_LOG = Path.home() / ".longhun" / "audit" / "capital_love_audit.jsonl"
AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)

BANNED_LIST = Path.home() / ".longhun" / "audit" / "capital_banned.json"
REPORT_DIR = AUDIT_ROOT / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 七维审计矩阵
# ============================================================

# 满分70，及格42
SCORE_WEIGHTS = {
    "social_good": 2,        # 社会公益 ×2
    "worker_dignity": 2,     # 劳动者尊严 ×2
    "tech_for_good": 2,      # 技术向善 ×2
    "national_loyalty": 1,   # 国家忠诚 ×1
    "user_sovereignty": 1,   # 用户主权 ×1
    "transparency": 1,       # 透明审计 ×1
    "historical_clean": 1,   # 历史清白 ×1
}

DIMENSION_LABELS = {
    "social_good": "社会公益",
    "worker_dignity": "劳动者尊严",
    "tech_for_good": "技术向善",
    "national_loyalty": "国家忠诚",
    "user_sovereignty": "用户主权",
    "transparency": "透明审计",
    "historical_clean": "历史清白",
}

MAX_RAW_SCORE = 70  # 7维 × 10分 × 权重求和

# 判定阈值
THRESHOLD_GREEN = 56   # ≥56 → 绿色通道
THRESHOLD_YELLOW = 42  # ≥42 → 有条件准入
THRESHOLD_ORANGE = 28  # ≥28 → 限期整改
# <28 → 永久禁入


def compute_love_score(scores: Dict[str, int]) -> Tuple[int, Dict[str, int], str]:
    """计算加权愛之审计分数."""
    weighted_scores = {}
    total = 0
    for dim, weight in SCORE_WEIGHTS.items():
        raw = scores.get(dim, 0)
        raw = max(0, min(10, raw))
        w = raw * weight
        weighted_scores[dim] = w
        total += w
    return total, weighted_scores, get_tier(total)


def get_tier(score: int) -> str:
    """返回准入等级."""
    if score >= THRESHOLD_GREEN:
        return "GREEN"    # 🟢 绿色通道
    elif score >= THRESHOLD_YELLOW:
        return "YELLOW"   # 🟡 有条件准入
    elif score >= THRESHOLD_ORANGE:
        return "ORANGE"   # 🟠 限期整改
    else:
        return "RED"      # 🔴 永久禁入


def generate_dna_trace(entity_id: str, action: str) -> str:
    """生成操作DNA追溯码."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    raw = f"{entity_id}-{action}-{ts}-{SEAL}"
    h = hashlib.sha256(raw.encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-CLAP-{action}-{h}"


def audit_to_log(entry: Dict[str, Any], log_path: Path = AUDIT_LOG):
    """追加式审计日志."""
    entry["_timestamp"] = datetime.now(timezone.utc).isoformat()
    entry["_dna"] = generate_dna_trace(entry.get("entity_id", "UNKNOWN"), "AUDIT")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def ban_entity(entity: Dict[str, Any]):
    """将实体加入永久禁入名单."""
    bans = []
    if BANNED_LIST.exists():
        with open(BANNED_LIST, "r", encoding="utf-8") as f:
            bans = json.load(f)
    bans.append({
        "entity_id": entity.get("entity_id"),
        "entity_name": entity.get("entity_name", "未命名"),
        "banned_at": datetime.now(timezone.utc).isoformat(),
        "reason": "愛之审计未通过（<28分）",
        "score": entity.get("total_score"),
        "dna": generate_dna_trace(entity.get("entity_id", "UNKNOWN"), "BAN"),
        "permanent": True,
    })
    with open(BANNED_LIST, "w", encoding="utf-8") as f:
        json.dump(bans, f, ensure_ascii=False, indent=2)


def freeze_entity(entity: Dict[str, Any]):
    """生成冻结指令."""
    freeze_instruction = {
        "entity_id": entity.get("entity_id"),
        "entity_name": entity.get("entity_name", "未命名"),
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "score": entity.get("total_score"),
        "tier": entity.get("tier"),
        "action_required": "限期整改，重新审计",
        "deadline_days": 90,
        "dna": generate_dna_trace(entity.get("entity_id", "UNKNOWN"), "FREEZE"),
    }
    audit_to_log(freeze_instruction)
    return freeze_instruction


# ============================================================
# 审计执行
# ============================================================

def audit_entity(entity_data: Dict[str, Any]) -> Dict[str, Any]:
    """对单个资本实体执行愛之审计."""
    entity_id = entity_data.get("entity_id", "UNKNOWN")
    scores = entity_data.get("scores", entity_data.get("love_scores", {}))

    total, weighted, tier = compute_love_score(scores)

    result = {
        "entity_id": entity_id,
        "entity_name": entity_data.get("entity_name", "未命名"),
        "entity_type": entity_data.get("entity_type", "capital"),
        "total_score": total,
        "max_score": MAX_RAW_SCORE,
        "weighted_scores": weighted,
        "raw_scores": scores,
        "tier": tier,
        "tier_emoji": {"GREEN": "🟢", "YELLOW": "🟡", "ORANGE": "🟠", "RED": "🔴"}[tier],
        "entry_decision": {
            "GREEN": "准许进入·绿色通道",
            "YELLOW": "有条件准入·附加条款约束",
            "ORANGE": "限期整改·重新审计后方可进入",
            "RED": "永久禁入·加入黑名单",
        }[tier],
        "dimension_details": {
            dim: {
                "raw": scores.get(dim, 0),
                "weighted": weighted.get(dim, 0),
                "label": DIMENSION_LABELS[dim],
                "weight": SCORE_WEIGHTS[dim],
            }
            for dim in SCORE_WEIGHTS
        },
    }

    # 写入审计日志
    audit_to_log(result)

    # 处理判定结果
    if tier == "RED":
        ban_entity(result)
        result["action"] = "BANNED_PERMANENTLY"
    elif tier == "ORANGE":
        freeze_info = freeze_entity(result)
        result["action"] = "FROZEN_PENDING_REMEDIATION"
        result["freeze_details"] = freeze_info
    elif tier == "YELLOW":
        result["action"] = "CONDITIONAL_ENTRY"
        result["conditions"] = [
            "签署完整龍魂协议",
            "接入DNA追溯链",
            "接受季度三色审计",
            "利润上限锁定条款生效",
        ]
    else:
        result["action"] = "GREEN_ENTRY"
        result["conditions"] = [
            "签署基本龍魂协议",
            "接入DNA追溯链",
        ]

    return result


def list_banned_entities() -> List[Dict[str, Any]]:
    """列出所有禁入实体."""
    if not BANNED_LIST.exists():
        return []
    with open(BANNED_LIST, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_quarterly_report(output_path: Optional[Path] = None):
    """生成本季度审计报告."""
    if not AUDIT_LOG.exists():
        return {"error": "无审计日志", "total_audits": 0}

    entries = []
    with open(AUDIT_LOG, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))

    banned = list_banned_entities()

    tiers = {"GREEN": 0, "YELLOW": 0, "ORANGE": 0, "RED": 0}
    for e in entries:
        tiers[e.get("tier", "UNKNOWN")] = tiers.get(e.get("tier", "UNKNOWN"), 0) + 1

    report = {
        "report_title": "龍魂资本愛之审计·季度报告",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "protocol_version": "CLAP v1.0",
        "total_audits": len(entries),
        "tier_distribution": tiers,
        "banned_count": len(banned),
        "banned_entities": banned,
        "dna": generate_dna_trace("QUARTERLY", "REPORT"),
    }

    path = output_path or REPORT_DIR / f"capital_love_audit_report_{datetime.now().strftime('%Y%m%d')}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return report


# ============================================================
# 自我校验
# ============================================================

def self_verify() -> Dict[str, Any]:
    """引擎自我校验."""
    return {
        "engine": "资本愛之审计引擎",
        "version": "v1.0",
        "dna": DNA,
        "confirm": CONFIRM[:16] + "...",  # 不完整输出
        "seal": SEAL[:16] + "...",
        "protocol": "CLAP v1.0",
        "audit_log": str(AUDIT_LOG),
        "banned_list": str(BANNED_LIST),
        "log_exists": AUDIT_LOG.exists(),
        "banned_list_exists": BANNED_LIST.exists(),
        "status": "🟢 ACTIVE",
    }


# ============================================================
# CLI
# ============================================================

def print_banner():
    print("""
╔══════════════════════════════════════════════════════════╗
║        🛡️  龍魂资本愛之审计引擎 CLAP v1.0  🛡️        ║
║  Capital Love Audit Engine                              ║
║  得罪少数人 · 造福14亿人                                  ║
╚══════════════════════════════════════════════════════════╝
""")


def print_audit_result(result: Dict[str, Any]):
    """格式化输出审计结果."""
    tier_e = result["tier_emoji"]
    print(f"\n{'='*60}")
    print(f"  {tier_e} 实体: {result['entity_name']} ({result['entity_id']})")
    print(f"  愛之分: {result['total_score']}/{result['max_score']}")
    print(f"  判定: {result['tier']} → {result['entry_decision']}")
    print(f"  操作: {result.get('action', 'N/A')}")
    print(f"{'='*60}")
    print(f"\n  各维度得分:")
    for dim, detail in result.get("dimension_details", {}).items():
        bar = "█" * detail["raw"] + "░" * (10 - detail["raw"])
        print(f"    {detail['label']:　<6s} [{bar}] {detail['raw']}/10 (加权={detail['weighted']})")

    if result.get("conditions"):
        print(f"\n  📋 准入条件:")
        for c in result["conditions"]:
            print(f"     • {c}")

    if result.get("freeze_details"):
        fd = result["freeze_details"]
        print(f"\n  🧊 冻结详情:")
        print(f"     整改期限: {fd['deadline_days']}天")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂资本愛之审计引擎 CLAP v1.0")
    parser.add_argument("--audit", type=str, help="审计实体 JSON 文件路径")
    parser.add_argument("--report", action="store_true", help="生成本季度报告")
    parser.add_argument("--list-banned", action="store_true", help="列出禁入名单")
    parser.add_argument("--verify", action="store_true", help="引擎自检")
    args = parser.parse_args()

    print_banner()

    if args.verify:
        result = self_verify()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.list_banned:
        banned = list_banned_entities()
        if not banned:
            print("  🟢 禁入名单为空。")
        else:
            print(f"  🔴 禁入实体: {len(banned)}个\n")
            for b in banned:
                print(f"    • {b['entity_name']} (ID:{b['entity_id']}) — {b['banned_at'][:10]}")
        return

    if args.audit:
        with open(args.audit, "r", encoding="utf-8") as f:
            entity = json.load(f)
        result = audit_entity(entity)
        print_audit_result(result)
        return

    if args.report:
        report = generate_quarterly_report()
        if "error" in report:
            print(f"  ⚠️ {report['error']}")
        else:
            print(f"  📊 季度报告已生成")
            print(f"  总审计数: {report['total_audits']}")
            dist = report['tier_distribution']
            print(f"  🟢{dist.get('GREEN',0)} 🟡{dist.get('YELLOW',0)} 🟠{dist.get('ORANGE',0)} 🔴{dist.get('RED',0)}")
            print(f"  禁入名单: {report['banned_count']}个")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
