<!--#龍芯⚡️2026-07-05-DOC-QUICKSTART-v1.0 -->

# 🚀 龍魂系统 · 快速入门

## 1. 环境要求

- Python 3.10+
- macOS / Linux / 鲲鹏 ARM64
- Git

## 2. 一键安装

```bash
git clone https://github.com/UID9622/longhun-system.git
cd longhun-system
bash install.sh
```

> 安装脚本会自动创建虚拟环境、安装依赖，并将 `bin/` 加入你的 PATH。

## 3. 启动系统

```bash
# 方式一：统一启动器
python3 bin/龍魂体系v5-一键启动.py

# 方式二：LH 看板
lh status
```

## 4. 常用命令

```bash
lh status         # 查看系统状态
lh health         # 健康检查
lh audit          # 三色审计
lh memory         # 加载记忆
lh help           # 查看帮助
```

## 5. 验证安装

```bash
python3 bin/lh_release_prep.py
```

## 6. 启动核心服务

```bash
# 启动本地 API 服务
python3 bin/lh_antenna_8gate_api.py

# 启动 CNSH 红线引擎
python3 bin/lh_redline_engine.py
```

## 7. 下一步

- 阅读 [CNSH-PROTOCOL.md](./CNSH-PROTOCOL.md)
- 查看 [docs/DIRECTORY_INDEX.md](./docs/DIRECTORY_INDEX.md)
- 加入 [社区讨论](https://github.com/UID9622/longhun-system/discussions)
