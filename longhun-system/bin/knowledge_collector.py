#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三色知识库采集引擎
DNA: #龍芯⚡️2026-04-08-KNOWLEDGE-COLLECTOR-v1.0

设计理念:
- 不抄知识库，只取碎片
- 拆解为最小单元：标签/词/句
- 可分可合，灵活重组
- DNA兼容度筛选
- 不适内容入隔离区
"""

import json
import hashlib
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import re


@dataclass
class KnowledgeFragment:
    """知识碎片 - 最小知识单元"""
    id: str
    type: str  # tag, term, phrase, sentence
    content: str
    content_hash: str
    source_id: str
    source_url: str
    source_title: str
    crawl_time: str
    category: str
    palace: int
    tags: List[str]
    language: str
    compatibility_score: float
    keywords_matched: List[str]
    persona_fit: List[str]
    status: str = "pending"
    status_reason: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class DNACompatibilityChecker:
    """DNA兼容度检测器"""
    
    # 三才关键词库（从luoshu_router.py继承）
    SANCAI_KEYWORDS = {
        "tian": ["算法", "天道", "规则", "逻辑", "智能", "优化", "模型", "计算", "AI", "神经网络"],
        "di": ["存储", "数据", "资源", "环境", "架构", "系统", "基础", "硬件", "网络", "协议"],
        "ren": ["交互", "体验", "用户", "界面", "情感", "人格", "对话", "服务", "应用", "产品"]
    }
    
    # 71人格适配关键词（简化版）
    PERSONA_KEYWORDS = {
        "P01_诸葛": ["算法", "策略", "优化", "逻辑"],
        "P02_老子": ["天道", "自然", "平衡", "无为"],
        "P03_孔子": ["仁义", "教育", "礼仪", "人文"],
        "P05_曾老": ["易经", "预测", "变化", "智慧"],
        "P10_宝宝": ["可爱", "陪伴", "温暖", "守护"],
        "P20_技术官": ["架构", "代码", "系统", "实现"],
        "P30_科学家": ["量子", "基因", "研究", "实验"],
        "P40_艺术家": ["创意", "美感", "设计", "表达"]
    }
    
    def check(self, content: str, category: str) -> Dict[str, Any]:
        """检测DNA兼容度"""
        content_lower = content.lower()
        
        # 三才匹配
        sancai_matches = []
        for key, words in self.SANCAI_KEYWORDS.items():
            for word in words:
                if word in content_lower:
                    sancai_matches.append(f"{key}:{word}")
        
        # 人格匹配
        persona_fits = []
        for persona, keywords in self.PERSONA_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in content_lower)
            if score > 0:
                persona_fits.append(f"{persona}({score})")
        
        # 计算兼容度分数
        base_score = 0.5
        sancai_bonus = min(len(sancai_matches) * 0.1, 0.3)
        persona_bonus = min(len(persona_fits) * 0.05, 0.2)
        
        # 类别加成
        category_bonus = {
            "quantum_tech": 0.05,
            "dna_tech": 0.05,
            "digital_human": 0.08,  # 人格相关加分
            "metaverse": 0.02,
            "frontier": 0.03
        }.get(category, 0)
        
        final_score = min(base_score + sancai_bonus + persona_bonus + category_bonus, 1.0)
        
        return {
            "compatibility_score": round(final_score, 2),
            "keywords_matched": sancai_matches[:5],
            "persona_fit": persona_fits[:3],
            "reusable": final_score >= 0.7
        }


class KnowledgeCollector:
    """知识采集引擎"""
    
    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path.home() / "longhun-system" / "knowledge-base"
        self.sources_file = self.base_path / "sources" / "tech_frontier_sources.json"
        self.fragments_dir = self.base_path / "fragments"
        self.quarantine_dir = self.base_path / "quarantine"
        self.indexed_dir = self.base_path / "indexed"
        
        self.dna_checker = DNACompatibilityChecker()
        self.sources: Dict[str, Any] = {}
        self._load_sources()
    
    def _load_sources(self):
        """加载知识源配置"""
        if self.sources_file.exists():
            with open(self.sources_file, 'r', encoding='utf-8') as f:
                self.sources = json.load(f)
            print(f"✅ 加载 {self.sources.get('stats', {}).get('total_sources', 0)} 个知识源")
    
    def _hash_content(self, content: str) -> str:
        """生成内容哈希"""
        return hashlib.md5(content.encode('utf-8')).hexdigest()[:16]
    
    def _extract_fragments(self, text: str, source_type: str = "auto") -> List[Dict[str, str]]:
        """从文本提取碎片"""
        fragments = []
        
        # 自动识别类型
        if source_type == "auto":
            if len(text) <= 10:
                source_type = "tag"
            elif len(text) <= 20:
                source_type = "term"
            elif len(text) <= 50:
                source_type = "phrase"
            else:
                source_type = "sentence"
        
        # 根据类型处理
        if source_type == "tag":
            # 清理并作为标签
            cleaned = re.sub(r'[^\w\u4e00-\u9fff]', '', text)
            if cleaned:
                fragments.append({"type": "tag", "content": cleaned})
        
        elif source_type == "sentence":
            # 分句
            sentences = re.split(r'[。！？\.\n]', text)
            for sent in sentences:
                sent = sent.strip()
                if len(sent) >= 5:
                    fragments.append({"type": "sentence", "content": sent})
                    # 再从句子中提取术语
                    terms = self._extract_terms(sent)
                    fragments.extend(terms)
        
        else:
            fragments.append({"type": source_type, "content": text.strip()})
        
        return fragments
    
    def _extract_terms(self, text: str) -> List[Dict[str, str]]:
        """从文本提取术语"""
        terms = []
        # 简单规则：2-4字的专业词汇
        # 实际应用可用更复杂的NLP
        common_term_patterns = [
            r'量子[\w\u4e00-\u9fff]{1,3}',
            r'[\w\u4e00-\u9fff]{2,4}技术',
            r'[\w\u4e00-\u9fff]{2,4}算法',
            r'[\w\u4e00-\u9fff]{2,4}系统',
        ]
        for pattern in common_term_patterns:
            matches = re.findall(pattern, text)
            for match in set(matches):
                terms.append({"type": "term", "content": match})
        return terms
    
    def ingest(self, content: str, source_id: str, source_url: str, 
               source_title: str, category: str, palace: int) -> List[KnowledgeFragment]:
        """
        摄入知识内容，拆解为碎片
        
        Args:
            content: 原始内容
            source_id: 来源ID
            source_url: 来源URL
            source_title: 来源标题
            category: 知识类别
            palace: 洛书宫位
            
        Returns:
            处理后的知识碎片列表
        """
        fragments = []
        raw_fragments = self._extract_fragments(content)
        
        crawl_time = datetime.now().isoformat()
        
        for raw in raw_fragments:
            # DNA兼容度检测
            dna_result = self.dna_checker.check(raw["content"], category)
            
            # 创建碎片
            fragment = KnowledgeFragment(
                id=str(uuid.uuid4())[:8],
                type=raw["type"],
                content=raw["content"],
                content_hash=self._hash_content(raw["content"]),
                source_id=source_id,
                source_url=source_url,
                source_title=source_title,
                crawl_time=crawl_time,
                category=category,
                palace=palace,
                tags=[],
                language="zh",
                compatibility_score=dna_result["compatibility_score"],
                keywords_matched=dna_result["keywords_matched"],
                persona_fit=dna_result["persona_fit"]
            )
            
            # 状态判定
            if dna_result["compatibility_score"] >= 0.6:
                fragment.status = "indexed"
                fragment.status_reason = "DNA兼容度达标"
            else:
                fragment.status = "quarantined"
                fragment.status_reason = "DNA兼容度不足，待审核"
            
            fragments.append(fragment)
        
        return fragments
    
    def save_fragments(self, fragments: List[KnowledgeFragment]):
        """保存碎片到相应目录"""
        for frag in fragments:
            data = frag.to_dict()
            
            if frag.status == "quarantined":
                # 入隔离区
                filepath = self.quarantine_dir / f"{frag.id}.json"
            else:
                # 入索引库
                filepath = self.indexed_dir / f"{frag.id}.json"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 保存 {len(fragments)} 个碎片")
        print(f"   - 已索引: {sum(1 for f in fragments if f.status == 'indexed')}")
        print(f"   - 隔离区: {sum(1 for f in fragments if f.status == 'quarantined')}")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计"""
        indexed_count = len(list(self.indexed_dir.glob("*.json")))
        quarantine_count = len(list(self.quarantine_dir.glob("*.json")))
        
        return {
            "indexed": indexed_count,
            "quarantined": quarantine_count,
            "total": indexed_count + quarantine_count
        }
    
    def search_fragments(self, keyword: str, min_compatibility: float = 0.6) -> List[Dict]:
        """搜索碎片"""
        results = []
        keyword_lower = keyword.lower()
        
        for filepath in self.indexed_dir.glob("*.json"):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                if data.get("compatibility_score", 0) < min_compatibility:
                    continue
                
                content = data.get("content", "").lower()
                if keyword_lower in content:
                    results.append(data)
        
        return sorted(results, key=lambda x: x.get("compatibility_score", 0), reverse=True)


def main():
    """测试"""
    print("🧪 三色知识库采集引擎测试\n")
    
    collector = KnowledgeCollector()
    
    # 模拟摄入一段量子科技内容
    test_content = """
    量子计算利用量子叠加态进行并行计算，实现量子优越性。
    量子比特是量子计算的基本单元，通过量子纠缠实现多比特协同。
    当前的NISQ时代，量子纠错是主要挑战。
    """
    
    fragments = collector.ingest(
        content=test_content,
        source_id="qtc_com_cn",
        source_url="http://www.qtc.com.cn",
        source_title="量子科技中心",
        category="quantum_tech",
        palace=1
    )
    
    print(f"📝 提取到 {len(fragments)} 个碎片:\n")
    for i, frag in enumerate(fragments[:5], 1):
        print(f"{i}. [{frag.type}] {frag.content[:30]}...")
        print(f"   DNA兼容度: {frag.compatibility_score}")
        print(f"   匹配关键词: {frag.keywords_matched[:3]}")
        print(f"   状态: {frag.status}")
        print()
    
    # 保存
    collector.save_fragments(fragments)
    
    # 统计
    stats = collector.get_stats()
    print(f"📊 当前统计: {stats}")
    
    # 搜索测试
    print("\n🔍 搜索'量子':")
    results = collector.search_fragments("量子")
    for r in results[:3]:
        print(f"   - {r['content'][:25]}... (兼容度:{r['compatibility_score']})")
    
    print("\n🎯 测试完成")


if __name__ == "__main__":
    main()
