# -*- coding: utf-8 -*-
"""lh_cnsh_gate.py — 新代码 CNSH 命名闸口 v1.1（语法统一化·闸口焊死 · 自动类型分类 + 自动留档）

功能: 检查「新增」的 .py 文件是否使用 CNSH 中文命名。
      违反 → 🔴 不入库（exit 1）。存量英文命名脚本不检查（只补缺不改心血）。

判定「新增」:
  --pre-commit : git diff --cached 中新增(A)的 .py
  --repo       : git status 中未跟踪(??)/新增(A)的 .py
判定「CNSH 命名」: 文件名（不含扩展名）含至少 1 个汉字。

v1.1 (2026-09-04 · PR #95 经验系统化):
  + 违规自动分类: PYTHON_PACKAGE / CLI_COMMAND / PYTEST_FIXTURE / OTHER
  + --json       : 机器可读输出（供 lh publish --auto 决策）
  + --record     : 自动留档 → 07_AUDIT/cnsh_gate_bypass.log（带 type 列）+ 审计 md
  + --classify   : 直接打印给定文件的分类（调试用）
  —— 自动绕行仅限三类已知合理冲突（详见 docs/闸口绕行规则.md）；OTHER 一律人工。

用法:
  python3 08_BIN/lh_cnsh_gate.py --pre-commit            # pre-commit 钩子模式
  python3 08_BIN/lh_cnsh_gate.py --repo                  # 扫描全仓库新增
  python3 08_BIN/lh_cnsh_gate.py --pre-commit --json     # 机器输出违规+类型
  python3 08_BIN/lh_cnsh_gate.py --record "原因" --flow PR-20260904-01 --title "…"
  python3 08_BIN/lh_cnsh_gate.py --abom                  # A-BOM 备案
  python3 08_BIN/lh_cnsh_gate.py --self-check            # 自检

DNA: #龍芯⚡️2026-09-04-新代码-CNSH命名闸口-v1.1-AUTO-BYPASS
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

# 仓库根（本文件位于 08_BIN/）
仓库根 = Path(__file__).resolve().parent.parent
# 豁免目录（构建/发布/依赖/历史归档——不视为「新代码」）
豁免目录 = {"_work", "dist", "build", "archive", "_archive", "backups", "backup",
           ".venv", "node_modules", "11_DATA", "models", "weights", "dist_ide",
           "build_ide", "龙魂成片", "dist/longhun-system-v5.0.0-opensource"}
汉字正则 = re.compile(r"[\u4e00-\u9fff]")

# ── v1.1 · 违规类型分类（供自动绕行决策）──────────────
TYPE_PYTHON_PACKAGE = "PYTHON_PACKAGE"   # 标准 Py 包 ASCII 模块（pyproject.toml 树内）
TYPE_CLI_COMMAND = "CLI_COMMAND"         # 工具链/命令名（08_BIN|bin 顶层）
TYPE_PYTEST_FIXTURE = "PYTEST_FIXTURE"   # pytest 发现惯例 test_*.py
TYPE_OTHER = "OTHER"                     # 未归类 → 禁止自动绕行，人工 P05 决策
KNOWN_TYPES = (TYPE_PYTHON_PACKAGE, TYPE_CLI_COMMAND, TYPE_PYTEST_FIXTURE)

AUDIT_DIR = 仓库根 / "07_AUDIT"
GATE_LOG = AUDIT_DIR / "cnsh_gate_bypass.log"
BYNAME_PREFIX = "cnsh_gate_bypass_"


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


def 判定类型(相对路径: str) -> str:
    """对违规英文命名 .py 自动分类（KNOWN_TYPES / OTHER）。"""
    p = Path(相对路径)
    名 = p.name
    # 1. pytest 惯例
    if 名.startswith("test_"):
        return TYPE_PYTEST_FIXTURE
    # 2. 标准 Py 包树：向上找 pyproject.toml/setup.py/setup.cfg（不穿过仓库根）
    父级 = [p.parent] + list(p.parents)[1:]  # [1:] 跳过仓库根自身
    for 父 in 父级:
        if 父 == Path("."):
            continue
        for 标记 in ("pyproject.toml", "setup.py", "setup.cfg"):
            if (仓库根 / 父 / 标记).exists():
                return TYPE_PYTHON_PACKAGE
    # 3. 工具链命令名（bin / 08_BIN 顶层脚本）
    if str(p).startswith(("08_BIN/", "bin/")):
        return TYPE_CLI_COMMAND
    return TYPE_OTHER


def 检查(模式: str) -> tuple[list[str], list[str]]:
    新增 = 获取新增文件(模式)
    违规 = [p for p in 新增 if not 是否为CNSH命名(p) and not 豁免判定(Path(p))]
    合规 = [p for p in 新增 if 是否为CNSH命名(p)]
    return 合规, 违规


def 违规明细(违规: list[str]) -> list[dict]:
    """违规文件 + 自动分类。"""
    return [{"file": p, "type": 判定类型(p)} for p in 违规]


# ── v1.1 · 自动留档 ─────────────────────────────────
def log_append(条目: dict):
    """append 到 07_AUDIT/cnsh_gate_bypass.log（TSV 带 type 列）。"""
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y-%m-%dT%H:%M:%S")
    with GATE_LOG.open("a", encoding="utf-8") as f:
        f.write(f"{ts} | {条目.get('desc','')} | gate=pre-commit cnsh-name | "
                f"type={条目.get('type','')} | flow={条目.get('flow','-')} | "
                f"pr={条目.get('pr','-')} | bypass reason: {条目.get('reason','')}\n")


def 留档_md(条目: dict):
    """生成/追加审计 md：07_AUDIT/cnsh_gate_bypass_<日期>[_<tag>].md（append 段落·append-only）。"""
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    日期 = time.strftime("%Y-%m-%d")
    tag = (条目.get("tag") or "").strip().replace(" ", "-")
    路径 = AUDIT_DIR / (BYNAME_PREFIX + 日期 + (f"_{tag}" if tag else "") + ".md")
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    if not 路径.exists():
        头 = (f"# 新代码闸口绕行审计留档 · {日期}\n\n"
              f"> 自动留档: `lh_cnsh_gate.py --record` · append-only · 每段落一次绕行\n"
              f"> DNA: #龍芯⚡️2026-09-04-CNSH-GATE-AUTO-RECORD\n"
              f"> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰\n"
              f"> 规则: docs/闸口绕行规则.md\n\n")
        with 路径.open("w", encoding="utf-8") as f:
            f.write(头)
    明细 = "\n".join(f"- `{i['file']}`（type={i['type']}）" for i in 条目.get("items", []))
    if not 明细:
        明细 = "- （无明细）"
    段 = (f"## [{ts}] {条目.get('title','未知发布')} · flow={条目.get('flow','-')}\n\n"
          f"- 类型: {条目.get('type','-')} · gate=pre-commit cnsh-name\n"
          f"- 文件清单:\n{明细}\n"
          f"- bypass reason: {条目.get('reason','-')}\n\n")
    with 路径.open("a", encoding="utf-8") as f:
        f.write(段)
    return 路径


# ── 存量备案 / 自检 ─────────────────────────────────
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
            print(f"❌ 自检失败(命名): {名}")
            return False
    类型用例 = [
        ("packaging/cnsh-stdlib/cnsh_std/crypto.py", TYPE_PYTHON_PACKAGE),
        ("packaging/cnsh-stdlib/tests/test_all.py", TYPE_PYTEST_FIXTURE),
        ("08_BIN/cnsh_pm.py", TYPE_CLI_COMMAND),
        ("08_BIN/lh_flow_engine.py", TYPE_CLI_COMMAND),
        ("web_apps/src/util_web.py", TYPE_OTHER),
    ]
    for 路径, 期望 in 类型用例:
        if 判定类型(路径) != 期望:
            print(f"❌ 自检失败(分类): {路径} → {判定类型(路径)} ≠ {期望}")
            return False
    return True


def 主程序() -> int:
    解析 = argparse.ArgumentParser(description="新代码 CNSH 命名闸口")
    解析.add_argument("--pre-commit", action="store_true", help="pre-commit 钩子模式")
    解析.add_argument("--repo", action="store_true", help="扫描全仓库新增 .py")
    解析.add_argument("--abom", action="store_true", help="A-BOM 备案统计存量")
    解析.add_argument("--self-check", action="store_true", help="自检")
    解析.add_argument("--json", action="store_true", help="机器可读输出（违规+类型）")
    解析.add_argument("--record", metavar="REASON", help="自动留档（log + md）")
    解析.add_argument("--type", default="", help="类型（逗号分隔: PYTHON_PACKAGE,CLI_COMMAND,...）")
    解析.add_argument("--flow", default="-", help="留档归属流程 ID（PR-<date>-<n>）")
    解析.add_argument("--title", default="CNSH 生态入库", help="留档标题")
    解析.add_argument("--tag", default="", help="md 文件名标签（同日多档区分）")
    解析.add_argument("--pr", default="-", help="PR 号")
    参数 = 解析.parse_args()

    if 参数.self_check:
        结果 = 自检()
        print("✅ 自检全过（命名 + 分类）" if 结果 else "🔴 自检失败")
        return 0 if 结果 else 1

    if 参数.abom:
        统计 = 存量备案()
        print(f"📋 A-BOM 备案 | 存量 .py 总数: {统计['总数']} | 中文命名: {统计.get('中文命名', 0)} | 英文命名: {统计.get('英文命名', 0)}")
        print("   （只统计不改写·存量英文命名脚本不强制改造）")
        return 0

    # 独立留档入口（供 lh publish 或人工调用）
    if 参数.record:
        条目 = {"reason": 参数.record, "flow": 参数.flow, "title": 参数.title,
                "tag": 参数.tag, "pr": 参数.pr, "desc": 参数.title,
                "type": 参数.type or "", "items": []}
        if 参数.type:
            log_append(条目)
        路径 = 留档_md(条目)
        print(f"✅ 已留档: {路径}")
        return 0

    if not (参数.pre_commit or 参数.repo):
        print("用法: lh_cnsh_gate.py --pre-commit | --repo | --abom | --self-check | --record <reason>")
        return 2

    模式 = "pre-commit" if 参数.pre_commit else "repo"
    合规, 违规 = 检查(模式)
    明细 = 违规明细(违规)
    类型集 = sorted({i["type"] for i in 明细})
    描述 = ("中文命名" if not 类型集 else "/".join(类型集))

    if 参数.json:
        # 机器可读：违规+类型（供 lh publish --auto 决策）
        输出 = {"ok": not 违规, "mode": 模式,
                "added_py": len(合规) + len(违规),
                "clean": 合规, "violations": 明细,
                "auto_bypassable": all(i["type"] in KNOWN_TYPES for i in 明细)}
        print(json.dumps(输出, ensure_ascii=False))
        return 0 if not 违规 else 1

    print(f"🔎 新代码闸口 | 模式={模式} | 新增 .py: {len(合规)+len(违规)} 个")
    for 路径 in 合规:
        print(f"   🟢 {路径}")
    if 违规:
        for i in 明细:
            print(f"   🔴 {i['file']} —— 文件名未使用 CNSH 中文命名（type={i['type']}）")
        print("❌ 闸口拦截: 新增 .py 必须 CNSH 中文命名（否则不入库）。存量不改。")
        if all(i["type"] in KNOWN_TYPES for i in 明细):
            print(f"   🟡 三类已知合理冲突（{', '.join(KNOWN_TYPES)}）→ 可 `--record` 留档 + `git commit --no-verify`（规则: docs/闸口绕行规则.md）")
        else:
            print("   🔴 含 OTHER 类型（无法自动归类）→ 禁止自动绕行，请人工 P05 决策留档")
        return 1 if 模式 == "pre-commit" else 0
    print("✅ 闸口通过: 无违规")
    return 0


if __name__ == "__main__":
    sys.exit(主程序())
