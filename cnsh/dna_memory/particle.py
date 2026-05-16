# -*- coding: utf-8 -*-
"""DNA 记忆粒子 · 强类型骨架（对接 YAML Schema §2）"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class YiJi:
    yi: List[str] = field(default_factory=list)
    ji: List[str] = field(default_factory=list)


@dataclass
class CNSHParticleTime:
    """time · 黄历 + ISO（§2 · §3）"""

    iso8601: str = ""
    lunar: str = ""
    shichen: str = ""
    digital_root: int = 0
    wuxing: str = ""
    trigram: str = ""
    yiji: YiJi = field(default_factory=YiJi)
    time_hash: str = ""  # YAML: _time_hash

    def to_dict(self) -> Dict[str, Any]:
        return {
            "iso8601": self.iso8601,
            "lunar": self.lunar,
            "shichen": self.shichen,
            "digital_root": self.digital_root,
            "wuxing": self.wuxing,
            "trigram": self.trigram,
            "yiji": {"yi": self.yiji.yi, "ji": self.yiji.ji},
            "_time_hash": self.time_hash,
        }


@dataclass
class SemanticCore:
    intent: str = ""
    domain: str = ""
    stability: int = 95
    freedom: int = 5


@dataclass
class EmotionBlock:
    surface: List[str] = field(default_factory=list)
    deep: List[str] = field(default_factory=list)
    intensity: int = 0
    action: str = ""


@dataclass
class DecisionTrace:
    input: str = ""
    route: str = ""
    audit: str = "AUTO_OK"
    risk_level: str = "🟢"
    output: str = ""


@dataclass
class ContextBlock:
    people: List[str] = field(default_factory=list)
    topics: List[str] = field(default_factory=list)
    scene: str = ""
    namespace: str = ""


@dataclass
class CompressionStats:
    raw_chars: int = 0
    compressed_chars: int = 0
    ratio: str = ""
    method: str = "tongxinyi_6layer + semantic_fold"


@dataclass
class RestoreHint:
    restore_mode: List[str] = field(default_factory=list)
    trigger_words: List[str] = field(default_factory=list)
    related_particles: List[str] = field(default_factory=list)


@dataclass
class ThermalBlock:
    layer: str = "热记忆"
    C_memory: float = 0.0
    last_triggered: str = ""


@dataclass
class ChainBlock:
    prev_hash: str = ""
    self_hash: str = ""


@dataclass
class CNSH_DNA_Particle:
    """
    CNSH DNA 记忆粒子（可调序列化为 §2 YAML）。
    """

    dna_id: str = ""
    dna_trace: str = ""
    uid: int = 9622
    time: CNSHParticleTime = field(default_factory=CNSHParticleTime)
    semantic_core: SemanticCore = field(default_factory=SemanticCore)
    emotion: EmotionBlock = field(default_factory=EmotionBlock)
    decision_trace: DecisionTrace = field(default_factory=DecisionTrace)
    context: ContextBlock = field(default_factory=ContextBlock)
    compression: CompressionStats = field(default_factory=CompressionStats)
    restore_hint: RestoreHint = field(default_factory=RestoreHint)
    thermal: ThermalBlock = field(default_factory=ThermalBlock)
    chain: ChainBlock = field(default_factory=ChainBlock)

    # 折叠过程留痕（§5 每层线索，便于审计/debug）
    fold_layer_traces: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "CNSH_DNA_PARTICLE": {
                "dna_id": self.dna_id,
                "dna_trace": self.dna_trace,
                "uid": self.uid,
                "time": self.time.to_dict(),
                "semantic_core": {
                    "intent": self.semantic_core.intent,
                    "domain": self.semantic_core.domain,
                    "stability": self.semantic_core.stability,
                    "freedom": self.semantic_core.freedom,
                },
                "emotion": {
                    "surface": self.emotion.surface,
                    "deep": self.emotion.deep,
                    "intensity": self.emotion.intensity,
                    "action": self.emotion.action,
                },
                "decision_trace": {
                    "input": self.decision_trace.input,
                    "route": self.decision_trace.route,
                    "audit": self.decision_trace.audit,
                    "risk_level": self.decision_trace.risk_level,
                    "output": self.decision_trace.output,
                },
                "context": {
                    "people": self.context.people,
                    "topics": self.context.topics,
                    "scene": self.context.scene,
                    "namespace": self.context.namespace,
                },
                "compression": {
                    "raw_chars": self.compression.raw_chars,
                    "compressed_chars": self.compression.compressed_chars,
                    "ratio": self.compression.ratio,
                    "method": self.compression.method,
                },
                "restore_hint": {
                    "restore_mode": self.restore_hint.restore_mode,
                    "trigger_words": self.restore_hint.trigger_words,
                    "related_particles": self.restore_hint.related_particles,
                },
                "thermal": {
                    "layer": self.thermal.layer,
                    "C_memory": self.thermal.C_memory,
                    "last_triggered": self.thermal.last_triggered,
                },
                "chain": {
                    "_prev_hash": self.chain.prev_hash,
                    "_self_hash": self.chain.self_hash,
                },
                "fold_layer_traces": self.fold_layer_traces,
            }
        }


def particle_from_flat_dict(d: Dict[str, Any]) -> CNSH_DNA_Particle:
    """从 `to_dict()[\"CNSH_DNA_PARTICLE\"]` 或含该键的 dict 还原。"""
    if "CNSH_DNA_PARTICLE" in d:
        d = dict(d["CNSH_DNA_PARTICLE"])
    t = d.get("time") or {}
    y = t.get("yiji") or {}
    return CNSH_DNA_Particle(
        dna_id=str(d.get("dna_id", "")),
        dna_trace=str(d.get("dna_trace", "")),
        uid=int(d.get("uid", 9622)),
        time=CNSHParticleTime(
            iso8601=str(t.get("iso8601", "")),
            lunar=str(t.get("lunar", "")),
            shichen=str(t.get("shichen", "")),
            digital_root=int(t.get("digital_root", 0)),
            wuxing=str(t.get("wuxing", "")),
            trigram=str(t.get("trigram", "")),
            yiji=YiJi(yi=list((y.get("yi") or [])), ji=list((y.get("ji") or []))),
            time_hash=str(t.get("_time_hash", "")),
        ),
        semantic_core=SemanticCore(**{k: v for k, v in (d.get("semantic_core") or {}).items() if k in SemanticCore.__dataclass_fields__}),  # type: ignore
        emotion=EmotionBlock(**{k: v for k, v in (d.get("emotion") or {}).items() if k in EmotionBlock.__dataclass_fields__}),  # type: ignore
        decision_trace=DecisionTrace(**{k: v for k, v in (d.get("decision_trace") or {}).items() if k in DecisionTrace.__dataclass_fields__}),  # type: ignore
        context=ContextBlock(**{k: v for k, v in (d.get("context") or {}).items() if k in ContextBlock.__dataclass_fields__}),  # type: ignore
        compression=CompressionStats(**{k: v for k, v in (d.get("compression") or {}).items() if k in CompressionStats.__dataclass_fields__}),  # type: ignore
        restore_hint=RestoreHint(**{k: v for k, v in (d.get("restore_hint") or {}).items() if k in RestoreHint.__dataclass_fields__}),  # type: ignore
        thermal=ThermalBlock(**{k: v for k, v in (d.get("thermal") or {}).items() if k in ThermalBlock.__dataclass_fields__}),  # type: ignore
        chain=ChainBlock(
            prev_hash=str((d.get("chain") or {}).get("_prev_hash", "")),
            self_hash=str((d.get("chain") or {}).get("_self_hash", "")),
        ),
        fold_layer_traces=dict(d.get("fold_layer_traces") or {}),
    )

