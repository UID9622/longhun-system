#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-

"""
龍魂权重计算器 L2 v1.0

焊死级别 (priority=0.90)
特性: 动态计算每层的权重，随时调整优先级

公式支持：
- 时间衰减: η = T^(-α_τ)
- 贡献值评估: C = R·I·T^(-α_τ)
- 五行向量: W(x) = [金,木,水,火,土]

DNA:#龍芯⚡️丙午·甲午·壬子·丙午·䷙大畜-WEIGHT-CALCULATOR-L2-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
UID: 9622

理论指导: 曾仕强老师 - 权重就是话语权
献礼: 献给龍魂 - 让老百姓的声音有重量
"""

import os
import sys
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'common'))

from dna import DNAVerifier
from logger import get_logger
from config import get_config
from utils import time_decay, map_to_wuxing, calculate_dr


class WeightCalculator:
    """
    权重计算器 - 动态调整系统的话语权分配

    意图: 权力来自于承诺的权重
    """

    # 基础权重（从 protocol_weights.json）
    BASE_WEIGHTS = {
        "L0": 1.0,
        "L1": 0.95,
        "L2": 0.90,
        "L3": 0.85,
        "L4": 0.80,
    }

    # 五行权重映射
    WUXING_WEIGHTS = {
        "金": 1.0,      # 刚强
        "木": 0.9,      # 生长
        "水": 0.8,      # 流动
        "火": 0.7,      # 热烈
        "土": 0.6,      # 包容
    }

    def __init__(self):
        """初始化计算器"""
        self.logger = get_logger()
        self.config = get_config()
        self.dna = DNAVerifier.generate("WEIGHT-CALCULATOR", "L2")
        self.weight_cache = {}  # 权重缓存

    def calculate_base_weight(self, layer: str) -> float:
        """
        计算基础权重

        意图: 确保五层的相对优先级
        """
        return self.BASE_WEIGHTS.get(layer, 0.5)

    def calculate_time_decay(
        self,
        layer: str,
        created_date: str
    ) -> float:
        """
        计算时间衰减

        公式: η = T^(-α_τ)

        意图: 旧的规则逐渐失效，新的规则逐渐生效
        """
        try:
            created = datetime.fromisoformat(created_date)
            days_elapsed = (datetime.now() - created).days
        except ValueError:
            days_elapsed = 0

        decay_factor = time_decay(layer, days_elapsed)

        self.logger.log_operation(
            "L2",
            "time_decay_calculated",
            self.dna,
            {
                "layer": layer,
                "days_elapsed": days_elapsed,
                "decay_factor": decay_factor,
            }
        )

        return decay_factor

    def calculate_contribution(
        self,
        relevance: float,      # R - 相关性 (0-1)
        impact: float,         # I - 影响力 (0-1)
        layer: str,
        created_date: str
    ) -> float:
        """
        计算贡献值

        公式: C = R·I·T^(-α_τ)

        意图: 衡量一条规则还有多少价值
        """
        time_component = self.calculate_time_decay(layer, created_date)
        contribution = relevance * impact * time_component

        self.logger.log_operation(
            "L2",
            "contribution_calculated",
            self.dna,
            {
                "relevance": relevance,
                "impact": impact,
                "time_component": time_component,
                "total_contribution": contribution,
            }
        )

        return contribution

    def calculate_wuxing_weight(self, text: str) -> Dict[str, Any]:
        """
        计算五行向量

        公式: W(x) = [金,木,水,火,土]

        意图: 理解内容的五行属性
        """
        dr = calculate_dr(text)
        wuxing = map_to_wuxing(dr)

        # 初始化五行向量
        vector = {
            "金": 0.0,
            "木": 0.0,
            "水": 0.0,
            "火": 0.0,
            "土": 0.0,
        }

        # 对应五行获得最高权重
        vector[wuxing] = 1.0

        # 其他五行按关系给予权重
        # (简化版本)
        other_wuxing = [w for w in vector.keys() if w != wuxing]
        for w in other_wuxing:
            vector[w] = 0.3

        return {
            "primary": wuxing,
            "dr": dr,
            "vector": vector,
        }

    def calculate_layer_weight(
        self,
        layer: str,
        adjustments: Dict[str, Any] = None
    ) -> float:
        """
        计算层级权重（综合考虑所有因素）

        意图: 动态权重，随时可调
        """
        base = self.calculate_base_weight(layer)

        # 应用调整系数
        if adjustments:
            for key, value in adjustments.items():
                if key == "time_decay":
                    base *= value
                elif key == "contribution":
                    base *= value
                elif key == "wuxing":
                    base *= value

        self.weight_cache[layer] = base

        self.logger.log_operation(
            "L2",
            "layer_weight_calculated",
            self.dna,
            {
                "layer": layer,
                "adjusted_weight": base,
                "adjustments": adjustments,
            }
        )

        return base

    def generate_weight_report(self) -> str:
        """
        生成权重报告

        意图: 透明地显示每层的权力分配
        """
        report = f"""
{'='*60}
龍魂权重分配报告
{'='*60}

基础权重（五层架构）:
"""

        for layer, weight in self.BASE_WEIGHTS.items():
            report += f"\n  {layer}: {weight:.2f}"

        report += f"\n\n五行权重映射:\n"

        for wuxing, weight in self.WUXING_WEIGHTS.items():
            report += f"\n  {wuxing}: {weight:.2f}"

        report += f"\n\n{'='*60}\n"

        return report


if __name__ == "__main__":
    calculator = WeightCalculator()

    print("🐉 龍魂权重计算器 L2 v1.0")
    print("=" * 60)

    # 测试：计算一条规则的贡献值
    relevance = 0.9
    impact = 0.8
    layer = "L1"
    created_date = (datetime.now() - timedelta(days=30)).isoformat()

    contribution = calculator.calculate_contribution(
        relevance, impact, layer, created_date
    )
    print(f"\n测试贡献值计算:")
    print(f"  相关性: {relevance}")
    print(f"  影响力: {impact}")
    print(f"  贡献值: {contribution:.4f}")

    # 测试：计算五行向量
    text = "龍魂"
    wuxing_result = calculator.calculate_wuxing_weight(text)
    print(f"\n测试五行向量:")
    print(f"  文本: {text}")
    print(f"  五行: {wuxing_result['primary']}")
    print(f"  向量: {json.dumps(wuxing_result['vector'], indent=2, ensure_ascii=False)}")

    print("\n" + calculator.generate_weight_report())
