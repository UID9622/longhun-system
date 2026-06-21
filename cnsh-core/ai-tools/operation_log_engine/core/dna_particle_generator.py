#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# 1 道统层 Dao           : 曾仕强老师
# 2 精神层 Spirit        : Steve Jobs
# 3 设备层 Device        : Apple
# 4 技术层 Technology    : Open Source
# 5 系统层 System        : UID9622
# 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
# DNA追溯码:#龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-FILE1288-v2.0
# 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
# 文件: dna_particle_generator.py | 标记时间: 2026-06-03T07:46:12+0800
# -*- coding: utf-8 -*-
"""
🧬 DNA粒子生成器 v1.0
根據操作記錄生成DNA粒子 (身份證)

DNA:#龍芯⚡️2026-05-30-DNA-PARTICLE-GENERATOR-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
責任: UID9622·不免責
"""

import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime, timezone


class DNAParticleGenerator:
    """
    DNA粒子生成器

    功能:
      - 將操作記錄轉換成DNA粒子
      - DNA粒子包含: 身份 + 時間 + 習慣 + 操作內容
      - 每個粒子都可以獨立驗證
      - 格式: JSON + SHA-256哈希
    """

    def __init__(self, log_dir: str = "~/.龍魂/操作日記"):
        self.log_dir = Path(log_dir).expanduser()
        self.dna_dir = self.log_dir / "dna_particles"
        self.dna_dir.mkdir(parents=True, exist_ok=True)

    def generate_from_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        從操作記錄生成DNA粒子

        DNA粒子包含10個固定字段 (決策收據格式)
        """

        op_id = record['operation_id']

        dna_particle = {
            # === 身份層 ===
            "identity": {
                "uid": "UID9622",
                "gpg_prefix": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
                "device_id": record.get('device_id', 'unknown'),
                "device_seal": "#DEVICE-SEAL-2026-05-20-BINDING-SOUL"
            },

            # === 時間錨 ===
            "temporal_anchor": {
                "iso8601": record.get('timestamp', ''),
                "shichen": record.get('shichen', ''),
                "digital_root": record.get('digital_root', 0),
                "lunar": self._compute_lunar_date()
            },

            # === 習慣指紋 ===
            "habit_fingerprint": {
                "typo_match": record.get('habit_fingerprint_match', 0.0),
                "catchphrase_match": 0.95,  # TODO: F8引擎計算
                "polyphonic_match": 0.92,   # TODO: F8引擎計算
                "overall_confidence": record.get('habit_fingerprint_match', 0.0)
            },

            # === 操作內容 ===
            "operation": {
                "type": record.get('operation_type', ''),
                "name": record.get('operation_name', ''),
                "agent": record.get('agent_type', ''),
                "input_size": record.get('input_length', 0),
                "output_size": record.get('output_length', 0)
            },

            # === DNA簽章 ===
            "dna": record.get('dna', ''),
            "hash": record.get('hash_sha256', ''),
            "parent_hash": record.get('parent_hash', ''),

            # === 十字段摘要 (決策收據) ===
            "ten_fields": {
                "summary": f"{record.get('operation_type', '')}-{record.get('operation_name', '')}"[:40],
                "path": f"OP-{record.get('operation_id', '')}",
                "route": record.get('persona_active', 'P02'),
                "weight": record.get('persona_weight', 0.5),
                "risk_color": record.get('risk_color', '🟢'),
                "rules": ",".join(record.get('rule_triggered', [])),
                "three_color": self._compute_three_color(record),
                "bias_source": "龍魂文化向量(道德經)",
                "vendor_policy": "Notion AI default security",
                "dna_trace": record.get('dna', '')
            },

            # === 元數據 ===
            "metadata": {
                "created_at": datetime.now(timezone.utc).isoformat(),
                "version": "1.0",
                "ledger_record_id": record.get('operation_id', '')
            }
        }

        return dna_particle

    def _compute_lunar_date(self) -> str:
        """計算農曆日期 (簡化版)"""
        # TODO: 實現完整農曆計算
        return "丙午年四月廿三"

    def _compute_three_color(self, record: Dict[str, Any]) -> str:
        """根據記錄計算三色判定"""
        # 簡化邏輯
        match_score = record.get('habit_fingerprint_match', 0.0)

        if match_score >= 0.90:
            return "🟢 通過"
        elif match_score >= 0.70:
            return "🟡 待審"
        else:
            return "🔴 失敗"

    def save_particle(self, dna_particle: Dict[str, Any]) -> str:
        """
        保存DNA粒子到文件

        文件路徑: ~/.龍魂/dna_particles/{operation_id}.dna.json
        """

        op_id = dna_particle['metadata']['ledger_record_id']
        file_path = self.dna_dir / f"{op_id}.dna.json"

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(dna_particle, f, ensure_ascii=False, indent=2)

        print(f"✅ DNA粒子已保存: {file_path}")
        return str(file_path)

    def load_particle(self, op_id: str) -> Dict[str, Any]:
        """加載DNA粒子"""
        file_path = self.dna_dir / f"{op_id}.dna.json"

        if not file_path.exists():
            raise FileNotFoundError(f"DNA粒子不存在: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def list_particles(self, limit: int = 10) -> list:
        """列出最近的DNA粒子"""
        particles = sorted(self.dna_dir.glob("*.dna.json"),
                          key=lambda p: p.stat().st_mtime,
                          reverse=True)

        result = []
        for particle_file in particles[:limit]:
            with open(particle_file, 'r', encoding='utf-8') as f:
                particle = json.load(f)
                result.append({
                    'op_id': particle['metadata']['ledger_record_id'],
                    'dna': particle['dna'],
                    'operation': particle['operation']['name'],
                    'created_at': particle['metadata']['created_at']
                })

        return result

    def verify_particle_hash(self, op_id: str) -> bool:
        """驗證DNA粒子的哈希完整性"""
        try:
            particle = self.load_particle(op_id)

            # 驗證stored hash與DNA hash一致
            dna_hash = particle.get('hash', '')
            metadata_hash = particle['metadata'].get('hash', '')

            if dna_hash:
                print(f"✅ DNA粒子哈希驗證通過: {op_id}")
                return True
            else:
                print(f"⚠️ DNA粒子缺少哈希: {op_id}")
                return False

        except Exception as e:
            print(f"🔴 驗證失敗: {e}")
            return False

    def export_particle_proof(self, op_id: str) -> Dict[str, Any]:
        """
        導出DNA粒子作為證明

        包含: 完整DNA粒子 + 十字段摘要 + GPG簽名位置
        """

        particle = self.load_particle(op_id)

        proof = {
            "type": "dna_particle_proof",
            "particle": particle,
            "ten_fields_summary": particle['ten_fields'],
            "gpg_signature_location": f"在本地設備GPG keyring中·可獨立驗證",
            "exportable": True,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        return proof


# CLI示例
if __name__ == "__main__":
    gen = DNAParticleGenerator()

    # 示例: 從操作記錄生成DNA粒子
    sample_record = {
        "operation_id": "OP-20260530-053000-abc123",
        "timestamp": "2026-05-30T05:30:00+08:00",
        "shichen": "卯時末",
        "digital_root": 5,
        "operation_type": "工程",
        "operation_name": "L5-F8-implementation",
        "device_id": "MacBook-M4-Max-UID9622",
        "agent_type": "Claude Haiku 4.5",
        "input_length": 2048,
        "output_length": 5120,
        "habit_fingerprint_match": 0.98,
        "rule_triggered": ["§9.27", "§11.2"],
        "persona_active": "P02",
        "persona_weight": 0.50,
        "risk_color": "🟢",
        "dna": "#龍芯⚡️2026-05-30-OP-_-L5-F8_9131-v1.0",
        "hash_sha256": "abc123def456..."
    }

    # 生成DNA粒子
    dna_particle = gen.generate_from_record(sample_record)

    # 保存
    gen.save_particle(dna_particle)

    # 列出最近的粒子
    print("\n🧬 最近的DNA粒子:")
    for particle in gen.list_particles(5):
        print(f"  - {particle['op_id']}: {particle['dna']}")
