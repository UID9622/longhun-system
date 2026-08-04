#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂技能自评 / 模块反馈机制
每个技能输出自己的“存在感、健康度、孤独度、建议”。

DNA: #龍芯⚡️2026-06-23-LONGHUN-MODULE-SELF-ASSESSMENT-v1.0
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from skills.registry import LonghunSkillRegistry


def _score_skill(sk: Dict[str, Any]) -> Dict[str, Any]:
    score = 0
    notes = []
    scripts = sk.get("scripts", [])

    if sk.get("description") and sk["description"] != sk["id"]:
        score += 20
    else:
        notes.append("描述缺失")

    if sk.get("version") and sk["version"] != "unknown":
        score += 20
    else:
        notes.append("版本未声明")

    if sk.get("dna"):
        score += 20
    else:
        notes.append("DNA 未提取")

    if scripts:
        score += min(len(scripts) * 10, 30)
    else:
        notes.append("无可执行脚本（纯文档/语义技能）")

    # 可执行性加权
    sk_type = sk.get("type", "")
    if sk_type in ("python", "mixed"):
        score += 10
    elif sk_type == "html":
        score += 5

    # 健康评级
    if score >= 85:
        health = "🟢 健康"
    elif score >= 60:
        health = "🟡 可用但需补全"
    else:
        health = "🔴 需关注"

    # 孤独度：外部 longhun-* 若无脚本，容易被冷落
    loneliness = "高" if (sk.get("source") == "external" and not scripts) else "中" if not scripts else "低"

    # 建议
    if not scripts:
        recommendation = "建议补充 CLI/API 入口，或接入语义调度层避免被冷落"
    elif score < 60:
        recommendation = "建议补全 SKILL.md 元数据（版本、描述、DNA）"
    elif sk.get("cloud_port"):
        recommendation = f"云端技能，建议通过端口 {sk['cloud_port']} 接入统一代理"
    else:
        recommendation = "状态良好，保持使用并定期反馈"

    return {
        "id": sk["id"],
        "name": sk["name"],
        "source": sk.get("source"),
        "type": sk_type,
        "version": sk.get("version"),
        "scripts_count": len(scripts),
        "score": score,
        "health": health,
        "loneliness": loneliness,
        "recommendation": recommendation,
        "notes": notes,
    }


def assess_all() -> Dict[str, Any]:
    registry = LonghunSkillRegistry()
    items = [_score_skill(sk) for sk in registry.list_skills()]
    items.sort(key=lambda x: x["score"], reverse=True)

    total = len(items)
    healthy = sum(1 for i in items if i["health"].startswith("🟢"))
    warning = sum(1 for i in items if i["health"].startswith("🟡"))
    critical = sum(1 for i in items if i["health"].startswith("🔴"))

    return {
        "total": total,
        "healthy": healthy,
        "warning": warning,
        "critical": critical,
        "skills": items,
        "dna": "#龍芯⚡️2026-06-23-LONGHUN-MODULE-SELF-ASSESSMENT-v1.0",
    }


def main():
    report = assess_all()
    out = ROOT / "docs" / "module-self-assessment.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[模块自评] 共评估 {report['total']} 个技能")
    print(f"  🟢 健康: {report['healthy']}  🟡 警告: {report['warning']}  🔴 需关注: {report['critical']}")
    print(f"[模块自评] 报告已保存: {out}")


if __name__ == "__main__":
    main()
