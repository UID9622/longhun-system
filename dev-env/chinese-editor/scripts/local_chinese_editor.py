#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂本地中文编辑器 · 闭环渲染与运行
DNA: #龍芯⚡️2026-06-26-DEVENV-LOCAL-EDITOR-v2.0

不依赖 VS Code / 浏览器，本地直接编辑、渲染和运行 CNSH / Python 文件。
"""
import argparse
import subprocess
import sys
from pathlib import Path


def run_cnsh_file(file_path: str, dry_run: bool = False) -> int:
    """调用 CNSH 本地运行时"""
    runtime = Path(__file__).parent / "cnsh_runtime.py"
    cmd = [sys.executable, str(runtime), file_path]
    if dry_run:
        cmd.append("--dry-run")
    result = subprocess.run(cmd, capture_output=False, text=True)
    return result.returncode


def render_cnsh(file_path: str) -> str:
    """渲染 CNSH 文件，高亮中文关键字"""
    p = Path(file_path)
    if not p.exists():
        return f"❌ 文件不存在: {file_path}"
    content = p.read_text(encoding="utf-8", errors="ignore")
    lines = content.splitlines()
    rendered = []
    keywords = ["函数", "如果", "否则", "循环", "返回", "打印", "整数", "字符串", "布尔", "列表"]
    for i, line in enumerate(lines, 1):
        # 高亮中文关键字
        for kw in keywords:
            line = line.replace(kw, f"\033[35m{kw}\033[0m")
        # 高亮 DNA
        if "#龍芯⚡️" in line:
            line = line.replace("#龍芯⚡️", "\033[36m#龍芯⚡️\033[0m")
        # 高亮 CONFIRM
        if "#CONFIRM" in line:
            line = line.replace("#CONFIRM", "\033[33m#CONFIRM\033[0m")
        rendered.append(f"{i:4d} │ {line}")
    return "\n".join(rendered)


def main():
    parser = argparse.ArgumentParser(description="龍魂本地中文编辑器")
    parser.add_argument("file", nargs="?", help="要打开的文件路径")
    parser.add_argument("--render", action="store_true", help="只渲染，不运行")
    parser.add_argument("--run", action="store_true", help="运行 CNSH/Python 文件")
    parser.add_argument("--dry-run", action="store_true", help="只显示翻译后的代码（仅 CNSH）")
    args = parser.parse_args()

    print("🐉 龍魂本地中文编辑器 v2.0")
    print("   闭环 · 中文 · 本地主权\n")

    if not args.file:
        print("用法:")
        print("  python3 local_chinese_editor.py <文件路径>")
        print("  python3 local_chinese_editor.py <文件路径.cnsh> --run")
        print("  python3 local_chinese_editor.py <文件路径.cnsh> --run --dry-run")
        return

    p = Path(args.file)
    if p.suffix == ".cnsh":
        if args.run:
            sys.exit(run_cnsh_file(args.file, args.dry_run))
        else:
            print(render_cnsh(args.file))
    else:
        print(render_cnsh(args.file))
        if args.run and p.suffix == ".py":
            subprocess.run([sys.executable, args.file])


if __name__ == "__main__":
    main()
