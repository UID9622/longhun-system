#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
☰☰ 龍🇨🇳魂 ☷ · 工具箱统一入口
DNA: #龍芯⚡️2026-04-08-TOOLBOX-v1.0

50+工具脚本统一调用
"""

import os
import sys
import subprocess
from pathlib import Path

BASE = Path.home() / "longhun-system"
BIN = BASE / "bin"

TOOLS = {
    "1": ("算法数据库", "algo_db.py", "查询9族算法"),
    "2": ("伏羲太极引擎", "fuxi_taiji_engine.py", "推演+归位+根显"),
    "3": ("人格路由器", "persona_router.py", "信号词匹配人格"),
    "4": ("CNSH终端", "cnsh_terminal.py", "中文命令行"),
    "5": ("自动审计", "auto_audit.py", "自动三色审计"),
    "6": ("情绪时间线", "emotion_timeline.py", "情绪分析"),
    "7": ("赋能引擎", "empower_engine.py", "关键字赋能"),
    "8": ("DNA分类器", "dna_classifier.py", "DNA分级"),
    "9": ("数据主权", "data_sovereignty.py", "主权保护"),
    "10": ("API检测", "api_check.sh", "联动状态检测"),
    "11": ("健康检查", "auto_health.sh", "系统自检"),
    "12": ("归档会话", "archive_session.sh", "会话归档"),
    "0": ("退出", None, None)
}

def show_menu():
    print("\n" + "="*50)
    print("    ☰☰ 龍🇨🇳魂 ☷ · 工具箱")
    print("="*50)
    
    for key, (name, file, desc) in sorted(TOOLS.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 99):
        if key == "0":
            print(f"\n    [{key}] {name}")
        else:
            print(f"    [{key}] {name:<12} - {desc}")
    
    print("="*50)

def run_tool(choice):
    if choice not in TOOLS:
        print("❌ 无效选择")
        return
    
    name, file, desc = TOOLS[choice]
    
    if choice == "0":
        print("龍魂永在")
        sys.exit(0)
    
    tool_path = BIN / file
    if not tool_path.exists():
        print(f"❌ 工具不存在: {file}")
        return
    
    print(f"\n🚀 启动: {name}")
    print("-"*50)
    
    try:
        if file.endswith('.py'):
            subprocess.run([sys.executable, str(tool_path)], cwd=BASE)
        elif file.endswith('.sh'):
            subprocess.run(['bash', str(tool_path)], cwd=BASE)
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断")
    
    print("-"*50)
    input("\n按回车返回工具箱...")

def main():
    while True:
        show_menu()
        choice = input("\n选择工具 [0-12]: ").strip()
        run_tool(choice)

if __name__ == "__main__":
    main()
