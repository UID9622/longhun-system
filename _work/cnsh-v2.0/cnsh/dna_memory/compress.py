# -*- coding: utf-8 -*-
"""五层折叠 · compress_dialogue → CNSH_DNA_Particle（§5.1）"""
from __future__ import annotations

import re
import secrets
from datetime import datetime, timezone
from typing import Iterable, List, Optional, Set, Tuple

from .huangli import generate_huangli_timestamp, huangli_dict_to_time_block
from .particle import (
    CNSH_DNA_Particle,
    CompressionStats,
    ContextBlock,
    DecisionTrace,
    EmotionBlock,
    RestoreHint,
    SemanticCore,
    ThermalBlock,
)

# 第一层：情绪词表（可外置 YAML）
_SURFACE = re.compile(
    r"(生气|愤怒|烦|累|崩溃|激动|开心|高兴|委屈|难过|害怕|焦虑|爽|无语)"
)
_DEEP_HINT = re.compile(r"(求认同|被看见|怕失控|要主权|怕辜负|憋屈)")
_INTENT_HINT = re.compile(
    r"(想要|需要|希望|帮我|务必|必须|能不能|可不可以|目标|目的)[^。.\n]{0,40}"
)
_TOPIC_KEYWORDS = (
    "路由",
    "DNA",
    "主权",
    "审计",
    "论文",
    "LoRA",
    "Anthropic",
    "CNSH",
    "Git",
    "人格",
    "闸门",
    "黄历",
    "记忆压缩",
)

_SENSITIVE_NS = re.compile(r"(客户[B-Z]|客户[甲乙丙]|namespace_[A-Z]+)")


def _uniq_keep(items: Iterable[str]) -> List[str]:
    seen: Set[str] = set()
    out: List[str] = []
    for x in items:
        x = x.strip()
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out


def _score_sentence(s: str) -> int:
    score = min(len(s), 80)
    for k in _TOPIC_KEYWORDS:
        if k.lower() in s.lower() or k in s:
            score += 12
    if re.search(r"[？?！!]", s):
        score += 5
    if re.search(r"(风险|审计|禁止|必须)", s):
        score += 15
    return score


def _truncate_importance(text: str, limit: int = 120) -> str:
    lines = re.split(r"(?<=[。！？!?])\s*|\n+", text.strip())
    ranked: List[Tuple[int, str]] = [(_score_sentence(ln), ln) for ln in lines if ln.strip()]
    ranked.sort(key=lambda x: -x[0])
    buf: List[str] = []
    n = 0
    for _, ln in ranked:
        if n + len(ln) + 1 <= limit or not buf:
            buf.append(ln[: max(0, limit - n)])
            n += len(buf[-1]) + 1
        if n >= limit:
            break
    out = " ".join(buf).strip()
    return out[:limit]


def compress_dialogue(
    raw_text: str,
    *,
    uid: int = 9622,
    dna_id: Optional[str] = None,
    dna_trace: str = "#龍芯⚡️2026-05-16-MEMORY-v1.0",
    namespace: str = "namespace_TECH",
    at_utc: Optional[datetime] = None,
) -> CNSH_DNA_Particle:
    """
    五层折叠（§5.1）：情绪分离 → 意图 → 决策摘要 → 关系标签 → 重要性截断。
    分层统计写入 fold_layer_traces；结构化字段保留恢复线索。
    """
    raw_text = (raw_text or "").strip()
    raw_chars = len(raw_text)
    fold: dict = {}

    # Layer 1 情绪分离
    surface = list({m.group(0) for m in _SURFACE.finditer(raw_text)})
    deep = list({m.group(0) for m in _DEEP_HINT.finditer(raw_text)})
    stripped = raw_text
    for w in surface:
        stripped = stripped.replace(w, " ")
    layer1_remain = len(re.sub(r"\s+", " ", stripped).strip())
    fold["layer1_emotion_stripped_chars"] = str(layer1_remain)

    # Layer 2 意图（启发式）
    intents = _INTENT_HINT.findall(raw_text)
    intent_blob = "；".join(intents[:5]) if intents else stripped[:500]
    layer2_intent = intent_blob[:500]
    fold["layer2_intent_chars"] = str(len(layer2_intent))

    # Layer 3 决策流抽象（关键词触发）
    audit = "AUTO_OK"
    risk = "🟢"
    route = "heuristic_compress_v1"
    if re.search(r"(BLOCK|阻断|禁止|一票否决)", raw_text, re.I):
        audit = "BLOCKED"
        risk = "🔴"
    elif re.search(r"(确认|待审|🟡|NEED_CONFIRM)", raw_text):
        audit = "NEED_CONFIRM"
        risk = "🟡"

    dt = DecisionTrace(
        input=raw_text[:280] + ("…" if len(raw_text) > 280 else ""),
        route=route,
        audit=audit,
        risk_level=risk,
        output=_truncate_importance(layer2_intent or stripped, 200),
    )
    layer3_blob = f"{dt.input[:120]}|{dt.route}|{dt.audit}|{dt.risk_level}"
    fold["layer3_decision_blob_chars"] = str(len(layer3_blob))

    # Layer 4 关系图
    people = ["UID9622"]
    if re.search(r"客户", raw_text):
        people.append("客户方")
    cust = _SENSITIVE_NS.findall(raw_text)
    people.extend(cust)
    topics = [k for k in _TOPIC_KEYWORDS if k in raw_text or k.lower() in raw_text.lower()]
    scene = "工程"
    if re.search(r"(情绪|难过|委屈)", raw_text):
        scene = "情绪输出"
    if re.search(r"(合同|报价|商务)", raw_text):
        scene = "商务"

    ctx = ContextBlock(
        people=_uniq_keep(people),
        topics=_uniq_keep(topics),
        scene=scene,
        namespace=namespace,
    )
    fold["layer4_context_topics_count"] = str(len(ctx.topics))

    # Layer 5 重要性截断 → semantic_core.intent
    merged_for_rank = f"{layer2_intent}\n{stripped}"
    intent_final = _truncate_importance(merged_for_rank, 120)
    fold["layer5_semantic_intent_chars"] = str(len(intent_final))

    intens = min(9, 3 + len(surface) + (3 if deep else 0))
    emotion = EmotionBlock(
        surface=surface or (["平静"] if not deep else []),
        deep=deep or [],
        intensity=intens,
        action="先响应情绪再解析指令" if surface or deep else "直接解析工程指令",
    )

    sem = SemanticCore(
        intent=intent_final or "(未检出显式意图·保留原文折叠链)",
        domain="AI语义系统 / 工程落地" if topics else "通用对话",
        stability=95 if risk == "🟢" else (75 if risk == "🟡" else 60),
        freedom=5 if risk == "🟢" else (15 if risk == "🟡" else 25),
    )

    # compression stats（目标 ~120 字核心 + 结构化字段总长单独统计）
    struct_summary_len = len(intent_final) + sum(
        len(x) for x in (dt.input, dt.output, dt.route, sem.domain)
    )
    ratio = f"{max(1, raw_chars)}:{max(1, len(intent_final))}"

    mid = dna_id
    if not mid:
        day = datetime.now(timezone.utc).strftime("%Y%m%d")
        mid = f"MEM-{day}-{secrets.token_hex(2).upper()}"

    h = generate_huangli_timestamp(utc_time=at_utc, timezone_offset_hours=7, uid=uid)
    triggers = _uniq_keep(list(topics) + surface + deep)[:12]
    related: List[str] = []

    p = CNSH_DNA_Particle(
        dna_id=mid,
        dna_trace=dna_trace,
        uid=uid,
        time=huangli_dict_to_time_block(h),
        semantic_core=sem,
        emotion=emotion,
        decision_trace=dt,
        context=ctx,
        compression=CompressionStats(
            raw_chars=raw_chars,
            compressed_chars=len(intent_final),
            ratio=ratio,
            method="tongxinyi_5layer + semantic_fold v1",
        ),
        restore_hint=RestoreHint(
            restore_mode=["timeline", "semantic", "emotional", "decisionflow"],
            trigger_words=triggers,
            related_particles=related,
        ),
        thermal=ThermalBlock(
            layer="热记忆",
            C_memory=min(0.99, 0.55 + 0.05 * len(triggers)),
            last_triggered=h.get("iso8601", "")[:10],
        ),
        fold_layer_traces=fold,
    )
    # 结构化总长写入 fold 备注，便于验收「约 25:1」为 INTENT 维度；全文仍在 decision_trace.input
    p.fold_layer_traces["structured_fold_chars_estimate"] = str(struct_summary_len)
    return p
