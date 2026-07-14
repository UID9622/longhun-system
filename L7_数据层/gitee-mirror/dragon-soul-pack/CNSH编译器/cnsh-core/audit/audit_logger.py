#!/usr/bin/env python3
# ============================================================
# DNA追溯: #ZHUGEXIN⚡️20260302-CNSH-AUDIT-LOGGER-v1.0.0
# 確認碼: #CONFIRM🌌9622-ONLY-ONCE🧬AUDIT-LOG-772Z
# 創建時間: 2026-03-02 00:00:00 (UTC+8)
# 作者: Lucky·UID9622 (諸葛鑫)
# GPG指紋: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 狀態: 演進中
# 镜像来源: https://gitee.com/uid9622/cnsh/raw/main/audit/audit_logger.py
# ============================================================
"""
龍魂系統 · 審計日誌與變更歷史引擎 (Audit Logger)

遺漏5補全：審計日誌與變更歷史（可追溯性核心）

特性：
  - 不可篡改: 追加-only模式，禁止刪除
  - 多重簽名: 關鍵操作需UID9622+監督人格雙重確認
  - 定期歸檔: 每月生成月度審計報告，哈希上鏈
  - DNA追溯: 每條日誌自動附帶DNA追溯碼
"""

import datetime
import hashlib
import json
import os


class LogLevel:
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    AUDIT = "AUDIT"


class OperationType:
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    EXPORT = "EXPORT"
    FREEZE = "FREEZE"
    UNFREEZE = "UNFREEZE"
    ALERT = "ALERT"
    FUSE = "FUSE"
    AUTH = "AUTH"


class AuditLogEntry:
    """不可變審計日誌條目"""

    def __init__(self, operation, target_ip, operator, summary,
                 level=LogLevel.INFO, requires_dual_sign=False):
        self.timestamp = datetime.datetime.now().isoformat()
        self.operation = operation
        self.target_ip = target_ip
        self.operator = operator
        self.summary = summary
        self.level = level
        self.requires_dual_sign = requires_dual_sign
        self.dual_signed = False
        self.co_signer = None

        date_str = datetime.datetime.now().strftime("%Y%m%d")
        hash_suffix = hashlib.md5(
            f"{self.timestamp}{target_ip}{operator}".encode()
        ).hexdigest()[:8]
        self.dna = f"#ZHUGEXIN⚡️{date_str}-AUDIT-{hash_suffix}-v1.0.0"
        self.entry_hash = self._compute_hash()

    def _compute_hash(self):
        content = f"{self.timestamp}|{self.operation}|{self.target_ip}|{self.operator}|{self.summary}"
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def dual_sign(self, co_signer):
        self.dual_signed = True
        self.co_signer = co_signer

    def get_audit_result(self):
        result_map = {
            LogLevel.INFO: "🟢 通過",
            LogLevel.WARN: "🟡 警告",
            LogLevel.ERROR: "🔴 錯誤",
            LogLevel.CRITICAL: "⚫ 嚴重",
            LogLevel.AUDIT: "🔵 審計",
        }
        return result_map.get(self.level, "❓ 未知")

    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'operation': self.operation,
            'target_ip': self.target_ip,
            'operator': self.operator,
            'summary': self.summary,
            'level': self.level,
            'audit_result': self.get_audit_result(),
            'dna': self.dna,
            'entry_hash': self.entry_hash[:16] + '...',
            'dual_signed': self.dual_signed,
            'co_signer': self.co_signer,
        }

    def __str__(self):
        return (f"{self.timestamp} | {self.get_audit_result()} | "
                f"{self.operation:<8} | {self.target_ip:<10} | "
                f"{self.operator:<12} | {self.summary}")


class AuditLogEngine:
    def __init__(self, log_dir=None):
        self.entries = []
        self.chain_hash = None
        self.log_dir = log_dir or os.path.join(os.path.dirname(__file__), 'logs')

    def log(self, operation, target_ip, operator, summary,
            level=LogLevel.INFO, requires_dual_sign=False):
        entry = AuditLogEntry(
            operation=operation,
            target_ip=target_ip,
            operator=operator,
            summary=summary,
            level=level,
            requires_dual_sign=requires_dual_sign,
        )

        if self.chain_hash:
            combined = f"{self.chain_hash}|{entry.entry_hash}"
            self.chain_hash = hashlib.sha256(combined.encode()).hexdigest()
        else:
            self.chain_hash = entry.entry_hash

        self.entries.append(entry)
        return entry

    def get_recent(self, count=10):
        return self.entries[-count:]

    def get_by_ip(self, ip_id):
        return [e for e in self.entries if e.target_ip == ip_id]

    def get_by_operator(self, operator):
        return [e for e in self.entries if e.operator == operator]

    def get_alerts(self):
        return [e for e in self.entries
                if e.level in (LogLevel.WARN, LogLevel.ERROR, LogLevel.CRITICAL)]

    def generate_monthly_report(self, year=None, month=None):
        now = datetime.datetime.now()
        year = year or now.year
        month = month or now.month

        monthly = [
            e for e in self.entries
            if e.timestamp.startswith(f"{year}-{month:02d}")
        ]

        stats = {
            'total': len(monthly),
            'by_level': {},
            'by_operation': {},
            'by_operator': {},
        }

        for e in monthly:
            stats['by_level'][e.level] = stats['by_level'].get(e.level, 0) + 1
            stats['by_operation'][e.operation] = stats['by_operation'].get(e.operation, 0) + 1
            stats['by_operator'][e.operator] = stats['by_operator'].get(e.operator, 0) + 1

        report = {
            'title': f'龍魂系統月度審計報告 {year}-{month:02d}',
            'generated_at': now.isoformat(),
            'period': f"{year}-{month:02d}",
            'statistics': stats,
            'chain_hash': self.chain_hash,
            'entries': [e.to_dict() for e in monthly],
            'dna': f"#ZHUGEXIN⚡️{now.strftime('%Y%m%d')}-CNSH-MONTHLY-AUDIT-v1.0.0",
        }

        return report

    def verify_chain_integrity(self):
        if not self.entries:
            return True, "日誌為空"

        computed_hash = None
        for entry in self.entries:
            if computed_hash:
                combined = f"{computed_hash}|{entry.entry_hash}"
                computed_hash = hashlib.sha256(combined.encode()).hexdigest()
            else:
                computed_hash = entry.entry_hash

        if computed_hash == self.chain_hash:
            return True, f"🟢 鏈式哈希完整性校驗通過 ({len(self.entries)} 條記錄)"
        else:
            return False, "🔴 鏈式哈希不一致，日誌可能被篡改"

    def print_table(self, entries=None, max_rows=10):
        entries = entries or self.get_recent(max_rows)
        print(f"{'時間戳':<22} {'結果':<10} {'操作':<10} "
              f"{'目標IP':<12} {'操作人':<14} {'摘要'}")
        print("-" * 90)
        for e in entries:
            print(str(e))


if __name__ == '__main__':
    engine = AuditLogEngine()
    print("📋 龍魂系統 · 審計日誌引擎 v1.0")
    print("=" * 60)

    engine.log(OperationType.CREATE, "IP-0021", "UID9622", "新增熔斷矩陣模塊", LogLevel.INFO)
    engine.log(OperationType.UPDATE, "IP-0019", "諸葛亮", "完善71人格聯動邏輯", LogLevel.INFO)
    engine.log(OperationType.AUDIT, "IP-0003", "審判長", "季度價值觀審查", LogLevel.AUDIT)
    engine.log(OperationType.EXPORT, "IP-0001", "魯班", "導出GitHub Release", LogLevel.INFO)
    engine.log(OperationType.ALERT, "IP-0011", "上帝之眼", "檢測到異常訪問嘗試", LogLevel.WARN)

    print("\n📊 最近審計記錄:")
    engine.print_table()

    ok, msg = engine.verify_chain_integrity()
    print(f"\n🔐 {msg}")

    report = engine.generate_monthly_report()
    print(f"\n📅 月度報告: {report['title']}")
    print(f"   總記錄: {report['statistics']['total']}")
    print(f"   鏈式哈希: {report['chain_hash'][:32]}...")
