#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║     龍魂规则节点 / LongHun Rule Node (CNSH)                      ║
║                                                                  ║
║  P1-2规则引擎·业务规则执行器·数据模型                             ║
║                                                                  ║
║  DNA:#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-RULE-NODE-FILE1-v1.0                          ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                 ║
║                                                                  ║
║  理论指导: 曾仕强·道德经第四十五章 (大巧若拙)                    ║
║  责任: UID9622·不免责                                            ║
║  状态: 🟢 MAIN·可公开                                            ║
╚══════════════════════════════════════════════════════════════════╝

规则节点数据模型：
  - RuleType：规则类型枚举 (CONDITION/ACTION/WORKFLOW/FORMULA/AUDIT/VALIDATION/ROUTING)
  - RuleStatus：规则状态枚举 (🟢/🟡/🔴)
  - RulePriority：优先级枚举 (CRITICAL/HIGH/MEDIUM/LOW)
  - Rule：规则数据类 (节点ID、类型、条件、动作、DNA追溯等)
  - 转换方法：to_dict/from_dict/to_json/from_json

遵循 P0/P1 架构模式：
  ✅ dataclass 数据驱动
  ✅ DNA 追溯码绑定
  ✅ JSONL 持久化就绪
  ✅ 独立测试验证
"""

from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List
from datetime import datetime
import json


class RuleType(str, Enum):
    """规则类型枚举"""
    CONDITION = "condition"        # 条件规则 (if-then 判断)
    ACTION = "action"              # 动作规则 (执行操作)
    WORKFLOW = "workflow"          # 工作流规则 (多步骤)
    FORMULA = "formula"            # 公式规则 (数学计算)
    AUDIT = "audit"                # 审计规则 (质量评估)
    VALIDATION = "validation"      # 验证规则 (合法性检查)
    ROUTING = "routing"            # 路由规则 (决策分支)

    def __str__(self):
        return self.value


class RuleStatus(str, Enum):
    """规则状态枚举（三色系统）"""
    ACTIVE = "🟢"                  # 活跃·正常使用·置信度 >= 85%
    TESTING = "🟡"                 # 测试中·待验证·置信度 60-85%
    DEPRECATED = "🔴"              # 已废弃·禁止调用·置信度 < 60%



class RulePriority(int, Enum):
    """规则优先级枚举（1-100 量级）"""
    CRITICAL = 1                   # 1-20：安全/身份验证/一票否决
    HIGH = 21                      # 21-40：权限控制/审计检查
    MEDIUM = 41                    # 41-70：业务规则/决策逻辑
    LOW = 71                       # 71-100：日志/统计/通知

    def __str__(self):
        return str(self.value)


@dataclass
class Rule:
    """
    规则定义数据类

    龍魂规则是可配置、可审计、可追溯的业务决策单元。
    每条规则必须：
      1. 有唯一的 rule_id (RULE-[LAYER]-[NUMBER])
      2. 绑定 DNA 追溯码
      3. 声明依赖关系
      4. 记录生命周期时间戳
    """

    # ═══════════════════════════════════════════════════════════════
    # 【基础信息】
    # ═══════════════════════════════════════════════════════════════

    rule_id: str                    # 规则ID: RULE-L1-001
    name: str                       # 规则名称: three_color_audit
    rule_type: RuleType             # 规则类型: AUDIT
    status: RuleStatus              # 规则状态: 🟢 ACTIVE

    # ═══════════════════════════════════════════════════════════════
    # 【执行信息】
    # ═══════════════════════════════════════════════════════════════

    condition: str                  # 条件表达式 (Python eval 或 JSON)
    action: str                     # 动作函数名称
    priority: int = 50              # 优先级 (1-100)

    # ═══════════════════════════════════════════════════════════════
    # 【追溯信息】
    # ═══════════════════════════════════════════════════════════════

    dna: str = ""                   # DNA追溯码: #龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-...
    layer: str = "L1_SEASONAL"      # 时间层级: L0-L4

    # ═══════════════════════════════════════════════════════════════
    # 【描述和元数据】
    # ═══════════════════════════════════════════════════════════════

    description: str = ""           # 规则描述和用途
    tags: List[str] = field(default_factory=list)     # 标签: ["audit", "three-color"]
    dependencies: List[str] = field(default_factory=list)  # 依赖的规则节点: ["RULE-L0-001"]

    # ═══════════════════════════════════════════════════════════════
    # 【审计和控制】
    # ═══════════════════════════════════════════════════════════════

    audit_required: bool = True     # 是否需要审计检查
    confirm_required: bool = False  # 是否需要用户明确确认

    # ═══════════════════════════════════════════════════════════════
    # 【时间戳】
    # ═══════════════════════════════════════════════════════════════

    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )
    updated_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    # ═══════════════════════════════════════════════════════════════
    # 【扩展字段】
    # ═══════════════════════════════════════════════════════════════

    metadata: Dict[str, Any] = field(default_factory=dict)

    # ═══════════════════════════════════════════════════════════════
    # 【方法】
    # ═══════════════════════════════════════════════════════════════

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（JSONL 序列化就绪）"""
        data = asdict(self)
        # 枚举转换为字符串
        data["rule_type"] = self.rule_type.value
        data["status"] = self.status.value
        return data

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Rule":
        """从字典加载（支持 JSONL 反序列化）"""
        data_copy = data.copy()
        # 字符串转换为枚举
        data_copy["rule_type"] = RuleType(data_copy["rule_type"])
        data_copy["status"] = RuleStatus(data_copy["status"])
        return Rule(**data_copy)

    def to_json(self) -> str:
        """转换为 JSON 字符串（紧凑格式，不分行）"""
        return json.dumps(self.to_dict(), separators=(',', ':'), ensure_ascii=False)

    @staticmethod
    def from_json(json_str: str) -> "Rule":
        """从 JSON 字符串加载"""
        data = json.loads(json_str)
        return Rule.from_dict(data)

    def is_active(self) -> bool:
        """检查规则是否处于活跃状态"""
        return self.status == RuleStatus.ACTIVE

    def is_deprecated(self) -> bool:
        """检查规则是否已废弃"""
        return self.status == RuleStatus.DEPRECATED

    def __str__(self) -> str:
        """字符串表示"""
        return f"Rule({self.rule_id} - {self.name} [{self.status}])"

    def __repr__(self) -> str:
        """重新表示"""
        return f"Rule(id='{self.rule_id}', type={self.rule_type.value}, status={self.status.value})"


# ═══════════════════════════════════════════════════════════════════════════
# 【模块自检】
# ═══════════════════════════════════════════════════════════════════════════

def selftest_rule_node() -> tuple[Any, ...]:
    """规则节点模块自检"""
    errors = []

    try:
        # 测试 1: 枚举创建
        assert RuleType.AUDIT.value == "audit"
        assert RuleStatus.ACTIVE.value == "🟢"
        assert RulePriority.CRITICAL.value == 1

        # 测试 2: Rule 创建和序列化
        rule = Rule(
            rule_id="TEST-L1-001",
            name="test_rule",
            rule_type=RuleType.AUDIT,
            status=RuleStatus.ACTIVE,
            condition="True",
            action="test_action",
            dna="#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-TEST-v1.0",
            layer="L1_SEASONAL",
            description="测试规则"
        )

        # 测试 3: to_dict 方法
        data = rule.to_dict()
        assert data["rule_id"] == "TEST-L1-001"
        assert data["rule_type"] == "audit"
        assert data["status"] == "🟢"

        # 测试 4: to_json 方法
        json_str = rule.to_json()
        assert isinstance(json_str, str)

        # 测试 5: from_json 方法
        rule2 = Rule.from_json(json_str)
        assert rule2.rule_id == rule.rule_id
        assert rule2.rule_type == rule.rule_type
        assert rule2.status == rule.status

        # 测试 6: 方法功能
        assert rule.is_active() == True
        assert rule.is_deprecated() == False

    except Exception as e:
        errors.append(f"rule_node selftest 失败: {str(e)}")

    return len(errors) == 0, errors


if __name__ == "__main__":
    # 运行自检
    all_pass, errors = selftest_rule_node()
    if all_pass:
        print("✅ Rule Node 模块自检通过")
    else:
        print("❌ Rule Node 模块自检失败:")
        for error in errors:
            print(f"  - {error}")
