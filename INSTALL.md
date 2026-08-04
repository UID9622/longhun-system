# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统 · 安装指南

> DNA: `#龍芯⚡️20260731-INSTALL-v1.0-UID9622`
> 最后更新: 2026-07-31

---

## 环境要求

| 依赖 | 最低版本 | 说明 |
|:---|:---|:---|
| Python | 3.11+ | 核心运行环境 |
| pip | 23.0+ | 包管理器 |
| Git | 2.30+ | 克隆仓库 |
| Redis | 6.0+ | 可选，异步API模式需要 |
| Docker | 24.0+ | 可选，容器部署 |

---

## 安装方式

### 方式一：一键安装（推荐 · Linux/macOS/鲲鹏）

```bash
# 克隆仓库
git clone https://github.com/UID9622/longhun-system.git
cd longhun-system

# 运行安装脚本
bash bin/install.sh
```

安装脚本自动完成：
1. 检测 Python 版本（>= 3.11）
2. 创建虚拟环境（`.venv/`）
3. 安装 Python 依赖（`pip install -r requirements.txt`）
4. 配置 `.env` 文件
5. 注册 `lh` 命令到 PATH
6. 验证安装（`lh --help`）

### 方式二：手动安装

```bash
# 1. 克隆仓库
git clone https://github.com/UID9622/longhun-system.git
cd longhun-system

# 2. 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境（可选）
cp .env.example .env
# 编辑 .env 填入你的配置

# 5. 设置 lh 别名
echo 'alias lh="python3 ~/longhun-system/bin/lh.py"' >> ~/.bashrc
source ~/.bashrc

# 6. 验证
lh --help
```

### 方式三：Windows

#### PowerShell
```powershell
# 以管理员身份运行
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\bin\install.ps1
```

#### CMD
```cmd
bin\install.bat
```

Windows 手动安装：
```powershell
# 1. 克隆仓库
git clone https://github.com/UID9622/longhun-system.git
cd longhun-system

# 2. 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置
copy .env.example .env

# 5. 验证
python bin\lh.py --help
```

### 方式四：Docker 部署

```bash
# 启动 API 服务 + Redis + Worker
docker-compose -f docker/docker-compose.api.yml up -d

# 查看日志
docker-compose -f docker/docker-compose.api.yml logs -f

# 停止
docker-compose -f docker/docker-compose.api.yml down
```

---

## 安装后验证

```bash
# 检查 lh 命令
lh --help

# 健康检查
lh health

# 查看系统状态
lh status

# 启动 API 服务（测试）
lh --api --port 9622
# 另一个终端测试
curl http://localhost:9622/health
```

---

## 常见问题

### Q1: `lh: command not found`
重新加载 shell 配置：
```bash
source ~/.bashrc    # bash
source ~/.zshrc     # zsh
```
或直接使用完整路径：
```bash
python3 ~/longhun-system/bin/lh.py
```

### Q2: `ModuleNotFoundError: No module named 'xxx'`
确保在虚拟环境中：
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Q3: Python 版本过低
macOS:
```bash
brew install python@3.11
```
Ubuntu/Debian:
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.11 python3.11-venv
```

### Q4: 鲲鹏服务器连接失败
检查 SSH 密钥和网络连通性：
```bash
ssh -i ~/.ssh/longhun_kunpeng_ed25519 root@119.13.90.27
```

### Q5: Docker 容器无法启动
```bash
# 检查端口占用
lsof -i :9622

# 查看详细日志
docker-compose -f docker/docker-compose.api.yml logs
```

### Q6: pip install 报权限错误
```bash
# 使用虚拟环境（推荐）
python3 -m venv .venv && source .venv/bin/activate

# 或使用 --user
pip install --user -r requirements.txt
```

---

## 卸载

```bash
# 删除虚拟环境
rm -rf .venv/

# 删除 lh 别名（编辑 ~/.bashrc 或 ~/.zshrc）

# 删除项目目录
cd .. && rm -rf longhun-system/
```

---

## 下一步

- [快速入门](./QUICKSTART.md) — 5分钟上手
- [API文档](./docs/API.md) — API使用指南
- [开发者文档](./docs/DEVELOPMENT.md) — 开发环境搭建
- [架构文档](./docs/ARCHITECTURE.md) — 系统架构

---

> 🐉 **装完就跑起。主权在你自己手里。**
