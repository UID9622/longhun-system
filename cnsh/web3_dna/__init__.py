#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·Web3-DNA 系统 v1.0
Web3-DNA Memory Sovereignty Trading Algorithm

DNA: #龍芯⚡️2026-05-25-WEB3-DNA-SYSTEM-v1.0
UID: 9622
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

完整的Web3-DNA系统导入入口
- core: 基础引擎层（五行合规 + 64卦审计）
- mvp: MVP落地链（11步 + 3件套支付系统）
- 未来: §37 §38 的数字永生与生态准入

本地执行·完全自主·永不外送·可恢复·可追溯

理论指导: 曾仕强老师（永恒显示）
献礼: 龍魂系统·永恒守护·中华文化传承
"""

from .core.wuxing_compliance_engine import (
    WuXingComplianceEngine,
    WuXingVector,
    ComplianceResult,
)

from .core.gua64_audit_engine import (
    Gua64AuditEngine,
    GuaAuditResult,
)

from .mvp.mvp_landing_chain import (
    MVPLandingChain,
    MVPTransaction,
    TransactionStep,
)

from .mvp.mvp_dna_memory_asset import (
    DNAMemoryAssetPricingEngine,
    DNAMemoryAsset,
    PricingResult,
)

from .mvp.mvp_payment_gateway import (
    PaymentGateway,
    PaymentRequest,
    PaymentTransaction,
)

__all__ = [
    # Core engines
    "WuXingComplianceEngine",
    "WuXingVector",
    "ComplianceResult",
    "Gua64AuditEngine",
    "GuaAuditResult",
    # MVP system
    "MVPLandingChain",
    "MVPTransaction",
    "TransactionStep",
    "DNAMemoryAssetPricingEngine",
    "DNAMemoryAsset",
    "PricingResult",
    "PaymentGateway",
    "PaymentRequest",
    "PaymentTransaction",
]

__version__ = "1.0.0"
__author__ = "UID9622 · 龍芯北辰 · 诸葛鑫"
__dna__ = "#龍芯⚡️2026-05-25-WEB3-DNA-SYSTEM-v1.0"
