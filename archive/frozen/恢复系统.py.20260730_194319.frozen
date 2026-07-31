#!/usr/bin/env python3
#龍芯⚡️2026-06-19-LONGHUN-BACKUP-v5.1
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂恢复系统 (Longhun Recovery System)
DNA: #龍芯⚡️2026-06-19-LONGHUN-BACKUP-v5.1

功能：
  - 快照恢复 (Snapshot Restore) - 从备份快照完整恢复
  - 版本回退 (Version Rollback) - 按层级/时间点回退
  - 完整性验证 (Integrity Verification) - SHA256校验和 + tar.gz结构验证
  - 差异对比 (Diff Comparison) - 源目录与备份快照对比
  - 选择性恢复 (Selective Restore) - 按层级/文件选择性恢复
"""

import os
import sys
import json
import hashlib
import shutil
import tarfile
import time
import filecmp
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set, Any
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import tempfile

# 复用备份管理器的工具函数
sys.path.insert(0, str(Path(__file__).parent))
from 备份管理器 import (
    BackupManager,
    BackupSnapshot,
    BackupStatus,
    BackupType,
    FileEntry,
    compute_checksum,
    format_size,
    generate_id,
    LAYER_CONFIG,
    DEFAULT_BACKUP_ROOT,
    META_FILE,
    MANIFEST_FILE,
)


# ============================================================================
# 数据类定义
# ============================================================================

class RestoreStatus(str, Enum):
    PENDING = "pending"
    VERIFYING = "verifying"
    RESTORING = "restoring"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


@dataclass
class RestoreResult:
    """恢复结果"""
    restore_id: str
    snapshot_id: str
    status: str
    target_path: str
    restored_files: List[str]
    failed_files: List[str]
    skipped_files: List[str]
    total_size: int
    elapsed_seconds: float
    verification: Dict[str, Any]
    timestamp: str
    metadata: Dict[str, Any]


@dataclass
class DiffResult:
    """差异对比结果"""
    added: List[str]       # 新增文件
    removed: List[str]     # 删除文件
    modified: List[str]    # 修改文件
    unchanged: List[str]   # 未变更文件
    layer_breakdown: Dict  # 按层级分解


@dataclass
class IntegrityReport:
    """完整性验证报告"""
    snapshot_id: str
    overall_status: str   # ok / warning / corrupted
    archive_valid: bool
    checksum_valid: bool
    manifest_valid: bool
    file_checks: List[Dict]
    missing_files: List[str]
    corrupted_files: List[str]
    details: Dict[str, Any]


# ============================================================================
# 核心类：恢复系统
# ============================================================================

class RecoverySystem:
    """
    龍魂恢复系统
    
    核心功能：
    1. 快照恢复 - 从tar.gz归档完整恢复到指定目录
    2. 版本回退 - 智能回退到指定版本，处理增量链
    3. 完整性验证 - 多层验证确保备份可用
    4. 差异对比 - 对比当前目录与备份状态
    5. 选择性恢复 - 按层级或文件路径选择性恢复
    """

    def __init__(self, backup_root: str = DEFAULT_BACKUP_ROOT):
        self.backup_root = Path(backup_root)
        self.backup_manager = BackupManager(backup_root)
        self.logger = self._setup_logger()
        self._restore_history: List[Dict] = []

    def _setup_logger(self) -> logging.Logger:
        """设置日志"""
        logger = logging.getLogger("LonghunRecovery")
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

    # ========================================================================
    # 1. 完整性验证
    # ========================================================================

    def verify_integrity(self, snapshot_id: str, deep_check: bool = False) -> IntegrityReport:
        """
        完整性验证 - 多层验证确保备份可用
        
        验证层级：
        1. 归档文件存在性
        2. SHA256校验和匹配
        3. tar.gz结构完整性
        4. 清单文件一致性
        5. (deep) 逐个文件校验和验证
        
        Args:
            snapshot_id: 快照ID
            deep_check: 是否执行深度检查（逐个文件校验）
        
        Returns:
            IntegrityReport 完整性报告
        """
        self.logger.info(f"[完整性验证] 开始 | ID={snapshot_id} | 深度={deep_check}")
        
        snapshot = self.backup_manager.get_snapshot(snapshot_id)
        if not snapshot:
            return IntegrityReport(
                snapshot_id=snapshot_id,
                overall_status="corrupted",
                archive_valid=False,
                checksum_valid=False,
                manifest_valid=False,
                file_checks=[],
                missing_files=[],
                corrupted_files=[],
                details={"error": "快照不存在"},
            )
        
        archive_path = Path(snapshot.backup_path)
        file_checks = []
        missing_files = []
        corrupted_files = []
        
        # 1. 归档文件存在性
        archive_valid = archive_path.exists()
        
        # 2. SHA256校验和
        checksum_valid = False
        if archive_valid:
            current_checksum = compute_checksum(str(archive_path))
            checksum_valid = current_checksum == snapshot.checksum
        
        # 3. tar.gz结构完整性
        tar_valid = True
        tar_members = []
        if archive_valid:
            try:
                with tarfile.open(str(archive_path), "r:gz") as tar:
                    tar_members = tar.getmembers()
                    for member in tar_members:
                        if member.isfile():
                            f = tar.extractfile(member)
                            if f:
                                f.read(1)  # 尝试读取验证
            except Exception as e:
                tar_valid = False
                self.logger.error(f"[完整性验证] tar.gz损坏: {e}")
        
        # 4. 清单一致性
        manifest_valid = False
        manifest_path = archive_path.parent / MANIFEST_FILE
        if manifest_path.exists():
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest_data = json.load(f)
                manifest_valid = manifest_data.get("snapshot_id") == snapshot_id
            except Exception:
                pass
        
        # 5. 深度检查 - 逐个文件校验
        if deep_check and archive_valid and tar_valid:
            with tarfile.open(str(archive_path), "r:gz") as tar:
                for member in tar_members:
                    if not member.isfile():
                        continue
                    
                    f = tar.extractfile(member)
                    if not f:
                        missing_files.append(member.name)
                        file_checks.append({
                            "path": member.name,
                            "status": "missing",
                        })
                        continue
                    
                    # 计算文件校验和
                    h = hashlib.sha256()
                    for chunk in iter(lambda: f.read(8192), b""):
                        h.update(chunk)
                    file_checksum = h.hexdigest()
                    
                    # 与清单对比
                    manifest_entry = next(
                        (fe for fe in snapshot.manifest.get("files", [])
                         if fe["path"] == member.name), None
                    )
                    
                    if manifest_entry:
                        entry_ok = manifest_entry["checksum"] == file_checksum
                        file_checks.append({
                            "path": member.name,
                            "status": "ok" if entry_ok else "mismatch",
                            "expected": manifest_entry["checksum"][:16] + "...",
                            "actual": file_checksum[:16] + "...",
                        })
                        if not entry_ok:
                            corrupted_files.append(member.name)
                    else:
                        file_checks.append({
                            "path": member.name,
                            "status": "untracked",
                        })
        
        # 确定总体状态
        if not archive_valid or not checksum_valid or not tar_valid:
            overall = "corrupted"
        elif corrupted_files:
            overall = "warning" if len(corrupted_files) < 5 else "corrupted"
        else:
            overall = "ok"
        
        report = IntegrityReport(
            snapshot_id=snapshot_id,
            overall_status=overall,
            archive_valid=archive_valid,
            checksum_valid=checksum_valid,
            manifest_valid=manifest_valid,
            file_checks=file_checks,
            missing_files=missing_files,
            corrupted_files=corrupted_files,
            details={
                "archive_size": archive_path.stat().st_size if archive_valid else 0,
                "member_count": len(tar_members),
                "checked_files": len(file_checks),
                "snapshot_type": snapshot.type,
                "snapshot_timestamp": snapshot.timestamp,
                "layers": snapshot.layers,
            },
        )
        
        self.logger.info(
            f"[完整性验证] 完成 | ID={snapshot_id} | 状态={overall} | "
            f"归档={'✓' if archive_valid else '✗'} | "
            f"校验和={'✓' if checksum_valid else '✗'} | "
            f"TAR={'✓' if tar_valid else '✗'}"
        )
        return report

    # ========================================================================
    # 2. 快照恢复
    # ========================================================================

    def restore_snapshot(
        self,
        snapshot_id: str,
        target_path: str,
        verify_before: bool = True,
        dry_run: bool = False,
    ) -> RestoreResult:
        """
        快照恢复 - 从备份归档完整恢复到指定目录
        
        流程：
        1. 验证备份完整性（可选）
        2. 创建恢复点（备份当前状态）
        3. 解压归档到目标目录
        4. 验证恢复结果
        
        Args:
            snapshot_id: 快照ID
            target_path: 恢复目标路径
            verify_before: 恢复前是否验证完整性
            dry_run: 模拟运行，不实际恢复
        
        Returns:
            RestoreResult 恢复结果
        """
        start_time = time.time()
        restore_id = f"RS_{generate_id()}"
        
        self.logger.info(
            f"[快照恢复] 开始 | 恢复ID={restore_id} | 快照={snapshot_id} | "
            f"目标={target_path} | 模拟={dry_run}"
        )
        
        snapshot = self.backup_manager.get_snapshot(snapshot_id)
        if not snapshot:
            return self._error_result(restore_id, snapshot_id, target_path, "快照不存在")
        
        # 1. 验证完整性
        if verify_before:
            self.logger.info("[快照恢复] 验证备份完整性...")
            integrity = self.verify_integrity(snapshot_id, deep_check=True)
            if integrity.overall_status == "corrupted":
                return self._error_result(
                    restore_id, snapshot_id, target_path,
                    f"备份已损坏，无法恢复: {integrity.details}"
                )
            elif integrity.overall_status == "warning":
                self.logger.warning("[快照恢复] 备份存在警告，继续恢复...")
        
        if dry_run:
            return self._dry_run_result(restore_id, snapshot_id, target_path, snapshot)
        
        # 2. 创建恢复点（备份当前状态）
        recovery_point = None
        target = Path(target_path)
        if target.exists() and any(target.iterdir()):
            self.logger.info("[快照恢复] 创建恢复点...")
            rp_id = f"RP_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            recovery_point = self.backup_root / "recovery_points" / rp_id
            recovery_point.mkdir(parents=True, exist_ok=True)
            # 快速备份当前状态
            rp_archive = recovery_point / f"{rp_id}.tar.gz"
            with tarfile.open(str(rp_archive), "w:gz") as tar:
                tar.add(str(target), arcname=".")
            self.logger.info(f"[快照恢复] 恢复点已创建: {rp_id}")
        
        # 3. 解压归档
        archive_path = Path(snapshot.backup_path)
        restored_files = []
        failed_files = []
        skipped_files = []
        total_size = 0
        
        try:
            with tarfile.open(str(archive_path), "r:gz") as tar:
                # 如果是增量备份，需要先恢复父快照
                if snapshot.type == BackupType.INCREMENTAL.value and snapshot.parent_id:
                    self._restore_with_parent(snapshot, target, tar)
                else:
                    # 全量恢复：清空目标目录后解压
                    if target.exists():
                        for item in target.iterdir():
                            if item.is_dir():
                                shutil.rmtree(item)
                            else:
                                item.unlink()
                    else:
                        target.mkdir(parents=True, exist_ok=True)
                    
                    tar.extractall(str(target))
                
                # 记录恢复的文件
                for member in tar.getmembers():
                    if member.isfile():
                        restored_path = target / member.name
                        if restored_path.exists():
                            restored_files.append(member.name)
                            total_size += restored_path.stat().st_size
                        else:
                            failed_files.append(member.name)
        
        except Exception as e:
            self.logger.error(f"[快照恢复] 恢复失败: {e}")
            return self._error_result(restore_id, snapshot_id, target_path, str(e))
        
        elapsed = time.time() - start_time
        
        # 4. 验证恢复结果
        verification = self._verify_restore(snapshot, target_path)
        
        result = RestoreResult(
            restore_id=restore_id,
            snapshot_id=snapshot_id,
            status=RestoreStatus.COMPLETED.value if not failed_files else RestoreStatus.PARTIAL.value,
            target_path=target_path,
            restored_files=restored_files,
            failed_files=failed_files,
            skipped_files=skipped_files,
            total_size=total_size,
            elapsed_seconds=elapsed,
            verification=verification,
            timestamp=datetime.now().isoformat(),
            metadata={
                "recovery_point": str(recovery_point) if recovery_point else None,
                "snapshot_type": snapshot.type,
                "layers": snapshot.layers,
            },
        )
        
        self._restore_history.append(asdict(result))
        
        self.logger.info(
            f"[快照恢复] 完成 | 恢复ID={restore_id} | "
            f"成功={len(restored_files)} | 失败={len(failed_files)} | "
            f"耗时={elapsed:.1f}s"
        )
        return result

    def _restore_with_parent(
        self,
        snapshot: BackupSnapshot,
        target: Path,
        incremental_tar: tarfile.TarFile,
    ):
        """恢复增量备份（先恢复父快照，再应用增量）"""
        # 递归恢复父快照
        if snapshot.parent_id:
            parent = self.backup_manager.get_snapshot(snapshot.parent_id)
            if parent:
                self.logger.info(f"[增量恢复] 先恢复父快照: {parent.id}")
                parent_archive = Path(parent.backup_path)
                with tarfile.open(str(parent_archive), "r:gz") as parent_tar:
                    self._restore_with_parent(parent, target, parent_tar)
        
        # 应用增量变更
        incremental_tar.extractall(str(target))

    def _verify_restore(self, snapshot: BackupSnapshot, target_path: str) -> Dict[str, Any]:
        """验证恢复结果"""
        target = Path(target_path)
        if not target.exists():
            return {"status": "failed", "reason": "目标目录不存在"}
        
        # 检查关键文件是否存在
        manifest_files = snapshot.manifest.get("files", [])
        found = 0
        missing = 0
        
        for fentry in manifest_files:
            fpath = target / fentry["path"]
            if fpath.exists():
                found += 1
            else:
                missing += 1
        
        return {
            "status": "ok" if missing == 0 else "partial",
            "expected_files": len(manifest_files),
            "found_files": found,
            "missing_files": missing,
        }

    def _error_result(self, restore_id: str, snapshot_id: str, target: str, error: str) -> RestoreResult:
        """创建错误结果"""
        return RestoreResult(
            restore_id=restore_id,
            snapshot_id=snapshot_id,
            status=RestoreStatus.FAILED.value,
            target_path=target,
            restored_files=[],
            failed_files=[],
            skipped_files=[],
            total_size=0,
            elapsed_seconds=0,
            verification={"error": error},
            timestamp=datetime.now().isoformat(),
            metadata={"error": error},
        )

    def _dry_run_result(self, restore_id: str, snapshot_id: str, target: str, snapshot: BackupSnapshot) -> RestoreResult:
        """创建模拟运行结果"""
        manifest_files = snapshot.manifest.get("files", [])
        return RestoreResult(
            restore_id=restore_id,
            snapshot_id=snapshot_id,
            status="dry_run",
            target_path=target,
            restored_files=[f["path"] for f in manifest_files],
            failed_files=[],
            skipped_files=[],
            total_size=sum(f.get("size", 0) for f in manifest_files),
            elapsed_seconds=0,
            verification={"mode": "dry_run", "would_restore": len(manifest_files)},
            timestamp=datetime.now().isoformat(),
            metadata={"dry_run": True},
        )

    # ========================================================================
    # 3. 版本回退
    # ========================================================================

    def rollback(
        self,
        target_path: str,
        to_snapshot_id: Optional[str] = None,
        to_timestamp: Optional[str] = None,
        to_layer_version: Optional[str] = None,
        dry_run: bool = False,
    ) -> RestoreResult:
        """
        版本回退 - 智能回退到指定版本
        
        回退策略：
        1. 指定快照ID -> 直接恢复到该快照
        2. 指定时间戳 -> 找到最接近的快照恢复
        3. 指定层级版本 -> 找到该层级的最新快照恢复
        
        Args:
            target_path: 回退目标路径
            to_snapshot_id: 目标快照ID
            to_timestamp: 目标时间戳 (ISO格式)
            to_layer_version: 目标层级版本 (如 "L1", "L2", "L3")
            dry_run: 模拟运行
        
        Returns:
            RestoreResult 恢复结果
        """
        self.logger.info(
            f"[版本回退] 开始 | 目标={target_path} | "
            f"快照={to_snapshot_id} | 时间={to_timestamp} | 层级={to_layer_version}"
        )
        
        snapshot = None
        
        # 策略1: 指定快照ID
        if to_snapshot_id:
            snapshot = self.backup_manager.get_snapshot(to_snapshot_id)
        
        # 策略2: 指定时间戳
        elif to_timestamp:
            target_time = datetime.fromisoformat(to_timestamp)
            candidates = self.backup_manager.list_snapshots()
            if candidates:
                # 找到最接近且不超过目标时间的快照
                best = None
                best_diff = float('inf')
                for c in candidates:
                    c_time = datetime.fromisoformat(c.timestamp)
                    diff = abs((c_time - target_time).total_seconds())
                    if diff < best_diff:
                        best_diff = diff
                        best = c
                snapshot = best
        
        # 策略3: 指定层级
        elif to_layer_version:
            candidates = self.backup_manager.list_snapshots(layers=[to_layer_version])
            if candidates:
                snapshot = candidates[0]  # 最新的
        
        if not snapshot:
            return self._error_result(
                f"RB_{generate_id()}", "unknown", target_path,
                "未找到匹配的回退目标快照"
            )
        
        self.logger.info(f"[版本回退] 选定快照: {snapshot.id} ({snapshot.timestamp})")
        
        # 执行恢复
        return self.restore_snapshot(
            snapshot.id,
            target_path,
            verify_before=True,
            dry_run=dry_run,
        )

    def rollback_to_last_good(
        self,
        target_path: str,
        dry_run: bool = False,
    ) -> RestoreResult:
        """
        回退到最后一个验证通过的版本
        
        自动查找最近一个完整性验证通过的快照进行恢复。
        """
        self.logger.info("[智能回退] 查找最后一个验证通过的版本...")
        
        candidates = self.backup_manager.list_snapshots()
        for snapshot in candidates:
            integrity = self.verify_integrity(snapshot.id, deep_check=False)
            if integrity.overall_status == "ok":
                self.logger.info(f"[智能回退] 找到可用快照: {snapshot.id}")
                return self.restore_snapshot(
                    snapshot.id, target_path,
                    verify_before=False,  # 已验证
                    dry_run=dry_run,
                )
        
        return self._error_result(
            f"RG_{generate_id()}", "unknown", target_path,
            "未找到任何验证通过的备份"
        )

    # ========================================================================
    # 4. 差异对比
    # ========================================================================

    def diff_against_snapshot(
        self,
        snapshot_id: str,
        current_path: str,
        layers: Optional[List[str]] = None,
    ) -> DiffResult:
        """
        差异对比 - 对比当前目录与备份快照
        
        Args:
            snapshot_id: 快照ID
            current_path: 当前目录路径
            layers: 只对比指定层级
        
        Returns:
            DiffResult 差异结果
        """
        self.logger.info(f"[差异对比] 开始 | 快照={snapshot_id} | 当前={current_path}")
        
        snapshot = self.backup_manager.get_snapshot(snapshot_id)
        if not snapshot:
            return DiffResult([], [], [], [], {})
        
        # 获取快照中的文件
        snapshot_files: Dict[str, FileEntry] = {}
        for fentry in snapshot.manifest.get("files", []):
            if layers and fentry.get("layer") not in layers:
                continue
            snapshot_files[fentry["path"]] = FileEntry(**fentry)
        
        # 扫描当前目录
        current_files: Dict[str, FileEntry] = {}
        current = Path(current_path)
        if current.exists():
            for root, _, filenames in os.walk(current):
                for filename in filenames:
                    filepath = Path(root) / filename
                    relative = str(filepath.relative_to(current))
                    if layers:
                        from 备份管理器 import classify_file_layer
                        if classify_file_layer(relative) not in layers:
                            continue
                    stat = filepath.stat()
                    current_files[relative] = FileEntry(
                        path=relative,
                        size=stat.st_size,
                        mtime=stat.st_mtime,
                        checksum=compute_checksum(str(filepath)),
                    )
        
        # 计算差异
        snap_keys = set(snapshot_files.keys())
        curr_keys = set(current_files.keys())
        
        added = list(curr_keys - snap_keys)           # 新增
        removed = list(snap_keys - curr_keys)          # 删除
        modified = []                                   # 修改
        unchanged = []                                  # 未变更
        
        for key in snap_keys & curr_keys:
            s_file = snapshot_files[key]
            c_file = current_files[key]
            if s_file.checksum != c_file.checksum or s_file.size != c_file.size:
                modified.append(key)
            else:
                unchanged.append(key)
        
        # 按层级分解
        layer_breakdown = {}
        for layer in ["L1", "L2", "L3"]:
            layer_added = [f for f in added if self._get_layer(f) == layer]
            layer_removed = [f for f in removed if self._get_layer(f) == layer]
            layer_modified = [f for f in modified if self._get_layer(f) == layer]
            layer_breakdown[layer] = {
                "added": len(layer_added),
                "removed": len(layer_removed),
                "modified": len(layer_modified),
            }
        
        result = DiffResult(
            added=sorted(added),
            removed=sorted(removed),
            modified=sorted(modified),
            unchanged=sorted(unchanged),
            layer_breakdown=layer_breakdown,
        )
        
        self.logger.info(
            f"[差异对比] 完成 | 新增={len(added)} | 删除={len(removed)} | "
            f"修改={len(modified)} | 未变更={len(unchanged)}"
        )
        return result

    def _get_layer(self, filepath: str) -> str:
        """获取文件层级"""
        from 备份管理器 import classify_file_layer
        return classify_file_layer(filepath)

    # ========================================================================
    # 5. 选择性恢复
    # ========================================================================

    def selective_restore(
        self,
        snapshot_id: str,
        target_path: str,
        layers: Optional[List[str]] = None,
        file_patterns: Optional[List[str]] = None,
        verify_before: bool = True,
        dry_run: bool = False,
    ) -> RestoreResult:
        """
        选择性恢复 - 按层级或文件模式恢复
        
        Args:
            snapshot_id: 快照ID
            target_path: 恢复目标路径
            layers: 只恢复指定层级 ["L1", "L2", "L3"]
            file_patterns: 文件匹配模式 (如 ["*.py", "*.json"])
            verify_before: 恢复前验证
            dry_run: 模拟运行
        
        Returns:
            RestoreResult 恢复结果
        """
        start_time = time.time()
        restore_id = f"SR_{generate_id()}"
        
        self.logger.info(
            f"[选择性恢复] 开始 | ID={restore_id} | 快照={snapshot_id} | "
            f"层级={layers} | 模式={file_patterns}"
        )
        
        snapshot = self.backup_manager.get_snapshot(snapshot_id)
        if not snapshot:
            return self._error_result(restore_id, snapshot_id, target_path, "快照不存在")
        
        if verify_before:
            integrity = self.verify_integrity(snapshot_id)
            if integrity.overall_status == "corrupted":
                return self._error_result(restore_id, snapshot_id, target_path, "备份已损坏")
        
        # 筛选要恢复的文件
        files_to_restore = []
        for fentry in snapshot.manifest.get("files", []):
            # 层级过滤
            if layers and fentry.get("layer") not in layers:
                continue
            # 模式过滤
            if file_patterns:
                from fnmatch import fnmatch
                if not any(fnmatch(fentry["path"], p) for p in file_patterns):
                    continue
            files_to_restore.append(fentry)
        
        if dry_run:
            return RestoreResult(
                restore_id=restore_id,
                snapshot_id=snapshot_id,
                status="dry_run",
                target_path=target_path,
                restored_files=[f["path"] for f in files_to_restore],
                failed_files=[],
                skipped_files=[],
                total_size=sum(f.get("size", 0) for f in files_to_restore),
                elapsed_seconds=0,
                verification={"mode": "dry_run", "would_restore": len(files_to_restore)},
                timestamp=datetime.now().isoformat(),
                metadata={"layers": layers, "patterns": file_patterns, "dry_run": True},
            )
        
        # 执行恢复
        target = Path(target_path)
        target.mkdir(parents=True, exist_ok=True)
        
        archive_path = Path(snapshot.backup_path)
        restored_files = []
        failed_files = []
        total_size = 0
        
        restore_set = {f["path"] for f in files_to_restore}
        
        with tarfile.open(str(archive_path), "r:gz") as tar:
            for member in tar.getmembers():
                if member.name in restore_set:
                    try:
                        tar.extract(member, str(target))
                        restored_path = target / member.name
                        if restored_path.exists():
                            restored_files.append(member.name)
                            total_size += restored_path.stat().st_size
                    except Exception as e:
                        self.logger.error(f"[选择性恢复] 失败: {member.name}: {e}")
                        failed_files.append(member.name)
        
        elapsed = time.time() - start_time
        
        result = RestoreResult(
            restore_id=restore_id,
            snapshot_id=snapshot_id,
            status=RestoreStatus.COMPLETED.value if not failed_files else RestoreStatus.PARTIAL.value,
            target_path=target_path,
            restored_files=restored_files,
            failed_files=failed_files,
            skipped_files=[],
            total_size=total_size,
            elapsed_seconds=elapsed,
            verification={"restored": len(restored_files), "failed": len(failed_files)},
            timestamp=datetime.now().isoformat(),
            metadata={"layers": layers, "patterns": file_patterns},
        )
        
        self.logger.info(
            f"[选择性恢复] 完成 | ID={restore_id} | "
            f"恢复={len(restored_files)} | 失败={len(failed_files)} | "
            f"耗时={elapsed:.1f}s"
        )
        return result

    # ========================================================================
    # 6. 恢复历史
    # ========================================================================

    def get_restore_history(self) -> List[Dict]:
        """获取恢复历史"""
        return self._restore_history

    def clear_restore_history(self):
        """清除恢复历史"""
        self._restore_history.clear()
        self.logger.info("[恢复历史] 已清除")


# ============================================================================
# CLI 命令行接口
# ============================================================================

def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="龍魂恢复系统")
    parser.add_argument("--root", default=DEFAULT_BACKUP_ROOT, help="备份根目录")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # 完整性验证
    verify_parser = subparsers.add_parser("verify", help="验证备份完整性")
    verify_parser.add_argument("snapshot_id", help="快照ID")
    verify_parser.add_argument("--deep", action="store_true", help="深度检查")
    
    # 快照恢复
    restore_parser = subparsers.add_parser("restore", help="快照恢复")
    restore_parser.add_argument("snapshot_id", help="快照ID")
    restore_parser.add_argument("target", help="目标路径")
    restore_parser.add_argument("--no-verify", action="store_true", help="跳过验证")
    restore_parser.add_argument("--dry-run", action="store_true", help="模拟运行")
    
    # 版本回退
    rollback_parser = subparsers.add_parser("rollback", help="版本回退")
    rollback_parser.add_argument("target", help="目标路径")
    rollback_parser.add_argument("--snapshot", help="指定快照ID")
    rollback_parser.add_argument("--time", help="指定时间戳")
    rollback_parser.add_argument("--layer", choices=["L1", "L2", "L3"], help="指定层级")
    rollback_parser.add_argument("--dry-run", action="store_true", help="模拟运行")
    
    # 智能回退
    rb_good = subparsers.add_parser("rollback-good", help="回退到最后可用版本")
    rb_good.add_argument("target", help="目标路径")
    rb_good.add_argument("--dry-run", action="store_true", help="模拟运行")
    
    # 差异对比
    diff_parser = subparsers.add_parser("diff", help="差异对比")
    diff_parser.add_argument("snapshot_id", help="快照ID")
    diff_parser.add_argument("current", help="当前目录路径")
    diff_parser.add_argument("--layer", nargs="+", help="指定层级")
    
    # 选择性恢复
    sel_parser = subparsers.add_parser("selective", help="选择性恢复")
    sel_parser.add_argument("snapshot_id", help="快照ID")
    sel_parser.add_argument("target", help="目标路径")
    sel_parser.add_argument("--layer", nargs="+", choices=["L1", "L2", "L3"], help="层级过滤")
    sel_parser.add_argument("--pattern", nargs="+", help="文件模式过滤")
    sel_parser.add_argument("--dry-run", action="store_true", help="模拟运行")
    
    # 恢复历史
    hist_parser = subparsers.add_parser("history", help="恢复历史")
    hist_parser.add_argument("--clear", action="store_true", help="清除历史")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    recovery = RecoverySystem(args.root)
    
    if args.command == "verify":
        report = recovery.verify_integrity(args.snapshot_id, deep_check=args.deep)
        print(f"\n🔍 完整性验证报告: {args.snapshot_id}")
        print(f"   总体状态: {report.overall_status.upper()}")
        print(f"   归档有效: {'✅' if report.archive_valid else '❌'}")
        print(f"   校验和匹配: {'✅' if report.checksum_valid else '❌'}")
        print(f"   清单有效: {'✅' if report.manifest_valid else '❌'}")
        if report.corrupted_files:
            print(f"   ⚠️  损坏文件: {len(report.corrupted_files)}")
            for f in report.corrupted_files[:10]:
                print(f"      - {f}")
        if args.deep and report.file_checks:
            print(f"\n   文件检查详情 ({len(report.file_checks)} 个):")
            for fc in report.file_checks[:20]:
                icon = "✅" if fc["status"] == "ok" else "❌"
                print(f"      {icon} {fc['path']}: {fc['status']}")
    
    elif args.command == "restore":
        result = recovery.restore_snapshot(
            args.snapshot_id, args.target,
            verify_before=not args.no_verify,
            dry_run=args.dry_run,
        )
        print(f"\n{'🔄' if not args.dry_run else '📋'} 恢复结果")
        print(f"   恢复ID: {result.restore_id}")
        print(f"   状态: {result.status}")
        print(f"   恢复文件: {len(result.restored_files)}")
        print(f"   失败文件: {len(result.failed_files)}")
        print(f"   总大小: {format_size(result.total_size)}")
        print(f"   耗时: {result.elapsed_seconds:.1f}s")
        if result.verification:
            print(f"   验证: {result.verification}")
    
    elif args.command == "rollback":
        result = recovery.rollback(
            args.target,
            to_snapshot_id=args.snapshot,
            to_timestamp=args.time,
            to_layer_version=args.layer,
            dry_run=args.dry_run,
        )
        print(f"\n⏮️  回退结果")
        print(f"   恢复ID: {result.restore_id}")
        print(f"   状态: {result.status}")
        print(f"   目标: {result.target_path}")
        print(f"   恢复文件: {len(result.restored_files)}")
        print(f"   耗时: {result.elapsed_seconds:.1f}s")
    
    elif args.command == "rollback-good":
        result = recovery.rollback_to_last_good(args.target, dry_run=args.dry_run)
        print(f"\n🔄 智能回退结果")
        print(f"   恢复ID: {result.restore_id}")
        print(f"   状态: {result.status}")
        print(f"   恢复文件: {len(result.restored_files)}")
        print(f"   耗时: {result.elapsed_seconds:.1f}s")
    
    elif args.command == "diff":
        result = recovery.diff_against_snapshot(
            args.snapshot_id, args.current, args.layer,
        )
        print(f"\n📊 差异对比结果: {args.snapshot_id} vs {args.current}")
        print(f"   新增: {len(result.added)}")
        print(f"   删除: {len(result.removed)}")
        print(f"   修改: {len(result.modified)}")
        print(f"   未变更: {len(result.unchanged)}")
        print(f"\n   按层级分解:")
        for layer, stats in result.layer_breakdown.items():
            print(f"     {layer}: +{stats['added']} -{stats['removed']} ~{stats['modified']}")
        if result.added:
            print(f"\n   新增文件 (前10):")
            for f in result.added[:10]:
                print(f"     + {f}")
        if result.removed:
            print(f"\n   删除文件 (前10):")
            for f in result.removed[:10]:
                print(f"     - {f}")
        if result.modified:
            print(f"\n   修改文件 (前10):")
            for f in result.modified[:10]:
                print(f"     ~ {f}")
    
    elif args.command == "selective":
        result = recovery.selective_restore(
            args.snapshot_id, args.target,
            layers=args.layer,
            file_patterns=args.pattern,
            dry_run=args.dry_run,
        )
        print(f"\n🎯 选择性恢复结果")
        print(f"   恢复ID: {result.restore_id}")
        print(f"   状态: {result.status}")
        print(f"   恢复文件: {len(result.restored_files)}")
        print(f"   总大小: {format_size(result.total_size)}")
        print(f"   耗时: {result.elapsed_seconds:.1f}s")
    
    elif args.command == "history":
        if args.clear:
            recovery.clear_restore_history()
            print("🗑️  恢复历史已清除")
        else:
            history = recovery.get_restore_history()
            print(f"\n📜 恢复历史 (共 {len(history)} 条)")
            for h in history:
                print(f"   [{h.get('timestamp', '?')[:19]}] "
                      f"{h.get('restore_id', '?')} | "
                      f"{h.get('status', '?')} | "
                      f"{len(h.get('restored_files', []))} files")


if __name__ == "__main__":
    main()
