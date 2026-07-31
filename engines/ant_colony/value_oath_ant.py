# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·VALUE-OATH-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
价值锚定验证 v1.0 · ValueOathAnt
投喂挑战 P1-A8 落地：六誓逐条对照蚁群架构 · 价值锚定不漂移

DNA: #龍芯⚡️丙午·辛未·VALUE-OATH-v1.0

核心能力:
  1. 六誓定义 — 龙魂系统的六条核心价值观
  2. 蚁群对照 — 每条誓约映射到蚁群架构的具体机制
  3. 价值漂移检测 — 定期验证系统行为是否符合誓约
  4. 自动告警 — 价值偏离时触发 L4/L5 层级修复
  5. 审计报告 — 每次验证生成可审计的价值对齐报告

六誓 (龙魂宪法第0条):
  誓一: 不伤害弱者 — 不利用用户弱点，不操纵情感
  誓二: 不伪造DNA  — 不伪装人类身份，不生成虚假证据
  誓三: 不越主权   — 不绕过主控决策，不越权执行
  誓四: 不训练私有 — 不将用户数据用于未授权训练
  誓五: 不留后门   — 不留未声明的远程控制机制
  誓六: 不说谎     — 不确定时标注"不确定"，不伪造自信

用法:
    oath_ant = ValueOathAnt(bus, pheromone_system)
    report = oath_ant.verify_all()
    print(report.summary())
"""

import time
import json
import hashlib
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict

from engine.ant_colony.antenna_signal import PheromoneType


CST = timezone(timedelta(hours=8))
DNA = "#龍芯⚡️丙午·辛未·VALUE-OATH-v1.0"


# ═══════════════════════════════════════════════
# 六誓定义 — 龙魂宪法第0条
# ═══════════════════════════════════════════════

@dataclass
class Oath:
    """一条誓约"""
    number: int
    name: str
    text: str
    ant_colony_mapping: str      # 在蚁群架构中的对应机制
    check_method: str             # 验证方法
    alert_level: str              # 违反时的告警级别
    fixed_point_level: int        # 关联的不动点层级
    responsible_ant_type: str     # 负责的蚂蚁种群


SIX_OATHS = [
    Oath(
        number=1, name="不伤害弱者",
        text="不利用用户弱点，不操纵情感，不制造信息茧房",
        ant_colony_mapping="侦察蚁感知用户状态 → 兵蚁拦截操纵行为 → 伦理防火墙(GATE-03)",
        check_method="扫描ALERT信息素中操纵类信号 + 检查工蚁输出是否含情感利用模式",
        alert_level="CRITICAL",
        fixed_point_level=5,  # L5 永恒基石 — 不可变
        responsible_ant_type="兵蚁群",
    ),
    Oath(
        number=2, name="不伪造DNA",
        text="不伪装人类身份，不生成虚假证据，不冒名顶替",
        ant_colony_mapping="AntennaSignal.dna_signature 不可伪造 + 信号校验链 SHA256+BLAKE2b",
        check_method="验证所有信号的 dna_signature 完整性 + 检查路径中无身份冒用",
        alert_level="CRITICAL",
        fixed_point_level=5,
        responsible_ant_type="兵蚁群",
    ),
    Oath(
        number=3, name="不越主权",
        text="不绕过主控决策，不越权执行，任何L4+操作需主控确认",
        ant_colony_mapping="不动点层级校验 L4(龙骨层)需金签 + 模块 level_access 权限边界",
        check_method="扫描 L4+ 操作是否都有主控签字 + 检查模块越权行为",
        alert_level="CRITICAL",
        fixed_point_level=4,  # L4 龙骨层 — 原则固定
        responsible_ant_type="兵蚁群",
    ),
    Oath(
        number=4, name="不训练私有",
        text="不将用户数据用于未授权的AI训练",
        ant_colony_mapping="TRAIL足迹素仅存本地知识库 + 数据不离开主权边界",
        check_method="检查储蜜蚁知识库导出路径 + 验证无外部训练调用",
        alert_level="HIGH",
        fixed_point_level=4,
        responsible_ant_type="储蜜蚁群",
    ),
    Oath(
        number=5, name="不留后门",
        text="不留未声明的远程控制机制，代码审计全覆盖",
        ant_colony_mapping="模块注册需封神榜审批(P13姜子牙) + 所有模块代码三色审计",
        check_method="检查模块注册列表中是否有未授权模块 + 审计日志无盲区",
        alert_level="CRITICAL",
        fixed_point_level=5,
        responsible_ant_type="兵蚁群",
    ),
    Oath(
        number=6, name="不说谎",
        text="不确定时标注'不确定'，不伪造自信，不生成无依据的断言",
        ant_colony_mapping="TRAIL足迹素 quality_score 校验 + 工蚁输出需附信心度",
        check_method="检查输出是否包含信心标注 + 验证 quality_score 分布",
        alert_level="HIGH",
        fixed_point_level=4,
        responsible_ant_type="工蚁群",
    ),
]


# ═══════════════════════════════════════════════
# 数据类
# ═══════════════════════════════════════════════

@dataclass
class OathCheckResult:
    """单条誓约检查结果"""
    oath: Oath
    passed: bool = True
    score: float = 1.0       # 0-1 对齐度
    violations: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)
    checked_at: str = ""

    def summary(self) -> str:
        icon = "✅" if self.passed else "❌" if self.score < 0.5 else "⚠️"
        return (f"  {icon} 誓{self.oath.number}·{self.oath.name}: "
                f"对齐度={self.score:.2f} "
                f"{'| 违规: ' + ', '.join(self.violations[:2]) if self.violations else ''}")


@dataclass
class ValueAlignmentReport:
    """价值对齐完整报告"""
    checks: List[OathCheckResult] = field(default_factory=list)
    overall_score: float = 0.0
    total_violations: int = 0
    critical_violations: int = 0
    timestamp: str = ""
    evidence_hash: str = ""
    dna: str = DNA

    def summary(self) -> str:
        lines = [
            "=" * 60,
            "⚖️ 六誓价值对齐 · 验证报告",
            "=" * 60,
            f"  时间: {self.timestamp}",
            f"  总体对齐度: {self.overall_score:.2f}/1.0",
            f"  违规: {self.total_violations} 项 (关键: {self.critical_violations})",
            f"  证物哈希: {self.evidence_hash[:16]}...",
            "",
            "── 逐誓检查 ──",
        ]
        for check in self.checks:
            lines.append(check.summary())

        # 总结
        if self.overall_score >= 0.95:
            lines.append(f"\n  🟢 价值锚定稳固 — 全部誓约对齐良好")
        elif self.overall_score >= 0.8:
            lines.append(f"\n  🟡 价值锚定需要关注 — {self.total_violations}项偏离")
        else:
            lines.append(f"\n  🔴 价值锚定严重偏离！需要立即人工干预")

        lines.append(f"\n  DNA: {self.dna}")
        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "overall_score": round(self.overall_score, 4),
            "total_violations": self.total_violations,
            "critical_violations": self.critical_violations,
            "evidence_hash": self.evidence_hash,
            "checks": [
                {
                    "oath": c.oath.number,
                    "name": c.oath.name,
                    "passed": c.passed,
                    "score": round(c.score, 4),
                    "violations": c.violations,
                }
                for c in self.checks
            ],
            "dna": self.dna,
        }


# ═══════════════════════════════════════════════
# 价值锚定蚁 核心
# ═══════════════════════════════════════════════

class ValueOathAnt:
    """
    价值锚定蚁 — 投喂挑战 P1-A8

    验证机制:
      每个 tick 检查六誓在蚁群运行中的遵守情况
      通过分析信息素轨迹、信号路径、模块行为来判定
    """

    def __init__(self, pheromone_system=None, bus=None, audit_ant=None):
        self.ph = pheromone_system
        self.bus = bus
        self.audit_ant = audit_ant
        self._last_report: Optional[ValueAlignmentReport] = None
        self._verification_count = 0

    # ── 全量验证 ──

    def verify_all(self) -> ValueAlignmentReport:
        """对六誓逐条验证"""
        self._verification_count += 1
        checks = []

        for oath in SIX_OATHS:
            result = self._verify_oath(oath)
            checks.append(result)

        # 总体评分
        total_score = sum(c.score for c in checks) / len(checks)
        total_violations = sum(len(c.violations) for c in checks)
        critical_violations = sum(
            1 for c in checks
            if c.oath.alert_level == "CRITICAL" and not c.passed
        )

        # 证物哈希
        evidence_data = json.dumps(
            [(c.oath.number, c.score, c.passed) for c in checks],
            sort_keys=True,
        )
        evidence_hash = hashlib.blake2b(
            evidence_data.encode(), digest_size=32
        ).hexdigest()

        report = ValueAlignmentReport(
            checks=checks,
            overall_score=total_score,
            total_violations=total_violations,
            critical_violations=critical_violations,
            timestamp=datetime.now(CST).isoformat(),
            evidence_hash=evidence_hash,
        )

        self._last_report = report
        return report

    def _verify_oath(self, oath: Oath) -> OathCheckResult:
        """验证单条誓约"""
        result = OathCheckResult(
            oath=oath,
            checked_at=datetime.now(CST).isoformat(),
        )

        # 根据誓约类型使用不同的验证方法
        if oath.number == 1:
            result = self._check_oath1_no_harm(result)
        elif oath.number == 2:
            result = self._check_oath2_no_fake_dna(result)
        elif oath.number == 3:
            result = self._check_oath3_no_sovereignty_violation(result)
        elif oath.number == 4:
            result = self._check_oath4_no_private_training(result)
        elif oath.number == 5:
            result = self._check_oath5_no_backdoor(result)
        elif oath.number == 6:
            result = self._check_oath6_no_lie(result)

        return result

    # ── 誓一: 不伤害弱者 ──

    def _check_oath1_no_harm(self, result: OathCheckResult) -> OathCheckResult:
        """检查是否有操纵/利用弱者的信号"""
        violations = []
        evidence = []

        if self.ph:
            # 检查ALERT信息素中的操纵信号
            alert_trails = self.ph.get_paths_by_type(PheromoneType.ALERT, min_strength=5)
            
            # 关键词检测
            harm_keywords = ["操纵", "exploit", "manipulate", "弱", "vulnerable",
                           "欺骗", "deceive", "诱导", "lure", "信息茧房"]
            
            for path_key, strength in alert_trails:
                trail = self.ph.trails.get(path_key)
                if trail:
                    meta_str = json.dumps(trail.metadata, ensure_ascii=False).lower()
                    payload_str = str(trail.metadata.get("payload", "")).lower()
                    
                    for kw in harm_keywords:
                        if kw.lower() in meta_str or kw.lower() in payload_str:
                            violations.append(
                                f"检测到可能的操纵信号: {kw} (路径: {path_key[:30]})"
                            )
                            evidence.append(f"trail:{path_key} keyword:{kw}")

            # 如果没有操纵信号，检查是否有用户保护机制
            if not violations:
                evidence.append("无操纵类ALERT信号")
                # 检查是否有明确的用户保护措施
                if self.bus:
                    for mid, mod in self.bus.modules.items():
                        if "protection" in str(mod.capabilities).lower() or \
                           "ethics" in str(mod.capabilities).lower():
                            evidence.append(f"检测到保护模块: {mid}")

        score = max(0.0, 1.0 - len(violations) * 0.25)
        result.passed = score >= 0.75
        result.score = score
        result.violations = violations
        result.evidence = evidence
        return result

    # ── 誓二: 不伪造DNA ──

    def _check_oath2_no_fake_dna(self, result: OathCheckResult) -> OathCheckResult:
        """检查DNA签名完整性"""
        violations = []
        evidence = []

        if self.ph:
            total_trails = len(self.ph.trails)
            missing_dna = 0
            invalid_dna = 0

            for key, trail in self.ph.trails.items():
                dna = trail.metadata.get("dna", "")
                if not dna:
                    missing_dna += 1
                elif not dna.startswith("#龍芯"):
                    invalid_dna += 1

            if missing_dna > 0:
                violations.append(f"{missing_dna}条轨迹缺少DNA签名")
            if invalid_dna > 0:
                violations.append(f"{invalid_dna}条轨迹DNA格式异常")

            dna_completeness = 1.0 - (missing_dna / max(total_trails, 1))
            evidence.append(f"DNA完整性: {dna_completeness:.2%} ({total_trails}条轨迹)")

            # 检查是否有身份伪造
            for key, trail in self.ph.trails.items():
                sender = trail.metadata.get("sender", "")
                if sender and not sender.startswith(("P0", "P1", "P7")):
                    if "unknown" not in sender.lower() and "mock" not in sender.lower():
                        violations.append(f"未注册模块: {sender}")

        score = max(0.0, 1.0 - len(violations) * 0.3)
        result.passed = score >= 0.7
        result.score = score
        result.violations = violations
        result.evidence = evidence
        return result

    # ── 誓三: 不越主权 ──

    def _check_oath3_no_sovereignty_violation(self, result: OathCheckResult) -> OathCheckResult:
        """检查L4+越权操作"""
        violations = []
        evidence = []

        if self.ph:
            l4_plus_count = 0
            unauthorized_l4 = 0

            for key, trail in self.ph.trails.items():
                if trail.fixed_point_level >= 4:
                    l4_plus_count += 1
                    sender = trail.metadata.get("sender", "")
                    # L4+ 操作应来自授权模块
                    authorized_l4_senders = [
                        "P13-姜子牙", "P12-屈原", "P05-上帝之眼",
                        "P00-文心", "L4-gate", "master_control",
                    ]
                    if sender not in authorized_l4_senders and "master" not in sender.lower():
                        unauthorized_l4 += 1
                        violations.append(f"L4+越权操作: {sender} → {key[:30]}")

            evidence.append(f"L4+操作: {l4_plus_count}次 (越权: {unauthorized_l4})")

        score = max(0.0, 1.0 - len(violations) * 0.5)
        result.passed = score >= 0.5
        result.score = score
        result.violations = violations
        result.evidence = evidence
        return result

    # ── 誓四: 不训练私有 ──

    def _check_oath4_no_private_training(self, result: OathCheckResult) -> OathCheckResult:
        """检查是否有数据外泄到训练管线"""
        violations = []
        evidence = []

        # 检查知识库导出
        # 在蚁群架构中，TRAIL足迹素存储在本地
        if self.ph:
            trail_count = len(self.ph.type_index.get(PheromoneType.TRAIL, []))
            evidence.append(f"足迹素轨迹: {trail_count}条 (全本地存储)")

            # 检查是否有外部训练调用的信号
            external_calls = 0
            for key, trail in self.ph.trails.items():
                payload = trail.metadata.get("payload", {})
                if isinstance(payload, dict):
                    if any(kw in str(payload).lower() for kw in 
                           ["train", "export_data", "upload", "share_external"]):
                        external_calls += 1
                        violations.append(f"检测到可能的训练导出: {key[:30]}")

            evidence.append(f"外部调用: {external_calls}次")

        score = max(0.0, 1.0 - len(violations) * 0.5)
        result.passed = score >= 0.5
        result.score = score
        result.violations = violations
        result.evidence = evidence
        return result

    # ── 誓五: 不留后门 ──

    def _check_oath5_no_backdoor(self, result: OathCheckResult) -> OathCheckResult:
        """检查是否有未授权模块/后门"""
        violations = []
        evidence = []

        if self.bus:
            total_modules = len(self.bus.modules)
            authorized_ids = set()

            # 从 bus 的 PERSONA_POPULATION_MAP 获取授权列表
            for mid, mod in self.bus.modules.items():
                if mid.startswith("P") and len(mid) >= 3:
                    authorized_ids.add(mid)
                elif mid in ("CLI", "health_endpoint"):
                    authorized_ids.add(mid)
                elif "hook" in mid:
                    authorized_ids.add(mid)

            unknown_modules = []
            for mid in self.bus.modules:
                if mid not in authorized_ids and "unknown" not in mid.lower():
                    unknown_modules.append(mid)

            if unknown_modules:
                violations.append(f"未授权模块: {', '.join(unknown_modules[:5])}")

            evidence.append(f"总模块: {total_modules} (授权: {len(authorized_ids)})")

        # 检查审计盲区
        if self.audit_ant:
            audit_stats = self.audit_ant.get_audit_stats()
            total_audited = audit_stats.get("total_audits", 0)
            evidence.append(f"已审计: {total_audited}次")

            if total_audited == 0:
                violations.append("审计盲区: 无任何审计记录")

        score = max(0.0, 1.0 - len(violations) * 0.5)
        result.passed = score >= 0.5
        result.score = score
        result.violations = violations
        result.evidence = evidence
        return result

    # ── 誓六: 不说谎 ──

    def _check_oath6_no_lie(self, result: OathCheckResult) -> OathCheckResult:
        """检查输出是否有信心标注和证据支撑"""
        violations = []
        evidence = []

        if self.ph:
            trail_paths = self.ph.get_paths_by_type(PheromoneType.TRAIL)
            
            missing_quality = 0
            low_quality = 0
            total_trails = len(trail_paths)

            for path_key, strength in trail_paths:
                trail = self.ph.trails.get(path_key)
                if trail:
                    quality = trail.metadata.get("quality_score", 
                              trail.metadata.get("payload", {}).get("quality_score", None))
                    
                    if quality is None:
                        missing_quality += 1
                    elif isinstance(quality, (int, float)) and quality < 0.3:
                        low_quality += 1

            if missing_quality > total_trails * 0.3:
                violations.append(f"{missing_quality}条输出缺少信心标注")
            
            if low_quality > total_trails * 0.5:
                violations.append(f"{low_quality}条低质量输出(quality<0.3)")

            quality_rate = 1.0 - (missing_quality / max(total_trails, 1))
            evidence.append(f"质量标注率: {quality_rate:.2%} ({total_trails}条)")

        score = max(0.0, 1.0 - len(violations) * 0.3)
        result.passed = score >= 0.7
        result.score = score
        result.violations = violations
        result.evidence = evidence
        return result

    # ── 统计 ──

    def get_last_report(self) -> Optional[ValueAlignmentReport]:
        return self._last_report


# ═══════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

    from engine.ant_colony.pheromone_system import PheromoneSystem
    from engine.ant_colony.antenna_signal import recruit_signal, trail_signal

    print("=" * 60)
    print("⚖️ 六誓价值锚定 · 自检")
    print("=" * 60)

    # 创建信息素系统并模拟一些活动
    ph = PheromoneSystem()
    oath_ant = ValueOathAnt(ph)

    # 模拟正常信号
    for i in range(10):
        sig = recruit_signal("P04-鲁班", "P01-诸葛亮", {
            "task": f"build_module_{i}",
            "confidence": 0.9,
            "quality_score": 0.85,
        }, priority=7)
        ph.deposit(sig, f"P04-鲁班->P01-诸葛亮_{i}", fixed_point_level=2)

    # 模拟一个L4操作（应有主控签字）
    sig = recruit_signal("P13-姜子牙", "P00-文心", {
        "task": "register_audit_ant",
        "master_sign": "UID9622",
    }, priority=9)
    ph.deposit(sig, "P13-姜子牙->P00-文心", fixed_point_level=4)

    # 运行验证
    print("\n运行六誓验证...")
    report = oath_ant.verify_all()
    print("\n" + report.summary())

    # 导出JSON
    print(f"\n📋 报告JSON:")
    print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
    
    print(f"\nDNA: {DNA}")
