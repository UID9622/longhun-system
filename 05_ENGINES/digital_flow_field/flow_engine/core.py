# 龍魂系统 · 工程实现层
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 文化归属: 思想框架归龍魂核心思想层 (CC BY-NC-SA 4.0)
# DNA: #龍芯⚡️丙午·癸未·甲申-DIGITAL-FLOW-FIELD-CORE-v2.0-UID9622
# 署名: UID9622（诸葛鑫·Lucky）

"""数字流场核心算法。

提供字符数字根、文本统计分析、χ² 随机性检验与数字指纹生成。
所有计算纯本地完成，不联网。
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Sequence


# 3×3 洛书矩阵的行列和均为 15；χ² 检验的自由度 df=8，α=0.05 临界值
_CHI2_CRITICAL_05 = 15.507
_MAX_INPUT_CHARS = 100_000


def char_digital_root(char: str) -> int:
    """返回单个字符的 Unicode 码点数字根（1-9）。

    空字符或码点为 0 时返回 0，表示无效粒子。
    """
    if not char:
        return 0
    code = ord(char)
    if code == 0:
        return 0
    # 对码点各位反复求和，直到得到个位数
    while code >= 10:
        code = sum(int(d) for d in str(code))
    return code


def preprocess_text(text: str | None, ignore_whitespace: bool = True) -> str:
    """输入文本预处理：可选去除空白、剔除控制字符与零宽字符。"""
    if not text:
        return ""
    # 剔除零宽及常见不可见控制字符（保留普通空白以便后续处理）
    text = re.sub(
        r"[\u0000-\u0008\u000b-\u000c\u000e-\u001f\u007f-\u009f"
        r"\u200b-\u200f\u2060-\u206f\ufeff\u202a-\u202e]",
        "",
        text,
    )
    if ignore_whitespace:
        text = re.sub(r"\s+", "", text)
    return text


def _even_sample(text: str, max_chars: int) -> str:
    """等距采样，尽量保留原始分布特征。"""
    if len(text) <= max_chars:
        return text
    step = max(1, len(text) // max_chars)
    return text[::step][:max_chars]


@dataclass
class TextAnalysis:
    """文本分析结果。"""

    total: int
    counts: List[int]                      # 索引 0 占位，counts[1..9] 有效
    percentages: List[float]
    chi2: float
    is_random_like: bool
    most_active_root: int
    most_active_pct: float
    least_active_root: int
    least_active_pct: float
    fingerprint: str
    sampled: bool
    raw_length: int


def analyze_text(
    text: str | None,
    ignore_whitespace: bool = True,
    max_chars: int = _MAX_INPUT_CHARS,
) -> TextAnalysis:
    """对文本进行数字根统计分析。

    Args:
        text: 输入文本。
        ignore_whitespace: 是否忽略空白字符。
        max_chars: 最大处理字符数，超长时等距采样。

    Returns:
        TextAnalysis 对象。
    """
    text = preprocess_text(text, ignore_whitespace=ignore_whitespace)
    raw_length = len(text)
    sampled = raw_length > max_chars
    text = _even_sample(text, max_chars)

    counts = [0] * 10
    for ch in text:
        root = char_digital_root(ch)
        if root:
            counts[root] += 1

    total = sum(counts[1:])
    if total == 0:
        return TextAnalysis(
            total=0,
            counts=counts,
            percentages=[0.0] * 10,
            chi2=0.0,
            is_random_like=False,
            most_active_root=0,
            most_active_pct=0.0,
            least_active_root=0,
            least_active_pct=0.0,
            fingerprint="",
            sampled=sampled,
            raw_length=raw_length,
        )

    expected = total / 9.0
    chi2 = sum((counts[i] - expected) ** 2 / expected for i in range(1, 10))
    is_random_like = chi2 < _CHI2_CRITICAL_05

    percentages = [0.0] * 10
    for i in range(1, 10):
        percentages[i] = counts[i] / total * 100.0

    roots_with_count = [i for i in range(1, 10) if counts[i] > 0]
    most_active_root = max(range(1, 10), key=lambda i: counts[i])
    least_active_root = min(roots_with_count, key=lambda i: counts[i])

    fingerprint = "".join(str(char_digital_root(ch)) for ch in text)[:500]

    return TextAnalysis(
        total=total,
        counts=counts,
        percentages=percentages,
        chi2=chi2,
        is_random_like=is_random_like,
        most_active_root=most_active_root,
        most_active_pct=percentages[most_active_root],
        least_active_root=least_active_root,
        least_active_pct=percentages[least_active_root],
        fingerprint=fingerprint,
        sampled=sampled,
        raw_length=raw_length,
    )


def generate_text_fingerprint(text: str | None, max_len: int = 500) -> str:
    """生成文本数字指纹。"""
    text = preprocess_text(text)
    return "".join(str(char_digital_root(ch)) for ch in text)[:max_len]


def distribution_to_csv_rows(analysis: TextAnalysis) -> List[List[str]]:
    """把分布表转为 CSV 行。"""
    rows = [["数字根", "次数", "占比(%)"]]
    for i in range(1, 10):
        rows.append([str(i), str(analysis.counts[i]), f"{analysis.percentages[i]:.2f}"])
    rows.append(["合计", str(analysis.total), "100.00"])
    return rows


if __name__ == "__main__":
    import argparse
    import json as _json

    parser = argparse.ArgumentParser(description="数字流场 CLI 分析")
    parser.add_argument("--input", "-i", required=True, help="输入文本或文件路径（支持 .txt/.md）")
    parser.add_argument("--output", "-o", default="result.json", help="输出 JSON 路径")
    parser.add_argument("--html", action="store_true", help="同时输出 HTML 报告")
    parser.add_argument("--csv", action="store_true", help="同时输出 CSV 分布表")
    args = parser.parse_args()

    raw = args.input
    if os.path.isfile(raw):
        with open(raw, "rb") as f:
            raw = f.read().decode("utf-8", errors="ignore")

    result = analyze_text(raw)
    payload = {
        "total": result.total,
        "counts": result.counts,
        "percentages": result.percentages,
        "chi2": result.chi2,
        "is_random_like": result.is_random_like,
        "most_active_root": result.most_active_root,
        "least_active_root": result.least_active_root,
        "fingerprint": result.fingerprint,
        "sampled": result.sampled,
        "raw_length": result.raw_length,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        _json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"JSON: {args.output}")

    if args.csv:
        csv_path = os.path.splitext(args.output)[0] + ".csv"
        import csv
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(distribution_to_csv_rows(result))
        print(f"CSV: {csv_path}")

    if args.html:
        html_path = os.path.splitext(args.output)[0] + ".html"
        rows = "\n".join(
            f"<tr><td>{i}</td><td>{result.counts[i]}</td><td>{result.percentages[i]:.2f}%</td></tr>"
            for i in range(1, 10)
        )
        html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>Flow Report</title>
<style>body{{background:#0a0a1a;color:#eee;font-family:sans-serif;padding:24px;}}
table{{border-collapse:collapse;}} td,th{{border:1px solid #444;padding:8px;}}</style>
</head><body>
<h1>🐲 数字流场报告</h1>
<p>总粒子: {result.total} · χ²: {result.chi2:.4f} · 随机性: {"✅ 符合" if result.is_random_like else "⚠️ 偏离"}</p>
<table><tr><th>数字根</th><th>次数</th><th>占比</th></tr>{rows}</table>
</body></html>"""
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"HTML: {html_path}")
