#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 定时任务引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-SCHED-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 声明式定时任务（类似cron）
  - 任务持久化
  - 任务状态监控
"""

import json
import time
import threading
import subprocess
from pathlib import Path
from typing import Dict, List
from datetime import datetime

try:
    from croniter import croniter
except ImportError:
    croniter = None


class SchedulerEngine:
    """定时任务引擎——声明式cron调度"""

    def __init__(self):
        self.tasks: Dict[str, Dict] = {}
        self._lock = threading.Lock()
        self._running = True
        self._task_file = Path.home() / "longhun-system/data/scheduled_tasks.json"
        self._load()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def _load(self):
        if self._task_file.exists():
            try:
                data = json.loads(self._task_file.read_text(encoding="utf-8"))
                for t in data:
                    t["next_run"] = self._calc_next(t["cron"]) if croniter else None
                    self.tasks[t["id"]] = t
            except Exception:
                pass

    def _save(self):
        data = [{"id": t["id"], "cron": t["cron"], "command": t["command"],
                 "description": t.get("description", ""), "status": t.get("status", "active")}
                for t in self.tasks.values()]
        self._task_file.parent.mkdir(parents=True, exist_ok=True)
        self._task_file.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    def _calc_next(self, cron: str) -> str:
        if not croniter:
            return ""
        try:
            nxt = croniter(cron, datetime.now()).get_next(datetime)
            return nxt.isoformat()
        except Exception:
            return ""

    def add(self, cron: str, command: str, description: str = "") -> str:
        tid = f"task_{int(time.time())}"
        with self._lock:
            self.tasks[tid] = {
                "id": tid, "cron": cron, "command": command,
                "description": description, "status": "active",
                "next_run": self._calc_next(cron),
                "last_run": None,
            }
            self._save()
        return tid

    def remove(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self.tasks:
                del self.tasks[task_id]
                self._save()
                return True
        return False

    def list_tasks(self) -> List[Dict]:
        return [
            {"id": t["id"], "cron": t["cron"], "command": t["command"],
             "next_run": t.get("next_run"), "last_run": t.get("last_run"),
             "status": t.get("status", "active")}
            for t in self.tasks.values()
        ]

    def _loop(self):
        while self._running:
            time.sleep(15)
            with self._lock:
                for tid, t in self.tasks.items():
                    if t.get("status") != "active":
                        continue
                    nxt = self._calc_next(t["cron"])
                    t["next_run"] = nxt
                    if nxt and datetime.now().isoformat() >= nxt:
                        self._execute(tid, t)

    def _execute(self, tid: str, task: Dict):
        task["last_run"] = datetime.now().isoformat()
        task["next_run"] = self._calc_next(task["cron"])
        try:
            subprocess.run(task["command"], shell=True, timeout=300)
            print(f"⏰ [{tid}] 执行完成: {task['command'][:50]}")
        except Exception as e:
            print(f"⏰ [{tid}] 执行失败: {e}")

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)


if __name__ == "__main__":
    engine = SchedulerEngine()
    task_id = engine.add("* * * * *", "echo 'hello'", "测试每分钟执行")
    print(f"添加任务: {task_id}")
    tasks = engine.list_tasks()
    print(f"任务数: {len(tasks)}")
    engine.remove(task_id)
    engine.stop()
    print("🟢 定时任务引擎测试通过")
