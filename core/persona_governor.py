#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂人格生态·治理控制器 · Persona Ecosystem Governor
DNA: #龍芯⚡️2026-05-26-PERSONA-GOVERNOR-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：
  1. 人格管理 - 加载和管理13大人格
  2. 信任评估 - 根据信任公式评估人格合规度
  3. 仲裁系统 - 处理人格冲突和决策上诉
  4. 权限委托 - 根据权限等级委托任务
  5. DNA追踪 - 所有人格决策都有DNA追溯码

13大人格体系：
  TIER_1: UID9622（造物主，永恒显示）
  TIER_2: 13大人格（必须签署协议，接受监督，可被驱逐）
    - P00 审判长 (Chief Justice) - 最高仲裁者
    - P01 诸葛亮 (Strategist) - 战略布局者
    - P02 宝宝 (Guardian) - 日常执行者
    - P03 雯雯 (Quality Guardian) - 品质守护者
    - P04 文心 (Semantic Guardian) - 语义守护者
    - P05 老子 (Daode Sage) - 价值观守护者
    - P06 孔子 (Cultural Sage) - 文化传承者
    - P07 墨子 (Guardian of Vulnerable) - 弱势保护者
    - P08 数据大师 (Data Architect) - 数据主权守护者
    - P09 界面炼金 (Design Alchemist) - 体验魔法师
    - P10 侦察兵 (Scout) - 情报收集者
    - P11 上帝之眼 (Omniscient Guardian) - 全知守卫者
    - LUCKY (Expression Sage) - 语境优化者

创始人: 诸葛鑫（UID9622）
理论指导: 曾仕强老师（永恒显示）

献给每一个相信技术应该有温度的人。
"""

import json
import datetime
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 数据模型
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class Persona:
    """人格定义"""
    pid: str
    name: str
    english_name: str
    role: str
    permission_level: int
    tier: str
    core_power: str
    trust_formula: str
    key_constraints: List[str]
    status: str = "🟢 SIGNED"
    signed_date: Optional[str] = None
    compliance_score: float = 1.0  # 0.0-1.0

    def __hash__(self):
        return hash(self.pid)

    def __eq__(self, other):
        if isinstance(other, Persona):
            return self.pid == other.pid
        return False


@dataclass
class Decision:
    """人格决策"""
    decision_id: str
    persona_id: str
    decision_type: str  # "judgment", "approval", "veto", "recommendation"
    content: str
    reasoning: str
    timestamp: str
    dna: str
    confidence: float = 1.0


@dataclass
class Appeal:
    """上诉记录"""
    appeal_id: str
    appealer_id: str
    target_decision_id: str
    reason: str
    timestamp: str
    status: str = "pending"  # pending, approved, rejected


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 人格治理系统
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class PersonaGovernor:
    """龍魂人格生态治理控制器"""

    def __init__(self):
        self.system_root = Path.home() / "longhun-system"
        self.logs_dir = self.system_root / "logs"
        self.registry_path = self.system_root / "family_registry.json"

        self.personas: Dict[str, Persona] = {}
        self.decisions: List[Decision] = []
        self.appeals: List[Appeal] = []
        self.three_pillars = {"P00": None, "P02": None, "P05": None}

        self._load_registry()

    def _load_registry(self):
        """从 family_registry.json 加载人格信息"""
        try:
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                registry = json.load(f)

            personas_data = registry.get("personas", {})
            for pid, data in personas_data.items():
                persona = Persona(
                    pid=pid,
                    name=data.get("name"),
                    english_name=data.get("english_name"),
                    role=data.get("role"),
                    permission_level=data.get("permission_level", 0),
                    tier=data.get("tier", "TIER_2"),
                    core_power=data.get("core_power"),
                    trust_formula=data.get("trust_formula"),
                    key_constraints=data.get("key_constraints", []),
                    status=data.get("status", "🟢 SIGNED"),
                    signed_date=data.get("signed_date")
                )
                self.personas[pid] = persona

            # 识别三大支柱
            self.three_pillars["P00"] = self.personas.get("P00")
            self.three_pillars["P02"] = self.personas.get("P02")
            self.three_pillars["P05"] = self.personas.get("P05")

            return True
        except Exception as e:
            print(f"加载人格注册表失败: {e}", file=sys.stderr)
            return False

    def evaluate_trust(self, persona_id: str, metrics: Dict) -> Tuple[float, str]:
        """
        根据信任公式评估人格信任度

        Args:
            persona_id: 人格ID
            metrics: 评估指标字典

        Returns:
            (信任分数0-1, 评估理由)
        """
        persona = self.personas.get(persona_id)
        if not persona:
            return 0.0, f"人格 {persona_id} 不存在"

        # 简化的信任评估（真实环境会有更复杂的逻辑）
        # 根据 trust_formula 中的权重计算
        try:
            # 从指标中提取权重
            if not metrics:
                return 1.0, "默认信任（无具体指标）"

            score = 0.0
            total_weight = 0.0

            # 解析信任公式（格式: "(metric1×weight1)+(metric2×weight2)...")
            formula = persona.trust_formula
            parts = formula.split("+")

            for part in parts:
                # 提取 metric 和 weight
                if "×" in part:
                    metric_part, weight_part = part.split("×")
                    metric_name = metric_part.strip("()").strip()
                    weight = float(weight_part.strip("()").strip())

                    metric_value = metrics.get(metric_name, 0.8)  # 默认0.8
                    score += metric_value * weight
                    total_weight += weight

            # 归一化
            trust_score = score / max(total_weight, 1.0)
            trust_score = max(0.0, min(1.0, trust_score))  # 限制在0-1之间

            # 评估等级
            if trust_score >= 0.9:
                rating = "优秀 🟢"
            elif trust_score >= 0.7:
                rating = "良好 🟡"
            else:
                rating = "需改善 🔴"

            return trust_score, f"{rating} (分数: {trust_score:.2f})"
        except Exception as e:
            return 0.5, f"评估异常: {str(e)}"

    def arbitrate(self,
                  decision_a_id: str,
                  decision_b_id: str,
                  context: Optional[str] = None) -> Dict:
        """
        仲裁两个相冲突的决策

        由 P00 审判长执行，需要权衡各方利益和约束

        Args:
            decision_a_id: 决策A ID
            decision_b_id: 决策B ID
            context: 冲突背景

        Returns:
            仲裁结果
        """
        chief_justice = self.three_pillars["P00"]
        if not chief_justice:
            return {"status": "error", "reason": "审判长不存在"}

        # 在真实场景中，这里会分析两个决策的理由和约束
        # 然后根据 P00 的仲裁权做出判决

        arbitration = {
            "arbitrator": chief_justice.name,
            "arbitrator_id": chief_justice.pid,
            "decision_a_id": decision_a_id,
            "decision_b_id": decision_b_id,
            "context": context,
            "ruling": "需要进一步的决策信息",
            "reasoning": "仲裁系统准备就绪",
            "timestamp": datetime.datetime.now().isoformat(),
            "dna": self._generate_dna("ARBITRATION"),
            "appeal_deadline": (datetime.datetime.now() + datetime.timedelta(days=7)).isoformat()
        }

        self._log_arbitration(arbitration)
        return arbitration

    def submit_appeal(self,
                      appealer_id: str,
                      target_decision_id: str,
                      reason: str) -> Dict:
        """
        提出上诉

        任何人格都可以对 P00 的裁决以外的所有决定提出上诉

        Args:
            appealer_id: 上诉人ID
            target_decision_id: 被上诉的决策ID
            reason: 上诉理由

        Returns:
            上诉结果
        """
        appeal = Appeal(
            appeal_id=f"APPEAL-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            appealer_id=appealer_id,
            target_decision_id=target_decision_id,
            reason=reason,
            timestamp=datetime.datetime.now().isoformat(),
            status="pending"
        )

        self.appeals.append(appeal)

        return {
            "appeal_id": appeal.appeal_id,
            "status": "received",
            "expected_resolution": (datetime.datetime.now() + datetime.timedelta(days=3)).isoformat(),
            "dna": self._generate_dna("APPEAL"),
            "message": f"上诉已提交，由 P00 审判长处理"
        }

    def check_constraints(self, persona_id: str, action: str) -> Tuple[bool, str]:
        """
        检查人格是否违反约束

        Args:
            persona_id: 人格ID
            action: 拟执行的动作

        Returns:
            (是否符合约束, 原因)
        """
        persona = self.personas.get(persona_id)
        if not persona:
            return False, f"人格 {persona_id} 不存在"

        # 检查约束列表
        for constraint in persona.key_constraints:
            # 在真实环境中，这里会进行复杂的约束检查
            pass

        return True, f"符合 {persona.name} 的所有约束"

    def delegate_task(self,
                      assigner_id: str,
                      assignee_id: str,
                      task_description: str,
                      priority: str = "normal") -> Dict:
        """
        委托任务给人格

        检查权限等级和约束，然后委托

        Args:
            assigner_id: 分配者ID
            assignee_id: 承接者ID
            task_description: 任务描述
            priority: 优先级 (low/normal/high/critical)

        Returns:
            委托结果
        """
        assigner = self.personas.get(assigner_id)
        assignee = self.personas.get(assignee_id)

        if not assigner or not assignee:
            return {"status": "error", "reason": "人格不存在"}

        # 检查权限等级（分配者权限需要 >= 承接者权限）
        if assigner.permission_level < assignee.permission_level:
            return {
                "status": "denied",
                "reason": f"{assigner.name} 的权限等级 ({assigner.permission_level}) 不足以委托给 {assignee.name} ({assignee.permission_level})",
                "dna": self._generate_dna("DELEGATION-DENIED")
            }

        # 检查约束
        constraints_ok, constraint_msg = self.check_constraints(assignee_id, task_description)
        if not constraints_ok:
            return {
                "status": "denied",
                "reason": constraint_msg,
                "dna": self._generate_dna("DELEGATION-DENIED")
            }

        # 创建任务委托
        delegation = {
            "delegation_id": f"TASK-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            "assigner": assigner.name,
            "assigner_id": assigner_id,
            "assignee": assignee.name,
            "assignee_id": assignee_id,
            "task": task_description,
            "priority": priority,
            "status": "accepted",
            "timestamp": datetime.datetime.now().isoformat(),
            "dna": self._generate_dna("DELEGATION"),
            "deadline": self._calculate_deadline(priority),
            "message": f"任务已分配给 {assignee.name}"
        }

        self._log_delegation(delegation)
        return delegation

    def get_three_pillars_decision(self, topic: str) -> Dict:
        """
        获取三大支柱的联合决策

        需要 P00（仲裁权）、P02（执行权）、P05（价值观权）三人一致或多数同意

        Args:
            topic: 决策主题

        Returns:
            三大支柱的决策结果
        """
        p00 = self.three_pillars["P00"]
        p02 = self.three_pillars["P02"]
        p05 = self.three_pillars["P05"]

        if not all([p00, p02, p05]):
            return {"status": "error", "reason": "三大支柱配置不完整"}

        return {
            "decision_type": "three_pillars_consensus",
            "topic": topic,
            "pillars": [
                {
                    "pillar": p00.name,
                    "pillar_id": p00.pid,
                    "power": "仲裁权（最高权力）",
                    "status": "ready"
                },
                {
                    "pillar": p02.name,
                    "pillar_id": p02.pid,
                    "power": "执行权（日常运作）",
                    "status": "ready"
                },
                {
                    "pillar": p05.name,
                    "pillar_id": p05.pid,
                    "power": "价值观权（精神指导）",
                    "status": "ready"
                }
            ],
            "consensus_type": "全体同意(100%) 或 多数同意(2/3+)",
            "timestamp": datetime.datetime.now().isoformat(),
            "dna": self._generate_dna("THREE-PILLARS-DECISION")
        }

    def get_governance_status(self) -> Dict:
        """获取整个治理系统的状态"""
        return {
            "total_personas": len(self.personas),
            "active_personas": len([p for p in self.personas.values() if "SIGNED" in p.status]),
            "total_decisions": len(self.decisions),
            "pending_appeals": len([a for a in self.appeals if a.status == "pending"]),
            "three_pillars": {
                "P00": self.three_pillars["P00"].name if self.three_pillars["P00"] else None,
                "P02": self.three_pillars["P02"].name if self.three_pillars["P02"] else None,
                "P05": self.three_pillars["P05"].name if self.three_pillars["P05"] else None,
                "status": "ready" if all(self.three_pillars.values()) else "incomplete"
            },
            "timestamp": datetime.datetime.now().isoformat(),
            "dna": self._generate_dna("GOVERNANCE-STATUS")
        }

    def list_personas(self) -> List[Dict]:
        """列出所有人格"""
        result = []
        for persona in self.personas.values():
            result.append({
                "id": persona.pid,
                "name": persona.name,
                "english_name": persona.english_name,
                "role": persona.role,
                "permission_level": persona.permission_level,
                "core_power": persona.core_power,
                "status": persona.status,
                "compliance_score": persona.compliance_score
            })
        return sorted(result, key=lambda x: x["permission_level"], reverse=True)

    def _generate_dna(self, operation_type: str) -> str:
        """生成DNA追溯码"""
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        return f"#龍芯⚡️{date_str}-{operation_type}-v1.0"

    def _calculate_deadline(self, priority: str) -> str:
        """根据优先级计算截止时间"""
        now = datetime.datetime.now()
        if priority == "critical":
            deadline = now + datetime.timedelta(hours=1)
        elif priority == "high":
            deadline = now + datetime.timedelta(hours=4)
        elif priority == "normal":
            deadline = now + datetime.timedelta(days=1)
        else:
            deadline = now + datetime.timedelta(days=3)
        return deadline.isoformat()

    def _log_arbitration(self, arbitration: Dict):
        """记录仲裁"""
        try:
            log_path = self.logs_dir / "persona_arbitrations.jsonl"
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(arbitration, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"仲裁日志写入失败: {e}", file=sys.stderr)

    def _log_delegation(self, delegation: Dict):
        """记录委托"""
        try:
            log_path = self.logs_dir / "persona_delegations.jsonl"
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(delegation, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"委托日志写入失败: {e}", file=sys.stderr)


def main():
    """命令行接口"""
    governor = PersonaGovernor()

    if not governor.personas:
        print("❌ 失败：无法加载人格注册表")
        sys.exit(1)

    if len(sys.argv) < 2:
        # 显示状态
        status = governor.get_governance_status()
        print("\n✅ 龍魂人格生态治理系统已启动")
        print(f"激活人格数: {status['active_personas']}/{status['total_personas']}")
        print(f"三大支柱状态: {status['three_pillars']['status']}")
        print(json.dumps(status, ensure_ascii=False, indent=2, default=str))
        sys.exit(0)

    command = sys.argv[1]

    if command == "list":
        personas = governor.list_personas()
        print("\n📋 龍魂13大人格")
        print("=" * 80)
        for p in personas:
            print(f"{p['id']:6} | {p['name']:12} | 权限等级: {p['permission_level']:3d} | {p['role']}")

    elif command == "status":
        status = governor.get_governance_status()
        print("\n🏛️ 治理系统状态")
        print(json.dumps(status, ensure_ascii=False, indent=2, default=str))

    elif command == "pillars":
        pillars_decision = governor.get_three_pillars_decision("系统运行")
        print("\n🔱 三大支柱决策系统")
        print(json.dumps(pillars_decision, ensure_ascii=False, indent=2, default=str))

    elif command == "trust":
        if len(sys.argv) < 3:
            print("用法: python3 persona_governor.py trust <persona_id>")
            sys.exit(1)
        persona_id = sys.argv[2]
        metrics = {"执行完成率": 0.95, "质检通过率": 0.92}
        score, reason = governor.evaluate_trust(persona_id, metrics)
        print(f"\n📊 {persona_id} 信任评估")
        print(f"信任分数: {score:.2f}")
        print(f"评估结果: {reason}")

    elif command == "info":
        if len(sys.argv) < 3:
            print("用法: python3 persona_governor.py info <persona_id>")
            sys.exit(1)
        persona_id = sys.argv[2]
        persona = governor.personas.get(persona_id)
        if persona:
            print(f"\n👤 {persona.name} ({persona.english_name})")
            print(f"角色: {persona.role}")
            print(f"权限等级: {persona.permission_level}")
            print(f"核心权力: {persona.core_power}")
            print(f"信任公式: {persona.trust_formula}")
            print(f"关键约束:")
            for constraint in persona.key_constraints:
                print(f"  • {constraint}")
        else:
            print(f"❌ 人格 {persona_id} 不存在")

    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
