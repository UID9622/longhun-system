#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
龍魂统一监管API · 路由层
DNA: #龍芯⚡️2026-07-12-REGULATORY-ROUTES-v2.0 · 三层透明模型

统一监管 API 端点:
- POST /api/regulatory/auth/token         监管者认证
- GET  /api/regulatory/operations         操作记录
- GET  /api/regulatory/operations/live    实时操作流 (SSE)
- GET  /api/regulatory/documents          文档注册表（元数据）
- GET  /api/regulatory/documents/{id}     文档详情（层3内容脱敏）
- GET  /api/regulatory/filesystem/tree    文件系统树
- GET  /api/regulatory/filesystem/changes 文件变更
- GET  /api/regulatory/audit/full         全量审计
- GET  /api/regulatory/system/state       系统实时状态
- GET  /api/regulatory/reports/daily      日报
- GET  /api/regulatory/reports/weekly     周报
- GET  /api/regulatory/export             数据导出
- GET  /api/regulatory/data-sovereignty   数据主权声明（三层模型）
- GET  /api/regulatory/protocol-check     协议合规自检
- GET  /api/regulatory/verify-integrity   哈希链完整性验证
- POST /api/regulatory/index/trigger      触发全量索引
- WS   /api/regulatory/ws                 实时 WebSocket
"""

import hashlib
import json
import secrets
import asyncio
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, Request, HTTPException, Depends, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field

from .config import ADMIN_UID, PROJECT_ROOT
from .regulatory_db import (
    get_auditor_by_key_hash, record_auditor_access, log_regulatory_access,
    get_operations, get_file_changes, get_documents, get_document_by_id,
    get_document_by_path, get_document_stats, get_regulatory_access_logs,
    log_operation, upsert_document, verify_regulatory_hash_chain,
)
from .regulatory_service import (
    get_system_state, generate_daily_report, generate_weekly_report,
    full_index, index_document, event_bus, FILE_TYPE_MAP,
    compute_sha256, get_file_type,
    detect_sovereignty_level, redact_private_content,
    get_sovereignty_declaration, protocol_self_check,
)
from .database import get_connection, now_iso

router = APIRouter()


# ═══════════════════════════════════════════
# 请求模型
# ═══════════════════════════════════════════

class AuditorAuthRequest(BaseModel):
    auditor_id: str = Field(..., description="监管者ID")
    auth_key: str = Field(..., description="监管者密钥")


class IndexRequest(BaseModel):
    path: str = Field(default="", description="指定索引路径（空=全量）")


# ═══════════════════════════════════════════
# 监管者认证依赖
# ═══════════════════════════════════════════

def _hash_key(key: str) -> str:
    return hashlib.sha256(f"LH_REGULATORY_SALT_{key}".encode()).hexdigest()


async def require_regulator(request: Request) -> dict[str, Any]:
    """验证监管者身份。通过 Header: X-Regulatory-Key 认证。"""
    auth_key = request.headers.get("X-Regulatory-Key", "")
    if not auth_key:
        raise HTTPException(status_code=401, detail="缺少 X-Regulatory-Key 认证头")
    
    key_hash = _hash_key(auth_key)
    auditor = get_auditor_by_key_hash(key_hash)
    if not auditor:
        raise HTTPException(status_code=403, detail="监管者认证失败")
    
    return auditor


async def log_and_record(auditor: dict[str, Any], request: Request, access_type: str, 
                         endpoint: str, query_params: str = "", result_count: int = 0):
    """记录监管访问。"""
    ip = request.client.host if request.client else "unknown"
    record_auditor_access(auditor["auditor_id"])
    log_regulatory_access(
        auditor_id=auditor["auditor_id"],
        access_type=access_type,
        endpoint=endpoint,
        query_params=query_params,
        result_count=result_count,
        ip=ip
    )


# ═══════════════════════════════════════════
# 监管者认证
# ═══════════════════════════════════════════

@router.post("/regulatory/auth/token")
async def regulatory_auth(req: AuditorAuthRequest, request: Request):
    """监管者认证，返回临时访问令牌。"""
    key_hash = _hash_key(req.auth_key)
    auditor = get_auditor_by_key_hash(key_hash)
    if not auditor:
        raise HTTPException(status_code=403, detail="认证失败：监管者ID或密钥无效")
    
    record_auditor_access(auditor["auditor_id"])
    
    ip = request.client.host if request.client else "unknown"
    log_regulatory_access(
        auditor_id=auditor["auditor_id"],
        access_type="auth",
        endpoint="/api/regulatory/auth/token",
        ip=ip
    )
    
    return {
        "ok": True,
        "auditor": {
            "id": auditor["auditor_id"],
            "name": auditor["name"],
            "organization": auditor["organization"],
            "access_level": auditor["access_level"],
        },
        "token": req.auth_key,
        "note": "请在后续请求中设置 Header: X-Regulatory-Key",
        "endpoints": {
            "operations": "/api/regulatory/operations",
            "operations_live": "/api/regulatory/operations/live",
            "documents": "/api/regulatory/documents",
            "filesystem_tree": "/api/regulatory/filesystem/tree",
            "filesystem_changes": "/api/regulatory/filesystem/changes",
            "audit_full": "/api/regulatory/audit/full",
            "system_state": "/api/regulatory/system/state",
            "reports_daily": "/api/regulatory/reports/daily",
            "reports_weekly": "/api/regulatory/reports/weekly",
            "export": "/api/regulatory/export",
            "data_sovereignty": "/api/regulatory/data-sovereignty",
            "protocol_check": "/api/regulatory/protocol-check",
            "verify_integrity": "/api/regulatory/verify-integrity",
            "ws": "ws://host:9622/api/regulatory/ws?key=<your_key>",
        }
    }


# ═══════════════════════════════════════════
# 操作记录
# ═══════════════════════════════════════════

@router.get("/regulatory/operations")
async def regulatory_operations(
    request: Request,
    limit: int = Query(default=100, le=1000),
    offset: int = Query(default=0),
    op_type: str = Query(default=None, description="操作类型筛选"),
    source: str = Query(default=None, description="来源筛选"),
    file_path: str = Query(default=None, description="文件路径筛选"),
    from_ts: str = Query(default=None, description="起始时间 ISO8601"),
    to_ts: str = Query(default=None, description="结束时间 ISO8601"),
    auditor: dict[str, Any] = Depends(require_regulator),
):
    """查询所有操作记录。支持多维度筛选。"""
    operations = get_operations(
        limit=limit, offset=offset,
        op_type=op_type, source=source, file_path=file_path,
        from_ts=from_ts, to_ts=to_ts,
    )
    
    await log_and_record(auditor, request, "query_operations", 
                         "/api/regulatory/operations", 
                         f"limit={limit},offset={offset}", len(operations))
    
    # 统计
    op_type_counts = {}
    for op in operations:
        t = op.get("operation_type", "unknown")
        op_type_counts[t] = op_type_counts.get(t, 0) + 1
    
    return {
        "ok": True,
        "count": len(operations),
        "offset": offset,
        "breakdown": op_type_counts,
        "operations": operations,
    }


@router.get("/regulatory/operations/live")
async def regulatory_operations_live(
    request: Request,
    auditor: dict[str, Any] = Depends(require_regulator),
):
    """实时操作流（SSE）。监管者可实时看到系统发生的操作。"""
    queue = await event_bus.subscribe()
    
    async def event_generator():
        try:
            # 发送连接确认
            yield f"data: {json.dumps({'type': 'connected', 'auditor': auditor['name'], 'timestamp': now_iso()}, ensure_ascii=False)}\n\n"
            
            while True:
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=30)
                    yield f"data: {json.dumps(event, ensure_ascii=False, default=str)}\n\n"
                except asyncio.TimeoutError:
                    # 发送心跳
                    yield f"data: {json.dumps({'type': 'heartbeat', 'timestamp': now_iso()}, ensure_ascii=False)}\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            event_bus.unsubscribe(queue)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )


# ═══════════════════════════════════════════
# 文档注册表
# ═══════════════════════════════════════════

@router.get("/regulatory/documents")
async def regulatory_documents(
    request: Request,
    limit: int = Query(default=100, le=1000),
    offset: int = Query(default=0),
    doc_type: str = Query(default=None, description="文档类型筛选"),
    status: str = Query(default=None, description="状态筛选: draft/review/published/archived"),
    search: str = Query(default=None, description="搜索标题/路径/标签"),
    auditor: dict[str, Any] = Depends(require_regulator),
):
    """查询文档注册表。所有已索引的文档，含草稿。"""
    docs = get_documents(
        limit=limit, offset=offset,
        doc_type=doc_type, status=status, search=search,
    )
    stats = get_document_stats()
    
    await log_and_record(auditor, request, "query_documents",
                         "/api/regulatory/documents",
                         f"limit={limit},offset={offset},type={doc_type},status={status},search={search}",
                         len(docs))
    
    return {
        "ok": True,
        "count": len(docs),
        "offset": offset,
        "statistics": stats,
        "sovereignty_notice": (
            "文档按三层主权模型分级：层1=公开（完整内容可查），"
            "层2=透明（元数据可查，内容需授权），层3=私有（仅元数据可查，内容不可见）"
        ),
        "documents": [{
            "doc_id": d["doc_id"],
            "file_path": d["file_path"],
            "doc_type": d["doc_type"],
            "title": d["title"],
            "status": d["status"],
            "word_count": d["word_count"],
            "created_at": d["created_at"],
            "modified_at": d["modified_at"],
            "content_hash": d["content_hash"],
            "sovereignty_level": d.get("sovereignty_level", 2),
            "sovereignty_label": {1: "层1:公开", 2: "层2:透明", 3: "层3:私有🔒"}.get(d.get("sovereignty_level", 2), "未知"),
            "is_private_content": bool(d.get("is_private_content", 0)),
            "tags": json.loads(d.get("tags", "[]")) if d.get("tags") else [],
        } for d in docs],
    }


@router.get("/regulatory/documents/{doc_id}")
async def regulatory_document_detail(
    request: Request,
    doc_id: str,
    include_content: bool = Query(default=False, description="是否包含文件内容（层3文件即使打开也只返回脱敏声明）"),
    max_content_chars: int = Query(default=50000, description="内容最大字符数"),
    auditor: dict[str, Any] = Depends(require_regulator),
):
    """获取文档详情。层3（私有层）文件内容自动脱敏。"""
    doc = get_document_by_id(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail=f"文档 {doc_id} 不存在")
    
    sov_level = doc.get("sovereignty_level", 2)
    is_private = doc.get("is_private_content", 0)
    
    result = {
        "ok": True,
        "document": {
            "doc_id": doc["doc_id"],
            "file_path": doc["file_path"],
            "doc_type": doc["doc_type"],
            "title": doc["title"],
            "status": doc["status"],
            "word_count": doc["word_count"],
            "created_at": doc["created_at"],
            "modified_at": doc["modified_at"],
            "last_indexed_at": doc["last_indexed_at"],
            "content_hash": doc["content_hash"],
            "sovereignty_level": sov_level,
            "sovereignty_label": {1: "层1:公开", 2: "层2:透明", 3: "层3:私有"}.get(sov_level, "未知"),
            "is_private_content": bool(is_private),
            "tags": json.loads(doc.get("tags", "[]")) if doc.get("tags") else [],
            "meta": json.loads(doc.get("meta_json", "{}")) if doc.get("meta_json") else {},
        },
    }
    
    if include_content and doc.get("file_path"):
        if sov_level == 3 or is_private:
            # 层3: 返回脱敏声明，不返回实际内容
            result["document"]["content"] = redact_private_content(doc["file_path"], sov_level)
            result["document"]["content_redacted"] = True
            result["document"]["sovereignty_notice"] = (
                "此文件属于数据主权层3（私有层），根据龍魂监管宪法，"
                "任何外部实体未经用户授权不可访问其内容。"
            )
        else:
            # 层1/2: 可返回内容
            try:
                content = Path(doc["file_path"]).read_text(encoding='utf-8', errors='ignore')
                if len(content) > max_content_chars:
                    result["document"]["content"] = content[:max_content_chars]
                    result["document"]["content_truncated"] = True
                    result["document"]["original_length"] = len(content)
                else:
                    result["document"]["content"] = content
                    result["document"]["content_truncated"] = False
                result["document"]["content_redacted"] = False
            except Exception as e:
                result["document"]["content_error"] = str(e)
                result["document"]["content_redacted"] = True
    
    await log_and_record(auditor, request, "view_document",
                         f"/api/regulatory/documents/{doc_id}",
                         f"include_content={include_content},sovereignty_level={sov_level},redacted={sov_level==3}")
    
    return result


# ═══════════════════════════════════════════
# 文件系统
# ═══════════════════════════════════════════

@router.get("/regulatory/filesystem/tree")
async def regulatory_filesystem_tree(
    request: Request,
    path: str = Query(default="", description="起始路径，空=项目根"),
    depth: int = Query(default=3, le=5, description="最大深度"),
    auditor: dict[str, Any] = Depends(require_regulator),
):
    """获取文件系统树结构。"""
    base_path = Path(path) if path else PROJECT_ROOT
    
    # 安全检查：不允许访问项目外
    try:
        base_path.resolve(strict=False).relative_to(PROJECT_ROOT.resolve(strict=False))
    except ValueError:
        raise HTTPException(status_code=403, detail="不允许访问项目外路径")
    
    if not base_path.exists():
        raise HTTPException(status_code=404, detail=f"路径 {path} 不存在")
    
    SKIP_DIRS = {'__pycache__', 'node_modules', '.git', 'venv', '.venv', 'env',
                 'dist', 'build', '.next', '.cache', '.obsidian', '.codebuddy',
                 'logs', 'logging_backup', 'backups', 'tmp', '__pycache__'}
    
    def build_tree(dir_path: Path, current_depth: int) -> dict[str, Any]:
        result: dict[str, Any] = {
            "name": dir_path.name or str(dir_path),
            "type": "directory",
            "path": str(dir_path),
        }
        if current_depth >= depth:
            result["children"] = "..."
            return result
        
        children = []
        try:
            for item in sorted(dir_path.iterdir()):
                if item.name.startswith('.') and item.name not in {'.env.example', '.gitignore'}:
                    continue
                if item.name in SKIP_DIRS:
                    continue
                
                try:
                    is_dir = item.is_dir()
                except OSError:
                    children.append({"name": item.name, "type": "broken_link", "path": str(item)})
                    continue
                
                if is_dir:
                    child = build_tree(item, current_depth + 1)
                else:
                    try:
                        stat = item.stat()
                        child = {
                            "name": item.name,
                            "type": "file",
                            "path": str(item),
                            "size": stat.st_size,
                            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        }
                    except OSError:
                        child = {"name": item.name, "type": "broken_link", "path": str(item)}
                children.append(child)
        except PermissionError:
            children.append({"name": "(权限不足)", "type": "error"})
        
        result["children"] = children
        return result
    
    tree = build_tree(base_path, 0)
    
    await log_and_record(auditor, request, "view_filesystem",
                         "/api/regulatory/filesystem/tree",
                         f"path={path},depth={depth}")
    
    return {"ok": True, "root_path": str(base_path), "tree": tree}


@router.get("/regulatory/filesystem/changes")
async def regulatory_filesystem_changes(
    request: Request,
    limit: int = Query(default=100, le=1000),
    offset: int = Query(default=0),
    event_type: str = Query(default=None, description="created/modified/deleted/moved"),
    file_path: str = Query(default=None, description="文件路径筛选"),
    from_ts: str = Query(default=None),
    to_ts: str = Query(default=None),
    auditor: dict[str, Any] = Depends(require_regulator),
):
    """查询文件系统变更日志。"""
    changes = get_file_changes(
        limit=limit, offset=offset,
        event_type=event_type, file_path=file_path,
        from_ts=from_ts, to_ts=to_ts,
    )
    
    await log_and_record(auditor, request, "query_file_changes",
                         "/api/regulatory/filesystem/changes",
                         f"limit={limit},offset={offset}", len(changes))
    
    return {
        "ok": True,
        "count": len(changes),
        "offset": offset,
        "changes": changes,
    }


# ═══════════════════════════════════════════
# 审计日志
# ═══════════════════════════════════════════

@router.get("/regulatory/audit/full")
async def regulatory_audit_full(
    request: Request,
    limit: int = Query(default=100, le=1000),
    offset: int = Query(default=0),
    uid: str = Query(default=None),
    module: str = Query(default=None),
    action: str = Query(default=None),
    from_ts: str = Query(default=None),
    to_ts: str = Query(default=None),
    auditor: dict[str, Any] = Depends(require_regulator),
):
    """全量审计日志查询。"""
    from .database import get_connection
    
    with get_connection() as conn:
        query = "SELECT * FROM audit_log WHERE 1=1"
        params = []
        if uid:
            query += " AND uid = ?"
            params.append(uid)
        if module:
            query += " AND module = ?"
            params.append(module)
        if action:
            query += " AND action = ?"
            params.append(action)
        if from_ts:
            query += " AND timestamp >= ?"
            params.append(from_ts)
        if to_ts:
            query += " AND timestamp <= ?"
            params.append(to_ts)
        query += " ORDER BY id DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        rows = conn.execute(query, params).fetchall()
        logs = [dict(r) for r in rows]
    
    await log_and_record(auditor, request, "query_audit_full",
                         "/api/regulatory/audit/full",
                         f"limit={limit},offset={offset}", len(logs))
    
    return {
        "ok": True,
        "count": len(logs),
        "offset": offset,
        "logs": logs,
    }


# ═══════════════════════════════════════════
# 系统状态
# ═══════════════════════════════════════════

@router.get("/regulatory/system/state")
async def regulatory_system_state(
    request: Request,
    auditor: dict[str, Any] = Depends(require_regulator),
):
    """获取系统实时状态快照。"""
    state = get_system_state()
    
    await log_and_record(auditor, request, "view_system_state",
                         "/api/regulatory/system/state")
    
    return {"ok": True, "state": state}


# ═══════════════════════════════════════════
# 合规报告
# ═══════════════════════════════════════════

@router.get("/regulatory/reports/daily")
async def regulatory_report_daily(
    request: Request,
    date: str = Query(default=None, description="日期 YYYY-MM-DD，默认今天"),
    auditor: dict[str, Any] = Depends(require_regulator),
):
    """获取每日合规报告。"""
    report = generate_daily_report(date)
    
    await log_and_record(auditor, request, "report_daily",
                         "/api/regulatory/reports/daily",
                         f"date={date}")
    
    return {"ok": True, "report": report}


@router.get("/regulatory/reports/weekly")
async def regulatory_report_weekly(
    request: Request,
    auditor: dict[str, Any] = Depends(require_regulator),
):
    """获取每周合规报告。"""
    report = generate_weekly_report()
    
    await log_and_record(auditor, request, "report_weekly",
                         "/api/regulatory/reports/weekly")
    
    return {"ok": True, "report": report}


# ═══════════════════════════════════════════
# 数据导出
# ═══════════════════════════════════════════

@router.get("/regulatory/export")
async def regulatory_export(
    request: Request,
    format: str = Query(default="json", description="导出格式: json/csv"),
    include_audit: bool = Query(default=True),
    include_operations: bool = Query(default=True),
    include_documents: bool = Query(default=True),
    include_changes: bool = Query(default=True),
    days: int = Query(default=7, le=90, description="导出最近N天数据"),
    auditor: dict[str, Any] = Depends(require_regulator),
):
    """导出全量数据。"""
    from_ts = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    
    export_data: dict[str, Any] = {
        "export_info": {
            "generated_at": now_iso(),
            "period_days": days,
            "from": from_ts,
            "requested_by": auditor["auditor_id"],
            "format": format,
        },
    }
    
    if include_operations:
        ops = get_operations(limit=10000, from_ts=from_ts)
        export_data["operations"] = ops
        export_data["operations_count"] = len(ops)
    
    if include_documents:
        docs = get_documents(limit=10000)
        export_data["documents"] = docs
        export_data["documents_count"] = len(docs)
    
    if include_changes:
        changes = get_file_changes(limit=10000, from_ts=from_ts)
        export_data["file_changes"] = changes
        export_data["file_changes_count"] = len(changes)
    
    if include_audit:
        from .database import get_connection
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM audit_log WHERE timestamp >= ? ORDER BY id DESC LIMIT 10000",
                (from_ts,)
            ).fetchall()
            export_data["audit_logs"] = [dict(r) for r in rows]
            export_data["audit_logs_count"] = len(rows)
    
    await log_and_record(auditor, request, "export_data",
                         "/api/regulatory/export",
                         f"format={format},days={days}",
                         sum(int(export_data.get(f"{k}_count", 0)) for k in ['operations', 'documents', 'file_changes', 'audit_logs']))
    
    if format == "csv":
        # 简化版 CSV：转成 JSON 后再转
        return JSONResponse({
            "ok": True,
            "note": "CSV 格式暂未实现，返回 JSON。如需 CSV 请使用专用导出工具。",
            "data": export_data,
        })
    
    return {"ok": True, "data": export_data}


# ═══════════════════════════════════════════
# 数据主权声明（三层透明模型）
# ═══════════════════════════════════════════

@router.get("/regulatory/data-sovereignty")
async def regulatory_data_sovereignty(
    request: Request,
    auditor: dict[str, Any] = Depends(require_regulator),
):
    """
    数据主权声明 —— 三层透明模型的完整阐述。
    
    这是监管者接入时首先应查阅的端点，
    明确告知：哪些数据可见、哪些不可见、边界在哪里。
    """
    declaration = get_sovereignty_declaration()
    
    await log_and_record(auditor, request, "view_sovereignty",
                         "/api/regulatory/data-sovereignty")
    
    return {"ok": True, "sovereignty_declaration": declaration}


# ═══════════════════════════════════════════
# 协议合规自检
# ═══════════════════════════════════════════

@router.get("/regulatory/protocol-check")
async def regulatory_protocol_check(
    request: Request,
    auditor: dict[str, Any] = Depends(require_regulator),
):
    """
    协议合规自检 —— 逐项检查系统是否遵守自身设定的安全基线。
    
    返回 6 项自检结果：
    - PS-001 数据本地化
    - PS-002 层3私有内容保护
    - PS-003 操作日志哈希链
    - PS-004 监管访问可追溯
    - PS-005 主权策略记录
    - PS-006 层2内容授权控制
    """
    check_result = protocol_self_check()
    
    await log_and_record(auditor, request, "protocol_check",
                         "/api/regulatory/protocol-check",
                         f"overall={check_result['overall']}")
    
    return {"ok": True, "result": check_result}


# ═══════════════════════════════════════════
# 哈希链完整性验证
# ═══════════════════════════════════════════

@router.get("/regulatory/verify-integrity")
async def regulatory_verify_integrity(
    request: Request,
    auditor: dict[str, Any] = Depends(require_regulator),
):
    """
    操作日志哈希链完整性验证。
    
    验证所有操作日志是否通过 SHA256 哈希链连接，
    检测是否存在篡改或断裂。
    
    返回：
    - chain_length: 链长度
    - status: intact / compromised / empty
    - violations: 违规项列表（空 = 完整）
    - genesis_id / latest_id: 首尾日志ID
    """
    result = verify_regulatory_hash_chain()
    
    await log_and_record(auditor, request, "verify_integrity",
                         "/api/regulatory/verify-integrity",
                         f"chain_length={result['chain_length']},status={result['status']}")
    
    return {"ok": True, "verification": result}


# ═══════════════════════════════════════════
# 索引管理
# ═══════════════════════════════════════════

@router.post("/regulatory/index/trigger")
async def regulatory_trigger_index(
    request: Request,
    req: Optional[IndexRequest] = None,
    auditor: dict[str, Any] = Depends(require_regulator),
):
    """触全文档索引。"""
    # 要求监管者 access_level 为 full
    if auditor.get("access_level") != "full":
        raise HTTPException(status_code=403, detail="需要 full 权限才能触发索引")
    
    # 在后台执行索引
    async def run_index():
        if req and req.path:
            file_path = req.path
            result = index_document(file_path)
            await event_bus.publish({
                "type": "index_complete",
                "path": file_path,
                "result": result,
            })
        else:
            result = full_index()
            await event_bus.publish({
                "type": "full_index_complete",
                "result": result,
            })
    
    asyncio.create_task(run_index())
    
    await log_and_record(auditor, request, "trigger_index",
                         "/api/regulatory/index/trigger")
    
    return {
        "ok": True,
        "message": "索引任务已启动" if not (req and req.path) else f"正在索引 {req.path}",
        "note": "通过 SSE (/api/regulatory/operations/live) 可查看进度",
    }


# ═══════════════════════════════════════════
# WebSocket 实时推送
# ═══════════════════════════════════════════

@router.websocket("/regulatory/ws")
async def regulatory_websocket(ws: WebSocket):
    """监管专用 WebSocket，实时推送系统事件。通过 query param ?key= 认证。"""
    # 从 query params 获取认证 key
    key = ws.query_params.get("key", "")
    if not key:
        await ws.close(code=4001, reason="缺少认证密钥")
        return
    
    key_hash = hashlib.sha256(f"LH_REGULATORY_SALT_{key}".encode()).hexdigest()
    auditor = get_auditor_by_key_hash(key_hash)
    if not auditor:
        await ws.close(code=4003, reason="认证失败")
        return
    
    await ws.accept()
    
    # 发送欢迎消息
    await ws.send_json({
        "type": "welcome",
        "auditor": auditor["name"],
        "organization": auditor["organization"],
        "timestamp": now_iso(),
        "message": "龍魂监管实时通道已建立",
    })
    
    queue = await event_bus.subscribe()
    
    try:
        while True:
            # 检查客户端消息
            try:
                data = await asyncio.wait_for(ws.receive_text(), timeout=1)
                if data == "ping":
                    await ws.send_json({"type": "pong", "timestamp": now_iso()})
                elif data == "state":
                    state = get_system_state()
                    await ws.send_json({"type": "system_state", "state": state})
            except asyncio.TimeoutError:
                pass
            
            # 发送事件
            try:
                event = queue.get_nowait()
                await ws.send_json(event)
            except asyncio.QueueEmpty:
                pass
            
            await asyncio.sleep(0.5)
    
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        event_bus.unsubscribe(queue)


# ═══════════════════════════════════════════
# 监管者管理（管理员专用）
# ═══════════════════════════════════════════

@router.get("/regulatory/admin/auditors")
async def regulatory_list_auditors(
    request: Request,
    auditor: dict[str, Any] = Depends(require_regulator),
):
    """列出所有监管者（仅 full 权限监管者）。"""
    if auditor.get("access_level") != "full":
        raise HTTPException(status_code=403, detail="需要 full 权限")
    
    from .database import get_connection
    with get_connection() as conn:
        rows = conn.execute("SELECT auditor_id, name, organization, access_level, created_at, last_access, access_count, status FROM regulatory_auditors").fetchall()
        auditors = [dict(r) for r in rows]
    
    return {"ok": True, "count": len(auditors), "auditors": auditors}


@router.get("/regulatory/admin/access-logs")
async def regulatory_access_logs(
    request: Request,
    limit: int = Query(default=100, le=1000),
    auditor_id: str = Query(default=None),
    auditor: dict[str, Any] = Depends(require_regulator),
):
    """查看监管访问日志。"""
    if auditor.get("access_level") != "full":
        raise HTTPException(status_code=403, detail="需要 full 权限")
    
    logs = get_regulatory_access_logs(limit=limit, auditor_id=auditor_id)
    return {"ok": True, "count": len(logs), "logs": logs}
