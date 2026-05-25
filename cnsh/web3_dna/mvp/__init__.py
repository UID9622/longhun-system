#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·Web3-DNA MVP落地链系统
§39 MVP Runtime Landing Chain: 11-Step Protocol + 3-File System
"""

from .mvp_landing_chain import (
    MVPLandingChain,
    MVPTransaction,
    TransactionStep,
    StepResult,
)

from .mvp_dna_memory_asset import (
    DNAMemoryAssetPricingEngine,
    DNAMemoryAsset,
    PricingResult,
    MemoryQualityScorer,
)

from .mvp_payment_gateway import (
    PaymentGateway,
    PaymentRequest,
    PaymentTransaction,
    KYCAMLEngine,
    RiskAssessmentEngine,
)

__all__ = [
    # Landing Chain
    "MVPLandingChain",
    "MVPTransaction",
    "TransactionStep",
    "StepResult",
    # DNA Memory Asset
    "DNAMemoryAssetPricingEngine",
    "DNAMemoryAsset",
    "PricingResult",
    "MemoryQualityScorer",
    # Payment Gateway
    "PaymentGateway",
    "PaymentRequest",
    "PaymentTransaction",
    "KYCAMLEngine",
    "RiskAssessmentEngine",
]
