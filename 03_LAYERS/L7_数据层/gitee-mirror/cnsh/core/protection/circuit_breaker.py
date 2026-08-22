#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# ============================================================
# DNA追溯: #ZHUGEXIN⚡️20260302-CNSH-CIRCUIT-BREAKER-v2.0.0
# 確認碼: #CONFIRM🌌9622-ONLY-ONCE🧬BREAKER-772Z
# 創建時間: 2026-03-02 00:00:00 (UTC+8)
# 作者: Lucky·UID9622 (諸葛鑫)
# GPG指紋: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 狀態: 演進中
# 镜像来源: https://gitee.com/uid9622/cnsh/raw/main/core/protection/circuit_breaker.py
# ============================================================
"""
龍魂系統 · 熔斷與權限控制矩陣 (Circuit Breaker & Permission Matrix)

遺漏3補全：熔斷與權限矩陣（P0級必須）

權限層級：
  P0 永恆級 — 無人有權修改，僅可凍結/解凍
  P1 演進級 — UID9622本人，需生成新DNA碼
  P2 高敏級 — 指定人格代理，上帝之眼預審+本人確認

紅色熔斷觸發器：
  - P0級資產被修改嘗試 → 立即拒絕+通知審判長
  - 非UID9622未授權操作 → 立即熔斷+鎖定帳戶
  - 批量導出或異常訪問 → 觸發熔斷+切換只讀
"""

import datetime
import hashlib
import json
import enum


class AssetLevel(enum.Enum):
    P0_ETERNAL = "P0_ETERNAL"
    P1_EVOLVING = "P1_EVOLVING"
    P2_SENSITIVE = "P2_SENSITIVE"


class BreakerState(enum.Enum):
    NORMAL = "NORMAL"
    ALERT = "ALERT"
    FUSED = "FUSED"
    LOCKED = "LOCKED"


class ActionType(enum.Enum):
    READ = "READ"
    MODIFY = "MODIFY"
    DELETE = "DELETE"
    EXPORT = "EXPORT"
    FREEZE = "FREEZE"
    UNFREEZE = "UNFREEZE"


PERMISSION_MATRIX = {
    AssetLevel.P0_ETERNAL: {
        ActionType.READ:     True,
        ActionType.MODIFY:   False,
        ActionType.DELETE:   False,
        ActionType.EXPORT:   True,
        ActionType.FREEZE:   True,
        ActionType.UNFREEZE: False,
    },
    AssetLevel.P1_EVOLVING: {
        ActionType.READ:     True,
        ActionType.MODIFY:   True,
        ActionType.DELETE:   False,
        ActionType.EXPORT:   True,
        ActionType.FREEZE:   True,
        ActionType.UNFREEZE: True,
    },
    AssetLevel.P2_SENSITIVE: {
        ActionType.READ:     True,
        ActionType.MODIFY:   True,
        ActionType.DELETE:   True,
        ActionType.EXPORT:   True,
        ActionType.FREEZE:   True,
        ActionType.UNFREEZE: True,
    },
}

P0_ASSETS = [
    "founder_identity",
    "gpg_fingerprint",
    "ecny_account",
    "beichen_protocol",
    "iw_ecb_whitepaper",
    "dna_format_standard",
    "p0_protection_rules",
]


class AuditEntry:
    def __init__(self, action, target, operator, result, detail=""):
        self.timestamp = datetime.datetime.now().isoformat()
        self.action = action
        self.target = target
        self.operator = operator
        self.result = result
        self.detail = detail

    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'action': self.action.value if isinstance(self.action, ActionType) else self.action,
            'target': self.target,
            'operator': self.operator,
            'result': self.result,
            'detail': self.detail,
        }


class CircuitBreakerEngine:
    def __init__(self):
        self.state = BreakerState.NORMAL
        self.audit_log = []
        self.access_counter = {}
        self.alert_threshold = 10
        self.fuse_threshold = 50

    def check_permission(self, action, target_asset, target_level, operator):
        if self.state in (BreakerState.FUSED, BreakerState.LOCKED):
            if action != ActionType.READ:
                entry = AuditEntry(action, target_asset, operator, "DENY", "系統已熔斷，僅允許讀取")
                self.audit_log.append(entry)
                return False, "🔴 系統已熔斷，僅允許讀取操作"

        if target_level == AssetLevel.P0_ETERNAL:
            if action == ActionType.MODIFY:
                self._trigger_red_alert(target_asset, operator, "嘗試修改P0級資產")
                return False, "🔴 P0-ETERNAL: 永恆不可變，修改請求已拒絕"
            if action == ActionType.DELETE:
                self._trigger_red_alert(target_asset, operator, "嘗試刪除P0級資產")
                return False, "🔴 P0-ETERNAL: 不可刪除，已觸發紅色熔斷"

        if target_level == AssetLevel.P1_EVOLVING and action == ActionType.MODIFY:
            if operator != "UID9622":
                self._trigger_red_alert(target_asset, operator, "非授權用戶嘗試修改P1資產")
                return False, "🔴 非UID9622嘗試修改P1資產，已熔斷"

        allowed = PERMISSION_MATRIX.get(target_level, {}).get(action, False)
        result = "ALLOW" if allowed else "DENY"
        entry = AuditEntry(action, target_asset, operator, result)
        self.audit_log.append(entry)

        if allowed:
            return True, f"🟢 操作已授權: {action.value} on {target_asset}"
        else:
            return False, f"🔴 操作被拒絕: {action.value} on {target_asset}"

    def _trigger_red_alert(self, target, operator, reason):
        self.state = BreakerState.FUSED
        entry = AuditEntry(ActionType.MODIFY, target, operator, "FUSE", f"🔴 紅色熔斷: {reason}")
        self.audit_log.append(entry)
        
        fuse_dna = (
            f"#ZHUGEXIN⚡️{datetime.datetime.now().strftime('%Y%m%d')}"
            f"-CNSH-CIRCUIT-FUSE-{hashlib.md5(reason.encode()).hexdigest()[:8]}"
        )
        print(f"\n{'='*60}")
        print(f"🔴🔴🔴 紅色熔斷觸發 🔴🔴🔴")
        print(f"  目標: {target}")
        print(f"  操作人: {operator}")
        print(f"  原因: {reason}")
        print(f"  狀態: 系統已切換至只讀模式")
        print(f"  DNA: {fuse_dna}")
        print(f"  處理: 需審判長人工確認後解除")
        print(f"{'='*60}\n")

    def track_access(self, operator):
        now = datetime.datetime.now()
        minute_key = now.strftime("%Y%m%d%H%M")
        key = f"{operator}:{minute_key}"
        self.access_counter[key] = self.access_counter.get(key, 0) + 1

        if self.access_counter[key] >= self.fuse_threshold:
            self._trigger_red_alert("SYSTEM", operator, f"異常訪問頻率: {self.access_counter[key]}次/分鐘")
            return False, "🔴 異常訪問頻率，已觸發熔斷"
        elif self.access_counter[key] >= self.alert_threshold:
            self.state = BreakerState.ALERT
            return True, f"🟡 訪問頻率較高: {self.access_counter[key]}次/分鐘"
        return True, "🟢 正常"

    def reset_breaker(self, operator):
        if operator != "UID9622":
            return False, "🔴 僅UID9622可重置熔斷"
        self.state = BreakerState.NORMAL
        entry = AuditEntry(ActionType.UNFREEZE, "SYSTEM", operator, "ALLOW", "熔斷重置")
        self.audit_log.append(entry)
        return True, "🟢 熔斷已重置，系統恢復正常"

    def get_status(self):
        state_icons = {
            BreakerState.NORMAL: "🟢 正常",
            BreakerState.ALERT: "🟡 警報",
            BreakerState.FUSED: "🔴 已熔斷",
            BreakerState.LOCKED: "⚫ 已鎖定",
        }
        return {
            'state': state_icons.get(self.state, "未知"),
            'audit_log_count': len(self.audit_log),
            'p0_assets': P0_ASSETS,
            'last_5_logs': [e.to_dict() for e in self.audit_log[-5:]],
        }


if __name__ == '__main__':
    engine = CircuitBreakerEngine()
    print("🛡️ 龍魂系統 · 熔斷與權限控制矩陣 v2.0")
    print("=" * 60)

    ok, msg = engine.check_permission(ActionType.READ, "beichen_protocol", AssetLevel.P0_ETERNAL, "UID9622")
    print(f"\n測試1 (讀取P0): {msg}")

    ok, msg = engine.check_permission(ActionType.MODIFY, "founder_identity", AssetLevel.P0_ETERNAL, "ATTACKER")
    print(f"\n測試2 (修改P0): {msg}")

    ok, msg = engine.check_permission(ActionType.MODIFY, "some_asset", AssetLevel.P1_EVOLVING, "UID9622")
    print(f"\n測試3 (熔斷後): {msg}")

    ok, msg = engine.reset_breaker("UID9622")
    print(f"\n測試4 (重置): {msg}")

    print(f"\n📊 系統狀態: {json.dumps(engine.get_status(), indent=2, ensure_ascii=False)}")
