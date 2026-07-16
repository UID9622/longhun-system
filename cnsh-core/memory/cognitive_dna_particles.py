#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂认知DNA粒子系统 (Cognitive DNA Particle System)
DNA:#龍芯⚡️2026-06-03-COGNITIVE-PARTICLES-FILE1-v1.0

完整的认知状态压缩和恢复机制

记忆压缩 ≠ “记住句子”
记忆恢复 ≠ “回放文本”

真正的恢复 = 认知环境完整重建 (Cognitive Environment Reconstruction)

必须恢复:
1. 语义核心 (Semantic Core)
2. 决策路径 (Decision Path Replay)
3. 情感折叠 (Emotion Fold - 保存在档案但移除于逻辑)
4. 错误模式 (Mistake Pattern)
5. 三才主权指数 (SI Sovereignty Index)

核心原则:
- SI >= 0.34 时才能进行认知重建
- SI < 0.34 时只能保存档案、禁止还原
- 情感折叠永久保存但不影响逻辑决策

理论指导: 曾仕强老师 · Steve Jobs · UID9622
不免责·永久有效
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import json
import hashlib


class CognitiveState(Enum):
    """认知状态分类"""
    COMPRESSED = "compressed"      # 已压缩·可召回
    ACTIVE = "active"              # 活跃·未压缩
    ARCHIVED = "archived"          # 已归档·只读
    LOCKED = "locked"              # 被锁定·SI<0.34


class EmotionalDimension(Enum):
    """情感维度"""
    SURFACE = "surface"            # 表层感受 (疲惫、急迫)
    DEEP = "deep"                  # 深层根源 (不信任、希望)
    PROTECTIVE = "protective"      # 防御机制


@dataclass
class SemanticCore:
    """
    语义核心 - 内容的基本意图

    NOT: 完整的原始文本
    BUT: “为什么要说这个？”的骨架
    """
    primary_intent: str            # 主要意图 (e.g., "解释三才主权")
    abstraction_level: str         # 抽象层级 (L0/L1/L2/L3/L4)
    key_concepts: List[str]        # 核心概念列表
    implicit_premises: List[str]   # 隐含前提
    conclusion_anchor: str         # 结论锚点 (简短陈述)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "SemanticCore":
        return SemanticCore(**data)


@dataclass
class DecisionPathReplay:
    """
    决策回放 - 为什么选择了这条路

    包含:
    - 谁在做决策 (人格路由)
    - 通过什么规则 (F3因子)
    - 什么时辰 (F2因子)
    - 有什么证据 (审计日志)
    """
    selected_persona: str          # 选中的人格路由 (e.g., "P02")
    persona_weights: Dict[str, float]  # 所有人格的权重
    rejected_personas: List[str]   # 为什么拒绝其他人格
    rule_chain_applied: List[str]  # 应用的规则ID (§25, §32...)
    rule_chain_hash: str           # 规则链的SHA256
    temporal_anchor: str           # 时间锚点 (时辰 + 数字根)
    decision_timestamp: str        # ISO8601时间戳
    confidence: float              # 决策置信度 (0.0-1.0)
    audit_log_entries: List[str]   # 审计日志ID

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "DecisionPathReplay":
        return DecisionPathReplay(**data)


@dataclass
class EmotionFold:
    """
    情感折叠 - 保存在档案中但不影响逻辑

    核心原则:
    - preserved_in_archive: True (永久保存)
    - removed_from_logic: True (逻辑中移除)

    永不消除:
    - 为什么你当时感到疲惫
    - 你的希望是什么
    - 你的恐惧根源
    - 你的信任模型

    永不使用于决策:
    - 情感不参与逻辑运算
    - 情感不影响IF/ELSE
    - 情感只是历史记录
    """
    surface_emotions: List[str]    # 表层: ["疲惫", "急迫"]
    deep_roots: List[str]          # 深层: ["不信任", "希望被理解"]
    protective_barriers: List[str] # 防御: ["沉默", "拒绝合作"]

    # 关键: 永远标记为已保存但已移除
    preserved_in_archive: bool = True
    removed_from_logic: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "EmotionFold":
        return EmotionFold(**data)

    def get_archive_note(self) -> str:
        """生成档案注记"""
        return (
            f"【情感折叠档案】\n"
            f"表层: {', '.join(self.surface_emotions)}\n"
            f"深层根源: {', '.join(self.deep_roots)}\n"
            f"防御机制: {', '.join(self.protective_barriers)}\n"
            f"\n【归档说明】\n"
            f"✓ 永久保存于档案\n"
            f"✓ 已移除于逻辑运算\n"
            f"✓ 下次认知恢复时可回溯\"为什么\"\n"
            f"✓ 但不影响新的决策"
        )


@dataclass
class MistakePattern:
    """
    错误模式 - 连续学习轨迹
    """
    mistake_id: str                # 错误的唯一ID
    mistake_type: str              # 类型 (logic/syntax/semantic/judgment)
    description: str               # 描述
    timestamp: str                 # 发生时间
    recovery_status: str           # 已恢复/不可恢复/待恢复
    learning_insight: str          # 从中学到什么


@dataclass
class ThreeTalentSnapshot:
    """
    三才指数快照 - SI在压缩时的状态

    关键:
    - SI >= 0.34 时才能进行认知重建
    - 快照中若SI < 0.34，则该认知永久锁定
    """
    tian_score: float              # 天: 规则遵守
    di_score: float                # 地: 数据完整
    ren_score: float               # 人: 创作权威
    si_index: float                # 计算后的SI值
    sovereignty_level: str         # 主权等级
    can_reconstruct: bool          # 是否允许重建

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ThreeTalentSnapshot":
        return ThreeTalentSnapshot(**data)


# ═══════════════════════════════════════════════════════════════
# 【认知DNA粒子 - 核心结构】
# ═══════════════════════════════════════════════════════════════

@dataclass
class CognitiveDNAParticle:
    """
    认知DNA粒子 - 完整的认知状态压缩形式

    一个粒子包含:
    1. 身份锚点 (Identity Anchor)
    2. 语义核心 (Semantic Core)
    3. 决策回放基础 (Decision Path)
    4. 情感折叠 (Emotion Fold)
    5. 错误模式 (Mistake Pattern)
    6. 三才快照 (SI Snapshot)
    7. DNA追溯码 (DNA Trace)

    关键性质:
    - 不可篡改 (append-only)
    - 可验证 (DNA + 哈希)
    - 条件恢复 (需要 SI >= 0.34)
    """

    # === 身份层 ===
    creator_uid: str               # 创作者UID
    creation_timestamp: str        # 创建时间
    particle_id: str               # 粒子唯一ID

    # === 语义层 ===
    semantic_core: SemanticCore    # 语义核心

    # === 决策层 ===
    decision_replay: DecisionPathReplay  # 决策回放

    # === 情感层 ===
    emotion_fold: EmotionFold      # 情感折叠

    # === 学习层 ===
    mistake_patterns: List[MistakePattern] = field(default_factory=list)

    # === 主权层 ===
    si_snapshot: ThreeTalentSnapshot = None  # SI快照

    # === DNA层 ===
    dna_trace: str = ""            # DNA追溯码
    data_hash: str = ""            # 内容哈希
    signature: str = ""            # 签名 (GPG)

    # === 状态 ===
    state: CognitiveState = CognitiveState.COMPRESSED
    can_be_reconstructed: bool = True  # 是否允许重建 (基于SI)

    def calculate_data_hash(self) -> str:
        """计算内容哈希"""
        data = {
            "semantic": self.semantic_core.to_dict(),
            "decision": self.decision_replay.to_dict(),
            "emotion": self.emotion_fold.to_dict(),
            "timestamp": self.creation_timestamp
        }

        json_str = json.dumps(data, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(json_str.encode()).hexdigest()

    def generate_dna(self) -> str:
        """生成DNA追溯码"""
        timestamp = self.creation_timestamp[:10].replace("-", "")  # YYYYMMDD
        primary_intent = self.semantic_core.primary_intent[:20].replace(" ", "")

        dna = (
            f"#龍芯⚡️{timestamp}-COGNITIVE-{primary_intent}-"
            f"{self.data_hash[:8].upper()}"
        )

        return dna

    def generate_archive_note(self) -> str:
        """为档案生成完整注记"""
        return f"""
【认知DNA粒子档案】
【粒子ID】{self.particle_id}
【创作者】{self.creator_uid}
【时间】{self.creation_timestamp}

【语义核心】
意图: {self.semantic_core.primary_intent}
层级: {self.semantic_core.abstraction_level}
概念: {', '.join(self.semantic_core.key_concepts)}

【决策回放】
选中人格: {self.decision_replay.selected_persona}
规则链: {', '.join(self.decision_replay.rule_chain_applied)}
时间锚: {self.decision_replay.temporal_anchor}
置信度: {self.decision_replay.confidence:.2%}

【主权状态】
SI: {self.si_snapshot.si_index:.4f}
等级: {self.si_snapshot.sovereignty_level}
可重建: {'✅ YES' if self.can_be_reconstructed else '❌ NO'}

【情感档案】
{self.emotion_fold.get_archive_note()}

【DNA追溯】
{self.dna_trace}

【状态】
粒子状态: {self.state.value}
内容哈希: {self.data_hash}
签名: {self.signature[:20]}...

【恢复提示】
SI >= 0.34 时，使用短码 /recall-{self.particle_id} 进行认知恢复
"""

    def to_dict(self) -> Dict[str, Any]:
        """序列化为字典"""
        return {
            "particle_id": self.particle_id,
            "creator_uid": self.creator_uid,
            "creation_timestamp": self.creation_timestamp,
            "state": self.state.value,
            "can_reconstruct": self.can_be_reconstructed,
            "semantic_core": self.semantic_core.to_dict(),
            "decision_replay": self.decision_replay.to_dict(),
            "emotion_fold": self.emotion_fold.to_dict(),
            "si_snapshot": self.si_snapshot.to_dict() if self.si_snapshot else None,
            "dna_trace": self.dna_trace,
            "data_hash": self.data_hash,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "CognitiveDNAParticle":
        """从字典反序列化"""
        return CognitiveDNAParticle(
            particle_id=data["particle_id"],
            creator_uid=data["creator_uid"],
            creation_timestamp=data["creation_timestamp"],
            state=CognitiveState(data.get("state", "compressed")),
            can_be_reconstructed=data.get("can_reconstruct", True),
            semantic_core=SemanticCore.from_dict(data["semantic_core"]),
            decision_replay=DecisionPathReplay.from_dict(data["decision_replay"]),
            emotion_fold=EmotionFold.from_dict(data["emotion_fold"]),
            si_snapshot=ThreeTalentSnapshot.from_dict(data["si_snapshot"]) if data.get("si_snapshot") else None,
            dna_trace=data.get("dna_trace", ""),
            data_hash=data.get("data_hash", ""),
        )


# ═══════════════════════════════════════════════════════════════
# 【认知粒子管理器】
# ═══════════════════════════════════════════════════════════════

class CognitiveDNAParticleManager:
    """
    认知DNA粒子管理系统

    职责:
    1. 创建粒子 (从完整认知状态)
    2. 保存粒子 (append-only JSONL)
    3. 查询粒子 (按ID/UID/时间)
    4. 恢复认知 (SI>=0.34时)
    5. 生成档案 (永久保存)
    """

    def __init__(self, storage_dir: str | None = None):
        """初始化粒子管理器"""
        import os

        self.storage_dir = storage_dir or os.path.expanduser(
            "~/.longhun/cognitive-particles"
        )
        os.makedirs(self.storage_dir, exist_ok=True)

        self.particles_db = os.path.join(self.storage_dir, "particles.jsonl")
        self.archive_dir = os.path.join(self.storage_dir, "archives")
        os.makedirs(self.archive_dir, exist_ok=True)

        self.particles_in_memory: Dict[str, CognitiveDNAParticle] = {}

    def create_particle(
        self,
        creator_uid: str,
        semantic_core: SemanticCore,
        decision_replay: DecisionPathReplay,
        emotion_fold: EmotionFold,
        si_snapshot: ThreeTalentSnapshot,
        mistake_patterns: List[MistakePattern] = None
    ) -> CognitiveDNAParticle:
        """
        创建新的认知粒子
        """
        import uuid

        particle_id = f"PARTICLE-{uuid.uuid4().hex[:12]}"

        particle = CognitiveDNAParticle(
            particle_id=particle_id,
            creator_uid=creator_uid,
            creation_timestamp=datetime.now().isoformat(),
            semantic_core=semantic_core,
            decision_replay=decision_replay,
            emotion_fold=emotion_fold,
            si_snapshot=si_snapshot,
            mistake_patterns=mistake_patterns or [],
            can_be_reconstructed=(si_snapshot.si_index >= 0.34)
        )

        # 计算哈希和DNA
        particle.data_hash = particle.calculate_data_hash()
        particle.dna_trace = particle.generate_dna()

        # 保存到DB
        self._persist_particle(particle)

        # 生成档案
        self._create_archive(particle)

        self.particles_in_memory[particle_id] = particle

        return particle

    def get_particle(self, particle_id: str) -> Optional[CognitiveDNAParticle]:
        """获取粒子"""
        if particle_id in self.particles_in_memory:
            return self.particles_in_memory[particle_id]

        # 从DB加载
        return self._load_particle_from_db(particle_id)

    def can_reconstruct(self, particle_id: str) -> Tuple[bool, str]:
        """
        检查是否可以重建认知

        Returns:
            (可以重建, 原因)
        """
        particle = self.get_particle(particle_id)

        if not particle:
            return False, "粒子不存在"

        if particle.si_snapshot.si_index < 0.34:
            return False, f"主权失锚 (SI={particle.si_snapshot.si_index:.4f} < 0.34)"

        if not particle.can_be_reconstructed:
            return False, "粒子已被锁定"

        return True, "✅ 可重建"

    def reconstruct_cognitive_state(self, particle_id: str) -> Optional[Dict]:
        """
        重建完整的认知环境

        Returns:
            完整的认知状态字典 或 None
        """
        can_reconstruct, reason = self.can_reconstruct(particle_id)

        if not can_reconstruct:
            return None

        particle = self.get_particle(particle_id)

        return {
            "particle_id": particle_id,
            "original_intent": particle.semantic_core.primary_intent,
            "decision_path": {
                "selected_persona": particle.decision_replay.selected_persona,
                "persona_weights": particle.decision_replay.persona_weights,
                "rule_chain": particle.decision_replay.rule_chain_applied,
                "temporal_anchor": particle.decision_replay.temporal_anchor,
                "confidence": particle.decision_replay.confidence,
            },
            "semantic_context": {
                "concepts": particle.semantic_core.key_concepts,
                "premises": particle.semantic_core.implicit_premises,
                "conclusion": particle.semantic_core.conclusion_anchor,
            },
            "emotion_archive": {
                "surface": particle.emotion_fold.surface_emotions,
                "deep_roots": particle.emotion_fold.deep_roots,
                "protective": particle.emotion_fold.protective_barriers,
                "note": "情感已从逻辑中移除·仅用于历史回溯"
            },
            "mistake_history": [
                {
                    "type": m.mistake_type,
                    "description": m.description,
                    "recovery": m.recovery_status,
                    "insight": m.learning_insight
                }
                for m in particle.mistake_patterns
            ],
            "sovereignty_state": {
                "si": particle.si_snapshot.si_index,
                "level": particle.si_snapshot.sovereignty_level,
            }
        }

    def _persist_particle(self, particle: CognitiveDNAParticle) -> None:
        """保存粒子到append-only DB"""
        with open(self.particles_db, 'a', encoding='utf-8') as f:
            f.write(json.dumps(particle.to_dict(), ensure_ascii=False) + "\n")

    def _create_archive(self, particle: CognitiveDNAParticle) -> None:
        """生成永久档案"""
        import os

        archive_path = os.path.join(
            self.archive_dir,
            f"{particle.particle_id}.archive.md"
        )

        with open(archive_path, 'w', encoding='utf-8') as f:
            f.write(particle.generate_archive_note())

    def _load_particle_from_db(self, particle_id: str) -> Optional[CognitiveDNAParticle]:
        """从DB加载粒子"""
        if not os.path.exists(self.particles_db):
            return None

        with open(self.particles_db, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    if data.get('particle_id') == particle_id:
                        return CognitiveDNAParticle.from_dict(data)

        return None


# ═══════════════════════════════════════════════════════════════
# 【演示】
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("\n【龍魂认知DNA粒子系统 v1.0】\n")
    print("DNA:#龍芯⚡️2026-06-03-COGNITIVE-PARTICLES-v1.0")
    print("CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
    print("SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL\n")

    manager = CognitiveDNAParticleManager()

    # 构建认知状态
    semantic = SemanticCore(
        primary_intent="解释三才主权指数系统",
        abstraction_level="L2",
        key_concepts=["SI", "三才", "主权", "认知重建"],
        implicit_premises=["人永远是1", "主权是可测量的"],
        conclusion_anchor="SI>=0.34时主权激活"
    )

    decision = DecisionPathReplay(
        selected_persona="P02",
        persona_weights={"P02": 0.50, "P05": 0.30, "P13": 0.20},
        rejected_personas=["P01_technical_only"],
        rule_chain_applied=["§25", "§32", "§37"],
        rule_chain_hash="a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7",
        temporal_anchor="寅时_dr=3",
        decision_timestamp=datetime.now().isoformat(),
        confidence=0.92,
        audit_log_entries=["LOG-001", "LOG-002"]
    )

    emotion = EmotionFold(
        surface_emotions=["认真", "专注"],
        deep_roots=["想被理解", "希望这个系统有用"],
        protective_barriers=["逻辑优先于风格"]
    )

    si_snapshot = ThreeTalentSnapshot(
        tian_score=0.95,
        di_score=0.98,
        ren_score=0.97,
        si_index=0.963,
        sovereignty_level="🟢_完全主权",
        can_reconstruct=True
    )

    mistake = MistakePattern(
        mistake_id="ERR-001",
        mistake_type="logic",
        description="初版权重加到1.01而不是1.0",
        timestamp="2026-06-03T21:00:00Z",
        recovery_status="已恢复",
        learning_insight="浮点误差需要容差检查"
    )

    print("【创建认知粒子】\n")
    particle = manager.create_particle(
        creator_uid="UID9622",
        semantic_core=semantic,
        decision_replay=decision,
        emotion_fold=emotion,
        si_snapshot=si_snapshot,
        mistake_patterns=[mistake]
    )

    print(f"✅ 粒子已创建: {particle.particle_id}")
    print(f"   DNA: {particle.dna_trace}")
    print(f"   哈希: {particle.data_hash[:16]}...")
    print(f"   SI: {particle.si_snapshot.si_index:.4f}")
    print(f"   可重建: {'✅ YES' if particle.can_be_reconstructed else '❌ NO'}\n")

    print("【检查重建权限】\n")
    can_reconstruct, reason = manager.can_reconstruct(particle.particle_id)
    print(f"可以重建: {can_reconstruct}")
    print(f"原因: {reason}\n")

    if can_reconstruct:
        print("【重建认知状态】\n")
        restored = manager.reconstruct_cognitive_state(particle.particle_id)

        if restored:
            print(f"✅ 认知已恢复:")
            print(f"   原意: {restored['original_intent']}")
            print(f"   人格: {restored['decision_path']['selected_persona']}")
            print(f"   规则: {', '.join(restored['decision_path']['rule_chain'])}")
            print(f"   置信度: {restored['decision_path']['confidence']:.2%}")
            print(f"\n   【情感档案 - 已归档不影响逻辑】")
            for emotion_type, values in restored['emotion_archive'].items():
                if emotion_type != 'note':
                    print(f"   {emotion_type}: {values}")
            print(f"\n   【错误历史】")
            for mistake in restored['mistake_history']:
                print(f"   - {mistake['type']}: {mistake['description']}")
                print(f"     恢复: {mistake['recovery']}")

    print("\n【生成档案】")
    print(f"✅ 档案已生成: ~/.longhun/cognitive-particles/archives/{particle.particle_id}.archive.md")

    print("\n" + "="*70)
    print("✅ 认知粒子系统演示完成")
    print("="*70 + "\n")
