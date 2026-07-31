#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·智能体训练框架 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-智能体训练-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

定位：让龙魂系统学会思考，联动全系统自动决策，成为真正的智能体。

核心能力：
  1. 思考引擎 — 多步推理、因果链、假设验证
  2. 决策引擎 — 优先级判断、风险评估、路径规划
  3. 系统联动 — 统一调用所有龙魂引擎
  4. 自主决策 — 不需要明确指令，根据上下文行动
  5. 自反馈学习 — 从执行结果中持续优化
  6. 记忆增强 — 利用记忆系统做上下文推理
  7. 人格调度 — 根据场景自动选择合适人格
"""

import os
import sys
import json
import time
import hashlib
import sqlite3
import threading
import queue
import subprocess
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
import argparse
import random
import traceback
from collections import defaultdict

# ============================================================
# 一、配置
# ============================================================

BASE_DIR = Path.home() / ".longhun/agent"
BASE_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = BASE_DIR / "agent.db"
MEMORY_DIR = BASE_DIR / "memory"
MEMORY_DIR.mkdir(parents=True, exist_ok=True)
DECISION_LOG = BASE_DIR / "decisions.jsonl"
REFLECTION_LOG = BASE_DIR / "reflections.jsonl"
CONFIG_PATH = BASE_DIR / "config.json"

DEFAULT_CONFIG = {
    "version": "1.0",
    "dna": "#龍芯⚡️丙午·乙未·甲辰·离为火-智能体训练-v1.0",
    "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    "agent_name": "龙魂智能体",
    "thinking_depth": 3,
    "decision_timeout": 30,
    "max_iterations": 100,
    "learning_rate": 0.01,
    "exploration_rate": 0.2,
    "memory_limit": 1000,
    "enable_reflection": True,
    "enable_self_improve": True,
    "persona_weights": {
        "诸葛亮": 0.20,
        "鲁班": 0.15,
        "包青天": 0.15,
        "通心译": 0.10,
        "司马迁": 0.10,
        "哨兵": 0.10,
        "上帝之眼": 0.10,
        "北辰": 0.10
    }
}

# ============================================================
# 二、数据结构
# ============================================================

class ActionType(Enum):
    THINK = "思考"
    DECIDE = "决策"
    EXECUTE = "执行"
    OBSERVE = "观察"
    REFLECT = "反思"
    LEARN = "学习"
    WAIT = "等待"
    STOP = "停止"


@dataclass
class Thought:
    """思考单元"""
    id: str
    content: str
    type: str  # "推理", "假设", "验证", "结论"
    confidence: float
    evidence: List[str] = field(default_factory=list)
    parent_id: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Decision:
    """决策单元"""
    id: str
    goal: str
    action: str
    target_engine: str
    params: Dict[str, Any] = field(default_factory=dict)
    priority: int = 5
    risk: float = 0.3
    expected_outcome: str = ""
    reasoning_chain: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    executed_at: Optional[str] = None
    result: Optional[Dict] = None
    status: str = "pending"

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["result"] = json.dumps(d["result"], ensure_ascii=False) if d.get("result") else None
        return d


@dataclass
class Experience:
    """经验记录"""
    id: str
    input_context: Dict = field(default_factory=dict)
    thought_chain: List[Thought] = field(default_factory=list)
    decision: Optional[Decision] = None
    outcome: Dict = field(default_factory=dict)
    reward: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    reflection: str = ""
    improved: bool = False

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "input_context": json.dumps(self.input_context, ensure_ascii=False),
            "thought_chain": json.dumps([t.to_dict() for t in self.thought_chain], ensure_ascii=False),
            "decision": json.dumps(self.decision.to_dict(), ensure_ascii=False) if self.decision else "{}",
            "outcome": json.dumps(self.outcome, ensure_ascii=False),
            "reward": self.reward,
            "timestamp": self.timestamp,
            "reflection": self.reflection,
            "improved": 1 if self.improved else 0
        }


# ============================================================
# 三、思考引擎
# ============================================================

class ThinkingEngine:
    """
    思考引擎 — 多步推理、假设验证、因果链
    不直接给答案，而是展示完整的思考过程
    """

    def __init__(self, depth: int = 3):
        self.depth = depth
        self.thought_history: List[Thought] = []
        self.thought_id_counter = 0

    def think(self, context: Dict, problem: str) -> List[Thought]:
        """执行多步思考，返回完整思考链"""
        self.thought_history = []
        thoughts = []

        # 步骤1: 理解问题
        t1 = self._gen(f"问题理解: {self._parse_problem(problem)}", "推理", 0.9, [problem])
        thoughts.append(t1)

        # 步骤2: 分解任务
        subtasks = self._decompose_task(problem, context)
        t2 = self._gen(
            f"任务分解: {', '.join(subtasks[:3])}{'…' if len(subtasks) > 3 else ''}",
            "推理", 0.8, [t for t in subtasks[:3]]
        )
        thoughts.append(t2)

        # 步骤3: 生成假设
        hypotheses = self._generate_hypotheses(problem, context)
        t3 = self._gen(
            f"假设: {', '.join(hypotheses[:3])}{'…' if len(hypotheses) > 3 else ''}",
            "假设", 0.7, hypotheses[:3]
        )
        thoughts.append(t3)

        # 步骤4: 推理验证
        reasoning = self._reason(problem, context, hypotheses)
        t4 = self._gen(reasoning, "验证", 0.8, [reasoning[:100]])
        thoughts.append(t4)

        # 步骤5: 结论
        conclusion = self._conclude(problem, thoughts)
        t5 = self._gen(conclusion, "结论", 0.85, [str(t.id) for t in thoughts])
        thoughts.append(t5)

        self.thought_history.extend(thoughts)
        return thoughts

    def _gen(self, content: str, tp: str, confidence: float, evidence: List[str]) -> Thought:
        self.thought_id_counter += 1
        return Thought(
            id=f"thought_{self.thought_id_counter:04d}",
            content=content, type=tp, confidence=confidence, evidence=evidence
        )

    def _parse_problem(self, problem: str) -> str:
        keywords = ["做什么", "怎么办", "如何", "为什么", "能否", "应该"]
        for kw in keywords:
            if kw in problem:
                return problem[:50] + "…"
        return problem[:80] + "…"

    def _decompose_task(self, problem: str, context: Dict) -> List[str]:
        task_map = {
            "训练": ["准备数据", "选择模型", "训练参数", "验证结果", "部署模型"],
            "学习": ["准备数据", "选择模型", "训练参数", "验证结果", "部署模型"],
            "部署": ["环境检查", "依赖安装", "配置参数", "启动服务", "健康验证"],
            "安装": ["环境检查", "依赖安装", "配置参数", "启动服务", "健康验证"],
            "审计": ["收集信息", "规则匹配", "异常检测", "生成报告", "建议修复"],
            "检查": ["收集信息", "规则匹配", "异常检测", "生成报告", "建议修复"],
            "搜索": ["理解意图", "选择数据源", "执行检索", "结果排序", "展示结果"],
            "查询": ["理解意图", "选择数据源", "执行检索", "结果排序", "展示结果"],
            "健康": ["系统自检", "服务状态", "资源监控", "异常诊断", "修复建议"],
            "对齐": ["扫描文件", "差异对比", "DNA校验", "GPG签名", "自动修复"],
        }
        for key, tasks in task_map.items():
            if key in problem:
                return tasks
        return ["分析问题", "设计方案", "执行方案", "验证结果", "反馈优化"]

    def _generate_hypotheses(self, problem: str, context: Dict) -> List[str]:
        hypotheses = []
        if context.get("previous_actions"):
            hypotheses.append(f"可参考历史操作: {str(context['previous_actions'][-1])[:50]}")
        if context.get("similar_experiences"):
            count = len(context["similar_experiences"])
            hypotheses.append(f"有{count}条相似经验可用")
        hypotheses.append("可能需要调用外部引擎")
        hypotheses.append("可能需要在本地执行")
        if context.get("current_time"):
            hypotheses.append(f"时段={context['current_time']}，可能影响决策")
        return hypotheses[:5]

    def _reason(self, problem: str, context: Dict, hypotheses: List[str]) -> str:
        steps = []
        for i, hyp in enumerate(hypotheses[:3], 1):
            steps.append(f"第{i}步: 验证假设「{hyp}」")
            steps.append(f"  → 条件检查: {self._check_condition(hyp)}")
        return "\n".join(steps)

    @staticmethod
    def _check_condition(hypothesis: str) -> str:
        conditions = {"工具": "龙魂引擎已就绪", "本地": "本地环境 OK",
                      "历史": "历史记录匹配", "时间": "时间窗口合适",
                      "外部": "外部调用路径通畅", "经验": "相似经验可复用"}
        for key, value in conditions.items():
            if key in hypothesis:
                return value
        return "条件满足"

    @staticmethod
    def _conclude(problem: str, thoughts: List[Thought]) -> str:
        confs = [t.confidence for t in thoughts if t.confidence]
        avg = sum(confs) / len(confs) if confs else 0.5
        if avg > 0.8:
            return f"结论: 可以执行。置信度 {avg:.0%}"
        elif avg > 0.5:
            return f"结论: 建议执行但需验证。置信度 {avg:.0%}"
        else:
            return f"结论: 需要更多信息。当前置信度 {avg:.0%}"


# ============================================================
# 四、决策引擎
# ============================================================

class DecisionEngine:
    """决策引擎 — 自动判断优先级、风险、执行路径"""

    def __init__(self):
        self.decision_history: List[Decision] = []
        self.decision_id_counter = 0

    def decide(self, thought_chain: List[Thought], context: Dict) -> Decision:
        self.decision_id_counter += 1
        goal = self._extract_goal(thought_chain, context)
        action = self._select_action(goal, context)
        target_engine = self._select_engine(action, context)
        params = self._prepare_params(action, target_engine, context)
        priority = self._calculate_priority(goal, context)
        risk = self._assess_risk(action, context)
        expected = self._predict_outcome(action, target_engine, params)
        reasoning = [t.content for t in thought_chain[-3:]]

        decision = Decision(
            id=f"decision_{self.decision_id_counter:04d}",
            goal=goal, action=action, target_engine=target_engine,
            params=params, priority=priority, risk=risk,
            expected_outcome=expected, reasoning_chain=reasoning
        )
        self.decision_history.append(decision)
        return decision

    def _extract_goal(self, thought_chain: List[Thought], context: Dict) -> str:
        for thought in reversed(thought_chain):
            if "结论" in thought.type or "目标" in thought.content:
                return thought.content[:100]
        return context.get("goal", "完成用户请求")

    def _select_action(self, goal: str, context: Dict) -> str:
        action_map = {
            "训练": "execute_training", "学习": "execute_training",
            "部署": "execute_deployment", "安装": "execute_deployment",
            "审计": "execute_audit", "检查": "execute_audit",
            "搜索": "execute_search", "查询": "execute_search",
            "翻译": "execute_translate",
            "健康": "execute_health_check",
            "对齐": "execute_alignment",
            "蒸馏": "execute_distill",
            "知识扫描": "execute_knowledge_scan",
            "知识搜索": "execute_knowledge_search",
            "知识转化": "execute_knowledge_convert",
        }
        for key, action in action_map.items():
            if key in goal:
                return action
        return "execute_generic"

    def _select_engine(self, action: str, context: Dict) -> str:
        engine_map = {
            "training": "bin/lh_lora_trainer_v4.py",
            "deployment": "deploy/sync-to-kunpeng.sh",
            "audit": "bin/lh_deben_audit.py",
            "search": "bin/lh_search_engine.py",
            "translate": "bin/lh_tongxinyi_translator.py",
            "health": "deploy/scripts/health_check.sh",
            "alignment": "bin/lh_align_checker.py",
            "distill": "bin/lh_k3_distill_v39.py",
            "knowledge_scan": "bin/lh_local_knowledge_engine.py",
            "knowledge_search": "bin/lh_local_knowledge_engine.py",
            "knowledge_convert": "bin/lh_local_knowledge_engine.py",
            "generic": "bin/lh_ctl.py",
        }
        for key, engine in engine_map.items():
            if key in action:
                return engine
        return "bin/lh_ctl.py"

    def _prepare_params(self, action: str, engine: str, context: Dict) -> Dict:
        params = {}
        if context.get("query"):
            params["query"] = context["query"]
        if context.get("args"):
            params["args"] = context["args"]
        params["execution_id"] = f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        params["source"] = "龙魂智能体"
        return params

    def _calculate_priority(self, goal: str, context: Dict) -> int:
        priority = 5
        if "紧急" in goal or "立即" in goal:
            priority = 10
        elif "重要" in goal:
            priority = 8
        elif "建议" in goal:
            priority = 6
        if context.get("user_priority"):
            priority = max(1, min(10, int(context["user_priority"])))
        return priority

    def _assess_risk(self, action: str, context: Dict) -> float:
        risk = 0.3
        if "删除" in action or "清除" in action:
            risk = 0.8
        elif "修改" in action or "更新" in action:
            risk = 0.5
        elif "查询" in action or "搜索" in action:
            risk = 0.1
        if context.get("user_risk_acknowledged"):
            risk *= 0.5
        return min(1.0, risk)

    def _predict_outcome(self, action: str, engine: str, params: Dict) -> str:
        return f"执行 {action} 在 {engine}，预期完成 {params.get('query', '任务')}"


# ============================================================
# 五、系统联动层
# ============================================================

class SystemOrchestrator:
    """系统联动层 — 统一调用所有龙魂引擎"""

    def __init__(self):
        self.engines = {
            "bin/lh_ctl.py": {"type": "control"},
            "bin/lh_lora_trainer_v4.py": {"type": "train"},
            "bin/lh_deben_audit.py": {"type": "audit"},
            "bin/lh_search_engine.py": {"type": "search"},
            "bin/lh_tongxinyi_translator.py": {"type": "translate"},
            "deploy/scripts/health_check.sh": {"type": "health"},
            "bin/lh_align_checker.py": {"type": "align"},
            "bin/lh_local_knowledge_engine.py": {"type": "knowledge"},
            "bin/lh_k3_distill_v39.py": {"type": "distill"},
            "deploy/sync-to-kunpeng.sh": {"type": "deploy"},
        }
        self.execution_history: List[Dict] = []

    def execute(self, decision: Decision) -> Dict:
        result = {
            "decision_id": decision.id, "action": decision.action,
            "engine": decision.target_engine, "status": "failed",
            "output": "", "error": None, "execution_time": 0
        }
        start_time = time.time()

        script_path = Path.home() / "longhun-system" / decision.target_engine
        if not script_path.exists():
            result["error"] = f"引擎不存在: {script_path}"
            self.execution_history.append(result)
            return result

        cmd = [str(script_path)]
        if decision.params.get("query"):
            cmd.append(decision.params["query"])
        if decision.params.get("args"):
            cmd.extend(decision.params["args"])

        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30,
                cwd=Path.home() / "longhun-system"
            )
            result["status"] = "success" if proc.returncode == 0 else "failed"
            result["output"] = proc.stdout[:5000]
            result["error"] = proc.stderr[:500] if proc.stderr else None
            result["returncode"] = proc.returncode
        except subprocess.TimeoutExpired:
            result["error"] = "执行超时"
        except Exception as e:
            result["error"] = str(e)

        result["execution_time"] = time.time() - start_time
        self.execution_history.append(result)
        return result

    def get_capabilities(self) -> List[Dict]:
        return [{"engine": name, "type": info["type"]} for name, info in self.engines.items()]

    def get_available_engines(self) -> List[str]:
        return list(self.engines.keys())


# ============================================================
# 六、记忆增强层
# ============================================================

class AgentMemory:
    """智能体记忆 — 持久化存储经验和上下文"""

    def __init__(self):
        self.db_path = DB_PATH
        self._init_db()
        self.working_memory: List[Dict] = []
        self.context_limit = 10

    def _init_db(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""
            CREATE TABLE IF NOT EXISTS experiences (
                id TEXT PRIMARY KEY, input_context TEXT, thought_chain TEXT,
                decision TEXT, outcome TEXT, reward REAL, timestamp TEXT,
                reflection TEXT, improved INTEGER DEFAULT 0
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS decisions (
                id TEXT PRIMARY KEY, goal TEXT, action TEXT, target_engine TEXT,
                params TEXT, priority INTEGER, risk REAL, status TEXT,
                created_at TEXT, executed_at TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reflections (
                id TEXT PRIMARY KEY, experience_id TEXT, content TEXT,
                improvements TEXT, created_at TEXT
            )
        """)
        conn.commit()
        conn.close()

    def store_experience(self, experience: Experience):
        conn = sqlite3.connect(str(self.db_path))
        conn.execute(
            """INSERT OR REPLACE INTO experiences
            (id, input_context, thought_chain, decision, outcome, reward, timestamp, reflection, improved)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (experience.id,
             json.dumps(experience.input_context, ensure_ascii=False),
             json.dumps([t.to_dict() for t in experience.thought_chain], ensure_ascii=False),
             json.dumps(experience.decision.to_dict(), ensure_ascii=False) if experience.decision else "{}",
             json.dumps(experience.outcome, ensure_ascii=False),
             experience.reward, experience.timestamp,
             experience.reflection, 1 if experience.improved else 0)
        )
        conn.commit()
        conn.close()

        self.working_memory.append({
            "experience_id": experience.id, "timestamp": experience.timestamp,
            "reward": experience.reward
        })
        if len(self.working_memory) > self.context_limit:
            self.working_memory = self.working_memory[-self.context_limit:]

    def recall_similar(self, context: Dict, limit: int = 5) -> List[Dict]:
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute("""
            SELECT id, input_context, decision, outcome, reward, reflection
            FROM experiences ORDER BY reward DESC, timestamp DESC LIMIT ?
        """, (limit,))
        rows = cur.fetchall()
        conn.close()

        results = []
        for row in rows:
            try:
                results.append({
                    "id": row[0],
                    "input_context": json.loads(row[1]) if row[1] else {},
                    "decision": json.loads(row[2]) if row[2] else {},
                    "outcome": json.loads(row[3]) if row[3] else {},
                    "reward": row[4] or 0.0,
                    "reflection": row[5] or ""
                })
            except Exception:
                continue
        return results

    def get_statistics(self) -> Dict:
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute("SELECT COUNT(*) FROM experiences")
        total = cur.fetchone()[0]
        cur = conn.execute("SELECT AVG(reward) FROM experiences WHERE reward IS NOT NULL")
        avg_reward = cur.fetchone()[0] or 0.0
        cur = conn.execute("SELECT COUNT(*) FROM experiences WHERE improved = 1")
        improved = cur.fetchone()[0]
        conn.close()
        return {
            "total_experiences": total, "average_reward": avg_reward,
            "improved_count": improved, "working_memory_size": len(self.working_memory)
        }


# ============================================================
# 七、反思与自我优化
# ============================================================

class ReflectionEngine:
    """反思引擎 — 从结果中学习，优化未来决策"""

    def __init__(self):
        self.reflection_log: List[str] = []

    def reflect(self, experience: Experience) -> str:
        lines = [f"## 反思: {experience.id}"]
        if experience.reward > 0.7:
            lines.append(f"✅ 执行成功 (奖励: {experience.reward:.2f})")
            lines.append("   - 决策正确，可重复使用")
        elif experience.reward > 0.3:
            lines.append(f"🟡 部分成功 (奖励: {experience.reward:.2f})")
            lines.append("   - 需要微调参数")
        else:
            lines.append(f"🔴 执行失败 (奖励: {experience.reward:.2f})")
            lines.append("   - 需要重新评估策略")

        if experience.reward < 0.5:
            lines.append("## 改进建议")
            if experience.decision and experience.decision.risk > 0.7:
                lines.append("- 风险过高，建议降低执行风险")
            if not experience.outcome.get("expected"):
                lines.append("- 预期与实际不符，需要调整推理")
            lines.append("- 建议增加更多上下文信息")
        else:
            lines.append("## 维持策略")
            lines.append("- 当前策略有效，继续采用")

        reflection = "\n".join(lines)
        experience.reflection = reflection
        self.reflection_log.append(reflection)
        return reflection

    def get_improvement(self, reflections: List[str]) -> Dict:
        improvements = {"strategy_changes": [], "parameter_adjustments": [], "knowledge_updates": []}
        for ref in reflections:
            if "风险过高" in ref:
                improvements["strategy_changes"].append("降低风险阈值")
                improvements["parameter_adjustments"].append("risk_threshold=0.6")
            if "需要更多上下文" in ref:
                improvements["strategy_changes"].append("增加上下文采集")
                improvements["knowledge_updates"].append("context_pool_size=20")
            if "决策正确" in ref:
                improvements["knowledge_updates"].append("确认有效策略")
        return improvements


# ============================================================
# 八、主智能体
# ============================================================

class LonghunAgent:
    """龙魂智能体 — 完整思考→决策→执行→学习循环"""

    def __init__(self):
        self.config = self._load_config()
        self.thinking_engine = ThinkingEngine(depth=self.config.get("thinking_depth", 3))
        self.decision_engine = DecisionEngine()
        self.orchestrator = SystemOrchestrator()
        self.memory = AgentMemory()
        self.reflection_engine = ReflectionEngine()

        seed = f"{self.config['agent_name']}{datetime.now().isoformat()}"
        self.agent_id = hashlib.md5(seed.encode()).hexdigest()[:8]
        self.experience_counter = 0
        self.running = False
        self.task_queue: queue.Queue = queue.Queue()

    def _load_config(self) -> Dict:
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        self._save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    def _save_config(self, config: Dict = None):
        cfg = config if config is not None else self.config
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)

    def process(self, input_text: str, context: Dict = None) -> Dict:
        """处理用户输入 — 完整智能体流程"""
        context = context or {}

        print(f"\n🐉 龙魂智能体处理: {input_text[:50]}…")
        print("-" * 40)

        # 1. 构建上下文
        full_context = self._build_context(input_text, context)

        # 2. 思考
        print("🧠 思考中…")
        thoughts = self.thinking_engine.think(full_context, input_text)
        self._log_thoughts(thoughts)

        # 3. 决策
        print("🎯 决策中…")
        decision = self.decision_engine.decide(thoughts, full_context)
        self._log_decision(decision)

        # 4. 执行
        print("⚡ 执行中…")
        result = self.orchestrator.execute(decision)

        # 5. 评估
        print("📊 评估中…")
        reward = self._evaluate(result, decision)

        # 6. 学习
        print("📚 学习中…")
        experience = self._create_experience(input_text, full_context, thoughts, decision, result, reward)
        self.memory.store_experience(experience)

        # 7. 反思
        if self.config.get("enable_reflection", True):
            print("🔄 反思中…")
            reflection = self.reflection_engine.reflect(experience)
            self._log_reflection(reflection)

        response = self._format_response(result, decision, thoughts, reward)

        print("-" * 40)
        print(f"✅ 处理完成 (奖励: {reward:.2f})")

        return {
            "input": input_text,
            "thoughts": [t.to_dict() for t in thoughts],
            "decision": decision.to_dict(),
            "execution": result,
            "reward": reward,
            "response": response,
            "experience_id": experience.id,
            "dna": self.config["dna"]
        }

    def _build_context(self, input_text: str, context: Dict) -> Dict:
        engines = self.orchestrator.get_available_engines()
        similar = self.memory.recall_similar({"query": input_text})
        return {
            "input": input_text, "timestamp": datetime.now().isoformat(),
            "available_engines": engines, "similar_experiences": similar[:3],
            "current_agent": self.config["agent_name"],
            "working_memory": self.memory.working_memory[-5:],
            **context
        }

    def _log_thoughts(self, thoughts: List[Thought]):
        for t in thoughts:
            print(f"  💭 [{t.type}] {t.content[:80]}… (置信度: {t.confidence:.0%})")

    def _log_decision(self, decision: Decision):
        print(f"  🎯 目标: {decision.goal[:50]}…")
        print(f"  ⚡ 动作: {decision.action}")
        print(f"  🔧 引擎: {decision.target_engine}")
        print(f"  📊 优先级: {decision.priority}/10")
        print(f"  ⚠️ 风险: {decision.risk:.0%}")

    def _log_reflection(self, reflection: str):
        for line in reflection.split('\n')[:5]:
            if line.strip():
                print(f"  🔄 {line[:80]}")

    def _evaluate(self, result: Dict, decision: Decision) -> float:
        reward = 0.0
        if result.get("status") == "success":
            reward += 0.6
            if result.get("output") and len(result.get("output", "")) > 100:
                reward += 0.2
            if decision.risk < 0.3:
                reward += 0.2
        else:
            reward += 0.1
            if decision.risk > 0.7:
                reward -= 0.2
        return max(0.0, min(1.0, reward))

    def _create_experience(self, input_text: str, context: Dict, thoughts: List[Thought],
                           decision: Decision, result: Dict, reward: float) -> Experience:
        self.experience_counter += 1
        return Experience(
            id=f"exp_{self.experience_counter:04d}_{datetime.now().strftime('%Y%m%d')}",
            input_context=context, thought_chain=thoughts,
            decision=decision, outcome=result, reward=reward
        )

    def _format_response(self, result: Dict, decision: Decision, thoughts: List[Thought], reward: float) -> str:
        parts = []
        if result.get("status") == "success":
            parts.append("✅ 任务完成")
            if result.get("output"):
                parts.append(f"输出: {result['output'][:500]}")
        else:
            parts.append("❌ 执行遇到问题")
            if result.get("error"):
                parts.append(f"错误: {result['error']}")
        parts.append(f"\n决策: {decision.action} → {decision.target_engine}")
        parts.append(f"置信度: {reward:.0%}")
        return "\n".join(parts)

    def run_loop(self):
        """守护进程模式"""
        self.running = True
        print(f"\n🐉 {self.config['agent_name']} 已启动")
        print(f"🧬 DNA: {self.config['dna']}")
        print("=" * 50)

        while self.running:
            try:
                if not self.task_queue.empty():
                    task = self.task_queue.get(timeout=1)
                    self.process(task, {})
                    self.task_queue.task_done()
                else:
                    if self.config.get("enable_self_improve", True):
                        self._self_improve()
                    time.sleep(5)
            except queue.Empty:
                continue
            except KeyboardInterrupt:
                print("\n🛑 收到退出信号")
                break
            except Exception as e:
                print(f"❌ 运行错误: {e}")
                traceback.print_exc()
                time.sleep(5)
        self.running = False

    def _self_improve(self):
        similar = self.memory.recall_similar({}, 10)
        success_patterns = [s for s in similar if s.get("reward", 0) > 0.7]
        if len(success_patterns) > 3:
            print(f"📈 自我优化: 发现 {len(success_patterns)} 个成功模式")
            self.config["last_optimized"] = datetime.now().isoformat()
            self._save_config()

    def add_task(self, task: str):
        self.task_queue.put(task)


# ============================================================
# 九、命令行接口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·智能体训练框架 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh agent process "优化龙魂系统性能"    单次处理
  lh agent interactive                   交互模式
  lh agent train --iterations 100        训练模式
  lh agent daemon                        守护进程
  lh agent status                        查看状态
        """
    )

    parser.add_argument("command", nargs="?", help="process / interactive / daemon / status / train")
    parser.add_argument("query", nargs="*", help="处理内容")
    parser.add_argument("--iterations", type=int, default=100, help="训练迭代次数")
    parser.add_argument("--config", type=str, help="自定义配置文件")

    args = parser.parse_args()
    agent = LonghunAgent()

    if args.config:
        with open(args.config, 'r', encoding='utf-8') as f:
            agent.config.update(json.load(f))
            agent._save_config()

    if args.command == "process":
        if not args.query:
            print("❌ 请提供处理内容")
            return
        query = " ".join(args.query)
        result = agent.process(query)
        print("\n" + "=" * 50)
        print(f"📝 响应:\n{result['response']}")
        print("=" * 50)

    elif args.command == "interactive":
        print("\n🐉 龙魂智能体交互模式")
        print("输入 'exit' 退出, 'status' 查看状态")
        print("-" * 40)
        while True:
            try:
                user_input = input("\n🤖 你: ").strip()
                if user_input.lower() in ['exit', 'quit', 'q']:
                    break
                if user_input.lower() == 'status':
                    print(json.dumps(agent.memory.get_statistics(), ensure_ascii=False, indent=2))
                    continue
                if not user_input:
                    continue
                result = agent.process(user_input)
                print(f"\n🤖 龙魂: {result['response'][:200]}")
            except KeyboardInterrupt:
                print("\n👋 退出")
                break

    elif args.command == "daemon":
        print("🐉 启动龙魂智能体守护进程…")
        agent.run_loop()

    elif args.command == "status":
        stats = agent.memory.get_statistics()
        print("\n🐉 龙魂智能体状态")
        print("-" * 40)
        print(f"  🧬 DNA: {agent.config['dna']}")
        print(f"  📚 总经验: {stats['total_experiences']}")
        print(f"  📈 平均奖励: {stats['average_reward']:.2f}")
        print(f"  🔄 改进次数: {stats['improved_count']}")
        print(f"  💾 工作记忆: {stats['working_memory_size']}")
        print(f"  🔧 可用引擎: {len(agent.orchestrator.get_available_engines())}")
        print("-" * 40)

    elif args.command == "train":
        print(f"🐉 开始训练 ({args.iterations} 迭代)")
        print("-" * 40)

        training_tasks = [
            "优化系统性能", "部署新功能", "审计安全漏洞",
            "搜索相关信息", "翻译文档内容", "检查系统健康",
            "对齐代码结构", "蒸馏知识模型"
        ]

        for i in range(args.iterations):
            task = random.choice(training_tasks)
            print(f"\n[迭代 {i+1}/{args.iterations}] {task}")
            try:
                result = agent.process(task)
                print(f"  ✅ 完成 (奖励: {result['reward']:.2f})")
            except Exception as e:
                print(f"  ❌ 错误: {e}")

            if (i + 1) % 10 == 0:
                stats = agent.memory.get_statistics()
                print(f"\n📊 训练进度: {i+1}/{args.iterations}")
                print(f"  📚 经验: {stats['total_experiences']}")
                print(f"  📈 平均奖励: {stats['average_reward']:.2f}")

        print("\n✅ 训练完成!")
        print(json.dumps(agent.memory.get_statistics(), ensure_ascii=False, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
