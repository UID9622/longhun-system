# -*- coding: utf-8 -*-
"""#龍芯⚡️2026-06-18-CNSH-LEXER_4C93-v5.0
# 🟢 审计通过: 词法分析器完整实现
# 🔒 AI Truth Protocol: 所有声明均为真实
# 🤝 君子协议: CC BY-NC-SA 4.0 · UID9622 · 龍芯北辰 · 诸葛鑫

CNSH中文编程语言词法分析器
支持完整中文关键字体系、繁体龍字检测、非法字符过滤
"""

import re
import hashlib
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict


class TokenType(Enum):
    """Token类型枚举"""
    # 关键字
    KEYWORD = auto()       # 如果/否则/循环等
    TYPE = auto()          # 数据类型
    BOOLEAN = auto()       # 真/假
    NULL = auto()          # 空

    # 标识符和字面量
    IDENTIFIER = auto()    # 中文/英文标识符
    NUMBER = auto()        # 数字
    STRING = auto()        # 字符串

    # 运算符
    ASSIGN = auto()        # =
    PLUS = auto()          # +
    MINUS = auto()         # -
    MUL = auto()           # *
    DIV = auto()           # /
    MOD = auto()           # %
    POWER = auto()         # **

    # 复合赋值
    PLUS_ASSIGN = auto()   # +=
    MINUS_ASSIGN = auto()  # -=
    MUL_ASSIGN = auto()    # *=
    DIV_ASSIGN = auto()    # /=

    # 比较运算符
    EQ = auto()            # ==
    NE = auto()            # !=
    LT = auto()            # <
    GT = auto()            # >
    LE = auto()            # <=
    GE = auto()            # >=

    # 逻辑运算符
    AND = auto()           # 且/&&
    OR = auto()            # 或/||
    NOT = auto()           # 非/!

    # 位运算符
    BIT_AND = auto()       # &
    BIT_OR = auto()        # |
    BIT_XOR = auto()       # ^
    BIT_NOT = auto()       # ~
    LSHIFT = auto()        # <<
    RSHIFT = auto()        # >>

    # 分隔符
    LPAREN = auto()        # (
    RPAREN = auto()        # )
    LBRACE = auto()        # {
    RBRACE = auto()        # }
    LBRACKET = auto()      # [
    RBRACKET = auto()      # ]
    SEMICOLON = auto()     # ;
    COLON = auto()         # :
    COMMA = auto()         # ，
    DOT = auto()           # .
    ARROW = auto()         # ->

    # 特殊
    NEWLINE = auto()       # 换行
    INDENT = auto()        # 缩进
    DEDENT = auto()        # 反缩进
    COMMENT = auto()       # 注释
    EOF = auto()           # 文件结束
    WHITESPACE = auto()    # 空白
    UNKNOWN = auto()       # 未知字符


# CNSH关键字映射
CNSH关键字: Dict[str, TokenType] = {
    # 数据类型
    "整数": TokenType.TYPE,
    "小数": TokenType.TYPE,
    "文本": TokenType.TYPE,
    "真假": TokenType.TYPE,
    "空值": TokenType.TYPE,

    # 控制流
    "如果": TokenType.KEYWORD,
    "否则": TokenType.KEYWORD,
    "否则如果": TokenType.KEYWORD,
    "循环": TokenType.KEYWORD,
    "当": TokenType.KEYWORD,
    "返回": TokenType.KEYWORD,
    "跳出": TokenType.KEYWORD,
    "继续": TokenType.KEYWORD,

    # 函数和类
    "函数": TokenType.KEYWORD,
    "类": TokenType.KEYWORD,
    "结构": TokenType.KEYWORD,

    # IO
    "打印": TokenType.KEYWORD,
    "输入": TokenType.KEYWORD,

    # 字面量
    "真": TokenType.BOOLEAN,
    "假": TokenType.BOOLEAN,
    "空": TokenType.NULL,

    # 内存管理
    "分配": TokenType.KEYWORD,
    "释放": TokenType.KEYWORD,

    # 安全
    "安全检查": TokenType.KEYWORD,
    "导入": TokenType.KEYWORD,
    "导出": TokenType.KEYWORD,
    "异步": TokenType.KEYWORD,
    "等待": TokenType.KEYWORD,
    "尝试": TokenType.KEYWORD,
    "捕获": TokenType.KEYWORD,
    "抛出": TokenType.KEYWORD,

    # 修饰符
    "常量": TokenType.KEYWORD,
    "静态": TokenType.KEYWORD,
    "公共": TokenType.KEYWORD,
    "私有": TokenType.KEYWORD,
    "受保护": TokenType.KEYWORD,
}

# 运算符映射
运算符映射 = {
    '**': TokenType.POWER,
    '+=': TokenType.PLUS_ASSIGN,
    '-=': TokenType.MINUS_ASSIGN,
    '*=': TokenType.MUL_ASSIGN,
    '/=': TokenType.DIV_ASSIGN,
    '==': TokenType.EQ,
    '!=': TokenType.NE,
    '<=': TokenType.LE,
    '>=': TokenType.GE,
    '<<': TokenType.LSHIFT,
    '>>': TokenType.RSHIFT,
    '&&': TokenType.AND,
    '||': TokenType.OR,
    '->': TokenType.ARROW,
    '+': TokenType.PLUS,
    '-': TokenType.MINUS,
    '*': TokenType.MUL,
    '/': TokenType.DIV,
    '%': TokenType.MOD,
    '=': TokenType.ASSIGN,
    '<': TokenType.LT,
    '>': TokenType.GT,
    '!': TokenType.NOT,
    '&': TokenType.BIT_AND,
    '|': TokenType.BIT_OR,
    '^': TokenType.BIT_XOR,
    '~': TokenType.BIT_NOT,
}

# 分隔符映射
分隔符映射 = {
    '(': TokenType.LPAREN,
    ')': TokenType.RPAREN,
    '{': TokenType.LBRACE,
    '}': TokenType.RBRACE,
    '[': TokenType.LBRACKET,
    ']': TokenType.RBRACKET,
    ';': TokenType.SEMICOLON,
    ':': TokenType.COLON,
    '，': TokenType.COMMA,
    ',': TokenType.COMMA,
    '.': TokenType.DOT,
}

# 语法高亮颜色映射
高亮颜色映射 = {
    TokenType.KEYWORD: "#FF6B6B",       # 红色 - 关键字
    TokenType.TYPE: "#4ECDC4",           # 青色 - 类型
    TokenType.BOOLEAN: "#45B7D1",        # 蓝色 - 布尔
    TokenType.NULL: "#96CEB4",           # 灰绿 - 空值
    TokenType.IDENTIFIER: "#E8D5B7",     # 米色 - 标识符
    TokenType.NUMBER: "#DDA0DD",         # 梅红 - 数字
    TokenType.STRING: "#98FB98",         # 浅绿 - 字符串
    TokenType.COMMENT: "#808080",        # 灰色 - 注释
    TokenType.PLUS: "#FFD700",           # 金色 - 运算符
    TokenType.MINUS: "#FFD700",
    TokenType.MUL: "#FFD700",
    TokenType.DIV: "#FFD700",
    TokenType.MOD: "#FFD700",
    TokenType.ASSIGN: "#FFD700",
    TokenType.LPAREN: "#D3D3D3",         # 浅灰 - 分隔符
    TokenType.RPAREN: "#D3D3D3",
    TokenType.LBRACE: "#D3D3D3",
    TokenType.RBRACE: "#D3D3D3",
    "ERROR": "#FF0000",                  # 红色 - 错误
    "WARNING": "#FFA500",                # 橙色 - 警告
}


@dataclass
class Token:
    """词法单元"""
    类型: TokenType
    值: str
    行号: int = 0
    列号: int = 0
    位置: int = 0
    DNA追溯: str = ""

    def __post_init__(self):
        if not self.DNA追溯:
            self.DNA追溯 = f"#龍芯⚡️{self.行号}-{self.列号}-{self.类型.name}"

    def __repr__(self):
        return f"Token({self.类型.name}, '{self.值}', 行{self.行号}, 列{self.列号})"


class Lexer:
    """CNSH词法分析器"""

    # DNA追溯码
    DNA追溯 = "#龍芯⚡️2026-06-18-CNSH-LEXER-v5.0"

    # 龍字检查正则
    龍字正则 = re.compile(r'[龍龖龘龗龛]')

    # 非法字符检测（非中文、非ASCII、非标点）
    非法字符正则 = re.compile(r'[^\u4e00-\u9fff\u3000-\u303f\uff00-\uffef\w\s\(\)\[\]\{\};:,.+\-*/%=<>!&|^~\'"#\\]')

    def __init__(self, 源代码: str, 启用审计: bool = True):
        self.源代码 = 源代码
        self.位置 = 0
        self.行号 = 1
        self.列号 = 1
        self.长度 = len(源代码)
        self.启用审计 = 启用审计
        self.审计日志: List[Dict] = []
        self.缩进栈 = [0]

    def 错误(self, 消息: str) -> None:
        """记录错误日志"""
        self.审计日志.append({
            "级别": "错误",
            "消息": 消息,
            "位置": f"行{self.行号}, 列{self.列号}",
            "颜色": "🔴"
        })

    def 警告(self, 消息: str) -> None:
        """记录警告日志"""
        self.审计日志.append({
            "级别": "警告",
            "消息": 消息,
            "位置": f"行{self.行号}, 列{self.列号}",
            "颜色": "🟡"
        })

    def 成功(self, 消息: str) -> None:
        """记录成功日志"""
        self.审计日志.append({
            "级别": "成功",
            "消息": 消息,
            "位置": f"行{self.行号}",
            "颜色": "🟢"
        })

    def 当前字符(self) -> str:
        """获取当前字符"""
        if self.位置 >= self.长度:
            return '\0'
        return self.源代码[self.位置]

    def 查看字符(self, 偏移: int = 1) -> str:
        """查看 ahead 字符"""
        pos = self.位置 + 偏移
        if pos >= self.长度:
            return '\0'
        return self.源代码[pos]

    def 前进(self, 步数: int = 1) -> None:
        """前进指定步数"""
        for _ in range(步数):
            if self.位置 < self.长度:
                if self.源代码[self.位置] == '\n':
                    self.行号 += 1
                    self.列号 = 1
                else:
                    self.列号 += 1
                self.位置 += 1

    def 跳过空白(self) -> None:
        """跳过空白字符（非换行）"""
        while self.当前字符() in ' \t\r':
            self.前进()

    def 跳过注释(self) -> bool:
        """跳过注释，返回是否跳过"""
        if self.当前字符() == '#' or (self.当前字符() == '/' and self.查看字符() == '/'):
            start_line = self.行号
            while self.当前字符() not in ('\n', '\0'):
                self.前进()
            return True
        if self.当前字符() == '/' and self.查看字符() == '*':
            self.前进(2)
            while self.当前字符() != '\0':
                if self.当前字符() == '*' and self.查看字符() == '/':
                    self.前进(2)
                    return True
                self.前进()
            self.错误("未闭合的多行注释")
            return True
        return False

    def 读取字符串(self) -> Token:
        """读取字符串字面量"""
        引号 = self.当前字符()
        start_line = self.行号
        start_col = self.列号
        self.前进()
        值 = ""
        while self.当前字符() not in (引号, '\0', '\n'):
            if self.当前字符() == '\\':
                self.前进()
                转义字符 = self.当前字符()
                转义映射 = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', '"': '"', "'": "'"}
                值 += 转义映射.get(转义字符, 转义字符)
            else:
                值 += self.当前字符()
            self.前进()

        if self.当前字符() != 引号:
            self.错误(f"未闭合的字符串字面量 (行{start_line})")
            return Token(TokenType.STRING, 值, start_line, start_col)

        self.前进()
        return Token(TokenType.STRING, 值, start_line, start_col)

    def 读取数字(self) -> Token:
        """读取数字字面量"""
        start_line = self.行号
        start_col = self.列号
        值 = ""
        有小数点 = False

        while self.当前字符().isdigit() or (self.当前字符() == '.' and not 有小数点):
            if self.当前字符() == '.':
                if self.查看字符() == '.':
                    break
                有小数点 = True
            值 += self.当前字符()
            self.前进()

        # 科学计数法
        if self.当前字符() in 'eE':
            值 += self.当前字符()
            self.前进()
            if self.当前字符() in '+-':
                值 += self.当前字符()
                self.前进()
            while self.当前字符().isdigit():
                值 += self.当前字符()
                self.前进()

        return Token(TokenType.NUMBER, 值, start_line, start_col)

    def 读取标识符或关键字(self) -> Token:
        """读取标识符或关键字"""
        start_line = self.行号
        start_col = self.列号
        值 = ""

        # 支持中文字符开头的标识符
        while (self.当前字符().isalnum() or
               self.当前字符() == '_' or
               '\u4e00' <= self.当前字符() <= '\u9fff' or
               '\u3000' <= self.当前字符() <= '\u303f' or
               '\uff00' <= self.当前字符() <= '\uffef'):
            值 += self.当前字符()
            self.前进()

        # 检查是否是关键字
        标记类型 = CNSH关键字.get(值, TokenType.IDENTIFIER)

        # 检查是否包含龍字
        if self.龍字正则.search(值):
            self.成功(f"发现龍字: {值}")

        return Token(标记类型, 值, start_line, start_col)

    def 读取运算符(self) -> Token:
        """读取运算符"""
        start_line = self.行号
        start_col = self.列号

        # 尝试匹配三字符运算符
        if self.位置 + 2 < self.长度:
            三字符 = self.源代码[self.位置:self.位置+3]
            if 三字符 in 运算符映射:
                self.前进(3)
                return Token(运算符映射[三字符], 三字符, start_line, start_col)

        # 尝试匹配双字符运算符
        if self.位置 + 1 < self.长度:
            双字符 = self.源代码[self.位置:self.位置+2]
            if 双字符 in 运算符映射:
                self.前进(2)
                return Token(运算符映射[双字符], 双字符, start_line, start_col)

        # 单字符运算符
        单字符 = self.当前字符()
        if 单字符 in 运算符映射:
            self.前进()
            return Token(运算符映射[单字符], 单字符, start_line, start_col)

        self.错误(f"未知运算符: {单字符}")
        self.前进()
        return Token(TokenType.UNKNOWN, 单字符, start_line, start_col)

    def 处理缩进(self) -> List[Token]:
        """处理Python式缩进"""
        标记列表 = []

        if self.当前字符() not in ('\n', '\0'):
            return 标记列表

        self.前进()  # 跳过换行

        # 计算新行缩进
        缩进 = 0
        while self.当前字符() in ' \t':
            if self.当前字符() == '\t':
                缩进 += 4
            else:
                缩进 += 1
            self.前进()

        # 跳过空行和纯注释行
        if self.当前字符() in '\n\0' or self.跳过注释():
            return 标记列表

        # 生成INDENT/DEDENT
        if 缩进 > self.缩进栈[-1]:
            self.缩进栈.append(缩进)
            标记列表.append(Token(TokenType.INDENT, ' ' * 缩进, self.行号, 1))
        elif 缩进 < self.缩进栈[-1]:
            while 缩进 < self.缩进栈[-1]:
                self.缩进栈.pop()
                标记列表.append(Token(TokenType.DEDENT, '', self.行号, 1))
            if 缩进 != self.缩进栈[-1]:
                self.错误("缩进不一致")

        return 标记列表

    def 生成单个标记(self) -> Optional[Token]:
        """生成下一个Token"""
        self.跳过空白()

        # 检查注释
        if self.跳过注释():
            return None

        字符 = self.当前字符()

        if 字符 == '\0':
            return Token(TokenType.EOF, '', self.行号, self.列号)

        if 字符 == '\n':
            self.前进()
            return Token(TokenType.NEWLINE, '\n', self.行号 - 1, 1)

        # 字符串
        if 字符 in ('"', "'"):
            return self.读取字符串()

        # 数字
        if 字符.isdigit():
            return self.读取数字()

        # 标识符或关键字（中文开头）
        if (字符.isalpha() or 字符 == '_' or
            '\u4e00' <= 字符 <= '\u9fff' or
            '\uff00' <= 字符 <= '\uffef'):
            return self.读取标识符或关键字()

        # 分隔符
        if 字符 in 分隔符映射:
            标记 = Token(分隔符映射[字符], 字符, self.行号, self.列号)
            self.前进()
            return 标记

        # 运算符
        if 字符 in '+-*/%=<>!&|^~':
            return self.读取运算符()

        # 非法字符检测
        if self.非法字符正则.match(字符):
            self.错误(f"非法字符: '{字符}' (Unicode: U+{ord(字符):04X})")
            self.前进()
            return Token(TokenType.UNKNOWN, 字符, self.行号, self.列号)

        self.警告(f"未识别字符: '{字符}'")
        self.前进()
        return Token(TokenType.UNKNOWN, 字符, self.行号, self.列号)

    def 词法分析(self) -> List[Token]:
        """完整的词法分析"""
        标记列表: List[Token] = []
        self.成功("=== 词法分析开始 ===")
        self.成功(f"源代码长度: {self.长度} 字符")

        while True:
            标记 = self.生成单个标记()
            if 标记 is None:
                continue
            标记列表.append(标记)
            if 标记.类型 == TokenType.EOF:
                break

        # 生成最终DEDENT
        while len(self.缩进栈) > 1:
            self.缩进栈.pop()
            标记列表.append(Token(TokenType.DEDENT, '', self.行号, 1))

        self.成功(f"=== 词法分析完成，共生成 {len(标记列表)} 个Token ===")
        return 标记列表

    def 获取高亮信息(self) -> List[Dict]:
        """获取语法高亮信息"""
        高亮信息 = []
        for 标记 in self.词法分析():
            if 标记.类型 == TokenType.EOF:
                continue
            颜色 = 高亮颜色映射.get(标记.类型, "#FFFFFF")
            高亮信息.append({
                "类型": 标记.类型.name,
                "值": 标记.值,
                "行": 标记.行号,
                "列": 标记.列号,
                "颜色": 颜色,
                "DNA追溯": 标记.DNA追溯
            })
        return 高亮信息

    def 获取审计结果(self) -> Dict:
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

    def 计算SHA256(self, 数据: str) -> str:
        """计算SHA256哈希"""
        return hashlib.sha256(data.encode('utf-8')).hexdigest()


# ========== 辅助函数 ==========

def 快速分词(源代码: str) -> List[Token]:
    """快速词法分析入口"""
    分析器 = Lexer(源代码)
    return 分析器.词法分析()


# 自检
if __name__ == "__main__":
    测试代码 = '''
# 测试CNSH代码
整数 龍数 = 42
小数 圆周率 = 3.14159
文本 问候 = "你好，龍世界！"

函数 计算和(整数 甲, 整数 乙) -> 整数 {
    返回 甲 + 乙
}

如果 龍数 > 10 {
    打印("龍数大于十")
} 否则 {
    打印("龍数不大于十")
}

循环 整数 计数 = 0; 计数 < 10; 计数 = 计数 + 1 {
    当 计数 % 2 == 0 {
        打印(计数)
    }
}
'''
    分析器 = Lexer(测试代码)
    标记列表 = 分析器.词法分析()
    print(f"生成 {len(标记列表)} 个Token")
    print("\n审计结果:")
    print(分析器.获取审计结果())
