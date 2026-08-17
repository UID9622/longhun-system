# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
<!-- DNA: #龍芯⚡️2026-07-13-QUICKSTART-v1.0 -->

# 🐉 龍魂系统 · 快速入门

> **5 分钟跑起来。3 步完成第一个功能。**

---

## 前提条件

| 要求 | 版本 |
|------|------|
| Python | ≥ 3.11 |
| pip | ≥ 23.0 |
| Git | 任意 |
| 操作系统 | macOS / Linux (推荐鲲鹏 openEuler) |

---

## 🚀 三步上手

### 第一步：安装

```bash
# 克隆仓库
git clone https://github.com/UID9622/longhun-system.git
cd longhun-system

# 一键安装
bash bin/install.sh
```

安装脚本会自动：
- 创建虚拟环境
- 安装核心依赖
- 验证环境
- 注册 CLI 命令

### 第二步：启动

```bash
# 查看系统状态
lh status

# 一键启动所有服务
python3 bin/龍魂体系v5-一键启动.py

# 或分步启动
lh start
```

### 第三步：验证

```bash
# 三色审计自检
python3 bin/lh_self_heal.py --quick

# MCP Server 测试（让 AI 调用 CNSH 工具）
python3 integrations/mcp/cnsh_syntax_mcp_server.py --test
```

看到 🟢 全部通过 = 跑起来了。

---

## 🧭 接下来看什么

| 你想... | 看这里 |
|---------|--------|
| 了解系统架构 | [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md) |
| 学习 CNSH 语言 | [`CNSH-PROTOCOL.md`](./CNSH-PROTOCOL.md) |
| 找到某个模块 | [`docs/DIRECTORY_INDEX.md`](./docs/DIRECTORY_INDEX.md) |
| 部署到服务器 | [`deploy/scripts/DEPLOY.md`](./deploy/scripts/DEPLOY.md) |
| 参与贡献 | [`CONTRIBUTING.md`](./CONTRIBUTING.md) |
| 了解规则 | [`CONSTITUTION.md`](./CONSTITUTION.md) |

---

## 🛠 常用命令速查

```bash
lh status          # 查看所有服务状态
lh start           # 启动核心服务
lh stop            # 停止所有服务
lh health          # 健康检查
lh audit           # 三色审计扫描
lh dashboard       # 打开收口面板
```

---

## 🐳 Docker 部署（可选）

```bash
docker-compose up -d
```

---

## ❓ 遇到问题？

1. 先看 [GitHub Discussions](https://github.com/UID9622/longhun-system/discussions)
2. 搜索已有的 [Issues](https://github.com/UID9622/longhun-system/issues)
3. 创建新 Issue（选对应模板）

---

> 🐉 一个人建造。逻辑驱动。AI 执行。社区一起看。
