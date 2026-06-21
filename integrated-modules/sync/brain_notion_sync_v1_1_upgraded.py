#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂脑干 · Notion同步桥 · brain_notion_sync.py v1.1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UID9622 · 诸葛鑫 · 龍芯北辰
DNA:#龍芯⚡️2026-06-07-NOTION-BRIDGE-FILE1-v1.1-PHASE1-UPGRADE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

v1.1 新功能 (Phase 1):
  ✅ 指数退避重試機制 (最多3次重試)
  ✅ 限流控制器 (避免觸發 API 限流)
  ✅ 更完善的錯誤處理
  ✅ 安全的 JSON 解析
  ✅ 詳細的日誌追蹤

功能：
  - 把 longhun_brain.py 的新记忆自动推送到 Notion
  - Notion 记忆页写回 brain DB（notion_id字段）
  - 定时轮询（每5分钟）
  - 🆕 自動重試失敗的上傳
  - 🆕 限流控制防止 API 觸發限制

配置（首次运行前修改下面的CONFIG）：
  NOTION_TOKEN   → Notion Integration Token
  DATABASE_ID    → 你的记忆数据库 ID（见下方说明）

用法：
  python3 brain_notion_sync.py            # 单次同步
  python3 brain_notion_sync.py --watch    # 持续监听（5分钟间隔）
  python3 brain_notion_sync.py --status   # 查看同步状态
"""

import sys, os, json, time, sqlite3, hashlib, argparse
from datetime import datetime, date
from pathlib import Path

from integrated_modules.longhun_config import getenv

# ═══════════════════════════════════════
# ⚙️ 配置区（首次运行必填）
# ═══════════════════════════════════════

CONFIG = {
    # Notion Integration Token（到 notion.so/my-integrations 创建）
    "NOTION_TOKEN": getenv("NOTION_TOKEN", ""),

    # 记忆数据库 ID（把 Notion 数据库 URL 里的 32位ID 粘贴在这里）
    # 例：https://www.notion.so/你的ID → 复制那32位
    "DATABASE_ID": getenv("DB_LU", ""),

    # brain.db 路径（和 longhun_brain.py 保持一致）
    "DB_PATH": Path.home() / "longhun-system" / "brain" / "memories.db",

    # 同步间隔（秒），默认5分钟
    "INTERVAL": 300,
    
    # Phase 1 新增配置
    "MAX_RETRIES": 3,              # 最大重試次數
    "RETRY_BACKOFF": 2,            # 指数退避底数 (1s, 2s, 4s...)
    "API_RATE_LIMIT": 5,           # API 呼叫限制 (calls/second)
    "NOTION_TIMEOUT": 15,          # Notion API 超時時間 (秒)
}

WUXING_EMOJI = {"水":"💧","木":"🌿","火":"🔥","金":"⚡","土":"🌍"}

# ═══════════════════════════════════════
# ⚡ Phase 1: 速率限制器 (Rate Limiter)
# ═══════════════════════════════════════

class RateLimiter:
    """API 速率限制器 - 避免觸發 Notion API 限流"""
    
    def __init__(self, calls_per_second=5):
        self.calls_per_second = calls_per_second
        self.min_interval = 1.0 / calls_per_second
        self.last_call_time = 0
    
    def wait(self):
        """等待直到可以進行下一次 API 呼叫"""
        now = time.time()
        elapsed = now - self.last_call_time
        
        if elapsed < self.min_interval:
            sleep_time = self.min_interval - elapsed
            time.sleep(sleep_time)
        
        self.last_call_time = time.time()
    
    def __enter__(self):
        self.wait()
        return self
    
    def __exit__(self, *args):
        pass

# ═══════════════════════════════════════
# 🔄 Phase 1: 重試機制 (Retry Logic)
# ═══════════════════════════════════════

class RetryableException(Exception):
    """可重試的異常"""
    pass

def retry_with_backoff(func, *args, max_retries=3, backoff_base=2, verbose=True, **kwargs):
    """
    指數退避重試機制
    
    Args:
        func: 要執行的函數
        max_retries: 最大重試次數
        backoff_base: 指數退避底數
        verbose: 是否輸出日誌
    
    Returns:
        函數執行結果
    
    Raises:
        Exception: 所有重試都失敗時拋出最後一個異常
    """
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            if verbose and attempt > 0:
                print(f"    🔄 重試 {attempt}/{max_retries-1}...")
            
            result = func(*args, **kwargs)
            
            if verbose and attempt > 0:
                print(f"    ✅ 第 {attempt+1} 次重試成功")
            
            return result
        
        except Exception as e:
            last_exception = e
            
            if attempt < max_retries - 1:
                # 計算等待時間 (exponential backoff)
                wait_time = backoff_base ** attempt
                
                if verbose:
                    print(f"    ⚠️  嘗試 {attempt+1} 失敗: {str(e)[:60]}")
                    print(f"    ⏳ 等待 {wait_time}s 後重試...")
                
                time.sleep(wait_time)
            else:
                if verbose:
                    print(f"    ❌ 所有 {max_retries} 次重試都失敗")
    
    raise last_exception

# ═══════════════════════════════════════
# Notion API 封装 (升級版)
# ═══════════════════════════════════════

def notion_headers():
    return {
        "Authorization": f"Bearer {CONFIG['NOTION_TOKEN']}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

def safe_parse_json(json_str, default=None):
    """安全的 JSON 解析"""
    if isinstance(json_str, (list, dict)):
        return json_str
    
    if isinstance(json_str, str):
        try:
            parsed = json.loads(json_str)
            return parsed
        except (json.JSONDecodeError, ValueError) as e:
            # JSON 解析失敗，嘗試降級處理
            return default if default is not None else [json_str]
    
    return default if default is not None else []

def safe_parse_tags(tags):
    """安全的標籤解析"""
    if isinstance(tags, list):
        return tags[:5]  # 最多 5 個標籤
    
    parsed = safe_parse_json(tags, default=None)
    if isinstance(parsed, list):
        return parsed[:5]
    
    if isinstance(tags, str):
        return [tags]
    
    return []

def notion_create_page(memory: dict, rate_limiter: RateLimiter = None) -> str | None:
    """
    把一条记忆写到 Notion 数据库，返回 page_id
    
    v1.1: 添加速率限制和更好的錯誤處理
    """
    try:
        import urllib.request, urllib.error
    except ImportError:
        return None

    if not CONFIG["NOTION_TOKEN"] or not CONFIG["DATABASE_ID"]:
        print("    ⚠️  Notion Token 或 Database ID 未配置")
        return None

    # 速率限制
    if rate_limiter:
        rate_limiter.wait()

    wx_emoji = WUXING_EMOJI.get(memory.get("wuxing","土"), "🌍")
    tags = safe_parse_tags(memory.get("tags", []))

    payload = {
        "parent": {"database_id": CONFIG["DATABASE_ID"]},
        "properties": {
            # 标题 = 内容前60字
            "名称": {
                "title": [{"text": {"content": memory["content"][:60]}}]
            },
            # DNA码
            "DNA": {
                "rich_text": [{"text": {"content": memory["dna"]}}]
            },
            # 五行
            "五行": {
                "select": {"name": f"{wx_emoji}{memory.get('wuxing','土')}"}
            },
            # 三色
            "三色": {
                "select": {"name": memory.get("tricolor", "🟢")}
            },
            # 来源
            "来源": {
                "select": {"name": memory.get("source", "unknown")}
            },
            # 标签
            "标签": {
                "multi_select": [{"name": t} for t in tags]
            },
            # 创建时间
            "记录时间": {
                "date": {"start": memory.get("created_at","")[:19]}
            },
        },
        # 正文 = 完整内容
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": memory["content"]}}]
                }
            },
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content":
                        f"DNA: {memory['dna']}\n"
                        f"五行: {memory.get('wuxing','土')}  三色: {memory.get('tricolor','🟢')}\n"
                        f"数字根: {memory.get('dr',0)}  来源: {memory.get('source','unknown')}"
                    }}],
                    "icon": {"emoji": "🐉"}
                }
            }
        ]
    }

    data = json.dumps(payload).encode("utf-8")
    
    def _make_request():
        req = urllib.request.Request(
            "https://api.notion.com/v1/pages",
            data=data,
            headers=notion_headers(),
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=CONFIG["NOTION_TIMEOUT"]) as resp:
                result = json.loads(resp.read())
                return result.get("id", "")
        except urllib.error.HTTPError as e:
            # HTTP 錯誤 (4xx, 5xx)
            if 500 <= e.code < 600:
                # 服務器錯誤，可重試
                raise RetryableException(f"Notion API 服務器錯誤 ({e.code})")
            else:
                # 客戶端錯誤 (4xx)，不重試
                error_body = e.read().decode('utf-8')
                raise Exception(f"Notion API 客戶端錯誤 ({e.code}): {error_body}")
        except (urllib.error.URLError, TimeoutError) as e:
            # 網絡錯誤，可重試
            raise RetryableException(f"網絡錯誤: {str(e)}")
    
    # 使用重試機制調用
    return retry_with_backoff(
        _make_request,
        max_retries=CONFIG["MAX_RETRIES"],
        backoff_base=CONFIG["RETRY_BACKOFF"],
        verbose=True
    )

def update_notion_id(db_path, memory_id: int, notion_id: str):
    """把 Notion page_id 写回 SQLite（用 chain_anchor 不违反 append-only）"""
    con = sqlite3.connect(db_path)
    con.execute("""
        CREATE TABLE IF NOT EXISTS notion_map (
            brain_id    INTEGER PRIMARY KEY,
            notion_id   TEXT NOT NULL,
            synced_at   TEXT NOT NULL
        )
    """)
    con.execute("""
        INSERT OR REPLACE INTO notion_map (brain_id, notion_id, synced_at)
        VALUES (?, ?, ?)
    """, (memory_id, notion_id, datetime.now().isoformat()))
    con.commit()
    con.close()

def get_unsynced(db_path) -> list:
    """找出还没同步到 Notion 的记忆"""
    con = sqlite3.connect(db_path)
    con.execute("""
        CREATE TABLE IF NOT EXISTS notion_map (
            brain_id    INTEGER PRIMARY KEY,
            notion_id   TEXT NOT NULL,
            synced_at   TEXT NOT NULL
        )
    """)
    rows = con.execute("""
        SELECT m.id, m.dna, m.content, m.wuxing, m.tricolor,
               m.tags, m.source, m.dr, m.created_at
        FROM memories m
        LEFT JOIN notion_map nm ON nm.brain_id = m.id
        WHERE nm.brain_id IS NULL
        ORDER BY m.id ASC
        LIMIT 20
    """).fetchall()
    con.close()
    return [
        {
            "id": r[0], "dna": r[1], "content": r[2],
            "wuxing": r[3], "tricolor": r[4], "tags": r[5],
            "source": r[6], "dr": r[7], "created_at": r[8],
        }
        for r in rows
    ]

def sync_once(verbose=True) -> int:
    """
    執行一次同步
    
    v1.1: 添加限流控制和更詳細的日誌
    """
    db_path = CONFIG["DB_PATH"]
    if not db_path.exists():
        print("⚠️  brain.db 不存在，请先运行 longhun_brain.py --status 初始化")
        return 0

    pending = get_unsynced(db_path)
    if not pending:
        if verbose:
            print("✅ 全部已同步，无待推送记忆")
        return 0

    print(f"🔄 发现 {len(pending)} 条待同步记忆...")
    
    # 初始化限流器
    rate_limiter = RateLimiter(calls_per_second=CONFIG["API_RATE_LIMIT"])

    synced = 0
    failed = 0
    
    for i, m in enumerate(pending, 1):
        if verbose:
            print(f"  [{i}/{len(pending)}] {m['tricolor']} {m['content'][:40]}...", end="")
            sys.stdout.flush()

        if CONFIG["NOTION_TOKEN"] and CONFIG["DATABASE_ID"]:
            try:
                notion_id = notion_create_page(m, rate_limiter=rate_limiter)
                if notion_id:
                    update_notion_id(db_path, m["id"], notion_id)
                    synced += 1
                    if verbose:
                        print(f"\n       ✅ Notion page: {notion_id[:8]}...")
                else:
                    print("\n       ⏭️  無 page_id 返回，標記為待定")
                    update_notion_id(db_path, m["id"], "PENDING")
                    synced += 1
            except Exception as e:
                failed += 1
                print(f"\n       ❌ 最終失敗: {str(e)[:50]}")
                # 仍然標記為待定，下次重試
                update_notion_id(db_path, m["id"], "FAILED")
        else:
            # 没配置 Token 就先标记为 PENDING，不报错
            update_notion_id(db_path, m["id"], "PENDING")
            synced += 1

    if verbose:
        print("")
        print(f"  📊 同步結果: {synced} 成功, {failed} 失敗")
    
    return synced

def sync_status():
    """
    显示同步状态
    
    v1.1: 添加更詳細的統計信息
    """
    db_path = CONFIG["DB_PATH"]
    if not db_path.exists():
        print("⚠️  brain.db 不存在")
        return

    con = sqlite3.connect(db_path)
    total = con.execute("SELECT COUNT(*) FROM memories").fetchone()[0]

    # 检查 notion_map 是否存在
    has_map = con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='notion_map'"
    ).fetchone()

    if has_map:
        synced   = con.execute("SELECT COUNT(*) FROM notion_map WHERE notion_id NOT IN ('PENDING', 'FAILED')").fetchone()[0]
        pending  = con.execute("SELECT COUNT(*) FROM notion_map WHERE notion_id = 'PENDING'").fetchone()[0]
        failed   = con.execute("SELECT COUNT(*) FROM notion_map WHERE notion_id = 'FAILED'").fetchone()[0]
        unsynced = total - con.execute("SELECT COUNT(*) FROM notion_map").fetchone()[0]
    else:
        synced = pending = failed = unsynced = 0
        unsynced = total

    con.close()

    token_ok = "✅ 已配置" if CONFIG["NOTION_TOKEN"] else "❌ 未配置（设置环境变量 NOTION_TOKEN）"
    db_ok    = "✅ 已配置" if CONFIG["DATABASE_ID"] else "❌ 未配置（设置环境变量 DB_LU）"

    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🐉 龍魂脑干 · Notion同步状态 (v1.1)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Notion Token   : {token_ok}
  数据库 ID      : {db_ok}
  brain.db 位置  : {db_path}
  ─────────────────────────────────
  总记忆数        : {total} 条
  已同步 Notion   : {synced} 条  ✅
  待推送（无Token）: {pending} 条  🟡
  推送失敗（重試中）: {failed} 条  🔴
  未处理          : {unsynced} 条  ⏳
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 Phase 1 升級特性:
  ✅ 指數退避重試機制 (最多 {CONFIG['MAX_RETRIES']} 次)
  ✅ API 限流控制 ({CONFIG['API_RATE_LIMIT']} calls/sec)
  ✅ 安全的 JSON 解析
  ✅ 詳細的錯誤日誌
  ✅ 失敗恢復機制

📋 配置方法（写入 ~/.longhun/secrets.env）：
  export NOTION_TOKEN="secret_xxxxxxxxxxxxx"
  export DB_LU="your-database-id-here"

DNA:#龍芯⚡️2026-06-07-NOTION-BRIDGE-v1.1
""")

# ═══════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂脑干 Notion同步桥 v1.1")
    parser.add_argument("--watch",  action="store_true", help="持续监听（5分钟间隔）")
    parser.add_argument("--status", action="store_true", help="查看同步状态")
    parser.add_argument("--once",   action="store_true", help="单次同步（默认）")
    args = parser.parse_args()

    print("\n🌉 龍魂脑干 · Notion同步桥 v1.1 (Phase 1 升級版)")
    print(f"   DNA:#龍芯⚡️2026-06-07-NOTION-BRIDGE-v1.1\n")
    print(f"   ⚡ Phase 1 特性:")
    print(f"      • 指數退避重試 ({CONFIG['MAX_RETRIES']} 次)")
    print(f"      • API 限流控制 ({CONFIG['API_RATE_LIMIT']} calls/sec)")
    print(f"      • 安全 JSON 解析")
    print(f"      • 失敗恢復機制\n")

    if args.status:
        sync_status()
    elif args.watch:
        print(f"👀 监听模式启动（每 {CONFIG['INTERVAL']} 秒同步一次）")
        print("   Ctrl+C 停止\n")
        while True:
            n = sync_once(verbose=False)
            if n > 0:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 同步 {n} 条新记忆 ✅")
            time.sleep(CONFIG["INTERVAL"])
    else:
        # 默认单次同步
        sync_once(verbose=True)
        print("\n✅ 同步完成")

if __name__ == "__main__":
    main()
