#!/usr/bin/env python3
# 龍魂系统 · 工程实现层
# License: MulanPSL v2
# 文化归属: 思想框架归龍魂核心思想层 (CC BY-NC-SA 4.0)
# DNA: #龍芯⚡️丙午·丙申·庚戌·PATH-NORMALIZE-v1.0-UID9622
"""批量替换代码/文档中的旧路径引用为编号化新路径。

替换规则：
  02_SKILLS/  → 02_SKILLS/
  06_HOUTU_OS/  → 06_HOUTU_OS/
  03_KNOWLEDGE_GRAPH/ → 03_KNOWLEDGE_GRAPH/

排除：
  - .git, dist, archive, _work, .venv, __pycache__, node_modules
  - .asc GPG 签名文件
  - 二进制文件
"""

from __future__ import annotations

import argparse
import mimetypes
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REPLACEMENTS: dict[str, str] = {
    "02_SKILLS/": "02_SKILLS/",
    "06_HOUTU_OS/": "06_HOUTU_OS/",
    "03_KNOWLEDGE_GRAPH/": "03_KNOWLEDGE_GRAPH/",
}

EXCLUDED_DIRS: set[str] = {
    ".git",
    "dist",
    "archive",
    "_work",
    ".venv",
    ".venv_tts",
    "__pycache__",
    "node_modules",
    ".pytest_cache",
    ".chromium-browser-snapshots",
}

EXCLUDED_EXTENSIONS: set[str] = {".asc", ".pyc", ".pyo", ".so", ".dylib", ".bin"}

# 额外允许处理的扩展名（即使 mimetypes 判断为二进制也可能实际是文本）
ALLOWED_EXTENSIONS: set[str] = {
    ".md", ".py", ".sh", ".json", ".yaml", ".yml", ".toml",
    ".txt", ".html", ".htm", ".js", ".css", ".ts", ".vue",
    ".xml", ".sql", ".ini", ".cfg", ".conf", ".plist",
    ".skill", ".cnsh",
}


def is_text_file(path: Path) -> bool:
    ext = path.suffix.lower()
    if ext in EXCLUDED_EXTENSIONS:
        return False
    if ext in ALLOWED_EXTENSIONS:
        return True

    # 无扩展名或未知扩展名：尝试读取前 4KB 判断是否含非法字节
    try:
        with path.open("rb") as f:
            chunk = f.read(4096)
            if b"\x00" in chunk:
                return False
            # 简单判断：如果是 UTF-8 可读
            chunk.decode("utf-8")
            return True
    except Exception:
        return False


def normalize_file(path: Path, dry_run: bool = True) -> tuple[int, list[str]]:
    """返回 (替换次数, [应用规则, ...])。"""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return 0, []

    new_text = text
    applied: list[str] = []
    total = 0
    for old, new in REPLACEMENTS.items():
        count = new_text.count(old)
        if count:
            new_text = new_text.replace(old, new)
            total += count
            applied.append(f"{old} → {new} ({count})")

    if total == 0:
        return 0, []

    if not dry_run:
        path.write_text(new_text, encoding="utf-8")

    return total, applied


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Normalize path references")
    parser.add_argument("--dry-run", action="store_true", help="preview changes")
    args = parser.parse_args(argv)

    modified = 0
    total_replacements = 0
    for root, dirs, files in os.walk(REPO_ROOT):
        # 排除目录
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        for filename in files:
            path = Path(root) / filename
            if not is_text_file(path):
                continue

            count, applied = normalize_file(path, dry_run=args.dry_run)
            if count:
                modified += 1
                total_replacements += count
                print(f"{path.relative_to(REPO_ROOT)}: {', '.join(applied)}")

    print(f"\n# files: {modified}, replacements: {total_replacements}")
    if args.dry_run:
        print("# dry-run mode; omit --dry-run to apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
