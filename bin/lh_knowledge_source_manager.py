#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·☴巽-KNOWLEDGE-SOURCE-MANAGER-v1.0-a3d7f162
# 创建者: 诸葛鑫 (UID9622)
# 协议: CC BY-NC-SA 4.0（君子协议，来源链不可切断）
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂 · 自动学习知识源管理器 v1.0

功能：
  1. 订阅固定知识源（GitHub Repo / RSS / 博客 / 论文库）
  2. 自动检测更新（指纹对比）
  3. 增量拉取新内容
  4. 自动喂入学习引擎（Inbox → DNA → Tasks）
  5. 来源追溯和更新记录

用法：
  python3 bin/lh_knowledge_source_manager.py --add --name "龙魂系统" --type github --url "https://github.com/UID9622/longhun-system"
  python3 bin/lh_knowledge_source_manager.py --scan                   # 扫描所有源更新
  python3 bin/lh_knowledge_source_manager.py --scan --source-id 1     # 扫描指定源
  python3 bin/lh_knowledge_source_manager.py --status                 # 查看所有源状态
  python3 bin/lh_knowledge_source_manager.py --auto --interval 3600   # 持续监控模式
"""

import os
import sys
import json
import sqlite3
import hashlib
import datetime
import time
import re
import socket
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Dict, List, Optional

# 全局网络超时：防止 urllib 在 IPv6 不可达等场景下长时间阻塞
socket.setdefaulttimeout(20)

# ============================================================
# 配置
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "knowledge_sources.db"
LEARNING_DB = DATA_DIR / "learning_engine.db"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

DATA_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)

# 把项目根目录加入 sys.path 以便导入学习引擎
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "bin") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "bin"))


# ============================================================
# 数据库初始化
# ============================================================

def init_db():
    conn = sqlite3.connect(str(DB_PATH), timeout=20.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    cursor = conn.cursor()

    # 知识源表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            url TEXT NOT NULL,
            config TEXT,
            status TEXT DEFAULT 'active',
            last_scan TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 内容指纹表（用于检测更新）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS content_fingerprints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id INTEGER,
            content_hash TEXT NOT NULL,
            content_path TEXT,
            title TEXT,
            detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ingested INTEGER DEFAULT 0,
            FOREIGN KEY(source_id) REFERENCES sources(id)
        )
    ''')

    # 更新记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS update_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id INTEGER,
            new_items INTEGER DEFAULT 0,
            ingested_items INTEGER DEFAULT 0,
            scan_duration REAL,
            error TEXT,
            scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(source_id) REFERENCES sources(id)
        )
    ''')

    # 内容-学习引擎关联表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS content_learning_link (
            content_hash TEXT PRIMARY KEY,
            inbox_id INTEGER,
            dna_id INTEGER,
            linked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print(f"✅ 知识源数据库已初始化: {DB_PATH}")


# ============================================================
# 工具函数
# ============================================================

def get_db(timeout: float = 20.0):
    conn = sqlite3.connect(str(DB_PATH), timeout=timeout)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def get_learning_db(timeout: float = 20.0):
    conn = sqlite3.connect(str(LEARNING_DB), timeout=timeout)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def compute_hash(content: str) -> str:
    return hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]


def _fetch_github_raw(owner: str, repo: str, path: str, timeout: int = 15) -> Optional[str]:
    """通过 GitHub Contents API 获取单个文件原始内容。

    不依赖 raw.githubusercontent.com（在该域名不可达的环境会阻塞），
    而是使用可正常访问的 api.github.com + Accept: application/vnd.github.v3.raw。
    """
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    req = urllib.request.Request(api_url, headers={
        "Accept": "application/vnd.github.v3.raw",
        "User-Agent": "Mozilla/5.0"
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except Exception:
        return None


def extract_github_content(url: str, path: str = "", max_files: int = 10, max_bytes: int = 500_000) -> List[Dict]:
    """从GitHub仓库提取内容

    修复：
      1. 限制处理文件数量与大小，防止文件过多时长时间阻塞。
      2. raw.githubusercontent.com 不可达时，改用 GitHub Contents API 取原始内容。
      3. 优先取 README，再取少量文档/配置，降低未认证 API 速率限制风险。
    """
    results = []

    if "github.com" not in url:
        return results

    parts = url.replace("https://github.com/", "").split("/")
    if len(parts) < 2:
        return results

    owner = parts[0]
    repo = parts[1].split("?")[0]

    try:
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        req = urllib.request.Request(api_url, headers={
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Mozilla/5.0"
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))

        if not isinstance(data, list):
            return results

        # 优先 README，再挑选小体积文档/配置，跳过签名文件
        candidates = []
        for item in data:
            if item.get("type") != "file":
                continue
            name = item.get("name", "")
            if name.endswith(".asc") or name.endswith(".sig"):
                continue
            size = item.get("size", 0)
            if size > max_bytes:
                continue
            if any(ext in name for ext in [".md", ".txt", ".py", ".json", ".yaml"]):
                candidates.append(item)

        # README 排最前，其余按大小升序，限制总数
        candidates.sort(key=lambda x: (0 if x.get("name", "").lower().startswith("readme") else 1, x.get("size", 0)))

        for item in candidates[:max_files]:
            name = item.get("name", "未知文件")
            file_path = item.get("path", "")
            content = _fetch_github_raw(owner, repo, file_path)
            if content is None:
                continue
            results.append({
                "title": name,
                "content": content[:5000],
                "path": file_path,
                "type": "file",
                "url": item.get("html_url", f"https://github.com/{owner}/{repo}/blob/main/{file_path}")
            })

    except urllib.error.HTTPError as e:
        print(f"⚠️ GitHub API 调用失败: HTTP {e.code}")
    except Exception as e:
        print(f"⚠️ GitHub API 调用失败: {e}")

    return results


def _parse_rss_xml(xml_text: str, limit: int = 20) -> List[Dict]:
    """使用标准库 xml.etree.ElementTree 解析 RSS/Atom，消除 feedparser 依赖"""
    results = []
    try:
        import xml.etree.ElementTree as ET
        root = ET.fromstring(xml_text)
    except Exception:
        return results

    # 处理 Atom (namespace)
    atom_ns = "{http://www.w3.org/2005/Atom}"
    is_atom = root.tag.startswith(atom_ns)

    if is_atom:
        for entry in root.findall(f"{atom_ns}entry")[:limit]:
            title = ""
            t = entry.find(f"{atom_ns}title")
            if t is not None and t.text:
                title = t.text.strip()
            link = ""
            l = entry.find(f"{atom_ns}link")
            if l is not None:
                link = l.get("href", "")
            content = ""
            for tag in (f"{atom_ns}summary", f"{atom_ns}content", f"{atom_ns}description"):
                c = entry.find(tag)
                if c is not None and c.text:
                    content = c.text.strip()
                    break
            results.append({
                "title": title or "未知",
                "content": content[:5000],
                "path": link,
                "type": "feed",
                "url": link
            })
        return results

    # 处理 RSS 2.0 / 1.0
    channel = root.find("channel")
    if channel is None:
        # RSS 1.0 根是 rdf:RDF，条目为 item
        items = root.findall("item")
    else:
        items = channel.findall("item")

    for item in items[:limit]:
        title = ""
        t = item.find("title")
        if t is not None and t.text:
            title = t.text.strip()
        link = ""
        l = item.find("link")
        if l is not None and l.text:
            link = l.text.strip()
        content = ""
        for tag in ("description", "summary", "content"):
            c = item.find(tag)
            if c is not None and c.text:
                content = c.text.strip()
                break
        results.append({
            "title": title or "未知",
            "content": content[:5000],
            "path": link,
            "type": "feed",
            "url": link
        })
    return results


def extract_rss_content(url: str, limit: int = 20) -> List[Dict]:
    """从RSS/Atom订阅源提取内容"""
    results = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            xml_text = resp.read().decode('utf-8', errors='ignore')

        # 优先使用标准库解析
        results = _parse_rss_xml(xml_text, limit)

        # 标准库解析失败且 feedparser 可用时回退
        if not results:
            try:
                import feedparser
                feed = feedparser.parse(xml_text)
                for entry in feed.entries[:limit]:
                    content = entry.get("summary", "") or entry.get("description", "") or ""
                    results.append({
                        "title": entry.get("title", "未知"),
                        "content": content[:5000],
                        "path": entry.get("link", ""),
                        "type": "feed",
                        "url": entry.get("link", "")
                    })
            except ImportError:
                pass
    except urllib.error.HTTPError as e:
        print(f"⚠️ RSS 请求失败: HTTP {e.code}")
    except Exception as e:
        print(f"⚠️ RSS 解析失败: {e}")
    return results


def extract_web_content(url: str) -> List[Dict]:
    """从普通网页提取内容（简化）"""
    results = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            title = title_match.group(1) if title_match else "未知页面"
            text = re.sub(r'<[^>]+>', ' ', content)
            text = re.sub(r'\s+', ' ', text)[:5000]
            results.append({
                "title": title,
                "content": text,
                "path": url,
                "type": "web",
                "url": url
            })
    except Exception as e:
        print(f"⚠️ 网页抓取失败: {e}")
    return results


# ============================================================
# 知识源管理器
# ============================================================

class KnowledgeSourceManager:
    def __init__(self):
        self._init_if_needed()

    def _init_if_needed(self):
        if not DB_PATH.exists():
            init_db()

    def add_source(self, name: str, type_: str, url: str, config: str = "") -> int:
        """添加知识源"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sources (name, type, url, config) VALUES (?, ?, ?, ?)",
            (name, type_, url, config)
        )
        conn.commit()
        source_id = cursor.lastrowid
        conn.close()
        print(f"📡 已添加知识源: {name} (ID: {source_id})")
        return source_id

    def list_sources(self) -> List[Dict]:
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sources ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_source(self, source_id: int) -> Optional[Dict]:
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sources WHERE id = ?", (source_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def scan_source(self, source_id: int) -> Dict:
        """扫描单个知识源，检测更新"""
        source = self.get_source(source_id)
        if not source:
            return {"error": "源不存在"}

        start_time = time.time()
        new_items = 0
        ingested_items = 0
        items = []

        # 根据类型拉取内容
        if source["type"] == "github":
            items = extract_github_content(source["url"])
        elif source["type"] == "rss":
            items = extract_rss_content(source["url"])
        elif source["type"] == "web":
            items = extract_web_content(source["url"])
        else:
            return {"error": f"不支持的类型: {source['type']}"}

        # 限制单次扫描处理量，防止大源阻塞自动监控/手动扫描
        items = items[:20]

        # 检测新内容
        conn = get_db()
        cursor = conn.cursor()

        for item in items:
            content_hash = compute_hash(item["content"])
            cursor.execute(
                "SELECT id, ingested FROM content_fingerprints WHERE source_id = ? AND content_hash = ?",
                (source_id, content_hash)
            )
            existing = cursor.fetchone()

            if not existing:
                cursor.execute(
                    "INSERT INTO content_fingerprints (source_id, content_hash, content_path, title, ingested) VALUES (?, ?, ?, ?, ?)",
                    (source_id, content_hash, item.get("path", ""), item["title"], 0)
                )
                new_items += 1

                # 自动喂入学习引擎（传入外层连接，避免同库嵌套连接导致 database is locked）
                if len(item["content"]) > 100:
                    ingested = self._ingest_to_learning(item, source_id, content_hash, source_conn=conn)
                    if ingested:
                        ingested_items += 1

        # 更新扫描记录
        duration = time.time() - start_time
        cursor.execute('''
            INSERT INTO update_history (source_id, new_items, ingested_items, scan_duration)
            VALUES (?, ?, ?, ?)
        ''', (source_id, new_items, ingested_items, duration))

        cursor.execute(
            "UPDATE sources SET last_scan = CURRENT_TIMESTAMP WHERE id = ?",
            (source_id,)
        )
        conn.commit()
        conn.close()

        return {
            "source_id": source_id,
            "source_name": source["name"],
            "new_items": new_items,
            "ingested_items": ingested_items,
            "duration": round(duration, 2),
            "status": "success"
        }

    def scan_all(self) -> List[Dict]:
        """扫描所有知识源"""
        sources = self.list_sources()
        results = []
        for src in sources:
            if src["status"] == "active":
                result = self.scan_source(src["id"])
                results.append(result)
                time.sleep(1)
        return results

    def _ingest_to_learning(self, item: Dict, source_id: int, content_hash: str,
                            source_conn: Optional[sqlite3.Connection] = None) -> bool:
        """将内容喂入学习引擎 — 使用真实可用的 lh_learning_engine API"""
        try:
            # 导入学习引擎模块
            from lh_learning_engine import add_inbox, auto_digest_inbox, create_dna, add_task

            title = item["title"][:100]
            content = item["content"][:5000]
            link = item.get("url", "")

            # 1. 添加到学习引擎 Inbox
            inbox_id = add_inbox(
                title=title,
                type_="KnowledgeSource",
                link=link,
                raw_content=content,
                source=f"source_id:{source_id}"
            )

            # 2. 自动拆解 DNA（规则降级）
            digest_result = auto_digest_inbox(inbox_id=inbox_id, use_llm=False)

            dna_id = None
            if digest_result.get("core_concept"):
                dna_info = digest_result
                dna_id = create_dna(
                    inbox_id=inbox_id,
                    core_concept=dna_info.get("core_concept", title)[:100],
                    direction=dna_info.get("direction", "未知"),
                    difficulty=dna_info.get("difficulty", 3),
                    value_score=dna_info.get("value_score", 5),
                    pollution_risk=dna_info.get("pollution_risk", 30)
                )

                # 3. 自动生成学习任务
                if dna_id:
                    add_task(
                        task_name=f"学习: {title[:80]}",
                        dna_id=dna_id,
                        mode="扫盲",
                        priority=3,
                        description=f"来源: {link}\n{content[:200]}"
                    )

            # 4. 记录关联（复用外层连接，避免同库锁竞争）
            if source_conn:
                cursor = source_conn.cursor()
                cursor.execute(
                    "INSERT OR REPLACE INTO content_learning_link (content_hash, inbox_id, dna_id) VALUES (?, ?, ?)",
                    (content_hash, inbox_id, dna_id)
                )
            else:
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR REPLACE INTO content_learning_link (content_hash, inbox_id, dna_id) VALUES (?, ?, ?)",
                    (content_hash, inbox_id, dna_id)
                )
                conn.commit()
                conn.close()

            # 5. 标记为已摄入
            if source_conn:
                cursor = source_conn.cursor()
                cursor.execute(
                    "UPDATE content_fingerprints SET ingested = 1 WHERE source_id = ? AND content_hash = ?",
                    (source_id, content_hash)
                )
            else:
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE content_fingerprints SET ingested = 1 WHERE source_id = ? AND content_hash = ?",
                    (source_id, content_hash)
                )
                conn.commit()
                conn.close()

            return True
        except Exception as e:
            print(f"⚠️ 喂入学习引擎失败: {e}")
            return False

    def get_status(self) -> Dict:
        """获取所有源的状态"""
        sources = self.list_sources()
        conn = get_db()
        cursor = conn.cursor()

        status = []
        for src in sources:
            cursor.execute(
                "SELECT COUNT(*) FROM content_fingerprints WHERE source_id = ?",
                (src["id"],)
            )
            total_items = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM content_fingerprints WHERE source_id = ? AND ingested = 1",
                (src["id"],)
            )
            ingested_items = cursor.fetchone()[0]

            cursor.execute(
                "SELECT MAX(scanned_at) FROM update_history WHERE source_id = ?",
                (src["id"],)
            )
            last_scan_row = cursor.fetchone()
            last_scan = last_scan_row[0] if last_scan_row else "从未"

            status.append({
                "id": src["id"],
                "name": src["name"],
                "type": src["type"],
                "total_items": total_items,
                "ingested_items": ingested_items,
                "last_scan": last_scan,
                "status": src["status"]
            })

        conn.close()
        return {"sources": status, "total": len(status)}

    def status_summary(self):
        status = self.get_status()
        print("\n📡 知识源状态")
        print("=" * 60)
        for s in status["sources"]:
            print(f"  📌 {s['name']} ({s['type']})")
            print(f"     内容: {s['total_items']} 条 | 已摄入: {s['ingested_items']} 条")
            print(f"     最后扫描: {s['last_scan']}")
            print()

    def auto_monitor(self, interval: int = 3600):
        """持续监控模式"""
        print(f"🔄 启动持续监控 (间隔: {interval}s)")
        print("按 Ctrl+C 停止")
        try:
            while True:
                print(f"\n⏰ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                results = self.scan_all()
                for r in results:
                    if r.get("new_items", 0) > 0:
                        print(f"  📥 {r['source_name']}: {r['new_items']} 条新内容 "
                              f"(已摄入 {r['ingested_items']} 条)")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n👋 监控已停止")


# ============================================================
# 预置知识源（取之不竭的知识库）
# ============================================================

PRESET_SOURCES = [
    {
        "name": "龙魂系统核心库",
        "type": "github",
        "url": "https://github.com/UID9622/longhun-system",
        "config": "core"
    },
    {
        "name": "arXiv AI 论文",
        "type": "rss",
        "url": "https://export.arxiv.org/rss/cs.AI",
        "config": "papers"
    },
    {
        "name": "arXiv 机器学习",
        "type": "rss",
        "url": "https://export.arxiv.org/rss/cs.LG",
        "config": "papers"
    },
    {
        "name": "Hacker News 技术",
        "type": "rss",
        "url": "https://hnrss.org/frontpage",
        "config": "tech_news"
    },
    {
        "name": "龙魂官网博客",
        "type": "web",
        "url": "https://uid9622.cn",
        "config": "blog"
    }
]


def setup_preset_sources():
    """初始化预置知识源"""
    manager = KnowledgeSourceManager()
    existing = manager.list_sources()
    existing_names = {s["name"] for s in existing}

    count = 0
    for src in PRESET_SOURCES:
        if src["name"] not in existing_names:
            manager.add_source(src["name"], src["type"], src["url"], src["config"])
            count += 1

    if count > 0:
        print(f"✅ 已添加 {count} 个预置知识源")
    else:
        print("📭 所有预置源已存在")


# ============================================================
# 命令行入口
# ============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="龙魂 · 自动学习知识源管理器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 初始化数据库
  python3 bin/lh_knowledge_source_manager.py --init

  # 添加知识源
  python3 bin/lh_knowledge_source_manager.py --add --name "AI论文" --type rss --url "http://export.arxiv.org/rss/cs.AI"

  # 添加预置源
  python3 bin/lh_knowledge_source_manager.py --preset

  # 扫描所有源更新
  python3 bin/lh_knowledge_source_manager.py --scan

  # 扫描指定源
  python3 bin/lh_knowledge_source_manager.py --scan --source-id 1

  # 查看状态
  python3 bin/lh_knowledge_source_manager.py --status

  # 持续监控 (每小时)
  python3 bin/lh_knowledge_source_manager.py --auto --interval 3600
        """
    )

    parser.add_argument("--init", action="store_true", help="初始化数据库")
    parser.add_argument("--add", action="store_true", help="添加知识源")
    parser.add_argument("--name", type=str, help="知识源名称")
    parser.add_argument("--type", type=str, choices=["github", "rss", "web"], help="知识源类型")
    parser.add_argument("--url", type=str, help="知识源URL")
    parser.add_argument("--config", type=str, default="", help="配置")
    parser.add_argument("--preset", action="store_true", help="添加预置知识源")
    parser.add_argument("--scan", action="store_true", help="扫描更新")
    parser.add_argument("--source-id", type=int, help="指定源ID")
    parser.add_argument("--status", action="store_true", help="查看状态")
    parser.add_argument("--auto", action="store_true", help="持续监控模式")
    parser.add_argument("--interval", type=int, default=3600, help="监控间隔(秒)")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")

    args = parser.parse_args()

    if args.init:
        init_db()
        return

    manager = KnowledgeSourceManager()

    if args.preset:
        setup_preset_sources()
        return

    if args.add and args.name and args.type and args.url:
        manager.add_source(args.name, args.type, args.url, args.config)
        return

    if args.scan:
        if args.source_id:
            result = manager.scan_source(args.source_id)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            results = manager.scan_all()
            if args.json:
                print(json.dumps(results, ensure_ascii=False, indent=2))
            else:
                for r in results:
                    print(f"  📥 {r['source_name']}: {r['new_items']} 条新内容 "
                          f"(已摄入 {r['ingested_items']} 条)")
                print(f"✅ 扫描完成，共 {len(results)} 个源")
        return

    if args.status:
        if args.json:
            status = manager.get_status()
            print(json.dumps(status, ensure_ascii=False, indent=2))
        else:
            manager.status_summary()
        return

    if args.auto:
        manager.auto_monitor(args.interval)
        return

    # 默认显示帮助
    parser.print_help()


if __name__ == "__main__":
    main()
