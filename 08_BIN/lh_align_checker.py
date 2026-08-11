#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂·代码对齐复盘器 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-对齐复盘-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

功能：扫描指定目录下所有 Python/Shell 文件，提取函数/类定义，
      检测重复功能、不一致命名、文件头缺失、GPG签名缺失，
      输出对齐报告。每次 AI 进门自动执行。

用法：
    python3 lh_align_checker.py [--dir 目录] [--report 报告文件] [--json]
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# ========== 配置 ==========
DEFAULT_TARGET_DIR = Path.home() / "longhun-system"
EXCLUDE_DIRS = {
    ".git", "__pycache__", ".venv", "venv", "node_modules",
    ".idea", ".vscode", "dist", "build", "egg-info",
}
# 排除的扫描子目录（第三方/历史遗留/大目录/备份归档/缓存副本/venv）
SKIP_SCAN_DIRS = {
    # 大目录/历史遗留
    "L7_数据层", "L1_内核层", "L8_治理层",
    "L4_数据层", "L3_数据层", "L6_记忆层", "L9_子系统",
    "CNSH_颜色历史", "CNSH_加工输出", "CNSH_修复输出", "CNSH_监管数据", "CNSH_护盾数据",
    # 第三方/供应商代码
    "05_ENGINES/gpt_sovits",      # GPT-SoVITS 第三方模型
    "05_ENGINES/video",            # 视频编码器第三方代码
    "engines/core",
    "09_TOOLS/bin/legacy_bin",     # 遗留工具
    # 知识图谱/执行记录/系统报告（参考文档）
    "03_知識圖譜", "02_執行記錄", "05_系統報告",
    "协议文档", "_work", "archive", "_archive",
    "backups", "backup",
    # 备份目录
    "11_DATA/backups",             # 数据备份归档
    "11_DATA/knowledge_pull/cache", # 知识拉取缓存
    # 独立子项目/实验目录
    "baobao-guardian",
    "research",
    "experiments",
    "15_LABS",
    # 协议/文档归档
    "01_protocols/downloads_archive",
    "01_技能庫/downloads_archive",
    "02_SKILLS/downloads_archive",
    "governance/protocols/P2_system/downloads_archive",
    "docs/claude-backlog",
    "data/training/home_absorb/sources/claude搭建待整理",
    # 缓存/训练数据/工作区
    "data/training/home_absorb/workspace/Desktop/龍魂系统-知识库/_archive",
    "data/training/home_absorb/workspace/Desktop/桌面项目箱",
    "data/training/home_absorb/workspace/_work",
    "tombstone_vault",
    "integrated_modules",
    "models",                      # 模型文件
    "dist",                        # 构建产物
    # Python/Node 虚拟环境
    "cnsh/core/runtime_governance/venv_notion",
    "data/training/home_absorb/sources/龍魂系统/运行环境",
    # 训练/融合模型
    "train", "training", "fused_model",
    # Rust/编译目标
    "rust",
    # 前端构建产物
    "web_apps", "web/node_modules",
}

EXCLUDE_FILES = {"setup.py", "conftest.py", "__init__.py"}

# 正则
FUNC_PATTERN = re.compile(r'^\s*def\s+(\w+)\s*\(', re.MULTILINE)
CLASS_PATTERN = re.compile(r'^\s*class\s+(\w+)\s*[\(:]', re.MULTILINE)
FUNC_BASH_PATTERN = re.compile(r'^\s*(?:function\s+)?(\w+)\s*\(\s*\)\s*\{?', re.MULTILINE)
DNA_PATTERN = re.compile(r'DNA:\s*(#?[^\n]+)', re.MULTILINE)
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


def scan_files(target_dir):
    """扫描目录下所有 .py/.sh 文件"""
    results = []
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        if not should_scan_dir(root, target_dir):
            dirs[:] = []  # 不深入子目录
            continue
        for file in files:
            if not (file.endswith('.py') or file.endswith('.sh')):
                continue
            if file in EXCLUDE_FILES:
                continue
            filepath = Path(root) / file
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"⚠️ 读取失败 {filepath}: {e}")
                continue

            is_py = file.endswith('.py')
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

            results.append({
                "file": str(filepath.relative_to(target_dir)),
                "functions": all_funcs,
                "classes": classes,
                "has_dna": bool(dna),
                "has_confirm": bool(confirm),
                "has_gpg": has_gpg,
                "dna_text": dna.group(1).strip() if dna else "",
                "confirm_text": (confirm.group(1).strip() if confirm.group(1) else CONFIRM_MARK) if confirm else "",
                "line_count": len(content.splitlines()),
                "imports": imports,
            })
    return results


def analyze_alignment(results):
    """分析重复、相似、缺失"""
    # 1. 全局函数索引
    func_index = defaultdict(list)
    for item in results:
        for func in item["functions"]:
            func_index[func].append(item["file"])

    # 2. 重复函数
    dup_threshold = 1
    duplicates = {
        f: files for f, files in func_index.items()
        if len(files) > dup_threshold and not f.startswith('_')
    }

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

    # 重复
    if report["duplicates"]:
        print(f"\n{R}🔴 重复函数（{len(report['duplicates'])}组）{Z}")
        for func, files in sorted(report["duplicates"].items()):
            print(f"  {Y}{func}{Z} → {len(files)}个文件:")
            for f in files[:5]:
                print(f"      - {f}")
    else:
        print(f"\n{G}✅ 无重复函数{Z}")

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
    args = parser.parse_args()
    # --no-print 等价于 --json（daemon兼容）
    if args.no_print:
        args.json = True

    target_dir = Path(args.dir)
    if not target_dir.exists():
        print(f"❌ {target_dir} 不存在", file=sys.stderr)
        sys.exit(2)

    if not args.quiet:
        print(f"🔍 扫描: {target_dir}", file=sys.stderr)

    raw = scan_files(target_dir)
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
