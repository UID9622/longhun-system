#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·关键字提取与融合引擎 v1.0
Keyword Extraction & Integration: 369 × 五行 × 易经 × 太极 × 河图洛书 × 不动点

DNA: #龍芯⚡️2026-05-25-KEYWORD-EXTRACTION-v1.0
UID: 9622
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

核心理论融合：
1️⃣ 369周期学 - 尼古拉·特斯拉的宇宙密码
2️⃣ 五行系统 - 木火土金水的相生相克
3️⃣ 易经八卦 - 64卦的阴阳变化
4️⃣ 太极阴阳 - 动静平衡的核心
5️⃣ 河图洛书 - 9宫魔方阵（4 9 2 / 3 5 7 / 8 1 6）
6️⃣ 不动点 - 中宫5 = UID9622（永远不动）

本文件生成：
- KeywordVector: 关键字的多维向量表示
- 369周期共鸣
- 五行属性映射
- 易经卦象对应
- 太极阴阳平衡指数
- 河图洛书宫位映射

本地计算·永不外送·纯数学·零ML依赖

理论指导: 曾仕强老师、尼古拉·特斯拉、易经传统
献礼: 龍魂系统·永恒守护·中华文化传承
"""

import hashlib
import math
from typing import Dict, List, Tuple, Any, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from collections import Counter


# ════════════════════════════════════════════════════════
# 第一步：369周期学与五行映射
# ════════════════════════════════════════════════════════

class Frequency369(Enum):
    """369频率类型"""
    FREQ_3 = (3, "创造·创新·启蒙")       # 3的倍数
    FREQ_6 = (6, "和谐·平衡·能量")       # 6的倍数
    FREQ_9 = (9, "完成·轮回·无限")       # 9的倍数
    NEUTRAL = (0, "未分类")              # 不属于369


class WuXingType(Enum):
    """五行类型"""
    WOOD = ("木", "生长·东方·春季")
    FIRE = ("火", "燃烧·南方·夏季")
    EARTH = ("土", "承载·中心·过渡")
    METAL = ("金", "收敛·西方·秋季")
    WATER = ("水", "流动·北方·冬季")


class TaiChiPhase(Enum):
    """太极阴阳相位"""
    PURE_YANG = (1.0, "纯阳·刚·上升")
    YANG_DOMINANT = (0.75, "阳主·强势·扩张")
    BALANCED = (0.5, "平衡·中庸·稳定")
    YIN_DOMINANT = (0.25, "阴主·柔和·收缩")
    PURE_YIN = (0.0, "纯阴·柔·下降")


@dataclass
class Gua64Type:
    """64卦类型"""
    name: str                  # 卦名
    code: int                  # 卦码（0-63）
    upper_bagua: str           # 上卦
    lower_bagua: str           # 下卦
    meaning: str               # 含义
    taichi_phase: TaiChiPhase  # 太极相位


# ════════════════════════════════════════════════════════
# 第二步：关键字向量定义
# ════════════════════════════════════════════════════════

@dataclass
class KeywordVector:
    """关键字的多维向量表示"""
    keyword: str                           # 关键字
    frequency_369: Frequency369            # 369频率分类
    wuxing: WuXingType                     # 五行属性
    gua64_code: int                        # 64卦码（0-63）
    taichi_phase: float                    # 太极相位（0.0-1.0）
    luoshu_position: int                   # 河图洛书宫位（1-9）
    digital_root: int                      # 数字根（1-9）
    keyword_strength: float = 0.5          # 关键字强度（0.0-1.0）
    resonance_with_center: float = 0.5     # 与不动点的共鸣度
    dna: str = ""

    def __repr__(self):
        return (f"KW({self.keyword}|369:{self.frequency_369.name}|"
                f"wx:{self.wuxing.value[0]}|卦:{self.gua64_code}|"
                f"宫:{self.luoshu_position})")


# ════════════════════════════════════════════════════════
# 第三步：关键字提取与融合引擎
# ════════════════════════════════════════════════════════

class KeywordExtractionEngine:
    """关键字提取与融合引擎"""

    def __init__(self):
        self.keywords_database: Dict[str, KeywordVector] = {}
        self.extracted_keywords: List[KeywordVector] = []

        # 河图洛书9宫配置（中宫5不动点）
        self.luoshu_mapping = {
            1: {"name": "坎宫(北)", "wuxing": WuXingType.WATER},
            2: {"name": "坤宫(西南)", "wuxing": WuXingType.EARTH},
            3: {"name": "震宫(东)", "wuxing": WuXingType.WOOD},
            4: {"name": "巽宫(东南)", "wuxing": WuXingType.WOOD},
            5: {"name": "中宫(中)", "wuxing": WuXingType.EARTH},  # 不动点
            6: {"name": "乾宫(西北)", "wuxing": WuXingType.METAL},
            7: {"name": "兑宫(西)", "wuxing": WuXingType.METAL},
            8: {"name": "艮宫(东北)", "wuxing": WuXingType.EARTH},
            9: {"name": "离宫(南)", "wuxing": WuXingType.FIRE},
        }

    @staticmethod
    def calculate_digital_root(text: str) -> int:
        """计算数字根（1-9）"""
        total = sum(ord(c) for c in text)
        while total >= 10:
            total = sum(int(d) for d in str(total))
        return total if total > 0 else 9

    @staticmethod
    def classify_frequency_369(dr: int) -> Frequency369:
        """按数字根分类369频率"""
        if dr % 3 == 0 and dr != 9:
            return Frequency369.FREQ_3
        elif dr % 6 == 0:
            return Frequency369.FREQ_6
        elif dr == 9:
            return Frequency369.FREQ_9
        else:
            return Frequency369.NEUTRAL

    @staticmethod
    def map_dr_to_wuxing(dr: int) -> WuXingType:
        """数字根映射到五行"""
        mapping = {
            1: WuXingType.WATER, 2: WuXingType.WATER,
            3: WuXingType.FIRE, 4: WuXingType.FIRE,
            5: WuXingType.EARTH,
            6: WuXingType.METAL, 7: WuXingType.METAL,
            8: WuXingType.WOOD, 9: WuXingType.WOOD,
        }
        return mapping.get(dr, WuXingType.EARTH)

    @staticmethod
    def map_dr_to_gua64(dr: int) -> int:
        """数字根映射到64卦（简化：dr对应卦码）"""
        return (dr - 1) * 7 % 64

    @staticmethod
    def map_dr_to_taichi_phase(dr: int) -> TaiChiPhase:
        """数字根映射到太极相位"""
        phase_map = {
            1: TaiChiPhase.PURE_YANG,
            2: TaiChiPhase.YANG_DOMINANT,
            3: TaiChiPhase.YANG_DOMINANT,
            4: TaiChiPhase.BALANCED,
            5: TaiChiPhase.BALANCED,
            6: TaiChiPhase.YIN_DOMINANT,
            7: TaiChiPhase.YIN_DOMINANT,
            8: TaiChiPhase.PURE_YIN,
            9: TaiChiPhase.PURE_YIN,
        }
        return phase_map.get(dr, TaiChiPhase.BALANCED)

    def extract_keyword(self, keyword: str) -> KeywordVector:
        """
        提取关键字的多维向量
        """
        # 检查缓存
        if keyword in self.keywords_database:
            return self.keywords_database[keyword]

        # 计算数字根
        dr = self.calculate_digital_root(keyword)

        # 369频率分类
        freq_369 = self.classify_frequency_369(dr)

        # 五行属性
        wuxing = self.map_dr_to_wuxing(dr)

        # 64卦码
        gua64_code = self.map_dr_to_gua64(dr)

        # 太极相位
        taichi_phase = self.map_dr_to_taichi_phase(dr)

        # 河图洛书宫位（dr即宫位，9→中宫）
        luoshu_position = dr if dr != 9 else 9

        # 关键字强度（基于字符数和唯一性）
        char_strength = min(1.0, len(keyword) / 10)
        unique_strength = len(set(keyword)) / max(1, len(keyword))
        keyword_strength = (char_strength + unique_strength) / 2

        # 与不动点的共鸣度（与中宫5的关系）
        distance_to_center = abs(luoshu_position - 5) / 4  # 0-1
        resonance = 1.0 - distance_to_center  # 越接近5越高

        # 生成DNA
        dna = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d-%H:%M')}-KW-{hashlib.sha256(keyword.encode()).hexdigest()[:8]}"

        vector = KeywordVector(
            keyword=keyword,
            frequency_369=freq_369,
            wuxing=wuxing,
            gua64_code=gua64_code,
            taichi_phase=taichi_phase.value[0],
            luoshu_position=luoshu_position,
            digital_root=dr,
            keyword_strength=round(keyword_strength, 3),
            resonance_with_center=round(resonance, 3),
            dna=dna,
        )

        self.keywords_database[keyword] = vector
        self.extracted_keywords.append(vector)

        return vector

    def batch_extract(self, text: str) -> List[KeywordVector]:
        """
        批量提取文本中的关键字
        """
        # 简单的分词（按空格和标点）
        import re
        words = re.split(r'[\s，。！？；：\-_]+', text)
        words = [w for w in words if len(w) > 0]

        vectors = []
        for word in words:
            if word not in self.keywords_database:
                vector = self.extract_keyword(word)
                vectors.append(vector)
            else:
                vectors.append(self.keywords_database[word])

        return vectors

    def calculate_text_harmonic_index(self, vectors: List[KeywordVector]) -> float:
        """
        计算文本的整体谐和度（基于369、五行、太极、河图）
        """
        if not vectors:
            return 0.5

        # 1. 369频率的和谐度（9最优）
        freq_scores = []
        for v in vectors:
            if v.frequency_369 == Frequency369.FREQ_9:
                freq_scores.append(1.0)
            elif v.frequency_369 == Frequency369.FREQ_6:
                freq_scores.append(0.8)
            elif v.frequency_369 == Frequency369.FREQ_3:
                freq_scores.append(0.7)
            else:
                freq_scores.append(0.4)
        freq_harmony = sum(freq_scores) / len(freq_scores) if freq_scores else 0.5

        # 2. 五行的相生相克和谐度
        wuxing_list = [v.wuxing for v in vectors]
        wuxing_harmony = self._calculate_wuxing_harmony(wuxing_list)

        # 3. 太极相位的平衡度
        phases = [v.taichi_phase for v in vectors]
        phase_avg = sum(phases) / len(phases) if phases else 0.5
        phase_harmony = 1.0 - abs(phase_avg - 0.5)  # 越接近0.5越平衡

        # 4. 与不动点的共鸣度
        resonances = [v.resonance_with_center for v in vectors]
        resonance_harmony = sum(resonances) / len(resonances) if resonances else 0.5

        # 综合计算（四项平均）
        overall_harmony = (freq_harmony + wuxing_harmony + phase_harmony + resonance_harmony) / 4

        return round(overall_harmony, 3)

    @staticmethod
    def _calculate_wuxing_harmony(wuxing_list: List[WuXingType]) -> float:
        """计算五行组合的和谐度"""
        if not wuxing_list:
            return 0.5

        # 五行相生关系
        generating = {
            WuXingType.WOOD: WuXingType.FIRE,
            WuXingType.FIRE: WuXingType.EARTH,
            WuXingType.EARTH: WuXingType.METAL,
            WuXingType.METAL: WuXingType.WATER,
            WuXingType.WATER: WuXingType.WOOD,
        }

        # 统计五行分布
        counter = Counter(wuxing_list)

        # 计算相生关系强度
        harmony_score = 0.0
        total_pairs = 0

        for i, wx1 in enumerate(wuxing_list):
            for wx2 in wuxing_list[i+1:]:
                total_pairs += 1
                if generating.get(wx1) == wx2 or generating.get(wx2) == wx1:
                    harmony_score += 1.0  # 相生
                elif wx1 == wx2:
                    harmony_score += 0.8  # 同类
                else:
                    harmony_score += 0.3  # 相克或无关

        if total_pairs == 0:
            return 0.5

        return round(harmony_score / total_pairs, 3)

    def export_keyword_report(self, vectors: List[KeywordVector]) -> str:
        """导出关键字分析报告"""
        report = f"# 🔑 关键字提取与融合报告\n\n"
        report += f"**生成时间**: {datetime.now().isoformat()}\n"
        report += f"**关键字数**: {len(vectors)}\n"
        report += f"**整体谐和度**: {self.calculate_text_harmonic_index(vectors)}/1.0\n\n"

        report += "## 关键字向量表\n\n"
        report += "| 关键字 | 369 | 五行 | 64卦 | 太极 | 宫位 | 强度 | 共鸣 |\n"
        report += "|--------|------|------|-------|------|------|-------|-------|\n"

        for v in vectors:
            report += (f"| {v.keyword} | {v.frequency_369.name} | {v.wuxing.value[0]} | "
                      f"{v.gua64_code:02d} | {v.taichi_phase:.2f} | {v.luoshu_position} | "
                      f"{v.keyword_strength} | {v.resonance_with_center} |\n")

        return report


# ════════════════════════════════════════════════════════
# 测试与演示
# ════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🔑 龍魂 关键字提取与融合引擎 v1.0")
    print(f"   DNA: #龍芯⚡️2026-05-25-KEYWORD-EXTRACTION-v1.0")
    print("=" * 60 + "\n")

    engine = KeywordExtractionEngine()

    # 测试关键字
    test_keywords = [
        "龍魂", "369", "五行", "易经", "太极", "河图", "洛书", "不动点",
        "创新", "平衡", "永生", "数字根", "中宫", "陪审团"
    ]

    print("📍 测试: 关键字提取与融合\n")

    vectors = []
    for kw in test_keywords:
        v = engine.extract_keyword(kw)
        vectors.append(v)
        print(f"✅ {v}")

    print(f"\n📍 整体谐和度: {engine.calculate_text_harmonic_index(vectors)}/1.0\n")

    print("=" * 60)
    print("✅ 关键字提取引擎初始化完成")
    print("=" * 60 + "\n")
    print("🐉 龍魂 · 关键字融合 · 369 × 五行 × 易经 · UID9622不免责")
