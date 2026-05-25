#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·核心算法系统 v2.0
Algorithms: 易经 × 五行 × 三才 × 流场融合

DNA: #龍芯⚡️2026-05-25-ALGORITHMS-FLOWFIELD-v2.0
UID: 9622
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

根据以下文档实现:
  - 🧠 诸葛亮沙盒训练场 易经道德经算法实验室
  - ① 洛书九宫矩阵 (Magic Square)·地场骨架
  - 龍魂·五行计算器
  - 🤖 三才流场·MCP自适应引擎 v4.0

本地计算·永不外送·纯数学·零 ML 依赖

理论指导: 曾仕强老师（永恒显示）
献礼: 龍魂系统·永恒守护
"""

import math
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from enum import Enum


# ════════════════════════════════════════════════════════
# 第一步：数字根与五行映射
# ════════════════════════════════════════════════════════

class WuXing(Enum):
    """五行"""
    WOOD = "木"  # 1, 2
    FIRE = "火"  # 3, 4
    EARTH = "土"  # 5
    METAL = "金"  # 6, 7
    WATER = "水"  # 8, 9, 0


@dataclass
class WuXingVector:
    """五行向量（4维：克制关系）"""
    wuxing: WuXing
    strength: float  # 0.0-1.0
    phase: str  # rising / peak / declining / dormant
    resonance: float  # 与环境的共鸣度


class DigitalRootCalculator:
    """数字根计算器（易经基础）"""

    @staticmethod
    def calculate(text_or_number) -> int:
        """计算数字根（1-9）"""
        if isinstance(text_or_number, str):
            # 文本 → 字符 ASCII 和
            total = sum(ord(c) for c in text_or_number)
        else:
            total = int(text_or_number)

        # 反复相加直到单个数字
        while total >= 10:
            total = sum(int(d) for d in str(total))

        return total if total > 0 else 9

    @staticmethod
    def map_to_wuxing(dr: int) -> WuXing:
        """数字根 → 五行"""
        mapping = {
            1: WuXing.WOOD,
            2: WuXing.WOOD,
            3: WuXing.FIRE,
            4: WuXing.FIRE,
            5: WuXing.EARTH,
            6: WuXing.METAL,
            7: WuXing.METAL,
            8: WuXing.WATER,
            9: WuXing.WATER,
        }
        return mapping.get(dr, WuXing.EARTH)


# ════════════════════════════════════════════════════════
# 第二步：洛书九宫矩阵（地场骨架）
# ════════════════════════════════════════════════════════

class LuoshuMatrix:
    """洛书九宫矩阵（Magic Square）- 地场骨架"""

    # 标准 3x3 洛书
    STANDARD = [
        [4, 9, 2],
        [3, 5, 7],
        [8, 1, 6],
    ]

    CENTER = 5  # 中宫 = UID9622 不动点

    @staticmethod
    def get_palace(position: int) -> Dict[str, Any]:
        """获取宫位信息（1-9）"""
        palaces = {
            1: {"name": "坎宫（北）", "element": WuXing.WATER, "meaning": "智慧·深度"},
            2: {"name": "坤宫（西南）", "element": WuXing.EARTH, "meaning": "承载·柔和"},
            3: {"name": "震宫（东）", "element": WuXing.WOOD, "meaning": "行动·生长"},
            4: {"name": "巽宫（东南）", "element": WuXing.WOOD, "meaning": "流动·传播"},
            5: {"name": "中宫（中）", "element": WuXing.EARTH, "meaning": "不动点·UID9622"},
            6: {"name": "乾宫（西北）", "element": WuXing.METAL, "meaning": "统治·决策"},
            7: {"name": "兑宫（西）", "element": WuXing.METAL, "meaning": "表达·喜悦"},
            8: {"name": "艮宫（东北）", "element": WuXing.EARTH, "meaning": "停止·思考"},
            9: {"name": "离宫（南）", "element": WuXing.FIRE, "meaning": "明亮·洞察"},
        }
        return palaces.get(position, {})

    @staticmethod
    def check_resonance(palace1: int, palace2: int) -> float:
        """检查两个宫位的共鸣度（0-1）"""
        # 五行相生相克关系
        wuxing_map = {
            1: WuXing.WATER, 2: WuXing.EARTH, 3: WuXing.WOOD,
            4: WuXing.WOOD, 5: WuXing.EARTH, 6: WuXing.METAL,
            7: WuXing.METAL, 8: WuXing.EARTH, 9: WuXing.FIRE,
        }

        w1, w2 = wuxing_map[palace1], wuxing_map[palace2]

        # 相生关系
        generating = {
            WuXing.WOOD: WuXing.FIRE,
            WuXing.FIRE: WuXing.EARTH,
            WuXing.EARTH: WuXing.METAL,
            WuXing.METAL: WuXing.WATER,
            WuXing.WATER: WuXing.WOOD,
        }

        if generating.get(w1) == w2 or generating.get(w2) == w1:
            return 0.8  # 相生
        elif w1 == w2:
            return 0.9  # 同类
        else:
            return 0.4  # 相克或无关


# ════════════════════════════════════════════════════════
# 第三步：三才系统（天·地·人）
# ════════════════════════════════════════════════════════

class SanCaiSystem:
    """三才系统：天（趋势）× 地（基础）× 人（主观）"""

    @staticmethod
    def calculate_sancai(input_text: str) -> Dict[str, Any]:
        """计算三才配置"""
        dr = DigitalRootCalculator.calculate(input_text)

        # 天才（外部条件）
        tian_dr = (dr * 2) % 9 or 9
        tian = {
            "dr": tian_dr,
            "wuxing": DigitalRootCalculator.map_to_wuxing(tian_dr),
            "meaning": "外部机遇与条件"
        }

        # 地才（基础条件）
        di_dr = (dr * 3) % 9 or 9
        di = {
            "dr": di_dr,
            "wuxing": DigitalRootCalculator.map_to_wuxing(di_dr),
            "meaning": "内在基础与资源"
        }

        # 人才（个人意志）
        ren_dr = dr  # 人才 = 输入本身
        ren = {
            "dr": ren_dr,
            "wuxing": DigitalRootCalculator.map_to_wuxing(ren_dr),
            "meaning": "主观努力与意志"
        }

        return {
            "input": input_text,
            "tian": tian,
            "di": di,
            "ren": ren,
            "harmony": SanCaiSystem._calculate_harmony(tian["wuxing"], di["wuxing"], ren["wuxing"])
        }

    @staticmethod
    def _calculate_harmony(tian_wx: WuXing, di_wx: WuXing, ren_wx: WuXing) -> float:
        """计算三才协调度"""
        # 简单启发式：相生关系最优
        harmony = 0.0

        if tian_wx == di_wx == ren_wx:
            harmony = 0.95  # 五行统一
        elif all(wx in [WuXing.WOOD, WuXing.FIRE, WuXing.EARTH] for wx in [tian_wx, di_wx, ren_wx]):
            harmony = 0.80  # 木火土相生
        elif all(wx in [WuXing.EARTH, WuXing.METAL, WuXing.WATER] for wx in [tian_wx, di_wx, ren_wx]):
            harmony = 0.75  # 土金水相生
        else:
            harmony = 0.50  # 杂乱

        return harmony


# ════════════════════════════════════════════════════════
# 第四步：流场融合引擎（三才 + 五行 + 洛书综合）
# ════════════════════════════════════════════════════════

@dataclass
class FlowFieldState:
    """流场状态"""
    center: int  # 中心宫位（1-9）
    sancai: Dict[str, Any]
    resonance_map: Dict[Tuple[int, int], float]
    harmony_index: float  # 总谐和度（0-1）
    flow_direction: str  # 流向（顺时针/逆时针/静止）
    timestamp: str


class FlowFieldEngine:
    """三才流场融合引擎 v4.0"""

    def __init__(self):
        self.center = 5  # UID9622 中心不动点
        self.luoshu = LuoshuMatrix()
        self.sancai = SanCaiSystem()

    def calculate_flow(self, intent: str) -> FlowFieldState:
        """计算完整流场"""
        from datetime import datetime

        # 1. 计算三才
        sancai = self.sancai.calculate_sancai(intent)

        # 2. 确定中心宫位
        dr = DigitalRootCalculator.calculate(intent)
        center = dr if dr != 5 else 5  # 保持 5 为不动点

        # 3. 计算共鸣矩阵（所有宫位间的共鸣）
        resonance_map = {}
        for i in range(1, 10):
            for j in range(i+1, 10):
                resonance = self.luoshu.check_resonance(i, j)
                resonance_map[(i, j)] = resonance

        # 4. 计算谐和度（基于三才 + 中心宫位）
        center_palace = self.luoshu.get_palace(center)
        sancai_harmony = sancai["harmony"]
        center_strength = 1.0 if center == 5 else 0.8
        overall_harmony = (sancai_harmony + sum(resonance_map.values()) / len(resonance_map)) / 2

        # 5. 确定流向
        flow_direction = self._determine_flow_direction(dr, sancai)

        flow_state = FlowFieldState(
            center=center,
            sancai=sancai,
            resonance_map=resonance_map,
            harmony_index=round(overall_harmony, 3),
            flow_direction=flow_direction,
            timestamp=datetime.now().isoformat(),
        )

        return flow_state

    @staticmethod
    def _determine_flow_direction(dr: int, sancai: Dict) -> str:
        """确定流向（顺/逆/静）"""
        tian_dr = sancai["tian"]["dr"]
        di_dr = sancai["di"]["dr"]

        if tian_dr > di_dr:
            return "顺时针（上升）"
        elif tian_dr < di_dr:
            return "逆时针（下降）"
        else:
            return "静止（平衡）"

    def generate_recommendation(self, flow_state: FlowFieldState) -> Dict[str, Any]:
        """根据流场生成建议"""
        harmony = flow_state.harmony_index

        if harmony >= 0.8:
            level = "极优"
            action = "继续执行，天时地利人和"
        elif harmony >= 0.6:
            level = "良好"
            action = "可执行，注意细节协调"
        elif harmony >= 0.4:
            level = "平稳"
            action = "谨慎执行，需要调整"
        else:
            level = "困难"
            action = "延期或重新规划"

        return {
            "harmony_level": level,
            "harmony_score": harmony,
            "recommended_action": action,
            "flow_direction": flow_state.flow_direction,
            "optimal_palace": flow_state.center,
        }


# ════════════════════════════════════════════════════════
# 示例与测试
# ════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧠 龍魂核心算法系统 v2.0")
    print(f"   DNA: #龍芯⚡️2026-05-25-ALGORITHMS-FLOWFIELD-v2.0")
    print("="*60 + "\n")

    # 测试 1: 数字根与五行
    print("📍 测试 1: 数字根与五行")
    test_text = "下一步怎么做"
    dr = DigitalRootCalculator.calculate(test_text)
    wx = DigitalRootCalculator.map_to_wuxing(dr)
    print(f"   文本: {test_text}")
    print(f"   数字根: {dr}")
    print(f"   五行: {wx.value}\n")

    # 测试 2: 洛书九宫
    print("📍 测试 2: 洛书九宫")
    palace_5 = LuoshuMatrix.get_palace(5)
    print(f"   中宫信息: {palace_5['name']}")
    print(f"   含义: {palace_5['meaning']}")
    resonance = LuoshuMatrix.check_resonance(5, 1)
    print(f"   中宫与坎宫共鸣: {resonance}\n")

    # 测试 3: 三才系统
    print("📍 测试 3: 三才系统")
    engine = FlowFieldEngine()
    sancai_result = engine.sancai.calculate_sancai(test_text)
    print(f"   天才: {sancai_result['tian']['wuxing'].value} (dr={sancai_result['tian']['dr']})")
    print(f"   地才: {sancai_result['di']['wuxing'].value} (dr={sancai_result['di']['dr']})")
    print(f"   人才: {sancai_result['ren']['wuxing'].value} (dr={sancai_result['ren']['dr']})")
    print(f"   协调度: {sancai_result['harmony']}\n")

    # 测试 4: 流场融合
    print("📍 测试 4: 流场融合")
    flow_state = engine.calculate_flow(test_text)
    print(f"   中心宫位: {flow_state.center}")
    print(f"   谐和度: {flow_state.harmony_index}")
    print(f"   流向: {flow_state.flow_direction}\n")

    # 测试 5: 建议生成
    print("📍 测试 5: 建议生成")
    recommendation = engine.generate_recommendation(flow_state)
    print(f"   谐和级别: {recommendation['harmony_level']}")
    print(f"   建议行动: {recommendation['recommended_action']}\n")

    print("="*60)
    print("✅ 核心算法系统初始化完成")
    print("="*60 + "\n")
    print("🐉 龍魂算法 · 易经五行 · 三才流场 · UID9622不免责")
