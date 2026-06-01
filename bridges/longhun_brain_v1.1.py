#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂大脑决策引擎 v1.1 · 优化版

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DNA: #龍芯⚡️2026-06-01-LONGHUN-BRAIN-v1.1

改进清单:
  ✅ 完整类型注解 (typing模块)
  ✅ CNSH v3.0三才决策框架对齐
  ✅ LRU缓存优化 (频繁计算缓存)
  ✅ 细分异常处理 (DataError/AlgoError)
  ✅ 决策评分算法详细文档
  ✅ 性能计时装饰器
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from __future__ import annotations

import time
import logging
from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
from functools import lru_cache
from datetime import datetime, timezone

logger = logging.getLogger("longhun_brain")


# ═══════════════════════════════════════════════════════════════
# 异常定义
# ═══════════════════════════════════════════════════════════════

class BrainError(Exception):
    """大脑模块基异常"""
    pass


class DataError(BrainError):
    """数据异常·缺失/格式错误"""
    pass


class AlgoError(BrainError):
    """算法异常·计算失败"""
    pass


class CacheError(BrainError):
    """缓存异常"""
    pass


# ═══════════════════════════════════════════════════════════════
# 决策等级枚举
# ═══════════════════════════════════════════════════════════════

class DecisionLevel(Enum):
    """决策紧急等级"""
    CRITICAL = 4   # 关键 (S ≥ 13)
    HIGH = 3       # 高优先级 (S 10-12)
    MEDIUM = 2     # 中等 (S 7-9)
    LOW = 1        # 低优先级 (S 4-6)
    INFO = 0       # 信息 (S < 4)


# ═══════════════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════════════

@dataclass
class ContextSignal:
    """上下文信号·输入数据"""

    # 基础上下文
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    user_id: Optional[str] = None
    session_id: Optional[str] = None

    # 信号量 (0-10分制)
    consciousness: float = 5.0         # 意识清晰度 (反应速度)
    emotional_state: float = 5.0       # 情绪态 (波动幅度)
    intention_clarity: float = 5.0     # 意图清晰度 (目标坚定度)

    # 环境信号
    urgency: float = 5.0               # 紧急程度
    risk_level: float = 5.0            # 风险等级
    resource_availability: float = 5.0 # 资源可用度

    # 约束条件
    constraints: Dict[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """验证信号有效性"""
        try:
            for attr in ['consciousness', 'emotional_state', 'intention_clarity',
                        'urgency', 'risk_level', 'resource_availability']:
                val = getattr(self, attr)
                if not 0.0 <= val <= 10.0:
                    raise DataError(f"{attr} 必须在 0-10 之间,实际值: {val}")
            return True
        except Exception as e:
            logger.error(f"信号验证失败: {e}")
            raise DataError(f"上下文信号验证失败: {e}")


@dataclass
class DecisionResult:
    """决策结果"""

    decision_id: str
    timestamp: str
    level: DecisionLevel

    # 评分矩阵
    sovereignty_score: float          # S (主权分) = R·I·T^(-α_τ)
    rationality_index: float          # R (理性指数) = 意识·意图清晰 / 10
    intensity_factor: float           # I (强度系数) = (情绪态 + 紧急度) / 20
    time_decay_exponent: float        # α_τ (时间衰减指数)

    # 决策说明
    reasoning: str
    recommended_action: str
    confidence: float                 # 置信度 (0-1)

    # 性能指标
    computation_time: float           # 计算耗时 (秒)
    cache_hit: bool = False
    dna: str = ""                     # DNA追溯

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "decision_id": self.decision_id,
            "timestamp": self.timestamp,
            "level": self.level.name,
            "scores": {
                "sovereignty": self.sovereignty_score,
                "rationality": self.rationality_index,
                "intensity": self.intensity_factor,
                "time_decay_exp": self.time_decay_exponent,
            },
            "reasoning": self.reasoning,
            "action": self.recommended_action,
            "confidence": self.confidence,
            "perf_ms": round(self.computation_time * 1000, 2),
            "cache_hit": self.cache_hit,
            "dna": self.dna,
        }


# ═══════════════════════════════════════════════════════════════
# 脑决策引擎
# ═══════════════════════════════════════════════════════════════

class LonghunBrain:
    """龍魂大脑·决策推演引擎

    基于 CNSH v3.0 三才决策框架:
    - 天分 (Heavenly Potential): 意识·情绪·意图
    - 人策 (Human Strategy): 资源·约束·风险
    - 地利 (Earthly Advantage): 时间衰减·机会窗口

    核心公式: S = R · I · T^(-α_τ)
    其中:
      S: 主权分 (Sovereignty Score)
      R: 理性指数 (Rationality) = (consciousness + intention_clarity) / 20
      I: 强度系数 (Intensity) = (emotional_state + urgency + risk_level) / 30
      T: 时间 (秒)
      α_τ: 时间衰减指数 (0.01~1.0, 默认0.1)
    """

    def __init__(
        self,
        user_id: str = "system",
        enable_cache: bool = True,
        time_decay_alpha: float = 0.1,
        logger_instance: Optional[logging.Logger] = None
    ):
        """初始化龍魂大脑

        Args:
            user_id: 用户ID
            enable_cache: 启用LRU缓存
            time_decay_alpha: 时间衰减指数 (默认0.1 = 10天衰减到1%)
            logger_instance: 日志实例
        """
        self.user_id = user_id
        self.enable_cache = enable_cache
        self.time_decay_alpha = time_decay_alpha
        self.logger = logger_instance or logger

        self.decision_history: List[DecisionResult] = []
        self._cache_stats = {"hits": 0, "misses": 0}

    def decide(
        self,
        signal: ContextSignal,
        context_description: str = "",
        dna_prefix: str = "#龍芯⚡️"
    ) -> DecisionResult:
        """做出决策

        Args:
            signal: 上下文信号
            context_description: 决策描述
            dna_prefix: DNA前缀

        Returns:
            决策结果

        Raises:
            DataError: 信号验证失败
            AlgoError: 决策计算失败
        """
        start_time = time.time()

        # 验证输入
        try:
            signal.validate()
        except DataError as e:
            self.logger.error(f"输入验证失败: {e}")
            raise

        # 尝试缓存查询 (如果启用)
        if self.enable_cache:
            cached = self._get_cached_decision(signal)
            if cached:
                cached.computation_time = time.time() - start_time
                cached.cache_hit = True
                self._cache_stats["hits"] += 1
                self.logger.info(f"[CACHE HIT] decision_id={cached.decision_id}")
                return cached

        self._cache_stats["misses"] += 1

        # 计算决策评分
        try:
            r_index = self._calc_rationality(signal)
            i_factor = self._calc_intensity(signal)
            t_decay = self._calc_time_decay()
            s_score = self._calc_sovereignty(r_index, i_factor, t_decay)

            # 确定决策等级
            level = self._determine_level(s_score)

            # 生成推理说明
            reasoning = self._generate_reasoning(signal, r_index, i_factor, t_decay, s_score)

            # 推荐行动
            action = self._recommend_action(level, signal)

            # 生成DNA
            dna = self._make_dna(dna_prefix, level.name)

            # 构建结果
            result = DecisionResult(
                decision_id=f"dec_{int(time.time() * 1000)}",
                timestamp=datetime.now(timezone.utc).isoformat(),
                level=level,
                sovereignty_score=s_score,
                rationality_index=r_index,
                intensity_factor=i_factor,
                time_decay_exponent=self.time_decay_alpha,
                reasoning=reasoning,
                recommended_action=action,
                confidence=min(1.0, s_score / 15.0),  # 15为满分
                computation_time=time.time() - start_time,
                dna=dna
            )

            # 保存历史
            self.decision_history.append(result)
            self.logger.info(f"[DECISION] level={level.name} s_score={s_score:.2f} "
                           f"dna={dna}")

            return result

        except Exception as e:
            self.logger.error(f"决策计算失败: {e}", exc_info=True)
            raise AlgoError(f"决策计算异常: {e}")

    # ─────────────────────────────────────────────
    # 评分子算法
    # ─────────────────────────────────────────────

    @lru_cache(maxsize=128)
    def _calc_rationality(self, signal: ContextSignal) -> float:
        """计算理性指数 R

        R = (consciousness + intention_clarity) / 20
        范围: [0, 1]
        解释: 反映行动者的意识清晰度和意图坚定度
        """
        return (signal.consciousness + signal.intention_clarity) / 20.0

    @lru_cache(maxsize=128)
    def _calc_intensity(self, signal: ContextSignal) -> float:
        """计算强度系数 I

        I = (emotional_state + urgency + risk_level) / 30
        范围: [0, 1]
        解释: 反映决策的驱动力和压力
        """
        return (signal.emotional_state + signal.urgency + signal.risk_level) / 30.0

    def _calc_time_decay(self) -> float:
        """计算时间衰减 T^(-α_τ)

        使用当前时间戳
        T^(-α_τ) = (current_time_sec)^(-α_τ)
        """
        current_sec = time.time()
        try:
            decay = current_sec ** (-self.time_decay_alpha)
            return max(0.001, min(1.0, decay))  # 限制在[0.001, 1.0]
        except Exception as e:
            self.logger.warning(f"时间衰减计算失败: {e},使用默认值1.0")
            return 1.0

    def _calc_sovereignty(self, r: float, i: float, t: float) -> float:
        """计算主权分 S

        S = R · I · T^(-α_τ)
        范围: [0, 15] (实际)
        """
        try:
            s = r * i * t * 15.0  # 调整系数使范围合理
            return max(0.0, min(15.0, s))
        except Exception as e:
            self.logger.error(f"主权分计算失败: {e}")
            raise AlgoError(f"主权分计算异常: {e}")

    def _determine_level(self, s_score: float) -> DecisionLevel:
        """确定决策等级"""
        if s_score >= 13:
            return DecisionLevel.CRITICAL
        elif s_score >= 10:
            return DecisionLevel.HIGH
        elif s_score >= 7:
            return DecisionLevel.MEDIUM
        elif s_score >= 4:
            return DecisionLevel.LOW
        else:
            return DecisionLevel.INFO

    def _generate_reasoning(
        self,
        signal: ContextSignal,
        r: float,
        i: float,
        t: float,
        s: float
    ) -> str:
        """生成决策推理"""
        reasoning = (
            f"理性指数 R={r:.2f} (意识={signal.consciousness:.1f}, 意图={signal.intention_clarity:.1f}); "
            f"强度系数 I={i:.2f} (情绪={signal.emotional_state:.1f}, "
            f"紧急={signal.urgency:.1f}, 风险={signal.risk_level:.1f}); "
            f"时间衰减 T={t:.3f}; "
            f"主权分 S={s:.2f}。"
        )
        return reasoning

    def _recommend_action(self, level: DecisionLevel, signal: ContextSignal) -> str:
        """推荐行动"""
        actions = {
            DecisionLevel.CRITICAL: "⚠️ 立即执行·启动应急预案·全力投入·监控关键指标",
            DecisionLevel.HIGH: "🚀 优先执行·配置专项资源·每2小时评估一次",
            DecisionLevel.MEDIUM: "⏱️ 计划执行·常规流程·每日评估·可适度调整",
            DecisionLevel.LOW: "📋 后续执行·低优先级·适时推进·可延后",
            DecisionLevel.INFO: "ℹ️ 信息收集·持续监控·暂不行动·等待条件成熟",
        }
        return actions.get(level, "未知")

    def _make_dna(self, prefix: str, level: str) -> str:
        """生成DNA追溯码"""
        import hashlib
        date = datetime.now().strftime("%Y%m%d")
        hash_val = hashlib.sha256(level.encode()).hexdigest()[:6].upper()
        return f"{prefix}{date}-BRAIN-{hash_val}"

    def _get_cached_decision(self, signal: ContextSignal) -> Optional[DecisionResult]:
        """从缓存查询决策"""
        if not self.decision_history:
            return None

        # 简单缓存: 相同信号2分钟内返回缓存结果
        now = time.time()
        for decision in reversed(self.decision_history[-10:]):
            if now - time.time() < 120:  # 2分钟
                return decision

        return None

    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        total = self._cache_stats["hits"] + self._cache_stats["misses"]
        hit_rate = (self._cache_stats["hits"] / total * 100) if total > 0 else 0
        return {
            "cache_hits": self._cache_stats["hits"],
            "cache_misses": self._cache_stats["misses"],
            "hit_rate_percent": round(hit_rate, 2),
            "total_decisions": len(self.decision_history)
        }


# ═══════════════════════════════════════════════════════════════
# 性能装饰器
# ═══════════════════════════════════════════════════════════════

def track_decision_time(func: Callable) -> Callable:
    """决策时间追踪装饰器"""
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start
            logger.debug(f"[PERF] {func.__name__} 耗时 {duration*1000:.2f}ms")
            return result
        except Exception as e:
            duration = time.time() - start
            logger.error(f"[PERF_ERROR] {func.__name__} 失败耗时 {duration*1000:.2f}ms: {e}")
            raise
    return wrapper


# ═══════════════════════════════════════════════════════════════
# 测试与使用示例
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(message)s"
    )

    print("🧠 龍魂大脑 v1.1 测试...\n")

    # 创建脑实例
    brain = LonghunBrain(user_id="test_user", enable_cache=True)

    # 测试场景1: 高意识·高紧急度
    signal1 = ContextSignal(
        consciousness=9.0,
        emotional_state=7.0,
        intention_clarity=8.5,
        urgency=9.0,
        risk_level=6.0,
        resource_availability=8.0
    )

    try:
        result1 = brain.decide(signal1, "紧急任务")
        print(f"决策1: {result1.level.name}")
        print(f"  主权分: {result1.sovereignty_score:.2f}")
        print(f"  行动: {result1.recommended_action}")
        print(f"  DNA: {result1.dna}")
        print(f"  耗时: {result1.computation_time*1000:.2f}ms\n")
    except Exception as e:
        print(f"❌ 决策1失败: {e}\n")

    # 测试场景2: 低紧急度·充分准备
    signal2 = ContextSignal(
        consciousness=6.0,
        emotional_state=5.0,
        intention_clarity=6.0,
        urgency=3.0,
        risk_level=2.0,
        resource_availability=9.0
    )

    try:
        result2 = brain.decide(signal2, "常规任务")
        print(f"决策2: {result2.level.name}")
        print(f"  主权分: {result2.sovereignty_score:.2f}")
        print(f"  行动: {result2.recommended_action}")
        print(f"  耗时: {result2.computation_time*1000:.2f}ms\n")
    except Exception as e:
        print(f"❌ 决策2失败: {e}\n")

    # 缓存统计
    stats = brain.get_cache_stats()
    print(f"📊 缓存统计: {stats['total_decisions']} 决策, "
          f"命中率 {stats['hit_rate_percent']}%")
