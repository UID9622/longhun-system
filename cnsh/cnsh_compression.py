#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·对话记忆压缩系统 v1.0
Semantic Memory Compression: 思考胶囊 × 时间胶囊

DNA: #龍芯⚡️2026-05-25-COMPRESSION-SYSTEM-v1.0
UID: 9622
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

根据 📦 对话记忆压缩 + LU 全文压缩归集器 实现
- 对话流 → 语义包
- 多轮对话 → 思考胶囊（精化摘要）
- 时间轴 → 时间胶囊（时间戳注记）
- 压缩结果 → MEMORY_INDEX.jsonl（append-only）

不烧 token·本地计算·纯语义压缩

理论指导: 曾仕强老师
献礼: 龍魂系统·永恒守护
"""

import json
import hashlib
import math
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum


# ════════════════════════════════════════════════════════
# 第一步：语义压缩算法（本地计算）
# ════════════════════════════════════════════════════════

class CompressionLevel(Enum):
    """压缩级别"""
    RAW = 0  # 原始
    LIGHT = 1  # 轻度（保留细节）
    MEDIUM = 2  # 中度（平衡）
    HEAVY = 3  # 重度（极致压缩）


@dataclass
class SemanticToken:
    """语义令牌（最小信息单位）"""
    text: str
    importance: float  # 0.0-1.0
    entity_type: str  # person / action / concept / reference
    context_window: int  # 前后文本距离


class SemanticCompressor:
    """语义压缩器（无 ML·纯算法）"""

    def __init__(self, compression_level: CompressionLevel = CompressionLevel.MEDIUM):
        self.level = compression_level
        self.stopwords = {
            "的", "是", "了", "和", "在", "一", "个", "中", "有", "吗",
            "这", "那", "我", "你", "他", "她", "it", "the", "a", "an"
        }

    def tokenize(self, text: str) -> List[SemanticToken]:
        """分词与语义标记"""
        words = text.split()
        tokens = []

        for i, word in enumerate(words):
            if word not in self.stopwords and len(word) > 2:
                # 简单启发式重要度评分
                importance = 1.0 - (len(self.stopwords & set(text.split()[max(0, i-3):i+4])) / 7)
                importance = max(0.0, min(1.0, importance))

                token = SemanticToken(
                    text=word,
                    importance=importance,
                    entity_type=self._classify_entity(word),
                    context_window=min(i, len(words) - i - 1)
                )
                tokens.append(token)

        return tokens

    def _classify_entity(self, word: str) -> str:
        """简单实体分类"""
        if word[0].isupper():
            return "person"
        elif word.endswith("了") or word.endswith("做"):
            return "action"
        else:
            return "concept"

    def compress(self, text: str) -> Dict[str, Any]:
        """压缩对话"""
        tokens = self.tokenize(text)

        # 按重要度排序
        sorted_tokens = sorted(tokens, key=lambda t: t.importance, reverse=True)

        # 根据压缩级别选择保留比例
        retention_rate = {
            CompressionLevel.RAW: 1.0,
            CompressionLevel.LIGHT: 0.7,
            CompressionLevel.MEDIUM: 0.5,
            CompressionLevel.HEAVY: 0.25,
        }[self.level]

        keep_count = max(1, int(len(sorted_tokens) * retention_rate))
        key_tokens = sorted_tokens[:keep_count]

        # 重新排序为原始顺序
        key_tokens_ordered = sorted(key_tokens, key=lambda t: tokens.index(t))

        # 生成摘要
        summary = " ".join([t.text for t in key_tokens_ordered])

        compression_ratio = 1.0 - (len(summary) / max(1, len(text)))

        return {
            "original_length": len(text),
            "compressed_length": len(summary),
            "compression_ratio": round(compression_ratio, 3),
            "compression_level": self.level.name,
            "key_tokens": len(key_tokens),
            "summary": summary,
        }


# ════════════════════════════════════════════════════════
# 第二步：思考胶囊 × 时间胶囊
# ════════════════════════════════════════════════════════

@dataclass
class ThinkingCapsule:
    """思考胶囊：多轮对话提炼"""
    capsule_id: str
    timestamp: str
    turns_count: int
    topic: str
    key_decisions: List[str]
    conclusion: str
    compressed_dialogue: str
    dna: str


@dataclass
class TimeCapsule:
    """时间胶囊：时间轴注记"""
    capsule_id: str
    created_at: str
    updated_at: str
    lifespan_days: int
    content_type: str  # dialogue / decision / memory / artifact
    reference_dna: str


class MemoryCompressor:
    """记忆压缩系统（思考胶囊 + 时间胶囊）"""

    def __init__(self, compression_dir: str = "~/.cnsh/memory"):
        self.compression_dir = Path(compression_dir).expanduser()
        self.compression_dir.mkdir(parents=True, exist_ok=True)
        self.semantic_compressor = SemanticCompressor(CompressionLevel.MEDIUM)
        self.memory_index: List[Dict] = []

    def compress_dialogue(self, dialogue_turns: List[Dict]) -> ThinkingCapsule:
        """压缩多轮对话"""
        capsule_id = f"tc-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # 合并所有轮次文本
        all_text = " ".join([turn.get("text", "") for turn in dialogue_turns])

        # 语义压缩
        compressed = self.semantic_compressor.compress(all_text)

        # 提取关键决策（简单启发式）
        decisions = []
        for turn in dialogue_turns:
            if any(keyword in turn.get("text", "").lower() for keyword in ["决定", "要求", "同意", "拒绝"]):
                decisions.append(turn.get("text", "")[:50])

        # 生成结论
        conclusion = f"包含 {len(dialogue_turns)} 轮对话，{len(decisions)} 项关键决策"

        # 生成 DNA
        dna_hash = hashlib.sha256(all_text.encode()).hexdigest()[:8]
        dna = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d-%H:%M')}-THINKING-CAPSULE-{dna_hash}"

        capsule = ThinkingCapsule(
            capsule_id=capsule_id,
            timestamp=datetime.now().isoformat(),
            turns_count=len(dialogue_turns),
            topic=dialogue_turns[0].get("topic", "未分类"),
            key_decisions=decisions,
            conclusion=conclusion,
            compressed_dialogue=compressed["summary"],
            dna=dna,
        )

        return capsule

    def create_time_capsule(self, capsule: ThinkingCapsule) -> TimeCapsule:
        """创建时间胶囊"""
        time_capsule = TimeCapsule(
            capsule_id=capsule.capsule_id,
            created_at=capsule.timestamp,
            updated_at=datetime.now().isoformat(),
            lifespan_days=0,
            content_type="dialogue",
            reference_dna=capsule.dna,
        )
        return time_capsule

    def index_memory(self, capsule: ThinkingCapsule, time_capsule: TimeCapsule) -> str:
        """索引到 MEMORY_INDEX（append-only）"""
        index_entry = {
            "timestamp": datetime.now().isoformat(),
            "thinking_capsule_id": capsule.capsule_id,
            "time_capsule_id": time_capsule.capsule_id,
            "dna": capsule.dna,
            "topic": capsule.topic,
            "turns_count": capsule.turns_count,
            "key_decisions_count": len(capsule.key_decisions),
            "compressed_length": len(capsule.compressed_dialogue),
            "created_at": capsule.timestamp,
            "content_type": time_capsule.content_type,
        }

        # 追加到索引
        index_file = self.compression_dir / "MEMORY_INDEX.jsonl"
        with open(index_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(index_entry, ensure_ascii=False) + "\n")

        self.memory_index.append(index_entry)

        return capsule.dna

    def export_compression_summary(self) -> str:
        """导出压缩总结"""
        summary = "# 💾 记忆压缩系统运行报告\n\n"
        summary += f"**生成时间**: {datetime.now().isoformat()}\n\n"

        summary += "## 思考胶囊统计\n\n"
        summary += f"- 总胶囊数: {len(self.memory_index)}\n"
        summary += f"- 总轮次: {sum(e.get('turns_count', 0) for e in self.memory_index)}\n"
        summary += f"- 总决策数: {sum(e.get('key_decisions_count', 0) for e in self.memory_index)}\n"
        summary += f"- 平均压缩长度: {sum(e.get('compressed_length', 0) for e in self.memory_index) // max(1, len(self.memory_index))}\n\n"

        summary += "## 索引记录（最近 5 条）\n\n"
        for entry in self.memory_index[-5:]:
            summary += f"- **{entry['topic']}** ({entry['dna']})\n"
            summary += f"  - 轮次: {entry['turns_count']} | 决策: {entry['key_decisions_count']}\n"
            summary += f"  - 类型: {entry['content_type']}\n\n"

        return summary


# ════════════════════════════════════════════════════════
# 示例与测试
# ════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "="*60)
    print("💾 龍魂对话记忆压缩 v1.0")
    print(f"   DNA: #龍芯⚡️2026-05-25-COMPRESSION-SYSTEM-v1.0")
    print("="*60 + "\n")

    # 测试 1: 语义压缩
    print("📍 测试 1: 语义压缩")
    text = "今天我们讨论了三个重要的决策：第一是关于系统架构的优化，第二是关于数据安全的加固措施，第三是关于用户体验的改进方案。"
    compressor = SemanticCompressor(CompressionLevel.MEDIUM)
    result = compressor.compress(text)
    print(f"   原始长度: {result['original_length']}")
    print(f"   压缩长度: {result['compressed_length']}")
    print(f"   压缩率: {result['compression_ratio']}")
    print(f"   摘要: {result['summary']}\n")

    # 测试 2: 思考胶囊
    print("📍 测试 2: 思考胶囊")
    dialogue = [
        {"text": "下一步应该怎么做", "topic": "决策"},
        {"text": "我的想法是先完成核心功能再优化", "topic": "决策"},
        {"text": "同意，但需要加强安全检查", "topic": "决策"},
    ]
    memory_compressor = MemoryCompressor()
    capsule = memory_compressor.compress_dialogue(dialogue)
    print(f"   胶囊ID: {capsule.capsule_id}")
    print(f"   轮次: {capsule.turns_count}")
    print(f"   决策数: {len(capsule.key_decisions)}")
    print(f"   DNA: {capsule.dna}\n")

    # 测试 3: 时间胶囊
    print("📍 测试 3: 时间胶囊")
    time_capsule = memory_compressor.create_time_capsule(capsule)
    print(f"   创建时间: {time_capsule.created_at}")
    print(f"   类型: {time_capsule.content_type}")
    print(f"   参考DNA: {time_capsule.reference_dna}\n")

    # 测试 4: 索引
    print("📍 测试 4: 记忆索引")
    dna = memory_compressor.index_memory(capsule, time_capsule)
    print(f"   索引完成，DNA: {dna}\n")

    # 测试 5: 导出报告
    print("📍 测试 5: 压缩报告")
    summary = memory_compressor.export_compression_summary()
    print(summary[:400] + "...\n")

    print("="*60)
    print("✅ 记忆压缩系统初始化完成")
    print("="*60 + "\n")
    print("🐉 龍魂压缩 · 本地计算 · 永不外送 · UID9622不免责")
