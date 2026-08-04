#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🧬 龍魂 DNA 格式校验器 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UID9622 · 诸葛鑫 · 龍芯北辰
DNA:#龍芯⚡️2026-05-17-DNA-VALIDATOR-FILE1-v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

功能: 校验主控页所有 DNA、确认码、版本号一致性

用法:
  python3 dna_validator.py --check-page <page_url>
  python3 dna_validator.py --fix-all <page_url>
"""

import json
import re
from datetime import datetime
from typing import List, Dict, Tuple, Any

class DNAValidator:
    """DNA 格式校验器"""

    def __init__(self):
        self.config_path = '~/.龍魂/decision_page_config.json'
        self.dna_pattern = r'#龍芯⚡️\d{4}-\d{2}-\d{2}-[\w\-·]+?-v[\d\.]+'
        self.confirm_pattern = r'#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z'
        self.seal_pattern = r'#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL'

        self.errors = []
        self.warnings = []
        self.fixes = []

    def validate_dna_format(self, dna_string: str) -> Tuple[bool, str]:
        """校验单个 DNA 格式"""
        if not re.match(self.dna_pattern, dna_string):
            error = f"❌ DNA 格式错误: {dna_string}"
            self.errors.append(error)
            return False, error

        # 提取日期部分
        match = re.search(r'(\d{4})-(\d{2})-(\d{2})', dna_string)
        if match:
            try:
                year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
                datetime(year, month, day)
            except ValueError:
                error = f"⚠️  DNA 日期无效: {dna_string}"
                self.warnings.append(error)
                return False, error

        return True, "✅ DNA 格式正确"

    def validate_confirm_code(self, text: str) -> List[str]:
        """校验确认码齐全性"""
        matches = re.findall(self.confirm_pattern, text)
        if not matches:
            warning = "⚠️  确认码缺失"
            self.warnings.append(warning)
            return []
        return matches

    def check_version_consistency(self, text: str) -> Dict[str, Any]:
        """检查版本号一致性"""
        versions = re.findall(r'v[\d\.]+', text)
        version_counts = {}

        for v in versions:
            version_counts[v] = version_counts.get(v, 0) + 1

        # 警告：出现多个不同版本
        if len(version_counts) > 1:
            warning = f"⚠️  版本号不统一，检测到: {list(version_counts.keys())}"
            self.warnings.append(warning)

        return version_counts

    def generate_fix_suggestions(self, text: str) -> List[str]:
        """生成修复建议"""
        suggestions = []

        # 建议 1: 统一版本号
        versions = self.check_version_consistency(text)
        if len(versions) > 1:
            suggestions.append(f"🔧 将所有版本统一为 v2.7.36（当前主版本）")

        # 建议 2: 检查重复的说明文本
        if text.count('§S-25-EXT-3-5 不假装记忆律·覆盖率坦白') > 3:
            suggestions.append(f"🔧 将覆盖率声明改为宏调用 {{COVERAGE_STATEMENT}}")

        # 建议 3: 检查确认码
        if not re.search(self.confirm_pattern, text):
            suggestions.append(f"🔧 添加缺失的确认码: {self.confirm_pattern}")

        return suggestions

    def validate_text(self, text: str) -> Dict[str, Any]:
        """校验整段文本"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "dna_count": len(re.findall(self.dna_pattern, text)),
            "confirm_count": len(re.findall(self.confirm_pattern, text)),
            "version_distribution": self.check_version_consistency(text),
            "errors": self.errors,
            "warnings": self.warnings,
            "suggestions": self.generate_fix_suggestions(text),
            "status": "🟢 通过" if not self.errors else "🔴 失败"
        }

        return report

def main():
    validator = DNAValidator()

    # 示例: 校验一段 DNA
    sample_dna = "#龍芯⚡️2026-05-17-DECISION-PAGE-AUTO-OPTIMIZATION-v1.0"
    is_valid, msg = validator.validate_dna_format(sample_dna)

    print(f"DNA 校验: {msg}")
    print(f"格式有效: {is_valid}")

if __name__ == '__main__':
    main()
