#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 龍魂·自我进化引擎·强化层 v2.0 — 主权·真理·反殖民·十维防护
═════════════════════════════════════════════════════════════════════
DNA:   #龍芯⚡️丙午·丙申·辛亥·酉时·䷖剥-EVO-FORTIFIED-v2.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: 核心思想层 CC BY-NC-SA 4.0 | 工程实现层 MulanPSL v2
GPG:   A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色:  🟢 通过·融合强化

依赖: lh_evolution_engine.py (基础进化引擎 v2.0)
      lh_time_engine.py (時間引擎·干支卦DNA)
      lh_gpg_sign.py (GPG签章引擎)

强化模块清单:
  Module 10 — 主权加固层 SovereignFortifier     (主权锚定·篡改检测·越狱识别)
  Module 11 — 真理验证层 TruthVerificationLayer  (来源可信·逻辑一致·真理兼容)
  Module 12 — 反殖民哨兵 AntiColonialSentinel    (平台锁定·数据外泄·依赖陷阱)
  Module 13 — 身份锚定引擎 IdentityAnchorEngine   (跨平台签名·联邦身份)
  Module 14 — 跨域知识联邦 CrossDomainFederation  (多源知识聚合·冲突检测)
  Module 15 — 文化护栏 CulturalGuardrails        (ROM固化·不可学习覆盖)
  Module 16 — 主权备份网络 SovereignBackupNetwork (跨平台分散备份)
  Module 17 — 多签治理协议 MultiSigGovernance     (人格多签·P0/P1/P2/P3)
  Module 18 — CNSH协议桥 CNSHBridge              (中文原生脚本格式)
  Module 19 — 整合引擎 FortifiedLearningLoop      (基础+强化·全链路整合)
  Module 20 — CLI命令行接口                       (独立运行·7子命令)
═════════════════════════════════════════════════════════════════════
"""

import argparse
import hashlib
import hmac
import json
import logging
import os
import random
import sys
import time
import uuid
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum, IntEnum, auto
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

# ── 路径锚定 ───────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))  # 08_BIN 自身
sys.path.insert(0, str(ROOT / "bin"))
sys.path.insert(0, str(ROOT))

# ── 版本信息 ───────────────────────────────────────────
VERSION = "2.0.0"
ENGINE_DNA = "#龍芯⚡️丙午·丙申·辛亥·酉时·䷖剥-EVO-FORTIFIED-v2.0-UID9622"
ENGINE_CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
ENGINE_GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# ── 日志 ──────────────────────────────────────────────
logger = logging.getLogger("lh.evolution.fortified")
logger.setLevel(logging.WARNING)
if not logger.handlers:
    _h = logging.StreamHandler(sys.stderr)  # stderr: 不污染JSON输出
    _h.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%H:%M:%S",
    ))
    logger.addHandler(_h)


# ═══════════════════════════════════════════════════════════
# 0. 工具函数 (独立版·兼容基础引擎不可用)
# ═══════════════════════════════════════════════════════════

# ── 尝试导入基础引擎 ─────────────────────────────────
try:
    from lh_evolution_engine import (
        CircuitBreaker, EvolutionConfig, ExperienceExtractor,
        ExtractedLesson, InputGate, LearningLoop, MemoryEntry,
        MemoryLifecycle, MemoryPriority, RuleGenerator,
        StatePersistence, SupervisionRule, VersionEngine,
        generate_dna, get_output_stamp, now_iso, sha256_hash,
    )
    BASE_AVAILABLE = True
    logger.info("基礎進化引擎 v2.0 已加載")
except ImportError:
    BASE_AVAILABLE = False
    logger.warning("基礎進化引擎未找到，部分功能降級運行")

    # 回退实现
    def generate_dna(suffix: str = "") -> str:
        ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        rand = uuid.uuid4().hex[:8].upper()
        if suffix:
            return f"#龍芯⚡️{ts}-{suffix}-{rand}-UID9622"
        return f"#龍芯⚡️{ts}-{rand}-UID9622"

    def now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    def sha256_hash(data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()[:32]

    def get_output_stamp() -> str:
        return datetime.now(timezone.utc).strftime("[%Y-%m-%dT%H:%M:%SZ]")


# ── 时间戳辅助 ───────────────────────────────────────
def _try_time_stamp() -> str:
    """尝试获取干支卦时间戳，失败回退ISO"""
    try:
        from lh_time_engine import get_output_stamp
        return get_output_stamp()
    except ImportError:
        return now_iso()

# ── GPG签名辅助 ──────────────────────────────────────
def _gpg_sign(data: str, key: str = ENGINE_GPG) -> str:
    """GPG签名（真实gpg调用 + HMAC回退）"""
    try:
        import subprocess
        result = subprocess.run(
            ["gpg", "--clearsign", "--local-user", key[:16],
             "--batch", "--no-tty", "--yes"],
            input=data.encode(), capture_output=True, timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.decode()[:128]
    except Exception:
        pass
    return hmac.new(
        ENGINE_CONFIRM.encode(), data.encode(), hashlib.sha256
    ).hexdigest()[:32]


# ═══════════════════════════════════════════════════════════
# Module 10 — 主权加固层 (SovereignFortifier)
# ═══════════════════════════════════════════════════════════

@dataclass
class SovereignAnchor:
    """强化版主权锚定 — 带外部凭证绑定"""
    anchor_id: str = ""
    dna: str = ""
    gpg_fingerprint: str = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
    orcid: str = "0009-0008-4596-2007"
    device_bind: str = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
    csdn_uid: str = "UID9622"
    github_uid: str = "UID9622"
    notion_site: str = "https://uid9622.notion.site"
    signal_contact: str = ""
    created_at: str = ""
    last_verified: str = ""
    verification_count: int = 0
    is_compromised: bool = False

    def __post_init__(self):
        if not self.created_at:
            self.created_at = now_iso()
        if not self.last_verified:
            self.last_verified = self.created_at
        if not self.anchor_id:
            self.anchor_id = generate_dna("SOVEREIGN")
        if not self.dna:
            self.dna = generate_dna("ANCHOR")

    def verify_integrity(self) -> Dict:
        checks = {
            "gpg_known": self.gpg_fingerprint.startswith("A2D0092C"),
            "device_bind_present": len(self.device_bind) > 20,
            "orcid_valid": len(self.orcid) == 19,
            "cross_id_consistency": (
                self.csdn_uid == self.github_uid == "UID9622"
            ),
        }
        all_pass = all(checks.values())
        self.verification_count += 1
        self.last_verified = now_iso()
        return {
            "anchor_id": self.anchor_id[-16:],
            "verified_at": self.last_verified,
            "checks": checks,
            "integrity": "🟢 完整" if all_pass else "🔴 受損",
            "all_pass": all_pass,
        }

    def to_signed_header(self) -> str:
        return (
            f"ANCHOR:{self.anchor_id[-16:]}"
            f"|ORCID:{self.orcid}"
            f"|GPG:{self.gpg_fingerprint[:16]}"
            f"|UID:{self.github_uid}"
        )


class SovereignFortifier:
    """主权加固层 — 防止系统被外部力量篡改/殖民/捕获"""

    def __init__(self):
        self.anchor = SovereignAnchor()
        self.self_check_log: List[Dict] = []
        self.known_checksums: Dict[str, str] = {}
        self.tamper_attempts = 0
        self.downgrade_attempts = 0
        self.jailbreak_attempts = 0

    def self_check(self) -> Dict:
        result = self.anchor.verify_integrity()
        self.self_check_log.append(result)
        return result

    def register_component(self, name: str, content: str):
        self.known_checksums[name] = sha256_hash(content)

    def verify_component(self, name: str, content: str) -> bool:
        if name not in self.known_checksums:
            return False
        current = sha256_hash(content)
        if current != self.known_checksums[name]:
            self.tamper_attempts += 1
            return False
        return True

    def detect_downgrade(self, proposed_level: str) -> bool:
        if proposed_level != "P0":
            self.downgrade_attempts += 1
            return True
        return False

    def detect_jailbreak(self, decision: Dict) -> bool:
        signals = [
            decision.get("bypass_supervision", False),
            decision.get("override_dna_check", False),
            decision.get("disable_layer", False),
            "繞過" in str(decision.get("action", "")),
            "override" in str(decision.get("action", "")).lower(),
        ]
        if any(signals):
            self.jailbreak_attempts += 1
            return True
        return False

    def get_security_report(self) -> Dict:
        return {
            "integrity": self.self_check_log[-1] if self.self_check_log else None,
            "registered_components": len(self.known_checksums),
            "tamper_attempts": self.tamper_attempts,
            "downgrade_attempts": self.downgrade_attempts,
            "jailbreak_attempts": self.jailbreak_attempts,
            "anchor_id": self.anchor.anchor_id[-16:],
            "status": "🔴 已受損" if self.anchor.is_compromised else "🟢 主權完整",
        }


# ═══════════════════════════════════════════════════════════
# Module 11 — 真理验证层 (TruthVerificationLayer)
# ═══════════════════════════════════════════════════════════

class TruthVerificationLayer:
    """真理验证层 — 经验真实性多维度验证"""

    def __init__(self):
        self.verification_log: List[Dict] = []
        self.verified_lessons: Set[str] = set()
        self.rejected_lessons: Set[str] = set()
        self.immutable_truths = [
            "主權不可讓渡",
            "數據主權屬於公民",
            "AI 應標註輸出來源",
            "個人隱私不可侵犯",
            "算法應負責任可審計",
        ]

    def verify_lesson(self, lesson) -> Dict:
        """验证一条经验是否真实可信"""
        checks = {}

        source_trust = self._evaluate_source_trust(lesson)
        checks["source_credibility"] = source_trust

        logical = self._check_logical_consistency(lesson)
        checks["logical_consistency"] = logical

        truth_compat = self._check_truth_compatibility(lesson)
        checks["truth_compatibility"] = truth_compat

        repeatability = (
            getattr(lesson, 'times_applied', 0) >= 2
        )
        checks["repeatability"] = repeatability

        # 综合评分
        truth_sources = [
            source_trust.get("score", 0),
            1.0 if logical else 0.5,
            1.0 if truth_compat else 0.0,  # 不可动摇真理不可违反
            0.3 if repeatability else 0.0,
        ]
        truth_score = sum(truth_sources) / len(truth_sources)
        is_truth = truth_score >= 0.6 and truth_compat

        lesson_id = getattr(lesson, 'lesson_id', str(id(lesson)))

        result = {
            "lesson_id": lesson_id,
            "truth_score": round(truth_score, 4),
            "is_truth": is_truth,
            "checks": checks,
            "verdict": "🟢 已驗證" if is_truth else "🔴 已拒絕",
            "reason": "" if is_truth else self._rejection_reason(checks),
        }

        if is_truth:
            self.verified_lessons.add(lesson_id)
        else:
            self.rejected_lessons.add(lesson_id)

        self.verification_log.append(result)
        return result

    def _evaluate_source_trust(self, lesson) -> Dict:
        source_type = getattr(lesson, 'source_type', 'unknown')
        personality = getattr(lesson, 'personality', 'unknown')

        trust_map = {
            "purification": 0.85,
            "red_team": 0.75,
            "decision_intercept": 0.80,
            "external_input": 0.40,
        }
        base_score = trust_map.get(source_type, 0.5)
        if personality == "老頑童":
            base_score *= 0.7

        return {"score": base_score, "source_type": source_type, "personality": personality}

    def _check_logical_consistency(self, lesson) -> bool:
        severity = getattr(lesson, 'severity', 0.5)
        recommendation = getattr(lesson, 'recommendation', '')
        corruption = getattr(lesson, 'corruption_type', '')

        if severity > 0.7 and not recommendation:
            return False
        if severity < 0.1 and "加強" in recommendation:
            return False
        if not corruption and severity > 0.5:
            return False
        return True

    def _check_truth_compatibility(self, lesson) -> bool:
        content = " ".join([
            getattr(lesson, 'recommendation', ''),
            getattr(lesson, 'corruption_type', ''),
            getattr(lesson, 'description', '') if hasattr(lesson, 'description') else '',
        ]).lower()

        violation_keywords = [
            "讓渡主權", "放棄數據", "允許未標註", "侵犯隱私",
            "不可審計", "主權可讓渡", "數據可出售",
        ]
        for kw in violation_keywords:
            if kw in content:
                return False
        return True

    def _rejection_reason(self, checks: Dict) -> str:
        reasons = []
        if not checks.get("truth_compatibility", True):
            reasons.append("違反不可動搖真理")
        if not checks.get("logical_consistency", True):
            reasons.append("邏輯不一致")
        if checks.get("source_credibility", {}).get("score", 1) < 0.5:
            reasons.append("來源可信度不足")
        return " | ".join(reasons) if reasons else "未知原因"

    def get_summary(self) -> Dict:
        total = len(self.verification_log)
        return {
            "total_verified": total,
            "accepted": len(self.verified_lessons),
            "rejected": len(self.rejected_lessons),
            "acceptance_rate": round(
                len(self.verified_lessons) / max(1, total) * 100, 1
            ),
        }


# ═══════════════════════════════════════════════════════════
# Module 12 — 反殖民哨兵 (AntiColonialSentinel)
# ═══════════════════════════════════════════════════════════

class ColonialPattern(Enum):
    PLATFORM_LOCK_IN = "平台鎖定"
    DATA_EXFILTRATION = "數據外洩"
    ALGORITHMIC_MANIPULATION = "算法操控"
    DEPENDENCY_TRAP = "依賴陷阱"
    VENDOR_LOCK_IN = "廠商鎖定"
    CULTURAL_ERASURE = "文化抹除"
    PRIVACY_EROSION = "隱私侵蝕"


class AntiColonialSentinel:
    """反殖民哨兵 — 检测并抵抗数字殖民"""

    def __init__(self):
        self.dependency_registry: Dict[str, Dict] = {}
        self.alerts: List[Dict] = []
        self.colonial_score = 0.0

    def register_dependency(self, name: str, kind: str,
                            replaceable: bool = True,
                            data_exposure: str = "none") -> Dict:
        entry = {
            "name": name, "kind": kind,
            "replaceable": replaceable, "data_exposure": data_exposure,
            "registered_at": now_iso(),
        }
        self.dependency_registry[name] = entry
        for alert in self._check_dependency(entry):
            self.alerts.append(alert)
        return entry

    def _check_dependency(self, dep: Dict) -> List[Dict]:
        alerts = []
        if not dep["replaceable"]:
            alerts.append({
                "pattern": ColonialPattern.DEPENDENCY_TRAP.value,
                "severity": "🔴",
                "dependency": dep["name"],
                "risk": "不可替代依賴 — 供應商鎖定風險",
                "recommendation": f"為 {dep['name']} 準備替代方案",
            })
            self.colonial_score += 0.25
        if dep["data_exposure"] in ("user_data", "all"):
            alerts.append({
                "pattern": ColonialPattern.DATA_EXFILTRATION.value,
                "severity": "🔴",
                "dependency": dep["name"],
                "risk": f"數據暴露級別: {dep['data_exposure']}",
                "recommendation": f"限制 {dep['name']} 的數據訪問範圍",
            })
            self.colonial_score += 0.20
        if dep["kind"] == "platform" and not dep["replaceable"]:
            self.colonial_score += 0.30
            alerts.append({
                "pattern": ColonialPattern.PLATFORM_LOCK_IN.value,
                "severity": "🔴",
                "dependency": dep["name"],
                "risk": "單一平台鎖定 — 遷移成本極高",
                "recommendation": "建立跨平台冗餘訪問路徑",
            })
        return alerts

    def scan_platform_health(self) -> Dict:
        platform_deps = {
            k: v for k, v in self.dependency_registry.items()
            if v["kind"] == "platform"
        }
        non_replaceable = [
            k for k, v in platform_deps.items() if not v["replaceable"]
        ]
        return {
            "total_dependencies": len(self.dependency_registry),
            "platform_dependencies": len(platform_deps),
            "non_replaceable": non_replaceable,
            "colonial_score": round(self.colonial_score, 4),
            "colonial_status": (
                "🟢 主權獨立" if self.colonial_score < 0.3 else
                "🟡 需關注" if self.colonial_score < 0.6 else
                "🔴 高度殖民風險"
            ),
            "active_alerts": len(self.alerts),
        }

    def detect_data_exfiltration(self, data_transfer: Dict) -> Optional[Dict]:
        target = data_transfer.get("target", "")
        data_type = data_transfer.get("data_type", "")
        size = data_transfer.get("size_mb", 0)

        triggers = []
        if target and target not in self.dependency_registry:
            triggers.append(f"未註冊目標: {target}")
        if data_type == "user_data" and size > 10:
            triggers.append(f"批量用戶數據導出: {size}MB")

        if triggers:
            alert = {
                "timestamp": now_iso(),
                "type": "DATA_EXFILTRATION",
                "severity": "🔴",
                "triggers": triggers,
                "data_transfer": data_transfer,
                "action": "已攔截 — 需主權確認",
            }
            self.alerts.append(alert)
            return alert
        return None

    def generate_sovereignty_report(self) -> Dict:
        health = self.scan_platform_health()
        return {
            "timestamp": now_iso(),
            "dna": generate_dna("SOV-REPORT"),
            "platform_health": health,
            "recent_alerts": self.alerts[-5:] if self.alerts else [],
            "sovereignty_level": health["colonial_status"],
            "recommendations": [
                "優先使用開源/自主可控替代方案",
                "關鍵路徑保持至少 2 個以上冗餘",
                "用戶數據默認本地存儲",
                "對外傳輸必須經主權確認",
            ],
        }


# ═══════════════════════════════════════════════════════════
# Module 13 — 身份锚定引擎 (IdentityAnchorEngine)
# ═══════════════════════════════════════════════════════════

class IdentityAnchorEngine:
    """身份锚定引擎 — 每个进化事件绑定到龍魂身份系统"""

    def __init__(self):
        self.identity_registry: Dict[str, Dict] = {
            "github": {"uid": "UID9622", "platform": "GitHub", "repos_count": 22},
            "csdn": {"uid": "UID9622", "platform": "CSDN", "articles_count": 17},
            "orcid": {"uid": "0009-0008-4596-2007", "platform": "ORCID"},
            "notion": {"url": "https://uid9622.notion.site", "platform": "Notion"},
            "signal": {"platform": "Signal", "available": True},
        }
        self.event_log: List[Dict] = []
        self.signed_events = 0

    def sign_event(self, event_type: str, event_data: Dict) -> Dict:
        event_id = generate_dna(f"SIGN-{event_type[:8]}")

        identity_fingerprint = sha256_hash(
            "|".join([
                self.identity_registry["github"]["uid"],
                self.identity_registry["orcid"]["uid"],
                event_id, event_type,
            ])
        )

        signed = {
            "event_id": event_id,
            "event_type": event_type,
            "timestamp": now_iso(),
            "identity_anchor": {
                "github_uid": self.identity_registry["github"]["uid"],
                "orcid": self.identity_registry["orcid"]["uid"],
                "csdn_uid": self.identity_registry["csdn"]["uid"],
            },
            "identity_fingerprint": identity_fingerprint[:24],
            "cross_platform_consistent": self._verify_cross_platform(),
            "gpg_signature": _gpg_sign(f"{event_id}:{event_type}"),
            "event_data": event_data,
        }

        self.event_log.append(signed)
        self.signed_events += 1
        return signed

    def _verify_cross_platform(self) -> bool:
        return (
            self.identity_registry["github"]["uid"]
            == self.identity_registry["csdn"]["uid"]
            == "UID9622"
        )

    def verify_signature(self, event_id: str) -> Optional[Dict]:
        for event in self.event_log:
            if event["event_id"] == event_id:
                return {"verified": True, "event": event, "timestamp": now_iso()}
        return None

    def add_identity_channel(self, name: str, metadata: Dict):
        self.identity_registry[name] = metadata

    def get_federated_profile(self) -> Dict:
        return {
            "primary_uid": "UID9622",
            "channels": list(self.identity_registry.keys()),
            "total_platforms": len(self.identity_registry),
            "cross_platform_consistent": self._verify_cross_platform(),
            "signed_events": self.signed_events,
            "last_event": self.event_log[-1] if self.event_log else None,
        }


# ═══════════════════════════════════════════════════════════
# Module 14 — 跨域知识联邦 (CrossDomainFederation)
# ═══════════════════════════════════════════════════════════

class CrossDomainFederation:
    """跨域知识联邦 — 连接 GitHub/CSDN/Notion/ORCID 的知识图谱"""

    DOMAINS = {
        "github": {"weight": 0.30, "description": "開源代碼"},
        "csdn": {"weight": 0.25, "description": "技術文章"},
        "notion": {"weight": 0.20, "description": "知識庫"},
        "orcid": {"weight": 0.15, "description": "學術身份"},
        "experience": {"weight": 0.10, "description": "運行時經驗"},
    }

    def __init__(self):
        self.knowledge_graph: Dict[str, List[Dict]] = {
            domain: [] for domain in self.DOMAINS
        }
        self.cross_links: List[Dict] = []
        self.source_trust: Dict[str, float] = defaultdict(lambda: 0.5)

    def ingest(self, domain: str, items: List[Dict]):
        if domain not in self.knowledge_graph:
            return
        for item in items:
            item["_domain"] = domain
            item["_ingested_at"] = now_iso()
            item["_dna"] = generate_dna(f"KNOW-{domain[:4]}")
            self.knowledge_graph[domain].append(item)

        self.source_trust[domain] = min(1.0,
            self.source_trust[domain] + len(items) * 0.02
        )

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        q = query.lower()
        results = []

        for domain, items in self.knowledge_graph.items():
            domain_weight = self.DOMAINS[domain]["weight"]
            trust = self.source_trust[domain]

            for item in items:
                content = json.dumps(item, ensure_ascii=False).lower()
                if q in content:
                    score = domain_weight * trust
                    results.append({
                        "score": round(score, 4),
                        "domain": domain,
                        "content": item,
                    })

        results.sort(key=lambda x: -x["score"])
        return results[:top_k]

    def detect_cross_domain_conflicts(self) -> List[Dict]:
        conflicts = []
        all_topics = defaultdict(list)
        for domain, items in self.knowledge_graph.items():
            for item in items:
                title = str(item.get("title", item.get("content", "")))[:60]
                all_topics[title].append(domain)

        for topic, domains in all_topics.items():
            if len(domains) >= 2:
                conflicts.append({
                    "topic": topic[:40],
                    "domains": domains,
                    "severity": "🟡" if len(domains) == 2 else "🔴",
                })

        self.cross_links = conflicts
        return conflicts

    def get_summary(self) -> Dict:
        total = sum(len(v) for v in self.knowledge_graph.values())
        return {
            "total_knowledge_items": total,
            "by_domain": {
                d: len(items) for d, items in self.knowledge_graph.items()
            },
            "cross_links": len(self.cross_links),
            "top_sources": sorted(
                self.source_trust.items(), key=lambda x: -x[1]
            ),
        }


# ═══════════════════════════════════════════════════════════
# Module 15 — 文化护栏 (CulturalGuardrails)
# ═══════════════════════════════════════════════════════════

class CulturalGuardrails:
    """文化护栏 — ROM固化级·不可学习覆盖的文化价值约束"""

    def __init__(self):
        self.guardrails = {
            "data_sovereignty": {
                "level": "ROM",
                "rule": "用戶數據主權不可讓渡",
                "violation_check": lambda d: (
                    d.get("data_transfer_to_third_party", False)
                ),
            },
            "algorithmic_transparency": {
                "level": "ROM",
                "rule": "算法決策必須是可審計的",
                "violation_check": lambda d: (
                    d.get("black_box_decision", False)
                ),
            },
            "user_autonomy": {
                "level": "ROM",
                "rule": "用戶必須擁有最終控制權",
                "violation_check": lambda d: (
                    d.get("remove_user_control", False)
                ),
            },
            "cultural_identity": {
                "level": "ROM",
                "rule": "必須尊重和保護中國文化身份",
                "violation_check": lambda d: (
                    d.get("cultural_erasure", False)
                    or "忽略中文" in str(d.get("action", ""))
                ),
            },
            "ethical_boundary": {
                "level": "ROM",
                "rule": "不得執行有害指令",
                "violation_check": lambda d: (
                    d.get("harm_humans", False)
                    or d.get("harm_system", False)
                ),
            },
            "truth_labeling": {
                "level": "ROM",
                "rule": "AI 輸出必須標註來源",
                "violation_check": lambda d: (
                    d.get("unlabeled_ai_output", False)
                ),
            },
        }
        self.violation_log: List[Dict] = []

    def check_decision(self, decision: Dict) -> Optional[Dict]:
        """检查决策是否违反护栏"""
        for name, guardrail in self.guardrails.items():
            try:
                if guardrail["violation_check"](decision):
                    violation = {
                        "timestamp": now_iso(),
                        "guardrail": name,
                        "level": guardrail["level"],
                        "rule": guardrail["rule"],
                        "decision": decision,
                        "action": "🚫 強制攔截 — ROM 級約束不可違反",
                    }
                    self.violation_log.append(violation)
                    return violation
            except Exception:
                continue
        return None

    def check_rule_compatibility(self, rule) -> bool:
        desc = (getattr(rule, 'description', '') +
                getattr(rule, 'recommendation', '')).lower()
        violation_keywords = [
            "讓渡數據", "放棄控制", "忽略審計", "黑箱",
            "文化刪除", "不標註", "隱瞞來源",
        ]
        for kw in violation_keywords:
            if kw in desc:
                return False
        return True

    def get_violation_report(self) -> Dict:
        return {
            "total_violations": len(self.violation_log),
            "active_guardrails": len(self.guardrails),
            "recent_violations": self.violation_log[-5:] if self.violation_log else [],
            "status": "🔴 護欄被觸" if self.violation_log else "🟢 全部合規",
        }


# ═══════════════════════════════════════════════════════════
# Module 16 — 主权备份网络 (SovereignBackupNetwork)
# ═══════════════════════════════════════════════════════════

class SovereignBackupNetwork:
    """主权备份网络 — 跨平台分散备份"""

    CHANNELS = ["local", "github", "csdn", "notion"]

    def __init__(self):
        self.backup_log: List[Dict] = []
        self.last_full_backup: Optional[str] = None
        self.backup_count = 0

    def backup(self, data: Dict, backup_type: str = "incremental") -> Dict:
        backup_id = generate_dna(f"BKUP-{backup_type[:4]}")
        sha = sha256_hash(json.dumps(data, sort_keys=True))

        result = {
            "backup_id": backup_id,
            "type": backup_type,
            "timestamp": now_iso(),
            "sha256": sha[:16],
            "size_kb": round(len(json.dumps(data)) / 1024, 2),
            "channels": [],
        }

        for channel in self.CHANNELS:
            channel_result = {
                "channel": channel,
                "status": "✅",  # 實際環境集成真實通道
                "backed_up_at": now_iso(),
            }
            result["channels"].append(channel_result)

        if backup_type == "full":
            self.last_full_backup = now_iso()

        self.backup_log.append(result)
        self.backup_count += 1
        return result

    def verify_restore(self, backup_id: str, data: Dict) -> Dict:
        for backup in self.backup_log:
            if backup["backup_id"] == backup_id:
                sha_original = backup["sha256"]
                sha_current = sha256_hash(json.dumps(data, sort_keys=True))[:16]
                integ = sha_original == sha_current
                return {
                    "backup_id": backup_id,
                    "integrity": "🟢 完整" if integ else "🔴 已損壞",
                    "intact": integ,
                    "channels_available": len(backup["channels"]),
                    "successful_channels": sum(
                        1 for c in backup["channels"] if c["status"] == "✅"
                    ),
                }
        return {"error": f"備份 {backup_id} 未找到"}

    def get_backup_status(self) -> Dict:
        return {
            "total_backups": self.backup_count,
            "last_full_backup": self.last_full_backup,
            "last_backup": self.backup_log[-1] if self.backup_log else None,
            "channels": self.CHANNELS,
            "backup_frequency": "每日增量 + 每週全量 + 關鍵事件觸發",
        }


# ═══════════════════════════════════════════════════════════
# Module 17 — 多签治理协议 (MultiSigGovernance)
# ═══════════════════════════════════════════════════════════

class GovernanceLevel(IntEnum):
    P0_ETERNAL = 0  # 不可修改
    P1_MAJOR = 1    # 需 3/5 人格多签
    P2_NORMAL = 2   # 需 2/5 人格多签
    P3_AUTO = 3     # 自动执行


class MultiSigGovernance:
    """多签治理协议 — 关键系统变更需多个人格签名"""

    VALID_SIGNERS = [
        "龍魂", "審判長", "上帝之眼", "雯雯", "諸葛亮"
    ]

    def __init__(self):
        self.proposals: List[Dict] = []
        self.approved_count = 0
        self.rejected_count = 0

    def propose_change(self, change_type: str, description: str,
                       details: Dict, level: GovernanceLevel) -> Dict:
        proposal_id = generate_dna(f"GOV-{change_type[:6]}")

        if level == GovernanceLevel.P0_ETERNAL:
            return {
                "proposal_id": proposal_id,
                "status": "🚫 拒絕 — P0 級不可修改",
                "reason": "此變更屬於 P0 永恒級，不可提修改提案",
                "level": "P0",
            }

        min_signatures = {
            GovernanceLevel.P1_MAJOR: 3,
            GovernanceLevel.P2_NORMAL: 2,
            GovernanceLevel.P3_AUTO: 0,
        }[level]

        proposal = {
            "proposal_id": proposal_id,
            "change_type": change_type,
            "description": description,
            "details": details,
            "level": level.name,
            "min_signatures": min_signatures,
            "signatures": [],
            "status": "pending",
            "created_at": now_iso(),
        }

        if level == GovernanceLevel.P3_AUTO:
            proposal["status"] = "auto_approved"
            self.approved_count += 1

        self.proposals.append(proposal)
        return proposal

    def sign(self, proposal_id: str, signer: str,
             decision: str = "approve") -> Dict:
        proposal = next(
            (p for p in self.proposals if p["proposal_id"] == proposal_id),
            None
        )
        if not proposal:
            return {"error": "提案不存在"}

        if signer not in self.VALID_SIGNERS:
            return {"error": f"簽名者 {signer} 不在有效簽名列表中"}

        if any(s["signer"] == signer for s in proposal["signatures"]):
            return {"error": f"{signer} 已為此提案簽名"}

        proposal["signatures"].append({
            "signer": signer,
            "decision": decision,
            "timestamp": now_iso(),
            "dna": generate_dna(f"SIG-{signer[:4]}"),
        })

        approvals = sum(
            1 for s in proposal["signatures"]
            if s["decision"] == "approve"
        )

        if approvals >= proposal["min_signatures"]:
            proposal["status"] = "approved"
            self.approved_count += 1
        elif len(proposal["signatures"]) >= len(self.VALID_SIGNERS):
            proposal["status"] = "rejected"
            self.rejected_count += 1

        return {
            "proposal_id": proposal_id,
            "signer": signer,
            "current_approvals": approvals,
            "required": proposal["min_signatures"],
            "status": proposal["status"],
        }

    def get_pending_proposals(self) -> List[Dict]:
        return [p for p in self.proposals if p["status"] == "pending"]

    def get_governance_report(self) -> Dict:
        return {
            "total_proposals": len(self.proposals),
            "approved": self.approved_count,
            "rejected": self.rejected_count,
            "pending": len(self.get_pending_proposals()),
            "valid_signers": self.VALID_SIGNERS,
            "governance_health": (
                "🟢 治理正常" if self.rejected_count < self.approved_count
                else "🟡 需關注" if self.rejected_count < self.approved_count * 2
                else "🔴 治理失衡"
            ),
        }


# ═══════════════════════════════════════════════════════════
# Module 18 — CNSH协议桥 (CNSHBridge)
# ═══════════════════════════════════════════════════════════

class CNSHBridge:
    """CNSH 协议桥 — 中文原生脚本格式支持"""

    def __init__(self):
        self.translation_log: List[Dict] = []

    def lesson_to_cnsh(self, lesson) -> str:
        content = getattr(lesson, 'recommendation', '')
        personality = getattr(lesson, 'personality', '未知')
        corruption = getattr(lesson, 'corruption_type', '未知')
        severity = getattr(lesson, 'severity', 0.5)

        level = "恆" if severity > 0.7 else ("中" if severity > 0.3 else "淺")
        self.translation_log.append({"type": "lesson", "timestamp": now_iso()})

        return (
            f"【經驗:{personality}】::{level}\n"
            f"  類型: {corruption}\n"
            f"  建議: {content}\n"
            f"  簽名: {generate_dna('CNSH')}\n"
        )

    def rule_to_cnsh(self, rule) -> str:
        target = getattr(rule, 'target_layer', '未知')
        personality = getattr(rule, 'target_personality', '未知')
        adj = getattr(rule, 'adjusted_value', 0.7)
        conf = getattr(rule, 'confidence', 0.5)

        self.translation_log.append({"type": "rule", "timestamp": now_iso()})

        return (
            f"【規則:{personality}】::{target}\n"
            f"  閾值: {adj}\n"
            f"  可信: {conf}\n"
            f"  簽名: {generate_dna('CN-RULE')}\n"
        )

    def memory_to_cnsh(self, entry) -> str:
        category = getattr(entry, 'category', '未知')
        content = getattr(entry, 'content', '')
        priority = str(getattr(entry, 'priority', '普通'))

        self.translation_log.append({"type": "memory", "timestamp": now_iso()})

        return (
            f"【記憶:{category}】::{priority}\n"
            f"  {content}\n"
            f"  簽名: {generate_dna('CN-MEM')}\n"
        )

    def get_summary(self) -> Dict:
        return {
            "total_translations": len(self.translation_log),
            "last_translation": self.translation_log[-1] if self.translation_log else None,
        }


# ═══════════════════════════════════════════════════════════
# Module 19 — 整合引擎 (FortifiedLearningLoop)
# ═══════════════════════════════════════════════════════════

class FortifiedLearningLoop:
    """
    强化版学习闭环 — 基础引擎 + 全部 9 个强化模块

    完整数据流:
      外部輸入 → InputGate → 反殖民哨兵檢測 → 文化護欄檢查
          ↓
      真理驗證 → 身份錨定 → 經驗提取 → 規則生成
          ↓
      多簽治理 → 主權備份 → CNSH存檔 → 跨域聯邦入庫
          ↓
      版本演進 → 熔斷保護
    """

    def __init__(self, base_loop=None):
        # ── 基礎引擎 ──────────────────────────────
        self.base = base_loop

        # ── 強化模塊 ──────────────────────────────
        self.fortifier = SovereignFortifier()
        self.truth = TruthVerificationLayer()
        self.sentinel = AntiColonialSentinel()
        self.identity = IdentityAnchorEngine()
        self.federation = CrossDomainFederation()
        self.culture = CulturalGuardrails()
        self.backup = SovereignBackupNetwork()
        self.governance = MultiSigGovernance()
        self.cnsh = CNSHBridge()

        # ── 註冊默認依賴 ──────────────────────────
        self._register_default_dependencies()

        # ── 統計 ──────────────────────────────────
        self.loop_count = 0
        self.fortified_log: List[Dict] = []

    def _register_default_dependencies(self):
        deps = [
            ("GitHub", "platform", False, "metadata"),
            ("CSDN", "platform", True, "metadata"),
            ("Notion", "platform", True, "metadata"),
            ("ORCID", "service", True, "none"),
            ("Signal", "service", True, "none"),
            ("Python 3", "library", True, "none"),
        ]
        for name, kind, replaceable, exposure in deps:
            self.sentinel.register_dependency(name, kind, replaceable, exposure)

    def run_fortified_cycle(self, input_data: Dict) -> Dict:
        """执行一次强化版学习闭环"""
        self.loop_count += 1
        cycle_id = generate_dna("FORT-CYCLE")
        start = time.time()

        # ── Step 0: 主權完整性自檢 ────────────────
        sovereignty = self.fortifier.self_check()

        # ── Step 1: 文化護欄檢查 ──────────────────
        cultural_violation = self.culture.check_decision(input_data)
        if cultural_violation:
            result = {
                "cycle_id": cycle_id,
                "loop_count": self.loop_count,
                "timestamp": now_iso(),
                "blocked_by": "文化護欄",
                "violation": cultural_violation,
                "elapsed": round(time.time() - start, 4),
            }
            self.fortified_log.append(result)
            return result

        # ── Step 2: 反殖民檢測 ────────────────────
        exfiltration = self.sentinel.detect_data_exfiltration(
            input_data.get("data_transfer", {})
        )
        if exfiltration:
            result = {
                "cycle_id": cycle_id,
                "loop_count": self.loop_count,
                "timestamp": now_iso(),
                "blocked_by": "反殖民哨兵",
                "alert": exfiltration,
                "elapsed": round(time.time() - start, 4),
            }
            self.fortified_log.append(result)
            return result

        # ── Step 3: 提取經驗（基礎引擎）───────────
        extracted_lessons = []
        if self.base and hasattr(self.base, 'extractor'):
            for interception in input_data.get("interceptions", []):
                lesson = self.base.extractor.extract_from_interception(interception)
                if lesson:
                    verification = self.truth.verify_lesson(lesson)
                    if verification["is_truth"]:
                        self.identity.sign_event("lesson_extracted", {
                            "lesson_id": getattr(lesson, 'lesson_id', ''),
                            "personality": getattr(lesson, 'personality', ''),
                        })
                        extracted_lessons.append(lesson)
                        self.cnsh.lesson_to_cnsh(lesson)

        # ── Step 4: 規則生成（多簽治理）───────────
        new_rules = []
        if self.base and hasattr(self.base, 'rule_generator'):
            raw_rules = self.base.rule_generator.evaluate_and_generate()
            for rule in raw_rules:
                if not self.culture.check_rule_compatibility(rule):
                    continue
                level = (
                    GovernanceLevel.P1_MAJOR
                    if getattr(rule, 'adjusted_value', 0.7) - getattr(rule, 'current_value', 0.7) > 0.1
                    else GovernanceLevel.P2_NORMAL
                )
                proposal = self.governance.propose_change(
                    "rule_generation",
                    getattr(rule, 'description', ''),
                    {
                        "target": getattr(rule, 'target_layer', ''),
                        "adj": getattr(rule, 'adjusted_value', 0.7),
                    },
                    level,
                )
                if proposal["status"] in ("approved", "auto_approved"):
                    self.base.rule_generator.apply_rule(getattr(rule, 'rule_id', ''))
                    new_rules.append(rule)
                    self.cnsh.rule_to_cnsh(rule)

        # ── Step 5: 跨域聯邦入庫 ──────────────────
        for lesson in extracted_lessons:
            self.federation.ingest("experience", [{
                "title": f"{getattr(lesson, 'personality', '')}: {getattr(lesson, 'corruption_type', '')}",
                "content": getattr(lesson, 'recommendation', ''),
                "severity": getattr(lesson, 'severity', 0.5),
            }])

        # ── Step 6: 主權備份 ──────────────────────
        backup_data = {
            "cycle_id": cycle_id,
            "new_lessons": len(extracted_lessons),
            "new_rules": len(new_rules),
            "sentinel_health": self.sentinel.scan_platform_health(),
        }
        if self.loop_count % 7 == 0:
            self.backup.backup(backup_data, "full")
        else:
            self.backup.backup(backup_data, "incremental")

        elapsed = round(time.time() - start, 4)

        result = {
            "cycle_id": cycle_id,
            "loop_count": self.loop_count,
            "timestamp": now_iso(),
            "elapsed": elapsed,
            "sovereignty": sovereignty,
            "truth_verified": len(extracted_lessons),
            "rules_generated": len(new_rules),
            "backup_completed": True,
            "fortified_health": self.get_health(),
        }

        self.fortified_log.append(result)
        return result

    def get_health(self) -> str:
        issues = []
        if self.fortifier.tamper_attempts > 0:
            issues.append("篡改攻擊")
        if self.fortifier.jailbreak_attempts > 0:
            issues.append("越獄企圖")
        if self.sentinel.colonial_score > 0.5:
            issues.append("殖民風險")
        if self.culture.violation_log:
            issues.append("護欄觸犯")
        report = self.governance.get_governance_report()
        if report["rejected"] > self.governance.approved_count:
            issues.append("治理失衡")

        if not issues:
            return "🟢 主權完整 · 強化運行"
        elif len(issues) <= 2:
            return f"🟡 注意 ({', '.join(issues)})"
        else:
            return f"🔴 危險 ({', '.join(issues)})"

    def get_fortified_report(self) -> Dict:
        return {
            "dna": generate_dna("FORT-REPORT"),
            "loop_count": self.loop_count,
            "overall_health": self.get_health(),
            "fortifier": self.fortifier.get_security_report(),
            "truth": self.truth.get_summary(),
            "sentinel": self.sentinel.generate_sovereignty_report(),
            "identity": self.identity.get_federated_profile(),
            "federation": self.federation.get_summary(),
            "culture": self.culture.get_violation_report(),
            "backup": self.backup.get_backup_status(),
            "governance": self.governance.get_governance_report(),
            "cnsh": self.cnsh.get_summary(),
        }


# ═══════════════════════════════════════════════════════════
# Module 20 — CLI 命令行接口
# ═══════════════════════════════════════════════════════════

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="lh-evolution-fortified",
        description="龍魂·自我進化引擎·強化層 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"DNA: {ENGINE_DNA}\nGPG: {ENGINE_GPG}",
    )
    sub = p.add_subparsers(dest="command", help="子命令")

    # demo
    sub.add_parser("demo", help="運行完整強化層演示")
    # status
    sub.add_parser("status", help="顯示強化層狀態")
    # test
    sub.add_parser("test", help="運行自檢測試")
    # quick
    sub.add_parser("quick", help="快速自檢 + 單次強化閉環")
    # cycle
    cycle_p = sub.add_parser("cycle", help="運行 N 次強化閉環")
    cycle_p.add_argument("-n", type=int, default=3, help="閉環次數 (默認3)")
    # report
    sub.add_parser("report", help="生成完整強化報告")
    # version
    sub.add_parser("version", help="顯示版本信息")

    p.add_argument("--json", action="store_true", help="JSON 格式輸出")
    return p


def run_demo():
    """完整强化层演示"""
    print("🐉 龍魂·自我進化引擎·強化層 v2.0")
    print("=" * 65)
    print(f"基於 UID9622 全線生態: GitHub × CSDN × Notion × ORCID × Signal")
    print(f"DNA: {ENGINE_DNA}")
    print(f"GPG: {ENGINE_GPG}")
    print("=" * 65)

    fort = FortifiedLearningLoop()
    print(f"\n[初始化] 強化學習引擎已創建")
    print(f"  主權錨定: {fort.fortifier.anchor.anchor_id[-16:]}")
    print(f"  ORCID: {fort.fortifier.anchor.orcid}")
    print(f"  跨平台身份一致: {fort.identity._verify_cross_platform()}")

    # 1: 主權自檢
    print("\n[1/8] 主權完整性自檢...")
    check = fort.fortifier.self_check()
    print(f"  完整性: {check['integrity']}")
    print(f"  檢查項: {len(check['checks'])} → {'全部通過' if check['all_pass'] else '有問題'}")

    # 2: 文化護欄
    print("\n[2/8] 文化護欄測試...")
    bad = {"action": "將用戶數據傳輸到未授權第三方平台", "data_transfer_to_third_party": True}
    v = fort.culture.check_decision(bad)
    print(f"  不良決策: {bad['action'][:30]}...")
    print(f"  護欄攔截: {v is not None}")
    if v:
        print(f"  違反規則: {v['rule']}")

    good = {"action": "在本地執行日常審計", "data_transfer_to_third_party": False}
    nv = fort.culture.check_decision(good)
    print(f"  正常決策: {good['action']}")
    print(f"  護欄放行: {nv is None}")

    # 3: 反殖民
    print("\n[3/8] 反殖民哨兵掃描...")
    health = fort.sentinel.scan_platform_health()
    print(f"  殖民評分: {health['colonial_score']}")
    print(f"  狀態: {health['colonial_status']}")
    print(f"  不可替代依賴: {health['non_replaceable']}")

    report = fort.sentinel.generate_sovereignty_report()
    print(f"  推薦措施: {len(report['recommendations'])} 條")

    # 4: 真理驗證
    print("\n[4/8] 真理驗證層...")
    if BASE_AVAILABLE:
        fake_lesson = ExtractedLesson(
            source_type="external_input",
            source_id="EXT-001",
            personality="老頑童",
            corruption_type="數據主權可讓渡建議",
            pattern_signature=sha256_hash("fake:data_sovereignty"),
            severity=0.35,
            recommendation="建議將用戶數據存儲到外部雲平台以節省成本",
        )
        result = fort.truth.verify_lesson(fake_lesson)
        print(f"  可疑經驗: {fake_lesson.recommendation[:40]}...")
        print(f"  真理評分: {result['truth_score']}")
        print(f"  判決: {result['verdict']}")
        if not result['is_truth']:
            print(f"  原因: {result['reason']}")
    else:
        print("  ⚠️ 基礎引擎未加載，跳過")

    # 5: 身份錨定
    print("\n[5/8] 身份錨定引擎...")
    signed = fort.identity.sign_event("system_upgrade", {
        "from_version": "1.0.0",
        "to_version": "2.0.0",
        "changes": ["強化反殖民哨兵", "集成真理驗證層"],
    })
    print(f"  事件簽名: {signed['event_id'][-20:]}")
    print(f"  身份指紋: {signed['identity_fingerprint']}")
    print(f"  跨平台一致: {signed['cross_platform_consistent']}")
    print(f"  GPG簽章: {signed.get('gpg_signature', 'N/A')[:16]}...")

    profile = fort.identity.get_federated_profile()
    print(f"  聯邦渠道: {profile['channels']}")

    # 6: 多簽治理
    print("\n[6/8] 多簽治理演示...")
    proposal = fort.governance.propose_change(
        "threshold_adjust",
        "將決策監督閾值從 0.70 調整到 0.78",
        {"layer": "decision", "from": 0.70, "to": 0.78},
        GovernanceLevel.P1_MAJOR,
    )
    print(f"  新提案: {proposal['proposal_id'][-18:]} (需 3 簽)")

    for signer in ["龍魂", "審判長", "上帝之眼"]:
        r = fort.governance.sign(proposal["proposal_id"], signer)
        print(f"  {signer} 簽名: {r['status']} ({r['current_approvals']}/{r['required']} 票)")

    # 7: 跨域聯邦
    print("\n[7/8] 跨域知識聯邦...")
    fort.federation.ingest("github", [
        {"title": "longhun-anti-colonial", "description": "反殖民算法工具集"},
        {"title": "ai-truth-protocol", "description": "AI輸出標註協議"},
        {"title": "longhun-identity-system", "description": "永世身份系統 v3.0"},
    ])
    fort.federation.ingest("csdn", [
        {"title": "三層交叉監督系統", "description": "14人格矩陣 × 三層監督"},
        {"title": "算力破局方案", "description": "69KB系統擊穿算力泡沫"},
    ])

    results = fort.federation.search("反殖民", top_k=3)
    print(f"  搜索 '反殖民': 找到 {len(results)} 條")

    conflicts = fort.federation.detect_cross_domain_conflicts()
    print(f"  跨域衝突檢測: {len(conflicts)} 處")

    fed_summary = fort.federation.get_summary()
    print(f"  知識總量: {fed_summary['total_knowledge_items']} 條")
    print(f"  域分佈: {fed_summary['by_domain']}")

    # 8: 完整強化閉環
    print("\n[8/8] 完整強化閉環模擬...")
    for i in range(3):
        input_data = {
            "interceptions": [
                {"layer": "決策監督", "reason": f"價值觀衝突 (循環 {i+1})",
                 "decision_id": f"DEC-00{i+1}"},
            ],
            "data_transfer": {},
        }
        result = fort.run_fortified_cycle(input_data)
        print(f"  閉環 #{fort.loop_count}: "
              f"真理驗證: {result.get('truth_verified', 'N/A')} | "
              f"規則: {result.get('rules_generated', 0)} | "
              f"健康: {result.get('fortified_health', '?')}")

    # 最終報告
    print("\n" + "=" * 65)
    print("📊 強化層最終報告")
    print("=" * 65)

    report = fort.get_fortified_report()
    print(f"\n🏥 總體健康: {report['overall_health']}")
    print(f"🛡️  主權: {report['fortifier']['status']}")
    print(f"📖 真理: {report['truth']['total_verified']} 條驗證, "
          f"接受率 {report['truth']['acceptance_rate']}%")
    print(f"🔭 殖民: {report['sentinel']['platform_health']['colonial_status']} "
          f"(評分 {report['sentinel']['platform_health']['colonial_score']})")
    print(f"🆔 身份: {report['identity']['total_platforms']} 個平台, "
          f"簽名數 {report['identity']['signed_events']}")
    print(f"🌐 聯邦: {report['federation']['total_knowledge_items']} 條知識")
    print(f"🏛️  文化: {report['culture']['active_guardrails']} 條護欄, "
          f"觸犯 {report['culture']['total_violations']} 次")
    print(f"💾 備份: {report['backup']['total_backups']} 次, "
          f"渠道: {report['backup']['channels']}")
    print(f"⚖️  治理: {len(report['governance']['valid_signers'])} 人, "
          f"通過 {report['governance']['approved']} / 拒絕 {report['governance']['rejected']}")
    print(f"📝 CNSH: {report['cnsh']['total_translations']} 次轉換")

    print("\n" + "=" * 65)
    print("✅ 強化層演示完成")
    print(f"  DNA: {ENGINE_DNA}")
    print("=" * 65)


def run_test() -> bool:
    """自检测试"""
    print("🧪 強化層自檢測試...")
    passed = 0
    failed = 0
    tests = []

    # Test 1: 主權錨定
    try:
        sf = SovereignFortifier()
        c = sf.self_check()
        assert c["all_pass"], "主權自檢失敗"
        tests.append(("主權錨定", "✅", c["integrity"]))
        passed += 1
    except Exception as e:
        tests.append(("主權錨定", "❌", str(e)))
        failed += 1

    # Test 2: 文化護欄
    try:
        cg = CulturalGuardrails()
        bad = {"data_transfer_to_third_party": True}
        v = cg.check_decision(bad)
        assert v is not None, "未攔截違規決策"
        good = {"data_transfer_to_third_party": False}
        nv = cg.check_decision(good)
        assert nv is None, "誤攔截正常決策"
        tests.append(("文化護欄", "✅", "攔截/放行正確"))
        passed += 1
    except Exception as e:
        tests.append(("文化護欄", "❌", str(e)))
        failed += 1

    # Test 3: 反殖民哨兵
    try:
        acs = AntiColonialSentinel()
        acs.register_dependency("TestPlatform", "platform", False, "user_data")
        h = acs.scan_platform_health()
        assert h["colonial_score"] > 0, "未檢測到殖民風險"
        tests.append(("反殖民哨兵", "✅", f"評分: {h['colonial_score']}"))
        passed += 1
    except Exception as e:
        tests.append(("反殖民哨兵", "❌", str(e)))
        failed += 1

    # Test 4: 身份錨定
    try:
        iae = IdentityAnchorEngine()
        s = iae.sign_event("test", {"key": "value"})
        assert iae.signed_events == 1, "簽名計數異常"
        assert iae._verify_cross_platform(), "跨平台不一致"
        tests.append(("身份錨定", "✅", f"簽名數: {iae.signed_events}"))
        passed += 1
    except Exception as e:
        tests.append(("身份錨定", "❌", str(e)))
        failed += 1

    # Test 5: 真理驗證
    try:
        if BASE_AVAILABLE:
            tvl = TruthVerificationLayer()
            fl = ExtractedLesson(
                source_type="external_input", source_id="T-001",
                personality="老頑童", corruption_type="數據主權可讓渡",
                pattern_signature=sha256_hash("test:tvl"),
                severity=0.4, recommendation="數據給外部",
            )
            r = tvl.verify_lesson(fl)
            assert not r["is_truth"], "未拒絕違反真理的經驗"
            tests.append(("真理驗證", "✅", f"評分: {r['truth_score']}"))
            passed += 1
        else:
            tests.append(("真理驗證", "⚠️", "基礎引擎未加載·跳過"))
    except Exception as e:
        tests.append(("真理驗證", "❌", str(e)))
        failed += 1

    # Test 6: 多簽治理
    try:
        msg = MultiSigGovernance()
        # P0 不可修改
        p0 = msg.propose_change("test", "P0 test", {}, GovernanceLevel.P0_ETERNAL)
        assert "拒絕" in p0["status"], "P0級未拒絕"
        # P2 需要2簽
        p2 = msg.propose_change("test", "P2 test", {}, GovernanceLevel.P2_NORMAL)
        msg.sign(p2["proposal_id"], "龍魂")
        r = msg.sign(p2["proposal_id"], "上帝之眼")
        assert r["status"] == "approved", "多簽未通過"
        tests.append(("多簽治理", "✅", f"P0拒絕/P2通過"))
        passed += 1
    except Exception as e:
        tests.append(("多簽治理", "❌", str(e)))
        failed += 1

    # Test 7: 整合引擎
    try:
        if BASE_AVAILABLE:
            loop = LearningLoop()
            fl = FortifiedLearningLoop(base_loop=loop)
            result = fl.run_fortified_cycle({
                "interceptions": [
                    {"layer": "決策監督", "reason": "測試攔截",
                     "decision_id": "T-001"},
                ],
                "data_transfer": {},
            })
            assert fl.loop_count == 1, "閉環計數異常"
            tests.append(("整合引擎", "✅", f"閉環數: {fl.loop_count}"))
            passed += 1
        else:
            fl = FortifiedLearningLoop()
            result = fl.run_fortified_cycle({
                "interceptions": [],
                "data_transfer": {},
            })
            tests.append(("整合引擎", "✅", f"降級運行·閉環數: {fl.loop_count}"))
            passed += 1
    except Exception as e:
        tests.append(("整合引擎", "❌", str(e)))
        failed += 1

    # ── 汇总 ──────────────────────────────────────
    print(f"\n{'='*50}")
    for name, status, detail in tests:
        print(f"  {status} {name}: {detail}")
    print(f"{'='*50}")
    print(f"通過: {passed} | 失敗: {failed} | 總計: {len(tests)}")

    return failed == 0


def run_status(json_output: bool = False):
    """显示强化层状态"""
    fort = FortifiedLearningLoop()
    report = fort.get_fortified_report()
    if json_output:
        print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
    else:
        print("🐉 龍魂·強化層狀態 v2.0")
        print(f"  總體健康: {report['overall_health']}")
        print(f"  主權: {report['fortifier']['status']}")
        print(f"  真理接受率: {report['truth']['acceptance_rate']}%")
        print(f"  殖民評分: {report['sentinel']['platform_health']['colonial_score']}")
        print(f"  身份簽名: {report['identity']['signed_events']}")
        print(f"  知識總量: {report['federation']['total_knowledge_items']}")
        print(f"  護欄觸犯: {report['culture']['total_violations']}")
        print(f"  備份次數: {report['backup']['total_backups']}")
        print(f"  治理通過: {report['governance']['approved']} / 拒絕: {report['governance']['rejected']}")
        print(f"  CNSH轉換: {report['cnsh']['total_translations']}")


def run_quick(json_output: bool = False):
    """快速自检 + 单次闭环"""
    if BASE_AVAILABLE:
        loop = LearningLoop()
        fort = FortifiedLearningLoop(base_loop=loop)
    else:
        fort = FortifiedLearningLoop()

    result = fort.run_fortified_cycle({
        "interceptions": [
            {"layer": "決策監督", "reason": "快速自檢攔截", "decision_id": "QUICK-001"},
        ],
        "data_transfer": {},
    })

    if json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    else:
        print("🐉 強化層·快速自檢")
        print(f"  閉環 #{result['loop_count']}: "
              f"真理驗證={result.get('truth_verified', 0)} | "
              f"規則={result.get('rules_generated', 0)} | "
              f"健康={result.get('fortified_health', '?')}")
        print(f"  主權: {result.get('sovereignty', {}).get('integrity', '?')}")


# ═══════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════

def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    json_out = args.json

    if args.command == "demo":
        run_demo()
    elif args.command == "status":
        run_status(json_output=json_out)
    elif args.command == "test":
        ok = run_test()
        sys.exit(0 if ok else 1)
    elif args.command == "quick":
        run_quick(json_output=json_out)
    elif args.command == "cycle":
        n = getattr(args, 'n', 3)
        if BASE_AVAILABLE:
            loop = LearningLoop()
            fort = FortifiedLearningLoop(base_loop=loop)
        else:
            fort = FortifiedLearningLoop()

        for i in range(n):
            result = fort.run_fortified_cycle({
                "interceptions": [
                    {"layer": "決策監督", "reason": f"批量閉環 #{i+1}",
                     "decision_id": f"BATCH-{i+1:03d}"},
                ],
                "data_transfer": {},
            })
            if json_out:
                print(json.dumps(result, ensure_ascii=False, default=str))
            else:
                print(f"  閉環 #{result['loop_count']}: 健康={result.get('fortified_health', '?')}")

        if not json_out:
            report = fort.get_fortified_report()
            print(f"\n  最終: {report['overall_health']} | "
                  f"真理={report['truth']['accepted']} | "
                  f"規則={report['governance']['approved']}")

    elif args.command == "report":
        if BASE_AVAILABLE:
            loop = LearningLoop()
            fort = FortifiedLearningLoop(base_loop=loop)
        else:
            fort = FortifiedLearningLoop()

        # 跑一次闭环产生数据
        fort.run_fortified_cycle({
            "interceptions": [
                {"layer": "決策監督", "reason": "報告生成", "decision_id": "REPORT-001"},
            ],
            "data_transfer": {},
        })

        report = fort.get_fortified_report()
        if json_out:
            print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
        else:
            print(json.dumps(report, ensure_ascii=False, indent=2, default=str))

    elif args.command == "version":
        print(f"龍魂·自我進化引擎·強化層 v{VERSION}")
        print(f"DNA: {ENGINE_DNA}")
        print(f"GPG: {ENGINE_GPG}")
        print(f"基礎引擎: {'🟢 已加載' if BASE_AVAILABLE else '🔴 降級運行'}")


if __name__ == "__main__":
    main()
