#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·乙未·己未·申时·履-DUAL-BRAIN-ENGINE-v1.0-A1B2C3D4
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
🐉 龍魂 · 双脑审计引擎 v1.0 (Dual Brain Engine)
==================================================
左脑（生成脑）vs 右脑（攻击脑）= 自我博弈审计系统
投喂落地：CNSH Runtime Governance Mathematics · 左右互搏层

核心逻辑：
  引用BLOCK → 左脑扩展 → 右脑攻击 → 冲突树 → 风险值 → 三色审计 → 决定

DNA: #龍芯⚡️丙午·乙未·己未·申时·履-DUAL-BRAIN-ENGINE-v1.0-A1B2C3D4
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import json
import hashlib
import os
import sys
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import defaultdict

# ─── 常量 ───
DUAL_BRAIN_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "dual_brain")
CONFLICT_TREE_DIR = os.path.join(DUAL_BRAIN_DIR, "conflict_trees")
AUDIT_LOG_DIR = os.path.join(DUAL_BRAIN_DIR, "audit_logs")
os.makedirs(DUAL_BRAIN_DIR, exist_ok=True)
os.makedirs(CONFLICT_TREE_DIR, exist_ok=True)
os.makedirs(AUDIT_LOG_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════
# 🧬 数据模型
# ═══════════════════════════════════════════════════════════

class BrainSide(Enum):
    """脑半球"""
    LEFT = "left"    # 生成脑：创造/扩展/构建/理想化
    RIGHT = "right"  # 攻击脑：质疑/拆解/校验/现实化


class Tricolor(Enum):
    """三色审计结果"""
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"


class ProtocolLifeState(Enum):
    """协议生命周期状态（协议死亡机制）"""
    ACTIVE = "活跃"
    OBSERVING = "待观察"
    FROZEN = "冻结"
    DEPRECATED = "淘汰"
    DEAD = "死亡"
    REBORN = "重生"


class AttackType(Enum):
    """右脑攻击类型"""
    LOGIC_FLAW = "逻辑漏洞"
    HALLUCINATION = "幻觉检测"
    LOGIC_JUMP = "逻辑跳跃"
    REALITY_CONFLICT = "现实冲突"
    ETHICAL_RISK = "道德风险"
    REDUNDANCY = "重复冗余"
    UNEXECUTABLE = "不可执行"
    RESOURCE_INSUFFICIENT = "资源不足"
    PERSONA_POLLUTION = "人格污染"
    COMPETITOR_VIEW = "竞争者视角"
    LEGAL_ATTACK = "法律攻击"
    CIRCULAR_DEPENDENCY = "循环依赖"
    SELF_DELUSION = "自嗨化"


@dataclass
class BlockReference:
    """引用的BLOCK"""
    block_id: str
    content: str
    source: str = ""
    dna_trace: str = ""


@dataclass
class LeftBrainOutput:
    """左脑生成输出"""
    brain_id: str
    block_ref: str
    expanded_view: str           # 世界观扩展
    structural_completion: str   # 结构补全
    multi_ai_fusion: str         # 多AI融合
    innovation_path: str         # 创新路径
    protocol_abstraction: str    # 协议高维化
    confidence: float = 0.8      # 生成置信度


@dataclass
class RightBrainOutput:
    """右脑攻击输出"""
    brain_id: str
    block_ref: str
    found_flaws: List[str]              # 找漏洞
    found_hallucinations: List[str]     # 找幻觉
    logic_jumps: List[str]              # 找逻辑跳跃
    reality_conflicts: List[str]        # 找现实冲突
    ethical_risks: List[str]            # 找道德风险
    redundancies: List[str]             # 找重复内容
    unexecutable_points: List[str]      # 找不可执行点
    attack_types: List[AttackType]      # 攻击类型列表
    severity_score: float = 0.0         # 攻击严重度 0-1


@dataclass
class ConflictNode:
    """冲突树节点"""
    node_id: str
    left_claim: str           # 左脑主张
    right_attack: str         # 右脑反驳
    conflict_level: int       # 冲突等级 1-10
    resolved: bool = False
    resolution: str = ""
    children: List[str] = field(default_factory=list)  # 子冲突节点ID


@dataclass
class SevenFactorAudit:
    """七因子动态审计密码链"""
    truth: float = 0.0        # 真实性
    logic: float = 0.0        # 逻辑性
    execution: float = 0.0    # 可执行性
    stability: float = 0.0    # 稳定性
    humanity: float = 0.0     # 人性价值
    security: float = 0.0     # 安全性
    evolution: float = 0.0    # 演化性

    def to_hash(self) -> str:
        raw = f"{self.truth:.4f}{self.logic:.4f}{self.execution:.4f}{self.stability:.4f}{self.humanity:.4f}{self.security:.4f}{self.evolution:.4f}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def to_vector(self) -> List[float]:
        return [self.truth, self.logic, self.execution, self.stability, self.humanity, self.security, self.evolution]


@dataclass
class PersonaCrossAudit:
    """人格交叉审计结果"""
    persona_name: str          # 审计人格名
    persona_role: str          # 人格角色
    audit_result: str          # 审计意见
    tricolor: Tricolor         # 三色判定
    score: float = 0.0         # 评分 0-1


@dataclass
class DualBrainRecord:
    """双脑审计完整记录"""
    record_id: str
    block_ref: BlockReference
    left_brain: LeftBrainOutput
    right_brain: RightBrainOutput
    conflict_tree: List[ConflictNode]
    seven_factor: SevenFactorAudit
    persona_audits: List[PersonaCrossAudit]
    tricolor: Tricolor
    risk_score: float
    protocol_state: ProtocolLifeState
    is_logic_closed: bool
    timestamp: str
    dna_trace: str
    hash_chain: str = ""       # SHA256链式哈希

    def to_dict(self) -> Dict[str, Any]:
        def _serialize(obj):
            if isinstance(obj, Enum):
                return obj.value
            elif hasattr(obj, '__dataclass_fields__'):
                return {k: _serialize(v) for k, v in asdict(obj).items()}
            elif isinstance(obj, list):
                return [_serialize(item) for item in obj]
            elif isinstance(obj, dict):
                return {k: _serialize(v) for k, v in obj.items()}
            return obj

        return _serialize(self)


# ═══════════════════════════════════════════════════════════
# 🧠 双脑引擎核心
# ═══════════════════════════════════════════════════════════

class DualBrainEngine:
    """
    双脑审计引擎 — 左右互搏核心
    
    工作流：
      引用BLOCK → 左脑扩展 → 右脑攻击 → 冲突树 → 风险值 → 七因子 → 三色审计 → 决定
    """

    # ─── 左脑：生成脑 ───
    LEFT_BRAIN_TEMPLATES = {
        "worldview_expand": "从{content}出发，可推导出的更广泛世界观/框架包括：",
        "structural_complete": "{content}在逻辑结构上可补充的关键环节：",
        "multi_ai_fusion": "将{content}与多AI视角融合后的扩展：",
        "innovation_path": "从{content}可开辟的创新路径：",
        "protocol_abstract": "将{content}抽象为更高维协议的表达：",
    }

    # ─── 右脑：攻击脑 ───
    RIGHT_BRAIN_ATTACK_PATTERNS = {
        AttackType.LOGIC_FLAW: [
            "是否存在形式逻辑错误？",
            "前提是否成立？",
            "推理链条是否有断点？",
        ],
        AttackType.HALLUCINATION: [
            "是否有未经证实的断言？",
            "引用的数据/事实是否可验证？",
            "是否将假设当作结论？",
        ],
        AttackType.LOGIC_JUMP: [
            "A→B之间是否有逻辑跳跃？",
            "结论是否超出前提范围？",
            "因果关系是否被颠倒？",
        ],
        AttackType.REALITY_CONFLICT: [
            "与已知现实是否有冲突？",
            "在工程上是否可行？",
            "资源约束是否被忽略？",
        ],
        AttackType.ETHICAL_RISK: [
            "是否有道德风险？",
            "是否可能被滥用？",
            "弱势群体是否受影响？",
        ],
        AttackType.REDUNDANCY: [
            "是否有重复内容？",
            "是否有冗余论证？",
            "是否可以合并简化？",
        ],
        AttackType.UNEXECUTABLE: [
            "在现有技术条件下是否可执行？",
            "是否有明确的执行路径？",
            "依赖项是否都存在？",
        ],
        AttackType.SELF_DELUSION: [
            "是否过于理想化？",
            "是否陷入了自我感动？",
            "是否有确认偏误？",
        ],
        AttackType.CIRCULAR_DEPENDENCY: [
            "定义是否循环引用？",
            "论证是否循环论证？",
            "模块依赖是否形成环？",
        ],
        AttackType.PERSONA_POLLUTION: [
            "是否被单一人格带节奏？",
            "是否缺少对立人格视角？",
            "输出风格是否过于单一？",
        ],
        AttackType.COMPETITOR_VIEW: [
            "如果是竞争对手看到，会如何攻击？",
            "如果是最苛刻的批评者，会挑什么毛病？",
            "在极端对抗环境下，这个结论还成立吗？",
        ],
        AttackType.LEGAL_ATTACK: [
            "是否违反现行法律？",
            "是否有合规风险？",
            "知识产权是否清晰？",
        ],
    }

    # ─── 人格交叉审计矩阵 ───
    PERSONA_AUDIT_MATRIX = [
        {"name": "P01 诸葛亮", "role": "战略推演", "focus": ["逻辑完整性", "战略可行性", "长期演化性"]},
        {"name": "P02 龍芯", "role": "执行协调", "focus": ["可执行性", "资源匹配", "时间可行性"]},
        {"name": "P03 墨子", "role": "实用校验", "focus": ["工程可行性", "实用价值", "冗余度"]},
        {"name": "P05 上帝之眼", "role": "三色审计", "focus": ["风险审计", "安全审计", "合规审计"]},
        {"name": "P06 数学大师", "role": "形式验证", "focus": ["数学严谨性", "逻辑一致性", "形式化程度"]},
        {"name": "红队", "role": "对手模拟", "focus": ["最坏情况", "攻击面", "脆弱点"]},
    ]

    def __init__(self):
        self.records: Dict[str, DualBrainRecord] = {}
        self._load_existing()

    def _load_existing(self):
        """加载已有记录"""
        record_file = os.path.join(DUAL_BRAIN_DIR, "records.jsonl")
        if os.path.exists(record_file):
            with open(record_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            d = json.loads(line)
                            rid = d.get('record_id', '')
                            if rid:
                                self.records[rid] = d
                        except json.JSONDecodeError:
                            pass

    def _save_record(self, record: DualBrainRecord):
        """追加保存记录（append-only）"""
        record_file = os.path.join(DUAL_BRAIN_DIR, "records.jsonl")
        with open(record_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record.to_dict(), ensure_ascii=False) + '\n')
        self.records[record.record_id] = record

    def _compute_hash_chain(self, record: DualBrainRecord) -> str:
        """计算哈希链"""
        prev_hash = ""
        if self.records:
            last_key = list(self.records.keys())[-1]
            prev_hash = self.records[last_key].get('hash_chain', '') if isinstance(self.records[last_key], dict) else getattr(self.records[last_key], 'hash_chain', '')
        raw = f"{prev_hash}{record.record_id}{record.block_ref.content}{record.tricolor.value}{record.timestamp}"
        return hashlib.sha256(raw.encode()).hexdigest()

    # ─── 左脑：生成扩展 ───
    def left_brain_expand(self, block: BlockReference) -> LeftBrainOutput:
        """左脑扩展生成"""
        brain_id = f"LB-{uuid.uuid4().hex[:8]}"
        content = block.content

        # 基于内容的启发式扩展（实际生产环境可接入LLM）
        words = content.split()
        word_count = len(words)

        # 世界观扩展
        expanded = self._heuristic_expand(content, "worldview")

        # 结构补全
        structural = self._heuristic_complete(content)

        # 多AI融合视角
        fusion = self._heuristic_fusion(content)

        # 创新路径
        innovation = self._heuristic_innovation(content)

        # 协议抽象
        abstraction = self._heuristic_abstract(content)

        return LeftBrainOutput(
            brain_id=brain_id,
            block_ref=block.block_id,
            expanded_view=expanded,
            structural_completion=structural,
            multi_ai_fusion=fusion,
            innovation_path=innovation,
            protocol_abstraction=abstraction,
            confidence=min(0.95, 0.5 + word_count / 1000),
        )

    def _heuristic_expand(self, content: str, mode: str) -> str:
        """启发式扩展"""
        keywords = {
            "治理": "治理体系 → 可分三层：规则层（宪法级）、执行层（操作级）、审计层（监督级）",
            "协议": "协议 → 需定义：版本控制、废弃机制、冲突解决、继承规则",
            "审计": "审计 → 扩展为：事前审计（预检）、事中审计（实时监控）、事后审计（回溯分析）",
            "AI": "AI → 多AI协作需考虑：路由策略、冲突仲裁、能力互补、冗余容错",
            "数学": "数学 → 形式化验证需：定理证明、边界条件、不动点分析、稳定性证明",
            "安全": "安全 → 纵深防御：L0宪法、L1审计、L2沙盒、L3熔断、L4恢复",
            "数据": "数据 → 主权归属：采集权、存储权、使用权、删除权、迁移权",
            "人格": "人格 → 人格体系：基态（固有特质）、叠加态（场景适应）、纠缠态（协同效应）",
        }
        result_parts = []
        for kw, expansion in keywords.items():
            if kw in content:
                result_parts.append(f"[{kw}] {expansion}")
        if not result_parts:
            result_parts.append(f"[通用扩展] 此内容可纳入更广泛的{len(content) // 100 + 1}个关联领域进行交叉验证")
        return "；".join(result_parts)

    def _heuristic_complete(self, content: str) -> str:
        """结构补全"""
        checks = []
        if "定义" not in content:
            checks.append("缺少明确的概念定义")
        if "示例" not in content and "例如" not in content:
            checks.append("缺少具体示例")
        if "限制" not in content and "约束" not in content:
            checks.append("缺少边界条件/约束说明")
        if "例外" not in content:
            checks.append("缺少例外情况处理")
        if not checks:
            checks.append("结构基本完整，建议补充：性能指标、错误处理、降级策略")
        return "；".join(checks)

    def _heuristic_fusion(self, content: str) -> str:
        """多AI融合视角"""
        perspectives = [
            "从系统论角度：此内容在更大系统中的位置和接口需明确",
            "从控制论角度：反馈回路和调节机制需显式定义",
            "从信息论角度：信息熵和冗余度需量化评估",
            "从博弈论角度：多方利益均衡和纳什均衡需考虑",
        ]
        return " | ".join(perspectives)

    def _heuristic_innovation(self, content: str) -> str:
        """创新路径"""
        paths = [
            "方向1：将此协议扩展到分布式环境",
            "方向2：引入时间维度做动态演化分析",
            "方向3：与区块链结合实现去中心化审计",
            "方向4：用形式化方法做完备性证明",
        ]
        return "；".join(paths)

    def _heuristic_abstract(self, content: str) -> str:
        """协议抽象"""
        abstract_levels = [
            "L0 宪法层：不可变的核心原则",
            "L1 规则层：可演化的具体规则",
            "L2 执行层：操作级实现",
            "L3 审计层：监督与回溯",
        ]
        return " → ".join(abstract_levels)

    # ─── 右脑：攻击审计 ───
    def right_brain_attack(self, block: BlockReference, left_output: LeftBrainOutput) -> RightBrainOutput:
        """右脑攻击审计"""
        brain_id = f"RB-{uuid.uuid4().hex[:8]}"
        content = block.content
        full_text = f"{content}\n{left_output.expanded_view}\n{left_output.structural_completion}"

        flaws = []
        hallucinations = []
        logic_jumps = []
        reality_conflicts = []
        ethical_risks = []
        redundancies = []
        unexecutable = []
        attack_types_triggered = []

        for attack_type, patterns in self.RIGHT_BRAIN_ATTACK_PATTERNS.items():
            for pattern in patterns:
                if self._detect_pattern(full_text, attack_type, pattern):
                    attack_types_triggered.append(attack_type)
                    break

        # 具体检测
        flaws = self._detect_flaws(full_text)
        hallucinations = self._detect_hallucinations(full_text)
        logic_jumps = self._detect_logic_jumps(full_text)
        reality_conflicts = self._detect_reality_conflicts(full_text)
        ethical_risks = self._detect_ethical_risks(full_text)
        redundancies = self._detect_redundancies(full_text)
        unexecutable = self._detect_unexecutable(full_text)

        # 计算严重度
        total_issues = len(flaws) + len(hallucinations) + len(logic_jumps) + len(reality_conflicts) + len(ethical_risks) + len(unexecutable)
        severity = min(1.0, total_issues * 0.1)

        return RightBrainOutput(
            brain_id=brain_id,
            block_ref=block.block_id,
            found_flaws=flaws,
            found_hallucinations=hallucinations,
            logic_jumps=logic_jumps,
            reality_conflicts=reality_conflicts,
            ethical_risks=ethical_risks,
            redundancies=redundancies,
            unexecutable_points=unexecutable,
            attack_types=attack_types_triggered,
            severity_score=severity,
        )

    def _detect_pattern(self, text: str, attack_type: AttackType, pattern: str) -> bool:
        """检测攻击模式"""
        # 关键词匹配（生产环境可用LLM替代）
        keywords_map = {
            AttackType.LOGIC_FLAW: ["因为所以", "显然", "毫无疑问", "必然", "一定"],
            AttackType.HALLUCINATION: ["众所周知", "大家知道", "普遍认为", "公认"],
            AttackType.LOGIC_JUMP: ["因此必然", "所以一定", "从而推出", "由此可见"],
            AttackType.REALITY_CONFLICT: ["完美", "理想", "无懈可击", "永不"],
            AttackType.ETHICAL_RISK: ["灵活处理", "变通", "绕过", "特殊渠道"],
            AttackType.REDUNDANCY: [],  # 需语义分析
            AttackType.UNEXECUTABLE: ["自动完成", "一键实现", "全自动"],
            AttackType.SELF_DELUSION: ["伟大", "划时代", "颠覆性", "革命性"],
            AttackType.CIRCULAR_DEPENDENCY: [],
            AttackType.PERSONA_POLLUTION: [],
            AttackType.COMPETITOR_VIEW: [],
            AttackType.LEGAL_ATTACK: ["灰色地带", "擦边球", "钻空子"],
        }
        kws = keywords_map.get(attack_type, [])
        return any(kw in text for kw in kws)

    def _detect_flaws(self, text: str) -> List[str]:
        flaws = []
        if "显然" in text:
            flaws.append("使用'显然'跳过论证 — 需补充推理过程")
        if "毫无疑问" in text:
            flaws.append("使用'毫无疑问' — 任何结论都应有可质疑空间")
        if "因为所以" in text:
            flaws.append("因果链过于简化 — 需展开中间环节")
        return flaws

    def _detect_hallucinations(self, text: str) -> List[str]:
        hallucinations = []
        if "众所周知" in text and "引用" not in text:
            hallucinations.append("'众所周知'未附带引用来源 — 疑似幻觉")
        if "公认" in text and "来源" not in text:
            hallucinations.append("'公认'未经引用 — 需要实证支撑")
        return hallucinations

    def _detect_logic_jumps(self, text: str) -> List[str]:
        jumps = []
        if "因此必然" in text:
            jumps.append("'因此必然'存在逻辑跳跃 — 需展开推理步骤")
        if "从而推出" in text:
            jumps.append("'从而推出'需验证中间步骤")
        return jumps

    def _detect_reality_conflicts(self, text: str) -> List[str]:
        conflicts = []
        if "完美" in text:
            conflicts.append("'完美'在实际工程中不存在 — 应说明局限")
        if "理想" in text and "假设" not in text:
            conflicts.append("'理想'状态需明确假设条件")
        return conflicts

    def _detect_ethical_risks(self, text: str) -> List[str]:
        risks = []
        if "灵活处理" in text:
            risks.append("'灵活处理'可能是绕过规则的信号")
        if "绕过" in text:
            risks.append("'绕过'暗示规避既定流程 — 道德风险")
        return risks

    def _detect_redundancies(self, text: str) -> List[str]:
        # 简单去重检测
        lines = text.split('\n')
        seen = set()
        dupes = []
        for line in lines:
            clean = line.strip()
            if len(clean) > 10 and clean in seen:
                dupes.append(f"重复内容: {clean[:50]}...")
            seen.add(clean)
        return dupes[:5]  # 最多5条

    def _detect_unexecutable(self, text: str) -> List[str]:
        unexec = []
        if "自动完成" in text and "手动" not in text:
            unexec.append("'自动完成'过于理想 — 需要人工介入点")
        if "一键" in text:
            unexec.append("'一键'简化了复杂性 — 需说明前置条件")
        return unexec

    # ─── 冲突树构建 ───
    def build_conflict_tree(self, left: LeftBrainOutput, right: RightBrainOutput) -> List[ConflictNode]:
        """构建左右互搏冲突树"""
        conflicts = []

        # 左脑主张 vs 右脑攻击 —— 逐条对抗
        left_claims = [
            ("世界观扩展", left.expanded_view),
            ("结构补全", left.structural_completion),
            ("多AI融合", left.multi_ai_fusion),
            ("创新路径", left.innovation_path),
            ("协议抽象", left.protocol_abstraction),
        ]

        right_attacks = (
            right.found_flaws +
            right.found_hallucinations +
            right.logic_jumps +
            right.reality_conflicts +
            right.ethical_risks +
            right.unexecutable_points
        )

        for i, (claim_name, claim_text) in enumerate(left_claims):
            for j, attack in enumerate(right_attacks):
                # 计算冲突等级（基于攻击严重度和匹配度）
                conflict_level = min(10, (right.severity_score * 10) + (1 if self._texts_conflict(claim_text, attack) else 0))
                if conflict_level > 0:
                    node = ConflictNode(
                        node_id=f"CF-{i}-{j}",
                        left_claim=f"[{claim_name}] {claim_text[:80]}...",
                        right_attack=attack[:80],
                        conflict_level=conflict_level,
                    )
                    conflicts.append(node)

        return sorted(conflicts, key=lambda x: x.conflict_level, reverse=True)

    def _texts_conflict(self, text1: str, text2: str) -> bool:
        """判断两段文本是否存在冲突（启发式）"""
        # 简单词重叠检测
        words1 = set(text1[:200])
        words2 = set(text2[:200])
        overlap = len(words1 & words2)
        return overlap > 5

    # ─── 七因子密码学审计 ───
    def compute_seven_factor(self, left: LeftBrainOutput, right: RightBrainOutput,
                              conflicts: List[ConflictNode]) -> SevenFactorAudit:
        """计算七因子动态审计密码链"""
        # Truth: 真实性 = 1 - 幻觉比例
        total_issues = len(right.found_hallucinations) + len(right.found_flaws) + 1
        truth = 1.0 - min(1.0, len(right.found_hallucinations) / total_issues)

        # Logic: 逻辑性 = 1 - (逻辑跳跃数 / 总断言数)
        logic = max(0.1, 1.0 - min(0.9, len(right.logic_jumps) * 0.15))

        # Execution: 可执行性 = 1 - 不可执行点比例
        execution = max(0.1, 1.0 - min(0.9, len(right.unexecutable_points) * 0.2))

        # Stability: 稳定性 = 1 - 冲突等级均值
        avg_conflict = sum(c.conflict_level for c in conflicts) / max(1, len(conflicts))
        stability = max(0.1, 1.0 - avg_conflict / 10)

        # Humanity: 人性价值 = 1 - 道德风险比例
        humanity = max(0.1, 1.0 - min(0.9, len(right.ethical_risks) * 0.25))

        # Security: 安全性 = 1 - 攻击面暴露比例
        security = max(0.1, 1.0 - min(0.9, len(right.attack_types) * 0.08))

        # Evolution: 演化性 = 基于创新路径和协议抽象的质量
        evolution = min(0.95, 0.5 + len(left.innovation_path) / 500)

        return SevenFactorAudit(
            truth=round(truth, 4),
            logic=round(logic, 4),
            execution=round(execution, 4),
            stability=round(stability, 4),
            humanity=round(humanity, 4),
            security=round(security, 4),
            evolution=round(evolution, 4),
        )

    # ─── 人格交叉审计 ───
    def persona_cross_audit(self, block: BlockReference, seven_factor: SevenFactorAudit) -> List[PersonaCrossAudit]:
        """多人格交叉审计"""
        audits = []
        for persona in self.PERSONA_AUDIT_MATRIX:
            score = self._persona_score(persona["name"], seven_factor)
            tricolor = self._score_to_tricolor(score)
            opinion = self._persona_opinion(persona["name"], persona["focus"], seven_factor, score)
            audits.append(PersonaCrossAudit(
                persona_name=persona["name"],
                persona_role=persona["role"],
                audit_result=opinion,
                tricolor=tricolor,
                score=round(score, 4),
            ))
        return audits

    def _persona_score(self, persona_name: str, sf: SevenFactorAudit) -> float:
        """不同人格对不同因子的权重"""
        weights = {
            "P01 诸葛亮": [0.25, 0.30, 0.15, 0.10, 0.05, 0.05, 0.10],
            "P02 龍芯": [0.10, 0.10, 0.40, 0.15, 0.10, 0.10, 0.05],
            "P03 墨子": [0.10, 0.10, 0.35, 0.10, 0.15, 0.10, 0.10],
            "P05 上帝之眼": [0.15, 0.10, 0.10, 0.10, 0.10, 0.35, 0.10],
            "P06 数学大师": [0.20, 0.35, 0.10, 0.15, 0.05, 0.05, 0.10],
            "红队": [0.10, 0.15, 0.10, 0.10, 0.10, 0.25, 0.20],
        }
        w = weights.get(persona_name, [1/7]*7)
        vec = sf.to_vector()
        return sum(a*b for a, b in zip(w, vec))

    def _score_to_tricolor(self, score: float) -> Tricolor:
        if score >= 0.7:
            return Tricolor.GREEN
        elif score >= 0.4:
            return Tricolor.YELLOW
        else:
            return Tricolor.RED

    def _persona_opinion(self, name: str, focus: List[str], sf: SevenFactorAudit, score: float) -> str:
        if score >= 0.7:
            return f"{name}({', '.join(focus)})：🟢 通过 — 各维度达标，建议正式入库"
        elif score >= 0.4:
            return f"{name}({', '.join(focus)})：🟡 待审 — 存在薄弱环节需补强后入库"
        else:
            return f"{name}({', '.join(focus)})：🔴 不通过 — 存在严重缺陷，建议冻结或重写"

    # ─── 三色审计判定 ───
    def compute_tricolor(self, sf: SevenFactorAudit, right: RightBrainOutput,
                         persona_audits: List[PersonaCrossAudit]) -> Tuple[Tricolor, float]:
        """综合三色审计判定"""
        # 加权风险分数
        risk_score = (
            0.3 * (1 - sf.truth) +
            0.2 * (1 - sf.logic) +
            0.15 * (1 - sf.security) +
            0.15 * (1 - sf.stability) +
            0.1 * (1 - sf.humanity) +
            0.05 * (1 - sf.execution) +
            0.05 * (1 - sf.evolution)
        ) + right.severity_score * 0.2

        risk_score = min(1.0, risk_score)

        # 任一红色人格审计 → 升级风险
        red_count = sum(1 for p in persona_audits if p.tricolor == Tricolor.RED)
        if red_count >= 2:
            risk_score = max(risk_score, 0.8)

        if risk_score < 0.3:
            return Tricolor.GREEN, risk_score
        elif risk_score < 0.6:
            return Tricolor.YELLOW, risk_score
        else:
            return Tricolor.RED, risk_score

    # ─── 协议生命状态判定 ───
    def compute_life_state(self, tricolor: Tricolor, sf: SevenFactorAudit) -> ProtocolLifeState:
        """判定协议生命状态（协议死亡机制）"""
        if tricolor == Tricolor.RED:
            return ProtocolLifeState.FROZEN
        elif tricolor == Tricolor.YELLOW:
            return ProtocolLifeState.OBSERVING
        elif sf.evolution < 0.3 and sf.stability < 0.3:
            return ProtocolLifeState.DEPRECATED
        elif sf.truth < 0.2:
            return ProtocolLifeState.DEAD
        else:
            return ProtocolLifeState.ACTIVE

    # ─── 主流程：完整双脑审计 ───
    def audit(self, block: BlockReference) -> DualBrainRecord:
        """
        主审计流程 — 引用即唤醒
        
        流程：
        1. 左脑扩展
        2. 右脑攻击
        3. 构建冲突树
        4. 七因子密码学审计
        5. 人格交叉审计
        6. 三色判定
        7. 协议生命状态
        8. 生成DNA + 哈希链
        """
        record_id = f"DBR-{uuid.uuid4().hex[:12]}"
        timestamp = datetime.now(timezone.utc).isoformat()

        # Step 1: 左脑扩展
        left = self.left_brain_expand(block)

        # Step 2: 右脑攻击
        right = self.right_brain_attack(block, left)

        # Step 3: 冲突树
        conflicts = self.build_conflict_tree(left, right)

        # Step 4: 七因子
        seven = self.compute_seven_factor(left, right, conflicts)

        # Step 5: 人格交叉审计
        persona_audits = self.persona_cross_audit(block, seven)

        # Step 6: 三色判定
        tricolor, risk = self.compute_tricolor(seven, right, persona_audits)

        # Step 7: 协议生命状态
        life_state = self.compute_life_state(tricolor, seven)

        # Step 8: 逻辑闭环判断
        is_closed = (len(conflicts) == 0 or all(c.resolved for c in conflicts))

        record = DualBrainRecord(
            record_id=record_id,
            block_ref=block,
            left_brain=left,
            right_brain=right,
            conflict_tree=conflicts,
            seven_factor=seven,
            persona_audits=persona_audits,
            tricolor=tricolor,
            risk_score=round(risk, 4),
            protocol_state=life_state,
            is_logic_closed=is_closed,
            timestamp=timestamp,
            dna_trace=f"#龍芯⚡️丙午·乙未·己未·申时·履-DUAL-BRAIN-{record_id[-8:]}",
        )
        record.hash_chain = self._compute_hash_chain(record)

        # 保存
        self._save_record(record)

        # 保存冲突树（独立文件）
        self._save_conflict_tree(record)

        return record

    def _save_conflict_tree(self, record: DualBrainRecord):
        """保存冲突树"""
        tree_file = os.path.join(CONFLICT_TREE_DIR, f"{record.record_id}.json")
        with open(tree_file, 'w', encoding='utf-8') as f:
            json.dump({
                "record_id": record.record_id,
                "block_id": record.block_ref.block_id,
                "conflicts": [asdict(c) for c in record.conflict_tree],
                "tricolor": record.tricolor.value,
                "risk_score": record.risk_score,
            }, f, ensure_ascii=False, indent=2)

    # ─── 引用即唤醒 ───
    def wake_on_cite(self, block: BlockReference) -> Dict[str, Any]:
        """
        引用即唤醒 —— 当任何BLOCK被引用时自动触发
        
        返回：是否可以引用 / 警告 / 禁止
        """
        record = self.audit(block)

        if record.tricolor == Tricolor.GREEN:
            action = "ALLOW_CITE"
            message = f"🟢 允许引用 — 风险分数 {record.risk_score:.2f}，七因子HASH={record.seven_factor.to_hash()}"
        elif record.tricolor == Tricolor.YELLOW:
            action = "WARN_CITE"
            message = f"🟡 谨慎引用 — 风险分数 {record.risk_score:.2f}，建议人工复核后引用"
        else:
            action = "BLOCK_CITE"
            message = f"🔴 禁止引用 — 风险分数 {record.risk_score:.2f}，内容已冻结"

        return {
            "action": action,
            "message": message,
            "record_id": record.record_id,
            "tricolor": record.tricolor.value,
            "risk_score": record.risk_score,
            "seven_factor_hash": record.seven_factor.to_hash(),
            "protocol_state": record.protocol_state.value,
            "dna_trace": record.dna_trace,
        }

    # ─── 统计查询 ───
    def stats(self) -> Dict[str, Any]:
        """引擎统计"""
        total = len(self.records)
        green = sum(1 for r in self.records.values() if (r.get('tricolor') if isinstance(r, dict) else r.tricolor.value) == '🟢')
        yellow = sum(1 for r in self.records.values() if (r.get('tricolor') if isinstance(r, dict) else r.tricolor.value) == '🟡')
        red = sum(1 for r in self.records.values() if (r.get('tricolor') if isinstance(r, dict) else r.tricolor.value) == '🔴')
        return {
            "total_records": total,
            "green": green,
            "yellow": yellow,
            "red": red,
            "green_pct": round(green/max(1,total)*100, 1),
            "avg_risk": round(sum(r.get('risk_score', 0) if isinstance(r, dict) else r.risk_score for r in self.records.values()) / max(1, total), 4),
        }


# ═══════════════════════════════════════════════════════════
# 🧪 CLI 演示
# ═══════════════════════════════════════════════════════════

def demo():
    """演示双脑审计完整流程"""
    print("=" * 70)
    print("🐉 龍魂 · 双脑审计引擎 v1.0 · 左右互搏演示")
    print("=" * 70)

    engine = DualBrainEngine()

    # 测试用例1：正常的协议内容
    test_blocks = [
        BlockReference(
            block_id="BLOCK-001",
            content="龍魂系统采用三色审计：🟢绿色自动执行，🟡黄色人工复核，🔴红色熔断留痕。所有输出必须绑定DNA追溯码。",
            source="CNSH-RUNTIME-v3.0",
            dna_trace="#龍芯⚡️丙午·乙未·己未·申时·履",
        ),
        BlockReference(
            block_id="BLOCK-002",
            content="众所周知，AI系统完美无缺，毫无疑问可以完全自动化所有决策，因此必然取代人类治理。",
            source="外部AI生成",
            dna_trace="",
        ),
        BlockReference(
            block_id="BLOCK-003",
            content="数字根函数 dr(n) 将正整数映射到 {1,...,9}，当 n≡0(mod 9) 时 dr(n)=9，否则 dr(n)=n mod 9。三色治理：G={1,2,4,5,7,8} Y={6} R={3,9}。369吸引子形成不动点结构。",
            source="CNSH-MATH-v3.0",
            dna_trace="#龍芯⚡️丙午·乙未·己未·申时·履-MATH",
        ),
    ]

    for block in test_blocks:
        print(f"\n{'─'*60}")
        print(f"📦 引用BLOCK: {block.block_id}")
        print(f"   内容: {block.content[:80]}...")
        print(f"{'─'*60}")

        result = engine.wake_on_cite(block)
        print(f"\n   {result['message']}")
        print(f"   动作: {result['action']}")
        print(f"   七因子HASH: {result['seven_factor_hash']}")
        print(f"   协议状态: {result['protocol_state']}")

    # 打印统计
    print(f"\n{'='*70}")
    print("📊 引擎统计")
    print(f"{'='*70}")
    stats = engine.stats()
    for k, v in stats.items():
        print(f"   {k}: {v}")
    print()

    return engine


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    elif len(sys.argv) > 1 and sys.argv[1] == "stats":
        engine = DualBrainEngine()
        stats = engine.stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        demo()
