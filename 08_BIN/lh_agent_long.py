#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丁未·癸巳·巳时·䷾既济-AGENT-LONG-TASK-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 协议: CC BY-NC-SA 4.0（核心思想层）
# -*- coding: utf-8 -*-
"""
龍魂 · 长期无人值守任务引擎 v1.0 · Long-Running Task Engine

对齐「长期自主智能体」能力（2026-09-03 · 裁决采纳 B 项）:
  - 任务队列持久化 ~/.longhun/agent/queue.json（kill 不丢）
  - 前台 run 阻塞执行 + 自动重试（默认最多 3 次）
  - 状态日志 ~/.longhun/agent/logs/<task_id>.log（append-only）
  - launchd 周期 recover：进程被杀 → 自动续跑/重试（断点续跑）
  - root-cause：规则式失败根因分析（exit_code/stderr/超时/重试耗尽）

命令:
  python3 lh_agent_long.py run "<描述>" --cmd "<命令>" [--max-hours 38] [--max-retries 3]
  python3 lh_agent_long.py status [--json] [--all]
  python3 lh_agent_long.py root-cause <task_id> [--json]
  python3 lh_agent_long.py recover [--json]            # launchd 周期调用
  python3 lh_agent_long.py cancel <task_id>
  python3 lh_agent_long.py test                        # 自测
"""
from __future__ import annotations

import argparse
import json
import os
import shlex
import signal
import subprocess
import sys
import time
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent          # longhun-system
AGENT_DIR = Path.home() / ".longhun" / "agent"
QUEUE_FILE = AGENT_DIR / "queue.json"
LOG_DIR = AGENT_DIR / "logs"
MAX_RETRIES_DEFAULT = 3
MAX_HOURS_DEFAULT = 38

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def load_queue() -> Dict[str, Any]:
    if QUEUE_FILE.exists():
        try:
            return json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"next_id": 1, "tasks": []}


def save_queue(q: Dict[str, Any]) -> None:
    AGENT_DIR.mkdir(parents=True, exist_ok=True)
    QUEUE_FILE.write_text(json.dumps(q, ensure_ascii=False, indent=2), encoding="utf-8")


def find_task(q: Dict[str, Any], task_id: int) -> Optional[Dict[str, Any]]:
    for t in q["tasks"]:
        if t["id"] == task_id:
            return t
    return None


def append_task_log(task: Dict[str, Any], line: str) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_DIR / f"{task['id']}.log", "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {line}\n")


def _task_output(task: Dict[str, Any]) -> str:
    fp = LOG_DIR / f"{task['id']}.log"
    if fp.exists():
        return fp.read_text(encoding="utf-8", errors="replace")
    return ""


def _update_task(q: Dict[str, Any], task: Dict[str, Any]) -> None:
    for i, t in enumerate(q["tasks"]):
        if t["id"] == task["id"]:
            q["tasks"][i] = task
            break
    save_queue(q)


def cmd_run(desc: str, command: Optional[str], max_hours: float, max_retries: int) -> int:
    """入队并前台执行一个长期任务（含自动重试）。无 --cmd 且非 --manual 则拒绝。"""
    q = load_queue()
    task_id = q["next_id"]
    q["next_id"] = task_id + 1
    task: Dict[str, Any] = {
        "id": task_id,
        "desc": desc,
        "command": command,
        "status": "pending",          # pending/running/success/failed/canceled
        "retries": 0,
        "max_retries": max_retries,
        "max_hours": max_hours,
        "pid": None,
        "exit_code": None,
        "last_error": "",
        "created_at": now_iso(),
        "started_at": None,
        "finished_at": None,
    }
    q["tasks"].append(task)
    save_queue(q)
    append_task_log(task, f"入队: {desc} | cmd={command} | max_hours={max_hours} | retries={max_retries}")
    return _execute_task(task_id, q)


def _execute_task(task_id: int, q: Optional[Dict[str, Any]] = None) -> int:
    """前台执行已入队任务（含自动重试）。cmd_run 与 _resume_run/recover 共用。"""
    if q is None:
        q = load_queue()
    task = find_task(q, task_id)
    if not task:
        print(f"❌ 任务 {task_id} 不存在")
        return 1
    if not task.get("command"):
        task["status"] = "failed"
        task["last_error"] = "no_command: 无执行体"
        task["finished_at"] = now_iso()
        _update_task(q, task)
        return 1

    max_retries = task["max_retries"]
    max_hours = task["max_hours"]
    task["status"] = "running"
    task["started_at"] = now_iso()
    task["pid"] = os.getpid()
    _update_task(q, task)

    deadline = time.monotonic() + max_hours * 3600
    while True:
        append_task_log(task, f"=== attempt {task['retries'] + 1}/{max_retries + 1} 开始 ===")
        try:
            proc = subprocess.Popen(
                shlex.split(task["command"]),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                start_new_session=True,
            )
            # 记录真实子进程 pid（供 recover 检测存活）
            task["pid"] = proc.pid
            _update_task(q, task)

            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError(f"总时长超限({max_hours}h)")
            try:
                out, _ = proc.communicate(timeout=max(1.0, remaining))
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(proc.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                append_task_log(task, f"[timeout] 超过 {max_hours}h 限额，已终止 pid={proc.pid}")
                task["status"] = "failed"
                task["last_error"] = f"timeout_after_{max_hours}h"
                task["finished_at"] = now_iso()
                task["pid"] = None
                _update_task(q, task)
                print(json.dumps({"id": task["id"], "status": "failed",
                                  "error": task["last_error"]}, ensure_ascii=False))
                return 1
            append_task_log(task, f"exit_code={proc.returncode}")
            if out:
                for ln in out.splitlines()[-40:]:
                    append_task_log(task, f"  | {ln}")
            if proc.returncode == 0:
                task["status"] = "success"
                task["finished_at"] = now_iso()
                task["pid"] = None
                _update_task(q, task)
                print(json.dumps({"id": task["id"], "status": "success",
                                  "attempts": task["retries"] + 1}, ensure_ascii=False))
                return 0
            rc = proc.returncode
        except TimeoutError as e:
            append_task_log(task, str(e))
            task["status"] = "failed"
            task["last_error"] = str(e)
            task["finished_at"] = now_iso()
            task["pid"] = None
            _update_task(q, task)
            print(json.dumps({"id": task["id"], "status": "failed", "error": str(e)},
                             ensure_ascii=False))
            return 1
        except Exception as e:  # 命令无法启动等
            append_task_log(task, f"[error] {e!r}")
            rc = -1
            task["last_error"] = repr(e)

        # rc != 0 → 重试
        if task["retries"] < max_retries:
            task["retries"] += 1
            task["status"] = "pending"   # 短暂释放，立即重试
            _update_task(q, task)
            append_task_log(task, f"失败 rc={rc}，第 {task['retries']}/{max_retries} 次重试，2s 后拉起")
            time.sleep(2)
            task["status"] = "running"
            task["started_at"] = now_iso()
            _update_task(q, task)
        else:
            task["status"] = "failed"
            task["last_error"] = f"exit_code={rc}·重试{max_retries}次耗尽"
            task["finished_at"] = now_iso()
            task["pid"] = None
            _update_task(q, task)
            print(json.dumps({"id": task["id"], "status": "failed",
                              "error": task["last_error"]}, ensure_ascii=False))
            return 1


def cmd_status(show_all: bool = False, as_json: bool = False) -> int:
    q = load_queue()
    tasks = q["tasks"]
    if not show_all:
        # 默认只展示未完成 + 最近 5 条已完成
        active = [t for t in tasks if t["status"] in ("pending", "running")]
        recent = [t for t in tasks if t["status"] not in ("pending", "running")][-5:]
        shown = active + recent
    else:
        shown = tasks
    payload = {"tasks": shown, "active_count": len([t for t in tasks if t["status"] in ("pending", "running")])}
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    print(f"\n  🐉 长期任务队列 · {len(tasks)} 条 · 活跃 {payload['active_count']}\n")
    if not shown:
        print("  （空队列）")
        return 0
    print(f"  {'ID':<5}{'状态':<10}{'重试':<7}{'运行时长':<12}描述")
    for t in reversed(shown):
        dur = ""
        if t.get("started_at"):
            try:
                s = datetime.fromisoformat(t["started_at"])
                e = datetime.fromisoformat(t.get("finished_at") or now_iso())
                dur = f"{max(0, (e - s).total_seconds()):.0f}s"
            except Exception:
                dur = "-"
        desc = (t["desc"] or "")[:46]
        print(f"  {t['id']:<5}{t['status']:<10}{str(t['retries']) + '/' + str(t['max_retries']):<7}{dur:<12}{desc}")
    return 0


def cmd_root_cause(task_id: int, as_json: bool = False) -> int:
    q = load_queue()
    task = find_task(q, task_id)
    if not task:
        print(f"❌ 任务 {task_id} 不存在")
        return 1
    causes: List[str] = []
    evidence: Dict[str, Any] = {}
    if task["status"] == "failed":
        err = task.get("last_error", "")
        if err.startswith("timeout"):
            causes.append("超时终止: 超出 --max-hours 限额，进程被 SIGTERM")
        elif "exit_code=" in err:
            try:
                rc = int(err.split("exit_code=")[1].split("·")[0])
                causes.append(f"命令退出码 {rc}（非零）: 业务执行失败")
            except Exception:
                causes.append(f"命令退出码非零: {err}")
        else:
            causes.append(f"异常: {err}")
        if task["retries"] >= task["max_retries"] and task["retries"] > 0:
            causes.append(f"自动重试 {task['max_retries']} 次全部失败（重试策略已耗尽）")
    elif task["status"] == "canceled":
        causes.append("已被人工 cancel")
    elif task["status"] == "running":
        causes.append("仍在运行（非失败状态）")
    else:
        causes.append(f"任务状态={task['status']}，无失败根因")
    tail = _task_output(task).strip().splitlines()[-10:]
    evidence = {
        "exit_code": task.get("exit_code"),
        "retries": task.get("retries"),
        "last_error": task.get("last_error"),
        "stderr_tail": tail,
    }
    if as_json:
        print(json.dumps({"id": task_id, "causes": causes, "evidence": evidence},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"\n  🐉 任务 {task_id} 根因分析")
    print(f"  描述: {task.get('desc')}")
    print(f"  状态: {task['status']} · 重试 {task.get('retries')}/{task.get('max_retries')}")
    print(f"  命令: {task.get('command')}")
    print(f"  根因: {causes[0] if causes else '未知'}")
    if task.get("retries") == task.get("max_retries") and task["status"] == "failed":
        print("  建议: 命令本身有缺陷或环境依赖缺失，先人工修正命令再重跑（lh agent run ...）")
    return 0


def cmd_cancel(task_id: int) -> int:
    q = load_queue()
    task = find_task(q, task_id)
    if not task:
        print(f"❌ 任务 {task_id} 不存在")
        return 1
    if task["status"] == "running" and task.get("pid"):
        try:
            os.kill(task["pid"], signal.SIGTERM)
        except ProcessLookupError:
            pass
    task["status"] = "canceled"
    task["finished_at"] = now_iso()
    _update_task(q, task)
    append_task_log(task, "人工 cancel")
    print(f"✅ 任务 {task_id} 已取消")
    return 0


def cmd_recover(as_json: bool = False) -> int:
    """launchd 周期调用：进程被杀 → 自动续跑（断点续跑）。
    - running 且 pid 已死(进程消失/超时) → 记 interrupted，retries<max → 重启
    - pending 且创建后未开始 → 拉起执行（恢复器单线程一次只拉起一个，防并发）
    拉起动作异步（detach），recover 立即返回。
    """
    q = load_queue()
    acted: List[str] = []
    now_mono = time.monotonic()

    def _pid_alive(pid: Optional[int]) -> bool:
        if not pid:
            return False
        try:
            os.kill(pid, 0)
            return True
        except (ProcessLookupError, PermissionError):
            return False

    for t in q["tasks"]:
        if t["status"] == "running":
            if _pid_alive(t.get("pid")):
                continue  # 还活着
            # 进程死 → 中断
            append_task_log(t, "[recover] 检测到运行中进程已死 → 中断续跑")
            t["last_error"] = t.get("last_error") or "process_killed"
            if t["retries"] < t["max_retries"]:
                t["retries"] += 1
                t["status"] = "pending"
                acted.append(f"interrupted+requeue#{t['id']}")
            else:
                t["status"] = "failed"
                t["finished_at"] = now_iso()
                t["last_error"] = "process_killed·重试耗尽"
                acted.append(f"killed_final#{t['id']}")
            _update_task(q, t)

    # 拉起最早一个 pending（无人值守续跑）
    for t in q["tasks"]:
        if t["status"] == "pending" and t.get("command"):
            # 超龄任务（超过 max_hours 倍数）不再拉起
            try:
                created = datetime.fromisoformat(t["created_at"])
                if datetime.fromisoformat(now_iso()) - created > timedelta(hours=t["max_hours"] * 2):
                    t["status"] = "failed"
                    t["last_error"] = "stale: 超过 2*max_hours 未完成"
                    t["finished_at"] = now_iso()
                    _update_task(q, t)
                    acted.append(f"stale#{t['id']}")
                    continue
            except Exception:
                pass
            t["status"] = "running"
            t["started_at"] = now_iso()
            t["pid"] = os.getpid()
            _update_task(q, t)
            append_task_log(t, f"[recover] 续跑拉起: {t['desc']} | cmd={t['command']}")
            # 异步执行，不阻塞 recover
            subprocess.Popen(
                [sys.executable, __file__, "run", str(t["id"]), "--recover", "--no-pick"],
                cwd=str(REPO_ROOT),
                start_new_session=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            acted.append(f"relaunch#{t['id']}")
            break
    if as_json:
        print(json.dumps({"acted": acted}, ensure_ascii=False))
        return 0
    print(f"recover: {acted if acted else '无待恢复任务'}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(prog="lh-agent-long", description="龍魂长期无人值守任务引擎 v1.0")
    sub = parser.add_subparsers(dest="command")

    p_run = sub.add_parser("run", help="入队并执行长期任务")
    p_run.add_argument("desc", nargs="?", default="", help="任务描述")
    p_run.add_argument("--cmd", type=str, default=None, help="实际执行命令(字符串)")
    p_run.add_argument("--max-hours", type=float, default=MAX_HOURS_DEFAULT)
    p_run.add_argument("--max-retries", type=int, default=MAX_RETRIES_DEFAULT)
    p_run.add_argument("--recover", action="store_true", help=argparse.SUPPRESS)
    p_run.add_argument("--no-pick", action="store_true", help=argparse.SUPPRESS)

    p_st = sub.add_parser("status", help="查看任务队列")
    p_st.add_argument("--json", action="store_true")
    p_st.add_argument("--all", action="store_true")

    p_rc = sub.add_parser("root-cause", help="失败根因分析")
    p_rc.add_argument("task_id", type=int)
    p_rc.add_argument("--json", action="store_true")

    p_can = sub.add_parser("cancel", help="取消任务")
    p_can.add_argument("task_id", type=int)

    p_rec = sub.add_parser("recover", help="kill 后自动续跑(launchd 周期调)")
    p_rec.add_argument("--json", action="store_true")

    p_t = sub.add_parser("test", help="自测")
    args = parser.parse_args()

    if args.command == "run":
        # recover 续跑模式：desc 参数实为已存在的 task_id
        if getattr(args, "recover", False) and args.desc.isdigit():
            _resume_run(int(args.desc))
            return
        cmd_run(args.desc, args.cmd, args.max_hours, args.max_retries)
    elif args.command == "status":
        cmd_status(show_all=args.all, as_json=args.json)
    elif args.command == "root-cause":
        cmd_root_cause(args.task_id, as_json=args.json)
    elif args.command == "cancel":
        cmd_cancel(args.task_id)
    elif args.command == "recover":
        cmd_recover(as_json=args.json)
    elif args.command == "test":
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(AgentLongTest)
        ok = unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
        sys.exit(0 if ok else 1)
    else:
        parser.print_help()


def _resume_run(task_id: int) -> None:
    """续跑已存在任务（不重造）：复用其 retries/max_retries/max_hours。"""
    q = load_queue()
    task = find_task(q, task_id)
    if not task:
        print(f"❌ 任务 {task_id} 不存在")
        sys.exit(1)
    if not task.get("command"):
        task["status"] = "failed"
        task["last_error"] = "no_command: 无执行体"
        _update_task(q, task)
        return
    # 直接复用执行循环（不二次入队）
    rc = _execute_task(task_id, q)
    sys.exit(0 if rc == 0 else 1)


class AgentLongTest(unittest.TestCase):
    """核心链路 5 项锚点"""

    def setUp(self):
        AGENT_DIR.mkdir(parents=True, exist_ok=True)
        self._bak = None
        if QUEUE_FILE.exists():
            self._bak = QUEUE_FILE.read_text(encoding="utf-8")
        # 清空队列以隔离测试
        save_queue({"next_id": 1, "tasks": []})

    def tearDown(self):
        if self._bak is not None:
            QUEUE_FILE.write_text(self._bak, encoding="utf-8")

    def test_01_success(self):
        """成功任务 → success + 队列持久化"""
        rc = cmd_run("测试成功任务", "python3 -c 'print(42)'", 0.1, 1)
        self.assertEqual(rc, 0)
        q = load_queue()
        self.assertEqual(q["tasks"][-1]["status"], "success")
        log = _task_output(q["tasks"][-1])
        self.assertIn("42", log)

    def test_02_retry_then_fail(self):
        """失败命令 → 重试 max_retries 后 failed"""
        rc = cmd_run("测试失败任务", "python3 -c 'import sys;sys.exit(7)'", 0.1, 2)
        self.assertNotEqual(rc, 0)
        t = load_queue()["tasks"][-1]
        self.assertEqual(t["status"], "failed")
        self.assertEqual(t["retries"], 2)

    def test_03_no_command_rejected(self):
        """无 --cmd → 执行返回非零并落 failed"""
        q0 = load_queue()
        task_id = q0["next_id"]
        cmd_run("无命令任务", None, 0.1, 1)
        q = load_queue()
        self.assertEqual(q["tasks"][-1]["status"], "failed")
        self.assertEqual(q["tasks"][-1]["id"], task_id)

    def test_04_status(self):
        """status 输出不抛错"""
        self.assertEqual(cmd_status(as_json=True), 0)

    def test_05_cancel(self):
        """cancel 状态机"""
        q = load_queue()
        q["next_id"] += 1
        q["tasks"].append({"id": 100, "desc": "x", "command": "sleep 100", "status": "running",
                           "retries": 0, "max_retries": 1, "max_hours": 38, "pid": None,
                           "created_at": now_iso()})
        save_queue(q)
        self.assertEqual(cmd_cancel(100), 0)
        self.assertEqual(find_task(load_queue(), 100)["status"], "canceled")


if __name__ == "__main__":
    main()
