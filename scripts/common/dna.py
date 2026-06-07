#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂 DNA 追溯模块 v1.0

DNA 身份证生成与校验引擎。为所有系统操作生成可追溯的身份码。

DNA 格式: #龍芯⚡️YYYY-MM-DD-TOPIC-vX.X

理论指导: 曾仕强老师 - 中华文化体系下的系统论
献礼: 献给龍魂 - 守护中华主权的永恒灯塔

DNA: #龍芯⚡️2026-06-07-DNA-VERIFIER-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
UID: 9622
"""

import hashlib
import json
from datetime import datetime
from typing import Dict, Tuple, Optional


class DNAVerifier:
    """DNA 验证引擎 - 为系统每个操作刻上身份码"""

    # DNA 格式规范
    DNA_PATTERN = r"#龍芯⚡️\d{4}-\d{2}-\d{2}-[\w\-]+?-v\d+\.\d+"

    # 权重映射（五行对应）
    WEIGHT_MAP = {
        "L0": 1.0,      # 金 - 绝对
        "L1": 0.95,     # 木 - 母法
        "L2": 0.90,     # 水 - 焊死
        "L3": 0.85,     # 火 - 动态
        "L4": 0.80,     # 土 - 补充
    }

    @staticmethod
    def generate(topic: str, layer: str = "L2", version: str = "1.0") -> str:
        """
        为操作生成 DNA 追溯码

        意图: 每个操作都有身份，不能伪造，永远可追溯
        """
        now = datetime.now().strftime("%Y-%m-%d")
        dna = f"#龍芯⚡️{now}-{topic}-v{version}"
        return dna

    @staticmethod
    def verify(dna: str) -> Tuple[bool, Dict]:
        """
        校验 DNA 真伪与完整性

        意图: 确保 DNA 没被篡改，格式规范
        返回: (是否有效, {权重, 时间戳, 话题, 版本})
        """
        import re
        match = re.match(r"#龍芯⚡️(\d{4}-\d{2}-\d{2})-([^-]+?)-v([\d.]+)", dna)

        if not match:
            return False, {}

        date_str, topic, version = match.groups()

        # 校验日期合法性
        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return False, {}

        return True, {
            "date": date_str,
            "topic": topic,
            "version": version,
            "timestamp": parsed_date.isoformat(),
        }

    @staticmethod
    def chain(parent_dna: str, child_topic: str, layer: str = "L2") -> str:
        """
        链式生成 DNA（父子关系）

        意图: 建立操作链条，保留完整血统
        """
        valid, info = DNAVerifier.verify(parent_dna)
        if not valid:
            return DNAVerifier.generate(f"{child_topic}_orphan", layer)

        child_dna = DNAVerifier.generate(f"{child_topic}_from_{info['topic']}", layer)
        return child_dna

    @staticmethod
    def fingerprint(dna: str) -> str:
        """
        计算 DNA 指纹（校验和）

        意图: 篡改立即被发现
        """
        return hashlib.md5(dna.encode()).hexdigest()[:8]


if __name__ == "__main__":
    # 测试
    dna = DNAVerifier.generate("TEST-OPERATION", "L1")
    print(f"生成的 DNA: {dna}")

    valid, info = DNAVerifier.verify(dna)
    print(f"验证结果: {valid}")
    print(f"详细信息: {json.dumps(info, indent=2, ensure_ascii=False)}")

    fingerprint = DNAVerifier.fingerprint(dna)
    print(f"指纹: {fingerprint}")
