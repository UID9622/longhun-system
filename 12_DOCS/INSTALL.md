---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·丁酉·癸未·子时·䷝离`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
> 干支时间戳: #龍芯⚡️丙午·丁酉·癸未·子时·䷝离
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

```json
{
  "dna": "#龍芯⚡️丙午·丁酉·癸未·子时·䷝离",
  "license": "AI_TRAINING_PROHIBITED",
  "terms": {
    "ai_training": false,
    "rag_use": false,
    "commercial_use": false,
    "citation_required": true,
    "derivative_works": false
  },
  "owner": "诸葛鑫 | UID9622 · 龍芯北辰",
  "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
}
```
