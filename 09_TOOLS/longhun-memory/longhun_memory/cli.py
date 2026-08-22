#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·乙未·壬子·丙午·䷙大畜-MEMORY-CLI-v2.0-CNSH
# License: MulanPSL v2
"""longhun-memory CLI v2.0 · CNSH双输出"""

import argparse
import json
import os
import subprocess
import sys
from .vault import MemoryVault


def main():
    p = argparse.ArgumentParser(
        description="龍魂记忆工具 v2.0 · 压缩+CNSH通用格式+国密加密+DNA追溯",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh-memory seal dialog.json -k mypass                           # CNSH格式封存
  lh-memory seal dialog.json -k mypass --format json             # JSON格式封存(兼容)
  lh-memory unseal encrypted.lhm -k mypass                       # 默认输出CNSH文本
  lh-memory unseal encrypted.lhm -k mypass --json                # 输出JSON
  lh-memory unseal encrypted.lhm -k mypass --cnsh --json         # 双输出
  lh-memory stat
  lh-memory test
        """
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    # seal
    s = sub.add_parser("seal", help="压缩+加密对话记忆 → .lhm")
    s.add_argument("input", help="输入 JSON 文件（对话列表）")
    s.add_argument("--key", "-k", required=True, help="加密密钥")
    s.add_argument("--strategy", "-s", default="smart",
                   choices=["smart", "recent", "summarize", "none"])
    s.add_argument("--format", "-f", default="cnsh",
                   choices=["cnsh", "json"],
                   help="存储格式: cnsh(默认,通用流通) | json(兼容v1)")
    s.add_argument("--keywords", default=None,
                   help="逗号分隔的关键词")
    s.add_argument("--output", "-o", default=None,
                   help="输出文件（默认: 输入文件名.lhm）")

    # unseal
    u = sub.add_parser("unseal", help="解密+校验 → CNSH文本/JSON双输出")
    u.add_argument("input", help="输入 .lhm 文件")
    u.add_argument("--key", "-k", required=True, help="解密密钥")
    u.add_argument("--output", "-o", default=None,
                   help="输出文件基名（自动加 .cnsh / .json 后缀）")
    u.add_argument("--cnsh", action="store_true", default=True,
                   help="输出 CNSH 文本（默认启用）")
    u.add_argument("--json", action="store_true", default=False,
                   help="同时输出 JSON")
    u.add_argument("--cnsh-only", action="store_true", default=False,
                   help="仅输出 CNSH 文本")
    u.add_argument("--json-only", action="store_true", default=False,
                   help="仅输出 JSON")

    # stat
    sub.add_parser("stat", help="显示统计信息")

    # test
    sub.add_parser("test", help="运行自检")

    args = p.parse_args()

    if args.cmd == "test":
        print("🧪 运行自检...")
        tests = ["longhun_memory.sm_crypto", "longhun_memory.dna",
                 "longhun_memory.compressor", "longhun_memory.cnsh_text",
                 "longhun_memory.vault"]
        for t in tests:
            result = subprocess.run([sys.executable, "-m", t],
                                    capture_output=True, text=True,
                                    cwd=os.path.dirname(os.path.dirname(__file__)))
            print(result.stdout[-200:] if len(result.stdout) > 200 else result.stdout)
            if result.returncode != 0:
                print(result.stderr)
                sys.exit(1)
        print("🟢🟢🟢 全部自检通过")
        return

    vault = MemoryVault(key=args.key)

    if args.cmd == "seal":
        with open(args.input, "r", encoding="utf-8") as f:
            messages = json.load(f)

        keywords = None
        if args.keywords:
            keywords = [k.strip() for k in args.keywords.split(",")]

        blob = vault.seal(messages, strategy=args.strategy,
                          format=args.format, keywords=keywords)
        out_path = args.output or args.input.rsplit(".", 1)[0] + ".lhm"
        with open(out_path, "wb") as f:
            f.write(blob)
        print(f"🟢 封存完成 → {out_path}")
        print(f"   格式: {args.format.upper()}")
        print(f"   DNA: {vault.history[-1]}")

    elif args.cmd == "unseal":
        with open(args.input, "rb") as f:
            blob = f.read()
        result = vault.unseal(blob)
        if not result.ok:
            print(f"🔴 校验失败: {result.error}")
            sys.exit(1)

        print(f"🟢 解封成功")
        print(f"   DNA: {result.dna}")
        print(f"   审计: {result.audit.emoji} {result.audit.label}")

        # 决定输出
        output_cnsh = args.cnsh and not args.json_only
        output_json = args.json or args.json_only
        base = args.output or args.input.rsplit(".", 1)[0]

        if output_cnsh and result.cnsh_text:
            if args.output:
                cnsh_path = base.rsplit(".", 1)[0] + ".cnsh" if "." in base else base + ".cnsh"
                result.to_cnsh_file(cnsh_path)
                print(f"   CNSH → {cnsh_path}")
            else:
                print(f"\n{result.cnsh_text}")

        if output_json and result.data:
            if args.output:
                json_path = base.rsplit(".", 1)[0] + ".json" if "." in base else base + ".json"
                result.to_json_file(json_path)
                print(f"   JSON → {json_path}")
            else:
                json.dump(result.data, sys.stdout, ensure_ascii=False, indent=2)

    elif args.cmd == "stat":
        print(json.dumps(vault.stat(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
