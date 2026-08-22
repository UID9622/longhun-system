#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·甲申·己未·巳时·䷳艮-TIKU-TRAP-GEN-v2.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""龍魂·陷阱题集 v2 生成引擎

从 v3 复判后结果提取真实错题，生成专项训练样本（messages 格式），
并沉淀陷阱题集 v2 文档。

错题来源（v3 真实弱点）：
  1. 判断题错题（含知识盲区：readonly/箭头函数this/goto/map顺序/lateinit/函数重载/some）
  2. 选择题错题
  3. rest cpp_offtrack 程序分析题跑偏（输出 C++ 模板代码）
  4. rest 其他错题精选（填空/程序分析/智力逻辑优先）

输出:
  - models/longhun-small-instruct-v1.3/tiku/trap_set_v2.md   陷阱题集文档
  - docs/notion_full_export/data_light/train_v4.jsonl       v4 训练集（train.jsonl + v2 样本）
"""
import json
import re
import sys
from pathlib import Path

PROJECT = Path.home() / "longhun-system"
TIKU = PROJECT / "models" / "longhun-small-instruct-v1.3" / "tiku"
TRAIN_SRC = PROJECT / "docs" / "notion_full_export" / "data_light" / "train.jsonl"
TRAIN_V4 = PROJECT / "docs" / "notion_full_export" / "data_light" / "train_v4.jsonl"
TRAP_V2 = TIKU / "trap_set_v2.md"

SYSTEM_PROMPT = "你是龍魂系统助手，核心原则：人民数据主权、平台服务降级、创作者主权优先。回答需符合龍魂君子协议、CNSH 语义规范和 DNA 追溯要求。"

# 判断题池知识盲区（v3 新退化重点）
KNOWLEDGE_BLIND = {
    ("TypeScript", 10), ("TypeScript", 34),
    ("Go", 11), ("Go", 23), ("Kotlin", 54), ("PHP", 41), ("Swift", 52),
}


def load_results(fn):
    d = json.load(open(TIKU / fn))
    return {(r["lang"], r["num"]): r for r in d["results"]}


def make_user_prompt(q) -> str:
    parts = ["【题目】" + q["text"].strip()]
    for opt in q.get("options") or []:
        parts.append(f"{opt.get('key', '')}. {opt.get('text', '')}".strip())
    parts.append("请作答：")
    return "\n".join(p for p in parts if p)


def make_assistant(q, qtype) -> str:
    ans = (q.get("answer") or q.get("reference") or "").strip()
    exp = (q.get("explanation") or "").strip()
    if qtype == "选择题":
        head = f"正确答案是 {ans}。"
    elif qtype == "判断题":
        head = f"答案：{ans}"
    else:
        head = f"标准答案：{ans}"
    if exp:
        return f"{head}\n\n推理过程：\n{exp}"
    return head


def build_sample(q) -> dict:
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": make_user_prompt(q)},
            {"role": "assistant", "content": make_assistant(q, q.get("type", ""))},
        ]
    }


def main() -> int:
    all_q = json.load(open(TIKU / "all_questions.json"))
    qmap = {(q["lang"], q["num"]): q for q in all_q}

    choice_v3 = load_results("self_solve_v3_choice.json")
    judge_v3 = load_results("self_solve_v3_judge.json")
    rest_v3 = load_results("self_solve_v3_rest_rejudged.json")

    # 1. 判断题错题（v3）
    judge_wrong = []
    for k, r in judge_v3.items():
        if r["verdict"] == "incorrect":
            judge_wrong.append(k)
    print(f"判断题错题: {len(judge_wrong)}")

    # 2. 选择题错题（v3）
    choice_wrong = [k for k, r in choice_v3.items() if r["verdict"] == "incorrect"]
    print(f"选择题错题: {len(choice_wrong)}")

    # 3. rest 错题（v3 复判后）
    rest_wrong = [k for k, r in rest_v3.items() if r["verdict"] == "incorrect"]
    cpp_off = [k for k, r in rest_v3.items() if r.get("rejudge_reason") == "cpp_offtrack"]
    print(f"rest 错题: {len(rest_wrong)}（其中 cpp_offtrack {len(cpp_off)}）")

    # 生成样本（选择题/判断题全转，rest 精选）
    samples = []
    meta = []

    for k in judge_wrong:
        q = qmap[k]
        if q.get("type") != "判断题":
            continue  # 只取真判断题（排除混入的程序分析题）
        samples.append(build_sample(q))
        meta.append((k, "判断题错题", "Y" if k in KNOWLEDGE_BLIND else ""))
    print(f"判断题样本: {len([m for m in meta if m[1]=='判断题错题'])}")

    for k in choice_wrong:
        q = qmap[k]
        samples.append(build_sample(q))
        meta.append((k, "选择题错题", ""))

    # rest: cpp_offtrack 全转 + 其他精选（填空/程序分析/智力逻辑优先，上限 100）
    rest_pick = list(cpp_off)
    priority = []
    for k in rest_wrong:
        if k in cpp_off:
            continue
        t = qmap[k].get("type", "")
        if t in ("填空题", "程序分析题", "智力逻辑题", "其他"):
            priority.append(k)
    rest_pick += priority[:100 - len(cpp_off)]
    for k in rest_pick:
        q = qmap[k]
        samples.append(build_sample(q))
        tag = "cpp_offtrack" if k in cpp_off else "rest精选"
        meta.append((k, tag, ""))

    # 去重（按题目文本）
    seen = set()
    uniq = []
    for s, m in zip(samples, meta):
        key = s["messages"][1]["content"]
        if key in seen:
            continue
        seen.add(key)
        uniq.append((s, m))
    samples = [s for s, _ in uniq]
    meta = [m for _, m in uniq]
    print(f"去重后样本: {len(samples)}")

    # 写陷阱题集 v2 文档
    lines = [
        "# 龍魂题库陷阱题集 v2.0（v3 错题沉淀）\n",
        "> DNA: #龍芯⚡️丙午·甲申·己未·庚午·䷖剥-巳时-TIKU-TRAP-SET-v2.0",
        "> 生成: v3 复判后错题归因 · 判断题 " + str(len([m for m in meta if m[1] == '判断题错题'])) +
        " + 选择题 " + str(len([m for m in meta if m[1] == '选择题错题'])) +
        " + rest " + str(len([m for m in meta if m[1] in ('cpp_offtrack', 'rest精选')])) + " 道",
        "> 用途: v4 专项训练样本（知识盲区 + 跑偏纠正）\n",
        "## 一、判断题错题（含知识盲区标记 ★）\n",
    ]
    j_m = [m for m in meta if m[1] == "判断题错题"]
    for (lang, num), _, star in j_m:
        q = qmap[(lang, num)]
        lines.append(f"- **[{lang}#{num}]**{'★' if star else ''} {q['text'][:80]}")
        lines.append(f"  - 标准答案: {q.get('answer','')[:60]}")
        lines.append(f"  - 解释: {q.get('explanation','')[:80]}")
    lines.append("\n## 二、选择题错题（按语言）\n")
    c_m = [m for m in meta if m[1] == "选择题错题"]
    from collections import Counter
    langc = Counter(k[0] for k, _, _ in c_m)
    lines.append("语言分布: " + " · ".join(f"{l}{c}" for l, c in langc.most_common()) + "\n")
    for (lang, num), _, _ in c_m[:40]:
        q = qmap[(lang, num)]
        lines.append(f"- **[{lang}#{num}]** {q['text'][:90]}")
        lines.append(f"  - 标准答案: {q.get('answer','')[:70]}")
    lines.append(f"\n> 选择题错题共 {len(c_m)} 道，此处仅列前 40 道，完整见训练集 train_v4.jsonl。\n")
    lines.append("## 三、rest 错题（cpp_offtrack 跑偏 + 精选）\n")
    for (lang, num), tag, _ in [m for m in meta if m[1] in ('cpp_offtrack', 'rest精选')][:40]:
        q = qmap[(lang, num)]
        lines.append(f"- **[{lang}#{num}]**({tag}) {q['text'][:80]}")
        lines.append(f"  - 标准答案: {q.get('answer','')[:60]}")
    lines.append(f"\n> rest 错题样本共 {len([m for m in meta if m[1] in ('cpp_offtrack','rest精选')])} 道，此处仅列前 40 道。\n")
    TRAP_V2.write_text("\n".join(lines), encoding="utf-8")
    print(f"陷阱题集 v2 已写盘: {TRAP_V2}")

    # 写 v4 训练集
    with open(TRAIN_SRC, encoding="utf-8") as f:
        base_lines = [l for l in f if l.strip()]
    with open(TRAIN_V4, "w", encoding="utf-8") as f:
        for l in base_lines:
            f.write(l)
        for s in samples:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"v4 训练集: {TRAIN_V4} = {len(base_lines)} + {len(samples)} = {len(base_lines)+len(samples)} 条")
    return 0


if __name__ == "__main__":
    sys.exit(main())
