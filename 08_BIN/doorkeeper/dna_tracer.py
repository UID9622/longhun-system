#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂DNA追溯链 v1.0
DNA: #龍芯⚡️2026-08-25-DNA-TRACER-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
功能：区块链式 DNA 追溯，sha256 prev_hash 链接，支持链完整性验证
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List


class DNATracer:
    def __init__(self, chain_dir: str = None):
        # 默认落在 longhun-system/08_STATE/dna-chain/，而非仓库根散落
        if chain_dir is None:
            chain_dir = str(Path.home() / "longhun-system" / "08_STATE" / "dna-chain")
        self.chain_dir = Path(chain_dir)
        self.chain_dir.mkdir(parents=True, exist_ok=True)
        self.chain_file = self.chain_dir / "dna_chain.json"
        self.创始人UID = "9622"
        self.系统名称 = "龍魂系统"
        self.当前版本 = "v1.0"
        self.chain: List[Dict] = self._load_chain()

    def _load_chain(self) -> List[Dict]:
        if self.chain_file.exists():
            try:
                with open(self.chain_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_chain(self):
        with open(self.chain_file, 'w', encoding='utf-8') as f:
            json.dump(self.chain, f, ensure_ascii=False, indent=2)

    def _generate_hash(self, data: str) -> str:
        return hashlib.sha256(data.encode('utf-8')).hexdigest()[:16]

    def stamp(
        self,
        event: str,
        level: str = "🟢",
        service: str = "",
        port: int = 0,
        additional_data: Optional[Dict] = None
    ) -> str:
        timestamp = datetime.now()
        timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        prev_hash = self.chain[-1]["hash"] if self.chain else "0" * 16

        block_data = {
            "timestamp": timestamp_str,
            "event": event,
            "level": level,
            "service": service,
            "port": port,
            "prev_hash": prev_hash,
            "uid": self.创始人UID,
            "version": self.当前版本,
            "additional": additional_data or {}
        }

        block_str = json.dumps(block_data, sort_keys=True, ensure_ascii=False)
        current_hash = self._generate_hash(block_str)
        # 事件名截断+清理，生成合法DNA码
        event_slug = event[:20].replace(' ', '-').replace('/', '-')
        dna_code = f"#龍芯⚡️{timestamp.strftime('%Y%m%d')}-{event_slug}-UID{self.创始人UID}"

        block = {
            "dna": dna_code,
            "hash": current_hash,
            "prev_hash": prev_hash,
            "timestamp": timestamp_str,
            "event": event,
            "level": level,
            "service": service,
            "port": port,
            "uid": self.创始人UID
        }

        self.chain.append(block)
        self._save_chain()
        return dna_code

    def verify_chain(self) -> Dict[str, Any]:
        """验证区块链完整性（prev_hash 链接校验）"""
        if not self.chain:
            return {"valid": True, "message": "空链", "total_blocks": 0}
        errors = []
        for i in range(1, len(self.chain)):
            if self.chain[i]["prev_hash"] != self.chain[i - 1]["hash"]:
                errors.append({"block_index": i, "error": "prev_hash不匹配"})
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "total_blocks": len(self.chain)
        }

    def get_events_by_level(self, level: str) -> List[Dict]:
        return [b for b in self.chain if b["level"] == level]

    def get_last_n(self, n: int = 10) -> List[Dict]:
        return self.chain[-n:]

    def export_summary(self) -> Dict:
        return {
            "total": len(self.chain),
            "red": len(self.get_events_by_level("🔴")),
            "yellow": len(self.get_events_by_level("🟡")),
            "green": len(self.get_events_by_level("🟢")),
            "last_event": self.chain[-1] if self.chain else None,
            "chain_valid": self.verify_chain()["valid"]
        }


# 全局单例（守护进程共享同一条链）
dna = DNATracer()
