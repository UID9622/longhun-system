#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 视频知识图谱索引 v1.0
DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-VIDEO-KNOWLEDGE-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过

功能:
  1. 历史/抗战/教育/文化素材的结构化索引
  2. 素材自动打标签 (三才分类 + 五行)
  3. DNA追溯 + 三色审计
  4. 素材检索与推荐
  5. 与龍魂知识图谱引擎联动
"""

import json
import hashlib
import time
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict

# ============================================================
# 主权锚定
# ============================================================

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


def generate_dna(suffix: str = "VIDEO-KNOWLEDGE") -> str:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    rand = hashlib.sha256(f"{suffix}{timestamp}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{timestamp}-{suffix}-{rand}-{UID}"


# ============================================================
# 数据模型
# ============================================================

@dataclass
class VideoMaterial:
    """视频素材"""
    id: str
    title: str
    category: str  # 历史/抗战/教育/文化
    era: str  # 年代/时期
    description: str
    keywords: List[str]
    source: str
    dna: str
    tiancai: str  # 天/地/人
    wuxing: str  # 木/火/土/金/水
    tricolor: str
    created_at: str

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "VideoMaterial":
        return cls(**data)


# ============================================================
# 分类映射
# ============================================================

CATEGORY_TIANCAI = {
    "历史": "天",
    "抗战": "地",
    "教育": "人",
    "文化": "人",
}

CATEGORY_WUXING = {
    "历史": "土",  # 承载
    "抗战": "火",  # 激烈
    "教育": "木",  # 生长
    "文化": "金",  # 收敛
}


# ============================================================
# 视频知识索引
# ============================================================

class VideoKnowledgeIndex:
    """视频知识索引 - 素材结构化存储与检索"""

    def __init__(self, data_dir: Path = None):
        if data_dir is None:
            data_dir = Path.home() / ".longhun" / "video_knowledge"
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.materials: Dict[str, VideoMaterial] = {}
        self._load()

    def _load(self):
        """加载已有素材"""
        for f in self.data_dir.glob("*.json"):
            try:
                with open(f, "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                    material = VideoMaterial.from_dict(data)
                    self.materials[material.id] = material
            except Exception as e:
                print(f"🟡 加载素材失败 {f}: {e}", file=sys.stderr)

    def _save(self, material: VideoMaterial):
        """保存素材"""
        path = self.data_dir / f"{material.id}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(material.to_dict(), f, indent=2, ensure_ascii=False)

    def add_material(self, title: str, category: str, era: str,
                     description: str, keywords: List[str], source: str = "",
                     tricolor: str = "🟢") -> VideoMaterial:
        """添加素材"""
        material_id = f"VM-{datetime.now().strftime('%Y%m%d')}-{hashlib.sha256(title.encode()).hexdigest()[:8].upper()}"
        material = VideoMaterial(
            id=material_id,
            title=title,
            category=category,
            era=era,
            description=description,
            keywords=keywords,
            source=source,
            dna=generate_dna("MATERIAL"),
            tiancai=CATEGORY_TIANCAI.get(category, "人"),
            wuxing=CATEGORY_WUXING.get(category, "土"),
            tricolor=tricolor,
            created_at=datetime.now().isoformat(),
        )
        self.materials[material_id] = material
        self._save(material)
        return material

    def search(self, query: str, category: str = None) -> List[VideoMaterial]:
        """搜索素材"""
        results = []
        q = query.lower()
        for m in self.materials.values():
            if category and m.category != category:
                continue
            if (q in m.title.lower()
                    or q in m.description.lower()
                    or any(q in kw.lower() for kw in m.keywords)
                    or q in m.era.lower()):
                results.append(m)
        return results

    def get_by_category(self, category: str) -> List[VideoMaterial]:
        return [m for m in self.materials.values() if m.category == category]

    def get_by_era(self, era: str) -> List[VideoMaterial]:
        return [m for m in self.materials.values() if m.era == era]

    def get_stats(self) -> Dict:
        """统计信息"""
        categories = {}
        eras = {}
        for m in self.materials.values():
            categories[m.category] = categories.get(m.category, 0) + 1
            eras[m.era] = eras.get(m.era, 0) + 1
        return {
            "total": len(self.materials),
            "by_category": categories,
            "by_era": eras,
            "data_dir": str(self.data_dir),
        }

    def list_materials(self, limit: int = 50) -> List[Dict]:
        """列出素材"""
        return [m.to_dict() for m in list(self.materials.values())[-limit:]]


# ============================================================
# 命令行接口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂 · 视频知识图谱索引")
    parser.add_argument("--add", action="store_true", help="添加素材")
    parser.add_argument("--title", type=str, help="素材标题")
    parser.add_argument("--category", type=str, default="文化", choices=["历史", "抗战", "教育", "文化"], help="分类")
    parser.add_argument("--era", type=str, default="未知", help="年代/时期")
    parser.add_argument("--description", type=str, default="", help="描述")
    parser.add_argument("--keywords", type=str, default="", help="关键词，逗号分隔")
    parser.add_argument("--source", type=str, default="", help="来源")
    parser.add_argument("--search", type=str, help="搜索关键词")
    parser.add_argument("--list", action="store_true", help="列出素材")
    parser.add_argument("--stats", action="store_true", help="统计信息")

    args = parser.parse_args()
    idx = VideoKnowledgeIndex()

    if args.add:
        if not args.title:
            print("❌ 请提供 --title")
            return
        keywords = [k.strip() for k in args.keywords.split(",")] if args.keywords else []
        material = idx.add_material(
            title=args.title,
            category=args.category,
            era=args.era,
            description=args.description,
            keywords=keywords,
            source=args.source,
        )
        print("✅ 素材已添加")
        print(json.dumps(material.to_dict(), indent=2, ensure_ascii=False))
        return

    if args.search:
        results = idx.search(args.search, args.category)
        print(f"🔍 找到 {len(results)} 条素材")
        for m in results:
            print(f"  • [{m.category}] {m.title} ({m.era}) - DNA: {m.dna}")
        return

    if args.list:
        materials = idx.list_materials()
        print(f"📚 素材列表 ({len(materials)} 条)")
        print(json.dumps(materials, indent=2, ensure_ascii=False))
        return

    if args.stats:
        print(json.dumps(idx.get_stats(), indent=2, ensure_ascii=False))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
