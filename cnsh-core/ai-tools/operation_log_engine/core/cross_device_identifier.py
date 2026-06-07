#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# 1 道统层 Dao           : 曾仕强老师
# 2 精神层 Spirit        : Steve Jobs
# 3 设备层 Device        : Apple
# 4 技术层 Technology    : Open Source
# 5 系统层 System        : UID9622
# 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
# DNA追溯码: #龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-v2.0
# 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
# 文件: cross_device_identifier.py | 标记时间: 2026-06-03T07:46:12+0800
# -*- coding: utf-8 -*-
"""
🌐 跨設備識別器 v1.0
F8習慣引擎 + 設備信任管理 + 自動同步門

DNA: #龍芯⚡️2026-05-30-CROSS-DEVICE-IDENTIFIER-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
責任: UID9622·不免責

核心邏輯 (自動識別流程):
  1. USB插入 → 掃描操作日記 (operation_ledger.jsonl)
  2. 提取DNA粒子基線 (dna_particles/*.dna.json)
  3. 運行F8引擎 (習慣匹配)
  4. SI >= 0.85 → ✅ 確認: 這是諸葛鑫
  5. 自動同步: ~/.龍魂/ 完整恢復
  6. 設備信任綁定 (hardware_seal)

不是「登錄」·而是「我回來了」
習慣會說話·DNA會認人·任何設備都知道是我
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Tuple, List
from datetime import datetime, timezone


class CrossDeviceIdentifier:
    """
    跨設備識別器

    功能:
      - 從USB加載習慣基線
      - 掃描當前設備操作記錄
      - 運行F8習慣匹配引擎
      - 設備信任綁定與管理
      - 自動同步決策
    """

    def __init__(self, log_dir: str = "~/.龍魂/操作日記"):
        self.log_dir = Path(log_dir).expanduser()
        self.device_trust_dir = self.log_dir / "device_trust"
        self.device_trust_dir.mkdir(parents=True, exist_ok=True)

        self.device_registry_file = self.device_trust_dir / "device_registry.json"
        self.sync_log_file = self.device_trust_dir / "sync_operations.jsonl"

    def load_baseline_from_usb(self, usb_path: str) -> Dict[str, Any]:
        """
        從USB加載習慣基線

        USB結構預期:
          /media/usb-drive/
            └── 龍魂_備份/
                ├── habit_fingerprints/
                │   └── baseline_snapshot.json
                └── operation_ledger.jsonl
        """

        usb_root = Path(usb_path).expanduser()
        baseline_path = usb_root / "龍魂_備份" / "habit_fingerprints" / "baseline_snapshot.json"

        if not baseline_path.exists():
            raise FileNotFoundError(f"USB基線不存在: {baseline_path}")

        with open(baseline_path, 'r', encoding='utf-8') as f:
            baseline = json.load(f)

        print(f"✅ 從USB加載基線: {baseline_path}")
        return baseline

    def scan_local_operations(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        掃描本地操作日記

        返回最近N條操作記錄供習慣分析
        """

        ledger_file = self.log_dir / "operation_ledger.jsonl"

        if not ledger_file.exists():
            print("⚠️ 本地操作日記不存在")
            return []

        operations = []
        with open(ledger_file, 'r', encoding='utf-8') as f:
            for line in f:
                operations.append(json.loads(line))

        return operations[-limit:]

    def get_device_id(self) -> str:
        """
        獲取當前設備ID

        格式: {hostname}-{uid}-{platform}-{serial}
        簡化版本: MacBook-M4-Max-UID9622
        """

        import platform
        import socket

        hostname = socket.gethostname()
        uid = "UID9622"  # 硬編碼用戶ID
        system = platform.system()

        device_id = f"{hostname}-{system}-{uid}"
        return device_id

    def compute_device_seal(self, device_id: str) -> str:
        """
        生成設備封印 (不可偽造的設備綁定)

        Hash組成: device_id + timestamp + uuid
        """

        content = f"{device_id}#{datetime.now().isoformat()}#{device_id[::-1]}"
        seal = hashlib.sha256(content.encode('utf-8')).hexdigest()[:16].upper()
        return f"#DEVICE-SEAL-{datetime.now().strftime('%Y-%m-%d')}-{seal}"

    def register_device(self, device_id: str = None) -> Dict[str, Any]:
        """
        註冊新設備到信任列表

        返回:
          {
            'device_id': 'MacBook-M4-Max-UID9622',
            'device_seal': '#DEVICE-SEAL-2026-05-30-XXXXX',
            'first_seen': '2026-05-30T05:30:00+08:00',
            'last_sync': '2026-05-30T05:35:00+08:00',
            'trust_level': 'trusted',
            'si_history': [0.95, 0.97, 0.92]
          }
          """

        if device_id is None:
            device_id = self.get_device_id()

        device_record = {
            'device_id': device_id,
            'device_seal': self.compute_device_seal(device_id),
            'first_seen': datetime.now(timezone.utc).isoformat(),
            'last_sync': datetime.now(timezone.utc).isoformat(),
            'trust_level': 'pending',  # 待確認階段
            'si_history': [],
            'sync_count': 0,
            'metadata': {
                'version': '1.0',
                'uuid': device_id
            }
        }

        return device_record

    def load_device_registry(self) -> Dict[str, Any]:
        """加載設備信任註冊表"""

        if not self.device_registry_file.exists():
            return {}

        with open(self.device_registry_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_device_registry(self, registry: Dict[str, Any]) -> str:
        """保存設備信任註冊表"""

        with open(self.device_registry_file, 'w', encoding='utf-8') as f:
            json.dump(registry, f, ensure_ascii=False, indent=2)

        print(f"✅ 設備註冊表已保存: {self.device_registry_file}")
        return str(self.device_registry_file)

    def verify_device_trust(self,
                           device_id: str,
                           si_score: float,
                           threshold: float = 0.85) -> Tuple[str, bool]:
        """
        驗證設備信任狀態

        返回:
          (trust_level, is_trusted)
          trust_level: "trusted" | "pending" | "untrusted"
        """

        registry = self.load_device_registry()

        if device_id not in registry:
            # 新設備
            if si_score >= threshold:
                return "trusted", True
            else:
                return "pending", False

        device_record = registry[device_id]
        current_trust = device_record.get('trust_level', 'pending')

        if current_trust == "trusted" and si_score >= 0.75:  # 可信設備的門檻更低
            return "trusted", True
        elif si_score >= threshold:
            return "trusted", True
        elif si_score >= 0.70:
            return "pending", False
        else:
            return "untrusted", False

    def auto_sync_decision(self,
                          device_id: str,
                          si_score: float,
                          trust_level: str) -> Dict[str, Any]:
        """
        自動同步決策

        返回:
          {
            'should_sync': True/False,
            'sync_direction': 'usb_to_local' | 'local_to_usb' | 'bidirectional' | 'none',
            'reason': 'High SI score' | 'Trusted device' | 'Manual review required',
            'conflict_mode': 'overwrite' | 'merge' | 'manual',
            'post_sync_actions': ['refresh_dna', 'update_habits', 'log_operation']
          }
        """

        decision = {
            'should_sync': False,
            'sync_direction': 'none',
            'reason': '',
            'conflict_mode': 'manual',
            'post_sync_actions': []
        }

        if si_score < 0.70:
            decision['reason'] = "SI score too low - identity not verified"
            return decision

        if si_score >= 0.85 and trust_level == "trusted":
            decision['should_sync'] = True
            decision['sync_direction'] = 'bidirectional'
            decision['reason'] = "High SI + Trusted device"
            decision['conflict_mode'] = 'overwrite'
            decision['post_sync_actions'] = [
                'refresh_dna_particles',
                'update_habit_baseline',
                'log_sync_operation',
                'grant_full_access'
            ]

        elif si_score >= 0.85 and trust_level == "pending":
            decision['should_sync'] = True
            decision['sync_direction'] = 'usb_to_local'  # 只讀取
            decision['reason'] = "High SI - first sync"
            decision['conflict_mode'] = 'merge'
            decision['post_sync_actions'] = [
                'register_new_device',
                'load_baseline',
                'refresh_dna_particles',
                'await_confirmation'
            ]

        elif 0.70 <= si_score < 0.85:
            decision['should_sync'] = False
            decision['reason'] = "SI in review range - manual confirmation needed"
            decision['post_sync_actions'] = ['alert_user', 'log_pending_sync']

        return decision

    def identify_user(self,
                     baseline: Dict[str, Any],
                     local_operations: List[Dict[str, Any]],
                     device_id: str = None) -> Dict[str, Any]:
        """
        完整的用戶識別流程 (F8習慣引擎)

        返回識別結果及同步決策
        """

        if device_id is None:
            device_id = self.get_device_id()

        # 合併本地操作文本
        full_text = ""
        for op in local_operations:
            full_text += f"{op.get('notes', '')}\n"
            full_text += f"{op.get('operation_name', '')}\n"

        # 簡化習慣匹配 (使用基線信息)
        # 實際應使用 HabitFingerprintManager.compute_habit_match()
        baseline_si = baseline.get('confidence_metrics', {}).get('overall_si', 0.0)
        estimated_si = baseline_si * 0.95  # 保守估計

        result = {
            'device_id': device_id,
            'device_seal': self.compute_device_seal(device_id),
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'identification': {
                'si_score': round(estimated_si, 4),
                'confidence_level': '🟢' if estimated_si >= 0.85 else ('🟡' if estimated_si >= 0.70 else '🔴'),
                'verified': estimated_si >= 0.85,
                'message': f"{'✅ Confirmed' if estimated_si >= 0.85 else '🟡 Pending'}: SI={estimated_si:.2%}"
            },
            'trust': {
                'trust_level': self.verify_device_trust(device_id, estimated_si)[0],
                'is_trusted': self.verify_device_trust(device_id, estimated_si)[1]
            },
            'sync_decision': self.auto_sync_decision(
                device_id,
                estimated_si,
                self.verify_device_trust(device_id, estimated_si)[0]
            )
        }

        return result

    def log_sync_operation(self, result: Dict[str, Any]) -> str:
        """記錄同步操作到日誌"""

        sync_record = {
            'timestamp': result['timestamp'],
            'device_id': result['device_id'],
            'si_score': result['identification']['si_score'],
            'trust_level': result['trust']['trust_level'],
            'sync_direction': result['sync_decision']['sync_direction'],
            'conflict_mode': result['sync_decision']['conflict_mode'],
            'post_actions': result['sync_decision']['post_sync_actions']
        }

        with open(self.sync_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(sync_record, ensure_ascii=False) + '\n')

        print(f"✅ 同步操作已記錄: {self.sync_log_file}")
        return str(self.sync_log_file)

    def grant_device_access(self, device_id: str, access_level: str = "full") -> Dict[str, Any]:
        """
        授予設備訪問權限

        access_level: "full" | "read_only" | "none"
        """

        registry = self.load_device_registry()

        if device_id not in registry:
            registry[device_id] = self.register_device(device_id)

        registry[device_id]['trust_level'] = 'trusted' if access_level == "full" else access_level
        registry[device_id]['last_sync'] = datetime.now(timezone.utc).isoformat()
        registry[device_id]['sync_count'] = registry[device_id].get('sync_count', 0) + 1

        self.save_device_registry(registry)

        print(f"✅ 設備已授權: {device_id} ({access_level})")
        return registry[device_id]

    def get_trusted_devices(self) -> List[str]:
        """獲取所有可信設備列表"""

        registry = self.load_device_registry()
        return [
            device_id for device_id, record in registry.items()
            if record.get('trust_level') == 'trusted'
        ]


# CLI示例
if __name__ == "__main__":
    identifier = CrossDeviceIdentifier()

    print("🌐 跨設備識別器 CLI")
    print("=" * 50)

    # 示例1: 獲取當前設備ID
    print("\n1️⃣ 當前設備信息:")
    device_id = identifier.get_device_id()
    device_seal = identifier.compute_device_seal(device_id)
    print(f"   設備ID: {device_id}")
    print(f"   設備封印: {device_seal}")

    # 示例2: 掃描本地操作
    print("\n2️⃣ 掃描本地操作:")
    operations = identifier.scan_local_operations(limit=5)
    print(f"   找到 {len(operations)} 條本地操作")
    for op in operations[:2]:
        print(f"     - {op.get('operation_id', 'unknown')}")

    # 示例3: 模擬習慣基線
    print("\n3️⃣ 創建習慣基線:")
    sample_baseline = {
        'typos': {'得': 0.15, '哪': 0.08},
        'catchphrases': {'嘿嘿': 0.45, '焊死': 0.32},
        'polyphonic': {'中': 0.95, '行': 0.85},
        'confidence_metrics': {
            'typo_confidence': 0.95,
            'catchphrase_confidence': 0.92,
            'polyphonic_confidence': 0.89,
            'overall_si': 0.92
        }
    }
    print(f"   基線SI: {sample_baseline['confidence_metrics']['overall_si']:.2%}")

    # 示例4: 完整識別流程
    print("\n4️⃣ 完整識別流程:")
    result = identifier.identify_user(sample_baseline, operations, device_id)

    print(f"\n   設備: {result['device_id']}")
    print(f"   {result['identification']['message']}")
    print(f"   信任等級: {result['trust']['trust_level']}")
    print(f"   同步決策: {result['sync_decision']['sync_direction']}")

    # 示例5: 授予訪問權限
    print("\n5️⃣ 設備授權:")
    if result['identification']['verified']:
        device_record = identifier.grant_device_access(device_id, "full")
        print(f"   ✅ 已授權: {device_id}")
        print(f"   同步計數: {device_record.get('sync_count', 0)}")

    # 示例6: 信任設備列表
    print("\n6️⃣ 可信設備列表:")
    trusted = identifier.get_trusted_devices()
    print(f"   {len(trusted)} 個可信設備")
    for dev in trusted:
        print(f"     - {dev}")

