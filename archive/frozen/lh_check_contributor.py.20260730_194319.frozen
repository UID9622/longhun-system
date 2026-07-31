#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·底线三：不让付出者寒心 检测引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-CHECK-CONTRIBUTOR-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

检测分配模型，确保所有付出者的劳动被记账、回报被兑现。
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

SYSTEM_ROOT = Path(__file__).parent.parent

# 寒心叙事模式
COLD_HEART_PATTERNS = [
    (r"好人.*必须穷|好人.*一生.*穷", "🔴", "好人=穷绑定"),
    (r"奉献.*必须苦|贡献.*不能.*回报", "🔴", "奉献=苦绑定"),
    (r"英雄.*必须死|英雄.*流血.*流泪", "🔴", "英雄=死绑定"),
    (r"捐款.*吃泡面|慈善.*穷困", "🟡", "苦情捐款叙事"),
    (r"科学家.*住平房|科学家.*买不起", "🟡", "苦情科学家叙事"),
    (r"环卫工人.*省吃俭用|清洁工.*为了.*攒", "🟡", "苦情劳动者叙事"),
    (r"牺牲.*穷人|穷人.*承担", "🔴", "牺牲绑定穷人"),
    (r"付出.*不能.*正常生活|付出者.*没有.*好报", "🟡", "付出=牺牲正常生活"),
    (r"过得好.*不能.*奉献|有钱.*就不.*善良", "🟡", "过得好≠能奉献"),
    (r"开源.*白嫖|免费.*应当|伸手.*理所应当", "🔴", "开源=白嫖"),
    (r"contributor.*unpaid|贡献者.*无偿|志愿.*活该", "🔴", "贡献者无偿劳动"),
    (r"没人.*感谢|没人.*记得|被遗忘.*付出", "🟡", "付出被遗忘叙事"),
]

EXCLUDED = {
    "bin/lh_check_contributor.py",
    "bin/lh_deben_audit.py",
    "01_protocols/LH-DEBEN-AUDIT-v1.0.md",
}


class ContributorChecker:
    """不让付出者寒心 — 底线3检测"""

    def __init__(self, root: Path = SYSTEM_ROOT):
        self.root = root

    def check(self) -> Dict[str, Any]:
        hits = []
        files_scanned = 0

        for f in self.root.rglob("*"):
            if f.suffix not in (".py", ".md", ".html", ".js", ".sh"):
                continue
            rel = str(f.relative_to(self.root))
            if rel in EXCLUDED:
                continue
            if any(rel.startswith(d) for d in ["_archive/", "_work/", "models/", "data/training/", "docs/"]):
                continue

            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                files_scanned += 1
                for pattern, severity, label in COLD_HEART_PATTERNS:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        hits.append({
                            "file": rel,
                            "pattern": pattern,
                            "severity": severity,
                            "label": label,
                            "matches": len(matches),
                        })
            except Exception:
                pass

        red = sum(1 for h in hits if h["severity"] == "🔴")
        yellow = sum(1 for h in hits if h["severity"] == "🟡")

        if red > 0:
            status = "🔴"
            verdict = f"触碰{red}条寒心叙事红线"
        elif yellow > 0:
            status = "🟡"
            verdict = f"发现{yellow}条寒心叙事警告"
        else:
            status = "🟢"
            verdict = "不让付出者寒心 — 通过"

        return {
            "底线": "不让付出者寒心",
            "状态": status,
            "判定": verdict,
            "扫描文件": files_scanned,
            "命中": len(hits),
            "🔴": red,
            "🟡": yellow,
            "详情": hits[:20],
        }


if __name__ == "__main__":
    checker = ContributorChecker()
    result = checker.check()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["状态"] == "🟢" else 1)
