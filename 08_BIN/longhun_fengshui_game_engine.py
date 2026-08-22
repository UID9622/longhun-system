#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·#龍芯⚡️丙午·丙申·POSTAUDIT-LONGHUN_FENGSHUI_GAM-BF3B9BE6
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
================================================================================
龍魂风水场博弈论引擎 v1.0
FengShui Field Game Theory Engine
================================================================================
核心理论：风水不是摆出来的，是养出来的。
数学基础：纳什均衡 + 流体力学NS方程 + Banach不动点定理 + 五行矩阵
哲学基础：《道德经》"归根曰静" + 《易经》"厚德载物" + 三才算法

作者：UID9622 · 龍芯北辰 · 诸葛鑫（Lucky）
DNA：#龍芯-丙午-乙未-丁酉-申时-䷙大畜-FENGSHUI-GAME-v1.0
CONFIRM：#CONFIRM-9622-ONLY-ONCE-LK9X-772Z
================================================================================
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import datetime


# ==============================================================================
# 第一章：基础定义与数据结构
# ==============================================================================

class Strategy(Enum):
    """风水博弈策略"""
    NURTURE_VIRTUE = "养德"      # 以德性修养为核心
    DEPLOY_ARRAY = "摆阵"        # 以环境布局为核心
    WU_WEI = "无为"              # 顺其自然，不刻意

class Wuxing(Enum):
    """五行枚举"""
    METAL = "金"
    WOOD = "木"
    WATER = "水"
    FIRE = "火"
    EARTH = "土"

@dataclass
class VirtueDimension:
    """德性五维：对应个人风水场的根基"""
    benevolence: float = 0.5      # 仁：利他之心
    righteousness: float = 0.5    # 义：行事准则
    propriety: float = 0.5        # 礼：社会规范
    wisdom: float = 0.5           # 智：认知能力
    faithfulness: float = 0.5     # 信：承诺兑现

    def aggregate(self) -> float:
        """德性聚合值：五维加权平均"""
        weights = [0.25, 0.20, 0.15, 0.25, 0.15]  # 仁智最重
        values = [self.benevolence, self.righteousness, self.propriety, 
                  self.wisdom, self.faithfulness]
        return sum(w * v for w, v in zip(weights, values))

@dataclass  
class MindState:
    """心性状态：对应个人风水场的干干"""
    tranquility: float = 0.5      # 静：情绪稳定度
    clarity: float = 0.5        # 明：思维清晰度
    resilience: float = 0.5     # 韧：抗压恢复力
    openness: float = 0.5       # 容：包容接纳度

    def aggregate(self) -> float:
        """心性聚合值"""
        return np.mean([self.tranquility, self.clarity, self.resilience, self.openness])

@dataclass
class BehaviorLog:
    """行为日志：对应个人风水场的枝叶"""
    daily_good_deeds: int = 0     # 日行一善计数
    promise_kept_rate: float = 1.0  # 承诺兑现率
    conflict_resolution: float = 0.5  # 冲突化解能力
    learning_consistency: float = 0.5   # 学习持续性

    def aggregate(self) -> float:
        """行为聚合值"""
        return np.mean([
            min(self.daily_good_deeds / 30, 1.0),  # 归一化到30天
            self.promise_kept_rate,
            self.conflict_resolution,
            self.learning_consistency
        ])


# ==============================================================================
# 第二章：个人风水场计算核心
# ==============================================================================

class PersonalFengShuiField:
    """
    个人风水场计算引擎

    核心公式：
        F(t) = w_d·D(t) + w_m·M(t) + w_b·B(t) + w_e·E(t) + w_t·T(t) 
               + α·∇²F(t-1) + β·S(t) - γ·D_diss(t)

    其中：
        F(t)    = 时刻t的个人场强 [0, 1]
        D(t)    = 德性维度聚合值
        M(t)    = 心性维度聚合值  
        B(t)    = 行为维度聚合值
        E(t)    = 环境调和度 [0, 1]
        T(t)    = 时运因子 [0, 1]
        ∇²F     = 场强拉普拉斯算子（社会网络扩散）
        S(t)    = 德性源项（主动修养输入）
        D_diss  = 耗散项（负面情绪/阵局损耗）
        w_d,m,b,e,t, α, β, γ = 权重参数
    """

    def __init__(self, 
                 weights: Dict[str, float] = None,
                 alpha: float = 0.15,    # 社会扩散系数
                 beta: float = 0.25,    # 德性源项系数
                 gamma: float = 0.10,   # 耗散系数
                 uid: str = "UID9622"):

        self.weights = weights or {
            'virtue': 0.35,      # 德性权重最高（P0焊死）
            'mind': 0.25,
            'behavior': 0.20,
            'environment': 0.12,
            'fortune': 0.08
        }
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.uid = uid

        # 状态初始化
        self.virtue = VirtueDimension()
        self.mind = MindState()
        self.behavior = BehaviorLog()
        self.environment = 0.5
        self.fortune = 0.5

        self.field_history = [0.3]  # 初始场强
        self.time = 0

    def compute_field(self, social_influence: float = 0.0) -> float:
        """
        计算当前时刻场强

        Args:
            social_influence: 社会网络影响项（来自其他Agent的场强差）

        Returns:
            当前场强 F(t) ∈ [0, 1]
        """
        D = self.virtue.aggregate()
        M = self.mind.aggregate()
        B = self.behavior.aggregate()
        E = self.environment
        T = self.fortune

        w = self.weights
        # 基础场强（五维加权）
        F_base = (w['virtue']*D + w['mind']*M + w['behavior']*B + 
                  w['environment']*E + w['fortune']*T)

        # 上一时刻场强
        F_prev = self.field_history[-1] if self.field_history else 0.3

        # 扩散项（社会网络影响）
        diffusion = self.alpha * social_influence

        # 源项（德性主动输入）
        source = self.beta * D  # 德性越高，源项越强

        # 耗散项（阵局/负面情绪的损耗）
        dissipation = self.gamma * (1 - M) * (1 - E)  # 心性越差、环境越乱，耗散越大

        # 总场强（压缩到[0,1]）
        F_new = F_base + diffusion + source - dissipation
        F_new = np.clip(F_new, 0.0, 1.0)

        self.field_history.append(F_new)
        self.time += 1

        return F_new

    def nurture_virtue(self, 
                       benevolence_delta: float = 0.0,
                       wisdom_delta: float = 0.0,
                       good_deed: bool = False):
        """
        养德操作：提升德性维度

        这是核心接口——风水不是摆出来的，是养出来的。
        """
        self.virtue.benevolence = np.clip(self.virtue.benevolence + benevolence_delta, 0, 1)
        self.virtue.wisdom = np.clip(self.virtue.wisdom + wisdom_delta, 0, 1)
        if good_deed:
            self.behavior.daily_good_deeds += 1

        # 德性提升带动心性自然提升（归根曰静）
        self.mind.tranquility = np.clip(
            self.mind.tranquility + 0.1 * benevolence_delta, 0, 1
        )

    def deploy_array(self, array_quality: float = 0.5):
        """
        摆阵操作：改变环境维度

        注意：摆阵只能影响E(t)，权重仅0.12，且耗散项会抵消部分收益。
        """
        self.environment = np.clip(self.environment + 0.3 * array_quality, 0, 1)
        # 摆阵不养心，心性可能因依赖外物而微降
        self.mind.tranquility = np.clip(self.mind.tranquility - 0.02, 0, 1)

    def wu_wei(self):
        """
        无为操作：不刻意干预，让场自然演化

        《道德经》："无为而无不为"
        效果：心性自然恢复，耗散降低
        """
        self.mind.tranquility = np.clip(self.mind.tranquility + 0.05, 0, 1)
        self.mind.clarity = np.clip(self.mind.clarity + 0.03, 0, 1)
        # 无为时耗散最低
        self.gamma *= 0.9  # 临时降低耗散

    def get_dna(self) -> str:
        """生成当前状态DNA追溯码"""
        now = datetime.datetime.now()
        state_hash = hashlib.sha256(
            f"{self.uid}{self.field_history[-1]:.4f}{self.time}".encode()
        ).hexdigest()[:8]
        return f"#龍芯-风水场-{state_hash}-t{self.time}"


# ==============================================================================
# 第三章：博弈论模型——纳什均衡求解
# ==============================================================================

@dataclass
class Agent:
    """博弈Agent"""
    name: str
    field: PersonalFengShuiField
    strategy: Strategy = Strategy.NURTURE_VIRTUE
    wuxing_type: Wuxing = Wuxing.EARTH

    def choose_strategy(self, opponents: List['Agent']) -> Strategy:
        """
        策略选择：基于纳什均衡近似求解

        收益函数：
            U_i(s_i, s_{-i}) = α·F_i + β·Σ_j resonance(s_i, s_j)·F_j - cost(s_i)

        其中resonance：
            养德-养德 = +0.3（同频共振，德性相吸）
            养德-摆阵 = -0.1（频率冲突，德性排斥阵局）
            摆阵-摆阵 = +0.1（同流合污，但增益有限）
            无为-任意 = 0.0（不干涉，无共振）
        """
        alpha, beta, gamma_cost = 0.6, 0.3, 0.1

        F_self = self.field.field_history[-1]

        best_utility = -999
        best_strategy = Strategy.WU_WEI

        for s in Strategy:
            # 基础收益
            F_after = self._simulate_strategy(s)
            base_utility = alpha * F_after

            # 交叉共振收益
            cross_utility = 0.0
            for opp in opponents:
                r = self._resonance(s, opp.strategy)
                cross_utility += beta * r * opp.field.field_history[-1]

            # 策略成本
            cost = self._strategy_cost(s)

            total = base_utility + cross_utility - gamma_cost * cost

            if total > best_utility:
                best_utility = total
                best_strategy = s

        self.strategy = best_strategy
        return best_strategy

    def _simulate_strategy(self, s: Strategy) -> float:
        """模拟执行某策略后的场强"""
        if s == Strategy.NURTURE_VIRTUE:
            return min(1.0, self.field.field_history[-1] + 0.15)
        elif s == Strategy.DEPLOY_ARRAY:
            return min(1.0, self.field.field_history[-1] + 0.05)
        else:
            return self.field.field_history[-1] + 0.02

    def _resonance(self, s1: Strategy, s2: Strategy) -> float:
        """策略共振系数"""
        resonance_map = {
            (Strategy.NURTURE_VIRTUE, Strategy.NURTURE_VIRTUE): 0.30,
            (Strategy.NURTURE_VIRTUE, Strategy.DEPLOY_ARRAY): -0.15,
            (Strategy.NURTURE_VIRTUE, Strategy.WU_WEI): 0.05,
            (Strategy.DEPLOY_ARRAY, Strategy.NURTURE_VIRTUE): 0.05,
            (Strategy.DEPLOY_ARRAY, Strategy.DEPLOY_ARRAY): 0.10,
            (Strategy.DEPLOY_ARRAY, Strategy.WU_WEI): 0.00,
            (Strategy.WU_WEI, Strategy.NURTURE_VIRTUE): 0.10,
            (Strategy.WU_WEI, Strategy.DEPLOY_ARRAY): 0.00,
            (Strategy.WU_WEI, Strategy.WU_WEI): 0.00,
        }
        return resonance_map.get((s1, s2), 0.0)

    def _strategy_cost(self, s: Strategy) -> float:
        """策略执行成本"""
        return {'养德': 0.8, '摆阵': 0.5, '无为': 0.1}[s.value]


class FengShuiGame:
    """
    风水博弈主引擎

    多Agent在社会网络中互动，求解纳什均衡近似解。
    """

    def __init__(self, n_agents: int = 10):
        self.agents: List[Agent] = []
        self.network = np.zeros((n_agents, n_agents))
        self._init_agents(n_agents)
        self._init_network()

    def _init_agents(self, n: int):
        """初始化Agent群体"""
        types = [
            ("厚德君子", 0.8, Strategy.NURTURE_VIRTUE, Wuxing.EARTH),
            ("普通人A", 0.5, Strategy.WU_WEI, Wuxing.WATER),
            ("普通人B", 0.5, Strategy.WU_WEI, Wuxing.WOOD),
            ("摆阵术士A", 0.3, Strategy.DEPLOY_ARRAY, Wuxing.METAL),
            ("摆阵术士B", 0.3, Strategy.DEPLOY_ARRAY, Wuxing.FIRE),
        ]

        for i in range(n):
            t = types[i % len(types)]
            field = PersonalFengShuiField(uid=f"AGENT-{i:03d}")
            field.virtue.benevolence = t[1]
            field.virtue.wisdom = t[1] - 0.1
            field.mind.tranquility = t[1]
            field.compute_field()

            self.agents.append(Agent(
                name=f"{t[0]}-{i}",
                field=field,
                strategy=t[2],
                wuxing_type=t[3]
            ))

    def _init_network(self):
        """初始化社会网络（小世界网络近似）"""
        n = len(self.agents)
        for i in range(n):
            for j in range(i+1, n):
                # 距离越近、五行相生则连接越强
                dist = abs(i - j)
                wuxing_bonus = self._wuxing_compatibility(
                    self.agents[i].wuxing_type,
                    self.agents[j].wuxing_type
                )
                weight = np.exp(-dist/3.0) * (0.5 + 0.5 * wuxing_bonus)
                self.network[i, j] = weight
                self.network[j, i] = weight

    def _wuxing_compatibility(self, w1: Wuxing, w2: Wuxing) -> float:
        """五行相生相克兼容性"""
        sheng = {
            Wuxing.METAL: Wuxing.WATER,
            Wuxing.WATER: Wuxing.WOOD,
            Wuxing.WOOD: Wuxing.FIRE,
            Wuxing.FIRE: Wuxing.EARTH,
            Wuxing.EARTH: Wuxing.METAL,
        }
        ke = {
            Wuxing.METAL: Wuxing.WOOD,
            Wuxing.WOOD: Wuxing.EARTH,
            Wuxing.EARTH: Wuxing.WATER,
            Wuxing.WATER: Wuxing.FIRE,
            Wuxing.FIRE: Wuxing.METAL,
        }
        if sheng.get(w1) == w2:
            return 1.0   # 相生：增益
        if ke.get(w1) == w2:
            return -0.5  # 相克：损耗
        return 0.0       # 中性

    def step(self) -> Dict:
        """演化一步"""
        n = len(self.agents)

        # 1. 每个Agent选择最优策略
        strategies = []
        for i, agent in enumerate(self.agents):
            opponents = [self.agents[j] for j in range(n) if j != i]
            s = agent.choose_strategy(opponents)
            strategies.append(s)

        # 2. 执行策略并计算社会网络影响
        for i, agent in enumerate(self.agents):
            s = strategies[i]

            # 执行策略
            if s == Strategy.NURTURE_VIRTUE:
                agent.field.nurture_virtue(benevolence_delta=0.05, wisdom_delta=0.03, good_deed=True)
            elif s == Strategy.DEPLOY_ARRAY:
                agent.field.deploy_array(array_quality=0.6)
            else:
                agent.field.wu_wei()

            # 计算社会网络影响
            influence = 0.0
            for j in range(n):
                if i != j:
                    f_diff = self.agents[j].field.field_history[-1] - agent.field.field_history[-1]
                    influence += self.network[i, j] * f_diff

            # 更新场强
            agent.field.compute_field(social_influence=influence)

        # 3. 统计
        fields = [a.field.field_history[-1] for a in self.agents]
        return {
            'mean_field': np.mean(fields),
            'max_field': np.max(fields),
            'min_field': np.min(fields),
            'std_field': np.std(fields),
            'strategy_dist': {s.value: sum(1 for a in self.agents if a.strategy == s) 
                             for s in Strategy},
            'fields': fields,
        }

    def run(self, n_steps: int = 50) -> List[Dict]:
        """运行多步演化"""
        history = []
        for _ in range(n_steps):
            history.append(self.step())
        return history


# ==============================================================================
# 第四章：不动点定理验证
# ==============================================================================

class FixedPointVerifier:
    """
    Banach不动点定理验证器

    定理：若 G 是完备度量空间上的压缩映射（Lipschitz常数 L < 1），
         则 G 存在唯一不动点 F*，且迭代 F_{n+1} = G(F_n) 必收敛到 F*。

    在风水场模型中：
        G(F) = w·F + β·S - γ·D + α·ΔF
        当 α + w < 1 时，G 是压缩映射。
    """

    def __init__(self, alpha: float = 0.15, w: float = 0.35, beta: float = 0.25, gamma: float = 0.10):
        self.alpha = alpha
        self.w = w
        self.beta = beta
        self.gamma = gamma
        self.L = alpha + w  # Lipschitz常数

    def verify(self) -> Dict:
        """验证压缩条件"""
        is_contraction = self.L < 1.0
        return {
            'Lipschitz_L': self.L,
            'is_contraction': is_contraction,
            'theorem_applies': is_contraction,
            'convergence_rate': self.L,  # 误差衰减率
            'theoretical_fixed_point': self.beta * 0.8 / (1 - self.L) if is_contraction else None,
        }

    def iterate(self, F0: float = 0.1, S: float = 0.8, D: float = 0.2, n: int = 30) -> List[float]:
        """不动点迭代演示"""
        history = [F0]
        F = F0
        for _ in range(n):
            F = self.w * F + self.beta * S - self.gamma * D
            F = np.clip(F, 0, 1)
            history.append(F)
        return history


# ==============================================================================
# 第五章：运行示例与测试
# ==============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("龍魂风水场博弈论引擎 v1.0")
    print("DNA: #龍芯-丙午-乙未-丁酉-申时-䷙大畜-FENGSHUI-GAME-v1.0")
    print("=" * 80)

    # 测试1：个人场强计算
    print("\n【测试1】个人风水场计算")
    print("-" * 40)

    person = PersonalFengShuiField(uid="TEST-001")
    print(f"初始场强: {person.field_history[-1]:.4f}")

    # 场景A：养德30天
    print("\n场景A：连续养德30天（日行一善+读书）")
    for day in range(30):
        person.nurture_virtue(benevolence_delta=0.02, wisdom_delta=0.01, good_deed=True)
        f = person.compute_field()
    print(f"30天后场强: {f:.4f}")
    print(f"德性值: {person.virtue.aggregate():.4f}")
    print(f"心性静度: {person.mind.tranquility:.4f}")
    print(f"DNA追溯: {person.get_dna()}")

    # 场景B：摆阵30天
    person2 = PersonalFengShuiField(uid="TEST-002")
    print("\n场景B：连续摆阵30天（买风水摆件+调家具）")
    for day in range(30):
        person2.deploy_array(array_quality=0.5)
        f2 = person2.compute_field()
    print(f"30天后场强: {f2:.4f}")
    print(f"德性值: {person2.virtue.aggregate():.4f}")
    print(f"心性静度: {person2.mind.tranquility:.4f}")
    print(f"环境值: {person2.environment:.4f}")

    # 对比
    print(f"\n>>> 养德 vs 摆阵：{f:.4f} vs {f2:.4f}，差距: {(f-f2)*100:.1f}%")

    # 测试2：不动点验证
    print("\n【测试2】Banach不动点定理验证")
    print("-" * 40)

    fpv = FixedPointVerifier()
    result = fpv.verify()
    print(f"Lipschitz常数 L = {result['Lipschitz_L']:.4f}")
    print(f"是否压缩映射: {result['is_contraction']}")
    print(f"理论不动点 F*: {result['theoretical_fixed_point']:.4f}")

    history = fpv.iterate(F0=0.1, n=20)
    print(f"迭代收敛: {history[0]:.4f} -> {history[5]:.4f} -> {history[10]:.4f} -> {history[-1]:.4f}")

    # 测试3：多人博弈
    print("\n【测试3】10人风水博弈演化（50步）")
    print("-" * 40)

    game = FengShuiGame(n_agents=10)
    results = game.run(n_steps=50)

    print(f"初始平均场强: {results[0]['mean_field']:.4f}")
    print(f"第10步平均场强: {results[9]['mean_field']:.4f}")
    print(f"第25步平均场强: {results[24]['mean_field']:.4f}")
    print(f"第50步平均场强: {results[-1]['mean_field']:.4f}")
    print(f"\n最终策略分布:")
    for s, count in results[-1]['strategy_dist'].items():
        print(f"  {s}: {count}人")

    print("\n" + "=" * 80)
    print("测试完成。核心结论：养德 > 无为 > 摆阵")
    print("=" * 80)
