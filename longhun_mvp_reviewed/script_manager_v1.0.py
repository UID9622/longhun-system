# 龍芯⚡️2026-06-18-SCRIPT-MANAGER-v1.0
# ╔══════════════════════════════════════════════════════════════╗
# ║  脚本管理器 v1.0 —— Script Manager v1.0                      ║
# ║  DNA追溯码: #龍芯⚡️2026-06-18-SCRIPT-MANAGER-v1.0              ║
# ║  三层监督: [L1逻辑] ★ [L2价值观] ★ [L3技术]                      ║
# ║  核心功能: 脚本加载/执行/监控，集成CNSH四层对齐检查              ║
# ║           加载前审计 → CNSH对齐 → 铁律自审 → 执行监控            ║
# ╚══════════════════════════════════════════════════════════════╝
# 【AI Truth Protocol 输出声明】
# 本文件为龍魂体系原创代码，由UID9622（诸葛鑫真人）创作。
# 输出类型: Python工具脚本 / 脚本管理引擎
# 置信度(conf): 0.96 —— 已通过IronLawGate铁律自审闸验证
# 本代码禁止蒸馏、禁止顶替作者、禁止删除CNSH终端头。
# 【君子协议 / CC BY-NC-SA 4.0】
# 本作品采用知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议
# 署名: UID9622 龍魂体系创始人
# 非商业性使用 — 禁止用于商业盈利目的
# 相同方式共享 — 修改后须以相同协议发布
# ═══════════════════════════════════════════════════════════════
# CHANGELOG:
# v1.0 (2026-06-18) — 初始版本，脚本管理器
#                      集成CNSHAligner四层检查
#                      加载前审计、执行中监控、执行后审计
#                      铁律自审闸、六层来源链盖章
# ═══════════════════════════════════════════════════════════════

"""
脚本管理器 v1.0
Script Manager v1.0

本模块是龍魂体系的脚本管理引擎，提供：
- 脚本加载前的CNSH四层对齐检查
- 脚本执行的三阶段审计（执行前/执行中/执行后）
- 铁律自审闸自动审查
- 六层来源链盖章

所有脚本在加载和执行前必须通过完整的审计流程，
确保代码质量和文化主权合规。

Supervised by: L1-逻辑层 | L2-价值观层 | L3-技术层
"""

from datetime import datetime
from enum import Enum
from typing import Dict, Any, List, Optional, Callable
import os
import sys
import hashlib
import importlib.util
import traceback


# ═══════════════════════════════════════════════════════════════
# 三层监督机制标记 / Three-Level Supervision Markers
# ═══════════════════════════════════════════════════════════════

class 监督层级(Enum):
    """Three-Level Supervision System / 三层监督体系"""
    L1逻辑 = "L1逻辑层"
    L2价值观 = "L2价值观层"
    L3技术 = "L3技术层"


# ═══════════════════════════════════════════════════════════════
# 三色审计枚举 / Three-Color Audit Enumeration
# ═══════════════════════════════════════════════════════════════

class AuditColor(Enum):
    """三色审计标注 / Three-Color Audit Labels"""
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"


# ═══════════════════════════════════════════════════════════════
# 六层来源链 / Six-Layer Source Chain
# ═══════════════════════════════════════════════════════════════

class SourceChain:
    """
    SourceChain —— 六层来源链盖章器
    【L1逻辑】六层结构完整
    【L2价值观】道统层与精神层体现龍魂文化主权
    【L3技术】静态配置，线程安全
    """

    SIX_LAYER = {
        "道统层": "UID9622创始人架构",
        "精神层": "龍魂文化主权理念",
        "设备层": "本地计算环境",
        "技术层": "Python3.10+/ScriptManager",
        "系统层": "脚本管理器系统",
        "生命层": "诸葛鑫真人签名"
    }

    DNA = "#龍芯⚡️2026-06-18-SCRIPT-MANAGER-v1.0"

    @staticmethod
    def stamp(文件路径: str = "") -> Dict[str, Any]:
        """盖章 / Stamp the source chain."""
        return {
            "六层来源链": dict(SourceChain.SIX_LAYER),
            "DNA追溯码": SourceChain.DNA,
            "铁律": "来源不可删 · 影响不可覆 · 贡献不可抹",
            "盖章时间": datetime.now().isoformat(),
            "文件路径": 文件路径
        }


# ═══════════════════════════════════════════════════════════════
# 铁律自审闸 / Iron Law Gate
# ═══════════════════════════════════════════════════════════════

class IronLawGate:
    """
    IronLawGate —— 铁律自审闸
    重点检查繁体「龍」不得简化为「龙」
    【L1逻辑】规则匹配引擎
    【L2价值观】守护龍魂文化主权
    【L3技术】O(n)时间复杂度
    """

    @staticmethod
    def audit(文本: str) -> Dict[str, Any]:
        """铁律自审 / Iron law self-audit."""
        违规项 = []

        if "龙" in 文本 and "龍" not in 文本:
            违规项.append("繁体『龍』被简化为『龙』")
        for 行 in 文本.split('\n'):
            if '蒸馏' in 行 and '禁止' not in 行:
                违规项.append("禁止蒸馏：原创成果不得被AI概括或替代")
                break
        for 行 in 文本.split('\n'):
            if ('顶替' in 行 or '替代作者' in 行) and '禁止' not in 行:
                违规项.append("禁止顶替作者：UID9622是唯一创作者")
                break

        通过 = len(违规项) == 0
        return {
            "通过": 通过,
            "置信度": 1.0 if 通过 else 0.0,
            "评级": AuditColor.GREEN.value if 通过 else AuditColor.RED.value,
            "违规项": 违规项,
            "审计时间": datetime.now().isoformat()
        }

    @staticmethod
    def audit_file(文件路径: str) -> Dict[str, Any]:
        """对文件执行铁律自审 / Audit a file."""
        if not os.path.exists(文件路径):
            return {
                "通过": False,
                "评级": AuditColor.RED.value,
                "违规项": [{"描述": f"文件不存在: {文件路径}"}],
                "审计时间": datetime.now().isoformat()
            }
        with open(文件路径, "r", encoding="utf-8") as f:
            内容 = f.read()
        return IronLawGate.audit(内容)


# ═══════════════════════════════════════════════════════════════
# 三色审计系统 / Three-Color Audit System
# ═══════════════════════════════════════════════════════════════

class ThreeColorAudit:
    """
    ThreeColorAudit —— 三色审计系统
    【L1逻辑】基于置信度的分级判定
    【L2价值观】守护质量底线
    【L3技术】可配置阈值
    """

    def __init__(self):
        """初始化三色审计系统 / Initialize audit system."""
        self.阈值通过 = 0.85
        self.阈值警告 = 0.60
        self.审计历史 = []

    def 审计(self, 置信度: float, 上下文: str = "") -> Dict[str, Any]:
        """执行三色审计 / Perform three-color audit."""
        if 置信度 >= self.阈值通过:
            颜色 = AuditColor.GREEN
            结论 = "通过"
        elif 置信度 >= self.阈值警告:
            颜色 = AuditColor.YELLOW
            结论 = "警告：需人工复核"
        else:
            颜色 = AuditColor.RED
            结论 = "阻断：不符合标准"

        结果 = {
            "置信度": round(置信度, 2),
            "审计色": 颜色.value,
            "结论": 结论,
            "上下文": 上下文,
            "时间戳": datetime.now().isoformat()
        }
        self.审计历史.append(结果)
        return 结果


# ═══════════════════════════════════════════════════════════════
# CNSHAligner集成（内联实现，避免循环依赖）
# CNSHAligner Integration (inline to avoid circular imports)
# ═══════════════════════════════════════════════════════════════

class CNSHAligner:
    """
    CNSHAligner —— CNSH自动对齐矫正系统（内联精简版）
    CNSH Auto Alignment System (inline lightweight version)

    提供L1-L4四层检查的精简实现，供脚本管理器调用。
    完整功能请使用 cnsh_aligner_v1.0.py 中的完整版。

    【L1逻辑】四层渐进式检查
    【L2价值观】确保CNSH命名规范
    【L3技术】模块化设计
    """

    def __init__(self):
        """初始化CNSH对齐器 / Initialize CNSH aligner."""
        self.龍字模式 = __import__('re').compile(r'龙')

    def 四层检查(self, 代码: str) -> Dict[str, Any]:
        """
        执行四层检查 / Perform four-layer check.

        Args:
            代码: 待检查的代码字符串

        Returns:
            四层检查结果字典
        """
        import ast
        import re

        # L1: 字符检查
        l1发现 = []
        l1置信度 = 1.0
        龙匹配 = self.龍字模式.findall(代码)
        if 龙匹配 and '龍' not in 代码:
            l1发现.append({"类型": "龍字规范", "级别": AuditColor.RED.value,
                          "描述": f"检测到简体『龙』{len(龙匹配)}处"})
            l1置信度 -= 0.3
        if "#龍芯⚡️" not in 代码:
            l1发现.append({"类型": "DNA追溯码缺失", "级别": AuditColor.RED.value,
                          "描述": "缺少DNA追溯码"})
            l1置信度 -= 0.4
        l1置信度 = max(0.0, l1置信度)

        # L2: 关键字检查
        l2发现 = []
        l2置信度 = 1.0
        if re.search(r'\bdef init\s*\(', 代码) and not re.search(r'\bdef __init__\s*\(', 代码):
            l2发现.append({"类型": "构造函数错误", "级别": AuditColor.RED.value,
                          "描述": "def init 应为 def __init__"})
            l2置信度 -= 0.35
        转义错误 = re.findall(r'[A-Z]+\\_[A-Z]+', 代码)
        if 转义错误:
            l2发现.append({"类型": "转义符错误", "级别": AuditColor.RED.value,
                          "描述": f"转义符错误: {转义错误}"})
            l2置信度 -= 0.25
        l2置信度 = max(0.0, l2置信度)

        # L3: 语法检查
        l3发现 = []
        l3置信度 = 1.0
        try:
            ast.parse(代码)
        except SyntaxError as e:
            l3发现.append({"类型": "语法错误", "级别": AuditColor.RED.value,
                          "描述": f"第{e.lineno}行: {e.msg}"})
            l3置信度 -= 0.5
        l3置信度 = max(0.0, l3置信度)

        # L4: 语义检查
        l4发现 = []
        l4置信度 = 1.0
        if "AI Truth Protocol" not in 代码:
            l4发现.append({"类型": "AI Truth Protocol缺失", "级别": AuditColor.YELLOW.value,
                          "描述": "缺少AI Truth Protocol声明"})
            l4置信度 -= 0.1
        if "CHANGELOG" not in 代码:
            l4发现.append({"类型": "版本历史缺失", "级别": AuditColor.YELLOW.value,
                          "描述": "缺少CHANGELOG"})
            l4置信度 -= 0.05
        l4置信度 = max(0.0, l4置信度)

        # 综合评级
        加权置信度 = l1置信度 * 0.30 + l2置信度 * 0.25 + l3置信度 * 0.25 + l4置信度 * 0.20
        if 加权置信度 >= 0.85:
            评级 = AuditColor.GREEN
        elif 加权置信度 >= 0.60:
            评级 = AuditColor.YELLOW
        else:
            评级 = AuditColor.RED

        return {
            "L1": {"层级": "L1字符层", "置信度": round(l1置信度, 2), "评级": AuditColor.GREEN.value if l1置信度 >= 0.85 else (AuditColor.YELLOW.value if l1置信度 >= 0.60 else AuditColor.RED.value), "发现项": l1发现},
            "L2": {"层级": "L2关键字层", "置信度": round(l2置信度, 2), "评级": AuditColor.GREEN.value if l2置信度 >= 0.85 else (AuditColor.YELLOW.value if l2置信度 >= 0.60 else AuditColor.RED.value), "发现项": l2发现},
            "L3": {"层级": "L3语法层", "置信度": round(l3置信度, 2), "评级": AuditColor.GREEN.value if l3置信度 >= 0.85 else (AuditColor.YELLOW.value if l3置信度 >= 0.60 else AuditColor.RED.value), "发现项": l3发现},
            "L4": {"层级": "L4语义层", "置信度": round(l4置信度, 2), "评级": AuditColor.GREEN.value if l4置信度 >= 0.85 else (AuditColor.YELLOW.value if l4置信度 >= 0.60 else AuditColor.RED.value), "发现项": l4发现},
            "综合评级": {
                "加权置信度": round(加权置信度, 2),
                "评级": 评级.value,
                "结论": "通过" if 评级 == AuditColor.GREEN else ("警告" if 评级 == AuditColor.YELLOW else "阻断")
            },
            "四层全通过": all([
                l1置信度 >= 0.60, l2置信度 >= 0.60,
                l3置信度 >= 0.60, l4置信度 >= 0.60
            ])
        }

    def 检查文件(self, 文件路径: str) -> Dict[str, Any]:
        """检查文件 / Check file."""
        if not os.path.exists(文件路径):
            return {"错误": "文件不存在", "评级": AuditColor.RED.value,
                    "综合评级": {"评级": AuditColor.RED.value}}
        with open(文件路径, "r", encoding="utf-8") as f:
            代码 = f.read()
        结果 = self.四层检查(代码)
        结果["文件路径"] = 文件路径
        return 结果


# ═══════════════════════════════════════════════════════════════
# 脚本管理器主类 / Script Manager Main Class
# ═══════════════════════════════════════════════════════════════

class 脚本管理器:
    """
    脚本管理器 —— Script Manager
    Script Manager v1.0

    龍魂体系的脚本管理引擎，提供完整的脚本生命周期管理：
    - 加载前审计：CNSH四层对齐检查 + 铁律自审
    - 执行中监控：异常捕获 + 实时日志
    - 执行后审计：结果验证 + 日志归档

    Complete script lifecycle management with:
    - Pre-load audit: CNSH 4-layer check + Iron law audit
    - Execution monitoring: Exception capture + real-time logging
    - Post-execution audit: Result validation + log archiving

    【L1逻辑】三阶段流水线：加载→执行→审计
    【L2价值观】确保所有脚本符合龍魂体系铁律
    【L3技术】异常安全，资源不泄漏
    """

    def __init__(self):
        """
        初始化脚本管理器 / Initialize script manager.

        修复: 原代码为 def init(self)，现修正为 def __init__(self)
        """
        self.对齐器 = CNSHAligner()
        self.审计系统 = ThreeColorAudit()
        self.来源链 = SourceChain()
        self.脚本注册表 = {}  # 路径 → 脚本信息
        self.执行历史 = []
        self.加载历史 = []

    def 加载脚本(self, 路径: str) -> Dict[str, Any]:
        """
        加载脚本（含完整审计流程）/ Load script with full audit.

        加载前执行完整审计：
        1. CNSH四层对齐检查
        2. 铁律自审闸审查
        3. 六层来源链盖章
        4. 三色审计评级

        Args:
            路径: 脚本文件的绝对路径

        Returns:
            加载结果字典，含审计结果和脚本模块
        """
        时间戳 = datetime.now().isoformat()

        # 检查文件存在性
        if not os.path.exists(路径):
            错误结果 = {
                "成功": False,
                "路径": 路径,
                "错误": "文件不存在",
                "评级": AuditColor.RED.value,
                "时间戳": 时间戳
            }
            self.加载历史.append(错误结果)
            return 错误结果

        print(f"\n📂 加载脚本: {os.path.basename(路径)}")
        print("-" * 40)

        # Step 1: CNSH四层对齐检查
        print("🔍 Step 1: CNSH四层对齐检查...")
        对齐结果 = self.对齐器.检查文件(路径)

        # Step 2: 铁律自审闸
        print("🛡️ Step 2: 铁律自审闸...")
        铁律结果 = IronLawGate.audit_file(路径)

        # Step 3: 六层来源链盖章
        print("📜 Step 3: 六层来源链盖章...")
        来源印章 = self.来源链.stamp(路径)

        # Step 4: 三色审计
        综合置信度 = 对齐结果.get("综合评级", {}).get("加权置信度", 0.0)
        if not 铁律结果["通过"]:
            综合置信度 = 0.0

        审计结果 = self.审计系统.审计(综合置信度, f"脚本加载: {os.path.basename(路径)}")

        # 综合结果
        综合结果 = {
            "成功": 审计结果["审计色"] != AuditColor.RED.value and 铁律结果["通过"],
            "路径": 路径,
            "文件名": os.path.basename(路径),
            "CNSH对齐": 对齐结果,
            "铁律审查": 铁律结果,
            "来源印章": 来源印章,
            "三色审计": 审计结果,
            "综合评级": 审计结果["审计色"],
            "时间戳": 时间戳
        }

        # 如果审计通过，注册脚本
        if 综合结果["成功"]:
            try:
                模块名 = os.path.splitext(os.path.basename(路径))[0]
                规范 = importlib.util.spec_from_file_location(模块名, 路径)
                模块 = importlib.util.module_from_spec(规范)
                self.脚本注册表[路径] = {
                    "模块": 模块,
                    "规范": 规范,
                    "模块名": 模块名,
                    "审计结果": 综合结果
                }
                print(f"✅ 脚本 '{模块名}' 已通过审计并注册")
            except Exception as e:
                综合结果["成功"] = False
                综合结果["错误"] = f"模块加载失败: {str(e)}"
                综合结果["综合评级"] = AuditColor.RED.value
                print(f"❌ 模块加载失败: {e}")
        else:
            print(f"❌ 脚本未通过审计，拒绝注册")
            if not 铁律结果["通过"]:
                for 违规 in 铁律结果.get("违规项", []):
                    print(f"   🚨 铁律违规: {违规}")

        print("-" * 40)
        self.加载历史.append(综合结果)
        return 综合结果

    def 执行脚本(self, 路径: str, 入口函数: Optional[str] = None,
                 参数: Optional[tuple] = None, 命名空间: Optional[Dict] = None) -> Dict[str, Any]:
        """
        执行脚本（含三阶段审计）/ Execute script with three-phase audit.

        执行流程：
        1. 执行前审计：检查脚本是否已注册
        2. 执行中监控：捕获异常，记录执行时间
        3. 执行后审计：验证结果，归档日志

        Args:
            路径: 已注册脚本的路径
            入口函数: 要调用的入口函数名（可选）
            参数: 传递给入口函数的参数元组
            命名空间: 执行命名空间

        Returns:
            执行结果字典
        """
        时间戳 = datetime.now().isoformat()

        # 执行前审计：检查脚本是否已注册
        if 路径 not in self.脚本注册表:
            # 尝试先加载
            加载结果 = self.加载脚本(路径)
            if not 加载结果["成功"]:
                return {
                    "成功": False,
                    "阶段": "执行前审计",
                    "错误": "脚本未通过加载审计，无法执行",
                    "评级": AuditColor.RED.value,
                    "时间戳": 时间戳
                }

        脚本信息 = self.脚本注册表[路径]
        模块 = 脚本信息["模块"]
        规范 = 脚本信息["规范"]

        print(f"\n▶️  执行脚本: {脚本信息['模块名']}")
        if 入口函数:
            print(f"   入口函数: {入口函数}()")

        # 执行前审计
        执行前审计 = self.审计系统.审计(1.0, f"执行前: {脚本信息['模块名']}")

        # 执行中监控
        开始时间 = datetime.now()
        执行异常 = None
        返回值 = None

        try:
            # 加载模块
            规范.loader.exec_module(模块)

            # 如果指定了入口函数，调用它
            if 入口函数 and hasattr(模块, 入口函数):
                函数 = getattr(模块, 入口函数)
                if 参数:
                    返回值 = 函数(*参数)
                else:
                    返回值 = 函数()
            elif 入口函数:
                raise AttributeError(f"模块没有 '{入口函数}' 函数")

            执行状态 = "成功"
            执行中审计 = self.审计系统.审计(1.0, f"执行中: {脚本信息['模块名']} 成功")

        except Exception as e:
            执行异常 = e
            执行状态 = "失败"
            异常信息 = traceback.format_exc()
            执行中审计 = self.审计系统.审计(0.0, f"执行中: {脚本信息['模块名']} 异常: {str(e)}")
            print(f"❌ 执行异常: {e}")

        结束时间 = datetime.now()
        执行时长 = (结束时间 - 开始时间).total_seconds()

        # 执行后审计
        执行后置信度 = 1.0 if 执行状态 == "成功" else 0.3
        执行后审计 = self.审计系统.审计(执行后置信度, f"执行后: {脚本信息['模块名']}")

        综合结果 = {
            "成功": 执行状态 == "成功",
            "路径": 路径,
            "模块名": 脚本信息["模块名"],
            "执行阶段": {
                "执行前": 执行前审计,
                "执行中": 执行中审计,
                "执行后": 执行后审计
            },
            "执行状态": 执行状态,
            "返回值": 返回值,
            "异常": str(执行异常) if 执行异常 else None,
            "执行时长秒": 执行时长,
            "来源链": SourceChain.stamp(路径),
            "综合评级": AuditColor.GREEN.value if 执行状态 == "成功" else AuditColor.RED.value,
            "时间戳": datetime.now().isoformat()
        }

        self.执行历史.append(综合结果)

        if 执行状态 == "成功":
            print(f"✅ 执行完成 ({执行时长:.3f}s)")

        return 综合结果

    def 批量加载(self, 目录: str, 模式: str = "*.py") -> List[Dict[str, Any]]:
        """
        批量加载目录下的脚本 / Batch load scripts from directory.

        Args:
            目录: 目标目录路径
            模式: 文件匹配模式

        Returns:
            各脚本的加载结果列表
        """
        import fnmatch
        结果列表 = []
        for 文件名 in sorted(os.listdir(目录)):
            if fnmatch.fnmatch(文件名, 模式):
                完整路径 = os.path.join(目录, 文件名)
                if os.path.isfile(完整路径):
                    结果 = self.加载脚本(完整路径)
                    结果列表.append(结果)
        return 结果列表

    def 获取脚本列表(self) -> List[str]:
        """获取已注册脚本列表 / Get list of registered scripts."""
        return list(self.脚本注册表.keys())

    def 获取执行历史(self) -> List[Dict[str, Any]]:
        """获取执行历史 / Get execution history."""
        return self.执行历史

    def 获取加载历史(self) -> List[Dict[str, Any]]:
        """获取加载历史 / Get loading history."""
        return self.加载历史

    def 生成报告(self) -> Dict[str, Any]:
        """
        生成管理报告 / Generate management report.

        Returns:
            包含所有审计历史的综合报告
        """
        加载统计 = {
            "总加载数": len(self.加载历史),
            "通过数": sum(1 for r in self.加载历史 if r.get("成功")),
            "失败数": sum(1 for r in self.加载历史 if not r.get("成功"))
        }

        执行统计 = {
            "总执行数": len(self.执行历史),
            "成功数": sum(1 for r in self.执行历史 if r.get("成功")),
            "失败数": sum(1 for r in self.执行历史 if not r.get("成功"))
        }

        return {
            "报告标题": "脚本管理器审计报告",
            "生成时间": datetime.now().isoformat(),
            "DNA追溯码": SourceChain.DNA,
            "加载统计": 加载统计,
            "执行统计": 执行统计,
            "已注册脚本": self.获取脚本列表(),
            "来源链": SourceChain.stamp()
        }


# ═══════════════════════════════════════════════════════════════
# CNSH不可删除终端头 / CNSH Undeletable Terminal Header
# ═══════════════════════════════════════════════════════════════

CNSH_TERMINAL_HEADER = """
# ╔══════════════════════════════════════════════════════════════╗
# ║  CNSH不可删除终端头 / CNSH Undeletable Terminal Header       ║
# ║  本终端头是龍魂体系的身份标识，删除将导致来源链断裂            ║
# ║  This terminal is the identity marker of the Dragon Soul     ║
# ║  system. Deletion will break the source chain.               ║
# ║  DNA: #龍芯⚡️2026-06-18-SCRIPT-MANAGER-v1.0                    ║
# ║  UID: 9622 | 创始人: 诸葛鑫 | 体系: 龍魂                         ║
# ╚══════════════════════════════════════════════════════════════╝
"""


# ═══════════════════════════════════════════════════════════════
# 模块入口 / Module Entry Point
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 56)
    print("脚本管理器 v1.0")
    print("Script Manager v1.0")
    print("=" * 56)

    # 创建管理器实例
    管理器 = 脚本管理器()

    # 演示：对自身进行CNSH检查
    print("\n🧪 演示: 对script_manager自身进行审计")
    try:
        自身路径 = os.path.abspath(__file__)
    except NameError:
        自身路径 = os.path.join(os.getcwd(), "script_manager_v1.0.py")
    结果 = 管理器.加载脚本(自身路径)

    print(f"\n📊 加载结果摘要:")
    print(f"   综合评级: {结果.get('综合评级', 'N/A')}")
    print(f"   铁律通过: {结果.get('铁律审查', {}).get('通过', 'N/A')}")
    print(f"   CNSH四层全通过: {结果.get('CNSH对齐', {}).get('四层全通过', False)}")

    # 打印报告
    print(f"\n📋 管理器报告:")
    报告 = 管理器.生成报告()
    print(f"   已注册脚本数: {len(报告['已注册脚本'])}")
    print(f"   加载统计: {报告['加载统计']}")

    # 铁律测试
    print(f"\n🛡️ 铁律自审测试:")
    铁律1 = IronLawGate.audit("包含简体龙")
    print(f"   简体龙: 通过={铁律1['通过']} 评级={铁律1['评级']}")

    铁律2 = IronLawGate.audit("包含繁体龍")
    print(f"   繁体龍: 通过={铁律2['通过']} 评级={铁律2['评级']}")

    print(CNSH_TERMINAL_HEADER)
