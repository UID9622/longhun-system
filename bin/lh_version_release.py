#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 版本发布引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-VERSION-RELEASE-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能:
  - 语义化版本管理 (major.minor.patch)
  - 自动生成 CHANGELOG
  - Git Tag 创建
  - 发布前预检（GPG签名/十闸口/引擎数量）

用法:
  lh 版本发布 --bump patch|minor|major
  lh 版本发布 --tag v2.0.0
  lh 版本发布 --status
  lh 版本发布 --check             # 发布前预检
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

PROJECT_ROOT = Path.home() / "longhun-system"
VERSION_FILE = PROJECT_ROOT / "VERSION"
CHANGELOG_FILE = PROJECT_ROOT / "CHANGELOG.md"
BIN_DIR = PROJECT_ROOT / "bin"


class VersionRelease:
    def __init__(self):
        self.current_version = self._read_version()

    def _read_version(self) -> str:
        if VERSION_FILE.exists():
            v = VERSION_FILE.read_text().strip()
            if v:
                return v
        return "v2.0.0"

    def _write_version(self, version: str):
        VERSION_FILE.write_text(version + "\n")

    def bump(self, level: str) -> Dict:
        """语义化版本升级"""
        v = self.current_version.lstrip('v')
        try:
            parts = [int(x) for x in v.split('.')]
        except ValueError:
            parts = [2, 0, 0]
        while len(parts) < 3:
            parts.append(0)

        major, minor, patch = parts[0], parts[1], parts[2]

        if level == "major":
            major += 1; minor = 0; patch = 0
        elif level == "minor":
            minor += 1; patch = 0
        elif level == "patch":
            patch += 1
        else:
            return {"status": "error", "message": f"未知升级级别: {level}，可选 major/minor/patch"}

        new_version = f"v{major}.{minor}.{patch}"
        self._write_version(new_version)
        return {
            "status": "success",
            "old_version": self.current_version,
            "new_version": new_version,
            "level": level,
        }

    def pre_check(self) -> Dict:
        """发布前预检"""
        checks = {}

        # 1. GPG签名覆盖
        py_files = list(BIN_DIR.glob("lh_*.py"))
        asc_files = list(BIN_DIR.glob("lh_*.py.asc"))
        gpg_coverage = round(len(asc_files) / max(1, len(py_files)) * 100, 1)
        checks["gpg_coverage"] = f"{gpg_coverage}% ({len(asc_files)}/{len(py_files)})"

        # 2. 引擎总数
        checks["engine_count"] = len(py_files)

        # 3. git状态
        try:
            result = subprocess.run(["git", "status", "--porcelain"], cwd=PROJECT_ROOT, capture_output=True, text=True)
            dirty = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            checks["uncommitted_changes"] = dirty
            checks["git_clean"] = dirty == 0
        except Exception:
            checks["uncommitted_changes"] = "unknown"

        # 4. 当前分支
        try:
            result = subprocess.run(["git", "branch", "--show-current"], cwd=PROJECT_ROOT, capture_output=True, text=True)
            checks["branch"] = result.stdout.strip()
        except Exception:
            checks["branch"] = "unknown"

        # 综合判定
        all_ok = (
            gpg_coverage >= 80
            and checks.get("git_clean", False)
            and len(py_files) >= 10
        )
        checks["ready"] = all_ok
        checks["recommendation"] = "✅ 可以发布" if all_ok else "⚠️ 建议修复后发布"

        return checks

    def generate_changelog(self, version: str) -> str:
        """生成 CHANGELOG"""
        header = f"""# CHANGELOG

## {version} ({datetime.now().strftime('%Y-%m-%d')})

"""
        # 从 git log 获取最近变更
        try:
            result = subprocess.run(
                ["git", "--no-pager", "log", "--oneline", "--since=2.weeks", "--", "."],
                capture_output=True, text=True, cwd=PROJECT_ROOT, timeout=10
            )
            commits = [l.strip() for l in result.stdout.split('\n') if l.strip()][:30]
        except Exception:
            commits = ["（无法获取git日志）"]

        body = "\n".join(f"- {c}" for c in commits)

        # 追加已有内容
        existing = ""
        if CHANGELOG_FILE.exists():
            existing = CHANGELOG_FILE.read_text(encoding="utf-8")
            # 去掉旧的第一个 ## 块
            existing = re.sub(r'^# CHANGELOG\s*\n\s*##.*?\n', '', existing, count=1, flags=re.DOTALL)
            existing = existing.strip()

        import re as _re
        full = header + body + "\n\n" + existing
        CHANGELOG_FILE.write_text(full, encoding="utf-8")
        return full

    def release(self, version: str) -> Dict:
        """执行发布"""
        pre = self.pre_check()
        if not pre.get("ready"):
            return {"status": "blocked", "reason": "预检未通过", "checks": pre}

        changelog = self.generate_changelog(version)

        try:
            # 更新 VERSION 文件
            self._write_version(version)

            # GPG 扫描
            subprocess.run(
                [sys.executable, str(BIN_DIR / "lh_gpg_sign.py"), "scan", "."],
                cwd=PROJECT_ROOT, capture_output=True
            )

            # Git 操作
            subprocess.run(["git", "add", "VERSION", "CHANGELOG.md"], cwd=PROJECT_ROOT, check=True)
            subprocess.run(["git", "commit", "-m", f"🚀 Release {version}"], cwd=PROJECT_ROOT, check=True)
            subprocess.run(["git", "tag", "-a", version, "-m", f"Release {version}"], cwd=PROJECT_ROOT, check=True)

            return {
                "status": "success",
                "version": version,
                "checks": pre,
                "changelog_preview": changelog[:300],
            }
        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": str(e)}


def main():
    import argparse, sys
    parser = argparse.ArgumentParser(description="龍魂·版本发布引擎")
    parser.add_argument("--bump", choices=["major", "minor", "patch"], help="版本升级类型")
    parser.add_argument("--tag", help="指定版本号")
    parser.add_argument("--status", action="store_true", help="查看当前版本")
    parser.add_argument("--check", action="store_true", help="发布前预检")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    args = parser.parse_args()

    release = VersionRelease()

    if args.status:
        checks = release.pre_check()
        print(f"当前版本: {release.current_version}")
        print(f"GPG覆盖: {checks.get('gpg_coverage')}")
        print(f"未提交变更: {checks.get('uncommitted_changes')}")
        print(f"可以发布: {'✅ 是' if checks.get('ready') else '⚠️ 否'}")
        return

    if args.check:
        result = release.pre_check()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("\n🔍 发布前预检")
            print("-" * 40)
            for k, v in result.items():
                print(f"  {k}: {v}")
        return

    if args.bump:
        result = release.bump(args.bump)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"版本升级: {result.get('old_version')} → {result.get('new_version')}")
        return

    if args.tag:
        result = release.release(args.tag)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n🚀 发布: {result.get('status')}")
            if result.get('status') == 'blocked':
                print(f"原因: {result.get('reason')}")
            elif result.get('status') == 'success':
                print(f"版本: {result['version']}")
                print(f"CHANGELOG 已更新")
                print(f"Git Tag 已创建（需手动 git push --tags）")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
