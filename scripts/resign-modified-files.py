#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 龍魂系统 · 工程实现层
# License: MulanPSL v2
# 文化归属: 思想框架归龍魂核心思想层 (CC BY-NC-SA 4.0)
# DNA: #龍芯⚡️丙午·丙申·庚戌·RESIGN-MODIFIED-v1.0-UID9622
"""为当前 Git 工作区中已修改且存在 .asc 签名文件的文件重新签名。"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def git_modified_files() -> list[Path]:
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    files: list[Path] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        # git status --short 格式: XY path 或 XY path -> orig_path
        status = line[:2]
        path_part = line[3:].split(" -> ", 1)[-1]
        # 只处理修改(M)、重命名(R)、新增(A)的文件
        if status[1] in "MRA" or status[0] in "MRA":
            p = REPO_ROOT / path_part
            if p.is_file() and not p.name.endswith(".asc"):
                files.append(p)
    return files


def resign_file(path: Path, dry_run: bool = True) -> bool:
    asc_path = Path(str(path) + ".asc")
    if not asc_path.exists():
        return False

    if dry_run:
        print(f"[dry-run] would resign: {path.relative_to(REPO_ROOT)}")
        return True

    try:
        subprocess.run(
            [
                "gpg",
                "--batch",
                "--yes",
                "--armor",
                "--detach-sign",
                "--output",
                str(asc_path),
                str(path),
            ],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
        )
        print(f"resigned: {path.relative_to(REPO_ROOT)}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"failed: {path.relative_to(REPO_ROOT)}: {e.stderr.decode('utf-8', errors='ignore')}", file=sys.stderr)
        return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Resign modified files with existing .asc signatures")
    parser.add_argument("--dry-run", action="store_true", help="preview files to resign")
    args = parser.parse_args(argv)

    files = git_modified_files()
    resigned = 0
    for f in files:
        if resign_file(f, dry_run=args.dry_run):
            resigned += 1

    print(f"\n# files to resign: {resigned}")
    if args.dry_run:
        print("# dry-run mode; omit --dry-run to apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
