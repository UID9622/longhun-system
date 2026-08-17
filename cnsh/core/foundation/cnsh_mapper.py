#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
🐉 CNSH 语义映射引擎
中文AST → 英文AST

DNA: #龍芯⚡️丙午·丙申·辛酉·寅时-MAPPER-UID9622
"""

import hashlib
import re
from typing import Dict, Optional


# ============================================================
# 语义映射表
# ============================================================

class SemanticMapper:
    """中文→英文语义映射器"""

    KEYWORD_MAP = {
        # 控制流
        "函数": "def",
        "类": "class",
        "如果": "if",
        "否则": "else",
        "否则如果": "elif",
        "循环": "for",
        "当": "while",
        "返回": "return",
        "导入": "import",
        "从": "from",
        "真": "True",
        "假": "False",
        "空": "None",
        "且": "and",
        "或": "or",
        "非": "not",
        "在": "in",
        "是": "is",
        "使用": "with",
        "作为": "as",
        "尝试": "try",
        "捕获": "except",
        "最终": "finally",
        "抛出": "raise",
        "生成": "yield",
        "异步": "async",
        "等待": "await",
        "匿名函数": "lambda",
        "全局": "global",
        "非局部": "nonlocal",
        "删除": "del",
        "通过": "pass",
        "跳出": "break",
        "继续": "continue",
        # 类型
        "整数": "int",
        "文本": "str",
        "列表": "list",
        "字典": "dict",
        "元组": "tuple",
        "集合": "set",
        "布尔": "bool",
        "浮点": "float",
        # 内置函数
        "输出": "print",
        "长度": "len",
        "类型": "type",
        "区间": "range",
        "枚举": "enumerate",
        "压缩": "zip",
        "映射": "map",
        "过滤": "filter",
        "求和": "sum",
        "最大值": "max",
        "最小值": "min",
        "排序": "sorted",
        "反转": "reversed",
        "打开": "open",
        "读取": "read",
        "写入": "write",
        "关闭": "close",
    }

    PUNCTUATION_MAP = {
        "。": ".",
        "，": ",",
        "！": "!",
        "？": "?",
        "；": ";",
        "：": ":",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "（": "(",
        "）": ")",
        "【": "[",
        "】": "]",
        "《": "<",
        "》": ">",
        "……": "...",
        "—": "-",
    }

    @classmethod
    def map_keyword(cls, keyword: str) -> str:
        """映射关键字"""
        return cls.KEYWORD_MAP.get(keyword, keyword)

    @classmethod
    def map_punctuation(cls, punct: str) -> str:
        """映射标点符号"""
        return cls.PUNCTUATION_MAP.get(punct, punct)

    @classmethod
    def map_code(cls, code: str, identifier_map: Optional[Dict[str, str]] = None) -> str:
        """映射整段代码：关键字→英文，标点→英文，标识符按需转换"""
        identifier_map = identifier_map or {}
        lines = code.split("\n")
        result = []

        for line in lines:
            # 保护字符串内容不被映射
            pieces = re.split(r'("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')', line)
            mapped_pieces = []

            for idx, piece in enumerate(pieces):
                if idx % 2 == 1:  # 字符串片段
                    mapped_pieces.append(piece)
                    continue

                # 逐词映射
                # 拆分出中文词、英文词、数字、操作符、分隔符
                tokens = re.findall(
                    r'[\u4e00-\u9fff]+|[a-zA-Z_][a-zA-Z0-9_]*|\d+\.?\d*|[+\-*/=<>!]+|[():;,.\[\]{}]',
                    piece,
                )
                mapped = []
                pos = 0
                for tok in tokens:
                    # 保留原字符串中的间隔
                    start = piece.find(tok, pos)
                    mapped.append(piece[pos:start])
                    pos = start + len(tok)

                    if tok in cls.KEYWORD_MAP:
                        mapped.append(cls.KEYWORD_MAP[tok])
                    elif tok in cls.PUNCTUATION_MAP:
                        mapped.append(cls.PUNCTUATION_MAP[tok])
                    elif tok in identifier_map:
                        mapped.append(identifier_map[tok])
                    elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', tok):
                        mapped.append(tok)
                    elif re.match(r'^\d+\.?\d*$', tok):
                        mapped.append(tok)
                    elif tok in "():;,.[]{}" or re.match(r'^[+\-*/=<>!]+$', tok):
                        mapped.append(tok)
                    else:
                        # 未映射的中文标识符：保持原样（执行层仍可用中文变量名）
                        mapped.append(tok)

                mapped.append(piece[pos:])
                mapped_pieces.append("".join(mapped))

            result.append("".join(mapped_pieces))

        return "\n".join(result)


# ============================================================
# 智能变量名映射 (保留语义)
# ============================================================

class SmartIdentifierMapper:
    """智能标识符映射器 - 将中文变量名映射为有意义的英文名"""

    COMMON_MAP = {
        "价格": "price",
        "数量": "quantity",
        "名称": "name",
        "描述": "description",
        "用户": "user",
        "订单": "order",
        "商品": "product",
        "类别": "category",
        "状态": "status",
        "创建时间": "created_at",
        "更新时间": "updated_at",
        "删除时间": "deleted_at",
        "是否有效": "is_active",
        "是否删除": "is_deleted",
        "总数": "total",
        "金额": "amount",
        "折扣": "discount",
        "折扣率": "discount_rate",
        "税率": "tax_rate",
        "利润": "profit",
        "成本": "cost",
        "收入": "revenue",
        "支出": "expense",
        "余额": "balance",
        "账户": "account",
        "密码": "password",
        "邮箱": "email",
        "电话": "phone",
        "地址": "address",
        "城市": "city",
        "省份": "province",
        "国家": "country",
        "邮编": "zipcode",
        "备注": "remark",
        "类型": "type",
        "编号": "id",
        "代码": "code",
        "结果": "result",
        "数据": "data",
        "列表": "list",
        "字典": "dict",
        "配置": "config",
        "设置": "settings",
        "选项": "options",
        "参数": "params",
        "返回值": "return_value",
        "异常": "exception",
        "错误": "error",
        "信息": "info",
        "日志": "log",
        "缓存": "cache",
        "会话": "session",
        "令牌": "token",
        "密钥": "key",
        "签名": "signature",
        "哈希": "hash",
        "验证": "verify",
        "认证": "auth",
        "授权": "authorize",
    }

    @classmethod
    def map(cls, chinese_name: str) -> str:
        """映射中文标识符到英文"""
        if chinese_name in cls.COMMON_MAP:
            return cls.COMMON_MAP[chinese_name]

        for cn, en in cls.COMMON_MAP.items():
            if cn in chinese_name:
                return en

        try:
            from pypinyin import lazy_pinyin

            pinyin = "_".join(lazy_pinyin(chinese_name))
            return pinyin or f"cn_{hashlib.md5(chinese_name.encode()).hexdigest()[:8]}"
        except Exception:
            return f"cn_{hashlib.md5(chinese_name.encode()).hexdigest()[:8]}"

    @classmethod
    def build_map(cls, code: str) -> Dict[str, str]:
        """从代码中自动构建中文标识符映射表"""
        mapping = {}
        # 简单提取可能的中文变量名
        tokens = re.findall(r'[\u4e00-\u9fff]{2,}', code)
        for tok in set(tokens):
            mapping[tok] = cls.map(tok)
        return mapping


# ============================================================
# 测试
# ============================================================


def test_mapper():
    """测试映射引擎"""
    code = """
    函数 计算折扣(价格, 折扣率):
        返回 价格 * 折扣率

    类 商品:
        函数 初始化(名称, 价格):
            这个.名称 = 名称
            这个.价格 = 价格
    """

    print("🐉 CNSH 语义映射结果")
    print("=" * 50)
    print("原始中文代码:")
    print(code)

    # 先构建标识符映射
    identifier_map = SmartIdentifierMapper.build_map(code)
    print("\n标识符映射表:")
    for k, v in identifier_map.items():
        print(f"  {k} → {v}")

    print("\n映射后英文代码:")
    mapped = SemanticMapper.map_code(code, identifier_map=identifier_map)
    print(mapped)

    return mapped


if __name__ == "__main__":
    test_mapper()
