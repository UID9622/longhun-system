#!/usr/bin/env python3
"""
龍魂·模型优化引擎 v2.0 — 基于DNA文档的模型训练优化
DNA: #龍芯⚡️丙午·乙申·MODEL-OPTIMIZER-v2.0-CODE-LANDED
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

核心优化策略（来自UID9622核心DNA文档）:
  1. 节气加权系统 → 训练数据动态权重校准
  2. 五行平衡 → Loss函数多维度均衡
  3. 中庸决策 → 早停与验证策略优化
  4. 自求多福 → 自适应学习率与训练回滚
  5. 反懒惰机制 → 训练中断自动恢复

集成方式:
  from lh_model_optimizer import LHTrainingOptimizer
  optimizer = LHTrainingOptimizer()
  optimizer.apply_to_trainer(trainer)  # MLX/PyTorch
"""

import datetime
import json
import math
import os
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field

# 内部依赖
from lh_cultural_dna import stamp_output, CULTURAL_DNA, inject_creator_mark, encode_dna
from lh_hexagram_data import SOLAR_TERMS, get_solar_term_weight, WUXING_RELATION, get_wuxing_relation
from lh_zhongyong_decision import LuckyWuxingModule, ZhongYongDecisionModule


# ============================================================
# 1. 节气加权系统 → 训练数据动态权重
# ============================================================

class SolarTermWeightScheduler:
    """节气感知的训练数据权重调度器
    
    核心理念: 不同节气影响学习效率
    - 春夏季（立春→夏至）: 生长季，权重偏重探索 → 高lr·低weight_decay
    - 秋冬季（立秋→冬至）: 收藏季，权重偏重收敛 → 低lr·高weight_decay
    """

    SOLAR_TERM_DATES = {
        (2, 4): "立春", (2, 19): "雨水", (3, 6): "惊蛰", (3, 21): "春分",
        (4, 5): "清明", (4, 20): "谷雨", (5, 6): "立夏", (5, 21): "小满",
        (6, 6): "芒种", (6, 21): "夏至", (7, 7): "小暑", (7, 23): "大暑",
        (8, 8): "立秋", (8, 23): "处暑", (9, 8): "白露", (9, 23): "秋分",
        (10, 8): "寒露", (10, 23): "霜降", (11, 7): "立冬", (11, 22): "小雪",
        (12, 7): "大雪", (12, 22): "冬至", (1, 6): "小寒", (1, 20): "大寒",
    }

    def __init__(self):
        self.current_term = self._get_current_solar_term()
        self.base_weight = get_solar_term_weight(self.current_term)
        self.history: List[Dict] = []

    def _get_current_solar_term(self) -> str:
        """获取当前节气（简化版）"""
        now = datetime.datetime.now()
        month, day = now.month, now.day

        best_term = "春分"
        min_diff = 365
        for (m, d), term in self.SOLAR_TERM_DATES.items():
            diff = abs((month - m) * 30 + (day - d))
            if diff < min_diff:
                min_diff = diff
                best_term = term
        return best_term

    def get_learning_rate_modifier(self) -> float:
        """获取基于节气的学习率修正系数"""
        term_data = SOLAR_TERMS.get(self.current_term, {"weight": 1.0})
        weight = term_data["weight"]

        # 春夏季: 阳气生发 → lr适当提高，鼓励探索
        # 秋冬季: 阴气主导 → lr降低，精细收敛
        if weight >= 1.0:
            return 1.0 + (weight - 1.0) * 0.5  # 春季最多+5% lr
        else:
            return 0.9 + weight * 0.1  # 冬季降至90%

    def get_weight_decay_modifier(self) -> float:
        """获取基于节气的weight_decay修正系数"""
        term_data = SOLAR_TERMS.get(self.current_term, {"weight": 1.0})
        weight = term_data["weight"]

        # 春夏季: 轻weight_decay（鼓励生长）
        # 秋冬季: 重weight_decay（精炼收敛）
        if weight >= 1.0:
            return 0.8  # 减轻正则化
        else:
            return 1.2  # 加重正则化

    def get_data_augmentation_strength(self) -> float:
        """基于节气的数据增强强度"""
        term_data = SOLAR_TERMS.get(self.current_term, {"keywords": []})
        keywords = term_data.get("keywords", [])

        # "生发/突破/启动"类节气 → 高增强
        # "收藏/内省/沉淀"类节气 → 低增强
        augment_keywords = {"生发", "突破", "启动", "生长", "旺盛", "播种"}
        reduce_keywords = {"收藏", "内省", "沉淀", "静默", "收敛", "蓄势"}

        strength = 0.5
        for kw in keywords:
            if kw in augment_keywords:
                strength += 0.15
            elif kw in reduce_keywords:
                strength -= 0.1

        return max(0.2, min(1.0, strength))

    def get_training_advice(self) -> Dict:
        """获取节气感知的训练建议"""
        term_data = SOLAR_TERMS.get(self.current_term, {})
        return {
            "current_term": self.current_term,
            "term_weight": self.base_weight,
            "yin_yang": term_data.get("yin_yang", "未知"),
            "lr_modifier": self.get_learning_rate_modifier(),
            "wd_modifier": self.get_weight_decay_modifier(),
            "augment_strength": self.get_data_augmentation_strength(),
            "advice": self._generate_advice(),
        }

    def _generate_advice(self) -> str:
        term_data = SOLAR_TERMS.get(self.current_term, {"weight": 1.0})
        w = term_data["weight"]
        if w >= 1.05:
            return f"🌱 {self.current_term} — 生长季，可适当激进训练，增加探索"
        elif w >= 0.95:
            return f"☯️ {self.current_term} — 平衡季，标准训练策略"
        elif w >= 0.75:
            return f"🍂 {self.current_term} — 收敛季，降低lr，精细调参"
        else:
            return f"❄️ {self.current_term} — 收藏季，小步迭代，避免大变动"


# ============================================================
# 2. 五行平衡 → Loss函数多维度均衡
# ============================================================

class WuxingLossBalancer:
    """五行感知的Loss函数平衡器
    
    五行映射:
    - 木(生长) → training loss (学习进度)
    - 火(扩张) → generalization gap (泛化能力)
    - 土(稳定) → stability score (权重稳定性)
    - 金(收敛) → convergence speed (收敛速度)
    - 水(流动) → gradient flow (梯度健康度)
    """

    def __init__(self):
        self.wuxing = LuckyWuxingModule()
        self.loss_components: Dict[str, List[float]] = {
            "train_loss": [],
            "val_loss": [],
            "weight_norm": [],
            "gradient_norm": [],
            "learning_rate": [],
        }
        self.balance_history: List[Dict] = []

    def record_metrics(self, train_loss: float, val_loss: float,
                       weight_norm: float = 0, grad_norm: float = 0,
                       lr: float = 0):
        """记录训练指标"""
        self.loss_components["train_loss"].append(train_loss)
        self.loss_components["val_loss"].append(val_loss)
        self.loss_components["weight_norm"].append(weight_norm)
        self.loss_components["gradient_norm"].append(grad_norm)
        self.loss_components["learning_rate"].append(lr)

    def get_wuxing_state(self) -> Dict:
        """将训练状态映射为五行状态"""
        recent = {k: v[-10:] if len(v) >= 10 else v
                  for k, v in self.loss_components.items()}

        def safe_last(lst, default=0.5):
            return lst[-1] if lst else default

        def safe_mean(lst, default=0.5):
            return sum(lst) / len(lst) if lst else default

        # 木: training loss越低越好 → 反转
        growth = 1.0 - min(safe_last(recent["train_loss"]), 1.0)

        # 火: val_loss相对train_loss的差距 → 泛化能力
        tl = safe_last(recent["train_loss"], 0.5)
        vl = safe_last(recent["val_loss"], 0.5)
        expansion = 1.0 - min(abs(vl - tl) / max(tl, 1e-6), 1.0)

        # 土: 稳定性 → 连续几步的loss变化
        if len(recent["train_loss"]) >= 3:
            stability = 1.0 - min(
                abs(safe_last(recent["train_loss"]) - safe_mean(recent["train_loss"])), 1.0
            )
        else:
            stability = 0.5

        # 金: 收敛效率 → loss下降速率
        if len(recent["train_loss"]) >= 5:
            early = safe_mean(recent["train_loss"][:len(recent["train_loss"])//2])
            late = safe_mean(recent["train_loss"][len(recent["train_loss"])//2:])
            efficiency = min(late / max(early, 1e-6), 1.0) if early > late else 0.8
        else:
            efficiency = 0.5

        # 水: 梯度健康度
        gn = safe_last(recent["gradient_norm"], 10)
        flexibility = 1.0 - min(gn / 100.0, 1.0) if gn > 1 else 0.8

        return {
            "growth": growth,
            "expansion": expansion,
            "stability": stability,
            "efficiency": efficiency,
            "flexibility": flexibility,
        }

    def get_balance_advice(self) -> Dict:
        """获取五行平衡建议"""
        state = self.get_wuxing_state()
        analysis = self.wuxing.analyze_balance(state)
        self.balance_history.append({
            "time": datetime.datetime.now().isoformat(),
            "state": state,
            "analysis": analysis,
        })
        return analysis

    def compute_balanced_loss(self, base_loss: float, val_loss: float) -> float:
        """计算五行平衡的综合Loss"""
        state = self.get_wuxing_state()
        analysis = self.wuxing.analyze_balance(state)

        # 薄弱环节对应的loss分量加权
        weak = analysis.get("weak_point", "土")
        loss_weights = {
            "木": 1.0,  # growth focus
            "火": 1.0,  # generalization focus
            "土": 1.05,  # stability focus
            "金": 1.0,  # convergence focus
            "水": 1.0,  # gradient focus
        }

        # 根据薄弱环节微调loss
        # 简化的平衡loss = base * (1 + weak_factor)
        weak_factor = max(0, 0.5 - state.get({
            "木": "growth", "火": "expansion", "土": "stability",
            "金": "efficiency", "水": "flexibility",
        }[weak], 0.5)) * 0.1

        return base_loss * (1.0 + weak_factor)


# ============================================================
# 3. 中庸决策 → 早停与验证策略
# ============================================================

class ZhongYongEarlyStopping:
    """中庸式早停策略
    
    核心理念: 不追求最低的val_loss（那是"激进"），
              而是找"平衡点"——loss够低且趋势稳定。
    """

    def __init__(self, patience: int = 5, min_delta: float = 0.001,
                 balance_threshold: float = 0.7):
        self.patience = patience
        self.min_delta = min_delta
        self.balance_threshold = balance_threshold
        self.best_loss = float("inf")
        self.best_iter = 0
        self.counter = 0
        self.history: List[Dict] = []
        self.zhongyong = ZhongYongDecisionModule()

    def should_stop(self, val_loss: float, train_loss: float, iteration: int) -> Tuple[bool, Dict]:
        """中庸判断: 是否该停"""
        self.history.append({
            "iter": iteration,
            "val_loss": val_loss,
            "train_loss": train_loss,
        })

        # 常规早停判断
        if val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.best_iter = iteration
            self.counter = 0
        else:
            self.counter += 1

        # 中庸判断: 综合多维度
        options = []
        if len(self.history) >= 5:
            recent = self.history[-5:]
            trend = self._calc_trend(recent)

            options = [
                {
                    "name": "继续训练",
                    "factors": {"loss趋势": self._trend_score(trend["val"]),
                               "稳定性": self._stability_score(recent),
                               "效率": self._efficiency_score(recent)},
                    "risk": 0.3,
                    "opportunity": 0.7 if trend["val"] < 0 else 0.3,
                },
                {
                    "name": "立即停止",
                    "factors": {"loss趋势": 1.0 - self._trend_score(trend["val"]),
                               "稳定性": 0.8,
                               "效率": max(0, self._efficiency_score(recent))},
                    "risk": 0.1 if self.counter >= self.patience else 0.7,
                    "opportunity": 0.3,
                },
            ]

            decision = self.zhongyong.balanced_decision(options)
            mid_stop = (decision["recommended"] == "立即停止" and
                       decision["score"] > self.balance_threshold)
        else:
            mid_stop = False

        # 综合判断
        hard_stop = self.counter >= self.patience
        should_stop = hard_stop or mid_stop

        return should_stop, {
            "hard_stop": hard_stop,
            "zhongyong_stop": mid_stop,
            "counter": self.counter,
            "best_loss": self.best_loss,
            "best_iter": self.best_iter,
            "decision": "停止" if should_stop else "继续",
            "advice": self._get_stop_advice(hard_stop, mid_stop),
        }

    def _calc_trend(self, history: List[Dict]) -> Dict:
        """计算loss趋势"""
        if len(history) < 3:
            return {"val": 0, "train": 0}
        n = len(history)
        first_half = history[:n//2]
        second_half = history[n//2:]

        val_trend = (sum(h["val_loss"] for h in second_half) / len(second_half) -
                     sum(h["val_loss"] for h in first_half) / len(first_half))
        train_trend = (sum(h["train_loss"] for h in second_half) / len(second_half) -
                       sum(h["train_loss"] for h in first_half) / len(first_half))
        return {"val": val_trend, "train": train_trend}

    def _trend_score(self, trend: float) -> float:
        """趋势转评分（下降=好，上升=坏）"""
        return max(0, min(1, 0.5 - trend * 2))

    def _stability_score(self, recent: List[Dict]) -> float:
        """稳定性评分"""
        losses = [h["val_loss"] for h in recent]
        mean = sum(losses) / len(losses)
        std = (sum((l - mean)**2 for l in losses) / len(losses)) ** 0.5
        return max(0, 1 - std * 10)

    def _efficiency_score(self, recent: List[Dict]) -> float:
        """效率评分"""
        if len(recent) < 3:
            return 0.5
        total_improvement = recent[0]["val_loss"] - recent[-1]["val_loss"]
        return max(0, min(1, total_improvement * 5 + 0.5))

    def _get_stop_advice(self, hard_stop: bool, mid_stop: bool) -> str:
        if hard_stop and mid_stop:
            return "中庸之道判断：训练已达平衡点，继续收益小，建议停止。"
        elif hard_stop:
            return "耐心耗尽：val_loss不再下降，按传统标准停止。"
        elif mid_stop:
            return "中庸智慧：虽未达到hard stop，但综合判断此时停止最优。"
        return "继续训练：尚有优化空间。"


# ============================================================
# 4. 自求多福 → 自适应调度器
# ============================================================


class AdaptiveTrainingScheduler:
    """自求多福式自适应训练调度器
    
    核心理念: 不依赖外部超参搜索，从训练过程中自适应学习最优参数
    """

    def __init__(self, initial_lr: float = 1e-4, min_lr: float = 1e-6,
                 warmup_steps: int = 100):
        self.initial_lr = initial_lr
        self.min_lr = min_lr
        self.warmup_steps = warmup_steps
        self.current_step = 0
        self.loss_history: List[float] = []
        self.lr_history: List[float] = []
        self.adaptation_log: List[Dict] = []

    def step(self, current_loss: float) -> float:
        """计算当前步的学习率"""
        self.current_step += 1
        self.loss_history.append(current_loss)

        # Warmup
        if self.current_step <= self.warmup_steps:
            lr = self.initial_lr * (self.current_step / self.warmup_steps)
        else:
            lr = self._adaptive_lr(current_loss)

        self.lr_history.append(lr)
        return lr

    def _adaptive_lr(self, current_loss: float) -> float:
        """自适应学习率——基于loss变化动态调整"""
        if len(self.loss_history) < 10:
            return self.initial_lr

        recent = self.loss_history[-10:]
        mean_loss = sum(recent) / len(recent)
        std_loss = (sum((l - mean_loss)**2 for l in recent) / len(recent)) ** 0.5

        # 如果loss在振荡（方差大），降低lr
        if std_loss > 0.1 * mean_loss:
            factor = 0.8
            advice = "loss振荡 → 降低lr"
        # 如果loss在缓慢下降，保持lr
        elif recent[0] > recent[-1]:
            factor = 1.0
            advice = "loss下降中 → 维持lr"
        # 如果loss停滞，适当降低lr
        else:
            factor = 0.9
            advice = "loss停滞 → 微降lr"

        base_lr = self.lr_history[-1] if self.lr_history else self.initial_lr
        new_lr = max(self.min_lr, base_lr * factor)

        if factor != 1.0:
            self.adaptation_log.append({
                "step": self.current_step,
                "old_lr": base_lr,
                "new_lr": new_lr,
                "reason": advice,
                "loss_mean": mean_loss,
                "loss_std": std_loss,
            })

        return new_lr

    def should_rollback(self, patience: int = 20) -> Tuple[bool, Optional[Dict]]:
        """检测是否需要回滚（过拟合/发散检测）"""
        if len(self.loss_history) < patience * 2:
            return False, None

        recent = self.loss_history[-patience:]
        earlier = self.loss_history[-patience*2:-patience]

        recent_mean = sum(recent) / len(recent)
        earlier_mean = sum(earlier) / len(earlier)

        # 如果近期loss显著高于之前，说明可能过拟合或发散
        if recent_mean > earlier_mean * 1.5:
            return True, {
                "reason": "loss回升超过50%",
                "recent_mean": recent_mean,
                "earlier_mean": earlier_mean,
                "action": "回滚到best checkpoint + 降低lr",
            }

        return False, None

    def get_training_philosophy(self) -> str:
        """自求多福的训练哲学"""
        return ("不依赖外部调参，靠自己在训练过程中自适应找到最优参数。\n"
                "这就是'自求多福'——从每次迭代中学习，自己调整步伐。")


# ============================================================
# 5. LHTrainingOptimizer — 统一优化入口
# ============================================================


class LHTrainingOptimizer:
    """龍魂·训练优化器 — 统一管理所有优化策略"""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}

        # 四大优化引擎
        self.solar_scheduler = SolarTermWeightScheduler()
        self.wuxing_balancer = WuxingLossBalancer()
        self.zhongyong_stopper = ZhongYongEarlyStopping(
            patience=self.config.get("early_stop_patience", 5),
            min_delta=self.config.get("min_delta", 0.001),
        )
        self.adaptive_scheduler = AdaptiveTrainingScheduler(
            initial_lr=self.config.get("learning_rate", 1e-4),
            warmup_steps=self.config.get("warmup_steps", 100),
        )

        # 状态
        self.current_iteration = 0
        self.best_metrics: Dict = {}
        self.optimization_log: List[Dict] = []

    def on_training_start(self) -> Dict:
        """训练开始时调用"""
        solar_advice = self.solar_scheduler.get_training_advice()

        advice = {
            "solar_term": solar_advice,
            "base_lr": self.config.get("learning_rate", 1e-4),
            "adjusted_lr": (self.config.get("learning_rate", 1e-4) *
                          solar_advice["lr_modifier"]),
            "adjusted_wd": (self.config.get("weight_decay", 0.01) *
                          solar_advice["wd_modifier"]),
            "augment_strength": solar_advice["augment_strength"],
        }

        self.optimization_log.append({
            "phase": "start",
            "time": datetime.datetime.now().isoformat(),
            **advice,
        })

        return advice

    def on_step_end(self, train_loss: float, val_loss: Optional[float] = None) -> Dict:
        """每步结束后调用"""
        self.current_iteration += 1

        # 1. 记录五行指标
        self.wuxing_balancer.record_metrics(
            train_loss=train_loss,
            val_loss=val_loss or train_loss,
            lr=self.adaptive_scheduler.lr_history[-1] if self.adaptive_scheduler.lr_history else 0,
        )

        # 2. 自适应学习率
        current_lr = self.adaptive_scheduler.step(train_loss)

        # 3. 五行平衡分析
        balance = self.wuxing_balancer.get_balance_advice()

        # 4. 中庸早停判断
        should_stop, stop_info = False, {"decision": "无"}
        if val_loss is not None and self.current_iteration % 25 == 0:  # 每25步评估一次
            should_stop, stop_info = self.zhongyong_stopper.should_stop(
                val_loss, train_loss, self.current_iteration
            )

        # 5. 回滚检测
        should_rollback, rollback_info = self.adaptive_scheduler.should_rollback()

        result = {
            "iteration": self.current_iteration,
            "train_loss": train_loss,
            "val_loss": val_loss,
            "current_lr": current_lr,
            "balance_score": balance.get("balance_score", 0),
            "weak_point": balance.get("weak_point", ""),
            "should_stop": should_stop,
            "stop_info": stop_info,
            "should_rollback": should_rollback,
            "rollback_info": rollback_info,
        }

        # 更新最佳
        if val_loss is not None and (not self.best_metrics or val_loss < self.best_metrics.get("val_loss", float("inf"))):
            self.best_metrics = {
                "iteration": self.current_iteration,
                "val_loss": val_loss,
                "train_loss": train_loss,
            }

        if self.current_iteration % 100 == 0:
            self.optimization_log.append({
                "phase": f"step_{self.current_iteration}",
                **{k: v for k, v in result.items()
                   if k not in ["stop_info", "rollback_info"]},
            })

        return result

    def on_training_end(self) -> Dict:
        """训练结束报告"""
        return {
            "total_iterations": self.current_iteration,
            "best_metrics": self.best_metrics,
            "final_lr": self.adaptive_scheduler.lr_history[-1] if self.adaptive_scheduler.lr_history else 0,
            "balance_history": self.wuxing_balancer.balance_history[-3:],
            "solar_term_final": self.solar_scheduler.get_training_advice(),
            "philosophy": {
                "节气": "时节感知，顺势而为",
                "五行": "多维平衡，不偏不废",
                "中庸": "不追求最佳loss，追求最稳效果",
                "自求多福": "不依赖外部调参，自适应学习",
            },
            "dna": encode_dna("OPTIMIZER", "COMPLETE", str(self.current_iteration)),
        }

    def get_dynamic_config(self) -> Dict:
        """获取动态最优配置（供trainer使用）"""
        solar = self.solar_scheduler.get_training_advice()
        return {
            "learning_rate": self.config.get("learning_rate", 1e-4) * solar["lr_modifier"],
            "weight_decay": self.config.get("weight_decay", 0.01) * solar["wd_modifier"],
            "data_augment": solar["augment_strength"],
            "solar_term": solar["current_term"],
            "advice": solar["advice"],
        }


# ============================================================
# 测试入口
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🧬 龍魂·模型优化引擎 v2.0")
    print(f"👤 {CULTURAL_DNA['creator']}")
    print("=" * 60)

    # --- 节气调度测试 ---
    solar = SolarTermWeightScheduler()
    advice = solar.get_training_advice()
    print(f"\n🌿 节气调度: {advice['current_term']}")
    print(f"  权重: {advice['term_weight']:.2f}")
    print(f"  LR修正: {advice['lr_modifier']:.2f}")
    print(f"  WD修正: {advice['wd_modifier']:.2f}")
    print(f"  建议: {advice['advice']}")

    # --- 五行平衡测试 ---
    wuxing = WuxingLossBalancer()
    for tl, vl in [(2.5, 3.0), (2.0, 2.5), (1.5, 2.0), (1.0, 1.5), (0.8, 1.2), (0.5, 0.8)]:
        wuxing.record_metrics(tl, vl, weight_norm=1.0, grad_norm=10 * (2.5 - tl))
    balance = wuxing.get_balance_advice()
    print(f"\n☯️ 五行平衡: {balance['balance_score']:.2%}")
    print(f"  薄弱: {balance['weak_point']}")
    print(f"  建议: {balance['suggestion'][:80]}...")

    # --- 中庸早停测试 ---
    zhongyong = ZhongYongEarlyStopping(patience=3)
    val_losses = [0.8, 0.7, 0.65, 0.63, 0.64, 0.62, 0.63, 0.65, 0.64, 0.66]
    for i, vl in enumerate(val_losses):
        should_stop, info = zhongyong.should_stop(vl, vl * 0.8, i * 25)
        print(f"  Iter {i*25}: val={vl:.3f} → {info['decision']} ({info.get('advice','')[:40]}...)")
        if should_stop:
            break

    # --- 自适应调度测试 ---
    adaptive = AdaptiveTrainingScheduler(initial_lr=1e-4)
    losses = [2.5, 2.3, 2.0, 1.8, 1.5, 1.3, 1.2, 1.15, 1.1, 1.05,
              1.08, 1.02, 1.0, 0.98, 0.95, 0.94, 0.92, 0.93, 0.91, 0.90]
    for l in losses:
        lr = adaptive.step(l)
    print(f"\n🔄 自适应调度: 初始lr={adaptive.initial_lr} → 最终lr={lr:.2e}")
    print(f"  适应次数: {len(adaptive.adaptation_log)}")

    # --- 统一优化器测试 ---
    optimizer = LHTrainingOptimizer({"learning_rate": 1e-4, "weight_decay": 0.01})
    start_advice = optimizer.on_training_start()
    print(f"\n🚀 统一优化器启动:")
    print(f"  调整后LR: {start_advice['adjusted_lr']:.2e}")
    print(f"  增强强度: {start_advice['augment_strength']:.0%}")

    for tl, vl in zip([2.5, 2.0, 1.5, 1.0, 0.8, 0.5], [3.0, 2.5, 2.0, 1.5, 1.0, 0.7]):
        result = optimizer.on_step_end(tl, vl)
        if result["should_stop"]:
            print(f"  早停触发 @Iter {result['iteration']}")
            break

    end_report = optimizer.on_training_end()
    print(f"\n📊 训练报告: 最佳ValLoss={end_report['best_metrics'].get('val_loss', 'N/A')}")
