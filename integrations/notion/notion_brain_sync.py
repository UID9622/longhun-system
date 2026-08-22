#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 Notion 大脑同步引擎 v2.0
Notion Brain Sync — 用 Notion 免费 API 作为外部知识脑

DNA: #龍芯⚡️丙午·乙未·壬辰·午时·䷄需-NOTION-BRAIN-v2.0
📇 项目身份 · 联系 · 支持 → assets/PUBLIC_IDENTITY.md

设计原则:
  - Notion 作为"外部大脑"存储知识库结构
  - 只用 Notion 免费 API（每个 integration 免费），不买 Notion AI
  - 本地是主，Notion 是镜像 — 数据主权归本地
  - 双向同步：本地 <-> Notion
  - 支持多账号：老账号(uid9622) + 新账号(uid9622@petalmail.com)

功能:
  - 拉取 Notion 数据库全量内容
  - 同步本地 Markdown 到 Notion
  - 知识图谱索引生成
  - 增量同步（按更新时间）
"""

import json
import os
import sys
import time
import hashlib
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any

import httpx

# ═══════════════════════════════════════════════════════
# 初始化
# ═══════════════════════════════════════════════════════

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from bin.lh_secrets_loader import get_credential

LOG_DIR = Path.home() / "longhun-system" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "notion_brain.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("notion_brain")

# ═══════════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════════

NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
BRAIN_CACHE = Path.home() / ".longhun" / "notion_brain_cache"
BRAIN_CACHE.mkdir(parents=True, exist_ok=True)

# 多账号配置
ACCOUNTS = {
    "primary": {
        "token_env": "NOTION_TOKEN",
        "email": "uid9622",
        "label": "主账号（老Notion）",
    },
    "petalmail": {
        "token_env": "NOTION_TOKEN_PETALMAIL",
        "email": "uid9622@petalmail.com",
        "label": "新账号（petalmail）",
    },
}

# 已知数据库 ID 映射
KNOWN_DATABASES = {
    "personas":       {"env": "NOTION_PERSONAS_DB",       "label": "人格库"},
    "routing_rules":  {"env": "NOTION_ROUTING_DB",        "label": "路由规则"},
    "knowledge_base": {"env": "NOTION_KNOWLEDGE_DB",      "label": "知识库"},
    "execution_logs": {"env": "NOTION_EXECUTION_DB",      "label": "执行日志"},
    "inbox":          {"env": "NOTION_INBOX_DB",          "label": "收集箱"},
    "snapshot":       {"env": "NOTION_SNAPSHOT_DB",       "label": "快照库"},
    "assets":         {"env": "NOTION_ASSETS_DB",         "label": "资产库"},
    "manifesto":      {"env": "NOTION_MANIFESTO_DB",      "label": "宣言库"},
    "violations":     {"env": "NOTION_VIOLATIONS_DB",     "label": "违规记录"},
    "conflicts":      {"env": "NOTION_CONFLICTS_DB",      "label": "冲突记录"},
}


# ═══════════════════════════════════════════════════════
# Notion 客户端
# ═══════════════════════════════════════════════════════

class NotionBrainClient:
    """Notion 大脑客户端 — 封装 Notion API"""
    
    def __init__(self, account: str = "primary"):
        if account not in ACCOUNTS:
            raise ValueError(f"未知账号: {account}. 可选: {list(ACCOUNTS.keys())}")
        
        self.account = account
        self.config = ACCOUNTS[account]
        self.token = get_credential(self.config["token_env"])
        
        if not self.token:
            logger.warning(f"⚠️ {self.config['label']} Token 未配置 ({self.config['token_env']})")
        
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_VERSION,
        }
        self.client = httpx.Client(timeout=30.0)
    
    def _request(self, method: str, path: str, **kwargs: Any) -> Optional[Dict[str, Any]]:
        """发送 Notion API 请求"""
        if not self.token:
            logger.error("❌ Token 未配置，无法请求")
            return None
        
        url = f"{NOTION_API}/{path}"
        try:
            resp = self.client.request(method, url, headers=self.headers, **kwargs)
            
            if resp.status_code == 429:
                # 速率限制 — 等1秒重试
                logger.warning("⏳ 速率限制，等待1秒...")
                time.sleep(1)
                resp = self.client.request(method, url, headers=self.headers, **kwargs)
            
            if resp.status_code == 200:
                return resp.json()
            else:
                logger.error(f"❌ API {method} {path} → {resp.status_code}: {resp.text[:200]}")
                return None
        except Exception as e:
            logger.error(f"❌ 请求异常: {e}")
            return None
    
    # ── 数据库操作 ──
    
    def query_database(self, database_id: str, filter_params: Optional[Dict[str, Any]] = None,
                       sorts: Optional[List[Dict[str, Any]]] = None, page_size: int = 100) -> List[Dict[str, Any]]:
        """查询数据库"""
        payload: dict[str, Any] = {"page_size": page_size}
        if filter_params:
            payload["filter"] = filter_params
        if sorts:
            payload["sorts"] = sorts
        
        all_results = []
        has_more = True
        start_cursor = None
        
        while has_more:
            if start_cursor:
                payload["start_cursor"] = start_cursor
            
            data = self._request("POST", f"databases/{database_id}/query", json=payload)
            if not data:
                break
            
            all_results.extend(data.get("results", []))
            has_more = data.get("has_more", False)
            start_cursor = data.get("next_cursor")
            
            if has_more:
                logger.info(f"   📄 分页... 已取 {len(all_results)} 条")
                time.sleep(0.3)  # 避免限流
        
        return all_results
    
    def get_database_info(self, database_id: str) -> Optional[Dict[str, Any]]:
        """获取数据库元信息"""
        return self._request("GET", f"databases/{database_id}")
    
    def search(self, query: str = "", filter_params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """搜索 Notion 内容"""
        payload = {}
        if query:
            payload["query"] = query
        if filter_params:
            payload["filter"] = filter_params
        
        data = self._request("POST", "search", json=payload)
        return data.get("results", []) if data else []
    
    # ── 页面操作 ──
    
    def get_page(self, page_id: str) -> Optional[Dict[str, Any]]:
        """获取页面内容"""
        return self._request("GET", f"pages/{page_id}")
    
    def get_block_children(self, block_id: str) -> List[Dict[str, Any]]:
        """获取 block 子元素"""
        data = self._request("GET", f"blocks/{block_id}/children?page_size=100")
        return data.get("results", []) if data else []
    
    def create_page(self, database_id: str, properties: Dict[str, Any],
                    children: Optional[List[Dict[str, Any]]] = None) -> Optional[Dict[str, Any]]:
        """在数据库中创建页面"""
        payload = {
            "parent": {"database_id": database_id},
            "properties": properties,
        }
        if children:
            payload["children"] = children
        
        return self._request("POST", "pages", json=payload)
    
    def update_page(self, page_id: str, properties: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """更新页面属性"""
        return self._request("PATCH", f"pages/{page_id}", json={"properties": properties})
    
    def append_blocks(self, block_id: str, children: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """追加 block 子元素"""
        return self._request("PATCH", f"blocks/{block_id}/children", json={"children": children})


# ═══════════════════════════════════════════════════════
# 同步引擎
# ═══════════════════════════════════════════════════════

class NotionBrainSync:
    """Notion 大脑同步引擎"""
    
    def __init__(self, account: str = "primary"):
        self.client = NotionBrainClient(account)
        self.account = account
        self.cache_file = BRAIN_CACHE / f"brain_snapshot_{account}.json"
    
    def pull_all_databases(self) -> Dict[str, List[Dict[str, Any]]]:
        """拉取所有已知数据库的内容"""
        result = {}
        for db_key, db_config in KNOWN_DATABASES.items():
            db_id = get_credential(db_config["env"])
            if not db_id:
                logger.info(f"  ⏭️  {db_key} ({db_config['label']}): 未配置 ID")
                continue
            
            logger.info(f"📥 拉取 {db_key} ({db_config['label']})...")
            pages = self.client.query_database(db_id)
            result[db_key] = pages
            logger.info(f"   ✅ {len(pages)} 条记录")
            time.sleep(0.5)  # 避免限流
        
        # 保存快照
        snapshot = {
            "account": self.account,
            "synced_at": datetime.now(timezone.utc).isoformat(),
            "databases": {k: len(v) for k, v in result.items()},
        }
        self.cache_file.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2))
        
        return result
    
    def pull_knowledge_base(self) -> List[Dict[str, Any]]:
        """拉取知识库内容（核心）"""
        db_id = get_credential("NOTION_KNOWLEDGE_DB")
        if not db_id:
            logger.error("❌ 知识库 ID 未配置")
            return []
        
        logger.info("📚 拉取知识库...")
        pages = self.client.query_database(db_id)
        logger.info(f"   📊 共 {len(pages)} 条知识条目")
        return pages
    
    def search_brain(self, query: str) -> List[Dict[str, Any]]:
        """在 Notion 大脑中搜索"""
        return self.client.search(query)
    
    def sync_local_to_notion(self, local_path: Path, database_id: str) -> bool:
        """
        将本地 Markdown 同步到 Notion 数据库
        
        这实现了"本地是主，Notion是镜像"的数据主权原则
        """
        if not local_path.exists():
            logger.error(f"❌ 文件不存在: {local_path}")
            return False
        
        content = local_path.read_text(encoding="utf-8")
        title = local_path.stem
        
        # 构建 Notion 页面属性
        properties = {
            "Name": {"title": [{"text": {"content": title}}]},
            "Source": {"rich_text": [{"text": {"content": str(local_path)}}]},
            "Synced": {"date": {"start": datetime.now(timezone.utc).isoformat()}},
        }
        
        # 构建内容 blocks
        blocks = _markdown_to_notion_blocks(content)
        
        result = self.client.create_page(database_id, properties, blocks)
        if result:
            logger.info(f"✅ 已同步: {title} → Notion ({result.get('id', '?')})")
            return True
        return False


# ═══════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════

def _markdown_to_notion_blocks(md_text: str) -> List[Dict[str, Any]]:
    """简单 Markdown → Notion Blocks 转换"""
    blocks = []
    for line in md_text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("# "):
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {"rich_text": [{"type": "text", "text": {"content": line[2:]}}]}
            })
        elif line.startswith("## "):
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"type": "text", "text": {"content": line[3:]}}]}
            })
        elif line.startswith("### "):
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {"rich_text": [{"type": "text", "text": {"content": line[4:]}}]}
            })
        elif line.startswith("- "):
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": line[2:]}}]}
            })
        elif line.startswith("```"):
            blocks.append({
                "object": "block",
                "type": "code",
                "code": {"rich_text": [{"type": "text", "text": {"content": line[3:].strip()}}],
                         "language": "plain text"}
            })
        else:
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": line}}]}
            })
    return blocks


# ═══════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="龍魂 Notion 大脑同步引擎")
    parser.add_argument("action", nargs="?", default="status",
                        choices=["status", "pull", "search", "sync"],
                        help="操作: status/pull/search/sync")
    parser.add_argument("--account", default="primary",
                        choices=list(ACCOUNTS.keys()),
                        help="Notion 账号")
    parser.add_argument("--query", default="", help="搜索关键词")
    parser.add_argument("--file", help="要同步的本地文件路径")
    parser.add_argument("--db", default="knowledge_base",
                        choices=list(KNOWN_DATABASES.keys()),
                        help="目标数据库")
    
    args = parser.parse_args()
    engine = NotionBrainSync(args.account)
    
    if args.action == "status":
        print(f"🧠 Notion 大脑状态 [{args.account}]")
        print(f"   账号: {ACCOUNTS[args.account]['label']}")
        token = get_credential(ACCOUNTS[args.account]["token_env"])
        print(f"   Token: {'🟢 已配置' if token else '🔴 未配置'}")
        print(f"\n📊 数据库配置:")
        for db_key, db_config in KNOWN_DATABASES.items():
            db_id = get_credential(db_config["env"])
            print(f"   {'🟢' if db_id else '🔴'} {db_key}: {db_config['label']}")
    
    elif args.action == "pull":
        data = engine.pull_all_databases()
        total = sum(len(v) for v in data.values())
        print(f"\n✅ 拉取完成: {len(data)} 个数据库, {total} 条记录")
    
    elif args.action == "search":
        if not args.query:
            print("用法: --query \"关键词\"")
            sys.exit(1)
        results = engine.search_brain(args.query)
        print(f"🔍 搜索 \"{args.query}\": {len(results)} 条结果")
        for r in results[:10]:
            title = r.get("properties", {}).get("Name", {}).get("title", [{}])[0].get("plain_text", "无标题")
            print(f"   📄 {title}")
    
    elif args.action == "sync":
        if not args.file:
            print("用法: --file /path/to/file.md")
            sys.exit(1)
        filepath = Path(args.file)
        db_id = get_credential(KNOWN_DATABASES[args.db]["env"])
        if not db_id:
            print(f"❌ 数据库 {args.db} 未配置 ID")
            sys.exit(1)
        ok = engine.sync_local_to_notion(filepath, db_id)
        sys.exit(0 if ok else 1)
