#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂开源发布包准备器
用途：整理、验证、打包 longhun-system 开源发行版
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-RELEASE-PREP-v1.0
"""

import os
import re
import sys
import json
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set, Tuple

ROOT = Path.home() / "longhun-system"
DIST_DIR = ROOT / "dist"
RELEASE_NAME = f"longhun-system-v5.0.0-opensource"
RELEASE_DIR = DIST_DIR / RELEASE_NAME
ZIP_PATH = DIST_DIR / f"{RELEASE_NAME}.zip"
ASC_PATH = DIST_DIR / f"{RELEASE_NAME}.zip.asc"
REPORT_PATH = DIST_DIR / f"{RELEASE_NAME}-report.json"

# ═══════════════════════════════════════════════════════════
# 开源包白名单（根目录级）
# ═══════════════════════════════════════════════════════════
INCLUDE_TOP_DIRS: Set[str] = {
    "01_protocols",
    "agents",
    "bin",
    "brand",
    "capabilities",
    "cnsh",
    "config",
    "deploy",
    "docs",
    "engines",
    "governance",
    "harmony",
    "knowledge",
    "personas",
    "portal",
    "scripts",
    "services",
    "state",
    "tests",
    "tools",
    "web",
}

INCLUDE_ROOT_FILES: Set[str] = {
    "README.md",
    "AGENTS.md",
    "CONSTITUTION.md",
    "LICENSE",
    "__init__.py",
    "lh_public_key.asc",
}

# 排除规则（即使在上面的目录里，也跳过）
EXCLUDE_PATTERNS: List[str] = [
    "_private",
    "_archive",
    "_work",
    ".git",
    ".longhun",
    ".codebuddy",
    ".vscode",
    ".pytest_cache",
    "__pycache__",
    "*.pyc",
    "*.pyo",
    "*.log",
    "*.pid",
    "*.tmp",
    "*.temp",
    ".DS_Store",
    "Thumbs.db",
    "node_modules",
    ".venv",
    "venv",
    "backups",
    "releases",
    "L7_数据层",
    "models/base_models_v4.0",        # 大权重
    "models/checkpoints",             # 训练检查点
    "models/evaluation",              # 评测大文件
    "models/longhun-v1.0",            # 旧大模型
    "models/training",                # 训练数据（可能大）
    "brain",
    "data",                           # 数据目录（按需）
    "logs",
    "output",
    "voice-twin/raw",
    "voice-twin/voice_dataset",
    "container_data",
    # --- 运行时/私有/遗留 ---
    "knowledge/ai-chats",             # 原始 AI 对话记录，含个人上下文
    "tools/bin/legacy_bin",           # 遗留工具，大量硬编码本地路径
    "agents/daemon_logs",
    "agents/daemon_state.json",
    "agents/daemon.pid",
    "agents/downloads-imports",
]

# README 中必须存在且存在文件系统的引用路径
README_REQUIRED_PATHS: List[str] = [
    "QUICKSTART.md",
    "CONTRIBUTING.md",
    "docs/DIRECTORY_INDEX.md",
    "CONSTITUTION.md",
    "AGENTS.md",
    "CODE_OF_CONDUCT.md",
    "install.sh",
    "bin/龍魂体系v5-一键启动.py",
]

# 收款码文件（相对根目录）
SUPPORT_IMAGES: List[str] = [
    "portal/browser-historian/support-alipay-ecny.jpg",
    "portal/browser-historian/support-wechat.jpg",
    "portal/browser-historian/support-ecny.jpg",
]

SUPPORT_SECTION = """
---

## 🍜 此路同行 · 支持龍魂

> **不是乞讨，是在茫茫数字荒原上，立下一塊路碑。**
> **同行者，自會相認。**

龍魂系统从一人一笔一键盘开始，所有核心代码、协议、训练数据均自主可控。
如果你认同「技术服务于人民，主权不可交易」，欢迎用一杯咖啡支持我们继续走下去。

| 微信支付 | 支付宝 | 数字人民币 |
|:---:|:---:|:---:|
| ![微信收款码](./portal/browser-historian/support-wechat.jpg) | ![支付宝收款码](./portal/browser-historian/support-alipay-ecny.jpg) | ![数字人民币收款码](./portal/browser-historian/support-ecny.jpg) |

**每一笔支持都会进入龍魂公共账本，全部用于：**
- 服务器与带宽（鲲鹏 / 华为云）
- CNSH 中文编程语言持续迭代
- 老百姓数字主权教育内容生产

**主权不灭，此路同行。**

*Technology serves the people. Sovereignty is not for sale.*
"""


# ═══════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════
def log(msg: str, level: str = "INFO"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] [{level}] {msg}")


def should_exclude(rel_path: Path) -> bool:
    """根据排除规则判断相对路径是否应被排除"""
    parts = rel_path.parts
    s = str(rel_path).replace("\\", "/")

    # 目录名/文件名级排除
    for part in parts:
        if part in {"__pycache__", ".git", "_private", "_archive", "_work", ".longhun", ".codebuddy", ".vscode", ".pytest_cache", "node_modules", ".venv", "venv", "backups", "releases", "brain", "data", "logs", "output", "container_data"}:
            return True
        if part.endswith(".pyc") or part.endswith(".pyo") or part.endswith(".log") or part.endswith(".pid") or part.endswith(".tmp"):
            return True

    # 模式级排除
    for pat in EXCLUDE_PATTERNS:
        if pat in s:
            return True
    if ".DS_Store" in s or "Thumbs.db" in s:
        return True
    if "voice-twin/raw" in s or "voice-twin/voice_dataset" in s:
        return True

    return False


def collect_files() -> List[Path]:
    """收集所有应进入开源包的文件（相对 ROOT 的 Path）"""
    files: List[Path] = []

    # 根目录文件
    for f in ROOT.iterdir():
        if f.is_file() and f.name in INCLUDE_ROOT_FILES:
            files.append(f.relative_to(ROOT))

    # 白名单目录
    for dirname in INCLUDE_TOP_DIRS:
        d = ROOT / dirname
        if not d.exists():
            log(f"目录不存在，跳过: {dirname}", "WARN")
            continue
        for p in d.rglob("*"):
            if p.is_file():
                rel = p.relative_to(ROOT)
                if not should_exclude(rel):
                    files.append(rel)

    return sorted(set(files))


def validate_python_syntax(files: List[Path]) -> List[str]:
    """对所有 .py 文件跑 py_compile，返回失败的相对路径列表"""
    failures: List[str] = []
    py_files = [f for f in files if str(f).endswith(".py")]
    log(f"开始验证 {len(py_files)} 个 Python 文件...")

    for rel in py_files:
        src = ROOT / rel
        try:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(src)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode != 0:
                failures.append(str(rel))
                log(f"Python 语法错误: {rel}", "ERROR")
                if result.stderr:
                    for line in result.stderr.strip().splitlines()[:3]:
                        log(f"  {line}", "ERROR")
        except Exception as e:
            failures.append(str(rel))
            log(f"验证异常 {rel}: {e}", "ERROR")

    return failures


def validate_shell_syntax(files: List[Path]) -> List[str]:
    """对所有 .sh 文件跑 bash -n，返回失败的相对路径列表"""
    failures: List[str] = []
    sh_files = [f for f in files if str(f).endswith(".sh")]
    log(f"开始验证 {len(sh_files)} 个 Shell 文件...")

    for rel in sh_files:
        src = ROOT / rel
        try:
            result = subprocess.run(
                ["bash", "-n", str(src)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode != 0:
                failures.append(str(rel))
                log(f"Shell 语法错误: {rel}", "ERROR")
                if result.stderr:
                    for line in result.stderr.strip().splitlines()[:3]:
                        log(f"  {line}", "ERROR")
        except Exception as e:
            failures.append(str(rel))
            log(f"验证异常 {rel}: {e}", "ERROR")

    return failures


def check_readme_links() -> Tuple[List[str], List[str]]:
    """检查 README 中引用的路径是否存在；返回 (缺失路径, 存在的路径)"""
    readme = ROOT / "README.md"
    if not readme.exists():
        return README_REQUIRED_PATHS, []

    content = readme.read_text(encoding="utf-8")
    missing = []
    exists = []
    for path in README_REQUIRED_PATHS:
        if (ROOT / path).exists():
            exists.append(path)
        else:
            # 如果 README 文本里没引用，也不算缺失（但我们的要求里是要存在的）
            missing.append(path)
    return missing, exists


def ensure_support_images_in_readme():
    """确保 README 底部有收款码区块"""
    readme = ROOT / "README.md"
    content = readme.read_text(encoding="utf-8")

    # 检查是否已经存在
    if "此路同行" in content or "support-wechat.jpg" in content:
        log("README 已包含收款码区块，跳过插入")
        return

    # 检查收款码文件是否真实存在
    exist_imgs = [img for img in SUPPORT_IMAGES if (ROOT / img).exists()]
    if not exist_imgs:
        log("收款码图片不存在，无法插入", "WARN")
        return

    content = content.rstrip() + "\n" + SUPPORT_SECTION
    readme.write_text(content, encoding="utf-8")
    log("已在 README 底部插入收款码区块")


def generate_missing_docs(missing_paths: List[str]):
    """生成 README 需要的缺失文档"""
    for path in missing_paths:
        target = ROOT / path
        target.parent.mkdir(parents=True, exist_ok=True)

        if path == "QUICKSTART.md":
            target.write_text(_QUICKSTART_MD, encoding="utf-8")
            log(f"已生成: {path}")
        elif path == "CONTRIBUTING.md":
            target.write_text(_CONTRIBUTING_MD, encoding="utf-8")
            log(f"已生成: {path}")
        elif path == "docs/DIRECTORY_INDEX.md":
            target.write_text(_DIRECTORY_INDEX_MD, encoding="utf-8")
            log(f"已生成: {path}")
        elif path == "CODE_OF_CONDUCT.md":
            target.write_text(_CODE_OF_CONDUCT_MD, encoding="utf-8")
            log(f"已生成: {path}")
        elif path == "install.sh":
            target.write_text(_INSTALL_SH, encoding="utf-8")
            target.chmod(0o755)
            log(f"已生成: {path}")
        elif path == "CNSH-PROTOCOL.md":
            target.write_text(_CNSH_PROTOCOL_MD, encoding="utf-8")
            log(f"已生成: {path}")


def generate_directory_index():
    """如果 docs/DIRECTORY_INDEX.md 已生成或已存在，则追加真实目录扫描"""
    target = ROOT / "docs/DIRECTORY_INDEX.md"
    if not target.exists():
        return

    # 扫描真实目录，生成模块列表
    sections = []
    scan_dirs = [
        ("01_protocols", "协议层"),
        ("bin", "可执行脚本"),
        ("engines", "核心引擎"),
        ("portal", "Web 门户"),
        ("services", "后台服务"),
        ("deploy", "部署脚本"),
        ("cnsh", "CNSH 语言"),
        ("governance", "治理层"),
        ("tests", "测试"),
    ]

    rows = []
    for dirname, label in scan_dirs:
        d = ROOT / dirname
        if not d.exists():
            continue
        count = len(list(d.rglob("*")))
        rows.append(f"| [{dirname}](./../{dirname}/) | {label} | {count} 项 |")

    dynamic = "\n\n## 📂 真实目录扫描\n\n| 目录 | 说明 | 规模 |\n|------|------|------|\n" + "\n".join(rows) + "\n"

    content = target.read_text(encoding="utf-8")
    if "真实目录扫描" not in content:
        content = content.rstrip() + dynamic
        target.write_text(content, encoding="utf-8")
        log("已更新 docs/DIRECTORY_INDEX.md 真实目录扫描")


def copy_files_to_release(files: List[Path]):
    """把文件复制到 RELEASE_DIR"""
    if RELEASE_DIR.exists():
        shutil.rmtree(RELEASE_DIR)
    RELEASE_DIR.mkdir(parents=True, exist_ok=True)

    for rel in files:
        src = ROOT / rel
        dst = RELEASE_DIR / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    log(f"已复制 {len(files)} 个文件到 {RELEASE_DIR}")


def create_zip():
    """打包成 zip"""
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()

    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(RELEASE_DIR):
            for f in files:
                full = Path(root) / f
                arcname = full.relative_to(RELEASE_DIR)
                zf.write(full, arcname)

    size_mb = ZIP_PATH.stat().st_size / (1024 * 1024)
    log(f"已生成压缩包: {ZIP_PATH} ({size_mb:.2f} MB)")


def gpg_sign() -> bool:
    """用 GPG 对 zip 签名（非交互 batch 模式）"""
    try:
        result = subprocess.run(
            ["gpg", "--batch", "--yes", "--armor", "--detach-sign", "--output", str(ASC_PATH), str(ZIP_PATH)],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode == 0:
            log(f"已生成 GPG 签名: {ASC_PATH}")
            return True
        else:
            log(f"GPG 签名失败: {result.stderr}", "WARN")
            return False
    except Exception as e:
        log(f"GPG 签名异常: {e}", "WARN")
        return False


HASH_PATH = DIST_DIR / f"{RELEASE_NAME}.sha256"


def sha256_checksum() -> bool:
    """生成 SHA256 校验文件"""
    try:
        result = subprocess.run(
            ["shasum", "-a", "256", str(ZIP_PATH)],
            capture_output=True,
            text=True,
            timeout=30,
            check=True,
        )
        HASH_PATH.write_text(result.stdout, encoding="utf-8")
        log(f"已生成 SHA256 校验: {HASH_PATH}")
        return True
    except Exception as e:
        log(f"SHA256 校验生成失败: {e}", "WARN")
        return False


def setup_nginx_download():
    """在本地 nginx 配置 /download/ 路径"""
    # 先找站点级配置（如 uid9622.cn.conf），再找主配置
    site_candidates = [
        Path("/opt/homebrew/etc/nginx/servers/uid9622.cn.conf"),
        Path("/usr/local/etc/nginx/servers/uid9622.cn.conf"),
        Path("/etc/nginx/conf.d/uid9622.cn.conf"),
    ]
    main_candidates = [
        Path("/opt/homebrew/etc/nginx/nginx.conf"),
        Path("/usr/local/etc/nginx/nginx.conf"),
        Path("/etc/nginx/nginx.conf"),
    ]

    nginx_conf = None
    for c in site_candidates:
        if c.exists():
            nginx_conf = c
            break
    if not nginx_conf:
        for c in main_candidates:
            if c.exists():
                nginx_conf = c
                break

    if not nginx_conf:
        log("未找到 nginx.conf，跳过本地下载配置", "WARN")
        return False

    content = nginx_conf.read_text(encoding="utf-8")
    marker = "location /download/"
    if marker in content:
        log("nginx 已配置 /download/，跳过")
        return True

    block = f"""
    # ── 开源发布包下载 ──
    location /download/ {{
        alias {DIST_DIR}/;
        autoindex on;
        add_header Cache-Control "public, max-age=3600";
    }}
"""
    # 在 HTTP server 块的最后一个 location /api/ 或 location / 之后插入
    # 简单策略：在最后一个 `}` 之前插入（假设是 server 块结尾）
    content = content.rstrip()
    last_brace = content.rfind("}")
    if last_brace > 0:
        content = content[:last_brace] + block + content[last_brace:] + "\n"
    else:
        content = content + block

    # 备份并写入
    backup = nginx_conf.with_suffix(".conf.bak.release")
    shutil.copy2(nginx_conf, backup)
    nginx_conf.write_text(content, encoding="utf-8")
    log(f"已更新 nginx 配置: {nginx_conf}（备份: {backup}）")

    # 尝试 reload
    try:
        subprocess.run(["nginx", "-t"], check=True, capture_output=True, timeout=30)
        subprocess.run(["nginx", "-s", "reload"], check=True, capture_output=True, timeout=30)
        log("nginx 测试并重载成功")
        return True
    except Exception as e:
        log(f"nginx 重载失败，请手动检查: {e}", "WARN")
        return False


def try_sync_kunpeng() -> Tuple[bool, str]:
    """尝试同步到鲲鹏服务器"""
    host = "119.13.90.27"
    try:
        result = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=5", "-o", "BatchMode=yes", f"root@{host}", "echo ok"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return False, f"SSH 无法连接: {result.stderr.strip() or result.stdout.strip()}"
    except Exception as e:
        return False, f"SSH 探测异常: {e}"

    try:
        remote_dir = "/opt/longhun-system/dist"
        subprocess.run(
            ["ssh", f"root@{host}", f"mkdir -p {remote_dir}"],
            check=True, capture_output=True, timeout=30,
        )
        subprocess.run(
            ["scp", "-o", "ConnectTimeout=10", str(ZIP_PATH), str(ASC_PATH), f"root@{host}:{remote_dir}/"],
            check=True, capture_output=True, timeout=120,
        )
        return True, f"已同步到 {host}:{remote_dir}"
    except Exception as e:
        return False, f"同步失败: {e}"


# ═══════════════════════════════════════════════════════════
# 缺失文档模板
# ═══════════════════════════════════════════════════════════
_QUICKSTART_MD = """<!--#龍芯⚡️2026-07-05-DOC-QUICKSTART-v1.0 -->

# 🚀 龍魂系统 · 快速入门

## 1. 环境要求

- Python 3.10+
- macOS / Linux / 鲲鹏 ARM64
- Git

## 2. 一键安装

```bash
bash install.sh
```

## 3. 启动系统

```bash
python3 bin/龍魂体系v5-一键启动.py
```

## 4. 常用命令

```bash
lh status         # 查看状态
lh start          # 启动服务
lh stop           # 停止服务
lh health         # 健康检查
```

## 5. 验证安装

```bash
python3 bin/lh_delivery_validator.py --self-test
```

## 6. 下一步

- 阅读 [CNSH-PROTOCOL.md](./CNSH-PROTOCOL.md)
- 查看 [docs/DIRECTORY_INDEX.md](./docs/DIRECTORY_INDEX.md)
- 加入 [社区讨论](https://github.com/UID9622/longhun-system/discussions)
"""

_CONTRIBUTING_MD = """<!--#龍芯⚡️2026-07-05-DOC-CONTRIBUTING-v1.0 -->

# 🤝 参与贡献

## 贡献前必读

1. 阅读 [CONSTITUTION.md](./CONSTITUTION.md) — 系统宪法不可违背。
2. 阅读 [AGENTS.md](./AGENTS.md) — AI 操作手册。
3. 所有提交必须通过三色审计：🟢通过 / 🟡警告 / 🔴拒绝。

## 贡献流程

1. Fork 本仓库
2. 在 `features/` 或 `fixes/` 分支工作
3. 提交前运行 `python3 bin/lh_delivery_validator.py --self-test`
4. 提交 PR，描述改动点和审计结果

## 禁止事项

- 上传私有密钥、密码、个人数据
- 引入未经审计的闭源依赖
- 修改系统宪法和零号协议

## 联系

- Discussions: https://github.com/UID9622/longhun-system/discussions
"""

_DIRECTORY_INDEX_MD = """<!--#龍芯⚡️2026-07-05-DOC-DIRECTORY-INDEX-v1.0 -->

# 📂 龍魂系统 · 目录导航

> 快速找到你要的东西。

## 📚 核心文档

| 文件 | 内容 |
|------|------|
| [README.md](../README.md) | 系统介绍 |
| [QUICKSTART.md](../QUICKSTART.md) | 5分钟上手 |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | 贡献指南 |
| [CONSTITUTION.md](../CONSTITUTION.md) | 系统宪法 |
| [AGENTS.md](../AGENTS.md) | AI 操作手册 |
| [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) | 行为准则 |

## 🔧 快速入口

| 目录 | 说明 |
|------|------|
| [bin/](../bin/) | 可执行脚本 |
| [engines/](../engines/) | 核心引擎 |
| [portal/](../portal/) | Web 门户 |
| [services/](../services/) | 后台服务 |
| [tests/](../tests/) | 测试 |

*(本文件由 release-prep 自动生成并追加真实目录扫描)*
"""

_CODE_OF_CONDUCT_MD = """<!--#龍芯⚡️2026-07-05-DOC-CODE-OF-CONDUCT-v1.0 -->

# 🛡️ 行为准则

## 我们的承诺

龍魂系统致力于为人民服务的数字主权事业。我们欢迎任何认同以下价值观的参与者：

- 技术服务于人民
- 数据主权不可交易
- 透明、可审计、可追责

## 不可接受行为

- 歧视、骚扰、人身攻击
- 传播虚假信息或恶意代码
- 窃取、滥用他人数据
- 破坏系统宪法和红线熔断机制

## 执行机制

违规者将接受三色审计：

- 🟢 警告
- 🟡 临时封禁
- 🔴 永久移除

最终裁决权归创造者 UID9622 所有。
"""

_INSTALL_SH = """#!/bin/bash
# 龍魂系统 · 一键安装脚本
set -e

echo "🐉 龍魂系统安装开始..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 python3，请先安装 Python 3.10+"
    exit 1
fi

PY_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python 版本: $PY_VERSION"

# 创建虚拟环境（可选）
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✅ 虚拟环境已创建"
fi

# 安装依赖
if [ -f "requirements.txt" ]; then
    .venv/bin/pip install -r requirements.txt
elif [ -f "pyproject.toml" ]; then
    .venv/bin/pip install -e .
fi

echo "✅ 依赖安装完成"
echo ""
echo "🚀 启动系统: python3 bin/龍魂体系v5-一键启动.py"
echo "📖 快速入门: cat QUICKSTART.md"
"""

_CNSH_PROTOCOL_MD = """<!--#龍芯⚡️2026-07-05-DOC-CNSH-PROTOCOL-v1.0 -->

# 📝 CNSH 中文原生编程语言 · 规范摘要

> CNSH（Chinese Native Script for Harmony）是龍魂系统的中文母语编程语言。

## 核心思想

- 用中文关键字表达计算意图
- 编译到 Python / JavaScript / Rust / C
- 每条代码必须带 DNA 追溯锚点

## 示例

```cnsl
定义 任务 "生成登录页"
设 风格 为 "暗色鎏金"
则 CodeBuddy 生成 前端页面
最后 审计 代码
```

## 完整规范

完整规范正在 `cnsh/` 目录下持续迭代。请查看：

- `cnsh/spec/`
- `cnsh/runtime/`
- `cnsh/compiler/`

## 设计原则

1. 中文优先
2. 主权不可让渡
3. 所有产出可追溯
4. 红线熔断内建
"""


# ═══════════════════════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════════════════════
def main():
    log("=" * 60)
    log("龍魂开源发布包准备器 v1.0 启动")
    log("=" * 60)

    # 1. 收集文件
    files = collect_files()
    log(f"进入开源包的文件总数: {len(files)}")

    # 2. 语法验证
    py_failures = validate_python_syntax(files)
    sh_failures = validate_shell_syntax(files)

    # 3. README 链接检查 + 补全文档 + 收款码
    missing_links, existing_links = check_readme_links()
    log(f"README 引用检查: 缺失 {len(missing_links)} 个，存在 {len(existing_links)} 个")
    if missing_links:
        log(f"缺失: {', '.join(missing_links)}")
        generate_missing_docs(missing_links)
        # 重新检查
        missing_links, existing_links = check_readme_links()

    ensure_support_images_in_readme()
    generate_directory_index()

    # 4. 重新收集（因为生成了新文件）
    files = collect_files()
    log(f"生成文档后文件总数: {len(files)}")

    # 5. 复制、打包、签名、校验
    copy_files_to_release(files)
    create_zip()
    gpg_ok = gpg_sign()
    sha256_ok = sha256_checksum()

    # 6. nginx 下载路径
    nginx_ok = setup_nginx_download()

    # 7. 尝试同步鲲鹏
    kunpeng_ok, kunpeng_msg = try_sync_kunpeng()
    if not kunpeng_ok:
        log(f"鲲鹏同步: {kunpeng_msg}", "WARN")

    # 8. 生成报告
    report = {
        "version": "v5.0.0",
        "release_name": RELEASE_NAME,
        "generated_at": datetime.now().isoformat(),
        "file_count": len(files),
        "zip_path": str(ZIP_PATH),
        "zip_size_mb": round(ZIP_PATH.stat().st_size / (1024 * 1024), 2),
        "asc_path": str(ASC_PATH) if ASC_PATH.exists() else None,
        "sha256_path": str(HASH_PATH) if HASH_PATH.exists() else None,
        "gpg_signed": gpg_ok,
        "sha256_ok": sha256_ok,
        "nginx_download_ok": nginx_ok,
        "kunpeng_sync_ok": kunpeng_ok,
        "kunpeng_sync_message": kunpeng_msg,
        "python_failures": py_failures,
        "shell_failures": sh_failures,
        "readme_missing_links_after_fix": missing_links,
        "readme_existing_links": existing_links,
        "download_url": "https://uid9622.cn/download/" + ZIP_PATH.name,
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    log(f"报告已生成: {REPORT_PATH}")

    # 9. 汇总
    log("=" * 60)
    log("发布准备完成")
    log(f"压缩包: {ZIP_PATH}")
    log(f"下载链接: {report['download_url']}")
    log(f"Python 语法失败: {len(py_failures)} 个")
    log(f"Shell 语法失败: {len(sh_failures)} 个")
    log(f"README 缺失链接: {len(missing_links)} 个")
    log(f"GPG 签名: {'成功' if gpg_ok else '失败'}")
    log(f"SHA256 校验: {'成功' if sha256_ok else '失败'}")
    log(f"鲲鹏同步: {'成功' if kunpeng_ok else '失败'} - {kunpeng_msg}")
    log("=" * 60)

    if py_failures or sh_failures or missing_links:
        log("存在阻塞问题，请先修复再发布", "ERROR")
        sys.exit(1)

    log("所有检查通过，可以发布")


if __name__ == "__main__":
    main()
