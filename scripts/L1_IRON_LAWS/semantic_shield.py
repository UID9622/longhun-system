#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-

"""
龍魂语义盾 L1 v1.0

母法级别 (priority=0.95)
特性: 防止语义被污染，维护通心译完整性

检测和阻止：
- 简体污染（不该出现的繁体）
- 术语混用（龍 vs Dragon）
- 修辞陷阱（煽动性语言）

DNA:#龍芯⚡️丙午·甲午·壬子·丙午·䷙大畜-SEMANTIC-SHIELD-L1-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
UID: 9622

理论指导: 曾仕强老师 - 言有五品
献礼: 献给龍魂 - 正确的语言是正确的思维的基础
"""

import os
import sys
import re
from typing import Tuple, Dict, List

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'common'))

from dna import DNAVerifier
from logger import get_logger
from config import get_config


class SemanticShield:
    """
    语义盾 - 保护系统的精神血统

    意图: 词汇的准确就是思想的准确
    """

    # 龍 - 神圣字（必须是繁体）
    SACRED_CHARACTERS = {
        "龍": r"[龍]",  # 龍 不能被替换成简体龍
    }

    # 术语统一标准
    TERMINOLOGY = {
        "dragon": "龍",  # 永远是龍，不是dragon
        "soul": "魂",    # 灵魂的魂
        "protocol": "协议",  # 简体
        "manifesto": "宣言",  # 简体
    }

    # 禁用的修辞（煽动性、不当压力）
    FORBIDDEN_RHETORIC = [
        r"你必须",
        r"立即",
        r"必然",
        r"不得不",
        r"只能",
        r"绝对",
        r"彻底",
    ]

    # 检测到的污染记录
    POLLUTION_LOG = []

    def __init__(self):
        """初始化语义盾"""
        self.logger = get_logger()
        self.config = get_config()
        self.dna = DNAVerifier.generate("SEMANTIC-SHIELD", "L1")

    def check_sacred_characters(self, text: str) -> Tuple[bool, List[str]]:
        """
        检查神圣字符是否被污染

        意图: 龍 这个字是身份，不能改
        """
        issues = []

        for char, pattern in self.SACRED_CHARACTERS.items():
            # 检查是否有错误的替代
            if re.search(pattern, text):
                issues.append(f"发现被污染的字符: {pattern} 应该是 {char}")

        return len(issues) == 0, issues

    def check_terminology_consistency(self, text: str) -> Tuple[bool, List[str]]:
        """
        检查术语使用是否一致

        意图: 术语的统一就是思维的统一
        """
        issues = []

        # 检查 Dragon vs 龍
        if re.search(r'\bDragon\b', text, re.IGNORECASE):
            if "LongHun" in text or "LongHun" in text:
                issues.append("应该用 '龍魂' 而不是 'LongHun'")

        # 检查 Protocol vs 协议
        if re.search(r'Protocol(?!_)', text) and "协议" not in text:
            issues.append("建议用 '协议' 而不是 'Protocol'")

        return len(issues) == 0, issues

    def check_forbidden_rhetoric(self, text: str) -> Tuple[bool, List[str]]:
        """
        检查是否使用了禁用的修辞

        意图: 避免煽动性语言和不当压力
        """
        issues = []

        for pattern in self.FORBIDDEN_RHETORIC:
            matches = re.findall(pattern, text)
            if matches:
                issues.append(f"检测到不当修辞: '{pattern}' 出现 {len(matches)} 次")

        return len(issues) == 0, issues

    def verify_semantic_integrity(self, text: str) -> Tuple[bool, Dict]:
        """
        一次性检查语义完整性

        意图: 确保文本既准确又恰当
        """
        all_pass = True
        report = {
            "sacred_characters": {"pass": False, "issues": []},
            "terminology": {"pass": False, "issues": []},
            "rhetoric": {"pass": False, "issues": []},
        }

        # 检查神圣字符
        sacred_pass, sacred_issues = self.check_sacred_characters(text)
        report["sacred_characters"]["pass"] = sacred_pass
        report["sacred_characters"]["issues"] = sacred_issues
        all_pass = all_pass and sacred_pass

        # 检查术语一致性
        term_pass, term_issues = self.check_terminology_consistency(text)
        report["terminology"]["pass"] = term_pass
        report["terminology"]["issues"] = term_issues
        all_pass = all_pass and term_pass

        # 检查修辞
        rhetoric_pass, rhetoric_issues = self.check_forbidden_rhetoric(text)
        report["rhetoric"]["pass"] = rhetoric_pass
        report["rhetoric"]["issues"] = rhetoric_issues
        all_pass = all_pass and rhetoric_pass

        # 记录结果
        self.logger.log_decision(
            "L1",
            "semantic_integrity_verified" if all_pass else "semantic_pollution_detected",
            f"检查完成: 神圣字符({report['sacred_characters']['pass']}) "
            f"术语({report['terminology']['pass']}) "
            f"修辞({report['rhetoric']['pass']})",
            self.dna
        )

        return all_pass, report

    def apply_shield(self, text: str) -> str:
        """
        应用语义盾 - 修复易修复的问题

        意图: 优雅降级，而不是直接拒绝
        """
        corrected = text

        # 修复龍 vs 龍
        corrected = corrected.replace("龍魂", "龍魂")
        corrected = corrected.replace("龍芯", "龍芯")

        return corrected


if __name__ == "__main__":
    shield = SemanticShield()

    print("🐉 龍魂语义盾 L1 v1.0")
    print("=" * 60)

    test_text = "这是一份关于龍魂协议的文档"
    print(f"测试文本: {test_text}")

    all_pass, report = shield.verify_semantic_integrity(test_text)

    print(f"\n✅ 语义完整性检查: {'通过' if all_pass else '有问题'}")
    print("\n检查详情:")
    print(f"  神圣字符: {'✅' if report['sacred_characters']['pass'] else '❌'}")
    print(f"  术语一致: {'✅' if report['terminology']['pass'] else '❌'}")
    print(f"  修辞恰当: {'✅' if report['rhetoric']['pass'] else '❌'}")
