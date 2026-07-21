#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂中文编辑开发环境 · 命令行入口
DNA: #龍芯⚡️2026-06-26-LONGHUN-CHINESE-EDITOR-CLI-v1.0
"""
import argparse
import sys
from pathlib import Path

from . import __dna__, __version__
from .compiler.lexer import Lexer, LexerError
from .compiler.pipeline import compile_cnsh_safe
from .editor import render_cnsh, run_cnsh_file, run_python_file
from .repl import repl_loop
from .runtime import run_cnsh


def _cmd_run(args):
    if not args.file.endswith(".cnsh"):
        print("⚠️  请提供 .cnsh 文件")
        sys.exit(1)
    use_compiler = not getattr(args, "legacy", False)
    sys.exit(run_cnsh(args.file, dry_run=args.dry_run, use_compiler=use_compiler))


def _cmd_compile(args):
    p = Path(args.file)
    if not p.exists() or p.suffix != ".cnsh":
        print("⚠️  请提供有效的 .cnsh 文件")
        sys.exit(1)
    source = p.read_text(encoding="utf-8", errors="ignore")
    ok, result, err_type = compile_cnsh_safe(source, include_main_guard=True)
    if not ok:
        print(f"❌ 编译失败 ({err_type}): {result}")
        sys.exit(1)
    if args.output:
        out = Path(args.output)
        out.write_text(result, encoding="utf-8")
        print(f"✅ 已生成 Python 文件: {out}")
    else:
        print(result)
    sys.exit(0)


def _cmd_tokenize(args):
    p = Path(args.file)
    if not p.exists():
        print(f"❌ 文件不存在: {p}")
        sys.exit(1)
    source = p.read_text(encoding="utf-8", errors="ignore")
    try:
        tokens = Lexer(source).tokenize()
    except LexerError as e:
        print(f"❌ 词法错误: {e}")
        sys.exit(1)
    print(f"{'#':>4} {'类型':<16} {'值':<24} 位置")
    print("-" * 60)
    for i, tok in enumerate(tokens):
        val = tok.value
        if tok.type.name == "NEWLINE":
            val = "\\n"
        elif tok.type.name == "EOF":
            val = "EOF"
        print(f"{i:4d} {tok.type.name:<16} {val[:22]!r:<24} L{tok.line}:{tok.col}")
    print("-" * 60)
    print(f"总计: {len(tokens)} 个 token")
    sys.exit(0)


def _cmd_version(args):
    print(f"longhun-chinese-editor v{__version__}")
    print(f"DNA: {__dna__}")
    sys.exit(0)


def _cmd_repl(args):
    sys.exit(repl_loop())


def _cmd_editor(args):
    if getattr(args, "repl", False):
        return repl_loop()

    print("🐉 龍魂本地中文编辑器")
    print(f"   版本: {__version__}  {__dna__}\n")

    if not args.file:
        print("用法:")
        print("  longhun-editor <文件路径>")
        print("  longhun-editor <文件路径.cnsh> --run")
        print("  longhun-editor <文件路径.cnsh> --run --dry-run")
        print("  longhun-editor --repl")
        sys.exit(0)

    use_compiler = not getattr(args, "legacy", False)
    p = Path(args.file)
    if p.suffix == ".cnsh":
        if args.run:
            sys.exit(run_cnsh_file(args.file, dry_run=args.dry_run, use_compiler=use_compiler))
        else:
            print(render_cnsh(args.file))
    else:
        print(render_cnsh(args.file))
        if args.run and p.suffix == ".py":
            sys.exit(run_python_file(args.file))


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="longhun-chinese-editor",
        description="龍魂中文编辑开发环境 CLI",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    subparsers = parser.add_subparsers(dest="command", required=False)

    run_parser = subparsers.add_parser("run", help="运行 CNSH 脚本")
    run_parser.add_argument("file", help="CNSH 脚本路径")
    run_parser.add_argument(
        "--dry-run", action="store_true", help="只输出翻译后的 Python 代码"
    )
    mode_group = run_parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--compiler", action="store_true", default=True,
        help="使用完整 CNSH 编译器（默认）"
    )
    mode_group.add_argument(
        "--legacy", action="store_true",
        help="使用正则翻译器（兼容模式）"
    )
    run_parser.set_defaults(func=_cmd_run)

    compile_parser = subparsers.add_parser("compile", help="将 CNSH 编译为 Python")
    compile_parser.add_argument("file", help="CNSH 脚本路径")
    compile_parser.add_argument("-o", "--output", help="输出 .py 文件路径（可选）")
    compile_parser.set_defaults(func=_cmd_compile)

    repl_parser = subparsers.add_parser("repl", help="启动 CNSH 交互式解释器")
    repl_parser.set_defaults(func=_cmd_repl)

    tokenize_parser = subparsers.add_parser("tokenize", help="显示 CNSH 分词结果")
    tokenize_parser.add_argument("file", help="CNSH 源文件路径")
    tokenize_parser.set_defaults(func=_cmd_tokenize)

    version_parser = subparsers.add_parser("version", help="显示版本信息")
    version_parser.set_defaults(func=_cmd_version)

    editor_parser = subparsers.add_parser("editor", help="启动本地中文编辑器")
    editor_parser.add_argument("file", nargs="?", help="要打开的文件路径")
    editor_parser.add_argument(
        "--run", action="store_true", help="同时运行文件"
    )
    editor_parser.add_argument(
        "--dry-run", action="store_true", help="只显示翻译后的代码（仅 CNSH）"
    )
    editor_parser.add_argument(
        "--repl", action="store_true", help="启动 CNSH 交互式解释器"
    )
    editor_mode = editor_parser.add_mutually_exclusive_group()
    editor_mode.add_argument(
        "--compiler", action="store_true", default=True,
        help="使用完整 CNSH 编译器（默认）"
    )
    editor_mode.add_argument(
        "--legacy", action="store_true",
        help="使用正则翻译器（兼容模式）"
    )
    editor_parser.set_defaults(func=_cmd_editor)

    args = parser.parse_args(argv)
    if args.command is None:
        # 无子命令时默认进入 editor 模式
        file_arg = argv[0] if argv else None
        args = argparse.Namespace(
            command="editor",
            file=file_arg,
            run=False,
            dry_run=False,
            legacy=False,
        )
    args.func(args)


def editor_main(argv=None):
    """longhun-editor 入口：无需子命令即可打开文件"""
    if argv is None:
        argv = sys.argv[1:]
    # --version / --help 属于顶层解析器
    if argv and argv[0] in ("--version", "-h", "--help"):
        main(argv)
    else:
        main(["editor"] + argv)


if __name__ == "__main__":
    main()
