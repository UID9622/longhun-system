#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · Notion 全量同步优化引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·壬午·☴巽-NOTION-FULL-SYNC-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

优化点：
  - 分页超时自动恢复 + 退避重试
  - 内容哈希去重（增量同步，只拉变化的）
  - 断点续传（中断后从上次位置继续）
  - 进度实时显示（百分比 + ETA）
  - 跳过已归档页面
  - 批量提交（每50页一次，减少IO）
  - 全文搜索（FTS5）

用法：
  python3 bin/lh_notion_full_sync.py sync              # 全量同步
  python3 bin/lh_notion_full_sync.py sync --max 500     # 快速同步500页
  python3 bin/lh_notion_full_sync.py sync --incremental # 增量同步（只拉变化的）
  python3 bin/lh_notion_full_sync.py search "关键词"    # 全文搜索
  python3 bin/lh_notion_full_sync.py status             # 查看同步状态

环境变量：
  NOTION_TOKEN_BACKUP 或 NOTION_TOKEN — Notion API 密钥
"""

import os
import sys
import time
import json
import hashlib
import sqlite3
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Callable, Set

# ─── 常量 ───────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
NOTION_BASE = "https://api.notion.com/v1"
NOTION_TOKEN = os.environ.get("NOTION_TOKEN_BACKUP") or os.environ.get("NOTION_TOKEN")
NOTION_VERSION = "2022-06-28"
SYNC_DB = PROJECT_ROOT / "data" / "notion_full_sync.db"
STATE_FILE = PROJECT_ROOT / "data" / "notion_full_sync_state.json"
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

PAGE_SIZE = 100  # Notion API 每页最多100
BATCH_DELAY = 0.34  # 请求间隔（避免429限流，每秒≈3请求）
COMMIT_INTERVAL = 50  # 每50页提交一次数据库
MAX_RETRIES = 3

DNA_PREFIX = "#龍芯⚡️"
SYNC_DNA = f"{DNA_PREFIX}丙午·丙申·乙巳·壬午·☴巽-NOTION-FULL-SYNC-v1.0-UID9622"

NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json",
}


# ─── 数据库 ───────────────────────────────────────

def init_db():
    """初始化 SQLite 数据库（含 FTS5 全文索引）"""
    conn = sqlite3.connect(str(SYNC_DB))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pages (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL DEFAULT '',
            content TEXT DEFAULT '',
            url TEXT DEFAULT '',
            object_type TEXT DEFAULT 'page',
            parent_type TEXT DEFAULT '',
            parent_id TEXT DEFAULT '',
            database_id TEXT DEFAULT '',
            last_edited TEXT DEFAULT '',
            created_time TEXT DEFAULT '',
            archived INTEGER DEFAULT 0,
            content_hash TEXT DEFAULT '',
            synced_at TEXT DEFAULT '',
            sync_dna TEXT DEFAULT ''
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_title ON pages(title)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_synced ON pages(synced_at)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_hash ON pages(content_hash)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_parent ON pages(parent_id)")

    # FTS5 全文索引
    conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS pages_fts USING fts5(
            title, content, content=pages, content_rowid=rowid
        )
    """)

    # 同步日志
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sync_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            started_at TEXT,
            finished_at TEXT,
            pages_total INTEGER DEFAULT 0,
            pages_added INTEGER DEFAULT 0,
            pages_updated INTEGER DEFAULT 0,
            pages_skipped INTEGER DEFAULT 0,
            pages_removed INTEGER DEFAULT 0,
            errors INTEGER DEFAULT 0,
            api_calls INTEGER DEFAULT 0,
            sync_type TEXT DEFAULT 'full',
            dna TEXT DEFAULT ''
        )
    """)

    # 断点续传状态
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sync_checkpoint (
            id INTEGER PRIMARY KEY CHECK (id=1),
            last_cursor TEXT DEFAULT '',
            last_page_index INTEGER DEFAULT 0,
            total_found INTEGER DEFAULT 0,
            updated_at TEXT DEFAULT ''
        )
    """)
    conn.execute("INSERT OR IGNORE INTO sync_checkpoint (id) VALUES (1)")

    conn.commit()
    conn.close()


def get_db() -> sqlite3.Connection:
    """获取数据库连接"""
    conn = sqlite3.connect(str(SYNC_DB))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    return conn


def rebuild_fts():
    """重建全文索引"""
    conn = get_db()
    conn.execute("INSERT INTO pages_fts(pages_fts) VALUES('rebuild')")
    conn.commit()
    conn.close()


# ─── Notion API 客户端 ──────────────────────────

class NotionSyncClient:
    """Notion API 同步客户端（stdlib urllib，零外部依赖）"""

    def __init__(self):
        if not NOTION_TOKEN:
            raise RuntimeError(
                "NOTION_TOKEN 未设置。请设置环境变量:\n"
                "  export NOTION_TOKEN_BACKUP='ntn_...'"
            )
        self.headers = NOTION_HEADERS
        self.calls = 0

    def _api_call(
        self, method: str, path: str, data: dict = None, timeout: int = 15
    ) -> Optional[dict]:
        """统一 API 调用（带重试和退避）"""
        for attempt in range(MAX_RETRIES):
            try:
                url = f"{NOTION_BASE}{path}"
                req_data = json.dumps(data).encode() if data else None
                req = urllib.request.Request(
                    url, data=req_data, headers=self.headers, method=method
                )
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    self.calls += 1
                    return json.loads(resp.read().decode())
            except urllib.error.HTTPError as e:
                body = e.read().decode()[:300]
                if e.code == 429:
                    wait = 2 ** attempt + 1
                    print(f"   ⏳ 限流，等待 {wait}s...")
                    time.sleep(wait)
                    continue
                if e.code >= 500:
                    time.sleep(2 ** attempt)
                    continue
                print(f"   ⚠️ HTTP {e.code}: {body[:100]}")
                return None
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(1)
                    continue
                print(f"   ⚠️ API 请求失败: {e}")
                return None
        return None

    def search_all(
        self,
        progress_callback: Callable = None,
        max_pages: int = 0,
        resume_cursor: str = "",
    ) -> tuple:
        """搜索所有页面和数据库（分页遍历）"""
        results = []
        cursor = resume_cursor if resume_cursor else None
        page_num = 0

        while True:
            page_num += 1
            payload = {"page_size": PAGE_SIZE}
            if cursor:
                payload["start_cursor"] = cursor

            resp = self._api_call("POST", "/search", payload)
            if not resp:
                print(f"   ⚠️ 第{page_num}页请求失败，已有 {len(results)} 项")
                break

            items = resp.get("results", [])
            results.extend(items)
            has_more = resp.get("has_more", False)
            cursor = resp.get("next_cursor")

            if progress_callback:
                progress_callback(len(results))

            if max_pages and len(results) >= max_pages:
                print(f"   🛑 已达上限 {max_pages} 项，停止搜索")
                break
            if not has_more or not cursor:
                break

            time.sleep(BATCH_DELAY)

        return results, cursor

    def query_database(self, database_id: str) -> List[dict]:
        """查询数据库所有条目"""
        results = []
        cursor = None

        while True:
            payload = {"page_size": PAGE_SIZE}
            if cursor:
                payload["start_cursor"] = cursor

            resp = self._api_call("POST", f"/databases/{database_id}/query", payload)
            if not resp:
                break

            items = resp.get("results", [])
            results.extend(items)

            if not resp.get("has_more"):
                break
            cursor = resp.get("next_cursor")
            time.sleep(BATCH_DELAY)

        return results

    def get_page_blocks(self, page_id: str) -> List[dict]:
        """获取页面所有块内容"""
        blocks = []
        cursor = None

        while True:
            path = f"/blocks/{page_id}/children?page_size=100"
            if cursor:
                path += f"&start_cursor={cursor}"

            resp = self._api_call("GET", path, timeout=10)
            if not resp:
                break

            items = resp.get("results", [])
            blocks.extend(items)

            if not resp.get("has_more"):
                break
            cursor = resp.get("next_cursor")
            time.sleep(BATCH_DELAY / 2)

        return blocks


# ─── 内容提取 ────────────────────────────────────

def extract_title(page: dict) -> str:
    """从 Notion 页面属性中提取标题"""
    props = page.get("properties", {})
    for prop in props.values():
        if isinstance(prop, dict) and prop.get("type") == "title":
            texts = prop.get("title", [])
            return "".join(t.get("plain_text", "") for t in texts)
    # 尝试从其他属性提取
    for prop in props.values():
        if isinstance(prop, dict):
            ptype = prop.get("type", "")
            if ptype == "rich_text":
                texts = prop.get("rich_text", [])
                return "".join(t.get("plain_text", "") for t in texts)
    return "(无标题)"


def blocks_to_text(blocks: List[dict]) -> str:
    """将 Notion 块列表提取为纯文本"""
    texts = []
    for block in blocks:
        btype = block.get("type", "")
        block_data = block.get(btype, {})

        if btype in ("paragraph", "heading_1", "heading_2", "heading_3",
                     "bulleted_list_item", "numbered_list_item", "to_do", "toggle",
                     "quote", "callout"):
            rich_text = block_data.get("rich_text", [])
            line = "".join(t.get("plain_text", "") for t in rich_text)
            if line.strip():
                prefix = {"heading_1": "# ", "heading_2": "## ", "heading_3": "### ",
                          "quote": "> ", "to_do": "[ ] "}.get(btype, "")
                texts.append(prefix + line)

        elif btype == "code":
            rich_text = block_data.get("rich_text", [])
            language = block_data.get("language", "")
            code = "".join(t.get("plain_text", "") for t in rich_text)
            texts.append(f"```{language}\n{code}\n```")

        elif btype == "image":
            alt = "".join(t.get("plain_text", "") for t in
                         block_data.get("caption", []))
            file_url = (block_data.get("file", {}).get("url", "") or
                       block_data.get("external", {}).get("url", ""))
            texts.append(f"[图片: {alt or file_url[:50]}]")

        elif block.get("has_children"):
            texts.append(f"[嵌套内容: {btype}]")

    return "\n".join(texts)


# ─── 同步引擎 ────────────────────────────────────

def sync_pages(
    max_items: int = 0,
    incremental: bool = False,
    resume: bool = False,
    progress_callback: Callable = None,
) -> Dict:
    """核心同步函数"""
    if not NOTION_TOKEN:
        return {"status": "error", "message": "NOTION_TOKEN 未设置"}

    init_db()
    client = NotionSyncClient()
    started = datetime.now(timezone.utc).isoformat()

    print(f"\n{'='*56}")
    print(f"  🐉 龍魂 · Notion 全量同步引擎 v1.0")
    mode = "增量" if incremental else ("断点续传" if resume else "全量")
    if max_items:
        print(f"  ⚡ 快速模式: 最多 {max_items} 项")
    print(f"  📡 模式: {mode}")
    print(f"  {SYNC_DNA}")
    print(f"{'='*56}\n")

    # ── Step 1: 搜索 ──
    print("📡 搜索所有 Notion 内容...")
    resume_cursor = ""
    if resume:
        conn = get_db()
        cp = conn.execute("SELECT last_cursor FROM sync_checkpoint").fetchone()
        resume_cursor = cp["last_cursor"] if cp else ""
        conn.close()
        if resume_cursor:
            print(f"   🔄 从断点续传: cursor={resume_cursor[:30]}...")

    all_items, last_cursor = client.search_all(
        progress_callback=lambda n: print(f"\r   📄 已搜索 {n} 项...", end="", flush=True)
        if n % 100 == 0 else None,
        max_pages=max_items,
        resume_cursor=resume_cursor,
    )
    print(f"\r   ✅ 搜索完成: {len(all_items)} 项  ")

    # 分类
    dbs = [x for x in all_items if x.get("object") == "database"]
    pages = [x for x in all_items if x.get("object") == "page"]
    active_pages = [p for p in pages if not p.get("archived")]
    archived_count = len(pages) - len(active_pages)
    if archived_count:
        print(f"   ⏭️  跳过 {archived_count} 个已归档页面")

    print(f"   📊 {len(dbs)} 数据库 + {len(active_pages)} 活跃页面")
    print(f"   🔌 API 调用: {client.calls} 次\n")

    # ── Step 2: 构建页面队列 ──
    page_queue = []

    # 独立页面
    for p in active_pages:
        pid = p.get("id", "").replace("-", "")
        if pid:
            parent = p.get("parent", {})
            page_queue.append({
                "id": pid,
                "title": extract_title(p),
                "url": p.get("url", ""),
                "object_type": "page",
                "parent_type": parent.get("type", ""),
                "parent_id": parent.get("database_id", "").replace("-", ""),
                "last_edited": p.get("last_edited_time", ""),
                "created_time": p.get("created_time", ""),
                "archived": 0,
            })

    # 数据库条目（限制前10个数据库，避免API爆炸）
    max_dbs = min(len(dbs), 10)
    for i, db in enumerate(dbs[:max_dbs]):
        db_id = db.get("id", "").replace("-", "")
        db_title = extract_title(db)
        if not db_id:
            continue
        print(f"   📊 [{i+1}/{min(len(dbs), max_dbs)}] 数据库: {db_title[:45]} ...")
        entries = client.query_database(db_id)
        active_entries = [e for e in entries if not e.get("archived")]
        print(f"      → {len(entries)} 条 ({len(active_entries)} 活跃)")

        for e in active_entries:
            if max_items and len(page_queue) >= max_items:
                break
            eid = e.get("id", "").replace("-", "")
            if eid:
                page_queue.append({
                    "id": eid,
                    "title": extract_title(e),
                    "url": e.get("url", ""),
                    "object_type": "database_entry",
                    "parent_type": "database_id",
                    "parent_id": db_id,
                    "database_id": db_id,
                    "last_edited": e.get("last_edited_time", ""),
                    "created_time": e.get("created_time", ""),
                    "archived": 0,
                })

        if max_items and len(page_queue) >= max_items:
            break
        time.sleep(BATCH_DELAY)

    if len(dbs) > max_dbs:
        print(f"   ⚠️  数据库过多({len(dbs)}个)，仅同步前{max_dbs}个（后续同步补齐）")

    # ── Step 3: 逐页拉取内容 ──
    total = len(page_queue)
    if total == 0:
        print("\n   📭 无内容需要同步")
        save_state({"status": "empty"})
        return {"status": "empty", "total_pages": 0, "api_calls": client.calls}

    print(f"\n📝 共 {total} 个页面，开始拉取...\n")

    stats = {"added": 0, "updated": 0, "skipped": 0, "errors": 0}
    all_page_ids = set()

    conn = get_db()
    existing = {
        row["id"]: (row["content_hash"], row["last_edited"])
        for row in conn.execute("SELECT id, content_hash, last_edited FROM pages").fetchall()
    }

    batch_start = time.time()

    for idx, page_info in enumerate(page_queue):
        pid = page_info["id"]
        if not pid:
            continue

        # 进度显示
        if idx > 0 and idx % 10 == 0:
            elapsed = time.time() - batch_start
            rate = idx / elapsed if elapsed > 0 else 0
            eta = (total - idx) / rate if rate > 0 else 0
            print(f"   [{idx}/{total}] "
                  f"🆕{stats['added']} 📝{stats['updated']} "
                  f"⏭️{stats['skipped']} ❌{stats['errors']} | "
                  f"{rate:.1f}页/s | ETA {eta:.0f}s | API:{client.calls}")

        # 增量模式跳过未变化的
        if incremental and pid in existing:
            old_hash, old_edited = existing[pid]
            if old_edited == page_info["last_edited"] and old_hash:
                stats["skipped"] += 1
                all_page_ids.add(pid)
                continue

        # 拉取块内容
        try:
            blocks = client.get_page_blocks(pid)
            content = blocks_to_text(blocks)
            content_hash = hashlib.md5(content.encode()).hexdigest()

            if pid in existing:
                conn.execute("""
                    UPDATE pages SET title=?, content=?, last_edited=?,
                    content_hash=?, synced_at=?, sync_dna=?
                    WHERE id=?
                """, (
                    page_info["title"], content, page_info["last_edited"],
                    content_hash, datetime.now(timezone.utc).isoformat(),
                    SYNC_DNA, pid,
                ))
                stats["updated"] += 1
            else:
                conn.execute("""
                    INSERT INTO pages (id, title, content, url, object_type,
                    parent_type, parent_id, database_id, last_edited,
                    created_time, archived, content_hash, synced_at, sync_dna)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (
                    pid, page_info["title"], content, page_info["url"],
                    page_info["object_type"], page_info["parent_type"],
                    page_info["parent_id"], page_info.get("database_id", ""),
                    page_info["last_edited"], page_info["created_time"],
                    page_info["archived"], content_hash,
                    datetime.now(timezone.utc).isoformat(), SYNC_DNA,
                ))
                stats["added"] += 1

            all_page_ids.add(pid)

        except Exception as e:
            stats["errors"] += 1
            if stats["errors"] <= 3:
                print(f"   ⚠️ 拉取失败 [{page_info['title'][:30]}]: {e}")

        # 定期提交 + 保存断点
        if idx > 0 and idx % COMMIT_INTERVAL == 0:
            conn.commit()
            conn.execute("""
                UPDATE sync_checkpoint SET last_cursor=?, last_page_index=?,
                total_found=?, updated_at=?
                WHERE id=1
            """, (last_cursor or "", idx, total, datetime.now(timezone.utc).isoformat()))
            conn.commit()

        time.sleep(BATCH_DELAY / 2)

    # 最终提交
    conn.commit()

    # 清理已删除页面（仅全量同步）
    if not incremental and not max_items:
        removed = set(existing.keys()) - all_page_ids
        if removed:
            placeholders = ",".join("?" * len(removed))
            conn.execute(f"DELETE FROM pages WHERE id IN ({placeholders})", list(removed))
            stats["removed"] = len(removed)

    # 同步日志
    conn.execute("""
        INSERT INTO sync_log (started_at, finished_at, pages_total,
        pages_added, pages_updated, pages_skipped, pages_removed,
        errors, api_calls, sync_type, dna)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """, (
        started, datetime.now(timezone.utc).isoformat(),
        total, stats["added"], stats["updated"], stats["skipped"],
        stats.get("removed", 0), stats["errors"],
        client.calls, "incremental" if incremental else "full", SYNC_DNA,
    ))

    # 清除断点
    conn.execute("UPDATE sync_checkpoint SET last_cursor='', last_page_index=0, updated_at='' WHERE id=1")
    conn.commit()
    conn.close()

    # ── 收尾 ──
    rebuild_fts()
    elapsed = time.time() - batch_start

    print(f"\n{'='*56}")
    print(f"  ✅ 同步完成")
    print(f"  🆕 新增: {stats['added']}  |  📝 更新: {stats['updated']}")
    print(f"  ⏭️  跳过: {stats['skipped']}  |  🗑️  移除: {stats.get('removed', 0)}")
    print(f"  ❌ 错误: {stats['errors']}")
    print(f"  🔌 API: {client.calls} 次  |  ⏱️  耗时: {elapsed:.1f}s")
    print(f"  🧬 {SYNC_DNA}")
    print(f"{'='*56}\n")

    state = {
        "last_sync": datetime.now(timezone.utc).isoformat(),
        "total_pages": total,
        "stats": stats,
        "api_calls": client.calls,
        "elapsed": elapsed,
        "dna": SYNC_DNA,
    }
    save_state(state)
    return state


def save_state(state: dict):
    """保存同步状态"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def load_state() -> dict:
    """加载同步状态"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


# ─── 搜索 ────────────────────────────────────────

def search_pages(query: str, limit: int = 10) -> List[dict]:
    """全文搜索（FTS5）"""
    init_db()
    conn = get_db()

    # 移除 FTS5 特殊字符
    safe_query = query.replace('"', '').replace("'", "")
    # 中文分词优化：在每个字符间插入空格
    if any('\u4e00' <= c <= '\u9fff' for c in safe_query):
        safe_query = " ".join(safe_query)

    try:
        rows = conn.execute("""
            SELECT p.*, rank
            FROM pages_fts f
            JOIN pages p ON f.rowid = p.rowid
            WHERE pages_fts MATCH ?
            ORDER BY rank
            LIMIT ?
        """, (safe_query, limit)).fetchall()
    except Exception:
        # 回退到 LIKE 搜索
        like_q = f"%{query}%"
        rows = conn.execute("""
            SELECT *, 1 as rank FROM pages
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY last_edited DESC
            LIMIT ?
        """, (like_q, like_q, limit)).fetchall()

    conn.close()

    results = []
    for row in rows:
        results.append({
            "id": row["id"],
            "title": row["title"],
            "content": row["content"][:300],
            "url": row["url"],
            "last_edited": row["last_edited"],
            "object_type": row["object_type"],
        })
    return results


def get_status() -> dict:
    """获取同步状态"""
    state = load_state()
    init_db()

    conn = get_db()
    page_count = conn.execute("SELECT COUNT(*) as c FROM pages").fetchone()["c"]
    content_size = conn.execute(
        "SELECT SUM(LENGTH(content)) as s FROM pages"
    ).fetchone()["s"] or 0
    last_sync = conn.execute(
        "SELECT * FROM sync_log ORDER BY started_at DESC LIMIT 1"
    ).fetchone()
    conn.close()

    return {
        "total_pages": page_count,
        "content_bytes": content_size,
        "last_sync": state.get("last_sync"),
        "last_sync_log": dict(last_sync) if last_sync else None,
        "db_path": str(SYNC_DB),
        "db_size_mb": SYNC_DB.stat().st_size / 1024 / 1024 if SYNC_DB.exists() else 0,
    }


# ─── CLI ──────────────────────────────────────────

def print_banner():
    print(f"""
{'='*56}
  🐉 龍魂 · Notion 全量同步引擎 v1.0
  {SYNC_DNA}
{'='*56}
""")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="🐉 龍魂 · Notion 全量同步引擎")
    sub = parser.add_subparsers(dest="command", help="子命令")

    # sync
    p_sync = sub.add_parser("sync", help="全量/增量同步")
    p_sync.add_argument("--max", type=int, default=0, help="最大同步项数（0=不限制）")
    p_sync.add_argument("--incremental", action="store_true", help="增量同步（只拉变化的）")
    p_sync.add_argument("--resume", action="store_true", help="断点续传")

    # search
    p_search = sub.add_parser("search", help="全文搜索")
    p_search.add_argument("query", help="搜索关键词")
    p_search.add_argument("--limit", type=int, default=10, help="返回条数")
    p_search.add_argument("--full", action="store_true", help="显示完整内容")

    # status
    sub.add_parser("status", help="查看同步状态")

    # reset
    sub.add_parser("reset", help="清空数据库重新同步")

    args = parser.parse_args()

    if not NOTION_TOKEN and args.command != "status":
        print("❌ NOTION_TOKEN 未设置")
        print("   export NOTION_TOKEN_BACKUP='ntn_...'")
        sys.exit(1)

    if args.command == "sync":
        result = sync_pages(
            max_items=args.max,
            incremental=args.incremental,
            resume=args.resume,
        )
    elif args.command == "search":
        print_banner()
        print(f"  🔍 搜索: {args.query}\n")
        results = search_pages(args.query, limit=args.limit)
        if results:
            for i, r in enumerate(results, 1):
                marker = f"[{i}]"
                print(f"  {marker} {r['title']}")
                print(f"     URL: {r['url']}")
                print(f"     更新时间: {r['last_edited'][:19] if r['last_edited'] else 'N/A'}")
                if args.full:
                    print(f"     {r['content']}")
                    print()
                else:
                    print(f"     {r['content'][:200]}...")
                    print()
            print(f"  共 {len(results)} 条结果")
        else:
            print("  📭 未找到匹配结果")
    elif args.command == "status":
        print_banner()
        s = get_status()
        print(f"""
  📊 同步状态
  {'─'*40}
  已同步页面:   {s['total_pages']}
  内容总量:     {s['content_bytes']/1024:.1f} KB
  数据库大小:   {s['db_size_mb']:.1f} MB
  上次同步:     {s['last_sync'][:19] if s['last_sync'] else '从未'}
  数据库路径:   {s['db_path']}
  {'─'*40}
""")
        if s["last_sync_log"]:
            log = s["last_sync_log"]
            print(f"  最近同步日志:")
            print(f"    开始: {log.get('started_at', '')[:19]}")
            print(f"    完成: {log.get('finished_at', '')[:19]}")
            print(f"    新增: {log.get('pages_added', 0)}  更新: {log.get('pages_updated', 0)}")
            print(f"    跳过: {log.get('pages_skipped', 0)}  错误: {log.get('errors', 0)}")
            print(f"    API: {log.get('api_calls', 0)} 次\n")
    elif args.command == "reset":
        print_banner()
        print("  🗑️  清空数据库...")
        if SYNC_DB.exists():
            SYNC_DB.unlink()
        if STATE_FILE.exists():
            STATE_FILE.unlink()
        init_db()
        print("  ✅ 已重置，可重新全量同步\n")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
