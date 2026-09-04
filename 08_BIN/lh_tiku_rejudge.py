#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·甲申·己未·辰时·䷳艮-TIKU-REJUDGE-v1.3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""龍魂·题库复判定引擎 v1.3

对自解结果 JSON 中 unknown 的结果做宽松复判定，修复原判定器三个缺陷：
  1. 短答案（<4 字）直接放弃 → 改为单关键词子串判定
  2. 英文空格粘连（`type alias`→`typealias` 匹配失败）→ 按空格拆词匹配
  3. or 型答案（`START` 或 `BEGIN`）→ 候选拆分，任一命中即对
v1.2 新增（救回 no_keywords 类 unknown）：
  4. 数字+单位答案（"2 次"/"第 29 天"）→ 答案标记数字比对 + 目标数字命中
  5. 单字中文答案（"表"）→ 子串命中即对
  6. 纯符号答案（`!`/`?:`/三引号/`||`）→ 符号段匹配
  7. 路径型 token（`/v2`）→ 加入候选词
v1.3 新增（编程题答案补全后的防虚高）：
  8. 跨语言跑偏检测（JS 题输出 Java/Python/Rust/Go/C++ → 判错）
  9. 编程题代码级判定：代码结构检查 + 专有标识符命中即对（替代通用关键词）
  10. 程序分析题数字答案：无"答案"标记不判对（防代码复述虚高）

用法:
  python3 bin/lh_tiku_rejudge.py <结果.json> [--out 修正后.json] [--verbose]
已判定为 correct/incorrect 的记录保持不变，只重判 unknown。
"""
import argparse
import json
import re
import sys
from pathlib import Path


# v1.2: 数字+单位/单字中文/纯符号判定（救回 no_keywords 类 unknown）
UNIT_ZH = ("次", "天", "个", "枚", "种", "度", "年", "月", "小时", "分钟", "块", "张", "秒", "名", "行", "位")

# 中文泛化停用词（命中不算，防止虚高）
STOP_ZH = {
    "输出", "问题", "类型", "使用", "例如", "表示", "结果", "方法", "区别", "作用",
    "优势", "注意", "说法", "方式", "情况", "过程", "内容", "什么", "为什么", "如何",
    "错误", "正确", "实现", "定义", "声明", "可以", "需要", "用于", "进行", "一个",
    "是否", "应该", "返回", "调用", "创建", "就是", "不是", "描述", "分析", "处理",
    "代码", "程序", "语句", "变量", "函数", "以下", "上述", "如下", "直接", "存在",
    "判断", "说明", "指出", "给出", "找到", "选择", "简单", "核心", "主要", "重要",
}

# 跑偏语言检测：模型输出出现 C/C++ 特征（非 C 语言题）
CPP_SIGNS = ["#include", "using namespace std", "std::", "int main()", "cout <<"]

# v1.3: 跨语言跑偏检测——题目语言 X 输出含其他语言强特征 → 判错
LANG_SIGNS = {
    "Java": ["import java.", "public class ", "public static", "java.util",
             "atomicinteger", "system.out.println"],
    "Python": ["def ", "print(", "import sys", "import os",
               "import numpy", "import pandas"],
    "Rust": ["use std::", "fn main(", "impl ", "::new()"],
    "Go": ["package main", "func main(", "fmt."],
    "C++": CPP_SIGNS,
}

# 编程题代码标识符判定的英语通用词（不作为命中依据）
GENERIC_IDS = {
    "function", "return", "const", "let", "var", "class", "new", "this", "if",
    "else", "for", "while", "import", "from", "public", "private", "static",
    "void", "int", "string", "main", "true", "false", "null", "undefined",
    "self", "fn", "use", "impl", "struct", "enum", "mut", "match", "async",
    "await", "try", "catch", "finally", "throw", "extends", "interface",
    "implements", "package", "def", "print", "type", "value", "data", "key",
    "map", "list", "array", "object", "number", "name", "args", "arg", "input",
    "output", "item", "items", "result", "index", "i", "j", "k", "len", "size",
    "error", "ok", "msg", "message", "id", "str", "char", "bool", "double",
    "float", "long", "short", "byte", "integer", "stringbuilder",
}


def is_missing(ans: str) -> bool:
    """标准答案缺失检测：空 / 见上 / 上题 / 略 / 纯标点"""
    t = ans.strip().replace("`", "").replace("*", "").strip()
    if not t:
        return True
    if re.fullmatch(r"[。.；;，,\s]*(见上|上题|同上|略|无|None|N/A)?[。.；;，,\s]*", t):
        return True
    return False


def is_cpp_offtrack(qtype_lang: str, output: str) -> bool:
    """检测输出是否跑偏成 C/C++ 模板代码（题目语言非 C/C++ 时）。

    v1.2: 豁免仅限 C/C++（C 语言题含 #include 正常）；C# 题出现
    `#include <iostream>`/`using namespace std` 仍视为跑偏。
    """
    if qtype_lang in ("C", "C++"):
        return False
    low = output.lower()
    return any(s in low for s in CPP_SIGNS)


def extract_candidates(ans: str) -> list:
    """从标准答案提取候选关键词。

    规则：
      - 去反引号/markdown；括号内容并入候选（or 型答案拆解）
      - 中文 2+ 字连续段（去掉停用词后仅保留 >=3 字的可信词；2 字词走短答案分支）
      - 英文/数字标识符 >=4 字母（词边界匹配）；短标识符走整体匹配分支
    返回 (candidates, short_token)：
      - candidates: 可信候选词（中文>=3且非停用 + 英文>=4）
      - short_token: 若整个答案是一个短 token（英文2-3字母/数字/单字符），返回它
    """
    text = ans.replace("`", " ").replace("**", " ")
    parts = [text]
    for m in re.findall(r"[（(]([^（）()]+)[)）]", text):
        parts.append(m)
    cands = []
    for p in parts:
        cands += re.findall(r"[\u4e00-\u9fff]{2,}", p)
        cands += [w for w in re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", p) if len(w) >= 4]
        cands += [w for w in re.findall(r"/[A-Za-z0-9_.-]+", p) if len(w) >= 2]  # /v2 型路径 token
    seen = set()
    out = []
    for c in cands:
        if c not in seen:
            seen.add(c)
            out.append(c)
    # 过滤中文停用词（>=3字且非停用）
    cands_f = [c for c in out if not (c[0] >= "\u4e00" and c in STOP_ZH)]
    # 短 token：整个答案去标点后是一个 token（保留空格，如 "3 4"）
    clean = re.sub(r"[^A-Za-z0-9_\s\u4e00-\u9fff]", "", ans).strip().lower()
    short_token = None
    if clean and len(clean) <= 10 and not re.search(r"[\u4e00-\u9fff]", clean):
        short_token = clean
    elif re.fullmatch(r"[\u4e00-\u9fff]{2}", ans.strip()) and " " not in ans:
        short_token = ans.strip()  # 2 字中文短答案
    return cands_f, short_token


def is_lang_offtrack(qtype_lang: str, output: str) -> bool:
    """跨语言跑偏检测：题目语言 X，输出含其他语言强特征 → 跑偏。"""
    low = output.lower()
    for lang, signs in LANG_SIGNS.items():
        if lang == qtype_lang:
            continue
        if any(s in low for s in signs):
            return True
    return False


def extract_prog_ids(ans: str, qtext: str = "") -> list[str]:
    """提取答案代码中的专有标识符（过滤英语通用词 + 题目标识符）。"""
    code = ans.replace("`", "").strip()
    ids = re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", code)
    # 题目标识符不作为命中依据（模型复述题目不算实现）
    if qtext:
        seen = {i.lower() for i in re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", qtext)}
    else:
        seen = set()
    out_ids = []
    for i in ids:
        low = i.lower()
        if low in GENERIC_IDS or len(i) < 3 or low in seen or i in out_ids:
            continue
        if re.fullmatch(r"[_0-9]+", i):
            continue
        out_ids.append(i)
        if len(out_ids) >= 8:
            break
    return out_ids


# 编程题代码级判定要求输出含代码结构（防"答案：正确/概念描述"虚高）
CODE_STRUCT_RE = re.compile(r"function |=>|class |const |let |var |\bdef\b|\bfn\b|\bimpl\b|\{\s*$|;\s*$|\{ |return ")


def match_prog_answer(ans: str, out: str, qtext: str = ""):
    """编程题代码级判定：输出含代码结构 + 任意 1 个答案特有标识符命中即对。"""
    ids = extract_prog_ids(ans, qtext)
    if not ids:
        return None
    # 模型必须给出实际代码（概念描述/判断题式回答不算实现）
    if not CODE_STRUCT_RE.search(out):
        return "incorrect", "prog_no_code"
    hits = [i for i in ids if re.search(
        rf"(?<![A-Za-z0-9_]){re.escape(i)}(?![A-Za-z0-9_])", out)]
    if hits:
        return "correct", f"prog_id:{','.join(hits[:3])}"
    return "incorrect", f"prog_id_miss:{','.join(ids[:3])}"


def match_number_answer(ans: str, out: str, no_marker_none: bool = False):
    """数字+单位答案判定（"2 次" / "第 29 天" / "7.5 度"）。

    优先解析 out 中"答案标记后"的数字（【答案】/答案：/正确答案），
    与标准答案数字比对：相等→correct，不相等→incorrect。
    无答案标记时：标准数字出现在 out → correct。
    no_marker_none=True（程序分析题等）：无答案标记不判对——
    代码里出现的数字 ≠ 模型答出答案（防 C#48 复述代码虚高）。
    """
    # 数字必须是答案主体（允许前置"第/约"+空格），从头匹配排除 /v2、A1 这类带其他前缀的
    clean = ans.replace("`", "").strip()
    m = re.match(r"(?:第|约)?\s*(\d+(?:\.\d+)?)\s*(" + "|".join(UNIT_ZH) + r")?", clean)
    if not m:
        return None
    num, unit = m.group(1), m.group(2) or ""
    pat = rf"(?<![0-9.]){re.escape(num)}(?![0-9])"
    # 答案标记后数字优先（【答案】/答案：/正确答案）
    am = re.search(r"(?:正确答案|答案为|答案)\s*[为是：:)]?\s*[^\d\n]{0,6}(\d+(?:\.\d+)?)", out)
    if am:
        return "correct" if am.group(1) == num else "incorrect"
    # 无标记：程序分析题不判对；其他题型目标数字出现在 out 即对
    if no_marker_none:
        return None
    if re.search(pat, out):
        return "correct"
    return None


def match_short_zh(ans: str, out: str):
    """单字中文答案（"表"）→ 子串命中即对。"""
    t = ans.replace("`", "").strip()
    if len(t) == 1 and "\u4e00" <= t <= "\u9fff" and t not in STOP_ZH:
        return "correct" if t in out else "incorrect"
    return None


def match_symbol_answer(ans: str, out: str):
    """纯符号答案（`!` / `%` / `?:` / 三引号 / `||`）→ out 含同符号段即对。"""
    t = ans.replace("`", "").strip()
    if not t or len(t) > 10 or re.search(r"[\u4e00-\u9fffa-zA-Z0-9]", t):
        return None
    segs = re.findall(r"[^\w\u4e00-\u9fff\s]+", t)
    if not segs:
        return None
    # 优先最长连续相同符号块（'"""'→匹配 out 中 '"""'，而非整串 '"""..."""'）
    best = ""
    for s in segs:
        for m in re.finditer(r"(.)\1+", s):
            if len(m.group(0)) > len(best):
                best = m.group(0)
    if not best:
        best = max(segs, key=len)
    return "correct" if re.escape(best) in out else "incorrect"


def rejudge(question: dict, output: str):
    """宽松复判定。返回 (verdict, reason)。

    verdict: correct / incorrect / unknown
    reason: 判定依据（用于审计追溯）
    """
    ans = (question.get("answer") or question.get("reference") or "").strip()
    if not ans or is_missing(ans):
        return "unknown", "answer_missing"

    qtype = question.get("type", "")
    out = output.strip().lower()

    if qtype == "判断题":
        if re.search(r"正确|√|对", ans) and re.search(r"正确|√|对|true|yes", out):
            return "correct", "judge_hit"
        if re.search(r"错误|×|错", ans) and re.search(r"错误|×|错|false|no", out):
            return "correct", "judge_hit"
        return "incorrect", "judge_miss"

    if qtype == "选择题":
        std_keys = re.findall(r"[A-H]", ans)
        out_keys = set(re.findall(r"答案[：:]\s*([A-H])", output))
        out_keys |= set(re.findall(
            r"(?:正确答案|答案为|答案)\s*[为是：:]?\s*\**\s*[（(]?([A-H])[)）]?\s*\**\s*[.、。]?", output))
        out_keys |= set(re.findall(r"([A-H])\s*[.、)）]", output))
        out_keys |= set(re.findall(r"[（(]([A-H])[)）]", output))
        out_keys |= set(re.findall(r"^\s*([A-H])\s*$", output, re.M))
        if any(k in out_keys for k in std_keys):
            return "correct", "choice_hit"
        return "incorrect", "choice_miss"

    # 自由文本（填空/简答/编程/程序分析等）
    # 跑偏检测：非 C 语言题输出 C/C++ 模板代码 → 直接判错
    if is_cpp_offtrack(question.get("lang", ""), output):
        return "incorrect", "cpp_offtrack"

    # v1.2 明确判定优先（数字/单字中文/纯符号）——模型已给出明确答案时不被跑偏检测误伤
    no_marker_none = qtype in ("程序分析题", "代码调试题")
    r = match_number_answer(ans, out, no_marker_none)
    if r:
        return r, "number_unit"
    r = match_short_zh(ans, out)
    if r:
        return r, "short_zh1"
    r = match_symbol_answer(ans, out)
    if r:
        return r, "symbol"

    # v1.3 跨语言跑偏（JS 题输出 Java/Python 等）
    if is_lang_offtrack(question.get("lang", ""), output):
        return "incorrect", "lang_offtrack"

    # v1.3 编程题/综合应用题：代码级标识符判定
    if qtype in ("编程题", "综合应用题", "程序分析题", "代码调试题"):
        r = match_prog_answer(ans, out, question.get("text", ""))
        if r:
            return r[0], r[1]

    cands, short_token = extract_candidates(ans)
    if short_token:
        if re.fullmatch(r"[\u4e00-\u9fff]{2}", short_token):
            # 2 字中文短答案：子串匹配（原子→原子性）
            if short_token in out:
                return "correct", f"short_zh:{short_token}"
        elif re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{1,3}", short_token):
            # 短标识符：词边界整体匹配（map/get/tsc/any）
            if re.search(rf"(?<![A-Za-z0-9_]){re.escape(short_token)}(?![A-Za-z0-9_])", out):
                return "correct", f"short_id:{short_token}"
            return "incorrect", f"short_id_miss:{short_token}"
        else:
            # 数字/混合短答案（3 4 / [4, 16] / 12）
            if re.search(rf"(?<![0-9]){re.escape(short_token)}(?![0-9])", out):
                return "correct", f"short_num:{short_token}"
            return "incorrect", f"short_num_miss:{short_token}"
    if not cands:
        return "unknown", "no_keywords"
    hits = [c for c in cands if (c[0] >= "\u4e00" and c in out) or re.search(
        rf"(?<![A-Za-z0-9_]){re.escape(c.lower())}(?![A-Za-z0-9_])", out)]
    if hits:
        return "correct", f"kw_hit:{','.join(hits[:3])}"
    if len(out) < 20:
        return "unknown", "output_too_short"
    return "incorrect", "no_hit"


def main() -> int:
    ap = argparse.ArgumentParser(description="题库 unknown 宽松复判定")
    ap.add_argument("result_json", help="自解结果 JSON（self_solve_*.json）")
    ap.add_argument("--questions", default=None, help="题库 JSON（缺省自动定位）")
    ap.add_argument("--out", default=None, help="修正后 JSON 输出路径（缺省不写盘）")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    src = Path(args.result_json)
    d = json.loads(src.read_text())
    results = d["results"]

    # 定位题库
    if args.questions:
        q_path = Path(args.questions)
    else:
        # 与结果同目录的 all_questions.json
        cand = src.parent / "all_questions.json"
        cand2 = src.parent / ".." / "tiku" / "all_questions.json"
        q_path = cand if cand.exists() else cand2
    questions = json.loads(q_path.read_text())
    by_key = {(q["lang"], q["num"]): q for q in questions}

    stats = {"correct": d.get("correct", 0), "incorrect": d.get("incorrect", 0),
             "unknown": d.get("unknown", 0)}
    fixed = {"unknown_to_correct": 0, "unknown_to_incorrect": 0, "stayed_unknown": 0}
    reasons = {}

    for r in results:
        if r["verdict"] != "unknown":
            continue
        q = by_key.get((r["lang"], r["num"]))
        if q is None:
            continue
        nv, reason = rejudge(q, r["model_output"])
        r["verdict"] = nv
        r["rejudge_reason"] = reason
        r["rejudge_version"] = "v1.3"
        if nv == "correct":
            stats["correct"] += 1
            stats["unknown"] -= 1
            fixed["unknown_to_correct"] += 1
        elif nv == "incorrect":
            stats["incorrect"] += 1
            stats["unknown"] -= 1
            fixed["unknown_to_incorrect"] += 1
        else:
            fixed["stayed_unknown"] += 1
        reasons[reason] = reasons.get(reason, 0) + 1
        if args.verbose:
            print(f"[{r['lang']}#{r['num']}][{r.get('type','')}] {r['verdict']} ({reason})"
                  f" | ans={q.get('answer','')[:40]!r} | out={r['model_output'][:50]!r}")

    n = len(results)
    acc = stats["correct"] / n * 100 if n else 0
    d["correct"] = stats["correct"]
    d["incorrect"] = stats["incorrect"]
    d["unknown"] = stats["unknown"]
    d["accuracy"] = round(acc, 4)
    d["rejudge_stats"] = fixed
    d["rejudge_reasons"] = reasons

    print(f"文件: {src.name}")
    print(f"复判修正: unknown→correct {fixed['unknown_to_correct']} | "
          f"unknown→incorrect {fixed['unknown_to_incorrect']} | 保持unknown {fixed['stayed_unknown']}")
    print(f"修正后: 对 {stats['correct']} / 错 {stats['incorrect']} / 未知 {stats['unknown']} | "
          f"准确率 {acc:.2f}%")
    print(f"原因分布: {reasons}")

    if args.out:
        out_p = Path(args.out)
        out_p.write_text(json.dumps(d, ensure_ascii=False, indent=2))
        print(f"已写盘: {out_p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
