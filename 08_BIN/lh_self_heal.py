#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 自修复/自迭代引擎 v1.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

自动发现项目里的常见问题并尝试修复，可在本地或鲲鹏服务器上定期运行。

DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-SELF-HEAL-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过
"""

import os
import sys
import json
import re
import subprocess
import hashlib
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# ============================================================
# 项目配置
# ============================================================
PROJECT_DIR = Path.home() / "longhun-system"
BIN_DIR = PROJECT_DIR / "bin"
STATE_DIR = PROJECT_DIR / "08_STATE"
AUDIT_DIR = PROJECT_DIR / "04_AUDIT"
LOGS_DIR = PROJECT_DIR / "logs"
AUDIT_FILE = AUDIT_DIR / "self_heal.jsonl"

VENV_PYTHON = PROJECT_DIR / ".venv" / "bin" / "python3"
SYSTEM_PYTHON = Path("/usr/bin/python3")

# 关键依赖
CRITICAL_DEPS = [
    ("pytest", "pytest"),
    ("fastapi", "fastapi"),
    ("uvicorn", "uvicorn"),
    ("httpx", "httpx"),
]

# 关键目录
CRITICAL_DIRS = [STATE_DIR, AUDIT_DIR, LOGS_DIR]

# 关键端口
CRITICAL_PORTS = [8766, 9766]

# Shell 脚本目录
SHELL_DIRS = [BIN_DIR, PROJECT_DIR]

DNA_PREFIX = "#龍芯⚡️"
UID = "9622"


def generate_dna(suffix: str = "") -> str:
    ts = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    rand = hashlib.sha256(f"{suffix}{ts}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"{DNA_PREFIX}{ts}-{suffix}-{UID}-{rand}"


def record_audit(operation: str, detail: Any, status: str = "ok"):
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now().isoformat(),
        "dna": generate_dna("SELF-HEAL"),
        "operation": operation,
        "detail": detail,
        "status": status,
    }
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def run_shell(cmd: str, timeout: int = 60) -> Dict[str, Any]:
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout
        )
        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def get_python() -> Path:
    if VENV_PYTHON.exists():
        return VENV_PYTHON
    if SYSTEM_PYTHON.exists():
        return SYSTEM_PYTHON
    return Path("python3")


# ============================================================
# 检查器
# ============================================================
class Issue:
    def __init__(self, category: str, file: Optional[Path], message: str, fixable: bool = True):
        self.category = category
        self.file = file
        self.message = message
        self.fixable = fixable
        self.fixed = False

    def to_dict(self):
        return {
            "category": self.category,
            "file": str(self.file) if self.file else None,
            "message": self.message,
            "fixable": self.fixable,
            "fixed": self.fixed,
        }


class HealthChecker:
    def __init__(self):
        self.issues: List[Issue] = []

    # ---------- 1. 关键目录 ----------
    def check_critical_dirs(self):
        for d in CRITICAL_DIRS:
            if not d.exists():
                self.issues.append(
                    Issue("missing_dir", d, f"关键目录不存在: {d}")
                )

    # ---------- 2. 关键依赖 ----------
    def check_dependencies(self):
        py = get_python()
        for module, package in CRITICAL_DEPS:
            result = run_shell(f"{py} -c 'import {module}'", timeout=10)
            if not result["ok"]:
                self.issues.append(
                    Issue("missing_dep", None, f"缺少依赖: {package} (import {module})")
                )

    # ---------- 3. Shell 脚本 shebang ----------
    def check_shell_shebangs(self):
        for d in SHELL_DIRS:
            if not d.exists():
                continue
            for f in d.iterdir():
                if not f.is_file():
                    continue
                # 无扩展名的可执行文件或 .sh 文件
                if f.suffix not in ("", ".sh"):
                    continue
                try:
                    text = f.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    continue
                if not text.strip():
                    continue
                # 判断是不是 shell 脚本（包含 bash 关键字或常见 shell 语法）
                shell_markers = ["#!/bin/bash", "#!/bin/sh", "#!/usr/bin/env bash"]
                is_shell = any(m in text.splitlines()[:5] for m in shell_markers)
                if not is_shell:
                    continue
                lines = text.splitlines()
                if not lines:
                    continue
                first = lines[0].strip()
                if not first.startswith("#!/"):
                    self.issues.append(
                        Issue("bad_shebang", f, f"shebang 不在第一行: {f}")
                    )

    # ---------- 4. Python 语法 ----------
    def check_python_syntax(self):
        py_files = list(PROJECT_DIR.rglob("*.py"))
        # 限制范围，避免扫描过大
        py_files = [p for p in py_files if "__pycache__" not in str(p)]
        for f in py_files[:200]:  # 每次最多 200 个
            result = run_shell(f"python3 -m py_compile {f}", timeout=10)
            if not result["ok"]:
                self.issues.append(
                    Issue("python_syntax", f, f"Python 语法错误: {result['stderr']}")
                )

    # ---------- 5. 关键端口 ----------
    def check_ports(self):
        for port in CRITICAL_PORTS:
            result = run_shell(f"lsof -ti :{port}")
            if result["stdout"]:
                continue
            self.issues.append(
                Issue("port_down", None, f"端口 {port} 无服务监听", fixable=False)
            )

    # ---------- 6. pyrightconfig 存在性 ----------
    def check_pyright_config(self):
        config = PROJECT_DIR / "pyrightconfig.json"
        if not config.exists():
            self.issues.append(
                Issue("missing_pyright_config", config, "缺少 pyrightconfig.json")
            )

    def run_all(self) -> List[Issue]:
        self.issues = []
        self.check_critical_dirs()
        self.check_dependencies()
        self.check_shell_shebangs()
        self.check_python_syntax()
        self.check_ports()
        self.check_pyright_config()
        return self.issues


# ============================================================
# 修复器
# ============================================================
class AutoFixer:
    def __init__(self, issues: List[Issue]):
        self.issues = issues

    def fix_missing_dir(self, issue: Issue):
        if issue.file:
            issue.file.mkdir(parents=True, exist_ok=True)
            issue.fixed = True

    def fix_missing_dep(self, issue: Issue):
        py = get_python()
        # 从 message 解析包名
        m = re.search(r"缺少依赖: ([^ ]+)", issue.message)
        package = m.group(1) if m else None
        if not package:
            return
        print(f"   📦 尝试安装 {package} 到 {py} ...")
        result = run_shell(f"{py} -m pip install {package}", timeout=180)
        print(f"   {'✅' if result['ok'] else '❌'} pip install {package}")
        if result["stderr"]:
            print(f"   stderr: {result['stderr'][:300]}")
        # 再次验证导入
        verify = run_shell(f"{py} -c 'import {package}'", timeout=15)
        issue.fixed = verify["ok"]

    def fix_bad_shebang(self, issue: Issue):
        if not issue.file:
            return
        try:
            text = issue.file.read_text(encoding="utf-8")
            lines = text.splitlines()
            # 找到第一个 shebang
            shebang_idx = None
            for i, line in enumerate(lines):
                if line.strip().startswith("#!/"):
                    shebang_idx = i
                    break
            if shebang_idx is None:
                # 没有 shebang，加一行 bash
                new_lines = ["#!/bin/bash", ""] + lines
            else:
                shebang = lines[shebang_idx]
                new_lines = [shebang]
                for i, line in enumerate(lines):
                    if i != shebang_idx:
                        new_lines.append(line)
            issue.file.write_text("\n".join(new_lines), encoding="utf-8")
            issue.fixed = True
        except Exception as e:
            issue.message += f" (修复失败: {e})"

    def fix_missing_pyright_config(self, issue: Issue):
        config = PROJECT_DIR / "pyrightconfig.json"
        content = {
            "venv": ".venv",
            "venvPath": ".",
            "pythonVersion": "3.12",
            "extraPaths": ["bin", "08_BIN", "05_ENGINES", "engines", "core"],
            "include": ["bin", "08_BIN", "05_ENGINES", "engines", "core", "tests"],
            "exclude": ["**/__pycache__", "**/.venv", "**/node_modules", "**/*.pyc"],
            "typeCheckingMode": "standard",
        }
        config.write_text(json.dumps(content, indent=2, ensure_ascii=False), encoding="utf-8")
        issue.fixed = True

    def run(self) -> List[Issue]:
        for issue in self.issues:
            if not issue.fixable:
                continue
            try:
                if issue.category == "missing_dir":
                    self.fix_missing_dir(issue)
                elif issue.category == "missing_dep":
                    self.fix_missing_dep(issue)
                elif issue.category == "bad_shebang":
                    self.fix_bad_shebang(issue)
                elif issue.category == "missing_pyright_config":
                    self.fix_missing_pyright_config(issue)
            except Exception as e:
                issue.message += f" (修复异常: {e})"
        return self.issues


# ============================================================
# 报告
# ============================================================
def print_report(issues: List[Issue]):
    print("\n" + "=" * 60, flush=True)
    print("🐉 龍魂 · 自修复报告", flush=True)
    print("=" * 60, flush=True)

    fixed = [i for i in issues if i.fixed]
    unfixed = [i for i in issues if i.fixable and not i.fixed]
    info = [i for i in issues if not i.fixable]

    if not issues:
        print("✅ 未发现明显问题", flush=True)
        return

    print(f"\n📊 共发现 {len(issues)} 项，已修复 {len(fixed)} 项", flush=True)

    if fixed:
        print("\n🟢 已修复:", flush=True)
        for i in fixed:
            print(f"   ✅ [{i.category}] {i.file or ''} {i.message}", flush=True)

    if unfixed:
        print("\n🔴 未修复:", flush=True)
        for i in unfixed:
            print(f"   ❌ [{i.category}] {i.file or ''} {i.message}", flush=True)

    if info:
        print("\n🟡 提示（需人工确认）:", flush=True)
        for i in info:
            print(f"   ⚠️  [{i.category}] {i.file or ''} {i.message}", flush=True)

    print("\n" + "=" * 60, flush=True)


# ============================================================
# 迭代模式
# ============================================================
def iterate(max_rounds: int = 3):
    for round_num in range(1, max_rounds + 1):
        print(f"\n🔄 自修复迭代第 {round_num}/{max_rounds} 轮...", flush=True)
        checker = HealthChecker()
        issues = checker.run_all()
        if not issues:
            print("✅ 无问题，提前结束迭代", flush=True)
            break
        fixer = AutoFixer(issues)
        fixed_issues = fixer.run()
        print_report(fixed_issues)
        record_audit(
            f"self_heal_round_{round_num}",
            {"total": len(issues), "fixed": len([i for i in fixed_issues if i.fixed])},
            "ok",
        )
        # 如果本轮没有修复任何问题，停止迭代避免死循环
        if not any(i.fixed for i in fixed_issues):
            print("⚠️ 本轮未修复任何问题，停止迭代", flush=True)
            break


# ============================================================
# 命令行入口
# ============================================================
def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║  🐉 龍魂 · 自修复/自迭代引擎 v1.0                           ║
║  自动发现 → 自动修复 → 迭代验证                             ║
║  DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-SELF-HEAL-UID9622       ║
╚══════════════════════════════════════════════════════════════╝
    """, flush=True)

    max_rounds = 3
    if len(sys.argv) > 1:
        try:
            max_rounds = int(sys.argv[1])
        except ValueError:
            pass

    iterate(max_rounds)

    print("\n✅ 自修复完成。详细记录见 04_AUDIT/self_heal.jsonl", flush=True)


if __name__ == "__main__":
    main()
