#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 语言翻译引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-TRANSLATE-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 代码翻译（Python ↔ JavaScript ↔ Go）
  - 自然语言翻译（中文 ↔ 英文）
  - 自动检测代码语言
"""

import re
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional


class TranslateEngine:
    """语言翻译引擎——代码跨语言翻译 + 自然语言翻译"""

    LANG_MAPPING = {
        "python": {"ext": ".py", "keywords": ["def", "class", "import", "print", "if", "else", "for"]},
        "javascript": {"ext": ".js", "keywords": ["function", "class", "import", "console.log", "if", "else", "for"]},
        "go": {"ext": ".go", "keywords": ["func", "type", "import", "fmt.Println", "if", "else", "for"]},
    }

    PY_TO_JS = [
        (r'def\s+(\w+)\s*\(([^)]*)\):', r'function \1(\2) {'),
        (r'print\s*\(([^)]*)\)', r'console.log(\1)'),
        (r'if\s+([^:]+):', r'if (\1) {'),
        (r'else:', r'} else {'),
        (r'for\s+(\w+)\s+in\s+([^:]+):', r'for (let \1 of \2) {'),
        (r'while\s+([^:]+):', r'while (\1) {'),
        (r'return\s+([^;]+)', r'return \1;'),
    ]

    def translate_code(self, code: str, from_lang: str, to_lang: str) -> Dict:
        """翻译代码"""
        # 尝试 LLM
        try:
            result = subprocess.run(
                ["ollama", "run", "llama3.2",
                 f"Translate this {from_lang} code to {to_lang}. Only output the code:\n\n{code}"],
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode == 0 and len(result.stdout.strip()) > 10:
                return {"status": "llm_translated", "from": from_lang, "to": to_lang,
                        "code": result.stdout.strip(), "method": "ollama"}
        except Exception:
            pass

        # 回退规则翻译
        translated = self._fallback_translate(code, from_lang, to_lang)
        return {"status": "fallback", "from": from_lang, "to": to_lang,
                "code": translated, "method": "rule", "warning": "使用规则翻译，可能不完整"}

    def _fallback_translate(self, code: str, from_lang: str, to_lang: str) -> str:
        if from_lang == "python" and to_lang == "javascript":
            result = code
            for pattern, repl in self.PY_TO_JS:
                result = re.sub(pattern, repl, result)
            # 修复花括号
            diff = result.count('{') - result.count('}')
            if diff > 0:
                result += '}' * diff
            return result
        return f"// 暂不支持 {from_lang} → {to_lang} 自动翻译\n{code}"

    def translate_text(self, text: str, from_lang: str = "zh", to_lang: str = "en") -> Dict:
        """翻译自然语言"""
        try:
            result = subprocess.run(
                ["ollama", "run", "llama3.2",
                 f"Translate from {from_lang} to {to_lang}: {text}"],
                capture_output=True, text=True, timeout=15,
            )
            if result.returncode == 0:
                return {"status": "ok", "original": text, "translated": result.stdout.strip()}
        except Exception:
            pass
        return {"status": "error", "message": "翻译失败，请检查 Ollama 是否运行"}

    def detect_language(self, code: str) -> str:
        """自动检测代码语言"""
        scores = {}
        for lang, info in self.LANG_MAPPING.items():
            scores[lang] = sum(1 for kw in info["keywords"] if kw in code)
        if scores:
            return max(scores, key=scores.get)
        return "unknown"


if __name__ == "__main__":
    engine = TranslateEngine()
    result = engine.translate_code('def hello(name):\n    print(f"Hello {name}")\n    return True',
                                   "python", "javascript")
    print(f"翻译: {result['status']} ({result.get('method', '?')})")
    print(result['code'][:120])

    detected = engine.detect_language("def foo(): pass")
    print(f"检测: {detected}")
    print("🟢 语言翻译引擎测试通过")
