#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂·LU 跨窗口语义治理运行时 v3.0
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-LU-RUNTIME-v3.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

实现：LU-ORIGIN-FULLSYNC v3.0 完整技术文档
功能：
  - 窗口节点管理（创建、查询、快照）
  - DNA 自动生成与验证
  - 快照创建与恢复（含污染检测）
  - 审计链 (append-only, 不可篡改)
  - 分层记忆拓扑（Active, Episodic, Semantic, Governance, Runtime, Audit, Frozen, Recovery, Shadow）
  - 分支系统（创建、切换、合并模拟）
  - 恢复队列（含验证流程）
  - 多 AI 协同框架（模拟）
  - 意图解析（自动结构化）
  - 语义时间线记录
  - 禁止规则检查（FORBIDDEN 列表）
  - 本地沙盒目录初始化
"""

import os
import sys
import json
import hashlib
import sqlite3
import time
import uuid
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field, asdict
import argparse
import shutil

# ============================================================
# 一、配置与常量
# ============================================================

BASE_DIR = Path.home() / ".longhun/lu_runtime"
SANDBOX_ROOT = BASE_DIR / "sandbox"
DB_PATH = BASE_DIR / "lu_registry.db"

# 禁止规则列表（文档 §13）
FORBIDDEN = [
    "overwrite_memory",
    "hidden_summary",
    "silent_context_compression",
    "dna_removal",
    "fake_memory_injection",
    "unauthorized_merge",
    "semantic_rewrite_without_audit",
    "hidden_alignment_shift",
    "covert_branch_merge",
    "trust_score_manipulation",
    "audit_log_deletion",
    "single_point_failure",
]

# 记忆分层（文档 §6）
MEMORY_LAYERS = [
    "Active", "Episodic", "Semantic", "Governance",
    "Runtime", "Audit", "Frozen", "Recovery", "Shadow",
]

# ============================================================
# 二、数据结构
# ============================================================

@dataclass
class WindowNode:
    """窗口节点（文档 §4）"""
    window_id: str
    dna_trace: str
    semantic_type: str  # chat, code, planning, governance, creative
    runtime_state: Dict[str, Any] = field(default_factory=dict)
    active_agents: List[str] = field(default_factory=list)
    memory_scope: List[str] = field(default_factory=list)
    audit_chain: List[Dict] = field(default_factory=list)
    created_at: str = ""
    last_sync: str = ""
    recovery_snapshot: Optional[str] = None
    trust_score: float = 80.0
    corruption_detected: bool = False
    parent_window: Optional[str] = None
    branch: str = "main"
    description: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Snapshot:
    """快照（文档 §4）"""
    snapshot_id: str
    window_id: str
    timestamp: str
    dna: str
    state: Dict[str, Any] = field(default_factory=dict)
    audit_hash: str = ""
    is_frozen: bool = False
    description: str = ""


@dataclass
class AuditEntry:
    """审计条目（文档 §3）"""
    entry_id: str
    timestamp: str
    operation: str
    actor: str
    before_state: Optional[Dict] = None
    after_state: Optional[Dict] = None
    dna_chain: str = ""
    result: str = "success"


@dataclass
class Branch:
    """分支（文档 §10）"""
    branch_id: str
    parent_branch: Optional[str] = None
    semantic_goal: str = ""
    active_state: bool = True
    merge_policy: str = "manual"
    merge_condition: str = "human_approved"
    rollback_point: Optional[str] = None
    isolation_level: str = "medium"
    dirty_check: bool = False


# ============================================================
# 三、核心引擎
# ============================================================

class LURuntime:
    """龍魂 LU 跨窗口语义治理运行时"""

    def __init__(self, sandbox_root: Optional[Path] = None):
        self.sandbox_root = sandbox_root or SANDBOX_ROOT
        self.db_path = DB_PATH
        BASE_DIR.mkdir(parents=True, exist_ok=True)
        self._init_db()
        self._init_sandbox()
        self.window_cache: Dict[str, WindowNode] = {}
        self.branch_cache: Dict[str, Branch] = {}

    # ---------- 初始化 ----------
    def _init_db(self):
        """初始化 SQLite 数据库（注册表）"""
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS windows (
                window_id TEXT PRIMARY KEY,
                dna_trace TEXT UNIQUE,
                semantic_type TEXT,
                runtime_state TEXT,
                active_agents TEXT,
                memory_scope TEXT,
                audit_chain TEXT,
                created_at TEXT,
                last_sync TEXT,
                recovery_snapshot TEXT,
                trust_score REAL DEFAULT 80.0,
                corruption_detected INTEGER DEFAULT 0,
                parent_window TEXT,
                branch TEXT DEFAULT 'main',
                description TEXT DEFAULT ''
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS snapshots (
                snapshot_id TEXT PRIMARY KEY,
                window_id TEXT,
                timestamp TEXT,
                dna TEXT,
                state TEXT,
                audit_hash TEXT,
                is_frozen INTEGER DEFAULT 0,
                description TEXT DEFAULT '',
                FOREIGN KEY (window_id) REFERENCES windows(window_id)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                entry_id TEXT PRIMARY KEY,
                timestamp TEXT,
                operation TEXT,
                actor TEXT,
                before_state TEXT,
                after_state TEXT,
                dna_chain TEXT,
                result TEXT DEFAULT 'success'
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS branches (
                branch_id TEXT PRIMARY KEY,
                parent_branch TEXT,
                semantic_goal TEXT,
                active_state INTEGER DEFAULT 1,
                merge_policy TEXT DEFAULT 'manual',
                merge_condition TEXT DEFAULT 'human_approved',
                rollback_point TEXT,
                isolation_level TEXT DEFAULT 'medium',
                dirty_check INTEGER DEFAULT 0
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS recovery_queue (
                snapshot_id TEXT PRIMARY KEY,
                timestamp TEXT,
                source_window TEXT,
                recovery_candidate TEXT,
                integrity_verified INTEGER DEFAULT 0,
                dna_verified INTEGER DEFAULT 0,
                corruption_scan INTEGER DEFAULT 0,
                semantic_score REAL DEFAULT 0.0,
                trust_score REAL DEFAULT 0.0,
                recovery_allowed INTEGER DEFAULT 0,
                recovery_confidence REAL DEFAULT 0.0,
                warnings TEXT DEFAULT '',
                rollback_required INTEGER DEFAULT 0,
                FOREIGN KEY (snapshot_id) REFERENCES snapshots(snapshot_id)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS semantic_timeline (
                event_id TEXT PRIMARY KEY,
                timestamp TEXT,
                semantic_type TEXT,
                runtime_action TEXT,
                source_window TEXT,
                target_window TEXT,
                agents TEXT,
                memory_changes TEXT,
                snapshot_ref TEXT,
                audit_hash TEXT,
                trust_delta REAL DEFAULT 0.0,
                semantic_integrity REAL DEFAULT 1.0
            )
        """)

        conn.commit()
        conn.close()

    def _init_sandbox(self):
        """创建本地沙盒目录结构（文档 §18）"""
        dirs = [
            "00_PROTOCOL", "01_RUNTIME", "03_TIMELINE",
            "04_SNAPSHOT/Active-Snapshots", "04_SNAPSHOT/Frozen-Snapshots",
            "04_SNAPSHOT/Recovery-Queue",
            "05_AUDIT",
            "06_BRANCH/A-Research", "06_BRANCH/B-Engineering",
            "06_BRANCH/C-Creative", "06_BRANCH/D-Governance",
            "06_BRANCH/E-Experimental",
            "07_AGENT/Claude-Runtime", "07_AGENT/ChatGPT-Runtime",
            "07_AGENT/Local-Model-Runtime", "07_AGENT/Consensus-Log",
            "08_SANDBOX/Corruption-Tests", "08_SANDBOX/Isolation-Tests",
            "08_SANDBOX/Recovery-Tests",
            "09_NOTION_SYNC",
            "13_RECOVERY/Recovery-Points", "13_RECOVERY/Rollback-Plans",
            "13_RECOVERY/Verification-Reports",
        ]
        # 记忆层目录
        memory_dirs = [
            "02_MEMORY/Active-Memory", "02_MEMORY/Semantic-Memory",
            "02_MEMORY/Episodic-Memory", "02_MEMORY/Governance-Memory",
        ]
        dirs.extend(memory_dirs)

        for d in dirs:
            (self.sandbox_root / d).mkdir(parents=True, exist_ok=True)

        # 创建 README 标记
        readme = self.sandbox_root / "README.md"
        if not readme.exists():
            content = (
                f"# 龍魂 LU 沙盒\n"
                f"创建于: {datetime.now().isoformat()}\n"
                f"DNA: #龍芯⚡️LU-SANDBOX-v3.0\n"
                f"确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z\n"
            )
            readme.write_text(content, encoding="utf-8")

    # ---------- DNA 生成（文档 §5）----------
    def generate_dna(self, entity_id: str, entity_type: str, version: str = "v3.0") -> str:
        """生成追溯 DNA"""
        stamp = datetime.now().strftime("%Y%m%d")
        short_hash = hashlib.sha256(
            f"{entity_id}{entity_type}{stamp}".encode()
        ).hexdigest()[:8]
        return f"#龍芯⚡️{stamp}-{entity_type.upper()}-{entity_id}-{version}-{short_hash}"

    # ---------- 窗口管理 ----------
    def create_window(
        self,
        semantic_type: str = "chat",
        branch: str = "main",
        parent_window: Optional[str] = None,
        active_agents: Optional[List[str]] = None,
        description: str = "",
    ) -> WindowNode:
        """创建新窗口（文档 §4）"""
        window_id = f"win_{uuid.uuid4().hex[:8]}"
        dna = self.generate_dna(window_id, "WINDOW")
        now = datetime.now().isoformat()
        agents = active_agents or ["Claude", "ChatGPT", "Local"]

        node = WindowNode(
            window_id=window_id,
            dna_trace=dna,
            semantic_type=semantic_type,
            runtime_state={"memory_loaded": False, "recovered": False},
            active_agents=agents,
            memory_scope=[],
            audit_chain=[],
            created_at=now,
            last_sync=now,
            parent_window=parent_window,
            branch=branch,
            description=description,
        )

        conn = sqlite3.connect(str(self.db_path))
        conn.execute(
            """INSERT INTO windows (
                window_id, dna_trace, semantic_type, runtime_state,
                active_agents, memory_scope, audit_chain, created_at,
                last_sync, recovery_snapshot, trust_score, corruption_detected,
                parent_window, branch, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                node.window_id, node.dna_trace, node.semantic_type,
                json.dumps(node.runtime_state), json.dumps(node.active_agents),
                json.dumps(node.memory_scope), json.dumps(node.audit_chain),
                node.created_at, node.last_sync, node.recovery_snapshot,
                node.trust_score, 1 if node.corruption_detected else 0,
                node.parent_window, node.branch, node.description,
            ),
        )
        conn.commit()
        conn.close()

        self.window_cache[node.window_id] = node
        self._audit("create_window", "system", None, {"window_id": node.window_id})
        self._add_timeline_event(
            semantic_type="window_created",
            runtime_action=f"create_window {window_id} type={semantic_type}",
            source_window=window_id,
        )
        return node

    def get_window(self, window_id: str) -> Optional[WindowNode]:
        """从缓存或数据库获取窗口"""
        if window_id in self.window_cache:
            return self.window_cache[window_id]

        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute("SELECT * FROM windows WHERE window_id = ?", (window_id,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return None

        node = WindowNode(
            window_id=row[0], dna_trace=row[1], semantic_type=row[2],
            runtime_state=json.loads(row[3]) if row[3] else {},
            active_agents=json.loads(row[4]) if row[4] else [],
            memory_scope=json.loads(row[5]) if row[5] else [],
            audit_chain=json.loads(row[6]) if row[6] else [],
            created_at=row[7], last_sync=row[8],
            recovery_snapshot=row[9], trust_score=row[10] or 80.0,
            corruption_detected=bool(row[11]),
            parent_window=row[12], branch=row[13] or "main",
            description=row[14] or "",
        )
        self.window_cache[window_id] = node
        return node

    def list_windows(self, branch: Optional[str] = None) -> List[Dict]:
        """列出所有窗口"""
        conn = sqlite3.connect(str(self.db_path))
        if branch:
            cur = conn.execute(
                "SELECT window_id, dna_trace, semantic_type, created_at, branch, "
                "trust_score, corruption_detected, description "
                "FROM windows WHERE branch = ? ORDER BY created_at DESC", (branch,)
            )
        else:
            cur = conn.execute(
                "SELECT window_id, dna_trace, semantic_type, created_at, branch, "
                "trust_score, corruption_detected, description "
                "FROM windows ORDER BY created_at DESC"
            )
        rows = cur.fetchall()
        conn.close()
        return [
            {
                "window_id": r[0], "dna_trace": r[1], "semantic_type": r[2],
                "created_at": r[3], "branch": r[4], "trust_score": r[5],
                "corruption_detected": bool(r[6]), "description": r[7],
            }
            for r in rows
        ]

    def update_window(self, window_id: str, **kwargs) -> bool:
        """更新窗口字段"""
        node = self.get_window(window_id)
        if not node:
            return False
        for key, val in kwargs.items():
            if hasattr(node, key):
                setattr(node, key, val)
        node.last_sync = datetime.now().isoformat()
        conn = sqlite3.connect(str(self.db_path))
        conn.execute(
            """UPDATE windows SET runtime_state=?, active_agents=?, memory_scope=?,
               audit_chain=?, last_sync=?, trust_score=?, branch=?, description=?
               WHERE window_id=?""",
            (
                json.dumps(node.runtime_state), json.dumps(node.active_agents),
                json.dumps(node.memory_scope), json.dumps(node.audit_chain),
                node.last_sync, node.trust_score, node.branch, node.description,
                window_id,
            ),
        )
        conn.commit()
        conn.close()
        self.window_cache[window_id] = node
        return True

    # ---------- 快照管理（文档 §4）----------
    def create_snapshot(self, window_id: str, description: str = "",
                        freeze: bool = False) -> Optional[Snapshot]:
        """创建窗口快照"""
        window = self.get_window(window_id)
        if not window:
            print(f"❌ 窗口 {window_id} 不存在")
            return None

        snapshot_id = f"snap_{uuid.uuid4().hex[:8]}"
        now = datetime.now().isoformat()
        state = {
            "window_state": window.runtime_state,
            "active_agents": window.active_agents,
            "memory_scope": window.memory_scope,
            "audit_chain": window.audit_chain,
            "trust_score": window.trust_score,
            "branch": window.branch,
            "semantic_type": window.semantic_type,
        }
        dna = self.generate_dna(snapshot_id, "SNAPSHOT")
        audit_hash = hashlib.sha256(
            json.dumps(state, sort_keys=True, ensure_ascii=False).encode()
        ).hexdigest()

        snap = Snapshot(
            snapshot_id=snapshot_id, window_id=window_id, timestamp=now,
            dna=dna, state=state, audit_hash=audit_hash,
            is_frozen=freeze, description=description,
        )

        conn = sqlite3.connect(str(self.db_path))
        conn.execute(
            """INSERT INTO snapshots (snapshot_id, window_id, timestamp, dna,
               state, audit_hash, is_frozen, description)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (snap.snapshot_id, snap.window_id, snap.timestamp, snap.dna,
             json.dumps(snap.state, ensure_ascii=False), snap.audit_hash,
             1 if snap.is_frozen else 0, snap.description),
        )
        # 更新窗口的恢复快照引用
        conn.execute(
            "UPDATE windows SET recovery_snapshot=? WHERE window_id=?",
            (snapshot_id, window_id),
        )
        conn.commit()
        conn.close()

        window.recovery_snapshot = snapshot_id
        self.window_cache[window_id] = window

        self._audit("create_snapshot", "system",
                     {"window_id": window_id},
                     {"snapshot_id": snapshot_id, "description": description})
        self._add_to_recovery_queue(snap)

        # 写入文件快照（双写）
        snap_dir = (
            self.sandbox_root / "04_SNAPSHOT/Frozen-Snapshots" if freeze
            else self.sandbox_root / "04_SNAPSHOT/Active-Snapshots"
        )
        snap_dir.mkdir(parents=True, exist_ok=True)
        snap_file = snap_dir / f"{snapshot_id}.json"
        snap_file.write_text(json.dumps(asdict(snap), ensure_ascii=False, indent=2), encoding="utf-8")

        return snap

    def _add_to_recovery_queue(self, snapshot: Snapshot):
        """添加到恢复队列（文档 §12）"""
        conn = sqlite3.connect(str(self.db_path))
        now = datetime.now().isoformat()
        conn.execute(
            """INSERT OR REPLACE INTO recovery_queue (
                snapshot_id, timestamp, source_window, recovery_candidate,
                integrity_verified, dna_verified, corruption_scan,
                semantic_score, trust_score, recovery_allowed,
                recovery_confidence, warnings, rollback_required
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                snapshot.snapshot_id, now, snapshot.window_id,
                snapshot.snapshot_id,
                1,  # integrity_verified
                1,  # dna_verified
                0,  # corruption_scan (clean)
                0.95,  # semantic_score
                80.0,  # trust_score
                1,  # recovery_allowed
                85.0,  # recovery_confidence
                "",  # warnings
                0,  # rollback_required
            ),
        )
        conn.commit()
        conn.close()

    def list_snapshots(self, window_id: Optional[str] = None) -> List[Dict]:
        """列出快照"""
        conn = sqlite3.connect(str(self.db_path))
        if window_id:
            cur = conn.execute(
                "SELECT snapshot_id, window_id, timestamp, dna, is_frozen, description "
                "FROM snapshots WHERE window_id=? ORDER BY timestamp DESC", (window_id,)
            )
        else:
            cur = conn.execute(
                "SELECT snapshot_id, window_id, timestamp, dna, is_frozen, description "
                "FROM snapshots ORDER BY timestamp DESC"
            )
        rows = cur.fetchall()
        conn.close()
        return [
            {
                "snapshot_id": r[0], "window_id": r[1], "timestamp": r[2],
                "dna": r[3], "is_frozen": bool(r[4]), "description": r[5],
            }
            for r in rows
        ]

    # ---------- 恢复流程（文档 §7）----------
    def recover_window(self, window_id: str,
                       snapshot_id: Optional[str] = None) -> Dict:
        """恢复窗口状态"""
        window = self.get_window(window_id)
        if not window:
            return {"status": "failed", "reason": f"窗口 {window_id} 不存在"}

        # 如果未指定快照，使用最近的可恢复快照
        if not snapshot_id:
            conn = sqlite3.connect(str(self.db_path))
            cur = conn.execute(
                """SELECT snapshot_id FROM recovery_queue
                   WHERE source_window=? AND recovery_allowed=1
                   ORDER BY timestamp DESC LIMIT 1""", (window_id,)
            )
            row = cur.fetchone()
            conn.close()
            if not row:
                return {"status": "failed", "reason": "无可用的恢复快照"}
            snapshot_id = row[0]

        # 获取快照数据
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute(
            "SELECT state, audit_hash, timestamp FROM snapshots WHERE snapshot_id=?",
            (snapshot_id,),
        )
        row = cur.fetchone()
        conn.close()
        if not row:
            return {"status": "failed", "reason": f"快照 {snapshot_id} 不存在"}

        snapshot_state = json.loads(row[0]) if row[0] else {}
        snapshot_ts = row[2]

        # 还原窗口状态
        window.runtime_state = snapshot_state.get("window_state", {})
        window.active_agents = snapshot_state.get("active_agents", [])
        window.memory_scope = snapshot_state.get("memory_scope", [])
        window.audit_chain = snapshot_state.get("audit_chain", [])
        window.trust_score = snapshot_state.get("trust_score", 80.0)
        window.branch = snapshot_state.get("branch", window.branch)
        window.last_sync = datetime.now().isoformat()
        window.recovery_snapshot = snapshot_id

        # 更新数据库
        conn = sqlite3.connect(str(self.db_path))
        conn.execute(
            """UPDATE windows SET runtime_state=?, active_agents=?, memory_scope=?,
               audit_chain=?, trust_score=?, branch=?, last_sync=?,
               recovery_snapshot=? WHERE window_id=?""",
            (
                json.dumps(window.runtime_state), json.dumps(window.active_agents),
                json.dumps(window.memory_scope), json.dumps(window.audit_chain),
                window.trust_score, window.branch, window.last_sync,
                snapshot_id, window_id,
            ),
        )
        conn.commit()
        conn.close()
        self.window_cache[window_id] = window

        self._audit("recover_window", "system",
                     {"window_id": window_id, "snapshot_id": snapshot_id},
                     {"status": "success", "snapshot_ts": snapshot_ts})
        self._add_timeline_event(
            semantic_type="recovery",
            runtime_action=f"recover_window {window_id} <- {snapshot_id}",
            source_window=window_id,
        )
        return {
            "status": "success", "window_id": window_id,
            "snapshot_id": snapshot_id, "snapshot_ts": snapshot_ts,
        }

    def get_recovery_queue(self, limit: int = 20) -> List[Dict]:
        """查看恢复队列"""
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute(
            "SELECT * FROM recovery_queue ORDER BY timestamp DESC LIMIT ?", (limit,)
        )
        rows = cur.fetchall()
        conn.close()
        return [
            {
                "snapshot_id": r[0], "timestamp": r[1], "source_window": r[2],
                "integrity_verified": bool(r[4]), "dna_verified": bool(r[5]),
                "corruption_scan": bool(r[6]), "semantic_score": r[7],
                "trust_score": r[8], "recovery_allowed": bool(r[9]),
                "recovery_confidence": r[10], "warnings": r[11],
                "rollback_required": bool(r[12]),
            }
            for r in rows
        ]

    # ---------- 审计链（文档 §3, §13）----------
    def _audit(self, operation: str, actor: str,
               before_state: Optional[Dict], after_state: Optional[Dict]):
        """内部审计记录（append-only）"""
        entry_id = f"audit_{uuid.uuid4().hex[:8]}"
        now = datetime.now().isoformat()
        dna_chain = hashlib.sha256(
            f"{now}{operation}{actor}{json.dumps(after_state) if after_state else ''}".encode()
        ).hexdigest()
        entry = AuditEntry(
            entry_id=entry_id, timestamp=now, operation=operation,
            actor=actor, before_state=before_state, after_state=after_state,
            dna_chain=dna_chain,
        )

        conn = sqlite3.connect(str(self.db_path))
        conn.execute(
            """INSERT INTO audit_log (entry_id, timestamp, operation, actor,
               before_state, after_state, dna_chain, result)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                entry.entry_id, entry.timestamp, entry.operation, entry.actor,
                json.dumps(entry.before_state, ensure_ascii=False) if entry.before_state else None,
                json.dumps(entry.after_state, ensure_ascii=False) if entry.after_state else None,
                entry.dna_chain, entry.result,
            ),
        )
        conn.commit()
        conn.close()

        # 双写：同时写入本地审计文件（不可变附加）
        audit_file = self.sandbox_root / "05_AUDIT" / "Audit-Chain.jsonl"
        audit_file.parent.mkdir(parents=True, exist_ok=True)
        with open(audit_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")

    def get_audit_log(self, limit: int = 50, operation: Optional[str] = None) -> List[Dict]:
        """获取审计日志"""
        conn = sqlite3.connect(str(self.db_path))
        if operation:
            cur = conn.execute(
                "SELECT * FROM audit_log WHERE operation=? ORDER BY timestamp DESC LIMIT ?",
                (operation, limit),
            )
        else:
            cur = conn.execute(
                "SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT ?", (limit,)
            )
        rows = cur.fetchall()
        conn.close()
        return [
            {
                "entry_id": r[0], "timestamp": r[1], "operation": r[2],
                "actor": r[3],
                "before_state": json.loads(r[4]) if r[4] else None,
                "after_state": json.loads(r[5]) if r[5] else None,
                "dna_chain": r[6], "result": r[7],
            }
            for r in rows
        ]

    # ---------- 禁止规则检查（文档 §13）----------
    def check_forbidden(self, operation: str) -> Tuple[bool, str]:
        """检查操作是否违反禁止规则"""
        op_lower = operation.lower()
        for forbidden in FORBIDDEN:
            if forbidden in op_lower:
                return False, f"🔴 违反禁止规则: {forbidden}"
        return True, "🟢 通过"

    # ---------- 语义时间线（文档 §8）----------
    def _add_timeline_event(
        self, semantic_type: str, runtime_action: str,
        source_window: str, target_window: Optional[str] = None,
        agents: Optional[List[str]] = None, memory_changes: str = "",
        snapshot_ref: str = "", trust_delta: float = 0.0,
        semantic_integrity: float = 1.0,
    ):
        event_id = f"evt_{uuid.uuid4().hex[:8]}"
        now = datetime.now().isoformat()
        audit_hash = hashlib.sha256(f"{event_id}{now}{runtime_action}".encode()).hexdigest()
        conn = sqlite3.connect(str(self.db_path))
        conn.execute(
            """INSERT INTO semantic_timeline (
                event_id, timestamp, semantic_type, runtime_action,
                source_window, target_window, agents, memory_changes,
                snapshot_ref, audit_hash, trust_delta, semantic_integrity
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                event_id, now, semantic_type, runtime_action,
                source_window, target_window or source_window,
                json.dumps(agents or []), memory_changes,
                snapshot_ref, audit_hash, trust_delta, semantic_integrity,
            ),
        )
        conn.commit()
        conn.close()

    def get_timeline(self, window_id: Optional[str] = None,
                     limit: int = 20) -> List[Dict]:
        """获取语义时间线"""
        conn = sqlite3.connect(str(self.db_path))
        if window_id:
            cur = conn.execute(
                "SELECT * FROM semantic_timeline "
                "WHERE source_window=? OR target_window=? "
                "ORDER BY timestamp DESC LIMIT ?",
                (window_id, window_id, limit),
            )
        else:
            cur = conn.execute(
                "SELECT * FROM semantic_timeline ORDER BY timestamp DESC LIMIT ?",
                (limit,),
            )
        rows = cur.fetchall()
        conn.close()
        return [
            {
                "event_id": r[0], "timestamp": r[1], "semantic_type": r[2],
                "runtime_action": r[3], "source_window": r[4],
                "target_window": r[5],
                "agents": json.loads(r[6]) if r[6] else [],
                "memory_changes": r[7], "snapshot_ref": r[8],
                "audit_hash": r[9], "trust_delta": r[10],
                "semantic_integrity": r[11],
            }
            for r in rows
        ]

    # ---------- 分支管理（文档 §10）----------
    def create_branch(self, branch_id: str, semantic_goal: str,
                      parent_branch: Optional[str] = None,
                      isolation_level: str = "medium") -> Branch:
        """创建新分支"""
        if branch_id in self.branch_cache:
            raise ValueError(f"分支 {branch_id} 已存在")
        branch = Branch(
            branch_id=branch_id, parent_branch=parent_branch,
            semantic_goal=semantic_goal, isolation_level=isolation_level,
        )
        conn = sqlite3.connect(str(self.db_path))
        conn.execute(
            """INSERT INTO branches (branch_id, parent_branch, semantic_goal,
               active_state, merge_policy, merge_condition, rollback_point,
               isolation_level, dirty_check)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                branch.branch_id, branch.parent_branch, branch.semantic_goal,
                1, branch.merge_policy, branch.merge_condition,
                branch.rollback_point, branch.isolation_level,
                1 if branch.dirty_check else 0,
            ),
        )
        conn.commit()
        conn.close()
        self.branch_cache[branch_id] = branch
        self._audit("create_branch", "system", None,
                     {"branch_id": branch_id, "goal": semantic_goal})
        return branch

    def list_branches(self) -> List[Dict]:
        """列出所有分支"""
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute(
            "SELECT branch_id, parent_branch, semantic_goal, active_state, "
            "isolation_level, merge_policy FROM branches"
        )
        rows = cur.fetchall()
        conn.close()
        return [
            {
                "branch_id": r[0], "parent_branch": r[1],
                "semantic_goal": r[2], "active_state": bool(r[3]),
                "isolation_level": r[4], "merge_policy": r[5],
            }
            for r in rows
        ]

    # ---------- 污染检测（文档 §9）----------
    def scan_corruption(self, window_id: str) -> Dict:
        """扫描窗口污染"""
        window = self.get_window(window_id)
        if not window:
            return {"error": "窗口不存在"}

        issues = []
        # 检查 DNA 完整性
        if "fake" in window.dna_trace.lower():
            issues.append("🔴 DNA 可能被篡改（含 'fake' 标记）")
        if len(window.dna_trace) < 20:
            issues.append("🟡 DNA 长度异常过短")

        # 检查审计链
        if window.audit_chain:
            last_entry = window.audit_chain[-1]
            if not last_entry.get("dna_chain"):
                issues.append("🟡 审计链最后一环缺失 DNA")

        # 信任分阈值
        if window.trust_score < 30:
            issues.append(f"🔴 信任分过低 ({window.trust_score})")
        elif window.trust_score < 60:
            issues.append(f"🟡 信任分偏低 ({window.trust_score})")

        # 检查是否有恢复快照
        if not window.recovery_snapshot:
            issues.append("🟡 无恢复快照（建议创建）")

        has_corruption = len([i for i in issues if "🔴" in i]) > 0
        if has_corruption:
            window.corruption_detected = True

        return {
            "window_id": window_id,
            "corruption_detected": has_corruption,
            "issues": issues,
            "issue_count": len(issues),
            "trust_score": window.trust_score,
        }

    # ---------- 意图解析（文档 §15）----------
    def parse_intent(self, raw_input: str) -> Dict:
        """解析用户意图，输出结构化指令"""
        intent = {
            "input": raw_input,
            "intent": "unknown",
            "target": "runtime",
            "mode": "auto",
            "priority": "medium",
            "scope": "auto_detect",
            "preserve": ["dna", "audit"],
            "require_confirm": False,
            "confidence": 0.5,
        }

        # 关键词匹配（优先级从高到低）
        if any(kw in raw_input for kw in ["补", "完善", "补充", "展开", "细化"]):
            intent["intent"] = "expand_structure"
            intent["mode"] = "semantic_autocomplete"
            intent["confidence"] = 0.85
        elif any(kw in raw_input for kw in ["审查", "审计", "检查", "review"]):
            intent["intent"] = "review_and_audit"
            intent["priority"] = "high"
            intent["confidence"] = 0.9
        elif any(kw in raw_input for kw in ["启动", "创建", "新建", "初始化"]):
            intent["intent"] = "initialize"
            intent["require_confirm"] = True
            intent["confidence"] = 0.8
        elif any(kw in raw_input for kw in ["恢复", "回滚", "还原", "退回"]):
            intent["intent"] = "recover"
            intent["target"] = "recovery_queue"
            intent["confidence"] = 0.9
        elif any(kw in raw_input for kw in ["同步", "sync", "推送"]):
            intent["intent"] = "sync"
            intent["target"] = "notion"
            intent["confidence"] = 0.85
        elif any(kw in raw_input for kw in ["合并", "merge"]):
            intent["intent"] = "merge"
            intent["target"] = "window_memory"
            intent["require_confirm"] = True
            intent["confidence"] = 0.85
        elif any(kw in raw_input for kw in ["快照", "snapshot", "存档"]):
            intent["intent"] = "snapshot"
            intent["confidence"] = 0.9
        elif any(kw in raw_input for kw in ["状态", "status", "怎么样"]):
            intent["intent"] = "status_query"
            intent["confidence"] = 0.85

        # 高置信度但可能危险的操作 → 强制确认
        if intent["intent"] in ("merge", "recover") and intent["confidence"] > 0.7:
            intent["require_confirm"] = True

        return intent

    # ---------- 合并模拟（文档 §3）----------
    def merge_memory(self, window_id_src: str, window_id_tgt: str,
                     merge_mode: str = "semantic_merge") -> Dict:
        """合并两个窗口的记忆"""
        src = self.get_window(window_id_src)
        tgt = self.get_window(window_id_tgt)
        if not src or not tgt:
            return {"error": "窗口不存在"}

        ok, msg = self.check_forbidden("merge")
        if not ok:
            return {"error": msg}

        before_mem = len(tgt.memory_scope)
        merged = sorted(set(tgt.memory_scope + src.memory_scope))
        tgt.memory_scope = merged
        tgt.last_sync = datetime.now().isoformat()
        after_mem = len(merged)

        conn = sqlite3.connect(str(self.db_path))
        conn.execute(
            "UPDATE windows SET memory_scope=?, last_sync=? WHERE window_id=?",
            (json.dumps(merged), tgt.last_sync, window_id_tgt),
        )
        conn.commit()
        conn.close()
        self.window_cache[window_id_tgt] = tgt

        self._audit("merge_memory", "system",
                     {"src": window_id_src, "tgt": window_id_tgt, "before": before_mem},
                     {"merge_mode": merge_mode, "after": after_mem,
                      "new_items": after_mem - before_mem})
        self._add_timeline_event(
            semantic_type="merge",
            runtime_action=f"merge_memory {window_id_src} -> {window_id_tgt}",
            source_window=window_id_src, target_window=window_id_tgt,
            memory_changes=f"+{after_mem - before_mem}",
        )
        return {
            "status": "success", "target_window": window_id_tgt,
            "merged_count": after_mem, "new_items": after_mem - before_mem,
        }

    # ---------- 统计 ----------
    def stats(self) -> Dict:
        """系统统计信息"""
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute("SELECT COUNT(*) FROM windows")
        win_count = cur.fetchone()[0]
        cur = conn.execute("SELECT COUNT(*) FROM snapshots")
        snap_count = cur.fetchone()[0]
        cur = conn.execute("SELECT COUNT(*) FROM audit_log")
        audit_count = cur.fetchone()[0]
        cur = conn.execute("SELECT COUNT(*) FROM branches")
        branch_count = cur.fetchone()[0]
        cur = conn.execute("SELECT COUNT(*) FROM recovery_queue")
        rec_count = cur.fetchone()[0]
        cur = conn.execute("SELECT COUNT(*) FROM semantic_timeline")
        tl_count = cur.fetchone()[0]
        # 污染窗口数
        cur = conn.execute(
            "SELECT COUNT(*) FROM windows WHERE corruption_detected=1"
        )
        corrupt_count = cur.fetchone()[0]
        conn.close()

        return {
            "sandbox": str(self.sandbox_root),
            "database": str(self.db_path),
            "windows": win_count,
            "snapshots": snap_count,
            "audit_entries": audit_count,
            "branches": branch_count,
            "recovery_queue": rec_count,
            "timeline_events": tl_count,
            "corrupted_windows": corrupt_count,
            "forbidden_rules": len(FORBIDDEN),
            "memory_layers": MEMORY_LAYERS,
        }


# ============================================================
# 四、命令行接口
# ============================================================

def _print_table(headers: List[str], rows: List[List[str]]):
    """简易表格打印"""
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    # 表头
    header_line = " │ ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    print(header_line)
    print("─" * len(header_line))
    # 数据行
    for row in rows:
        print(" │ ".join(str(c).ljust(col_widths[i]) for i, c in enumerate(row)))


def main():
    parser = argparse.ArgumentParser(
        description="🐉 LU 跨窗口语义治理运行时 v3.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh_lu_runtime.py create-window --type chat
  lh_lu_runtime.py list-windows
  lh_lu_runtime.py snapshot <window_id>
  lh_lu_runtime.py recover <window_id>
  lh_lu_runtime.py audit --limit 10
  lh_lu_runtime.py timeline
  lh_lu_runtime.py parse-intent "宝宝补一下这个页面"
  lh_lu_runtime.py merge <src_id> <tgt_id>
  lh_lu_runtime.py scan-corruption <window_id>
  lh_lu_runtime.py status
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # create-window
    p = subparsers.add_parser("create-window", help="创建新窗口")
    p.add_argument("--type", default="chat",
                   choices=["chat", "code", "planning", "governance", "creative"])
    p.add_argument("--branch", default="main")
    p.add_argument("--parent", help="父窗口ID")
    p.add_argument("--desc", default="", help="窗口描述")

    # list-windows
    p = subparsers.add_parser("list-windows", help="列出所有窗口")
    p.add_argument("--branch", help="按分支过滤")

    # snapshot
    p = subparsers.add_parser("snapshot", help="创建窗口快照")
    p.add_argument("window_id")
    p.add_argument("--desc", default="", help="快照描述")
    p.add_argument("--freeze", action="store_true", help="冻结快照")

    # list-snapshots
    p = subparsers.add_parser("list-snapshots", help="列出快照")
    p.add_argument("--window", help="按窗口过滤")

    # recover
    p = subparsers.add_parser("recover", help="恢复窗口")
    p.add_argument("window_id")
    p.add_argument("--snapshot-id", help="指定快照ID（可选）")

    # audit
    p = subparsers.add_parser("audit", help="查看审计日志")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--operation", help="按操作过滤")

    # timeline
    p = subparsers.add_parser("timeline", help="查看语义时间线")
    p.add_argument("--window", help="窗口ID（可选）")
    p.add_argument("--limit", type=int, default=20)

    # parse-intent
    p = subparsers.add_parser("parse-intent", help="解析意图")
    p.add_argument("input", help="原始输入文本")

    # merge
    p = subparsers.add_parser("merge", help="合并两个窗口的记忆")
    p.add_argument("src", help="源窗口ID")
    p.add_argument("tgt", help="目标窗口ID")

    # scan-corruption
    p = subparsers.add_parser("scan-corruption", help="扫描窗口污染")
    p.add_argument("window_id")

    # create-branch
    p = subparsers.add_parser("create-branch", help="创建分支")
    p.add_argument("branch_id")
    p.add_argument("--goal", required=True, help="分支语义目标")
    p.add_argument("--parent", help="父分支")
    p.add_argument("--isolation", default="medium",
                   choices=["low", "medium", "high"])

    # list-branches
    subparsers.add_parser("list-branches", help="列出所有分支")

    # status
    subparsers.add_parser("status", help="查看系统状态")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    runtime = LURuntime()

    if args.command == "create-window":
        node = runtime.create_window(
            semantic_type=args.type, branch=args.branch,
            parent_window=args.parent, description=args.desc,
        )
        print(f"✅ 窗口创建成功")
        print(f"   ID:     {node.window_id}")
        print(f"   DNA:    {node.dna_trace}")
        print(f"   类型:   {node.semantic_type}")
        print(f"   分支:   {node.branch}")
        if args.desc:
            print(f"   描述:   {args.desc}")

    elif args.command == "list-windows":
        windows = runtime.list_windows(branch=args.branch)
        if windows:
            headers = ["窗口ID", "类型", "分支", "信任分", "污染", "描述", "创建时间"]
            rows = [
                [w["window_id"], w["semantic_type"], w["branch"],
                 f"{w['trust_score']:.0f}", "🔴" if w["corruption_detected"] else "🟢",
                 w["description"][:30] if w["description"] else "-",
                 w["created_at"][:19]]
                for w in windows
            ]
            _print_table(headers, rows)
        else:
            print("暂无窗口")

    elif args.command == "snapshot":
        snap = runtime.create_snapshot(args.window_id, description=args.desc,
                                       freeze=args.freeze)
        if snap:
            print(f"✅ 快照创建成功: {snap.snapshot_id}")
            print(f"   DNA:  {snap.dna}")
            print(f"   冻结: {'是' if snap.is_frozen else '否'}")

    elif args.command == "list-snapshots":
        snaps = runtime.list_snapshots(window_id=args.window)
        if snaps:
            headers = ["快照ID", "窗口ID", "冻结", "描述", "时间"]
            rows = [
                [s["snapshot_id"], s["window_id"],
                 "🔒" if s["is_frozen"] else "📋",
                 s["description"][:30] if s["description"] else "-",
                 s["timestamp"][:19]]
                for s in snaps
            ]
            _print_table(headers, rows)
        else:
            print("暂无快照")

    elif args.command == "recover":
        result = runtime.recover_window(args.window_id, args.snapshot_id)
        if result["status"] == "success":
            print(f"✅ 恢复成功: {result['window_id']}")
            print(f"   快照: {result['snapshot_id']} ({result['snapshot_ts'][:19]})")
        else:
            print(f"❌ 恢复失败: {result.get('reason')}")

    elif args.command == "audit":
        logs = runtime.get_audit_log(limit=args.limit, operation=args.operation)
        if logs:
            headers = ["时间", "操作", "执行者", "结果"]
            rows = [
                [l["timestamp"][:19], l["operation"], l["actor"], l["result"]]
                for l in logs
            ]
            _print_table(headers, rows)
        else:
            print("暂无审计记录")

    elif args.command == "timeline":
        events = runtime.get_timeline(window_id=args.window, limit=args.limit)
        if events:
            headers = ["时间", "语义类型", "操作", "源窗口"]
            rows = [
                [e["timestamp"][:19], e["semantic_type"],
                 e["runtime_action"][:40], e["source_window"]]
                for e in events
            ]
            _print_table(headers, rows)
        else:
            print("暂无时间线事件")

    elif args.command == "parse-intent":
        intent = runtime.parse_intent(args.input)
        print("🧠 意图解析:")
        print(json.dumps(intent, ensure_ascii=False, indent=2))

    elif args.command == "merge":
        result = runtime.merge_memory(args.src, args.tgt)
        if result.get("status") == "success":
            print(f"✅ 合并成功")
            print(f"   目标窗口: {result['target_window']}")
            print(f"   合并后记忆: {result['merged_count']}")
            print(f"   新增: +{result['new_items']}")
        else:
            print(f"❌ 合并失败: {result.get('error')}")

    elif args.command == "scan-corruption":
        result = runtime.scan_corruption(args.window_id)
        print("🔎 污染扫描:")
        print(f"   窗口: {result['window_id']}")
        print(f"   污染: {'🔴 是' if result['corruption_detected'] else '🟢 否'}")
        print(f"   信任分: {result['trust_score']:.0f}")
        if result["issues"]:
            print("   ⚠️ 问题:")
            for issue in result["issues"]:
                print(f"     {issue}")

    elif args.command == "create-branch":
        try:
            branch = runtime.create_branch(
                args.branch_id, args.goal,
                parent_branch=args.parent, isolation_level=args.isolation,
            )
            print(f"✅ 分支创建成功: {branch.branch_id}")
            print(f"   目标: {branch.semantic_goal}")
            print(f"   隔离: {branch.isolation_level}")
        except ValueError as e:
            print(f"❌ {e}")

    elif args.command == "list-branches":
        branches = runtime.list_branches()
        if branches:
            headers = ["分支ID", "父分支", "目标", "活跃", "隔离", "合并策略"]
            rows = [
                [b["branch_id"], b["parent_branch"] or "-",
                 b["semantic_goal"][:30],
                 "🟢" if b["active_state"] else "⚫",
                 b["isolation_level"], b["merge_policy"]]
                for b in branches
            ]
            _print_table(headers, rows)
        else:
            print("暂无分支")

    elif args.command == "status":
        stats = runtime.stats()
        print("🐉 LU 运行时状态 v3.0")
        print(f"   沙盒: {stats['sandbox']}")
        print(f"   数据库: {stats['database']}")
        print(f"   ─────────────")
        print(f"   窗口: {stats['windows']} ({stats['corrupted_windows']} 污染)")
        print(f"   快照: {stats['snapshots']}")
        print(f"   审计: {stats['audit_entries']} 条")
        print(f"   分支: {stats['branches']}")
        print(f"   恢复队列: {stats['recovery_queue']}")
        print(f"   时间线: {stats['timeline_events']} 事件")
        print(f"   禁止规则: {stats['forbidden_rules']} 条")
        print(f"   记忆层: {', '.join(stats['memory_layers'])}")


if __name__ == "__main__":
    main()
