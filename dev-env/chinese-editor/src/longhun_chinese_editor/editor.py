#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂本地中文编辑器 · 闭环渲染与运行
DNA: #龍芯⚡️2026-06-26-LONGHUN-LOCAL-EDITOR-v2.1

不依赖 VS Code / 浏览器，本地直接编辑、渲染和运行 CNSH / Python 文件。
"""
import subprocess
import sys
from pathlib import Path

from .runtime import run_cnsh


KEYWORDS = [
    "函数",
    "如果",
    "否则如果",
    "否则",
    "循环",
    "当",
    "对于",
    "在",
    "范围",
    "返回",
    "打印",
    "整数",
    "小数",
    "文本",
    "真假",
    "列表",
    "字典",
    "真",
    "假",
    "空",
    "字符串",
    "布尔",
]


def render_cnsh(file_path: str) -> str:
    """渲染 CNSH 文件，高亮中文关键字"""
    p = Path(file_path)
    if not p.exists():
        return f"❌ 文件不存在: {file_path}"
    content = p.read_text(encoding="utf-8", errors="ignore")
    lines = content.splitlines()
    rendered = []
    for i, line in enumerate(lines, 1):
        for kw in sorted(KEYWORDS, key=len, reverse=True):
            line = line.replace(kw, f"\033[35m{kw}\033[0m")
        if "#龍芯⚡️" in line:
            line = line.replace("#龍芯⚡️", "\033[36m#龍芯⚡️\033[0m")
        if "#CONFIRM" in line:
            line = line.replace("#CONFIRM", "\033[33m#CONFIRM\033[0m")
        rendered.append(f"{i:4d} │ {line}")
    return "\n".join(rendered)


def run_cnsh_file(file_path: str, dry_run: bool = False, use_compiler: bool = True) -> int:
    """调用 CNSH 本地运行时（直接函数调用，不依赖子进程路径）"""
    return run_cnsh(file_path, dry_run=dry_run, use_compiler=use_compiler)


def run_python_file(file_path: str) -> int:
    """直接运行 Python 文件"""
    result = subprocess.run([sys.executable, file_path])
    return result.returncode


def editor_main():
    """本地中文编辑器入口（无参数解析，由 cli.py 调用）"""
    pass
