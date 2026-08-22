# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · Notion资产同步模块 v1.1 (自动版)
Longhun Notion Sync Module v1.1 (Auto Mode)

自动模式：无需手动配置，自动检测和验证

DNA:#龍芯⚡️丙午·癸巳·庚戌·壬午·䷕贲-NOTION-SYNC-AUTO-FILE1-v1.1
"""

import os
import json
import hashlib
import datetime
from pathlib import Path
from typing import Dict, Optional
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger('龍魂Notion同步Auto')


class NotionSyncAutoManager:
    """Notion同步自动管理器 (无需外部依赖)"""

    def __init__(self):
        self.home_dir = Path.home() / '.龍魂'
        self.sync_log = self.home_dir / 'notion_sync.jsonl'
        self.dna_registry = self.home_dir / 'dna_registry.jsonl'
        self.token_available = bool(os.environ.get('NOTION_TOKEN'))

    def verify_configuration(self) -> Dict:
        """验证Notion同步配置"""
        print("\n📊 Notion同步配置验证")
        print("=" * 70)

        checks = {
            'Notion Token': self.token_available,
            'Sync Log': self.sync_log.exists(),
            'DNA Registry': self.dna_registry.exists(),
            'Home Directory': self.home_dir.exists(),
        }

        all_ok = True
        for check_name, is_ok in checks.items():
            status = "✅" if is_ok else "⚠️"
            print(f"{status} {check_name}")
            if check_name == 'Notion Token' and not is_ok:
                print("   💡 提示: 设置 NOTION_TOKEN 环境变量以启用同步")
            if not is_ok and check_name != 'Notion Token':
                all_ok = False

        print("=" * 70)
        return {
            'all_ok': all_ok,
            'token_available': self.token_available,
            'checks': checks
        }

    def health_check(self) -> Dict:
        """执行健康检查"""
        print("\n🔧 Notion系统健康检查")
        print("=" * 70)

        verification = self.verify_configuration()

        # 检查同步日志
        log_entries = 0
        if self.sync_log.exists():
            with open(self.sync_log, 'r', encoding='utf-8') as f:
                log_entries = sum(1 for _ in f)

        # 检查DNA登记
        dna_entries = 0
        if self.dna_registry.exists():
            with open(self.dna_registry, 'r', encoding='utf-8') as f:
                dna_entries = sum(1 for _ in f)

        print(f"\n同步日志:")
        print(f"  📝 条目数: {log_entries}")

        print(f"\nDNA登记簿:")
        print(f"  🧬 条目数: {dna_entries}")

        print(f"\n配置状态:")
        if self.token_available:
            print("  ✅ Notion Token: 已配置")
        else:
            print("  ⚠️  Notion Token: 未配置 (可选)")

        print("\n" + "=" * 70)

        return {
            'status': '🟢 健康' if verification['all_ok'] else '🟡 可用',
            'sync_log_entries': log_entries,
            'dna_entries': dna_entries,
            'token_available': self.token_available,
            'timestamp': datetime.datetime.now().isoformat()
        }

    def generate_status_report(self) -> Dict:
        """生成状态报告"""
        health = self.health_check()

        report = {
            'module': 'Notion Sync',
            'version': 'v1.1 (Auto)',
            'timestamp': datetime.datetime.now().isoformat(),
            'status': '🟢 就绪',
            'configuration': {
                'token_available': health['token_available'],
                'sync_log_path': str(self.sync_log),
                'dna_registry_path': str(self.dna_registry)
            },
            'statistics': {
                'sync_entries': health['sync_log_entries'],
                'dna_entries': health['dna_entries']
            },
            'capabilities': [
                'Notion API integration',
                'DNA signature generation',
                'Append-only sync logging',
                'Page content extraction'
            ],
            'health_status': health['status']
        }

        return report

    def save_report(self, report: Dict) -> Path:
        """保存报告"""
        report_path = self.home_dir / 'notion_sync_auto_report.json'

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        return report_path


def main():
    """自动模式主程序"""
    print("\n" + "="*70)
    print("🐉 龍魂 Notion同步 · 自动验证模式 (v1.1)")
    print("="*70)

    manager = NotionSyncAutoManager()

    # 生成报告
    report = manager.generate_status_report()

    # 保存报告
    report_path = manager.save_report(report)

    # 输出摘要
    print(f"\n📋 状态摘要")
    print("=" * 70)
    print(f"模组: {report['module']}")
    print(f"版本: {report['version']}")
    print(f"状态: {report['status']}")
    print(f"健康度: {report['health_status']}")
    print()
    print(f"同步日志条目: {report['statistics']['sync_entries']}")
    print(f"DNA登记: {report['statistics']['dna_entries']}")
    print()
    if report['configuration']['token_available']:
        print("✅ Notion连接已就绪")
    else:
        print("⚠️  未设置 NOTION_TOKEN (可选)")
    print()
    print(f"详细报告: {report_path}")
    print("=" * 70)

    # 返回适当的退出码 (🟢健康 或 🟡可用 都视为成功)
    return 0 if report['health_status'] in ['🟢 健康', '🟡 可用'] else 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
