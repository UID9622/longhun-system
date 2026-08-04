#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-RUYI-COMMANDER-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
CNSH·如意 命令行指挥官 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-RUYI-COMMANDER-v1.0

一键执行如意指令的CLI工具。

用法:
  python3 bin/lh_ruyi_commander.py "定义 任务 \"生成登录页\" 则 CodeBuddy 生成 前端页面"
  python3 bin/lh_ruyi_commander.py --file my_task.cnsh
  python3 bin/lh_ruyi_commander.py --interactive

🐉 心意所指·万物皆成
"""

import os
import sys
import json
import argparse
from pathlib import Path

# 路径设置
_PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_DIR))
sys.path.insert(0, str(_PROJECT_DIR / "engines"))

from lh_ruyi_parser import parse_ruyi_command
from lh_ruyi_router import RuyiRouter, RuyiExecutionReport
from lh_ruyi_migration import RuyiMigrationEngine, migrate_code


def print_banner():
    print(r"""
    ╔══════════════════════════════════════════╗
    ║     🐉 CNSH·如意 命令行指挥官 v1.0       ║
    ║     心意所指 · 万物皆成                  ║
    ╚══════════════════════════════════════════╝
    """)


def execute_single(command: str, work_dir: Path = None):
    """执行单条CNSH指令"""
    router = RuyiRouter(work_dir=work_dir or _PROJECT_DIR)
    ctx = router.load_memory()

    print(f"记忆加载: {'✅ 已加载' if ctx.loaded else '⚠️ 离线模式'}")
    print()

    task = parse_ruyi_command(command)
    report = router.route(task)

    print(f"\n{'='*60}")
    print(f"📊 执行报告")
    print(f"{'='*60}")
    print(f"  DNA:    {report.dna}")
    print(f"  任务:   {task.task_name}")
    print(f"  审计:   {report.audit_mark}")
    print(f"  状态:   {report.status}")
    print(f"  耗时:   {report.duration_ms:.0f}ms")

    for i, r in enumerate(report.route_results):
        icon = "✅" if r.get("success") else "❌"
        print(f"  路由{i+1}: {icon} {r.get('target_ai')} → {r.get('action')}")

    return report


def execute_file(filepath: str, work_dir: Path = None):
    """执行.cnsh文件中的所有指令"""
    path = Path(filepath)
    if not path.exists():
        print(f"❌ 文件不存在: {filepath}")
        return

    content = path.read_text(encoding="utf-8")

    # 按空行分割多条指令
    commands = [c.strip() for c in content.split("\n\n") if c.strip()]

    print(f"📄 从文件加载了 {len(commands)} 条指令\n")

    for i, cmd in enumerate(commands, 1):
        print(f"\n{'─'*60}")
        print(f"  指令 {i}/{len(commands)}")
        print(f"{'─'*60}")
        try:
            execute_single(cmd, work_dir)
        except Exception as e:
            print(f"  ❌ 执行失败: {e}")


def interactive_mode(work_dir: Path = None):
    """交互式REPL模式"""
    router = RuyiRouter(work_dir=work_dir or _PROJECT_DIR)
    ctx = router.load_memory()

    print_banner()
    print("输入CNSH指令，空行结束一条指令，输入 'quit' 退出。")
    print("输入 'help' 查看语法帮助。")
    print(f"记忆: {'✅' if ctx.loaded else '⚠️ 离线'}")
    print()

    buffer = []
    while True:
        try:
            prompt = "如意> " if not buffer else "    | "
            line = input(prompt)

            if line.strip().lower() in ('quit', 'exit', 'q'):
                print("\n👋 如意退下，随时待命。")
                break

            if line.strip().lower() == 'help':
                print("""
CNSH·如意 语法:
  定义 任务 "名称"
  设 属性 为 值
  则 AI角色 动作 目标
  最后 转移 至 平台 动作

AI角色: CodeBuddy / Kimi / 华云道
动作: 生成 / 优化 / 检测 / 转移 / 渲染 / 修复 / 搭建

快捷键: Ctrl+D 或输入 'quit' 退出
                """)
                continue

            if line.strip() == '':
                if buffer:
                    cmd = '\n'.join(buffer)
                    buffer = []
                    try:
                        execute_single(cmd, work_dir)
                    except Exception as e:
                        print(f"❌ {e}")
                    print()
                continue

            buffer.append(line)

        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 如意退下。")
            break


def main():
    parser = argparse.ArgumentParser(
        description="CNSH·如意 命令行指挥官",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "定义 任务 \\"登录页\\" 则 CodeBuddy 生成 前端"
  %(prog)s --file my_tasks.cnsh
  %(prog)s --interactive
  %(prog)s --migrate example.py --from python --to javascript
        """
    )

    parser.add_argument("command", nargs="?", help="CNSH·如意指令文本")
    parser.add_argument("--file", "-f", help="从文件加载指令")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--migrate", "-m", help="代码迁移: 指定源文件")
    parser.add_argument("--from", dest="from_lang", default="python", help="源语言 (默认python)")
    parser.add_argument("--to", dest="to_lang", default="javascript", help="目标语言 (默认javascript)")
    parser.add_argument("--work-dir", "-w", help="工作目录")

    args = parser.parse_args()
    work_dir = Path(args.work_dir) if args.work_dir else _PROJECT_DIR

    if args.migrate:
        # 代码迁移模式
        source_file = Path(args.migrate)
        if not source_file.exists():
            print(f"❌ 文件不存在: {args.migrate}")
            sys.exit(1)

        code = source_file.read_text(encoding="utf-8")
        report = migrate_code(
            code,
            source_lang=args.from_lang,
            target_lang=args.to_lang,
            source_path=str(source_file),
            target_path=str(source_file.with_suffix(f".{args.to_lang[:2]}")),
        )

        print(report.to_markdown())
        return

    if args.interactive:
        interactive_mode(work_dir)
        return

    if args.file:
        execute_file(args.file, work_dir)
        return

    if args.command:
        execute_single(args.command, work_dir)
        return

    # 无参数 → 进入交互模式
    interactive_mode(work_dir)


if __name__ == "__main__":
    main()
