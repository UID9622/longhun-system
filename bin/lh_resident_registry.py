#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 常驻工具注册表 v2.0 (Resident Function Registry)
============================================================
系统级自动任务——不需要人叫，到点自己干。

注册的常驻任务：
  disk_cleanup     → 每日凌晨2点   — 清理临时文件、归档旧日志
  log_archive      → 每小时        — 压缩归档日志文件
  memory_monitor   → 每5分钟       — 内存使用监控+预警
  git_auto_sync    → 每30分钟      — Git自动提交+推送
  security_scan    → 每日凌晨3点   — 安全扫描（敏感信息泄露检查）
  health_report    → 每日早8点     — 生成系统健康日报
  persona_health   → 每6小时       — 人格矩阵健康度检查
  dependency_check → 每日          — Python依赖安全检查

架构：
  任务定义 → 调度器 → 执行器 → 审计日志

集成：
  - 对接 lh_event_bus_engine.EventBus
  - 对接 lh_active_observation.ActiveObservationEngine (TIME_EVENT触发)
  - 独立运行: python3 bin/lh_resident_registry.py --daemon

DNA: #龍芯⚡️丙午·辛未·丙戌·亥时·需-RESIDENT-REGISTRY-v2.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import argparse
import glob
import hashlib
import json
import os
import platform
import psutil
import re
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

# ── 项目根 ──
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from bin.lh_event_bus_engine import EventBus, EventType, Event  # noqa: E402

# ── 常量 ──
DNA = "#龍芯⚡️丙午·辛未·乙酉·亥时·需-RESIDENT-REGISTRY-v2.2-SLIM"
VERSION = "2.2.0"
REG_DIR = PROJECT_ROOT / "data" / "resident_registry"
REG_DIR.mkdir(parents=True, exist_ok=True)
TASK_STATE_FILE = REG_DIR / "task_state.json"
AUDIT_LOG_FILE = REG_DIR / "execution_audit.jsonl"

# 日志目录
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

# ── 缓存目录（轻量级，替代数据库）──
CACHE_DIR = REG_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)
SECURITY_LAST_SCAN = CACHE_DIR / "security_last_scan.json"
DEPENDENCY_CACHE = CACHE_DIR / "dependency_cache.json"

# ── 缓存 TTL ──
CACHE_TTL = {
    "security_full_scan": 7 * 86400,    # 全量扫描：每周一次
    "dependency_check": 24 * 3600,      # 依赖检查：每天一次
}


# ═══════════════════════════════════════════════════════════
# 数据类
# ═══════════════════════════════════════════════════════════

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class ResidentTask:
    """常驻任务定义"""
    task_id: str
    name: str
    description: str
    handler: Callable[[], Dict[str, Any]]
    cron_expr: str                     # cron表达式
    interval_seconds: int = 3600       # 最小执行间隔
    enabled: bool = True
    timeout_seconds: int = 300         # 超时时间
    max_retries: int = 2               # 最大重试次数

    # 运行时状态
    last_run: float = 0.0
    last_status: TaskStatus = TaskStatus.PENDING
    run_count: int = 0
    fail_count: int = 0
    consecutive_fails: int = 0

    def should_run(self) -> bool:
        """检查是否应该执行"""
        if not self.enabled:
            return False
        if self.last_run == 0:
            return True
        return (time.time() - self.last_run) >= self.interval_seconds


@dataclass
class ExecutionRecord:
    """执行记录"""
    task_id: str
    started_at: str
    finished_at: str
    status: TaskStatus
    duration_ms: float
    result: Dict[str, Any] = field(default_factory=dict)
    error: str = ""
    dna: str = ""


# ═══════════════════════════════════════════════════════════
# 常驻工具注册表
# ═══════════════════════════════════════════════════════════

class ResidentFunctionRegistry:
    """
    常驻工具注册表 — 注册→调度→执行→审计。

    用法:
        registry = ResidentFunctionRegistry()
        registry.register_all()
        registry.start()
    """

    def __init__(self, event_bus: Optional[EventBus] = None):
        self.tasks: Dict[str, ResidentTask] = {}
        self._running = False
        self._lock = threading.Lock()
        self._event_bus = event_bus or EventBus()
        self._executor_thread: Optional[threading.Thread] = None

    # ── 注册 ──

    def register(self, task: ResidentTask):
        with self._lock:
            self.tasks[task.task_id] = task
            self._log(f"📋 注册常驻任务: {task.task_id} [{task.cron_expr}] {task.description}")

    def register_all(self):
        """注册所有系统级常驻任务"""
        self.register(ResidentTask(
            task_id="disk_cleanup",
            name="磁盘清理",
            description="清理临时文件、Python缓存、旧日志归档",
            handler=self._disk_cleanup,
            cron_expr="0 2 * * *",
            interval_seconds=86400,
        ))
        self.register(ResidentTask(
            task_id="log_archive",
            name="日志归档",
            description="压缩归档超过7天的日志文件",
            handler=self._log_archive,
            cron_expr="0 * * * *",
            interval_seconds=3600,
        ))
        self.register(ResidentTask(
            task_id="memory_monitor",
            name="内存监控",
            description="记录内存使用趋势，超阈值时告警",
            handler=self._memory_monitor,
            cron_expr="*/30 * * * *",
            interval_seconds=1800,
        ))
        self.register(ResidentTask(
            task_id="git_auto_sync",
            name="Git自动同步",
            description="自动提交本地变更并推送到远程",
            handler=self._git_auto_sync,
            cron_expr="0 */6 * * *",
            interval_seconds=21600,
        ))
        self.register(ResidentTask(
            task_id="security_scan",
            name="安全扫描",
            description="扫描敏感信息泄露（API密钥、密码硬编码等）",
            handler=self._security_scan,
            cron_expr="0 3 * * *",
            interval_seconds=86400,
        ))
        self.register(ResidentTask(
            task_id="health_report",
            name="健康日报",
            description="生成系统健康日报（服务状态/资源/异常）",
            handler=self._health_report,
            cron_expr="0 8 * * *",
            interval_seconds=86400,
        ))
        self.register(ResidentTask(
            task_id="persona_health",
            name="人格健康检查",
            description="检查16人格矩阵健康度",
            handler=self._persona_health_check,
            cron_expr="0 8 * * *",
            interval_seconds=86400,
        ))
        self.register(ResidentTask(
            task_id="dependency_check",
            name="依赖安全检查",
            description="检查Python依赖是否有已知漏洞",
            handler=self._dependency_check,
            cron_expr="0 4 * * *",
            interval_seconds=86400,
        ))
        self._log(f"✅ 已注册 {len(self.tasks)} 个常驻任务")

    # ── 生命周期 ──

    def start(self):
        if self._running:
            return
        self._running = True
        self._executor_thread = threading.Thread(target=self._scheduler_loop, name="resident-scheduler", daemon=True)
        self._executor_thread.start()
        self._log(f"🚀 常驻工具注册表 v{VERSION} 启动")

    def stop(self):
        self._running = False
        if self._executor_thread:
            self._executor_thread.join(timeout=5)
        self._save_state()
        self._log("🛑 常驻工具注册表已停止")

    def run_once(self):
        """执行一次所有到期任务后退出"""
        self._log("⚡ 单次执行模式")
        for task_id, task in self.tasks.items():
            if task.should_run():
                self._execute_task(task)
        self._save_state()

    # ── 调度循环 ──

    def _scheduler_loop(self):
        """调度器主循环 — 每30秒检查一次到期任务"""
        check_interval = 30
        while self._running:
            try:
                for task_id, task in self.tasks.items():
                    if task.should_run():
                        self._execute_task(task)
            except Exception as e:
                self._log(f"❌ 调度器异常: {e}", "error")
            time.sleep(check_interval)

    # ── 任务执行 ──

    def _execute_task(self, task: ResidentTask):
        """执行单个任务（含重试、超时、审计）"""
        task.last_run = time.time()
        task.run_count += 1

        record = ExecutionRecord(
            task_id=task.task_id,
            started_at=datetime.now(timezone.utc).isoformat(),
            finished_at="",
            status=TaskStatus.RUNNING,
            duration_ms=0,
        )

        self._log(f"▶️  执行: {task.name} ({task.task_id})")

        for attempt in range(task.max_retries + 1):
            if attempt > 0:
                self._log(f"  ↻ 重试 {attempt}/{task.max_retries}")

            start = time.time()
            try:
                # 超时控制
                result = {}
                exec_thread = threading.Thread(target=lambda: result.update(task.handler()))
                exec_thread.start()
                exec_thread.join(timeout=task.timeout_seconds)

                if exec_thread.is_alive():
                    raise TimeoutError(f"任务超时 ({task.timeout_seconds}s)")

                duration = (time.time() - start) * 1000
                task.last_status = TaskStatus.SUCCESS
                task.consecutive_fails = 0

                record.status = TaskStatus.SUCCESS
                record.duration_ms = duration
                record.result = result
                record.finished_at = datetime.now(timezone.utc).isoformat()
                record.dna = self._sign_task(task.task_id)

                self._log(f"  ✅ 完成 ({duration:.0f}ms)")
                break

            except Exception as e:
                duration = (time.time() - start) * 1000
                if attempt >= task.max_retries:
                    task.last_status = TaskStatus.FAILED
                    task.fail_count += 1
                    task.consecutive_fails += 1

                    record.status = TaskStatus.FAILED
                    record.duration_ms = duration
                    record.error = str(e)
                    record.finished_at = datetime.now(timezone.utc).isoformat()

                    self._log(f"  ❌ 失败 ({duration:.0f}ms): {e}", "error")

                    # 连续失败3次 → 告警
                    if task.consecutive_fails >= 3:
                        self._alert(f"常驻任务连续失败: {task.name} ({task.task_id}) — {e}")

        # 写审计日志（大结果摘要化，避免日志膨胀）
        self._write_audit(record)

        # 发布到 EventBus（摘要化payload）
        payload = asdict(record)
        for k, v in payload.items():
            if isinstance(v, TaskStatus):
                payload[k] = v.value
        # 裁剪大结果：alert数组只保留摘要
        payload = self._summarize_payload(payload, task.task_id)
        self._event_bus.publish(
            event_type=EventType.EXECUTION_COMPLETED if record.status == TaskStatus.SUCCESS else EventType.EXECUTION_FAILED,
            source=f"ResidentRegistry.{task.task_id}",
            dna_trace=record.dna,
            payload=payload,
        )

    # ═══════════════════════════════════════════════════════
    # 任务实现
    # ═══════════════════════════════════════════════════════

    def _disk_cleanup(self) -> Dict[str, Any]:
        """磁盘清理 — 清理Python缓存、临时文件"""
        cleaned = {"pycache_dirs": 0, "pyc_files": 0, "tmp_files": 0, "freed_mb": 0.0}

        # 清理 __pycache__
        for pycache in PROJECT_ROOT.rglob("__pycache__"):
            try:
                size_before = sum(f.stat().st_size for f in pycache.rglob("*") if f.is_file())
                shutil.rmtree(pycache)
                cleaned["pycache_dirs"] += 1
                cleaned["freed_mb"] += size_before / (1024 * 1024)
            except Exception:
                pass

        # 清理 .pyc 文件
        for pyc in PROJECT_ROOT.rglob("*.pyc"):
            try:
                size = pyc.stat().st_size
                pyc.unlink()
                cleaned["pyc_files"] += 1
                cleaned["freed_mb"] += size / (1024 * 1024)
            except Exception:
                pass

        # 清理超过30天的 .tmp 文件
        cutoff = time.time() - 30 * 86400
        for tmp in PROJECT_ROOT.rglob("*.tmp"):
            try:
                if tmp.stat().st_mtime < cutoff:
                    tmp.unlink()
                    cleaned["tmp_files"] += 1
            except Exception:
                pass

        return cleaned

    def _log_archive(self) -> Dict[str, Any]:
        """日志归档 — 压缩超过7天的日志"""
        result = {"archived_files": 0, "freed_mb": 0.0}
        cutoff = time.time() - 7 * 86400
        log_patterns = ["*.log", "*.jsonl"]

        for pattern in log_patterns:
            for log_file in LOG_DIR.rglob(pattern):
                try:
                    if log_file.stat().st_mtime < cutoff:
                        archive_path = log_file.with_suffix(log_file.suffix + ".gz")
                        if not archive_path.exists():
                            import gzip
                            with open(log_file, 'rb') as f_in:
                                with gzip.open(archive_path, 'wb') as f_out:
                                    shutil.copyfileobj(f_in, f_out)
                            result["archived_files"] += 1
                            result["freed_mb"] += log_file.stat().st_size / (1024 * 1024)
                except Exception:
                    pass
        return result

    def _memory_monitor(self) -> Dict[str, Any]:
        """内存监控"""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        result = {
            "memory_percent": mem.percent,
            "memory_used_gb": round(mem.used / (1024**3), 2),
            "memory_total_gb": round(mem.total / (1024**3), 2),
            "memory_available_gb": round(mem.available / (1024**3), 2),
            "swap_percent": swap.percent,
            "swap_used_gb": round(swap.used / (1024**3), 2),
            "status": "normal",
        }

        if mem.percent > 85:
            result["status"] = "warning"
            self._alert(f"⚠️ 内存使用率 {mem.percent}% — 超过85%阈值")
        elif mem.percent > 95:
            result["status"] = "critical"
            self._alert(f"🚨 内存使用率 {mem.percent}% — 超过95%严重阈值")

        # 持久化内存趋势
        trend_file = REG_DIR / "memory_trend.jsonl"
        with open(trend_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps({
                "ts": datetime.now(timezone.utc).isoformat(),
                **result,
            }) + '\n')

        return result

    def _git_auto_sync(self) -> Dict[str, Any]:
        """Git自动同步 — 检测变更并提交，推送采用最佳努力（快速超时）"""
        result = {"has_changes": False, "committed": False, "pushed": False, "message": ""}

        try:
            os.chdir(PROJECT_ROOT)

            # 检查是否有变更
            status = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True, timeout=10,
            )
            if not status.stdout.strip():
                result["message"] = "无变更"
                return result

            result["has_changes"] = True
            changed_files = len(status.stdout.strip().split("\n"))

            # 添加所有变更
            subprocess.run(["git", "add", "-A"], capture_output=True, timeout=15)

            # 提交
            dna_hash = hashlib.sha256(status.stdout.encode()).hexdigest()[:8]
            commit_msg = (
                f"🤖 龙魂自动同步 {datetime.now().strftime('%m-%d %H:%M')}\n"
                f"DNA: #龍芯⚡️AUTO-SYNC-{dna_hash}"
            )
            commit = subprocess.run(
                ["git", "commit", "-m", commit_msg],
                capture_output=True, text=True, timeout=15,
            )
            result["committed"] = commit.returncode == 0

            # 推送 — 快速超时（10s），远程不可达不阻塞
            push = subprocess.run(
                ["git", "push", "origin", "main"],
                capture_output=True, text=True, timeout=10,
            )
            if push.returncode == 0:
                result["pushed"] = True
                result["message"] = f"已推送 {changed_files} 个文件"
            else:
                # 区分：网络不可达 vs 真正失败
                if "Could not resolve" in push.stderr or "timeout" in push.stderr.lower():
                    result["message"] = f"已本地提交({changed_files}文件)，远程暂不可达"
                else:
                    result["message"] = f"推送失败: {push.stderr[:150]}"

        except subprocess.TimeoutExpired:
            result["message"] = "推送超时，本地已提交"
        except Exception as e:
            result["message"] = str(e)
        finally:
            os.chdir(PROJECT_ROOT)

        return result

    def _security_scan(self) -> Dict[str, Any]:
        """安全扫描 — 增量式扫描，仅检查变更文件（无海量数据库下的最优方案）"""
        result = {
            "scanned_files": 0,
            "findings": 0,
            "alerts": [],
            "mode": "incremental",
        }

        sensitive_patterns = [
            (r'api[_-]?key\s*[=:]\s*["\'][A-Za-z0-9_\-]{20,}["\']', "API密钥硬编码"),
            (r'password\s*[=:]\s*["\'][^"\']+["\']', "密码硬编码"),
            (r'secret\s*[=:]\s*["\'][A-Za-z0-9_\-]{10,}["\']', "Secret硬编码"),
            (r'token\s*[=:]\s*["\'][A-Za-z0-9_\-\.]{20,}["\']', "Token硬编码"),
            (r'-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----', "私钥泄露"),
        ]

        # 编译正则（性能优化）
        compiled_patterns = [(re.compile(p, re.IGNORECASE), desc) for p, desc in sensitive_patterns]

        exclude_dirs = {'.git', '__pycache__', 'venv', '.venv', 'node_modules', 'logs', 'backups'}

        # ── 判断增量 vs 全量 ──
        last_scan_info = self._load_cache(SECURITY_LAST_SCAN)
        do_full_scan = True
        prev_commit = None

        if last_scan_info:
            elapsed = time.time() - last_scan_info.get("timestamp", 0)
            if elapsed < CACHE_TTL["security_full_scan"]:
                do_full_scan = False
                prev_commit = last_scan_info.get("commit")

        # ── 获取要扫描的文件列表 ──
        files_to_scan = []

        if do_full_scan:
            result["mode"] = "full"
            self._log("  🔍 全量扫描模式 (每周例行)")
            try:
                os.chdir(PROJECT_ROOT)
                tracked = subprocess.run(
                    ["git", "ls-files"],
                    capture_output=True, text=True, timeout=15,
                )
                if tracked.returncode == 0:
                    for line in tracked.stdout.strip().split("\n"):
                        if line:
                            fp = PROJECT_ROOT / line
                            if fp.exists() and fp.is_file() and fp.stat().st_size < 5 * 1024 * 1024:
                                if not any(d in fp.parts for d in exclude_dirs):
                                    files_to_scan.append(fp)
                os.chdir(PROJECT_ROOT)
            except Exception:
                os.chdir(PROJECT_ROOT)
                # 回退：只用 git diff
                do_full_scan = False  # 强制降级为增量

        if not do_full_scan or not files_to_scan:
            # 增量模式：只扫描自上次扫描后变更的文件
            result["mode"] = "incremental"
            try:
                os.chdir(PROJECT_ROOT)
                if prev_commit:
                    diff_cmd = ["git", "diff", "--name-only", prev_commit, "HEAD"]
                else:
                    diff_cmd = ["git", "diff", "--name-only", "HEAD~50"]  # 最多50个提交

                diff = subprocess.run(diff_cmd, capture_output=True, text=True, timeout=15)
                if diff.returncode == 0 and diff.stdout.strip():
                    for line in diff.stdout.strip().split("\n"):
                        if line:
                            fp = PROJECT_ROOT / line
                            if fp.exists() and fp.is_file() and fp.stat().st_size < 5 * 1024 * 1024:
                                if not any(d in fp.parts for d in exclude_dirs):
                                    files_to_scan.append(fp)
                os.chdir(PROJECT_ROOT)
            except Exception:
                os.chdir(PROJECT_ROOT)

        if not files_to_scan:
            result["message"] = "无文件需扫描"
            return result

        self._log(f"  📂 扫描 {len(files_to_scan)} 个文件 ({result['mode']}模式)")

        # ── 扫描 ──
        for fpath in files_to_scan:
            result["scanned_files"] += 1
            try:
                content = fpath.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue

            for pattern, desc in compiled_patterns:
                matches = pattern.findall(content)
                if matches:
                    result["findings"] += len(matches)
                    rel_path = fpath.relative_to(PROJECT_ROOT)
                    result["alerts"].append({
                        "file": str(rel_path),
                        "issue": desc,
                        "count": len(matches),
                    })

        # ── 保存扫描状态（轻量缓存）──
        try:
            current_commit = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True, text=True, timeout=5,
                cwd=PROJECT_ROOT
            ).stdout.strip()
            self._save_cache(SECURITY_LAST_SCAN, {
                "timestamp": time.time(),
                "commit": current_commit,
                "files_scanned": len(files_to_scan),
                "mode": result["mode"],
            })
        except Exception:
            pass

        # 告警仅在有真实发现时触发，且只发摘要不内嵌全部结果
        if result["alerts"]:
            self._alert(f"🔐 安全扫描({result['mode']})发现 {result['findings']} 个潜在问题")

        return result

    def _health_report(self) -> Dict[str, Any]:
        """健康日报"""
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        cpu = psutil.cpu_percent(interval=1)

        report = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "system": {
                "platform": platform.platform(),
                "python": sys.version.split()[0],
                "cpu_percent": cpu,
                "memory_percent": mem.percent,
                "memory_used_gb": round(mem.used / (1024**3), 2),
                "disk_percent": disk.percent,
                "disk_free_gb": round(disk.free / (1024**3), 2),
            },
            "longhun": {
                "services": self._check_services(),
                "active_engines": self._count_engines(),
            },
            "overall_status": "healthy",
        }

        # 综合判断
        if mem.percent > 85 or disk.percent > 90:
            report["overall_status"] = "warning"
        if mem.percent > 95 or disk.percent > 95:
            report["overall_status"] = "critical"

        # 保存报告
        report_file = REG_DIR / f"health_{datetime.now().strftime('%Y%m%d')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        return report

    def _persona_health_check(self) -> Dict[str, Any]:
        """人格矩阵健康度检查"""
        personas_dir = PROJECT_ROOT / "personas"
        executors_dir = PROJECT_ROOT / "bin" / "personas"

        result = {
            "persona_files": 0,
            "executor_files": 0,
            "missing_executors": [],
        }

        if personas_dir.exists():
            result["persona_files"] = len(list(personas_dir.glob("*.md")))

        if executors_dir.exists():
            result["executor_files"] = len(list(executors_dir.glob("*.py")))

        return result

    def _dependency_check(self) -> Dict[str, Any]:
        """依赖安全检查 — 缓存优先，减少网络调用"""
        result = {"checked": False, "outdated_packages": 0, "message": "", "cached": False}

        # ── 缓存优先 ──
        cached = self._load_cache(DEPENDENCY_CACHE)
        if cached:
            elapsed = time.time() - cached.get("timestamp", 0)
            if elapsed < CACHE_TTL["dependency_check"]:
                result["checked"] = True
                result["outdated_packages"] = cached.get("outdated_packages", 0)
                result["message"] = cached.get("message", "(缓存)")
                result["cached"] = True
                return result

        # ── 联网检查（带快速超时）──
        try:
            r = subprocess.run(
                [sys.executable, "-m", "pip", "list", "--outdated", "--format=json"],
                capture_output=True, text=True, timeout=30,
            )
            if r.returncode == 0:
                outdated = json.loads(r.stdout)
                result["outdated_packages"] = len(outdated)
                result["checked"] = True
                if outdated:
                    names = [p['name'] for p in outdated[:5]]
                    result["message"] = f"{len(outdated)} 个包可更新: {', '.join(names)}"
                else:
                    result["message"] = "所有包均为最新"
            else:
                result["message"] = f"pip list 失败: {r.stderr[:100]}"
        except subprocess.TimeoutExpired:
            # 超时不阻塞，用缓存兜底
            if cached:
                result["checked"] = True
                result["outdated_packages"] = cached.get("outdated_packages", 0)
                result["message"] = cached.get("message", "(缓存-网络超时)")
                result["cached"] = True
            else:
                result["message"] = "网络超时，无缓存可用"
        except Exception as e:
            result["message"] = str(e)

        # ── 写缓存 ──
        if result["checked"]:
            self._save_cache(DEPENDENCY_CACHE, {
                "timestamp": time.time(),
                "outdated_packages": result["outdated_packages"],
                "message": result["message"],
            })

        return result

    # ── 辅助方法 ──

    def _load_cache(self, cache_file: Path) -> Optional[Dict]:
        """加载轻量级缓存（无数据库方案）"""
        try:
            if cache_file.exists():
                return json.loads(cache_file.read_text())
        except Exception:
            pass
        return None

    def _save_cache(self, cache_file: Path, data: Dict[str, Any]):
        """保存轻量级缓存"""
        try:
            cache_file.write_text(json.dumps(data, ensure_ascii=False))
        except Exception:
            pass

    def _summarize_payload(self, payload: Dict[str, Any], _task_id: str = "") -> Dict[str, Any]:
        """摘要化负载：裁剪大数组，避免日志膨胀"""
        p = dict(payload)
        result = p.get("result", {})
        if isinstance(result, dict):
            alerts = result.get("alerts", [])
            if isinstance(alerts, list) and len(alerts) > 5:
                # 大结果：只保留前5条+总数
                result["alerts_summary"] = f"{len(alerts)}条告警（已裁剪，完整结果见审计日志）"
                result["alerts_top5"] = alerts[:5]
                del result["alerts"]
            p["result"] = result
        return p

    def _check_services(self) -> Dict[str, str]:
        """检查龙魂服务状态"""
        services = {}
        svc_names = ["longhun-api", "longhun-portal", "longhun-dashboard", "longhun-core"]
        for svc in svc_names:
            try:
                r = subprocess.run(
                    ["systemctl", "is-active", svc],
                    capture_output=True, text=True, timeout=10,
                )
                services[svc] = r.stdout.strip()
            except Exception:
                services[svc] = "unknown"
        return services

    def _count_engines(self) -> int:
        """统计活跃引擎数"""
        bin_dir = PROJECT_ROOT / "bin"
        if bin_dir.exists():
            return len(list(bin_dir.glob("lh_*.py")))
        return 0

    def _write_audit(self, record: ExecutionRecord):
        """写审计日志（大结果摘要化）"""
        d = asdict(record)
        # 枚举→字符串
        for k, v in d.items():
            if isinstance(v, TaskStatus):
                d[k] = v.value
        # 裁剪大结果
        d = self._summarize_payload(d, record.task_id)
        with open(AUDIT_LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(d, ensure_ascii=False, default=str) + '\n')

    def _sign_task(self, task_id: str) -> str:
        payload = f"{task_id}-{time.time()}"
        return f"#龍芯⚡️TASK-{hashlib.sha256(payload.encode()).hexdigest()[:12]}"

    def _alert(self, msg: str):
        """发送告警"""
        self._log(f"🚨 {msg}", "warn")
        # TODO: 对接 Bark推送
        alert_file = REG_DIR / "alerts.jsonl"
        with open(alert_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps({
                "ts": datetime.now(timezone.utc).isoformat(),
                "message": msg,
            }) + '\n')

    def _save_state(self):
        """保存任务状态"""
        state = {
            "saved_at": datetime.now(timezone.utc).isoformat(),
            "tasks": {
                tid: {
                    "last_run": t.last_run,
                    "last_status": t.last_status.value,
                    "run_count": t.run_count,
                    "fail_count": t.fail_count,
                    "consecutive_fails": t.consecutive_fails,
                } for tid, t in self.tasks.items()
            },
        }
        with open(TASK_STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def load_state(self):
        """加载任务状态"""
        if not TASK_STATE_FILE.exists():
            return
        with open(TASK_STATE_FILE, 'r', encoding='utf-8') as f:
            state = json.load(f)
        for tid, tstate in state.get("tasks", {}).items():
            if tid in self.tasks:
                self.tasks[tid].last_run = tstate.get("last_run", 0)
                self.tasks[tid].run_count = tstate.get("run_count", 0)
                self.tasks[tid].fail_count = tstate.get("fail_count", 0)
                self.tasks[tid].consecutive_fails = tstate.get("consecutive_fails", 0)

    def _log(self, msg: str, level: str = "info"):
        prefix = {"debug": "🔍", "info": "  ", "warn": "⚠️", "error": "❌"}.get(level, "  ")
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[resident {ts}] {prefix} {msg}")

    def get_status(self) -> Dict[str, Any]:
        """获取注册表状态"""
        return {
            "running": self._running,
            "version": VERSION,
            "dna": DNA,
            "tasks_count": len(self.tasks),
            "active_tasks": sum(1 for t in self.tasks.values() if t.enabled),
            "tasks": {
                tid: {
                    "name": t.name,
                    "enabled": t.enabled,
                    "cron": t.cron_expr,
                    "last_run": datetime.fromtimestamp(t.last_run).isoformat() if t.last_run else None,
                    "last_status": t.last_status.value,
                    "run_count": t.run_count,
                    "fail_count": t.fail_count,
                } for tid, t in self.tasks.items()
            },
        }


# ═══════════════════════════════════════════════════════════
# 单例入口
# ═══════════════════════════════════════════════════════════

_registry_instance: Optional[ResidentFunctionRegistry] = None


def get_resident_registry() -> ResidentFunctionRegistry:
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = ResidentFunctionRegistry()
    return _registry_instance


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂 · 常驻工具注册表 v2.0")
    parser.add_argument("--daemon", action="store_true", help="后台守护模式运行")
    parser.add_argument("--once", action="store_true", help="执行一次所有到期任务后退出")
    parser.add_argument("--status", action="store_true", help="查看注册表状态")
    parser.add_argument("--run", type=str, help="手动执行指定任务ID")
    parser.add_argument("--list", action="store_true", help="列出所有注册任务")
    args = parser.parse_args()

    registry = get_resident_registry()
    registry.register_all()
    registry.load_state()

    if args.status:
        print(json.dumps(registry.get_status(), ensure_ascii=False, indent=2))
        return

    if args.list:
        for tid, t in registry.tasks.items():
            icon = "🟢" if t.enabled else "🔴"
            print(f"{icon} {tid:22s} [{t.cron_expr:14s}] {t.name:10s} | {t.description}")
        return

    if args.run:
        task = registry.tasks.get(args.run)
        if task:
            registry._execute_task(task)
        else:
            print(f"❌ 任务不存在: {args.run}")
            print(f"可用: {', '.join(registry.tasks.keys())}")
        return

    if args.once:
        registry.run_once()
        return

    # 守护模式
    registry.start()
    try:
        while registry._running:
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n⏹️  收到中断信号")
    finally:
        registry.stop()


if __name__ == "__main__":
    main()
