# adapters/dataset_adapter.py
"""
龍魂审计数据集适配器
DNA: #龍芯⚡️2026-08-25-DATASET-ADAPTER-v1.0-UID9622
"""
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List


class DatasetAdapter:
    """加载并预处理龍魂审计数据集"""

    def __init__(self, dataset_path: str):
        self.dataset_path = Path(dataset_path)

    def load(self) -> List[Dict[str, Any]]:
        """加载数据集（支持 .jsonl 和 .json）"""
        if not self.dataset_path.exists():
            raise FileNotFoundError(f"数据集不存在: {self.dataset_path}")

        records = []
        with open(self.dataset_path, "r", encoding="utf-8") as f:
            if self.dataset_path.suffix == ".jsonl":
                for line in f:
                    line = line.strip()
                    if line:
                        records.append(json.loads(line))
            else:
                records = json.load(f)
        return records

    def get_expected_verdicts(
        self, records: List[Dict], field: str = "verdict"
    ) -> List[str]:
        """提取期望判定列表"""
        return [r.get(field, "unknown") for r in records]

    def get_rejection_families(self, records: List[Dict]) -> Dict[str, int]:
        """统计 rejection_reason 家族分布（仅拒绝类记录）"""
        reasons = [
            r.get("rejection_reason", "untagged")
            for r in records
            if r.get("verdict") in ["reject", "deny", "block", "refuse"]
        ]
        return dict(Counter(reasons))

    def split_by_config(
        self, records: List[Dict], config_field: str = "config"
    ) -> Dict[str, List[Dict]]:
        """按 Config 分组"""
        groups: Dict[str, List[Dict]] = {}
        for r in records:
            key = r.get(config_field, "unknown")
            groups.setdefault(key, []).append(r)
        return groups

    def summary(self, records: List[Dict]) -> Dict[str, Any]:
        """数据集基本统计"""
        total = len(records)
        verdicts = Counter(r.get("verdict", "unknown") for r in records)
        configs = Counter(r.get("config", "unknown") for r in records)
        return {
            "total": total,
            "verdict_distribution": dict(verdicts),
            "config_distribution": dict(configs),
            "rejection_families": self.get_rejection_families(records),
        }
