#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂·一体化命令引擎 v2.0
DNA: #龍芯⚡️丙午·乙未·甲辰·庚午·䷝离为火-RUNNER-v2.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

功能：
  - 自然语言匹配命令（精确→模糊→补全）
  - 自动检查索引更新（新增脚本后自动刷新）
  - 干运行（--dry-run）
  - 带参数执行（--args）
  - 历史记录
  - 一键更新索引（--update）
"""

import os
import sys
import re
import json
import subprocess
import time
import shlex
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from difflib import get_close_matches
import argparse

# ============================================================
# 配置
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_PATH = BASE_DIR / ".codebuddy" / "COMMAND_INDEX.md"
HISTORY_FILE = Path.home() / ".longhun" / "command_history.jsonl"
UPDATE_SCRIPT = BASE_DIR / "bin" / "lh_update_index.py"
AUTO_UPDATE_INTERVAL = 3600  # 1小时

# ============================================================
# 索引管理器
# ============================================================

class CommandIndex:
    """加载并解析 COMMAND_INDEX.md，提供命令查找能力"""

    def __init__(self):
        self.index_path = INDEX_PATH
        self.commands: Dict[str, Dict] = {}
        self.aliases: Dict[str, str] = {}
        self.triggers: Dict[str, str] = {}
        self.last_update = None
        self._load()

    def _load(self):
        if not self.index_path.exists():
            self.commands = {}
            self.aliases = {}
            self.triggers = {}
            self.last_update = None
            return

        self.last_update = datetime.fromtimestamp(self.index_path.stat().st_mtime)

        with open(self.index_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 解析主触发词表：## 🎯 自然语言触发词
        self._parse_trigger_table(content)

        # 硬编码别名
        self.aliases["lh"] = "python3 ~/longhun-system/bin/lh.py"
        self.aliases["lh-update"] = "python3 ~/longhun-system/bin/lh_update_index.py"
        self.aliases["lh-run"] = "python3 ~/longhun-system/bin/lh_run.py"

        # 补一条：自更新索引
        self.triggers["更新索引"] = "python3 ~/longhun-system/bin/lh_update_index.py"
        self.triggers["index更新"] = "python3 ~/longhun-system/bin/lh_update_index.py"

    def _parse_trigger_table(self, content: str):
        """解析 ## 🎯 自然语言触发词 表格"""
        # 匹配从 "## 🎯 自然语言触发词" 到下一个 "---" 或 "## " 之间的内容
        pattern = r'## 🎯 自然语言触发词.*?\n(.*?)(?=\n---\n|\n## )'
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            return
        section = match.group(1)
        lines = section.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line or not line.startswith('|'):
                continue
            # 跳过对齐行和分割线
            if re.match(r'^\|[\s:\-|]+\|$', line):
                continue
            # 跳过表头
            if '触发词' in line and '自动执行命令' in line:
                continue
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) >= 2:
                trigger_text, cmd_raw = parts[0], parts[1]
                desc = parts[2] if len(parts) >= 3 else ""
                if not trigger_text or not cmd_raw:
                    continue
                # 去除命令两侧的反引号
                cmd = cmd_raw.strip('`').strip()
                if not cmd:
                    continue
                self.commands[trigger_text] = {
                    "command": cmd,
                    "description": desc
                }
                # 拆分逗号触发词
                for t in trigger_text.split(','):
                    t = t.strip()
                    if t:
                        self.triggers[t.lower()] = cmd

    def get_command(self, query: str) -> Optional[str]:
        """四级匹配：精确别名→精确触发词→包含匹配→模糊匹配"""
        q = query.strip().lower()

        # 1. 精确匹配别名
        if q in self.aliases:
            return self.aliases[q]

        # 2. 精确匹配触发词
        if q in self.triggers:
            return self.triggers[q]

        # 3. 包含匹配（双向：触发词在query中，或query在触发词中）
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

        # 4. difflib 模糊匹配（cutoff=0.45 宽容匹配）
        matches = get_close_matches(q, list(self.triggers.keys()), n=1, cutoff=0.45)
        if matches:
            return self.triggers[matches[0]]

        return None

    def list_commands(self) -> List[Tuple[str, str, str]]:
        results = []
        for trigger, data in self.commands.items():
            results.append((trigger, data["command"], data["description"]))
        return results


# ============================================================
# 核心引擎
# ============================================================

class CommandRunner:
    def __init__(self, auto_update: bool = True):
        self.index = CommandIndex()
        self.auto_update = auto_update
        self.history_file = HISTORY_FILE
        self.history_file.parent.mkdir(parents=True, exist_ok=True)

    def _need_update(self) -> bool:
        if not self.auto_update:
            return False
        if not self.index.last_update:
            return True
        age = (datetime.now() - self.index.last_update).total_seconds()
        return age > AUTO_UPDATE_INTERVAL

    def _run_update(self) -> bool:
        if not UPDATE_SCRIPT.exists():
            print("⚠️ 更新脚本不存在，跳过自动更新")
            return False
        try:
            print("🔄 检查索引更新...")
            result = subprocess.run(
                [sys.executable, str(UPDATE_SCRIPT)],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                self.index = CommandIndex()
                print("✅ 索引已自动更新")
                return True
            else:
                print(f"⚠️ 索引更新失败（退出码{result.returncode}），继续使用旧索引")
                return False
        except subprocess.TimeoutExpired:
            print("⚠️ 索引更新超时，继续使用旧索引")
            return False
        except Exception as e:
            print(f"⚠️ 索引更新异常: {e}")
            return False

    def run(self, query: str, args: Optional[List[str]] = None,
            dry_run: bool = False, force_update: bool = False) -> int:
        # 强制更新
        if force_update:
            print("🔄 强制更新索引...")
            self._run_update()

        # 自动更新检查
        if self._need_update():
            self._run_update()

        command = self.index.get_command(query)

        if not command:
            print(f"\n❌ 未找到匹配命令: {query}")
            # 列出相似建议
            suggestions = get_close_matches(
                query.strip().lower(),
                list(self.index.triggers.keys()),
                n=5, cutoff=0.3
            )
            if suggestions:
                print(f"💡 你可能想找: {', '.join(suggestions)}")
            print("\n📋 可用命令 (前10个):")
            for trigger, cmd, desc in self.index.list_commands()[:10]:
                display_cmd = cmd[:55] + "..." if len(cmd) > 55 else cmd
                print(f"   {trigger}: {desc}")
                print(f"       {display_cmd}")
            print("\n💡 提示: 使用 --list 查看全部, 或运行 --update 强制刷新索引")
            return 1

        # 参数替换
        if args:
            if "{}" in command:
                command = command.replace("{}", " ".join(args))
            else:
                for i, arg in enumerate(args, 1):
                    command = command.replace(f"${i}", arg)

        # 解析命令
        try:
            cmd_parts = shlex.split(command)
        except ValueError:
            cmd_parts = command.split()
        if not cmd_parts:
            return 1

        # 记录历史
        self._log_history(query, command)

        if dry_run:
            print(f"🔍 [干运行] {command}")
            return 0

        # 执行
        print(f"🚀 执行: {command}")
        try:
            if cmd_parts[0].endswith('.py'):
                result = subprocess.run(
                    [sys.executable] + cmd_parts,
                    cwd=str(BASE_DIR)
                )
            else:
                result = subprocess.run(cmd_parts, cwd=str(BASE_DIR))

            if result.returncode == 0:
                print("✅ 执行成功")
            else:
                print(f"❌ 执行失败 (退出码: {result.returncode})")
            return result.returncode

        except FileNotFoundError:
            print(f"❌ 命令不存在: {cmd_parts[0]}")
            return 1
        except Exception as e:
            print(f"❌ 执行错误: {e}")
            return 1

    def _log_history(self, query: str, command: str):
        try:
            with open(self.history_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps({
                    "timestamp": datetime.now().isoformat(),
                    "query": query,
                    "command": command
                }, ensure_ascii=False) + '\n')
        except Exception:
            pass


# ============================================================
# 命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·一体化命令引擎 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 自然语言执行
  lh-run "健康检查"
  lh-run "反诈" --dry-run
  lh-run "做视频" --args 稿.txt

  # 查看全部命令
  lh-run --list

  # 自动补全
  lh-run --complete "部署"

  # 强制更新索引
  lh-run --update

  # 查看历史
  lh-run --history
        """
    )

    parser.add_argument("query", nargs="?", help="自然语言命令")
    parser.add_argument("--args", nargs="*", help="传递参数给命令")
    parser.add_argument("--dry-run", action="store_true", help="只显示匹配命令不执行")
    parser.add_argument("--list", action="store_true", help="列出所有可用命令")
    parser.add_argument("--complete", metavar="文本", help="自动补全建议")
    parser.add_argument("--update", action="store_true", help="强制更新索引")
    parser.add_argument("--history", action="store_true", help="显示执行历史")
    parser.add_argument("--no-auto", action="store_true", help="禁用自动索引更新")

    args = parser.parse_args()

    runner = CommandRunner(auto_update=not args.no_auto)

    # --list
    if args.list:
        print("📋 可用命令:\n" + "-" * 70)
        all_cmds = runner.index.list_commands()
        for trigger, cmd, desc in all_cmds:
            display_cmd = cmd[:50] + "..." if len(cmd) > 50 else cmd
            print(f"  {trigger}: {desc}")
            print(f"    命令: {display_cmd}")
        print(f"\n  共 {len(all_cmds)} 条命令")
        return

    # --complete
    if args.complete is not None:
        text = args.complete
        matches = []
        for trigger in runner.index.triggers.keys():
            if trigger.startswith(text) or text in trigger:
                matches.append(trigger)
        if matches:
            # 排序：完全匹配优先，然后按长度
            exact = [m for m in matches if m == text]
            starts = [m for m in matches if m.startswith(text) and m != text]
            contains = [m for m in matches if text in m and not m.startswith(text) and m != text]
            sorted_matches = exact + starts + contains
            print(f"📋 补全建议 ({len(sorted_matches)}个):")
            for m in sorted_matches[:20]:
                cmd = runner.index.triggers[m]
                display_cmd = cmd[:55] + "..." if len(cmd) > 55 else cmd
                print(f"   {m} → {display_cmd}")
        else:
            print("无匹配补全")
        return

    # --history
    if args.history:
        if runner.history_file.exists():
            with open(runner.history_file, 'r') as f:
                lines = f.readlines()
                if lines:
                    print(f"📜 执行历史 (最近20条):\n" + "-" * 70)
                    for line in lines[-20:]:
                        try:
                            data = json.loads(line)
                            ts = data.get('timestamp', '')[:19]
                            q = data.get('query', '')[:25]
                            c = data.get('command', '')[:55]
                            print(f"  [{ts}] {q} → {c}")
                        except Exception:
                            pass
                else:
                    print("📜 暂无执行历史")
        else:
            print("📜 暂无执行历史")
        return

    # --update
    if args.update:
        runner._run_update()
        return

    # 执行模式
    if not args.query:
        parser.print_help()
        return

    sys.exit(runner.run(args.query, args.args, args.dry_run, force_update=args.update))


if __name__ == "__main__":
    main()
