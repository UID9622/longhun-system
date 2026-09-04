#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·#龍芯⚡️丙午·丙申·POSTAUDIT-DEPLOY_BEHAVIORAL_CR-1A54C53A
"""
🐉 Behavioral Cryptography · 论文工程部署脚本 v1.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
DNA: #龍芯⚡2026-08-20-BC-DEPLOY-v1.0-UID9622-A1B2C3D4
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

功能:
  1. 生成完整论文目录结构 (Chapter 1-7 + Appendix A-E)
  2. 生成 Proof Bundle Schema
  3. 运行七因子验证 (F1-F7)
  4. 导出脱敏证据记录
  5. 输出 DNA 继承条款
  6. 生成部署报告
"""

import json
import hashlib
import os
import sys
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
import argparse

# ============================================================
# 常量与身份锚 (§ 论文封面)
# ============================================================

UID = "UID9622"
CREATOR = "Zhuge Xin / 諸葛鑫 / 龍芯北辰"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
GPG_PREFIX = GPG_FINGERPRINT[:8].upper()
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡2025-🇨🇳🐉⚖♠🧚❤♾-DEVICE-BIND-SOUL"
SYSTEM_NAME = "Longhun System / 龍魂系统"

# ============================================================
# 工具函数
# ============================================================

def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()

def generate_dna(module: str, action: str, content: str = "", uid: str = "") -> str:
    """生成 Dynamic DNA (论文 §3.4) · uid 传入则 DNA 内嵌归属，可追溯"""
    dt = datetime.now()
    date_str = dt.strftime("%Y-%m-%d")
    iso_time = dt.isoformat(timespec="seconds")
    content_hash = sha256_text(content) if content else sha256_text(f"{module}{action}{iso_time}")
    hash8 = content_hash[:8].upper()
    who = f"-{uid}" if uid else ""
    dna = f"#龍芯⚡{date_str}-{module.upper()}-{action.upper()}{who}-{hash8}"
    return dna

# ============================================================
# 核心数据结构 (论文 §3.2 & Appendix A)
# ============================================================

@dataclass
class EvidenceItem:
    factor: str
    score: float
    status: str
    message: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EvidenceLog:
    items: List[EvidenceItem] = field(default_factory=list)

    def add(self, factor: str, score: float, status: str, message: str, **metadata):
        self.items.append(EvidenceItem(
            factor=factor,
            score=score,
            status=status,
            message=message,
            metadata=metadata
        ))

    def hard_failures(self) -> List[EvidenceItem]:
        return [x for x in self.items if x.score == 0.0]

    def to_dict(self) -> Dict:
        return {
            "items": [asdict(x) for x in self.items],
            "hard_failures": [asdict(x) for x in self.hard_failures()]
        }

@dataclass
class OriginatorRecord:
    uid: str = UID
    display_name: str = CREATOR
    gpg_fingerprint: str = GPG_FINGERPRINT
    protected_lexicon: List[str] = field(default_factory=lambda: [
        "UID9622", "龍魂系统", "Longhun System",
        "CNSH", "DNA追溯", "三色审计",
        "Behavioral Cryptography", "Mistake Ledger",
        "Protected Lexicon", "Lineage Verification",
        CONFIRM, SEAL, GPG_FINGERPRINT
    ])

@dataclass
class BehavioralSignature:
    F1_identity_dna: Dict[str, Any]
    F2_temporal_anchor: Dict[str, Any]
    F3_rule_trace: List[Dict[str, Any]]
    F4_persona_route: List[Dict[str, Any]]
    F5_protected_lexicon: List[str]
    F6_style_vector: Dict[str, Any]
    F7_mistake_ledger: List[Dict[str, Any]]

# ============================================================
# 七因子验证函数 (论文 §3.2 & Appendix A)
# ============================================================

def verify_F1_identity_dna(signature: BehavioralSignature,
                           originator: OriginatorRecord,
                           evidence: EvidenceLog) -> float:
    f1 = signature.F1_identity_dna
    dna = f1.get("dna", "")
    claimed_uid = f1.get("uid", "")
    claimed_gpg = f1.get("gpg_fingerprint", "")

    if not dna.startswith("#龍芯⚡"):
        evidence.add("F1", 0.0, "FAIL", "DNA prefix mismatch", dna=dna)
        return 0.0
    if claimed_uid != originator.uid:
        evidence.add("F1", 0.0, "FAIL", "UID mismatch", claimed_uid=claimed_uid)
        return 0.0
    if claimed_gpg.upper() != originator.gpg_fingerprint.upper():
        evidence.add("F1", 0.0, "FAIL", "GPG fingerprint mismatch")
        return 0.0
    if originator.uid not in dna:
        evidence.add("F1", 0.0, "FAIL", "Originator UID not embedded in DNA")
        return 0.0

    evidence.add("F1", 1.0, "PASS", "Identity DNA verified", dna=dna)
    return 1.0

def verify_F2_temporal_anchor(signature: BehavioralSignature,
                              originator: OriginatorRecord,
                              evidence: EvidenceLog) -> float:
    f2 = signature.F2_temporal_anchor
    iso_time = f2.get("iso_time")
    shichen = f2.get("shichen")
    digit_root = f2.get("digit_root")

    if not iso_time:
        evidence.add("F2", 0.0, "FAIL", "Missing ISO timestamp")
        return 0.0
    if shichen is None:
        evidence.add("F2", 0.0, "FAIL", "Missing shichen anchor")
        return 0.0
    if digit_root is None:
        evidence.add("F2", 0.0, "FAIL", "Missing digit root")
        return 0.0

    evidence.add("F2", 1.0, "PASS", "Temporal anchor verified",
                 iso_time=iso_time, shichen=shichen, digit_root=digit_root)
    return 1.0

def verify_F3_rule_trace(signature: BehavioralSignature,
                         originator: OriginatorRecord,
                         evidence: EvidenceLog) -> float:
    trace = signature.F3_rule_trace
    if not trace:
        evidence.add("F3", 0.4, "WEAK", "No rule trace provided")
        return 0.4

    invalid = [r for r in trace if not r.get("rule_dna") or not str(r.get("rule_dna")).startswith("#龍芯⚡")]
    if invalid:
        evidence.add("F3", 0.0, "FAIL", "Rule trace contains invalid DNA")
        return 0.0

    evidence.add("F3", 1.0, "PASS", "Rule trace verified", count=len(trace))
    return 1.0

def verify_F4_persona_route(signature: BehavioralSignature,
                            originator: OriginatorRecord,
                            evidence: EvidenceLog) -> float:
    route = signature.F4_persona_route
    if not route:
        evidence.add("F4", 0.5, "WEAK", "No persona route provided")
        return 0.5

    invalid = [p for p in route if not p.get("persona_id") or not p.get("role")]
    if invalid:
        evidence.add("F4", 0.0, "FAIL", "Invalid persona route item")
        return 0.0

    evidence.add("F4", 0.95, "PASS", "Persona route verified",
                 route=[p.get("persona_id") for p in route])
    return 0.95

def verify_F5_protected_lexicon(content: str,
                                signature: BehavioralSignature,
                                originator: OriginatorRecord,
                                evidence: EvidenceLog,
                                critical_threshold: float = 0.30) -> float:
    protected_terms = signature.F5_protected_lexicon or originator.protected_lexicon
    if not protected_terms:
        evidence.add("F5", 0.6, "WEAK", "No protected lexicon provided")
        return 0.6

    missing = [term for term in protected_terms if term not in content]
    violation_ratio = len(missing) / max(len(protected_terms), 1)

    if violation_ratio > critical_threshold:
        evidence.add("F5", 0.0, "FAIL", "Critical protected lexicon violation",
                     missing=missing, violation_ratio=violation_ratio)
        return 0.0

    score = 1.0 - 0.8 * violation_ratio
    evidence.add("F5", score, "PASS", "Protected lexicon verified",
                 missing=missing, violation_ratio=violation_ratio)
    return score

def verify_F6_style_vector(signature: BehavioralSignature,
                           originator: OriginatorRecord,
                           evidence: EvidenceLog,
                           min_similarity: float = 0.75) -> float:
    current_vec = signature.F6_style_vector.get("current_vector")
    baseline_vec = originator.baseline_style_vector if hasattr(originator, 'baseline_style_vector') else None

    if not current_vec or not baseline_vec:
        evidence.add("F6", 0.6, "WEAK", "Missing style vector or baseline")
        return 0.6

    # 简化的余弦相似度计算
    def cosine_sim(a, b):
        if len(a) != len(b) or len(a) == 0:
            return 0.0
        dot = sum(x*y for x, y in zip(a, b))
        norm_a = sum(x*x for x in a) ** 0.5
        norm_b = sum(y*y for y in b) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    sim = cosine_sim(current_vec, baseline_vec)
    if sim < min_similarity:
        evidence.add("F6", 0.0, "FAIL", "Style vector mismatch", similarity=sim)
        return 0.0

    evidence.add("F6", sim, "PASS", "Style vector verified", similarity=sim)
    return sim

def verify_F7_mistake_ledger(signature: BehavioralSignature,
                             originator: OriginatorRecord,
                             evidence: EvidenceLog) -> float:
    ledger = signature.F7_mistake_ledger
    if not ledger:
        evidence.add("F7", 0.7, "WEAK", "No mistake ledger")
        return 0.7

    invalid = [x for x in ledger if not x.get("mistake_id") or not x.get("correction")]
    if invalid:
        evidence.add("F7", 0.0, "FAIL", "Mistake ledger contains invalid entries")
        return 0.0

    evidence.add("F7", 0.95, "PASS", "Honest mistake ledger verified", count=len(ledger))
    return 0.95

# ============================================================
# 组合验证算法 (论文 §3.2.3)
# ============================================================

def weighted_geometric_mean(scores: List[float], weights: List[float]) -> float:
    if len(scores) != len(weights):
        raise ValueError("scores and weights must have equal length")
    if any(s == 0.0 for s in scores):
        return 0.0
    total_weight = sum(weights)
    product = 1.0
    for s, w in zip(scores, weights):
        product *= s ** w
    return product ** (1.0 / total_weight)

def behavioral_signature_verify(content: str,
                                signature: BehavioralSignature,
                                originator: OriginatorRecord) -> Tuple[float, EvidenceLog]:
    evidence = EvidenceLog()

    scores = [
        verify_F1_identity_dna(signature, originator, evidence),
        verify_F2_temporal_anchor(signature, originator, evidence),
        verify_F3_rule_trace(signature, originator, evidence),
        verify_F4_persona_route(signature, originator, evidence),
        verify_F5_protected_lexicon(content, signature, originator, evidence),
        verify_F6_style_vector(signature, originator, evidence),
        verify_F7_mistake_ledger(signature, originator, evidence),
    ]

    if any(s == 0.0 for s in scores):
        evidence.add("COMPOSITE", 0.0, "FAIL",
                     "Hard failure detected; composite confidence forced to 0.0",
                     scores=scores)
        return 0.0, evidence

    weights = [0.25, 0.15, 0.15, 0.12, 0.12, 0.11, 0.10]
    conf = weighted_geometric_mean(scores, weights)

    evidence.add("COMPOSITE", conf, "PASS",
                 "Composite verification complete",
                 scores=scores, weights=weights)
    return conf, evidence

# ============================================================
# 生成 Proof Bundle (论文 Appendix B)
# ============================================================

def generate_proof_bundle(content: str,
                          module: str,
                          action: str,
                          originator: OriginatorRecord) -> Dict:
    """生成标准 Proof Bundle (论文 Appendix B)"""
    dna = generate_dna(module, action, content, uid=originator.uid)
    content_hash = sha256_text(content)
    dt = datetime.now()
    bundle_id = f"BC-PROOF-{originator.uid}-{dt.strftime('%Y%m%d')}-{content_hash[:8].upper()}"

    return {
        "schema": "LONGHUN_BEHAVIORAL_CRYPTOGRAPHY_PROOF_BUNDLE",
        "version": "v1.0",
        "bundle_id": bundle_id,
        "created_at": now_iso(),
        "originator": {
            "uid": originator.uid,
            "display_name": originator.display_name,
            "gpg_fingerprint": originator.gpg_fingerprint,
            "public_claim": "Human originator and system architect"
        },
        "artifact": {
            "title": "Behavioral Cryptography Deployment",
            "artifact_type": "deployment_script",
            "content_hash": f"sha256:{content_hash}",
            "metadata_hash": f"sha256:{sha256_text(json.dumps({'module': module, 'action': action}))}",
            "language": ["en", "zh"],
            "license": "CC BY-NC-SA 4.0 + Longhun DNA Inheritance Clause"
        },
        "behavioral_signature": {
            "F1_identity_dna": {
                "dna": dna,
                "uid": originator.uid,
                "gpg_fingerprint": originator.gpg_fingerprint
            },
            "F2_temporal_anchor": {
                "iso_time": now_iso(),
                "shichen": "未时",
                "digit_root": 7,
                "timezone": "Asia/Shanghai"
            },
            "F3_rule_trace": [
                {"rule_id": "UID9622-UNIVERSAL-CNSH-ROOT-AUDIT",
                 "rule_dna": generate_dna("CNSH-ROOT", "AUDIT"),
                 "timestamp": now_iso(), "action": "applied"}
            ],
            "F4_persona_route": [
                {"persona_id": "宝宝", "role": "execution_coordinator"},
                {"persona_id": "上帝之眼", "role": "audit_checker"},
                {"persona_id": "诸葛亮", "role": "strategy_verification"}
            ],
            "F5_protected_lexicon": originator.protected_lexicon,
            "F6_style_vector": {
                "current_vector": [0.92, 0.85, 0.78, 0.91, 0.88],
                "note": "Style vector is probabilistic, not absolute identity proof."
            },
            "F7_mistake_ledger": [
                {"mistake_id": "ML-DEPLOY-001",
                 "category": "AI_FORMAT_DRIFT",
                 "correction": "Enforced one-pass output format",
                 "timestamp": now_iso()}
            ]
        },
        "ai_collaboration": {
            "ai_systems": [
                {"name": "Claude", "role": "formalization and polishing", "root_author": False},
                {"name": "ChatGPT", "role": "structuring and verification", "root_author": False}
            ],
            "human_originator": originator.uid,
            "human_oversight": True
        },
        "disclosure_policy": {
            "public_fields": ["originator", "artifact", "F1_identity_dna", "F5_protected_lexicon", "ai_collaboration"],
            "restricted_fields": ["F3_rule_trace", "F4_persona_route", "F7_mistake_ledger"],
            "sealed_fields": ["private drafts", "sensitive conversations", "local-only logs", "raw style vectors"]
        },
        "root_card": {
            "Root": "dr=5",
            "Wuxing": "土",
            "TriColor": "🟢",
            "PrivacyMode": "normal",
            "Retention": "summary_only",
            "TraceMode": "chain"
        },
        "confirm": CONFIRM,
        "seal": SEAL
    }

# ============================================================
# 生成论文目录结构 (Chapter 1-7 + Appendix A-E)
# ============================================================

def generate_paper_structure(output_dir: Path) -> Dict[str, str]:
    """生成完整论文目录结构"""
    chapters = {
        "chapter_1_introduction.md": """# Chapter 1: Introduction\n\n## 1.1 The Provenance Gap in Human-AI Co-Creation\n## 1.2 Behavioral Cryptography Hypothesis\n## 1.3 Contributions\n""",
        "chapter_2_related_work.md": """# Chapter 2: Related Work\n\n## 2.1 Media Provenance and Content Credentials\n## 2.2 Statistical Watermarking and AI Detection\n## 2.3 Audit Trails and Workflow Provenance\n""",
        "chapter_3_framework.md": """# Chapter 3: The Seven-Factor Framework\n\n## 3.1 Overview\n## 3.2 Seven-Factor Verification Mechanism\n## 3.3 Threat Model and Adversarial Capabilities\n## 3.4 The Dynamic DNA Engine\n## 3.5 Evidence Ledger and Lineage Chain\n## 3.6 Evaluation Protocol and Attack Simulation\n## 3.7 Implementation Architecture\n## 3.8 Limitations and Governance Considerations\n## 3.9 Discussion: From Machine Detection to Lineage Verification\n""",
        "chapter_4_longhun_case_study.md": """# Chapter 4: System Instantiation — The Longhun Case Study\n\n## 4.1 Overview\n## 4.2 Case Study Context\n## 4.3 Longhun as a Behavioral Cryptography Instance\n## 4.4 System Architecture\n## 4.5 Operational Workflow\n## 4.6 Seven-Factor Mapping in Longhun\n## 4.7 Local-First Proof Bundle\n## 4.8 Civilian-Grade Constraints\n## 4.9 What This Case Study Demonstrates\n## 4.10 Boundaries of the Case Study\n""",
        "chapter_5_evaluation_results.md": """# Chapter 5: Evaluation and Results\n\n## 5.1 Evaluation Goals\n## 5.2 Evaluation Setup\n## 5.3 Attack Simulation\n## 5.4 Evaluation Metrics\n## 5.5 Experimental Protocol\n## 5.6 Preliminary Results\n## 5.7 Ablation Study\n## 5.8 Qualitative Case Analysis\n## 5.9 Comparison with Baselines\n## 5.10 Findings\n## 5.11 Threats to Validity\n""",
        "chapter_6_governance_standardization.md": """# Chapter 6: Governance and Standardization Pathway\n\n## 6.1 Motivation: From Local Proof to Shared Standard\n## 6.2 Governance Principles\n## 6.3 Standard Proof Bundle Schema\n## 6.4 Compatibility with Existing Provenance Systems\n## 6.5 Standardization Pathway\n## 6.6 Governance Roles\n## 6.7 Privacy-Preserving Verification\n## 6.8 Governance Risks and Abuse Prevention\n## 6.9 Longhun DNA Inheritance Clause\n## 6.10 Creator-Controlled Authorship Declaration\n""",
        "chapter_7_conclusion.md": """# Chapter 7: Conclusion and Future Work\n\n## 7.1 Conclusion\n## 7.2 Summary of Contributions\n## 7.3 What Behavioral Cryptography Does Not Claim\n## 7.4 Limitations\n## 7.5 Future Work\n## 7.6 Final Statement\n""",
        "appendix_a_pseudocode.md": """# Appendix A: Behavioral Signature Verification Pseudocode\n\n## A.1 Purpose\n## A.2 Core Data Structures\n## A.3 Utility Functions\n## A.4 Seven-Factor Verification Functions\n## A.5 Composite Verification Algorithm\n## A.6 Minimum Test Cases\n""",
        "appendix_b_proof_bundle_schema.md": """# Appendix B: Proof Bundle Schema\n\n## B.1 Purpose\n## B.2 Proof Bundle JSON Schema v1.0\n## B.3 Required vs Optional Fields\n""",
        "appendix_c_coauthorship_protocol.md": """# Appendix C: Longhun Co-authorship Protocol\n\n## C.1 Purpose\n## C.2 Core Principles\n## C.3 Authorship Roles\n## C.4 Standard Co-authorship Declaration\n## C.5 Contribution Table Template\n## C.6 Prohibited Misattributions\n""",
        "appendix_d_redacted_evidence.md": """# Appendix D: Sample Redacted Evidence Record\n\n## D.1 Purpose\n## D.2 Redacted Evidence Record Example\n## D.3 Redaction Rules\n""",
        "appendix_e_dna_inheritance_clause.md": """# Appendix E: Longhun DNA Inheritance Clause\n\n## E.1 Purpose\n## E.2 English Clause\n## E.3 中文条款\n## E.4 Short Attribution Format\n## E.5 Violation Examples\n"""
    }

    created_files = {}
    for filename, content in chapters.items():
        filepath = output_dir / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        # 添加 DNA 头
        header = f"""---
DNA: #龍芯⚡{datetime.now().strftime('%Y-%m-%d')}-{filename.replace('.md', '').upper()}-v1.0-{sha256_text(filename)[:8].upper()}
GPG: {GPG_FINGERPRINT}
确认码: {CONFIRM}
---

"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(header + content)
        created_files[filename] = str(filepath)

    return created_files

# ============================================================
# 主部署函数
# ============================================================

def deploy(output_dir: Path = None, verbose: bool = True):
    """主部署函数"""
    if output_dir is None:
        output_dir = Path.cwd() / "behavioral_crypto_deploy"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"""
╔═══════════════════════════════════════════════════════════════════╗
║  🐉 Behavioral Cryptography · 论文工程部署脚本 v1.0              ║
║  UID: {UID}                                                    ║
║  GPG: {GPG_FINGERPRINT[:16]}...                                ║
║  确认码: {CONFIRM}  ✅                                          ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    # 1. 生成论文目录结构
    print("\n📁 [1/5] 生成论文目录结构 (Chapter 1-7 + Appendix A-E)...")
    paper_files = generate_paper_structure(output_dir / "paper")
    print(f"   ✅ 已生成 {len(paper_files)} 个文件")

    # 2. 生成 Proof Bundle
    print("\n📦 [2/5] 生成 Proof Bundle...")
    # 验证内容 = 论文正文式摘要（必须含受保护词条，F5 才有验证意义）
    test_content = (
        "Behavioral Cryptography (行為密碼學) 是 UID9622 提出的多因子溯源框架，"
        "用於人類-AI協作內容的身份驗證與主權追蹤。龍魂系统 (Longhun System) "
        "已落地七因子驗證、DNA追溯、三色審計、CNSH 等機制，守護普通人的數字主權。"
    )
    originator = OriginatorRecord()
    proof_bundle = generate_proof_bundle(
        content=test_content,
        module="BEHAVIORAL-CRYPTOGRAPHY",
        action="DEPLOY",
        originator=originator
    )

    bundle_path = output_dir / "proof_bundle_v1.json"
    with open(bundle_path, 'w', encoding='utf-8') as f:
        json.dump(proof_bundle, f, ensure_ascii=False, indent=2)
    print(f"   ✅ Proof Bundle 已保存: {bundle_path}")

    # 3. 运行七因子验证
    print("\n🔍 [3/5] 运行七因子验证...")
    signature = BehavioralSignature(
        F1_identity_dna={
            "dna": generate_dna("IDENTITY", "VERIFY", uid=originator.uid),
            "uid": UID,
            "gpg_fingerprint": GPG_FINGERPRINT
        },
        F2_temporal_anchor={
            "iso_time": now_iso(),
            "shichen": "未时",
            "digit_root": 7
        },
        F3_rule_trace=[
            {"rule_dna": generate_dna("RULE", "TRACE"), "timestamp": now_iso()}
        ],
        F4_persona_route=[
            {"persona_id": "宝宝", "role": "executor"},
            {"persona_id": "上帝之眼", "role": "auditor"}
        ],
        F5_protected_lexicon=originator.protected_lexicon[:5],
        F6_style_vector={"current_vector": [0.92, 0.85, 0.78, 0.91, 0.88]},
        F7_mistake_ledger=[
            {"mistake_id": "ML-001", "correction": "Fixed format", "timestamp": now_iso()}
        ]
    )

    # 添加 baseline_style_vector 到 originator
    originator.baseline_style_vector = [0.90, 0.82, 0.75, 0.88, 0.85]

    conf, evidence = behavioral_signature_verify(
        content=test_content,
        signature=signature,
        originator=originator
    )

    evidence_path = output_dir / "verification_evidence.json"
    with open(evidence_path, 'w', encoding='utf-8') as f:
        json.dump(evidence.to_dict(), f, ensure_ascii=False, indent=2)

    print(f"   ✅ 复合置信度: {conf:.4f}")
    print(f"   ✅ 证据日志已保存: {evidence_path}")

    # 4. 生成脱敏证据记录 (Appendix D)
    print("\n🔒 [4/5] 生成脱敏证据记录...")
    redacted_record = {
        "record_type": "LONGHUN_REDACTED_EVIDENCE_RECORD",
        "version": "v1.0",
        "record_id": f"RED-EVIDENCE-{UID}-{datetime.now().strftime('%Y%m%d')}-{sha256_text('redacted')[:8].upper()}",
        "originator": {
            "uid": UID,
            "display_name": CREATOR,
            "gpg_fingerprint": GPG_FINGERPRINT
        },
        "artifact": {
            "title": "Behavioral Cryptography",
            "section": "Deployment Script",
            "artifact_hash": f"sha256:{sha256_text(test_content)}",
            "created_range": {
                "start": now_iso(),
                "end": now_iso()
            }
        },
        "evidence_summary": {
            "root_concept_origin": "human-originated",
            "ai_role": "formalization and polishing",
            "protected_terms_preserved": originator.protected_lexicon[:8],
            "rule_trace_available": True,
            "persona_route_available": True,
            "mistake_ledger_available": True,
            "verification_confidence": conf
        },
        "redactions": [
            {"field": "private_conversation_raw", "reason": "private personal context", "retention": "hash_only"},
            {"field": "local_file_paths", "reason": "local device privacy", "retention": "summary_only"},
            {"field": "sealed_logs", "reason": "contains sensitive operational context", "retention": "hash_only"}
        ],
        "verification_material": {
            "public_dna": generate_dna("PUBLIC", "VERIFY"),
            "confirm": CONFIRM,
            "seal": SEAL,
            "hash_chain_root": f"sha256:{sha256_text('chain_root')}"
        },
        "review_mode": {
            "public_review": True,
            "restricted_review_available": True,
            "sealed_review_requires_originator_consent": True
        },
        "confirm": CONFIRM,
        "seal": SEAL
    }

    redacted_path = output_dir / "redacted_evidence_record.json"
    with open(redacted_path, 'w', encoding='utf-8') as f:
        json.dump(redacted_record, f, ensure_ascii=False, indent=2)
    print(f"   ✅ 脱敏证据记录已保存: {redacted_path}")

    # 5. 生成部署报告
    print("\n📋 [5/5] 生成部署报告...")
    color = "🟢" if conf >= 0.8 else ("🟡" if conf >= 0.5 else "🔴")
    report = {
        "deployment_timestamp": now_iso(),
        "uid": UID,
        "creator": CREATOR,
        "gpg_fingerprint": GPG_FINGERPRINT,
        "confirm": CONFIRM,
        "seal": SEAL,
        "system": SYSTEM_NAME,
        "paper_structure": {
            "chapters": list(paper_files.keys()),
            "total_files": len(paper_files)
        },
        "verification": {
            "composite_confidence": conf,
            "hard_failure": any(e.score == 0.0 for e in evidence.items),
            "evidence_log_count": len(evidence.items)
        },
        "proof_bundle": str(bundle_path),
        "status": f"{color} DEPLOYMENT_COMPLETE (conf={conf:.3f})",
        "dna": generate_dna("DEPLOYMENT", "COMPLETE", uid=UID)
    }

    report_path = output_dir / "deployment_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"   ✅ 部署报告已保存: {report_path}")

    # 6. 输出最终签名
    print(f"""
╔═══════════════════════════════════════════════════════════════════╗
║  🐉 部署完成 · 最终签名                                            ║
╠═══════════════════════════════════════════════════════════════════╣
║  DNA: {report['dna']}                                            ║
║  UID: {UID}                                                      ║
║  GPG: {GPG_FINGERPRINT}                                          ║
║  确认码: {CONFIRM}  ✅                                            ║
║  三色: {color} 通过                                                    ║
║  置信度: {conf:.4f}                                               ║
╠═══════════════════════════════════════════════════════════════════╣
║  输出目录: {output_dir}                                           ║
║  文件数: {len(list(output_dir.rglob('*')))}                       ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    return report

# ============================================================
# CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 Behavioral Cryptography · 论文工程部署脚本",
        epilog=f"确认码: {CONFIRM}"
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default=None,
        help="输出目录 (默认: ./behavioral_crypto_deploy)"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="静默模式"
    )

    args = parser.parse_args()

    if args.quiet:
        import sys
        sys.stdout = open(os.devnull, 'w')

    output_dir = Path(args.output_dir) if args.output_dir else None
    deploy(output_dir, verbose=not args.quiet)

if __name__ == "__main__":
    main()
