#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·庚戌·巳时·需-PUBLIC-EXPRESSION-AUDIT-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
lh_public_expression_audit — 龍魂公开表述审计引擎 v1.0

扫描系统中所有公开面向的内容（文章、知识图谱、协议文档、网页文案），
检测是否存在"好人=穷""奉献=苦""英雄=死"等寒心叙事。

来源: UID9622《别再加戏了》《地道战与"地道战"》
DNA: #龍芯⚡️丙午·乙未·庚戌·巳时·需-PUBLIC-EXPRESSION-AUDIT-v1.0

用法:
  python3 bin/lh_public_expression_audit.py scan         # 扫描所有公开内容
  python3 bin/lh_public_expression_audit.py report       # 生成报告
  python3 bin/lh_public_expression_audit.py rules        # 显示审计规则
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ============================================================
# 寒心叙事检测规则
# ============================================================

# 核心有害叙事（必须杜绝的）
CORE_HARMFUL_NARRATIVES: List[Tuple[str, str, str, str]] = [
    # (正则模式, 严重度, 标签, 说明)
    (r"好人.*必须穷", "🔴", "好人=穷绑定", "把付出和贫穷强行焊死"),
    (r"好人.*穷人", "🔴", "好人=穷人", "暗示好人就该是穷人"),
    (r"奉献.*必须苦", "🔴", "奉献=苦绑定", "把奉献和痛苦强行绑定"),
    (r"英雄.*必须死", "🔴", "英雄=死绑定", "暗示英雄只有牺牲一条路"),
    (r"有钱.*有罪|赚钱.*不道德", "🔴", "有钱=有罪", "把财富与道德对立"),
    (r"舒服.*不真诚|享受.*不纯洁", "🟡", "舒服=虚伪", "暗示过得好就是假"),
    (r"活着.*不够伟大", "🟡", "活着≠伟大", "暗示不死就不够伟大"),
]

# 苦情叙事（可能存在的）
SUFFERING_NARRATIVES: List[Tuple[str, str, str, str]] = [
    (r"捐款.*吃泡面", "🟡", "捐款=卖惨", "将捐款与苦难生活绑定"),
    (r"科学家.*住平房", "🟡", "科学家=穷", "将科学家与贫穷绑定"),
    (r"环卫工人.*省吃俭用.*捐款", "🟡", "底层=牺牲", "消费底层劳动者的奉献"),
    (r"省吃俭用.*捐款", "🟡", "省吃俭用捐款", "苦情捐款叙事"),
    (r"自己却吃泡面", "🟡", "吃泡面叙事", "把苦难当美德宣传"),
    (r"奖金全捐了", "🟡", "全捐叙事", "暗示奉献=倾尽所有"),
]

# 付出=牺牲叙事
SACRIFICE_NARRATIVES: List[Tuple[str, str, str, str]] = [
    (r"付出.*牺牲", "🟡", "付出=牺牲", "把付出和牺牲等同"),
    (r"奉献.*不能.*正常生活", "🟡", "奉献≠正常生活", "暗示奉献者不该过正常生活"),
    (r"过得好.*不能.*奉献", "🟡", "过得好≠奉献", "暗示享受生活的人不配奉献"),
    (r"付出.*成本太高", "🟡", "付出成本高", "暗示付出要付出巨大代价"),
]

# 为你好绑架
FOR_YOUR_OWN_GOOD: List[Tuple[str, str, str, str]] = [
    (r"为你好.*审查", "🔴", "\u201c为你好\u201d审查", "用为你好之名行审查之实"),
    (r"为你好.*限制", "🔴", "\u201c为你好\u201d限制", "用为你好之名行限制之实"),
    (r"为你好.*隐私", "🔴", "\u201c为你好\u201d侵犯隐私", "用为你好之名侵犯隐私"),
    (r"这是为你好", "🟡", "\u201c为你好\u201d万能盾牌", "为你好不能成为万能理由"),
]

# 但这些都是批评性的引用 — 需要区分"宣扬"和"批判"
# 关键: 如果文章本身是在批判这种叙事，则不算违规
CRITICAL_CONTEXT_SIGNALS: List[str] = [
    r"这不是|这是把|这他妈|这逻辑有|这套叙事|寒心|蠢|有毒|问题",
    r"不能这样|不应该|凭什么|谁还愿意",
    r"把.*焊死|绑死|绑定",
]

# 需要扫描的目录
SCAN_DIRS = [
    "03_知識圖譜",
    "01_protocols",
    "02_rules",
    "articles",
    "docs",
    "web",
    "web_apps",
    "portal",
    "data/sources/fetched",
    "data/sources/cleaned",
    "papers",
]

# 忽略目录
IGNORE_IN_SCAN = {"__pycache__", ".git", "node_modules", "venv", "tmp"}


class PublicExpressionAuditor:
    """公开表述审计器"""

    def __init__(self, root: Path = None):
        self.root = root or PROJECT_ROOT
        self.findings: List[Dict[str, Any]] = []
        self.stats: Dict[str, int] = defaultdict(int)

    def _is_critical_context(self, line: str, match_start: int, filepath: Path) -> bool:
        """判断命中行是否在批判语境中"""
        rel_path = str(filepath)

        # 1) data/sources 中的训练数据都是批判性文章本体
        if "data/sources/" in rel_path:
            return True

        # 2) 论文/协议文档是UID9622本人写的分析性文档
        if "01_protocols/" in rel_path and "THESIS" in rel_path.upper():
            return True

        # 3) 文件名含批判关键词
        fname = filepath.name.lower()
        critical_file_keywords = ["别再加戏", "地道战", "寒心", "评论战场", "离火运", "浮躁"]
        if any(kw in fname for kw in critical_file_keywords):
            return True

        # 4) 取匹配位置前后100个字符检查批判信号
        start = max(0, match_start - 100)
        end = min(len(line), match_start + 150)
        context = line[start:end]

        for sig in CRITICAL_CONTEXT_SIGNALS:
            if re.search(sig, context):
                return True
        return False

    def scan_file(self, filepath: Path) -> List[Dict[str, Any]]:
        """扫描单个文件"""
        findings = []
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except Exception:
            return findings

        all_patterns = (
            [(p, s, l, d, "核心有害") for p, s, l, d in CORE_HARMFUL_NARRATIVES]
            + [(p, s, l, d, "苦情叙事") for p, s, l, d in SUFFERING_NARRATIVES]
            + [(p, s, l, d, "付出=牺牲") for p, s, l, d in SACRIFICE_NARRATIVES]
            + [(p, s, l, d, "为你好绑架") for p, s, l, d in FOR_YOUR_OWN_GOOD]
        )

        for i, line in enumerate(lines, 1):
            for pattern, severity, label, desc, category in all_patterns:
                for match in re.finditer(pattern, line, re.IGNORECASE):
                    is_critical = self._is_critical_context(line, match.start(), filepath)
                    findings.append({
                        "文件": str(filepath.relative_to(self.root)),
                        "行号": i,
                        "匹配文本": line.strip()[:120],
                        "模式": pattern,
                        "严重度": severity,
                        "标签": label,
                        "说明": desc,
                        "分类": category,
                        "批判语境": is_critical,
                        "实际风险": "🟢 批判性引用·非违规" if is_critical else severity,
                    })

        return findings

    def scan_all(self) -> List[Dict[str, Any]]:
        """扫描所有公开内容"""
        self.findings = []

        for scan_dir in SCAN_DIRS:
            dir_path = self.root / scan_dir
            if not dir_path.exists():
                continue

            for root, dirs, files in os.walk(dir_path):
                dirs[:] = [d for d in dirs if d not in IGNORE_IN_SCAN and not d.startswith(".")]

                for fname in files:
                    if not fname.endswith((".md", ".html", ".txt", ".jsonl", ".py")):
                        continue
                    fpath = Path(root) / fname
                    findings = self.scan_file(fpath)
                    self.findings.extend(findings)

        # 统计
        self.stats["扫描文件总数"] = len(set(f["文件"] for f in self.findings)) if self.findings else 0
        self.stats["命中总数"] = len(self.findings)
        self.stats["核心有害(实际风险)"] = len([
            f for f in self.findings
            if f["分类"] == "核心有害" and f["实际风险"] in ("🔴", "🟡")
        ])
        self.stats["批判性引用(安全)"] = len([
            f for f in self.findings if f["批判语境"]
        ])

        return self.findings

    def generate_report(self) -> str:
        """生成审计报告"""
        lines = []
        lines.append("=" * 60)
        lines.append("  🐉 龍魂公开表述审计报告")
        lines.append("  离火运底线3: 不让付出者寒心")
        lines.append("  DNA: #龍芯⚡️丙午·乙未·庚戌·巳时·需-PUBLIC-EXPR-v1.0")
        lines.append("=" * 60)
        lines.append("")

        # 统计
        lines.append("## 统计")
        for k, v in sorted(self.stats.items()):
            lines.append(f"  - {k}: {v}")
        lines.append("")

        # 高风险（非批判语境）
        real_risks = [
            f for f in self.findings
            if not f["批判语境"] and f["严重度"] in ("🔴", "🟡")
        ]

        if real_risks:
            lines.append("## ⚠️ 实际风险项（非批判性引用·需处理）")
            lines.append("")
            for f in sorted(real_risks, key=lambda x: x["严重度"], reverse=True):
                lines.append(f"  {f['严重度']} [{f['标签']}] {f['文件']}:{f['行号']}")
                lines.append(f"     > {f['匹配文本']}")
                lines.append("")
        else:
            lines.append("## ✅ 无实际风险")
            lines.append("  所有命中项均为批判性引用（文章在批判寒心叙事，而非宣扬）。")
            lines.append("")

        # 批判性引用
        critical_refs = [f for f in self.findings if f["批判语境"]]
        if critical_refs:
            lines.append("## ℹ️ 批判性引用（安全·不违规）")
            lines.append("")
            ref_files = defaultdict(int)
            for f in critical_refs:
                ref_files[f["文件"]] += 1
            for fname, count in sorted(ref_files.items()):
                lines.append(f"  - {fname} ({count}处引用)")
            lines.append("")
            lines.append("  以上均为批判寒心叙事的文章本体，目的在揭露问题而非宣扬。")
            lines.append("")

        # 结论
        if real_risks:
            lines.append("## 🔴 结论")
            lines.append(f"  发现 {len(real_risks)} 个需要处理的表述问题。")
            lines.append("  底线3要求：系统公开表述不得绑死好人=穷、奉献=苦、英雄=死。")
        else:
            lines.append("## 🟢 结论")
            lines.append("  系统公开表述健康。")
            lines.append("  未发现宣扬寒心叙事的实际风险。")
            lines.append("  批判性文章中引用的反例正常，属于揭露问题而非制造问题。")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="龍魂公开表述审计引擎 v1.0 — 底线3: 不让付出者寒心",
    )
    parser.add_argument("action", nargs="?", default="scan",
                        choices=["scan", "report", "rules"])
    parser.add_argument("--json", action="store_true", help="JSON输出")

    args = parser.parse_args()

    if args.action == "rules":
        print("🐉 龍魂公开表述审计 · 规则")
        print("=" * 40)
        print("\n核心有害叙事（严禁）:")
        for p, s, l, d in CORE_HARMFUL_NARRATIVES:
            print(f"  {s} {l}: {d}")
        print("\n苦情叙事（警惕）:")
        for p, s, l, d in SUFFERING_NARRATIVES:
            print(f"  {s} {l}: {d}")
        print("\n付出=牺牲叙事（警惕）:")
        for p, s, l, d in SACRIFICE_NARRATIVES:
            print(f"  {s} {l}: {d}")
        print("\n为你好绑架（警惕）:")
        for p, s, l, d in FOR_YOUR_OWN_GOOD:
            print(f"  {s} {l}: {d}")
        return

    auditor = PublicExpressionAuditor()
    findings = auditor.scan_all()

    if args.json:
        result = {
            "stats": dict(auditor.stats),
            "findings": [
                {k: v for k, v in f.items()}
                for f in findings if not f["批判语境"]
            ],
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(auditor.generate_report())


if __name__ == "__main__":
    main()
