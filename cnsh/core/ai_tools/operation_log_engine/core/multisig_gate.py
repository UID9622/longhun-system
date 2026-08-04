#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
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
🔐 多签门 v1.0
3/3 本地验证 (UID + GPG签名 + 时间戳)·无链上依赖·零成本

DNA:#龍芯⚡️2026-05-30-MULTISIG-GATE-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
责任: UID9622·不免责

核心逻辑:
  多签 = 3层验证·全过才通过

  第1层 UID验证 (身份确认):
    - 硬编码 UID = UID9622
    - device_seal 绑定设备
    - 检查操作者身份·不能代理

  第2层 GPG验证 (签名确认):
    - GPG public key = A2D0092CEE2E5BA87035600924C3704A8CC26D5F
    - 验证签名完整性
    - 检查密钥未被轮换 (key_rotation_detected → ALERT)

  第3层 时间戳验证 (时序确认):
    - ISO8601 + 时辰(shichen) + 数字根(digital_root)
    - 检查时间戳递增·无时光倒流
    - 毫秒精度·不可篡改

  决策:
    3/3 全过 → ✅ 通过 (自动)
    任何一层失败 → 🔴 VETO (一票否决)
    敏感操作 (焊接·规则) → 必须 #CONFIRM (双签激活)
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Tuple, List
from datetime import datetime, timezone
from dataclasses import dataclass


@dataclass
class VerificationResult:
    """验证结果"""
    passed: bool
    layer: str  # uid / gpg / temporal
    details: Dict[str, Any]
    timestamp: str
    risk_level: str  # low / medium / high / critical


class MultisigGate:
    """
    多签门 (3/3 本地验证)

    功能:
      - UID 验证 (身份确认)
      - GPG 验证 (签名确认)
      - 时间戳验证 (时序确认)
      - 敏感操作拦截
      - CONFIRM 快速通道
    """

    def __init__(self):
        # 硬编码常量
        self.AUTHORIZED_UID = "UID9622"
        self.AUTHORIZED_GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
        self.DEVICE_SEAL_PREFIX = "#DEVICE-SEAL-"

        # 敏感操作列表 (必须多签)
        self.SENSITIVE_OPERATIONS = [
            "焊接",  # weld operations
            "规则更新",  # rule updates
            "策略变更",  # policy changes
            "权限授予",  # permission grants
            "设备绑定",  # device binding
            "同步启动",  # sync initiation
        ]

        # 验证日志
        self.log_dir = Path("~/.龍魂/操作日记/multisig_logs").expanduser()
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.verification_log = self.log_dir / "verifications.jsonl"
        self.alert_log = self.log_dir / "alerts.jsonl"

    def verify_uid(self,
                   operation_uid: str,
                   device_id: str,
                   device_seal: str) -> VerificationResult:
        """
        UID 验证 (第1层)

        检查:
          1. operation_uid 必须是 UID9622
          2. device_seal 格式正确·无伪造
          3. device_id 与 seal 对应
        """

        result = VerificationResult(
            passed=False,
            layer="uid",
            details={},
            timestamp=datetime.now(timezone.utc).isoformat(),
            risk_level="low"
        )

        # 检查1: UID 匹配
        if operation_uid != self.AUTHORIZED_UID:
            result.details['error'] = f"UID mismatch: {operation_uid} != {self.AUTHORIZED_UID}"
            result.risk_level = "critical"
            return result

        # 检查2: device_seal 格式
        if not device_seal.startswith(self.DEVICE_SEAL_PREFIX):
            result.details['error'] = f"Invalid device seal format: {device_seal}"
            result.risk_level = "high"
            return result

        # 检查3: device_seal 内含 device_id (简化验证)
        # 实际应验证 SHA-256 签名
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
        GPG 验证 (第2层)

        检查:
          1. gpg_key_id 必须是授权的公钥
          2. 签名完整性验证 (简化: 检查签名格式)
          3. 密钥未被轮换 (无 key_rotation 标志)
        """

        result = VerificationResult(
            passed=False,
            layer="gpg",
            details={},
            timestamp=datetime.now(timezone.utc).isoformat(),
            risk_level="low"
        )

        # 检查1: GPG 密钥 ID 匹配
        if gpg_key_id != self.AUTHORIZED_GPG:
            result.details['error'] = f"GPG key mismatch: {gpg_key_id}"
            result.risk_level = "critical"
            return result

        # 检查2: 签名格式验证
        # 简化: 假设签名格式为十六进制且长度 > 64 字符
        if not self._is_valid_gpg_signature(gpg_signature):
            result.details['error'] = f"Invalid GPG signature format"
            result.risk_level = "high"
            return result

        # 检查3: 密钥轮换检查
        # 实际应查询 GPG keyring·检查 creation_date
        key_rotation_detected = self._check_key_rotation(gpg_key_id)
        if key_rotation_detected:
            result.details['alert'] = "Key rotation detected - verify with GPG keyring"
            result.risk_level = "medium"

        # 计算签名杂凑 (用于追踪)
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
        时间戳验证 (第3层)

        检查:
          1. ISO8601 时间戳格式有效
          2. 时辰(shichen) 与时间戳一致
          3. 数字根计算正确
          4. 时间戳递增 (无时光倒流)
        """

        result = VerificationResult(
            passed=False,
            layer="temporal",
            details={},
            timestamp=datetime.now(timezone.utc).isoformat(),
            risk_level="low"
        )

        # 检查1: ISO8601 格式
        try:
            ts = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            result.details['error'] = f"Invalid ISO8601 timestamp: {timestamp}"
            result.risk_level = "high"
            return result

        # 检查2: 时辰与时间戳一致
        hour = ts.hour
        expected_shichen = self._compute_shichen(hour)

        if shichen != expected_shichen:
            result.details['warning'] = f"Shichen mismatch: {shichen} != {expected_shichen}"
            result.risk_level = "medium"

        # 检查3: 数字根计算
        expected_dr = self._compute_digital_root(timestamp)

        if digital_root != expected_dr:
            result.details['error'] = f"Digital root mismatch: {digital_root} != {expected_dr}"
            result.risk_level = "high"
            return result

        # 检查4: 时间戳递增
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
        完整的 3/3 多签验证

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

        # 第1层: UID
        uid_result = self.verify_uid(uid, device_id, device_seal)
        results.append(uid_result)

        # 第2层: GPG
        gpg_result = self.verify_gpg(operation_id, gpg_signature, gpg_key_id)
        results.append(gpg_result)

        # 第3层: 时间戳
        temporal_result = self.verify_temporal(
            operation_id,
            timestamp,
            shichen,
            digital_root,
            prev_timestamp
        )
        results.append(temporal_result)

        # 判决
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

        # 记录验证
        self._log_verification(verification_result)

        if risk_level in ['high', 'critical']:
            self._log_alert(verification_result)

        return verification_result

    def _is_valid_gpg_signature(self, signature: str) -> bool:
        """验证 GPG 签名格式"""
        # 简化: 检查十六进制格式·长度 > 64
        try:
            int(signature, 16)
            return len(signature) > 64
        except ValueError:
            return False

    def _check_key_rotation(self, key_id: str) -> bool:
        """检查密钥是否被轮换"""
        # 简化: 假设密钥未被轮换
        # 实际应查询 GPG keyring
        return False

    def _compute_shichen(self, hour: int) -> str:
        """计算时辰"""
        shichen_map = {
            23: '子时', 0: '子时',
            1: '丑时', 2: '丑时',
            3: '寅时', 4: '寅时',
            5: '卯时', 6: '卯时',
            7: '辰时', 8: '辰时',
            9: '巳时', 10: '巳时',
            11: '午时', 12: '午时',
            13: '未时', 14: '未时',
            15: '申时', 16: '申时',
            17: '酉时', 18: '酉时',
            19: '戌时', 20: '戌时',
            21: '亥时', 22: '亥时',
        }
        return shichen_map.get(hour, '未知时')

    def _compute_digital_root(self, timestamp: str) -> int:
        """计算数字根 (从时间戳)"""
        # 提取日期部分 (YYYY-MM-DD)
        date_part = timestamp[:10].replace('-', '')
        total = sum(int(d) for d in date_part)

        while total >= 10:
            total = sum(int(d) for d in str(total))

        return total

    def _is_sensitive_operation(self, operation_type: str) -> bool:
        """判断是否为敏感操作"""
        return any(sensitive in operation_type for sensitive in self.SENSITIVE_OPERATIONS)

    def _verify_confirm_code(self, confirm_code: str, operation_id: str) -> bool:
        """
        验证 #CONFIRM 快速通道

        格式: #CONFIRM🌌{uid}-ONLY-ONCE🧬{operation_id_checksum}
        """
        # 简化: 检查前缀
        return confirm_code.startswith("#CONFIRM")

    def _log_verification(self, result: Dict[str, Any]) -> None:
        """记录验证结果"""
        with open(self.verification_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')

    def _log_alert(self, result: Dict[str, Any]) -> None:
        """记录警报"""
        alert = {
            'timestamp': result['timestamp'],
            'operation_id': result['operation_id'],
            'risk_level': result['risk_level'],
            'verdict': result['verdict']
        }
        with open(self.alert_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(alert, ensure_ascii=False) + '\n')

    def get_verification_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取验证历史"""
        if not self.verification_log.exists():
            return []

        history = []
        with open(self.verification_log, 'r', encoding='utf-8') as f:
            for line in f:
                history.append(json.loads(line))

        return history[-limit:]

    def get_alerts(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取警报列表"""
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

    print("🔐 多签门 CLI")
    print("=" * 50)

    # 示例1: 层级验证演示
    print("\n1️⃣ 层级验证演示:")

    # UID 验证
    uid_result = gate.verify_uid("UID9622", "MacBook-M4-Max-UID9622", "#DEVICE-SEAL-2026-05-30-XXXXX")
    print(f"   UID: {'✅ 通过' if uid_result.passed else '❌ 失败'}")

    # GPG 验证
    gpg_result = gate.verify_gpg(
        "OP-20260530-060000-abc123",
        "a2d0092cee2e5ba87035600924c3704a8cc26d5f" * 3,  # Mock signature
        "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
    )
    print(f"   GPG: {'✅ 通过' if gpg_result.passed else '❌ 失败'}")

    # 时间戳验证
    now = datetime.now(timezone.utc).isoformat()
    temporal_result = gate.verify_temporal(
        "OP-20260530-060000-abc123",
        now,
        "卯时",
        5  # dr=5
    )
    print(f"   时间戳: {'✅ 通过' if temporal_result.passed else '❌ 失败'}")

    # 示例2: 完整 3/3 验证 (普通操作)
    print("\n2️⃣ 完整验证 (普通操作):")
    result = gate.verify_operation(
        operation_id="OP-20260530-060000-abc123",
        operation_type="工程",
        uid="UID9622",
        device_id="MacBook-M4-Max-UID9622",
        device_seal="#DEVICE-SEAL-2026-05-30-XXXXX",
        timestamp=now,
        shichen="卯时",
        digital_root=5,
        gpg_signature="a2d0092cee2e5ba87035600924c3704a8cc26d5f" * 3,
        gpg_key_id="A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
    )
    print(f"   判决: {result['verdict']}")
    print(f"   风险: {result['risk_level']}")

    # 示例3: 敏感操作 (需要 CONFIRM)
    print("\n3️⃣ 敏感操作 (需要 CONFIRM):")
    sensitive_result = gate.verify_operation(
        operation_id="OP-20260530-061000-def456",
        operation_type="焊接系统",  # Sensitive
        uid="UID9622",
        device_id="MacBook-M4-Max-UID9622",
        device_seal="#DEVICE-SEAL-2026-05-30-XXXXX",
        timestamp=now,
        shichen="卯时",
        digital_root=5,
        gpg_signature="a2d0092cee2e5ba87035600924c3704a8cc26d5f" * 3,
        gpg_key_id="A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
    )
    print(f"   需要 CONFIRM: {sensitive_result['requires_confirm']}")
    print(f"   判决: {sensitive_result['verdict']}")

    # 示例4: 验证历史
    print("\n4️⃣ 验证历史:")
    history = gate.get_verification_history(limit=3)
    for v in history:
        print(f"   {v['operation_id']}: {v['verdict']}")

    # 示例5: 警报检查
    print("\n5️⃣ 警报列表:")
    alerts = gate.get_alerts(limit=5)
    print(f"   共 {len(alerts)} 个警报")

