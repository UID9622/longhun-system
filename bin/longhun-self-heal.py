#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂左右互搏 · 自愈審計引擎 v1.0

自己尋找漏洞，自己修復，自己疊送。
複雜留給 AI，簡單留給人。

DNA: #龍芯⚡️2026-06-18-LONGHUN-SELF-HEAL-v1.0
"""

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


ROOT = Path(__file__).resolve().parent.parent


@dataclass
class Issue:
    category: str
    severity: str      # info / warning / error
    message: str
    path: Optional[Path] = None
    fix: Optional[callable] = field(default=None, compare=False)


class SelfHealEngine:
    """龍魂系統自愈引擎"""

    DNA = "#龍芯⚡️2026-06-18-LONGHUN-SELF-HEAL-v1.0"

    def __init__(self, root: Path):
        self.root = root
        self.issues: List[Issue] = []
        self.fixed = 0
        self.failed = 0

    def run_all_checks(self):
        self.issues = []
        self.check_required_directories()
        self.check_script_executability()
        self.check_pycache_pollution()
        self.check_desktop_menu_sync()
        self.check_git_status()
        self.check_duplicate_skills()
        self.check_service_health()
        self.check_file_permissions()
        return self.issues

    # ─────────────────────────────── 檢查項 ───────────────────────────────

    def check_required_directories(self):
        required = ["logs", "var", "var/kimi-agent-v2", "var/xpay"]
        for name in required:
            path = self.root / name
            if not path.exists():
                self.issues.append(Issue(
                    category="目錄結構",
                    severity="warning",
                    message=f"缺少必要目錄: {name}",
                    path=path,
                    fix=lambda p=path: p.mkdir(parents=True, exist_ok=True) or True
                ))

    def check_script_executability(self):
        scripts = [
            "bin/longhun-autostart.sh",
            "bin/install-autostart.sh",
            "bin/build-desktop-switch.sh",
            "bin/build-chinese-editor.sh",
            "bin/build-control-center.sh",
            "bin/longhun-status.sh",
            "bin/longhun-daily-audit.sh",
            "bin/refresh-longhun.sh",
        ]
        for rel in scripts:
            path = self.root / rel
            if not path.exists():
                continue
            if not os.access(path, os.X_OK):
                self.issues.append(Issue(
                    category="腳本權限",
                    severity="warning",
                    message=f"腳本未設置可執行: {rel}",
                    path=path,
                    fix=lambda p=path: (p.chmod(p.stat().st_mode | 0o111), True)[1]
                ))

    def check_pycache_pollution(self):
        pycaches = list(self.root.rglob("__pycache__"))
        # 只處理 .git 未忽略的（簡單判斷：不在 _archive 或 .venv 下）
        dirty = [p for p in pycaches if not any(x in p.parts for x in [".venv", "venv", "_archive"])]
        if dirty:
            self.issues.append(Issue(
                category="環境清潔",
                severity="info",
                message=f"發現 {len(dirty)} 個 __pycache__ 目錄",
                fix=lambda dirs=dirty: all(self._rm_tree(d) for d in dirs)
            ))

    def check_desktop_menu_sync(self):
        source = self.root / "desktop" / "龍魂主开关.applescript"
        registry = self.root / "desktop" / "menu-registry.json"
        if source.exists() and registry.exists():
            src_mtime = source.stat().st_mtime
            reg_mtime = registry.stat().st_mtime
            if reg_mtime > src_mtime:
                self.issues.append(Issue(
                    category="桌面菜單",
                    severity="warning",
                    message="菜單註冊表比桌面 App 新，需要重新生成",
                    fix=lambda: self._run(["bash", str(self.root / "bin" / "build-desktop-switch.sh")])
                ))

    def check_git_status(self):
        try:
            result = subprocess.run(
                ["git", "status", "--short"],
                cwd=self.root,
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.stdout.strip():
                lines = result.stdout.strip().splitlines()
                self.issues.append(Issue(
                    category="Git 狀態",
                    severity="info",
                    message=f"工作區有 {len(lines)} 處未提交變更",
                    fix=None  # 不自動提交，只報告
                ))
        except Exception as e:
            self.issues.append(Issue("Git 狀態", "error", f"無法檢查 Git: {e}"))

    def check_duplicate_skills(self):
        """掃描重複的技能文件名"""
        names = {}
        for path in self.root.rglob("longhun_*_engine.py"):
            if any(x in path.parts for x in [".git", "__pycache__"]):
                continue
            names.setdefault(path.name, []).append(path)
        for name, paths in names.items():
            if len(paths) > 1:
                self.issues.append(Issue(
                    category="重複模塊",
                    severity="warning",
                    message=f"技能文件重複: {name} 出現在 {len(paths)} 處",
                    fix=None
                ))

    def check_service_health(self):
        try:
            result = subprocess.run(
                ["lsof", "-ti:9622"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if not result.stdout.strip():
                self.issues.append(Issue(
                    category="服務健康",
                    severity="warning",
                    message="龍魂操作台 (:9622) 未運行",
                    fix=lambda: self._run([
                        "bash", "-c",
                        f"cd {self.root} && export PYTHONPATH={self.root} && mkdir -p logs && "
                        f"cd control-panel && nohup python3 main.py >> ../logs/control-panel.log 2>&1 &"
                    ])
                ))
        except Exception as e:
            self.issues.append(Issue("服務健康", "error", f"無法檢查端口: {e}"))

    def check_file_permissions(self):
        """檢查關鍵數據文件權限是否過寬"""
        sensitive = [
            self.root / "xpay" / "var" / "xpay.db",
        ]
        for path in sensitive:
            if path.exists():
                mode = path.stat().st_mode & 0o777
                if mode & 0o077:
                    self.issues.append(Issue(
                        category="文件權限",
                        severity="warning",
                        message=f"敏感文件權限過寬: {path} ({oct(mode)})",
                        path=path,
                        fix=lambda p=path: (p.chmod(0o600), True)[1]
                    ))

    # ─────────────────────────────── 修復工具 ───────────────────────────────

    def _rm_tree(self, path: Path) -> bool:
        try:
            import shutil
            shutil.rmtree(path)
            return True
        except Exception:
            return False

    def _run(self, cmd: List[str]) -> bool:
        try:
            subprocess.run(cmd, cwd=self.root, check=True, timeout=60)
            return True
        except Exception:
            return False

    # ─────────────────────────────── 執行修復 ───────────────────────────────

    def repair(self, issue: Issue) -> bool:
        if issue.fix is None:
            return False
        try:
            result = issue.fix()
            return bool(result)
        except Exception as e:
            print(f"  修復失敗: {e}")
            return False

    # ─────────────────────────────── 報告 ───────────────────────────────

    def report(self) -> dict:
        by_category = {}
        for issue in self.issues:
            by_category.setdefault(issue.category, []).append(issue)
        return {
            "dna": self.DNA,
            "total": len(self.issues),
            "fixable": sum(1 for i in self.issues if i.fix is not None),
            "fixed": self.fixed,
            "failed": self.failed,
            "categories": {
                cat: [
                    {
                        "severity": i.severity,
                        "message": i.message,
                        "path": str(i.path) if i.path else None,
                        "auto_fix": i.fix is not None,
                    }
                    for i in items
                ]
                for cat, items in by_category.items()
            },
        }

    def print_report(self):
        print("\n" + "=" * 60)
        print("  🐉 龍魂左右互搏 · 自愈審計報告")
        print("=" * 60)
        print(f"  DNA: {self.DNA}")
        print(f"  發現問題: {len(self.issues)}")
        print(f"  可自動修復: {sum(1 for i in self.issues if i.fix is not None)}")
        print(f"  已修復: {self.fixed}")
        print(f"  修復失敗: {self.failed}")
        print("-" * 60)
        for issue in self.issues:
            icon = {"info": "ℹ️", "warning": "⚠️", "error": "❌"}.get(issue.severity, "•")
            fixable = " [可自動修復]" if issue.fix else ""
            print(f"  {icon} [{issue.category}] {issue.message}{fixable}")
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="龍魂左右互搏自愈審計")
    parser.add_argument("--repair", action="store_true", help="自動修復可修復的問題")
    parser.add_argument("--json", action="store_true", help="輸出 JSON 報告")
    args = parser.parse_args()

    engine = SelfHealEngine(ROOT)
    engine.run_all_checks()

    if args.repair:
        print("🐉 開始左右互搏自愈修復...")
        for issue in engine.issues:
            if issue.fix:
                print(f"  修復中: {issue.message}")
                if engine.repair(issue):
                    engine.fixed += 1
                else:
                    engine.failed += 1

    if args.json:
        print(json.dumps(engine.report(), indent=2, ensure_ascii=False))
    else:
        engine.print_report()

    # 非嚴重錯誤不視為失敗
    sys.exit(0)


if __name__ == "__main__":
    main()
