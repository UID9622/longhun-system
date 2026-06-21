#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂編年史 v1.0

把原本鎖在 Claude 記憶檔裡的項目歷史，變成龍魂系統自己的可執行資產。

功能：
- 記錄里程碑（標題、分類、內容、來源）
- 每條記錄生成 DNA 簽名
- 自動生成結構化 Markdown 頁面
- 索引 cnsh-core/規範 目錄

普通人只需：添加里程碑 → 系統自動歸檔 → 生成頁面。

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

CATEGORIES = ["系統驗收", "協議焊死", "生產部署", "理論突破", "工具發布", "其他"]


def dna_signature(title: str, content: str, timestamp: str) -> str:
    raw = f"{title}|{content}|{timestamp}|{uuid.uuid4().hex[:8]}".encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()[:16].upper()
    return f"#龍芯⚡️{timestamp.replace('-','').replace(':','').replace('.','')[:14]}-CHRONICLE-{digest}"


class 龍魂編年史:
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
        """從 Claude 記憶檔中提取關鍵里程碑，作為系統自有資產啟動"""
        samples = [
            ("龍魂系統完整測試驗收通過", "2026-06-10 系統生產就緒：2,317 個 Python 檔案、642 個核心模組、成熟度 98/100。", "系統驗收", "Claude_MEMORY_ARCHIVE.md"),
            ("生產部署引擎 Staging 驗收完成", "2026-06-08 27/27 步驟通過，藍綠部署、監控告警、災難恢復就緒。", "生產部署", "Claude_MEMORY_ARCHIVE.md"),
            ("龍魂憲章 v1.1 確立為唯一真源", "2026-06-08 v1.0 協議廢棄，v1.1 成為全球可見規範。", "協議焊死", "Claude_MEMORY_ARCHIVE.md"),
            ("龍魂·黎曼猜想 arXiv 投稿成功", "2026-06-08 論文編號 2406.12459，全球發佈，永久存檔。", "理論突破", "Claude_MEMORY_ARCHIVE.md"),
            ("GPG 簽署管理工具整合主干", "2026-06-08 CNSH_v2.0_SIGN 融入主干，簽署從 bash 升級為 Python。", "工具發布", "Claude_MEMORY_ARCHIVE.md"),
        ]
        added = 0
        for title, content, category, source in samples:
            existing = [m for m in self.list(category=category) if m["title"] == title]
            if not existing:
                self.add(title, content, category, source)
                added += 1
        return added

    def list_specs(self) -> List[Dict]:
        """索引 cnsh-core/規範 目錄"""
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
            "# 🐉 龍魂編年史 · 項目記憶宇宙",
            "",
            f"> DNA: `{dna_signature('龍魂編年史', '項目記憶宇宙', datetime.now().isoformat())}`",
            f"> 生成時間: {datetime.now().isoformat()}",
            f"> 里程碑總數: {stats['total']}",
            f"> 規範文件數: {len(specs)}",
            "",
            "---",
            "",
            "## 缘起",
            "",
            "原本這些記憶鎖在 Claude 的記憶檔裡，不屬於系統，也無法被普通人調用。",
            "現在它們是龍魂系統自己的資產：可讀、可查、可追加、可 DNA 追溯。",
            "",
            "---",
            "",
        ]

        for category in CATEGORIES:
            cat_items = [m for m in milestones if m["category"] == category]
            lines.append(f"## {category}")
            lines.append("")
            if not cat_items:
                lines.append("*暫無記錄。*")
                lines.append("")
                continue
            for m in cat_items:
                lines.append(f"### {m['title']}")
                lines.append("")
                lines.append(m["content"])
                lines.append("")
                lines.append(f"- **來源**: {m['source'] or '手動錄入'}")
                lines.append(f"- **時間**: {m['created_at']}")
                lines.append(f"- **DNA**: `{m['dna_signature']}`")
                lines.append("")

        lines.extend([
            "---",
            "",
            "## 規範索引",
            "",
            "| 文件名 | 大小 | 路徑 |",
            "|---|---|---|",
        ])
        for s in specs:
            lines.append(f"| {s['name']} | {s['size_kb']} KB | `{s['path']}` |")

        lines.extend([
            "",
            "---",
            "",
            "## 自動化說明",
            "",
            "本頁面由 `project-memory/龍魂編年史.py` 自動生成。",
            "",
            "```bash",
            "# 添加里程碑",
            "python3 project-memory/龍魂編年史.py add --title \"標題\" --content \"內容\" --category \"系統驗收\"",
            "",
            "# 生成頁面",
            "python3 project-memory/龍魂編年史.py generate",
            "```",
            "",
            "---",
            "",
            "## 分類統計",
            "",
            "| 分類 | 數量 |",
            "|---|---|",
        ])
        for c in CATEGORIES:
            lines.append(f"| {c} | {stats.get(c, 0)} |")

        lines.extend([
            "",
            "---",
            "",
            "*龍魂不滅 · 記憶歸主 🐉*",
            "",
        ])

        PAGE_PATH.write_text("\n".join(lines), encoding="utf-8")
        return PAGE_PATH


def main():
    parser = argparse.ArgumentParser(description="龍魂編年史")
    sub = parser.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add", help="添加里程碑")
    add_p.add_argument("--title", required=True)
    add_p.add_argument("--content", required=True)
    add_p.add_argument("--category", default="其他", choices=CATEGORIES)
    add_p.add_argument("--source", default="")

    sub.add_parser("list", help="列出里程碑")
    sub.add_parser("seed", help="從 Claude 記憶檔初始化示例")
    sub.add_parser("generate", help="生成 index.md")
    sub.add_parser("stats", help="統計")
    sub.add_parser("specs", help="列出規範文件")

    args = parser.parse_args()
    ch = 龍魂編年史()

    if args.command == "add":
        r = ch.add(args.title, args.content, args.category, args.source)
        print(json.dumps(r, indent=2, ensure_ascii=False))
        ch.generate_page()
        print(f"\n✅ 已生成頁面: {PAGE_PATH}")
    elif args.command == "list":
        print(json.dumps(ch.list(), indent=2, ensure_ascii=False))
    elif args.command == "seed":
        n = ch.seed()
        ch.generate_page()
        print(f"✅ 已初始化 {n} 條里程碑，頁面已更新")
    elif args.command == "generate":
        print(f"✅ 已生成頁面: {ch.generate_page()}")
    elif args.command == "stats":
        print(json.dumps(ch.stats(), indent=2, ensure_ascii=False))
    elif args.command == "specs":
        print(json.dumps(ch.list_specs(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
