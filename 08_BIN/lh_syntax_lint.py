#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂系统 · 语法规范校验器 v1.0
═══════════════════════════════════════════════════════════════
DNA:        #龍芯⚡️丙午·丙申·辛亥·戊戌·䷔噬嗑-SYNTAX-LINT-V1.0-UID9622
确认码:      #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG:        A2D0092CEE2E5BA87035600924C3704A8CC26D5F
主权锚定:    #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
描述:        依据 LH-SYNTAX-SPEC-v3.0 自动化校验全系统语法合规
依循:        `01_protocols/LH-SYNTAX-SPEC-v3.0.md`（P0·繁体龍永存）
分层许可:     工程层 MulanPSL v2
═══════════════════════════════════════════════════════════════
"""

import re
import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# ── 常量（焊死·不可修改）─────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
SYNTAX_SPEC = ROOT / "01_protocols" / "LH-SYNTAX-SPEC-v3.0.md"

# P0: 品牌标识「龍」永存 — 这些字符串必须用繁体
BRAND_DRAGON_TARGETS = [
    "龍魂", "龍芯", "龍盾", "龍智", "龍字", "龍腾",
    "龍淵", "龍威", "龍翼", "龍鸣", "龍吟", "龍骨",
    "龍脉", "龍鳞", "龍爪", "龍眸", "龍息",
]
# 对应的简体字符串（发现即报错）
BRAND_DRAGON_VIOLATIONS = [
    "龍魂", "龍芯", "龍盾", "龍智", "龍字", "龍腾",
    "龍淵", "龍威", "龍翼", "龍鸣", "龍吟", "龍骨",
    "龍脉", "龍鳞", "龍爪", "龍眸", "龍息",
]

# DNA正则
DNA_PATTERN = re.compile(r'DNA:\s*#(\S+)⚡️')
CONFIRM_PATTERN = re.compile(r'#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z')
SOVEREIGN_PATTERN = re.compile(r'#ZHUGEXIN⚡️2025-[^\s]+-DEVICE-BIND-SOUL')
TRICOLOR_PATTERN = re.compile(r'[🟢🟡🔴]')
LICENSE_PATTERN = re.compile(r'MulanPSL|CC BY-NC-SA')

# Tab检测
TAB_RE = re.compile(r'\t')

# 文件类型分类
PY_FILE = {'.py'}
SH_FILE = {'.sh', '.bash', '.zsh'}
MD_FILE = {'.md'}
HTML_FILE = {'.html', '.htm'}
JSON_FILE = {'.json'}
YAML_FILE = {'.yml', '.yaml'}

ALL_CODE_FILES = PY_FILE | SH_FILE | MD_FILE | HTML_FILE

# 白名单（跳过校验的路径模式）
SKIP_PATTERNS = [
    '.git/', '__pycache__/', 'node_modules/', '.venv/',
    'venv/', '.codebuddy/', '_archive/', '_private/',
    '*.pyc', '*.asc', '*.pyo', '.DS_Store',
    'backups/', 'backup/', '.backup', 'dist/',
    'models/', '*.egg-info/', 'logos/', 'icons/',
    'tombstone_vault/', 'audit_log.jsonl',
    # 以下为自动生成/第三方/大文件不校验
    'fused_model/', 'rag_indexes/', 'test_results/',
    'notion_prompt_library/', '11_DATA/', 'archive/',
]


def should_skip(filepath: Path) -> bool:
    """判断是否跳过该文件"""
    rel = str(filepath.relative_to(ROOT))
    for pattern in SKIP_PATTERNS:
        if '*' in pattern:
            if filepath.match(pattern):
                return True
        elif pattern.endswith('/'):
            if rel.startswith(pattern) or f'/{pattern}' in f'/{rel}':
                return True
        elif pattern == rel or f'/{pattern}' in f'/{rel}':
            return True
    return False


def get_ext(filepath: Path) -> str:
    return filepath.suffix.lower()


class SyntaxIssue:
    """单条语法问题"""
    def __init__(self, filepath: Path, level: str, rule: str, detail: str, line: int = 0):
        self.filepath = filepath
        self.level = level      # 🔴 error / 🟡 warning / 🟢 ok
        self.rule = rule
        self.detail = detail
        self.line = line

    def to_dict(self) -> dict:
        return {
            "file": str(self.filepath.relative_to(ROOT)),
            "level": self.level,
            "rule": self.rule,
            "detail": self.detail,
            "line": self.line,
        }

    def __str__(self):
        loc = f":{self.line}" if self.line else ""
        return f"  {self.level} [{self.rule}] {self.filepath.name}{loc}: {self.detail}"


class SyntaxLinter:
    """龍魂语法规范校验器"""

    def __init__(self, root_path: Path = None):
        self.root = root_path or ROOT
        self.issues: List[SyntaxIssue] = []
        self.stats = {
            "files_scanned": 0,
            "files_skipped": 0,
            "error_files": 0,
            "warning_files": 0,
            "error_issues": 0,
            "warning_issues": 0,
            "passes": 0,
        }

    def scan_all(self, target_dir: Path = None) -> List[SyntaxIssue]:
        """扫描整个项目"""
        target = target_dir or self.root
        files_with_errors: set = set()
        files_with_warnings: set = set()

        for f in target.rglob('*'):
            if not f.is_file():
                continue
            if should_skip(f):
                self.stats["files_skipped"] += 1
                continue

            ext = get_ext(f)
            if ext in ALL_CODE_FILES:
                self.stats["files_scanned"] += 1
                before = len(self.issues)
                self._lint_file(f, ext)
                after = len(self.issues)

                # 按文件统计
                if after > before:
                    for i in self.issues[before:after]:
                        if i.level == "🔴":
                            files_with_errors.add(str(f))
                        elif i.level == "🟡":
                            files_with_warnings.add(str(f))

        # 文件级统计（去重）
        self.stats["error_files"] = len(files_with_errors)
        self.stats["warning_files"] = len(files_with_warnings)
        self.stats["error_issues"] = sum(1 for i in self.issues if i.level == "🔴")
        self.stats["warning_issues"] = sum(1 for i in self.issues if i.level == "🟡")
        self.stats["passes"] = self.stats["files_scanned"] - len(files_with_errors | files_with_warnings)

        return self.issues

    def _lint_file(self, filepath: Path, ext: str):
        """校验单个文件"""
        try:
            content = filepath.read_text(encoding='utf-8')
        except Exception:
            return

        lines = content.split('\n')
        relpath = str(filepath.relative_to(self.root))

        # ── 检查1: DNA追溯码 ──────────────────
        if not DNA_PATTERN.search(content):
            self.issues.append(SyntaxIssue(
                filepath, "🔴", "DNA_MISSING",
                "缺少DNA追溯码（格式: DNA: #龍芯⚡️YYYY-MM-DD-类型-ID-UID9622）"
            ))

        # ── 检查2: 确认码 ──────────────────
        if not CONFIRM_PATTERN.search(content):
            self.issues.append(SyntaxIssue(
                filepath, "🔴", "CONFIRM_MISSING",
                "缺少确认码（格式: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z）"
            ))

        # ── 检查3: 品牌「龍」字对齐 ────────────────
        for i, violation in enumerate(BRAND_DRAGON_VIOLATIONS):
            if violation in content:
                # 查找行号
                line_no = 0
                for idx, line in enumerate(lines, 1):
                    if violation in line:
                        line_no = idx
                        break
                self.issues.append(SyntaxIssue(
                    filepath, "🔴", "DRAGON_CHAR",
                    f"品牌标识必须用繁体：'{violation}' → '{BRAND_DRAGON_TARGETS[i]}'",
                    line=line_no,
                ))

        # ── 检查4: Tab缩进 ──────────────────
        for idx, line in enumerate(lines, 1):
            if '\t' in line:
                self.issues.append(SyntaxIssue(
                    filepath, "🔴", "TAB_INDENT",
                    f"发现Tab缩进，必须使用4空格",
                    line=idx,
                ))
                break  # 只报告一次

        # ── 检查5: 许可声明 ──────────────────
        if not LICENSE_PATTERN.search(content):
            self.issues.append(SyntaxIssue(
                filepath, "🟡", "LICENSE_MISSING",
                "缺少分层许可声明（MulanPSL v2 / CC BY-NC-SA）"
            ))

        # ── 检查6: 三色标记（仅.md必须）──
        if ext == '.md' and not TRICOLOR_PATTERN.search(content):
            self.issues.append(SyntaxIssue(
                filepath, "🟡", "TRICOLOR_MISSING",
                "缺少三色审计标记（🟢/🟡/🔴）"
            ))

        # ── 检查7: Python/Shell shebang ──────
        if ext in PY_FILE and not lines[0].startswith('#!/'):
            self.issues.append(SyntaxIssue(
                filepath, "🟡", "SHEBANG_MISSING",
                "Python文件缺少shebang（#!/usr/bin/env python3）"
            ))
        if ext in SH_FILE and not lines[0].startswith('#!/'):
            self.issues.append(SyntaxIssue(
                filepath, "🟡", "SHEBANG_MISSING",
                "Shell脚本缺少shebang（#!/bin/bash）"
            ))

    def report_text(self, verbose: bool = False) -> str:
        """生成文本报告"""
        lines = []
        lines.append("🐉 龍魂语法规范校验报告")
        lines.append("═" * 60)
        lines.append(f"校验时间: {datetime.now().isoformat()}")
        lines.append(f"语法规范: LH-SYNTAX-SPEC-v3.0（繁体龍永存·P0）")
        lines.append(f"扫描文件: {self.stats['files_scanned']}")
        lines.append(f"跳过文件: {self.stats['files_skipped']}")
        lines.append(f"🔴 错误文件: {self.stats['error_files']} （{self.stats['error_issues']} 处问题）")
        lines.append(f"🟡 警告文件: {self.stats['warning_files']} （{self.stats['warning_issues']} 处问题）")
        lines.append(f"🟢 通过: {self.stats['passes']}")
        lines.append("═" * 60)

        if not self.issues:
            lines.append("✅ 全部通过！零错误零警告")
            return '\n'.join(lines)

        # 按规则分组
        by_rule: Dict[str, List] = {}
        for issue in self.issues:
            by_rule.setdefault(issue.rule, []).append(issue)

        for rule, issues in sorted(by_rule.items()):
            lines.append(f"\n📋 {rule} ({len(issues)}处):")
            for issue in issues:
                lines.append(str(issue))

        lines.append("\n" + "═" * 60)
        if self.stats["error_files"] == 0:
            lines.append("🟢 所有P0铁律检查通过")
        else:
            lines.append(f"🔴 发现 {self.stats['error_files']} 个文件·{self.stats['error_issues']} 处P0铁律违规，必须修复！")
        lines.append(f"📖 语法标准: {SYNTAX_SPEC}")
        lines.append("")
        return '\n'.join(lines)

    def report_json(self) -> str:
        """生成JSON报告"""
        return json.dumps({
            "timestamp": datetime.now().isoformat(),
            "spec": "LH-SYNTAX-SPEC-v3.0",
            "stats": self.stats,
            "issues": [i.to_dict() for i in self.issues],
        }, ensure_ascii=False, indent=2)


def parse_args():
    parser = argparse.ArgumentParser(
        description='🐉 龍魂语法规范校验器 · 依据 LH-SYNTAX-SPEC-v3.0',
    )
    parser.add_argument('target', nargs='?', default='.',
                        help='目标目录或文件（默认: 项目根目录）')
    parser.add_argument('--dir', '-d', default=None,
                        help='指定扫描目录')
    parser.add_argument('--json', action='store_true',
                        help='JSON格式输出')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='详细输出')
    parser.add_argument('--fix-dragon', action='store_true',
                        help='自动修正简体「龍」→繁体「龍」（仅品牌标识）')
    return parser.parse_args()


def auto_fix_dragon(target_dir: Path):
    """自动修正品牌「龍」→「龍」"""
    fixed = 0
    files_touched = 0

    for f in target_dir.rglob('*'):
        if not f.is_file():
            continue
        if should_skip(f):
            continue
        ext = get_ext(f)
        if ext not in ALL_CODE_FILES:
            continue

        try:
            content = f.read_text(encoding='utf-8')
        except Exception:
            continue

        modified = content
        for violation, target in zip(BRAND_DRAGON_VIOLATIONS, BRAND_DRAGON_TARGETS):
            count = modified.count(violation)
            if count > 0:
                modified = modified.replace(violation, target)
                fixed += count

        if modified != content:
            f.write_text(modified, encoding='utf-8')
            files_touched += 1
            print(f"  ✅ 修正: {f.relative_to(target_dir)} ({len(BRAND_DRAGON_TARGETS)}个品牌词→繁体龍)")

    print(f"\n共计修正 {fixed} 处 · {files_touched} 个文件")


def main():
    args = parse_args()

    target = Path(args.dir or args.target)
    if not target.is_absolute():
        target = ROOT / target
    target = target.resolve()

    # 自动修正模式
    if args.fix_dragon:
        print(f"🐉 自动修正「龍」→「龍」（品牌标识）")
        print(f"目标: {target}")
        print("═" * 50)
        auto_fix_dragon(target)
        return 0

    # 校验模式
    linter = SyntaxLinter(ROOT)
    linter.scan_all(target)

    if args.json:
        print(linter.report_json())
    else:
        print(linter.report_text())

    # 返回码: 有🔴错误→1
    return 1 if linter.stats["error_files"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
