##龍芯⚡️2026-06-21-SCRIPT-SETUP_UID9622_DEVENV-v1.0
# 君子協議: 本文件受龍魂DNA追溯保護

#!/bin/zsh
# UID9622 zsh环境下开发环境完整搭建脚本
# 使用UID9622专用终端环境

set -euo pipefail

echo "🚀 UID9622 zsh开发环境搭建开始"

# 步骤1: 创建项目结构
echo "📁 步骤1: 创建完整项目结构"
mkdir -p ~/UID9622_Projects/{Python,NodeJS,Scripts,Config,Data,Tests}
mkdir -p ~/UID9622_DevEnv
echo "✅ 项目结构已创建"
ls -la ~/UID9622_Projects

# 步骤2: 检查并安装Homebrew
echo "🍺 步骤2: 检查Homebrew环境"
if ! command -v brew &> /dev/null; then
    echo "正在安装Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    # 将 Homebrew 加入当前 zsh 路径（如需要）
    if [[ -f /opt/homebrew/bin/brew ]]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    elif [[ -f /usr/local/bin/brew ]]; then
        eval "$(/usr/local/bin/brew shellenv)"
    fi
else
    echo "✅ Homebrew已存在，正在更新"
    brew update
fi

# 步骤3: 安装Python环境
echo "🐍 步骤3: 安装Python开发环境"
# 优先使用项目已有的 Python 3.14，不强制降级到 3.12
if ! command -v python3 &> /dev/null; then
    brew install python@3.12
fi
echo "Python版本: $(python3 --version)"
python3 -m pip install --upgrade pip --user 2>/dev/null || python3 -m pip install --upgrade pip
echo "✅ Python环境就绪"

# 步骤4: 安装Node.js
echo "📦 步骤4: 安装Node.js环境"
if ! command -v node &> /dev/null; then
    brew install node
fi
echo "Node.js版本: $(node --version)"
echo "npm版本: $(npm --version)"
echo "✅ Node.js环境就绪"

# 步骤5: 安装开发工具
echo "🔧 步骤5: 安装开发工具"
if ! command -v git &> /dev/null; then
    brew install git
fi
if ! command -v code &> /dev/null; then
    brew install --cask visual-studio-code
fi
echo "Git版本: $(git --version)"
echo "✅ 开发工具安装完成"

# 步骤6: 安装Python开发包
echo "📚 步骤6: 安装Python开发包"
# 推荐：使用 virtualenv 隔离，避免污染系统 Python
python3 -m venv ~/UID9622_Projects/.venv
source ~/UID9622_Projects/.venv/bin/activate
pip install --upgrade pip
pip install virtualenv requests python-dotenv watchdog colorama psutil openai notion-client
echo "✅ Python包安装完成"

# 步骤7: 创建配置文件
echo "⚙️ 步骤7: 创建配置文件"
cd ~/UID9622_Projects

today=$(date +%Y-%m-%d)
cat > Config/.env.template << EOF
# UID9622 环境配置模板
# 创建日期: ${today}

# OpenAI API 配置
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4

# Notion API 配置
NOTION_TOKEN=your_notion_token_here
NOTION_DATABASE_ID=your_database_id_here

# 开发环境设置
NODE_ENV=development
PYTHON_ENV=development
DEBUG=true

# UID9622 专用配置
UID9622_PROJECT_ROOT=~/UID9622_Projects
UID9622_WORKSPACE=UID9622_DevEnv
EOF

echo "✅ 配置文件模板已创建"
cat Config/.env.template

# 步骤8: 创建环境测试脚本
echo "🧪 步骤8: 创建环境测试脚本"
cat > Scripts/test_env.py << 'PYEOF'
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

    # 检查Python
    python_ok = check_python_version()

    # 检查Python包
    packages = [
        ('requests', 'Requests HTTP库'),
        ('psutil', '系统监控库'),
        ('openai', 'OpenAI API库'),
        ('dotenv', 'python-dotenv'),
        ('watchdog', '文件监控库'),
        ('colorama', '命令行颜色库'),
    ]

    package_results = [check_package(pkg, display) for pkg, display in packages]

    # 检查系统命令
    commands = [
        ('git', 'Git 版本控制'),
        ('node', 'Node.js'),
        ('npm', 'npm 包管理器'),
        ('brew', 'Homebrew'),
        ('code', 'VS Code'),
    ]

    command_results = [check_command(cmd, display) for cmd, display in commands]

    # 检查目录结构
    dir_ok = check_directories()

    # 总结
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
PYEOF

chmod +x Scripts/test_env.py
echo "✅ 环境测试脚本已创建"

# 步骤9: 运行测试
echo "🧪 步骤9: 运行环境测试"
python3 Scripts/test_env.py || true

echo "🎉 UID9622 zsh开发环境搭建完成"
echo "提示：要激活虚拟环境，请运行 source ~/UID9622_Projects/.venv/bin/activate"
