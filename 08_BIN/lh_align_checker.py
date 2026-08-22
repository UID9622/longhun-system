#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂·代码对齐复盘器 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·庚午·䷝离为火-对齐复盘-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

功能：扫描指定目录下所有 Python/Shell 文件，提取函数/类定义，
      检测重复功能、不一致命名、文件头缺失、GPG签名缺失，
      输出对齐报告。每次 AI 进门自动执行。

用法：
    python3 lh_align_checker.py [--dir 目录] [--report 报告文件] [--json]
    python3 lh_align_checker.py --dir 目录 --files a.py b.sh --json
        # --files: 只审计指定文件（相对target_dir）· git钩子只审变更文件用
        # 修正 (2026-08-22): pre-commit 阶段三全库红线堵死提交 → 只审本次暂存区变更
"""

import os
import sys
import re
import json
import ast
import hashlib
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# ========== 配置 ==========
DEFAULT_TARGET_DIR = Path.home() / "longhun-system"
EXCLUDE_DIRS = {
    ".git", "__pycache__", ".venv", "venv", "node_modules",
    ".idea", ".vscode", "dist", "build", "egg-info",
    # 修正 (P77 黑天使审计 2026-08-14): 归档目录按"不删除只冻结"保留但不得当活动代码审计
    "_archive", "quarantine", "deprecated",
}
EXCLUDE_FILES = {"setup.py", "conftest.py", "__init__.py"}

# 共享排除配置路径（单一真相源）
_SHARED_CONFIG_PATH = Path(__file__).resolve().parent.parent / ".codebuddy/rules/scan-exclusions.json"


def _load_shared_exclusions():
    """从 scan-exclusions.json 加载共享排除配置，合并到 SKIP_SCAN_DIRS"""
    try:
        if _SHARED_CONFIG_PATH.exists():
            with open(_SHARED_CONFIG_PATH, "r", encoding="utf-8") as f:
                shared = json.load(f)
            ed = shared.get("excluded_dirs", {})
            for category in ed:
                for d in ed[category]:
                    if d not in _HARDCODED_SKIP_SCAN_DIRS and d not in SKIP_SCAN_DIRS:
                        SKIP_SCAN_DIRS.add(d)
    except Exception:
        pass  # 降级：使用硬编码兜底


# 硬编码兜底排除目录（共享配置不可达时使用）
_HARDCODED_SKIP_SCAN_DIRS = {
    "L7_数据层", "L1_内核层", "L8_治理层",
    "L4_数据层", "L3_数据层", "L6_记忆层", "L9_子系统",
    # 修正 (P77 黑天使审计 2026-08-14): 03_LAYERS 下的层实现区同样排除 (SKIP 裸名匹配不到 03_LAYERS/ 前缀)
    "03_LAYERS/L1_内核层", "03_LAYERS/L2_主权层", "03_LAYERS/L3_语义层", "03_LAYERS/L3_执行层",
    "03_LAYERS/L4_数据层", "03_LAYERS/L5_服务层", "03_LAYERS/L6_同步层", "03_LAYERS/L6_记忆层",
    "03_LAYERS/L7_数据层", "03_LAYERS/L7_表达层", "03_LAYERS/L8_分发层", "03_LAYERS/L8_治理层",
    "03_LAYERS/L9_子系统",
    "CNSH_颜色历史", "CNSH_加工输出", "CNSH_修复输出", "CNSH_监管数据", "CNSH_护盾数据",
    "05_ENGINES/gpt_sovits", "05_ENGINES/video",
    "engines/core", "09_TOOLS/bin/legacy_bin",
    "03_知識圖譜", "02_執行記錄", "05_系統報告",
    "协议文档", "_work", "archive", "_archive", "backups", "backup",
    "11_DATA/backups", "11_DATA/knowledge_pull/cache",
    "baobao-guardian", "research", "experiments", "15_LABS",
    "01_protocols/downloads_archive", "01_技能庫/downloads_archive",
    "02_SKILLS/downloads_archive",
    "governance/protocols/P2_system/downloads_archive",
    "docs/claude-backlog",
    "data/training/home_absorb/sources/claude搭建待整理",
    "data/training/home_absorb/workspace/Desktop/龍魂系统-知识库/_archive",
    # 修正 (P77 黑天使审计 2026-08-14): 实际路径是 11_DATA/ 前缀 + 简体「龍」; training 整目录为数据吸收区非活动代码
    "11_DATA/training/home_absorb/workspace/Desktop/龍魂系统-知识库/_archive",
    "11_DATA/training/home_absorb/workspace/Desktop/龍魂系统-知识库/_archive",
    "11_DATA/training",
    # 修正 (P77 黑天使审计 2026-08-14): 下载导入区/外部导入区/数据区均为吸收区非活动代码
    "cnsh/core/downloads_imports", "imports/", "11_DATA",
    "data/training/home_absorb/workspace/Desktop/桌面项目箱",
    "data/training/home_absorb/workspace/_work",
    "tombstone_vault", "integrated_modules",
    "models", "dist",
    "cnsh/core/runtime_governance/venv_notion",
    "data/training/home_absorb/sources/龍魂系统/运行环境",
    "train", "training", "fused_model", "rust",
    "web_apps", "web/node_modules",
}

# 排除的扫描子目录（合并：硬编码兜底 + 共享配置加载）
SKIP_SCAN_DIRS = set(_HARDCODED_SKIP_SCAN_DIRS)

# 加载共享排除配置（追加到 SKIP_SCAN_DIRS）
_load_shared_exclusions()

# 正则
FUNC_PATTERN = re.compile(r'^\s*def\s+(\w+)\s*\(', re.MULTILINE)
CLASS_PATTERN = re.compile(r'^\s*class\s+(\w+)\s*[\(:]', re.MULTILINE)
FUNC_BASH_PATTERN = re.compile(r'^\s*(?:function\s+)?(\w+)\s*\(\s*\)\s*\{?', re.MULTILINE)
DNA_PATTERN = re.compile(r'(?:#\s*DNA:\s*)?(#?龍芯⚡️[^\n]*)', re.MULTILINE)
CONFIRM_MARK = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
CONFIRM_PATTERN = re.compile(r'CONFIRM:\s*(#?[^\n]+)|' + re.escape(CONFIRM_MARK), re.MULTILINE)
IMPORT_PATTERN = re.compile(r'^\s*(?:from\s+(\S+)\s+)?import\s+(.+)$', re.MULTILINE)


def should_scan_dir(dirpath, root):
    """判断目录是否应扫描"""
    rel = str(Path(dirpath).relative_to(root))
    for skip in SKIP_SCAN_DIRS:
        if rel.startswith(skip) or rel == skip:
            return False
    return True


def _scan_one_file(filepath, target_dir):
    """扫描单个文件，返回对齐条目（非 .py/.sh 或排除文件返回 None）"""
    name = filepath.name
    if not (name.endswith('.py') or name.endswith('.sh')):
        return None
    if name in EXCLUDE_FILES:
        return None
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"⚠️ 读取失败 {filepath}: {e}")
        return None

    is_py = name.endswith('.py')
    functions = FUNC_PATTERN.findall(content)
    classes = CLASS_PATTERN.findall(content) if is_py else []
    bash_funcs = FUNC_BASH_PATTERN.findall(content) if not is_py else []
    all_funcs = functions + bash_funcs
    # imports (py only)
    imports = []
    if is_py:
        imports = [m.group(0).strip() for m in IMPORT_PATTERN.finditer(content)]

    dna = DNA_PATTERN.search(content)
    confirm = CONFIRM_PATTERN.search(content)

    # 检查是否存在 .asc 签名文件
    asc_path = filepath.with_suffix(filepath.suffix + '.asc')
    has_gpg = asc_path.exists()

    # v2.1(2026-08-22): 函数体hash（用于"同名+同体"真重复判定，区分同名噪音）
    #   只提取模块顶层 + 类方法层，避免嵌套局部函数误判；解析失败降级为空
    func_bodies = {}
    if is_py:
        try:
            tree = ast.parse(content)
            _fb = defaultdict(list)
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    seg = ast.get_source_segment(content, node) or ""
                    _fb[node.name].append(hashlib.sha256(seg.encode()).hexdigest())
                elif isinstance(node, ast.ClassDef):
                    for m in node.body:
                        if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            seg = ast.get_source_segment(content, m) or ""
                            _fb[m.name].append(hashlib.sha256(seg.encode()).hexdigest())
            func_bodies = dict(_fb)
        except Exception:
            func_bodies = {}

    return {
        "file": str(filepath.relative_to(target_dir)),
        "functions": all_funcs,
        "classes": classes,
        "func_bodies": func_bodies,
        "has_dna": bool(dna),
        "has_confirm": bool(confirm),
        "has_gpg": has_gpg,
        "dna_text": dna.group(1).strip() if dna else "",
        "confirm_text": (confirm.group(1).strip() if confirm.group(1) else CONFIRM_MARK) if confirm else "",
        "line_count": len(content.splitlines()),
        "imports": imports,
    }


def scan_files(target_dir, only_files=None):
    """扫描 .py/.sh 文件。
    only_files 指定时只审计这些文件（相对 target_dir 的路径列表，git钩子用），
    否则全目录扫描。"""
    results = []
    if only_files is not None:
        for rel in only_files:
            # 只接受相对路径，防路径穿越
            if rel.startswith('/') or '..' in Path(rel).parts:
                continue
            filepath = (target_dir / rel).resolve()
            if not filepath.exists() or not filepath.is_file():
                continue
            parent = filepath.parent
            # 排除目录检查（与全目录模式一致）
            if not should_scan_dir(parent, target_dir):
                continue
            if parent.name in EXCLUDE_DIRS:
                continue
            item = _scan_one_file(filepath, target_dir)
            if item:
                results.append(item)
        return results

    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        if not should_scan_dir(root, target_dir):
            dirs[:] = []  # 不深入子目录
            continue
        for file in files:
            filepath = Path(root) / file
            item = _scan_one_file(filepath, target_dir)
            if item:
                results.append(item)
    return results


def analyze_alignment(results):
    """分析重复、相似、缺失"""
    # 1. 全局函数索引
    func_index = defaultdict(list)
    for item in results:
        for func in item["functions"]:
            func_index[func].append(item["file"])

    # 2. 重复函数
    # v2.0降噪(2026-08-21): 通用函数名黑名单——main/init/run等高频通用名不视为"重复定义"，
    #   修复 auto_align 每小时扫出 24951 组噪音(此前大量同名通用函数被误报为重复)
    GENERIC_FUNC_NAMES = {
        "main", "init", "run", "start", "stop", "setup", "cleanup", "test",
        "load", "save", "read", "write", "get", "set", "build", "check",
        "verify", "parse", "process", "create", "update", "delete", "config",
        "app", "handler", "handle", "main_", "_main", "main_func", "run_main",
        "do_run", "main_run", "runner", "bootstrap", "initialize", "reset",
        "ping", "health", "version", "usage", "help",
    }
    dup_threshold = 1
    duplicates = {
        f: files for f, files in func_index.items()
        if len(files) > dup_threshold
        and not f.startswith('_')
        and f not in GENERIC_FUNC_NAMES
    }

    # v2.1(2026-08-22): 真重复判定——同名且函数体一致才算真重复，区分同名噪音。
    #   可配 lh_fix_duplicate_functions.py 自动去重（同文件同体）。
    true_duplicates = {}
    same_name_diff_impl = {}
    for f, files in duplicates.items():
        hashes_by_file = {}
        for item in results:
            if item["file"] in files:
                hs = (item.get("func_bodies") or {}).get(f)
                if hs:
                    hashes_by_file[item["file"]] = set(hs)
        if not hashes_by_file:
            continue  # 无法解析AST（如 sh/bash），维持原名判重
        try:
            common = set.intersection(*hashes_by_file.values())
        except TypeError:
            common = set()
        if common:
            true_duplicates[f] = sorted(hashes_by_file.keys())
        else:
            same_name_diff_impl[f] = sorted(hashes_by_file.keys())

    # 3. 相似函数名（公共前缀≥5或编辑距离小）
    all_funcs = sorted(set(func_index.keys()))
    similar_pairs = []
    for i in range(len(all_funcs)):
        for j in range(i+1, len(all_funcs)):
            a, b = all_funcs[i], all_funcs[j]
            if a == b:
                continue
            prefix = os.path.commonprefix([a, b])
            # 长公共前缀 或 互相包含
            if len(prefix) >= 5 or a in b or b in a:
                similar_pairs.append((a, b))

    # 4. 缺失检查
    missing_dna = [item["file"] for item in results if not item["has_dna"]]
    missing_confirm = [item["file"] for item in results if not item["has_confirm"]]
    missing_gpg = [item["file"] for item in results if not item["has_gpg"]]

    # 5. 统计
    total_lines = sum(item["line_count"] for item in results)
    total_funcs = sum(len(item["functions"]) for item in results)
    total_classes = sum(len(item["classes"]) for item in results)

    # 6. 评分：0-100，各项扣分
    score = 100
    if duplicates:
        score -= min(len(duplicates) * 3, 30)
    if similar_pairs:
        score -= min(len(similar_pairs) * 1, 15)
    if missing_dna:
        score -= min(len(missing_dna) * 2, 20)
    if missing_gpg:
        score -= min(len(missing_gpg) * 2, 20)
    score = max(score, 0)

    return {
        "total_files": len(results),
        "total_functions": total_funcs,
        "total_classes": total_classes,
        "total_lines": total_lines,
        "alignment_score": score,
        "duplicates": duplicates,
        "true_duplicates": true_duplicates,
        "same_name_diff_impl": same_name_diff_impl,
        "similar_pairs": similar_pairs[:30],
        "missing_dna": missing_dna,
        "missing_confirm": missing_confirm,
        "missing_gpg": missing_gpg,
        "all_items": results,
    }


def print_report(report, json_output=False):
    """终端打印报告 或 JSON输出"""
    if json_output:
        print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
        return

    B = '\033[1m'
    R = '\033[91m'
    Y = '\033[93m'
    G = '\033[92m'
    C = '\033[96m'
    Z = '\033[0m'

    print(f"\n{B}{'='*65}{Z}")
    print(f"{B}🐉 龍魂代码对齐复盘报告{Z}")
    print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  文件: {report['total_files']}  |  函数: {report['total_functions']}  |  类: {report['total_classes']}  |  总行: {report['total_lines']:,}")
    print(f"  对齐评分: {report['alignment_score']}/100")
    print(f"{B}{'='*65}{Z}")

    # 重复（v2.1: 区分真重复 vs 同名异实现·降噪）
    true_dups = report.get("true_duplicates") or {}
    same_diff = report.get("same_name_diff_impl") or {}
    if true_dups:
        print(f"\n{R}🔴 真重复函数（同名+同体·{len(true_dups)}组·可配 lh_fix_duplicate_functions.py 去重）{Z}")
        for func, files in sorted(true_dups.items())[:20]:
            print(f"  {Y}{func}{Z} → {len(files)}个文件:")
            for f in files[:5]:
                print(f"      - {f}")
        if len(true_dups) > 20:
            print(f"  ... 还有 {len(true_dups)-20} 组")
    elif report["duplicates"]:
        print(f"\n{G}✅ 无真重复函数（同名但实现不同·正常）{Z}")
    else:
        print(f"\n{G}✅ 无重复函数{Z}")

    if same_diff:
        print(f"\n{Y}🟡 同名异实现（{len(same_diff)}组·各模块独立实现·通常正常）{Z}")
        for func, files in sorted(same_diff.items())[:8]:
            print(f"  {func} → {len(files)}个文件")

    # 相似
    if report["similar_pairs"]:
        print(f"\n{Y}🟡 相似函数名（{len(report['similar_pairs'])}对·可能功能重叠）{Z}")
        for a, b in report["similar_pairs"][:15]:
            print(f"  {a} ↔ {b}")
    else:
        print(f"\n{G}✅ 无显著相似{Z}")

    # 缺失DNA
    if report["missing_dna"]:
        print(f"\n{R}🔴 缺失DNA签章: {len(report['missing_dna'])} 个文件{Z}")
        for f in report["missing_dna"][:12]:
            print(f"  - {f}")
        if len(report["missing_dna"]) > 12:
            print(f"  ... 还有 {len(report['missing_dna']) - 12} 个")
    else:
        print(f"\n{G}✅ 所有文件含DNA{Z}")

    # 缺失GPG
    if report["missing_gpg"]:
        print(f"\n{R}🔴 缺失GPG签名: {len(report['missing_gpg'])} 个文件{Z}")
        for f in report["missing_gpg"][:12]:
            print(f"  - {f}")
        if len(report["missing_gpg"]) > 12:
            print(f"  ... 还有 {len(report['missing_gpg']) - 12} 个")

    # 建议
    print(f"\n{C}📊 建议:{Z}")
    if report["duplicates"]:
        print("  ▸ 合并同名函数或加前缀区分用途")
    if report["similar_pairs"]:
        print("  ▸ 相似函数可抽象为公共函数")
    if report["missing_dna"]:
        print("  ▸ 补充DNA签章: #龍芯⚡️YYYY-MM-DD-功能-v1.0")
    if report["missing_gpg"]:
        print("  ▸ 补签名: python3 bin/lh_gpg_sign.py sign --force .")
    if report["alignment_score"] >= 90:
        print(f"  {G}▸ 总体健康 · 评分 {report['alignment_score']}/100{Z}")

    print(f"{B}{'='*65}{Z}\n")


def save_json_report(report, output_path):
    """保存JSON报告"""
    report_copy = {k: v for k, v in report.items() if k != "all_items"}
    report_copy["top_duplicates"] = list(report["duplicates"].keys())[:20]
    report_copy["top_true_duplicates"] = list((report.get("true_duplicates") or {}).keys())[:20]
    report_copy["timestamp"] = datetime.now().isoformat()

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report_copy, f, ensure_ascii=False, indent=2, default=str)
    print(f"✅ JSON报告: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="龍魂代码对齐复盘器·每次AI进门自动执行")
    parser.add_argument("--dir", type=str, default=str(DEFAULT_TARGET_DIR),
                        help=f"目标目录 (默认: {DEFAULT_TARGET_DIR})")
    parser.add_argument("--report", type=str, help="输出JSON报告路径")
    parser.add_argument("--json", action="store_true", help="终端输出JSON格式（管道友好）")
    parser.add_argument("--no-print", action="store_true", help="同--json·管道友好（lh_auto_align_daemon调用）")
    parser.add_argument("--quiet", action="store_true", help="静默模式·仅输出退出码(0=ok, 1=有问题)")
    parser.add_argument("--files", nargs="+", default=None,
                        help="只审计指定文件（相对target_dir的路径，空格分隔）· git钩子只审变更文件用")
    args = parser.parse_args()
    # --no-print 等价于 --json（daemon兼容）
    if args.no_print:
        args.json = True

    target_dir = Path(args.dir).resolve()
    if not target_dir.exists():
        print(f"❌ {target_dir} 不存在", file=sys.stderr)
        sys.exit(2)

    if not args.quiet:
        if args.files:
            print(f"🔍 仅审计 {len(args.files)} 个变更文件: {target_dir}", file=sys.stderr)
        else:
            print(f"🔍 扫描: {target_dir}", file=sys.stderr)

    raw = scan_files(target_dir, only_files=args.files)
    if not raw:
        if args.quiet:
            sys.exit(0)
        print("⚠️ 未找到可扫描文件", file=sys.stderr)
        return

    report = analyze_alignment(raw)

    if args.report:
        save_json_report(report, args.report)

    if args.quiet:
        has_issues = bool(report["duplicates"] or report["missing_dna"] or report["missing_gpg"])
        sys.exit(1 if has_issues else 0)

    print_report(report, json_output=args.json)


if __name__ == "__main__":
    main()
