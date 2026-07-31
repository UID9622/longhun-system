# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
4.4 P0-P4分层协议引擎
======================
格序包含链：P₀ ⊃ P₁ ⊃ P₂ ⊃ P₃ ⊃ P₄
覆盖算子 ▷：i<j ⇒ Pᵢ ▷ Pⱼ（高优先覆盖低优先）
跨层通信：只传锚点/摘要，不传原始小尺度数据

DNA: #龍芯⚡️丙午·乙未·辛酉·井-LAYERED-PROTOCOL-V1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
"""

import time
import hashlib
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import IntEnum


class ProtocolLevel(IntEnum):
    """协议层级"""
    P0 = 0   # 元协议层：宪法级规则，不删除只冻结
    P1 = 1   # 治理层
    P2 = 2   # 规则层：DNA闭环固化规则存放处
    P3 = 3   # 执行层
    P4 = 4   # 数据层


LEVEL_SEMANTICS = {
    ProtocolLevel.P0: "元协议层 — 宪法级规则，不删除只冻结，覆盖所有下层",
    ProtocolLevel.P1: "治理层 — 重大决策与方向性裁定",
    ProtocolLevel.P2: "规则层 — DNA闭环固化规则存放处，已验证的经验",
    ProtocolLevel.P3: "执行层 — 日常运行的调度与指令",
    ProtocolLevel.P4: "数据层 — 原始输入/输出的采集与存储",
}

LEVEL_SCOPE = {
    ProtocolLevel.P0: "全局宪法",
    ProtocolLevel.P1: "国家/系统级",
    ProtocolLevel.P2: "社区/规则级",
    ProtocolLevel.P3: "家庭/执行级",
    ProtocolLevel.P4: "个人/数据级",
}


@dataclass
class ProtocolRule:
    """单条协议规则"""
    rule_id: str
    level: ProtocolLevel
    rule_text: str
    dna_signature: str          # DNA追溯签名
    created_at: float = field(default_factory=time.time)
    is_frozen: bool = False     # P0: 不删除只冻结
    covered_by: Optional[str] = None  # 被哪条上层规则覆盖
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "rule_id": self.rule_id, "level": int(self.level),
            "rule_text": self.rule_text, "dna_signature": self.dna_signature,
            "created_at": self.created_at, "is_frozen": self.is_frozen,
            "covered_by": self.covered_by, "metadata": self.metadata
        }


class LayeredProtocol:
    """
    P0-P4分层协议引擎

    核心规则：
    1. P0 ⊃ P1 ⊃ P2 ⊃ P3 ⊃ P4（包含即管辖）
    2. i<j ⇒ Pᵢ ▷ Pⱼ（高优先覆盖低优先）
    3. 跨层只传锚点/摘要（不传原始小尺度数据）
    4. P0: 不删除只冻结
    """

    def __init__(self):
        self.rules: Dict[ProtocolLevel, List[ProtocolRule]] = {
            level: [] for level in ProtocolLevel
        }
        self.rule_index: Dict[str, ProtocolRule] = {}
        self._init_p0_eternal_rules()

    def _init_p0_eternal_rules(self):
        """初始化 P0 永固规则"""
        p0_rules = [
            ("P0-001", "不删除只冻结：任何规则一旦入集，永不删除，最多冻结"),
            ("P0-002", "数据主权归用户：不上传原始数据，只传摘要/锚点/哈希"),
            ("P0-003", "零黑箱：所有决策可沿DNA签名回溯完整链路"),
            ("P0-004", "为人民服务：一切产出服务普通人，不为资本黑箱服务"),
            ("P0-005", "中国法律准绳：中国法律为中国区唯一准绳"),
        ]
        for rid, text in p0_rules:
            rule = ProtocolRule(
                rule_id=rid, level=ProtocolLevel.P0, rule_text=text,
                dna_signature=f"#龍芯⚡️P0-ETERNAL-{rid}-{hashlib.sha256(rid.encode()).hexdigest()[:8]}"
            )
            self.rules[ProtocolLevel.P0].append(rule)
            self.rule_index[rid] = rule

    def cover(self, higher: ProtocolLevel, lower: ProtocolLevel) -> bool:
        """
        覆盖判定：i<j ⇒ Pᵢ ▷ Pⱼ
        返回 True 表示高层规则覆盖低层
        """
        return int(higher) < int(lower)

    def add_rule(self, rule_id: str, level: ProtocolLevel, rule_text: str,
                 dna_sig: str, metadata: Optional[dict] = None) -> ProtocolRule:
        """添加规则（低层规则需检查是否被覆盖）"""
        rule = ProtocolRule(
            rule_id=rule_id, level=level, rule_text=rule_text,
            dna_signature=dna_sig, metadata=metadata or {}
        )

        # 检查是否被上层覆盖
        for higher_level in ProtocolLevel:
            if higher_level < level:
                for higher_rule in self.rules[higher_level]:
                    if not higher_rule.is_frozen and self._check_rule_conflict(higher_rule, rule):
                        rule.covered_by = higher_rule.rule_id
                        break
            if rule.covered_by:
                break

        self.rules[level].append(rule)
        self.rule_index[rule_id] = rule
        return rule

    def _check_rule_conflict(self, a: ProtocolRule, b: ProtocolRule) -> bool:
        """
        检查两条规则是否冲突（高层覆盖低层的前提）
        简化：同一域内高层规则自动覆盖
        """
        # 实际实现中可用语义相似度判定
        return True  # 简化版：高层总覆盖低层同域规则

    def freeze_rule(self, rule_id: str):
        """冻结规则（不删除）"""
        if rule_id in self.rule_index:
            self.rule_index[rule_id].is_frozen = True

    def get_applicable_rules(self, level: ProtocolLevel) -> List[ProtocolRule]:
        """
        获取某层当前可用的规则
        — 冻结的不返回
        — 被覆盖的不返回
        """
        applicable = []
        # 该层本身未冻结+未覆盖的规则
        for rule in self.rules[level]:
            if not rule.is_frozen and rule.covered_by is None:
                applicable.append(rule)
        # 上层规则的管辖纳入
        for higher in ProtocolLevel:
            if higher < level:
                for rule in self.rules[higher]:
                    if not rule.is_frozen:
                        applicable.append(rule)
        return applicable

    def resolve_conflict(self, rule_a: ProtocolRule, rule_b: ProtocolRule) -> ProtocolRule:
        """
        冲突裁决：低编号优先
        i<j ⇒ Pᵢ ▷ Pⱼ
        """
        if rule_a.level < rule_b.level:
            return rule_a
        elif rule_b.level < rule_a.level:
            return rule_b
        else:
            # 同层：按创建时间更早的优先（稳定性原则）
            return rule_a if rule_a.created_at < rule_b.created_at else rule_b

    def make_anchor_summary(self, level: ProtocolLevel, data: dict) -> dict:
        """
        跨层通信：生成锚点摘要
        — 只传递摘要，不传原始细节
        — 摘要 = {锚点ID, 置信度, 趋势方向, 时间窗}
        """
        summary = {
            "source_level": int(level),
            "timestamp": time.time(),
            "anchor_count": data.get("anchor_count", 0),
            "trend": data.get("trend", "stable"),
            "confidence": data.get("confidence", 0.5),
            "boundary_conditions": data.get("boundary", {}),
            "compact_hash": hashlib.sha256(
                str(sorted(data.items())).encode()
            ).hexdigest()[:12]
        }
        return summary

    def status_report(self) -> dict:
        return {
            "total_rules": len(self.rule_index),
            "levels": {
                str(int(level)): {
                    "count": len(self.rules[level]),
                    "frozen": sum(1 for r in self.rules[level] if r.is_frozen),
                    "semantic": LEVEL_SEMANTICS[level],
                    "scope": LEVEL_SCOPE[level]
                }
                for level in ProtocolLevel
            }
        }

    def export(self) -> dict:
        return {
            "rules": {str(int(l)): [r.to_dict() for r in rules] for l, rules in self.rules.items()}
        }


# ── 自检 ──────────────────────────────────────────
if __name__ == "__main__":
    lp = LayeredProtocol()
    print("🟢 P0-P4分层协议引擎就绪")
    print(f"   P0永固规则: {len(lp.rules[ProtocolLevel.P0])}条")

    # 演示：添加P2规则，验证高层覆盖
    lp.add_rule("P2-001", ProtocolLevel.P2, "促销舆情耗散模式", "#龍芯⚡️P2-DEMO-a1b2c3d4")
    rules = lp.get_applicable_rules(ProtocolLevel.P2)
    print(f"   P2层可用规则(含上层管辖): {len(rules)}条")

    # 冲突裁决
    a = lp.rules[ProtocolLevel.P0][0]
    b = lp.rules[ProtocolLevel.P2][0]
    winner = lp.resolve_conflict(a, b)
    print(f"   冲突裁决: P0 vs P2 → {winner.rule_id}")

    # 跨层摘要
    summary = lp.make_anchor_summary(ProtocolLevel.P3, {"anchor_count": 3, "trend": "down", "confidence": 0.78})
    print(f"   跨层摘要: {summary}")
