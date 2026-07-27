#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH·如意 路由引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-RUYI-ROUTER-v1.0

任务路由器 - 把解析后的如意任务分派到正确的AI执行节点。

路由规则:
  - CodeBuddy(P04鲁班) → 工程执行·代码生成·架构搭建·代码迁移
  - Kimi(画师)         → UI/UX设计·视觉优化·图表生成·文档排版
  - 华云道(织女)       → 最终渲染·展示·编织成品

三层联动:
  L1 记忆API → 读取历史上下文
  L2 任务路由 → 分解分派
  L3 审计签章 → 三色审计+DNA追溯

🐉 心意所指·万物皆成
"""

import json
import os
import sys
import hashlib
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum

# 添加解析器路径
_ENGINES_DIR = os.path.dirname(os.path.abspath(__file__))
if _ENGINES_DIR not in sys.path:
    sys.path.insert(0, _ENGINES_DIR)

try:
    from lh_ruyi_parser import RuyiTask, RuyiTaskAction, parse_ruyi_command
except ImportError:
    # Fallback for standalone use
    RuyiTask = None


# ─── 枚举 ──────────────────────────────────────────────

class TaskStatus(Enum):
    PENDING = "pending"
    ROUTING = "routing"
    IN_PROGRESS = "in_progress"
    CODEBUDDY_DONE = "codebuddy_done"
    KIMI_DONE = "kimi_done"
    MIGRATION_DONE = "migration_done"
    RENDERED = "rendered"           # 华云道渲染完成
    AUDIT_PASSED = "audit_passed"   # 审计通过
    COMPLETED = "completed"
    FAILED = "failed"

class AuditMark(Enum):
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"


# ─── 数据类型 ───────────────────────────────────────────

@dataclass
class RouteResult:
    """单次路由结果"""
    target_ai: str
    action: str
    success: bool
    output: str = ""
    error: str = ""
    artifacts: List[str] = field(default_factory=list)  # 产出的文件/路径
    duration_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class MemoryContext:
    """从记忆API加载的上下文"""
    identity: Dict[str, Any] = field(default_factory=dict)
    anchors: Dict[str, Any] = field(default_factory=dict)
    recent_tasks: List[str] = field(default_factory=list)
    project_state: Dict[str, Any] = field(default_factory=dict)
    loaded: bool = False

@dataclass
class RuyiExecutionReport:
    """如意任务执行报告"""
    task: Dict[str, Any] = field(default_factory=dict)
    dna: str = ""
    status: str = "pending"
    memory_loaded: bool = False
    route_results: List[Dict[str, Any]] = field(default_factory=list)
    migration_report: Optional[Dict[str, Any]] = None
    audit_mark: str = "🟡"
    audit_notes: List[str] = field(default_factory=list)
    started_at: str = ""
    completed_at: str = ""
    duration_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ─── 路由引擎 ──────────────────────────────────────────

class RuyiRouter:
    """
    CNSH·如意 任务路由引擎。

    工作流:
    1. load_memory()     → 加载记忆API上下文
    2. route(task)       → 解析任务·分派到各AI
    3. execute()         → 逐项执行(CodeBuddy本地·Kimi生成提示词·华云道准备转移)
    4. audit()           → 三色审计
    5. generate_report() → 输出执行报告
    """

    # 任务类型 → AI映射
    TASK_ROUTING_MAP = {
        # 工程类 → CodeBuddy
        "generate":  "CodeBuddy",
        "build":     "CodeBuddy",
        "fix":       "CodeBuddy",
        "check":     "CodeBuddy",
        "transfer":  "CodeBuddy",
        # 设计类 → Kimi
        "optimize":  "Kimi",
        "beautify":  "Kimi",
        # 渲染类 → 华云道
        "render":    "华云道",
        "present":   "华云道",
    }

    def __init__(self, memory_api_url: str = "http://127.0.0.1:8771/v1/memory",
                 memory_api_token: Optional[str] = None,
                 work_dir: Optional[Path] = None):
        self.memory_api_url = memory_api_url.rstrip("/")
        self.memory_api_token = memory_api_token
        self.work_dir = work_dir or Path.cwd()
        self.memory: Optional[MemoryContext] = None
        self._pending_tasks: List[RuyiTask] = []
        self._execution_history: List[RuyiExecutionReport] = []

    # ─── 记忆加载 ─────────────────────────────────────

    def load_memory(self) -> MemoryContext:
        """从记忆API加载上下文 - 焊死第一步"""
        ctx = MemoryContext()

        # 尝试从本地MEMORY.md加载（更可靠）
        memory_file = self.work_dir / ".codebuddy" / "memory" / "MEMORY.md"
        try:
            if memory_file.exists():
                content = memory_file.read_text(encoding="utf-8")
                ctx.loaded = True
                ctx.project_state["memory_file"] = str(memory_file)
                ctx.project_state["memory_size"] = len(content)
                # 提取锚点
                for line in content.split("\n"):
                    if "UID9622" in line:
                        ctx.identity["uid"] = "UID9622"
                    if "GPG:" in line:
                        ctx.identity["gpg"] = line.split(":")[-1].strip()
        except Exception:
            pass

        # 尝试HTTP加载（带认证）
        try:
            import urllib.request
            headers = {}
            if self.memory_api_token:
                headers["Authorization"] = f"Bearer {self.memory_api_token}"

            # health
            req = urllib.request.Request(f"{self.memory_api_url}/health", headers=headers)
            resp = urllib.request.urlopen(req, timeout=5)
            if resp.status == 200:
                ctx.project_state["memory_api"] = "healthy"
                ctx.loaded = True

            # identity
            req = urllib.request.Request(f"{self.memory_api_url}/identity", headers=headers)
            resp = urllib.request.urlopen(req, timeout=5)
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                ctx.identity = data.get("identity", data)
                ctx.loaded = True

            # full memory
            req = urllib.request.Request(f"{self.memory_api_url}/memory", headers=headers)
            resp = urllib.request.urlopen(req, timeout=5)
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                ctx.anchors = data.get("anchors", {})
                ctx.recent_tasks = data.get("recent_tasks", [])
                ctx.project_state["memory_sections"] = data.get("sections", 0)
                ctx.loaded = True
        except Exception as e:
            ctx.project_state["memory_api"] = f"unreachable: {str(e)[:80]}"

        # 读取STATE.md
        state_file = self.work_dir / "STATE.md"
        try:
            if state_file.exists():
                content = state_file.read_text(encoding="utf-8")
                ctx.project_state["state_loaded"] = True
        except Exception:
            ctx.project_state["state_loaded"] = False

        self.memory = ctx
        return ctx

    # ─── 任务路由 ─────────────────────────────────────

    def route(self, task: RuyiTask) -> RuyiExecutionReport:
        """
        路由并执行一个如意任务。

        Args:
            task: 解析后的如意任务

        Returns:
            RuyiExecutionReport: 执行报告
        """
        start_time = time.time()
        report = RuyiExecutionReport(
            task=task.to_dict(),
            started_at=datetime.now().isoformat(),
            memory_loaded=bool(self.memory and self.memory.loaded),
        )

        # 生成DNA
        task.dna = self._generate_dna(task.task_name)
        report.dna = task.dna

        print(f"\n{'='*60}")
        print(f"🐉 CNSH·如意 执行中")
        print(f"   任务: {task.task_name}")
        print(f"   DNA:  {task.dna}")
        print(f"   记忆: {'✅ 已加载' if report.memory_loaded else '⚠️ 离线'}")
        print(f"{'='*60}\n")

        # 路由每个动作
        for i, action in enumerate(task.actions):
            print(f"  [{i+1}/{len(task.actions)}] 分派 → {action.target_ai} · {action.action} · {action.target}")

            result = self._execute_action(action, task)
            report.route_results.append(result.to_dict())

            status_icon = "✅" if result.success else "❌"
            print(f"       {status_icon} {result.output[:80]}...")
            if result.error:
                print(f"       ⚠️ {result.error}")

            if not result.success:
                report.audit_notes.append(f"动作[{i}]失败: {result.error}")

        # 处理转移（如果有）
        if task.transfer_target:
            print(f"\n  📦 转移至 → {task.transfer_target}")
            # 此处预留代码迁移引擎集成
            report.migration_report = {
                "source": "如意任务",
                "target_platform": task.transfer_target,
                "status": "pending_transfer",
            }

        # 审计
        report.audit_mark, audit_notes = self._audit(report)
        report.audit_notes.extend(audit_notes)

        report.status = TaskStatus.COMPLETED.value if all(
            r.get("success", False) for r in report.route_results
        ) else TaskStatus.FAILED.value

        report.completed_at = datetime.now().isoformat()
        report.duration_ms = (time.time() - start_time) * 1000

        print(f"\n{'='*60}")
        print(f"  审计: {report.audit_mark}")
        print(f"  状态: {report.status}")
        print(f"  耗时: {report.duration_ms:.0f}ms")
        print(f"{'='*60}\n")

        self._execution_history.append(report)
        return report

    # ─── 动作执行 ────────────────────────────────────

    def _execute_action(self, action: RuyiTaskAction, task: RuyiTask) -> RouteResult:
        """执行单个动作"""
        start = time.time()
        target_ai = action.target_ai

        try:
            if target_ai == "CodeBuddy":
                output = self._execute_codebuddy(action, task)
            elif target_ai == "Kimi":
                output = self._generate_kimi_prompt(action, task)
            elif target_ai == "华云道":
                output = self._prepare_huayundao_transfer(action, task)
            else:
                output = f"未知AI目标: {target_ai}，已路由到CodeBuddy默认处理"
                output += "\n" + self._execute_codebuddy(action, task)

            return RouteResult(
                target_ai=target_ai,
                action=action.action,
                success=True,
                output=output,
                artifacts=[],
                duration_ms=(time.time() - start) * 1000,
            )
        except Exception as e:
            return RouteResult(
                target_ai=target_ai,
                action=action.action,
                success=False,
                output="",
                error=str(e),
                duration_ms=(time.time() - start) * 1000,
            )

    def _execute_codebuddy(self, action: RuyiTaskAction, task: RuyiTask) -> str:
        """CodeBuddy(P04鲁班) 执行工程任务"""
        action_type = action.action
        target = action.target
        style = task.style
        tech_stack = task.tech_stack

        prompts = []

        if action_type == "generate":
            prompts.append(f"## 工程生成任务\n")
            prompts.append(f"请为任务「{task.task_name}」生成代码。")
            prompts.append(f"目标: {target}")
            if tech_stack:
                prompts.append(f"技术栈: {', '.join(tech_stack)}")
            if style:
                prompts.append(f"风格: {style}")
            prompts.append(f"\n注意: 遵循龍魂体系规则 - 文件路径落入对应目录、代码含DNA注释头、德本审计五问自检。")

        elif action_type == "fix":
            prompts.append(f"## 修复任务\n")
            prompts.append(f"请修复: {target}")
            prompts.append(f"上下文: 任务「{task.task_name}」")
            if tech_stack:
                prompts.append(f"相关技术栈: {', '.join(tech_stack)}")

        elif action_type == "check":
            prompts.append(f"## 检测任务\n")
            prompts.append(f"请检测: {target}")
            prompts.append(f"产出检测报告，标注🟢🟡🔴三色标记。")

        elif action_type == "transfer":
            prompts.append(f"## 代码转移任务\n")
            prompts.append(f"请将代码转移至目标: {target}")
            prompts.append(f"要求: 运行变量检测引擎、生成变量映射表、输出转移报告。")
            if tech_stack:
                prompts.append(f"源→目标: {', '.join(tech_stack)}")

        elif action_type == "build":
            prompts.append(f"## 架构搭建任务\n")
            prompts.append(f"请搭建: {target}")
            if tech_stack:
                prompts.append(f"技术栈: {', '.join(tech_stack)}")

        else:
            prompts.append(f"## CodeBuddy任务\n")
            prompts.append(f"请执行: {action_type} → {target}")

        return "\n".join(prompts)

    def _generate_kimi_prompt(self, action: RuyiTaskAction, task: RuyiTask) -> str:
        """为Kimi(画师)生成设计提示词"""
        prompts = []
        prompts.append(f"## Kimi 设计任务\n")
        prompts.append(f"任务背景: {task.task_name}")
        prompts.append(f"设计需求: {action.target}")
        if task.style:
            prompts.append(f"风格要求: {task.style}")
        if task.tech_stack:
            prompts.append(f"适配技术栈: {', '.join(task.tech_stack)}")

        prompts.append(f"\n--- 设计指引 ---")
        prompts.append(f"请根据以上需求，设计UI/UX方案或生成视觉素材。")
        prompts.append(f"输出格式: Markdown设计规格 + SVG/PNG素材链接(如有)")

        return "\n".join(prompts)

    def _prepare_huayundao_transfer(self, action: RuyiTaskAction, task: RuyiTask) -> str:
        """准备华云道转移"""
        prompts = []
        prompts.append(f"## 华云道 渲染准备\n")
        prompts.append(f"任务: {task.task_name}")
        prompts.append(f"渲染需求: {action.target}")
        prompts.append(f"\n转移清单:")
        prompts.append(f"  - 代码文件已由CodeBuddy生成")
        prompts.append(f"  - 视觉素材已由Kimi设计")
        prompts.append(f"  - 待华云道编织为最终成品")
        return "\n".join(prompts)

    # ─── 审计 ────────────────────────────────────────

    def _audit(self, report: RuyiExecutionReport) -> Tuple[str, List[str]]:
        """三色审计"""
        notes = []

        # 检查1: 任务名是否为空
        task = report.task
        if not task.get("task_name"):
            return AuditMark.RED.value, ["🔴 任务名为空"]

        # 检查2: 动作是否全部成功
        all_success = all(r.get("success", False) for r in report.route_results)
        if not all_success:
            failed = [r for r in report.route_results if not r.get("success")]
            notes.append(f"🟡 {len(failed)}个动作执行失败")
            return AuditMark.YELLOW.value, notes

        # 检查3: 是否有转移但未执行
        if task.get("transfer_target") and not report.migration_report:
            notes.append("🟡 有转移目标但未生成迁移报告")

        # 检查4: 记忆是否加载
        if not report.memory_loaded:
            notes.append("🟡 记忆API离线，上下文可能不完整")

        # 确定最终标记
        if not notes:
            return AuditMark.GREEN.value, ["🟢 全检查点通过"]
        elif any("🔴" in n for n in notes):
            return AuditMark.RED.value, notes
        else:
            return AuditMark.YELLOW.value, notes

    # ─── 辅助 ────────────────────────────────────────

    def _generate_dna(self, task_name: str) -> str:
        """生成任务DNA追溯码"""
        now = datetime.now()
        stem = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
        branch = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
        gz_days = ["甲子","乙丑","丙寅","丁卯","戊辰","己巳","庚午","辛未",
                    "壬申","癸酉","甲戌","乙亥","丙子","丁丑","戊寅","己卯",
                    "庚辰","辛巳","壬午","癸未","甲申","乙酉","丙戌","丁亥",
                    "戊子","己丑","庚寅","辛卯","壬辰","癸巳","甲午","乙未",
                    "丙申","丁酉","戊戌","己亥","庚子","辛丑","壬寅","癸卯",
                    "甲辰","乙巳","丙午","丁未","戊申","己酉","庚戌","辛亥",
                    "壬子","癸丑","甲寅","乙卯","丙辰","丁巳","戊午","己未",
                    "庚申","辛酉","壬戌","癸亥"]
        day_idx = now.day % 60
        date_str = f"{now.year}-{now.month:02d}-{now.day:02d}"
        hash_id = hashlib.sha256(f"{task_name}{now.timestamp()}".encode()).hexdigest()[:8]
        return f"#龍芯⚡️{date_str}-RUYI-{hash_id}"


# ─── 便捷函数 ──────────────────────────────────────────

def execute_ruyi_command(raw_command: str, work_dir: Optional[Path] = None) -> RuyiExecutionReport:
    """
    一键执行CNSH·如意指令。

    Args:
        raw_command: CNSH·如意指令文本
        work_dir: 工作目录

    Returns:
        RuyiExecutionReport: 完整执行报告
    """
    # 1. 加载记忆
    router = RuyiRouter(work_dir=work_dir)
    ctx = router.load_memory()

    # 2. 解析指令
    task = parse_ruyi_command(raw_command)

    # 3. 路由执行
    report = router.route(task)

    return report


# ─── 自测 ──────────────────────────────────────────────

if __name__ == "__main__":
    print("🧪 CNSH·如意 路由引擎 自测")
    print("=" * 60)

    # 加载记忆
    router = RuyiRouter()
    ctx = router.load_memory()
    print(f"记忆加载: {'✅' if ctx.loaded else '⚠️ 离线模式'}")

    # 测试命令
    test_cmd = '''定义 任务 "生成用户登录页"
设 风格 为 "简约商务风"
设 技术栈 为 ["React", "TypeScript"]
则 CodeBuddy 生成 前端页面
则 Kimi 优化 视觉风格
最后 转移 代码 至 华云道 渲染'''

    task = parse_ruyi_command(test_cmd)
    report = router.route(task)

    print("\n📋 执行报告摘要:")
    print(f"  DNA: {report.dna}")
    print(f"  审计: {report.audit_mark}")
    print(f"  状态: {report.status}")
    print(f"  耗时: {report.duration_ms:.0f}ms")
    print(f"  记忆: {'已加载' if report.memory_loaded else '离线'}")

    for i, r in enumerate(report.route_results):
        status = "✅" if r["success"] else "❌"
        print(f"  路由{i+1}: {status} {r['target_ai']} → {r['action']} ({r['duration_ms']:.0f}ms)")

    print("\n✅ 路由引擎自测完成")
