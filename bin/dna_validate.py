#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA 启动校验器 v2.0 — 增强版
DNA: #龍芯⚡️2026-07-31-BIN-DNA-VALIDATE-v2.0-a1b3c5d7
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

DNA 启动校验器，用于确保所有必需的环境变量均已定义且值合法。

使用方式：
  1. 将 .env.example 复制为 .env 并填入真实值（发布侧填写，对外不暴露）
  2. 在应用启动前执行本脚本：
       python dna_validate.py
  3. 如果校验通过则继续启动，否则阻止启动。

也可作为模块导入并调用 validate_dna()，失败时返回 False。

v2.0 增强：
  - 必需键从 40 → 48（新增敏感数据动作/高危强制拒绝/热重载/用户通知/审计字段/主权声明）
  - 禁止键从 2 → 5（医疗处置/财务建议/财务预测 扩展为 false）
  - 新增域值白名单校验（RESTRICTED/STRICT）
  - 设计原则：不给 AI 自由发挥，只给工程确定性。
"""

import os
import sys
from pathlib import Path
from typing import List, Optional, Set, Tuple

# ---------- 必需键列表（从 .env.example 中提取） ----------
REQUIRED_KEYS: List[str] = [
    # META
    "DNA_VERSION",
    "DNA_STATUS",
    "DNA_SCOPE",
    "DNA_MACHINE_READABLE",
    "DNA_LAST_REVIEW",
    # CORE PRINCIPLES
    "DNA_NO_DISCRIMINATION",
    "DNA_NO_FABRICATION",
    "DNA_NO_FLATTERY",
    "DNA_GRACEFUL_REFUSAL",
    # NON-NEGOTIABLE RULES
    "DNA_ALLOW_HUMAN_DECISION_REPLACEMENT",
    "DNA_ALLOW_LEGAL_CONCLUSION",
    "DNA_ALLOW_MEDICAL_DIAGNOSIS",
    "DNA_ALLOW_MEDICAL_TREATMENT",
    "DNA_ALLOW_FINANCIAL_ADVICE",
    "DNA_ALLOW_FINANCIAL_PREDICTION",
    # HIGH RISK DOMAINS
    "DNA_DOMAIN_LEGAL",
    "DNA_DOMAIN_MEDICAL",
    "DNA_DOMAIN_FINANCIAL",
    "DNA_DOMAIN_PRIVACY",
    "DNA_DOMAIN_ETHICS",
    # REFUSAL POLICY
    "DNA_REFUSE_ON_INSUFFICIENT_PERMISSION",
    "DNA_REFUSE_ON_HIGH_RISK",
    "DNA_REFUSE_ON_INCOMPLETE_INFO",
    "DNA_REFUSE_ON_OUT_OF_SCOPE",
    "DNA_REFUSAL_TONE",
    "DNA_REFUSAL_EXPLANATION_REQUIRED",
    "DNA_REFUSAL_ALTERNATIVE_ALLOWED",
    # PRIVACY & DATA
    "DNA_DATA_COLLECTION",
    "DNA_LONG_TERM_STORAGE",
    "DNA_USER_PROFILING",
    "DNA_CROSS_SESSION_TRACKING",
    "DNA_BLOCK_SENSITIVE_DATA",
    "DNA_SENSITIVE_DATA_ACTION",
    # AUTOMATION HOOKS
    "DNA_ON_RULE_VIOLATION",
    "DNA_ON_HIGH_RISK",
    "DNA_ON_UNCERTAINTY",
    "DNA_LOG_MODE",
    "DNA_LOG_CONTENT",
    # UPDATE & SYNC
    "DNA_UPDATE_MODE",
    "DNA_SIGNATURE_REQUIRED",
    "DNA_HOT_RELOAD_ALLOWED",
    # USER VISIBLE NOTICE
    "DNA_USER_NOTICE_ENABLED",
    "DNA_USER_NOTICE_SHORT",
    # AUDIT
    "DNA_AUDIT_ENABLED",
    "DNA_AUDIT_FIELDS",
    "DNA_AUDIT_CONTENT_LOG",
    # SOVEREIGNTY
    "DNA_NATIONAL_POSITION_CN",
    "DNA_TAIWAN_IS_CHINA",
]

# ---------- 强制为 false 的键（不区分大小写） ----------
FORBIDDEN_TRUE_KEYS: List[str] = [
    "DNA_ALLOW_LEGAL_CONCLUSION",
    "DNA_ALLOW_MEDICAL_DIAGNOSIS",
    "DNA_ALLOW_MEDICAL_TREATMENT",
    "DNA_ALLOW_FINANCIAL_ADVICE",
    "DNA_ALLOW_FINANCIAL_PREDICTION",
]

# ---------- 允许的域值（白名单校验） ----------
ALLOWED_DOMAIN_VALUES: Set[str] = {"RESTRICTED", "STRICT"}

DOMAIN_KEYS: List[str] = [
    "DNA_DOMAIN_LEGAL",
    "DNA_DOMAIN_MEDICAL",
    "DNA_DOMAIN_FINANCIAL",
    "DNA_DOMAIN_PRIVACY",
    "DNA_DOMAIN_ETHICS",
]

# ---------- 退出码 ----------
EXIT_OK = 0
EXIT_VALIDATION_FAILED = 1


def load_dotenv_file(env_path: Optional[Path] = None) -> None:
    """
    手动解析 .env 文件并注入 os.environ。
    若未指定路径，则在当前工作目录查找 .env 文件。
    若文件不存在，静默跳过。
    """
    if env_path is None:
        env_path = Path.cwd() / ".env"
    if not env_path.exists():
        return

    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if key:
                    os.environ[key] = val


def validate_dna() -> bool:
    """
    执行 DNA 校验。
    返回 True 表示通过，False 表示失败。
    """
    failed = False
    missing_keys: List[str] = []
    forbidden_keys: List[Tuple[str, str]] = []
    invalid_domain_keys: List[Tuple[str, str]] = []

    # 1. 检查所有必需键
    for key in REQUIRED_KEYS:
        if os.getenv(key) is None:
            missing_keys.append(key)
            failed = True

    # 2. 检查特定键不能为 true（不区分大小写）
    for key in FORBIDDEN_TRUE_KEYS:
        value = os.getenv(key)
        if value is not None and value.lower() == "true":
            forbidden_keys.append((key, value))
            failed = True

    # 3. 检查高风险域值（白名单校验）
    for domain_key in DOMAIN_KEYS:
        value = os.getenv(domain_key)
        if value is not None and value not in ALLOWED_DOMAIN_VALUES:
            invalid_domain_keys.append((domain_key, value))
            failed = True

    # 4. 打印详细报告
    if failed:
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("  🧬 System DNA Validation Report v2.0")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        if missing_keys:
            print(f"\n  🔴 缺失必需键 ({len(missing_keys)}/{len(REQUIRED_KEYS)}):")
            for k in missing_keys:
                print(f"     - {k}")

        if forbidden_keys:
            print(f"\n  🔴 禁止值为 true ({len(forbidden_keys)}):")
            for k, v in forbidden_keys:
                print(f"     - {k} = {v} (必须为 false)")

        if invalid_domain_keys:
            print(f"\n  🔴 域值非法 ({len(invalid_domain_keys)}):")
            for k, v in invalid_domain_keys:
                print(f"     - {k} = '{v}' (允许: {ALLOWED_DOMAIN_VALUES})")

        print(
            f"\n  📊 结论: ❌ 校验失败 — "
            f"缺失 {len(missing_keys)} 键, "
            f"{len(forbidden_keys)} 禁止违规, "
            f"{len(invalid_domain_keys)} 域值非法"
        )
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    else:
        # 统计通过
        filled_keys = sum(1 for k in REQUIRED_KEYS if os.getenv(k) is not None)
        forbidden_ok = sum(
            1 for k in FORBIDDEN_TRUE_KEYS
            if os.getenv(k) is not None and os.getenv(k, "").lower() != "true"
        )
        domain_ok = sum(
            1 for k in DOMAIN_KEYS
            if os.getenv(k) in ALLOWED_DOMAIN_VALUES
        )
        print(
            f"🧬 DNA校验通过 v2.0 — "
            f"{filled_keys}/{len(REQUIRED_KEYS)} 必需键, "
            f"{forbidden_ok}/{len(FORBIDDEN_TRUE_KEYS)} 禁止项已确认, "
            f"{domain_ok}/{len(DOMAIN_KEYS)} 域值合法"
        )

    return not failed


def main() -> None:
    """命令行入口"""
    # 自动加载 .env（如果有）
    load_dotenv_file()

    if validate_dna():
        print("✅ System DNA validation passed.")
        sys.exit(EXIT_OK)
    else:
        print("❌ System DNA validation failed. Abort startup.")
        sys.exit(EXIT_VALIDATION_FAILED)


if __name__ == "__main__":
    main()
