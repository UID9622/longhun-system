# 🐉 龍魂系统 · 手把手部署教程

> **DNA**: `#龍芯⚡️丙午·乙未·癸未·戌时-手把手教程-v2.0`
> **适用**: 全平台 · UID9622 及所有龍魂生态用户
> **级别**: L1 · 教程文档
> **最后更新**: 2026-07-12

---

## 目录

1. [一、选择你的平台](#一选择你的平台)
2. [二、环境准备](#二环境准备)
3. [三、拉代码 + 装依赖](#三拉代码--装依赖)
4. [四、配置 API 密钥](#四配置-api-密钥)
5. [五、注册 DNA（身份锚定）](#五注册-dna身份锚定)
6. [六、创建生态通行证](#六创建生态通行证)
7. [七、用 DeepSeek 修复代码](#七用-deepseek-修复代码)
8. [八、CNSH 闸门审查](#八cnsh-闸门审查)
9. [九、CodeBuddy 联动](#九codebuddy-联动)
10. [十、完整链路示例](#十完整链路示例)
11. [十一、常用命令速查](#十一常用命令速查)
12. [附录：DNA头部模板 + 故障排查](#附录-adna头部模板直接复制)

---

## 一、选择你的平台

| 平台 | 章节 | 难度 |
|------|------|:---:|
| macOS (Intel / Apple Silicon) | [二-A](#二-a--macos) | ⭐ |
| Windows 10/11 | [二-B](#二-b--windows-1011) | ⭐⭐ |
| Linux (Ubuntu/Debian) | [二-C](#二-c--linux-ubuntudebian) | ⭐ |
| Linux (华为欧拉 openEuler) | [二-D](#二-d--华为欧拉-openeuler) | ⭐⭐ |
| 鸿蒙 HarmonyOS (手机/平板) | [二-E](#二-e--鸿蒙-harmonyos-手机平板) | ⭐⭐⭐ |
| 鸿蒙 PC 版 | [二-F](#二-f--鸿蒙-pc-版) | ⭐⭐ |

---

## 二、环境准备

### 二-A · macOS

#### 你需要的
| 序号 | 东西 | 检查命令 |
|:---:|------|------|
| 1 | Python 3.10+ | `python3 --version` |
| 2 | Git | `git --version` |
| 3 | DeepSeek API Key | [platform.deepseek.com](https://platform.deepseek.com) 申请 |
| 4 | CodeBuddy 编辑器 | IDE，联动目标 |
| 5 | GPG 密钥（推荐） | `gpg --version` |

#### 安装
```bash
# 安装 Homebrew（如果没有）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Python 3.12
brew install python@3.12

# 安装 Git
brew install git

# 安装 GPG
brew install gnupg

# 生成 GPG 密钥
gpg --full-generate-key
# → 选 RSA and RSA (default)
# → 4096 bit
# → 设过期时间（建议 2y）
# → 填名字 + 邮箱
# → 记下生成的 40 位指纹！
```

---

### 二-B · Windows 10/11

#### 你需要的
| 序号 | 东西 | 怎么搞 |
|:---:|------|------|
| 1 | Python 3.10+ | [python.org](https://python.org/downloads/) 下载安装包 |
| 2 | Git for Windows | [git-scm.com](https://git-scm.com/download/win) 下载 |
| 3 | DeepSeek API Key | [platform.deepseek.com](https://platform.deepseek.com) 申请 |
| 4 | CodeBuddy 编辑器 | IDE，联动目标 |
| 5 | GPG（可选） | Git for Windows 自带或装 Gpg4win |

#### 安装步骤

**Python：**
1. 去 https://python.org/downloads/ 下载 Python 3.12.x Windows installer (64-bit)
2. 运行安装程序，**勾选 ☑ Add Python to PATH**
3. 点 Install Now，等装完
4. 打开 **PowerShell**（Win+R → 输入 `powershell` → 回车），验证：
```powershell
python --version
# 输出: Python 3.12.x
```

**Git：**
1. 去 https://git-scm.com/download/win 下载 64-bit Git for Windows Setup
2. 一路 Next，默认选项即可
3. 验证：
```powershell
git --version
# 输出: git version 2.x.x
```

**GPG（可选）：**
```powershell
# Git for Windows 自带 gpg，直接验证
gpg --version
# 如果没有，下载 Gpg4win: https://gpg4win.org/

# 生成密钥
gpg --full-generate-key
```

---

### 二-C · Linux (Ubuntu/Debian)

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Python 3.12
sudo apt install -y python3 python3-pip python3-venv

# 安装 Git
sudo apt install -y git

# 安装 GPG
sudo apt install -y gnupg

# 验证
python3 --version
git --version
gpg --version

# 生成 GPG 密钥
gpg --full-generate-key
```

---

### 二-D · 华为欧拉 openEuler

> 华为欧拉（openEuler）是华为自研 Linux 发行版，鲲鹏/昇腾服务器常用。
> 包管理器是 `dnf`（类似 CentOS/Fedora）。

```bash
# 更新系统
sudo dnf update -y

# 安装 Python 3.12
sudo dnf install -y python3 python3-pip python3-devel

# 安装 Git
sudo dnf install -y git

# 安装 GPG
sudo dnf install -y gnupg2

# 验证
python3 --version
git --version
gpg --version

# 如果 Python 版本 < 3.10，需要手动编译安装：
# sudo dnf install -y gcc openssl-devel bzip2-devel libffi-devel
# cd /tmp
# wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz
# tar xzf Python-3.12.0.tgz
# cd Python-3.12.0
# ./configure --enable-optimizations
# make -j$(nproc)
# sudo make altinstall
# python3.12 --version

# 生成 GPG 密钥
gpg --full-generate-key
```

---

### 二-E · 鸿蒙 HarmonyOS (手机/平板)

> 鸿蒙手机/平板不能直接跑 Python 脚本，但可以通过 **Termux** 或 **云服务器** 两种方式使用龍魂。

#### 方式一：Termux（推荐·本地跑）

**1. 安装 Termux**
- 鸿蒙应用市场搜 "Termux" 安装
- 或去 [F-Droid](https://f-droid.org/packages/com.termux/) 下载 APK 手动安装
- ⚠️ 鸿蒙 Next (5.0) 可能不兼容，用方式二

**2. Termux 内安装环境**
```bash
# 更新 Termux
pkg update && pkg upgrade -y

# 安装 Python + Git
pkg install -y python git openssh gnupg

# 验证
python --version
git --version

# 拉代码
cd ~
git clone https://github.com/UID9622/longhun-system.git
cd longhun-system

# 装依赖
pip install -r requirements.txt
```

**3. Termux 内配置 API**
```bash
# 设置 DeepSeek API Key
echo 'export DEEPSEEK_API_KEY="sk-你的密钥"' >> ~/.bashrc
source ~/.bashrc

# 注意：Termux 没有 ~/.zshrc，用 ~/.bashrc
```

#### 方式二：云服务器（推荐·稳定）

在云服务器上部署龍魂，鸿蒙设备通过 SSH 连接使用。

```bash
# 在云服务器（openEuler/Ubuntu 等）上按 [二-C] 或 [二-D] 部署
# 然后在鸿蒙设备上安装 SSH 客户端：

# Termius（推荐）: 鸿蒙应用市场搜 "Termius"
# JuiceSSH: 搜 "JuiceSSH"
# 连接后即可使用龍魂全部命令
```

---

### 二-F · 鸿蒙 PC 版

> 鸿蒙 PC 版（HarmonyOS PC）支持 DevEco Studio + 终端。

```bash
# 1. 打开终端（从 DevEco Studio 或系统终端）
# 2. 检查 Python（鸿蒙 PC 可能自带或需手动装）
python3 --version

# 如果没有 Python：
# 方式A: 通过包管理器（如果有）
# sudo pkg install python3

# 方式B: 手动编译（参考 openEuler 编译步骤）
# 鸿蒙 PC 内核基于 Linux，编译方式与 openEuler 类似

# 3. 安装 Git
# 鸿蒙 PC 可能不自带 Git
# 从 https://git-scm.com/download/linux 下载源码编译
# 或用包管理器: sudo pkg install git

# 4. 后续步骤与 Linux 一致
cd ~
git clone https://github.com/UID9622/longhun-system.git
cd longhun-system
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 三、拉代码 + 装依赖

### 全平台通用（选一个仓库源）

```bash
# GitHub（主力·推荐）
git clone https://github.com/UID9622/longhun-system.git

# Gitee（国内·速度快）
git clone https://gitee.com/UID9622/longhun-system.git

# GitCode（华为云·国内）
git clone https://gitcode.com/UID9622/longhun-system.git

cd longhun-system
```

### 虚拟环境（macOS / Linux / 鸿蒙 PC / Termux）

```bash
python3 -m venv venv
source venv/bin/activate     # macOS/Linux/鸿蒙PC/Termux
```

### 虚拟环境（Windows PowerShell）

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
# 如果报错"无法加载文件"，先执行：
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 虚拟环境（Windows CMD）

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### 装依赖（全平台统一）

```bash
pip install -r requirements.txt
```

### 验证安装

```bash
# 应输出帮助信息
python3 bin/lh_deepseek_fixer.py
# 输出: 🧬 龍魂·DeepSeek 修复引擎 v1.0

python3 bin/cnsh_gatekeeper.py
# 输出: 🧬 龍魂·CNSH 合规闸门
```

---

## 四、配置 API 密钥

### macOS / Linux / 鸿蒙PC

```bash
# 设置 DeepSeek API Key
export DEEPSEEK_API_KEY="sk-你的DeepSeek密钥"

# 写入配置文件（每次开终端自动加载）
echo 'export DEEPSEEK_API_KEY="sk-你的DeepSeek密钥"' >> ~/.zshrc
source ~/.zshrc

# 如果用 bash（Termux / 部分 Linux）
echo 'export DEEPSEEK_API_KEY="sk-你的DeepSeek密钥"' >> ~/.bashrc
source ~/.bashrc
```

### Windows PowerShell

```powershell
# 临时设置（当前窗口有效）
$env:DEEPSEEK_API_KEY="sk-你的DeepSeek密钥"

# 永久设置（每次开 PowerShell 自动加载）
[Environment]::SetEnvironmentVariable("DEEPSEEK_API_KEY", "sk-你的DeepSeek密钥", "User")

# 验证
echo $env:DEEPSEEK_API_KEY
```

### Windows CMD

```cmd
set DEEPSEEK_API_KEY=sk-你的DeepSeek密钥
:: 永久设置：
setx DEEPSEEK_API_KEY "sk-你的DeepSeek密钥"
```

### Kimi API（可选·联动用）

```bash
# macOS/Linux
export KIMI_API_KEY="sk-kimi-你的Kimi密钥"

# Windows PowerShell
$env:KIMI_API_KEY="sk-kimi-你的Kimi密钥"
```

---

## 五、注册 DNA（身份锚定）

> DNA = 你的身份锚定串。唯一标识，绑物理资产 + 虚拟身份。
> 格式：`#龍芯⚡️<年干支>·<月干支>·<日干支>·<时辰>·<卦名>-<模块名>-<版本>`

### 第一步：注册统一 DNA

```bash
# 进入项目目录
cd ~/longhun-system     # macOS/Linux/鸿蒙PC
# 或 cd %USERPROFILE%\longhun-system   # Windows

# 注册资产（可多次执行，UID 用你的标识）

# 注册 GPG 密钥
python3 bin/lh_unified_dna_registry.py register uid9622 gpg "你的GPG指纹40位" "主密钥"

# 注册代码仓库
python3 bin/lh_unified_dna_registry.py register uid9622 repo "https://github.com/xxx/longhun-system" "主仓库"

# 查看你的 DNA 清单
python3 bin/lh_unified_dna_registry.py list uid9622

# 查看 DNA 总体状态
python3 bin/lh_unified_dna_registry.py status uid9622

# 生成主 DNA 哈希（公开用，不泄露原始数据）
python3 bin/lh_unified_dna_registry.py master uid9622
```

### 第二步：记录 DNA 到登记册

```bash
python3 bin/lh_dna_registry.py \
  --register "#龍芯⚡️丙午·乙未·癸未·戌时·YOUR-MODULE-v1.0" \
  --type CREATE \
  --target "你的文件.py"
```

### DNA 格式说明

| 格式 | 示例 | 用途 |
|------|------|------|
| v1.0 格里历 | `#龍芯⚡️2026-07-12-DEEPSEEK-FIXER-v1.0` | 日常开发 |
| v∞ 干支时辰 | `#龍芯⚡️丙午·乙未·癸未·戌时·䷾既济-YOUR-MODULE-v1.0` | 核心模块 |
| 紧凑格式 | `#龍芯⚡️丙午·戌时·䷾-YOUR-MODULE-v1.0` | 快速标记 |

**⚠️ 你自己写的文件必须带 DNA 头部，否则闸门过不了。**

---

## 六、创建生态通行证

```bash
# 创建通行证
python3 bin/lh_ecosystem_passport.py passport create uid9622

# 查看通行证状态
python3 bin/lh_ecosystem_passport.py passport show uid9622

# 生成 API 密钥
python3 bin/lh_ecosystem_passport.py apikey generate uid9622
# 记下生成的 API Key！

# 查看所有 API 密钥
python3 bin/lh_ecosystem_passport.py apikey list uid9622
```

### 层级说明

| 层级 | Emoji | 获取方式 | 权限 |
|------|:---:|------|------|
| 免费 free | 🆓 | DNA 注册自动获得 | 基础 API，限速 |
| 基础 basic | ⭐ | 身份认证通过 | 标准 API，优先队列 |
| 专业 pro | 🌟 | GPG + 代码贡献 | 高级功能，批量 API |
| 创始人 founder | 👑 | UID9622 专属 | 全功能，投票权 |

---

## 七、用 DeepSeek 修复代码

### 什么时候用

- 代码报类型错误（basedpyright 检查）
- 语法错误
- CNSH 中文关键字对齐

### 四种模式

```bash
# 全量修复（类型 + 语法 + CNSH 对齐）
python3 bin/lh_deepseek_fixer.py bin/你的文件.py full

# 只修复类型错误
python3 bin/lh_deepseek_fixer.py bin/你的文件.py type_error

# 只修复语法错误
python3 bin/lh_deepseek_fixer.py bin/你的文件.py syntax

# CNSH 中文语法对齐
python3 bin/lh_deepseek_fixer.py bin/你的文件.py cnsh_align
```

### 自动修复流程

```
你的命令
  ↓
① 读取文件
  ↓
② basedpyright 提取错误
  ↓
③ 构建错误描述 → 发给 DeepSeek API
  ↓
④ DeepSeek 返回修复结果
  ↓
⑤ 提取代码块 → 备份原文件（.backup）
  ↓
⑥ 写入修复代码
  ↓
⑦ 语法验证
  ↓
⑧ CNSH 闸门审查（自动）
  ↓
⑨ CodeBuddy 联动刷新
```

### 关键参数

```bash
# 跳过闸门审查（仅调试用！不要在生产环境用）
python3 bin/lh_deepseek_fixer.py bin/你的文件.py full --skip-gate

# 指定 API Key（覆盖环境变量）
# macOS/Linux:
DEEPSEEK_API_KEY="sk-xxx" python3 bin/lh_deepseek_fixer.py bin/你的文件.py full

# Windows CMD:
set DEEPSEEK_API_KEY=sk-xxx && python bin/lh_deepseek_fixer.py bin/你的文件.py full
```

---

## 八、CNSH 闸门审查

### 闸门是什么

CNSH 闸门 = 代码入库前的最后一道门。焊死·不可跳过。

检查 8 项：
1. DNA 追溯码 — 必须有
2. CONFIRM 确认码 — P0/L0 级模块必须有
3. 三色审计状态 — 必须声明
4. GPG 签名 — 核心文件必须
5. 中文关键字 — 变量/函数名用中文
6. 变量前缀 — L0/L1 用 `龍_` 前缀
7. 繁简归一 — `龍` 繁体为规范
8. 不删除原则 — 禁止 `rm -rf` 等

### 手动审查

```bash
# 审查单个文件
python3 bin/cnsh_gatekeeper.py check --file bin/你的文件.py

# 审查整个目录
python3 bin/cnsh_gatekeeper.py check --dir bin/

# 审查并自动修复简单问题
python3 bin/cnsh_gatekeeper.py fix --file bin/你的文件.py
```

### 闸门结果解读

| 结果 | 含义 | 操作 |
|------|------|------|
| 🟢 通过 | 全部合规 | 入库 |
| 🟡 警告 | 有小问题（如英文变量名） | 可入库，建议修复 |
| 🔴 拒绝 | 严重违规（缺DNA/含删除操作） | 禁止入库，必须修复 |

---

## 九、CodeBuddy 联动

### 联动机制

```
你修改文件
    ↓
CodeBuddy 自动检测文件变化
    ↓
CodeBuddy 重新加载文件
    ↓
类型检查（basedpyright）自动运行
    ↓
错误显示在编辑器里
```

### DeepSeek 修复后自动联动

`lh_deepseek_fixer.py` 修复完成后会自动：

1. 写入触发文件（路径因平台而异）
2. CodeBuddy 检测到触发文件 → 重新加载修复后的文件
3. basedpyright 重新检查 → 错误消失或减少

```bash
# macOS/Linux/鸿蒙PC 查看触发文件
cat ~/.龍魂/.codebuddy_trigger

# Windows PowerShell 查看触发文件
type $env:USERPROFILE\.龍魂\.codebuddy_trigger
```

### 手动触发刷新

```bash
# macOS/Linux/鸿蒙PC/Termux
python3 -c "
import json, time
from pathlib import Path
触发 = Path.home() / '.龍魂' / '.codebuddy_trigger'
触发.parent.mkdir(parents=True, exist_ok=True)
触发.write_text(json.dumps({
    'action': 'reload',
    'file': 'bin/你的文件.py',
    'timestamp': time.time(),
    'source': 'manual',
}, ensure_ascii=False, indent=2))
print('触发信号已发送')
"
```

---

## 十、完整链路示例

### 场景：你写了一个新 Python 脚本，要入库

#### Step 1: 写好代码 + DNA 头部

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ═══════════════════════════════════════════
# 龍魂体系 | 你的模块名
# ═══════════════════════════════════════════
# DNA: #龍芯⚡️丙午·乙未·癸未·戌时·YOUR-MODULE-v1.0
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬YOUR-CODE
# 创建者：你的名字
# 三色审计状态：🟢 通过
# ═══════════════════════════════════════════
"""

def 你的函数():
    pass
```

#### Step 2: 过闸门

```bash
python3 bin/cnsh_gatekeeper.py check --file bin/你的文件.py
# 🟢 通过 → 继续
# 🔴 拒绝 → 修到通过为止
```

#### Step 3: 有类型错误就调 DeepSeek 修

```bash
python3 bin/lh_deepseek_fixer.py bin/你的文件.py full
```

#### Step 4: 注册 DNA 到登记册

```bash
python3 bin/lh_dna_registry.py \
  --register "#龍芯⚡️丙午·乙未·癸未·戌时·YOUR-MODULE-v1.0" \
  --type CREATE \
  --target "bin/你的文件.py"
```

#### Step 5: 提交到 Git

```bash
git add bin/你的文件.py
git commit -m "feat: 你的功能描述"
git push
```

### 完整链路图

```
写代码
  ↓
加 DNA 头部（必须）
  ↓
CNSH 闸门审查 ← 不通过 → 修代码
  ↓ 🟢 通过
DeepSeek 修复（可选·有类型错误时） ← 修复失败 → 人工介入
  ↓ ✅
闸门再审查（自动）
  ↓ 🟢
DNA 登记册记录
  ↓
CodeBuddy 刷新
  ↓
Git 提交
```

---

## 十一、常用命令速查

### 全平台通用命令（Windows 把 `python3` 换成 `python`）

```bash
# ═══ DNA 相关 ═══

# 注册统一 DNA
python3 bin/lh_unified_dna_registry.py register uid9622 <资产类型> <资产编号> [标签]

# 查看 DNA 清单
python3 bin/lh_unified_dna_registry.py list uid9622

# 查看 DNA 状态
python3 bin/lh_unified_dna_registry.py status uid9622

# 查看登记册最近 N 条
python3 bin/lh_dna_registry.py --recent 20

# 查询特定 DNA
python3 bin/lh_dna_registry.py --query "#龍芯⚡️2026-07-12"

# 登记册统计
python3 bin/lh_dna_registry.py --stats

# ═══ 通行证相关 ═══

python3 bin/lh_ecosystem_passport.py passport create uid9622
python3 bin/lh_ecosystem_passport.py passport show uid9622
python3 bin/lh_ecosystem_passport.py apikey generate uid9622
python3 bin/lh_ecosystem_passport.py apikey list uid9622

# ═══ 修复相关 ═══

python3 bin/lh_deepseek_fixer.py <文件路径> full
python3 bin/lh_deepseek_fixer.py <文件路径> type_error
python3 bin/lh_deepseek_fixer.py <文件路径> syntax
python3 bin/lh_deepseek_fixer.py <文件路径> cnsh_align

# ═══ 闸门相关 ═══

python3 bin/cnsh_gatekeeper.py check --file <文件路径>
python3 bin/cnsh_gatekeeper.py check --dir <目录路径>
python3 bin/cnsh_gatekeeper.py fix --file <文件路径>

# ═══ 推送 ═══

# 推送到所有远端（GitHub + Gitee + GitCode）
bash bin/lh_push_all.sh
```

---

## 附录 A：DNA 头部模板（直接复制）

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ═══════════════════════════════════════════
# 龍魂体系 | 模块名称
# ═══════════════════════════════════════════
# ENCODING: UTF-8
# DNA追溯码(v∞): #龍芯⚡️[年干支]·[月干支]·[日干支]·[时辰]·[卦名]-[模块名]-[版本]
# DNA追溯码(v1.0): #龍芯⚡️YYYY-MM-DD-[模块名]-[版本]
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬[你的4位码]-[3位码]
# 创建者：你的名字（UID）
# 权重级别：L0/L1/L2/L3...
# 三色审计状态：🟢/🟡/🔴
# GPG指纹：你的40位GPG指纹
# ═══════════════════════════════════════════
"""
```

## 附录 B：各平台快速对照

| 操作 | macOS | Windows | Linux/openEuler | 鸿蒙/Termux |
|------|-------|---------|-----------------|-------------|
| 包管理器 | `brew` | 手动下载 | `apt` / `dnf` | `pkg` |
| Python | `brew install python@3.12` | 官网下载安装包 | `apt/dnf install python3` | `pkg install python` |
| Git | `brew install git` | 官网下载 | `apt/dnf install git` | `pkg install git` |
| 虚拟环境 | `source venv/bin/activate` | `venv\Scripts\activate` | 同 macOS | 同 macOS |
| 环境变量 | `export KEY=val` | `$env:KEY="val"` | 同 macOS | 同 macOS |
| 配置文件 | `~/.zshrc` | 系统环境变量 | `~/.bashrc` | `~/.bashrc` |
| 触发文件 | `~/.龍魂/` | `%USERPROFILE%\.龍魂\` | 同 macOS | `~/.龍魂/` |

## 附录 C：故障排查

| 问题 | 平台 | 原因 | 解决 |
|------|------|------|------|
| DeepSeek API 报错 | 全部 | 密钥未设或过期 | `echo $DEEPSEEK_API_KEY` 检查 |
| 闸门一直🔴拒绝 | 全部 | 缺DNA头部或含删除操作 | 加DNA头部，移除`rm -rf` |
| 修复后代码更差 | 全部 | DeepSeek 没理解上下文 | 分小块修，不用 full |
| CodeBuddy 不刷新 | 全部 | 触发文件未写入 | 手动写 `~/.龍魂/.codebuddy_trigger` |
| `python3: command not found` | Linux | Python未装或叫`python` | `sudo apt/dnf install python3` |
| `pip: command not found` | Windows | 安装时没勾Add to PATH | 重装Python并勾选 |
| Termux 装不了包 | 鸿蒙 | 网络问题 | `termux-change-repo` 换镜像 |
| GPG 生成密钥卡住 | 全部 | 需要随机熵 | 随机敲键盘/移动鼠标 |
| Git clone 超时 | 全部（国内） | GitHub 被墙 | 换 Gitee 源 |

---

**总结一句话：写代码 → 加DNA头 → 过闸门 → 有错调DeepSeek修 → 再闸门 → 登记册 → 提交。**
