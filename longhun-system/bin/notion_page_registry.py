#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Notion页面注册表模块
封装notion_pages.json为Python API
DNA: #龍芯⚡️2026-04-08-NOTION-REGISTRY-v1.0
"""

import json
import os
from typing import Optional, Dict, List, Any
from pathlib import Path

# 默认索引文件路径
DEFAULT_INDEX_PATH = Path(__file__).parent.parent / "notion-index" / "notion_pages.json"
FULL_INDEX_PATH = Path(__file__).parent.parent / "notion-index" / "out" / "index.jsonl"


class NotionPageRegistry:
    """Notion页面注册表 - 快速查找Notion页面"""
    
    def __init__(self, index_path: Optional[Path] = None):
        self.index_path = index_path or DEFAULT_INDEX_PATH
        self._pages: List[Dict[str, Any]] = []
        self._by_id: Dict[str, Dict[str, Any]] = {}
        self._by_title: Dict[str, Dict[str, Any]] = {}
        self._keywords_map: Dict[str, List[Dict[str, Any]]] = {}
        self._loaded = False
        self._load()
    
    def _load(self):
        """加载索引文件"""
        if not self.index_path.exists():
            print(f"⚠️ 索引文件不存在: {self.index_path}")
            return
        
        try:
            with open(self.index_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._pages = data.get('pages', [])
            
            # 构建索引
            for page in self._pages:
                page_id = page.get('id', '')
                title = page.get('title', '')
                keywords = page.get('keywords', [])
                
                if page_id:
                    self._by_id[page_id] = page
                
                if title:
                    self._by_title[title] = page
                
                # 关键词索引
                for kw in keywords:
                    if kw not in self._keywords_map:
                        self._keywords_map[kw] = []
                    self._keywords_map[kw].append(page)
            
            self._loaded = True
            print(f"✅ Notion注册表加载完成: {len(self._pages)} 页")
            
        except Exception as e:
            print(f"❌ 加载失败: {e}")
    
    def find_page(self, keyword: str) -> Optional[Dict[str, Any]]:
        """
        按关键词查找页面
        
        Args:
            keyword: 搜索关键词（标题/ID/关键词匹配）
            
        Returns:
            匹配的第一条页面记录，或None
        """
        keyword = keyword.lower()
        
        # 1. 精确ID匹配
        for pid, page in self._by_id.items():
            if keyword in pid.lower():
                return page
        
        # 2. 标题包含匹配
        for title, page in self._by_title.items():
            if keyword in title.lower():
                return page
        
        # 3. 关键词匹配
        for kw, pages in self._keywords_map.items():
            if keyword in kw.lower() and pages:
                return pages[0]
        
        # 4. 模糊搜索tags和purpose
        for page in self._pages:
            tags = ' '.join(page.get('tags', [])).lower()
            purpose = page.get('purpose', '').lower()
            if keyword in tags or keyword in purpose:
                return page
        
        return None
    
    def find_pages(self, keyword: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        按关键词查找多个页面
        
        Args:
            keyword: 搜索关键词
            limit: 最大返回数量
            
        Returns:
            匹配的页面列表
        """
        keyword = keyword.lower()
        results = []
        seen_ids = set()
        
        for page in self._pages:
            page_id = page.get('id', '')
            title = page.get('title', '').lower()
            keywords = [k.lower() for k in page.get('keywords', [])]
            tags = ' '.join(page.get('tags', [])).lower()
            purpose = page.get('purpose', '').lower()
            
            if (keyword in page_id.lower() or 
                keyword in title or 
                any(keyword in k for k in keywords) or
                keyword in tags or
                keyword in purpose):
                
                if page_id not in seen_ids:
                    results.append(page)
                    seen_ids.add(page_id)
                    
                if len(results) >= limit:
                    break
        
        return results
    
    def get_page_id(self, title_or_id: str) -> Optional[str]:
        """
        获取页面ID
        
        Args:
            title_or_id: 页面标题或部分ID
            
        Returns:
            完整页面ID
        """
        page = self.find_page(title_or_id)
        return page.get('id') if page else None
    
    def get_page_url(self, title_or_id: str, public: bool = False) -> Optional[str]:
        """
        获取页面URL
        
        Args:
            title_or_id: 页面标题或ID
            public: 是否返回公开分享链接（需要先设置）
            
        Returns:
            Notion页面URL
        """
        page = self.find_page(title_or_id)
        if not page:
            return None
        
        page_id = page.get('id', '')
        
        # 公开链接格式（需要先在Notion里开启Share → Publish to web）
        if public:
            # 公开链接格式: https://username.notion.site/xxxx
            return f"https://zuimeidedeyihan.notion.site/{page_id}"
        
        return page.get('url')
    
    def get_by_palace(self, palace_num: int) -> List[Dict[str, Any]]:
        """按洛书宫位查找页面"""
        return [p for p in self._pages if p.get('palace') == palace_num]
    
    def get_all_pages(self) -> List[Dict[str, Any]]:
        """获取所有页面"""
        return self._pages.copy()
    
    def stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "total_pages": len(self._pages),
            "indexed_by_id": len(self._by_id),
            "indexed_by_title": len(self._by_title),
            "keyword_mappings": len(self._keywords_map),
            "loaded": self._loaded
        }


# 全局单例实例
_registry: Optional[NotionPageRegistry] = None


def get_registry() -> NotionPageRegistry:
    """获取全局注册表实例"""
    global _registry
    if _registry is None:
        _registry = NotionPageRegistry()
    return _registry


# 便捷函数
def find_page(keyword: str) -> Optional[Dict[str, Any]]:
    """查找页面"""
    return get_registry().find_page(keyword)


def find_pages(keyword: str, limit: int = 5) -> List[Dict[str, Any]]:
    """查找多个页面"""
    return get_registry().find_pages(keyword, limit)


def get_page_id(title_or_id: str) -> Optional[str]:
    """获取页面ID"""
    return get_registry().get_page_id(title_or_id)


def get_page_url(title_or_id: str, public: bool = False) -> Optional[str]:
    """获取页面URL"""
    return get_registry().get_page_url(title_or_id, public)


if __name__ == "__main__":
    # 测试
    print("🧪 Notion页面注册表测试\n")
    
    reg = NotionPageRegistry()
    print(f"统计: {reg.stats()}\n")
    
    # 测试查找
    test_keywords = ["三才流场", "全局入口", "天道系统", "宝宝"]
    for kw in test_keywords:
        result = reg.find_page(kw)
        if result:
            print(f"✅ '{kw}' → {result.get('title', 'N/A')[:40]}... ({result.get('id', 'N/A')})")
        else:
            print(f"❌ '{kw}' → 未找到")
    
    print("\n🎯 测试完成")
