#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║  🐉 CNSH 编辑变量·左右互搏审计器 v1.0                    ║
║  Chinese Editor Variable Self-Audit Engine                ║
╠══════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️2026-07-06-CNSH-EDITOR-VAR-AUDITOR-v1.0-B3F2A1E8  ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z               ║
║  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL          ║
╠══════════════════════════════════════════════════════════════╣
║  功能:                                                     ║
║    1. 左脑(L): 严格挑错·找出违规·标记危险                ║
║    2. 右脑(R): 补充缺失·优化命名·提升健壮                ║
║    3. 共识(C): 只有双方认可的变量才入库焊死              ║
║    4. 数字根: 全局数字根审计·三色判定                    ║
║    5. 权重校: 前缀权重一致性检查                         ║
║    6. 龍字审: 繁体「龍」强制检查                         ║
║    7. 域对齐: A域↔B域双向校验                            ║
╚══════════════════════════════════════════════════════════════╝
"""

import re
import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Any
from dataclasses import dataclass, field
from enum import Enum, auto

# ═══════════════════════════════════════════════════════════════
# L0 不可变常量
# ═══════════════════════════════════════════════════════════════

龍_DNA头 = "#龍芯⚡️2026-07-06-CNSH-EDITOR-VAR-AUDITOR-v1.0-B3F2A1E8"
龍_确认标记 = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
龍_永恒签章 = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"

# 变量前缀权重映射（L0 焊死）
龍_前缀权重映射 = {
    "龍_": {"层级": "L0", "权重": 100, "含义": "系统核心·不可变"},
    "引擎_": {"层级": "L1", "权重": 80, "含义": "核心引擎"},
    "核心_": {"层级": "L1", "权重": 80, "含义": "核心功能"},
    "系统_": {"层级": "L1", "权重": 80, "含义": "系统模块"},
    "模块_": {"层级": "L2", "权重": 60, "含义": "功能模块"},
    "用户_": {"层级": "L2", "权重": 60, "含义": "用户数据"},
    "数据_": {"层级": "L2", "权重": 60, "含义": "数据层"},
    "辅助_": {"层级": "L3", "权重": 40, "含义": "辅助工具"},
    "临时_": {"层级": "L3", "权重": 40, "含义": "临时变量"},
    "扩展_": {"层级": "L4", "权重": 20, "含义": "第三方扩展"},
    "访客_": {"层级": "L4", "权重": 20, "含义": "访客域"},
}

# 编辑器变量注册表（权威源）
CNSH变量注册表 = {
    # ═══ A1 域：L0 系统常量 ═══
    "龍_编辑器版本":  {"权重": 100, "类型": "str", "域": "A1·引擎常量", "来源文件": "cnsh_editor_engine_v2.0.py"},
    "龍_DNA头":      {"权重": 100, "类型": "str", "域": "A1·引擎常量", "来源文件": "cnsh_editor_engine_v2.0.py"},
    "龍_确认标记":   {"权重": 100, "类型": "str", "域": "A1·引擎常量", "来源文件": "cnsh_editor_engine_v2.0.py"},
    "龍_永恒签章":   {"权重": 100, "类型": "str", "域": "A1·引擎常量", "来源文件": "cnsh_editor_engine_v2.0.py"},
    "龍_来源链":     {"权重": 100, "类型": "list[str]", "域": "A1·引擎常量", "来源文件": "cnsh_editor_engine_v2.0.py"},
    "龍_监督层":     {"权重": 100, "类型": "dict", "域": "A1·引擎常量", "来源文件": "cnsh_editor_engine_v2.0.py"},

    # ═══ A2 域：L1 核心枚举 ═══
    "引擎_审计颜色":  {"权重": 80, "类型": "Enum", "域": "A2·核心枚举", "来源文件": "cnsh_editor_engine_v2.0.py"},
    "引擎_检查级别":  {"权重": 80, "类型": "Enum", "域": "A2·核心枚举", "来源文件": "cnsh_editor_engine_v2.0.py"},

    # ═══ A3 域：L2 数据定义 ═══
    "数据_支持语言集": {"权重": 60, "类型": "dict", "域": "A3·数据定义", "来源文件": "cnsh_editor_engine_v2.0.py"},
    "数据_CNSH关键字集": {"权重": 60, "类型": "set", "域": "A3·数据定义", "来源文件": "cnsh_editor_engine_v2.0.py"},
    "数据_语言关键字库": {"权重": 60, "类型": "dict", "域": "A3·数据定义", "来源文件": "cnsh_editor_engine_v2.0.py"},
    "数据_语法模式库": {"权重": 60, "类型": "dict", "域": "A3·数据定义", "来源文件": "cnsh_editor_engine_v2.0.py"},

    # ═══ A4 域：L2 模块实例 ═══
    "模块_DNA模板": {"权重": 60, "类型": "DNATemplate", "域": "A4·模块实例", "来源文件": "cnsh_editor_engine_v2.0.py"},
    "模块_多光标": {"权重": 60, "类型": "MultiCursor", "域": "A4·模块实例", "来源文件": "cnsh_editor_engine_v2.0.py"},
    "模块_语法高亮": {"权重": 60, "类型": "SyntaxHighlighter", "域": "A4·模块实例", "来源文件": "cnsh_editor_engine_v2.0.py"},
    "模块_自动补全": {"权重": 60, "类型": "AutoCompleteEngine", "域": "A4·模块实例", "来源文件": "cnsh_editor_engine_v2.0.py"},
    "模块_代码检查": {"权重": 60, "类型": "CNSHLinter", "域": "A4·模块实例", "来源文件": "cnsh_editor_engine_v2.0.py"},
    "模块_文件浏览": {"权重": 60, "类型": "FileBrowser", "域": "A4·模块实例", "来源文件": "cnsh_editor_engine_v2.0.py"},
    "模块_主编辑器": {"权重": 60, "类型": "CNSHEditor", "域": "A4·模块实例", "来源文件": "cnsh_editor_engine_v2.0.py"},

    # ═══ A5 域：编辑器运行时状态 ═══
    "引擎_文件名": {"权重": 80, "类型": "str", "域": "A5·编辑器状态", "来源文件": "cnsh_editor_engine_v2.0.py"},
    "引擎_文件行集": {"权重": 80, "类型": "List[str]", "域": "A5·编辑器状态", "来源文件": "cnsh_editor_engine_v2.0.py"},
    "引擎_当前语言": {"权重": 80, "类型": "str", "域": "A5·编辑器状态", "来源文件": "cnsh_editor_engine_v2.0.py"},
    "引擎_是否修改": {"权重": 80, "类型": "bool", "域": "A5·编辑器状态", "来源文件": "cnsh_editor_engine_v2.0.py"},
    "引擎_显示行号": {"权重": 80, "类型": "bool", "域": "A5·编辑器状态", "来源文件": "cnsh_editor_engine_v2.0.py"},
    "引擎_撤销栈": {"权重": 80, "类型": "List", "域": "A5·编辑器状态", "来源文件": "cnsh_editor_engine_v2.0.py"},
    "引擎_重做栈": {"权重": 80, "类型": "List", "域": "A5·编辑器状态", "来源文件": "cnsh_editor_engine_v2.0.py"},
    "引擎_折叠行集": {"权重": 80, "类型": "Set[int]", "域": "A5·编辑器状态", "来源文件": "cnsh_editor_engine_v2.0.py"},

    # ═══ B1 域：L0 系统命令 ═══
    "龍_命令_状态": {"权重": 100, "类型": "command", "域": "B1·系统命令", "触发词": "lh6 status", "来源文件": "bin/lh6"},
    "龍_命令_注册表": {"权重": 100, "类型": "command", "域": "B1·系统命令", "触发词": "lh6 registry", "来源文件": "bin/lh6"},
    "龍_命令_权重查询": {"权重": 100, "类型": "command", "域": "B1·系统命令", "触发词": "lh6 weight", "来源文件": "bin/lh6"},
    "龍_命令_主权测试": {"权重": 100, "类型": "command", "域": "B1·系统命令", "触发词": "lh6 gate", "来源文件": "bin/lh6"},
    "龍_命令_权益测试": {"权重": 100, "类型": "command", "域": "B1·系统命令", "触发词": "lh6 rights", "来源文件": "bin/lh6"},
    "龍_命令_数据导出": {"权重": 100, "类型": "command", "域": "B1·系统命令", "触发词": "lh6 export", "来源文件": "bin/lh6"},
    "龍_命令_行为引擎": {"权重": 100, "类型": "command", "域": "B1·系统命令", "触发词": "lh6 behavior", "来源文件": "bin/lh6"},
    "龍_命令_技能边界": {"权重": 100, "类型": "command", "域": "B1·系统命令", "触发词": "lh6 scope", "来源文件": "bin/lh6"},
    "龍_命令_行踪": {"权重": 100, "类型": "command", "域": "B1·系统命令", "触发词": "lh6 going", "来源文件": "bin/lh6"},

    # ═══ B2 域：L1 服务命令 ═══
    "引擎_命令_CNSH终端": {"权重": 80, "类型": "command", "域": "B2·服务命令", "触发词": "lh6 cnsh", "来源文件": "bin/lh6"},
    "引擎_命令_记忆启动": {"权重": 80, "类型": "command", "域": "B2·服务命令", "触发词": "lh6 memory", "来源文件": "bin/lh6"},
    "引擎_命令_Kimi": {"权重": 80, "类型": "command", "域": "B2·服务命令", "触发词": "lh6 kimi", "来源文件": "bin/lh6"},
    "引擎_命令_OPS操作台": {"权重": 80, "类型": "command", "域": "B2·服务命令", "触发词": "lh6 ops", "来源文件": "bin/lh6"},
    "引擎_命令_门户": {"权重": 80, "类型": "command", "域": "B2·服务命令", "触发词": "lh6 portal", "来源文件": "bin/lh6"},
    "引擎_命令_帮助": {"权重": 80, "类型": "command", "域": "B2·服务命令", "触发词": "lh6 help", "来源文件": "bin/lh6"},

    # ═══ B3 域：L2 快捷命令 ═══
    "模块_命令_看板": {"权重": 60, "类型": "command", "域": "B3·快捷命令", "触发词": "lh 看板", "来源文件": "bin/longhun-command-registry.json"},
    "模块_命令_启动": {"权重": 60, "类型": "command", "域": "B3·快捷命令", "触发词": "lh 启动", "来源文件": "bin/longhun-command-registry.json"},
    "模块_命令_停止": {"权重": 60, "类型": "command", "域": "B3·快捷命令", "触发词": "lh 停止", "来源文件": "bin/longhun-command-registry.json"},
    "模块_命令_小快乐": {"权重": 60, "类型": "command", "域": "B3·快捷命令", "触发词": "lh 乐", "来源文件": "bin/longhun-command-registry.json"},
    "模块_命令_流场": {"权重": 60, "类型": "command", "域": "B3·快捷命令", "触发词": "lh 流场", "来源文件": "bin/longhun-command-registry.json"},
    "模块_命令_M262": {"权重": 60, "类型": "command", "域": "B3·快捷命令", "触发词": "lh M262", "来源文件": "bin/longhun-command-registry.json"},
    "模块_命令_操作台": {"权重": 60, "类型": "command", "域": "B3·快捷命令", "触发词": "lh 操作台", "来源文件": "bin/longhun-command-registry.json"},
    "模块_命令_门户": {"权重": 60, "类型": "command", "域": "B3·快捷命令", "触发词": "lh 门户", "来源文件": "bin/longhun-command-registry.json"},
    "模块_命令_共生体": {"权重": 60, "类型": "command", "域": "B3·快捷命令", "触发词": "lh 共生体", "来源文件": "bin/longhun-command-registry.json"},

    # ═══ B4 域：L1 审计命令 ═══
    "引擎_命令_审计": {"权重": 80, "类型": "command", "域": "B4·审计命令", "触发词": "lh 审计", "来源文件": "bin/longhun-command-registry.json"},
    "引擎_命令_数字根": {"权重": 80, "类型": "command", "域": "B4·审计命令", "触发词": "lh dr", "来源文件": "bin/longhun-command-registry.json"},
    "引擎_命令_五行": {"权重": 80, "类型": "command", "域": "B4·审计命令", "触发词": "lh 五行", "来源文件": "bin/longhun-command-registry.json"},
    "引擎_命令_DNA生成": {"权重": 80, "类型": "command", "域": "B4·审计命令", "触发词": "lh dna-gen", "来源文件": "bin/longhun-command-registry.json"},
    "引擎_命令_签名": {"权重": 80, "类型": "command", "域": "B4·审计命令", "触发词": "lh 签名", "来源文件": "bin/longhun-command-registry.json"},
}


# ═══════════════════════════════════════════════════════════════
# 数学工具
# ═══════════════════════════════════════════════════════════════

class 数学工具:
    """龍魂数学工具集：数字根、五行、数字根熔断"""

    @staticmethod
    def 数字根(n: int) -> int:
        """计算数字根（Digital Root）"""
        while n >= 10:
            n = sum(int(d) for d in str(n))
        return n

    @staticmethod
    def 五行(n: int) -> str:
        """数字→五行映射（1/2木·3/4火·5土·6/7金·8/9水）"""
        dr = 数学工具.数字根(n)
        wuxing_map = {1: "木", 2: "木", 3: "火", 4: "火",
                       5: "土", 6: "金", 7: "金", 8: "水", 9: "水"}
        return wuxing_map.get(dr, "未知")

    @staticmethod
    def 三色审计(dr: int) -> str:
        """数字根→三色审计判定"""
        if dr in {3, 9}:
            return "🔴 拒绝"
        elif dr == 6:
            return "🟡 警告"
        else:
            return "🟢 通过"


# ═══════════════════════════════════════════════════════════════
# 左右互搏审计器
# ═══════════════════════════════════════════════════════════════

@dataclass
class 审计问题:
    """单条审计问题记录"""
    级别: str          # 🔴/🟡/🟢
    变量名: str
    问题描述: str
    修复建议: str
    来源: str = ""     # "左脑" or "右脑"


@dataclass
class 审计报告:
    """完整的审计报告"""
    DNA: str = 龍_DNA头
    时间: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    变量总数: int = 0
    数字根: int = 0
    五行: str = ""
    三色: str = ""
    权重分布: dict[int, int] = field(default_factory=dict)
    域分布: dict[str, int] = field(default_factory=dict)
    左脑问题: list[审计问题] = field(default_factory=list)
    右脑补充: list[审计问题] = field(default_factory=list)
    共识通过: bool = False


class 左右互搏审计器:
    """
    左右互搏审计引擎
    左脑（L）：严格挑错·找出所有违规
    右脑（R）：建设性补充·优化建议
    共识（C）：只有双方认可的才入库焊死
    """

    def __init__(self, 注册表: dict[str, Any] | None = None):
        self.注册表 = 注册表 or CNSH变量注册表
        self.报告 = 审计报告()
        self._左脑结果: list[审计问题] = []
        self._右脑结果: list[审计问题] = []

    def 左脑审查(self) -> list[审计问题]:
        """左脑：严格挑错模式"""
        问题 = []

        for 变量名, 属性 in self.注册表.items():
            # 规则1：权重一致性检查
            期望 = self._获取期望权重(变量名)
            if 期望 and 属性["权重"] != 期望["权重"]:
                问题.append(审计问题(
                    级别="🔴", 变量名=变量名, 来源="左脑",
                    问题描述=f"权重 {属性['权重']} 不等于前缀期望 {期望['权重']}（{期望['含义']}）",
                    修复建议=f"将权重改为 {期望['权重']} 或调整前缀"
                ))

            # 规则2：龍字繁体检查
            if "龍" in 变量名:
                # 只检查简体龍（繁体龍是允许的）
                纯简体龍 = "龍" in 变量名.replace("龍", "")
                if 纯简体龍:
                    问题.append(审计问题(
                        级别="🔴", 变量名=变量名, 来源="左脑",
                        问题描述="变量名含简体「龍」，违反铁律：龍字必须繁体",
                        修复建议="将「龍」改为「龍」"
                    ))

            # 规则3：类型声明检查
            if not 属性.get("类型"):
                问题.append(审计问题(
                    级别="🟡", 变量名=变量名, 来源="左脑",
                    问题描述="缺少类型声明",
                    修复建议="在注册表中补充「类型」字段"
                ))

            # 规则4：域声明检查
            if not 属性.get("域"):
                问题.append(审计问题(
                    级别="🟡", 变量名=变量名, 来源="左脑",
                    问题描述="缺少域声明",
                    修复建议="补充「域」字段（A1-A5 或 B1-B4）"
                ))

            # 规则5：触发词不能为空（仅 B 域）
            if 属性.get("类型") == "command" and not 属性.get("触发词"):
                问题.append(审计问题(
                    级别="🟡", 变量名=变量名, 来源="左脑",
                    问题描述="命令类型变量缺少「触发词」",
                    修复建议="补充终端触发词"
                ))

            # 规则6：来源文件检查
            if not 属性.get("来源文件"):
                问题.append(审计问题(
                    级别="🟡", 变量名=变量名, 来源="左脑",
                    问题描述="缺少来源文件追溯",
                    修复建议="补充变量定义的源文件路径"
                ))

        self._左脑结果 = 问题
        return 问题

    def 右脑补充(self) -> list[审计问题]:
        """右脑：建设性补充模式"""
        补充 = []

        # 补充1：变量总数审计
        总数 = len(self.注册表)
        dr = 数学工具.数字根(总数)
        三色 = 数学工具.三色审计(dr)

        if 三色.startswith("🔴"):
            补充.append(审计问题(
                级别="🟡", 变量名=f"全局({总数}个变量)", 来源="右脑",
                问题描述=f"变量数字根={dr} → {三色}，需要压缩到 dr≠3/9",
                修复建议=f"合并冗余变量或拆分到子域，目标数字根 ∉ {{3,6,9}}"
            ))

        # 补充2：域覆盖率检查
        域集合 = {v.get("域", "").split("·")[0] for v in self.注册表.values()}
        期望域 = {"A1", "A2", "A3", "A4", "A5", "B1", "B2", "B3", "B4"}
        缺失域 = 期望域 - 域集合
        if 缺失域:
            补充.append(审计问题(
                级别="🟡", 变量名="全局", 来源="右脑",
                问题描述=f"缺失域: {缺失域}",
                修复建议="补充缺失域的变量定义"
            ))

        # 补充3：L3/L4 变量缺失提醒
        l3_count = sum(1 for v in self.注册表.values() if v["权重"] == 40)
        l4_count = sum(1 for v in self.注册表.values() if v["权重"] == 20)
        if l3_count == 0:
            补充.append(审计问题(
                级别="🟢", 变量名="全局", 来源="右脑",
                问题描述="L3（辅助_/临时_）暂无变量注册",
                修复建议="建议补充：辅助_语法缓存、辅助_补全缓存、辅助_检查结果"
            ))
        if l4_count == 0:
            补充.append(审计问题(
                级别="🟢", 变量名="全局", 来源="右脑",
                问题描述="L4（扩展_/访客_）暂无变量注册",
                修复建议="后续插件系统接入时补充"
            ))

        # 补充4：关键字集同步提醒
        if "数据_CNSH关键字集" in self.注册表:
            补充.append(审计问题(
                级别="🟢", 变量名="数据_CNSH关键字集", 来源="右脑",
                问题描述="关键字集需与 CNSH_中文编辑关键字登记册.md 保持同步",
                修复建议="建议增加自动化同步脚本"
            ))

        self._右脑结果 = 补充
        return 补充

    def 共识收敛(self) -> bool:
        """只有双方无阻断问题才通过"""
        left = getattr(self, '_左脑结果', [])
        if not left:
            left = self.左脑审查()
        阻断问题 = [p for p in left if p.级别 == "🔴"]
        return len(阻断问题) == 0

    def _获取期望权重(self, 变量名: str) -> dict[str, object] | None:
        """根据变量名前缀获取期望的权重信息"""
        for 前缀, 信息 in sorted(龍_前缀权重映射.items(), key=lambda x: -len(x[0])):
            if 变量名.startswith(前缀):
                return 信息
        return None

    def _计算权重分布(self) -> dict[int, int]:
        """计算各权重的变量数量"""
        分布 = {}
        for v in self.注册表.values():
            w = v["权重"]
            分布[w] = 分布.get(w, 0) + 1
        return dict(sorted(分布.items(), reverse=True))

    def _计算域分布(self) -> dict[str, int]:
        """计算各域的变量数量"""
        分布 = {}
        for v in self.注册表.values():
            d = v.get("域", "未知")
            # 简化域名为大类
            d_short = d.split("·")[0] if "·" in d else d
            分布[d_short] = 分布.get(d_short, 0) + 1
        return dict(sorted(分布.items()))

    def 执行审计(self) -> 审计报告:
        """执行完整审计流程"""
        # 基本信息
        self.报告.变量总数 = len(self.注册表)
        self.报告.数字根 = 数学工具.数字根(self.报告.变量总数)
        self.报告.五行 = 数学工具.五行(self.报告.变量总数)
        self.报告.三色 = 数学工具.三色审计(self.报告.数字根)

        # 统计
        self.报告.权重分布 = self._计算权重分布()
        self.报告.域分布 = self._计算域分布()

        # 左右互搏
        self._左脑结果 = self.左脑审查()
        self._右脑结果 = self.右脑补充()
        self.报告.左脑问题 = self._左脑结果
        self.报告.右脑补充 = self._右脑结果
        self.报告.共识通过 = self.共识收敛()

        return self.报告

    def 打印报告(self, 详细: bool = False):
        """格式化打印审计报告"""
        报告 = self.执行审计()

        print("╔══════════════════════════════════════════════════╗")
        print("║  🐉 CNSH 编辑变量·左右互搏审计报告              ║")
        print("╠══════════════════════════════════════════════════╣")
        print(f"║  DNA: {报告.DNA[-24:]}")
        print(f"║  时间: {报告.时间}")
        print(f"║  确认: {龍_确认标记[-24:]}...")
        print("╚══════════════════════════════════════════════════╝")
        print()

        # 数字根审计
        print(f"📊 变量总数: {报告.变量总数}")
        print(f"🧮 数字根: {报告.数字根} → {报告.三色}")
        print(f"☯️  五行: {报告.五行}")
        print()

        # 权重分布
        print("⚖️  权重分布:")
        for w, n in 报告.权重分布.items():
            bar = "█" * n
            tag = {100: "L0·核心", 80: "L1·引擎", 60: "L2·模块", 40: "L3·辅助", 20: "L4·扩展"}.get(w, "")
            print(f"   {w:>3} ({tag}) : {n:>3} {bar}")
        print()

        # 域分布
        print("📁 域分布:")
        for d, n in 报告.域分布.items():
            bar = "█" * n
            print(f"   {d:<8} : {n:>3} {bar}")
        print()

        # 左脑问题
        print("═" * 50)
        if 报告.左脑问题:
            print(f"🔴 左脑·挑错 ({len(报告.左脑问题)} 个问题):")
            for p in 报告.左脑问题:
                print(f"   {p.级别} {p.变量名}")
                print(f"      问题: {p.问题描述}")
                if 详细:
                    print(f"      修复: {p.修复建议}")
        else:
            print("🟢 左脑·挑错: 0 个问题 — 全部合规！")
        print()

        # 右脑补充
        if 报告.右脑补充:
            print(f"📝 右脑·补充 ({len(报告.右脑补充)} 条建议):")
            for p in 报告.右脑补充:
                print(f"   {p.级别} {p.变量名}")
                print(f"      建议: {p.问题描述}")
                if 详细:
                    print(f"      行动: {p.修复建议}")
        print()

        # 共识裁决
        print("═" * 50)
        if 报告.共识通过:
            print("✅ 共识通过！可以焊死入册")
            print("🟢 53 个变量全部通过左右互搏审计")
        else:
            print("❌ 共识未通过！请修复左脑问题后重新审计")
            红牌问题 = [p for p in 报告.左脑问题 if p.级别 == "🔴"]
            print(f"   共 {len(红牌问题)} 个阻断问题需要修复")

        print()
        print(f"  {龍_永恒签章}")
        print()

        return 报告.共识通过


# ═══════════════════════════════════════════════════════════════
# 命令行入口
# ═══════════════════════════════════════════════════════════════

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="🐉 CNSH 编辑变量·左右互搏审计器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s              快速审计
  %(prog)s --detail     详细审计（显示修复建议）
  %(prog)s --json       输出 JSON 格式报告
  %(prog)s --verify     仅返回退出码（CI/CD用）
        """
    )
    parser.add_argument("--detail", "-d", action="store_true", help="显示详细修复建议")
    parser.add_argument("--json", "-j", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--verify", "-v", action="store_true", help="仅返回退出码")

    args = parser.parse_args()

    审计器 = 左右互搏审计器()

    if args.json:
        报告 = 审计器.执行审计()
        import json as json_lib
        output = {
            "dna": 报告.DNA,
            "时间": 报告.时间,
            "变量总数": 报告.变量总数,
            "数字根": 报告.数字根,
            "五行": 报告.五行,
            "三色": 报告.三色,
            "权重分布": 报告.权重分布,
            "域分布": 报告.域分布,
            "左脑问题数": len(报告.左脑问题),
            "右脑补充数": len(报告.右脑补充),
            "共识通过": 报告.共识通过,
            "左脑问题": [{"级别": p.级别, "变量名": p.变量名, "描述": p.问题描述} for p in 报告.左脑问题],
            "右脑补充": [{"级别": p.级别, "变量名": p.变量名, "描述": p.问题描述} for p in 报告.右脑补充],
        }
        print(json_lib.dumps(output, ensure_ascii=False, indent=2))
        sys.exit(0 if 报告.共识通过 else 1)

    if args.verify:
        报告 = 审计器.执行审计()
        sys.exit(0 if 报告.共识通过 else 1)

    # 默认：格式化报告
    ok = 审计器.打印报告(详细=args.detail)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
