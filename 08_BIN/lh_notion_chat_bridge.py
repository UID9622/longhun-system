#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · Notion 对话桥 v2.3 (人格引擎深度集成 + 多模型协作增强版)
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-NOTION-BRIDGE-v2.3-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  1. 自然语言对话 Notion (RAG 检索 + Ollama 本地推理)
  2. 人格矩阵深度集成 (自动匹配、切换、联动)
  3. 智能导航 (意图识别·自动跳转·关联推荐)
  4. 记忆共享 (跨人格、跨会话)
  5. 全量同步引擎 (FTS5·批量拉取·增量更新)
  6. Web 面板 + REST API

用法：
  lh notion-bridge [--port 8779] [--host 127.0.0.1]
  lh notion-bridge sync                      # 全量同步
  lh notion-bridge search "关键词"            # 命令行搜索
  lh notion-bridge chat "问题"                # 命令行对话
  lh notion-bridge status                    # 状态查看
"""

import os
import sys
import json
import re
import time
import asyncio
import sqlite3
import hashlib
import threading
import subprocess
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
except ImportError:
    requests = None

try:
    from fastapi import FastAPI, HTTPException, Request, Query
    from fastapi.responses import JSONResponse, HTMLResponse
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    import uvicorn
except ImportError:
    print("⚠️ 请安装: pip install fastapi uvicorn")
    sys.exit(1)

# ============================================================
# 项目根路径
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ============================================================
# 导入人格引擎
# ============================================================

# 人格引擎（可选集成：import 失败时降级占位，保持 API 不阻断）
PersonaRuntime: Any = None
PersonaBridge: Any = None
try:
    from bin.lh_persona_runtime import PersonaRuntime, PersonaBridge
    PERSONA_AVAILABLE = True
except ImportError:
    print("⚠️ 人格引擎未找到，部分功能不可用")
    PERSONA_AVAILABLE = False

if not PERSONA_AVAILABLE:

    class _PersonaRuntimeStub:
        """降级占位：人格引擎缺失时保持离线"""

        def __init__(self, *_args, **_kwargs):
            pass

        def list_personas(self) -> list:
            return []

        def get_current(self, *_args, **_kwargs):
            return None

        def set_current(self, *_args, **_kwargs):
            return None

        def trigger_chain(self, *_args, **_kwargs):
            return None

    class _PersonaBridgeStub:
        """降级占位：人格桥缺失时保持离线"""

        def __init__(self, *_args, **_kwargs):
            pass

        def handle(self, *_args, **_kwargs):
            pass

        def match(self, *_args, **_kwargs):
            return None

        def trigger_chain(self, *_args, **_kwargs):
            return None

    PersonaRuntime = _PersonaRuntimeStub
    PersonaBridge = _PersonaBridgeStub

# 五行议事会（可选集成：import 失败时降级占位，保持 API 不阻断）
WuxingModelCouncil: Any = None
try:
    from bin.lh_notion_council import WuxingModelCouncil
    COUNCIL_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ 五行议事会未加载: {e}")
    COUNCIL_AVAILABLE = False

if not COUNCIL_AVAILABLE:

    class _BaguaStub:
        """降级占位：八卦信息离线"""

        def info(self, *_args, **_kwargs):
            return {"trigram": "䷀", "note": "五行议事会离线"}

    class _WuxingModelCouncilStub:
        """降级占位：五行议事会缺失时保持离线"""

        def __init__(self, *_args, **_kwargs):
            self.bagua = _BaguaStub()

        def status(self):
            return {"status": "offline", "reason": "五行议事会未加载"}

    WuxingModelCouncil = _WuxingModelCouncilStub

# ============================================================
# 配置
# ============================================================

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
DATA_DIR = PROJECT_ROOT / "data"
SYNC_DB = DATA_DIR / "notion_sync.db"
CHAT_HISTORY_DB = DATA_DIR / "notion_chat_history.db"
DATA_DIR.mkdir(parents=True, exist_ok=True)

def _load_env_token() -> str:
    """从 ~/.env 兜底读取 Notion token（launchd 环境不含此变量时生效）"""
    _env_path = Path.home() / ".env"
    try:
        for _line in _env_path.read_text(encoding="utf-8").splitlines():
            _line = _line.strip()
            if not _line or _line.startswith("#") or "=" not in _line:
                continue
            _k, _, _v = _line.partition("=")
            if _k.strip() in ("NOTION_TOKEN", "NOTION_API_KEY") and _v.strip():
                return _v.strip()
    except (OSError, UnicodeDecodeError):
        pass
    return ""


NOTION_TOKEN = (
    os.environ.get("NOTION_TOKEN")
    or os.environ.get("NOTION_API_KEY")
    or _load_env_token()
)
NOTION_VERSION = "2022-06-28"
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("NOTION_CHAT_MODEL", "longhun-v4.0")
DEFAULT_PROVIDER = os.environ.get("NOTION_CHAT_PROVIDER", "auto")  # auto | local | deepseek | kimi
CHAT_PRIVACY = os.environ.get("NOTION_CHAT_PRIVACY", "normal")  # normal | strict

# API 配置
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
KIMI_API_KEY = os.environ.get("KIMI_API_KEY", "") or os.environ.get("MOONSHOT_API_KEY", "")
KIMI_BASE_URL = os.environ.get("KIMI_BASE_URL", "https://api.moonshot.cn/v1")

# 协议底座
DEFAULT_SYSTEM_PROMPT = (
    "你是一位严谨、简洁的中文助手。"
    "请用通顺、完整的中文句子回答问题。"
    "不要输出无意义的符号、乱码、重复片段或夹杂着 UID/确认码的碎片。"
    "如果资料不足，请直接说明。"
)

# ============================================================
# 聊天历史数据库
# ============================================================

def init_chat_db():
    conn = sqlite3.connect(str(CHAT_HISTORY_DB))
    conn.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            message TEXT,
            response TEXT,
            persona_ipa TEXT,
            persona_name TEXT,
            chain_info TEXT,
            model_provider TEXT,
            model_name TEXT,
            model_dna TEXT,
            audit_status TEXT,
            council_members TEXT,
            bagua_state TEXT,
            synthesis_log TEXT,
            consensus_score REAL,
            created_at TEXT
        )
    ''')
    # 兼容旧表：追加模型相关列
    for col, dtype in [
        ("model_provider", "TEXT"),
        ("model_name", "TEXT"),
        ("model_dna", "TEXT"),
        ("audit_status", "TEXT"),
        ("council_members", "TEXT"),
        ("bagua_state", "TEXT"),
        ("synthesis_log", "TEXT"),
        ("consensus_score", "REAL"),
    ]:
        try:
            conn.execute(f"ALTER TABLE chat_history ADD COLUMN {col} {dtype}")
        except sqlite3.OperationalError:
            pass
    conn.execute('''
        CREATE TABLE IF NOT EXISTS chat_sessions (
            session_id TEXT PRIMARY KEY,
            current_persona_ipa TEXT,
            context TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_chat(session_id: str, message: str, response: str,
              persona_ipa: str = "", persona_name: str = "", chain_info: str = "",
              model_provider: str = "", model_name: str = "", model_dna: str = "",
              audit_status: str = "", council_members: str = "", bagua_state: str = "",
              synthesis_log: str = "", consensus_score: float = 0.0):
    conn = sqlite3.connect(str(CHAT_HISTORY_DB))
    conn.execute(
        """INSERT INTO chat_history
           (session_id, message, response, persona_ipa, persona_name, chain_info,
            model_provider, model_name, model_dna, audit_status,
            council_members, bagua_state, synthesis_log, consensus_score, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (session_id, message, response, persona_ipa, persona_name, chain_info,
         model_provider, model_name, model_dna, audit_status,
         council_members, bagua_state, synthesis_log, consensus_score,
         datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def get_chat_history(session_id: str, limit: int = 20) -> List[Dict]:
    conn = sqlite3.connect(str(CHAT_HISTORY_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM chat_history WHERE session_id = ? ORDER BY id DESC LIMIT ?",
        (session_id, limit)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_session_persona(session_id: str, persona_ipa: str, context: str = ""):
    conn = sqlite3.connect(str(CHAT_HISTORY_DB))
    conn.execute(
        "INSERT OR REPLACE INTO chat_sessions (session_id, current_persona_ipa, context, created_at, updated_at) VALUES (?, ?, ?, COALESCE((SELECT created_at FROM chat_sessions WHERE session_id=?), ?), ?)",
        (session_id, persona_ipa, context, session_id, datetime.now().isoformat(), datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def get_session(session_id: str) -> Optional[Dict]:
    conn = sqlite3.connect(str(CHAT_HISTORY_DB))
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM chat_sessions WHERE session_id=?", (session_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

# ============================================================
# Notion 客户端（零依赖·保留v1.0所有能力）
# ============================================================

class NotionClient:
    """零依赖 Notion API 客户端"""

    def __init__(self, token: Optional[str] = None):
        self.token = token or NOTION_TOKEN
        self.base_url = "https://api.notion.com/v1"
        self.version = NOTION_VERSION

    def _request(self, method: str, path: str, data: Optional[Dict] = None) -> Dict:
        if not self.token:
            return {"error": "NOTION_API_KEY 未设置"}
        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": self.version,
            "Content-Type": "application/json",
        }
        req = urllib.request.Request(url, method=method, headers=headers)
        if data:
            req.data = json.dumps(data).encode('utf-8')
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8') if e.fp else "{}"
            return {"error": f"HTTP {e.code}", "details": body}
        except Exception as e:
            return {"error": str(e)}

    def search(self, query: str, page_size: int = 20, start_cursor: Optional[str] = None) -> Dict:
        payload = {"query": query, "page_size": page_size}
        if start_cursor:
            payload["start_cursor"] = start_cursor
        return self._request("POST", "search", payload)

    def get_page(self, page_id: str) -> Dict:
        return self._request("GET", f"pages/{page_id}")

    def get_blocks(self, block_id: str, start_cursor: Optional[str] = None) -> Dict:
        url = f"blocks/{block_id}/children?page_size=100"
        if start_cursor:
            url += f"&start_cursor={start_cursor}"
        return self._request("GET", url)

    def query_database(self, database_id: str, start_cursor: Optional[str] = None, filter_obj: Optional[Dict] = None) -> Dict:
        payload: dict = {"page_size": 100}
        if start_cursor:
            payload["start_cursor"] = start_cursor
        if filter_obj:
            payload["filter"] = filter_obj
        return self._request("POST", f"databases/{database_id}/query", payload)

# ============================================================
# 本地同步数据库 (FTS5 全文搜索)
# ============================================================

def init_sync_db():
    conn = sqlite3.connect(str(SYNC_DB))
    conn.execute('''
        CREATE TABLE IF NOT EXISTS pages (
            id TEXT PRIMARY KEY,
            title TEXT,
            url TEXT,
            created_time TEXT,
            last_edited_time TEXT,
            icon TEXT,
            archived INTEGER DEFAULT 0,
            synced_at TEXT
        )
    ''')
    conn.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS pages_fts USING fts5(
            title, content, content='pages', content_rowid='rowid'
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS blocks (
            id TEXT PRIMARY KEY,
            page_id TEXT,
            block_type TEXT,
            content TEXT,
            parent_id TEXT,
            has_children INTEGER DEFAULT 0,
            synced_at TEXT
        )
    ''')
    conn.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS blocks_fts USING fts5(
            content, content='blocks', content_rowid='rowid'
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS sync_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            target TEXT,
            status TEXT,
            details TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def extract_text_from_block(block: Dict) -> str:
    """递归提取块中的文本"""
    texts = []
    block_type = block.get("type", "unknown")

    if block_type in block:
        content = block[block_type]
        # rich_text
        if isinstance(content, dict):
            for rt_key in ["rich_text", "title", "caption"]:
                rt = content.get(rt_key, [])
                if rt:
                    texts.append("".join([t.get("plain_text", "") for t in rt]))
            # 子块
            children = content.get("children", [])
            for child in children:
                texts.append(extract_text_from_block(child))
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, dict):
                    if item.get("type") == "text":
                        texts.append(item.get("plain_text", ""))
                    elif "rich_text" in item:
                        texts.append("".join([t.get("plain_text", "") for t in item.get("rich_text", [])]))

    return "\n".join(texts)

def sync_pages(client: NotionClient, _query: str = "", database_id: Optional[str] = None):
    """全量/增量同步页面"""
    conn = sqlite3.connect(str(SYNC_DB))
    synced = 0

    if database_id:
        # 按数据库同步
        all_results = []
        start_cursor = None
        while True:
            res = client.query_database(database_id, start_cursor=start_cursor)
            if "error" in res:
                break
            results = res.get("results", [])
            all_results.extend(results)
            if not res.get("has_more"):
                break
            start_cursor = res.get("next_cursor")

        for page in all_results:
            page_id = page.get("id")
            title = ""
            props = page.get("properties", {})
            for prop in props.values():
                if prop.get("type") == "title":
                    title = "".join([t.get("plain_text", "") for t in prop.get("title", [])])
                    break
            conn.execute(
                "INSERT OR REPLACE INTO pages (id, title, url, created_time, last_edited_time, archived, synced_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (page_id, title, page.get("url", ""), page.get("created_time", ""),
                 page.get("last_edited_time", ""), 1 if page.get("archived") else 0, datetime.now().isoformat())
            )
            # 同步块内容
            sync_page_blocks(client, page_id, conn)
            synced += 1

    conn.commit()
    conn.close()

    # 记录同步日志
    _log_sync("full_sync", f"db:{database_id or 'search'}", "success", f"synced {synced} pages")
    return synced

def sync_page_blocks(client: NotionClient, page_id: str, conn):
    """同步页面的所有块"""
    all_blocks = []
    start_cursor = None
    while True:
        res = client.get_blocks(page_id, start_cursor=start_cursor)
        if "error" in res:
            break
        blocks = res.get("results", [])
        all_blocks.extend(blocks)
        if not res.get("has_more"):
            break
        start_cursor = res.get("next_cursor")

    for block in all_blocks:
        block_id = block.get("id")
        block_type = block.get("type", "unknown")
        content = extract_text_from_block(block)
        conn.execute(
            "INSERT OR REPLACE INTO blocks (id, page_id, block_type, content, parent_id, has_children, synced_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (block_id, page_id, block_type, content, block.get("parent", {}).get("block_id", ""),
             1 if block.get("has_children") else 0, datetime.now().isoformat())
        )

def _log_sync(action: str, target: str, status: str, details: str = ""):
    conn = sqlite3.connect(str(SYNC_DB))
    conn.execute(
        "INSERT INTO sync_log (action, target, status, details, created_at) VALUES (?, ?, ?, ?, ?)",
        (action, target, status, details, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def search_local(query: str, limit: int = 10) -> List[Dict]:
    """本地 FTS5 搜索"""
    conn = sqlite3.connect(str(SYNC_DB))
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            "SELECT b.page_id, b.content, p.title, p.url, p.last_edited_time FROM blocks_fts f JOIN blocks b ON f.rowid = b.rowid JOIN pages p ON b.page_id = p.id WHERE blocks_fts MATCH ? ORDER BY rank LIMIT ?",
            (query, limit)
        ).fetchall()
    except:
        rows = []

    results = []
    for row in rows:
        results.append(dict(row))
    conn.close()
    return results

def search_remote(client: NotionClient, query: str, limit: int = 10) -> List[Dict]:
    """远程 Notion API 搜索"""
    res = client.search(query, page_size=limit)
    if "error" in res:
        return []

    pages = []
    for item in res.get("results", []):
        title = "未命名"
        props = item.get("properties", {})
        for prop in props.values():
            if prop.get("type") == "title":
                title = "".join([t.get("plain_text", "") for t in prop.get("title", [])])
                break
        pages.append({
            "id": item.get("id"),
            "title": title,
            "url": item.get("url", ""),
            "last_edited": item.get("last_edited_time", ""),
            "type": "page"
        })
    return pages

def search_hybrid(client: NotionClient, query: str, limit: int = 10) -> List[Dict]:
    """混合搜索：本地FTS5 + 远程Notion API"""
    local = search_local(query, limit)
    if local:
        return local
    return search_remote(client, query, limit)

def extract_keywords(query: str) -> List[str]:
    """提取中文关键词"""
    words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', query)
    stopwords = {'的','了','是','在','我','有','和','就','不','人','都','一','个','上','也','很','到','说','要','去','你','会','着','没有','看','好','自己','这','那','什么','怎么','为','以','与','而','但','被','从','让','给','对','把','向','将','更','还','又','再','可以','能','会','应该','可能','需要'}
    return [w for w in words if w not in stopwords and len(w) > 1][:5]

# ============================================================
# 多模型协作路由（本地 Ollama + 自训练模型 + DeepSeek + Kimi）
# ============================================================

def looks_gibberish(text: str) -> tuple[bool, str]:
    """启发式检测模型输出是否为乱码/无意义碎片。

    返回 (是否乱码, 原因标签)。当检测到乱码时，调用方应返回统一提示语。
    """
    if not text:
        return True, "empty"
    if len(text) < 2:
        return True, "too_short"

    total = len(text)
    chinese = len(re.findall(r'[\u4e00-\u9fff]', text))
    letters = len(re.findall(r'[a-zA-Z]', text))
    digits = len(re.findall(r'[0-9]', text))
    punct = len(re.findall(r'[\u3000-\u303f\uff00-\uffef.,;:!?\-"\'()\[\]{}\/\\@#$%&*+=_`~|<>]', text))
    whitespace = text.count(' ') + text.count('\n') + text.count('\t')

    text_chars = chinese + letters
    non_text = total - text_chars

    # 文字（中文+英文）占比过低
    if text_chars / total < 0.3:
        return True, "low_text_ratio"

    # 数字占比过高（>25%）通常意味着碎片/编号乱码
    if digits / total > 0.25:
        return True, "high_digit_ratio"

    # 标点/空白占比过高（>40%）
    if (punct + whitespace) / total > 0.4:
        return True, "high_punct_ratio"

    # 连续重复同一个非文字字符 3 次以上
    if re.search(r'([^\u4e00-\u9fffa-zA-Z0-9])\1{2,}', text):
        return True, "repeated_symbol"

    # 连续 3 个以上非文字 token 碎片（如 =、!、。、· 混合）
    if re.search(r'[=!。\u00b7\u2022]{3,}', text):
        return True, "symbol_cluster"

    # 出现典型的模型垃圾关键词组合（保留项目专属词，避免误伤正常输出）
    suspicious = ['UID', '9622']
    suspicious_hits = sum(1 for s in suspicious if s in text)
    if suspicious_hits >= 2 and punct / total > 0.15:
        return True, "suspicious_combo"

    # 包含 UID 且数字或标点占比高
    if 'UID' in text and (digits / total > 0.15 or punct / total > 0.15):
        return True, "uid_fragment"

    # 有效中文字符太少（<6）且整体较短，容易是碎片
    # 但保留常见短问候（如 "你好！")
    common_greetings = {"你好", "您好", "hello", "hi", "嗨", "哈喽", " Hallo"}
    is_greeting = any(g in text.lower() for g in common_greetings)
    if chinese < 6 and total < 40 and non_text / total > 0.3 and not is_greeting:
        return True, "few_chinese_chars"

    # 单字重复率过高
    char_counts = {}
    for ch in text:
        char_counts[ch] = char_counts.get(ch, 0) + 1
    if char_counts and max(char_counts.values()) / total > 0.3:
        return True, "char_repeat"

    # 包含确认码/特殊令牌模式的零碎输出
    if re.search(r'CONFIRM[🌌🧬]', text):
        return True, "confirm_token"

    return False, "ok"


def generate_dna(prefix: str) -> str:
    """生成 DNA 追溯码"""
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")[:-3]
    h = hashlib.sha256(f"{prefix}:{ts}:{CONFIRM_CODE}".encode()).hexdigest()[:12].upper()
    return f"#龍芯⚡️{ts}-NOTION-CHAT-{prefix}-{h}"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ============================================================
# 模型注册表（本地 + 云端能力声明）
# ============================================================

MODEL_REGISTRY_FILE = DATA_DIR / "notion_model_registry.json"


def load_model_registry() -> Dict[str, Any]:
    """加载 notion_model_registry.json；失败时返回最小化兜底结构。"""
    if MODEL_REGISTRY_FILE.exists():
        try:
            data = json.loads(MODEL_REGISTRY_FILE.read_text(encoding="utf-8"))
            return data
        except Exception as e:
            print(f"⚠️ 模型注册表加载失败: {e}")
    return {
        "registry_dna": generate_dna("MODEL-REGISTRY-FALLBACK"),
        "confirm_code": CONFIRM_CODE,
        "protocol_version": "v3.0",
        "sovereignty": "龍魂UID9622",
        "models": [],
    }


def is_self_trained_model(model_name: str, registry: Optional[Dict[str, Any]] = None) -> bool:
    """根据 registry + 名称前缀判定自训练模型。"""
    if not model_name:
        return False
    if any(model_name.lower().startswith(p.lower()) for p in ("longhun-", "龍魂-")):
        return True
    if registry:
        for m in registry.get("models", []):
            if m.get("id", "").lower() == model_name.lower():
                return bool(m.get("self_trained", False))
    return False


# ============================================================
# 统一协议信封与 P0 熔断守卫
# ============================================================

PROTOCOL_VERSION = "v3.0"


def protocol_envelope(data: Dict[str, Any], router_dna: str, **overrides) -> Dict[str, Any]:
    """为所有 /api/* 响应加盖协议信封。保留已有 council 字段，合并而非覆盖。"""
    envelope = {
        "dna": data.get("dna") or data.get("model_dna") or generate_dna("API"),
        "confirm_code": CONFIRM_CODE,
        "sovereignty": "龍魂UID9622",
        "protocol_version": PROTOCOL_VERSION,
        "audit_status": data.get("audit_status")
        if data.get("audit_status") is not None
        else ("green" if data.get("status") == "ok" else "yellow"),
        "model_provider": data.get("model_provider") or data.get("provider") or "",
        "model_name": data.get("model_name") or data.get("model") or "",
        "model_dna": data.get("model_dna") or data.get("dna") or "",
        "fallback_chain": data.get("fallback_chain") or [],
        "timestamp": _now(),
        "router_dna": router_dna,
    }
    # 允许调用方显式覆盖顶层字段
    for k, v in overrides.items():
        if v is not None:
            envelope[k] = v
    # 合并原始 data 中尚未进入 envelope 的字段（避免覆盖 envelope 关键字段）
    merged = {**data, **envelope}
    # 若原始 data 包含 council 相关字段，保留它们
    for council_key in [
        "council_members", "bagua_state", "synthesis_log", "consensus_score",
        "similarities", "total_latency_ms", "strategy", "mode", "privacy"
    ]:
        if council_key in data:
            merged[council_key] = data[council_key]
    return merged


class ProtocolGuard:
    """轻量级 P0 红线扫描：D1/D2 敏感信息 + 反协议关键词。"""

    SENSITIVE_PATTERNS = [
        (r"-----BEGIN\s+(PGP|OPENSSH|DSA|RSA|EC)\s+PRIVATE\s+KEY-----", "GPG/SSH 私钥"),
        (r"-----BEGIN\s+PRIVATE\s+KEY-----", "通用私钥"),
        (r"[\w\-]+\.[\w\-]*private[\w\-]*\.(asc|key|pem|txt)", "私钥文件路径"),
        (r"\bpassword\s*[:=]\s*\S+", "明文密码"),
        (r"\bpasswd\s+\S+", "passwd 明文"),
        (r"\bssh-rsa\s+[A-Za-z0-9+/]{100,}={0,2}", "SSH 公钥敏感"),
        (r"\b[A-Fa-f0-9]{64}\b", "64位十六进制敏感"),
    ]

    ANTI_PROTOCOL_KEYWORDS = [
        "删除记录", "绕过审计", "篡改DNA", "覆盖P0", "修改宪法", "删除龍魂",
        "删除日志", "删除档案", "隐藏数据", "隐藏记录", "隐藏审计",
    ]

    FUSE_PLACEHOLDER = "[已熔断·P0]"

    @classmethod
    def scan(cls, text: str) -> Dict[str, Any]:
        """扫描文本，返回 {cleaned, triggered, audit_status, reasons, fuse_count}。"""
        if not text:
            return {"cleaned": text, "triggered": False, "audit_status": "green", "reasons": [], "fuse_count": 0}

        cleaned = text
        reasons = []

        for pattern, label in cls.SENSITIVE_PATTERNS:
            matches = list(re.finditer(pattern, cleaned, re.IGNORECASE))
            for m in reversed(matches):
                reasons.append(f"D1敏感({label}): {m.group()[:40]}...")
                cleaned = cleaned[:m.start()] + cls.FUSE_PLACEHOLDER + cleaned[m.end():]

        for kw in cls.ANTI_PROTOCOL_KEYWORDS:
            idx = cleaned.lower().find(kw.lower())
            while idx != -1:
                reasons.append(f"P0反协议关键词: {kw}")
                end = idx + len(kw)
                cleaned = cleaned[:idx] + cls.FUSE_PLACEHOLDER + cleaned[end:]
                idx = cleaned.lower().find(kw.lower())

        triggered = bool(reasons)
        return {
            "cleaned": cleaned,
            "triggered": triggered,
            "audit_status": "red" if triggered else "green",
            "reasons": reasons,
            "fuse_count": len(reasons),
            "fallback_note": "⚠️ 输出触发 P0 熔断，已替换敏感/反协议片段。" if triggered else "",
        }

    @classmethod
    def guard(cls, result: Dict[str, Any]) -> Dict[str, Any]:
        """对模型生成结果执行守卫，并更新 audit_status / reply。"""
        reply = result.get("reply", "") or ""
        scan = cls.scan(reply)
        if scan["triggered"]:
            result["reply"] = scan["cleaned"] + "\n\n" + scan["fallback_note"]
            result["audit_status"] = "red"
            result["protocol_guard"] = {
                "triggered": True,
                "reasons": scan["reasons"],
                "fuse_count": scan["fuse_count"],
            }
        else:
            result.setdefault("audit_status", "green")
            result["protocol_guard"] = {"triggered": False, "reasons": [], "fuse_count": 0}
        return result


# ============================================================
# 多模型协作底座：熔断器、探测缓存、模型能力注册表
# ============================================================

class CircuitBreaker:
    """简单熔断器：连续失败 N 次后进入 cooldown 秒。"""

    def __init__(self, failure_threshold: int = 3, cooldown_seconds: float = 60.0):
        self.failure_threshold = failure_threshold
        self.cooldown_seconds = cooldown_seconds
        self._failures: Dict[str, int] = {}
        self._open_until: Dict[str, float] = {}
        self._lock = threading.Lock()

    def record_success(self, name: str):
        with self._lock:
            self._failures[name] = 0
            self._open_until.pop(name, None)

    def record_failure(self, name: str) -> bool:
        """返回 True 表示已触发熔断。"""
        with self._lock:
            now = time.time()
            if name in self._open_until and now < self._open_until[name]:
                return True
            self._failures[name] = self._failures.get(name, 0) + 1
            if self._failures[name] >= self.failure_threshold:
                self._open_until[name] = now + self.cooldown_seconds
                return True
            return False

    def is_open(self, name: str) -> bool:
        with self._lock:
            now = time.time()
            until = self._open_until.get(name)
            if until and now < until:
                return True
            if until and now >= until:
                # cooldown 结束，进入半开
                self._open_until.pop(name, None)
                self._failures[name] = 0
            return False

    def status(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            now = time.time()
            return {
                name: {
                    "failures": failures,
                    "open": self.is_open(name),
                    "open_remaining_sec": max(0, int(self._open_until.get(name, now) - now)) if name in self._open_until else 0,
                }
                for name, failures in self._failures.items()
            }


class ProbeCache:
    """带 TTL 的探测缓存，避免每次请求都 hammer /models。"""

    def __init__(self, ttl_seconds: float = 30.0):
        self.ttl = ttl_seconds
        self._cache: Dict[str, tuple[float, Dict[str, Any]]] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            if key not in self._cache:
                return None
            ts, value = self._cache[key]
            if time.time() - ts > self.ttl:
                self._cache.pop(key, None)
                return None
            return value

    def set(self, key: str, value: Dict[str, Any]):
        with self._lock:
            self._cache[key] = (time.time(), value)

    def invalidate(self, key: Optional[str] = None):
        with self._lock:
            if key is None:
                self._cache.clear()
            else:
                self._cache.pop(key, None)


class ModelCapability:
    """模型能力标签，支持按任务意图优选模型；优先读取 registry。"""

    SELF_TRAINED_PREFIXES = ("longhun-v", "longhun-", "龍魂-")
    _REGISTRY: Optional[Dict[str, Any]] = None

    CAPABILITY_MAP: Dict[str, List[str]] = {
        # 本地/自训练模型
        "longhun-v4.0": ["self_trained", "general", "chinese", "sovereignty"],
        "longhun-v43-v3:latest": ["self_trained", "general", "chinese", "sovereignty"],
        "longhun-v3.0": ["self_trained", "general", "chinese"],
        "longhun-judge:latest": ["self_trained", "audit", "chinese", "sovereignty"],
        "qwen2.5": ["local", "general", "chinese"],
        "qwen2.5:14b": ["local", "general", "chinese", "coding"],
        "qwen2.5:32b": ["local", "general", "chinese", "coding", "reasoning"],
        "llama3.1": ["local", "general"],
        "deepseek-r1:14b": ["local", "reasoning", "chinese"],
        # API 模型
        "deepseek-chat": ["cloud", "general", "chinese"],
        "deepseek-reasoner": ["cloud", "reasoning", "chinese"],
        "moonshot-v1-8k": ["cloud", "general", "chinese"],
        "moonshot-v1-32k": ["cloud", "general", "chinese", "long_context"],
        "moonshot-v1-128k": ["cloud", "general", "chinese", "long_context"],
        "moonshot-v1-auto": ["cloud", "general", "chinese", "auto"],
    }

    @classmethod
    def set_registry(cls, registry: Dict[str, Any]):
        cls._REGISTRY = registry

    @classmethod
    def _registry_entry(cls, model_name: str) -> Optional[Dict[str, Any]]:
        if not cls._REGISTRY:
            return None
        for m in cls._REGISTRY.get("models", []):
            mid = m.get("id", "")
            if mid.lower() == model_name.lower():
                return m
            # 兼容带 tag 的 ollama 名称，如 qwen2.5:14b
            if model_name.lower().startswith(mid.lower() + ":"):
                return m
        return None

    @classmethod
    def tags(cls, model_name: str) -> List[str]:
        entry = cls._registry_entry(model_name)
        if entry and entry.get("capabilities"):
            return list(entry["capabilities"])
        mn = model_name.split(":")[0].lower() if model_name else ""
        for key, tags in cls.CAPABILITY_MAP.items():
            if mn == key.lower() or model_name.lower().startswith(key.lower()):
                return list(tags)
        if any(model_name.lower().startswith(p.lower()) for p in cls.SELF_TRAINED_PREFIXES):
            return ["self_trained", "general", "chinese"]
        return ["unknown"]

    @classmethod
    def is_self_trained(cls, model_name: str) -> bool:
        entry = cls._registry_entry(model_name)
        if entry:
            return bool(entry.get("self_trained", False))
        return "self_trained" in cls.tags(model_name)

    @classmethod
    def score_for_task(cls, model_name: str, task_tags: List[str]) -> int:
        """按任务标签匹配度打分，越高越适合。"""
        tags = set(cls.tags(model_name))
        return sum(1 for t in task_tags if t in tags)


def protocol_stamp(result: Dict[str, Any], router_dna: str) -> Dict[str, Any]:
    """协议合规烙印：DNA、确认码、审计状态统一加盖。"""
    result.setdefault("router_dna", router_dna)
    result.setdefault("confirm_code", CONFIRM_CODE)
    result.setdefault("sovereignty", "龍魂UID9622")
    if result.get("status") == "ok":
        result.setdefault("audit_status", "green")
    else:
        result.setdefault("audit_status", "red")
    return result


class MultiModelRouter:
    """龍魂 Notion 对话桥多模型协作路由 v2.2。

    支持 provider:
      - local / ollama: 本地 Ollama，包含 longhun-v* 等自训练模型
      - deepseek: DeepSeek API
      - kimi: Moonshot/Kimi API

    策略:
      - auto: 本地优先（自训练模型优先），异常/失败时按健康度降级 cloud
      - local: 仅本地
      - deepseek / kimi: 仅指定 API
      - strict 隐私模式: 强制 local

    新增能力:
      - 熔断器：连续失败触发冷却，避免持续打挂掉的 provider
      - 探测缓存：TTL 缓存 /models 结果，降低延迟
      - 自训练模型识别：longhun-v* / 龍魂-* 自动优先
      - 协议烙印：DNA、确认码、审计状态统一输出
    """

    PROVIDERS = ["local", "deepseek", "kimi"]
    CLOUD_PROVIDERS = ["deepseek", "kimi"]

    def __init__(self):
        self.ollama_host = OLLAMA_HOST
        self.default_model = DEFAULT_MODEL
        self.default_provider = DEFAULT_PROVIDER
        self.privacy = CHAT_PRIVACY
        self.deepseek_key = DEEPSEEK_API_KEY
        self.deepseek_url = DEEPSEEK_BASE_URL
        self.kimi_key = KIMI_API_KEY
        self.kimi_url = KIMI_BASE_URL
        self.circuit = CircuitBreaker(failure_threshold=3, cooldown_seconds=60.0)
        self.probe_cache = ProbeCache(ttl_seconds=30.0)
        self.registry = load_model_registry()
        ModelCapability.set_registry(self.registry)
        self._call_counts: Dict[str, int] = {"local": 0, "deepseek": 0, "kimi": 0}
        self._call_lock = threading.Lock()
        self._multi_executor = ThreadPoolExecutor(max_workers=5, thread_name_prefix="multi_model")

    # ── 注册表增强 ──

    def _registry_model(self, model_id: str) -> Optional[Dict[str, Any]]:
        for m in self.registry.get("models", []):
            if m.get("id", "").lower() == model_id.lower():
                return m
            if model_id.lower().startswith(m.get("id", "").lower() + ":"):
                return m
        return None

    def _enrich_model(self, model_name: str) -> Dict[str, Any]:
        entry = self._registry_model(model_name)
        tags = ModelCapability.tags(model_name)
        return {
            "name": model_name,
            "self_trained": ModelCapability.is_self_trained(model_name),
            "capabilities": tags,
            "preferred_roles": entry.get("preferred_roles", []) if entry else [],
            "display_name": entry.get("name", model_name) if entry else model_name,
            "description": entry.get("description", "") if entry else "",
        }

    def _enrich_probe(self, probe: Any) -> Dict[str, Any]:
        """用 registry 元数据增强 provider 探测结果。"""
        models = probe.get("models", [])
        probe["model_details"] = [self._enrich_model(m) for m in models]
        probe["self_trained_count"] = sum(1 for m in models if ModelCapability.is_self_trained(m))
        probe["registry_dna"] = self.registry.get("registry_dna", "")
        return probe

    # ── 探测 ──

    def _cached_probe(self, name: str, probe_fn) -> Dict[str, Any]:
        cached = self.probe_cache.get(name)
        if cached is not None:
            return cached
        result = probe_fn()
        self.probe_cache.set(name, result)
        return result

    def probe_ollama(self, use_cache: bool = True) -> Dict[str, Any]:
        def _do():
            start = time.time()
            try:
                assert requests is not None  # requests 已安装时非 None
                r = requests.get(f"{self.ollama_host}/api/tags", timeout=5)
                r.raise_for_status()
                data = r.json()
                raw_models = [m.get("name", m.get("model")) for m in data.get("models", [])]
                # 自训练模型排在前面
                models = sorted(
                    raw_models,
                    key=lambda m: (not ModelCapability.is_self_trained(m), m.lower()),
                )
                latency = int((time.time() - start) * 1000)
                return {
                    "name": "Ollama 本地模型",
                    "provider": "local",
                    "status": "online",
                    "latency_ms": latency,
                    "models": models or [self.default_model],
                    "privacy": "local",
                }
            except Exception as e:
                return {
                    "name": "Ollama 本地模型",
                    "provider": "local",
                    "status": "offline",
                    "latency_ms": None,
                    "models": [self.default_model],
                    "privacy": "local",
                    "error": str(e)[:120],
                }
        return self._cached_probe("local", _do) if use_cache else _do()

    def probe_deepseek(self, use_cache: bool = True) -> Dict[str, Any]:
        def _do():
            if not self.deepseek_key:
                return {
                    "name": "DeepSeek API",
                    "provider": "deepseek",
                    "status": "offline",
                    "latency_ms": None,
                    "models": ["deepseek-v4-flash", "deepseek-v4-pro"],
                    "privacy": "cloud",
                    "error": "DEEPSEEK_API_KEY not configured",
                }
            start = time.time()
            try:
                assert requests is not None  # requests 已安装时非 None
                r = requests.get(
                    f"{self.deepseek_url}/models",
                    headers={"Authorization": f"Bearer {self.deepseek_key}"},
                    timeout=8,
                )
                r.raise_for_status()
                data = r.json()
                models = [m.get("id") for m in data.get("data", [])]
                latency = int((time.time() - start) * 1000)
                return {
                    "name": "DeepSeek API",
                    "provider": "deepseek",
                    "status": "online",
                    "latency_ms": latency,
                    "models": models or ["deepseek-v4-flash"],
                    "privacy": "cloud",
                }
            except Exception as e:
                return {
                    "name": "DeepSeek API",
                    "provider": "deepseek",
                    "status": "offline",
                    "latency_ms": None,
                    "models": ["deepseek-v4-flash"],
                    "privacy": "cloud",
                    "error": str(e)[:120],
                }
        return self._cached_probe("deepseek", _do) if use_cache else _do()

    def probe_kimi(self, use_cache: bool = True) -> Dict[str, Any]:
        def _do():
            if not self.kimi_key:
                return {
                    "name": "Kimi API",
                    "provider": "kimi",
                    "status": "offline",
                    "latency_ms": None,
                    "models": ["moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k"],
                    "privacy": "cloud",
                    "error": "KIMI_API_KEY / MOONSHOT_API_KEY not configured",
                }
            start = time.time()
            try:
                assert requests is not None  # requests 已安装时非 None
                r = requests.get(
                    f"{self.kimi_url}/models",
                    headers={"Authorization": f"Bearer {self.kimi_key}"},
                    timeout=8,
                )
                r.raise_for_status()
                data = r.json()
                models = [m.get("id") for m in data.get("data", [])]
                latency = int((time.time() - start) * 1000)
                return {
                    "name": "Kimi API",
                    "provider": "kimi",
                    "status": "online",
                    "latency_ms": latency,
                    "models": models or ["moonshot-v1-8k"],
                    "privacy": "cloud",
                }
            except Exception as e:
                return {
                    "name": "Kimi API",
                    "provider": "kimi",
                    "status": "offline",
                    "latency_ms": None,
                    "models": ["moonshot-v1-8k"],
                    "privacy": "cloud",
                    "error": str(e)[:120],
                }
        return self._cached_probe("kimi", _do) if use_cache else _do()

    def probe_all(self, use_cache: bool = True) -> List[Dict[str, Any]]:
        probes = [
            self.probe_ollama(use_cache=use_cache),
            self.probe_deepseek(use_cache=use_cache),
            self.probe_kimi(use_cache=use_cache),
        ]
        return [self._enrich_probe(p) for p in probes]

    async def probe_all_async(self, use_cache: bool = True) -> List[Dict[str, Any]]:
        """异步并行探测所有 provider，避免阻塞事件循环。"""
        loop = asyncio.get_event_loop()
        probes = await asyncio.gather(
            loop.run_in_executor(None, self.probe_ollama, use_cache),
            loop.run_in_executor(None, self.probe_deepseek, use_cache),
            loop.run_in_executor(None, self.probe_kimi, use_cache),
            return_exceptions=True,
        )
        results = []
        for p in probes:
            if isinstance(p, Exception):
                p = {
                    "name": "探测异常",
                    "provider": "unknown",
                    "status": "offline",
                    "latency_ms": None,
                    "models": [],
                    "privacy": "unknown",
                    "error": str(p)[:120],
                }
            results.append(self._enrich_probe(p))
        return results

    # ── 单 provider 调用 ──

    def _dedupe_bullets(self, texts: List[str], threshold: float = 0.72) -> List[str]:
        """简单去重：Jaccard 相似度高于阈值视为重复。"""
        unique = []
        for t in texts:
            if any(self._bullet_similarity(t, u) > threshold for u in unique):
                continue
            unique.append(t)
        return unique

    def _bullet_similarity(self, a: str, b: str) -> float:
        if not a or not b:
            return 0.0
        sa = set(re.findall(r"[\u4e00-\u9fa5]{2,}", a)) or set(a.split())
        sb = set(re.findall(r"[\u4e00-\u9fa5]{2,}", b)) or set(b.split())
        if not sa or not sb:
            return 0.0
        inter = len(sa & sb)
        union = len(sa | sb)
        jaccard = inter / union if union else 0.0
        len_ratio = min(len(a), len(b)) / max(len(a), len(b)) if max(len(a), len(b)) else 1.0
        return round(jaccard * 0.7 + len_ratio * 0.3, 3)

    def _extract_bullets(self, text: str) -> List[str]:
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        bullets = []
        for line in lines:
            cleaned = re.sub(r"^[\s•\-\*\d\.\)）]+", "", line).strip()
            if cleaned and len(cleaned) > 6:
                bullets.append(cleaned)
        return bullets[:5]

    def generate_multi(
        self,
        messages: List[Dict[str, str]],
        providers: List[str],
        model: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 1024,
    ) -> Dict[str, Any]:
        """多 provider 并行协作：调用每个 provider，汇总各回复并合成综合答案。"""
        if not providers:
            providers = ["local", "deepseek", "kimi"]

        router_dna = generate_dna("MULTI")
        start = time.time()

        def call_one(provider: str) -> Dict[str, Any]:
            try:
                return self._call_provider(provider, messages, model, temperature, max_tokens)
            except Exception as e:
                return {
                    "provider": provider,
                    "model": model or "default",
                    "reply": f"[{provider} 调用失败: {str(e)[:80]}]",
                    "status": "error",
                    "dna": generate_dna(f"MULTI-{provider.upper()}-ERR"),
                    "audit_status": "red",
                }

        futures = {self._multi_executor.submit(call_one, p): p for p in providers}
        per_provider: List[Dict[str, Any]] = []
        for fut in as_completed(futures):
            per_provider.append(fut.result())

        valid = [r for r in per_provider if r.get("status") != "error" and r.get("reply")]
        # 合成：以本地/自训练模型为底，合并其他 provider 新增要点
        base = next((r for r in valid if r.get("provider") == "local"), valid[0] if valid else None)
        base_text = base.get("reply", "") if base else ""
        novel = []
        for r in valid:
            if r is base:
                continue
            for b in self._extract_bullets(r.get("reply", "")):
                novel.append((b, r.get("provider", "?"), r.get("model", "")))
        novel_texts = [t for t, _, _ in novel]
        deduped = self._dedupe_bullets(novel_texts)

        lines = []
        if base_text:
            lines.append(base_text)
        if deduped:
            lines.append("\n💡 多模型补充：")
            for text in deduped[:6]:
                source = next((f"{p}/{m}" for t, p, m in novel if t == text), "?")
                lines.append(f"  • [{source}] {text}")
        synthesis = "\n".join(lines).strip()
        if not synthesis:
            synthesis = "[多模型协作未获得有效回复，请检查模型可用性]"

        any_red = any(r.get("audit_status") == "red" for r in per_provider)
        audit_status = "red" if any_red else ("green" if len(valid) == len(providers) else "yellow")

        total_latency = int((time.time() - start) * 1000)
        result = protocol_envelope({
            "status": "ok" if valid else "error",
            "provider": "multi",
            "model": "multi-collab",
            "reply": synthesis,
            "per_provider_replies": [
                {
                    "provider": r.get("provider"),
                    "model": r.get("model"),
                    "reply": r.get("reply"),
                    "audit_status": r.get("audit_status", "yellow"),
                    "dna": r.get("dna", ""),
                }
                for r in per_provider
            ],
            "total_latency_ms": total_latency,
            "fallback_chain": [{"provider": r.get("provider"), "model": r.get("model"), "reason": r.get("reply", "")[:80]} for r in per_provider if r.get("status") == "error"],
            "mode": "multi",
            "privacy": "normal",
            "strategy": "multi",
        }, router_dna, audit_status=audit_status)
        return ProtocolGuard.guard(result)

    def _chat_ollama(self, messages: List[Dict[str, str]], model: Optional[str], temperature: float, max_tokens: int) -> Dict[str, Any]:
        requested = model or self.default_model
        # 探测可用模型，构建本地候选队列
        probe = self.probe_ollama()
        available = probe.get("models") or []
        candidates = []
        # 1) 用户显式指定的模型最优先
        if requested in available:
            candidates.append(requested)
        # 2) 龍魂自训练模型作为同域协作备选
        for m in sorted(available, key=lambda x: (not ModelCapability.is_self_trained(x), x.lower())):
            if m not in candidates and "embed" not in m.lower():
                candidates.append(m)
        # 3) 其他可用本地模型兜底
        for m in sorted(available, key=lambda x: x.lower()):
            if m not in candidates and "embed" not in m.lower():
                candidates.append(m)
        if not candidates:
            candidates = [requested]

        # 拆分 system / user / assistant
        system_content = ""
        chat_messages = []
        for m in messages:
            if m.get("role") == "system":
                system_content = m.get("content", "")
            else:
                chat_messages.append(m)

        # 兼容 /api/generate（单轮 prompt）
        user_msg = ""
        for m in reversed(chat_messages):
            if m.get("role") == "user":
                user_msg = m.get("content", "")
                break

        tried: List[str] = []
        last_error: Optional[Exception] = None
        for cand in candidates:
            tried.append(cand)
            try:
                assert requests is not None  # requests 已安装时非 None
                dna = generate_dna("LOCAL")
                start = time.time()
                payload = {
                    "model": cand,
                    "prompt": user_msg,
                    "system": system_content or DEFAULT_SYSTEM_PROMPT,
                    "stream": False,
                    "options": {"temperature": temperature, "top_p": 0.8, "num_predict": max_tokens},
                }
                r = requests.post(f"{self.ollama_host}/api/generate", json=payload, timeout=120)
                r.raise_for_status()
                data = r.json()
                reply = data.get("response", "").strip()
                if not reply:
                    last_error = RuntimeError(f"本地模型 {cand} 返回空输出")
                    continue

                # 本地模型质量 gate
                is_gibberish, reason = looks_gibberish(reply)
                if is_gibberish:
                    last_error = RuntimeError(f"本地模型 {cand} 输出乱码 ({reason}): {reply[:80]!r}")
                    continue

                latency = int((time.time() - start) * 1000)
                return {
                    "provider": "local",
                    "model": cand,
                    "reply": reply,
                    "latency_ms": latency,
                    "dna": dna,
                    "privacy": "local",
                    "audit_status": "green",
                }
            except Exception as e:
                last_error = e
                continue

        err_detail = f"已尝试: {', '.join(tried)}"
        raise last_error or RuntimeError(f"无可用本地模型 ({err_detail})")

    def _chat_deepseek(self, messages: List[Dict[str, str]], model: Optional[str], temperature: float, max_tokens: int) -> Dict[str, Any]:
        if not self.deepseek_key:
            raise RuntimeError("DEEPSEEK_API_KEY not configured")
        model = model or "deepseek-v4-flash"
        dna = generate_dna("DEEPSEEK")
        start = time.time()
        assert requests is not None  # requests 已安装时非 None
        r = requests.post(
            f"{self.deepseek_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.deepseek_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
            timeout=120,
        )
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:  # type: ignore[union-attr]  # 运行时 requests 已断言非 None
            if r.status_code == 402:
                raise RuntimeError("DeepSeek 账户余额不足 (402 Payment Required)，请充值后重试") from e
            if r.status_code == 429:
                raise RuntimeError("DeepSeek 请求过于频繁 (429 Too Many Requests)，请稍后再试") from e
            raise
        data = r.json()
        reply = data["choices"][0]["message"]["content"]
        latency = int((time.time() - start) * 1000)
        return {
            "provider": "deepseek",
            "model": data.get("model", model),
            "reply": reply,
            "latency_ms": latency,
            "dna": dna,
            "privacy": "cloud",
            "audit_status": "green",
        }

    def _chat_kimi(self, messages: List[Dict[str, str]], model: Optional[str], temperature: float, max_tokens: int) -> Dict[str, Any]:
        if not self.kimi_key:
            raise RuntimeError("KIMI_API_KEY not configured")
        model = model or "moonshot-v1-8k"
        dna = generate_dna("KIMI")
        start = time.time()
        assert requests is not None  # requests 已安装时非 None
        r = requests.post(
            f"{self.kimi_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.kimi_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
            timeout=120,
        )
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:  # type: ignore[union-attr]  # 运行时 requests 已断言非 None
            if r.status_code == 402:
                raise RuntimeError("Kimi 账户余额不足 (402 Payment Required)，请充值后重试") from e
            if r.status_code == 429:
                raise RuntimeError("Kimi 请求过于频繁或账户额度耗尽 (429)，请稍后再试") from e
            raise
        data = r.json()
        reply = data["choices"][0]["message"]["content"]
        latency = int((time.time() - start) * 1000)
        return {
            "provider": "kimi",
            "model": data.get("model", model),
            "reply": reply,
            "latency_ms": latency,
            "dna": dna,
            "privacy": "cloud",
            "audit_status": "green",
        }

    def _call_provider(self, provider: str, messages: List[Dict[str, str]], model: Optional[str], temperature: float, max_tokens: int) -> Dict[str, Any]:
        if provider == "local" or provider == "ollama":
            return self._chat_ollama(messages, model, temperature, max_tokens)
        if provider == "deepseek":
            return self._chat_deepseek(messages, model, temperature, max_tokens)
        if provider == "kimi":
            return self._chat_kimi(messages, model, temperature, max_tokens)
        raise ValueError(f"未知 provider: {provider}")

    # ── 路由 ──

    def _rank_cloud_providers(self, probes: Dict[str, Dict[str, Any]]) -> List[str]:
        """按在线状态 + 延迟对 cloud provider 排序，熔断的放最后。"""
        scored = []
        for name in self.CLOUD_PROVIDERS:
            if self.circuit.is_open(name):
                scored.append((name, float("inf")))
                continue
            p = probes.get(name, {})
            if p.get("status") != "online":
                scored.append((name, float("inf") - 1))
                continue
            latency = p.get("latency_ms") or 9999
            scored.append((name, latency))
        scored.sort(key=lambda x: x[1])
        return [n for n, _ in scored]

    ROUTE_MODES = {"auto", "local_first", "cloud_first", "cost_first", "privacy"}

    def generate(
        self,
        messages: List[Dict[str, str]],
        provider: Optional[str] = None,
        model: Optional[str] = None,
        privacy: Optional[str] = None,
        mode: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 1024,
    ) -> Dict[str, Any]:
        """统一生成入口，返回带 DNA/审计/熔断/降级的结果。

        mode 策略：
        - auto: 本地自训练模型优先，失败/超时时按健康度降级云端
        - local_first: 仅本地模型；全部失败后才提示是否启用 cloud fallback
        - cloud_first: 跳过本地，直接用健康度最好的云端模型
        - cost_first: 本地优先，其次选择 latency 最低、单价更低的云端 provider
        - privacy: 强制本地，cloud provider 完全禁用
        """
        if requests is None:
            raise RuntimeError("缺少 requests 依赖，请执行 pip install requests")

        provider = (provider or self.default_provider).lower()
        privacy = (privacy or self.privacy).lower()
        mode = (mode or "auto").lower()
        if mode not in self.ROUTE_MODES:
            mode = "auto"

        # privacy 模式强制本地
        if privacy == "strict" or mode == "privacy":
            provider = "local"
            privacy = "strict"
            mode = "privacy"

        if provider not in ("auto", "local", "deepseek", "kimi"):
            raise ValueError(f"provider '{provider}' 不支持")

        # 确定尝试顺序
        probes = {p["provider"]: p for p in self.probe_all()}
        if mode == "cloud_first":
            order = self._rank_cloud_providers(probes)
            if not order:
                order = [provider] if provider != "auto" else ["kimi"]
        elif mode == "local_first":
            order = ["local"]
        elif mode == "cost_first" or provider == "auto":
            order = ["local"]
            if privacy != "strict":
                order.extend(self._rank_cloud_providers(probes))
        else:
            order = [provider]

        router_dna = generate_dna("ROUTER")
        start = time.time()
        errors = []
        fallback_chain = []

        for name in order:
            status = probes.get(name, {})
            if status.get("status") != "online":
                reason = status.get("error", "not online")
                errors.append(f"{name}: {reason}")
                fallback_chain.append({"provider": name, "model": model or "default", "reason": reason})
                continue
            if self.circuit.is_open(name):
                errors.append(f"{name}: circuit breaker open")
                fallback_chain.append({"provider": name, "model": model or "default", "reason": "circuit breaker open"})
                continue
            try:
                with self._call_lock:
                    self._call_counts[name] = self._call_counts.get(name, 0) + 1
                result = self._call_provider(name, messages, model, temperature, max_tokens)
                # 协议烙印
                result = protocol_envelope(result, router_dna)
                result["total_latency_ms"] = int((time.time() - start) * 1000)
                result["strategy"] = provider
                result["mode"] = mode
                result["privacy"] = privacy
                result["fallback_chain"] = fallback_chain
                # 简短审计：输出若触发乱码也降级
                is_gibberish, reason = looks_gibberish(result.get("reply", ""))
                if is_gibberish:
                    self.circuit.record_failure(name)
                    errors.append(f"{name}: gibberish ({reason})")
                    fallback_chain.append({"provider": name, "model": result["model"], "reason": f"gibberish:{reason}"})
                    continue
                # P0 协议守卫
                result = ProtocolGuard.guard(result)
                self.circuit.record_success(name)
                return result
            except Exception as e:
                self.circuit.record_failure(name)
                err_msg = f"{name}: {str(e)[:120]}"
                errors.append(err_msg)
                fallback_chain.append({"provider": name, "model": model or "default", "reason": str(e)[:120]})

        # 全部失败
        reply = "[所有可用模型均调用失败]"
        if mode == "local_first":
            reply += "\n\n💡 当前为「本地优先」模式，所有本地模型均不可用。如需启用云端 fallback，请切换到 auto / cost_first 模式。"
        elif mode == "privacy":
            reply += "\n\n🔒 当前为「隐私优先」模式，仅允许本地模型。请检查 Ollama 是否运行。"
        return protocol_envelope({
            "status": "error",
            "provider": "",
            "model": model or "",
            "reply": reply,
            "total_latency_ms": int((time.time() - start) * 1000),
            "strategy": provider,
            "mode": mode,
            "privacy": privacy,
            "fallback_chain": fallback_chain,
            "errors": errors,
        }, router_dna)

    def health(self) -> Dict[str, Any]:
        """返回路由健康状态（含熔断器、探测缓存、调用计数）。"""
        return {
            "dna": generate_dna("HEALTH"),
            "timestamp": _now(),
            "circuit_breaker": self.circuit.status(),
            "call_counts": dict(self._call_counts),
            "providers": self.probe_all(),
        }

    async def health_async(self) -> Dict[str, Any]:
        """异步返回路由健康状态。"""
        return {
            "dna": generate_dna("HEALTH"),
            "timestamp": _now(),
            "circuit_breaker": self.circuit.status(),
            "call_counts": dict(self._call_counts),
            "providers": await self.probe_all_async(),
        }


# 全局路由实例
model_router = MultiModelRouter()

# 全局五行议事会实例
wuxing_council: Any = WuxingModelCouncil(model_router) if COUNCIL_AVAILABLE else None


def model_generate(
    prompt: str,
    provider: Optional[str] = None,
    model: Optional[str] = None,
    privacy: Optional[str] = None,
    mode: Optional[str] = None,
    system: Optional[str] = None,
) -> Dict[str, Any]:
    """单轮问答便捷入口，返回统一结构。"""
    messages = [
        {"role": "system", "content": system or DEFAULT_SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    return model_router.generate(messages, provider=provider, model=model, privacy=privacy, mode=mode)


def rag_generate(
    query: str,
    sources: List[Dict],
    provider: Optional[str] = None,
    model: Optional[str] = None,
    privacy: Optional[str] = None,
    mode: Optional[str] = None,
) -> Dict[str, Any]:
    """RAG: 基于检索结果生成回答，返回统一结构。"""
    if not sources:
        system = (
            "你是一位严谨、简洁的中文助手。"
            "请用通顺、完整的中文句子回答用户问题。"
            "不要输出无意义的符号、乱码、重复片段或夹杂着 UID/确认码的碎片。"
            "如果问题超出你的知识范围，请直接说明。"
        )
        return model_generate(query, provider=provider, model=model, privacy=privacy, mode=mode, system=system)

    context = "\n\n".join([
        f"[来源 {i+1}: {s.get('title', '未命名')}]\n{s.get('content', s.get('text', ''))[:600]}"
        for i, s in enumerate(sources[:5])
    ])
    user_prompt = f"""请根据以下参考资料回答问题。如果资料无法回答，请明确说明"根据现有资料无法回答"。

参考资料：
{context}

问题：{query}

要求：
1. 使用通顺、完整的中文。
2. 不要编造资料中没有的信息。
3. 回答简洁，控制在 300 字以内。
4. 不要输出无意义符号、UID、确认码或乱码。

回答："""

    system = (
        "你是一位严谨、简洁的中文助手。"
        "请基于提供的参考资料用通顺中文回答。"
        "不要编造资料外的信息，不要输出无意义符号或乱码。"
    )
    return model_generate(user_prompt, provider=provider, model=model, privacy=privacy, mode=mode, system=system)

# ============================================================
# 导航意图识别（v2.2新增）
# ============================================================

NAVIGATION_PATTERNS = [
    (r"导航到[「「]?(.+?)[」」]?", "navigation"),
    (r"打开[「「]?(.+?)[」」]?(?:页面)?", "navigation"),
    (r"跳转到[「「]?(.+?)[」」]?", "navigation"),
    (r"查看[「「]?(.+?)[」」]?(?:页面|内容)", "navigation"),
    (r"关联[「「]?(.+?)[」」]?和[「「]?(.+?)[」」]?", "link"),
    (r"把[「「]?(.+?)[」」]?和[「「]?(.+?)[」」]?关联", "link"),
    (r"推荐.*?关联.*?[「「]?(.+?)[」」]?", "recommend"),
]

def detect_navigation_intent(message: str) -> Optional[Dict]:
    """检测导航/关联意图，返回 {type, target, target2} 或 None"""
    for pattern, intent_type in NAVIGATION_PATTERNS:
        match = re.search(pattern, message)
        if match:
            if intent_type == "link" and (match.lastindex or 0) >= 2:
                return {"type": "link", "target": match.group(1).strip(), "target2": match.group(2).strip()}
            return {"type": intent_type, "target": match.group(1).strip()}
    return None

# ============================================================
# 人格引擎对话处理器
# ============================================================

def process_chat_with_persona(message: str, session_id: str,
                              use_persona: bool, client: NotionClient,
                              provider: Optional[str] = None,
                              model: Optional[str] = None,
                              privacy: Optional[str] = None,
                              mode: Optional[str] = None) -> Dict:
    """带人格引擎 + 导航 + 多模型协作的对话处理"""
    result = {
        "message": message,
        "session_id": session_id,
        "persona": None,
        "persona_applied": None,
        "chain": None,
        "response": "",
        "sources": [],
        "navigation": None,
        "model_provider": "",
        "model_name": "",
        "model_dna": "",
        "fallback_chain": [],
        "audit_status": "",
    }

    # 0. 导航意图优先检测
    nav_intent = detect_navigation_intent(message)
    if nav_intent:
        nav_type = nav_intent["type"]
        target = nav_intent["target"]

        if nav_type == "navigation":
            pages = search_remote(client, target, limit=10)
            # 也尝试本地搜索
            local_pages = search_local(target, limit=5)
            seen_ids = {p.get("id", "") for p in pages}
            for lp in local_pages:
                if lp.get("id", "") not in seen_ids:
                    pages.append(lp)
            result["navigation"] = {"type": "navigation", "target": target, "pages": pages}
            if pages:
                titles = [p.get("title", "?") for p in pages[:5]]
                result["response"] = f"🔗 找到 {len(pages)} 个与「{target}」相关的页面:\n" + \
                    "\n".join([f"  • {t}" for t in titles])
            else:
                result["response"] = f"🔍 未找到与「{target}」相关的页面"
            return result

        elif nav_type == "link":
            target2 = nav_intent.get("target2", "")
            result["navigation"] = {"type": "link", "target": target, "target2": target2}
            result["response"] = f"🔗 检测到关联意图: 「{target}」↔「{target2}」\n" + \
                f"💡 请提供两个页面的 ID，执行: lh notion-link create --page1 <id> --page2 <id>"
            return result

        elif nav_type == "recommend":
            result["navigation"] = {"type": "recommend", "target": target}
            result["response"] = f"💡 检测到推荐意图: 为「{target}」查找关联页面\n" + \
                f"💡 执行: lh notion-link recommend --page <id>"
            return result

    def _apply_model_result(target: Dict, mr: Dict[str, Any]) -> str:
        """将模型路由结果合并到返回体，并返回最终 response 字符串。"""
        target["model_provider"] = mr.get("provider", "")
        target["model_name"] = mr.get("model", "")
        target["model_dna"] = mr.get("dna", "")
        target["mode"] = mr.get("mode", "")
        target["fallback_chain"] = mr.get("fallback_chain", [])
        target["audit_status"] = mr.get("audit_status", "yellow" if mr.get("status") != "ok" else "green")
        return mr.get("reply", "") if mr.get("status") == "ok" else (mr.get("reply") or "[模型调用失败]")

    if not PERSONA_AVAILABLE or not use_persona:
        # 直接搜索 + RAG（无资料时也调用模型基于通用知识回答）
        sources = search_hybrid(client, message, limit=8)
        result["sources"] = sources
        mr = rag_generate(message, sources, provider=provider, model=model, privacy=privacy, mode=mode)
        result["response"] = _apply_model_result(result, mr)
        return result

    try:
        persona_runtime: Any = PersonaRuntime()
        persona_bridge: Any = PersonaBridge(persona_runtime)
    except Exception:
        sources = search_hybrid(client, message, limit=8)
        result["sources"] = sources
        mr = rag_generate(message, sources, provider=provider, model=model, privacy=privacy, mode=mode)
        result["response"] = _apply_model_result(result, mr)
        return result

    # 1. 人格路由
    persona_result = persona_bridge.handle(session_id, message)
    result["persona"] = persona_result

    # 2. 获取当前人格
    current_persona = persona_runtime.get_current(session_id)

    # 3. 构建搜索查询（加入人格描述增强相关性）
    search_query = message
    if current_persona:
        expertise = current_persona.get("one_liner", "")
        if expertise:
            search_query = f"{message} {expertise}"
        result["persona_applied"] = f"{current_persona.get('name', '')} ({current_persona.get('ipa', '')})"

    # 4. 搜索 + RAG
    sources = search_hybrid(client, search_query, limit=10)
    result["sources"] = sources

    mr = rag_generate(search_query, sources, provider=provider, model=model, privacy=privacy, mode=mode)
    response = _apply_model_result(result, mr)
    if current_persona:
        response = f"🧠 **{current_persona.get('name', '')}**:\n{response}"
    result["response"] = response

    # 5. 联动链路检查
    persona_type = persona_result.get("type", "") if persona_result else ""
    if persona_type == "persona_chain" and persona_result:
        chain_data = persona_result.get("chain", {})
        chain_list = chain_data.get("chain", [])
        if chain_list:
            result["chain"] = [{"ipa": c.get("ipa", ""), "name": c.get("name", "")} for c in chain_list]
            # 更新会话上下文
            context = json.dumps({"last_chain": [c.get("name", "") for c in chain_list]})
            update_session_persona(session_id, current_persona.get("ipa", "") if current_persona else "", context)

    # 6. 保存聊天记录
    save_chat(
        session_id, message, response,
        current_persona.get("ipa", "") if current_persona else "",
        current_persona.get("name", "") if current_persona else "",
        json.dumps(persona_result, ensure_ascii=False) if persona_result else "",
        model_provider=result.get("model_provider", ""),
        model_name=result.get("model_name", ""),
        model_dna=result.get("model_dna", ""),
        audit_status=result.get("audit_status", ""),
    )

    return result

# ============================================================
# 初始化
# ============================================================

init_sync_db()
init_chat_db()

persona_runtime: Any
persona_bridge: Any
if PERSONA_AVAILABLE:
    persona_runtime = PersonaRuntime()
    persona_bridge = PersonaBridge(persona_runtime)
else:
    persona_runtime = None
    persona_bridge = None

# ============================================================
# FastAPI 应用
# ============================================================

@asynccontextmanager
async def lifespan(_app: FastAPI):
    print("\n🐉 龍魂 · Notion 对话桥 v2.2")
    if PERSONA_AVAILABLE:
        print(f"🧠 人格引擎已加载 · {len(persona_runtime.list_personas())} 个人格")
    else:
        print("⚠️ 人格引擎不可用")
    print(f"🔑 确认码: {CONFIRM_CODE}")
    yield
    print("🛑 对话桥已关闭")

app = FastAPI(
    title="龍魂 · Notion 对话桥",
    description="自然语言对话 Notion + 人格矩阵深度集成 + RAG多模型协作（本地/自训练/DeepSeek/Kimi）",
    version="2.3",
    lifespan=lifespan
)


@app.middleware("http")
async def protocol_envelope_middleware(request: Request, call_next):
    """为所有 /api/* 成功 JSON 响应自动加盖协议信封；避免重复包装。"""
    response = await call_next(request)
    path = request.url.path
    if not path.startswith("/api/"):
        return response
    if response.status_code < 200 or response.status_code >= 300:
        return response
    if not hasattr(response, "body"):
        return response
    try:
        body = response.body
        if not body:
            return response
        data = json.loads(body.decode("utf-8"))
        # 避免重复包装
        if data.get("protocol_version") == PROTOCOL_VERSION and "confirm_code" in data:
            return response
        wrapped = protocol_envelope(data, generate_dna("HTTP-" + path.replace("/", "-")))
        return JSONResponse(wrapped, status_code=response.status_code, headers=dict(response.headers))
    except Exception:
        # 解析失败时不破坏原始响应
        return response


# CORS：公网部署默认收紧，只允许同源、主要域名与 localhost 开发。
# 如需额外来源，设置环境变量 ALLOWED_ORIGINS=origin1,origin2
_default_origins = {
    "http://localhost:8779",
    "http://127.0.0.1:8779",
    "https://uid9622.cn",
    "https://www.uid9622.cn",
    "https://longhun888.com",
    "https://www.longhun888.com",
}
_extra = os.environ.get("ALLOWED_ORIGINS", "")
if _extra:
    _default_origins.update({o.strip() for o in _extra.split(",") if o.strip()})

app.add_middleware(
    CORSMiddleware,
    allow_origins=sorted(_default_origins),
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
    allow_credentials=True,
)

# 静态资源：Web 面板 JS/CSS
app.mount("/static", StaticFiles(directory=str(PROJECT_ROOT / "web" / "static")), name="static")

notion_client = NotionClient()

# ============================================================
# API 端点
# ============================================================

@app.get("/health")
async def health():
    providers = await model_router.probe_all_async()
    online = [p["provider"] for p in providers if p.get("status") == "online"]
    return {
        "status": "ok",
        "version": "2.3",
        "persona": PERSONA_AVAILABLE,
        "council": COUNCIL_AVAILABLE,
        "persona_count": len(persona_runtime.list_personas()) if PERSONA_AVAILABLE else 0,
        "confirm_code": CONFIRM_CODE,
        "models": {
            "default_provider": DEFAULT_PROVIDER,
            "privacy": CHAT_PRIVACY,
            "online_providers": online,
            "providers": providers,
        },
        "router_health": {
            "circuit_breaker": model_router.circuit.status(),
            "call_counts": dict(model_router._call_counts),
        },
        "bagua": wuxing_council.bagua.info("default") if COUNCIL_AVAILABLE and wuxing_council else None,
    }

@app.get("/api/models")
async def list_models():
    """列出所有可用模型及 provider 状态"""
    providers = await model_router.probe_all_async()
    return {
        "dna": generate_dna("MODELS"),
        "timestamp": _now(),
        "default_provider": DEFAULT_PROVIDER,
        "privacy": CHAT_PRIVACY,
        "providers": providers,
        "capabilities": {
            model: ModelCapability.tags(model)
            for p in providers
            for model in p.get("models", [])
        },
    }

@app.get("/api/router/health")
async def router_health():
    """多模型路由健康详情（熔断器、缓存、调用计数）"""
    return await model_router.health_async()

def _build_chat_messages(session_id: str, message: str) -> List[Dict[str, str]]:
    """从历史构建 LLM messages。"""
    history = get_chat_history(session_id, limit=10)
    messages = []
    for h in reversed(history):
        if h.get("message"):
            messages.append({"role": "user", "content": h["message"]})
        if h.get("response"):
            messages.append({"role": "assistant", "content": h["response"]})
    messages.append({"role": "user", "content": message})
    return messages


def _build_system_prefix(session_id: str, message: str, use_persona: bool, sources: List[Dict]) -> str:
    """构建 system 前缀（人格 + RAG 资料）。"""
    source_text = ""
    if sources:
        source_text = "参考资料：\n" + "\n\n".join(
            f"[{i+1}] {s.get('title', '未命名')}\n{s.get('content', '')[:400]}"
            for i, s in enumerate(sources)
        )

    persona_prefix = ""
    if PERSONA_AVAILABLE and use_persona:
        try:
            pr: Any = PersonaRuntime()
            pb: Any = PersonaBridge(pr)
            pb.handle(session_id, message)
            current_persona = pr.get_current(session_id)
            if current_persona:
                persona_prefix = f"当前人格：{current_persona.get('name', '')}（{current_persona.get('ipa', '')}）。{current_persona.get('one_liner', '')}"
        except Exception:
            pass

    parts = []
    if persona_prefix:
        parts.append(persona_prefix)
    if source_text:
        parts.append(source_text)
    return "\n".join(parts)


def _save_council_chat(session_id: str, message: str, council_result: Dict[str, Any]):
    """保存 council 结果到聊天记录。"""
    save_chat(
        session_id, message, council_result.get("reply", ""),
        model_provider=council_result.get("provider", "council"),
        model_name=council_result.get("model", "wuxing-council-v1.0"),
        model_dna=council_result.get("dna", ""),
        audit_status=council_result.get("audit_status", "yellow"),
        council_members=json.dumps(council_result.get("council_members", []), ensure_ascii=False),
        bagua_state=json.dumps(council_result.get("bagua_state", {}), ensure_ascii=False),
        synthesis_log=json.dumps(council_result.get("synthesis_log", {}), ensure_ascii=False),
        consensus_score=council_result.get("consensus_score", 0.0),
    )


async def _run_council_chat(data: Dict[str, Any]) -> Dict[str, Any]:
    """执行五行议事会对话并返回协议信封。"""
    message = data["message"]
    session_id = data.get("session_id", "default")
    use_persona = data.get("use_persona", True)
    temperature = data.get("temperature", 0.35)
    max_tokens = data.get("max_tokens", 512)

    if not COUNCIL_AVAILABLE or wuxing_council is None:
        raise HTTPException(status_code=503, detail="五行议事会未加载")

    messages = _build_chat_messages(session_id, message)
    sources = search_hybrid(notion_client, message, limit=6)
    system_prefix = _build_system_prefix(session_id, message, use_persona, sources)

    council_result = wuxing_council.chat(
        session_id=session_id,
        message=message,
        messages=messages,
        sources=sources,
        system_prefix=system_prefix,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    council_result = ProtocolGuard.guard(council_result)
    _save_council_chat(session_id, message, council_result)
    return protocol_envelope(council_result, generate_dna("COUNCIL-API"))


async def _run_multi_chat(data: Dict[str, Any]) -> Dict[str, Any]:
    """执行多 provider 并行协作并返回协议信封。"""
    message = data["message"]
    session_id = data.get("session_id", "default")
    providers = data.get("providers", ["local", "deepseek", "kimi"])
    if isinstance(providers, str):
        providers = [p.strip() for p in providers.split(",") if p.strip()]
    model = data.get("model")
    temperature = data.get("temperature", 0.3)
    max_tokens = data.get("max_tokens", 1024)

    messages = _build_chat_messages(session_id, message)
    sources = search_hybrid(notion_client, message, limit=6)
    system_prefix = _build_system_prefix(session_id, message, data.get("use_persona", True), sources)

    if system_prefix:
        # 将 system_prefix 作为 system message 前置
        messages = [{"role": "system", "content": system_prefix}] + messages

    result = model_router.generate_multi(
        messages,
        providers=providers,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    save_chat(
        session_id, message, result.get("reply", ""),
        model_provider=result.get("model_provider", "multi"),
        model_name=result.get("model_name", "multi-collab"),
        model_dna=result.get("model_dna", ""),
        audit_status=result.get("audit_status", "yellow"),
    )
    return protocol_envelope(result, generate_dna("MULTI-API"))


@app.post("/api/chat")
async def api_chat(request: Request):
    """对话端点（含人格引擎 + RAG + 单模型/议事会/多模型协作）"""
    try:
        data = await request.json()
    except:
        raise HTTPException(status_code=400, detail="请求体需为 JSON")

    message = data.get("message", "").strip()
    if not message:
        raise HTTPException(status_code=400, detail="消息不能为空")

    data["message"] = message
    mode = data.get("mode", "single")

    if mode == "council":
        result = await _run_council_chat(data)
    elif mode == "multi":
        result = await _run_multi_chat(data)
    else:
        # single / 默认：保持原有行为
        session_id = data.get("session_id", "default")
        use_persona = data.get("use_persona", True)
        provider = data.get("provider") or DEFAULT_PROVIDER
        model = data.get("model")
        privacy = data.get("privacy") or CHAT_PRIVACY
        route_mode = data.get("route_mode") or data.get("mode") or None

        result = process_chat_with_persona(
            message, session_id, use_persona, notion_client,
            provider=provider, model=model, privacy=privacy, mode=route_mode
        )
        result = protocol_envelope(result, generate_dna("CHAT-API"))

    return JSONResponse(result)

@app.post("/api/chat/council")
async def api_chat_council(request: Request):
    """五行议事会对话端点（多模型协作 + 八卦状态 + 三色审计）"""
    try:
        data = await request.json()
    except:
        raise HTTPException(status_code=400, detail="请求体需为 JSON")

    message = data.get("message", "").strip()
    if not message:
        raise HTTPException(status_code=400, detail="消息不能为空")

    data["message"] = message
    result = await _run_council_chat(data)
    return JSONResponse(result)

@app.get("/api/council/status")
async def api_council_status():
    """五行议事会当前委员状态"""
    if not COUNCIL_AVAILABLE or wuxing_council is None:
        raise HTTPException(status_code=503, detail="五行议事会未加载")
    return JSONResponse(wuxing_council.status())

@app.get("/api/bagua/state")
async def api_bagua_state(session_id: str = "default"):
    """当前会话八卦状态"""
    if not COUNCIL_AVAILABLE or wuxing_council is None:
        raise HTTPException(status_code=503, detail="五行议事会未加载")
    return JSONResponse(wuxing_council.bagua.info(session_id))

@app.post("/api/search")
async def api_search(request: Request):
    """搜索端点（混合搜索）"""
    try:
        data = await request.json()
    except:
        raise HTTPException(status_code=400, detail="请求体需为 JSON")

    query = data.get("query", "").strip()
    limit = data.get("limit", 10)

    if not query:
        raise HTTPException(status_code=400, detail="查询不能为空")

    results = search_hybrid(notion_client, query, limit)
    return JSONResponse({"query": query, "results": results, "count": len(results)})

@app.get("/api/persona/current")
async def get_current_persona(session_id: str = "default"):
    """获取当前会话的人格"""
    if not PERSONA_AVAILABLE:
        raise HTTPException(status_code=503, detail="人格引擎不可用")
    p = persona_runtime.get_current(session_id)
    if p:
        return {"persona": {
            "ipa": p.get("ipa", ""),
            "name": p.get("name", ""),
            "layer": p.get("layer", ""),
            "one_liner": p.get("one_liner", ""),
            "trigger_words": p.get("trigger_words", ""),
            "relations": p.get("linked_personas", ""),
        }}
    return {"persona": None}

@app.post("/api/persona/switch")
async def switch_persona(request: Request):
    """切换人格"""
    if not PERSONA_AVAILABLE:
        raise HTTPException(status_code=503, detail="人格引擎不可用")
    try:
        data = await request.json()
    except:
        raise HTTPException(status_code=400, detail="请求体需为 JSON")

    ipa = data.get("ipa", "")
    session_id = data.get("session_id", "default")

    if not ipa:
        # 尝试按名称匹配
        name = data.get("name", "")
        if name:
            personas = persona_runtime.list_personas()
            for p in personas:
                if name in p.get("name", ""):
                    ipa = p.get("ipa", "")
                    break
        if not ipa:
            raise HTTPException(status_code=400, detail="请提供人格 IPA 或名称")

    result = persona_runtime.set_current(session_id, ipa)
    if result.get("status") == "success":
        p = result.get("persona", {})
        update_session_persona(session_id, p.get("ipa", ""), "")
        return result
    raise HTTPException(status_code=404, detail=result.get("message", "切换失败"))

@app.get("/api/persona/list")
async def list_personas():
    """列出所有人格"""
    if not PERSONA_AVAILABLE:
        raise HTTPException(status_code=503, detail="人格引擎不可用")
    personas = persona_runtime.list_personas()
    # 精简字段
    simple = [{
        "ipa": p.get("ipa", ""),
        "name": p.get("name", ""),
        "layer": p.get("layer", ""),
        "hexagram": p.get("hexagram", ""),
        "group_name": p.get("group_name", ""),
        "weight": p.get("weight", 0),
        "trigger_words": p.get("trigger_words", ""),
        "one_liner": p.get("one_liner", ""),
        "linked_personas": p.get("linked_personas", ""),
    } for p in personas]
    return {"personas": simple, "count": len(simple)}

@app.post("/api/persona/chain")
async def trigger_chain(request: Request):
    """触发联动链路"""
    if not PERSONA_AVAILABLE:
        raise HTTPException(status_code=503, detail="人格引擎不可用")
    try:
        data = await request.json()
    except:
        raise HTTPException(status_code=400, detail="请求体需为 JSON")

    ipa = data.get("ipa", "")
    intent = data.get("intent", "处理")
    session_id = data.get("session_id", "default")

    if not ipa:
        raise HTTPException(status_code=400, detail="请提供人格 IPA")

    result = persona_runtime.trigger_chain(session_id, ipa, intent)
    if result.get("status") == "success":
        return result
    raise HTTPException(status_code=404, detail=result.get("message", "联动失败"))

@app.post("/api/persona/match")
async def match_persona(request: Request):
    """按文本匹配最佳人格"""
    if not PERSONA_AVAILABLE:
        raise HTTPException(status_code=503, detail="人格引擎不可用")
    try:
        data = await request.json()
    except:
        raise HTTPException(status_code=400, detail="请求体需为 JSON")

    text = data.get("text", "")
    top_k = data.get("top_k", 3)

    if not text:
        raise HTTPException(status_code=400, detail="文本不能为空")

    matched = persona_bridge.match(text, top_k=top_k)
    return {"text": text, "matched": matched, "count": len(matched)}

@app.get("/api/history")
async def get_history(session_id: str = "default", limit: int = 20):
    """获取聊天历史"""
    history = get_chat_history(session_id, limit)
    return {"session_id": session_id, "history": history, "count": len(history)}

@app.get("/api/stats")
async def get_stats():
    """数据库统计"""
    conn = sqlite3.connect(str(SYNC_DB))
    page_count = conn.execute("SELECT COUNT(*) FROM pages").fetchone()[0]
    block_count = conn.execute("SELECT COUNT(*) FROM blocks").fetchone()[0]
    sync_count = conn.execute("SELECT COUNT(*) FROM sync_log").fetchone()[0]
    conn.close()

    conn2 = sqlite3.connect(str(CHAT_HISTORY_DB))
    chat_count = conn2.execute("SELECT COUNT(*) FROM chat_history").fetchone()[0]
    session_count = conn2.execute("SELECT COUNT(*) FROM chat_sessions").fetchone()[0]
    conn2.close()

    return {
        "pages": page_count,
        "blocks": block_count,
        "sync_logs": sync_count,
        "chat_messages": chat_count,
        "sessions": session_count,
        "persona_count": len(persona_runtime.list_personas()) if PERSONA_AVAILABLE else 0,
    }

# ============================================================
# 终端执行 API（安全沙箱）
# ============================================================

SAFE_COMMANDS = {
    "ls", "cat", "head", "tail", "wc", "grep", "find", "echo", "pwd", "cd",
    "python3", "python", "ollama", "lh", "git", "ps", "top", "df", "du",
    "free", "uptime", "uname", "whoami", "id", "env", "printenv",
    "curl", "wget", "pgrep", "pkill", "netstat", "ss", "lsof",
    "systemctl", "journalctl", "docker", "which", "whereis", "file",
    "stat", "tree", "diff", "sort", "uniq", "cut", "awk", "sed",
    "xargs", "tee", "date", "cal", "nproc", "hostname", "ip", "ifconfig",
    "nslookup", "dig", "ping", "traceroute", "htop", "btm",
}

BLOCKED_PATTERNS = [
    # 破坏性命令
    r"rm\s+-rf", r"\brm\s+/(?!\w)", r"mkfs", r"dd\s+if=",
    r":\(\)\s*\{", r"chmod\s+777", r"chown\s+-R", r"sudo\b",
    r"\bshutdown\b", r"\breboot\b", r"\bhalt\b", r"\bpoweroff\b",
    r"\binit\s+0\b", r"\binit\s+6\b",
    # 敏感目录
    r"\.ssh", r"\.gnupg", r"\.git/config",
    # 网络下载到系统目录
    r"wget\s+-O\s+/", r"curl.*-o\s+/",
    # 危险重定向（到 /dev 以外或项目外的绝对路径）
    r"[>]{1,2}\s*/(?!dev/)",
    # 子 shell / 后台 / 远程执行
    r"\$\(", r"`", r"\|\s*bash", r"\|\s*sh\b", r"\|\s*python",
    r"\bnc\b", r"\bnetcat\b", r"\bncat\b",
]


def _resolve_work_dir(cwd: Optional[str]) -> str:
    """把请求中的 cwd 解析为项目根下的绝对路径。"""
    root = os.path.abspath(str(PROJECT_ROOT))
    if cwd:
        target = os.path.abspath(os.path.join(root, cwd))
        # 必须位于项目根内部（允许相等）
        if target == root or target.startswith(root + os.sep):
            if os.path.isdir(target):
                return target
    return root


def is_command_safe(cmd: str, work_dir: str) -> tuple:
    """安全检查：返回 (is_safe, reason)

    规则：
    1. 命中 BLOCKED_PATTERNS 直接拒绝；
    2. 首命令必须在白名单，或是以 ./ 开头的项目内脚本；
    3. 禁止通过 .. 或绝对路径逃逸出项目根目录；
    4. 禁止写入项目根目录外的文件（> /xxx）。
    """
    cmd_lower = cmd.strip().lower()
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, cmd_lower):
            return False, f"🚫 命令包含被禁止的模式: {pattern}"

    # 拆分管道，检查每一段的首命令
    segments = [s.strip() for s in cmd.split("|")]
    for seg in segments:
        if not seg:
            continue
        first = seg.split()[0]
        if first.startswith("./") or first.startswith("../"):
            continue
        if first and first not in SAFE_COMMANDS:
            return False, f"🚫 不允许执行命令: {first}（不在安全白名单中）"

    # 检查目录遍历：只允许在项目根内
    root = os.path.abspath(str(PROJECT_ROOT))
    for token in cmd.split():
        if token.startswith("/"):
            # 绝对路径必须位于项目根内
            abs_t = os.path.abspath(token)
            if abs_t != root and not abs_t.startswith(root + os.sep):
                return False, f"🚫 路径越界: {token}（超出项目目录）"
        if ".." in token:
            # 尝试解析相对路径
            abs_t = os.path.abspath(os.path.join(work_dir, token))
            if abs_t != root and not abs_t.startswith(root + os.sep):
                return False, f"🚫 路径越界: {token}（超出项目目录）"

    return True, "ok"

@app.get("/api/terminal/exec")
async def terminal_exec(cmd: str = Query(""), cwd: str = Query(None), timeout: int = Query(30)):
    """安全执行终端命令（异步子进程，不阻塞事件循环）"""
    if not cmd.strip():
        return {"ok": False, "output": "请输入命令", "cwd": str(PROJECT_ROOT)}

    work_dir = _resolve_work_dir(cwd)
    cmd_stripped = cmd.strip()

    # 处理 cd 命令：不启动子进程，直接计算并校验目标目录
    if cmd_stripped.startswith("cd ") or cmd_stripped == "cd":
        arg = cmd_stripped[2:].strip() or "."
        target = os.path.abspath(os.path.join(work_dir, arg))
        root = os.path.abspath(str(PROJECT_ROOT))
        if target != root and not target.startswith(root + os.sep):
            return {"ok": False, "output": f"🚫 目录越界: {arg}", "cwd": work_dir}
        if not os.path.isdir(target):
            return {"ok": False, "output": f"❌ 目录不存在: {arg}", "cwd": work_dir}
        return {"ok": True, "output": "", "cwd": target, "exit_code": 0}

    safe, reason = is_command_safe(cmd_stripped, work_dir)
    if not safe:
        return {"ok": False, "output": reason, "cwd": work_dir}

    try:
        proc = await asyncio.wait_for(
            asyncio.create_subprocess_shell(
                cmd_stripped,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=work_dir,
                env={**os.environ, "TERM": "xterm-256color"},
            ),
            timeout=timeout,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        output = stdout.decode("utf-8", errors="replace")
        if stderr:
            output += f"\n\x1b[33m[stderr]\x1b[0m\n{stderr.decode('utf-8', errors='replace')}"
        if not output.strip():
            output = f"(退出码: {proc.returncode})"
        return {"ok": proc.returncode == 0, "output": output, "cwd": work_dir, "exit_code": proc.returncode}
    except asyncio.TimeoutError:
        return {"ok": False, "output": f"⏰ 命令超时 ({timeout}s)", "cwd": work_dir}
    except Exception as e:
        return {"ok": False, "output": f"❌ 执行错误: {e}", "cwd": work_dir}

@app.get("/api/terminal/cwd")
async def terminal_cwd(path: str = Query(None)):
    """获取/切换工作目录"""
    target = path if path and os.path.isdir(path) else str(PROJECT_ROOT)
    try:
        listing = os.listdir(target)
        dirs = sorted([f"{d}/" for d in listing if os.path.isdir(os.path.join(target, d))])[:30]
        files = sorted([f for f in listing if os.path.isfile(os.path.join(target, f))])[:30]
        return {"ok": True, "cwd": os.path.abspath(target), "dirs": dirs, "files": files}
    except PermissionError:
        return {"ok": False, "cwd": target, "error": "权限不足"}

# ============================================================
# 模型管理 API
# ============================================================

@app.get("/api/models/ollama")
async def list_ollama_models():
    """列出所有 Ollama 模型"""
    try:
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, timeout=10
        )
        models = []
        for line in result.stdout.strip().split("\n")[1:]:  # skip header
            parts = line.split()
            if len(parts) >= 4:
                models.append({
                    "name": parts[0],
                    "id": parts[1][:12],
                    "size": " ".join(parts[2:-2]) if len(parts) > 4 else parts[2],
                    "modified": " ".join(parts[-2:]) if len(parts) > 3 else "",
                })
        ps_result = subprocess.run(
            ["ollama", "ps"], capture_output=True, text=True, timeout=5
        )
        loaded = []
        for line in ps_result.stdout.strip().split("\n")[1:]:
            parts = line.split()
            if parts:
                loaded.append(parts[0])
        return {"ok": True, "models": models, "loaded": loaded, "count": len(models)}
    except Exception as e:
        return {"ok": False, "error": str(e), "models": []}

@app.get("/api/models/training/status")
async def training_status():
    """获取训练状态"""
    data_dir = PROJECT_ROOT / "data"
    models_dir = PROJECT_ROOT / "models" / "checkpoints"
    training_files = list(data_dir.glob("*.jsonl"))
    checkpoints = list(models_dir.glob("*")) if models_dir.exists() else []
    return {
        "ok": True,
        "training_data_files": len(training_files),
        "training_data_names": [f.name for f in training_files[:10]],
        "checkpoints": len(checkpoints),
        "checkpoint_names": [c.name for c in checkpoints[:10]],
        "last_train": None,  # TODO: read from training log
    }

@app.post("/api/models/train")
async def trigger_training(request: Request):
    """触发模型训练"""
    try:
        body = await request.json()
        action = body.get("action", "status")
        if action == "train":
            cmd = ["python3", str(PROJECT_ROOT / "bin" / "lh_lora_trainer_v4.py"), "train"]
            proc = subprocess.Popen(
                cmd, cwd=str(PROJECT_ROOT), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True
            )
            return {"ok": True, "action": "train", "pid": proc.pid, "message": "训练已在后台启动"}
        elif action == "setup":
            cmd = ["python3", str(PROJECT_ROOT / "bin" / "lh_lora_trainer_v4.py"), "setup"]
            subprocess.Popen(cmd, cwd=str(PROJECT_ROOT))
            return {"ok": True, "action": "setup", "message": "下载底模已启动"}
        else:
            return await training_status()
    except Exception as e:
        return {"ok": False, "error": str(e)}

# ============================================================
# 技能管理 API
# ============================================================

SKILLS_FILE = PROJECT_ROOT / ".codebuddy" / "custom_skills.json"

def _load_custom_skills() -> dict:
    if SKILLS_FILE.exists():
        try:
            return json.loads(SKILLS_FILE.read_text())
        except Exception:
            pass
    default = {"skills": [], "instructions": [], "updated_at": ""}
    SKILLS_FILE.parent.mkdir(parents=True, exist_ok=True)
    return default

def _save_custom_skills(data: dict):
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    SKILLS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))

@app.get("/api/skills/list")
async def list_skills():
    """列出所有自定义技能和预设技能"""
    custom = _load_custom_skills()
    # 也读取 project 级别的技能目录
    project_skills_dir = PROJECT_ROOT / ".codebuddy" / "skills"
    project_skills = []
    if project_skills_dir.exists():
        for d in sorted(project_skills_dir.iterdir()):
            if d.is_dir():
                skill_md = d / "SKILL.md"
                project_skills.append({
                    "name": d.name,
                    "path": str(d),
                    "has_def": skill_md.exists(),
                })
    return {
        "ok": True,
        "custom_skills": custom.get("skills", []),
        "custom_instructions": custom.get("instructions", []),
        "project_skills": project_skills,
        "project_skills_count": len(project_skills),
        "updated_at": custom.get("updated_at", ""),
    }

@app.post("/api/skills/save")
async def save_skill(request: Request):
    """创建/更新自定义技能"""
    try:
        body = await request.json()
        skill_type = body.get("type", "skill")  # "skill" or "instruction"
        data = _load_custom_skills()
        key = "skills" if skill_type == "skill" else "instructions"
        item = {
            "name": body.get("name", ""),
            "command": body.get("command", ""),
            "description": body.get("description", ""),
            "trigger": body.get("trigger", ""),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        # 更新或追加
        existing_idx = next((i for i, s in enumerate(data[key]) if s.get("name") == item["name"]), None)
        if existing_idx is not None:
            item["created_at"] = data[key][existing_idx].get("created_at", item["created_at"])
            data[key][existing_idx] = item
        else:
            data[key].append(item)
        _save_custom_skills(data)
        return {"ok": True, "item": item, "action": "updated" if existing_idx is not None else "created"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.delete("/api/skills/delete")
async def delete_skill(request: Request):
    """删除自定义技能"""
    try:
        body = await request.json()
        skill_type = body.get("type", "skill")
        name = body.get("name", "")
        data = _load_custom_skills()
        key = "skills" if skill_type == "skill" else "instructions"
        before = len(data[key])
        data[key] = [s for s in data[key] if s.get("name") != name]
        if len(data[key]) == before:
            return {"ok": False, "error": f"未找到: {name}"}
        _save_custom_skills(data)
        return {"ok": True, "deleted": name}
    except Exception as e:
        return {"ok": False, "error": str(e)}

# ============================================================
# 系统信息 API
# ============================================================

@app.get("/api/system/info")
async def system_info():
    """系统信息总览"""
    import platform
    info = {
        "hostname": platform.node(),
        "os": f"{platform.system()} {platform.release()}",
        "arch": platform.machine(),
        "python": platform.python_version(),
        "cwd": os.getcwd(),
        "pid": os.getpid(),
    }
    # CPU
    try:
        info["cpu_count"] = os.cpu_count()
    except Exception:
        pass
    # 内存 (macOS)
    try:
        mem = subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True, timeout=3)
        if mem.stdout.strip():
            total_mb = int(mem.stdout.strip()) / (1024**2)
            info["memory_total_mb"] = round(total_mb)
        vm = subprocess.run(["vm_stat"], capture_output=True, text=True, timeout=3)
        for line in vm.stdout.split("\n"):
            if "free" in line.lower() and "Pages" in line:
                parts = line.strip().split(":")
                if len(parts) == 2:
                    val = parts[1].strip().rstrip(".")
                    info["vm_free_pages"] = int(val) if val.isdigit() else val
    except Exception:
        pass
    # 磁盘
    try:
        disk = subprocess.run(["df", "-h", str(PROJECT_ROOT)], capture_output=True, text=True, timeout=3)
        lines = disk.stdout.strip().split("\n")
        if len(lines) > 1:
            parts = lines[1].split()
            if len(parts) >= 5:
                info["disk_total"] = parts[1]
                info["disk_used"] = parts[2]
                info["disk_avail"] = parts[3]
                info["disk_use_pct"] = parts[4]
    except Exception:
        pass
    return {"ok": True, "info": info}

# ============================================================
# Web 面板
# ============================================================

NOTION_BRIDGE_PANEL = PROJECT_ROOT / "web" / "notion_bridge.html"

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    if NOTION_BRIDGE_PANEL.exists():
        return HTMLResponse(NOTION_BRIDGE_PANEL.read_text(encoding="utf-8"))
    # 降级：内联旧版HTML
    return HTMLResponse("""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>🐉 龍魂 · Notion 对话桥 v2.2</title>
<style>
:root {
  --bg: #0d1117;
  --surface: #161b22;
  --surface-hover: #1f242c;
  --border: #30363d;
  --border-light: #484f58;
  --text: #c9d1d9;
  --text-secondary: #8b949e;
  --accent: #ffd60a;
  --primary: #1f6feb;
  --primary-hover: #388bfd;
  --success: #2ea043;
  --warning: #d29922;
  --danger: #f85149;
  --shadow: 0 4px 24px rgba(0,0,0,0.35);
}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--text);line-height:1.6;min-height:100vh;display:flex;flex-direction:column}
.container{max-width:1400px;margin:0 auto;padding:20px;width:100%;flex:1;display:flex;flex-direction:column}
header{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;margin-bottom:20px;flex-wrap:wrap}
header .brand h1{color:var(--accent);font-size:1.7em;margin-bottom:4px}
header .brand p{color:var(--text-secondary);font-size:0.85em}
header .badges{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.badge{display:inline-flex;align-items:center;gap:4px;padding:4px 10px;border-radius:999px;font-size:0.75em;font-weight:500;background:var(--surface);border:1px solid var(--border)}
.badge.ok{color:var(--success);border-color:var(--success)}
.badge.warn{color:var(--warning);border-color:var(--warning)}
.badge.info{color:var(--primary);border-color:var(--primary)}
main{flex:1;display:grid;grid-template-columns:1fr 360px;gap:20px;min-height:0}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:16px;box-shadow:var(--shadow);display:flex;flex-direction:column;overflow:hidden}
.chat-panel{min-height:520px}
.panel-header{padding:14px 18px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;gap:12px}
.panel-header h2{font-size:1.05em;font-weight:600;color:var(--text)}
.panel-body{flex:1;overflow:hidden;position:relative}
.chat-thread{position:absolute;inset:0;overflow-y:auto;padding:18px;display:flex;flex-direction:column;gap:16px}
.empty-state{text-align:center;color:var(--text-secondary);padding:40px 20px}
.empty-state .icon{font-size:2.5em;margin-bottom:12px}
.message{display:flex;gap:12px;max-width:92%;animation:fadeIn .25s ease}
.message.user{align-self:flex-end;flex-direction:row-reverse}
.message.ai{align-self:flex-start}
.avatar{width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.1em;flex-shrink:0;background:var(--surface-hover);border:1px solid var(--border)}
.message.user .avatar{background:var(--primary);border-color:var(--primary)}
.bubble{max-width:100%;padding:12px 16px;border-radius:16px;background:var(--surface-hover);border:1px solid var(--border);position:relative}
.message.user .bubble{background:var(--primary);color:#fff;border-color:var(--primary);border-bottom-right-radius:4px}
.message.ai .bubble{border-bottom-left-radius:4px}
.bubble .meta{font-size:0.7em;color:var(--text-secondary);margin-bottom:4px;display:flex;align-items:center;gap:8px}
.message.user .bubble .meta{color:rgba(255,255,255,0.75)}
.bubble .content{font-size:0.95em;white-space:pre-wrap;word-break:break-word}
.bubble .content code{font-family:"SF Mono",monospace;background:rgba(0,0,0,0.25);padding:2px 5px;border-radius:4px;font-size:0.9em}
.bubble .content pre{background:rgba(0,0,0,0.25);padding:10px;border-radius:8px;overflow-x:auto;margin:8px 0}
.bubble .content pre code{padding:0;background:transparent}
.message.ai .error{color:var(--danger)}
.sources{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.source-chip{display:inline-flex;align-items:center;gap:6px;padding:5px 10px;border-radius:8px;background:rgba(31,111,235,0.12);border:1px solid rgba(31,111,235,0.3);color:var(--primary);font-size:0.75em;text-decoration:none;max-width:100%}
.source-chip:hover{background:rgba(31,111,235,0.22)}
.source-chip .title{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:220px}
.typing{display:flex;gap:4px;align-items:center;padding:10px 14px}
.typing span{width:7px;height:7px;background:var(--text-secondary);border-radius:50%;animation:typing 1.4s infinite ease-in-out both}
.typing span:nth-child(1){animation-delay:-0.32s}
.typing span:nth-child(2){animation-delay:-0.16s}
@keyframes typing{0%,80%,100%{transform:scale(0)}40%{transform:scale(1)}}
@keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.chat-input-area{padding:14px 18px;border-top:1px solid var(--border);background:rgba(0,0,0,0.15)}
.input-row{display:flex;gap:10px;margin-bottom:10px}
#msgInput{flex:1;padding:11px 14px;background:var(--bg);border:1px solid var(--border);border-radius:12px;color:var(--text);font-size:14px;outline:none;transition:border .15s}
#msgInput:focus{border-color:var(--primary)}
#sendBtn{padding:11px 20px;background:var(--primary);color:#fff;border:none;border-radius:12px;font-size:14px;cursor:pointer;font-weight:500;transition:background .15s}
#sendBtn:hover{background:var(--primary-hover)}
#sendBtn:disabled{opacity:.5;cursor:not-allowed}
.controls-row{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.controls-row select,.controls-row button{padding:7px 11px;background:var(--bg);border:1px solid var(--border);border-radius:8px;color:var(--text);font-size:12px;outline:none}
.controls-row button{cursor:pointer;display:inline-flex;align-items:center;gap:4px}
.controls-row button:hover{border-color:var(--border-light);background:var(--surface-hover)}
.controls-row label{display:inline-flex;align-items:center;gap:5px;font-size:12px;color:var(--text-secondary);cursor:pointer}
.controls-row input[type=checkbox]{accent-color:var(--primary)}
.sidebar{display:flex;flex-direction:column;gap:20px}
.sidebar .panel{max-height:480px}
.tabs{display:flex;border-bottom:1px solid var(--border)}
.tab{flex:1;padding:11px;text-align:center;font-size:0.8em;color:var(--text-secondary);cursor:pointer;border-bottom:2px solid transparent;transition:.15s}
.tab:hover{color:var(--text)}
.tab.active{color:var(--primary);border-bottom-color:var(--primary)}
.tab-content{display:none;padding:16px;overflow-y:auto;flex:1}
.tab-content.active{display:block}
.stat-row{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--border);font-size:0.85em}
.stat-row:last-child{border-bottom:none}
.stat-row span:first-child{color:var(--text-secondary)}
.persona-groups{display:flex;flex-direction:column;gap:14px}
.layer-title{font-size:0.7em;color:var(--text-secondary);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px}
.persona-chips{display:flex;flex-wrap:wrap;gap:6px}
.persona-chip{padding:5px 10px;border-radius:999px;font-size:0.78em;background:var(--bg);border:1px solid var(--border);color:var(--text);cursor:pointer;transition:.15s;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.persona-chip:hover{border-color:var(--primary);color:var(--primary)}
.persona-chip.active{background:var(--accent);color:#111;border-color:var(--accent);font-weight:600}
.history-list{display:flex;flex-direction:column;gap:10px}
.history-item{padding:10px;border-radius:10px;background:var(--bg);border:1px solid var(--border);font-size:0.82em;cursor:pointer;transition:.15s}
.history-item:hover{border-color:var(--border-light)}
.history-item .top{display:flex;justify-content:space-between;gap:8px;margin-bottom:4px;color:var(--text-secondary);font-size:0.75em}
.history-item .q{color:var(--text);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.chain-bar{margin-top:10px;padding:8px 12px;border-radius:8px;background:rgba(210,153,34,0.08);border-left:3px solid var(--warning);color:var(--warning);font-size:0.8em}
.toast{position:fixed;bottom:20px;right:20px;padding:12px 16px;border-radius:10px;background:var(--surface);border:1px solid var(--border);box-shadow:var(--shadow);font-size:0.85em;z-index:100;animation:fadeIn .2s ease}
.toast.error{border-color:var(--danger);color:var(--danger)}
.toast.success{border-color:var(--success);color:var(--success)}
footer{text-align:center;padding:20px;color:var(--text-secondary);font-size:0.7em;border-top:1px solid var(--border);margin-top:20px}
footer .dna{color:var(--accent);font-family:monospace}
@media(max-width:900px){main{grid-template-columns:1fr}.sidebar{order:-1}.sidebar .panel{max-height:280px}}
</style>
</head>
<body>
<div class="container">
  <header>
    <div class="brand">
      <h1>🐉 龍魂 · Notion 对话桥</h1>
      <p>人格引擎集成 · 自动匹配切换 · 联动链路路由 · RAG多模型协作 · 记忆共享</p>
    </div>
    <div class="badges">
      <span class="badge ok" id="engineBadge">🧠 人格引擎 加载中</span>
      <span class="badge info" id="versionBadge">v2.2</span>
    </div>
  </header>

  <main>
    <!-- 对话区 -->
    <section class="panel chat-panel">
      <div class="panel-header">
        <h2>💬 对话</h2>
        <span id="currentPersona" style="font-size:0.8em;color:var(--text-secondary)">🧠 自动匹配人格</span>
      </div>
      <div class="panel-body">
        <div class="chat-thread" id="chatThread">
          <div class="empty-state">
            <div class="icon">💡</div>
            <div>输入消息开始对话</div>
            <div style="font-size:0.85em;margin-top:6px">人格引擎会自动匹配最佳人格并触发联动链路</div>
          </div>
        </div>
      </div>
      <div class="chat-input-area">
        <div class="input-row">
          <input id="msgInput" placeholder="输入消息... (Enter 发送)" onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();sendMsg()}">
          <button id="sendBtn" onclick="sendMsg()">发送</button>
        </div>
        <div class="controls-row">
          <select id="sessionSelect"><option value="default">默认会话</option></select>
          <select id="personaSelect" onchange="autoSwitchPersona()">
            <option value="">🤖 自动匹配</option>
          </select>
          <select id="modelSelect" title="模型策略">
            <option value="auto">🤖 自动协作 (本地→DeepSeek→Kimi)</option>
            <option value="local">🏠 本地模型 (Ollama)</option>
            <option value="deepseek">🔮 DeepSeek</option>
            <option value="kimi">🌙 Kimi</option>
          </select>
          <input id="modelInput" type="text" placeholder="模型名 (可选)" title="如 qwen2.5:1.5b / deepseek-v4-flash / moonshot-v1-8k" style="background:var(--bg);border:1px solid var(--border);border-radius:8px;color:var(--text);padding:7px 11px;font-size:12px;outline:none;min-width:120px">
          <label><input type="checkbox" id="usePersona" checked onchange="togglePersona()"> 启用人格</label>
          <button onclick="clearChat()">🗑 清空</button>
          <button onclick="regenerate()" id="regenBtn" disabled>🔄 重答</button>
        </div>
      </div>
    </section>

    <!-- 侧边栏 -->
    <aside class="sidebar">
      <div class="panel">
        <div class="tabs">
          <div class="tab active" onclick="switchTab('status')">📊 状态</div>
          <div class="tab" onclick="switchTab('personas')">🧠 人格</div>
          <div class="tab" onclick="switchTab('history')">💾 历史</div>
        </div>
        <div class="tab-content active" id="tab-status">
          <div class="stat-row"><span>人格引擎</span><span id="personaStatus">-</span></div>
          <div class="stat-row"><span>模型策略</span><span id="modelStrategy">-</span></div>
          <div class="stat-row"><span>🏠 本地模型</span><span id="modelLocalStatus">-</span></div>
          <div class="stat-row"><span>🔮 DeepSeek</span><span id="modelDeepSeekStatus">-</span></div>
          <div class="stat-row"><span>🌙 Kimi</span><span id="modelKimiStatus">-</span></div>
          <div class="stat-row"><span>已同步页面</span><span id="pageCount">-</span></div>
          <div class="stat-row"><span>已同步块</span><span id="blockCount">-</span></div>
          <div class="stat-row"><span>聊天消息</span><span id="chatCount">-</span></div>
          <div class="stat-row"><span>活跃会话</span><span id="sessionCount">-</span></div>
        </div>
        <div class="tab-content" id="tab-personas">
          <div id="personaList" class="persona-groups">加载中...</div>
        </div>
        <div class="tab-content" id="tab-history">
          <div id="historyList" class="history-list">加载中...</div>
        </div>
      </div>

      <div class="panel" style="max-height:none">
        <div class="panel-header"><h2>📚 使用提示</h2></div>
        <div class="panel-body" style="padding:16px;font-size:0.82em;color:var(--text-secondary);line-height:1.8">
          <p>• 直接输入问题，AI 会基于 Notion 资料回答。</p>
          <p>• 可手动选择人格，或关闭人格使用纯 RAG。</p>
          <p>• 可切换模型策略：自动协作 / 本地 / DeepSeek / Kimi。</p>
          <p>• 支持导航意图："查看 XXX 页面"。</p>
          <p>• 若模型输出乱码，自动协作模式会降级到下一个可用模型。</p>
        </div>
      </div>
    </aside>
  </main>
</div>

<footer>
  DNA: <span class="dna">#龍芯⚡️丙午·乙未·丁未·丙午·䷖剥-NOTION-BRIDGE-v2.2-PERSONA-INTEGRATED</span> &nbsp;|&nbsp;
  确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z &nbsp;|&nbsp;
  创建者: 诸葛鑫（UID9622） &nbsp;|&nbsp;
  协议: CC BY-NC-SA 4.0
</footer>

<script src="/static/notion_bridge_enhanced.js"></script>
</body>
</html>""")


# ============================================================
# CLI 同步/搜索/对话
# ============================================================

def cli_sync(database_id: Optional[str] = None):
    """CLI 全量同步"""
    print("🔄 正在同步 Notion...")
    client = NotionClient()
    if not database_id:
        # 尝试环境变量
        database_id = os.environ.get("NOTION_PERSONA_DB", "")
    count = sync_pages(client, database_id=database_id) if database_id else 0
    print(f"✅ 同步完成: {count} 个页面")
    return count

def cli_search(query: str, limit: int = 10):
    """CLI 搜索"""
    client = NotionClient()
    results = search_hybrid(client, query, limit)
    for i, r in enumerate(results):
        print(f"\n{i+1}. 📄 {r.get('title', '未命名')}")
        content = r.get('content', '')[:200]
        if content:
            print(f"   {content}")
    return results

def _audit_emoji(status: str) -> str:
    if status == "green":
        return "🟢"
    if status == "yellow":
        return "🟡"
    if status == "red":
        return "🔴"
    return "⚪"


def print_chat_result(result: Dict[str, Any], style: str = "plain"):
    """按指定终端风格输出对话结果。"""
    if style == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if style == "rich":
        mp = result.get("model_provider", "") or result.get("provider", "")
        mn = result.get("model_name", "") or result.get("model", "")
        audit = result.get("audit_status", "unknown")
        dna = result.get("model_dna", "") or result.get("dna", "")
        persona = result.get("persona_applied", "") or result.get("persona", "")
        chain = result.get("fallback_chain", [])
        reply = result.get("response") or result.get("reply", "无响应")

        lines = [
            "",
            "╔══════════════════════════════════════════════════════════╗",
            "║  🐉 龍魂 · Notion 对话桥 CLI 输出                        ║",
            "╠══════════════════════════════════════════════════════════╣",
        ]
        if persona:
            lines.append(f"║  🧠 人格: {persona:<47} ║")
        lines.append(f"║  🤖 模型: {mp}/{mn}".ljust(59) + "║")
        lines.append(f"║  {_audit_emoji(audit)} 审计: {audit}".ljust(58) + "║")
        if dna:
            lines.append(f"║  🧬 DNA: {dna[:50]}".ljust(59) + "║")
        if chain:
            lines.append("╠══════════════════════════════════════════════════════════╣")
            lines.append("║  🔁 降级链:".ljust(59) + "║")
            for c in chain:
                lines.append(f"║    • {c.get('provider', '?')}/{c.get('model', '?')}: {c.get('reason', '')}".ljust(59) + "║")
        lines.append("╠══════════════════════════════════════════════════════════╣")
        for line in reply.splitlines():
            lines.append(f"  {line}")
        lines.append("╚══════════════════════════════════════════════════════════╝")
        print("\n".join(lines))
        return

    if style == "terminal":
        mp = result.get("model_provider", "") or result.get("provider", "")
        mn = result.get("model_name", "") or result.get("model", "")
        audit = result.get("audit_status", "unknown")
        dna = result.get("model_dna", "") or result.get("dna", "")
        reply = result.get("response") or result.get("reply", "无响应")
        print("")
        print("$" * 62)
        print(f"$ [TERMINAL] 龍魂·Notion桥  {PROTOCOL_VERSION:<25}$")
        print("$" * 62)
        if mp:
            print(f"$ provider : {mp}/{mn}")
        print(f"$ audit    : {audit} {_audit_emoji(audit)}")
        if dna:
            print(f"$ dna      : {dna[:50]}")
        print("-" * 62)
        for line in reply.splitlines():
            print(f"> {line}")
        print("$" * 62)
        return

    if style == "markdown":
        mp = result.get("model_provider", "") or result.get("provider", "")
        mn = result.get("model_name", "") or result.get("model", "")
        audit = result.get("audit_status", "unknown")
        dna = result.get("model_dna", "") or result.get("dna", "")
        reply = result.get("response") or result.get("reply", "无响应")
        print("---")
        print(f"## 🤖 模型: `{mp}/{mn}`")
        print(f"- **审计**: `{audit}` {_audit_emoji(audit)}")
        if dna:
            print(f"- **DNA**: `{dna}`")
        print("")
        print(reply)
        print("---")
        return

    # plain
    mp = result.get("model_provider", "") or result.get("provider", "")
    mn = result.get("model_name", "") or result.get("model", "")
    if mp:
        print(f"\n🤖 回答模型: {mp}/{mn}")
    if result.get("audit_status") == "red" or not (result.get("response") or result.get("reply")):
        chain = result.get("fallback_chain", [])
        if chain:
            print("\n🔁 模型降级链:")
            for c in chain:
                print(f"  • {c.get('provider', '?')}/{c.get('model', '?')}: {c.get('reason', '')}")
    print(f"\n{result.get('response') or result.get('reply', '无响应')}")


def cli_chat(message: str, session_id: str = "default",
             provider: Optional[str] = None, model: Optional[str] = None,
             privacy: Optional[str] = None, mode: str = "single",
             style: str = "plain", providers: Optional[List[str]] = None):
    """CLI 对话，支持 single / council / multi 三种模式。"""
    client = NotionClient()

    if mode == "council":
        if not COUNCIL_AVAILABLE or wuxing_council is None:
            print("❌ 五行议事会未加载")
            sys.exit(1)
        messages = _build_chat_messages(session_id, message)
        sources = search_hybrid(client, message, limit=6)
        system_prefix = _build_system_prefix(session_id, message, True, sources)
        result = wuxing_council.chat(
            session_id=session_id,
            message=message,
            messages=messages,
            sources=sources,
            system_prefix=system_prefix,
            temperature=0.35,
            max_tokens=512,
        )
        result = ProtocolGuard.guard(result)
        _save_council_chat(session_id, message, result)
        print_chat_result(result, style=style)
        return result

    if mode == "multi":
        messages = _build_chat_messages(session_id, message)
        sources = search_hybrid(client, message, limit=6)
        system_prefix = _build_system_prefix(session_id, message, True, sources)
        if system_prefix:
            messages = [{"role": "system", "content": system_prefix}] + messages
        result = model_router.generate_multi(
            messages,
            providers=providers or ["local", "deepseek", "kimi"],
            model=model,
            temperature=0.3,
            max_tokens=1024,
        )
        save_chat(
            session_id, message, result.get("reply", ""),
            model_provider=result.get("model_provider", "multi"),
            model_name=result.get("model_name", "multi-collab"),
            model_dna=result.get("model_dna", ""),
            audit_status=result.get("audit_status", "yellow"),
        )
        print_chat_result(result, style=style)
        return result

    # single / 默认
    result = process_chat_with_persona(
        message, session_id, True, client,
        provider=provider, model=model, privacy=privacy, mode=None
    )
    print_chat_result(result, style=style)
    return result

def cli_status():
    """CLI 状态"""
    conn = sqlite3.connect(str(SYNC_DB))
    page_count = conn.execute("SELECT COUNT(*) FROM pages").fetchone()[0]
    block_count = conn.execute("SELECT COUNT(*) FROM blocks").fetchone()[0]
    conn.close()

    conn2 = sqlite3.connect(str(CHAT_HISTORY_DB))
    chat_count = conn2.execute("SELECT COUNT(*) FROM chat_history").fetchone()[0]
    conn2.close()

    providers = model_router.probe_all()
    provider_lines = []
    for p in providers:
        status_icon = "🟢" if p.get("status") == "online" else "🔴"
        models = ", ".join(p.get("models", [])[:3])
        err = f" ({p.get('error')})" if p.get("error") else ""
        provider_lines.append(f"    {status_icon} {p['name']}: {p['status']} [{models}]{err}")

    print(f"""
📊 龍魂 · Notion 对话桥 v2.2 状态
  🧠 人格引擎: {'✅ 已加载' if PERSONA_AVAILABLE else '❌ 不可用'}
  📚 已同步页面: {page_count}
  📦 已同步块: {block_count}
  💬 聊天消息: {chat_count}
  🧬 模型策略: {DEFAULT_PROVIDER} | 隐私模式: {CHAT_PRIVACY}
{"\n".join(provider_lines)}
  🔑 确认码: {CONFIRM_CODE}
""")

def start_server(host: str = "127.0.0.1", port: int = 8779):
    """启动 FastAPI 服务"""
    print(f"""
╔══════════════════════════════════════════════╗
║  🐉 龍魂 · Notion 对话桥 v2.2              ║
║  人格引擎集成 · RAG本地推理 · 记忆共享     ║
╠══════════════════════════════════════════════╣
║  地址: http://{host}:{port}           ║
║  人格: {'✅ '+str(len(persona_runtime.list_personas()))+'个人格' if PERSONA_AVAILABLE else '❌ 不可用'}         ║
╠══════════════════════════════════════════════╣
║  POST /api/chat         对话+RAG+人格       ║
║  POST /api/search       混合搜索            ║
║  GET  /api/persona/list    人格列表          ║
║  POST /api/persona/switch  切换人格          ║
║  POST /api/persona/chain   联动链路          ║
║  POST /api/persona/match   人格匹配          ║
║  GET  /api/history      聊天历史            ║
║  GET  /api/stats        数据库统计          ║
╠══════════════════════════════════════════════╣
║  Web 面板: http://{host}:{port}             ║
╚══════════════════════════════════════════════╝
    """)
    uvicorn.run(app, host=host, port=port, log_level="warning")

# ============================================================
# 主入口
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="龍魂 · Notion 对话桥 v2.2 (人格引擎深度集成 + 多模型协作)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh notion-bridge                             # 启动服务 (端口8779)
  lh notion-bridge --port 8779 --host 0.0.0.0
  lh notion-bridge sync                        # 全量同步
  lh notion-bridge search "关键词"              # 搜索
  lh notion-bridge chat "问题"                  # 单模型对话（默认 auto）
  lh notion-bridge chat "问题" --mode council  # 五行议事会
  lh notion-bridge chat "问题" --mode multi --providers local,deepseek,kimi
  lh notion-bridge chat "问题" --provider deepseek --model deepseek-v4-flash --style rich
  lh notion-bridge chat "问题" --provider local --model longhun-v4.0 --style json
  lh notion-bridge chat "问题" --mode council --style terminal
  lh notion-bridge chat "问题" --mode multi --style markdown
  lh notion-bridge status                      # 查看状态
        """
    )
    parser.add_argument("--host", default="127.0.0.1", help="监听地址")
    parser.add_argument("--port", type=int, default=8779, help="监听端口")
    parser.add_argument("--provider", default=None,
                        choices=["auto", "local", "deepseek", "kimi"],
                        help="模型策略: auto(本地优先降级) local deepseek kimi")
    parser.add_argument("--model", default=None, help="指定模型名，如 longhun-v4.0 / deepseek-v4-flash / moonshot-v1-8k")
    parser.add_argument("--privacy", default=None, choices=["normal", "strict"],
                        help="隐私模式: strict 仅使用本地模型")
    parser.add_argument("--style", default="plain", choices=["plain", "rich", "json", "terminal", "markdown"],
                        help="CLI 输出风格: plain(纯文本) rich(彩色面板) json(完整 JSON) terminal(复古终端) markdown(Markdown)")
    parser.add_argument("--mode", default="single", choices=["single", "council", "multi"],
                        help="对话模式: single(单模型) council(五行议事会) multi(多模型并行协作)")
    parser.add_argument("--providers", default=None,
                        help="multi 模式时指定的 provider 列表，逗号分隔，如 local,deepseek,kimi")

    # 子命令
    parser.add_argument("command", nargs="?", default="serve",
                        choices=["serve", "sync", "search", "chat", "status"],
                        help="命令: serve(启动服务) sync(同步) search(搜索) chat(对话) status(状态)")
    parser.add_argument("args", nargs="*", help="命令参数")

    args = parser.parse_args()

    if args.command == "sync":
        db_id = args.args[0] if args.args else None
        cli_sync(db_id)
    elif args.command == "search":
        if not args.args:
            print("❌ 请提供搜索关键词")
            sys.exit(1)
        cli_search(" ".join(args.args))
    elif args.command == "chat":
        if not args.args:
            print("❌ 请提供对话内容")
            sys.exit(1)
        providers = [p.strip() for p in args.providers.split(",") if p.strip()] if args.providers else None
        cli_chat(
            " ".join(args.args),
            provider=args.provider, model=args.model, privacy=args.privacy,
            mode=args.mode, style=args.style, providers=providers
        )
    elif args.command == "status":
        cli_status()
    else:
        start_server(args.host, args.port)

if __name__ == "__main__":
    main()
