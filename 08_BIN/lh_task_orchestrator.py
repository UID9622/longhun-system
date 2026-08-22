# DNA: #龍芯⚡️丙午·丙申·甲子·癸酉·䷪夬-CODE-补DNA-da2501db
#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
🐉 龍魂任务编排与执行可视化引擎 v1.1
将用户需求自动拆解为可执行任务链，追踪每一步执行状态

DNA: #龍芯⚡️丙午·癸未·壬午·丙午·䷳艮为山-TASK-ORCHESTRATOR-v1.1-UID9622

v1.1 修订要点:
  ① MD5 → SHA-256（对齐 L0 密码学标准）
  ② _create_subtask 由桩函数补全为完整实现（步骤落库）
  ③ 暂停/恢复/取消改为协作式线程控制（threading.Event）
  ④ 新增任务状态机（非法转换拒绝）+ 断点续跑（已完成步骤跳过）
  ⑤ 接入三色审计与 L0·R4 数根熔断（dr∈{3,9} → 🔴）
  ⑥ SQLite 开启 WAL + busy_timeout，多线程读写安全
  ⑦ 新增高危命令黑名单、review 复核子命令、retry 重试

用法:
  lh --task create --title "门户落地页开发" --priority 8
  lh --task list [--status pending]
  lh --task status TASK-20260804-XXXX
  lh --task execute TASK-20260804-XXXX [--sync]
  lh --task pause TASK-20260804-XXXX
  lh --task resume TASK-20260804-XXXX
  lh --task cancel TASK-20260804-XXXX
  lh --task review TASK-20260804-XXXX      # 🆕 人工复核，解除🟡待审
  lh --task retry TASK-20260804-XXXX       # 🆕 失败任务重试
  lh --task serve --port 9631              # 启动任务看板Web服务
"""

import os
import sys
import json
import hashlib
import time
import sqlite3
import threading
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import logging

# ============================================================
# 配置
# ============================================================

ROOT_DIR = Path.home() / "longhun-system"
TASK_DIR = ROOT_DIR / "25_TASK_ENGINE"
TASK_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = TASK_DIR / "tasks.db"
LOG_DIR = ROOT_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

DNA_PREFIX = "#龍芯⚡️丙午·癸未·壬午·丙午·䷳艮为山"

# 🆕 v1.1 修订注①: MD5 → SHA-256（对齐 L0 密码学标准，与受益算法引擎一致）
def _sha256_short(text: str, length: int = 8) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length].upper()

def generate_dna(module: str = "TASK") -> str:
    h = _sha256_short(f"{module}{time.time()}{os.getpid()}")
    return f"{DNA_PREFIX}-{module}-UID9622-{h}"

# ============================================================
# 🆕 v1.1 修订注⑤: 三色审计 + L0·R4 数根熔断
# ============================================================

def digital_root(n: int) -> int:
    """数根: dr(n) ∈ {1..9}，0 单独返回 0"""
    return 0 if n == 0 else (1 + (n - 1) % 9)

def task_dr(task_id: str) -> int:
    """任务的数学根: SHA-256(task_id) 整数值的数根（确定性，可复算）"""
    h = int(hashlib.sha256(task_id.encode("utf-8")).hexdigest(), 16)
    return digital_root(h)

# 高危命令黑名单 → 命中即 🔴
HIGH_RISK_PATTERNS = [
    "rm -rf", "sudo ", "mkfs", ":(){", "curl | sh", "wget | sh",
    "> /dev/sd", "chmod 777 /", "dd if=", "shutdown", "reboot",
]

def audit_task(task: "Task", steps: List["TaskStep"]) -> Dict:
    """三色审计: 🟢 通行 / 🟡 待审 / 🔴 阻断（熔断）"""
    dr = task_dr(task.task_id)
    if dr in (3, 9):
        return {
            "color": "🔴", "dr": dr,
            "reason": f"L0·R4 熔断: 数根 dr={dr} ∈ {{3,9}}",
            "action": "拒绝执行，需人工重签 DNA 后重建任务",
        }
    for s in steps:
        cmd = (s.command or "") + " " + (s.script or "")
        for p in HIGH_RISK_PATTERNS:
            if p in cmd:
                return {
                    "color": "🔴", "dr": dr,
                    "reason": f"高危命令命中黑名单: '{p.strip()}'（步骤 {s.step_id}）",
                    "action": "阻断，转入人工审核队列",
                }
    if task.priority >= 9 and "human-reviewed" not in task.tags:
        return {
            "color": "🟡", "dr": dr,
            "reason": "优先级 ≥ 9 且无 human-reviewed 标签",
            "action": "挂起待审：lh --task review <task_id> 后放行",
        }
    return {"color": "🟢", "dr": dr, "reason": "常规任务，审计通过", "action": "通行"}

# ============================================================
# 日志
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(str(LOG_DIR / f"task_{datetime.now().strftime('%Y%m%d')}.log")),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("task_orchestrator")

# ============================================================
# 枚举
# ============================================================

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 5
    HIGH = 8
    CRITICAL = 10

class ExecutorType(Enum):
    AI = "ai"
    HUMAN = "human"
    SYSTEM = "system"
    AUTO = "auto"

# 🆕 v1.1 修订注④: 任务状态机 —— 非法转换一律拒绝并留痕
LEGAL_TRANSITIONS = {
    "pending":   ["running", "cancelled"],
    "running":   ["paused", "completed", "failed", "cancelled"],
    "paused":    ["running", "cancelled"],
    "completed": [],
    "failed":    ["pending"],      # 允许 retry 重试
    "cancelled": [],
}

# ============================================================
# 数据类
# ============================================================

@dataclass
class Task:
    """任务数据结构"""
    task_id: str
    title: str
    description: str
    status: str = "pending"
    priority: int = 5
    dna: str = ""
    parent_id: Optional[str] = None
    subtasks: List[str] = field(default_factory=list)
    assigned_to: str = "auto"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    execution_log: List[Dict] = field(default_factory=list)
    result: Dict = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    estimated_duration: int = 0  # 秒
    actual_duration: int = 0

@dataclass
class TaskStep:
    """任务步骤"""
    step_id: str
    task_id: str
    order: int
    name: str
    description: str
    status: str = "pending"
    executor: str = "auto"
    command: Optional[str] = None   # 可执行命令
    script: Optional[str] = None    # 可执行脚本
    output: str = ""
    error: str = ""
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    dna: str = field(default_factory=lambda: generate_dna("STEP"))
    duration_ms: int = 0

# ============================================================
# 任务数据库
# ============================================================

class TaskDB:
    """任务存储数据库"""

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_db()

    # 🆕 v1.1 修订注⑥: 统一连接入口，WAL + busy_timeout，多线程安全
    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), timeout=30)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=30000")
        return conn

    def _init_db(self):
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                title TEXT,
                description TEXT,
                status TEXT,
                priority INTEGER,
                dna TEXT,
                parent_id TEXT,
                subtasks TEXT,
                assigned_to TEXT,
                created_at TEXT,
                updated_at TEXT,
                completed_at TEXT,
                result TEXT,
                tags TEXT,
                estimated_duration INTEGER,
                actual_duration INTEGER
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS task_steps (
                step_id TEXT PRIMARY KEY,
                task_id TEXT,
                order_num INTEGER,
                name TEXT,
                description TEXT,
                status TEXT,
                executor TEXT,
                command TEXT,
                script TEXT,
                output TEXT,
                error TEXT,
                started_at TEXT,
                completed_at TEXT,
                dna TEXT,
                duration_ms INTEGER,
                FOREIGN KEY(task_id) REFERENCES tasks(task_id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS execution_logs (
                log_id TEXT PRIMARY KEY,
                task_id TEXT,
                step_id TEXT,
                level TEXT,
                message TEXT,
                data TEXT,
                dna TEXT,
                timestamp TEXT,
                FOREIGN KEY(task_id) REFERENCES tasks(task_id)
            )
        """)

        conn.commit()
        conn.close()

    def save_task(self, task: Task) -> bool:
        conn = self._connect()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT OR REPLACE INTO tasks
                (task_id, title, description, status, priority, dna, parent_id,
                 subtasks, assigned_to, created_at, updated_at, completed_at,
                 result, tags, estimated_duration, actual_duration)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task.task_id, task.title, task.description, task.status,
                task.priority, task.dna, task.parent_id,
                json.dumps(task.subtasks), task.assigned_to,
                task.created_at, task.updated_at, task.completed_at,
                json.dumps(task.result), json.dumps(task.tags),
                task.estimated_duration, task.actual_duration,
            ))
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"保存任务失败: {e}")
            return False
        finally:
            conn.close()

    def _row_to_task(self, row: sqlite3.Row) -> Task:
        subs = []
        if row["subtasks"]:
            try:
                subs = json.loads(row["subtasks"])
            except json.JSONDecodeError:
                subs = []
        r = {}
        if row["result"]:
            try:
                r = json.loads(row["result"])
            except json.JSONDecodeError:
                r = {}
        t = []
        if row["tags"]:
            try:
                t = json.loads(row["tags"])
            except json.JSONDecodeError:
                t = []
        return Task(
            task_id=row["task_id"], title=row["title"],
            description=row["description"], status=row["status"],
            priority=row["priority"], dna=row["dna"],
            parent_id=row["parent_id"],
            subtasks=subs,
            assigned_to=row["assigned_to"],
            created_at=row["created_at"], updated_at=row["updated_at"],
            completed_at=row["completed_at"],
            result=r, tags=t,
            estimated_duration=row["estimated_duration"] or 0,
            actual_duration=row["actual_duration"] or 0,
        )

    def get_task(self, task_id: str) -> Optional[Task]:
        conn = self._connect()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,))
        row = cur.fetchone()
        conn.close()
        return self._row_to_task(row) if row else None

    def list_tasks(self, status: Optional[str] = None, limit: int = 50) -> List[Task]:
        conn = self._connect()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        query = "SELECT * FROM tasks"
        params: List[Any] = []
        if status:
            query += " WHERE status = ?"
            params.append(status)
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()
        return [self._row_to_task(r) for r in rows]

    def update_status(self, task_id: str, status: str,
                      completed_at: Optional[str] = None,
                      enforce_machine: bool = True) -> bool:
        """🆕 v1.1: 状态机校验 —— 非法转换拒绝并留痕"""
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT status FROM tasks WHERE task_id = ?", (task_id,))
        row = cur.fetchone()
        if not row:
            conn.close()
            return False
        current = row[0]
        if enforce_machine and status not in LEGAL_TRANSITIONS.get(current, []):
            logger.warning(f"⛔ 非法状态转换被拒绝: {task_id} {current} → {status}")
            self.add_log(task_id, "", "warn",
                         f"非法状态转换被拒绝: {current} → {status}")
            conn.close()
            return False
        cur.execute("""
            UPDATE tasks SET status = ?, updated_at = ?, completed_at = COALESCE(?, completed_at)
            WHERE task_id = ?
        """, (status, datetime.now().isoformat(), completed_at, task_id))
        conn.commit()
        conn.close()
        return True

    # 🆕 v1.1 修订注②: 步骤持久化（原 _create_subtask 为桩函数，步骤从未落库）
    def save_step(self, step: TaskStep) -> bool:
        conn = self._connect()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT OR REPLACE INTO task_steps
                (step_id, task_id, order_num, name, description, status, executor,
                 command, script, output, error, started_at, completed_at, dna, duration_ms)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                step.step_id, step.task_id, step.order, step.name, step.description,
                step.status, step.executor, step.command, step.script, step.output,
                step.error, step.started_at, step.completed_at, step.dna, step.duration_ms,
            ))
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"保存步骤失败: {e}")
            return False
        finally:
            conn.close()

    def get_steps(self, task_id: str) -> List[TaskStep]:
        conn = self._connect()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM task_steps WHERE task_id = ? ORDER BY order_num ASC",
            (task_id,),
        )
        rows = cur.fetchall()
        conn.close()
        return [TaskStep(
            step_id=r["step_id"], task_id=r["task_id"], order=r["order_num"],
            name=r["name"], description=r["description"], status=r["status"],
            executor=r["executor"], command=r["command"], script=r["script"],
            output=r["output"] or "", error=r["error"] or "",
            started_at=r["started_at"], completed_at=r["completed_at"],
            dna=r["dna"], duration_ms=r["duration_ms"] or 0,
        ) for r in rows]

    def update_step(self, step_id: str, **fields) -> bool:
        allowed = {"status", "output", "error", "started_at", "completed_at", "duration_ms"}
        sets = {k: v for k, v in fields.items() if k in allowed}
        if not sets:
            return False
        clause = ", ".join(f"{k} = ?" for k in sets)
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(f"UPDATE task_steps SET {clause} WHERE step_id = ?",
                    (*sets.values(), step_id))
        conn.commit()
        ok = cur.rowcount > 0
        conn.close()
        return ok

    def count_steps(self, task_id: str) -> int:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM task_steps WHERE task_id = ?", (task_id,))
        n = cur.fetchone()[0]
        conn.close()
        return n

    def add_log(self, task_id: str, step_id: str, level: str,
                message: str, data: Dict = None):
        # 🆕 v1.1 修订注①: MD5 → SHA-256
        log_id = f"LOG-{_sha256_short(f'{task_id}{time.time()}{message}', 16)}"
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO execution_logs
            (log_id, task_id, step_id, level, message, data, dna, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            log_id, task_id, step_id, level, message,
            json.dumps(data, ensure_ascii=False) if data else None,
            generate_dna("LOG"),
            datetime.now().isoformat(),
        ))
        conn.commit()
        conn.close()

    def add_tag(self, task_id: str, tag: str) -> bool:
        """🆕 v1.1: 追加标签（用于 human-reviewed 复核放行）"""
        task = self.get_task(task_id)
        if not task:
            return False
        if tag not in task.tags:
            task.tags.append(tag)
        return self.save_task(task)

# ============================================================
# 任务编排引擎核心
# ============================================================

class TaskOrchestrator:
    """任务编排引擎（v1.1：协作式线程控制 + 状态机 + 三色审计）"""

    # 模拟执行单步时长（秒），分片睡眠保证暂停/取消毫秒级响应
    SIM_STEP_SECONDS = 1.0
    SIM_SLICE = 0.05
    CMD_TIMEOUT = 30

    def __init__(self, db_path: Path = DB_PATH):
        self.db = TaskDB(db_path)
        self.running_tasks: Dict[str, threading.Thread] = {}
        self._cancel_events: Dict[str, threading.Event] = {}  # 🆕 set   = 请求取消
        self._pause_events: Dict[str, threading.Event] = {}   # 🆕 clear = 暂停中
        self._lock = threading.Lock()
        self.is_running = False

    # ============================================================
    # 任务创建
    # ============================================================

    def create_task(self, title: str, description: str = "",
                    priority: int = 5, tags: List[str] = None,
                    subtasks: List[Dict] = None) -> Task:
        """创建新任务"""
        # 🆕 v1.1 修订注①: MD5 → SHA-256
        task_id = (f"TASK-{datetime.now().strftime('%Y%m%d')}-"
                   f"{_sha256_short(f'{title}{time.time()}')}")

        task = Task(
            task_id=task_id,
            title=title,
            description=description,
            priority=priority,
            dna=generate_dna("TASK"),
            tags=tags or [],
            status="pending",
        )

        self.db.save_task(task)
        self.db.add_log(task_id, "", "info", f"任务创建: {title}")

        # 🆕 v1.1 修订注②: 子任务真实落库
        if subtasks:
            for st in subtasks:
                step = self._create_subtask(task_id, st)
                task.subtasks.append(step.step_id)
            self.db.save_task(task)

        logger.info(f"📋 任务创建: {task_id} - {title}")
        return task

    def _create_subtask(self, parent_id: str, data: Dict) -> TaskStep:
        """🆕 v1.1 补全实现: 创建子任务步骤并落库（原为桩函数 pass）"""
        order = data.get("order") or (self.db.count_steps(parent_id) + 1)
        step = TaskStep(
            step_id=data.get("id", f"{parent_id}-S{order:02d}"),
            task_id=parent_id,
            order=order,
            name=data.get("name", "未命名步骤"),
            description=data.get("description", ""),
            executor=data.get("executor", "auto"),
            command=data.get("command"),
            script=data.get("script"),
        )
        self.db.save_step(step)
        self.db.add_log(parent_id, step.step_id, "info", f"子步骤创建: {step.name}")
        return step

    # ============================================================
    # 任务执行
    # ============================================================

    def execute_task(self, task_id: str, async_mode: bool = True) -> Dict:
        """执行任务（先过三色审计，🟢 才放行）"""
        task = self.db.get_task(task_id)
        if not task:
            return {"error": "任务不存在"}
        if task.status not in ("pending",):
            return {"error": f"任务状态为: {task.status}，仅 pending 可启动（failed 请先 retry）"}

        # 🆕 v1.1 修订注⑤: 三色审计闸门
        steps = self.db.get_steps(task_id)
        audit = audit_task(task, steps)
        self.db.add_log(task_id, "", "audit",
                        f"三色审计: {audit['color']} {audit['reason']}", audit)
        if audit["color"] == "🔴":
            return {"status": "blocked", "audit": audit, "task_id": task_id}
        if audit["color"] == "🟡":
            return {"status": "pending_review", "audit": audit, "task_id": task_id}

        self.db.update_status(task_id, "running")
        self.db.add_log(task_id, "", "info", "任务开始执行")

        # 🆕 v1.1 修订注③: 注册协作控制事件
        with self._lock:
            self._cancel_events[task_id] = threading.Event()
            self._pause_events[task_id] = threading.Event()
            self._pause_events[task_id].set()  # 默认非暂停

        if async_mode:
            thread = threading.Thread(
                target=self._run_task, args=(task_id,), daemon=True,
                name=f"task-{task_id}",
            )
            thread.start()
            self.running_tasks[task_id] = thread
            return {"status": "started", "task_id": task_id, "audit": audit}
        return self._run_task(task_id)

    def _run_task(self, task_id: str) -> Dict:
        """🆕 v1.1 修订注③④: 真实步骤执行器 + 协作式中断 + 断点续跑"""
        task = self.db.get_task(task_id)
        if not task:
            return {"error": "任务不存在"}

        cancel_ev = self._cancel_events.setdefault(task_id, threading.Event())
        pause_ev = self._pause_events.setdefault(task_id, threading.Event())
        pause_ev.set()

        steps = self.db.get_steps(task_id)
        if not steps:
            # 无子任务时包装一个隐式步骤，保证日志与状态机完整
            steps = [self._create_subtask(task_id, {
                "name": "执行任务主体", "description": task.description or task.title,
            })]

        started = time.time()
        try:
            for step in steps:
                if step.status == "completed":
                    continue  # 🆕 断点续跑: 已完成步骤自动跳过

                # 取消检查（步骤边界）
                if cancel_ev.is_set():
                    self.db.update_step(step.step_id, status="cancelled")
                    self._finish(task_id, "cancelled", started,
                                 f"🚫 任务在步骤 {step.step_id} 前被取消（协作式中断）")
                    return {"status": "cancelled", "task_id": task_id}

                self.db.update_step(step.step_id, status="running",
                                    started_at=datetime.now().isoformat())
                self.db.add_log(task_id, step.step_id, "info",
                                f"步骤开始: {step.name}")

                result = self._execute_step(task_id, step, cancel_ev, pause_ev)

                if result["status"] == "aborted":
                    self.db.update_step(step.step_id, status="cancelled")
                    self._finish(task_id, "cancelled", started,
                                 f"🚫 步骤 {step.step_id} 执行中被取消")
                    return {"status": "cancelled", "task_id": task_id}

                if result["status"] != "success":
                    self.db.update_step(step.step_id, status="failed",
                                        error=result.get("error", ""),
                                        completed_at=datetime.now().isoformat(),
                                        duration_ms=result["duration_ms"])
                    self._finish(task_id, "failed", started,
                                 f"❌ 步骤失败: {step.name} — {result.get('error','')}")
                    return {"status": "failed", "task_id": task_id,
                            "error": result.get("error", "")}

                self.db.update_step(step.step_id, status="completed",
                                    output=result.get("output", ""),
                                    completed_at=datetime.now().isoformat(),
                                    duration_ms=result["duration_ms"])
                self.db.add_log(task_id, step.step_id, "info",
                                f"步骤完成: {step.name}（{result['duration_ms']}ms）")

            self._finish(task_id, "completed", started, "✅ 任务完成")
            return {"status": "completed", "task_id": task_id}

        except Exception as e:
            self._finish(task_id, "failed", started, f"❌ 任务异常: {e}")
            return {"status": "failed", "task_id": task_id, "error": str(e)}
        finally:
            with self._lock:
                self.running_tasks.pop(task_id, None)

    def _execute_step(self, task_id: str, step: TaskStep,
                      cancel_ev: threading.Event,
                      pause_ev: threading.Event) -> Dict:
        """执行单个步骤：有 command 走真实子进程，否则分片模拟（可暂停/可取消）"""
        t0 = time.time()

        def interrupted() -> bool:
            """等待暂停期间同时监听取消；返回 True 表示被取消"""
            while not pause_ev.is_set():
                if cancel_ev.is_set():
                    return True
                time.sleep(self.SIM_SLICE)
            return cancel_ev.is_set()

        if step.command:
            # 🆕 真实命令执行（30s 超时 + 输出捕获；高危命令已在审计层拦截）
            if interrupted():
                return {"status": "aborted", "duration_ms": 0}
            try:
                proc = subprocess.run(
                    step.command, shell=True, capture_output=True,
                    text=True, timeout=self.CMD_TIMEOUT,
                )
                duration = int((time.time() - t0) * 1000)
                if proc.returncode == 0:
                    return {"status": "success", "output": proc.stdout.strip(),
                            "duration_ms": duration}
                return {"status": "failure", "error": proc.stderr.strip()[:500],
                        "duration_ms": duration}
            except subprocess.TimeoutExpired:
                return {"status": "failure",
                        "error": f"命令超时（>{self.CMD_TIMEOUT}s）",
                        "duration_ms": int((time.time() - t0) * 1000)}

        # 模拟执行：分片睡眠，暂停/取消响应 ≤ 50ms
        slices = max(1, int(self.SIM_STEP_SECONDS / self.SIM_SLICE))
        for _ in range(slices):
            if interrupted():
                return {"status": "aborted",
                        "duration_ms": int((time.time() - t0) * 1000)}
            time.sleep(self.SIM_SLICE)
        return {"status": "success", "output": f"模拟执行完成: {step.name}",
                "duration_ms": int((time.time() - t0) * 1000)}

    def _finish(self, task_id: str, status: str, started: float, message: str):
        actual = int(time.time() - started)
        completed_at = datetime.now().isoformat() if status in (
            "completed", "failed", "cancelled") else None
        self.db.update_status(task_id, status, completed_at=completed_at)
        conn = self.db._connect()
        conn.execute("UPDATE tasks SET actual_duration = ? WHERE task_id = ?",
                     (actual, task_id))
        conn.commit()
        conn.close()
        level = "info" if status == "completed" else ("warn" if status == "cancelled" else "error")
        self.db.add_log(task_id, "", level, f"{message}（实际耗时 {actual}s）")

    # ============================================================
    # 任务管理
    # ============================================================

    def pause_task(self, task_id: str) -> Dict:
        """暂停任务（🆕 协作式: 运行线程在步骤内 50ms 内响应并原地等待）"""
        task = self.db.get_task(task_id)
        if not task:
            return {"error": "任务不存在"}
        if task.status != "running":
            return {"error": f"任务不在运行状态: {task.status}"}

        with self._lock:
            self._pause_events.setdefault(task_id, threading.Event()).clear()
        self.db.update_status(task_id, "paused")
        self.db.add_log(task_id, "", "warn", "任务已暂停（线程原地挂起，进度保留）")
        return {"status": "paused", "task_id": task_id}

    def resume_task(self, task_id: str) -> Dict:
        """恢复任务（🆕 修订注③: 唤醒原线程，不再重复启动新线程）"""
        task = self.db.get_task(task_id)
        if not task:
            return {"error": "任务不存在"}
        if task.status != "paused":
            return {"error": f"任务不在暂停状态: {task.status}"}

        if task_id in self._pause_events:
            # 本进程持有原线程 → 直接唤醒，断点续跑
            self._pause_events[task_id].set()
            self.db.update_status(task_id, "running")
            self.db.add_log(task_id, "", "info", "任务已恢复（唤醒原线程，断点续跑）")
            return {"status": "resumed", "mode": "wake-original-thread",
                    "task_id": task_id}

        # 跨进程恢复: 原线程已不存在，从「未完成步骤」重新拉起
        self.db.add_log(task_id, "", "info", "任务跨进程恢复（跳过已完成步骤）")
        conn = self.db._connect()
        conn.execute("UPDATE tasks SET status = 'pending', updated_at = ? WHERE task_id = ?",
                     (datetime.now().isoformat(), task_id))
        conn.commit()
        conn.close()
        return self.execute_task(task_id, async_mode=True)

    def cancel_task(self, task_id: str) -> Dict:
        """取消任务（🆕 协作式: 置位取消事件，线程在下一个检查点退出）"""
        task = self.db.get_task(task_id)
        if not task:
            return {"error": "任务不存在"}
        if task.status in ["completed", "failed", "cancelled"]:
            return {"error": f"任务已结束: {task.status}"}

        with self._lock:
            self._cancel_events.setdefault(task_id, threading.Event()).set()
            # 若线程正挂起在暂停点，先唤醒让它看到取消标志
            if task_id in self._pause_events:
                self._pause_events[task_id].set()

        self.db.update_status(task_id, "cancelled",
                              completed_at=datetime.now().isoformat())
        self.db.add_log(task_id, "", "warn", "任务已取消（协作式中断信号已发出）")
        return {"status": "cancelled", "task_id": task_id}

    def review_task(self, task_id: str) -> Dict:
        """🆕 v1.1: 人工复核 —— 加盖 human-reviewed 标签，解除 🟡 待审"""
        task = self.db.get_task(task_id)
        if not task:
            return {"error": "任务不存在"}
        self.db.add_tag(task_id, "human-reviewed")
        self.db.add_log(task_id, "", "audit",
                        "人工复核通过: human-reviewed 标签已加盖（UID9622 授权链）")
        audit = audit_task(self.db.get_task(task_id), self.db.get_steps(task_id))
        return {"status": "reviewed", "task_id": task_id, "audit": audit}

    def retry_task(self, task_id: str) -> Dict:
        """🆕 v1.1: 失败任务重试（failed → pending → 重新走审计）"""
        task = self.db.get_task(task_id)
        if not task:
            return {"error": "任务不存在"}
        if task.status != "failed":
            return {"error": f"仅 failed 状态可重试: {task.status}"}
        ok = self.db.update_status(task_id, "pending")
        if not ok:
            return {"error": "状态机拒绝转换"}
        self.db.add_log(task_id, "", "info", "任务重试: failed → pending")
        return {"status": "pending", "task_id": task_id}

    # ============================================================
    # 查询
    # ============================================================

    def get_task_status(self, task_id: str) -> Dict:
        task = self.db.get_task(task_id)
        if not task:
            return {"error": "任务不存在"}
        steps = self.db.get_steps(task_id)
        return {
            "task_id": task.task_id,
            "title": task.title,
            "status": task.status,
            "priority": task.priority,
            "dna": task.dna,
            "dr": task_dr(task.task_id),  # 🆕 数学根，可复算
            "created_at": task.created_at,
            "updated_at": task.updated_at,
            "subtasks": len(steps),
            "steps": [{"step_id": s.step_id, "name": s.name,
                       "status": s.status, "duration_ms": s.duration_ms}
                      for s in steps],
            "logs": self._get_task_logs(task_id, limit=10),
        }

    def _get_task_logs(self, task_id: str, limit: int = 50) -> List[Dict]:
        conn = self.db._connect()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM execution_logs
            WHERE task_id = ?
            ORDER BY timestamp DESC LIMIT ?
        """, (task_id, limit))
        rows = cur.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def list_tasks(self, status: Optional[str] = None) -> List[Dict]:
        tasks = self.db.list_tasks(status)
        return [{
            "task_id": t.task_id, "title": t.title, "status": t.status,
            "priority": t.priority, "dna": t.dna, "created_at": t.created_at,
        } for t in tasks]

    def get_stats(self) -> Dict:
        all_tasks = self.db.list_tasks()
        return {
            "total": len(all_tasks),
            "pending": sum(1 for t in all_tasks if t.status == "pending"),
            "running": sum(1 for t in all_tasks if t.status == "running"),
            "completed": sum(1 for t in all_tasks if t.status == "completed"),
            "failed": sum(1 for t in all_tasks if t.status == "failed"),
            "paused": sum(1 for t in all_tasks if t.status == "paused"),
            "cancelled": sum(1 for t in all_tasks if t.status == "cancelled"),
        }

# ============================================================
# 任务看板Web服务
# ============================================================

def serve_web(port: int = 9631, host: str = "0.0.0.0"):
    """启动任务看板Web服务"""
    try:
        from fastapi import FastAPI
        from fastapi.responses import HTMLResponse
        import uvicorn
    except ImportError:
        print("请安装: pip install fastapi uvicorn")
        return

    app = FastAPI(title="🐉 龍魂任务看板", version="1.1")
    orchestrator = TaskOrchestrator()

    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>🐉 龍魂任务看板</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Inter', -apple-system, sans-serif;
                background: #0a0a14; color: #e0e0e0; padding: 24px;
            }
            .header {
                display: flex; justify-content: space-between; align-items: center;
                margin-bottom: 32px; border-bottom: 1px solid rgba(212,175,55,0.2);
                padding-bottom: 16px;
            }
            .header h1 { color: #d4af37; font-size: 28px; }
            .header .dna { font-size: 12px; color: rgba(212,175,55,0.4); }
            .stats {
                display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
                gap: 16px; margin-bottom: 32px;
            }
            .stat-card {
                background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.06);
                border-radius: 12px; padding: 16px; text-align: center;
            }
            .stat-card .number { font-size: 28px; font-weight: 700; color: #d4af37; }
            .stat-card .label { font-size: 12px; color: rgba(255,255,255,0.4); margin-top: 4px; }
            .task-list { display: flex; flex-direction: column; gap: 12px; }
            .task-item {
                background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06);
                border-radius: 10px; padding: 16px 20px;
                display: flex; justify-content: space-between; align-items: center;
                transition: all 0.2s;
            }
            .task-item:hover { background: rgba(255,255,255,0.06); }
            .task-info .title { font-weight: 600; }
            .task-info .meta { font-size: 12px; color: rgba(255,255,255,0.3); }
            .status-badge {
                padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 500;
            }
            .status-pending { background: rgba(255,255,0,0.15); color: #ffd700; }
            .status-running { background: rgba(0,255,100,0.15); color: #22c55e; }
            .status-completed { background: rgba(0,255,200,0.1); color: #14b8a6; }
            .status-failed { background: rgba(255,0,0,0.15); color: #ef4444; }
            .status-paused { background: rgba(255,165,0,0.15); color: #f59e0b; }
            .status-cancelled { background: rgba(100,100,100,0.2); color: #6b7280; }
            .refresh-btn {
                background: rgba(212,175,55,0.15); border: 1px solid rgba(212,175,55,0.3);
                color: #d4af37; padding: 8px 20px; border-radius: 8px;
                cursor: pointer; font-size: 14px;
            }
            .refresh-btn:hover { background: rgba(212,175,55,0.25); }
            .empty { text-align: center; color: rgba(255,255,255,0.2); padding: 60px 0; }
        </style>
    </head>
    <body>
        <div class="header">
            <div>
                <h1>🐉 龍魂任务看板 v1.1</h1>
                <div class="dna">DNA: #龍芯⚡️丙午·癸未·壬午-TASK-BOARD-UID9622</div>
            </div>
            <button class="refresh-btn" onclick="loadData()">🔄 刷新</button>
        </div>

        <div class="stats" id="stats">
            <div class="stat-card"><div class="number">-</div><div class="label">总计</div></div>
            <div class="stat-card"><div class="number">-</div><div class="label">进行中</div></div>
            <div class="stat-card"><div class="number">-</div><div class="label">已完成</div></div>
            <div class="stat-card"><div class="number">-</div><div class="label">待执行</div></div>
        </div>

        <div class="task-list" id="task-list">
            <div class="empty">暂无任务，创建任务: lh --task create --title "任务名称"</div>
        </div>

        <script>
            async function loadData() {
                try {
                    const [statsRes, tasksRes] = await Promise.all([
                        fetch('/api/stats'), fetch('/api/tasks')
                    ]);
                    const stats = await statsRes.json();
                    const tasks = await tasksRes.json();
                    document.querySelectorAll('.stat-card')[0].querySelector('.number').textContent = stats.total || 0;
                    document.querySelectorAll('.stat-card')[1].querySelector('.number').textContent = stats.running || 0;
                    document.querySelectorAll('.stat-card')[2].querySelector('.number').textContent = stats.completed || 0;
                    document.querySelectorAll('.stat-card')[3].querySelector('.number').textContent = stats.pending || 0;
                    const list = document.getElementById('task-list');
                    if (tasks.length === 0) {
                        list.innerHTML = '<div class="empty">暂无任务</div>';
                        return;
                    }
                    list.innerHTML = tasks.map(t => `
                        <div class="task-item">
                            <div class="task-info">
                                <div class="title">${t.title}</div>
                                <div class="meta">${t.task_id} · ${t.created_at} · ${t.dna}</div>
                            </div>
                            <span class="status-badge status-${t.status}">${t.status}</span>
                        </div>
                    `).join('');
                } catch(e) { console.error(e); }
            }
            loadData();
            setInterval(loadData, 5000);
        </script>
    </body>
    </html>
    """

    @app.get("/", response_class=HTMLResponse)
    async def index():
        return HTML_TEMPLATE

    @app.get("/api/stats")
    async def get_stats():
        return orchestrator.get_stats()

    @app.get("/api/tasks")
    async def get_tasks(status: Optional[str] = None):
        return orchestrator.list_tasks(status)

    @app.get("/api/task/{task_id}")
    async def get_task(task_id: str):
        return orchestrator.get_task_status(task_id)

    @app.post("/api/task")
    async def create_task(data: Dict):
        task = orchestrator.create_task(
            title=data.get("title", "未命名任务"),
            description=data.get("description", ""),
            priority=data.get("priority", 5),
            tags=data.get("tags", []),
            subtasks=data.get("subtasks"),  # 🆕 支持 API 直接下发子任务
        )
        return {"task_id": task.task_id, "status": "created", "dna": task.dna}

    @app.post("/api/task/{task_id}/execute")
    async def execute_task(task_id: str):
        return orchestrator.execute_task(task_id, async_mode=True)

    @app.post("/api/task/{task_id}/pause")
    async def pause_task(task_id: str):
        return orchestrator.pause_task(task_id)

    @app.post("/api/task/{task_id}/resume")
    async def resume_task(task_id: str):
        return orchestrator.resume_task(task_id)

    @app.post("/api/task/{task_id}/cancel")
    async def cancel_task(task_id: str):
        return orchestrator.cancel_task(task_id)

    # 🆕 v1.1: 复核与审计查询端点
    @app.post("/api/task/{task_id}/review")
    async def review_task(task_id: str):
        return orchestrator.review_task(task_id)

    @app.get("/api/task/{task_id}/audit")
    async def get_task_audit(task_id: str):
        task = orchestrator.db.get_task(task_id)
        if not task:
            return {"error": "任务不存在"}
        return audit_task(task, orchestrator.db.get_steps(task_id))

    print(f"""
🐉 龍魂任务看板 v1.1
========================================
🚀 启动服务: http://{host}:{port}
📊 查看任务: http://{host}:{port}
💬 API文档: http://{host}:{port}/docs
========================================
    """)

    uvicorn.run(app, host=host, port=port)

# ============================================================
# 命令行
# ============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="🐉 龍魂任务编排与执行可视化引擎 v1.1"
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    create_parser = subparsers.add_parser("create", help="创建任务")
    create_parser.add_argument("--title", "-t", required=True, help="任务标题")
    create_parser.add_argument("--description", "-d", help="任务描述")
    create_parser.add_argument("--priority", "-p", type=int, default=5, help="优先级 1-10")
    create_parser.add_argument("--tags", help="标签，逗号分隔")

    list_parser = subparsers.add_parser("list", help="列出任务")
    list_parser.add_argument("--status", "-s", help="筛选状态")

    status_parser = subparsers.add_parser("status", help="查看任务状态")
    status_parser.add_argument("task_id", help="任务ID")

    execute_parser = subparsers.add_parser("execute", help="执行任务")
    execute_parser.add_argument("task_id", help="任务ID")
    execute_parser.add_argument("--sync", action="store_true", help="同步执行")

    pause_parser = subparsers.add_parser("pause", help="暂停任务")
    pause_parser.add_argument("task_id", help="任务ID")

    resume_parser = subparsers.add_parser("resume", help="恢复任务")
    resume_parser.add_argument("task_id", help="任务ID")

    cancel_parser = subparsers.add_parser("cancel", help="取消任务")
    cancel_parser.add_argument("task_id", help="任务ID")

    # 🆕 v1.1
    review_parser = subparsers.add_parser("review", help="人工复核，解除🟡待审")
    review_parser.add_argument("task_id", help="任务ID")

    retry_parser = subparsers.add_parser("retry", help="失败任务重试")
    retry_parser.add_argument("task_id", help="任务ID")

    serve_parser = subparsers.add_parser("serve", help="启动任务看板Web服务")
    serve_parser.add_argument("--port", type=int, default=9631, help="端口")
    serve_parser.add_argument("--host", default="0.0.0.0", help="主机")

    args = parser.parse_args()
    orchestrator = TaskOrchestrator()

    if args.command == "create":
        tags = args.tags.split(",") if args.tags else []
        task = orchestrator.create_task(
            title=args.title, description=args.description or "",
            priority=args.priority, tags=tags,
        )
        print(f"✅ 任务创建: {task.task_id}")
        print(f"   DNA: {task.dna}")
        print(f"   数学根 dr: {task_dr(task.task_id)}")
        print(f"   🧬 lh --task status {task.task_id}")

    elif args.command == "list":
        tasks = orchestrator.list_tasks(args.status)
        print(f"\n📋 任务列表 ({len(tasks)} 个)")
        print("-" * 60)
        for t in tasks:
            icon = {"pending": "⏳", "running": "🔄", "completed": "✅",
                    "failed": "❌", "paused": "⏸", "cancelled": "🚫"}.get(t["status"], "❓")
            print(f"  {icon} {t['task_id']}: {t['title']} [{t['status']}]")

    elif args.command == "status":
        result = orchestrator.get_task_status(args.task_id)
        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            print(f"\n📊 任务状态: {result['task_id']}")
            print("-" * 60)
            print(f"  标题: {result['title']}")
            print(f"  状态: {result['status']}")
            print(f"  优先级: {result['priority']}")
            print(f"  DNA: {result['dna']}")
            print(f"  数学根 dr: {result['dr']}")
            print(f"  创建: {result['created_at']}")
            print(f"  更新: {result['updated_at']}")
            print(f"  子任务: {result['subtasks']}")
            for s in result.get("steps", []):
                print(f"    · {s['step_id']} {s['name']} [{s['status']}] {s['duration_ms']}ms")
            if result.get("logs"):
                print("\n📝 最近日志:")
                for log in result["logs"][:5]:
                    print(f"    [{log['level']}] {log['message']}")

    elif args.command == "execute":
        result = orchestrator.execute_task(args.task_id, async_mode=not args.sync)
        print(f"🔄 任务执行: {result}")

    elif args.command == "pause":
        print(f"⏸ {orchestrator.pause_task(args.task_id)}")

    elif args.command == "resume":
        print(f"▶️ {orchestrator.resume_task(args.task_id)}")

    elif args.command == "cancel":
        print(f"🚫 {orchestrator.cancel_task(args.task_id)}")

    elif args.command == "review":
        print(f"🔍 {orchestrator.review_task(args.task_id)}")

    elif args.command == "retry":
        print(f"🔁 {orchestrator.retry_task(args.task_id)}")

    elif args.command == "serve":
        serve_web(port=args.port, host=args.host)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
