#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 · Notion 雙向同步腳本 v1.0

功能：
  - pull：把 Notion 頁面（含子塊）拉取為本地 Markdown
  - push：把本地 Markdown 推送為 Notion 子頁面
  - sync：按配置文件執行批量 pull/push

用法：
  python3 notion_sync.py pull --page-id 2d87125a-9c9f-8028-89e2-e18002f7cf4f -o page.md
  python3 notion_sync.py push --parent-id <page_id> -i page.md --title "同步測試"
  python3 notion_sync.py sync --config config.json

DNA: #龍芯⚡️丙午·甲午·庚辰·壬午·䷑蛊-LONGHUN-NOTION-SYNC-v1.0
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# ═══════════════════════════════════════════
# 0. 路徑與配置
# ═══════════════════════════════════════════
HOME = Path.home()
LONGHUN_ROOT = Path(os.environ.get("LONGHUN_ROOT", HOME / "longhun-system"))
SYNC_DIR = HOME / ".longhun" / "notion_sync"
AUDIT_DIR = HOME / ".longhun" / "audit"
SYNC_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

# 自动加载本地密钥文件（LaunchAgent / cron 场景下环境变量可能未注入）
SECRETS_ENV = HOME / ".longhun" / "secrets.env"
if SECRETS_ENV.exists():
    for line in SECRETS_ENV.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, val = line.split("=", 1)
            key = key.strip()
            # 兼容 export KEY=val 写法
            if key.startswith("export "):
                key = key[7:].strip()
            val = val.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = val

AUDIT_FILE = AUDIT_DIR / "notion_sync_audit.jsonl"
STATE_FILE = SYNC_DIR / "state.json"
DEFAULT_CONFIG = LONGHUN_ROOT / "config" / "notion_sync.json"

DNA_PREFIX = "#龍芯⚡️"


# ═══════════════════════════════════════════
# 1. DNA 與審計
# ═══════════════════════════════════════════
def now_iso() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat()


def make_dna(op: str) -> str:
    ts = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    raw = f"{op}-{ts}-{uuid.uuid4().hex[:8]}"
    h = hashlib.sha256(raw.encode()).hexdigest()[:8].upper()
    return f"{DNA_PREFIX}{ts}-NOTION-SYNC-{op}-{h}"


def audit(action: str, page_id: str, path: str, status: str, detail: dict[str, Any]):
    entry = {
        "timestamp": now_iso(),
        "action": action,
        "page_id": page_id,
        "path": path,
        "status": status,
        "detail": detail,
        "dna": make_dna(action),
    }
    AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with AUDIT_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry["dna"]


# ═══════════════════════════════════════════
# 2. Notion API 客戶端
# ═══════════════════════════════════════════
class NotionClient:
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get("NOTION_TOKEN")
        if not self.token:
            raise RuntimeError("未設置 NOTION_TOKEN 環境變量")
        self.base = "https://api.notion.com/v1"
        self._req_count = 0

    def _req(self, method: str, path: str, data: Optional[dict[str, Any]] = None, timeout: float = 60.0) -> dict[str, Any]:
        url = f"{self.base}{path}"
        cmd = [
            "curl", "-s", "-X", method,
            "--max-time", str(int(timeout)),
            "-H", f"Authorization: Bearer {self.token}",
            "-H", "Notion-Version: 2022-06-28",
            "-w", "\nHTTP_CODE:%{http_code}",
            url,
        ]
        if data is not None:
            cmd.extend(["-H", "Content-Type: application/json", "-d", json.dumps(data, ensure_ascii=False)])

        for attempt in range(3):
            try:
                result = subprocess.run(cmd, capture_output=True, timeout=timeout + 5)
                out = result.stdout.decode("utf-8", errors="ignore")
                if "HTTP_CODE:" not in out:
                    raise RuntimeError(f"curl 未返回 HTTP_CODE: {out[:200]}")
                body, code_str = out.rsplit("HTTP_CODE:", 1)
                code = int(code_str.strip())
                self._req_count += 1
                if code == 429:
                    sleep = 1 + attempt * 2
                    print(f"[速率限制] 等待 {sleep}s 後重試...")
                    time.sleep(sleep)
                    continue
                if code >= 400:
                    raise RuntimeError(f"Notion API {method} {url} -> HTTP {code}: {body.strip()[:500]}")
                return json.loads(body)
            except subprocess.TimeoutExpired as e:
                if attempt < 2:
                    print(f"[超時] 等待 2s 後重試...")
                    time.sleep(2)
                    continue
                raise RuntimeError(f"Notion API 超時: {method} {url}")
            except RuntimeError:
                raise
            except Exception as e:
                if attempt < 2:
                    time.sleep(1)
                    continue
                raise RuntimeError(f"Notion API 請求失敗: {method} {url} -> {e}")
        raise RuntimeError(f"Notion API 重試耗盡: {method} {url}")

    def get_page(self, page_id: str) -> dict[str, Any]:
        return self._req("GET", f"/pages/{page_id}")

    def get_children(self, block_id: str, page_size: int = 100, start_cursor: Optional[str] = None, timeout: float = 60.0) -> dict[str, Any]:
        path = f"/blocks/{block_id}/children?page_size={page_size}"
        if start_cursor:
            path += f"&start_cursor={start_cursor}"
        return self._req("GET", path, timeout=timeout)

    def create_page(self, parent_id: str, title: str, children: List[dict[str, Any]]) -> dict[str, Any]:
        payload = {
            "parent": {"page_id": parent_id},
            "properties": {
                "title": {"title": [{"text": {"content": title}}]}
            },
        }
        # 一次最多 100 個子塊，先寫入前 100，後續 append
        payload["children"] = children[:100]
        page = self._req("POST", "/pages", payload)
        remaining = children[100:]
        while remaining:
            chunk = remaining[:100]
            remaining = remaining[100:]
            self._req("PATCH", f"/blocks/{page['id']}/children", {"children": chunk})
        return page

    def append_blocks(self, block_id: str, children: List[dict[str, Any]]) -> dict[str, Any]:
        return self._req("PATCH", f"/blocks/{block_id}/children", {"children": children})


# ═══════════════════════════════════════════
# 3. Pull：Notion → Markdown
# ═══════════════════════════════════════════
def rich_text(rt: List[dict[str, Any]]) -> str:
    return "".join(t.get("plain_text", "") for t in rt)


def block_to_md(b: dict[str, Any], depth: int = 0) -> List[str]:
    t = b.get("type")
    d = b.get(t, {})
    text = rich_text(d.get("rich_text", []))
    indent = "  " * depth
    lines: List[str] = []

    if t == "paragraph":
        if text.strip():
            lines.append(indent + text)
    elif t.startswith("heading_"):
        lvl = int(t.split("_")[1])
        lines.append(indent + "#" * lvl + " " + text)
    elif t == "callout":
        icon = d.get("icon", {}).get("emoji", "")
        lines.append(indent + f"> {icon} {text}")
    elif t == "quote":
        lines.append(indent + "> " + text)
    elif t == "bulleted_list_item":
        lines.append(indent + "- " + text)
    elif t == "numbered_list_item":
        lines.append(indent + "1. " + text)
    elif t == "to_do":
        chk = "[x]" if d.get("checked") else "[ ]"
        lines.append(indent + f"- {chk} {text}")
    elif t == "code":
        lang = d.get("language", "")
        lines.append(indent + f"```{lang}")
        lines.append(indent + text)
        lines.append(indent + "```")
    elif t == "divider":
        lines.append(indent + "---")
    elif t == "table":
        lines.append(indent + "[table]")
    elif t == "table_row":
        cells = [rich_text(cell) for cell in d.get("cells", [])]
        lines.append(indent + "| " + " | ".join(cells) + " |")
    elif t == "image":
        url = d.get("external", {}).get("url") or d.get("file", {}).get("url", "")
        lines.append(indent + f"![image]({url})")
    elif t == "bookmark":
        lines.append(indent + f"[bookmark: {d.get('url', '')}]")
    elif t == "link_to_page":
        lines.append(indent + f"[link_to_page: {d.get('page_id', '')}]")
    elif t == "child_page":
        lines.append(indent + f"[child_page: {d.get('title', '')}]")
    elif text:
        lines.append(indent + f"[{t}] {text}")
    return lines


class NotionPuller:
    def __init__(self, client: NotionClient, max_depth: int = 6, max_blocks: Optional[int] = None):
        self.client = client
        self.max_depth = max_depth
        self.max_blocks = max_blocks
        self.block_count = 0
        self._stop = False

    def pull(self, page_id: str) -> str:
        page = self.client.get_page(page_id)
        title = ""
        title_obj = page.get("properties", {}).get("title", {})
        if title_obj:
            title = rich_text(title_obj.get("title", []))
        lines = [f"# {title}", f"", f"<!-- Notion page_id: {page_id} -->", f"<!-- pulled_at: {now_iso()} -->", ""]
        self._fetch_children(page_id, lines, depth=0)
        return "\n".join(lines)

    def _fetch_children(self, block_id: str, lines: List[str], depth: int):
        if self._stop or depth > self.max_depth:
            return
        cursor = None
        # 子塊查詢用較短超時，避免單個超級大 callout/toggle 拖垮整個 pull
        page_size = 10 if depth > 0 else 100
        timeout = 8.0 if depth > 0 else 30.0
        while True:
            try:
                data = self.client.get_children(block_id, page_size=page_size, start_cursor=cursor, timeout=timeout)
            except Exception as e:
                lines.append(f"<!-- 拉取子塊失敗 {block_id}: {e} -->")
                break
            for b in data.get("results", []):
                if self.max_blocks is not None and self.block_count >= self.max_blocks:
                    self._stop = True
                    lines.append("<!-- 已達 max_blocks 上限，內容截斷 -->")
                    break
                self.block_count += 1
                lines.extend(block_to_md(b, depth))
                if b.get("has_children") and b.get("type") != "table_row":
                    self._fetch_children(b["id"], lines, depth + 1)
                if self._stop:
                    break
            if self._stop or not data.get("has_more"):
                break
            cursor = data.get("next_cursor")


# ═══════════════════════════════════════════
# 4. Push：Markdown → Notion 子頁面
# ═══════════════════════════════════════════
def md_to_blocks(md_text: str) -> List[dict[str, Any]]:
    blocks: List[dict[str, Any]] = []
    lines = md_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # 代碼塊
        if stripped.startswith("```"):
            lang = stripped[3:].strip() or "plain text"
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # 跳過結尾 ```
            blocks.append({
                "object": "block",
                "type": "code",
                "code": {"rich_text": [{"type": "text", "text": {"content": "\n".join(code_lines)}}], "language": lang},
            })
            continue

        # 標題
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            level = len(m.group(1))
            blocks.append({
                "object": "block",
                "type": f"heading_{level}",
                f"heading_{level}": {"rich_text": [{"type": "text", "text": {"content": m.group(2)}}]},
            })
            i += 1
            continue

        # to_do
        m = re.match(r"^-\s+\[(x| )\]\s+(.*)$", stripped)
        if m:
            blocks.append({
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [{"type": "text", "text": {"content": m.group(2)}}],
                    "checked": m.group(1) == "x",
                },
            })
            i += 1
            continue

        # 無序列表
        if stripped.startswith("- "):
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": stripped[2:]}}]},
            })
            i += 1
            continue

        # 有序列表
        m = re.match(r"^\d+\.\s+(.*)$", stripped)
        if m:
            blocks.append({
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": m.group(1)}}]},
            })
            i += 1
            continue

        # 引用
        if stripped.startswith("> "):
            blocks.append({
                "object": "block",
                "type": "quote",
                "quote": {"rich_text": [{"type": "text", "text": {"content": stripped[2:]}}]},
            })
            i += 1
            continue

        # 空行跳過
        if not stripped:
            i += 1
            continue

        # 默認段落
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": stripped}}]},
        })
        i += 1

    return blocks


def push_markdown(client: NotionClient, parent_id: str, md_path: Path, title: Optional[str] = None) -> dict[str, Any]:
    text = md_path.read_text(encoding="utf-8")
    blocks = md_to_blocks(text)
    if not title:
        # 取第一個一級標題，否則用文件名
        for line in text.splitlines():
            m = re.match(r"^#\s+(.*)$", line.strip())
            if m:
                title = m.group(1)
                break
        if not title:
            title = md_path.stem
    page = client.create_page(parent_id, title, blocks)
    return page


# ═══════════════════════════════════════════
# 5. Sync：批量配置
# ═══════════════════════════════════════════
def run_sync(config_path: Path, direction: Optional[str] = None, max_blocks: Optional[int] = None, max_depth: Optional[int] = None):
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    client = NotionClient(cfg.get("token") or os.environ.get("NOTION_TOKEN"))
    mappings = cfg.get("mappings", [])
    for m in mappings:
        action = direction or m.get("direction", "pull")
        page_id = m.get("notion_page_id")
        parent_id = m.get("notion_parent_id")
        local = Path(m["local_path"]).expanduser()
        # CLI 覆盖配置
        mb = max_blocks if max_blocks is not None else m.get("max_blocks")
        md = max_depth if max_depth is not None else m.get("max_depth", 6)
        if action == "pull" and page_id:
            puller = NotionPuller(client, max_depth=md, max_blocks=mb)
            md_text = puller.pull(page_id)
            local.parent.mkdir(parents=True, exist_ok=True)
            local.write_text(md_text, encoding="utf-8")
            dna = audit("pull", page_id, str(local), "success", {"blocks": puller.block_count})
            print(f"[pull] {page_id} -> {local} （{puller.block_count} blocks） DNA:{dna}")
        elif action == "push" and parent_id:
            page = push_markdown(client, parent_id, local, title=m.get("title"))
            dna = audit("push", page["id"], str(local), "success", {"title": page.get("url")})
            print(f"[push] {local} -> {page['url']} DNA:{dna}")
        else:
            print(f"[skip] 配置缺少必要字段: {m}")


# ═══════════════════════════════════════════
# 6. CLI
# ═══════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(description="龍魂 Notion 雙向同步腳本 v1.0")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_pull = sub.add_parser("pull", help="Notion → Markdown")
    p_pull.add_argument("--page-id", required=True)
    p_pull.add_argument("-o", "--output", required=True)
    p_pull.add_argument("--max-depth", type=int, default=6)
    p_pull.add_argument("--max-blocks", type=int, default=None)

    p_push = sub.add_parser("push", help="Markdown → Notion 子頁面")
    p_push.add_argument("--parent-id", required=True)
    p_push.add_argument("-i", "--input", required=True, type=Path)
    p_push.add_argument("--title", default=None)

    p_sync = sub.add_parser("sync", help="按配置文件批量同步")
    p_sync.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    p_sync.add_argument("--direction", choices=["pull", "push"], default=None)
    p_sync.add_argument("--max-blocks", type=int, default=None, help="覆盖配置中的 max_blocks，0 表示不限制")
    p_sync.add_argument("--max-depth", type=int, default=None, help="覆盖配置中的 max_depth")

    args = parser.parse_args()
    client = NotionClient()

    if args.cmd == "pull":
        puller = NotionPuller(client, max_depth=args.max_depth, max_blocks=args.max_blocks)
        md = puller.pull(args.page_id)
        out = Path(args.output).expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md, encoding="utf-8")
        dna = audit("pull", args.page_id, str(out), "success", {"blocks": puller.block_count})
        print(f"✅ 已拉取 {args.page_id} -> {out}")
        print(f"   塊數: {puller.block_count} | DNA: {dna}")

    elif args.cmd == "push":
        page = push_markdown(client, args.parent_id, args.input, title=args.title)
        dna = audit("push", page["id"], str(args.input), "success", {"title": page.get("url")})
        print(f"✅ 已推送 {args.input} -> {page['url']}")
        print(f"   DNA: {dna}")

    elif args.cmd == "sync":
        # 命令行传入 0 视为不限制
        mb = args.max_blocks if args.max_blocks != 0 else None
        run_sync(args.config, args.direction, max_blocks=mb, max_depth=args.max_depth)


if __name__ == "__main__":
    main()
