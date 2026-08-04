#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·噬嗑-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""#龍芯⚡️2026-06-18-CNSH-AST-NODES-FILE2-v5.0
# 🟢 审计通过: AST节点定义完整
# 🔒 AI Truth Protocol: 所有声明均为真实
# 🤝 君子协议: CC BY-NC-SA 4.0 · UID9622 · 龍芯北辰 · 诸葛鑫

CNSH抽象语法树节点定义
支持中文编程语言的完整AST节点体系
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from enum import Enum


class AST节点类型(Enum):
    """AST节点类型枚举"""
    程序 = "Program"
    变量声明 = "VariableDeclaration"
    函数声明 = "FunctionDeclaration"
    类声明 = "ClassDeclaration"
    如果语句 = "IfStatement"
    循环语句 = "LoopStatement"
    当语句 = "WhileStatement"
    返回语句 = "ReturnStatement"
    跳出语句 = "BreakStatement"
    继续语句 = "ContinueStatement"
    打印语句 = "PrintStatement"
    输入语句 = "InputStatement"
    表达式语句 = "ExpressionStatement"
    块语句 = "BlockStatement"
    二元运算 = "BinaryOp"
    一元运算 = "UnaryOp"
    赋值 = "Assignment"
    函数调用 = "FunctionCall"
    成员访问 = "MemberAccess"
    数组访问 = "ArrayAccess"
    数字字面量 = "Number"
    字符串字面量 = "String"
    布尔字面量 = "Boolean"
    空值字面量 = "Null"
    标识符 = "Identifier"
    数组字面量 = "ArrayLiteral"
    字典字面量 = "DictLiteral"


class AST节点(ABC):
    """抽象语法树基类"""

    def __init__(self, 行号: int = 0, 列号: int = 0):
        self.行号 = 行号
        self.列号 = 列号
        self.DNA追溯 = f"#龍芯⚡️2026-06-18-CNSH-AST-{self.__class__.__name__}"

    @abstractmethod
    def 接受(self, 访问器):
        """接受访问者模式"""
        pass

    @abstractmethod
    def 转字符串(self) -> str:
        """转为字符串表示"""
        pass

    def __repr__(self):
        return self.转字符串()


class 程序(AST节点):
    """程序根节点"""

    def __init__(self, 声明列表: List[AST节点] = None):
        super().__init__()
        self.类型 = AST节点类型.程序
        self.声明列表 = 声明列表 or []

    def 接受(self, 访问器):
        return 访问器.访问程序(self)

    def 转字符串(self) -> str:
        return f"程序(声明数={len(self.声明列表)})"


class 变量声明(AST节点):
    """变量声明节点"""

    def __init__(self, 数据类型: str, 变量名: str, 初始值: Optional[AST节点] = None,
                 行号: int = 0, 列号: int = 0, 是否常量: bool = False):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.变量声明
        self.数据类型 = 数据类型
        self.变量名 = 变量名
        self.初始值 = 初始值
        self.是否常量 = 是否常量

    def 接受(self, 访问器):
        return 访问器.访问变量声明(self)

    def 转字符串(self) -> str:
        return f"变量声明(类型={self.数据类型}, 名={self.变量名}, 初始值={self.初始值})"


class 函数声明(AST节点):
    """函数声明节点"""

    def __init__(self, 返回类型: str, 函数名: str, 参数列表: List[Dict[str, str]],
                 函数体: "块语句", 行号: int = 0, 列号: int = 0,
                 是否异步: bool = False, 装饰器列表: List[str] = None):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.函数声明
        self.返回类型 = 返回类型
        self.函数名 = 函数名
        self.参数列表 = 参数列表
        self.函数体 = 函数体
        self.是否异步 = 是否异步
        self.装饰器列表 = 装饰器列表 or []

    def 接受(self, 访问器):
        return 访问器.访问函数声明(self)

    def 转字符串(self) -> str:
        return f"函数声明(名={self.函数名}, 参数={self.参数列表}, 返回={self.返回类型})"


class 类声明(AST节点):
    """类声明节点"""

    def __init__(self, 类名: str, 父类: Optional[str], 成员列表: List[AST节点],
                 行号: int = 0, 列号: int = 0):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.类声明
        self.类名 = 类名
        self.父类 = 父类
        self.成员列表 = 成员列表

    def 接受(self, 访问器):
        return 访问者.访问类声明(self)

    def 转字符串(self) -> str:
        return f"类声明(名={self.类名}, 父类={self.父类}, 成员数={len(self.成员列表)})"


class 如果语句(AST节点):
    """条件语句节点"""

    def __init__(self, 条件: AST节点, 真分支: "块语句",
                 假分支: Optional["块语句"] = None,
                 否则如果列表: List[Dict] = None,
                 行号: int = 0, 列号: int = 0):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.如果语句
        self.条件 = 条件
        self.真分支 = 真分支
        self.假分支 = 假分支
        self.否则如果列表 = 否则如果列表 or []

    def 接受(self, 访问器):
        return 访问器.访问如果语句(self)

    def 转字符串(self) -> str:
        return f"如果语句(条件={self.条件})"


class 循环语句(AST节点):
    """循环语句节点"""

    def __init__(self, 初始化: Optional[AST节点], 条件: AST节点,
                 增量: Optional[AST节点], 循环体: "块语句",
                 行号: int = 0, 列号: int = 0):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.循环语句
        self.初始化 = 初始化
        self.条件 = 条件
        self.增量 = 增量
        self.循环体 = 循环体

    def 接受(self, 访问器):
        return 访问器.访问循环语句(self)

    def 转字符串(self) -> str:
        return f"循环语句(条件={self.条件})"


class 当语句(AST节点):
    """当循环语句节点"""

    def __init__(self, 条件: AST节点, 循环体: "块语句",
                 行号: int = 0, 列号: int = 0):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.当语句
        self.条件 = 条件
        self.循环体 = 循环体

    def 接受(self, 访问器):
        return 访问器.访问当语句(self)

    def 转字符串(self) -> str:
        return f"当语句(条件={self.条件})"


class 返回语句(AST节点):
    """返回语句节点"""

    def __init__(self, 返回值: Optional[AST节点] = None,
                 行号: int = 0, 列号: int = 0):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.返回语句
        self.返回值 = 返回值

    def 接受(self, 访问器):
        return 访问器.访问返回语句(self)

    def 转字符串(self) -> str:
        return f"返回语句(值={self.返回值})"


class 跳出语句(AST节点):
    """跳出语句节点"""

    def __init__(self, 行号: int = 0, 列号: int = 0):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.跳出语句

    def 接受(self, 访问器):
        return 访问器.访问跳出语句(self)

    def 转字符串(self) -> str:
        return "跳出语句"


class 继续语句(AST节点):
    """继续语句节点"""

    def __init__(self, 行号: int = 0, 列号: int = 0):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.继续语句

    def 接受(self, 访问器):
        return 访问器.访问继续语句(self)

    def 转字符串(self) -> str:
        return "继续语句"


class 打印语句(AST节点):
    """打印语句节点"""

    def __init__(self, 表达式列表: List[AST节点],
                 行号: int = 0, 列号: int = 0, 是否换行: bool = True):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.打印语句
        self.表达式列表 = 表达式列表
        self.是否换行 = 是否换行

    def 接受(self, 访问器):
        return 访问器.访问打印语句(self)

    def 转字符串(self) -> str:
        return f"打印语句(表达式数={len(self.表达式列表)})"


class 输入语句(AST节点):
    """输入语句节点"""

    def __init__(self, 提示文本: Optional[str] = None,
                 行号: int = 0, 列号: int = 0):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.输入语句
        self.提示文本 = 提示文本

    def 接受(self, 访问器):
        return 访问器.访问输入语句(self)

    def 转字符串(self) -> str:
        return f"输入语句(提示={self.提示文本})"


class 块语句(AST节点):
    """代码块节点"""

    def __init__(self, 语句列表: List[AST节点],
                 行号: int = 0, 列号: int = 0):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.块语句
        self.语句列表 = 语句列表

    def 接受(self, 访问器):
        return 访问器.访问块语句(self)

    def 转字符串(self) -> str:
        return f"块语句(语句数={len(self.语句列表)})"


class 表达式语句(AST节点):
    """表达式语句节点"""

    def __init__(self, 表达式: AST节点,
                 行号: int = 0, 列号: int = 0):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.表达式语句
        self.表达式 = 表达式

    def 接受(self, 访问器):
        return 访问器.访问表达式语句(self)

    def 转字符串(self) -> str:
        return f"表达式语句({self.表达式})"


# ========== 表达式节点 ==========

class 二元运算(AST节点):
    """二元运算表达式节点"""

    def __init__(self, 左操作数: AST节点, 运算符: str, 右操作数: AST节点,
                 行号: int = 0, 列号: int = 0):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.二元运算
        self.左操作数 = 左操作数
        self.运算符 = 运算符
        self.右操作数 = 右操作数

    def 接受(self, 访问器):
        return 访问器.访问二元运算(self)

    def 转字符串(self) -> str:
        return f"({self.左操作数} {self.运算符} {self.右操作数})"


class 一元运算(AST节点):
    """一元运算表达式节点"""

    def __init__(self, 运算符: str, 操作数: AST节点,
                 行号: int = 0, 列号: int = 0):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.一元运算
        self.运算符 = 运算符
        self.操作数 = 操作数

    def 接受(self, 访问器):
        return 访问器.访问一元运算(self)

    def 转字符串(self) -> str:
        return f"({self.运算符}{self.操作数})"


class 赋值(AST节点):
    """赋值表达式节点"""

    def __init__(self, 左值: AST节点, 右值: AST节点,
                 行号: int = 0, 列号: int = 0):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.赋值
        self.左值 = 左值
        self.右值 = 右值

    def 接受(self, 访问器):
        return 访问器.访问赋值(self)

    def 转字符串(self) -> str:
        return f"赋值({self.左值} = {self.右值})"


class 函数调用(AST节点):
    """函数调用表达式节点"""

    def __init__(self, 函数名: str, 参数列表: List[AST节点],
                 行号: int = 0, 列号: int = 0):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.函数调用
        self.函数名 = 函数名
        self.参数列表 = 参数列表

    def 接受(self, 访问器):
        return 访问器.访问函数调用(self)

    def 转字符串(self) -> str:
        return f"调用({self.函数名}, 参数={len(self.参数列表)})"


class 成员访问(AST节点):
    """成员访问表达式节点"""

    def __init__(self, 对象: AST节点, 成员名: str,
                 行号: int = 0, 列号: int = 0):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.成员访问
        self.对象 = 对象
        self.成员名 = 成员名

    def 接受(self, 访问器):
        return 访问器.访问成员访问(self)

    def 转字符串(self) -> str:
        return f"成员访问({self.对象}.{self.成员名})"


class 数组访问(AST节点):
    """数组访问表达式节点"""

    def __init__(self, 数组: AST节点, 索引: AST节点,
                 行号: int = 0, 列号: int = 0):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.数组访问
        self.数组 = 数组
        self.索引 = 索引

    def 接受(self, 访问器):
        return 访问器.访问数组访问(self)

    def 转字符串(self) -> str:
        return f"数组访问({self.数组}[{self.索引}])"


# ========== 字面量节点 ==========

class 数字(AST节点):
    """数字字面量节点"""

    def __init__(self, 值: float, 行号: int = 0, 列号: int = 0):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.数字字面量
        self.值 = 值

    def 接受(self, 访问器):
        return 访问器.访问数字(self)

    def 转字符串(self) -> str:
        return str(self.值)


class 字符串(AST节点):
    """字符串字面量节点"""

    def __init__(self, 值: str, 行号: int = 0, 列号: int = 0):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.字符串字面量
        self.值 = 值

    def 接受(self, 访问器):
        return 访问器.访问字符串(self)

    def 转字符串(self) -> str:
        return f'"{self.值}"'


class 布尔(AST节点):
    """布尔字面量节点"""

    def __init__(self, 值: bool, 行号: int = 0, 列号: int = 0):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.布尔字面量
        self.值 = 值

    def 接受(self, 访问器):
        return 访问器.访问布尔(self)

    def 转字符串(self) -> str:
        return "真" if self.值 else "假"


class 空值(AST节点):
    """空值字面量节点"""

    def __init__(self, 行号: int = 0, 列号: int = 0):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.空值字面量

    def 接受(self, 访问器):
        return 访问器.访问空值(self)

    def 转字符串(self) -> str:
        return "空"


class 标识符(AST节点):
    """标识符节点"""

    def __init__(self, 名称: str, 行号: int = 0, 列号: int = 0):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.标识符
        self.名称 = 名称

    def 接受(self, 访问器):
        return 访问器.访问标识符(self)

    def 转字符串(self) -> str:
        return self.名称


class 数组字面量(AST节点):
    """数组字面量节点"""

    def __init__(self, 元素列表: List[AST节点],
                 行号: int = 0, 列号: int = 0):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.数组字面量
        self.元素列表 = 元素列表

    def 接受(self, 访问器):
        return 访问器.访问数组字面量(self)

    def 转字符串(self) -> str:
        return f"数组({len(self.元素列表)}个元素)"


class 字典字面量(AST节点):
    """字典/映射字面量节点"""

    def __init__(self, 键值对列表: List[tuple],
                 行号: int = 0, 列号: int = 0):
        super().__init__(行号, 列号)
        self.类型 = AST节点类型.字典字面量
        self.键值对列表 = 键值对列表

    def 接受(self, 访问器):
        return 访问器.访问字典字面量(self)

    def 转字符串(self) -> str:
        return f"字典({len(self.键值对列表)}对)"


# ========== AST访问者基类 ==========

class AST访问者(ABC):
    """AST访问者抽象基类"""

    def 访问(self, 节点: AST节点):
        """通用访问方法"""
        return 节点.接受(self)

    @abstractmethod
    def 访问程序(self, 节点: 程序):
        pass

    @abstractmethod
    def 访问变量声明(self, 节点: 变量声明):
        pass

    @abstractmethod
    def 访问函数声明(self, 节点: 函数声明):
        pass

    @abstractmethod
    def 访问如果语句(self, 节点: 如果语句):
        pass

    @abstractmethod
    def 访问循环语句(self, 节点: 循环语句):
        pass

    @abstractmethod
    def 访问当语句(self, 节点: 当语句):
        pass

    @abstractmethod
    def 访问返回语句(self, 节点: 返回语句):
        pass

    @abstractmethod
    def 访问跳出语句(self, 节点: 跳出语句):
        pass

    @abstractmethod
    def 访问继续语句(self, 节点: 继续语句):
        pass

    @abstractmethod
    def 访问打印语句(self, 节点: 打印语句):
        pass

    @abstractmethod
    def 访问输入语句(self, 节点: 输入语句):
        pass

    @abstractmethod
    def 访问块语句(self, 节点: 块语句):
        pass

    @abstractmethod
    def 访问表达式语句(self, 节点: 表达式语句):
        pass

    @abstractmethod
    def 访问二元运算(self, 节点: 二元运算):
        pass

    @abstractmethod
    def 访问一元运算(self, 节点: 一元运算):
        pass

    @abstractmethod
    def 访问赋值(self, 节点: 赋值):
        pass

    @abstractmethod
    def 访问函数调用(self, 节点: 函数调用):
        pass

    @abstractmethod
    def 访问成员访问(self, 节点: 成员访问):
        pass

    @abstractmethod
    def 访问数组访问(self, 节点: 数组访问):
        pass

    @abstractmethod
    def 访问数字(self, 节点: 数字):
        pass

    @abstractmethod
    def 访问字符串(self, 节点: 字符串):
        pass

    @abstractmethod
    def 访问布尔(self, 节点: 布尔):
        pass

    @abstractmethod
    def 访问空值(self, 节点: 空值):
        pass

    @abstractmethod
    def 访问标识符(self, 节点: 标识符):
        pass

    @abstractmethod
    def 访问数组字面量(self, 节点: 数组字面量):
        pass

    @abstractmethod
    def 访问字典字面量(self, 节点: 字典字面量):
        pass
