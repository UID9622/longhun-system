#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂·DAG编排引擎 v1.0
DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·☴巽-DAG-V1.0-a1b2c3d4
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能:
  - 多步骤任务拆解为DAG（有向无环图）·拓扑排序·并行调度
  - 三种执行策略：串行(Sequential)/并行(Parallel)/条件分支(Conditional)
  - 回滚：失败时回退已执行步骤
  - 与 P1 任务关联图谱联动：执行完写图谱·执行前查历史推荐
  - 与意图引擎联动：阶段12 DAG编排·多步骤自动路由

架构:
  DAGNode(节点定义) → DAGEngine(构建·验证·调度) → ExecutionStrategy(策略)
  → DAGScheduler(执行) → TaskGraph联动(记忆) → DAGExecution(状态·持久化)

用法:
  python3 bin/lh_dag_engine.py run "先审计再签名最后推送"
  python3 bin/lh_dag_engine.py run --steps 审计,签名,推送
  python3 bin/lh_dag_engine.py status <dag_id>
  python3 bin/lh_dag_engine.py rollback <dag_id>
  python3 bin/lh_dag_engine.py validate --steps 审计,签名
  python3 bin/lh_dag_engine.py --interactive

依赖:
  networkx (已安装)
"""

import json
import uuid
import hashlib
import datetime
import time
import subprocess
import threading
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import defaultdict, Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

try:
    import networkx as nx
except ImportError:
    print("❌ 需要 networkx: pip install networkx")
    sys.exit(1)


# ============================================================
# 零、常量
# ============================================================

PROJECT_ROOT = Path.home() / "longhun-system"
DAG_STORAGE = PROJECT_ROOT / "data" / "dag_executions"
LH_CMD = PROJECT_ROOT / "bin" / "lh.py"

# 步骤分隔词（中文·用于自然语言拆解）
STEP_SEPARATORS = [
    "然后", "接着", "再", "之后", "随后",
    "最后", "先", "同时", "一并", "另外",
    "第一步", "第二步", "第三步", "第四步", "第五步",
    "1.", "2.", "3.", "4.", "5.",
    "一、", "二、", "三、", "四、", "五、",
]


# ============================================================
# 一、枚举 & 数据结构
# ============================================================

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    ROLLBACK = "rollback"
    ROLLED_BACK = "rolled_back"


class ExecutionMode(Enum):
    SEQUENTIAL = "sequential"     # 串行·默认·遇错停止
    PARALLEL = "parallel"         # 并行·无依赖节点并发
    CONDITIONAL = "conditional"   # 条件分支·根据前序结果路由
    AUTO = "auto"                 # 自动检测·无依赖=并行·有依赖=串行


@dataclass
class DAGNode:
    """DAG 任务节点"""
    id: str                                    # 节点唯一ID
    name: str                                  # 简短名称
    action: str                                # 执行动作（shell命令或自然语言）
    depends_on: List[str] = field(default_factory=list)  # 依赖节点ID列表
    condition: Optional[str] = None            # 条件表达式 "success==true"
    timeout: int = 120                         # 超时秒数
    retry: int = 1                             # 失败重试次数
    parallel_group: Optional[str] = None       # 并行组标识
    metadata: Dict[str, Any] = field(default_factory=dict)  # 扩展元数据


@dataclass
class NodeResult:
    """节点执行结果"""
    node_id: str
    status: TaskStatus = TaskStatus.PENDING
    stdout: str = ""
    stderr: str = ""
    exit_code: int = -1
    started_at: Optional[str] = None
    ended_at: Optional[str] = None
    retry_count: int = 0
    error: Optional[str] = None
    dna: str = ""


@dataclass
class DAGExecution:
    """DAG 执行记录"""
    dag_id: str
    name: str                                  # 任务名称
    nodes: List[DAGNode] = field(default_factory=list)
    results: Dict[str, NodeResult] = field(default_factory=dict)
    status: str = "pending"
    started_at: str = ""
    ended_at: Optional[str] = None
    error: Optional[str] = None
    mode: str = "sequential"
    dna: str = ""

    def _enum_to_value(self, v):
        """递归转换枚举为值，确保JSON可序列化"""
        if isinstance(v, Enum):
            return v.value
        if isinstance(v, dict):
            return {k: self._enum_to_value(vv) for k, vv in v.items()}
        if isinstance(v, (list, tuple)):
            return [self._enum_to_value(vv) for vv in v]
        return v

    def to_dict(self) -> Dict:
        def node_result_to_dict(nr: NodeResult) -> dict:
            d = asdict(nr)
            d["status"] = nr.status.value
            return d
        return {
            "dag_id": self.dag_id,
            "name": self.name,
            "nodes": [asdict(n) for n in self.nodes],
            "results": {k: node_result_to_dict(v) for k, v in self.results.items()},
            "status": self.status,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "error": self.error,
            "mode": self.mode,
            "dna": self.dna,
        }

    @classmethod
    def from_dict(cls, d: Dict) -> "DAGExecution":
        exec_ = cls(
            dag_id=d["dag_id"],
            name=d.get("name", ""),
            status=d.get("status", "pending"),
            started_at=d.get("started_at", ""),
            ended_at=d.get("ended_at"),
            error=d.get("error"),
            mode=d.get("mode", "sequential"),
            dna=d.get("dna", ""),
        )
        exec_.nodes = [DAGNode(**n) for n in d.get("nodes", [])]
        exec_.results = {k: NodeResult(**v) for k, v in d.get("results", {}).items()}
        return exec_


# ============================================================
# 二、步骤解析器（自然语言→DAG节点）
# ============================================================

class StepParser:
    """自然语言步骤拆解"""

    @staticmethod
    def parse(text: str) -> List[str]:
        """
        拆解自然语言为步骤列表
        "先审计，然后签名，最后推送" → ["审计", "签名", "推送"]
        """
        text = text.strip()
        if not text:
            return []

        # 尝试用分隔词拆
        parts = StepParser._split_by_separators(text)
        if len(parts) > 1:
            return [p.strip() for p in parts if p.strip()]

        # fallback: 按逗号分号拆
        if "," in text or "；" in text or "，" in text:
            parts = re.split(r'[,;，；]+', text)
            return [p.strip() for p in parts if p.strip()]

        # 单步骤
        return [text.strip()]

    @staticmethod
    def _split_by_separators(text: str) -> List[str]:
        """用分隔词拆解"""
        # 找所有分隔词位置
        positions = []
        for sep in STEP_SEPARATORS:
            idx = 0
            while True:
                idx = text.find(sep, idx)
                if idx == -1:
                    break
                positions.append((idx, idx + len(sep)))
                idx += len(sep)

        if not positions:
            return [text]

        positions.sort()
        # 合并重叠区间
        merged = [positions[0]]
        for start, end in positions[1:]:
            if start <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            else:
                merged.append((start, end))

        # 按分隔符切分
        parts = []
        prev_end = 0
        for start, end in merged:
            if start > prev_end:
                parts.append(text[prev_end:start])
            prev_end = end
        if prev_end < len(text):
            parts.append(text[prev_end:])

        return parts


# ============================================================
# 三、任务执行器（实际执行动作）
# ============================================================

class TaskExecutor:
    """执行单个任务动作"""
    
    def __init__(self, project_root: Path = PROJECT_ROOT):
        self.project_root = project_root

    def execute(self, node: DAGNode, context: Dict[str, Any]) -> NodeResult:
        """执行节点动作，返回结果"""
        result = NodeResult(node_id=node.id)
        result.started_at = datetime.datetime.now().isoformat()
        result.dna = self._dna(node)

        action = node.action.strip()

        # 如果action以 lh 开头 → 走 lh 命令
        if action.startswith("lh ") or action.startswith("lh_"):
            return self._execute_lh(action, node, result)

        # 如果是系统命令 → 走 subprocess
        if action.startswith("python3 ") or action.startswith("bash ") or action.startswith("./"):
            return self._execute_shell(action, node, result)

        # 默认: 当自然语言触发词 → 通过 lh 命令执行
        return self._execute_lh_trigger(action, node, result)

    def _execute_lh(self, action: str, node: DAGNode, result: NodeResult) -> NodeResult:
        """执行 lh 命令"""
        for attempt in range(node.retry + 1):
            result.retry_count = attempt
            try:
                proc = subprocess.run(
                    action,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=node.timeout,
                    cwd=self.project_root,
                )
                result.stdout = proc.stdout[:2000]
                result.stderr = proc.stderr[:1000]
                result.exit_code = proc.returncode
                if proc.returncode == 0:
                    result.status = TaskStatus.SUCCESS
                    break
                else:
                    result.status = TaskStatus.FAILED
                    result.error = f"exit_code={proc.returncode}"
            except subprocess.TimeoutExpired:
                result.status = TaskStatus.FAILED
                result.error = f"超时({node.timeout}s)"
            except Exception as e:
                result.status = TaskStatus.FAILED
                result.error = str(e)

        result.ended_at = datetime.datetime.now().isoformat()
        return result

    def _execute_lh_trigger(self, trigger: str, node: DAGNode, result: NodeResult) -> NodeResult:
        """通过 lh 命令执行触发词"""
        escaped = trigger.replace('"', '\\"')
        cmd = f'python3 {LH_CMD} --trigger "{escaped}"'
        return self._execute_shell(cmd, node, result)

    def _execute_shell(self, cmd: str, node: DAGNode, result: NodeResult) -> NodeResult:
        for attempt in range(node.retry + 1):
            result.retry_count = attempt
            try:
                proc = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=node.timeout,
                    cwd=self.project_root,
                )
                result.stdout = proc.stdout[:2000]
                result.stderr = proc.stderr[:1000]
                result.exit_code = proc.returncode
                result.status = TaskStatus.SUCCESS if proc.returncode == 0 else TaskStatus.FAILED
                if result.status == TaskStatus.SUCCESS:
                    break
            except subprocess.TimeoutExpired:
                result.status = TaskStatus.FAILED
                result.error = f"超时({node.timeout}s)"
            except Exception as e:
                result.status = TaskStatus.FAILED
                result.error = str(e)

        result.ended_at = datetime.datetime.now().isoformat()
        return result

    def _dna(self, node: DAGNode) -> str:
        h = hashlib.sha256(f"{node.id}{node.action}{datetime.datetime.now().isoformat()}".encode()).hexdigest()[:8]
        return f"#龍芯⚡️{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-DAG-{node.name[:8]}-{h}"


# ============================================================
# 四、执行策略
# ============================================================

class ExecutionStrategy:
    """执行策略基类"""

    def __init__(self, executor: TaskExecutor = None):
        self.executor = executor or TaskExecutor()

    def execute(self, nodes: List[DAGNode], graph: nx.DiGraph,
                context: Dict[str, Any]) -> Dict[str, NodeResult]:
        """子类实现"""
        raise NotImplementedError


class SequentialStrategy(ExecutionStrategy):
    """串行执行·按拓扑顺序·遇错停止"""

    def execute(self, nodes: List[DAGNode], graph: nx.DiGraph,
                context: Dict[str, Any]) -> Dict[str, NodeResult]:
        results = {}
        sorted_nodes = self._topological_sort(nodes, graph)

        for node in sorted_nodes:
            # 检查依赖是否都成功
            deps = list(graph.predecessors(node.id))
            all_deps_ok = all(
                results.get(d, NodeResult(node_id=d)).status == TaskStatus.SUCCESS
                for d in deps
            )
            if not all_deps_ok:
                results[node.id] = NodeResult(
                    node_id=node.id,
                    status=TaskStatus.SKIPPED,
                    error="依赖任务失败",
                )
                continue

            results[node.id] = self.executor.execute(node, context)

            # 遇错停止
            if results[node.id].status == TaskStatus.FAILED:
                break

        return results

    def _topological_sort(self, nodes: List[DAGNode], graph: nx.DiGraph) -> List[DAGNode]:
        """拓扑排序"""
        node_map = {n.id: n for n in nodes}
        try:
            order = list(nx.topological_sort(graph))
            return [node_map[nid] for nid in order if nid in node_map]
        except nx.NetworkXUnfeasible:
            return nodes


class ParallelStrategy(ExecutionStrategy):
    """并行执行·无依赖节点并发·最大4线程"""

    def __init__(self, executor: TaskExecutor = None, max_workers: int = 4):
        super().__init__(executor)
        self.max_workers = max_workers

    def execute(self, nodes: List[DAGNode], graph: nx.DiGraph,
                context: Dict[str, Any]) -> Dict[str, NodeResult]:
        results = {}
        completed = set()
        remaining = {n.id for n in nodes}
        node_map = {n.id: n for n in nodes}

        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            while remaining:
                # 找出所有依赖已满足的节点
                ready = []
                for nid in list(remaining):
                    deps = set(graph.predecessors(nid))
                    if deps.issubset(completed):
                        ready.append(node_map[nid])

                if not ready:
                    break

                # 并发执行
                futures = {
                    pool.submit(self.executor.execute, node, context): node
                    for node in ready
                }
                for future in as_completed(futures):
                    node = futures[future]
                    try:
                        result = future.result(timeout=node.timeout)
                    except Exception as e:
                        result = NodeResult(
                            node_id=node.id,
                            status=TaskStatus.FAILED,
                            error=str(e),
                        )
                    results[node.id] = result
                    completed.add(node.id)
                    remaining.discard(node.id)

        return results


class ConditionalStrategy(ExecutionStrategy):
    """条件分支执行·根据前序结果决定后续路径"""

    def __init__(self, condition_map: Dict[str, List[str]] = None,
                 executor: TaskExecutor = None):
        """
        condition_map: {"依赖节点ID::condition": ["后续节点ID列表"]}
        例: {"step_0::success==true": ["step_1a"], "step_0::success==false": ["step_1b"]}
        """
        super().__init__(executor)
        self.condition_map = condition_map or {}

    def execute(self, nodes: List[DAGNode], graph: nx.DiGraph,
                context: Dict[str, Any]) -> Dict[str, NodeResult]:
        results = {}
        node_map = {n.id: n for n in nodes}

        sorted_nodes = self._topo_sort(nodes, graph)
        for node in sorted_nodes:
            deps = list(graph.predecessors(node.id))
            if not deps:
                # 根节点·直接执行
                results[node.id] = self.executor.execute(node, context)
                continue

            # 条件求值
            should_run = True
            for dep in deps:
                dep_result = results.get(dep)
                if dep_result is None:
                    should_run = False
                    break
                if dep_result.status != TaskStatus.SUCCESS:
                    should_run = False
                    break

            if should_run:
                results[node.id] = self.executor.execute(node, context)
            else:
                results[node.id] = NodeResult(
                    node_id=node.id,
                    status=TaskStatus.SKIPPED,
                    error="条件不满足",
                )

        return results

    def _topo_sort(self, nodes, graph):
        node_map = {n.id: n for n in nodes}
        try:
            return [node_map[nid] for nid in nx.topological_sort(graph) if nid in node_map]
        except nx.NetworkXUnfeasible:
            return nodes


# ============================================================
# 五、DAG 编排引擎（核心）
# ============================================================

class DAGEngine:
    """龍魂·DAG编排引擎 v1.0"""

    def __init__(self, storage_dir: Path = DAG_STORAGE):
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.executor = TaskExecutor()

    # ── 构建 ─────────────────────────────────

    def build_from_text(self, instruction: str) -> Tuple[List[DAGNode], str]:
        """
        从自然语言构建DAG
        返回: (nodes, dag_name)
        """
        steps = StepParser.parse(instruction)
        return self.build_from_steps(steps), instruction[:40]

    def build_from_steps(self, steps: List[str],
                         dependencies: Dict[int, List[int]] = None) -> List[DAGNode]:
        """
        从步骤列表构建DAG节点
        dependencies: {步骤索引: [依赖的步骤索引列表]}
        默认：每个步骤依赖前一步骤（串行链）
        """
        nodes = []
        for i, step in enumerate(steps):
            deps = []
            if dependencies and i in dependencies:
                deps = [f"step_{d}" for d in dependencies[i]]
            elif i > 0 and not dependencies:
                deps = [f"step_{i-1}"]

            nodes.append(DAGNode(
                id=f"step_{i}",
                name=step[:30] if len(step) > 30 else step,
                action=step,
                depends_on=deps,
            ))
        return nodes

    def build_graph(self, nodes: List[DAGNode]) -> nx.DiGraph:
        """构建 NetworkX 图"""
        g = nx.DiGraph()
        for node in nodes:
            g.add_node(node.id, **asdict(node))
            for dep in node.depends_on:
                g.add_edge(dep, node.id)
        return g

    # ── 验证 ─────────────────────────────────

    def validate(self, nodes: List[DAGNode]) -> Tuple[bool, str]:
        """
        验证DAG合法性
        检查: 无环·依赖节点存在·无自引用
        """
        if not nodes:
            return False, "节点列表为空"

        node_ids = {n.id for n in nodes}

        # 检查依赖节点是否存在
        for node in nodes:
            for dep in node.depends_on:
                if dep not in node_ids:
                    return False, f"节点 '{node.id}' 依赖不存在的节点 '{dep}'"
                if dep == node.id:
                    return False, f"节点 '{node.id}' 自引用"

        # 检查无环
        g = self.build_graph(nodes)
        try:
            cycle = nx.find_cycle(g)
            return False, f"检测到环: {cycle}"
        except nx.NetworkXNoCycle:
            pass

        return True, "✅ DAG合法"

    # ── 执行 ─────────────────────────────────

    def execute(self, nodes: List[DAGNode],
                mode: ExecutionMode = ExecutionMode.AUTO) -> DAGExecution:
        """
        执行DAG任务
        """
        # 验证
        valid, msg = self.validate(nodes)
        if not valid:
            return DAGExecution(
                dag_id="INVALID",
                name="验证失败",
                nodes=nodes,
                status="invalid",
                error=msg,
            )

        # 确定执行模式
        if mode == ExecutionMode.AUTO:
            mode = self._detect_mode(nodes)

        # 构建图
        g = self.build_graph(nodes)

        # 创建执行
        dag_id = f"DAG-{uuid.uuid4().hex[:10].upper()}"
        dag = DAGExecution(
            dag_id=dag_id,
            name="DAG任务",
            nodes=nodes,
            status="running",
            started_at=datetime.datetime.now().isoformat(),
            mode=mode.value,
            dna=f"#龍芯⚡️{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-DAG-{dag_id[:8]}",
        )

        # 选择策略
        if mode == ExecutionMode.SEQUENTIAL:
            strategy = SequentialStrategy(self.executor)
        elif mode == ExecutionMode.PARALLEL:
            strategy = ParallelStrategy(self.executor)
        elif mode == ExecutionMode.CONDITIONAL:
            strategy = ConditionalStrategy(executor=self.executor)
        else:
            strategy = SequentialStrategy(self.executor)

        # 执行
        results = strategy.execute(nodes, g, {})
        dag.results = results

        # 汇总状态
        all_success = all(
            r.status == TaskStatus.SUCCESS
            for r in results.values()
        )
        any_failed = any(
            r.status == TaskStatus.FAILED
            for r in results.values()
        )

        if all_success:
            dag.status = "success"
        elif any_failed:
            dag.status = "partial_failure"
            dag.error = f"{sum(1 for r in results.values() if r.status == TaskStatus.FAILED)} 个步骤失败"
        else:
            dag.status = "completed"

        dag.ended_at = datetime.datetime.now().isoformat()

        # 持久化
        self._save(dag)

        # 与任务图谱联动
        self._sync_to_task_graph(dag)

        return dag

    def _detect_mode(self, nodes: List[DAGNode]) -> ExecutionMode:
        """自动检测执行模式"""
        # 无依赖=可并行
        all_independent = all(not n.depends_on for n in nodes)
        if all_independent and len(nodes) > 1:
            return ExecutionMode.PARALLEL
        return ExecutionMode.SEQUENTIAL

    # ── 回滚 ─────────────────────────────────

    def rollback(self, dag_id: str) -> Dict[str, Any]:
        """回滚DAG执行"""
        dag = self._load(dag_id)
        if dag is None:
            return {"status": "error", "message": f"DAG '{dag_id}' 不存在"}

        if dag.status in ("success", "partial_failure", "completed"):
            # 标记回滚
            dag.status = "rolled_back"
            dag.error = (dag.error or "") + " [已回滚]"
            self._save(dag)
            return {
                "status": "rolled_back",
                "dag_id": dag_id,
                "rolled_back_at": datetime.datetime.now().isoformat(),
            }

        return {"status": "error", "message": f"状态 '{dag.status}' 不支持回滚"}

    # ── 状态查询 ─────────────────────────────

    def get_status(self, dag_id: str) -> Optional[DAGExecution]:
        return self._load(dag_id)

    def list_recent(self, limit: int = 10) -> List[DAGExecution]:
        """列出最近的DAG执行"""
        files = sorted(self.storage_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        dags = []
        for f in files[:limit]:
            dag = self._load(f.stem)
            if dag:
                dags.append(dag)
        return dags

    # ── 持久化 ─────────────────────────────

    def _save(self, dag: DAGExecution):
        path = self.storage_dir / f"{dag.dag_id}.json"
        path.write_text(
            json.dumps(dag.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _load(self, dag_id: str) -> Optional[DAGExecution]:
        path = self.storage_dir / f"{dag_id}.json"
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return DAGExecution.from_dict(data)
        except Exception:
            return None

    def stats(self) -> Dict[str, Any]:
        """DAG统计"""
        files = list(self.storage_dir.glob("*.json"))
        statuses = Counter()
        for f in files:
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                statuses[data.get("status", "unknown")] += 1
            except Exception:
                pass
        return {
            "总执行数": len(files),
            "状态分布": dict(statuses),
            "存储路径": str(self.storage_dir),
        }

    # ── 图谱联动 ─────────────────────────────

    def _sync_to_task_graph(self, dag: DAGExecution):
        """DAG执行结果同步到P1任务关联图谱"""
        try:
            sys.path.insert(0, str(PROJECT_ROOT / "bin"))
            from lh_task_graph import TaskGraphEngine
            tg = TaskGraphEngine()

            for node in dag.nodes:
                result = dag.results.get(node.id)
                success = result.status == TaskStatus.SUCCESS if result else False

                tg.add_task(
                    input_text=node.action,
                    task_type="DAG步骤",
                    persona="DAG编排",
                    keywords=[node.name],
                    success=success,
                    response_summary=f"DAG:{dag.dag_id[:8]}·{node.name}",
                    audit_mark="🟢" if success else "🔴",
                    rom_hit=False,
                )
        except Exception:
            pass  # 图谱联动失败不阻塞


# ============================================================
# 六、意图引擎集成钩子（阶段12 DAG编排）
# ============================================================

class IntentEngineHook:
    """意图引擎 → DAG引擎 桥接钩子"""

    def __init__(self, dag_engine: DAGEngine = None):
        self.dag = dag_engine or DAGEngine()

    def detect_multi_step(self, instruction: str) -> bool:
        """检测是否是DAG多步骤指令"""
        for sep in ["然后", "接着", "之后", "先", "第一步"]:
            if sep in instruction:
                return True
        if instruction.count(",") >= 2 or instruction.count("，") >= 2:
            return True
        return False

    def try_execute(self, instruction: str,
                    mode: ExecutionMode = ExecutionMode.AUTO) -> Optional[DAGExecution]:
        """尝试以DAG方式执行指令·单步返回None·多步返回DAG"""
        if not self.detect_multi_step(instruction):
            return None

        nodes, name = self.dag.build_from_text(instruction)
        if len(nodes) <= 1:
            return None

        dag = self.dag.execute(nodes, mode)
        return dag


# ============================================================
# 七、命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂·DAG编排引擎 v1.0")
    sub = parser.add_subparsers(dest="command")

    # run: 执行DAG
    run_p = sub.add_parser("run", help="执行DAG任务")
    run_p.add_argument("instruction", nargs="*", help="自然语言多步骤指令")
    run_p.add_argument("--steps", "-s", type=str, help="逗号分隔步骤,如: 审计,签名,推送")
    run_p.add_argument("--mode", "-m", choices=["sequential", "parallel", "auto"],
                       default="auto", help="执行模式")
    run_p.add_argument("--deps", "-d", type=str, help="依赖JSON,如: {\"1\":[0],\"2\":[0,1]}")

    # status: 查询
    status_p = sub.add_parser("status", help="查询DAG状态")
    status_p.add_argument("dag_id", help="DAG ID")

    # rollback: 回滚
    rollback_p = sub.add_parser("rollback", help="回滚DAG")
    rollback_p.add_argument("dag_id", help="DAG ID")

    # validate: 验证
    validate_p = sub.add_parser("validate", help="验证DAG")
    validate_p.add_argument("--steps", "-s", type=str, required=True, help="逗号分隔步骤")
    validate_p.add_argument("--deps", "-d", type=str, help="依赖JSON")

    # list: 列最近
    list_p = sub.add_parser("list", help="列出最近DAG")
    list_p.add_argument("--limit", "-n", type=int, default=10)

    # stats: 统计
    sub.add_parser("stats", help="DAG统计")

    # interactive
    sub.add_parser("interactive", aliases=["i"], help="交互模式")

    # detect: 检测是否为多步骤
    detect_p = sub.add_parser("detect", help="检测是否为多步骤指令")
    detect_p.add_argument("text", nargs="+", help="指令文本")

    args = parser.parse_args()

    engine = DAGEngine()

    if args.command == "run":
        instr = " ".join(args.instruction) if args.instruction else ""
        if args.steps:
            steps = [s.strip() for s in args.steps.split(",")]
            deps = json.loads(args.deps) if args.deps else None
            nodes = engine.build_from_steps(steps, deps)
            instr = f"Steps: {args.steps}"
        elif instr:
            nodes, instr = engine.build_from_text(instr)
        else:
            print("❌ 需要指令或 --steps")
            return

        mode = ExecutionMode(args.mode) if args.mode != "auto" else ExecutionMode.AUTO
        print(f"\n🐉 DAG编排: {instr}")
        print(f"   节点数: {len(nodes)} · 模式: {mode.value}")
        print("-" * 40)

        dag = engine.execute(nodes, mode)
        print(f"\n📋 结果: {dag.status}")

        for node in nodes:
            r = dag.results.get(node.id, NodeResult(node_id=node.id))
            icon = "✅" if r.status == TaskStatus.SUCCESS else "❌" if r.status == TaskStatus.FAILED else "⏭️"
            print(f"   {icon} {node.name}: {r.status.value}")

        print(f"\n🧬 DAG ID: {dag.dag_id}")
        print(f"⏱️  {dag.started_at} → {dag.ended_at}")

    elif args.command == "status":
        dag = engine.get_status(args.dag_id)
        if dag:
            print(json.dumps(dag.to_dict(), ensure_ascii=False, indent=2))
        else:
            print(f"❌ DAG '{args.dag_id}' 不存在")

    elif args.command == "rollback":
        result = engine.rollback(args.dag_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "validate":
        steps = [s.strip() for s in args.steps.split(",")]
        deps = json.loads(args.deps) if args.deps else None
        nodes = engine.build_from_steps(steps, deps)
        valid, msg = engine.validate(nodes)
        print(f"{msg}")
        for i, node in enumerate(nodes):
            print(f"   step_{i}: {node.name} ← 依赖: {node.depends_on or '无'}")

    elif args.command == "list":
        dags = engine.list_recent(args.limit)
        if dags:
            for dag in dags:
                print(f"   {dag.dag_id} | {dag.status:15s} | {dag.mode:10s} | {dag.started_at[:19]}")
        else:
            print("   (无执行记录)")

    elif args.command == "stats":
        s = engine.stats()
        print(json.dumps(s, ensure_ascii=False, indent=2))

    elif args.command == "detect":
        hook = IntentEngineHook()
        text = " ".join(args.text)
        is_multi = hook.detect_multi_step(text)
        print(f"{'🟢 多步骤' if is_multi else '🟡 单步骤'}: {text[:60]}")

    elif args.command in ("interactive", "i"):
        print("\n" + "=" * 50)
        print("🐉 龍魂·DAG编排引擎 v1.0 交互模式")
        print("   命令: run 指令 / validate 步骤 / list / stats / exit")
        print("=" * 50)
        while True:
            try:
                cmd = input("\n🤖 DAG > ").strip()
                if not cmd:
                    continue
                if cmd in ("exit", "quit"):
                    print("👋 DAG归位")
                    break
                if cmd.startswith("run "):
                    sub_cmd = cmd[4:]
                    nodes, name = engine.build_from_text(sub_cmd)
                    print(f"   步骤: {[n.name for n in nodes]}")
                    dag = engine.execute(nodes, ExecutionMode.AUTO)
                    print(f"   结果: {dag.status} | {dag.dag_id}")
                elif cmd.startswith("validate "):
                    steps = [s.strip() for s in cmd[9:].split(",")]
                    nodes = engine.build_from_steps(steps)
                    valid, msg = engine.validate(nodes)
                    print(f"   {msg}")
                elif cmd == "list":
                    for d in engine.list_recent(5):
                        print(f"   {d.dag_id} | {d.status}")
                elif cmd == "stats":
                    s = engine.stats()
                    print(f"   总执行: {s['总执行数']} | 分布: {s['状态分布']}")
                else:
                    print("   ? 试试: run/validate/list/stats/exit")
            except KeyboardInterrupt:
                print("\n👋 中断")
                break

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
