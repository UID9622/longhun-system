#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂·自触发编排引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·䷝离-AUTO-TRIGGER-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

口号: 老大说人话 → 系统找脚本 → 自动跑 → 跑完自动停

三层引擎:
  L1 意图层 — 人话匹配脚本（复用 lh_run.py CommandIndex）
  L2 执行层 — 生命周期管理（启动→监控→停止，复用 lh_lifecycle.ScriptRunner）
  L3 守护层 — 后台监控触发源（文件变化/Unix Socket/定时任务）

使用方式:
  # 一次性触发
  python3 bin/lh_auto_trigger.py "健康检查"
  python3 bin/lh_auto_trigger.py "做视频" --args 稿.txt --dry-run

  # 守护模式（后台监听触发）
  python3 bin/lh_auto_trigger.py --watch

  # 批量触发
  python3 bin/lh_auto_trigger.py --batch "健康检查,反诈,同步鲲鹏"

  # 查看运行中的进程
  python3 bin/lh_auto_trigger.py --ps

  # 停止所有
  python3 bin/lh_auto_trigger.py --kill-all
"""

import os
import sys
import re
import json
import time
import shlex
import signal
import socket
import threading
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from difflib import get_close_matches

# 导入生命周期管理器
from lh_lifecycle import ScriptRunner, RunResult, RunStatus, ps_list, stop_running

# ============================================================
# 配置
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_PATH = BASE_DIR / ".codebuddy" / "COMMAND_INDEX.md"
HISTORY_FILE = Path.home() / ".longhun" / "trigger_history.jsonl"
SOCKET_PATH = Path.home() / ".longhun" / "trigger.sock"
WATCH_DIRS = [
    BASE_DIR / "bin",
    BASE_DIR / "engines",
    BASE_DIR / "deploy",
]
PID_FILE = Path.home() / ".longhun" / "auto_trigger.pid"

# 默认脚本超时（秒）
DEFAULT_TIMEOUTS = {
    "健康检查": 120,
    "部署": 300,
    "训练": 3600,
    "视频": 600,
    "搜索": 30,
    "审计": 60,
    "同步": 180,
    "对齐": 120,
    "签名": 60,
    "备份": 300,
    "default": 300,
}


# ============================================================
# 意图匹配器（复用 lh_run.py 的 CommandIndex）
# ============================================================

class IntentMatcher:
    """意图→脚本 匹配器"""

    def __init__(self):
        self.triggers: Dict[str, str] = {}
        self.commands: Dict[str, Dict] = {}
        self.aliases: Dict[str, str] = {}
        self._load()

    def _load(self):
        if not INDEX_PATH.exists():
            self._load_fallback()
            return

        with open(INDEX_PATH, 'r', encoding='utf-8') as f:
            content = f.read()

        self._parse_trigger_table(content)
        self._parse_subcommand_table(content)
        self._set_aliases()

    def _parse_trigger_table(self, content: str):
        """解析 ## 🎯 自然语言触发词 表格"""
        pattern = r'## 🎯 自然语言触发词.*?\n(.*?)(?=\n---\n|\n## )'
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            return
        section = match.group(1)
        for line in section.strip().split('\n'):
            line = line.strip()
            if not line or not line.startswith('|'):
                continue
            if re.match(r'^\|[\s:\-|]+\|$', line):
                continue
            if '触发词' in line and '自动执行命令' in line:
                continue
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) >= 2:
                trigger_text, cmd_raw = parts[0], parts[1]
                desc = parts[2] if len(parts) >= 3 else ""
                cmd = cmd_raw.strip('`').strip()
                if trigger_text and cmd:
                    self.commands[trigger_text] = {"command": cmd, "description": desc}
                    for t in trigger_text.split(','):
                        t = t.strip()
                        if t:
                            self.triggers[t.lower()] = cmd

    def _parse_subcommand_table(self, content: str):
        """解析 ## 🔥 lh 子命令速查 中的命令"""
        # 抓取所有 code 块中的 lh --xxx 命令
        lh_commands = re.findall(r'`lh (--[\w-]+)`', content)
        for cmd in lh_commands:
            key = cmd.replace('--', '').replace('-', ' ')
            if key not in self.triggers:
                self.triggers[key] = f"python3 bin/lh.py {cmd}"

    def _set_aliases(self):
        self.aliases = {
            "lh": "python3 bin/lh.py",
            "lh-update": "python3 bin/lh_update_index.py",
            "lh-run": "python3 bin/lh_run.py",
            "健康": "python3 deploy/scripts/health_check.sh",
            "体检": "python3 deploy/scripts/health_check.sh",
            "状态": "python3 bin/lh_unified_brain.py status",
            "搜": "python3 bin/lh_search_engine.py search",
            "推到鲲鹏": "bash deploy/sync-to-kunpeng.sh",
            "同步鲲鹏": "bash deploy/sync-to-kunpeng.sh",
            "签名": "python3 bin/lh_gpg_sign.py sign .",
            "GPG": "python3 bin/lh_gpg_sign.py scan .",
            "对齐": "python3 bin/lh_align_checker.py --json",
            "自检": "python3 bin/lh_deben_audit.py scan",
            "审计": "python3 bin/lh_deben_audit.py scan",
            "代码审计": "python3 bin/lh_three_color_audit.py audit",
            "安全检查": "python3 bin/lh_regulatory_firewall.py --test",
            "反诈": "python3 bin/lh_regulatory_firewall.py --test -p 2",
            "记忆": "python3 bin/lh_memory_load.py",
            "知识搜索": "python3 bin/lh_local_knowledge_engine.py search",
            "语义搜索": "python3 bin/lh_local_knowledge_engine.py search",
            "浏览器史官": "python3 bin/lh_browser_historian.py status",
            "CNSH编译": "python3 bin/cnsh_compiler.py",
            "七维推演": "python3 bin/lh_seven_dimension_engine_v2.py --interactive",
            "数字孪生": "python3 bin/lh_digital_twin.py --status",
            "三才": "python3 bin/san_cai_v2.py --interactive",
            "权重": "python3 bin/lh_weight_algorithm.py --all",
            "DNA": "python3 bin/lh_dna_generator.py",
            "部署": "bash deploy/sync-to-kunpeng.sh",
            "停止": "__STOP_ALL__",
            "停": "__STOP_ALL__",
            "杀了": "__KILL_ALL__",
            "全部停": "__KILL_ALL__",
        }

    def _load_fallback(self):
        """无索引文件时的降级匹配"""
        self._set_aliases()

    def match(self, query: str) -> Optional[str]:
        """四级匹配：别名→精确→包含→模糊"""
        q = query.strip().lower()

        # 0. 特殊命令
        if q in ("停止", "停"):
            return "__STOP_ALL__"
        if q in ("杀了", "全部停", "终止全部"):
            return "__KILL_ALL__"

        # 1. 精确别名
        if q in self.aliases:
            return self.aliases[q]

        # 2. 精确触发词
        if q in self.triggers:
            return self.triggers[q]

        # 3. 包含匹配
        best_match = None
        best_score = 0
        for trigger, cmd in self.triggers.items():
            if trigger in q or q in trigger:
                score = len(trigger) if trigger in q else len(q)
                if score > best_score:
                    best_score = score
                    best_match = cmd

        if best_match:
            return best_match

        # 4. 模糊匹配
        matches = get_close_matches(q, list(self.triggers.keys()), n=1, cutoff=0.4)
        if matches:
            return self.triggers[matches[0]]

        # 5. 别名模糊
        alias_matches = get_close_matches(q, list(self.aliases.keys()), n=1, cutoff=0.4)
        if alias_matches:
            return self.aliases[alias_matches[0]]

        return None

    def get_timeout(self, query: str) -> int:
        """根据意图获取建议超时"""
        q = query.strip()
        for key, timeout in DEFAULT_TIMEOUTS.items():
            if key in q:
                return timeout
        return DEFAULT_TIMEOUTS["default"]

    def list_all(self) -> List[Tuple[str, str]]:
        results = []
        for trigger, data in self.commands.items():
            results.append((trigger, data.get("command", "")))
        for alias, cmd in self.aliases.items():
            if alias not in [r[0] for r in results]:
                results.append((alias, cmd))
        return sorted(results)


# ============================================================
# 自触发编排器
# ============================================================

class AutoTrigger:
    """
    自触发编排器

    用法:
      at = AutoTrigger()
      result = at.trigger("健康检查")          # 一次性触发
      at.batch(["健康检查", "同步鲲鹏", "审计"])  # 批量触发
      at.watch()                               # 守护模式
    """

    def __init__(self):
        self.matcher = IntentMatcher()
        self.runner = ScriptRunner(timeout=300, idle_timeout=0)
        self._watcher_running = False

    def trigger(self, query: str, args: List[str] = None,
                dry_run: bool = False, timeout: int = None) -> RunResult:
        """
        一次触发：人话→脚本→自动跑→自动停

        返回 RunResult
        """
        command = self.matcher.match(query)

        # 特殊命令
        if command == "__STOP_ALL__":
            print("🛑 停止所有运行中的脚本...")
            self.runner.stop_all()
            return RunResult(
                run_id="stop-all",
                command="stop-all",
                status=RunStatus.SUCCESS,
                finished_at=datetime.now().isoformat()
            )

        if command == "__KILL_ALL__":
            print("💀 强制终止所有...")
            killed = self.runner.stop_all()
            return RunResult(
                run_id="kill-all",
                command="kill-all",
                status=RunStatus.SUCCESS,
                stdout=f"终止 {killed} 个进程",
                finished_at=datetime.now().isoformat()
            )

        if not command:
            print(f"\n❌ 未找到匹配: {query}")
            suggestions = get_close_matches(
                query.strip().lower(),
                list(self.matcher.triggers.keys()) + list(self.matcher.aliases.keys()),
                n=5, cutoff=0.3
            )
            if suggestions:
                print(f"💡 你可能想: {', '.join(suggestions)}")
            return RunResult(
                run_id="no-match",
                command=query,
                status=RunStatus.ERROR,
                error_message=f"未找到匹配命令: {query}",
                finished_at=datetime.now().isoformat()
            )

        # 参数替换
        if args:
            if "{}" in command:
                command = command.replace("{}", " ".join(args))
            else:
                for i, arg in enumerate(args, 1):
                    command = command.replace(f"${i}", arg)

        if dry_run:
            print(f"\n🔍 [干运行] {command}")
            return RunResult(
                run_id="dry-run",
                command=command,
                status=RunStatus.SUCCESS,
                finished_at=datetime.now().isoformat()
            )

        # 确定超时
        if timeout is None:
            timeout = self.matcher.get_timeout(query)
        self.runner.timeout = timeout

        # 执行
        label = query[:30]
        result = self.runner.run(command, cwd=str(BASE_DIR), label=label)

        # 记录历史
        self._log(query, command, result)

        return result

    def batch(self, queries: List[str], dry_run: bool = False,
              parallel: bool = False, timeout: int = None) -> List[RunResult]:
        """
        批量触发

        参数:
          - parallel: True=并行执行，False=串行
        """
        results = []
        if parallel:
            threads = []
            for query in queries:
                t = threading.Thread(
                    target=lambda q: results.append(self.trigger(q, dry_run=dry_run, timeout=timeout)),
                    args=(query,)
                )
                threads.append(t)
                t.start()
            for t in threads:
                t.join(timeout=timeout or 300)
        else:
            for query in queries:
                result = self.trigger(query, dry_run=dry_run, timeout=timeout)
                results.append(result)

        return results

    def watch(self, daemonize: bool = False):
        """
        守护模式：后台持续监听触发

        触发源:
          1. Unix Socket → ~/.longhun/trigger.sock
          2. 后续可扩展: 文件监控 / HTTP API
        """
        if daemonize:
            self._daemonize()

        # 写 PID
        PID_FILE.parent.mkdir(parents=True, exist_ok=True)
        PID_FILE.write_text(str(os.getpid()))

        self._watcher_running = True
        print(f"🐉 自触发守护已启动 · PID {os.getpid()}")
        print(f"   Socket: {SOCKET_PATH}")
        print(f"   发送触发: echo '健康检查' | nc -U {SOCKET_PATH}")
        print(f"   停止守护: kill {os.getpid()} 或 lh --trigger 停")

        # 清理旧 socket
        if SOCKET_PATH.exists():
            SOCKET_PATH.unlink()

        # 创建 Unix Socket 监听
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(str(SOCKET_PATH))
        server.listen(5)
        server.settimeout(1.0)  # 1秒超时用于检查停止信号

        def handle_client(conn):
            try:
                data = conn.recv(4096).decode('utf-8').strip()
                if data:
                    print(f"\n📨 收到触发: {data}")
                    self.trigger(data)
            except Exception as e:
                print(f"⚠️ 处理触发异常: {e}")
            finally:
                conn.close()

        try:
            while self._watcher_running:
                try:
                    conn, _ = server.accept()
                    t = threading.Thread(target=handle_client, args=(conn,))
                    t.daemon = True
                    t.start()
                except socket.timeout:
                    continue
                except Exception as e:
                    if self._watcher_running:
                        print(f"⚠️ Socket异常: {e}")
        except KeyboardInterrupt:
            print("\n🛑 守护停止")
        finally:
            server.close()
            if SOCKET_PATH.exists():
                SOCKET_PATH.unlink()
            if PID_FILE.exists():
                PID_FILE.unlink()
            self.runner.stop_all()

    def stop_watch(self):
        """停止守护"""
        self._watcher_running = False

    def _daemonize(self):
        """双 fork 守护进程化"""
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            sys.exit(1)

        os.setsid()
        os.umask(0)

        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            sys.exit(1)

        # 重定向标准流
        sys.stdout.flush()
        sys.stderr.flush()
        null = os.open(os.devnull, os.O_RDWR)
        os.dup2(null, sys.stdin.fileno())
        os.dup2(null, sys.stdout.fileno())
        os.dup2(null, sys.stderr.fileno())

    def _log(self, query: str, command: str, result: RunResult):
        try:
            HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
                f.write(json.dumps({
                    "timestamp": datetime.now().isoformat(),
                    "query": query,
                    "command": command,
                    "status": result.status.value,
                    "duration": result.duration,
                    "exit_code": result.exit_code
                }, ensure_ascii=False) + '\n')
        except Exception:
            pass

    def list_processes(self):
        """查看运行中的进程"""
        return self.runner.list_running()


# ============================================================
# 命令行入口
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·自触发编排引擎 — 说人话→自动跑→自动停",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 一次性触发
  lh-auto "健康检查"
  lh-auto "做视频" --args 稿.txt
  lh-auto "反诈" --dry-run

  # 守护模式
  lh-auto --watch                   # 前台监听
  lh-auto --watch --daemon          # 后台守护

  # 批量
  lh-auto --batch "健康检查,同步鲲鹏,审计"

  # 管理
  lh-auto --ps                      # 查看运行中
  lh-auto --kill-all                # 全部停止
  lh-auto --list                    # 查看所有可触发命令
"""
    )
    parser.add_argument('query', nargs='?', help='自然语言触发（如 "健康检查"）')
    parser.add_argument('--args', nargs='*', help='传递给脚本的参数')
    parser.add_argument('--dry-run', action='store_true', help='干运行（只看不执行）')
    parser.add_argument('--timeout', type=int, help='超时秒数（覆盖默认）')
    parser.add_argument('--watch', action='store_true', help='守护模式（后台监听触发）')
    parser.add_argument('--daemon', action='store_true', help='后台守护（配合--watch）')
    parser.add_argument('--batch', type=str, help='批量触发（逗号分隔）')
    parser.add_argument('--parallel', action='store_true', help='批量时并行执行')
    parser.add_argument('--ps', action='store_true', help='查看运行中的进程')
    parser.add_argument('--kill-all', action='store_true', help='终止所有运行中的进程')
    parser.add_argument('--list', action='store_true', help='列出所有可触发命令')
    parser.add_argument('--search', type=str, help='搜索可触发命令')

    args = parser.parse_args()
    at = AutoTrigger()

    # --ps
    if args.ps:
        procs = at.list_processes()
        if not procs:
            print("✅ 没有正在运行的脚本")
        else:
            print(f"📊 正在运行的脚本 ({len(procs)}):")
            for p in procs:
                print(f"   PID {p['pid']} · {p['command'][:60]} · {p['started_at']}")
        return

    # --kill-all
    if args.kill_all:
        killed = at.runner.stop_all()
        print(f"🛑 已终止 {killed} 个进程")
        return

    # --list
    if args.list:
        cmds = at.matcher.list_all()
        if args.search:
            cmds = [(t, c) for t, c in cmds if args.search.lower() in t.lower() or args.search.lower() in c.lower()]
        print(f"\n📋 可触发命令 ({len(cmds)}):\n")
        for trigger, cmd in cmds:
            display_cmd = cmd[:70] + "..." if len(cmd) > 70 else cmd
            print(f"   {trigger:20s} → {display_cmd}")
        return

    # --watch
    if args.watch:
        try:
            at.watch(daemonize=args.daemon)
        except KeyboardInterrupt:
            print("\n🛑 守护停止")
        return

    # --batch
    if args.batch:
        queries = [q.strip() for q in args.batch.split(',') if q.strip()]
        results = at.batch(queries, dry_run=args.dry_run, parallel=args.parallel, timeout=args.timeout)
        # 汇总
        success = sum(1 for r in results if r.is_ok())
        print(f"\n📊 批量执行完成: {success}/{len(results)} 成功")
        sys.exit(0 if success == len(results) else 1)
        return

    # 单次触发
    if args.query:
        result = at.trigger(args.query, args=args.args, dry_run=args.dry_run, timeout=args.timeout)
        sys.exit(0 if result.is_ok() else 1)
        return

    # 无参数
    parser.print_help()


if __name__ == "__main__":
    main()
