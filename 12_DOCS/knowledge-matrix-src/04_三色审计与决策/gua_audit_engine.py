# DNA: #龍芯⚡️丙午·丙申·戊辰·丙辰·䷸巽为风-CODE-补DNA-5ce3faa5
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
👁️ 上帝之眼 · 64卦审计算法引擎
DNA: #ZHUGEXIN⚡️2025-🇨🇳🐉👁️-64GUA-AUDIT-ENGINE-V1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅

将系统状态映射到64卦，自动推演审计结论。
8维度指标 → 上卦 + 下卦 → 64卦之一 → 三色审计 + 建议。
"""

import json
import time
import hashlib
import statistics
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict


# ============================================================
# DNA 追溯
# ============================================================

def 生成DNA(動作: str, 卦名: str) -> str:
    時間戳 = time.strftime("%Y%m%d-%H%M%S")
    熵 = hashlib.sha256(f"{動作}-{卦名}-{time.time_ns()}".encode()).hexdigest()[:8].upper()
    return f"#ZHUGEXIN⚡️2025-🇨🇳🐉👁️-64GUA-AUDIT-{動作}-{卦名}-{熵}"


# ============================================================
# 64卦审计算法引擎
# ============================================================

@dataclass
class GuaAuditResult:
    upper_gua: str
    lower_gua: str
    gua_name: str
    gua_number: int
    audit_color: str
    suggestion: str
    risk_level: str
    confidence: float
    metrics: Dict[str, float]
    dna_code: str
    timestamp: str

    def to_dict(self) -> Dict:
        return asdict(self)


class GuaAuditEngine:
    """64卦审计算法引擎"""

    def __init__(self):
        self.bagua = {
            '☰': {'name': '乾', 'attr': '创新突破', 'value': 7},
            '☷': {'name': '坤', 'attr': '支持辅助', 'value': 8},
            '☳': {'name': '震', 'attr': '快速响应', 'value': 4},
            '☴': {'name': '巽', 'attr': '渗透优化', 'value': 5},
            '☵': {'name': '坎', 'attr': '风险管控', 'value': 6},
            '☲': {'name': '离', 'attr': '传播表达', 'value': 3},
            '☶': {'name': '艮', 'attr': '坚守防御', 'value': 7},
            '☱': {'name': '兑', 'attr': '协作联动', 'value': 2}
        }
        self.liushisi_gua = self._init_64gua()

    def _init_64gua(self) -> Dict[str, Dict]:
        """初始化64卦完整映射表"""
        # 八卦组合生成64卦
        gua_names = {
            '☰☰': ('乾为天', 1, 'low'),
            '☰☷': ('泰', 11, 'low'),
            '☰☳': ('大壮', 34, 'low'),
            '☰☴': ('小畜', 9, 'medium'),
            '☰☵': ('需', 5, 'medium'),
            '☰☲': ('大有', 14, 'low'),
            '☰☶': ('大畜', 26, 'low'),
            '☰☱': ('夬', 43, 'medium'),
            '☷☰': ('否', 12, 'high'),
            '☷☷': ('坤为地', 2, 'medium'),
            '☷☳': ('豫', 16, 'medium'),
            '☷☴': ('观', 20, 'medium'),
            '☷☵': ('比', 8, 'medium'),
            '☷☲': ('晋', 35, 'medium'),
            '☷☶': ('剥', 23, 'high'),
            '☷☱': ('萃', 45, 'medium'),
            '☳☰': ('无妄', 25, 'medium'),
            '☳☷': ('复', 24, 'medium'),
            '☳☳': ('震为雷', 51, 'medium'),
            '☳☴': ('益', 42, 'low'),
            '☳☵': ('屯', 3, 'medium'),
            '☳☲': ('噬嗑', 21, 'medium'),
            '☳☶': ('颐', 27, 'medium'),
            '☳☱': ('随', 17, 'low'),
            '☴☰': ('姤', 44, 'high'),
            '☴☷': ('升', 46, 'low'),
            '☴☳': ('恒', 32, 'low'),
            '☴☴': ('巽为风', 57, 'medium'),
            '☴☵': ('井', 48, 'medium'),
            '☴☲': ('鼎', 50, 'low'),
            '☴☶': ('蛊', 18, 'high'),
            '☴☱': ('大过', 28, 'high'),
            '☵☰': ('讼', 6, 'high'),
            '☵☷': ('师', 7, 'medium'),
            '☵☳': ('解', 40, 'low'),
            '☵☴': ('涣', 59, 'medium'),
            '☵☵': ('坎为水', 29, 'high'),
            '☵☲': ('未济', 64, 'high'),
            '☵☶': ('蒙', 4, 'medium'),
            '☵☱': ('困', 47, 'high'),
            '☲☰': ('同人', 13, 'low'),
            '☲☷': ('明夷', 36, 'high'),
            '☲☳': ('丰', 55, 'medium'),
            '☲☴': ('家人', 37, 'low'),
            '☲☵': ('既济', 63, 'low'),
            '☲☲': ('离为火', 30, 'medium'),
            '☲☶': ('贲', 22, 'medium'),
            '☲☱': ('革', 49, 'medium'),
            '☶☰': ('遁', 33, 'medium'),
            '☶☷': ('谦', 15, 'low'),
            '☶☳': ('小过', 62, 'medium'),
            '☶☴': ('渐', 53, 'low'),
            '☶☵': ('蹇', 39, 'high'),
            '☶☲': ('旅', 56, 'medium'),
            '☶☶': ('艮为山', 52, 'medium'),
            '☶☱': ('咸', 31, 'low'),
            '☱☰': ('履', 10, 'medium'),
            '☱☷': ('临', 19, 'low'),
            '☱☳': ('归妹', 54, 'medium'),
            '☱☴': ('中孚', 61, 'low'),
            '☱☵': ('节', 60, 'medium'),
            '☱☲': ('睽', 38, 'medium'),
            '☱☶': ('损', 41, 'medium'),
            '☱☱': ('兑为泽', 58, 'low'),
        }
        result = {}
        for combo, (name, number, risk) in gua_names.items():
            suggestions = {
                'low': '系统运行良好，保持当前态势，可适当进取',
                'medium': '系统基本稳定，存在局部风险，建议优化后推进',
                'high': '系统存在显著风险，建议暂停并整改关键问题',
            }
            result[combo] = {
                'number': number,
                'name': name,
                'risk_level': risk,
                'suggestion': suggestions.get(risk, '请结合具体指标人工研判')
            }
        return result

    def calculate_gua(self, metrics: Dict[str, float], context: str = "") -> GuaAuditResult:
        """
        根据系统指标计算当前卦象并返回审计结果。

        metrics = {
            'innovation': 0-100,    # 创新突破度
            'support': 0-100,       # 支持辅助度
            'response': 0-100,      # 快速响应度
            'optimization': 0-100,  # 渗透优化度
            'risk_control': 0-100,  # 风险管控度
            'communication': 0-100, # 传播表达度
            'defense': 0-100,       # 坚守防御度
            'collaboration': 0-100  # 协作联动度
        }
        """
        required_keys = {'innovation', 'support', 'response', 'optimization',
                         'risk_control', 'communication', 'defense', 'collaboration'}
        if not required_keys.issubset(metrics.keys()):
            missing = required_keys - set(metrics.keys())
            raise ValueError(f"缺少8维度指标: {missing}")

        # 计算上卦（外卦）：创新 + 传播表达 + 协作联动
        upper_score = (
            metrics['innovation'] * 0.3 +
            metrics['communication'] * 0.3 +
            metrics['collaboration'] * 0.4
        )
        upper_gua = self._score_to_gua(upper_score, 'upper')

        # 计算下卦（内卦）：支持辅助 + 风险管控 + 坚守防御
        lower_score = (
            metrics['support'] * 0.3 +
            metrics['risk_control'] * 0.4 +
            metrics['defense'] * 0.3
        )
        lower_gua = self._score_to_gua(lower_score, 'lower')

        gua_combo = f"{upper_gua}{lower_gua}"
        gua_info = self.liushisi_gua.get(gua_combo, {
            'number': 0,
            'name': '未知',
            'risk_level': 'medium',
            'suggestion': '未识别的卦象组合，请人工复核'
        })

        audit_color = self._determine_audit_color(gua_info, metrics)
        confidence = self._calculate_confidence(metrics)

        # 根据审计颜色补充建议
        suggestion = gua_info['suggestion']
        if audit_color == '🔴':
            suggestion = f"【🔴 立即拦截】{suggestion}"
        elif audit_color == '🟡':
            suggestion = f"【🟡 条件通过】{suggestion}"
        else:
            suggestion = f"【🟢 批准执行】{suggestion}"

        return GuaAuditResult(
            upper_gua=upper_gua,
            lower_gua=lower_gua,
            gua_name=gua_info['name'],
            gua_number=gua_info['number'],
            audit_color=audit_color,
            suggestion=suggestion,
            risk_level=gua_info['risk_level'],
            confidence=confidence,
            metrics=metrics,
            dna_code=生成DNA("RUN", gua_info['name']),
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        )

    def _score_to_gua(self, score: float, position: str) -> str:
        """将0-100分映射到八卦之一"""
        if score >= 90:
            return '☰'
        elif score >= 80:
            return '☱'
        elif score >= 70:
            return '☲'
        elif score >= 60:
            return '☳'
        elif score >= 50:
            return '☴'
        elif score >= 40:
            return '☵'
        elif score >= 30:
            return '☶'
        else:
            return '☷'

    def _determine_audit_color(self, gua_info: Dict, metrics: Dict[str, float]) -> str:
        """根据卦象和指标确定审计颜色"""
        risk_level = gua_info.get('risk_level', 'medium')
        avg_score = sum(metrics.values()) / len(metrics)
        min_score = min(metrics.values())

        if risk_level == 'high' or avg_score < 50 or min_score < 30:
            return '🔴'
        elif risk_level == 'low' and avg_score >= 70 and min_score >= 50:
            return '🟢'
        else:
            return '🟡'

    def _calculate_confidence(self, metrics: Dict[str, float]) -> float:
        """计算置信度：指标标准差越小，系统越平衡，置信度越高"""
        values = list(metrics.values())
        if len(values) < 2:
            return 0.5
        std_dev = statistics.stdev(values)
        confidence = max(0.5, 1 - (std_dev / 100))
        return round(confidence, 2)

    def dynamic_divination(self, current_gua: str, trend: Dict[str, str]) -> Dict:
        """
        基于当前卦象和8维度变化趋势，推演未来24小时状态。
        trend: {'innovation': 'up'|'down'|'stable', ...}
        """
        if len(current_gua) != 2:
            return {"error": "current_gua 必须是两位卦符"}

        upper, lower = current_gua[0], current_gua[1]
        change_reasons = []

        # 简单的变卦规则：下降趋势可能导致上卦或下卦降级
        upper_trend = trend.get('innovation', 'stable')
        lower_trend = trend.get('risk_control', 'stable')

        bagua_order = ['☰', '☱', '☲', '☳', '☴', '☵', '☶', '☷']

        def shift_gua(gua: str, direction: str) -> str:
            if gua not in bagua_order:
                return gua
            idx = bagua_order.index(gua)
            if direction == 'down' and idx < len(bagua_order) - 1:
                return bagua_order[idx + 1]
            elif direction == 'up' and idx > 0:
                return bagua_order[idx - 1]
            return gua

        new_upper = shift_gua(upper, upper_trend)
        new_lower = shift_gua(lower, lower_trend)

        if new_upper != upper:
            change_reasons.append(f"创新/沟通/协作趋势 {upper_trend}，上卦由 {self.bagua[upper]['name']} 变 {self.bagua[new_upper]['name']}")
        if new_lower != lower:
            change_reasons.append(f"支持/风险/防御趋势 {lower_trend}，下卦由 {self.bagua[lower]['name']} 变 {self.bagua[new_lower]['name']}")

        future_combo = f"{new_upper}{new_lower}"
        future_info = self.liushisi_gua.get(future_combo, {
            'name': '未知', 'risk_level': 'medium', 'suggestion': ''
        })

        risk_prediction = '🟢' if future_info['risk_level'] == 'low' else '🔴' if future_info['risk_level'] == 'high' else '🟡'

        return {
            'future_gua': future_combo,
            'future_gua_name': future_info['name'],
            'change_reason': '；'.join(change_reasons) or '卦象保持稳定',
            'risk_prediction': risk_prediction,
            'action_suggestion': future_info['suggestion']
        }


# ============================================================
# 内置示例
# ============================================================

def demo():
    engine = GuaAuditEngine()
    metrics = {
        'innovation': 85,
        'support': 78,
        'response': 65,
        'optimization': 72,
        'risk_control': 55,
        'communication': 80,
        'defense': 90,
        'collaboration': 88
    }
    result = engine.calculate_gua(metrics, context="部署新功能")
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    demo()
