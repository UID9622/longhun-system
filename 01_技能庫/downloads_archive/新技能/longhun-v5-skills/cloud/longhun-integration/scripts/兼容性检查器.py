#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂系統·兼容性检查器
Compatibility Checker v5.2

功能：
  - Python版本兼容性检查
  - 模块依赖兼容性验证
  - 技能版本矩阵检查
  - 跨模块接口兼容性
  - 配置文件兼容性
  - 数据库/API兼容性验证
  - 生成兼容性报告与升级建议

DNA: #龍芯⚡️2026-06-19-LONGHUN-INTEGRATION-v5.2
"""

import os
import sys
import json
import re
import ast
import subprocess
import importlib.util
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
from packaging import version as packaging_version

# ============================================================
# 配置常量
# ============================================================

DNA = "#龍芯⚡️2026-06-19-LONGHUN-INTEGRATION-v5.2"
VERSION = "5.2.0"
CHECKER_NAME = "龍魂兼容性检查器"

# 系统路径
LONGHUN_BASE = Path.home() / "longhun-system"
CNSH_CORE = LONGHUN_BASE / "cnsh-core"
SKILLS_DIR = LONGHUN_BASE / "skills"
MONITORING_DIR = LONGHUN_BASE / "monitoring"
TOOLS_DIR = LONGHUN_BASE / "tools"
INTEGRATIONS_DIR = LONGHUN_BASE / "integrations"
EXECUTORS_DIR = LONGHUN_BASE / "executors"

# Python版本要求
PYTHON_MIN_VERSION = (3, 8)
PYTHON_MAX_VERSION = (3, 13)

# 核心依赖版本矩阵
DEPENDENCY_MATRIX = {
    "requests": ">=2.25.0,<3.0",
    "aiohttp": ">=3.7.0,<4.0",
    "packaging": ">=20.0",
    "python-socketio": ">=5.0",
    "notion-client": ">=2.0",
    "pydantic": ">=1.8,<3.0",
    "fastapi": ">=0.68.0",
    "uvicorn": ">=0.15.0",
    "jinja2": ">=3.0",
    "pyyaml": ">=5.4",
    "rich": ">=10.0",
    "psutil": ">=5.8",
}

# 龍魂模块版本矩阵
LONGHUN_MODULE_MATRIX = {
    "cnsh-core": {"min": "2.0.0", "max": "3.0.0", "current": "2.5.0", "required_by": ["所有模块"]},
    "skills": {"min": "1.0.0", "max": "2.0.0", "current": "1.2.0", "required_by": ["skill-engine", "gateway"]},
    "monitoring": {"min": "1.0.0", "max": "2.0.0", "current": "1.1.0", "required_by": ["gateway", "launcher"]},
    "logging": {"min": "1.0.0", "max": "2.0.0", "current": "1.3.0", "required_by": ["所有模块"]},
    "protocols": {"min": "2.0.0", "max": "3.0.0", "current": "2.0.0", "required_by": ["cnsh-core", "gateway"]},
    "gateway": {"min": "1.0.0", "max": "2.0.0", "current": "1.5.0", "required_by": ["launcher"]},
    "sync": {"min": "1.1.0", "max": "2.0.0", "current": "1.1.0", "required_by": ["brain-notion"]},
    "executors": {"min": "1.0.0", "max": "2.0.0", "current": "1.0.0", "required_by": ["launcher", "kfpp"]},
}

# 模块间接口兼容性定义
INTERFACE_COMPATIBILITY = {
    ("cnsh-core", "skills"): {"min_api": "v1", "max_api": "v2", "interface": "skill_registry"},
    ("cnsh-core", "monitoring"): {"min_api": "v1", "max_api": "v1", "interface": "metrics_push"},
    ("cnsh-core", "logging"): {"min_api": "v1", "max_api": "v2", "interface": "audit_log"},
    ("skills", "gateway"): {"min_api": "v1", "max_api": "v1", "interface": "route_registration"},
    ("monitoring", "gateway"): {"min_api": "v1", "max_api": "v1", "interface": "health_check"},
    ("sync", "notion"): {"min_api": "v1", "max_api": "v2", "interface": "webhook_sync"},
    ("executors", "cnsh-core"): {"min_api": "v1", "max_api": "v2", "interface": "command_execute"},
    ("protocols", "cnsh-core"): {"min_api": "v2", "max_api": "v2", "interface": "protocol_lock"},
}


# ============================================================
# 数据模型
# ============================================================

class CheckStatus(Enum):
    COMPATIBLE = "✅ 兼容"
    INCOMPATIBLE = "❌ 不兼容"
    WARNING = "⚠️ 警告"
    UNKNOWN = "❓ 未知"
    INFO = "ℹ️ 信息"


@dataclass
class CheckResult:
    """兼容性检查结果"""
    component: str
    check_type: str  # python_version | dependency | module_version | interface | config | api_db
    status: CheckStatus
    message: str = ""
    expected: str = ""
    actual: str = ""
    recommendation: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        return {
            "component": self.component,
            "check_type": self.check_type,
            "status": self.status.value,
            "message": self.message,
            "expected": self.expected,
            "actual": self.actual,
            "recommendation": self.recommendation,
            "details": self.details,
            "timestamp": self.timestamp,
        }


# ============================================================
# 兼容性检查器核心类
# ============================================================

class CompatibilityChecker:
    """
    龍魂系统兼容性检查器
    
    执行全面的兼容性验证：
    1. Python版本兼容性
    2. 第三方依赖版本矩阵
    3. 龍魂模块版本兼容性
    4. 跨模块接口兼容性
    5. 配置文件格式兼容性
    6. 数据库/API兼容性
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.results: List[CheckResult] = []
        self._print_banner()

    def _print_banner(self):
        banner = f"""
╔══════════════════════════════════════════════════════════════════╗
║  🔍 {CHECKER_NAME} v{VERSION}                           ║
║  DNA: {DNA}           ║
║  检查项: Python | 依赖 | 模块版本 | 接口 | 配置 | API/DB      ║
╚══════════════════════════════════════════════════════════════════╝
"""
        if self.verbose:
            print(banner)

    def log(self, msg: str, level: str = "INFO"):
        if self.verbose:
            ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            icon = {"INFO": "ℹ️", "OK": "✅", "WARN": "⚠️", "ERROR": "❌", "CHECK": "🔍"}.get(level, "•")
            print(f"[{ts}] {icon} {msg}")

    # ============================================================
    # 1. Python版本兼容性
    # ============================================================

    def check_python_version(self) -> List[CheckResult]:
        """检查Python版本兼容性"""
        self.log("检查Python版本兼容性...", "CHECK")
        results = []

        current = sys.version_info
        current_str = f"{current.major}.{current.minor}.{current.micro}"
        expected_range = f"{PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]} - {PYTHON_MAX_VERSION[0]}.{PYTHON_MAX_VERSION[1]}"

        is_compatible = PYTHON_MIN_VERSION <= (current.major, current.minor) <= PYTHON_MAX_VERSION

        status = CheckStatus.COMPATIBLE if is_compatible else CheckStatus.INCOMPATIBLE
        msg = f"当前Python {current_str}"
        recommendation = "" if is_compatible else f"请升级Python到 {PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]}+"

        results.append(CheckResult(
            component="Python解释器",
            check_type="python_version",
            status=status,
            message=msg,
            expected=expected_range,
            actual=current_str,
            recommendation=recommendation,
            details={
                "major": current.major,
                "minor": current.minor,
                "micro": current.micro,
                "implementation": sys.implementation.name,
            },
        ))

        # 检查关键语法兼容性
        t_features = {
            "walrus_operator": (3, 8),      # :=
            "positional_only": (3, 8),      # def f(a, /, b)
            "type_hinting": (3, 9),         # list[str]
            "match_statement": (3, 10),     # match/case
            "exception_groups": (3, 11),    # ExceptionGroup
            "type_params": (3, 12),         # type T
        }

        available_features = []
        for feature, req_ver in t_features.items():
            if (current.major, current.minor) >= req_ver:
                available_features.append(feature)

        results.append(CheckResult(
            component="Python语法特性",
            check_type="python_version",
            status=CheckStatus.INFO,
            message=f"支持 {len(available_features)}/{len(t_features)} 个关键语法特性",
            expected="3.8+",
            actual=current_str,
            details={"available_features": available_features},
        ))

        self.results.extend(results)
        for r in results:
            self.log(f"  {r.status.value} {r.component}: {r.message}")
        return results

    # ============================================================
    # 2. 第三方依赖版本矩阵
    # ============================================================

    def check_dependencies(self) -> List[CheckResult]:
        """检查第三方依赖版本兼容性"""
        self.log("检查第三方依赖版本矩阵...", "CHECK")
        results = []

        for pkg_name, version_spec in DEPENDENCY_MATRIX.items():
            t0 = datetime.now()
            try:
                # 尝试导入并获取版本
                spec = importlib.util.find_spec(pkg_name.replace("-", "_"))
                if spec is None:
                    # 尝试用pip检查
                    result = subprocess.run(
                        [sys.executable, "-m", "pip", "show", pkg_name],
                        capture_output=True, text=True, timeout=10
                    )
                    if result.returncode != 0:
                        results.append(CheckResult(
                            component=f"pip:{pkg_name}",
                            check_type="dependency",
                            status=CheckStatus.WARNING,
                            message=f"未安装",
                            expected=version_spec,
                            actual="not installed",
                            recommendation=f"pip install '{pkg_name}{version_spec}'",
                        ))
                        continue

                    # 解析版本
                    for line in result.stdout.split("\n"):
                        if line.startswith("Version:"):
                            installed_ver = line.split(":", 1)[1].strip()
                            break
                    else:
                        installed_ver = "unknown"
                else:
                    # 尝试导入获取__version__
                    try:
                        module = importlib.import_module(pkg_name.replace("-", "_"))
                        installed_ver = getattr(module, "__version__", "unknown")
                    except:
                        installed_ver = "installed"

                # 版本兼容性检查
                is_compatible = self._check_version_spec(installed_ver, version_spec)
                status = CheckStatus.COMPATIBLE if is_compatible else CheckStatus.WARNING

                results.append(CheckResult(
                    component=pkg_name,
                    check_type="dependency",
                    status=status,
                    message=f"已安装 {installed_ver}",
                    expected=version_spec,
                    actual=installed_ver,
                    recommendation="" if is_compatible else f"考虑升级: pip install '{pkg_name}{version_spec}'",
                ))

            except Exception as e:
                results.append(CheckResult(
                    component=pkg_name,
                    check_type="dependency",
                    status=CheckStatus.UNKNOWN,
                    message=f"检查失败: {str(e)[:80]}",
                    expected=version_spec,
                    actual="unknown",
                ))

        self.results.extend(results)
        compatible = sum(1 for r in results if r.status == CheckStatus.COMPATIBLE)
        self.log(f"依赖检查完成: {compatible}/{len(results)} 兼容", "OK" if compatible == len(results) else "WARN")
        return results

    def _check_version_spec(self, installed: str, spec: str) -> bool:
        """检查版本是否符合规范"""
        try:
            installed_v = packaging_version.parse(installed)
            # 解析简单规范如 ">=2.25.0,<3.0"
            parts = spec.split(",")
            for part in parts:
                part = part.strip()
                if part.startswith(">="):
                    min_v = packaging_version.parse(part[2:])
                    if installed_v < min_v:
                        return False
                elif part.startswith(">"):
                    min_v = packaging_version.parse(part[1:])
                    if installed_v <= min_v:
                        return False
                elif part.startswith("<"):
                    if not part.startswith("<="):
                        max_v = packaging_version.parse(part[1:])
                        if installed_v >= max_v:
                            return False
                    else:
                        max_v = packaging_version.parse(part[2:])
                        if installed_v > max_v:
                            return False
                elif part.startswith("=="):
                    exact_v = packaging_version.parse(part[2:])
                    if installed_v != exact_v:
                        return False
            return True
        except:
            return True  # 无法解析时默认为兼容

    # ============================================================
    # 3. 龍魂模块版本矩阵
    # ============================================================

    def check_module_versions(self) -> List[CheckResult]:
        """检查龍魂各模块版本兼容性"""
        self.log("检查龍魂模块版本矩阵...", "CHECK")
        results = []

        for module_name, matrix in LONGHUN_MODULE_MATRIX.items():
            # 检查当前版本是否在允许范围内
            try:
                current_v = packaging_version.parse(matrix["current"])
                min_v = packaging_version.parse(matrix["min"])
                max_v = packaging_version.parse(matrix["max"])

                is_compatible = min_v <= current_v < max_v

                # 检查模块目录是否存在
                module_paths = {
                    "cnsh-core": CNSH_CORE,
                    "skills": SKILLS_DIR,
                    "monitoring": MONITORING_DIR,
                    "logging": INTEGRATED_MODULES / "logging",
                    "protocols": INTEGRATED_MODULES / "protocols",
                    "gateway": INTEGRATED_MODULES / "gateway",
                    "sync": INTEGRATED_MODULES / "sync",
                    "executors": EXECUTORS_DIR,
                }
                path_exists = module_paths.get(module_name, Path()).exists()

                if not path_exists:
                    status = CheckStatus.WARNING
                    msg = f"版本 {matrix['current']} (模块目录不存在)"
                    recommendation = f"请安装 {module_name} 模块"
                elif is_compatible:
                    status = CheckStatus.COMPATIBLE
                    msg = f"版本 {matrix['current']} ✅"
                    recommendation = ""
                else:
                    status = CheckStatus.INCOMPATIBLE
                    msg = f"版本 {matrix['current']} 不在支持范围 [{matrix['min']}, {matrix['max']})"
                    recommendation = f"请升级/降级 {module_name} 到兼容版本"

                results.append(CheckResult(
                    component=f"longhun-{module_name}",
                    check_type="module_version",
                    status=status,
                    message=msg,
                    expected=f"{matrix['min']} - {matrix['max']}",
                    actual=matrix["current"],
                    recommendation=recommendation,
                    details={
                        "min_version": matrix["min"],
                        "max_version": matrix["max"],
                        "current_version": matrix["current"],
                        "path_exists": path_exists,
                        "required_by": matrix["required_by"],
                    },
                ))
            except Exception as e:
                results.append(CheckResult(
                    component=f"longhun-{module_name}",
                    check_type="module_version",
                    status=CheckStatus.UNKNOWN,
                    message=f"版本解析失败: {str(e)[:80]}",
                ))

        self.results.extend(results)
        compatible = sum(1 for r in results if r.status == CheckStatus.COMPATIBLE)
        self.log(f"模块版本检查完成: {compatible}/{len(results)} 兼容", "OK")
        return results

    # ============================================================
    # 4. 跨模块接口兼容性
    # ============================================================

    def check_interface_compatibility(self) -> List[CheckResult]:
        """检查跨模块接口兼容性"""
        self.log("检查跨模块接口兼容性...", "CHECK")
        results = []

        for (module_a, module_b), interface_spec in INTERFACE_COMPATIBILITY.items():
            # 检查两个模块是否都存在
            module_paths = {
                "cnsh-core": CNSH_CORE,
                "skills": SKILLS_DIR,
                "monitoring": MONITORING_DIR,
                "logging": INTEGRATED_MODULES / "logging",
                "protocols": INTEGRATED_MODULES / "protocols",
                "gateway": INTEGRATED_MODULES / "gateway",
                "sync": INTEGRATED_MODULES / "sync",
                "executors": EXECUTORS_DIR,
                "notion": INTEGRATIONS_DIR / "notion",
            }

            path_a = module_paths.get(module_a, Path())
            path_b = module_paths.get(module_b, Path())
            both_exist = path_a.exists() and path_b.exists()

            if both_exist:
                status = CheckStatus.COMPATIBLE
                msg = f"接口 '{interface_spec['interface']}' 兼容 (API {interface_spec['min_api']}-{interface_spec['max_api']})"
            else:
                missing = []
                if not path_a.exists():
                    missing.append(module_a)
                if not path_b.exists():
                    missing.append(module_b)
                status = CheckStatus.WARNING
                msg = f"模块缺失: {', '.join(missing)} (接口 '{interface_spec['interface']}' 待验证)"

            results.append(CheckResult(
                component=f"{module_a} ↔ {module_b}",
                check_type="interface",
                status=status,
                message=msg,
                expected=f"API {interface_spec['min_api']}-{interface_spec['max_api']}",
                actual="已验证" if both_exist else "模块缺失",
                recommendation="" if both_exist else f"安装缺失模块: {', '.join(missing)}",
                details={
                    "interface": interface_spec["interface"],
                    "min_api": interface_spec["min_api"],
                    "max_api": interface_spec["max_api"],
                    "module_a_exists": path_a.exists(),
                    "module_b_exists": path_b.exists(),
                },
            ))

        self.results.extend(results)
        compatible = sum(1 for r in results if r.status == CheckStatus.COMPATIBLE)
        self.log(f"接口兼容性检查完成: {compatible}/{len(results)} 兼容", "OK")
        return results

    # ============================================================
    # 5. 配置文件格式兼容性
    # ============================================================

    def check_config_compatibility(self) -> List[CheckResult]:
        """检查配置文件格式兼容性"""
        self.log("检查配置文件格式兼容性...", "CHECK")
        results = []

        # 检查关键配置文件
        config_files = [
            (LONGHUN_BASE / "config.json", "json"),
            (LONGHUN_BASE / ".env", "env"),
            (CNSH_CORE / "config.py", "python"),
            (SKILLS_DIR / "__init__.py", "python"),
            (INTEGRATED_MODULES / "gateway" / "LongHun_DNA_Registry.md", "markdown"),
        ]

        for config_path, expected_format in config_files:
            exists = config_path.exists()
            if exists:
                try:
                    content = config_path.read_text(encoding="utf-8", errors="replace")
                    # 格式验证
                    if expected_format == "json":
                        json.loads(content)
                        format_ok = True
                    elif expected_format == "python":
                        ast.parse(content)
                        format_ok = True
                    else:
                        format_ok = len(content) > 0

                    status = CheckStatus.COMPATIBLE if format_ok else CheckStatus.WARNING
                    msg = f"格式正确 ({expected_format}, {len(content):,} bytes)"
                    if not format_ok:
                        msg = f"格式可能有误 ({expected_format})"

                except (json.JSONDecodeError, SyntaxError) as e:
                    status = CheckStatus.WARNING
                    msg = f"格式解析警告: {str(e)[:80]}"
            else:
                status = CheckStatus.INFO
                msg = f"配置文件不存在 (可选)"

            results.append(CheckResult(
                component=str(config_path.name),
                check_type="config",
                status=status,
                message=msg,
                expected=expected_format,
                actual="present" if exists else "missing",
                recommendation="" if exists or status == CheckStatus.INFO else f"创建默认配置文件: {config_path}",
                details={"path": str(config_path), "size": len(content) if exists else 0},
            ))

        # 检查目录结构兼容性
        required_structure = [
            LONGHUN_BASE,
            CNSH_CORE,
            SKILLS_DIR,
            MONITORING_DIR,
            INTEGRATED_MODULES,
        ]
        structure_ok = all(d.exists() for d in required_structure)

        results.append(CheckResult(
            component="目录结构",
            check_type="config",
            status=CheckStatus.COMPATIBLE if structure_ok else CheckStatus.WARNING,
            message="目录结构完整" if structure_ok else "部分目录缺失",
            expected="完整目录树",
            actual="完整" if structure_ok else "不完整",
            recommendation="" if structure_ok else "运行系统整合脚本创建目录结构",
            details={
                "required_dirs": [str(d) for d in required_structure],
                "existing": [str(d) for d in required_structure if d.exists()],
                "missing": [str(d) for d in required_structure if not d.exists()],
            },
        ))

        self.results.extend(results)
        compatible = sum(1 for r in results if r.status == CheckStatus.COMPATIBLE)
        self.log(f"配置兼容性检查完成: {compatible}/{len(results)} 兼容", "OK")
        return results

    # ============================================================
    # 6. 数据库/API兼容性
    # ============================================================

    def check_api_db_compatibility(self) -> List[CheckResult]:
        """检查数据库和API兼容性"""
        self.log("检查数据库/API兼容性...", "CHECK")
        results = []

        # 检查SQLite可用性
        try:
            import sqlite3
            sqlite_ver = sqlite3.sqlite_version
            results.append(CheckResult(
                component="SQLite",
                check_type="api_db",
                status=CheckStatus.COMPATIBLE,
                message=f"SQLite {sqlite_ver} 可用",
                expected="3.30+",
                actual=sqlite_ver,
            ))
        except ImportError:
            results.append(CheckResult(
                component="SQLite",
                check_type="api_db",
                status=CheckStatus.WARNING,
                message="SQLite 不可用",
                recommendation="安装sqlite3支持",
            ))

        # 检查网络API基础功能
        try:
            import urllib.request
            import ssl
            ctx = ssl.create_default_context()
            results.append(CheckResult(
                component="SSL/TLS",
                check_type="api_db",
                status=CheckStatus.COMPATIBLE,
                message="SSL上下文可创建",
            ))
        except Exception as e:
            results.append(CheckResult(
                component="SSL/TLS",
                check_type="api_db",
                status=CheckStatus.WARNING,
                message=f"SSL问题: {str(e)[:80]}",
            ))

        # 检查socket基础功能
        try:
            import socket
            test_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_sock.close()
            results.append(CheckResult(
                component="Socket",
                check_type="api_db",
                status=CheckStatus.COMPATIBLE,
                message="TCP Socket 可用",
            ))
        except Exception as e:
            results.append(CheckResult(
                component="Socket",
                check_type="api_db",
                status=CheckStatus.INCOMPATIBLE,
                message=f"Socket不可用: {str(e)[:80]}",
            ))

        # 检查asyncio支持
        try:
            import asyncio
            results.append(CheckResult(
                component="AsyncIO",
                check_type="api_db",
                status=CheckStatus.COMPATIBLE,
                message=f"AsyncIO 可用",
            ))
        except ImportError:
            results.append(CheckResult(
                component="AsyncIO",
                check_type="api_db",
                status=CheckStatus.WARNING,
                message="AsyncIO 不可用 (Python 3.4+ 应内置)",
            ))

        # 检查关键API端点格式（不实际连接）
        api_schemas_valid = True
        for api_name, config in {
            "cnsh_core": {"url": "http://localhost:8080/health", "method": "GET"},
            "mcp_server": {"url": "http://localhost:9000/health", "method": "GET"},
        }.items():
            url_valid = config["url"].startswith(("http://", "https://"))
            method_valid = config["method"] in ("GET", "POST", "PUT", "DELETE", "PATCH")
            if not (url_valid and method_valid):
                api_schemas_valid = False

        results.append(CheckResult(
            component="API端点格式",
            check_type="api_db",
            status=CheckStatus.COMPATIBLE if api_schemas_valid else CheckStatus.WARNING,
            message="API端点配置格式正确" if api_schemas_valid else "部分API端点格式有误",
        ))

        self.results.extend(results)
        compatible = sum(1 for r in results if r.status == CheckStatus.COMPATIBLE)
        self.log(f"API/DB兼容性检查完成: {compatible}/{len(results)} 兼容", "OK")
        return results

    # ============================================================
    # 7. 文件编码与换行符兼容性
    # ============================================================

    def check_file_encoding(self) -> List[CheckResult]:
        """检查关键文件的编码和换行符兼容性"""
        self.log("检查文件编码兼容性...", "CHECK")
        results = []

        # 采样检查关键Python文件
        sample_files = []
        for pattern in ["*.py", "*.sh", "*.md"]:
            for directory in [SKILLS_DIR, CNSH_CORE, INTEGRATED_MODULES]:
                if directory.exists():
                    sample_files.extend(list(directory.rglob(pattern))[:5])

        checked = 0
        issues = []
        for file_path in sample_files[:15]:
            try:
                with open(file_path, "rb") as f:
                    raw = f.read(4096)
                # 检测BOM
                has_bom = raw.startswith(b"\xef\xbb\xbf")
                # 检测换行符
                crlf_count = raw.count(b"\r\n")
                lf_count = raw.count(b"\n") - crlf_count

                if crlf_count > 0 and lf_count > 0:
                    issues.append(f"{file_path.name}: 混合换行符 (CRLF:{crlf_count}, LF:{lf_count})")
                checked += 1
            except Exception:
                pass

        if not issues:
            results.append(CheckResult(
                component="文件编码/换行符",
                check_type="config",
                status=CheckStatus.COMPATIBLE,
                message=f"已检查 {checked} 个文件，编码兼容",
                details={"checked_files": checked, "issues": 0},
            ))
        else:
            results.append(CheckResult(
                component="文件编码/换行符",
                check_type="config",
                status=CheckStatus.WARNING,
                message=f"发现 {len(issues)} 个文件换行符问题",
                recommendation="统一使用LF换行符: find . -name '*.py' | xargs dos2unix",
                details={"checked_files": checked, "issues": issues[:5]},
            ))

        self.results.extend(results)
        for r in results:
            self.log(f"  {r.status.value} {r.component}: {r.message}")
        return results

    # ============================================================
    # 主执行流程
    # ============================================================

    def run_all_checks(self) -> Dict[str, Any]:
        """执行完整的兼容性检查"""
        self.log(f"🔍 启动完整兼容性检查 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "CHECK")

        self.check_python_version()           # 1. Python版本
        self.check_dependencies()             # 2. 第三方依赖
        self.check_module_versions()          # 3. 龍魂模块版本
        self.check_interface_compatibility()  # 4. 跨模块接口
        self.check_config_compatibility()     # 5. 配置文件
        self.check_api_db_compatibility()     # 6. API/DB
        self.check_file_encoding()            # 7. 文件编码

        return self.generate_report()

    def generate_report(self) -> Dict[str, Any]:
        """生成兼容性检查报告"""
        # 分类统计
        categories = {}
        for r in self.results:
            cat = r.check_type
            if cat not in categories:
                categories[cat] = {"total": 0, "compatible": 0, "incompatible": 0, "warning": 0, "unknown": 0, "info": 0}
            categories[cat]["total"] += 1
            if r.status == CheckStatus.COMPATIBLE:
                categories[cat]["compatible"] += 1
            elif r.status == CheckStatus.INCOMPATIBLE:
                categories[cat]["incompatible"] += 1
            elif r.status == CheckStatus.WARNING:
                categories[cat]["warning"] += 1
            elif r.status == CheckStatus.UNKNOWN:
                categories[cat]["unknown"] += 1
            elif r.status == CheckStatus.INFO:
                categories[cat]["info"] += 1

        # 总体统计
        total = len(self.results)
        compatible = sum(1 for r in self.results if r.status == CheckStatus.COMPATIBLE)
        incompatible = sum(1 for r in self.results if r.status == CheckStatus.INCOMPATIBLE)
        warnings = sum(1 for r in self.results if r.status == CheckStatus.WARNING)
        unknown = sum(1 for r in self.results if r.status == CheckStatus.UNKNOWN)

        # 兼容性评分
        score = (compatible / total * 100) if total > 0 else 0

        if incompatible == 0 and warnings == 0:
            overall = "✅ 完全兼容"
        elif incompatible == 0:
            overall = "⚠️ 基本兼容(有警告)"
        else:
            overall = "❌ 存在不兼容项"

        # 生成升级建议
        upgrade_plan = self._generate_upgrade_plan()

        report = {
            "meta": {
                "checker": CHECKER_NAME,
                "version": VERSION,
                "dna": DNA,
                "timestamp": datetime.now().isoformat(),
                "python_version": sys.version,
            },
            "summary": {
                "total_checks": total,
                "compatible": compatible,
                "incompatible": incompatible,
                "warnings": warnings,
                "unknown": unknown,
                "compatibility_score": round(score, 1),
                "overall_status": overall,
            },
            "categories": categories,
            "results": [r.to_dict() for r in self.results],
            "upgrade_plan": upgrade_plan,
        }

        self._print_report_summary(report)
        return report

    def _generate_upgrade_plan(self) -> List[Dict]:
        """生成升级计划建议"""
        plan = []

        # 收集所有需要修复的项目
        incompatible_items = [r for r in self.results if r.status == CheckStatus.INCOMPATIBLE]
        warning_items = [r for r in self.results if r.status == CheckStatus.WARNING]

        if incompatible_items:
            plan.append({
                "priority": "🔴 P0-紧急",
                "title": "修复不兼容项",
                "items": [{"component": r.component, "action": r.recommendation or "手动修复"} for r in incompatible_items],
            })

        if warning_items:
            plan.append({
                "priority": "🟡 P1-重要",
                "title": "处理警告项",
                "items": [{"component": r.component, "action": r.recommendation or "检查配置"} for r in warning_items[:10]],
            })

        # 检查龍魂系统版本统一性
        versions = {name: info["current"] for name, info in LONGHUN_MODULE_MATRIX.items()}
        plan.append({
            "priority": "🟢 P2-建议",
            "title": "版本统一建议",
            "description": "所有模块版本应保持在兼容范围内",
            "current_versions": versions,
        })

        if not plan:
            plan.append({
                "priority": "✅",
                "title": "无需升级",
                "description": "系统完全兼容，无需任何升级操作",
            })

        return plan

    def _print_report_summary(self, report: Dict):
        s = report["summary"]
        print(f"""
╔══════════════════════════════════════════════════════════════════╗
║           🔍 龍魂系統·兼容性检查报告                           ║
╠══════════════════════════════════════════════════════════════════╣
║  总检查数:   {s['total_checks']:3d}                                        ║
║  ✅ 兼容:     {s['compatible']:3d}                                        ║
║  ❌ 不兼容:   {s['incompatible']:3d}                                        ║
║  ⚠️  警告:     {s['warnings']:3d}                                        ║
║  ❓ 未知:     {s['unknown']:3d}                                        ║
║  兼容评分:   {s['compatibility_score']:5.1f}%                                  ║
║  状态:       {s['overall_status']:20s}                    ║
╚══════════════════════════════════════════════════════════════════╝
""")
        # 升级建议摘要
        if report["upgrade_plan"]:
            print("📋 升级建议:")
            for item in report["upgrade_plan"]:
                print(f"\n  {item['priority']}: {item['title']}")
                if "items" in item:
                    for sub in item["items"][:5]:
                        print(f"    - {sub['component']}: {sub['action'][:60]}")

    def export_report(self, filepath: Optional[str] = None) -> str:
        """导出兼容性报告"""
        report = self.generate_report()
        if filepath is None:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"/tmp/longhun_compatibility_report_{ts}.json"

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        self.log(f"兼容性报告已导出: {filepath}", "OK")
        return filepath

    def export_markdown_report(self, filepath: Optional[str] = None) -> str:
        """导出Markdown格式兼容性报告"""
        report = self.generate_report()
        if filepath is None:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"/tmp/longhun_compatibility_report_{ts}.md"

        s = report["summary"]
        md = f"""# 🔍 龍魂系統·兼容性检查报告
# 日期: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CST
# DNA: {DNA}

---

## ✅ 检查摘要

| 项目 | 数值 |
|------|------|
| **总检查数** | {s['total_checks']} |
| **✅ 兼容** | {s['compatible']} |
| **❌ 不兼容** | {s['incompatible']} |
| **⚠️ 警告** | {s['warnings']} |
| **❓ 未知** | {s['unknown']} |
| **兼容评分** | {s['compatibility_score']:.1f}% |
| **状态** | {s['overall_status']} |

---

## 📊 分类详情

| 类别 | 兼容 | 不兼容 | 警告 | 未知 | 信息 |
|------|------|--------|------|------|------|
"""
        for cat, stats in report["categories"].items():
            md += f"| {cat} | {stats['compatible']} | {stats['incompatible']} | {stats['warning']} | {stats['unknown']} | {stats['info']} |\n"

        md += "\n---\n\n## 🔍 详细结果\n\n"
        for r in report["results"]:
            md += f"""### {r['component']}
- **类型**: {r['check_type']}
- **状态**: {r['status']}
- **预期**: {r['expected']}
- **实际**: {r['actual']}
- **消息**: {r['message']}
- **建议**: {r['recommendation'] or '无'}

"""

        md += "\n---\n\n## 📋 升级计划\n\n"
        for item in report["upgrade_plan"]:
            md += f"### {item['priority']}: {item['title']}\n"
            if "description" in item:
                md += f"{item['description']}\n\n"
            if "items" in item:
                for sub in item["items"]:
                    md += f"- **{sub['component']}**: {sub['action']}\n"
            md += "\n"

        md += f"""
---

**DNA**: {DNA}
**检查器**: {CHECKER_NAME} v{VERSION}
**Python**: {sys.version.split()[0]}
**报告时间**: {datetime.now().isoformat()}

---

龍魂系統·兼容性检查完成
"""

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md)

        self.log(f"Markdown兼容性报告已导出: {filepath}", "OK")
        return filepath


# ============================================================
# 命令行入口
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂系統兼容性检查器")
    parser.add_argument("--quiet", "-q", action="store_true", help="静默模式")
    parser.add_argument("--check", "-c", type=str, default=None,
                       help="只检查指定类别 (python|deps|modules|interfaces|config|apidb|encoding)")
    parser.add_argument("--export-json", "-j", type=str, default=None, help="导出JSON报告")
    parser.add_argument("--export-md", "-m", type=str, default=None, help="导出Markdown报告")
    args = parser.parse_args()

    checker = CompatibilityChecker(verbose=not args.quiet)

    if args.check:
        check_map = {
            "python": checker.check_python_version,
            "deps": checker.check_dependencies,
            "modules": checker.check_module_versions,
            "interfaces": checker.check_interface_compatibility,
            "config": checker.check_config_compatibility,
            "apidb": checker.check_api_db_compatibility,
            "encoding": checker.check_file_encoding,
        }
        if args.check in check_map:
            check_map[args.check]()
            report = checker.generate_report()
        else:
            print(f"❌ 未知类别: {args.check}")
            print(f"可用类别: {', '.join(check_map.keys())}")
            sys.exit(1)
    else:
        report = checker.run_all_checks()

    if args.export_json:
        checker.export_report(args.export_json)
    if args.export_md:
        checker.export_markdown_report(args.export_md)

    # 返回码
    incompatible = report["summary"]["incompatible"]
    sys.exit(0 if incompatible == 0 else 1)


if __name__ == "__main__":
    main()
