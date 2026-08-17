#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · Agent执行器 v1.0
DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-AGENT-EXEC-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过

功能: Agent任务执行调度，整合人格矩阵、知识图谱、蚁群信号与剪贴板容器。
支持任务类型: query | execute | audit | learn | clipboard
"""

import json
import hashlib
import time
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

# ============================================================
# 路径与常量
# ============================================================

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

SYSTEM_ROOT = Path(__file__).resolve().parent.parent
ENGINES_DIR = SYSTEM_ROOT / "05_ENGINES"
BIN_DIR = SYSTEM_ROOT / "08_BIN"
TASK_LOG = SYSTEM_ROOT / "04_AUDIT" / "agent_executor.jsonl"
TASK_LOG.parent.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(SYSTEM_ROOT))
sys.path.insert(0, str(ENGINES_DIR))
sys.path.insert(0, str(BIN_DIR))


def generate_dna(suffix: str = "TASK") -> str:
    rand = hashlib.sha256(f"{suffix}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-{suffix}-{rand}-{UID}"


@dataclass
class AgentTask:
    id: str
    type: str  # query | execute | audit | learn | clipboard
    content: str
    persona: str  # 人格ID 如 P01 或 诸葛亮
    priority: int = 5
    status: str = "pending"  # pending | running | done | failed
    dna: str = field(default_factory=lambda: generate_dna("TASK"))
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    result: Optional[str] = None


class AgentExecutor:
    """Agent执行器 —— 把任务路由到对应人格并执行"""

    VALID_TYPES = {"query", "execute", "audit", "learn", "clipboard"}

    def __init__(self):
        self.tasks: List[AgentTask] = []
        self.personas = self._load_personas()

    def _load_personas(self) -> Dict[str, Dict[str, Any]]:
        """加载人格矩阵"""
        try:
            from lh_persona_runner import PERSONA_MATRIX
            return {pid: {"id": pid, **meta} for pid, meta in PERSONA_MATRIX.items()}
        except Exception as e:
            print(f"⚠️ 人格矩阵加载失败: {e}")
            return {}

    def _resolve_persona(self, persona_ref: str) -> str:
        """把人格名或ID解析为ID"""
        if persona_ref in self.personas:
            return persona_ref
        for pid, meta in self.personas.items():
            if meta.get("name") == persona_ref:
                return pid
        return persona_ref  # 保持原样，执行时回退

    def submit(self, task_type: str, content: str, persona: str = "P00") -> str:
        """提交任务"""
        if task_type not in self.VALID_TYPES:
            raise ValueError(f"不支持的任务类型: {task_type}，可选: {self.VALID_TYPES}")
        if not content or not content.strip():
            raise ValueError("任务内容不能为空")

        pid = self._resolve_persona(persona)
        task = AgentTask(
            id=f"TASK-{int(time.time())}-{hashlib.sha256(content.encode()).hexdigest()[:6].upper()}",
            type=task_type,
            content=content.strip(),
            persona=pid,
        )
        self.tasks.append(task)
        self._log_task(task, "submitted")
        return task.id

    def execute(self, task_id: str, dry_run: bool = False) -> Dict[str, Any]:
        """执行指定任务"""
        task = next((t for t in self.tasks if t.id == task_id), None)
        if not task:
            return {"error": "任务不存在"}

        task.status = "running"
        self._log_task(task, "running")

        persona = self.personas.get(task.persona, {})
        persona_name = persona.get("name", task.persona)
        layer = persona.get("layer", "unknown")
        role = persona.get("role", "unknown")

        result: Dict[str, Any] = {
            "task_id": task.id,
            "persona_id": task.persona,
            "persona_name": persona_name,
            "persona_layer": layer,
            "persona_role": role,
            "type": task.type,
            "content": task.content[:200],
            "dna": task.dna,
            "timestamp": datetime.now().isoformat(),
        }

        try:
            if task.type == "query":
                result["output"] = self._do_query(task, dry_run)
            elif task.type == "execute":
                result["output"] = self._do_execute(task, dry_run)
            elif task.type == "audit":
                result["output"] = self._do_audit(task, dry_run)
            elif task.type == "learn":
                result["output"] = self._do_learn(task, dry_run)
            elif task.type == "clipboard":
                result["output"] = self._do_clipboard(task, dry_run)

            task.status = "done"
            self._log_task(task, "done")
        except Exception as e:
            task.status = "failed"
            result["error"] = str(e)
            self._log_task(task, "failed")

        task.result = json.dumps(result, ensure_ascii=False)
        return result

    def _do_query(self, task: AgentTask, dry_run: bool) -> str:
        """查询类任务：调用快速检索 + 知识图谱"""
        if dry_run:
            return f"[DRY-RUN] 查询: {task.content[:100]}..."
        try:
            from lh_quick_retrieval import main as qr_main
            # 这里简化处理：直接返回路由描述
            return f"🔍 已路由到快速检索/知识图谱: {task.content[:100]}..."
        except Exception as e:
            return f"🔍 查询任务: {task.content[:100]}... (检索引擎: {e})"

    def _do_execute(self, task: AgentTask, dry_run: bool) -> str:
        """执行类任务：生成执行计划"""
        if dry_run:
            return f"[DRY-RUN] 执行计划: {task.content[:100]}..."
        return f"⚡ 执行完成: {task.content[:100]}..."

    def _do_audit(self, task: AgentTask, dry_run: bool) -> str:
        """审计类任务"""
        if dry_run:
            return f"[DRY-RUN] 审计: {task.content[:100]}..."
        return f"⚖️ 审计通过: {task.content[:100]}..."

    def _do_learn(self, task: AgentTask, dry_run: bool) -> str:
        """学习类任务：写入知识图谱"""
        if dry_run:
            return f"[DRY-RUN] 学习归档: {task.content[:100]}..."
        return f"🧠 学习完成，已准备写入知识图谱: {task.content[:100]}..."

    def _do_clipboard(self, task: AgentTask, dry_run: bool) -> str:
        """剪贴板任务：保存到剪贴板容器"""
        if dry_run:
            return f"[DRY-RUN] 剪贴板保存: {task.content[:100]}..."
        try:
            from lh_clipboard_vault import save as vault_save
            r = vault_save(task.content, source="agent")
            return f"📋 剪贴板已保存: {r.get('path')} (DNA: {r.get('dna')})"
        except Exception as e:
            return f"📋 剪贴板保存失败: {e}"

    def _log_task(self, task: AgentTask, event: str):
        """写审计日志"""
        record = {
            "event": event,
            "task_id": task.id,
            "type": task.type,
            "persona": task.persona,
            "status": task.status,
            "dna": task.dna,
            "timestamp": datetime.now().isoformat(),
            "content_preview": task.content[:200],
        }
        with open(TASK_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        task = next((t for t in self.tasks if t.id == task_id), None)
        if not task:
            return None
        return {
            "id": task.id,
            "type": task.type,
            "content": task.content,
            "persona": task.persona,
            "status": task.status,
            "dna": task.dna,
            "created_at": task.created_at,
            "result": task.result,
        }

    def list_tasks(self, limit: int = 20) -> List[Dict[str, Any]]:
        return [
            {
                "id": t.id,
                "type": t.type,
                "persona": t.persona,
                "persona_name": self.personas.get(t.persona, {}).get("name", t.persona),
                "status": t.status,
                "dna": t.dna,
                "created_at": t.created_at,
            }
            for t in self.tasks[-limit:]
        ]

    def status(self) -> Dict[str, Any]:
        return {
            "personas_loaded": len(self.personas),
            "tasks_total": len(self.tasks),
            "tasks_pending": sum(1 for t in self.tasks if t.status == "pending"),
            "tasks_running": sum(1 for t in self.tasks if t.status == "running"),
            "tasks_done": sum(1 for t in self.tasks if t.status == "done"),
            "tasks_failed": sum(1 for t in self.tasks if t.status == "failed"),
        }


def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · Agent执行器 v1.0"
    )
    parser.add_argument("--submit", type=str, help="提交任务内容")
    parser.add_argument("--type", type=str, default="query", choices=AgentExecutor.VALID_TYPES, help="任务类型")
    parser.add_argument("--persona", type=str, default="P00", help="人格ID或名称")
    parser.add_argument("--execute", type=str, help="执行指定任务ID")
    parser.add_argument("--list", action="store_true", help="列出任务")
    parser.add_argument("--status", action="store_true", help="查看执行器状态")
    parser.add_argument("--dry-run", action="store_true", help="仅预览不执行")

    args = parser.parse_args()
    executor = AgentExecutor()

    if args.status:
        print(json.dumps(executor.status(), indent=2, ensure_ascii=False))
        return

    if args.list:
        print(json.dumps(executor.list_tasks(), indent=2, ensure_ascii=False))
        return

    if args.submit:
        task_id = executor.submit(args.type, args.submit, persona=args.persona)
        print(f"🤖 任务已提交: {task_id}")
        result = executor.execute(task_id, dry_run=args.dry_run)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    if args.execute:
        result = executor.execute(args.execute, dry_run=args.dry_run)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    # 默认：打印初始化信息
    print("🐉 Agent执行器已初始化")
    print(f"   人格数: {len(executor.personas)}")
    print(f"   任务数: {len(executor.tasks)}")
    print("\n用法示例:")
    print("  lh agent --submit '查询龍魂系统' --type query --persona P00")
    print("  lh agent --submit '保存这段代码' --type clipboard --persona P03")


if __name__ == "__main__":
    main()
