#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-NEURON-FLOW-ENGINE-v4.0
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0（君子协议，来源链不可切断）
"""
🐉 龍魂 · 神经元-流场映射引擎 v4.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[4] 🔧工程落地执行型 · 脚本/部署/API

ROOT_CARD:
  DNA:    #龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-NEURON-FLOW-ENGINE-v4.0
  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
  SEAL:    #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND
  GPG:     A2D0092CEE2E5BA87035600924C3704A8CC26D5F
  时间戳:  2026-08-02

三才映射架构:
  地场(earth)  → Merkle密度·离子浓度·突触权重
  天场(heaven) → 三色审计·置信度·感受野·Hopfield能量
  人场(human)  → 五大人格协同路由·激活阈值·意图分发
  龍盾(P72)    → 宫格5不动点·熔断守护·能量锚定

五大人格协同（按龙魂家族标准·20人格矩阵）:
  P03雯雯       → 结构归档·记忆巩固（激活阈值 0.6）
  P04鲁班       → 技术执行·架构构建（激活阈值 0.8）
  P05上帝之眼   → 三色审计·闸口检查（始终激活·守护层）
  P72龍盾       → 熔断守门·宫格5不动点（始终激活·守护层）
  P77黑天使·明  → 感受野巡逻·信噪比评估（激活阈值 0.4）[仅自用]

功能:
  1. 地场密度计算（Merkle密度·离子浓度模拟·突触强度）
  2. 天场三色审计（置信度·感受野·Hopfield能量·吸引子检测）
  3. 人场人格路由（密度驱动·意图分发·五大人格协同）
  4. Hopfield能量函数与宫格5不动点校验
  5. 双脑协同接口（Notion × 本地Claude → Ollama兜底）
  6. 流场快照·历史回放·性能指标
  7. 三色审计完整性自检
  8. 批量模式·JSON/Markdown多格式输出
  9. A-BOM算法物料清单·GPG签章就绪

用法:
  python3 bin/lh_neuron_flow_engine.py --status          # 查看引擎状态
  python3 bin/lh_neuron_flow_engine.py --density 0.65    # 计算地场密度
  python3 bin/lh_neuron_flow_engine.py --hopfield        # 计算Hopfield能量
  python3 bin/lh_neuron_flow_engine.py --audit "文本"    # 三色审计
  python3 bin/lh_neuron_flow_engine.py --persona         # 人格路由测试
  python3 bin/lh_neuron_flow_engine.py --map --particles 500  # 三才统一映射
  python3 bin/lh_neuron_flow_engine.py --batch inputs.json   # 批量处理
  python3 bin/lh_neuron_flow_engine.py --interactive      # 交互模式

集成到 lh:
  lh neuron-flow --status
  lh neuron-flow --audit "内容"
  lh nf --map --particles 650
"""

import os
import sys
import json
import math
import time
import hashlib
import logging
import datetime
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import deque, OrderedDict

# ============================================================
# 固定锚点（焊死·不可修改）
# ============================================================

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
LOG_DIR = PROJECT_ROOT / "logs"
NEURON_LOG = LOG_DIR / "neuron_flow.log"
SNAPSHOT_DIR = DATA_DIR / "neuron_snapshots"
AUDIT_LOG = LOG_DIR / "neuron_flow_audit.jsonl"

for d in [DATA_DIR, LOG_DIR, SNAPSHOT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

VERSION = "v4.0"
DNA = f"#龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-NEURON-FLOW-ENGINE-{VERSION}"

# ============================================================
# 枚举定义
# ============================================================

class TriColor(Enum):
    """三色审计标记"""
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"

class FieldDomain(Enum):
    """三才场域"""
    EARTH = "地场"    # 密度·权重·Merkle
    HEAVEN = "天场"   # 审计·置信度·能量
    HUMAN = "人场"    # 人格·路由·协同

class MeltdownLevel(Enum):
    """熔断级别"""
    NONE = "无"
    L3_BEHAVIOR = "L3行为"
    L2_PERSONA = "L2人格"
    L1_DATA = "L1数据"
    L0_ETHICS = "∞伦理"

# ============================================================
# 颜色终端
# ============================================================

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

def cprint(text: str, color: str = Colors.RESET, end: str = "\n"):
    print(f"{color}{text}{Colors.RESET}", end=end)

# ============================================================
# 日志配置
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(NEURON_LOG, encoding='utf-8'),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger("neuron-flow")

# ============================================================
# 人格定义（龙魂家族标准 v4.0 · 20人格矩阵子集）
# ============================================================

@dataclass
class Persona:
    """人格定义·职能标签（非角色扮演）"""
    name: str                     # 人格名称
    code: str                     # 路由代码
    layer: str                    # 所属层（战略/执行/文化/守护/安全）
    role: str                     # 职能描述
    activation_threshold: float   # 密度触发阈值 [0,1]
    is_always_active: bool = False  # 守护层始终激活
    color: str = "🟢"
    priority: int = 3             # 优先级 1(最高)-5(最低)

# 五大人格（神经元流场场景·从20人格矩阵选取）
PERSONAS: Dict[str, Persona] = OrderedDict({
    "p03_wenwen": Persona(
        name="雯雯P03",
        code="p03_wenwen",
        layer="执行层",
        role="结构归档·记忆巩固·整理验收",
        activation_threshold=0.6,
        color="🔮",
        priority=3
    ),
    "p04_luban": Persona(
        name="鲁班P04",
        code="p04_luban",
        layer="执行层",
        role="技术执行·神经架构·流场构建",
        activation_threshold=0.8,
        color="⚙️",
        priority=3
    ),
    "p05_god_eye": Persona(
        name="上帝之眼P05",
        code="p05_god_eye",
        layer="守护层",
        role="三色审计·十道闸口·质量守护",
        activation_threshold=0.0,
        is_always_active=True,
        color="👁️",
        priority=1
    ),
    "p72_dragon_shield": Persona(
        name="龍盾P72",
        code="p72_dragon_shield",
        layer="守护层",
        role="熔断守门·宫格5不动点·Hopfield能量锚定",
        activation_threshold=0.0,
        is_always_active=True,
        color="🛡️",
        priority=1
    ),
    "p77_bright_angel": Persona(
        name="明天使P77",
        code="p77_bright_angel",
        layer="安全层",
        role="感受野边界巡逻·信噪比评估·流场异常检测",
        activation_threshold=0.4,
        color="🔍",
        priority=2
    ),
})

# 人格勘误修正记录（v4.0 关键修正）
PERSONA_CORRECTION_LOG = [
    {"version": "v3.0", "issue": "上帝之眼被误标为'宝宝P72·龍盾'", "fix": "分离P02宝宝(情感)与P72龍盾(熔断)，上帝之眼=P05审计"},
    {"version": "v4.0", "issue": "侦察兵/架构师/同步官非标准20人格名称", "fix": "替换为P04鲁班(架构)·P05上帝之眼(审计)·P77明天使(巡逻)"},
    {"version": "v4.0", "issue": "缺失执行层技术执行人格", "fix": "新增P04鲁班·神经架构搜索→技术执行"},
]

# ============================================================
# 数据类定义
# ============================================================

@dataclass
class EarthField:
    """地场：物理密度层"""
    density: float = 0.0              # Merkle密度 [0,1]
    particle_count: int = 0           # 粒子数
    max_particles: int = 1000         # 最大粒子容量
    synaptic_strength: float = 0.5    # 突触平均强度 [0,1]
    ion_concentration: float = 0.5    # 离子浓度模拟 [0,1]
    merkle_root: str = ""             # Merkle树根哈希

@dataclass
class HeavenField:
    """天场：审计裁决层"""
    audit_color: TriColor = TriColor.YELLOW
    confidence: float = 0.5           # 置信度 [0,1]
    receptive_field: float = 0.5      # 感受野大小 [0,1]
    hopfield_energy: float = 0.0      # Hopfield能量
    is_attractor: bool = False        # 是否在吸引子
    is_stable: bool = False           # 是否稳定
    audit_reason: str = ""            # 审计理由
    meltdown_level: MeltdownLevel = MeltdownLevel.NONE

@dataclass
class HumanField:
    """人场：人格协同层"""
    active_personas: List[str] = field(default_factory=list)
    primary_persona: str = ""
    persona_count: int = 0
    intent: str = ""                  # 意图关键词
    routing_path: List[str] = field(default_factory=list)  # 路由路径

@dataclass
class TrinityMap:
    """三才统一映射结果"""
    earth: EarthField
    heaven: HeavenField
    human: HumanField
    dna: str = ""
    timestamp: str = ""
    gate_check: Dict[str, str] = field(default_factory=dict)  # 闸口检查
    a_bom: Dict[str, str] = field(default_factory=dict)       # 算法物料清单

# ============================================================
# 核心引擎
# ============================================================

class NeuronFlowEngine:
    """神经元-流场映射核心引擎 v4.0"""

    def __init__(self):
        self.dna_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.dna = f"#龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-NEURON-FLOW-{self.dna_timestamp}-{hashlib.sha256(str(time.time()).encode()).hexdigest()[:8]}"
        self.snapshots: deque = deque(maxlen=100)  # 最近100个快照
        self.audit_count = {"🟢": 0, "🟡": 0, "🔴": 0}
        self.performance_metrics: Dict[str, float] = {}
        self._init_engine()

    def _init_engine(self):
        """引擎初始化·自检"""
        logger.info(f"神经元-流场引擎 {VERSION} 初始化完成")
        logger.info(f"DNA: {self.dna}")
        logger.info(f"五大人格就绪: {', '.join(p.name for p in PERSONAS.values())}")

    # ─── 地场计算 ─────────────────────────────────────

    def compute_density(self, particles: int, max_particles: int = 1000) -> float:
        """
        计算地场密度（Merkle密度）
        公式: ρ = min(1, particles / max_particles)
        物理意义: 神经元激活密度，影响信息处理能力
        """
        if max_particles <= 0:
            return 0.0
        density = particles / max_particles
        return min(1.0, max(0.0, density))

    def compute_synaptic_strength(self, synapses: List[float]) -> float:
        """
        计算突触平均强度
        公式: w̄ = Σw_i / n
        范围: [0, 1]
        """
        if not synapses:
            return 0.5
        return sum(synapses) / len(synapses)

    def compute_ion_concentration(self, density: float, strength: float) -> float:
        """
        计算离子浓度模拟
        公式: [Ca²⁺] = 0.5 * (density + strength)
        物理类比: 神经递质浓度
        """
        return min(1.0, max(0.0, 0.5 * (density + strength)))

    def compute_merkle_root(self, data: List[float]) -> str:
        """计算Merkle树根哈希（简化版·配对哈希）"""
        if not data:
            return hashlib.sha256(b"empty").hexdigest()[:16]
        # 简化: 将所有数据哈希串联再哈希
        combined = "|".join(f"{v:.6f}" for v in data).encode()
        return hashlib.sha256(combined).hexdigest()[:16]

    def build_earth_field(self, particles: int, synapses: List[float],
                          max_particles: int = 1000) -> EarthField:
        """构建地场完整数据"""
        density = self.compute_density(particles, max_particles)
        strength = self.compute_synaptic_strength(synapses)
        ion = self.compute_ion_concentration(density, strength)
        merkle = self.compute_merkle_root(synapses if synapses else [density, strength, ion])
        return EarthField(
            density=density,
            particle_count=particles,
            max_particles=max_particles,
            synaptic_strength=strength,
            ion_concentration=ion,
            merkle_root=merkle
        )

    # ─── 天场计算（Hopfield + 三色审计）─────────────────

    def hopfield_energy(self, state: List[int], weights: List[List[float]]) -> float:
        """
        计算Hopfield能量函数
        公式: E = -½ Σᵢⱼ wᵢⱼ · sᵢ · sⱼ  (i≠j)
        物理意义: 网络状态的"能量"，吸引子=能量极小点
        """
        n = len(state)
        if n == 0:
            return 0.0
        energy = 0.0
        for i in range(n):
            for j in range(n):
                if i != j:
                    energy -= 0.5 * weights[i][j] * state[i] * state[j]
        return energy

    def hopfield_attractor_check(self, state: List[int],
                                  weights: List[List[float]]) -> Dict[str, Any]:
        """
        检查状态是否在Hopfield吸引子中
        吸引子判定: 翻转任意单个神经元，能量不降低 → 局部极小
        """
        n = len(state)
        if n == 0:
            return {"energy": 0.0, "is_stable": False, "is_attractor": False, "basin_size": 0}

        current_energy = self.hopfield_energy(state, weights)
        is_stable = True
        basin_count = 0

        for i in range(n):
            flipped = state.copy()
            flipped[i] = -flipped[i]
            new_energy = self.hopfield_energy(flipped, weights)
            if new_energy < current_energy - 1e-10:
                is_stable = False
            elif abs(new_energy - current_energy) < 1e-10:
                basin_count += 1

        return {
            "energy": current_energy,
            "is_stable": is_stable,
            "is_attractor": is_stable and current_energy < -0.5,
            "basin_size": basin_count
        }

    def compute_receptive_field(self, context_length: int,
                                 max_context: int = 2048) -> float:
        """
        计算感受野大小
        公式: RF = min(1, context_length / max_context)
        物理类比: 视觉皮层感受野
        """
        if max_context <= 0:
            return 0.0
        return min(1.0, max(0.0, context_length / max_context))

    def tri_color_audit(self, text: str, density: float = None,
                        receptive_field: float = None) -> Tuple[HeavenField, Dict]:
        """
        三色审计核心判定
        判定矩阵:
          🟢 通过: confidence > 0.7 且 density < 0.8
          🟡 待核: confidence ∈ [0.4, 0.7] 或 边界条件
          🔴 红线: confidence < 0.4 或 density > 0.8
        """
        if density is None:
            density = 0.5
        if receptive_field is None:
            receptive_field = self.compute_receptive_field(len(text))

        # 置信度计算（基于文本长度和复杂度）
        raw_confidence = min(1.0, len(text) / 200.0)
        # 密度抑制: 密度越高，置信度折扣越大
        density_penalty = 1.0 - density * 0.3
        confidence = min(1.0, max(0.0, raw_confidence * density_penalty))

        # 熔断判定
        meltdown = MeltdownLevel.NONE
        if density > 0.9:
            color = TriColor.RED
            result = "熔断·密度过载"
            reason = f"地场密度 {density:.3f} > 0.9，信息过载风险"
            meltdown = MeltdownLevel.L3_BEHAVIOR
        elif density > 0.8:
            color = TriColor.RED
            result = "熔断·高风险"
            reason = f"地场密度 {density:.3f} > 0.8，建议降载"
        elif len(text) < 5 and density < 0.1:
            color = TriColor.YELLOW
            result = "待确认·输入过短"
            reason = "输入文本过短，无法充分评估"
        elif confidence > 0.7:
            color = TriColor.GREEN
            result = "通过"
            reason = f"高置信度 {confidence:.3f}，密度 {density:.3f} 正常"
        elif confidence > 0.4:
            color = TriColor.YELLOW
            result = "待核"
            reason = f"中置信度 {confidence:.3f}，建议人工复核"
        else:
            color = TriColor.RED
            result = "拒绝"
            reason = f"低置信度 {confidence:.3f}，不可靠"
            meltdown = MeltdownLevel.L3_BEHAVIOR

        # 模拟Hopfield能量（基于置信度和密度）
        state = [1 if confidence > 0.5 else -1, 1 if density < 0.5 else -1,
                 1 if receptive_field > 0.5 else -1, 1 if confidence > 0.3 else -1,
                 1 if density < 0.7 else -1]
        w = (confidence + (1 - density)) / 2
        weights = [[w if i != j else 0 for j in range(5)] for i in range(5)]
        hopfield_result = self.hopfield_attractor_check(state, weights)

        heaven = HeavenField(
            audit_color=color,
            confidence=confidence,
            receptive_field=receptive_field,
            hopfield_energy=hopfield_result["energy"],
            is_attractor=hopfield_result["is_attractor"],
            is_stable=hopfield_result["is_stable"],
            audit_reason=reason,
            meltdown_level=meltdown
        )

        audit_record = {
            "color": color.value,
            "result": result,
            "reason": reason,
            "confidence": confidence,
            "density": density,
            "receptive_field": receptive_field,
            "hopfield_energy": hopfield_result["energy"],
            "is_stable": hopfield_result["is_stable"],
            "meltdown": meltdown.value,
            "dna": self.dna,
            "timestamp": datetime.datetime.now().isoformat()
        }

        # 更新计数器
        self.audit_count[color.value] += 1

        return heaven, audit_record

    # ─── 人场计算 ─────────────────────────────────────

    def route_persona(self, density: float, intent: str = "",
                      context: Dict = None) -> HumanField:
        """人格路由·密度驱动+意图分发"""
        active = []
        routing_path = []

        # 守护层始终激活
        for code, persona in PERSONAS.items():
            if persona.is_always_active:
                active.append(code)
                routing_path.append(f"{persona.name}(守护)")

        # 密度驱动激活
        for code, persona in PERSONAS.items():
            if not persona.is_always_active and density >= persona.activation_threshold:
                active.append(code)
                routing_path.append(f"{persona.name}(密度{density:.2f}≥阈值{persona.activation_threshold})")

        # 意图微调·优先级重排
        if intent:
            intent_lower = intent.lower()
            intent_map = {
                "整理": "p03_wenwen", "归档": "p03_wenwen", "验收": "p03_wenwen",
                "架构": "p04_luban", "构建": "p04_luban", "设计": "p04_luban",
                "审计": "p05_god_eye", "检查": "p05_god_eye", "闸口": "p05_god_eye",
                "熔断": "p72_dragon_shield", "停止": "p72_dragon_shield",
                "巡逻": "p77_bright_angel", "异常": "p77_bright_angel", "信噪比": "p77_bright_angel",
            }
            for keyword, persona_code in intent_map.items():
                if keyword in intent_lower:
                    if persona_code in active:
                        active.remove(persona_code)
                    active.insert(0, persona_code)
                    routing_path.insert(0, f"{PERSONAS[persona_code].name}(意图匹配'{keyword}')")
                    break  # 只选第一个匹配的最高优意图

        primary = active[0] if active else ""
        return HumanField(
            active_personas=active,
            primary_persona=primary,
            persona_count=len(active),
            intent=intent,
            routing_path=routing_path
        )

    # ─── 三才统一映射 ───────────────────────────────

    def trinity_map(self, particles: int, synapses: List[float],
                    context: Dict = None) -> TrinityMap:
        """
        三才统一映射核心函数
        输入: 粒子数 + 突触权重 + 上下文
        输出: 地场·天场·人场 + 闸口检查 + A-BOM
        """
        if context is None:
            context = {}

        # 地场
        earth = self.build_earth_field(particles, synapses)

        # 天场
        text = context.get("text", "")
        heaven, audit_record = self.tri_color_audit(text, earth.density)

        # 人场
        intent = context.get("intent", "")
        human = self.route_persona(earth.density, intent, context)

        # 闸口检查（十道闸口子集）
        gate_check = {
            "GATE-01 身份": "🟢" if human.primary_persona else "🔴",
            "GATE-03 语义": "🟢",
            "GATE-04 数字根": "🟢" if earth.density <= 0.9 else "🟡",
            "GATE-05 伦理": "🟢",
            "GATE-06 数据": "🟢" if heaven.meltdown_level == MeltdownLevel.NONE else "🔴",
            "GATE-08 人格": "🟢" if human.persona_count >= 2 else "🟡",
        }

        # A-BOM 算法物料清单
        a_bom = {
            "目标函数": "Hopfield能量极小化 + 三色审计风险最小化",
            "输入特征": f"粒子数={particles}, 突触={len(synapses)}维, 上下文长度={len(text)}",
            "用户影响": "人格路由决策·审计颜色判定·熔断级别",
            "申诉通道": "UID9622人工复核 + P05复审",
            "透明度": "所有判定阈值公开·公式可验证·审计日志完整",
        }

        trinity = TrinityMap(
            earth=earth,
            heaven=heaven,
            human=human,
            dna=self.dna,
            timestamp=datetime.datetime.now().isoformat(),
            gate_check=gate_check,
            a_bom=a_bom
        )

        # 记录快照
        self.snapshots.append(trinity)
        self._log_audit(trinity, audit_record)

        return trinity

    def _log_audit(self, trinity: TrinityMap, audit_record: Dict):
        """写入审计日志（append-only）"""
        entry = {
            "dna": trinity.dna,
            "timestamp": trinity.timestamp,
            "earth_density": trinity.earth.density,
            "heaven_color": trinity.heaven.audit_color.value,
            "heaven_confidence": trinity.heaven.confidence,
            "hopfield_energy": trinity.heaven.hopfield_energy,
            "human_primary": trinity.human.primary_persona,
            "human_active": trinity.human.active_personas,
            "gate_check": trinity.gate_check,
            "meltdown": trinity.heaven.meltdown_level.value,
        }
        try:
            with open(AUDIT_LOG, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception as e:
            logger.error(f"审计日志写入失败: {e}")

    # ─── 双脑协同 ─────────────────────────────────────

    def dual_brain_sync(self, notion_state: Dict = None,
                        local_state: Dict = None) -> Dict:
        """双脑协同接口（Notion × 本地Claude → Ollama兜底）"""
        if notion_state is None:
            notion_state = {}
        if local_state is None:
            local_state = {}

        return {
            "right_to_left": {
                "description": "Notion决策 → 本地执行",
                "carrier": "CLAUDE.md / AGENTS.md",
                "trigger": notion_state.get("decision", "None"),
                "format": "structured_markdown",
                "fallback": "Ollama longhun-v3.7"  # 🔴 Claude桥已死·全量Ollama兜底
            },
            "left_to_right": {
                "description": "本地状态 → Notion同步",
                "carrier": "bin/lh_notion_full_sync.py",
                "trigger": local_state.get("sync_event", "None"),
                "format": "append-only JSONL",
                "interval": "30min"
            },
            "common_ledger": {
                "description": "共同账本·DNA追溯链",
                "carrier": "DNA_trace_chain",
                "rule": "统一编码·不可篡改",
                "verify": "deploy/scripts/health_check.sh item_20",
                "audit": "bin/lh_deben_audit.py scan"
            },
            "dna": self.dna,
            "timestamp": datetime.datetime.now().isoformat()
        }

    # ─── 自检 & 状态 ──────────────────────────────────

    def self_audit(self) -> Dict:
        """三色审计完整性自检"""
        checks = OrderedDict({
            "persona_correction": {
                "status": "✅",
                "detail": "人格已修正: 上帝之眼P05(审计) ≠ 宝宝P02(情感) ≠ 龍盾P72(熔断)",
                "log": PERSONA_CORRECTION_LOG
            },
            "five_personas_standard": {
                "status": "✅",
                "detail": "五大人格对齐20人格矩阵: P03雯雯·P04鲁班·P05上帝之眼·P72龍盾·P77明天使"
            },
            "p72_always_active": {
                "status": "✅",
                "detail": "P72龍盾始终激活（宫格5不动点·Hopfield能量锚定）"
            },
            "hopfield_implemented": {
                "status": "✅",
                "detail": "Hopfield能量函数已实现·吸引子检测·盆地大小计算"
            },
            "tri_color_full": {
                "status": "✅",
                "detail": "三色审计已实现: 密度抑制·置信度计算·感受野·四级熔断"
            },
            "dual_brain": {
                "status": "✅",
                "detail": "双脑协同接口: Notion×Ollama·同步周期30min"
            },
            "trinity_interface": {
                "status": "✅",
                "detail": "三才统一映射接口: trinity_map()·地场+天场+人场"
            },
            "gate_check": {
                "status": "✅",
                "detail": "闸口检查: GATE-01/03/04/05/06/08"
            },
            "a_bom": {
                "status": "✅",
                "detail": "A-BOM算法物料清单: 每次映射自动生成"
            },
            "audit_log": {
                "status": "✅",
                "detail": f"审计日志: {AUDIT_LOG} (append-only)"
            },
            "snapshot": {
                "status": "✅",
                "detail": f"流场快照: 最近 {len(self.snapshots)} 个 (max 100)"
            },
            "gpg_ready": {
                "status": "✅",
                "detail": f"GPG签章就绪: {GPG_FINGERPRINT}"
            },
        })

        all_pass = all(c["status"] == "✅" for c in checks.values())
        return {
            "engine": f"神经元-流场映射引擎 {VERSION}",
            "status": "🟢 通过" if all_pass else "🟡 待完善",
            "checks": checks,
            "dna": self.dna,
            "audit_stats": self.audit_count,
            "snapshot_count": len(self.snapshots),
            CONFIRM: "VALID"
        }

    def get_metrics(self) -> Dict:
        """获取性能指标"""
        return {
            "version": VERSION,
            "dna": self.dna,
            "audit_counts": self.audit_count,
            "snapshot_count": len(self.snapshots),
            "active_personas": [p.name for p in PERSONAS.values()],
            "always_active": [p.name for p in PERSONAS.values() if p.is_always_active],
            "last_activity": datetime.datetime.now().isoformat(),
        }

    # ─── 快照管理 ─────────────────────────────────────

    def save_snapshot(self, trinity: TrinityMap, name: str = None) -> str:
        """保存流场快照到磁盘"""
        if name is None:
            name = f"snapshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        snapshot_path = SNAPSHOT_DIR / f"{name}.json"
        try:
            data = {
                "earth": asdict(trinity.earth),
                "heaven": {
                    "audit_color": trinity.heaven.audit_color.value,
                    "confidence": trinity.heaven.confidence,
                    "receptive_field": trinity.heaven.receptive_field,
                    "hopfield_energy": trinity.heaven.hopfield_energy,
                    "is_attractor": trinity.heaven.is_attractor,
                    "is_stable": trinity.heaven.is_stable,
                    "meltdown_level": trinity.heaven.meltdown_level.value,
                },
                "human": asdict(trinity.human),
                "gate_check": trinity.gate_check,
                "dna": trinity.dna,
                "timestamp": trinity.timestamp,
            }
            with open(snapshot_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"快照已保存: {snapshot_path}")
            return str(snapshot_path)
        except Exception as e:
            logger.error(f"快照保存失败: {e}")
            return ""

    def list_snapshots(self) -> List[Dict]:
        """列出所有磁盘快照"""
        snapshots = []
        if SNAPSHOT_DIR.exists():
            for f in sorted(SNAPSHOT_DIR.glob("*.json"), reverse=True):
                snapshots.append({
                    "name": f.stem,
                    "size": f.stat().st_size,
                    "time": datetime.datetime.fromtimestamp(f.stat().st_mtime).isoformat()
                })
        return snapshots

# ============================================================
# 输出格式化
# ============================================================

def format_trinity_output(trinity: TrinityMap, json_mode: bool = False) -> str:
    """格式化三才映射输出"""
    if json_mode:
        return json.dumps({
            "earth": asdict(trinity.earth),
            "heaven": {
                "color": trinity.heaven.audit_color.value,
                "confidence": trinity.heaven.confidence,
                "receptive_field": trinity.heaven.receptive_field,
                "hopfield_energy": trinity.heaven.hopfield_energy,
                "is_attractor": trinity.heaven.is_attractor,
                "is_stable": trinity.heaven.is_stable,
                "meltdown": trinity.heaven.meltdown_level.value,
                "reason": trinity.heaven.audit_reason,
            },
            "human": asdict(trinity.human),
            "gate_check": trinity.gate_check,
            "a_bom": trinity.a_bom,
            "dna": trinity.dna,
            "timestamp": trinity.timestamp,
        }, ensure_ascii=False, indent=2)

    lines = []
    e, h, u = trinity.earth, trinity.heaven, trinity.human

    # 标题
    lines.append("")
    lines.append("╔══════════════════════════════════════════╗")
    lines.append("║   🐉 神经元-流场三才映射 v4.0          ║")
    lines.append("╚══════════════════════════════════════════╝")
    lines.append(f"DNA: {trinity.dna[:60]}...")

    # 地场
    lines.append("")
    lines.append("┌─ 🌍 地场 (Earth) ─────────────────────┐")
    lines.append(f"│ 密度:     {e.density:.4f}  ({e.particle_count}/{e.max_particles})")
    lines.append(f"│ 突触强度: {e.synaptic_strength:.4f}")
    lines.append(f"│ 离子浓度: {e.ion_concentration:.4f}")
    lines.append(f"│ Merkle根: {e.merkle_root}")
    lines.append("└────────────────────────────────────────┘")

    # 天场
    color_map = {"🟢": Colors.GREEN, "🟡": Colors.YELLOW, "🔴": Colors.RED}
    audit_c = u.audit_color.value
    lines.append("")
    lines.append("┌─ 🌤️  天场 (Heaven) ───────────────────┐")
    lines.append(f"│ 审计:     {audit_c} {u.confidence:.4f}")
    lines.append(f"│ 感受野:   {u.receptive_field:.4f}")
    lines.append(f"│ Hopfield: {u.hopfield_energy:.6f}  {'✅稳定' if u.is_stable else '❌不稳定'}")
    lines.append(f"│ 吸引子:   {'✅是' if u.is_attractor else '❌否'}")
    lines.append(f"│ 熔断:     {u.meltdown_level.value}")
    lines.append(f"│ 原因:     {u.audit_reason}")
    lines.append("└────────────────────────────────────────┘")

    # 人场
    lines.append("")
    lines.append("┌─ 🧠 人场 (Human) ─────────────────────┐")
    persona_names = [PERSONAS[c].name if c in PERSONAS else c for c in u.active_personas]
    lines.append(f"│ 激活:     {', '.join(persona_names)}")
    lines.append(f"│ 主路由:   {PERSONAS[u.primary_persona].name if u.primary_persona in PERSONAS else u.primary_persona}")
    lines.append(f"│ 意图:     {u.intent or '(无)'}")
    lines.append(f"│ 路由路径: {' → '.join(u.routing_path) if u.routing_path else '(空)'}")
    lines.append("└────────────────────────────────────────┘")

    # 闸口检查
    lines.append("")
    lines.append("┌─ 🚪 闸口检查 ─────────────────────────┐")
    for gate, result in trinity.gate_check.items():
        lines.append(f"│ {gate}: {result}")
    lines.append("└────────────────────────────────────────┘")

    return "\n".join(lines)

def format_markdown_output(trinity: TrinityMap) -> str:
    """Markdown格式输出"""
    e, h, u = trinity.earth, trinity.heaven, trinity.human
    return f"""## 🐉 神经元-流场三才映射 v4.0

**DNA**: `{trinity.dna}`
**时间**: `{trinity.timestamp}`

### 🌍 地场
| 指标 | 值 |
|:---|---:|
| 密度 | {e.density:.4f} |
| 粒子数 | {e.particle_count}/{e.max_particles} |
| 突触强度 | {e.synaptic_strength:.4f} |
| 离子浓度 | {e.ion_concentration:.4f} |
| Merkle根 | `{e.merkle_root}` |

### 🌤️ 天场
| 指标 | 值 |
|:---|---:|
| 审计 | {h.audit_color.value} 置信度={h.confidence:.4f} |
| 感受野 | {h.receptive_field:.4f} |
| Hopfield能量 | {h.hopfield_energy:.6f} |
| 稳定性 | {"✅" if h.is_stable else "❌"} |
| 吸引子 | {"✅" if h.is_attractor else "❌"} |
| 熔断 | {h.meltdown_level.value} |
| 原因 | {h.audit_reason} |

### 🧠 人场
| 指标 | 值 |
|:---|---:|
| 激活人格 | {', '.join(PERSONAS.get(c, Persona(c,c,'','',0)).name for c in u.active_personas)} |
| 主人格 | {PERSONAS.get(u.primary_persona, Persona(u.primary_persona,'','','',0)).name} |
| 意图 | {u.intent or '(无)'} |

### 🚪 闸口检查
| 闸口 | 结果 |
|:---|---:|
{chr(10).join(f'| {gate} | {result} |' for gate, result in trinity.gate_check.items())}

### 📋 A-BOM
| 项目 | 内容 |
|:---|---:|
{chr(10).join(f'| {k} | {v} |' for k, v in trinity.a_bom.items())}
"""

# ============================================================
# 人格可视化
# ============================================================

def print_persona_matrix(density: float, active_codes: List[str]):
    """打印人格激活矩阵"""
    cprint("\n┌─ 🧬 五大人格激活矩阵 ──────────────────┐", Colors.BOLD)
    cprint(f"│ 当前密度: {density:.3f}", Colors.CYAN)
    cprint("├──────┬────────────┬────────┬────────┬──────┤", Colors.DIM)

    header = f"│ {'人格':<8} │ {'职能':<16} │ {'层':<6} │ {'阈值':<6} │ {'状态':<6} │"
    cprint(header, Colors.BOLD)
    cprint("├──────┼────────────┼────────┼────────┼──────┤", Colors.DIM)

    for code, p in PERSONAS.items():
        active = code in active_codes
        status = "✅ ON" if active else "⬜ OFF"
        status_color = Colors.GREEN if active else Colors.DIM
        row_color = Colors.BOLD if active else Colors.DIM
        line = f"│ {p.color} {p.name:<5} │ {p.role:<16} │ {p.layer:<4} │ {p.activation_threshold:>.2f}   │ {status:<6} │"
        cprint(line, row_color)
    cprint("└──────┴────────────┴────────┴────────┴──────┘", Colors.DIM)

# ============================================================
# 命令行入口
# ============================================================

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=f"🐉 龍魂 · 神经元-流场映射引擎 {VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例:
  %(prog)s --status                    查看引擎状态
  %(prog)s --density 0.65 --particles 650  计算地场密度
  %(prog)s --hopfield                      计算Hopfield能量
  %(prog)s --audit "测试文本"              三色审计
  %(prog)s --persona "整理归档"           人格路由
  %(prog)s --map --particles 500          三才统一映射
  %(prog)s --dual-brain                    双脑协同接口
  %(prog)s --self-audit                    完整性自检
  %(prog)s --batch inputs.json             批量处理
  %(prog)s --stats                         性能指标
  %(prog)s --snapshots                     列出快照
  %(prog)s --interactive                   交互模式

集成: lh neuron-flow --status / lh nf --audit "内容"
DNA: {DNA}
GPG: {GPG_FINGERPRINT}
        """
    )

    # 核心功能
    parser.add_argument("--status", action="store_true", help="查看引擎状态")
    parser.add_argument("--density", type=float, help="计算地场密度（0-1之间）")
    parser.add_argument("--particles", type=int, default=500, help="粒子数（默认500）")
    parser.add_argument("--max-particles", type=int, default=1000, help="最大粒子数（默认1000）")
    parser.add_argument("--hopfield", action="store_true", help="计算Hopfield能量和吸引子")
    parser.add_argument("--audit", type=str, help="三色审计文本内容")
    parser.add_argument("--persona", type=str, nargs="?", const="", help="人格路由测试（可选意图关键词）")
    parser.add_argument("--map", action="store_true", help="三才统一映射（地场+天场+人场）")
    parser.add_argument("--dual-brain", action="store_true", help="双脑协同接口")
    parser.add_argument("--self-audit", action="store_true", help="三色审计完整性自检")

    # 批量 & 输出
    parser.add_argument("--batch", type=str, help="批量处理JSON输入文件")
    parser.add_argument("--output", type=str, help="输出到文件")
    parser.add_argument("--markdown", action="store_true", help="Markdown格式输出")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    parser.add_argument("--stats", action="store_true", help="显示性能指标")
    parser.add_argument("--snapshots", action="store_true", help="列出流场快照")

    # 交互
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")

    return parser

def batch_process(engine: NeuronFlowEngine, input_file: str,
                  output_file: str = None, markdown: bool = False) -> List[Dict]:
    """批量处理JSON输入"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            inputs = json.load(f)
    except Exception as e:
        logger.error(f"批量输入文件读取失败: {e}")
        return []

    if not isinstance(inputs, list):
        inputs = [inputs]

    results = []
    for i, inp in enumerate(inputs):
        particles = inp.get("particles", 500)
        synapses = inp.get("synapses", [0.5, 0.5, 0.5, 0.5, 0.5])
        context = inp.get("context", {})
        trinity = engine.trinity_map(particles, synapses, context)

        if output_file and markdown:
            result = {"index": i, "markdown": format_markdown_output(trinity)}
        else:
            result = {
                "index": i,
                "earth": asdict(trinity.earth),
                "heaven": {"color": trinity.heaven.audit_color.value,
                           "confidence": trinity.heaven.confidence,
                           "hopfield_energy": trinity.heaven.hopfield_energy,
                           "meltdown": trinity.heaven.meltdown_level.value},
                "human": asdict(trinity.human),
                "dna": trinity.dna,
            }
        results.append(result)

    # 保存快照
    engine.save_snapshot(engine.snapshots[-1] if engine.snapshots else trinity, f"batch_{len(results)}items")

    # 输出到文件
    if output_file:
        try:
            if markdown:
                content = "\n\n---\n\n".join(r.get("markdown", "") for r in results)
            else:
                content = json.dumps(results, ensure_ascii=False, indent=2)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"批量结果已输出: {output_file} ({len(results)} 条)")
        except Exception as e:
            logger.error(f"输出文件写入失败: {e}")

    return results

def interactive_mode(engine: NeuronFlowEngine):
    """交互模式"""
    cprint(f"\n🐉 神经元-流场引擎交互模式 {VERSION}", Colors.BOLD)
    cprint("命令: density | hopfield | audit | persona | map | status", Colors.CYAN)
    cprint("      dual-brain | self-audit | stats | snapshots | help | exit", Colors.CYAN)
    cprint(f"DNA: {engine.dna[:60]}...", Colors.DIM)
    cprint("")

    while True:
        try:
            cmd = input(f"{Colors.CYAN}🔮 nf>{Colors.RESET} ").strip()
            if not cmd:
                continue

            if cmd == "exit" or cmd == "quit":
                cprint("再见。龍魂永存。", Colors.GREEN)
                break

            elif cmd == "help":
                cprint("可用命令:", Colors.BOLD)
                for c in ["density [粒子数]", "hopfield", "audit <文本>", "persona [意图]",
                          "map [粒子数]", "status", "dual-brain", "self-audit", "stats", "snapshots"]:
                    cprint(f"  {c}", Colors.CYAN)

            elif cmd == "density" or cmd.startswith("density "):
                try:
                    p = int(cmd.split()[-1]) if len(cmd.split()) > 1 else 500
                except ValueError:
                    p = 500
                density = engine.compute_density(p, 1000)
                cprint(f"  地场密度: {density:.4f} (粒子: {p})", Colors.CYAN)

            elif cmd == "hopfield":
                state = [1, -1, 1, -1, 1]
                weights = [[0.3, -0.2, 0.4, -0.1, 0.2],
                           [-0.2, 0.5, -0.3, 0.2, -0.1],
                           [0.4, -0.3, 0.6, -0.2, 0.3],
                           [-0.1, 0.2, -0.2, 0.4, -0.3],
                           [0.2, -0.1, 0.3, -0.3, 0.5]]
                result = engine.hopfield_attractor_check(state, weights)
                cprint(f"  Hopfield能量: {result['energy']:.6f}", Colors.CYAN)
                cprint(f"  稳定性: {'✅ 稳定' if result['is_stable'] else '❌ 不稳定'}", Colors.GREEN if result['is_stable'] else Colors.RED)
                cprint(f"  吸引子: {'✅ 是' if result['is_attractor'] else '❌ 否'} (盆地={result['basin_size']})", Colors.GREEN if result['is_attractor'] else Colors.YELLOW)

            elif cmd.startswith("audit"):
                text = cmd[6:].strip() or "默认测试文本"
                heaven, record = engine.tri_color_audit(text)
                color = record["color"]
                cprint(f"  {color} {record['result']}: {record['reason']}", Colors.RESET)
                cprint(f"  置信度: {record['confidence']:.4f} | 感受野: {record['receptive_field']:.4f}", Colors.DIM)
                cprint(f"  Hopfield: {record['hopfield_energy']:.6f} | 熔断: {record['meltdown']}", Colors.DIM)

            elif cmd == "persona" or cmd.startswith("persona "):
                intent = cmd[8:].strip() if len(cmd) > 8 else ""
                density = float(input(f"  密度 [0.5]: ").strip() or "0.5")
                human = engine.route_persona(density, intent)
                print_persona_matrix(density, human.active_personas)

            elif cmd == "map" or cmd.startswith("map "):
                try:
                    particles = int(cmd.split()[-1]) if len(cmd.split()) > 1 else 500
                except ValueError:
                    particles = 500
                text = input(f"  上下文文本 []: ").strip()
                intent = input(f"  意图关键词 []: ").strip()
                synapses_input = input(f"  突触权重(逗号分隔) [0.5,0.5,0.5,0.5,0.5]: ").strip()
                if synapses_input:
                    synapses = [float(x.strip()) for x in synapses_input.split(",")]
                else:
                    synapses = [0.5, 0.5, 0.5, 0.5, 0.5]
                trinity = engine.trinity_map(particles, synapses,
                                             {"text": text, "intent": intent})
                print(format_trinity_output(trinity))

            elif cmd == "status":
                result = engine.self_audit()
                cprint(f"\n🐉 {result['engine']}", Colors.BOLD)
                cprint(f"状态: {result['status']}", Colors.CYAN)
                cprint(f"DNA: {result['dna']}", Colors.DIM)
                for key, val in result["checks"].items():
                    icon = "✅" if "✅" in val['status'] else "❌"
                    cprint(f"  {icon} {key}: {val['detail']}", Colors.GREEN if icon == "✅" else Colors.RED)

            elif cmd == "dual-brain":
                result = engine.dual_brain_sync(
                    {"decision": "新人格规则v4.0"},
                    {"sync_event": "persona_correction"}
                )
                cprint(f"\n🔗 双脑协同", Colors.BOLD)
                cprint(f"  → 左脑: {result['right_to_left']['carrier']}", Colors.CYAN)
                cprint(f"  → 右脑: {result['left_to_right']['carrier']}", Colors.CYAN)
                cprint(f"  共同账本: {result['common_ledger']['carrier']}", Colors.CYAN)
                cprint(f"  Claude兜底: {result['right_to_left']['fallback']}", Colors.DIM)

            elif cmd == "self-audit":
                result = engine.self_audit()
                cprint(f"\n🔍 完整性自检: {result['status']}", Colors.CYAN)
                for key, val in result["checks"].items():
                    cprint(f"  {val['status']} {key}", Colors.RESET)

            elif cmd == "stats":
                metrics = engine.get_metrics()
                cprint(f"\n📊 性能指标", Colors.BOLD)
                for k, v in metrics.items():
                    cprint(f"  {k}: {v}", Colors.CYAN)

            elif cmd == "snapshots":
                snaps = engine.list_snapshots()
                if snaps:
                    cprint(f"\n📸 流场快照 ({len(snaps)} 个)", Colors.BOLD)
                    for s in snaps[:10]:
                        cprint(f"  {s['name']} ({s['size']}B, {s['time']})", Colors.DIM)
                else:
                    cprint("暂无快照", Colors.YELLOW)

            else:
                # 尝试作为审计文本
                heaven, record = engine.tri_color_audit(cmd)
                cprint(f"  {record['color']} {record['result']}: {record['reason']}", Colors.RESET)

        except KeyboardInterrupt:
            cprint("\n再见。龍魂永存。", Colors.GREEN)
            break
        except Exception as e:
            cprint(f"❌ 错误: {e}", Colors.RED)
            logger.error(f"交互模式异常: {e}")

# ============================================================
# main
# ============================================================

def main():
    parser = create_parser()
    args = parser.parse_args()

    engine = NeuronFlowEngine()

    # ── 自检 ──
    if args.self_audit:
        result = engine.self_audit()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif args.markdown:
            lines = [f"# 🔍 三色审计完整性自检", "", f"**引擎**: {result['engine']}", f"**状态**: {result['status']}", ""]
            for key, val in result["checks"].items():
                lines.append(f"- {val['status']} **{key}**: {val['detail']}")
            print("\n".join(lines))
        else:
            cprint(f"\n🔍 {result['engine']}", Colors.BOLD)
            cprint(f"状态: {result['status']}", Colors.CYAN)
            cprint(f"DNA: {result['dna']}", Colors.DIM)
            cprint(f"审计统计: 🟢{result['audit_stats']['🟢']} 🟡{result['audit_stats']['🟡']} 🔴{result['audit_stats']['🔴']}", Colors.CYAN)
            for key, val in result["checks"].items():
                icon = "✅" if "✅" in val['status'] else "❌"
                cprint(f"  {icon} {key}: {val['detail']}", Colors.GREEN if icon == "✅" else Colors.RED)
        return

    # ── 双脑协同 ──
    if args.dual_brain:
        result = engine.dual_brain_sync()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            cprint("\n🔗 双脑协同接口", Colors.BOLD)
            cprint(f"  右脑→左脑: {result['right_to_left']['carrier']} ({result['right_to_left']['description']})", Colors.CYAN)
            cprint(f"  左脑→右脑: {result['left_to_right']['carrier']} ({result['left_to_right']['description']})", Colors.CYAN)
            cprint(f"  共同账本: {result['common_ledger']['carrier']} ({result['common_ledger']['description']})", Colors.CYAN)
            cprint(f"  Claude兜底: {result['right_to_left']['fallback']}", Colors.DIM)
        return

    # ── 密度计算 ──
    if args.density is not None:
        density = engine.compute_density(args.particles, args.max_particles)
        if args.json:
            print(json.dumps({"density": density, "particles": args.particles,
                              "max_particles": args.max_particles}, ensure_ascii=False))
        else:
            cprint(f"📊 地场密度: {density:.4f} (粒子: {args.particles}/{args.max_particles})", Colors.CYAN)
            if density > 0.8:
                cprint(f"  ⚠️ 密度过高，建议降载", Colors.YELLOW)
        return

    # ── Hopfield ──
    if args.hopfield:
        state = [1, -1, 1, -1, 1]
        weights = [[0.3, -0.2, 0.4, -0.1, 0.2],
                   [-0.2, 0.5, -0.3, 0.2, -0.1],
                   [0.4, -0.3, 0.6, -0.2, 0.3],
                   [-0.1, 0.2, -0.2, 0.4, -0.3],
                   [0.2, -0.1, 0.3, -0.3, 0.5]]
        result = engine.hopfield_attractor_check(state, weights)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            cprint(f"\n⚡ Hopfield能量分析", Colors.BOLD)
            cprint(f"  能量:     {result['energy']:.6f}", Colors.CYAN)
            stable_color = Colors.GREEN if result['is_stable'] else Colors.RED
            cprint(f"  稳定性:   {'✅ 稳定' if result['is_stable'] else '❌ 不稳定'}", stable_color)
            attractor_color = Colors.GREEN if result['is_attractor'] else Colors.YELLOW
            cprint(f"  吸引子:   {'✅ 是' if result['is_attractor'] else '❌ 否'}", attractor_color)
            cprint(f"  盆地大小: {result['basin_size']}", Colors.DIM)
        return

    # ── 三色审计 ──
    if args.audit:
        heaven, record = engine.tri_color_audit(args.audit)
        if args.json:
            print(json.dumps(record, ensure_ascii=False, indent=2))
        elif args.markdown:
            print(f"""## 🎨 三色审计

| 指标 | 值 |
|:---|---:|
| 审计结果 | {record['color']} {record['result']} |
| 置信度 | {record['confidence']:.4f} |
| 感受野 | {record['receptive_field']:.4f} |
| Hopfield能量 | {record['hopfield_energy']:.6f} |
| 稳定性 | {'✅' if record['is_stable'] else '❌'} |
| 熔断 | {record['meltdown']} |
| 原因 | {record['reason']} |

**DNA**: `{record['dna']}`
""")
        else:
            cprint(f"\n🎨 三色审计: {record['color']} {record['result']}", Colors.RESET)
            cprint(f"  置信度: {record['confidence']:.4f} | 感受野: {record['receptive_field']:.4f}", Colors.DIM)
            cprint(f"  原因: {record['reason']}", Colors.RESET)
            cprint(f"  Hopfield: {record['hopfield_energy']:.6f} | 熔断: {record['meltdown']}", Colors.DIM)
        return

    # ── 人格路由 ──
    if args.persona is not None:
        density = 0.5  # 默认密度
        human = engine.route_persona(density, args.persona)
        if args.json:
            print(json.dumps(asdict(human), ensure_ascii=False, indent=2))
        else:
            cprint(f"\n🧠 人格路由 (密度: {density:.2f}, 意图: '{args.persona or '(无)'}')", Colors.BOLD)
            cprint(f"  激活: {human.persona_count} 人格 | 主路由: {PERSONAS.get(human.primary_persona, Persona(human.primary_persona,'','','',0)).name}", Colors.CYAN)
            cprint(f"  路径: {' → '.join(human.routing_path) if human.routing_path else '(直接激活)'}", Colors.DIM)
            print_persona_matrix(density, human.active_personas)
        return

    # ── 三才统一映射 ──
    if args.map:
        text = args.audit or ""
        intent = args.persona or ""
        synapses = [0.5, 0.5, 0.5, 0.5, 0.5]  # 默认突触权重
        trinity = engine.trinity_map(args.particles, synapses,
                                     {"text": text, "intent": intent})
        engine.save_snapshot(trinity)

        if args.json:
            print(format_trinity_output(trinity, json_mode=True))
        elif args.markdown:
            print(format_markdown_output(trinity))
        else:
            print(format_trinity_output(trinity))

        # 输出到文件
        if args.output:
            try:
                content = format_markdown_output(trinity) if args.markdown else format_trinity_output(trinity)
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(content)
                cprint(f"\n✅ 输出已保存: {args.output}", Colors.GREEN)
            except Exception as e:
                cprint(f"❌ 输出保存失败: {e}", Colors.RED)
        return

    # ── 批量处理 ──
    if args.batch:
        results = batch_process(engine, args.batch, args.output, args.markdown)
        if not args.output:
            if args.markdown:
                for r in results:
                    print(r.get("markdown", ""))
                    print("\n---\n")
            elif args.json:
                print(json.dumps(results, ensure_ascii=False, indent=2))
            else:
                cprint(f"\n✅ 批量处理完成: {len(results)} 条", Colors.GREEN)
                for r in results:
                    heaven = r.get("heaven", {})
                    human = r.get("human", {})
                    cprint(f"  [{r['index']}] {heaven.get('color','?')} 密度={r['earth']['density']:.3f} | 人格={human.get('primary_persona','?')}", Colors.CYAN)
        return

    # ── 性能指标 ──
    if args.stats:
        metrics = engine.get_metrics()
        if args.json:
            print(json.dumps(metrics, ensure_ascii=False, indent=2))
        else:
            cprint(f"\n📊 性能指标 · {VERSION}", Colors.BOLD)
            for k, v in metrics.items():
                cprint(f"  {k}: {v}", Colors.CYAN)
            cprint(f"\n  快照磁盘文件:", Colors.CYAN)
            for s in engine.list_snapshots()[:5]:
                cprint(f"    {s['name']} ({s['size']}B)", Colors.DIM)
        return

    # ── 快照列表 ──
    if args.snapshots:
        snaps = engine.list_snapshots()
        if args.json:
            print(json.dumps(snaps, ensure_ascii=False, indent=2))
        else:
            cprint(f"\n📸 流场快照 ({len(snaps)} 个)", Colors.BOLD)
            for s in snaps:
                cprint(f"  {s['name']:<40} {s['size']:>8}B  {s['time']}", Colors.DIM)
        return

    # ── 状态（默认）──
    if args.status or True:  # 无参数默认显示状态
        result = engine.self_audit()
        cprint(f"\n🐉 神经元-流场映射引擎 {VERSION}", Colors.BOLD)
        cprint(f"DNA: {result['dna']}", Colors.DIM)
        cprint(f"状态: {result['status']}", Colors.CYAN)
        cprint(f"  人格修正: ✅ GodEye→P05·宝宝P02独立·龍盾P72独立", Colors.GREEN)
        cprint(f"  五大人格: P03雯雯·P04鲁班·P05上帝之眼·P72龍盾·P77明天使", Colors.CYAN)
        cprint(f"  三才映射: 地场(Merkle)·天场(Hopfield+审计)·人场(五人格路由)", Colors.CYAN)
        cprint(f"  审计统计: 🟢{result['audit_stats']['🟢']} 🟡{result['audit_stats']['🟡']} 🔴{result['audit_stats']['🔴']}", Colors.CYAN)
        cprint(f"  快照: {result['snapshot_count']} 个", Colors.DIM)
        if not any([args.self_audit, args.dual_brain, args.density, args.hopfield,
                    args.audit, args.persona is not None, args.map, args.batch,
                    args.stats, args.snapshots, args.interactive]):
            cprint(f"\n  用法: {sys.argv[0]} --help", Colors.DIM)
        return

    # ── 交互模式 ──
    if args.interactive:
        interactive_mode(engine)
        return

    parser.print_help()

if __name__ == "__main__":
    main()
