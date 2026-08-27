#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 搜索底座 v1.0
DNA: #龍芯⚡️丙午·丙申·丁未·丙午·䷱鼎-SEARCH-BASE-v1.0-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰

轻量 · 本地优先 · 鲲鹏 ARM64 原生 · 零外部依赖
- 纯 Python 标准库, 无需 Flask/requests/bs4
- 默认只搜本地知识图谱 + 认知索引, 不碰外网
- 可选 `--web` 启用轻量爬取(urllib)
- 所有搜索写入史官日志, 透明看板可查
- 支持 CLI 与 HTTP 服务两种模式
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Any


# ============================================================
# 常量与铁律
# ============================================================

DNA = "#龍芯⚡️丙午·丙申·丁未·丙午·䷱鼎-SEARCH-BASE-v1.0-UID9622"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

PROJECT_ROOT = Path.home() / "longhun-system"
LONGHUN_DIR = Path.home() / ".longhun"
SEARCH_DB_DIR = LONGHUN_DIR / "search"
SEARCH_DB_PATH = SEARCH_DB_DIR / "search_base.db"
HISTORIAN_DIR = LONGHUN_DIR / "04_AUDIT"

KG_PATH = LONGHUN_DIR / "knowledge_graph" / "graph.json"
COGNITIVE_INDEX_PATH = LONGHUN_DIR / "cognitive_index.json"

DEFAULT_PORT = 8090
DEFAULT_HOST = "127.0.0.1"
DEFAULT_LIMIT = 10
CACHE_TTL_SECONDS = 3600  # 本地缓存 1 小时


# ============================================================
# DNA 与日志
# ============================================================

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _generate_dna(query: str, action: str = "search") -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    raw = f"{action}|UID9622|{ts}|{query}|{time.time()}"
    h = hashlib.sha256(raw.encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now(timezone.utc).strftime('%Y-%m-%d')}-SEARCH-{h}-UID9622"


def _write_historian(query: str, result_count: int, source: str, dna: str):
    """写入史官日志, 供透明看板读取。"""
    HISTORIAN_DIR.mkdir(parents=True, exist_ok=True)
    log_file = HISTORIAN_DIR / f"search_{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.jsonl"
    entry = {
        "timestamp": _now(),
        "operation": "search",
        "query": query,
        "result_count": result_count,
        "source": source,
        "dna": dna,
        "actor": "UID9622",
        "module": "lh_search_engine",
    }
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass  # 日志不阻塞搜索


# ============================================================
# 数据库层
# ============================================================

class SearchStore:
    def __init__(self, db_path: Path = SEARCH_DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS search_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL,
                    source TEXT NOT NULL,
                    result TEXT NOT NULL,
                    dna TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL
                )
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_query ON search_cache(query, source)
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS search_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL,
                    count INTEGER DEFAULT 1,
                    last_searched TEXT NOT NULL
                )
            """)
            cur.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS idx_query_log ON search_log(query)
            """)
            conn.commit()

    def get_cache(self, query: str, source: str) -> list[dict] | None:
        now = _now()
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT result FROM search_cache
                WHERE query = ? AND source = ? AND expires_at > ?
                ORDER BY id DESC LIMIT 1
            """, (query, source, now))
            row = cur.fetchone()
        if row:
            try:
                return json.loads(row[0])
            except json.JSONDecodeError:
                return None
        return None

    def set_cache(self, query: str, source: str, results: list[dict], dna: str):
        now = datetime.now(timezone.utc)
        created = now.isoformat()
        expires = (now.timestamp() + CACHE_TTL_SECONDS)
        expires_str = datetime.fromtimestamp(expires, tz=timezone.utc).isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO search_cache (query, source, result, dna, created_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (query, source, json.dumps(results, ensure_ascii=False), dna, created, expires_str))
            conn.commit()

    def log_query(self, query: str):
        now = _now()
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO search_log (query, count, last_searched)
                VALUES (?, 1, ?)
                ON CONFLICT(query) DO UPDATE SET
                    count = count + 1,
                    last_searched = excluded.last_searched
            """, (query, now))
            conn.commit()


# ============================================================
# 检索引擎
# ============================================================

class SearchEngine:
    def __init__(self, store: SearchStore | None = None):
        self.store = store or SearchStore()

    def search(self, query: str, source: str = "local", limit: int = DEFAULT_LIMIT) -> dict:
        dna = _generate_dna(query)

        # 1. 缓存命中
        cached = self.store.get_cache(query, source)
        if cached is not None:
            _write_historian(query, len(cached), source + "(cache)", dna)
            return {
                "query": query,
                "results": cached[:limit],
                "total": len(cached),
                "source": source,
                "cached": True,
                "dna": dna,
                "timestamp": _now(),
            }

        # 2. 本地检索
        results: list[dict] = []
        if source in ("local", "web"):
            results.extend(self._search_knowledge_graph(query))
            results.extend(self._search_cognitive_index(query))
            results.extend(self._search_local_files(query))

        # 3. 可选外网轻量抓取
        if source == "web":
            results.extend(self._scrape_web(query))

        # 4. 去重排序
        unique = self._deduplicate(results)
        unique = self._rank(query, unique)

        # 5. 缓存与日志
        self.store.set_cache(query, source, unique, dna)
        self.store.log_query(query)
        _write_historian(query, len(unique), source, dna)

        return {
            "query": query,
            "results": unique[:limit],
            "total": len(unique),
            "source": source,
            "cached": False,
            "dna": dna,
            "timestamp": _now(),
        }

    def _search_knowledge_graph(self, query: str) -> list[dict]:
        if not KG_PATH.exists():
            return []
        try:
            with open(KG_PATH, "r", encoding="utf-8") as f:
                kg = json.load(f)
        except Exception:
            return []

        q = query.lower()
        results = []
        for node in kg.get("nodes", []):
            title = str(node.get("title", ""))
            content = str(node.get("content", ""))
            if q in title.lower() or q in content.lower():
                results.append({
                    "title": title or "知识图谱节点",
                    "snippet": (content[:200] + "...") if len(content) > 200 else content,
                    "source": "知识图谱",
                    "dna": node.get("dna", ""),
                    "score": self._score(q, title, content),
                })
        return results

    def _search_cognitive_index(self, query: str) -> list[dict]:
        if not COGNITIVE_INDEX_PATH.exists():
            return []
        try:
            with open(COGNITIVE_INDEX_PATH, "r", encoding="utf-8") as f:
                index = json.load(f)
        except Exception:
            return []

        q = query.lower()
        results = []
        for key, value in index.items():
            text = f"{key} {value}"
            if q in text.lower():
                snippet = str(value)
                results.append({
                    "title": key,
                    "snippet": (snippet[:200] + "...") if len(snippet) > 200 else snippet,
                    "source": "认知索引",
                    "score": self._score(q, key, snippet),
                })
        return results

    def _search_local_files(self, query: str) -> list[dict]:
        """轻量扫描项目内 Markdown/Python 文件标题/路径。"""
        q = query.lower()
        results = []
        # 只扫描核心目录, 避免递归过深
        scan_roots = [
            PROJECT_ROOT / "01_protocols",
            PROJECT_ROOT / "12_DOCS",
            PROJECT_ROOT / "03_KNOWLEDGE_GRAPH",
        ]
        for root in scan_roots:
            if not root.exists():
                continue
            for path in root.iterdir():
                if not path.is_file():
                    continue
                name = path.name.lower()
                if q in name:
                    results.append({
                        "title": path.name,
                        "snippet": f"本地文件: {path.relative_to(PROJECT_ROOT)}",
                        "source": "本地文件",
                        "path": str(path),
                        "score": 20 if q in path.stem.lower() else 10,
                    })
                if len(results) >= 50:
                    break
        return results

    def _scrape_web(self, query: str) -> list[dict]:
        """轻量网页抓取, 仅作为可选 fallback。"""
        results = []
        try:
            encoded = urllib.parse.quote(query)
            url = f"https://html.duckduckgo.com/html/?q={encoded}"
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                },
            )
            with urllib.request.urlopen(req, timeout=8) as resp:
                html = resp.read().decode("utf-8", errors="ignore")

            pattern = re.compile(r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.S)
            for link, title_html in pattern.findall(html)[:10]:
                title = re.sub(r"<[^>]+>", "", title_html).strip()
                if title:
                    results.append({
                        "title": title,
                        "snippet": link,
                        "source": "web",
                        "url": link,
                        "score": 5,
                    })
        except Exception:
            pass
        return results

    @staticmethod
    def _score(q: str, title: str, content: str) -> int:
        score = 0
        t = title.lower()
        c = content.lower()
        if q in t:
            score += 30
        if q in c:
            score += 10
        # 简单词频
        score += c.count(q) * 2
        return score

    @staticmethod
    def _rank(query: str, items: list[dict]) -> list[dict]:
        return sorted(items, key=lambda x: x.get("score", 0), reverse=True)

    @staticmethod
    def _deduplicate(items: list[dict]) -> list[dict]:
        seen = set()
        unique = []
        for item in items:
            key = item.get("title", "") + "|" + item.get("snippet", "")[:80]
            if key not in seen:
                seen.add(key)
                unique.append(item)
        return unique


# ============================================================
# CLI 输出
# ============================================================

def _strip_ansi(text: str) -> str:
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


def _display_width(text: str) -> int:
    import unicodedata
    w = 0
    for ch in _strip_ansi(text):
        if unicodedata.east_asian_width(ch) in ("F", "W", "A"):
            w += 2
        else:
            w += 1
    return w


def _truncate(text: str, width: int) -> str:
    if width <= 0:
        return ""
    out = []
    display_len = 0
    for ch in text:
        ch_w = 2 if _display_width(ch) > 1 else 1  # 简化处理
        if display_len + ch_w > width:
            break
        out.append(ch)
        display_len += ch_w
    return "".join(out)


def format_text(query: str, data: dict, no_color: bool = False) -> str:
    lines = []
    lines.append(f"🐉 龍魂搜索 · {query}")
    lines.append(f"   后端: {data['source']} | 缓存: {'是' if data.get('cached') else '否'} | 结果: {data['total']}条")
    lines.append(f"   DNA: {data['dna']}")
    lines.append("-" * 60)

    for i, res in enumerate(data["results"], 1):
        title = res.get("title", "无标题")
        snippet = res.get("snippet", "")
        source = res.get("source", "未知")
        lines.append(f"{i}. [{source}] {title}")
        if snippet:
            lines.append(f"   {snippet[:120]}")
    return "\n".join(lines)


def format_json(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def format_csv(data: dict) -> str:
    lines = ["rank,source,title,snippet"]
    for i, res in enumerate(data["results"], 1):
        title = res.get("title", "").replace(",", " ")
        snippet = res.get("snippet", "").replace(",", " ").replace("\n", " ")
        source = res.get("source", "")
        lines.append(f"{i},{source},{title},{snippet}")
    return "\n".join(lines)


# ============================================================
# HTTP 服务
# ============================================================

class SearchHandler(BaseHTTPRequestHandler):
    engine: SearchEngine = SearchEngine()

    def _send_json(self, data: dict, status: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html: str, status: int = 200):
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        # BaseHTTPRequestHandler 把请求行按 latin-1 解码, 但 URL 本身是 utf-8 字节
        # 这里显式用 utf-8 重新解析查询参数
        raw_path = self.path.encode("latin-1").decode("utf-8", errors="replace")
        parsed = urllib.parse.urlparse(raw_path)
        path = parsed.path
        qs = urllib.parse.parse_qs(parsed.query, encoding="utf-8")

        if path == "/" or path == "/index.html":
            html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>🐉 龍魂搜索底座</title></head>
<body style="font-family:sans-serif;max-width:800px;margin:40px auto;">
<h1>🐉 龍魂搜索底座</h1>
<p>{DNA}</p>
<form action="/search" method="get">
<input type="text" name="q" placeholder="输入搜索词" style="width:60%;padding:8px;" />
<select name="source">
<option value="local">本地</option>
<option value="web">本地+网络</option>
</select>
<button type="submit">搜索</button>
</form>
<p>示例: <a href="/search?q=龍魂系统&source=local">/search?q=龍魂系统&source=local</a></p>
</body>
</html>"""
            self._send_html(html)
            return

        if path == "/health":
            self._send_json({"status": "ok", "dna": DNA, "timestamp": _now()})
            return

        if path == "/search":
            query = qs.get("q", [""])[0].strip()
            source = qs.get("source", ["local"])[0]
            limit = int(qs.get("limit", [str(DEFAULT_LIMIT)])[0])
            if not query:
                self._send_json({"error": "缺少参数 q"}, status=400)
                return
            result = self.engine.search(query, source=source, limit=limit)
            self._send_json(result)
            return

        self._send_json({"error": "Not Found"}, status=404)

    def log_message(self, format: str, *args):
        # 静默访问日志, 避免污染
        pass


def run_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
    SearchHandler.engine = SearchEngine()
    server = HTTPServer((host, port), SearchHandler)
    print(f"🐉 龍魂搜索底座已启动: http://{host}:{port}", file=sys.stderr)
    print(f"   DNA: {DNA}", file=sys.stderr)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 已停止", file=sys.stderr)


# ============================================================
# CLI
# ============================================================

def main(argv: list[str] | None = None) -> int:
    argv = list(argv or sys.argv[1:])

    # 兼容 lh-ctl 调用: lh_search_engine.py search <query> [options]
    # 也支持直接调用: lh_search_engine.py <query> [options]
    if argv and argv[0] == "search":
        argv = argv[1:]

    parser = argparse.ArgumentParser(description="龍魂 · 搜索底座")
    parser.add_argument("query", nargs="?", help="搜索关键词")
    parser.add_argument("--n", type=int, default=DEFAULT_LIMIT, help="返回结果数")
    parser.add_argument("--deep", type=int, default=0, help="保留参数, 当前版本忽略")
    parser.add_argument("--source", choices=["local", "web"], default="local", help="搜索来源")
    parser.add_argument("--output", choices=["text", "json", "csv"], default="text", help="输出格式")
    parser.add_argument("--style", default="default", help="保留参数, 当前版本忽略")
    parser.add_argument("--no-color", action="store_true", help="禁用颜色")
    parser.add_argument("--server", action="store_true", help="启动 HTTP 服务")
    parser.add_argument("--host", default=DEFAULT_HOST, help="服务监听地址")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="服务监听端口")

    args = parser.parse_args(argv)

    if args.server:
        run_server(args.host, args.port)
        return 0

    if not args.query:
        parser.error("请提供搜索词, 或使用 --server 启动服务")

    engine = SearchEngine()
    result = engine.search(args.query, source=args.source, limit=args.n)

    if args.output == "json":
        print(format_json(result))
    elif args.output == "csv":
        print(format_csv(result))
    else:
        print(format_text(args.query, result, no_color=args.no_color))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
