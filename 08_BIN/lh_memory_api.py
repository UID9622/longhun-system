#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙未·辛酉·井-MEMORY-API-v1.2-NOTION-INDEX-BRIDGE
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# 职能: 龍魂统一记忆API — 所有AI（无论国家/模型）的唯一记忆入口
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
龍魂·统一记忆 API v1.2
────────────────────────────
端口: 8771 (Mac) / 8773 (鲲鹏)

v1.2 更新:
  - 🧠 Notion回源：本地未命中 → 自动搜索Notion数据库
  - 📇 日志索引：启动时自动加载 ~/.longhun/memory_index.json
  - 🔍 三级搜索：本地MEMORY.md → 日志索引 → Notion后备大脑
v1.1 更新:
  - 🔥 身份联动闭环：远程请求 Token 验证前置调用 identity 服务
  - 🔥 Token 安全：客户端从环境变量/文件静默读取，不暴露明文

设计原则:
  1. 所有 AI 统一入口 — 不给任何模型开特例
  2. 只读为主 — AI 只能读取记忆，不能修改
  3. 本地优先 — 默认只绑 127.0.0.1
  4. 主权焊死 — UID9622 身份永不可改
  5. 身份联动 — 远程Token通过identity服务动态验证

端点:
  GET  /v1/memory                    — 获取完整记忆（JSON结构化）
  GET  /v1/memory/raw                — 获取原始 MEMORY.md 全文
  GET  /v1/memory/section/{name}     — 获取指定节
  GET  /v1/memory/identity           — 获取身份焊死块
  GET  /v1/memory/search?q=xxx       — 三级搜索（本地→索引→Notion）
  GET  /v1/memory/anchors            — 获取锚清单
  GET  /v1/memory/health             — 健康检查
  GET  /v1/memory/stats              — 统计信息
  GET  /v1/memory/index              — 日志索引状态
  POST /v1/memory/reload             — 重载索引（需本地/auth）
  POST /v1/memory/daily              — 追加今日日志（需认证）

认证链路（远程请求）:
  Client → [X-API-Token] → Memory API
    → POST https://uid9622.cn/identity/token-verify (身份服务动态确认)
    → ✅ 通过 → 返回记忆数据
    → 🔴 拒绝 → 403
    → ⏱ 不可用 → 回退本地Token验证

启动: python3 bin/lh_memory_api.py [--port 8771] [--host 127.0.0.1]
"""

import hashlib
import hmac
import json
import os
import re
import logging
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel

# ═══════════════════════════════════════════════
# 常量·路径
# ═══════════════════════════════════════════════
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from engines.lh_fixed_point_memory_archive import MemoryArchive
except Exception:
    MemoryArchive = None
CST = timezone(timedelta(hours=8))
MEMORY_FILE = PROJECT_ROOT / ".codebuddy" / "memory" / "MEMORY.md"
DAILY_LOG_DIR = PROJECT_ROOT / ".codebuddy" / "memory"
TOKEN_FILE = PROJECT_ROOT / ".codebuddy" / "memory" / ".api_token"
API_LOG_FILE = PROJECT_ROOT / "logs" / "memory_api.log"
INDEX_FILE = Path.home() / ".longhun" / "memory_index.json"

# Notion 后备大脑
NOTION_TOKEN = os.environ.get("NOTION_TOKEN") or os.environ.get("NOTION_TOKEN_CNSH") or ""
NOTION_DB_ID = "3a97125a-9c9f-81aa-89f2-c372b7d40522"
NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}
NOTION_ENABLED = bool(NOTION_TOKEN)

# 焊死确认码
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"

# v1.2: 日志记录器
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger("lh_memory_api")

# 确保日志目录
(API_LOG_FILE.parent).mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════════════
# 内存缓存
# ═══════════════════════════════════════════════
_memory_cache: Dict[str, Any] = {}
_cache_time: float = 0
CACHE_TTL = 30  # 秒，30秒刷新一次

# 🔥 v1.2: 日志索引缓存
_index_cache: Optional[Dict[str, Any]] = None
_index_time: float = 0
INDEX_CACHE_TTL = 120  # 索引刷新间隔（秒）


# ═══════════════════════════════════════════════
# FastAPI 应用
# ═══════════════════════════════════════════════
app = FastAPI(
    title="龍魂·统一记忆 API",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    expose_headers=["X-Memory-Version", "X-Memory-DNA"],
)

# ═══════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════

class DailyLogEntry(BaseModel):
    content: str
    token: Optional[str] = None


class ArchiveIngestEntry(BaseModel):
    text: str
    source: str = "api"
    tags: List[str] = []
    token: Optional[str] = None


class SearchResult(BaseModel):
    section: str
    snippet: str
    line_num: int


# ═══════════════════════════════════════════════
# Token 管理 + 身份服务桥接
# ═══════════════════════════════════════════════

# 身份服务地址（通过 Nginx 反代到鲲鹏 8772）
IDENTITY_SERVICE_URL = "https://uid9622.cn/identity/token-verify"
IDENTITY_SERVICE_TIMEOUT = 5  # 秒


def get_or_create_token() -> str:
    """获取或生成 API Token"""
    if TOKEN_FILE.exists():
        return TOKEN_FILE.read_text().strip()
    # 生成唯一 token
    seed = f"longhun-memory-{CONFIRM_CODE}-{time.time()}"
    token = hashlib.sha256(seed.encode()).hexdigest()[:32]
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(token)
    TOKEN_FILE.chmod(0o600)  # 仅 owner 可读写
    return token


def verify_token_via_identity(token: str) -> Optional[bool]:
    """
    🔥 身份联动闭环：调用 identity 服务动态验证 Token。
    返回 True=验证通过, False=验证拒绝, None=服务不可用（回退本地验证）。
    """
    try:
        payload = json.dumps({"token": token, "source": "memory-api"}).encode("utf-8")
        req = urllib.request.Request(
            IDENTITY_SERVICE_URL,
            data=payload,
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=IDENTITY_SERVICE_TIMEOUT) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            valid = result.get("valid", False)
            log_identity_result("PASS" if valid else "DENY", result.get("message", ""))
            return valid
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:200]
        log_identity_result("ERROR", f"HTTP {e.code}: {body}")
        return None
    except urllib.error.URLError as e:
        log_identity_result("UNREACHABLE", str(e.reason))
        return None
    except Exception as e:
        log_identity_result("ERROR", str(e))
        return None


def log_identity_result(status: str, detail: str):
    """记录身份验证结果到日志"""
    ts = datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")
    marker = "✅" if status == "PASS" else "🔴" if status == "DENY" else "🟡"
    line = f"[{ts}] {marker} IDENTITY-CHECK [{status}] {detail}\n"
    try:
        with open(API_LOG_FILE, "a") as f:
            f.write(line)
    except Exception:
        pass


def verify_token(request: Request, token_from_body: Optional[str] = None) -> bool:
    """验证请求令牌（v1.1: 远程请求前置身份服务动态验证）"""
    # 本地请求无需认证
    client_host = request.client.host if request.client else ""
    if client_host in ("127.0.0.1", "::1", "localhost"):
        return True

    # 远程请求需要 token
    provided = request.headers.get("X-API-Token", "")
    if not provided and token_from_body:
        provided = token_from_body

    if not provided:
        return False

    # 🔥 v1.1 身份联动：前置调用 identity 服务动态验证
    identity_result = verify_token_via_identity(provided)

    if identity_result is True:
        # 身份服务确认 → 通过
        return True
    elif identity_result is False:
        # 身份服务拒绝 → 拒绝
        return False
    else:
        # 身份服务不可用 → 回退本地 Token 验证
        expected = get_or_create_token()
        log_identity_result("FALLBACK", "identity service unreachable, falling back to local token")
        return hmac.compare_digest(provided, expected)


def require_auth(func):
    """认证装饰器 — 只对 POST/写操作"""
    async def wrapper(*args, **kwargs):
        request = kwargs.get("request")
        if not request:
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
        if not request or not verify_token(request):
            raise HTTPException(status_code=403, detail="需要 API Token。本地访问无需认证。")
        return await func(*args, **kwargs)
    return wrapper


# ═══════════════════════════════════════════════
# 记忆解析引擎
# ═══════════════════════════════════════════════

def parse_memory_md() -> Dict[str, Any]:
    """解析 MEMORY.md 为结构化 JSON"""
    global _memory_cache, _cache_time

    now = time.time()
    if _memory_cache and (now - _cache_time) < CACHE_TTL:
        return _memory_cache

    if not MEMORY_FILE.exists():
        return {"error": "MEMORY.md 不存在", "sections": {}, "raw": ""}

    raw = MEMORY_FILE.read_text(encoding="utf-8")
    sections: Dict[str, str] = {}
    current_section = "_preamble"
    current_content: List[str] = []

    for line in raw.split("\n"):
        # 检测节标题: ## §N. 或 ## §N
        m = re.match(r'^##\s+(§\d+[\.\s])', line)
        if m:
            if current_content:
                sections[current_section] = "\n".join(current_content).strip()
            current_section = m.group(1).rstrip(".").strip()
            current_content = [line]
        else:
            current_content.append(line)

    if current_content:
        sections[current_section] = "\n".join(current_content).strip()

    # 提取元信息
    version_match = re.search(r'v(\d+\.\d+)', raw[:500])
    dna_match = re.search(r'DNA:\s*(#龍芯[^\n]+)', raw[:500])

    result = {
        "version": version_match.group(1) if version_match else "unknown",
        "dna": dna_match.group(1).strip() if dna_match else "",
        "confirm_code": CONFIRM_CODE,
        "section_count": len(sections),
        "sections": sections,
        "raw": raw,
        "size_bytes": len(raw.encode("utf-8")),
        "loaded_at": datetime.now(CST).isoformat(),
    }

    _memory_cache = result
    _cache_time = now
    return result


def get_identity_block() -> Dict[str, str]:
    """提取焊死身份块"""
    memory = parse_memory_md()
    section_1 = memory["sections"].get("§1", "")
    lines = section_1.split("\n")
    result = {}
    for line in lines:
        line = line.strip().lstrip("-").strip()
        if "UID9622" in line and "=" in line:
            result["identity"] = line
        elif "焊死" in line or "雷打不动" in line:
            result["sealed"] = line
        elif "唯一" in line and "主权" in line:
            result["sovereignty"] = line
    result["raw"] = section_1
    return result


def search_memory(query: str) -> List[Dict[str, Any]]:
    """全文搜索记忆"""
    memory = parse_memory_md()
    results = []
    q_lower = query.lower()

    for sec_name, content in memory["sections"].items():
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if q_lower in line.lower():
                # 取上下文
                start = max(0, i - 1)
                end = min(len(lines), i + 3)
                snippet = "\n".join(lines[start:end])
                results.append({
                    "section": sec_name,
                    "line_num": i + 1,
                    "snippet": snippet.strip(),
                    "match_line": line.strip(),
                })

    return results


# ═══════════════════════════════════════════════
# v1.2: 日志索引加载 & 搜索
# ═══════════════════════════════════════════════

def load_index(force: bool = False) -> Optional[Dict[str, Any]]:
    """加载日志索引（带缓存）"""
    global _index_cache, _index_time
    now = time.time()

    if not force and _index_cache and (now - _index_time < INDEX_CACHE_TTL):
        return _index_cache

    if not INDEX_FILE.exists():
        logger.warning("[index] 索引文件不存在，运行 python3 bin/lh_memory_indexer.py 构建")
        return None

    try:
        _index_cache = json.loads(INDEX_FILE.read_text(encoding='utf-8'))
        _index_time = now
        assert _index_cache is not None  # json.loads 永不为 None
        logger.info(f"[index] 加载成功: {_index_cache.get('total_files', 0)} 日志, "
                    f"{_index_cache.get('total_keywords', 0)} 关键词")
        return _index_cache
    except Exception as e:
        logger.error(f"[index] 加载失败: {e}")
        return None


def search_local_index(query: str, limit: int = 20) -> Optional[Dict[str, Any]]:
    """在本地日志索引中搜索"""
    idx = load_index()
    if not idx:
        return None

    entries = idx.get("entries", {})
    q_lower = query.lower()
    results = []

    for date_str, entry in entries.items():
        score = 0
        matched_kws = []

        # 关键词匹配
        for kw in entry.get("keywords", []):
            if q_lower in kw.lower() or kw.lower() in q_lower:
                score += 2
                matched_kws.append(kw)

        # 标题匹配
        if q_lower in entry.get("title", "").lower():
            score += 5
            matched_kws.append(entry["title"])

        # 摘要匹配
        if q_lower in entry.get("preview", "").lower():
            score += 1

        # DNA 匹配
        for dna in entry.get("dnas", []):
            if q_lower in dna.lower():
                score += 3
                matched_kws.append(f"[DNA]{dna[:40]}...")

        if score > 0:
            results.append({
                "date": date_str,
                "title": entry.get("title", ""),
                "file": entry.get("file", ""),
                "score": score,
                "matched_keywords": matched_kws[:5],
                "preview": entry.get("preview", "")[:300],
            })

    results.sort(key=lambda x: x["score"], reverse=True)

    return {
        "query": query,
        "total_results": len(results),
        "source": "log_index",
        "index_built": idx.get("built_at", ""),
        "results": results[:limit],
    }


# ═══════════════════════════════════════════════
# v1.2: Notion 后备大脑搜索
# ═══════════════════════════════════════════════

async def search_notion(query: str, limit: int = 10) -> Optional[Dict[str, Any]]:
    """
    在 Notion 数据库中搜索（异步 HTTP 调用）
    如果 NOTION_TOKEN 未配置 → 静默降级返回 None
    """
    if not NOTION_ENABLED:
        return None

    import httpx

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(
                f"https://api.notion.com/v1/databases/{NOTION_DB_ID}/query",
                headers=NOTION_HEADERS,
                json={
                    "page_size": 50,
                    "sorts": [{"timestamp": "last_edited_time", "direction": "descending"}],
                },
            )

            if resp.status_code != 200:
                logger.warning(f"[notion] 查询失败 HTTP {resp.status_code}: {resp.text[:200]}")
                return {"query": query, "total_results": 0, "source": "notion",
                        "error": f"HTTP {resp.status_code}", "results": []}

            data = resp.json()
            pages = data.get("results", [])
            results = []
            q_lower = query.lower()

            for page in pages:
                # 提取标题
                title_text = ""
                for prop_name in ("Name", "Title", "标题", "名称"):
                    try:
                        prop = page.get("properties", {}).get(prop_name, {})
                        if prop:
                            title_parts = prop.get("title", [])
                            title_text = "".join(p.get("plain_text", "") for p in title_parts)
                            if title_text:
                                break
                    except Exception:
                        continue

                # 标题匹配打分
                score = 0
                if q_lower in title_text.lower():
                    score += 10

                page_id = page.get("id", "")
                last_edited = page.get("last_edited_time", "")
                url = page.get("url", f"https://www.notion.so/{page_id.replace('-', '')}")

                # 尝试提取摘要属性
                summary = ""
                for sum_prop_name in ("Summary", "摘要", "Description", "描述"):
                    try:
                        sp = page.get("properties", {}).get(sum_prop_name, {})
                        if sp and sp.get("rich_text"):
                            summary = "".join(p.get("plain_text", "") for p in sp["rich_text"])
                            if summary:
                                break
                    except Exception:
                        continue

                # 摘要中也做匹配
                if q_lower in summary.lower():
                    score += 3

                # 如果标题命中，尝试拉页面内容前几行
                if score > 0 and not summary:
                    try:
                        blocks_resp = await client.get(
                            f"https://api.notion.com/v1/blocks/{page_id}/children",
                            headers=NOTION_HEADERS,
                            params={"page_size": 3},
                        )
                        if blocks_resp.status_code == 200:
                            bdata = blocks_resp.json()
                            for block in bdata.get("results", []):
                                bt = block.get("type", "")
                                if bt in ("paragraph", "heading_1", "heading_2", "heading_3"):
                                    rt = block.get(bt, {}).get("rich_text", [])
                                    txt = "".join(t.get("plain_text", "") for t in rt)
                                    if txt.strip():
                                        summary = txt.strip()[:300]
                                        break
                    except Exception:
                        pass

                if score > 0:
                    results.append({
                        "score": score,
                        "title": title_text,
                        "last_edited": last_edited,
                        "url": url,
                        "preview": summary[:300] if summary else title_text,
                        "source": "notion",
                    })

            results.sort(key=lambda x: x["score"], reverse=True)

            return {
                "query": query,
                "total_results": len(results),
                "source": "notion",
                "notion_enabled": True,
                "results": results[:limit],
            }

    except Exception as e:
        logger.warning(f"[notion] 搜索异常: {e}")
        return {"query": query, "total_results": 0, "source": "notion", "error": str(e),
                "results": []}


# ═══════════════════════════════════════════════
# v1.2: 三级级联搜索
# ═══════════════════════════════════════════════

async def search_cascaded(query: str, limit: int = 20) -> Dict[str, Any]:
    """
    三级级联搜索:
      L1: 本地 MEMORY.md 全文搜索（最快·最精确）
      L2: 日志索引搜索（覆盖25天日志·关键词+标题）
      L3: Notion 数据库搜索（后备大脑·标题匹配）
    """
    cascaded = {
        "query": query,
        "layers": {},
        "merged": [],
        "final_source": "local_memory.md",
    }

    # L1: 本地 MEMORY.md
    l1 = search_memory(query)
    cascaded["layers"]["L1_local"] = {"source": "local_memory.md", "count": len(l1)}
    for r in l1:
        r["layer"] = "L1"
        cascaded["merged"].append(r)

    # L2: 如果本地结果少，查日志索引
    need_deeper = len(cascaded["merged"]) < 3
    if need_deeper:
        l2 = search_local_index(query, limit)
        if l2 and l2["total_results"] > 0:
            cascaded["layers"]["L2_index"] = {"source": "log_index", "count": l2["total_results"]}
            cascaded["final_source"] = "log_index"
            for r in l2["results"]:
                r["layer"] = "L2"
                cascaded["merged"].append(r)
        else:
            cascaded["layers"]["L2_index"] = {"source": "log_index", "count": 0}
        need_deeper = len(cascaded["merged"]) < 3

    # L3: Notion 后备大脑
    if need_deeper:
        l3 = await search_notion(query, limit)
        if l3 and l3["total_results"] > 0:
            cascaded["layers"]["L3_notion"] = {"source": "notion", "count": l3["total_results"]}
            cascaded["final_source"] = "notion_fallback"
            for r in l3["results"]:
                r["layer"] = "L3"
                cascaded["merged"].append(r)
        else:
            cascaded["layers"]["L3_notion"] = {"source": "notion", "count": 0}

    # 去重
    seen = set()
    unique = []
    for r in cascaded["merged"]:
        key = (r.get("title", "") or r.get("section", "") or "") + \
              (r.get("preview", "") or r.get("snippet", ""))[:60]
        if key not in seen:
            seen.add(key)
            unique.append(r)

    cascaded["merged"] = unique[:limit]
    cascaded["total_merged"] = len(unique)

    return cascaded


def log_api_access(endpoint: str, client_ip: str, status: int):
    """记录 API 访问日志"""
    ts = datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {client_ip} → {endpoint} → {status}\n"
    with open(API_LOG_FILE, "a") as f:
        f.write(line)


# ═══════════════════════════════════════════════
# API 端点
# ═══════════════════════════════════════════════

# 🔥 v1.1 远程请求中间件：所有非本地请求强制身份验证
@app.middleware("http")
async def remote_auth_middleware(request: Request, call_next):
    """远程请求先过身份验证，本地请求直接放行"""
    client_ip = request.client.host if request.client else ""

    # 本地请求放行
    if client_ip in ("127.0.0.1", "::1", "localhost"):
        return await call_next(request)

    # 排除无需认证的路径
    public_paths = ("/docs", "/openapi.json", "/v1/memory/health", "/v1/memory/stats")
    if request.url.path in public_paths:
        return await call_next(request)

    # 🔥 远程请求：走身份联动验证
    if not verify_token(request):
        log_api_access(f"REMOTE-AUTH-DENIED {request.method} {request.url.path}", client_ip, 403)
        return JSONResponse(
            status_code=403,
            content={
                "error": "远程访问需要身份验证",
                "hint": "设置 $LH_MEMORY_TOKEN 或 ~/.longhun/.memory_token",
                "required_header": "X-API-Token",
            },
        )

    return await call_next(request)

@app.get("/v1/memory/health")
async def health_check(request: Request):
    """健康检查"""
    return await _health_response(request)


@app.get("/health")
async def health_check_root(request: Request):
    """统一健康检查入口（与/v1/memory/health等价）。"""
    return await _health_response(request)


async def _health_response(request: Request):
    memory = parse_memory_md()
    client_ip = request.client.host if request.client else "unknown"
    log_api_access("GET /health", client_ip, 200)

    token = get_or_create_token()
    return {
        "status": "🟢 记忆API在线",
        "service": "龍魂·统一记忆API v1.0",
        "memory_version": memory.get("version", "unknown"),
        "sections": memory.get("section_count", 0),
        "size_kb": round(memory.get("size_bytes", 0) / 1024, 1),
        "cache_ttl_sec": CACHE_TTL,
        "server_time": datetime.now(CST).isoformat(),
        "client_ip": client_ip,
    }


@app.get("/v1/memory")
async def get_full_memory(request: Request):
    """获取完整结构化记忆"""
    memory = parse_memory_md()
    client_ip = request.client.host if request.client else "unknown"
    log_api_access("GET /v1/memory", client_ip, 200)

    return JSONResponse(
        content=memory,
        headers={
            "X-Memory-Version": memory.get("version", "unknown"),
        }
    )


@app.get("/v1/memory/raw")
async def get_raw_memory(request: Request):
    """获取原始 MEMORY.md 全文"""
    memory = parse_memory_md()
    client_ip = request.client.host if request.client else "unknown"
    log_api_access("GET /v1/memory/raw", client_ip, 200)

    return PlainTextResponse(
        content=memory["raw"],
        headers={
            "X-Memory-Version": memory.get("version", "unknown"),
        }
    )


@app.get("/v1/memory/section/{section_name}")
async def get_section(section_name: str, request: Request):
    """获取指定记忆节"""
    memory = parse_memory_md()
    client_ip = request.client.host if request.client else "unknown"
    log_api_access(f"GET /v1/memory/section/{section_name}", client_ip, 200)

    # 支持 §1, 1, §1., s1 等格式
    clean = section_name.strip().lstrip("§Ss").strip(".")
    key = f"§{clean}"

    content = memory["sections"].get(key)
    if content is None:
        # 模糊匹配
        for k, v in memory["sections"].items():
            if clean in k:
                content = v
                key = k
                break

    if content is None:
        available = list(memory["sections"].keys())
        raise HTTPException(
            status_code=404,
            detail=f"节 '{section_name}' 不存在。可用节: {available}",
        )

    return {
        "section": key,
        "content": content,
        "version": memory.get("version"),
    }


@app.get("/v1/memory/identity")
async def get_identity(request: Request):
    """获取身份焊死块"""
    client_ip = request.client.host if request.client else "unknown"
    log_api_access("GET /v1/memory/identity", client_ip, 200)

    identity = get_identity_block()
    return {
        **identity,
        "confirm_code": CONFIRM_CODE,
        "note": "🔥 此块焊死·雷打不动·时间不可覆盖·不可删除·不可改写",
    }


@app.get("/v1/memory/search")
async def search(request: Request, q: str = "", mode: str = "cascaded"):
    """三级级联搜索记忆（本地→索引→Notion）
    mode: cascaded(默认) | local(仅本地) | notion_direct(仅Notion)
    """
    if not q or len(q.strip()) < 2:
        raise HTTPException(status_code=400, detail="搜索词至少2个字符")

    client_ip = request.client.host if request.client else "unknown"

    if mode == "notion_direct":
        log_api_access(f"GET /v1/memory/search?q={q[:50]}&mode=notion", client_ip, 200)
        result = await search_notion(q)
        return result if result else {"query": q, "total_results": 0, "source": "notion", "results": []}

    if mode == "local":
        log_api_access(f"GET /v1/memory/search?q={q[:50]}&mode=local", client_ip, 200)
        results = search_memory(q)
        return {
            "query": q,
            "total_results": len(results),
            "source": "local_memory.md",
            "results": results[:20],
        }

    # 默认: cascaded (三级级联)
    log_api_access(f"GET /v1/memory/search?q={q[:50]}&mode=cascaded", client_ip, 200)
    result = await search_cascaded(q)
    return result


@app.get("/v1/memory/anchors")
async def get_anchors(request: Request):
    """获取锚清单"""
    memory = parse_memory_md()
    client_ip = request.client.host if request.client else "unknown"
    log_api_access("GET /v1/memory/anchors", client_ip, 200)

    section_13 = memory["sections"].get("§13", "")
    return {
        "section": "§13 全锚清单",
        "content": section_13,
    }


@app.get("/v1/memory/stats")
async def get_stats(request: Request):
    """统计信息"""
    memory = parse_memory_md()
    client_ip = request.client.host if request.client else "unknown"
    log_api_access("GET /v1/memory/stats", client_ip, 200)

    # 统计每日日志
    daily_count = 0
    if DAILY_LOG_DIR.exists():
        daily_count = len(list(DAILY_LOG_DIR.glob("20*.md")))

    # 统计各节大小
    section_sizes = {
        k: len(v.encode("utf-8"))
        for k, v in memory["sections"].items()
    }

    # 日志读取
    try:
        log_size = API_LOG_FILE.stat().st_size if API_LOG_FILE.exists() else 0
        with open(API_LOG_FILE, "r") as f:
            log_lines = f.readlines()
        recent_logs = log_lines[-20:] if log_lines else []
    except Exception:
        log_size = 0
        recent_logs = []

    return {
        "memory_version": memory.get("version", "unknown"),
        "sections": memory.get("section_count", 0),
        "total_size_kb": round(memory.get("size_bytes", 0) / 1024, 1),
        "section_sizes_bytes": section_sizes,
        "daily_logs": daily_count,
        "cache_ttl_sec": CACHE_TTL,
        "api_log_size_kb": round(log_size / 1024, 1),
        "recent_api_logs": [l.strip() for l in recent_logs],
        "server_uptime": datetime.now(CST).isoformat(),
    }


# ═══════════════════════════════════════════════
# v1.2: 日志索引端点
# ═══════════════════════════════════════════════

@app.get("/v1/memory/index")
async def get_index(request: Request):
    """日志索引状态"""
    client_ip = request.client.host if request.client else "unknown"
    log_api_access("GET /v1/memory/index", client_ip, 200)

    idx = load_index()
    if not idx:
        return {
            "status": "not_built",
            "hint": "运行 python3 bin/lh_memory_indexer.py 构建索引",
            "index_file": str(INDEX_FILE),
        }

    dates = sorted(idx.get("entries", {}).keys())
    top_kw = sorted(idx.get("keyword_index", {}).items(),
                    key=lambda x: len(x[1]), reverse=True)[:15]

    return {
        "status": "active",
        "version": idx.get("version", ""),
        "built_at": idx.get("built_at", ""),
        "total_files": idx.get("total_files", 0),
        "total_keywords": idx.get("total_keywords", 0),
        "total_dnas": idx.get("total_dnas", 0),
        "date_range": [dates[0], dates[-1]] if dates else [],
        "top_keywords": {kw: len(dates) for kw, dates in top_kw},
        "index_file": str(INDEX_FILE),
        "notion_enabled": NOTION_ENABLED,
    }


@app.post("/v1/memory/reload")
async def reload_index(request: Request):
    """强制重载日志索引（仅本地调用）"""
    client_ip = request.client.host if request.client else "unknown"

    # 安全检查：仅本地
    if client_ip not in ("127.0.0.1", "::1", "localhost"):
        log_api_access("POST /v1/memory/reload", client_ip, 403)
        raise HTTPException(status_code=403, detail="仅本地可重载索引")

    log_api_access("POST /v1/memory/reload", client_ip, 200)

    # 强制重建
    global _index_cache, _index_time
    _index_cache = None
    _index_time = 0

    idx = load_index(force=True)
    if idx:
        return {
            "status": "reloaded",
            "total_files": idx.get("total_files", 0),
            "total_keywords": idx.get("total_keywords", 0),
            "built_at": idx.get("built_at", ""),
        }
    else:
        return {
            "status": "rebuild_needed",
            "hint": "运行 python3 bin/lh_memory_indexer.py --force",
        }


@app.post("/v1/memory/daily")
async def append_daily_log(entry: DailyLogEntry, request: Request):
    """追加今日日志（需认证）"""
    # 认证
    client_host = request.client.host if request.client else ""
    if client_host not in ("127.0.0.1", "::1", "localhost"):
        if not verify_token(request, entry.token):
            log_api_access("POST /v1/memory/daily", client_host, 403)
            raise HTTPException(status_code=403, detail="认证失败。需要有效 Token。")

    if not entry.content or len(entry.content.strip()) < 5:
        raise HTTPException(status_code=400, detail="日志内容至少5个字符")

    # 写入当日日志文件
    today = datetime.now(CST).strftime("%Y-%m-%d")
    daily_file = DAILY_LOG_DIR / f"{today}.md"

    ts = datetime.now(CST).strftime("%H:%M:%S")
    log_entry = f"\n[{ts}] {entry.content.strip()}\n"

    # 追加写入
    with open(daily_file, "a", encoding="utf-8") as f:
        f.write(log_entry)

    log_api_access("POST /v1/memory/daily", client_host, 200)

    return {
        "status": "✅ 已追加",
        "date": today,
        "time": ts,
        "file": str(daily_file),
    }


@app.get("/v1/memory/daily/{date_str}")
async def get_daily_log(date_str: str, request: Request):
    """读取指定日期的日志"""
    client_host = request.client.host if request.client else "unknown"
    log_api_access(f"GET /v1/memory/daily/{date_str}", client_host, 200)

    daily_file = DAILY_LOG_DIR / f"{date_str}.md"
    if not daily_file.exists():
        raise HTTPException(status_code=404, detail=f"日期 {date_str} 的日志不存在")

    content = daily_file.read_text(encoding="utf-8")
    return {
        "date": date_str,
        "content": content,
        "size_bytes": len(content.encode("utf-8")),
    }


@app.get("/v1/memory/archive/status")
async def get_archive_status(request: Request):
    """不动点记忆归档状态"""
    client_ip = request.client.host if request.client else "unknown"
    log_api_access("GET /v1/memory/archive/status", client_ip, 200)

    if MemoryArchive is None:
        return {
            "status": "unavailable",
            "reason": "归档引擎未加载",
        }

    archive = MemoryArchive()
    return archive.status()


@app.post("/v1/memory/archive/ingest")
async def archive_ingest(entry: ArchiveIngestEntry, request: Request):
    """摄入一条记忆到不动点归档引擎（需认证）"""
    client_host = request.client.host if request.client else ""
    if client_host not in ("127.0.0.1", "::1", "localhost"):
        if not verify_token(request, entry.token):
            log_api_access("POST /v1/memory/archive/ingest", client_host, 403)
            raise HTTPException(status_code=403, detail="认证失败。需要有效 Token。")

    if not entry.text or len(entry.text.strip()) < 5:
        raise HTTPException(status_code=400, detail="归档文本至少5个字符")

    if MemoryArchive is None:
        raise HTTPException(status_code=503, detail="归档引擎未加载")

    archive = MemoryArchive()
    result = archive.ingest(
        entry.text,
        source=entry.source,
        tags=entry.tags,
        context={"client_ip": client_host, "via": "memory_api"},
    )

    log_api_access("POST /v1/memory/archive/ingest", client_host, 200)
    return {
        "status": result.get("status"),
        "state": result.get("state"),
        "score": result.get("score"),
        "dna": result.get("dna"),
        "reasons": result.get("reasons", []),
        "reference": result.get("reference"),
    }


@app.get("/v1/memory/token")
async def get_token_info(request: Request):
    """获取 Token 信息（仅本地）"""
    client_host = request.client.host if request.client else ""
    if client_host not in ("127.0.0.1", "::1", "localhost"):
        raise HTTPException(status_code=403, detail="仅本地访问")

    token = get_or_create_token()
    return {
        "token": token,
        "note": "将此 Token 配置到远程 AI 的请求头 X-API-Token 中",
        "usage": "curl -H 'X-API-Token: <token>' http://IP:8770/v1/memory",
        "warning": "🔴 此 Token 仅在本地显示。远程访问从不返回 Token。",
    }


# ═══════════════════════════════════════════════
# 中间件：全局日志
# ═══════════════════════════════════════════════

@app.middleware("http")
async def add_memory_headers(request: Request, call_next):
    """为所有响应添加记忆版本头"""
    response = await call_next(request)
    memory = parse_memory_md()
    response.headers["X-Memory-API"] = "Longhun-Unified-Memory-API-v1.0"
    response.headers["X-Memory-Version"] = memory.get("version", "unknown")
    response.headers["X-Sovereignty"] = "UID9622-LongXinBeiChen-CN-Sovereign"
    return response


# ═══════════════════════════════════════════════
# 启动入口
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    import argparse

    parser = argparse.ArgumentParser(description="龍魂·统一记忆 API")
    parser.add_argument("--port", type=int, default=8771, help="服务端口 (默认: 8771)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="绑定地址 (默认: 127.0.0.1)")
    args = parser.parse_args()

    # 首次启动时生成 token
    token = get_or_create_token()
    token_display = token[:8] + "..." if args.host != "127.0.0.1" else token

    # v1.2: 启动时预加载日志索引
    idx_status = "⏳"
    idx_info = ""
    try:
        idx = load_index()
        if idx:
            idx_status = "✅"
            idx_info = f"{idx.get('total_files', 0)}日志·{idx.get('total_keywords', 0)}关键词"
        else:
            idx_status = "⏳"
            idx_info = "需构建"
    except Exception:
        idx_status = "⚠️ "
        idx_info = "加载失败"

    # v1.2: Notion 状态
    notion_status = "✅" if NOTION_ENABLED else "⏳"

    print(f"""
╔══════════════════════════════════════════════╗
║  龍魂·统一记忆 API v1.2                        ║
║  DNA: #龍芯⚡️丙午·乙未·辛酉·井-MEMORY-API-v1.2  ║
║  主权人: UID9622·龍芯北辰·中国自主可控            ║
╠══════════════════════════════════════════════╣
║  端口: {args.port:<5}  地址: {args.host:<20} ║
║  Token: {token_display:<35} ║
║  CONFIRM: {CONFIRM_CODE[:40]}... ║
╠══════════════════════════════════════════════╣
║  🧠 索引: {idx_status} {idx_info:<37} ║
║  ☁️  Notion后备: {notion_status:<43} ║
╠══════════════════════════════════════════════╣
║  端点:                                        ║
║  GET  /v1/memory              — 完整记忆JSON      ║
║  GET  /v1/memory/raw          — 原始MEMORY.md全文  ║
║  GET  /v1/memory/identity     — 身份焊死块        ║
║  GET  /v1/memory/search?q=xxx — 三级搜索🧠        ║
║  GET  /v1/memory/index        — 索引状态📇         ║
║  POST /v1/memory/reload       — 重载索引🔄         ║
║  GET  /v1/memory/health       — 健康检查          ║
║  POST /v1/memory/daily        — 追加日志(需认证)   ║
║  GET  /v1/memory/archive/status  — 归档状态📦     ║
║  POST /v1/memory/archive/ingest  — 记忆归档(需认证) ║
╠══════════════════════════════════════════════╣
║  搜索策略: 本地MEMORY.md → 日志索引 → Notion  ║
║  所有 AI（不论国家/模型）统一此入口。             ║
╚══════════════════════════════════════════════╝
""")

    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        log_level="info",
        access_log=False,
    )
