#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂·命令自动执行引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-命令执行-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

铁律第11条：老大不记命令，AI自己挑。
功能：解析 COMMAND_INDEX.md，根据用户自然语言意图匹配并执行命令。
"""

import os
import sys
import re
import json
import subprocess
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from difflib import get_close_matches
from datetime import datetime

# ===== 路径常量 =====
ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / ".codebuddy/COMMAND_INDEX.md"
HISTORY_FILE = ROOT / "logs/command_history.jsonl"

# ============================================================
# 一、索引解析器
# ============================================================

class CommandIndex:
    """从 COMMAND_INDEX.md 解析命令映射"""

    def __init__(self, index_path: Path = None):
        self.index_path = index_path or INDEX_PATH
        self.commands: Dict[str, Dict] = {}     # trigger → {cmd, desc, section}
        self.aliases: Dict[str, str] = {}       # alias → cmd
        self.triggers: List[Tuple[str, str, str]] = []  # (trigger, cmd, desc)
        self._load()

    def _load(self):
        """加载并解析 COMMAND_INDEX.md"""
        if not self.index_path.exists():
            return
        with open(self.index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self._parse_trigger_table(content)
        self._parse_aliases(content)

    def _parse_trigger_table(self, content: str):
        """解析 🎯 自然语言触发词 表格"""
        # 找触发词表格: ## 🎯 自然语言触发词 到下一个 ##
        pattern = r'##\s*🎯\s*自然语言触发词\s*\n(.*?)(?=\n##\s|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            return
        section = match.group(1)
        in_table = False
        for line in section.split('\n'):
            line = line.strip()
            if not line:
                continue
            if line.startswith('|') and '---' in line:
                in_table = True
                continue
            if in_table and line.startswith('|'):
                parts = [p.strip() for p in line.split('|')[1:-1]]
                if len(parts) >= 3:
                    trigger, command, desc = parts[0], parts[1], parts[2]
                    if trigger and command:
                        # 去除 ` 包裹
                        cmd_clean = command.strip('`')
                        self.commands[trigger] = {
                            "command": cmd_clean,
                            "description": desc,
                            "section": "自然语言"
                        }
                        self.triggers.append((trigger, cmd_clean, desc))
                        # 拆分多触发词
                        for t in trigger.split(','):
                            t = t.strip()
                            if t:
                                self.commands[t] = {
                                    "command": cmd_clean,
                                    "description": desc,
                                    "section": "自然语言"
                                }

    def _parse_aliases(self, content: str):
        """解析 lh 快捷别名"""
        pattern = r'\|\s*`(lh\s+\S+)`\s*\|\s*`([^`]+)`\s*\|'
        for match in re.finditer(pattern, content):
            alias, cmd = match.group(1), match.group(2).strip()
            self.aliases[alias] = cmd
        # 也解析三秒速查表
        pattern2 = r'\|\s*\|([^|]+)\|\s*`([^`]+)`\s*\|'
        for match in re.finditer(pattern2, content):
            desc_raw = match.group(1).strip()
            cmd = match.group(2).strip()
            # 提取中文简短描述
            desc_short = desc_raw[:20] if desc_raw else ""
            if cmd:
                self.aliases[desc_short] = cmd

    def match(self, query: str) -> Optional[Tuple[str, str]]:
        """
        多级匹配：
        1. 精确匹配触发词
        2. 精确匹配别名
        3. 关键词包含匹配
        4. difflib 模糊匹配
        """
        q = query.strip().lower()

        # 1. 精确匹配触发词
        if q in self.commands:
            d = self.commands[q]
            return (d["command"], d["description"])

        # 2. 别名匹配
        if q in self.aliases:
            return (self.aliases[q], f"别名: {q}")

        # 3. 关键词包含（触发词在查询中、或查询在触发词中）+ 中文逐字匹配
        best = None
        best_score = 0
        for trigger, d in self.commands.items():
            t = trigger.lower()
            # 触发词包含查询词
            if q in t:
                score = len(q) / max(len(t), 1)
                if score > best_score:
                    best_score = score
                    best = d
            # 查询词包含触发词
            elif t in q:
                score = len(t) / max(len(q), 1)
                if score > best_score:
                    best_score = score
                    best = d
            # 空格分词交集匹配
            else:
                q_words = set(q.replace(',', ' ').replace('，', ' ').split())
                t_words = set(t.replace(',', ' ').replace('，', ' ').split())
                overlap = q_words & t_words
                if overlap:
                    score = len(overlap) / max(len(q_words), len(t_words), 1)
                    if score > best_score:
                        best_score = score
                        best = d
                # 中文逐字重叠匹配（无空格时）
                if not overlap and best_score < 0.5:
                    q_chars = set(q)
                    t_chars = set(t)
                    char_overlap = q_chars & t_chars
                    if char_overlap:
                        score = len(char_overlap) / max(len(q_chars), len(t_chars), 1) * 0.8  # 降权
                        if score > best_score:
                            best_score = score
                            best = d

        if best and best_score >= 0.3:
            return (best["command"], best["description"])

        # 4. difflib 模糊
        all_triggers = list(self.commands.keys()) + list(self.aliases.keys())
        matches = get_close_matches(q, [t.lower() for t in all_triggers], n=1, cutoff=0.6)
        if matches:
            matched = matches[0]
            if matched in self.commands:
                d = self.commands[matched]
                return (d["command"], d["description"] + " (模糊匹配)")
            elif matched in self.aliases:
                return (self.aliases[matched], f"别名(模糊): {matched}")

        return None

    def list_all(self) -> List[Tuple[str, str, str]]:
        """列出所有触发词 → 命令"""
        seen = set()
        result = []
        for trigger, cmd, desc in self.triggers:
            if trigger not in seen:
                seen.add(trigger)
                result.append((trigger, cmd, desc))
        return result

    def suggest(self, partial: str) -> List[str]:
        """自动补全建议"""
        q = partial.strip().lower()
        all_keys = list(self.commands.keys()) + list(self.aliases.keys())
        suggestions = []
        for k in all_keys:
            if q in k.lower():
                suggestions.append(k)
        if not suggestions:
            suggestions = get_close_matches(q, [k.lower() for k in all_keys], n=10, cutoff=0.4)
        return suggestions[:15]


# ============================================================
# 二、命令执行引擎
# ============================================================

class CommandRunner:
    """执行匹配到的命令"""

    def __init__(self):
        self.index = CommandIndex()
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    def execute(self, query: str, extra_args: List[str] = None, dry_run: bool = False) -> int:
        """匹配并执行命令"""
        match = self.index.match(query)

        if not match:
            print(f"❌ 未找到匹配命令: \"{query}\"")
            suggestions = self.index.suggest(query)
            if suggestions:
                print(f"💡 试试这些: {', '.join(suggestions[:8])}")
            else:
                print("📋 可用触发词:")
                for trigger, cmd, desc in self.index.list_all()[:12]:
                    print(f"   {trigger} → {desc}")
            return 1

        command, desc = match

        # 追加参数
        if extra_args:
            command = f"{command} {' '.join(extra_args)}"

        # 记录历史
        self._log(query, command, desc)

        if dry_run:
            print(f"🔍 [干运行] {desc}")
            print(f"   命令: {command}")
            return 0

        print(f"🚀 {desc}")
        print(f"   {command}")

        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=str(ROOT),
            )
            if result.returncode == 0:
                print("✅ 完成")
            else:
                print(f"⚠️ 退出码: {result.returncode}")
            return result.returncode
        except Exception as e:
            print(f"❌ 执行错误: {e}")
            return 1

    def _log(self, query: str, command: str, desc: str):
        """写入执行历史"""
        try:
            with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
                f.write(json.dumps({
                    "time": datetime.now().isoformat(),
                    "query": query,
                    "command": command,
                    "description": desc,
                }, ensure_ascii=False) + '\n')
        except Exception:
            pass

    def show_history(self, n: int = 20):
        """显示执行历史"""
        if not HISTORY_FILE.exists():
            print("📋 暂无执行历史")
            return
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines[-n:]:
            try:
                d = json.loads(line)
                print(f"  [{d.get('time','')[:16]}] {d.get('query','')} → {d.get('description','')}")
            except Exception:
                pass


# ============================================================
# 三、命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·命令自动执行引擎 v1.0\n铁律#11: 老大不记命令，AI自己挑。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh-run "健康检查"              # 自然语言执行
  lh-run "对齐复盘"              # 模糊匹配
  lh-run "采集历史" --args 7    # 带参数
  lh-run "通心译" --dry-run      # 干运行预览
  lh-run --list                  # 列出所有命令
  lh-run --complete "健"        # 自动补全
  lh-run --history               # 执行历史
        """
    )
    parser.add_argument("query", nargs="?", help="自然语言查询（干什么）")
    parser.add_argument("--args", nargs="*", default=[], help="附加参数")
    parser.add_argument("--dry-run", action="store_true", help="只预览不执行")
    parser.add_argument("--list", action="store_true", help="列出所有触发词")
    parser.add_argument("--complete", metavar="部分文字", help="自动补全建议")
    parser.add_argument("--history", action="store_true", help="执行历史")
    parser.add_argument("--index", help="查看索引文件路径")

    args = parser.parse_args()
    runner = CommandRunner()

    if args.index:
        print(f"📋 索引文件: {INDEX_PATH}")
        print(f"   存在: {'✅' if INDEX_PATH.exists() else '❌'}")
        return

    if args.list:
        print("🎯 自然语言触发词 → 命令映射\n")
        for trigger, cmd, desc in runner.index.list_all():
            print(f"  {trigger:12s} → {desc}")
            print(f"  {'':12s}   {cmd}")
        return

    if args.complete:
        suggestions = runner.index.suggest(args.complete)
        if suggestions:
            print(f"💡 \"{args.complete}\" 补全建议:")
            for s in suggestions:
                print(f"   {s}")
        else:
            print(f"无补全匹配: {args.complete}")
        return

    if args.history:
        runner.show_history()
        return

    if not args.query:
        parser.print_help()
        return

    sys.exit(runner.execute(args.query, args.args, args.dry_run))


if __name__ == "__main__":
    main()
