#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 CNSH 本地主权 AgentOS v2.0
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-CNSH-RUNTIME-v2.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

定位：中文原生本地主权 AI 执行生态
核心理念：本地优先 · 多AI协同 · 记忆治理 · 可恢复 · 可审计 · 可演化

架构组件（12模块）：
  1. Runtime Core      — 主控运行时·9层记忆拓扑·目录初始化
  2. Agent Runtime     — AI执行实体·生命周期管理(start/stop/monitor)
  3. CNSH Compiler桥   — .cnsh→.py 编译集成
  4. CNSH Absorber桥   — 外部代码→CNSH吸收集成
  5. Memory Engine     — 9层记忆治理（Active→Shadow）
  6. Snapshot System   — 快照创建/恢复/列表·pre-restore备份
  7. Sandbox Workspace — AI沙盒·脚本执行·安全隔离
  8. Notion Registry   — 元数据中心·同步缓存
  9. Audit Engine      — 审计系统·三色判定联动
  10. GPG签名引擎      — 自动签名·防篡改
  11. DNA追溯引擎      — v∞干支卦DNA·文档+人物双维度
  12. Evolution Engine  — 演化治理·系统自我进化

与现有生态集成：
  - 记忆拓扑对齐 lh_lu_runtime.py（9层: Active→Shadow）
  - DNA生成复用 lh_dna_generator.py
  - CNSH编译复用 cnsh_compiler.py
  - 代码吸收复用 lh_cnsh_absorb.py
  - GPG签名复用 lh_gpg_sign.py
  - 审计联动 P05三色审计引擎
  - 根路径 ~/.longhun/cnsh_runtime/（对齐 LU runtime 的 ~/.longhun/lu_runtime/）
"""

import json
import uuid
import hashlib
import hmac
import sqlite3
import shutil
import subprocess
import time
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field, asdict
from enum import Enum
import argparse

# ═══════════════════════════════════════════════════════════
# L0 常量
# ═══════════════════════════════════════════════════════════

# 根路径：对齐 LU runtime (~/.longhun/lu_runtime/)
CNSH_ROOT = Path.home() / ".longhun" / "cnsh_runtime"
CNSH_ROOT.mkdir(parents=True, exist_ok=True)

# 项目 bin/ 路径（用于导入兄弟模块）
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 目录结构
DIRS = {
    "runtime":    CNSH_ROOT / "runtime",
    "memory":     CNSH_ROOT / "memory",
    "snapshots":  CNSH_ROOT / "snapshots",
    "sandbox":    CNSH_ROOT / "sandbox",
    "notion":     CNSH_ROOT / "notion",
    "prompts":    CNSH_ROOT / "prompts",
    "models":     CNSH_ROOT / "models",
    "logs":       CNSH_ROOT / "logs",
    "database":   CNSH_ROOT / "database",
    "scripts":    CNSH_ROOT / "scripts",
    "agents":     CNSH_ROOT / "agents",
    "cnsh_src":   CNSH_ROOT / "cnsh_src",      # CNSH源码目录
    "absorbed":   CNSH_ROOT / "absorbed",       # 吸收的外部代码
}

# 9层记忆拓扑（对齐 lh_lu_runtime.py）
MEMORY_LAYERS = [
    "Active",      # 当前运行时激活的记忆
    "Episodic",    # 事件型记忆
    "Semantic",    # 知识型记忆
    "Governance",  # 治理决策记忆
    "Runtime",     # 运行时状态记忆
    "Audit",       # 完整审计链
    "Frozen",      # 已冻结的快照
    "Recovery",    # 恢复点记忆
    "Shadow",      # 隔离沙盒记忆
]

# 沙盒子目录
SANDBOX_SUBDIRS = [
    "claude", "chatgpt", "local_llm",
    "experiments", "compression_lab", "diff_lab", "dna_lab",
]

# 固定脚本
FIXED_SCRIPTS = [
    "snapshot.sh", "restore.sh", "audit.sh",
    "notion_sync.sh", "governance_commit.sh",
    "claude_runtime.sh", "start_local_llm.sh",
    "semantic_diff.py", "memory_cleaner.py",
]

# 禁止操作（对齐 LU runtime FORBIDDEN）
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

# ═══════════════════════════════════════════════════════════
# 一、数据结构
# ═══════════════════════════════════════════════════════════

class 三色(Enum):
    绿色 = "🟢"
    黄色 = "🟡"
    红色 = "🔴"

class 执行动作(Enum):
    NONE = "无操作"
    REQUEST_UPDATE = "请求更新"
    FORCE_UPDATE = "强制执行"
    BLOCK = "阻止"

@dataclass
class 快照元数据:
    """快照元数据"""
    快照ID: str
    名称: str
    路径: str
    创建时间: str
    描述: str
    大小字节: int
    dna: str
    校验和: str = ""

@dataclass
class 记忆记录:
    """记忆记录"""
    记忆ID: str
    层: str
    内容: str
    dna: str
    创建时间: str
    标签: List[str] = field(default_factory=list)
    来源: str = "system"
    校验和: str = ""

@dataclass
class 审计记录:
    """审计记录"""
    审计ID: str
    操作: str
    目标: str
    结果: str
    详情: Dict = field(default_factory=dict)
    创建时间: str = ""
    dna: str = ""
    三色: str = "🟢"

@dataclass
class 沙盒记录:
    """沙盒执行记录"""
    记录ID: str
    代理: str
    操作: str
    结果: str
    创建时间: str
    dna: str
    输出: str = ""
    返回码: int = 0

@dataclass
class AgentInfo:
    """AI代理信息"""
    代理ID: str
    名称: str
    类型: str  # claude / chatgpt / ollama / local
    状态: str  # running / stopped / paused / error
    模型: str = ""
    端口: int = 0
    启动时间: str = ""
    最后心跳: str = ""
    dna: str = ""


# ═══════════════════════════════════════════════════════════
# 二、工具函数
# ═══════════════════════════════════════════════════════════

def _生成DNA(模块: str = "CNSH-RUNTIME", 动作: str = "OP") -> str:
    """生成标准v∞ DNA（尝试调用 lh_dna_generator，降级自生成）"""
    try:
        from bin.lh_dna_generator import DNA生成器
        gen = DNA生成器()
        结果 = gen.生成文档DNA(模块=模块, 动作=动作)
        if 结果 and isinstance(结果, dict) and 结果.get("dna"):
            return 结果["dna"]
    except Exception:
        pass
    # 降级：自生成
    now = datetime.now()
    干支 = f"{now.year}-{now.month:02d}-{now.day:02d}"
    return f"#龍芯⚡️{干支}-{模块}-{动作}-{uuid.uuid4().hex[:8]}"


def _计算校验和(内容: str) -> str:
    """SHA256 校验和"""
    return hashlib.sha256(内容.encode('utf-8')).hexdigest()[:16]


def _签名(内容: str, 密钥: str = "cnsh-sovereign-9622") -> str:
    """HMAC-SHA256 签名"""
    return hmac.new(密钥.encode(), 内容.encode(), hashlib.sha256).hexdigest()[:16]


def _now() -> str:
    return datetime.now().isoformat()


def _防篡改指纹(数据: Dict) -> str:
    """生成防篡改指纹"""
    规范 = json.dumps(数据, sort_keys=True, ensure_ascii=False)
    return _计算校验和(规范)

# ═══════════════════════════════════════════════════════════
# 三、CNSH Runtime Core
# ═══════════════════════════════════════════════════════════

class 运行时核心:
    """CNSH 主控运行时"""

    def __init__(self):
        self.root = CNSH_ROOT
        self._初始化目录()
        self._初始化数据库()
        self._初始化脚本()
        self._初始化沙盒()
        self._初始化记忆清单()
        self._加载状态()

    def _初始化目录(self):
        """初始化全部目录结构"""
        for key, path in DIRS.items():
            path.mkdir(parents=True, exist_ok=True)
        for sub in SANDBOX_SUBDIRS:
            (DIRS["sandbox"] / sub).mkdir(parents=True, exist_ok=True)
        for layer in MEMORY_LAYERS:
            (DIRS["memory"] / layer).mkdir(parents=True, exist_ok=True)
        for model in ["ollama", "deepseek", "qwen", "mistral"]:
            (DIRS["models"] / model).mkdir(parents=True, exist_ok=True)

    def _初始化数据库(self):
        """初始化 SQLite 数据库（6表）"""
        db = DIRS["database"] / "cnsh_runtime.db"
        with sqlite3.connect(str(db)) as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS snapshots (
                    id TEXT PRIMARY KEY, name TEXT, path TEXT,
                    created_at TEXT, description TEXT, size INTEGER, checksum TEXT,
                    dna TEXT
                );
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY, layer TEXT, content TEXT,
                    dna TEXT, created_at TEXT, tags TEXT, source TEXT,
                    checksum TEXT
                );
                CREATE TABLE IF NOT EXISTS audits (
                    id TEXT PRIMARY KEY, operation TEXT, target TEXT,
                    result TEXT, details TEXT, created_at TEXT,
                    dna TEXT, tricolor TEXT DEFAULT '🟢'
                );
                CREATE TABLE IF NOT EXISTS sandbox_records (
                    id TEXT PRIMARY KEY, agent TEXT, operation TEXT,
                    result TEXT, created_at TEXT, dna TEXT,
                    output TEXT, returncode INTEGER DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS notion_sync (
                    id TEXT PRIMARY KEY, sync_type TEXT,
                    items_synced INTEGER, last_sync TEXT, status TEXT
                );
                CREATE TABLE IF NOT EXISTS agents (
                    id TEXT PRIMARY KEY, name TEXT, type TEXT,
                    status TEXT DEFAULT 'stopped', model TEXT,
                    port INTEGER DEFAULT 0, started_at TEXT,
                    last_heartbeat TEXT, dna TEXT
                );
            """)
        self.db_path = db

    def _初始化脚本(self):
        """生成固定脚本"""
        sdir = DIRS["scripts"]

        脚本内容 = {
            "snapshot.sh": f"""#!/bin/bash
# CNSH 快照脚本 · DNA: {_生成DNA('SNAPSHOT', 'SHELL')}
ROOT={CNSH_ROOT}
NAME="snapshot_$(date +%Y%m%d_%H%M%S)"
D="$ROOT/snapshots/$NAME"
mkdir -p "$D"
cp -r "$ROOT/runtime" "$D/" 2>/dev/null
cp -r "$ROOT/memory/Active" "$D/" 2>/dev/null
cp -r "$ROOT/memory/Governance" "$D/" 2>/dev/null
echo "✅ 快照: $NAME"
""",
            "restore.sh": f"""#!/bin/bash
# CNSH 恢复脚本 · DNA: {_生成DNA('RESTORE', 'SHELL')}
ROOT={CNSH_ROOT}
[ -z "$1" ] && {{ echo "用法: $0 <快照名>"; exit 1; }}
D="$ROOT/snapshots/$1"
[ ! -d "$D" ] && {{ echo "❌ 快照不存在: $1"; exit 1; }}
echo "⚠️ 将恢复快照: $1"
read -p "确认? (y/n): " c
[ "$c" != "y" ] && {{ echo "取消"; exit 0; }}
cp -r "$D/runtime" "$ROOT/" 2>/dev/null
cp -r "$D/Active" "$ROOT/memory/" 2>/dev/null
cp -r "$D/Governance" "$ROOT/memory/" 2>/dev/null
echo "✅ 恢复完成: $1"
""",
            "audit.sh": f"""#!/bin/bash
# CNSH 审计脚本 · DNA: {_生成DNA('AUDIT', 'SHELL')}
ROOT={CNSH_ROOT}
LOG="$ROOT/logs/audit_$(date +%Y%m%d).log"
echo "🔍 CNSH审计 $(date)" > "$LOG"
for layer in {' '.join(MEMORY_LAYERS)}; do
    c=$(find "$ROOT/memory/$layer" -type f 2>/dev/null | wc -l | tr -d ' ')
    echo "  $layer: $c 条" >> "$LOG"
done
echo "✅ 审计完成: $LOG"
""",
        }

        for 脚本名, 内容 in 脚本内容.items():
            fp = sdir / 脚本名
            if not fp.exists():
                fp.write_text(内容, encoding='utf-8')
                fp.chmod(0o755)

    def _初始化沙盒(self):
        """初始化沙盒配置"""
        cfg = DIRS["sandbox"] / "sandbox_config.json"
        if not cfg.exists():
            config = {
                "allowed_paths": [
                    str(DIRS["sandbox"]), str(DIRS["prompts"]),
                    str(DIRS["runtime"]), str(DIRS["memory"] / "Active"),
                ],
                "forbidden_paths": [
                    str(Path.home() / ".ssh"),
                    str(Path.home() / "Library/Keychains"),
                    "/System", "/Applications",
                ],
                "permissions": {
                    "file_read": True, "file_write": "limited",
                    "network_access": "restricted", "shell_execute": "sandbox_only",
                },
                "audit": {"enabled": True},
                "snapshot_before_write": True,
                "dna": _生成DNA('SANDBOX', 'CONFIG'),
            }
            with open(cfg, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)

    def _初始化记忆清单(self):
        """初始化9层记忆清单"""
        mf = DIRS["memory"] / "manifest.json"
        if not mf.exists():
            data = {
                "version": "2.0",
                "layers": MEMORY_LAYERS,
                "descriptions": {
                    "Active":      "当前运行时激活的记忆",
                    "Episodic":    "事件型记忆",
                    "Semantic":    "知识型记忆",
                    "Governance":  "治理决策记忆",
                    "Runtime":     "运行时状态记忆",
                    "Audit":       "完整审计链",
                    "Frozen":      "已冻结的快照",
                    "Recovery":    "恢复点记忆",
                    "Shadow":      "隔离沙盒记忆",
                },
                "created_at": _now(),
                "dna": _生成DNA('MEMORY', 'MANIFEST'),
            }
            with open(mf, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    def _加载状态(self):
        sf = CNSH_ROOT / "status.json"
        if sf.exists():
            with open(sf, 'r', encoding='utf-8') as f:
                self.status = json.load(f)
        else:
            self.status = {"status": "initialized", "last_snapshot": None}

    def 保存状态(self):
        with open(CNSH_ROOT / "status.json", 'w', encoding='utf-8') as f:
            json.dump(self.status, f, ensure_ascii=False, indent=2)

    def 获取状态(self) -> Dict:
        return {
            "root": str(CNSH_ROOT),
            "status": self.status.get("status", "running"),
            "memory_layers": MEMORY_LAYERS,
            "sandbox_subdirs": SANDBOX_SUBDIRS,
            "last_snapshot": self.status.get("last_snapshot"),
            "agents_registered": self._数代理(),
            "dna": _生成DNA('CNSH-RUNTIME', 'STATUS'),
        }

    def _数代理(self) -> int:
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                return conn.execute("SELECT COUNT(*) FROM agents").fetchone()[0]
        except Exception:
            return 0


# ═══════════════════════════════════════════════════════════
# 四、Agent Runtime（AI代理生命周期）
# ═══════════════════════════════════════════════════════════

class 代理运行时:
    """AI代理生命周期管理"""

    def __init__(self, db_path: Path):
        self.db_path = db_path

    def 注册(self, 名称: str, 类型: str, 模型: str = "", 端口: int = 0) -> AgentInfo:
        """注册新代理"""
        代理ID = f"AGENT-{uuid.uuid4().hex[:8].upper()}"
        dna = _生成DNA('AGENT', 'REGISTER')
        info = AgentInfo(
            代理ID=代理ID, 名称=名称, 类型=类型,
            状态="stopped", 模型=模型, 端口=端口,
            启动时间="", 最后心跳="", dna=dna,
        )
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute(
                """INSERT OR REPLACE INTO agents
                   (id, name, type, status, model, port, started_at, last_heartbeat, dna)
                   VALUES (?,?,?,?,?,?,?,?,?)""",
                (代理ID, 名称, 类型, "stopped", 模型, 端口, "", "", dna),
            )
        return info

    def 启动(self, 代理ID: str) -> Dict:
        """启动代理"""
        with sqlite3.connect(str(self.db_path)) as conn:
            row = conn.execute("SELECT * FROM agents WHERE id=?", (代理ID,)).fetchone()
            if not row:
                return {"error": f"代理不存在: {代理ID}"}
            now = _now()
            conn.execute(
                "UPDATE agents SET status='running', started_at=?, last_heartbeat=? WHERE id=?",
                (now, now, 代理ID),
            )
        return {"agent_id": 代理ID, "status": "running", "started_at": now}

    def 停止(self, 代理ID: str) -> Dict:
        """停止代理"""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("UPDATE agents SET status='stopped' WHERE id=?", (代理ID,))
        return {"agent_id": 代理ID, "status": "stopped"}

    def 心跳(self, 代理ID: str) -> Dict:
        """更新心跳"""
        now = _now()
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("UPDATE agents SET last_heartbeat=? WHERE id=?", (now, 代理ID))
        return {"agent_id": 代理ID, "heartbeat": now}

    def 列表(self) -> List[AgentInfo]:
        """列出所有代理"""
        result = []
        with sqlite3.connect(str(self.db_path)) as conn:
            for row in conn.execute("SELECT * FROM agents ORDER BY started_at DESC").fetchall():
                result.append(AgentInfo(
                    代理ID=row[0], 名称=row[1], 类型=row[2],
                    状态=row[3], 模型=row[4], 端口=row[5],
                    启动时间=row[6], 最后心跳=row[7], dna=row[8],
                ))
        return result

    def 获取(self, 代理ID: str) -> Optional[AgentInfo]:
        """获取单个代理"""
        with sqlite3.connect(str(self.db_path)) as conn:
            row = conn.execute("SELECT * FROM agents WHERE id=?", (代理ID,)).fetchone()
            if row:
                return AgentInfo(
                    代理ID=row[0], 名称=row[1], 类型=row[2],
                    状态=row[3], 模型=row[4], 端口=row[5],
                    启动时间=row[6], 最后心跳=row[7], dna=row[8],
                )
        return None


# ═══════════════════════════════════════════════════════════
# 五、CNSH 编译器/吸收器桥接
# ═══════════════════════════════════════════════════════════

class CNSH编译桥:
    """CNSH 编译器桥接 · .cnsh → .py"""

    @staticmethod
    def 编译(输入文件: str, 输出文件: Optional[str] = None) -> Dict:
        """编译 .cnsh 文件为 .py"""
        try:
            from bin.cnsh_compiler import CNSHCompiler
            编译器 = CNSHCompiler()
            with open(输入文件, 'r', encoding='utf-8') as f:
                源码 = f.read()
            结果 = 编译器.编译(源码)
            if not 输出文件:
                输出文件 = 输入文件.replace('.cnsh', '.py')
            with open(输出文件, 'w', encoding='utf-8') as f:
                f.write(结果)
            return {
                "success": True,
                "input": 输入文件,
                "output": 输出文件,
                "dna": _生成DNA('CNSH-COMPILE', 'BRIDGE'),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def 吸收(文件路径: str, 名称: Optional[str] = None) -> Dict:
        """吸收外部代码 → CNSH"""
        try:
            from bin.lh_cnsh_absorb import CNSHAbsorber
            吸收器 = CNSHAbsorber()
            if not 名称:
                名称 = Path(文件路径).stem
            结果 = 吸收器.absorb(文件路径, uid="UID9622", name=名称)
            return {
                "success": True,
                "name": 名称,
                "source": 文件路径,
                "result": str(结果)[:200] if 结果 else "吸收完成",
                "dna": _生成DNA('CNSH-ABSORB', 'BRIDGE'),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


# ═══════════════════════════════════════════════════════════
# 六、Memory Engine（9层记忆治理）
# ═══════════════════════════════════════════════════════════

class 记忆引擎:
    """9层记忆拓扑治理"""

    def __init__(self):
        self.root = DIRS["memory"]
        self.db_path = DIRS["database"] / "cnsh_runtime.db"

    def 写入(self, 层: str, 内容: str, 标签: List[str] = None, 来源: str = "system") -> Dict:
        """写入记忆到指定层"""
        if 层 not in MEMORY_LAYERS:
            return {"error": f"无效记忆层: {层}，有效层: {MEMORY_LAYERS}"}
        if any(f in 内容 for f in FORBIDDEN):
            return {"error": "内容包含禁止操作", "forbidden": True}

        记忆ID = f"MEM-{uuid.uuid4().hex[:8].upper()}"
        dna = _生成DNA(层.upper(), 'WRITE')
        now = _now()
        校验和 = _计算校验和(内容)
        标签s = json.dumps(标签 or [], ensure_ascii=False)

        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute(
                """INSERT INTO memories (id, layer, content, dna, created_at, tags, source, checksum)
                   VALUES (?,?,?,?,?,?,?,?)""",
                (记忆ID, 层, 内容, dna, now, 标签s, 来源, 校验和),
            )

        # 文件落盘
        layer_dir = self.root / 层
        文件 = layer_dir / f"{记忆ID}.json"
        with open(文件, 'w', encoding='utf-8') as f:
            json.dump({
                "id": 记忆ID, "layer": 层, "content": 内容,
                "dna": dna, "created_at": now,
                "tags": 标签 or [], "source": 来源, "checksum": 校验和,
            }, f, ensure_ascii=False, indent=2)

        # GPG签名（尝试）
        self._尝试GPG签名(文件)

        return {"id": 记忆ID, "layer": 层, "dna": dna, "checksum": 校验和}

    def 读取(self, 记忆ID: str) -> Optional[Dict]:
        """读取单条记忆"""
        with sqlite3.connect(str(self.db_path)) as conn:
            row = conn.execute("SELECT * FROM memories WHERE id=?", (记忆ID,)).fetchone()
        if row:
            return {
                "id": row[0], "layer": row[1], "content": row[2],
                "dna": row[3], "created_at": row[4],
                "tags": json.loads(row[5]) if row[5] else [],
                "source": row[6], "checksum": row[7],
            }
        return None

    def 查询(self, 层: str = None, 标签: str = None, limit: int = 20) -> List[Dict]:
        """查询记忆"""
        sql = "SELECT * FROM memories WHERE 1=1"
        params = []
        if 层:
            sql += " AND layer = ?"
            params.append(层)
        if 标签:
            sql += " AND tags LIKE ?"
            params.append(f'%"{标签}"%')
        sql += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        with sqlite3.connect(str(self.db_path)) as conn:
            rows = conn.execute(sql, params).fetchall()
        return [{
            "id": r[0], "layer": r[1],
            "content": r[2][:200] + "..." if len(r[2]) > 200 else r[2],
            "dna": r[3], "created_at": r[4],
            "tags": json.loads(r[5]) if r[5] else [],
            "source": r[6], "checksum": r[7],
        } for r in rows]

    def 清理(self, days: int = 30, 层s: List[str] = None) -> Dict:
        """清理旧记忆（仅 Episodic/Shadow 层）"""
        if 层s is None:
            层s = ["Episodic", "Shadow"]
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        deleted = 0
        with sqlite3.connect(str(self.db_path)) as conn:
            for 层 in 层s:
                cur = conn.execute(
                    "DELETE FROM memories WHERE layer=? AND created_at<?", (层, cutoff)
                )
                deleted += cur.rowcount
        return {"deleted": deleted, "days": days, "layers": 层s}

    def 统计(self) -> Dict:
        """各层记忆统计"""
        stats = {}
        with sqlite3.connect(str(self.db_path)) as conn:
            for 层 in MEMORY_LAYERS:
                cnt = conn.execute("SELECT COUNT(*) FROM memories WHERE layer=?", (层,)).fetchone()[0]
                stats[层] = cnt
        stats["total"] = sum(stats.values())
        return stats

    def _尝试GPG签名(self, 文件: Path):
        """尝试 GPG 签名"""
        try:
            subprocess.run(
                ["python3", str(PROJECT_ROOT / "bin" / "lh_gpg_sign.py"), "sign", "--force", str(文件)],
                capture_output=True, timeout=10, cwd=str(PROJECT_ROOT),
            )
        except Exception:
            pass  # 签名失败不影响主流程


# ═══════════════════════════════════════════════════════════
# 七、Snapshot System（快照系统）
# ═══════════════════════════════════════════════════════════

class 快照系统:
    """可恢复运行时快照"""

    def __init__(self):
        self.root = DIRS["snapshots"]
        self.db_path = DIRS["database"] / "cnsh_runtime.db"

    def 创建(self, 名称: str = None, 描述: str = "") -> Dict:
        """创建快照"""
        if not 名称:
            名称 = f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        snap_dir = self.root / 名称
        if snap_dir.exists():
            return {"error": f"快照已存在: {名称}"}
        snap_dir.mkdir(parents=True)

        # 复制 runtime + active + governance
        复制映射 = {
            "runtime": DIRS["runtime"],
            "Active": DIRS["memory"] / "Active",
            "Governance": DIRS["memory"] / "Governance",
        }
        for dst_name, src in 复制映射.items():
            if src.exists():
                shutil.copytree(src, snap_dir / dst_name, dirs_exist_ok=True)

        # 元数据
        size = self._大小(snap_dir)
        dna = _生成DNA('SNAPSHOT', 'CREATE')
        meta = {
            "name": 名称, "description": 描述,
            "created_at": _now(), "size": size, "dna": dna,
        }
        with open(snap_dir / "metadata.json", 'w', encoding='utf-8') as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)

        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute(
                "INSERT INTO snapshots (id, name, path, created_at, description, size, dna) VALUES (?,?,?,?,?,?,?)",
                (f"SNAP-{uuid.uuid4().hex[:8].upper()}", 名称, str(snap_dir), _now(), 描述, size, dna),
            )
        return {"name": 名称, "path": str(snap_dir), "size": size, "dna": dna}

    def 恢复(self, 名称: str) -> Dict:
        """恢复快照"""
        snap_dir = self.root / 名称
        if not snap_dir.exists():
            return {"error": f"快照不存在: {名称}"}

        # pre-restore 备份
        backup = self.root / f"pre_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup.mkdir()
        for name in ["runtime", "Active", "Governance"]:
            src = DIRS["runtime"] if name == "runtime" else DIRS["memory"] / name
            if src.exists():
                shutil.copytree(src, backup / name, dirs_exist_ok=True)

        # 恢复
        for name, dst in [("runtime", DIRS["runtime"]), ("Active", DIRS["memory"] / "Active"), ("Governance", DIRS["memory"] / "Governance")]:
            src = snap_dir / name
            if src.exists():
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)

        return {"restored": 名称, "backup": str(backup), "timestamp": _now()}

    def 列表(self) -> List[Dict]:
        """列出所有快照"""
        snaps = []
        for item in sorted(self.root.iterdir(), key=lambda x: x.name, reverse=True):
            if item.is_dir():
                meta_file = item / "metadata.json"
                if meta_file.exists():
                    with open(meta_file, 'r', encoding='utf-8') as f:
                        meta = json.load(f)
                    snaps.append({
                        "name": meta.get("name", item.name),
                        "created_at": meta.get("created_at"),
                        "size": meta.get("size"),
                        "description": meta.get("description", ""),
                        "dna": meta.get("dna"),
                    })
        return snaps

    @staticmethod
    def _大小(path: Path) -> int:
        total = 0
        for f in path.rglob("*"):
            if f.is_file():
                total += f.stat().st_size
        return total


# ═══════════════════════════════════════════════════════════
# 八、Sandbox Workspace（AI沙盒）
# ═══════════════════════════════════════════════════════════

class 沙盒空间:
    """AI 沙盒 · 隔离执行环境"""

    def __init__(self):
        self.root = DIRS["sandbox"]
        self.db_path = DIRS["database"] / "cnsh_runtime.db"
        self._加载配置()

    def _加载配置(self):
        cfg = self.root / "sandbox_config.json"
        if cfg.exists():
            with open(cfg, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {"allowed_paths": [str(self.root)], "forbidden_paths": []}

    def 执行(self, 代理: str, 脚本: str, args: List[str] = None) -> Dict:
        """沙盒执行脚本"""
        agent_dir = self.root / 代理
        agent_dir.mkdir(parents=True, exist_ok=True)

        if ".." in 脚本 or 脚本.startswith("/"):
            return {"error": "沙盒安全: 禁止路径穿越"}

        script_path = agent_dir / 脚本
        if not script_path.exists():
            return {"error": f"脚本不存在: {脚本}"}

        try:
            result = subprocess.run(
                [str(script_path)] + (args or []),
                capture_output=True, text=True, timeout=30, cwd=str(agent_dir),
            )
            记录ID = f"SBX-{uuid.uuid4().hex[:8].upper()}"
            dna = _生成DNA('SANDBOX', 'EXEC')
            with sqlite3.connect(str(self.db_path)) as conn:
                conn.execute(
                    "INSERT INTO sandbox_records (id, agent, operation, result, created_at, dna, output, returncode) VALUES (?,?,?,?,?,?,?,?)",
                    (记录ID, 代理, 脚本, "success" if result.returncode == 0 else "failed", _now(), dna, result.stdout[:500], result.returncode),
                )
            return {
                "agent": 代理, "script": 脚本,
                "stdout": result.stdout, "stderr": result.stderr,
                "returncode": result.returncode, "executed_at": _now(),
                "dna": dna,
            }
        except subprocess.TimeoutExpired:
            return {"error": "执行超时(30s)", "agent": 代理, "script": 脚本}
        except Exception as e:
            return {"error": str(e), "agent": 代理, "script": 脚本}

    def 写脚本(self, 代理: str, 名称: str, 内容: str) -> Dict:
        """写入沙盒脚本"""
        agent_dir = self.root / 代理
        agent_dir.mkdir(parents=True, exist_ok=True)
        fp = agent_dir / 名称
        fp.write_text(内容, encoding='utf-8')
        fp.chmod(0o755)
        return {"agent": 代理, "script": 名称, "path": str(fp), "written_at": _now()}


# ═══════════════════════════════════════════════════════════
# 九、Notion Registry（元数据中心）
# ═══════════════════════════════════════════════════════════

class Notion注册中心:
    """Notion 元数据同步"""

    def __init__(self):
        self.root = DIRS["notion"]
        self.db_path = DIRS["database"] / "cnsh_runtime.db"

    def 同步(self, 类型: str = "metadata", 条目: List[Dict] = None) -> Dict:
        """同步到Notion缓存"""
        条目 = 条目 or []
        cache_file = self.root / "sync_cache.json"
        existing = []
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                existing = json.load(f)

        merged = existing + 条目
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(merged, f, ensure_ascii=False, indent=2)

        sync_id = f"SYNC-{uuid.uuid4().hex[:8].upper()}"
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute(
                "INSERT INTO notion_sync (id, sync_type, items_synced, last_sync, status) VALUES (?,?,?,?,?)",
                (sync_id, 类型, len(条目), _now(), "success"),
            )
        return {"sync_type": 类型, "items_synced": len(条目), "timestamp": _now()}

    def 获取注册表(self) -> Dict:
        rf = self.root / "registry.json"
        if rf.exists():
            with open(rf, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"items": [], "last_sync": None}


# ═══════════════════════════════════════════════════════════
# 十、Audit Engine（审计系统）
# ═══════════════════════════════════════════════════════════

class 审计引擎:
    """审计系统 · 三色判定联动"""

    def __init__(self):
        self.db_path = DIRS["database"] / "cnsh_runtime.db"

    def 记录(self, 操作: str, 目标: str, 结果: str, 详情: Dict = None, 三色标记: str = "🟢") -> Dict:
        """记录审计日志"""
        审计ID = f"AUDIT-{uuid.uuid4().hex[:8].upper()}"
        dna = _生成DNA('AUDIT', 'LOG')
        now = _now()
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute(
                "INSERT INTO audits (id, operation, target, result, details, created_at, dna, tricolor) VALUES (?,?,?,?,?,?,?,?)",
                (审计ID, 操作, 目标, 结果, json.dumps(详情 or {}, ensure_ascii=False), now, dna, 三色标记),
            )
        return {"id": 审计ID, "dna": dna, "tricolor": 三色标记}

    def 查询(self, limit: int = 50) -> List[Dict]:
        """查询审计日志"""
        with sqlite3.connect(str(self.db_path)) as conn:
            rows = conn.execute(
                "SELECT id, operation, target, result, details, created_at, dna, tricolor FROM audits ORDER BY created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [{
            "id": r[0], "operation": r[1], "target": r[2],
            "result": r[3], "details": json.loads(r[4]) if r[4] else {},
            "created_at": r[5], "dna": r[6], "tricolor": r[7],
        } for r in rows]

    def 三色判定(self, 内容: str, 类型: str = "系统行为") -> Dict:
        """调用 P05 三色审计引擎进行判定"""
        try:
            from bin.lh_three_color_audit import quick_audit
            颜色, 理由 = quick_audit(内容)
            return {"color": 颜色, "reason": 理由}
        except Exception:
            # 降级：基础关键词检测
            red_words = ["攻击", "入侵", "漏洞", "越权", "P0", "铁律", "窃取"]
            yellow_words = ["未加密", "异常", "警告", "可疑"]
            for w in red_words:
                if w in 内容:
                    return {"color": "🔴", "reason": f"命中红线词: {w}"}
            for w in yellow_words:
                if w in 内容:
                    return {"color": "🟡", "reason": f"命中黄线词: {w}"}
            return {"color": "🟢", "reason": "未触发规则"}


# ═══════════════════════════════════════════════════════════
# 十一、Evolution Engine（演化治理）
# ═══════════════════════════════════════════════════════════

class 演化引擎:
    """演化治理 · 系统自我进化"""

    def __init__(self):
        self.evo_dir = DIRS["runtime"] / "evolution"
        self.evo_dir.mkdir(parents=True, exist_ok=True)

    def 分析(self) -> Dict:
        """分析系统状态"""
        stats = {}
        for layer in MEMORY_LAYERS:
            ld = DIRS["memory"] / layer
            stats[layer] = len(list(ld.glob("*.json"))) if ld.exists() else 0
        snap_cnt = len(list(DIRS["snapshots"].iterdir())) if DIRS["snapshots"].exists() else 0
        total_mem = sum(stats.values())

        建议 = []
        if stats.get("Episodic", 0) > 100:
            建议.append("Episodic 层记忆 > 100，建议清理")
        if snap_cnt < 1:
            建议.append("无快照，建议立即创建")
        if stats.get("Shadow", 0) > 50:
            建议.append("Shadow 层堆积 > 50，建议审查并清理")

        return {
            "memory_stats": stats,
            "total_memories": total_mem,
            "snapshot_count": snap_cnt,
            "suggestions": 建议 or ["系统状态良好"],
            "health_score": min(100, max(0, total_mem - stats.get("Shadow", 0) * 2 + snap_cnt * 10)),
            "dna": _生成DNA('EVOLUTION', 'ANALYZE'),
        }

    def 执行演化(self, 建议: str) -> Dict:
        evo_id = f"EVO-{uuid.uuid4().hex[:8].upper()}"
        log = self.evo_dir / "evolution_log.jsonl"
        entry = {
            "id": evo_id, "suggestion": 建议, "executed_at": _now(),
            "status": "pending", "dna": _生成DNA('EVOLUTION', 'EXEC'),
        }
        with open(log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        return {"id": evo_id, "suggestion": 建议, "status": "pending"}


# ═══════════════════════════════════════════════════════════
# 十二、主引擎：CNSH 本地主权 AgentOS
# ═══════════════════════════════════════════════════════════

class CNSH本地主权AgentOS:
    """龍魂 CNSH 本地主权 AI 执行生态 · 统一入口"""

    def __init__(self):
        self.运行时 = 运行时核心()
        self.代理 = 代理运行时(self.运行时.db_path)
        self.记忆 = 记忆引擎()
        self.快照 = 快照系统()
        self.沙盒 = 沙盒空间()
        self.notion = Notion注册中心()
        self.审计 = 审计引擎()
        self.演化 = 演化引擎()
        self.编译桥 = CNSH编译桥()

    def 系统状态(self) -> Dict:
        return {
            "runtime": self.运行时.获取状态(),
            "memory_layers": MEMORY_LAYERS,
            "memory_stats": self.记忆.统计(),
            "snapshots": len(self.快照.列表()),
            "agents": len(self.代理.列表()),
            "sandbox_dirs": SANDBOX_SUBDIRS,
            "dna": _生成DNA('CNSH-AGENTOS', 'STATUS'),
        }

    def 每日复盘(self) -> Dict:
        """每日复盘：快照 + 审计 + 演化分析"""
        snap = self.快照.创建(描述="daily_review")
        audit = self.审计.记录("daily_review", "system", "completed")
        evo = self.演化.分析()
        记忆统计 = self.记忆.统计()
        return {
            "snapshot": snap,
            "audit": audit,
            "evolution": evo,
            "memory": 记忆统计,
            "timestamp": _now(),
            "dna": _生成DNA('DAILY', 'REVIEW'),
        }


# ═══════════════════════════════════════════════════════════
# 十三、命令行入口
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="🐉 CNSH 本地主权 AgentOS v2.0 · 9层记忆·CNSH编译·GPG·审计",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
子命令:
  status              查看系统状态
  snapshot create     创建快照
  snapshot list       列出快照
  snapshot restore    恢复快照
  memory write        写入记忆
  memory query        查询记忆
  memory stats        记忆统计
  memory clean        清理旧记忆
  sandbox exec        沙盒执行脚本
  sandbox write       写入沙盒脚本
  agent list          列出代理
  agent register      注册代理
  agent start/stop    启动/停止代理
  audit               查询审计日志
  compile             编译 .cnsh → .py
  absorb              吸收外部代码 → CNSH
  daily               每日复盘
  evolve              演化分析

示例:
  lh_cnsh_runtime status
  lh_cnsh_runtime snapshot create --name my_snap --desc "状态良好"
  lh_cnsh_runtime memory write --layer Active --content "完成安全检查"
  lh_cnsh_runtime agent register --name claude --type claude
  lh_cnsh_runtime compile --input test.cnsh
  lh_cnsh_runtime absorb --file external_code.py
  lh_cnsh_runtime daily
        """,
    )

    sub = parser.add_subparsers(dest="command", help="子命令")

    # ── status ──
    p_status = sub.add_parser("status", help="系统状态")
    p_status.add_argument("--json", "-j", action="store_true", help="JSON 输出")

    # ── snapshot ──
    p_snap = sub.add_parser("snapshot", help="快照管理")
    p_snap_sub = p_snap.add_subparsers(dest="snap_cmd")
    p_snap_create = p_snap_sub.add_parser("create", help="创建快照")
    p_snap_create.add_argument("--name", "-n", type=str, help="快照名称")
    p_snap_create.add_argument("--desc", "-d", type=str, default="", help="描述")
    p_snap_create.add_argument("--json", "-j", action="store_true")
    p_snap_list = p_snap_sub.add_parser("list", help="列出快照")
    p_snap_list.add_argument("--json", "-j", action="store_true")
    p_snap_restore = p_snap_sub.add_parser("restore", help="恢复快照")
    p_snap_restore.add_argument("--name", "-n", type=str, required=True, help="快照名称")
    p_snap_restore.add_argument("--json", "-j", action="store_true")

    # ── memory ──
    p_mem = sub.add_parser("memory", help="记忆管理")
    p_mem_sub = p_mem.add_subparsers(dest="mem_cmd")
    p_mem_write = p_mem_sub.add_parser("write", help="写入记忆")
    p_mem_write.add_argument("--layer", "-l", type=str, default="Active", choices=MEMORY_LAYERS, help="记忆层")
    p_mem_write.add_argument("--content", "-c", type=str, required=True, help="内容")
    p_mem_write.add_argument("--tag", type=str, nargs="*", help="标签")
    p_mem_write.add_argument("--source", type=str, default="cli", help="来源")
    p_mem_write.add_argument("--json", "-j", action="store_true")
    p_mem_query = p_mem_sub.add_parser("query", help="查询记忆")
    p_mem_query.add_argument("--layer", "-l", type=str, choices=MEMORY_LAYERS, help="记忆层")
    p_mem_query.add_argument("--tag", type=str, help="标签筛选")
    p_mem_query.add_argument("--limit", type=int, default=20)
    p_mem_query.add_argument("--json", "-j", action="store_true")
    p_mem_stats = p_mem_sub.add_parser("stats", help="记忆统计")
    p_mem_stats.add_argument("--json", "-j", action="store_true")
    p_mem_clean = p_mem_sub.add_parser("clean", help="清理旧记忆")
    p_mem_clean.add_argument("--days", type=int, default=30, help="保留天数")
    p_mem_clean.add_argument("--json", "-j", action="store_true")

    # ── sandbox ──
    p_sbx = sub.add_parser("sandbox", help="沙盒管理")
    p_sbx_sub = p_sbx.add_subparsers(dest="sbx_cmd")
    p_sbx_exec = p_sbx_sub.add_parser("exec", help="沙盒执行")
    p_sbx_exec.add_argument("--agent", "-a", type=str, required=True)
    p_sbx_exec.add_argument("--script", "-s", type=str, required=True)
    p_sbx_exec.add_argument("--args", nargs="*", help="脚本参数")
    p_sbx_exec.add_argument("--json", "-j", action="store_true")
    p_sbx_write = p_sbx_sub.add_parser("write", help="写入沙盒脚本")
    p_sbx_write.add_argument("--agent", "-a", type=str, required=True)
    p_sbx_write.add_argument("--name", "-n", type=str, required=True)
    p_sbx_write.add_argument("--content", "-c", type=str, required=True)
    p_sbx_write.add_argument("--json", "-j", action="store_true")

    # ── agent ──
    p_agt = sub.add_parser("agent", help="代理管理")
    p_agt_sub = p_agt.add_subparsers(dest="agt_cmd")
    p_agt_list = p_agt_sub.add_parser("list", help="列出代理")
    p_agt_list.add_argument("--json", "-j", action="store_true")
    p_agt_reg = p_agt_sub.add_parser("register", help="注册代理")
    p_agt_reg.add_argument("--name", "-n", type=str, required=True)
    p_agt_reg.add_argument("--type", "-t", type=str, default="ollama")
    p_agt_reg.add_argument("--model", "-m", type=str, default="")
    p_agt_reg.add_argument("--port", type=int, default=0)
    p_agt_reg.add_argument("--json", "-j", action="store_true")
    p_agt_start = p_agt_sub.add_parser("start", help="启动代理")
    p_agt_start.add_argument("--id", type=str, required=True)
    p_agt_start.add_argument("--json", "-j", action="store_true")
    p_agt_stop = p_agt_sub.add_parser("stop", help="停止代理")
    p_agt_stop.add_argument("--id", type=str, required=True)
    p_agt_stop.add_argument("--json", "-j", action="store_true")

    # ── audit ──
    p_aud = sub.add_parser("audit", help="审计日志")
    p_aud.add_argument("--limit", type=int, default=20)
    p_aud.add_argument("--json", "-j", action="store_true")

    # ── compile ──
    p_cpl = sub.add_parser("compile", help="编译 CNSH → Python")
    p_cpl.add_argument("--input", "-i", type=str, required=True, help=".cnsh 输入文件")
    p_cpl.add_argument("--output", "-o", type=str, help=".py 输出文件（可选）")
    p_cpl.add_argument("--json", "-j", action="store_true")

    # ── absorb ──
    p_abs = sub.add_parser("absorb", help="吸收外部代码 → CNSH")
    p_abs.add_argument("--file", "-f", type=str, required=True, help="外部代码文件")
    p_abs.add_argument("--name", "-n", type=str, help="服务名（可选）")
    p_abs.add_argument("--json", "-j", action="store_true")

    # ── daily ──
    p_daily = sub.add_parser("daily", help="每日复盘")
    p_daily.add_argument("--json", "-j", action="store_true")

    # ── evolve ──
    p_evo = sub.add_parser("evolve", help="演化分析")
    p_evo.add_argument("--json", "-j", action="store_true")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    os_agent = CNSH本地主权AgentOS()

    # ── status ──
    if args.command == "status":
        result = os_agent.系统状态()
        if getattr(args, 'json', False):
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("\n🐉 CNSH 本地主权 AgentOS v2.0")
            print("=" * 56)
            print(f"  根路径:   {result['runtime']['root']}")
            print(f"  状态:     {result['runtime']['status']}")
            print(f"  记忆层:   {len(MEMORY_LAYERS)} 层")
            for k, v in result['memory_stats'].items():
                if k != 'total':
                    print(f"    {k}: {v}")
            print(f"  记忆总计: {result['memory_stats']['total']}")
            print(f"  快照:     {result['snapshots']}")
            print(f"  代理:     {result['agents']}")
            print(f"  DNA:      {result['dna']}")
            print("=" * 56)

    # ── snapshot ──
    elif args.command == "snapshot":
        if args.snap_cmd == "create":
            result = os_agent.快照.创建(
                名称=getattr(args, 'name', None),
                描述=getattr(args, 'desc', ""),
            )
        elif args.snap_cmd == "list":
            result = os_agent.快照.列表()
        elif args.snap_cmd == "restore":
            result = os_agent.快照.恢复(args.name)
        else:
            print("❌ 请指定 snapshot 子命令: create / list / restore")
            return

        if getattr(args, 'json', False):
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            if isinstance(result, list):
                print(f"\n📸 快照列表 ({len(result)} 个):")
                for s in result:
                    ts = s.get('created_at', '')[:16]
                    print(f"  {s['name']}  {ts}  {s.get('size',0):,}B")
            elif 'error' in result:
                print(f"❌ {result['error']}")
            elif args.snap_cmd == "create":
                print(f"\n✅ 快照已创建: {result['name']}")
                print(f"  路径: {result['path']}")
                print(f"  大小: {result['size']:,} 字节")
                print(f"  DNA:  {result['dna']}")
            elif args.snap_cmd == "restore":
                print(f"\n✅ 快照已恢复: {result['restored']}")
                print(f"  备份: {result['backup']}")

    # ── memory ──
    elif args.command == "memory":
        if args.mem_cmd == "write":
            result = os_agent.记忆.写入(
                层=args.layer, 内容=args.content,
                标签=getattr(args, 'tag', None),
                来源=getattr(args, 'source', "cli"),
            )
            if getattr(args, 'json', False):
                print(json.dumps(result, ensure_ascii=False, indent=2))
            elif 'error' in result:
                print(f"❌ {result['error']}")
            else:
                print(f"✅ 记忆已写入: {result['id']} [{result['layer']}]")
                print(f"   DNA: {result['dna']}")
        elif args.mem_cmd == "query":
            result = os_agent.记忆.查询(
                层=getattr(args, 'layer', None),
                标签=getattr(args, 'tag', None),
                limit=args.limit,
            )
            if getattr(args, 'json', False):
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(f"\n📋 记忆查询 ({len(result)} 条):")
                for r in result:
                    print(f"  {r['id']} [{r['layer']}] {r['content'][:60]}...")
        elif args.mem_cmd == "stats":
            result = os_agent.记忆.统计()
            if getattr(args, 'json', False):
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(f"\n📊 记忆统计 (总计 {result['total']}):")
                for 层 in MEMORY_LAYERS:
                    print(f"  {层}: {result[层]}")
        elif args.mem_cmd == "clean":
            result = os_agent.记忆.清理(days=args.days)
            if getattr(args, 'json', False):
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(f"✅ 已清理 {result['deleted']} 条旧记忆（{args.days}天前）")
        else:
            print("❌ 请指定 memory 子命令: write / query / stats / clean")

    # ── sandbox ──
    elif args.command == "sandbox":
        if args.sbx_cmd == "exec":
            result = os_agent.沙盒.执行(代理=args.agent, 脚本=args.script, args=getattr(args, 'args', None))
        elif args.sbx_cmd == "write":
            result = os_agent.沙盒.写脚本(代理=args.agent, 名称=args.name, 内容=args.content)
        else:
            print("❌ 请指定 sandbox 子命令: exec / write")
            return

        if getattr(args, 'json', False):
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif 'error' in result:
            print(f"❌ {result['error']}")
        else:
            print(f"\n🏖️ 沙盒执行:")
            print(f"  Agent: {result.get('agent', '?')}")
            print(f"  Script: {result.get('script', '?')}")
            if 'returncode' in result:
                print(f"  返回码: {result['returncode']}")
            if result.get('stdout'):
                print(f"  输出: {result['stdout'][:200]}...")

    # ── agent ──
    elif args.command == "agent":
        if args.agt_cmd == "list":
            result = os_agent.代理.列表()
            if getattr(args, 'json', False):
                print(json.dumps([asdict(a) for a in result], ensure_ascii=False, indent=2))
            else:
                print(f"\n🤖 代理列表 ({len(result)}):")
                for a in result:
                    print(f"  {a.代理ID}  {a.名称} [{a.类型}] {a.状态}")
        elif args.agt_cmd == "register":
            result = os_agent.代理.注册(
                名称=args.name, 类型=args.type,
                模型=getattr(args, 'model', ""), 端口=getattr(args, 'port', 0),
            )
            if getattr(args, 'json', False):
                print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
            else:
                print(f"✅ 代理已注册: {result.代理ID}")
                print(f"   名称: {result.名称}  类型: {result.类型}")
        elif args.agt_cmd == "start":
            result = os_agent.代理.启动(args.id)
            if getattr(args, 'json', False):
                print(json.dumps(result, ensure_ascii=False, indent=2))
            elif 'error' in result:
                print(f"❌ {result['error']}")
            else:
                print(f"✅ 代理已启动: {result['agent_id']}")
        elif args.agt_cmd == "stop":
            result = os_agent.代理.停止(args.id)
            if getattr(args, 'json', False):
                print(json.dumps(result, ensure_ascii=False, indent=2))
            elif 'error' in result:
                print(f"❌ {result['error']}")
            else:
                print(f"✅ 代理已停止: {result['agent_id']}")
        else:
            print("❌ 请指定 agent 子命令: list / register / start / stop")

    # ── audit ──
    elif args.command == "audit":
        result = os_agent.审计.查询(limit=args.limit)
        if getattr(args, 'json', False):
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n📋 审计日志 ({len(result)} 条):")
            for r in result:
                ts = r.get('created_at', '')[:16]
                print(f"  {ts} | {r['operation']} | {r['target']} | {r['tricolor']}")

    # ── compile ──
    elif args.command == "compile":
        result = CNSH编译桥.编译(输入文件=args.input, 输出文件=getattr(args, 'output', None))
        if getattr(args, 'json', False):
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif result.get('success'):
            print(f"✅ CNSH 编译成功: {result['output']}")
            print(f"   DNA: {result['dna']}")
        else:
            print(f"❌ 编译失败: {result.get('error')}")

    # ── absorb ──
    elif args.command == "absorb":
        result = CNSH编译桥.吸收(文件路径=args.file, 名称=getattr(args, 'name', None))
        if getattr(args, 'json', False):
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif result.get('success'):
            print(f"✅ 吸收完成: {result['name']}")
            print(f"   DNA: {result['dna']}")
        else:
            print(f"❌ 吸收失败: {result.get('error')}")

    # ── daily ──
    elif args.command == "daily":
        result = os_agent.每日复盘()
        if getattr(args, 'json', False):
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n🌅 每日复盘完成")
            print(f"  快照: {result['snapshot'].get('name', '?')}")
            print(f"  审计: {result['audit'].get('id', '?')}")
            print(f"  健康: {result['evolution'].get('health_score', '?')}")
            print(f"  建议: {'; '.join(result['evolution'].get('suggestions', []))}")
            print(f"  DNA:  {result['dna']}")

    # ── evolve ──
    elif args.command == "evolve":
        result = os_agent.演化.分析()
        if getattr(args, 'json', False):
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n🧬 演化分析")
            print(f"  健康分: {result['health_score']}")
            print(f"  快照数: {result['snapshot_count']}")
            print(f"  记忆总计: {result['total_memories']}")
            print(f"  建议:")
            for s in result['suggestions']:
                print(f"    - {s}")


def quick_status() -> str:
    """快速状态（供外部导入）"""
    os_agent = CNSH本地主权AgentOS()
    stats = os_agent.记忆.统计()
    return f"CNSH AgentOS: {stats['total']} memories, {len(os_agent.快照.列表())} snapshots"


if __name__ == "__main__":
    main()
