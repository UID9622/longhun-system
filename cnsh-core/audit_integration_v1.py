#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
═══════════════════════════════════════════════════════════════════════════════

⚖️ 三色审计·龍魂系统集成模块 v1.0

Three-Color Audit System Integration with Longhun Ecosystem

═══════════════════════════════════════════════════════════════════════════════

Author:      Claude Haiku 4.5
Authorized:  UID9622 (DragonCore North Star)

DNA:     #龍芯⚡️2026-06-08-Audit-Integration-Longhun-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL:    #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

Integration Points:
  1. 天道系统 v1.3 - contamination_events 记错本
  2. P72·龍盾 - 五态情绪触发审计流程
  3. 九层权重体系 - 敏感断言权重加倍
  4. 确认码+GPG+DNA - 格式安全度验证链
  5. Bra-Ket量子态 - 全真概率投影测量

═══════════════════════════════════════════════════════════════════════════════
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
import hashlib

# Import audit engine
from audit_3color_v1 import (
    AuditReport,
    Assertion,
    TruthComponent,
    AssertionType,
    JudgmentColor,
    ThreeColorAuditEngine
)


# ═════════════════════════════════════════════════════════════════════════════
# 系统常量
# ═════════════════════════════════════════════════════════════════════════════

HOME = os.path.expanduser("~/longhun-system")
KFPP_DB = os.path.expanduser("~/.龍魂/kfpp/kfpp_execution.db")
AUDIT_LOG_PATH = os.path.join(HOME, "logs/audit_3color.log")

# 敏感关键词 - 触发权重加倍
SENSITIVE_KEYWORDS = [
    "确认码", "DNA", "GPG", "身份", "签名",
    "核心算法", "密钥", "权限", "安全",
    "人民", "弱势", "隐私", "权利"
]


# ═════════════════════════════════════════════════════════════════════════════
# 集成数据结构
# ═════════════════════════════════════════════════════════════════════════════

@dataclass
class ContaminationEvent:
    """污染事件（写入KFPP记错本）"""
    timestamp: str                      # ISO 8601
    assertion_id: int
    assertion_content: str
    truth_score: float
    issue_type: str                     # "格式污染" | "编造断言" | "数值错误"
    source_ai: str                      # 来源AI的标识
    audit_dna: str                      # 审计的DNA签章
    remediation_required: bool = True

    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "assertion_id": self.assertion_id,
            "assertion_content": self.assertion_content,
            "truth_score": self.truth_score,
            "issue_type": self.issue_type,
            "source_ai": self.source_ai,
            "audit_dna": self.audit_dna,
            "remediation_required": self.remediation_required,
        }


# ═════════════════════════════════════════════════════════════════════════════
# 集成接口 1: 天道系统对接（KFPP记错本写入）
# ═════════════════════════════════════════════════════════════════════════════

class TiandaoIntegration:
    """与天道系统v1.3的对接 - 自动写入污染事件"""

    @staticmethod
    def ensure_db_ready() -> bool:
        """确保KFPP数据库已初始化"""
        try:
            os.makedirs(os.path.dirname(KFPP_DB), exist_ok=True)
            con = sqlite3.connect(KFPP_DB)
            cur = con.cursor()

            # 检查表是否存在
            cur.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name='contamination_events'
            """)

            if not cur.fetchone():
                # 创建表
                cur.execute("""
                    CREATE TABLE contamination_events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        assertion_id INTEGER,
                        assertion_content TEXT,
                        truth_score REAL,
                        issue_type TEXT,
                        source_ai TEXT,
                        audit_dna TEXT,
                        remediation_required BOOLEAN,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                con.commit()

            con.close()
            return True
        except Exception as e:
            print(f"🔴 KFPP库初始化失败: {e}")
            return False

    @staticmethod
    def record_contamination(
        report: AuditReport,
        source_ai: str,
        audit_dna: str
    ) -> Tuple[bool, str]:
        """记录污染事件到KFPP记错本"""

        if not TiandaoIntegration.ensure_db_ready():
            return False, "数据库初始化失败"

        try:
            con = sqlite3.connect(KFPP_DB)
            cur = con.cursor()

            recorded_count = 0

            # 记录所有错误断言
            for assertion in report.get_error_assertions():
                issue_type = "格式污染" if assertion.truth_component.F == 0 else "编造断言"

                event = ContaminationEvent(
                    timestamp=datetime.now().isoformat(),
                    assertion_id=assertion.id,
                    assertion_content=assertion.content,
                    truth_score=assertion.truth_score,
                    issue_type=issue_type,
                    source_ai=source_ai,
                    audit_dna=audit_dna,
                    remediation_required=True
                )

                cur.execute("""
                    INSERT INTO contamination_events
                    (timestamp, assertion_id, assertion_content, truth_score,
                     issue_type, source_ai, audit_dna, remediation_required)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    event.timestamp,
                    event.assertion_id,
                    event.assertion_content,
                    event.truth_score,
                    event.issue_type,
                    event.source_ai,
                    event.audit_dna,
                    event.remediation_required
                ))

                recorded_count += 1

            con.commit()
            con.close()

            return True, f"已记录 {recorded_count} 条污染事件"

        except Exception as e:
            return False, f"写入失败: {e}"


# ═════════════════════════════════════════════════════════════════════════════
# 集成接口 2: P72·龍盾对接（触发审计流程）
# ═════════════════════════════════════════════════════════════════════════════

class ShieldIntegration:
    """与P72·龍盾的对接 - 五态情绪触发审计"""

    EMOTION_STATES = {
        "calm": 0.0,         # 平静 - 无需审计
        "alert": 0.3,        # 警觉 - 轻度审计
        "vigilant": 0.6,     # 警惕 - 中度审计
        "suspicious": 0.85,  # 怀疑 - 重度审计
        "alarm": 1.0,        # 警报 - 立即熔断审计
    }

    @staticmethod
    def trigger_audit(
        current_emotion: str,
        response_length: int,
        response: str
    ) -> Tuple[str, float]:
        """
        根据P72情绪状态决定是否触发审计及严格程度

        返回: (触发级别, 严格度 [0-1])
        """
        if current_emotion not in ShieldIntegration.EMOTION_STATES:
            current_emotion = "calm"

        severity = ShieldIntegration.EMOTION_STATES[current_emotion]

        # 长回复自动升级严格度
        if response_length > 5000:
            severity = min(1.0, severity + 0.15)

        if severity < 0.1:
            return "SKIP", 0.0       # 不审计
        elif severity < 0.4:
            return "LIGHT", 0.3      # 轻度（采样审计）
        elif severity < 0.7:
            return "MEDIUM", 0.6     # 中度（全审计）
        elif severity < 1.0:
            return "HEAVY", 0.85     # 重度（严格审计）
        else:
            return "ALARM", 1.0      # 警报（立即熔断）

    @staticmethod
    def get_audit_sample_rate(severity: float) -> float:
        """根据严格度返回采样率"""
        if severity == 0.0:
            return 0.0        # 不审计
        elif severity <= 0.3:
            return 0.2        # 20% 采样
        elif severity <= 0.6:
            return 0.5        # 50% 采样
        elif severity <= 0.85:
            return 1.0        # 100% 审计
        else:
            return 1.0        # 立即熔断


# ═════════════════════════════════════════════════════════════════════════════
# 集成接口 3: 权重系统对接（敏感性加权）
# ═════════════════════════════════════════════════════════════════════════════

class WeightSystemIntegration:
    """与九层权重体系的对接 - 敏感断言权重加倍"""

    @staticmethod
    def adjust_assertion_weight(
        assertion: Assertion,
        context_sensitivity: float = 1.0
    ) -> int:
        """
        根据上下文敏感性调整断言权重

        返回: 调整后的权重
        """
        base_weight = assertion.importance_weight

        # 检查敏感关键词
        is_sensitive = any(
            keyword in assertion.content
            for keyword in SENSITIVE_KEYWORDS
        )

        # 应用敏感性倍数
        if is_sensitive:
            adjusted = int(base_weight * (1.0 + context_sensitivity))
        else:
            adjusted = base_weight

        return max(1, min(5, adjusted))  # 限制在 [1, 5]

    @staticmethod
    def calculate_weighted_sensitivity(
        assertions: List[Assertion],
        context_sensitivity: float = 1.0
    ) -> float:
        """计算加权后的敏感度分数"""
        total_weight = 0
        sensitive_count = 0

        for assertion in assertions:
            adjusted_weight = WeightSystemIntegration.adjust_assertion_weight(
                assertion, context_sensitivity
            )
            total_weight += adjusted_weight

            if any(keyword in assertion.content for keyword in SENSITIVE_KEYWORDS):
                sensitive_count += adjusted_weight

        if total_weight == 0:
            return 0.0

        return sensitive_count / total_weight


# ═════════════════════════════════════════════════════════════════════════════
# 集成接口 4: DNA·确认码·GPG验证链
# ═════════════════════════════════════════════════════════════════════════════

class IdentityVerificationIntegration:
    """与DNA/确认码/GPG的验证链对接"""

    GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
    CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
    SEAL_CODE = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"

    @staticmethod
    def verify_identity_chain(response: str) -> Tuple[bool, str, Dict]:
        """
        完整的身份验证链检查

        返回: (通过, 消息, 详情)
        """
        checks = {
            "dna_present": False,
            "confirm_intact": False,
            "seal_intact": False,
            "no_injection": True,
            "no_truncation": True,
        }

        # 检查DNA追溯码
        if "#龍芯⚡️" in response:
            checks["dna_present"] = True
        else:
            checks["dna_present"] = False

        # 检查CONFIRM码完整性
        if IdentityVerificationIntegration.CONFIRM_CODE in response:
            checks["confirm_intact"] = True
        elif "#CONFIRM" in response:
            checks["confirm_intact"] = False  # 被篡改

        # 检查SEAL码完整性
        if IdentityVerificationIntegration.SEAL_CODE in response:
            checks["seal_intact"] = True
        elif "#ZHUGEXIN" in response:
            checks["seal_intact"] = False  # 被篡改

        # 检查系统注入标记
        injection_markers = ["<|im_message|>", "<refer>", "<final>", "<|", "|>"]
        checks["no_injection"] = not any(m in response for m in injection_markers)

        # 检查截断标记
        checks["no_truncation"] = not response.endswith("...")

        # 综合判定
        all_passed = all(checks.values())

        if all_passed:
            return True, "身份验证链完整", checks
        else:
            failed = [k for k, v in checks.items() if not v]
            return False, f"身份验证失败: {failed}", checks


# ═════════════════════════════════════════════════════════════════════════════
# 集成引擎：完整审计流程
# ═════════════════════════════════════════════════════════════════════════════

class LonghunAuditEngine:
    """龍魂系统的完整三色审计引擎"""

    def __init__(self, source_ai: str = "unknown"):
        self.source_ai = source_ai
        self.audit_dna = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-AUDIT-INTEGRATION-v1.0"

    def execute_full_audit(
        self,
        response: str,
        assertions_data: List[Dict],
        current_shield_emotion: str = "calm",
        context_sensitivity: float = 1.0
    ) -> Dict:
        """
        执行完整的龍魂三色审计流程

        流程：
        1. 身份验证链检查 (DNA/CONFIRM/SEAL)
        2. P72·龍盾触发判定
        3. 三色审计执行
        4. 权重系统调整
        5. 污染事件记录
        """

        # 第一步：身份验证
        identity_ok, identity_msg, identity_details = (
            IdentityVerificationIntegration.verify_identity_chain(response)
        )

        # 第二步：P72触发判定
        trigger_level, severity = ShieldIntegration.trigger_audit(
            current_shield_emotion,
            len(response),
            response
        )

        if trigger_level == "SKIP":
            return {
                "status": "SKIP",
                "message": "P72未触发审计",
                "identity_ok": identity_ok,
            }

        # 第三步：执行审计
        report = ThreeColorAuditEngine.audit_simple_response(
            response=response[:50] + "..." if len(response) > 50 else response,
            assertions_data=assertions_data
        )

        # 第四步：调整权重（敏感性）
        for assertion in report.assertions:
            original_weight = assertion.importance_weight
            adjusted_weight = WeightSystemIntegration.adjust_assertion_weight(
                assertion, context_sensitivity
            )
            if original_weight != adjusted_weight:
                assertion.importance_weight = adjusted_weight

        # 重新计算加权总分
        report.total_truth_score = report.calculate_weighted_total()

        # 重新判定颜色
        if report.veto_triggered:
            report.judgment = JudgmentColor.RED
        elif report.total_truth_score >= 0.85:
            report.judgment = JudgmentColor.GREEN
        elif report.total_truth_score >= 0.60:
            report.judgment = JudgmentColor.YELLOW
        else:
            report.judgment = JudgmentColor.RED

        # 第五步：记录污染事件
        if report.judgment == JudgmentColor.RED or report.judgment == JudgmentColor.YELLOW:
            record_ok, record_msg = TiandaoIntegration.record_contamination(
                report, self.source_ai, self.audit_dna
            )
        else:
            record_ok, record_msg = True, "无污染事件"

        return {
            "status": "COMPLETED",
            "trigger_level": trigger_level,
            "severity": severity,
            "identity_ok": identity_ok,
            "identity_details": identity_details,
            "audit_report": report.to_json(),
            "judgment": report.judgment.value,
            "total_score": report.total_truth_score,
            "contamination_recorded": record_ok,
            "contamination_message": record_msg,
            "audit_dna": self.audit_dna,
        }

    def generate_integrated_report(self, audit_result: Dict) -> str:
        """生成集成后的审计报告"""
        lines = []
        lines.append("═" * 80)
        lines.append("🟢 龍魂三色审计·集成报告 v1.0")
        lines.append("═" * 80)
        lines.append("")

        lines.append(f"【执行时间】{datetime.now().strftime('%Y-%m-%d %H:%M:%S CST')}")
        lines.append(f"【来源AI】{self.source_ai}")
        lines.append(f"【审计DNA】{audit_result['audit_dna']}")
        lines.append("")

        lines.append("【身份验证链】")
        if audit_result["identity_ok"]:
            lines.append("  🟢 身份验证通过")
        else:
            lines.append("  🔴 身份验证失败")
            for check, status in audit_result["identity_details"].items():
                lines.append(f"    {check}: {'✅' if status else '❌'}")
        lines.append("")

        lines.append("【P72·龍盾触发】")
        lines.append(f"  触发级别: {audit_result['trigger_level']}")
        lines.append(f"  严格程度: {audit_result['severity']:.1%}")
        lines.append("")

        if audit_result["status"] == "COMPLETED":
            lines.append("【三色审计结果】")
            lines.append(f"  判定: {audit_result['judgment']}")
            lines.append(f"  总分: {audit_result['total_score']:.4f}")
            lines.append("")

            lines.append("【天道系统对接】")
            lines.append(f"  污染事件记录: {'✅' if audit_result['contamination_recorded'] else '❌'}")
            lines.append(f"  消息: {audit_result['contamination_message']}")
        else:
            lines.append("【审计状态】")
            lines.append(f"  {audit_result['status']}")

        lines.append("")
        lines.append("═" * 80)

        return "\n".join(lines)


# ═════════════════════════════════════════════════════════════════════════════
# 演示
# ═════════════════════════════════════════════════════════════════════════════

def demo_full_integration():
    """演示完整集成流程"""
    print("=" * 80)
    print("🧮 龍魂三色审计·集成演示 v1.0")
    print("=" * 80)
    print()

    # 初始化引擎
    engine = LonghunAuditEngine(source_ai="Claude-Assistant")

    # 示例断言
    assertions_data = [
        {"content": "RM是势利眼审判官", "type": "logical", "M": 1.0, "V": 1.0, "F": 1},
        {"content": "龍魂系统核心算法已验证", "type": "formula", "M": 1.0, "V": 1.0, "F": 1},
        {"content": "确认码：#CONFIRM<refer>9622...", "type": "identity", "M": 0.0, "V": 0.0, "F": 0},  # 一票否决
    ]

    # 示例响应
    response = """
    龍魂系统的身份验证链完整。
    DNA: #龍芯⚡️2026-06-08-DEMO
    CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
    """

    # 执行完整审计
    result = engine.execute_full_audit(
        response=response,
        assertions_data=assertions_data,
        current_shield_emotion="vigilant",
        context_sensitivity=1.5
    )

    # 输出报告
    print(engine.generate_integrated_report(result))
    print()

    # JSON输出
    print("【JSON结果】")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    demo_full_integration()
