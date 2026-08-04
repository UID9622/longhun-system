#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 CNSH -> iOS 原生UI（SwiftUI版）· Python本地测试版
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-CNSH-iOS-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

定位：在Mac上运行CNSH解释器的Python版本，与iOS版逻辑一致
功能：
  - 解析.cnsh脚本
  - 执行 设/打印/理解 指令
  - 维护运行时变量
  - 支持本地文件执行
  - 交互式命令行

iOS原生版已完整落地，本脚本用于本地调试和验证。
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field

# ============================================================
# 一、运行时（对应 CNSHRuntime.swift）
# ============================================================

class CNSHRuntime:
    """CNSH运行时 - 维护变量环境"""
    
    def __init__(self):
        self.vars: Dict[str, str] = {}
    
    def set(self, key: str, value: str) -> None:
        """设置变量"""
        self.vars[key] = value
    
    def get(self, key: str) -> str:
        """获取变量"""
        return self.vars.get(key, "")
    
    def get_all(self) -> Dict[str, str]:
        """获取所有变量"""
        return self.vars.copy()


# ============================================================
# 二、AI接口（对应 CNSHAI.swift）
# ============================================================

class CNSHAI:
    """CNSH AI接口"""
    
    @staticmethod
    def ask(prompt: str, use_real_ai: bool = False) -> str:
        """
        AI理解接口
        可替换为真实API调用
        """
        if use_real_ai:
            # 这里可接入真实AI API
            return f"[AI真实理解] {prompt}"
        else:
            # 本地模拟
            return f"[AI理解] {prompt}"


# ============================================================
# 三、解析器（对应 CNSHParser.swift）
# ============================================================

class CNSHParser:
    """CNSH脚本解析器"""
    
    @staticmethod
    def parse(content: str) -> List[List[str]]:
        """
        解析CNSH脚本
        返回指令列表: [[cmd, arg1, arg2, ...], ...]
        """
        instructions = []
        lines = content.split('\n')
        
        for line in lines:
            trimmed = line.strip()
            
            # 跳过空行和注释
            if not trimmed or trimmed.startswith('#'):
                continue
            
            # 设 变量 = 值
            if trimmed.startswith('设'):
                # 支持 设 名字 = "值" 或 设 名字 = 值
                parts = trimmed[1:].strip().split('=', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    # 去除引号
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    instructions.append(['set', key, value])
                else:
                    # 尝试匹配 设 名字 = 值 但可能有空格
                    match = re.match(r'设\s+(\S+)\s*=\s*(.+)', trimmed)
                    if match:
                        key = match.group(1).strip()
                        value = match.group(2).strip()
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        instructions.append(['set', key, value])
            
            # 打印 内容
            elif trimmed.startswith('打印'):
                value = trimmed[2:].strip()
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                instructions.append(['print', value])
            
            # 理解 "内容"
            elif trimmed.startswith('理解'):
                value = trimmed[2:].strip()
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                instructions.append(['ai', value])
            
            # @任务 开始 / @任务 结束 (CNSH任务标记)
            elif trimmed.startswith('@任务'):
                instructions.append(['task_marker', trimmed])
            
            # 其他指令（可扩展）
            elif trimmed.startswith('执行'):
                value = trimmed[2:].strip()
                instructions.append(['exec', value])
        
        return instructions


# ============================================================
# 四、执行器（对应 CNSHExecutor.swift）
# ============================================================

class CNSHExecutor:
    """CNSH指令执行器"""
    
    @staticmethod
    def execute(instructions: List[List[str]], runtime: CNSHRuntime, 
                use_real_ai: bool = False) -> Tuple[str, List[str]]:
        """
        执行指令列表
        返回: (输出文本, 执行日志)
        """
        output_lines = []
        logs = []
        task_active = False
        
        for inst in instructions:
            cmd = inst[0]
            
            if cmd == 'set':
                key = inst[1]
                value = inst[2]
                runtime.set(key, value)
                logs.append(f"变量设置: {key} = {value}")
            
            elif cmd == 'print':
                val = inst[1]
                # 检查是否为变量
                if val in runtime.get_all():
                    val = runtime.get(val)
                output_lines.append(f"[输出] {val}")
                logs.append(f"打印: {val}")
            
            elif cmd == 'ai':
                prompt = inst[1]
                result = CNSHAI.ask(prompt, use_real_ai)
                runtime.set("AI结果", result)
                output_lines.append(result)
                logs.append(f"AI理解: {prompt} -> {result}")
            
            elif cmd == 'exec':
                # 执行外部指令（可扩展）
                output_lines.append(f"[执行] {inst[1]}")
                logs.append(f"执行: {inst[1]}")
            
            elif cmd == 'task_marker':
                marker = inst[1]
                if '开始' in marker:
                    task_active = True
                    logs.append(f"任务开始: {marker}")
                elif '结束' in marker:
                    task_active = False
                    logs.append(f"任务结束: {marker}")
            
            elif cmd == 'eval':
                # 计算表达式（可扩展）
                try:
                    result = str(eval(inst[1], {}, runtime.get_all()))
                    output_lines.append(f"[计算] {result}")
                    logs.append(f"计算: {inst[1]} = {result}")
                except:
                    output_lines.append(f"[计算] 错误: {inst[1]}")
                    logs.append(f"计算错误: {inst[1]}")
        
        return '\n'.join(output_lines), logs


# ============================================================
# 五、主解释器（对应 CNSHInterpreter.swift）
# ============================================================

class CNSHInterpreter:
    """CNSH主解释器"""
    
    @staticmethod
    def run_file(file_path: str, use_real_ai: bool = False) -> Tuple[str, List[str]]:
        """运行CNSH文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return CNSHInterpreter.run_script(content, use_real_ai)
        except FileNotFoundError:
            return f"[错误] 文件不存在: {file_path}", []
        except Exception as e:
            return f"[错误] {e}", []
    
    @staticmethod
    def run_script(content: str, use_real_ai: bool = False) -> Tuple[str, List[str]]:
        """运行CNSH脚本内容"""
        runtime = CNSHRuntime()
        instructions = CNSHParser.parse(content)
        
        if not instructions:
            return "[提示] 无有效指令", []
        
        return CNSHExecutor.execute(instructions, runtime, use_real_ai)


# ============================================================
# 六、命令行接口
# ============================================================

def interactive_mode():
    """交互式模式"""
    print("\n" + "=" * 60)
    print("🐉 CNSH 控制台 (iOS本地测试版)")
    print("=" * 60)
    print("输入 CNSH 代码，按回车执行")
    print("输入 'exit' 退出")
    print("输入 'file <路径>' 运行文件")
    print("输入 'demo' 运行示例")
    print("-" * 60)
    
    runtime = CNSHRuntime()
    
    while True:
        try:
            user_input = input("\nCNSH> ").strip()
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit']:
                print("👋 龙魂永存")
                break
            
            if user_input.startswith('file '):
                file_path = user_input[5:].strip()
                output, logs = CNSHInterpreter.run_file(file_path)
                print(output)
                continue
            
            if user_input.lower() == 'demo':
                demo = '''
设 名字 = "[U-GAMMA]"
打印 名字
理解 "换一种表达方式"
打印 AI结果
'''
                output, logs = CNSHInterpreter.run_script(demo)
                print(output)
                continue
            
            # 直接执行输入的CNSH代码
            output, logs = CNSHInterpreter.run_script(user_input)
            print(output)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ 错误: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="🐉 CNSH -> iOS 原生UI（SwiftUI版）· Python本地测试",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 交互模式（推荐）
  python3 cnsh_ios_test.py --interactive

  # 运行CNSH文件
  python3 cnsh_ios_test.py demo.cnsh

  # 直接执行CNSH代码
  python3 cnsh_ios_test.py --code '设 名字 = "龙魂" 打印 名字'

  # 使用真实AI（需配置）
  python3 cnsh_ios_test.py demo.cnsh --ai
        """
    )
    
    parser.add_argument("file", nargs="?", help="CNSH脚本文件路径")
    parser.add_argument("--code", "-c", type=str, help="直接执行CNSH代码")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--ai", "-a", action="store_true", help="启用真实AI接口")
    parser.add_argument("--json", "-j", action="store_true", help="JSON格式输出")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
        return
    
    if args.code:
        output, logs = CNSHInterpreter.run_script(args.code, args.ai)
        if args.json:
            print(json.dumps({
                "output": output,
                "logs": logs
            }, ensure_ascii=False, indent=2))
        else:
            print(output)
        return
    
    if args.file:
        output, logs = CNSHInterpreter.run_file(args.file, args.ai)
        if args.json:
            print(json.dumps({
                "output": output,
                "logs": logs
            }, ensure_ascii=False, indent=2))
        else:
            print(output)
        return
    
    # 无参数，显示帮助
    print(__doc__)


if __name__ == "__main__":
    main()
