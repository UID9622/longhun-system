#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍芯⚡️丙午·丙申·壬戌·子时·需-TIKU-PARSER-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0（核心思想层）
"""
🐉 龍魂 · 题库解析器 v1.0
DNA: #龍芯⚡️丙午·丙申·壬戌·子时·䷄需-TIKU-PARSER-v1.0

功能:
  1. 解析 12_DOCS/notion_mirror/ 下所有"全方位笔试题库" md 文件
  2. 抽取 题目/选项/答案/解析/参考答案/难度/题型/所属部分/语言
  3. 输出结构化 JSON + 统计报告（难度分布/题型分布/题量）

用法:
  python3 08_BIN/lh_tiku_parser.py                 # 解析+统计
  python3 08_BIN/lh_tiku_parser.py --json-only     # 只出 JSON
  python3 08_BIN/lh_tiku_parser.py --stats-only    # 只出统计
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NOTION_MIRROR = PROJECT_ROOT / "12_DOCS" / "notion_mirror"
OUT_DIR = PROJECT_ROOT / "models" / "longhun-small-instruct-v1.3" / "tiku"

LANGS = ["C", "Go", "Java", "JavaScript", "Kotlin", "PHP", "Ruby", "Rust", "Shell_Bash", "SQL", "Swift", "TypeScript"]


def lang_display(name: str) -> str:
    """文件名→人类可读语言名。"""
    mapping = {
        "C": "C#",
        "Go": "Go",
        "Java": "Java",
        "JavaScript": "JavaScript",
        "Kotlin": "Kotlin",
        "PHP": "PHP",
        "Ruby": "Ruby",
        "Rust": "Rust",
        "Shell_Bash": "Shell/Bash",
        "SQL": "SQL",
        "Swift": "Swift",
        "TypeScript": "TypeScript",
    }
    return mapping.get(name, name)


def infer_type(text: str, options: list, answer: str = "") -> str:
    """从题目文本+选项+答案推断题型。"""
    if options:
        return "选择题"
    if re.search(r"___+|______+|（\s*）|\(\s*\)\s*$", text) or ("输出" in text and "___" in text):
        return "填空题"
    # 判断题：答案含对错标记 或 文本为陈述句带"正确/错误/是否/对错"
    if answer and re.search(r"✅|❌|√|×|正确|错误|对|错", answer):
        return "判断题"
    if re.search(r"是否正确|是否正确|对错|判断|（正确|(正确|错误)[。?？]?\s*$", text):
        return "判断题"
    if re.search(r"智力|逻辑题|最少需要称|天平|不均匀的绳子|数列|睡莲|红苹果|守卫|烧完", text, re.IGNORECASE):
        return "智力逻辑题"
    if re.search(r"综合应用", text, re.IGNORECASE):
        return "综合应用题"
    if re.search(r"编程题|编程：|实现|编写|写出.*代码|设计.*方法|完成.*函数|扩展方法|递归方法|泛型方法|写一个|实现一个|方法|函数", text, re.IGNORECASE):
        return "编程题"
    if re.search(r"系统设计|架构设计|如何设计|设计一个.*系统", text, re.IGNORECASE):
        return "系统设计题"
    if re.search(r"调试|修复|找错|排错|bug", text, re.IGNORECASE):
        return "代码调试题"
    if re.search(r"阅读.*代码|以下代码|写出输出|程序输出|输出什么|输出是", text, re.IGNORECASE):
        return "程序分析题"
    if re.search(r"简述|说明|描述|比较|区别|分析|解释|谈谈|为什么|说出", text):
        return "简答题"
    return "其他"


def parse_stars(text: str) -> int | None:
    """提取 [难度：⭐⭐] → 3。"""
    m = re.search(r"\[?难度[：:]\s*([⭐☆★]+|\d+)\s*\]?", text)
    if not m:
        return None
    raw = m.group(1)
    if raw.isdigit():
        return int(raw)
    return raw.count("⭐") or raw.count("★")


def parse_md(path: Path) -> list[dict]:
    """解析单个题库 md 文件。"""
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")

    questions: list[dict] = []
    cur: dict | None = None
    section = ""
    in_ref = False
    in_code = False
    code_target = ""  # "answer" / "reference"
    code_buf: list[str] = []  # 待定代码块缓冲（尚未判定是题干还是答案）

    # 预扫描：知识点难度表（部分题库有）
    star_map: dict[str, int] = {}
    for m in re.finditer(r"\|\s*([^|]+?)\s*\|\s*([⭐☆★]{1,5}|\d)\s*\|\s*(\d+)", text):
        star_map[m.group(1).strip()] = m.group(2).count("⭐") or m.group(2).count("★") or int(m.group(2))

    for line in lines:
        s = line.strip()
        if not s:
            continue

        # 章节标题
        sec_m = re.match(r"^#\s*第[一二三四五六七八九十]+部分[：:]\s*(.+)$", s)
        if sec_m:
            section = sec_m.group(1).strip()
            continue

        # 题目行: ### 1. ... 或 ### 21. 编程题：...
        q_m = re.match(r"^###\s*(\d+)[.、]\s*(.+)$", s)
        if q_m:
            if cur:
                questions.append(cur)
            raw_text = q_m.group(2).strip()
            stars = parse_stars(raw_text)
            # 去掉 [难度：xx] 标记
            clean_text = re.sub(r"\[?难度[：:]\s*[⭐☆★]+\s*\]?\s*", "", raw_text)
            cur = {
                "lang": path.name.split("_")[0],
                "num": int(q_m.group(1)),
                "section": section,
                "text": clean_text,
                "options": [],
                "answer": "",
                "explanation": "",
                "reference": "",
                "stars": stars,
                "type": "",
            }
            in_ref = False
            in_code = False
            code_target = ""
            code_buf = []
            continue

        if cur is None:
            continue

        # 选项: A. xxx / A、xxx / A) xxx
        opt_m = re.match(r"^([A-H])[.、\)]\s*(.+)$", s)
        if opt_m and not s.startswith("**"):
            cur["options"].append({"key": opt_m.group(1), "text": opt_m.group(2)})
            continue

        # 代码块开始/结束（先处理，因为可能在任何位置出现）
        if s.startswith("```"):
            if not in_code:
                in_code = True
            else:
                in_code = False
            continue

        # 代码块内容收集（在未判定归属前先进缓冲）
        if in_code:
            code_buf.append(s)
            continue

        # 答案: **答案：B** / **答案：** / **答案：** xxx（出现答案标记 → 缓冲代码块是题干，丢弃）
        ans_m = re.match(r"^\*\*答案[：:]\*?\*?\s*(.*?)\*?\*?\s*$", s)
        if ans_m and not cur["answer"]:
            cur["answer"] = ans_m.group(1).strip().rstrip("*").strip()
            in_ref = False
            code_target = "answer"
            code_buf = []
            continue

        # 参考答案（简答/编程）→ 缓冲代码块并入参考答案
        ref_m = re.match(r"^\*\*参考答案[：:]\*?\*?\s*(.*)$", s)
        if ref_m:
            in_ref = True
            code_target = "reference"
            if code_buf:
                cur["reference"] = "\n".join(code_buf)
                code_buf = []
            if ref_m.group(1).strip():
                cur["reference"] += ("\n" if cur["reference"] else "") + ref_m.group(1).strip()
            continue

        # 解析: **解析：** xxx（出现解析标记 → 缓冲代码块是参考答案）
        exp_m = re.match(r"^\*\*解析[：:]\*?\*?\s*(.+)$", s)
        if exp_m and not cur["explanation"]:
            if code_buf and not cur["reference"] and not cur["answer"]:
                cur["reference"] = "\n".join(code_buf)
            code_buf = []
            cur["explanation"] = exp_m.group(1).strip()
            in_ref = False
            in_code = False
            continue

        # 补充参考答案续行（在参考答案段内，非题目标记、非下一个题目）
        if in_ref:
            if not s.startswith(("#", "---", "|", ">", "```")):
                cur["reference"] += ("\n" if cur["reference"] else "") + s
                continue

        # 答案续行（**答案：xxx** 之后可能有多行内容）
        if cur["answer"] and not cur["explanation"] and not s.startswith(("#", "---", "```")):
            if not s.startswith(("A.", "B.", "C.", "D.", "E.", "F.", "G.", "H.")):
                # 仅当答案后面紧跟解析前的补充说明才追加（防御过度吞并）
                pass

    if cur:
        questions.append(cur)

    # 后处理：题型推断 + 难度回填
    for q in questions:
        q["type"] = infer_type(q["text"], q["options"], q["answer"])
        if q["stars"] is None:
            # 回填：按题型基准难度
            base = {"选择题": 2, "填空题": 2, "判断题": 1, "简答题": 3, "编程题": 4,
                    "程序分析题": 3, "系统设计题": 5, "代码调试题": 4, "其他": 2}
            q["stars"] = base.get(q["type"], 2)
    return questions


def main() -> int:
    ap = argparse.ArgumentParser(description="龍魂题库解析器")
    ap.add_argument("--json-only", action="store_true")
    ap.add_argument("--stats-only", action="store_true")
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    all_questions: list[dict] = []
    per_lang: dict[str, list[dict]] = {}

    for lang in LANGS:
        pattern = f"{lang}_全方位笔试题库*.md"
        files = list(NOTION_MIRROR.glob(pattern))
        if not files:
            print(f"[warn] 未找到 {lang} 题库", file=sys.stderr)
            continue
        qs = parse_md(files[0])
        per_lang[lang] = qs
        all_questions.extend(qs)

    # 写 JSON（按语言分文件 + 合并）
    for lang, qs in per_lang.items():
        (OUT_DIR / f"{lang}.json").write_text(
            json.dumps(qs, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_DIR / "all_questions.json").write_text(
        json.dumps(all_questions, ensure_ascii=False, indent=2), encoding="utf-8")

    # 统计
    n = len(all_questions)
    star_cnt = Counter(q["stars"] for q in all_questions)
    type_cnt = Counter(q["type"] for q in all_questions)
    lang_cnt = Counter(q["lang"] for q in all_questions)
    with_ans = sum(1 for q in all_questions if q["answer"] or q["reference"])
    with_exp = sum(1 for q in all_questions if q["explanation"])

    stats = {
        "total": n,
        "languages": {lang_display(k): v for k, v in sorted(lang_cnt.items(), key=lambda x: -x[1])},
        "stars": {f"{k}⭐": v for k, v in sorted(star_cnt.items())},
        "types": {k: v for k, v in type_cnt.most_common()},
        "with_answer": with_ans,
        "with_explanation": with_exp,
        "answer_rate": round(with_ans / n * 100, 1) if n else 0,
    }
    (OUT_DIR / "stats.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.json_only:
        return 0

    # 打印报告
    print(f"🐉 题库解析完成 | 总题量: {n}")
    print(f"   覆盖语言: {len(per_lang)} 种 | 带答案: {with_ans} ({stats['answer_rate']}%) | 带解析: {with_exp}")
    print(f"\n📊 难度分布:")
    for k in sorted(star_cnt, key=lambda x: -x):
        print(f"   {k}⭐: {star_cnt[k]}")
    print(f"\n📝 题型分布:")
    for k, v in type_cnt.most_common():
        print(f"   {k}: {v}")
    print(f"\n🌐 语言分布:")
    for k, v in sorted(lang_cnt.items(), key=lambda x: -x[1]):
        print(f"   {lang_display(k)}: {v}")
    print(f"\n📁 输出: {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
