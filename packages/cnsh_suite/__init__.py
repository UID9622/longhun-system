#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH 套件 · DeepSeek Harness 插件集（Python 完整实现）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-CNSH-SUITE-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

能力清单:
  - generate_dna     : DNA追溯码生成
  - tricolor_audit   : 三色审计
  - run_cnsh         : CNSH脚本执行
  - tricolor_gate    : 审计审批门
  - historian        : 史官全链路记录
  - persona_router   : 人格路由

安装:
  pip install -e .

使用:
  from cnsh_suite import CNSHSuite
  suite = CNSHSuite()
  result = suite.execute("生成DNA: 我的文档")
"""

__version__ = "1.0.0"
__author__ = "诸葛鑫 · UID9622"

from .core import CNSHSuite, CNSHEngine, CNSHError, CNSHErrorCode
from .tools import DNAGenerator, TricolorAuditor, CNSHExecutor
from .hooks import TricolorGate
from .events import Historian
from .agents import PersonaRouter
from .cli import main

__all__ = [
    "CNSHSuite",
    "CNSHEngine",
    "CNSHError",
    "CNSHErrorCode",
    "DNAGenerator",
    "TricolorAuditor",
    "CNSHExecutor",
    "TricolorGate",
    "Historian",
    "PersonaRouter",
    "main"
]
