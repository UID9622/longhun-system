#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂智能体 · L1 常驻五大人格守护进程
Resident Agent Daemon: 雯雯 / 侦察兵 / 上帝之眼 / 宝宝 / 文心

特性：
- 单进程多线程，5 个人格各跑一个守护循环
- 只做本地扫描/计数/轻量执行，不依赖外部平台
- 输出状态文件与心跳，供状态上报与三才审计使用

DNA: #龍芯⚡️2026-06-26-LONGHUN-AGENT-DAEMON-v1.0
"""

import argparse
import datetime
import fnmatch
import hashlib
import json
import os
import re
import signal
import subprocess
import sys
import threading
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# ============================================================
# 常量
# ============================================================
DNA = "#龍芯⚡️2026-06-26-LONGHUN-AGENT-DAEMON-v1.0"
VERSION = "1.0.0"
AGENT_HOME = Path.home() / "longhun-system" / "agents"
LOG_DIR = AGENT_HOME / "daemon_logs"
QUEUE_DIR = AGENT_HOME / "queues"
PID_FILE = AGENT_HOME / "daemon.pid"
STATE_FILE = AGENT_HOME / "daemon_state.json"
HEARTBEAT_FILE = LOG_DIR / "heartbeat.json"

WATCH_DIRS = [
    Path.home() / "longhun-system",
    Path.home() / ".kimi-code" / "sessions",
    Path.home() / ".longhun" / "memory",
    Path.home() / "_work",
]

SENSITIVE_PATTERNS = [
    r"password\s*[=:]\s*\S+",
    r"api[_-]?key\s*[=:]\s*\S+",
    r"secret\s*[=:]\s*\S+",
    r"token\s*[=:]\s*\S+",
    r"private[_-]?key",
    r"-----BEGIN .* PRIVATE KEY-----",
]
SENSITIVE_NAME_PATTERNS = ["*.env*", "*credentials*", "*secret*", "*password*", "*token*", "*private*"]

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(QUEUE_DIR, exist_ok=True)


# ============================================================
# 工具函数
# ============================================================
def now_iso() -> str:
    return datetime.datetime.now().isoformat()


def write_json(path: Path, data: Any):
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp.replace(path)


def read_json(path: Path, default=None) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default if default is not None else {}


def safe_list_files(root: Path, since_sec: float, max_files: int = 10000) -> List[Path]:
    """递归列出 root 下在 since_sec 内修改的文件，受 max_files 限制。"""
    results = []
    cutoff = time.time() - since_sec
    if not root.exists():
        return results
    try:
        for dirpath, dirnames, filenames in os.walk(root):
            # 跳过巨大/临时目录
            dirnames[:] = [d for d in dirnames if d not in {"node_modules", ".git", "__pycache__", ".venv", "venv"}]
            for fn in filenames:
                if len(results) >= max_files:
                    return results
                p = Path(dirpath) / fn
                try:
                    if p.stat().st_mtime >= cutoff:
                        results.append(p)
                except Exception:
                    continue
    except Exception:
        pass
    return results


# ============================================================
# 人格基类
# ============================================================
class ResidentAgent(ABC):
    def __init__(self, agent_id: str, name: str, interval_sec: int):
        self.agent_id = agent_id
        self.name = name
        self.interval_sec = interval_sec
        self.state = "idle"  # idle / running / error / stopped
        self.last_run = None
        self.last_error = ""
        self.counters: Dict[str, int] = {}
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self.log_path = LOG_DIR / f"{agent_id}.json"

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._loop, name=f"Agent-{self.agent_id}", daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self.state = "stopped"

    def _loop(self):
        # 首次启动错开 0-5 秒，避免所有线程同时刷盘
        time.sleep(hash(self.agent_id) % 5)
        while not self._stop_event.is_set():
            self.state = "running"
            self.last_run = now_iso()
            try:
                self.tick()
                self.last_error = ""
            except Exception as e:
                self.state = "error"
                self.last_error = str(e)
            self.state = "idle"
            self._flush_status()
            # 分步睡眠，便于快速响应 stop
            for _ in range(self.interval_sec):
                if self._stop_event.is_set():
                    break
                time.sleep(1)

    @abstractmethod
    def tick(self):
        pass

    def _flush_status(self):
        data = {
            "agent_id": self.agent_id,
            "name": self.name,
            "state": self.state,
            "last_run": self.last_run,
            "last_error": self.last_error,
            "counters": self.counters,
            "updated_at": now_iso(),
            "dna": DNA,
        }
        write_json(self.log_path, data)


# ============================================================
# 五大人格实现
# ============================================================
class WenwenAgent(ResidentAgent):
    """雯雯：整理逻辑 —— 扫描新增/变动文件，生成本地整理摘要。"""

    def __init__(self):
        super().__init__("wenwen", "雯雯", 3600)  # 每小时

    def tick(self):
        total = 0
        by_ext: Dict[str, int] = {}
        recent_files: List[str] = []
        for d in WATCH_DIRS:
            files = safe_list_files(d, since_sec=3600, max_files=5000)
            total += len(files)
            for p in files:
                ext = p.suffix.lower() or "(no_ext)"
                by_ext[ext] = by_ext.get(ext, 0) + 1
                recent_files.append(str(p.relative_to(Path.home())))
        self.counters["scanned_files_hour"] = total
        self.counters["distinct_exts"] = len(by_ext)
        summary = {
            "timestamp": now_iso(),
            "total_new_or_modified_hour": total,
            "by_extension": by_ext,
            "sample_files": recent_files[:20],
        }
        write_json(LOG_DIR / "wenwen_summary.json", summary)


class ScoutAgent(ResidentAgent):
    """侦察兵：搜索逻辑 —— 监听本地情报源，发现新鲜事。"""

    def __init__(self):
        super().__init__("scout", "侦察兵", 600)  # 每 10 分钟

    def tick(self):
        # 1) 最近 10 分钟有变动的文件
        hot = []
        for d in WATCH_DIRS:
            hot += safe_list_files(d, since_sec=600, max_files=2000)
        # 2) 读取 longhun 记忆摘要，统计关键事件
        digest_path = Path.home() / ".longhun" / "memory" / "latest_digest.md"
        key_events = 0
        if digest_path.exists():
            try:
                text = digest_path.read_text(encoding="utf-8", errors="ignore")
                key_events = text.count("**最近关键事件：**") + text.count("- ")
            except Exception:
                pass
        self.counters["hot_files_10min"] = len(hot)
        self.counters["memory_key_events"] = key_events
        write_json(LOG_DIR / "scout_intel.json", {
            "timestamp": now_iso(),
            "hot_files_count": len(hot),
            "hot_files_sample": [str(p.relative_to(Path.home())) for p in hot[:10]],
            "memory_digest_events": key_events,
        })


class GuardianAgent(ResidentAgent):
    """上帝之眼：守护逻辑 —— 敏感文件/内容扫描，只计数不泄露值。"""

    def __init__(self):
        super().__init__("guardian", "上帝之眼", 1800)  # 每 30 分钟

    def tick(self):
        sensitive_files = []
        suspicious_lines = 0
        regex = re.compile("|".join(SENSITIVE_PATTERNS), re.IGNORECASE)
        SKIP_DIRS = {"node_modules", ".git", "__pycache__", ".venv", "venv", "site-packages"}
        for d in WATCH_DIRS:
            if not d.exists():
                continue
            for dirpath, dirnames, filenames in os.walk(d):
                dirnames[:] = [x for x in dirnames if x not in SKIP_DIRS]
                for fn in filenames:
                    p = Path(dirpath) / fn
                    # 跳过过大文件
                    try:
                        if p.stat().st_size > 50 * 1024:
                            continue
                    except Exception:
                        continue
                    rel = str(p.relative_to(Path.home()))
                    # 敏感文件名
                    if any(fnmatch.fnmatch(fn.lower(), pat) for pat in SENSITIVE_NAME_PATTERNS):
                        sensitive_files.append(rel)
                        continue
                    # 敏感内容（仅前 2KB）
                    try:
                        data = p.read_bytes()[:2048]
                        text = data.decode("utf-8", errors="ignore")
                        if regex.search(text):
                            suspicious_lines += text.count("\n") + 1
                            sensitive_files.append(rel)
                    except Exception:
                        continue
        self.counters["sensitive_files"] = len(sensitive_files)
        self.counters["suspicious_content_snippets"] = suspicious_lines
        audit_color = "🟢" if len(sensitive_files) == 0 else "🟡" if len(sensitive_files) < 50 else "🔴"
        write_json(LOG_DIR / "guardian_audit.json", {
            "timestamp": now_iso(),
            "sensitive_file_count": len(sensitive_files),
            "suspicious_snippet_count": suspicious_lines,
            "audit_color": audit_color,
            "sensitive_files_sample": sensitive_files[:20],  # 仅路径，不含内容
        })


class BuilderAgent(ResidentAgent):
    """宝宝：构建逻辑 —— 消费 builder_tasks.jsonl 队列，完成轻量构建任务。"""

    def __init__(self):
        super().__init__("builder", "宝宝", 300)  # 每 5 分钟
        self.queue_path = QUEUE_DIR / "builder_tasks.jsonl"

    def tick(self):
        processed = 0
        failed = 0
        if self.queue_path.exists():
            lines = []
            try:
                with open(self.queue_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
            except Exception:
                pass
            remaining = []
            for line in lines:
                try:
                    task = json.loads(line)
                except Exception:
                    continue
                status = task.get("status", "pending")
                if status != "pending":
                    remaining.append(line)
                    continue
                ok = self._execute(task)
                if ok:
                    task["status"] = "done"
                    task["done_at"] = now_iso()
                    processed += 1
                else:
                    task["status"] = "failed"
                    failed += 1
                remaining.append(json.dumps(task, ensure_ascii=False) + "\n")
            with open(self.queue_path, "w", encoding="utf-8") as f:
                f.writelines(remaining)
        self.counters["processed_tasks"] = self.counters.get("processed_tasks", 0) + processed
        self.counters["failed_tasks"] = self.counters.get("failed_tasks", 0) + failed
        write_json(LOG_DIR / "builder_status.json", {
            "timestamp": now_iso(),
            "processed_this_tick": processed,
            "failed_this_tick": failed,
            "queue_file": str(self.queue_path.relative_to(Path.home())),
        })

    def _execute(self, task: Dict[str, Any]) -> bool:
        ttype = task.get("type", "")
        try:
            if ttype == "create_dir":
                Path(task["path"]).expanduser().mkdir(parents=True, exist_ok=True)
                return True
            elif ttype == "create_file":
                p = Path(task["path"]).expanduser()
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(task.get("content", ""), encoding="utf-8")
                return True
            elif ttype == "append_file":
                p = Path(task["path"]).expanduser()
                p.parent.mkdir(parents=True, exist_ok=True)
                with open(p, "a", encoding="utf-8") as f:
                    f.write(task.get("content", ""))
                return True
            else:
                return False
        except Exception as e:
            task["error"] = str(e)
            return False


class SyncerAgent(ResidentAgent):
    """文心：同步逻辑 —— 检查 Git 状态、汇总各人格心跳为系统心跳。"""

    def __init__(self):
        super().__init__("syncer", "文心", 300)  # 每 5 分钟

    def tick(self):
        git_changes = 0
        git_root = Path.home() / "longhun-system"
        if (git_root / ".git").exists():
            try:
                out = subprocess.check_output(
                    ["git", "-C", str(git_root), "status", "--short"],
                    stderr=subprocess.DEVNULL,
                    text=True,
                )
                git_changes = len([l for l in out.splitlines() if l.strip()])
            except Exception:
                pass
        self.counters["git_uncommitted_changes"] = git_changes
        # 汇总心跳
        agents_status = []
        for aid in ["wenwen", "scout", "guardian", "builder", "syncer"]:
            st = read_json(LOG_DIR / f"{aid}.json", {})
            agents_status.append({
                "id": aid,
                "name": st.get("name", aid),
                "state": st.get("state", "unknown"),
                "last_run": st.get("last_run"),
                "counters": st.get("counters", {}),
            })
        heartbeat = {
            "timestamp": now_iso(),
            "daemon_version": VERSION,
            "daemon_dna": DNA,
            "pid": os.getpid(),
            "agents": agents_status,
            "git_uncommitted_changes": git_changes,
        }
        write_json(HEARTBEAT_FILE, heartbeat)


# ============================================================
# 守护进程管理
# ============================================================
AGENT_CLASSES = [WenwenAgent, ScoutAgent, GuardianAgent, BuilderAgent, SyncerAgent]


def _write_state(pid: int, running: bool):
    write_json(STATE_FILE, {
        "pid": pid,
        "running": running,
        "started_at": now_iso(),
        "version": VERSION,
        "dna": DNA,
    })


def _read_pid() -> Optional[int]:
    try:
        data = read_json(STATE_FILE, {})
        pid = data.get("pid")
        if pid and isinstance(pid, int):
            return pid
    except Exception:
        pass
    if PID_FILE.exists():
        try:
            return int(PID_FILE.read_text().strip())
        except Exception:
            pass
    return None


def _is_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except Exception:
        return False


def run_daemon_once():
    """只跑一轮，用于测试。"""
    agents = [cls() for cls in AGENT_CLASSES]
    for a in agents:
        a.tick()
        a._flush_status()
    print("✅ 五大人格各执行一轮")


def run_daemon():
    """真正进入守护循环。"""
    # 信号处理
    def on_sigterm(signum, frame):
        for a in agents:
            a.stop()
        sys.exit(0)

    signal.signal(signal.SIGTERM, on_sigterm)
    signal.signal(signal.SIGINT, on_sigterm)

    agents = [cls() for cls in AGENT_CLASSES]
    _write_state(os.getpid(), True)
    PID_FILE.write_text(str(os.getpid()), encoding="utf-8")

    for a in agents:
        a.start()

    # 主线程保持存活
    while True:
        time.sleep(10)
        # 如果某个线程挂掉（理论上不会），可在这里重启
        for a in agents:
            if not a._thread or not a._thread.is_alive():
                a.start()


def start_daemon():
    # 如果已在运行，直接返回
    pid = _read_pid()
    if pid and _is_alive(pid):
        print(f"守护进程已在运行，PID={pid}")
        return
    # 用 subprocess 启动后台进程
    cmd = [sys.executable, __file__, "run-background"]
    proc = subprocess.Popen(
        cmd,
        stdout=open(LOG_DIR / "daemon.stdout.log", "a"),
        stderr=open(LOG_DIR / "daemon.stderr.log", "a"),
        start_new_session=True,
    )
    # 给一点时间写入 pid
    time.sleep(0.5)
    print(f"🟢 L1 守护进程已启动，PID={proc.pid}")


def stop_daemon():
    pid = _read_pid()
    if not pid:
        print("未找到守护进程 PID")
        return
    if not _is_alive(pid):
        print(f"PID={pid} 已不存在，清理状态文件")
        _write_state(pid, False)
        return
    try:
        os.kill(pid, signal.SIGTERM)
        # 等待进程退出
        for _ in range(20):
            if not _is_alive(pid):
                break
            time.sleep(0.2)
        print(f"🔴 守护进程 PID={pid} 已停止")
    except Exception as e:
        print(f"停止失败: {e}")
    finally:
        _write_state(pid, False)


def status_daemon():
    pid = _read_pid()
    alive = bool(pid and _is_alive(pid))
    state = read_json(STATE_FILE, {})
    print(f"守护进程状态: {'🟢 运行中' if alive else '🔴 未运行'}")
    if pid:
        print(f"PID: {pid}")
    print(f"启动时间: {state.get('started_at', 'N/A')}")
    print(f"版本: {state.get('version', VERSION)}")
    print("人格状态:")
    for aid in ["wenwen", "scout", "guardian", "builder", "syncer"]:
        st = read_json(LOG_DIR / f"{aid}.json", {})
        print(f"  - {aid:10s} {st.get('name', aid):8s} [{st.get('state', 'unknown')}] last={st.get('last_run')}")


def main():
    parser = argparse.ArgumentParser(description="龍魂 L1 常驻五大人格守护进程")
    parser.add_argument("command", choices=["start", "stop", "status", "once", "run-background"])
    args = parser.parse_args()

    if args.command == "start":
        start_daemon()
    elif args.command == "stop":
        stop_daemon()
    elif args.command == "status":
        status_daemon()
    elif args.command == "once":
        run_daemon_once()
    elif args.command == "run-background":
        run_daemon()


if __name__ == "__main__":
    main()
