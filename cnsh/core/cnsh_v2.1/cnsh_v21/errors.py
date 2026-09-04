#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
CNSH v2.1 错误体系
DNA: #龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-CNSH-ERRORS-v2.1
"""


class CNSHError(Exception):
    """CNSH 基础异常"""
    def __init__(self, message: str, line: int = 0, column: int = 0, file: str = "<cnsh>"):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column
        self.file = file

    def __str__(self) -> str:
        loc = f"{self.file}:{self.line}:{self.column}" if self.line else self.file
        return f"🔴 CNSH 错误 [{loc}]: {self.message}"


class CNSHLexError(CNSHError):
    """词法错误"""
    pass


class CNSHParseError(CNSHError):
    """语法错误"""
    pass


class CNSHRuntimeError(CNSHError):
    """运行时错误"""
    pass


class CNSHAuditError(CNSHRuntimeError):
    """三色审计熔断"""
    pass
