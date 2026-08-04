#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 Notion 下载缺失统计报告生成器

对比索引与本地数据库，输出 Markdown 缺失清单，便于最后统一补全。

DNA: #龍芯⚡️2026-06-23-NOTION-MISSING-REPORT-v1.0
"""
from __future__ import annotations

import json
import pathlib
import sqlite3
import sys
from collections import Counter
from datetime import datetime, timezone, timedelta

HOME = pathlib.Path.home()
INDEX_PATH = HOME / ".longhun" / "index" / "notion_exports.json"
DB_PATH = HOME / ".longhun" / "notion_pages" / "notion_pages.db"
OUT_PATH = HOME / ".longhun" / "notion_pages" / "MISSING_REPORT.md"
LONGHUN_KB = pathlib.Path("/Users/zuimeidedeyihan/longhun-system/scripts")
if str(LONGHUN_KB) not in sys.path:
    sys.path.insert(0, str(LONGHUN_KB))
from longhun_kb import WUXING, category_to_wuxing

CST = timezone(timedelta(hours=8))


def main() -> None:
    data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    entries = data.get("entries", [])
    conn = sqlite3.connect(DB_PATH)
    db_rows = conn.execute("SELECT id, status, error FROM pages").fetchall()
    db_map = {r[0]: {"status": r[1], "error": r[2]} for r in db_rows}

    missing = []
    for e in entries:
        pid = e["id"]
        rec = db_map.get(pid)
        if not rec or rec["status"] != "done":
            missing.append({
                "id": pid,
                "title": e.get("title", "无标题"),
                "category": e.get("category", ""),
                "notion_url": e.get("notion_url", ""),
                "status": rec["status"] if rec else "pending",
                "error": rec["error"] if rec else "",
            })

    cat_counter = Counter(m["category"] for m in missing)
    status_counter = Counter(m["status"] for m in missing)
    done_count = len(entries) - len(missing)

    # 已完成页面的五行情绪分布
    done_wx_counter: Counter = Counter()
    done_cats = conn.execute("SELECT category FROM pages WHERE status='done'")
    for (cat,) in done_cats:
        done_wx_counter[category_to_wuxing(cat)["name"]] += 1

    wx_bars = "\n".join(
        f"- <span style='color:{WUXING[n]['hex']}'>■</span> **{n}** {WUXING[n]['emotion']} · {done_wx_counter.get(n, 0)} 页"
        for n in WUXING
    )

    lines = [
        "# 🐉 Notion 本地下载缺失统计报告",
        "",
        f"- 生成时间：{datetime.now(CST).isoformat()}",
        f"- 索引总数：{len(entries)}",
        f"- 本地完成：{done_count}",
        f"- 缺失总数：{len(missing)}",
        "",
        "## 五色情绪 · 已完成页面气质",
        "",
        wx_bars,
        "",
        "> 🎨 金=明断收敛 · 木=生长扩展 · 水=流动同步 · 火=核心热烈 · 土=稳定承载",
        "",
        "## 状态分布",
        "",
        "| 状态 | 数量 |",
        "|---|---|",
    ]
    for status, count in status_counter.most_common():
        lines.append(f"| {status} | {count} |")

    lines += ["", "## 分类分布（缺失）", "", "| 分类 | 数量 |", "|---|---|"]
    for cat, count in cat_counter.most_common():
        lines.append(f"| {cat} | {count} |")

    lines += ["", "## 失败页面详情", "", "| 分类 | 标题 | 错误 |", "|---|---|---|"]
    for m in missing:
        if m["status"] == "error":
            err = (m["error"] or "").replace("\n", " ")[:120]
            lines.append(f"| {m['category']} | {m['title'][:60]} | {err} |")

    lines += ["", "## 超大页面（延后处理）", "", "| 分类 | 标题 | 备注 |", "|---|---|---|"]
    for m in missing:
        if m["status"] == "large":
            lines.append(f"| {m['category']} | {m['title'][:60]} | block 数超过上限，需单独处理 |")

    pending = [m for m in missing if m["status"] not in ("error", "large")]
    pending_top = pending[:100]
    lines += [
        "",
        f"## 未开始/待处理页面（前 {len(pending_top)} / {len(pending)}）",
        "",
        "| 分类 | 标题 | Notion URL |",
        "|---|---|---|",
    ]
    for m in pending_top:
        lines.append(f"| {m['category']} | {m['title'][:60]} | {m['notion_url']} |")
    if len(pending) > len(pending_top):
        lines.append(f"| … | … | 还有 {len(pending) - len(pending_top)} 条未列出 |")

    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"📝 缺失报告已生成：{OUT_PATH}")
    print(f"   索引 {len(entries)} | 完成 {done_count} | 缺失 {len(missing)}")
    print(f"   按状态：{dict(status_counter)}")


if __name__ == "__main__":
    main()
