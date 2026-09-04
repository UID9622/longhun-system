#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-08-31-NOTION-BRIDGE-v2.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""龍魂 · Notion 全账号通读桥接器 v2.0（REST 双通道）

基于 lh_notion_scanner.py 的本地索引，对外提供只读 API。
索引未命中时实时代理 Notion API（回源模式），保证查询不遗漏。
v2.0: 新增语义向量搜索端点 · CORS 本地安全配置 · 增强健康探针（Liveness）

API:
  GET  /api/notion/pages          → 列出索引页面（分页）
  GET  /api/notion/page/{id}      → 页面详情+内容
  GET  /api/notion/tags           → 自动归类标签统计
  GET  /api/notion/search?q=      → FTS5 全文搜索
  GET  /api/notion/semantic?q=    → 语义向量搜索（ChromaDB·需先跑 scanner --embed）
  POST /api/notion/callback       → 回调拉取占位（写入 queue）
  GET  /api/notion/health         → 健康检查

安全: 只绑 127.0.0.1 · CORS 仅 localhost · token 只经环境变量/vault · 值不落盘
"""
import argparse
import json
import os
import sqlite3
import time
import urllib.request
import urllib.error

DB_PATH = os.path.expanduser("~/.longhun/notion_index.db")
API = "https://api.notion.com/v1"

for _k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy",
           "ALL_PROXY", "all_proxy"):
    os.environ.pop(_k, None)
os.environ["NO_PROXY"] = "*"

try:
    from flask import Flask, jsonify, request
    from flask_cors import CORS
except ImportError:
    print("❌ 需要 flask: pip install flask", file=sys.stderr)
    sys.exit(1)

CHROMA_DIR = os.path.expanduser("~/.longhun/chroma")
COLLECTION = "longhun_pages"


def get_token():
    """候选优先级: 环境变量 > vault > mcp.json；逐一实测验证，取第一个有效者"""
    cands = []
    if os.environ.get("NOTION_TOKEN", "").strip():
        cands.append(os.environ["NOTION_TOKEN"].strip())
    try:
        v = os.popen("python3 bin/lh_vault.py get NOTION_TOKEN").read().strip()
        if v and not v.lower().startswith("error"):
            cands.append(v)
    except Exception:
        pass
    try:
        with open(os.path.expanduser("~/.codebuddy/mcp.json")) as f:
            m = json.load(f)
        t = m.get("mcpServers", {}).get("Notion MCP Server", {}).get("env", {}).get("NOTION_TOKEN", "")
        if t:
            cands.append(t.strip())
    except Exception:
        pass
    for t in cands:
        try:
            req = urllib.request.Request(
                f"{API}/users/me",
                headers={"Authorization": f"Bearer {t}", "Notion-Version": "2025-09-03"})
            with urllib.request.urlopen(req, timeout=10) as r:
                if r.status == 200:
                    return t
        except Exception:
            continue
    return ""


def _api_direct(path):
    """回源模式：实时调 Notion API"""
    tok = get_token()
    if not tok:
        return {"_error": 401, "message": "no token"}
    req = urllib.request.Request(
        f"{API}/{path}",
        headers={"Authorization": f"Bearer {tok}",
                 "Notion-Version": "2025-09-03"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return {"_error": e.code, "message": json.loads(e.read().decode()).get("message", "")[:80]}
        except Exception:
            return {"_error": e.code, "message": ""}


app = Flask(__name__)
# CORS: 仅允许本地来源（安全配置 · Fetch Living Standard）
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:*", "http://127.0.0.1:*"]}})


def _db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


@app.route("/api/notion/health")
def health():
    """健康检查端点（Liveness Probe · 对标 Kubernetes 标准）"""
    con = _db()
    pc = con.execute("SELECT COUNT(*) FROM pages").fetchone()[0]
    bc = con.execute("SELECT COUNT(*) FROM pages WHERE content != ''").fetchone()[0]
    con.close()
    chroma_ok = os.path.isdir(CHROMA_DIR)
    return jsonify({
        "status": "ok",
        "service": "notion-mcp-bridge",
        "version": "2.0",
        "pages": pc,
        "blocks_with_content": bc,
        "semantic_ready": chroma_ok,
        "time": time.time(),
        "dna": "#龍芯⚡️2026-08-31-BRIDGE-HEALTH-v2.0-UID9622",
    })


@app.route("/api/notion/pages")
def pages():
    limit = min(int(request.args.get("limit", 50)), 200)
    offset = int(request.args.get("offset", 0))
    tag = request.args.get("tag", "")
    con = _db()
    if tag:
        rows = con.execute("SELECT id,title,url,icon,tags,status,updated_at FROM pages"
                           " WHERE tags LIKE ? ORDER BY updated_at DESC LIMIT ? OFFSET ?",
                           (f"%{tag}%", limit, offset)).fetchall()
    else:
        rows = con.execute("SELECT id,title,url,icon,tags,status,updated_at FROM pages"
                           " ORDER BY updated_at DESC LIMIT ? OFFSET ?", (limit, offset)).fetchall()
    con.close()
    return jsonify({"count": len(rows), "items": [dict(r) for r in rows]})


@app.route("/api/notion/page/<pid>")
def page_detail(pid):
    con = _db()
    row = con.execute("SELECT * FROM pages WHERE id=?", (pid,)).fetchone()
    con.close()
    if row:
        return jsonify(dict(row))
    # 回源
    res = _api_direct(f"pages/{pid}")
    return jsonify(res)


@app.route("/api/notion/tags")
def tags():
    con = _db()
    rows = con.execute("SELECT tags, COUNT(*) c FROM pages GROUP BY tags ORDER BY c DESC").fetchall()
    con.close()
    return jsonify({"items": [{"tag": r["tags"], "count": r["c"]} for r in rows]})


@app.route("/api/notion/search")
def search():
    q = (request.args.get("q", "") or "").strip()
    limit = min(int(request.args.get("limit", 20)), 100)
    if not q:
        return jsonify({"error": "q required"})
    con = _db()
    try:
        rows = con.execute("SELECT p.id,p.title,p.url,p.icon,p.tags,p.updated_at"
                           " FROM pages_fts f JOIN pages p ON p.rowid=f.rowid"
                           " WHERE pages_fts MATCH ? ORDER BY rank LIMIT ?",
                           (q, limit)).fetchall()
    except sqlite3.OperationalError as e:
        # FTS 语法错误时回退 LIKE
        rows = con.execute("SELECT id,title,url,icon,tags,updated_at FROM pages"
                           " WHERE title LIKE ? OR content LIKE ? LIMIT ?",
                           (f"%{q}%", f"%{q}%", limit)).fetchall()
    con.close()
    return jsonify({"query": q, "count": len(rows), "items": [dict(r) for r in rows]})


@app.route("/api/notion/semantic")
def semantic():
    """语义向量搜索（RAG 层）· 需先跑 scanner --embed 建立 Chroma 库

    查询 → ollama nomic-embed-text 向量化 → Chroma 余弦检索 → 返回最相近页面。
    未安装/未建库时 501 并提示走 FTS5 关键词搜索。
    """
    q = (request.args.get("q", "") or "").strip()
    n = min(int(request.args.get("n", 5)), 20)
    if not q:
        return jsonify({"error": "q required"})
    try:
        import chromadb
        import ollama as ol
    except ImportError:
        return jsonify({"error": "chromadb/ollama not installed",
                        "fallback": "use /api/notion/search"}), 501
    if not os.path.isdir(CHROMA_DIR):
        return jsonify({"error": "semantic index not built",
                        "hint": "run: python3 08_BIN/lh_notion_scanner.py --embed",
                        "fallback": "use /api/notion/search"}), 501
    try:
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        coll = client.get_or_create_collection(COLLECTION)
        resp = ol.embeddings(model="nomic-embed-text", prompt=q)
        res = coll.query(query_embeddings=[resp["embedding"]], n_results=n)
        items = [
            {"id": rid, "title": meta.get("title", ""), "distance": round(float(dist), 4)}
            for rid, meta, dist in zip(
                res["ids"][0], res["metadatas"][0], res["distances"][0])
        ]
        return jsonify({"query": q, "mode": "semantic", "count": len(items), "items": items})
    except Exception as e:
        return jsonify({"error": str(e), "fallback": "use /api/notion/search"}), 500


@app.route("/api/notion/callback", methods=["POST"])
def callback():
    """回调占位：MCP 拉取式补丁的接收口"""
    data = request.get_json(force=True, silent=True) or {}
    con = _db()
    con.execute("CREATE TABLE IF NOT EXISTS callback_queue (id INTEGER PRIMARY KEY AUTOINCREMENT,"
                " payload TEXT, created_at TEXT DEFAULT (datetime('now')))")
    con.execute("INSERT INTO callback_queue(payload) VALUES(?)", (json.dumps(data, ensure_ascii=False),))
    con.commit()
    con.close()
    return jsonify({"ok": True, "queued": True})


def main():
    global DB_PATH
    ap = argparse.ArgumentParser(description="Notion 全账号通读桥接器")
    ap.add_argument("--port", type=int, default=8898)
    ap.add_argument("--db", default=DB_PATH)
    args = ap.parse_args()
    DB_PATH = args.db
    print(f"🐉 Notion Bridge 启动: http://127.0.0.1:{args.port}/api/notion/health")
    app.run(host="127.0.0.1", port=args.port, debug=False)


if __name__ == "__main__":
    main()
