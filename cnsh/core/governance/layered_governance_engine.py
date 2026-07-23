#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂分层治理自愈引擎 · LongHun Layered Governance Self-Healing Engine v1.0

把 L0-L7 分层治理、F1-F7 七因子行为密码学、三才主权指数 (SI)、文化主权算法
全部接入自动巡检、自动报警、自动修复、自动启动。

核心铁律：
  - 只冻结 / 停用 / 激活，绝不删除任何用户授权或数据
  - 每次修复必须写出日志、决策路径、DNA 追溯码
  - 修复前先做 F1-F7 验证与 SI 主权检查
  - 任何触及 L0 / P0 的异常立即升级为 🔴 并冻结

治理层 (L0-L7):
  L0 宪法层/永恒层    : UID9622 一票否决、P0 铁律
  L1 基础协议层       : DNA 追溯、三色审计、369 熔断
  L2 治理与人治层     : 君子协议、价值排序 (孝义忠)
  L3 经济与激励层     : 月费激活、功勋系统
  L4 文化与开源层     : 字体生态、通心译、资产主权声明
  L5 技术与分布式层   : 分布式 DNA、认知压缩、常驻服务
  L6 人权与退出层     : 退出权利、错误纠正
  L7 内容主权层       : 来源链、数字永生、AI 时代主权

DNA: #龍芯⚡️2026-06-22-LAYERED-GOVERNANCE-ENGINE-v1.0
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import signal
import socket
import sqlite3
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

# 兼容从项目根目录或本文件直接运行
_ROOT_CANDIDATES = [
    pathlib.Path(__file__).resolve().parents[2],  # cnsh-core/governance/ -> longhun-system
    pathlib.Path.cwd(),
]
ROOT: pathlib.Path = next((p for p in _ROOT_CANDIDATES if (p / "bin" / "longhun-launcher.py").exists()), _ROOT_CANDIDATES[0])

# 把项目根目录与 cnsh-core 加入路径，方便导入 F1-F7 / SI
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "cnsh-core") not in sys.path:
    sys.path.insert(0, str(ROOT / "cnsh-core"))

LOG_DIR = ROOT / "logs"
GOV_DIR = ROOT / "var" / "governance"
FREEZE_REGISTRY = GOV_DIR / "freeze_registry.json"
ALARM_LOG = GOV_DIR / "governance_alarms.jsonl"
HEAL_LOG = GOV_DIR / "governance_heal.jsonl"
STATUS_FILE = GOV_DIR / "governance_status.json"

DNA = "#龍芯⚡️2026-06-22-LAYERED-GOVERNANCE-ENGINE-v1.0"


class Tricolor(str, Enum):
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"


class LayerLevel(str, Enum):
    L0 = "L0"
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    L4 = "L4"
    L5 = "L5"
    L6 = "L6"
    L7 = "L7"


@dataclass
class LayerSpec:
    """治理层规范"""
    id: str
    name: str
    description: str
    owner: str
    critical: bool  # 是否关键层（L0/L1/L7 等）
    files: List[pathlib.Path] = field(default_factory=list)      # 应存在的文件
    file_patterns: List[str] = field(default_factory=list)       # 自动发现模式
    processes: List[str] = field(default_factory=list)           # 应运行的进程/服务 id
    si_dimension: Optional[str] = None                           # 三才维度映射: tian/di/ren
    f1_f7_required: bool = False                                 # 是否需要七因子验证
    rules: List[str] = field(default_factory=list)               # 该层核心规则摘要


@dataclass
class ComponentCheck:
    """单个组件检查结果"""
    layer_id: str
    component_id: str
    component_type: str  # file | process | f1f7 | sovereignty
    status: str  # ok | warning | error | frozen
    tricolor: str
    score: float  # 0.0-1.0
    message: str
    evidence: Dict[str, Any] = field(default_factory=dict)
    auto_fixable: bool = False
    fix_action: Optional[str] = None


@dataclass
class HealRecord:
    """修复记录"""
    dna: str
    timestamp: str
    layer_id: str
    component_id: str
    action: str
    reason: str
    before_status: str
    after_status: str
    decision_path: List[str] = field(default_factory=list)
    side_effects: List[str] = field(default_factory=list)


@dataclass
class AlarmRecord:
    """报警记录"""
    dna: str
    timestamp: str
    level: str  # info / warning / critical
    layer_id: str
    component_id: str
    message: str
    tricolor: str


# ═══════════════════════════════════════════════════════════════════
# 治理层注册表
# ═══════════════════════════════════════════════════════════════════

def _layer_specs() -> List[LayerSpec]:
    return [
        LayerSpec(
            id=LayerLevel.L0,
            name="宪法层/永恒层",
            description="UID9622 一票否决、P0 铁律、人民主权优先",
            owner="UID9622",
            critical=True,
            files=[
                ROOT / "AGENTS.md",
                ROOT / "cnsh-core" / "constitution" / "__init__.py",
                ROOT / "cnsh-core" / "permissions" / "__init__.py",
            ],
            file_patterns=["AGENTS.md", "cnsh-core/constitution/**", "cnsh-core/permissions/**"],
            processes=[],
            si_dimension="ren",
            f1_f7_required=True,
            rules=["P0铁律不可改", "UID9622一票否决", "人民主权优先"],
        ),
        LayerSpec(
            id=LayerLevel.L1,
            name="基础协议层",
            description="DNA 追溯、三色审计、369 熔断、数字根不变量",
            owner="龍芯算法委员会",
            critical=True,
            files=[
                pathlib.Path.home() / "chain_hash.jsonl",
                pathlib.Path.home() / "_work" / "dragon_knowledge.db",
            ],
            file_patterns=["brain/*.db"],
            processes=["longhun-brain"],
            si_dimension="tian",
            f1_f7_required=True,
            rules=["DNA全链路追溯", "三色审计", "369熔断"],
        ),
        LayerSpec(
            id=LayerLevel.L2,
            name="治理与人治层",
            description="君子协议、价值排序、道义制",
            owner="社区治理层",
            critical=False,
            files=[
                ROOT / "cnsh-core" / "governance" / "f1_through_f7_verifier.py",
                ROOT / "cnsh-core" / "governance" / "sovereignty_index.py",
            ],
            file_patterns=["cnsh-core/governance/**", "docs/**/君子协议*"],
            processes=[],
            si_dimension="tian",
            f1_f7_required=False,
            rules=["君子协议", "孝义忠价值排序", "曾仕强老师L∞"],
        ),
        LayerSpec(
            id=LayerLevel.L3,
            name="经济与激励层",
            description="月费激活、功勋系统、收益透明",
            owner="经济模型层",
            critical=False,
            files=[
                ROOT / "xpay" / "README.md",
                ROOT / "xpay" / "LICENSE",
                ROOT / "xpay" / "CONTRIBUTING.md",
                ROOT / "xpay" / "CODE_OF_CONDUCT.md",
                ROOT / "xpay" / "INCENTIVE_MODEL.md",
            ],
            file_patterns=["xpay/**"],
            processes=[],
            si_dimension="di",
            f1_f7_required=False,
            rules=["月费激活", "功勋透明", "收益公式公开"],
        ),
        LayerSpec(
            id=LayerLevel.L4,
            name="文化与开源层",
            description="字体生态、通心译、资产主权声明",
            owner="文化主权委员会",
            critical=True,
            files=[
                ROOT / "longhun-font" / "README.md",
                ROOT / "longhun-font" / "LICENSE",
                ROOT / "longhun-font" / "CONTRIBUTING.md",
                ROOT / "longhun-font" / "CODE_OF_CONDUCT.md",
                ROOT / "longhun-font" / "字体主权执行报告.md",
                ROOT / "cnsh-core" / "language",
            ],
            file_patterns=["longhun-font/**", "cnsh-core/language/**", "docs/**/通心译*"],
            processes=[],
            si_dimension="ren",
            f1_f7_required=False,
            rules=["龍字规范", "通心译五大原则", "资产属于中华人民共和国"],
        ),
        LayerSpec(
            id=LayerLevel.L5,
            name="技术与分布式层",
            description="分布式 DNA、认知压缩、常驻服务、统一知识中枢",
            owner="技术执行层",
            critical=True,
            files=[
                ROOT / "scripts" / "longhun_compression_engine.py",
                ROOT / "scripts" / "kg_unified.py",
                ROOT / "cnsh-core" / "runtime-governance",
            ],
            file_patterns=["scripts/longhun_compression_engine.py", "scripts/kg_unified.py", "cnsh-core/runtime-governance/**"],
            processes=["compression-engine"],
            si_dimension="di",
            f1_f7_required=False,
            rules=["分布式DNA", "认知压缩", "统一知识中枢"],
        ),
        LayerSpec(
            id=LayerLevel.L6,
            name="人权与退出层",
            description="退出权利、数据可携带、错误纠正",
            owner="权利保障层",
            critical=False,
            files=[
                ROOT / "cnsh-core" / "identity",
            ],
            file_patterns=["cnsh-core/identity/**", "sovereignty/**"],
            processes=["identity-portal"],
            si_dimension="ren",
            f1_f7_required=False,
            rules=["完全退出", "数据带走", "错误纠正三层审核"],
        ),
        LayerSpec(
            id=LayerLevel.L7,
            name="内容主权层",
            description="来源链、数字永生、AI 时代主权",
            owner="内容主权委员会",
            critical=True,
            files=[
                ROOT / "docs",
            ],
            file_patterns=["docs/**", "README.md"],
            processes=[],
            si_dimension="ren",
            f1_f7_required=True,
            rules=["来源不可删", "影响不可覆", "贡献不可抹除"],
        ),
    ]


# ═══════════════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════════════

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _dna(prefix: str, seed: str = "") -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")[:-3]
    h = hashlib.sha256(f"{prefix}|{seed}|{ts}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-{prefix}-{h}"


def _ensure_dirs() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    GOV_DIR.mkdir(parents=True, exist_ok=True)


def _is_port_open(port: int) -> bool:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect(("127.0.0.1", port))
        return True
    except Exception:
        return False
    finally:
        s.close()


def _find_pid_by_port(port: int) -> Optional[int]:
    try:
        result = subprocess.run(
            ["lsof", "-ti", f":{port}"],
            capture_output=True, text=True, check=False, timeout=5,
        )
        if result.stdout.strip():
            return int(result.stdout.strip().split("\n")[0])
    except Exception:
        pass
    return None


def _file_has_dna(path: pathlib.Path) -> bool:
    """检查文件是否包含 DNA 追溯码（支持注释和 JSON 字段）"""
    dna_re = re.compile(r"#龍芯⚡️[^\s\"']+")
    try:
        # JSON 配置文件 DNA 字段可能在尾部，读取更多字节
        max_bytes = 262144 if path.suffix.lower() in (".json", ".jsonl") else 8192
        text = path.read_text(encoding="utf-8", errors="ignore")[:max_bytes]
        if dna_re.search(text):
            return True
        # JSON 文件可能把 DNA 放在 dna / _dna 字段
        if path.suffix.lower() in (".json", ".jsonl"):
            # 先在整个文本片段里搜索龍芯 DNA 字段（避免大文件解析失败）
            if re.search(r'"(_dna|dna)"\s*:\s*"#龍芯⚡️[^"]+"', text):
                return True
            # 对于配置文件，只要有 _dna/dna 字段即视为有身份标记
            try:
                data = json.loads(text)
                if isinstance(data, dict) and ("_dna" in data or "dna" in data):
                    return True
            except Exception:
                pass
        return False
    except Exception:
        return False


def _load_json(path: pathlib.Path) -> Dict[str, Any]:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_json(path: pathlib.Path, data: Dict[str, Any]) -> None:
    _ensure_dirs()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _append_jsonl(path: pathlib.Path, record: Dict[str, Any]) -> None:
    _ensure_dirs()
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")


# ═══════════════════════════════════════════════════════════════════
# 文化主权算法：数字根 → 三色
# ═══════════════════════════════════════════════════════════════════

def digital_root(n: int) -> int:
    """数字根 dr(n) = 1 + ((n-1) mod 9)，n>0"""
    if n <= 0:
        return 0
    return 1 + ((n - 1) % 9)


def tricolor_from_dr(dr: int) -> str:
    """369 三色审计：{3,9}->🔴, {6}->🟡, 其余->🟢"""
    if dr in (3, 9):
        return Tricolor.RED
    if dr == 6:
        return Tricolor.YELLOW
    return Tricolor.GREEN


def tricolor_from_score(score: float) -> str:
    """0.0-1.0 映射到三色"""
    if score >= 0.85:
        return Tricolor.GREEN
    if score >= 0.50:
        return Tricolor.YELLOW
    return Tricolor.RED


def cultural_sovereignty_score(text: str) -> Tuple[float, str]:
    """
    文化主权算法：检查文本中关键主权词汇的保留情况。
    采用分级评分，避免普通代码文件因缺少全部主权词而被过度扣分。
    返回 (score, detail)。
    """
    sovereign_terms = ["龍", "龍魂", "龍芯", "UID9622", "通心译", "曾仕强老师"]
    core_terms = ["龍", "龍魂", "龍芯"]  # 核心标识，至少保留一个即视为文化归属明确
    if not text:
        return 0.0, "空文本"
    found = [t for t in sovereign_terms if t in text]
    n = len(found)
    if n == 6:
        score = 1.0
    elif n >= 4:
        score = 0.95
    elif n >= 2:
        score = 0.90
    elif any(t in text for t in core_terms):
        score = 0.85
    else:
        score = 0.50
    detail = f"保留 {n}/{len(sovereign_terms)} 个主权词: {found}"
    return score, detail


# ═══════════════════════════════════════════════════════════════════
# 冻结注册表
# ═══════════════════════════════════════════════════════════════════

def load_freeze_registry() -> Dict[str, Any]:
    return _load_json(FREEZE_REGISTRY)


def save_freeze_registry(registry: Dict[str, Any]) -> None:
    _save_json(FREEZE_REGISTRY, registry)


def is_frozen(component_id: str) -> bool:
    reg = load_freeze_registry()
    return reg.get(component_id, {}).get("frozen", False)


def freeze_component(component_id: str, reason: str, layer_id: str, dna: str) -> None:
    """冻结组件：只标记，不删除任何文件或数据"""
    reg = load_freeze_registry()
    reg[component_id] = {
        "frozen": True,
        "reason": reason,
        "layer_id": layer_id,
        "frozen_at": _now(),
        "frozen_by": "layered_governance_engine",
        "dna": dna,
    }
    save_freeze_registry(reg)


def activate_component(component_id: str, reason: str, dna: str) -> None:
    """激活已冻结组件"""
    reg = load_freeze_registry()
    if component_id in reg:
        reg[component_id]["frozen"] = False
        reg[component_id]["activated_at"] = _now()
        reg[component_id]["activate_reason"] = reason
        reg[component_id]["activate_dna"] = dna
        save_freeze_registry(reg)


# ═══════════════════════════════════════════════════════════════════
# F1-F7 与 SI 集成
# ═══════════════════════════════════════════════════════════════════

def run_f1f7_verification(component_path: pathlib.Path) -> Dict[str, Any]:
    """对文件/组件执行简化 F1-F7 验证"""
    try:
        from governance.f1_through_f7_verifier import (
            F1IdentityVerification, F2TemporalAnchor, F3RuleTrace,
            F4PersonaRouting, F5ProtectedVocabulary, F6StyleVector,
            F7MistakeLedger, SevenFactorVerifier,
        )
    except Exception as e:
        return {"available": False, "error": str(e)}

    try:
        text = component_path.read_text(encoding="utf-8", errors="ignore") if component_path.is_file() else ""
    except Exception:
        text = ""

    f1 = F1IdentityVerification(
        uid="9622",
        gpg_fingerprint="A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
        gpg_prefix_marker="#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
        identity_dna="#龍芯⚡️2026-06-22-LAYERED-GOVERNANCE-ENGINE-v1.0",
        creation_timestamp="2025-05-20T10:00:00Z",
    )
    ts = datetime.now(timezone.utc)
    shichen_list = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    shichen = shichen_list[ts.hour % 24 // 2]
    dr = digital_root(ts.day)
    f2 = F2TemporalAnchor(
        iso8601=ts.isoformat(),
        shichen=shichen,
        digital_root=dr,
        lunar_calendar="",
        time_window_violation=False,
    )
    f3 = F3RuleTrace(
        rule_ids=["P0", "L0", "L7"],
        rule_chain_hash="a" * 64,
        signature="system_signature",
        audit_log_entries=3,
    )
    f4 = F4PersonaRouting(
        primary_persona="P00",
        persona_weights={"P00": 1.0},
        veto_words_detected=False,
        routing_confidence=0.95,
    )
    cs_score, cs_detail = cultural_sovereignty_score(text)
    f5 = F5ProtectedVocabulary(
        sovereign_terms_found=["龍", "龍魂", "龍芯"],
        sovereign_terms_correct=cs_score >= 0.5,
        character_preservation="龍" in text,
        semantic_integrity=cs_score >= 0.3,
    )
    f6 = F6StyleVector(
        cosine_similarity=0.85,
        vocabulary_consistency=cs_score,
        syntax_pattern_match=0.80,
        tone_consistency=0.85,
    )
    f7 = F7MistakeLedger(
        total_mistakes=0,
        recent_mistakes_30days=0,
        mistake_recovery_rate=1.0,
        critical_mistakes=0,
    )

    verifier = SevenFactorVerifier()
    result = verifier.verify(f1, f2, f3, f4, f5, f6, f7)
    return {
        "available": True,
        "confidence": result.get("confidence", 0.0),
        "passed": result.get("passed", False),
        "result": result.get("result", ""),
        "factors": result.get("factors", {}),
    }


def get_sovereignty_index(uid: str = "UID9622") -> Dict[str, Any]:
    """获取三才主权指数"""
    try:
        from governance.sovereignty_index import get_sovereignty_index as _get_si
        si = _get_si(uid)
        return {
            "available": True,
            "si": si.calculate_si(),
            "level": si.get_sovereignty_level().value,
            "tian": si.tian_score,
            "di": si.di_score,
            "ren": si.ren_score,
            "can_decide": si.can_make_decisions(),
        }
    except Exception as e:
        return {"available": False, "error": str(e)}


# ═══════════════════════════════════════════════════════════════════
# 核心引擎
# ═══════════════════════════════════════════════════════════════════

class LayeredGovernanceEngine:
    """龍魂分层治理自愈引擎"""

    DNA = DNA

    # 服务端口映射（与 longhun-launcher.py 对齐）
    SERVICE_PORTS = {
        "longhun-brain": 9625,
        "identity-portal": 8444,
        "control-panel": 9622,
        "compression-engine": None,  # 一次性任务，无常驻端口
    }

    def __init__(self, root: pathlib.Path = ROOT, auto_load: bool = True):
        self.root = root
        self.layers = _layer_specs()
        self.checks: List[ComponentCheck] = []
        self.heal_records: List[HealRecord] = []
        self.alarm_records: List[AlarmRecord] = []
        self.si_report: Dict[str, Any] = {}
        _ensure_dirs()
        if auto_load:
            self.load_state()

    # ───────────────────────── 状态持久化 ─────────────────────────

    def load_state(self) -> None:
        state = _load_json(STATUS_FILE)
        # 仅读取上次状态作为参考，不覆盖当前检查结果
        self.last_status = state

    def save_status(self) -> None:
        status = {
            "dna": _dna("GOV-STATUS"),
            "timestamp": _now(),
            "engine_dna": self.DNA,
            "layers": self._layer_status_summary(),
            "checks": [asdict(c) for c in self.checks],
            "si_report": self.si_report,
            "summary": self._summary(),
        }
        _save_json(STATUS_FILE, status)

    def _layer_status_summary(self) -> Dict[str, Dict[str, Any]]:
        summary: Dict[str, Dict[str, Any]] = {}
        for layer in self.layers:
            layer_checks = [c for c in self.checks if c.layer_id == layer.id]
            if not layer_checks:
                continue
            scores = [c.score for c in layer_checks]
            avg_score = sum(scores) / len(scores)
            worst = min(layer_checks, key=lambda x: x.score)
            summary[layer.id] = {
                "name": layer.name,
                "tricolor": tricolor_from_score(avg_score),
                "score": round(avg_score, 4),
                "worst_component": worst.component_id,
                "worst_status": worst.status,
                "checks_count": len(layer_checks),
                "error_count": sum(1 for c in layer_checks if c.tricolor == Tricolor.RED),
                "warning_count": sum(1 for c in layer_checks if c.tricolor == Tricolor.YELLOW),
            }
        return summary

    def _summary(self) -> Dict[str, Any]:
        total = len(self.checks)
        errors = sum(1 for c in self.checks if c.tricolor == Tricolor.RED)
        warnings = sum(1 for c in self.checks if c.tricolor == Tricolor.YELLOW)
        ok = total - errors - warnings
        frozen = sum(1 for c in self.checks if c.status == "frozen")
        return {
            "total_checks": total,
            "ok": ok,
            "warning": warnings,
            "error": errors,
            "frozen": frozen,
            "overall_tricolor": Tricolor.RED if errors else (Tricolor.YELLOW if warnings else Tricolor.GREEN),
            "overall_score": round(sum(c.score for c in self.checks) / max(1, total), 4),
        }

    # ───────────────────────── 检查入口 ─────────────────────────

    def run_all_checks(self) -> List[ComponentCheck]:
        self.checks = []
        # 先做一次全局 SI 检查
        self.si_report = get_sovereignty_index("UID9622")

        for layer in self.layers:
            self._check_layer(layer)

        return self.checks

    def _check_layer(self, layer: LayerSpec) -> None:
        # 1) 文件存在性 + DNA 完整性（只检查真正的文件，目录跳过）
        for fp in layer.files:
            if fp.is_dir():
                continue
            self._check_file(layer, fp)

        # 2) 自动发现文件模式（补充检查），每层最多抽查 20 个文本文件
        discovered: List[pathlib.Path] = []
        for pattern in layer.file_patterns:
            if "*" in pattern:
                for matched in self.root.rglob(pattern):
                    if matched.is_file() and matched not in layer.files:
                        discovered.append(matched)
        # 去重、过滤二进制、限制数量
        discovered = self._filter_text_files(discovered)[:20]
        for matched in discovered:
            self._check_file(layer, matched)

        # 3) 进程健康
        for proc_id in layer.processes:
            self._check_process(layer, proc_id)

        # 4) F1-F7 验证（对关键文件）
        if layer.f1_f7_required:
            for fp in layer.files:
                if fp.is_file():
                    self._check_f1f7(layer, fp)

        # 5) SI 维度检查
        if layer.si_dimension and self.si_report.get("available"):
            self._check_si_dimension(layer)

    @staticmethod
    def _filter_text_files(paths: List[pathlib.Path]) -> List[pathlib.Path]:
        """过滤掉二进制文件、隐藏文件、缓存文件、虚拟环境，保留文本文件"""
        text_exts = {
            ".md", ".py", ".txt", ".json", ".yaml", ".yml", ".toml",
            ".js", ".ts", ".html", ".css", ".sh", ".bash", ".zsh",
            ".cpp", ".c", ".h", ".hpp", ".java", ".go", ".rs",
            ".swift", ".kt", ".xml", ".sql", ".log", ".csv",
        }
        skip_dirs = {
            ".git", "__pycache__", ".venv", "venv", "venv_notion",
            "node_modules", "dist", "build", ".pytest_cache", ".mypy_cache",
            "releases", "_archive", "archive", "backup", "backups",
        }
        result = []
        for p in paths:
            parts = p.parts
            if any(part in skip_dirs for part in parts):
                continue
            if any(part.startswith(".") and part not in (".", "..") for part in parts[-3:]):
                continue
            if p.suffix.lower() in text_exts:
                result.append(p)
        return result

    def _check_file(self, layer: LayerSpec, path: pathlib.Path) -> None:
        comp_id = f"{layer.id}:file:{path.name}"
        if is_frozen(comp_id):
            self.checks.append(ComponentCheck(
                layer_id=layer.id,
                component_id=comp_id,
                component_type="file",
                status="frozen",
                tricolor=Tricolor.YELLOW,
                score=0.5,
                message=f"组件已冻结: {path}",
                evidence={"path": str(path), "frozen": True},
                auto_fixable=True,
                fix_action="activate",
            ))
            return

        if not path.exists():
            self.checks.append(ComponentCheck(
                layer_id=layer.id,
                component_id=comp_id,
                component_type="file",
                status="error",
                tricolor=Tricolor.RED,
                score=0.0,
                message=f"关键文件缺失: {path}",
                evidence={"path": str(path), "exists": False},
                auto_fixable=False,
                fix_action="freeze_and_alarm",
            ))
            return

        has_dna = _file_has_dna(path)
        # 二进制/非文本文件跳过 DNA 注入要求
        binary_suffixes = {".db", ".otf", ".ttf", ".woff", ".woff2", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".log", ".pkl", ".npz"}
        skip_dna = path.suffix.lower() in binary_suffixes

        if layer.critical and not has_dna and not skip_dna:
            self.checks.append(ComponentCheck(
                layer_id=layer.id,
                component_id=comp_id,
                component_type="file",
                status="warning",
                tricolor=Tricolor.YELLOW,
                score=0.5,
                message=f"文件存在但缺少 DNA 追溯码: {path}",
                evidence={"path": str(path), "has_dna": False},
                auto_fixable=True,
                fix_action="inject_dna_marker",
            ))
            return

        # 文化主权检查（仅对龍魂相关文本文件，避免无关文件拉低评分）
        cs_score = 1.0
        cs_detail = "跳过文化主权检查"
        if path.suffix in (".md", ".py", ".txt", ".json", ".yaml", ".yml", ".sh"):
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
                # 只有文件内容明显与龍魂/CNSH/主权相关时才检查
                if any(k in text for k in ["龍魂", "龍芯", "CNSH", "LongHun", "longhun", " sovereignty", "主权"]):
                    cs_score, cs_detail = cultural_sovereignty_score(text)
                else:
                    cs_detail = "非龍魂相关文件，跳过"
            except Exception:
                pass

        score = 1.0 if has_dna else 0.85
        if cs_score < 1.0:
            score = min(score, 0.5 + 0.5 * cs_score)
        self.checks.append(ComponentCheck(
            layer_id=layer.id,
            component_id=comp_id,
            component_type="file",
            status="ok",
            tricolor=tricolor_from_score(score),
            score=score,
            message=f"文件正常 ({cs_detail}): {path.name}",
            evidence={"path": str(path), "has_dna": has_dna, "cultural_score": cs_score},
            auto_fixable=False,
        ))

    def _check_process(self, layer: LayerSpec, proc_id: str) -> None:
        comp_id = f"{layer.id}:process:{proc_id}"
        port = self.SERVICE_PORTS.get(proc_id)

        if is_frozen(comp_id):
            self.checks.append(ComponentCheck(
                layer_id=layer.id,
                component_id=comp_id,
                component_type="process",
                status="frozen",
                tricolor=Tricolor.YELLOW,
                score=0.5,
                message=f"进程已冻结: {proc_id}",
                evidence={"proc_id": proc_id, "frozen": True},
                auto_fixable=True,
                fix_action="activate_and_restart",
            ))
            return

        running = False
        pid = None
        if port:
            running = _is_port_open(port)
            pid = _find_pid_by_port(port)
        else:
            # 对于一次性任务，检查最近是否执行过
            running = self._check_task_executed_recently(proc_id)

        if not running:
            self.checks.append(ComponentCheck(
                layer_id=layer.id,
                component_id=comp_id,
                component_type="process",
                status="error",
                tricolor=Tricolor.RED,
                score=0.0,
                message=f"进程未运行: {proc_id}",
                evidence={"proc_id": proc_id, "port": port, "pid": pid},
                auto_fixable=True,
                fix_action="restart_process",
            ))
            return

        self.checks.append(ComponentCheck(
            layer_id=layer.id,
            component_id=comp_id,
            component_type="process",
            status="ok",
            tricolor=Tricolor.GREEN,
            score=1.0,
            message=f"进程运行中: {proc_id}",
            evidence={"proc_id": proc_id, "port": port, "pid": pid},
            auto_fixable=False,
        ))

    def _check_f1f7(self, layer: LayerSpec, path: pathlib.Path) -> None:
        comp_id = f"{layer.id}:f1f7:{path.name}"
        result = run_f1f7_verification(path)

        if not result.get("available"):
            self.checks.append(ComponentCheck(
                layer_id=layer.id,
                component_id=comp_id,
                component_type="f1f7",
                status="warning",
                tricolor=Tricolor.YELLOW,
                score=0.6,
                message=f"F1-F7 验证器不可用: {result.get('error')}",
                evidence={"path": str(path), "error": result.get("error")},
                auto_fixable=False,
            ))
            return

        conf = result.get("confidence", 0.0)
        passed = result.get("passed", False)
        status = "ok" if passed else ("warning" if conf >= 0.50 else "error")
        self.checks.append(ComponentCheck(
            layer_id=layer.id,
            component_id=comp_id,
            component_type="f1f7",
            status=status,
            tricolor=tricolor_from_score(conf),
            score=conf,
            message=f"F1-F7 置信度 {conf:.4f}: {result.get('result')}",
            evidence={"path": str(path), "confidence": conf, "passed": passed, "factors": result.get("factors", {})},
            auto_fixable=not passed,
            fix_action="freeze_component" if conf < 0.50 else "alarm_only",
        ))

    def _check_si_dimension(self, layer: LayerSpec) -> None:
        comp_id = f"{layer.id}:si:{layer.si_dimension}"
        dim = layer.si_dimension
        dim_score = self.si_report.get(dim, 0.0)
        si = self.si_report.get("si", 0.0)

        if si < 0.34:
            status = "error"
            tricolor = Tricolor.RED
            score = si
            message = f"三才主权指数失锚 (SI={si:.4f} < 0.34)，{dim} 层锁定"
            auto_fix = False
            fix_action = "alarm_and_lock"
        elif dim_score < 0.5:
            status = "warning"
            tricolor = Tricolor.YELLOW
            score = dim_score
            message = f"{dim} 维度薄弱 ({dim_score:.4f})"
            auto_fix = True
            fix_action = "alarm_only"
        else:
            status = "ok"
            tricolor = Tricolor.GREEN
            score = dim_score
            message = f"{dim} 维度健康 ({dim_score:.4f})"
            auto_fix = False
            fix_action = None

        self.checks.append(ComponentCheck(
            layer_id=layer.id,
            component_id=comp_id,
            component_type="sovereignty",
            status=status,
            tricolor=tricolor,
            score=score,
            message=message,
            evidence={"dimension": dim, "dim_score": dim_score, "si": si},
            auto_fixable=auto_fix,
            fix_action=fix_action,
        ))

    def _check_task_executed_recently(self, proc_id: str, hours: int = 24) -> bool:
        """检查一次性任务最近一次执行时间"""
        log_path = LOG_DIR / "autostart.log"
        if not log_path.exists():
            return False
        try:
            mtime = log_path.stat().st_mtime
            return (time.time() - mtime) < (hours * 3600)
        except Exception:
            return False

    # ───────────────────────── 报警 ─────────────────────────

    def alarm(self, level: str, layer_id: str, component_id: str, message: str, tricolor: str) -> AlarmRecord:
        rec = AlarmRecord(
            dna=_dna("GOV-ALARM", f"{layer_id}:{component_id}"),
            timestamp=_now(),
            level=level,
            layer_id=layer_id,
            component_id=component_id,
            message=message,
            tricolor=tricolor,
        )
        self.alarm_records.append(rec)
        _append_jsonl(ALARM_LOG, asdict(rec))
        return rec

    # ───────────────────────── 自动修复 ─────────────────────────

    def heal(self, dry_run: bool = False) -> List[HealRecord]:
        """
        自动修复所有可修复问题。
        原则：只冻结/停用/重启，不删除任何数据。
        """
        self.heal_records = []
        if not self.checks:
            self.run_all_checks()

        for check in self.checks:
            if check.status == "ok":
                continue
            if not check.auto_fixable and dry_run:
                continue

            record = self._heal_check(check, dry_run=dry_run)
            if record:
                self.heal_records.append(record)
                _append_jsonl(HEAL_LOG, asdict(record))

        # 修复后重新巡检，反映最新状态
        self.run_all_checks()
        self.save_status()
        return self.heal_records

    def _heal_check(self, check: ComponentCheck, dry_run: bool = False) -> Optional[HealRecord]:
        dna = _dna("GOV-HEAL", f"{check.layer_id}:{check.component_id}")
        before = check.status
        after = before
        action = "observe"
        reason = check.message
        decision_path: List[str] = []
        side_effects: List[str] = []

        # L0 宪法文件 AGENTS.md 缺失 → 优先自动创建（而不是冻结）
        if (check.component_type == "file" and check.status == "error" and
                check.layer_id == LayerLevel.L0 and
                pathlib.Path(check.evidence.get("path", "")).name == "AGENTS.md"):
            path = pathlib.Path(check.evidence.get("path", ""))
            decision_path.append("L0 宪法文件 AGENTS.md 缺失，自动创建最小版本")
            action = "create_agents_md"
            if not dry_run:
                if self._create_minimal_agents_md(path):
                    after = "ok"
                    side_effects.append(f"已创建 {path}")
                else:
                    freeze_component(check.component_id, reason, check.layer_id, dna)
                    self.alarm("critical", check.layer_id, check.component_id, f"AGENTS.md 创建失败已冻结: {reason}", Tricolor.RED)
                    after = "frozen"

        # L0/L7 关键层硬失败 → 立即冻结并报警
        elif check.layer_id in (LayerLevel.L0, LayerLevel.L7) and check.tricolor == Tricolor.RED:
            decision_path.append("L0/L7 关键层出现 🔴，触发冻结保护")
            action = "freeze"
            if not dry_run:
                freeze_component(check.component_id, reason, check.layer_id, dna)
                self.alarm("critical", check.layer_id, check.component_id, f"关键层硬失败已冻结: {reason}", Tricolor.RED)
            after = "frozen"

        elif check.component_type == "file" and check.status == "error":
            # 文件缺失：无法自动恢复，只能冻结并报警（AGENTS.md 已单独处理）
            decision_path.append("文件缺失，无法重建，执行冻结保护")
            action = "freeze"
            if not dry_run:
                freeze_component(check.component_id, reason, check.layer_id, dna)
                self.alarm("critical", check.layer_id, check.component_id, f"关键文件缺失已冻结: {reason}", Tricolor.RED)
            after = "frozen"

        elif check.component_type == "file" and check.status == "warning" and check.fix_action == "inject_dna_marker":
            decision_path.append("关键文件缺少 DNA，自动注入标记（不修改内容逻辑）")
            action = "inject_dna_marker"
            if not dry_run:
                if self._inject_dna_marker(pathlib.Path(check.evidence["path"])):
                    after = "ok"
                    side_effects.append("文件头部追加 DNA 追溯标记")
                else:
                    after = "frozen"
                    freeze_component(check.component_id, reason, check.layer_id, dna)

        elif check.component_type == "process" and check.fix_action == "restart_process":
            decision_path.append("进程未运行，尝试重启")
            action = "restart"
            if not dry_run:
                if self._restart_process(check.evidence["proc_id"]):
                    after = "ok"
                    side_effects.append("进程已重启")
                else:
                    after = "frozen"
                    freeze_component(check.component_id, reason, check.layer_id, dna)
                    self.alarm("critical", check.layer_id, check.component_id, f"进程重启失败已冻结: {reason}", Tricolor.RED)

        elif check.component_type == "f1f7" and check.fix_action == "freeze_component":
            decision_path.append("F1-F7 置信度低于阈值，冻结组件等待人工复核")
            action = "freeze"
            if not dry_run:
                freeze_component(check.component_id, reason, check.layer_id, dna)
                self.alarm("warning", check.layer_id, check.component_id, f"F1-F7 未通过已冻结: {reason}", Tricolor.YELLOW)
            after = "frozen"

        elif check.component_type == "f1f7" and check.fix_action == "alarm_only":
            decision_path.append("F1-F7 警告，仅报警不冻结")
            action = "alarm"
            if not dry_run:
                self.alarm("warning", check.layer_id, check.component_id, reason, Tricolor.YELLOW)
            after = "warning"

        elif check.component_type == "sovereignty" and check.fix_action == "alarm_only":
            decision_path.append("三才维度薄弱，仅报警")
            action = "alarm"
            if not dry_run:
                self.alarm("warning", check.layer_id, check.component_id, reason, Tricolor.YELLOW)
            after = "warning"

        elif check.component_type == "sovereignty" and check.fix_action == "alarm_and_lock":
            decision_path.append("SI < 0.34，主权失锚，报警并锁定决策能力")
            action = "lock"
            if not dry_run:
                self.alarm("critical", check.layer_id, check.component_id, reason, Tricolor.RED)
            after = "locked"

        else:
            # 默认：观察并报警
            decision_path.append("无可执行自动修复策略，记录并报警")
            action = "alarm"
            if not dry_run:
                level = "critical" if check.tricolor == Tricolor.RED else "warning"
                self.alarm(level, check.layer_id, check.component_id, reason, check.tricolor)
            after = check.status

        if dry_run:
            action = f"[DRY-RUN] {action}"

        return HealRecord(
            dna=dna,
            timestamp=_now(),
            layer_id=check.layer_id,
            component_id=check.component_id,
            action=action,
            reason=reason,
            before_status=before,
            after_status=after,
            decision_path=decision_path,
            side_effects=side_effects,
        )

    def _inject_dna_marker(self, path: pathlib.Path) -> bool:
        """在文件中注入 DNA 标记，不破坏原有格式"""
        try:
            if not path.exists():
                return False
            dna = _dna("AUTO-DNA", path.name)
            original = path.read_text(encoding="utf-8")
            if dna in original:
                return True

            suffix = path.suffix.lower()
            name_upper = path.name.upper()
            # 无后缀的协议/指南文件用 # 注释
            if name_upper in ("LICENSE", "CONTRIBUTING", "CODE_OF_CONDUCT", "COPYING"):
                marker = f"# {dna} 自动注入·分层治理自愈引擎 · 来源可查\n"
            elif suffix == ".json":
                # JSON 不能加注释，把 DNA 写入顶层 _dna 字段
                try:
                    data = json.loads(original)
                    if isinstance(data, dict):
                        existing_dna = data.get("_dna", "")
                        if dna in original and "#龍芯⚡️" in existing_dna:
                            return True
                        data["_dna"] = dna
                        data["_dna_note"] = "自动注入·分层治理自愈引擎·来源可查"
                        data["_longhun_identity"] = "龍魂 · UID9622 · 中国自主可控"
                        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
                        return True
                    else:
                        # JSON 顶层不是对象，无法安全注入
                        return False
                except json.JSONDecodeError:
                    return False
            elif suffix in (".py", ".sh", ".yaml", ".yml", ".jsonl"):
                marker = f"# {dna} 自动注入·分层治理自愈引擎 · 来源可查\n"
            elif suffix in (".md", ".html", ".htm"):
                marker = f"<!-- {dna} 自动注入·分层治理自愈引擎 · 来源可查 -->\n"
            elif suffix in (".js", ".ts", ".cpp", ".c", ".java", ".rs"):
                marker = f"// {dna} 自动注入·分层治理自愈引擎 · 来源可查\n"
            else:
                # 未知格式，跳过注入以免破坏
                return False

            path.write_text(marker + original, encoding="utf-8")
            return True
        except Exception as e:
            self.alarm("warning", "L1", f"dna-inject:{path.name}", f"DNA 注入失败: {e}", Tricolor.YELLOW)
            return False

    def _create_minimal_agents_md(self, path: pathlib.Path) -> bool:
        """创建最小化 AGENTS.md 宪法文件（L0 缺失时自动补齐）"""
        try:
            dna = _dna("AGENTS-CREATE", "L0")
            content = f"""# 龍魂系统 · 项目宪法层

> 本文件由分层治理自愈引擎自动生成，确保 L0 宪法层完整。
> 来源可查、去向可追、责任可究。

## 身份与主权

- 最终决策者：**UID9622**
- 系统目标：中国自主可控，数据主权归集本地
- 核心原则：人民数据主权、平台服务降级、忠诚执行、实心办事

## 不可变铁律

1. **来源不可删** · 影响不可覆 · 贡献不可抹除
2. **只冻结/停用，不删除** 任何用户授权或数据
3. **每个动作必须绑定 DNA 追溯码**
4. **三才主权指数 SI < 0.34 时锁定决策能力**

## 追溯

- DNA: `{dna}`
- 引擎: `{self.DNA}`
- 生成时间: `{_now()}`
"""
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            return True
        except Exception as e:
            self.alarm("critical", "L0", "agents-md-create", f"AGENTS.md 创建失败: {e}", Tricolor.RED)
            return False

    def _restart_process(self, proc_id: str) -> bool:
        """尝试重启进程/服务"""
        try:
            launcher = ROOT / "bin" / "longhun-launcher.py"
            if not launcher.exists():
                return False
            if proc_id in ("compression-engine",):
                # 一次性任务：调用压缩引擎
                script = ROOT / "scripts" / "longhun_compression_engine.py"
                subprocess.run(
                    [sys.executable, str(script), "--compress-all-skills"],
                    cwd=ROOT, check=False, timeout=300,
                )
                return True
            # 常驻服务：调用启动器重启单个服务
            subprocess.run(
                [sys.executable, str(launcher), "start"],
                cwd=ROOT, check=False, timeout=120,
            )
            return True
        except Exception as e:
            self.alarm("warning", "L5", f"restart:{proc_id}", f"重启失败: {e}", Tricolor.YELLOW)
            return False

    # ───────────────────────── 激活 ─────────────────────────

    def activate(self, component_id: str) -> HealRecord:
        """手动激活已冻结组件"""
        dna = _dna("GOV-ACTIVATE", component_id)
        reason = f"手动激活组件 {component_id}"
        activate_component(component_id, reason, dna)
        record = HealRecord(
            dna=dna,
            timestamp=_now(),
            layer_id="manual",
            component_id=component_id,
            action="activate",
            reason=reason,
            before_status="frozen",
            after_status="active",
            decision_path=["用户手动请求激活"],
            side_effects=["组件从冻结注册表移除冻结标记"],
        )
        _append_jsonl(HEAL_LOG, asdict(record))
        return record

    # ───────────────────────── 报告 ─────────────────────────

    def print_report(self) -> None:
        summary = self._summary()
        print("\n" + "=" * 70)
        print("  🐉 龍魂分层治理自愈引擎 · 状态报告")
        print("=" * 70)
        print(f"  DNA: {self.DNA}")
        print(f"  时间: {_now()}")
        print(f"  总检查项: {summary['total_checks']}")
        print(f"  🟢 正常: {summary['ok']}  🟡 警告: {summary['warning']}  🔴 错误: {summary['error']}  🧊 冻结: {summary['frozen']}")
        print(f"  综合评分: {summary['overall_score']:.4f}  {summary['overall_tricolor']}")

        if self.si_report.get("available"):
            print(f"\n  三才主权指数 SI: {self.si_report.get('si', 0):.4f} ({self.si_report.get('level', '?')})")
            print(f"    天: {self.si_report.get('tian', 0):.2f}  地: {self.si_report.get('di', 0):.2f}  人: {self.si_report.get('ren', 0):.2f}")

        print("\n  分层状态:")
        print("  " + "-" * 66)
        layer_summary = self._layer_status_summary()
        for layer in self.layers:
            info = layer_summary.get(layer.id)
            if not info:
                continue
            print(f"  {layer.id} {layer.name:<18} {info['tricolor']} 评分:{info['score']:.2f} "
                  f"(🔴{info['error_count']} 🟡{info['warning_count']})")

        if self.checks:
            print("\n  异常明细:")
            print("  " + "-" * 66)
            for c in self.checks:
                if c.tricolor != Tricolor.GREEN:
                    print(f"  {c.tricolor} [{c.layer_id}] {c.component_type}:{c.component_id.split(':')[-1]}")
                    print(f"      {c.message}")

        if self.heal_records:
            print(f"\n  本次修复动作: {len(self.heal_records)} 条")
            for r in self.heal_records:
                print(f"    - {r.action}: {r.layer_id}:{r.component_id} ({r.before_status}->{r.after_status}) {r.dna}")

        print("\n" + "=" * 70 + "\n")

    def json_report(self) -> Dict[str, Any]:
        return {
            "dna": _dna("GOV-REPORT"),
            "timestamp": _now(),
            "engine_dna": self.DNA,
            "summary": self._summary(),
            "si_report": self.si_report,
            "layers": self._layer_status_summary(),
            "checks": [asdict(c) for c in self.checks],
            "heal_records": [asdict(r) for r in self.heal_records],
            "alarm_records": [asdict(r) for r in self.alarm_records],
        }


# ═══════════════════════════════════════════════════════════════════
# 命令行入口
# ═══════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="龍魂分层治理自愈引擎")
    parser.add_argument("command", choices=["status", "heal", "watch", "activate", "freeze"])
    parser.add_argument("--component", type=str, help="activate/freeze 时指定组件 ID")
    parser.add_argument("--reason", type=str, default="manual", help="freeze 原因")
    parser.add_argument("--dry-run", action="store_true", help="heal 时只演练不执行")
    parser.add_argument("--json", action="store_true", help="输出 JSON 报告")
    parser.add_argument("--interval", type=int, default=60, help="watch 模式间隔秒数")
    args = parser.parse_args()

    engine = LayeredGovernanceEngine()

    if args.command == "status":
        engine.run_all_checks()
        engine.save_status()
        if args.json:
            print(json.dumps(engine.json_report(), ensure_ascii=False, indent=2))
        else:
            engine.print_report()

    elif args.command == "heal":
        print("🐉 启动分层治理自愈流程...")
        engine.run_all_checks()
        engine.heal(dry_run=args.dry_run)
        if args.json:
            print(json.dumps(engine.json_report(), ensure_ascii=False, indent=2))
        else:
            engine.print_report()

    elif args.command == "watch":
        print(f"🐉 进入分层治理值守模式，每 {args.interval} 秒巡检一次 (Ctrl+C 退出)")
        try:
            while True:
                engine = LayeredGovernanceEngine()
                engine.run_all_checks()
                engine.heal(dry_run=False)
                engine.print_report()
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n👋 退出值守模式")

    elif args.command == "activate":
        if not args.component:
            print("❌ 请使用 --component 指定要激活的组件 ID")
            sys.exit(1)
        record = engine.activate(args.component)
        print(f"✅ 已激活 {args.component} · DNA: {record.dna}")

    elif args.command == "freeze":
        if not args.component:
            print("❌ 请使用 --component 指定要冻结的组件 ID")
            sys.exit(1)
        dna = _dna("MANUAL-FREEZE", args.component)
        freeze_component(args.component, args.reason, "manual", dna)
        print(f"🧊 已冻结 {args.component} · 原因: {args.reason} · DNA: {dna}")


if __name__ == "__main__":
    main()
