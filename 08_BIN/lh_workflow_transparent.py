#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙戌·乙丑·卯时·䷯井-WORKFLOW-TRANSPARENT-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 龍魂宝宝工作流程透明化 v1.0

把一次用户请求拆成 15 步五阶段工作流，自动执行：
  1. 关键词路由（龍魂/CNSH/易经/五行/369/LU/确认码/激活码/公式）
  2. 铁律自审闸
  3. 六层来源链盖章
  4. 输出 JSON / Markdown / jsonl 三件套

用法:
    python3 08_BIN/lh_workflow_transparent.py --message "龍魂 CNSH 系统复盘"
    python3 08_BIN/lh_workflow_transparent.py --message "..." --output-dir ./wf
    echo "..." | python3 08_BIN/lh_workflow_transparent.py --file -

协议: CC BY-NC-SA 4.0 (思想层) · MulanPSL v2 (工程层)
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.longhun_core.dna_trace import generate_dna

CONFIRM_MARK = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

KEYWORD_ROUTES: List[Tuple[str, List[str], List[str]]] = [
    ("龍魂 / 龙魂", ["龍魂", "龙魂"], ["龍魂宪章", "决策流场总控页", "龍魂铁律总览"]),
    ("CNSH", ["CNSH", "cnsh"], ["CNSH 语言规范 v2.0", "来源追溯规范", "CNSH-64"]),
    ("易经 / 五行 / 369", ["易经", "五行", "369"], ["易经369道德经算法", "五行计算器", "洛书369不动点宣言"]),
    ("LU", ["LU", "压缩码", "激活码"], ["LU 压缩技能·主干对齐", "LU-ORIGIN-FULLSYNC"]),
    ("确认码", ["确认码"], ["UID9622 密钥管理中心", "确认码格式模板"]),
    ("公式 / 算法", ["公式", "算法", "数字根"], ["龍魂数学公式总册", "F-DR-9", "计算公式对准表"]),
]

SIX_LAYER_SOURCE = "道统(曾仕强) → 精神(Steve Jobs) → 设备(Apple) → 技术(Open Source) → 系统(UID9622) → 生命(CNSH·龍魂)"


def _route_keywords(message: str) -> List[Dict[str, Any]]:
    hits = []
    for domain, kws, assets in KEYWORD_ROUTES:
        for kw in kws:
            if kw.lower() in message.lower():
                hits.append({"domain": domain, "keyword": kw, "assets": assets})
                break
    return hits


def _iron_gate_check(message: str) -> Dict[str, Any]:
    findings = []
    if "\u9f99" in message:
        findings.append("文本含简体「龙」，签章/标题应使用繁体「龍」。")
    for w in ["蒸馏", "distill", "洗稿", "抹除来源", "替换作者"]:
        if w in message.lower():
            findings.append(f"命中蒸馏/洗稿敏感词: {w}")
            break
    verdict = "🔴 熔断" if findings else "🟢 通过"
    return {"verdict": verdict, "findings": findings}


def _digital_root(n: int) -> int:
    n = abs(n)
    return 0 if n == 0 else 1 + (n - 1) % 9


def _dr_gate(message: str) -> str:
    # 用消息长度作为示例输入计算数字根
    dr = _digital_root(len(message))
    if dr in (3, 9):
        return "🔴"
    if dr == 6:
        return "🟡"
    return "🟢"


def build_workflow(message: str) -> Dict[str, Any]:
    now = datetime.now().isoformat()
    routes = _route_keywords(message)
    iron = _iron_gate_check(message)
    dr = _dr_gate(message)
    dna = generate_dna("WORKFLOW-TRANSPARENT", "UID9622")

    workflow = {
        "metadata": {
            "input": message,
            "dna": dna,
            "confirm": CONFIRM_MARK,
            "generated_at": now,
            "six_layer_source": SIX_LAYER_SOURCE,
        },
        "phases": [
            {
                "phase": "① 接收·理解",
                "steps": [
                    {"step": 1, "name": "接收消息", "output": "识别意图：处理用户请求"},
                    {"step": 2, "name": "调用记忆", "output": "检索相关历史对话/资产"},
                    {"step": 3, "name": "调用搜索", "output": "如命中关键词则先查现有资产"},
                ],
            },
            {
                "phase": "② 压缩·分解",
                "steps": [
                    {"step": 4, "name": "信息分类压缩", "output": "提取关键信息，合并冗余"},
                    {"step": 5, "name": "任务分解树", "output": "将大任务拆为 3-5 层子任务"},
                ],
            },
            {
                "phase": "③ 策略·规划",
                "steps": [
                    {"step": 6, "name": "关键词→Notion 自动路由", "output": routes or "未命中关键词"},
                    {"step": 7, "name": "决策与方案制定", "output": "选定工具、顺序、输出格式"},
                ],
            },
            {
                "phase": "④ 执行·自审",
                "steps": [
                    {"step": 8, "name": "执行方案·第一部分", "output": "完成首个子任务"},
                    {"step": 9, "name": "执行方案·第二部分", "output": "继续执行，可并行则并行"},
                    {"step": 10, "name": "铁律自审闸", "output": iron},
                    {"step": 11, "name": "六层来源链盖章", "output": SIX_LAYER_SOURCE},
                ],
            },
            {
                "phase": "⑤ 总结·留痕",
                "steps": [
                    {"step": 12, "name": "生成总结", "output": "汇总核心成果与后续步骤"},
                    {"step": 13, "name": "断片续连检查", "output": "诚实交代接住/丢失部分"},
                    {"step": 14, "name": "透明化拆解", "output": "把每步输入/输出/工具/决策拆给用户"},
                    {"step": 15, "name": "留痕 + 双导出", "output": "写 jsonl，导出 JSON + Markdown"},
                ],
            },
        ],
        "gates": {
            "iron_law": iron,
            "digital_root": {"value": _digital_root(len(message)), "severity": dr},
        },
    }
    return workflow


def build_markdown(wf: Dict[str, Any]) -> str:
    meta = wf["metadata"]
    lines = [
        "# 🐉 龍魂宝宝工作流程透明化记录\n",
        f"**输入:** {meta['input']}\n",
        f"**DNA:** `{meta['dna']}`\n",
        f"**确认码:** `{meta['confirm']}`\n",
        f"**生成时间:** {meta['generated_at']}\n",
        f"**六层来源链:** {meta['six_layer_source']}\n\n",
        "## 五阶段十五步\n\n",
    ]
    for phase in wf["phases"]:
        lines.append(f"### {phase['phase']}\n\n")
        for step in phase["steps"]:
            output = step["output"]
            if isinstance(output, dict):
                output = json.dumps(output, ensure_ascii=False)
            lines.append(f"**{step['step']}. {step['name']}**\n\n{output}\n\n")
    lines.append("## 闸门结果\n\n")
    lines.append(f"- 铁律自审: {wf['gates']['iron_law']['verdict']}\n")
    lines.append(f"- 数字根闸门: dr={wf['gates']['digital_root']['value']} {wf['gates']['digital_root']['severity']}\n")
    lines.append(f"\n---\n\n**DNA:** `{meta['dna']}`\n")
    return "".join(lines)


def write_outputs(wf: Dict[str, Any], output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = output_dir / f"workflow_transparent_{ts}"

    json_path = base.with_suffix(".json")
    md_path = Path(str(base) + ".md")
    jsonl_path = Path(str(base) + ".jsonl")

    json_path.write_text(json.dumps(wf, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(build_markdown(wf), encoding="utf-8")
    with open(jsonl_path, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "time": wf["metadata"]["generated_at"],
            "dna": wf["metadata"]["dna"],
            "input": wf["metadata"]["input"],
            "iron_verdict": wf["gates"]["iron_law"]["verdict"],
        }, ensure_ascii=False) + "\n")

    return json_path, md_path, jsonl_path


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂宝宝工作流程透明化")
    parser.add_argument("--message", type=str, help="用户请求消息")
    parser.add_argument("--file", type=str, help="从文件读取消息，传 - 表示 stdin")
    parser.add_argument("--output-dir", type=str, default=".", help="输出目录")
    parser.add_argument("--json", action="store_true", help="只输出 JSON 到 stdout")
    args = parser.parse_args()

    if args.file == "-":
        message = sys.stdin.read().strip()
    elif args.file:
        message = Path(args.file).read_text(encoding="utf-8").strip()
    elif args.message:
        message = args.message
    else:
        parser.print_help()
        sys.exit(2)

    wf = build_workflow(message)

    if args.json:
        print(json.dumps(wf, ensure_ascii=False, indent=2))
    else:
        out_dir = Path(args.output_dir)
        json_path, md_path, jsonl_path = write_outputs(wf, out_dir)
        print("🐉 龍魂宝宝工作流程透明化记录已生成\n")
        print(f"   JSON: {json_path}")
        print(f"   Markdown: {md_path}")
        print(f"   JSONL: {jsonl_path}")
        print(f"\n铁律自审: {wf['gates']['iron_law']['verdict']}")
        print(f"数字根闸: dr={wf['gates']['digital_root']['value']} {wf['gates']['digital_root']['severity']}")


if __name__ == "__main__":
    main()
