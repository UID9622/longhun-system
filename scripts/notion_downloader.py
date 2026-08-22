#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
🐉 Notion 云端正文下载器 · 龍魂本地知识库建设

功能：
1. 读取 ~/.longhun/index/notion_exports.json 中的页面索引。
2. 使用 Notion Integration Token 从云端拉取 block children，转成 Markdown。
3. 保存到 ~/.longhun/notion_pages/<category>/<safe_title>_<id>.md。
4. 元数据写入 ~/.longhun/notion_pages/notion_pages.db（SQLite）。
5. 分阶段下载，支持断点续传、强制刷新、缺失统计。

DNA: #龍芯⚡️丙午·甲午·戊辰·戊午·䷑蛊-NOTION-DOWNLOADER-v1.0
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import sqlite3
import sys
import time
import unicodedata
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

import requests

CST = timezone(timedelta(hours=8))

HOME = pathlib.Path.home()
INDEX_PATH = HOME / ".longhun" / "index" / "notion_exports.json"
OUT_DIR = HOME / ".longhun" / "notion_pages"
DB_PATH = OUT_DIR / "notion_pages.db"
SECRETS_PATH = HOME / ".longhun" / "secrets.env"

# 分阶段配置：阶段 -> 类别集合
PHASES: Dict[str, List[str]] = {
    "P0": ["龍魂系统", "工作区页面", "核心价值", "核心控制"],
    "P1": ["子页面", "DNA追溯", "法律合规", "系统保护", "安全加密", "AI智能", "同步备份"],
    "P2": ["数据库页面", "价值体系", "人格系统", "道德经", "知识库", "目标规划"],
    "P3": ["任务清单", "项目发布", "数据分析", "工具配置", "网络服务", "文档笔记"],
    "P4": [],  # 其余未分类/低频
}


def load_token() -> str:
    token = os.environ.get("NOTION_TOKEN")
    if token:
        return token
    if SECRETS_PATH.exists():
        text = SECRETS_PATH.read_text(encoding="utf-8")
        m = re.search(r'export\s+NOTION_TOKEN=["\']([^"\']+)["\']', text)
        if m:
            return m.group(1)
    raise RuntimeError("找不到 NOTION_TOKEN。请设置环境变量或在 ~/.longhun/secrets.env 中配置。")


def init_db() -> sqlite3.Connection:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
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
    conn.execute("CREATE INDEX IF NOT EXISTS idx_cat ON pages(category)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_status ON pages(status)")
    conn.commit()
    return conn


def safe_filename(name: str, max_len: int = 80) -> str:
    name = name.strip().replace("/", "_").replace("\\", "_").replace("|", "_")
    name = "".join(c if unicodedata.category(c)[0] != "C" else "_" for c in name)
    if len(name) > max_len:
        name = name[:max_len]
    return name or "untitled"


ASSETS_DIR = OUT_DIR / "assets"


def api_get(token: str, url: str, params: Dict[str, Any] = None, retries: int = 3) -> requests.Response:
    """带 429 退避重试的 GET 请求。"""
    for attempt in range(retries):
        r = requests.get(
            url,
            headers={"Authorization": f"Bearer {token}", "Notion-Version": "2022-06-28"},
            params=params or {},
            timeout=60,
        )
        if r.status_code == 429:
            wait = 2 ** attempt + 0.5
            print(f"    ⏳ 触发 Notion 限流，等待 {wait:.1f}s 后重试…", flush=True)
            time.sleep(wait)
            continue
        return r
    return r


def download_asset(url: str, block_id: str) -> Optional[str]:
    """下载图片/文件到本地 assets 目录，返回相对 Markdown 路径。"""
    if not url:
        return None
    try:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        ct = r.headers.get("Content-Type", "").split(";")[0]
        ext_map = {
            "image/png": "png", "image/jpeg": "jpg", "image/gif": "gif",
            "image/webp": "webp", "image/svg+xml": "svg",
            "application/pdf": "pdf", "application/zip": "zip",
            "text/plain": "txt",
        }
        ext = ext_map.get(ct, "")
        if not ext:
            # try URL suffix
            suffix = pathlib.Path(url.split("?")[0]).suffix.lower()
            if suffix in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".pdf", ".zip", ".txt"):
                ext = suffix.lstrip(".")
            else:
                ext = "bin"
        ASSETS_DIR.mkdir(parents=True, exist_ok=True)
        local_path = ASSETS_DIR / f"{block_id}.{ext}"
        local_path.write_bytes(r.content)
        return f"assets/{local_path.name}"
    except Exception as e:
        print(f"    ⚠️ 资源下载失败 {url[:60]}: {e}", flush=True)
        return None


def rich_text_to_md(rich_text: List[Dict]) -> str:
    parts = []
    for rt in rich_text:
        if rt.get("type") != "text":
            # mention / equation fallback
            parts.append(rt.get("plain_text", ""))
            continue
        content = rt.get("text", {}).get("content", "")
        ann = rt.get("annotations", {})
        if ann.get("code"):
            content = f"`{content}`"
        if ann.get("bold"):
            content = f"**{content}**"
        if ann.get("italic"):
            content = f"*{content}*"
        if ann.get("strikethrough"):
            content = f"~~{content}~~"
        link = rt.get("text", {}).get("link")
        if link and link.get("url"):
            content = f"[{content}]({link['url']})"
        parts.append(content)
    return "".join(parts)


def fetch_table_rows(token: str, table_id: str) -> List[List[str]]:
    """拉取 table 的 table_row children，返回每行 cell 文本列表。"""
    rows: List[List[str]] = []
    base_url = f"https://api.notion.com/v1/blocks/{table_id}/children"
    params: Dict[str, Any] = {"page_size": 100}
    while True:
        r = api_get(token, base_url, params)
        if r.status_code != 200:
            break
        data = r.json()
        for b in data.get("results", []):
            if b.get("type") == "table_row":
                cells = [rich_text_to_md(cell) for cell in b.get("table_row", {}).get("cells", [])]
                rows.append(cells)
        if not data.get("has_more"):
            break
        params = {"page_size": 100, "start_cursor": data["next_cursor"]}
        time.sleep(0.12)
    return rows


class TooLargeError(RuntimeError):
    pass


def fetch_blocks(token: str, block_id: str, indent: str = "", depth: int = 0, max_blocks: int = 0) -> tuple[str, int]:
    """递归拉取 block children，返回 Markdown 文本和 block 数量。"""
    md_parts: List[str] = []
    count = 0
    if depth > 12:
        return "", 0
    base_url = f"https://api.notion.com/v1/blocks/{block_id}/children"
    params: Dict[str, Any] = {"page_size": 100}
    while True:
        r = api_get(token, base_url, params)
        if r.status_code != 200:
            raise RuntimeError(f"Notion API {r.status_code}: {r.text[:200]}")
        data = r.json()
        for b in data.get("results", []):
            count += 1
            if max_blocks and count > max_blocks:
                raise TooLargeError(f"block 数超过上限 {max_blocks}")
            if count % 100 == 0:
                print(f"    📦 已拉取 {count} blocks (depth={depth})...", flush=True)
            btype = b.get("type", "")
            body = b.get(btype) or {}
            text_md = ""
            if btype in ("paragraph", "heading_1", "heading_2", "heading_3",
                         "bulleted_list_item", "numbered_list_item", "to_do",
                         "quote", "callout"):
                text_md = rich_text_to_md(body.get("rich_text", []))

            if btype == "paragraph":
                if text_md.strip():
                    md_parts.append(f"{indent}{text_md}")
            elif btype == "heading_1":
                md_parts.append(f"{indent}# {text_md}")
            elif btype == "heading_2":
                md_parts.append(f"{indent}## {text_md}")
            elif btype == "heading_3":
                md_parts.append(f"{indent}### {text_md}")
            elif btype == "bulleted_list_item":
                md_parts.append(f"{indent}- {text_md}")
            elif btype == "numbered_list_item":
                md_parts.append(f"{indent}1. {text_md}")
            elif btype == "to_do":
                checked = "x" if body.get("checked") else " "
                md_parts.append(f"{indent}- [{checked}] {text_md}")
            elif btype == "quote":
                md_parts.append(f"{indent}> {text_md}")
            elif btype == "callout":
                icon_obj = body.get("icon") or {}
                icon = icon_obj.get("emoji", "💡")
                lines = text_md.splitlines() or [""]
                md_parts.append(f"{indent}> {icon} {lines[0]}")
                for line in lines[1:]:
                    md_parts.append(f"{indent}> {line}")
            elif btype == "code":
                lang = body.get("language", "")
                code = body.get("rich_text", [{}])[0].get("text", {}).get("content", "") if body.get("rich_text") else ""
                # Preserve multi-line code if rich_text has multiple segments
                code = rich_text_to_md(body.get("rich_text", []))
                md_parts.append(f"{indent}```{lang}\n{code}\n{indent}```")
            elif btype == "divider":
                md_parts.append(f"{indent}---")
            elif btype == "image":
                img_url = body.get("external", {}).get("url") or body.get("file", {}).get("url", "")
                caption = rich_text_to_md(body.get("caption", []))
                local = download_asset(img_url, b["id"])
                src = local if local else img_url
                md_parts.append(f"{indent}![{caption}]({src})")
            elif btype == "file":
                furl = body.get("external", {}).get("url") or body.get("file", {}).get("url", "")
                fname = body.get("name", "file")
                local = download_asset(furl, b["id"])
                src = local if local else furl
                md_parts.append(f"{indent}[📎 {fname}]({src})")
            elif btype == "bookmark":
                burl = body.get("url", "")
                md_parts.append(f"{indent}[🔗 书签]({burl})")
            elif btype == "link_to_page":
                pid = body.get("page_id", "")
                md_parts.append(f"{indent}[→ 关联页面](https://www.notion.so/{pid.replace('-', '')})")
            elif btype == "child_page":
                md_parts.append(f"{indent}> 📄 子页面：{b.get('child_page', {}).get('title', '')}")
            elif btype == "child_database":
                md_parts.append(f"{indent}> 🗃️ 子数据库：{b.get('child_database', {}).get('title', '')}")
            elif btype == "table":
                rows = fetch_table_rows(token, b["id"])
                count += len(rows)
                if rows:
                    # Markdown table: first row header, then separator
                    for i, cells in enumerate(rows):
                        md_parts.append(f"{indent}| {' | '.join(cells)} |")
                        if i == 0:
                            md_parts.append(f"{indent}|{'|'.join('---' for _ in cells)}|")
            elif btype == "table_row":
                # table rows are handled via fetch_table_rows
                cells = [rich_text_to_md(cell) for cell in body.get("cells", [])]
                md_parts.append(f"{indent}| {' | '.join(cells)} |")
            elif btype in ("column_list", "column", "synced_block"):
                # flatten children
                if b.get("has_children"):
                    try:
                        child_md, child_count = fetch_blocks(token, b["id"], indent, depth + 1, max_blocks)
                        count += child_count
                        md_parts.append(child_md)
                    except RuntimeError as e:
                        if "not supported" in str(e).lower():
                            md_parts.append(f"{indent}> ⚠️ 不支持通过 API 读取的块，已跳过")
                        else:
                            raise
            else:
                # Fallback: include plain_text if available
                plain = body.get("rich_text", [{}])[0].get("plain_text", "") if body.get("rich_text") else ""
                if plain:
                    md_parts.append(f"{indent}{plain}")

            # Recurse for non-table generic children
            if b.get("has_children") and btype not in ("table", "column_list", "column", "synced_block"):
                try:
                    child_md, child_count = fetch_blocks(token, b["id"], indent + "  ", depth + 1, max_blocks)
                    count += child_count
                    if child_md.strip():
                        md_parts.append(child_md)
                except RuntimeError as e:
                    if "not supported" in str(e).lower():
                        md_parts.append(f"{indent}> ⚠️ 子块不支持 API 读取，已跳过")
                    else:
                        raise

        if not data.get("has_more"):
            break
        params = {"page_size": 100, "start_cursor": data["next_cursor"]}
        time.sleep(0.12)
    return "\n\n".join(md_parts), count


def download_page(token: str, entry: Dict, conn: sqlite3.Connection, phase: str, force: bool = False, max_blocks: int = 0) -> None:
    page_id = entry["id"]
    cur = conn.execute("SELECT status FROM pages WHERE id=?", (page_id,))
    row = cur.fetchone()
    if row and row[0] == "done" and not force:
        return

    title = entry.get("title", "无标题")
    category = entry.get("category", "未分类")
    safe_title = safe_filename(title)
    cat_dir = OUT_DIR / safe_filename(category)
    cat_dir.mkdir(parents=True, exist_ok=True)
    md_path = cat_dir / f"{safe_title}_{page_id}.md"

    try:
        # Fetch page metadata (optional, for properties)
        page_resp = api_get(token, f"https://api.notion.com/v1/pages/{page_id}")
        if page_resp.status_code != 200:
            raise RuntimeError(f"page fetch {page_resp.status_code}: {page_resp.text[:200]}")
        time.sleep(0.12)

        try:
            md_body, block_count = fetch_blocks(token, page_id, max_blocks=max_blocks)
        except TooLargeError as e:
            conn.execute(
                """INSERT INTO pages(id,title,icon,category,subcategory,notion_url,created,modified,
                   local_md_path,status,error,word_count,block_count,phase)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                   ON CONFLICT(id) DO UPDATE SET
                   status='large', error=excluded.error, block_count=excluded.block_count, phase=excluded.phase""",
                (
                    page_id, title, entry.get("icon", ""), category,
                    entry.get("subcategory", ""), entry.get("notion_url", ""),
                    entry.get("created", ""), entry.get("modified", ""),
                    str(md_path), "large",
                    str(e), 0, 0, phase,
                ),
            )
            conn.commit()
            print(f"🟡 [{category}] {title[:40]} → LARGE (>{max_blocks} blocks) 延后", flush=True)
            return
        header = f"# {entry.get('icon', '')} {title}\n\n"
        header += f"- **Notion**: {entry.get('notion_url', '')}\n"
        header += f"- **分类**: {category} / {entry.get('subcategory', '')}\n"
        header += f"- **创建**: {entry.get('created', '')} · **修改**: {entry.get('modified', '')}\n"
        header += f"- **DNA**: #龍芯⚡️{datetime.now(CST).strftime('%Y-%m-%d')}-NOTION-PAGE-{page_id.split('-')[0].upper()}\n\n"
        header += "---\n\n"
        full_md = header + md_body
        md_path.write_text(full_md, encoding="utf-8")

        word_count = len(re.findall(r"\w+", full_md)) + len(re.findall(r"[\u4e00-\u9fff]", full_md))

        conn.execute(
            """INSERT INTO pages(id,title,icon,category,subcategory,notion_url,created,modified,
               local_md_path,status,error,word_count,block_count,downloaded_at,phase,dna)
               VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(id) DO UPDATE SET
               title=excluded.title, icon=excluded.icon, category=excluded.category,
               subcategory=excluded.subcategory, notion_url=excluded.notion_url,
               created=excluded.created, modified=excluded.modified,
               local_md_path=excluded.local_md_path, status=excluded.status,
               error=excluded.error, word_count=excluded.word_count,
               block_count=excluded.block_count, downloaded_at=excluded.downloaded_at,
               phase=excluded.phase, dna=excluded.dna""",
            (
                page_id, title, entry.get("icon", ""), category,
                entry.get("subcategory", ""), entry.get("notion_url", ""),
                entry.get("created", ""), entry.get("modified", ""),
                str(md_path), "done", "", word_count, block_count,
                datetime.now(CST).isoformat(), phase,
                f"#龍芯⚡️{datetime.now(CST).strftime('%Y-%m-%d')}-NOTION-PAGE-{page_id.split('-')[0].upper()}",
            ),
        )
        conn.commit()
        print(f"🟢 [{category}] {title[:40]} → {md_path.name} ({block_count} blocks, {word_count} words)", flush=True)
    except Exception as e:
        conn.execute(
            """INSERT INTO pages(id,title,icon,category,subcategory,notion_url,created,modified,
               local_md_path,status,error,phase)
               VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(id) DO UPDATE SET
               title=excluded.title, icon=excluded.icon, category=excluded.category,
               subcategory=excluded.subcategory, notion_url=excluded.notion_url,
               created=excluded.created, modified=excluded.modified,
               local_md_path=excluded.local_md_path, status='error', error=excluded.error,
               phase=excluded.phase""",
            (
                page_id, title, entry.get("icon", ""), category,
                entry.get("subcategory", ""), entry.get("notion_url", ""),
                entry.get("created", ""), entry.get("modified", ""),
                str(md_path), "error", str(e)[:500], phase,
            ),
        )
        conn.commit()
        print(f"🔴 [{category}] {title[:40]} → ERROR: {e}", flush=True)


def phase_for_entry(entry: Dict) -> str:
    cat = entry.get("category", "")
    for phase, cats in PHASES.items():
        if cat in cats:
            return phase
    return "P4"


def main() -> None:
    parser = argparse.ArgumentParser(description="龍魂 Notion 正文下载器")
    parser.add_argument("--phase", default="P0", help="下载阶段: P0/P1/P2/P3/P4/all")
    parser.add_argument("--limit", type=int, default=0, help="本阶段最多下载页数，0=不限")
    parser.add_argument("--force", action="store_true", help="强制重新下载已完成的页面")
    parser.add_argument("--dry-run", action="store_true", help="只统计，不下载")
    parser.add_argument("--max-blocks", type=int, default=0, help="单页 block 数上限，超过则标记为 large 跳过，0=不限")
    args = parser.parse_args()

    token = load_token()
    conn = init_db()

    data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    entries = data.get("entries", [])

    # 为每个 entry 分配 phase
    for e in entries:
        e["_phase"] = phase_for_entry(e)

    if args.phase == "all":
        selected = entries
    else:
        selected = [e for e in entries if e["_phase"] == args.phase]

    if not args.force:
        # 默认跳过已完成/失败/超大的页面，避免分块时重复处理
        pending_selected = []
        for e in selected:
            row = conn.execute("SELECT status FROM pages WHERE id=?", (e["id"],)).fetchone()
            if not row or row[0] == "pending":
                pending_selected.append(e)
        selected = pending_selected

    if args.limit:
        selected = selected[:args.limit]

    print(f"阶段 {args.phase}: 共 {len(selected)} 页待处理（索引总计 {len(entries)}）", flush=True)
    if args.dry_run:
        for e in selected[:20]:
            print(f"  - [{e['_phase']}] {e.get('category')} / {e.get('title')[:50]}", flush=True)
        return

    for i, e in enumerate(selected, 1):
        print(f"\n[{i}/{len(selected)}]", end=" ", flush=True)
        download_page(token, e, conn, e["_phase"], force=args.force, max_blocks=args.max_blocks)

    # 统计
    total = len(entries)
    done = conn.execute("SELECT COUNT(*) FROM pages WHERE status='done'").fetchone()[0]
    err = conn.execute("SELECT COUNT(*) FROM pages WHERE status='error'").fetchone()[0]
    large = conn.execute("SELECT COUNT(*) FROM pages WHERE status='large'").fetchone()[0]
    pending = total - done - err - large
    print("\n" + "=" * 60, flush=True)
    print(f"下载统计：总计 {total} | 完成 {done} | 失败 {err} | 超大 {large} | 未开始 {pending}", flush=True)
    print(f"数据库：{DB_PATH}", flush=True)
    print(f"文件目录：{OUT_DIR}", flush=True)

    # 缺失清单
    if err:
        print("\n失败页面清单（前 20）：", flush=True)
        for row in conn.execute("SELECT title,category,error FROM pages WHERE status='error' LIMIT 20"):
            print(f"  🔴 [{row[1]}] {row[0][:50]}: {row[2][:100]}", flush=True)
    if large:
        print("\n超大页面清单（延后处理）：", flush=True)
        for row in conn.execute("SELECT title,category,block_count FROM pages WHERE status='large' LIMIT 20"):
            print(f"  🟡 [{row[1]}] {row[0][:50]}: {row[2]} blocks", flush=True)


if __name__ == "__main__":
    main()
