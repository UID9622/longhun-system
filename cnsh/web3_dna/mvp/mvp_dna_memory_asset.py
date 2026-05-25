#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·Web3-DNA DNA记忆资产化系统 v1.0
DNA Memory Asset-ification: Market Pricing Engine

DNA: #龍芯⚡️2026-05-25-WEB3-DNA-MEMORY-ASSET-v1.0
UID: 9622
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

§39 MVP三件套第2件：DNA记忆资产化与价格模型

核心理论：
- 记忆 → 数字化DNA资产
- DNA资产可交易、可定价、可继承
- 价格模型基于：(1) 记忆质量评分 (2) 市场热度 (3) 稀缺性系数 (4) 时间衰减

价格算法：
  Price(t) = BasePrice × QualityFactor × MarketFactor × RarityCoeff × TimeDecay(t)

  其中：
    BasePrice = 100 e-CNY (基础价格)
    QualityFactor = memory_quality / 100  (0.0-1.0)
    MarketFactor = 0.8 - 1.2 (市场周期)
    RarityCoeff = log(1 + supply_inverse)  (稀缺性)
    TimeDecay(t) = e^(-t/365) (365天周期衰减)

本地执行·完全自主·永不外送·可恢复·可追溯

理论指导: 曾仕强老师（永恒显示）
献礼: 龍魂系统·永恒守护·中华文化传承
"""

import hashlib
import math
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import json


# ════════════════════════════════════════════════════════
# 第一步：DNA记忆资产定义
# ════════════════════════════════════════════════════════

class MemoryQualityLevel(Enum):
    """记忆质量等级"""
    PRISTINE = (95, "完美无瑕")       # 95-100分
    EXCELLENT = (85, "优秀")          # 85-94分
    GOOD = (75, "良好")              # 75-84分
    FAIR = (65, "一般")              # 65-74分
    POOR = (45, "较差")              # 45-64分


@dataclass
class DNAMemoryAsset:
    """DNA记忆资产"""
    asset_id: str                      # 资产ID
    owner_id: str                      # 拥有者ID
    memory_content: str                # 记忆内容（摘要）
    memory_quality_score: int          # 质量评分（0-100）
    memory_category: str               # 类别（personal/professional/creative/scientific）
    created_timestamp: int             # 创建时间戳
    market_listings: int = 0           # 市场挂单数
    trading_volume: float = 0.0        # 交易量（e-CNY）
    scarcity_coefficient: float = 1.0  # 稀缺性系数
    dna: str = ""                      # DNA追溯码
    price_history: List[Tuple[str, float]] = field(default_factory=list)  # 价格历史


@dataclass
class PricingResult:
    """定价结果"""
    asset_id: str
    current_price: float               # 当前价格（e-CNY）
    base_price: float                  # 基础价格
    quality_factor: float              # 质量因子
    market_factor: float               # 市场因子
    rarity_coefficient: float          # 稀缺性系数
    time_decay_factor: float           # 时间衰减因子
    price_breakdown: Dict[str, float]  # 价格分解明细
    effective_date: str                # 有效日期
    dna: str                           # DNA追溯码


# ════════════════════════════════════════════════════════
# 第二步：质量评分引擎
# ════════════════════════════════════════════════════════

class MemoryQualityScorer:
    """记忆质量评分器"""

    @staticmethod
    def score_memory_quality(
        content: str,
        category: str,
        metadata: Dict[str, Any] = None
    ) -> int:
        """
        评分记忆质量（0-100）

        评分因素：
        1. 内容长度与复杂度 (30%)
        2. 信息密度 (25%)
        3. 原创性 (25%)
        4. 历史重要性 (20%)
        """
        metadata = metadata or {}

        # 因素1：内容长度与复杂度（30%）
        content_length = len(content)
        complexity_score = min(100, (content_length / 50))  # 每50字为一个单位
        factor1 = complexity_score * 0.30

        # 因素2：信息密度（25%）
        # 统计关键词数量
        keywords = metadata.get("keywords", [])
        keyword_density = min(100, len(keywords) * 10)
        factor2 = keyword_density * 0.25

        # 因素3：原创性（25%）
        # 基于内容哈希的唯一性
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        originality_score = (int(content_hash[:8], 16) % 100)  # 0-99
        factor3 = originality_score * 0.25

        # 因素4：历史重要性（20%）
        # 基于时间和类别
        category_importance = {
            "personal": 60,
            "professional": 80,
            "creative": 85,
            "scientific": 95,
        }
        factor4 = category_importance.get(category, 70) * 0.20

        total_score = int(factor1 + factor2 + factor3 + factor4)
        return max(0, min(100, total_score))

    @staticmethod
    def get_quality_level(score: int) -> MemoryQualityLevel:
        """根据分数获取质量等级"""
        if score >= 95:
            return MemoryQualityLevel.PRISTINE
        elif score >= 85:
            return MemoryQualityLevel.EXCELLENT
        elif score >= 75:
            return MemoryQualityLevel.GOOD
        elif score >= 65:
            return MemoryQualityLevel.FAIR
        else:
            return MemoryQualityLevel.POOR


# ════════════════════════════════════════════════════════
# 第三步：市场因子计算引擎
# ════════════════════════════════════════════════════════

class MarketFactorEngine:
    """市场因子计算引擎"""

    def __init__(self):
        self.market_sentiment = 0.8  # 当前市场情绪（0.0-2.0，1.0为中性）
        self.cycle_phase = "growth"  # 当前周期阶段

    def calculate_market_factor(self, category: str, trading_volume: float = 0.0) -> float:
        """
        计算市场因子（0.8-1.2）

        影响因素：
        1. 全局市场情绪 (40%)
        2. 类别热度 (35%)
        3. 成交量信号 (25%)
        """
        # 因素1：全局市场情绪
        market_sentiment_factor = self.market_sentiment * 0.4

        # 因素2：类别热度
        category_heat = {
            "personal": 0.9,       # 个人记忆较冷
            "professional": 1.0,   # 专业记忆中性
            "creative": 1.1,       # 创意记忆较热
            "scientific": 1.2,     # 科学记忆最热
        }
        category_heat_factor = category_heat.get(category, 1.0) * 0.35

        # 因素3：成交量信号
        volume_factor = 1.0
        if trading_volume > 100000:
            volume_factor = 1.1  # 高成交量提升
        elif trading_volume < 10000:
            volume_factor = 0.9  # 低成交量压低

        volume_signal = volume_factor * 0.25

        total_factor = market_sentiment_factor + category_heat_factor + volume_signal
        return max(0.8, min(1.2, total_factor))

    def calculate_rarity_coefficient(self, total_supply: int) -> float:
        """
        计算稀缺性系数
        公式：RarityCoeff = log(1 + 1/supply)

        供应量越少，稀缺性越高
        """
        if total_supply <= 0:
            return 1.0

        # 反向供应（供应越少，系数越大）
        inverse_supply = 1.0 / total_supply
        rarity = math.log(1 + inverse_supply * 100)  # 放大系数
        return max(1.0, min(2.0, rarity))


# ════════════════════════════════════════════════════════
# 第四步：DNA价格模型引擎（主类）
# ════════════════════════════════════════════════════════

class DNAMemoryAssetPricingEngine:
    """DNA记忆资产定价引擎"""

    def __init__(self):
        self.base_price = 100.0  # 基础价格（e-CNY）
        self.quality_scorer = MemoryQualityScorer()
        self.market_engine = MarketFactorEngine()
        self.asset_registry: Dict[str, DNAMemoryAsset] = {}
        self.pricing_history: List[PricingResult] = []

    def create_dna_memory_asset(
        self,
        owner_id: str,
        memory_content: str,
        category: str,
        metadata: Dict[str, Any] = None
    ) -> DNAMemoryAsset:
        """
        创建DNA记忆资产
        """
        metadata = metadata or {}

        # 评分记忆质量
        quality_score = self.quality_scorer.score_memory_quality(
            memory_content,
            category,
            metadata
        )

        # 生成资产ID和DNA
        asset_id = f"dna-asset-{hashlib.sha256(f'{owner_id}{memory_content}'.encode()).hexdigest()[:8]}"
        dna = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d-%H:%M')}-DNA-ASSET-{asset_id}"

        asset = DNAMemoryAsset(
            asset_id=asset_id,
            owner_id=owner_id,
            memory_content=memory_content[:100],  # 摘要
            memory_quality_score=quality_score,
            memory_category=category,
            created_timestamp=int(datetime.now().timestamp()),
            dna=dna,
        )

        self.asset_registry[asset_id] = asset
        return asset

    def calculate_price(
        self,
        asset_id: str,
        total_supply: int = 1000,
        trading_volume: float = 50000.0
    ) -> PricingResult:
        """
        计算DNA记忆资产的价格

        公式：
        Price = BasePrice × QualityFactor × MarketFactor × RarityCoeff × TimeDecay
        """
        asset = self.asset_registry.get(asset_id)
        if not asset:
            # 创建临时资产用于演示
            asset = DNAMemoryAsset(
                asset_id=asset_id,
                owner_id="unknown",
                memory_content="",
                memory_quality_score=70,
                memory_category="professional",
                created_timestamp=int(datetime.now().timestamp()),
            )

        # 1. 质量因子（QualityFactor = quality_score / 100）
        quality_factor = asset.memory_quality_score / 100.0

        # 2. 市场因子（0.8-1.2）
        market_factor = self.market_engine.calculate_market_factor(
            asset.memory_category,
            asset.trading_volume
        )

        # 3. 稀缺性系数
        rarity_coefficient = self.market_engine.calculate_rarity_coefficient(total_supply)

        # 4. 时间衰减（365天周期）
        time_elapsed = datetime.now().timestamp() - asset.created_timestamp
        time_decay = math.exp(-time_elapsed / (365 * 24 * 3600))  # 自然对数衰减

        # 5. 计算最终价格
        final_price = (
            self.base_price *
            quality_factor *
            market_factor *
            rarity_coefficient *
            time_decay
        )

        # 记录价格历史
        price_record = (datetime.now().isoformat(), final_price)
        asset.price_history.append(price_record)

        # 生成DNA
        dna = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d-%H:%M')}-PRICING-{asset_id}"

        result = PricingResult(
            asset_id=asset_id,
            current_price=round(final_price, 2),
            base_price=self.base_price,
            quality_factor=round(quality_factor, 3),
            market_factor=round(market_factor, 3),
            rarity_coefficient=round(rarity_coefficient, 3),
            time_decay_factor=round(time_decay, 3),
            price_breakdown={
                "base_price": self.base_price,
                "quality_impact": self.base_price * quality_factor,
                "market_impact": self.base_price * quality_factor * market_factor,
                "rarity_impact": self.base_price * quality_factor * market_factor * rarity_coefficient,
                "final_price": final_price,
            },
            effective_date=datetime.now().isoformat(),
            dna=dna,
        )

        self.pricing_history.append(result)
        return result

    def export_pricing_report(self, result: PricingResult) -> str:
        """导出定价报告"""
        report = f"# 💰 DNA记忆资产定价报告\n\n"
        report += f"**资产ID**: {result.asset_id}\n"
        report += f"**当前价格**: {result.current_price} e-CNY\n"
        report += f"**有效时间**: {result.effective_date}\n\n"

        report += f"## 定价因子\n\n"
        report += f"| 因子 | 值 | 含义 |\n"
        report += f"|------|-----|---------|\n"
        report += f"| BasePrice | {result.base_price} | 基础价格 |\n"
        report += f"| QualityFactor | {result.quality_factor} | 质量评分影响 |\n"
        report += f"| MarketFactor | {result.market_factor} | 市场情绪影响 |\n"
        report += f"| RarityCoeff | {result.rarity_coefficient} | 稀缺性影响 |\n"
        report += f"| TimeDecay | {result.time_decay_factor} | 时间衰减 |\n\n"

        report += f"## 价格分解\n\n"
        for key, value in result.price_breakdown.items():
            report += f"- **{key}**: {value:.2f} e-CNY\n"

        report += f"\n**DNA**: {result.dna}\n"

        return report


# ════════════════════════════════════════════════════════
# 测试与演示
# ════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("💰 龍魂 Web3-DNA DNA记忆资产化系统 v1.0")
    print(f"   DNA: #龍芯⚡️2026-05-25-WEB3-DNA-MEMORY-ASSET-v1.0")
    print("=" * 60 + "\n")

    engine = DNAMemoryAssetPricingEngine()

    # 测试用例
    test_cases = [
        ("user-001", "我在2026年成功实现龍魂系统与Web3-DNA的融合", "professional", {"keywords": ["龍魂", "Web3", "融合"]}),
        ("user-002", "一次失败的创业历程与其中学到的经验", "personal", {"keywords": ["失败", "学习", "成长"]}),
        ("user-003", "关于中华文化与AI伦理的深度思考", "scientific", {"keywords": ["文化", "伦理", "AI"]}),
    ]

    print("📍 测试1: 创建DNA记忆资产\n")
    for owner_id, content, category, metadata in test_cases:
        asset = engine.create_dna_memory_asset(owner_id, content, category, metadata)
        print(f"资产ID: {asset.asset_id}")
        print(f"所有者: {asset.owner_id}")
        print(f"质量分数: {asset.memory_quality_score}/100")
        print(f"DNA: {asset.dna}\n")

    print("📍 测试2: 计算DNA记忆资产价格\n")
    for asset_id in engine.asset_registry.keys():
        pricing = engine.calculate_price(asset_id)
        print(f"资产: {asset_id}")
        print(f"当前价格: {pricing.current_price} e-CNY")
        print(f"质量因子: {pricing.quality_factor}")
        print(f"市场因子: {pricing.market_factor}")
        print(f"稀缺性: {pricing.rarity_coefficient}")
        print(f"时间衰减: {pricing.time_decay_factor}\n")

    print("=" * 60)
    print("✅ DNA记忆资产化系统初始化完成")
    print("=" * 60 + "\n")
    print("🐉 龍魂 Web3-DNA · DNA资产化 · UID9622不免责")
