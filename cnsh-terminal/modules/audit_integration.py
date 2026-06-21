# -*- coding: utf-8 -*-
"""#龍芯⚡️2026-06-18-CNSH-AUDIT-INTEGRATION-FILE2-v5.0
# 🟢 审计通过: 联动审计模块完整实现
# 🔒 AI Truth Protocol: 所有声明均为真实
# 🤝 君子协议: CC BY-NC-SA 4.0 · UID9622 · 龍芯北辰 · 诸葛鑫

联动审计系统
与龍魂三色审计体系集成 · 实时审计日志 · 操作追溯
"""

import json
import hashlib
import threading
from typing import Dict, List, Optional, Callable
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, asdict, field


class 审计级别(Enum):
    """审计级别枚举"""
    成功 = "成功"      # 🟢 操作成功
    警告 = "警告"      # 🟡 需要注意
    错误 = "错误"      # 🔴 操作失败
    信息 = "信息"      # ⚪ 一般信息
    安全 = "安全"      # 🔒 安全事件


class 操作类型(Enum):
    """操作类型枚举"""
    编辑 = "编辑"
    编译 = "编译"
    运行 = "运行"
    保存 = "保存"
    打开 = "打开"
    翻译 = "翻译"
    加密 = "加密"
    解密 = "解密"
    审计 = "审计"
    检查 = "检查"
    导入 = "导入"
    导出 = "导出"
    删除 = "删除"
    配置 = "配置"


@dataclass
class 审计记录:
    """单条审计记录"""
    序号: int
    时间: str
    级别: str
    颜色: str
    操作: str
    模块: str
    消息: str
    详情: Dict = field(default_factory=dict)
    DNA追溯: str = ""

    def 格式化(self) -> str:
        """格式化为审计日志字符串"""
        return f"[{self.时间}] {self.颜色} [{self.操作}] {self.模块}: {self.消息}"

    def 转字典(self) -> Dict:
        return asdict(self)


class 联动审计:
    """
    联动审计系统
    集成所有模块的审计功能，统一日志管理
    支持实时回调通知
    """

    DNA追溯 = "#龍芯⚡️2026-06-18-CNSH-AUDIT-INTEGRATION-v5.0"

    # 级别到颜色的映射
    级别颜色 = {
        审计级别.成功: "🟢",
        审计级别.警告: "🟡",
        审计级别.错误: "🔴",
        审计级别.信息: "⚪",
        审计级别.安全: "🔒",
    }

    def __init__(self, 实时回调: Callable = None):
        self.审计记录列表: List[审计记录] = []
        self.序号计数器 = 0
        self.实时回调 = 实时回调
        self.锁 = threading.Lock()
        self.模块审计器: Dict[str, object] = {}

        # 初始化日志
        self.记录(审计级别.信息, 操作类型.审计, "联动审计", "联动审计系统初始化")

    def 注册模块(self, 模块名: str, 模块实例: object) -> None:
        """注册模块审计器"""
        self.模块审计器[模块名] = 模块实例
        self.记录(审计级别.成功, 操作类型.配置, "联动审计", f"注册模块: {模块名}")

    def 记录(self, 级别: 审计级别, 操作: 操作类型, 模块: str,
             消息: str, 详情: Dict = None) -> 审计记录:
        """
        记录审计事件
        核心审计方法
        """
        with self.锁:
            self.序号计数器 += 1
            序号 = self.序号计数器

        记录 = 审计记录(
            序号=序号,
            时间=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            级别=级别.value,
            颜色=self.级别颜色[级别],
            操作=操作.value,
            模块=模块,
            消息=消息,
            详情=详情 or {},
            DNA追溯=f"{self.DNA追溯}-{序号:06d}"
        )

        self.审计记录列表.append(记录)

        # 实时回调
        if self.实时回调:
            try:
                self.实时回调(记录)
            except Exception as e:
                print(f"审计回调错误: {e}")

        return 记录

    # ========== 快捷记录方法 ==========

    def 成功(self, 操作: 操作类型, 模块: str, 消息: str, 详情: Dict = None) -> 审计记录:
        """记录成功事件"""
        return self.记录(审计级别.成功, 操作, 模块, 消息, 详情)

    def 警告(self, 操作: 操作类型, 模块: str, 消息: str, 详情: Dict = None) -> 审计记录:
        """记录警告事件"""
        return self.记录(审计级别.警告, 操作, 模块, 消息, 详情)

    def 错误(self, 操作: 操作类型, 模块: str, 消息: str, 详情: Dict = None) -> 审计记录:
        """记录错误事件"""
        return self.记录(审计级别.错误, 操作, 模块, 消息, 详情)

    def 信息(self, 操作: 操作类型, 模块: str, 消息: str, 详情: Dict = None) -> 审计记录:
        """记录信息事件"""
        return self.记录(审计级别.信息, 操作, 模块, 消息, 详情)

    def 安全(self, 操作: 操作类型, 模块: str, 消息: str, 详情: Dict = None) -> 审计记录:
        """记录安全事件"""
        return self.记录(审计级别.安全, 操作, 模块, 消息, 详情)

    # ========== 集成审计 ==========

    def 审计编译(self, 源代码: str, 结果: Dict) -> None:
        """审计编译操作"""
        状态 = 结果.get("状态", "未知")
        颜色 = "🟢" if "通过" in 状态 else ("🟡" if "警告" in 状态 else "🔴")

        self.记录(
            审计级别.成功 if "通过" in 状态 else (审计级别.警告 if "警告" in 状态 else 审计级别.错误),
            操作类型.编译,
            "编译器",
            f"编译{状态}",
            {"代码长度": len(源代码), "状态": 状态, "颜色": 颜色}
        )

    def 审计运行(self, 命令: str, 输出: str, 返回码: int) -> None:
        """审计运行操作"""
        是否成功 = 返回码 == 0
        self.记录(
            审计级别.成功 if 是否成功 else 审计级别.错误,
            操作类型.运行,
            "运行环境",
            f"命令执行{'成功' if 是否成功 else '失败'} (返回码: {返回码})",
            {"命令": 命令[:100], "返回码": 返回码, "输出长度": len(输出)}
        )

    def 审计编辑(self, 文件路径: str, 操作描述: str) -> None:
        """审计编辑操作"""
        self.记录(
            审计级别.成功,
            操作类型.编辑,
            "编辑器",
            f"{操作描述}: {文件路径}",
            {"文件路径": 文件路径}
        )

    def 审计翻译(self, 方向: str, 原文长度: int, 译文长度: int) -> None:
        """审计翻译操作"""
        self.记录(
            审计级别.成功,
            操作类型.翻译,
            "通心译",
            f"翻译完成: {方向} ({原文长度} → {译文长度} 字符)",
            {"方向": 方向, "原文长度": 原文长度, "译文长度": 译文长度}
        )

    def 审计加密(self, 算法: str, 成功: bool) -> None:
        """审计加密操作"""
        self.记录(
            审计级别.成功 if 成功 else 审计级别.错误,
            操作类型.加密,
            "加密模块",
            f"加密{'成功' if 成功 else '失败'} ({算法})",
            {"算法": 算法}
        )

    def 审计熔断(self, 命令: str, 是否拦截: bool, 风险: List[str] = None) -> None:
        """审计熔断操作"""
        if 是否拦截:
            self.安全(
                操作类型.运行,
                "熔断机制",
                f"🚨 危险命令被拦截: {命令[:100]}",
                {"命令": 命令[:200], "风险": 风险 or []}
            )
        else:
            self.记录(
                审计级别.信息,
                操作类型.运行,
                "熔断机制",
                f"命令安全检查通过: {命令[:100]}",
                {"命令": 命令[:200]}
            )

    # ========== 查询与报告 ==========

    def 获取全部记录(self) -> List[审计记录]:
        """获取全部审计记录"""
        return self.审计记录列表.copy()

    def 获取最近记录(self, 数量: int = 10) -> List[审计记录]:
        """获取最近N条记录"""
        return self.审计记录列表[-数量:]

    def 按级别筛选(self, 级别: 审计级别) -> List[审计记录]:
        """按级别筛选记录"""
        return [r for r in self.审计记录列表 if r.级别 == 级别.value]

    def 按模块筛选(self, 模块: str) -> List[审计记录]:
        """按模块筛选记录"""
        return [r for r in self.审计记录列表 if r.模块 == 模块]

    def 生成报告(self) -> Dict:
        """生成审计报告"""
        统计 = {}
        for 级别 in 审计级别:
            统计[级别.value] = sum(1 for r in self.审计记录列表 if r.级别 == 级别.value)

        模块统计 = {}
        for 记录 in self.审计记录列表:
            if 记录.模块 not in 模块统计:
                模块统计[记录.模块] = 0
            模块统计[记录.模块] += 1

        return {
            "DNA追溯": self.DNA追溯,
            "总记录数": len(self.审计记录列表),
            "级别统计": 统计,
            "模块统计": 模块统计,
            "时间段": {
                "起始": self.审计记录列表[0].时间 if self.审计记录列表 else "",
                "结束": self.审计记录列表[-1].时间 if self.审计记录列表 else ""
            }
        }

    def 格式化日志(self, 数量: int = None) -> str:
        """格式化为可读日志文本"""
        记录列表 = self.审计记录列表[-数量:] if 数量 else self.审计记录列表
        行列表 = []

        for 记录 in 记录列表:
            行列表.append(
                f"[{记录.序号:06d}] [{记录.时间}] {记录.颜色} "
                f"[{记录.操作}] {记录.模块}: {记录.消息}"
            )

        return "\n".join(行列表)

    def 导出JSON(self, 文件路径: str = None) -> str:
        """导出审计记录为JSON"""
        数据 = [r.转字典() for r in self.审计记录列表]
        json字符串 = json.dumps(数据, ensure_ascii=False, indent=2)

        if 文件路径:
            with open(文件路径, 'w', encoding='utf-8') as f:
                f.write(json字符串)
            self.成功(操作类型.导出, "联动审计", f"审计记录导出到: {文件路径}")

        return json字符串

    def 清空(self) -> None:
        """清空审计记录"""
        数量 = len(self.审计记录列表)
        self.审计记录列表.clear()
        self.记录(审计级别.信息, 操作类型.配置, "联动审计", f"已清空 {数量} 条审计记录")

    # ========== 审计模块集成 ==========

    def 收集模块审计(self) -> Dict[str, Dict]:
        """收集所有注册模块的审计结果"""
        结果 = {}
        for 模块名, 模块实例 in self.模块审计器.items():
            if hasattr(模块实例, '获取审计结果'):
                try:
                    结果[模块名] = 模块实例.获取审计结果()
                except Exception as e:
                    结果[模块名] = {"错误": str(e)}
        return 结果

    # ========== 综合审计结果 ==========

    def 获取审计结果(self) -> Dict:
        """获取审计系统自身的审计结果"""
        报告 = self.生成报告()

        错误数 = sum(1 for r in self.审计记录列表 if r.级别 == 审计级别.错误.value)
        警告数 = sum(1 for r in self.审计记录列表 if r.级别 == 审计级别.警告.value)

        return {
            "DNA追溯": self.DNA追溯,
            "错误数": 错误数,
            "警告数": 警告数,
            "成功数": sum(1 for r in self.审计记录列表 if r.级别 == 审计级别.成功.value),
            "报告": 报告,
            "状态": "🔴 失败" if 错误数 > 0 else ("🟡 警告" if 警告数 > 0 else "🟢 通过")
        }


# ========== 便捷函数 ==========

def 创建审计系统(回调: Callable = None) -> 联动审计:
    """创建联动审计系统实例"""
    return 联动审计(回调)
