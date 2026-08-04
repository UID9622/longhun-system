#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
CNSH v2.1 CLI 工具链
DNA: #龍芯⚡️2026-06-29-CNSH-TOOLCHAIN-v2.1

子命令：
- cnsh run <file>
- cnsh compile <file> --target <python|js|rust|c> -o <out>
- cnsh test [path]
- cnsh init <name>
- cnsh publish
- cnsh lsp --stdio
"""
import argparse
import io
import json
import subprocess
import sys
import unittest
import zipfile
from pathlib import Path
from typing import List

from . import run_source, compile_source
from .errors import CNSHError
from .lsp_server import LspServer
from .project import CNSHProject, DEFAULT_CONFIG


__version__ = "2.1.0"


def _read_file(path: Path) -> str:
    if not path.exists():
        raise CNSHError(f"文件不存在: {path}")
    return path.read_text(encoding="utf-8")


def cmd_run(args):
    source = _read_file(Path(args.file))
    result = run_source(
        source,
        file=str(args.file),
        optimize_level=args.optimize,
        strict_types=args.strict_types,
    )
    print(f"✅ 执行完成，返回值: {result!r}")


def cmd_compile(args):
    source = _read_file(Path(args.file))
    code = compile_source(
        source,
        target=args.target,
        file=str(args.file),
        optimize_level=args.optimize,
        strict_types=args.strict_types,
    )
    if args.output:
        Path(args.output).write_text(code, encoding="utf-8")
        print(f"✅ 已编译到: {args.output}")
    else:
        print(code)


def cmd_test(args):
    path = Path(args.path) if args.path else Path("tests")
    if path.is_file():
        suite = unittest.defaultTestLoader.discover(
            str(path.parent), pattern=path.name, top_level_dir=str(path.parent)
        )
    else:
        top = path.parent if path.name == "tests" else path
        suite = unittest.defaultTestLoader.discover(str(path), pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)


def cmd_init(args):
    root = Path(args.name)
    root.mkdir(parents=True, exist_ok=True)
    config = DEFAULT_CONFIG.copy()
    config["name"] = root.name
    config["description"] = args.description or f"{args.name} 项目"
    project = CNSHProject(root)
    project.config = config
    project.save()

    main_file = root / config["entry"]
    if not main_file.exists():
        main_file.write_text(
            f'# DNA: #龍芯⚡️2026-06-29-{args.name}-v0.1.0\n\n'
            f'输出("欢迎来到 {args.name}！")\n',
            encoding="utf-8",
        )
    print(f"✅ 已创建项目: {root.resolve()}")
    print(f"   入口文件: {main_file}")
    print(f"   配置文件: {root / 'cnsh.json'}")


def cmd_publish(args):
    project = CNSHProject(Path("."))
    dist = Path("dist")
    dist.mkdir(exist_ok=True)
    out = dist / f"{project.name}-{project.version}.zip"
    include: List[str] = ["cnsh.json", "*.cnsh", "tests", "README.md"]
    if out.exists():
        out.unlink()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for pattern in include:
            for p in Path(".").glob(pattern):
                if p.is_dir():
                    for f in p.rglob("*"):
                        if f.is_file():
                            zf.write(f, f.as_posix())
                else:
                    zf.write(p, p.as_posix())
    print(f"✅ 已发布: {out.resolve()}")


def cmd_lsp(args):
    if not args.stdio:
        print("LSP 服务器必须使用 --stdio 启动", file=sys.stderr)
        sys.exit(1)
    LspServer().run()


def main(argv=None):
    parser = argparse.ArgumentParser(prog="cnsh", description="CNSH v2.1 工具链")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="解释执行 .cnsh 文件")
    run_parser.add_argument("file", help="要执行的文件")
    run_parser.add_argument("--optimize", "-O", type=int, default=0, help="优化级别 0-3")
    run_parser.add_argument("--strict-types", action="store_true", help="严格类型模式")
    run_parser.set_defaults(func=cmd_run)

    compile_parser = subparsers.add_parser("compile", help="编译 .cnsh 文件")
    compile_parser.add_argument("file", help="要编译的文件")
    compile_parser.add_argument("--target", "-t", default="python", help="目标语言 python|js|rust|c")
    compile_parser.add_argument("--output", "-o", help="输出文件路径")
    compile_parser.add_argument("--optimize", "-O", type=int, default=0, help="优化级别 0-3")
    compile_parser.add_argument("--strict-types", action="store_true", help="严格类型模式")
    compile_parser.set_defaults(func=cmd_compile)

    test_parser = subparsers.add_parser("test", help="运行测试")
    test_parser.add_argument("path", nargs="?", help="测试文件或目录（默认 tests）")
    test_parser.set_defaults(func=cmd_test)

    init_parser = subparsers.add_parser("init", help="初始化新项目")
    init_parser.add_argument("name", help="项目名称")
    init_parser.add_argument("--description", help="项目描述")
    init_parser.set_defaults(func=cmd_init)

    publish_parser = subparsers.add_parser("publish", help="打包发布项目")
    publish_parser.set_defaults(func=cmd_publish)

    lsp_parser = subparsers.add_parser("lsp", help="启动 LSP 服务器")
    lsp_parser.add_argument("--stdio", action="store_true", required=True, help="使用 stdio 通信")
    lsp_parser.set_defaults(func=cmd_lsp)

    args = parser.parse_args(argv)
    try:
        args.func(args)
    except CNSHError as exc:
        print(f"❌ {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
