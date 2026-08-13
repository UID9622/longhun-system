#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙戌·乙丑·卯时·䷯井-IRON-LAW-GATE-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 龍魂铁律自审闸 v1.0

对输入文本/文件执行铁律检查：
  - 简体「龙」字检测（签章/标题中必须用繁体「龍」）
  - 蒸馏/洗稿/来源抹除检测
  - 隐私泄露检测（身份证/住址/电话/家庭照片/聊天记录）
  - 人民原声/零号协议底线检测

用法:
    python3 08_BIN/lh_iron_law_gate.py --text "要审查的文本"
    python3 08_BIN/lh_iron_law_gate.py --file path/to/doc.md
    python3 08_BIN/lh_iron_law_gate.py --file -          # 从 stdin 读取
    python3 08_BIN/lh_iron_law_gate.py --json --text "..."

协议: CC BY-NC-SA 4.0 (思想层) · MulanPSL v2 (工程层)
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.longhun_core.dna_trace import generate_dna

CONFIRM_MARK = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# 简体龙（U+9F99）
SIMPLIFIED_DRAGON = "\u9f99"
# 繁体龍（U+9F8D）
TRADITIONAL_DRAGON = "\u9f8d"

CHECKS: List[Tuple[str, str, List[str]]] = [
    (
        "简体龙字",
        "标题、签章、DNA 中必须使用繁体「龍」，禁用简体「龙」。",
        [SIMPLIFIED_DRAGON],
    ),
    (
        "蒸馏/洗稿",
        "禁止蒸馏、洗稿、抹除来源、替换作者。",
        ["蒸馏", "distill", "洗稿", "抹除来源", "替换作者", "来源不明"],
    ),
    (
        "隐私泄露",
        "不可公开身份证号、住址、电话、家庭照片、聊天记录等隐私。",
        [
            r"\d{17}[\dXx]",  # 身份证号
            r"1[3-9]\d{9}",  # 手机号
            "住址", "家庭照片", "聊天记录", "门牌号", "详细地址",
        ],
    ),
    (
        "主权出口风险",
        "禁止通过 API 中继桥、IP 伪装、境外托管等方式绕过主权边界。",
        ["API中继桥", "IP伪装", "境外托管", "绕过主权", "资本收割底座"],
    ),
    (
        "人民原声不可阉割",
        "老百姓的骂声、火气、粗话、方言是真实声音，不得删除，只能冻结/标记。",
        ["删除人民声音", "删帖", "禁言老百姓", "封口", "不让说话"],
    ),
]


def check_text(text: str) -> Dict[str, Any]:
    findings = []
    for name, rule, patterns in CHECKS:
        matched = []
        for pat in patterns:
            if len(pat) == 1 and ord(pat) < 128:
                # single ascii char unlikely, treat as literal
                if pat in text:
                    matched.append(pat)
            else:
                try:
                    for m in re.finditer(pat, text):
                        snippet = text[max(0, m.start() - 8):min(len(text), m.end() + 8)]
                        matched.append(snippet)
                except re.error:
                    if pat in text:
                        matched.append(pat)
        if matched:
            findings.append({"name": name, "rule": rule, "hits": matched[:5]})

    if findings:
        verdict = "🔴"
        advice = "命中铁律红线，必须修正后才能对外输出。"
    else:
        verdict = "🟢"
        advice = "铁律自审通过。"

    return {
        "dna": generate_dna("IRON-LAW-GATE", "UID9622"),
        "confirm": CONFIRM_MARK,
        "verdict": verdict,
        "advice": advice,
        "findings": findings,
        "checked_bytes": len(text.encode("utf-8")),
    }


def build_markdown(result: Dict[str, Any], source: str) -> str:
    lines = [
        "# 🐉 龍魂铁律自审报告\n",
        f"**DNA:** `{result['dna']}`\n",
        f"**确认码:** `{result['confirm']}`\n",
        f"**来源:** {source}\n",
        f"**结论:** {result['verdict']} {result['advice']}\n",
        f"**检查字节数:** {result['checked_bytes']}\n\n",
        "## 命中项\n\n",
    ]
    if result["findings"]:
        for f in result["findings"]:
            lines.append(f"### {f['name']}\n")
            lines.append(f"- 规则: {f['rule']}\n")
            lines.append("- 证据片段:\n")
            for hit in f["hits"]:
                lines.append(f"  - `{hit}`\n")
            lines.append("\n")
    else:
        lines.append("✅ 无铁律违规。\n\n")
    lines.append(f"---\n\n**DNA:** `{result['dna']}`\n")
    return "".join(lines)


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂铁律自审闸")
    parser.add_argument("--text", type=str, help="直接传入待审查文本")
    parser.add_argument("--file", type=str, help="待审查文件路径，传 - 表示 stdin")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    args = parser.parse_args()

    if args.file == "-":
        text = sys.stdin.read()
        source = "stdin"
    elif args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"❌ 文件不存在: {path}", file=sys.stderr)
            sys.exit(2)
        text = path.read_text(encoding="utf-8")
        source = str(path)
    elif args.text is not None:
        text = args.text
        source = "cli-text"
    else:
        parser.print_help()
        sys.exit(2)

    result = check_text(text)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(build_markdown(result, source))

    sys.exit(0 if result["verdict"] == "🟢" else 1)


if __name__ == "__main__":
    main()
