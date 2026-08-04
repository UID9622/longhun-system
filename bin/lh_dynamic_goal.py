#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂·动态目标推进协议 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-动态目标-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

定位：目标驱动 + 自适应规划 + 闭环执行系统
核心思想：你只给目标和边界，AI自己规划步骤，并在过程中动态调整策略。
适用场景：系统设计、工程推进、策略推演（如CNSH字体系统）

使用方式：
  1. 设置目标、约束、资源、当前状态
  2. 运行协议 → 自动生成路径
  3. 每一步执行后评估 → 调整或继续
  4. 直到目标达成或你手动停止
"""

import os
import sys
import json
import time
import uuid
import hashlib
import datetime
import argparse
import traceback
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import random
import re
import threading
from concurrent.futures import ThreadPoolExecutor

# ============================================================
# 一、配置与常量
# ============================================================

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
BASE_DIR = Path.home() / ".longhun/dynamic_goal"
BASE_DIR.mkdir(parents=True, exist_ok=True)
LOG_PATH = BASE_DIR / "protocol.log"
HISTORY_PATH = BASE_DIR / "history.jsonl"
STATE_PATH = BASE_DIR / "state.json"

# ============================================================
# 二、数据结构
# ============================================================

@dataclass
class Goal:
    """目标定义"""
    description: str
    constraints: List[str]  # 约束条件
    resources: List[str]    # 可用资源
    current_state: str      # 当前状态
    desired_state: str      # 期望状态
    priority: int = 5       # 1-10 优先级

    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class Step:
    """步骤"""
    id: str
    description: str
    action_type: str  # "create", "modify", "test", "verify", "deploy"
    params: Dict[str, Any]
    status: str = "pending"  # pending, running, success, failed, skipped
    result: Optional[Dict] = None
    feedback: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())

@dataclass
class Plan:
    """执行计划"""
    goal: Goal
    steps: List[Step]
    current_step_index: int = 0
    status: str = "planning"  # planning, executing, completed, failed, paused
    iteration: int = 0
    created_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    dna: str = ""

    def to_dict(self) -> Dict:
        return {
            "goal": self.goal.to_dict(),
            "steps": [asdict(s) for s in self.steps],
            "current_step_index": self.current_step_index,
            "status": self.status,
            "iteration": self.iteration,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "dna": self.dna
        }

# ============================================================
# 三、目标解析器
# ============================================================

class GoalParser:
    """解析自然语言目标"""

    @staticmethod
    def parse_goal_from_text(text: str) -> Dict[str, Any]:
        """从自然语言提取目标、约束、资源"""
        result = {
            "description": "",
            "constraints": [],
            "resources": [],
            "current_state": "",
            "desired_state": ""
        }

        # 提取目标描述
        desc_patterns = [
            r"目标[：:]\s*(.*)",
            r"Goal[：:]\s*(.*)",
            r"要做[：:]\s*(.*)",
            r"项目[：:]\s*(.*)"
        ]
        for pattern in desc_patterns:
            match = re.search(pattern, text)
            if match:
                result["description"] = match.group(1).strip()
                break
        if not result["description"]:
            # 取第一句话
            first_line = text.split('\n')[0] if '\n' in text else text
            result["description"] = first_line.strip()

        # 提取约束
        constraint_patterns = [
            r"约束[：:]\s*(.*)",
            r"不(.*)",
            r"避免(.*)",
            r"限制[：:]\s*(.*)"
        ]
        for pattern in constraint_patterns:
            matches = re.findall(pattern, text)
            for m in matches:
                result["constraints"].extend([c.strip() for c in m.split('，') if c.strip()])

        # 提取资源
        resource_patterns = [
            r"资源[：:]\s*(.*)",
            r"可用(.*)",
            r"有(.*)"
        ]
        for pattern in resource_patterns:
            matches = re.findall(pattern, text)
            for m in matches:
                result["resources"].extend([r.strip() for r in m.split('，') if r.strip()])

        # 如果没有提取到约束或资源，使用默认值
        if not result["constraints"]:
            result["constraints"] = ["不要过度设计", "先跑MVP"]
        if not result["resources"]:
            result["resources"] = ["Notion", "AI", "本地代码"]

        return result

# ============================================================
# 四、核心引擎：动态目标推进协议
# ============================================================

class DynamicGoalProtocol:
    """动态目标推进协议引擎"""

    def __init__(self):
        self.goal: Optional[Goal] = None
        self._plan: Optional[Plan] = None
        self.history: List[Dict] = []
        self.running = False
        self.executor = ThreadPoolExecutor(max_workers=2)
        self._lock = threading.Lock()
        self._load_state()

    def _load_state(self):
        """加载状态"""
        if STATE_PATH.exists():
            try:
                with open(STATE_PATH, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.history = data.get("history", [])
            except:
                pass

    def _save_state(self):
        """保存状态"""
        with open(STATE_PATH, 'w', encoding='utf-8') as f:
            json.dump({
                "history": self.history,
                "last_update": datetime.datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)

    def _generate_dna(self) -> str:
        """生成DNA追溯码"""
        today = datetime.datetime.now().strftime("%Y%m%d")
        hash_val = hashlib.sha256(
            f"{self.goal.description if self.goal else 'unknown'}{datetime.datetime.now().isoformat()}".encode()
        ).hexdigest()[:8]
        return f"#龍芯⚡️{today}-DGP-{hash_val.upper()}"

    def set_goal(self, description: str, constraints: List[str] = None,
                 resources: List[str] = None, current_state: str = "",
                 desired_state: str = "") -> Goal:
        """设置目标"""
        self.goal = Goal(
            description=description,
            constraints=constraints or ["不要过度设计", "先跑MVP"],
            resources=resources or ["Notion", "AI", "本地代码"],
            current_state=current_state or "只有概念",
            desired_state=desired_state or "可运行的MVP"
        )
        return self.goal

    def set_goal_from_text(self, text: str) -> Goal:
        """从文本解析并设置目标"""
        parsed = GoalParser.parse_goal_from_text(text)
        return self.set_goal(
            description=parsed["description"],
            constraints=parsed["constraints"],
            resources=parsed["resources"],
            current_state=parsed.get("current_state", "只有概念"),
            desired_state=parsed.get("desired_state", "可运行的MVP")
        )

    def plan(self, auto_execute: bool = False) -> Plan:
        """生成执行计划"""
        if not self.goal:
            raise ValueError("请先设置目标")

        dna = self._generate_dna()
        steps = self._generate_steps()
        self._plan = Plan(
            goal=self.goal,
            steps=steps,
            dna=dna,
            status="planning"
        )
        self._save_state()

        if auto_execute:
            self.execute()

        return self._plan

    def _generate_steps(self) -> List[Step]:
        """根据目标生成步骤"""
        steps = []

        # 根据目标类型生成步骤
        goal_desc = self.goal.description.lower()

        # 字体/字库类目标
        if "字体" in goal_desc or "字库" in goal_desc or "字元" in goal_desc:
            steps.extend([
                Step(
                    id=f"step_{uuid.uuid4().hex[:8]}",
                    description="定义字元格式和存储结构",
                    action_type="create",
                    params={"format": "JSON", "storage": "本地"}
                ),
                Step(
                    id=f"step_{uuid.uuid4().hex[:8]}",
                    description="建立字库基础数据（核心字元）",
                    action_type="create",
                    params={"count": 100, "type": "基础字元"}
                ),
                Step(
                    id=f"step_{uuid.uuid4().hex[:8]}",
                    description="实现简单渲染引擎（预览）",
                    action_type="create",
                    params={"output": "HTML"}
                ),
                Step(
                    id=f"step_{uuid.uuid4().hex[:8]}",
                    description="接入Notion作为数据存储和展示层",
                    action_type="deploy",
                    params={"platform": "Notion"}
                ),
                Step(
                    id=f"step_{uuid.uuid4().hex[:8]}",
                    description="测试并优化MVP",
                    action_type="test",
                    params={"scope": "端到端"}
                ),
            ])
        # 系统/架构类目标
        elif "系统" in goal_desc or "架构" in goal_desc or "框架" in goal_desc:
            steps.extend([
                Step(
                    id=f"step_{uuid.uuid4().hex[:8]}",
                    description="定义系统边界和核心模块",
                    action_type="create",
                    params={"type": "系统架构"}
                ),
                Step(
                    id=f"step_{uuid.uuid4().hex[:8]}",
                    description="实现核心模块原型",
                    action_type="create",
                    params={"type": "原型"}
                ),
                Step(
                    id=f"step_{uuid.uuid4().hex[:8]}",
                    description="连接各模块形成闭环",
                    action_type="modify",
                    params={"type": "集成"}
                ),
                Step(
                    id=f"step_{uuid.uuid4().hex[:8]}",
                    description="测试并部署到Notion",
                    action_type="deploy",
                    params={"platform": "Notion"}
                ),
            ])
        # AI/智能体类目标
        elif "AI" in goal_desc or "智能" in goal_desc or "自动化" in goal_desc:
            steps.extend([
                Step(
                    id=f"step_{uuid.uuid4().hex[:8]}",
                    description="定义AI行为边界和交互方式",
                    action_type="create",
                    params={"type": "交互协议"}
                ),
                Step(
                    id=f"step_{uuid.uuid4().hex[:8]}",
                    description="实现核心推理引擎（简化版）",
                    action_type="create",
                    params={"type": "推理引擎"}
                ),
                Step(
                    id=f"step_{uuid.uuid4().hex[:8]}",
                    description="接入工具和知识库",
                    action_type="modify",
                    params={"type": "工具集成"}
                ),
                Step(
                    id=f"step_{uuid.uuid4().hex[:8]}",
                    description="测试并迭代优化",
                    action_type="test",
                    params={"scope": "功能测试"}
                ),
            ])
        # 通用目标
        else:
            steps.extend([
                Step(
                    id=f"step_{uuid.uuid4().hex[:8]}",
                    description="分析需求，拆解核心问题",
                    action_type="create",
                    params={"type": "需求分析"}
                ),
                Step(
                    id=f"step_{uuid.uuid4().hex[:8]}",
                    description="设计最小可行方案",
                    action_type="create",
                    params={"type": "MVP设计"}
                ),
                Step(
                    id=f"step_{uuid.uuid4().hex[:8]}",
                    description="实现原型并验证",
                    action_type="create",
                    params={"type": "原型"}
                ),
                Step(
                    id=f"step_{uuid.uuid4().hex[:8]}",
                    description="优化并部署",
                    action_type="deploy",
                    params={"type": "部署"}
                ),
            ])

        # 根据约束调整步骤
        for constraint in self.goal.constraints:
            if "简单" in constraint or "不复杂" in constraint:
                # 简化步骤
                steps = [s for s in steps if "复杂" not in s.description and "深入" not in s.description]
            if "MVP" in constraint or "最小" in constraint:
                # 减少步骤数量
                steps = steps[:min(len(steps), 4)]

        return steps

    def execute(self) -> Plan:
        """执行计划（闭环推进）"""
        if not self._plan:
            self.plan()
            if not self._plan:
                raise ValueError("无法生成计划")

        self.running = True
        self._plan.status = "executing"

        while self.running and self._plan.current_step_index < len(self._plan.steps):
            step = self._plan.steps[self._plan.current_step_index]
            step.status = "running"
            step.updated_at = datetime.datetime.now().isoformat()

            print(f"\n🚀 执行步骤 {self._plan.current_step_index + 1}/{len(self._plan.steps)}: {step.description}")
            print(f"   操作: {step.action_type} | 参数: {step.params}")

            # 执行步骤（模拟实际执行）
            result = self._execute_step(step)

            if result.get("status") == "success":
                step.status = "success"
                step.result = result
                self._plan.current_step_index += 1
                print(f"   ✅ {step.description} 完成")

                # 检查是否达成目标
                if self._check_goal_achieved():
                    self._plan.status = "completed"
                    print("\n🎉 目标达成！")
                    break
            else:
                step.status = "failed"
                step.result = result
                step.feedback = result.get("feedback", "执行失败")

                # 调整策略（重新规划）
                print(f"   ❌ {step.description} 失败: {step.feedback}")
                print("   🔄 正在重新规划...")
                self._replan(step)
                continue

            # 记录进度
            self._save_state()
            self._log_history(f"步骤 {self._plan.current_step_index} 完成: {step.description}")

            # 短暂暂停，让用户看到进度
            time.sleep(1)

        if self._plan.status == "executing" and self._plan.current_step_index >= len(self._plan.steps):
            self._plan.status = "completed"
            print("\n🎉 所有步骤执行完成！")

        self.running = False
        self._save_state()
        return self._plan

    def _execute_step(self, step: Step) -> Dict[str, Any]:
        """执行单个步骤（模拟实际执行）"""
        # 模拟成功/失败概率
        if random.random() < 0.15:  # 15% 概率失败
            return {
                "status": "failed",
                "feedback": f"{step.description} 遇到问题，需要调整方案",
                "error": "模拟执行错误"
            }

        # 模拟执行结果
        result = {
            "status": "success",
            "step_id": step.id,
            "executed_at": datetime.datetime.now().isoformat(),
            "message": f"{step.description} 执行成功",
            "artifacts": self._generate_artifacts(step)
        }
        return result

    def _generate_artifacts(self, step: Step) -> List[Dict]:
        """生成模拟产物"""
        artifacts = []
        if step.action_type == "create":
            artifacts.append({
                "type": "文件",
                "name": f"{step.description.replace(' ', '_')}.md",
                "content": f"# {step.description}\n\n自动生成的产物"
            })
        elif step.action_type == "deploy":
            artifacts.append({
                "type": "部署",
                "platform": step.params.get("platform", "Notion"),
                "status": "已部署"
            })
        elif step.action_type == "test":
            artifacts.append({
                "type": "测试报告",
                "passed": random.randint(5, 15),
                "failed": random.randint(0, 2)
            })
        return artifacts

    def _replan(self, failed_step: Step):
        """重新规划（调整策略）"""
        self._plan.iteration += 1

        # 生成替代步骤
        alternatives = [
            f"简化 {failed_step.description}",
            f"重新设计 {failed_step.description}",
            f"使用替代方案 {failed_step.description}",
            f"拆分 {failed_step.description} 为更小步骤"
        ]

        # 选择替代方案
        alt_description = random.choice(alternatives)
        new_step = Step(
            id=f"step_alt_{uuid.uuid4().hex[:8]}",
            description=f"{failed_step.description} (替代方案)",
            action_type=failed_step.action_type,
            params={**failed_step.params, "alternative": alt_description}
        )

        # 替换失败步骤
        self._plan.steps[self._plan.current_step_index] = new_step
        self._plan.status = "planning"
        print(f"   📋 替换为: {new_step.description}")
        self._log_history(f"重新规划: {failed_step.description} → {new_step.description}")

    def _check_goal_achieved(self) -> bool:
        """检查目标是否达成"""
        # 简化：如果所有步骤都成功，认为目标达成
        all_success = all(s.status == "success" for s in self._plan.steps)
        return all_success

    def pause(self):
        """暂停执行"""
        self.running = False
        if self._plan:
            self._plan.status = "paused"
        print("⏸️ 已暂停")

    def resume(self):
        """恢复执行"""
        if not self._plan:
            print("❌ 没有计划可恢复")
            return
        if self._plan.status == "paused":
            self._plan.status = "executing"
            self.running = True
            print("▶️ 已恢复")
            self.execute()
        else:
            print(f"❌ 计划状态为 {self._plan.status}，无法恢复")

    def status(self) -> Dict:
        """获取当前状态"""
        if not self._plan:
            return {"status": "no_plan", "message": "尚未生成计划"}

        progress = self._plan.current_step_index / max(len(self._plan.steps), 1)
        return {
            "status": self._plan.status,
            "goal": self.goal.description if self.goal else "",
            "total_steps": len(self._plan.steps),
            "completed_steps": self._plan.current_step_index,
            "progress": f"{progress*100:.1f}%",
            "iteration": self._plan.iteration,
            "dna": self._plan.dna,
            "current_step": self._plan.steps[self._plan.current_step_index].description if self._plan.current_step_index < len(self._plan.steps) else None
        }

    def report(self) -> str:
        """生成执行报告"""
        if not self._plan:
            return "❌ 无计划"

        report = []
        report.append("=" * 60)
        report.append(f"🐉 动态目标推进协议 · 执行报告")
        report.append("=" * 60)
        report.append(f"🧬 DNA: {self._plan.dna}")
        report.append(f"🎯 目标: {self.goal.description}")
        report.append(f"📊 状态: {self._plan.status}")
        report.append(f"🔄 迭代: {self._plan.iteration}")
        report.append("-" * 40)
        report.append("📋 步骤:")
        for i, step in enumerate(self._plan.steps, 1):
            status_icon = "✅" if step.status == "success" else "❌" if step.status == "failed" else "⏳" if step.status == "running" else "⏸️"
            report.append(f"  {i}. {status_icon} {step.description}")
            if step.status == "success":
                report.append(f"     结果: {step.result.get('message', '') if step.result else ''}")
            elif step.status == "failed":
                report.append(f"     失败: {step.feedback}")
        report.append("-" * 40)
        report.append(f"📈 进度: {self.status()['progress']}")
        report.append(f"📊 约束: {', '.join(self.goal.constraints)}")
        report.append(f"📦 资源: {', '.join(self.goal.resources)}")
        report.append("=" * 60)
        return "\n".join(report)

    def _log_history(self, entry: str):
        """记录历史"""
        record = {
            "timestamp": datetime.datetime.now().isoformat(),
            "entry": entry,
            "dna": self._plan.dna if self._plan else ""
        }
        self.history.append(record)
        with open(HISTORY_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')

    def get_history(self, limit: int = 20) -> List[Dict]:
        """获取历史记录"""
        return self.history[-limit:]

# ============================================================
# 五、交互式命令行
# ============================================================

def interactive():
    """交互式模式"""
    protocol = DynamicGoalProtocol()

    print("\n" + "=" * 60)
    print("🐉 龍魂·动态目标推进协议 v1.0")
    print("=" * 60)
    print("目标驱动 + 自适应规划 + 闭环执行")
    print("=" * 60)
    print("命令:")
    print("  set <目标描述>        - 设置目标")
    print("  plan                  - 生成执行计划")
    print("  exec                  - 执行计划")
    print("  pause                 - 暂停执行")
    print("  resume                - 恢复执行")
    print("  status                - 查看状态")
    print("  report                - 生成报告")
    print("  history               - 查看历史")
    print("  exit                  - 退出")
    print("-" * 60)

    while True:
        try:
            user_input = input("\n🤖 > ").strip()
            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit']:
                print("👋 龙魂永存")
                break

            if user_input.startswith("set "):
                text = user_input[4:].strip()
                protocol.set_goal_from_text(text)
                print(f"✅ 目标已设置: {protocol.goal.description}")
                print(f"   📋 约束: {', '.join(protocol.goal.constraints)}")
                print(f"   📦 资源: {', '.join(protocol.goal.resources)}")
                continue

            if user_input.lower() == "plan":
                if not protocol.goal:
                    print("❌ 请先设置目标 (set 目标描述)")
                    continue
                plan = protocol.plan()
                print(f"✅ 计划已生成: {len(plan.steps)} 个步骤")
                for i, step in enumerate(plan.steps, 1):
                    print(f"  {i}. {step.description}")
                continue

            if user_input.lower() == "exec":
                if not protocol.plan:
                    print("❌ 请先生成计划 (plan)")
                    continue
                # 在后台线程执行
                threading.Thread(target=protocol.execute, daemon=True).start()
                print("▶️ 开始执行...")
                continue

            if user_input.lower() == "pause":
                protocol.pause()
                continue

            if user_input.lower() == "resume":
                protocol.resume()
                continue

            if user_input.lower() == "status":
                status = protocol.status()
                if status.get("status") == "no_plan":
                    print("📭 尚无计划")
                else:
                    print(f"📊 状态: {status['status']}")
                    print(f"🎯 目标: {status['goal']}")
                    print(f"📈 进度: {status['progress']}")
                    print(f"🔄 迭代: {status['iteration']}")
                    print(f"🧬 DNA: {status['dna']}")
                    if status.get('current_step'):
                        print(f"⏳ 当前步骤: {status['current_step']}")
                continue

            if user_input.lower() == "report":
                print(protocol.report())
                continue

            if user_input.lower() == "history":
                history = protocol.get_history(limit=10)
                if not history:
                    print("📭 暂无历史记录")
                else:
                    print("📋 最近历史:")
                    for h in history[-10:]:
                        print(f"  {h['timestamp'][:19]} - {h['entry']}")
                continue

            print("❌ 未知命令")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ 错误: {e}")

# ============================================================
# 六、命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·动态目标推进协议 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 交互模式
  python3 lh_dynamic_goal.py --interactive

  # 直接运行目标
  python3 lh_dynamic_goal.py --goal "做一个CNSH字体系统" --constraints "不复杂" "先跑MVP"

  # 从文件加载目标
  python3 lh_dynamic_goal.py --file goal.txt

  # 查看状态
  python3 lh_dynamic_goal.py --status

  # JSON输出
  python3 lh_dynamic_goal.py --goal "构建AI助手" --json
        """
    )

    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--goal", "-g", type=str, help="目标描述")
    parser.add_argument("--constraints", "-c", nargs="+", help="约束条件")
    parser.add_argument("--resources", "-r", nargs="+", help="可用资源")
    parser.add_argument("--file", "-f", type=str, help="从文件加载目标")
    parser.add_argument("--status", "-s", action="store_true", help="查看状态")
    parser.add_argument("--json", "-j", action="store_true", help="JSON输出")
    parser.add_argument("--execute", "-e", action="store_true", help="生成计划后自动执行")

    args = parser.parse_args()

    if args.interactive:
        interactive()
        return

    protocol = DynamicGoalProtocol()

    if args.status:
        status = protocol.status()
        if args.json:
            print(json.dumps(status, ensure_ascii=False, indent=2))
        else:
            print(f"📊 状态: {status.get('status', '无')}")
            print(f"🎯 目标: {status.get('goal', '未设置')}")
            print(f"📈 进度: {status.get('progress', '0%')}")
            print(f"🧬 DNA: {status.get('dna', '')}")
        return

    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
            protocol.set_goal_from_text(text)
        except Exception as e:
            print(f"❌ 读取文件失败: {e}")
            return
    elif args.goal:
        constraints = args.constraints or ["不要过度设计", "先跑MVP"]
        resources = args.resources or ["Notion", "AI", "本地代码"]
        protocol.set_goal(
            description=args.goal,
            constraints=constraints,
            resources=resources
        )
    else:
        parser.print_help()
        return

    plan = protocol.plan(auto_execute=args.execute)

    if args.json:
        print(json.dumps(plan.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(f"\n✅ 计划已生成: {len(plan.steps)} 个步骤")
        for i, step in enumerate(plan.steps, 1):
            print(f"  {i}. {step.description}")
        print(f"\n🧬 DNA: {plan.dna}")

        if args.execute:
            print("\n▶️ 开始执行...")
            # 等待执行完成（简化版）
            while plan.status in ["planning", "executing"]:
                time.sleep(2)
                if plan.status == "completed":
                    print("\n🎉 目标达成！")
                    print(protocol.report())
                    break


if __name__ == "__main__":
    main()
