#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-08-31-NOTION-SCANNER-v2.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""龍魂 · Notion 全账号通读扫描器 v2.0

把 Notion 工作区内有权访问的页面/数据库递归拉取，写入本地 SQLite + FTS5 全文索引。
解决「MCP 只能按数据库 ID 查询、无法发现独立页面」的结构性缺口。
v2.0: 新增语义向量索引（ChromaDB + ollama nomic-embed-text）· RAG 语义搜索管道
指数退避(429→2^attempt+抖动) 与速率保护(≤3 req/s) 已在 _api() 内置。

用法:
  python3 08_BIN/lh_notion_scanner.py             # 全量扫描
  python3 08_BIN/lh_notion_scanner.py --incremental  # 增量同步（只更新变化的页）
  python3 08_BIN/lh_notion_scanner.py --embed        # 本地库→Chroma 语义向量化（不扫 API·最节能）
  python3 08_BIN/lh_notion_scanner.py --limit 50     # 限量扫描（测试用）
  python3 08_BIN/lh_notion_scanner.py --stats        # 只看统计

Token 来源优先级: 环境变量 NOTION_TOKEN > vault (lh_vault get NOTION_TOKEN)。值不落盘。
"""
import argparse
import json
import os
import re
import sqlite3
import sys
import time
import urllib.request
import urllib.error

API = "https://api.notion.com/v1"
DB_PATH = os.path.expanduser("~/.longhun/notion_index.db")

for _k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy",
           "ALL_PROXY", "all_proxy"):
    os.environ.pop(_k, None)
os.environ["NO_PROXY"] = "*"

# 标签分类器（手册 §四：10+ 规则）
TAG_RULES = [
    ("🧬 DNA系统", ["dna", "追溯", "签章", "gpg", "uid9622", "双签"]),
    ("🐉 龙魂核心", ["协议", "宪法", "铁律", "主权", "焊死", "白皮书", "宪法", "m261"]),
    ("🧠 知识库", ["计算机科学", "知识点", "cs知识", "教程", "算法", "数据结构"]),
    ("🎭 人格系统", ["人格", "花名册", "p00", "p01", "p02", "p03", "p04", "p05", "p06", "p07",
                 "p08", "p09", "p10", "p11", "p12", "p13", "p14", "p15", "p72", "p77"]),
    ("🔐 安全审计", ["三色审计", "熔断", "kill", "安全", "漏洞", "审计", "红蓝"]),
    ("⚙️ 工程实现", ["代码", "部署", "api", "引擎", "脚本", "mcp", "配置", "端口"]),
    ("🌐 门户展示", ["首页", "3d", "拓扑", "通心译", "门户", "官网", "平台矩阵"]),
    ("📚 文档归档", ["归档", "日志", "历史", "复盘", "记录"]),
    ("🎬 媒体创作", ["视频", "音频", "图片", "设计", "成片", "剪辑"]),
    ("💡 待办/草案", ["待办", "todo", "草案", "计划", "备忘"]),
    ("🏆 等级体系", ["等级", "称号", "科技风格", "体系"]),
]


def _probe_token(tok):
    """轻量验证 token 是否有效（GET /users/me）"""
    req = urllib.request.Request(
        f"{API}/users/me",
        headers={"Authorization": f"Bearer {tok}", "Notion-Version": "2025-09-03"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status == 200
    except Exception:
        return False


def get_token():
    """候选优先级: 环境变量 > vault > mcp.json；逐一实测验证，取第一个有效者"""
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
    print(f"❌ 全部 {len(cands)} 个 NOTION_TOKEN 候选均无效: {[n for n, _ in cands]}", file=sys.stderr)
    sys.exit(1)


class NotionScanner:
    def __init__(self, token, db_path=DB_PATH):
        self.token = token
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._init_db()

    def _h(self):
        return {"Authorization": f"Bearer {self.token}",
                "Notion-Version": "2025-09-03",
                "Content-Type": "application/json"}

    def _api(self, method, path, body=None, retries=5):
        """Notion API 请求 · 指数退避+抖动（对齐 MCP 手册 §0.6）
        - 429: 2^attempt + random jitter 防惊群
        - 5xx: 2^attempt 重试
        - 每次成功返回前 0.35s 限速（≤3 req/s 官方限制）
        """
        req = urllib.request.Request(
            f"{API}/{path}",
            data=json.dumps(body).encode() if body is not None else None,
            method=method, headers=self._h())
        for attempt in range(retries + 1):
            try:
                with self.opener.open(req, timeout=30) as r:
                    time.sleep(0.35)  # 安全间隔：低于 3 req/s
                    return json.loads(r.read().decode())
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < retries:
                    wait = (2 ** attempt) + random.uniform(0, 1)
                    print(f"⚠️ Notion Rate Limited(429), 等待 {wait:.1f}s [retry {attempt+1}/{retries}]")
                    time.sleep(wait)
                    continue
                if e.code >= 500 and attempt < retries:
                    wait = 2 ** attempt
                    print(f"⚠️ Notion Server Error {e.code}, 等待 {wait}s")
                    time.sleep(wait)
                    continue
                try:
                    return {"_error": e.code, "message": json.loads(e.read().decode()).get("message", "")[:80]}
                except Exception:
                    return {"_error": e.code, "message": ""}
        return {"_error": 0}

    def _init_db(self):
        con = sqlite3.connect(self.db_path)
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
        con.close()

    def _classify(self, title, content):
        blob = f"{title} {content}".lower()
        tags = []
        for name, kws in TAG_RULES:
            if any(k in blob for k in kws):
                tags.append(name)
        return "|".join(tags) if tags else "📄 未归类"

    @staticmethod
    def _extract_title(props):
        for k, v in (props or {}).items():
            if v.get("type") == "title" and v.get("title"):
                return "".join(x.get("plain_text", "") for x in v["title"])
        return ""

    @staticmethod
    def _extract_icon(obj):
        ic = obj.get("icon") or {}
        if ic.get("type") == "emoji":
            return ic.get("emoji", "")
        if ic.get("type") in ("external", "file"):
            return "🖼"
        return ""

    def _blocks_text(self, page_id, depth=0, max_depth=1):
        """拉取页面子块拼接纯文本（递归 depth 层，限量防爆）"""
        parts = []
        cursor = None
        while True:
            path = f"blocks/{page_id}/children"
            if cursor:
                path += f"?start_cursor={cursor}"
            res = self._api("GET", path)
            if "_error" in res:
                return ""
            for b in res.get("results", []):
                t = b.get("type")
                if t == "child_page":
                    parts.append(f"\n## {b.get('child_page', {}).get('title', '')}")
                    continue
                try:
                    val = b.get(t, {})
                    if isinstance(val, dict):
                        r = val.get("rich_text")
                        if isinstance(r, list):
                            txt = "".join(x.get("plain_text", "") for x in r)
                            if txt:
                                parts.append(txt)
                    elif t == "to_do":
                        txt = "".join(x.get("plain_text", "") for x in b["to_do"].get("rich_text", []))
                        if txt:
                            parts.append(txt)
                except Exception:
                    pass
            if res.get("has_more") and res.get("next_cursor"):
                cursor = res["next_cursor"]
            else:
                break
        return "\n".join(parts)[:20000]

    def search_pages(self, limit=None, incremental=False):
        """分页拉取权限内全部页面+数据库"""
        out = []
        cursor = None
        while True:
            body = {"query": "", "page_size": 100}
            if cursor:
                body["start_cursor"] = cursor
            res = self._api("POST", "search", body)
            if "_error" in res:
                print(f"❌ search 失败: {res}", file=sys.stderr)
                break
            out.extend(res.get("results", []))
            if limit and len(out) >= limit:
                out = out[:limit]
                break
            if res.get("has_more") and res.get("next_cursor"):
                cursor = res["next_cursor"]
            else:
                break
        return out

    def index(self, limit=None, incremental=False):
        pages = self.search_pages(limit, incremental)
        print(f"🔎 命中 {len(pages)} 个对象（页面+数据库）")
        con = sqlite3.connect(self.db_path)
        ok = skip = fail = 0
        for p in pages:
            pid = p.get("id", "")
            if not pid:
                continue
            otype = p.get("object", "page")
            title = self._extract_title(p.get("properties"))
            if not title:
                raw = p.get("title") or ""
                if isinstance(raw, list):
                    title = "".join(
                        (x.get("plain_text", "") if isinstance(x, dict) else "") or
                        (x.get("text", {}).get("content", "") if isinstance(x, dict) else "")
                        for x in raw)
                elif isinstance(raw, str):
                    title = raw
            if not title:
                # 数据库无 title property 时用 id 结尾
                title = f"({otype[:4]}·{pid[:8]})"
            icon = self._extract_icon(p)
            last_edited = p.get("last_edited_time", "")
            parent = p.get("parent", {})
            parent_id = parent.get("page_id") or parent.get("database_id") or ""
            if incremental:
                row = con.execute("SELECT updated_at FROM pages WHERE id=?", (pid,)).fetchone()
                if row and row[0] == last_edited:
                    skip += 1
                    continue
            url = f"https://www.notion.so/{pid.replace('-', '')}"
            content = ""
            if otype == "page":
                content = self._blocks_text(pid)
            tags = self._classify(title, content)
            row = con.execute("SELECT rowid FROM pages WHERE id=?", (pid,)).fetchone()
            if row:
                con.execute("UPDATE pages SET title=?,url=?,icon=?,tags=?,content=?,"
                            "status='ok',updated_at=?,scanned_at=datetime('now') WHERE id=?",
                            (title, url, icon, tags, content, last_edited, pid))
            else:
                con.execute("INSERT INTO pages(id,parent_id,title,url,icon,tags,content,status,updated_at,scanned_at)"
                            " VALUES(?,?,?,?,?,?,?,?,?,datetime('now'))",
                            (pid, parent_id, title, url, icon, tags, content, "ok", last_edited))
            ok += 1
            if ok % 20 == 0:
                print(f"  已索引 {ok} ...")
            time.sleep(0.35)  # Notion API 限速 3 req/s
        con.commit()
        con.close()
        print(f"✅ 完成: 新/更新 {ok} · 跳过(未变) {skip} · 失败 {fail}")

    def stats(self):
        con = sqlite3.connect(self.db_path)
        n = con.execute("SELECT COUNT(*) FROM pages").fetchone()[0]
        by_tag = con.execute("SELECT tags, COUNT(*) FROM pages GROUP BY tags ORDER BY 2 DESC LIMIT 12").fetchall()
        con.close()
        print(f"📊 索引总数: {n} 页")
        for t, c in by_tag:
            print(f"   {t}: {c}")
        return n


CHROMA_DIR = os.path.expanduser("~/.longhun/chroma")
COLLECTION = "longhun_pages"


def embed_all(db_path=DB_PATH):
    """本地 SQLite → Chroma 语义向量化（不调 Notion API·纯本地计算）

    逐页读 title+content → ollama nomic-embed-text → chroma upsert。
    幂等：同 page_id 覆盖。未装 chromadb/ollama 或模型缺失时优雅降级。
    """
    try:
        import chromadb
    except ImportError:
        print("❌ 需要 chromadb: pip3 install chromadb", file=sys.stderr)
        return 0
    try:
        import ollama as ol
    except ImportError:
        print("❌ 需要 ollama python 包: pip3 install ollama", file=sys.stderr)
        return 0

    os.makedirs(CHROMA_DIR, exist_ok=True)
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    coll = client.get_or_create_collection(COLLECTION)

    # 确认 embedding 模型存在（ollama list）
    model = "nomic-embed-text"
    have = [m.get("name", "") for m in ol.list().get("models", [])]
    if not any(model in n for n in have):
        print(f"📥 拉取 embedding 模型 {model}（~274MB·一次性）...")
        ol.pull(model)

    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    rows = con.execute("SELECT id, title, content FROM pages WHERE title IS NOT NULL AND title != ''").fetchall()
    con.close()
    print(f"🧠 开始语义向量化 {len(rows)} 页 → chroma/{COLLECTION} ...")
    ok = 0
    for r in rows:
        text = f"{r['title']}\n{(r['content'] or '')[:2000]}".strip()
        if not text:
            continue
        try:
            resp = ol.embeddings(model=model, prompt=text)
            coll.upsert(ids=[r["id"]], embeddings=[resp["embedding"]],
                        metadatas=[{"title": r["title"], "page_id": r["id"]}])
            ok += 1
        except Exception as e:
            print(f"  ⚠️ {r['id'][:8]} embed 失败: {e}")
        if ok % 20 == 0:
            print(f"  已向量化 {ok} ...")
    print(f"✅ 语义向量化完成: {ok}/{len(rows)} 页 → {CHROMA_DIR}")
    return ok


def semantic_search(query, n=5, db_path=DB_PATH):
    """语义搜索：query → embedding → chroma 余弦检索"""
    try:
        import chromadb
        import ollama as ol
    except ImportError:
        return None
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    coll = client.get_or_create_collection(COLLECTION)
    resp = ol.embeddings(model="nomic-embed-text", prompt=query)
    return coll.query(query_embeddings=[resp["embedding"]], n_results=n)


def main():
    ap = argparse.ArgumentParser(description="Notion 全账号通读扫描器")
    ap.add_argument("--incremental", action="store_true", help="增量同步")
    ap.add_argument("--limit", type=int, default=None, help="限量扫描")
    ap.add_argument("--stats", action="store_true", help="只看统计")
    ap.add_argument("--embed", action="store_true", help="本地库→Chroma 语义向量化")
    ap.add_argument("--db", default=DB_PATH, help="SQLite 路径")
    args = ap.parse_args()
    if args.embed:
        n = embed_all(args.db)
        print(f"🧬 DNA: #龍芯⚡️{time.strftime('%Y-%m-%d')}-EMBED-DONE-v2.0-UID9622")
        return
    token = get_token()
    sc = NotionScanner(token, args.db)
    if args.stats:
        sc.stats()
        return
    print(f"🗂 索引库: {args.db}")
    sc.index(limit=args.limit, incremental=args.incremental)
    sc.stats()


if __name__ == "__main__":
    main()
