#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂DNA记忆库 · 语义匹配引擎（engines）

职责：
  - 接入龍魂语义统一注册表（bin/lh_semantic_unified_registry.py）做专业术语对齐
  - 本地语义生长网络（SemanticWeb）做用户标签自生长
  - 余弦相似度占位（无向量库时诚实降级为共现评分）

反黑箱：所有匹配须可解释（命中了哪个词/哪个标签）。
DNA: #龍魂⚡️2026-0716-引擎-语义
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

ROOT = Path(__file__).resolve().parent.parent.parent

# 尝试接入语义统一注册表（优雅降级）
try:
    sys.path.insert(0, str(ROOT / "bin"))
    from lh_semantic_unified_registry import load_registry
    _HAVE_REGISTRY = True
except Exception:
    _HAVE_REGISTRY = False


class SemanticEngine:
    """语义匹配引擎 — 本地生长 + 全局注册表对齐。"""

    def __init__(self):
        self.registry = load_registry() if _HAVE_REGISTRY else None

    def align_term(self, word: str) -> Optional[str]:
        """用全局注册表对齐专业术语（如：电子签→数字签名）。"""
        if not self.registry:
            return None
        try:
            cats = self.registry.get("categories", {})
            for cat_key, cat_data in cats.items():
                blob = str(cat_data).lower()
                if word.lower() in blob:
                    return f"[{cat_key}] {word}"
        except Exception:
            return None
        return None

    def explain(self, query: str, matched_tags: List[str]) -> Dict[str, Any]:
        """生成可解释匹配说明（杜绝黑箱）。"""
        return {
            "query": query,
            "matched_tags": matched_tags,
            "registry_aligned": [self.align_term(t) for t in matched_tags if self.align_term(t)],
            "method": "共现评分 + 信息素加权（无向量库时诚实降级）",
        }

    def stats(self) -> Dict[str, Any]:
        return {
            "registry_loaded": self.registry is not None,
            "registry_categories": len(self.registry.get("categories", {})) if self.registry else 0,
        }


if __name__ == "__main__":
    e = SemanticEngine()
    print("注册表接入:", e.stats())
    print(e.explain("押金不退合同", ["押金", "合同"]))
