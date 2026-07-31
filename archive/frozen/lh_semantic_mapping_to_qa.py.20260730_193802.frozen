#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_SEMANTIC_MAPPING_TO_QA-v1.0-d3ebfc7e
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂·统一语义指令对照表 → QA 训练数据生成器

读取 01_protocols/LH-SEMANTIC-COMMAND-MAPPING-v1.0.md 中的触发说法映射表，
自动生成 JSONL 训练数据，注入下一版模型训练。

DNA 由生成器自动产出，禁止手写。
"""

import json
import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lh_dna_generator import generate_dna

PROJECT = Path(__file__).resolve().parent.parent
SOURCE_MD = PROJECT / "01_protocols" / "LH-SEMANTIC-COMMAND-MAPPING-v1.0.md"
OUTPUT_DIR = PROJECT / "models" / "longhun-v1.0" / "lora_output" / "semantic_command_qa"
OUTPUT_FILE = OUTPUT_DIR / "train.jsonl"

UNIFIED_SYSTEM_PROMPT = (
    "你是龍魂，UID9622（诸葛鑫·Lucky）的个人主权AI。回答原则：人民数据主权至上，中国自主可控；"
    "来源可查去向可追责任可究；不删除只冻结；底座焊死（369不动点/河图洛书/易经/五行八卦）。\n"
    "六大铁律：①来源不可删·影响不可覆·贡献不可抹 ②只冻结不删除 ③每个动作绑定DNA追溯码 "
    "④三才主权指数SI<0.34锁定AI决策 ⑤三才算法为L0宪法层 ⑥农历干支时间戳。\n"
    "回答请简洁准确、用中文。"
)


def parse_mapping_table(md_path: Path) -> list[dict]:
    """解析 markdown 中的触发说法映射表（仅读取'三、触发说法映射表'节）"""
    text = md_path.read_text(encoding="utf-8")
    entries = []
    in_target_section = False

    for line in text.splitlines():
        line = line.strip()
        # 节边界：只在二级标题处切换，三级/四级子标题保持当前状态
        if line.startswith("## "):
            in_target_section = "触发说法映射表" in line
            continue
        if not in_target_section or not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|")]
        # 过滤空表头和分隔行
        parts = [p for p in parts if p]
        if len(parts) != 3:
            continue
        trigger, action, note = parts
        if trigger in ("触发说法", "---") or trigger.startswith("-"):
            continue
        entries.append({
            "trigger": trigger,
            "action": action,
            "note": note,
        })

    return entries


def build_answer(action: str, note: str, trigger: str) -> str:
    """根据动作标签和说明构建 assistant 回答"""
    # 统一回答模板：动作标签 + 一句话解释 + 可选引导
    return (
        f"【意图识别】你的说法「{trigger}」对应系统动作标签 `{action}`。\n"
        f"【一句话解释】{note}。\n"
        f"【下一步】我已将请求路由到对应引擎，请继续说明具体需求。"
    )


def generate_qa(entries: list[dict]) -> list[dict]:
    """生成 messages 格式训练样本"""
    samples = []
    for e in entries:
        samples.append({
            "messages": [
                {"role": "system", "content": UNIFIED_SYSTEM_PROMPT},
                {"role": "user", "content": e["trigger"]},
                {"role": "assistant", "content": build_answer(e["action"], e["note"], e["trigger"])},
            ],
            "metadata": {
                "action": e["action"],
                "source": "LH-SEMANTIC-COMMAND-MAPPING-v1.0",
            }
        })
    return samples


def main():
    print("📝 统一语义指令对照表 → QA 训练数据")
    print(f"   源文档: {SOURCE_MD}")

    if not SOURCE_MD.exists():
        print(f"   ❌ 源文档不存在: {SOURCE_MD}")
        sys.exit(1)

    entries = parse_mapping_table(SOURCE_MD)
    print(f"   解析条目: {len(entries)}")

    if len(entries) < 200:
        print(f"   ⚠️ 条目不足 200，当前 {len(entries)}")

    samples = generate_qa(entries)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for s in samples:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    print(f"   ✅ 输出: {OUTPUT_FILE}")
    print(f"   样本数: {len(samples)}")
    print(f"   DNA: {generate_dna('SEMANTIC-QA-GEN', '1.0')}")


if __name__ == "__main__":
    main()
