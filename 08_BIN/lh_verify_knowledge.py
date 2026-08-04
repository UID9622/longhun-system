#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 知识拉取验证器 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-VERIFY-HARVEST-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  验证知识拉取是否正常工作
  - 检查生成文件完整性
  - 检查 MISSING_MODULES.md 误报
  - 输出彩色终端报告

用法：
  lh 验证知识拉取
  python3 bin/lh_verify_knowledge.py
  python3 bin/lh_verify_knowledge.py --json
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

PROJECT_ROOT = Path.home() / "longhun-system"
HARVEST_DIR = PROJECT_ROOT / "data" / "harvested_knowledge"
BIN_DIR = PROJECT_ROOT / "bin"

# 期望产出的文件列表
EXPECTED_FILES = [
    "PRINCIPLES.md",
    "RULES.md",
    "MISSING_MODULES.md",
    "CODE_CANDIDATES.md",
    "harvest_report.json",
]

# 已知存在的模块 → bin/ 下的文件名模式
KNOWN_MODULE_PATTERNS = {
    "反虚伪": ["反虚伪", "anti_hypocrisy", "lh_anti"],
    "主权验证": ["主权", "sovereignty", "lh_sovereignty"],
    "省电积分": ["省电", "energy", "lh_energy", "lh_power"],
    "君子协议": ["君子", "gentleman", "lh_gentleman"],
    "掀黑箱": ["掀黑箱", "lh_blackbox", "lh_openbox"],
    "因果推断": ["因果", "causal", "lh_causal"],
    "多智能体": ["多智能", "multi_agent", "lh_multi"],
    "DAG编排": ["dag", "lh_dag", "编排"],
    "神经补全": ["神经", "neural", "lh_neural"],
}


def check_expected_files() -> Dict[str, bool]:
    """检查期望输出文件是否存在"""
    status = {}
    for filename in EXPECTED_FILES:
        filepath = HARVEST_DIR / filename
        status[filename] = filepath.exists()
    return status


def check_missing_modules() -> Dict:
    """检查 MISSING_MODULES.md 中是否存在误报"""
    missing_file = HARVEST_DIR / "MISSING_MODULES.md"
    if not missing_file.exists():
        return {"exists": False, "listed_modules": [], "false_positives": []}

    content = missing_file.read_text(encoding="utf-8")
    # 提取 ### 标题格式的模块名
    listed_modules = re.findall(r'##\s+(.*?)(?:\n|$)', content)

    # 检查每个模块是否在 bin/ 下已有对应文件
    false_positives = []
    all_bin_files = list(BIN_DIR.glob("*.py")) + list(BIN_DIR.glob("*.sh"))
    bin_names_lower = [f.stem.lower() for f in all_bin_files]

    for module_name in listed_modules:
        module_name_clean = module_name.strip()
        patterns = KNOWN_MODULE_PATTERNS.get(module_name_clean, [module_name_clean.lower()])
        for p in patterns:
            p_lower = p.lower()
            if any(p_lower in name for name in bin_names_lower):
                false_positives.append({
                    "module": module_name_clean,
                    "matched_files": [f.stem for f in all_bin_files if p_lower in f.stem.lower()],
                })
                break

    return {
        "exists": True,
        "listed_modules": listed_modules,
        "false_positives": false_positives,
    }


def verify() -> Tuple[Dict, str, str]:
    """主验证逻辑，返回 (结果字典, 总体状态, 状态色)"""
    result = {
        "timestamp": datetime.now().isoformat(),
        "files": {},
        "missing_analysis": {},
        "score": 100,
        "issues": [],
    }

    # 1. 文件完整性检查
    file_status = check_expected_files()
    result["files"] = file_status
    missing_files = [f for f, ok in file_status.items() if not ok]
    if missing_files:
        result["issues"].append(f"缺失文件: {', '.join(missing_files)}")
        result["score"] -= len(missing_files) * 15

    # 2. 缺失模块误报检查
    missing_analysis = check_missing_modules()
    result["missing_analysis"] = missing_analysis

    if missing_analysis["exists"]:
        fp = missing_analysis["false_positives"]
        if fp:
            fp_names = [f["module"] for f in fp]
            result["issues"].append(f"误报模块 ({len(fp)}个): {', '.join(fp_names)}")
            result["score"] -= len(fp) * 10

        # 如果没有任何模块列出 = 完全健康
        if not missing_analysis["listed_modules"]:
            result["score"] = 100
    else:
        result["issues"].append("MISSING_MODULES.md 不存在（尚未运行拉取？）")
        result["score"] -= 20

    # 3. 判定总体状态
    score = max(0, min(100, result["score"]))
    result["score"] = score
    if score >= 90:
        result["status"] = "🟢 健康"
    elif score >= 60:
        result["status"] = "🟡 一般"
    else:
        result["status"] = "🔴 需关注"
    result["color"] = "green" if score >= 90 else "yellow" if score >= 60 else "red"

    return result, result["status"], result["color"]


def terminal_output():
    """终端彩色输出"""
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

    result, status, color = verify()

    color_map = {"green": GREEN, "yellow": YELLOW, "red": RED}

    print(f"\n{BOLD}🐉 知识拉取验证器{RESET}")
    print("=" * 56)
    print(f"评分: {result['score']}/100  {status}")
    print(f"时间: {result['timestamp'][:19]}")
    print("-" * 56)

    # 文件状态
    print(f"\n{BOLD}📄 生成文件状态:{RESET}")
    for f, exists in result["files"].items():
        icon = f"{GREEN}✅{RESET}" if exists else f"{RED}❌{RESET}"
        size_info = ""
        if exists:
            size = (HARVEST_DIR / f).stat().st_size
            size_info = f" ({size:,}B)"
        print(f"  {icon} {f}{size_info}")

    # 缺失模块分析
    ma = result["missing_analysis"]
    print(f"\n{BOLD}📋 缺失模块分析:{RESET}")
    if ma["exists"]:
        listed = ma["listed_modules"]
        fp = ma["false_positives"]
        print(f"  列出模块: {len(listed)} 个")
        if fp:
            print(f"  {YELLOW}⚠️ 误报模块: {len(fp)} 个（已有对应文件）{RESET}")
            for f_item in fp:
                print(f"    - {f_item['module']} → 已存在: {', '.join(f_item['matched_files'][:3])}")
        else:
            print(f"  {GREEN}✅ 无误报{RESET}")
    else:
        print(f"  {RED}❌ MISSING_MODULES.md 不存在{RESET}")

    # 问题汇总
    if result["issues"]:
        print(f"\n{YELLOW}⚠️ 发现 {len(result['issues'])} 个问题:{RESET}")
        for issue in result["issues"]:
            print(f"  - {issue}")
    else:
        print(f"\n{GREEN}✅ 所有检查通过{RESET}")

    print("-" * 56)
    if result["score"] >= 90:
        print(f"{GREEN}✅ 知识拉取状态: 完全健康{RESET}\n")
    elif result["score"] >= 60:
        print(f"{YELLOW}🟡 知识拉取状态: 文件齐全，存在少量问题{RESET}\n")
    else:
        print(f"{RED}🔴 知识拉取状态: 需要重新运行 lh 知识拉取 --force{RESET}\n")


def json_output():
    """JSON 输出"""
    result, _, _ = verify()
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龙魂 · 知识拉取验证器")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    args = parser.parse_args()

    if args.json:
        json_output()
    else:
        terminal_output()


if __name__ == "__main__":
    main()
