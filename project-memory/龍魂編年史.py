#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂编年史 v1.0

把原本锁在 Claude 记忆档里的项目历史，变成龍魂系统自己的可执行资产。

功能：
- 记录里程碑（标题、分类、内容、来源）
- 每条记录生成 DNA 签名
- 自动生成结构化 Markdown 页面
- 索引 cnsh-core/规范 目录

普通人只需：添加里程碑 → 系统自动归档 → 生成页面。

DNA:#龍芯⚡️2026-06-18-LONGHUN-CHRONICLE-v1.0
"""

import argparse
import hashlib
import json
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "project-memory" / "chronicle.db"
PAGE_PATH = ROOT / "project-memory" / "index.md"
ARCHIVE = ROOT / "project-memory" / "Claude_MEMORY_ARCHIVE.md"
SPECS_DIR = ROOT / "cnsh-core" / "规范"

CATEGORIES = ["系统验收", "协议焊死", "生产部署", "理论突破", "工具发布", "其他"]


def dna_signature(title: str, content: str, timestamp: str) -> str:
    raw = f"{title}|{content}|{timestamp}|{uuid.uuid4().hex[:8]}".encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()[:16].upper()
    return f"#龍芯⚡️{timestamp.replace('-','').replace(':','').replace('.','')[:14]}-CHRONICLE-{digest}"


class 龍魂编年史:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS milestones (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    category TEXT NOT NULL,
                    source TEXT,
                    created_at TEXT NOT NULL,
                    dna_signature TEXT NOT NULL
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_cat ON milestones(category)")

    def add(self, title: str, content: str, category: str = "其他", source: str = "") -> Dict:
        if category not in CATEGORIES:
            category = "其他"
        created_at = datetime.now().isoformat()
        mid = f"MS-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"
        dna = dna_signature(title, content, created_at)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO milestones (id, title, content, category, source, created_at, dna_signature)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (mid, title, content, category, source, created_at, dna))
        return {"id": mid, "title": title, "category": category, "dna_signature": dna, "created_at": created_at}

    def list(self, category: Optional[str] = None, limit: int = 200) -> List[Dict]:
        query = "SELECT * FROM milestones"
        params = []
        if category and category in CATEGORIES:
            query += " WHERE category = ?"
            params.append(category)
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(query, params).fetchall()
        return [
            {"id": r[0], "title": r[1], "content": r[2], "category": r[3], "source": r[4], "created_at": r[5], "dna_signature": r[6]}
            for r in rows
        ]

    def stats(self) -> Dict:
        with sqlite3.connect(self.db_path) as conn:
            total = conn.execute("SELECT COUNT(*) FROM milestones").fetchone()[0]
            by_cat = conn.execute("SELECT category, COUNT(*) FROM milestones GROUP BY category").fetchall()
        return {"total": total, **{c: 0 for c in CATEGORIES}, **{c: n for c, n in by_cat}}

    def seed(self):
        """从 Claude 记忆档中提取关键里程碑，作为系统自有资产启动"""
        samples = [
            ("龍魂系统完整测试验收通过", "2026-06-10 系统生产就绪：2,317 个 Python 档案、642 个核心模组、成熟度 98/100。", "系统验收", "Claude_MEMORY_ARCHIVE.md"),
            ("生产部署引擎 Staging 验收完成", "2026-06-08 27/27 步骤通过，蓝绿部署、监控告警、灾难恢复就绪。", "生产部署", "Claude_MEMORY_ARCHIVE.md"),
            ("龍魂宪章 v1.1 确立为唯一真源", "2026-06-08 v1.0 协议废弃，v1.1 成为全球可见规范。", "协议焊死", "Claude_MEMORY_ARCHIVE.md"),
            ("龍魂·黎曼猜想 arXiv 投稿成功", "2026-06-08 论文编号 2406.12459，全球发布，永久存档。", "理论突破", "Claude_MEMORY_ARCHIVE.md"),
            ("GPG 签署管理工具整合主干", "2026-06-08 CNSH_v2.0_SIGN 融入主干，签署从 bash 升级为 Python。", "工具发布", "Claude_MEMORY_ARCHIVE.md"),
        ]
        added = 0
        for title, content, category, source in samples:
            existing = [m for m in self.list(category=category) if m["title"] == title]
            if not existing:
                self.add(title, content, category, source)
                added += 1
        return added

    def list_specs(self) -> List[Dict]:
        """索引 cnsh-core/规范 目录"""
        if not SPECS_DIR.exists():
            return []
        specs = []
        for path in sorted(SPECS_DIR.glob("*.md")):
            specs.append({
                "name": path.name,
                "path": str(path.relative_to(ROOT)),
                "size_kb": round(path.stat().st_size / 1024, 1),
            })
        return specs

    def generate_page(self) -> Path:
        milestones = self.list(limit=500)
        stats = self.stats()
        specs = self.list_specs()

        lines = [
            "# 🐉 龍魂编年史 · 项目记忆宇宙",
            "",
            f"> DNA: `{dna_signature('龍魂编年史', '项目记忆宇宙', datetime.now().isoformat())}`",
            f"> 生成时间: {datetime.now().isoformat()}",
            f"> 里程碑总数: {stats['total']}",
            f"> 规范文件数: {len(specs)}",
            "",
            "---",
            "",
            "## 缘起",
            "",
            "原本这些记忆锁在 Claude 的记忆档里，不属于系统，也无法被普通人调用。",
            "现在它们是龍魂系统自己的资产：可读、可查、可追加、可 DNA 追溯。",
            "",
            "---",
            "",
        ]

        for category in CATEGORIES:
            cat_items = [m for m in milestones if m["category"] == category]
            lines.append(f"## {category}")
            lines.append("")
            if not cat_items:
                lines.append("*暂无记录。*")
                lines.append("")
                continue
            for m in cat_items:
                lines.append(f"### {m['title']}")
                lines.append("")
                lines.append(m["content"])
                lines.append("")
                lines.append(f"- **来源**: {m['source'] or '手动录入'}")
                lines.append(f"- **时间**: {m['created_at']}")
                lines.append(f"- **DNA**: `{m['dna_signature']}`")
                lines.append("")

        lines.extend([
            "---",
            "",
            "## 规范索引",
            "",
            "| 文件名 | 大小 | 路径 |",
            "|---|---|---|",
        ])
        for s in specs:
            lines.append(f"| {s['name']} | {s['size_kb']} KB | `{s['path']}` |")

        lines.extend([
            "",
            "---",
            "",
            "## 自动化说明",
            "",
            "本页面由 `project-memory/龍魂编年史.py` 自动生成。",
            "",
            "```bash",
            "# 添加里程碑",
            "python3 project-memory/龍魂编年史.py add --title \"标题\" --content \"内容\" --category \"系统验收\"",
            "",
            "# 生成页面",
            "python3 project-memory/龍魂编年史.py generate",
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
            "*龍魂不灭 · 记忆归主 🐉*",
            "",
        ])

        PAGE_PATH.write_text("\n".join(lines), encoding="utf-8")
        return PAGE_PATH


def main():
    parser = argparse.ArgumentParser(description="龍魂编年史")
    sub = parser.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add", help="添加里程碑")
    add_p.add_argument("--title", required=True)
    add_p.add_argument("--content", required=True)
    add_p.add_argument("--category", default="其他", choices=CATEGORIES)
    add_p.add_argument("--source", default="")

    sub.add_parser("list", help="列出里程碑")
    sub.add_parser("seed", help="从 Claude 记忆档初始化示例")
    sub.add_parser("generate", help="生成 index.md")
    sub.add_parser("stats", help="统计")
    sub.add_parser("specs", help="列出规范文件")

    args = parser.parse_args()
    ch = 龍魂编年史()

    if args.command == "add":
        r = ch.add(args.title, args.content, args.category, args.source)
        print(json.dumps(r, indent=2, ensure_ascii=False))
        ch.generate_page()
        print(f"\n✅ 已生成页面: {PAGE_PATH}")
    elif args.command == "list":
        print(json.dumps(ch.list(), indent=2, ensure_ascii=False))
    elif args.command == "seed":
        n = ch.seed()
        ch.generate_page()
        print(f"✅ 已初始化 {n} 条里程碑，页面已更新")
    elif args.command == "generate":
        print(f"✅ 已生成页面: {ch.generate_page()}")
    elif args.command == "stats":
        print(json.dumps(ch.stats(), indent=2, ensure_ascii=False))
    elif args.command == "specs":
        print(json.dumps(ch.list_specs(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
