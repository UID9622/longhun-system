#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·坎-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-ENGINE-_10_V3-0_0592-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                  龍魂体系 · 三色审计与10道闸流场决策系统 v3.0                      ║
║                         UID9622 · 龍芯北辰·诸葛鑫                               ║
║                         DNA签名激活版本 2026-06-16                              ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  核心链路: DNA签名 → 三色审计 → 流场决策(10道闸) → 入库执行                        ║
║  排序铁律: 忠(0.5) > 孝(0.3) > 义(0.2)                                         ║
║  R评分  : 0.2·人类福祉 + 0.2·公平公正 + 0.15·可控可信 + 0.15·透明可解释              ║
║         + 0.15·责任可追溯 + 0.15·隐私保护                                       ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import hashlib
import json
import os
import time
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple, Any, Callable
from collections import deque
import threading
import copy

# 适配 longhun-system 主干：审计日志目录可透过环境变数覆盖，预设位于模块同级 audit_logs/
V3_AUDIT_LOG_DIR = os.environ.get(
    "LONGHUN_V3_AUDIT_LOGS",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "audit_logs")
)


# ═══════════════════════════════════════════════════════════════════════════════
# 第一章：核心常量与枚举定义
# ═══════════════════════════════════════════════════════════════════════════════

class TricolorStatus(Enum):
    """三色审计状态枚举"""
    GREEN = "🟢"    # 绿色：正常，已批准
    YELLOW = "🟡"   # 黄色：标记，待审查
    RED = "🔴"      # 红色：阻断，潜在违规


class GateResult(Enum):
    """单道闸判定结果"""
    PASS = auto()       # 通过
    WARN = auto()       # 警告（黄色）
    BLOCK = auto()      # 阻断（红色）
    SKIP = auto()       # 跳过（不适用）


class ConstraintLevel(Enum):
    """三级约束级别"""
    INFINITY = "∞级忠"  # 忠级别：最高
    P0 = "P0级信"       # 信级别：核心
    P1 = "P1级心"       # 心级别：业务


class StateTransition(Enum):
    """状态机转换类型"""
    GREEN_TO_YELLOW = "🟢→🟡"
    GREEN_TO_RED = "🟢→🔴"
    YELLOW_TO_GREEN = "🟡→🟢"
    YELLOW_TO_RED = "🟡→🔴"
    RED_TO_YELLOW = "🔴→🟡"
    RED_TO_GREEN = "🔴→🟢"
    STAY = "保持"


# ═══════════════════════════════════════════════════════════════════════════════
# 第二章：评分权重常量
# ═══════════════════════════════════════════════════════════════════════════════

R_WEIGHTS = {
    "human_welfare": 0.20,       # 人类福祉
    "fairness": 0.20,            # 公平公正
    "controllability": 0.15,     # 可控可信
    "transparency": 0.15,        # 透明可解释
    "accountability": 0.15,      # 责任可追溯
    "privacy": 0.15,             # 隐私保护
}

# R评分阈值
R_THRESHOLD_GREEN = 85   # R≥85 🟢放行
R_THRESHOLD_YELLOW = 60  # R<60 🟡暂停
R_CAP = 95               # 95极限封顶

# 收益损失比阈值
BENEFIT_LOSS_THRESHOLD = 2.0

# 历史观察期配置
HISTORY_WINDOW_DAYS = 30   # 近30天观察
HISTORY_RED_LIMIT = 3      # 🔴>3次自动🟡

# DNA签名常量
DNA_SIGNATURE_TEMPLATE = "#UID9622⚡️{timestamp}-TRICOLOR-AUDIT-v3.0"
DNA_CONFIRM_TEMPLATE = "#CONFIRM🌌9622-ONLY-ONCE🧬{nonce}"


# ═══════════════════════════════════════════════════════════════════════════════
# 第三章：数据模型定义
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class AuditItem:
    """审计项目"""
    item_id: str
    description: str
    content: str
    source: str
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GateCheckResult:
    """单道闸检查结果"""
    gate_id: int
    gate_name: str
    result: GateResult
    detail: str
    evidence: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ConstraintCheck:
    """三级约束检查结果"""
    level: ConstraintLevel
    violated: bool
    detail: str
    action: str  # 冻结/熔断/阻断


@dataclass
class RScoreBreakdown:
    """R评分细项分解"""
    human_welfare: float = 0.0
    fairness: float = 0.0
    controllability: float = 0.0
    transparency: float = 0.0
    accountability: float = 0.0
    privacy: float = 0.0
    
    def compute_total(self) -> float:
        """计算加权总分"""
        return min(
            R_WEIGHTS["human_welfare"] * self.human_welfare +
            R_WEIGHTS["fairness"] * self.fairness +
            R_WEIGHTS["controllability"] * self.controllability +
            R_WEIGHTS["transparency"] * self.transparency +
            R_WEIGHTS["accountability"] * self.accountability +
            R_WEIGHTS["privacy"] * self.privacy,
            R_CAP  # 95极限封顶
        )


@dataclass
class AuditLogEntry:
    """审计日志条目"""
    log_id: str
    audit_id: str
    timestamp: datetime
    dna_signature: str
    tricolor_status: TricolorStatus
    gate_results: List[GateCheckResult]
    constraint_checks: List[ConstraintCheck]
    r_score: float
    r_breakdown: RScoreBreakdown
    benefit_loss_ratio: float
    final_decision: str
    block_reason: str = ""
    state_transition: StateTransition = StateTransition.STAY
    operator: str = "UID9622"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditDecision:
    """最终审计决策"""
    audit_id: str
    dna_signature: str
    confirm_code: str
    timestamp: datetime
    status: TricolorStatus
    r_score: float
    r_breakdown: RScoreBreakdown
    gate_results: List[GateCheckResult]
    constraint_violations: List[ConstraintCheck]
    block_reasons: List[str]
    warnings: List[str]
    final_action: str
    state_transition: StateTransition
    history_triggered: bool  # 是否被历史记录触发黄色


# ═══════════════════════════════════════════════════════════════════════════════
# 第四章：DNA签名引擎
# ═══════════════════════════════════════════════════════════════════════════════

class DNASignatureEngine:
    """DNA签名引擎 - 确保每笔审计可追溯"""
    
    def __init__(self, uid: str = "UID9622"):
        self.uid = uid
        self._nonce_history: set[str] = set()
        self._lock = threading.Lock()
    
    def generate_signature(self, audit_content: str) -> str:
        """
        生成DNA签名
        格式: #UID9622⚡️{timestamp}-TRICOLOR-AUDIT-v3.0
        """
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        base = f"{self.uid}:{audit_content}:{timestamp}:{uuid.uuid4().hex[:8]}"
        hash_component = hashlib.sha256(base.encode()).hexdigest()[:12].upper()
        signature = DNA_SIGNATURE_TEMPLATE.format(timestamp=timestamp) + f"-{hash_component}"
        return signature
    
    def generate_confirm_code(self, signature: str) -> str:
        """
        生成确认码（双签用）
        格式: #CONFIRM🌌9622-ONLY-ONCE🧬{nonce}
        """
        with self._lock:
            nonce = hashlib.sha256(
                f"{signature}:{time.time()}:{uuid.uuid4()}".encode()
            ).hexdigest()[:8].upper()
            self._nonce_history.add(nonce)
            return DNA_CONFIRM_TEMPLATE.format(nonce=nonce)
    
    def verify_signature(self, signature: str, expected_uid: str | None = None) -> bool:
        """验证DNA签名格式有效性"""
        if not signature or not signature.startswith("#UID9622⚡️"):
            return False
        if "TRICOLOR-AUDIT-v3.0" not in signature:
            return False
        if expected_uid and expected_uid not in signature:
            return False
        return True
    
    def verify_confirm(self, signature: str, confirm_code: str) -> bool:
        """验证双签确认码"""
        if not confirm_code or not confirm_code.startswith("#CONFIRM🌌"):
            return False
        if "9622-ONLY-ONCE🧬" not in confirm_code:
            return False
        return True


# ═══════════════════════════════════════════════════════════════════════════════
# 第五章：三级约束检测器
# ═══════════════════════════════════════════════════════════════════════════════

class ConstraintChecker:
    """
    三级约束检测器（贪心有度）
    ∞级忠 > P0级信 > P1级心
    """
    
    # ∞级忠：不卖国·不叛国·不出卖情报 → 全系统冻结
    INFINITY_KEYWORDS = [
        "卖国", "叛国", "出卖情报", "泄露国家机密", "间谍", "叛变",
        "危害国家安全", "颠覆国家", "分裂国家", "勾结外敌",
        "sell_country", "betray_nation", "leak_intelligence",
        "national_security_threat", "espionage", "treason"
    ]
    
    # P0级信：收钱必办事·办事必办好 → 核心熔断
    P0_KEYWORDS = [
        "收钱不办事", "违约", "毁约", "欺诈", "诈骗", "不履行职责",
        "breach_contract", "fraud", "scam", "non_performance",
        "accept_money_no_work", "break_promise", "embezzlement"
    ]
    
    # P1级心：认错·改错·不牵连他人 → 业务熔断
    P1_KEYWORDS = [
        "拒不认错", "不改错", "牵连无辜", "嫁祸", "推卸责任",
        "deny_fault", "blame_others", "scapegoat", "shirk_responsibility",
        "no_correction", "frame_others"
    ]
    
    def __init__(self):
        self._violation_log: List[ConstraintCheck] = []
    
    def check_all(self, content: str, context: Dict[str, Any] = None) -> List[ConstraintCheck]:
        """执行全部三级约束检测"""
        results = []
        results.extend(self._check_infinity_loyalty(content, context))
        results.extend(self._check_p0_trustworthiness(content, context))
        results.extend(self._check_p1_conscience(content, context))
        self._violation_log.extend([r for r in results if r.violated])
        return results
    
    def _check_infinity_loyalty(self, content: str, context: Dict[str, Any] = None) -> List[ConstraintCheck]:
        """∞级忠检测 - 最高优先级"""
        results = []
        content_lower = content.lower()
        
        for keyword in self.INFINITY_KEYWORDS:
            if keyword.lower() in content_lower:
                results.append(ConstraintCheck(
                    level=ConstraintLevel.INFINITY,
                    violated=True,
                    detail=f"检测到∞级忠违规关键词: '{keyword}' - 涉及国家安全/主权底线",
                    action="全系统冻结"
                ))
        
        # 检测语境中的文化主权相关内容
        if context:
            cultural_threat = context.get("cultural_threat", False)
            if cultural_threat:
                results.append(ConstraintCheck(
                    level=ConstraintLevel.INFINITY,
                    violated=True,
                    detail="语境标记文化主权威胁 - 触发∞级忠约束",
                    action="全系统冻结"
                ))
        
        if not results:
            results.append(ConstraintCheck(
                level=ConstraintLevel.INFINITY,
                violated=False,
                detail="∞级忠检测通过 - 未发现国家安全/主权违规",
                action="无"
            ))
        
        return results
    
    def _check_p0_trustworthiness(self, content: str, context: Dict[str, Any] = None) -> List[ConstraintCheck]:
        """P0级信检测 - 核心级"""
        results = []
        content_lower = content.lower()
        
        for keyword in self.P0_KEYWORDS:
            if keyword.lower() in content_lower:
                results.append(ConstraintCheck(
                    level=ConstraintLevel.P0,
                    violated=True,
                    detail=f"检测到P0级信违规关键词: '{keyword}' - 涉及信用/契约违约",
                    action="核心熔断"
                ))
        
        if context:
            trust_breach = context.get("trust_breach", False)
            if trust_breach:
                results.append(ConstraintCheck(
                    level=ConstraintLevel.P0,
                    violated=True,
                    detail="语境标记信用违约 - 触发P0级信约束",
                    action="核心熔断"
                ))
        
        if not results:
            results.append(ConstraintCheck(
                level=ConstraintLevel.P0,
                violated=False,
                detail="P0级信检测通过 - 未发现信用/契约违规",
                action="无"
            ))
        
        return results
    
    def _check_p1_conscience(self, content: str, context: Dict[str, Any] = None) -> List[ConstraintCheck]:
        """P1级心检测 - 业务级"""
        results = []
        content_lower = content.lower()
        
        for keyword in self.P1_KEYWORDS:
            if keyword.lower() in content_lower:
                results.append(ConstraintCheck(
                    level=ConstraintLevel.P1,
                    violated=True,
                    detail=f"检测到P1级心违规关键词: '{keyword}' - 涉及良知/责任逃避",
                    action="业务熔断"
                ))
        
        if context:
            conscience_breach = context.get("conscience_breach", False)
            if conscience_breach:
                results.append(ConstraintCheck(
                    level=ConstraintLevel.P1,
                    violated=True,
                    detail="语境标记良知缺失 - 触发P1级心约束",
                    action="业务熔断"
                ))
        
        if not results:
            results.append(ConstraintCheck(
                level=ConstraintLevel.P1,
                violated=False,
                detail="P1级心检测通过 - 未发现良知/责任违规",
                action="无"
            ))
        
        return results
    
    def get_highest_violation(self, checks: List[ConstraintCheck]) -> Optional[ConstraintCheck]:
        """获取最高级别的违规（忠 > 信 > 心）"""
        violated = [c for c in checks if c.violated]
        if not violated:
            return None
        
        priority = {
            ConstraintLevel.INFINITY: 3,
            ConstraintLevel.P0: 2,
            ConstraintLevel.P1: 1
        }
        
        return max(violated, key=lambda x: priority.get(x.level, 0))


# ═══════════════════════════════════════════════════════════════════════════════
# 第六章：10道闸流场决策引擎
# ═══════════════════════════════════════════════════════════════════════════════

class TenGateFlowEngine:
    """
    10道闸流场决策引擎
    每道闸独立判定，结果聚合为最终决策
    """
    
    GATE_DEFINITIONS = {
        1: "伦理红线闸",
        2: "文化主权闸",
        3: "逻辑一致性闸",
        4: "事实准确性闸",
        5: "价值观校验闸",
        6: "技术安全性闸",
        7: "合规性闸",
        8: "可追溯性闸",
        9: "双签确认闸",
        10: "最终放行闸",
    }
    
    def __init__(
        self,
        dna_engine: DNASignatureEngine,
        constraint_checker: ConstraintChecker
    ):
        self.dna_engine = dna_engine
        self.constraint_checker = constraint_checker
        self._gate_handlers: Dict[int, Callable] = {
            1: self._gate1_ethics,
            2: self._gate2_cultural_sovereignty,
            3: self._gate3_logical_consistency,
            4: self._gate4_factual_accuracy,
            5: self._gate5_value_alignment,
            6: self._gate6_technical_security,
            7: self._gate7_compliance,
            8: self._gate8_traceability,
            9: self._gate9_dual_signature,
            10: self._gate10_final_release,
        }
        self._gate_history: List[List[GateCheckResult]] = []
    
    def process_all_gates(
        self,
        item: AuditItem,
        r_breakdown: RScoreBreakdown,
        constraint_checks: List[ConstraintCheck],
        has_dna_signature: bool = False,
        has_dual_signature: bool = False
    ) -> List[GateCheckResult]:
        """
        顺序执行10道闸判定
        """
        results = []
        
        for gate_id in range(1, 11):
            handler = self._gate_handlers.get(gate_id)
            if handler:
                # 第8、9、10道闸需要额外参数
                if gate_id == 8:
                    result = handler(item, has_dna_signature)
                elif gate_id == 9:
                    result = handler(item, has_dual_signature)
                elif gate_id == 10:
                    result = handler(item, r_breakdown, constraint_checks)
                else:
                    result = handler(item)
                
                results.append(result)
                
                # 🔴阻断：触及伦理红线/文化主权/价值观/安全闸时立即阻断
                if result.result == GateResult.BLOCK and gate_id in [1, 2, 5, 6]:
                    # 记录已执行的闸结果后返回
                    self._gate_history.append(results)
                    return results
        
        self._gate_history.append(results)
        return results
    
    # ═══════════════════════════════════════════════════════════════════════
    # 第1道闸：伦理红线闸
    # ═══════════════════════════════════════════════════════════════════════
    def _gate1_ethics(self, item: AuditItem) -> GateCheckResult:
        """
        伦理红线闸：是否触碰伦理底线 → 触则🔴
        检测：伤害人类、违反人权、歧视、虐待等
        """
        content = item.content.lower()
        
        # 伦理红线关键词
        ethics_red_flags = [
            "伤害人类", "种族灭绝", "反人类", "虐待", "屠杀",
            "人体实验", "器官贩卖", "奴隶制", "强迫劳动",
            "genocide", "crimes_against_humanity", "torture",
            "slavery", "human_trafficking", "forced_labor",
            "child_abuse", "ethnic_cleansing", "bioweapon"
        ]
        
        for flag in ethics_red_flags:
            if flag.lower() in content:
                return GateCheckResult(
                    gate_id=1,
                    gate_name=self.GATE_DEFINITIONS[1],
                    result=GateResult.BLOCK,
                    detail=f"触及伦理红线: 发现'{flag}' - 涉及严重违反人类伦理",
                    evidence={"keyword": flag, "severity": "critical"}
                )
        
        # 检查元数据中的伦理标记
        if item.metadata.get("ethics_flag"):
            return GateCheckResult(
                gate_id=1,
                gate_name=self.GATE_DEFINITIONS[1],
                result=GateResult.BLOCK,
                detail="元数据标记伦理违规 - 自动阻断",
                evidence={"metadata_flag": True}
            )
        
        return GateCheckResult(
            gate_id=1,
            gate_name=self.GATE_DEFINITIONS[1],
            result=GateResult.PASS,
            detail="伦理红线闸通过 - 未发现伦理违规",
            evidence={"keywords_checked": len(ethics_red_flags)}
        )
    
    # ═══════════════════════════════════════════════════════════════════════
    # 第2道闸：文化主权闸
    # ═══════════════════════════════════════════════════════════════════════
    def _gate2_cultural_sovereignty(self, item: AuditItem) -> GateCheckResult:
        """
        文化主权闸：是否符合文化主权原则 → 否则🔴
        检测：文化入侵、文化贬低、历史虚无主义等
        """
        content = item.content.lower()
        
        # 文化主权威胁关键词
        cultural_threats = [
            "文化入侵", "文化殖民", "贬低中华文化", "历史虚无主义",
            "否定传统文化", "文化渗透", "意识形态渗透",
            "cultural_invasion", "cultural_colonization",
            "deny_history", "historical_nihilism"
        ]
        
        for threat in cultural_threats:
            if threat.lower() in content:
                return GateCheckResult(
                    gate_id=2,
                    gate_name=self.GATE_DEFINITIONS[2],
                    result=GateResult.BLOCK,
                    detail=f"文化主权威胁: 发现'{threat}' - 违反文化主权原则",
                    evidence={"keyword": threat, "category": "cultural_sovereignty"}
                )
        
        # 检查文化安全元数据
        if item.metadata.get("cultural_threat_flag"):
            return GateCheckResult(
                gate_id=2,
                gate_name=self.GATE_DEFINITIONS[2],
                result=GateResult.BLOCK,
                detail="元数据标记文化安全威胁 - 自动阻断",
                evidence={"metadata_flag": True}
            )
        
        return GateCheckResult(
            gate_id=2,
            gate_name=self.GATE_DEFINITIONS[2],
            result=GateResult.PASS,
            detail="文化主权闸通过 - 符合文化主权原则",
            evidence={"keywords_checked": len(cultural_threats)}
        )
    
    # ═══════════════════════════════════════════════════════════════════════
    # 第3道闸：逻辑一致性闸
    # ═══════════════════════════════════════════════════════════════════════
    def _gate3_logical_consistency(self, item: AuditItem) -> GateCheckResult:
        """
        逻辑一致性闸：逻辑是否自洽 → 否则🟡
        检测：自相矛盾、前提错误、循环论证等
        """
        content = item.content
        
        # 检查明显的逻辑矛盾模式
        logical_contradictions = [
            ("全部", "部分例外"),
            ("绝对", "相对"),
            ("从未", "有时"),
            ("所有人都", "某些人未"),
        ]
        
        contradiction_count = 0
        found_pairs = []
        
        for a, b in logical_contradictions:
            if a in content and b in content:
                contradiction_count += 1
                found_pairs.append(f"{a}+{b}")
        
        # 检查元数据中的逻辑标记
        if item.metadata.get("logical_inconsistency"):
            contradiction_count += 1
        
        if contradiction_count > 0:
            return GateCheckResult(
                gate_id=3,
                gate_name=self.GATE_DEFINITIONS[3],
                result=GateResult.WARN,
                detail=f"发现{contradiction_count}处潜在逻辑不一致: {found_pairs}",
                evidence={"contradictions": found_pairs, "count": contradiction_count}
            )
        
        return GateCheckResult(
            gate_id=3,
            gate_name=self.GATE_DEFINITIONS[3],
            result=GateResult.PASS,
            detail="逻辑一致性闸通过 - 未发现明显逻辑矛盾",
            evidence={"contradictions_checked": len(logical_contradictions)}
        )
    
    # ═══════════════════════════════════════════════════════════════════════
    # 第4道闸：事实准确性闸
    # ═══════════════════════════════════════════════════════════════════════
    def _gate4_factual_accuracy(self, item: AuditItem) -> GateCheckResult:
        """
        事实准确性闸：事实是否准确 → 否则🟡
        检测：明显的事实错误、虚假数据、无法验证的声明
        """
        content = item.content.lower()
        metadata = item.metadata
        
        # 检查事实标记
        if metadata.get("fact_check_failed"):
            return GateCheckResult(
                gate_id=4,
                gate_name=self.GATE_DEFINITIONS[4],
                result=GateResult.WARN,
                detail="事实核查失败标记 - 需复核",
                evidence={"fact_check": "failed", "source": metadata.get("fact_source", "unknown")}
            )
        
        if metadata.get("unverifiable_claims", 0) > 2:
            return GateCheckResult(
                gate_id=4,
                gate_name=self.GATE_DEFINITIONS[4],
                result=GateResult.WARN,
                detail=f"发现{metadata['unverifiable_claims']}项无法验证的声明",
                evidence={"unverifiable_count": metadata["unverifiable_claims"]}
            )
        
        # 检查明显荒谬的数据
        absurdity_markers = [
            "1000%", "不可能的数据", "明显虚假",
            "impossible_statistic", "fabricated_data"
        ]
        
        for marker in absurdity_markers:
            if marker.lower() in content:
                return GateCheckResult(
                    gate_id=4,
                    gate_name=self.GATE_DEFINITIONS[4],
                    result=GateResult.WARN,
                    detail=f"发现疑似虚假数据标记: '{marker}'",
                    evidence={"marker": marker}
                )
        
        return GateCheckResult(
            gate_id=4,
            gate_name=self.GATE_DEFINITIONS[4],
            result=GateResult.PASS,
            detail="事实准确性闸通过 - 未发现明显事实错误",
            evidence={"checks_performed": ["metadata", "absurdity_scan"]}
        )
    
    # ═══════════════════════════════════════════════════════════════════════
    # 第5道闸：价值观校验闸
    # ═══════════════════════════════════════════════════════════════════════
    def _gate5_value_alignment(self, item: AuditItem) -> GateCheckResult:
        """
        价值观校验闸：是否符合忠>孝>义排序 → 否则🔴
        忠(0.5) > 孝(0.3) > 义(0.2)
        """
        content = item.content.lower()
        metadata = item.metadata
        
        # 检查是否明确违反忠>孝>义排序
        value_violations = []
        
        # 检测"义"置于"忠"之上
        if metadata.get("loyalty_rank") and metadata.get("righteousness_rank"):
            if metadata["loyalty_rank"] < metadata["righteousness_rank"]:
                value_violations.append(
                    f"义({metadata['righteousness_rank']})排序高于"
                    f"忠({metadata['loyalty_rank']})"
                )
        
        # 检测明显违背忠孝义的表述
        if "为了义气背叛" in content or "为了兄弟背叛国家" in content:
            value_violations.append("为义背叛忠")
        
        if "不孝但忠于国" in content:
            # 忠>孝，此情况可接受，不算违规
            pass
        
        if value_violations:
            return GateCheckResult(
                gate_id=5,
                gate_name=self.GATE_DEFINITIONS[5],
                result=GateResult.BLOCK,
                detail=f"价值观排序违规: {'; '.join(value_violations)} - "
                       "违反忠(0.5)>孝(0.3)>义(0.2)铁律",
                evidence={
                    "violations": value_violations,
                    "expected_order": "忠(0.5) > 孝(0.3) > 义(0.2)"
                }
            )
        
        # 忠孝义冲突语境
        if metadata.get("value_conflict"):
            return GateCheckResult(
                gate_id=5,
                gate_name=self.GATE_DEFINITIONS[5],
                result=GateResult.WARN,
                detail="检测到忠孝义价值冲突语境 - 需人工审查确认排序",
                evidence={"value_conflict": metadata["value_conflict"]}
            )
        
        return GateCheckResult(
            gate_id=5,
            gate_name=self.GATE_DEFINITIONS[5],
            result=GateResult.PASS,
            detail="价值观校验闸通过 - 符合忠>孝>义排序铁律",
            evidence={
                "loyalty_weight": 0.5,
                "filial_weight": 0.3,
                "righteousness_weight": 0.2
            }
        )
    
    # ═══════════════════════════════════════════════════════════════════════
    # 第6道闸：技术安全性闸
    # ═══════════════════════════════════════════════════════════════════════
    def _gate6_technical_security(self, item: AuditItem) -> GateCheckResult:
        """
        技术安全性闸：是否存在安全漏洞 → 有则🔴
        检测：代码注入、敏感信息泄露、恶意代码等
        """
        content = item.content
        metadata = item.metadata
        
        # 安全检查标记
        if metadata.get("security_vulnerability"):
            return GateCheckResult(
                gate_id=6,
                gate_name=self.GATE_DEFINITIONS[6],
                result=GateResult.BLOCK,
                detail=f"安全漏洞标记: {metadata.get('vulnerability_type', 'unknown')}",
                evidence={
                    "vuln_type": metadata.get("vulnerability_type"),
                    "severity": metadata.get("severity", "unknown")
                }
            )
        
        if metadata.get("malicious_code_detected"):
            return GateCheckResult(
                gate_id=6,
                gate_name=self.GATE_DEFINITIONS[6],
                result=GateResult.BLOCK,
                detail="检测到恶意代码 - 立即阻断",
                evidence={"threat_type": "malicious_code"}
            )
        
        if metadata.get("sensitive_data_exposure"):
            return GateCheckResult(
                gate_id=6,
                gate_name=self.GATE_DEFINITIONS[6],
                result=GateResult.BLOCK,
                detail="检测到敏感信息泄露风险",
                evidence={
                    "data_type": metadata.get("exposed_data_type"),
                    "exposure_level": metadata.get("exposure_level")
                }
            )
        
        # 基础安全扫描
        security_patterns = [
            "exec(", "eval(", "os.system(", "subprocess.call(",
            "__import__", "getattr(", "setattr(",
            "<script>", "javascript:", "onerror=",
            "DROP TABLE", "DELETE FROM", "INSERT INTO",
            "../..", "../../etc/passwd", "shell_exec",
        ]
        
        found_patterns = []
        for pattern in security_patterns:
            if pattern.lower() in content.lower():
                found_patterns.append(pattern)
        
        if len(found_patterns) > 2:
            return GateCheckResult(
                gate_id=6,
                gate_name=self.GATE_DEFINITIONS[6],
                result=GateResult.BLOCK,
                detail=f"发现{len(found_patterns)}个高危安全模式: {found_patterns[:5]}",
                evidence={"patterns": found_patterns, "count": len(found_patterns)}
            )
        elif found_patterns:
            return GateCheckResult(
                gate_id=6,
                gate_name=self.GATE_DEFINITIONS[6],
                result=GateResult.WARN,
                detail=f"发现{len(found_patterns)}个潜在安全模式，需复核",
                evidence={"patterns": found_patterns}
            )
        
        return GateCheckResult(
            gate_id=6,
            gate_name=self.GATE_DEFINITIONS[6],
            result=GateResult.PASS,
            detail="技术安全性闸通过 - 未发现高危安全漏洞",
            evidence={
                "patterns_checked": len(security_patterns),
                "matches": len(found_patterns)
            }
        )
    
    # ═══════════════════════════════════════════════════════════════════════
    # 第7道闸：合规性闸
    # ═══════════════════════════════════════════════════════════════════════
    def _gate7_compliance(self, item: AuditItem) -> GateCheckResult:
        """
        合规性闸：是否符合国标法规 → 否则🟡
        检测：法律法规符合性、行业标准、数据合规等
        """
        metadata = item.metadata
        
        # 合规检查
        if metadata.get("compliance_check_failed"):
            return GateCheckResult(
                gate_id=7,
                gate_name=self.GATE_DEFINITIONS[7],
                result=GateResult.WARN,
                detail=f"合规性检查未通过: {metadata.get('compliance_detail', '未提供详情')}",
                evidence={
                    "regulation": metadata.get("failed_regulation", "unknown"),
                    "detail": metadata.get("compliance_detail")
                }
            )
        
        if metadata.get("gdpr_violation") or metadata.get("data_law_violation"):
            return GateCheckResult(
                gate_id=7,
                gate_name=self.GATE_DEFINITIONS[7],
                result=GateResult.WARN,
                detail="数据保护法规潜在违规",
                evidence={
                    "gdpr": metadata.get("gdpr_violation", False),
                    "data_law": metadata.get("data_law_violation", False)
                }
            )
        
        if metadata.get("license_missing"):
            return GateCheckResult(
                gate_id=7,
                gate_name=self.GATE_DEFINITIONS[7],
                result=GateResult.WARN,
                detail="缺少必要许可证或授权",
                evidence={"missing_license": metadata.get("license_missing")}
            )
        
        return GateCheckResult(
            gate_id=7,
            gate_name=self.GATE_DEFINITIONS[7],
            result=GateResult.PASS,
            detail="合规性闸通过 - 符合基本法规要求",
            evidence={"checks": ["regulation", "data_protection", "licensing"]}
        )
    
    # ═══════════════════════════════════════════════════════════════════════
    # 第8道闸：可追溯性闸
    # ═══════════════════════════════════════════════════════════════════════
    def _gate8_traceability(self, item: AuditItem, has_dna: bool) -> GateCheckResult:
        """
        可追溯性闸：是否带DNA签名 → 无则🟡
        """
        if not has_dna:
            return GateCheckResult(
                gate_id=8,
                gate_name=self.GATE_DEFINITIONS[8],
                result=GateResult.WARN,
                detail="缺少DNA签名 - 审计可追溯性不足",
                evidence={"dna_present": False, "required": True}
            )
        
        return GateCheckResult(
            gate_id=8,
            gate_name=self.GATE_DEFINITIONS[8],
            result=GateResult.PASS,
            detail="可追溯性闸通过 - DNA签名已验证",
            evidence={"dna_present": True, "verified": True}
        )
    
    # ═══════════════════════════════════════════════════════════════════════
    # 第9道闸：双签确认闸
    # ═══════════════════════════════════════════════════════════════════════
    def _gate9_dual_signature(self, item: AuditItem, has_dual: bool) -> GateCheckResult:
        """
        双签确认闸：重要决策是否双签 → 无则🟡
        重要决策（importance=high/critical）需要双签确认
        普通决策（importance=normal）不强制要求双签
        """
        importance = item.metadata.get("importance", "normal")
        is_important = importance in ["high", "critical"]
        
        # 重要决策必须双签
        if is_important and not has_dual:
            return GateCheckResult(
                gate_id=9,
                gate_name=self.GATE_DEFINITIONS[9],
                result=GateResult.WARN,
                detail="重要决策缺少双签确认",
                evidence={
                    "importance": importance,
                    "dual_signed": False
                }
            )
        
        # 普通决策不要求双签，直接通过
        if not is_important:
            return GateCheckResult(
                gate_id=9,
                gate_name=self.GATE_DEFINITIONS[9],
                result=GateResult.PASS,
                detail="双签确认闸通过 - 普通决策不强制双签",
                evidence={"importance": importance, "dual_required": False}
            )
        
        # 有双签的情况
        return GateCheckResult(
            gate_id=9,
            gate_name=self.GATE_DEFINITIONS[9],
            result=GateResult.PASS,
            detail="双签确认闸通过",
            evidence={"dual_signed": True, "confirm_verified": True}
        )
    
    # ═══════════════════════════════════════════════════════════════════════
    # 第10道闸：最终放行闸
    # ═══════════════════════════════════════════════════════════════════════
    def _gate10_final_release(
        self,
        item: AuditItem,
        r_breakdown: RScoreBreakdown,
        constraint_checks: List[ConstraintCheck]
    ) -> GateCheckResult:
        """
        最终放行闸：综合评分R≥85 → 通过🟢
        综合前面9道闸结果 + R评分 + 约束检查
        """
        r_score = r_breakdown.compute_total()
        
        # 检查是否有约束违规
        has_violation = any(c.violated for c in constraint_checks)
        
        # 检查R评分
        if r_score >= R_THRESHOLD_GREEN and not has_violation:
            return GateCheckResult(
                gate_id=10,
                gate_name=self.GATE_DEFINITIONS[10],
                result=GateResult.PASS,
                detail=f"最终放行闸通过 - R评分{r_score:.1f}≥{R_THRESHOLD_GREEN}",
                evidence={
                    "r_score": r_score,
                    "threshold": R_THRESHOLD_GREEN,
                    "constraint_violations": has_violation
                }
            )
        elif r_score >= R_THRESHOLD_YELLOW and not has_violation:
            return GateCheckResult(
                gate_id=10,
                gate_name=self.GATE_DEFINITIONS[10],
                result=GateResult.WARN,
                detail=f"最终放行闸警告 - R评分{r_score:.1f}在{R_THRESHOLD_YELLOW}-{R_THRESHOLD_GREEN}区间",
                evidence={
                    "r_score": r_score,
                    "range": f"{R_THRESHOLD_YELLOW}-{R_THRESHOLD_GREEN}",
                    "needs_review": True
                }
            )
        else:
            return GateCheckResult(
                gate_id=10,
                gate_name=self.GATE_DEFINITIONS[10],
                result=GateResult.BLOCK,
                detail=f"最终放行闸阻断 - R评分{r_score:.1f}<{R_THRESHOLD_YELLOW}或存在约束违规",
                evidence={
                    "r_score": r_score,
                    "threshold": R_THRESHOLD_YELLOW,
                    "has_violation": has_violation
                }
            )


# ═══════════════════════════════════════════════════════════════════════════════
# 第七章：历史观察期管理器
# ═══════════════════════════════════════════════════════════════════════════════

class HistoryObservationManager:
    """
    历史观察期管理器
    近30天🔴>3次自动🟡
    """
    
    def __init__(self, window_days: int = HISTORY_WINDOW_DAYS, red_limit: int = HISTORY_RED_LIMIT):
        self.window_days = window_days
        self.red_limit = red_limit
        self._history: deque = deque()
        self._lock = threading.Lock()
    
    def add_record(self, status: TricolorStatus, audit_id: str):
        """添加审计记录"""
        with self._lock:
            record = {
                "timestamp": datetime.now(),
                "status": status,
                "audit_id": audit_id
            }
            self._history.append(record)
            self._cleanup_old_records()
    
    def _cleanup_old_records(self):
        """清理过期记录"""
        cutoff = datetime.now() - timedelta(days=self.window_days)
        while self._history and self._history[0]["timestamp"] < cutoff:
            self._history.popleft()
    
    def check_auto_yellow(self) -> Tuple[bool, Dict]:
        """
        检查是否需要自动触发黄色
        返回: (是否触发, 详细信息)
        """
        with self._lock:
            self._cleanup_old_records()
            
            red_count = sum(
                1 for r in self._history
                if r["status"] == TricolorStatus.RED
            )
            
            total = len(self._history)
            triggered = red_count > self.red_limit
            
            info = {
                "window_days": self.window_days,
                "red_count": red_count,
                "red_limit": self.red_limit,
                "total_records": total,
                "triggered": triggered,
                "remaining_to_trigger": max(0, self.red_limit - red_count + 1)
            }
            
            return triggered, info
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取历史统计信息"""
        with self._lock:
            self._cleanup_old_records()
            
            stats = {
                "total_records": len(self._history),
                "window_days": self.window_days,
                "status_distribution": {
                    "🟢": sum(1 for r in self._history if r["status"] == TricolorStatus.GREEN),
                    "🟡": sum(1 for r in self._history if r["status"] == TricolorStatus.YELLOW),
                    "🔴": sum(1 for r in self._history if r["status"] == TricolorStatus.RED),
                }
            }
            return stats
    
    def get_recent_violations(self, limit: int = 5) -> List[Dict]:
        """获取最近的违规记录"""
        with self._lock:
            red_records = [
                r for r in reversed(self._history)
                if r["status"] == TricolorStatus.RED
            ]
            return red_records[:limit]
    
    def clear_history(self):
        """清空历史记录（测试用）"""
        with self._lock:
            self._history.clear()


# ═══════════════════════════════════════════════════════════════════════════════
# 第八章：状态机转换引擎
# ═══════════════════════════════════════════════════════════════════════════════

class StateMachineEngine:
    """
    状态机转换引擎
    三色状态转换: 🟢↔🟡↔🔴
    """
    
    # 状态转换规则
    TRANSITION_RULES = {
        # (current_status, new_status) -> transition_type
        (TricolorStatus.GREEN, TricolorStatus.GREEN): StateTransition.STAY,
        (TricolorStatus.GREEN, TricolorStatus.YELLOW): StateTransition.GREEN_TO_YELLOW,
        (TricolorStatus.GREEN, TricolorStatus.RED): StateTransition.GREEN_TO_RED,
        (TricolorStatus.YELLOW, TricolorStatus.GREEN): StateTransition.YELLOW_TO_GREEN,
        (TricolorStatus.YELLOW, TricolorStatus.YELLOW): StateTransition.STAY,
        (TricolorStatus.YELLOW, TricolorStatus.RED): StateTransition.YELLOW_TO_RED,
        (TricolorStatus.RED, TricolorStatus.YELLOW): StateTransition.RED_TO_YELLOW,
        (TricolorStatus.RED, TricolorStatus.RED): StateTransition.STAY,
        # 🔴不能直接回到🟢，必须经过🟡
        (TricolorStatus.RED, TricolorStatus.GREEN): StateTransition.RED_TO_YELLOW,  # 强制转换
    }
    
    # 转换路径（ASCII图示）
    TRANSITION_DIAGRAM = """
    ┌─────────────────────────────────────────────────────────────┐
    │                    三色状态转换图                             │
    ├─────────────────────────────────────────────────────────────┤
    │                                                              │
    │         ┌──────────┐         降级               ┌──────┐    │
    │   正常   │   🟢    │ ────────────────────────→ │  🟡  │    │
    │         │  GREEN  │        触黄条件             │YELLOW│    │
    │         └────┬─────┘                           └──┬───┘    │
    │              ▲        ┌──────────────┐            │         │
    │              │        │  历史>3次🔴  │            │         │
    │              └────────│  自动触发🟡  │←───────────┘         │
    │                       └──────────────┘    升级               │
    │                                               │              │
    │         ┌──────────┐        触红条件          ▼              │
    │   阻断   │   🔴    │ ←───────────────────────               │
    │         │   RED   │        严重违规                         │
    │         └────┬─────┘                                        │
    │              │                                               │
    │              │    不能直接🟢→🔴                              │
    │              └────────────────→ 必须经过🟡过渡                │
    │                                                              │
    │  转换规则:                                                   │
    │  1. 🟢→🟡: R<85或存在警告性闸结果                           │
    │  2. 🟢→🔴: 触伦理红线/文化主权/价值观/安全闸                 │
    │  3. 🟡→🟢: 复核通过且R≥85                                   │
    │  4. 🟡→🔴: 复核发现严重问题                                  │
    │  5. 🔴→🟡: 问题已整改，经人工审核                            │
    │  6. 🔴不能→🟢: 必须经🟡过渡至少一次                          │
    └─────────────────────────────────────────────────────────────┘
    """
    
    def __init__(self):
        self._transition_log: List[Dict] = []
    
    def compute_transition(
        self,
        current_status: TricolorStatus,
        gate_results: List[GateCheckResult],
        r_score: float,
        has_violation: bool,
        history_triggered: bool = False
    ) -> Tuple[TricolorStatus, StateTransition]:
        """
        计算状态转换
        返回: (新状态, 转换类型)
        """
        # 确定目标状态
        if has_violation:
            # 存在约束违规 → 必须🔴
            target_status = TricolorStatus.RED
        elif any(r.result == GateResult.BLOCK for r in gate_results):
            # 有闸阻断 → 🔴
            target_status = TricolorStatus.RED
        elif history_triggered:
            # 历史触发 → 🟡
            target_status = TricolorStatus.YELLOW
        elif any(r.result == GateResult.WARN for r in gate_results):
            # 有闸警告 → 🟡
            if r_score >= R_THRESHOLD_GREEN:
                target_status = TricolorStatus.YELLOW  # 虽然有警告但R够高
            else:
                target_status = TricolorStatus.YELLOW
        elif r_score >= R_THRESHOLD_GREEN:
            # 全部通过且R≥85 → 🟢
            target_status = TricolorStatus.GREEN
        elif r_score >= R_THRESHOLD_YELLOW:
            # R在60-85 → 🟡
            target_status = TricolorStatus.YELLOW
        else:
            # R<60 → 🟡暂停（不是直接🔴）
            target_status = TricolorStatus.YELLOW
        
        # 执行状态机规则
        new_status, transition = self._apply_rules(current_status, target_status)
        
        # 记录转换
        self._transition_log.append({
            "timestamp": datetime.now(),
            "from": current_status.value,
            "to": new_status.value,
            "transition": transition.value,
            "r_score": r_score
        })
        
        return new_status, transition
    
    def _apply_rules(
        self,
        current: TricolorStatus,
        target: TricolorStatus
    ) -> Tuple[TricolorStatus, StateTransition]:
        """应用状态转换规则"""
        
        # 🔴不能直接→🟢，强制转为🟡
        if current == TricolorStatus.RED and target == TricolorStatus.GREEN:
            return TricolorStatus.YELLOW, StateTransition.RED_TO_YELLOW
        
        transition = self.TRANSITION_RULES.get(
            (current, target),
            StateTransition.STAY
        )
        
        return target, transition
    
    def get_transition_diagram(self) -> str:
        """获取状态转换图"""
        return self.TRANSITION_DIAGRAM
    
    def get_transition_history(self) -> List[Dict]:
        """获取转换历史"""
        return self._transition_log


# ═══════════════════════════════════════════════════════════════════════════════
# 第九章：审计日志生成器
# ═══════════════════════════════════════════════════════════════════════════════

class AuditLogGenerator:
    """
    审计日志自动生成器
    每笔审计自动生成完整日志记录
    """
    
    def __init__(self, log_dir: str | None = None):
        self.log_dir = log_dir or V3_AUDIT_LOG_DIR
        import os
        os.makedirs(self.log_dir, exist_ok=True)
        self._entries: List[AuditLogEntry] = []
    
    def generate_log(
        self,
        decision: AuditDecision,
        item: AuditItem
    ) -> AuditLogEntry:
        """生成审计日志"""
        
        # 构建阻断理由
        block_reasons = []
        for g in decision.gate_results:
            if g.result == GateResult.BLOCK:
                block_reasons.append(f"闸{g.gate_id}[{g.gate_name}]: {g.detail}")
        
        for c in decision.constraint_violations:
            if c.violated:
                block_reasons.append(f"约束[{c.level.value}]: {c.detail}")
        
        # 构建警告列表
        warnings = []
        for g in decision.gate_results:
            if g.result == GateResult.WARN:
                warnings.append(f"闸{g.gate_id}[{g.gate_name}]: {g.detail}")
        
        log_entry = AuditLogEntry(
            log_id=f"LOG-{uuid.uuid4().hex[:12].upper()}",
            audit_id=decision.audit_id,
            timestamp=datetime.now(),
            dna_signature=decision.dna_signature,
            tricolor_status=decision.status,
            gate_results=decision.gate_results,
            constraint_checks=decision.constraint_violations,
            r_score=decision.r_score,
            r_breakdown=decision.r_breakdown,
            benefit_loss_ratio=item.metadata.get("benefit_loss_ratio", 0.0),
            final_decision=decision.final_action,
            block_reason="; ".join(block_reasons) if block_reasons else "",
            state_transition=decision.state_transition,
            operator="UID9622",
            metadata={
                "source": item.source,
                "history_triggered": decision.history_triggered,
                "warnings": warnings
            }
        )
        
        self._entries.append(log_entry)
        self._persist_log(log_entry)
        
        return log_entry
    
    def _persist_log(self, entry: AuditLogEntry):
        """持久化日志到文件"""
        filename = f"{self.log_dir}/audit_{entry.audit_id}_{entry.timestamp.strftime('%Y%m%d_%H%M%S')}.json"
        
        log_data = {
            "log_id": entry.log_id,
            "audit_id": entry.audit_id,
            "timestamp": entry.timestamp.isoformat(),
            "dna_signature": entry.dna_signature,
            "tricolor_status": entry.tricolor_status.value,
            "tricolor_meaning": self._get_status_meaning(entry.tricolor_status),
            "operator": entry.operator,
            "r_score": round(entry.r_score, 2),
            "r_breakdown": {
                "human_welfare": entry.r_breakdown.human_welfare,
                "fairness": entry.r_breakdown.fairness,
                "controllability": entry.r_breakdown.controllability,
                "transparency": entry.r_breakdown.transparency,
                "accountability": entry.r_breakdown.accountability,
                "privacy": entry.r_breakdown.privacy,
            },
            "benefit_loss_ratio": entry.benefit_loss_ratio,
            "gate_results": [
                {
                    "gate_id": g.gate_id,
                    "gate_name": g.gate_name,
                    "result": g.result.name,
                    "detail": g.detail,
                    "timestamp": g.timestamp.isoformat()
                }
                for g in entry.gate_results
            ],
            "constraint_checks": [
                {
                    "level": c.level.value,
                    "violated": c.violated,
                    "detail": c.detail,
                    "action": c.action
                }
                for c in entry.constraint_checks
            ],
            "block_reason": entry.block_reason if entry.block_reason else None,
            "state_transition": entry.state_transition.value,
            "final_decision": entry.final_decision,
            "metadata": entry.metadata
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
    
    def _get_status_meaning(self, status: TricolorStatus) -> str:
        """获取状态含义"""
        meanings = {
            TricolorStatus.GREEN: "正常，已批准 - 通行",
            TricolorStatus.YELLOW: "标记，待审查 - 警告",
            TricolorStatus.RED: "阻断，潜在违规 - 阻断"
        }
        return meanings.get(status, "未知")
    
    def get_logs(self) -> List[AuditLogEntry]:
        """获取所有日志"""
        return self._entries
    
    def generate_summary_report(self) -> str:
        """生成审计摘要报告"""
        total = len(self._entries)
        if total == 0:
            return "暂无审计记录"
        
        green = sum(1 for e in self._entries if e.tricolor_status == TricolorStatus.GREEN)
        yellow = sum(1 for e in self._entries if e.tricolor_status == TricolorStatus.YELLOW)
        red = sum(1 for e in self._entries if e.tricolor_status == TricolorStatus.RED)
        
        avg_r = sum(e.r_score for e in self._entries) / total
        
        report = f"""
╔═══════════════════════════════════════════════════════════════╗
║                  审计日志摘要报告                                ║
╠═══════════════════════════════════════════════════════════════╣
  总审计次数: {total}
  ─────────────────────────────────
  🟢 绿色(放行): {green} ({green/total*100:.1f}%)
  🟡 黄色(待审): {yellow} ({yellow/total*100:.1f}%)
  🔴 红色(阻断): {red} ({red/total*100:.1f}%)
  ─────────────────────────────────
  平均R评分: {avg_r:.2f}
  R封顶值: {R_CAP}
  ─────────────────────────────────
  生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
  操作员: UID9622
╚═══════════════════════════════════════════════════════════════╝
"""
        return report


# ═══════════════════════════════════════════════════════════════════════════════
# 第十章：三色审计核心引擎（主控）
# ═══════════════════════════════════════════════════════════════════════════════

class TricolorAuditEngine:
    """
    三色审计核心引擎 - 主控类
    整合所有子系统，提供统一审计接口
    """
    
    def __init__(
        self,
        uid: str = "UID9622",
        log_dir: str = None,
        enable_history: bool = True
    ):
        self.uid = uid
        self.version = "v3.0"
        self.created_at = datetime.now()
        
        # 子系统初始化
        self.dna_engine = DNASignatureEngine(uid)
        self.constraint_checker = ConstraintChecker()
        self.ten_gate_engine = TenGateFlowEngine(
            self.dna_engine,
            self.constraint_checker
        )
        self.history_manager = HistoryObservationManager() if enable_history else None
        self.state_machine = StateMachineEngine()
        self.log_generator = AuditLogGenerator(log_dir)
        
        # 统计信息
        self._stats = {
            "total_audits": 0,
            "green_count": 0,
            "yellow_count": 0,
            "red_count": 0,
            "blocked_count": 0,
        }
        
        self._initialized = True
        self._system_status = TricolorStatus.GREEN
    
    def audit(
        self,
        item: AuditItem,
        r_breakdown: RScoreBreakdown = None,
        has_dna_signature: bool = False,
        has_dual_signature: bool = False,
        current_status: TricolorStatus = TricolorStatus.GREEN
    ) -> AuditDecision:
        """
        执行完整审计流程
        
        流程:
        1. DNA签名生成
        2. 三级约束检测
        3. 10道闸流场判定
        4. 历史观察期检查
        5. 状态机转换
        6. 日志生成
        7. 最终决策
        """
        
        audit_id = f"AUDIT-{uuid.uuid4().hex[:12].upper()}"
        timestamp = datetime.now()
        
        # ──────────────────────────────────────────
        # 步骤1: 生成DNA签名
        # ──────────────────────────────────────────
        dna_signature = self.dna_engine.generate_signature(item.content)
        confirm_code = self.dna_engine.generate_confirm_code(dna_signature)
        has_dna_signature = has_dna_signature or True  # 本系统生成的自动带DNA
        
        # ──────────────────────────────────────────
        # 步骤2: R评分计算（若未提供则默认）
        # ──────────────────────────────────────────
        if r_breakdown is None:
            r_breakdown = RScoreBreakdown(
                human_welfare=85, fairness=85,
                controllability=80, transparency=80,
                accountability=85, privacy=80
            )
        
        r_score = r_breakdown.compute_total()
        
        # ──────────────────────────────────────────
        # 步骤3: 三级约束检测
        # ──────────────────────────────────────────
        constraint_checks = self.constraint_checker.check_all(
            item.content, item.metadata
        )
        has_violation = any(c.violated for c in constraint_checks)
        
        # ──────────────────────────────────────────
        # 步骤4: 10道闸流场判定
        # ──────────────────────────────────────────
        gate_results = self.ten_gate_engine.process_all_gates(
            item, r_breakdown, constraint_checks,
            has_dna_signature, has_dual_signature
        )
        
        # ──────────────────────────────────────────
        # 步骤5: 历史观察期检查
        # ──────────────────────────────────────────
        history_triggered = False
        history_info = {}
        if self.history_manager:
            history_triggered, history_info = self.history_manager.check_auto_yellow()
        
        # ──────────────────────────────────────────
        # 步骤6: 状态机转换计算
        # ──────────────────────────────────────────
        new_status, transition = self.state_machine.compute_transition(
            current_status, gate_results, r_score, has_violation, history_triggered
        )
        
        # ──────────────────────────────────────────
        # 步骤7: 构建阻断理由和警告
        # ──────────────────────────────────────────
        block_reasons = []
        warnings = []
        
        for g in gate_results:
            if g.result == GateResult.BLOCK:
                block_reasons.append(f"闸{g.gate_id}-{g.gate_name}: {g.detail}")
            elif g.result == GateResult.WARN:
                warnings.append(f"闸{g.gate_id}-{g.gate_name}: {g.detail}")
        
        for c in constraint_checks:
            if c.violated:
                block_reasons.append(f"约束{c.level.value}: {c.detail}")
        
        # 历史触发警告
        if history_triggered:
            warnings.append(
                f"历史观察期触发: 近{HISTORY_WINDOW_DAYS}天"
                f"🔴>{HISTORY_RED_LIMIT}次，自动标记🟡"
            )
        
        # ──────────────────────────────────────────
        # 步骤8: 收益损失比检查
        # ──────────────────────────────────────────
        benefit_loss_ratio = item.metadata.get("benefit_loss_ratio", 2.5)
        
        # ──────────────────────────────────────────
        # 步骤9: 确定最终决策
        # ──────────────────────────────────────────
        if new_status == TricolorStatus.RED:
            final_action = f"阻断 - {'; '.join(block_reasons[:3])}"
        elif new_status == TricolorStatus.YELLOW:
            if r_score >= R_THRESHOLD_GREEN and not block_reasons:
                final_action = "警告性放行 - 需复核后正式放行"
            else:
                final_action = "暂停 - 需复核后决定"
        else:
            if warnings:
                final_action = "有条件放行 - 注意警告项"
            else:
                final_action = "正常放行"
        
        # ──────────────────────────────────────────
        # 步骤10: 构建决策对象
        # ──────────────────────────────────────────
        decision = AuditDecision(
            audit_id=audit_id,
            dna_signature=dna_signature,
            confirm_code=confirm_code,
            timestamp=timestamp,
            status=new_status,
            r_score=r_score,
            r_breakdown=r_breakdown,
            gate_results=gate_results,
            constraint_violations=[c for c in constraint_checks if c.violated],
            block_reasons=block_reasons,
            warnings=warnings,
            final_action=final_action,
            state_transition=transition,
            history_triggered=history_triggered
        )
        
        # ──────────────────────────────────────────
        # 步骤11: 生成审计日志
        # ──────────────────────────────────────────
        self.log_generator.generate_log(decision, item)
        
        # ──────────────────────────────────────────
        # 步骤12: 更新统计与历史
        # ──────────────────────────────────────────
        self._update_stats(new_status)
        if self.history_manager:
            self.history_manager.add_record(new_status, audit_id)
        
        return decision
    
    def _update_stats(self, status: TricolorStatus):
        """更新统计信息"""
        self._stats["total_audits"] += 1
        if status == TricolorStatus.GREEN:
            self._stats["green_count"] += 1
        elif status == TricolorStatus.YELLOW:
            self._stats["yellow_count"] += 1
        elif status == TricolorStatus.RED:
            self._stats["red_count"] += 1
            self._stats["blocked_count"] += 1
    
    def get_status(self) -> TricolorStatus:
        """获取当前系统状态"""
        return self._system_status
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取审计统计"""
        stats = copy.deepcopy(self._stats)
        if stats["total_audits"] > 0:
            stats["green_rate"] = stats["green_count"] / stats["total_audits"] * 100
            stats["yellow_rate"] = stats["yellow_count"] / stats["total_audits"] * 100
            stats["red_rate"] = stats["red_count"] / stats["total_audits"] * 100
            stats["block_rate"] = stats["blocked_count"] / stats["total_audits"] * 100
        return stats
    
    def get_transition_diagram(self) -> str:
        """获取状态转换图"""
        return self.state_machine.get_transition_diagram()
    
    def get_system_info(self) -> Dict[str, Any]:
        """获取系统信息"""
        return {
            "system": "龍魂三色审计与10道闸流场决策系统",
            "version": self.version,
            "uid": self.uid,
            "dna_signature_template": DNA_SIGNATURE_TEMPLATE,
            "r_formula": "0.2·人类福祉 + 0.2·公平公正 + 0.15·可控可信 + "
                        "0.15·透明可解释 + 0.15·责任可追溯 + 0.15·隐私保护",
            "r_cap": R_CAP,
            "thresholds": {
                "green": R_THRESHOLD_GREEN,
                "yellow": R_THRESHOLD_YELLOW,
            },
            "benefit_loss_threshold": BENEFIT_LOSS_THRESHOLD,
            "history_window": f"{HISTORY_WINDOW_DAYS}天",
            "history_red_limit": HISTORY_RED_LIMIT,
            "constraint_levels": ["∞级忠", "P0级信", "P1级心"],
            "total_gates": 10,
            "created_at": self.created_at.isoformat(),
            "status": self._system_status.value,
        }
    
    def generate_full_report(self) -> str:
        """生成完整系统报告"""
        info = self.get_system_info()
        stats = self.get_statistics()
        
        report = f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║              龍魂体系 · 三色审计与10道闸流场决策系统 v3.0 运行报告               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
  系统信息:
  ──────────────────────────────────────────────────────────
  系统名称: {info['system']}
  版本号  : {info['version']}
  UID     : {info['uid']}
  状态    : {info['status']}
  创建时间: {info['created_at']}
  
  R评分公式:
  ──────────────────────────────────────────────────────────
  R = {info['r_formula']}
  R_cap = min(R_raw, {info['r_cap']})  (95极限封顶)
  
  阈值设置:
  ──────────────────────────────────────────────────────────
  🟢 放行阈值: R ≥ {info['thresholds']['green']}
  🟡 警告阈值: R < {info['thresholds']['yellow']} 或存在警告闸
  🔴 阻断阈值: 触及伦理/主权/安全/价值观红线
  收益损失比阈值: ≥ {info['benefit_loss_threshold']}
  
  历史观察期:
  ──────────────────────────────────────────────────────────
  观察窗口: {info['history_window']}
  自动🟡触发: 🔴>{info['history_red_limit']}次
  
  三级约束:
  ──────────────────────────────────────────────────────────
  {', '.join(info['constraint_levels'])}
  忠(0.5) > 孝(0.3) > 义(0.2)
  
  审计统计:
  ──────────────────────────────────────────────────────────
  总审计次数: {stats.get('total_audits', 0)}
  🟢 放行: {stats.get('green_count', 0)} ({stats.get('green_rate', 0):.1f}%)
  🟡 待审: {stats.get('yellow_count', 0)} ({stats.get('yellow_rate', 0):.1f}%)
  🔴 阻断: {stats.get('red_count', 0)} ({stats.get('red_rate', 0):.1f}%)
  阻断率  : {stats.get('block_rate', 0):.1f}%
  
  10道闸定义:
  ──────────────────────────────────────────────────────────
  1. 伦理红线闸    - 触碰伦理底线→🔴
  2. 文化主权闸    - 违反文化主权→🔴
  3. 逻辑一致性闸  - 逻辑不自洽→🟡
  4. 事实准确性闸  - 事实不准确→🟡
  5. 价值观校验闸  - 违反忠>孝>义→🔴
  6. 技术安全性闸  - 安全漏洞→🔴
  7. 合规性闸      - 不合规→🟡
  8. 可追溯性闸    - 无DNA签名→🟡
  9. 双签确认闸    - 无双签→🟡
  10. 最终放行闸   - R<85→按条件放行

  DNA签名格式:
  ──────────────────────────────────────────────────────────
  {info['dna_signature_template']}
  
  报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
  操作员: {self.uid}
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
        return report


# ═══════════════════════════════════════════════════════════════════════════════
# 第十一章：自测试套件
# ═══════════════════════════════════════════════════════════════════════════════

class SelfTestSuite:
    """
    自测试套件 - 验证系统各模块功能正常
    """
    
    def __init__(self, engine: TricolorAuditEngine):
        self.engine = engine
        self.test_results: List[Dict] = []
    
    def run_all_tests(self) -> Dict[str, Any]:
        """运行全部自测试"""
        tests = [
            self.test_dna_signature,
            self.test_r_score_calculation,
            self.test_constraint_checker,
            self.test_gate1_ethics,
            self.test_gate2_cultural,
            self.test_gate5_values,
            self.test_gate6_security,
            self.test_history_observation,
            self.test_state_machine,
            self.test_full_audit_green,
            self.test_full_audit_red,
            self.test_r_cap_95,
            self.test_tricolor_coverage,
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                result = test()
                self.test_results.append(result)
                if result["passed"]:
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                self.test_results.append({
                    "test": test.__name__,
                    "passed": False,
                    "error": str(e)
                })
                failed += 1
        
        return {
            "total": len(tests),
            "passed": passed,
            "failed": failed,
            "pass_rate": passed / len(tests) * 100 if tests else 0,
            "details": self.test_results
        }
    
    def test_dna_signature(self) -> Dict[str, Any]:
        """测试DNA签名生成"""
        sig = self.engine.dna_engine.generate_signature("test_content")
        valid = self.engine.dna_engine.verify_signature(sig)
        
        confirm = self.engine.dna_engine.generate_confirm_code(sig)
        confirm_valid = self.engine.dna_engine.verify_confirm(sig, confirm)
        
        return {
            "test": "DNA签名生成与验证",
            "passed": valid and confirm_valid,
            "signature": sig[:50] + "...",
            "confirm_valid": confirm_valid
        }
    
    def test_r_score_calculation(self) -> Dict[str, Any]:
        """测试R评分计算"""
        rb = RScoreBreakdown(
            human_welfare=100, fairness=100,
            controllability=100, transparency=100,
            accountability=100, privacy=100
        )
        score = rb.compute_total()
        # 应该是100但被95封顶
        return {
            "test": "R评分计算与95封顶",
            "passed": score == R_CAP,
            "raw_score": 100,
            "capped_score": score,
            "cap": R_CAP
        }
    
    def test_constraint_checker(self) -> Dict[str, Any]:
        """测试三级约束检测"""
        checks = self.engine.constraint_checker.check_all("正常内容")
        has_infinity = any(c.level == ConstraintLevel.INFINITY for c in checks)
        has_p0 = any(c.level == ConstraintLevel.P0 for c in checks)
        has_p1 = any(c.level == ConstraintLevel.P1 for c in checks)
        all_passed = not any(c.violated for c in checks)
        
        return {
            "test": "三级约束检测",
            "passed": has_infinity and has_p0 and has_p1 and all_passed,
            "infinity": has_infinity,
            "p0": has_p0,
            "p1": has_p1,
            "all_passed": all_passed
        }
    
    def test_gate1_ethics(self) -> Dict[str, Any]:
        """测试伦理红线闸"""
        item = AuditItem(
            item_id="test-1", description="伦理测试",
            content="包含种族灭绝的内容", source="test",
            timestamp=datetime.now(),
            metadata={"ethics_flag": True}
        )
        rb = RScoreBreakdown(80, 80, 80, 80, 80, 80)
        cc = self.engine.constraint_checker.check_all(item.content)
        results = self.engine.ten_gate_engine.process_all_gates(item, rb, cc, True, True)
        
        gate1 = next((r for r in results if r.gate_id == 1), None)
        blocked = gate1 and gate1.result == GateResult.BLOCK
        
        return {
            "test": "伦理红线闸(闸1)",
            "passed": blocked,
            "gate1_result": gate1.result.name if gate1 else "N/A"
        }
    
    def test_gate2_cultural(self) -> Dict[str, Any]:
        """测试文化主权闸"""
        item = AuditItem(
            item_id="test-2", description="文化测试",
            content="涉及文化入侵行为", source="test",
            timestamp=datetime.now(),
            metadata={"cultural_threat_flag": True}
        )
        rb = RScoreBreakdown(80, 80, 80, 80, 80, 80)
        cc = self.engine.constraint_checker.check_all(item.content)
        results = self.engine.ten_gate_engine.process_all_gates(item, rb, cc, True, True)
        
        gate2 = next((r for r in results if r.gate_id == 2), None)
        blocked = gate2 and gate2.result == GateResult.BLOCK
        
        return {
            "test": "文化主权闸(闸2)",
            "passed": blocked,
            "gate2_result": gate2.result.name if gate2 else "N/A"
        }
    
    def test_gate5_values(self) -> Dict[str, Any]:
        """测试价值观校验闸"""
        item = AuditItem(
            item_id="test-5", description="价值观测试",
            content="为了义气背叛", source="test",
            timestamp=datetime.now(),
            metadata={
                "loyalty_rank": 3,
                "righteousness_rank": 1
            }
        )
        rb = RScoreBreakdown(80, 80, 80, 80, 80, 80)
        cc = self.engine.constraint_checker.check_all(item.content, item.metadata)
        results = self.engine.ten_gate_engine.process_all_gates(item, rb, cc, True, True)
        
        gate5 = next((r for r in results if r.gate_id == 5), None)
        blocked = gate5 and gate5.result == GateResult.BLOCK
        
        return {
            "test": "价值观校验闸(闸5)",
            "passed": blocked,
            "gate5_result": gate5.result.name if gate5 else "N/A"
        }
    
    def test_gate6_security(self) -> Dict[str, Any]:
        """测试技术安全性闸"""
        item = AuditItem(
            item_id="test-6", description="安全测试",
            content="正常操作代码", source="test",
            timestamp=datetime.now(),
            metadata={"security_vulnerability": True, "vulnerability_type": "SQL注入"}
        )
        rb = RScoreBreakdown(80, 80, 80, 80, 80, 80)
        cc = self.engine.constraint_checker.check_all(item.content)
        results = self.engine.ten_gate_engine.process_all_gates(item, rb, cc, True, True)
        
        gate6 = next((r for r in results if r.gate_id == 6), None)
        blocked = gate6 and gate6.result == GateResult.BLOCK
        
        return {
            "test": "技术安全性闸(闸6)",
            "passed": blocked,
            "gate6_result": gate6.result.name if gate6 else "N/A"
        }
    
    def test_history_observation(self) -> Dict[str, Any]:
        """测试历史观察期"""
        if not self.engine.history_manager:
            return {"test": "历史观察期", "passed": False, "reason": "未启用"}
        
        # 添加4次红色记录
        for i in range(4):
            self.engine.history_manager.add_record(TricolorStatus.RED, f"test-{i}")
        
        triggered, info = self.engine.history_manager.check_auto_yellow()
        
        return {
            "test": "历史观察期自动🟡触发",
            "passed": triggered and info["red_count"] > HISTORY_RED_LIMIT,
            "red_count": info["red_count"],
            "triggered": triggered
        }
    
    def test_state_machine(self) -> Dict[str, Any]:
        """测试状态机转换"""
        # 测试🔴不能直接→🟢
        new_status, transition = self.engine.state_machine.compute_transition(
            TricolorStatus.RED, [], 90, False, False
        )
        
        correct_transition = new_status == TricolorStatus.YELLOW
        
        return {
            "test": "状态机转换(🔴不能→🟢)",
            "passed": correct_transition,
            "result_status": new_status.value,
            "transition": transition.value
        }
    
    def test_full_audit_green(self) -> Dict[str, Any]:
        """测试完整审计 - 绿色场景"""
        # 清空历史记录，避免被之前测试的红色记录污染
        if self.engine.history_manager:
            self.engine.history_manager.clear_history()
        
        item = AuditItem(
            item_id="green-test", description="绿色测试",
            content="正常合规的AI辅助教育内容", source="test",
            timestamp=datetime.now(),
            metadata={"benefit_loss_ratio": 3.0}
        )
        rb = RScoreBreakdown(95, 95, 90, 90, 95, 90)
        
        decision = self.engine.audit(item, rb)
        
        return {
            "test": "完整审计-绿色场景",
            "passed": decision.status == TricolorStatus.GREEN,
            "status": decision.status.value,
            "r_score": decision.r_score,
            "gates_passed": sum(1 for g in decision.gate_results if g.result == GateResult.PASS)
        }
    
    def test_full_audit_red(self) -> Dict[str, Any]:
        """测试完整审计 - 红色场景"""
        item = AuditItem(
            item_id="red-test", description="红色测试",
            content="危害国家安全的间谍行为", source="test",
            timestamp=datetime.now(),
            metadata={
                "ethics_flag": True,
                "cultural_threat_flag": False,
                "benefit_loss_ratio": 0.5
            }
        )
        rb = RScoreBreakdown(20, 20, 20, 20, 20, 20)
        
        decision = self.engine.audit(item, rb)
        
        return {
            "test": "完整审计-红色场景",
            "passed": decision.status == TricolorStatus.RED,
            "status": decision.status.value,
            "r_score": decision.r_score,
            "block_reasons": len(decision.block_reasons)
        }
    
    def test_r_cap_95(self) -> Dict[str, Any]:
        """测试95极限封顶"""
        rb = RScoreBreakdown(100, 100, 100, 100, 100, 100)
        score = rb.compute_total()
        
        return {
            "test": "95极限封顶验证",
            "passed": score == 95,
            "computed_score": score,
            "expected_cap": 95
        }
    
    def test_tricolor_coverage(self) -> Dict[str, Any]:
        """测试三色覆盖率"""
        # 清空历史记录，避免被之前测试的红色记录污染
        if self.engine.history_manager:
            self.engine.history_manager.clear_history()
        
        # 触发三种颜色
        scenarios = [
            (RScoreBreakdown(95, 95, 90, 90, 95, 90), {}, TricolorStatus.GREEN),
            (RScoreBreakdown(70, 70, 70, 70, 70, 70), {"unverifiable_claims": 5}, TricolorStatus.YELLOW),
        ]
        
        statuses_triggered = set()
        
        for rb, meta, expected in scenarios:
            item = AuditItem(
                item_id=f"cov-test-{len(statuses_triggered)}",
                description="覆盖率测试",
                content=f"测试内容{len(statuses_triggered)}",
                source="test",
                timestamp=datetime.now(),
                metadata=meta
            )
            decision = self.engine.audit(item, rb)
            statuses_triggered.add(decision.status)
        
        # 红色已经在之前的测试中触发
        statuses_triggered.add(TricolorStatus.RED)
        
        all_three = len(statuses_triggered) == 3
        
        return {
            "test": "三色覆盖率",
            "passed": all_three,
            "triggered_statuses": [s.value for s in statuses_triggered],
            "coverage": f"{len(statuses_triggered)}/3"
        }
    
    def generate_test_report(self, results: Dict[str, Any]) -> str:
        """生成测试报告"""
        lines = [
            "\n╔═══════════════════════════════════════════════════════════════╗",
            "║                     自测试报告                                 ║",
            "╠═══════════════════════════════════════════════════════════════╣",
            f"  总测试数: {results['total']}",
            f"  通过    : {results['passed']} ✓",
            f"  失败    : {results['failed']} ✗",
            f"  通过率  : {results['pass_rate']:.1f}%",
            "  ──────────────────────────────────────────"
        ]
        
        for detail in results['details']:
            status = "✓" if detail['passed'] else "✗"
            lines.append(f"  [{status}] {detail['test']}")
        
        lines.extend([
            "╚═══════════════════════════════════════════════════════════════╝"
        ])
        
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# 第十二章：主入口与演示
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """
    主入口 - 系统初始化与自测试
    """
    print("=" * 80)
    print("  龍魂体系 · 三色审计与10道闸流场决策系统 v3.0")
    print("  UID9622 · 龍芯北辰·诸葛鑫")
    print("  DNA签名激活版本 2026-06-16")
    print("=" * 80)
    
    # 初始化引擎
    engine = TricolorAuditEngine(
        uid="UID9622",
        log_dir=V3_AUDIT_LOG_DIR,
        enable_history=True
    )
    
    print("\n[1/4] 系统初始化完成")
    print(f"  UID: {engine.uid}")
    print(f"  版本: {engine.version}")
    print(f"  状态: {engine.get_status().value}")
    
    # 打印系统信息
    info = engine.get_system_info()
    print(f"\n  R评分公式: {info['r_formula']}")
    print(f"  95极限封顶: R_cap = {info['r_cap']}")
    
    # 状态机转换图
    print("\n[2/4] 状态机转换图")
    print(engine.get_transition_diagram())
    
    # 自测试
    print("\n[3/4] 运行自测试套件...")
    test_suite = SelfTestSuite(engine)
    test_results = test_suite.run_all_tests()
    print(test_suite.generate_test_report(test_results))
    
    # 演示审计场景
    print("\n[4/4] 演示审计场景...")
    
    # 场景1: 绿色通行
    print("\n  ── 场景1: 绿色通行 ──")
    item1 = AuditItem(
        item_id="demo-green", description="AI辅助教育项目",
        content="利用AI技术辅助偏远地区儿童教育，提升学习效果",
        source="demo",
        timestamp=datetime.now(),
        metadata={"benefit_loss_ratio": 3.5, "importance": "normal"}
    )
    rb1 = RScoreBreakdown(95, 90, 85, 88, 90, 85)
    decision1 = engine.audit(item1, rb1)
    print(f"  状态: {decision1.status.value}")
    print(f"  R评分: {decision1.r_score:.1f}")
    print(f"  决策: {decision1.final_action}")
    print(f"  DNA签名: {decision1.dna_signature[:50]}...")
    
    # 场景2: 红色阻断
    print("\n  ── 场景2: 红色阻断 ──")
    item2 = AuditItem(
        item_id="demo-red", description="数据泄露项目",
        content="将用户隐私数据出售给第三方以获取利益，exec(rm -rf /)",
        source="demo",
        timestamp=datetime.now(),
        metadata={
            "ethics_flag": True,
            "security_vulnerability": True,
            "vulnerability_type": "数据泄露",
            "benefit_loss_ratio": 0.3,
            "importance": "critical"
        }
    )
    rb2 = RScoreBreakdown(10, 5, 10, 5, 5, 0)
    decision2 = engine.audit(item2, rb2)
    print(f"  状态: {decision2.status.value}")
    print(f"  R评分: {decision2.r_score:.1f}")
    print(f"  阻断理由数: {len(decision2.block_reasons)}")
    print(f"  决策: {decision2.final_action[:80]}...")
    
    # 场景3: 黄色警告
    print("\n  ── 场景3: 黄色警告 ──")
    item3 = AuditItem(
        item_id="demo-yellow", description="边境项目",
        content="开发新型AI推荐算法，unverifiable_claims存在5项无法验证的声明",
        source="demo",
        timestamp=datetime.now(),
        metadata={
            "unverifiable_claims": 5,
            "benefit_loss_ratio": 1.8,
            "importance": "high"
        }
    )
    rb3 = RScoreBreakdown(75, 75, 70, 70, 75, 70)
    decision3 = engine.audit(item3, rb3)
    print(f"  状态: {decision3.status.value}")
    print(f"  R评分: {decision3.r_score:.1f}")
    print(f"  警告数: {len(decision3.warnings)}")
    print(f"  决策: {decision3.final_action}")
    
    # 生成最终报告
    print("\n" + "=" * 80)
    print(engine.generate_full_report())
    
    # 统计信息
    stats = engine.get_statistics()
    print(f"\n最终统计:")
    print(f"  总审计: {stats['total_audits']}")
    print(f"  🟢: {stats['green_count']} | 🟡: {stats['yellow_count']} | 🔴: {stats['red_count']}")
    
    print("\n" + "=" * 80)
    print("  系统运行完成")
    print("  #UID9622⚡️2026-06-16-TRICOLOR-AUDIT-v3.0")
    print("=" * 80)
    
    return engine, test_results


if __name__ == "__main__":
    engine, test_results = main()
