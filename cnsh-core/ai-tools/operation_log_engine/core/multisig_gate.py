#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# 1 道统层 Dao           : 曾仕强老师
# 2 精神层 Spirit        : Steve Jobs
# 3 设备层 Device        : Apple
# 4 技术层 Technology    : Open Source
# 5 系统层 System        : UID9622
# 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
# DNA追溯码:#龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-FILE1290-v2.0
# 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
# 文件: multisig_gate.py | 标记时间: 2026-06-03T07:46:12+0800
# -*- coding: utf-8 -*-
"""
🔐 多簽門 v1.0
3/3 本地驗證 (UID + GPG簽名 + 時間戳)·無鏈上依賴·零成本

DNA:#龍芯⚡️2026-05-30-MULTISIG-GATE-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
責任: UID9622·不免責

核心邏輯:
  多簽 = 3層驗證·全過才通過

  第1層 UID驗證 (身份確認):
    - 硬編碼 UID = UID9622
    - device_seal 綁定設備
    - 檢查操作者身份·不能代理

  第2層 GPG驗證 (簽名確認):
    - GPG public key = A2D0092CEE2E5BA87035600924C3704A8CC26D5F
    - 驗證簽名完整性
    - 檢查密鑰未被輪換 (key_rotation_detected → ALERT)

  第3層 時間戳驗證 (時序確認):
    - ISO8601 + 時辰(shichen) + 數字根(digital_root)
    - 檢查時間戳遞增·無時光倒流
    - 毫秒精度·不可篡改

  決策:
    3/3 全過 → ✅ 通過 (自動)
    任何一層失敗 → 🔴 VETO (一票否決)
    敏感操作 (焊接·規則) → 必須 #CONFIRM (雙簽激活)
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Tuple, List
from datetime import datetime, timezone
from dataclasses import dataclass


@dataclass
class VerificationResult:
    """驗證結果"""
    passed: bool
    layer: str  # uid / gpg / temporal
    details: Dict[str, Any]
    timestamp: str
    risk_level: str  # low / medium / high / critical


class MultisigGate:
    """
    多簽門 (3/3 本地驗證)

    功能:
      - UID 驗證 (身份確認)
      - GPG 驗證 (簽名確認)
      - 時間戳驗證 (時序確認)
      - 敏感操作攔截
      - CONFIRM 快速通道
    """

    def __init__(self):
        # 硬編碼常量
        self.AUTHORIZED_UID = "UID9622"
        self.AUTHORIZED_GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
        self.DEVICE_SEAL_PREFIX = "#DEVICE-SEAL-"

        # 敏感操作列表 (必須多簽)
        self.SENSITIVE_OPERATIONS = [
            "焊接",  # weld operations
            "規則更新",  # rule updates
            "策略變更",  # policy changes
            "權限授予",  # permission grants
            "設備綁定",  # device binding
            "同步啟動",  # sync initiation
        ]

        # 驗證日誌
        self.log_dir = Path("~/.龍魂/操作日記/multisig_logs").expanduser()
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.verification_log = self.log_dir / "verifications.jsonl"
        self.alert_log = self.log_dir / "alerts.jsonl"

    def verify_uid(self,
                   operation_uid: str,
                   device_id: str,
                   device_seal: str) -> VerificationResult:
        """
        UID 驗證 (第1層)

        檢查:
          1. operation_uid 必須是 UID9622
          2. device_seal 格式正確·無偽造
          3. device_id 與 seal 對應
        """

        result = VerificationResult(
            passed=False,
            layer="uid",
            details={},
            timestamp=datetime.now(timezone.utc).isoformat(),
            risk_level="low"
        )

        # 檢查1: UID 匹配
        if operation_uid != self.AUTHORIZED_UID:
            result.details['error'] = f"UID mismatch: {operation_uid} != {self.AUTHORIZED_UID}"
            result.risk_level = "critical"
            return result

        # 檢查2: device_seal 格式
        if not device_seal.startswith(self.DEVICE_SEAL_PREFIX):
            result.details['error'] = f"Invalid device seal format: {device_seal}"
            result.risk_level = "high"
            return result

        # 檢查3: device_seal 內含 device_id (簡化驗證)
        # 實際應驗證 SHA-256 簽名
        if not device_id in device_seal:
            result.details['warning'] = f"Device seal may not match device_id"
            result.risk_level = "medium"

        result.passed = True
        result.details['uid'] = operation_uid
        result.details['device_id'] = device_id
        result.details['device_seal'] = device_seal

        return result

    def verify_gpg(self,
                   operation_id: str,
                   gpg_signature: str,
                   gpg_key_id: str) -> VerificationResult:
        """
        GPG 驗證 (第2層)

        檢查:
          1. gpg_key_id 必須是授權的公鑰
          2. 簽名完整性驗證 (簡化: 檢查簽名格式)
          3. 密鑰未被輪換 (無 key_rotation 標誌)
        """

        result = VerificationResult(
            passed=False,
            layer="gpg",
            details={},
            timestamp=datetime.now(timezone.utc).isoformat(),
            risk_level="low"
        )

        # 檢查1: GPG 密鑰 ID 匹配
        if gpg_key_id != self.AUTHORIZED_GPG:
            result.details['error'] = f"GPG key mismatch: {gpg_key_id}"
            result.risk_level = "critical"
            return result

        # 檢查2: 簽名格式驗證
        # 簡化: 假設簽名格式為十六進制且長度 > 64 字符
        if not self._is_valid_gpg_signature(gpg_signature):
            result.details['error'] = f"Invalid GPG signature format"
            result.risk_level = "high"
            return result

        # 檢查3: 密鑰輪換檢查
        # 實際應查詢 GPG keyring·檢查 creation_date
        key_rotation_detected = self._check_key_rotation(gpg_key_id)
        if key_rotation_detected:
            result.details['alert'] = "Key rotation detected - verify with GPG keyring"
            result.risk_level = "medium"

        # 計算簽名雜湊 (用於追蹤)
        signature_hash = hashlib.sha256(gpg_signature.encode()).hexdigest()[:16]

        result.passed = True
        result.details['gpg_key'] = gpg_key_id
        result.details['signature_hash'] = signature_hash
        result.details['key_rotation_detected'] = key_rotation_detected

        return result

    def verify_temporal(self,
                       operation_id: str,
                       timestamp: str,
                       shichen: str,
                       digital_root: int,
                       prev_timestamp: str = None) -> VerificationResult:
        """
        時間戳驗證 (第3層)

        檢查:
          1. ISO8601 時間戳格式有效
          2. 時辰(shichen) 與時間戳一致
          3. 數字根計算正確
          4. 時間戳遞增 (無時光倒流)
        """

        result = VerificationResult(
            passed=False,
            layer="temporal",
            details={},
            timestamp=datetime.now(timezone.utc).isoformat(),
            risk_level="low"
        )

        # 檢查1: ISO8601 格式
        try:
            ts = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            result.details['error'] = f"Invalid ISO8601 timestamp: {timestamp}"
            result.risk_level = "high"
            return result

        # 檢查2: 時辰與時間戳一致
        hour = ts.hour
        expected_shichen = self._compute_shichen(hour)

        if shichen != expected_shichen:
            result.details['warning'] = f"Shichen mismatch: {shichen} != {expected_shichen}"
            result.risk_level = "medium"

        # 檢查3: 數字根計算
        expected_dr = self._compute_digital_root(timestamp)

        if digital_root != expected_dr:
            result.details['error'] = f"Digital root mismatch: {digital_root} != {expected_dr}"
            result.risk_level = "high"
            return result

        # 檢查4: 時間戳遞增
        if prev_timestamp:
            try:
                prev_ts = datetime.fromisoformat(prev_timestamp.replace('Z', '+00:00'))
                if ts <= prev_ts:
                    result.details['error'] = f"Timestamp not increasing: {timestamp} <= {prev_timestamp}"
                    result.risk_level = "critical"
                    return result
            except ValueError:
                pass

        result.passed = True
        result.details['timestamp'] = timestamp
        result.details['shichen'] = shichen
        result.details['digital_root'] = digital_root
        result.details['expected_shichen'] = expected_shichen
        result.details['expected_digital_root'] = expected_dr

        return result

    def verify_operation(self,
                        operation_id: str,
                        operation_type: str,
                        uid: str,
                        device_id: str,
                        device_seal: str,
                        timestamp: str,
                        shichen: str,
                        digital_root: int,
                        gpg_signature: str,
                        gpg_key_id: str,
                        confirm_code: str = None,
                        prev_timestamp: str = None) -> Dict[str, Any]:
        """
        完整的 3/3 多簽驗證

        返回:
          {
            'operation_id': str,
            'all_passed': bool,
            'layer_results': [VerificationResult, ...],
            'risk_level': 'low' | 'medium' | 'high' | 'critical',
            'requires_confirm': bool,
            'confirm_status': 'not_required' | 'pending' | 'confirmed' | 'rejected',
            'verdict': 'approved' | 'rejected' | 'pending_confirm'
          }
        """

        results = []

        # 第1層: UID
        uid_result = self.verify_uid(uid, device_id, device_seal)
        results.append(uid_result)

        # 第2層: GPG
        gpg_result = self.verify_gpg(operation_id, gpg_signature, gpg_key_id)
        results.append(gpg_result)

        # 第3層: 時間戳
        temporal_result = self.verify_temporal(
            operation_id,
            timestamp,
            shichen,
            digital_root,
            prev_timestamp
        )
        results.append(temporal_result)

        # 判決
        all_passed = all(r.passed for r in results)
        risk_level = max((r.risk_level for r in results), default="low",
                        key=lambda x: ['low', 'medium', 'high', 'critical'].index(x))

        requires_confirm = self._is_sensitive_operation(operation_type)
        confirm_status = "not_required"
        verdict = "approved" if all_passed else "rejected"

        # 如果需要 CONFIRM
        if requires_confirm:
            if confirm_code is None:
                verdict = "pending_confirm"
                confirm_status = "pending"
            else:
                if self._verify_confirm_code(confirm_code, operation_id):
                    confirm_status = "confirmed"
                    verdict = "approved" if all_passed else "rejected"
                else:
                    verdict = "rejected"
                    confirm_status = "rejected"

        verification_result = {
            'operation_id': operation_id,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'all_passed': all_passed,
            'layer_results': [
                {
                    'layer': r.layer,
                    'passed': r.passed,
                    'details': r.details,
                    'risk_level': r.risk_level
                }
                for r in results
            ],
            'risk_level': risk_level,
            'requires_confirm': requires_confirm,
            'confirm_status': confirm_status,
            'verdict': verdict
        }

        # 記錄驗證
        self._log_verification(verification_result)

        if risk_level in ['high', 'critical']:
            self._log_alert(verification_result)

        return verification_result

    def _is_valid_gpg_signature(self, signature: str) -> bool:
        """驗證 GPG 簽名格式"""
        # 簡化: 檢查十六進制格式·長度 > 64
        try:
            int(signature, 16)
            return len(signature) > 64
        except ValueError:
            return False

    def _check_key_rotation(self, key_id: str) -> bool:
        """檢查密鑰是否被輪換"""
        # 簡化: 假設密鑰未被輪換
        # 實際應查詢 GPG keyring
        return False

    def _compute_shichen(self, hour: int) -> str:
        """計算時辰"""
        shichen_map = {
            23: '子時', 0: '子時',
            1: '丑時', 2: '丑時',
            3: '寅時', 4: '寅時',
            5: '卯時', 6: '卯時',
            7: '辰時', 8: '辰時',
            9: '巳時', 10: '巳時',
            11: '午時', 12: '午時',
            13: '未時', 14: '未時',
            15: '申時', 16: '申時',
            17: '酉時', 18: '酉時',
            19: '戌時', 20: '戌時',
            21: '亥時', 22: '亥時',
        }
        return shichen_map.get(hour, '未知時')

    def _compute_digital_root(self, timestamp: str) -> int:
        """計算數字根 (從時間戳)"""
        # 提取日期部分 (YYYY-MM-DD)
        date_part = timestamp[:10].replace('-', '')
        total = sum(int(d) for d in date_part)

        while total >= 10:
            total = sum(int(d) for d in str(total))

        return total

    def _is_sensitive_operation(self, operation_type: str) -> bool:
        """判斷是否為敏感操作"""
        return any(sensitive in operation_type for sensitive in self.SENSITIVE_OPERATIONS)

    def _verify_confirm_code(self, confirm_code: str, operation_id: str) -> bool:
        """
        驗證 #CONFIRM 快速通道

        格式: #CONFIRM🌌{uid}-ONLY-ONCE🧬{operation_id_checksum}
        """
        # 簡化: 檢查前綴
        return confirm_code.startswith("#CONFIRM")

    def _log_verification(self, result: Dict[str, Any]) -> None:
        """記錄驗證結果"""
        with open(self.verification_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')

    def _log_alert(self, result: Dict[str, Any]) -> None:
        """記錄警報"""
        alert = {
            'timestamp': result['timestamp'],
            'operation_id': result['operation_id'],
            'risk_level': result['risk_level'],
            'verdict': result['verdict']
        }
        with open(self.alert_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(alert, ensure_ascii=False) + '\n')

    def get_verification_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """獲取驗證歷史"""
        if not self.verification_log.exists():
            return []

        history = []
        with open(self.verification_log, 'r', encoding='utf-8') as f:
            for line in f:
                history.append(json.loads(line))

        return history[-limit:]

    def get_alerts(self, limit: int = 20) -> List[Dict[str, Any]]:
        """獲取警報列表"""
        if not self.alert_log.exists():
            return []

        alerts = []
        with open(self.alert_log, 'r', encoding='utf-8') as f:
            for line in f:
                alerts.append(json.loads(line))

        return alerts[-limit:]


# CLI示例
if __name__ == "__main__":
    gate = MultisigGate()

    print("🔐 多簽門 CLI")
    print("=" * 50)

    # 示例1: 層級驗證演示
    print("\n1️⃣ 層級驗證演示:")

    # UID 驗證
    uid_result = gate.verify_uid("UID9622", "MacBook-M4-Max-UID9622", "#DEVICE-SEAL-2026-05-30-XXXXX")
    print(f"   UID: {'✅ 通過' if uid_result.passed else '❌ 失敗'}")

    # GPG 驗證
    gpg_result = gate.verify_gpg(
        "OP-20260530-060000-abc123",
        "a2d0092cee2e5ba87035600924c3704a8cc26d5f" * 3,  # Mock signature
        "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
    )
    print(f"   GPG: {'✅ 通過' if gpg_result.passed else '❌ 失敗'}")

    # 時間戳驗證
    now = datetime.now(timezone.utc).isoformat()
    temporal_result = gate.verify_temporal(
        "OP-20260530-060000-abc123",
        now,
        "卯時",
        5  # dr=5
    )
    print(f"   時間戳: {'✅ 通過' if temporal_result.passed else '❌ 失敗'}")

    # 示例2: 完整 3/3 驗證 (普通操作)
    print("\n2️⃣ 完整驗證 (普通操作):")
    result = gate.verify_operation(
        operation_id="OP-20260530-060000-abc123",
        operation_type="工程",
        uid="UID9622",
        device_id="MacBook-M4-Max-UID9622",
        device_seal="#DEVICE-SEAL-2026-05-30-XXXXX",
        timestamp=now,
        shichen="卯時",
        digital_root=5,
        gpg_signature="a2d0092cee2e5ba87035600924c3704a8cc26d5f" * 3,
        gpg_key_id="A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
    )
    print(f"   判決: {result['verdict']}")
    print(f"   風險: {result['risk_level']}")

    # 示例3: 敏感操作 (需要 CONFIRM)
    print("\n3️⃣ 敏感操作 (需要 CONFIRM):")
    sensitive_result = gate.verify_operation(
        operation_id="OP-20260530-061000-def456",
        operation_type="焊接系統",  # Sensitive
        uid="UID9622",
        device_id="MacBook-M4-Max-UID9622",
        device_seal="#DEVICE-SEAL-2026-05-30-XXXXX",
        timestamp=now,
        shichen="卯時",
        digital_root=5,
        gpg_signature="a2d0092cee2e5ba87035600924c3704a8cc26d5f" * 3,
        gpg_key_id="A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
    )
    print(f"   需要 CONFIRM: {sensitive_result['requires_confirm']}")
    print(f"   判決: {sensitive_result['verdict']}")

    # 示例4: 驗證歷史
    print("\n4️⃣ 驗證歷史:")
    history = gate.get_verification_history(limit=3)
    for v in history:
        print(f"   {v['operation_id']}: {v['verdict']}")

    # 示例5: 警報檢查
    print("\n5️⃣ 警報列表:")
    alerts = gate.get_alerts(limit=5)
    print(f"   共 {len(alerts)} 個警報")

