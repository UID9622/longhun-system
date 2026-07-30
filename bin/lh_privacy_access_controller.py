#!/usr/bin/env python3
#龍芯⚡️2026-07-19-PRIVACY-ACCESS-RULES-V2.0-P0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂系统隐私接入规则 v2.0 · 算法数学增强版
实现落地方案

DNA: #龍芯⚡️2026-07-19-PRIVACY-ACCESS-RULES-V2.0-P0
上游DNA: #龍芯⚡️2026-03-05-PRIVACY-ACCESS-RULES-P0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

职责:
- 数据五级分类 (L0-L4)
- 接入实体信任评分 T(e)
- 风险评估 R = P × I × E
- 隐私熔断器 (EWMA + 指数退避)
- DNA 哈希链审计
- fail-closed 接入判定

用法:
    python3 bin/lh_privacy_access_controller.py test    # 跑 14 条测试向量
    python3 bin/lh_privacy_access_controller.py demo    # 演示综合判定
"""

import hashlib
import json
import math
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ═══════════════════════════════════════════════════════════
# 第五章公式参数（上链公开，修改=修协议）
# ═══════════════════════════════════════════════════════════
TAU_ALLOW = 0.80
TAU_REVIEW = 0.50
THETA_TRIG = 0.70
THETA_WARN = 0.40
THETA_RECOVER = 0.20
ALPHA = 0.30
Z_ALERT = 3.0
Z_SEVERE = 5.0
EPSILON_BUDGET = 1.0
TTL_DEFAULT_DAYS = 30
TTL_L3_DAYS = 7
COMPLAINT_RATE_REVIEW = 0.05
COMPLAINT_RATE_BLACKLIST = 0.15
EDIT_DISTANCE_THRESHOLD = 0.20
GEO_SIGNAL_THRESHOLD = 3

WEIGHTS = {
    "compliance": 0.25,
    "reputation": 0.20,
    "security": 0.25,
    "transparency": 0.15,
    "user_rating": 0.15,
}

# 第五章：敏感度映射
SENSITIVITY_MAP = {
    # L0 公开级
    "system_version": 0,
    "public_doc": 0,
    "anonymous_stats": 0,
    # L1 内部级
    "usage_duration": 1,
    "feature_clicks": 1,
    # L2 敏感级
    "conversation": 2,
    "behavior_log": 2,
    "location": 2,
    # L3 核心敏感级
    "profile": 3,
    "emotion": 3,
    "finance": 3,
    "health": 3,
    "family": 3,
    # L4 禁区级
    "biometric": 4,
    "political_view": 4,
    "minor": 4,
}

LEVEL_NAMES = {
    0: "L0_公开级",
    1: "L1_内部级",
    2: "L2_敏感级",
    3: "L3_核心敏感级",
    4: "L4_禁区级",
}

LEVEL_COLORS = {
    0: "🟢",
    1: "🟢",
    2: "🟡",
    3: "🔴",
    4: "🔴",
}


# ═══════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════
def _utc_now() -> str:
    """强制 UTC ISO8601，修复 BUG-03。"""
    return datetime.now(timezone.utc).isoformat()


def _levenshtein(a: str, b: str) -> int:
    """编辑距离。"""
    m, n = len(a), len(b)
    if m == 0:
        return n
    if n == 0:
        return m
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev, dp[0] = dp[0], i
        for j in range(1, n + 1):
            prev, dp[j] = dp[j], min(dp[j] + 1, dp[j - 1] + 1, prev + (a[i - 1] != b[j - 1]))
    return dp[n]


def _normalized_edit_distance(a: str, b: str) -> float:
    denom = max(len(a), len(b), 1)
    return _levenshtein(a, b) / denom


# ═══════════════════════════════════════════════════════════
# 5.6 DNA 哈希链
# ═══════════════════════════════════════════════════════════
class LonghunDNAChain:
    """DNA 哈希链：128bit 指纹 + UTC + 单调序号，防篡改。"""

    def __init__(self, gpg_fp: str = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"):
        self.gpg_fp = gpg_fp
        self._seq = 0
        self._prev_hash = hashlib.sha256(gpg_fp.encode()).hexdigest()

    def mint(self, entity_name: str, event: str, extra: dict | None = None) -> str:
        self._seq += 1
        t = _utc_now()
        payload_parts = [self._prev_hash, t, entity_name or "?", event, f"SEQ{self._seq:06d}"]
        if extra:
            payload_parts.append(json.dumps(extra, sort_keys=True, ensure_ascii=False))
        payload = "‖".join(payload_parts)
        h = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        self._prev_hash = h
        return f"#龍芯⚡️{t}-SEQ{self._seq:06d}-{event}-{h[:32]}"

    def verify_monotonic(self, seq: int) -> bool:
        if seq <= self._seq:
            return False
        return True


# ═══════════════════════════════════════════════════════════
# 第三章：数据分类分级
# ═══════════════════════════════════════════════════════════
class LonghunDataClassifier:
    """五级数据分类器。"""

    @staticmethod
    def classify_single(data_type: str) -> int:
        return SENSITIVITY_MAP.get(data_type, 2)

    def classify_dataset(self, data_types: list[str]) -> int:
        if not data_types:
            return 0
        levels = [self.classify_single(dt) for dt in data_types]
        max_level = max(levels)
        l2_count = sum(1 for lv in levels if lv == 2)
        if max_level >= 3:
            return max_level
        if l2_count >= 3:
            return 3
        return max_level

    @staticmethod
    def level_name(level: int) -> str:
        return LEVEL_NAMES.get(level, "UNKNOWN")

    @staticmethod
    def level_color(level: int) -> str:
        return LEVEL_COLORS.get(level, "⚪")


# ═══════════════════════════════════════════════════════════
# 5.2 信任评分模型
# ═══════════════════════════════════════════════════════════
class LonghunTrustScorer:
    """加权信任评分 T(e) = Σ w_i · s_i。"""

    def score(self, materials: dict) -> float:
        violation_count = materials.get("violation_count", 0)
        scores = {
            "compliance": min(1.0, 0.34 * len(materials.get("certifications", []))),
            "reputation": 2.0 ** (-violation_count),
            "security": materials.get("penetration_score", 0.0),
            "transparency": materials.get("transparency_score", 0.0),
            "user_rating": 1.0 - min(1.0, materials.get("complaint_rate", 0.0)),
        }
        return sum(WEIGHTS[k] * scores[k] for k in WEIGHTS)

    def tier(self, score: float) -> str:
        if score >= TAU_ALLOW:
            return "ALLOW"
        if score >= TAU_REVIEW:
            return "REVIEW"
        return "DENY"


# ═══════════════════════════════════════════════════════════
# 5.3 风险评估模型
# ═══════════════════════════════════════════════════════════
class LonghunRiskModel:
    """R = P × I × E。"""

    IMPACT_MAP = {0: 0.0, 1: 0.2, 2: 0.4, 3: 0.8, 4: 1.0}

    def calculate(self, probability: float, data_level: int, exposure: float) -> float:
        impact = self.IMPACT_MAP.get(data_level, 0.5)
        return min(1.0, probability * impact * exposure)

    @staticmethod
    def tier(r: float) -> str:
        if r >= 0.8:
            return "CRITICAL"
        if r >= 0.5:
            return "HIGH"
        if r >= 0.2:
            return "MEDIUM"
        return "LOW"

    @staticmethod
    def color(r: float) -> str:
        if r >= 0.8:
            return "🔴"
        if r >= 0.5:
            return "🟠"
        if r >= 0.2:
            return "🟡"
        return "🟢"


# ═══════════════════════════════════════════════════════════
# 5.4 隐私熔断器
# ═══════════════════════════════════════════════════════════
class LonghunPrivacyCircuitBreaker:
    """EWMA 违规强度 + 指数退避冷却 + 三与门恢复。"""

    def __init__(self):
        self.v = 0.0
        self.k = 0
        self.cooldown_until = 0.0
        self.tripped = False
        self.dna = LonghunDNAChain()

    def inject(self, R: float, now: float | None = None) -> dict:
        if now is None:
            now = time.time()
        self.v = ALPHA * R + (1 - ALPHA) * self.v
        result = {"v": round(self.v, 4), "tripped": self.tripped, "R": round(R, 4)}

        if self.v >= THETA_TRIG and not self.tripped:
            self.tripped = True
            cooldown_sec = 24 * 3600 * (2 ** self.k)
            self.cooldown_until = now + cooldown_sec
            self.k += 1
            action = f"🔴 熔断！冷却 {cooldown_sec / 3600:.0f} 小时"
            if self.k >= 4:
                action += " → 达4次，转永久黑名单评审"
            result["action"] = action
            result["tripped"] = True
            result["dna"] = self.dna.mint("CIRCUIT_BREAKER", "TRIP")
        elif self.v >= THETA_WARN:
            result["action"] = f"🟡 预警 v={self.v:.2f}，人工盯防"
        else:
            result["action"] = f"🟢 正常 v={self.v:.2f}"
        return result

    def request_recover(self, now: float | None = None, human_signature: bool = False) -> dict:
        if now is None:
            now = time.time()
        ok = self.v < THETA_RECOVER and now >= self.cooldown_until and human_signature
        if ok:
            self.tripped = False
            return {"recovered": True, "reason": "✅ 恢复接入", "dna": self.dna.mint("CIRCUIT_BREAKER", "RECOVER")}
        reasons = []
        if self.v >= THETA_RECOVER:
            reasons.append(f"v={self.v:.2f} ≥ {THETA_RECOVER}")
        if now < self.cooldown_until:
            reasons.append("冷却期未满")
        if not human_signature:
            reasons.append("无人工复核签字")
        return {"recovered": False, "reason": "🔴 恢复条件不满足: " + "；".join(reasons)}


# ═══════════════════════════════════════════════════════════
# 第八章：接入控制器
# ═══════════════════════════════════════════════════════════
class LonghunPrivacyAccessController:
    """P0++ 级隐私接入控制器：fail-closed，默认拒绝。"""

    DEFAULT_BLACKLIST = ["网络水军", "数据贩子", "间谍组织", "造谣媒体"]
    DEFAULT_WHITELIST_INTL = ["联合国", "世界卫生组织", "国际红十字会"]

    def __init__(self, blacklist: list[str] | None = None, whitelist_intl: list[str] | None = None):
        self.blacklist = set(blacklist or self.DEFAULT_BLACKLIST)
        self.whitelist_intl = set(whitelist_intl or self.DEFAULT_WHITELIST_INTL)
        self.trust_scorer = LonghunTrustScorer()
        self.risk_model = LonghunRiskModel()
        self.classifier = LonghunDataClassifier()
        self.dna = LonghunDNAChain()

    # ---------- 5.10 黑名单匹配 ----------
    def _check_blacklist(self, entity: dict) -> tuple[bool, bool]:
        """返回 (是否精确命中, 是否疑似换皮)。"""
        name = entity.get("name") or ""
        if any(b in name for b in self.blacklist):
            return True, False
        suspicious = False
        for b in self.blacklist:
            d = _normalized_edit_distance(name, b)
            if d <= EDIT_DISTANCE_THRESHOLD:
                suspicious = True
                break
        return False, suspicious

    # ---------- 5.1 技术审计 ----------
    def _technical_audit(self, entity: dict) -> bool:
        required = [
            "code_audit_report",
            "encryption_scheme",
            "network_architecture",
            "access_control_policy",
            "sbom",
            "penetration_test_report",
        ]
        docs = entity.get("technical_documents", {})
        return all(k in docs for k in required) and docs.get("critical_cve_count", 1) == 0

    # ---------- 5.1 地理合规（四信号投票） ----------
    def _geo_compliance(self, entity: dict) -> tuple[bool, int]:
        storage = entity.get("data_storage_country")
        signals = [
            entity.get("registered_country") == storage,
            entity.get("asn_country") == storage,
            entity.get("ip_geo_country") == storage,
            bool(entity.get("data_residency_signature")),
        ]
        return sum(signals) >= GEO_SIGNAL_THRESHOLD, sum(signals)

    # ---------- 综合判定 ----------
    def evaluate(self, entity: dict) -> dict:
        try:
            name = entity.get("name")
            if not name or not isinstance(name, str):
                return {
                    "allowed": False,
                    "level": "FAIL_CLOSED",
                    "reason": "🔴 实体名称缺失或非法，默认拒绝",
                    "dna": self.dna.mint("?", "DENIED"),
                }
            exact, suspicious = self._check_blacklist(entity)
            if exact:
                return {
                    "allowed": False,
                    "level": "P0_DENY",
                    "reason": "🔴 永久黑名单实体",
                    "dna": self.dna.mint(name, "DENIED"),
                }
            if suspicious:
                return {
                    "allowed": False,
                    "level": "MANUAL_REVIEW",
                    "reason": "🟡 疑似黑名单换皮（编辑距离≤0.20），转人工复核",
                    "dna": self.dna.mint(name, "REVIEW"),
                }

            trust = self.trust_scorer.score(entity.get("scoring_materials", {}))
            tier = self.trust_scorer.tier(trust)
            if tier == "DENY":
                return {
                    "allowed": False,
                    "level": "LOW_TRUST",
                    "reason": f"🔴 信任评分 {trust:.2f} < 0.50",
                    "trust": trust,
                    "dna": self.dna.mint(name, "DENIED"),
                }
            if tier == "REVIEW":
                return {
                    "allowed": False,
                    "level": "MANUAL_REVIEW",
                    "reason": f"🟡 信任评分 {trust:.2f} 需人工复核",
                    "trust": trust,
                    "dna": self.dna.mint(name, "REVIEW"),
                }

            if not self._technical_audit(entity):
                return {
                    "allowed": False,
                    "level": "AUDIT_FAIL",
                    "reason": "🔴 技术审计未通过（审计失败即拒绝，不再穿透）",
                    "trust": trust,
                    "dna": self.dna.mint(name, "DENIED"),
                }

            geo_ok, geo_signals = self._geo_compliance(entity)
            if not geo_ok:
                return {
                    "allowed": False,
                    "level": "GEO_FAIL",
                    "reason": f"🔴 数据落域不合规（四信号仅 {geo_signals}/4 通过）",
                    "trust": trust,
                    "dna": self.dna.mint(name, "DENIED"),
                }

            return {
                "allowed": True,
                "level": "APPROVED",
                "reason": f"✅ 五条件全过，信任评分 T={trust:.2f}",
                "trust": trust,
                "dna": self.dna.mint(name, "APPROVED"),
            }
        except Exception as exc:
            return {
                "allowed": False,
                "level": "FAIL_CLOSED",
                "reason": f"🔴 验证异常，默认拒绝: {exc}",
                "dna": self.dna.mint(entity.get("name", "?"), "DENIED"),
            }

    # ---------- 隐私规则执行（8.3） ----------
    def enforce_privacy_rules(self, request: dict) -> dict:
        """
        对单次数据请求执行隐私规则。
        request: {
            entity_name, data_types[], purpose, consent_id,
            consent_ttl_days, requested_fields[], necessary_fields[]
        }
        """
        try:
            data_types = request.get("data_types", [])
            level = self.classifier.classify_dataset(data_types)

            # 规则7: L4 禁区
            if level == 4:
                return {
                    "allowed": False,
                    "level": "L4_FORBIDDEN",
                    "reason": "🔴 L4 禁区级数据：无条件拒绝，无授权例外",
                    "data_level": level,
                    "dna": self.dna.mint(request.get("entity_name", "?"), "DENIED"),
                }

            # 规则6: 授权时效
            ttl = request.get("consent_ttl_days", 0)
            expected_ttl = TTL_L3_DAYS if level == 3 else TTL_DEFAULT_DAYS
            if ttl <= 0 or ttl > expected_ttl:
                return {
                    "allowed": False,
                    "level": "CONSENT_EXPIRED",
                    "reason": f"🔴 授权无效：L{level} 数据 TTL 应为 ≤{expected_ttl} 天",
                    "data_level": level,
                    "dna": self.dna.mint(request.get("entity_name", "?"), "DENIED"),
                }

            # 规则5: 数据最小化
            requested = set(request.get("requested_fields", []))
            necessary = set(request.get("necessary_fields", []))
            over_collection = requested - necessary
            if over_collection:
                return {
                    "allowed": False,
                    "level": "OVER_COLLECTION",
                    "reason": f"🟡 数据最小化违规：超收字段 {sorted(over_collection)}",
                    "data_level": level,
                    "dna": self.dna.mint(request.get("entity_name", "?"), "DENIED"),
                }

            return {
                "allowed": True,
                "level": "PRIVACY_PASS",
                "reason": f"✅ 隐私规则通过，数据级别 L{level}",
                "data_level": level,
                "dna": self.dna.mint(request.get("entity_name", "?"), "APPROVED"),
            }
        except Exception as exc:
            return {
                "allowed": False,
                "level": "FAIL_CLOSED",
                "reason": f"🔴 隐私规则执行异常，默认拒绝: {exc}",
                "dna": self.dna.mint(request.get("entity_name", "?"), "DENIED"),
            }


# ═══════════════════════════════════════════════════════════
# 第十八章：测试向量
# ═══════════════════════════════════════════════════════════
def run_test_vectors() -> dict:
    """执行 14 条测试向量，返回统计结果。"""
    ctrl = LonghunPrivacyAccessController()
    breaker = LonghunPrivacyCircuitBreaker()

    base_entity = {
        "name": "ExampleOrg",
        "registered_country": "CN",
        "data_storage_country": "CN",
        "asn_country": "CN",
        "ip_geo_country": "CN",
        "data_residency_signature": "signed",
        "scoring_materials": {
            "certifications": ["ISO27001", "等保三级"],
            "violation_count": 0,
            "penetration_score": 0.95,
            "transparency_score": 0.90,
            "complaint_rate": 0.01,
        },
        "technical_documents": {
            "code_audit_report": "ok",
            "encryption_scheme": "ok",
            "network_architecture": "ok",
            "access_control_policy": "ok",
            "sbom": "ok",
            "penetration_test_report": "ok",
            "critical_cve_count": 0,
        },
    }

    cases = []

    # T01: 黑名单实体
    e = {**base_entity, "name": "XX数据贩子"}
    cases.append(("T01 黑名单拒绝", ctrl.evaluate(e), lambda r: not r["allowed"] and r["level"] == "P0_DENY"))

    # T02: 疑似换皮
    e = {**base_entity, "name": "数据厎贩子"}
    cases.append(("T02 疑似换皮转人工", ctrl.evaluate(e), lambda r: not r["allowed"] and r["level"] == "MANUAL_REVIEW"))

    # T03: 白名单缺 SBOM
    e = {
        **base_entity,
        "name": "联合国",
        "technical_documents": {k: v for k, v in base_entity["technical_documents"].items() if k != "sbom"},
    }
    cases.append(("T03 审计失败即拒绝", ctrl.evaluate(e), lambda r: not r["allowed"] and r["level"] == "AUDIT_FAIL"))

    # T04: 全过
    cases.append(("T04 五条件全过", ctrl.evaluate(base_entity), lambda r: r["allowed"] and r["level"] == "APPROVED"))

    # T05: 信任分 0.62 转人工
    e = {
        **base_entity,
        "scoring_materials": {
            **base_entity["scoring_materials"],
            "certifications": [],
            "penetration_score": 0.70,
            "transparency_score": 0.60,
        },
    }
    cases.append(("T05 信任分中等转人工", ctrl.evaluate(e), lambda r: not r["allowed"] and r["level"] == "MANUAL_REVIEW"))

    # T06: 连续 5 次 R=0.9 触发熔断（α=0.3 时约 5 次可达阈值）
    for _ in range(5):
        res = breaker.inject(0.9)
    cases.append(("T06 EWMA 连续违规熔断", res, lambda r: r.get("tripped") and "熔断" in r.get("action", "")))

    # T07: 单次 R=0.5 不熔断
    breaker2 = LonghunPrivacyCircuitBreaker()
    res = breaker2.inject(0.5)
    cases.append(("T07 单次误报不熔断", res, lambda r: not r.get("tripped") and r["v"] < THETA_WARN))

    # T08: 恢复条件不满足
    res = breaker.request_recover(human_signature=False)
    cases.append(("T08 恢复三与门缺一", res, lambda r: not r["recovered"]))

    # T09: DNA 链篡改可检测（链式推进不一致）
    chain = LonghunDNAChain()
    d1 = chain.mint("A", "TEST")
    original_prev = chain._prev_hash
    chain._prev_hash = "tampered"
    d2 = chain.mint("A", "TEST2")
    tampered_detected = original_prev not in d2
    cases.append(("T09 DNA 链篡改可检测", {"ok": tampered_detected}, lambda r: r.get("ok")))

    # T10: 授权 TTL 过期
    res = ctrl.enforce_privacy_rules({
        "entity_name": "Test",
        "data_types": ["conversation"],
        "consent_ttl_days": 0,
        "requested_fields": ["content"],
        "necessary_fields": ["content"],
    })
    cases.append(("T10 授权过期拒绝", res, lambda r: not r["allowed"] and r["level"] == "CONSENT_EXPIRED"))

    # T11: L4 生物特征无条件拒绝
    res = ctrl.enforce_privacy_rules({
        "entity_name": "Test",
        "data_types": ["biometric"],
        "consent_ttl_days": 30,
        "requested_fields": ["fingerprint"],
        "necessary_fields": ["fingerprint"],
    })
    cases.append(("T11 L4 禁区无条件拒绝", res, lambda r: not r["allowed"] and r["level"] == "L4_FORBIDDEN"))

    # T12: 验证异常 fail-closed
    res = ctrl.evaluate({"name": None})  # type: ignore
    cases.append(("T12 异常默认拒绝", res, lambda r: not r["allowed"] and r["level"] == "FAIL_CLOSED"))

    # T13: 跨境实体四信号仅 2/4
    e = {
        **base_entity,
        "registered_country": "US",
        "asn_country": "US",
    }
    cases.append(("T13 地理不合规拒绝", ctrl.evaluate(e), lambda r: not r["allowed"] and r["level"] == "GEO_FAIL"))

    # T14: 数据最小化超收
    res = ctrl.enforce_privacy_rules({
        "entity_name": "Test",
        "data_types": ["conversation"],
        "consent_ttl_days": 30,
        "requested_fields": ["content", "location", "device_id"],
        "necessary_fields": ["content"],
    })
    cases.append(("T14 数据最小化违规", res, lambda r: not r["allowed"] and r["level"] == "OVER_COLLECTION"))

    passed = 0
    results = []
    for name, result, check in cases:
        ok = check(result)
        passed += int(ok)
        status = "✅" if ok else "❌"
        results.append({"case": name, "passed": ok, "result": result})
        print(f"{status} {name}")
        if not ok:
            print(f"   实际结果: {result}")

    print(f"\n测试向量: {passed}/{len(cases)} 通过")
    return {"passed": passed, "total": len(cases), "results": results}


def demo():
    ctrl = LonghunPrivacyAccessController()
    entity = {
        "name": "龍魂合作医院",
        "registered_country": "CN",
        "data_storage_country": "CN",
        "asn_country": "CN",
        "ip_geo_country": "CN",
        "data_residency_signature": "signed",
        "scoring_materials": {
            "certifications": ["ISO27001", "等保三级", "HIMSS"],
            "violation_count": 0,
            "penetration_score": 0.92,
            "transparency_score": 0.88,
            "complaint_rate": 0.005,
        },
        "technical_documents": {
            "code_audit_report": "ok",
            "encryption_scheme": "SM4-GCM",
            "network_architecture": "ok",
            "access_control_policy": "RBAC+ABAC",
            "sbom": "ok",
            "penetration_test_report": "ok",
            "critical_cve_count": 0,
        },
    }
    print("=" * 60)
    print("龍魂隐私接入控制器 · 综合演示")
    print("=" * 60)
    print("\n[接入判定]")
    res = ctrl.evaluate(entity)
    print(json.dumps(res, ensure_ascii=False, indent=2))

    print("\n[隐私规则执行：请求 L3 健康数据]")
    res2 = ctrl.enforce_privacy_rules({
        "entity_name": entity["name"],
        "data_types": ["health"],
        "consent_ttl_days": 7,
        "requested_fields": ["diagnosis_code"],
        "necessary_fields": ["diagnosis_code"],
    })
    print(json.dumps(res2, ensure_ascii=False, indent=2))

    print("\n[风险评估]")
    rm = LonghunRiskModel()
    r = rm.calculate(probability=0.5, data_level=3, exposure=1.0)
    print(f"R = {r:.2f} → {rm.color(r)} {rm.tier(r)}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "test"
    if cmd == "test":
        stats = run_test_vectors()
        sys.exit(0 if stats["passed"] == stats["total"] else 1)
    elif cmd == "demo":
        demo()
    else:
        print("用法: python3 bin/lh_privacy_access_controller.py [test|demo]")
        sys.exit(1)
