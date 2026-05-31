#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 Notion 集成 · Stage 4 審計日誌同步

DNA: #龍芯⚇️2026-06-01-AUDIT-SYNC-v1.0
Purpose: 同步龍魂系統的審計日誌到 Notion

Features:
  - 分析系統審計日誌（393 條記錄）
  - 健康檢查日誌分類
  - 性能基線統計
  - 警告事件聚合
  - 審計追踪同步
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict

current_dir = str(Path(__file__).parent)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from .notion_config import NotionConfigManager, NotionConfig
    from .notion_client import NotionClient, NotionAuthError
except ImportError:
    from notion_config import NotionConfigManager, NotionConfig
    from notion_client import NotionClient, NotionAuthError


class AuditLogAnalyzer:
    """審計日誌分析引擎"""

    def __init__(self):
        self.home = Path.home()
        self.audit_dir = self.home / ".龍魂"
        self.system_dir = self.home / "longhun-system" / "日誌"

    def load_audit_files(self) -> Dict[str, List[dict]]:
        """加載系統審計日誌"""
        audit_data = {
            "health_checks": [],
            "performance_metrics": [],
            "warning_events": [],
            "audit_logs": []
        }

        try:
            # 健康檢查日誌
            health_files = [
                "home_full_chain_trace.jsonl",
                "home_battlefield_trace.jsonl",
                "semantic_hook_trace.jsonl",
                "audit_check.jsonl"
            ]

            for filename in health_files:
                filepath = self.system_dir / filename
                if filepath.exists():
                    audit_data["health_checks"].extend(
                        self._parse_jsonl(filepath)
                    )

            # 性能基線 / DNA 註冊
            perf_files = [
                "dna_registry.jsonl",
                "batch_audit_20260526_142653.jsonl",
                "engine_audit.jsonl"
            ]

            for filename in perf_files:
                filepath = self.system_dir / filename
                if filepath.exists():
                    audit_data["performance_metrics"].extend(
                        self._parse_jsonl(filepath)
                    )

            # 警告事件（拒絕、異常）
            warning_files = [
                "render_session.jsonl",
                "共振命中_20260519.jsonl"
            ]

            for filename in warning_files:
                filepath = self.system_dir / filename
                if filepath.exists():
                    records = self._parse_jsonl(filepath)
                    # 過濾警告和拒絕事件
                    for rec in records:
                        if isinstance(rec, dict):
                            event = rec.get("event", "")
                            if event in ["deny", "error", "warning", "hit"]:
                                audit_data["warning_events"].append(rec)

            # 審計日誌（身份、憑證、權限）
            audit_files = [
                "credential_audit.jsonl",
                "credentials_verified_on_boot.jsonl",
                "authority_audit.jsonl",
                "identity_audit.jsonl",
                "mcp-mini-audit.jsonl"
            ]

            for filename in audit_files:
                filepath = self.system_dir / filename
                if filepath.exists():
                    audit_data["audit_logs"].extend(
                        self._parse_jsonl(filepath)
                    )

            # 會話審計
            state_dir = self.home / "longhun-system" / "state"
            dialog_audit = state_dir / "dialog-audit.jsonl"
            if dialog_audit.exists():
                audit_data["audit_logs"].extend(
                    self._parse_jsonl(dialog_audit)
                )

        except Exception as e:
            print(f"⚠️  加載審計日誌出錯: {e}")

        return audit_data

    def _parse_jsonl(self, filepath: Path) -> List[dict]:
        """解析 JSONL 文件"""
        records = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            records.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            print(f"❌ 讀取 {filepath} 失敗: {e}")
        return records

    def analyze_health_checks(self, records: List[dict]) -> Dict:
        """分析健康檢查日誌"""
        summary = {
            "total_checks": len(records),
            "checks_by_status": defaultdict(int),
            "items": []
        }

        for rec in records:
            if isinstance(rec, dict):
                status = rec.get("status", rec.get("ok", "unknown"))
                summary["checks_by_status"][str(status)] += 1

                # 提取檢查項
                if "items" in rec:
                    summary["items"].extend(rec["items"])

        return dict(summary)

    def analyze_performance_metrics(self, records: List[dict]) -> Dict:
        """分析性能基線"""
        summary = {
            "total_records": len(records),
            "dr_distribution": defaultdict(int),
            "color_distribution": defaultdict(int),
            "items": []
        }

        for rec in records:
            if isinstance(rec, dict):
                dr = rec.get("dr", rec.get("digital_root", 0))
                color = rec.get("color", self._get_color_by_dr(dr))

                summary["dr_distribution"][str(dr)] += 1
                summary["color_distribution"][color] += 1

                summary["items"].append({
                    "timestamp": rec.get("timestamp", ""),
                    "dr": dr,
                    "color": color,
                    "description": rec.get("name", rec.get("description", ""))[:200]
                })

        return dict(summary)

    def analyze_warning_events(self, records: List[dict]) -> Dict:
        """分析警告事件"""
        summary = {
            "total_warnings": len(records),
            "events_by_type": defaultdict(int),
            "severity_distribution": defaultdict(int),
            "items": []
        }

        for rec in records:
            if isinstance(rec, dict):
                event = rec.get("event", rec.get("status", "unknown"))
                summary["events_by_type"][event] += 1

                # 判斷嚴重性
                severity = "medium"
                if event in ["error", "deny"]:
                    severity = "high"
                elif event in ["warning"]:
                    severity = "medium"
                else:
                    severity = "low"

                summary["severity_distribution"][severity] += 1

                summary["items"].append({
                    "timestamp": rec.get("timestamp", rec.get("ts", "")),
                    "event": event,
                    "severity": severity,
                    "note": rec.get("note", rec.get("message", ""))[:300]
                })

        return dict(summary)

    def analyze_audit_logs(self, records: List[dict]) -> Dict:
        """分析審計日誌"""
        summary = {
            "total_logs": len(records),
            "operation_types": defaultdict(int),
            "uid_distribution": defaultdict(int),
            "items": []
        }

        for rec in records:
            if isinstance(rec, dict):
                operation = rec.get("operation", rec.get("action", "unknown"))
                uid = rec.get("uid", rec.get("user_id", "unknown"))

                summary["operation_types"][str(operation)] += 1
                summary["uid_distribution"][str(uid)] += 1

                summary["items"].append({
                    "timestamp": rec.get("timestamp", ""),
                    "uid": uid,
                    "operation": operation,
                    "status": rec.get("status", rec.get("result", "")),
                    "description": rec.get("message", rec.get("description", ""))[:300]
                })

        return dict(summary)

    @staticmethod
    def _get_color_by_dr(dr: int) -> str:
        """根據數字根獲得顏色"""
        if dr in [1, 2]:
            return "🟢"
        elif dr in [3, 4, 5, 6]:
            return "🟡"
        else:
            return "🔴"


class AuditNotionSync:
    """審計日誌 Notion 同步器"""

    def __init__(self, client: NotionClient, config: NotionConfig):
        self.client = client
        self.config = config
        self.analyzer = AuditLogAnalyzer()
        self.sync_log = []

    def sync_all(self) -> bool:
        """執行全量同步"""
        print("\n📊 分析審計日誌...")

        audit_data = self.analyzer.load_audit_files()

        if not any(audit_data.values()):
            print("⚠️  未找到審計日誌數據，進入本地預覽模式")
            return self._preview_data(audit_data)

        print(f"✅ 加載審計數據：")
        print(f"   - 健康檢查: {len(audit_data['health_checks'])} 條")
        print(f"   - 性能基線: {len(audit_data['performance_metrics'])} 條")
        print(f"   - 警告事件: {len(audit_data['warning_events'])} 條")
        print(f"   - 審計日誌: {len(audit_data['audit_logs'])} 條")

        # 檢查數據庫配置
        if not self._check_databases():
            print("⚠️  未配置數據庫 ID，進入本地預覽模式")
            return self._preview_data(audit_data)

        # 執行同步
        try:
            print("\n🔄 開始同步...")

            if audit_data["health_checks"]:
                self._sync_health_checks(audit_data["health_checks"])

            if audit_data["performance_metrics"]:
                self._sync_performance_metrics(audit_data["performance_metrics"])

            if audit_data["warning_events"]:
                self._sync_warning_events(audit_data["warning_events"])

            if audit_data["audit_logs"]:
                self._sync_audit_logs(audit_data["audit_logs"])

            self._log_sync("success")
            print("✅ 審計日誌同步完成")
            return True

        except Exception as e:
            print(f"❌ 同步失敗: {e}")
            self._log_sync("error", str(e))
            return False

    def _check_databases(self) -> bool:
        """驗證數據庫 ID"""
        required = ["health_db", "baseline_db", "alert_db", "audit_db"]
        missing = [db for db in required if not getattr(self.config, db, None)]

        if missing:
            print(f"❌ 缺少以下數據庫 ID:")
            for db in missing:
                print(f"   - {db}")
            return False

        return True

    def _preview_data(self, audit_data: dict) -> bool:
        """本地預覽模式"""
        print("\n" + "=" * 70)
        print("🏠 本地預覽模式 - 審計日誌數據")
        print("=" * 70)

        analyzer = AuditLogAnalyzer()

        if audit_data["health_checks"]:
            print("\n📋 健康檢查分析")
            summary = analyzer.analyze_health_checks(audit_data["health_checks"])
            print(f"   總檢查數: {summary.get('total_checks', 0)}")
            for status, count in summary.get('checks_by_status', {}).items():
                print(f"   - {status}: {count}")

        if audit_data["performance_metrics"]:
            print("\n📊 性能基線分析")
            summary = analyzer.analyze_performance_metrics(audit_data["performance_metrics"])
            print(f"   總記錄數: {summary.get('total_records', 0)}")
            print("   數字根分布:")
            for dr, count in sorted(summary.get('dr_distribution', {}).items()):
                color = analyzer._get_color_by_dr(int(dr))
                print(f"   - dr={dr} {color}: {count}")

        if audit_data["warning_events"]:
            print("\n⚠️  警告事件分析")
            summary = analyzer.analyze_warning_events(audit_data["warning_events"])
            print(f"   總警告數: {summary.get('total_warnings', 0)}")
            for event, count in summary.get('events_by_type', {}).items():
                print(f"   - {event}: {count}")

        if audit_data["audit_logs"]:
            print("\n🔐 審計日誌分析")
            summary = analyzer.analyze_audit_logs(audit_data["audit_logs"])
            print(f"   總日誌數: {summary.get('total_logs', 0)}")
            print("   操作類型:")
            for op, count in summary.get('operation_types', {}).items():
                print(f"   - {op}: {count}")

        print("\n" + "=" * 70)
        print("💡 提示: 運行 stage_4_setup.py 創建數據庫並執行同步")
        print("=" * 70)

        return True

    def _sync_health_checks(self, records: List[dict]):
        """同步健康檢查日誌"""
        print(f"🏥 同步健康檢查 ({len(records)} 條)...")

        analyzer = AuditLogAnalyzer()
        summary = analyzer.analyze_health_checks(records)

        # 創建摘要頁面
        properties = {
            "名稱": {"title": [{"text": {"content": f"健康檢查摘要 - {datetime.now().strftime('%Y-%m-%d')}"}}]},
            "狀態": {"rich_text": [{"text": {"content": str(summary.get('checks_by_status', {}))}}]},
            "檢查項數": {"number": summary.get('total_checks', 0)},
            "DNA": {"rich_text": [{"text": {"content": "#龍芯⚇️2026-06-01-AUDIT-HEALTH-CHECK-SYNC"}}]}
        }

        try:
            result = self.client.create_page(
                parent_id=self.config.health_db,
                properties=properties
            )
            print(f"   ✅ 摘要頁面: {result.get('id', 'unknown')}")
        except Exception as e:
            print(f"   ⚠️  創建摘要失敗: {e}")

    def _sync_performance_metrics(self, records: List[dict]):
        """同步性能基線"""
        print(f"📈 同步性能基線 ({len(records)} 條)...")

        analyzer = AuditLogAnalyzer()
        summary = analyzer.analyze_performance_metrics(records)

        # 按數字根分類創建頁面
        for dr in sorted(summary.get('dr_distribution', {}).keys()):
            count = summary['dr_distribution'][dr]
            color = analyzer._get_color_by_dr(int(dr))

            properties = {
                "數字根": {"title": [{"text": {"content": f"DR={dr} {color}"}}]},
                "記錄數": {"number": count},
                "顏色": {"rich_text": [{"text": {"content": color}}]},
                "DNA": {"rich_text": [{"text": {"content": f"#龍芯⚇️2026-06-01-BASELINE-DR{dr}"}}]}
            }

            try:
                result = self.client.create_page(
                    parent_id=self.config.baseline_db,
                    properties=properties
                )
                print(f"   ✅ DR={dr}: {count} 條")
            except Exception as e:
                print(f"   ⚠️  DR={dr} 創建失敗: {e}")

    def _sync_warning_events(self, records: List[dict]):
        """同步警告事件"""
        print(f"🚨 同步警告事件 ({len(records)} 條)...")

        analyzer = AuditLogAnalyzer()
        summary = analyzer.analyze_warning_events(records)

        # 按嚴重性分類創建頁面
        for severity in ["high", "medium", "low"]:
            count = summary['severity_distribution'].get(severity, 0)
            if count > 0:
                emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(severity, "❓")

                properties = {
                    "嚴重性": {"title": [{"text": {"content": f"{emoji} {severity.upper()}"}}]},
                    "事件數": {"number": count},
                    "說明": {"rich_text": [{"text": {"content": f"共 {count} 個 {severity} 級別事件"}}]},
                    "DNA": {"rich_text": [{"text": {"content": f"#龍芯⚇️2026-06-01-ALERT-{severity.upper()}"}}]}
                }

                try:
                    result = self.client.create_page(
                        parent_id=self.config.alert_db,
                        properties=properties
                    )
                    print(f"   ✅ {emoji} {severity}: {count} 條")
                except Exception as e:
                    print(f"   ⚠️  {severity} 創建失敗: {e}")

    def _sync_audit_logs(self, records: List[dict]):
        """同步審計日誌"""
        print(f"🔐 同步審計日誌 ({len(records)} 條)...")

        analyzer = AuditLogAnalyzer()
        summary = analyzer.analyze_audit_logs(records)

        # 按操作類型分類創建頁面
        for operation in list(summary.get('operation_types', {}).keys())[:5]:  # 最多 5 個
            count = summary['operation_types'][operation]

            properties = {
                "操作": {"title": [{"text": {"content": f"{operation}"}}]},
                "計數": {"number": count},
                "狀態": {"rich_text": [{"text": {"content": "已記錄"}}]},
                "DNA": {"rich_text": [{"text": {"content": f"#龍芯⚇️2026-06-01-AUDIT-{str(operation).upper()}"}}]}
            }

            try:
                result = self.client.create_page(
                    parent_id=self.config.audit_db,
                    properties=properties
                )
                print(f"   ✅ {operation}: {count} 條")
            except Exception as e:
                print(f"   ⚠️  {operation} 創建失敗: {e}")

    def _log_sync(self, status: str, error: Optional[str] = None):
        """記錄同步操作"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "stage": "4",
            "module": "audit_sync",
            "status": status,
            "records_processed": sum([
                len(self.analyzer.load_audit_files().get(k, []))
                for k in ["health_checks", "performance_metrics", "warning_events", "audit_logs"]
            ]),
        }

        if error:
            log_entry["error"] = error

        log_file = Path.home() / ".龍魂" / "notion_audit_sync.jsonl"
        log_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"⚠️  無法寫入審計日誌: {e}")
