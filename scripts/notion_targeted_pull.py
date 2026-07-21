#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════╗
║  龍魂系统 · Notion 精准拉取引擎 v1.0                          ║
║  指定页面/数据库 → 递归下载所有子页面 → 训练语料                ║
║  DNA: #龍芯⚡️丙午·辛未·乙酉·午时·姤-TARGETED-PULL-v1.0       ║
║  UID: 9622                                                   ║
╚═══════════════════════════════════════════════════════════════╝

用法:
  python3 scripts/notion_targeted_pull.py --url "https://www.notion.so/uid9622/xxx"
  python3 scripts/notion_targeted_pull.py --all          # 拉取硬编码的4个目标
  python3 scripts/notion_targeted_pull.py --url "xxx" --to-corpus  # 直接转训练语料
"""

import os
import re
import sys
import json
import time
import sqlite3
import pathlib
import argparse
import unicodedata
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Set, Tuple

import requests

# ══════════════════════════════════════════════════════════════
# 常量
# ══════════════════════════════════════════════════════════════

DNA_SIGNATURE = "#龍芯⚡️丙午·辛未·乙酉·午时·姤-TARGETED-PULL-v1.0"
CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
CST = timezone(timedelta(hours=8))

HOME = pathlib.Path.home()
PROJECT_ROOT = HOME / "longhun-system"
NOTION_BASE = HOME / ".longhun" / "notion_pages"
NOTION_BASE.mkdir(parents=True, exist_ok=True)

DB_PATH = NOTION_BASE / "notion_pages.db"
ASSETS_DIR = NOTION_BASE / "assets"
TARGET_DIR = NOTION_BASE / "targeted_pull"  # 本次拉取的输出目录

SECRETS_PATH = HOME / ".longhun" / "secrets.env"
CHECKPOINT_FILE = NOTION_BASE / ".targeted_pull_checkpoint.json"
TRAIN_CORPUS = PROJECT_ROOT / "models" / "longhun-v1.0" / "notion_targeted_corpus.md"

MAX_BLOCKS_PER_PAGE = 800
API_DELAY = 0.15  # Notion API 节流
DEPTH_LIMIT = 8    # 递归深度限制

# 硬编码的4个目标URL
TARGET_URLS = [
    "https://www.notion.so/uid9622/baf3b574023e49c987eee620a811e70d?v=76806f3368ad4fbfbac11cb2847dce8d&source=copy_link",
    "https://www.notion.so/uid9622/3367125a9c9f808a9692f0c6752e92fa?v=3367125a9c9f80349364000cc2a0eb8c&source=copy_link",
    "https://www.notion.so/uid9622/f545874667f4438e8bc76d7a76182b9e?source=copy_link",
    "https://www.notion.so/uid9622/v3-0-3debae713c554137abafdc3dc3874cc6?source=copy_link",
]

# ══════════════════════════════════════════════════════════════
# 工具函数
# ══════════════════════════════════════════════════════════════

def load_token() -> str:
    """加载 Notion API Token"""
    token = os.environ.get("NOTION_TOKEN")
    if token:
        return token
    if SECRETS_PATH.exists():
        text = SECRETS_PATH.read_text(encoding="utf-8")
        m = re.search(r'export\s+NOTION_TOKEN=["\']([^"\']+)["\']', text)
        if m:
            return m.group(1)
    raise RuntimeError("找不到 NOTION_TOKEN")


def extract_id_from_url(url: str) -> str:
    """从 Notion URL 提取页面/数据库ID（32位hex）"""
    # 匹配 32 位 hex
    m = re.search(r'([a-f0-9]{32})', url)
    if not m:
        raise ValueError(f"无法从URL提取ID: {url}")
    return m.group(1)


def format_notion_id(raw_id: str) -> str:
    """将 32 位 hex 格式化为 Notion UUID: 8-4-4-4-12"""
    h = raw_id.replace("-", "")
    return f"{h[0:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"


def safe_filename(name: str, max_len: int = 80) -> str:
    name = name.strip().replace("/", "_").replace("\\", "_").replace("|", "_")
    name = "".join(c if unicodedata.category(c)[0] != "C" else "_" for c in name)
    if len(name) > max_len:
        name = name[:max_len]
    return name or "untitled"


def now_iso() -> str:
    return datetime.now(CST).isoformat()


def api_get(token: str, url: str, params: Optional[Dict[str, Any]] = None, retries: int = 3) -> requests.Response:
    for attempt in range(retries):
        r = requests.get(
            url,
            headers={"Authorization": f"Bearer {token}", "Notion-Version": "2022-06-28"},
            params=params or {},
            timeout=60,
        )
        if r.status_code == 429:
            wait = 2 ** attempt + 0.5
            print(f"    ⏳ 限流，等待 {wait:.1f}s...", flush=True)
            time.sleep(wait)
            continue
        return r
    return r


def api_post(token: str, url: str, body: Optional[Dict[str, Any]] = None, retries: int = 3) -> requests.Response:
    for attempt in range(retries):
        r = requests.post(
            url,
            headers={"Authorization": f"Bearer {token}", "Notion-Version": "2022-06-28", "Content-Type": "application/json"},
            json=body or {},
            timeout=60,
        )
        if r.status_code == 429:
            wait = 2 ** attempt + 0.5
            print(f"    ⏳ 限流，等待 {wait:.1f}s...", flush=True)
            time.sleep(wait)
            continue
        return r
    return r


def rich_text_to_md(rich_text: List[Dict[str, Any]]) -> str:
    parts = []
    for rt in rich_text:
        if rt.get("type") != "text":
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


# ══════════════════════════════════════════════════════════════
# 存储层
# ══════════════════════════════════════════════════════════════

def init_db() -> sqlite3.Connection:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS targeted_pages (
            id TEXT PRIMARY KEY,
            title TEXT,
            icon TEXT,
            notion_url TEXT,
            source_url TEXT,
            page_type TEXT,
            local_md_path TEXT,
            status TEXT DEFAULT 'pending',
            error TEXT,
            word_count INTEGER DEFAULT 0,
            block_count INTEGER DEFAULT 0,
            downloaded_at TEXT,
            dna TEXT
        )
    """)
    conn.commit()
    return conn


def save_page_md(page_id: str, title: str, icon: str, notion_url: str, source_url: str,
                 md_content: str, block_count: int, conn: sqlite3.Connection) -> pathlib.Path:
    """保存页面 Markdown 到本地，更新数据库"""
    safe_title = safe_filename(title)
    md_path = TARGET_DIR / f"{safe_title}_{page_id.replace('-', '')[:8]}.md"
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    header = f"# {icon} {title}\n\n"
    header += f"- **Notion**: {notion_url}\n"
    header += f"- **来源**: {source_url}\n"
    header += f"- **下载时间**: {now_iso()}\n"
    header += f"- **DNA**: #龍芯⚡️{datetime.now(CST).strftime('%Y-%m-%d')}-PULL-{page_id.split('-')[0].upper()}\n\n"
    header += "---\n\n"

    md_path.write_text(header + md_content, encoding="utf-8")

    word_count = len(re.findall(r"\w+", md_content)) + len(re.findall(r"[\u4e00-\u9fff]", md_content))

    conn.execute("""
        INSERT INTO targeted_pages(id, title, icon, notion_url, source_url, page_type,
            local_md_path, status, word_count, block_count, downloaded_at, dna)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(id) DO UPDATE SET
            title=excluded.title, icon=excluded.icon, notion_url=excluded.notion_url,
            source_url=excluded.source_url, local_md_path=excluded.local_md_path,
            status='done', word_count=excluded.word_count, block_count=excluded.block_count,
            downloaded_at=excluded.downloaded_at, dna=excluded.dna
    """, (
        page_id, title, icon, notion_url, source_url, "page",
        str(md_path), "done", word_count, block_count,
        now_iso(),
        f"#龍芯⚡️{datetime.now(CST).strftime('%Y-%m-%d')}-PULL-{page_id.split('-')[0].upper()}",
    ))
    conn.commit()
    return md_path


def save_checkpoint(data: Dict[str, Any]) -> None:
    CHECKPOINT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_checkpoint() -> Optional[Dict[str, Any]]:
    if CHECKPOINT_FILE.exists():
        return json.loads(CHECKPOINT_FILE.read_text(encoding="utf-8"))
    return None


# ══════════════════════════════════════════════════════════════
# 块拉取引擎（递归）
# ══════════════════════════════════════════════════════════════

class BlockTooLarge(RuntimeError):
    pass


def fetch_blocks(token: str, block_id: str, depth: int = 0, max_blocks: int = 0) -> Tuple[str, int, List[str], List[str]]:
    """
    递归拉取 block children。
    返回: (markdown_text, block_count, child_page_ids, child_db_ids)
    """
    md_parts: List[str] = []
    child_pages: List[str] = []
    child_dbs: List[str] = []
    count = 0

    if depth > DEPTH_LIMIT:
        return "", 0, [], []

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
                raise BlockTooLarge(f"超过上限 {max_blocks} blocks")

            if count % 100 == 0:
                print(f"    📦 {count} blocks (depth={depth})...", flush=True)

            btype = b.get("type", "")
            body = b.get(btype) or {}
            text_md = ""

            # 文本类块
            if btype in ("paragraph", "heading_1", "heading_2", "heading_3",
                         "bulleted_list_item", "numbered_list_item", "to_do", "quote", "callout"):
                text_md = rich_text_to_md(body.get("rich_text", []))

            if btype == "paragraph":
                if text_md.strip():
                    md_parts.append(f"{text_md}")
            elif btype == "heading_1":
                md_parts.append(f"# {text_md}")
            elif btype == "heading_2":
                md_parts.append(f"## {text_md}")
            elif btype == "heading_3":
                md_parts.append(f"### {text_md}")
            elif btype == "bulleted_list_item":
                md_parts.append(f"- {text_md}")
            elif btype == "numbered_list_item":
                md_parts.append(f"1. {text_md}")
            elif btype == "to_do":
                checked = "x" if body.get("checked") else " "
                md_parts.append(f"- [{checked}] {text_md}")
            elif btype == "quote":
                md_parts.append(f"> {text_md}")
            elif btype == "callout":
                icon = (body.get("icon") or {}).get("emoji", "💡")
                md_parts.append(f"> {icon} {text_md}")
            elif btype == "code":
                lang = body.get("language", "")
                code = rich_text_to_md(body.get("rich_text", []))
                md_parts.append(f"```{lang}\n{code}\n```")
            elif btype == "divider":
                md_parts.append("---")
            elif btype == "image":
                img_url = body.get("external", {}).get("url") or body.get("file", {}).get("url", "")
                caption = rich_text_to_md(body.get("caption", []))
                md_parts.append(f"![{caption}]({img_url})")
            elif btype == "file":
                furl = body.get("external", {}).get("url") or body.get("file", {}).get("url", "")
                fname = body.get("name", "file")
                md_parts.append(f"[📎 {fname}]({furl})")
            elif btype == "bookmark":
                md_parts.append(f"[🔗 书签]({body.get('url', '')})")
            elif btype == "link_to_page":
                pid = body.get("page_id", "")
                md_parts.append(f"[→ 关联页面](https://www.notion.so/{pid.replace('-', '')})")
            elif btype == "child_page":
                child_title = b.get("child_page", {}).get("title", "子页面")
                md_parts.append(f"\n> 📄 **子页面: {child_title}**\n")
                child_pages.append(b["id"])
            elif btype == "child_database":
                child_title = b.get("child_database", {}).get("title", "子数据库")
                md_parts.append(f"\n> 🗃️ **子数据库: {child_title}**\n")
                child_dbs.append(b["id"])
            elif btype == "table":
                rows = _fetch_table_rows(token, b["id"])
                if rows:
                    for i, cells in enumerate(rows):
                        md_parts.append(f"| {' | '.join(cells)} |")
                        if i == 0:
                            md_parts.append(f"|{'|'.join('---' for _ in cells)}|")
            elif btype in ("column_list", "column", "synced_block", "toggle"):
                if b.get("has_children"):
                    try:
                        child_md, child_cnt, cp, cd = fetch_blocks(token, b["id"], depth + 1, max_blocks)
                        count += child_cnt
                        child_pages.extend(cp)
                        child_dbs.extend(cd)
                        if child_md.strip():
                            md_parts.append(child_md)
                    except (RuntimeError, BlockTooLarge):
                        pass
            else:
                plain = (body.get("rich_text") or [{}])[0].get("plain_text", "")
                if plain:
                    md_parts.append(plain)

            # 递归子块
            if b.get("has_children") and btype not in ("table", "column_list", "column", "synced_block", "toggle"):
                try:
                    child_md, child_cnt, cp, cd = fetch_blocks(token, b["id"], depth + 1, max_blocks)
                    count += child_cnt
                    child_pages.extend(cp)
                    child_dbs.extend(cd)
                    if child_md.strip():
                        md_parts.append(child_md)
                except (RuntimeError, BlockTooLarge) as e:
                    md_parts.append(f"> ⚠️ 子块跳过: {e}")

        if not data.get("has_more"):
            break
        params = {"page_size": 100, "start_cursor": data["next_cursor"]}
        time.sleep(API_DELAY)

    return "\n\n".join(md_parts), count, child_pages, child_dbs


def _fetch_table_rows(token: str, table_id: str) -> List[List[str]]:
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
        time.sleep(API_DELAY)
    return rows


# ══════════════════════════════════════════════════════════════
# 数据库拉取
# ══════════════════════════════════════════════════════════════

def query_database(token: str, database_id: str) -> List[Dict[str, Any]]:
    """查询数据库，返回所有页面条目（带进度输出）"""
    pages = []
    body: Dict[str, Any] = {"page_size": 100}
    page_num = 0

    while True:
        r = api_post(token, f"https://api.notion.com/v1/databases/{database_id}/query", body)
        if page_num == 0:
            print(f"    📡 首次查询: status={r.status_code}", flush=True)
        if r.status_code != 200:
            print(f"  ⚠️ 数据库查询失败 {r.status_code}: {r.text[:200]}", flush=True)
            break
        data = r.json()
        results = data.get("results", [])
        for p in results:
            page_num += 1
            props = p.get("properties", {})
            title_prop = _extract_title(props)
            pages.append({
                "id": p["id"],
                "title": title_prop,
                "icon": (p.get("icon") or {}).get("emoji", ""),
                "url": p.get("url", ""),
            })
            if page_num % 20 == 0 or page_num == 1:
                print(f"    📋 已列举 {page_num} 条...", flush=True)

        if not data.get("has_more"):
            break
        body["start_cursor"] = data["next_cursor"]
        time.sleep(API_DELAY)

    return pages


def _extract_title(props: Dict[str, Any]) -> str:
    """从 properties 中提取标题"""
    for key, val in props.items():
        if val.get("type") == "title":
            texts = val.get("title", [])
            return rich_text_to_md(texts) if texts else "无标题"
    # Fallback: 尝试其他文本类型
    for key, val in props.items():
        if val.get("type") in ("rich_text", "text"):
            texts = val.get("rich_text") or val.get("text") or []
            return rich_text_to_md(texts) if texts else "无标题"
    return "无标题"


# ══════════════════════════════════════════════════════════════
# 页面类型检测
# ══════════════════════════════════════════════════════════════

def detect_type(token: str, notion_id: str, raw_url: str = "") -> Tuple[str, Dict[str, Any]]:
    """
    检测 Notion 对象类型：page 或 database。
    优化: 如果URL包含 ?v= 优先尝试数据库（避免无效的page请求）。
    返回 (type, metadata_dict)
    """
    # 如果URL含 ?v= 参数，99%是数据库视图，直接查数据库
    if "?v=" in raw_url:
        print(f"   🔍 DB探测中...", flush=True)
        try:
            r = api_get(token, f"https://api.notion.com/v1/databases/{notion_id}")
        except Exception as e:
            print(f"   ❌ DB API异常: {e}", flush=True)
            raise
        print(f"   📡 DB响应: {r.status_code}", flush=True)
        if r.status_code == 200:
            data = r.json()
            title_list = data.get("title", [])
            title = rich_text_to_md(title_list) if title_list else "数据库"
            print(f"   类型: database (从?v=判定)", flush=True)
            return "database", {
                "title": title,
                "icon": (data.get("icon") or {}).get("emoji", "🗃️"),
                "url": f"https://www.notion.so/{notion_id.replace('-', '')}",
                "id": data["id"],
            }

    # 先尝试作为 page
    r = api_get(token, f"https://api.notion.com/v1/pages/{notion_id}")
    if r.status_code == 200:
        data = r.json()
        title_prop = _extract_title(data.get("properties", {}))
        return "page", {
            "title": title_prop,
            "icon": (data.get("icon") or {}).get("emoji", ""),
            "url": data.get("url", ""),
            "id": data["id"],
        }

    # 尝试作为 database
    r = api_get(token, f"https://api.notion.com/v1/databases/{notion_id}")
    if r.status_code == 200:
        data = r.json()
        title_list = data.get("title", [])
        title = rich_text_to_md(title_list) if title_list else "数据库"
        return "database", {
            "title": title,
            "icon": (data.get("icon") or {}).get("emoji", "🗃️"),
            "url": f"https://www.notion.so/{notion_id.replace('-', '')}",
            "id": data["id"],
        }

    raise RuntimeError(f"无法识别对象类型: {r.status_code}")


# ══════════════════════════════════════════════════════════════
# 递归下载引擎
# ══════════════════════════════════════════════════════════════

def download_page_recursive(token: str, page_id: str, title: str, icon: str,
                            notion_url: str, source_url: str, conn: sqlite3.Connection,
                            visited: Set[str], all_md_contents: List[str]) -> Tuple[int, int]:
    """
    递归下载页面及其所有子页面、子数据库。
    返回 (total_pages, total_blocks)
    """
    if page_id in visited:
        return 0, 0
    visited.add(page_id)

    print(f"\n  📄 页面: {title[:60]} ({page_id[:8]}...)", flush=True)

    try:
        md_body, block_count, child_pages, child_dbs = fetch_blocks(
            token, page_id, max_blocks=MAX_BLOCKS_PER_PAGE
        )
    except BlockTooLarge:
        print(f"    🟡 页面过大(>{MAX_BLOCKS_PER_PAGE} blocks)，仅下载前{MAX_BLOCKS_PER_PAGE}块", flush=True)
        try:
            md_body, block_count, child_pages, child_dbs = fetch_blocks(
                token, page_id, max_blocks=MAX_BLOCKS_PER_PAGE
            )
        except BlockTooLarge:
            print(f"    🔴 跳过", flush=True)
            return 0, 0

    md_path = save_page_md(page_id, title, icon, notion_url, source_url, md_body, block_count, conn)
    all_md_contents.append(f"\n\n<!-- PAGE: {title} -->\n\n{md_body}")
    print(f"    ✅ {block_count} blocks · {md_path.name}", flush=True)
    total_pages = 1
    total_blocks = block_count
    time.sleep(API_DELAY)

    # 递归处理子页面
    for child_id in child_pages:
        try:
            r = api_get(token, f"https://api.notion.com/v1/pages/{child_id}")
            if r.status_code == 200:
                child_data = r.json()
                child_title = _extract_title(child_data.get("properties", {}))
                child_url = child_data.get("url", "")
                p, b = download_page_recursive(
                    token, child_id, child_title, "📄", child_url, source_url,
                    conn, visited, all_md_contents,
                )
                total_pages += p
                total_blocks += b
            time.sleep(API_DELAY)
        except Exception as e:
            print(f"    ⚠️ 子页面 {child_id[:8]} 跳过: {e}", flush=True)

    # 递归处理子数据库
    for db_id in child_dbs:
        try:
            p, b = download_database_recursive(token, db_id, source_url, conn, visited, all_md_contents)
            total_pages += p
            total_blocks += b
        except Exception as e:
            print(f"    ⚠️ 子数据库 {db_id[:8]} 跳过: {e}", flush=True)

    return total_pages, total_blocks


def download_database_recursive(token: str, database_id: str, source_url: str,
                                 conn: sqlite3.Connection, visited: Set[str],
                                 all_md_contents: List[str]) -> Tuple[int, int]:
    """
    下载数据库的所有条目，每个条目作为页面递归下载。
    返回 (total_pages, total_blocks)
    """
    print(f"\n  🗃️ 数据库: {database_id[:8]}...", flush=True)

    entries = query_database(token, database_id)
    print(f"    📊 {len(entries)} 个条目", flush=True)

    total_pages = 0
    total_blocks = 0

    for i, entry in enumerate(entries):
        if entry["id"] in visited:
            continue
        print(f"  [{i+1}/{len(entries)}]", end="", flush=True)
        p, b = download_page_recursive(
            token, entry["id"], entry["title"], entry["icon"],
            entry["url"] or f"https://www.notion.so/{entry['id'].replace('-', '')}",
            source_url, conn, visited, all_md_contents,
        )
        total_pages += p
        total_blocks += b
        time.sleep(API_DELAY)

        # 定时保存检查点
        save_checkpoint({
            "visited": list(visited),
            "last_db_id": database_id,
            "last_entry_idx": i,
            "total_pages_so_far": total_pages,
            "total_blocks_so_far": total_blocks,
        })

    return total_pages, total_blocks


def process_url(token: str, url: str, conn: sqlite3.Connection,
                visited: Set[str], all_md_contents: List[str]) -> Tuple[int, int]:
    """处理单个 Notion URL"""
    raw_id = extract_id_from_url(url)
    notion_id = format_notion_id(raw_id)
    print(f"\n{'═'*60}")
    print(f"🎯 目标: {url[:80]}...")
    print(f"   ID: {notion_id}", flush=True)

    obj_type, meta = detect_type(token, notion_id, raw_url=url)
    print(f"   标题: {meta['title'][:60]}", flush=True)

    if obj_type == "page":
        return download_page_recursive(
            token, notion_id, meta["title"], meta["icon"],
            meta["url"], url, conn, visited, all_md_contents,
        )
    else:  # database
        return download_database_recursive(
            token, notion_id, url, conn, visited, all_md_contents,
        )


# ══════════════════════════════════════════════════════════════
# 训练语料生成
# ══════════════════════════════════════════════════════════════

def generate_training_corpus(all_md_contents: List[str]) -> pathlib.Path:
    """将所有拉取的 Markdown 合并为训练语料"""
    if not all_md_contents:
        print("⚠️ 无内容可生成训练语料")
        return TRAIN_CORPUS

    TRAIN_CORPUS.parent.mkdir(parents=True, exist_ok=True)

    header = f"""# 龍魂系统 · Notion 精准拉取训练语料

> 生成时间: {now_iso()}
> DNA: {DNA_SIGNATURE}
> 目标数量: {len(TARGET_URLS)}
> 确认: {CONFIRM_SEAL}

---

"""
    full_corpus = header + "\n\n---\n\n".join(all_md_contents)
    TRAIN_CORPUS.write_text(full_corpus, encoding="utf-8")

    size_kb = TRAIN_CORPUS.stat().st_size / 1024
    words = len(re.findall(r"\w+", full_corpus)) + len(re.findall(r"[\u4e00-\u9fff]", full_corpus))
    print(f"\n📚 训练语料: {TRAIN_CORPUS} ({size_kb:.1f} KB · {words} 词/字)", flush=True)
    return TRAIN_CORPUS


# ══════════════════════════════════════════════════════════════
# 主入口
# ══════════════════════════════════════════════════════════════

def main() -> int:
    parser = argparse.ArgumentParser(description="龍魂 Notion 精准拉取引擎")
    parser.add_argument("--url", type=str, action="append", help="Notion 页面/数据库 URL（可重复）")
    parser.add_argument("--all", action="store_true", help="拉取硬编码的4个目标URL")
    parser.add_argument("--to-corpus", action="store_true", help="拉取后生成训练语料")
    parser.add_argument("--resume", action="store_true", help="从检查点恢复")
    args = parser.parse_args()

    urls = []
    if args.all:
        urls = TARGET_URLS
    elif args.url:
        urls = args.url
    else:
        parser.print_help()
        return 1

    if not urls:
        print("❌ 未指定目标URL")
        return 1

    print("🐉 龍魂 Notion 精准拉取引擎 v1.0")
    print(f"DNA: {DNA_SIGNATURE}")
    print(f"目标: {len(urls)} 个URL")
    print(f"输出: {TARGET_DIR}")
    print()

    token = load_token()
    conn = init_db()

    visited: Set[str] = set()
    all_md_contents: List[str] = []

    # 从检查点恢复
    if args.resume:
        cp = load_checkpoint()
        if cp:
            visited = set(cp.get("visited", []))
            print(f"📋 从检查点恢复: {len(visited)} 个已访问页面")

    total_pages = 0
    total_blocks = 0

    for url in urls:
        try:
            p, b = process_url(token, url, conn, visited, all_md_contents)
            total_pages += p
            total_blocks += b
            save_checkpoint({
                "visited": list(visited),
                "completed_urls": len([u for u in urls if u != url]),
                "total_pages": total_pages,
                "total_blocks": total_blocks,
            })
        except Exception as e:
            print(f"\n❌ URL处理失败: {url[:80]}...")
            print(f"   错误: {e}")
            import traceback
            traceback.print_exc()

    # 统计
    print(f"\n{'═'*60}")
    print(f"📊 拉取完成统计:")
    print(f"   页面总数: {total_pages}")
    print(f"   块总数: {total_blocks}")
    print(f"   输出目录: {TARGET_DIR}")
    print(f"   唯一页面: {len(visited)}")

    done_count = conn.execute("SELECT COUNT(*) FROM targeted_pages WHERE status='done'").fetchone()[0]
    print(f"   成功入库: {done_count}")

    # 生成训练语料
    if args.to_corpus or args.all:
        corpus_path = generate_training_corpus(all_md_contents)
        print(f"   训练语料: {corpus_path}")

    # 清理检查点
    if CHECKPOINT_FILE.exists():
        print(f"\n📋 检查点已保存: {CHECKPOINT_FILE}")
        print(f"   下次可运行 --resume 继续")

    print(f"\n✅ 拉取完成 · DNA: {DNA_SIGNATURE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
