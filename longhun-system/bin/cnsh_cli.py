#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH语言终端 · LU-ORIGIN-FULLSYNC
DNA: #龍芯⚡️2026-04-08-CNSH-CLI-v1.0

接入cnsh-compiler.js，提供CNSH编译执行环境
"""

import subprocess
import sys
import json
from pathlib import Path

CNSH_DIR = Path.home() / "longhun-system" / "cnsh语言"
COMPILER = CNSH_DIR / "cnsh-compiler.js"

def compile_cnsh(source_file):
    """编译CNSH文件为C代码"""
    if not COMPILER.exists():
        return {"error": "编译器不存在"}
    
    try:
        result = subprocess.run(
            ["node", str(COMPILER), str(source_file)],
            capture_output=True,
            text=True,
            cwd=CNSH_DIR
        )
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.stderr else None
        }
    except Exception as e:
        return {"error": str(e)}

def main():
    print("☰☰ 龍🇨🇳魂 ☷ · CNSH语言终端")
    print("DNA: #龍芯⚡️2026-04-08-CNSH-CLI-v1.0")
    print("")
    
    if len(sys.argv) < 2:
        print("用法: python3 cnsh_cli.py <文件.cnsh>")
        print("")
        print("示例文件:")
        for f in CNSH_DIR.glob("*.cnsh"):
            print(f"  - {f.name}")
        return
    
    source = Path(sys.argv[1])
    if not source.exists():
        print(f"❌ 文件不存在: {source}")
        return
    
    print(f"正在编译: {source.name}")
    print("-" * 40)
    
    result = compile_cnsh(source)
    
    if result.get("success"):
        print("✅ 编译成功")
        if result.get("output"):
            print(result["output"])
    else:
        print("❌ 编译失败")
        if result.get("error"):
            print(result["error"])

if __name__ == "__main__":
    main()
