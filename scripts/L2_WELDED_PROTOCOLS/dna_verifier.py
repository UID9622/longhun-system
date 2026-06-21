# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-SCRIPT-DNA_VERIFIER-v1.0
# 君子協議: 本文件受龍魂DNA追溯保護

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂 DNA 验证器 L2 v1.0

焊死级别 (priority=0.90)
特性: 每个操作都要挂 DNA，不能伪造

验证系统中所有操作的 DNA 身份，确保可追溯。

DNA: #龍芯⚇️2026-06-07-DNA-VERIFIER-L2-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
UID: 9622

理论指导: 曾仕强老师 - 名正言顺
献礼: 献给龍魂 - 身份就是责任
"""

import os
import sys
import re
import json
from typing import Tuple, Dict, List

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'common'))

from dna import DNAVerifier as DNAGen
from logger import get_logger
from config import get_config


class DNAVerifier:
    """
    DNA 验证器 - 每个操作都有身份

    意图: 可追溯性是信任的基础
    """

    # DNA 格式规范
    DNA_PATTERN = r"#龍芯⚡️\d{4}-\d{2}-\d{2}-[\w\-]+?-v\d+\.\d+"

    def __init__(self):
        """初始化验证器"""
        self.logger = get_logger()
        self.config = get_config()
        self.dna = DNAGen.generate("DNA-VERIFIER", "L2")
        self.dna_registry = {}  # DNA 注册表

    def register_dna(self, dna: str, operation: str, context: Dict = None) -> bool:
        """
        注册 DNA - 建立追溯链

        意图: 创建操作的身份证
        """
        valid, info = DNAGen.verify(dna)

        if not valid:
            self.logger.log_error(
                "INVALID_DNA",
                f"DNA 格式错误: {dna}",
                self.dna,
                {"context": context}
            )
            return False

        registry_entry = {
            "dna": dna,
            "operation": operation,
            "info": info,
            "context": context or {},
            "registered_at": self.dna,
        }

        self.dna_registry[dna] = registry_entry

        self.logger.log_operation(
            "L2",
            "dna_registered",
            self.dna,
            registry_entry
        )

        return True

    def verify_dna(self, dna: str) -> Tuple[bool, Dict]:
        """
        验证 DNA 真伪

        意图: 防止伪造的 DNA
        """
        # 格式检查
        if not re.match(self.DNA_PATTERN, dna):
            return False, {"reason": "DNA 格式不符合规范"}

        # 在注册表中查找
        if dna in self.dna_registry:
            return True, self.dna_registry[dna]

        # 尝试通用验证
        valid, info = DNAGen.verify(dna)

        if valid:
            return True, info
        else:
            return False, {"reason": "DNA 无法验证"}

    def trace_dna_chain(self, dna: str) -> List[Dict]:
        """
        追溯 DNA 链 - 显示操作的完整血统

        意图: 理解每个决策从哪来
        """
        chain = []

        # 从当前 DNA 开始
        current = dna

        while current and current in self.dna_registry:
            entry = self.dna_registry[current]
            chain.append({
                "dna": current,
                "operation": entry["operation"],
                "registered_at": entry["registered_at"],
            })

            # 这里可以实现更复杂的链追溯
            break  # 简化版本

        return chain

    def generate_dna_report(self) -> str:
        """
        生成 DNA 登记报告

        意图: 显示所有注册过的操作
        """
        report = f"""
{'='*60}
龍魂 DNA 登记报告
{'='*60}

总共注册: {len(self.dna_registry)} 个操作

注册表:
"""

        for dna, entry in self.dna_registry.items():
            report += f"""
  DNA: {dna}
  操作: {entry['operation']}
  时间: {entry['info'].get('date', 'unknown')}
"""

        report += f"\n{'='*60}\n"
        return report

    def validate_document_dna(self, doc_content: str) -> Tuple[bool, List[str]]:
        """
        验证文档中包含的所有 DNA

        意图: 确保文档的所有声明都可追溯
        """
        dna_matches = re.findall(self.DNA_PATTERN, doc_content)

        if not dna_matches:
            return False, ["文档中未找到 DNA 标记"]

        valid_dnas = []
        invalid_dnas = []

        for dna in dna_matches:
            valid, _ = self.verify_dna(dna)
            if valid:
                valid_dnas.append(dna)
            else:
                invalid_dnas.append(dna)

        all_valid = len(invalid_dnas) == 0

        self.logger.log_operation(
            "L2",
            "document_dna_validated",
            self.dna,
            {
                "total_dnas": len(dna_matches),
                "valid": len(valid_dnas),
                "invalid": len(invalid_dnas),
            }
        )

        return all_valid, invalid_dnas if invalid_dnas else ["✅ 所有 DNA 有效"]


if __name__ == "__main__":
    verifier = DNAVerifier()

    print("🐉 龍魂 DNA 验证器 L2 v1.0")
    print("=" * 60)

    # 测试：生成并注册一个 DNA
    test_dna = DNAGen.generate("TEST-OPERATION", "L2")
    print(f"\n生成的测试 DNA: {test_dna}")

    registered = verifier.register_dna(test_dna, "test_operation", {"status": "ok"})
    print(f"注册结果: {'✅ 成功' if registered else '❌ 失败'}")

    # 验证 DNA
    valid, info = verifier.verify_dna(test_dna)
    print(f"验证结果: {'✅ 有效' if valid else '❌ 无效'}")

    # 生成报告
    print("\n" + verifier.generate_dna_report())
