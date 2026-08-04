#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 Markdown → Notion 同步脚本 v1.0
DNA: #龍芯⚡️2026-07-04-LONGHUN-MD2NOTION-v1.0

功能：
- 把本地 Markdown 文件同步到 Notion 页面
- 支持创建新页面或更新已有页面（按标题匹配）
- 自动将 Markdown 转为 Notion block（标题/段落/列表/引用/代码/分隔线/表格）
- 大文件自动分块追加，避开 Notion API 100 block/次限制
- 生成 DNA 审计报告

用法：
  python3 sync_to_notion.py <markdown文件> --title "页面标题" --parent <parent_page_id>
  python3 sync_to_notion.py longhun-system/docs/道德经81章_..._v4.1_多维度注解.md \
      --title "道德经81章 · 多维度注解 v4.1" --parent <page_id> --dry-run

配置（首次运行前设置）：
  export NOTION_TOKEN="secret_xxx"                        # 或写入 ~/.longhun/config/notion_sync.json
  export NOTION_DEFAULT_PARENT_PAGE="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # 可选默认父页面
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any

import requests

CONFIG_PATH = Path.home() / ".longhun" / "config" / "notion_sync.json"
NOTION_API = "https://api.notion.com/v1"
MAX_BLOCKS_PER_REQUEST = 90  # 留余量，Notion 限制 100


def dna(prefix: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")[:-3]
    h = __import__("hashlib").sha256(f"{prefix}|{ts}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-{prefix}-{h}"


def load_config() -> Dict[str, str]:
    cfg = {}
    if CONFIG_PATH.exists():
        try:
            cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"🟡 读取配置失败: {e}")
    cfg.setdefault("token", os.getenv("NOTION_TOKEN", ""))
    cfg.setdefault("default_parent_page", os.getenv("NOTION_DEFAULT_PARENT_PAGE", ""))
    return cfg


def save_config(cfg: Dict[str, str]):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")


def notion_headers(token: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }


def extract_title_from_front(text: str, fallback: str) -> str:
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else fallback


def text_block_obj(text: str, annotations: Optional[Dict] = None) -> Dict[str, Any]:
    obj = {"type": "text", "text": {"content": text[:2000]}}
    if annotations:
        obj["annotations"] = annotations
    return obj


def make_rich_text(text: str) -> List[Dict]:
    """简单实现：把 **bold** 和 `code` 转成 rich_text。"""
    parts = []
    # 先处理 `code`
    segments = re.split(r"(`[^`]+`)", text)
    for seg in segments:
        if seg.startswith("`") and seg.endswith("`") and len(seg) > 2:
            parts.append(text_block_obj(seg[1:-1], {"code": True}))
        else:
            # 再处理 **bold**
            sub_segs = re.split(r"(\*\*[^*]+\*\*)", seg)
            for sub in sub_segs:
                if sub.startswith("**") and sub.endswith("**") and len(sub) > 4:
                    parts.append(text_block_obj(sub[2:-2], {"bold": True}))
                else:
                    parts.append(text_block_obj(sub))
    return parts


def paragraph_block(text: str) -> Dict[str, Any]:
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": make_rich_text(text)}}


def heading_block(level: int, text: str) -> Dict[str, Any]:
    key = f"heading_{level}"
    return {"object": "block", "type": key, key: {"rich_text": make_rich_text(text)}}


def quote_block(text: str) -> Dict[str, Any]:
    return {"object": "block", "type": "quote", "quote": {"rich_text": make_rich_text(text.lstrip("> ").strip())}}


def bulleted_item(text: str) -> Dict[str, Any]:
    return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": make_rich_text(text)}}


def numbered_item(text: str) -> Dict[str, Any]:
    return {"object": "block", "type": "numbered_list_item", "numbered_list_item": {"rich_text": make_rich_text(text)}}


# Notion 支持的 code 语言白名单（节选常见）
NOTION_CODE_LANGUAGES = {
    "abap", "abc", "agda", "arduino", "ascii art", "assembly", "autohotkey", "batch", "bison",
    "c", "csharp", "cpp", "clojure", "coffeescript", "css", "d", "dart", "docker", "elixir",
    "erlang", "fortran", "fsharp", "go", "graphql", "groovy", "haskell", "html", "java",
    "javascript", "json", "julia", "kotlin", "latex", "lisp", "lua", "markdown", "matlab",
    "nginx", "objective-c", "ocaml", "pascal", "perl", "php", "plain text", "powershell",
    "protobuf", "python", "r", "ruby", "rust", "sass", "scala", "scheme", "scss", "shell",
    "smalltalk", "sql", "swift", "typescript", "vb.net", "verilog", "vhdl", "xml", "yaml",
}


def normalize_code_language(language: str) -> str:
    lang = language.strip().lower()
    if not lang or lang in ("text", "txt", "cns", "cnsl"):
        return "plain text"
    if lang in NOTION_CODE_LANGUAGES:
        return lang
    # 常见别名映射
    aliases = {
        "py": "python",
        "js": "javascript",
        "ts": "typescript",
        "sh": "shell",
        "bash": "shell",
        "zsh": "shell",
        "yml": "yaml",
        "c++": "cpp",
        "csharp": "c#",
        "objc": "objective-c",
    }
    if lang in aliases:
        mapped = aliases[lang]
        if mapped in NOTION_CODE_LANGUAGES:
            return mapped
    return "plain text"


def code_block(text: str, language: str = "plain text") -> Dict[str, Any]:
    return {"object": "block", "type": "code", "code": {"rich_text": [text_block_obj(text)], "language": normalize_code_language(language)}}


def divider_block() -> Dict[str, Any]:
    return {"object": "block", "type": "divider", "divider": {}}


def table_block(rows: List[List[str]]) -> Optional[Dict]:
    if not rows or len(rows) < 2:
        return None
    header = rows[0]
    body = rows[1:]
    table = {
        "object": "block",
        "type": "table",
        "table": {
            "table_width": len(header),
            "has_column_header": True,
            "has_row_header": False,
            "children": [],
        },
    }
    for row in [header] + body:
        cells = [{"type": "text", "text": {"content": cell.strip()[:1000]}} for cell in row]
        table["table"]["children"].append({
            "object": "block",
            "type": "table_row",
            "table_row": {"cells": [[c] for c in cells]},
        })
    return table


def parse_markdown(text: str) -> List[Dict]:
    """把 Markdown 文本解析为 Notion block 列表。"""
    lines = text.splitlines()
    blocks: List[Dict] = []
    i = 0
    code_buffer: List[str] = []
    code_lang = "plain text"
    in_code = False

    def flush_code():
        nonlocal code_buffer, code_lang, in_code
        if code_buffer:
            blocks.append(code_block("\n".join(code_buffer), code_lang))
            code_buffer = []
            code_lang = "plain text"
            in_code = False

    while i < len(lines):
        line = lines[i]

        if line.strip().startswith("```"):
            if in_code:
                flush_code()
            else:
                lang = line.strip()[3:].strip()
                if lang:
                    code_lang = lang
                in_code = True
            i += 1
            continue

        if in_code:
            code_buffer.append(line)
            i += 1
            continue

        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # 分隔线
        if stripped == "---" or stripped == "***" or stripped == "___":
            blocks.append(divider_block())
            i += 1
            continue

        # 引用
        if stripped.startswith("> "):
            blocks.append(quote_block(stripped))
            i += 1
            continue

        # 标题
        m = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if m:
            level = len(m.group(1))
            blocks.append(heading_block(min(level, 3), m.group(2)))
            i += 1
            continue

        # 无序列表
        m = re.match(r"^[-*+]\s+\[?\s?\]?\s*(.*)$", stripped)
        if m:
            blocks.append(bulleted_item(m.group(1)))
            i += 1
            continue

        # 有序列表
        m = re.match(r"^\d+\.\s+(.*)$", stripped)
        if m:
            blocks.append(numbered_item(m.group(1)))
            i += 1
            continue

        # 表格
        if "|" in stripped and i + 1 < len(lines) and re.match(r"^\|?\s*[-:|\s]+\s*\|?\s*$", lines[i + 1].strip()):
            rows = []
            while i < len(lines) and "|" in lines[i].strip():
                row = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                rows.append(row)
                i += 1
            # 跳过分隔行
            if rows and len(rows) >= 2:
                rows = [rows[0]] + rows[2:]
                tbl = table_block(rows)
                if tbl:
                    blocks.append(tbl)
            continue

        # 普通段落
        blocks.append(paragraph_block(stripped))
        i += 1

    flush_code()
    return blocks


def find_page_by_title(token: str, parent_page_id: str, title: str) -> Optional[str]:
    """在父页面下按标题查找已有页面。优先用搜索 API，失败再遍历子 block。"""
    headers = notion_headers(token)
    # 方案 A：Notion 搜索 API（快）
    try:
        r = requests.post(
            f"{NOTION_API}/search",
            headers=headers,
            json={"query": title, "page_size": 10},
            timeout=10,
        )
        if r.status_code == 200:
            for page in r.json().get("results", []):
                if page.get("object") == "page":
                    props = page.get("properties", {})
                    page_title = ""
                    if "title" in props:
                        title_parts = props["title"].get("title", [])
                        page_title = "".join(t.get("text", {}).get("content", "") for t in title_parts)
                    if page_title == title:
                        # 确认父页面匹配
                        parent = page.get("parent", {})
                        if parent.get("type") == "page_id" and parent.get("page_id") == parent_page_id:
                            return page["id"]
    except Exception as e:
        print(f"   搜索 API 失败，回退到子 block 遍历: {e}")

    # 方案 B：遍历父页面子 block（慢，兜底）
    url = f"{NOTION_API}/blocks/{parent_page_id}/children"
    page_idx = 0
    while url:
        page_idx += 1
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None
        data = r.json()
        for block in data.get("results", []):
            if block.get("type") == "child_page" and block.get("child_page", {}).get("title") == title:
                return block["id"]
        nxt = data.get("next_cursor")
        if nxt:
            url = f"{NOTION_API}/blocks/{parent_page_id}/children?start_cursor={nxt}"
        else:
            url = None
    return None


def create_page(token: str, parent_page_id: str, title: str, icon: str = "📜") -> str:
    headers = notion_headers(token)
    payload = {
        "parent": {"page_id": parent_page_id},
        "properties": {"title": {"title": [{"text": {"content": title}}]}},
        "icon": {"emoji": icon},
    }
    r = requests.post(f"{NOTION_API}/pages", headers=headers, json=payload, timeout=15)
    if r.status_code != 200:
        raise RuntimeError(f"创建页面失败: {r.status_code} {r.text}")
    return r.json()["id"]


def append_blocks(token: str, page_id: str, blocks: List[Dict], dry_run: bool = False) -> int:
    if dry_run:
        print(f"  [DRY-RUN] 将追加 {len(blocks)} 个 block")
        return len(blocks)
    headers = notion_headers(token)
    url = f"{NOTION_API}/blocks/{page_id}/children"
    total = 0
    chunks = list(range(0, len(blocks), MAX_BLOCKS_PER_REQUEST))
    print(f"   共 {len(blocks)} 个 block，分 {len(chunks)} 批写入")
    for idx, i in enumerate(chunks):
        chunk = blocks[i:i + MAX_BLOCKS_PER_REQUEST]
        for attempt in range(3):
            try:
                r = requests.patch(url, headers=headers, json={"children": chunk}, timeout=(5, 30))
                if r.status_code == 200:
                    total += len(chunk)
                    print(f"   [{idx+1}/{len(chunks)}] 已写入 {total}/{len(blocks)} 个 block")
                    break
                else:
                    print(f"   [{idx+1}/{len(chunks)}] 尝试 {attempt+1} 失败: {r.status_code} {r.text[:200]}")
                    time.sleep(1.5 ** attempt)
            except Exception as e:
                print(f"   [{idx+1}/{len(chunks)}] 尝试 {attempt+1} 异常: {e}")
                time.sleep(1.5 ** attempt)
        else:
            raise RuntimeError(f"追加 block 失败 (cursor={i})，已重试 3 次")
        time.sleep(0.35)  # 限流
    return total


def clear_page_blocks(token: str, page_id: str, dry_run: bool = False) -> int:
    """删除页面现有 block（仅删除顶层 block）。"""
    if dry_run:
        print("  [DRY-RUN] 将清空页面现有 block")
        return 0
    headers = notion_headers(token)
    url = f"{NOTION_API}/blocks/{page_id}/children"
    r = requests.get(url, headers=headers, timeout=15)
    if r.status_code != 200:
        return 0
    blocks = r.json().get("results", [])
    count = 0
    for b in blocks:
        bid = b.get("id")
        if bid:
            dr = requests.delete(f"{NOTION_API}/blocks/{bid}", headers=headers, timeout=15)
            if dr.status_code == 200:
                count += 1
            time.sleep(0.15)
    return count


def main():
    parser = argparse.ArgumentParser(description="龍魂 Markdown → Notion 同步")
    parser.add_argument("file", help="要同步的 Markdown 文件路径")
    parser.add_argument("--title", help="Notion 页面标题（默认从文件首行 # 提取）")
    parser.add_argument("--parent", help="父页面 ID（默认使用配置文件或环境变量）")
    parser.add_argument("--icon", default="📜", help="页面图标 emoji")
    parser.add_argument("--dry-run", action="store_true", help="试运行，不实际写入 Notion")
    parser.add_argument("--skip-clear", action="store_true", help="不清空已有 block（追加模式）")
    parser.add_argument("--force-new", action="store_true", help="强制创建新页面，不查找/更新已有页面")
    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"🔴 文件不存在: {file_path}")
        sys.exit(1)

    cfg = load_config()
    token = cfg.get("token", "")
    parent_page_id = args.parent or cfg.get("default_parent_page", "")

    if not token:
        print("🔴 未配置 NOTION_TOKEN。请设置环境变量或写入配置文件。")
        print(f"   配置文件: {CONFIG_PATH}")
        print('   格式: {"token": "secret_xxx", "default_parent_page": "page_id"}')
        sys.exit(1)

    if not parent_page_id:
        print("🔴 未指定父页面 ID。请使用 --parent 或在配置文件中设置 default_parent_page。")
        sys.exit(1)

    text = file_path.read_text(encoding="utf-8")
    title = args.title or extract_title_from_front(text, file_path.stem)

    print(f"🐉 龍魂 Markdown → Notion 同步")
    print(f"   文件: {file_path}")
    print(f"   标题: {title}")
    print(f"   父页面: {parent_page_id}")
    print(f"   模式: {'DRY-RUN' if args.dry_run else '真实写入'}")
    print()

    print("▶ 解析 Markdown...")
    blocks = parse_markdown(text)
    print(f"   共解析 {len(blocks)} 个 block")

    print("▶ 查找/创建 Notion 页面...")
    if args.dry_run:
        print("   [DRY-RUN] 将查找或创建页面")
        page_id = "DRY-RUN-PAGE-ID"
    elif args.force_new:
        page_id = create_page(token, parent_page_id, title, icon=args.icon)
        print(f"   强制创建新页面: {page_id}")
    else:
        page_id = find_page_by_title(token, parent_page_id, title)
        if page_id:
            print(f"   找到已有页面: {page_id}")
            if not args.skip_clear:
                cleared = clear_page_blocks(token, page_id, dry_run=args.dry_run)
                print(f"   已清空 {cleared} 个旧 block")
        else:
            page_id = create_page(token, parent_page_id, title, icon=args.icon)
            print(f"   已创建新页面: {page_id}")

    print("▶ 写入 block...")
    total = append_blocks(token, page_id, blocks, dry_run=args.dry_run)
    print(f"   已写入 {total} 个 block")

    page_url = f"https://notion.so/{page_id.replace('-', '')}"
    print(f"\n✅ 同步完成")
    print(f"   页面 URL: {page_url}")

    report = {
        "dna": dna("NOTION-SYNC"),
        "source_file": str(file_path.resolve()),
        "notion_page_id": page_id,
        "notion_page_url": page_url,
        "title": title,
        "blocks_count": total,
        "dry_run": args.dry_run,
        "synced_at": datetime.now(timezone.utc).isoformat(),
    }
    report_path = file_path.with_suffix(".notion_sync_report.json")
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"   报告: {report_path}")
    print(f"   DNA: {report['dna']}")


if __name__ == "__main__":
    main()
