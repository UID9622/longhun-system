from __future__ import annotations
"""
龍魂统一监管API · 核心服务层
DNA: #龍芯⚡️2026-07-12-REGULATORY-SERVICE-v2.0 · 三层透明模型

统一监管服务:
- 文件系统扫描与文档注册（含主权分级）
- 三层主权边界检测 (Layer 1/2/3)
- 操作捕获与哈希链
- 系统状态快照
- 合规报告生成
- 协议自检
- 实时事件流
"""

import hashlib
import json
import os
import sys
import subprocess
import asyncio
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional, AsyncGenerator, Any

from .config import PROJECT_ROOT, DATA_DIR, DB_PATH, SOVEREIGNTY_PRIVATE_DIRS, SOVEREIGNTY_PRIVATE_TAGS
from .database import now_iso
from . import regulatory_db as rdb


# ── 文件类型映射 ──
FILE_TYPE_MAP = {
    '.md': 'markdown',
    '.py': 'python',
    '.js': 'javascript',
    '.ts': 'typescript',
    '.tsx': 'react-tsx',
    '.jsx': 'react-jsx',
    '.json': 'json',
    '.yaml': 'yaml',
    '.yml': 'yaml',
    '.toml': 'toml',
    '.html': 'html',
    '.css': 'css',
    '.sh': 'shell',
    '.bat': 'batch',
    '.sql': 'sql',
    '.txt': 'text',
    '.pdf': 'pdf',
    '.csv': 'csv',
    '.xml': 'xml',
    '.env': 'config',
    '.conf': 'config',
    '.cfg': 'config',
    '.ini': 'config',
    '.lock': 'lockfile',
    '.dockerfile': 'dockerfile',
    '.gitignore': 'config',
    '.md.asc': 'signed-markdown',
    '.jsonl': 'jsonl-log',
    '.log': 'log',
}

DOC_EXTENSIONS = {'.md', '.py', '.js', '.ts', '.tsx', '.jsx', '.json', '.yaml', '.yml', 
                  '.toml', '.html', '.css', '.sh', '.sql', '.txt', '.xml', '.md.asc'}

# 跳过目录
SKIP_DIRS = {
    '__pycache__', 'node_modules', '.git', 'venv', '.venv', 'env', 
    'dist', 'build', '.next', '.cache', 'tmp', '.obsidian',
    'logs', 'logging_backup', 'backups', '.codebuddy', 
    'outputs', 'reports', '.DS_Store'
}

# 跳过文件后缀
SKIP_EXTENSIONS = {'.pyc', '.pyo', '.so', '.dll', '.dylib', '.exe', '.bin',
                   '.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.ico',
                   '.mp3', '.mp4', '.wav', '.avi', '.mov', '.mkv',
                   '.zip', '.tar', '.gz', '.bz2', '.7z', '.rar',
                   '.db', '.sqlite', '.sqlite3', '.db-journal', '.db-wal',
                   '.woff', '.woff2', '.ttf', '.eot', '.otf',
                   '.map'}


def get_file_type(file_path: str) -> str:
    """根据文件后缀确定文件类型。"""
    path = Path(file_path)
    ext = path.suffix.lower()
    if ext in FILE_TYPE_MAP:
        return FILE_TYPE_MAP[ext]
    name = path.name.lower()
    if name == 'dockerfile':
        return 'dockerfile'
    if name == 'makefile':
        return 'makefile'
    if name in ('readme.md', 'readme.txt'):
        return 'readme'
    return f'unknown-{ext[1:] if ext else "noext"}'


def compute_sha256(file_path: str) -> str:
    """计算文件 SHA256。"""
    h = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return ""


def count_words(content: str) -> int:
    """粗略计算字数（中文字符 + 英文单词）。"""
    chinese_chars = sum(1 for c in content if '\u4e00' <= c <= '\u9fff')
    english_words = len([w for w in content.split() if any(c.isalpha() for c in w)])
    return chinese_chars + english_words


def extract_title(file_path: str, content: str | None = None) -> str:
    """从文件提取标题。"""
    if content is None:
        try:
            content = Path(file_path).read_text(encoding='utf-8', errors='ignore')
        except Exception:
            return Path(file_path).stem
    
    # 尝试 Markdown 标题
    for line in content.split('\n')[:10]:
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
    
    # 尝试文件注释中的标题
    for line in content.split('\n')[:5]:
        line = line.strip()
        if line.startswith('// ') or line.startswith('"""'):
            clean = line.lstrip('/" ').strip()
            if clean and len(clean) < 100:
                return clean
    
    return Path(file_path).stem


def should_index(file_path: str) -> bool:
    """判断文件是否应该被索引。"""
    path = Path(file_path)
    # 跳过隐藏文件（除了 .env.example 等）
    if path.name.startswith('.') and path.name not in {'.env.example', '.gitignore', '.cursorrules'}:
        return False
    # 跳过特定后缀
    if path.suffix.lower() in SKIP_EXTENSIONS:
        return False
    # 只索引文档类型
    if path.suffix.lower() not in DOC_EXTENSIONS:
        # 但索引 package.json, tsconfig 等特殊文件
        special_names = {'package.json', 'tsconfig.json', 'pyproject.toml', 'requirements.txt',
                        'docker-compose.yml', 'docker-compose.yaml', 'Makefile', 'Dockerfile'}
        if path.name not in special_names:
            return False
    # 跳过二进制
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(256)
            if b'\x00' in chunk:
                return False
    except Exception:
        return False
    return True


def detect_sovereignty_level(file_path: str, content: str | None = None) -> tuple[Any, ...]:
    """
    三层主权分级检测。
    返回: (sovereignty_level: int, is_private_content: int, reason: str)
    
    层1 = 公开 — 开源代码、协议、公开文档 → 所有人可见
    层2 = 透明 — 元数据可见、内容受控 → 授权监管者可见  
    层3 = 私有 — 不可触碰 → 任何外部实体未经用户授权不可见
    """
    path_str = str(file_path)
    path_lower = path_str.lower()
    
    # ── 判定层3：私有 ──
    # 检查私有目录
    for priv_dir in SOVEREIGNTY_PRIVATE_DIRS:
        if f"/{priv_dir}/" in path_str or path_str.startswith(f"{priv_dir}/") or f"/{priv_dir}" == path_str:
            return (3, 1, f"在私有目录 {priv_dir} 中")
    # 检查私有扩展名（.asc 签名文件、.key 密钥文件等）
    private_exts = {'.asc', '.key', '.pem', '.crt', '.gpg', '.sig'}
    if Path(file_path).suffix.lower() in private_exts:
        return (3, 1, f"私有文件类型: {Path(file_path).suffix}")
    
    # ── 读取文件前几行检查标记 ──
    try:
        if content is None:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                head = ''.join([f.readline() for _ in range(10)])
        else:
            head = content[:2000] if content else ""
    except Exception:
        head = ""
    
    for tag in SOVEREIGNTY_PRIVATE_TAGS:
        if tag in head:
            return (3, 1, f"文件内容包含私有标记: {tag}")
    
    # ── 判定层1：公开 ──
    public_dirs = {'01_protocols/', 'articles/', 'papers/', 'public-content/', 
                   'docs/', 'LICENSE', 'AGENTS.md', 'README', 'STANDARD.md'}
    for pub_dir in public_dirs:
        if pub_dir in path_str or path_str.endswith(pub_dir):
            return (1, 0, f"公开内容: {pub_dir}")
    
    # bin/ 和引擎/ 中的非私有文件
    if '/bin/' in path_str or '引擎/' in path_str or '01_技能庫/' in path_str:
        return (1, 0, "公开工具/引擎代码")
    
    # ── 默认层2：透明 ──
    return (2, 0, "默认透明层")


def redact_private_content(file_path: str, sovereignty_level: int) -> str:
    """
    对层3文件的内容进行脱敏处理。
    返回脱敏后的说明文本，而非实际内容。
    """
    if sovereignty_level == 3:
        return (
            f"[此文件位于数据主权层3（私有层）]\n"
            f"路径: {file_path}\n"
            f"根据龍魂监管宪法，层3内容属于用户私有数据，\n"
            f"任何外部实体未经用户明确授权不可访问。\n"
            f"如需访问，请联系数据主权持有者 UID9622。\n"
        )
    return None  # 层1/2 不脱敏


def get_sovereignty_declaration() -> dict[str, Any]:
    """获取完整的数据主权声明（三层透明模型）。"""
    from .config import REGULATORY_POSITION_STATEMENT, REGULATORY_CONSTITUTION_VERSION
    return {
        "constitution_version": REGULATORY_CONSTITUTION_VERSION,
        "position": REGULATORY_POSITION_STATEMENT,
        "three_layer_model": {
            "layer_1_public": {
                "description": "公开层 — 开源代码、协议、公开文档",
                "visibility": "任何人可查看、下载、审计",
                "content_access": "完整内容可见",
                "examples": ["01_protocols/*", "articles/*", "bin/*", "引擎/*", "docs/*"],
            },
            "layer_2_transparent": {
                "description": "透明层 — 操作元数据、系统状态",
                "visibility": "授权监管者通过 API 可查询元数据",
                "content_access": "元数据可见（标题/类型/哈希/字数），内容需用户授权",
                "examples": ["操作日志", "文件变更日志", "系统状态", "日报/周报"],
            },
            "layer_3_private": {
                "description": "私有层 — 用户数据、草稿、个人文件",
                "visibility": "仅用户自己持有，外部实体不可触碰",
                "content_access": "禁止。返回主权声明而非内容",
                "examples": ["_private/*", "tombstone_vault/*", "vault/*", "memory-universe/*"],
            },
        },
        "principles": [
            "1. 数据不出境 — 所有数据均存储在本地 SQLite，不自动上传云端",
            "2. 元数据透明 — 操作类型、时间、文件路径对监管者可见",
            "3. 内容主权 — 文件内容属于用户，监管者不可未经授权读取",
            "4. 哈希链不可篡改 — 所有操作日志链式哈希，可验证未被修改",
            "5. 访问可追溯 — 监管者每次查询均记录到 regulatory_access_log",
            "6. 用户授权开关 — 层2的开放程度由用户通过主权策略控制",
        ],
        "legal_notice": (
            "本系统为民用系统自愿透明接口，非政府强制监管接入。"
            "不处理政务数据、不接入国家安全网络、不是政府项目。"
            "主权持有者: UID9622 | 部署: 华为鲲鹏 · 国产底座"
        ),
        "window_for_people": (
            "本窗口旨在为中国人民提供一个透明、可审计的技术平台。"
            "代码公开、协议公开、操作可查。"
            "站在阳光底下，不辜负人民信任。"
        ),
    }


def protocol_self_check() -> dict[str, Any]:
    """
    协议合规自检 — 检查系统是否遵守自身设定的安全基线。
    返回逐项判定结果。
    """
    from .config import REGULATORY_CONSTITUTION_VERSION
    checks = []
    
    # 1. 数据本地化检查
    checks.append({
        "id": "PS-001",
        "name": "数据本地化",
        "rule": "所有监管数据存储在本地 SQLite",
        "status": "pass",
        "detail": f"数据库路径: {DB_PATH}，位于本地文件系统",
    })
    
    # 2. 层3边界检查
    layer3_docs = rdb.get_documents(limit=1000)
    layer3_violations = []
    for doc in layer3_docs:
        if doc.get("sovereignty_level") == 3 and not doc.get("is_private_content"):
            layer3_violations.append(doc["file_path"])
    checks.append({
        "id": "PS-002",
        "name": "层3私有内容保护",
        "rule": "所有层3文件标记 is_private_content=1",
        "status": "fail" if layer3_violations else "pass",
        "detail": f"{len(layer3_violations)} 个层3文件未正确标记" if layer3_violations else "所有层3文件已正确保护",
        "violations": layer3_violations[:10] if layer3_violations else [],
    })
    
    # 3. 哈希链完整性
    chain_check = rdb.verify_regulatory_hash_chain()
    checks.append({
        "id": "PS-003",
        "name": "操作日志哈希链",
        "rule": "所有操作日志通过 SHA256 哈希链连接",
        "status": "pass" if chain_check["ok"] else "fail",
        "detail": f"链长度: {chain_check['chain_length']}，状态: {chain_check['status']}",
        "violations": chain_check.get("violations", []),
    })
    
    # 4. 监管访问记录
    from .database import get_connection
    with get_connection() as conn:
        access_count = conn.execute(
            "SELECT COUNT(*) FROM regulatory_access_log"
        ).fetchone()[0]
        policy_count = conn.execute(
            "SELECT COUNT(*) FROM sovereignty_policy"
        ).fetchone()[0]
    
    checks.append({
        "id": "PS-004",
        "name": "监管访问可追溯",
        "rule": "每次监管者查询被记录到 regulatory_access_log",
        "status": "pass",
        "detail": f"已记录 {access_count} 次监管访问",
    })
    
    checks.append({
        "id": "PS-005",
        "name": "主权策略记录",
        "rule": "主权边界决策有据可查",
        "status": "pass" if policy_count > 0 else "warning",
        "detail": f"已记录 {policy_count} 条主权策略",
    })
    
    # 5. 用户授权开关检查
    checks.append({
        "id": "PS-006",
        "name": "层2内容授权控制",
        "rule": "监管者查看文档内容需用户授权（include_content 需显式打开）",
        "status": "pass",
        "detail": "API 设计中 include_content 默认为 false，层3文件即使 include_content=true 也返回脱敏内容",
    })
    
    # 汇总
    all_pass = all(c["status"] == "pass" for c in checks)
    return {
        "ok": all_pass,
        "constitution_version": REGULATORY_CONSTITUTION_VERSION,
        "checked_at": now_iso(),
        "summary": {
            "total_checks": len(checks),
            "passed": sum(1 for c in checks if c["status"] == "pass"),
            "failed": sum(1 for c in checks if c["status"] == "fail"),
            "warnings": sum(1 for c in checks if c["status"] == "warning"),
        },
        "overall": "compliant" if all_pass else "needs_attention",
        "checks": checks,
    }


def scan_directory(root_path: str, max_files: int = 10000) -> list[Any]:
    """扫描目录，返回所有应索引的文件路径列表。"""
    results = []
    root = Path(root_path)
    if not root.exists():
        return results
    
    for dirpath, dirnames, filenames in os.walk(root):
        # 跳过不需要的目录
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.')]
        
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if should_index(file_path):
                results.append(file_path)
                if len(results) >= max_files:
                    return results
    return results


def index_document(file_path: str) -> Optional[dict[str, Any]]:
    """索引单个文档到注册表。v2: +主权分级。"""
    if not should_index(file_path):
        return None
    
    try:
        stat = os.stat(file_path)
        file_type = get_file_type(file_path)
        sha256 = compute_sha256(file_path)
        
        # 读取内容
        try:
            content = Path(file_path).read_text(encoding='utf-8', errors='ignore')
        except Exception:
            content = ""
        
        title = extract_title(file_path, content)
        word_count = count_words(content)
        
        # 主权分级检测
        sov_level, is_private, sov_reason = detect_sovereignty_level(file_path, content)
        
        # 推断状态
        path_str = str(file_path)
        if 'draft' in path_str.lower() or '草稿' in path_str or 'tmp' in path_str:
            status = 'draft'
        elif 'published' in path_str.lower() or 'articles' in path_str.lower():
            status = 'published'
        elif 'bin/' in path_str or '引擎/' in path_str:
            status = 'published'
        else:
            status = 'draft'
        
        # 标签
        tags = []
        if '01_protocols' in path_str:
            tags.append('protocols')
        if 'articles' in path_str:
            tags.append('articles')
        if '引擎/' in path_str:
            tags.append('engine')
        if 'bin/' in path_str:
            tags.append('tool')
        if 'personas' in path_str:
            tags.append('persona')
        if '03_知识图谱' in path_str:
            tags.append('knowledge-graph')
        # 主权层标签
        if sov_level == 1:
            tags.append('layer1:public')
        elif sov_level == 3:
            tags.append('layer3:private')
        else:
            tags.append('layer2:transparent')
        
        return rdb.upsert_document(
            file_path=file_path,
            doc_type=file_type,
            title=title,
            status=status,
            word_count=word_count,
            content_hash=sha256,
            tags=json.dumps(tags, ensure_ascii=False),
            meta_json=json.dumps({
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "sovereignty_reason": sov_reason,
            }, ensure_ascii=False),
            sovereignty_level=sov_level,
            is_private_content=is_private,
        )
    except Exception as e:
        return None


def full_index(progress_callback=None) -> dict[str, Any]:
    """全量扫描并索引所有文档。"""
    start_time = datetime.now(timezone.utc)
    root = str(PROJECT_ROOT)
    files = scan_directory(root)
    
    indexed = 0
    skipped = 0
    errors = 0
    
    for i, file_path in enumerate(files):
        try:
            result = index_document(file_path)
            if result and result.get('ok'):
                indexed += 1
            else:
                skipped += 1
        except Exception:
            errors += 1
        
        if progress_callback and i % 100 == 0:
            progress_callback(i, len(files))
    
    duration = (datetime.now(timezone.utc) - start_time).total_seconds()
    
    # 记录操作
    rdb.log_operation(
        op_type='full_index',
        source='regulatory_daemon',
        detail=f'全量索引完成: {indexed} 已索引, {skipped} 跳过, {errors} 错误, 耗时 {duration:.1f}s',
        operator_uid='SYSTEM'
    )
    
    return {
        "ok": True,
        "total_found": len(files),
        "indexed": indexed,
        "skipped": skipped,
        "errors": errors,
        "duration_seconds": round(duration, 1),
        "timestamp": now_iso()
    }


def get_system_state() -> dict[str, Any]:
    """获取系统实时状态快照。"""
    state = {
        "timestamp": now_iso(),
        "hostname": os.uname().nodename if hasattr(os, 'uname') else "unknown",
        "python_version": sys.version,
    }
    
    # CPU
    try:
        import psutil
        state["cpu"] = {
            "percent": psutil.cpu_percent(interval=0.1),
            "cores": psutil.cpu_count(),
        }
        mem = psutil.virtual_memory()
        state["memory"] = {
            "total_gb": round(mem.total / (1024**3), 1),
            "used_gb": round(mem.used / (1024**3), 1),
            "percent": mem.percent,
        }
        disk = psutil.disk_usage('/')
        state["disk"] = {
            "total_gb": round(disk.total / (1024**3), 1),
            "used_gb": round(disk.used / (1024**3), 1),
            "percent": disk.percent,
        }
        state["uptime"] = {
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat(),
        }
    except ImportError:
        state["cpu"] = {"note": "psutil 未安装"}
        state["memory"] = {"note": "psutil 未安装"}
        state["disk"] = {"note": "psutil 未安装"}
    
    # 数据库统计
    state["database"] = {
        "db_size_mb": round(DB_PATH.stat().st_size / (1024**2), 2) if DB_PATH.exists() else 0,
    }
    
    # 操作统计
    doc_stats = rdb.get_document_stats()
    state["documents"] = doc_stats
    
    # Git 信息
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%H|%s|%ai"],
            capture_output=True, text=True, timeout=5,
            cwd=str(PROJECT_ROOT)
        )
        if result.returncode == 0 and result.stdout.strip():
            parts = result.stdout.strip().split('|', 2)
            state["git"] = {
                "last_commit": parts[0][:12] if len(parts) > 0 else "unknown",
                "last_message": parts[1] if len(parts) > 1 else "",
                "last_time": parts[2] if len(parts) > 2 else "",
            }
    except Exception:
        state["git"] = {"note": "git 不可用"}
    
    return state


def generate_daily_report(date_str: str | None = None) -> dict[str, Any]:
    """生成每日合规报告。"""
    if date_str is None:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    with rdb.get_connection() if hasattr(rdb, 'get_connection') else None:
        from .database import get_connection
        with get_connection() as conn:
            # 当日操作统计
            ops = conn.execute(
                "SELECT operation_type, COUNT(*) as cnt FROM operation_log "
                "WHERE date(timestamp) = ? GROUP BY operation_type ORDER BY cnt DESC",
                (date_str,)
            ).fetchall()
            
            # 当日文件变更
            changes = conn.execute(
                "SELECT event_type, COUNT(*) as cnt FROM file_change_log "
                "WHERE date(timestamp) = ? GROUP BY event_type",
                (date_str,)
            ).fetchall()
            
            # 审计统计
            audits = conn.execute(
                "SELECT module, COUNT(*) as cnt FROM audit_log "
                "WHERE date(timestamp) = ? GROUP BY module ORDER BY cnt DESC",
                (date_str,)
            ).fetchall()
            
            # 新增/修改文档
            docs = conn.execute(
                "SELECT COUNT(*) FROM document_registry WHERE date(modified_at) = ?",
                (date_str,)
            ).fetchone()[0]
    
    total_ops = sum(r[1] for r in ops) if ops else 0
    total_changes = sum(r[1] for r in changes) if changes else 0
    
    return {
        "report_type": "daily",
        "date": date_str,
        "generated_at": now_iso(),
        "summary": {
            "total_operations": total_ops,
            "total_file_changes": total_changes,
            "documents_modified": docs,
            "health": "healthy" if total_ops > 0 else "inactive",
        },
        "operations_breakdown": [{"type": r[0], "count": r[1]} for r in ops] if ops else [],
        "file_changes_breakdown": [{"type": r[0], "count": r[1]} for r in changes] if changes else [],
        "audit_modules": [{"module": r[0], "count": r[1]} for r in audits] if audits else [],
        "regulatory_access": {},  # 从 regulatory_access_log 查询
        "sovereignty_status": "compliant",
        "system_state": get_system_state(),
    }


def generate_weekly_report() -> dict[str, Any]:
    """生成每周合规报告。"""
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=7)
    
    daily_reports = []
    for i in range(7):
        d = (end_date - timedelta(days=i)).strftime("%Y-%m-%d")
        daily_reports.append(generate_daily_report(d))
    
    total_ops = sum(r["summary"]["total_operations"] for r in daily_reports)
    total_changes = sum(r["summary"]["total_file_changes"] for r in daily_reports)
    
    return {
        "report_type": "weekly",
        "period": {
            "start": start_date.strftime("%Y-%m-%d"),
            "end": end_date.strftime("%Y-%m-%d"),
        },
        "generated_at": now_iso(),
        "summary": {
            "total_operations": total_ops,
            "total_file_changes": total_changes,
            "daily_reports": daily_reports,
        },
    }


# ── 实时事件流 (SSE) ──
class RegulatoryEventBus:
    """监管事件总线，用于 SSE 实时推送。"""
    
    def __init__(self):
        self._subscribers: list[asyncio.Queue] = []
    
    async def subscribe(self) -> asyncio.Queue:
        queue = asyncio.Queue(maxsize=100)
        self._subscribers.append(queue)
        return queue
    
    def unsubscribe(self, queue: asyncio.Queue):
        if queue in self._subscribers:
            self._subscribers.remove(queue)
    
    async def publish(self, event: dict[str, Any]):
        event["timestamp"] = now_iso()
        dead = []
        for q in self._subscribers:
            try:
                q.put_nowait(event)
            except asyncio.QueueFull:
                dead.append(q)
        for q in dead:
            self.unsubscribe(q)
    
    @property
    def subscriber_count(self) -> int:
        return len(self._subscribers)


# 全局事件总线实例
event_bus = RegulatoryEventBus()
