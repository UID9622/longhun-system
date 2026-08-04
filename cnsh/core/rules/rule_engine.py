#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║     龍魂规则引擎 / LongHun Rule Engine (CNSH)                    ║
║                                                                  ║
║  P1-2 规则引擎·业务规则执行器                                    ║
║                                                                  ║
║  DNA:#龍芯⚡️2026-06-03-RULE-ENGINE-FILE1-v1.0                        ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                 ║
║                                                                  ║
║  理论指导: 曾仕强·道德经第二十八章 (知其白·守其黑)              ║
║  责任: UID9622·不免责                                            ║
║  状态: 🟢 MAIN·可公开                                            ║
╚══════════════════════════════════════════════════════════════════╝

规则引擎核心职责：
  1. 规则注册和管理 (O(1) 查找)
  2. 规则生命周期 (定义→激活→评估→归档)
  3. 规则执行调度 (条件/优先级过滤)
  4. 规则审计留痕 (append-only 日志)
  5. 系统自检 (selftest)

规则引擎设计原则：
  ✅ 单例模式 (global singleton instance)
  ✅ O(1) 查找 (memory dict)
  ✅ Append-only 持久化 (JSONL 格式)
  ✅ DNA 追溯码绑定
  ✅ 三色状态管理 (🟢/🟡/🔴)
  ✅ 自检能力 (selftest)
  ✅ 日志集成 (append-only audit log)
"""

from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import os
import json

from .rule_node import Rule, RuleType, RuleStatus
from .rule_executor import RuleExecutor


class RuleEngine:
    """
    龍魂规则引擎 - 业务规则执行器

    核心功能：
      - 规则注册：register_rule(rule) → (success, message)
      - 规则查找：find_rule(rule_id) → Optional[Rule]
      - 规则执行：execute_rule(rule_id, context) → execution_result
      - 规则评估：evaluate(context, rule_type, priority) → [results]
      - 规则列表：list_rules(rule_type, status) → [rules]
      - 统计信息：get_statistics() → dict
      - 自检验证：selftest() → (all_pass, errors)

    持久化：
      - JSONL 格式 (仅追加，不覆盖)
      - 每行一条规则记录
      - 支持快速恢复和审计

    设计模式：
      - 单例模式 (get_rule_engine())
      - 工厂模式 (RuleExecutor 注入)
      - 依赖注入 (rule_file 参数)
    """

    def __init__(self, rule_file: str | None = None):
        """
        初始化规则引擎

        Args:
            rule_file: 规则注册表文件路径（JSONL 格式）
                      默认: ~/longhun-system/02_rules/RULE-REGISTRY.local.jsonl
        """
        self.rule_file = rule_file or self._get_default_rule_path()
        self.rules: Dict[str, Rule] = {}
        self.executor = RuleExecutor()
        self._ensure_rule_file()
        self._load_rules()

    # ═══════════════════════════════════════════════════════════════
    # 【初始化和文件管理】
    # ═══════════════════════════════════════════════════════════════

    @staticmethod
    def _get_default_rule_path() -> str:
        """获取默认的规则文件路径"""
        home = os.path.expanduser("~")
        return os.path.join(home, "longhun-system", "02_rules", "RULE-REGISTRY.local.jsonl")

    def _ensure_rule_file(self):
        """确保规则文件存在"""
        rule_dir = os.path.dirname(self.rule_file)
        if not os.path.exists(rule_dir):
            os.makedirs(rule_dir, exist_ok=True)

        if not os.path.exists(self.rule_file):
            # 创建空文件，附加注释头
            with open(self.rule_file, 'w', encoding='utf-8') as f:
                f.write("# 龍魂·业务规则注册表 (Append-Only JSONL)\n")
                f.write("# DNA:#龍芯⚡️2026-06-03-RULE-REGISTRY-LOCAL-v1.0\n")
                f.write("# 格式: JSONL（JSON Lines）- 仅追加，不覆盖\n")
                f.write("# 每行一条规则记录\n")
                f.write(f"# 初始化时间: {datetime.now().isoformat()}\n")
                f.write("# ═════════════════════════════════════════════\n")

    def _load_rules(self):
        """从文件加载规则到内存"""
        if not os.path.exists(self.rule_file):
            return

        try:
            with open(self.rule_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # 跳过空行和注释行
                    if not line or line.startswith('#'):
                        continue

                    try:
                        data = json.loads(line)
                        rule = Rule.from_dict(data)
                        self.rules[rule.rule_id] = rule
                    except Exception as e:
                        # 日志记录加载失败，但不中断
                        # print(f"⚠️  规则加载失败: {line[:50]}... - {str(e)}")
                        pass
        except Exception as e:
            # 文件读取失败
            # print(f"❌ 规则文件读取失败: {self.rule_file}")
            pass

    # ═══════════════════════════════════════════════════════════════
    # 【核心操作：注册/查找/执行/评估】
    # ═══════════════════════════════════════════════════════════════

    def register_rule(self, rule: Rule) -> Tuple[bool, str]:
        """
        注册新规则

        操作流程：
          1. 检查规则ID重复
          2. 检查依赖规则存在
          3. 保存到内存字典
          4. 追加到 JSONL 文件
          5. 记录日志

        Args:
            rule: Rule 对象

        Returns:
            (success: bool, message: str)
        """
        # 检查1: 规则ID重复
        if rule.rule_id in self.rules:
            return False, f"规则已存在: {rule.rule_id}"

        # 检查2: 依赖规则存在
        for dep_id in rule.dependencies:
            if dep_id not in self.rules:
                return False, f"依赖规则不存在: {dep_id}"

        # 保存到内存
        self.rules[rule.rule_id] = rule

        # 追加到文件
        try:
            with open(self.rule_file, 'a', encoding='utf-8') as f:
                f.write(rule.to_json() + '\n')
        except Exception as e:
            # 文件写入失败，从内存中删除
            del self.rules[rule.rule_id]
            return False, f"保存到文件失败: {str(e)}"

        return True, f"规则注册成功: {rule.rule_id}"

    def find_rule(self, rule_id: str) -> Optional[Rule]:
        """
        查找规则（O(1) 时间复杂度）

        Args:
            rule_id: 规则ID

        Returns:
            Rule 对象，如果不存在返回 None
        """
        return self.rules.get(rule_id)

    def execute_rule(self, rule_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行单条规则

        Args:
            rule_id: 规则ID
            context: 执行上下文

        Returns:
            {
                "success": bool,           # 执行是否成功
                "result": Any,             # 执行结果
                "color": str,              # 三色判定: 🟢/🟡/🔴
                "message": str,            # 执行消息
                "execution_time": float,   # 耗时（秒）
                "rule_id": str,            # 规则ID
                "rule_type": str           # 规则类型
            }
        """
        rule = self.find_rule(rule_id)
        if not rule:
            return {
                "success": False,
                "result": None,
                "color": "🔴",
                "message": f"规则不存在: {rule_id}",
                "execution_time": 0,
                "rule_id": rule_id
            }

        # 检查规则状态
        if rule.status != RuleStatus.ACTIVE:
            return {
                "success": False,
                "result": None,
                "color": "🟡",
                "message": f"规则未激活: {rule.status}",
                "execution_time": 0,
                "rule_id": rule_id,
                "rule_type": rule.rule_type.value
            }

        # 执行规则
        return self.executor.execute(rule, context)

    def evaluate(
        self,
        context: Dict[str, Any],
        rule_type: Optional[RuleType] = None,
        priority_min: int = 1
    ) -> List[Dict[str, Any]]:
        """
        评估所有适用规则

        规则将按优先级排序执行，如果遇到 🔴 审计规则将立即停止。

        Args:
            context: 执行上下文
            rule_type: 仅评估特定类型的规则（可选）
            priority_min: 最小优先级（只执行 priority >= priority_min 的规则）

        Returns:
            规则执行结果列表
        """
        results = []

        # 过滤规则
        applicable_rules = [
            r for r in self.rules.values()
            if (rule_type is None or r.rule_type == rule_type)
            and r.priority >= priority_min
            and r.status == RuleStatus.ACTIVE
        ]

        # 按优先级排序（低优先级数值优先执行）
        applicable_rules.sort(key=lambda r: r.priority)

        # 依次执行规则
        for rule in applicable_rules:
            result = self.execute_rule(rule.rule_id, context)
            results.append(result)

            # 如果遇到 🔴 审计规则，立即停止评估
            if result.get("color") == "🔴" and rule.rule_type == RuleType.AUDIT:
                break

        return results

    def list_rules(
        self,
        rule_type: Optional[RuleType] = None,
        status: Optional[RuleStatus] = None,
        layer: Optional[str] = None
    ) -> List[Rule]:
        """
        列出规则（支持过滤）

        Args:
            rule_type: 过滤规则类型
            status: 过滤规则状态
            layer: 过滤时间层级

        Returns:
            规则列表（按优先级排序）
        """
        results = []
        for rule in self.rules.values():
            if rule_type and rule.rule_type != rule_type:
                continue
            if status and rule.status != status:
                continue
            if layer and rule.layer != layer:
                continue
            results.append(rule)

        # 按优先级排序
        return sorted(results, key=lambda r: (r.priority, r.rule_id))

    # ═══════════════════════════════════════════════════════════════
    # 【统计和自检】
    # ═══════════════════════════════════════════════════════════════

    def get_statistics(self) -> Dict[str, Any]:
        """获取规则引擎的统计信息"""
        by_status = {"🟢": 0, "🟡": 0, "🔴": 0}
        by_type = {}

        for rule in self.rules.values():
            # 统计状态
            status_str = rule.status.value
            by_status[status_str] = by_status.get(status_str, 0) + 1

            # 统计类型
            type_str = rule.rule_type.value
            by_type[type_str] = by_type.get(type_str, 0) + 1

        return {
            "total_rules": len(self.rules),
            "by_status": by_status,
            "by_type": by_type,
            "rule_file": self.rule_file,
            "executor_stats": self.executor.get_statistics()
        }

    def selftest(self) -> Tuple[bool, List[str]]:
        """
        自检规则引擎

        检查项：
          1. 规则文件可读写
          2. 所有规则的依赖存在
          3. DNA 格式正确
          4. 规则ID 格式正确

        Returns:
            (all_pass: bool, errors: List[str])
        """
        errors = []

        # 检查1: 规则文件可读写
        if not os.path.exists(self.rule_file):
            errors.append(f"规则文件不存在: {self.rule_file}")
        elif not os.access(self.rule_file, os.R_OK | os.W_OK):
            errors.append(f"规则文件不可访问: {self.rule_file}")

        # 检查2: 所有规则的依赖完整
        for rule_id, rule in self.rules.items():
            for dep_id in rule.dependencies:
                if dep_id not in self.rules:
                    errors.append(f"规则 {rule_id} 依赖不存在: {dep_id}")

        # 检查3: DNA 格式验证
        for rule_id, rule in self.rules.items():
            if rule.dna and not rule.dna.startswith("#龍芯⚡️"):
                errors.append(f"规则 {rule_id} DNA 格式错误: {rule.dna}")

        # 检查4: 规则ID 格式验证
        for rule_id in self.rules.keys():
            if not rule_id.startswith("RULE-"):
                errors.append(f"规则ID 格式错误: {rule_id}")

        return len(errors) == 0, errors

    # ═══════════════════════════════════════════════════════════════
    # 【管理操作】
    # ═══════════════════════════════════════════════════════════════

    def update_rule_status(self, rule_id: str, new_status: RuleStatus) -> Tuple[bool, str]:
        """
        更新规则状态

        注意：状态变更会创建新的规则记录追加到 JSONL，不修改现有记录。

        Args:
            rule_id: 规则ID
            new_status: 新的状态

        Returns:
            (success: bool, message: str)
        """
        rule = self.find_rule(rule_id)
        if not rule:
            return False, f"规则不存在: {rule_id}"

        old_status = rule.status
        rule.status = new_status
        rule.updated_at = datetime.now().isoformat()

        # 追加到文件（作为新记录）
        try:
            with open(self.rule_file, 'a', encoding='utf-8') as f:
                f.write(rule.to_json() + '\n')
        except Exception as e:
            return False, f"状态更新失败: {str(e)}"

        return True, f"状态更新成功: {old_status} → {new_status}"

    def reset(self):
        """重置规则引擎（清空内存中的规则）"""
        self.rules.clear()
        self.executor.reset_statistics()


# ═══════════════════════════════════════════════════════════════════════════
# 【全局单例实例】
# ═══════════════════════════════════════════════════════════════════════════

_GLOBAL_RULE_ENGINE: Optional[RuleEngine] = None


def get_rule_engine(rule_file: str | None = None) -> RuleEngine:
    """
    获取全局规则引擎实例（单例模式）

    Args:
        rule_file: 规则文件路径（仅在首次初始化时使用）

    Returns:
        RuleEngine 全局实例
    """
    global _GLOBAL_RULE_ENGINE

    if _GLOBAL_RULE_ENGINE is None:
        _GLOBAL_RULE_ENGINE = RuleEngine(rule_file=rule_file)

    return _GLOBAL_RULE_ENGINE


def reset_rule_engine():
    """重置规则引擎（用于测试）"""
    global _GLOBAL_RULE_ENGINE
    if _GLOBAL_RULE_ENGINE:
        _GLOBAL_RULE_ENGINE.reset()
