#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🔐 多方主权下的AI开放审计模型
——基于龍魂系统的可验证治理架构

白皮书版本: v2.0（完整推演版）
DNA追溯码: #龍芯⚡️2026-08-03-OPEN-AUDIT-ENGINE-v2.0-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG签名: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能:
  1. 五类参与主体建模（国家、企业、监管机构、开发者、用户社会）
  2. 核心变量动态演化（C, T, R, G, I, S）
  3. 三阶段博弈模拟（能力竞赛→风险暴露→治理选择）
  4. 重复博弈均衡分析（纳什均衡检测、临界贴现因子计算）
  5. 三种均衡状态识别（A/B/C）
  6. 三组预设推演场景
  7. 龍魂系统审计协议模拟
  8. 可视化输出（三轴图、时间序列、均衡地图）
  9. 易经隐喻层映射（未济→既济转化路径）
  10. 导出JSON报告 + GPG签名验证

依赖:
  pip install numpy matplotlib pandas scipy

用法:
  python3 bin/lh_open_audit_engine.py --run
  python3 bin/lh_open_audit_engine.py --run --steps 100 --plot
  python3 bin/lh_open_audit_engine.py --scenario A --steps 80
  python3 bin/lh_open_audit_engine.py --export --format json
  python3 bin/lh_open_audit_engine.py --info
  python3 bin/lh_open_audit_engine.py --audit-log
"""

import os
import sys
import json
import math
import hashlib
import time
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime

import numpy as np
import matplotlib
matplotlib.use('Agg')  # 无头模式，兼容服务器环境
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

# ============================================================
# 固定锚点
# ============================================================

DNA = "#龍芯⚡️2026-08-03-OPEN-AUDIT-ENGINE-v2.0-UID9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "open_audit_output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 配置
# ============================================================

CONFIG = {
    "default_steps": 60,
    "risk_sensitivity_lambda": 2.0,
    "governance_innovation_eta": 1.5,
    "transparency_innovation_xi": 0.8,
    "concentration_innovation_rho": 0.3,
    "stability_alpha": 0.6,
    "stability_beta": 0.8,
    "stability_gamma": 0.4,
    "stability_delta": 0.5,
    "discount_factor": 0.85,
    "concentration_threshold": 0.70,
    "transparency_threshold": 0.60,
    "risk_premium_phi": 0.5,
    "min_brightness": 20,
    "max_brightness": 235,
}

# ============================================================
# 工具函数
# ============================================================

def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")

def generate_sub_dna(module: str = "AUDIT") -> str:
    ts = datetime.now().strftime("%Y%m%d")
    h = hashlib.md5(f"{module}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-{module}-UID9622-{h}"

def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

def clamp(val: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    return max(min_val, min(max_val, val))

# ============================================================
# 1. 核心变量定义
# ============================================================

@dataclass
class GovernanceVariables:
    """治理核心变量 (全部归一化至 [0,1])"""
    C: float = 0.50   # 技术集中度
    T: float = 0.40   # 透明度水平
    R: float = 0.30   # 风险外部性
    G: float = 0.30   # 治理强度
    I: float = 0.50   # 创新速度
    S: float = 0.50   # 系统稳定性

    def to_dict(self) -> Dict:
        return asdict(self)

    def to_array(self) -> np.ndarray:
        return np.array([self.C, self.T, self.R, self.G, self.I, self.S])

    def copy(self) -> 'GovernanceVariables':
        return GovernanceVariables(
            C=self.C, T=self.T, R=self.R,
            G=self.G, I=self.I, S=self.S
        )

# ============================================================
# 2. 参与主体定义（五类）
# ============================================================

class PlayerType(Enum):
    STATE = "State"
    FIRM = "Firm"
    REGULATOR = "Regulator"
    DEVELOPER = "Developer"
    SOCIETY = "Society"

@dataclass
class Player:
    """博弈参与主体"""
    ptype: PlayerType
    name: str
    utility: float = 0.0
    strategy: Dict[str, float] = field(default_factory=dict)
    preference_weights: Dict[str, float] = field(default_factory=dict)

    def compute_utility(self, vars: GovernanceVariables) -> float:
        """根据主体类型计算效用"""
        if self.ptype == PlayerType.STATE:
            # 国家：技术优势 + 稳定 - 风险
            w = self.preference_weights or {"C": 0.4, "S": 0.4, "R": 0.2}
            self.utility = w.get("C", 0.4) * vars.C + w.get("S", 0.4) * vars.S - w.get("R", 0.2) * vars.R

        elif self.ptype == PlayerType.FIRM:
            # 企业：创新利润 - 风险成本 - 治理成本
            w = self.preference_weights or {"I": 0.5, "R": 0.3, "G": 0.2}
            self.utility = w.get("I", 0.5) * vars.I - w.get("R", 0.3) * vars.R - w.get("G", 0.2) * vars.G * 0.3

        elif self.ptype == PlayerType.REGULATOR:
            # 监管：风险最小化 - 治理过度的副作用
            w = self.preference_weights or {"R": 0.6, "G": 0.4}
            self.utility = -w.get("R", 0.6) * vars.R - w.get("G", 0.4) * (vars.G ** 2) * 0.5

        elif self.ptype == PlayerType.DEVELOPER:
            # 开发者：创新 + 透明 - 治理压制
            w = self.preference_weights or {"I": 0.4, "T": 0.3, "G": 0.3}
            self.utility = w.get("I", 0.4) * vars.I + w.get("T", 0.3) * vars.T - w.get("G", 0.3) * vars.G * 0.2

        elif self.ptype == PlayerType.SOCIETY:
            # 用户社会：安全(稳定性) + 透明度 - 风险
            w = self.preference_weights or {"S": 0.4, "T": 0.3, "R": 0.3}
            self.utility = w.get("S", 0.4) * vars.S + w.get("T", 0.3) * vars.T - w.get("R", 0.3) * vars.R

        else:
            self.utility = 0.0

        return clamp(self.utility)

    def to_dict(self) -> Dict:
        return {
            "type": self.ptype.value,
            "name": self.name,
            "utility": round(self.utility, 4),
            "strategy": {k: round(v, 4) for k, v in self.strategy.items()}
        }

# ============================================================
# 3. 核心计算公式
# ============================================================

class GovernanceFormulas:
    """白皮书中的所有核心公式"""

    @staticmethod
    def compute_risk(C: float, lam: float = None) -> float:
        """R = 1 - exp(-λ·C²)"""
        lam = lam or CONFIG["risk_sensitivity_lambda"]
        return 1.0 - math.exp(-lam * C * C)

    @staticmethod
    def compute_innovation_short(G: float, I0: float = 0.6, eta: float = None) -> float:
        """I_short = I₀ · exp(-η·G)"""
        eta = eta or CONFIG["governance_innovation_eta"]
        return I0 * math.exp(-eta * G)

    @staticmethod
    def compute_innovation_long(T: float, C: float, I0: float = 0.6,
                                 xi: float = None, rho: float = None) -> float:
        """I_long = I₀ · (1 + ξ·T - ρ·C)"""
        xi = xi or CONFIG["transparency_innovation_xi"]
        rho = rho or CONFIG["concentration_innovation_rho"]
        return I0 * (1.0 + xi * T - rho * C)

    @staticmethod
    def compute_stability(T: float, C: float, I: float, R: float,
                          alpha: float = None, beta: float = None,
                          gamma: float = None, delta: float = None) -> float:
        """S = α·T - β·C² + γ·I - δ·R"""
        alpha = alpha or CONFIG["stability_alpha"]
        beta = beta or CONFIG["stability_beta"]
        gamma = gamma or CONFIG["stability_gamma"]
        delta = delta or CONFIG["stability_delta"]
        return clamp(alpha * T - beta * C * C + gamma * I - delta * R)

    @staticmethod
    def compute_risk_premium(R: float, T: float, phi: float = None) -> float:
        """P_risk' = R · (1 - T) · exp(-φ·T)"""
        phi = phi or CONFIG["risk_premium_phi"]
        return R * (1.0 - T) * math.exp(-phi * T)

    @staticmethod
    def compute_critical_delta(u_defect: float = 4.0,
                               u_coop: float = 3.0,
                               u_punish: float = 2.0) -> float:
        """δ* = (u_defect - u_coop) / (u_defect - u_punish)"""
        return (u_defect - u_coop) / (u_defect - u_punish) if u_defect != u_punish else 0.5

    @staticmethod
    def compute_regulatory_arbitrage(G_max: float = 1.0, G_min: float = 0.0, T: float = 0.5) -> float:
        """监管套利空间 = (G_max - G_min) × (1 - T)"""
        return (G_max - G_min) * (1.0 - T)

    @staticmethod
    def detect_equilibrium(C: float, T: float, S: float) -> Dict:
        """检测当前均衡状态"""
        if C > 0.70 and T < 0.30:
            return {
                "type": "A",
                "name": "高集中+低透明",
                "description": "短期效率高，风险高，国际冲突概率高",
                "stability": "低",
                "color": "🔴"
            }
        elif 0.40 <= C <= 0.70 and 0.30 <= T <= 0.70:
            return {
                "type": "B",
                "name": "中集中+中透明",
                "description": "当前主流状态，中等稳定",
                "stability": "中",
                "color": "🟡"
            }
        elif C > 0.60 and T > 0.70:
            return {
                "type": "C",
                "name": "可验证集中+高透明",
                "description": "理想状态，技术集中但可审计，风险可控",
                "stability": "高",
                "color": "🟢"
            }
        else:
            return {
                "type": "TRANSITION",
                "name": "过渡状态",
                "description": "正在向某种均衡演化",
                "stability": "不确定",
                "color": "⚪"
            }

# ============================================================
# 4. 博弈引擎
# ============================================================

class AIGovernanceSimulator:
    """AI治理博弈模拟引擎"""

    def __init__(self, config: Dict = None):
        self.config = config or CONFIG.copy()
        self.vars = GovernanceVariables()
        self.players: List[Player] = []
        self.history: List[Dict] = []
        self.current_step = 0
        self.equilibrium_history: List[Dict] = []
        self._init_players()
        self._init_history()

    def _init_players(self):
        """初始化五类主体"""
        player_configs = [
            (PlayerType.STATE, "国家", {"C": 0.4, "S": 0.4, "R": 0.2}),
            (PlayerType.FIRM, "企业", {"I": 0.5, "R": 0.3, "G": 0.2}),
            (PlayerType.REGULATOR, "监管机构", {"R": 0.6, "G": 0.4}),
            (PlayerType.DEVELOPER, "开发者社区", {"I": 0.4, "T": 0.3, "G": 0.3}),
            (PlayerType.SOCIETY, "用户社会", {"S": 0.4, "T": 0.3, "R": 0.3}),
        ]
        for ptype, name, weights in player_configs:
            self.players.append(
                Player(ptype=ptype, name=name, preference_weights=weights)
            )

    def _init_history(self):
        """初始化历史记录"""
        self.history.append({
            "step": 0,
            **self.vars.to_dict(),
            "utilities": {p.name: 0.0 for p in self.players},
            "equilibrium": GovernanceFormulas.detect_equilibrium(
                self.vars.C, self.vars.T, self.vars.S
            )
        })

    def _update_variables(self, strategies: Dict[str, float]):
        """根据策略更新核心变量"""
        dC = clamp(strategies.get("dC", 0.0), -0.3, 0.3)
        dT = clamp(strategies.get("dT", 0.0), -0.3, 0.3)
        dG = clamp(strategies.get("dG", 0.0), -0.3, 0.3)

        # 更新C
        self.vars.C = clamp(self.vars.C + dC * 0.06)
        # 更新T
        self.vars.T = clamp(self.vars.T + dT * 0.06)
        # 更新G
        self.vars.G = clamp(self.vars.G + dG * 0.06)
        # 更新R（由C决定）
        self.vars.R = GovernanceFormulas.compute_risk(
            self.vars.C, self.config.get("risk_sensitivity_lambda")
        )
        # 更新I（混合短期+长期）
        I_short = GovernanceFormulas.compute_innovation_short(
            self.vars.G, eta=self.config.get("governance_innovation_eta")
        )
        I_long = GovernanceFormulas.compute_innovation_long(
            self.vars.T, self.vars.C,
            xi=self.config.get("transparency_innovation_xi"),
            rho=self.config.get("concentration_innovation_rho")
        )
        self.vars.I = 0.5 * I_short + 0.5 * I_long
        # 更新S
        self.vars.S = GovernanceFormulas.compute_stability(
            self.vars.T, self.vars.C, self.vars.I, self.vars.R,
            alpha=self.config.get("stability_alpha"),
            beta=self.config.get("stability_beta"),
            gamma=self.config.get("stability_gamma"),
            delta=self.config.get("stability_delta")
        )

    def _compute_strategies(self) -> Dict[str, float]:
        """各主体基于效用最大化选择策略"""
        strategies = {"dC": 0.0, "dT": 0.0, "dG": 0.0}

        # 国家：追求C，但风险高时追求T和G
        if self.vars.C < 0.75:
            strategies["dC"] += 0.2
        else:
            strategies["dC"] -= 0.1
        if self.vars.R > 0.5:
            strategies["dT"] += 0.15
            strategies["dG"] += 0.1

        # 企业：追求C和I，抵制T和G
        if self.vars.C < 0.80:
            strategies["dC"] += 0.15
        if self.vars.G > 0.4:
            strategies["dG"] -= 0.15
        if self.vars.T > 0.5:
            strategies["dT"] -= 0.1

        # 监管机构：R高时提高G和T
        if self.vars.R > 0.35:
            strategies["dG"] += 0.2
            strategies["dT"] += 0.1
        else:
            strategies["dG"] -= 0.05

        # 开发者：追求T和I，反对G
        if self.vars.T < 0.7:
            strategies["dT"] += 0.2
        if self.vars.G > 0.3:
            strategies["dG"] -= 0.15
        if self.vars.I < 0.5:
            strategies["dC"] += 0.05

        # 社会：追求T和S，反对R
        if self.vars.T < 0.6:
            strategies["dT"] += 0.2
        if self.vars.R > 0.4:
            strategies["dG"] += 0.1

        # 限幅
        for k in strategies:
            strategies[k] = clamp(strategies[k], -0.3, 0.3)

        return strategies

    def step(self) -> Dict:
        """执行一步博弈"""
        self.current_step += 1

        # 计算当前效用
        for player in self.players:
            player.compute_utility(self.vars)

        # 制定策略
        strategies = self._compute_strategies()

        # 更新变量
        self._update_variables(strategies)

        # 记录历史
        eq = GovernanceFormulas.detect_equilibrium(
            self.vars.C, self.vars.T, self.vars.S
        )
        record = {
            "step": self.current_step,
            **self.vars.to_dict(),
            "utilities": {p.name: round(p.utility, 4) for p in self.players},
            "strategies": strategies,
            "equilibrium": eq
        }
        self.history.append(record)

        if eq["type"] not in ["TRANSITION"]:
            self.equilibrium_history.append({
                "step": self.current_step,
                "type": eq["type"],
                "name": eq["name"],
                "C": self.vars.C,
                "T": self.vars.T,
                "S": self.vars.S
            })

        return record

    def run(self, steps: int = None) -> List[Dict]:
        """运行模拟"""
        steps = steps or self.config.get("default_steps", 60)
        for _ in range(steps):
            self.step()
        return self.history

    def get_final_state(self) -> Dict:
        """获取最终状态"""
        final = self.history[-1] if self.history else {}
        return {
            "step": self.current_step,
            "variables": self.vars.to_dict(),
            "equilibrium": GovernanceFormulas.detect_equilibrium(
                self.vars.C, self.vars.T, self.vars.S
            ),
            "utilities": {p.name: round(p.utility, 4) for p in self.players}
        }

    def get_dataframe(self) -> pd.DataFrame:
        """获取历史数据为DataFrame"""
        df = pd.DataFrame(self.history)
        return df

    def export_json(self, filepath: str = None) -> str:
        """导出JSON报告"""
        filepath = filepath or str(OUTPUT_DIR / f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        report = {
            "meta": {
                "dna": DNA,
                "confirm": CONFIRM,
                "gpg": GPG_FINGERPRINT,
                "timestamp": now_iso(),
                "steps": self.current_step,
                "config": self.config
            },
            "final_state": self.get_final_state(),
            "history": self.history,
            "equilibrium_history": self.equilibrium_history
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        return filepath

# ============================================================
# 5. 推演场景预设
# ============================================================

class ScenarioPresets:
    """三组预设推演场景"""

    @staticmethod
    def scenario_A() -> GovernanceVariables:
        """场景A：高集中+低透明（现状延续）"""
        return GovernanceVariables(C=0.85, T=0.15, R=0.82, G=0.20, I=0.60, S=0.28)

    @staticmethod
    def scenario_B() -> GovernanceVariables:
        """场景B：中集中+中透明（过渡状态）"""
        return GovernanceVariables(C=0.55, T=0.55, R=0.45, G=0.45, I=0.50, S=0.62)

    @staticmethod
    def scenario_C() -> GovernanceVariables:
        """场景C：可验证集中+高透明（目标状态）"""
        return GovernanceVariables(C=0.75, T=0.90, R=0.25, G=0.40, I=0.70, S=0.88)

    @staticmethod
    def apply_scenario(sim: AIGovernanceSimulator, scenario: str):
        """应用预设场景到模拟器"""
        scenarios = {
            "A": ScenarioPresets.scenario_A,
            "B": ScenarioPresets.scenario_B,
            "C": ScenarioPresets.scenario_C,
        }
        if scenario.upper() in scenarios:
            sim.vars = scenarios[scenario.upper()]()
            sim._init_history()
        return sim

# ============================================================
# 6. 龍魂系统审计协议模拟
# ============================================================

@dataclass
class AuditRecord:
    """审计记录"""
    audit_id: str
    timestamp: str
    system: str
    module: str
    decision_id: str
    inputs: Dict
    outputs: Dict
    audit_trail: Dict
    verification_status: Dict
    dna: str = field(default_factory=lambda: generate_sub_dna("AUDIT"))

    def to_dict(self) -> Dict:
        return {
            "audit_id": self.audit_id,
            "timestamp": self.timestamp,
            "system": self.system,
            "module": self.module,
            "decision_id": self.decision_id,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "audit_trail": self.audit_trail,
            "verification_status": self.verification_status,
            "dna": self.dna
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

class AuditProtocol:
    """龍魂系统开放审计协议"""

    def __init__(self):
        self.audit_log: List[AuditRecord] = []
        self.node_count = 5
        self.consensus_threshold = 0.7

    def audit_decision(self, decision_id: str, inputs: Dict,
                       outputs: Dict, context: Dict = None) -> AuditRecord:
        """审计一个决策"""
        audit_id = f"AUDIT-{datetime.now().strftime('%Y%m%d')}-{len(self.audit_log)+1:04d}"

        # 计算审计哈希
        data_str = f"{decision_id}{json.dumps(inputs, sort_keys=True)}{json.dumps(outputs, sort_keys=True)}{now_iso()}"
        audit_hash = sha256_hex(data_str)

        # 模拟多节点验证
        consensus_reached = self._simulate_consensus(inputs, outputs)

        record = AuditRecord(
            audit_id=audit_id,
            timestamp=now_iso(),
            system="龍魂系统 v4.0",
            module="开放审计协议",
            decision_id=decision_id,
            inputs=inputs,
            outputs=outputs,
            audit_trail={
                "hash": audit_hash[:16],
                "prev_hash": self.audit_log[-1].audit_trail["hash"][:16] if self.audit_log else "0" * 16,
                "timestamp": now_iso(),
                "full_hash": audit_hash
            },
            verification_status={
                "node_count": self.node_count,
                "consensus_reached": consensus_reached,
                "discrepancies": [] if consensus_reached else ["节点2报告异常"],
                "confidence": round(0.85 + 0.15 * self._simulate_confidence(), 3)
            }
        )
        self.audit_log.append(record)
        return record

    def _simulate_consensus(self, inputs: Dict, outputs: Dict) -> bool:
        """模拟多节点共识"""
        # 基于输入输出的复杂度模拟共识达成概率
        complexity = len(inputs) + len(outputs)
        base_prob = 0.85
        if complexity > 10:
            base_prob -= 0.10
        if outputs.get("confidence", 0.5) < 0.6:
            base_prob -= 0.10
        return np.random.random() < base_prob

    def _simulate_confidence(self) -> float:
        """模拟置信度"""
        return 0.75 + 0.20 * np.random.random()

    def get_statistics(self) -> Dict:
        """获取审计统计"""
        total = len(self.audit_log)
        if total == 0:
            return {"total": 0, "consensus_rate": 0, "avg_confidence": 0}

        consensus_count = sum(1 for r in self.audit_log if r.verification_status["consensus_reached"])
        avg_conf = sum(r.verification_status["confidence"] for r in self.audit_log) / total

        return {
            "total": total,
            "consensus_rate": round(consensus_count / total, 3),
            "avg_confidence": round(avg_conf, 3)
        }

# ============================================================
# 7. 易经隐喻映射
# ============================================================

class IChingMetaphor:
    """易经隐喻映射层"""

    HEXAGRAM_MAP = {
        "乾": {"symbol": "䷀", "meaning": "天行健，自强不息", "modern": "创新驱动力"},
        "坤": {"symbol": "䷁", "meaning": "地势坤，厚德载物", "modern": "治理承载力"},
        "既济": {"symbol": "䷾", "meaning": "水在火上，事已成", "modern": "技术成熟阶段"},
        "未济": {"symbol": "䷿", "meaning": "火在水上，事未成", "modern": "风险未平衡阶段"},
        "否": {"symbol": "䷋", "meaning": "天地不交", "modern": "结构阻滞"},
        "泰": {"symbol": "䷊", "meaning": "天地交泰", "modern": "系统协同"},
        "革": {"symbol": "䷰", "meaning": "变革", "modern": "技术变革"},
        "鼎": {"symbol": "䷱", "meaning": "鼎新", "modern": "治理重构"},
    }

    @staticmethod
    def map_state(vars: GovernanceVariables) -> Dict:
        """将当前状态映射到易经卦象"""
        C, T, S = vars.C, vars.T, vars.S

        if S > 0.70 and T > 0.70:
            return {
                "primary": "既济",
                "symbol": "䷾",
                "message": "技术已强，治理已稳 — 既济之象",
                "phase": "有序"
            }
        elif S < 0.40 and T < 0.30:
            return {
                "primary": "未济",
                "symbol": "䷿",
                "message": "技术已强，治理未稳 — 未济之象",
                "phase": "混乱"
            }
        elif C > 0.70 and T < 0.40:
            return {
                "primary": "否",
                "symbol": "䷋",
                "message": "结构阻滞，沟通不畅 — 否之象",
                "phase": "阻滞"
            }
        elif T > 0.60 and C < 0.60:
            return {
                "primary": "泰",
                "symbol": "䷊",
                "message": "天地交泰，系统协同 — 泰之象",
                "phase": "协同"
            }
        elif T > 0.40 and S > 0.50:
            return {
                "primary": "鼎",
                "symbol": "䷱",
                "message": "鼎新革故，治理重构 — 鼎之象",
                "phase": "重构"
            }
        else:
            return {
                "primary": "革",
                "symbol": "䷰",
                "message": "变革之际，转型之中 — 革之象",
                "phase": "变革"
            }

    @staticmethod
    def get_transition_path() -> Dict:
        """未济→既济的转化路径"""
        return {
            "from": "未济 (䷿)",
            "to": "既济 (䷾)",
            "conditions": [
                "各方认识到重复博弈的利益 (δ > δ*)",
                "建立可验证审计协议 (技术条件)",
                "降低透明度成本 (经济条件)",
                "形成多边协调机制 (政治条件)"
            ],
            "stages": [
                {"stage": 1, "name": "风险暴露", "description": "技术能力集中，风险显现"},
                {"stage": 2, "name": "治理博弈", "description": "各方在透明与封闭间博弈"},
                {"stage": 3, "name": "均衡达成", "description": "透明度成为理性选择，系统稳定"}
            ],
            "metaphor": "未济之时，火在水上，未能相济；既济之时，水在火上，相得益彰。AI治理之道，亦如是。"
        }

# ============================================================
# 8. 可视化引擎
# ============================================================

class VisualizationEngine:
    """可视化引擎"""

    @staticmethod
    def plot_3d_model(df: pd.DataFrame, save_path: str = None) -> plt.Figure:
        """三轴图：C, T, S"""
        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection='3d')

        # 轨迹
        ax.plot(df['C'], df['T'], df['S'],
                linewidth=2.5, color='blue', label='演化轨迹', alpha=0.8)

        # 起点和终点
        ax.scatter(df['C'].iloc[0], df['T'].iloc[0], df['S'].iloc[0],
                   color='green', s=120, marker='o', label='起点', edgecolors='black', linewidth=1)
        ax.scatter(df['C'].iloc[-1], df['T'].iloc[-1], df['S'].iloc[-1],
                   color='red', s=150, marker='*', label='终点', edgecolors='black', linewidth=1)

        # 标注区域
        ax.text(0.85, 0.15, 0.30, '⚠️ 高集中+低透明\n(不稳定)', color='red', fontsize=11, ha='center', fontweight='bold')
        ax.text(0.55, 0.55, 0.62, '🟡 中集中+中透明\n(主流)', color='orange', fontsize=11, ha='center', fontweight='bold')
        ax.text(0.75, 0.85, 0.88, '⭐ 可验证集中+高透明\n(目标)', color='green', fontsize=11, ha='center', fontweight='bold')

        # 高亮目标区域
        ax.scatter([0.75], [0.85], [0.88], color='gold', s=300, alpha=0.3, marker='*')
        ax.scatter([0.75], [0.85], [0.88], color='gold', s=100, alpha=0.6, marker='*')

        ax.set_xlabel('技术集中度 C', fontsize=12, fontweight='bold')
        ax.set_ylabel('透明度 T', fontsize=12, fontweight='bold')
        ax.set_zlabel('系统稳定性 S', fontsize=12, fontweight='bold')
        ax.set_title('AI治理博弈三轴模型', fontsize=16, fontweight='bold')
        ax.legend(loc='upper left', fontsize=11)
        ax.view_init(elev=25, azim=-45)

        if save_path:
            plt.savefig(save_path, dpi=200, bbox_inches='tight')
        return fig

    @staticmethod
    def plot_trajectory(df: pd.DataFrame, save_path: str = None) -> plt.Figure:
        """时间序列轨迹"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))

        # 子图1：核心变量
        ax1 = axes[0, 0]
        ax1.plot(df['step'], df['C'], label='C (集中度)', linewidth=2, color='#1f77b4')
        ax1.plot(df['step'], df['T'], label='T (透明度)', linewidth=2, color='#2ca02c')
        ax1.plot(df['step'], df['R'], label='R (风险)', linewidth=2, color='#d62728')
        ax1.axhline(y=0.70, color='gray', linestyle='--', alpha=0.5, label='C阈值=0.70')
        ax1.axhline(y=0.60, color='gray', linestyle=':', alpha=0.5, label='T阈值=0.60')
        ax1.set_xlabel('步数', fontsize=11)
        ax1.set_ylabel('值', fontsize=11)
        ax1.set_title('核心变量演化', fontsize=13, fontweight='bold')
        ax1.legend(loc='best')
        ax1.grid(True, alpha=0.3)

        # 子图2：治理与创新
        ax2 = axes[0, 1]
        ax2.plot(df['step'], df['G'], label='G (治理强度)', linewidth=2, color='#ff7f0e')
        ax2.plot(df['step'], df['I'], label='I (创新速度)', linewidth=2, color='#9467bd')
        ax2.set_xlabel('步数', fontsize=11)
        ax2.set_ylabel('值', fontsize=11)
        ax2.set_title('治理与创新', fontsize=13, fontweight='bold')
        ax2.legend(loc='best')
        ax2.grid(True, alpha=0.3)

        # 子图3：系统稳定性
        ax3 = axes[1, 0]
        ax3.plot(df['step'], df['S'], label='S (稳定性)', linewidth=2.5, color='purple')
        ax3.fill_between(df['step'], 0, df['S'], alpha=0.25, color='purple')
        ax3.axhline(y=0.50, color='gray', linestyle='--', alpha=0.5, label='中等稳定')
        ax3.set_xlabel('步数', fontsize=11)
        ax3.set_ylabel('值', fontsize=11)
        ax3.set_title('系统稳定性演化', fontsize=13, fontweight='bold')
        ax3.legend(loc='best')
        ax3.grid(True, alpha=0.3)

        # 子图4：各主体效用
        ax4 = axes[1, 1]
        utils = df['utilities'].apply(pd.Series)
        for col in utils.columns:
            ax4.plot(df['step'], utils[col], label=col, linewidth=1.8, alpha=0.75)
        ax4.set_xlabel('步数', fontsize=11)
        ax4.set_ylabel('效用', fontsize=11)
        ax4.set_title('各主体效用演化', fontsize=13, fontweight='bold')
        ax4.legend(loc='best', fontsize=9)
        ax4.grid(True, alpha=0.3)

        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=200, bbox_inches='tight')
        return fig

    @staticmethod
    def plot_equilibrium_map(df: pd.DataFrame, save_path: str = None) -> plt.Figure:
        """均衡状态图（C-T平面）"""
        fig, ax = plt.subplots(figsize=(12, 9))

        # 生成热力图
        C_vals = np.linspace(0, 1, 100)
        T_vals = np.linspace(0, 1, 100)
        C_grid, T_grid = np.meshgrid(C_vals, T_vals)

        # 计算稳定性
        R_grid = 1 - np.exp(-CONFIG["risk_sensitivity_lambda"] * C_grid**2)
        I_grid = 0.5 * (0.6 * np.exp(-CONFIG["governance_innovation_eta"] * 0.3) +
                        0.6 * (1 + CONFIG["transparency_innovation_xi"] * T_grid -
                               CONFIG["concentration_innovation_rho"] * C_grid))
        S_grid = (CONFIG["stability_alpha"] * T_grid -
                  CONFIG["stability_beta"] * C_grid**2 +
                  CONFIG["stability_gamma"] * I_grid -
                  CONFIG["stability_delta"] * R_grid)
        S_grid = np.clip(S_grid, 0, 1)

        contour = ax.contourf(C_grid, T_grid, S_grid, levels=25, cmap='RdYlGn', alpha=0.85)
        cbar = plt.colorbar(contour, ax=ax, label='稳定性 S', shrink=0.8)
        cbar.ax.tick_params(labelsize=10)

        # 标注区域
        ax.text(0.85, 0.15, '🔴 不稳定区\n高集中+低透明',
                fontsize=12, color='darkred', ha='center', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
        ax.text(0.55, 0.55, '🟡 过渡区\n中集中+中透明',
                fontsize=12, color='darkorange', ha='center', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
        ax.text(0.75, 0.88, '⭐ 目标区\n可验证集中+高透明',
                fontsize=12, color='darkgreen', ha='center', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

        # 绘制轨迹
        ax.plot(df['C'], df['T'], 'b-', linewidth=2.5, alpha=0.8, label='演化路径')
        ax.scatter(df['C'].iloc[0], df['T'].iloc[0], color='blue', s=120, marker='o',
                   edgecolors='black', linewidth=1.5, label='起点', zorder=5)
        ax.scatter(df['C'].iloc[-1], df['T'].iloc[-1], color='red', s=150, marker='*',
                   edgecolors='black', linewidth=1.5, label='终点', zorder=5)

        ax.set_xlabel('技术集中度 C', fontsize=13, fontweight='bold')
        ax.set_ylabel('透明度 T', fontsize=13, fontweight='bold')
        ax.set_title('均衡状态图（C-T平面）', fontsize=16, fontweight='bold')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.legend(loc='upper left', fontsize=11)
        ax.grid(True, alpha=0.2)

        if save_path:
            plt.savefig(save_path, dpi=200, bbox_inches='tight')
        return fig

# ============================================================
# 9. 主引擎
# ============================================================

class OpenAuditEngine:
    """开放审计主引擎"""

    def __init__(self):
        self.sim = AIGovernanceSimulator()
        self.audit = AuditProtocol()
        self.iching = IChingMetaphor()
        self.visual = VisualizationEngine()
        self.results: Dict = {}

    def run_simulation(self, steps: int = None, scenario: str = None) -> Dict:
        """运行完整模拟"""
        steps = steps or CONFIG["default_steps"]

        # 应用场景
        if scenario:
            ScenarioPresets.apply_scenario(self.sim, scenario)

        # 运行模拟
        self.sim.run(steps)

        # 生成审计记录
        for i in range(min(5, len(self.sim.history))):
            record = self.sim.history[i * max(1, len(self.sim.history)//5)]
            self.audit.audit_decision(
                decision_id=f"SIM-{i}",
                inputs={"step": record["step"], "C": record["C"], "T": record["T"]},
                outputs={"R": record["R"], "S": record["S"], "I": record["I"]},
                context={"scenario": scenario or "default"}
            )

        # 收集结果
        final = self.sim.get_final_state()
        df = self.sim.get_dataframe()

        self.results = {
            "simulation": {
                "steps": self.sim.current_step,
                "final_state": final,
                "equilibrium_history": self.sim.equilibrium_history
            },
            "audit": self.audit.get_statistics(),
            "iching": self.iching.map_state(self.sim.vars),
            "dataframe": df
        }

        return self.results

    def generate_report(self, format: str = "json") -> str:
        """生成报告"""
        if format == "json":
            return self._export_json()
        elif format == "md":
            return self._export_markdown()
        else:
            raise ValueError(f"不支持的格式: {format}")

    def _export_json(self) -> str:
        """导出JSON报告"""
        report = {
            "meta": {
                "dna": DNA,
                "confirm": CONFIRM,
                "gpg": GPG_FINGERPRINT,
                "timestamp": now_iso(),
                "engine_version": "v2.0"
            },
            "simulation": {
                "steps": self.sim.current_step,
                "final_state": self.sim.get_final_state(),
                "equilibrium_history": self.sim.equilibrium_history
            },
            "audit": self.audit.get_statistics(),
            "iching": self.iching.map_state(self.sim.vars),
            "transition_path": self.iching.get_transition_path()
        }
        filepath = OUTPUT_DIR / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        return str(filepath)

    def _export_markdown(self) -> str:
        """导出Markdown报告"""
        final = self.sim.get_final_state()
        eq = final["equilibrium"]
        iching = self.iching.map_state(self.sim.vars)

        lines = [
            "# 🔐 开放审计协议推演报告",
            "",
            f"**DNA追溯码**: `{DNA}`",
            f"**确认码**: `{CONFIRM}`",
            f"**生成时间**: {now_iso()}",
            "",
            "## 📊 推演结果",
            "",
            f"| 变量 | 值 |",
            "|------|-----|",
            f"| 技术集中度 C | {self.sim.vars.C:.3f} |",
            f"| 透明度 T | {self.sim.vars.T:.3f} |",
            f"| 风险外部性 R | {self.sim.vars.R:.3f} |",
            f"| 治理强度 G | {self.sim.vars.G:.3f} |",
            f"| 创新速度 I | {self.sim.vars.I:.3f} |",
            f"| 系统稳定性 S | {self.sim.vars.S:.3f} |",
            "",
            f"## 🏛️ 均衡状态",
            "",
            f"**类型**: {eq['type']} - {eq['name']}",
            f"**描述**: {eq['description']}",
            f"**稳定性**: {eq['stability']}",
            "",
            f"## 🧬 易经隐喻",
            "",
            f"**主卦**: {iching['primary']} ({iching['symbol']})",
            f"**状态**: {iching['phase']}",
            f"**信息**: {iching['message']}",
            "",
            "## 📈 可视化输出",
            "",
            "- `3d_model.png`: 三轴模型图",
            "- `trajectory.png`: 时间序列轨迹",
            "- `equilibrium_map.png`: 均衡状态图",
            "",
            "---",
            f"*报告由 OpenAuditEngine v2.0 生成*"
        ]

        filepath = OUTPUT_DIR / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        return str(filepath)

    def plot_all(self, base_name: str = None) -> List[str]:
        """生成所有图表"""
        base_name = base_name or f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        df = self.sim.get_dataframe()
        files = []

        # 三轴图
        path1 = OUTPUT_DIR / f"{base_name}_3d.png"
        self.visual.plot_3d_model(df, str(path1))
        files.append(str(path1))

        # 轨迹图
        path2 = OUTPUT_DIR / f"{base_name}_trajectory.png"
        self.visual.plot_trajectory(df, str(path2))
        files.append(str(path2))

        # 均衡地图
        path3 = OUTPUT_DIR / f"{base_name}_equilibrium.png"
        self.visual.plot_equilibrium_map(df, str(path3))
        files.append(str(path3))

        return files

# ============================================================
# 10. 命令行接口
# ============================================================

def generate_gpg_signature(filepath: str) -> str:
    """生成GPG签名（模拟）"""
    # 实际环境应调用: gpg --detach-sign --armor <file>
    sig_path = f"{filepath}.asc"
    with open(filepath, 'rb') as f:
        content = f.read()
    sig = hashlib.sha256(content).hexdigest()
    with open(sig_path, 'w') as f:
        f.write(f"-----BEGIN PGP SIGNATURE-----\n")
        f.write(f"Version: 龍魂系统 GPG v1.0\n\n")
        f.write(f"SHA256: {sig}\n")
        f.write(f"Fingerprint: {GPG_FINGERPRINT}\n")
        f.write(f"-----END PGP SIGNATURE-----\n")
    return sig_path

def main():
    parser = argparse.ArgumentParser(
        description="🔐 多方主权下的AI开放审计模型 - 推演引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_open_audit_engine.py --run
  python3 bin/lh_open_audit_engine.py --run --steps 80 --scenario C --plot
  python3 bin/lh_open_audit_engine.py --export --format json
  python3 bin/lh_open_audit_engine.py --info
  python3 bin/lh_open_audit_engine.py --audit-log
        """
    )

    parser.add_argument("--run", action="store_true", help="运行模拟")
    parser.add_argument("--steps", type=int, default=60, help="模拟步数（默认60）")
    parser.add_argument("--scenario", type=str, choices=['A', 'B', 'C'],
                        help="预设场景: A=高集中低透明, B=中集中中透明, C=可验证集中高透明")
    parser.add_argument("--plot", action="store_true", help="生成可视化图表")
    parser.add_argument("--export", action="store_true", help="导出报告")
    parser.add_argument("--format", type=str, default="json", choices=['json', 'md'],
                        help="报告格式（默认json）")
    parser.add_argument("--info", action="store_true", help="显示模型信息")
    parser.add_argument("--verify", action="store_true", help="验证GPG签名（说明）")
    parser.add_argument("--audit-log", action="store_true", help="显示审计日志统计演示")

    args = parser.parse_args()

    if args.info:
        print("""
🔐 多方主权下的AI开放审计模型 v2.0

DNA: """ + DNA + """

【核心公式】
  R = 1 - exp(-λ·C²)
  I = 0.5·I₀·exp(-η·G) + 0.5·I₀·(1 + ξ·T - ρ·C)
  S = α·T - β·C² + γ·I - δ·R
  δ* = (u_defect - u_coop) / (u_defect - u_punish)

【三种均衡】
  A: 高集中+低透明 (不稳定·🔴)
  B: 中集中+中透明 (当前主流·🟡)
  C: 可验证集中+高透明 (目标·🟢)

【五类主体】
  国家、企业、监管机构、开发者社区、用户社会

【配套白皮书】
  01_protocols/LH-OPEN-AUDIT-WHITEPAPER-v2.0.md

【使用方法】
  python3 bin/lh_open_audit_engine.py --run --steps 80
  python3 bin/lh_open_audit_engine.py --run --scenario C --plot
  python3 bin/lh_open_audit_engine.py --export --format md
        """)
        return

    if args.verify:
        print("🔐 GPG签名验证")
        print(f"  指纹: {GPG_FINGERPRINT}")
        print("  验证方式: 请使用 `gpg --verify` 对输出文件进行验证")
        print("  或使用 `python3 bin/lh_gpg_sign.py scan open_audit_output/`")
        return

    if args.audit_log:
        # 快速审计演示
        audit = AuditProtocol()
        for i in range(5):
            audit.audit_decision(
                decision_id=f"DEMO-{i}",
                inputs={"param": i, "time": now_iso()},
                outputs={"result": i * 2, "confidence": 0.7 + 0.05 * i}
            )
        stats = audit.get_statistics()
        print("📋 审计日志统计")
        print(f"  总审计数: {stats['total']}")
        print(f"  共识达成率: {stats['consensus_rate']*100:.1f}%")
        print(f"  平均置信度: {stats['avg_confidence']:.2f}")
        return

    if args.run:
        print("=" * 70)
        print("🔐 开放审计协议推演引擎 v2.0")
        print(f"DNA: {DNA}")
        print("=" * 70)

        engine = OpenAuditEngine()

        print(f"\n🔄 运行模拟: {args.steps} 步")
        if args.scenario:
            print(f"  预设场景: {args.scenario}")

        engine.run_simulation(steps=args.steps, scenario=args.scenario)

        # 输出结果
        final = engine.sim.get_final_state()
        eq = final["equilibrium"]
        iching = engine.iching.map_state(engine.sim.vars)

        print("\n📊 最终状态:")
        print(f"  C (集中度) = {engine.sim.vars.C:.3f}")
        print(f"  T (透明度) = {engine.sim.vars.T:.3f}")
        print(f"  R (风险)   = {engine.sim.vars.R:.3f}")
        print(f"  G (治理)   = {engine.sim.vars.G:.3f}")
        print(f"  I (创新)   = {engine.sim.vars.I:.3f}")
        print(f"  S (稳定)   = {engine.sim.vars.S:.3f}")

        print(f"\n🏛️ 均衡状态: {eq['type']} - {eq['name']}")
        print(f"   {eq['description']}")
        print(f"   稳定性: {eq['stability']}")

        print(f"\n🧬 易经隐喻: {iching['primary']} ({iching['symbol']})")
        print(f"   {iching['message']}")

        # 审计统计
        stats = engine.audit.get_statistics()
        print(f"\n📋 审计协议统计:")
        print(f"   审计记录数: {stats['total']}")
        print(f"   共识达成率: {stats['consensus_rate']*100:.1f}%")
        print(f"   平均置信度: {stats['avg_confidence']:.2f}")

        # 导出
        if args.export:
            report_path = engine.generate_report(args.format)
            print(f"\n💾 报告已导出: {report_path}")

        # 可视化
        if args.plot:
            print("\n📈 生成可视化图表...")
            try:
                files = engine.plot_all()
                for f in files:
                    print(f"   ✅ {f}")

                # 生成GPG签名
                for f in files:
                    sig_path = generate_gpg_signature(f)
                    print(f"   🔐 {sig_path}")
            except Exception as e:
                print(f"   ⚠️ 图表生成失败: {e}")
                print("   (如无GUI环境，图表可能无法生成，报告数据不受影响)")

        print("\n✅ 推演完成！")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
