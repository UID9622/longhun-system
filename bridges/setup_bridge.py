#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 DeepSeek 中继桥·自动化配置脚本 v1.0

DNA: #龍芯⚡️2026-05-31-23:44-DEEPSEEK-BRIDGE-SETUP-v1.0
M号: M266

五个步骤完成桥的配置：
  1. 验证 DeepSeek API 密钥
  2. 创建虚拟环境
  3. 安装依赖
  4. 配置 .env 文件 (权限 chmod 600)
  5. 启动测试

主权声明:
  · 密钥只存 ~/.deepseek_bridge.env (chmod 600)
  · 虚拟环境在 ./bridges/.venv/
  · .gitignore 已加 .venv/ 和 ~/.deepseek_bridge.env
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from getpass import getpass

# 颜色输出
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'

def print_step(step, msg):
    print(f"{BLUE}[步骤 {step}]{NC} {msg}")

def print_ok(msg):
    print(f"{GREEN}✅{NC} {msg}")

def print_error(msg):
    print(f"{RED}❌{NC} {msg}")

def print_warning(msg):
    print(f"{YELLOW}⚠️{NC} {msg}")

def run_cmd(cmd, desc=""):
    if desc:
        print(f"  运行: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"    {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"    错误: {e}")
        return False

def main():
    print(f"\n{BLUE}╔═══════════════════════════════════════════════════════╗{NC}")
    print(f"{BLUE}║   龍魂 DeepSeek 中继桥 · 自动化配置 v1.0              ║{NC}")
    print(f"{BLUE}║   DNA: #龍芯⚡️2026-05-31-23:44-DEEPSEEK-BRIDGE-v1.0  ║{NC}")
    print(f"{BLUE}╚═══════════════════════════════════════════════════════╝{NC}\n")

    # 获取项目根目录
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    venv_dir = script_dir / ".venv"
    env_file = Path.home() / ".deepseek_bridge.env"

    print_step("1/5", "验证 DeepSeek API 密钥")
    print()

    if env_file.exists():
        print_warning(f"检测到已有 {env_file}")
        with open(env_file) as f:
            existing_key = f.read().strip()
            if "DEEPSEEK_API_KEY=" in existing_key:
                response = input(f"是否使用现有密钥? (y/n): ").strip().lower()
                if response == "y":
                    print_ok(f"使用现有密钥 (文件: {env_file})")
                    api_key = None
                else:
                    api_key = getpass("请输入新的 DeepSeek API 密钥 (sk-xxx): ").strip()
            else:
                api_key = getpass("请输入 DeepSeek API 密钥 (sk-xxx): ").strip()
    else:
        api_key = getpass("请输入 DeepSeek API 密钥 (sk-xxx): ").strip()

    # 验证密钥格式
    if api_key and not api_key.startswith("sk-"):
        print_error("密钥必须以 'sk-' 开头")
        sys.exit(1)

    # 写入 .env 文件 (权限 600)
    if api_key:
        with open(env_file, "w") as f:
            f.write(f"DEEPSEEK_API_KEY={api_key}\n")
            f.write(f"DEEPSEEK_MODEL=deepseek-chat\n")
            f.write(f"OLLAMA_FALLBACK=false\n")
        os.chmod(env_file, 0o600)
        print_ok(f"密钥已保存: {env_file} (权限: 600)")
    else:
        print_ok(f"使用现有密钥: {env_file}")

    print()

    # 步骤 2: 虚拟环境
    print_step("2/5", "创建 Python 虚拟环境")
    if venv_dir.exists():
        print_warning(f"虚拟环境已存在: {venv_dir}")
    else:
        print("  创建虚拟环境...")
        if not run_cmd(f"python3 -m venv {venv_dir}"):
            print_error("虚拟环境创建失败")
            sys.exit(1)
        print_ok(f"虚拟环境已创建: {venv_dir}")

    print()

    # 步骤 3: 安装依赖
    print_step("3/5", "安装 Python 依赖")
    pip_cmd = f"source {venv_dir}/bin/activate && pip install -q -r {script_dir}/requirements.txt"
    if run_cmd(pip_cmd):
        print_ok("依赖安装完成")
    else:
        print_error("依赖安装失败")
        sys.exit(1)

    print()

    # 步骤 4: 配置 .gitignore
    print_step("4/5", "配置 .gitignore (密钥不入 Git)")
    gitignore = project_root / ".gitignore"
    entries = [
        "bridges/.venv/",
        "~/.deepseek_bridge.env"
    ]

    if gitignore.exists():
        with open(gitignore) as f:
            content = f.read()
        for entry in entries:
            if entry not in content:
                with open(gitignore, "a") as f:
                    f.write(f"\n{entry}")
                print_ok(f"已添加到 .gitignore: {entry}")
            else:
                print_ok(f"已在 .gitignore 中: {entry}")
    else:
        with open(gitignore, "w") as f:
            for entry in entries:
                f.write(f"{entry}\n")
        print_ok(f".gitignore 已创建")

    print()

    # 步骤 5: 验证
    print_step("5/5", "验证桥启动")
    print()
    print(f"{YELLOW}🧪 测试命令:${NC}")
    print(f"  cd {script_dir}")
    print(f"  source .venv/bin/activate")
    print(f"  python3 deepseek_bridge.py")
    print()

    # 提示后续步骤
    print(f"{BLUE}════ 接下来的步骤 ════{NC}")
    print()
    print("1️⃣  启动 DeepSeek 桥:")
    print(f"   cd {script_dir}")
    print(f"   source .venv/bin/activate")
    print(f"   uvicorn deepseek_bridge:app --host 127.0.0.1 --port 8788")
    print()
    print("2️⃣  在新终端测试 (伪装成 Anthropic SDK):")
    print(f"   curl http://127.0.0.1:8788/v1/messages \\")
    print(f"     -H 'x-api-key: sk-anthropic-dummy' \\")
    print(f"     -H 'Content-Type: application/json' \\")
    print(f"     -d '{{\"model\": \"claude-3-5-sonnet\", \"max_tokens\": 128, \"messages\": [{{\"role\": \"user\", \"content\": \"你是谁\"}}]}}'")
    print()
    print("3️⃣  修改 dialog-server.js:")
    print(f"   export ANTHROPIC_BASE_URL=\"http://127.0.0.1:8788\"")
    print(f"   export ANTHROPIC_API_KEY=\"sk-anthropic-dummy\"")
    print()
    print("4️⃣  查看日志:")
    print(f"   tail -f ~/longhun-system/logs/deepseek_bridge.log")
    print()

    print_ok("配置完成！")
    print()

if __name__ == "__main__":
    main()
