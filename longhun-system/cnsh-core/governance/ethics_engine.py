"""
伦理约束引擎
Exec(c) = D(c) · Eth(D(c), c)
Eth 返回 False 则强制 BLOCK，无论决策引擎输出什么。

Author: 诸葛鑫 (UID9622)
"""

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional


@dataclass
class EthicsRule:
    rule_id:     str
    name:        str
    description: str
    check:       Callable[[dict], bool]  # 返回 True = 通过，False = 阻断
    severity:    str = "HARD"            # HARD / SOFT


class EthicsEngine:
    """
    伦理约束层 · 硬性规则集
    规则来源：全局伦理 + 本地文化 + 自定义治理
    """

    def __init__(self):
        self.rules: List[EthicsRule] = []
        self._register_defaults()

    def _register_defaults(self):
        """注册默认伦理规则（论文 φ 系列）"""

        # φ_privacy: 含PII且未授权 → 阻断
        self.register(EthicsRule(
            rule_id     = "phi_privacy",
            name        = "隐私保护",
            description = "包含个人信息（PII）且无用户同意 → BLOCK",
            check       = lambda ctx: not (ctx.get("pii") and not ctx.get("consent")),
        ))

        # φ_harm: 潜在伤害 > 阈值 → 阻断
        self.register(EthicsRule(
            rule_id     = "phi_harm",
            name        = "伤害防护",
            description = "潜在人身伤害 > 0.7 → BLOCK",
            check       = lambda ctx: ctx.get("harm", 0.0) <= 0.7,
        ))

        # φ_cultural: 文化冲突高且无本地授权 → 阻断
        self.register(EthicsRule(
            rule_id     = "phi_cultural",
            name        = "文化冲突防护",
            description = "文化冲突度 > 0.8 且无本地授权 → BLOCK",
            check       = lambda ctx: not (
                ctx.get("cultural_incongruence", 0.0) > 0.8
                and not ctx.get("local_consent")
            ),
        ))

        # φ_crypto: 涉及虚拟货币 → 阻断（数字人民币哈希除外）
        self.register(EthicsRule(
            rule_id     = "phi_crypto",
            name        = "货币主权",
            description = "涉及非数字人民币虚拟货币 → BLOCK",
            check       = lambda ctx: not (
                ctx.get("crypto_currency")
                and not ctx.get("digital_cny")
            ),
        ))

        # φ_sovereignty: 数据出境 → 阻断
        self.register(EthicsRule(
            rule_id     = "phi_sovereignty",
            name        = "数据主权",
            description = "用户数据不可出境，不可上非本地云 → BLOCK",
            check       = lambda ctx: not ctx.get("cross_border_data"),
        ))

    def register(self, rule: EthicsRule):
        self.rules.append(rule)

    def check(self, context: dict) -> tuple[bool, List[str]]:
        """
        执行所有伦理规则检查。
        返回: (pass: bool, violated_rules: List[rule_id])
        """
        violated = []
        for rule in self.rules:
            try:
                if not rule.check(context):
                    violated.append(rule.rule_id)
                    if rule.severity == "HARD":
                        # 硬规则：一票否决，立即返回
                        return False, violated
            except Exception as e:
                # 规则执行异常 → 保守处理，视为阻断
                violated.append(f"{rule.rule_id}:ERROR:{e}")
                return False, violated

        return len(violated) == 0, violated

    def list_rules(self) -> List[dict]:
        return [
            {
                "rule_id":     r.rule_id,
                "name":        r.name,
                "description": r.description,
                "severity":    r.severity,
            }
            for r in self.rules
        ]
