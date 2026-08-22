#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂系统 · 结构重组规划脚本
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
文化归属: 思想框架归龍魂核心思想层 (CC BY-NC-SA 4.0)
LAYER: engineering
DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷕贲-RESTRUCTURE-PLAN-v1.0-UID9622
署名: UID9622（诸葛鑫·Lucky）

功能：
  - 根据 SYSTEM_STRUCTURE_AUDIT_v1.0 目标架构生成迁移计划
  - 支持 dry-run 预览
  - 安全执行目录重命名、Symlink 清理、文件移动
  - 生成迁移日志与回滚清单

警告：
  - 本脚本默认 dry-run，不会修改任何文件
  - 使用 --apply 才会真正执行
  - 执行前请确保已备份或版本控制已提交
"""

import os
import json
import sys
import shutil
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Tuple


CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def generate_dna(prefix: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")[:-3]
    import hashlib
    h = hashlib.sha256(f"{prefix}|{ts}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-{prefix}-{h}"


# 预定义迁移映射：当前路径 -> 目标路径
# 注意：这是 Phase 1 的安全迁移（只重命名/移动，不拆内容）
DIRECTORY_RENAMES: List[Tuple[str, str]] = [
    # 协议与治理
    ("01_protocols", "01_PROTOCOLS"),
    ("01_技能庫", "02_SKILLS"),

    # 架构与代码
    ("layers", "03_LAYERS"),
    ("engines", "04_ENGINES"),
    ("services", "05_SERVICES"),
    ("apps", "06_APPS"),
    ("portal", "07_PORTAL"),

    # 数据与资产
    ("articles", "11_ARTICLES"),
    ("docs", "12_DOCS"),
    ("data", "10_DATA"),

    # 归档与工作区
    ("archive", "16_ARCHIVE"),
    ("_archive", "16_ARCHIVE/_legacy_archive"),
    ("_work", "22_WORK"),
    ("_private", "21_PRIVATE"),

    # 应用与子系统
    ("android-auto", "24_ANDROID"),
    ("baobao-guardian", "25_BAOBAO"),
    ("25_TASK_ENGINE", "26_TASK_ENGINE"),

    # CNSH 相关（中文目录）
    ("CNSH_修复输出", "15_LABS/CNSH_修复输出"),
    ("CNSH_加工输出", "15_LABS/CNSH_加工输出"),
    ("CNSH_护盾数据", "15_LABS/CNSH_护盾数据"),
    ("CNSH_监管数据", "15_LABS/CNSH_监管数据"),
]

# 建议删除的 Symlink（相对根目录）
# 这些 Symlink 指向 archive/experiments 或重复入口
SYMLINKS_TO_REMOVE: List[str] = [
    "02_rules",
    "02_執行記錄",
    "03_compiler",
    "04_決策日誌",
    "05_系統報告",
    "06_技術文檔",
    "L1_内核层",
    "L1_身份层",
    "L2_技能层",
    "L2_主权层",
    "L3_数据层",
    "L3_语义层",
    "L3_执行层",
    "L4_数据层",
    "L5_服务层",
    "L6_集成层",
    "L6_记忆层",
    "L6_同步层",
    "L7_表达层",
    "L7_数据层",
    "L8_分发层",
    "L8_治理层",
    "L9_子系统",
    "rag_indexes",
    "calendar-context-logger",
    "skill-standards.integrated",
    "forensic_kernel",
    "memory-universe",
    "ops-console",
    "core",
    "training",
    "backend",
    "backups",
    "benchmarks",
    "arxiv",
    "knowledge-graph",
    "mobile-monitoring.integrated",
    "sovereign-registry",
    "统一入口",
    "人民维权助手",
    "字体",
]

# 保留的 Symlink（过渡期）
PRESERVED_SYMLINKS: List[str] = [
    # "docs",  # 如果 docs 被重命名为 12_DOCS，可以保留 docs -> 12_DOCS 兼容
    # "install.sh" 是文件，不是 symlink
]


class RestructurePlanner:
    def __init__(self, root: Path, target_root: Path = None):
        self.root = root.resolve()
        self.target_root = (target_root or root).resolve()
        self.operations: List[Dict[str, Any]] = []
        self.warnings: List[str] = []
        self.errors: List[str] = []

    def add_op(self, op_type: str, src: Path, dst: Path = None, reason: str = ""):
        self.operations.append({
            "type": op_type,
            "src": str(src.relative_to(self.root)),
            "dst": str(dst.relative_to(self.root)) if dst else None,
            "reason": reason,
        })

    def plan_directory_renames(self):
        """规划目录重命名"""
        for current_name, target_name in DIRECTORY_RENAMES:
            src = self.root / current_name
            dst = self.target_root / target_name

            if not src.exists():
                self.warnings.append(f"源目录不存在，跳过: {current_name}")
                continue

            if dst.exists():
                self.warnings.append(f"目标目录已存在，跳过: {target_name}")
                continue

            self.add_op("rename", src, dst, reason="目录命名规范化")

    def plan_symlink_cleanup(self):
        """规划 Symlink 清理"""
        for link_name in SYMLINKS_TO_REMOVE:
            link_path = self.root / link_name
            if link_path.exists() or link_path.is_symlink():
                self.add_op("remove_symlink", link_path, reason="清理非必要 Symlink")

    def plan_hidden_dir_migration(self):
        """规划隐藏工具目录迁移到 20_CONFIG/"""
        hidden_dirs = [
            ".cnsh", ".codebuddy", ".commander", ".daoyin_workspace",
            ".devcontainer", ".githooks", ".github", ".longhun",
            ".obsidian", ".vscode",
        ]
        for dirname in hidden_dirs:
            src = self.root / dirname
            if not src.exists():
                continue
            # 保留 .github 在根目录（GitHub 要求）
            if dirname == ".github":
                continue
            dst = self.target_root / "20_CONFIG" / dirname
            self.add_op("move_config", src, dst, reason="隐藏工具目录归集到 20_CONFIG/")

    def plan_bin_split(self):
        """规划 bin/ 拆分到 08_BIN/"""
        bin_src = self.root / "bin"
        bin_dst = self.target_root / "08_BIN"

        if not bin_src.exists():
            self.warnings.append("bin/ 目录不存在")
            return

        # 如果 08_BIN 已存在，只迁移文件；否则整体迁移
        if bin_dst.exists():
            self.warnings.append("08_BIN/ 已存在，需要手动合并")
            return

        self.add_op("rename", bin_src, bin_dst, reason="bin/ 重命名为 08_BIN/")

    def generate(self) -> Dict[str, Any]:
        self.plan_directory_renames()
        self.plan_symlink_cleanup()
        self.plan_hidden_dir_migration()
        self.plan_bin_split()

        return {
            "dna": generate_dna("RESTRUCTURE-PLAN"),
            "confirm_code": CONFIRM_CODE,
            "timestamp": _now(),
            "root": str(self.root),
            "target_root": str(self.target_root),
            "operations_count": len(self.operations),
            "operations": self.operations,
            "warnings": self.warnings,
            "errors": self.errors,
        }


def execute_operations(root: Path, operations: List[Dict[str, Any]], dry_run: bool = True) -> Dict[str, Any]:
    """执行或预览迁移操作"""
    results = []

    for op in operations:
        src = root / op["src"]
        dst = root / op["dst"] if op["dst"] else None

        result = {
            "type": op["type"],
            "src": op["src"],
            "dst": op["dst"],
            "status": "pending",
            "error": None,
        }

        if dry_run:
            result["status"] = "dry-run"
            results.append(result)
            continue

        try:
            if op["type"] == "rename":
                if not src.exists():
                    result["status"] = "skipped"
                    result["error"] = "source not found"
                elif dst.exists():
                    result["status"] = "skipped"
                    result["error"] = "destination exists"
                else:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src), str(dst))
                    result["status"] = "done"

            elif op["type"] == "move_config":
                if not src.exists():
                    result["status"] = "skipped"
                    result["error"] = "source not found"
                elif dst.exists():
                    result["status"] = "skipped"
                    result["error"] = "destination exists"
                else:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src), str(dst))
                    result["status"] = "done"

            elif op["type"] == "remove_symlink":
                if src.is_symlink():
                    src.unlink()
                    result["status"] = "done"
                elif src.exists():
                    # 如果存在但不是 symlink，不要删除
                    result["status"] = "skipped"
                    result["error"] = "not a symlink"
                else:
                    result["status"] = "skipped"
                    result["error"] = "not found"

            else:
                result["status"] = "skipped"
                result["error"] = f"unknown operation type: {op['type']}"

        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)

        results.append(result)

    return {
        "dry_run": dry_run,
        "results": results,
        "done": sum(1 for r in results if r["status"] in ("done", "dry-run")),
        "skipped": sum(1 for r in results if r["status"] == "skipped"),
        "failed": sum(1 for r in results if r["status"] == "failed"),
    }


def main():
    parser = argparse.ArgumentParser(description="龍魂系统结构重组规划")
    parser.add_argument("--root", default=".", help="仓库根目录")
    parser.add_argument("--apply", action="store_true", help="真正执行迁移（默认 dry-run）")
    parser.add_argument("--output", default="reports/restructure-plan.json", help="迁移计划输出路径")
    parser.add_argument("--log", default="reports/restructure-log.json", help="执行日志输出路径")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="输出格式")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"错误：根目录不存在 {root}", file=sys.stderr)
        sys.exit(1)

    planner = RestructurePlanner(root)
    plan = planner.generate()

    # 输出迁移计划
    plan_path = Path(args.output)
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"迁移计划已保存: {plan_path}")
    print(f"总操作数: {plan['operations_count']}")
    print(f"警告: {len(plan['warnings'])}")
    print(f"错误: {len(plan['errors'])}")

    if args.format == "markdown":
        md_lines = [
            "# 龍魂系统 · 结构重组计划",
            "",
            f"> DNA: {plan['dna']}",
            f"> 时间: {plan['timestamp']}",
            f"> 根目录: `{plan['root']}`",
            f"> 模式: {'🟢 真实执行' if args.apply else '🟡 预览模式 (dry-run)'} ",
            "",
            f"## 摘要\n\n总操作数: {plan['operations_count']} | 警告: {len(plan['warnings'])} | 错误: {len(plan['errors'])}",
            "",
            "## 操作清单",
            "",
            "| # | 类型 | 源路径 | 目标路径 | 理由 |",
            "|---:|:---|:---|:---|:---|",
        ]
        for i, op in enumerate(plan["operations"], 1):
            md_lines.append(f"| {i} | {op['type']} | `{op['src']}` | `{op['dst'] or '-'}` | {op['reason']} |")

        if plan["warnings"]:
            md_lines.extend(["", "## 警告", ""])
            for w in plan["warnings"]:
                md_lines.append(f"- ⚠️ {w}")

        if plan["errors"]:
            md_lines.extend(["", "## 错误", ""])
            for e in plan["errors"]:
                md_lines.append(f"- 🔴 {e}")

        md_path = plan_path.with_suffix(".md")
        md_path.write_text("\n".join(md_lines), encoding="utf-8")
        print(f"Markdown 计划已保存: {md_path}")

    # 如果 apply，执行迁移
    if args.apply:
        print("\n⚠️  开始真实执行迁移...")
        exec_result = execute_operations(root, plan["operations"], dry_run=False)
        log_path = Path(args.log)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(json.dumps(exec_result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"执行日志已保存: {log_path}")
        print(f"完成: {exec_result['done']} | 跳过: {exec_result['skipped']} | 失败: {exec_result['failed']}")

        if exec_result["failed"] > 0:
            sys.exit(3)
    else:
        print("\n🟡 这是 dry-run 预览。如要执行，请加 --apply")


if __name__ == "__main__":
    main()
