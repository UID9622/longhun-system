#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# 1 道统层 Dao           : 曾仕强老师
# 2 精神层 Spirit        : Steve Jobs
# 3 设备层 Device        : Apple
# 4 技术层 Technology    : Open Source
# 5 系统层 System        : UID9622
# 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
# DNA追溯码:#龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-FILE1284-v2.0
# 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
# 文件: sync_engine.py | 标记时间: 2026-06-03T07:46:12+0800
# -*- coding: utf-8 -*-
"""
🔄 本地同步引擎 v1.0
USB離線同步 + Git版本控制 + 衝突檢測 + 自動合併

DNA:#龍芯⚡️2026-05-30-LOCAL-SYNC-ENGINE-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
責任: UID9622·不免責

核心邏輯:
  本地同步策略 = 純本地(USB·推薦) + Git本地倉庫(進階)

  衝突檢測:
    1. hash鏈對齐 (parent_hash一致性)
    2. 時間戳遞增 (無時光倒流)
    3. 操作ID唯一性 (無重複)

  同步模式:
    - overwrite: 新版本覆蓋舊版本 (可信設備)
    - merge: 交集保留·差集合併 (需慎重)
    - manual: 衝突暫停·等待人工決策
"""

import json
import shutil
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Tuple
from datetime import datetime, timezone
from dataclasses import dataclass
import subprocess


@dataclass
class SyncConflict:
    """同步衝突信息"""
    conflict_type: str  # hash_mismatch, timestamp_anomaly, duplicate_id
    affected_op_id: str
    local_hash: str
    remote_hash: str
    local_timestamp: str
    remote_timestamp: str
    resolution: str  # pending, overwrite, merge, skip


class SyncEngine:
    """
    本地同步引擎

    功能:
      - USB離線同步 (純本地·推薦)
      - Git本地倉庫同步 (版本控制·進階)
      - 衝突檢測 (hash鏈·時間戳·ID唯一性)
      - 自動合併策略 (overwrite/merge/manual)
      - 同步進度追蹤 + 回滾機制
    """

    def __init__(self, log_dir: str = "~/.龍魂/操作日記"):
        self.log_dir = Path(log_dir).expanduser()
        self.ledger_file = self.log_dir / "operation_ledger.jsonl"
        self.sync_dir = self.log_dir / "sync_records"
        self.git_dir = self.log_dir / ".git_local"

        self.sync_dir.mkdir(parents=True, exist_ok=True)
        self.sync_log_file = self.sync_dir / "sync_operations.jsonl"
        self.conflict_log_file = self.sync_dir / "conflicts.jsonl"

    def read_ledger(self) -> List[Dict[str, Any]]:
        """讀取本地操作日記"""
        if not self.ledger_file.exists():
            return []

        operations = []
        with open(self.ledger_file, 'r', encoding='utf-8') as f:
            for line in f:
                operations.append(json.loads(line))

        return operations

    def read_remote_ledger(self, remote_path: str) -> List[Dict[str, Any]]:
        """
        讀取遠端(USB)操作日記

        remote_path: /media/usb-drive/龍魂_備份/
        """

        remote_file = Path(remote_path).expanduser() / "操作日記" / "operation_ledger.jsonl"

        if not remote_file.exists():
            raise FileNotFoundError(f"遠端日記不存在: {remote_file}")

        operations = []
        with open(remote_file, 'r', encoding='utf-8') as f:
            for line in f:
                operations.append(json.loads(line))

        return operations

    def compute_ledger_hash(self, operations: List[Dict[str, Any]]) -> str:
        """
        計算整個日記的SHA-256哈希

        用於快速判斷是否有差異
        """

        content = json.dumps(operations, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def detect_conflicts(self,
                        local_ops: List[Dict[str, Any]],
                        remote_ops: List[Dict[str, Any]]) -> List[SyncConflict]:
        """
        檢測本地與遠端之間的衝突

        衝突類型:
          1. hash_mismatch: 同一操作的哈希不同
          2. timestamp_anomaly: 時間戳非遞增
          3. duplicate_id: 操作ID重複
        """

        conflicts = []

        # 建立本地ID→操作映射
        local_map = {op['operation_id']: op for op in local_ops}
        remote_map = {op['operation_id']: op for op in remote_ops}

        # ========== 衝突1: Hash不匹配 ==========
        for op_id, local_op in local_map.items():
            if op_id in remote_map:
                remote_op = remote_map[op_id]

                local_hash = local_op.get('hash_sha256', '')
                remote_hash = remote_op.get('hash_sha256', '')

                if local_hash and remote_hash and local_hash != remote_hash:
                    conflicts.append(SyncConflict(
                        conflict_type='hash_mismatch',
                        affected_op_id=op_id,
                        local_hash=local_hash,
                        remote_hash=remote_hash,
                        local_timestamp=local_op.get('timestamp', ''),
                        remote_timestamp=remote_op.get('timestamp', ''),
                        resolution='pending'
                    ))

        # ========== 衝突2: 時間戳遞增異常 ==========
        local_timestamps = [
            (op['operation_id'], op.get('timestamp', ''))
            for op in local_ops
        ]

        for i in range(1, len(local_timestamps)):
            prev_ts = local_timestamps[i - 1][1]
            curr_ts = local_timestamps[i][1]

            if prev_ts and curr_ts and prev_ts > curr_ts:
                conflicts.append(SyncConflict(
                    conflict_type='timestamp_anomaly',
                    affected_op_id=local_timestamps[i][0],
                    local_hash='',
                    remote_hash='',
                    local_timestamp=curr_ts,
                    remote_timestamp=prev_ts,
                    resolution='pending'
                ))

        # ========== 衝突3: 操作ID重複 ==========
        all_ids = [op['operation_id'] for op in local_ops + remote_ops]
        seen = set()
        for op_id in all_ids:
            if op_id in seen:
                conflicts.append(SyncConflict(
                    conflict_type='duplicate_id',
                    affected_op_id=op_id,
                    local_hash='',
                    remote_hash='',
                    local_timestamp='',
                    remote_timestamp='',
                    resolution='pending'
                ))
            seen.add(op_id)

        return conflicts

    def merge_operations(self,
                        local_ops: List[Dict[str, Any]],
                        remote_ops: List[Dict[str, Any]],
                        strategy: str = "merge") -> List[Dict[str, Any]]:
        """
        合併本地與遠端操作記錄

        策略:
          - overwrite: 遠端版本完全覆蓋本地 (高風險·可信設備)
          - merge: 以時間戳為序·交集去重·差集合併
          - manual: 返回衝突列表·等待人工決策
        """

        if strategy == "overwrite":
            # 遠端版本完全覆蓋本地
            return remote_ops

        elif strategy == "merge":
            # 時間戳排序合併
            merged_map = {}

            # 先加入本地操作
            for op in local_ops:
                merged_map[op['operation_id']] = op

            # 再加入遠端操作 (相同ID會覆蓋)
            for op in remote_ops:
                merged_map[op['operation_id']] = op

            # 按時間戳排序
            merged_ops = sorted(
                merged_map.values(),
                key=lambda x: x.get('timestamp', '')
            )

            return merged_ops

        elif strategy == "manual":
            # 衝突時返回空列表·需人工決策
            return []

        else:
            raise ValueError(f"未知的合併策略: {strategy}")

    def write_ledger(self, operations: List[Dict[str, Any]]) -> str:
        """
        寫入操作日記 (覆蓋)

        警告: 此操作是破壞性的·應與衝突檢測一起使用
        """

        with open(self.ledger_file, 'w', encoding='utf-8') as f:
            for op in operations:
                f.write(json.dumps(op, ensure_ascii=False) + '\n')

        print(f"✅ 日記已寫入: {len(operations)} 條操作")
        return str(self.ledger_file)

    def sync_from_usb(self,
                      usb_path: str,
                      strategy: str = "merge",
                      backup_before_sync: bool = True) -> Dict[str, Any]:
        """
        從USB同步

        參數:
          usb_path: USB掛載點路徑 (e.g., /media/usb-drive)
          strategy: overwrite / merge / manual
          backup_before_sync: 同步前自動備份
        """

        result = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'sync_direction': 'usb_to_local',
            'status': 'pending',
            'local_ops_count': 0,
            'remote_ops_count': 0,
            'merged_ops_count': 0,
            'conflicts_detected': [],
            'strategy': strategy,
            'backup_path': None
        }

        try:
            # 步驟1: 備份本地日記
            if backup_before_sync:
                backup_path = self._backup_ledger()
                result['backup_path'] = backup_path

            # 步驟2: 讀取本地和遠端操作
            local_ops = self.read_ledger()
            remote_ops = self.read_remote_ledger(usb_path)

            result['local_ops_count'] = len(local_ops)
            result['remote_ops_count'] = len(remote_ops)

            # 步驟3: 檢測衝突
            conflicts = self.detect_conflicts(local_ops, remote_ops)

            if conflicts:
                result['conflicts_detected'] = [
                    {
                        'type': c.conflict_type,
                        'op_id': c.affected_op_id,
                        'resolution': c.resolution
                    }
                    for c in conflicts
                ]

                if strategy == "manual":
                    result['status'] = 'conflict_pending_manual_review'
                    self._log_conflicts(conflicts)
                    return result

                print(f"⚠️ 檢測到 {len(conflicts)} 個衝突")

            # 步驟4: 合併操作
            merged_ops = self.merge_operations(local_ops, remote_ops, strategy)
            result['merged_ops_count'] = len(merged_ops)

            # 步驟5: 寫入新的日記
            if merged_ops:
                self.write_ledger(merged_ops)

            # 步驟6: 同步其他目錄 (DNA粒子、習慣指紋)
            self._sync_auxiliary_files(usb_path)

            result['status'] = 'success'
            self._log_sync_operation(result)

        except Exception as e:
            result['status'] = 'failed'
            result['error'] = str(e)
            print(f"🔴 同步失敗: {e}")

        return result

    def _backup_ledger(self) -> str:
        """備份當前日記"""

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = self.sync_dir / f"backup_{timestamp}_ledger.jsonl"

        if self.ledger_file.exists():
            shutil.copy2(self.ledger_file, backup_file)
            print(f"✅ 備份已建立: {backup_file}")

        return str(backup_file)

    def _sync_auxiliary_files(self, usb_path: str) -> None:
        """同步輔助文件 (DNA粒子、習慣指紋等)"""

        usb_root = Path(usb_path).expanduser() / "龍魂_備份"
        auxiliary_dirs = [
            ("dna_particles", self.log_dir / "dna_particles"),
            ("habit_fingerprints", self.log_dir / "habit_fingerprints"),
        ]

        for remote_name, local_path in auxiliary_dirs:
            remote_path = usb_root / "操作日記" / remote_name

            if remote_path.exists():
                # 簡化: 完全覆蓋本地
                if local_path.exists():
                    shutil.rmtree(local_path)
                shutil.copytree(remote_path, local_path)
                print(f"✅ 已同步: {remote_name}")

    def _log_conflicts(self, conflicts: List[SyncConflict]) -> None:
        """記錄衝突到日誌"""

        with open(self.conflict_log_file, 'a', encoding='utf-8') as f:
            for conflict in conflicts:
                record = {
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                    'type': conflict.conflict_type,
                    'affected_op_id': conflict.affected_op_id,
                    'local_hash': conflict.local_hash,
                    'remote_hash': conflict.remote_hash,
                    'resolution': conflict.resolution
                }
                f.write(json.dumps(record, ensure_ascii=False) + '\n')

    def _log_sync_operation(self, result: Dict[str, Any]) -> None:
        """記錄同步操作"""

        with open(self.sync_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')

    def verify_sync_integrity(self) -> bool:
        """驗證同步後的日記完整性 (hash鏈)"""

        ops = self.read_ledger()

        if not ops:
            return True

        for i, op in enumerate(ops):
            if i == 0:
                continue

            parent_hash = op.get('parent_hash')
            expected_hash = ops[i - 1].get('hash_sha256')

            if parent_hash != expected_hash:
                print(f"🔴 同步後鏈斷裂在操作 {i}: {op['operation_id']}")
                return False

        print(f"✅ 同步後完整性驗證通過 ({len(ops)} 條記錄)")
        return True

    def get_sync_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """獲取同步歷史"""

        if not self.sync_log_file.exists():
            return []

        history = []
        with open(self.sync_log_file, 'r', encoding='utf-8') as f:
            for line in f:
                history.append(json.loads(line))

        return history[-limit:]

    def rollback_to_backup(self, backup_file: str) -> bool:
        """回滾到指定備份"""

        backup_path = Path(backup_file)

        if not backup_path.exists():
            print(f"🔴 備份不存在: {backup_file}")
            return False

        try:
            shutil.copy2(backup_path, self.ledger_file)
            print(f"✅ 已回滾到備份: {backup_file}")
            return True
        except Exception as e:
            print(f"🔴 回滾失敗: {e}")
            return False


# CLI示例
if __name__ == "__main__":
    engine = SyncEngine()

    print("🔄 本地同步引擎 CLI")
    print("=" * 50)

    # 示例1: 讀取本地日記
    print("\n1️⃣ 讀取本地日記:")
    local_ops = engine.read_ledger()
    print(f"   找到 {len(local_ops)} 條本地操作")

    # 示例2: 模擬衝突檢測
    print("\n2️⃣ 衝突檢測 (模擬):")
    sample_remote = [
        {
            "operation_id": "OP-20260530-051000-abc111",
            "timestamp": "2026-05-30T05:10:00+08:00",
            "hash_sha256": "different_hash",
            "operation_name": "test-op-1"
        },
        {
            "operation_id": "OP-20260530-052000-abc222",
            "timestamp": "2026-05-30T05:20:00+08:00",
            "hash_sha256": "hash_abc222",
            "operation_name": "test-op-2"
        }
    ]

    if len(local_ops) >= 2:
        conflicts = engine.detect_conflicts(local_ops[:2], sample_remote)
        print(f"   檢測到 {len(conflicts)} 個衝突")
        for conflict in conflicts:
            print(f"     - {conflict.conflict_type}: {conflict.affected_op_id}")

    # 示例3: 合併策略
    print("\n3️⃣ 合併策略演示:")
    if local_ops and sample_remote:
        merged = engine.merge_operations(local_ops[:2], sample_remote, strategy="merge")
        print(f"   合併後: {len(merged)} 條操作")

    # 示例4: 同步歷史
    print("\n4️⃣ 同步歷史:")
    history = engine.get_sync_history(limit=3)
    for sync in history:
        print(f"   {sync['timestamp']}: {sync['status']}")

    # 示例5: 完整性驗證
    print("\n5️⃣ 完整性驗證:")
    is_valid = engine.verify_sync_integrity()
    print(f"   {'✅ 通過' if is_valid else '🔴 失敗'}")

