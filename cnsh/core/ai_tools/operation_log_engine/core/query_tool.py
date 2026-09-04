#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# 1 道统层 Dao           : 曾仕强老师
# 2 精神层 Spirit        : Steve Jobs
# 3 设备层 Device        : Apple
# 4 技术层 Technology    : Open Source
# 5 系统层 System        : UID9622
# 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
# DNA追溯码:#龍芯⚡️丙午·癸巳·丁未·丙午·䷖剥-CNSH-SOVEREIGN-PUBLISH-METADATA-FILE1286-v2.0
# 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
# 文件: query_tool.py | 标记时间: 2026-06-03T07:46:12+0800
# -*- coding: utf-8 -*-
"""
🔍 系统查询引擎 v1.0
操作日记 + DNA粒子 + 习惯分析 + 跨设备查询

DNA:#龍芯⚡️丙午·癸巳·甲辰·庚午·䷑蛊-QUERY-TOOL-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
责任: UID9622·不免责

核心查询功能:
  1. 操作日记查询 (按时间·ID·类型·设备)
  2. DNA粒子检索 (按信心度·三色·时间)
  3. 习惯指纹分析 (拼音·口头禅·多音字)
  4. 同步历史追踪 (USB·Git·冲突)
  5. 多签验证审计 (3/3状态·风险)
  6. 统计摘要 (趋势·基线·对比)
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple
from datetime import datetime, timezone
from collections import Counter
import re


class QueryTool:
    """
    系统查询引擎

    功能:
      - 多维度查询操作日记
      - DNA粒子检索与分析
      - 习惯指纹统计
      - 跨设备追踪
      - 审计和合规性查询
    """

    def __init__(self, log_dir: str = "~/.龍魂/操作日记"):
        self.log_dir = Path(log_dir).expanduser()
        self.ledger_file = self.log_dir / "operation_ledger.jsonl"
        self.dna_dir = self.log_dir / "dna_particles"
        self.habit_dir = self.log_dir / "habit_fingerprints"
        self.sync_dir = self.log_dir / "sync_records"
        self.multisig_dir = self.log_dir / "multisig_logs"

    # ========== 操作日记查询 ==========

    def query_operations(self,
                        start_date: str = None,
                        end_date: str = None,
                        operation_type: str = None,
                        device_id: str = None,
                        limit: int = 100) -> List[Dict[str, Any]]:
        """
        查询操作日记

        参数:
          start_date: ISO8601 开始时间 (e.g., "2026-05-30T00:00:00")
          end_date: ISO8601 结束时间
          operation_type: 操作类型 (工程·焊接·审计)
          device_id: 设备ID (MacBook-M4-Max-UID9622)
          limit: 返回最多N条

        返回: 匹配的操作记录列表
        """

        if not self.ledger_file.exists():
            return []

        operations = []
        with open(self.ledger_file, 'r', encoding='utf-8') as f:
            for line in f:
                op = json.loads(line)

                # 时间范围过滤
                if start_date and op.get('timestamp', '') < start_date:
                    continue
                if end_date and op.get('timestamp', '') > end_date:
                    continue

                # 操作类型过滤
                if operation_type and operation_type not in op.get('operation_type', ''):
                    continue

                # 设备过滤
                if device_id and op.get('device_id', '') != device_id:
                    continue

                operations.append(op)

        return operations[-limit:]

    def query_by_operation_id(self, operation_id: str) -> Dict[str, Any]:
        """按ID查询单个操作"""

        if not self.ledger_file.exists():
            return {}

        with open(self.ledger_file, 'r', encoding='utf-8') as f:
            for line in f:
                op = json.loads(line)
                if op['operation_id'] == operation_id:
                    return op

        return {}

    # ========== DNA粒子查询 ==========

    def query_dna_particles(self,
                           confidence_min: float = 0.0,
                           risk_color: str = None,
                           operation_type: str = None,
                           limit: int = 50) -> List[Dict[str, Any]]:
        """
        查询DNA粒子

        参数:
          confidence_min: 最低信心度 (0.0-1.0)
          risk_color: 风险颜色 (🟢·🟡·🔴)
          operation_type: 操作类型过滤
          limit: 返回最多N条
        """

        if not self.dna_dir.exists():
            return []

        particles = []
        for dna_file in sorted(self.dna_dir.glob("*.dna.json"), reverse=True)[:limit]:
            with open(dna_file, 'r', encoding='utf-8') as f:
                particle = json.load(f)

                # 信心度过滤
                confidence = particle.get('habit_fingerprint', {}).get('overall_confidence', 0)
                if confidence < confidence_min:
                    continue

                # 风险颜色过滤
                if risk_color and particle.get('ten_fields', {}).get('risk_color', '') != risk_color:
                    continue

                # 操作类型过滤
                if operation_type and operation_type not in particle.get('operation', {}).get('type', ''):
                    continue

                particles.append(particle)

        return particles

    def get_dna_particle(self, operation_id: str) -> Dict[str, Any]:
        """获取单个DNA粒子"""

        dna_file = self.dna_dir / f"{operation_id}.dna.json"
        if not dna_file.exists():
            return {}

        with open(dna_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    # ========== 习惯指纹分析 ==========

    def analyze_habit_fingerprint(self) -> Dict[str, Any]:
        """
        分析习惯指纹 (完整统计)

        返回:
          {
            'pinyin_typos': {字: 频率, ...},
            'catchphrases': {短语: 频率, ...},
            'polyphonic_chars': {字: 惯用读音, ...},
            'trend': {日期: 操作数, ...}
          }
        """

        if not self.habit_dir.exists():
            return {}

        baseline_file = self.habit_dir / "baseline_snapshot.json"
        if not baseline_file.exists():
            return {}

        with open(baseline_file, 'r', encoding='utf-8') as f:
            baseline = json.load(f)

        # 构造返回结果
        analysis = {
            'typos': baseline.get('typos', {}),
            'catchphrases': baseline.get('catchphrases', {}),
            'polyphonic': baseline.get('polyphonic', {}),
            'confidence_metrics': baseline.get('confidence_metrics', {}),
            'collection_stats': {
                'records_analyzed': baseline.get('metadata', {}).get('records_analyzed', 0),
                'baseline_created': baseline.get('metadata', {}).get('baseline_created', ''),
                'confidence_threshold': baseline.get('metadata', {}).get('confidence_threshold', 0.85)
            }
        }

        return analysis

    def get_habit_trend(self, days: int = 7) -> Dict[str, int]:
        """
        获取习惯趋势 (最近N天)

        返回: {日期: 操作数, ...}
        """

        if not self.ledger_file.exists():
            return {}

        trend = {}
        with open(self.ledger_file, 'r', encoding='utf-8') as f:
            for line in f:
                op = json.loads(line)
                timestamp = op.get('timestamp', '')
                if timestamp:
                    date = timestamp[:10]  # YYYY-MM-DD
                    trend[date] = trend.get(date, 0) + 1

        return dict(sorted(trend.items())[-days:])

    # ========== 跨设备查询 ==========

    def get_device_summary(self) -> Dict[str, Any]:
        """获取所有设备的统计摘要"""

        if not self.ledger_file.exists():
            return {}

        device_stats = {}
        with open(self.ledger_file, 'r', encoding='utf-8') as f:
            for line in f:
                op = json.loads(line)
                device = op.get('device_id', 'unknown')

                if device not in device_stats:
                    device_stats[device] = {
                        'operation_count': 0,
                        'avg_habit_match': 0.0,
                        'first_seen': op.get('timestamp', ''),
                        'last_seen': op.get('timestamp', ''),
                        'operation_types': []
                    }

                stats = device_stats[device]
                stats['operation_count'] += 1
                stats['last_seen'] = op.get('timestamp', '')
                stats['operation_types'].append(op.get('operation_type', ''))

        # 计算平均
        for device, stats in device_stats.items():
            if stats['operation_count'] > 0:
                all_matches = []
                with open(self.ledger_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        op = json.loads(line)
                        if op.get('device_id', '') == device:
                            all_matches.append(op.get('habit_fingerprint_match', 0))
                stats['avg_habit_match'] = sum(all_matches) / len(all_matches) if all_matches else 0.0
                stats['operation_types'] = list(set(stats['operation_types']))

        return device_stats

    def get_device_operations(self, device_id: str) -> List[Dict[str, Any]]:
        """获取某设备的所有操作"""

        return self.query_operations(device_id=device_id, limit=1000)

    # ========== 同步和验证查询 ==========

    def get_sync_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """查询同步历史"""

        sync_log = self.sync_dir / "sync_operations.jsonl"
        if not sync_log.exists():
            return []

        history = []
        with open(sync_log, 'r', encoding='utf-8') as f:
            for line in f:
                history.append(json.loads(line))

        return history[-limit:]

    def get_conflicts(self) -> List[Dict[str, Any]]:
        """获取所有同步冲突记录"""

        conflict_log = self.sync_dir / "conflicts.jsonl"
        if not conflict_log.exists():
            return []

        conflicts = []
        with open(conflict_log, 'r', encoding='utf-8') as f:
            for line in f:
                conflicts.append(json.loads(line))

        return conflicts

    def get_multisig_verification_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """查询多签验证历史"""

        verify_log = self.multisig_dir / "verifications.jsonl"
        if not verify_log.exists():
            return []

        history = []
        with open(verify_log, 'r', encoding='utf-8') as f:
            for line in f:
                history.append(json.loads(line))

        return history[-limit:]

    def get_multisig_alerts(self, risk_level: str | None = None) -> List[Dict[str, Any]]:
        """查询多签警报·按风险等级过滤"""

        alert_log = self.multisig_dir / "alerts.jsonl"
        if not alert_log.exists():
            return []

        alerts = []
        with open(alert_log, 'r', encoding='utf-8') as f:
            for line in f:
                alert = json.loads(line)
                if risk_level is None or alert.get('risk_level', '') == risk_level:
                    alerts.append(alert)

        return alerts

    # ========== 系统统计 ==========

    def get_system_stats(self) -> Dict[str, Any]:
        """获取完整系统统计"""

        stats = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'total_operations': 0,
            'total_devices': 0,
            'avg_habit_match': 0.0,
            'operation_types_distribution': {},
            'time_range': {'first': '', 'last': ''},
            'sync_summary': {'total_syncs': 0, 'successful': 0, 'conflicts': 0},
            'verification_summary': {'total_verifications': 0, 'approved': 0, 'rejected': 0}
        }

        # 操作统计
        if self.ledger_file.exists():
            operations = []
            with open(self.ledger_file, 'r', encoding='utf-8') as f:
                for line in f:
                    operations.append(json.loads(line))

            stats['total_operations'] = len(operations)

            if operations:
                devices = set(op.get('device_id', '') for op in operations)
                stats['total_devices'] = len(devices)

                avg_match = sum(op.get('habit_fingerprint_match', 0) for op in operations) / len(operations)
                stats['avg_habit_match'] = round(avg_match, 4)

                # 操作类型分布
                op_type_counter = Counter(op.get('operation_type', '未知') for op in operations)
                stats['operation_types_distribution'] = dict(op_type_counter)

                # 时间范围
                stats['time_range']['first'] = operations[0].get('timestamp', '')
                stats['time_range']['last'] = operations[-1].get('timestamp', '')

        # 同步统计
        sync_history = self.get_sync_history(limit=1000)
        if sync_history:
            stats['sync_summary']['total_syncs'] = len(sync_history)
            successful = sum(1 for s in sync_history if s.get('status', '') == 'success')
            stats['sync_summary']['successful'] = successful
            stats['sync_summary']['conflicts'] = len(self.get_conflicts())

        # 验证统计
        verify_history = self.get_multisig_verification_history(limit=1000)
        if verify_history:
            stats['verification_summary']['total_verifications'] = len(verify_history)
            approved = sum(1 for v in verify_history if v.get('verdict', '') == 'approved')
            rejected = sum(1 for v in verify_history if v.get('verdict', '') == 'rejected')
            stats['verification_summary']['approved'] = approved
            stats['verification_summary']['rejected'] = rejected

        return stats

    # ========== 报告生成 ==========

    def generate_audit_report(self, days: int = 7) -> Dict[str, Any]:
        """
        生成审计报告

        包含: 操作统计·习惯分析·安全事件·合规性
        """

        report = {
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'period_days': days,
            'summary': self.get_system_stats(),
            'habit_analysis': self.analyze_habit_fingerprint(),
            'habit_trend': self.get_habit_trend(days=days),
            'device_summary': self.get_device_summary(),
            'recent_conflicts': self.get_conflicts()[-10:],
            'security_alerts': self.get_multisig_alerts(),
            'compliance': {
                'hash_chain_verified': self._verify_hash_chain(),
                'no_duplicate_ids': self._check_no_duplicates(),
                'timestamps_monotonic': self._check_timestamps_monotonic()
            }
        }

        return report

    def _verify_hash_chain(self) -> bool:
        """验证 SHA-256 链完整性"""
        if not self.ledger_file.exists():
            return True

        with open(self.ledger_file, 'r', encoding='utf-8') as f:
            operations = [json.loads(line) for line in f]

        for i in range(1, len(operations)):
            parent = operations[i].get('parent_hash', '')
            expected = operations[i - 1].get('hash_sha256', '')
            if parent and expected and parent != expected:
                return False

        return True

    def _check_no_duplicates(self) -> bool:
        """检查无重复操作ID"""
        if not self.ledger_file.exists():
            return True

        ids = set()
        with open(self.ledger_file, 'r', encoding='utf-8') as f:
            for line in f:
                op = json.loads(line)
                op_id = op.get('operation_id', '')
                if op_id in ids:
                    return False
                ids.add(op_id)

        return True

    def _check_timestamps_monotonic(self) -> bool:
        """检查时间戳递增"""
        if not self.ledger_file.exists():
            return True

        prev_ts = ''
        with open(self.ledger_file, 'r', encoding='utf-8') as f:
            for line in f:
                op = json.loads(line)
                ts = op.get('timestamp', '')
                if prev_ts and ts < prev_ts:
                    return False
                prev_ts = ts

        return True


# CLI示例
if __name__ == "__main__":
    tool = QueryTool()

    print("🔍 系统查询引擎 CLI")
    print("=" * 60)

    # 示例1: 系统统计
    print("\n1️⃣ 系统统计:")
    stats = tool.get_system_stats()
    print(f"   总操作数: {stats['total_operations']}")
    print(f"   总设备数: {stats['total_devices']}")
    print(f"   平均习惯匹配: {stats['avg_habit_match']:.2%}")
    print(f"   操作类型分布: {stats['operation_types_distribution']}")

    # 示例2: 操作日记查询
    print("\n2️⃣ 最近操作 (最多10条):")
    recent = tool.query_operations(limit=10)
    for op in recent[-3:]:
        print(f"   {op['operation_id']}: {op.get('operation_type', '未知')} @ {op.get('timestamp', '')[:10]}")

    # 示例3: 习惯指纹分析
    print("\n3️⃣ 习惯指纹分析:")
    habits = tool.analyze_habit_fingerprint()
    if habits:
        print(f"   拼音错别字: {list(habits.get('typos', {}).keys())}")
        print(f"   口头禅: {list(habits.get('catchphrases', {}).keys())}")
        print(f"   信心度: {habits.get('confidence_metrics', {}).get('overall_si', 0):.2%}")

    # 示例4: 习惯趋势
    print("\n4️⃣ 习惯趋势 (最近7天):")
    trend = tool.get_habit_trend(days=7)
    for date, count in trend.items():
        print(f"   {date}: {count} 次操作")

    # 示例5: 设备统计
    print("\n5️⃣ 设备统计:")
    devices = tool.get_device_summary()
    for device_id, stats_dict in devices.items():
        print(f"   {device_id}: {stats_dict['operation_count']} 次·平均匹配 {stats_dict['avg_habit_match']:.2%}")

    # 示例6: 同步历史
    print("\n6️⃣ 同步历史 (最近5次):")
    sync_history = tool.get_sync_history(limit=5)
    for sync in sync_history[-3:]:
        print(f"   {sync['timestamp'][:16]}: {sync.get('status', '未知')}")

    # 示例7: 审计报告
    print("\n7️⃣ 审计报告摘要:")
    report = tool.generate_audit_report(days=7)
    compliance = report['compliance']
    print(f"   哈希链完整: {'✅' if compliance['hash_chain_verified'] else '❌'}")
    print(f"   无重复ID: {'✅' if compliance['no_duplicate_ids'] else '❌'}")
    print(f"   时间戳递增: {'✅' if compliance['timestamps_monotonic'] else '❌'}")

    # 示例8: 安全警报
    print("\n8️⃣ 安全警报:")
    alerts = tool.get_multisig_alerts()
    if alerts:
        critical = [a for a in alerts if a.get('risk_level', '') == 'critical']
        print(f"   🔴 Critical: {len(critical)} 个")
    else:
        print(f"   ✅ 无警报")

