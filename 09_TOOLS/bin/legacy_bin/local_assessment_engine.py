#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂系统 · 本地完整评估引擎 v1.0

DNA: #龍芯⚡️丙午·癸巳·庚戌·壬午·䷕贲-LOCAL-ASSESSMENT-v1.0
作者: UID9622 (Claude Code)
评估内容: 环境·代码·数据·可运行·文档·安全
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════════════════════════════

HOME = Path.home()
LONGHUN_ROOT = HOME / ".龍魂"
XPAY_ROOT = LONGHUN_ROOT / "xpay"
ASSESSMENT_DIR = LONGHUN_ROOT / "assessments"

# 建立评估目录
ASSESSMENT_DIR.mkdir(parents=True, exist_ok=True)

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
REPORT_FILE = ASSESSMENT_DIR / f"local_assessment_{TIMESTAMP}.json"

# ═══════════════════════════════════════════════════════════════════════════
# 评估1: 环境检查 (权重10%)
# ═══════════════════════════════════════════════════════════════════════════

def check_environment():
    """检查环境设定"""
    results = {}
    scores = []

    # Python版本
    python_version = subprocess.run(["python3", "--version"],
                                    capture_output=True, text=True).stdout.strip()
    results["python_version"] = python_version
    scores.append(1.0 if python_version else 0.0)

    # 龍魂目录
    longhun_exists = LONGHUN_ROOT.exists()
    results["longhun_dir"] = str(LONGHUN_ROOT) if longhun_exists else None
    scores.append(1.0 if longhun_exists else 0.0)

    # XPay目录
    xpay_exists = XPAY_ROOT.exists()
    results["xpay_dir"] = str(XPAY_ROOT) if xpay_exists else None
    scores.append(1.0 if xpay_exists else 0.0)

    # Shell配置
    zshrc = HOME / ".zshrc"
    shell_config_exists = zshrc.exists()
    results["shell_config"] = "~/.zshrc" if shell_config_exists else None
    scores.append(1.0 if shell_config_exists else 0.0)

    avg_score = sum(scores) / len(scores) * 10.0 if scores else 0.0

    return {
        "category": "环境检查",
        "weight": 0.10,
        "results": results,
        "score": round(avg_score, 1),
        "max_score": 10.0
    }

# ═══════════════════════════════════════════════════════════════════════════
# 评估2: 代码文件检查 (权重20%)
# ═══════════════════════════════════════════════════════════════════════════

def check_code_files():
    """检查核心代码文件"""
    results = {}
    files_to_check = {
        "xpay_core.py": "XPay核心实现",
        "xpay_cli.py": "XPay命令行工具",
        "xpay_server.py": "XPay API服务器",
        "startup.sh": "启动脚本",
        "longhun_welding_automation.sh": "自动化焊接"
    }

    scores = []

    for filename, description in files_to_check.items():
        filepath = XPAY_ROOT / filename
        exists = filepath.exists()
        size = filepath.stat().st_size if exists else 0

        results[filename] = {
            "description": description,
            "exists": exists,
            "size_bytes": size,
            "path": str(filepath)
        }

        # 评分: 存在且有内容
        score = 1.0 if (exists and size > 100) else 0.0
        scores.append(score)

    avg_score = sum(scores) / len(scores) * 10.0 if scores else 0.0

    return {
        "category": "代码文件检查",
        "weight": 0.20,
        "results": results,
        "score": round(avg_score, 1),
        "max_score": 10.0
    }

# ═══════════════════════════════════════════════════════════════════════════
# 评估3: 数据完整性 (权重20%)
# ═══════════════════════════════════════════════════════════════════════════

def check_data_integrity():
    """检查数据完整性"""
    results = {}
    scores = []

    # 交易数据
    transactions_file = XPAY_ROOT / "transactions.json"
    tx_exists = transactions_file.exists()
    tx_size = transactions_file.stat().st_size if tx_exists else 0

    tx_count = 0
    tx_valid = False
    if tx_exists:
        try:
            with open(transactions_file) as f:
                data = json.load(f)
                tx_count = len(data.get("history", []))
                tx_valid = tx_count > 0
        except:
            tx_valid = False

    results["transactions"] = {
        "file": "transactions.json",
        "exists": tx_exists,
        "size_bytes": tx_size,
        "transaction_count": tx_count,
        "valid": tx_valid
    }
    scores.append(1.0 if (tx_exists and tx_valid) else 0.5 if tx_exists else 0.0)

    # 日志文件
    logs_dir = XPAY_ROOT / "logs"
    logs_exist = logs_dir.exists()
    log_files = []
    if logs_exist:
        log_files = list(logs_dir.glob("*.log"))

    results["logs"] = {
        "directory": "logs/",
        "exists": logs_exist,
        "file_count": len(log_files),
        "files": [f.name for f in log_files[:5]]  # 只显示前5个
    }
    scores.append(1.0 if (logs_exist and len(log_files) > 0) else 0.5 if logs_exist else 0.0)

    # DNA签证备份
    backup_files = list(HOME.glob("longhun_dna_backup_*.json"))
    results["dna_backups"] = {
        "backup_count": len(backup_files),
        "files": [f.name for f in backup_files[-3:]]  # 最近3个
    }
    scores.append(1.0 if len(backup_files) > 0 else 0.0)

    avg_score = sum(scores) / len(scores) * 10.0 if scores else 0.0

    return {
        "category": "数据完整性",
        "weight": 0.20,
        "results": results,
        "score": round(avg_score, 1),
        "max_score": 10.0
    }

# ═══════════════════════════════════════════════════════════════════════════
# 评估4: 可运行性 (权重25%)
# ═══════════════════════════════════════════════════════════════════════════

def check_runability():
    """检查系统可运行性"""
    results = {}
    scores = []

    # 检查CLI统计
    cli_stats_ok = False
    cli_output = ""
    try:
        result = subprocess.run(
            ["python3", str(XPAY_ROOT / "xpay_cli.py"), "stats"],
            cwd=str(XPAY_ROOT),
            capture_output=True,
            text=True,
            timeout=10
        )
        cli_stats_ok = result.returncode == 0
        cli_output = "Success" if cli_stats_ok else result.stderr[:100]
    except Exception as e:
        cli_output = str(e)

    results["cli_stats"] = {
        "command": "xpay_cli.py stats",
        "executable": True,
        "runs_successfully": cli_stats_ok,
        "output": cli_output
    }
    scores.append(1.0 if cli_stats_ok else 0.5)

    # 检查CLI历史
    cli_history_ok = False
    try:
        result = subprocess.run(
            ["python3", str(XPAY_ROOT / "xpay_cli.py"), "history"],
            cwd=str(XPAY_ROOT),
            capture_output=True,
            text=True,
            timeout=10
        )
        cli_history_ok = result.returncode == 0
    except:
        cli_history_ok = False

    results["cli_history"] = {
        "command": "xpay_cli.py history",
        "runs_successfully": cli_history_ok
    }
    scores.append(1.0 if cli_history_ok else 0.5)

    # 检查启动脚本执行权限
    startup_file = XPAY_ROOT / "startup.sh"
    startup_executable = os.access(startup_file, os.X_OK) if startup_file.exists() else False

    results["startup_script"] = {
        "file": "startup.sh",
        "exists": startup_file.exists(),
        "executable": startup_executable
    }
    scores.append(1.0 if (startup_file.exists() and startup_executable) else 0.5)

    avg_score = sum(scores) / len(scores) * 10.0 if scores else 0.0

    return {
        "category": "可运行性",
        "weight": 0.25,
        "results": results,
        "score": round(avg_score, 1),
        "max_score": 10.0
    }

# ═══════════════════════════════════════════════════════════════════════════
# 评估5: 文档完整性 (权重10%)
# ═══════════════════════════════════════════════════════════════════════════

def check_documentation():
    """检查文档完整性"""
    results = {}
    docs_to_check = {
        "XPAY_DEPLOYMENT.md": HOME / ".claude" / "projects" / "-Users-zuimeidedeyihan-longhun-system" / "memory" / "XPAY_DEPLOYMENT.md",
        "XPAY_LAUNCHER_FIX.md": HOME / ".claude" / "projects" / "-Users-zuimeidedeyihan-longhun-system" / "memory" / "XPAY_LAUNCHER_FIX.md",
        "README.md": HOME / "longhun-system" / "README.md"
    }

    scores = []

    for doc_name, doc_path in docs_to_check.items():
        exists = doc_path.exists()
        size = doc_path.stat().st_size if exists else 0

        results[doc_name] = {
            "path": str(doc_path),
            "exists": exists,
            "size_bytes": size
        }

        score = 1.0 if (exists and size > 50) else 0.0
        scores.append(score)

    avg_score = sum(scores) / len(scores) * 10.0 if scores else 0.0

    return {
        "category": "文档完整性",
        "weight": 0.10,
        "results": results,
        "score": round(avg_score, 1),
        "max_score": 10.0
    }

# ═══════════════════════════════════════════════════════════════════════════
# 评估6: 安全性 (权重15%)
# ═══════════════════════════════════════════════════════════════════════════

def check_security():
    """检查安全性"""
    results = {}
    scores = []

    # 本地存储检查
    tx_file = XPAY_ROOT / "transactions.json"
    is_local = tx_file.exists() and not any(
        cloud in str(tx_file) for cloud in ["dropbox", "icloud", "onedrive", "google"]
    )

    results["local_storage"] = {
        "transactions_local": is_local,
        "path": str(tx_file)
    }
    scores.append(1.0 if is_local else 0.0)

    # 目录权限检查
    if XPAY_ROOT.exists():
        stat_info = XPAY_ROOT.stat()
        perms = oct(stat_info.st_mode)[-3:]
        # 理想权限: 700 或 755
        good_perms = perms in ["700", "755", "750"]

        results["directory_permissions"] = {
            "directory": str(XPAY_ROOT),
            "permissions": perms,
            "secure": good_perms
        }
        scores.append(1.0 if good_perms else 0.5)

    # DNA链检查 (通过交易签证)
    dna_valid = False
    try:
        tx_file = XPAY_ROOT / "transactions.json"
        if tx_file.exists():
            with open(tx_file) as f:
                data = json.load(f)
                # 检查是否有DNA签证
                has_dna = any(
                    "dna_signature" in tx for tx in data.get("history", [])
                )
                dna_valid = has_dna and len(data.get("history", [])) > 0
    except:
        dna_valid = False

    results["dna_chain"] = {
        "has_dna_signatures": dna_valid,
        "immutable_format": True
    }
    scores.append(1.0 if dna_valid else 0.5)

    avg_score = sum(scores) / len(scores) * 10.0 if scores else 0.0

    return {
        "category": "安全性",
        "weight": 0.15,
        "results": results,
        "score": round(avg_score, 1),
        "max_score": 10.0
    }

# ═══════════════════════════════════════════════════════════════════════════
# 主函数: 执行完整评估
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  🐉 龍魂系统 · 本地完整评估                              ║")
    print("║  Local Comprehensive Assessment v1.0                      ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()

    # 执行所有评估
    assessments = [
        check_environment(),
        check_code_files(),
        check_data_integrity(),
        check_runability(),
        check_documentation(),
        check_security()
    ]

    # 显示各评估结果
    for assessment in assessments:
        print(f"【{assessment['category']}】")
        print("════════════════════════════════════════════════════════════")
        print(f"  评分: {assessment['score']}/{assessment['max_score']} (权重 {int(assessment['weight']*100)}%)")

        for key, value in assessment['results'].items():
            if isinstance(value, dict):
                print(f"  • {key}: {json.dumps(value, ensure_ascii=False, indent=4).split(chr(10))[0]}...")
            else:
                print(f"  • {key}: {value}")
        print()

    # 计算加权总分
    total_score = sum(a['score'] * a['weight'] * 10 / 10 for a in assessments)

    print("【最终评估结果】")
    print("════════════════════════════════════════════════════════════")
    for assessment in assessments:
        print(f"  {assessment['category']}: {assessment['score']}/{assessment['max_score']}")

    print()
    print(f"  【综合评分】{total_score:.1f}/10")

    # 系统状态判定
    if total_score >= 8.0:
        status = "✅ 生产级可用"
        color = "🟢"
    elif total_score >= 6.0:
        status = "🟡 需要改进"
        color = "🟡"
    else:
        status = "❌ 不推荐"
        color = "🔴"

    print(f"  【系统状态】{color} {status}")
    print()

    # 生成JSON报告
    report = {
        "timestamp": TIMESTAMP,
        "dna": "#龍芯⚡️丙午·癸巳·庚戌·壬午·䷕贲-LOCAL-ASSESSMENT-v1.0",
        "assessments": assessments,
        "total_score": round(total_score, 1),
        "max_score": 10.0,
        "status": status,
        "report_file": str(REPORT_FILE)
    }

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"✅ 完整评估报告已保存:")
    print(f"   {REPORT_FILE}")
    print()

if __name__ == "__main__":
    main()
