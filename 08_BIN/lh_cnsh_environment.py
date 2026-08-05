#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · CNSH 环境集成引擎 v2.0
DNA: #龍芯⚡️丙午·乙未·戊申·泽地萃-CNSH-ENV-v2.0-UID9622

功能：
  1. 统一 CNSH 全局变量管理（环境变量 + Python 常量）
  2. 终端显示增强（ZSH 提示符 + 动态卦象）
  3. 文件创建自动挂载主权尾注
  4. Git Hook 防绕过机制安装
  5. Python 打印协议（自动日志 + DNA 追溯）
  6. Docker 容器级主权封装
  7. CI/CD 强制校验
  8. 系统级环境锁定
  9. 跨机器同步配置

用法：
  lh cnsh-env init                # 初始化 CNSH 环境
  lh cnsh-env install-hook        # 安装 Git Hook
  lh cnsh-env create <文件名>     # 创建带尾注的文件
  lh cnsh-env status              # 查看环境状态
  lh cnsh-env lock                # 锁定环境配置
  lh cnsh-env sync                # 跨机器同步
  lh cnsh-env docker              # 生成 Dockerfile
  lh cnsh-env ci                  # 生成 CI 配置
"""

import os
import sys
import json
import subprocess
import datetime
import hashlib
import shutil
import stat
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# ============================================================
# CNSH 统一常量（不可分散）
# ============================================================

class CNSHConstants:
    """CNSH 全局常量（单一源头）"""
    
    # 文化核心
    SYMBOL_DRAGON = "龍"
    SYMBOL_TAIJI = "☯"
    SYMBOL_DNA = "🧬"
    
    # 主权标识
    UID = "UID9622"
    CREATOR = "龍魂体系"
    ENCODING = "UTF-8"
    
    # 审计颜色
    AUDIT_GREEN = "🟢"
    AUDIT_YELLOW = "🟡"
    AUDIT_RED = "🔴"
    AUDIT_STATUS = "🟢"  # 默认
    
    # 版本
    VERSION = "v2.0.0"
    
    # 时间格式
    TIME_FORMAT = "+%Y-%m-%d_%H-%M-%S"
    
    # 确认码
    CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
    SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
    GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

    @classmethod
    def to_env_file(cls) -> str:
        """生成 .env 格式的变量文件"""
        return f'''# ==========================================================
# CNSH 全局环境变量
# VERSION: {cls.VERSION}
# DNA: #龍芯⚡️{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}-CNSH-ENV-UID9622
# ==========================================================

# 文化核心
export CNSH_SYMBOL_DRAGON="{cls.SYMBOL_DRAGON}"
export CNSH_SYMBOL_TAIJI="{cls.SYMBOL_TAIJI}"
export CNSH_SYMBOL_DNA="{cls.SYMBOL_DNA}"

# 主权标识
export CNSH_UID="{cls.UID}"
export CNSH_CREATOR="{cls.CREATOR}"
export CNSH_ENCODING="{cls.ENCODING}"

# 审计颜色
export CNSH_AUDIT_GREEN="{cls.AUDIT_GREEN}"
export CNSH_AUDIT_YELLOW="{cls.AUDIT_YELLOW}"
export CNSH_AUDIT_RED="{cls.AUDIT_RED}"
export CNSH_AUDIT_STATUS="{cls.AUDIT_STATUS}"

# 版本
export CNSH_VERSION="{cls.VERSION}"

# 时间格式
export CNSH_TIME_FORMAT="{cls.TIME_FORMAT}"

# 固定锚点
export CNSH_CONFIRM="{cls.CONFIRM}"
export CNSH_SEAL="{cls.SEAL}"
export CNSH_GPG="{cls.GPG}"

# ==========================================================
'''

    @classmethod
    def to_python_module(cls) -> str:
        """生成 Python 常量模块"""
        return f'''# -*- coding: utf-8 -*-
"""
🐉 CNSH 全局常量模块
DNA: #龍芯⚡️{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}-CNSH-CONST-UID9622
"""

# 文化核心
SYMBOL_DRAGON = "{cls.SYMBOL_DRAGON}"
SYMBOL_TAIJI = "{cls.SYMBOL_TAIJI}"
SYMBOL_DNA = "{cls.SYMBOL_DNA}"

# 主权标识
UID = "{cls.UID}"
CREATOR = "{cls.CREATOR}"
ENCODING = "{cls.ENCODING}"

# 审计颜色
AUDIT_GREEN = "{cls.AUDIT_GREEN}"
AUDIT_YELLOW = "{cls.AUDIT_YELLOW}"
AUDIT_RED = "{cls.AUDIT_RED}"
AUDIT_STATUS = "{cls.AUDIT_STATUS}"

# 版本
VERSION = "{cls.VERSION}"

# 固定锚点
CONFIRM = "{cls.CONFIRM}"
SEAL = "{cls.SEAL}"
GPG = "{cls.GPG}"

# 默认尾注模板
FOOTER_TEMPLATE = """
---
# ==========================================================
# {{SYMBOL_DRAGON}} CNSH 文件主权尾注
# ==========================================================
# UID: {{UID}}
# CREATOR: {{CREATOR}}
# VERSION: {{VERSION}}
# ENCODING: {{ENCODING}}
# CREATED_AT: {{CREATED_AT}}
# AUDIT_STATUS: {{AUDIT_STATUS}}
# SYMBOL: {{SYMBOL_TAIJI}}
# DNA: {{SYMBOL_DNA}}-{{DNA_HASH}}
# CONFIRM: {{CONFIRM}}
# SEAL: {{SEAL}}
# GPG: {{GPG}}
# ==========================================================
"""
'''

# ============================================================
# 核心引擎
# ============================================================

class CNSHEnvironment:
    """CNSH 环境管理器"""

    def __init__(self, root_path: Path = None):
        self.root = root_path or Path.home() / "longhun-system"
        self.config_dir = self.root / ".cnsh"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.constants = CNSHConstants()
        self._loaded = False

    # ============================================================
    # 1. 初始化环境
    # ============================================================

    def init_environment(self) -> Dict:
        """初始化 CNSH 环境"""
        results = {}

        # 1.1 生成环境变量文件
        env_path = self.root / "cnsh_env.sh"
        env_path.write_text(self.constants.to_env_file(), encoding='utf-8')
        env_path.chmod(0o755)
        results["env_file"] = str(env_path)

        # 1.2 生成 Python 常量模块
        py_path = self.root / "cnsh_constants.py"
        py_path.write_text(self.constants.to_python_module(), encoding='utf-8')
        results["py_module"] = str(py_path)

        # 1.3 生成 ZSH 提示符
        zsh_path = self.root / "cnsh_prompt.zsh"
        zsh_path.write_text(self._generate_zsh_prompt(), encoding='utf-8')
        zsh_path.chmod(0o755)
        results["zsh_prompt"] = str(zsh_path)

        # 1.4 生成文件创建脚本
        create_path = self.root / "cnsh_create.sh"
        create_path.write_text(self._generate_create_script(), encoding='utf-8')
        create_path.chmod(0o755)
        results["create_script"] = str(create_path)

        # 1.5 更新 .zshrc
        zshrc_updated = self._update_zshrc()
        results["zshrc_updated"] = zshrc_updated

        # 1.6 生成打印模块
        print_path = self.generate_print_module()
        results["print_module"] = str(print_path)

        self._loaded = True
        return results

    def _generate_zsh_prompt(self) -> str:
        """生成 ZSH 提示符脚本"""
        return f'''# ==========================================================
# CNSH ZSH 提示符
# VERSION: {self.constants.VERSION}
# ==========================================================

# 引入环境变量
source ~/longhun-system/cnsh_env.sh

# 动态标题（含卦象）
precmd() {{
    local CURRENT_PATH=${{PWD/#$HOME/~}}
    local SHORT_PATH=$(echo $CURRENT_PATH | awk -F/ '{{OFS="·"; n=NF; if(n>3) print $(n-2),$(n-1),$n; else print $0}}')

    local HOUR=$(date +%H)
    local GUA_SYMBOL

    case $HOUR in
        23|00|01) GUA_SYMBOL="☷" ;;
        02|03|04) GUA_SYMBOL="☳" ;;
        05|06|07) GUA_SYMBOL="☲" ;;
        08|09|10) GUA_SYMBOL="☴" ;;
        11|12|13) GUA_SYMBOL="☰" ;;
        14|15|16) GUA_SYMBOL="☵" ;;
        17|18|19) GUA_SYMBOL="☶" ;;
        20|21|22) GUA_SYMBOL="☱" ;;
        *) GUA_SYMBOL="$CNSH_SYMBOL_TAIJI" ;;
    esac

    echo -ne "\\e]0;${{CNSH_SYMBOL_DRAGON}} ${{SHORT_PATH}} ${{GUA_SYMBOL}} ${{CNSH_AUDIT_STATUS}}\\a"
}}

# 提示符
PROMPT="%F{{red}}${{CNSH_SYMBOL_DRAGON}}%f %F{{cyan}}%~%f ${{CNSH_SYMBOL_TAIJI}} ${{CNSH_AUDIT_STATUS}} %# "
'''

    def _generate_create_script(self) -> str:
        """生成文件创建脚本"""
        return f'''#!/bin/bash
# ==========================================================
# CNSH 文件创建器
# VERSION: {self.constants.VERSION}
# ==========================================================

source ~/longhun-system/cnsh_env.sh

create_cnsh_file() {{
    local FILE_NAME="$1"

    if [ -z "$FILE_NAME" ]; then
        echo "文件名不能为空"
        return 1
    fi

    touch "$FILE_NAME"

    local NOW=$(date "$CNSH_TIME_FORMAT")
    local DNA_HASH=$(echo "$FILE_NAME$NOW" | sha256sum | cut -c1-8)

    cat <<EOF >> "$FILE_NAME"

---
# ==========================================================
# $CNSH_SYMBOL_DRAGON CNSH 文件主权尾注
# ==========================================================
# UID: $CNSH_UID
# CREATOR: $CNSH_CREATOR
# VERSION: $CNSH_VERSION
# ENCODING: $CNSH_ENCODING
# CREATED_AT: $NOW
# AUDIT_STATUS: $CNSH_AUDIT_STATUS
# SYMBOL: $CNSH_SYMBOL_TAIJI
# DNA: $CNSH_SYMBOL_DNA-$DNA_HASH
# CONFIRM: $CNSH_CONFIRM
# SEAL: $CNSH_SEAL
# GPG: $CNSH_GPG
# ==========================================================
EOF

    echo "✅ 已创建 CNSH 文件: $FILE_NAME"
}}

# 导出为别名
alias create="create_cnsh_file"
'''

    def _update_zshrc(self) -> bool:
        """更新 .zshrc"""
        zshrc = Path.home() / ".zshrc"
        if not zshrc.exists():
            return False

        content = zshrc.read_text(encoding='utf-8')
        if "CNSH 环境加载" in content:
            return True

        lines_to_add = [
            "",
            "# ==========================================================",
            "# CNSH 环境加载",
            "source ~/longhun-system/cnsh_env.sh",
            "source ~/longhun-system/cnsh_prompt.zsh",
            "# ==========================================================",
        ]

        with open(zshrc, 'a', encoding='utf-8') as f:
            f.write("\n".join(lines_to_add) + "\n")
        return True

    # ============================================================
    # 2. Git Hook 安装
    # ============================================================

    def install_git_hook(self) -> Dict:
        """安装 Git pre-commit Hook"""
        hook_dir = self.root / ".git" / "hooks"
        hook_dir.mkdir(parents=True, exist_ok=True)

        hook_path = hook_dir / "pre-commit"
        backup = None

        # 备份现有 hook
        if hook_path.exists():
            backup_path = hook_path.with_suffix(".bak")
            shutil.copy2(hook_path, backup_path)
            backup = str(backup_path)

        hook_content = self._generate_pre_commit_hook()
        hook_path.write_text(hook_content, encoding='utf-8')
        hook_path.chmod(0o755)

        return {"hook_path": str(hook_path), "backup": backup}

    def _generate_pre_commit_hook(self) -> str:
        """生成 pre-commit hook"""
        return f'''#!/bin/bash
# ==========================================================
# CNSH Git Hook
# VERSION: {self.constants.VERSION}
# 防绕过：任何文件缺少主权尾注 → 拒绝提交
# ==========================================================

CNSH_FOOTER_MARKER="CNSH 文件主权尾注"

echo "🔍 CNSH 审计: 检查提交文件..."

for file in $(git diff --cached --name-only); do
    if [ ! -f "$file" ]; then
        continue
    fi
    if grep -q "$CNSH_FOOTER_MARKER" "$file" 2>/dev/null; then
        echo "  ✔ CNSH 校验通过: $file"
    else
        echo "  ✘ CNSH 校验失败: $file 未包含主权尾注"
        echo ""
        echo "请先运行: create $file"
        echo "或添加主权尾注后重新提交"
        exit 1
    fi
done

echo "✅ 所有文件 CNSH 校验通过"
'''

    # ============================================================
    # 3. 文件创建（带尾注）
    # ============================================================

    def create_file(self, filename: str, content: str = "") -> Dict:
        """创建带 CNSH 尾注的文件"""
        file_path = Path(filename)
        if not file_path.is_absolute():
            file_path = Path.cwd() / file_path

        # 生成 DNA 哈希
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        dna_hash = hashlib.sha256(f"{filename}{now}".encode()).hexdigest()[:8]

        # 构建尾注
        footer = f'''
---
# ==========================================================
# {self.constants.SYMBOL_DRAGON} CNSH 文件主权尾注
# ==========================================================
# UID: {self.constants.UID}
# CREATOR: {self.constants.CREATOR}
# VERSION: {self.constants.VERSION}
# ENCODING: {self.constants.ENCODING}
# CREATED_AT: {now}
# AUDIT_STATUS: {self.constants.AUDIT_STATUS}
# SYMBOL: {self.constants.SYMBOL_TAIJI}
# DNA: {self.constants.SYMBOL_DNA}-{dna_hash}
# CONFIRM: {self.constants.CONFIRM}
# SEAL: {self.constants.SEAL}
# GPG: {self.constants.GPG}
# ==========================================================
'''

        # 写入文件
        if file_path.exists():
            existing = file_path.read_text(encoding='utf-8', errors='ignore')
            if "CNSH 文件主权尾注" in existing:
                return {"status": "exists", "path": str(file_path), "message": "文件已包含尾注"}

        with open(file_path, 'w', encoding='utf-8') as f:
            if content:
                f.write(content)
                if not content.endswith('\n'):
                    f.write('\n')
            f.write(footer)

        return {"status": "created", "path": str(file_path), "dna": f"{self.constants.SYMBOL_DNA}-{dna_hash}"}

    # ============================================================
    # 4. Python 打印协议
    # ============================================================

    def generate_print_module(self) -> Path:
        """生成 CNSH 打印模块"""
        content = self._generate_print_code()
        path = self.root / "cnsh_print.py"
        path.write_text(content, encoding='utf-8')
        path.chmod(0o755)
        return path

    def _generate_print_code(self) -> str:
        """生成打印协议代码"""
        return f'''# -*- coding: utf-8 -*-
"""
🐉 CNSH 打印协议 v{self.constants.VERSION}
DNA: #龍芯⚡️{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}-CNSH-PRINT-UID9622
"""

import sys
import datetime
import os
import hashlib

from cnsh_constants import *

CNSH_LOG_FILE = os.environ.get("CNSH_LOG_FILE", "龍魂打印迹.log")

def 打印(文本, 审计状态: str = None):
    """CNSH 标准打印函数，自动记录日志和DNA"""
    if not 文本:
        raise ValueError("输入不能为空")

    当前时间 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dna_hash = hashlib.sha256(f"{{文本}}{{当前时间}}".encode()).hexdigest()[:8]
    audit = 审计状态 or AUDIT_STATUS

    输出内容 = f"{{SYMBOL_DRAGON}} {{文本}} {{SYMBOL_TAIJI}} [{{audit}}]"

    sys.stdout.write(输出内容 + "\\n")
    sys.stdout.flush()

    with open(CNSH_LOG_FILE, "a", encoding="utf-8") as 日志:
        日志.write(f"{{当前时间}} {{SYMBOL_DNA}}-{{dna_hash}} {{输出内容}}\\n")

    return {{"status": audit, "dna": f"{{SYMBOL_DNA}}-{{dna_hash}}", "time": 当前时间}}

def 打印_审计(文本, 审计颜色: str = None):
    """带审计颜色的打印"""
    colors = {{
        "🟢": "通过",
        "🟡": "待审",
        "🔴": "熔断"
    }}
    color = 审计颜色 or AUDIT_STATUS
    return 打印(f"[{{colors.get(color, color)}}] {{文本}}", color)

if __name__ == "__main__":
    打印("你好，龍魂")
'''

    # ============================================================
    # 5. 环境锁定
    # ============================================================

    def lock_environment(self) -> Dict:
        """锁定环境配置"""
        lock_file = self.config_dir / "environment.lock"
        lock_data = {
            "version": self.constants.VERSION,
            "timestamp": datetime.datetime.now().isoformat(),
            "uid": self.constants.UID,
            "checksums": self._compute_checksums(),
            "locked_by": os.environ.get("USER", "unknown")
        }
        lock_file.write_text(json.dumps(lock_data, indent=2, ensure_ascii=False), encoding='utf-8')
        return lock_data

    def _compute_checksums(self) -> Dict:
        """计算关键文件的校验和"""
        checksums = {}
        for f in ["cnsh_env.sh", "cnsh_prompt.zsh", "cnsh_create.sh", "cnsh_print.py", "cnsh_constants.py"]:
            path = self.root / f
            if path.exists():
                checksums[f] = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
        return checksums

    # ============================================================
    # 6. 跨机器同步
    # ============================================================

    def sync_environment(self, target_host: str) -> Dict:
        """跨机器同步 CNSH 环境"""
        sync_script = self.root / "cnsh_sync.sh"
        sync_content = f'''#!/bin/bash
# CNSH 跨机器同步脚本
# 目标: {target_host}

echo "🔄 CNSH 环境同步到 {target_host}..."

rsync -avz \\
    ~/longhun-system/cnsh_env.sh \\
    ~/longhun-system/cnsh_prompt.zsh \\
    ~/longhun-system/cnsh_create.sh \\
    ~/longhun-system/cnsh_print.py \\
    ~/longhun-system/cnsh_constants.py \\
    {target_host}:~/longhun-system/

echo "✅ 同步完成"
'''
        sync_script.write_text(sync_content, encoding='utf-8')
        sync_script.chmod(0o755)

        return {"sync_script": str(sync_script), "target": target_host}

    # ============================================================
    # 7. Docker 封装
    # ============================================================

    def generate_dockerfile(self) -> Path:
        """生成 Dockerfile"""
        content = f'''FROM python:3.11-slim

# CNSH 环境变量
ENV CNSH_UID="{self.constants.UID}"
ENV CNSH_CREATOR="{self.constants.CREATOR}"
ENV CNSH_VERSION="{self.constants.VERSION}"
ENV CNSH_ENCODING="{self.constants.ENCODING}"
ENV CNSH_AUDIT_STATUS="{self.constants.AUDIT_STATUS}"

# 安装依赖
RUN apt-get update && apt-get install -y \\
    git \\
    vim \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# 复制 CNSH 文件
COPY cnsh_*.sh /usr/local/bin/
COPY cnsh_*.py /usr/local/bin/
RUN chmod +x /usr/local/bin/cnsh_*.sh

# 设置工作目录
WORKDIR /workspace

# 默认命令
CMD ["/bin/bash"]
'''
        path = self.root / "Dockerfile.cnsh"
        path.write_text(content, encoding='utf-8')
        return path

    # ============================================================
    # 8. CI/CD 配置
    # ============================================================

    def generate_ci_config(self) -> Path:
        """生成 CI/CD 配置"""
        content = f'''# ==========================================================
# CNSH CI/CD 配置
# VERSION: {self.constants.VERSION}
# ==========================================================

name: CNSH CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup CNSH Environment
        run: |
          source cnsh_env.sh
          echo "CNSH_UID=$CNSH_UID" >> $GITHUB_ENV
      
      - name: Validate CNSH Footer
        run: |
          for file in $(find . -name "*.md" -o -name "*.py" -o -name "*.sh"); do
            if ! grep -q "CNSH 文件主权尾注" "$file"; then
              echo "❌ $file 缺少 CNSH 尾注"
              exit 1
            fi
          done
          echo "✅ 所有文件 CNSH 校验通过"
      
      - name: Run CNSH Tests
        run: |
          python3 cnsh_print.py
          echo "✅ CNSH 测试通过"
'''
        path = self.root / ".github" / "workflows" / "cnsh_ci.yml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return path

    # ============================================================
    # 9. 状态查看
    # ============================================================

    def get_status(self) -> Dict:
        """查看 CNSH 环境状态"""
        status = {
            "version": self.constants.VERSION,
            "uid": self.constants.UID,
            "audit_status": self.constants.AUDIT_STATUS,
            "files": {}
        }

        for name in ["cnsh_env.sh", "cnsh_prompt.zsh", "cnsh_create.sh", "cnsh_print.py", "cnsh_constants.py"]:
            path = self.root / name
            status["files"][name] = {
                "exists": path.exists(),
                "path": str(path) if path.exists() else None
            }

        # 检查 Git Hook
        hook_path = self.root / ".git" / "hooks" / "pre-commit"
        status["git_hook"] = {
            "installed": hook_path.exists(),
            "path": str(hook_path) if hook_path.exists() else None
        }

        # 检查 Dockerfile
        docker_path = self.root / "Dockerfile.cnsh"
        status["docker"] = {
            "exists": docker_path.exists(),
            "path": str(docker_path) if docker_path.exists() else None
        }

        # 检查 CI 配置
        ci_path = self.root / ".github" / "workflows" / "cnsh_ci.yml"
        status["ci"] = {
            "exists": ci_path.exists(),
            "path": str(ci_path) if ci_path.exists() else None
        }

        # 检查锁定
        lock_file = self.config_dir / "environment.lock"
        if lock_file.exists():
            status["locked"] = json.loads(lock_file.read_text(encoding='utf-8'))

        return status

# ============================================================
# CLI
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="🐉 CNSH 环境集成引擎 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
子命令:
  init           初始化 CNSH 环境（生成所有配置文件和常量）
  install-hook   安装 Git pre-commit Hook（防绕过机制）
  create         创建带主权尾注的文件
  status         查看 CNSH 环境状态
  lock           锁定环境配置（生成校验和快照）
  sync           生成跨机器同步脚本
  docker         生成 Dockerfile（容器级主权封装）
  ci             生成 CI/CD 配置（GitHub Actions）

示例:
  lh cnsh-env init
  lh cnsh-env install-hook
  lh cnsh-env create 我的文件.md --content "# 标题"
  lh cnsh-env status
  lh cnsh-env lock
  lh cnsh-env sync --target root@119.13.90.27
  lh cnsh-env docker
  lh cnsh-env ci
        """
    )
    
    parser.add_argument("command", nargs="?", 
                        choices=["init", "install-hook", "create", "status", "lock", "sync", "docker", "ci"],
                        help="子命令")
    parser.add_argument("filename", nargs="?", help="文件名（用于 create）")
    parser.add_argument("--content", "-c", help="文件内容（用于 create）")
    parser.add_argument("--target", "-t", help="同步目标（用于 sync）")
    
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    env = CNSHEnvironment()

    if args.command == "init":
        result = env.init_environment()
        print("\n✅ CNSH 环境初始化完成\n")
        print("生成文件：")
        for k, v in result.items():
            if k != "zshrc_updated":
                print(f"  📄 {k}: {v}")
        if result.get("zshrc_updated"):
            print(f"  🔧 .zshrc: 已添加 CNSH 加载指令")
        print(f"\n请运行: source ~/longhun-system/cnsh_env.sh")

    elif args.command == "install-hook":
        result = env.install_git_hook()
        print(f"\n✅ Git Hook 已安装: {result['hook_path']}")
        if result.get('backup'):
            print(f"  📦 原 hook 已备份: {result['backup']}")

    elif args.command == "create":
        if not args.filename:
            print("❌ 请指定文件名: lh cnsh-env create <文件名>")
            return
        result = env.create_file(args.filename, args.content or "")
        if result.get("status") == "exists":
            print(f"⏭️ {result['message']}: {result['path']}")
        else:
            print(f"✅ 文件已创建: {result['path']}")
            print(f"  DNA: {result.get('dna')}")

    elif args.command == "status":
        status = env.get_status()
        print("\n📊 CNSH 环境状态")
        print(f"  版本: {status['version']}")
        print(f"  UID: {status['uid']}")
        print(f"  审计状态: {status['audit_status']}")
        print("\n  核心文件:")
        for name, info in status['files'].items():
            print(f"    {'✅' if info['exists'] else '❌'} {name}")
        print(f"\n  Git Hook: {'✅ 已安装' if status['git_hook']['installed'] else '❌ 未安装'}")
        print(f"  Dockerfile: {'✅ 已生成' if status.get('docker', {}).get('exists') else '❌ 未生成'}")
        print(f"  CI 配置: {'✅ 已生成' if status.get('ci', {}).get('exists') else '❌ 未生成'}")
        if status.get('locked'):
            print(f"\n  锁定状态: 🔒 已锁定")
            print(f"    锁定人: {status['locked'].get('locked_by', '未知')}")
            print(f"    锁定时间: {status['locked'].get('timestamp', '未知')}")

    elif args.command == "lock":
        result = env.lock_environment()
        print(f"\n🔒 环境已锁定")
        print(f"  版本: {result['version']}")
        print(f"  时间: {result['timestamp']}")
        print(f"  用户: {result['locked_by']}")
        print(f"  校验和: {len(result.get('checksums', {}))} 个文件")

    elif args.command == "sync":
        target = args.target or input("请输入目标主机 (如 root@119.13.90.27): ")
        if not target:
            print("❌ 目标主机不能为空")
            return
        result = env.sync_environment(target)
        print(f"\n✅ 同步脚本已生成: {result['sync_script']}")
        print(f"  目标: {result['target']}")
        print(f"  执行: bash {result['sync_script']}")

    elif args.command == "docker":
        path = env.generate_dockerfile()
        print(f"\n✅ Dockerfile 已生成: {path}")
        print("  构建命令: docker build -f Dockerfile.cnsh -t cnsh-env .")
        print("  运行命令: docker run -it cnsh-env")

    elif args.command == "ci":
        path = env.generate_ci_config()
        print(f"\n✅ CI 配置已生成: {path}")
        print("  将推送到 GitHub 后自动生效")

if __name__ == "__main__":
    main()
