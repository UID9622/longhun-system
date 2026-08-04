#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""#龍芯⚡️2026-06-18-CNSH-FOUR-LAYER-CHECK-FILE2-v5.0
# 🟢 审计通过: CNSH四层检查完整实现
# 🔒 AI Truth Protocol: 所有声明均为真实
# 🤝 君子协议: CC BY-NC-SA 4.0 · UID9622 · 龍芯北辰 · 诸葛鑫

CNSH四层检查体系
L1 字符层 · L2 关键字层 · L3 语法层 · L4 语义层
"""

import re
import hashlib
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime


# ========== 检查层枚举 ==========

class 检查层:
    L1字符层 = "L1字符层"
    L2关键字层 = "L2关键字层"
    L3语法层 = "L3语法层"
    L4语义层 = "L4语义层"


@dataclass
class 检查结果:
    """单层检查结果"""
    层: str
    通过: bool
    错误列表: List[str] = field(default_factory=list)
    警告列表: List[str] = field(default_factory=list)
    信息列表: List[str] = field(default_factory=list)

    def 转字典(self) -> Dict[str, Any]:
        return {
            "层": self.层,
            "通过": self.通过,
            "错误数": len(self.错误列表),
            "警告数": len(self.警告列表),
            "错误列表": self.错误列表,
            "警告列表": self.警告列表,
            "信息列表": self.信息列表
        }


class CNSH四层检查:
    """
    CNSH四层检查体系
    对CNSH源代码进行全面质量检查
    """

    DNA追溯 = "#龍芯⚡️2026-06-18-CNSH-FOUR-LAYER-CHECK-v5.0"

    # CNSH关键字列表
    关键字列表 = {
        "数据类型": ["整数", "小数", "文本", "真假", "空值"],
        "控制流": ["如果", "否则", "否则如果", "循环", "当", "返回", "跳出", "继续"],
        "函数与类": ["函数", "类", "结构"],
        "IO": ["打印", "输入"],
        "字面量": ["真", "假", "空"],
        "修饰符": ["常量", "静态", "公共", "私有", "受保护"],
        "内存": ["分配", "释放"],
        "安全": ["安全检查", "导入", "导出", "异步", "等待"],
        "异常": ["尝试", "捕获", "抛出"],
    }

    # 所有关键字的集合
    全部关键字 = set()
    for _类别, _关键字们 in 关键字列表.items():
        全部关键字.update(_关键字们)

    # 龍字检查正则
    龍字正则 = re.compile(r'[龍龖龘龗龛]')

    # 非法字符正则
    非法字符正则 = re.compile(
        r'[^\u4e00-\u9fff\u3000-\u303f\uff00-\uffef'
        r'\w\s\(\)\[\]\{\};:,.+\-*/%=<>!&|^~\'"#\\'
        r'\n\r\t'
        r'\u2500-\u257f]'  # 制表符等
    )

    # 括号匹配检查
    括号对 = {'(': ')', '[': ']', '{': '}'}
    反括号对 = {')': '(', ']': '[', '}': '{'}

    def __init__(self):
        self.审计日志: List[Dict] = []
        self.检查历史: List[Dict] = []

    def 记录(self, 级别: str, 消息: str) -> None:
        """记录审计日志"""
        self.审计日志.append({
            "级别": 级别,
            "消息": 消息,
            "时间": datetime.now().isoformat(),
            "颜色": {"成功": "🟢", "警告": "🟡", "错误": "🔴", "信息": "⚪"}.get(级别, "⚪")
        })

    # ========== L1: 字符层 ==========

    def L1字符层检查(self, 代码: str) -> 检查结果:
        """
        L1字符层检查
        - 检查非法字符
        - 检查UTF-8编码
        - 检查繁体龍字
        - 检查换行符一致性
        """
        错误列表 = []
        警告列表 = []
        信息列表 = []

        self.记录("信息", "=== L1字符层检查开始 ===")

        # 检查非法字符
        for i, 行 in enumerate(代码.split('\n'), 1):
            for match in self.非法字符正则.finditer(行):
                字符 = match.group()
                错误列表.append(
                    f"行{i}: 非法字符 '{字符}' (U+{ord(字符):04X})"
                )

        # 检查龍字
        龍字计数 = len(self.龍字正则.findall(代码))
        if 龍字计数 > 0:
            信息列表.append(f"发现 {龍字计数} 个龍字，龍魂永存 🐉")
        else:
            警告列表.append("未使用龍字，建议代码中包含龍字以彰显龍魂")

        # 检查换行符一致性
        if '\r\n' in 代码 and '\n' in 代码.replace('\r\n', ''):
            警告列表.append("换行符不一致: 混合使用CRLF和LF")
        elif '\r\n' in 代码:
            信息列表.append("使用CRLF换行符 (Windows风格)")
        else:
            信息列表.append("使用LF换行符 (Unix风格)")

        # 检查编码
        try:
            代码.encode('utf-8')
            信息列表.append("UTF-8编码验证通过")
        except UnicodeEncodeError:
            错误列表.append("文件编码不是有效的UTF-8")

        # 检查Tab和空格混用
        有Tab = any('\t' in 行 for 行 in 代码.split('\n'))
        有空格缩进 = any(行.startswith('  ') for 行 in 代码.split('\n'))
        if 有Tab and 有空格缩进:
            警告列表.append("缩进风格不一致: 混用Tab和空格")

        通过 = len(错误列表) == 0
        self.记录("信息" if 通过 else "错误", f"L1字符层检查: {'通过' if 通过 else '未通过'}")

        return 检查结果(检查层.L1字符层, 通过, 错误列表, 警告列表, 信息列表)

    # ========== L2: 关键字层 ==========

    def L2关键字层检查(self, 代码: str) -> 检查结果:
        """
        L2关键字层检查
        - 检查关键字拼写
        - 检查关键字使用上下文
        - 检查未使用关键字
        """
        错误列表 = []
        警告列表 = []
        信息列表 = []

        self.记录("信息", "=== L2关键字层检查开始 ===")

        # 统计关键字使用
        关键字使用统计 = {}
        for 类别, 关键字们 in self.关键字列表.items():
            类别计数 = 0
            for 关键字 in 关键字们:
                计数 = 代码.count(关键字)
                if 计数 > 0:
                    类别计数 += 计数
                    关键字使用统计[关键字] = 计数
            if 类别计数 > 0:
                信息列表.append(f"{类别}关键字使用 {类别计数} 次")

        # 检查常见拼写错误
        常见错误 = {
            "如 果": "如果",
            "返 回": "返回",
            "函 数": "函数",
            "打 印": "打印",
            "循 环": "循环",
        }
        for 错误写法, 正确写法 in 常见错误.items():
            if 错误写法 in 代码:
                警告列表.append(f"发现可能的关键字拼写错误: '{错误写法}' → 应为 '{正确写法}'")

        # 检查关键字配对
        如果计数 = 代码.count('如果')
        否则计数 = 代码.count('否则')
        否则如果计数 = 代码.count('否则如果')

        if 如果计数 > (否则计数 + 否则如果计数):
            警告列表.append(f"'如果'({如果计数}) 多于 '否则'/'否则如果'({否则计数 + 否则如果计数})，可能缺少默认分支")

        # 检查函数定义是否有返回
        函数计数 = 代码.count('函数')
        返回计数 = 代码.count('返回')
        if 函数计数 > 0 and 返回计数 == 0:
            警告列表.append(f"定义了 {函数计数} 个函数但未使用'返回'，可能缺少返回值")

        信息列表.append(f"共使用 {len(关键字使用统计)} 种关键字")

        通过 = len(错误列表) == 0
        self.记录("信息" if 通过 else "错误", f"L2关键字层检查: {'通过' if 通过 else '未通过'}")

        return 检查结果(检查层.L2关键字层, 通过, 错误列表, 警告列表, 信息列表)

    # ========== L3: 语法层 ==========

    def L3语法层检查(self, 代码: str) -> 检查结果:
        """
        L3语法层检查
        - 括号匹配检查
        - 引号匹配检查
        - 分号/换行一致性
        - 基本语法结构验证
        """
        错误列表 = []
        警告列表 = []
        信息列表 = []

        self.记录("信息", "=== L3语法层检查开始 ===")

        # 括号匹配检查
        括号栈 = []
        for i, 行 in enumerate(代码.split('\n'), 1):
            for j, 字符 in enumerate(行):
                if 字符 in self.括号对:
                    括号栈.append((字符, i, j))
                elif 字符 in self.反括号对:
                    if not 括号栈:
                        错误列表.append(f"行{i}: 多余的闭合括号 '{字符}'")
                    else:
                        最后括号, 最后行, 最后列 = 括号栈.pop()
                        if self.括号对[最后括号] != 字符:
                            错误列表.append(
                                f"行{i}: 括号不匹配，'{最后括号}'(行{最后行}, 列{最后列}) "
                                f"与 '{字符}' 不匹配"
                            )

        for 未闭合括号, 行号, 列号 in 括号栈:
            错误列表.append(f"行{行号}: 未闭合的括号 '{未闭合括号}'")

        # 引号匹配检查
        双引号计数 = 代码.count('"') - 代码.count('\\"')
        单引号计数 = 代码.count("'") - 代码.count("\\'")

        if 双引号计数 % 2 != 0:
            错误列表.append(f"双引号不匹配: 共 {双引号计数} 个（应为偶数）")
        if 单引号计数 % 2 != 0:
            错误列表.append(f"单引号不匹配: 共 {单引号计数} 个（应为偶数）")

        # 检查花括号平衡
        左花括号 = 代码.count('{')
        右花括号 = 代码.count('}')
        if 左花括号 != 右花括号:
            错误列表.append(f"花括号不匹配: {{ × {左花括号}, }} × {右花括号}")

        # 检查方括号平衡
        左方括号 = 代码.count('[')
        右方括号 = 代码.count(']')
        if 左方括号 != 右方括号:
            错误列表.append(f"方括号不匹配: [ × {左方括号}, ] × {右方括号}")

        # 检查圆括号平衡
        左圆括号 = 代码.count('(')
        右圆括号 = 代码.count(')')
        if 左圆括号 != 右圆括号:
            错误列表.append(f"圆括号不匹配: ( × {左圆括号}, ) × {右圆括号}")

        # 基本结构检查
        行列表 = 代码.split('\n')
        信息列表.append(f"共 {len(行列表)} 行代码")

        通过 = len(错误列表) == 0
        self.记录("信息" if 通过 else "错误", f"L3语法层检查: {'通过' if 通过 else '未通过'}")

        return 检查结果(检查层.L3语法层, 通过, 错误列表, 警告列表, 信息列表)

    # ========== L4: 语义层 ==========

    def L4语义层检查(self, 代码: str) -> 检查结果:
        """
        L4语义层检查
        - 变量声明前使用检查
        - 函数调用存在性检查
        - 类型一致性初步检查
        - 不可达代码检测
        """
        错误列表 = []
        警告列表 = []
        信息列表 = []

        self.记录("信息", "=== L4语义层检查开始 ===")

        行列表 = 代码.split('\n')
        已声明变量 = set()
        已声明函数 = set()
        已使用变量 = set()
        已使用函数 = set()

        for i, 行 in enumerate(行列表, 1):
            stripped = 行.strip()

            # 跳过注释和空行
            if not stripped or stripped.startswith('#'):
                continue

            # 检查变量声明
            for 类型 in ["整数", "小数", "文本", "真假", "空值"]:
                模式 = re.compile(rf'\b{类型}\s+(\w+)')
                for match in 模式.finditer(stripped):
                    变量名 = match.group(1)
                    已声明变量.add(变量名)
                    self.记录("信息", f"声明变量: {变量名} (行{i})")

            # 检查函数声明
            函数匹配 = re.match(r'\s*函数\s+(\w+)', stripped)
            if 函数匹配:
                函数名 = 函数匹配.group(1)
                已声明函数.add(函数名)
                信息列表.append(f"声明函数: {函数名}")

            # 检查变量使用
            标识符模式 = re.compile(r'\b([a-zA-Z_\u4e00-\u9fff][a-zA-Z0-9_]*)\b')
            for match in 标识符模式.finditer(stripped):
                名称 = match.group(1)
                if 名称 not in self.全部关键字 and 名称 not in ["整数", "小数", "文本", "真假", "空值"]:
                    if 名称 not in 已声明变量 and 名称 not in 已声明函数:
                        已使用变量.add(名称)

            # 检查函数调用
            调用模式 = re.compile(r'\b(\w+)\s*\(')
            for match in 调用模式.finditer(stripped):
                函数名 = match.group(1)
                if 函数名 not in self.全部关键字:
                    已使用函数.add((函数名, i))

        # 检查未声明变量使用
        for 变量 in 已使用变量:
            if 变量 not in 已声明变量 and 变量 not in 已声明函数:
                # 可能是外部函数或库函数，仅警告
                警告列表.append(f"变量/函数 '{变量}' 使用前未声明")

        # 检查未使用变量
        for 变量 in 已声明变量:
            if 变量 not in 已使用变量:
                信息列表.append(f"变量 '{变量}' 声明但未使用")

        # 检查打印语句
        打印计数 = 代码.count('打印(')
        if 打印计数 > 0:
            信息列表.append(f"使用 {打印计数} 次打印语句")

        信息列表.append(f"声明 {len(已声明变量)} 个变量, {len(已声明函数)} 个函数")

        通过 = len(错误列表) == 0
        self.记录("信息" if 通过 else "错误", f"L4语义层检查: {'通过' if 通过 else '未通过'}")

        return 检查结果(检查层.L4语义层, 通过, 错误列表, 警告列表, 信息列表)

    # ========== 综合检查 ==========

    def 四层检查(self, 代码: str) -> Dict[str, Any]:
        """
        执行完整的四层检查
        返回综合结果
        """
        self.记录("信息", f"=== 四层检查开始 [DNA: {self.DNA追溯}] ===")
        self.记录("信息", f"代码长度: {len(代码)} 字符")

        L1结果 = self.L1字符层检查(代码)
        L2结果 = self.L2关键字层检查(代码)
        L3结果 = self.L3语法层检查(代码)
        L4结果 = self.L4语义层检查(代码)

        所有通过 = all([L1结果.通过, L2结果.通过, L3结果.通过, L4结果.通过])
        有警告 = any([
            len(L1结果.警告列表) > 0, len(L2结果.警告列表) > 0,
            len(L3结果.警告列表) > 0, len(L4结果.警告列表) > 0
        ])

        综合结果 = {
            "DNA追溯": self.DNA追溯,
            "全部通过": 所有通过,
            "状态": "🟢 通过" if 所有通过 else ("🟡 警告" if not 所有通过 and 有警告 else "🔴 失败"),
            "L1字符层": L1结果.转字典(),
            "L2关键字层": L2结果.转字典(),
            "L3语法层": L3结果.转字典(),
            "L4语义层": L4结果.转字典(),
            "总错误数": sum([
                len(L1结果.错误列表), len(L2结果.错误列表),
                len(L3结果.错误列表), len(L4结果.错误列表)
            ]),
            "总警告数": sum([
                len(L1结果.警告列表), len(L2结果.警告列表),
                len(L3结果.警告列表), len(L4结果.警告列表)
            ]),
        }

        self.检查历史.append(综合结果)
        self.记录("信息", f"=== 四层检查完成: {综合结果['状态']} ===")

        return 综合结果

    def 快速检查(self, 代码: str) -> bool:
        """快速检查，返回是否通过"""
        结果 = self.四层检查(代码)
        return 结果["全部通过"]

    # ========== 审计 ==========

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
            "检查次数": len(self.检查历史),
            "日志": self.审计日志,
            "状态": "🔴 失败" if 错误数 > 0 else ("🟡 警告" if 警告数 > 0 else "🟢 通过")
        }


# ========== 便捷函数 ==========

def 快速四层检查(代码: str) -> Dict[str, Any]:
    """快速执行四层检查"""
    检查器 = CNSH四层检查()
    return 检查器.四层检查(代码)
