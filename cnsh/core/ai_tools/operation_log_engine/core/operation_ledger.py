#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# 1 道统层 Dao           : 曾仕强老师
# 2 精神层 Spirit        : Steve Jobs
# 3 设备层 Device        : Apple
# 4 技术层 Technology    : Open Source
# 5 系统层 System        : UID9622
# 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
# DNA追溯码:#龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-FILE1291-v2.0
# 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
# 文件: operation_ledger.py | 标记时间: 2026-06-03T07:46:12+0800
# -*- coding: utf-8 -*-
"""
🐉 龍魂操作日记核心引擎 v1.0
操作日记 = append-only ledger + DNA粒子 + 习惯指纹追踪

DNA:#龍芯⚡️2026-05-30-OPERATION-LEDGER-CORE-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
责任: UID9622·不免责
"""

import json
import hashlib
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, List
import re


class OperationLedger:
    """
    操作日记核心引擎

    特性:
      - append-only: 每次操作追加·不可修改
      - SHA-256链: 每操作记录parent_hash·无断裂
      - DNA粒子: 自动生成身份证
      - 习惯追踪: 自动提取拼音错别字·口头禅
    """

    def __init__(self, log_dir: str = "~/.龍魂/操作日记"):
        self.log_dir = Path(log_dir).expanduser()
        self.ledger_file = self.log_dir / "operation_ledger.jsonl"
        self.dna_dir = self.log_dir / "dna_particles"
        self.habit_dir = self.log_dir / "habit_fingerprints"

        # 确保目录存在
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.dna_dir.mkdir(parents=True, exist_ok=True)
        self.habit_dir.mkdir(parents=True, exist_ok=True)

    def _get_last_hash(self) -> Optional[str]:
        """获取上一个操作的hash (用于链接)"""
        if not self.ledger_file.exists():
            return None

        try:
            with open(self.ledger_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if not lines:
                    return None
                last_record = json.loads(lines[-1])
                return last_record.get('hash_sha256')
        except Exception as e:
            print(f"⚠️ 读取最后hash失败: {e}")
            return None

    def _compute_hash(self, data: Dict[str, Any]) -> str:
        """计算记录的SHA-256 hash"""
        # 去掉hash和parent_hash本身·计算内容hash
        hash_data = {k: v for k, v in data.items()
                     if k not in ['hash_sha256', 'parent_hash']}
        json_str = json.dumps(hash_data, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(json_str.encode('utf-8')).hexdigest()

    def _extract_habits(self, text: str) -> Dict[str, Any]:
        """从操作描述中提取习惯特征"""
        habits = {
            'typos': {},
            'catchphrases': [],
            'polyphonic': {},
            'punctuation_patterns': []
        }

        # 常见拼音错别字检测
        typo_map = {
            '得': ['的'],
            '哪': ['那'],
            '行': ['xíng', 'háng'],  # 多音字
            '中': ['zhōng', 'zhòng'],
        }

        for correct, variants in typo_map.items():
            for variant in variants:
                if variant in text:
                    habits['typos'][correct] = variant

        # 口头禅检测
        catchphrases_list = ['嘿嘿', '焊死', '宝宝', ',,,', '。。。', '...']
        for phrase in catchphrases_list:
            count = text.count(phrase)
            if count > 0:
                habits['catchphrases'].append({
                    'phrase': phrase,
                    'count': count
                })

        # 逗号连点习惯
        comma_runs = re.findall(r',{2,}', text)
        if comma_runs:
            habits['punctuation_patterns'].append({
                'type': 'comma_run',
                'count': len(comma_runs),
                'avg_length': sum(len(r) for r in comma_runs) / len(comma_runs)
            })

        return habits

    def _get_shichen(self) -> str:
        """获取当前时辰"""
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
        hour = datetime.now().hour
        return shichen_map.get(hour, '未知时')

    def _get_digital_root(self) -> int:
        """计算当前日期的数字根 (1-9)"""
        date_str = datetime.now().strftime('%Y%m%d')
        total = sum(int(d) for d in date_str)
        while total >= 10:
            total = sum(int(d) for d in str(total))
        return total

    def append_operation(self,
                        operation_type: str,
                        operation_name: str,
                        device_id: str,
                        agent_type: str,
                        input_text: str = "",
                        output_text: str = "",
                        rules_triggered: List[str] = None,
                        persona_active: str = "P02",
                        persona_weight: float = 0.50,
                        notes: str = "") -> Dict[str, Any]:
        """
        追加一个操作到日记

        Args:
            operation_type: 操作类型 (焊接|工程|审计|压缩)
            operation_name: 操作名称 (如 L5-F8-implementation)
            device_id: 设备ID (如 MacBook-M4-Max-UID9622)
            agent_type: AI代理 (Claude Haiku 4.5)
            input_text: 输入文本
            output_text: 输出文本
            rules_triggered: 触发的规则列表
            persona_active: 当前人格 (P02/P05/P13等)
            persona_weight: 人格权重
            notes: 备注

        Returns:
            操作记录dict
        """

        # 生成操作ID
        op_id = f"OP-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"

        # 时间信息
        now = datetime.now(timezone.utc).astimezone(timezone(
            datetime.now().astimezone().utcoffset()
        ))
        timestamp = now.isoformat()
        shichen = self._get_shichen()
        digital_root = self._get_digital_root()

        # 习惯提取
        full_text = f"{input_text}\n{output_text}\n{notes}"
        habits = self._extract_habits(full_text)

        # 习惯匹配度 (暂时硬编码)
        habit_match = 0.98  # TODO: 实现F8匹配引擎

        # 构造记录
        record = {
            "operation_id": op_id,
            "timestamp": timestamp,
            "shichen": shichen,
            "digital_root": digital_root,
            "operation_type": operation_type,
            "operation_name": operation_name,
            "device_id": device_id,
            "agent_type": agent_type,
            "input_length": len(input_text),
            "output_length": len(output_text),
            "habit_fingerprint_match": habit_match,
            "habit_typos_detected": habits['typos'],
            "catchphrases": [p['phrase'] for p in habits['catchphrases']],
            "rule_triggered": rules_triggered or [],
            "persona_active": persona_active,
            "persona_weight": persona_weight,
            "risk_color": "🟢",  # 默认绿线
            "execution_time_ms": 245,  # TODO: 实际测量
            "status": "success",
            "dna": f"#龍芯⚡️{datetime.now().strftime('%Y%m%d-%H%M%S')}-OP-{operation_type}-{operation_name}-v1.0",
            "notes": notes
        }

        # 计算hash并添加链接
        record['hash_sha256'] = self._compute_hash(record)
        last_hash = self._get_last_hash()
        if last_hash:
            record['parent_hash'] = last_hash

        # 追加到ledger
        with open(self.ledger_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')

        print(f"✅ 操作已记录: {op_id}")
        print(f"   DNA: {record['dna']}")
        print(f"   Hash: {record['hash_sha256'][:16]}...")

        return record

    def get_last_n_operations(self, n: int = 10) -> List[Dict[str, Any]]:
        """获取最后N个操作"""
        if not self.ledger_file.exists():
            return []

        operations = []
        with open(self.ledger_file, 'r', encoding='utf-8') as f:
            for line in f:
                operations.append(json.loads(line))

        return operations[-n:]

    def verify_chain_integrity(self) -> bool:
        """验证SHA-256链的完整性 (无断裂)"""
        if not self.ledger_file.exists():
            return True

        operations = []
        with open(self.ledger_file, 'r', encoding='utf-8') as f:
            for line in f:
                operations.append(json.loads(line))

        for i, op in enumerate(operations):
            if i == 0:
                # 第一条记录不需要parent
                continue

            parent_hash = op.get('parent_hash')
            if parent_hash != operations[i-1]['hash_sha256']:
                print(f"🔴 链断裂在操作 {i}: {op['operation_id']}")
                return False

        print(f"✅ 链完整性验证通过 ({len(operations)}条记录)")
        return True

    def get_stats(self) -> Dict[str, Any]:
        """获取统计数据"""
        if not self.ledger_file.exists():
            return {
                'total_operations': 0,
                'average_habit_match': 0.0,
                'device_count': 0
            }

        operations = self.get_last_n_operations(n=1000)

        devices = set(op['device_id'] for op in operations)
        avg_match = sum(op['habit_fingerprint_match'] for op in operations) / len(operations) if operations else 0

        return {
            'total_operations': len(operations),
            'average_habit_match': round(avg_match, 4),
            'device_count': len(devices),
            'devices': list(devices)
        }


# CLI示例
if __name__ == "__main__":
    ledger = OperationLedger()

    # 追加测试操作
    record = ledger.append_operation(
        operation_type="工程",
        operation_name="L5-F8-implementation",
        device_id="MacBook-M4-Max-UID9622",
        agent_type="Claude Haiku 4.5",
        input_text="嘿嘿,,,帮我设计操作日记,,,我想同步本地",
        output_text="收到! 这是跨设备身份识别系统...",
        rules_triggered=["§9.27", "§11.2"],
        persona_active="P02",
        persona_weight=0.50,
        notes="操作日记系统Phase 2.1启动"
    )

    # 验证链
    ledger.verify_chain_integrity()

    # 统计
    print("\n📊 统计数据:")
    stats = ledger.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # 查看最近操作
    print("\n📋 最近5个操作:")
    for op in ledger.get_last_n_operations(5):
        print(f"  - {op['operation_id']}: {op['operation_name']}")
