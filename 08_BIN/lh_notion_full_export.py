#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·#龍芯⚡️丙午·丙申·POSTAUDIT-LH_NOTION_FULL_EXPOR-53916C88
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍芯⚡️丙午·丙申·辛酉·未时·☰乾-NOTION-FULL-EXPORT-v1.0
"""
🐉 龍魂 · Notion 工作区全量导出引擎 v1.0

功能:
  1. 用 Notion Search API 遍历所有页面和数据库
  2. 递归抓取页面块（block children）
  3. 将块内容转换为 Markdown
  4. 保存到 docs/notion_full_export/

用法:
  .venv/bin/python3 08_BIN/lh_notion_full_export.py
  .venv/bin/python3 08_BIN/lh_notion_full_export.py --output /path/to/export
"""

import argparse
import json
import os
import re
import time
from pathlib import Path
from datetime import datetime

import requests


NOTION_VERSION = "2022-06-28"
API_BASE = "https://api.notion.com/v1"


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _test_token(token: str) -> bool:
    try:
        r = requests.post(
            f"{API_BASE}/search",
            headers=headers(token),
            json={"page_size": 1},
            timeout=10,
        )
        return r.status_code == 200
    except Exception:
        return False


def get_token() -> str:
    """获取有效 NOTION_TOKEN：环境变量、config 文件都试，选能用的。"""
    candidates = []
    if os.environ.get("NOTION_TOKEN"):
        candidates.append(("环境变量", os.environ["NOTION_TOKEN"]))
    cfg_path = Path(__file__).resolve().parent.parent / "config" / "notion_config.json"
    if cfg_path.exists():
        data = json.load(open(cfg_path, encoding="utf-8"))
        token = data.get("notion_token") or data.get("token")
        if token:
            candidates.append(("config/notion_config.json", token))
    # 尝试 ~/.env
    env_path = Path.home() / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("NOTION_TOKEN="):
                token = line.split("=", 1)[1].strip()
                candidates.append(("~/.env", token))
                break

    for source, token in candidates:
        print(f"[{_now()}]   测试 token 来源: {source}")
        if _test_token(token):
            print(f"[{_now()}]   ✅ 使用 {source} 的 token")
            return token
        else:
            print(f"[{_now()}]   ⚠️ {source} 的 token 无效")

    raise RuntimeError("❌ 找不到有效的 NOTION_TOKEN。请检查环境变量、~/.env 或 config/notion_config.json")


def headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def _request_with_retry(method: str, url: str, token: str, **kwargs) -> requests.Response:
    """带指数退避重试的请求包装。"""
    for attempt in range(5):
        try:
            r = requests.request(method, url, headers=headers(token), timeout=30, **kwargs)
            if r.status_code in (429, 502, 503, 504):
                wait = 2 ** attempt
                print(f"[{_now()}]   ⏳ HTTP {r.status_code}，退避 {wait}s 后重试...")
                time.sleep(wait)
                continue
            return r
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            wait = 2 ** attempt
            print(f"[{_now()}]   ⏳ 网络错误: {type(e).__name__}，{wait}s 后重试 ({attempt+1}/5)")
            time.sleep(wait)
    raise RuntimeError(f"❌ 请求失败（重试耗尽）: {url}")


def search_all(token: str, query: str = "") -> list:
    """Notion Search API 分页获取所有对象。"""
    results = []
    next_cursor = None
    page_count = 0
    while True:
        payload = {"page_size": 100}
        if query:
            payload["query"] = query
        if next_cursor:
            payload["start_cursor"] = next_cursor
        r = _request_with_retry("POST", f"{API_BASE}/search", token, json=payload)
        r.raise_for_status()
        data = r.json()
        batch = data.get("results", [])
        results.extend(batch)
        page_count += 1
        print(f"[{_now()}]   search page {page_count}: +{len(batch)} items, total {len(results)}")
        if not data.get("has_more"):
            break
        next_cursor = data.get("next_cursor")
        time.sleep(0.2)
    return results


def query_database(token: str, db_id: str) -> list:
    """查询数据库所有条目。"""
    results = []
    next_cursor = None
    while True:
        payload = {"page_size": 100}
        if next_cursor:
            payload["start_cursor"] = next_cursor
        r = _request_with_retry(
            "POST",
            f"{API_BASE}/databases/{db_id}/query",
            token,
            json=payload,
        )
        if r.status_code == 404:
            print(f"[{_now()}]   ⚠️ 数据库 {db_id} 不存在或不可访问")
            break
        r.raise_for_status()
        data = r.json()
        batch = data.get("results", [])
        results.extend(batch)
        if not data.get("has_more"):
            break
        next_cursor = data.get("next_cursor")
        time.sleep(0.2)
    return results


def fetch_block_children(token: str, block_id: str) -> list:
    """获取块的直接子块。"""
    results = []
    next_cursor = None
    while True:
        url = f"{API_BASE}/blocks/{block_id}/children"
        params = {"page_size": 100}
        if next_cursor:
            params["start_cursor"] = next_cursor
        r = _request_with_retry("GET", url, token, params=params)
        if r.status_code in (404, 400):
            break
        r.raise_for_status()
        data = r.json()
        batch = data.get("results", [])
        results.extend(batch)
        if not data.get("has_more"):
            break
        next_cursor = data.get("next_cursor")
        time.sleep(0.1)
    return results


def rich_text_to_markdown(rich_texts: list) -> str:
    """将 rich_text 数组转为 Markdown 字符串。"""
    out = ""
    for rt in rich_texts:
        text = rt.get("text", {}).get("content", "")
        annotations = rt.get("annotations", {})
        if annotations.get("bold"):
            text = f"**{text}**"
        if annotations.get("italic"):
            text = f"*{text}*"
        if annotations.get("code"):
            text = f"`{text}`"
        if annotations.get("strikethrough"):
            text = f"~~{text}~~"
        href = rt.get("href")
        if href:
            text = f"[{text}]({href})"
        out += text
    return out


def block_to_markdown(block: dict, indent: int = 0) -> str:
    """单块转 Markdown（递归处理子块）。"""
    t = block.get("type", "")
    val = block.get(t) or {}
    prefix = "  " * indent
    md = ""

    if t in ("paragraph",):
        text = rich_text_to_markdown(val.get("rich_text", []))
        if text.strip():
            md += f"{prefix}{text}\n\n"
    elif t.startswith("heading_"):
        level = int(t.split("_")[-1])
        text = rich_text_to_markdown(val.get("rich_text", []))
        md += f"{prefix}{ '#' * level } {text}\n\n"
    elif t == "bulleted_list_item":
        text = rich_text_to_markdown(val.get("rich_text", []))
        md += f"{prefix}- {text}\n"
    elif t == "numbered_list_item":
        text = rich_text_to_markdown(val.get("rich_text", []))
        md += f"{prefix}1. {text}\n"
    elif t == "to_do":
        text = rich_text_to_markdown(val.get("rich_text", []))
        checked = "x" if val.get("checked") else " "
        md += f"{prefix}- [{checked}] {text}\n"
    elif t == "quote":
        text = rich_text_to_markdown(val.get("rich_text", []))
        md += f"{prefix}> {text}\n\n"
    elif t == "code":
        text = rich_text_to_markdown(val.get("rich_text", []))
        lang = val.get("language", "")
        md += f"{prefix}```{lang}\n{text}\n```\n\n"
    elif t == "callout":
        text = rich_text_to_markdown(val.get("rich_text", []))
        icon = val.get("icon", {}).get("emoji", "💡")
        md += f"{prefix}> {icon} {text}\n\n"
    elif t == "divider":
        md += f"{prefix}---\n\n"
    elif t == "image":
        caption = rich_text_to_markdown(val.get("caption", []))
        url = val.get("external", {}).get("url") or val.get("file", {}).get("url", "")
        md += f"{prefix}![{caption}]({url})\n\n"
    elif t == "table":
        md += f"{prefix}[表格]\n\n"
    else:
        # 其他块类型简单占位
        text = rich_text_to_markdown(val.get("rich_text", []))
        if text:
            md += f"{prefix}{text}\n\n"

    return md


def fetch_page_markdown(token: str, page_id: str) -> str:
    """递归抓取页面所有块并转 Markdown。"""
    md = ""
    blocks = fetch_block_children(token, page_id)
    for b in blocks:
        md += block_to_markdown(b)
        # 递归处理有子块的块
        if b.get("has_children"):
            child_md = fetch_page_markdown(token, b["id"])
            # 给子块加缩进
            indented = "\n".join("  " + line if line.strip() else line for line in child_md.splitlines())
            md += indented + "\n"
    return md


def safe_filename(name: str) -> str:
    """生成安全的文件名。"""
    name = name.replace("/", "_").replace("\\", "_").replace(":", "_")
    name = re.sub(r"\s+", "_", name)
    name = name.strip("._")
    return name[:80] or "untitled"


RELEVANT_KEYWORDS = [
    "龍魂", "龙魂", "LongHun", "longhun", "LONGHUN", "龍",
    "CNSH", "cnsh", "UID9622", "三才", "DNA", "铁律", "宪法",
    "道德经", "通心译", "Tongxin", "tongxin", "君子", "审计",
    "主权", "民生", "认知", "知识图谱", "记忆", "bootstrap",
    "徽章", "license", "协议", "治理", "鲲鹏", "龙芯",
]


def get_page_title(page: dict) -> str:
    """安全获取页面标题。"""
    props = page.get("properties", {})
    title = ""
    if "title" in props:
        title = "".join(t.get("plain_text", "") for t in props["title"].get("title", []))
    if not title and "Name" in props:
        title = "".join(t.get("plain_text", "") for t in props["Name"].get("title", []))
    return title.strip() or page.get("id", "untitled")


def get_db_title(db: dict) -> str:
    """安全获取数据库标题。"""
    titles = db.get("title", [])
    if titles:
        return titles[0].get("plain_text", "").strip() or db.get("id", "untitled")
    return db.get("id", "untitled")


def is_relevant(item: dict) -> bool:
    """判断对象是否与龍魂相关。"""
    item_type = item.get("object", "")
    text_pool = ""
    if item_type == "page":
        text_pool = get_page_title(item)
        for prop in item.get("properties", {}).values():
            if prop.get("type") == "title":
                text_pool += " " + "".join(t.get("plain_text", "") for t in prop.get("title", []))
    elif item_type == "database":
        text_pool = get_db_title(item)
        for title in item.get("title", []):
            text_pool += " " + title.get("plain_text", "")

    text_pool_lower = text_pool.lower()
    return any(kw.lower() in text_pool_lower for kw in RELEVANT_KEYWORDS)


def main():
    parser = argparse.ArgumentParser(description="龍魂 · Notion 工作区全量导出")
    parser.add_argument("--output", default="docs/notion_full_export", help="导出目录")
    parser.add_argument("--query", default="", help="搜索关键词（默认空=全部）")
    parser.add_argument("--max-pages", type=int, default=500, help="最多导出相关页面数（默认500）")
    args = parser.parse_args()

    token = get_token()
    out_root = Path(args.output)
    out_root.mkdir(parents=True, exist_ok=True)

    print(f"[{_now()}] 🐉 开始全量导出 Notion 工作区")
    print(f"[{_now()}]    输出: {out_root.resolve()}")

    # 1. 搜索所有对象
    print(f"[{_now()}] 🔍 搜索所有页面和数据库...")
    all_items = search_all(token, args.query)
    pages = [x for x in all_items if x.get("object") == "page"]
    databases = [x for x in all_items if x.get("object") == "database"]
    print(f"[{_now()}]    原始页面: {len(pages)} | 原始数据库: {len(databases)}")

    # 2. 过滤相关对象
    pages = [p for p in pages if is_relevant(p)]
    databases = [d for d in databases if is_relevant(d)]
    print(f"[{_now()}]    过滤后页面: {len(pages)} | 过滤后数据库: {len(databases)}")

    # 限制页面数量防止爆炸
    if len(pages) > args.max_pages:
        print(f"[{_now()}]    ⚠️ 页面数超过 --max-pages={args.max_pages}，只取前 {args.max_pages} 个")
        pages = pages[:args.max_pages]

    # 2.5 保存索引
    index = {
        "exported_at": datetime.now().isoformat(),
        "total_pages": len(pages),
        "total_databases": len(databases),
        "pages": [
            {
                "id": p.get("id"),
                "title": get_page_title(p),
                "url": p.get("url", ""),
                "created_time": p.get("created_time", ""),
                "last_edited_time": p.get("last_edited_time", ""),
            }
            for p in pages
        ],
        "databases": [
            {
                "id": d.get("id"),
                "title": get_db_title(d),
                "url": d.get("url", ""),
            }
            for d in databases
        ],
    }
    with open(out_root / "_index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"[{_now()}]    索引已保存: {out_root / '_index.json'}")

    # 3. 导出每个页面为 Markdown
    pages_dir = out_root / "pages"
    pages_dir.mkdir(exist_ok=True)
    for idx, page in enumerate(pages, 1):
        title = get_page_title(page)
        fname = f"{idx:03d}_{safe_filename(title)}.md"
        fpath = pages_dir / fname
        print(f"[{_now()}] 📄 [{idx}/{len(pages)}] {title[:60]}")
        try:
            md = fetch_page_markdown(token, page["id"])
            # 清洗简体龙 → 繁体龍
            md = md.replace("龙", "龍")
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(f"# {title}\n\n")
                f.write(f"**DNA**: #龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-NOTION-EXPORT-{page['id']}\n\n")
                f.write(md)
        except Exception as e:
            print(f"[{_now()}]   ⚠️ 导出失败 {page['id']}: {e}")

    # 4. 导出每个数据库为 JSONL
    dbs_dir = out_root / "databases"
    dbs_dir.mkdir(exist_ok=True)
    for idx, db in enumerate(databases, 1):
        db_title = get_db_title(db)
        fname = f"{idx:03d}_{safe_filename(db_title)}.jsonl"
        fpath = dbs_dir / fname
        print(f"[{_now()}] 🗃️  [{idx}/{len(databases)}] {db_title[:60]}")
        try:
            rows = query_database(token, db["id"])
            with open(fpath, "w", encoding="utf-8") as f:
                for row in rows:
                    # 清洗简体龙
                    row_text = json.dumps(row, ensure_ascii=False).replace("龙", "龍")
                    row = json.loads(row_text)
                    f.write(json.dumps(row, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"[{_now()}]   ⚠️ 查询失败 {db['id']}: {e}")

    print(f"[{_now()}] ✅ 导出完成")
    print(f"    页面: {pages_dir}")
    print(f"    数据库: {dbs_dir}")
    print(f"    索引: {out_root / '_index.json'}")


if __name__ == "__main__":
    main()
