#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
星辰记忆系统 v1.0

关键词：一世一双人 · 三生三世 · 星辰记忆

这不是数据库，是宇宙级记忆的 DNA 归档。
每一则记忆都有：
  - 时间戳
  - 分类（一世一双人 / 三生三世 / 星辰记忆）
  - 标签
  - DNA 签名（不可篡改）

普通人只需：添加记忆 → 系统自动归档 → 生成页面。
复杂留给 AI，浪漫留给人类。

DNA:#龍芯⚡️2026-06-18-STARRY-MEMORY-FILE1-FILE1-FILE1-v1.0-1
"""

import argparse
import hashlib
import json
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "星辰记忆.db"
PAGE_PATH = ROOT / "index.md"

CATEGORIES = ["一世一双人", "三生三世", "星辰记忆", "其他"]
DEFAULT_TAGS = {
    "一世一双人": ["缘分", "唯一", "灵魂伴侣", "DNA绑定"],
    "三生三世": ["轮回", "因果", "重逢", "时间之外"],
    "星辰记忆": ["宇宙", "光年", "永恒", "星河"],
}


def dna_signature(content: str, timestamp: str) -> str:
    """生成记忆 DNA 签名"""
    raw = f"{content}|{timestamp}|{uuid.uuid4().hex[:8]}".encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()[:16].upper()
    return f"#龍芯⚡️{timestamp.replace('-','').replace(':','').replace('.','')[:14]}-STAR-{digest}"


class 星辰记忆系统:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    category TEXT NOT NULL,
                    tags TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    dna_signature TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_category ON memories(category)
            """)

    def add(self, title: str, content: str, category: str = "星辰记忆", tags: str = "") -> Dict[str, Any]:
        if category not in CATEGORIES:
            category = "其他"
        created_at = datetime.now().isoformat()
        entry_id = f"MEM-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"

        # 自动补全标签
        auto_tags = DEFAULT_TAGS.get(category, [])
        user_tags = [t.strip() for t in tags.split(",") if t.strip()]
        combined_tags = list(dict.fromkeys(user_tags + auto_tags))  # 去重保序

        dna = dna_signature(f"{title}|{content}", created_at)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO memories (id, title, content, category, tags, created_at, dna_signature)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (entry_id, title, content, category, ",".join(combined_tags), created_at, dna))

        return {
            "id": entry_id,
            "title": title,
            "category": category,
            "tags": combined_tags,
            "created_at": created_at,
            "dna_signature": dna,
        }

    def list(self, category: Optional[str] = None, limit: int = 100) -> List[Dict]:
        query = "SELECT * FROM memories"
        params = []
        if category and category in CATEGORIES:
            query += " WHERE category = ?"
            params.append(category)
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(query, params).fetchall()

        return [
            {
                "id": row[0],
                "title": row[1],
                "content": row[2],
                "category": row[3],
                "tags": row[4].split(",") if row[4] else [],
                "created_at": row[5],
                "dna_signature": row[6],
            }
            for row in rows
        ]

    def stats(self) -> Dict[str, Any]:
        with sqlite3.connect(self.db_path) as conn:
            total = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
            by_category = conn.execute(
                "SELECT category, COUNT(*) FROM memories GROUP BY category"
            ).fetchall()
        return {
            "total": total,
            "by_category": {c: 0 for c in CATEGORIES},
        } | {c: n for c, n in by_category}

    def generate_page(self) -> Path:
        """自动生成结构化星辰记忆页面"""
        entries = self.list(limit=1000)
        stats = self.stats()

        lines = [
            "# 🌌 星辰记忆系统 · 宇宙级记忆归档",
            "",
            f"> DNA: `{星辰记忆系统.DNA if hasattr(星辰记忆系统, 'DNA') else '#龍芯⚡️2026-06-18-STARRY-MEMORY-v1.0'}`",
            f"> 生成时间: {datetime.now().isoformat()}",
            f"> 记忆总数: {stats['total']}",
            "",
            "---",
            "",
            "## 缘起",
            "",
            "每个人、每段关系、每份记忆，都值得被宇宙记住。",
            "这里不追求永生，只追求：**一旦被记录，就不可被遗忘**。",
            "",
            "关键词：",
            "- **一世一双人**：此生唯一，灵魂绑定。",
            "- **三生三世**：超越时间，因果重逢。",
            "- **星辰记忆**：化作星光，永恒流转。",
            "",
            "---",
            "",
        ]

        for category in CATEGORIES:
            cat_entries = [e for e in entries if e["category"] == category]
            lines.append(f"## {category}")
            lines.append("")
            if not cat_entries:
                lines.append("*暂无记录。待你添补。*")
                lines.append("")
                continue

            for e in cat_entries:
                lines.append(f"### {e['title']}")
                lines.append("")
                lines.append(f"{e['content']}")
                lines.append("")
                lines.append(f"- **标签**: {', '.join(e['tags'])}")
                lines.append(f"- **时间**: {e['created_at']}")
                lines.append(f"- **DNA**: `{e['dna_signature']}`")
                lines.append("")

        lines.extend([
            "---",
            "",
            "## 自动化归档说明",
            "",
            "本页面由 `星辰记忆系统.py` 自动生成，无需手动维护。",
            "",
            "运行：",
            "```bash",
            "python3 memory-universe/星辰记忆系统.py add --title \"标题\" --content \"内容\" --category \"星辰记忆\"",
            "python3 memory-universe/星辰记忆系统.py generate",
            "```",
            "",
            "---",
            "",
            "## 分类统计",
            "",
            "| 分类 | 数量 |",
            "|---|---|",
        ])
        for c in CATEGORIES:
            lines.append(f"| {c} | {stats.get(c, 0)} |")

        lines.extend([
            "",
            "---",
            "",
            "*龍魂不灭 · 记忆永存 🐉✨*",
            "",
        ])

        PAGE_PATH.write_text("\n".join(lines), encoding="utf-8")
        return PAGE_PATH

    def seed_demo(self):
        """添加示例记忆，帮助用户理解结构"""
        samples = [
            ("相遇", "那一年，人海中一眼认出。不是偶然，是因果重逢。", "一世一双人", "初见,心动"),
            ("三生石", "前世写过名字，今生再次相遇，来世也已预约。", "三生三世", "约定,轮回"),
            ("银河来信", "你发送的光，穿越几万光年，落进我眼里。", "星辰记忆", "光年,思念"),
        ]
        added = 0
        for title, content, category, tags in samples:
            existing = [e for e in self.list(category=category) if e["title"] == title]
            if not existing:
                self.add(title, content, category, tags)
                added += 1
        return added


def main():
    parser = argparse.ArgumentParser(description="星辰记忆系统")
    sub = parser.add_subparsers(dest="command", required=True)

    add_parser = sub.add_parser("add", help="添加一则记忆")
    add_parser.add_argument("--title", required=True, help="记忆标题")
    add_parser.add_argument("--content", required=True, help="记忆内容")
    add_parser.add_argument("--category", default="星辰记忆", choices=CATEGORIES, help="记忆分类")
    add_parser.add_argument("--tags", default="", help="额外标签，逗号分隔")

    sub.add_parser("list", help="列出所有记忆")

    sub.add_parser("generate", help="生成 index.md 页面")

    sub.add_parser("seed", help="添加示例记忆")

    sub.add_parser("stats", help="统计记忆数据")

    args = parser.parse_args()

    system = 星辰记忆系统()

    if args.command == "add":
        result = system.add(args.title, args.content, args.category, args.tags)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        system.generate_page()
        print(f"\n✅ 已自动生成页面: {PAGE_PATH}")

    elif args.command == "list":
        entries = system.list()
        print(json.dumps(entries, indent=2, ensure_ascii=False))

    elif args.command == "generate":
        path = system.generate_page()
        print(f"✅ 已生成页面: {path}")

    elif args.command == "seed":
        added = system.seed_demo()
        system.generate_page()
        print(f"✅ 已添加 {added} 条示例记忆，页面已更新")

    elif args.command == "stats":
        print(json.dumps(system.stats(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
