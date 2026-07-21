#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂/CNSH 主权变量审计脚本
DNA:#龍芯⚡️2026-06-15-LONGHUN-SOVEREIGN-ENV-AUDIT-v1.0

用途：扫描项目文件，检查是否还有硬编码密钥或非标准变量名残留。
不修改文件，只输出报告。
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# 需要警惕的硬编码模式
SECRET_PATTERNS = [
    (r'(?<![A-Z_])KIMI_API_KEY\s*=\s*["\']sk-[a-zA-Z0-9]{20,}["\']', "硬编码 Kimi API Key"),
    (r'(?<![A-Z_])TELEGRAM_BOT_TOKEN\s*=\s*["\'][0-9]{9,}:[a-zA-Z0-9_-]{30,}["\']', "硬编码 Telegram Bot Token"),
    (r'(?<![A-Z_])NOTION_TOKEN\s*=\s*["\']secret_[a-zA-Z0-9]{20,}["\']', "硬编码 Notion Token"),
    (r'Bearer\s+[a-zA-Z0-9_-]{30,}', "硬编码 Bearer Token"),
    (r'api_key\s*=\s*["\'][a-zA-Z0-9_-]{32,}["\']', "硬编码 API Key"),
]

# 旧变量名（应在代码中逐渐消失）
LEGACY_ENV_PATTERNS = [
    r'os\.(?:environ\.get|getenv)\(["\']NOTION_BRAIN_DB["\']',
    r'os\.(?:environ\.get|getenv)\(["\']NOTION_MULTICURRENCY_DB["\']',
    r'os\.(?:environ\.get|getenv)\(["\']NOTION_MULTICURRENCY_PAGE["\']',
    r'os\.(?:environ\.get|getenv)\(["\']NOTION_AUDIT_DB_ID["\']',
    r'os\.(?:environ\.get|getenv)\(["\']NOTION_LOG_DB["\']',
    r'os\.(?:environ\.get|getenv)\(["\']NOTION_TEAM_PARENT_ID["\']',
]

# 扫描路径
EXCLUDE_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", "_archive"}


def should_scan(path: Path) -> bool:
    if any(part in EXCLUDE_DIRS for part in path.parts):
        return False
    return path.suffix in {".py", ".sh", ".md", ".json"}


def scan_file(path: Path) -> Tuple[List[Tuple[int, str, str]], List[Tuple[int, str]]]:
    secrets: List[Tuple[int, str, str]] = []
    legacy: List[Tuple[int, str]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return secrets, legacy

    for lineno, line in enumerate(text.splitlines(), 1):
        for pattern, desc in SECRET_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                secrets.append((lineno, desc, line.strip()))
        for pattern in LEGACY_ENV_PATTERNS:
            if re.search(pattern, line):
                legacy.append((lineno, line.strip()))
    return secrets, legacy


def main() -> int:
    all_secrets: List[Tuple[Path, int, str, str]] = []
    all_legacy: List[Tuple[Path, int, str]] = []

    for path in PROJECT_ROOT.rglob("*"):
        if not path.is_file() or not should_scan(path):
            continue
        secrets, legacy = scan_file(path)
        for lineno, desc, line in secrets:
            all_secrets.append((path.relative_to(PROJECT_ROOT), lineno, desc, line))
        for lineno, line in legacy:
            all_legacy.append((path.relative_to(PROJECT_ROOT), lineno, line))

    print("=" * 70)
    print("🐉 龍魂/CNSH 主权变量审计报告")
    print("=" * 70)

    if all_secrets:
        print(f"\n🔴 发现 {len(all_secrets)} 处硬编码密钥/Token：")
        for p, lineno, desc, line in all_secrets:
            print(f"  {p}:{lineno}  {desc}")
            print(f"    {line[:120]}")
    else:
        print("\n🟢 未发现明显硬编码密钥/Token")

    if all_legacy:
        print(f"\n🟡 发现 {len(all_legacy)} 处旧变量名（建议迁移到主权变量）：")
        for p, lineno, line in all_legacy:
            print(f"  {p}:{lineno}")
            print(f"    {line[:120]}")
    else:
        print("\n🟢 未发现旧变量名")

    print("\n" + "=" * 70)
    if all_secrets:
        print("结论：❌ 存在硬编码密钥，请脱敏后再提交")
        return 1
    if all_legacy:
        print("结论：⚠️ 存在旧变量名，建议继续迁移")
        return 0
    print("结论：✅ 通过主权变量审计")
    return 0


if __name__ == "__main__":
    sys.exit(main())
