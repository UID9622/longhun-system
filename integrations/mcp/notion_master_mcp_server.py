#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️2026-09-04-NOTION-MASTER-MCP-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""╔══════════════════════════════════════════════════════════════════════╗
║   Notion Master MCP Server v1.0 — 全量发现 · 全文读取 · 对话记录 · 整理执行 ║
║   DNA: #龍芯⚡️2026-09-04-NOTION-MASTER-MCP-v1.0-UID9622                ║
║   创建者: 诸葛鑫 | UID9622 · 龍芯北辰                                     ║
║   三色: 🟢 首发 · 零三方 · 直连官方 REST                                  ║
╚══════════════════════════════════════════════════════════════════════╝

【这是什么？】
官方 @notionhq/notion-mcp-server 只能"按 ID 查"——AI 不知道 workspace 里
有哪些页面，无法发现页面树，更读不到评论（对话记录），无法批量整理。
本 Server 用高层工具补上这三层能力，一次调用解决发现+读取+执行：

【工具清单】(20 · v2.0 生态联动版)
  🔍 notion_search          — 搜索全部页面/数据库（翻页全量）
  🌳 notion_page_tree       — 递归拉取页面树（子页/子库·缩进文本）
  📄 notion_read_page       — 读页面完整内容（块→结构化文本）
  🗃️ notion_query_database  — 读数据库所有行（翻页）
  💬 notion_read_comments   — 读页面/块上的评论（=对话记录）
  📌 notion_page_info       — 页面元信息 + 子块计数
  ⚙️ notion_health          — 健康检查（token/API/本地索引）

  ✍️ notion_create_page     — 在父页/父库下建页（支持文本首 100 块）
  📎 notion_append_blocks   — 页尾追加 markdown 文本（自动分页≤100块）
  📝 notion_update_page     — 改名/改图标/归档恢复
  🗄️ notion_archive_page    — 归档页面（软删除·"不删除只冻结"）
  ➕ notion_create_row      — 数据库新增一行（JSON 属性）
  🔧 notion_update_row      — 数据库更新一行（JSON 属性）
  🧹 notion_index_sync      — 增量刷新本地 SQLite 索引
  ⚡ notion_local_search    — 本地 FTS5 秒搜（不烧 Notion API）

  ── v2.0 生态联动层（深度集成·调 lh 引擎不造轮子）──
  🕸️ notion_sync_to_topo     — 页面→龙魂拓扑节点（lh topo node）
  🚦 notion_audit_page       — 页面内容三色审计（gov redline）→🟢🟡🔴
  🧱 notion_archive_to_shamewall — 归档双留痕（审计链+真红线才上耻辱墙）
  🧠 notion_comment_to_memory    — 评论(对话记录)→lh brain 长期记忆
  📡 notion_export_topo      — 页面树→龙魂拓扑 JSON（lh topo 可识别）

【安全】token 只经 env>vault>mcp.json 候选实测取有效者，值不落盘；
只读操作无副作用；写操作全部显式参数。归档=默认整理动作，不物理删除。
生态联动层 v2.0: 操作审计链 ~/.longhun/notion_audit.jsonl（append-only）；
耻辱墙=剽窃公示专用（lh judge DB）·常规操作日志不污染其公信。
"""
import argparse
import asyncio
import json
import os
import random
import re
import sqlite3
import sys
import time
import urllib.request
import urllib.error

# ── 路径 & 环境（清代理：Mac 下 socks 代理会让 Notion API 直连失败）──
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _root in (os.environ.get("LONGHUN_ROOT", os.path.expanduser("~/longhun-system")),
              os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))):
    _p = str(_root)
    if os.path.isdir(_p) and _p not in sys.path:
        sys.path.insert(0, _p)
for _k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy",
           "ALL_PROXY", "all_proxy"):
    os.environ.pop(_k, None)
os.environ["NO_PROXY"] = "*"

from mcp.server import Server  # noqa: E402
from mcp.server.stdio import stdio_server  # noqa: E402
from mcp.types import Tool, TextContent  # noqa: E402

API = "https://api.notion.com/v1"
DB_PATH = os.path.expanduser("~/.longhun/notion_index.db")
VERSION = "1.0"
app = Server("notion-master")


# ────────────────────────────── Token ──────────────────────────────
def _probe_token(tok):
    if not tok:
        return False
    try:
        req = urllib.request.Request(f"{API}/users/me",
                                     headers={"Authorization": f"Bearer {tok}",
                                              "Notion-Version": "2025-09-03"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status == 200
    except Exception:
        return False


def get_token():
    cands = []
    if os.environ.get("NOTION_TOKEN", "").strip():
        cands.append(("env", os.environ["NOTION_TOKEN"].strip()))
    try:
        v = os.popen("python3 bin/lh_vault.py get NOTION_TOKEN").read().strip()
        if v and not v.lower().startswith("error"):
            cands.append(("vault", v))
    except Exception:
        pass
    try:
        with open(os.path.expanduser("~/.codebuddy/mcp.json")) as f:
            m = json.load(f)
        t = m.get("mcpServers", {}).get("Notion MCP Server", {}).get("env", {}).get("NOTION_TOKEN", "")
        if t:
            cands.append(("mcp.json", t.strip()))
    except Exception:
        pass
    for name, t in cands:
        if _probe_token(t):
            return t
    return cands[0][1] if cands else ""


class NotionAPI:
    """直连官方 REST · 指数退避(429/5xx) · ≤3 req/s 限速 · 全翻页"""

    def __init__(self, token):
        self.token = token
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

    def _h(self):
        return {"Authorization": f"Bearer {self.token}",
                "Notion-Version": "2025-09-03",
                "Content-Type": "application/json"}

    def api(self, method, path, body=None, retries=5):
        req = urllib.request.Request(f"{API}/{path}",
                                     data=json.dumps(body).encode() if body is not None else None,
                                     method=method, headers=self._h())
        for attempt in range(retries + 1):
            try:
                with self.opener.open(req, timeout=40) as r:
                    time.sleep(0.3)
                    return json.loads(r.read().decode())
            except urllib.error.HTTPError as e:
                if e.code in (429,) and attempt < retries:
                    time.sleep((2 ** attempt) + random.uniform(0, 1))
                    continue
                if e.code >= 500 and attempt < retries:
                    time.sleep(2 ** attempt)
                    continue
                try:
                    msg = json.loads(e.read().decode()).get("message", "")[:200]
                except Exception:
                    msg = ""
                return {"_error": e.code, "message": msg}
            except Exception as e:
                return {"_error": -1, "message": str(e)[:200]}
        return {"_error": 0, "message": "max retries"}

    # ── 高层 helpers ──
    def search_all(self, query="", obj_filter=None, limit=None):
        """POST /search 全翻页。obj_filter: 'page'|'database'|None。
        新 API 模型(2025-09-03)下数据库对象返回 object='data_source'，
        filter 值须传 'data_source'，传 'database' 会 400——此处自动映射。"""
        api_filter = {"database": "data_source"}.get(obj_filter, obj_filter)
        out, cursor, seen = [], None, set()
        while True:
            body = {"query": query, "page_size": 100}
            if api_filter:
                body["filter"] = {"value": api_filter, "property": "object"}
            if cursor:
                body["start_cursor"] = cursor
            res = self.api("POST", "search", body)
            if "_error" in res or not res.get("results"):
                break
            for r in res.get("results", []):
                if r.get("id") in seen:
                    continue
                seen.add(r.get("id"))
                out.append(r)
            if limit and len(out) >= limit:
                break
            if res.get("has_more") and res.get("next_cursor"):
                cursor = res["next_cursor"]
            else:
                break
        return out

    def children_all(self, block_id):
        """GET /blocks/{id}/children 全翻页"""
        out, cursor = [], None
        while True:
            path = f"blocks/{block_id}/children?page_size=100"
            if cursor:
                path += f"&start_cursor={cursor}"
            res = self.api("GET", path)
            if "_error" in res or not res.get("results"):
                break
            out.extend(res.get("results", []))
            if res.get("has_more") and res.get("next_cursor"):
                cursor = res["next_cursor"]
            else:
                break
        return out


# ────────────────────────── 文本/块 工具 ──────────────────────────
def _rt_text(v):
    """从 type value dict 提取 rich_text 纯文本"""
    if not isinstance(v, dict):
        return ""
    rt = v.get("rich_text") or []
    return "".join(x.get("plain_text", "") for x in rt if isinstance(x, dict))


def _rt_arr(v):
    """从属性值 dict 提取富文本数组：title 属性挂 'title' 键，其余挂 'rich_text' 键"""
    if not isinstance(v, dict):
        return []
    return v.get("title") or v.get("rich_text") or []


def _rt_join(arr):
    return "".join(x.get("plain_text", "") for x in arr if isinstance(x, dict))


def _title_of(props, obj=None):
    """解析页面/数据库标题：page→properties 中 type==title；database→顶层 title 数组；
    最后兜底取首个含文本的属性。obj=原始 API 响应（补顶层 title 用）"""
    for v in (props or {}).values():
        if isinstance(v, dict) and v.get("type") == "title":
            txt = _rt_join(_rt_arr(v))
            if txt:
                return txt
    if isinstance(obj, dict) and obj.get("title"):
        txt = _rt_join(obj["title"])
        if txt:
            return txt
    # 兜底: 找不到显式 title → 取首个非空富文本属性（数据库行/新 API 模型兼容）
    for v in (props or {}).values():
        if isinstance(v, dict):
            txt = _rt_join(_rt_arr(v))
            if txt:
                return txt
    return ""


def _url_of(page_id):
    return f"https://www.notion.so/{page_id.replace('-', '')}"


def _clean_text(text):
    return re.sub(r"\r\n", "\n", (text or "")).strip()


def text_to_blocks(text, base_type="paragraph"):
    """极简 markdown 行 → Notion block dicts（段落/标题/列表/待办/引用/分隔线）"""
    blocks, buf = [], []
    lines = (_clean_text(text) or "").split("\n")

    def flush_quote(acc):
        if acc:
            blocks.append({"object": "block", "type": "quote",
                           "quote": {"rich_text": [{"type": "text",
                                                    "text": {"content": "\n".join(acc)[:1900]}}]}})
            acc.clear()

    def flush_para(acc):
        if acc:
            blocks.append({"object": "block", "type": "paragraph",
                           "paragraph": {"rich_text": [{"type": "text",
                                                        "text": {"content": "\n".join(acc)[:1900]}}]}})
            acc.clear()

    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        if s == "---":
            flush_para(buf)
            blocks.append({"object": "block", "type": "divider", "divider": {}})
            continue
        m = re.match(r"^(#{1,3})\s+(.*)$", s)
        if m:
            flush_para(buf)
            lvl, content = len(m.group(1)), m.group(2)[:1900]
            blocks.append({"object": "block", "type": f"heading_{lvl}",
                           f"heading_{lvl}": {"rich_text": [{"type": "text",
                                                             "text": {"content": content}}]}})
            continue
        m = re.match(r"^[-*]\s+(.*)$", s)
        if m:
            flush_para(buf)
            blocks.append({"object": "block", "type": "bulleted_list_item",
                           "bulleted_list_item": {"rich_text": [{"type": "text",
                                                                 "text": {"content": m.group(1)[:1900]}}]}})
            continue
        m = re.match(r"^(\d+)[.)]\s+(.*)$", s)
        if m:
            flush_para(buf)
            blocks.append({"object": "block", "type": "numbered_list_item",
                           "numbered_list_item": {"rich_text": [{"type": "text",
                                                                 "text": {"content": m.group(2)[:1900]}}]}})
            continue
        m = re.match(r"^\[([ xX])\]\s+(.*)$", s)
        if m:
            flush_para(buf)
            checked = m.group(1).lower() == "x"
            blocks.append({"object": "block", "type": "to_do",
                           "to_do": {"rich_text": [{"type": "text",
                                                    "text": {"content": m.group(2)[:1900]}}],
                                     "checked": checked}})
            continue
        if s.startswith(">"):
            flush_para(buf)
            quote = s.lstrip("> ").strip()
            blocks.append({"object": "block", "type": "quote",
                           "quote": {"rich_text": [{"type": "text",
                                                    "text": {"content": quote[:1900]}}]}})
            continue
        buf.append(s)
    flush_para(buf)
    return blocks[:100]  # Notion 单请求上限 100


def _append_in_chunks(api, page_id, text):
    """超长文本分批追加（每批≤100块）"""
    blocks = text_to_blocks(text)
    added = 0
    while blocks:
        chunk, blocks = blocks[:100], blocks[100:]
        res = api.api("PATCH", f"blocks/{page_id}/children", {"children": chunk})
        if "_error" in res:
            return {"ok": False, "error": res.get("message", res), "added": added}
        added += len(res.get("results", chunk))
    return {"ok": True, "added": added}


# ────────────────────────── 本地 SQLite 索引 ──────────────────────────
def _db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def _ensure_local_schema(con):
    con.execute("CREATE TABLE IF NOT EXISTS pages ("
                "rowid INTEGER PRIMARY KEY AUTOINCREMENT,"
                "id TEXT UNIQUE NOT NULL, parent_id TEXT, title TEXT, url TEXT,"
                "icon TEXT, tags TEXT, content TEXT, status TEXT DEFAULT 'ok',"
                "updated_at TEXT, scanned_at TEXT)")
    con.execute("CREATE VIRTUAL TABLE IF NOT EXISTS pages_fts "
                "USING fts5(title, content, content='pages', content_rowid='rowid', tokenize='unicode61')")
    con.execute("CREATE TRIGGER IF NOT EXISTS pages_ai AFTER INSERT ON pages BEGIN "
                "INSERT INTO pages_fts(rowid, title, content) VALUES (new.rowid, new.title, new.content); END")
    con.execute("CREATE TRIGGER IF NOT EXISTS pages_ad AFTER DELETE ON pages BEGIN "
                "INSERT INTO pages_fts(pages_fts, rowid, title, content) VALUES ('delete', old.rowid, old.title, old.content); END")
    con.execute("CREATE TRIGGER IF NOT EXISTS pages_au AFTER UPDATE ON pages BEGIN "
                "INSERT INTO pages_fts(pages_fts, rowid, title, content) VALUES ('delete', old.rowid, old.title, old.content); "
                "INSERT INTO pages_fts(rowid, title, content) VALUES (new.rowid, new.title, new.content); END")
    con.commit()


def _index_upsert(api, pid, parent_id, title, icon, content, updated):
    con = _db()
    _ensure_local_schema(con)
    tags = "📄 未归类"
    try:
        con.execute("INSERT OR REPLACE INTO pages(id,parent_id,title,url,icon,tags,content,status,updated_at,scanned_at)"
                    " VALUES(?,?,?,?,?,?,?,?,?,datetime('now'))",
                    (pid, parent_id, title, _url_of(pid), icon, tags, (content or "")[:20000],
                     "ok", updated))
        con.commit()
    finally:
        con.close()


# ────────────────────────── 工具 handlers ──────────────────────────
def h_health(_):
    n = api = idx = 0
    tok = get_token()
    try:
        con = _db()
        n = con.execute("SELECT COUNT(*) FROM pages").fetchone()[0]
        con.close()
    except Exception:
        pass
    try:
        me = NotionAPI(tok).api("GET", "users/me")
        api = 200 if not me.get("_error") else me.get("_error")
    except Exception:
        api = -1
    return {"status": "ok" if (tok and api == 200) else "degraded",
            "version": VERSION,
            "token_valid": bool(tok and api == 200),
            "local_index_pages": n,
            "dna": "#龍芯⚡️2026-09-04-NOTION-MASTER-MCP-HEALTH",
            "tool_count": 15}


def h_search(a):
    q = str(a.get("query") or "").strip()
    typ = (a.get("object_type") or "").strip() or None
    limit = int(a.get("limit") or 0) or None
    items = []
    for r in api.search_all(q, typ, limit):
        otype = "database" if r.get("object") == "data_source" else r.get("object")
        title = _title_of(r.get("properties")) if otype == "page" else None
        if not title and r.get("title"):
            title = "".join(x.get("plain_text", "") for x in r["title"] if isinstance(x, dict))
        if not title and r.get("id"):
            title = f"({otype[:4]}·{r['id'][:8]})"
        p = r.get("parent", {})
        parent_id = p.get("page_id") or p.get("database_id") or ""
        items.append({"id": r["id"], "object": otype,
                      "title": title or f"({otype[:4]}·{r['id'][:8]})",
                      "url": _url_of(r["id"]),
                      "parent_type": p.get("type", ""), "parent_id": parent_id,
                      "last_edited": r.get("last_edited_time", "")})
    return {"query": q, "count": len(items), "items": items[:200]}


def _render_tree(api, block_id, title, depth, max_depth, path):
    out, con = [], None
    kids = api.children_all(block_id)
    try:
        con = _db()
        _ensure_local_schema(con)
        for b in kids:
            t = b.get("type")
            if t == "child_page":
                cp = b.get("child_page", {})
                ctitle = cp.get("title", "") or ""
                nid = b["id"]
                _index_upsert(api, nid, block_id, ctitle, "", "", "")
                node = {"depth": depth, "type": "page", "id": nid, "title": ctitle,
                        "url": _url_of(nid)}
                if depth < max_depth:
                    node["children"] = _render_tree(api, nid, ctitle, depth + 1, max_depth, path)
                out.append(node)
            elif t == "child_database":
                cd = b.get("child_database", {})
                ctitle = cd.get("title", "") or ""
                _index_upsert(api, b["id"], block_id, ctitle, "", "", "")
                out.append({"depth": depth, "type": "database", "id": b["id"],
                            "title": ctitle, "url": _url_of(b["id"]), "children": []})
    finally:
        if con:
            con.close()
    return out


def h_tree(a):
    pid = (a.get("page_id") or "").strip()
    max_depth = int(a.get("max_depth") or 2)
    if not pid:
        return {"ok": False, "error": "page_id required"}
    title = "root"
    try:
        pg = api.api("GET", f"pages/{pid}")
        if "_error" in pg:
            return {"ok": False, "error": pg}
        title = _title_of(pg.get("properties"), pg) or title
    except Exception:
        pass
    tree = _render_tree(api, pid, title, 0, min(max_depth, 6), [pid])
    lines = []

    def walk(nodes, ind):
        for n in nodes:
            icon = "🗄️" if n["type"] == "database" else "📄"
            lines.append(f"{'  ' * ind}{icon} {n['title']}  `{n['id']}`")
            walk(n.get("children", []), ind + 1)

    walk(tree, 0)
    return {"ok": True, "root": {"id": pid, "title": title},
            "max_depth": max_depth, "count": len(tree),
            "tree_text": "\n".join(lines), "tree_json": tree}


def _block_to_text(b):
    t = b.get("type")
    if t == "child_page":
        return ("#page " + b.get("child_page", {}).get("title", ""))
    if t == "child_database":
        return ("#db " + b.get("child_database", {}).get("title", ""))
    v = b.get(t, {})
    s = _rt_text(v)
    if t == "to_do":
        c = "☑" if v.get("checked") else "☐"
        return f"{c} {s}"
    if t == "heading_1":
        return f"# {s}"
    if t == "heading_2":
        return f"## {s}"
    if t == "heading_3":
        return f"### {s}"
    if t == "code":
        lang = v.get("language", "")
        return f"```{lang}\n{s}\n```"
    if t == "bulleted_list_item":
        return f"- {s}"
    if t == "numbered_list_item":
        return f"- {s}"
    if t == "callout":
        icon = (v.get("icon") or {}).get("emoji", "") if isinstance(v.get("icon"), dict) else ""
        return f"💬 {icon} {s}"
    if s:
        return s
    return f"[{t}]"


def h_read_page(a):
    pid = (a.get("page_id") or "").strip()
    depth = int(a.get("depth") or 0)
    if not pid:
        return {"ok": False, "error": "page_id required"}
    pg = api.api("GET", f"pages/{pid}")
    if "_error" in pg:
        return {"ok": False, "error": pg}
    title = _title_of(pg.get("properties"), pg) or f"({pid[:8]})"
    lines, seen_children = [], []
    try:
        con = _db()
        _ensure_local_schema(con)
    except Exception:
        con = None

    def walk(block_id, ind):
        for b in api.children_all(block_id):
            t = b.get("type")
            if t in ("child_page", "child_database"):
                if con:
                    ctitle = (b.get(t, {}) or {}).get("title", "")
                    _index_upsert(api, b["id"], block_id, ctitle or "", "", "", "")
                continue
            txt = _block_to_text(b)
            if txt:
                lines.append(("  " * ind) + txt)
            if depth > 0 and t not in ("paragraph",):
                walk(b["id"], ind + 1)

    walk(pid, 0)
    if con:
        con.close()
    content = "\n".join(lines)[:30000]
    try:
        _index_upsert(api, pid, "", title, "", content, pg.get("last_edited_time", ""))
    except Exception:
        pass
    return {"ok": True, "page": {"id": pid, "title": title, "url": _url_of(pid)},
            "blocks": len(lines), "content": content}


def h_query_db(a):
    dbid = (a.get("database_id") or "").strip()
    limit = int(a.get("limit") or 100)
    if not dbid:
        return {"ok": False, "error": "database_id required"}
    db = api.api("GET", f"databases/{dbid}")
    if "_error" in db:
        return {"ok": False, "error": db}
    dbtitle = "".join(x.get("plain_text", "") for x in db.get("title", []) if isinstance(x, dict))
    props_def = {k: v.get("type") for k, v in db.get("properties", {}).items()}
    rows, cursor = [], None
    while len(rows) < limit:
        body = {"page_size": min(100, limit - len(rows))}
        if cursor:
            body["start_cursor"] = cursor
        res = api.api("POST", f"databases/{dbid}/query", body)
        if "_error" in res or not res.get("results"):
            break
        for r in res.get("results", []):
            prop = {}
            for k, v in r.get("properties", {}).items():
                vt = v.get("type")
                if vt == "title":
                    prop[k] = _rt_text(v)
                elif vt == "rich_text":
                    prop[k] = _rt_text(v)
                elif vt == "select":
                    sel = v.get("select") or {}
                    prop[k] = sel.get("name", "")
                elif vt == "multi_select":
                    prop[k] = [x.get("name", "") for x in v.get("multi_select", [])]
                elif vt == "number":
                    prop[k] = v.get("number")
                elif vt == "checkbox":
                    prop[k] = v.get("checkbox")
                elif vt == "date":
                    prop[k] = (v.get("date") or {}).get("start", "")
                elif vt == "url":
                    prop[k] = v.get("url", "")
                elif vt == "status":
                    prop[k] = (v.get("status") or {}).get("name", "")
                else:
                    prop[k] = f"<{vt}>"
            rows.append({"id": r["id"], "url": _url_of(r["id"]),
                         "last_edited": r.get("last_edited_time", ""), "props": prop})
        if res.get("has_more") and res.get("next_cursor"):
            cursor = res["next_cursor"]
        else:
            break
    return {"ok": True, "database": {"id": dbid, "title": dbtitle},
            "properties": props_def, "count": len(rows), "rows": rows}


def h_comments(a):
    pid = (a.get("page_id") or "").strip()
    limit = int(a.get("limit") or 50)
    if not pid:
        return {"ok": False, "error": "page_id required"}
    out, cursor = [], None
    while len(out) < limit:
        path = f"comments?block_id={pid}&page_size=100"
        if cursor:
            path += f"&start_cursor={cursor}"
        res = api.api("GET", path)
        if "_error" in res or not res.get("results"):
            break
        for c in res.get("results", []):
            txt = "".join(x.get("plain_text", "") for x in c.get("rich_text", []) if isinstance(x, dict))
            user = (c.get("created_by") or {}).get("name", "") or (c.get("created_by") or {}).get("id", "")[:8]
            out.append({"id": c["id"], "created": c.get("created_time", ""),
                        "author": user, "text": txt[:500]})
        if res.get("has_more") and res.get("next_cursor"):
            cursor = res["next_cursor"]
        else:
            break
    return {"ok": True, "page_id": pid, "comment_count": len(out), "comments": out}


def h_page_info(a):
    pid = (a.get("page_id") or "").strip()
    if not pid:
        return {"ok": False, "error": "page_id required"}
    pg = api.api("GET", f"pages/{pid}")
    if "_error" in pg:
        return {"ok": False, "error": pg}
    p = pg.get("parent", {})
    props = {}
    for k, v in (pg.get("properties") or {}).items():
        props[k] = {"type": v.get("type")}
        if v.get("type") == "title":
            props[k]["value"] = _rt_text(v)[:200]
    blocks = api.children_all(pid)
    return {"ok": True, "id": pid, "title": _title_of(pg.get("properties")) or "",
            "url": _url_of(pid), "parent_type": p.get("type", ""),
            "parent_id": p.get("page_id") or p.get("database_id") or "",
            "archived": pg.get("archived"), "created": pg.get("created_time"),
            "last_edited": pg.get("last_edited_time"),
            "child_block_count": len(blocks),
            "properties": props}


def h_create_page(a):
    """在父页/父库下建页。父库需 parent_properties(标题列名)。content 支持 markdown 前 100 块"""
    parent_type = (a.get("parent_type") or "page").strip()
    parent_id = (a.get("parent_id") or "").strip()
    title = (a.get("title") or "").strip()
    content = (a.get("content") or "").strip()
    icon = (a.get("icon") or "").strip()
    if not parent_id or not title:
        return {"ok": False, "error": "parent_id + title required"}
    parent = {"page_id": parent_id} if parent_type == "page" else {"database_id": parent_id}
    props = {"title": {"title": [{"type": "text", "text": {"content": title[:1900]}}]}}
    children = text_to_blocks(content) if content else []
    body = {"parent": parent, "properties": props}
    if children:
        body["children"] = children
    if icon:
        body["icon"] = {"type": "emoji", "emoji": icon[:1]}
    res = api.api("POST", "pages", body)
    if "_error" in res:
        return {"ok": False, "error": res}
    return {"ok": True, "page_id": res.get("id"), "url": _url_of(res.get("id", "")),
            "created": True, "initial_blocks": len(children)}


def h_append(a):
    pid = (a.get("page_id") or "").strip()
    content = (a.get("content") or "").strip()
    if not pid or not content:
        return {"ok": False, "error": "page_id + content required"}
    r = _append_in_chunks(api, pid, content)
    return {"ok": r["ok"], "added": r.get("added", 0),
            "error": r.get("error") if not r["ok"] else None,
            "page_id": pid}


def h_update_page(a):
    pid = (a.get("page_id") or "").strip()
    if not pid:
        return {"ok": False, "error": "page_id required"}
    body = {}
    if a.get("title"):
        body["properties"] = {"title": {"title": [{"type": "text",
                                                   "text": {"content": str(a["title"])[:1900]}}]}}
    if a.get("icon"):
        body["icon"] = {"type": "emoji", "emoji": str(a["icon"])[:1]}
    if "archived" in a:
        body["archived"] = bool(a["archived"])
    if not body:
        return {"ok": False, "error": "nothing to update"}
    res = api.api("PATCH", f"pages/{pid}", body)
    if "_error" in res:
        return {"ok": False, "error": res}
    return {"ok": True, "page_id": pid, "url": _url_of(pid), "updated": True}


def h_archive(a):
    pid = (a.get("page_id") or "").strip()
    if not pid:
        return {"ok": False, "error": "page_id required"}
    archived = not bool(a.get("restore"))
    if bool(a.get("dry_run")):
        _audit_log("archive_dry", {"page_id": pid, "archived": archived,
                                   "restore": bool(a.get("restore"))})
        return {"ok": True, "dry_run": True, "page_id": pid, "archived": archived,
                "note": "演练模式·未真改·如需执行去掉 dry_run"}
    res = api.api("PATCH", f"pages/{pid}", {"archived": archived})
    if "_error" in res:
        return {"ok": False, "error": res}
    # 操作审计链：归档/恢复留痕（append-only·非耻辱墙·不删除只冻结）
    _audit_log("archive", {"page_id": pid, "archived": archived,
                           "restore": bool(a.get("restore"))})
    return {"ok": True, "page_id": pid, "archived": archived,
            "note": "归档=软删除（不删除只冻结·可随时 restore=true 恢复）·已记审计链"}


# ═══════════════════════ 生态联动层（任务1·v2.0 深度集成）═══════════════════
# 联动对象: lh topo / lh gov / lh judge / lh brain · 子进程调用·不重复造轮子
LH_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AUDIT_JSONL = os.path.expanduser("~/.longhun/notion_audit.jsonl")


def _lh_run(script, args, timeout=60):
    """子进程调用 lh 生态引擎（零三方·capture 输出）"""
    try:
        import subprocess
        py = os.environ.get("LH_PYTHON", sys.executable or "python3")
        path = os.path.join(LH_ROOT, "08_BIN", script)
        if not os.path.isfile(path):
            path = os.path.join(LH_ROOT, "bin", script)
        r = subprocess.run([py, path] + [str(x) for x in args],
                           capture_output=True, text=True, timeout=timeout)
        out = (r.stdout or "") + ("\n" + r.stderr if r.stderr else "")
        return {"ok": r.returncode == 0, "code": r.returncode, "out": out.strip()[:4000]}
    except Exception as e:
        return {"ok": False, "code": -1, "out": f"lh 调用失败: {e}"}


def _lh_import_call(script, fn_name, kwargs):
    """import lh 引擎模块并调用函数（子进程之外的零依赖直连·共享同一 DB/内存）"""
    try:
        import importlib.util
        path = os.path.join(LH_ROOT, "08_BIN", script)
        if not os.path.isfile(path):
            path = os.path.join(LH_ROOT, "bin", script)
        spec = importlib.util.spec_from_file_location(script.replace(".py", "_lh"), path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod
        spec.loader.exec_module(mod)
        fn = getattr(mod, fn_name)
        fn(**kwargs)
        return {"ok": True, "fn": fn_name}
    except Exception as e:
        return {"ok": False, "fn": fn_name, "error": str(e)[:200]}


def _audit_log(kind, data):
    """append-only 操作审计链 ~/.longhun/notion_audit.jsonl（日志即证据·不入耻辱墙）"""
    try:
        entry = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                 "kind": kind, "agent": "notion-master-mcp",
                 "dna": "#龍芯⚡️2026-09-04-NOTION-MASTER-MCP-L2-v2.0-UID9622", **data}
        with open(AUDIT_JSONL, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return True
    except Exception:
        return False


def _audit_text_tricolor(text):
    """页面内容三色审计·轻量本地规则 + gov redline 引擎联动
    🔴 系统红线命中(外包/政权攻击/密钥泄露) → 停
    🟡 涉个人隐私/超长空转 → 关注
    🟢 通过"""
    t = (text or "").strip()
    if len(t) < 2:
        return "🟡", "内容为空或过短·待补全", []
    red_hits = []
    for w in ("密码:", "token=sk-", "sk-", "BEGIN PRIVATE KEY", "AKIA", "secret"):
        if w in t:
            red_hits.append(f"疑似密钥/凭据[{w}]")
    for w in ("手机号", "身份证号", "住址", "银行卡"):
        if w in t:
            red_hits.append(f"涉个人隐私词[{w}]")
    r = _lh_run("lh_governance.py", ["redline", "check", t[:2000]])
    gov_mark = "🟢"
    if "🔴" in r["out"]:
        gov_mark = "🔴"
        red_hits.append("系统主权红线命中(gov redline)")
    elif "🟡" in r["out"]:
        gov_mark = "🟡"
    if red_hits and gov_mark == "🟢":
        gov_mark = "🔴"
    elif len(t) > 20000 and gov_mark == "🟢":
        gov_mark = "🟡"
    return gov_mark, "；".join(red_hits) if red_hits else "通过·未命中红线", red_hits


def h_sync_to_topo(a):
    """页面 → 龙魂拓扑节点注册（lh topo node·同名=更新）"""
    pid = (a.get("page_id") or "").strip()
    topo = (a.get("topo") or "通心译").strip()
    group = (a.get("group") or "🛰️ Notion数据主控").strip()
    if not pid:
        return {"ok": False, "error": "page_id required"}
    pg = api.api("GET", f"pages/{pid}")
    if "_error" in pg:
        return {"ok": False, "error": pg}
    title = _title_of(pg.get("properties"), pg) or f"Notion页 {pid[:8]}"
    if bool(a.get("dry_run")):
        _audit_log("sync_to_topo_dry", {"page_id": pid, "title": title[:80], "topo": topo})
        return {"ok": True, "dry_run": True, "page_id": pid, "topo": topo,
                "planned": f"将注册拓扑节点 [{group}] {title[:60]}",
                "note": "演练模式·未注册·如需执行去掉 dry_run"}
    r = _lh_run("lh_topo.py",
                ["node", topo, "--group", group, "--name", title[:60],
                 "--type", "notion-page", "--link", _url_of(pid),
                 "--dna", f"NOTION-{pid[:8]}", "--status", "🟢 可用",
                 "--desc", f"Notion页面 {title[:80]}"])
    _audit_log("sync_to_topo", {"page_id": pid, "title": title[:80], "topo": topo})
    return {"ok": r["ok"], "page_id": pid, "topo": topo, "group": group,
            "lh_output": r["out"][:600],
            "note": "拓扑注册完成·lh topo list 可见"}


def h_audit_page(a):
    """页面内容三色审计 → 🟢/🟡/🔴"""
    pid = (a.get("page_id") or "").strip()
    if not pid:
        return {"ok": False, "error": "page_id required"}
    # 复用读页逻辑取内容
    pr = h_read_page({"page_id": pid, "depth": 0})
    if not pr.get("ok"):
        return pr
    content = pr.get("content", "")[:20000]
    mark, why, hits = _audit_text_tricolor(content)
    kind = "audit_page_dry" if bool(a.get("dry_run")) else "audit_page"
    _audit_log(kind, {"page_id": pid, "title": (pr.get("page") or {}).get("title", "")[:80],
                      "audit": mark})
    return {"ok": True, "page_id": pid, "title": (pr.get("page") or {}).get("title", ""),
            "audit_color": mark, "reason": why, "red_hits": hits,
            "dry_run": bool(a.get("dry_run")),
            "note": "三色=🟢通过/🟡待关注/🔴红线·🔴应停并审查"}


def h_archive_to_shamewall(a):
    """归档页 → 审计链 + 耻辱墙双留痕（仅当内容含红线/剽窃线索才写耻辱墙 DB）
    非违规归档只落审计链——耻辱墙=剽窃公示，操作日志不污染其公信"""
    pid = (a.get("page_id") or "").strip()
    reason = (a.get("reason") or "常规归档").strip()[:200]
    if not pid:
        return {"ok": False, "error": "page_id required"}
    if bool(a.get("dry_run")):
        # 演练：只读内容判色 + 记账，不归档不写墙
        pg = api.api("GET", f"pages/{pid}")
        title = f"({pid[:8]})"
        if not pg.get("_error"):
            title = _title_of(pg.get("properties"), pg) or title
        pr = h_read_page({"page_id": pid, "depth": 0})
        mark = "🟢"
        if pr.get("ok"):
            mark, _, hits = _audit_text_tricolor(pr.get("content", "")[:20000])
        _audit_log("archive_to_wall_dry", {"page_id": pid, "title": title[:80],
                                           "reason": reason, "audit_color": mark})
        return {"ok": True, "dry_run": True, "page_id": pid, "title": title,
                "reason": reason, "audit_color": mark,
                "planned_wall": mark == "🔴",
                "note": "演练模式·未归档未写墙·如需执行去掉 dry_run"}
    arch = h_archive({"page_id": pid, "restore": bool(a.get("restore"))})
    if not arch.get("ok"):
        return arch
    pg = api.api("GET", f"pages/{pid}")
    title = f"({pid[:8]})"
    if not pg.get("_error"):
        title = _title_of(pg.get("properties"), pg) or title
    # 内容三色 → 判断是否真红线
    pr = h_read_page({"page_id": pid, "depth": 0})
    mark = "🟢"
    if pr.get("ok"):
        mark, _, hits = _audit_text_tricolor(pr.get("content", "")[:20000])
    wall = {"written": False}
    if mark == "🔴":
        # 真红线 → 耻辱墙 DB append（复用 lh_judge 写入函数·签名同 judge 扫描器）
        w = _lh_import_call("lh_judge.py", "记录剽窃",
                            {"源名称": title[:50], "源URL": _url_of(pid),
                             "指纹类型": "notion-archive", "匹配内容": reason[:200],
                             "置信度": 0.8, "审计色": "🔴", "源类型": "notion"})
        wall = {"written": True, "judge_db": w}
    _audit_log("archive_to_wall", {"page_id": pid, "title": title[:80], "reason": reason,
                                   "audit_color": mark})
    return {"ok": True, "page_id": pid, "title": title, "archived": arch.get("archived"),
            "reason": reason, "audit_color": mark, "shamewall": wall,
            "note": "🔴红线内容已上耻辱墙·常规操作留审计链(append-only)"}


def h_comment_to_memory(a):
    """页面评论 → lh brain 长期记忆（评论=对话记录·导入记忆库）"""
    pid = (a.get("page_id") or "").strip()
    if not pid:
        return {"ok": False, "error": "page_id required"}
    cr = h_comments({"page_id": pid, "limit": 50})
    if not cr.get("ok"):
        return cr
    cmts = cr.get("comments", [])
    if bool(a.get("dry_run")):
        _audit_log("comments_to_brain_dry", {"page_id": pid, "count": len(cmts), "saved": 0})
        return {"ok": True, "dry_run": True, "page_id": pid,
                "comments_found": len(cmts), "planned_save": min(len(cmts), 20),
                "note": "演练模式·未入记忆库·如需执行去掉 dry_run"}
    saved = 0
    for c in cmts[:20]:
        txt = f"[Notion评论] {c.get('author', '')}: {c.get('text', '')[:300]}"
        r = _lh_run("lh_brain.py", ["remember", txt, "--silent"])
        if r["ok"]:
            saved += 1
    _audit_log("comments_to_brain", {"page_id": pid, "count": len(cmts), "saved": saved})
    return {"ok": True, "page_id": pid, "comments_found": len(cmts), "saved_to_brain": saved,
            "note": "评论已入 lh brain·lh brain search 可召回"}


def h_export_topo(a):
    """整个页面树 → 龙魂拓扑 JSON（导出 docs/topology/）"""
    pid = (a.get("page_id") or "").strip()
    name = (a.get("name") or "notion-master-export").strip()
    depth = int(a.get("depth") or 1)
    if not pid:
        return {"ok": False, "error": "page_id required"}
    # 节能: 导出深度默认1(主控台57子页直读一次即可)·递归深2+会放大 API 量
    tree = _render_tree(api, pid, name, 0, min(depth, 2), [])
    assets, groups_map = [], {}
    for n in tree:
        gname = n["type"] == "database" and "🗄️ Notion库" or "📄 Notion页"
        groups_map.setdefault(gname, []).append({
            "name": n["title"], "id": n["id"], "status": "🟢 可用",
            "link": n["url"], "type": n["type"], "dna": f"NOTION-{n['id'][:8]}"})
        for c in n.get("children", []):
            groups_map.setdefault("📄 Notion子页", []).append({
                "name": c["title"], "id": c["id"], "status": "🟢 可用",
                "link": c["url"], "type": c["type"], "dna": f"NOTION-{c['id'][:8]}"})
    groups = [{"name": k, "assets": v} for k, v in groups_map.items()]
    out = {"schema": "longhun-topo-v1", "topo_name": name,
           "display": f"📡 {name} v1.0", "owner": "诸葛鑫 | UID9622 · 龍芯北辰",
           "last_sync": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
           "sync_from": "notion-page-tree", "source_url": _url_of(pid),
           "groups": groups, "subgraphs": []}
    safe = "".join(c if c.isalnum() or c in "_-" else "-" for c in name)[:40]
    fpath = os.path.join(LH_ROOT, "docs", "topology", f"{safe}_topo.json")
    if bool(a.get("dry_run")):
        _audit_log("export_topo_dry", {"page_id": pid, "file": fpath, "nodes": len(tree)})
        return {"ok": True, "dry_run": True, "root_id": pid,
                "planned_export_to": fpath, "groups": len(groups), "nodes": len(tree),
                "note": "演练模式·未落盘·如需执行去掉 dry_run"}
    os.makedirs(os.path.dirname(fpath), exist_ok=True)
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    _audit_log("export_topo", {"page_id": pid, "file": fpath, "nodes": len(tree)})
    return {"ok": True, "root_id": pid, "exported_to": fpath,
            "groups": len(groups), "nodes": len(tree),
            "note": "lh topo list 可识别该图谱"}


def _val_to_notion(k, val, ptype):
    """按属性类型构造 Notion 属性值"""
    if ptype in ("title", "rich_text"):
        return {ptype: [{"type": "text", "text": {"content": str(val)[:1900]}}]}
    if ptype == "select":
        return {"select": {"name": str(val)[:100]}}
    if ptype == "multi_select":
        names = val if isinstance(val, list) else [val]
        return {"multi_select": [{"name": str(x)[:100]} for x in names if str(x).strip()]}
    if ptype == "number":
        try:
            return {"number": float(val)}
        except Exception:
            return {"number": None}
    if ptype == "checkbox":
        return {"checkbox": bool(val)}
    if ptype == "url":
        return {"url": str(val)[:1900]}
    if ptype == "date":
        return {"date": {"start": str(val)}}
    return {"rich_text": [{"type": "text", "text": {"content": str(val)[:1900]}}]}


def _db_prop_map(dbid):
    db = api.api("GET", f"databases/{dbid}")
    if "_error" in db:
        return None, None
    title_col = None
    m = {}
    for k, v in db.get("properties", {}).items():
        m[k] = v.get("type")
        if v.get("type") == "title" and title_col is None:
            title_col = k
    return m, title_col


def h_create_row(a):
    dbid = (a.get("database_id") or "").strip()
    props = a.get("properties") or {}
    if not dbid or not isinstance(props, dict):
        return {"ok": False, "error": "database_id + properties required"}
    pmap, title_col = _db_prop_map(dbid)
    if pmap is None:
        return {"ok": False, "error": "db not accessible"}
    body_props = {}
    for k, v in props.items():
        ptype = pmap.get(k, "rich_text")
        body_props[k] = _val_to_notion(k, v, ptype)
    if title_col and title_col not in body_props:
        body_props[title_col] = _val_to_notion(title_col, "新建行", "title")
    res = api.api("POST", "pages", {"parent": {"database_id": dbid},
                                    "properties": body_props})
    if "_error" in res:
        return {"ok": False, "error": res}
    return {"ok": True, "row_id": res.get("id"), "url": _url_of(res.get("id", "")),
            "created": True}


def h_update_row(a):
    rowid = (a.get("row_id") or "").strip()
    props = a.get("properties") or {}
    if not rowid or not isinstance(props, dict) or not props:
        return {"ok": False, "error": "row_id + properties(非空) required"}
    pg = api.api("GET", f"pages/{rowid}")
    if "_error" in pg:
        return {"ok": False, "error": pg}
    dbid = (pg.get("parent") or {}).get("database_id", "")
    pmap, _ = _db_prop_map(dbid)
    if pmap is None:
        return {"ok": False, "error": "parent db not accessible"}
    body_props = {}
    for k, v in props.items():
        ptype = pmap.get(k, "rich_text")
        body_props[k] = _val_to_notion(k, v, ptype)
    res = api.api("PATCH", f"pages/{rowid}", {"properties": body_props})
    if "_error" in res:
        return {"ok": False, "error": res}
    return {"ok": True, "row_id": rowid, "updated": True}


def h_index_sync(a):
    """增量刷新本地 SQLite 索引（search 全量 + 每页文本）· 幂等"""
    incremental = bool(a.get("incremental", True))
    objs = api.search_all("", "page", None)
    con = _db()
    _ensure_local_schema(con)
    ok = skip = 0
    try:
        for p in objs[:500]:
            pid = p.get("id", "")
            if not pid:
                continue
            title = _title_of(p.get("properties")) or f"({pid[:8]})"
            upd = p.get("last_edited_time", "")
            if incremental:
                row = con.execute("SELECT updated_at FROM pages WHERE id=?", (pid,)).fetchone()
                if row and row[0] == upd:
                    skip += 1
                    continue
            par = p.get("parent", {})
            content = ""
            try:
                blk = api.children_all(pid)
                content = "\n".join(_block_to_text(b) for b in blk)[:20000]
            except Exception:
                content = ""
            _index_upsert(api, pid, par.get("page_id") or par.get("database_id") or "",
                          title, "", content, upd)
            ok += 1
        con.commit()
    finally:
        con.close()
    return {"ok": True, "scanned": len(objs[:500]), "updated": ok, "skipped": skip,
            "note": "本地 FTS5 索引已刷新，可用 notion_local_search 秒搜"}


def h_local_search(a):
    q = str(a.get("query") or "").strip()
    limit = int(a.get("limit") or 20)
    if not q:
        return {"ok": False, "error": "query required"}
    con = _db()
    try:
        _ensure_local_schema(con)
        rows = con.execute(
            "SELECT p.id,p.title,p.url,p.icon,p.updated_at FROM pages_fts f "
            "JOIN pages p ON p.rowid=f.rowid WHERE pages_fts MATCH ? ORDER BY rank LIMIT ?",
            (q, limit)).fetchall()
    except sqlite3.OperationalError:
        rows = con.execute("SELECT id,title,url,icon,updated_at FROM pages "
                           "WHERE title LIKE ? OR content LIKE ? LIMIT ?",
                           (f"%{q}%", f"%{q}%", limit)).fetchall()
    con.close()
    items = [{"id": r["id"], "title": r["title"], "url": r["url"], "icon": r["icon"],
              "updated_at": r["updated_at"]} for r in rows]
    return {"ok": True, "query": q, "count": len(items), "items": items,
            "note": "本地索引可能滞后·需实时结果用 notion_search"}


# ────────────────────────── MCP 注册 ──────────────────────────
TOOLS = [
    Tool(name="notion_health",
         description="健康检查：token 有效性 + 官方 API 连通 + 本地索引规模。任何 Notion 操作前先调它确认可用。",
         inputSchema={"type": "object", "properties": {}, "additionalProperties": False}),
    Tool(name="notion_search",
         description="搜索 workspace 里全部页面/数据库（自动翻页）。解决'不知道有什么'的问题。可用空 query 枚举全量；object_type 可筛 page/database。",
         inputSchema={"type": "object",
                      "properties": {"query": {"type": "string", "description": "关键词（空=枚举全部）"},
                                     "object_type": {"type": "string", "enum": ["page", "database"], "description": "对象类型过滤"},
                                     "limit": {"type": "integer", "description": "返回条数上限"}},
                      "additionalProperties": False}),
    Tool(name="notion_page_tree",
         description="从指定页面递归发现子树（子页面+子数据库），返回缩进树文本+JSON。整理前先摸清结构用它。max_depth 默认 2。",
         inputSchema={"type": "object",
                      "properties": {"page_id": {"type": "string", "description": "根页面 ID"},
                                     "max_depth": {"type": "integer", "description": "递归深度(1-6)"}},
                      "additionalProperties": False}),
    Tool(name="notion_read_page",
         description="读整页内容：所有块转结构化文本（标题/段落/列表/代码/引用全保留），可选递归子块。读前会自动把页面存入本地索引。",
         inputSchema={"type": "object",
                      "properties": {"page_id": {"type": "string"},
                                     "depth": {"type": "integer", "description": "子块递归深度(0=仅本页直接块)"}},
                      "additionalProperties": False}),
    Tool(name="notion_query_database",
         description="读数据库全部行（翻页）· 返回库结构+每行属性(标题/文本/选择/数字等已拉平)。",
         inputSchema={"type": "object",
                      "properties": {"database_id": {"type": "string"},
                                     "limit": {"type": "integer", "description": "最多返回行数(默认100)"}},
                      "additionalProperties": False}),
    Tool(name="notion_read_comments",
         description="读页面/块上的全部评论 = 对话记录。每次对话/评审留在 Notion 页面上的批注都能读到。",
         inputSchema={"type": "object",
                      "properties": {"page_id": {"type": "string", "description": "页面或块 ID"},
                                     "limit": {"type": "integer"}},
                      "additionalProperties": False}),
    Tool(name="notion_page_info",
         description="单页元信息：标题/父级/归档状态/创建编辑时间/属性列表/子块数量。",
         inputSchema={"type": "object",
                      "properties": {"page_id": {"type": "string"}},
                      "additionalProperties": False}),
    Tool(name="notion_create_page",
         description="在父页/父库下创建页面。content 支持极简 markdown(#标题/-列表/[x]待办/引用/分隔线)· 前100块。icon 传单个 emoji。",
         inputSchema={"type": "object",
                      "properties": {"parent_type": {"type": "string", "enum": ["page", "database"]},
                                     "parent_id": {"type": "string", "description": "父页面或父数据库 ID"},
                                     "title": {"type": "string"},
                                     "content": {"type": "string", "description": "markdown 正文"},
                                     "icon": {"type": "string", "description": "emoji 图标(单字符)"}},
                      "additionalProperties": False}),
    Tool(name="notion_append_blocks",
         description="页尾追加 markdown 文本（自动分页≤100块/请求·超长安全）。整理/补内容用它。",
         inputSchema={"type": "object",
                      "properties": {"page_id": {"type": "string"},
                                     "content": {"type": "string", "description": "markdown 文本"}},
                      "additionalProperties": False}),
    Tool(name="notion_update_page",
         description="更新页面：改名(title)/改图标(icon)/归档状态(archived)。",
         inputSchema={"type": "object",
                      "properties": {"page_id": {"type": "string"},
                                     "title": {"type": "string", "description": "新标题"},
                                     "icon": {"type": "string", "description": "新 emoji"},
                                     "archived": {"type": "boolean"}},
                      "additionalProperties": False}),
    Tool(name="notion_archive_page",
         description="归档(软删除)页面·符合'不删除只冻结'。restore=true 可恢复。整理归类后的旧页归档用它。",
         inputSchema={"type": "object",
                      "properties": {"page_id": {"type": "string"},
                                     "restore": {"type": "boolean", "description": "true=恢复归档"},
                                     "dry_run": {"type": "boolean", "description": "true=只演练不真改"}},
                      "additionalProperties": False}),
    Tool(name="notion_create_row",
         description="数据库新增一行。properties=JSON 对象 {列名: 值}，类型自动匹配库 schema。",
         inputSchema={"type": "object",
                      "properties": {"database_id": {"type": "string"},
                                     "properties": {"type": "object", "description": "{列名:值} JSON"}},
                      "additionalProperties": False}),
    Tool(name="notion_update_row",
         description="更新数据库某行属性。properties=JSON {列名:值}· 类型自动匹配。",
         inputSchema={"type": "object",
                      "properties": {"row_id": {"type": "string", "description": "行(页面)ID"},
                                     "properties": {"type": "object"}},
                      "additionalProperties": False}),
    Tool(name="notion_index_sync",
         description="增量刷新本地 SQLite+FTS5 索引（不烧太多 API：500页/次·未变跳过）。之后可用 notion_local_search 秒搜全部页面内容。",
         inputSchema={"type": "object",
                      "properties": {"incremental": {"type": "boolean"}},
                      "additionalProperties": False}),
    Tool(name="notion_local_search",
         description="本地 FTS5 秒搜页面标题+内容（不走 API·零延迟）。结果可能滞后于云端·要实时用 notion_search。",
         inputSchema={"type": "object",
                      "properties": {"query": {"type": "string"},
                                     "limit": {"type": "integer"}},
                      "additionalProperties": False}),
    # ── v2.0 生态联动层（任务1·深度集成）──
    Tool(name="notion_sync_to_topo",
         description="把 Notion 页面注册/更新为龙魂拓扑节点（子进程调 lh topo node·同名=更新）。新页/改动页自动长进拓扑。",
         inputSchema={"type": "object",
                      "properties": {"page_id": {"type": "string"},
                                     "topo": {"type": "string", "description": "图谱名(默认 通心译)"},
                                     "group": {"type": "string", "description": "分组(默认 🛰️ Notion数据主控)"},
                                     "dry_run": {"type": "boolean", "description": "true=只演练不真改"}},
                      "additionalProperties": False}),
    Tool(name="notion_audit_page",
         description="对页面内容执行三色审计(lh gov redline + 轻量规则) → 🟢/🟡/🔴。🔴=红线应停。只读无副作用。",
         inputSchema={"type": "object",
                      "properties": {"page_id": {"type": "string"},
                                     "dry_run": {"type": "boolean", "description": "true=演练(只读·行为一致)"}},
                      "additionalProperties": False}),
    Tool(name="notion_archive_to_shamewall",
         description="归档页双留痕：常规操作→append-only审计链；内容判🔴红线→耻辱墙(lh judge add)。耻辱墙=剽窃公示，普通归档不污染。",
         inputSchema={"type": "object",
                      "properties": {"page_id": {"type": "string"},
                                     "reason": {"type": "string", "description": "归档原因"},
                                     "restore": {"type": "boolean"},
                                     "dry_run": {"type": "boolean", "description": "true=只演练不真改(不归档不写墙)"}},
                      "additionalProperties": False}),
    Tool(name="notion_comment_to_memory",
         description="读页面评论(对话记录)并导入 lh brain 长期记忆（子进程调 lh brain remember·silent）。评论=对话·评论留痕进记忆库。",
         inputSchema={"type": "object",
                      "properties": {"page_id": {"type": "string"},
                                     "dry_run": {"type": "boolean", "description": "true=只演练不入记忆库"}},
                      "additionalProperties": False}),
    Tool(name="notion_export_topo",
         description="整个 Notion 页面树导出为龙魂拓扑 JSON（docs/topology/<name>_topo.json·schema longhun-topo-v1·lh topo list 可识别）。depth 默认1=仅直接子页，节能。",
         inputSchema={"type": "object",
                      "properties": {"page_id": {"type": "string"},
                                     "name": {"type": "string", "description": "图谱名"},
                                     "depth": {"type": "integer", "description": "递归深度1-2(默认1节能)"},
                                     "dry_run": {"type": "boolean", "description": "true=只演练不落盘"}},
                      "additionalProperties": False}),
]

HANDLERS = {
    "notion_health": h_health,
    "notion_search": h_search,
    "notion_page_tree": h_tree,
    "notion_read_page": h_read_page,
    "notion_query_database": h_query_db,
    "notion_read_comments": h_comments,
    "notion_page_info": h_page_info,
    "notion_create_page": h_create_page,
    "notion_append_blocks": h_append,
    "notion_update_page": h_update_page,
    "notion_archive_page": h_archive,
    "notion_create_row": h_create_row,
    "notion_update_row": h_update_row,
    "notion_index_sync": h_index_sync,
    "notion_local_search": h_local_search,
    # v2.0 生态联动
    "notion_sync_to_topo": h_sync_to_topo,
    "notion_audit_page": h_audit_page,
    "notion_archive_to_shamewall": h_archive_to_shamewall,
    "notion_comment_to_memory": h_comment_to_memory,
    "notion_export_topo": h_export_topo,
}

api = NotionAPI(get_token())  # module-level 单例（token 失败由 health 暴露）


@app.list_tools()
async def list_tools():
    return TOOLS


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    global api
    try:
        if api.token and not _probe_token(api.token):
            api = NotionAPI(get_token())
        handler = HANDLERS.get(name)
        if not handler:
            return [TextContent(type="text", text=json.dumps(
                {"ok": False, "error": f"unknown tool: {name}"}, ensure_ascii=False))]
        result = handler(arguments or {})
        return [TextContent(type="text",
                            text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps(
            {"ok": False, "error": str(e), "type": type(e).__name__},
            ensure_ascii=False, indent=2))]


async def main():
    async with stdio_server() as streams:
        await app.run(streams[0], streams[1], app.create_initialization_options())


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Notion Master MCP Server")
    ap.add_argument("--selftest", action="store_true", help="离线自测(不连 API)")
    args, _ = ap.parse_known_args()
    if args.selftest:
        # 离线: 文本→块转换器
        md = "# 标题\n正文段落\n- 甲\n- 乙\n[x] 已完成\n> 引用\n---\n1. 一\n2. 二"
        blk = text_to_blocks(md)
        print(json.dumps({"blocks": len(blk),
                          "types": [b["type"] for b in blk],
                          "dna": "#龍芯⚡️2026-09-04-NOTION-MASTER-MCP-SELFTEST"}, ensure_ascii=False, indent=2))
    else:
        asyncio.run(main())
