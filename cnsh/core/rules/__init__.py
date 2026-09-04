#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
║     龍魂规则引擎 / LongHun Rule Engine (CNSH)                    ║
║                                                                  ║
║  P1-2 规则引擎·业务规则执行器                                    ║
║                                                                  ║
║  DNA:#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-RULE-ENGINE-SYSTEM-FILE1-v1.0                ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                 ║
║                                                                  ║
║  理论指导: 曾仕强·道德经第三十三章 (知人者智·自知者明)            ║
║  责任: UID9622·不免责                                            ║
║  状态: 🟢 MAIN·可公开                                            ║
╚══════════════════════════════════════════════════════════════════╝

龍魂规则引擎包结构：
  ├── rule_node.py      - 规则数据模型 (Rule/RuleType/RuleStatus)
  ├── rule_engine.py    - 规则引擎核心 (注册/查找/执行/评估)
  ├── rule_executor.py  - 规则执行器 (条件评估/动作执行/审计)
  ├── builtin_rules.py  - 内置规则库 (三色审计/一票否决等)
  └── README.md         - 完整使用文档

使用示例：
  from cnsh_core.rules import get_rule_engine, Rule, RuleType

  engine = get_rule_engine()
  result = engine.execute_rule("RULE-AUDIT-001", {"score": 85})
"""

from .rule_node import (
    Rule,
    RuleType,
    RuleStatus,
    RulePriority,
    selftest_rule_node
)

from .rule_engine import (
    RuleEngine,
    get_rule_engine,
    reset_rule_engine
)

from .rule_executor import (
    RuleExecutor
)

__version__ = "1.0.0"
__author__ = "UID9622 · 诸葛鑫 · 龍芯北辰"
__dna__ = "#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-RULE-ENGINE-SYSTEM-v1.0"

__all__ = [
    # Rule model
    'Rule',
    'RuleType',
    'RuleStatus',
    'RulePriority',
    'selftest_rule_node',
    # Rule engine
    'RuleEngine',
    'get_rule_engine',
    'reset_rule_engine',
    # Rule executor
    'RuleExecutor',
]
