#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA: #龍芯⚡️丙午·丁酉·乙酉·午时·䷾既济-CNSH-CLI-V1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: CC BY-NC-SA 4.0（核心思想层）· License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

CNSH 统一命令行工具 v1.0 —— 编译器/运行器/测试/包管理/文档站 单一入口
对比不照抄：词法/语法/AST/Python 代码生成复用 08_BIN/cnsh_compiler.py（56KB 四阶段完备）；
JS target 复用 08_BIN/cnsh_jsgen.py；测试复用 cnsh_test_runner；pm/docs 委托同族引擎。

用法:
  cnsh build <file.cnsh> [-o out] [--target python|js] [--sign]   # 编译
  cnsh run <file.cnsh>                                            # 编译并执行 (python target)
  cnsh test [--verbose]                                           # 基线测试
  cnsh test <dir或文件> [--verbose]                                # 指定测试
  cnsh pm init|install|publish|list [args]                        # 包管理 → cnsh_pm.py
  cnsh docs [--serve]                                             # 文档站 → packaging/cnsh-docs
  cnsh init [dir]                                                 # 项目骨架 (cnsh.json + src/)
  cnsh version                                                    # 版本信息
"""
import sys
import os
import json
import argparse
import subprocess
from pathlib import Path

VERSION = "1.0.0"
UID = "UID9622"
ROOT = Path(__file__).resolve().parent.parent
BIN = Path(__file__).resolve().parent

DNA = f"#龍芯⚡️丙午·丁酉·乙酉·午时·䷾既济-CNSH-CLI-V{VERSION}-{UID}"


# ── 编译器委托 ───────────────────────────────
def _compiler():
    sys.path.insert(0, str(BIN))
    from cnsh_compiler import CNSHCompiler
    return CNSHCompiler()


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def cmd_build(args):
    src = Path(args.input)
    if not src.exists():
        print(f"❌ 文件不存在: {src}")
        return 1
    source = _read(src)
    if args.target == "python":
        comp = _compiler()
        result = comp.compile(source, str(src))
        if not result["success"]:
            print("❌ 编译失败:")
            for e in result["errors"]:
                print(f"  {e}")
            return 1
        code = result["python_code"]
        out = Path(args.output) if args.output else src.with_suffix(".py")
    elif args.target == "js":
        sys.path.insert(0, str(BIN))
        from cnsh_jsgen import compile_source
        result = compile_source(source, str(src))
        if not result["success"]:
            print("❌ 编译失败:")
            for e in result["errors"]:
                print(f"  {e}")
            return 1
        code = result["js_code"]
        out = Path(args.output) if args.output else src.with_suffix(".js")
    else:
        print(f"❌ 未知 target: {args.target}（支持 python|js）")
        return 1

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(code + "\n", encoding="utf-8")
    print(f"✅ 编译成功 [{args.target}]: {out}")
    if args.sign:
        try:
            subprocess.run([sys.executable, str(ROOT / "bin" / "lh_gpg_sign.py"),
                            "sign", str(out), "--force"], check=True, timeout=60)
            print(f"🔐 GPG 已签: {out}.asc")
        except Exception as e:
            print(f"🟡 GPG 签名跳过: {e}")
    return 0


def cmd_run(args):
    src = Path(args.input)
    if not src.exists():
        print(f"❌ 文件不存在: {src}")
        return 1
    source = _read(src)
    comp = _compiler()
    result = comp.run(source, str(src))
    if not result["success"]:
        print("❌ 编译失败:")
        for e in result["errors"]:
            print(f"  {e}")
        return 1
    if result.get("execution") == "error":
        print(f"❌ 执行错误: {result.get('execution_error')}")
        return 1
    return 0


def cmd_test(args):
    if args.path is None:
        # 基线测试 → 委托 cnsh_test_runner
        runner = BIN / "cnsh_test_runner.py"
        argv = [sys.executable, str(runner)]
        if args.verbose:
            argv.append("--verbose")
        return subprocess.call(argv)
    # 指定路径测试：扫描 test_*.cnsh，编译+执行判定
    p = Path(args.path)
    files = []
    if p.is_dir():
        files = sorted(p.rglob("test_*.cnsh"))
    elif p.is_file():
        files = [p]
    if not files:
        print(f"❌ 未找到测试文件: {p}")
        return 1
    comp = _compiler()
    passed, failed = 0, []
    for f in files:
        try:
            result = comp.run(_read(f), str(f))
            if result["success"] and result.get("execution") != "error":
                passed += 1
                print(f"  🟢 {f.relative_to(ROOT)}")
            else:
                failed.append(f)
                msg = (result.get("errors") or [result.get("execution_error", "?")])[:1]
                print(f"  ❌ {f.relative_to(ROOT)} — {msg}")
        except Exception as e:
            failed.append(f)
            print(f"  ❌ {f.relative_to(ROOT)} — {e}")
    print(f"\n总计: {len(files)} | ✅ 通过: {passed} | ❌ 失败: {len(failed)}")
    return 1 if failed else 0


def cmd_pm(args):
    pm = BIN / "cnsh_pm.py"
    if not pm.exists():
        print("❌ 缺少 cnsh_pm.py")
        return 1
    argv = [sys.executable, str(pm)] + args.args
    return subprocess.call(argv)


def cmd_docs(args):
    gen = ROOT / "packaging" / "cnsh-docs" / "generate_site.py"
    if not gen.exists():
        print("❌ 缺少文档站生成器 packaging/cnsh-docs/generate_site.py")
        return 1
    argv = [sys.executable, str(gen)]
    if args.serve:
        argv.append("--serve")
    return subprocess.call(argv)


def cmd_init(args):
    target = Path(args.dir) if args.dir else Path(".")
    target.mkdir(parents=True, exist_ok=True)
    src = target / "src"
    src.mkdir(parents=True, exist_ok=True)
    pkg = {
        "name": target.name or "cnsh-project",
        "version": "0.1.0",
        "description": "CNSH 项目",
        "license": "CC BY-NC-SA 4.0",
        "entry": "src/main.cnsh",
        "author": {"name": "诸葛鑫", "uid": UID},
        "dependencies": {},
    }
    manifest = target / "cnsh.json"
    if not manifest.exists():
        manifest.write_text(json.dumps(pkg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    hello = src / "main.cnsh"
    if not hello.exists():
        hello.write_text(
            "# 创建者: 诸葛鑫（UID9622）\n"
            "# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰\n"
            "# DNA: #龍芯⚡️丙午·丁酉·丙辰·午时·䷆师-CNSH-PROJECT-HELLO-v1.1-UID9622\n\n"
            "功能 主() {\n"
            '    打印("你好，龍魂 CNSH 世界")\n'
            "}\n\n"
            "主()\n", encoding="utf-8")
    print(f"✅ CNSH 项目骨架已创建: {target}/")
    print(f"   cnsh.json · src/main.cnsh")
    print(f"   下一步: cnsh run {target}/src/main.cnsh")
    return 0


def main():
    ap = argparse.ArgumentParser(
        prog="cnsh",
        description="🐉 CNSH 统一命令行工具 v" + VERSION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  cnsh build hello.cnsh --target python -o hello.py
  cnsh build hello.cnsh --target js -o hello.js
  cnsh run hello.cnsh
  cnsh test --verbose
  cnsh pm init && cnsh pm list
  cnsh docs --serve
  cnsh init demo && cnsh run demo/src/main.cnsh
""")
    ap.add_argument("--version", action="store_true", help="版本信息")
    sub = ap.add_subparsers(dest="cmd")

    b = sub.add_parser("build", help="编译 CNSH → python/js")
    b.add_argument("input")
    b.add_argument("-o", "--output")
    b.add_argument("--target", default="python", choices=["python", "js"])
    b.add_argument("--sign", action="store_true", help="编译产物自动 GPG 签名")
    b.set_defaults(fn=cmd_build)

    r = sub.add_parser("run", help="编译并执行 CNSH (python target)")
    r.add_argument("input")
    r.set_defaults(fn=cmd_run)

    t = sub.add_parser("test", help="运行 CNSH 测试")
    t.add_argument("path", nargs="?", default=None)
    t.add_argument("--verbose", "-v", action="store_true")
    t.set_defaults(fn=cmd_test)

    p = sub.add_parser("pm", help="CNSH 包管理器 (委托 cnsh_pm)")
    p.add_argument("args", nargs=argparse.REMAINDER)
    p.set_defaults(fn=cmd_pm)

    d = sub.add_parser("docs", help="生成/服务 CNSH 文档站")
    d.add_argument("--serve", action="store_true")
    d.set_defaults(fn=cmd_docs)

    i = sub.add_parser("init", help="初始化 CNSH 项目骨架")
    i.add_argument("dir", nargs="?")
    i.set_defaults(fn=cmd_init)

    args = ap.parse_args()
    if args.version:
        print(f"🐉 CNSH 统一命令行工具 v{VERSION}")
        print(f"DNA: {DNA}")
        print("归属名: 诸葛鑫 | UID9622 · 龍芯北辰")
        return 0
    if not getattr(args, "cmd", None):
        ap.print_help()
        return 0
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
