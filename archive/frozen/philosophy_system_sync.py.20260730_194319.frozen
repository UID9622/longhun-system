#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · Notion 最高哲学体系同步器 v1.0

功能：
- 从指定 Notion 页面拉取内容，转成 Markdown 保存到 docs/philosophy-system/
- 在该 Notion 页面下建立顶层知识库结构（索引数据库 + 核心子页面）

用法：
    export NOTION_TOKEN="secret_xxx"
    python3 integrations/notion/philosophy_system_sync.py \
        --url "https://www.notion.so/uid9622/v1-0-DNA-095994fbc6c44138808e7d23c634e019"

DNA:#龍芯⚡️2026-06-17-NOTION-PHILOSOPHY-SYNC-v1.0
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests


class NotionClient:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        self.base = "https://api.notion.com/v1"

    def get(self, path: str) -> Optional[Dict[str, Any]]:
        url = f"{self.base}{path}"
        r = requests.get(url, headers=self.headers, timeout=30)
        if r.status_code != 200:
            print(f"❌ GET {path} 失败: {r.status_code} {r.text[:200]}")
            return None
        return r.json()

    def post(self, path: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        url = f"{self.base}{path}"
        r = requests.post(url, headers=self.headers, json=payload, timeout=30)
        if r.status_code not in (200, 201):
            print(f"❌ POST {path} 失败: {r.status_code} {r.text[:300]}")
            return None
        return r.json()

    def patch(self, path: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        url = f"{self.base}{path}"
        r = requests.patch(url, headers=self.headers, json=payload, timeout=30)
        if r.status_code != 200:
            print(f"❌ PATCH {path} 失败: {r.status_code} {r.text[:300]}")
            return None
        return r.json()


def extract_page_id(url_or_id: str) -> str:
    """从 Notion URL 或各种 ID 格式中提取 32 位 page id（无连字符）。"""
    s = url_or_id.strip()
    # 处理带 ? 的 URL
    s = s.split("?")[0]
    # 尝试匹配 32 位十六进制
    m = re.search(r"([0-9a-fA-F]{32})", s)
    if m:
        return m.group(1).lower()
    # 尝试匹配连字符格式
    m = re.search(r"([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})", s)
    if m:
        return m.group(1).replace("-", "").lower()
    raise ValueError(f"无法从 {url_or_id!r} 提取 Notion page id")


def format_uuid(raw_id: str) -> str:
    """将 32 位 raw id 格式化成带连字符的 UUID。"""
    raw_id = raw_id.lower()
    return f"{raw_id[:8]}-{raw_id[8:12]}-{raw_id[12:16]}-{raw_id[16:20]}-{raw_id[20:]}"


def get_title(page: Dict[str, Any]) -> str:
    title_objs = page.get("properties", {}).get("title", {}).get("title", [])
    return "".join(t.get("plain_text", "") for t in title_objs).strip() or "Untitled"


def rich_text_to_markdown(rich_texts: List[Dict[str, Any]]) -> str:
    out = []
    for rt in rich_texts:
        text = rt.get("plain_text", "")
        annotations = rt.get("annotations", {})
        if annotations.get("bold"):
            text = f"**{text}**"
        if annotations.get("italic"):
            text = f"*{text}*"
        if annotations.get("strikethrough"):
            text = f"~~{text}~~"
        if annotations.get("code"):
            text = f"`{text}`"
        link = rt.get("href") or rt.get("text", {}).get("link", {}).get("url")
        if link:
            text = f"[{text}]({link})"
        out.append(text)
    return "".join(out)


def block_to_markdown(block: Dict[str, Any], depth: int = 0) -> str:
    btype = block.get("type", "")
    handler = {
        "paragraph": lambda b: rich_text_to_markdown(b["paragraph"].get("rich_text", [])) or "",
        "heading_1": lambda b: f"# {rich_text_to_markdown(b['heading_1'].get('rich_text', []))}",
        "heading_2": lambda b: f"## {rich_text_to_markdown(b['heading_2'].get('rich_text', []))}",
        "heading_3": lambda b: f"### {rich_text_to_markdown(b['heading_3'].get('rich_text', []))}",
        "bulleted_list_item": lambda b: f"- {rich_text_to_markdown(b['bulleted_list_item'].get('rich_text', []))}",
        "numbered_list_item": lambda b: f"1. {rich_text_to_markdown(b['numbered_list_item'].get('rich_text', []))}",
        "to_do": lambda b: f"- [{'x' if b['to_do'].get('checked') else ' '}] {rich_text_to_markdown(b['to_do'].get('rich_text', []))}",
        "quote": lambda b: f"> {rich_text_to_markdown(b['quote'].get('rich_text', []))}",
        "callout": lambda b: f"> 📌 {rich_text_to_markdown(b['callout'].get('rich_text', []))}",
        "code": lambda b: f"```{b['code'].get('language', '')}\n{rich_text_to_markdown(b['code'].get('rich_text', []))}\n```",
        "divider": lambda b: "---",
        "bookmark": lambda b: f"🔗 书签: {b['bookmark'].get('url', '')}",
        "link_to_page": lambda b: f"🔗 连结页面: {b['link_to_page'].get('page_id', '')}",
        "child_page": lambda b: f"📄 子页面: {b.get('child_page', {}).get('title', '')}",
        "image": lambda b: "",
        "table": lambda b: "",
        "unsupported": lambda b: "",
    }.get(btype)

    if handler is None:
        return f"<!-- 未支持区块类型: {btype} -->"

    text = handler(block)
    if text:
        indent = "  " * depth
        return indent + text
    return ""


def fetch_all_blocks(client: NotionClient, block_id: str) -> List[Dict[str, Any]]:
    blocks: List[Dict[str, Any]] = []
    cursor: Optional[str] = None
    while True:
        url = f"/blocks/{block_id}/children"
        params = {"page_size": 100}
        if cursor:
            params["start_cursor"] = cursor
        # GET with query params
        r = requests.get(
            f"{client.base}{url}",
            headers=client.headers,
            params=params,
            timeout=30,
        )
        if r.status_code != 200:
            print(f"❌ 无法获取区块 {block_id}: {r.status_code} {r.text[:200]}")
            break
        data = r.json()
        blocks.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")
        time.sleep(0.35)
    return blocks


def blocks_to_markdown(client: NotionClient, blocks: List[Dict[str, Any]], depth: int = 0) -> str:
    lines: List[str] = []
    for block in blocks:
        md = block_to_markdown(block, depth)
        if md:
            lines.append(md)
        # 递回处理嵌套区块
        children = block.get("children", fetch_all_blocks(client, block["id"])) if block.get("has_children") else []
        if children:
            lines.append(blocks_to_markdown(client, children, depth + 1))
    return "\n\n".join(lines)


def save_local_export(root: Path, page_id: str, title: str, markdown: str, notion_url: str) -> Path:
    dest_dir = root / "docs" / "philosophy-system"
    dest_dir.mkdir(parents=True, exist_ok=True)

    safe_title = re.sub(r"[^\w\u4e00-\u9fff-]", "_", title)[:60]
    md_file = dest_dir / f"{safe_title}-{page_id}.md"
    index_file = dest_dir / "INDEX.md"

    header = f"""# {title}

> 来源：[Notion 原始页面]({notion_url})
> 同步时间：{datetime.now().isoformat()}
> Page ID：`{page_id}`

---

"""
    content = header + markdown
    md_file.write_text(content, encoding="utf-8")

    # 更新索引
    index_entries = []
    if index_file.exists():
        for line in index_file.read_text(encoding="utf-8").splitlines():
            if line.startswith("- [") and page_id not in line:
                index_entries.append(line)
    index_entries.append(f"- [{title}]({md_file.name}) — {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    index_content = f"""# 龍魂最高哲学体系 · Notion 同步索引

本地备份来自 Notion，作为系统最高哲学体系的单一真相源。

## 同步条目

{"\n".join(index_entries)}

## 原始入口

- [Notion 页面]({notion_url})
"""
    index_file.write_text(index_content, encoding="utf-8")

    return md_file


def create_philosophy_database(client: NotionClient, parent_page_id: str, title: str) -> Optional[str]:
    """在指定页面下建立“哲学体系索引”数据库。"""
    payload = {
        "parent": {"type": "page_id", "page_id": format_uuid(parent_page_id)},
        "title": [{"type": "text", "text": {"content": "🧠 哲学体系索引"}}],
        "properties": {
            "名称": {"title": {}},
            "层级": {
                "select": {
                    "options": [
                        {"name": "L0 永恒层", "color": "red"},
                        {"name": "L1 压舱石", "color": "orange"},
                        {"name": "L2 国家DNA", "color": "yellow"},
                        {"name": "L3 全球共识", "color": "green"},
                        {"name": "执行方法", "color": "blue"},
                    ]
                }
            },
            "状态": {
                "select": {
                    "options": [
                        {"name": "🌱 萌芽", "color": "gray"},
                        {"name": "📝 草稿", "color": "yellow"},
                        {"name": "✅ 定稿", "color": "green"},
                    ]
                }
            },
            "标签": {"multi_select": {"options": []}},
            "来源": {"url": {}},
            "同步时间": {"date": {}},
        },
    }
    result = client.post("/databases", payload)
    if result:
        print(f"✅ 已建立哲学体系索引数据库：{result.get('id')}")
        return result.get("id")
    return None


def create_child_pages(client: NotionClient, parent_page_id: str) -> List[Dict[str, str]]:
    """在指定页面下建立核心子页面模板。"""
    pages = [
        {"title": "一、核心命题", "content": "记录系统的最高命题与第一性原理。"},
        {"title": "二、治理原则", "content": "全球治理、主权、信任、审计的底层原则。"},
        {"title": "三、执行方法", "content": "将哲学转化为代码、流程、检查清单的具体方法。"},
        {"title": "四、参考文档", "content": "相关论文、协议、备份与外部链接。"},
    ]
    created = []
    for page in pages:
        payload = {
            "parent": {"type": "page_id", "page_id": format_uuid(parent_page_id)},
            "properties": {
                "title": {"title": [{"type": "text", "text": {"content": page["title"]}}]}
            },
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": page["content"]}}]
                    },
                }
            ],
        }
        result = client.post("/pages", payload)
        if result:
            created.append({"title": page["title"], "id": result.get("id", "")})
            print(f"✅ 已建立子页面：{page['title']}")
        time.sleep(0.35)
    return created


def main():
    parser = argparse.ArgumentParser(description="龍魂 Notion 最高哲学体系同步器")
    parser.add_argument("--url", required=True, help="Notion 页面 URL 或 Page ID")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[2]), help="项目根目录")
    parser.add_argument("--build-structure", action="store_true", help="在 Notion 建立顶层结构")
    args = parser.parse_args()

    token = os.environ.get("NOTION_TOKEN")
    if not token:
        print("❌ 请设置环境变量 NOTION_TOKEN")
        sys.exit(1)

    page_id = extract_page_id(args.url)
    notion_url = f"https://www.notion.so/{page_id}"

    client = NotionClient(token)

    print(f"🐉 开始同步 Notion 哲学体系")
    print(f"   Page ID: {page_id}")

    page = client.get(f"/pages/{format_uuid(page_id)}")
    if not page:
        print("❌ 无法获取页面。请确认：")
        print("   1. Token 有效")
        print("   2. 已将该页面 Share 给此 Integration")
        sys.exit(1)

    title = get_title(page)
    print(f"   页面标题: {title}")

    print("📥 拉取区块内容...")
    blocks = fetch_all_blocks(client, page_id)
    print(f"   共 {len(blocks)} 个区块")

    print("📝 转换为 Markdown...")
    markdown = blocks_to_markdown(client, blocks)

    root_path = Path(args.root)
    md_file = save_local_export(root_path, page_id, title, markdown, notion_url)
    print(f"✅ 已保存本地备份: {md_file}")

    if args.build_structure:
        print("🏛️ 建立 Notion 顶层结构...")
        db_id = create_philosophy_database(client, page_id, title)
        create_child_pages(client, page_id)
        if db_id:
            print(f"   数据库 ID: {db_id}")

    print("\n✅ 同步完成")
    print(f"   本地索引: {root_path / 'docs' / 'philosophy-system' / 'INDEX.md'}")
    print(f"   Notion 页面: {notion_url}")


if __name__ == "__main__":
    main()
