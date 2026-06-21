#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍字規範化工具 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UID9622 · 诸葛鑫 · 龍芯北辰
DNA:#龍芯⚡️2026-06-07-DRAGON-CHAR-NORMALIZER-v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

功能: 統一龍字編碼 (簡體龙 U+9F99 → 繁體龍 U+9F8D)

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
# 字符定義
# ═══════════════════════════════════════════════════════════════

# 簡體 "龙" (U+9F99)
SIMPLIFIED = "龙"

# 繁體 "龍" (U+9F8D)
TRADITIONAL = "龍"

# ═══════════════════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════════════════

# 只處理這些副檔名
ALLOWED_EXTENSIONS = {
    '.md', '.txt', '.markdown',
    '.json', '.yaml', '.yml',
    '.html', '.csv'
}

# 排除這些目錄
EXCLUDED_DIRS = {
    '.git', '__pycache__', 'node_modules',
    '.venv', 'venv', '.egg-info',
    '_archive', '.obsidian'
}

# ═══════════════════════════════════════════════════════════════
# 統計類
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
        print("📊 龍字規範化統計報告")
        print("═" * 70)
        print(f"掃描文件數:     {self.files_scanned}")
        print(f"修改文件數:     {self.files_modified}")
        print(f"替換字符數:     {self.chars_replaced}")
        print(f"備份文件數:     {len(self.backup_files)}")
        print(f"錯誤數:         {len(self.errors)}")

        if self.errors:
            print("\n⚠️  錯誤詳情:")
            for error in self.errors:
                print(f"   - {error}")

# ═══════════════════════════════════════════════════════════════
# 核心函數
# ═══════════════════════════════════════════════════════════════

def normalize_file(file_path: Path, traditional: bool = True,
                   dry_run: bool = False, backup: bool = True) -> Tuple[int, bool]:
    """
    規範化單個文件

    Returns:
        (替換次數, 文件是否修改)
    """
    try:
        # 讀取原文件內容
        content = file_path.read_text(encoding='utf-8')

        # 判斷是否需要替換
        if traditional:
            # 簡體 → 繁體
            source_char = SIMPLIFIED
            target_char = TRADITIONAL
            if source_char not in content:
                return 0, False
        else:
            # 繁體 → 簡體 (不建議)
            source_char = TRADITIONAL
            target_char = SIMPLIFIED
            if source_char not in content:
                return 0, False

        # 執行替換
        new_content = content.replace(source_char, target_char)
        replace_count = content.count(source_char)

        if not dry_run and new_content != content:
            # 備份原文件
            if backup:
                backup_path = file_path.with_suffix(file_path.suffix + '.bak')
                shutil.copy2(file_path, backup_path)

            # 寫入新內容
            file_path.write_text(new_content, encoding='utf-8')
            return replace_count, True

        return replace_count, False

    except Exception as e:
        raise Exception(f"處理 {file_path} 失敗: {str(e)}")

def scan_directory(root_path: Path, stats: NormalizationStats,
                   traditional: bool = True, dry_run: bool = False,
                   backup: bool = True, verbose: bool = True):
    """
    遞歸掃描目錄並規範化所有文件
    """
    for item in sorted(root_path.rglob('*')):
        # 跳過目錄
        if item.is_dir():
            # 跳過排除的目錄
            if any(excluded in item.parts for excluded in EXCLUDED_DIRS):
                continue
            continue

        # 檢查副檔名
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
                status = "✅ 已修改" if not dry_run else "🔍 將修改"
                if verbose:
                    print(f"{status}: {item.relative_to(root_path)} (+{replace_count} 字符)")

        except Exception as e:
            stats.errors.append(str(e))
            print(f"❌ 錯誤: {str(e)}")

# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍字規範化工具 v1.0"
    )

    parser.add_argument(
        '--root',
        type=Path,
        required=True,
        help='掃描根目錄 (必須)'
    )

    parser.add_argument(
        '--normalize-to-traditional',
        action='store_true',
        help='簡體 → 繁體 (默認) · 龙 → 龍'
    )

    parser.add_argument(
        '--normalize-to-simplified',
        action='store_true',
        help='繁體 → 簡體 (不建議) · 龍 → 龙'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='預演模式 (不實際修改文件)'
    )

    parser.add_argument(
        '--backup',
        action='store_true',
        default=True,
        help='修改前備份原文件 (默認啟用)'
    )

    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='禁用備份'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        default=True,
        help='詳細輸出 (默認啟用)'
    )

    args = parser.parse_args()

    # ═════════════════════════════════════════════
    # 驗證参數
    # ═════════════════════════════════════════════

    if not args.root.exists():
        print(f"❌ 路徑不存在: {args.root}")
        sys.exit(1)

    traditional = args.normalize_to_traditional or not args.normalize_to_simplified
    backup = args.backup and not args.no_backup

    # ═════════════════════════════════════════════
    # 執行規範化
    # ═════════════════════════════════════════════

    print("════════════════════════════════════════════════════════════════")
    print("🐉 龍字規範化工具 v1.0")
    print("════════════════════════════════════════════════════════════════")
    print(f"根目錄:         {args.root}")
    print(f"規範方向:       {'簡體 → 繁體 (龙 → 龍)' if traditional else '繁體 → 簡體 (龍 → 龙)'}")
    print(f"模式:           {'預演 (不修改)' if args.dry_run else '實際執行 (會修改)'}")
    print(f"備份:           {'啟用' if backup else '禁用'}")
    print("════════════════════════════════════════════════════════════════\n")

    if args.dry_run:
        print("⚠️  預演模式啟動 - 不會實際修改任何文件\n")

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
        print("\n⏹️  用戶中斷")
        sys.exit(1)

    # ═════════════════════════════════════════════
    # 輸出統計報告
    # ═════════════════════════════════════════════

    stats.report()

    print("\n" + "═" * 70)
    if args.dry_run:
        print("✅ 預演完成 - 確認無誤後可去掉 --dry-run 標誌重新運行")
    else:
        print("✅ 規範化完成")
    print("═" * 70)
    print(f"\nDNA:#龍芯⚡️2026-06-07-DRAGON-CHAR-NORMALIZER-v1.0")
    print("責任: UID9622 · 不免責\n")

if __name__ == "__main__":
    main()
