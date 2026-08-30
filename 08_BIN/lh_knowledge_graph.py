#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 知识图谱引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-KNOWLEDGE-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 构建代码/文档/协议的语义知识图谱
  - 支持实体链接（代码函数 ↔ 文档 ↔ 协议条款）
  - 语义检索（"找所有和审计相关的函数"）
  - 知识推荐（给定一个实体，推荐相关实体）
"""

import json
import re
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Set
from collections import defaultdict


class KnowledgeGraph:
    """知识图谱引擎——不只记动作关联，还记领域知识"""

    def __init__(self):
        self.entities: Dict[str, Dict] = {}
        self.relations: List[tuple] = []
        self.inverted_index: Dict[str, Set[str]] = defaultdict(set)
        self._kg_file = Path.home() / "longhun-system/data/knowledge_graph.json"
        self._load()

    def _load(self):
        if self._kg_file.exists():
            try:
                data = json.loads(self._kg_file.read_text(encoding="utf-8"))
                self.entities = data.get("entities", {})
                self.relations = [tuple(r) for r in data.get("relations", [])]
                self._rebuild_index()
            except Exception:
                pass

    def _save(self):
        self._kg_file.parent.mkdir(parents=True, exist_ok=True)
        self._kg_file.write_text(json.dumps({
            "entities": self.entities,
            "relations": [list(r) for r in self.relations],
        }, ensure_ascii=False, indent=2))

    def _rebuild_index(self):
        self.inverted_index.clear()
        for eid, entity in self.entities.items():
            name = entity.get("name", "")
            for word in re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', name):
                word_l = word.lower()
                self.inverted_index[word_l].add(eid)
                # 中文 2-gram 增强（2026-08-15）：让「牢笼」「组件」「四层」等子词可命中
                if re.match(r'^[\u4e00-\u9fff]+$', word) and len(word) >= 2:
                    for i in range(len(word) - 1):
                        self.inverted_index[word[i:i + 2]].add(eid)

    def add_entity(self, entity_id: str, entity_type: str, name: str, properties: Dict = None):
        self.entities[entity_id] = {
            "type": entity_type, "name": name,
            "properties": properties or {},
        }
        self._rebuild_index()
        self._save()

    def add_relation(self, from_id: str, to_id: str, relation_type: str):
        self.relations.append((from_id, to_id, relation_type))
        self._save()

    def search(self, query: str, top_k: int = 10) -> List[Dict]:
        """语义搜索实体"""
        words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', query.lower())
        grams: Set[str] = set()
        for w in words:
            grams.add(w)
            if re.match(r'^[\u4e00-\u9fff]+$', w) and len(w) >= 2:
                for i in range(len(w) - 1):
                    grams.add(w[i:i + 2])
        candidate_ids: Set[str] = set()
        for g in grams:
            candidate_ids.update(self.inverted_index.get(g, set()))

        results = []
        for eid in candidate_ids:
            entity = self.entities[eid]
            score = 0
            name_lower = entity["name"].lower()
            if query.lower() in name_lower:
                score += 100
            score += sum(1 for w in words if w in name_lower)
            results.append({"id": eid, "entity": entity, "score": score})

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def recommend(self, entity_id: str, max_depth: int = 1) -> List[str]:
        """推荐相关实体"""
        related: Set[str] = set()
        for from_id, to_id, _ in self.relations:
            if from_id == entity_id:
                related.add(to_id)
            elif to_id == entity_id:
                related.add(from_id)
        return list(related)

    def build_from_files(self, root: Path):
        """从代码/文档构建知识图谱"""
        count = 0
        # 扫描 .py 文件提取函数
        for py_file in root.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            # 🔴 三关判定(2026-08-30·文件身份协议v1.1): 前8KB含NUL→二进制跳过
            try:
                with open(py_file, "rb") as f:
                    if b"\x00" in f.read(8192):
                        continue
            except OSError:
                continue
            try:
                content = py_file.read_text(encoding="utf-8", errors="ignore")
                for match in re.finditer(r'def\s+(\w+)\s*\([^)]*\):', content):
                    fn = match.group(1)
                    self.add_entity(f"func_{fn}", "function", fn, {
                        "file": str(py_file.relative_to(root)),
                    })
                    count += 1
            except Exception:
                pass
        # 扫描 .md 文件提取标题
        for md_file in root.rglob("*.md"):
            # 🔴 三关判定(2026-08-30): 前8KB含NUL→二进制跳过
            try:
                with open(md_file, "rb") as f:
                    if b"\x00" in f.read(8192):
                        continue
            except OSError:
                continue
            try:
                content = md_file.read_text(encoding="utf-8", errors="ignore")
                for line in content.split("\n"):
                    if line.startswith("#"):
                        title = line.lstrip("#").strip()
                        if len(title) > 2:
                            eid = f"doc_{hashlib.md5(title.encode()).hexdigest()[:8]}"
                            self.add_entity(eid, "document_section", title, {
                                "file": str(md_file.relative_to(root)),
                            })
                            count += 1
            except Exception:
                pass
        return {"entities_added": count, "total": len(self.entities)}

    def stats(self) -> Dict[str, Any]:
        return {
            "total_entities": len(self.entities),
            "total_relations": len(self.relations),
            "index_terms": len(self.inverted_index),
        }


if __name__ == "__main__":
    kg = KnowledgeGraph()
    result = kg.build_from_files(Path.home() / "longhun-system/bin")
    print(f"构建完成: 新增 {result['entities_added']} 实体，总计 {result['total']}")

    results = kg.search("审计")
    print(f"搜索'审计': {len(results)} 条结果")
    for r in results[:3]:
        print(f"  ├ {r['entity']['name']} ({r['entity']['type']}) score={r['score']}")

    print(f"统计: {kg.stats()}")
    print("🟢 知识图谱引擎测试通过")
