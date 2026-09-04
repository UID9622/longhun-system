# 龍魂系统·安装指南 / Longhun System · Installation Guide

> DNA: #龍芯⚡️2026-09-05-安装指南-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层）· 代码: MulanPSL v2
> 文档版本: v5.2.0
> 三色: 🟢 安装流程 2026-09-05 实测（macOS 原生 + 鲲鹏 aarch64 已跑通）

---

## [中文] 安装指南

### 代码仓库（两条镜像源）

```
# GitHub 主源（P0）
git clone git@github.com:UID9622/longhun-system.git ~/longhun-system
# 或 HTTPS
git clone https://github.com/UID9622/longhun-system.git ~/longhun-system

# GitCode 镜像源（国内加速备用）
git clone git@gitcode.com:UID9622/longhun-system.git ~/longhun-system
```

### macOS 安装（推荐·原生支持）
```bash
# 1) 基础依赖
xcode-select --install
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install git gpg curl jq git-lfs python3 ollama
git lfs install

# 2) Python 依赖
pip3 install pyyaml pytest build twine

# 3) 克隆并验证
git clone git@github.com:UID9622/longhun-system.git ~/longhun-system
cd ~/longhun-system
python3 08_BIN/lh.py health --json     # 预期: {"ok": true, ...} · 22 项引擎检查全过
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update && sudo apt install -y git gpg curl jq git-lfs python3 python3-pip build-essential python3-dev
git lfs install
git clone https://github.com/UID9622/longhun-system.git ~/longhun-system
cd ~/longhun-system && pip3 install pyyaml pytest build twine
python3 08_BIN/lh.py health --json
```

### 🏔️ 鲲鹏 ARM64（华为云·欧拉OS/openEuler · 零适配已跑通）
```bash
uname -m                                # 应输出 aarch64
sudo dnf install -y git gnupg2 curl jq python39 python39-pip git-lfs
git lfs install
git clone https://github.com/UID9622/longhun-system.git ~/longhun-system
cd ~/longhun-system && pip3 install pyyaml pytest build twine
python3 08_BIN/lh.py health --json     # 与 x86 完全一致（纯 Python 天然跨架构）

# 可选: Ollama 本地模型（离线推理）
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull qwen2:7b
```

### Windows (WSL2 推荐)
```powershell
# 管理员 PowerShell
wsl --install -d Ubuntu-22.04
# 重启后在 WSL2 内执行上方 Linux 步骤
```

### 离线模式（可选）
```bash
export LONGHUN_OFFLINE_MODE=1
mkdir -p ~/.longhun/local_store/
python3 08_BIN/lh.py health --json     # 核心功能 100% 可用
```

### 便捷别名（建议）
```bash
echo 'alias lh="python3 ~/longhun-system/08_BIN/lh.py"' >> ~/.zshrc
source ~/.zshrc
lh health --json
```

### 验证安装清单
```bash
python3 -c "import yaml; print('pyyaml OK')"
python3 -c "import pytest; print('pytest OK')"
gpg --list-keys A2D0092CEE2E5BA87035600924C3704A8CC26D5F   # 导入签名公钥
python3 08_BIN/lh.py health --json                          # 22 项引擎全 ✅ = 安装成功
```

---

## [English] Installation Guide

### Repositories
- GitHub: `git clone git@github.com:UID9622/longhun-system.git ~/longhun-system` (P0)
- GitCode mirror: `git clone git@gitcode.com:UID9622/longhun-system.git ~/longhun-system`

### macOS / Linux / Kunpeng-ARM64
```bash
# deps: git gpg curl jq git-lfs python3 (+ pyyaml pytest)  →  git lfs install
# clone → cd → pip3 install pyyaml pytest
python3 08_BIN/lh.py health --json   # expect ok:true, 22 checks green
```
Kunpeng (aarch64 / EulerOS): `sudo dnf install -y git gnupg2 curl jq python39 python39-pip git-lfs` — pure Python = zero ARM64 adaptation (verified on Huawei Cloud Kunpeng).

### Offline Mode
`export LONGHUN_OFFLINE_MODE=1` → all core features run offline; only Notion MCP needs internet (local-Markdown fallback).

---
🐉 2026-09-05 · 丙午年·壬申月·庚戌日 · UID9622 · 🟢
