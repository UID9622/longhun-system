#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📦 记忆打包器 · Memory Packer
DNA: #龍芯⚡️2026-05-22-MEMORY-PACKER-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者: UID9622 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）

记忆打包器负责：
1. 将原始内容打包成记忆单元
2. 智能分类（L0-L4层级）
3. 自动计算五行属性
4. 生成DNA追溯码
"""

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Union

from .memory_unit import (
    MemoryUnit, MemoryChain, MemoryType, AccessLevel,
    create_memory
)


class MemoryPacker:
    """
    记忆打包器

    负责将各种格式的内容打包成统一的记忆单元
    """

    def __init__(self, base_path: Optional[Path] = None):
        """初始化打包器"""
        self.base_path = base_path or Path.home() / "longhun-system" / "memory-pack"
        self.base_path.mkdir(parents=True, exist_ok=True)

        # 索引文件
        self.index_file = self.base_path / "index.json"
        self.index: Dict[str, Dict] = self._load_index()

    def _load_index(self) -> Dict:
        """加载索引"""
        if self.index_file.exists():
            with open(self.index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"units": {}, "chains": {}, "meta": {"created": datetime.now().isoformat()}}

    def _save_index(self):
        """保存索引"""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)

    def classify_content(self, text: str) -> MemoryType:
        """
        智能分类内容层级

        基于关键词和语义特征自动判断应该放在哪一层
        """
        text_lower = text.lower()

        # L0 永恒层 · 不可动的核心
        l0_keywords = [
            "不能动", "永恒", "永久", "绝对不能", "铁律",
            "immutable", "eternal", "永不", "核心信条"
        ]
        if any(kw in text for kw in l0_keywords):
            return MemoryType.L0_ETERNAL

        # L1 百年层 · 封印级
        l1_keywords = [
            "百年", "遗嘱", "传承", "封印", "Shamir",
            "密钥分片", "后代", "century"
        ]
        if any(kw in text for kw in l1_keywords):
            return MemoryType.L1_CENTURY

        # L2 十年层 · 战略级
        l2_keywords = [
            "十年", "战略", "规划", "架构", "decade",
            "长期", "愿景", "目标"
        ]
        if any(kw in text for kw in l2_keywords):
            return MemoryType.L2_DECADE

        # L4 瞬时层 · 临时性内容
        l4_keywords = [
            "临时", "草稿", "测试", "debug", "tmp",
            "待删除", "instant", "临时记录"
        ]
        if any(kw in text for kw in l4_keywords):
            return MemoryType.L4_INSTANT

        # 默认 L3 日常层
        return MemoryType.L3_DAILY

    def classify_access(self, text: str) -> AccessLevel:
        """
        智能分类访问级别

        基于内容敏感度判断访问级别
        """
        sensitive_keywords = [
            "密码", "password", "token", "secret", "key",
            "私钥", "private", "机密", "保密"
        ]
        if any(kw in text.lower() for kw in sensitive_keywords):
            return AccessLevel.SEALED

        public_keywords = [
            "公开", "public", "发布", "分享", "开源"
        ]
        if any(kw in text.lower() for kw in public_keywords):
            return AccessLevel.PUBLIC

        return AccessLevel.PRIVATE

    def pack_text(self,
                  text: str,
                  memory_type: Optional[MemoryType] = None,
                  access_level: Optional[AccessLevel] = None,
                  tags: List[str] = None,
                  source_url: str = "",
                  source_title: str = "") -> MemoryUnit:
        """
        打包文本内容

        Args:
            text: 文本内容
            memory_type: 记忆类型（可选，自动分类）
            access_level: 访问级别（可选，自动分类）
            tags: 标签列表
            source_url: 来源URL
            source_title: 来源标题

        Returns:
            打包好的记忆单元
        """
        # 自动分类
        if memory_type is None:
            memory_type = self.classify_content(text)
        if access_level is None:
            access_level = self.classify_access(text)

        # 创建记忆单元
        unit = MemoryUnit(
            memory_type=memory_type,
            access_level=access_level,
            source_url=source_url,
            source_title=source_title,
            tags=tags or []
        )
        unit.set_text_content(text)

        # 保存到索引
        self.index["units"][unit.unit_id] = unit.to_dict()
        self._save_index()

        return unit

    def pack_file(self, file_path: Union[str, Path]) -> MemoryUnit:
        """
        打包文件

        Args:
            file_path: 文件路径

        Returns:
            打包好的记忆单元
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {path}")

        # 读取文件内容
        with open(path, 'rb') as f:
            content = f.read()

        # 推断MIME类型
        suffix = path.suffix.lower()
        mime_map = {
            '.txt': 'text/plain',
            '.md': 'text/markdown',
            '.json': 'application/json',
            '.py': 'text/x-python',
            '.js': 'text/javascript',
            '.html': 'text/html',
            '.css': 'text/css',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.pdf': 'application/pdf',
        }
        content_type = mime_map.get(suffix, 'application/octet-stream')

        # 文本文件尝试自动分类
        memory_type = MemoryType.L3_DAILY
        access_level = AccessLevel.PRIVATE
        if content_type.startswith('text/'):
            try:
                text = content.decode('utf-8')
                memory_type = self.classify_content(text)
                access_level = self.classify_access(text)
            except:
                pass

        # 创建记忆单元
        unit = MemoryUnit(
            memory_type=memory_type,
            access_level=access_level,
            source_url=str(path.absolute()),
            source_title=path.name,
            tags=[path.suffix.lstrip('.'), 'file']
        )
        unit.set_content(content, content_type)

        # 保存到索引
        self.index["units"][unit.unit_id] = unit.to_dict()
        self._save_index()

        return unit

    def pack_batch(self, items: List[Union[str, Path, Dict]]) -> List[MemoryUnit]:
        """
        批量打包

        Args:
            items: 内容列表（可以是文本、文件路径或字典）

        Returns:
            记忆单元列表
        """
        units = []
        for item in items:
            if isinstance(item, Path) or (isinstance(item, str) and os.path.exists(item)):
                units.append(self.pack_file(item))
            elif isinstance(item, str):
                units.append(self.pack_text(item))
            elif isinstance(item, dict):
                units.append(self.pack_text(
                    text=item.get('text', ''),
                    tags=item.get('tags', []),
                    source_url=item.get('source_url', ''),
                    source_title=item.get('source_title', '')
                ))
        return units

    def create_chain(self, units: List[MemoryUnit] = None) -> MemoryChain:
        """
        创建记忆链

        Args:
            units: 初始记忆单元列表

        Returns:
            记忆链
        """
        chain = MemoryChain()
        if units:
            for unit in units:
                chain.append(unit)

        # 保存到索引
        self.index["chains"][chain.chain_id] = {
            "chain_id": chain.chain_id,
            "dna": chain.dna,
            "created_at": chain.created_at.isoformat(),
            "unit_count": len(chain),
            "unit_ids": [u.unit_id for u in chain.units]
        }
        self._save_index()

        return chain

    def get_unit(self, unit_id: str) -> Optional[Dict]:
        """获取记忆单元元数据"""
        return self.index["units"].get(unit_id)

    def get_chain(self, chain_id: str) -> Optional[Dict]:
        """获取记忆链元数据"""
        return self.index["chains"].get(chain_id)

    def list_units(self, memory_type: Optional[MemoryType] = None) -> List[Dict]:
        """列出记忆单元"""
        units = list(self.index["units"].values())
        if memory_type:
            units = [u for u in units if u.get("memory_type") == memory_type.value]
        return units

    def stats(self) -> Dict:
        """统计信息"""
        units = list(self.index["units"].values())
        chains = list(self.index["chains"].values())

        total_original = sum(u.get("original_size", 0) for u in units)
        total_compressed = sum(u.get("compressed_size", 0) for u in units)

        by_type = {}
        for u in units:
            t = u.get("memory_type", "L3")
            by_type[t] = by_type.get(t, 0) + 1

        by_wuxing = {}
        for u in units:
            w = u.get("wuxing", "土")
            by_wuxing[w] = by_wuxing.get(w, 0) + 1

        return {
            "total_units": len(units),
            "total_chains": len(chains),
            "total_original_size": total_original,
            "total_compressed_size": total_compressed,
            "compression_ratio": total_compressed / total_original if total_original > 0 else 1.0,
            "by_memory_type": by_type,
            "by_wuxing": by_wuxing,
            "dna": f"#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-STATS"
        }


# 全局实例
_packer: Optional[MemoryPacker] = None


def get_packer() -> MemoryPacker:
    """获取全局打包器实例"""
    global _packer
    if _packer is None:
        _packer = MemoryPacker()
    return _packer


if __name__ == "__main__":
    # 测试
    print("📦 记忆打包器测试")
    print("=" * 60)

    packer = MemoryPacker()

    # 打包文本
    unit1 = packer.pack_text("龍魂系统核心信条，永恒不可动")
    print(f"打包结果: {unit1}")
    print(f"自动分类: {unit1.memory_type.value} ({unit1.access_level.value})")

    unit2 = packer.pack_text("今天的工作日志记录")
    print(f"打包结果: {unit2}")
    print(f"自动分类: {unit2.memory_type.value}")

    unit3 = packer.pack_text("这是一个临时测试文件，待删除")
    print(f"打包结果: {unit3}")
    print(f"自动分类: {unit3.memory_type.value}")

    # 统计
    print()
    print("📊 统计信息:")
    stats = packer.stats()
    print(f"   总单元数: {stats['total_units']}")
    print(f"   按层级: {stats['by_memory_type']}")
    print(f"   按五行: {stats['by_wuxing']}")
