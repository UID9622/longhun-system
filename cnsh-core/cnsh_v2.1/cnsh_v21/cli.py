# -*- coding: utf-8 -*-
"""
CNSH v2.1 命令行入口
DNA: #龍芯⚡️2026-06-29-CNSH-CLI-v2.1
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from . import run_source, compile_source
from .repl import run_repl
from .errors import CNSHError


def _read_file(path: Path) -> str:
    if not path.exists():
        raise CNSHError(f"文件不存在: {path}")
    return path.read_text(encoding="utf-8")


def _print_type_diagnostics(errors, warnings):
    for w in warnings:
        print(f"⚠️ 类型警告: {w}")
    for e in errors:
        print(f"❌ 类型错误: {e}")


def _run_compiled(python_code: str, path: Path):
    print("=== 执行编译结果 ===")
    exec_globals = {"__builtins__": __builtins__}
    exec(compile(python_code, str(path), "exec"), exec_globals)


def _run_js(js_code: str, path: Path):
    print("=== 执行编译结果 ===")
    tmp = tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8")
    tmp.write(js_code)
    tmp.close()
    try:
        subprocess.run(["node", tmp.name], check=True)
    finally:
        Path(tmp.name).unlink(missing_ok=True)


def _run_rust(rust_code: str, path: Path):
    print("=== 执行编译结果 ===")
    tmp = tempfile.NamedTemporaryFile("w", suffix=".rs", delete=False, encoding="utf-8")
    tmp.write(rust_code)
    tmp.close()
    exe = tmp.name.replace(".rs", "")
    try:
        subprocess.run(["rustc", tmp.name, "-o", exe], check=True)
        subprocess.run([exe], check=True)
    finally:
        Path(tmp.name).unlink(missing_ok=True)
        Path(exe).unlink(missing_ok=True)


def _run_c(c_code: str, path: Path):
    print("=== 执行编译结果 ===")
    tmp = tempfile.NamedTemporaryFile("w", suffix=".c", delete=False, encoding="utf-8")
    tmp.write(c_code)
    tmp.close()
    exe = tmp.name.replace(".c", "")
    try:
        subprocess.run(["gcc", tmp.name, "-o", exe, "-lm"], check=True)
        subprocess.run([exe], check=True)
    finally:
        Path(tmp.name).unlink(missing_ok=True)
        Path(exe).unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description="CNSH v2.1 解释器 / 编译器")
    parser.add_argument("file", nargs="?", type=Path, help="要执行的 .cnsh 文件")
    parser.add_argument("--compile", action="store_true", help="仅编译输出")
    parser.add_argument("--target", "-t", default="python", help="编译目标: python|javascript|rust|c (默认 python)")
    parser.add_argument("--output", "-o", type=Path, help="编译输出文件路径")
    parser.add_argument("--run-compiled", action="store_true", help="编译后自动执行")
    parser.add_argument("--optimize", "-O", type=int, default=0, help="优化级别 0-3 (默认 0)")
    parser.add_argument("--type-check", dest="type_check", action="store_true", default=True, help="启用类型检查 (默认)")
    parser.add_argument("--no-type-check", dest="type_check", action="store_false", help="禁用类型检查")
    parser.add_argument("--strict-types", action="store_true", help="严格类型模式：类型错误时终止执行")
    parser.add_argument("--repl", action="store_true", help="进入交互式解释器")
    args = parser.parse_args()

    if args.repl:
        run_repl()
        return

    if not args.file:
        parser.print_help()
        sys.exit(1)

    source = _read_file(args.file)
    print(f"🐉 CNSH v2.1 | 文件: {args.file} | 目标: {args.target} | 优化级别: {args.optimize}")

    if args.compile:
        code = compile_source(
            source,
            target=args.target,
            file=str(args.file),
            optimize_level=args.optimize,
            type_check=args.type_check,
            strict_types=args.strict_types,
            diagnostics_callback=_print_type_diagnostics,
        )
        if args.output:
            args.output.write_text(code, encoding="utf-8")
            print(f"✅ 已编译到: {args.output}")
        else:
            print(f"=== 生成的 {args.target} 代码 ===")
            print(code)
        if args.run_compiled:
            if args.target in ("python", "py"):
                _run_compiled(code, args.file)
            elif args.target in ("javascript", "js"):
                _run_js(code, args.file)
            elif args.target in ("rust", "rs"):
                _run_rust(code, args.file)
            elif args.target in ("c", "cc"):
                _run_c(code, args.file)
            else:
                print(f"⚠️ 暂不支持自动执行目标: {args.target}")
        return

    try:
        result = run_source(
            source,
            file=str(args.file),
            optimize_level=args.optimize,
            type_check=args.type_check,
            strict_types=args.strict_types,
            diagnostics_callback=_print_type_diagnostics,
        )
        print(f"✅ 执行完成，返回值: {result!r}")
    except CNSHError as exc:
        print(exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
