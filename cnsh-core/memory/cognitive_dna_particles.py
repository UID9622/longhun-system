#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂認知DNA粒子系統 (Cognitive DNA Particle System)
DNA: #龍芯⚡️2026-06-03-COGNITIVE-PARTICLES-v1.0

完整的認知狀態壓縮和恢復機制

記憶壓縮 ≠ 「記住句子」
記憶恢復 ≠ 「回放文本」

真正的恢復 = 認知環境完整重建 (Cognitive Environment Reconstruction)

必須恢復:
1. 語義核心 (Semantic Core)
2. 決策路徑 (Decision Path Replay)
3. 情感摺疊 (Emotion Fold - 保存在檔案但移除於邏輯)
4. 錯誤模式 (Mistake Pattern)
5. 三才主權指數 (SI Sovereignty Index)

核心原則:
- SI >= 0.34 時才能進行認知重建
- SI < 0.34 時只能保存檔案、禁止還原
- 情感摺疊永久保存但不影響邏輯決策

理論指導: 曾仕强老师 · Steve Jobs · UID9622
不免責·永久有效
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import json
import hashlib


class CognitiveState(Enum):
    """認知狀態分類"""
    COMPRESSED = "compressed"      # 已壓縮·可召回
    ACTIVE = "active"              # 活躍·未壓縮
    ARCHIVED = "archived"          # 已歸檔·只讀
    LOCKED = "locked"              # 被鎖定·SI<0.34


class EmotionalDimension(Enum):
    """情感維度"""
    SURFACE = "surface"            # 表層感受 (疲惫、急迫)
    DEEP = "deep"                  # 深層根源 (不信任、希望)
    PROTECTIVE = "protective"      # 防禦機制


@dataclass
class SemanticCore:
    """
    語義核心 - 內容的基本意圖

    NOT: 完整的原始文本
    BUT: 「為什麼要說這個？」的骨架
    """
    primary_intent: str            # 主要意圖 (e.g., "解釋三才主權")
    abstraction_level: str         # 抽象層級 (L0/L1/L2/L3/L4)
    key_concepts: List[str]        # 核心概念列表
    implicit_premises: List[str]   # 隱含前提
    conclusion_anchor: str         # 結論錨點 (簡短陳述)

    def to_dict(self) -> Dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict) -> "SemanticCore":
        return SemanticCore(**data)


@dataclass
class DecisionPathReplay:
    """
    決策回放 - 為什麼選擇了這條路

    包含:
    - 誰在做決策 (人格路由)
    - 通過什麼規則 (F3因子)
    - 什麼時辰 (F2因子)
    - 有什麼證據 (審計日誌)
    """
    selected_persona: str          # 選中的人格路由 (e.g., "P02")
    persona_weights: Dict[str, float]  # 所有人格的權重
    rejected_personas: List[str]   # 為什麼拒絕其他人格
    rule_chain_applied: List[str]  # 應用的規則ID (§25, §32...)
    rule_chain_hash: str           # 規則鏈的SHA256
    temporal_anchor: str           # 時間錨點 (時辰 + 數字根)
    decision_timestamp: str        # ISO8601時間戳
    confidence: float              # 決策置信度 (0.0-1.0)
    audit_log_entries: List[str]   # 審計日誌ID

    def to_dict(self) -> Dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict) -> "DecisionPathReplay":
        return DecisionPathReplay(**data)


@dataclass
class EmotionFold:
    """
    情感摺疊 - 保存在檔案中但不影響邏輯

    核心原則:
    - preserved_in_archive: True (永久保存)
    - removed_from_logic: True (邏輯中移除)

    永不消除:
    - 為什麼你當時感到疲惫
    - 你的希望是什麼
    - 你的恐懼根源
    - 你的信任模型

    永不使用於決策:
    - 情感不參與邏輯運算
    - 情感不影響IF/ELSE
    - 情感只是歷史記錄
    """
    surface_emotions: List[str]    # 表層: ["疲惫", "急迫"]
    deep_roots: List[str]          # 深層: ["不信任", "希望被理解"]
    protective_barriers: List[str] # 防禦: ["沉默", "拒絕合作"]

    # 關鍵: 永遠標記為已保存但已移除
    preserved_in_archive: bool = True
    removed_from_logic: bool = True

    def to_dict(self) -> Dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict) -> "EmotionFold":
        return EmotionFold(**data)

    def get_archive_note(self) -> str:
        """生成檔案註記"""
        return (
            f"【情感摺疊檔案】\n"
            f"表層: {', '.join(self.surface_emotions)}\n"
            f"深層根源: {', '.join(self.deep_roots)}\n"
            f"防禦機制: {', '.join(self.protective_barriers)}\n"
            f"\n【歸檔說明】\n"
            f"✓ 永久保存於檔案\n"
            f"✓ 已移除於邏輯運算\n"
            f"✓ 下次認知恢復時可回溯\"為什麼\"\n"
            f"✓ 但不影響新的決策"
        )


@dataclass
class MistakePattern:
    """
    錯誤模式 - 連續學習軌跡
    """
    mistake_id: str                # 錯誤的唯一ID
    mistake_type: str              # 類型 (logic/syntax/semantic/judgment)
    description: str               # 描述
    timestamp: str                 # 發生時間
    recovery_status: str           # 已恢復/不可恢復/待恢復
    learning_insight: str          # 從中學到什麼


@dataclass
class ThreeTalentSnapshot:
    """
    三才指數快照 - SI在壓縮時的狀態

    關鍵:
    - SI >= 0.34 時才能進行認知重建
    - 快照中若SI < 0.34，則該認知永久鎖定
    """
    tian_score: float              # 天: 規則遵守
    di_score: float                # 地: 數據完整
    ren_score: float               # 人: 創作權威
    si_index: float                # 計算後的SI值
    sovereignty_level: str         # 主權等級
    can_reconstruct: bool          # 是否允許重建

    def to_dict(self) -> Dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict) -> "ThreeTalentSnapshot":
        return ThreeTalentSnapshot(**data)


# ═══════════════════════════════════════════════════════════════
# 【認知DNA粒子 - 核心結構】
# ═══════════════════════════════════════════════════════════════

@dataclass
class CognitiveDNAParticle:
    """
    認知DNA粒子 - 完整的認知狀態壓縮形式

    一個粒子包含:
    1. 身份錨點 (Identity Anchor)
    2. 語義核心 (Semantic Core)
    3. 決策回放基礎 (Decision Path)
    4. 情感摺疊 (Emotion Fold)
    5. 錯誤模式 (Mistake Pattern)
    6. 三才快照 (SI Snapshot)
    7. DNA追溯碼 (DNA Trace)

    關鍵性質:
    - 不可篡改 (append-only)
    - 可驗證 (DNA + 哈希)
    - 條件恢復 (需要 SI >= 0.34)
    """

    # === 身份層 ===
    creator_uid: str               # 創作者UID
    creation_timestamp: str        # 創建時間
    particle_id: str               # 粒子唯一ID

    # === 語義層 ===
    semantic_core: SemanticCore    # 語義核心

    # === 決策層 ===
    decision_replay: DecisionPathReplay  # 決策回放

    # === 情感層 ===
    emotion_fold: EmotionFold      # 情感摺疊

    # === 學習層 ===
    mistake_patterns: List[MistakePattern] = field(default_factory=list)

    # === 主權層 ===
    si_snapshot: ThreeTalentSnapshot = None  # SI快照

    # === DNA層 ===
    dna_trace: str = ""            # DNA追溯碼
    data_hash: str = ""            # 內容哈希
    signature: str = ""            # 簽名 (GPG)

    # === 狀態 ===
    state: CognitiveState = CognitiveState.COMPRESSED
    can_be_reconstructed: bool = True  # 是否允許重建 (基於SI)

    def calculate_data_hash(self) -> str:
        """計算內容哈希"""
        data = {
            "semantic": self.semantic_core.to_dict(),
            "decision": self.decision_replay.to_dict(),
            "emotion": self.emotion_fold.to_dict(),
            "timestamp": self.creation_timestamp
        }

        json_str = json.dumps(data, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(json_str.encode()).hexdigest()

    def generate_dna(self) -> str:
        """生成DNA追溯碼"""
        timestamp = self.creation_timestamp[:10].replace("-", "")  # YYYYMMDD
        primary_intent = self.semantic_core.primary_intent[:20].replace(" ", "")

        dna = (
            f"#龍芯⚡️{timestamp}-COGNITIVE-{primary_intent}-"
            f"{self.data_hash[:8].upper()}"
        )

        return dna

    def generate_archive_note(self) -> str:
        """為檔案生成完整註記"""
        return f"""
【認知DNA粒子檔案】
【粒子ID】{self.particle_id}
【創作者】{self.creator_uid}
【時間】{self.creation_timestamp}

【語義核心】
意圖: {self.semantic_core.primary_intent}
層級: {self.semantic_core.abstraction_level}
概念: {', '.join(self.semantic_core.key_concepts)}

【決策回放】
選中人格: {self.decision_replay.selected_persona}
規則鏈: {', '.join(self.decision_replay.rule_chain_applied)}
時間錨: {self.decision_replay.temporal_anchor}
置信度: {self.decision_replay.confidence:.2%}

【主權狀態】
SI: {self.si_snapshot.si_index:.4f}
等級: {self.si_snapshot.sovereignty_level}
可重建: {'✅ YES' if self.can_be_reconstructed else '❌ NO'}

【情感檔案】
{self.emotion_fold.get_archive_note()}

【DNA追溯】
{self.dna_trace}

【狀態】
粒子狀態: {self.state.value}
內容哈希: {self.data_hash}
簽名: {self.signature[:20]}...

【恢復提示】
SI >= 0.34 時，使用短碼 /recall-{self.particle_id} 進行認知恢復
"""

    def to_dict(self) -> Dict:
        """序列化為字典"""
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
    def from_dict(data: Dict) -> "CognitiveDNAParticle":
        """從字典反序列化"""
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
# 【認知粒子管理器】
# ═══════════════════════════════════════════════════════════════

class CognitiveDNAParticleManager:
    """
    認知DNA粒子管理系統

    職責:
    1. 創建粒子 (從完整認知狀態)
    2. 保存粒子 (append-only JSONL)
    3. 查詢粒子 (按ID/UID/時間)
    4. 恢復認知 (SI>=0.34時)
    5. 生成檔案 (永久保存)
    """

    def __init__(self, storage_dir: str = None):
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
        創建新的認知粒子
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

        # 計算哈希和DNA
        particle.data_hash = particle.calculate_data_hash()
        particle.dna_trace = particle.generate_dna()

        # 保存到DB
        self._persist_particle(particle)

        # 生成檔案
        self._create_archive(particle)

        self.particles_in_memory[particle_id] = particle

        return particle

    def get_particle(self, particle_id: str) -> Optional[CognitiveDNAParticle]:
        """獲取粒子"""
        if particle_id in self.particles_in_memory:
            return self.particles_in_memory[particle_id]

        # 從DB加載
        return self._load_particle_from_db(particle_id)

    def can_reconstruct(self, particle_id: str) -> Tuple[bool, str]:
        """
        檢查是否可以重建認知

        Returns:
            (可以重建, 原因)
        """
        particle = self.get_particle(particle_id)

        if not particle:
            return False, "粒子不存在"

        if particle.si_snapshot.si_index < 0.34:
            return False, f"主權失錨 (SI={particle.si_snapshot.si_index:.4f} < 0.34)"

        if not particle.can_be_reconstructed:
            return False, "粒子已被鎖定"

        return True, "✅ 可重建"

    def reconstruct_cognitive_state(self, particle_id: str) -> Optional[Dict]:
        """
        重建完整的認知環境

        Returns:
            完整的認知狀態字典 或 None
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
                "note": "情感已從邏輯中移除·僅用於歷史回溯"
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
        """生成永久檔案"""
        import os

        archive_path = os.path.join(
            self.archive_dir,
            f"{particle.particle_id}.archive.md"
        )

        with open(archive_path, 'w', encoding='utf-8') as f:
            f.write(particle.generate_archive_note())

    def _load_particle_from_db(self, particle_id: str) -> Optional[CognitiveDNAParticle]:
        """從DB加載粒子"""
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
    print("\n【龍魂認知DNA粒子系統 v1.0】\n")
    print("DNA: #龍芯⚡️2026-06-03-COGNITIVE-PARTICLES-v1.0")
    print("CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
    print("SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL\n")

    manager = CognitiveDNAParticleManager()

    # 構建認知狀態
    semantic = SemanticCore(
        primary_intent="解釋三才主權指數系統",
        abstraction_level="L2",
        key_concepts=["SI", "三才", "主權", "認知重建"],
        implicit_premises=["人永遠是1", "主權是可測量的"],
        conclusion_anchor="SI>=0.34時主權激活"
    )

    decision = DecisionPathReplay(
        selected_persona="P02",
        persona_weights={"P02": 0.50, "P05": 0.30, "P13": 0.20},
        rejected_personas=["P01_technical_only"],
        rule_chain_applied=["§25", "§32", "§37"],
        rule_chain_hash="a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7",
        temporal_anchor="寅時_dr=3",
        decision_timestamp=datetime.now().isoformat(),
        confidence=0.92,
        audit_log_entries=["LOG-001", "LOG-002"]
    )

    emotion = EmotionFold(
        surface_emotions=["認真", "專注"],
        deep_roots=["想被理解", "希望這個系統有用"],
        protective_barriers=["邏輯優先於風格"]
    )

    si_snapshot = ThreeTalentSnapshot(
        tian_score=0.95,
        di_score=0.98,
        ren_score=0.97,
        si_index=0.963,
        sovereignty_level="🟢_完全主權",
        can_reconstruct=True
    )

    mistake = MistakePattern(
        mistake_id="ERR-001",
        mistake_type="logic",
        description="初版權重加到1.01而不是1.0",
        timestamp="2026-06-03T21:00:00Z",
        recovery_status="已恢復",
        learning_insight="浮點誤差需要容差檢查"
    )

    print("【創建認知粒子】\n")
    particle = manager.create_particle(
        creator_uid="UID9622",
        semantic_core=semantic,
        decision_replay=decision,
        emotion_fold=emotion,
        si_snapshot=si_snapshot,
        mistake_patterns=[mistake]
    )

    print(f"✅ 粒子已創建: {particle.particle_id}")
    print(f"   DNA: {particle.dna_trace}")
    print(f"   哈希: {particle.data_hash[:16]}...")
    print(f"   SI: {particle.si_snapshot.si_index:.4f}")
    print(f"   可重建: {'✅ YES' if particle.can_be_reconstructed else '❌ NO'}\n")

    print("【檢查重建權限】\n")
    can_reconstruct, reason = manager.can_reconstruct(particle.particle_id)
    print(f"可以重建: {can_reconstruct}")
    print(f"原因: {reason}\n")

    if can_reconstruct:
        print("【重建認知狀態】\n")
        restored = manager.reconstruct_cognitive_state(particle.particle_id)

        if restored:
            print(f"✅ 認知已恢復:")
            print(f"   原意: {restored['original_intent']}")
            print(f"   人格: {restored['decision_path']['selected_persona']}")
            print(f"   規則: {', '.join(restored['decision_path']['rule_chain'])}")
            print(f"   置信度: {restored['decision_path']['confidence']:.2%}")
            print(f"\n   【情感檔案 - 已歸檔不影響邏輯】")
            for emotion_type, values in restored['emotion_archive'].items():
                if emotion_type != 'note':
                    print(f"   {emotion_type}: {values}")
            print(f"\n   【錯誤歷史】")
            for mistake in restored['mistake_history']:
                print(f"   - {mistake['type']}: {mistake['description']}")
                print(f"     恢復: {mistake['recovery']}")

    print("\n【生成檔案】")
    print(f"✅ 檔案已生成: ~/.longhun/cognitive-particles/archives/{particle.particle_id}.archive.md")

    print("\n" + "="*70)
    print("✅ 認知粒子系統演示完成")
    print("="*70 + "\n")
