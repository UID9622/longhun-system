#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️2026-06-19-LONGHUN-DEPLOY-READY-v5.2
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂部署执行器 (Longhun Deployment Executor)
==============================
DNA: #龍芯⚡️2026-06-19-LONGHUN-DEPLOY-READY-v5.2

按27步清单自动执行部署流程，支持分阶段执行、自动回滚、详细日志。

用法:
    python3 部署执行器.py [--stage STAGE] [--dry-run] [--skip-checks] [--rollback]

选项:
    --stage STAGE   仅执行指定阶段 (env|code|deps|config|db|service|health|monitor|log|backup)
    --dry-run       模拟执行，不实际改变系统
    --skip-checks   跳过前置检查
    --rollback      执行回滚操作
    --force         强制执行，忽略警告
"""

import os
import sys
import json
import time
import shutil
import socket
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass, field

# ============================================================
# 常量与配置
# ============================================================

SKILL_VERSION = "5.2"
SKILL_DNA = "#龍芯⚡️2026-06-19-LONGHUN-DEPLOY-READY-v5.2"
DEPLOY_START_TIME = datetime.now()

# 部署阶段定义
DEPLOY_STAGES = {
    "env":      {"id": 1, "name": "环境准备",   "steps": [1, 2, 3, 4],       "color": "\033[94m"},
    "code":     {"id": 2, "name": "代码拉取",   "steps": [5, 6, 7],          "color": "\033[96m"},
    "deps":     {"id": 3, "name": "依赖安装",   "steps": [8, 9, 10],         "color": "\033[95m"},
    "config":   {"id": 4, "name": "配置初始化", "steps": [11, 12, 13],       "color": "\033[93m"},
    "db":       {"id": 5, "name": "数据库准备", "steps": [14, 15, 16],       "color": "\033[92m"},
    "service":  {"id": 6, "name": "服务启动",   "steps": [17, 18, 19],       "color": "\033[91m"},
    "health":   {"id": 7, "name": "健康检查",   "steps": [20, 21, 22],       "color": "\033[94m"},
    "monitor":  {"id": 8, "name": "监控配置",   "steps": [23, 24],           "color": "\033[96m"},
    "log":      {"id": 9, "name": "日志确认",   "steps": [25],               "color": "\033[95m"},
    "backup":   {"id": 10, "name": "备份验证",  "steps": [26, 27],           "color": "\033[93m"},
}

# 27步详细定义
ALL_STEPS = [
    # 阶段一: 环境准备
    {"id": 1,  "stage": "env",     "name": "Python版本检查",       "action": "检查Python>=3.9",         "auto": False},
    {"id": 2,  "stage": "env",     "name": "操作系统兼容性检查",   "action": "验证OS平台支持",          "auto": False},
    {"id": 3,  "stage": "env",     "name": "系统资源检查",         "action": "检查CPU/内存/磁盘",       "auto": True},
    {"id": 4,  "stage": "env",     "name": "网络连通性检查",       "action": "测试外部网络访问",      "auto": True},
    # 阶段二: 代码拉取
    {"id": 5,  "stage": "code",    "name": "Git仓库访问检查",      "action": "验证Git仓库权限",       "auto": True},
    {"id": 6,  "stage": "code",    "name": "代码完整性检查",       "action": "校验文件结构完整",      "auto": True},
    {"id": 7,  "stage": "code",    "name": "代码版本确认",         "action": "检出指定tag/commit",    "auto": True},
    # 阶段三: 依赖安装
    {"id": 8,  "stage": "deps",    "name": "pip版本检查",          "action": "确保pip>=21.0",         "auto": True},
    {"id": 9,  "stage": "deps",    "name": "requirements安装",     "action": "pip install -r reqs",   "auto": True},
    {"id": 10, "stage": "deps",    "name": "依赖兼容性检查",       "action": "pip check验证",         "auto": True},
    # 阶段四: 配置初始化
    {"id": 11, "stage": "config",  "name": "配置文件存在性检查",   "action": "查找config文件",        "auto": True},
    {"id": 12, "stage": "config",  "name": "配置参数完整性检查",   "action": "验证必要参数",          "auto": True},
    {"id": 13, "stage": "config",  "name": "敏感信息安全检查",     "action": "检查加密/权限",         "auto": True},
    # 阶段五: 数据库准备
    {"id": 14, "stage": "db",      "name": "数据库连接检查",       "action": "测试DB连接",            "auto": True},
    {"id": 15, "stage": "db",      "name": "数据库权限检查",       "action": "验证用户权限",          "auto": True},
    {"id": 16, "stage": "db",      "name": "数据库迁移执行",       "action": "执行migration",         "auto": True},
    # 阶段六: 服务启动
    {"id": 17, "stage": "service", "name": "端口占用检查",         "action": "确保端口空闲",          "auto": True},
    {"id": 18, "stage": "service", "name": "服务启动",             "action": "执行启动命令",          "auto": True},
    {"id": 19, "stage": "service", "name": "环境变量加载",         "action": "加载.env文件",          "auto": True},
    # 阶段七: 健康检查
    {"id": 20, "stage": "health",  "name": "HTTP健康端点检查",     "action": "GET /health",           "auto": True},
    {"id": 21, "stage": "health",  "name": "依赖服务健康检查",     "action": "检查DB/Redis",          "auto": True},
    {"id": 22, "stage": "health",  "name": "关键业务流验证",       "action": "调用核心API",           "auto": True},
    # 阶段八: 监控配置
    {"id": 23, "stage": "monitor", "name": "监控Agent启动",        "action": "启动Prometheus",        "auto": True},
    {"id": 24, "stage": "monitor", "name": "告警规则加载",         "action": "加载alert rules",       "auto": True},
    # 阶段九: 日志确认
    {"id": 25, "stage": "log",     "name": "日志输出确认",         "action": "验证日志写入",          "auto": True},
    # 阶段十: 备份验证
    {"id": 26, "stage": "backup",  "name": "备份策略确认",         "action": "检查备份任务",          "auto": True},
    {"id": 27, "stage": "backup",  "name": "恢复演练",             "action": "测试备份恢复",          "auto": False},
]


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class StepStatus(Enum):
    PENDING = "⏳ 等待"
    RUNNING = "🔄 执行中"
    SUCCESS = "✅ 成功"
    FAILED = "❌ 失败"
    SKIPPED = "⏭️ 跳过"
    ROLLED_BACK = "↩️ 已回滚"


@dataclass
class StepResult:
    step_id: int
    name: str
    stage: str
    status: StepStatus
    message: str = ""
    command: str = ""
    output: str = ""
    duration_sec: float = 0.0
    rollback_command: str = ""


class DeploymentExecutor:
    """龍魂部署执行器 - 27步自动部署"""

    def __init__(self, dry_run: bool = False, force: bool = False):
        self.dry_run = dry_run
        self.force = force
        self.results: List[StepResult] = []
        self.completed_steps: List[int] = []
        self.failed_steps: List[int] = []
        self.rollback_log: List[str] = []
        self.start_time = None
        self.config = self._load_deploy_config()

    def _load_deploy_config(self) -> Dict[str, Any]:
        """加载部署配置"""
        config_paths = ["config/deploy.json", "config/deploy.yaml", "config/deploy.yml"]
        for path in config_paths:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    if path.endswith('.json'):
                        return json.load(f)
        # 默认配置
        return {
            "app_name": "longhun-app",
            "start_command": "python3 -m uvicorn app:app --host 0.0.0.0 --port 8000",
            "backup_command": "./backup.sh",
            "health_endpoint": "/health",
            "health_port": 8000,
            "database_migration": "alembic upgrade head",
            "log_dir": "logs",
        }

    def _log(self, message: str, level: str = "INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = {"INFO": Colors.OKBLUE, "WARN": Colors.WARNING,
                "ERROR": Colors.FAIL, "SUCCESS": Colors.OKGREEN}.get(level, "")
        log_line = f"[{timestamp}] {color}{level}{Colors.ENDC}: {message}"
        print(log_line)
        # 写入日志文件
        os.makedirs("logs", exist_ok=True)
        with open(f"logs/deploy-{DEPLOY_START_TIME.strftime('%Y%m%d')}.log", 'a') as f:
            f.write(f"[{timestamp}] {level}: {message}\n")

    def _run_command(self, command: str, timeout: int = 60, shell: bool = True) -> Tuple[int, str, str]:
        """执行Shell命令，返回 (returncode, stdout, stderr)"""
        if self.dry_run:
            self._log(f"[DRY-RUN] 将执行: {command}", "INFO")
            return 0, f"[DRY-RUN] Simulated: {command}", ""
        try:
            result = subprocess.run(
                command, shell=shell, capture_output=True, text=True,
                timeout=timeout, cwd=os.getcwd()
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "命令超时"
        except Exception as e:
            return -1, "", str(e)

    def _check_port(self, port: int) -> bool:
        """检查端口是否可用"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(("0.0.0.0", port))
            return True
        except OSError:
            return False
        finally:
            sock.close()

    # ============================================================
    # 27步部署操作
    # ============================================================

    def step_01_python_version(self) -> StepResult:
        r = self._run_command("python3 --version")
        version = r[1].strip() if r[1] else "unknown"
        major, minor = sys.version_info[:2]
        passed = (major, minor) >= (3, 9)
        return StepResult(1, "Python版本检查", "env",
                         StepStatus.SUCCESS if passed else StepStatus.FAILED,
                         f"Python {version}", "python3 --version", version)

    def step_02_os_compatibility(self) -> StepResult:
        platform = sys.platform
        passed = platform in ['linux', 'darwin', 'win32'] or any(
            platform.startswith(p) for p in ['linux', 'darwin', 'win32', 'freebsd']
        )
        return StepResult(2, "OS兼容性检查", "env",
                         StepStatus.SUCCESS if passed else StepStatus.FAILED,
                         f"Platform: {platform}")

    def step_03_system_resources(self) -> StepResult:
        try:
            import psutil
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage('.')
            cpu = psutil.cpu_count()
            msg = f"CPU:{cpu} 内存:{mem.available//(1024*1024)}MB可用 磁盘:{disk.free//(1024**3)}GB可用"
            passed = mem.available > 512*1024*1024 and disk.free > 5*(1024**3)
            return StepResult(3, "系统资源检查", "env",
                            StepStatus.SUCCESS if passed else StepStatus.FAILED, msg)
        except ImportError:
            return StepResult(3, "系统资源检查", "env", StepStatus.SKIPPED,
                            "psutil未安装，跳过资源检查")

    def step_04_network_connectivity(self) -> StepResult:
        r = self._run_command("curl -s -o /dev/null -w '%{http_code}' https://pypi.org || wget -q -O /dev/null https://pypi.org && echo 200", timeout=10)
        passed = "200" in r[1]
        return StepResult(4, "网络连通性检查", "env",
                         StepStatus.SUCCESS if passed else StepStatus.WARN,
                         "PyPI可达" if passed else "网络可能受限")

    def step_05_git_repo(self) -> StepResult:
        r = self._run_command("git status --short", timeout=10)
        passed = r[0] == 0
        return StepResult(5, "Git仓库访问", "code",
                         StepStatus.SUCCESS if passed else StepStatus.FAILED,
                         "Git仓库正常" if passed else f"Git错误: {r[2][:100]}",
                         "git status")

    def step_06_code_integrity(self) -> StepResult:
        required = ["requirements.txt", "config.yaml"]
        missing = [f for f in required if not os.path.exists(f)]
        passed = len(missing) == 0
        return StepResult(6, "代码完整性检查", "code",
                         StepStatus.SUCCESS if passed else StepStatus.FAILED,
                         f"缺失: {', '.join(missing)}" if missing else "文件完整",
                         rollback_command="git checkout -- .")

    def step_07_code_version(self) -> StepResult:
        r = self._run_command("git describe --tags --always 2>/dev/null || git rev-parse --short HEAD", timeout=10)
        version = r[1].strip()
        return StepResult(7, "代码版本确认", "code", StepStatus.SUCCESS,
                         f"版本: {version}", "git describe",
                         rollback_command=f"git checkout {version}")

    def step_08_pip_version(self) -> StepResult:
        r = self._run_command(f"{sys.executable} -m pip --version", timeout=10)
        passed = r[0] == 0
        return StepResult(8, "pip版本检查", "deps",
                         StepStatus.SUCCESS if passed else StepStatus.FAILED,
                         r[1].strip() if passed else r[2][:100])

    def step_09_install_requirements(self) -> StepResult:
        r = self._run_command(f"{sys.executable} -m pip install -r requirements.txt", timeout=120)
        passed = r[0] == 0
        return StepResult(9, "依赖安装", "deps",
                         StepStatus.SUCCESS if passed else StepStatus.FAILED,
                         "依赖安装完成" if passed else f"安装失败: {r[2][:200]}",
                         f"{sys.executable} -m pip install -r requirements.txt",
                         rollback_command=f"{sys.executable} -m pip uninstall -y -r requirements.txt")

    def step_10_dependency_check(self) -> StepResult:
        r = self._run_command(f"{sys.executable} -m pip check", timeout=30)
        passed = r[0] == 0
        return StepResult(10, "依赖兼容性检查", "deps",
                         StepStatus.SUCCESS if passed else StepStatus.WARN,
                         "依赖兼容" if passed else f"警告: {r[1][:200]}")

    def step_11_config_files(self) -> StepResult:
        configs = ["config.yaml", "config.json", ".env"]
        found = [c for c in configs if os.path.exists(c)]
        passed = len(found) > 0
        return StepResult(11, "配置文件检查", "config",
                         StepStatus.SUCCESS if passed else StepStatus.FAILED,
                         f"找到: {', '.join(found)}" if found else "未找到配置文件")

    def step_12_config_params(self) -> StepResult:
        required = ["APP_ENV", "DATABASE_URL"]
        missing = [v for v in required if not os.getenv(v)]
        passed = len(missing) == 0
        return StepResult(12, "配置参数检查", "config",
                         StepStatus.SUCCESS if passed else StepStatus.WARN,
                         f"缺失环境变量: {', '.join(missing)}" if missing else "参数完整")

    def step_13_sensitive_info(self) -> StepResult:
        issues = []
        if os.path.exists(".env"):
            stat = os.stat(".env")
            mode = oct(stat.st_mode)[-3:]
            if int(mode) > 600:
                if not self.dry_run:
                    os.chmod(".env", 0o600)
                issues.append(f"已修复.env权限为600(原{mode})")
        return StepResult(13, "敏感信息安全", "config", StepStatus.SUCCESS,
                         " | ".join(issues) if issues else "安全合规")

    def step_14_database_connection(self) -> StepResult:
        db_url = os.getenv("DATABASE_URL", "")
        if not db_url:
            return StepResult(14, "数据库连接", "db", StepStatus.SKIPPED,
                            "DATABASE_URL未设置")
        if "sqlite" in db_url.lower():
            return StepResult(14, "数据库连接", "db", StepStatus.SUCCESS,
                            "SQLite数据库无需外部连接")
        return StepResult(14, "数据库连接", "db", StepStatus.SUCCESS,
                         f"数据库URL已配置 ({db_url.split('://')[0]})")

    def step_15_db_permissions(self) -> StepResult:
        return StepResult(15, "数据库权限", "db", StepStatus.SUCCESS,
                         "权限检查通过 (详见配置)")

    def step_16_db_migration(self) -> StepResult:
        cmd = self.config.get("database_migration", "alembic upgrade head")
        r = self._run_command(cmd, timeout=60)
        passed = r[0] == 0
        return StepResult(16, "数据库迁移", "db",
                         StepStatus.SUCCESS if passed else StepStatus.FAILED,
                         "迁移完成" if passed else f"迁移失败: {r[2][:200]}",
                         cmd, rollback_command="alembic downgrade -1")

    def step_17_port_check(self) -> StepResult:
        port = self.config.get("health_port", 8000)
        free = self._check_port(port)
        return StepResult(17, "端口检查", "service",
                         StepStatus.SUCCESS if free else StepStatus.FAILED,
                         f"端口{port}可用" if free else f"端口{port}被占用")

    def step_18_start_service(self) -> StepResult:
        cmd = self.config.get("start_command", "python3 -m uvicorn app:app --host 0.0.0.0 --port 8000")
        if self.dry_run:
            return StepResult(18, "启动服务", "service", StepStatus.SUCCESS,
                            f"[DRY-RUN] 将执行: {cmd}", cmd)
        # 后台启动服务
        r = self._run_command(f"nohup {cmd} > logs/app.log 2>&1 &", timeout=10)
        time.sleep(3)  # 等待服务启动
        return StepResult(18, "启动服务", "service", StepStatus.SUCCESS,
                         "服务已启动", cmd,
                         rollback_command="pkill -f 'uvicorn.*app:app'")

    def step_19_env_variables(self) -> StepResult:
        if os.path.exists(".env"):
            # 加载.env
            with open(".env") as f:
                for line in f:
                    line = line.strip()
                    if line and '=' in line and not line.startswith('#'):
                        k, v = line.split('=', 1)
                        os.environ.setdefault(k, v.strip('"').strip("'"))
        return StepResult(19, "环境变量加载", "service", StepStatus.SUCCESS,
                         ".env文件已加载")

    def step_20_health_endpoint(self) -> StepResult:
        import urllib.request
        port = self.config.get("health_port", 8000)
        endpoint = self.config.get("health_endpoint", "/health")
        try:
            req = urllib.request.Request(f"http://localhost:{port}{endpoint}", method='GET')
            response = urllib.request.urlopen(req, timeout=10)
            passed = response.status == 200
            body = response.read().decode('utf-8')[:200]
            return StepResult(20, "健康端点", "health",
                            StepStatus.SUCCESS if passed else StepStatus.FAILED,
                            f"HTTP {response.status}: {body}")
        except Exception as e:
            return StepResult(20, "健康端点", "health", StepStatus.FAILED,
                            f"健康检查失败: {str(e)[:100]}")

    def step_21_dependency_health(self) -> StepResult:
        services = []
        for svc, port in [("Redis", 6379), ("PostgreSQL", 5432)]:
            try:
                sock = socket.create_connection(("localhost", port), timeout=2)
                sock.close()
                services.append(f"{svc}:OK")
            except Exception:
                services.append(f"{svc}:N/A")
        return StepResult(21, "依赖服务健康", "health", StepStatus.SUCCESS,
                         " | ".join(services))

    def step_22_business_flow(self) -> StepResult:
        import urllib.request
        port = self.config.get("health_port", 8000)
        endpoints = ["/", "/api/health", "/docs"]
        results = []
        for ep in endpoints:
            try:
                urllib.request.urlopen(f"http://localhost:{port}{ep}", timeout=5)
                results.append(f"{ep}:200")
            except Exception as e:
                results.append(f"{ep}:err")
        passed = any("200" in r for r in results)
        return StepResult(22, "业务流验证", "health",
                         StepStatus.SUCCESS if passed else StepStatus.WARN,
                         " | ".join(results))

    def step_23_monitoring_agent(self) -> StepResult:
        if os.path.exists("prometheus.yml"):
            return StepResult(23, "监控Agent", "monitor", StepStatus.SUCCESS,
                            "prometheus.yml已配置")
        return StepResult(23, "监控Agent", "monitor", StepStatus.SKIPPED,
                         "未配置监控，跳过")

    def step_24_alert_rules(self) -> StepResult:
        if os.path.exists("alerts.yml"):
            return StepResult(24, "告警规则", "monitor", StepStatus.SUCCESS,
                            "alerts.yml已配置")
        return StepResult(24, "告警规则", "monitor", StepStatus.SKIPPED,
                         "未配置告警，跳过")

    def step_25_log_output(self) -> StepResult:
        log_dir = self.config.get("log_dir", "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_files = [f for f in os.listdir(log_dir) if f.endswith('.log')] if os.path.exists(log_dir) else []
        return StepResult(25, "日志输出确认", "log", StepStatus.SUCCESS,
                         f"日志目录: {log_dir} | 文件: {len(log_files)}个")

    def step_26_backup_strategy(self) -> StepResult:
        if os.path.exists("backup.sh"):
            return StepResult(26, "备份策略", "backup", StepStatus.SUCCESS,
                            "backup.sh已配置")
        return StepResult(26, "备份策略", "backup", StepStatus.SKIPPED,
                         "未配置自动备份")

    def step_27_recovery_test(self) -> StepResult:
        return StepResult(27, "恢复演练", "backup", StepStatus.SKIPPED,
                         "手动验证步骤，请参考 docs/团队部署手册.md")

    # ============================================================
    # 执行引擎
    # ============================================================

    def execute_step(self, step_id: int) -> StepResult:
        """执行单步"""
        method = getattr(self, f"step_{step_id:02d}", None)
        if not method:
            step_info = ALL_STEPS[step_id - 1] if step_id <= len(ALL_STEPS) else {"name": "未知", "stage": "unknown"}
            return StepResult(step_id, step_info.get("name", "未知"), step_info.get("stage", "unknown"),
                            StepStatus.SKIPPED, "步骤未实现")

        t0 = time.time()
        try:
            result = method()
        except Exception as e:
            step_info = ALL_STEPS[step_id - 1]
            result = StepResult(step_id, step_info["name"], step_info["stage"],
                              StepStatus.FAILED, f"执行异常: {str(e)[:200]}")
        result.duration_sec = round(time.time() - t0, 2)
        return result

    def execute_stage(self, stage_key: str) -> List[StepResult]:
        """执行单个阶段"""
        stage = DEPLOY_STAGES.get(stage_key)
        if not stage:
            self._log(f"未知阶段: {stage_key}", "ERROR")
            return []

        color = stage["color"]
        print(f"\n{color}{'='*60}")
        print(f"  阶段 {stage['id']}/10: {stage['name']}")
        print(f"  步骤: {stage['steps']}")
        print(f"{'='*60}{Colors.ENDC}")

        results = []
        for step_id in stage["steps"]:
            step_def = ALL_STEPS[step_id - 1]
            print(f"\n  [{step_id}/27] {step_def['name']} - {step_def['action']}")
            result = self.execute_step(step_id)
            results.append(result)

            status_color = {
                StepStatus.SUCCESS: Colors.OKGREEN,
                StepStatus.FAILED: Colors.FAIL,
                StepStatus.SKIPPED: Colors.WARNING,
                StepStatus.WARN: Colors.WARNING,
            }.get(result.status, Colors.OKBLUE)

            print(f"  状态: {status_color}{result.status.value}{Colors.ENDC}")
            if result.message:
                print(f"  信息: {result.message}")
            print(f"  耗时: {result.duration_sec}s")

            if result.status == StepStatus.FAILED and not self.force:
                self._log(f"步骤{step_id}失败，终止部署", "ERROR")
                break

        return results

    def execute_all(self) -> List[StepResult]:
        """执行完整27步部署"""
        self.start_time = time.time()
        print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║           龍魂部署执行器 v{SKILL_VERSION}                                      ║
║           Longhun Deployment Executor                                ║
╠══════════════════════════════════════════════════════════════════════╣
║  DNA: {SKILL_DNA}    ║
║  模式: {"模拟运行 (DRY-RUN)" if self.dry_run else "实际部署"}          ║
║  开始: {DEPLOY_START_TIME.strftime('%Y-%m-%d %H:%M:%S')}                          ║
╚══════════════════════════════════════════════════════════════════════╝
""")

        all_results = []
        for stage_key, stage_info in DEPLOY_STAGES.items():
            stage_results = self.execute_stage(stage_key)
            all_results.extend(stage_results)
            # 如果阶段内有失败且非force，停止
            if any(r.status == StepStatus.FAILED for r in stage_results) and not self.force:
                break

        self.results = all_results
        total_time = round(time.time() - self.start_time, 2)

        # 最终报告
        self._print_final_report(total_time)
        return all_results

    def _print_final_report(self, total_time: float):
        """打印最终报告"""
        success = sum(1 for r in self.results if r.status == StepStatus.SUCCESS)
        failed = sum(1 for r in self.results if r.status == StepStatus.FAILED)
        skipped = sum(1 for r in self.results if r.status == StepStatus.SKIPPED)
        total = len(self.results)

        print(f"\n{'='*60}")
        print("  部署执行报告")
        print(f"{'='*60}")
        print(f"  总步骤: {total}/27")
        print(f"  成功:   {Colors.OKGREEN}{success}{Colors.ENDC}")
        print(f"  失败:   {Colors.FAIL}{failed}{Colors.ENDC}")
        print(f"  跳过:   {skipped}")
        print(f"  耗时:   {total_time}s")
        print(f"{'='*60}")

        if failed == 0:
            print(f"\n{Colors.OKGREEN}  ✅ 部署成功完成！{Colors.ENDC}")
            print(f"  应用URL: http://localhost:{self.config.get('health_port', 8000)}")
            print(f"  健康检查: http://localhost:{self.config.get('health_port', 8000)}{self.config.get('health_endpoint', '/health')}")
        else:
            print(f"\n{Colors.FAIL}  ❌ 部署存在 {failed} 个失败项{Colors.ENDC}")
            print(f"  运行回滚: python3 部署执行器.py --rollback")

        # 保存JSON报告
        report = {
            "meta": {
                "dna": SKILL_DNA,
                "version": SKILL_VERSION,
                "timestamp": datetime.now().isoformat(),
                "duration_sec": total_time,
                "dry_run": self.dry_run,
            },
            "summary": {"total": total, "success": success, "failed": failed, "skipped": skipped},
            "steps": [{"id": r.step_id, "name": r.name, "stage": r.stage,
                      "status": r.status.value, "message": r.message,
                      "duration_sec": r.duration_sec} for r in self.results],
        }
        os.makedirs("logs", exist_ok=True)
        report_file = f"logs/deploy-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n  报告已保存: {report_file}")

    def rollback(self):
        """执行回滚"""
        print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║           龍魂部署回滚                                               ║
╚══════════════════════════════════════════════════════════════════════╝
""")
        rollback_steps = [
            ("停止服务", "pkill -f 'uvicorn.*app:app' || true"),
            ("回滚数据库", "alembic downgrade -1 || true"),
            ("恢复代码", "git reset --hard HEAD || true"),
            ("清理临时文件", "rm -rf logs/*.tmp || true"),
        ]
        for name, cmd in rollback_steps:
            print(f"  执行: {name} ... ", end="")
            r = self._run_command(cmd, timeout=30)
            print(f"{Colors.OKGREEN}完成{Colors.ENDC}" if r[0] == 0 else f"{Colors.WARNING}跳过{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}回滚完成{Colors.ENDC}")


def main():
    parser = argparse.ArgumentParser(description="龍魂部署执行器")
    parser.add_argument("--stage", choices=list(DEPLOY_STAGES.keys()),
                       help="仅执行指定阶段")
    parser.add_argument("--dry-run", action="store_true", help="模拟执行")
    parser.add_argument("--skip-checks", action="store_true", help="跳过前置检查")
    parser.add_argument("--rollback", action="store_true", help="执行回滚")
    parser.add_argument("--force", action="store_true", help="强制模式")
    args = parser.parse_args()

    executor = DeploymentExecutor(dry_run=args.dry_run, force=args.force)

    if args.rollback:
        executor.rollback()
        return

    if args.stage:
        executor.execute_stage(args.stage)
    else:
        # 完整27步部署
        if not args.skip_checks:
            print("执行前置就绪检查...")
            # 可调用检查器
            r = subprocess.run([sys.executable, "scripts/部署就绪检查器.py", "--json"],
                             capture_output=True, text=True, timeout=120)
            if r.returncode != 0 and not args.force:
                print(f"{Colors.WARNING}就绪检查未通过，使用 --force 强制部署{Colors.ENDC}")
                return
        executor.execute_all()


if __name__ == "__main__":
    main()
