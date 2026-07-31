#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH 解释器 v1.0（完整交付版）
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-CNSH-INTERPRETER-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

功能：
  - 解析 .cnsh 脚本
  - 执行指令（打印/等待/记录）
  - 日志记录
  - 守护进程模式（自动监听 modules 目录）
  - 支持扩展（变量/条件/AI接口预留）

使用方式：
  python3 cnsh_interpreter.py                 # 交互模式
  python3 cnsh_interpreter.py --file test.cnsh # 执行文件
  python3 cnsh_interpreter.py --daemon         # 守护进程模式
"""

import os
import sys
import re
import time
import json
import hashlib
import datetime
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

# ============================================================
# 一、配置
# ============================================================

BASE = os.path.expanduser("~/longhun-system/cnsh")
MODULE_DIR = os.path.join(BASE, "modules")
LOG_DIR = os.path.join(BASE, "logs")
RUNTIME_DIR = os.path.join(BASE, "runtime")
CONFIG_DIR = os.path.join(BASE, "config")

for d in [BASE, MODULE_DIR, LOG_DIR, RUNTIME_DIR, CONFIG_DIR]:
    os.makedirs(d, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "daemon.log")
ERR_FILE = os.path.join(LOG_DIR, "error.log")
STATE_FILE = os.path.join(RUNTIME_DIR, "state.json")
LOCK_FILE = os.path.join(RUNTIME_DIR, "lock")
CONFIG_FILE = os.path.join(CONFIG_DIR, "system.json")

# ============================================================
# 二、工具函数
# ============================================================

def log(msg: str) -> None:
    """写入日志"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(f"[LOG] {msg}")

def error(msg: str) -> None:
    """写入错误日志"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ERR_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(f"[ERR] {msg}")

def save_state(data: Dict) -> None:
    """保存状态"""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_state() -> Dict:
    """加载状态"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def acquire_lock() -> bool:
    """获取文件锁"""
    if os.path.exists(LOCK_FILE):
        return False
    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))
    return True

def release_lock() -> None:
    """释放文件锁"""
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

# ============================================================
# 三、CNSH 解析器
# ============================================================

class CNSHParser:
    """CNSH 语法解析器"""

    @staticmethod
    def parse(content: str) -> List[Tuple[str, Any]]:
        """
        解析 CNSH 脚本
        返回指令列表: [(cmd, value), ...]
        """
        instructions = []
        lines = content.strip().split('\n')

        for line in lines:
            line = line.strip()

            if not line or line.startswith('#'):
                continue

            # @任务 开始/结束 - 任务标记
            if line.startswith('@任务'):
                instructions.append(('task', line))

            # 打印 "内容"
            elif line.startswith('打印'):
                match = re.search(r'"(.*?)"', line)
                if match:
                    instructions.append(('print', match.group(1)))
                else:
                    instructions.append(('print', line.replace('打印', '').strip()))

            # 等待 N (秒)
            elif line.startswith('等待'):
                try:
                    num = int(re.search(r'\d+', line).group())
                    instructions.append(('sleep', num))
                except:
                    instructions.append(('sleep', 1))

            # 记录 "内容"
            elif line.startswith('记录'):
                match = re.search(r'"(.*?)"', line)
                if match:
                    instructions.append(('log', match.group(1)))
                else:
                    instructions.append(('log', line.replace('记录', '').strip()))

            # 设 变量 = 值 - 变量设置
            elif line.startswith('设'):
                parts = line.replace('设', '').strip().split('=', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    instructions.append(('set', (key, value)))

            # 如果 条件 - 条件判断
            elif line.startswith('如果'):
                condition = line.replace('如果', '').strip()
                # 收集条件块
                block_lines = []
                # 这里简化处理：假设结束在下一行
                # 实际实现需要递归解析
                instructions.append(('if', condition))

            # 理解 "内容" - AI理解
            elif line.startswith('理解'):
                match = re.search(r'"(.*?)"', line)
                if match:
                    instructions.append(('ai', match.group(1)))
                else:
                    instructions.append(('ai', line.replace('理解', '').strip()))

        return instructions

# ============================================================
# 四、CNSH 执行器
# ============================================================

class CNSHExecutor:
    """CNSH 指令执行器"""

    def __init__(self):
        self.vars: Dict[str, str] = {}
        self.output_lines: List[str] = []
        self.logs: List[str] = []

    def execute(self, instructions: List[Tuple[str, Any]]) -> str:
        """
        执行指令列表
        返回执行输出
        """
        for cmd, val in instructions:
            if cmd == 'print':
                # 检查是否为变量
                if isinstance(val, str) and val in self.vars:
                    val = self.vars[val]
                output = f"[输出] {val}"
                self.output_lines.append(output)
                print(output)
                log(output)

            elif cmd == 'sleep':
                time.sleep(val)
                log(f"[等待] {val}秒")

            elif cmd == 'log':
                msg = f"[记录] {val}"
                self.logs.append(msg)
                print(msg)
                log(msg)

            elif cmd == 'set':
                key, value = val
                self.vars[key] = value
                log(f"[变量] {key} = {value}")

            elif cmd == 'if':
                # 条件判断（预留）
                log(f"[条件] {val}")

            elif cmd == 'ai':
                # AI接口（预留）
                result = f"[AI理解] {val}"
                self.output_lines.append(result)
                print(result)
                log(result)

            elif cmd == 'task':
                log(f"[任务] {val}")

        return '\n'.join(self.output_lines)

# ============================================================
# 五、CNSH 解释器核心
# ============================================================

class CNSHInterpreter:
    """CNSH 主解释器"""

    @staticmethod
    def run_file(file_path: str) -> Tuple[str, bool]:
        """
        运行 CNSH 文件
        返回: (输出内容, 是否成功)
        """
        try:
            if not os.path.exists(file_path):
                error(f"文件不存在: {file_path}")
                return f"[错误] 文件不存在: {file_path}", False

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            log(f"[执行] {file_path}")

            # 解析
            parser = CNSHParser()
            instructions = parser.parse(content)

            if not instructions:
                msg = "[提示] 无有效指令"
                print(msg)
                log(msg)
                return msg, True

            # 执行
            executor = CNSHExecutor()
            output = executor.execute(instructions)

            # 保存状态
            save_state({
                "last_file": file_path,
                "last_run": datetime.datetime.now().isoformat(),
                "instructions_count": len(instructions),
                "vars": executor.vars
            })

            log(f"[完成] {file_path}")
            return output, True

        except Exception as e:
            error(f"[错误] {e}")
            return f"[错误] {e}", False

    @staticmethod
    def run_script(content: str) -> str:
        """运行 CNSH 脚本内容"""
        parser = CNSHParser()
        instructions = parser.parse(content)

        if not instructions:
            return "[提示] 无有效指令"

        executor = CNSHExecutor()
        return executor.execute(instructions)

    @staticmethod
    def interactive():
        """交互模式"""
        print("\n" + "=" * 60)
        print("🐉 CNSH 解释器 v1.0 - 交互模式")
        print("=" * 60)
        print("输入 CNSH 代码，按回车执行")
        print("输入 'exit' 退出")
        print("输入 'demo' 运行示例")
        print("输入 'clear' 清屏")
        print("-" * 60)

        while True:
            try:
                user_input = input("\nCNSH> ").strip()
                if not user_input:
                    continue

                if user_input.lower() in ['exit', 'quit']:
                    print("👋 龙魂永存")
                    break

                if user_input.lower() == 'clear':
                    os.system('clear' if os.name == 'posix' else 'cls')
                    continue

                if user_input.lower() == 'demo':
                    demo = '''
@任务 开始
打印 "系统启动成功"
等待 1
记录 "第一阶段完成"
打印 "继续执行..."
等待 1
记录 "全部完成"
@任务 结束
'''
                    print(CNSHInterpreter.run_script(demo))
                    continue

                # 执行输入的代码
                output = CNSHInterpreter.run_script(user_input)
                print(output)

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ 错误: {e}")

# ============================================================
# 六、守护进程
# ============================================================

class CNSHDaemon:
    """CNSH 守护进程"""

    def __init__(self):
        self.seen_files: set = set()
        self.running = True

    def watch(self):
        """监听 modules 目录"""
        log("[SYS-ETA] 守护进程启动")
        log(f"[监听] {MODULE_DIR}")

        # 初始化状态
        state = load_state()
        self.seen_files = set(state.get("seen_files", []))

        while self.running:
            try:
                # 获取文件锁
                if not acquire_lock():
                    error("[锁] 另一个实例正在运行")
                    time.sleep(2)
                    continue

                # 扫描目录
                if os.path.exists(MODULE_DIR):
                    files = os.listdir(MODULE_DIR)

                    for f in files:
                        if f.endswith(".cnsh"):
                            full_path = os.path.join(MODULE_DIR, f)

                            # 检查是否已处理
                            if f not in self.seen_files:
                                self.seen_files.add(f)
                                log(f"[发现] {f}")
                                CNSHInterpreter.run_file(full_path)

                # 保存状态
                save_state({
                    "seen_files": list(self.seen_files),
                    "last_scan": datetime.datetime.now().isoformat()
                })

                # 释放锁
                release_lock()

            except Exception as e:
                error(f"[守护进程错误] {e}")

            time.sleep(2)

    def stop(self):
        """停止守护进程"""
        self.running = False
        log("[SYS-ETA] 守护进程停止")

# ============================================================
# 七、命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 CNSH 解释器 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 交互模式
  python3 cnsh_interpreter.py --interactive

  # 执行文件
  python3 cnsh_interpreter.py --file test.cnsh

  # 守护进程模式
  python3 cnsh_interpreter.py --daemon

  # 创建示例文件
  python3 cnsh_interpreter.py --create-demo
        """
    )

    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--file", "-f", type=str, help="执行 CNSH 文件")
    parser.add_argument("--daemon", "-d", action="store_true", help="守护进程模式")
    parser.add_argument("--create-demo", action="store_true", help="创建示例文件")
    parser.add_argument("--code", "-c", type=str, help="直接执行 CNSH 代码")

    args = parser.parse_args()

    # 创建示例文件
    if args.create_demo:
        demo_path = os.path.join(MODULE_DIR, "demo.cnsh")
        demo_content = '''@任务 开始

打印 "系统启动成功"
等待 1
记录 "第一阶段完成"

打印 "继续执行..."
等待 1
记录 "全部完成"

@任务 结束
'''
        with open(demo_path, 'w', encoding='utf-8') as f:
            f.write(demo_content)
        print(f"✅ 示例文件已创建: {demo_path}")
        return

    # 交互模式
    if args.interactive:
        CNSHInterpreter.interactive()
        return

    # 执行代码
    if args.code:
        output = CNSHInterpreter.run_script(args.code)
        print(output)
        return

    # 执行文件
    if args.file:
        output, success = CNSHInterpreter.run_file(args.file)
        print(output)
        sys.exit(0 if success else 1)

    # 守护进程模式
    if args.daemon:
        daemon = CNSHDaemon()
        try:
            daemon.watch()
        except KeyboardInterrupt:
            print("\n🛑 守护进程已停止")
            daemon.stop()
        return

    # 无参数，显示帮助
    parser.print_help()


if __name__ == "__main__":
    main()
