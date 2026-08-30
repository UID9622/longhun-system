# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂环境验证器 (Longhun Environment Validator)
==============================
DNA: #龍芯⚡️2026-06-19-LONGHUN-DEPLOY-READY-v5.2

验证部署环境的各项条件：Python版本、依赖包、系统资源、端口占用。

用法:
    python3 环境验证器.py [--detail] [--fix]
"""

import os
import sys
import json
import socket
import shutil
import platform
import subprocess
import importlib.util
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field

SKILL_DNA = "#龍芯⚡️2026-06-19-LONGHUN-DEPLOY-READY-v5.2"


class Colors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    OKBLUE = '\033[94m'


@dataclass
class ValidationResult:
    component: str
    status: str  # PASS / WARN / FAIL
    current: str
    required: str
    message: str
    auto_fixed: bool = False


class EnvironmentValidator:
    """环境验证器 - 全面检查部署环境"""

    def __init__(self, auto_fix: bool = False):
        self.auto_fix = auto_fix
        self.results: List[ValidationResult] = []
        self.checks = {
            "python": self._check_python,
            "pip": self._check_pip,
            "os": self._check_os,
            "memory": self._check_memory,
            "disk": self._check_disk,
            "ports": self._check_ports,
            "git": self._check_git,
            "curl_wget": self._check_network_tools,
            "docker": self._check_docker,
            "env_vars": self._check_env_vars,
        }

    def _check_python(self) -> ValidationResult:
        """检查Python版本"""
        version = sys.version_info
        current = f"{version.major}.{version.minor}.{version.micro}"
        required = ">= 3.9"
        passed = (version.major, version.minor) >= (3, 9)
        return ValidationResult("Python", "PASS" if passed else "FAIL", current, required,
                               f"Python {current} {'满足' if passed else '不满足'}要求")

    def _check_pip(self) -> ValidationResult:
        """检查pip版本"""
        try:
            import pip
            current = pip.__version__
            ver_tuple = tuple(map(int, current.split('.')[:2]))
            required = ">= 21.0"
            passed = ver_tuple >= (21, 0)
            return ValidationResult("pip", "PASS" if passed else "WARN", current, required,
                                   f"pip {current}")
        except Exception:
            return ValidationResult("pip", "FAIL", "unknown", ">= 21.0", "无法检测pip版本")

    def _check_os(self) -> ValidationResult:
        """检查操作系统"""
        system = platform.system()
        release = platform.release()
        supported = ["Linux", "Darwin", "Windows"]
        passed = system in supported
        return ValidationResult("OS", "PASS" if passed else "WARN",
                               f"{system} {release}", "Linux/macOS/Windows",
                               f"操作系统: {system} {release}")

    def _check_memory(self) -> ValidationResult:
        """检查内存"""
        try:
            import psutil
            mem = psutil.virtual_memory()
            available_mb = mem.available // (1024 * 1024)
            total_mb = mem.total // (1024 * 1024)
            required_mb = 512
            passed = available_mb >= required_mb
            return ValidationResult("内存", "PASS" if passed else "WARN",
                                   f"{available_mb}MB可用 / {total_mb}MB总",
                                   f">= {required_mb}MB可用",
                                   f"可用内存: {available_mb}MB")
        except ImportError:
            return ValidationResult("内存", "WARN", "unknown", ">= 512MB",
                                   "安装psutil获取详细内存信息: pip install psutil")

    def _check_disk(self) -> ValidationResult:
        """检查磁盘空间"""
        try:
            stat = shutil.disk_usage(".")
            free_gb = stat.free // (1024 ** 3)
            total_gb = stat.total // (1024 ** 3)
            required_gb = 5
            passed = free_gb >= required_gb
            return ValidationResult("磁盘", "PASS" if passed else "FAIL",
                                   f"{free_gb}GB可用 / {total_gb}GB总", f">= {required_gb}GB",
                                   f"可用磁盘: {free_gb}GB")
        except Exception as e:
            return ValidationResult("磁盘", "WARN", "unknown", ">= 5GB", str(e))

    def _check_ports(self) -> ValidationResult:
        """检查端口占用"""
        ports = [8000, 8080, 5432, 6379, 9090]
        occupied = []
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.bind(("0.0.0.0", port))
            except OSError:
                occupied.append(str(port))
            finally:
                sock.close()
        passed = len(occupied) == 0
        msg = f"端口空闲" if passed else f"端口被占用: {', '.join(occupied)}"
        return ValidationResult("端口", "PASS" if passed else "WARN",
                               f"{len(ports) - len(occupied)}/{len(ports)}可用",
                               "关键端口空闲", msg)

    def _check_git(self) -> ValidationResult:
        """检查Git"""
        git_path = shutil.which("git")
        if git_path:
            try:
                result = subprocess.run(["git", "--version"], capture_output=True, text=True, timeout=10)
                version = result.stdout.strip().replace("git version ", "")
                return ValidationResult("Git", "PASS", version, "已安装",
                                       f"Git {version} at {git_path}")
            except Exception:
                return ValidationResult("Git", "WARN", "unknown", "已安装", "Git检测异常")
        return ValidationResult("Git", "WARN", "未安装", "已安装", "Git未安装，代码拉取功能受限")

    def _check_network_tools(self) -> ValidationResult:
        """检查网络工具"""
        tools = []
        for tool in ["curl", "wget"]:
            if shutil.which(tool):
                tools.append(tool)
        passed = len(tools) > 0
        return ValidationResult("网络工具", "PASS" if passed else "WARN",
                               ", ".join(tools) if tools else "无",
                               "curl 或 wget", f"可用: {', '.join(tools)}" if tools else "建议安装curl")

    def _check_docker(self) -> ValidationResult:
        """检查Docker"""
        docker_path = shutil.which("docker")
        if docker_path:
            try:
                result = subprocess.run(["docker", "--version"], capture_output=True, text=True, timeout=10)
                version = result.stdout.strip()
                return ValidationResult("Docker", "PASS", version, "可选",
                                       f"Docker已安装: {version[:30]}")
            except Exception:
                return ValidationResult("Docker", "WARN", "unknown", "可选", "Docker检测异常")
        return ValidationResult("Docker", "WARN", "未安装", "可选",
                               "Docker未安装(可选)，容器化部署不可用")

    def _check_env_vars(self) -> ValidationResult:
        """检查必要环境变量"""
        required = ["APP_ENV", "DATABASE_URL", "SECRET_KEY"]
        configured = [v for v in required if os.getenv(v)]
        passed = len(configured) == len(required)
        return ValidationResult("环境变量", "PASS" if passed else "WARN",
                               f"{len(configured)}/{len(required)}已设置", "全部设置",
                               f"已设置: {', '.join(configured)}" if configured else "均未设置")

    def run_all(self) -> List[ValidationResult]:
        """运行所有验证"""
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║        龍魂环境验证器                                          ║
╠══════════════════════════════════════════════════════════════╣
║  {SKILL_DNA}    ║
╚══════════════════════════════════════════════════════════════╝
""")
        for name, check_fn in self.checks.items():
            print(f"  检查 {name} ... ", end="", flush=True)
            result = check_fn()
            self.results.append(result)
            color = Colors.OKGREEN if result.status == "PASS" else (
                Colors.WARNING if result.status == "WARN" else Colors.FAIL
            )
            print(f"{color}[{result.status}]{Colors.ENDC}")
            print(f"      当前: {result.current} | 要求: {result.required}")
            if result.message:
                print(f"      {result.message}")
        return self.results

    def print_summary(self):
        """打印汇总"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == "PASS")
        warnings = sum(1 for r in self.results if r.status == "WARN")
        failed = sum(1 for r in self.results if r.status == "FAIL")

        print(f"\n{'='*50}")
        print("  环境验证汇总")
        print(f"{'='*50}")
        print(f"  通过:   {Colors.OKGREEN}{passed}{Colors.ENDC}")
        print(f"  警告:   {Colors.WARNING}{warnings}{Colors.ENDC}")
        print(f"  失败:   {Colors.FAIL}{failed}{Colors.ENDC}")
        print(f"  总计:   {total}")

        if failed == 0:
            print(f"\n  {Colors.OKGREEN}✅ 环境验证通过，可以进行部署{Colors.ENDC}")
        else:
            print(f"\n  {Colors.FAIL}❌ 环境存在 {failed} 个问题，请先修复{Colors.ENDC}")

        # 保存JSON报告
        report = {
            "timestamp": datetime.now().isoformat(),
            "dna": SKILL_DNA,
            "summary": {"pass": passed, "warn": warnings, "fail": failed, "total": total},
            "details": [{"component": r.component, "status": r.status,
                        "current": r.current, "required": r.required,
                        "message": r.message} for r in self.results]
        }
        os.makedirs("logs", exist_ok=True)
        with open(f"logs/env-validation-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json", 'w') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", action="store_true", help="自动修复")
    parser.add_argument("--detail", action="store_true", help="详细输出")
    args = parser.parse_args()

    validator = EnvironmentValidator(auto_fix=args.fix)
    validator.run_all()
    validator.print_summary()


if __name__ == "__main__":
    main()
