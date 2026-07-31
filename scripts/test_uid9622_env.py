# DNA: #龍芯⚡️丙午·乙未·乙丑·井-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-SCRIPT-TEST_UID9622_ENV-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UID9622 环境测试脚本
检查所有必要的开发环境组件
"""

import sys
import os
import subprocess
import importlib.util
from datetime import datetime


def check_python_version():
    """检查Python版本"""
    print(f"🐍 Python版本: {sys.version.split()[0]}")
    version_info = sys.version_info
    if version_info.major >= 3 and version_info.minor >= 8:
        print("✅ Python版本符合要求")
        return True
    else:
        print("❌ Python版本过低，建议升级到3.8+")
        return False


def check_package(package_name, display_name=None):
    """检查Python包是否安装"""
    if display_name is None:
        display_name = package_name

    try:
        spec = importlib.util.find_spec(package_name)
        if spec is not None:
            print(f"✅ {display_name}包正常")
            return True
        else:
            print(f"❌ {display_name}包未安装")
            return False
    except ImportError:
        print(f"❌ {display_name}包未安装")
        return False


def check_command(command, display_name=None):
    """检查系统命令是否可用"""
    if display_name is None:
        display_name = command

    try:
        result = subprocess.run(
            [command, '--version'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip().splitlines()[0]
            print(f"✅ {display_name}: {version}")
            return True
        else:
            print(f"❌ {display_name}未安装或无法访问")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print(f"❌ {display_name}未安装或无法访问")
        return False


def check_directories():
    """检查项目目录结构"""
    base_path = os.path.expanduser("~/UID9622_Projects")
    required_dirs = ['Python', 'NodeJS', 'Scripts', 'Config', 'Data', 'Tests']

    print(f"📁 检查项目结构: {base_path}")

    all_exist = True
    for directory in required_dirs:
        dir_path = os.path.join(base_path, directory)
        if os.path.exists(dir_path):
            print(f"✅ {directory}/")
        else:
            print(f"❌ {directory}/")
            all_exist = False

    return all_exist


def main():
    """主测试函数"""
    print("🔍 UID9622 环境测试开始")
    print("=" * 50)
    print(f"📅 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"💻 系统: {os.uname().sysname} {os.uname().release}")
    print(f"👨‍💻 用户: {os.getenv('USER')}")
    print(f"📁 当前目录: {os.getcwd()}")
    print("=" * 50)

    python_ok = check_python_version()

    packages = [
        ('requests', 'Requests HTTP库'),
        ('psutil', '系统监控库'),
        ('openai', 'OpenAI API库'),
        ('dotenv', 'python-dotenv'),
        ('watchdog', '文件监控库'),
        ('colorama', '命令行颜色库'),
    ]

    package_results = [check_package(pkg, display) for pkg, display in packages]

    commands = [
        ('git', 'Git 版本控制'),
        ('node', 'Node.js'),
        ('npm', 'npm 包管理器'),
        ('brew', 'Homebrew'),
        ('code', 'VS Code'),
    ]

    command_results = [check_command(cmd, display) for cmd, display in commands]

    dir_ok = check_directories()

    print("=" * 50)
    print("📋 测试总结:")
    print(f"Python环境: {'✅' if python_ok else '❌'}")
    print(f"Python包: {sum(package_results)}/{len(package_results)} {'✅' if all(package_results) else '⚠️'}")
    print(f"系统命令: {sum(command_results)}/{len(command_results)} {'✅' if all(command_results) else '⚠️'}")
    print(f"目录结构: {'✅' if dir_ok else '❌'}")

    if all([python_ok, all(package_results), all(command_results), dir_ok]):
        print("🎉 所有环境检查通过！UID9622开发环境就绪！")
        return 0
    else:
        print("⚠️ 部分环境检查未通过，请检查上述问题")
        return 1


if __name__ == "__main__":
    sys.exit(main())
