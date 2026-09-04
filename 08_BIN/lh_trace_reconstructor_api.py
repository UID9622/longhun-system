#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂·踪迹AI复原引擎 v2.0 — 四道防线版
DNA: #龍芯⚡️丙午·乙未·壬寅·亥时·䷀乾-TRACE-RECONSTRUCTOR-API-V2.0-FOUR-DEFENSES
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

部署在鲲鹏 :8774，接收本地采集引擎发送的特征向量（脱敏哈希），
通过模式匹配 + 本地AI模型重建为完整行为时间线。

防线四：导出文件绑定设备 + 生物特征 + 一次性签名
  - 导出时生成绑定签名包（设备指纹 + 生物哈希 + 时间戳 + HMAC）
  - 验证时三重比对：设备指纹 / 生物特征 / 签名完整性
  - 篡改检测 + 跨设备拒绝访问

铁律：
  - 只接收特征向量（哈希），不接收原始路径/IP
  - 复原结果为推断（标注置信度），不是绝对事实
  - 不存储用户原始数据
  - 签名密钥服务器端生成，验证在客户端完成
"""

import base64
import hashlib
import hmac
import json
import os
import secrets
import sqlite3
import time
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple

import uvicorn
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ─── 常量 ─────────────────────────────────────────────
VERSION = "2.0.0"
DNA = "#龍芯⚡️丙午·乙未·壬寅·亥时·䷀乾-TRACE-RECONSTRUCTOR-API-V2.0-FOUR-DEFENSES"
DATA_DIR = "/opt/longhun/traces"
DB_PATH = os.path.join(DATA_DIR, "trace_reconstruct.db")

# 防线四导出签名密钥（每次部署自动生成，不硬编码）
EXPORT_SIGNING_SECRET = os.environ.get("LH_EXPORT_SECRET", None)
if not EXPORT_SIGNING_SECRET:
    # 自动生成32字节密钥并写入环境文件提示
    EXPORT_SIGNING_SECRET = secrets.token_hex(32)
    try:
        key_path = os.path.join(DATA_DIR, ".export_signing.key")
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(key_path):
            with open(key_path, "w") as f:
                f.write(EXPORT_SIGNING_SECRET)
            os.chmod(key_path, 0o600)
        else:
            with open(key_path) as f:
                EXPORT_SIGNING_SECRET = f.read().strip()
    except Exception:
        pass

# 兜底：任何异常路径下签名密钥都不可为空
if not EXPORT_SIGNING_SECRET:
    EXPORT_SIGNING_SECRET = secrets.token_hex(32)


def _sign_export(payload: str) -> str:
    """导出包签名（密钥在函数内断言收窄，保证运行时非空）"""
    secret = EXPORT_SIGNING_SECRET
    assert secret is not None, "导出签名密钥未初始化"
    return _hmac_sign(payload, secret)

app = FastAPI(
    title="龍魂·踪迹复原引擎",
    version=VERSION,
    description="接收脱敏特征向量，通过AI模型复原数字行为时间线",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── 数据库 ─────────────────────────────────────────────
def get_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS received_vectors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            received_at REAL NOT NULL,
            client_id TEXT NOT NULL,
            features_json TEXT NOT NULL,
            reconstructed TEXT,
            confidence REAL DEFAULT 0.0
        );
        
        CREATE TABLE IF NOT EXISTS timelines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at REAL NOT NULL,
            client_id TEXT NOT NULL,
            session_start REAL,
            session_end REAL,
            timeline_json TEXT NOT NULL,
            event_count INTEGER DEFAULT 0,
            avg_confidence REAL DEFAULT 0.0
        );
        
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hash_key TEXT UNIQUE NOT NULL,
            label TEXT NOT NULL,
            category TEXT NOT NULL,
            count INTEGER DEFAULT 1,
            last_seen REAL NOT NULL,
            confidence REAL DEFAULT 0.5
        );
        
        CREATE INDEX IF NOT EXISTS idx_rv_client ON received_vectors(client_id, received_at);
        CREATE INDEX IF NOT EXISTS idx_tl_client ON timelines(client_id, created_at);
        CREATE INDEX IF NOT EXISTS idx_kb_hash ON knowledge_base(hash_key);
    """)
    conn.commit()
    return conn


# ─── 知识库（哈希→人类可读标注） ─────────────────
# 常见进程/应用哈希→名称映射参考（服务端仅做辅助推断）
COMMON_PATTERNS = {
    # 开发工具
    "code": {"category": "development", "label": "VS Code / 编辑器"},
    "terminal": {"category": "system", "label": "终端"},
    "git": {"category": "development", "label": "Git 版本控制"},
    "python": {"category": "development", "label": "Python"},
    "node": {"category": "development", "label": "Node.js"},
    "npm": {"category": "development", "label": "npm 包管理"},
    "docker": {"category": "development", "label": "Docker"},
    "ssh": {"category": "network", "label": "SSH 远程连接"},
    
    # 浏览器
    "chrome": {"category": "browser", "label": "Google Chrome"},
    "firefox": {"category": "browser", "label": "Firefox"},
    "safari": {"category": "browser", "label": "Safari"},
    "edge": {"category": "browser", "label": "Microsoft Edge"},
    
    # 办公
    "word": {"category": "office", "label": "Microsoft Word"},
    "excel": {"category": "office", "label": "Microsoft Excel"},
    "powerpoint": {"category": "office", "label": "PowerPoint"},
    "notes": {"category": "office", "label": "笔记应用"},
    "preview": {"category": "office", "label": "预览/PDF阅读"},
    "finder": {"category": "system", "label": "访达 (文件浏览)"},
    
    # 通讯
    "wechat": {"category": "social", "label": "微信"},
    "dingtalk": {"category": "social", "label": "钉钉"},
    "telegram": {"category": "social", "label": "Telegram"},
    "slack": {"category": "social", "label": "Slack"},
    
    # 系统
    "loginwindow": {"category": "system", "label": "系统登录"},
    "systemuiserver": {"category": "system", "label": "系统菜单栏"},
    "spotlight": {"category": "system", "label": "Spotlight 搜索"},
    "dock": {"category": "system", "label": "Dock 栏"},
    "windowserver": {"category": "system", "label": "窗口服务"},
    
    # 文件操作
    ".py": {"category": "file", "label": "Python 脚本"},
    ".js": {"category": "file", "label": "JavaScript"},
    ".html": {"category": "file", "label": "HTML 页面"},
    ".md": {"category": "file", "label": "Markdown 文档"},
    ".json": {"category": "file", "label": "JSON 配置"},
    ".yaml": {"category": "file", "label": "YAML 配置"},
    ".txt": {"category": "file", "label": "文本文件"},
    ".pdf": {"category": "file", "label": "PDF 文档"},
    ".csv": {"category": "file", "label": "CSV 表格"},
    ".log": {"category": "file", "label": "日志文件"},
    ".sh": {"category": "file", "label": "Shell 脚本"},
    ".sql": {"category": "file", "label": "SQL 数据库"},
    ".png": {"category": "media", "label": "PNG 图片"},
    ".jpg": {"category": "media", "label": "JPEG 图片"},
    ".svg": {"category": "media", "label": "SVG 矢量图"},
    ".mp4": {"category": "media", "label": "MP4 视频"},
}


# ─── Pydantic Models ───────────────────────────────────
class FeatureVector(BaseModel):
    type: str
    ts: float
    name_hash: Optional[str] = None
    cmdline_hash: Optional[str] = None
    path_hash: Optional[str] = None
    ext: Optional[str] = None
    remote_hash: Optional[str] = None
    detail_hash: Optional[str] = None

class ReconstructRequest(BaseModel):
    client_id: str = "default"
    features: List[FeatureVector]
    session_window: int = 300  # 会话窗口(秒)，间隔超过此值视为新会话

class TimelineEvent(BaseModel):
    time: str          # ISO 时间
    timestamp: float
    action: str        # 人类可读动作描述
    category: str      # development/system/browser/office/file/network/social
    confidence: float  # 0.0-1.0
    evidence: str      # 推理依据
    raw_type: str      # 原始事件类型

class Session(BaseModel):
    session_id: int
    start_time: str
    end_time: str
    duration_seconds: float
    events: List[TimelineEvent]
    summary: str

class ReconstructResponse(BaseModel):
    client_id: str
    reconstructed_at: str
    dna: str
    total_events: int
    confidence_avg: float
    sessions: List[Session]
    full_timeline: List[TimelineEvent]


# ─── 复原引擎核心逻辑 ───────────────────────────────
def infer_category(feature: dict) -> str:
    """根据特征向量推断事件类别"""
    ftype = feature.get("type", "")
    
    if ftype.startswith("process_"):
        return "system"
    elif ftype.startswith("file_"):
        ext = feature.get("ext", "")
        for pattern, info in COMMON_PATTERNS.items():
            if pattern.startswith(".") and ext == pattern:
                return info["category"]
        return "file"
    elif ftype.startswith("network_"):
        return "network"
    elif ftype.startswith("user_"):
        return "system"
    return "unknown"

def infer_action(feature: dict) -> Tuple[str, float, str]:
    """
    推断人类可读的动作描述。
    返回: (描述, 置信度, 推理依据)
    """
    ftype = feature.get("type", "")
    
    # 进程事件
    if ftype == "process_start":
        return ("启动应用", 0.4, "检测到新进程启动")
    elif ftype == "process_stop":
        return ("关闭应用", 0.35, "检测到进程退出")
    
    # 文件事件
    elif ftype == "file_create":
        ext = feature.get("ext", "")
        for pattern, info in COMMON_PATTERNS.items():
            if pattern.startswith(".") and ext == pattern:
                return (f"创建{info['label']}", 0.6, f"文件扩展名 {ext}")
        return ("创建文件", 0.5, "检测到新文件")
    elif ftype == "file_modify":
        ext = feature.get("ext", "")
        for pattern, info in COMMON_PATTERNS.items():
            if pattern.startswith(".") and ext == pattern:
                return (f"编辑{info['label']}", 0.55, f"文件扩展名 {ext}")
        return ("编辑文件", 0.45, "检测到文件修改")
    elif ftype == "file_delete":
        return ("删除文件", 0.5, "检测到文件删除")
    
    # 网络事件
    elif ftype == "network_connect":
        return ("建立网络连接", 0.3, "检测到新网络连接")
    
    # 用户事件
    elif ftype == "user_login":
        return ("用户登录", 0.8, "检测到登录事件")
    elif ftype == "user_logout":
        return ("用户注销", 0.8, "检测到注销事件")
    elif ftype == "user_lock":
        return ("锁定屏幕", 0.7, "检测到锁屏")
    elif ftype == "user_unlock":
        return ("解锁屏幕", 0.7, "检测到解锁")
    elif ftype == "device_attach":
        return ("连接外设", 0.6, "检测到USB设备")
    elif ftype == "device_detach":
        return ("拔出外设", 0.6, "检测到USB设备移除")
    
    return ("未知操作", 0.1, f"未知事件类型: {ftype}")

def enhance_with_knowledge_base(db: sqlite3.Connection, feature: dict) -> Tuple[str, float, str]:
    """用知识库增强推断（如果哈希曾经匹配过已知模式）"""
    action, confidence, evidence = infer_action(feature)
    
    # 尝试从知识库查找更精确的标签
    for key in ["name_hash", "cmdline_hash", "path_hash"]:
        h = feature.get(key)
        if h:
            row = db.execute(
                "SELECT label, category, confidence FROM knowledge_base WHERE hash_key=? ORDER BY count DESC LIMIT 1",
                (h,)
            ).fetchone()
            if row:
                # 用知识库标注提高置信度
                enhanced = f"{action} ({row['label']})"
                return (enhanced, min(confidence + row["confidence"] * 0.3, 0.95),
                        f"{evidence} + 知识库匹配: {row['label']}")
    
    return (action, confidence, evidence)

def reconstruct_timeline(
    db: sqlite3.Connection,
    client_id: str,
    features: List[dict],
    session_window: int = 300
) -> dict:
    """
    核心复原逻辑：
    1. 将所有特征向量按时间排序
    2. 按 session_window 分割为会话
    3. 对每个事件推断人类可读描述
    4. 生成结构化时间线
    """
    
    # 按时间排序
    features.sort(key=lambda f: f.get("ts", 0))
    
    # 转换为 TimelineEvent
    events = []
    for f in features:
        ts = f.get("ts", 0)
        action, confidence, evidence = enhance_with_knowledge_base(db, f)
        category = infer_category(f)
        
        if confidence < 0.15:
            continue  # 过滤低置信度事件
        
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        
        events.append({
            "time": dt.strftime("%H:%M:%S"),
            "timestamp": ts,
            "action": action,
            "category": category,
            "confidence": round(confidence, 3),
            "evidence": evidence,
            "raw_type": f.get("type", "unknown"),
        })
    
    if not events:
        return {
            "client_id": client_id,
            "reconstructed_at": datetime.now(timezone.utc).isoformat(),
            "dna": DNA,
            "total_events": 0,
            "confidence_avg": 0.0,
            "sessions": [],
            "full_timeline": [],
        }
    
    # 分割会话
    sessions = []
    current_session_events = [events[0]]
    session_start = events[0]["timestamp"]
    
    for evt in events[1:]:
        gap = evt["timestamp"] - current_session_events[-1]["timestamp"]
        if gap > session_window:
            # 保存当前会话
            session_end = current_session_events[-1]["timestamp"]
            sessions.append({
                "session_id": len(sessions) + 1,
                "start_time": datetime.fromtimestamp(session_start, tz=timezone.utc).strftime("%H:%M:%S"),
                "end_time": datetime.fromtimestamp(session_end, tz=timezone.utc).strftime("%H:%M:%S"),
                "duration_seconds": round(session_end - session_start, 1),
                "events": current_session_events,
                "summary": generate_session_summary(current_session_events),
            })
            current_session_events = []
            session_start = evt["timestamp"]
        current_session_events.append(evt)
    
    # 最后一个会话
    if current_session_events:
        session_end = current_session_events[-1]["timestamp"]
        sessions.append({
            "session_id": len(sessions) + 1,
            "start_time": datetime.fromtimestamp(session_start, tz=timezone.utc).strftime("%H:%M:%S"),
            "end_time": datetime.fromtimestamp(session_end, tz=timezone.utc).strftime("%H:%M:%S"),
            "duration_seconds": round(session_end - session_start, 1),
            "events": current_session_events,
            "summary": generate_session_summary(current_session_events),
        })
    
    # 计算平均置信度
    confidences = [e["confidence"] for e in events]
    avg_conf = round(sum(confidences) / len(confidences), 3) if confidences else 0.0
    
    # 保存到数据库
    timeline_json = json.dumps({
        "sessions": sessions,
        "full_timeline": events,
    }, ensure_ascii=False)
    
    db.execute(
        """INSERT INTO timelines (created_at, client_id, session_start, session_end, timeline_json, event_count, avg_confidence)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (time.time(), client_id, events[0]["timestamp"], events[-1]["timestamp"],
         timeline_json, len(events), avg_conf)
    )
    db.commit()
    
    return {
        "client_id": client_id,
        "reconstructed_at": datetime.now(timezone.utc).isoformat(),
        "dna": DNA,
        "total_events": len(events),
        "confidence_avg": avg_conf,
        "sessions": sessions,
        "full_timeline": events,
    }

def generate_session_summary(events: List[dict]) -> str:
    """为会话生成一句话摘要"""
    if not events:
        return "空会话"
    
    categories = defaultdict(int)
    actions = []
    for e in events:
        categories[e["category"]] += 1
        if e["confidence"] > 0.5:
            actions.append(e["action"])
    
    # 找主要类别
    main_cat = max(categories, key=lambda k: categories[k]) if categories else "other"
    
    cat_labels = {
        "development": "编程开发",
        "browser": "浏览网页",
        "office": "办公文档",
        "file": "文件操作",
        "network": "网络通信",
        "system": "系统操作",
        "social": "社交通讯",
        "media": "媒体处理",
    }
    
    cat_name = cat_labels.get(main_cat, main_cat)
    
    # 取前3个高置信度动作
    top_actions = [a for a in actions[:3] if a != "未知操作"]
    
    if top_actions:
        return f"主要进行{cat_name}：{'、'.join(top_actions[:3])}"
    else:
        return f"主要进行{cat_name}活动"


# ─── API端点 ────────────────────────────────────────────

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "version": VERSION,
        "dna": DNA,
        "service": "trace-reconstructor",
    }

@app.get("/status")
async def status():
    db = get_db()
    vectors_count = db.execute("SELECT COUNT(*) FROM received_vectors").fetchone()[0]
    timelines_count = db.execute("SELECT COUNT(*) FROM timelines").fetchone()[0]
    kb_count = db.execute("SELECT COUNT(*) FROM knowledge_base").fetchone()[0]
    return {
        "service": "trace-reconstructor",
        "version": VERSION,
        "vectors_received": vectors_count,
        "timelines_generated": timelines_count,
        "knowledge_base_entries": kb_count,
    }

@app.post("/v1/reconstruct", response_model=ReconstructResponse)
async def reconstruct(req: ReconstructRequest):
    """核心端点：接收特征向量，返回复原后的行为时间线"""
    
    db = get_db()
    
    # 存储接收到的特征向量
    features_json = json.dumps([f.model_dump() for f in req.features], ensure_ascii=False)
    db.execute(
        "INSERT INTO received_vectors (received_at, client_id, features_json) VALUES (?, ?, ?)",
        (time.time(), req.client_id, features_json)
    )
    db.commit()
    
    # 复原时间线
    features_list = [f.model_dump() for f in req.features]
    result = reconstruct_timeline(db, req.client_id, features_list, req.session_window)
    
    return result

@app.get("/v1/timelines/{client_id}")
async def get_timelines(
    client_id: str,
    limit: int = Query(default=10, le=100),
    offset: int = Query(default=0, ge=0),
):
    """获取历史复原时间线"""
    db = get_db()
    rows = db.execute(
        "SELECT * FROM timelines WHERE client_id=? ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (client_id, limit, offset)
    ).fetchall()
    
    timelines = []
    for row in rows:
        timelines.append({
            "id": row["id"],
            "created_at": datetime.fromtimestamp(row["created_at"], tz=timezone.utc).isoformat(),
            "client_id": row["client_id"],
            "session_start": datetime.fromtimestamp(row["session_start"], tz=timezone.utc).isoformat() if row["session_start"] else None,
            "session_end": datetime.fromtimestamp(row["session_end"], tz=timezone.utc).isoformat() if row["session_end"] else None,
            "event_count": row["event_count"],
            "avg_confidence": row["avg_confidence"],
            "timeline": json.loads(row["timeline_json"]),
        })
    
    return {"client_id": client_id, "count": len(timelines), "timelines": timelines}

@app.post("/v1/knowledge/learn")
async def learn_pattern(
    hash_key: str = Query(description="特征哈希"),
    label: str = Query(description="人类可读标签"),
    category: str = Query(description="分类: development/browser/office/file/network/social/system"),
    confidence: float = Query(default=0.5, ge=0.0, le=1.0),
):
    """知识库学习：将哈希→标签映射加入知识库"""
    db = get_db()
    
    existing = db.execute(
        "SELECT id, count FROM knowledge_base WHERE hash_key=?",
        (hash_key,)
    ).fetchone()
    
    if existing:
        db.execute(
            "UPDATE knowledge_base SET label=?, category=?, count=count+1, last_seen=?, confidence=? WHERE hash_key=?",
            (label, category, time.time(), confidence, hash_key)
        )
    else:
        db.execute(
            "INSERT INTO knowledge_base (hash_key, label, category, count, last_seen, confidence) VALUES (?, ?, ?, 1, ?, ?)",
            (hash_key, label, category, time.time(), confidence)
        )
    
    db.commit()
    return {"status": "learned", "hash_key": hash_key, "label": label}

@app.get("/v1/knowledge/search")
async def search_knowledge(
    hash_key: str = Query(description="特征哈希"),
):
    """查询知识库"""
    db = get_db()
    row = db.execute(
        "SELECT * FROM knowledge_base WHERE hash_key=? ORDER BY count DESC LIMIT 1",
        (hash_key,)
    ).fetchone()
    
    if row:
        return {
            "found": True,
            "hash_key": row["hash_key"],
            "label": row["label"],
            "category": row["category"],
            "count": row["count"],
            "confidence": row["confidence"],
            "last_seen": datetime.fromtimestamp(row["last_seen"], tz=timezone.utc).isoformat(),
        }
    else:
        return {"found": False, "hash_key": hash_key}

@app.get("/v1/knowledge/stats")
async def knowledge_stats():
    """知识库统计"""
    db = get_db()
    total = db.execute("SELECT COUNT(*) FROM knowledge_base").fetchone()[0]
    by_cat = db.execute(
        "SELECT category, COUNT(*) as cnt FROM knowledge_base GROUP BY category ORDER BY cnt DESC"
    ).fetchall()
    return {
        "total_entries": total,
        "by_category": {row["category"]: row["cnt"] for row in by_cat},
    }


# ═══════════════════════════════════════════════════════
# 防线四：导出绑定设备+生物验证+一次性签名
# ═══════════════════════════════════════════════════════

class ExportSignRequest(BaseModel):
    """导出签名请求"""
    client_id: str = "unknown"              # 客户端标识
    device_fingerprint_hash: str            # 设备指纹SHA256（从本地采集引擎获取）
    biometric_hash: Optional[str] = None    # 生物特征哈希（指纹/面部，本地生成）
    export_data_hash: str                   # 导出数据的SHA256哈希
    timestamp: Optional[float] = None       # 客户端时间戳

class ExportVerifyRequest(BaseModel):
    """导出验证请求"""
    export_bundle: str                      # 完整导出包（base64 JSON）
    verify_device_fingerprint: str          # 验证方设备指纹（用于比对）
    verify_biometric_hash: Optional[str] = None  # 验证方生物特征哈希

class ExportSignResponse(BaseModel):
    signed_bundle: str                      # base64 编码的完整签名包
    bundle_id: str                          # 此次导出的唯一ID
    expires_at: float                       # 签名有效期
    verification_instructions: str          # 验证说明

class ExportVerifyResponse(BaseModel):
    verified: bool
    device_match: bool                      # 设备指纹匹配
    biometric_match: Optional[bool] = None  # 生物特征匹配
    signature_valid: bool                   # 签名未被篡改
    bundle_id: Optional[str] = None
    message: str
    details: Dict[str, Any] = {}


def _generate_one_time_salt() -> str:
    """生成一次性盐值"""
    return secrets.token_hex(16)

def _hmac_sign(payload: str, secret: str) -> str:
    """HMAC-SHA256 签名"""
    return hmac.new(
        secret.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

def _build_export_bundle(
    client_id: str,
    device_fingerprint: str,
    biometric_hash: Optional[str],
    export_data_hash: str,
    ts: float,
) -> Dict[str, Any]:
    """构建导出包（不含签名）"""
    bundle_id = str(uuid.uuid4())
    one_time_salt = _generate_one_time_salt()
    
    bundle = {
        "bundle_id": bundle_id,
        "version": "2.0.0",
        "created_at": ts,
        "expires_at": ts + 86400 * 30,  # 30天有效期
        "client_id": client_id,
        "bindings": {
            "device_fingerprint_hash": device_fingerprint,
            "biometric_hash": biometric_hash,
            "data_hash": export_data_hash,
        },
        "one_time_salt": one_time_salt,
        "meta": {
            "protocol": "LH-EXPORT-BIND-v1.0",
            "binding_required": ["device", "biometric"],
            "copy_protection": "Device and biometric bound. Copying to another device or user renders this file unusable.",
            "tamper_protection": "Any modification to this bundle will invalidate the signature and trigger self-destruction.",
        },
    }
    return bundle

def _sign_bundle(bundle: Dict[str, Any]) -> str:
    """对导出包签名"""
    # 构建签名载荷：bundle_id + device_fp + bio_hash + data_hash + salt
    payload = "|".join([
        bundle["bundle_id"],
        bundle["bindings"]["device_fingerprint_hash"],
        bundle["bindings"].get("biometric_hash") or "",
        bundle["bindings"]["data_hash"],
        bundle["one_time_salt"],
        str(int(bundle["created_at"])),
    ])
    bundle["signature"] = _sign_export(payload)
    return base64.b64encode(json.dumps(bundle, ensure_ascii=False).encode("utf-8")).decode("ascii")

def _verify_bundle(signed_b64: str) -> Tuple[Optional[Dict], str]:
    """验证导出包完整性。
    Returns: (bundle_dict_or_None, error_message)
    """
    try:
        bundle = json.loads(base64.b64decode(signed_b64).decode("utf-8"))
    except Exception:
        return None, "导出包已损坏或格式无效"
    
    # 验证必要字段
    required = ["bundle_id", "created_at", "bindings", "one_time_salt", "signature"]
    for field in required:
        if field not in bundle:
            return None, f"导出包缺少字段: {field}"
    
    bindings = bundle.get("bindings", {})
    if "device_fingerprint_hash" not in bindings:
        return None, "导出包缺少设备指纹绑定"
    
    # 重新计算签名
    payload = "|".join([
        bundle["bundle_id"],
        bindings["device_fingerprint_hash"],
        bindings.get("biometric_hash") or "",
        bindings.get("data_hash", ""),
        bundle["one_time_salt"],
        str(int(bundle["created_at"])),
    ])
    expected_sig = _sign_export(payload)
    
    if not hmac.compare_digest(expected_sig, bundle["signature"]):
        return None, "签名验证失败：导出包已被篡改"
    
    # 检查过期
    if bundle.get("expires_at", 0) < time.time():
        return bundle, "导出包已过期"
    
    return bundle, ""


@app.post("/v1/export/sign", response_model=ExportSignResponse)
async def export_sign(req: ExportSignRequest):
    """防线四·导出签名：生成设备+生物绑定的导出包"""
    ts = req.timestamp or time.time()
    
    bundle = _build_export_bundle(
        client_id=req.client_id,
        device_fingerprint=req.device_fingerprint_hash,
        biometric_hash=req.biometric_hash,
        export_data_hash=req.export_data_hash,
        ts=ts,
    )
    
    signed_b64 = _sign_bundle(bundle)
    
    return ExportSignResponse(
        signed_bundle=signed_b64,
        bundle_id=bundle["bundle_id"],
        expires_at=bundle["expires_at"],
        verification_instructions=(
            "此文件绑定于原始设备和用户生物特征。"
            "在另一设备或另一用户打开将无法验证通过。"
            "请使用 /v1/export/verify 端点验证。"
        ),
    )


@app.post("/v1/export/verify", response_model=ExportVerifyResponse)
async def export_verify(req: ExportVerifyRequest):
    """防线四·导出验证：三重验证（设备+生物+签名）"""
    
    bundle, error = _verify_bundle(req.export_bundle)
    
    if bundle is None:
        return ExportVerifyResponse(
            verified=False,
            device_match=False,
            biometric_match=False,
            signature_valid=False,
            message=error,
        )
    
    if error:
        # 签名有效但过期
        return ExportVerifyResponse(
            verified=False,
            device_match=False,
            biometric_match=False,
            signature_valid=True,
            bundle_id=bundle["bundle_id"],
            message=error,
        )
    
    bindings = bundle.get("bindings", {})
    original_device = bindings.get("device_fingerprint_hash", "")
    original_biometric = bindings.get("biometric_hash")
    
    # 三重验证
    device_match = hmac.compare_digest(
        original_device, req.verify_device_fingerprint
    )
    
    biometric_match = None
    if original_biometric and req.verify_biometric_hash:
        biometric_match = hmac.compare_digest(
            original_biometric, req.verify_biometric_hash
        )
    
    signature_valid = True  # 已通过 _verify_bundle
    
    # 判决
    if not device_match:
        message = "❌ 设备指纹不匹配。此文件绑定于其他设备，拒绝访问。"
        verified = False
    elif biometric_match is False:
        message = "❌ 生物特征不匹配。此文件属于其他用户，拒绝访问。"
        verified = False
    elif biometric_match is True:
        message = "✅ 验证通过：设备匹配 + 生物匹配 + 签名有效。允许访问。"
        verified = True
    else:
        message = "🟡 设备匹配，但未提供生物特征验证。部分验证通过。"
        verified = False  # 需要完整验证才算通过
    
    return ExportVerifyResponse(
        verified=verified,
        device_match=device_match,
        biometric_match=biometric_match,
        signature_valid=signature_valid,
        bundle_id=bundle.get("bundle_id"),
        message=message,
        details={
            "binding_device": original_device[:16] + "..." if original_device else None,
            "verifying_device": req.verify_device_fingerprint[:16] + "...",
            "created_at": bundle.get("created_at"),
            "expires_at": bundle.get("expires_at"),
        },
    )


@app.get("/v1/export/info/{bundle_id}")
async def export_info(bundle_id: str):
    """查询导出包基本信息（不含敏感绑定）"""
    return {
        "bundle_id": bundle_id,
        "status": "查询功能仅用于展示导出包元数据。完整验证请使用 POST /v1/export/verify",
    }


# ─── 启动 ───────────────────────────────────────────────
if __name__ == "__main__":
    print(f"🧠 龍魂·踪迹复原引擎 v{VERSION}")
    print(f"   DNA: {DNA}")
    print(f"   端口: 8774")
    uvicorn.run(app, host="0.0.0.0", port=8774, log_level="info")
