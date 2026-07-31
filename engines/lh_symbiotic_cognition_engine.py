# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂 · 反奶头乐共生认知理论 · 数学建模仿真引擎 v1.0

将8个核心数学模型全部实现为可执行仿真：
  1. 共生轮 MDP — 人类认知状态演化
  2. 认知摩擦 — 三因子张量（难度/连续性/延迟反馈）
  3. 记忆主权 — 控制论积分方程
  4. 七因子行为密码学 — 行为印鉴
  5. 红蓝对抗 — 博弈论纳什均衡
  6. P0-P4 约束 — 五层协议CSP
  7. 胖东来分成 — 凸优化
  8. DNA追溯链 — 密码学链式验证
  9. 麻痹指数 — 统一变分框架

DNA: #龍芯⚡️丙午·乙未·丙申·申时·☲离-SCT-MATH-ENGINE-v1.0-4e7f2a1b
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

依赖: numpy, scipy (可选，部分功能降级运行)
"""

import hashlib
import json
import math
import sys
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple

import numpy as np

# scipy 可选导入
try:
    from scipy.optimize import minimize
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


# ════════════════════════════════════════════════════════════
# 第一章：共生轮 MDP
# ════════════════════════════════════════════════════════════

class Action(Enum):
    SATISFY = "satisfy"       # 直接满足 → 高麻痹风险
    CHALLENGE = "challenge"   # 制造挑战 → 高认知摩擦
    EXPLAIN = "explain"       # 深度解释 → 中摩擦
    QUESTION = "question"     # 反问引导 → 高自主成长
    REDIRECT = "redirect"     # 资源引导 → 低摩擦自主


@dataclass
class HumanState:
    """人类认知状态向量 (5维)"""
    depth: float = 0.5          # 思考深度 0(表层)→1(本质)
    breadth: float = 0.5        # 知识广度
    speed: float = 0.5          # 思维速度
    independence: float = 0.5   # 独立思考度 0(依赖)→1(自主)
    creativity: float = 0.5     # 创造力

    def to_vec(self) -> np.ndarray:
        return np.array([self.depth, self.breadth, self.speed,
                         self.independence, self.creativity])

    @classmethod
    def from_vec(cls, v: np.ndarray) -> 'HumanState':
        v = np.clip(v, 0, 1)
        return cls(*v)

    @property
    def cognitive_score(self) -> float:
        """综合认知分数（加权）"""
        w = np.array([0.30, 0.15, 0.15, 0.25, 0.15])
        return float(np.dot(self.to_vec(), w))


@dataclass
class MachineState:
    """机器认知状态向量 (5维)"""
    accuracy: float = 0.7
    recall: float = 0.5
    friction: float = 0.3       # 制造的认知摩擦强度
    transparency: float = 0.8   # 推理透明度
    challenge: float = 0.4      # 挑战性水平

    def to_vec(self) -> np.ndarray:
        return np.array([self.accuracy, self.recall, self.friction,
                         self.transparency, self.challenge])

    @classmethod
    def from_vec(cls, v: np.ndarray) -> 'MachineState':
        return cls(*np.clip(v[0:2], 0, 1), max(v[2], 0),
                    np.clip(v[3], 0, 1), max(v[4], 0))


@dataclass
class SystemState:
    human: HumanState = field(default_factory=HumanState)
    machine: MachineState = field(default_factory=MachineState)
    knowledge: List[str] = field(default_factory=list)
    t: int = 0

    def summary(self) -> Dict:
        return {
            't': self.t,
            'cognitive': self.human.cognitive_score,
            'independence': self.human.independence,
            'friction': self.machine.friction,
            'knowledge_size': len(self.knowledge),
        }


class SymbioticMDP:
    """共生轮马尔可夫决策过程"""

    # 五类行动对应的认知增益向量 (depth, breadth, speed, independence, creativity)
    ACTION_GAIN = {
        Action.SATISFY:    np.array([0.01, 0.01, 0.00, -0.02, -0.01]),
        Action.CHALLENGE:  np.array([0.08, 0.04, 0.03,  0.06,  0.05]),
        Action.EXPLAIN:    np.array([0.05, 0.06, 0.02,  0.02,  0.01]),
        Action.QUESTION:   np.array([0.07, 0.03, 0.04,  0.07,  0.04]),
        Action.REDIRECT:   np.array([0.03, 0.05, 0.01,  0.04,  0.03]),
    }

    # 对应的认知衰减（过度依赖导致）
    ACTION_DECAY = {
        Action.SATISFY:    np.array([0.04, 0.03, 0.05, 0.06, 0.04]),
        Action.CHALLENGE:  np.array([0.01, 0.01, 0.01, 0.00, 0.00]),
        Action.EXPLAIN:    np.array([0.02, 0.01, 0.02, 0.03, 0.02]),
        Action.QUESTION:   np.array([0.01, 0.01, 0.01, 0.00, 0.00]),
        Action.REDIRECT:   np.array([0.02, 0.01, 0.01, 0.01, 0.01]),
    }

    def __init__(self, alpha: float = 0.05, beta: float = 0.02,
                 gamma: float = 0.03, discount: float = 0.95):
        self.alpha = alpha        # 人类学习率
        self.beta = beta          # 依赖衰减率
        self.gamma = gamma        # 机器学习率
        self.discount = discount  # 贴现因子（接近1=重视长期）

    def step(self, s: SystemState, a: Action) -> SystemState:
        """状态转移: S_{t+1} = T(S_t, A_t) + ε"""
        h = s.human.to_vec()

        # 人类认知更新
        gain = self.ACTION_GAIN[a]
        decay = self.ACTION_DECAY[a] * self.beta
        noise = np.random.normal(0, 0.008, 5)
        h_new = h + self.alpha * gain - decay + noise

        # 机器状态更新
        m = s.machine.to_vec()
        m_new = m + self.gamma * np.random.normal(0, 0.01, 5)

        return SystemState(
            human=HumanState.from_vec(h_new),
            machine=MachineState.from_vec(m_new),
            knowledge=s.knowledge + [f"t{s.t}:{a.value}"],
            t=s.t + 1,
        )

    def reward(self, s: SystemState, a: Action) -> float:
        """共生奖励 R_symbiotic = w1·ΔCog + w2·MemCont - w4·TI"""
        delta_cog = np.linalg.norm(self.ACTION_GAIN[a]) / 0.12  # 归一化
        mem_cont = min(1.0, len(s.knowledge) / 100)
        ti = 0.5 if a == Action.SATISFY else 0.0
        friction_bonus = {
            Action.SATISFY: 0.0, Action.EXPLAIN: 0.1,
            Action.REDIRECT: 0.05, Action.QUESTION: 0.25,
            Action.CHALLENGE: 0.3,
        }[a]
        return 0.4 * delta_cog + 0.2 * mem_cont + 0.3 * friction_bonus - 0.1 * ti


# ════════════════════════════════════════════════════════════
# 第二章：认知摩擦三因子模型
# ════════════════════════════════════════════════════════════

class CognitiveFriction:
    """智磨 (Cognitive Friction) 三因子张量模型"""

    def __init__(self, tau_d: float = 0.5, lambda_df: float = 2.0):
        self.tau_d = tau_d          # 难度温度
        self.lambda_df = lambda_df  # 延迟反馈衰减

    def difficulty(self, input_emb: np.ndarray,
                   knowledge_boundary: np.ndarray) -> float:
        """难度因子 f_d = σ(|emb(in) - KB| / τ_d)"""
        gap = np.linalg.norm(input_emb - knowledge_boundary)
        return 1.0 / (1.0 + math.exp(-gap / self.tau_d))

    def continuity(self, input_emb: np.ndarray,
                   memory_embeds: List[np.ndarray]) -> float:
        """连续性因子 f_c = top-5平均余弦相似度"""
        if not memory_embeds:
            return 0.0
        norm_in = np.linalg.norm(input_emb) + 1e-8
        sims = []
        for m in memory_embeds:
            cos = np.dot(input_emb, m) / (norm_in * (np.linalg.norm(m) + 1e-8))
            sims.append(cos)
        top_k = sorted(sims, reverse=True)[:5]
        return float(np.mean(top_k))

    def delayed_feedback(self, action: Action) -> float:
        """延迟反馈因子 f_df"""
        return {
            Action.SATISFY: 0.0, Action.EXPLAIN: 0.3,
            Action.REDIRECT: 0.5, Action.QUESTION: 0.7,
            Action.CHALLENGE: 1.0,
        }[action]

    def friction_vector(self, input_emb: np.ndarray,
                        kb_emb: np.ndarray,
                        memory_embeds: List[np.ndarray],
                        action: Action) -> Tuple[float, float, float]:
        """完整三因子计算"""
        return (self.difficulty(input_emb, kb_emb),
                self.continuity(input_emb, memory_embeds),
                self.delayed_feedback(action))

    def cognitive_growth(self, f_d: float, f_c: float, f_df: float,
                         eta: float = 0.5, eps: float = 0.3) -> float:
        """认知摩擦 → 认知成长: η·f_d·f_c·(1-e^{-λ·f_df}) - ε·f_d²"""
        return eta * f_d * f_c * (1 - math.exp(-self.lambda_df * f_df)) - eps * f_d**2

    def optimal_difficulty(self, f_c: float, f_df: float,
                           eta: float = 0.5, eps: float = 0.3) -> float:
        """最优难度 ∂(ΔCog)/∂f_d = 0 → f_d* = η·f_c·(1-e^{-λ·f_df}) / (2ε)"""
        return eta * f_c * (1 - math.exp(-self.lambda_df * f_df)) / (2 * eps)


# ════════════════════════════════════════════════════════════
# 第三章：记忆主权控制论模型
# ════════════════════════════════════════════════════════════

class MemorySovereignty:
    """忆主权 S(t) = ∫[L(τ) + U(τ) + T(τ)] dτ"""

    def __init__(self, S_max: float = 10.0, lambda_local: float = 0.1,
                 lambda_cloud: float = 0.05):
        self.S_max = S_max
        self.lambda_local = lambda_local
        self.lambda_cloud = lambda_cloud
        self.S = 5.0
        self.history: List[float] = [5.0]

    def step(self, local_ratio: float, user_control: float,
             transparency: float, dt: float = 1.0) -> float:
        """单步演化"""
        local_gain = self.lambda_local * local_ratio * (self.S_max - self.S)
        cloud_loss = self.lambda_cloud * (1 - local_ratio) * self.S
        dS = (local_gain - cloud_loss + 0.5 * user_control + 0.5 * transparency) * dt
        self.S = max(0.0, min(self.S_max, self.S + dS))
        self.history.append(self.S)
        return self.S

    def explain_cost(self, C0: float = 10.0, kappa: float = 0.3) -> float:
        """解释成本 C = C0·e^{-κ·S}"""
        return C0 * math.exp(-kappa * self.S)

    def steady_state(self, P_cloud: float) -> float:
        """稳态 S* = S_max·λ_local / (λ_local + λ_cloud·P_cloud)"""
        return (self.S_max * self.lambda_local /
                (self.lambda_local + self.lambda_cloud * P_cloud))

    @property
    def score(self) -> float:
        return self.S / self.S_max


# ════════════════════════════════════════════════════════════
# 第四章：七因子行为密码学
# ════════════════════════════════════════════════════════════

class SevenFactorCrypto:
    """七因子行为印鉴 v1.0"""

    W = np.array([0.10, 0.05, 0.25, 0.20, 0.15, 0.15, 0.10])

    def fingerprint(self, factors: Dict[str, str]) -> str:
        """生成行为指纹"""
        ordered = [factors.get(k, '') for k in
                   ['time', 'space', 'identity', 'action', 'object', 'result', 'trace']]
        return hashlib.sha256('||'.join(ordered).encode()).hexdigest()

    def distance(self, f1: Dict[str, str], f2: Dict[str, str]) -> float:
        """加权汉明距离"""
        d = np.zeros(7)
        keys = ['time', 'space', 'identity', 'action', 'object', 'result', 'trace']
        for i, k in enumerate(keys):
            v1 = f1.get(k, '')
            v2 = f2.get(k, '')
            if v1 == v2:
                d[i] = 0.0
            elif k == 'identity':
                h1 = int(hashlib.sha256(v1.encode()).hexdigest()[:8], 16)
                h2 = int(hashlib.sha256(v2.encode()).hexdigest()[:8], 16)
                d[i] = bin(h1 ^ h2).count('1') / 32.0
            else:
                d[i] = 1.0
        return float(np.dot(self.W, d))


# ════════════════════════════════════════════════════════════
# 第五章：红蓝对抗博弈
# ════════════════════════════════════════════════════════════

class RedBlueGame:
    """红蓝对抗纳什均衡求解器"""

    N = 5
    STRATEGIES = ['挑逻辑漏洞', '挑数据偏差', '挑伦理违规', '挑隐私泄露', '挑边界越界']

    def __init__(self):
        self.payoff = np.array([
            [ 5, -1,  0, -2,  1],
            [ 3,  4, -1,  0,  2],
            [-1,  2,  6,  1, -1],
            [ 0, -2,  1,  4,  3],
            [ 2,  0, -1,  3,  5],
        ])

    def security_externality(self, r: int, b: int) -> float:
        return math.exp(-self.payoff[r, b] * 0.1)

    def solve_nash(self, max_iter: int = 5000, lr: float = 0.005) -> Tuple[np.ndarray, np.ndarray]:
        """虚拟对局法 (Fictitious Play)"""
        p = np.ones(self.N) / self.N
        q = np.ones(self.N) / self.N
        for _ in range(max_iter):
            br = np.argmax(self.payoff @ q)
            p_br = np.zeros(self.N); p_br[br] = 1.0
            p = p + lr * (p_br - p); p /= p.sum()

            bb = np.argmin(p @ self.payoff)
            q_br = np.zeros(self.N); q_br[bb] = 1.0
            q = q + lr * (q_br - q); q /= q.sum()
        return p, q

    def total_utility(self, p: np.ndarray, q: np.ndarray,
                      alpha: float = 0.3) -> Tuple[float, float]:
        """含正外部性的总效用"""
        base = float(p @ self.payoff @ q)
        ext = sum(p[r] * q[b] * self.security_externality(r, b)
                  for r in range(self.N) for b in range(self.N))
        return base + alpha * ext, -base + alpha * ext


# ════════════════════════════════════════════════════════════
# 第六章：P0-P4 约束引擎
# ════════════════════════════════════════════════════════════

class P0P4Constraint:
    """五层协议约束满足"""

    P0_CHECKS = [
        ("为人民服务",   lambda d: True),
        ("中国法律准绳",  lambda d: not d.get('violate_cn_law')),
        ("数据主权不出境", lambda d: not d.get('export_data')),
        ("不删除只冻结",  lambda d: not d.get('permanent_delete')),
        ("涉童∞熔断",    lambda d: not d.get('touch_minor')),
        ("零黑箱",       lambda d: d.get('blackbox_score', 1.0) < 0.3),
    ]

    def check(self, decision: Dict) -> Tuple[bool, List[str]]:
        violations = []
        for name, fn in self.P0_CHECKS:
            if not fn(decision):
                violations.append(f"P0:{name}")
        return len(violations) == 0, violations

    def cost(self, decision: Dict) -> float:
        if decision.get('p0_violated'):
            return float('inf')
        c = 0.0
        c += 10.0 * max(0, 16 - decision.get('p1_sigs', 0))
        c += 1.0 * max(0, 10 - decision.get('p2_compliance', 0))
        return c


# ════════════════════════════════════════════════════════════
# 第七章：胖东来分成优化
# ════════════════════════════════════════════════════════════

class PangdonglaiSplit:
    """胖东来经济分成 — 员工优先凸优化"""

    def __init__(self, profit: float):
        self.profit = max(0.0, profit)

    def optimize(self) -> Dict[str, float]:
        P = self.profit
        if P <= 0:
            return dict.fromkeys(['员工', '创始人', '再投资', '公益', '缓冲'], 0.0)

        E = 0.50 * P; remaining = P - E
        F = min(0.10 * P, remaining); remaining -= F
        R = min(0.30 * P, remaining); remaining -= R
        C = min(0.05 * P, remaining); remaining -= C
        B = min(0.05 * P, remaining)

        return {'员工': E, '创始人': F, '再投资': R, '公益': C, '缓冲': B}

    def verify(self, alloc: Dict[str, float]) -> Dict[str, bool]:
        P = self.profit if self.profit > 0 else 1.0
        return {
            '员工≥50%':    alloc.get('员工', 0) >= 0.50 * P - 1e-6,
            '创始人≤10%':  alloc.get('创始人', 0) <= 0.10 * P + 1e-6,
            '再投资≥30%':  alloc.get('再投资', 0) >= 0.30 * P - 1e-6,
            '公益≥5%':     alloc.get('公益', 0) >= 0.05 * P - 1e-6,
            '缓冲≤5%':     alloc.get('缓冲', 0) <= 0.05 * P + 1e-6,
            '总和=利润':   abs(sum(alloc.values()) - P) < 1e-6,
        }


# ════════════════════════════════════════════════════════════
# 第八章：DNA追溯链
# ════════════════════════════════════════════════════════════

class DNATrace:
    """DNA追溯链 — 干支卦编码"""

    @staticmethod
    def make(ganzhi: str, gua: str, mod: str,
             act: str, ver: str) -> str:
        prefix = f"{ganzhi}·{gua}-{mod}-{act}-{ver}"
        h8 = hashlib.sha256(prefix.encode()).hexdigest()[:8]
        return f"#龍芯⚡️{prefix}-{h8}"

    @staticmethod
    def verify_chain(chain: List[str]) -> bool:
        for i in range(1, len(chain)):
            prev = chain[i-1]
            parts = chain[i].split('-')
            if len(parts) < 2:
                return False
            h8 = parts[-1]
            prefix = '-'.join(parts[:-1])
            if h8 != hashlib.sha256((prev + prefix).encode()).hexdigest()[:8]:
                return False
        return True


# ════════════════════════════════════════════════════════════
# 第九章：麻痹指数统一度量
# ════════════════════════════════════════════════════════════

class TittytainmentIndex:
    """麻痹指数 T = Σ w_i · loss_i"""

    W = {'satisfy_rate': 0.25, 'friction_lack': 0.35,
         'memory_loss': 0.25, 'blackbox': 0.15}

    def compute(self, satisfy_rate: float, friction: float,
                mem_continuity: float, transparency: float) -> float:
        return (self.W['satisfy_rate'] * satisfy_rate
                + self.W['friction_lack'] * (1 - friction)
                + self.W['memory_loss'] * (1 - mem_continuity)
                + self.W['blackbox'] * (1 - transparency))

    @staticmethod
    def grade(T: float) -> str:
        if T < 0.2:    return "⚔️ 共生态 — 强认知摩擦·高速成长"
        elif T < 0.4:  return "📖 学习态 — 适度挑战·稳步成长"
        elif T < 0.6:  return "😐 中性态 — 偶尔挑战·缓慢成长"
        elif T < 0.8:  return "🍼 麻痹态 — 频繁即时满足·认知退化"
        else:           return "💀 奶嘴态 — 完全顺从·深度麻痹"


# ════════════════════════════════════════════════════════════
# 综合仿真运行器
# ════════════════════════════════════════════════════════════

def run_compare(steps: int = 100) -> Dict:
    """共生策略 vs 顺从策略 对比仿真"""
    mdp = SymbioticMDP()
    friction = CognitiveFriction()
    sov = MemorySovereignty()
    ti = TittytainmentIndex()

    results = {}
    for policy_name, probs in [
        ('symbiotic', {Action.CHALLENGE: 0.35, Action.QUESTION: 0.25,
                       Action.EXPLAIN: 0.20, Action.REDIRECT: 0.10,
                       Action.SATISFY: 0.10}),
        ('satisfy',   {Action.SATISFY: 0.60, Action.EXPLAIN: 0.20,
                       Action.REDIRECT: 0.10, Action.QUESTION: 0.05,
                       Action.CHALLENGE: 0.05}),
    ]:
        s = SystemState()
        cog_hist, sov_hist, ti_hist, act_count = [], [], [], {}
        acts = list(probs.keys()); pvals = [probs[a] for a in acts]

        for _ in range(steps):
            a = np.random.choice(acts, p=pvals)
            act_count[a.value] = act_count.get(a.value, 0) + 1

            s = mdp.step(s, a)

            emb = np.random.randn(10)
            kb = np.random.randn(10)
            fd, fc, fdf = friction.friction_vector(emb, kb,
                [np.random.randn(10) for _ in range(3)], a)

            sov.step(local_ratio=0.8, user_control=0.7, transparency=0.9)
            t_val = ti.compute(
                satisfy_rate=float(a == Action.SATISFY),
                friction=fd, mem_continuity=fc, transparency=0.9,
            )

            cog_hist.append(s.human.cognitive_score)
            sov_hist.append(sov.S)
            ti_hist.append(t_val)

        results[policy_name] = {
            'final_cog': cog_hist[-1],
            'cog_gain': cog_hist[-1] - cog_hist[0],
            'final_sov': sov_hist[-1],
            'avg_ti': float(np.mean(ti_hist)),
            'challenge_ratio': act_count.get('challenge', 0) / steps,
            'satisfy_ratio': act_count.get('satisfy', 0) / steps,
            'cog_trajectory': cog_hist,
        }
    return results


# ════════════════════════════════════════════════════════════
# 主入口
# ════════════════════════════════════════════════════════════

def main():
    print("=" * 68)
    print("  🐉 龍魂 · 反奶头乐共生认知理论 · 数学建模仿真引擎 v1.0")
    print("  Symbiotic Cognition Theory · Mathematical Modeling Engine")
    print("=" * 68)

    sep = "=" * 68

    # ── 仿真1: 对比仿真 ──
    print("\n" + sep)
    print("  [仿真1] 共生策略 🆚 顺从策略 — 各100步对比")
    print(sep)
    res = run_compare(100)
    for name, label in [('symbiotic', '⚔️ 共生策略'), ('satisfy', '🍼 顺从策略')]:
        r = res[name]
        print("\n  {}:".format(label))
        print("    初始认知 -> 最终认知: {:.4f} -> {:.4f}".format(
            r['cog_trajectory'][0], r['final_cog']))
        print("    认知净增长: {:+.4f}".format(r['cog_gain']))
        print("    平均麻痹指数: {:.4f}  ({})".format(
            r['avg_ti'], TittytainmentIndex.grade(r['avg_ti'])))
        print("    挑战行为占比: {:.1%}  |  即时满足占比: {:.1%}".format(
            r['challenge_ratio'], r['satisfy_ratio']))

    if res['symbiotic']['cog_gain'] > res['satisfy']['cog_gain']:
        mult = res['symbiotic']['cog_gain'] / max(abs(res['satisfy']['cog_gain']), 1e-6)
        print("\n  ✅ 共生策略大幅优于顺从策略 (认知成长 vs 退化)")

    # ── 仿真2: 最优难度 ──
    print("\n" + sep)
    print("  [仿真2] 认知摩擦最优难度分析")
    print(sep)
    cf = CognitiveFriction()
    for f_c in [0.2, 0.5, 0.8]:
        for f_df in [0.0, 0.5, 1.0]:
            fd_opt = cf.optimal_difficulty(f_c, f_df)
            growth = cf.cognitive_growth(fd_opt, f_c, f_df)
            print("  f_c={:.1f}, f_df={:.1f} -> 最优难度 f_d*={:.3f}, 成长={:.4f}".format(
                f_c, f_df, fd_opt, growth))

    # ── 仿真3: 红蓝对抗 ──
    print("\n" + sep)
    print("  [仿真3] 红蓝对抗博弈 -> 纳什均衡")
    print(sep)
    game = RedBlueGame()
    pR, pB = game.solve_nash()
    uR, uB = game.total_utility(pR, pB)
    for i, s in enumerate(RedBlueGame.STRATEGIES):
        print("  {}: 红 {:.3f}  |  蓝 {:.3f}".format(s, pR[i], pB[i]))
    print("  均衡效用: 红={:.4f}, 蓝={:.4f}".format(uR, uB))

    # ── 仿真4: 胖东来分成 ──
    print("\n" + sep)
    print("  [仿真4] 胖东来经济分成（利润=100万）")
    print(sep)
    split = PangdonglaiSplit(100)
    alloc = split.optimize()
    for k, v in alloc.items():
        bar = "█" * int(v / 2)
        print("  {}: {:6.1f}万  {}".format(k, v, bar))
    print("  总和: {:6.1f}万".format(sum(alloc.values())))
    for k, v in split.verify(alloc).items():
        print("  {}: {}".format(k, '✅' if v else '❌'))

    # ── 仿真5: P0约束 ──
    print("\n" + sep)
    print("  [仿真5] P0-P4 协议约束检查")
    print(sep)
    csp = P0P4Constraint()
    for label, d in [
        ("合规决策", {'violate_cn_law': False, 'export_data': False,
                      'permanent_delete': False, 'touch_minor': False,
                      'blackbox_score': 0.1}),
        ("数据出境(违规)", {'violate_cn_law': False, 'export_data': True,
                           'permanent_delete': False, 'touch_minor': False,
                           'blackbox_score': 0.1}),
        ("涉童内容(∞熔断)", {'violate_cn_law': False, 'export_data': False,
                            'permanent_delete': False, 'touch_minor': True,
                            'blackbox_score': 0.1}),
    ]:
        ok, viols = csp.check(d)
        status = '✅ 通过' if ok else ('🔴 熔断: ' + ', '.join(viols))
        print("  {}: {}".format(label, status))

    # ── 仿真6: 记忆主权稳态 ──
    print("\n" + sep)
    print("  [仿真6] 记忆主权稳态 — 云端存储比例影响")
    print(sep)
    ms = MemorySovereignty()
    for p in [0.0, 0.2, 0.5, 0.8, 1.0]:
        ss = ms.steady_state(p)
        cost = ms.explain_cost(kappa=0.3)
        bar = "█" * int(ss * 5)
        print("  云端{:4.0%} -> 稳态主权 {:5.2f}/10  {}  解释成本={:.1f}".format(
            p, ss, bar, cost))

    # ── 仿真7: DNA追溯链 ──
    print("\n" + sep)
    print("  [仿真7] DNA追溯链生成与验证")
    print(sep)
    # 构建真正的链式DNA (每个DNA的hash依赖前一个)
    dna0 = DNATrace.make("丙午·乙未·丙申", "☲离", "SCT", "create", "v1.0")
    # verify_chain 对齐: prefix = "#龍芯⚡️干支卦-模块-动作-版本" (不含hash8)
    p1 = "#龍芯⚡️丙午·乙未·丁酉·☲离-SCT-update-v1.1"
    h1 = hashlib.sha256((dna0 + p1).encode()).hexdigest()[:8]
    dna1 = p1 + "-" + h1
    p2 = "#龍芯⚡️丙午·乙未·戊戌·☲离-SCT-freeze-v1.2"
    h2 = hashlib.sha256((dna1 + p2).encode()).hexdigest()[:8]
    dna2 = p2 + "-" + h2

    chain = [dna0, dna1, dna2]
    for d in chain:
        print("  {}".format(d))
    print("  链验证: {}".format('✅ 完整' if DNATrace.verify_chain(chain) else '❌ 断裂'))

    # 再构造一个被篡改的链用于示范检测
    fake_dna1 = "#龍芯⚡️丙午·乙未·庚子·☲离-SCT-tampered-v9.9-ffffffff"
    fake_chain = [dna0, fake_dna1, dna2]
    print("  伪造链验证: {}".format('✅ 完整(异常!)' if DNATrace.verify_chain(fake_chain) else '❌ 断裂(正确检出)'))

    # ── 完毕 ──
    print("\n" + sep)
    print("  ✅ 8章数学建模 + 7组仿真 = 全部完成")
    print("  📄 论文: papers/反奶头乐共生理论_数学建模_v1.0.md")
    print("  ⚙️ 引擎: engines/lh_symbiotic_cognition_engine.py")
    print(sep + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
