#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂 日志·版本·追溯系统 v1.0
Longhun Logging · Versioning · Tracing System

DNA:#龍芯⚡️2026-06-07-LOGGING-VERSIONING-TRACING-v1.0
核心逻辑: 每次运行→记录日志→成功压缩→失败保留→版本演变一清二楚
"""

import json
import sqlite3
import gzip
import hashlib
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass, asdict
import threading

# ═══════════════════════════════════════════════════════════════════════════
# 第一部·枚举与常量
# ═══════════════════════════════════════════════════════════════════════════

class LogLevel(Enum):
    """日志级别"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    SUCCESS = "success"

class OperationType(Enum):
    """操作类型"""
    SKILL_EXECUTE = "skill_execute"
    SKILL_CREATE = "skill_create"
    SKILL_DELETE = "skill_delete"
    SKILL_UPDATE = "skill_update"
    VERSION_CREATE = "version_create"
    VERSION_DEPLOY = "version_deploy"
    SYSTEM_START = "system_start"
    SYSTEM_SHUTDOWN = "system_shutdown"
    DATA_EXPORT = "data_export"
    DATA_IMPORT = "data_import"
    ERROR_RECOVERY = "error_recovery"

class ChangeType(Enum):
    """变更类型"""
    FEATURE_ADD = "feature_add"      # 功能增加 = 扩展
    FEATURE_IMPROVE = "feature_improve"  # 功能改进 = 升级
    FEATURE_FIX = "feature_fix"      # Bug修复 = 维护
    FEATURE_REMOVE = "feature_remove"    # 功能移除 = 缩减
    PERFORMANCE_IMPROVE = "perf_improve"  # 性能改进 = 升级

# ═══════════════════════════════════════════════════════════════════════════
# 第二部·数据模型
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class LogEntry:
    """日志条目"""
    timestamp: str
    level: str
    operation: str
    category: str
    message: str
    details: Dict[str, Any]
    duration_ms: int
    status: str  # success/failure/partial
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def compress(self) -> bytes:
        """压缩日志条目 (仅成功的日志)"""
        if self.status != "success":
            return None
        content = self.to_json().encode('utf-8')
        return gzip.compress(content)
    
    def get_dna_signature(self) -> str:
        """生成DNA签章"""
        content = f"{self.timestamp}{self.operation}{self.status}{self.message}"
        hash_obj = hashlib.sha256(content.encode())
        return f"#龍芯⚡️{self.timestamp[:10]}-{hash_obj.hexdigest()[:16]}"


@dataclass
class VersionRecord:
    """版本记录"""
    version: str
    timestamp: str
    change_type: str  # feature_add/improve/fix/remove
    category: str  # skill_name or system_component
    description: str
    success_count: int = 0
    failure_count: int = 0
    dna_signature: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class SystemSnapshot:
    """系统快照 (用于演变追踪)"""
    timestamp: str
    version: str
    total_skills: int
    total_logs: int
    compressed_logs: int
    failed_logs: int
    active_categories: List[str]
    change_summary: Dict[str, int]  # 扩展/升级/维护计数
    system_health: float  # 0-100%
    dna_signature: str


# ═══════════════════════════════════════════════════════════════════════════
# 第三部·核心日志系统
# ═══════════════════════════════════════════════════════════════════════════

class LonghunLogger:
    """龍魂日志系统"""
    
    def __init__(self, db_path: str = "~/.龍魂/logs/longhun.db"):
        self.db_path = os.path.expanduser(db_path)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_database()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def init_database(self) -> None:
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 日志表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                level TEXT NOT NULL,
                operation TEXT NOT NULL,
                category TEXT NOT NULL,
                message TEXT NOT NULL,
                details TEXT,
                duration_ms INTEGER,
                status TEXT NOT NULL,
                error_message TEXT,
                compressed INTEGER DEFAULT 0,
                dna_signature TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_timestamp (timestamp),
                INDEX idx_category (category),
                INDEX idx_status (status),
                INDEX idx_compressed (compressed)
            )
        """)
        
        # 版本记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                version TEXT UNIQUE NOT NULL,
                timestamp TEXT NOT NULL,
                change_type TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                success_count INTEGER DEFAULT 0,
                failure_count INTEGER DEFAULT 0,
                dna_signature TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_version (version),
                INDEX idx_category (category),
                INDEX idx_change_type (change_type)
            )
        """)
        
        # 系统快照表 (演变追踪)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT UNIQUE NOT NULL,
                version TEXT NOT NULL,
                total_skills INTEGER,
                total_logs INTEGER,
                compressed_logs INTEGER,
                failed_logs INTEGER,
                active_categories TEXT,
                change_summary TEXT,
                system_health REAL,
                dna_signature TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_timestamp (timestamp)
            )
        """)
        
        # 压缩日志存储表 (节省空间)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS compressed_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_log_id INTEGER NOT NULL,
                compressed_data BLOB NOT NULL,
                original_size INTEGER,
                compressed_size INTEGER,
                compression_ratio REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (original_log_id) REFERENCES logs(id),
                INDEX idx_log_id (original_log_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def log(
        self,
        level: LogLevel,
        operation: str,
        category: str,
        message: str,
        details: Dict[str, Any] = None,
        duration_ms: int = 0,
        status: str = "success",
        error_message: str = None
    ) -> LogEntry:
        """记录日志"""
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            level=level.value,
            operation=operation,
            category=category,
            message=message,
            details=details or {},
            duration_ms=duration_ms,
            status=status,
            error_message=error_message
        )
        
        # 保存到数据库
        self._save_log_entry(entry)
        
        # 如果成功，后台压缩
        if status == "success":
            threading.Thread(target=self._compress_old_logs, daemon=True).start()
        
        return entry
    
    def _save_log_entry(self, entry: LogEntry) -> int:
        """保存日志条目到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        dna = entry.get_dna_signature()
        
        cursor.execute("""
            INSERT INTO logs 
            (timestamp, level, operation, category, message, details, 
             duration_ms, status, error_message, dna_signature)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entry.timestamp,
            entry.level,
            entry.operation,
            entry.category,
            entry.message,
            json.dumps(entry.details, ensure_ascii=False),
            entry.duration_ms,
            entry.status,
            entry.error_message,
            dna
        ))
        
        conn.commit()
        log_id = cursor.lastrowid
        conn.close()
        
        return log_id
    
    def _compress_old_logs(self, days: int = 7) -> Dict:
        """压缩旧的成功日志 (节省空间)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        # 查找未压缩的成功日志
        cursor.execute("""
            SELECT id, message, details FROM logs 
            WHERE status = 'success' 
            AND compressed = 0 
            AND timestamp < ?
            LIMIT 100
        """, (cutoff_date,))
        
        logs = cursor.fetchall()
        stats = {
            "compressed": 0,
            "total_size": 0,
            "compressed_size": 0,
            "ratio": 0.0
        }
        
        for log_id, message, details in logs:
            # 构建日志条目用于压缩
            content = f"{message}|{details}".encode('utf-8')
            compressed = gzip.compress(content)
            
            original_size = len(content)
            compressed_size = len(compressed)
            ratio = compressed_size / original_size if original_size > 0 else 0
            
            # 保存压缩数据
            cursor.execute("""
                INSERT INTO compressed_logs 
                (original_log_id, compressed_data, original_size, 
                 compressed_size, compression_ratio)
                VALUES (?, ?, ?, ?, ?)
            """, (log_id, compressed, original_size, compressed_size, ratio))
            
            # 标记原日志为已压缩
            cursor.execute(
                "UPDATE logs SET compressed = 1 WHERE id = ?",
                (log_id,)
            )
            
            stats["compressed"] += 1
            stats["total_size"] += original_size
            stats["compressed_size"] += compressed_size
        
        if stats["total_size"] > 0:
            stats["ratio"] = stats["compressed_size"] / stats["total_size"]
        
        conn.commit()
        conn.close()
        
        return stats
    
    def record_version(
        self,
        version: str,
        change_type: ChangeType,
        category: str,
        description: str
    ) -> VersionRecord:
        """记录版本变更"""
        record = VersionRecord(
            version=version,
            timestamp=datetime.now().isoformat(),
            change_type=change_type.value,
            category=category,
            description=description,
            dna_signature=f"#龍芯⚡️{version}-{hashlib.sha256(description.encode()).hexdigest()[:16]}"
        )
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO versions 
            (version, timestamp, change_type, category, description, dna_signature)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            record.version,
            record.timestamp,
            record.change_type,
            record.category,
            record.description,
            record.dna_signature
        ))
        
        conn.commit()
        conn.close()
        
        return record
    
    def create_snapshot(self) -> SystemSnapshot:
        """创建系统快照 (演变追踪)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 统计信息
        cursor.execute("SELECT COUNT(*) FROM logs")
        total_logs = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM logs WHERE compressed = 1")
        compressed_logs = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM logs WHERE status = 'failure'")
        failed_logs = cursor.fetchone()[0]
        
        cursor.execute(
            "SELECT COUNT(DISTINCT category) FROM logs"
        )
        total_skills = cursor.fetchone()[0]
        
        cursor.execute(
            "SELECT DISTINCT category FROM logs"
        )
        active_categories = [row[0] for row in cursor.fetchall()]
        
        # 变更类型统计
        cursor.execute("""
            SELECT change_type, COUNT(*) as count 
            FROM versions 
            GROUP BY change_type
        """)
        change_summary = {row[0]: row[1] for row in cursor.fetchall()}
        
        # 获取最新版本
        cursor.execute("SELECT version FROM versions ORDER BY timestamp DESC LIMIT 1")
        result = cursor.fetchone()
        version = result[0] if result else "1.0.0"
        
        # 计算系统健康度
        success_rate = (total_logs - failed_logs) / total_logs if total_logs > 0 else 100
        system_health = min(100, success_rate * 100)
        
        conn.close()
        
        snapshot = SystemSnapshot(
            timestamp=datetime.now().isoformat(),
            version=version,
            total_skills=total_skills,
            total_logs=total_logs,
            compressed_logs=compressed_logs,
            failed_logs=failed_logs,
            active_categories=active_categories,
            change_summary=change_summary,
            system_health=system_health,
            dna_signature=f"#龍芯⚡️{datetime.now().isoformat()[:10]}-SNAPSHOT"
        )
        
        return snapshot
    
    def get_operation_history(self, category: str, limit: int = 50) -> List[Dict]:
        """获取操作历史"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT timestamp, operation, status, message, duration_ms 
            FROM logs 
            WHERE category = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (category, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "timestamp": row[0],
                "operation": row[1],
                "status": row[2],
                "message": row[3],
                "duration_ms": row[4]
            }
            for row in rows
        ]
    
    def analyze_evolution(self) -> Dict:
        """分析系统演变 (一清二楚!)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 扩展: 新增功能
        cursor.execute("""
            SELECT COUNT(*) FROM versions 
            WHERE change_type = 'feature_add'
        """)
        extensions = cursor.fetchone()[0]
        
        # 升级: 功能改进
        cursor.execute("""
            SELECT COUNT(*) FROM versions 
            WHERE change_type IN ('feature_improve', 'perf_improve')
        """)
        upgrades = cursor.fetchone()[0]
        
        # 维护: Bug修复
        cursor.execute("""
            SELECT COUNT(*) FROM versions 
            WHERE change_type = 'feature_fix'
        """)
        maintenance = cursor.fetchone()[0]
        
        # 总日志数
        cursor.execute("SELECT COUNT(*) FROM logs")
        total_logs = cursor.fetchone()[0]
        
        # 成功率
        cursor.execute(
            "SELECT COUNT(*) FROM logs WHERE status = 'success'"
        )
        success_logs = cursor.fetchone()[0]
        
        # 压缩效率
        cursor.execute("""
            SELECT SUM(original_size), SUM(compressed_size) 
            FROM compressed_logs
        """)
        result = cursor.fetchone()
        original_size = result[0] or 0
        compressed_size = result[1] or 0
        
        conn.close()
        
        return {
            "evolution": {
                "extensions": extensions,  # 扩展功能
                "upgrades": upgrades,      # 升级改进
                "maintenance": maintenance  # 维护修复
            },
            "reliability": {
                "total_logs": total_logs,
                "success_logs": success_logs,
                "success_rate": success_logs / total_logs * 100 if total_logs > 0 else 0,
                "failure_logs": total_logs - success_logs
            },
            "storage": {
                "original_size_kb": original_size / 1024,
                "compressed_size_kb": compressed_size / 1024,
                "compression_ratio": compressed_size / original_size if original_size > 0 else 0,
                "storage_saved_kb": (original_size - compressed_size) / 1024
            }
        }


# ═══════════════════════════════════════════════════════════════════════════
# 第四部·使用示例
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🐉 龍魂日志·版本·追溯系统 v1.0")
    print("=" * 60)
    
    logger = LonghunLogger()
    
    # 记录一些操作
    print("\n📝 记录操作...")
    
    logger.log(
        level=LogLevel.INFO,
        operation="skill_execute",
        category="algorithmic-art",
        message="执行算法艺术技能",
        details={"param1": "value1"},
        duration_ms=234,
        status="success"
    )
    
    logger.log(
        level=LogLevel.SUCCESS,
        operation="skill_execute",
        category="canvas-design",
        message="执行画布设计技能",
        details={"param2": "value2"},
        duration_ms=156,
        status="success"
    )
    
    logger.log(
        level=LogLevel.ERROR,
        operation="skill_execute",
        category="brand-guidelines",
        message="品牌指南技能执行失败",
        details={"error_code": "001"},
        duration_ms=50,
        status="failure",
        error_message="资源加载失败"
    )
    
    # 记录版本
    print("\n📌 记录版本变更...")
    
    logger.record_version(
        version="1.1.0",
        change_type=ChangeType.FEATURE_ADD,
        category="algorithmic-art",
        description="添加新的配色方案"
    )
    
    logger.record_version(
        version="1.1.1",
        change_type=ChangeType.FEATURE_FIX,
        category="canvas-design",
        description="修复导出PNG的缩放问题"
    )
    
    logger.record_version(
        version="1.2.0",
        change_type=ChangeType.FEATURE_IMPROVE,
        category="doc-coauthoring",
        description="优化Markdown预览性能"
    )
    
    # 创建快照
    print("\n📸 创建系统快照...")
    snapshot = logger.create_snapshot()
    print(f"✅ 快照已创建")
    print(f"   技能数: {snapshot.total_skills}")
    print(f"   总日志: {snapshot.total_logs}")
    print(f"   压缩日志: {snapshot.compressed_logs}")
    print(f"   系统健康: {snapshot.system_health:.1f}%")
    
    # 分析演变
    print("\n📊 分析系统演变...")
    evolution = logger.analyze_evolution()
    print(f"✅ 演变分析完成")
    print(f"   扩展: {evolution['evolution']['extensions']} 个新功能")
    print(f"   升级: {evolution['evolution']['upgrades']} 次改进")
    print(f"   维护: {evolution['evolution']['maintenance']} 次修复")
    print(f"   成功率: {evolution['reliability']['success_rate']:.1f}%")
    print(f"   存储节省: {evolution['storage']['storage_saved_kb']:.2f} KB")
    
    print("\n✅ 系统运行完成！")
    print(f"🔐 DNA:#龍芯⚡️2026-06-07-LOGGING-VERSIONING-TRACING-v1.0")
