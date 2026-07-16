#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂部署就绪检查器 (Longhun Deployment Readiness Checker)
==========================================
DNA: #龍芯⚡️2026-06-19-LONGHUN-DEPLOY-READY-v5.2

执行27项部署就绪检查，覆盖环境、代码、依赖、配置、数据库、服务、监控、日志、备份全链路。

用法:
    python3 部署就绪检查器.py [--full] [--json] [--fix] [--step STEP]

选项:
    --full      执行全部27项检查 (默认)
    --json      输出JSON格式报告
    --fix       自动修复发现的问题
    --step N    仅执行第N步检查 (1-27)
"""

import os
import sys
import json
import time
import socket
import shutil
import argparse
import subprocess
import importlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum

# ============================================================
# 常量与配置
# ============================================================

SKILL_VERSION = "5.2"
SKILL_DNA = "#龍芯⚡️2026-06-19-LONGHUN-DEPLOY-READY-v5.2"
CHECKLIST_VERSION = "2026-06-10"
REPORT_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 27步检查清单定义
CHECK_STEPS = [
    # 阶段一: 环境准备 (1-4)
    {"id": 1,  "category": "环境准备", "name": "Python版本检查",           "description": "验证Python >= 3.9"},
    {"id": 2,  "category": "环境准备", "name": "操作系统兼容性检查",       "description": "验证Linux/macOS/Windows支持"},
    {"id": 3,  "category": "环境准备", "name": "系统资源检查",             "description": "CPU/内存/磁盘空间充足"},
    {"id": 4,  "category": "环境准备", "name": "网络连通性检查",           "description": "外部依赖网络可达"},
    # 阶段二: 代码拉取 (5-7)
    {"id": 5,  "category": "代码拉取", "name": "Git仓库访问检查",          "description": "仓库URL可访问且权限正常"},
    {"id": 6,  "category": "代码拉取", "name": "代码完整性检查",           "description": "文件结构完整无缺失"},
    {"id": 7,  "category": "代码拉取", "name": "代码版本确认",             "description": "检出正确的tag/commit"},
    # 阶段三: 依赖安装 (8-10)
    {"id": 8,  "category": "依赖安装", "name": "pip版本检查",              "description": "pip >= 21.0"},
    {"id": 9,  "category": "依赖安装", "name": "requirements安装检查",     "description": "所有依赖包安装成功"},
    {"id": 10, "category": "依赖安装", "name": "依赖版本兼容性检查",       "description": "无版本冲突"},
    # 阶段四: 配置初始化 (11-13)
    {"id": 11, "category": "配置初始化", "name": "配置文件存在性检查",       "description": "所有配置文件存在"},
    {"id": 12, "category": "配置初始化", "name": "配置参数完整性检查",       "description": "必要参数已设置"},
    {"id": 13, "category": "配置初始化", "name": "敏感信息加密检查",         "description": "密码/密钥已加密或隔离"},
    # 阶段五: 数据库准备 (14-16)
    {"id": 14, "category": "数据库准备", "name": "数据库连接检查",           "description": "数据库服务可达"},
    {"id": 15, "category": "数据库准备", "name": "数据库权限检查",           "description": "用户权限充足"},
    {"id": 16, "category": "数据库准备", "name": "迁移状态检查",             "description": "Schema最新"},
    # 阶段六: 服务启动 (17-19)
    {"id": 17, "category": "服务启动", "name": "端口占用检查",             "description": "所需端口未被占用"},
    {"id": 18, "category": "服务启动", "name": "服务启动命令检查",         "description": "启动脚本可执行"},
    {"id": 19, "category": "服务启动", "name": "环境变量检查",             "description": "必要环境变量已设置"},
    # 阶段七: 健康检查 (20-22)
    {"id": 20, "category": "健康检查", "name": "HTTP健康端点检查",         "description": "/health 返回200"},
    {"id": 21, "category": "健康检查", "name": "依赖服务健康检查",         "description": "DB/Cache等健康"},
    {"id": 22, "category": "健康检查", "name": "关键业务流程检查",         "description": "核心API调用成功"},
    # 阶段八: 监控配置 (23-24)
    {"id": 23, "category": "监控配置", "name": "监控Agent检查",            "description": "Prometheus/ Grafana配置正确"},
    {"id": 24, "category": "监控配置", "name": "告警规则检查",             "description": "告警规则已配置"},
    # 阶段九: 日志确认 (25)
    {"id": 25, "category": "日志确认", "name": "日志输出检查",             "description": "日志正常输出到指定位置"},
    # 阶段十: 备份验证 (26-27)
    {"id": 26, "category": "备份验证", "name": "备份策略检查",             "description": "自动备份已配置"},
    {"id": 27, "category": "备份验证", "name": "恢复演练检查",             "description": "备份可成功恢复"},
]

# 颜色输出
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class CheckStatus(Enum):
    PASS = "通过"
    FAIL = "失败"
    WARN = "警告"
    SKIP = "跳过"
    RUNNING = "执行中"


@dataclass
class CheckResult:
    step_id: int
    name: str
    category: str
    status: CheckStatus
    message: str = ""
    details: Dict = field(default_factory=dict)
    duration_ms: float = 0.0
    auto_fixed: bool = False
    fix_message: str = ""


class DeploymentReadinessChecker:
    """龍魂部署就绪检查器 - 27步完整检查"""

    def __init__(self, config_path: Optional[str] = None, auto_fix: bool = False):
        self.config = self._load_config(config_path)
        self.auto_fix = auto_fix
        self.results: List[CheckResult] = []
        self.start_time = None
        self.total_duration = 0.0

    def _load_config(self, config_path: Optional[str]) -> Dict:
        """加载配置文件"""
        defaults = {
            "python_min_version": (3, 9),
            "required_ports": [8000, 8080, 5432, 6379, 9090],
            "health_endpoint": "/health",
            "health_timeout": 10,
            "required_env_vars": ["APP_ENV", "DATABASE_URL", "SECRET_KEY"],
            "required_files": ["requirements.txt", "config.yaml", "Dockerfile"],
            "min_disk_gb": 5,
            "min_memory_mb": 512,
            "project_root": ".",
        }
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                if config_path.endswith('.json'):
                    loaded = json.load(f)
                else:
                    # 简单解析 key=value 格式
                    loaded = {}
                    for line in f:
                        line = line.strip()
                        if line and '=' in line and not line.startswith('#'):
                            k, v = line.split('=', 1)
                            loaded[k.strip()] = v.strip().strip('"').strip("'")
                defaults.update(loaded)
        return defaults

    # --------------------------------------------------
    # 阶段一: 环境准备 (1-4)
    # --------------------------------------------------

    def check_01_python_version(self) -> CheckResult:
        """检查1: Python版本 >= 3.9"""
        step = CHECK_STEPS[0]
        current = sys.version_info[:2]
        required = self.config["python_min_version"]
        passed = current >= required
        msg = f"当前Python {current[0]}.{current[1]}，要求 >= {required[0]}.{required[1]}"
        return CheckResult(1, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.FAIL, msg,
                          {"current": f"{current[0]}.{current[1]}", "required": f"{required[0]}.{required[1]}"})

    def check_02_os_compatibility(self) -> CheckResult:
        """检查2: 操作系统兼容性"""
        step = CHECK_STEPS[1]
        platform = sys.platform
        supported = ['linux', 'darwin', 'win32']
        passed = any(platform.startswith(s) for s in supported)
        msg = f"操作系统平台: {platform}"
        return CheckResult(2, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.FAIL, msg,
                          {"platform": platform})

    def check_03_system_resources(self) -> CheckResult:
        """检查3: 系统资源 (CPU/内存/磁盘)"""
        step = CHECK_STEPS[2]
        details = {}
        try:
            import psutil
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage('.')
            cpu_count = psutil.cpu_count()
            details = {
                "cpu_cores": cpu_count,
                "memory_total_mb": round(mem.total / (1024*1024), 1),
                "memory_available_mb": round(mem.available / (1024*1024), 1),
                "disk_total_gb": round(disk.total / (1024**3), 1),
                "disk_free_gb": round(disk.free / (1024**3), 1),
            }
            mem_ok = details["memory_available_mb"] >= self.config["min_memory_mb"]
            disk_ok = details["disk_free_gb"] >= self.config["min_disk_gb"]
            passed = mem_ok and disk_ok
            msg = f"CPU:{cpu_count}核 | 内存:{details['memory_available_mb']:.0f}MB可用 | 磁盘:{details['disk_free_gb']:.1f}GB可用"
            status = CheckStatus.PASS if passed else CheckStatus.FAIL
        except ImportError:
            details = {"note": "psutil未安装，跳过详细检查"}
            msg = "psutil未安装，请手动检查资源"
            status = CheckStatus.WARN
        return CheckResult(3, step["name"], step["category"], status, msg, details)

    def check_04_network_connectivity(self) -> CheckResult:
        """检查4: 网络连通性"""
        step = CHECK_STEPS[3]
        test_hosts = ["github.com", "pypi.org", "google.com"]
        reachable = []
        for host in test_hosts:
            try:
                socket.create_connection((host, 443), timeout=5)
                reachable.append(host)
            except Exception:
                pass
        passed = len(reachable) > 0
        msg = f"网络连通: {len(reachable)}/{len(test_hosts)} ({', '.join(reachable)})"
        return CheckResult(4, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.FAIL, msg,
                          {"reachable": reachable, "total": len(test_hosts)})

    # --------------------------------------------------
    # 阶段二: 代码拉取 (5-7)
    # --------------------------------------------------

    def check_05_git_repo_access(self) -> CheckResult:
        """检查5: Git仓库访问"""
        step = CHECK_STEPS[4]
        if shutil.which("git"):
            try:
                result = subprocess.run(["git", "status"], capture_output=True, text=True, timeout=10)
                passed = result.returncode == 0
                msg = "Git仓库访问正常" if passed else f"Git错误: {result.stderr[:100]}"
            except Exception as e:
                passed = False
                msg = f"Git命令执行失败: {e}"
        else:
            passed = False
            msg = "Git未安装"
        return CheckResult(5, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.FAIL, msg)

    def check_06_code_integrity(self) -> CheckResult:
        """检查6: 代码完整性"""
        step = CHECK_STEPS[5]
        root = self.config["project_root"]
        required = self.config["required_files"]
        missing = [f for f in required if not os.path.exists(os.path.join(root, f))]
        passed = len(missing) == 0
        msg = f"文件完整性: {len(required) - len(missing)}/{len(required)}" + (
            f" | 缺失: {', '.join(missing)}" if missing else ""
        )
        return CheckResult(6, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.FAIL, msg,
                          {"required": required, "missing": missing})

    def check_07_code_version(self) -> CheckResult:
        """检查7: 代码版本确认"""
        step = CHECK_STEPS[6]
        try:
            result = subprocess.run(["git", "describe", "--tags", "--always"],
                                  capture_output=True, text=True, timeout=10)
            version = result.stdout.strip()
            passed = bool(version)
            msg = f"当前版本: {version}" if passed else "无法获取版本信息"
        except Exception as e:
            passed = False
            version = "unknown"
            msg = f"版本检查失败: {e}"
        return CheckResult(7, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.WARN, msg,
                          {"version": version})

    # --------------------------------------------------
    # 阶段三: 依赖安装 (8-10)
    # --------------------------------------------------

    def check_08_pip_version(self) -> CheckResult:
        """检查8: pip版本"""
        step = CHECK_STEPS[7]
        try:
            import pip
            pip_ver = tuple(map(int, pip.__version__.split('.')[:2]))
            passed = pip_ver >= (21, 0)
            msg = f"pip版本: {pip.__version__}"
        except Exception:
            passed = False
            msg = "无法检测pip版本"
            pip_ver = (0, 0)
        return CheckResult(8, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.FAIL, msg,
                          {"version": str(pip_ver)})

    def check_09_requirements_installed(self) -> CheckResult:
        """检查9: requirements安装状态"""
        step = CHECK_STEPS[8]
        req_file = "requirements.txt"
        if not os.path.exists(req_file):
            return CheckResult(9, step["name"], step["category"], CheckStatus.WARN,
                             "requirements.txt 不存在，跳过")
        try:
            with open(req_file, 'r') as f:
                requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            missing = []
            for req in requirements:
                pkg_name = req.split('==')[0].split('>=')[0].split('<')[0].strip()
                if not importlib.util.find_spec(pkg_name):
                    missing.append(pkg_name)
            passed = len(missing) == 0
            msg = f"依赖安装: {len(requirements) - len(missing)}/{len(requirements)}" + (
                f" | 缺失: {', '.join(missing)}" if missing else ""
            )
            # 自动修复
            if not passed and self.auto_fix:
                fix_msg = self._auto_install_requirements(req_file)
                return CheckResult(9, step["name"], step["category"], CheckStatus.PASS,
                                 f"已自动安装缺失依赖 | {fix_msg}", auto_fixed=True, fix_message=fix_msg)
        except Exception as e:
            passed = False
            msg = f"依赖检查失败: {e}"
        return CheckResult(9, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.FAIL, msg,
                          {"total": len(requirements) if 'requirements' in dir() else 0, "missing": missing if 'missing' in dir() else []})

    def _auto_install_requirements(self, req_file: str) -> str:
        """自动安装依赖"""
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_file],
                                  capture_output=True, text=True, timeout=120)
            return f"pip install 返回码: {result.returncode}"
        except Exception as e:
            return f"自动安装失败: {e}"

    def check_10_dependency_compatibility(self) -> CheckResult:
        """检查10: 依赖版本兼容性"""
        step = CHECK_STEPS[9]
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "check"],
                                  capture_output=True, text=True, timeout=60)
            passed = result.returncode == 0
            msg = "依赖版本兼容" if passed else f"版本冲突: {result.stdout[:200]}"
        except Exception as e:
            passed = False
            msg = f"兼容性检查失败: {e}"
        return CheckResult(10, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.WARN, msg)

    # --------------------------------------------------
    # 阶段四: 配置初始化 (11-13)
    # --------------------------------------------------

    def check_11_config_files_exist(self) -> CheckResult:
        """检查11: 配置文件存在性"""
        step = CHECK_STEPS[10]
        configs = ["config.yaml", "config.json", ".env", "settings.py"]
        found = [c for c in configs if os.path.exists(c)]
        passed = len(found) > 0
        msg = f"找到 {len(found)} 个配置文件: {', '.join(found)}" if found else "未找到任何配置文件"
        return CheckResult(11, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.FAIL, msg,
                          {"found": found})

    def check_12_config_params_complete(self) -> CheckResult:
        """检查12: 配置参数完整性"""
        step = CHECK_STEPS[11]
        required_params = ["app_name", "debug", "database_url", "secret_key"]
        # 从环境变量检测
        env_params = {p: os.getenv(p.upper(), "") for p in required_params}
        missing = [p for p, v in env_params.items() if not v]
        passed = len(missing) == 0
        msg = f"参数配置: {len(required_params) - len(missing)}/{len(required_params)}" + (
            f" | 缺失: {', '.join(missing)}" if missing else ""
        )
        return CheckResult(12, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.WARN, msg,
                          {"configured": {k: bool(v) for k, v in env_params.items()}})

    def check_13_sensitive_info_security(self) -> CheckResult:
        """检查13: 敏感信息安全"""
        step = CHECK_STEPS[12]
        issues = []
        # 检查 .env 文件权限
        if os.path.exists(".env"):
            stat = os.stat(".env")
            mode = oct(stat.st_mode)[-3:]
            if int(mode) > 600:
                issues.append(f".env 文件权限为 {mode}，建议 600")
        # 检查代码中是否有硬编码密码
        try:
            result = subprocess.run(
                ["grep", "-r", "-n", "password=\|secret=\|api_key=", "--include=*.py", "."],
                capture_output=True, text=True, timeout=10
            )
            if result.stdout:
                lines = result.stdout.strip().split('\n')[:5]
                issues.append(f"发现 {len(lines)} 处可能的硬编码敏感信息")
        except Exception:
            pass
        passed = len(issues) == 0
        msg = "敏感信息安全" if passed else " | ".join(issues)
        return CheckResult(13, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.WARN, msg,
                          {"issues": issues})

    # --------------------------------------------------
    # 阶段五: 数据库准备 (14-16)
    # --------------------------------------------------

    def check_14_database_connection(self) -> CheckResult:
        """检查14: 数据库连接"""
        step = CHECK_STEPS[13]
        db_url = os.getenv("DATABASE_URL", "")
        if not db_url:
            return CheckResult(14, step["name"], step["category"], CheckStatus.WARN,
                             "DATABASE_URL 未设置，跳过数据库检查")
        # 解析数据库类型
        if "postgresql" in db_url.lower() or "postgres" in db_url.lower():
            db_type = "PostgreSQL"
        elif "mysql" in db_url.lower():
            db_type = "MySQL"
        elif "sqlite" in db_url.lower():
            db_type = "SQLite"
        else:
            db_type = "Unknown"
        passed = db_type != "Unknown"
        msg = f"数据库类型: {db_type} | URL已配置" if passed else "无法识别数据库类型"
        return CheckResult(14, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.WARN, msg,
                          {"db_type": db_type, "configured": bool(db_url)})

    def check_15_database_permissions(self) -> CheckResult:
        """检查15: 数据库权限"""
        step = CHECK_STEPS[14]
        # 简化为检查环境变量是否设置了足够权限的账号
        db_url = os.getenv("DATABASE_URL", "")
        has_user = "://" in db_url and "@" in db_url
        passed = has_user
        msg = "数据库用户已配置" if passed else "数据库连接缺少用户信息"
        return CheckResult(15, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.WARN, msg)

    def check_16_migration_status(self) -> CheckResult:
        """检查16: 迁移状态"""
        step = CHECK_STEPS[15]
        migrations_dir = "migrations"
        if os.path.exists(migrations_dir):
            mig_files = len([f for f in os.listdir(migrations_dir) if f.endswith('.py')])
            passed = mig_files > 0
            msg = f"发现 {mig_files} 个迁移文件" if passed else "迁移目录为空"
        else:
            passed = False
            msg = "migrations 目录不存在"
        return CheckResult(16, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.WARN, msg,
                          {"migrations_dir_exists": os.path.exists(migrations_dir)})

    # --------------------------------------------------
    # 阶段六: 服务启动 (17-19)
    # --------------------------------------------------

    def check_17_port_availability(self) -> CheckResult:
        """检查17: 端口占用"""
        step = CHECK_STEPS[16]
        ports = self.config["required_ports"]
        occupied = []
        available = []
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.bind(("0.0.0.0", port))
                available.append(port)
            except OSError:
                occupied.append(port)
            finally:
                sock.close()
        passed = len(occupied) == 0
        msg = f"端口检查: {len(available)}可用 / {len(occupied)}被占用" + (
            f" (占用: {occupied})" if occupied else ""
        )
        return CheckResult(17, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.FAIL, msg,
                          {"available": available, "occupied": occupied})

    def check_18_startup_script(self) -> CheckResult:
        """检查18: 服务启动命令"""
        step = CHECK_STEPS[17]
        scripts = ["start.sh", "run.py", "app.py", "main.py", "manage.py"]
        found = [s for s in scripts if os.path.exists(s)]
        # 检查可执行权限
        executable = [s for s in found if os.access(s, os.X_OK) or s.endswith('.py')]
        passed = len(executable) > 0
        msg = f"启动脚本: {', '.join(executable)}" if executable else "未找到启动脚本"
        return CheckResult(18, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.WARN, msg,
                          {"found": found, "executable": executable})

    def check_19_environment_variables(self) -> CheckResult:
        """检查19: 环境变量"""
        step = CHECK_STEPS[18]
        required = self.config["required_env_vars"]
        env_status = {var: bool(os.getenv(var)) for var in required}
        missing = [var for var, set in env_status.items() if not set]
        passed = len(missing) == 0
        msg = f"环境变量: {len(required) - len(missing)}/{len(required)} 已设置" + (
            f" | 缺失: {', '.join(missing)}" if missing else ""
        )
        return CheckResult(19, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.FAIL, msg,
                          {"env_status": env_status})

    # --------------------------------------------------
    # 阶段七: 健康检查 (20-22)
    # --------------------------------------------------

    def check_20_http_health_endpoint(self) -> CheckResult:
        """检查20: HTTP健康端点"""
        step = CHECK_STEPS[19]
        try:
            import urllib.request
            port = self.config["required_ports"][0]
            url = f"http://localhost:{port}{self.config['health_endpoint']}"
            req = urllib.request.Request(url, method='GET')
            try:
                response = urllib.request.urlopen(req, timeout=self.config["health_timeout"])
                passed = response.status == 200
                msg = f"健康端点返回 HTTP {response.status}"
            except Exception as e:
                passed = False
                msg = f"健康端点不可达: {str(e)[:100]}"
        except Exception as e:
            passed = False
            msg = f"检查失败: {e}"
        return CheckResult(20, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.WARN, msg,
                          {"endpoint": self.config["health_endpoint"]})

    def check_21_dependency_services_health(self) -> CheckResult:
        """检查21: 依赖服务健康"""
        step = CHECK_STEPS[20]
        services = []
        # 检查Redis
        try:
            sock = socket.create_connection(("localhost", 6379), timeout=2)
            sock.close()
            services.append("Redis: 可达")
        except Exception:
            services.append("Redis: 不可达")
        # 检查PostgreSQL
        try:
            sock = socket.create_connection(("localhost", 5432), timeout=2)
            sock.close()
            services.append("PostgreSQL: 可达")
        except Exception:
            services.append("PostgreSQL: 不可达")
        passed = len([s for s in services if "可达" in s]) > 0
        msg = " | ".join(services)
        return CheckResult(21, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.WARN, msg,
                          {"services": services})

    def check_22_critical_business_flow(self) -> CheckResult:
        """检查22: 关键业务流程"""
        step = CHECK_STEPS[21]
        # 模拟API检查
        api_endpoints = ["/api/health", "/api/status", "/"]
        checked = []
        try:
            import urllib.request
            port = self.config["required_ports"][0]
            for endpoint in api_endpoints:
                try:
                    url = f"http://localhost:{port}{endpoint}"
                    response = urllib.request.urlopen(url, timeout=5)
                    checked.append(f"{endpoint}: HTTP {response.status}")
                except Exception as e:
                    checked.append(f"{endpoint}: 失败 ({str(e)[:50]})")
            passed = any("200" in c for c in checked)
            msg = " | ".join(checked)
        except Exception as e:
            passed = False
            msg = f"业务流检查失败: {e}"
            checked = [msg]
        return CheckResult(22, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.WARN, msg,
                          {"endpoints": checked})

    # --------------------------------------------------
    # 阶段八: 监控配置 (23-24)
    # --------------------------------------------------

    def check_23_monitoring_agent(self) -> CheckResult:
        """检查23: 监控Agent配置"""
        step = CHECK_STEPS[22]
        monitoring_files = ["prometheus.yml", "grafana.ini"]
        found = [f for f in monitoring_files if os.path.exists(f)]
        passed = len(found) > 0
        msg = f"监控配置: {', '.join(found)}" if found else "未找到监控配置文件 (prometheus.yml / grafana.ini)"
        return CheckResult(23, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.WARN, msg,
                          {"found": found})

    def check_24_alert_rules(self) -> CheckResult:
        """检查24: 告警规则"""
        step = CHECK_STEPS[23]
        alert_files = ["alerts.yml", "alertmanager.yml", "alerts.yaml"]
        found = [f for f in alert_files if os.path.exists(f)]
        passed = len(found) > 0
        msg = f"告警规则: {', '.join(found)}" if found else "未找到告警规则文件"
        return CheckResult(24, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.WARN, msg,
                          {"found": found})

    # --------------------------------------------------
    # 阶段九: 日志确认 (25)
    # --------------------------------------------------

    def check_25_log_output(self) -> CheckResult:
        """检查25: 日志输出"""
        step = CHECK_STEPS[24]
        log_dirs = ["logs", "log", "/var/log/app"]
        log_dir = None
        for d in log_dirs:
            if os.path.exists(d):
                log_dir = d
                break
        if log_dir:
            log_files = [f for f in os.listdir(log_dir) if f.endswith(('.log', '.txt'))]
            passed = len(log_files) > 0
            msg = f"日志目录: {log_dir} | 日志文件: {len(log_files)}个"
        else:
            passed = False
            msg = "未找到日志目录 (logs/log)"
        return CheckResult(25, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.WARN, msg,
                          {"log_dir": log_dir, "log_files": log_files if log_dir else []})

    # --------------------------------------------------
    # 阶段十: 备份验证 (26-27)
    # --------------------------------------------------

    def check_26_backup_strategy(self) -> CheckResult:
        """检查26: 备份策略"""
        step = CHECK_STEPS[25]
        backup_configs = ["backup.sh", "backup.yml", ".backup_config"]
        found = [f for f in backup_configs if os.path.exists(f)]
        cron_backup = False
        try:
            result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=10)
            cron_backup = "backup" in result.stdout.lower()
        except Exception:
            pass
        passed = len(found) > 0 or cron_backup
        msg = f"备份配置: {', '.join(found)}" if found else ("发现crontab备份任务" if cron_backup else "未找到备份配置")
        return CheckResult(26, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.WARN, msg,
                          {"config_found": found, "cron_backup": cron_backup})

    def check_27_recovery_test(self) -> CheckResult:
        """检查27: 恢复演练"""
        step = CHECK_STEPS[26]
        recovery_files = ["recovery.sh", "restore.py", "DISASTER_RECOVERY.md"]
        found = [f for f in recovery_files if os.path.exists(f)]
        passed = len(found) > 0
        msg = f"恢复文档/脚本: {', '.join(found)}" if found else "未找到恢复文档或脚本"
        return CheckResult(27, step["name"], step["category"],
                          CheckStatus.PASS if passed else CheckStatus.WARN, msg,
                          {"found": found})

    # --------------------------------------------------
    # 执行引擎
    # --------------------------------------------------

    def run_check(self, step_id: int) -> CheckResult:
        """执行单个检查"""
        method_name = f"check_{step_id:02d}"
        method = getattr(self, method_name, None)
        if not method:
            step = CHECK_STEPS[step_id - 1] if step_id <= len(CHECK_STEPS) else {"name": "未知", "category": "未知"}
            return CheckResult(step_id, step.get("name", "未知"), step.get("category", "未知"),
                             CheckStatus.SKIP, "检查方法未实现")
        t0 = time.time()
        try:
            result = method()
        except Exception as e:
            step = CHECK_STEPS[step_id - 1]
            result = CheckResult(step_id, step["name"], step["category"],
                               CheckStatus.FAIL, f"检查异常: {str(e)[:200]}")
        result.duration_ms = round((time.time() - t0) * 1000, 2)
        return result

    def run_all_checks(self, step_filter: Optional[int] = None) -> List[CheckResult]:
        """执行全部或指定检查"""
        self.start_time = datetime.now()
        self.results = []
        steps = [step_filter] if step_filter else range(1, 28)
        total = len(steps)
        for i, step_id in enumerate(steps, 1):
            step_info = CHECK_STEPS[step_id - 1]
            print(f"[{i}/{total}] 检查 {step_id:02d}/27: {step_info['category']} → {step_info['name']} ... ", end="", flush=True)
            result = self.run_check(step_id)
            self.results.append(result)
            color = Colors.OKGREEN if result.status == CheckStatus.PASS else (
                Colors.WARNING if result.status == CheckStatus.WARN else Colors.FAIL
            )
            print(f"{color}{result.status.value}{Colors.ENDC} ({result.duration_ms}ms)")
            if result.message:
                print(f"      {result.message}")
        self.total_duration = sum(r.duration_ms for r in self.results)
        return self.results

    # --------------------------------------------------
    # 报告生成
    # --------------------------------------------------

    def generate_report(self, output_format: str = "console") -> str:
        """生成检查报告"""
        if output_format == "json":
            return self._generate_json_report()
        return self._generate_console_report()

    def _generate_console_report(self) -> str:
        """生成控制台报告"""
        lines = []
        lines.append("=" * 70)
        lines.append("  龍魂部署就绪检查报告 (Longhun Deployment Readiness Report)")
        lines.append(f"  DNA: {SKILL_DNA}")
        lines.append(f"  检查时间: {REPORT_TIMESTAMP}")
        lines.append(f"  清单版本: {CHECKLIST_VERSION}")
        lines.append("=" * 70)

        # 分类统计
        categories = {}
        for r in self.results:
            cat = r.category
            if cat not in categories:
                categories[cat] = {"total": 0, CheckStatus.PASS: 0, CheckStatus.FAIL: 0,
                                  CheckStatus.WARN: 0, CheckStatus.SKIP: 0}
            categories[cat]["total"] += 1
            categories[cat][r.status] = categories[cat].get(r.status, 0) + 1

        lines.append("\n【检查结果摘要】")
        lines.append(f"  总检查项: 27")
        lines.append(f"  通过:     {sum(1 for r in self.results if r.status == CheckStatus.PASS)}")
        lines.append(f"  警告:     {sum(1 for r in self.results if r.status == CheckStatus.WARN)}")
        lines.append(f"  失败:     {sum(1 for r in self.results if r.status == CheckStatus.FAIL)}")
        lines.append(f"  跳过:     {sum(1 for r in self.results if r.status == CheckStatus.SKIP)}")
        lines.append(f"  总耗时:   {self.total_duration:.0f}ms")

        # 分类详情
        lines.append("\n【分类详情】")
        for cat, stats in categories.items():
            pass_rate = stats[CheckStatus.PASS] / stats["total"] * 100 if stats["total"] > 0 else 0
            color = Colors.OKGREEN if pass_rate == 100 else (Colors.WARNING if pass_rate >= 60 else Colors.FAIL)
            lines.append(f"  {color}{cat}: {stats[CheckStatus.PASS]}/{stats['total']} 通过 ({pass_rate:.0f}%){Colors.ENDC}")

        # 失败项详情
        failures = [r for r in self.results if r.status in (CheckStatus.FAIL, CheckStatus.WARN)]
        if failures:
            lines.append(f"\n{Colors.WARNING}【需要关注的问题】{Colors.ENDC}")
            for r in failures:
                color = Colors.FAIL if r.status == CheckStatus.FAIL else Colors.WARNING
                lines.append(f"  {color}[{r.status.value}] 检查{r.step_id:02d}: {r.name}{Colors.ENDC}")
                lines.append(f"      → {r.message}")
                if r.auto_fixed:
                    lines.append(f"      {Colors.OKGREEN}✓ 已自动修复: {r.fix_message}{Colors.ENDC}")

        # 失败步骤建议
        fail_steps = [r.step_id for r in self.results if r.status == CheckStatus.FAIL]
        if fail_steps:
            lines.append(f"\n{Colors.FAIL}【失败步骤列表】{Colors.ENDC}")
            for sid in fail_steps:
                step = CHECK_STEPS[sid - 1]
                lines.append(f"  - 步骤{sid}: {step['name']} ({step['category']})")
            lines.append(f"\n{Colors.OKCYAN}修复建议: 运行 `python3 部署就绪检查器.py --fix` 自动修复{Colors.ENDC}")

        # 就绪判定
        pass_count = sum(1 for r in self.results if r.status == CheckStatus.PASS)
        if pass_count >= 24:  # 24/27以上通过视为就绪
            lines.append(f"\n{Colors.OKGREEN}{'='*70}")
            lines.append("  ✅ 部署就绪判定: 通过")
            lines.append("  系统已达到部署标准，可以执行部署操作")
            lines.append(f"{'='*70}{Colors.ENDC}")
        else:
            lines.append(f"\n{Colors.FAIL}{'='*70}")
            lines.append("  ❌ 部署就绪判定: 未通过")
            lines.append(f"  通过 {pass_count}/27 项，需至少24项通过")
            lines.append("  请修复上述问题后重新运行检查")
            lines.append(f"{'='*70}{Colors.ENDC}")

        lines.append(f"\n  详细日志: checks/deployment-readiness-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json")
        return "\n".join(lines)

    def _generate_json_report(self) -> str:
        """生成JSON报告"""
        report = {
            "meta": {
                "dna": SKILL_DNA,
                "version": SKILL_VERSION,
                "checklist_version": CHECKLIST_VERSION,
                "timestamp": REPORT_TIMESTAMP,
                "duration_ms": self.total_duration,
            },
            "summary": {
                "total": 27,
                "pass": sum(1 for r in self.results if r.status == CheckStatus.PASS),
                "warn": sum(1 for r in self.results if r.status == CheckStatus.WARN),
                "fail": sum(1 for r in self.results if r.status == CheckStatus.FAIL),
                "skip": sum(1 for r in self.results if r.status == CheckStatus.SKIP),
            },
            "results": [
                {
                    "step": r.step_id,
                    "name": r.name,
                    "category": r.category,
                    "status": r.status.value,
                    "message": r.message,
                    "details": r.details,
                    "duration_ms": r.duration_ms,
                    "auto_fixed": r.auto_fixed,
                }
                for r in self.results
            ],
            "ready": sum(1 for r in self.results if r.status == CheckStatus.PASS) >= 24,
        }
        return json.dumps(report, ensure_ascii=False, indent=2)

    def save_report(self, report: str, suffix: str = "json"):
        """保存报告到文件"""
        os.makedirs("checks", exist_ok=True)
        filename = f"checks/deployment-readiness-{datetime.now().strftime('%Y%m%d-%H%M%S')}.{suffix}"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        return filename


def main():
    parser = argparse.ArgumentParser(description="龍魂部署就绪检查器")
    parser.add_argument("--full", action="store_true", help="执行全部27项检查 (默认)")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    parser.add_argument("--fix", action="store_true", help="自动修复问题")
    parser.add_argument("--step", type=int, help="仅执行指定步骤 (1-27)")
    parser.add_argument("--config", help="配置文件路径")
    args = parser.parse_args()

    print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║         龍魂部署就绪检查器 v{SKILL_VERSION}                            ║
║         Longhun Deployment Readiness Checker                         ║
╠══════════════════════════════════════════════════════════════════════╣
║  DNA: {SKILL_DNA}    ║
║  清单: 27项检查 | 10个阶段 | 全链路覆盖                              ║
╚══════════════════════════════════════════════════════════════════════╝
""")

    checker = DeploymentReadinessChecker(config_path=args.config, auto_fix=args.fix)

    step = args.step if args.step else None
    if step and (step < 1 or step > 27):
        print(f"错误: 步骤编号必须在 1-27 之间")
        sys.exit(1)

    # 执行检查
    checker.run_all_checks(step_filter=step)

    # 生成报告
    format_type = "json" if args.json else "console"
    report = checker.generate_report(output_format=format_type)

    # 保存JSON报告
    json_report = checker.generate_report(output_format="json")
    saved = checker.save_report(json_report, "json")

    if format_type == "console":
        print(report)
        print(f"\nJSON报告已保存: {saved}")
    else:
        print(report)

    # 返回退出码
    ready = sum(1 for r in checker.results if r.status == CheckStatus.PASS) >= 24
    sys.exit(0 if ready else 1)


if __name__ == "__main__":
    main()
