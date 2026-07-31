# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️2026-06-19-LONGHUN-BACKUP-v5.1
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂备份管理器 (Longhun Backup Manager)
DNA: #龍芯⚡️2026-06-19-LONGHUN-BACKUP-v5.1

三层备份策略：
  L1: 协议文件备份 (41KB) - CNSH协议文件v2.0双语版
  L2: 五层脚本备份 (340KB) - L0-L4 + common + main.py + setup.sh
  L3: 配置文件备份 (135KB) - 权重·权限·熔断阈值·防护盾规则
  总备份量: 516KB

功能：
  - 三层分级备份策略
  - 全量备份 (Full Backup)
  - 增量备份 (Incremental Backup)
  - 定时备份 (Scheduled Backup)
  - 备份完整性校验
  - 备份生命周期管理
"""

import os
import sys
import json
import hashlib
import shutil
import tarfile
import gzip
import time
import threading
import schedule
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Callable, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
import logging

# ============================================================================
# 配置与常量
# ============================================================================

DEFAULT_BACKUP_ROOT = "/mnt/agents/output/longhun-v5-skills/backups"
META_FILE = "backup_meta.json"
MANIFEST_FILE = "backup_manifest.json"
CHECKSUM_ALGO = "sha256"

# 三层备份策略定义
LAYER_CONFIG = {
    "L1": {
        "name": "协议文件备份",
        "description": "CNSH协议文件v2.0双语版",
        "size_kb": 41,
        "patterns": ["**/CNSH*", "**/protocol*", "**/*协议*", "**/*.md"],
        "priority": 1,
        "retention_days": 90,
    },
    "L2": {
        "name": "五层脚本备份",
        "description": "L0-L4 + common + main.py + setup.sh",
        "size_kb": 340,
        "patterns": ["**/L[0-4]*", "**/common*", "**/main.py", "**/setup.sh", "**/*.py", "**/*.sh"],
        "priority": 2,
        "retention_days": 60,
    },
    "L3": {
        "name": "配置文件备份",
        "description": "权重·权限·熔断阈值·防护盾规则",
        "size_kb": 135,
        "patterns": ["**/config*", "**/*.json", "**/*.yaml", "**/*.yml", "**/*.toml", "**/weight*", "**/permission*", "**/fuse*", "**/shield*"],
        "priority": 3,
        "retention_days": 30,
    },
}


class BackupType(str, Enum):
    FULL = "full"           # 全量备份
    INCREMENTAL = "incremental"  # 增量备份
    SCHEDULED = "scheduled"     # 定时备份
    MANUAL = "manual"           # 手动备份


class BackupStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    VERIFIED = "verified"


# ============================================================================
# 数据类定义
# ============================================================================

@dataclass
class FileEntry:
    """文件条目"""
    path: str
    size: int
    mtime: float
    checksum: str
    layer: str = ""  # L1/L2/L3


@dataclass
class BackupSnapshot:
    """备份快照"""
    id: str
    timestamp: str
    type: str
    status: str
    layers: List[str]
    source_path: str
    backup_path: str
    size_bytes: int
    file_count: int
    checksum: str
    parent_id: Optional[str] = None  # 增量备份的父快照
    manifest: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BackupPolicy:
    """备份策略"""
    name: str
    layers: List[str]  # ["L1", "L2", "L3"]
    backup_type: BackupType
    schedule: Optional[str] = None  # cron格式或schedule库格式
    retention_count: int = 10
    retention_days: int = 30
    enabled: bool = True


# ============================================================================
# 工具函数
# ============================================================================

def generate_id() -> str:
    """生成唯一备份ID"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_suffix = hashlib.sha256(str(time.time_ns()).encode()).hexdigest()[:8]
    return f"BH_{timestamp}_{random_suffix}"


def compute_checksum(filepath: str, algo: str = CHECKSUM_ALGO) -> str:
    """计算文件校验和"""
    h = hashlib.new(algo)
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return ""


def compute_string_checksum(data: str, algo: str = CHECKSUM_ALGO) -> str:
    """计算字符串校验和"""
    h = hashlib.new(algo)
    h.update(data.encode("utf-8"))
    return h.hexdigest()


def format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f}TB"


def match_layer_patterns(filepath: str, patterns: List[str]) -> bool:
    """匹配层级模式"""
    from fnmatch import fnmatch
    for pattern in patterns:
        if fnmatch(filepath, pattern) or fnmatch(os.path.basename(filepath), pattern):
            return True
    return False


def classify_file_layer(filepath: str) -> str:
    """分类文件到对应层级"""
    for layer_id, config in LAYER_CONFIG.items():
        if match_layer_patterns(filepath, config["patterns"]):
            return layer_id
    return "L2"  # 默认归入L2


# ============================================================================
# 核心类：备份管理器
# ============================================================================

class BackupManager:
    """
    龍魂备份管理器
    
    核心功能：
    1. 三层分级备份 (L1/L2/L3)
    2. 全量备份 & 增量备份
    3. 定时备份调度
    4. 备份验证 & 生命周期管理
    """

    def __init__(self, backup_root: str = DEFAULT_BACKUP_ROOT):
        self.backup_root = Path(backup_root)
        self.backup_root.mkdir(parents=True, exist_ok=True)
        self.snapshots: Dict[str, BackupSnapshot] = {}
        self.policies: Dict[str, BackupPolicy] = {}
        self._scheduler_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._lock = threading.RLock()
        
        # 日志
        self.logger = self._setup_logger()
        
        # 加载元数据
        self._load_meta()

    def _setup_logger(self) -> logging.Logger:
        """设置日志"""
        logger = logging.getLogger("LonghunBackup")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                "[%(asctime)s] %(levelname)s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def _load_meta(self):
        """加载备份元数据"""
        meta_path = self.backup_root / META_FILE
        if meta_path.exists():
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for snap_data in data.get("snapshots", []):
                    snap = BackupSnapshot(**snap_data)
                    self.snapshots[snap.id] = snap
                for name, policy_data in data.get("policies", {}).items():
                    self.policies[name] = BackupPolicy(**policy_data)
                self.logger.info(f"已加载 {len(self.snapshots)} 个备份快照, {len(self.policies)} 个策略")
            except Exception as e:
                self.logger.warning(f"加载元数据失败: {e}")

    def _save_meta(self):
        """保存备份元数据"""
        meta_path = self.backup_root / META_FILE
        with self._lock:
            data = {
                "dna": "#龍芯⚡️2026-06-19-LONGHUN-BACKUP-v5.1",
                "updated_at": datetime.now().isoformat(),
                "snapshots": [asdict(s) for s in self.snapshots.values()],
                "policies": {name: asdict(p) for name, p in self.policies.items()},
            }
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _scan_source_files(self, source_path: str, layers: List[str]) -> List[FileEntry]:
        """扫描源文件并按层级分类"""
        source = Path(source_path)
        files = []
        
        if not source.exists():
            self.logger.error(f"源路径不存在: {source_path}")
            return files

        for root, _, filenames in os.walk(source):
            for filename in filenames:
                filepath = Path(root) / filename
                relative_path = str(filepath.relative_to(source))
                
                # 确定文件层级
                file_layer = classify_file_layer(relative_path)
                
                # 过滤只备份指定层级
                if file_layer not in layers:
                    continue
                
                stat = filepath.stat()
                entry = FileEntry(
                    path=relative_path,
                    size=stat.st_size,
                    mtime=stat.st_mtime,
                    checksum=compute_checksum(str(filepath)),
                    layer=file_layer,
                )
                files.append(entry)
        
        # 按层级排序 (L1优先)
        files.sort(key=lambda x: (LAYER_CONFIG[x.layer]["priority"], x.path))
        return files

    def _create_backup_archive(
        self,
        snapshot_id: str,
        source_path: str,
        files: List[FileEntry],
        backup_type: BackupType,
        parent_snapshot: Optional[BackupSnapshot] = None,
    ) -> Tuple[str, int, int]:
        """
        创建备份归档
        
        Returns:
            (archive_path, total_size, file_count)
        """
        snapshot_dir = self.backup_root / snapshot_id
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        
        archive_path = snapshot_dir / f"{snapshot_id}.tar.gz"
        manifest = {
            "snapshot_id": snapshot_id,
            "created_at": datetime.now().isoformat(),
            "backup_type": backup_type.value,
            "dna": "#龍芯⚡️2026-06-19-LONGHUN-BACKUP-v5.1",
            "files": [],
        }
        
        total_size = 0
        file_count = 0
        
        with tarfile.open(str(archive_path), "w:gz") as tar:
            source = Path(source_path)
            
            for entry in files:
                # 增量备份：跳过未变更文件
                if backup_type == BackupType.INCREMENTAL and parent_snapshot:
                    parent_files = parent_snapshot.manifest.get("files", [])
                    parent_entry = next(
                        (f for f in parent_files if f["path"] == entry.path), None
                    )
                    if parent_entry and parent_entry["checksum"] == entry.checksum:
                        continue
                
                full_path = source / entry.path
                if full_path.exists():
                    tar.add(str(full_path), arcname=entry.path)
                    total_size += entry.size
                    file_count += 1
                
                manifest["files"].append(asdict(entry))
        
        # 保存清单
        manifest_path = snapshot_dir / MANIFEST_FILE
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        
        # 计算归档校验和
        archive_checksum = compute_checksum(str(archive_path))
        
        return str(archive_path), total_size, file_count, archive_checksum, manifest

    # ========================================================================
    # 公开API：备份操作
    # ========================================================================

    def full_backup(
        self,
        source_path: str,
        layers: List[str] = None,
        label: str = "",
    ) -> BackupSnapshot:
        """
        执行全量备份
        
        Args:
            source_path: 源目录路径
            layers: 备份层级 ["L1", "L2", "L3"]，默认全部
            label: 备份标签
        
        Returns:
            BackupSnapshot 备份快照对象
        """
        if layers is None:
            layers = ["L1", "L2", "L3"]
        
        snapshot_id = generate_id()
        self.logger.info(f"[全量备份] 开始 | ID={snapshot_id} | 源={source_path} | 层级={layers}")
        
        # 扫描文件
        files = self._scan_source_files(source_path, layers)
        if not files:
            self.logger.warning("没有找到匹配的文件")
            return None
        
        # 创建归档
        archive_path, total_size, file_count, checksum, manifest = self._create_backup_archive(
            snapshot_id, source_path, files, BackupType.FULL
        )
        
        # 创建快照记录
        layer_stats = {}
        for layer in layers:
            layer_files = [f for f in files if f.layer == layer]
            layer_size = sum(f.size for f in layer_files)
            layer_stats[layer] = {
                "file_count": len(layer_files),
                "size_bytes": layer_size,
                "size_human": format_size(layer_size),
            }
        
        snapshot = BackupSnapshot(
            id=snapshot_id,
            timestamp=datetime.now().isoformat(),
            type=BackupType.FULL.value,
            status=BackupStatus.COMPLETED.value,
            layers=layers,
            source_path=source_path,
            backup_path=archive_path,
            size_bytes=total_size,
            file_count=file_count,
            checksum=checksum,
            manifest=manifest,
            metadata={
                "label": label,
                "layer_stats": layer_stats,
                "total_size_human": format_size(total_size),
            },
        )
        
        with self._lock:
            self.snapshots[snapshot_id] = snapshot
        self._save_meta()
        
        self.logger.info(
            f"[全量备份] 完成 | ID={snapshot_id} | "
            f"文件={file_count} | 大小={format_size(total_size)} | "
            f"校验和={checksum[:16]}..."
        )
        return snapshot

    def incremental_backup(
        self,
        source_path: str,
        base_snapshot_id: Optional[str] = None,
        layers: List[str] = None,
        label: str = "",
    ) -> BackupSnapshot:
        """
        执行增量备份
        
        Args:
            source_path: 源目录路径
            base_snapshot_id: 基础快照ID（默认使用最新的）
            layers: 备份层级
            label: 备份标签
        
        Returns:
            BackupSnapshot 备份快照对象
        """
        if layers is None:
            layers = ["L1", "L2", "L3"]
        
        # 确定父快照
        parent_snapshot = None
        if base_snapshot_id and base_snapshot_id in self.snapshots:
            parent_snapshot = self.snapshots[base_snapshot_id]
        else:
            # 查找最新的完整备份
            full_backups = [
                s for s in self.snapshots.values()
                if s.type == BackupType.FULL.value and s.layers == layers
            ]
            if full_backups:
                full_backups.sort(key=lambda x: x.timestamp, reverse=True)
                parent_snapshot = full_backups[0]
        
        if not parent_snapshot:
            self.logger.warning("未找到基础快照，将执行全量备份")
            return self.full_backup(source_path, layers, label)
        
        snapshot_id = generate_id()
        self.logger.info(
            f"[增量备份] 开始 | ID={snapshot_id} | "
            f"父快照={parent_snapshot.id} | 源={source_path}"
        )
        
        # 扫描文件
        files = self._scan_source_files(source_path, layers)
        
        # 创建增量归档
        archive_path, total_size, file_count, checksum, manifest = self._create_backup_archive(
            snapshot_id, source_path, files, BackupType.INCREMENTAL, parent_snapshot
        )
        
        snapshot = BackupSnapshot(
            id=snapshot_id,
            timestamp=datetime.now().isoformat(),
            type=BackupType.INCREMENTAL.value,
            status=BackupStatus.COMPLETED.value,
            layers=layers,
            source_path=source_path,
            backup_path=archive_path,
            size_bytes=total_size,
            file_count=file_count,
            checksum=checksum,
            parent_id=parent_snapshot.id,
            manifest=manifest,
            metadata={"label": label, "parent_checksum": parent_snapshot.checksum},
        )
        
        with self._lock:
            self.snapshots[snapshot_id] = snapshot
        self._save_meta()
        
        self.logger.info(
            f"[增量备份] 完成 | ID={snapshot_id} | "
            f"新增/变更={file_count} | 大小={format_size(total_size)}"
        )
        return snapshot

    def scheduled_backup(
        self,
        source_path: str,
        schedule_expr: str,
        backup_type: BackupType = BackupType.INCREMENTAL,
        layers: List[str] = None,
        policy_name: str = "default",
    ) -> str:
        """
        设置定时备份
        
        Args:
            source_path: 源目录路径
            schedule_expr: 调度表达式
                - "daily@02:00" 每天2点
                - "hourly" 每小时
                - "weekly@sun@03:00" 每周日3点
            backup_type: 备份类型
            layers: 备份层级
            policy_name: 策略名称
        
        Returns:
            policy_name 策略名称
        """
        if layers is None:
            layers = ["L1", "L2", "L3"]
        
        policy = BackupPolicy(
            name=policy_name,
            layers=layers,
            backup_type=backup_type,
            schedule=schedule_expr,
        )
        
        with self._lock:
            self.policies[policy_name] = policy
        self._save_meta()
        
        # 解析调度表达式
        self._parse_schedule(policy_name, source_path, schedule_expr, backup_type, layers)
        
        self.logger.info(f"[定时备份] 已设置 | 策略={policy_name} | 表达式={schedule_expr}")
        return policy_name

    def _parse_schedule(
        self,
        policy_name: str,
        source_path: str,
        schedule_expr: str,
        backup_type: BackupType,
        layers: List[str],
    ):
        """解析并注册调度表达式"""
        parts = schedule_expr.lower().split("@")
        
        def backup_job():
            self.logger.info(f"[定时任务] 执行备份 | 策略={policy_name}")
            if backup_type == BackupType.FULL:
                self.full_backup(source_path, layers, f"scheduled_{policy_name}")
            else:
                self.incremental_backup(source_path, None, layers, f"scheduled_{policy_name}")
        
        if parts[0] == "hourly":
            schedule.every().hour.do(backup_job)
        elif parts[0] == "daily" and len(parts) >= 2:
            schedule.every().day.at(parts[1]).do(backup_job)
        elif parts[0] == "weekly" and len(parts) >= 3:
            day_map = {"mon": "monday", "tue": "tuesday", "wed": "wednesday",
                      "thu": "thursday", "fri": "friday", "sat": "saturday", "sun": "sunday"}
            day = day_map.get(parts[1], "sunday")
            getattr(schedule.every(), day).at(parts[2]).do(backup_job)
        elif parts[0] == "minute":
            schedule.every(int(parts[1]) if len(parts) > 1 else 5).minutes.do(backup_job)
        else:
            # 默认每6小时
            schedule.every(6).hours.do(backup_job)

    def start_scheduler(self):
        """启动调度器线程"""
        if self._scheduler_thread and self._scheduler_thread.is_alive():
            self.logger.info("调度器已在运行")
            return
        
        self._stop_event.clear()
        
        def run_scheduler():
            self.logger.info("[调度器] 已启动")
            while not self._stop_event.is_set():
                schedule.run_pending()
                time.sleep(60)
            self.logger.info("[调度器] 已停止")
        
        self._scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        self._scheduler_thread.start()

    def stop_scheduler(self):
        """停止调度器"""
        self._stop_event.set()
        if self._scheduler_thread:
            self._scheduler_thread.join(timeout=5)
        self.logger.info("[调度器] 停止信号已发送")

    # ========================================================================
    # 公开API：查询与管理
    # ========================================================================

    def list_snapshots(
        self,
        layers: Optional[List[str]] = None,
        backup_type: Optional[str] = None,
    ) -> List[BackupSnapshot]:
        """列出备份快照"""
        results = list(self.snapshots.values())
        
        if layers:
            results = [s for s in results if any(l in s.layers for l in layers)]
        if backup_type:
            results = [s for s in results if s.type == backup_type]
        
        results.sort(key=lambda x: x.timestamp, reverse=True)
        return results

    def get_snapshot(self, snapshot_id: str) -> Optional[BackupSnapshot]:
        """获取指定快照"""
        return self.snapshots.get(snapshot_id)

    def verify_backup(self, snapshot_id: str) -> Dict[str, Any]:
        """
        验证备份完整性
        
        Returns:
            {"status": "ok|corrupted", "details": [...]}
        """
        snapshot = self.snapshots.get(snapshot_id)
        if not snapshot:
            return {"status": "error", "message": f"快照不存在: {snapshot_id}"}
        
        self.logger.info(f"[验证] 开始 | ID={snapshot_id}")
        
        archive_path = Path(snapshot.backup_path)
        if not archive_path.exists():
            return {"status": "corrupted", "message": "归档文件不存在"}
        
        # 校验归档校验和
        current_checksum = compute_checksum(str(archive_path))
        checksum_ok = current_checksum == snapshot.checksum
        
        # 验证tar.gz完整性
        tar_ok = True
        try:
            with tarfile.open(str(archive_path), "r:gz") as tar:
                members = tar.getmembers()
                for member in members:
                    if member.isfile():
                        # 尝试读取以验证
                        f = tar.extractfile(member)
                        if f:
                            f.read(1)
        except Exception as e:
            tar_ok = False
        
        status = "ok" if (checksum_ok and tar_ok) else "corrupted"
        
        result = {
            "status": status,
            "snapshot_id": snapshot_id,
            "checksum_ok": checksum_ok,
            "tar_integrity_ok": tar_ok,
            "expected_checksum": snapshot.checksum[:16] + "...",
            "actual_checksum": current_checksum[:16] + "...",
        }
        
        # 更新快照状态
        snapshot.status = BackupStatus.VERIFIED.value if status == "ok" else BackupStatus.FAILED.value
        self._save_meta()
        
        self.logger.info(f"[验证] 完成 | ID={snapshot_id} | 状态={status}")
        return result

    def delete_snapshot(self, snapshot_id: str) -> bool:
        """删除指定快照"""
        snapshot = self.snapshots.get(snapshot_id)
        if not snapshot:
            return False
        
        # 删除归档文件
        snapshot_dir = self.backup_root / snapshot_id
        if snapshot_dir.exists():
            shutil.rmtree(snapshot_dir)
        
        with self._lock:
            del self.snapshots[snapshot_id]
        self._save_meta()
        
        self.logger.info(f"[删除] 已删除快照 | ID={snapshot_id}")
        return True

    def cleanup_old_backups(self, max_age_days: Optional[int] = None):
        """
        清理过期备份
        
        按各层级保留策略清理：
        - L1: 90天
        - L2: 60天
        - L3: 30天
        """
        now = datetime.now()
        deleted = []
        
        for snap_id, snapshot in list(self.snapshots.items()):
            # 确定保留期限
            if max_age_days:
                retention = max_age_days
            else:
                retention = max(
                    LAYER_CONFIG.get(layer, {}).get("retention_days", 30)
                    for layer in snapshot.layers
                )
            
            snap_time = datetime.fromisoformat(snapshot.timestamp)
            age = (now - snap_time).days
            
            if age > retention:
                self.delete_snapshot(snap_id)
                deleted.append(snap_id)
        
        self.logger.info(f"[清理] 已删除 {len(deleted)} 个过期备份")
        return deleted

    def get_stats(self) -> Dict[str, Any]:
        """获取备份统计信息"""
        total_size = sum(s.size_bytes for s in self.snapshots.values())
        type_counts = {}
        layer_counts = {}
        
        for s in self.snapshots.values():
            type_counts[s.type] = type_counts.get(s.type, 0) + 1
            for layer in s.layers:
                layer_counts[layer] = layer_counts.get(layer, 0) + 1
        
        return {
            "total_snapshots": len(self.snapshots),
            "total_size_bytes": total_size,
            "total_size_human": format_size(total_size),
            "by_type": type_counts,
            "by_layer": layer_counts,
            "backup_root": str(self.backup_root),
            "dna": "#龍芯⚡️2026-06-19-LONGHUN-BACKUP-v5.1",
        }

    def export_manifest(self, snapshot_id: str, output_path: str):
        """导出备份清单"""
        snapshot = self.snapshots.get(snapshot_id)
        if not snapshot:
            return False
        
        manifest = {
            "snapshot": asdict(snapshot),
            "layer_config": LAYER_CONFIG,
            "export_time": datetime.now().isoformat(),
        }
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        
        return True


# ============================================================================
# CLI 命令行接口
# ============================================================================

def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="龍魂备份管理器")
    parser.add_argument("--root", default=DEFAULT_BACKUP_ROOT, help="备份根目录")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # 全量备份
    full_parser = subparsers.add_parser("full", help="全量备份")
    full_parser.add_argument("source", help="源目录路径")
    full_parser.add_argument("--layers", nargs="+", default=["L1", "L2", "L3"], help="备份层级")
    full_parser.add_argument("--label", default="", help="备份标签")
    
    # 增量备份
    incr_parser = subparsers.add_parser("incremental", help="增量备份")
    incr_parser.add_argument("source", help="源目录路径")
    incr_parser.add_argument("--base", help="基础快照ID")
    incr_parser.add_argument("--layers", nargs="+", default=["L1", "L2", "L3"], help="备份层级")
    
    # 列出快照
    list_parser = subparsers.add_parser("list", help="列出备份快照")
    list_parser.add_argument("--layer", help="过滤层级")
    list_parser.add_argument("--type", help="过滤类型")
    
    # 验证
    verify_parser = subparsers.add_parser("verify", help="验证备份")
    verify_parser.add_argument("snapshot_id", help="快照ID")
    
    # 删除
    del_parser = subparsers.add_parser("delete", help="删除快照")
    del_parser.add_argument("snapshot_id", help="快照ID")
    
    # 清理
    cleanup_parser = subparsers.add_parser("cleanup", help="清理过期备份")
    cleanup_parser.add_argument("--days", type=int, help="最大保留天数")
    
    # 统计
    subparsers.add_parser("stats", help="备份统计")
    
    # 定时备份
    sched_parser = subparsers.add_parser("schedule", help="设置定时备份")
    sched_parser.add_argument("source", help="源目录路径")
    sched_parser.add_argument("--expr", default="daily@02:00", help="调度表达式")
    sched_parser.add_argument("--type", default="incremental", choices=["full", "incremental"], help="备份类型")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = BackupManager(args.root)
    
    if args.command == "full":
        snap = manager.full_backup(args.source, args.layers, args.label)
        if snap:
            print(f"\n✅ 全量备份完成")
            print(f"   快照ID: {snap.id}")
            print(f"   文件数: {snap.file_count}")
            print(f"   大小: {format_size(snap.size_bytes)}")
            print(f"   层级: {', '.join(snap.layers)}")
    
    elif args.command == "incremental":
        snap = manager.incremental_backup(args.source, args.base, args.layers)
        if snap:
            print(f"\n✅ 增量备份完成")
            print(f"   快照ID: {snap.id}")
            print(f"   父快照: {snap.parent_id or '无'}")
            print(f"   文件数: {snap.file_count}")
            print(f"   大小: {format_size(snap.size_bytes)}")
    
    elif args.command == "list":
        layers = [args.layer] if args.layer else None
        btype = args.type if args.type else None
        snaps = manager.list_snapshots(layers, btype)
        print(f"\n📋 备份快照列表 (共 {len(snaps)} 个)\n")
        print(f"{'ID':<30} {'类型':<12} {'层级':<15} {'文件':<8} {'大小':<10} {'时间'}")
        print("-" * 100)
        for s in snaps:
            ts = s.timestamp[:19].replace("T", " ")
            layers_str = ",".join(s.layers)
            print(f"{s.id:<30} {s.type:<12} {layers_str:<15} {s.file_count:<8} {format_size(s.size_bytes):<10} {ts}")
    
    elif args.command == "verify":
        result = manager.verify_backup(args.snapshot_id)
        print(f"\n🔍 验证结果: {result['status']}")
        for k, v in result.items():
            print(f"   {k}: {v}")
    
    elif args.command == "delete":
        if manager.delete_snapshot(args.snapshot_id):
            print(f"\n🗑️  已删除快照: {args.snapshot_id}")
        else:
            print(f"\n❌ 快照不存在: {args.snapshot_id}")
    
    elif args.command == "cleanup":
        deleted = manager.cleanup_old_backups(args.days)
        print(f"\n🧹 已清理 {len(deleted)} 个过期备份")
        for sid in deleted:
            print(f"   - {sid}")
    
    elif args.command == "stats":
        stats = manager.get_stats()
        print(f"\n📊 备份统计")
        print(f"   DNA: {stats['dna']}")
        print(f"   总快照数: {stats['total_snapshots']}")
        print(f"   总大小: {stats['total_size_human']}")
        print(f"   备份根目录: {stats['backup_root']}")
        print(f"\n   按类型分布:")
        for t, c in stats['by_type'].items():
            print(f"     {t}: {c}")
        print(f"\n   按层级分布:")
        for l, c in stats['by_layer'].items():
            print(f"     {l}: {c}")
    
    elif args.command == "schedule":
        btype = BackupType.FULL if args.type == "full" else BackupType.INCREMENTAL
        policy_name = manager.scheduled_backup(args.source, args.expr, btype)
        manager.start_scheduler()
        print(f"\n⏰ 定时备份已设置")
        print(f"   策略: {policy_name}")
        print(f"   表达式: {args.expr}")
        print(f"   类型: {args.type}")
        print(f"   调度器已启动，按 Ctrl+C 停止")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            manager.stop_scheduler()
            print("\n   调度器已停止")


if __name__ == "__main__":
    main()
