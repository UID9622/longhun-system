#!/usr/bin/env python3
# 龍魂系统 · 工程实现层
# License: MulanPSL v2
# 文化归属: 思想框架归龍魂核心思想层 (CC BY-NC-SA 4.0)
# DNA: #龍芯⚡️丙午·丙申·庚戌·COMPAT-PATH-v1.0-UID9622
"""旧路径兼容映射脚本。

功能:
1. 将重组前的旧路径翻译为新结构路径。
2. 记录已清理的实验性 Symlink。
3. 为仍在引用旧路径的脚本/服务提供兼容入口。

使用:
    python3 scripts/compat-path.py resolve <old_path>
    python3 scripts/compat-path.py list-removed
    python3 scripts/compat-path.py install-symlinks --dry-run
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# 旧路径 → 新路径映射（相对仓库根目录）
COMPAT_MAP: dict[str, str] = {
    # 重组后的规范化目录（v1.0 安全阶段）
    "training": "train",
    "backend": "services/backend_legacy",
    "knowledge-graph": "knowledge/graph",
    "字体": "longhun-font",

    # 计划中的高风险重命名（仅记录，不自动执行）
    # "bin": "08_BIN",
    # "layers": "03_LAYERS",
    # "services": "04_SERVICES",
    # "engines": "05_ENGINES",
    # "protocols": "01_PROTOCOLS",
    # "memory": "06_MEMORY",
    # "audit": "07_AUDIT",
    # "tools": "09_TOOLS",
    # "portal": "10_PORTAL",
    # "data": "11_DATA",
    # "docs": "12_DOCS",
    # "tests": "13_TESTS",
    # "assets": "14_ASSETS",
    # "labs": "15_LABS",
    # "config": "20_CONFIG",
}

# 2026-08-04 已清理的实验性 Symlink（原指向 archive/experiments/）
REMOVED_SYMLINKS: list[str] = [
    "arxiv",
    "benchmarks",
    "brain",
    "bridges",
    "calendar-context-logger",
    "chrome_extension",
    "compute_kernels",
    "core",
    "core-services",
    "crypto-stack",
    "data-hub",
    "desktop",
    "forensic_kernel",
    "kg-api",
    "memory-universe",
    "monitoring",
    "ops-console",
    "orders",
    "project-memory",
    "rag_indexes",
    "rules-engine-v2.5",
    "skill-standards.integrated",
    "var",
    "wuxing-visual",
]


class CompatPathError(Exception):
    pass


def resolve(old_path: str) -> str | None:
    """将旧路径解析为新路径；如路径已不存在于映射中，返回 None。"""
    old_path = old_path.strip().lstrip("/")
    parts = old_path.split(os.sep)
    if not parts or not parts[0]:
        return None

    head = parts[0]
    tail = parts[1:]

    if head in COMPAT_MAP:
        new_head = COMPAT_MAP[head]
        return "/".join([new_head] + tail)
    return None


def install_symlinks(dry_run: bool = True) -> list[str]:
    """为需要保留的兼容路径创建/修复 Symlink（当前仅低风险映射）。"""
    actions: list[str] = []
    for old_name, new_name in COMPAT_MAP.items():
        old_path = REPO_ROOT / old_name
        new_path = REPO_ROOT / new_name

        if not new_path.exists():
            actions.append(f"SKIP {old_name}: target {new_name} does not exist")
            continue

        if old_path.is_symlink():
            current_target = os.readlink(old_path)
            if current_target == new_name:
                actions.append(f"OK   {old_name} -> {new_name}")
                continue
            actions.append(f"FIX  {old_name} -> {current_target} => {new_name}")
        else:
            actions.append(f"ADD  {old_name} -> {new_name}")

        if not dry_run:
            old_path.unlink(missing_ok=True)
            old_path.symlink_to(new_name, target_is_directory=new_path.is_dir())

    return actions


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="LongHun path compatibility resolver")
    sub = parser.add_subparsers(dest="command", required=True)

    p_resolve = sub.add_parser("resolve", help="resolve an old path to new path")
    p_resolve.add_argument("old_path", help="old relative path from repo root")

    sub.add_parser("list-removed", help="list experiment symlinks removed in v1.0 cleanup")

    p_install = sub.add_parser("install-symlinks", help="create/repair compatibility symlinks")
    p_install.add_argument("--yes", action="store_true", help="apply changes (default is dry-run)")

    args = parser.parse_args(argv)

    if args.command == "resolve":
        new_path = resolve(args.old_path)
        if new_path:
            print(new_path)
            return 0
        print(f"[compat-path] no mapping for: {args.old_path}", file=sys.stderr)
        return 1

    if args.command == "list-removed":
        print("# 已清理的实验性 Symlink（原指向 archive/experiments/）")
        for name in REMOVED_SYMLINKS:
            print(f"- {name}")
        return 0

    if args.command == "install-symlinks":
        dry_run = not args.yes
        for line in install_symlinks(dry_run=dry_run):
            print(line)
        if dry_run:
            print("\n# dry-run mode; use --yes to apply")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
