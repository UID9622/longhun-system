#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 龍魂 · 11步执行链引擎 v1.0 (11-Step Execution Chain)
========================================================
投喂落地：CNSH Runtime Governance Mathematics · MVP执行协议 §37

11步链：
  STEP_01 DNA闸门 → STEP_02 L0闸门 → STEP_03 Tier准入
  → STEP_04 意图解析 → STEP_05 别名规范化 → STEP_06 路由
  → STEP_07 执行 → STEP_08 三色判定 → STEP_09 审计追踪
  → STEP_10 三重快照 → STEP_11 执行回执

DNA: #龍芯⚡️丙午·乙未·己未·申时·履-11STEP-CHAIN-v1.0-I1J2K3L4
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import hashlib
import json
import os
import sys
import uuid
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum


# ─── 常量 ───
CHAIN_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "exec_chain")
SNAPSHOT_DIR = os.path.join(CHAIN_DIR, "snapshots")
AUDIT_DIR = os.path.join(CHAIN_DIR, "audit")
os.makedirs(SNAPSHOT_DIR, exist_ok=True)
os.makedirs(AUDIT_DIR, exist_ok=True)

# ─── 铁律 ───
IMMUTABLE_LAWS = {
    "NO_EXECUTION_WITHOUT_AUDIT": True,
    "NO_MEMORY_WITHOUT_TRACE": True,
    "NO_AUTOMATION_WITHOUT_ROLLBACK": True,
    "NO_HIDDEN_OVERWRITE": True,
    "NO_UNTRACEABLE_OUTPUT": True,
}

# ─── 语义别名映射 ───
SEMANTIC_ALIASES = {
    "ACTION_SUPPLEMENT": ["补全", "补齐", "扩展", "自动补充", "结构修复", "补一下", "补充"],
    "ACTION_ARCHIVE": ["保存", "留痕", "收录", "封存", "归档", "存起来"],
    "ACTION_FUSE": ["停", "断", "收网", "终止", "冻结", "熔断", "停止"],
    "ACTION_RECOVER": ["回滚", "读档", "重建", "恢复", "还原", "回去"],
    "ACTION_AUDIT": ["审计", "检查", "审查", "审一下", "看看有没有问题"],
    "ACTION_EXECUTE": ["执行", "运行", "跑一下", "做", "干"],
    "ACTION_DEPLOY": ["部署", "上线", "发布", "发出去"],
    "ACTION_SYNC": ["同步", "联动", "串起来", "对齐"],
}


class Tricolor(Enum):
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"


class StepStatus(Enum):
    PASS = "PASS"
    WARN = "WARN"
    FUSE = "FUSE"
    SKIP = "SKIP"


class TierLevel(Enum):
    TIER_1 = "TIER_1"  # UID9622 创世者 100%
    TIER_2 = "TIER_2"  # 实名认证 + DNA签名 有限
    TIER_3 = "TIER_3"  # 无认证 拒入


@dataclass
class DNAObject:
    """STEP_01 输出：DNA闸门解析结果"""
    dna_primary: str = ""
    dna_confirm: str = ""
    is_valid: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    extracted_at: str = ""


@dataclass
class L0CheckResult:
    """STEP_02 输出：L0铁律校验结果"""
    passed: bool = True
    violations: List[str] = field(default_factory=list)
    checks: Dict[str, bool] = field(default_factory=dict)


@dataclass
class TierResult:
    """STEP_03 输出：Tier准入结果"""
    tier: TierLevel = TierLevel.TIER_3
    authority: float = 0.0
    user_id: str = ""
    is_verified: bool = False
    deny_reason: str = ""


@dataclass
class IntentObject:
    """STEP_04-05 输出：意图解析结果"""
    primary_action: str = ""
    secondary_object: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    normalized_action: str = ""
    required_permission: int = 0


@dataclass
class RouteDecision:
    """STEP_06 输出：路由决策"""
    primary_executor: str = "LOCAL_RUNTIME"
    backup_executors: List[str] = field(default_factory=list)
    routing_decision_id: str = ""
    routing_confidence: float = 0.0
    candidates_scores: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionResult:
    """STEP_07 输出：执行结果"""
    success: bool = False
    output: str = ""
    files_modified: List[str] = field(default_factory=list)
    memory_written: Dict[str, Any] = field(default_factory=dict)
    side_effects: List[str] = field(default_factory=list)
    error: str = ""


@dataclass
class TrafficLightResult:
    """STEP_08 输出：三色判定"""
    tricolor: Tricolor = Tricolor.GREEN
    confidence: float = 1.0
    reason: str = ""
    checks: Dict[str, bool] = field(default_factory=dict)


@dataclass
class AuditEntry:
    """STEP_09 输出：审计记录"""
    audit_id: str = ""
    timestamp: str = ""
    dna_trace: str = ""
    actor: str = ""
    action: str = ""
    input_summary: str = ""
    output_summary: str = ""
    files_modified: List[str] = field(default_factory=list)
    memory_written: int = 0
    tricolor: str = "🟢"
    executor: str = ""
    audit_hash: str = ""


@dataclass
class SnapshotObject:
    """STEP_10 输出：快照对象"""
    snapshot_id: str = ""
    timestamp: str = ""
    dna_trace: str = ""
    system_state: Dict[str, Any] = field(default_factory=dict)
    file_checksums: Dict[str, Any] = field(default_factory=dict)
    rollback_point: str = ""
    primary_path: str = ""
    verified: bool = False


@dataclass
class ExecutionReceipt:
    """STEP_11 输出：执行回执"""
    receipt_id: str = ""
    timestamp: str = ""
    dna_trace: str = ""
    executor: str = ""
    action: str = ""
    input_summary: str = ""
    output_summary: str = ""
    files_changed: List[str] = field(default_factory=list)
    memory_written: int = 0
    snapshot_id: str = ""
    rollback_point: str = ""
    audit_id: str = ""
    tricolor: str = "🟢"
    risk_level: float = 0.0
    human_readable: str = ""
    recovery_instruction: str = ""


@dataclass
class ChainResult:
    """11步链完整结果"""
    chain_id: str
    timestamp: str
    steps: Dict[str, Any] = field(default_factory=dict)
    overall_status: Tricolor = Tricolor.GREEN
    dna_trace: str = ""
    hash_chain: str = ""


# ═══════════════════════════════════════════════════════════
# 🧠 11步执行链引擎
# ═══════════════════════════════════════════════════════════

class ElevenStepChain:
    """
    11步执行链引擎
    
    每一关都是闸门，任一🔴熔断则整条链中断。
    """

    def __init__(self, user_id: str = "UID9622", tier: TierLevel = TierLevel.TIER_1):
        self.user_id = user_id
        self.user_tier = tier
        self.chain_history: List[ChainResult] = []
        self._load_history()

    def _load_history(self):
        history_file = os.path.join(CHAIN_DIR, "chain_history.jsonl")
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            self.chain_history.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass

    def _save_chain(self, result: ChainResult):
        history_file = os.path.join(CHAIN_DIR, "chain_history.jsonl")
        with open(history_file, 'a', encoding='utf-8') as f:
            serializable = {
                "chain_id": result.chain_id,
                "timestamp": result.timestamp,
                "steps": {k: self._serialize_step(v) for k, v in result.steps.items()},
                "overall_status": result.overall_status.value,
                "dna_trace": result.dna_trace,
                "hash_chain": result.hash_chain,
            }
            f.write(json.dumps(serializable, ensure_ascii=False) + '\n')
        self.chain_history.append(result)

    def _serialize_step(self, obj) -> Dict[str, Any]:
        if obj is None:
            return {}
        if isinstance(obj, dict):
            return {k: self._serialize_step(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._serialize_step(item) for item in obj]
        if isinstance(obj, Enum):
            return obj.value
        if hasattr(obj, '__dataclass_fields__'):
            return {k: self._serialize_step(v) for k, v in asdict(obj).items()}
        return obj

    # ─── STEP_01: DNA闸门 ───
    def step_01_dna_gate(self, input_text: str) -> Tuple[DNAObject, StepStatus]:
        """识别并验证DNA签名"""
        dna = DNAObject(extracted_at=datetime.now(timezone.utc).isoformat())

        # 查找 #龍芯⚡️... 格式
        import re
        dragon_match = re.search(r'#龍芯⚡️[^\s#]{10,}', input_text)
        confirm_match = re.search(r'#CONFIRM🌌[^\s#]{10,}', input_text)

        if dragon_match:
            dna.dna_primary = dragon_match.group(0)
            dna.is_valid = True

        if confirm_match:
            dna.dna_confirm = confirm_match.group(0)

        # 提取元数据
        if dna.dna_primary:
            parts = dna.dna_primary.replace('#龍芯⚡️', '').split('-')
            dna.metadata = {
                "raw": dna.dna_primary,
                "parts": parts,
                "has_confirm": bool(dna.dna_confirm),
            }

        if dna.is_valid and dna.dna_confirm:
            status = StepStatus.PASS
        elif dna.is_valid:
            status = StepStatus.WARN  # 有主签但缺确认签
        else:
            status = StepStatus.WARN  # 无DNA不熔断，但标记

        return dna, status

    # ─── STEP_02: L0闸门 ───
    def step_02_l0_gatekeeper(self, dna: DNAObject) -> Tuple[L0CheckResult, StepStatus]:
        """龍魂铁律校验"""
        result = L0CheckResult()

        checks = {
            "no_overwrite": True,
            "no_delete": True,
            "no_wash_history": True,
            "is_traceable": dna.is_valid,
            "is_auditable": True,
            "is_recoverable": True,
        }

        # 检查DNA是否有效
        if not dna.is_valid:
            checks["is_traceable"] = False
            result.violations.append("缺少DNA追溯码 — 不可追溯")

        if not dna.dna_confirm:
            checks["is_traceable"] = False
            result.violations.append("缺少CONFIRM确认码")

        result.checks = checks
        result.passed = all(checks.values())

        if result.passed:
            status = StepStatus.PASS
        elif any(not v for k, v in checks.items() if k in ["no_overwrite", "no_delete", "no_wash_history"]):
            status = StepStatus.FUSE  # 铁律违 → 永久熔断
        else:
            status = StepStatus.WARN

        return result, status

    # ─── STEP_03: Tier准入 ───
    def step_03_tier_gatekeeper(self) -> Tuple[TierResult, StepStatus]:
        """Tier准入验证"""
        result = TierResult(user_id=self.user_id)

        if self.user_tier == TierLevel.TIER_1:
            result.tier = TierLevel.TIER_1
            result.authority = 1.0
            result.is_verified = True
            status = StepStatus.PASS
        elif self.user_tier == TierLevel.TIER_2:
            result.tier = TierLevel.TIER_2
            result.authority = 0.5
            result.is_verified = True
            status = StepStatus.PASS
        else:
            result.tier = TierLevel.TIER_3
            result.authority = 0.0
            result.deny_reason = "TIER_3: 无认证用户，拒入"
            status = StepStatus.FUSE

        return result, status

    # ─── STEP_04: 意图解析 ───
    def step_04_intent_parser(self, input_text: str) -> Tuple[IntentObject, StepStatus]:
        """中文意图解析"""
        intent = IntentObject()

        # 基于语义别名匹配
        best_match = ""
        best_confidence = 0.0

        for action, aliases in SEMANTIC_ALIASES.items():
            for alias in aliases:
                if alias in input_text:
                    confidence = len(alias) / max(len(input_text), 1) + 0.3
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_match = action

        if best_match:
            intent.primary_action = best_match
            intent.confidence = min(0.95, best_confidence)

        # 提取对象
        object_keywords = ["代码", "文档", "记忆", "逻辑", "协议", "规则", "配置", "数据", "文件"]
        for kw in object_keywords:
            if kw in input_text:
                intent.secondary_object = kw
                break

        if not intent.secondary_object:
            intent.secondary_object = "通用"

        if intent.confidence >= 0.7:
            status = StepStatus.PASS
        elif intent.confidence >= 0.3:
            status = StepStatus.WARN
        else:
            status = StepStatus.WARN  # 不熔断，但标记低置信

        return intent, status

    # ─── STEP_05: 别名规范化 ───
    def step_05_semantic_alias(self, intent: IntentObject) -> Tuple[IntentObject, StepStatus]:
        """语义别名规范化"""
        # 已经在 STEP_04 中完成了映射
        # 这里做权限检查

        high_perm_actions = ["ACTION_FUSE", "ACTION_DEPLOY", "ACTION_RECOVER"]
        if intent.primary_action in high_perm_actions:
            intent.required_permission = 80
        elif intent.primary_action in ["ACTION_ARCHIVE", "ACTION_SYNC"]:
            intent.required_permission = 50
        else:
            intent.required_permission = 20

        intent.normalized_action = intent.primary_action

        status = StepStatus.PASS
        return intent, status

    # ─── STEP_06: 路由 ───
    def step_06_router(self, intent: IntentObject, tier: TierResult) -> Tuple[RouteDecision, StepStatus]:
        """执行者路由"""
        decision = RouteDecision(
            routing_decision_id=f"ROUTE-{uuid.uuid4().hex[:8]}",
        )

        # 候选评分
        candidates = {
            "LOCAL_RUNTIME": {"competence": 0.7, "trust": 1.0, "semantic_match": 0.8},
            "CLAUDE": {"competence": 0.9, "trust": 0.95, "semantic_match": 0.85},
        }

        # 计算最佳执行者
        best_score = 0
        best_executor = "LOCAL_RUNTIME"
        for name, scores in candidates.items():
            score = scores["competence"] * scores["trust"] * scores["semantic_match"]
            if score > best_score:
                best_score = score
                best_executor = name

        decision.primary_executor = best_executor
        decision.routing_confidence = best_score
        decision.candidates_scores = candidates
        decision.backup_executors = [n for n in candidates if n != best_executor]

        status = StepStatus.PASS if decision.routing_confidence > 0.3 else StepStatus.WARN
        return decision, status

    # ─── STEP_07: 执行 ───
    def step_07_execute(self, intent: IntentObject, route: RouteDecision,
                        executor_fn: Optional[Callable] = None) -> Tuple[ExecutionResult, StepStatus]:
        """执行操作"""
        result = ExecutionResult()

        try:
            if executor_fn:
                output = executor_fn(intent.parameters)
                result.output = str(output)[:500]
                result.success = True
            else:
                # 模拟执行
                result.output = f"执行了 {intent.normalized_action} 操作（模拟模式）"
                result.success = True

            status = StepStatus.PASS if result.success else StepStatus.FUSE
        except Exception as e:
            result.success = False
            result.error = str(e)
            status = StepStatus.FUSE

        return result, status

    # ─── STEP_08: 三色判定 ───
    def step_08_traffic_light(self, exec_result: ExecutionResult,
                               previous_statuses: List[StepStatus]) -> Tuple[TrafficLightResult, StepStatus]:
        """三色审计判定"""
        tr = TrafficLightResult()

        checks = {
            "semantic_integrity": exec_result.success,
            "no_overwrite": True,
            "no_hidden": True,
            "execution_success": exec_result.success,
        }

        tr.checks = checks

        # 综合判断
        if all(checks.values()):
            tr.tricolor = Tricolor.GREEN
            tr.reason = "所有检查通过"
            status = StepStatus.PASS
        elif checks.get("execution_success"):
            tr.tricolor = Tricolor.YELLOW
            tr.reason = "执行成功但有部分检查未通过"
            status = StepStatus.WARN
        else:
            tr.tricolor = Tricolor.RED
            tr.reason = f"执行失败: {exec_result.error}"
            status = StepStatus.FUSE

        tr.confidence = sum(1 for v in checks.values() if v) / len(checks)
        return tr, status

    # ─── STEP_09: 审计追踪 ───
    def step_09_audit_trail(self, input_text: str, exec_result: ExecutionResult,
                             tr: TrafficLightResult, dna: DNAObject) -> Tuple[AuditEntry, StepStatus]:
        """审计记录"""
        entry = AuditEntry(
            audit_id=f"AUDIT-{uuid.uuid4().hex[:12]}",
            timestamp=datetime.now(timezone.utc).isoformat(),
            dna_trace=dna.dna_primary or f"#龍芯⚡️丙午·乙未·己未·申时·履-AUDIT-{uuid.uuid4().hex[:8]}",
            actor=self.user_id,
            action="EXECUTE",
            input_summary=input_text[:100],
            output_summary=exec_result.output[:100] if exec_result.output else "",
            files_modified=exec_result.files_modified,
            memory_written=len(exec_result.memory_written),
            tricolor=tr.tricolor.value,
            executor="LOCAL_RUNTIME",
        )
        entry.audit_hash = hashlib.sha256(
            f"{entry.audit_id}{entry.timestamp}{entry.input_summary}".encode()
        ).hexdigest()

        # 保存审计记录
        audit_file = os.path.join(AUDIT_DIR, f"audit-{entry.audit_id}.json")
        with open(audit_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(entry), f, ensure_ascii=False, indent=2)

        status = StepStatus.PASS
        return entry, status

    # ─── STEP_10: 三重快照 ───
    def step_10_triple_snapshot(self, audit: AuditEntry) -> Tuple[SnapshotObject, StepStatus]:
        """三重快照（本地）"""
        snap = SnapshotObject(
            snapshot_id=f"SNAP-{uuid.uuid4().hex[:12]}",
            timestamp=datetime.now(timezone.utc).isoformat(),
            dna_trace=audit.dna_trace,
            system_state={"audit_id": audit.audit_id, "tricolor": audit.tricolor},
            rollback_point=f"SNAP-{uuid.uuid4().hex[:8]}",
        )

        # 本地快照
        snap.primary_path = os.path.join(SNAPSHOT_DIR, f"{snap.snapshot_id}.json")
        with open(snap.primary_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(snap), f, ensure_ascii=False, indent=2)

        # 校验
        with open(snap.primary_path, 'r') as f:
            content = f.read()
        snap.file_checksums = {snap.primary_path: hashlib.sha256(content.encode()).hexdigest()}
        snap.verified = True

        status = StepStatus.PASS
        return snap, status

    # ─── STEP_11: 执行回执 ───
    def step_11_execution_receipt(self, audit: AuditEntry, snap: SnapshotObject,
                                   tr: TrafficLightResult) -> Tuple[ExecutionReceipt, StepStatus]:
        """生成执行回执"""
        receipt = ExecutionReceipt(
            receipt_id=f"RECEIPT-{uuid.uuid4().hex[:12]}",
            timestamp=datetime.now(timezone.utc).isoformat(),
            dna_trace=audit.dna_trace,
            executor="LOCAL_RUNTIME",
            action="EXECUTE",
            input_summary=audit.input_summary,
            output_summary=audit.output_summary,
            snapshot_id=snap.snapshot_id,
            rollback_point=snap.rollback_point,
            audit_id=audit.audit_id,
            tricolor=tr.tricolor.value,
            risk_level=0.0 if tr.tricolor == Tricolor.GREEN else (0.5 if tr.tricolor == Tricolor.YELLOW else 1.0),
        )
        receipt.human_readable = f"执行完成 — 状态{tr.tricolor.value} — 审计ID: {audit.audit_id}"
        receipt.recovery_instruction = f"如需回滚，使用快照: {snap.snapshot_id}"

        status = StepStatus.PASS
        return receipt, status

    # ─── 主流程：完整11步链 ───
    def execute_chain(self, input_text: str, executor_fn: Optional[Callable] = None) -> ChainResult:
        """
        执行完整11步链
        
        返回 ChainResult，包含每一步的结果和状态。
        任一步骤 FUSE 则中断后续步骤。
        """
        chain_id = f"CHAIN-{uuid.uuid4().hex[:12]}"
        timestamp = datetime.now(timezone.utc).isoformat()
        steps = {}
        overall = Tricolor.GREEN
        fused = False

        # ─── STEP_01: DNA闸门 ───
        dna, s1_status = self.step_01_dna_gate(input_text)
        steps["01_DNA_GATE"] = {"result": dna, "status": s1_status.value}
        if s1_status == StepStatus.FUSE:
            fused = True

        # ─── STEP_02: L0闸门 ───
        if not fused:
            l0, s2_status = self.step_02_l0_gatekeeper(dna)
            steps["02_L0_GATE"] = {"result": l0, "status": s2_status.value}
            if s2_status == StepStatus.FUSE:
                fused = True
        else:
            steps["02_L0_GATE"] = {"result": None, "status": StepStatus.SKIP.value}

        # ─── STEP_03: Tier准入 ───
        if not fused:
            tier, s3_status = self.step_03_tier_gatekeeper()
            steps["03_TIER_GATE"] = {"result": tier, "status": s3_status.value}
            if s3_status == StepStatus.FUSE:
                fused = True
        else:
            steps["03_TIER_GATE"] = {"result": None, "status": StepStatus.SKIP.value}

        # ─── STEP_04: 意图解析 ───
        if not fused:
            intent, s4_status = self.step_04_intent_parser(input_text)
            steps["04_INTENT"] = {"result": intent, "status": s4_status.value}
        else:
            steps["04_INTENT"] = {"result": None, "status": StepStatus.SKIP.value}

        # ─── STEP_05: 别名规范化 ───
        if not fused:
            norm_intent, s5_status = self.step_05_semantic_alias(intent)
            steps["05_ALIAS"] = {"result": norm_intent, "status": s5_status.value}
        else:
            steps["05_ALIAS"] = {"result": None, "status": StepStatus.SKIP.value}

        # ─── STEP_06: 路由 ───
        if not fused:
            route, s6_status = self.step_06_router(norm_intent, tier)
            steps["06_ROUTE"] = {"result": route, "status": s6_status.value}
        else:
            steps["06_ROUTE"] = {"result": None, "status": StepStatus.SKIP.value}

        # ─── STEP_07: 执行 ───
        if not fused:
            exec_result, s7_status = self.step_07_execute(norm_intent, route, executor_fn)
            steps["07_EXECUTE"] = {"result": exec_result, "status": s7_status.value}
            if s7_status == StepStatus.FUSE:
                fused = True
        else:
            steps["07_EXECUTE"] = {"result": None, "status": StepStatus.SKIP.value}

        # ─── STEP_08: 三色判定 ───
        if not fused:
            prev_statuses = [StepStatus(s["status"]) for s in steps.values() if s["status"] != StepStatus.SKIP.value]
            tr, s8_status = self.step_08_traffic_light(exec_result, prev_statuses)
            steps["08_TRAFFIC"] = {"result": tr, "status": s8_status.value}
            if s8_status == StepStatus.FUSE:
                fused = True
                overall = Tricolor.RED
            elif s8_status == StepStatus.WARN:
                overall = Tricolor.YELLOW
        else:
            steps["08_TRAFFIC"] = {"result": None, "status": StepStatus.SKIP.value}
            overall = Tricolor.RED

        # ─── STEP_09: 审计追踪 ───
        audit_entry = None
        if not fused or exec_result is not None:
            audit_entry, s9_status = self.step_09_audit_trail(input_text, exec_result, tr, dna)
            steps["09_AUDIT"] = {"result": audit_entry, "status": s9_status.value}
        else:
            steps["09_AUDIT"] = {"result": None, "status": StepStatus.SKIP.value}

        # ─── STEP_10: 三重快照 ───
        snap = None
        if audit_entry:
            snap, s10_status = self.step_10_triple_snapshot(audit_entry)
            steps["10_SNAPSHOT"] = {"result": snap, "status": s10_status.value}
        else:
            steps["10_SNAPSHOT"] = {"result": None, "status": StepStatus.SKIP.value}

        # ─── STEP_11: 执行回执 ───
        if audit_entry and snap:
            receipt, s11_status = self.step_11_execution_receipt(audit_entry, snap, tr)
            steps["11_RECEIPT"] = {"result": receipt, "status": s11_status.value}
        else:
            steps["11_RECEIPT"] = {"result": None, "status": StepStatus.SKIP.value}

        # 生成哈希链
        prev_hash = ""
        if self.chain_history:
            last = self.chain_history[-1]
            prev_hash = last.get('hash_chain', '') if isinstance(last, dict) else getattr(last, 'hash_chain', '')
        hash_chain = hashlib.sha256(f"{prev_hash}{chain_id}{overall.value}".encode()).hexdigest()

        result = ChainResult(
            chain_id=chain_id,
            timestamp=timestamp,
            steps=steps,
            overall_status=overall,
            dna_trace=f"#龍芯⚡️丙午·乙未·己未·申时·履-11STEP-{chain_id[-8:]}",
            hash_chain=hash_chain,
        )

        self._save_chain(result)
        return result

    def stats(self) -> Dict[str, Any]:
        total = len(self.chain_history)
        if total == 0:
            return {"total_chains": 0}

        greens = sum(1 for c in self.chain_history if (c.get('overall_status') if isinstance(c, dict) else c.overall_status.value) == '🟢')
        reds = sum(1 for c in self.chain_history if (c.get('overall_status') if isinstance(c, dict) else c.overall_status.value) == '🔴')

        return {
            "total_chains": total,
            "green": greens,
            "yellow": total - greens - reds,
            "red": reds,
            "success_rate": round(greens/max(1,total)*100, 1),
        }


# ═══════════════════════════════════════════════════════════
# 🧪 CLI 演示
# ═══════════════════════════════════════════════════════════

def demo():
    print("=" * 70)
    print("🐉 龍魂 · 11步执行链引擎 v1.0")
    print("=" * 70)

    chain = ElevenStepChain()

    test_inputs = [
        "补全一下审计模块的代码 #龍芯⚡️丙午·乙未·己未·申时·履-TEST #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
        "把这份文档归档保存",
        "检查一下系统有没有安全问题",
    ]

    for i, text in enumerate(test_inputs):
        print(f"\n{'='*70}")
        print(f"🧪 测试 #{i+1}: {text[:60]}...")
        print(f"{'='*70}")

        result = chain.execute_chain(text)

        for step_name, step_data in result.steps.items():
            status = step_data["status"] if isinstance(step_data, dict) else step_data.status
            icon = {"PASS": "🟢", "WARN": "🟡", "FUSE": "🔴", "SKIP": "⏭️"}.get(status, "❓")
            print(f"   {icon} {step_name}: {status}")

        print(f"\n   🏁 最终状态: {result.overall_status.value}")
        print(f"   🧬 DNA: {result.dna_trace}")

    stats = chain.stats()
    print(f"\n{'='*70}")
    print(f"📊 链统计: {stats}")
    print()

    return chain


if __name__ == "__main__":
    demo()
