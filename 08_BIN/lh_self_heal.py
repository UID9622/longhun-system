#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️2026-06-18-LONGHUN-SELF-HEAL-FILE1-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂左右互搏 · 自愈审计引擎 v1.0

自己寻找漏洞，自己修复，自己叠送。
复杂留给 AI，简单留给人。

DNA:#龍芯⚡️2026-06-18-LONGHUN-SELF-HEAL-FILE1-v1.0
"""

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Any


ROOT = Path(__file__).resolve().parent.parent


@dataclass
class Issue:
    category: str
    severity: str      # info / warning / error
    message: str
    path: Optional[Path] = None
    fix: Optional[callable] = field(default=None, compare=False)


class SelfHealEngine:
    """龍魂系统自愈引擎"""

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

    # ─────────────────────────────── 检查项 ───────────────────────────────

    def check_required_directories(self):
        required = ["logs", "var", "var/kimi-agent-v2", "var/xpay"]
        for name in required:
            path = self.root / name
            if not path.exists():
                self.issues.append(Issue(
                    category="目录结构",
                    severity="warning",
                    message=f"缺少必要目录: {name}",
                    path=path,
                    fix=lambda p=path: p.mkdir(parents=True, exist_ok=True) or True
                ))

    def check_script_executability(self):
        scripts = [
            "bin/lh_autostart.sh",
            "bin/install-autostart.sh",
            "bin/build-desktop-switch.sh",
            "bin/build-chinese-editor.sh",
            "bin/build-control-center.sh",
            "bin/lh_status.sh",
            "bin/lh_daily-audit.sh",
            "bin/refresh-longhun.sh",
        ]
        for rel in scripts:
            path = self.root / rel
            if not path.exists():
                continue
            if not os.access(path, os.X_OK):
                self.issues.append(Issue(
                    category="脚本权限",
                    severity="warning",
                    message=f"脚本未设置可执行: {rel}",
                    path=path,
                    fix=lambda p=path: (p.chmod(p.stat().st_mode | 0o111), True)[1]
                ))

    def check_pycache_pollution(self):
        pycaches = list(self.root.rglob("__pycache__"))
        # 只处理 .git 未忽略的（简单判断：不在 _archive 或 .venv 下）
        dirty = [p for p in pycaches if not any(x in p.parts for x in [".venv", "venv", "_archive"])]
        if dirty:
            self.issues.append(Issue(
                category="环境清洁",
                severity="info",
                message=f"发现 {len(dirty)} 个 __pycache__ 目录",
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
                    category="桌面菜单",
                    severity="warning",
                    message="菜单注册表比桌面 App 新，需要重新生成",
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
                    category="Git 状态",
                    severity="info",
                    message=f"工作区有 {len(lines)} 处未提交变更",
                    fix=None  # 不自动提交，只报告
                ))
        except Exception as e:
            self.issues.append(Issue("Git 状态", "error", f"无法检查 Git: {e}"))

    def check_duplicate_skills(self):
        """扫描重复的技能文件名"""
        names = {}
        for path in self.root.rglob("longhun_*_engine.py"):
            if any(x in path.parts for x in [".git", "__pycache__"]):
                continue
            names.setdefault(path.name, []).append(path)
        for name, paths in names.items():
            if len(paths) > 1:
                self.issues.append(Issue(
                    category="重复模块",
                    severity="warning",
                    message=f"技能文件重复: {name} 出现在 {len(paths)} 处",
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
                    category="服务健康",
                    severity="warning",
                    message="龍魂操作台 (:9622) 未运行",
                    fix=lambda: self._run([
                        "bash", "-c",
                        f"cd {self.root} && export PYTHONPATH={self.root} && mkdir -p logs && "
                        f"cd control-panel && nohup python3 main.py >> ../logs/control-panel.log 2>&1 &"
                    ])
                ))
        except Exception as e:
            self.issues.append(Issue("服务健康", "error", f"无法检查端口: {e}"))

    def check_file_permissions(self):
        """检查关键数据文件权限是否过宽"""
        sensitive = [
            self.root / "xpay" / "var" / "xpay.db",
        ]
        for path in sensitive:
            if path.exists():
                mode = path.stat().st_mode & 0o777
                if mode & 0o077:
                    self.issues.append(Issue(
                        category="文件权限",
                        severity="warning",
                        message=f"敏感文件权限过宽: {path} ({oct(mode)})",
                        path=path,
                        fix=lambda p=path: (p.chmod(0o600), True)[1]
                    ))

    # ─────────────────────────────── 修复工具 ───────────────────────────────

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

    # ─────────────────────────────── 执行修复 ───────────────────────────────

    def repair(self, issue: Issue) -> bool:
        if issue.fix is None:
            return False
        try:
            result = issue.fix()
            return bool(result)
        except Exception as e:
            print(f"  修复失败: {e}")
            return False

    # ─────────────────────────────── 报告 ───────────────────────────────

    def report(self) -> dict[str, Any]:
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
        print("  🐉 龍魂左右互搏 · 自愈审计报告")
        print("=" * 60)
        print(f"  DNA: {self.DNA}")
        print(f"  发现问题: {len(self.issues)}")
        print(f"  可自动修复: {sum(1 for i in self.issues if i.fix is not None)}")
        print(f"  已修复: {self.fixed}")
        print(f"  修复失败: {self.failed}")
        print("-" * 60)
        for issue in self.issues:
            icon = {"info": "ℹ️", "warning": "⚠️", "error": "❌"}.get(issue.severity, "•")
            fixable = " [可自动修复]" if issue.fix else ""
            print(f"  {icon} [{issue.category}] {issue.message}{fixable}")
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="龍魂左右互搏自愈审计")
    parser.add_argument("--repair", action="store_true", help="自动修复可修复的问题")
    parser.add_argument("--json", action="store_true", help="输出 JSON 报告")
    args = parser.parse_args()

    engine = SelfHealEngine(ROOT)
    engine.run_all_checks()

    if args.repair:
        print("🐉 开始左右互搏自愈修复...")
        for issue in engine.issues:
            if issue.fix:
                print(f"  修复中: {issue.message}")
                if engine.repair(issue):
                    engine.fixed += 1
                else:
                    engine.failed += 1

    if args.json:
        print(json.dumps(engine.report(), indent=2, ensure_ascii=False))
    else:
        engine.print_report()

    # 非严重错误不视为失败
    sys.exit(0)


if __name__ == "__main__":
    main()
