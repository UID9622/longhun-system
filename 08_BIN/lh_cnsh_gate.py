# -*- coding: utf-8 -*-
"""lh_cnsh_gate.py — 新代码 CNSH 命名闸口 v1.0（语法统一化·闸口焊死）。

功能: 检查「新增」的 .py 文件是否使用 CNSH 中文命名。
      违反 → 🔴 不入库（exit 1）。存量英文命名脚本不检查（只补缺不改心血）。

判定「新增」:
  --pre-commit : git diff --cached 中新增(A)的 .py
  --repo       : git status 中未跟踪(??)/新增(A)的 .py
判定「CNSH 命名」: 文件名（不含扩展名）含至少 1 个汉字。

用法:
  python3 08_BIN/lh_cnsh_gate.py --pre-commit   # pre-commit 钩子模式
  python3 08_BIN/lh_cnsh_gate.py --repo         # 扫描全仓库新增
  python3 08_BIN/lh_cnsh_gate.py --abom         # A-BOM 备案: 统计存量英文命名 .py（不改）
  python3 08_BIN/lh_cnsh_gate.py --self-check   # 自检

DNA: #龍芯⚡️2026-09-01-新代码-CNSH命名闸口-v1.0
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

# 仓库根（本文件位于 08_BIN/）
仓库根 = Path(__file__).resolve().parent.parent
# 豁免目录（构建/发布/依赖/历史归档——不视为「新代码」）
豁免目录 = {"_work", "dist", "build", "archive", "_archive", "backups", "backup",
           ".venv", "node_modules", "11_DATA", "models", "weights", "dist_ide",
           "build_ide", "龙魂成片", "dist/longhun-system-v5.0.0-opensource"}
汉字正则 = re.compile(r"[\u4e00-\u9fff]")


def 豁免判定(路径: Path) -> bool:
    """路径是否位于豁免目录。"""
    return any(part in 豁免目录 for part in 路径.parts)


def 获取新增文件(模式: str) -> list[str]:
    """获取新增 .py 文件列表（相对仓库根）。"""
    if 模式 == "pre-commit":
        输出 = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=A"],
            capture_output=True, text=True, cwd=仓库根).stdout
    else:  # repo
        输出 = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, cwd=仓库根).stdout
    文件 = []
    for 行 in 输出.splitlines():
        if 模式 == "pre-commit":
            路径 = 行.strip()
        else:
            状态, 路径 = 行[:2].strip(), 行[3:].strip()
            if 状态 not in ("??", "A"):
                continue
        if 路径.endswith(".py") and not 路径.endswith(".py.asc"):
            文件.append(路径)
    return 文件


def 是否为CNSH命名(路径: str) -> bool:
    """文件名（不含扩展名）含汉字即视为 CNSH 命名。"""
    return bool(汉字正则.search(os.path.basename(路径)))


def 检查(模式: str) -> tuple[list[str], list[str]]:
    新增 = 获取新增文件(模式)
    违规 = [p for p in 新增 if not 是否为CNSH命名(p) and not 豁免判定(Path(p))]
    合规 = [p for p in 新增 if 是否为CNSH命名(p)]
    return 合规, 违规


def 存量备案() -> dict:
    """A-BOM 备案: 统计仓库内存量 .py 命名分布（只读不改）。"""
    from collections import Counter
    计数: Counter = Counter()
    总数 = 0
    for 根, _, 文件 in os.walk(仓库根):
        for 名 in 文件:
            if not 名.endswith(".py"):
                continue
            if 豁免判定(Path(根)):
                continue
            if ".git" in 根 or "__pycache__" in 根:
                continue
            总数 += 1
            计数["中文命名" if 汉字正则.search(名) else "英文命名"] += 1
    return {"总数": 总数, **计数}


def 自检() -> bool:
    """自检用例（确定性·不改库）。"""
    用例 = [
        ("甲子引擎.py", True),
        ("flow_engine.py", False),
        ("数字根_计算.py", True),
        ("lh_api.py", False),
    ]
    for 名, 期望 in 用例:
        if 是否为CNSH命名(名) != 期望:
            print(f"❌ 自检失败: {名}")
            return False
    return True


def 主程序() -> int:
    解析 = argparse.ArgumentParser(description="新代码 CNSH 命名闸口")
    解析.add_argument("--pre-commit", action="store_true", help="pre-commit 钩子模式")
    解析.add_argument("--repo", action="store_true", help="扫描全仓库新增 .py")
    解析.add_argument("--abom", action="store_true", help="A-BOM 备案统计存量")
    解析.add_argument("--self-check", action="store_true", help="自检")
    参数 = 解析.parse_args()

    if 参数.self_check:
        结果 = 自检()
        print("✅ 自检全过" if 结果 else "🔴 自检失败")
        return 0 if 结果 else 1

    if 参数.abom:
        统计 = 存量备案()
        print(f"📋 A-BOM 备案 | 存量 .py 总数: {统计['总数']} | 中文命名: {统计.get('中文命名', 0)} | 英文命名: {统计.get('英文命名', 0)}")
        print("   （只统计不改写·存量英文命名脚本不强制改造）")
        return 0

    if not (参数.pre_commit or 参数.repo):
        print("用法: lh_cnsh_gate.py --pre-commit | --repo | --abom | --self-check")
        return 2

    模式 = "pre-commit" if 参数.pre_commit else "repo"
    合规, 违规 = 检查(模式)

    print(f"🔎 新代码闸口 | 模式={模式} | 新增 .py: {len(合规)+len(违规)} 个")
    for 路径 in 合规:
        print(f"   🟢 {路径}")
    if 违规:
        for 路径 in 违规:
            print(f"   🔴 {路径} —— 文件名未使用 CNSH 中文命名")
        print("❌ 闸口拦截: 新增 .py 必须 CNSH 中文命名（否则不入库）。存量不改。")
        # pre-commit（入库瞬间）硬拦截；--repo 巡检只报告（存量未跟踪文件不误伤）
        return 1 if 模式 == "pre-commit" else 0
    print("✅ 闸口通过: 无违规")
    return 0


if __name__ == "__main__":
    sys.exit(主程序())
