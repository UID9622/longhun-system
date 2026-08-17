#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 龍字规范化守护程序 (LongHun Glyph Sovereignty Guard)
DNA: #龍芯⚡️丙午·甲申·丁未·鼎-GLYPH-GUARD-v1.0-UID9622

核心铁律:
  1. 简体 "龙" (U+9F99) → 繁体 "龍" (U+9F8D)（协议强制）
  2. "龍芯⚡️" 是文化主权符号，绝对不可翻译、拆分或改写
  3. 国际开源英文语境品牌名统一为 LongHun
  4. 中国本土内容保留中文，不进行英文化

用法:
  干跑模式（默认）:
    python3 08_BIN/lh_dragon_glyph_guard.py --scan .
  实际写入:
    python3 08_BIN/lh_dragon_glyph_guard.py --scan . --write --backup
  单文件处理:
    python3 08_BIN/lh_dragon_glyph_guard.py --input README.md --output README.md --write
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


# ============================================================
# 常量与铁律配置
# ============================================================

DNA = "#龍芯⚡️丙午·甲申·丁未·鼎-GLYPH-GUARD-v1.0-UID9622"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# 文化主权符号，不可触碰
LONGXIN_GLYPH = "龍芯⚡️"
LONGXIN_PLACEHOLDER = "\x00__LONGXIN_SOVEREIGN_GLYPH__\x00"

# 默认处理的文本文件后缀
DEFAULT_TEXT_EXTENSIONS: frozenset[str] = frozenset({
    ".md", ".txt", ".rst",
    ".py", ".pyi",
    ".sh", ".bash", ".zsh",
    ".yaml", ".yml", ".json", ".toml",
    ".html", ".htm", ".css", ".js", ".ts",
    ".cnsh",
})

# 二进制与只读排除
DEFAULT_EXCLUDE_DIRS: frozenset[str] = frozenset({
    ".git", ".venv", ".venv_tts", "venv", "__pycache__",
    "node_modules", ".pytest_cache", ".mypy_cache",
    "site-packages", "dist-packages",
    "_archive", "_private", "_work",
})


# ============================================================
# 转换引擎
# ============================================================

class GlyphTransformer:
    """龍字规范化转换引擎。"""

    def __init__(
        self,
        fix_chinese: bool = True,
        fix_en_brand: bool = True,
        aggressive_en_brand: bool = False,
    ) -> None:
        self.fix_chinese = fix_chinese
        self.fix_en_brand = fix_en_brand
        self.aggressive_en_brand = aggressive_en_brand
        self.stats = {
            "chinese_replacements": 0,
            "en_brand_replacements": 0,
            "longxin_protected_hits": 0,
        }

    def transform(self, text: str) -> str:
        """对文本执行完整规范化。"""
        result = text

        # 第一步：保护文化主权符号
        result, protected_count = self._protect_longxin(result)
        self.stats["longxin_protected_hits"] += protected_count

        # 第二步：中文简体 → 繁体
        if self.fix_chinese:
            result, count = self._normalize_chinese_long(result)
            self.stats["chinese_replacements"] += count

        # 第三步：英文品牌规范化
        if self.fix_en_brand:
            result, count = self._normalize_english_brand(result)
            self.stats["en_brand_replacements"] += count

        # 第四步：恢复文化主权符号
        result = self._restore_longxin(result)

        return result

    def _protect_longxin(self, text: str) -> tuple[str, int]:
        """将龍芯⚡️替换为占位符，防止被后续规则误改。"""
        count = text.count(LONGXIN_GLYPH)
        return text.replace(LONGXIN_GLYPH, LONGXIN_PLACEHOLDER), count

    def _restore_longxin(self, text: str) -> str:
        """恢复龍芯⚡️。"""
        return text.replace(LONGXIN_PLACEHOLDER, LONGXIN_GLYPH)

    @staticmethod
    def _normalize_chinese_long(text: str) -> tuple[str, int]:
        """简体 '龙' (U+9F99) 全部转为繁体 '龍' (U+9F8D)。"""
        count = text.count("龙")
        return text.replace("龙", "龍"), count

    def _normalize_english_brand(self, text: str) -> tuple[str, int]:
        """
        国际开源英文品牌名规范化。
        保守策略：只改明显作为品牌名的组合。
        激进策略：额外改独立出现的 Dragon。

        注意:
          - 仓库名/包名中的全小写 longhun、longhun-system 保持原样
          - URL、命令行、文件路径中出现的小写 longhun 不动
        """
        count = 0
        result = text

        # 必须优先处理 LongHun（多词品牌）
        result, n = re.subn(r"\bDragon Soul\b", "LongHun", result, flags=re.IGNORECASE)
        count += n

        # 大写 LongHun（旧写法）→ LongHun；全小写 longhun 通常是路径/仓库名，保持不动
        result, n = re.subn(r"\bLonghun\b", "LongHun", result)
        count += n

        # 激进模式：独立大写 Dragon 也视为品牌
        if self.aggressive_en_brand:
            result, n = re.subn(r"\bDragon\b", "LongHun", result)
            count += n

        return result, count


# ============================================================
# 文件扫描与写入
# ============================================================

def is_text_file(path: Path) -> bool:
    """简单判断是否为文本文件。"""
    if path.suffix.lower() in DEFAULT_TEXT_EXTENSIONS:
        return True
    return False


def iter_target_files(
    root: Path,
    extensions: Iterable[str] | None = None,
    exclude_dirs: Iterable[str] | None = None,
) -> Iterable[Path]:
    """递归遍历目标文本文件。"""
    exts = frozenset(extensions) if extensions else DEFAULT_TEXT_EXTENSIONS
    excludes = DEFAULT_EXCLUDE_DIRS | frozenset(exclude_dirs or ())

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in excludes for part in path.parts):
            continue
        if path.suffix.lower() in exts:
            yield path


def process_file(
    path: Path,
    transformer: GlyphTransformer,
    write: bool = False,
    backup: bool = False,
) -> dict | None:
    """处理单个文件，返回变更摘要。"""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None
    except Exception as exc:
        return {"path": str(path), "error": str(exc)}

    # 仅对实际发生变更的文件累计统计，避免干跑数字失真
    stats_before = transformer.stats.copy()
    transformed = transformer.transform(text)
    if transformed == text:
        transformer.stats = stats_before
        return None

    changed_lines = sum(
        1 for a, b in zip(text.splitlines(), transformed.splitlines()) if a != b
    ) + abs(len(transformed.splitlines()) - len(text.splitlines()))

    digest_before = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    digest_after = hashlib.sha256(transformed.encode("utf-8")).hexdigest()[:16]

    if write:
        if backup:
            backup_path = path.with_suffix(path.suffix + ".glyph-backup")
            shutil.copy2(path, backup_path)
        path.write_text(transformed, encoding="utf-8")

    return {
        "path": str(path),
        "changed_lines": changed_lines,
        "digest_before": digest_before,
        "digest_after": digest_after,
    }


# ============================================================
# 报告生成
# ============================================================

def generate_report(
    changed_files: list[dict],
    transformer: GlyphTransformer,
    root: Path,
    write_mode: bool,
) -> str:
    """生成 Markdown / JSON 审计报告。"""
    now = datetime.now(timezone.utc).isoformat()
    report = {
        "dna": DNA,
        "confirm_code": CONFIRM_CODE,
        "timestamp": now,
        "root": str(root),
        "write_mode": write_mode,
        "summary": {
            "files_changed": len(changed_files),
            "chinese_replacements": transformer.stats["chinese_replacements"],
            "en_brand_replacements": transformer.stats["en_brand_replacements"],
            "longxin_protected_hits": transformer.stats["longxin_protected_hits"],
        },
        "changed_files": changed_files,
    }
    return json.dumps(report, ensure_ascii=False, indent=2)


def print_human_summary(
    changed_files: list[dict],
    transformer: GlyphTransformer,
    write_mode: bool,
) -> None:
    """打印人类可读的执行摘要。"""
    mode = "✍️ 已写入" if write_mode else "🔍 干跑模式（未写入）"
    print(f"\n{mode}")
    print(f"DNA: {DNA}")
    print(f"确认码: {CONFIRM_CODE}")
    print("-" * 60)
    print(f"📁 处理文件数: {len(changed_files)}")
    print(f"🇨🇳 简体龙 → 繁体龍: {transformer.stats['chinese_replacements']} 处")
    print(f"🌐 英文品牌规范化: {transformer.stats['en_brand_replacements']} 处")
    print(f"🛡️ 龍芯⚡️ 主权保护: {transformer.stats['longxin_protected_hits']} 处")
    print("-" * 60)
    if changed_files:
        print("📝 变更文件列表:")
        for item in changed_files[:20]:
            print(f"  · {item['path']} ({item['changed_lines']} 行)")
        if len(changed_files) > 20:
            print(f"  ... 等共 {len(changed_files)} 个文件")
    print("-" * 60)


# ============================================================
# CLI
# ============================================================

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="龍魂 · 龍字规范化守护程序",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--scan",
        type=Path,
        help="扫描目录并规范化文本文件（默认干跑）",
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="输入单个文件",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="输出单个文件（与 --input 同时使用）",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="实际写入文件（否则为干跑）",
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="写入前创建 .glyph-backup 备份",
    )
    parser.add_argument(
        "--extensions",
        nargs="+",
        help=f"自定义文本后缀（默认 {sorted(DEFAULT_TEXT_EXTENSIONS)[:5]}... 等）",
    )
    parser.add_argument(
        "--exclude-dirs",
        nargs="+",
        help=f"自定义排除目录",
    )
    parser.add_argument(
        "--aggressive-en-brand",
        action="store_true",
        help="激进英文品牌规范化（独立 Dragon 也替换为 LongHun）",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="将 JSON 审计报告写入指定路径",
    )
    parser.add_argument(
        "--no-fix-chinese",
        action="store_true",
        help="跳过中文龍字规范化",
    )
    parser.add_argument(
        "--no-fix-en-brand",
        action="store_true",
        help="跳过英文品牌规范化",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    transformer = GlyphTransformer(
        fix_chinese=not args.no_fix_chinese,
        fix_en_brand=not args.no_fix_en_brand,
        aggressive_en_brand=args.aggressive_en_brand,
    )

    # 单文件模式
    if args.input:
        if not args.output:
            parser.error("--input 必须与 --output 同时使用")
        text = args.input.read_text(encoding="utf-8")
        transformed = transformer.transform(text)
        if args.write:
            if args.backup:
                shutil.copy2(args.input, args.input.with_suffix(args.input.suffix + ".glyph-backup"))
            args.output.write_text(transformed, encoding="utf-8")
        else:
            sys.stdout.write(transformed)
        print_human_summary([], transformer, args.write)
        return 0

    # 目录扫描模式
    if not args.scan:
        parser.error("请提供 --scan 目录或 --input/--output 文件")

    root = args.scan.resolve()
    changed_files: list[dict] = []
    self_path = Path(__file__).resolve()

    for path in iter_target_files(
        root,
        extensions=args.extensions,
        exclude_dirs=args.exclude_dirs,
    ):
        # 规则引擎自身不可被自身规则改写（防自噬：转换会破坏简体→繁体规则参数）
        if path.resolve() == self_path:
            continue
        # 历史审计报告是证据快照，保持原样（其中的路径与磁盘简体目录名一致）
        if "GLYPH-AUDIT" in path.name:
            continue
        result = process_file(path, transformer, write=args.write, backup=args.backup)
        if result:
            changed_files.append(result)

    print_human_summary(changed_files, transformer, args.write)

    if args.report:
        report_json = generate_report(changed_files, transformer, root, args.write)
        args.report.write_text(report_json, encoding="utf-8")
        print(f"\n📊 审计报告已保存: {args.report}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
