#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2
"""
🐲 龍魂·总编排器 GrandOrchestrator v2.0
DNA: #龍芯⚡️2026-08-04-GRAND-ORCHESTRATOR-UID9622

三合一总控：
  Layer 1 — 人格矩阵 (Persona Matrix): 24人格Agent·意图路由·链式/并行调度
  Layer 2 — 蚁群架构 (Ant Colony): 信息素协同·涌现评估·不动点桥接
  Layer 3 — 黑板主编 (Blackboard+Editor): 共享知识库·专家协作·报告整合

架构：
  用户输入 → P00意图解析 → 人格路由表 → 多Agent并行/链式执行
  → 蚁群信息素协同过滤 → 主编整合 → 黑板落盘 → 最终报告

用法:
  go = GrandOrchestrator()
  result = go.run("分析龙魂系统架构", mode="full")   # 全量模式
  result = go.run("审计一下代码", mode="audit")        # 审计模式
  result = go.run("快速检查", mode="quick")             # 快速模式
  go.demo()  # 演示
"""

import os
import sys
import json
import threading
import time
from pathlib import Path
from datetime import datetime
from enum import Enum, auto
from typing import Dict, Any, Optional, List

# 路径处理
_SYSTEM_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(_SYSTEM_ROOT))
sys.path.insert(0, str(_SYSTEM_ROOT / "05_ENGINES"))

from .blackboard_adapter import BlackboardAdapter
from .agent_bus_adapter import AgentBusAdapter
from .chunker import DocumentChunker, ChunkMethod
from ..agents.persona_agents import (
    AGENT_REGISTRY, AGENT_META, create_agent, create_all_agents,
)
from ..agents.integrator_agent import IntegratorAgent


class OrchestrationMode(Enum):
    FULL = auto()       # 全量——所有层同时运作
    AUDIT = auto()      # 审计——守护层+文化层底线
    QUICK = auto()      # 快速——仅意图解析+路由
    DEPLOY = auto()     # 部署——执行层部署+安全扫描
    TEACHING = auto()   # 教学——文化层教育链路


# ── 意图→人格路由表 ──

ROUTE_TABLE = {
    # 关键词 → (主要人格, 辅助人格链, 模式)
    "审计": ("P05", ["P06", "P12"], OrchestrationMode.AUDIT),
    "检查": ("P05", ["P06"], OrchestrationMode.AUDIT),
    "安全": ("P77", ["P05", "P72"], OrchestrationMode.AUDIT),
    "漏洞": ("P77", ["P05", "P72"], OrchestrationMode.AUDIT),
    "修复": ("P04", ["P05"], OrchestrationMode.FULL),
    "代码": ("P04", ["P05", "P06"], OrchestrationMode.FULL),
    "架构": ("P04", ["P01", "P05"], OrchestrationMode.FULL),
    "开发": ("P04", ["P05", "P15"], OrchestrationMode.FULL),
    "部署": ("P14", ["P77", "P05"], OrchestrationMode.DEPLOY),
    "上线": ("P14", ["P77", "P05"], OrchestrationMode.DEPLOY),
    "算一下": ("P06", ["P01"], OrchestrationMode.QUICK),
    "数字": ("P06", ["P01"], OrchestrationMode.QUICK),
    "评估": ("P01", ["P06", "P07"], OrchestrationMode.FULL),
    "推演": ("P01", ["P06", "P12"], OrchestrationMode.FULL),
    "命名": ("P08", ["P03"], OrchestrationMode.QUICK),
    "教我": ("P02", ["P08", "P11"], OrchestrationMode.TEACHING),
    "教学": ("P02", ["P08", "P11"], OrchestrationMode.TEACHING),
    "温度": ("P02", [], OrchestrationMode.QUICK),
    "诊断": ("P09", ["P05"], OrchestrationMode.AUDIT),
    "健康": ("P09", ["P05"], OrchestrationMode.AUDIT),
    "冲突": ("P10", ["P12"], OrchestrationMode.QUICK),
    "创意": ("P11", ["P04"], OrchestrationMode.FULL),
    "底线": ("P12", ["P72"], OrchestrationMode.AUDIT),
    "授权": ("P13", ["P15"], OrchestrationMode.QUICK),
    "归档": ("P03", ["P15"], OrchestrationMode.QUICK),
    "签章": ("P15", ["P03"], OrchestrationMode.QUICK),
    "经济": ("P07", ["P01", "P06"], OrchestrationMode.FULL),
    "成本": ("P07", ["P01"], OrchestrationMode.FULL),
    "预算": ("P07", ["P01"], OrchestrationMode.FULL),
    "维权": ("S3", ["P12", "S1"], OrchestrationMode.QUICK),
    "法律": ("S1", ["P12"], OrchestrationMode.AUDIT),
    "合规": ("S1", ["P05"], OrchestrationMode.AUDIT),
    "熔断": ("P72", ["P05"], OrchestrationMode.AUDIT),
}


class GrandOrchestrator:
    """
    龍魂·总编排器

    三层架构统一调度：
      人格矩阵(Agent层) → 22+人格智能体·意图路由·执行
      蚁群架构(Colony层) → 信息素协同·涌现评估·桥接
      黑板主编(Knowledge层) → 共享黑板·专家协作·报告整合
    """

    def __init__(self, config: dict = None, llm_client=None,
                 enable_ant_colony: bool = True,
                 enable_blackboard: bool = True):
        self.config = config or {}
        self._llm = llm_client
        self._enable_ant_colony = enable_ant_colony
        self._enable_blackboard = enable_blackboard

        # 初始化三层
        self.blackboard = BlackboardAdapter(use_global=True) if enable_blackboard else None
        self.bus = AgentBusAdapter(use_global=True)

        # 蚁群桥接（按需加载）
        self._ant_colony_runtime = None
        self._ant_colony_bridge = None
        if enable_ant_colony:
            self._init_ant_colony()

        # 所有Agent
        self._agents: Dict[str, Any] = {}
        self._integrator: Optional[IntegratorAgent] = None

        # 状态
        self._booted = False
        self._lock = threading.RLock()
        self._execution_log: List[Dict] = []

    def _init_ant_colony(self):
        """延迟加载蚁群引擎"""
        try:
            from engines.ant_colony.runtime import get_runtime
            self._ant_colony_runtime = get_runtime()
            from engines.ant_colony.engine_bridge import get_bridge
            self._ant_colony_bridge = get_bridge()
        except ImportError:
            pass

    # ── 启动 ──

    def boot(self, layers: List[str] = None) -> Dict[str, bool]:
        """启动所有Agent"""
        with self._lock:
            if self._booted:
                return {pid: True for pid in self._agents}

            agents = create_all_agents(
                llm=self._llm,
                blackboard=self.blackboard,
                bus=self.bus,
                layers=layers,
            )
            self._agents.update(agents)

            # 主编Agent
            self._integrator = IntegratorAgent(
                llm_client=self._llm,
                blackboard=self.blackboard,
                bus=self.bus,
            )

            self._booted = True
            return {pid: True for pid in agents}

    def boot_agent(self, pid: str) -> bool:
        """启动单个人格"""
        agent = create_agent(pid, llm=self._llm, blackboard=self.blackboard, bus=self.bus)
        if agent:
            self._agents[pid] = agent
            return True
        return False

    # ── 意图解析 ──

    def parse_intent(self, text: str) -> Dict[str, Any]:
        """解析用户意图 → 路由到对应人格"""
        # 关键词匹配
        for keyword, (primary, chain, mode) in ROUTE_TABLE.items():
            if keyword in text:
                return {
                    "intent": keyword,
                    "primary": primary,
                    "chain": [primary] + chain,
                    "mode": mode,
                }

        # 默认路由
        return {
            "intent": "general",
            "primary": "P00",
            "chain": ["P00", "P01"],
            "mode": OrchestrationMode.FULL,
        }

    # ── 执行 ──

    def run(self, task: str, mode: str = "auto",
            agents: List[str] = None) -> Dict[str, Any]:
        """
        执行多智能体协作

        Args:
            task: 任务描述
            mode: auto/full/audit/quick/deploy/teaching
            agents: 指定Agent列表（覆盖自动路由）
        Returns:
            完整执行结果
        """
        start_time = time.time()
        print(f"\n{'='*60}")
        print(f"🐲 龍魂·多智能体协作启动")
        print(f"{'='*60}")

        # 1. 意图解析（如果未指定Agent）
        intent = self.parse_intent(task) if not agents else None
        if agents:
            target_chain = agents
        else:
            target_chain = intent["chain"]
            mode = mode if mode != "auto" else intent["mode"].name.lower()

        print(f"📌 意图: {intent['intent'] if intent else 'manual'} → 路由: {' → '.join(target_chain)}")

        # 2. 确保Agent已启动
        for pid in target_chain:
            if pid not in self._agents and pid in AGENT_REGISTRY:
                self.boot_agent(pid)

        # 3. 按模式执行
        if mode == "quick":
            result = self._run_quick(task, target_chain)
        elif mode == "audit":
            result = self._run_audit(task, target_chain)
        elif mode == "deploy":
            result = self._run_deploy(task, target_chain)
        elif mode == "teaching":
            result = self._run_teaching(task, target_chain)
        else:
            result = self._run_full(task, target_chain)

        # 4. 蚁群协同（可选）
        if self._enable_ant_colony and self._ant_colony_bridge:
            self._ant_colony_inject(result)

        # 5. 主编整合
        report = self._integrate(task, result)

        # 6. 执行日志
        elapsed = time.time() - start_time
        log_entry = {
            "task": task[:200],
            "mode": mode,
            "agents": target_chain,
            "elapsed_sec": round(elapsed, 2),
            "ts": datetime.now().isoformat(),
            "dna": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-ORCHESTRATOR-RUN-UID9622",
        }
        self._execution_log.append(log_entry)

        result["orchestrator"] = {
            "elapsed_sec": elapsed,
            "agents_used": len(target_chain),
            "integration_done": True,
            "report_available": report is not None,
        }

        print(f"\n{'='*60}")
        print(f"✅ 协作完成 ({elapsed:.1f}s) | Agents: {len(target_chain)} | 模式: {mode}")
        print(f"{'='*60}\n")

        return result

    def _run_full(self, task: str, chain: List[str]) -> Dict[str, Any]:
        """全量模式：链式执行 + 并行补审"""
        results = {}
        context = {"task": task}

        # 链式执行
        for pid in chain:
            agent = self._agents.get(pid)
            if agent is None:
                continue
            try:
                r = agent.process(task, **context)
                results[pid] = r
                context[f"output_{pid}"] = r
                context["previous_output"] = r
            except Exception as e:
                results[pid] = {"status": "error", "error": str(e)}

        # 守护层并行补审（如果审计/安全未在链中）
        if "P05" not in chain:
            self._run_parallel_audit(task, results, context)
        if "P72" not in chain:
            self._run_parallel_safety(task, results, context)

        return {"chain": chain, "agent_results": results, "mode": "full"}

    def _run_audit(self, task: str, chain: List[str]) -> Dict[str, Any]:
        """审计模式：全量守护层审查"""
        results = {}
        audit_chain = ["P05", "P06", "P12", "P15"]
        for pid in audit_chain:
            if pid in chain and pid not in results:
                agent = self._agents.get(pid)
                if agent:
                    try:
                        results[pid] = agent.process(task)
                    except Exception as e:
                        results[pid] = {"status": "error", "error": str(e)}

        # 补充原始链中其他Agent
        for pid in chain:
            if pid not in results and pid not in audit_chain:
                agent = self._agents.get(pid)
                if agent:
                    try:
                        results[pid] = agent.process(task)
                    except Exception as e:
                        results[pid] = {"status": "error", "error": str(e)}

        # P72熔断检查
        p72 = self._agents.get("P72")
        if p72 and "P72" not in results:
            try:
                results["P72"] = p72.process(task)
            except Exception as e:
                results["P72"] = {"status": "error", "error": str(e)}

        return {"chain": audit_chain, "agent_results": results, "mode": "audit"}

    def _run_deploy(self, task: str, chain: List[str]) -> Dict[str, Any]:
        """部署模式：P14 + P77安全扫描 + P05审计"""
        results = {}
        deploy_order = ["P14", "P77", "P05", "P72", "P15"]
        for pid in deploy_order:
            agent = self._agents.get(pid)
            if agent:
                try:
                    results[pid] = agent.process(task)
                except Exception as e:
                    results[pid] = {"status": "error", "error": str(e)}
        return {"chain": deploy_order, "agent_results": results, "mode": "deploy"}

    def _run_teaching(self, task: str, chain: List[str]) -> Dict[str, Any]:
        """教学模式：P02情感温度 + P08术语桥接 + P11创意教学"""
        results = {}
        teach_order = ["P02", "P08", "P11"]
        for pid in teach_order:
            agent = self._agents.get(pid)
            if agent:
                try:
                    results[pid] = agent.process(task)
                except Exception as e:
                    results[pid] = {"status": "error", "error": str(e)}
        return {"chain": teach_order, "agent_results": results, "mode": "teaching"}

    def _run_quick(self, task: str, chain: List[str]) -> Dict[str, Any]:
        """快速模式：仅意图解析+主路由"""
        results = {}
        for pid in chain[:3]:  # 最多3个
            agent = self._agents.get(pid)
            if agent:
                try:
                    results[pid] = agent.process(task)
                except Exception as e:
                    results[pid] = {"status": "error", "error": str(e)}
        return {"chain": chain[:3], "agent_results": results, "mode": "quick"}

    def _run_parallel_audit(self, task: str, results: dict, context: dict):
        """后台并行审计"""
        for pid in ["P05", "P15"]:
            agent = self._agents.get(pid)
            if agent and pid not in results:
                try:
                    results[pid] = agent.process(task)
                except Exception:
                    pass

    def _run_parallel_safety(self, task: str, results: dict, context: dict):
        """后台并行安全检查"""
        p72 = self._agents.get("P72")
        if p72 and "P72" not in results:
            try:
                results["P72"] = p72.process(task)
            except Exception:
                pass

    # ── 蚁群协同注入 ──

    def _ant_colony_inject(self, result: Dict):
        """将执行结果注入蚁群引擎"""
        if not self._ant_colony_bridge:
            return
        try:
            # 简化桥接
            agent_results = result.get("agent_results", {})
            for pid, output in agent_results.items():
                if self._ant_colony_runtime:
                    self._ant_colony_runtime.touch(pid, str(output)[:200])
        except Exception:
            pass

    # ── 主编整合 ──

    def _integrate(self, task: str, result: Dict) -> Optional[str]:
        """主编整合所有Agent输出"""
        if not self._integrator:
            return None
        try:
            agent_results = result.get("agent_results", {})
            integration = self._integrator.act(task, agent_results=agent_results)
            return self._integrator.finalize()
        except Exception:
            return None

    # ── 查询 ──

    def status_all(self) -> Dict[str, Any]:
        """所有Agent状态"""
        return {
            "booted": self._booted,
            "agents": {
                pid: {
                    "name": agent.PERSONA_NAME,
                    "layer": agent.LAYER,
                    "state": agent.state.name,
                    "tasks": agent.task_count,
                    "stats": agent.stats,
                }
                for pid, agent in self._agents.items()
            },
            "ant_colony": self._ant_colony_runtime is not None,
            "blackboard": self.blackboard is not None,
            "execution_count": len(self._execution_log),
        }

    def status_by_layer(self) -> Dict[str, List[str]]:
        layers = {}
        for pid, agent in self._agents.items():
            layers.setdefault(agent.LAYER, []).append(f"{pid}({agent.PERSONA_NAME})")
        return dict(sorted(layers.items()))

    # ── 黑板操作 ──

    def get_final_report(self) -> Optional[str]:
        if self.blackboard:
            return self.blackboard.read_md("final_report")
        return None

    def get_blackboard_context(self) -> Dict:
        if self.blackboard:
            return self.blackboard.get_context()
        return {}

    # ── 演示 ──

    def demo(self):
        """运行完整演示"""
        print("""
╔══════════════════════════════════════════════════════╗
║  🐲 龍魂·多智能体统一协作框架 v2.0                       ║
║  DNA: #龍芯⚡️2026-08-04-GRAND-ORCHESTRATOR-DEMO-UID9622 ║
║  🟢 24人格完整落地·蚁群协同·黑板主编                       ║
╚══════════════════════════════════════════════════════╝
""")
        demo_task = "请分析龙魂系统的架构安全性并进行审计"

        print("【演示1】意图解析...")
        intent = self.parse_intent(demo_task)
        print(f"  意图: {intent['intent']} → {intent['chain']}")

        print("\n【演示2】启动24人格Agent...")
        result = self.boot()
        print(f"  成功启动: {sum(1 for v in result.values() if v)}/{len(result)}")

        print("\n【演示3】全量执行...")
        result = self.run(demo_task, mode="full")
        agent_count = len(result.get("agent_results", {}))
        print(f"  参与Agent: {agent_count}")

        print("\n【演示4】按层分组状态...")
        for layer, agents in self.status_by_layer().items():
            print(f"  [{layer}] {', '.join(agents)}")

        print("\n【演示5】主编整合报告...")
        report = self.get_final_report()
        if report:
            print(f"  ✅ 报告已生成 ({len(report)}字符)")
        else:
            print(f"  ⚠️ 报告生成中...")

        print("\n✅ 演示完成\n")

    def shutdown(self):
        """关闭所有Agent"""
        for agent in list(self._agents.values()):
            try:
                agent.shutdown()
            except Exception:
                pass
        self._agents.clear()
        if self._ant_colony_runtime:
            try:
                from engines.ant_colony.runtime import stop_runtime
                stop_runtime()
            except Exception:
                pass
        self._booted = False


# ═══════════════════════════════════════════════════════════════
# 全局单例
# ═══════════════════════════════════════════════════════════════

_orchestrator_instance: Optional[GrandOrchestrator] = None
_orch_lock = threading.Lock()


def get_orchestrator(**kwargs) -> GrandOrchestrator:
    global _orchestrator_instance
    with _orch_lock:
        if _orchestrator_instance is None:
            _orchestrator_instance = GrandOrchestrator(**kwargs)
        return _orchestrator_instance
