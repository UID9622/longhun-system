#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH 中文原生脚本運行時 · 通心譯執行引擎
Chinese Native Script Runtime · TongXinYi Execution Engine

DNA: #龍芯⚡️2026-06-16-CNSH-RUNTIME-v1.0
責任: UID9622·不免責

核心信念：
  英文不是唯一計算機執行的指令。
  CNSH 用中文語法承載意圖，運行時透過通心譯將其解釋為可執行代碼，
  支持 Python 作為首選目標語言，並保留中文語義之心。

用法：
  python3 cnsh_runner.py examples/hello.cnsh
  python3 cnsh_runner.py examples/hello.cnsh --explain
  python3 cnsh_runner.py examples/hello.cnsh --target python
"""

import argparse
import ast
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class CNSHRuntimeError(Exception):
    """CNSH 運行時錯誤"""
    pass


class TongXinYiTranslator:
    """
    通心譯雙語轉換器
    負責將 CNSH 中文關鍵字/標點解釋為目標語言符號，同時保留中文意圖註釋。
    """

    def __init__(self, dict_path: Optional[Path] = None):
        self.dict_path = dict_path or self._default_dict_path()
        self.data = self._load_dict()
        self.keywords: Dict[str, str] = self.data.get("keywords", {})
        self.punct: Dict[str, str] = self.data.get("punctuation_equivalents", {})
        self.builtins: Dict[str, str] = self.data.get("builtins", {})
        self.methods: Dict[str, str] = self.data.get("common_methods", {})
        self.tongxinyi_terms: Dict[str, str] = self.data.get("tongxinyi_terms", {})

    @staticmethod
    def _default_dict_path() -> Path:
        return Path(__file__).parent / "dictionaries" / "cnsh_to_python.json"

    def _load_dict(self) -> Dict:
        try:
            with open(self.dict_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as exc:
            raise CNSHRuntimeError(f"無法載入 CNSH 字典: {self.dict_path}: {exc}")

    def explain_line(self, line: str) -> str:
        """
        對單行代碼進行通心譯解釋：保留中文心，輸出外殼含義。
        返回一行註釋形式的解釋。
        """
        parts = []
        # 檢測通心譯專屬術語
        for cn, en in self.tongxinyi_terms.items():
            if cn in line:
                parts.append(f"{cn}→{en}")
        # 檢測關鍵字映射
        for cn, py in self.keywords.items():
            if re.search(rf"\b{re.escape(cn)}\b", line) and cn not in self.tongxinyi_terms:
                parts.append(f"{cn}→{py}")
        if not parts:
            return "# 語句保持原意執行"
        return "# 通心譯: " + "; ".join(parts[:5])


class CNSHInterpreter:
    """
    CNSH 解釋器：將 .cnsh 源代碼轉譯為 Python 並執行。
    """

    def __init__(self, translator: Optional[TongXinYiTranslator] = None):
        self.translator = translator or TongXinYiTranslator()
        self.source_lines: List[str] = []
        self.translated_lines: List[str] = []

    def translate(self, source: str, add_explanations: bool = False) -> str:
        """
        將 CNSH 源碼轉譯為 Python。
        """
        self.source_lines = source.splitlines()
        self.translated_lines = []

        for idx, raw_line in enumerate(self.source_lines, 1):
            line = raw_line.rstrip()
            if not line.strip():
                self.translated_lines.append("")
                continue

            # 跳過純註釋行（保留）
            if line.strip().startswith("#"):
                self.translated_lines.append(line)
                continue

            translated = self._translate_line(line)

            if add_explanations:
                explanation = self.translator.explain_line(raw_line)
                self.translated_lines.append(f"{explanation}")

            self.translated_lines.append(translated)

        return "\n".join(self.translated_lines)

    def _translate_line(self, line: str) -> str:
        """逐行轉譯：保護字符串，轉譯關鍵字、標點、內建函數、方法。"""
        # 提取並保護字符串字面量
        string_placeholders: Dict[str, str] = {}
        placeholder_idx = 0

        def protect_string(match: re.Match) -> str:
            nonlocal placeholder_idx
            key = f"__CNSH_STR_{placeholder_idx}__"
            string_placeholders[key] = match.group(0)
            placeholder_idx += 1
            return key

        # 匹配單引號或雙引號字符串，含 f-string / r-string
        line = re.sub(r"[frbu]*(?:'[^'\\]*(?:\\.[^'\\]*)*'|\"[^\"\\]*(?:\\.[^\"\\]*)*\")", protect_string, line)

        result = line

        # 1. 轉譯關鍵字
        multi_char = sorted(
            [kv for kv in self.translator.keywords.items() if len(kv[0]) >= 2],
            key=lambda x: -len(x[0])
        )
        for cn, py in multi_char:
            result = result.replace(cn, py)

        single_char = [kv for kv in self.translator.keywords.items() if len(kv[0]) == 1]
        for cn, py in single_char:
            result = re.sub(rf"(?<![\u4e00-\u9fa5]){re.escape(cn)}(?![\u4e00-\u9fa5])", py, result)

        # 2. 轉譯標點
        for cn_punct, py_punct in self.translator.punct.items():
            result = result.replace(cn_punct, py_punct)

        # 3. 轉譯內建函數調用（後面接左括號）
        for cn, py in sorted(self.translator.builtins.items(), key=lambda x: -len(x[0])):
            result = re.sub(rf"(?<![\u4e00-\u9fa5]){re.escape(cn)}(?=\s*\()", py, result)

        # 4. 轉譯方法調用（.方法()）
        for cn, py in sorted(self.translator.methods.items(), key=lambda x: -len(x[0])):
            result = re.sub(rf"\.{re.escape(cn)}(?=\s*\()", f".{py}", result)

        # 恢復字符串字面量
        for key, original in string_placeholders.items():
            result = result.replace(key, original)

        return result

    def validate(self, code: str) -> None:
        """用 AST 檢查轉譯後代碼語法是否合法。"""
        try:
            ast.parse(code)
        except SyntaxError as exc:
            raise CNSHRuntimeError(
                f"轉譯後 Python 語法錯誤 (行 {exc.lineno}): {exc.msg}\n"
                f"{exc.text}"
            )

    def execute(self, source: str, add_explanations: bool = False, globals_dict: Optional[Dict] = None) -> Dict:
        """
        執行 CNSH 源碼：轉譯、驗證、運行。
        """
        python_code = self.translate(source, add_explanations=add_explanations)
        self.validate(python_code)

        # 沙盒執行環境
        safe_globals = globals_dict or {
            "__name__": "__cnsh__",
            "__file__": "<cnsh>",
        }
        safe_globals["__builtins__"] = __builtins__

        try:
            exec(python_code, safe_globals)
        except Exception as exc:
            raise CNSHRuntimeError(f"CNSH 執行錯誤: {type(exc).__name__}: {exc}")

        return {
            "translated_code": python_code,
            "globals": safe_globals,
        }


def run_file(path: Path, explain: bool = False, show_code: bool = False, dry_run: bool = False) -> None:
    """運行單個 .cnsh 文件。"""
    if not path.exists():
        raise CNSHRuntimeError(f"文件不存在: {path}")

    source = path.read_text(encoding="utf-8")
    interpreter = CNSHInterpreter()

    print(f"🐉 CNSH 通心譯執行引擎")
    print(f"   源碼: {path}")
    print(f"   DNA: #龍芯⚡️2026-06-16-CNSH-RUNTIME-v1.0")
    print()

    if dry_run:
        python_code = interpreter.translate(source, add_explanations=explain)
        print("=== 轉譯後的 Python 代碼（不干運行）===")
        print(python_code)
        return

    result = interpreter.execute(source, add_explanations=explain)

    if show_code or explain:
        print("=== 轉譯後的 Python 代碼 ===")
        print(result["translated_code"])
        print()

    print("✅ 執行完成")


def run_repl() -> None:
    """CNSH 交互式解釋器（簡易 REPL）。"""
    interpreter = CNSHInterpreter()
    print("🐉 CNSH 交互式通心譯解釋器")
    print("   輸入 '退出' 或 'exit' 結束")
    print()

    buffer: List[str] = []
    while True:
        prompt = "... " if buffer else ">>> "
        try:
            line = input(prompt)
        except EOFError:
            print()
            break

        if line.strip().lower() in ("退出", "exit", "quit"):
            break

        buffer.append(line)
        source = "\n".join(buffer)

        # 嘗試執行，若語法不完整則繼續讀入
        try:
            python_code = interpreter.translate(source)
            ast.parse(python_code)
            buffer = []
            result = interpreter.execute(source)
        except (SyntaxError, CNSHRuntimeError):
            continue

    print("👋 再會")


def main():
    parser = argparse.ArgumentParser(description="CNSH 中文原生脚本運行時")
    parser.add_argument("file", nargs="?", type=Path, help="要執行的 .cnsh 文件")
    parser.add_argument("--explain", action="store_true", help="輸出通心譯解釋註釋")
    parser.add_argument("--show-code", action="store_true", help="顯示轉譯後的 Python 代碼")
    parser.add_argument("--dry-run", action="store_true", help="僅轉譯不執行")
    parser.add_argument("--repl", action="store_true", help="進入交互式模式")
    args = parser.parse_args()

    if args.repl:
        run_repl()
    elif args.file:
        run_file(args.file, explain=args.explain, show_code=args.show_code, dry_run=args.dry_run)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
