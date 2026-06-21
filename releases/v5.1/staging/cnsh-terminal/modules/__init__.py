# -*- coding: utf-8 -*-
"""#龍芯⚡️2026-06-18-CNSH-TERMINAL-FILE2-v5.0-MODULES-INIT
# 🟢 审计通过: 模块初始化文件
# 🔒 AI Truth Protocol: 所有声明均为真实
# 🤝 君子协议: CC BY-NC-SA 4.0 · UID9622 · 龍芯北辰 · 诸葛鑫

CNSH多语言编辑器终端v5.0 模块包
中文编程语言 · 繁體龍字永存
"""

__version__ = "5.0.0"
__author__ = "龍芯北辰 · 诸葛鑫"
__uid__ = "UID9622"
__license__ = "CC BY-NC-SA 4.0"
__dna__ = "#龍芯⚡️2026-06-18-CNSH-TERMINAL-v5.0"

# 模块导出
from .lexer import Lexer, TokenType, Token
from .parser import Parser
from .ast_nodes import *
from .code_generator import CCodeGenerator
from .translator import 通心译翻译器
from .terminology_bank import 中央藏经阁
from .encryption import 点对点加密
from .circuit_breaker import 熔断机制
from .ai_timestamp import AI时间戳规范
from .four_layer_check import CNSH四层检查
from .audit_integration import 联动审计

__all__ = [
    "Lexer", "TokenType", "Token", "Parser",
    "CCodeGenerator", "通心译翻译器", "中央藏经阁",
    "点对点加密", "熔断机制", "AI时间戳规范",
    "CNSH四层检查", "联动审计"
]
