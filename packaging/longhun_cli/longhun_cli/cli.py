# -*- coding: utf-8 -*-
"""cli.py — 对外分发薄壳入口（双态分派）。

外部态（无 LONGHUN_ROOT）：health/flow/version 零依赖可用。
系统态（LONGHUN_ROOT 指向龍魂源码树）：health/cil/doc-sync 透传系统内完整逻辑。
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from . import __version__
from .core import bazi, benchmark, flow, health_basic, security_check

# ── 系统树探测 ────────────────────────────────────────────────
def find_root() -> Path | None:
    env = os.environ.get("LONGHUN_ROOT")
    if env:
        # LONGHUN_ROOT 显式设置但无效 → 明确外部态（不静默 fallback）
        return Path(env).expanduser() if (Path(env).expanduser() / "bin" / "lh.py").exists() else None
    home = Path.home() / "longhun-system"
    if (home / "bin" / "lh.py").exists():
        return home
    return None


def _run(cmd: list[str]) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        out = (r.stdout or "") + (("\n" + r.stderr) if r.stderr and r.stdout else r.stderr or "")
        return r.returncode, out.strip()
    except Exception as e:  # noqa: BLE001
        return 1, f"ERROR: {e}"


def _emit(data, as_json: bool, text: str | None = None) -> None:
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    elif text is not None:
        print(text)
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


# ── 子命令 ────────────────────────────────────────────────────
def cmd_version(args) -> None:
    data = {"service": "longhun-cli", "version": __version__, "protocol": "对外接口协议-v1.0"}
    _emit(data, args.json, text=f"longhun-cli {__version__} (龍魂 CIL 对外分发弹头)")


def cmd_flow(args) -> None:
    data = flow(args.text or "龍魂")
    _emit(data, args.json)


def cmd_bazi(args) -> None:
    data = bazi(args.date, args.time)
    _emit(data, args.json)


def cmd_health(args, root: Path | None) -> None:
    if root is None:
        data = health_basic()
        _emit(data, args.json)
        return
    # 系统态：转发系统内健康检查（位置子命令 `health`，支持 --json）
    cmd = [sys.executable, str(root / "bin" / "lh.py"), "health"] + (["--json"] if args.json else [])
    code, out = _run(cmd)
    if code != 0:
        data = {"status": "error", "mode": "system", "error": out}
        _emit(data, args.json)
        return
    if args.json:
        # 系统内 lh.py --health 已输出可解析 JSON 时直接透传
        print(out)
    else:
        print(out)


def cmd_security(args, root: Path | None) -> None:
    if root is not None:
        cmd = [sys.executable, str(root / "bin" / "lh.py"), "security", "--json"]
        code, out = _run(cmd)
        if code == 0:
            print(out)
            return
    data = security_check(args.scan_dir)
    _emit(data, args.json)


def cmd_benchmark(args, root: Path | None) -> None:
    if root is not None:
        cmd = [sys.executable, str(root / "bin" / "lh.py"), "benchmark",
               "--iterations", str(args.iterations), "--json"]
        code, out = _run(cmd)
        if code == 0:
            print(out)
            return
    data = benchmark(args.iterations)
    _emit(data, args.json)


def cmd_system(args, root: Path | None, name: str) -> None:
    if root is None:
        data = {
            "status": "error",
            "mode": "external",
            "message": f"`lh {name}` 需要龍魂系统源码树。请设置 LONGHUN_ROOT 指向源码树（如 ~/longhun-system）后重试。",
        }
        _emit(data, args.json)
        return
    cmd = [sys.executable, str(root / "bin" / "lh.py"), name] + args.rest
    code, out = _run(cmd)
    if code != 0:
        data = {"status": "error", "mode": "system", "command": name, "error": out}
        _emit(data, args.json)
        return
    print(out)


# ── 入口 ──────────────────────────────────────────────────────
def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="lh",
        description="龍魂 CIL · 文化主权命令行接口（对外分发弹头）",
        add_help=False,
    )
    parser.add_argument("--json", action="store_true", help="JSON 可解析输出")
    parser.add_argument("--help", "-h", action="store_true", help="帮助")
    sub = parser.add_subparsers(dest="command")

    p_version = sub.add_parser("version")
    p_version.add_argument("--json", action="store_true")

    p_flow = sub.add_parser("flow")
    p_flow.add_argument("text", nargs="?", default="龍魂")
    p_flow.add_argument("--json", action="store_true")

    p_bazi = sub.add_parser("bazi")
    p_bazi.add_argument("--date", default=None, help="出生日期 YYYY-MM-DD（默认今天）")
    p_bazi.add_argument("--time", default=None, help="出生时间 HH:MM（默认当前时刻）")
    p_bazi.add_argument("--json", action="store_true")

    p_health = sub.add_parser("health")
    p_health.add_argument("--json", action="store_true")

    p_security = sub.add_parser("security")
    p_security.add_argument("--json", action="store_true")
    p_security.add_argument("--scan-dir", default=None, help="敏感信息扫描目录（默认本包）")

    p_benchmark = sub.add_parser("benchmark")
    p_benchmark.add_argument("--iterations", type=int, default=1000, help="每项迭代次数 (默认 1000)")
    p_benchmark.add_argument("--json", action="store_true")

    p_cil = sub.add_parser("cil")
    p_cil.add_argument("--json", action="store_true")
    p_cil.add_argument("rest", nargs=argparse.REMAINDER)

    p_doc = sub.add_parser("doc-sync")
    p_doc.add_argument("--json", action="store_true")
    p_doc.add_argument("rest", nargs=argparse.REMAINDER)

    args = parser.parse_args(argv)

    if args.help or args.command is None:
        parser.print_help()
        print("\n子命令: version · health · flow · bazi · security · benchmark · cil · doc-sync  （均支持 --json）")
        return

    root = find_root()
    if args.command == "version":
        cmd_version(args)
    elif args.command == "flow":
        cmd_flow(args)
    elif args.command == "bazi":
        cmd_bazi(args)
    elif args.command == "health":
        cmd_health(args, root)
    elif args.command == "security":
        cmd_security(args, root)
    elif args.command == "benchmark":
        cmd_benchmark(args, root)
    elif args.command == "cil":
        cmd_system(args, root, "cil")
    elif args.command == "doc-sync":
        cmd_system(args, root, "doc-sync")


if __name__ == "__main__":
    main()
