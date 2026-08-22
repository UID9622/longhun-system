#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · LU 记忆卡片画廊生成器

把 ~/.longhun/lu_memory/ 里的 LU 记忆和视觉卡片打包成一个本地 HTML 画廊，
支持关键词搜索、按时间排序、点击看原文（如果本地可访问）。

DNA:#龍芯⚡️丙午·甲午·乙亥·壬午·䷚颐-LONGHUN-LU-GALLERY-FILE1-v1.0
"""

import argparse
import json
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

HOME = Path.home()
LU_ROOT = HOME / ".longhun" / "lu_memory"
LU_DB = LU_ROOT / "lu_memory.db"
CARDS_DIR = LU_ROOT / "cards"
GALLERY_DIR = LU_ROOT / "gallery"

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>龍魂 · LU 记忆卡片画廊</title>
<style>
  :root {{ --bg:#0f0f12; --card:#18181d; --accent:#d4af37; --text:#e8e8e8; --muted:#999; }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; background:var(--bg); color:var(--text); padding:2rem; }}
  header {{ max-width:1400px; margin:0 auto 2rem; text-align:center; }}
  h1 {{ color:var(--accent); margin:0 0 .5rem; font-size:2rem; }}
  .subtitle {{ color:var(--muted); font-size:.95rem; }}
  .stats {{ max-width:1400px; margin:0 auto 1.5rem; display:flex; gap:1rem; flex-wrap:wrap; justify-content:center; }}
  .stat {{ background:var(--card); padding:.6rem 1rem; border-radius:8px; border:1px solid #2a2a30; }}
  .controls {{ max-width:1400px; margin:0 auto 2rem; display:flex; gap:1rem; flex-wrap:wrap; justify-content:center; }}
  input[type="text"] {{ background:var(--card); color:var(--text); border:1px solid #333; padding:.6rem 1rem; border-radius:8px; width:min(100%, 360px); font-size:1rem; }}
  select {{ background:var(--card); color:var(--text); border:1px solid #333; padding:.6rem 1rem; border-radius:8px; }}
  .grid {{ max-width:1400px; margin:0 auto; display:grid; grid-template-columns:repeat(auto-fill, minmax(360px, 1fr)); gap:1.5rem; }}
  .item {{ background:var(--card); border:1px solid #2a2a30; border-radius:12px; overflow:hidden; transition:transform .15s, box-shadow .15s; }}
  .item:hover {{ transform:translateY(-4px); box-shadow:0 8px 24px rgba(212,175,55,.15); }}
  .item img {{ width:100%; height:auto; display:block; border-bottom:1px solid #2a2a30; }}
  .meta {{ padding:1rem; }}
  .code {{ font-family: "SFMono-Regular", Consolas, monospace; color:var(--accent); font-size:.9rem; word-break:break-all; }}
  .dna {{ font-family: monospace; color:var(--muted); font-size:.75rem; word-break:break-all; margin:.4rem 0; }}
  .title {{ font-size:1.05rem; margin:.6rem 0 .4rem; }}
  .summary {{ color:var(--muted); font-size:.9rem; line-height:1.4; }}
  .keywords {{ margin-top:.6rem; }}
  .keywords span {{ display:inline-block; background:#222; color:#ccc; padding:.2rem .5rem; border-radius:4px; font-size:.75rem; margin:0 .3rem .3rem 0; }}
  .footer {{ text-align:center; margin-top:3rem; color:var(--muted); font-size:.85rem; }}
  .hidden {{ display:none !important; }}
</style>
</head>
<body>
<header>
  <h1>🐉 龍魂 · LU 记忆卡片画廊</h1>
  <div class="subtitle">Long-form → Unified token · UID9622 首创认知压缩</div>
</header>

<div class="stats">
  <div class="stat">总记忆数：{total}</div>
  <div class="stat">总字符数：{total_chars:,}</div>
  <div class="stat">生成时间：{generated_at}</div>
</div>

<div class="controls">
  <input type="text" id="search" placeholder="搜索关键词、标题、LU短码、DNA..." oninput="filter()">
  <select id="sort" onchange="filter()">
    <option value="newest">最新优先</option>
    <option value="oldest">最早优先</option>
  </select>
</div>

<div class="grid" id="grid">
{items}
</div>

<div class="footer">
  DNA: {dna} · 本地主权 · 仅本地访问
</div>

<script>
const items = {items_js};
function filter() {{
  const q = document.getElementById('search').value.toLowerCase().trim();
  const sort = document.getElementById('sort').value;
  let visible = items.filter(it => {{
    if (!q) return true;
    return (it.lu_code + ' ' + it.dna + ' ' + it.title + ' ' + it.summary + ' ' + it.keywords.join(' ')).toLowerCase().includes(q);
  }});
  visible.sort((a,b) => sort === 'newest' ? b.ts.localeCompare(a.ts) : a.ts.localeCompare(b.ts));
  document.querySelectorAll('.item').forEach(el => {{
    const id = el.dataset.id;
    el.classList.toggle('hidden', !visible.some(v => v.id === id));
  }});
}}
</script>
</body>
</html>
"""


def _load_records(limit: int = 1000) -> List[Dict[str, Any]]:
    if not LU_DB.exists():
        return []
    conn = sqlite3.connect(str(LU_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT lu_code, dna, title, summary, keywords, char_count, card_path, created_at "
        "FROM lu_records WHERE status='active' ORDER BY created_at DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    records = []
    for r in rows:
        rec = dict(r)
        try:
            rec["keywords"] = json.loads(rec.get("keywords") or "[]")
        except Exception:
            rec["keywords"] = []
        records.append(rec)
    return records


def _copy_card(src: Path, gallery: Path) -> Path:
    dst = gallery / src.name
    shutil.copy2(str(src), str(dst))
    return dst


def generate(output_dir: Path = GALLERY_DIR) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    records = _load_records()
    total_chars = sum(r.get("char_count", 0) for r in records)

    items_html = []
    items_js = []
    for rec in records:
        card_src = Path(rec["card_path"]) if rec.get("card_path") else CARDS_DIR / f"{rec['lu_code'].replace('/', '')}.png"
        img_name = ""
        if card_src.exists():
            copied = _copy_card(card_src, output_dir)
            img_name = copied.name
        img_html = f'<img src="{img_name}" alt="{rec["lu_code"]}">' if img_name else '<div style="padding:2rem;text-align:center;color:#666">暂无视觉卡片</div>'

        keywords_html = "".join(f"<span>{k}</span>" for k in rec.get("keywords", [])[:12])
        item_id = rec["lu_code"].replace("/", "")
        items_html.append(
            f'<div class="item" data-id="{item_id}">\n'
            f'  {img_html}\n'
            f'  <div class="meta">\n'
            f'    <div class="code">{rec["lu_code"]}</div>\n'
            f'    <div class="dna">{rec["dna"]}</div>\n'
            f'    <div class="title">{rec.get("title") or rec.get("summary") or ""}</div>\n'
            f'    <div class="summary">{rec.get("summary", "")}</div>\n'
            f'    <div class="keywords">{keywords_html}</div>\n'
            f'  </div>\n'
            f'</div>'
        )
        items_js.append({
            "id": item_id,
            "lu_code": rec["lu_code"],
            "dna": rec["dna"],
            "title": rec.get("title") or "",
            "summary": rec.get("summary") or "",
            "keywords": rec.get("keywords", []),
            "ts": rec.get("created_at") or "",
        })

    html = HTML_TEMPLATE.format(
        total=len(records),
        total_chars=total_chars,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        items="\n".join(items_html),
        items_js=json.dumps(items_js, ensure_ascii=False),
        dna="#龍芯⚡️丙午·甲午·乙亥·壬午·䷚颐-LONGHUN-LU-GALLERY-v1.0",
    )

    index = output_dir / "index.html"
    index.write_text(html, encoding="utf-8")
    return index


def main() -> int:
    parser = argparse.ArgumentParser(description="龍魂 LU 记忆卡片画廊生成器")
    parser.add_argument("--output", "-o", type=Path, default=GALLERY_DIR, help="输出目录")
    args = parser.parse_args()
    path = generate(args.output)
    print(f"🟢 画廊已生成：{path}")
    print(f"   可用浏览器打开：file://{path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
