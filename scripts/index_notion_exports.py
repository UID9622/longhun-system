#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️2026-06-23-LONGHUN-NOTION-INDEXER-v1.0
"""
Notion 导出目录索引器

扫描 CNSH-整理版等 Notion 导出目录中的 `_INDEX.json` 元数据文件，
把页面标题、标签、分类、原始 Notion URL 汇总成一个统一索引，
供 longhun-notion-legacy 技能快速检索。
"""

import json
import re
from pathlib import Path

DNA = "#龍芯⚡️2026-06-23-LONGHUN-NOTION-INDEXER-v1.0"

NOTION_EXPORT_DIRS = [
    Path.home() / "longhun-system" / "_archive" / "cnsh-history" / "CNSH-整理版",
]

OUTPUT_INDEX = Path.home() / ".longhun" / "index" / "notion_exports.json"


def parse_index_file(path: Path) -> dict[str, Any]:
    """解析带 YAML/comment 前缀的 _INDEX.json 文件。"""
    text = path.read_text(encoding="utf-8")
    # 去掉开头的注释行
    lines = []
    in_json = False
    for line in text.splitlines():
        if not in_json and line.strip().startswith("{"):
            in_json = True
        if in_json:
            lines.append(line)
    try:
        return json.loads("\n".join(lines))
    except json.JSONDecodeError as e:
        print(f"⚠️ 解析失败 {path}: {e}")
        return {}


def build_index():
    entries = []
    for root in NOTION_EXPORT_DIRS:
        if not root.exists():
            continue
        for idx_path in sorted(root.rglob("_INDEX.json")):
            data = parse_index_file(idx_path)
            category = data.get("category", idx_path.parent.name)
            for page in data.get("pages", []):
                entries.append({
                    "id": page.get("id"),
                    "title": page.get("title", ""),
                    "icon": page.get("icon", ""),
                    "tags": page.get("tags", []),
                    "category": category,
                    "subcategory": idx_path.parent.name,
                    "notion_url": page.get("url", ""),
                    "created": page.get("created", ""),
                    "modified": page.get("modified", ""),
                    "category_reason": page.get("category_reason", ""),
                })

    index = {
        "dna": DNA,
        "total": len(entries),
        "sources": [str(d) for d in NOTION_EXPORT_DIRS],
        "entries": entries,
    }

    OUTPUT_INDEX.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ 已索引 {len(entries)} 个 Notion 页面")
    print(f"   文件: {OUTPUT_INDEX}")
    print(f"   DNA: {DNA}")


def search_index(keywords: list[Any], limit: int = 20):
    """简单关键词搜索。"""
    if not OUTPUT_INDEX.exists():
        build_index()
    data = json.loads(OUTPUT_INDEX.read_text(encoding="utf-8"))
    keywords = [k.lower() for k in keywords]
    results = []
    for entry in data["entries"]:
        text = f"{entry['title']} {' '.join(entry['tags'])} {entry['category']} {entry['category_reason']}".lower()
        score = sum(1 for k in keywords if k in text)
        if score:
            results.append((score, entry))
    results.sort(key=lambda x: x[0], reverse=True)
    return [r[1] for r in results[:limit]]


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "search":
        kw = sys.argv[2:]
        for r in search_index(kw):
            print(f"[{r['category']}] {r['icon']} {r['title']} | tags={r['tags']} | {r['notion_url']}")
    else:
        build_index()
