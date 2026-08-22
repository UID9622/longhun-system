#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
🐉 龍字规范化工具 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UID9622 · 诸葛鑫 · 龍芯北辰
DNA:#龍芯⚡️丙午·甲午·壬子·丙午·䷙大畜-DRAGON-CHAR-NORMALIZER-v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

功能: 统一龍字编码 (简体龍 U+9F99 → 繁体龍 U+9F8D)

用法:
  python3 dragon_char_normalizer.py --root ~/longhun-system --dry-run
  python3 dragon_char_normalizer.py --root ~/longhun-system --normalize-to-traditional --backup
"""

import os
import sys
import re
import argparse
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Tuple

# ═══════════════════════════════════════════════════════════════
# 字符定义
# ═══════════════════════════════════════════════════════════════

# 简体 "龍" (U+9F99)
SIMPLIFIED = "龍"

# 繁体 "龍" (U+9F8D)
TRADITIONAL = "龍"

# ═══════════════════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════════════════

# 只处理这些副档名
ALLOWED_EXTENSIONS = {
    '.md', '.txt', '.markdown',
    '.json', '.yaml', '.yml', '.jsonl',
    '.html', '.csv',
    '.py', '.sh', '.js', '.ts', '.tsx', '.css',
    '.toml', '.cnsh', '.cpp', '.cfg', '.conf',
    '.tex', '.ini'
}

# 排除这些目录
EXCLUDED_DIRS = {
    '.git', '__pycache__', 'node_modules',
    '.venv', 'venv', '.egg-info',
    '_archive', '.obsidian',
    '.venv_longhun_math', 'voice-twin'
}

# ═══════════════════════════════════════════════════════════════
# 统计类
# ═══════════════════════════════════════════════════════════════

class NormalizationStats:
    def __init__(self):
        self.files_scanned = 0
        self.files_modified = 0
        self.chars_replaced = 0
        self.backup_files = []
        self.errors = []

    def report(self):
        print("\n" + "═" * 70)
        print("📊 龍字规范化统计报告")
        print("═" * 70)
        print(f"扫描文件数:     {self.files_scanned}")
        print(f"修改文件数:     {self.files_modified}")
        print(f"替换字符数:     {self.chars_replaced}")
        print(f"备份文件数:     {len(self.backup_files)}")
        print(f"错误数:         {len(self.errors)}")

        if self.errors:
            print("\n⚠️  错误详情:")
            for error in self.errors:
                print(f"   - {error}")

# ═══════════════════════════════════════════════════════════════
# 核心函数
# ═══════════════════════════════════════════════════════════════

def normalize_file(file_path: Path, traditional: bool = True,
                   dry_run: bool = False, backup: bool = True) -> Tuple[int, bool]:
    """
    规范化单个文件

    Returns:
        (替换次数, 文件是否修改)
    """
    try:
        # 读取原文件内容
        content = file_path.read_text(encoding='utf-8')

        # 判断是否需要替换
        if traditional:
            # 简体 → 繁体
            source_char = SIMPLIFIED
            target_char = TRADITIONAL
            if source_char not in content:
                return 0, False
        else:
            # 繁体 → 简体 (不建议)
            source_char = TRADITIONAL
            target_char = SIMPLIFIED
            if source_char not in content:
                return 0, False

        # 执行替换
        new_content = content.replace(source_char, target_char)
        replace_count = content.count(source_char)

        if not dry_run and new_content != content:
            # 备份原文件
            if backup:
                backup_path = file_path.with_suffix(file_path.suffix + '.bak')
                shutil.copy2(file_path, backup_path)

            # 写入新内容
            file_path.write_text(new_content, encoding='utf-8')
            return replace_count, True

        return replace_count, False

    except Exception as e:
        raise Exception(f"处理 {file_path} 失败: {str(e)}")

def scan_directory(root_path: Path, stats: NormalizationStats,
                   traditional: bool = True, dry_run: bool = False,
                   backup: bool = True, verbose: bool = True):
    """
    递归扫描目录并规范化所有文件
    """
    for item in sorted(root_path.rglob('*')):
        # 排除的目录/文件统一跳过（无论是目录还是文件都检查）
        if any(excluded in item.parts for excluded in EXCLUDED_DIRS):
            continue
        # 跳过目录本身
        if item.is_dir():
            continue

        # 检查副档名
        if item.suffix not in ALLOWED_EXTENSIONS:
            continue

        stats.files_scanned += 1

        try:
            replace_count, modified = normalize_file(
                item, traditional=traditional,
                dry_run=dry_run, backup=backup
            )

            if modified:
                stats.files_modified += 1
                stats.chars_replaced += replace_count
                status = "✅ 已修改" if not dry_run else "🔍 将修改"
                if verbose:
                    print(f"{status}: {item.relative_to(root_path)} (+{replace_count} 字符)")

        except Exception as e:
            stats.errors.append(str(e))
            print(f"❌ 错误: {str(e)}")

# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍字规范化工具 v1.0"
    )

    parser.add_argument(
        '--root',
        type=Path,
        required=True,
        help='扫描根目录 (必须)'
    )

    parser.add_argument(
        '--normalize-to-traditional',
        action='store_true',
        help='简体 → 繁体 (默认) · 龍 → 龍'
    )

    parser.add_argument(
        '--normalize-to-simplified',
        action='store_true',
        help='繁体 → 简体 (不建议) · 龍 → 龍'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='预演模式 (不实际修改文件)'
    )

    parser.add_argument(
        '--backup',
        action='store_true',
        default=True,
        help='修改前备份原文件 (默认启用)'
    )

    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='禁用备份'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        default=True,
        help='详细输出 (默认启用)'
    )

    args = parser.parse_args()

    # ═════════════════════════════════════════════
    # 验证参数
    # ═════════════════════════════════════════════

    if not args.root.exists():
        print(f"❌ 路径不存在: {args.root}")
        sys.exit(1)

    traditional = args.normalize_to_traditional or not args.normalize_to_simplified
    backup = args.backup and not args.no_backup

    # ═════════════════════════════════════════════
    # 执行规范化
    # ═════════════════════════════════════════════

    print("════════════════════════════════════════════════════════════════")
    print("🐉 龍字规范化工具 v1.0")
    print("════════════════════════════════════════════════════════════════")
    print(f"根目录:         {args.root}")
    print(f"规范方向:       {'简体 → 繁体 (龍 → 龍)' if traditional else '繁体 → 简体 (龍 → 龍)'}")
    print(f"模式:           {'预演 (不修改)' if args.dry_run else '实际执行 (会修改)'}")
    print(f"备份:           {'启用' if backup else '禁用'}")
    print("════════════════════════════════════════════════════════════════\n")

    if args.dry_run:
        print("⚠️  预演模式启动 - 不会实际修改任何文件\n")

    stats = NormalizationStats()

    try:
        scan_directory(
            args.root, stats,
            traditional=traditional,
            dry_run=args.dry_run,
            backup=backup,
            verbose=args.verbose
        )
    except KeyboardInterrupt:
        print("\n⏹️  用户中断")
        sys.exit(1)

    # ═════════════════════════════════════════════
    # 输出统计报告
    # ═════════════════════════════════════════════

    stats.report()

    print("\n" + "═" * 70)
    if args.dry_run:
        print("✅ 预演完成 - 确认无误后可去掉 --dry-run 标志重新运行")
    else:
        print("✅ 规范化完成")
    print("═" * 70)
    print(f"\nDNA:#龍芯⚡️丙午·甲午·壬子·丙午·䷙大畜-DRAGON-CHAR-NORMALIZER-v1.0")
    print("责任: UID9622 · 不免责\n")

if __name__ == "__main__":
    main()
