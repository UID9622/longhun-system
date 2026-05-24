# -*- coding: utf-8 -*-
"""
伪代码 / 代码块留白 轻量审计 — 鲁班链与 CNSW 的补充信号。

- 有界扫描，避免把整本 Notion / 超大补丁一次性吃满（自适应、可迭代补规则）。
- 与 Notion「总索引页」（dcb73d6f…）关系：那边是图谱与层级入口；此处是**工程文本**侧探针，不镜像全文。

DNA: #龍芯⚡️2026-05-16-CNSW-PSEUDOCODE-AUDIT-v1.0
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple

# 单次扫描上限（UTF-8 字节近似用字符数封顶，切断消耗）
_SCAN_CHAR_CAP = 96_000

_DECLARED_RE = re.compile(
    r"(伪代码|伪码|pseudocode|示意(?:代码|算法)|"
    r"附录\s*[A-Za-z0-9]?\s*[:：]?\s*(伪|算法|代码)|"
    r"仅供说明|非生产代码|示例仅|illustration\s+only|not\s+production)",
    re.I,
)


def _iter_fence_bodies(text: str) -> List[Tuple[str, str]]:
    """解析 ``` 围栏：(语言/信息行, 正文)。"""
    lines = text.splitlines()
    out: List[Tuple[str, str]] = []
    i = 0
    n = len(lines)
    while i < n:
        raw = lines[i]
        if raw.strip().startswith("```"):
            info = raw.strip()[3:].strip()
            i += 1
            chunk: List[str] = []
            while i < n and not lines[i].strip().startswith("```"):
                chunk.append(lines[i])
                i += 1
            if i < n:
                i += 1
            out.append((info, "\n".join(chunk)))
        else:
            i += 1
    return out


def _ellipsis_score_in_body(body: str, _lang_hint: str) -> int:
    """围栏内「留白/省略」信号计数（启发式，可后续补规则）。"""
    score = 0
    for line in body.splitlines():
        s = line.strip()
        if not s:
            continue
        if s in (".", ".."):
            continue
        if re.fullmatch(r"\.{3,}", s) or s in ("…", "# ...", "# …", "// ...", "/* ... */"):
            score += 2
            continue
        if re.search(r"//\s*\.{3,}\s*$", s) or re.search(r"#\s*\.{3,}\s*$", s):
            score += 1
            continue
        # 行尾 …… 且围栏像过程式草稿（每围栏只记一次，防误报膨胀）
        if re.search(r"\.\.\.\s*$", s) and re.search(
            r"\b(def|class|function|func|fn|void|int)\b", body
        ):
            score += 1
            break
    return score


def audit_pseudocode_in_text(text: str) -> Dict[str, Any]:
    """
    返回结构化信号；``risk`` ∈ none | notice | review。
    ``score_delta``：仅建议用于**助手输出**场景，由 hook_scanner 酌情扣主权分。
    """
    raw = text or ""
    capped = len(raw) > _SCAN_CHAR_CAP
    t = raw[:_SCAN_CHAR_CAP]
    declared = bool(_DECLARED_RE.search(t))
    fences = _iter_fence_bodies(t)
    fence_count = len(fences)
    ell_total = 0
    for info, body in fences:
        ell_total += _ellipsis_score_in_body(body, info)

    hints: List[str] = []
    risk = "none"
    score_delta = 0

    if fence_count == 0:
        pass
    elif declared:
        risk = "notice"
        hints.append("declared_illustration_or_pseudo")
    else:
        if ell_total >= 4 or (ell_total >= 2 and fence_count >= 2):
            risk = "review"
            score_delta = 10
            hints.append("unmarked_ellipsis_heavy_fence")
        elif ell_total >= 2:
            risk = "review"
            score_delta = 8
            hints.append("unmarked_ellipsis_in_fence")

    return {
        "scan_chars": len(t),
        "capped_input": capped,
        "fence_count": fence_count,
        "declared_intent": declared,
        "ellipsis_signal": ell_total,
        "risk": risk,
        "score_delta": score_delta,
        "hints": hints,
    }


def incremental_added_text_from_patch(patch: str) -> str:
    """
    从 unified diff 抽取「新增行」正文（去掉首字符 +），供补丁侧伪代码审计。
    不包含 diff 元数据行，降低误报。
    """
    lines: List[str] = []
    for line in (patch or "").splitlines():
        if not line.startswith("+") or line.startswith("+++"):
            continue
        lines.append(line[1:])
    return "\n".join(lines)
