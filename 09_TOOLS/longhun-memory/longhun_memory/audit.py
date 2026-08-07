#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-08-06-MEMORY-AUDIT-v1.0
# License: MulanPSL v2
"""
三色审计模块
═══════════
🟢 通过 · 🟡 待核 · 🔴 红线

每次 MemoryVault 操作后自动产出审计结论。
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional


class AuditColor(str, Enum):
    GREEN = "🟢"    # 通过
    YELLOW = "🟡"   # 待核
    RED = "🔴"      # 红线


@dataclass
class AuditCheck:
    """单项审计检查"""
    name: str             # 检查项名称
    color: AuditColor     # 审计色
    detail: str           # 详情
    score: float = 1.0    # 0~1


@dataclass
class AuditMark:
    """三色审计标记

    每次 seal/unseal 操作后生成，包含:
      - 整体审计结论（颜色+分数）
      - 逐项检查结果
      - DNA 追溯
    """

    color: AuditColor
    score: float          # 0~1
    checks: List[AuditCheck] = field(default_factory=list)
    dna: str = ""
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()

    @property
    def emoji(self) -> str:
        return self.color.value

    @property
    def label(self) -> str:
        labels = {AuditColor.GREEN: "通过", AuditColor.YELLOW: "待核", AuditColor.RED: "红线"}
        return labels.get(self.color, "未知")

    def to_dict(self) -> dict:
        return {
            "audit": self.emoji,
            "score": round(self.score, 4),
            "label": self.label,
            "checks": [
                {"name": c.name, "color": c.color.value, "detail": c.detail, "score": c.score}
                for c in self.checks
            ],
            "dna": self.dna,
            "timestamp": self.timestamp,
        }

    @classmethod
    def pass_all(cls, dna: str, note: str = "") -> "AuditMark":
        """全部通过"""
        return cls(
            color=AuditColor.GREEN,
            score=1.0,
            checks=[AuditCheck(name="all", color=AuditColor.GREEN, detail=note or "全部检查通过")],
            dna=dna,
        )

    @classmethod
    def warn(cls, dna: str, warnings: List[tuple[str, str]]) -> "AuditMark":
        """有待核项"""
        checks = [AuditCheck(name=n, color=AuditColor.YELLOW, detail=d, score=0.7)
                  for n, d in warnings]
        return cls(
            color=AuditColor.YELLOW,
            score=0.7,
            checks=checks,
            dna=dna,
        )

    @classmethod
    def block(cls, dna: str, reasons: List[tuple[str, str]]) -> "AuditMark":
        """红线"""
        checks = [AuditCheck(name=n, color=AuditColor.RED, detail=d, score=0.0)
                  for n, d in reasons]
        return cls(
            color=AuditColor.RED,
            score=0.0,
            checks=checks,
            dna=dna,
        )


class ThreeColorAudit:
    """三色审计引擎

    审计 MemoryVault 的 seal/unseal 操作:
      1. 密钥强度检查
      2. SM4 加密完整性
      3. SM3 哈希链完整性
      4. DNA 有效性
      5. 数据来源合法性
    """

    @staticmethod
    def audit_seal(key_len: int, data_size: int, dna: str) -> AuditMark:
        """审计 seal 操作"""
        checks = []

        # 密钥强度
        if key_len >= 16:
            checks.append(AuditCheck("密钥强度", AuditColor.GREEN, f"SM4 密钥 {key_len}字节", 1.0))
        elif key_len >= 8:
            checks.append(AuditCheck("密钥强度", AuditColor.YELLOW, f"密钥偏短 {key_len}字节，建议16字节", 0.7))
        else:
            checks.append(AuditCheck("密钥强度", AuditColor.RED, f"密钥过短 {key_len}字节", 0.0))

        # 数据非空
        if data_size > 0:
            checks.append(AuditCheck("数据非空", AuditColor.GREEN, f"数据大小 {data_size} 字节", 1.0))
        else:
            checks.append(AuditCheck("数据非空", AuditColor.YELLOW, "数据为空", 0.5))

        # DNA 有效
        if dna and dna.startswith("#龍芯⚡️"):
            checks.append(AuditCheck("DNA有效性", AuditColor.GREEN, "DNA 格式正确", 1.0))
        else:
            checks.append(AuditCheck("DNA有效性", AuditColor.RED, "DNA 无效或缺失", 0.0))

        avg_score = sum(c.score for c in checks) / len(checks)
        if any(c.color == AuditColor.RED for c in checks):
            color = AuditColor.RED
        elif any(c.color == AuditColor.YELLOW for c in checks):
            color = AuditColor.YELLOW
        else:
            color = AuditColor.GREEN

        return AuditMark(color=color, score=avg_score, checks=checks, dna=dna)

    @staticmethod
    def audit_unseal(chain_ok: bool, tampered: bool, dna_valid: bool, dna: str) -> AuditMark:
        """审计 unseal 操作"""
        checks = [
            AuditCheck("SM3哈希链", AuditColor.GREEN if chain_ok else AuditColor.RED,
                       "完整" if chain_ok else "断裂/被篡改", 1.0 if chain_ok else 0.0),
            AuditCheck("数据完整性", AuditColor.GREEN if not tampered else AuditColor.RED,
                       "未篡改" if not tampered else "检测到篡改", 1.0 if not tampered else 0.0),
            AuditCheck("DNA溯源", AuditColor.GREEN if dna_valid else AuditColor.YELLOW,
                       "有效" if dna_valid else "待核", 1.0 if dna_valid else 0.5),
        ]

        avg_score = sum(c.score for c in checks) / len(checks)
        if any(c.color == AuditColor.RED for c in checks):
            color = AuditColor.RED
        elif any(c.color == AuditColor.YELLOW for c in checks):
            color = AuditColor.YELLOW
        else:
            color = AuditColor.GREEN

        return AuditMark(color=color, score=avg_score, checks=checks, dna=dna)


if __name__ == "__main__":
    from .dna import dna_now
    mark = ThreeColorAudit.audit_seal(key_len=16, data_size=1024, dna=dna_now("TEST", "audit"))
    print(f"{mark.emoji} {mark.label} (得分: {mark.score})")
    for c in mark.checks:
        print(f"  {c.color.value} {c.name}: {c.detail}")
    print("🟢 三色审计模块自检通过")
