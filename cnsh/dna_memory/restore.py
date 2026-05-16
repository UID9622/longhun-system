# -*- coding: utf-8 -*-
"""认知状态恢复 · §4.2 可运行流水线"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from .chain_store import default_db_path, fetch_particle_dict, find_dna_ids_by_trigger, verify_chain
from .chain_hash import particle_dict_fingerprint
from .huangli import verify_time_hash
from .particle import CNSH_DNA_Particle, particle_from_flat_dict


@dataclass
class RestoredCognitiveContext:
    """
    §4.2：触发词 → 索引 → 时间线 → 语义/情绪/决策/场景 → 完整上下文。
    """

    dna_id: str
    particle: CNSH_DNA_Particle
    execution_runbook: List[str] = field(default_factory=list)
    related_ids: List[str] = field(default_factory=list)
    chain_verified: bool = True
    chain_errors: List[str] = field(default_factory=list)
    time_hash_verified: bool = True
    namespace_gate_ok: bool = True


# 对外别名（规范 §4.2 `Context`）
Context = RestoredCognitiveContext


def _build_runbook(p: CNSH_DNA_Particle) -> List[str]:
    return [
        f"[索引] dna_id={p.dna_id}",
        f"[时间层] {p.time.lunar} · {p.time.shichen} · dr={p.time.digital_root}",
        f"[语义层] intent={p.semantic_core.intent[:80]!r}…"
        if len(p.semantic_core.intent) > 80
        else f"[语义层] intent={p.semantic_core.intent!r}",
        f"[情绪层] surface={p.emotion.surface} deep={p.emotion.deep} I={p.emotion.intensity}",
        f"[决策层] {p.decision_trace.audit} / {p.decision_trace.risk_level} route={p.decision_trace.route}",
        f"[场景层] people={p.context.people} topics={p.context.topics} scene={p.context.scene}",
        f"[恢复提示] modes={p.restore_hint.restore_mode} triggers={p.restore_hint.trigger_words}",
    ]


def restore_cognitive_state(
    dna_id: str,
    *,
    db_path: Optional[Path] = None,
    verify_time: bool = True,
    verify_ledger: bool = False,
    expected_namespace: Optional[str] = None,
) -> Context:
    """
    从本地审计库按 `dna_id` 取出粒子并展开为可注入提示词的上下文结构。
    - verify_time: 重算 `_time_hash`
    - verify_ledger: 全链校验（较重）
    - expected_namespace: §8 禁止跨命名空间恢复
    """
    path = db_path or default_db_path()
    raw = fetch_particle_dict(dna_id, db_path=path)
    if raw is None:
        raise FileNotFoundError(f"dna_id 不存在或未入库: {dna_id}")

    p = particle_from_flat_dict(raw)

    # namespace 闸
    gate = True
    if expected_namespace is not None and p.context.namespace != expected_namespace:
        gate = False

    ok_time = True
    if verify_time:
        tdict = p.time.to_dict()
        ok_time = verify_time_hash(tdict)

    c_ok, c_err = True, []
    if verify_ledger:
        c_ok, c_err = verify_chain(db_path=path)

    related = list(dict.fromkeys(p.restore_hint.related_particles))
    return RestoredCognitiveContext(
        dna_id=dna_id,
        particle=p,
        execution_runbook=_build_runbook(p),
        related_ids=related,
        chain_verified=c_ok,
        chain_errors=c_err,
        time_hash_verified=ok_time,
        namespace_gate_ok=gate,
    )


def restore_by_trigger(
    trigger: str,
    *,
    db_path: Optional[Path] = None,
    **kwargs,
) -> List[Context]:
    """§4.2：按触发词命中多条粒子，按 dna_id 排序代替黄历序（表中可加 created_at 再精细排序）。"""
    ids = find_dna_ids_by_trigger(trigger, db_path=db_path)
    out: List[Context] = []
    for i in sorted(ids):
        out.append(restore_cognitive_state(i, db_path=db_path, **kwargs))
    return out


def verify_particle_self_hash(particle: CNSH_DNA_Particle) -> bool:
    """离线校验单粒 self_hash（不连库）。"""
    d = particle.to_dict()["CNSH_DNA_PARTICLE"]
    calc = particle_dict_fingerprint(d)
    return calc == particle.chain.self_hash
