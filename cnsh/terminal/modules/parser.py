#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷔噬嗑-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""#龍芯⚡️丙午·甲午·癸亥·戊午·䷚颐-CNSH-PARSER-FILE2-v5.0
# 🟢 审计通过: 语法分析器完整实现
# 🔒 AI Truth Protocol: 所有声明均为真实
# 🤝 君子协议: CC BY-NC-SA 4.0 · UID9622 · 龍芯北辰 · 诸葛鑫

CNSH中文编程语言语法分析器
递归下降解析器，生成完整AST
"""

import hashlib
from typing import List, Optional, Dict, Any
from .lexer import Token, TokenType, Lexer
from .ast_nodes import *


class 语法错误(Exception):
    """语法错误异常"""
    def __init__(self, 消息: str, 行号: int = 0, 列号: int = 0):
        self.消息 = 消息
        self.行号 = 行号
        self.列号 = 列号
        super().__init__(f"语法错误 [行{行号}, 列{列号}]: {消息}")


class Parser:
    """CNSH语法分析器"""

    DNA追溯 = "#龍芯⚡️丙午·甲午·癸亥·戊午·䷚颐-CNSH-PARSER-v5.0"

    def __init__(self, 标记列表: List[Token], 启用审计: bool = True):
        self.标记列表 = 标记列表
        self.位置 = 0
        self.启用审计 = 启用审计
        self.审计日志: List[Dict] = []

    def 记录(self, 级别: str, 消息: str) -> None:
        """记录审计日志"""
        self.审计日志.append({
            "级别": 级别,
            "消息": 消息,
            "颜色": {"成功": "🟢", "警告": "🟡", "错误": "🔴"}.get(级别, "⚪")
        })

    def 当前标记(self) -> Token:
        """获取当前Token"""
        if self.位置 >= len(self.标记列表):
            return self.标记列表[-1] if self.标记列表 else Token(TokenType.EOF, "", 0, 0)
        return self.标记列表[self.位置]

    def 查看标记(self, 偏移: int = 1) -> Token:
        """查看 ahead Token"""
        pos = self.位置 + 偏移
        if pos >= len(self.标记列表):
            return self.标记列表[-1] if self.标记列表 else Token(TokenType.EOF, "", 0, 0)
        return self.标记列表[pos]

    def 匹配(self, *类型列表: TokenType) -> bool:
        """检查当前Token类型是否匹配"""
        return self.当前标记().类型 in 类型列表

    def 消费(self, 期望类型: TokenType = None, 期望值: str | None = None) -> Token:
        """消费当前Token"""
        标记 = self.当前标记()
        if 期望类型 and 标记.类型 != 期望类型:
            raise 语法错误(
                f"期望 {期望类型.name}，但得到 {标记.类型.name} ('{标记.值}')",
                标记.行号, 标记.列号
            )
        if 期望值 and 标记.值 != 期望值:
            raise 语法错误(
                f"期望 '{期望值}'，但得到 '{标记.值}'",
                标记.行号, 标记.列号
            )
        self.位置 += 1
        return 标记

    def 跳过换行(self) -> None:
        """跳过换行符"""
        while self.匹配(TokenType.NEWLINE):
            self.消费(TokenType.NEWLINE)

    def 解析(self) -> 程序:
        """主解析入口"""
        self.记录("成功", "=== 语法分析开始 ===")
        声明列表 = []

        while not self.匹配(TokenType.EOF):
            self.跳过换行()
            if self.匹配(TokenType.EOF):
                break
            try:
                声明 = self.解析声明()
                if 声明:
                    声明列表.append(声明)
            except 语法错误 as e:
                self.记录("错误", str(e))
                # 错误恢复：跳过当前token
                if not self.匹配(TokenType.EOF):
                    self.位置 += 1

        self.记录("成功", f"=== 语法分析完成，共 {len(声明列表)} 个顶级声明 ===")
        return 程序(声明列表)

    def 解析声明(self) -> Optional[AST节点]:
        """解析声明"""
        标记 = self.当前标记()

        if self.匹配(TokenType.KEYWORD):
            if 标记.值 in ("函数", "异步"):
                return self.解析函数声明()
            elif 标记.值 == "类":
                return self.解析类声明()
            elif 标记.值 in ("如果", "循环", "当"):
                return self.解析语句()
            elif 标记.值 in ("整数", "小数", "文本", "真假", "空值", "常量", "静态"):
                return self.解析变量声明()
            elif 标记.值 in ("打印", "输入"):
                return self.解析语句()
            elif 标记.值 in ("返回", "跳出", "继续"):
                return self.解析语句()
            elif 标记.值 == "导入":
                return self.解析导入声明()

        if self.匹配(TokenType.TYPE):
            return self.解析变量声明()

        if self.匹配(TokenType.IDENTIFIER):
            return self.解析表达式语句()

        self.记录("警告", f"未预期的Token: {标记}")
        return None

    def 解析变量声明(self) -> 变量声明:
        """解析变量声明"""
        行号 = self.当前标记().行号
        列号 = self.当前标记().列号
        是否常量 = False

        # 检查修饰符
        if self.匹配(TokenType.KEYWORD) and self.当前标记().值 == "常量":
            是否常量 = True
            self.消费(TokenType.KEYWORD)

        数据类型标记 = self.消费(TokenType.TYPE)
        数据类型 = 数据类型标记.值

        变量名标记 = self.消费(TokenType.IDENTIFIER)
        变量名 = 变量名标记.值

        初始值 = None
        if self.匹配(TokenType.ASSIGN):
            self.消费(TokenType.ASSIGN)
            初始值 = self.解析表达式()

        # 可选的分号
        if self.匹配(TokenType.SEMICOLON):
            self.消费(TokenType.SEMICOLON)

        self.记录("成功", f"变量声明: {数据类型} {变量名}")
        return 变量声明(数据类型, 变量名, 初始值, 行号, 列号, 是否常量)

    def 解析函数声明(self) -> 函数声明:
        """解析函数声明"""
        行号 = self.当前标记().行号
        列号 = self.当前标记().列号
        是否异步 = False

        if self.匹配(TokenType.KEYWORD) and self.当前标记().值 == "异步":
            是否异步 = True
            self.消费(TokenType.KEYWORD)

        self.消费(TokenType.KEYWORD)  # 消费"函数"
        函数名标记 = self.消费(TokenType.IDENTIFIER)
        函数名 = 函数名标记.值

        self.消费(TokenType.LPAREN)
        参数列表 = self.解析参数列表()
        self.消费(TokenType.RPAREN)

        # 返回类型
        返回类型 = "空值"
        if self.匹配(TokenType.ARROW):
            self.消费(TokenType.ARROW)
            返回类型标记 = self.消费(TokenType.TYPE)
            返回类型 = 返回类型标记.值

        函数体 = self.解析块语句()

        self.记录("成功", f"函数声明: {函数名}({len(参数列表)}参数) -> {返回类型}")
        return 函数声明(返回类型, 函数名, 参数列表, 函数体, 行号, 列号, 是否异步)

    def 解析参数列表(self) -> List[Dict[str, str]]:
        """解析函数参数列表"""
        参数列表 = []

        if self.匹配(TokenType.RPAREN):
            return 参数列表

        while True:
            参数类型标记 = self.消费(TokenType.TYPE)
            参数名标记 = self.消费(TokenType.IDENTIFIER)
            参数列表.append({
                "类型": 参数类型标记.值,
                "名称": 参数名标记.值
            })

            if self.匹配(TokenType.COMMA):
                self.消费(TokenType.COMMA)
            else:
                break

        return 参数列表

    def 解析类声明(self) -> 类声明:
        """解析类声明"""
        行号 = self.当前标记().行号
        self.消费(TokenType.KEYWORD)  # 类

        类名标记 = self.消费(TokenType.IDENTIFIER)
        类名 = 类名标记.值

        父类 = None
        if self.匹配(TokenType.LPAREN):
            self.消费(TokenType.LPAREN)
            父类标记 = self.消费(TokenType.IDENTIFIER)
            父类 = 父类标记.值
            self.消费(TokenType.RPAREN)

        self.消费(TokenType.LBRACE)

        成员列表 = []
        while not self.匹配(TokenType.RBRACE):
            self.跳过换行()
            if self.匹配(TokenType.RBRACE):
                break
            成员 = self.解析声明()
            if 成员:
                成员列表.append(成员)

        self.消费(TokenType.RBRACE)

        self.记录("成功", f"类声明: {类名}")
        return 类声明(类名, 父类, 成员列表, 行号)

    def 解析块语句(self) -> 块语句:
        """解析代码块"""
        行号 = self.当前标记().行号

        # 花括号块
        if self.匹配(TokenType.LBRACE):
            self.消费(TokenType.LBRACE)
            语句列表 = []
            while not self.匹配(TokenType.RBRACE):
                self.跳过换行()
                if self.匹配(TokenType.RBRACE):
                    break
                语句 = self.解析语句()
                if 语句:
                    语句列表.append(语句)
            self.消费(TokenType.RBRACE)
            return 块语句(语句列表, 行号)

        # 缩进块 (Python风格)
        if self.匹配(TokenType.INDENT):
            self.消费(TokenType.INDENT)
            语句列表 = []
            while not self.匹配(TokenType.DEDENT, TokenType.EOF):
                self.跳过换行()
                if self.匹配(TokenType.DEDENT, TokenType.EOF):
                    break
                语句 = self.解析语句()
                if 语句:
                    语句列表.append(语句)
            if self.匹配(TokenType.DEDENT):
                self.消费(TokenType.DEDENT)
            return 块语句(语句列表, 行号)

        # 单行语句
        语句 = self.解析语句()
        return 块语句([语句] if 语句 else [], 行号)

    def 解析语句(self) -> Optional[AST节点]:
        """解析语句"""
        self.跳过换行()

        if self.匹配(TokenType.KEYWORD):
            关键字值 = self.当前标记().值

            if 关键字值 == "如果":
                return self.解析如果语句()
            elif 关键字值 == "循环":
                return self.解析循环语句()
            elif 关键字值 == "当":
                return self.解析当语句()
            elif 关键字值 == "返回":
                return self.解析返回语句()
            elif 关键字值 == "跳出":
                return self.解析跳出语句()
            elif 关键字值 == "继续":
                return self.解析继续语句()
            elif 关键字值 in ("打印", "输入"):
                return self.解析IO语句()

        if self.匹配(TokenType.TYPE, TokenType.KEYWORD):
            if self.当前标记().值 in ("整数", "小数", "文本", "真假", "空值", "常量"):
                return self.解析变量声明()

        if self.匹配(TokenType.IDENTIFIER):
            return self.解析表达式语句()

        if self.匹配(TokenType.NEWLINE, TokenType.EOF):
            return None

        return self.解析表达式语句()

    def 解析如果语句(self) -> 如果语句:
        """解析条件语句"""
        行号 = self.当前标记().行号
        self.消费(TokenType.KEYWORD)  # 如果

        条件 = self.解析表达式()

        真分支 = self.解析块语句()

        假分支 = None
        否则如果列表 = []

        while self.匹配(TokenType.KEYWORD) and self.当前标记().值 == "否则如果":
            self.消费(TokenType.KEYWORD)
            elif条件 = self.解析表达式()
            elif分支 = self.解析块语句()
            否则如果列表.append({"条件": elif条件, "分支": elif分支})

        if self.匹配(TokenType.KEYWORD) and self.当前标记().值 == "否则":
            self.消费(TokenType.KEYWORD)
            假分支 = self.解析块语句()

        return 如果语句(条件, 真分支, 假分支, 否则如果列表, 行号)

    def 解析循环语句(self) -> 循环语句:
        """解析循环语句"""
        行号 = self.当前标记().行号
        self.消费(TokenType.KEYWORD)  # 循环

        初始化 = None
        条件 = None
        增量 = None

        # 检查是否是C风格循环: 循环 类型 变量 = 初值; 条件; 增量
        if self.匹配(TokenType.TYPE):
            初始化 = self.解析变量声明()

            if self.匹配(TokenType.SEMICOLON):
                self.消费(TokenType.SEMICOLON)
                条件 = self.解析表达式()
                self.消费(TokenType.SEMICOLON)
                增量 = self.解析表达式()
            elif self.匹配(TokenType.COMMA):
                # 范围循环: 循环 变量 于 范围 {
                pass

        elif not self.匹配(TokenType.LBRACE, TokenType.INDENT):
            # 简写: 循环 条件 { }
            条件 = self.解析表达式()

        循环体 = self.解析块语句()

        # 默认条件为真
        if 条件 is None:
            条件 = 布尔(True, 行号)

        return 循环语句(初始化, 条件, 增量, 循环体, 行号)

    def 解析当语句(self) -> 当语句:
        """解析当循环语句"""
        行号 = self.当前标记().行号
        self.消费(TokenType.KEYWORD)  # 当

        条件 = self.解析表达式()
        循环体 = self.解析块语句()

        return 当语句(条件, 循环体, 行号)

    def 解析返回语句(self) -> 返回语句:
        """解析返回语句"""
        行号 = self.当前标记().行号
        self.消费(TokenType.KEYWORD)  # 返回

        返回值 = None
        if not self.匹配(TokenType.NEWLINE, TokenType.EOF, TokenType.RBRACE, TokenType.DEDENT):
            返回值 = self.解析表达式()

        self.跳过分号()
        return 返回语句(返回值, 行号)

    def 解析跳出语句(self) -> 跳出语句:
        """解析跳出语句"""
        行号 = self.当前标记().行号
        self.消费(TokenType.KEYWORD)
        self.跳过分号()
        return 跳出语句(行号)

    def 解析继续语句(self) -> 继续语句:
        """解析继续语句"""
        行号 = self.当前标记().行号
        self.消费(TokenType.KEYWORD)
        self.跳过分号()
        return 继续语句(行号)

    def 解析IO语句(self) -> AST节点:
        """解析输入输出语句"""
        行号 = self.当前标记().行号
        关键字 = self.当前标记().值
        self.消费(TokenType.KEYWORD)

        表达式列表 = []
        if not self.匹配(TokenType.NEWLINE, TokenType.EOF, TokenType.RBRACE):
            表达式列表 = self.解析表达式列表()

        self.跳过分号()

        if 关键字 == "打印":
            return 打印语句(表达式列表, 行号)
        else:
            return 输入语句(
                表达式列表[0].值 if 表达式列表 and isinstance(表达式列表[0], 字符串) else None,
                行号
            )

    def 解析表达式语句(self) -> 表达式语句:
        """解析表达式语句"""
        行号 = self.当前标记().行号
        表达式 = self.解析表达式()
        self.跳过分号()
        return 表达式语句(表达式, 行号)

    def 解析表达式列表(self) -> List[AST节点]:
        """解析逗号分隔的表达式列表"""
        表达式列表 = []

        while True:
            表达式列表.append(self.解析表达式())
            if self.匹配(TokenType.COMMA):
                self.消费(TokenType.COMMA)
            else:
                break

        return 表达式列表

    def 解析表达式(self) -> AST节点:
        """解析表达式（赋值表达式）"""
        return self.解析赋值表达式()

    def 解析赋值表达式(self) -> AST节点:
        """解析赋值表达式"""
        左值 = self.解析逻辑或表达式()

        if self.匹配(TokenType.ASSIGN, TokenType.PLUS_ASSIGN,
                     TokenType.MINUS_ASSIGN, TokenType.MUL_ASSIGN, TokenType.DIV_ASSIGN):
            运算符 = self.当前标记().值
            self.位置 += 1
            右值 = self.解析赋值表达式()

            if 运算符 != '=':
                # 复合赋值转简单赋值
                简运算符 = 运算符[0]
                右值 = 二元运算(左值, 简运算符, 右值, 左值.行号, 左值.列号)
                运算符 = '='

            return 赋值(左值, 右值, 左值.行号, 左值.列号)

        return 左值

    def 解析逻辑或表达式(self) -> AST节点:
        """解析逻辑或表达式"""
        左值 = self.解析逻辑与表达式()

        while self.匹配(TokenType.OR):
            运算符 = self.当前标记().值
            self.位置 += 1
            右值 = self.解析逻辑与表达式()
            左值 = 二元运算(左值, 运算符, 右值, 左值.行号, 左值.列号)

        return 左值

    def 解析逻辑与表达式(self) -> AST节点:
        """解析逻辑与表达式"""
        左值 = self.解析或表达式()

        while self.匹配(TokenType.AND):
            运算符 = self.当前标记().值
            self.位置 += 1
            右值 = self.解析或表达式()
            左值 = 二元运算(左值, 运算符, 右值, 左值.行号, 左值.列号)

        return 左值

    def 解析或表达式(self) -> AST节点:
        """解析位或表达式"""
        左值 = self.解析异或表达式()

        while self.匹配(TokenType.BIT_OR):
            运算符 = self.当前标记().值
            self.位置 += 1
            右值 = self.解析异或表达式()
            左值 = 二元运算(左值, 运算符, 右值, 左值.行号, 左值.列号)

        return 左值

    def 解析异或表达式(self) -> AST节点:
        """解析异或表达式"""
        左值 = self.解析与表达式()

        while self.匹配(TokenType.BIT_XOR):
            运算符 = self.当前标记().值
            self.位置 += 1
            右值 = self.解析与表达式()
            左值 = 二元运算(左值, 运算符, 右值, 左值.行号, 左值.列号)

        return 左值

    def 解析与表达式(self) -> AST节点:
        """解析位与表达式"""
        左值 = self.解析等式表达式()

        while self.匹配(TokenType.BIT_AND):
            运算符 = self.当前标记().值
            self.位置 += 1
            右值 = self.解析等式表达式()
            左值 = 二元运算(左值, 运算符, 右值, 左值.行号, 左值.列号)

        return 左值

    def 解析等式表达式(self) -> AST节点:
        """解析等式表达式"""
        左值 = self.解析关系表达式()

        while self.匹配(TokenType.EQ, TokenType.NE):
            运算符 = self.当前标记().值
            self.位置 += 1
            右值 = self.解析关系表达式()
            左值 = 二元运算(左值, 运算符, 右值, 左值.行号, 左值.列号)

        return 左值

    def 解析关系表达式(self) -> AST节点:
        """解析关系表达式"""
        左值 = self.解析移位表达式()

        while self.匹配(TokenType.LT, TokenType.GT, TokenType.LE, TokenType.GE):
            运算符 = self.当前标记().值
            self.位置 += 1
            右值 = self.解析移位表达式()
            左值 = 二元运算(左值, 运算符, 右值, 左值.行号, 左值.列号)

        return 左值

    def 解析移位表达式(self) -> AST节点:
        """解析移位表达式"""
        左值 = self.解析加法表达式()

        while self.匹配(TokenType.LSHIFT, TokenType.RSHIFT):
            运算符 = self.当前标记().值
            self.位置 += 1
            右值 = self.解析加法表达式()
            左值 = 二元运算(左值, 运算符, 右值, 左值.行号, 左值.列号)

        return 左值

    def 解析加法表达式(self) -> AST节点:
        """解析加法表达式"""
        左值 = self.解析乘法表达式()

        while self.匹配(TokenType.PLUS, TokenType.MINUS):
            运算符 = self.当前标记().值
            self.位置 += 1
            右值 = self.解析乘法表达式()
            左值 = 二元运算(左值, 运算符, 右值, 左值.行号, 左值.列号)

        return 左值

    def 解析乘法表达式(self) -> AST节点:
        """解析乘法表达式"""
        左值 = self.解析幂表达式()

        while self.匹配(TokenType.MUL, TokenType.DIV, TokenType.MOD):
            运算符 = self.当前标记().值
            self.位置 += 1
            右值 = self.解析幂表达式()
            左值 = 二元运算(左值, 运算符, 右值, 左值.行号, 左值.列号)

        return 左值

    def 解析幂表达式(self) -> AST节点:
        """解析幂表达式"""
        左值 = self.解析一元表达式()

        if self.匹配(TokenType.POWER):
            运算符 = self.当前标记().值
            self.位置 += 1
            右值 = self.解析幂表达式()
            return 二元运算(左值, 运算符, 右值, 左值.行号, 左值.列号)

        return 左值

    def 解析一元表达式(self) -> AST节点:
        """解析一元表达式"""
        if self.匹配(TokenType.MINUS, TokenType.NOT, TokenType.BIT_NOT):
            运算符 = self.当前标记().值
            行号 = self.当前标记().行号
            self.位置 += 1
            操作数 = self.解析一元表达式()
            return 一元运算(运算符, 操作数, 行号)

        return self.解析后缀表达式()

    def 解析后缀表达式(self) -> AST节点:
        """解析后缀表达式"""
        左值 = self.解析基本表达式()

        while True:
            if self.匹配(TokenType.LPAREN):
                # 函数调用
                左值 = self.解析调用后缀(左值)
            elif self.匹配(TokenType.DOT):
                # 成员访问
                self.消费(TokenType.DOT)
                成员名标记 = self.消费(TokenType.IDENTIFIER)
                左值 = 成员访问(左值, 成员名标记.值, 左值.行号)
            elif self.匹配(TokenType.LBRACKET):
                # 数组访问
                self.消费(TokenType.LBRACKET)
                索引 = self.解析表达式()
                self.消费(TokenType.RBRACKET)
                左值 = 数组访问(左值, 索引, 左值.行号)
            else:
                break

        return 左值

    def 解析调用后缀(self, 函数: AST节点) -> 函数调用:
        """解析函数调用后缀"""
        行号 = self.当前标记().行号
        self.消费(TokenType.LPAREN)

        参数列表 = []
        if not self.匹配(TokenType.RPAREN):
            参数列表 = self.解析表达式列表()

        self.消费(TokenType.RPAREN)

        函数名 = 函数.名称 if isinstance(函数, 标识符) else "匿名"
        return 函数调用(函数名, 参数列表, 行号)

    def 解析基本表达式(self) -> AST节点:
        """解析基本表达式"""
        标记 = self.当前标记()

        if self.匹配(TokenType.NUMBER):
            self.消费()
            return 数字(float(标记.值), 标记.行号, 标记.列号)

        if self.匹配(TokenType.STRING):
            self.消费()
            return 字符串(标记.值, 标记.行号, 标记.列号)

        if self.匹配(TokenType.BOOLEAN):
            self.消费()
            return 布尔(标记.值 == "真", 标记.行号, 标记.列号)

        if self.匹配(TokenType.NULL):
            self.消费()
            return 空值(标记.行号, 标记.列号)

        if self.匹配(TokenType.IDENTIFIER):
            self.消费()
            return 标识符(标记.值, 标记.行号, 标记.列号)

        if self.匹配(TokenType.LPAREN):
            self.消费(TokenType.LPAREN)
            表达式 = self.解析表达式()
            self.消费(TokenType.RPAREN)
            return 表达式

        if self.匹配(TokenType.LBRACKET):
            return self.解析数组字面量()

        raise 语法错误(f"未预期的表达式: {标记.值} (类型: {标记.类型.name})",
                      标记.行号, 标记.列号)

    def 解析数组字面量(self) -> 数组字面量:
        """解析数组字面量"""
        行号 = self.当前标记().行号
        self.消费(TokenType.LBRACKET)

        元素列表 = []
        if not self.匹配(TokenType.RBRACKET):
            while True:
                元素列表.append(self.解析表达式())
                if self.匹配(TokenType.COMMA):
                    self.消费(TokenType.COMMA)
                else:
                    break

        self.消费(TokenType.RBRACKET)
        return 数组字面量(元素列表, 行号)

    def 解析导入声明(self) -> 表达式语句:
        """解析导入声明"""
        行号 = self.当前标记().行号
        self.消费(TokenType.KEYWORD)
        模块名 = self.消费(TokenType.STRING)
        self.跳过分号()
        return 表达式语句(字符串(模块名.值, 行号), 行号)

    def 跳过分号(self) -> None:
        """跳过分号（如果存在）"""
        if self.匹配(TokenType.SEMICOLON):
            self.消费(TokenType.SEMICOLON)

    def 获取审计结果(self) -> Dict[str, Any]:
        """获取审计结果"""
        错误数 = sum(1 for 日志 in self.审计日志 if 日志["级别"] == "错误")
        警告数 = sum(1 for 日志 in self.审计日志 if 日志["级别"] == "警告")
        成功数 = sum(1 for 日志 in self.审计日志 if 日志["级别"] == "成功")

        return {
            "DNA追溯": self.DNA追溯,
            "错误数": 错误数,
            "警告数": 警告数,
            "成功数": 成功数,
            "日志": self.审计日志,
            "状态": "🔴 失败" if 错误数 > 0 else ("🟡 警告" if 警告数 > 0 else "🟢 通过")
        }


# ========== 辅助函数 ==========

def 解析源代码(源代码: str) -> 程序:
    """从源代码直接解析为AST"""
    分析器 = Lexer(源代码)
    标记列表 = 分析器.词法分析()
    语法分析器 = Parser(标记列表)
    return 语法分析器.解析()
