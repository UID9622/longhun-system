#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 记忆单元 · Memory Unit
DNA: #龍芯⚡️2026-05-22-MEMORY-UNIT-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者: UID9622 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）

记忆单元是记忆打包算法的基本数据结构
每个记忆单元包含：内容、元数据、DNA追溯、五行属性
"""

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any


class MemoryType(Enum):
    """记忆类型 · 五层分级"""
    L0_ETERNAL = "L0"      # 永恒层 · α=0 · 不可变
    L1_CENTURY = "L1"      # 百年层 · 封印级
    L2_DECADE = "L2"       # 十年层 · 战略级
    L3_DAILY = "L3"        # 日常层 · 操作级
    L4_INSTANT = "L4"      # 瞬时层 · 毫秒级


class AccessLevel(Enum):
    """访问级别"""
    PUBLIC = "public"           # 公开
    PRIVATE = "private"         # 私有
    SEALED = "sealed"           # 封印（需密钥解封）
    SHAMIR = "shamir"           # Shamir分片（需多密钥）


class WuXing(Enum):
    """五行属性"""
    JIN = "金"    # 金 · 收敛 · 6/7
    MU = "木"     # 木 · 生发 · 1/2
    SHUI = "水"   # 水 · 润下 · 8/9
    HUO = "火"    # 火 · 炎上 · 3/4
    TU = "土"     # 土 · 中和 · 5


@dataclass
class MemoryUnit:
    """
    记忆单元 · 最小存储单位

    每个记忆单元是一个不可分割的信息包
    包含原始内容、压缩内容、元数据、DNA追溯
    """

    # 唯一标识
    unit_id: str = ""

    # 内容
    content: bytes = field(default_factory=bytes)
    content_type: str = "text/plain"  # MIME类型
    original_size: int = 0
    compressed_size: int = 0

    # 分类
    memory_type: MemoryType = MemoryType.L3_DAILY
    access_level: AccessLevel = AccessLevel.PRIVATE

    # 五行属性（基于内容数字根计算）
    wuxing: WuXing = WuXing.TU
    digital_root: int = 5

    # 时间戳
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None  # L4瞬时层有过期时间

    # 来源追溯
    source_url: str = ""
    source_title: str = ""
    source_author: str = "UID9622"

    # DNA追溯
    dna: str = ""
    parent_dna: str = ""  # 父记忆DNA（用于追溯链）

    # 哈希验证
    sha256: str = ""
    gpg_signature: str = ""

    # 存储位置（分布式）
    storage_nodes: List[str] = field(default_factory=list)

    # 元数据
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """初始化后计算属性"""
        if not self.unit_id:
            self.unit_id = self._generate_id()
        if not self.dna:
            self.dna = self._generate_dna()
        if not self.sha256 and self.content:
            self.sha256 = self._compute_hash()
        self._compute_wuxing()

    def _generate_id(self) -> str:
        """生成唯一ID"""
        ts = datetime.now().strftime("%Y%m%d%H%M%S%f")
        h = hashlib.sha256(f"{ts}|9622|{id(self)}".encode()).hexdigest()[:12]
        return f"MU-{ts[:14]}-{h}"

    def _generate_dna(self) -> str:
        """生成DNA追溯码"""
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        h = hashlib.sha256(f"{self.unit_id}|{ts}".encode()).hexdigest()[:8]
        return f"#龍芯⚡️{ts}-MU-{h}"

    def _compute_hash(self) -> str:
        """计算SHA256哈希"""
        return hashlib.sha256(self.content).hexdigest()

    def _compute_wuxing(self):
        """计算五行属性（基于数字根）"""
        if self.content:
            char_sum = sum(self.content)
            dr = char_sum
            while dr > 9:
                dr = sum(int(d) for d in str(dr))
            self.digital_root = dr if dr > 0 else 9

            # 数字根 → 五行映射
            wuxing_map = {
                1: WuXing.MU, 2: WuXing.MU,     # 木
                3: WuXing.HUO, 4: WuXing.HUO,   # 火
                5: WuXing.TU,                   # 土
                6: WuXing.JIN, 7: WuXing.JIN,   # 金
                8: WuXing.SHUI, 9: WuXing.SHUI  # 水
            }
            self.wuxing = wuxing_map.get(self.digital_root, WuXing.TU)

    def set_content(self, data: bytes, content_type: str = "text/plain"):
        """设置内容"""
        self.content = data
        self.content_type = content_type
        self.original_size = len(data)
        self.compressed_size = len(data)  # 压缩后更新
        self.sha256 = self._compute_hash()
        self._compute_wuxing()
        self.modified_at = datetime.now()

    def set_text_content(self, text: str):
        """设置文本内容"""
        self.set_content(text.encode('utf-8'), "text/plain; charset=utf-8")

    def get_text_content(self) -> str:
        """获取文本内容"""
        if self.content_type.startswith("text/"):
            return self.content.decode('utf-8')
        return ""

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（用于JSON序列化）"""
        return {
            "unit_id": self.unit_id,
            "content_type": self.content_type,
            "original_size": self.original_size,
            "compressed_size": self.compressed_size,
            "memory_type": self.memory_type.value,
            "access_level": self.access_level.value,
            "wuxing": self.wuxing.value,
            "digital_root": self.digital_root,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "source_url": self.source_url,
            "source_title": self.source_title,
            "source_author": self.source_author,
            "dna": self.dna,
            "parent_dna": self.parent_dna,
            "sha256": self.sha256,
            "gpg_signature": self.gpg_signature,
            "storage_nodes": self.storage_nodes,
            "tags": self.tags,
            "metadata": self.metadata,
        }

    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], content: bytes = b"") -> "MemoryUnit":
        """从字典创建"""
        unit = cls(
            unit_id=data.get("unit_id", ""),
            content=content,
            content_type=data.get("content_type", "text/plain"),
            original_size=data.get("original_size", 0),
            compressed_size=data.get("compressed_size", 0),
            memory_type=MemoryType(data.get("memory_type", "L3")),
            access_level=AccessLevel(data.get("access_level", "private")),
            source_url=data.get("source_url", ""),
            source_title=data.get("source_title", ""),
            source_author=data.get("source_author", "UID9622"),
            dna=data.get("dna", ""),
            parent_dna=data.get("parent_dna", ""),
            sha256=data.get("sha256", ""),
            gpg_signature=data.get("gpg_signature", ""),
            storage_nodes=data.get("storage_nodes", []),
            tags=data.get("tags", []),
            metadata=data.get("metadata", {}),
        )

        # 解析时间
        if data.get("created_at"):
            unit.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("modified_at"):
            unit.modified_at = datetime.fromisoformat(data["modified_at"])
        if data.get("expires_at"):
            unit.expires_at = datetime.fromisoformat(data["expires_at"])

        return unit

    def verify_integrity(self) -> bool:
        """验证完整性"""
        if not self.content:
            return True
        return self.sha256 == self._compute_hash()

    def __repr__(self) -> str:
        return (
            f"MemoryUnit(id={self.unit_id}, "
            f"type={self.memory_type.value}, "
            f"size={self.original_size}→{self.compressed_size}, "
            f"wuxing={self.wuxing.value})"
        )


@dataclass
class MemoryChain:
    """
    记忆链 · 多个记忆单元的有序集合

    用于追溯完整的记忆演变历史
    """
    chain_id: str = ""
    units: List[MemoryUnit] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    dna: str = ""

    def __post_init__(self):
        if not self.chain_id:
            ts = datetime.now().strftime("%Y%m%d%H%M%S")
            h = hashlib.sha256(f"chain|{ts}|9622".encode()).hexdigest()[:8]
            self.chain_id = f"MC-{ts}-{h}"
        if not self.dna:
            ts = datetime.now().strftime("%Y%m%d%H%M%S")
            self.dna = f"#龍芯⚡️{ts}-MC-CHAIN"

    def append(self, unit: MemoryUnit):
        """添加记忆单元"""
        if self.units:
            unit.parent_dna = self.units[-1].dna
        self.units.append(unit)

    def get_latest(self) -> Optional[MemoryUnit]:
        """获取最新的记忆单元"""
        return self.units[-1] if self.units else None

    def verify_chain(self) -> bool:
        """验证链完整性"""
        for i, unit in enumerate(self.units):
            if not unit.verify_integrity():
                return False
            if i > 0 and unit.parent_dna != self.units[i-1].dna:
                return False
        return True

    def total_size(self) -> tuple:
        """返回总大小 (原始, 压缩后)"""
        original = sum(u.original_size for u in self.units)
        compressed = sum(u.compressed_size for u in self.units)
        return original, compressed

    def __len__(self) -> int:
        return len(self.units)

    def __repr__(self) -> str:
        orig, comp = self.total_size()
        return f"MemoryChain(id={self.chain_id}, units={len(self)}, size={orig}→{comp})"


# 快捷函数
def create_memory(text: str,
                  memory_type: MemoryType = MemoryType.L3_DAILY,
                  tags: List[str] = None) -> MemoryUnit:
    """快速创建文本记忆单元"""
    unit = MemoryUnit(memory_type=memory_type)
    unit.set_text_content(text)
    if tags:
        unit.tags = tags
    return unit


if __name__ == "__main__":
    # 测试
    print("🧠 记忆单元测试")
    print("=" * 60)

    # 创建记忆单元
    unit = create_memory(
        "龍魂系统是我一年心血的结晶，不能动",
        memory_type=MemoryType.L0_ETERNAL,
        tags=["龍魂", "核心"]
    )

    print(f"记忆单元: {unit}")
    print(f"DNA: {unit.dna}")
    print(f"五行: {unit.wuxing.value} (dr={unit.digital_root})")
    print(f"SHA256: {unit.sha256[:32]}...")
    print(f"完整性: {'✅' if unit.verify_integrity() else '❌'}")
    print()

    # 创建记忆链
    chain = MemoryChain()
    chain.append(create_memory("第一版草稿", MemoryType.L4_INSTANT))
    chain.append(create_memory("第二版修改", MemoryType.L3_DAILY))
    chain.append(create_memory("最终版本", MemoryType.L2_DECADE))

    print(f"记忆链: {chain}")
    print(f"链完整性: {'✅' if chain.verify_chain() else '❌'}")
    print(f"最新版本: {chain.get_latest().dna}")
