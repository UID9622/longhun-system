#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · Notion DB3367 批量种子模块生成器 v1.0

把分类为「有代码」的条目批量生成为 CNSH 种子模块，
每个模块包含：定义占位、CNSH 语义映射、龍魂对齐、待回填事项。

用法：
  python3 batch_seed_modules.py

DNA: #龍芯⚡️2026-07-05-LONGHUN-NOTION-DB3367-BATCH-SEED-v1.0
"""
from __future__ import annotations

import json
import os
import re
import datetime
from pathlib import Path
from typing import Dict, List

HOME = Path.home()
LONGHUN_ROOT = Path(os.environ.get("LONGHUN_ROOT", HOME / "longhun-system"))
INDEX_PATH = LONGHUN_ROOT / "docs" / "notion_mirror" / "db_3367_knowledge_index.json"
OUT_DIR = LONGHUN_ROOT / "cnsh" / "notion" / "modules" / "db3367" / "seed"
MANIFEST_PATH = LONGHUN_ROOT / "outputs" / "manifest.json"

DNA = "#龍芯⚡️2026-07-05-LONGHUN-NOTION-DB3367-BATCH-SEED-v1.0"


def now_iso() -> str:
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()


def safe_filename(title: str, page_id: str) -> str:
    """生成安全的文件名"""
    if not title:
        title = "untitled"
    # 移除 emoji、特殊符号
    clean = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9\s_-]", "", title)
    clean = re.sub(r"\s+", "_", clean).strip("_-")[:40]
    short_id = page_id.replace("-", "")[:8]
    return f"M_{clean}_{short_id}.md"


def generate_module(entry: dict) -> str:
    title = entry.get("title") or "未命名条目"
    page_id = entry.get("page_id", "")
    url = entry.get("url", "")
    tags = entry.get("tags") or []
    status = entry.get("status") or ""
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    dna = f"#龍芯⚡️{ts}-NOTION-DB3367-SEED-{page_id[:8].upper()}-v1.0"

    tag_str = "、".join(tags) if tags else "未分类"

    lines = []
    lines.append(f"# {title}｜龍魂 CNSH 种子模块")
    lines.append("")
    lines.append(f"- **Notion 来源**：`{page_id}`")
    lines.append(f"- **Notion URL**：{url}")
    lines.append(f"- **Notion 状态**：{status or '未设置'}")
    lines.append(f"- **本地状态**：🔧 接入中（种子模块）")
    lines.append(f"- **DNA**：`{dna}`")
    lines.append(f"- **标签**：{tag_str}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 一句话")
    lines.append("")
    lines.append(f"{title} 是龍魂知识库中标记为「有代码」的条目，待进一步填充理论、实现与 CNSH 语义映射。")
    lines.append("")
    lines.append("## 核心概念")
    lines.append("")
    lines.append("> 【待回填：是什么 · 从哪来 · 解决什么问题 · 类比是什么】")
    lines.append("")
    lines.append("## 核心公式 / 关键语法")
    lines.append("")
    lines.append("```python")
    lines.append("# 【待回填：把核心代码/伪代码/公式写在这里】")
    lines.append("pass")
    lines.append("```")
    lines.append("")
    lines.append("## 龍魂对齐")
    lines.append("")
    lines.append("- **应用场景**：【待填】")
    lines.append("- **对接模块**：【待填】")
    lines.append("- **CNSH 变量命名**：")
    lines.append("  - `xxx` → `【待填】`")
    lines.append("")
    lines.append("## Python 可运行片段（待实现）")
    lines.append("")
    lines.append("```python")
    lines.append("def 待实现():")
    lines.append("    pass")
    lines.append("")
    lines.append("if __name__ == '__main__':")
    lines.append("    待实现()")
    lines.append("```")
    lines.append("")
    lines.append("## 待回填事项")
    lines.append("")
    lines.append(f"- [ ] 拉取 Notion 原页 [{title}]({url}) 的完整内容")
    lines.append("- [ ] 补充核心定义与公式")
    lines.append("- [ ] 补充 CNSH 语义映射")
    lines.append("- [ ] 实现可运行 Python 片段")
    lines.append("- [ ] 与 `longhun-math-formula-core` 注册函数")
    lines.append("")
    lines.append("---")
    lines.append(f"**签章**：`{dna}` · UID9622")
    return "\n".join(lines)


def main():
    data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    entries = data["entries"]
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    generated = []
    skipped = 0
    for e in entries:
        cat = e.get("lh_category")
        if cat != "有代码":
            continue
        # 跳过已有模块的条目
        if e.get("lh_module_path"):
            skipped += 1
            continue
        title = e.get("title") or "untitled"
        page_id = e.get("page_id", "")
        filename = safe_filename(title, page_id)
        path = OUT_DIR / filename
        # 如果文件已存在也跳过
        if path.exists():
            e["lh_module_path"] = str(path)
            skipped += 1
            continue
        content = generate_module(e)
        path.write_text(content, encoding="utf-8")
        e["lh_module_path"] = str(path)
        e["status"] = "🔧 接入中"
        generated.append({
            "title": title,
            "page_id": page_id,
            "path": str(path),
        })

    # 写回索引
    INDEX_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    # 更新 manifest
    if MANIFEST_PATH.exists():
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        manifest.append({
            "dna": DNA,
            "content_type": "batch_seed_modules",
            "topic": f"Notion DB3367 批量种子模块（{len(generated)} 个）",
            "file_path": str(OUT_DIR),
            "created_at": now_iso(),
        })
        MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"manifest updated, total entries: {len(manifest)}")

    print(f"generated: {len(generated)}, skipped (already have module): {skipped}")
    print(f"output dir: {OUT_DIR}")


if __name__ == "__main__":
    main()
