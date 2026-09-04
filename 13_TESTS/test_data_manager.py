#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-TEST-DATA-MGR-UID9622
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
🐉 龍魂 · 测试数据管理 v1.1
功能: 生成、脱敏、版本控制测试数据（仅测试环境 LONGHUN_HOME 隔离区）
"""

import json
import random
from pathlib import Path
from datetime import datetime

# 测试数据脱敏：姓名/手机号/身份证 → 假数据（不触碰真实数据）
MASKED_NAMES = ["测试一", "测试二", "测试三"]


class TestDataManager:
    """测试数据管理器"""

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def generate_memory_data(self, count: int = 100) -> dict:
        """生成测试记忆数据（脱敏）"""
        data = {
            "entries": [],
            "dna": "#龍芯⚡️丙午·丙酉·丙寅·申时-TEST-DATA-UID9622",
            "generated_at": datetime.now().isoformat()
        }

        for i in range(count):
            data["entries"].append({
                "id": i,
                "content": f"测试记忆条目 {i}",
                "author": random.choice(MASKED_NAMES),
                "tags": random.sample(["test", "memory", "knowledge", "audit"], 2),
                "timestamp": datetime.now().isoformat()
            })

        return data

    def save(self, name: str, data: dict) -> Path:
        """保存测试数据"""
        filepath = self.data_dir / f"{name}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return filepath

    def load(self, name: str) -> dict:
        """加载测试数据"""
        filepath = self.data_dir / f"{name}.json"
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}


def _self_test():
    """自带冒烟（无 pytest 依赖也可直接运行）"""
    tmp = Path("/tmp/longhun_test_data_selfcheck")
    mgr = TestDataManager(tmp)
    data = mgr.generate_memory_data(count=5)
    path = mgr.save("sample", data)
    loaded = mgr.load("sample")
    assert loaded.get("dna", "").startswith("#龍芯⚡️"), "DNA缺失"
    assert len(loaded["entries"]) == 5, "条目数不符"
    import shutil
    shutil.rmtree(tmp, ignore_errors=True)
    print("✅ test_data_manager 自检通过")


if __name__ == "__main__":
    _self_test()
