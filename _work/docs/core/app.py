#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂本地引擎 v2.0 · 全自动摄入版
功能：对话 + CS知识库 + 自动摄入 sessions/ + memory.jsonl + plans/

DNA: #龍芯⚡️2026-04-03-LOCAL-ENGINE-全自动版
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
创建者: UID9622 诸葛鑫
理论指导: 曾仕强老师（永恒显示）

保存为: ~/longhun-system/app.py
"""

import json
import sqlite3
import hashlib
import os
import glob
import re
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

# ============================================================
# 配置
# ============================================================

BASE_DIR = Path.home() / "longhun-system"
SESSIONS_DIR = BASE_DIR / "sessions"
MEMORY_FILE = BASE_DIR / "memory.jsonl"
PLANS_DIR = BASE_DIR / "plans"
KNOWLEDGE_DB = BASE_DIR / "knowledge.db"
CS_CARDS_FILE = BASE_DIR / "cs_cards.json"

for d in [SESSIONS_DIR, PLANS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ============================================================
# 初始化知识库（SQLite）
# ============================================================

def init_knowledge_db():
    conn = sqlite3.connect(KNOWLEDGE_DB)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY,
            source TEXT,
            title TEXT,
            content TEXT,
            compressed TEXT,
            dna TEXT UNIQUE,
            tags TEXT,
            timestamp TEXT,
            status TEXT DEFAULT 'active'
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY,
            content TEXT,
            tags TEXT,
            dna TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_knowledge_db()

# ============================================================
# 自动摄入：sessions/ 目录
# ============================================================

def ingest_sessions():
    """摄入所有 session 文件到 knowledge.db"""
    files = list(SESSIONS_DIR.glob("session_*.md"))
    if not files:
        return 0
    
    ingested = 0
    conn = sqlite3.connect(KNOWLEDGE_DB)
    
    for f in files:
        # 检查是否已摄入（用文件路径作为唯一标识）
        existing = conn.execute(
            "SELECT id FROM knowledge WHERE source = ?", (str(f),)
        ).fetchone()
        if existing:
            continue
        
        content = f.read_text(encoding="utf-8")
        title = f.name.replace(".md", "")
        
        # 生成DNA
        dna_data = f"{title}|{content[:500]}|{datetime.now().isoformat()}"
        dna_hash = hashlib.sha256(dna_data.encode()).hexdigest()[:24]
        dna = f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-SESSION-{dna_hash}"
        
        conn.execute('''
            INSERT INTO knowledge (source, title, content, compressed, dna, tags, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (str(f), title, content[:5000], content[:800], dna, "会话归档", datetime.now().isoformat()))
        ingested += 1
    
    conn.commit()
    conn.close()
    return ingested

# ============================================================
# 自动摄入：memory.jsonl
# ============================================================

def ingest_memory_jsonl():
    """摄入 memory.jsonl 到 memory 表"""
    if not MEMORY_FILE.exists():
        return 0
    
    ingested = 0
    conn = sqlite3.connect(KNOWLEDGE_DB)
    
    with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                # 检查是否已存在（用内容+时间戳）
                existing = conn.execute(
                    "SELECT id FROM memory WHERE content = ? AND timestamp = ?",
                    (data.get('content', '')[:200], data.get('t', ''))
                ).fetchone()
                if existing:
                    continue
                
                conn.execute('''
                    INSERT INTO memory (content, tags, dna, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', (
                    data.get('content', ''),
                    data.get('type', 'idea'),
                    data.get('dna', ''),
                    data.get('t', datetime.now().isoformat())
                ))
                ingested += 1
            except json.JSONDecodeError:
                continue
    
    conn.commit()
    conn.close()
    return ingested

# ============================================================
# 自动摄入：plans/ 目录
# ============================================================

def ingest_plans():
    """摄入 plans/ 目录下的 md 文件"""
    files = list(PLANS_DIR.glob("*.md"))
    if not files:
        return 0
    
    ingested = 0
    conn = sqlite3.connect(KNOWLEDGE_DB)
    
    for f in files:
        existing = conn.execute(
            "SELECT id FROM knowledge WHERE source = ?", (str(f),)
        ).fetchone()
        if existing:
            continue
        
        content = f.read_text(encoding="utf-8")
        title = f.name.replace(".md", "")
        
        dna_data = f"{title}|{content[:500]}|{datetime.now().isoformat()}"
        dna_hash = hashlib.sha256(dna_data.encode()).hexdigest()[:24]
        dna = f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-PLAN-{dna_hash}"
        
        conn.execute('''
            INSERT INTO knowledge (source, title, content, compressed, dna, tags, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (str(f), title, content[:5000], content[:500], dna, "计划", datetime.now().isoformat()))
        ingested += 1
    
    conn.commit()
    conn.close()
    return ingested

# ============================================================
# 搜索知识库
# ============================================================

def search_knowledge(query: str) -> list:
    """搜索知识库，返回匹配的条目"""
    conn = sqlite3.connect(KNOWLEDGE_DB)
    keywords = query.split()[:5]
    
    results = []
    for kw in keywords:
        if len(kw) < 2:
            continue
        rows = conn.execute(
            "SELECT title, compressed, tags, source FROM knowledge WHERE content LIKE ? OR title LIKE ? LIMIT 3",
            (f'%{kw}%', f'%{kw}%')
        ).fetchall()
        for row in rows:
            results.append({
                "title": row[0],
                "compressed": row[1][:300],
                "tags": row[2],
                "source": row[3]
            })
    
    conn.close()
    # 去重
    seen = set()
    unique = []
    for r in results:
        key = r["title"]
        if key not in seen:
            seen.add(key)
            unique.append(r)
    return unique[:5]

# ============================================================
# 自动摄入所有（启动时执行）
# ============================================================

def auto_ingest_all():
    """启动时自动摄入所有本地数据"""
    print("📥 自动摄入中...")
    s = ingest_sessions()
    m = ingest_memory_jsonl()
    p = ingest_plans()
    print(f"✅ 已摄入: sessions={s}, memory={m}, plans={p}")
    return s + m + p

# ============================================================
# CS知识库加载（原有）
# ============================================================

cs_cards = []
if CS_CARDS_FILE.exists():
    try:
        with open(CS_CARDS_FILE, 'r', encoding='utf-8') as f:
            cs_cards = json.load(f)
        print(f"📚 CS知识库已加载 ({len(cs_cards)} 张卡片)")
    except:
        pass

# ============================================================
# HTTP 服务
# ============================================================

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 静态文件服务
        if self.path.startswith('/static/'):
            file_path = BASE_DIR / self.path[1:]  # 去掉开头的 /
            if file_path.exists() and file_path.is_file():
                self.send_response(200)
                # 根据扩展名设置 Content-Type
                if str(file_path).endswith('.ttf'):
                    self.send_header('Content-Type', 'font/ttf')
                elif str(file_path).endswith('.css'):
                    self.send_header('Content-Type', 'text/css')
                elif str(file_path).endswith('.js'):
                    self.send_header('Content-Type', 'application/javascript')
                else:
                    self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
                return
            else:
                self.send_response(404)
                self.end_headers()
                return
        
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "engine": "龍魂v2.0"}).encode())
            return
        
        if self.path == '/stats':
            conn = sqlite3.connect(KNOWLEDGE_DB)
            k_count = conn.execute("SELECT COUNT(*) FROM knowledge").fetchone()[0]
            m_count = conn.execute("SELECT COUNT(*) FROM memory").fetchone()[0]
            conn.close()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "knowledge_count": k_count,
                "memory_count": m_count,
                "sessions_dir": str(SESSIONS_DIR),
                "cs_cards": len(cs_cards)
            }).encode())
            return
        
        self.send_response(404)
        self.end_headers()
    
    def do_POST(self):
        if self.path == '/chat':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode()
            try:
                data = json.loads(body)
                messages = data.get('messages', [])
                user_msg = ""
                for m in messages:
                    if m.get('role') == 'user':
                        user_msg = m.get('content', '')
                        break
                
                if not user_msg:
                    user_msg = data.get('message', '')
                
                # 搜索知识库
                knowledge_hits = search_knowledge(user_msg)
                
                # 构建回复
                reply = f"🐉 龍魂已收到：{user_msg[:50]}"
                if knowledge_hits:
                    reply += "\n\n📚 相关知识："
                    for hit in knowledge_hits[:2]:
                        reply += f"\n• {hit['title']}: {hit['compressed']}..."
                else:
                    reply += "\n\n💡 当前知识库暂无相关内容。"
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"reply": reply}).encode())
                
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return
        
        self.send_response(404)
        self.end_headers()

# ============================================================
# 主程序
# ============================================================

def main():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🐉 龍魂本地引擎 v2.0 · 全自动摄入版")
    print("DNA: #龍芯⚡️2026-04-03-LOCAL-ENGINE-全自动版")
    print("确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # 自动摄入所有本地数据
    total = auto_ingest_all()
    print(f"📦 总摄入: {total} 条新数据")
    
    # 启动服务
    port = 8000
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"\n🚀 龍魂服务已启动: http://localhost:{port}")
    print(f"📁 sessions目录: {SESSIONS_DIR}")
    print(f"📁 memory文件: {MEMORY_FILE}")
    print(f"📁 plans目录: {PLANS_DIR}")
    print("\n按 Ctrl+C 停止服务")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 服务已停止")

if __name__ == "__main__":
    main()
