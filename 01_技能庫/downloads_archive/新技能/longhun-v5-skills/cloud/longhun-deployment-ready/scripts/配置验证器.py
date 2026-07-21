#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂配置验证器 (Longhun Configuration Validator)
================================
DNA: #龍芯⚡️2026-06-19-LONGHUN-DEPLOY-READY-v5.2

验证配置文件完整性、参数正确性、权限安全性。

用法:
    python3 配置验证器.py [--fix] [--strict]
"""

import os
import sys
import re
import json
import stat
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

SKILL_DNA = "#龍芯⚡️2026-06-19-LONGHUN-DEPLOY-READY-v5.2"


class Colors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    OKBLUE = '\033[94m'


@dataclass
class ConfigCheckResult:
    file: str
    check: str
    status: str
    message: str
    suggestion: str = ""


class ConfigurationValidator:
    """配置验证器 - 全面检查配置文件"""

    # 配置文件清单
    REQUIRED_FILES = [
        "config.yaml",
        "config.json",
        ".env",
        "requirements.txt",
    ]

    # 必要配置参数
    REQUIRED_PARAMS = {
        "app_name": str,
        "debug": bool,
        "database_url": str,
        "secret_key": str,
        "log_level": str,
    }

    # 敏感字段模式
    SENSITIVE_PATTERNS = [
        r'password\s*=\s*["\']?[^"\'\s]+["\']?',
        r'secret\s*=\s*["\']?[^"\'\s]+["\']?',
        r'api_key\s*=\s*["\']?[^"\'\s]+["\']?',
        r'token\s*=\s*["\']?[^"\'\s]+["\']?',
        r'private_key\s*=\s*["\']?[^"\'\s]+["\']?',
    ]

    # 安全的文件权限 (八进制)
    SECURE_PERMISSIONS = {
        ".env": 0o600,
        "config.yaml": 0o644,
        "config.json": 0o644,
        ".secret": 0o600,
        "id_rsa": 0o600,
    }

    def __init__(self, project_root: str = ".", auto_fix: bool = False, strict: bool = False):
        self.project_root = Path(project_root)
        self.auto_fix = auto_fix
        self.strict = strict
        self.results: List[ConfigCheckResult] = []

    def check_file_existence(self) -> List[ConfigCheckResult]:
        """检查配置文件是否存在"""
        results = []
        for filename in self.REQUIRED_FILES:
            path = self.project_root / filename
            exists = path.exists()
            status = "PASS" if exists else ("FAIL" if filename in ["config.yaml", ".env"] else "WARN")
            msg = f"文件{'存在' if exists else '缺失'}: {filename}"
            suggestion = "" if exists else f"创建 {filename} 文件"
            results.append(ConfigCheckResult(filename, "文件存在性", status, msg, suggestion))
        self.results.extend(results)
        return results

    def check_file_permissions(self) -> List[ConfigCheckResult]:
        """检查文件权限安全性"""
        results = []
        for filename, expected_mode in self.SECURE_PERMISSIONS.items():
            path = self.project_root / filename
            if not path.exists():
                continue
            current_mode = stat.S_IMODE(path.stat().st_mode)
            is_secure = current_mode <= expected_mode
            status = "PASS" if is_secure else "WARN"
            current_oct = oct(current_mode)[2:].zfill(3)
            expected_oct = oct(expected_mode)[2:].zfill(3)
            msg = f"权限: {current_oct} (期望: <={expected_oct})"
            suggestion = f"chmod {expected_oct} {filename}" if not is_secure else ""

            if not is_secure and self.auto_fix:
                os.chmod(path, expected_mode)
                msg += " [已自动修复]"
                status = "PASS"

            results.append(ConfigCheckResult(filename, "权限安全", status, msg, suggestion))
        self.results.extend(results)
        return results

    def check_env_variables(self) -> List[ConfigCheckResult]:
        """检查环境变量配置"""
        results = []
        required_env = ["APP_ENV", "DATABASE_URL", "SECRET_KEY", "LOG_LEVEL"]
        missing = []
        for var in required_env:
            value = os.getenv(var)
            if not value:
                missing.append(var)

        if missing:
            results.append(ConfigCheckResult(".env", "环境变量",
                                           "WARN" if not self.strict else "FAIL",
                                           f"缺失环境变量: {', '.join(missing)}",
                                           "在.env或环境变量中设置"))
        else:
            results.append(ConfigCheckResult(".env", "环境变量", "PASS",
                                           f"所有{len(required_env)}个环境变量已设置"))

        # 检查SECRET_KEY强度
        secret_key = os.getenv("SECRET_KEY", "")
        if secret_key and len(secret_key) < 16:
            results.append(ConfigCheckResult(".env", "密钥强度", "WARN",
                                           f"SECRET_KEY长度{len(secret_key)}，建议>=16字符",
                                           "生成更强的密钥: openssl rand -hex 32"))
        elif secret_key:
            results.append(ConfigCheckResult(".env", "密钥强度", "PASS",
                                           f"SECRET_KEY长度{len(secret_key)}，强度OK"))

        self.results.extend(results)
        return results

    def check_sensitive_exposure(self) -> List[ConfigCheckResult]:
        """检查敏感信息是否暴露"""
        results = []
        issues_found = []

        # 扫描代码文件
        for ext in ['*.py', '*.yaml', '*.yml', '*.json', '*.sh']:
            for filepath in self.project_root.rglob(ext):
                if 'venv' in str(filepath) or '__pycache__' in str(filepath):
                    continue
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        for i, line in enumerate(content.split('\n'), 1):
                            for pattern in self.SENSITIVE_PATTERNS:
                                if re.search(pattern, line, re.IGNORECASE):
                                    if 'os.getenv' not in line and 'getenv' not in line:
                                        issues_found.append(f"{filepath}:{i}")
                except Exception:
                    pass

        if issues_found:
            status = "WARN" if not self.strict else "FAIL"
            msg = f"发现{len(issues_found)}处可能的硬编码敏感信息"
            suggestion = "使用环境变量替代硬编码: os.getenv('VAR_NAME')"
            results.append(ConfigCheckResult("源代码", "敏感信息暴露", status, msg, suggestion))
            if len(issues_found) <= 5:
                for issue in issues_found:
                    results.append(ConfigCheckResult(issue, "敏感信息", "WARN", "硬编码敏感值", "移到.env文件"))
        else:
            results.append(ConfigCheckResult("源代码", "敏感信息暴露", "PASS",
                                           "未发现硬编码敏感信息"))

        self.results.extend(results)
        return results

    def check_database_url(self) -> List[ConfigCheckResult]:
        """检查数据库URL格式"""
        results = []
        db_url = os.getenv("DATABASE_URL", "")
        if not db_url:
            results.append(ConfigCheckResult("DATABASE_URL", "格式检查", "WARN",
                                           "DATABASE_URL未设置"))
        else:
            # 检查URL格式
            pattern = r'^(postgresql|mysql|sqlite|mongodb)://[^\s]+$'
            if re.match(pattern, db_url, re.IGNORECASE):
                # 检查是否包含密码
                if '@' in db_url and ':' in db_url.split('@')[0]:
                    results.append(ConfigCheckResult("DATABASE_URL", "格式检查", "PASS",
                                                   "数据库URL格式正确且包含认证信息"))
                else:
                    results.append(ConfigCheckResult("DATABASE_URL", "格式检查", "PASS",
                                                   "数据库URL格式正确"))
            else:
                results.append(ConfigCheckResult("DATABASE_URL", "格式检查", "WARN",
                                               "数据库URL格式可能不正确",
                                               "格式: dialect://user:pass@host/db"))
        self.results.extend(results)
        return results

    def check_config_yaml(self) -> List[ConfigCheckResult]:
        """检查YAML配置文件"""
        results = []
        config_path = self.project_root / "config.yaml"
        if not config_path.exists():
            self.results.append(ConfigCheckResult("config.yaml", "YAML格式", "SKIP",
                                                "config.yaml不存在"))
            return results

        try:
            import yaml
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            if config is None:
                results.append(ConfigCheckResult("config.yaml", "YAML格式", "WARN",
                                               "文件为空"))
            elif isinstance(config, dict):
                # 检查必要字段
                missing_keys = [k for k in self.REQUIRED_PARAMS.keys() if k not in config]
                if missing_keys:
                    results.append(ConfigCheckResult("config.yaml", "必要字段",
                                                   "WARN",
                                                   f"缺失字段: {', '.join(missing_keys)}"))
                else:
                    results.append(ConfigCheckResult("config.yaml", "必要字段",
                                                   "PASS", "所有必要字段已配置"))
                results.append(ConfigCheckResult("config.yaml", "YAML格式", "PASS",
                                               "YAML格式有效"))
            else:
                results.append(ConfigCheckResult("config.yaml", "YAML格式", "WARN",
                                               "配置应为字典格式"))
        except ImportError:
            results.append(ConfigCheckResult("config.yaml", "YAML格式", "SKIP",
                                           "PyYAML未安装: pip install pyyaml"))
        except Exception as e:
            results.append(ConfigCheckResult("config.yaml", "YAML格式", "FAIL",
                                           f"解析错误: {str(e)[:100]}"))

        self.results.extend(results)
        return results

    def run_all(self) -> List[ConfigCheckResult]:
        """运行全部配置检查"""
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║        龍魂配置验证器                                          ║
╠══════════════════════════════════════════════════════════════╣
║  {SKILL_DNA}    ║
╚══════════════════════════════════════════════════════════════╝
""")
        self.check_file_existence()
        self.check_file_permissions()
        self.check_env_variables()
        self.check_sensitive_exposure()
        self.check_database_url()
        self.check_config_yaml()
        return self.results

    def print_report(self):
        """打印检查报告"""
        print("\n【配置验证报告】")
        for r in self.results:
            color = Colors.OKGREEN if r.status == "PASS" else (
                Colors.WARNING if r.status in ("WARN", "SKIP") else Colors.FAIL
            )
            print(f"  {color}[{r.status}]{Colors.ENDC} {r.file} - {r.check}")
            print(f"      {r.message}")
            if r.suggestion:
                print(f"      建议: {r.suggestion}")

        # 汇总
        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == "PASS")
        warns = sum(1 for r in self.results if r.status in ("WARN", "SKIP"))
        failed = sum(1 for r in self.results if r.status == "FAIL")

        print(f"\n{'='*50}")
        print(f"  汇总: {passed}通过 / {warns}警告 / {failed}失败 (共{total}项)")
        if failed == 0:
            print(f"  {Colors.OKGREEN}配置检查通过{Colors.ENDC}")
        else:
            print(f"  {Colors.FAIL}存在 {failed} 个配置问题{Colors.ENDC}")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", action="store_true", help="自动修复权限问题")
    parser.add_argument("--strict", action="store_true", help="严格模式")
    parser.add_argument("--root", default=".", help="项目根目录")
    args = parser.parse_args()

    validator = ConfigurationValidator(project_root=args.root, auto_fix=args.fix, strict=args.strict)
    validator.run_all()
    validator.print_report()


if __name__ == "__main__":
    main()
