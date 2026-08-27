#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-KB-API-ROUTER-v1.0
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂·Notion 知识库引用架构 L4 — 鲲鹏 API 路由
=============================================
DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-KB-API-ROUTER-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（核心思想层）/ MulanPSL v2（工程实现层）

端点（prefix /api/kb）:
  GET  /search?q=&limit=        — 本地索引检索（D4 公开，只回摘要+链接，不回全文）
  GET  /page/{page_id}          — Notion 页面代理（有 NOTION_TOKEN 调 Notion，无则降级索引摘要）
  GET  /dna?title=&category=…   — 社区实时 DNA 公式计算（复用 lh_dna_generator.generate，非手写）
  POST /webhook                 — Notion 变更回调（X-API-Key 鉴权→重算 DNA→更新索引）

安全基线:
  - token/密钥只从环境变量读（NOTION_TOKEN / KB_WEBHOOK_KEY），不硬编码、不进日志
  - 索引路径可配: NOTION_KB_INDEX > 脚本同目录 notion_kb_index.json > ~/.longhun/data/notion_kb/index.json
  - 防投毒/输入过滤由网关全局中间件兜底（本 router 不重复造轮子）
  - 索引原子写（tmp + os.replace），防半写
"""
import os
import sys
import json
import time
import logging
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Request, HTTPException, Query, Header

# 同目录依赖（部署时与网关一起同步）
_SELF_DIR = Path(__file__).resolve().parent
if str(_SELF_DIR) not in sys.path:
    sys.path.insert(0, str(_SELF_DIR))

try:
    from lh_dna_generator import generate as dna_generate
except ImportError:
    dna_generate = None

logger = logging.getLogger("kb_api_router")

router = APIRouter(prefix="/api/kb", tags=["kb"])

# ─────────────────────────────────────────────────────────
# 常量
# ─────────────────────────────────────────────────────────
DEFAULT_INDEX_CANDIDATES = [
    "notion_kb_index.json",                      # 部署目录
    os.path.expanduser("~/.longhun/data/notion_kb/index.json"),  # 鲲鹏数据目录
]
NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
MAX_LIMIT = 20
DEFAULT_LIMIT = 10
MAX_TITLE_LEN = 200
MAX_QUERY_LEN = 100


# ─────────────────────────────────────────────────────────
# 索引读写（原子）
# ─────────────────────────────────────────────────────────
def _resolve_index_path() -> Path:
    env_path = os.environ.get("NOTION_KB_INDEX")
    if env_path:
        return Path(env_path)
    for cand in DEFAULT_INDEX_CANDIDATES:
        p = Path(cand)
        if p.exists():
            return p
    # 都不存在 → 用部署目录默认路径（读取会得到空，但可写）
    return _SELF_DIR / "notion_kb_index.json"


LIST_KEYS = ("pages", "items", "entries")


def _load_index() -> List[Dict[str, Any]]:
    path = _resolve_index_path()
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            for k in LIST_KEYS:
                if isinstance(data.get(k), list):
                    return data[k]
            return []
        if isinstance(data, list):
            return data
    except (json.JSONDecodeError, OSError) as e:
        logger.warning("索引读取失败 %s: %s", path, e)
    return []


def _save_index(items: List[Dict[str, Any]]) -> Path:
    """原子写索引（结构感知：保留原文件顶层骨架，兼容 pages/items/entries）"""
    path = _resolve_index_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    skeleton: Dict[str, Any] = {"meta": {"schema_version": 1, "updated_at": datetime_utc()}}
    list_key = "pages"
    try:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                old = json.load(f)
            if isinstance(old, dict):
                skeleton = old
                for k in LIST_KEYS:
                    if isinstance(old.get(k), list):
                        list_key = k
                        break
    except (json.JSONDecodeError, OSError):
        pass  # 原文件不可读 → 用默认骨架
    skeleton[list_key] = items
    skeleton["meta"] = {**(skeleton.get("meta") or {}), "updated_at": datetime_utc(), "total": len(items)}
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(skeleton, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
    return path


def datetime_utc() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ─────────────────────────────────────────────────────────
# 检索
# ─────────────────────────────────────────────────────────
def _match_score(item: Dict[str, Any], q_lower: str) -> int:
    """匹配度：标题3 > 标签/分类2 > 摘要1 > 0"""
    title = str(item.get("title", "")).lower()
    if q_lower in title:
        return 3
    for key in ("tags", "category"):
        vals = item.get(key, "")
        if isinstance(vals, list):
            vals = " ".join(str(v) for v in vals)
        if q_lower in str(vals).lower():
            return 2
    summary = str(item.get("summary", "")).lower()
    if q_lower in summary:
        return 1
    return 0


@router.get("/search")
async def kb_search(
    q: str = Query(..., description="检索关键词"),
    limit: int = Query(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT),
    request: Request = None,
):
    """社区检索：只回摘要+链接，不回全文（信息主权边界）"""
    q_clean = (q or "").strip()[:MAX_QUERY_LEN]
    if not q_clean:
        raise HTTPException(status_code=400, detail="q 不能为空")
    items = _load_index()
    scored = [(item, _match_score(item, q_clean.lower())) for item in items]
    hits = [it for it, s in scored if s > 0]
    # 按匹配度降序，同分保持原顺序
    hits.sort(key=lambda it: -_match_score(it, q_clean.lower()))
    result = [
        {
            "id": item.get("id"),
            "title": item.get("title"),
            "category": item.get("category"),
            "summary": (str(item.get("summary", "")) or "")[:300],
            "dna": item.get("dna"),
            "url": item.get("url"),
            "updated_at": item.get("updated_at"),
        }
        for item in hits[:limit]
    ]
    return {
        "query": q_clean,
        "hits": len(hits),
        "returned": len(result),
        "items": result,
        "dna_engine": "lh_dna_generator.v2.0",
        "sovereign": "UID9622",
    }


# ─────────────────────────────────────────────────────────
# 页面详情（Notion 代理，可降级）
# ─────────────────────────────────────────────────────────
def _is_valid_page_id(page_id: str) -> bool:
    return bool(page_id) and len(page_id) <= 64 and all(
        c in "0123456789abcdefABCDEF-" for c in page_id
    )


def _notion_fetch(page_id: str) -> Optional[Dict[str, Any]]:
    """调 Notion API 取页面；无 token 或失败返回 None"""
    token = os.environ.get("NOTION_TOKEN", "").strip()
    if not token or not dna_generate:
        return None
    import urllib.request

    url = f"{NOTION_API}/pages/{page_id}"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:  # 网络/401/404 一律降级
        logger.warning("Notion 代理失败 %s: %s", page_id, e)
        return None


def _extract_notion_summary(data: Dict[str, Any]) -> Dict[str, Any]:
    """从 Notion page 响应提取轻量摘要（不返回全文属性）"""
    title = "Untitled"
    props = data.get("properties", {}) or {}
    for key, val in props.items():
        if val.get("type") == "title" and val.get("title"):
            texts = [t.get("plain_text", "") for t in val["title"]]
            title = "".join(texts)
            break
    return {
        "id": data.get("id"),
        "title": title,
        "url": data.get("url"),
        "notion": True,
        "archived": data.get("archived", False),
    }


@router.get("/page/{page_id}")
async def kb_page(page_id: str, request: Request = None):
    """页面详情：优先 Notion 代理，无 token 降级返回本地索引摘要"""
    if not _is_valid_page_id(page_id):
        raise HTTPException(status_code=400, detail="非法 page_id")
    # 降级：本地索引
    for item in _load_index():
        if str(item.get("id", "")).replace("-", "") == page_id.replace("-", ""):
            local = {
                "id": item.get("id"),
                "title": item.get("title"),
                "category": item.get("category"),
                "summary": item.get("summary"),
                "dna": item.get("dna"),
                "url": item.get("url"),
                "source": "local_index",
            }
            break
    else:
        local = None

    notion = _notion_fetch(page_id)
    if notion:
        return {"source": "notion_live", **local, **{k: v for k, v in _extract_notion_summary(notion).items() if k not in ("id",)}}
    if local:
        return local
    return {"source": "not_found", "id": page_id, "hint": "索引无此页且 Notion 代理不可用（服务端未配置 NOTION_TOKEN）"}


# ─────────────────────────────────────────────────────────
# DNA 社区计算（公式一致·非手写）
# ─────────────────────────────────────────────────────────
@router.get("/dna")
async def kb_dna(
    title: str = Query(..., description="标题"),
    category: str = Query("doc", description="分类"),
    action: str = Query("社区引用", description="动作"),
    actor: str = Query("COMMUNITY", description="行为者"),
):
    """社区实时 DNA 计算——复用 lh_dna_generator.generate，与全系统公式完全一致"""
    if not dna_generate:
        raise HTTPException(status_code=503, detail="DNA 引擎不可用")
    title_clean = (title or "").strip()[:MAX_TITLE_LEN]
    if not title_clean:
        raise HTTPException(status_code=400, detail="title 不能为空")
    cat = (category or "doc").strip()[:50]
    act = (action or "社区引用").strip()[:50]
    actr = (actor or "COMMUNITY").strip()[:50]

    payload = dna_generate(title_clean, cat, act, actr)
    return {
        "dna_string": payload.dna_string,
        "compact_dna": payload.compact_dna,
        "hexagram": f"{payload.hexagram_symbol}{payload.hexagram_name}",
        "hexagram_num": payload.hexagram_num,
        "phase": payload.hexagram_phase,
        "wuxing": {"dominant": payload.wuxing.dominant, "tendency": payload.wuxing.tendency, "sheng": payload.wuxing.sheng, "ke": payload.wuxing.ke},
        "digital_root": payload.digital_root,
        "is_369": payload.is_369,
        "title_hash": payload.title_hash,
        "timestamp": payload.timestamp,
        "root_card": payload.root_card,
        "sovereign": "UID9622",
        "dna_engine": "lh_dna_generator.v2.0",
    }


# ─────────────────────────────────────────────────────────
# Webhook — Notion 变更回调（X-API-Key 鉴权）
# ─────────────────────────────────────────────────────────
@router.post("/webhook")
async def kb_webhook(
    request: Request,
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
):
    """Notion 变更回调：校验密钥 → 重算 DNA → 原子更新索引"""
    expected = os.environ.get("KB_WEBHOOK_KEY", "").strip()
    if not expected:
        raise HTTPException(status_code=503, detail="服务端未配置 KB_WEBHOOK_KEY，webhook 未启用")
    if not x_api_key or x_api_key.strip() != expected:
        raise HTTPException(status_code=401, detail="X-API-Key 无效")

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="请求体必须是 JSON")
    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="请求体必须是对象")

    page_id = str(body.get("page_id", "")).strip()
    title = str(body.get("title", "")).strip()[:MAX_TITLE_LEN]
    if not page_id or not title:
        raise HTTPException(status_code=400, detail="page_id 与 title 必填")
    category = str(body.get("category", "doc")).strip()[:50]
    action = str(body.get("action", "更新")).strip()[:50]
    actor = str(body.get("actor", "WEBHOOK")).strip()[:50]

    # 重算 DNA（公式一致）
    if not dna_generate:
        raise HTTPException(status_code=503, detail="DNA 引擎不可用")
    payload = dna_generate(title, category, action, actor)

    # 更新索引（命中更新，未命中追加）
    items = _load_index()
    entry = {
        "id": page_id,
        "title": title,
        "category": category,
        "summary": str(body.get("summary", ""))[:500],
        "url": body.get("url"),
        "dna": payload.dna_string,
        "updated_at": datetime_utc(),
        "source": "webhook",
    }
    replaced = False
    for i, item in enumerate(items):
        if str(item.get("id", "")).replace("-", "") == page_id.replace("-", ""):
            items[i] = {**item, **entry}
            replaced = True
            break
    if not replaced:
        items.append(entry)
    path = _save_index(items)

    logger.info("KB webhook 更新 %s（%s）→ %s", title, page_id, path)
    return {
        "ok": True,
        "mode": "updated" if replaced else "appended",
        "id": page_id,
        "dna": payload.dna_string,
        "total": len(items),
        "index_path": str(path),
        "sovereign": "UID9622",
    }
