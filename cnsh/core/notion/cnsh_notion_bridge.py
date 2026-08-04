#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · CNSH ↔ Notion 数据库桥 v1.0

让 CNSH 中文原生脚本直接读写 Notion 数据库，
实现「CNSH 运行时」与「Notion 知识库」的一体化。

核心能力：
  • 查询 Notion 数据库条目
  • 读取/拉取 Notion 页面
  • 创建/更新 Notion 页面
  • 把 Notion 条目同步为 CNSH 种子模块
  • 把 CNSH 运行结果推送回 Notion

用法（在 .cnsh 脚本中）：
  结果 = 查询数据库("3367125a9c9f808a9692f0c6752e92fa")
  打印(结果)

DNA: #龍芯⚡️2026-07-05-CNSH-NOTION-BRIDGE-v1.0
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# 兼容：requests 在某些网络环境下会挂起，统一用 curl 子进程兜底
HAS_REQUESTS = False
try:
    import requests
    HAS_REQUESTS = True
except Exception:
    pass

# ═══════════════════════════════════════════════════════════════
# 0. 路径与配置
# ═══════════════════════════════════════════════════════════════
HOME = Path.home()
LONGHUN_ROOT = Path(os.environ.get("LONGHUN_ROOT", HOME / "longhun-system"))
SYNC_DIR = HOME / ".longhun" / "notion_sync"
AUDIT_DIR = HOME / ".longhun" / "audit"
INDEX_PATH = LONGHUN_ROOT / "docs" / "notion_mirror" / "db_3367_knowledge_index.json"
SEED_DIR = LONGHUN_ROOT / "cnsh" / "notion" / "modules" / "db3367" / "seed"

for d in (SYNC_DIR, AUDIT_DIR, SEED_DIR):
    d.mkdir(parents=True, exist_ok=True)

DNA_PREFIX = "#龍芯⚡️"


# ═══════════════════════════════════════════════════════════════
# 1. DNA 与审计
# ═══════════════════════════════════════════════════════════════
def _now_iso() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat()


def _make_dna(op: str) -> str:
    ts = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    raw = f"{op}-{ts}-{uuid.uuid4().hex[:8]}"
    h = hashlib.sha256(raw.encode()).hexdigest()[:8].upper()
    return f"{DNA_PREFIX}{ts}-CNSH-NOTION-{op}-{h}"


def _audit(action: str, page_id: str, path: str, status: str, detail: dict[str, Any]):
    entry = {
        "timestamp": _now_iso(),
        "action": action,
        "page_id": page_id,
        "path": path,
        "status": status,
        "detail": detail,
        "dna": _make_dna(action),
    }
    audit_file = AUDIT_DIR / "cnsh_notion_bridge_audit.jsonl"
    audit_file.parent.mkdir(parents=True, exist_ok=True)
    with audit_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry["dna"]


# ═══════════════════════════════════════════════════════════════
# 2. Notion API 客户端
# ═══════════════════════════════════════════════════════════════
class NotionAPIClient:
    """底层 Notion API 客户端（中英文双语接口）"""

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get("NOTION_TOKEN")
        if not self.token:
            raise RuntimeError("未设置 NOTION_TOKEN 环境变量")
        self.base = "https://api.notion.com/v1"
        self.version = "2022-06-28"
        self.req_count = 0

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": self.version,
            "Content-Type": "application/json",
        }

    def _request(self, method: str, path: str, data: Optional[dict[str, Any]] = None,
                 timeout: float = 60.0, retries: int = 3) -> dict[str, Any]:
        """统一使用 curl 子进程调用 Notion API，避免 requests 网络层挂起。"""
        import subprocess
        url = f"{self.base}{path}"
        cmd = ["curl", "-s", "-X", method, "--max-time", str(int(timeout)),
               "-H", f"Authorization: Bearer {self.token}",
               "-H", f"Notion-Version: {self.version}",
               "-H", "Content-Type: application/json",
               "-w", "\nHTTP_CODE:%{http_code}", url]
        if data is not None:
            cmd.extend(["-d", json.dumps(data, ensure_ascii=False)])

        for attempt in range(retries):
            try:
                result = subprocess.run(cmd, capture_output=True, timeout=timeout + 5)
                out = result.stdout.decode("utf-8", errors="ignore")
                if "HTTP_CODE:" not in out:
                    raise RuntimeError(f"curl 未返回 HTTP_CODE: {out[:200]}")
                body, code_str = out.rsplit("HTTP_CODE:", 1)
                code = int(code_str.strip())
                if code == 429:
                    time.sleep(1 + attempt * 2)
                    continue
                if code >= 400:
                    raise RuntimeError(f"Notion API {method} {url} -> HTTP {code}: {body.strip()[:500]}")
                body = body.strip()
                if not body:
                    raise RuntimeError(f"Notion API {method} {url} -> HTTP {code} 但返回空 body")
                self.req_count += 1
                try:
                    return json.loads(body)
                except json.JSONDecodeError as je:
                    raise RuntimeError(f"Notion API JSON 解析失败 {method} {url}: {je} | body前200: {body[:200]}")
            except subprocess.TimeoutExpired:
                if attempt < retries - 1:
                    time.sleep(2)
                    continue
                raise RuntimeError(f"Notion API 超时: {method} {url}")

        raise RuntimeError(f"Notion API 重试耗尽: {method} {url}")

    def get_page(self, page_id: str) -> dict[str, Any]:
        return self._request("GET", f"/pages/{page_id}")

    def query_database(self, database_id: str, filter_obj: Optional[dict[str, Any]] = None,
                       page_size: int = 100, start_cursor: Optional[str] = None) -> dict[str, Any]:
        database_id = database_id.replace("-", "")
        payload: Dict[str, Any] = {"page_size": page_size}
        if filter_obj:
            payload["filter"] = filter_obj
        if start_cursor:
            payload["start_cursor"] = start_cursor
        return self._request("POST", f"/databases/{database_id}/query", payload)

    def create_page(self, parent_id: str, title: str, children: Optional[List[dict[str, Any]]] = None,
                    parent_type: str = "page_id") -> dict[str, Any]:
        payload = {
            "parent": {parent_type: parent_id},
            "properties": {
                "title": {"title": [{"text": {"content": title}}]}
            },
        }
        if children:
            payload["children"] = children[:100]
        page = self._request("POST", "/pages", payload)
        remaining = children[100:] if children else []
        while remaining:
            chunk = remaining[:100]
            remaining = remaining[100:]
            self._request("PATCH", f"/blocks/{page['id']}/children", {"children": chunk})
        return page

    def update_page_properties(self, page_id: str, properties: dict[str, Any]) -> dict[str, Any]:
        return self._request("PATCH", f"/pages/{page_id}", {"properties": properties})

    def get_block_children(self, block_id: str, page_size: int = 100,
                           start_cursor: Optional[str] = None) -> dict[str, Any]:
        path = f"/blocks/{block_id}/children?page_size={page_size}"
        if start_cursor:
            path += f"&start_cursor={start_cursor}"
        return self._request("GET", path)

    def append_blocks(self, block_id: str, children: List[dict[str, Any]]) -> dict[str, Any]:
        return self._request("PATCH", f"/blocks/{block_id}/children", {"children": children})


# ═══════════════════════════════════════════════════════════════
# 3. 中文命名函数（CNSH 运行时直接调用）
# ═══════════════════════════════════════════════════════════════
_客户端: Optional[NotionAPIClient] = None


def _get_client() -> NotionAPIClient:
    global _客户端
    if _客户端 is None:
        _客户端 = NotionAPIClient()
    return _客户端


def 查询数据库(数据库ID: str, 筛选: Optional[dict] = None, 页大小: int = 100,
             最大条数: Optional[int] = None) -> List[dict]:
    """查询 Notion 数据库，返回条目列表（自动翻页，可用 最大条数 限制）"""
    client = _get_client()
    results: List[dict[str, Any]] = []
    cursor = None
    while True:
        resp = client.query_database(数据库ID, filter_obj=筛选, page_size=页大小, start_cursor=cursor)
        batch = resp.get("results", [])
        results.extend(batch)
        if 最大条数 and len(results) >= 最大条数:
            return results[:最大条数]
        if not resp.get("has_more"):
            break
        cursor = resp.get("next_cursor")
    return results


def 获取页面(页面ID: str) -> dict[str, Any]:
    """获取单个 Notion 页面元数据"""
    return _get_client().get_page(页面ID)


def 创建页面(父页面ID: str, 标题: str, 内容块: Optional[List[dict]] = None) -> dict[str, Any]:
    """在指定父页面下创建子页面"""
    return _get_client().create_page(父页面ID, 标题, 内容块 or [])


def 更新页面属性(页面ID: str, 属性: dict[str, Any]) -> dict[str, Any]:
    """更新 Notion 页面属性"""
    return _get_client().update_page_properties(页面ID, 属性)


def 追加块(页面ID: str, 内容块: List[dict]) -> dict[str, Any]:
    """在页面末尾追加内容块"""
    return _get_client().append_blocks(页面ID, 内容块)


# ═══════════════════════════════════════════════════════════════
# 4. Markdown 双向转换
# ═══════════════════════════════════════════════════════════════
def _rich_text(rt: List[dict[str, Any]]) -> str:
    return "".join(t.get("plain_text", "") for t in rt)


def _block_to_md(b: dict[str, Any], depth: int = 0) -> List[str]:
    t = b.get("type")
    d = b.get(t, {})
    text = _rich_text(d.get("rich_text", []))
    indent = "  " * depth
    lines: List[str] = []

    if t == "paragraph":
        if text.strip():
            lines.append(indent + text)
    elif t and t.startswith("heading_"):
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
    elif t == "table_row":
        cells = [_rich_text(cell) for cell in d.get("cells", [])]
        lines.append(indent + "| " + " | ".join(cells) + " |")
    elif text:
        lines.append(indent + f"[{t}] {text}")
    return lines


def 拉取页面(页面ID: str, 输出路径: Optional[str] = None, 最大深度: int = 6) -> str:
    """把 Notion 页面拉取为 Markdown 字符串，可保存到文件"""
    client = _get_client()
    page = client.get_page(页面ID)
    title_obj = page.get("properties", {}).get("title", {})
    title = _rich_text(title_obj.get("title", []))

    lines = [f"# {title}", "", f"<!-- Notion page_id: {页面ID} -->",
             f"<!-- pulled_at: {_now_iso()} -->", ""]

    def fetch_children(block_id: str, depth: int):
        if depth > 最大深度:
            return
        cursor = None
        while True:
            data = client.get_block_children(block_id, page_size=100, start_cursor=cursor)
            for b in data.get("results", []):
                lines.extend(_block_to_md(b, depth))
                if b.get("has_children") and b.get("type") != "table_row":
                    fetch_children(b["id"], depth + 1)
            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")

    fetch_children(页面ID, 0)
    md = "\n".join(lines)

    if 输出路径:
        p = Path(输出路径).expanduser()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(md, encoding="utf-8")
        _audit("pull", 页面ID, str(p), "success", {"blocks": len(lines)})

    return md


def _md_to_blocks(md_text: str) -> List[dict[str, Any]]:
    blocks: List[dict[str, Any]] = []
    lines = md_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            lang = stripped[3:].strip() or "plain text"
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1
            blocks.append({
                "object": "block",
                "type": "code",
                "code": {"rich_text": [{"type": "text", "text": {"content": "\n".join(code_lines)}}],
                         "language": lang},
            })
            continue

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

        if stripped.startswith("- "):
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": stripped[2:]}}]},
            })
            i += 1
            continue

        m = re.match(r"^\d+\.\s+(.*)$", stripped)
        if m:
            blocks.append({
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": m.group(1)}}]},
            })
            i += 1
            continue

        if stripped.startswith("> "):
            blocks.append({
                "object": "block",
                "type": "quote",
                "quote": {"rich_text": [{"type": "text", "text": {"content": stripped[2:]}}]},
            })
            i += 1
            continue

        if not stripped:
            i += 1
            continue

        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": stripped}}]},
        })
        i += 1

    return blocks


def 推送页面(父页面ID: str, 文件路径: str, 标题: Optional[str] = None) -> dict[str, Any]:
    """把本地 Markdown 文件推送为 Notion 子页面"""
    p = Path(文件路径).expanduser()
    text = p.read_text(encoding="utf-8")
    blocks = _md_to_blocks(text)

    if not 标题:
        for line in text.splitlines():
            m = re.match(r"^#\s+(.*)$", line.strip())
            if m:
                标题 = m.group(1)
                break
        if not 标题:
            标题 = p.stem

    page = _get_client().create_page(父页面ID, 标题, blocks)
    _audit("push", page["id"], str(p), "success", {"title": 标题})
    return page


# ═══════════════════════════════════════════════════════════════
# 5. DB3367 与 CNSH 种子模块同步
# ═══════════════════════════════════════════════════════════════
def _safe_filename(title: str, page_id: str) -> str:
    if not title:
        title = "untitled"
    clean = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9\s_-]", "", title)
    clean = re.sub(r"\s+", "_", clean).strip("_-")[:40]
    short_id = page_id.replace("-", "")[:8]
    return f"M_{clean}_{short_id}.md"


def _generate_seed_module(entry: dict[str, Any]) -> str:
    title = entry.get("title") or "未命名条目"
    page_id = entry.get("page_id", "")
    url = entry.get("url", "")
    tags = entry.get("tags") or []
    status = entry.get("status") or ""
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    dna = f"{DNA_PREFIX}{ts}-NOTION-DB3367-SEED-{page_id[:8].upper()}-v1.0"
    tag_str = "、".join(tags) if tags else "未分类"

    return f"""# {title}｜龍魂 CNSH 种子模块

- **Notion 来源**：`{page_id}`
- **Notion URL**：{url}
- **Notion 状态**：{status or '未设置'}
- **本地状态**：🔧 接入中（种子模块）
- **DNA**：`{dna}`
- **标签**：{tag_str}

---

## 一句话

{title} 是龍魂知识库中标记为「有代码」的条目，待进一步填充理论、实现与 CNSH 语义映射。

## 核心概念

> 【待回填：是什么 · 从哪来 · 解决什么问题 · 类比是什么】

## 核心公式 / 关键语法

```python
# 【待回填：把核心代码/伪代码/公式写在这里】
pass
```

## 龍魂对齐

- **应用场景**：【待填】
- **对接模块**：【待填】
- **CNSH 变量命名**：
  - `xxx` → `【待填】`

## Python 可运行片段（待实现）

```python
def 待实现():
    pass

if __name__ == '__main__':
    待实现()
```

## 待回填事项

- [ ] 拉取 Notion 原页 [{title}]({url}) 的完整内容
- [ ] 补充核心定义与公式
- [ ] 补充 CNSH 语义映射
- [ ] 实现可运行 Python 片段
- [ ] 与 `longhun-math-formula-core` 注册函数

---

**签章**：`{dna}` · UID9622
"""


def 同步DB3367种子模块(数据库ID: str = "3367125a9c9f808a9692f0c6752e92fa") -> dict[str, Any]:
    """
    从 Notion DB3367 拉取「有代码」条目，生成/更新 CNSH 种子模块。
    返回同步统计。
    """
    if not INDEX_PATH.exists():
        raise RuntimeError(f"本地索引不存在: {INDEX_PATH}")

    data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    entries = data.get("entries", [])

    # 以本地索引为主，同时把 Notion 最新状态回写
    # 先拉取 Notion 全部条目构建状态映射（最多 500 条，足够覆盖当前库）
    notion_entries = 查询数据库(数据库ID, 最大条数=500)
    notion_status_map = {}
    for e in notion_entries:
        pid = e.get("id", "").replace("-", "")
        props = e.get("properties", {})
        status_value = ""
        for prop in props.values():
            if prop.get("type") == "status" and prop.get("status"):
                status_value = prop["status"].get("name", "")
                break
            elif prop.get("type") == "select" and prop.get("select"):
                status_value = prop["select"].get("name", "")
                break
        if status_value:
            notion_status_map[pid] = status_value

    generated = 0
    updated = 0
    skipped = 0

    for e in entries:
        if e.get("lh_category") != "有代码":
            continue
        page_id = e.get("page_id", "").replace("-", "")
        title = e.get("title") or "untitled"
        filename = _safe_filename(title, page_id)
        path = SEED_DIR / filename

        # 更新 Notion 最新状态到索引
        if page_id in notion_status_map:
            e["status"] = notion_status_map[page_id]

        if path.exists():
            # 已存在：如果索引里没有路径就补录
            if not e.get("lh_module_path"):
                e["lh_module_path"] = str(path)
                updated += 1
            else:
                skipped += 1
            continue

        content = _generate_seed_module(e)
        path.write_text(content, encoding="utf-8")
        e["lh_module_path"] = str(path)
        e["status"] = "🔧 接入中"
        generated += 1

    INDEX_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    result = {
        "generated": generated,
        "updated": updated,
        "skipped": skipped,
        "total_entries": len(entries),
        "seed_dir": str(SEED_DIR),
        "dna": _make_dna("SYNC-DB3367-SEED"),
    }
    _audit("sync_db3367_seed", 数据库ID, str(SEED_DIR), "success", result)
    return result


# ═══════════════════════════════════════════════════════════════
# 6. 自检
# ═══════════════════════════════════════════════════════════════
def 自检() -> dict[str, Any]:
    """检查 Notion Token、网络、索引文件是否就绪"""
    token = os.environ.get("NOTION_TOKEN")
    checks = {
        "token_set": bool(token),
        "token_length": len(token) if token else 0,
        "requests_available": HAS_REQUESTS,
        "index_exists": INDEX_PATH.exists(),
        "seed_dir_exists": SEED_DIR.exists(),
        "audit_dir_exists": AUDIT_DIR.exists(),
    }
    return checks


def selftest():
    print("=" * 70)
    print("🐉 CNSH ↔ Notion 数据库桥 · 自检")
    print("=" * 70)
    checks = 自检()
    for k, v in checks.items():
        print(f"  {k}: {v}")
    print("=" * 70)
    print("✅ 自检完成")
    print(f"   DNA: #龍芯⚡️2026-07-05-CNSH-NOTION-BRIDGE-v1.0")
    print("=" * 70)


# ═══════════════════════════════════════════════════════════════
# 7. 英文别名（方便直接 Python 调用）
# ═══════════════════════════════════════════════════════════════
query_database = 查询数据库
get_page = 获取页面
create_page = 创建页面
update_page_properties = 更新页面属性
append_blocks = 追加块
pull_page = 拉取页面
push_markdown = 推送页面
sync_db3367_seed_modules = 同步DB3367种子模块
self_check = 自检


if __name__ == "__main__":
    selftest()
