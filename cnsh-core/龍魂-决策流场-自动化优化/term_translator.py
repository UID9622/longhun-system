#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 龍魂术语自动翻译器 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UID9622 · 诸葛鑫 · 龍芯北辰
DNA: #龍芯⚡️2026-05-17-TERM-TRANSLATOR-v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

功能: 在"老大语境"和"外人语境"之间自动转换术语

用法:
  python3 term_translator.py --mode internal <text>
  python3 term_translator.py --mode external <text>
  python3 term_translator.py --auto-convert <file.md>
"""

import json
import re
from typing import Dict, List

class TermTranslator:
    """术语翻译器"""

    def __init__(self):
        self.term_map = {
            "constraint": {
                "internal": "配合",
                "external": "铁律",
                "description": "系统约束"
            },
            "workflow": {
                "internal": "习惯做法",
                "external": "标准流程",
                "description": "工作方式"
            },
            "method": {
                "internal": "咋做",
                "external": "方法论",
                "description": "执行方式"
            },
            "requirement": {
                "internal": "得这样",
                "external": "必须项",
                "description": "强制要求"
            },
            "recommendation": {
                "internal": "建议",
                "external": "推荐实践",
                "description": "可选建议"
            }
        }

        # 构建反向映射
        self.internal_to_external = {}
        self.external_to_internal = {}

        for category, variants in self.term_map.items():
            internal = variants.get("internal", "")
            external = variants.get("external", "")
            if internal:
                self.internal_to_external[internal] = external
            if external:
                self.external_to_internal[external] = internal

    def translate_to_mode(self, text: str, target_mode: str) -> str:
        """将文本翻译到目标模式"""
        result = text

        if target_mode == "internal":
            # 外人语境 → 老大语境
            for external, internal in self.external_to_internal.items():
                result = re.sub(
                    rf'\b{re.escape(external)}\b',
                    internal,
                    result,
                    flags=re.IGNORECASE
                )
        elif target_mode == "external":
            # 老大语境 → 外人语境
            for internal, external in self.internal_to_external.items():
                result = re.sub(
                    rf'\b{re.escape(internal)}\b',
                    external,
                    result,
                    flags=re.IGNORECASE
                )

        return result

    def detect_mode(self, text: str) -> str:
        """检测文本所属模式"""
        internal_count = sum(1 for term in self.internal_to_external.keys() if term in text)
        external_count = sum(1 for term in self.external_to_internal.keys() if term in text)

        if internal_count > external_count:
            return "internal"
        elif external_count > internal_count:
            return "external"
        else:
            return "mixed"

    def generate_translation_report(self, text: str) -> Dict:
        """生成翻译报告"""
        internal_mode = self.translate_to_mode(text, "internal")
        external_mode = self.translate_to_mode(text, "external")

        return {
            "original_mode": self.detect_mode(text),
            "internal_version": internal_mode,
            "external_version": external_mode,
            "term_count": len(re.findall(r'\b(' + '|'.join(
                list(self.internal_to_external.keys()) +
                list(self.external_to_internal.keys())
            ) + r')\b', text))
        }

def main():
    translator = TermTranslator()

    # 示例文本
    sample = "龍魂系统遵循一套铁律，这些都是配合的原则。"

    print("📝 原文本:")
    print(f"  {sample}")
    print()

    internal_version = translator.translate_to_mode(sample, "internal")
    external_version = translator.translate_to_mode(sample, "external")

    print("🔄 老大语境版本:")
    print(f"  {internal_version}")
    print()

    print("🔄 外人语境版本:")
    print(f"  {external_version}")
    print()

    report = translator.generate_translation_report(sample)
    print("📊 翻译报告:")
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
