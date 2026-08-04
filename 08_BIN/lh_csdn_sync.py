#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·丙申·戊申·申时·䷗复-CSDN-SYNC-ENGINE-v1.0
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂·CSDN博客 → Notion + 鲲鹏知识库 自动同步引擎 v1.0

功能:
  1. 抓取CSDN博客所有文章 (支持分页/增量)
  2. 解析文章内容、标签、发布时间、DNA追溯码
  3. 同步到Notion数据库 (结构化存储)
  4. 归档到本地鲲鹏知识库 (Markdown + JSON元数据 + 全文索引)
  5. 三色审计标记 + GPG签名 + DNA追溯

依赖: requests, beautifulsoup4, lxml, notion-client
用法:
  python3 bin/lh_csdn_sync.py --sync                  # 全量同步
  python3 bin/lh_csdn_sync.py --sync --latest          # 仅同步最新
  python3 bin/lh_csdn_sync.py --sync --incremental     # 增量同步(新增+变更)
  python3 bin/lh_csdn_sync.py --notion-only            # 仅同步到Notion
  python3 bin/lh_csdn_sync.py --local-only             # 仅归档本地
  python3 bin/lh_csdn_sync.py --build-index            # 重建本地索引
  python3 bin/lh_csdn_sync.py --status                 # 查看同步状态
  python3 bin/lh_csdn_sync.py --export --format json   # 导出文章数据
"""

import os
import sys
import json
import re
import time
import hashlib
import sqlite3
import logging
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict, field

import requests
from bs4 import BeautifulSoup

# ============================================================
# 路径 & 自举
# ============================================================
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "bin"))
sys.path.insert(0, str(ROOT))

# 尝试导入时间引擎
try:
    from lh_time_engine import get_output_stamp, get_compact_dna
    HAS_TIME_ENGINE = True
except ImportError:
    HAS_TIME_ENGINE = False
    def get_output_stamp():
        return f"[{datetime.now().isoformat()}]"
    def get_compact_dna():
        return "#龍芯⚡️CSDN-SYNC"

# Notion SDK (可选)
try:
    from notion_client import Client as NotionClient
    HAS_NOTION = True
except ImportError:
    HAS_NOTION = False
    NotionClient = None

# ============================================================
# 配置
# ============================================================
TZ = timezone(timedelta(hours=8))  # 北京时间

CONFIG = {
    "CSDN_BLOG_URL": "https://blog.csdn.net/UID9622",
    "CSDN_USERNAME": "UID9622",
    "CSDN_ARTICLE_API": "https://blog.csdn.net/community/home-api/v1/get-business-list",
    # Notion (从环境变量读取)
    "NOTION_TOKEN": os.environ.get("NOTION_TOKEN", ""),
    "NOTION_DATABASE_ID": os.environ.get("NOTION_CSDN_DB_ID", ""),
    "NOTION_VERSION": "2022-06-28",
    # 本地存储
    "LOCAL_STORAGE_DIR": ROOT / "archive" / "csdn_sync",
    "DB_PATH": ROOT / "data" / "csdn_sync.db",
    "EXPORT_DIR": ROOT / "archive" / "csdn_export",
    # 请求参数
    "REQUEST_DELAY": 1.0,
    "MAX_RETRIES": 3,
    "PAGE_SIZE": 40,
    "MAX_PAGES": 50,
    "USER_AGENT": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
}

# 确保目录存在
for d in [CONFIG["LOCAL_STORAGE_DIR"], CONFIG["DB_PATH"].parent, CONFIG["EXPORT_DIR"]]:
    d.mkdir(parents=True, exist_ok=True)

# ============================================================
# 日志
# ============================================================
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] 🐉 %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_DIR / "csdn_sync.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("csdn_sync")

# ============================================================
# 数据模型
# ============================================================

@dataclass
class CSDNArticle:
    """CSDN文章"""
    article_id: str
    title: str
    url: str
    content_html: str = ""
    content_text: str = ""
    summary: str = ""
    tags: List[str] = field(default_factory=list)
    column: str = ""
    publish_time: str = ""
    update_time: str = ""
    view_count: int = 0
    like_count: int = 0
    comment_count: int = 0
    collect_count: int = 0
    dna_code: str = ""
    status: str = "active"
    sync_time: str = ""

    def __post_init__(self):
        if not self.sync_time:
            self.sync_time = datetime.now(TZ).isoformat()

    def to_dict(self) -> Dict:
        return asdict(self)

    def content_hash(self) -> str:
        return hashlib.sha256(self.content_text.encode()).hexdigest()[:16]

    @property
    def safe_filename(self) -> str:
        safe = re.sub(r'[^\w\s-]', '', self.title)
        safe = re.sub(r'[-\s]+', '-', safe).strip('-')[:50]
        return f"{self.article_id}_{safe}"

# ============================================================
# 本地数据库
# ============================================================

class SyncDB:
    """SQLite本地同步状态库"""

    def __init__(self, db_path: Path = None):
        self.db_path = db_path or CONFIG["DB_PATH"]
        self._init()

    def _init(self):
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                article_id TEXT PRIMARY KEY,
                title TEXT,
                url TEXT,
                content_hash TEXT,
                publish_time TEXT,
                tags TEXT,
                column_name TEXT,
                dna_code TEXT,
                notion_synced INTEGER DEFAULT 0,
                local_archived INTEGER DEFAULT 0,
                first_sync TEXT,
                last_sync TEXT,
                sync_count INTEGER DEFAULT 0
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS sync_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sync_time TEXT,
                mode TEXT,
                total_fetched INTEGER,
                new_synced INTEGER,
                updated INTEGER,
                skipped INTEGER,
                failed INTEGER,
                notion_ok INTEGER DEFAULT 0,
                local_ok INTEGER DEFAULT 0,
                status TEXT,
                dna TEXT
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated TEXT
            )
        """)
        conn.commit()
        conn.close()

    def is_known(self, article_id: str) -> bool:
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("SELECT 1 FROM articles WHERE article_id=?", (article_id,))
        r = c.fetchone() is not None
        conn.close()
        return r

    def needs_update(self, article_id: str, new_hash: str) -> bool:
        """检查内容是否已变更"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("SELECT content_hash FROM articles WHERE article_id=?", (article_id,))
        row = c.fetchone()
        conn.close()
        if not row:
            return True
        return row[0] != new_hash

    def upsert_article(self, article: CSDNArticle, notion_ok: bool = False, local_ok: bool = False):
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        now = datetime.now(TZ).isoformat()
        c.execute("""
            INSERT INTO articles (article_id, title, url, content_hash, publish_time,
                tags, column_name, dna_code, notion_synced, local_archived, first_sync, last_sync, sync_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            ON CONFLICT(article_id) DO UPDATE SET
                title=excluded.title, content_hash=excluded.content_hash,
                publish_time=excluded.publish_time, tags=excluded.tags,
                column_name=excluded.column_name, dna_code=excluded.dna_code,
                notion_synced=MAX(articles.notion_synced, excluded.notion_synced),
                local_archived=MAX(articles.local_archived, excluded.local_archived),
                last_sync=excluded.last_sync,
                sync_count=articles.sync_count + 1
        """, (
            article.article_id, article.title, article.url, article.content_hash(),
            article.publish_time, json.dumps(article.tags, ensure_ascii=False),
            article.column, article.dna_code,
            1 if notion_ok else 0, 1 if local_ok else 0,
            now, now
        ))
        conn.commit()
        conn.close()

    def log_sync(self, **kwargs):
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        # 获取sync_log表实际列名，只插入存在的列
        c.execute("PRAGMA table_info(sync_log)")
        valid_cols = {row[1] for row in c.fetchall()}
        kwargs.setdefault("sync_time", datetime.now(TZ).isoformat())
        kwargs.setdefault("dna", get_compact_dna() if HAS_TIME_ENGINE else "")
        # 过滤并映射stats键 → 表列名
        filtered = {}
        for k, v in kwargs.items():
            if k in valid_cols:
                # SQLite不支持NaN，替换为0
                if isinstance(v, float) and (v != v):  # NaN check
                    v = 0
                filtered[k] = v
        if not filtered:
            conn.close()
            return
        fields = list(filtered.keys())
        placeholders = ", ".join(["?" for _ in fields])
        values = [filtered[f] for f in fields]
        c.execute(f"INSERT INTO sync_log ({', '.join(fields)}) VALUES ({placeholders})", values)
        conn.commit()
        conn.close()

    def get_stats(self) -> Dict:
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        stats = {}
        c.execute("SELECT COUNT(*) FROM articles"); stats["total"] = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM articles WHERE notion_synced=1"); stats["notion"] = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM articles WHERE local_archived=1"); stats["local"] = c.fetchone()[0]
        c.execute("SELECT MAX(last_sync) FROM articles"); stats["last_sync"] = c.fetchone()[0] or "从未"
        c.execute("SELECT COUNT(*) FROM sync_log"); stats["sync_runs"] = c.fetchone()[0]
        conn.close()
        return stats

    def get_unsynced(self, limit: int = 20) -> List[str]:
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("SELECT article_id FROM articles WHERE notion_synced=0 OR local_archived=0 LIMIT ?", (limit,))
        ids = [row[0] for row in c.fetchall()]
        conn.close()
        return ids

# ============================================================
# CSDN 抓取器
# ============================================================

class CSDNFetcher:
    """CSDN博客抓取器"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": CONFIG["USER_AGENT"],
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        })
        self.username = CONFIG["CSDN_USERNAME"]
        self._total_articles = 0

    def _request(self, url: str, params: dict = None, retries: int = None) -> requests.Response:
        retries = retries or CONFIG["MAX_RETRIES"]
        for attempt in range(retries):
            try:
                resp = self.session.get(url, params=params, timeout=30)
                resp.raise_for_status()
                return resp
            except requests.exceptions.RequestException as e:
                if attempt < retries - 1:
                    wait = (attempt + 1) * 2
                    logger.warning(f"请求失败 (尝试 {attempt+1}/{retries}), {wait}s后重试: {e}")
                    time.sleep(wait)
                else:
                    raise

    def get_article_list(self, page: int = 1, page_size: int = None) -> Tuple[List[Dict], int]:
        """获取文章列表 (HTML抓取为主，API为备)"""
        page_size = page_size or CONFIG["PAGE_SIZE"]
        # 主方案：HTML列表页抓取（API常被Cloudflare拦截）
        articles = self._scrape_list_html(page)
        if articles:
            return articles, self._total_articles

        # 备用方案：API（可能被521拦截）
        logger.info("HTML抓取为空，尝试API...")
        return self._fetch_list_api(page, page_size)

    def _scrape_list_html(self, page: int) -> List[Dict]:
        """从HTML列表页抓取文章列表"""
        list_url = f"https://blog.csdn.net/{self.username}/article/list/{page}"
        try:
            resp = self._request(list_url)
            soup = BeautifulSoup(resp.text, 'lxml')

            # 提取总数（仅第1页）
            if page == 1:
                total_match = re.search(r'(\d+)篇', resp.text)
                if total_match:
                    self._total_articles = int(total_match.group(1))

            articles = []
            for item in soup.select('.article-item-box'):
                h4 = item.select_one('h4 a') or item.select_one('h4')
                title = h4.get_text(strip=True) if h4 else ''
                # 去掉"原创"前缀
                title = re.sub(r'^原创\s*', '', title).strip()

                link = h4.get('href', '') if h4 and h4.name == 'a' else ''
                # 补全链接
                if link and not link.startswith('http'):
                    link = 'https://blog.csdn.net' + link if link.startswith('/') else ''

                # 提取 article_id
                aid_match = re.search(r'/article/details/(\d+)', link)
                article_id = aid_match.group(1) if aid_match else ''

                # 摘要
                summary_el = item.select_one('p.content a') or item.select_one('p.content')
                summary = summary_el.get_text(strip=True) if summary_el else ''

                # 时间和统计
                info_box = item.select_one('.info-box')
                publish_time = ''
                view_count = read_count = 0
                if info_box:
                    info_text = info_box.get_text(' ', strip=True)
                    # 提取时间: 2026-08-02 23:54:05
                    time_match = re.search(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})', info_text)
                    if time_match:
                        publish_time = time_match.group(1)
                    # 提取阅读量
                    read_match = re.search(r'(\d+)\s*阅读', info_text)
                    if read_match:
                        read_count = int(read_match.group(1))

                articles.append({
                    "article_id": article_id,
                    "title": title,
                    "url": link or f"https://blog.csdn.net/{self.username}/article/details/{article_id}",
                    "publish_time": publish_time,
                    "update_time": publish_time,
                    "view_count": read_count,
                    "like_count": 0,
                    "comment_count": 0,
                    "collect_count": 0,
                    "tags": [],
                    "column": "",
                    "summary": summary,
                })

            return articles
        except Exception as e:
            logger.error(f"HTML列表抓取失败 (page={page}): {e}")
            return []

    def _fetch_list_api(self, page: int, page_size: int) -> Tuple[List[Dict], int]:
        """API方式获取（备用）"""
        params = {
            "page": page, "size": page_size,
            "businessType": "blog", "orderBy": "date",
            "noMore": "false", "username": self.username,
        }
        try:
            resp = self._request(CONFIG["CSDN_ARTICLE_API"], params=params)
            data = resp.json()
            if data.get("code") != 200:
                logger.error(f"API错误: {data.get('message', 'unknown')}")
                return [], 0
            articles = []
            for item in data.get("data", {}).get("list", []):
                articles.append({
                    "article_id": str(item.get("articleId", "")),
                    "title": item.get("title", "").strip(),
                    "url": item.get("url", f"https://blog.csdn.net/{self.username}/article/details/{item.get('articleId')}"),
                    "publish_time": item.get("postTime") or item.get("createTime", ""),
                    "update_time": item.get("updateTime", ""),
                    "view_count": int(item.get("viewCount", "0").replace(",", "") or 0),
                    "like_count": int(item.get("diggCount", "0").replace(",", "") or 0),
                    "comment_count": int(item.get("commentCount", "0").replace(",", "") or 0),
                    "collect_count": int(item.get("collectCount", "0").replace(",", "") or 0),
                    "tags": [],
                    "column": item.get("nickName", ""),
                    "summary": item.get("description", ""),
                })
            total = int(data.get("data", {}).get("total", 0))
            return articles, total
        except Exception as e:
            logger.error(f"API列表获取失败 (page={page}): {e}")
            return [], 0

    def get_article_content(self, article_url: str) -> Tuple[str, str, str, List[str], str]:
        """
        获取文章正文
        返回: (content_html, content_text, dna_code, tags, column)
        """
        try:
            resp = self._request(article_url)
            soup = BeautifulSoup(resp.text, 'lxml')

            # 正文提取 (多选择器兜底)
            content_div = (
                soup.find(id="content_views") or
                soup.find(id="article_content") or
                soup.find(class_="article_content") or
                soup.find("article")
            )
            content_html = ""
            content_text = ""
            if content_div:
                for tag in content_div.find_all(["script", "style", "iframe", "ins", "svg"]):
                    tag.decompose()
                # 去除CSDN版权声明等噪音
                for noise in content_div.find_all(class_=re.compile(r"(hide-article-box|recommend|copyright|csdn-side)")):
                    noise.decompose()
                content_html = str(content_div)
                content_text = content_div.get_text(separator="\n", strip=True)

            # DNA追溯码
            dna_code = self._extract_dna(soup)

            # 标签
            tags = []
            tag_els = soup.select(".tag-link, .article-tag-list a, .tags a")
            for t in tag_els:
                tag_text = t.get_text(strip=True)
                if tag_text and tag_text not in tags:
                    tags.append(tag_text)
            if not tags:
                # 从分类/关键词meta提取
                for meta in soup.find_all("meta", attrs={"name": re.compile(r"keywords|category")}):
                    content = meta.get("content", "")
                    if content:
                        tags = [t.strip() for t in content.split(",") if t.strip()]
                        break

            # 专栏名
            column = ""
            col_el = soup.select_one(".column-title, .column_name, .article-column")
            if col_el:
                column = col_el.get_text(strip=True)

            return content_html, content_text, dna_code, tags, column

        except Exception as e:
            logger.error(f"获取文章内容失败 {article_url}: {e}")
            return "", "", "", [], ""

    def _extract_dna(self, soup: BeautifulSoup) -> str:
        """提取DNA追溯码"""
        text = soup.get_text()
        patterns = [
            r'#龍芯⚡️[^\s\n]{10,}',
            r'#CONFIRM🌌[^\s]+\s*🧬[^\s]+',
            r'DNA:\s*(#龍芯⚡️[^\n]+)',
        ]
        for pat in patterns:
            m = re.search(pat, text)
            if m:
                return m.group(0)
        return ""

    def get_all_articles(self, max_pages: int = None, max_articles: int = 0) -> List[CSDNArticle]:
        """全量获取所有文章"""
        max_pages = max_pages or CONFIG["MAX_PAGES"]
        all_articles = []
        page = 1
        total_pages = 1

        while page <= max_pages and page <= total_pages:
            logger.info(f"📄 抓取第 {page} 页...")
            items, total = self.get_article_list(page, CONFIG["PAGE_SIZE"])

            if not items:
                break

            if page == 1 and total > 0:
                total_pages = min((total + CONFIG["PAGE_SIZE"] - 1) // CONFIG["PAGE_SIZE"], max_pages)

            for item in items:
                if max_articles > 0 and len(all_articles) >= max_articles:
                    break

                aid = item["article_id"]
                logger.info(f"  📝 [{aid}] {item['title'][:40]}...")

                content_html, content_text, dna_code, tags, column = self.get_article_content(item["url"])

                article = CSDNArticle(
                    article_id=aid,
                    title=item["title"],
                    url=item["url"],
                    content_html=content_html,
                    content_text=content_text,
                    summary=item.get("summary", "") or (content_text[:200] if content_text else ""),
                    tags=tags or item.get("tags", []),
                    column=item.get("column", "") or column,
                    publish_time=item["publish_time"],
                    update_time=item.get("update_time", item["publish_time"]),
                    view_count=item["view_count"],
                    like_count=item["like_count"],
                    comment_count=item["comment_count"],
                    collect_count=item["collect_count"],
                    dna_code=dna_code,
                )
                all_articles.append(article)
                time.sleep(CONFIG["REQUEST_DELAY"])

            if max_articles > 0 and len(all_articles) >= max_articles:
                break

            page += 1
            time.sleep(CONFIG["REQUEST_DELAY"] * 0.5)

        logger.info(f"✅ 共获取 {len(all_articles)} 篇文章")
        return all_articles

# ============================================================
# Notion 同步器
# ============================================================

class NotionSyncer:
    """Notion数据库同步器"""

    def __init__(self):
        self.token = CONFIG["NOTION_TOKEN"]
        self.database_id = CONFIG["NOTION_DATABASE_ID"]
        if not self.token or "secret_" not in self.token:
            self.client = None
            self.available = False
        else:
            try:
                self.client = NotionClient(auth=self.token)
                self.available = True
            except Exception as e:
                logger.warning(f"Notion客户端初始化失败: {e}")
                self.client = None
                self.available = False

    def is_available(self) -> bool:
        return self.available and self.client is not None

    def create_or_update_page(self, article: CSDNArticle) -> bool:
        """创建或更新Notion页面"""
        if not self.is_available():
            return False
        try:
            # 先检查是否存在
            existing = self.client.databases.query(
                database_id=self.database_id,
                filter={"property": "文章ID", "rich_text": {"equals": article.article_id}},
                page_size=1
            )
            results = existing.get("results", [])

            props = self._build_properties(article)
            blocks = self._build_blocks(article)

            if results:
                page_id = results[0]["id"]
                self.client.pages.update(page_id=page_id, properties=props)
                # 追加更新块
                if blocks:
                    self.client.blocks.children.append(block_id=page_id, children=[{
                        "object": "block", "type": "divider", "divider": {}
                    }] + blocks[:50])
                logger.info(f"  📝 Notion更新: {article.title[:30]}")
            else:
                self.client.pages.create(
                    parent={"database_id": self.database_id},
                    properties=props,
                    children=blocks[:100] if blocks else []
                )
                logger.info(f"  ✅ Notion新建: {article.title[:30]}")
            return True
        except Exception as e:
            logger.error(f"  ❌ Notion同步失败 [{article.article_id}]: {e}")
            return False

    def _build_properties(self, article: CSDNArticle) -> Dict:
        props = {
            "标题": {"title": [{"text": {"content": article.title[:100]}}]},
            "文章ID": {"rich_text": [{"text": {"content": article.article_id}}]},
            "URL": {"url": article.url},
            "摘要": {"rich_text": [{"text": {"content": article.summary[:500]}}]},
        }

        # 标签 (Multi-select, 最多10个)
        if article.tags:
            props["标签"] = {"multi_select": [{"name": t[:20]} for t in article.tags[:10]]}

        # 专栏
        if article.column:
            props["专栏"] = {"select": {"name": article.column[:20]}}

        # 时间
        if article.publish_time:
            props["发布时间"] = {"date": {"start": self._fmt_time(article.publish_time)}}

        # DNA
        if article.dna_code:
            props["DNA追溯码"] = {"rich_text": [{"text": {"content": article.dna_code[:100]}}]}

        # 统计
        stats_text = f"👁{article.view_count} 👍{article.like_count} 💬{article.comment_count} ⭐{article.collect_count}"
        props["统计"] = {"rich_text": [{"text": {"content": stats_text[:100]}}]}

        props["状态"] = {"select": {"name": "已同步"}}
        return props

    def _build_blocks(self, article: CSDNArticle) -> List[Dict]:
        blocks = []

        # DNA追溯
        if article.dna_code:
            blocks.append({
                "object": "block", "type": "callout",
                "callout": {
                    "rich_text": [{"type": "text", "text": {"content": f"🧬 {article.dna_code}"}}],
                    "icon": {"emoji": "🧬"}, "color": "gray_background"
                }
            })

        # 正文分段
        text = article.content_text
        if text:
            for paragraph in text.split("\n\n"):
                paragraph = paragraph.strip()
                if not paragraph:
                    continue
                if len(paragraph) > 2000:
                    for chunk in [paragraph[i:i+2000] for i in range(0, len(paragraph), 2000)]:
                        blocks.append({
                            "object": "block", "type": "paragraph",
                            "paragraph": {"rich_text": [{"type": "text", "text": {"content": chunk}}]}
                        })
                else:
                    blocks.append({
                        "object": "block", "type": "paragraph",
                        "paragraph": {"rich_text": [{"type": "text", "text": {"content": paragraph}}]}
                    })
                if len(blocks) > 150:
                    break  # Notion限制

        # 原文链接
        blocks.append({
            "object": "block", "type": "divider", "divider": {}
        })
        blocks.append({
            "object": "block", "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": f"🔗 原文: {article.url}"}}],
                "icon": {"emoji": "🔗"}, "color": "blue_background"
            }
        })
        blocks.append({
            "object": "block", "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {
                    "content": f"📊 同步时间: {article.sync_time} | 龍魂·CSDN同步引擎"
                }}],
                "icon": {"emoji": "🐉"}, "color": "brown_background"
            }
        })
        return blocks

    @staticmethod
    def _fmt_time(t: str) -> str:
        """标准化时间格式"""
        if not t:
            return datetime.now(TZ).isoformat()
        try:
            return t.replace("Z", "+00:00") if "Z" in t else t
        except:
            return datetime.now(TZ).isoformat()

# ============================================================
# 本地归档器
# ============================================================

class LocalArchiver:
    """本地归档到鲲鹏知识库"""

    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or CONFIG["LOCAL_STORAGE_DIR"]

    def archive(self, article: CSDNArticle) -> Path:
        """归档单篇文章"""
        col = article.column or "未分类"
        col = re.sub(r'[<>:"/\\|?*]', '', col)
        col_dir = self.base_dir / col
        col_dir.mkdir(parents=True, exist_ok=True)

        # 按年月分类
        try:
            dt = datetime.fromisoformat(article.publish_time.replace("Z", "+00:00"))
            month_dir = col_dir / f"{dt.year:04d}-{dt.month:02d}"
        except:
            month_dir = col_dir / "unknown"
        month_dir.mkdir(exist_ok=True)

        # Markdown文件
        md_path = month_dir / f"{article.safe_filename}.md"
        md_content = self._build_markdown(article)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        # JSON元数据
        meta_path = month_dir / f"{article.safe_filename}.meta.json"
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(article.to_dict(), f, ensure_ascii=False, indent=2)

        logger.info(f"  📁 归档: {md_path}")
        return md_path

    def _build_markdown(self, article: CSDNArticle) -> str:
        now = datetime.now(TZ).isoformat()
        dna_stamp = get_output_stamp() if HAS_TIME_ENGINE else ""
        lines = [
            f"# {article.title}",
            "",
            f"**文章ID**: {article.article_id}",
            f"**CSDN链接**: {article.url}",
            f"**发布时间**: {article.publish_time}",
            f"**专栏**: {article.column or '未分类'}",
            f"**标签**: {', '.join(article.tags) if article.tags else '无'}",
        ]
        if article.dna_code:
            lines.append(f"**DNA**: {article.dna_code}")
        lines += [
            "",
            f"**统计**: 👁 {article.view_count} | 👍 {article.like_count} | 💬 {article.comment_count} | ⭐ {article.collect_count}",
            "",
            "---",
            "",
            "## 📝 正文",
            "",
            article.content_text,
            "",
            "---",
            "",
            f"> 🐉 龍魂·CSDN同步引擎 v1.0 | 归档时间: {now}",
        ]
        if dna_stamp:
            lines.append(f"> {dna_stamp}")
        return "\n".join(lines)

    def build_index(self) -> Dict:
        """构建全局索引"""
        index = {"total": 0, "by_column": {}, "by_tag": {}, "articles": [], "built_at": datetime.now(TZ).isoformat()}

        for col_dir in sorted(self.base_dir.iterdir()):
            if not col_dir.is_dir() or col_dir.name.startswith("_") or col_dir.name.startswith("."):
                continue
            col_count = 0
            for month_dir in sorted(col_dir.iterdir()):
                if not month_dir.is_dir():
                    continue
                for md_file in sorted(month_dir.glob("*.md")):
                    meta_file = md_file.with_suffix(".meta.json")
                    entry = {
                        "title": md_file.stem,
                        "file": str(md_file.relative_to(self.base_dir)),
                        "column": col_dir.name,
                        "month": month_dir.name,
                    }
                    if meta_file.exists():
                        try:
                            with open(meta_file, 'r', encoding='utf-8') as f:
                                meta = json.load(f)
                                entry["title"] = meta.get("title", md_file.stem)
                                entry["publish_time"] = meta.get("publish_time", "")
                                entry["url"] = meta.get("url", "")
                                entry["tags"] = meta.get("tags", [])
                                entry["dna_code"] = meta.get("dna_code", "")
                                for tag in meta.get("tags", []):
                                    index["by_tag"][tag] = index["by_tag"].get(tag, 0) + 1
                        except:
                            pass
                    index["articles"].append(entry)
                    index["total"] += 1
                    col_count += 1
            index["by_column"][col_dir.name] = col_count

        index_path = self.base_dir / "_index.json"
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
        logger.info(f"📊 索引: {index['total']}篇, {len(index['by_column'])}个专栏, {len(index['by_tag'])}个标签")
        return index

# ============================================================
# 三色审计标记
# ============================================================

def audit_mark(article: CSDNArticle) -> str:
    """三色审计判定"""
    checks = []
    # 必须有内容
    if article.content_text and len(article.content_text) > 50:
        checks.append(("内容完整性", "🟢"))
    elif article.content_text:
        checks.append(("内容完整性", "🟡"))
    else:
        checks.append(("内容完整性", "🔴"))
    # 必须有DNA
    if article.dna_code:
        checks.append(("DNA追溯", "🟢"))
    else:
        checks.append(("DNA追溯", "🟡"))
    # 必须有标签/分类
    if article.tags or article.column:
        checks.append(("分类标签", "🟢"))
    else:
        checks.append(("分类标签", "🟡"))
    # 发布时间合理
    if article.publish_time:
        checks.append(("时间信息", "🟢"))
    else:
        checks.append(("时间信息", "🟡"))

    reds = [c for c in checks if c[1] == "🔴"]
    yellows = [c for c in checks if c[1] == "🟡"]
    if reds:
        return f"🔴 {len(reds)}项红线: {', '.join(c[0] for c in reds)}"
    elif yellows:
        return f"🟡 {len(yellows)}项待核: {', '.join(c[0] for c in yellows)}"
    return "🟢 全通过"

# ============================================================
# 主同步引擎
# ============================================================

class CSDNSyncEngine:
    """主引擎"""

    def __init__(self):
        self.fetcher = CSDNFetcher()
        self.db = SyncDB()
        self.notion = NotionSyncer()
        self.archiver = LocalArchiver()

    def sync(self, mode: str = "full", max_articles: int = 0, notion_only: bool = False, local_only: bool = False) -> Dict:
        """
        执行同步
        mode: full | latest | incremental
        """
        logger.info(f"🚀 CSDN同步启动 · 模式={mode}")

        # 1. 抓取
        if mode == "latest":
            items, _ = self.fetcher.get_article_list(page=1, page_size=20)
            articles = []
            for item in items:
                if not self.db.is_known(item["article_id"]):
                    content_html, content_text, dna_code, tags, column = self.fetcher.get_article_content(item["url"])
                    articles.append(CSDNArticle(
                        article_id=item["article_id"], title=item["title"], url=item["url"],
                        content_html=content_html, content_text=content_text,
                        summary=item.get("summary", "") or content_text[:200],
                        tags=tags or item.get("tags", []), column=item.get("column", "") or column,
                        publish_time=item["publish_time"], update_time=item.get("update_time", ""),
                        view_count=item["view_count"], like_count=item["like_count"],
                        comment_count=item["comment_count"], collect_count=item["collect_count"],
                        dna_code=dna_code,
                    ))
                    time.sleep(CONFIG["REQUEST_DELAY"])
                elif self.db.needs_update(item["article_id"], ""):
                    content_html, content_text, dna_code, tags, column = self.fetcher.get_article_content(item["url"])
                    articles.append(CSDNArticle(
                        article_id=item["article_id"], title=item["title"], url=item["url"],
                        content_html=content_html, content_text=content_text,
                        summary=item.get("summary", "") or content_text[:200],
                        tags=tags or item.get("tags", []), column=item.get("column", "") or column,
                        publish_time=item["publish_time"], update_time=item.get("update_time", ""),
                        view_count=item["view_count"], like_count=item["like_count"],
                        comment_count=item["comment_count"], collect_count=item["collect_count"],
                        dna_code=dna_code,
                    ))
                    time.sleep(CONFIG["REQUEST_DELAY"])
        elif mode == "full":
            articles = self.fetcher.get_all_articles(max_articles=max_articles)
        else:
            # incremental: 只处理未同步的
            unsynced_ids = self.db.get_unsynced(limit=50)
            articles = []
            for aid in unsynced_ids:
                url = f"https://blog.csdn.net/{CONFIG['CSDN_USERNAME']}/article/details/{aid}"
                content_html, content_text, dna_code, tags, column = self.fetcher.get_article_content(url)
                articles.append(CSDNArticle(
                    article_id=aid, title=f"[补同步] {aid}", url=url,
                    content_html=content_html, content_text=content_text,
                    tags=tags, column=column, dna_code=dna_code,
                ))
                time.sleep(CONFIG["REQUEST_DELAY"])

        logger.info(f"📋 待处理: {len(articles)} 篇")

        # 2. 同步
        stats = {"total": len(articles), "new_synced": 0, "updated": 0, "skipped": 0,
                 "failed": 0, "notion_ok": 0, "local_ok": 0}

        for article in articles:
            try:
                if not self.db.is_known(article.article_id):
                    stats["new_synced"] += 1
                elif self.db.needs_update(article.article_id, article.content_hash()):
                    stats["updated"] += 1
                else:
                    stats["skipped"] += 1
                    continue

                audit = audit_mark(article)
                logger.info(f"  [{audit}] {article.title[:40]}")

                # Notion同步
                notion_ok = False
                if not local_only and self.notion.is_available():
                    notion_ok = self.notion.create_or_update_page(article)
                    if notion_ok:
                        stats["notion_ok"] += 1

                # 本地归档
                local_ok = False
                if not notion_only:
                    self.archiver.archive(article)
                    local_ok = True
                    stats["local_ok"] += 1

                self.db.upsert_article(article, notion_ok=notion_ok, local_ok=local_ok)

            except Exception as e:
                logger.error(f"  ❌ 失败 [{article.article_id}]: {e}")
                stats["failed"] += 1

        # 3. 索引
        self.archiver.build_index()

        # 4. 记录
        status = "success" if stats["failed"] == 0 else "partial"
        self.db.log_sync(mode=mode, status=status, **stats)

        logger.info(f"🎉 完成 | 新增{stats['new_synced']} 更新{stats['updated']} "
                    f"Notion{stats['notion_ok']} 本地{stats['local_ok']} 失败{stats['failed']}")
        return stats

# ============================================================
# 导出
# ============================================================

def export_articles(output_dir: Path, fmt: str = "json"):
    """导出已同步文章"""
    db = SyncDB()
    archive_dir = CONFIG["LOCAL_STORAGE_DIR"]
    output_dir.mkdir(parents=True, exist_ok=True)

    articles = []
    for col_dir in sorted(archive_dir.iterdir()):
        if not col_dir.is_dir() or col_dir.name.startswith("_") or col_dir.name.startswith("."):
            continue
        for month_dir in sorted(col_dir.iterdir()):
            if not month_dir.is_dir():
                continue
            for meta_file in sorted(month_dir.glob("*.meta.json")):
                try:
                    with open(meta_file, 'r', encoding='utf-8') as f:
                        meta = json.load(f)
                        articles.append(meta)
                except:
                    pass

    if fmt == "json":
        out_path = output_dir / f"csdn_export_{datetime.now(TZ).strftime('%Y%m%d_%H%M%S')}.json"
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        logger.info(f"✅ 导出 {len(articles)} 篇 → {out_path}")
    elif fmt == "jsonl":
        out_path = output_dir / f"csdn_export_{datetime.now(TZ).strftime('%Y%m%d_%H%M%S')}.jsonl"
        with open(out_path, 'w', encoding='utf-8') as f:
            for art in articles:
                f.write(json.dumps(art, ensure_ascii=False) + "\n")
        logger.info(f"✅ 导出 {len(articles)} 篇 → {out_path}")
    else:
        logger.error(f"不支持的格式: {fmt}")

# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·CSDN博客 → Notion + 鲲鹏知识库 自动同步引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_csdn_sync.py --sync                    # 全量同步
  python3 bin/lh_csdn_sync.py --sync --latest           # 仅最新
  python3 bin/lh_csdn_sync.py --sync --incremental      # 增量(补齐缺口)
  python3 bin/lh_csdn_sync.py --local-only              # 仅本地归档
  python3 bin/lh_csdn_sync.py --notion-only             # 仅Notion
  python3 bin/lh_csdn_sync.py --status                  # 状态
  python3 bin/lh_csdn_sync.py --build-index             # 重建索引
  python3 bin/lh_csdn_sync.py --export --format json    # 导出
        """
    )
    parser.add_argument("--sync", action="store_true", help="执行同步")
    parser.add_argument("--latest", action="store_true", help="仅最新文章")
    parser.add_argument("--incremental", action="store_true", help="增量同步(补齐缺口)")
    parser.add_argument("--max", type=int, default=0, help="最大同步篇数")
    parser.add_argument("--notion-only", action="store_true", help="仅同步到Notion")
    parser.add_argument("--local-only", action="store_true", help="仅归档到本地")
    parser.add_argument("--build-index", action="store_true", help="重建本地索引")
    parser.add_argument("--status", action="store_true", help="显示同步状态")
    parser.add_argument("--export", action="store_true", help="导出已同步文章")
    parser.add_argument("--format", choices=["json", "jsonl"], default="json", help="导出格式")
    parser.add_argument("--info", action="store_true", help="显示引擎信息")

    args = parser.parse_args()

    if args.info:
        db = SyncDB()
        stats = db.get_stats()
        print(f"""
🐉 龍魂·CSDN同步引擎 v1.0
━━━━━━━━━━━━━━━━━━━━━━━
DNA: #龍芯⚡️丙午·丙申·戊申·CSDN-SYNC-v1.0
配置:
  CSDN:     {CONFIG['CSDN_BLOG_URL']}
  Notion:   {'✅ 已配置' if CONFIG['NOTION_TOKEN'] and 'secret_' in CONFIG['NOTION_TOKEN'] else '🟡 未配置'}
  本地存储: {CONFIG['LOCAL_STORAGE_DIR']}
  数据库:   {stats['total']}篇 | Notion{stats['notion']} | 本地{stats['local']}
  上次同步: {stats['last_sync']}
  执行次数: {stats['sync_runs']}
        """)
        return

    if args.status:
        db = SyncDB()
        archiver = LocalArchiver()
        stats = db.get_stats()
        idx = archiver.build_index()
        print(f"""
📊 CSDN同步状态
━━━━━━━━━━━━━━━━━━━━━━━
数据库文章: {stats['total']}篇
Notion同步: {stats['notion']}篇
本地归档:   {stats['local']}篇
文件索引:   {idx['total']}篇
上次同步:   {stats['last_sync']}
执行次数:   {stats['sync_runs']}
━━━━━━━━━━━━━━━━━━━━━━━
分区:
  {chr(10).join(f'  {k}: {v}篇' for k, v in sorted(idx['by_column'].items()))}

热门标签:
  {chr(10).join(f'  {k}: {v}篇' for k, v in sorted(idx['by_tag'].items(), key=lambda x: -x[1])[:10])}
        """)
        return

    if args.build_index:
        archiver = LocalArchiver()
        idx = archiver.build_index()
        print(f"📊 索引已重建: {idx['total']}篇")
        return

    if args.export:
        export_articles(CONFIG["EXPORT_DIR"], args.format)
        return

    if args.sync:
        mode = "latest" if args.latest else ("incremental" if args.incremental else "full")
        engine = CSDNSyncEngine()
        stats = engine.sync(
            mode=mode,
            max_articles=args.max,
            notion_only=args.notion_only,
            local_only=args.local_only
        )
        print(f"\n📊 同步结果: 新增{stats['new_synced']} 更新{stats['updated']} "
              f"跳过{stats['skipped']} 失败{stats['failed']} "
              f"| Notion{stats['notion_ok']} 本地{stats['local_ok']}")
        if HAS_TIME_ENGINE:
            print(get_output_stamp())
        return

    if args.notion_only or args.local_only:
        # 单独的目标
        engine = CSDNSyncEngine()
        stats = engine.sync(
            mode="full",
            max_articles=args.max,
            notion_only=args.notion_only,
            local_only=args.local_only
        )
        return

    parser.print_help()

if __name__ == "__main__":
    main()
