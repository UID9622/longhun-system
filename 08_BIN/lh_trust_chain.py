#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 信任链统一入口 v1.2.0
DNA: #龍芯⚡️丙午·丙申·己未·癸酉-TRUST-CHAIN-ENTRY-v1.2-UID9622
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

用法:
    lh_trust_chain.py demo                # 一键演示篡改检测
    lh_trust_chain.py deploy [args...]    # 生产环境一键部署
    lh_trust_chain.py verify [path]       # 验证签章链完整性
    lh_trust_chain.py status [path]       # 查看链状态
    lh_trust_chain.py docs                # 打开/打印协议文档路径

协议: MulanPSL v2（工程代码层）
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIN = ROOT / "08_BIN"
PROTOCOL = ROOT / "01_protocols" / "LH-TRUST-CHAIN-DELIVERY-v1.2.md"
PORTAL = ROOT / "10_PORTAL" / "trust-chain.html"

VERSION = "v1.2.0"
DNA = "#龍芯⚡️丙午·丙申·己未·癸酉-TRUST-CHAIN-ENTRY-v1.2-UID9622"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


def _color(c: str, text: str) -> str:
    codes = {
        "green": "\033[0;32m",
        "yellow": "\033[1;33m",
        "red": "\033[0;31m",
        "blue": "\033[0;34m",
        "reset": "\033[0m",
    }
    if os.environ.get("NO_COLOR"):
        return text
    return f"{codes.get(c, '')}{text}{codes['reset']}"


def _run(cmd: list, cwd: Path | None = None) -> int:
    print(_color("blue", f"$ {' '.join(str(c) for c in cmd)}"))
    return subprocess.call(cmd, cwd=str(cwd) if cwd else None)


def cmd_demo(_args):
    """运行 demo_trust_chain.sh 演示脚本。"""
    script = BIN / "demo_trust_chain.sh"
    if not script.exists():
        print(_color("red", f"❌ 演示脚本不存在: {script}"))
        return 1
    return _run(["bash", str(script)])


def cmd_deploy(args, extra: list):
    """转发参数到 deploy_trust_chain.sh。"""
    script = BIN / "deploy_trust_chain.sh"
    if not script.exists():
        print(_color("red", f"❌ 部署脚本不存在: {script}"))
        return 1
    return _run(["bash", str(script)] + extra)


def _find_chain_dir(path: Path) -> Path:
    chain = path / ".dna-chain"
    if chain.exists():
        return chain
    # 兼容旧命名
    chain2 = path / ".stamp-chain"
    if chain2.exists():
        return chain2
    return chain


def _load_stamps(chain_dir: Path):
    if not chain_dir.exists():
        return []
    stamps = []
    for p in sorted(chain_dir.iterdir()):
        if p.is_file() and p.name.startswith("stamp_") and p.suffix == ".json":
            try:
                stamps.append((p, json.loads(p.read_text(encoding="utf-8"))))
            except Exception as e:
                print(_color("yellow", f"⚠️ 解析失败 {p}: {e}"))
    stamps.sort(key=lambda x: x[1].get("index", 0))
    return stamps


def _compute_hash(stamp: dict) -> str:
    payload = "|".join([
        str(stamp.get("index", "")),
        str(stamp.get("version", "")),
        str(stamp.get("diff", "")),
        str(stamp.get("prev_hash", "")),
        str(stamp.get("timestamp", "")),
        str(stamp.get("author", "")),
    ])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def cmd_verify(args):
    """验证签章链完整性。"""
    chain_dir = _find_chain_dir(Path(args.path))
    if not chain_dir.exists():
        print(_color("red", f"❌ 签章链目录不存在: {chain_dir}"))
        print(_color("yellow", "提示: 先运行 'lh trust-chain deploy' 初始化链。"))
        return 1

    stamps = _load_stamps(chain_dir)
    if not stamps:
        print(_color("yellow", f"🟡 签章链目录为空: {chain_dir}"))
        return 0

    print(_color("blue", f"🔍 验证签章链: {chain_dir} (共 {len(stamps)} 个签章)"))

    broken_index = None
    tamper_index = None
    prev_hash = None

    # 读取 genesis hash
    genesis_file = chain_dir / "genesis.hash"
    if genesis_file.exists():
        prev_hash = genesis_file.read_text(encoding="utf-8").strip()

    for path, stamp in stamps:
        idx = stamp.get("index", 0)

        # 链式检查
        if idx == 1:
            expected_prev = prev_hash
        else:
            expected_prev = stamps[idx - 2][1].get("current_hash") if idx >= 2 else None

        if expected_prev is not None and stamp.get("prev_hash") != expected_prev:
            broken_index = idx
            print(_color("red", f"  ❌ 签章{idx} 前驱哈希断裂 (prev_hash 不匹配)"))
            break

        # 指纹检查
        expected_current = _compute_hash(stamp)
        if stamp.get("current_hash") != expected_current:
            tamper_index = idx
            print(_color("red", f"  ❌ 签章{idx} 指纹校验失败 (内容可能被篡改)"))
            break

        print(_color("green", f"  ✅ 签章{idx} 通过"))

    if broken_index is not None:
        print(_color("red", f"\n🔴 链式断裂于签章 {broken_index}"))
        return 2
    if tamper_index is not None:
        print(_color("red", f"\n🔴 篡改检测于签章 {tamper_index}"))
        return 3

    print(_color("green", "\n🟢 签章链完整，所有签章通过验证。"))
    return 0


def cmd_status(args):
    """查看签章链状态。"""
    chain_dir = _find_chain_dir(Path(args.path))
    print(_color("blue", f"🐉 龍魂信任链状态 · {VERSION}"))
    print(f"  DNA: {DNA}")
    print(f"  链目录: {chain_dir}")

    if not chain_dir.exists():
        print(_color("yellow", "  🟡 链目录不存在"))
        return 0

    stamps = _load_stamps(chain_dir)
    print(f"  签章数量: {len(stamps)}")

    if stamps:
        last_path, last_stamp = stamps[-1]
        print(f"  最新签章: {last_stamp.get('index', '?')} @ {last_stamp.get('timestamp', '?')}")
        print(f"  作者: {last_stamp.get('author', '?')}")
        print(f"  摘要: {last_stamp.get('diff', '?')[:60]}...")

    # 自动验证
    print("")
    return cmd_verify(args)


def cmd_docs(_args):
    """打印并尝试打开协议文档。"""
    print(_color("blue", "📄 龍魂信任链协议文档"))
    print(f"  Markdown: {PROTOCOL}")
    print(f"  HTML展示: {PORTAL}")

    if sys.platform == "darwin":
        subprocess.call(["open", str(PROTOCOL)])
    elif sys.platform.startswith("linux"):
        subprocess.call(["xdg-open", str(PROTOCOL)])
    else:
        print(_color("yellow", "  请手动打开上述路径。"))
    return 0


def main():
    parser = argparse.ArgumentParser(
        prog="lh_trust_chain",
        description="龍魂信任链统一入口",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh_trust_chain.py demo
  lh_trust_chain.py deploy --env production --gpg-key A2D0092CEE2E5BA87035600924C3704A8CC26D5F
  lh_trust_chain.py verify ./my-project
  lh_trust_chain.py status
  lh_trust_chain.py docs
        """,
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION} {DNA}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_demo = sub.add_parser("demo", help="一键演示篡改检测")
    p_demo.set_defaults(func=cmd_demo)

    p_deploy = sub.add_parser("deploy", help="生产环境一键部署")
    p_deploy.set_defaults(func=cmd_deploy)

    p_verify = sub.add_parser("verify", help="验证签章链完整性")
    p_verify.add_argument("path", nargs="?", default=".", help="包含 .dna-chain 的目录")
    p_verify.set_defaults(func=cmd_verify)

    p_status = sub.add_parser("status", help="查看链状态并自动验证")
    p_status.add_argument("path", nargs="?", default=".", help="包含 .dna-chain 的目录")
    p_status.set_defaults(func=cmd_status)

    p_docs = sub.add_parser("docs", help="打开协议文档")
    p_docs.set_defaults(func=cmd_docs)

    args, unknown = parser.parse_known_args()
    if args.command == "deploy":
        sys.exit(args.func(args, unknown))
    if unknown:
        parser.error(f"unrecognized arguments: {' '.join(unknown)}")
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
