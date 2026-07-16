#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║  DNA: #龍芯⚡️2026-06-19-CNSH-CHINA-COMPLIANCE-v1.0              ║
║  中国法律合规检查系统 — 龍魂体系 · 合规智脑                        ║
║  China Legal Compliance System — Dragon Soul Architecture           ║
╚══════════════════════════════════════════════════════════════════════╝

【君子协议】本系统仅用于中国法律合规自检，不构成法律意见。
【Gentleman's Agreement】For self-checking PRC laws only; not legal advice.

覆盖法律：
  1. 《个人信息保护法》（个保法）- Personal Information Protection Law (PIPL)
  2. 《数据安全法》- Data Security Law (DSL)
  3. 《电子商务法》- E-Commerce Law
  4. 《网络安全法》- Cybersecurity Law (CSL)
  5. 《e-CNY（数字人民币）相关规定》- e-CNY Regulations

三色审计：🟢 合规 | 🟡 警示 | 🔴 违规
"""

from .个保法检查器 import 个保法检查器
from .数安法检查器 import 数安法检查器
from .电商法检查器 import 电商法检查器
from .网安法检查器 import 网安法检查器
from .eCNY合规检查器 import eCNY合规检查器
from .中国合规矩阵 import 中国合规矩阵, 合规报告

__version__ = "1.0.0"
__dna__ = "#龍芯⚡️2026-06-19-CNSH-CHINA-COMPLIANCE-v1.0"
__author__ = "龍魂体系 · CNSH"

__all__ = [
    "中国合规矩阵",
    "合规报告",
    "个保法检查器",
    "数安法检查器",
    "电商法检查器",
    "网安法检查器",
    "eCNY合规检查器",
]
