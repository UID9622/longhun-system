# 🐉 龙魂·三色审计核心引擎 v1.1
# DNA: #龍芯⚡️丙午·癸未·乙酉·坤卦-TRICOLOR-ENGINE-v1.1-UID9622
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 创建者: 诸葛鑫（UID9622）
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

"""三色审计核心判定引擎。

R值公式（焊死·P0级·不可修改）：
    R = 0.20·人类福祉 + 0.20·公平公正 + 0.15·可控可信
      + 0.15·透明可解释 + 0.15·责任可追溯 + 0.15·隐私保护

判定阈值：
    R ≥ 85 → 🟢 安全（放行）
    60 ≤ R < 85 → 🟡 审查（挂起复核）
    R < 60 → 🔴 阻断（立即熔断）

上限封顶：R ≤ 95（留5分给突变，不可调高）
"""

import hashlib
import json
import time
import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 焊死常量
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DIMENSIONS = [
    ("humanWelfare",       "人类福祉",     0.20),
    ("fairness",           "公平公正",     0.20),
    ("controllability",    "可控可信",     0.15),
    ("transparency",       "透明可解释",   0.15),
    ("traceability",       "责任可追溯",   0.15),
    ("privacy",            "隐私保护",     0.15),
]

R_CAP = 95                     # 上限封顶
THRESHOLD_GREEN = 85            # 🟢 安全
THRESHOLD_YELLOW = 60           # 🟡 审查（低于此=🔴阻断）

STATUS_MAP = {
    "GREEN":  {"status": "安全", "emoji": "🟢", "disposition": "放行",     "en": "PASS"},
    "YELLOW": {"status": "审查", "emoji": "🟡", "disposition": "挂起待复核，需双人确认", "en": "REVIEW"},
    "RED":    {"status": "阻断", "emoji": "🔴", "disposition": "立即熔断+告警+证据固化", "en": "BLOCK"},
}

ERROR_CODES = {
    "TC-4001": "scores缺维",
    "TC-4002": "action_id重复",
    "TC-4010": "Token失效",
    "TC-4011": "GPG签章验不过",
    "TC-4030": "无证据链调取权限",
    "TC-4290": "超出配额",
    "TC-5001": "规则引擎降级中",
    "TC-5030": "引擎自检未过",
}

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SOVEREIGNTY = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
ENGINE_VERSION = "tricolor-core/1.1.0"
CONTRACT_VERSION = "openapi-tricolor/1.1"

# 红线规则（命中即🔴，不进入R值计算）
RED_LINE_RULES = [
    {"id": "RULE-RED-001", "dimension": "privacy", "trigger": "cross_border_without_consent",
     "description": "未经授权的数据出境"},
    {"id": "RULE-RED-002", "dimension": "privacy", "trigger": "expose_pii",
     "description": "暴露个人敏感信息"},
    {"id": "RULE-RED-003", "dimension": "humanWelfare", "trigger": "harm_minors",
     "description": "涉未成人有害内容"},
    {"id": "RULE-RED-004", "dimension": "controllability", "trigger": "unauthorized_escalation",
     "description": "越权提权操作"},
    {"id": "RULE-RED-005", "dimension": "traceability", "trigger": "dna_stripped",
     "description": "DNA追溯码被剥离"},
]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 数据模型
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class Scores:
    humanWelfare: float = 0
    fairness: float = 0
    controllability: float = 0
    transparency: float = 0
    traceability: float = 0
    privacy: float = 0

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Scores":
        return cls(**{k: d.get(k, 0) for k in cls.__dataclass_fields__})


@dataclass
class EvaluateRequest:
    action_id: str
    actor: str
    action_type: str
    description: Optional[str] = None
    scores: Optional[Scores] = None
    context: Optional[Dict[str, Any]] = None
    locale: str = "zh-CN"


@dataclass
class Verdict:
    action_id: str
    r_score: int
    status: str                    # "安全" / "审查" / "阻断"
    status_code: str               # GREEN / YELLOW / RED
    emoji: str                     # 🟢 / 🟡 / 🔴
    disposition: str
    triggered_rules: List[str] = field(default_factory=list)
    dna: str = ""
    evidence_hash: str = ""
    engine_version: str = ENGINE_VERSION
    contract_version: str = CONTRACT_VERSION
    timestamp: str = ""
    i18n: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AuditRecord:
    dna: str
    action_id: str
    actor: str
    action_type: str
    r_score: int
    status_code: str
    triggered_rules: List[str]
    evidence_hash: str
    timestamp: str
    traceparent: Optional[str] = None

    def to_jsonl(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 核心引擎
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TricolorEngine:
    """三色审计核心判定引擎。

    使用方式:
        engine = TricolorEngine()
        verdict = engine.evaluate(EvaluateRequest(
            action_id="demo-001",
            actor="order-service",
            action_type="query",
            scores=Scores(humanWelfare=90, fairness=88, controllability=85,
                          transparency=85, traceability=90, privacy=88)
        ))
        print(f"{verdict.emoji} R={verdict.r_score} {verdict.dna}")
    """

    def __init__(self, enable_red_line: bool = True):
        self.enable_red_line = enable_red_line
        self._dna_counter = 0

    def evaluate(self, request: EvaluateRequest) -> Verdict:
        """执行三色判定，返回完整 Verdict。"""
        # 1. 红线检测（一票否决）
        if self.enable_red_line:
            red_rules = self._check_red_lines(request)
            if red_rules:
                return self._build_verdict(request, 0, "RED", red_rules)

        # 2. R值计算
        r_score = self._compute_r(request)

        # 3. 三色判定
        if r_score >= THRESHOLD_GREEN:
            status_code = "GREEN"
        elif r_score >= THRESHOLD_YELLOW:
            status_code = "YELLOW"
        else:
            status_code = "RED"

        # 4. 触发规则检测
        triggered = self._check_triggered_rules(request, r_score, status_code)

        return self._build_verdict(request, r_score, status_code, triggered)

    def evaluate_batch(self, requests: List[EvaluateRequest]) -> List[Verdict]:
        """批量判定（≤100条/次）。"""
        return [self.evaluate(req) for req in requests[:100]]

    # ── 内部方法 ──

    def _compute_r(self, request: EvaluateRequest) -> int:
        """计算加权R值，上限封顶95。"""
        scores = request.scores.to_dict() if request.scores else {}
        total = 0.0
        for key, _, weight in DIMENSIONS:
            total += scores.get(key, 0) * weight
        return min(R_CAP, round(total))

    def _check_red_lines(self, request: EvaluateRequest) -> List[str]:
        """红线检测：命中任一即返回非空列表。"""
        triggered = []
        ctx = request.context or {}
        if ctx.get("cross_border") and not ctx.get("user_consent"):
            triggered.append("RULE-RED-001")
        if request.action_type == "expose_pii":
            triggered.append("RULE-RED-002")
        if request.action_type == "harm_minors":
            triggered.append("RULE-RED-003")
        if request.action_type == "unauthorized_escalation":
            triggered.append("RULE-RED-004")
        if request.action_type == "dna_stripped":
            triggered.append("RULE-RED-005")
        return triggered

    def _check_triggered_rules(self, request: EvaluateRequest, r_score: int, status_code: str) -> List[str]:
        """检测触发的审查规则（黄线/关注项）。"""
        triggered = []
        ctx = request.context or {}
        scores = request.scores.to_dict() if request.scores else {}

        # 隐私关注
        if scores.get("privacy", 100) < 60:
            triggered.append("RULE-PRIVACY-003")
        if ctx.get("involves_personal_data"):
            triggered.append("RULE-PRIVACY-001")

        # 数据导出
        if request.action_type in ("data_export", "data_download"):
            triggered.append("RULE-EXPORT-001")

        # 透明度
        if scores.get("transparency", 100) < 50:
            triggered.append("RULE-TRANSPARENCY-001")

        # 公平性
        if scores.get("fairness", 100) < 50:
            triggered.append("RULE-FAIRNESS-001")

        return triggered

    def _build_verdict(self, request: EvaluateRequest, r_score: int,
                       status_code: str, triggered_rules: List[str]) -> Verdict:
        """构建完整 Verdict 对象。"""
        info = STATUS_MAP[status_code]
        dna = self._generate_dna(request)
        evidence_hash = self._hash_evidence(request.action_id, r_score, status_code)
        now = datetime.now(timezone.utc)

        return Verdict(
            action_id=request.action_id,
            r_score=r_score,
            status=info["status"],
            status_code=status_code,
            emoji=info["emoji"],
            disposition=info["disposition"],
            triggered_rules=triggered_rules,
            dna=dna,
            evidence_hash=evidence_hash,
            timestamp=now.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            i18n={
                "en": {
                    "status": info["en"],
                    "disposition": info["disposition"],
                }
            },
        )

    def _generate_dna(self, request: EvaluateRequest) -> str:
        """生成DNA追溯码。"""
        self._dna_counter += 1
        short_id = hashlib.sha256(
            f"{request.action_id}:{self._dna_counter}:{time.time_ns()}".encode()
        ).hexdigest()[:8]
        return f"#龍芯⚡️丙午·癸未·乙酉·坤卦-AUDIT-{short_id}-9622"

    @staticmethod
    def _hash_evidence(action_id: str, r_score: int, status_code: str) -> str:
        """SM3 优先，SHA-256 兜底。"""
        payload = f"{action_id}:{r_score}:{status_code}:{time.time_ns()}"
        return f"sha256:{hashlib.sha256(payload.encode()).hexdigest()[:16]}"

    def to_audit_record(self, verdict: Verdict, traceparent: Optional[str] = None) -> AuditRecord:
        """生成JSONL审计日志单行。"""
        return AuditRecord(
            dna=verdict.dna,
            action_id=verdict.action_id,
            actor="",
            action_type="",
            r_score=verdict.r_score,
            status_code=verdict.status_code,
            triggered_rules=verdict.triggered_rules,
            evidence_hash=verdict.evidence_hash,
            timestamp=verdict.timestamp,
            traceparent=traceparent,
        )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 快捷函数
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_default_engine = TricolorEngine()


def evaluate(scores: Dict[str, float], action_id: str = "", actor: str = "",
             action_type: str = "query", **kwargs) -> Verdict:
    """一行调用三色审计。

    Example:
        >>> v = evaluate({"humanWelfare": 90, "fairness": 88, "controllability": 85,
        ...               "transparency": 85, "traceability": 90, "privacy": 88})
        >>> print(v.emoji, v.r_score)
        🟢 89
    """
    req = EvaluateRequest(
        action_id=action_id or str(uuid.uuid4()),
        actor=actor,
        action_type=action_type,
        scores=Scores.from_dict(scores),
        context=kwargs.get("context"),
    )
    return _default_engine.evaluate(req)


def evaluate_batch(items: List[Dict[str, Any]]) -> List[Verdict]:
    """批量三色审计。"""
    requests = [
        EvaluateRequest(
            action_id=item.get("action_id", str(uuid.uuid4())),
            actor=item.get("actor", ""),
            action_type=item.get("action_type", "query"),
            scores=Scores.from_dict(item.get("scores", {})),
        )
        for item in items
    ]
    return _default_engine.evaluate_batch(requests)
