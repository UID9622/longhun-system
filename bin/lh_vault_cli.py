#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════╗
# ║  龍魂·本地保险柜 CLI v1.0                                    ║
# ║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-VAULT-CLI-v1.0        ║
# ║  用法: python3 bin/lh_vault_cli.py <command> [args]          ║
# ╚══════════════════════════════════════════════════════════════╝
"""
本地私人保险柜命令行入口。

命令:
  init                    初始化保险柜
  add <type> <data>       加密存储（data 可以是字符串或文件路径）
  get <dna>               解密读取
  list                    列出所有条目
  delete <dna>            冻结删除
  export <dna> <file>     导出到文件
  sync                    与记忆系统同步，生成快照
"""

import os
import sys
import json
import argparse
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from engines.lh_local_vault import LocalVault

DNA = "#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-VAULT-CLI-v1.0"


def read_data_input(value: str) -> str:
    """支持直接字符串或 @文件路径。"""
    if value.startswith("@"):
        p = Path(value[1:])
        if not p.exists():
            raise FileNotFoundError(f"文件不存在: {p}")
        return p.read_text(encoding="utf-8")
    return value


def cmd_init(vault: LocalVault, args):
    vault.init_vault()
    return 0


def cmd_add(vault: LocalVault, args):
    data = read_data_input(args.data)
    dna = vault.store(args.type, data, password=args.password)
    print(f"[VAULT] 已存储 | DNA: {dna}")
    return 0


def cmd_get(vault: LocalVault, args):
    plaintext = vault.retrieve(args.dna, password=args.password)
    print(plaintext)
    return 0


def cmd_list(vault: LocalVault, args):
    entries = vault.list_entries()
    print(f"[VAULT] 共 {len(entries)} 条记录")
    for e in entries:
        print(f"  - {e['dna']} | {e['data_type']} | {e['size']} bytes | {e['status']}")
    return 0


def cmd_delete(vault: LocalVault, args):
    vault.delete(args.dna, password=args.password)
    print(f"[VAULT] 已冻结: {args.dna}")
    return 0


def cmd_export(vault: LocalVault, args):
    plaintext = vault.retrieve(args.dna, password=args.password)
    Path(args.file).write_text(plaintext, encoding="utf-8")
    print(f"[VAULT] 已导出: {args.file}")
    return 0


def cmd_sync(vault: LocalVault, args):
    """调用记忆系统生成快照。"""
    snapshot_script = ROOT / "engines" / "lh_memory_eternity.py"
    if snapshot_script.exists():
        import subprocess
        result = subprocess.run(
            ["python3", str(snapshot_script), "snapshot"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        print(result.stdout)
        if result.returncode != 0:
            print(result.stderr, file=sys.stderr)
            return result.returncode
    print(f"[VAULT] 记忆快照已生成")
    return 0


def main():
    parser = argparse.ArgumentParser(description="龍魂·本地保险柜 CLI")
    parser.add_argument("--password", help="用户密码（可选）")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="初始化保险柜")

    p_add = sub.add_parser("add", help="加密存储")
    p_add.add_argument("type", help="数据类型")
    p_add.add_argument("data", help="数据内容，或 @文件路径")

    p_get = sub.add_parser("get", help="解密读取")
    p_get.add_argument("dna", help="DNA 追溯码")

    sub.add_parser("list", help="列出条目")

    p_del = sub.add_parser("delete", help="冻结删除")
    p_del.add_argument("dna", help="DNA 追溯码")

    p_exp = sub.add_parser("export", help="导出到文件")
    p_exp.add_argument("dna", help="DNA 追溯码")
    p_exp.add_argument("file", help="输出文件路径")

    sub.add_parser("sync", help="与记忆系统同步")

    args = parser.parse_args()

    vault = LocalVault()
    if args.command == "init":
        return cmd_init(vault, args)

    # 其他命令需要保险柜已初始化
    if not (Path.home() / ".longhun" / "vault" / "index.json").exists():
        print("[VAULT] 保险柜未初始化，先执行: python3 bin/lh_vault_cli.py init", file=sys.stderr)
        return 1

    handlers = {
        "add": cmd_add,
        "get": cmd_get,
        "list": cmd_list,
        "delete": cmd_delete,
        "export": cmd_export,
        "sync": cmd_sync,
    }
    return handlers[args.command](vault, args)


if __name__ == "__main__":
    sys.exit(main())
