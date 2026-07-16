#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂本地知识库 · SQLite + FTS5 + DNA/关键词索引 + LonghunFont 视觉卡片

DNA: #龍芯⚡️2026-06-23-LONGHUN-KB-v1.0
"""
from __future__ import annotations

import argparse
import html
import json
import os
import pathlib
import re
import shutil
import sqlite3
import sys
import textwrap
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any

from PIL import Image, ImageDraw, ImageFont

# 引入书法渲染引擎（项目内路径）
_CALLIGRAPHY_ROOT = pathlib.Path(__file__).resolve().parents[1] / "longhun-font"
if str(_CALLIGRAPHY_ROOT) not in sys.path:
    sys.path.insert(0, str(_CALLIGRAPHY_ROOT))
import calligraphy

HOME = pathlib.Path.home()
OUT_DIR = HOME / ".longhun" / "notion_pages"
DB_PATH = OUT_DIR / "notion_pages.db"
DEFAULT_FONT = (
    pathlib.Path(__file__).resolve().parents[1]
    / "longhun-font"
    / "output"
    / "LonghunFont-Regular.otf"
)
FALLBACK_FONTS = [
    # 优先用 PingFang：CJK + 常见 emoji 都全，阅读性最好
    pathlib.Path("/System/Library/Fonts/PingFang.ttc"),
    pathlib.Path("/System/Library/Fonts/STHeiti Medium.ttc"),
    pathlib.Path("/System/Library/Fonts/Apple Color Emoji.ttc"),
    pathlib.Path("/Library/Fonts/Arial Unicode.ttf"),
]

CST = timezone(timedelta(hours=8))

# 龍魂 DNA 标签正则
DNA_PATTERNS = [
    re.compile(r"#龍芯⚡️[\w\-:\.\u4e00-\u9fff]+"),
    re.compile(r"#CONFIRM🌌9622-ONLY-ONCE🧬[\w\-]+"),
    re.compile(r"#ZHUGEXIN⚡️[\w\-:\.🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️]+"),
]

# 🎨 龍魂五色 · 五行情绪映射
# 金=收敛/判定  木=生长/扩展  水=流动/同步  火=核心/热烈  土=稳定/底座
WUXING = {
    "金": {
        "name": "金",
        "emotion": "明断 · 收敛",
        "rgb": (232, 196, 103),
        "hex": "#e8c467",
        "keyword": ["AI", "智能", "算法", "判定", "合规"],
    },
    "木": {
        "name": "木",
        "emotion": "生长 · 扩展",
        "rgb": (76, 175, 125),
        "hex": "#4caf7d",
        "keyword": ["子页面", "扩展", "模块", "创作", "生态"],
    },
    "水": {
        "name": "水",
        "emotion": "流动 · 同步",
        "rgb": (74, 144, 226),
        "hex": "#4a90e2",
        "keyword": ["同步", "备份", "传输", "日志", "流水"],
    },
    "火": {
        "name": "火",
        "emotion": "核心 · 热烈",
        "rgb": (226, 85, 85),
        "hex": "#e25555",
        "keyword": ["DNA", "追溯", "核心", "主权", "安全"],
    },
    "土": {
        "name": "土",
        "emotion": "稳定 · 承载",
        "rgb": (199, 163, 111),
        "hex": "#c7a36f",
        "keyword": ["工作区", "底座", "归档", "系统", "规范"],
    },
}


def category_to_wuxing(category: str) -> dict[str, Any]:
    """根据分类名匹配五行情绪。"""
    cat = category or ""
    for wx, info in WUXING.items():
        for kw in info["keyword"]:
            if kw in cat:
                return info
    # 默认：按 hash 取五行，保证稳定
    idx = sum(ord(c) for c in cat) % 5
    return list(WUXING.values())[idx]


def rgb_to_hex(rgb: tuple[Any, ...]) -> str:
    return "#%02x%02x%02x" % rgb


def init_db() -> sqlite3.Connection:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    # 复用 downloader 的 pages 表
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pages (
            id TEXT PRIMARY KEY,
            title TEXT,
            icon TEXT,
            category TEXT,
            subcategory TEXT,
            notion_url TEXT,
            created TEXT,
            modified TEXT,
            local_md_path TEXT,
            status TEXT DEFAULT 'pending',
            error TEXT,
            word_count INTEGER DEFAULT 0,
            block_count INTEGER DEFAULT 0,
            downloaded_at TEXT,
            phase TEXT,
            dna TEXT
        )
    """)
    # FTS5 全文检索
    conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS page_fts USING fts5(
            title, content, page_id UNINDEXED,
            tokenize='trigram'
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS dna_tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page_id TEXT NOT NULL,
            tag TEXT NOT NULL,
            context TEXT,
            FOREIGN KEY(page_id) REFERENCES pages(id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS page_keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page_id TEXT NOT NULL,
            keyword TEXT NOT NULL,
            FOREIGN KEY(page_id) REFERENCES pages(id)
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_dna_tag ON dna_tags(tag)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_kw ON page_keywords(keyword)")
    ensure_cards_table(conn)
    conn.commit()
    return conn


def ensure_cards_table(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cards (
            page_id TEXT PRIMARY KEY,
            path TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)


def save_card_path(conn: sqlite3.Connection, page_id: str, path: str) -> None:
    ensure_cards_table(conn)
    conn.execute(
        "INSERT OR REPLACE INTO cards(page_id, path, created_at) VALUES(?,?,?)",
        (page_id, path, datetime.now(CST).isoformat()),
    )
    conn.commit()


def extract_dna_tags(text: str) -> List[str]:
    found: List[str] = []
    for pat in DNA_PATTERNS:
        found.extend(pat.findall(text))
    return sorted(set(found))


def index_pages(conn: sqlite3.Connection, force: bool = False) -> Dict[str, int]:
    rows = conn.execute(
        "SELECT id, local_md_path, title, category, subcategory FROM pages WHERE status='done'"
    ).fetchall()
    stats = {"indexed": 0, "skipped": 0, "errors": 0}
    for row in rows:
        page_id, md_path, title, category, subcategory = row
        if not md_path or not pathlib.Path(md_path).exists():
            stats["errors"] += 1
            continue
        # 若已索引且非强制，简单跳过
        if not force:
            cur = conn.execute("SELECT 1 FROM page_fts WHERE page_id=?", (page_id,))
            if cur.fetchone():
                stats["skipped"] += 1
                continue
        content = pathlib.Path(md_path).read_text(encoding="utf-8")
        # 清掉旧索引
        conn.execute("DELETE FROM page_fts WHERE page_id=?", (page_id,))
        conn.execute("DELETE FROM dna_tags WHERE page_id=?", (page_id,))
        conn.execute("DELETE FROM page_keywords WHERE page_id=?", (page_id,))
        # 插入 FTS
        conn.execute(
            "INSERT INTO page_fts(title, content, page_id) VALUES(?,?,?)",
            (title or "", content, page_id),
        )
        # DNA 标签
        for tag in extract_dna_tags(content):
            conn.execute(
                "INSERT INTO dna_tags(page_id, tag, context) VALUES(?,?,?)",
                (page_id, tag, ""),
            )
        # 关键词：标题分词 + 分类
        keywords = set()
        if title:
            keywords.update(re.findall(r"[\u4e00-\u9fff]{2,}", title))
        if category:
            keywords.add(category)
        if subcategory and subcategory != category:
            keywords.add(subcategory)
        for kw in keywords:
            conn.execute(
                "INSERT INTO page_keywords(page_id, keyword) VALUES(?,?)",
                (page_id, kw),
            )
        conn.commit()
        stats["indexed"] += 1
    return stats


def search_kb(conn: sqlite3.Connection, query: str, limit: int = 20) -> List[Dict]:
    sql = """
        SELECT p.id, p.title, p.icon, p.category, p.notion_url, p.local_md_path,
               p.word_count, p.phase, p.dna,
               snippet(page_fts, 1, '**', '**', '…', 80) AS snippet,
               rank
        FROM page_fts
        JOIN pages p ON p.id = page_fts.page_id
        WHERE page_fts MATCH ?
        ORDER BY rank
        LIMIT ?
    """
    rows = conn.execute(sql, (query, limit)).fetchall()
    results = []
    for r in rows:
        results.append({
            "id": r[0],
            "title": r[1],
            "icon": r[2],
            "category": r[3],
            "notion_url": r[4],
            "local_md_path": r[5],
            "word_count": r[6],
            "phase": r[7],
            "dna": r[8],
            "snippet": r[9],
            "rank": r[10],
        })
    return results


def list_missing(conn: sqlite3.Connection, limit: int = 50) -> List[Dict]:
    rows = conn.execute(
        """SELECT id, title, category, status, error, notion_url FROM pages
           WHERE status != 'done' ORDER BY category LIMIT ?""",
        (limit,),
    ).fetchall()
    return [
        {"id": r[0], "title": r[1], "category": r[2], "status": r[3], "error": r[4], "url": r[5]}
        for r in rows
    ]


def load_fallback_font(size: int) -> ImageFont.FreeTypeFont:
    for f in FALLBACK_FONTS:
        if f.exists():
            try:
                return ImageFont.truetype(str(f), size)
            except Exception:
                continue
    raise RuntimeError("找不到可用的中文字体")


def char_use_longhun(ch: str) -> bool:
    """LonghunFont 目前仅对拉丁字母、数字、常见标点有艺术字形；
    CJK、emoji、CJK标点使用系统字体兜底。"""
    o = ord(ch)
    # ASCII / Latin-1 补充标点
    if o < 0x3000:
        return True
    # 排除 CJK 标点区中的部分符号，让中文更自然
    if 0x3000 <= o <= 0x303F:
        return False
    return False


def draw_mixed_line(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    text: str,
    size: int,
    fill: tuple[Any, ...],
    longhun_path: pathlib.Path = DEFAULT_FONT,
) -> int:
    """用 LonghunFont + 系统中文字体混合绘制一行文本，返回绘制后的 x 坐标。"""
    longhun_font = ImageFont.truetype(str(longhun_path), size)
    fallback_font = load_fallback_font(size)
    seg_font = longhun_font
    seg_text = ""
    for ch in text:
        target = longhun_font if char_use_longhun(ch) else fallback_font
        if target is not seg_font and seg_text:
            draw.text((x, y), seg_text, font=seg_font, fill=fill)
            x += int(draw.textlength(seg_text, font=seg_font))
            seg_text = ""
        seg_font = target
        seg_text += ch
    if seg_text:
        draw.text((x, y), seg_text, font=seg_font, fill=fill)
        x += int(draw.textlength(seg_text, font=seg_font))
    return x


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> List[str]:
    """按像素宽度折行（支持中文）。"""
    lines: List[str] = []
    draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    for para in text.splitlines():
        if not para.strip():
            continue
        line = ""
        for ch in para:
            test = line + ch
            if draw.textlength(test, font=font) <= max_width:
                line = test
            else:
                if line:
                    lines.append(line)
                line = ch
        if line:
            lines.append(line)
    return lines


def render_calligraphy_banner(
    title: str,
    output_path: pathlib.Path,
    style_code: str = "WXZ-XS",
    size: tuple[Any, ...] = (1200, 280),
) -> pathlib.Path:
    """把页面标题渲染成书法横幅，返回最终图片路径。"""
    text = re.sub(r"[^\u4e00-\u9fff]", "", title)  # 只保留 CJK
    if not text:
        text = "龍魂"
    text = text[:8]  # 横幅太长不好看
    style = calligraphy.load_style(style_code)
    spacing_x = style.get("parameters", {}).get("spacing_x", 1.1)
    # 按横幅宽度自动压字号，确保不溢出
    font_size = min(220, int(size[0] / (max(len(text), 1) * spacing_x * 1.05)))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result = calligraphy.render(
        text=text,
        style_code=style_code,
        layout="horizontal",
        seal_text="龍魂",
        classic="LONGHUN",
        output_name=output_path.stem,
        size=size,
        font_size=font_size,
    )
    src = pathlib.Path(result["output"])
    if src != output_path:
        shutil.copy2(src, output_path)
    return output_path


def render_card(
    page_id: str,
    title: str,
    category: str,
    dna: str,
    excerpt: str,
    output_path: pathlib.Path,
    font_path: pathlib.Path = DEFAULT_FONT,
    calligraphy: bool = False,
    calligraphy_style: str = "WXZ-XS",
) -> pathlib.Path:
    """生成龍魂知识视觉卡片。中文/emoji 用系统字体兜底，英文/数字用 LonghunFont。
    启用 calligraphy 时，标题先渲染成书法横幅贴入卡片顶部。
    """
    W = 1200
    banner_path: Optional[pathlib.Path] = None
    if calligraphy:
        banner_path = render_calligraphy_banner(
            title,
            OUT_DIR / "cards" / f"banner_{page_id}.png",
            style_code=calligraphy_style,
            size=(W, 280),
        )
        H = 840
        banner_h = 280
    else:
        H = 630
        banner_h = 0

    wuxing = category_to_wuxing(category)
    wx_rgb = wuxing["rgb"]
    wx_hex = rgb_to_hex(wx_rgb)

    bg = Image.new("RGB", (W, H), color=(15, 15, 25))
    draw = ImageDraw.Draw(bg)

    # 贴入书法横幅
    if banner_path and banner_path.exists():
        banner = Image.open(banner_path).convert("RGB")
        bg.paste(banner, (0, 0))

    # 装饰边框：外层用五行情绪色，内层用暗金
    draw.rectangle([20, 20, W - 20, H - 20], outline=wx_rgb, width=4)
    draw.rectangle([30, 30, W - 30, H - 30], outline=(100, 70, 30), width=1)

    # 底部五色情绪条：把分类情绪可视化
    bar_h = 12
    draw.rectangle([20, H - 20 - bar_h, W - 20, H - 20], fill=wx_rgb)
    font_wx = load_fallback_font(22)
    emotion_text = f"{wuxing['name']} · {wuxing['emotion']}"
    tw = int(draw.textlength(emotion_text, font=font_wx))
    draw.text((W - 40 - tw, H - 20 - bar_h - 34), emotion_text, font=font_wx, fill=wx_rgb)

    # 折行用兜底字体计算宽度
    font_title_wrap = load_fallback_font(56)
    font_meta_wrap = load_fallback_font(28)
    font_body_wrap = load_fallback_font(32)

    # 标题（横幅下方）
    y = banner_h + 50
    if calligraphy:
        # 书法横幅已有艺术字标题，下方用清晰系统字体显示完整标题
        for line in wrap_text(title, font_title_wrap, W - 120):
            draw.text((60, y), line, font=font_title_wrap, fill=(240, 220, 180))
            y += 70
    else:
        for line in wrap_text(title, font_title_wrap, W - 120):
            draw_mixed_line(draw, 60, y, line, 56, (240, 220, 180), font_path)
            y += 70

    # 元信息、摘要、水印使用系统中文字体，避免 URL/日期/英文 DNA 用艺术字导致难读
    y += 20
    meta = f"分类：{category}  ·  DNA：{dna[:60]}..."
    for line in wrap_text(meta, font_meta_wrap, W - 120):
        draw.text((60, y), line, font=font_meta_wrap, fill=(160, 160, 160))
        y += 40

    # 分隔
    y += 10
    draw.line([60, y, W - 60, y], fill=(180, 140, 60), width=2)
    y += 30

    # 摘要
    for line in wrap_text(excerpt, font_body_wrap, W - 120)[:6]:
        draw.text((60, y), line, font=font_body_wrap, fill=(220, 220, 220))
        y += 50

    # 水印
    watermark = "龍魂知识库 · 本地主权 · UID9622"
    w_width = int(draw.textlength(watermark, font=font_meta_wrap))
    draw.text((W - w_width - 60, H - 50), watermark, font=font_meta_wrap, fill=(80, 80, 80))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    bg.save(output_path)
    return output_path


def cmd_init(args) -> None:
    conn = init_db()
    print(f"🟢 知识库已初始化：{DB_PATH}")
    conn.close()


def cmd_index(args) -> None:
    conn = init_db()
    stats = index_pages(conn, force=args.force)
    print(f"索引完成：新增 {stats['indexed']} | 跳过 {stats['skipped']} | 错误 {stats['errors']}")
    conn.close()


def cmd_search(args) -> None:
    conn = init_db()
    results = search_kb(conn, args.query, limit=args.limit)
    for r in results:
        print(f"\n[{r['icon']}] {r['title']}")
        print(f"   分类：{r['category']} | 字数：{r['word_count']} | 阶段：{r['phase']}")
        print(f"   本地：{r['local_md_path']}")
        print(f"   摘要：{r['snippet']}")
    if not results:
        print("未找到结果。")
    conn.close()


def cmd_missing(args) -> None:
    conn = init_db()
    missing = list_missing(conn, limit=args.limit)
    by_status: Dict[str, int] = {}
    for m in missing:
        by_status[m["status"]] = by_status.get(m["status"], 0) + 1
        print(f"[{m['status']}] [{m['category']}] {m['title'] or '无标题'}\n    {m['error'] or m['url']}")
    print("\n状态统计：", by_status)
    conn.close()


def cmd_render(args) -> None:
    conn = init_db()
    row = conn.execute(
        "SELECT id, title, category, dna, local_md_path FROM pages WHERE id=? OR title LIKE ?",
        (args.page, f"%{args.page}%"),
    ).fetchone()
    if not row:
        print("找不到页面。")
        return
    page_id, title, category, dna, md_path = row
    excerpt = ""
    if md_path and pathlib.Path(md_path).exists():
        text = pathlib.Path(md_path).read_text(encoding="utf-8")
        excerpt = text[:300].replace("#", "").replace("\n", " ")
    out = pathlib.Path(args.output or f"/tmp/longhun_card_{page_id}.png")
    render_card(
        page_id,
        title or "无标题",
        category or "",
        dna or "",
        excerpt,
        out,
        calligraphy=args.calligraphy,
        calligraphy_style=args.calligraphy_style,
    )
    save_card_path(conn, page_id, str(out))
    print(f"🖼️ 卡片已生成：{out}")
    conn.close()


def cmd_render_all(args) -> None:
    conn = init_db()
    rows = conn.execute(
        "SELECT id, title, category, dna, local_md_path FROM pages WHERE status='done'"
    ).fetchall()
    cards_dir = OUT_DIR / "cards"
    cards_dir.mkdir(parents=True, exist_ok=True)
    for i, row in enumerate(rows, 1):
        page_id, title, category, dna, md_path = row
        excerpt = ""
        if md_path and pathlib.Path(md_path).exists():
            text = pathlib.Path(md_path).read_text(encoding="utf-8")
            excerpt = text[:300].replace("#", "").replace("\n", " ")
        out = cards_dir / f"{page_id}.png"
        try:
            render_card(
                page_id,
                title or "无标题",
                category or "",
                dna or "",
                excerpt,
                out,
                calligraphy=args.calligraphy,
                calligraphy_style=args.calligraphy_style,
            )
            save_card_path(conn, page_id, str(out))
        except Exception as e:
            print(f"  [{i}/{len(rows)}] 🔴 {title or page_id}: {e}")
            continue
        if i % 10 == 0 or i == len(rows):
            print(f"  [{i}/{len(rows)}] 🟢 已生成 {i} 张卡片")
    print(f"🎴 批量卡片完成，保存在：{cards_dir}")
    conn.close()


def cmd_gallery(args) -> None:
    conn = init_db()
    rows = conn.execute("""
        SELECT c.page_id, c.path, p.title, p.category, p.local_md_path, p.notion_url
        FROM cards c
        JOIN pages p ON p.id = c.page_id
        ORDER BY p.category, p.title
    """).fetchall()
    # 统计五行情绪分布
    wuxing_counts: Dict[str, int] = {}
    conn2 = sqlite3.connect(DB_PATH)
    for r in conn2.execute("SELECT category FROM pages WHERE status='done'"):
        wx_name = category_to_wuxing(r[0])["name"]
        wuxing_counts[wx_name] = wuxing_counts.get(wx_name, 0) + 1
    conn2.close()
    marquee_items = " · ".join(
        f"<span style='color:{WUXING[n]['hex']}'>◆ {WUXING[n]['name']} {WUXING[n]['emotion']} ({c})</span>"
        for n, c in wuxing_counts.items()
    )

    cards_html = []
    for page_id, path, title, category, md_path, notion_url in rows:
        img = pathlib.Path(path).name
        title_e = html.escape(title or "无标题")
        category_e = html.escape(category or "")
        md_url = html.escape(f"file://{md_path}" if md_path else "")
        notion_e = html.escape(notion_url or "")
        wx = category_to_wuxing(category)
        wx_hex = wx["hex"]
        cards_html.append(f"""<div class="item" style="--wx:{wx_hex}">
  <a href="{md_url or notion_e}" target="_blank"><img src="{img}" loading="lazy" alt="{title_e}"></a>
  <h3>{title_e}</h3>
  <p><span class="wx-dot" style="background:{wx_hex}"></span>{category_e} · {wx['name']} {wx['emotion']}</p>
</div>""")

    body = "\n".join(cards_html)
    page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>龍魂知识库 · 视觉卡片画廊</title>
<style>
  :root {{ background:#0c0c14; color:#eee; font-family: -apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif; }}
  body {{ margin:0; padding:2rem; }}
  h1 {{ color:#e8c467; margin-bottom:.5rem; }}
  .meta {{ color:#888; margin-bottom:1.5rem; }}
  .marquee-wrap {{ background:linear-gradient(90deg,#161622,#1a1a2e,#161622); border-top:1px solid #2a2a3a; border-bottom:1px solid #2a2a3a; overflow:hidden; padding:.6rem 0; margin-bottom:1.5rem; }}
  .marquee {{ display:inline-block; white-space:nowrap; padding-left:100%; animation:scroll 24s linear infinite; font-size:.95rem; }}
  @keyframes scroll {{ 0% {{ transform:translateX(0); }} 100% {{ transform:translateX(-100%); }} }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(360px, 1fr)); gap:1.5rem; }}
  .item {{ background:#161622; border:2px solid var(--wx,#2a2a3a); border-radius:8px; overflow:hidden; transition:transform .2s,box-shadow .2s; }}
  .item:hover {{ transform:translateY(-4px); box-shadow:0 8px 24px rgba(0,0,0,.5), 0 0 12px var(--wx,#e8c46722); }}
  .item img {{ width:100%; display:block; }}
  .item h3 {{ margin:.8rem 1rem .3rem; font-size:1rem; color:#f5e6c3; }}
  .item p {{ margin:0 1rem 1rem; color:#888; font-size:.85rem; }}
  .wx-dot {{ display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:6px; box-shadow:0 0 6px currentColor; }}
  a {{ text-decoration:none; color:inherit; }}
</style>
</head>
<body>
<h1>🐉 龍魂知识库 · 视觉卡片画廊</h1>
<p class="meta">本地主权 · UID9622 · 共 {len(rows)} 张卡片 · 五色情绪脉动</p>
<div class="marquee-wrap">
  <div class="marquee">🌈 {marquee_items} · 金木水火土 · 系统有情绪 · 颜色即温度 · 🌈 {marquee_items}</div>
</div>
<div class="grid">
{body}
</div>
</body>
</html>"""
    out = OUT_DIR / "cards" / "index.html"
    out.write_text(page, encoding="utf-8")
    print(f"🌐 画廊已生成：{out}")
    conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="龍魂本地知识库")
    sub = parser.add_subparsers(dest="command")

    p_init = sub.add_parser("init", help="初始化数据库")
    p_init.set_defaults(func=cmd_init)

    p_index = sub.add_parser("index", help="为已下载页面建立全文/DNA/关键词索引")
    p_index.add_argument("--force", action="store_true", help="强制重新索引")
    p_index.set_defaults(func=cmd_index)

    p_search = sub.add_parser("search", help="全文检索")
    p_search.add_argument("query")
    p_search.add_argument("--limit", type=int, default=10)
    p_search.set_defaults(func=cmd_search)

    p_missing = sub.add_parser("missing", help="列出未下载/失败的页面")
    p_missing.add_argument("--limit", type=int, default=50)
    p_missing.set_defaults(func=cmd_missing)

    p_render = sub.add_parser("render", help="为页面生成 LonghunFont 视觉卡片")
    p_render.add_argument("page", help="页面 ID 或标题片段")
    p_render.add_argument("--output", "-o", help="输出图片路径")
    p_render.add_argument("--calligraphy", action="store_true", help="顶部使用书法横幅")
    p_render.add_argument("--calligraphy-style", default="WXZ-XS", help="书法样式代码，默认王羲之-行书")
    p_render.set_defaults(func=cmd_render)

    p_render_all = sub.add_parser("render-all", help="为所有已下载页面批量生成视觉卡片")
    p_render_all.add_argument("--calligraphy", action="store_true", help="顶部使用书法横幅（较慢）")
    p_render_all.add_argument("--calligraphy-style", default="WXZ-XS", help="书法样式代码，默认王羲之-行书")
    p_render_all.set_defaults(func=cmd_render_all)

    p_gallery = sub.add_parser("gallery", help="生成 HTML 视觉卡片画廊")
    p_gallery.set_defaults(func=cmd_gallery)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
