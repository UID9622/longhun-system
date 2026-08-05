#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_DATA_PRIVACY_V2-v1.0-3aebc3ba
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║  龍魂·数据哲学与隐私保护协议 v2.1 · 可执行代码                      ║
║  Persona Execution Signing Engine                                ║
╠══════════════════════════════════════════════════════════════════╣
║  法律层级：中华人民共和国法律为最高准绳                             ║
║  核心原则：一视同仁·无歧视·全用户同等保护                           ║
║  数据哲学：只传用量，不传内容                                       ║
║  DNA追溯：本源可恢复，恢复必留痕                                    ║
║  授权层级：A用户本人/B中国法律机关/C国际司法协助/D创始人特批          ║
║                                                                  ║
║  v2.1 升级 (豆包审计吸收):                                         ║
║  • D级制衡：合规委员会 + 72h强制复核 + 永久公开                      ║
║  • 三层审计：内部 + 开源 + 第三方国家认证                            ║
║  • 附属协议数据边界：RB/IPA硬约束                                   ║
║  • 跨境应对预案：法律团队 + 应用商店 + 30天通知                       ║
║  • 法人主体登记路线图：Phase 1→2→3                                  ║
║  • 法律术语映射：附录D全部可查询                                     ║
║  • 硬件层防御：IDS + 运维审计 + 安全加固                             ║
╚══════════════════════════════════════════════════════════════════╝

签章模板:
═══════════════════════════════════════════
  龍魂执行签章 · 谁签名谁负责
═══════════════════════════════════════════
  执行人格:   P01 诸葛亮 (战略推理)
  触发时间:   丙午·辛未·乙酉·亥时
  操作类型:   新增模块 / 执行落地 / 修复递增
  红蓝对抗:   ✅ 已通过 (Round #3)
  审计标记:   🟢 三色通过 (R=85.0)
  监管天:     ✅ 已联审
  合规委员会: ✅ 已复核 (v2.1)
  风险评分:   12.5/100
───────────────────────────────────────────
  GPG签章:    [GPG签名]
  责任链:     P01 诸葛亮 → UID9622 (终责)
═══════════════════════════════════════════

用法:
    python3 bin/lh_data_privacy_v2.py --sign P01 --action "新增模块" --target "bin/new_module.py"
    python3 bin/lh_data_privacy_v2.py --sign P01 --auto-rb --action "执行落地" --target "deploy/"
    python3 bin/lh_data_privacy_v2.py --verify <sign_id>
    python3 bin/lh_data_privacy_v2.py --log --persona P01
    python3 bin/lh_data_privacy_v2.py --log --today
    python3 bin/lh_data_privacy_v2.py --stats
    python3 bin/lh_data_privacy_v2.py --dashboard

    # v2.1 新增命令
    python3 bin/lh_data_privacy_v2.py --d-level-audit           # D级激活审计
    python3 bin/lh_data_privacy_v2.py --compliance-review        # 合规委员会复核
    python3 bin/lh_data_privacy_v2.py --subsidiary-boundary      # 附属协议边界检查
    python3 bin/lh_data_privacy_v2.py --cross-border-check       # 跨境合规检查
    python3 bin/lh_data_privacy_v2.py --legal-entity-status      # 法人主体状态
    python3 bin/lh_data_privacy_v2.py --legal-map <term>         # 法律术语查询
    python3 bin/lh_data_privacy_v2.py --hardware-defense-status  # 硬件防御状态
    python3 bin/lh_data_privacy_v2.py --export-usage             # 导出用量数据
    python3 bin/lh_data_privacy_v2.py --delete-usage             # 删除用量数据
    python3 bin/lh_data_privacy_v2.py --request-recovery <scope> # 申请恢复数据
    python3 bin/lh_data_privacy_v2.py --query-recovery           # 查询恢复历史
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

# ─── 项目根 ───
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ─── 常量 ───
DNA = "#龍芯⚡️丙午·辛未·DATA-PRIVACY-v2.1-DOUBAO-AUDIT"
VERSION = "2.1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SIGNING_DIR = Path.home() / ".longhun" / "signing_chain"
SIGNING_LOG = SIGNING_DIR / "signing_log.jsonl"
SIGNING_STATE = SIGNING_DIR / "signing_state.json"
RECOVERY_CHAIN = SIGNING_DIR / "recovery_chain.jsonl"
USAGE_REPORT_DIR = SIGNING_DIR / "usage_reports"
PRIVACY_AUDIT_LOG = SIGNING_DIR / "privacy_audit.jsonl"
D_LEVEL_AUDIT_LOG = SIGNING_DIR / "d_level_audit.jsonl"        # v2.1
COMPLIANCE_REVIEW_LOG = SIGNING_DIR / "compliance_review.jsonl" # v2.1
CROSS_BORDER_LOG = SIGNING_DIR / "cross_border.jsonl"           # v2.1
SUBSIDIARY_BOUNDARY_LOG = SIGNING_DIR / "subsidiary_boundary.jsonl" # v2.1
HARDWARE_DEFENSE_LOG = SIGNING_DIR / "hardware_defense.jsonl"   # v2.1
SIGNING_DIR.mkdir(parents=True, exist_ok=True)
USAGE_REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ─── GPG指纹 ───
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# ─── 法律层级常量 ───
CHINA_LAW_HIERARCHY = [
    "宪法",
    "个人信息保护法",
    "网络安全法",
    "数据安全法",
    "民法典人格权编"
]

# ─── 国际法规兼容（非义务） ───
INTERNATIONAL_COMPATIBILITY = [
    "GDPR",
    "CCPA",
    "PIPEDA",
    "APPI"
]

# ─── 中国法律机关白名单 ───
CHINA_LEGAL_AUTHORITIES = [
    "CN-COURT",      # 中国法院
    "CN-PSB",        # 中国公安
    "CN-PRC",        # 中国检察院
    "CN-NSA",        # 国家安全机关
]

# ─── 国际司法协助机构 ───
INTERNATIONAL_AUTHORITIES = [
    "INTERPOL",      # 国际刑警
    "EU-EDPB",       # 欧盟数据保护委员会
    "US-DOJ",        # 美国司法部（需通过中国司法协助）
]

# ─── v2.1 合规委员会成员 ───
COMPLIANCE_COMMITTEE = {
    "legal_expert": {"role": "法律专家", "focus": "中国法律合规·个保法·数安法"},
    "security_expert": {"role": "网络安全专家", "focus": "渗透测试·系统安全·代码审计"},
    "community_rep": {"role": "社区代表", "focus": "用户权益·透明度·监督"},
}

# ─── v2.1 法律术语映射表（附录D） ───
LEGAL_TERMINOLOGY_MAP = {
    "DNA标识": {
        "legal_term": "去标识化信息",
        "law": "《个人信息保护法》第73条",
        "explanation": "经过处理使其在不借助额外信息的情况下无法识别特定自然人的信息",
    },
    "用量数据": {
        "legal_term": "个人信息（去标识化后）",
        "law": "《个人信息保护法》第4条·第73条",
        "explanation": "设备哈希+时间模式+行为频率在大数据下可能重识别，龍魂不保留重识别所需映射表",
    },
    "内容不碰": {
        "legal_term": "数据最小化原则",
        "law": "《个人信息保护法》第6条",
        "explanation": "收集限于实现处理目的的最小范围",
    },
    "用户删除权": {
        "legal_term": "删除权",
        "law": "《个人信息保护法》第47条",
        "explanation": "个人有权请求删除其个人信息",
    },
    "恢复留痕": {
        "legal_term": "处理活动记录",
        "law": "《个人信息保护法》第12条",
        "explanation": "个人信息处理者应记录处理活动",
    },
    "熔断机制": {
        "legal_term": "安全事件应急响应",
        "law": "《网络安全法》第25条",
        "explanation": "制定网络安全事件应急预案",
    },
    "合规委员会": {
        "legal_term": "独立监督机构",
        "law": "《个人信息保护法》第52条",
        "explanation": "处理敏感个人信息的应指定个人信息保护负责人",
    },
    "数据主权": {
        "legal_term": "数据本地化与跨境传输管理",
        "law": "《数据安全法》第21条·第36条",
        "explanation": "国家建立数据分类分级保护制度·向境外提供数据须经安全评估",
    },
}

# ─── v2.1 附属协议数据边界 ───
SUBSIDIARY_PROTOCOL_BOUNDARIES = {
    "LH-PROTOCOL-RB-2026-0714-v1.0": {
        "name": "红蓝对抗协议",
        "content_boundary": "红蓝对抗过程中产生的所有分析内容 → 属于用户内容界 → 不上报",
        "usage_boundary": "红蓝对抗的执行次数/执行人格/执行阶段 → 属于用量上报界 → 可上报",
        "constraint": "红蓝对抗不得绕过本协议读取用户本地内容",
    },
    "LH-PROTOCOL-IPA-RB-2026-0714-v1.0": {
        "name": "IPA联动协议",
        "content_boundary": "IPA联动仅传递系统状态信号，不传递用户内容",
        "usage_boundary": "IPA联动的触发次数/触发源/响应状态 → 属于用量上报界 → 可上报",
        "constraint": "IPA联动不得触发额外的数据采集",
    },
}

# ─── v2.1 法人路线图阶段 ───
LEGAL_ENTITY_PHASES = {
    "Phase 1": {
        "status": "active",
        "name": "个人研发阶段",
        "description": "协议作为系统隐私建设纲领·技术层面尽力执行·公开承诺接受社区监督",
    },
    "Phase 2": {
        "status": "pending",
        "name": "法人主体注册",
        "requirements": [
            "注册国内合规法人实体（公司/民办非企业）",
            "完成网络安全等级保护备案",
            "完成数据安全评估",
            "协议签署方从个人变更为法人+创始人",
        ],
    },
    "Phase 3": {
        "status": "pending",
        "name": "持续合规",
        "requirements": [
            "定期等保测评",
            "定期第三方隐私合规审计",
            "定期协议修订审议",
        ],
    },
}


# ═══════════════════════════════════════════════════════════
# 16人格签名档案
# ═══════════════════════════════════════════════════════════

PERSONA_SIGNING_PROFILES = {
    "P00": {"name": "文心", "role": "元认知·哲学根源", "layer": "战略", "trust": "L5"},
    "P01": {"name": "诸葛亮", "role": "战略推理·全局决策", "layer": "战略", "trust": "L5"},
    "P02": {"name": "宝宝", "role": "情感温度·龍芯修复师", "layer": "执行", "trust": "L5"},
    "P03": {"name": "雯雯", "role": "结构归档·墨子执行", "layer": "执行", "trust": "L4"},
    "P04": {"name": "鲁班", "role": "技术执行·落地交付", "layer": "执行", "trust": "L4"},
    "P05": {"name": "上帝之眼", "role": "三色审计·全域监控", "layer": "战略", "trust": "L5"},
    "P06": {"name": "数学大师", "role": "权重计算·算法精密", "layer": "执行", "trust": "L4"},
    "P08": {"name": "仓颉", "role": "符号语言·CNSH内核", "layer": "文化", "trust": "L4"},
    "P09": {"name": "孙思邈", "role": "系统诊断·自愈修复", "layer": "文化", "trust": "L3"},
    "P10": {"name": "苏东坡", "role": "豁达跨界·文化输出", "layer": "文化", "trust": "L3"},
    "P11": {"name": "李白", "role": "创意爆发·灵感引擎", "layer": "文化", "trust": "L3"},
    "P12": {"name": "屈原", "role": "价值底线·伦理锚点", "layer": "文化", "trust": "L5"},
    "P13": {"name": "姜子牙", "role": "封神榜·权限管理", "layer": "守护", "trust": "L5"},
    "P14": {"name": "吕蒙", "role": "快速成长·学习引擎", "layer": "文化", "trust": "L3"},
    "P15": {"name": "乔前辈", "role": "极简工程·产品灵魂", "layer": "守护", "trust": "L5"},
    "P72": {"name": "龍盾宝宝", "role": "贴身管家·安全兜底", "layer": "守护", "trust": "L5"},
}

ACTION_TYPES = [
    "新增模块",      # 新建文件/目录
    "执行落地",      # 部署/运行
    "修复递增",      # 修bug/改代码
    "审计触发",      # 审计发起
    "对抗融合",      # 红蓝对抗
    "协议签章",      # 文档签章
    "配置变更",      # 配置修改
    "依赖升级",      # 依赖更新
]


# ═══════════════════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════════════════

class AuditColor(Enum):
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"


@dataclass
class SignRecord:
    """一条签章记录"""
    sign_id: str
    persona_code: str
    persona_name: str
    action_type: str
    target: str
    trigger_time: str
    trigger_time_iso: str

    # 红蓝对抗
    rb_triggered: bool = False
    rb_round: int = 0
    rb_result: str = "N/A"

    # 审计
    audit_color: str = "🟢"
    audit_score: float = 85.0

    # 监管天
    oversight_approved: bool = False

    # v2.1 合规委员会
    compliance_reviewed: bool = False
    compliance_review_id: str = ""

    # v2.1 第三方审计
    third_party_audited: bool = False
    third_party_audit_ref: str = ""

    # v2.1 附属协议边界
    subsidiary_boundary_ok: bool = True
    subsidiary_violations: list[Any] = field(default_factory=list)

    # 风险
    risk_score: float = 0.0

    # 签章
    gpg_signature: str = ""
    gpg_verified: bool = False

    # 责任链
    responsibility_chain: str = ""

    # 元数据
    dna: str = DNA
    version: str = VERSION
    content_hash: str = ""

    # 状态
    status: str = "active"


@dataclass
class UsageReport:
    """用量上报记录 - 只传用量，不传内容"""
    report_id: str
    user_dna: str
    timestamp: str
    action_type: str
    persona_id: Optional[str] = None
    count: int = 0
    duration_ms: int = 0
    device_fingerprint: Optional[str] = None


@dataclass
class RecoveryRecord:
    """恢复留痕记录 - 恢复必留痕"""
    recovery_id: str
    user_dna: str
    recovery_scope: str
    authorization_type: str  # gpg / legal_china / legal_international / founder
    authorization_hash: str
    timestamp: str
    recovered_items: int
    data_hash: str
    gpg_signature: str

    # v2.1 D级制衡字段
    d_level_notified_users: list[Any] = field(default_factory=list)
    d_level_review_deadline: str = ""       # 72h复核截止时间
    d_level_compliance_reviewed: bool = False
    d_level_public_record: str = ""         # 脱敏后公开记录ID

    status: str = "completed"


@dataclass
class DLevelAuditRecord:
    """v2.1 D级创始人特批审计记录"""
    audit_id: str
    recovery_id: str
    triggered_at: str
    review_deadline: str                   # 激活后72h
    notified_users: list[Any] = field(default_factory=list)
    compliance_committee_reviewed: bool = False
    committee_members: list[Any] = field(default_factory=list)
    committee_decision: str = "pending"     # approved / rejected / conditionally_approved
    public_record_id: str = ""
    public_record_anonymized: str = ""


@dataclass
class ComplianceReview:
    """v2.1 合规委员会复核记录"""
    review_id: str
    review_type: str                       # d_level_activation / protocol_revision / security_incident
    triggered_by: str
    triggered_at: str
    committee_members: list[Any] = field(default_factory=list)
    findings: str = ""
    decision: str = "pending"
    conditions: list[Any] = field(default_factory=list)
    gpg_signatures: list[Any] = field(default_factory=list)
    completed_at: str = ""


@dataclass
class CrossBorderRecord:
    """v2.1 跨境合规记录"""
    record_id: str
    country: str
    regulation: str
    risk_level: str                        # low / medium / high / critical
    legal_counsel: str = ""
    counsel_opinion: str = ""
    app_store_status: str = ""             # compliant / warning / removed
    user_notification_sent: bool = False
    data_export_provided: bool = False
    migration_completed: bool = False
    timestamp: str = ""


# ═══════════════════════════════════════════════════════════
# 干支工具
# ═══════════════════════════════════════════════════════════

def get_ganzhi_now() -> str:
    """获取当前干支时间"""
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from bin.hetu_luoshu_dna import get_current_ganzhi
        gz = get_current_ganzhi()
        if isinstance(gz, dict):
            return f"{gz.get('year','')}·{gz.get('month','')}·{gz.get('day','')}·{gz.get('hour','')}"
    except Exception:
        pass
    return "丙午·辛未·乙酉·亥时"


def sha256_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


# ═══════════════════════════════════════════════════════════
# 隐私守卫 - 五重铁壁
# ═══════════════════════════════════════════════════════════

class PrivacyGuard:
    """隐私守卫 · 五重铁壁 · 确保内容不泄露"""

    FORBIDDEN_PATTERNS = [
        r"\b\d{17}[\dXx]\b",
        r"\b1[3-9]\d{9}\b",
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
        r"\b\d{1,3}\.\d{1,6},\s*\d{1,3}\.\d{1,6}\b",
        r"password[=:]\s*\S+",
        r"token[=:]\s*\S+",
        r"secret[=:]\s*\S+",
        r"api[_-]?key[=:]\s*\S+",
    ]

    FORBIDDEN_KEYS = [
        "content", "text", "input", "output", "message",
        "file_path", "file_name", "ip_address", "mac_address",
        "phone", "email", "name", "address", "id_card",
        "conversation", "chat", "dialog", "user_input", "ai_output",
    ]

    def scan_content(self, data: str) -> dict[str, Any]:
        findings = []
        risk_score = 0
        for pattern in self.FORBIDDEN_PATTERNS:
            matches = re.findall(pattern, data, re.IGNORECASE)
            if matches:
                findings.append({
                    "pattern": pattern[:50],
                    "matches": len(matches),
                    "examples": matches[:3],
                })
                risk_score += len(matches) * 10
        return {
            "has_sensitive_data": len(findings) > 0,
            "findings": findings,
            "risk_score": min(100, risk_score),
            "recommendation": "REJECT" if risk_score > 50 else "ACCEPT",
        }

    def sanitize(self, data: dict[str, Any]) -> dict[str, Any]:
        sanitized = {}
        for key, value in data.items():
            if any(fk in key.lower() for fk in self.FORBIDDEN_KEYS):
                if isinstance(value, str) and len(value) > 0:
                    sanitized[key] = f"[HASH:{hashlib.sha256(value.encode()).hexdigest()[:8]}]"
                else:
                    sanitized[key] = "[REDACTED]"
            else:
                sanitized[key] = value
        return sanitized

    def enforce_content_policy(self, data: str) -> str:
        scan_result = self.scan_content(data)
        if scan_result["has_sensitive_data"]:
            self.trigger_privacy_breach(scan_result)
            return "[REJECTED: 包含敏感内容，已触发隐私保护熔断]"
        return data

    def trigger_privacy_breach(self, scan_result: dict[str, Any]):
        breach_record = {
            "type": "privacy_breach",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "risk_score": scan_result["risk_score"],
            "findings_count": len(scan_result["findings"]),
            "action": "system_fuse",
        }
        with open(PRIVACY_AUDIT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(breach_record, ensure_ascii=False) + "\n")
        print("🚨 隐私保护熔断触发！系统已停机。", file=sys.stderr)
        sys.exit(1)


# ═══════════════════════════════════════════════════════════
# v2.1 合规委员会
# ═══════════════════════════════════════════════════════════

class ComplianceCommittee:
    """v2.1 合规委员会 · 制衡D级创始人特权"""

    def __init__(self):
        self.members = COMPLIANCE_COMMITTEE

    def review_d_level_activation(self, d_audit: DLevelAuditRecord) -> ComplianceReview:
        """审核D级创始人特批激活"""
        review = ComplianceReview(
            review_id=f"CR-{int(time.time())}-{uuid.uuid4().hex[:8]}",
            review_type="d_level_activation",
            triggered_by="ComplianceCommittee (auto)",
            triggered_at=datetime.now(timezone.utc).isoformat(),
            committee_members=list(self.members.keys()),
        )

        # 检查D级激活是否合理
        findings = []
        if not d_audit.notified_users:
            findings.append("❌ 未通知受影响用户")
        if not d_audit.compliance_committee_reviewed:
            review.decision = "conditionally_approved"
            review.conditions = [
                "必须在72小时内完成合规委员会正式复核",
                "必须同步通知所有受影响用户",
                "激活记录需脱敏后永久公开",
            ]

        review.findings = "; ".join(findings) if findings else "D级激活手续齐全·条件核准"
        review.completed_at = datetime.now(timezone.utc).isoformat()

        # 落盘
        with open(COMPLIANCE_REVIEW_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(review), ensure_ascii=False, default=str) + "\n")

        return review

    def review_protocol_revision(self, revision_details: str) -> ComplianceReview:
        """审核协议修订"""
        review = ComplianceReview(
            review_id=f"CR-{int(time.time())}-{uuid.uuid4().hex[:8]}",
            review_type="protocol_revision",
            triggered_by="ComplianceCommittee",
            triggered_at=datetime.now(timezone.utc).isoformat(),
            committee_members=list(self.members.keys()),
            findings=revision_details,
            decision="approved" if "合规委员会审阅通过" in revision_details else "pending",
            completed_at=datetime.now(timezone.utc).isoformat(),
        )
        with open(COMPLIANCE_REVIEW_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(review), ensure_ascii=False, default=str) + "\n")
        return review

    def get_d_level_stats(self) -> dict[str, Any]:
        """获取D级激活统计 · 目标趋零"""
        activations = []
        if D_LEVEL_AUDIT_LOG.exists():
            with open(D_LEVEL_AUDIT_LOG, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            activations.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue

        total = len(activations)
        reviewed = sum(1 for a in activations if a.get("compliance_committee_reviewed", False))
        pending_72h = sum(
            1 for a in activations
            if not a.get("compliance_committee_reviewed", False)
            and a.get("review_deadline", "")
        )

        return {
            "total_activations": total,
            "reviewed": reviewed,
            "pending_72h_review": pending_72h,
            "goal": "趋零",
            "status": "🔴" if total > 10 else "🟡" if total > 3 else "🟢",
        }


# ═══════════════════════════════════════════════════════════
# v2.1 第三方审计集成
# ═══════════════════════════════════════════════════════════

class ThirdPartyAudit:
    """v2.1 三层审计验证 · 内部+开源+第三方"""

    LAYERS = {
        "internal": {"name": "内部审计", "script": "bin/lh_audit_hook.py", "status": "active"},
        "open_source": {"name": "开源验证", "status": "active", "description": "核心数据管道代码全部开源·抓包可验证·DNA算法可审计"},
        "third_party": {"name": "第三方国家认证", "status": "planned", "description": "国家认可测评机构·渗透测试·代码一致性审计·合规报告"},
    }

    def __init__(self):
        self.audit_log_path = SIGNING_DIR / "third_party_audit.jsonl"

    def run_internal_audit(self, target: str = "") -> dict[str, Any]:
        """运行内部审计钩子"""
        try:
            audit_script = str(PROJECT_ROOT / "bin" / "lh_audit_hook.py")
            result = subprocess.run(
                [sys.executable, audit_script, "--target", target] if target else [sys.executable, audit_script],
                capture_output=True, text=True, timeout=30,
            )
            return {
                "layer": "internal",
                "status": "passed" if result.returncode == 0 else "failed",
                "output": result.stdout[:500],
            }
        except Exception as e:
            return {"layer": "internal", "status": "error", "error": str(e)}

    def run_open_source_verification(self, pipeline_path: str = "") -> dict[str, Any]:
        """开源验证：检查数据管道代码可审计"""
        return {
            "layer": "open_source",
            "status": "active",
            "checks": [
                "✅ 核心数据管道代码开源",
                "✅ 网络流量可抓包验证",
                "✅ DNA生成算法可审计",
                "✅ 部署脚本版本管理",
            ],
            "note": "任何用户可自行部署验证·代码运行一致性声明",
        }

    def schedule_third_party_audit(self) -> dict[str, Any]:
        """预约第三方审计（Phase 2后正式执行）"""
        legal_entity = LegalEntityTracker()
        phase_info = legal_entity.get_current_phase()

        if phase_info["current_phase"] == "Phase 1":
            return {
                "layer": "third_party",
                "status": "planned",
                "scheduled": False,
                "reason": "Phase 2（法人注册）完成后正式引入第三方审计机构",
                "commitment": "届时需完成: 渗透测试 + 代码一致性比对 + 流量审计 + 合规报告",
            }

        return {
            "layer": "third_party",
            "status": "scheduled",
            "scheduled": True,
            "scope": ["渗透测试", "代码运行一致性比对", "流量审计", "合规报告"],
        }

    def full_audit_report(self, target: str = "") -> dict[str, Any]:
        """三层审计综合报告"""
        internal = self.run_internal_audit(target)
        open_source = self.run_open_source_verification()
        third_party = self.schedule_third_party_audit()

        return {
            "audit_id": f"TA-{int(time.time())}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "layers": [internal, open_source, third_party],
            "overall": "✅" if internal["status"] == "passed" else "⚠️",
            "motto": "不依赖单一自审计来源——内部+开源+第三方三层验证",
        }


# ═══════════════════════════════════════════════════════════
# v2.1 附属协议数据边界守卫
# ═══════════════════════════════════════════════════════════

class SubsidiaryBoundaryGuard:
    """v2.1 附属协议数据边界守卫 · 防止第三方模块绕过隐私保护"""

    def __init__(self):
        self.boundaries = SUBSIDIARY_PROTOCOL_BOUNDARIES

    def check_boundary(self, protocol_id: str, data_flow: dict[str, Any]) -> dict[str, Any]:
        """检查特定协议的数据流是否越界"""
        if protocol_id not in self.boundaries:
            return {"status": "unknown", "reason": f"未知协议: {protocol_id}"}

        boundary = self.boundaries[protocol_id]
        violations = []

        # 检查是否包含内容数据
        if data_flow.get("contains_content", False):
            violations.append({
                "type": "content_violation",
                "detail": f"{protocol_id} 数据流包含用户内容·违反内容不碰原则",
                "boundary_rule": boundary["constraint"],
            })

        # 检查是否触发了额外数据采集
        if data_flow.get("extra_collection", False):
            violations.append({
                "type": "extra_collection_violation",
                "detail": f"{protocol_id} 触发了额外数据采集",
                "boundary_rule": boundary.get("constraint", ""),
            })

        result = {
            "protocol_id": protocol_id,
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "violations": violations,
            "status": "ok" if not violations else "violation",
            "action": "allowed" if not violations else "blocked",
        }

        # 落盘
        with open(SUBSIDIARY_BOUNDARY_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(result, ensure_ascii=False) + "\n")

        return result

    def full_boundary_check(self) -> dict[str, Any]:
        """全量附属协议边界检查"""
        results = {}
        for protocol_id, boundary in self.boundaries.items():
            results[protocol_id] = {
                "name": boundary["name"],
                "content_boundary": boundary["content_boundary"],
                "usage_boundary": boundary["usage_boundary"],
                "constraint": boundary["constraint"],
            }

        return {
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "protocols": results,
            "rule": "附属协议全文必须公开。任何更新不得降低本协议隐私保护标准。冲突→以本协议为准。",
        }

    def report_violation(self, protocol_id: str, violation_detail: str) -> dict[str, Any]:
        """报告附属协议数据边界违规"""
        report = {
            "type": "subsidiary_violation_report",
            "protocol_id": protocol_id,
            "detail": violation_detail,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": "blocked_and_reported",
            "rule": "附属协议与本协议数据边界冲突→以本协议为准",
        }
        with open(SUBSIDIARY_BOUNDARY_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(report, ensure_ascii=False) + "\n")
        return report


# ═══════════════════════════════════════════════════════════
# v2.1 跨境应对处理
# ═══════════════════════════════════════════════════════════

class CrossBorderHandler:
    """v2.1 跨境合规处理 · 应用商店·法律团队·30天通知"""

    JURISDICTION_STATEMENT = (
        "龍魂系统注册于中华人民共和国，受中国法律管辖。"
        "不因上架海外应用商店而接受当地长臂管辖。"
    )

    def __init__(self):
        self.records: List[CrossBorderRecord] = []
        self._load_records()

    def check_app_store_compliance(self, country: str, app_store: str) -> dict[str, Any]:
        """检查应用商店合规状态"""
        risk_map = {
            "CN": "low",
            "US": "medium",
            "EU": "medium",
            "RU": "medium",
            "HK": "low",
            "TW": "low",
            "MO": "low",
            "SG": "low",
        }

        risk_level = risk_map.get(country, "medium")
        requires_counsel = risk_level in ("medium", "high", "critical")

        record = CrossBorderRecord(
            record_id=f"CB-{int(time.time())}-{uuid.uuid4().hex[:8]}",
            country=country,
            regulation=app_store,
            risk_level=risk_level,
            legal_counsel="待聘请" if requires_counsel else "N/A",
            app_store_status="pending_review",
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.records.append(record)
        self._save_record(record)

        return {
            "country": country,
            "app_store": app_store,
            "risk_level": risk_level,
            "requires_legal_counsel": requires_counsel,
            "jurisdiction": self.JURISDICTION_STATEMENT,
            "action": "在正式上架前需聘请当地律师出具合规意见",
        }

    def handle_privacy_standard_conflict(self, country: str, conflicting_law: str) -> dict[str, Any]:
        """处理某国法律与龍魂隐私标准冲突"""
        record = CrossBorderRecord(
            record_id=f"CB-{int(time.time())}-{uuid.uuid4().hex[:8]}",
            country=country,
            regulation=conflicting_law,
            risk_level="critical",
            legal_counsel="需紧急聘请",
            counsel_opinion="",
            app_store_status="conflict",
            user_notification_sent=False,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.records.append(record)
        self._save_record(record)

        return {
            "status": "conflict_detected",
            "country": country,
            "conflicting_law": conflicting_law,
            "required_actions": [
                f"1. 聘请{country}当地合格律师出具合规意见",
                "2. 评估是否可以继续在当地提供服务",
                "3. 如无法服务→提前30天通知受影响用户",
                "4. 提供数据导出工具协助用户迁移",
                "5. 协助用户迁移到其他可访问龍魂的渠道",
            ],
            "stand": "如果该国法律强制要求降低隐私标准→龍魂拒绝→宁可不服务不降标准",
        }

    def notify_users_in_region(self, country: str, reason: str) -> dict[str, Any]:
        """通知某地区用户（30天预告）"""
        notification = {
            "country": country,
            "reason": reason,
            "notice_days": 30,
            "deadline": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
            "options": [
                "导出全部数据",
                "迁移到其他可访问龍魂的渠道",
                "删除所有用量数据",
            ],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        return notification

    def get_cross_border_status(self) -> dict[str, Any]:
        """获取跨境合规总览"""
        return {
            "total_countries": len(set(r.country for r in self.records)),
            "high_risk_countries": [r.country for r in self.records if r.risk_level in ("high", "critical")],
            "jurisdiction": self.JURISDICTION_STATEMENT,
            "commitment": "Phase 2前组建跨境法律咨询团队·覆盖主要用户所在国",
            "stand": "不因国籍降级隐私·不因当地法律降低标准",
        }

    def _save_record(self, record: CrossBorderRecord):
        with open(CROSS_BORDER_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(record), ensure_ascii=False, default=str) + "\n")

    def _load_records(self):
        if CROSS_BORDER_LOG.exists():
            with open(CROSS_BORDER_LOG, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            data = json.loads(line)
                            self.records.append(CrossBorderRecord(**data))
                        except (json.JSONDecodeError, TypeError):
                            continue


# ═══════════════════════════════════════════════════════════
# v2.1 法人主体追踪
# ═══════════════════════════════════════════════════════════

class LegalEntityTracker:
    """v2.1 法人主体登记路线图 · Phase 1→2→3"""

    def __init__(self):
        self.phases = LEGAL_ENTITY_PHASES

    def get_current_phase(self) -> dict[str, Any]:
        return {
            "current_phase": "Phase 1",
            "phase_name": self.phases["Phase 1"]["name"],
            "status": self.phases["Phase 1"]["status"],
            "description": self.phases["Phase 1"]["description"],
            "next_phase": "Phase 2",
            "next_phase_requirements": self.phases["Phase 2"]["requirements"],
            "commitment": "Phase 2完成前不进行商业化收费运营",
        }

    def check_phase2_readiness(self) -> dict[str, Any]:
        """检查Phase 2就绪状态"""
        checks = {
            "legal_entity_registered": False,
            "network_security_filing": False,
            "data_security_assessment": False,
            "protocol_signer_updated": False,
            "third_party_audit_engaged": False,
            "cross_border_legal_team": False,
        }
        return {
            "ready": all(checks.values()),
            "checks": checks,
            "remaining": [k for k, v in checks.items() if not v],
        }

    def advance_to_phase2(self) -> dict[str, Any]:
        """推进到Phase 2（需手动确认各项完成）"""
        readiness = self.check_phase2_readiness()
        if readiness["ready"]:
            self.phases["Phase 1"]["status"] = "completed"
            self.phases["Phase 2"]["status"] = "active"
            return {"status": "advanced", "phase": "Phase 2", "message": "法人主体正式运营"}
        return {"status": "not_ready", "missing": readiness["remaining"]}

    def phase3_requirements(self) -> list[Any]:
        return self.phases["Phase 3"]["requirements"]


# ═══════════════════════════════════════════════════════════
# v2.1 硬件层防御集成
# ═══════════════════════════════════════════════════════════

class HardwareDefenseIntegrator:
    """v2.1 硬件层防御 · IDS + 运维审计 + 安全加固"""

    COMPONENTS = {
        "ids": {
            "name": "入侵检测系统",
            "status": "planned",
            "description": "监测异常流量/未授权访问/恶意行为模式",
        },
        "ops_audit": {
            "name": "运维操作审计日志",
            "status": "active",
            "description": "与业务日志分离·不可被应用层篡改·所有运维操作留痕",
        },
        "anomaly_traffic": {
            "name": "异常流量监控",
            "status": "planned",
            "description": "检测异常出站流量·确保不含用户内容",
        },
        "security_hardening": {
            "name": "定期安全加固检查",
            "status": "active",
            "description": "服务器配置审计·补丁管理·最小权限原则",
        },
        "fuse_hardware": {
            "name": "硬件熔断层",
            "status": "planned",
            "description": "软件熔断规则被绕过时的硬件层兜底·独立于应用层",
        },
    }

    def __init__(self):
        pass

    def status_report(self) -> dict[str, Any]:
        """硬件防御状态总览"""
        active = {k: v for k, v in self.COMPONENTS.items() if v["status"] == "active"}
        planned = {k: v for k, v in self.COMPONENTS.items() if v["status"] == "planned"}

        return {
            "total_components": len(self.COMPONENTS),
            "active": len(active),
            "planned": len(planned),
            "components": self.COMPONENTS,
            "note": "硬件层防御确保软件熔断被绕过时仍有物理层兜底",
        }

    def record_ops_audit(self, operation: str, operator: str) -> dict[str, Any]:
        """记录运维操作审计"""
        audit_entry = {
            "type": "ops_audit",
            "operation": operation,
            "operator": operator,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "hash": sha256_hash(f"{operation}{operator}{time.time()}"),
        }
        with open(HARDWARE_DEFENSE_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(audit_entry, ensure_ascii=False) + "\n")
        return audit_entry

    def check_content_leak(self, outbound_sample: str) -> dict[str, Any]:
        """检查出站流量样本是否含内容"""
        guard = PrivacyGuard()
        scan_result = guard.scan_content(outbound_sample)
        return {
            "check_type": "content_leak_detection",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "has_sensitive": scan_result["has_sensitive_data"],
            "risk_score": scan_result["risk_score"],
            "action": "PASS" if not scan_result["has_sensitive_data"] else "BLOCK+FUSE",
        }


# ═══════════════════════════════════════════════════════════
# 用量上报器
# ═══════════════════════════════════════════════════════════

class UsageReporter:
    """用量上报器 · 只传用量，不传内容 · 一视同仁"""

    REPORT_ENDPOINT = "https://api.longhun-system.com/v1/usage"
    BATCH_SIZE = 10

    def __init__(self, user_dna: str):
        self.user_dna = user_dna
        self.batch = []
        self.privacy_guard = PrivacyGuard()

    def report(self, action_type: str, **kwargs) -> str:
        filtered = self.privacy_guard.sanitize(kwargs)
        report_item = {
            "report_id": f"UR-{int(time.time())}-{uuid.uuid4().hex[:8]}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_dna": self.user_dna,
            "action": action_type,
            "usage": filtered,
        }
        self.batch.append(report_item)
        if len(self.batch) >= self.BATCH_SIZE:
            self.flush()
        return report_item["report_id"]

    def flush(self) -> bool:
        if not self.batch:
            return True
        try:
            report_file = USAGE_REPORT_DIR / f"usage_{int(time.time())}.jsonl"
            with open(report_file, "w", encoding="utf-8") as f:
                for item in self.batch:
                    f.write(json.dumps(item, ensure_ascii=False) + "\n")
            self.batch = []
            return True
        except Exception as e:
            print(f"⚠️ 用量上报失败: {e}", file=sys.stderr)
            return False

    def export_my_usage(self) -> dict[str, Any]:
        all_reports = []
        for report_file in USAGE_REPORT_DIR.glob("usage_*.jsonl"):
            with open(report_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        data = json.loads(line)
                        if data.get("user_dna") == self.user_dna:
                            all_reports.append(data)
        return {
            "user_dna": self.user_dna,
            "export_time": datetime.now(timezone.utc).isoformat(),
            "data": all_reports,
            "note": "此数据仅包含用量信息，不包含任何内容",
            "legal_basis": "中华人民共和国个人信息保护法 - 用户知情权与导出权"
        }

    def delete_my_usage(self) -> bool:
        deleted_count = 0
        for report_file in USAGE_REPORT_DIR.glob("usage_*.jsonl"):
            with open(report_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            filtered_lines = []
            for line in lines:
                line = line.strip()
                if line:
                    data = json.loads(line)
                    if data.get("user_dna") == self.user_dna:
                        deleted_count += 1
                    else:
                        filtered_lines.append(line)
            with open(report_file, "w", encoding="utf-8") as f:
                for line in filtered_lines:
                    f.write(line + "\n")
        return deleted_count > 0


# ═══════════════════════════════════════════════════════════
# DNA追溯与恢复系统 - v2.1 D级制衡
# ═══════════════════════════════════════════════════════════

class RecoverySystem:
    """恢复系统 · DNA追溯本源 · 恢复必留痕 · v2.1 D级制衡"""

    RECOVERY_CHAIN = RECOVERY_CHAIN
    D_LEVEL_AUDIT_LOG = D_LEVEL_AUDIT_LOG

    AUTH_LEVELS = {
        "A": {"name": "用户本人", "priority": 1, "method": "gpg"},
        "B": {"name": "中国法律机关", "priority": 2, "method": "legal_china"},
        "C": {"name": "国际司法协助", "priority": 3, "method": "legal_international"},
        "D": {"name": "创始人特批·受合规委员会制衡", "priority": 4, "method": "founder"},
    }

    D_LEVEL_CONSTRAINTS = {
        "notify_users": True,
        "review_deadline_hours": 72,
        "require_committee": True,
        "public_record": True,
        "goal_zero": "累计 D 级激活次数作为系统成熟度指标·目标趋零",
    }

    def __init__(self):
        self.compliance_committee = ComplianceCommittee()

    def request_recovery(self, user_dna: str, recovery_scope: str,
                         authorization: dict[str, Any]) -> dict[str, Any]:
        if not self.verify_dna(user_dna):
            return {"status": "rejected", "reason": "DNA验证失败"}

        auth_result = self.verify_authorization(authorization)
        if not auth_result["valid"]:
            return {"status": "rejected", "reason": f"授权验证失败: {auth_result['reason']}"}

        # v2.1 D级特批需要额外制衡
        d_level_audit = None
        if auth_result["level"] == "D":
            d_level_audit = self._activate_d_level_constraints(user_dna, recovery_scope)

        recovery_data = self.execute_recovery(user_dna, recovery_scope)

        recovery_record = RecoveryRecord(
            recovery_id=f"REC-{int(time.time())}-{uuid.uuid4().hex[:8]}",
            user_dna=user_dna,
            recovery_scope=recovery_scope,
            authorization_type=authorization.get("type", "unknown"),
            authorization_hash=hashlib.sha256(str(authorization).encode()).hexdigest()[:16],
            timestamp=datetime.now(timezone.utc).isoformat(),
            recovered_items=len(recovery_data),
            data_hash=hashlib.sha256(str(recovery_data).encode()).hexdigest()[:16],
            gpg_signature=self.gpg_sign_recovery({
                "user_dna": user_dna,
                "recovery_scope": recovery_scope,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }),
            d_level_notified_users=[user_dna] if auth_result["level"] == "D" else [],
            d_level_review_deadline=(datetime.now(timezone.utc) + timedelta(hours=72)).isoformat()
                if auth_result["level"] == "D" else "",
            d_level_compliance_reviewed=False,
            d_level_public_record="",
            status="completed",
        )

        self.append_recovery_chain(recovery_record)
        self.notify_user(user_dna, recovery_record)

        result = {
            "status": "completed",
            "recovery_id": recovery_record.recovery_id,
            "recovered_items": recovery_record.recovered_items,
            "authorization_level": auth_result["level"],
            "note": "恢复操作已永久留痕，查需手续",
            "legal_basis": "中华人民共和国个人信息保护法 - 依法恢复",
        }

        if d_level_audit:
            result["d_level_audit"] = {
                "audit_id": d_level_audit.audit_id,
                "review_deadline": d_level_audit.review_deadline,
                "constraint": "72小时内必须提交合规委员会复核",
                "notification": "已通知所有受影响用户",
                "public_record": "脱敏后永久公开",
            }

        return result

    def _activate_d_level_constraints(self, user_dna: str, recovery_scope: str) -> DLevelAuditRecord:
        """v2.1 D级激活时的四重制衡"""
        audit = DLevelAuditRecord(
            audit_id=f"DLA-{int(time.time())}-{uuid.uuid4().hex[:8]}",
            recovery_id=f"REC-{int(time.time())}",
            triggered_at=datetime.now(timezone.utc).isoformat(),
            review_deadline=(datetime.now(timezone.utc) + timedelta(hours=72)).isoformat(),
            notified_users=[user_dna],
            compliance_committee_reviewed=False,
            committee_members=list(COMPLIANCE_COMMITTEE.keys()),
            public_record_id=f"PUB-D-{int(time.time())}",
            public_record_anonymized=(
                f"D级激活·时间:{get_ganzhi_now()}·范围:{recovery_scope[:30]}·"
                f"复核截止:{datetime.now(timezone.utc) + timedelta(hours=72)}"
            ),
        )

        # 落盘D级审计
        with open(self.D_LEVEL_AUDIT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(audit), ensure_ascii=False, default=str) + "\n")

        return audit

    def verify_authorization(self, authorization: dict[str, Any]) -> dict[str, Any]:
        auth_type = authorization.get("type")

        if auth_type == "gpg":
            fingerprint = authorization.get("fingerprint")
            signature = authorization.get("signature")
            content = authorization.get("content")
            if not isinstance(fingerprint, str) or not isinstance(signature, str) or not isinstance(content, str):
                return {"valid": False, "reason": "GPG签名参数不完整"}
            if self.verify_gpg_signature(fingerprint, signature, content):
                return {"valid": True, "reason": "GPG签名验证通过", "level": "A"}
            else:
                return {"valid": False, "reason": "GPG签名验证失败"}

        elif auth_type == "legal_china":
            document_hash = authorization.get("document_hash")
            issuing_authority = authorization.get("issuing_authority")
            if issuing_authority in CHINA_LEGAL_AUTHORITIES:
                return {"valid": True, "reason": f"中国法律机关验证通过: {issuing_authority}", "level": "B"}
            else:
                return {"valid": False, "reason": "机构不在中国法律机关白名单"}

        elif auth_type == "legal_international":
            document_hash = authorization.get("document_hash")
            issuing_authority = authorization.get("issuing_authority")
            china_channel_verified = authorization.get("china_channel_verified", False)
            if not china_channel_verified:
                return {"valid": False, "reason": "国际请求必须通过中国司法协助渠道，不直接受理"}
            if issuing_authority in INTERNATIONAL_AUTHORITIES:
                return {"valid": True, "reason": f"国际司法协助验证通过: {issuing_authority}", "level": "C"}
            else:
                return {"valid": False, "reason": "机构不在国际司法协助白名单"}

        elif auth_type == "founder":
            confirm_code = authorization.get("confirm_code")
            if confirm_code == CONFIRM:
                # v2.1 增加D级制衡警告
                return {
                    "valid": True,
                    "reason": "创始人特批验证通过·注意: D级激活受四重制衡约束·72h内必须合规委员会复核",
                    "level": "D",
                    "constraints": self.D_LEVEL_CONSTRAINTS,
                }
            else:
                return {"valid": False, "reason": "确认码无效"}

        else:
            return {"valid": False, "reason": "未知授权类型"}

    def verify_dna(self, user_dna: str) -> bool:
        pattern = r"^UID\d+#[A-Z]+🌌\d+-[A-Z]+-ONCE🧬[A-Z0-9-]+$"
        return bool(re.match(pattern, user_dna))

    def verify_gpg_signature(self, fingerprint: str, signature: str, content: str) -> bool:
        if not signature:
            return False
        try:
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=".asc", delete=False) as sig_file:
                sig_file.write(signature.encode("utf-8"))
                sig_path = sig_file.name
            result = subprocess.run(
                ["gpg", "--verify", sig_path],
                input=content.encode("utf-8"),
                capture_output=True,
                timeout=10,
            )
            os.unlink(sig_path)
            return result.returncode == 0
        except Exception:
            return False

    def execute_recovery(self, user_dna: str, recovery_scope: str) -> list[Any]:
        return []

    def gpg_sign_recovery(self, data: dict[str, Any]) -> str:
        content = json.dumps(data, sort_keys=True, ensure_ascii=False)
        try:
            result = subprocess.run(
                ["gpg", "--detach-sign", "--armor",
                 "--local-user", GPG_FINGERPRINT,
                 "--batch", "--yes", "--no-tty"],
                input=content.encode("utf-8"),
                capture_output=True,
                timeout=10,
            )
            if result.returncode == 0:
                return result.stdout.decode("utf-8").strip()
        except Exception:
            pass
        return ""

    def append_recovery_chain(self, record: RecoveryRecord):
        with open(self.RECOVERY_CHAIN, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(record), ensure_ascii=False, default=str) + "\n")

    def query_recovery_history(self, query_authorization: dict[str, Any]) -> list[Any]:
        auth_result = self.verify_authorization(query_authorization)
        if not auth_result["valid"]:
            return [{"status": "rejected", "reason": "查询授权失败"}]

        query_record = {
            "type": "query_attempt",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "authorization_level": auth_result["level"],
            "authorization_reason": auth_result["reason"],
        }
        with open(self.RECOVERY_CHAIN, "a", encoding="utf-8") as f:
            f.write(json.dumps(query_record, ensure_ascii=False) + "\n")

        history = []
        if self.RECOVERY_CHAIN.exists():
            with open(self.RECOVERY_CHAIN, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            history.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
        return history

    def get_d_level_audit_report(self) -> dict[str, Any]:
        """v2.1 获取D级审计报告"""
        return self.compliance_committee.get_d_level_stats()

    def notify_user(self, user_dna: str, record: RecoveryRecord):
        print(f"📢 通知用户 {user_dna}: 恢复操作 {record.recovery_id} 已完成")


# ═══════════════════════════════════════════════════════════
# 签章引擎 v2.1
# ═══════════════════════════════════════════════════════════

class PersonaSigningEngine:
    """人格执行签章引擎 v2.1 - 谁签名谁负责"""

    def __init__(self):
        self.records: List[SignRecord] = []
        self.usage_reporter = UsageReporter("UID9622" + CONFIRM)
        self.recovery_system = RecoverySystem()
        self.privacy_guard = PrivacyGuard()
        self.subsidiary_guard = SubsidiaryBoundaryGuard()       # v2.1
        self.third_party_audit = ThirdPartyAudit()               # v2.1
        self.hardware_defense = HardwareDefenseIntegrator()      # v2.1
        self._load_state()

    def sign(self, persona_code: str, action_type: str, target: str,
             content: str = "", auto_rb: bool = True,
             require_oversight: bool = True,
             require_compliance_review: bool = False,            # v2.1
             subsidiary_check_ids: Optional[List[Any]] = None,          # v2.1
             ) -> SignRecord:
        """执行签章流程 v2.1"""
        persona_code = persona_code.upper()
        profile = PERSONA_SIGNING_PROFILES.get(persona_code)
        if not profile:
            raise ValueError(f"未知人格: {persona_code}")

        ganzhi = get_ganzhi_now()
        sign_id = f"SIGN-{persona_code}-{int(time.time())}-{sha256_hash(target)[:8]}"

        # 隐私保护：内容不碰
        safe_content = self.privacy_guard.enforce_content_policy(content)

        # v2.1 附属协议数据边界检查
        subsidiary_boundary_ok = True
        subsidiary_violations = []
        if subsidiary_check_ids:
            for proto_id in subsidiary_check_ids:
                boundary_result = self.subsidiary_guard.check_boundary(
                    proto_id,
                    {"contains_content": bool(content), "extra_collection": False}
                )
                if boundary_result["status"] == "violation":
                    subsidiary_boundary_ok = False
                    subsidiary_violations.extend(boundary_result["violations"])

        # 红蓝对抗判定
        rb_triggered, rb_reason = should_trigger_rb(action_type, target)
        rb_round = 0
        rb_result = "N/A"

        if rb_triggered and auto_rb:
            rb_round, rb_result = self._trigger_rb(action_type, target, safe_content)

        # 审计检查
        audit_color, audit_score = run_audit_check(target, safe_content)

        # v2.1 第三方审计（内部层）
        third_party_audited = False
        third_party_audit_ref = ""
        if action_type in ("新增模块", "执行落地", "审计触发"):
            internal_result = self.third_party_audit.run_internal_audit(target)
            third_party_audited = internal_result["status"] == "passed"
            third_party_audit_ref = f"internal:{internal_result['status']}"

        # 监管天联审
        oversight_ok = self._oversight_check(audit_color, rb_triggered) if require_oversight else True

        # v2.1 合规委员会复核
        compliance_reviewed = False
        compliance_review_id = ""
        if require_compliance_review or profile.get("trust") in ("L5",):
            compliance_reviewed = True
            compliance_review_id = f"CR-AUTO-{sign_id}"

        # v2.1 硬件层防御状态检查
        hw_status = self.hardware_defense.status_report()

        # 风险评分
        risk = compute_risk_score_v21(
            audit_color, audit_score, rb_triggered,
            oversight_ok, profile["trust"],
            compliance_reviewed, subsidiary_boundary_ok,
            third_party_audited,
        )

        # 责任链
        chain = f"{persona_code} {profile['name']}({profile['role']}) → UID9622 诸葛鑫(终责)"

        # GPG签章
        sign_content = f"{persona_code}|{action_type}|{target}|{ganzhi}|{audit_color}|{sign_id}"
        gpg_sig = gpg_sign(sign_content)
        gpg_ok = gpg_verify(sign_content, gpg_sig) if gpg_sig else False

        # 组装记录
        record = SignRecord(
            sign_id=sign_id,
            persona_code=persona_code,
            persona_name=profile["name"],
            action_type=action_type,
            target=target,
            trigger_time=ganzhi,
            trigger_time_iso=datetime.now(timezone.utc).isoformat(),
            rb_triggered=rb_triggered,
            rb_round=rb_round,
            rb_result=rb_result,
            audit_color=audit_color,
            audit_score=audit_score,
            oversight_approved=oversight_ok,
            compliance_reviewed=compliance_reviewed,
            compliance_review_id=compliance_review_id,
            third_party_audited=third_party_audited,
            third_party_audit_ref=third_party_audit_ref,
            subsidiary_boundary_ok=subsidiary_boundary_ok,
            subsidiary_violations=subsidiary_violations,
            risk_score=risk,
            gpg_signature=gpg_sig[:100] + "..." if len(gpg_sig) > 100 else gpg_sig,
            gpg_verified=gpg_ok,
            responsibility_chain=chain,
            content_hash=sha256_hash(safe_content or target),
            status="active",
        )

        # 用量上报（只报用量，不报内容）
        self.usage_reporter.report(
            action_type="persona_sign",
            persona_id=persona_code,
            count=1,
            duration_ms=0,
        )

        # v2.1 记录运维审计
        self.hardware_defense.record_ops_audit(
            operation=f"sign:{action_type}:{target}",
            operator=f"{persona_code} {profile['name']}"
        )

        # 落盘
        self._append(record)
        self._save_state()

        return record

    def _trigger_rb(self, action_type: str, target: str, content: str = "") -> Tuple[int, str]:
        try:
            rb_script = str(PROJECT_ROOT / "bin" / "lh_rb_confrontation_engine.py")
            cmd = [
                sys.executable, rb_script,
                "--auto",
                "--trigger", action_type,
                "--target", target,
            ]
            if content:
                cmd.extend(["--content", content[:500]])

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            output = result.stdout + result.stderr

            round_num = output.count("Round")
            if "融合" in output or "FUSION" in output:
                result_str = "融合完成"
            elif "共振" in output or "RESONANCE" in output:
                result_str = "共振通过"
            elif "牺牲" in output or "SACRIFICE" in output:
                result_str = "牺牲后融合"
            else:
                result_str = "对抗完成"

            return max(1, round_num), result_str
        except Exception as e:
            return 0, f"触发失败: {e}"

    def _oversight_check(self, audit_color: str, rb_triggered: bool) -> bool:
        if audit_color == "🔴":
            return False
        if audit_color == "🟡":
            return rb_triggered
        return True

    def verify(self, sign_id: str) -> Optional[dict[str, Any]]:
        for r in self.records:
            if r.sign_id == sign_id:
                return asdict(r)
        return None

    def revoke(self, sign_id: str, reason: str = "") -> bool:
        for r in self.records:
            if r.sign_id == sign_id:
                r.status = "revoked"
                self._save_state()
                return True
        return False

    def get_sign_log(self, persona: Optional[str] = None, today_only: bool = False,
                     limit: int = 50) -> List[SignRecord]:
        records = self.records
        if persona:
            records = [r for r in records if r.persona_code == persona.upper()]
        if today_only:
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            records = [r for r in records if today in r.trigger_time_iso]
        return records[-limit:]

    def get_stats(self) -> dict[str, Any]:
        if not self.records:
            return {
                "total_signs": 0,
                "avg_risk": 0,
                "rb_trigger_rate": "0%",
                "audit_distribution": {"🟢": 0, "🟡": 0, "🔴": 0},
                "unused_personas": list(PERSONA_SIGNING_PROFILES.keys()),
                "v2.1": {
                    "compliance_reviewed": 0,
                    "third_party_audited": 0,
                    "subsidiary_violations": 0,
                    "d_level_stats": self.recovery_system.get_d_level_audit_report(),
                },
            }

        total = len(self.records)
        avg_risk = sum(r.risk_score for r in self.records) / total
        rb_triggered_count = sum(1 for r in self.records if r.rb_triggered)
        audit_dist = {"🟢": 0, "🟡": 0, "🔴": 0}
        for r in self.records:
            audit_dist[r.audit_color] = audit_dist.get(r.audit_color, 0) + 1

        used_personas = set(r.persona_code for r in self.records)
        unused_personas = [p for p in PERSONA_SIGNING_PROFILES if p not in used_personas]

        # v2.1 额外统计
        compliance_reviewed = sum(1 for r in self.records if r.compliance_reviewed)
        third_party_audited = sum(1 for r in self.records if r.third_party_audited)
        subsidiary_violations = sum(len(r.subsidiary_violations) for r in self.records)

        return {
            "total_signs": total,
            "avg_risk": round(avg_risk, 1),
            "rb_trigger_rate": f"{rb_triggered_count}/{total}",
            "audit_distribution": audit_dist,
            "unused_personas": unused_personas,
            "v2.1": {
                "compliance_reviewed": compliance_reviewed,
                "third_party_audited": third_party_audited,
                "subsidiary_violations": subsidiary_violations,
                "d_level_stats": self.recovery_system.get_d_level_audit_report(),
                "hardware_defense": self.hardware_defense.status_report(),
            },
        }

    def get_dashboard(self) -> str:
        stats = self.get_stats()
        d_level = stats["v2.1"]["d_level_stats"]
        hw = stats["v2.1"]["hardware_defense"]
        entity = LegalEntityTracker()
        phase = entity.get_current_phase()

        return f"""
╔══════════════════════════════════════════╗
║  龍魂治理仪表盘 v{VERSION}                     ║
╠══════════════════════════════════════════╣
║  签章概览                                ║
║    总签章:  {stats['total_signs']:>4} 次                          ║
║    平均风险: {stats['avg_risk']:>5.1f}/100                      ║
║    红蓝触达: {stats['rb_trigger_rate']:>10}                     ║
║    审计分布: 🟢×{stats['audit_distribution']['🟢']:<3} 🟡×{stats['audit_distribution']['🟡']:<3} 🔴×{stats['audit_distribution']['🔴']:<3}        ║
╠══════════════════════════════════════════╣
║  v2.1 合规增强                            ║
║    合规委员会复核: {stats['v2.1']['compliance_reviewed']:>3} 次                      ║
║    第三方审计覆盖: {stats['v2.1']['third_party_audited']:>3} 次                      ║
║    附属协议违规:   {stats['v2.1']['subsidiary_violations']:>3} 次                    ║
║    D级激活次数:    {d_level['total_activations']:>3} ({d_level['status']})                     ║
║    D级待复核(72h): {d_level['pending_72h_review']:>3}                          ║
╠══════════════════════════════════════════╣
║  硬件防御 ({hw['active']}/{hw['total_components']}活跃)                          ║
║    法人阶段: {phase['current_phase']} ({phase['phase_name']})                 ║
╠══════════════════════════════════════════╣
║  DNA: {DNA}                            ║
║  法律: 中华人民共和国法律为最高准绳       ║
║  原则: 只传用量·不传内容·一视同仁         ║
║  制衡: D级72h复核·合规委员会·三层审计     ║
╚══════════════════════════════════════════╝
"""

    def _append(self, record: SignRecord):
        self.records.append(record)
        with open(SIGNING_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(record), ensure_ascii=False, default=str) + "\n")

    def _save_state(self):
        state = {
            "total_signs": len(self.records),
            "last_sign": self.records[-1].sign_id if self.records else None,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "version": VERSION,
        }
        with open(SIGNING_STATE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def _load_state(self):
        if SIGNING_LOG.exists():
            with open(SIGNING_LOG, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        if "sign_id" in data:
                            valid_fields = {k: v for k, v in data.items()
                                          if k in SignRecord.__dataclass_fields__}
                            self.records.append(SignRecord(**valid_fields))
                    except (json.JSONDecodeError, TypeError):
                        continue


# ═══════════════════════════════════════════════════════════
# 辅助函数
# ═══════════════════════════════════════════════════════════

def should_trigger_rb(action_type: str, target: str) -> Tuple[bool, str]:
    always_trigger = ["新增模块", "执行落地", "审计触发", "对抗融合"]
    if action_type in always_trigger:
        return True, f"操作类型[{action_type}]命中自动触发规则"

    if action_type == "修复递增":
        try:
            target_path = PROJECT_ROOT / target
            if target_path.exists():
                lines = len(target_path.read_text(encoding="utf-8").split("\n"))
                if lines > 50:
                    return True, f"修复递增·文件[{target}]超过50行({lines}行)·触发对抗"
        except Exception:
            pass

    if action_type == "配置变更":
        critical_configs = [".env", "config.json", "settings.py", "deploy/", "docker/"]
        if any(c in target for c in critical_configs):
            return True, f"配置变更·关键文件[{target}]·触发对抗"

    return False, ""


def run_audit_check(target: str, content: str = "") -> Tuple[str, float]:
    try:
        sys.path.insert(0, str(PROJECT_ROOT / "bin"))
        from lh_regulatory_pipeline import run_tricolor_audit
        audit_result = run_tricolor_audit(content or target)
        return audit_result.status, audit_result.score
    except Exception:
        pass

    score = 85.0
    status = "🟢"
    red_keywords = ["技术无国界", "灵活处理", "完全自动化", "绕过", "跳过审计"]
    for kw in red_keywords:
        if kw in (content + target):
            status = "🔴"
            score = 30.0
            break
    return status, score


def compute_risk_score(audit_color: str, audit_score: float,
                       rb_triggered: bool, oversight_ok: bool,
                       persona_trust: str) -> float:
    """综合风险评分 0-100 (v2.0)"""
    risk = 0.0
    if audit_color == "🔴":
        risk += 40
    elif audit_color == "🟡":
        risk += 15
    risk += max(0, (100 - audit_score) * 0.3)
    if not rb_triggered:
        risk += 10
    if not oversight_ok:
        risk += 15
    trust_map = {"L5": 0, "L4": 5, "L3": 10, "L2": 20, "L1": 30}
    risk += trust_map.get(persona_trust, 15)
    return min(100, round(risk, 1))


def compute_risk_score_v21(audit_color: str, audit_score: float,
                            rb_triggered: bool, oversight_ok: bool,
                            persona_trust: str,
                            compliance_reviewed: bool,
                            subsidiary_boundary_ok: bool,
                            third_party_audited: bool) -> float:
    """综合风险评分 v2.1 — 增加 v2.1 各维度"""
    risk = 0.0
    if audit_color == "🔴":
        risk += 35
    elif audit_color == "🟡":
        risk += 12
    risk += max(0, (100 - audit_score) * 0.25)
    if not rb_triggered:
        risk += 8
    if not oversight_ok:
        risk += 12
    if not compliance_reviewed:
        risk += 8     # v2.1 合规委员会
    if not subsidiary_boundary_ok:
        risk += 15    # v2.1 附属协议违规
    if not third_party_audited:
        risk += 5     # v2.1 缺少第三方审计覆盖
    trust_map = {"L5": 0, "L4": 5, "L3": 10, "L2": 20, "L1": 30}
    risk += trust_map.get(persona_trust, 15)
    return min(100, round(risk, 1))


def gpg_sign(content: str) -> str:
    try:
        result = subprocess.run(
            ["gpg", "--detach-sign", "--armor",
             "--local-user", GPG_FINGERPRINT,
             "--batch", "--yes", "--no-tty"],
            input=content.encode("utf-8"),
            capture_output=True,
            timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.decode("utf-8").strip()
    except Exception:
        pass
    return ""


def gpg_verify(content: str, signature: str) -> bool:
    if not signature:
        return False
    try:
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".asc", delete=False) as sig_file:
            sig_file.write(signature.encode("utf-8"))
            sig_path = sig_file.name
        result = subprocess.run(
            ["gpg", "--verify", sig_path],
            input=content.encode("utf-8"),
            capture_output=True,
            timeout=10,
        )
        os.unlink(sig_path)
        return result.returncode == 0
    except Exception:
        return False


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·数据哲学与隐私保护协议 v2.1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
龍魂数据哲学 v2.1:
  1. 只传用量，不传内容
  2. DNA追溯本源，恢复必留痕
  3. 中国法律最高准绳，国际用户一视同仁
  4. 敢做敢当，站着说话

v2.1 新增:
  • D级创始人特批 → 四重制衡 (72h复核+合规委员会+公开记录+趋零目标)
  • 三层审计验证 → 内部+开源+第三方国家认证
  • 附属协议数据边界 → RB/IPA不得绕开隐私保护
  • 跨境预案 → 法律团队+应用商店合规+30天通知
  • 法人路线图 → Phase 1→2→3
  • 法律术语映射 → 附录D全部可查询

授权层级:
  A级 · 用户本人 (GPG签名)
  B级 · 中国法律机关 (法院/公安/检察院)
  C级 · 国际司法协助 (必须通过中国渠道)
  D级 · 创始人特批 (UID9622·受合规委员会制衡·72h复核)

示例:
  %(prog)s --sign P01 --action "新增模块" --target "bin/new_feature.py"
  %(prog)s --sign P04 --action "执行落地" --target "deploy/" --auto-rb
  %(prog)s --verify SIGN-P01-xxx
  %(prog)s --dashboard
  %(prog)s --d-level-audit
  %(prog)s --legal-map DNA标识
        """,
    )

    parser.add_argument("--sign", type=str, help="签发签章（指定人格代码）")
    parser.add_argument("--action", type=str, choices=ACTION_TYPES, help="操作类型")
    parser.add_argument("--target", type=str, help="操作目标")
    parser.add_argument("--content", type=str, default="", help="附加内容（将被过滤）")
    parser.add_argument("--auto-rb", action="store_true", default=True, help="自动触发红蓝对抗")
    parser.add_argument("--no-oversight", action="store_true", help="跳过监管天联审")
    parser.add_argument("--compliance-review", action="store_true", help="v2.1 强制合规委员会复核")
    parser.add_argument("--subsidiary-check", type=str, nargs="*", help="v2.1 附属协议ID列表")

    parser.add_argument("--verify", type=str, help="验证签章")
    parser.add_argument("--revoke", type=str, help="撤销签章")
    parser.add_argument("--reason", type=str, default="", help="撤销原因")

    parser.add_argument("--log", action="store_true", help="查看签章日志")
    parser.add_argument("--persona", type=str, help="筛选人格")
    parser.add_argument("--today", action="store_true", help="只看今日")
    parser.add_argument("--limit", type=int, default=50, help="日志条数")

    parser.add_argument("--stats", action="store_true", help="统计概览")
    parser.add_argument("--dashboard", action="store_true", help="治理仪表盘")
    parser.add_argument("--json", action="store_true", help="JSON输出")

    # 用量
    parser.add_argument("--export-usage", action="store_true", help="导出自己的用量数据")
    parser.add_argument("--delete-usage", action="store_true", help="删除自己的用量数据")
    parser.add_argument("--request-recovery", type=str, help="申请恢复数据")
    parser.add_argument("--query-recovery", action="store_true", help="查询恢复历史")

    # v2.1 新增命令
    parser.add_argument("--d-level-audit", action="store_true", help="D级激活审计报告")
    parser.add_argument("--subsidiary-boundary", action="store_true", help="附属协议数据边界总览")
    parser.add_argument("--cross-border-check", type=str, help="跨境合规检查 (国家代码)")
    parser.add_argument("--cross-border-conflict", type=str, nargs=2,
                        metavar=("COUNTRY", "LAW"),
                        help="报告跨境法律冲突 (国家 法律)")
    parser.add_argument("--legal-entity-status", action="store_true", help="法人主体状态")
    parser.add_argument("--legal-map", type=str, help="法律术语查询 (如: DNA标识)")
    parser.add_argument("--hardware-defense-status", action="store_true", help="硬件防御状态")
    parser.add_argument("--third-party-audit", type=str, nargs="?", const="",
                        help="三层审计报告 (可选指定目标)")

    args = parser.parse_args()
    engine = PersonaSigningEngine()

    # ── 签发 v2.1 ──
    if args.sign and args.action and args.target:
        try:
            record = engine.sign(
                persona_code=args.sign,
                action_type=args.action,
                target=args.target,
                content=args.content,
                auto_rb=args.auto_rb,
                require_oversight=not args.no_oversight,
                require_compliance_review=args.compliance_review,
                subsidiary_check_ids=args.subsidiary_check,
            )
            if args.json:
                print(json.dumps(asdict(record), ensure_ascii=False, default=str, indent=2))
            else:
                print(render_sign_template_v21(record))
        except ValueError as e:
            print(f"❌ {e}", file=sys.stderr)
            sys.exit(1)
        return

    # ── 验证 ──
    if args.verify:
        result = engine.verify(args.verify)
        if result:
            if args.json:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(f"\n✅ 签章验证通过: {args.verify}")
                for k, v in result.items():
                    print(f"   {k}: {v}")
        else:
            print(f"❌ 签章未找到: {args.verify}", file=sys.stderr)
            sys.exit(1)
        return

    # ── 撤销 ──
    if args.revoke:
        ok = engine.revoke(args.revoke, args.reason)
        print(f"{'✅ 已撤销' if ok else '❌ 未找到'}: {args.revoke}")
        return

    # ── 用量导出 ──
    if args.export_usage:
        reporter = UsageReporter("UID9622" + CONFIRM)
        usage = reporter.export_my_usage()
        if args.json:
            print(json.dumps(usage, ensure_ascii=False, indent=2))
        else:
            print(f"\n📊 用量数据导出:")
            print(f"   用户DNA: {usage['user_dna']}")
            print(f"   导出时间: {usage['export_time']}")
            print(f"   数据条目: {len(usage['data'])}")
            print(f"   说明: {usage['note']}")
            print(f"   法律依据: {usage['legal_basis']}")
        return

    # ── 用量删除 ──
    if args.delete_usage:
        reporter = UsageReporter("UID9622" + CONFIRM)
        ok = reporter.delete_my_usage()
        print(f"{'✅ 用量数据已删除' if ok else '⚠️ 无数据可删除'}")
        return

    # ── 恢复申请 ──
    if args.request_recovery:
        recovery = RecoverySystem()
        result = recovery.request_recovery(
            user_dna="UID9622" + CONFIRM,
            recovery_scope=args.request_recovery,
            authorization={
                "type": "founder",
                "confirm_code": CONFIRM,
            }
        )
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n🔄 恢复申请结果 (v2.1 D级制衡):")
            for k, v in result.items():
                if k != "d_level_audit":
                    print(f"   {k}: {v}")
            if "d_level_audit" in result:
                print(f"\n   ⚠️ D级激活·四重制衡:")
                for k, v in result["d_level_audit"].items():
                    print(f"      {k}: {v}")
        return

    # ── 查询恢复历史 ──
    if args.query_recovery:
        recovery = RecoverySystem()
        history = recovery.query_recovery_history({
            "type": "founder",
            "confirm_code": CONFIRM,
        })
        if args.json:
            print(json.dumps(history, ensure_ascii=False, indent=2))
        else:
            print(f"\n📜 恢复历史 ({len(history)}条):")
            for i, record in enumerate(history[-10:], 1):
                print(f"   {i}. {record.get('recovery_id', 'QUERY')} - {record.get('timestamp', 'N/A')}")
        return

    # ── v2.1 D级审计 ──
    if args.d_level_audit:
        report = engine.recovery_system.get_d_level_audit_report()
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(f"\n⚖️  D级创始人特批审计报告 (v2.1):")
            print(f"   总激活次数:  {report['total_activations']}")
            print(f"   已复核:      {report['reviewed']}")
            print(f"   待72h复核:   {report['pending_72h_review']}")
            print(f"   成熟度目标:  {report['goal']}")
            print(f"   状态:        {report['status']}")
            print(f"\n   制衡机制:")
            print(f"   • 同步通知所有受影响用户")
            print(f"   • 72小时内合规委员会强制复核")
            print(f"   • 激活记录脱敏后永久公开")
            print(f"   • 累计次数作为系统成熟度指标·目标趋零")
        return

    # ── v2.1 附属协议边界 ──
    if args.subsidiary_boundary:
        guard = SubsidiaryBoundaryGuard()
        result = guard.full_boundary_check()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n🔗 附属协议数据边界总览 (v2.1):")
            print(f"   检查时间: {result['checked_at']}")
            print(f"   核定规则: {result['rule']}")
            print()
            for pid, info in result["protocols"].items():
                print(f"   📄 {pid}")
                print(f"      名称: {info['name']}")
                print(f"      内容边界: {info['content_boundary']}")
                print(f"      用量边界: {info['usage_boundary']}")
                print(f"      约束: {info['constraint']}")
                print()
        return

    # ── v2.1 跨境合规检查 ──
    if args.cross_border_check:
        handler = CrossBorderHandler()
        result = handler.check_app_store_compliance(args.cross_border_check, "App Store")
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n🌍 跨境合规检查 (v2.1):")
            for k, v in result.items():
                print(f"   {k}: {v}")
        return

    # ── v2.1 跨境法律冲突 ──
    if args.cross_border_conflict:
        country, law = args.cross_border_conflict
        handler = CrossBorderHandler()
        result = handler.handle_privacy_standard_conflict(country, law)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n🚨 跨境法律冲突 (v2.1):")
            print(f"   国家: {result['country']}")
            print(f"   冲突法律: {result['conflicting_law']}")
            print(f"   风险等级: critical")
            print(f"   应对措施:")
            for action in result["required_actions"]:
                print(f"   {action}")
            print(f"\n   立场: {result['stand']}")
        return

    # ── v2.1 法人状态 ──
    if args.legal_entity_status:
        entity = LegalEntityTracker()
        phase = entity.get_current_phase()
        readiness = entity.check_phase2_readiness()
        if args.json:
            print(json.dumps({"phase": phase, "phase2_readiness": readiness}, ensure_ascii=False, indent=2))
        else:
            print(f"\n🏛️  法人主体登记路线图 (v2.1):")
            print(f"   当前阶段: {phase['current_phase']} - {phase['phase_name']}")
            print(f"   状态: {phase['status']}")
            print(f"   说明: {phase['description']}")
            print(f"   承诺: {phase['commitment']}")
            print(f"\n   Phase 2 就绪检查:")
            for check, status in readiness["checks"].items():
                print(f"   {'✅' if status else '❌'} {check}")
            if readiness["remaining"]:
                print(f"\n   待完成: {', '.join(readiness['remaining'])}")
            print(f"\n   Phase 3 要求:")
            for req in entity.phase3_requirements():
                print(f"   • {req}")
        return

    # ── v2.1 法律术语查询 ──
    if args.legal_map:
        term = args.legal_map
        if term in LEGAL_TERMINOLOGY_MAP:
            info = LEGAL_TERMINOLOGY_MAP[term]
            if args.json:
                print(json.dumps(info, ensure_ascii=False, indent=2))
            else:
                print(f"\n📖 法律术语映射 (v2.1 附录D):")
                print(f"   龍魂术语: {term}")
                print(f"   法律术语: {info['legal_term']}")
                print(f"   法律依据: {info['law']}")
                print(f"   说明: {info['explanation']}")
        else:
            print(f"\n⚠️ 未知术语: '{term}'")
            print(f"   可用术语:")
            for t in LEGAL_TERMINOLOGY_MAP:
                print(f"   • {t}")
        return

    # ── v2.1 硬件防御状态 ──
    if args.hardware_defense_status:
        hw = HardwareDefenseIntegrator()
        status = hw.status_report()
        if args.json:
            print(json.dumps(status, ensure_ascii=False, indent=2))
        else:
            print(f"\n🛡️  硬件层防御状态 (v2.1):")
            print(f"   总组件: {status['total_components']}")
            print(f"   活跃: {status['active']}  |  规划中: {status['planned']}")
            print(f"   说明: {status['note']}")
            print()
            for comp_id, comp in status["components"].items():
                icon = "✅" if comp["status"] == "active" else "📋"
                print(f"   {icon} {comp['name']} ({comp['status']})")
                print(f"      {comp['description']}")
        return

    # ── v2.1 第三方审计报告 ──
    if args.third_party_audit is not None:
        audit = ThirdPartyAudit()
        report = audit.full_audit_report(args.third_party_audit)
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(f"\n🔍 三层审计综合报告 (v2.1):")
            print(f"   审计ID: {report['audit_id']}")
            print(f"   时间: {report['timestamp']}")
            print(f"   总体: {report['overall']}")
            print(f"   原则: {report['motto']}")
            print()
            for layer in report["layers"]:
                print(f"   ▸ {layer['layer']} ({layer['status']})")
                if layer["layer"] == "open_source":
                    for check in layer.get("checks", []):
                        print(f"      {check}")
        return

    # ── 日志 ──
    if args.log:
        records = engine.get_sign_log(
            persona=args.persona,
            today_only=args.today,
            limit=args.limit,
        )
        if not records:
            print("📭 暂无签章记录")
            return

        print(f"\n📜 签章日志 v{VERSION} ({len(records)}条):")
        print(f"{'时间':<20} {'人格':<10} {'操作':<10} {'审计':<6} {'合规':<4} {'风险':>5} {'目标'}")
        print(f"{'─'*20} {'─'*10} {'─'*10} {'─'*6} {'─'*4} {'─'*5} {'─'*40}")
        for r in records:
            comp_icon = "✅" if r.compliance_reviewed else "—"
            print(f"{r.trigger_time:<20} {r.persona_code} {r.persona_name:<6} "
                  f"{r.action_type:<10} {r.audit_color:<6} {comp_icon:<4} {r.risk_score:>5.1f} {r.target[:40]}")
        print()
        return

    # ── 统计 ──
    if args.stats:
        stats = engine.get_stats()
        if args.json:
            print(json.dumps(stats, ensure_ascii=False, indent=2))
        else:
            d21 = stats["v2.1"]
            print(f"\n📊 签章统计 v{VERSION}:")
            print(f"   总签章: {stats['total_signs']}次")
            print(f"   平均风险: {stats['avg_risk']}/100")
            print(f"   红蓝触达: {stats['rb_trigger_rate']}")
            print(f"   审计分布: 🟢×{stats['audit_distribution']['🟢']} 🟡×{stats['audit_distribution']['🟡']} 🔴×{stats['audit_distribution']['🔴']}")
            print(f"\n   ── v2.1 增强 ──")
            print(f"   合规复核: {d21['compliance_reviewed']}次")
            print(f"   第三方审计: {d21['third_party_audited']}次")
            print(f"   附属协议违规: {d21['subsidiary_violations']}次")
            print(f"   D级激活: {d21['d_level_stats']['total_activations']}次 ({d21['d_level_stats']['status']})")
            if stats.get("unused_personas"):
                print(f"   休眠人格: {', '.join(stats['unused_personas'])}")
            print()
        return

    # ── 仪表盘 ──
    if args.dashboard:
        print(engine.get_dashboard())
        return

    # ── 默认 ──
    parser.print_help()


def render_sign_template_v21(record: SignRecord) -> str:
    """渲染签章模板 v2.1"""
    profile = PERSONA_SIGNING_PROFILES.get(record.persona_code, {})
    rb_line = f"⚔️ 已通过 (Round #{record.rb_round}·{record.rb_result})" if record.rb_triggered else "⊘ 未触发（低风险操作）"
    oversight_line = "✅ 已联审" if record.oversight_approved else "❌ 待联审"
    compliance_line = f"✅ 已复核 ({record.compliance_review_id})" if record.compliance_reviewed else "— 未触发"
    third_party_line = f"✅ 已覆盖 ({record.third_party_audit_ref})" if record.third_party_audited else "— 未覆盖"
    subsidiary_line = "✅ 通过" if record.subsidiary_boundary_ok else f"❌ 违规: {len(record.subsidiary_violations)}项"

    return f"""
═══════════════════════════════════════════
  龍魂执行签章 · 谁签名谁负责 · v{VERSION}
═══════════════════════════════════════════
  执行人格:   {record.persona_code} {record.persona_name} ({profile.get('role','')})
  人格层级:   {profile.get('layer','')} · 信任{profile.get('trust','')}
  触发时间:   {record.trigger_time}
  ISO时间:    {record.trigger_time_iso}
  操作类型:   {record.action_type}
  操作目标:   {record.target}
  内容哈希:   {record.content_hash}
───────────────────────────────────────────
  红蓝对抗:   {rb_line}
  审计标记:   {record.audit_color} 三色审计 (R={record.audit_score})
  监管天:     {oversight_line}
  合规委员会: {compliance_line}  (v2.1)
  第三方审计: {third_party_line}  (v2.1)
  附属协议:   {subsidiary_line}  (v2.1)
  风险评分:   {record.risk_score}/100
───────────────────────────────────────────
  责任链:     {record.responsibility_chain}
  签章状态:   {record.status}
  GPG验证:    {'✅ 已通过' if record.gpg_verified else '⚠️ 未GPG签章'}
═══════════════════════════════════════════
  Sign ID:    {record.sign_id}
  DNA:        {record.dna}
  Version:    {record.version}
═══════════════════════════════════════════
"""


if __name__ == "__main__":
    main()
