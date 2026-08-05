#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂·量子自动仲裁引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰-量子仲裁-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

定位：不再由Lucky选择模板，系统自动决定唤醒哪一个。
目标：每次只激活一个量子，其余休眠。算力可控，不并发。
负责人格：⚖️ 审判长
协同人格：🤖 宝宝(执行)、🧙 诸葛亮(推演)
优先级：P0级

核心流程：
  1. 信号识别与分类
  2. 候选池筛选
  3. 评分计算（核心仲裁）
  4. 唯一唤醒（硬约束）
  5. 唤醒执行与输出封装
  6. 状态回写与进化
  7. Index Hub联动
"""

import json
import uuid
import hashlib
import datetime
import re
import math
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
import argparse
from collections import defaultdict

# ============================================================
# 一、数据结构
# ============================================================

class 信号类型(Enum):
    用户语言 = "🗣️ 用户语言"
    系统事件 = "⚡ 系统事件"
    指令调用 = "📟 指令调用"
    状态信号 = "📊 状态信号"

class 量子类型(Enum):
    合规型 = "🛡️ 合规型"
    判断型 = "🧠 判断型"
    仲裁型 = "⚖️ 仲裁型"
    执行型 = "⚡ 执行型"
    调度型 = "🔄 调度型"

class 记忆状态(Enum):
    激活 = "🟢 激活"
    休眠 = "🟡 休眠"
    冻结 = "🔴 冻结"
    待炼化 = "🟠 待炼化"

@dataclass
class 触发信号:
    """触发信号"""
    信号ID: str
    类型: 信号类型
    内容: str
    关键词: List[str]
    情绪: Optional[str] = None
    事件类型: Optional[str] = None
    指令: Optional[str] = None
    重复次数: int = 0
    错误计数: int = 0
    时间戳: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    dna: str = ""

    def __post_init__(self):
        if not self.dna:
            self.dna = f"#龍芯⚡️{datetime.datetime.now().strftime('%Y-%m-%d')}-SIG-{uuid.uuid4().hex[:6].upper()}"

@dataclass
class 量子模板:
    """量子模板"""
    模板ID: str
    名称: str
    类型: 量子类型
    负责人格: str
    唤醒信号: List[str]  # 关键词
    记忆状态: 记忆状态
    使用频率: int = 0
    错误计数: int = 0
    可信度: int = 50  # 0-100
    算力消耗: float = 1.0  # 相对值
    最后使用: Optional[str] = None
    dna: str = ""

    def __post_init__(self):
        if not self.dna:
            self.dna = f"#龍芯⚡️{datetime.datetime.now().strftime('%Y-%m-%d')}-Q{uuid.uuid4().hex[:6].upper()}"

@dataclass
class 评分结果:
    """评分结果"""
    模板ID: str
    模板名称: str
    类型: 量子类型
    负责人格: str
    类型权重: float
    风险匹配: float
    人格适配: float
    历史稳定性: float
    算力惩罚: float
    总分: float
    是否选中: bool = False
    未选原因: str = ""

@dataclass
class 仲裁记录:
    """仲裁记录"""
    仲裁ID: str
    信号ID: str
    选中模板ID: str
    选中模板名称: str
    评分: float
    唤醒原因: str
    未选中: List[Dict]
    时间戳: str
    dna: str


# ============================================================
# 二、量子模板库
# ============================================================

class 量子模板库:
    """预置量子模板库（单例·状态持久化）"""

    _模板缓存: Optional[Dict[str, 量子模板]] = None

    @classmethod
    def _初始化缓存(cls):
        """首次调用时初始化模板缓存"""
        if cls._模板缓存 is not None:
            return
        templates = [
            量子模板(
                模板ID="QT-001",
                名称="三色审计量子",
                类型=量子类型.合规型,
                负责人格="上帝之眼",
                唤醒信号=["审计", "安全", "风险", "合规", "检查", "审核", "评估"],
                记忆状态=记忆状态.激活,
                算力消耗=0.8
            ),
            量子模板(
                模板ID="QT-002",
                名称="战略推演量子",
                类型=量子类型.判断型,
                负责人格="诸葛亮",
                唤醒信号=["推演", "战略", "预测", "分析", "决策", "方向", "规划"],
                记忆状态=记忆状态.激活,
                算力消耗=1.2
            ),
            量子模板(
                模板ID="QT-003",
                名称="万能补全量子",
                类型=量子类型.执行型,
                负责人格="宝宝",
                唤醒信号=["补全", "翻译", "需求", "整理", "模糊", "完善", "帮忙"],
                记忆状态=记忆状态.激活,
                算力消耗=0.6
            ),
            量子模板(
                模板ID="QT-004",
                名称="权重算法量子",
                类型=量子类型.仲裁型,
                负责人格="审判长",
                唤醒信号=["权重", "评分", "优先级", "排序", "权衡", "平衡"],
                记忆状态=记忆状态.激活,
                算力消耗=0.9
            ),
            量子模板(
                模板ID="QT-005",
                名称="文档生成量子",
                类型=量子类型.执行型,
                负责人格="雯雯",
                唤醒信号=["文档", "生成", "创建", "写", "说明", "手册", "指南"],
                记忆状态=记忆状态.激活,
                算力消耗=0.5
            ),
            量子模板(
                模板ID="QT-006",
                名称="安全守护量子",
                类型=量子类型.合规型,
                负责人格="上帝之眼",
                唤醒信号=["安全", "告警", "威胁", "攻击", "漏洞", "防护", "隔离"],
                记忆状态=记忆状态.激活,
                算力消耗=0.9
            ),
            量子模板(
                模板ID="QT-007",
                名称="社区问答量子",
                类型=量子类型.执行型,
                负责人格="宝宝",
                唤醒信号=["回答", "解答", "求助", "问题", "help", "求教"],
                记忆状态=记忆状态.激活,
                算力消耗=0.7
            ),
        ]
        cls._模板缓存 = {t.模板ID: t for t in templates}

    @classmethod
    def 获取全部(cls) -> List[量子模板]:
        """获取所有量子模板（从持久缓存）"""
        cls._初始化缓存()
        return list(cls._模板缓存.values())

    @classmethod
    def 按ID查找(cls, template_id: str) -> Optional[量子模板]:
        """按ID查找量子模板"""
        cls._初始化缓存()
        return cls._模板缓存.get(template_id)

    @classmethod
    def 按名称查找(cls, name: str) -> Optional[量子模板]:
        """按名称查找量子模板"""
        cls._初始化缓存()
        for qt in cls._模板缓存.values():
            if qt.名称 == name:
                return qt
        return None


# ============================================================
# 三、信号识别器
# ============================================================

class 信号识别器:
    """识别并分类触发信号"""

    # 情绪关键词
    情绪映射 = {
        "迷茫": "迷茫",
        "困惑": "困惑",
        "烦躁": "烦躁",
        "累": "疲惫",
        "没意思": "无意义",
        "开心": "开心",
        "好": "好",
        "不知道": "不知道",
        "不安": "不安",
        "焦虑": "焦虑"
    }

    @classmethod
    def 识别(cls, 输入内容: str) -> 触发信号:
        """识别并分类触发信号"""

        # 检测信号类型
        类型 = cls._判断类型(输入内容)
        关键词 = cls._提取关键词(输入内容)
        情绪 = cls._检测情绪(输入内容)

        # 检测特殊指令
        指令 = None
        if 输入内容.startswith("/"):
            指令 = 输入内容.split()[0] if 输入内容.split() else 输入内容

        # 检测重复次数（模拟）
        重复次数 = 0
        错误计数 = 0

        return 触发信号(
            信号ID=f"SIG-{uuid.uuid4().hex[:8].upper()}",
            类型=类型,
            内容=输入内容,
            关键词=关键词,
            情绪=情绪,
            事件类型=cls._判断事件类型(输入内容),
            指令=指令,
            重复次数=重复次数,
            错误计数=错误计数,
            dna=f"#龍芯⚡️{datetime.datetime.now().strftime('%Y-%m-%d')}-SIG-{uuid.uuid4().hex[:6].upper()}"
        )

    @classmethod
    def _判断类型(cls, 内容: str) -> 信号类型:
        """判断信号类型"""
        # 指令调用
        if 内容.startswith("/"):
            return 信号类型.指令调用

        # 系统事件（关键词）
        系统事件词 = ["风险", "告警", "错误", "异常", "冲突", "安全"]
        if any(词 in 内容 for 词 in 系统事件词):
            return 信号类型.系统事件

        # 状态信号
        状态词 = ["重复", "频率", "统计", "历史", "习惯"]
        if any(词 in 内容 for 词 in 状态词):
            return 信号类型.状态信号

        # 默认用户语言
        return 信号类型.用户语言

    @classmethod
    def _提取关键词(cls, 内容: str) -> List[str]:
        """提取关键词"""
        # 简单分词
        words = re.findall(r'[\u4e00-\u9fa5a-zA-Z]+', 内容)
        # 过滤虚词
        虚词 = ["的", "了", "是", "在", "和", "有", "我", "你", "他", "她", "它"]
        return [w for w in words if w not in 虚词][:10]

    @classmethod
    def _检测情绪(cls, 内容: str) -> Optional[str]:
        """检测情绪"""
        for 关键词, 情绪 in cls.情绪映射.items():
            if 关键词 in 内容:
                return 情绪
        return None

    @classmethod
    def _判断事件类型(cls, 内容: str) -> Optional[str]:
        """判断事件类型"""
        if "风险" in 内容:
            return "风险事件"
        if "安全" in 内容:
            return "安全事件"
        if "冲突" in 内容:
            return "冲突事件"
        if "异常" in 内容:
            return "异常事件"
        return None


# ============================================================
# 四、候选池筛选器
# ============================================================

class 候选池筛选器:
    """从模板库筛选符合条件的量子"""

    @classmethod
    def 筛选(cls, 信号: 触发信号) -> List[量子模板]:
        """筛选候选量子"""
        全部量子 = 量子模板库.获取全部()
        候选 = []

        for qt in 全部量子:
            # 检查记忆状态
            if qt.记忆状态 == 记忆状态.冻结:
                continue

            # 检查唤醒信号匹配
            匹配 = False
            for 关键词 in qt.唤醒信号:
                if 关键词 in 信号.内容:
                    匹配 = True
                    break

            if 匹配:
                候选.append(qt)

        # 如果没有候选，返回所有激活的量子（降级路径）
        if not 候选:
            候选 = [qt for qt in 全部量子 if qt.记忆状态 == 记忆状态.激活]

        return 候选


# ============================================================
# 五、评分计算引擎（核心仲裁）
# ============================================================

class 评分计算引擎:
    """计算每个候选量子的优先级评分P"""

    # 量子类型权重
    类型权重 = {
        量子类型.合规型: 10,
        量子类型.判断型: 8,
        量子类型.仲裁型: 7,
        量子类型.执行型: 6,
        量子类型.调度型: 5
    }

    # 人格适配映射
    人格适配 = {
        "上帝之眼": {"安全": 1.2, "风险": 1.2, "审计": 1.1},
        "诸葛亮": {"战略": 1.2, "推演": 1.2, "分析": 1.1},
        "宝宝": {"补全": 1.2, "协助": 1.1, "模糊": 1.1},
        "审判长": {"仲裁": 1.2, "评分": 1.1},
        "雯雯": {"文档": 1.2, "整理": 1.1}
    }

    # 风险等级映射
    风险映射 = {
        "P0": 10,
        "P1": 8,
        "P2": 5,
        "P3": 3
    }

    @classmethod
    def 计算(cls, 信号: 触发信号, 候选: List[量子模板]) -> List[评分结果]:
        """计算所有候选的评分"""
        结果列表 = []

        for qt in 候选:
            # 1. 类型权重
            类型分 = cls.类型权重.get(qt.类型, 5)

            # 2. 风险匹配度
            风险分 = cls._计算风险匹配(信号, qt)

            # 3. 人格适配度
            人格分 = cls._计算人格适配(信号, qt)

            # 4. 历史稳定性
            稳定分 = cls._计算历史稳定性(qt)

            # 5. 算力惩罚
            算力惩罚 = cls._计算算力惩罚(qt)

            # 总分
            总分 = 类型分 + 风险分 + 人格分 + 稳定分 - 算力惩罚

            结果列表.append(评分结果(
                模板ID=qt.模板ID,
                模板名称=qt.名称,
                类型=qt.类型,
                负责人格=qt.负责人格,
                类型权重=类型分,
                风险匹配=风险分,
                人格适配=人格分,
                历史稳定性=稳定分,
                算力惩罚=算力惩罚,
                总分=round(总分, 2)
            ))

        # 按总分降序排列
        结果列表.sort(key=lambda x: x.总分, reverse=True)
        return 结果列表

    @classmethod
    def _计算风险匹配(cls, 信号: 触发信号, qt: 量子模板) -> float:
        """计算风险匹配度"""
        # 检测风险等级
        风险等级 = "P3"
        if any(词 in 信号.内容 for 词 in ["P0", "永恒", "铁律"]):
            风险等级 = "P0"
        elif any(词 in 信号.内容 for 词 in ["高危", "严重", "关键"]):
            风险等级 = "P1"
        elif any(词 in 信号.内容 for 词 in ["中危", "警告"]):
            风险等级 = "P2"

        风险分 = cls.风险映射.get(风险等级, 3)

        # 合规型对高风险有加成
        if qt.类型 == 量子类型.合规型 and 风险等级 in ["P0", "P1"]:
            风险分 += 5

        # 判断型对中风险有加成
        if qt.类型 == 量子类型.判断型 and 风险等级 == "P2":
            风险分 += 3

        return float(风险分)

    @classmethod
    def _计算人格适配(cls, 信号: 触发信号, qt: 量子模板) -> float:
        """计算人格适配度"""
        适配分 = 0.0

        # 获取该人格的适配规则
        规则 = cls.人格适配.get(qt.负责人格, {})

        for 关键词, 权重 in 规则.items():
            if 关键词 in 信号.内容:
                适配分 += 权重 * 0.5

        return min(适配分, 5.0)

    @classmethod
    def _计算历史稳定性(cls, qt: 量子模板) -> float:
        """计算历史稳定性"""
        稳定分 = 0.0

        # 使用频率高 + 可信度高
        if qt.使用频率 > 10 and qt.可信度 > 70:
            稳定分 += 3.0
        elif qt.使用频率 > 5 and qt.可信度 > 50:
            稳定分 += 1.0

        # 错误惩罚
        if qt.错误计数 >= 3:
            稳定分 -= 5.0
        elif qt.错误计数 >= 1:
            稳定分 -= 2.0

        return max(0.0, 稳定分)

    @classmethod
    def _计算算力惩罚(cls, qt: 量子模板) -> float:
        """计算算力惩罚"""
        惩罚 = 0.0

        # 算力消耗基础
        if qt.算力消耗 > 1.0:
            惩罚 += (qt.算力消耗 - 1.0) * 2

        # 使用频率惩罚（避免过度依赖）
        if qt.使用频率 > 10:
            惩罚 += 3.0
        elif qt.使用频率 > 5:
            惩罚 += 1.0

        return min(惩罚, 5.0)


# ============================================================
# 六、唯一唤醒执行器
# ============================================================

class 唯一唤醒执行器:
    """确保每次只激活一个量子"""

    安全阈值 = 5.0

    @classmethod
    def 唤醒(cls, 评分列表: List[评分结果], 信号: 触发信号) -> Dict:
        """执行唯一唤醒"""

        if not 评分列表:
            return {
                "状态": "❌ 无候选",
                "原因": "没有可用的量子模板",
                "动作": "降级路径：使用通用模板"
            }

        # 检查最高分是否低于安全阈值
        if 评分列表[0].总分 < cls.安全阈值:
            return {
                "状态": "⚠️ 安全阈值",
                "原因": f"最高分 {评分列表[0].总分} 低于安全阈值 {cls.安全阈值}",
                "动作": "不唤醒任何量子，返回安全提示",
                "最高分": 评分列表[0].总分
            }

        # 检查是否有并列最高分
        最高分 = 评分列表[0].总分
        并列 = [r for r in 评分列表 if r.总分 == 最高分]

        if len(并列) > 1:
            # 按优先级打破平局
            选中 = cls._打破平局(并列)
        else:
            选中 = 评分列表[0]

        # 标记选中
        选中.是否选中 = True

        # 构建未选中列表
        未选中 = []
        for r in 评分列表[1:]:
            未选中.append({
                "模板名称": r.模板名称,
                "评分": r.总分,
                "未选原因": cls._生成未选原因(r, 选中)
            })

        return {
            "状态": "✅ 已唤醒",
            "选中": {
                "模板ID": 选中.模板ID,
                "模板名称": 选中.模板名称,
                "类型": 选中.类型.value,
                "负责人格": 选中.负责人格,
                "评分": 选中.总分,
                "唤醒原因": cls._生成唤醒原因(选中, 信号)
            },
            "未选中": 未选中[:5],  # 最多显示5个
            "安全阈值": cls.安全阈值
        }

    @classmethod
    def _打破平局(cls, 并列列表: List[评分结果]) -> 评分结果:
        """按优先级打破平局"""
        # 优先级1: P0级合规型优先
        for r in 并列列表:
            if r.类型 == 量子类型.合规型:
                return r

        # 优先级2: 使用频率高且稳定的优先
        排序 = sorted(并列列表, key=lambda x: (x.历史稳定性, x.类型权重), reverse=True)
        return 排序[0]

    @classmethod
    def _生成唤醒原因(cls, 选中: 评分结果, 信号: 触发信号) -> str:
        """生成唤醒原因"""
        原因 = []
        原因.append(f"信号类型: {信号.类型.value}")

        if 信号.关键词:
            原因.append(f"匹配关键词: {', '.join(信号.关键词[:3])}")

        原因.append(f"类型权重: {选中.类型权重}分")
        原因.append(f"风险匹配: {选中.风险匹配}分")
        原因.append(f"人格适配: {选中.人格适配}分")
        原因.append(f"历史稳定性: {选中.历史稳定性}分")

        return " | ".join(原因)

    @classmethod
    def _生成未选原因(cls, 未选中: 评分结果, 选中: 评分结果) -> str:
        """生成未选原因"""
        原因 = []

        if 未选中.总分 < 选中.总分:
            原因.append(f"评分低于主量子 {选中.总分 - 未选中.总分:.1f}分")

        if 未选中.类型 != 选中.类型:
            原因.append(f"类型权重较低 ({未选中.类型权重} < {选中.类型权重})")

        if 未选中.历史稳定性 < 选中.历史稳定性:
            原因.append("历史稳定性较低")

        if 未选中.算力惩罚 > 选中.算力惩罚:
            原因.append("算力消耗较高")

        return "；".join(原因[:3]) if 原因 else "综合评分较低"


# ============================================================
# 七、状态回写器
# ============================================================

class 状态回写器:
    """自动更新量子状态"""

    def __init__(self):
        self.使用记录: Dict[str, List[Dict]] = defaultdict(list)

    def 回写(self, 模板ID: str, 成功: bool, 错误信息: Optional[str] = None):
        """回写状态"""
        qt = 量子模板库.按ID查找(模板ID)
        if not qt:
            return

        qt.使用频率 += 1
        qt.最后使用 = datetime.datetime.now().isoformat()

        if 成功:
            qt.可信度 = min(100, qt.可信度 + 1)
        else:
            qt.错误计数 += 1
            qt.可信度 = max(0, qt.可信度 - 5)

            if qt.错误计数 >= 3:
                qt.记忆状态 = 记忆状态.待炼化
                # 如果再出错，进入休眠
                if qt.错误计数 >= 5:
                    qt.记忆状态 = 记忆状态.休眠

        # 记录
        self.使用记录[模板ID].append({
            "时间": datetime.datetime.now().isoformat(),
            "成功": 成功,
            "错误": 错误信息
        })


# ============================================================
# 八、Index Hub联动
# ============================================================

class IndexHub:
    """Index Hub联动 - 记录所有仲裁"""

    def __init__(self):
        self.记录: List[仲裁记录] = []
        self.记录路径 = Path.home() / ".longhun/arbitration_history.json"
        self.记录路径.parent.mkdir(parents=True, exist_ok=True)

    def 记录仲裁(self, 信号: 触发信号, 唤醒结果: Dict) -> 仲裁记录:
        """记录仲裁过程"""
        仲裁ID = f"ARB-{uuid.uuid4().hex[:8].upper()}"

        记录 = 仲裁记录(
            仲裁ID=仲裁ID,
            信号ID=信号.信号ID,
            选中模板ID=唤醒结果.get("选中", {}).get("模板ID", ""),
            选中模板名称=唤醒结果.get("选中", {}).get("模板名称", ""),
            评分=唤醒结果.get("选中", {}).get("评分", 0),
            唤醒原因=唤醒结果.get("选中", {}).get("唤醒原因", ""),
            未选中=唤醒结果.get("未选中", []),
            时间戳=datetime.datetime.now().isoformat(),
            dna=f"#龍芯⚡️{datetime.datetime.now().strftime('%Y-%m-%d')}-ARB-{uuid.uuid4().hex[:6].upper()}"
        )

        self.记录.append(记录)

        # 保存到文件
        try:
            with open(self.记录路径, 'w', encoding='utf-8') as f:
                json.dump([self._记录转字典(r) for r in self.记录[-100:]], f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Index Hub保存失败: {e}")

        return 记录

    @staticmethod
    def _记录转字典(r: 仲裁记录) -> Dict:
        """仲裁记录转字典（处理枚举序列化）"""
        return {
            "仲裁ID": r.仲裁ID,
            "信号ID": r.信号ID,
            "选中模板ID": r.选中模板ID,
            "选中模板名称": r.选中模板名称,
            "评分": r.评分,
            "唤醒原因": r.唤醒原因,
            "未选中": r.未选中,
            "时间戳": r.时间戳,
            "dna": r.dna
        }

    def 查询(self, 信号ID: Optional[str] = None, limit: int = 20) -> List[Dict]:
        """查询仲裁记录"""
        if 信号ID:
            return [self._记录转字典(r) for r in self.记录 if r.信号ID == 信号ID][:limit]
        return [self._记录转字典(r) for r in self.记录[-limit:]]

    def 统计(self) -> Dict:
        """统计仲裁数据"""
        if not self.记录:
            return {"总仲裁": 0}

        总 = len(self.记录)
        # 统计各模板被选中次数
        模板统计 = defaultdict(int)
        for r in self.记录:
            if r.选中模板ID:
                模板统计[r.选中模板ID] += 1

        return {
            "总仲裁": 总,
            "模板统计": dict(模板统计)
        }


# ============================================================
# 九、主引擎：量子自动仲裁引擎
# ============================================================

class 量子自动仲裁引擎:
    """龍魂量子自动仲裁引擎主控"""

    def __init__(self):
        self.信号识别器 = 信号识别器()
        self.候选筛选器 = 候选池筛选器()
        self.评分引擎 = 评分计算引擎()
        self.唤醒执行器 = 唯一唤醒执行器()
        self.状态回写器 = 状态回写器()
        self.index_hub = IndexHub()

    def _评分转字典(self, r: 评分结果) -> Dict:
        """评分结果转字典（处理枚举序列化）"""
        return {
            "模板ID": r.模板ID,
            "模板名称": r.模板名称,
            "类型": r.类型.value,
            "负责人格": r.负责人格,
            "类型权重": r.类型权重,
            "风险匹配": r.风险匹配,
            "人格适配": r.人格适配,
            "历史稳定性": r.历史稳定性,
            "算力惩罚": r.算力惩罚,
            "总分": r.总分,
            "是否选中": r.是否选中,
            "未选原因": r.未选原因
        }

    def 仲裁(self, 输入内容: str) -> Dict:
        """
        执行完整仲裁流程

        流程：识别 → 筛选 → 评分 → 唤醒 → 回写 → Index Hub
        """
        # 1. 识别信号
        信号 = self.信号识别器.识别(输入内容)

        # 2. 筛选候选
        候选 = self.候选筛选器.筛选(信号)

        if not 候选:
            return {
                "状态": "❌ 无候选",
                "信号": self._信号转字典(信号),
                "原因": "没有匹配的量子模板",
                "动作": "降级路径：使用通用模板"
            }

        # 3. 计算评分
        评分结果 = self.评分引擎.计算(信号, 候选)

        # 4. 唯一唤醒
        唤醒结果 = self.唤醒执行器.唤醒(评分结果, 信号)

        # 5. 状态回写（如果唤醒成功）
        if 唤醒结果.get("状态") == "✅ 已唤醒":
            选中 = 唤醒结果["选中"]
            self.状态回写器.回写(选中["模板ID"], True)
        else:
            # 记录未唤醒
            pass

        # 6. Index Hub联动
        仲裁记录 = self.index_hub.记录仲裁(信号, 唤醒结果)

        # 7. 返回结果
        return {
            "信号": self._信号转字典(信号),
            "候选数量": len(候选),
            "评分": [self._评分转字典(r) for r in 评分结果[:5]],  # 前5名
            "唤醒结果": 唤醒结果,
            "仲裁记录": self.index_hub._记录转字典(仲裁记录)
        }

    @staticmethod
    def _信号转字典(s: 触发信号) -> Dict:
        """触发信号转字典（处理枚举）"""
        return {
            "信号ID": s.信号ID,
            "类型": s.类型.value,
            "内容": s.内容,
            "关键词": s.关键词,
            "情绪": s.情绪,
            "事件类型": s.事件类型,
            "指令": s.指令,
            "重复次数": s.重复次数,
            "错误计数": s.错误计数,
            "时间戳": s.时间戳,
            "dna": s.dna
        }

    def 快速仲裁(self, 输入内容: str) -> Dict:
        """快速仲裁 - 只返回选中的量子"""
        结果 = self.仲裁(输入内容)
        if 结果.get("唤醒结果", {}).get("状态") == "✅ 已唤醒":
            return {
                "选中": 结果["唤醒结果"]["选中"],
                "仲裁ID": 结果["仲裁记录"]["仲裁ID"],
                "dna": 结果["仲裁记录"]["dna"]
            }
        return {
            "状态": "❌ 未唤醒",
            "原因": 结果.get("唤醒结果", {}).get("原因", "未知")
        }


# ============================================================
# 十、命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·量子自动仲裁引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 交互模式
  python3 lh_quantum_arbitrator.py --interactive

  # 单次仲裁
  python3 lh_quantum_arbitrator.py "帮我做安全检查"

  # 快速仲裁（只返回选中）
  python3 lh_quantum_arbitrator.py "帮我做安全检查" --quick

  # 查看模板库
  python3 lh_quantum_arbitrator.py --list

  # 查看Index Hub
  python3 lh_quantum_arbitrator.py --hub
        """
    )

    parser.add_argument("输入", nargs="*", help="触发输入")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--quick", "-q", action="store_true", help="快速仲裁")
    parser.add_argument("--list", "-l", action="store_true", help="查看量子模板库")
    parser.add_argument("--hub", "-H", action="store_true", help="查看Index Hub")
    parser.add_argument("--json", "-j", action="store_true", help="JSON格式输出")

    args = parser.parse_args()

    engine = 量子自动仲裁引擎()

    # 查看模板库
    if args.list:
        print("\n📋 量子模板库:")
        print("-" * 60)
        for qt in 量子模板库.获取全部():
            状态 = qt.记忆状态.value
            print(f"  {qt.模板ID} | {qt.名称}")
            print(f"    类型: {qt.类型.value} | 人格: {qt.负责人格}")
            print(f"    唤醒信号: {', '.join(qt.唤醒信号[:3])}...")
            print(f"    状态: {状态} | 使用: {qt.使用频率}次 | 可信度: {qt.可信度}")
            print()
        return

    # 查看Index Hub
    if args.hub:
        统计 = engine.index_hub.统计()
        记录 = engine.index_hub.查询(limit=10)
        print("\n📊 Index Hub:")
        print("-" * 60)
        print(f"总仲裁: {统计.get('总仲裁', 0)}")
        if 统计.get('模板统计'):
            for tid, cnt in 统计['模板统计'].items():
                qt = 量子模板库.按ID查找(tid)
                name = qt.名称 if qt else tid
                print(f"  {name}: {cnt}次")
        print("\n最近10条记录:")
        for r in 记录:
            选中名 = r['选中模板名称'] or '无'
            print(f"  {r['仲裁ID']} | {选中名} | {r['评分']}分")
        return

    # 交互模式
    if args.interactive:
        print("\n" + "=" * 60)
        print("🐉 量子自动仲裁引擎 - 交互模式")
        print("=" * 60)
        print("输入任意内容，系统自动选择最优量子")
        print("输入 'exit' 退出")
        print("=" * 60)

        while True:
            try:
                输入 = input("\n📥 > ").strip()
                if not 输入:
                    continue
                if 输入.lower() in ['exit', 'quit']:
                    break

                if args.quick:
                    结果 = engine.快速仲裁(输入)
                else:
                    结果 = engine.仲裁(输入)

                if args.json:
                    print(json.dumps(结果, ensure_ascii=False, indent=2))
                else:
                    if args.quick:
                        if "选中" in 结果:
                            print(f"\n✅ 选中: {结果['选中']['模板名称']}")
                            print(f"  评分: {结果['选中']['评分']}分")
                            print(f"  人格: {结果['选中']['负责人格']}")
                        else:
                            print(f"\n❌ {结果.get('原因', '未知')}")
                    else:
                        # 简化显示
                        唤醒 = 结果.get("唤醒结果", {})
                        if 唤醒.get("状态") == "✅ 已唤醒":
                            选中 = 唤醒["选中"]
                            print(f"\n✅ 选中: {选中['模板名称']}")
                            print(f"  评分: {选中['评分']}分")
                            print(f"  人格: {选中['负责人格']}")
                            print(f"  原因: {选中['唤醒原因']}")
                        else:
                            print(f"\n{唤醒.get('状态', '⚠️')}: {唤醒.get('原因', '')}")

            except KeyboardInterrupt:
                break
        return

    # 单次仲裁
    if args.输入:
        输入 = " ".join(args.输入)

        if args.quick:
            结果 = engine.快速仲裁(输入)
        else:
            结果 = engine.仲裁(输入)

        if args.json:
            print(json.dumps(结果, ensure_ascii=False, indent=2))
        else:
            if args.quick:
                if "选中" in 结果:
                    print(f"\n✅ 选中: {结果['选中']['模板名称']} ({结果['选中']['评分']}分)")
                    print(f"  人格: {结果['选中']['负责人格']}")
                    print(f"  DNA: {结果.get('dna', '')}")
                else:
                    print(f"\n❌ {结果.get('原因', '未知')}")
            else:
                唤醒 = 结果.get("唤醒结果", {})
                if 唤醒.get("状态") == "✅ 已唤醒":
                    选中 = 唤醒["选中"]
                    print("\n" + "=" * 50)
                    print("🐉 仲裁结果")
                    print("=" * 50)
                    print(f"✅ 选中: {选中['模板名称']}")
                    print(f"  评分: {选中['评分']}分")
                    print(f"  类型: {选中['类型']}")
                    print(f"  人格: {选中['负责人格']}")
                    print(f"  原因: {选中['唤醒原因']}")
                    print(f"  DNA: {结果['仲裁记录']['dna']}")
                    print("\n📋 未选中:")
                    for u in 唤醒.get("未选中", [])[:3]:
                        print(f"  - {u['模板名称']} ({u['评分']}分) → {u['未选原因']}")
                else:
                    print(f"\n{唤醒.get('状态', '⚠️')}: {唤醒.get('原因', '')}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
