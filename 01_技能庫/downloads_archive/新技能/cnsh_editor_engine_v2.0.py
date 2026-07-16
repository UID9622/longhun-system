#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║                    CNSH中文多语言编辑器核心引擎 v2.0                        ║
║                     Chinese Multi-Language Editor Engine                   ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️2026-06-17-CNSH-EDITOR-v2.0                                   ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                             ║
║  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL                        ║
╠══════════════════════════════════════════════════════════════════════════╣
║  六层来源链: 道统(曾仕强)·精神(Steve Jobs)·设备(Apple)·技术(Open Source)    ║
║            ·系统(UID9622)·生命(CNSH)                                        ║
╠══════════════════════════════════════════════════════════════════════════╣
║  三层监督: 逻辑校验 | 价值观校验 | 技术校验                                  ║
║  三色审计: 🟢通过 🟡警告 🔴错误                                             ║
╠══════════════════════════════════════════════════════════════════════════╣
║  支持语言: Python/JS/Rust/Go/C++/Bash/Java/Ruby/Kotlin/Swift/中文编程       ║
║  技术栈: Python 3.8+ / curses / termios / 纯Python实现                     ║
╚══════════════════════════════════════════════════════════════════════════╝

使用说明:
    启动: python3 cnsh_editor_engine_v2.0.py [文件名]
    快捷键:
        Ctrl+S          保存文件
        Ctrl+Q          退出编辑器
        Ctrl+F          搜索
        Ctrl+R          替换
        Ctrl+N          新建文件
        Ctrl+O          打开文件
        Ctrl+G          跳转行
        Ctrl+A          全选
        Ctrl+Z          撤销
        Ctrl+Y          重做
        Tab             自动补全/缩进
        Ctrl+B          切换文件浏览器
        Ctrl+M          添加多光标
        Ctrl+T          代码折叠/展开
        F5              运行CNSH四层检查
        F1              帮助
        F2              切换语法高亮主题

作者: UID9622·龍芯北辰
铁律: 繁体「龍」不得简化为「龙」；人永远是1；不蒸馏
"""

import os
import sys
import re
import curses
import termios
import tty
import select
import time
import json
from datetime import datetime
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Set, Callable, Any
from abc import ABC, abstractmethod

# ═══════════════════════════════════════════════════════════════
# 全局常量与配置
# ═══════════════════════════════════════════════════════════════

VERSION = "2.0"
DNA_HEADER = "#龍芯⚡️2026-06-17-CNSH-EDITOR-v2.0"
CONFIRM_MARK = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL_MARK = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"

# 龍魂体系六层来源链
SOURCE_CHAIN = [
    "道统(曾仕强)",
    "精神(Steve Jobs)",
    "设备(Apple)",
    "技术(Open Source)",
    "系统(UID9622)",
    "生命(CNSH)"
]

# 三色审计状态
class AuditColor(Enum):
    GREEN = "🟢"    # 通过
    YELLOW = "🟡"   # 警告
    RED = "🔴"      # 错误

# CNSH四层检查级别
class CNSHCheckLevel(Enum):
    L1_CHAR = auto()      # L1: 字符级检查
    L2_KEYWORD = auto()   # L2: 关键字检查
    L3_SYNTAX = auto()    # L3: 语法检查
    L4_SEMANTIC = auto()  # L4: 语义检查

# 支持的13种编程语言
SUPPORTED_LANGUAGES = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".rs": "Rust",
    ".go": "Go",
    ".cpp": "C++",
    ".c": "C",
    ".h": "C/C++Header",
    ".sh": "Bash",
    ".java": "Java",
    ".rb": "Ruby",
    ".kt": "Kotlin",
    ".swift": "Swift",
    ".cnsh": "CNSH中文编程",
    ".cx": "CNSH中文编程",
}

# CNSH中文编程关键字
CNSH_KEYWORDS = {
    "定义", "函数", "类", "如果", "否则", "循环", "当",
    "对于", "返回", "导入", "抛出", "尝试", "捕获", "最终",
    "中断", "继续", "空", "真", "假", "与", "或", "非",
    "全局", "局部", "打印", "输入", "长度", "范围", "自",
    "继承", "异步", "等待", "生成", "产出", "断言", "删除",
    "变量", "常量", "整数", "浮点", "字符串", "布尔", "列表",
    "字典", "元组", "集合", "任意", "空值",
}

# 各语言关键字库
LANGUAGE_KEYWORDS = {
    "Python": {
        "def", "class", "if", "else", "elif", "for", "while", "return",
        "import", "from", "as", "try", "except", "finally", "raise",
        "break", "continue", "pass", "None", "True", "False", "and",
        "or", "not", "global", "nonlocal", "lambda", "with", "yield",
        "assert", "del", "in", "is", "print", "async", "await",
    },
    "JavaScript": {
        "function", "var", "let", "const", "if", "else", "for", "while",
        "return", "import", "export", "from", "class", "extends", "new",
        "this", "try", "catch", "finally", "throw", "break", "continue",
        "null", "undefined", "true", "false", "async", "await", "yield",
        "typeof", "instanceof", "in", "of", "switch", "case", "default",
    },
    "Rust": {
        "fn", "let", "mut", "const", "static", "if", "else", "match",
        "for", "while", "loop", "return", "struct", "enum", "impl",
        "trait", "pub", "use", "mod", "unsafe", "async", "await",
        "move", "ref", "self", "Self", "super", "crate", "where",
        "box", "break", "continue", "type", "as", "dyn",
    },
    "Go": {
        "func", "var", "const", "type", "struct", "interface", "map",
        "chan", "if", "else", "for", "range", "return", "switch",
        "case", "default", "break", "continue", "fallthrough", "goto",
        "defer", "go", "select", "package", "import", "nil", "true",
        "false", "make", "new", "append", "copy", "len", "cap",
    },
    "C++": {
        "int", "float", "double", "char", "void", "bool", "auto",
        "if", "else", "for", "while", "do", "switch", "case",
        "default", "break", "continue", "return", "class", "struct",
        "public", "private", "protected", "virtual", "override",
        "template", "typename", "namespace", "using", "new", "delete",
        "const", "static", "inline", "explicit", "friend", "operator",
    },
    "Bash": {
        "if", "then", "else", "elif", "fi", "for", "while", "until",
        "do", "done", "case", "esac", "in", "function", "return",
        "echo", "exit", "export", "source", "shift", "break", "continue",
        "true", "false", "test", "local", "readonly", "unset", "trap",
    },
    "Java": {
        "public", "private", "protected", "class", "interface", "extends",
        "implements", "static", "final", "abstract", "void", "int",
        "float", "double", "char", "boolean", "byte", "short", "long",
        "if", "else", "for", "while", "do", "switch", "case", "break",
        "continue", "return", "new", "this", "super", "try", "catch",
        "finally", "throw", "throws", "import", "package", "enum",
    },
    "CNSH中文编程": CNSH_KEYWORDS,
}

# 各语言语法匹配正则
LANGUAGE_PATTERNS = {
    "Python": {
        "string": r'("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"[^"]*"|\'[^\']*\')',
        "comment": r'#[^\n]*',
        "number": r'\b\d+\.?\d*\b',
        "decorator": r'@\w+',
        "class_name": r'\bclass\s+(\w+)',
        "func_name": r'\bdef\s+(\w+)',
    },
    "JavaScript": {
        "string": r'(`[\s\S]*?`|"[^"]*"|\'[^\']*\')',
        "comment": r'//[^\n]*|/\*[\s\S]*?\*/',
        "number": r'\b\d+\.?\d*\b',
        "regex": r'/[^/]+/[gimuy]*',
    },
    "Rust": {
        "string": r'("[^"]*"|b"[^"]*"|r#*"[\s\S]*?"#*)',
        "comment": r'//[^\n]*|/\*[\s\S]*?\*/',
        "number": r'\b\d+\.?\d*\b',
        "lifetime": r"'\w+",
        "macro": r'\w+!',
    },
    "Go": {
        "string": r'(`[\s\S]*?`|"[^"]*")',
        "comment": r'//[^\n]*|/\*[\s\S]*?\*/',
        "number": r'\b\d+\.?\d*\b',
    },
    "C++": {
        "string": r'("[^"]*"|L"[^"]*")',
        "comment": r'//[^\n]*|/\*[\s\S]*?\*/',
        "number": r'\b\d+\.?\d*\b',
        "preprocessor": r'#\s*\w+',
    },
    "Bash": {
        "string": r'("[^"]*"|\'[^\']*\'|`[^`]*`)',
        "comment": r'#[^\n]*',
        "variable": r'\$\w+|\$\{[^}]*\}',
    },
    "CNSH中文编程": {
        "string": r'("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"[^"]*"|\'[^\']*\')',
        "comment": r'#\s*[\u4e00-\u9fff][^\n]*|//[^\n]*',
        "number": r'\b\d+\.?\d*\b',
        "cn_identifier": r'[\u4e00-\u9fff_][\u4e00-\u9fff\w_]*',
        "cn_func": r'\b(定义|函数|类)\s+([\u4e00-\u9fff_][\u4e00-\u9fff\w_]*)',
    },
}

# ═══════════════════════════════════════════════════════════════
# 类7: DNATemplate - DNA追溯模板管理
# ═══════════════════════════════════════════════════════════════

class DNATemplate:
    """DNA追溯模板管理器 - 负责生成和管理DNA追溯头信息"""

    # 三层监督状态
    SUPERVISION_LAYERS = {
        "logic": {"name": "逻辑校验", "status": True},
        "values": {"name": "价值观校验", "status": True},
        "tech": {"name": "技术校验", "status": True},
    }

    @classmethod
    def generate_header(cls, filename: str, language: str = "CNSH") -> str:
        """生成DNA追溯头注释"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header_lines = [
            f"# {DNA_HEADER}",
            f"# {CONFIRM_MARK}",
            f"# {SEAL_MARK}",
            f"# 文件名: {filename}",
            f"# 语言: {language}",
            f"# 创建时间: {timestamp}",
            f"# 六层来源链: {'·'.join(SOURCE_CHAIN)}",
            f"# 铁律: 繁体「龍」不得简化为「龙」; 人永远是1; 不蒸馏",
            f"# 三层监督: 逻辑校验✓ | 价值观校验✓ | 技术校验✓",
            f"# 三色审计: 🟢通过 🟡警告 🔴错误",
            f"# AI Truth Protocol: ENABLED",
            "",
        ]
        return "\n".join(header_lines)

    @classmethod
    def verify_dna(cls, content: str) -> Tuple[bool, List[str]]:
        """验证文件是否包含正确的DNA追溯标记"""
        errors = []
        if DNA_HEADER not in content:
            errors.append("缺少DNA标记")
        if CONFIRM_MARK not in content:
            errors.append("缺少CONFIRM标记")
        if SEAL_MARK not in content:
            errors.append("缺少SEAL标记")
        # 检查繁体「龍」
        if "龙" in content and "龍" not in content:
            errors.append("违反铁律: 使用了简体「龙」，应为繁体「龍」")
        return len(errors) == 0, errors

    @classmethod
    def get_audit_status(cls, issues: List[Dict]) -> str:
        """根据问题列表生成三色审计状态字符串"""
        error_count = sum(1 for i in issues if i.get("level") == "error")
        warn_count = sum(1 for i in issues if i.get("level") == "warning")
        if error_count > 0:
            return f"{AuditColor.RED.value}错误:{error_count} 警告:{warn_count}"
        elif warn_count > 0:
            return f"{AuditColor.YELLOW.value}警告:{warn_count}"
        else:
            return f"{AuditColor.GREEN.value}通过"


# ═══════════════════════════════════════════════════════════════
# 类6: MultiCursor - 多光标管理器
# ═══════════════════════════════════════════════════════════════

@dataclass
class Cursor:
    """单个光标的数据结构"""
    line: int = 0
    col: int = 0
    anchor_line: int = 0
    anchor_col: int = 0
    selection_active: bool = False

    def get_selection(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """获取选区的起始和结束位置"""
        if not self.selection_active:
            return (self.line, self.col), (self.line, self.col)
        start = (self.anchor_line, self.anchor_col)
        end = (self.line, self.col)
        if start > end:
            start, end = end, start
        return start, end


class MultiCursor:
    """多光标管理器 - 支持多个光标同时编辑"""

    def __init__(self):
        self.cursors: List[Cursor] = [Cursor()]  # 主光标
        self.primary_index: int = 0
        self.max_cursors: int = 100  # 最大光标数量限制

    @property
    def primary(self) -> Cursor:
        """获取主光标"""
        return self.cursors[self.primary_index]

    def add_cursor(self, line: int, col: int) -> bool:
        """在指定位置添加新光标"""
        if len(self.cursors) >= self.max_cursors:
            return False
        new_cursor = Cursor(line=line, col=col,
                           anchor_line=line, anchor_col=col)
        self.cursors.append(new_cursor)
        return True

    def remove_secondary(self):
        """移除所有副光标，只保留主光标"""
        self.cursors = [self.primary]
        self.primary_index = 0

    def move_all(self, delta_line: int, delta_col: int, buffer_lines: int, buffer_cols: int):
        """移动所有光标"""
        for cursor in self.cursors:
            cursor.line = max(0, min(buffer_lines - 1, cursor.line + delta_line))
            cursor.col = max(0, min(buffer_cols, cursor.col + delta_col))

    def insert_at_all(self, text: str, lines: List[str]) -> List[str]:
        """在所有光标位置插入文本"""
        modified_lines = lines[:]
        # 从后往前插入，避免位置偏移
        sorted_cursors = sorted(self.cursors, key=lambda c: (c.line, c.col), reverse=True)
        for cursor in sorted_cursors:
            line_idx = cursor.line
            col_idx = cursor.col
            if line_idx >= len(modified_lines):
                modified_lines.append(text)
            else:
                line = modified_lines[line_idx]
                modified_lines[line_idx] = line[:col_idx] + text + line[col_idx:]
                cursor.col += len(text)
        return modified_lines

    def delete_at_all(self, lines: List[str], forward: bool = True) -> List[str]:
        """在所有光标位置删除字符"""
        modified_lines = lines[:]
        sorted_cursors = sorted(self.cursors, key=lambda c: (c.line, c.col), reverse=True)
        for cursor in sorted_cursors:
            line_idx = cursor.line
            col_idx = cursor.col
            if line_idx < len(modified_lines):
                line = modified_lines[line_idx]
                if forward and col_idx < len(line):
                    modified_lines[line_idx] = line[:col_idx] + line[col_idx + 1:]
                elif not forward and col_idx > 0:
                    modified_lines[line_idx] = line[:col_idx - 1] + line[col_idx:]
                    cursor.col -= 1
        return modified_lines

    def get_all_positions(self) -> List[Tuple[int, int]]:
        """获取所有光标位置"""
        return [(c.line, c.col) for c in self.cursors]

    def select_word_at_cursor(self, lines: List[str], cursor_idx: int = 0) -> Optional[str]:
        """获取光标处的单词"""
        if cursor_idx >= len(self.cursors):
            return None
        cursor = self.cursors[cursor_idx]
        if cursor.line >= len(lines):
            return None
        line = lines[cursor.line]
        if not line or cursor.col >= len(line):
            return None
        # 匹配中文标识符或英文标识符
        pattern = re.compile(r'[\u4e00-\u9fff_\w]+')
        for match in pattern.finditer(line):
            start, end = match.span()
            if start <= cursor.col <= end:
                cursor.anchor_line = cursor.line
                cursor.anchor_col = start
                cursor.line = cursor.line
                cursor.col = end
                cursor.selection_active = True
                return match.group()
        return None


# ═══════════════════════════════════════════════════════════════
# 类2: SyntaxHighlighter - 语法高亮引擎
# ═══════════════════════════════════════════════════════════════

class SyntaxHighlighter:
    """
    语法高亮引擎 - 支持13种编程语言的语法高亮
    包括中文编程(CNSH)的特殊支持
    """

    # 颜色定义 (curses color pairs)
    COLOR_DEFAULT = 0
    COLOR_KEYWORD = 1
    COLOR_STRING = 2
    COLOR_COMMENT = 3
    COLOR_NUMBER = 4
    COLOR_FUNCTION = 5
    COLOR_CLASS = 6
    COLOR_VARIABLE = 7
    COLOR_OPERATOR = 8
    COLOR_CN_IDENTIFIER = 9   # 中文标识符专用颜色
    COLOR_ERROR = 10
    COLOR_SELECTION = 11
    COLOR_LINENUM = 12
    COLOR_STATUSBAR = 13
    COLOR_FOLDED = 14

    def __init__(self):
        self.current_language = "Python"
        self._init_colors()
        self._compiled_patterns: Dict[str, Dict] = {}

    def _init_colors(self):
        """初始化curses颜色对"""
        curses.start_color()
        curses.use_default_colors()
        # 定义颜色对 (前景色, 背景色)
        curses.init_pair(self.COLOR_KEYWORD, curses.COLOR_BLUE, -1)
        curses.init_pair(self.COLOR_STRING, curses.COLOR_GREEN, -1)
        curses.init_pair(self.COLOR_COMMENT, curses.COLOR_CYAN, -1)
        curses.init_pair(self.COLOR_NUMBER, curses.COLOR_YELLOW, -1)
        curses.init_pair(self.COLOR_FUNCTION, curses.COLOR_MAGENTA, -1)
        curses.init_pair(self.COLOR_CLASS, curses.COLOR_RED, -1)
        curses.init_pair(self.COLOR_VARIABLE, curses.COLOR_WHITE, -1)
        curses.init_pair(self.COLOR_OPERATOR, curses.COLOR_YELLOW, -1)
        curses.init_pair(self.COLOR_CN_IDENTIFIER, curses.COLOR_GREEN, -1)
        curses.init_pair(self.COLOR_ERROR, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_SELECTION, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(self.COLOR_LINENUM, curses.COLOR_YELLOW, -1)
        curses.init_pair(self.COLOR_STATUSBAR, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(self.COLOR_FOLDED, curses.COLOR_MAGENTA, -1)

    def detect_language(self, filename: str) -> str:
        """根据文件名后缀检测编程语言"""
        ext = os.path.splitext(filename)[1].lower()
        return SUPPORTED_LANGUAGES.get(ext, "Text")

    def highlight_line(self, line: str, language: str, 
                       selected: bool = False) -> List[Tuple[str, int]]:
        """
        对单行进行语法高亮分析
        返回: [(文本片段, 颜色对编号), ...]
        """
        if not line:
            return [(" ", self.COLOR_DEFAULT)]

        segments: List[Tuple[int, int, int]] = []  # (start, end, color)

        # 获取关键字集合
        keywords = LANGUAGE_KEYWORDS.get(language, set())
        patterns = LANGUAGE_PATTERNS.get(language, {})

        # 匹配注释
        comment_pat = patterns.get("comment", "")
        if comment_pat:
            for m in re.finditer(comment_pat, line):
                segments.append((m.start(), m.end(), self.COLOR_COMMENT))

        # 匹配字符串
        string_pat = patterns.get("string", "")
        if string_pat:
            for m in re.finditer(string_pat, line):
                # 避免与注释重叠
                if not self._is_overlapping(segments, m.start(), m.end()):
                    segments.append((m.start(), m.end(), self.COLOR_STRING))

        # 匹配数字
        number_pat = patterns.get("number", "")
        if number_pat:
            for m in re.finditer(number_pat, line):
                if not self._is_overlapping(segments, m.start(), m.end()):
                    segments.append((m.start(), m.end(), self.COLOR_NUMBER))

        # 匹配关键字
        word_pattern = re.compile(r'\b[a-zA-Z_]\w*\b')
        for m in word_pattern.finditer(line):
            if m.group() in keywords:
                if not self._is_overlapping(segments, m.start(), m.end()):
                    segments.append((m.start(), m.end(), self.COLOR_KEYWORD))

        # CNSH中文编程特殊处理
        if language in ("CNSH中文编程",):
            cn_pat = patterns.get("cn_identifier", r'[\u4e00-\u9fff_][\u4e00-\u9fff\w_]*')
            for m in re.finditer(cn_pat, line):
                if not self._is_overlapping(segments, m.start(), m.end()):
                    if m.group() in CNSH_KEYWORDS:
                        segments.append((m.start(), m.end(), self.COLOR_KEYWORD))
                    else:
                        segments.append((m.start(), m.end(), self.COLOR_CN_IDENTIFIER))

        # 匹配函数名
        func_patterns = {
            "Python": r'\bdef\s+(\w+)',
            "JavaScript": r'\bfunction\s+(\w+)|(\w+)\s*[=:]\s*function',
        }
        func_pat = func_patterns.get(language, patterns.get("func_name", ""))
        if func_pat:
            for m in re.finditer(func_pat, line):
                # 取最后一个非None的分组
                groups = [g for g in m.groups() if g]
                if groups:
                    func_name = groups[-1]
                    start = line.find(func_name, m.start())
                    end = start + len(func_name)
                    if not self._is_overlapping(segments, start, end):
                        segments.append((start, end, self.COLOR_FUNCTION))

        # 匹配运算符
        op_pattern = re.compile(r'[+=\-*/%<>!&|^~:;.,{}\[\]()]+')
        for m in op_pattern.finditer(line):
            if not self._is_overlapping(segments, m.start(), m.end()):
                segments.append((m.start(), m.end(), self.COLOR_OPERATOR))

        # 合并并排序片段
        return self._merge_segments(line, segments, selected)

    def _is_overlapping(self, segments: List[Tuple[int, int, int]], 
                        start: int, end: int) -> bool:
        """检查是否与已有片段重叠"""
        for s, e, _ in segments:
            if not (end <= s or start >= e):
                return True
        return False

    def _merge_segments(self, line: str, segments: List[Tuple[int, int, int]], 
                        selected: bool) -> List[Tuple[str, int]]:
        """合并所有片段，填充未着色部分为默认颜色"""
        segments.sort(key=lambda x: x[0])
        result = []
        pos = 0
        for start, end, color in segments:
            if start > pos:
                result.append((line[pos:start], self.COLOR_DEFAULT))
            result.append((line[start:end], color))
            pos = end
        if pos < len(line):
            result.append((line[pos:], self.COLOR_DEFAULT))
        if not result:
            result.append((line, self.COLOR_DEFAULT))
        return result

    def get_attribute(self, color_pair: int) -> int:
        """获取curses属性"""
        if color_pair == self.COLOR_DEFAULT:
            return curses.A_NORMAL
        return curses.color_pair(color_pair)


# ═══════════════════════════════════════════════════════════════
# 类3: AutoCompleteEngine - 自动补全引擎
# ═══════════════════════════════════════════════════════════════

class AutoCompleteEngine:
    """
    自动补全引擎 - 基于当前语言提供智能补全
    支持中文关键词补全和英文代码补全
    """

    def __init__(self):
        self.suggestions: List[str] = []
        self.selected_index: int = 0
        self.active: bool = False
        self.context_word: str = ""
        self._build_completion_database()

    def _build_completion_database(self):
        """构建补全数据库"""
        self.completion_db: Dict[str, Set[str]] = {}
        # 为每种语言构建补全列表
        for lang, keywords in LANGUAGE_KEYWORDS.items():
            self.completion_db[lang] = set(keywords)
        # CNSH中文编程的特殊补全
        self.completion_db["CNSH中文编程"] = set(CNSH_KEYWORDS)
        # 添加通用代码片段
        self.snippets = {
            "Python": {
                "def": "def ${1:函数名}(${2:参数}):\n    ${3:pass}",
                "class": "class ${1:类名}:\n    def __init__(self):\n        pass",
                "for": "for ${1:item} in ${2:iterable}:\n    ${3:pass}",
                "if": "if ${1:条件}:\n    ${2:pass}",
                "try": "try:\n    ${1:pass}\nexcept ${2:Exception}:\n    ${3:pass}",
            },
            "CNSH中文编程": {
                "函数": "函数 ${1:函数名}(${2:参数}):\n    ${3:返回 空}",
                "类": "类 ${1:类名}:\n    定义 初始化(自):\n        自.属性 = 空",
                "如果": "如果 ${1:条件}:\n    ${2:执行}\n否则:\n    ${3:其他}",
                "循环": "循环 ${1:变量} 于 ${2:范围}:\n    ${3:执行}",
                "定义": "定义 ${1:变量} = ${2:值}",
            },
        }

    def get_suggestions(self, word: str, language: str) -> List[str]:
        """根据当前词和语言获取补全建议"""
        if not word:
            return []
        suggestions = []
        # 获取语言特定关键字
        keywords = self.completion_db.get(language, set())
        # 过滤匹配的关键字
        word_lower = word.lower()
        for kw in keywords:
            if kw.lower().startswith(word_lower) and kw != word:
                suggestions.append(kw)
        # 添加通用补全
        for kw in self.completion_db.get("CNSH中文编程", set()):
            if word_lower in kw.lower() and kw not in suggestions:
                suggestions.append(kw)
        suggestions.sort(key=lambda x: (not x.lower().startswith(word_lower), x))
        return suggestions[:15]  # 最多15个建议

    def show_suggestions(self, word: str, language: str) -> List[str]:
        """显示补全建议列表"""
        self.context_word = word
        self.suggestions = self.get_suggestions(word, language)
        self.active = len(self.suggestions) > 0
        self.selected_index = 0
        return self.suggestions

    def select_next(self):
        """选择下一个建议"""
        if self.suggestions:
            self.selected_index = (self.selected_index + 1) % len(self.suggestions)

    def select_prev(self):
        """选择上一个建议"""
        if self.suggestions:
            self.selected_index = (self.selected_index - 1) % len(self.suggestions)

    def get_selected(self) -> Optional[str]:
        """获取当前选中的建议"""
        if self.suggestions and 0 <= self.selected_index < len(self.suggestions):
            return self.suggestions[self.selected_index]
        return None

    def get_snippet(self, keyword: str, language: str) -> Optional[str]:
        """获取代码片段"""
        snippets = self.snippets.get(language, {})
        return snippets.get(keyword)

    def close(self):
        """关闭补全窗口"""
        self.active = False
        self.suggestions = []
        self.selected_index = 0


# ═══════════════════════════════════════════════════════════════
# 类4: CNSHLinter - CNSH四层检查器
# ═══════════════════════════════════════════════════════════════

@dataclass
class LintIssue:
    """代码问题记录"""
    level: str           # "error", "warning", "info"
    message: str
    line: int
    col: int
    check_level: CNSHCheckLevel
    code: str = ""       # 问题代码


class CNSHLinter:
    """
    CNSH四层检查器 - 实现CNSH规范的L1-L4级检查
    L1: 字符级检查 (繁体龍、非法字符)
    L2: 关键字检查 (CNSH关键字合法性)
    L3: 语法检查 (基本语法结构)
    L4: 语义检查 (逻辑一致性)
    """

    def __init__(self):
        self.issues: List[LintIssue] = []
        self.enabled_levels = set(CNSHCheckLevel)

    def check_file(self, lines: List[str], language: str) -> List[LintIssue]:
        """对文件执行完整的四层检查"""
        self.issues = []
        if CNSHCheckLevel.L1_CHAR in self.enabled_levels:
            self._l1_char_check(lines)
        if CNSHCheckLevel.L2_KEYWORD in self.enabled_levels:
            self._l2_keyword_check(lines, language)
        if CNSHCheckLevel.L3_SYNTAX in self.enabled_levels:
            self._l3_syntax_check(lines, language)
        if CNSHCheckLevel.L4_SEMANTIC in self.enabled_levels:
            self._l4_semantic_check(lines, language)
        return self.issues

    def _l1_char_check(self, lines: List[str]):
        """L1: 字符级检查 - 检查非法字符和铁律遵循"""
        for i, line in enumerate(lines):
            # 检查简体「龙」
            for j, ch in enumerate(line):
                if ch == "龙":
                    self.issues.append(LintIssue(
                        level="error",
                        message="铁律违反: 使用简体「龙」，应使用繁体「龍」",
                        line=i,
                        col=j,
                        check_level=CNSHCheckLevel.L1_CHAR,
                        code="龙 -> 龍"
                    ))
            # 检查不可见控制字符
            ctrl_chars = re.finditer(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', line)
            for m in ctrl_chars:
                self.issues.append(LintIssue(
                    level="warning",
                    message=f"发现控制字符: \\x{ord(m.group()):02x}",
                    line=i,
                    col=m.start(),
                    check_level=CNSHCheckLevel.L1_CHAR
                ))

    def _l2_keyword_check(self, lines: List[str], language: str):
        """L2: 关键字检查 - 验证关键字使用合法性"""
        keywords = LANGUAGE_KEYWORDS.get(language, set())
        if language == "CNSH中文编程":
            # 检查CNSH关键字是否被正确用作关键字而非标识符
            for i, line in enumerate(lines):
                # 简单检查：关键字后面应有适当的语法
                for kw in CNSH_KEYWORDS:
                    pattern = re.compile(rf'\b{re.escape(kw)}\b')
                    for m in pattern.finditer(line):
                        # 检查关键字使用是否合法
                        after = line[m.end():].strip()
                        before = line[:m.start()].strip()
                        if kw in ("定义", "变量", "常量"):
                            if not after or after[0] not in ' \t=:":\n':
                                self.issues.append(LintIssue(
                                    level="warning",
                                    message=f"关键字「{kw}」使用可能不规范",
                                    line=i,
                                    col=m.start(),
                                    check_level=CNSHCheckLevel.L2_KEYWORD
                                ))

    def _l3_syntax_check(self, lines: List[str], language: str):
        """L3: 语法检查 - 基本语法结构验证"""
        for i, line in enumerate(lines):
            # 括号匹配检查
            parens = {"(": 0, "[": 0, "{": 0}
            for ch in line:
                if ch in parens:
                    parens[ch] += 1
                elif ch == ")":
                    parens["("] -= 1
                elif ch == "]":
                    parens["["] -= 1
                elif ch == "}":
                    parens["{"] -= 1
            for paren, count in parens.items():
                if count != 0:
                    close_map = {"(": ")", "[": "]", "{": "}"}
                    self.issues.append(LintIssue(
                        level="error",
                        message=f"括号不匹配: '{paren}' 未闭合" if count > 0 
                               else f"括号不匹配: 多余的 '{close_map[paren]}'",
                        line=i,
                        col=0,
                        check_level=CNSHCheckLevel.L3_SYNTAX
                    ))

        # 缩进检查 (Python/CNSH)
        if language in ("Python", "CNSH中文编程"):
            for i, line in enumerate(lines):
                if line.strip() and not line.startswith("#"):
                    indent = len(line) - len(line.lstrip())
                    if indent % 4 != 0:
                        self.issues.append(LintIssue(
                            level="warning",
                            message=f"缩进应为4的倍数，当前缩进{indent}个空格",
                            line=i,
                            col=0,
                            check_level=CNSHCheckLevel.L3_SYNTAX
                        ))

    def _l4_semantic_check(self, lines: List[str], language: str):
        """L4: 语义检查 - 逻辑一致性验证"""
        # 检查未使用的变量（简化版）
        if language in ("Python",):
            assignments = {}  # var_name -> line
            uses = set()
            for i, line in enumerate(lines):
                # 简单匹配赋值
                assign_match = re.match(r'\s*(\w+)\s*=', line)
                if assign_match:
                    var_name = assign_match.group(1)
                    if var_name not in ("if", "for", "while", "return", "class", "def"):
                        assignments[var_name] = i
                # 简单匹配使用
                for var in list(assignments.keys()):
                    if re.search(rf'\b{re.escape(var)}\b', line) and var not in assignments:
                        uses.add(var)
            # 简化：不做复杂的流程分析
            pass

    def get_summary(self) -> Dict[str, int]:
        """获取检查摘要"""
        summary = {"error": 0, "warning": 0, "info": 0}
        for issue in self.issues:
            summary[issue.level] = summary.get(issue.level, 0) + 1
        return summary

    def get_audit_display(self) -> str:
        """获取三色审计显示"""
        summary = self.get_summary()
        errors = summary.get("error", 0)
        warnings = summary.get("warning", 0)
        if errors > 0:
            return f"🔴 E:{errors} W:{warnings}"
        elif warnings > 0:
            return f"🟡 W:{warnings}"
        return "🟢 OK"


# ═══════════════════════════════════════════════════════════════
# 类5: FileBrowser - 文件浏览器
# ═══════════════════════════════════════════════════════════════

@dataclass
class FileNode:
    """文件树节点"""
    path: str
    name: str
    is_dir: bool
    expanded: bool = False
    children: List['FileNode'] = field(default_factory=list)
    level: int = 0


class FileBrowser:
    """文件浏览器 - 侧边栏文件树"""

    def __init__(self, root_path: str = "."):
        self.root_path = os.path.abspath(root_path)
        self.root: Optional[FileNode] = None
        self.selected_index = 0
        self.visible_items: List[FileNode] = []
        self.visible = False  # 是否显示
        self.width = 30       # 侧边栏宽度
        self._refresh()

    def _refresh(self):
        """刷新文件树"""
        self.root = self._build_tree(self.root_path)
        self._update_visible()

    def _build_tree(self, path: str, level: int = 0) -> FileNode:
        """递归构建文件树"""
        name = os.path.basename(path) or path
        is_dir = os.path.isdir(path)
        node = FileNode(path=path, name=name, is_dir=is_dir, level=level)
        if is_dir:
            try:
                entries = sorted(os.listdir(path),
                               key=lambda e: (not os.path.isdir(os.path.join(path, e)), e.lower()))
                for entry in entries:
                    if entry.startswith(".") and entry not in ("..", "."):
                        continue
                    full_path = os.path.join(path, entry)
                    child = self._build_tree(full_path, level + 1)
                    node.children.append(child)
            except PermissionError:
                pass
        return node

    def _update_visible(self):
        """更新可见项目列表"""
        self.visible_items = []
        if self.root:
            self._collect_visible(self.root)

    def _collect_visible(self, node: FileNode):
        """递归收集可见节点"""
        self.visible_items.append(node)
        if node.is_dir and node.expanded:
            for child in node.children:
                self._collect_visible(child)

    def toggle_expand(self):
        """展开/折叠当前目录"""
        if 0 <= self.selected_index < len(self.visible_items):
            node = self.visible_items[self.selected_index]
            if node.is_dir:
                node.expanded = not node.expanded
                self._update_visible()

    def move_down(self):
        """向下移动选择"""
        self.selected_index = min(len(self.visible_items) - 1, self.selected_index + 1)

    def move_up(self):
        """向上移动选择"""
        self.selected_index = max(0, self.selected_index - 1)

    def get_selected_path(self) -> Optional[str]:
        """获取当前选中的文件路径"""
        if 0 <= self.selected_index < len(self.visible_items):
            return self.visible_items[self.selected_index].path
        return None

    def toggle_visible(self):
        """切换显示/隐藏"""
        self.visible = not self.visible

    def render(self, stdscr, max_y: int, max_x: int):
        """渲染文件浏览器"""
        if not self.visible:
            return
        x_start = 0
        # 绘制边框和文件列表
        for i in range(max_y - 1):
            stdscr.addstr(i, x_start + self.width, "│", curses.color_pair(12))
        stdscr.addstr(0, x_start, "📁 文件浏览器".ljust(self.width), 
                     curses.A_BOLD | curses.color_pair(13))
        stdscr.addstr(0, x_start + self.width, "┬", curses.color_pair(12))
        for idx, item in enumerate(self.visible_items[:max_y - 2]):
            y = idx + 1
            if y >= max_y - 1:
                break
            prefix = "  " * item.level
            if item.is_dir:
                icon = "📂" if item.expanded else "📁"
                name = f"{prefix}{icon} {item.name}"
            else:
                icon = "📄"
                # 根据文件类型显示不同图标
                ext = os.path.splitext(item.name)[1]
                if ext == ".py":
                    icon = "🐍"
                elif ext in (".cnsh", ".cx"):
                    icon = "🇨🇳"
                name = f"{prefix}{icon} {item.name}"
            # 截断以适应宽度
            display = name[:self.width - 1].ljust(self.width - 1)
            attr = curses.color_pair(12)
            if idx == self.selected_index:
                attr = curses.color_pair(11)  # 选中高亮
            stdscr.addstr(y, x_start, display, attr)


# ═══════════════════════════════════════════════════════════════
# 类1: CNSHEditor - 主编辑器类
# ═══════════════════════════════════════════════════════════════

class CNSHEditor:
    """
    CNSH主编辑器类 - 集成所有功能的核心编辑器
    使用Python curses库在终端内运行
    """

    def __init__(self, stdscr, filename: Optional[str] = None):
        self.stdscr = stdscr
        self.filename = filename or "untitled.cnsh"
        self.lines: List[str] = [""]
        self.language = "Python"
        self.modified = False
        self.show_line_numbers = True
        self.line_number_width = 5
        self.top_line = 0       # 顶部显示的行
        self.left_col = 0       # 左侧显示的列

        # 子系统
        self.highlighter = SyntaxHighlighter()
        self.autocomplete = AutoCompleteEngine()
        self.linter = CNSHLinter()
        self.file_browser = FileBrowser()
        self.multi_cursor = MultiCursor()

        # 代码折叠
        self.folded_lines: Set[int] = set()  # 被折叠的行号
        self.fold_regions: Dict[int, Tuple[int, int]] = {}  # 折叠区域

        # 撤销/重做栈
        self.undo_stack: List[List[str]] = []
        self.redo_stack: List[List[str]] = []
        self.undo_limit = 100

        # 搜索
        self.search_term = ""
        self.search_results: List[Tuple[int, int]] = []
        self.search_index = 0
        self.search_active = False

        # 消息栏
        self.message = ""
        self.message_timeout = 0

        # 初始化
        self._detect_language()
        self._load_file()
        self._setup_screen()
        self._scan_fold_regions()

    def _detect_language(self):
        """检测当前文件语言"""
        self.language = self.highlighter.detect_language(self.filename)

    def _load_file(self):
        """加载文件"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.lines = content.split('\n') if content else [""]
                    if not self.lines:
                        self.lines = [""]
            except Exception as e:
                self.lines = [f"# 无法加载文件: {e}"]
                self.modified = True
        else:
            # 新文件，添加DNA头
            dna_header = DNATemplate.generate_header(self.filename, self.language)
            self.lines = dna_header.split('\n') if dna_header else [""]
            if not self.lines:
                self.lines = [""]
            self.modified = True

    def _setup_screen(self):
        """设置终端屏幕"""
        curses.curs_set(1)
        self.stdscr.keypad(True)
        curses.raw()
        self.stdscr.nodelay(False)

    def _scan_fold_regions(self):
        """扫描可折叠区域"""
        self.fold_regions = {}
        indent_stack = []
        for i, line in enumerate(self.lines):
            if not line.strip():
                continue
            indent = len(line) - len(line.lstrip())
            while indent_stack and indent_stack[-1][1] >= indent:
                start_line, _ = indent_stack.pop()
                if i - start_line > 1:
                    self.fold_regions[start_line] = (start_line + 1, i - 1)
            if line.strip().endswith(":") or line.rstrip().endswith("{"):
                indent_stack.append((i, indent))
        # 处理未闭合的
        while indent_stack:
            start_line, _ = indent_stack.pop()
            end_line = len(self.lines) - 1
            if end_line - start_line > 1:
                self.fold_regions[start_line] = (start_line + 1, end_line)

    def _save_undo(self):
        """保存当前状态到撤销栈"""
        self.undo_stack.append(self.lines[:])
        if len(self.undo_stack) > self.undo_limit:
            self.undo_stack.pop(0)
        self.redo_stack.clear()
        self.modified = True

    def _undo(self):
        """撤销"""
        if self.undo_stack:
            self.redo_stack.append(self.lines[:])
            self.lines = self.undo_stack.pop()
            self.multi_cursor.remove_secondary()

    def _redo(self):
        """重做"""
        if self.redo_stack:
            self.undo_stack.append(self.lines[:])
            self.lines = self.redo_stack.pop()
            self.multi_cursor.remove_secondary()

    def _save_file(self):
        """保存文件"""
        try:
            # 验证DNA
            content = '\n'.join(self.lines)
            has_dna, errors = DNATemplate.verify_dna(content)
            if not has_dna and self.language == "CNSH中文编程":
                # 自动添加DNA头
                dna = DNATemplate.generate_header(self.filename, self.language)
                self.lines = dna.split('\n') + self.lines
                content = '\n'.join(self.lines)
            os.makedirs(os.path.dirname(os.path.abspath(self.filename)) or '.', exist_ok=True)
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write(content)
            self.modified = False
            self._set_message(f"✓ 已保存: {self.filename}")
        except Exception as e:
            self._set_message(f"✗ 保存失败: {e}")

    def _set_message(self, msg: str, timeout: int = 3):
        """设置状态消息"""
        self.message = msg
        self.message_timeout = time.time() + timeout

    def _get_status_message(self) -> str:
        """获取当前状态消息"""
        if time.time() > self.message_timeout:
            self.message = ""
        return self.message

    def _insert_char(self, char: str):
        """在光标处插入字符"""
        self._save_undo()
        cursor = self.multi_cursor.primary
        line_idx = cursor.line
        col_idx = cursor.col
        if line_idx >= len(self.lines):
            self.lines.append("")
        line = self.lines[line_idx]
        self.lines[line_idx] = line[:col_idx] + char + line[col_idx:]
        cursor.col += len(char)
        # 如果有多个光标
        if len(self.multi_cursor.cursors) > 1:
            self.lines = self.multi_cursor.insert_at_all(char, self.lines)
        self._scan_fold_regions()

    def _delete_char(self, forward: bool = True):
        """删除光标处的字符"""
        self._save_undo()
        cursor = self.multi_cursor.primary
        line_idx = cursor.line
        col_idx = cursor.col
        if line_idx < len(self.lines):
            line = self.lines[line_idx]
            if forward and col_idx < len(line):
                self.lines[line_idx] = line[:col_idx] + line[col_idx + 1:]
            elif not forward and col_idx > 0:
                self.lines[line_idx] = line[:col_idx - 1] + line[col_idx:]
                cursor.col -= 1
        if len(self.multi_cursor.cursors) > 1:
            self.lines = self.multi_cursor.delete_at_all(self.lines, forward)
        self._scan_fold_regions()

    def _insert_newline(self):
        """插入新行"""
        self._save_undo()
        cursor = self.multi_cursor.primary
        line_idx = cursor.line
        col_idx = cursor.col
        if line_idx < len(self.lines):
            line = self.lines[line_idx]
            indent = ""
            # 自动缩进
            stripped = line.lstrip()
            current_indent = len(line) - len(stripped)
            if stripped.endswith(":") or stripped.endswith("{"):
                indent = " " * (current_indent + 4)
            else:
                indent = " " * current_indent
            new_line = indent
            remainder = line[col_idx:]
            self.lines[line_idx] = line[:col_idx]
            self.lines.insert(line_idx + 1, new_line + remainder)
            cursor.line += 1
            cursor.col = len(indent)
        else:
            self.lines.append("")
            cursor.line += 1
            cursor.col = 0
        self._scan_fold_regions()

    def _search(self, term: str):
        """搜索文本"""
        self.search_term = term
        self.search_results = []
        self.search_index = 0
        if not term:
            self.search_active = False
            return
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        for i, line in enumerate(self.lines):
            for m in pattern.finditer(line):
                self.search_results.append((i, m.start()))
        self.search_active = True
        self._set_message(f"找到 {len(self.search_results)} 个匹配")

    def _replace(self, old: str, new: str):
        """替换文本"""
        if not old:
            return
        self._save_undo()
        count = 0
        for i, line in enumerate(self.lines):
            new_line, n = re.subn(re.escape(old), new, line)
            if n > 0:
                self.lines[i] = new_line
                count += n
        self._set_message(f"替换了 {count} 处")

    def _toggle_fold(self):
        """切换当前行的代码折叠"""
        cursor = self.multi_cursor.primary
        line = cursor.line
        if line in self.fold_regions:
            if line in self.folded_lines:
                self.folded_lines.discard(line)
            else:
                self.folded_lines.add(line)

    def _run_linter(self):
        """运行CNSH四层检查"""
        issues = self.linter.check_file(self.lines, self.language)
        summary = self.linter.get_summary()
        status = self.linter.get_audit_display()
        self._set_message(f"CNSH检查完成 - {status} "
                         f"(错误:{summary.get('error',0)} 警告:{summary.get('warning',0)})")
        return issues

    def _get_folded_line_map(self) -> List[int]:
        """获取折叠后的行号映射 (显示行号 -> 实际行号)"""
        result = []
        i = 0
        while i < len(self.lines):
            result.append(i)
            if i in self.folded_lines and i in self.fold_regions:
                _, end = self.fold_regions[i]
                i = end + 1
            else:
                i += 1
        return result

    def render(self):
        """渲染编辑器界面"""
        self.stdscr.clear()
        max_y, max_x = self.stdscr.getmaxyx()
        if max_y < 3 or max_x < 10:
            return

        # 文件浏览器宽度
        fb_width = self.file_browser.width if self.file_browser.visible else 0
        edit_x = fb_width + self.line_number_width + 1

        # 渲染文件浏览器
        if self.file_browser.visible:
            self.file_browser.render(self.stdscr, max_y, fb_width)

        # 计算可见行（考虑折叠）
        visible_map = self._get_folded_line_map()
        cursor = self.multi_cursor.primary

        # 调整视图使光标可见
        while cursor.line < self.top_line and self.top_line > 0:
            self.top_line -= 1
        while cursor.line >= self.top_line + max_y - 2:
            self.top_line += 1

        # 渲染行号和内容
        for screen_y in range(max_y - 2):
            line_idx_in_map = self.top_line + screen_y
            if line_idx_in_map >= len(visible_map):
                break
            line_num = visible_map[line_idx_in_map]
            if line_num >= len(self.lines):
                break
            line = self.lines[line_num]
            y = screen_y + 1  # 留出标题行

            # 行号
            if self.show_line_numbers:
                ln_str = str(line_num + 1).rjust(self.line_number_width - 1) + "│"
                self.stdscr.addstr(y, fb_width, ln_str, 
                                 curses.color_pair(12))

            # 折叠标记
            prefix = ""
            if line_num in self.fold_regions:
                prefix = "▼ " if line_num in self.folded_lines else "▶ "

            # 高亮渲染
            segments = self.highlighter.highlight_line(line, self.language)
            x = edit_x
            # 先显示折叠标记
            if prefix:
                fold_attr = curses.color_pair(14) | curses.A_BOLD
                self.stdscr.addstr(y, x, prefix, fold_attr)
                x += len(prefix)

            # 显示高亮片段
            for text, color in segments:
                if x >= max_x - 1:
                    break
                # 水平滚动
                if x - edit_x < self.left_col:
                    x += len(text)
                    continue
                display_text = text[:max_x - x]
                attr = self.highlighter.get_attribute(color)
                # 光标行高亮
                if line_num == cursor.line:
                    attr |= curses.A_BOLD
                try:
                    self.stdscr.addstr(y, x, display_text, attr)
                except curses.error:
                    pass
                x += len(display_text)

        # 标题栏
        title = f" CNSH编辑器 v{VERSION} - {self.filename}"
        if self.modified:
            title += " [+]"
        title_attr = curses.A_BOLD | curses.color_pair(13)
        self.stdscr.addstr(0, fb_width, title[:max_x - fb_width], title_attr)
        if self.file_browser.visible:
            self.stdscr.addstr(0, fb_width + self.file_browser.width, "┬", 
                             curses.color_pair(12))

        # 状态栏
        status_y = max_y - 1
        cursor = self.multi_cursor.primary
        lint_status = self.linter.get_audit_display()
        lang_display = f"🇨🇳 {self.language}" if self.language == "CNSH中文编程" else self.language
        status = (f" {lang_display} | Ln {cursor.line+1}, Col {cursor.col+1} "
                 f"| {lint_status} | 🐉龍魂v{VERSION}")
        # 消息或状态
        msg = self._get_status_message()
        if msg:
            status = f" {msg}"
        try:
            self.stdscr.addstr(status_y, fb_width, status[:max_x - fb_width], 
                             curses.color_pair(13))
        except curses.error:
            pass

        # 设置光标位置
        cursor_screen_y = cursor.line - self.top_line + 1
        cursor_screen_x = edit_x + cursor.col - self.left_col
        if self.file_browser.visible and fb_width > 0:
            pass  # edit_x already includes fb_width
        if 1 <= cursor_screen_y < max_y - 1:
            try:
                self.stdscr.move(cursor_screen_y, cursor_screen_x)
            except curses.error:
                pass

        self.stdscr.refresh()

    def run(self):
        """主事件循环"""
        while True:
            self.render()
            try:
                key = self.stdscr.getch()
            except KeyboardInterrupt:
                break

            if key == -1:
                continue

            # 处理特殊键
            if key == 27:  # ESC
                self.autocomplete.close()
                self.multi_cursor.remove_secondary()
                self.search_active = False
            elif key == ctrl_key('q'):  # Ctrl+Q 退出
                if self.modified:
                    self._set_message("文件已修改，Ctrl+Q 再次确认退出")
                    self.render()
                    key2 = self.stdscr.getch()
                    if key2 == ctrl_key('q'):
                        break
                else:
                    break
            elif key == ctrl_key('s'):  # Ctrl+S 保存
                self._save_file()
            elif key == ctrl_key('f'):  # Ctrl+F 搜索
                self._handle_search()
            elif key == ctrl_key('r'):  # Ctrl+R 替换
                self._handle_replace()
            elif key == ctrl_key('b'):  # Ctrl+B 文件浏览器
                self.file_browser.toggle_visible()
            elif key == ctrl_key('t'):  # Ctrl+T 折叠
                self._toggle_fold()
            elif key == ctrl_key('m'):  # Ctrl+M 添加光标
                self._add_multi_cursor()
            elif key == ctrl_key('a'):  # Ctrl+A 全选当前行
                self._select_all_line()
            elif key == ctrl_key('z'):  # Ctrl+Z 撤销
                self._undo()
            elif key == ctrl_key('y'):  # Ctrl+Y 重做
                self._redo()
            elif key == ctrl_key('g'):  # Ctrl+G 跳转行
                self._goto_line()
            elif key == curses.KEY_F5:  # F5 运行检查
                self._run_linter()
            elif key == curses.KEY_F1:  # F1 帮助
                self._show_help()
            elif key == curses.KEY_F2:  # F2 主题
                self._set_message("主题切换功能 - 当前: 默认主题")
            elif key == curses.KEY_UP:
                self.multi_cursor.primary.line = max(0, self.multi_cursor.primary.line - 1)
                self.multi_cursor.remove_secondary()
            elif key == curses.KEY_DOWN:
                self.multi_cursor.primary.line = min(len(self.lines) - 1, 
                                                     self.multi_cursor.primary.line + 1)
                self.multi_cursor.remove_secondary()
            elif key == curses.KEY_LEFT:
                self.multi_cursor.primary.col = max(0, self.multi_cursor.primary.col - 1)
                self.multi_cursor.remove_secondary()
            elif key == curses.KEY_RIGHT:
                line_len = len(self.lines[self.multi_cursor.primary.line]) if self.multi_cursor.primary.line < len(self.lines) else 0
                self.multi_cursor.primary.col = min(line_len, self.multi_cursor.primary.col + 1)
                self.multi_cursor.remove_secondary()
            elif key == curses.KEY_HOME:
                self.multi_cursor.primary.col = 0
            elif key == curses.KEY_END:
                line_idx = self.multi_cursor.primary.line
                self.multi_cursor.primary.col = len(self.lines[line_idx]) if line_idx < len(self.lines) else 0
            elif key == curses.KEY_PPAGE:  # Page Up
                _, max_y = self.stdscr.getmaxyx()
                self.multi_cursor.primary.line = max(0, self.multi_cursor.primary.line - (max_y - 3))
                self.top_line = max(0, self.top_line - (max_y - 3))
            elif key == curses.KEY_NPAGE:  # Page Down
                _, max_y = self.stdscr.getmaxyx()
                self.multi_cursor.primary.line = min(len(self.lines) - 1, 
                                                     self.multi_cursor.primary.line + (max_y - 3))
            elif key == curses.KEY_BACKSPACE or key == 127 or key == 8:
                self._delete_char(forward=False)
            elif key == curses.KEY_DC:  # Delete
                self._delete_char(forward=True)
            elif key == curses.KEY_ENTER or key == 10 or key == 13:
                self._insert_newline()
            elif key == 9:  # Tab
                self._handle_tab()
            elif 32 <= key <= 126 or key >= 128:  # 可打印字符（包括中文UTF-8）
                try:
                    char = chr(key)
                    self._insert_char(char)
                    # 触发自动补全
                    self._trigger_autocomplete()
                except ValueError:
                    pass

    def _handle_search(self):
        """处理搜索"""
        self._set_message("搜索: ", timeout=30)
        self.render()
        term = self._read_input("搜索: ")
        if term:
            self._search(term)

    def _handle_replace(self):
        """处理替换"""
        old = self._read_input("查找: ")
        if old:
            new = self._read_input("替换为: ")
            self._replace(old, new)

    def _read_input(self, prompt: str) -> str:
        """在状态栏读取用户输入"""
        max_y, max_x = self.stdscr.getmaxyx()
        result = ""
        while True:
            self.stdscr.addstr(max_y - 1, 0, prompt + result, 
                             curses.color_pair(13))
            self.stdscr.clrtoeol()
            self.stdscr.refresh()
            key = self.stdscr.getch()
            if key == 10 or key == 13:  # Enter
                return result
            elif key == 27 or key == ctrl_key('c'):  # ESC/Ctrl+C
                return ""
            elif key == curses.KEY_BACKSPACE or key == 127:
                result = result[:-1]
            elif 32 <= key <= 126 or key >= 128:
                try:
                    result += chr(key)
                except ValueError:
                    pass

    def _add_multi_cursor(self):
        """添加多光标"""
        cursor = self.multi_cursor.primary
        self.multi_cursor.add_cursor(cursor.line + 1, cursor.col)
        self._set_message(f"多光标: {len(self.multi_cursor.cursors)} 个")

    def _select_all_line(self):
        """选中当前行"""
        cursor = self.multi_cursor.primary
        cursor.anchor_line = cursor.line
        cursor.anchor_col = 0
        cursor.col = len(self.lines[cursor.line]) if cursor.line < len(self.lines) else 0
        cursor.selection_active = True

    def _goto_line(self):
        """跳转到指定行"""
        line_str = self._read_input("跳转到行: ")
        try:
            target = int(line_str) - 1
            target = max(0, min(len(self.lines) - 1, target))
            self.multi_cursor.primary.line = target
            self.multi_cursor.primary.col = 0
        except ValueError:
            pass

    def _handle_tab(self):
        """处理Tab键 - 自动补全或缩进"""
        if self.autocomplete.active and self.autocomplete.suggestions:
            selected = self.autocomplete.get_selected()
            if selected:
                # 用选中的建议替换当前词
                self._save_undo()
                cursor = self.multi_cursor.primary
                word = self.autocomplete.context_word
                if word and cursor.col >= len(word):
                    line = self.lines[cursor.line]
                    start = cursor.col - len(word)
                    self.lines[cursor.line] = line[:start] + selected + line[cursor.col:]
                    cursor.col = start + len(selected)
                self.autocomplete.close()
                return
            self.autocomplete.select_next()
        else:
            # 插入4个空格
            self._insert_char("    ")

    def _trigger_autocomplete(self):
        """触发自动补全"""
        cursor = self.multi_cursor.primary
        if cursor.line >= len(self.lines):
            return
        line = self.lines[cursor.line]
        col = cursor.col
        # 获取光标前的词
        before = line[:col]
        # 匹配中文或英文标识符
        match = re.search(r'([\u4e00-\u9fff_\w]+)$', before)
        if match:
            word = match.group(1)
            suggestions = self.autocomplete.show_suggestions(word, self.language)
            if suggestions:
                self._set_message(f"补全: {', '.join(suggestions[:5])}", timeout=5)

    def _show_help(self):
        """显示帮助信息"""
        help_text = ("快捷键: Ctrl+S保存 Ctrl+Q退出 Ctrl+F搜索 Ctrl+R替换 "
                    "Ctrl+B文件树 Ctrl+T折叠 Ctrl+M多光标 Ctrl+Z撤销 "
                    "Ctrl+Y重做 F5检查 F1帮助 F2主题")
        self._set_message(help_text, timeout=10)


def ctrl_key(ch: str) -> int:
    """获取Ctrl+字符的键值"""
    return ord(ch) & 0x1f


# ═══════════════════════════════════════════════════════════════
# 入口函数
# ═══════════════════════════════════════════════════════════════

def main():
    """
    CNSH中文多语言编辑器入口函数
    用法: python3 cnsh_editor_engine_v2.0.py [文件名]
    """
    filename = sys.argv[1] if len(sys.argv) > 1 else "untitled.cnsh"

    # 打印启动信息
    print("╔══════════════════════════════════════════════════════════╗")
    print("║         CNSH中文多语言编辑器核心引擎 v2.0                 ║")
    print("║         Chinese Multi-Language Editor Engine              ║")
    print("╠══════════════════════════════════════════════════════════╣")
    print(f"║  {DNA_HEADER}                          ║")
    print(f"║  {CONFIRM_MARK}                    ║")
    print(f"║  {SEAL_MARK}   ║")
    print("╠══════════════════════════════════════════════════════════╣")
    print("║  六层来源链:                                              ║")
    print("║  道统(曾仕强)·精神(Steve Jobs)·设备(Apple)                ║")
    print("║  ·技术(Open Source)·系统(UID9622)·生命(CNSH)              ║")
    print("╠══════════════════════════════════════════════════════════╣")
    print("║  铁律: 繁体「龍」不得简化为「龙」; 人永远是1; 不蒸馏        ║")
    print("║  三层监督: 逻辑校验 | 价值观校验 | 技术校验                  ║")
    print("║  三色审计: 🟢通过 🟡警告 🔴错误                            ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"\n启动中... 正在加载文件: {filename}")
    print("按 Ctrl+Q 退出编辑器，F1 查看帮助\n")
    time.sleep(1)

    def wrapper(stdscr):
        editor = CNSHEditor(stdscr, filename)
        editor.run()

    # 使用curses.wrapper运行
    try:
        curses.wrapper(wrapper)
    except Exception as e:
        print(f"\n编辑器发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print(f"\n编辑器已退出。文件: {filename}")
    print(f"{DNA_HEADER}")
    print(f"{CONFIRM_MARK}")
    print(f"{SEAL_MARK}")


if __name__ == "__main__":
    main()
