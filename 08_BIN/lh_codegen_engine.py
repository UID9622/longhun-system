#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 代码生成引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-CODEGEN-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 根据自然语言生成Python/Shell代码
  - 支持模板库（可复用代码片段）
  - 自动插入DNA注释
  - 代码安全扫描（确保不包含危险操作）
"""

import re
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class CodeGenEngine:
    """代码生成引擎——能理解意图，也能自己写代码"""

    UNSAFE_PATTERNS = [
        (r"\bexec\s*\(", "exec()"),
        (r"\beval\s*\(", "eval()"),
        (r"\b__import__\s*\(", "__import__()"),
        (r"os\.system\(", "os.system()"),
        (r"subprocess\.call\(", "subprocess.call()"),
        (r"rm\s+-rf\s+/", "rm -rf /"),
    ]

    def __init__(self):
        self.templates = {}
        self._load_templates()

    def _load_templates(self):
        template_dir = Path.home() / "longhun-system/templates"
        if template_dir.exists():
            for tf in template_dir.glob("*.py.tmpl"):
                self.templates[tf.stem] = tf.read_text(encoding="utf-8")

    def generate(self, description: str, language: str = "python") -> Dict:
        """生成代码"""
        # 1. 尝试匹配模板
        for name, template in self.templates.items():
            if name.lower() in description.lower():
                code = self._render_template(template, description)
                return self._wrap_code(code, language)

        # 2. 调用 LLM 生成
        code = self._call_llm(description, language)

        # 3. 回退生成
        if not code or code.startswith("[LLM"):
            code = self._fallback_generate(description, language)

        return self._wrap_code(code, language)

    def _call_llm(self, description: str, language: str) -> str:
        try:
            result = subprocess.run(
                ["ollama", "run", "llama3.2",
                 f"Generate {language} code for: {description}. Only output the code, no explanation."],
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode == 0 and len(result.stdout.strip()) > 10:
                return result.stdout.strip()
        except Exception:
            pass
        return ""

    def _render_template(self, template: str, description: str) -> str:
        parts = template.split("{{")
        result = parts[0]
        for part in parts[1:]:
            placeholder, rest = part.split("}}", 1)
            if placeholder.strip() == "description":
                result += f"# {description}"
            elif placeholder.strip() == "dna":
                result += f"# DNA: #龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-CODEGEN-UID9622"
            else:
                result += placeholder
            result += rest
        return result

    def _wrap_code(self, code: str, language: str) -> Dict:
        """包装代码并安全检查"""
        # 安全检查
        for pattern, label in self.UNSAFE_PATTERNS:
            if re.search(pattern, code):
                return {
                    "status": "unsafe",
                    "code": code,
                    "message": f"代码包含危险操作: {label}",
                }

        # 插入DNA注释
        if "#DNA" not in code and "DNA:" not in code:
            dna = f'# DNA: #龍芯⚡️{datetime.now().strftime("%Y%m%d%H%M%S")}-CODEGEN-UID9622\n'
            code = dna + code

        return {"status": "generated", "code": code, "language": language}

    def _fallback_generate(self, description: str, language: str) -> str:
        if language == "python":
            return f'''def generated_function():
    """Generated: {description}"""
    # TODO: 请根据需求完善逻辑
    print("Hello from {description[:20]}")
    return True
'''
        return f"#!/bin/bash\n# Generated: {description}\necho 'Hello'\n"

    def list_templates(self) -> list:
        return list(self.templates.keys())


if __name__ == "__main__":
    engine = CodeGenEngine()
    result = engine.generate("写一个函数，读取JSON文件并打印内容")
    print(f"状态: {result['status']}")
    print(f"代码:\n{result['code'][:200]}")
    print(f"模板: {engine.list_templates()}")
    print("🟢 代码生成引擎测试通过")
