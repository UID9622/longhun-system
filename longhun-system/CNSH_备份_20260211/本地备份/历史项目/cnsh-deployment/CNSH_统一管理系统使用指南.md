# CNSH 统一管理系统使用指南

## 🇨🇳 UID9622 | Made in China • By 诸葛鑫

## 🚀 快速开始

### 安装UID9622终端标识

```bash
cd /Users/zuimeidedeyihan/LuckyCommandCenter/cnsh-deployment
./install-uid9622-banner.sh
source ~/.bashrc  # 或重新打开终端
```

安装后，每次打开终端都会显示：

```
═══════════════════════════════════════════════════════
   🇨🇳  UID9622 系统 | Made in China • By 诸葛鑫
   中国创新 · 世界共享 · 铜墙铁壁
═══════════════════════════════════════════════════════
```

## 🎮 CNSH便捷命令

安装完成后，您可以使用以下便捷命令：

| 命令 | 功能 |
|------|------|
| `cnsh-start` | 启动所有CNSH服务 |
| `cnsh-stop` | 停止所有CNSH服务 |
| `cnsh-restart` | 重启所有CNSH服务 |
| `cnsh-status` | 查看服务状态 |
| `cnsh-logs` | 查看日志 |
| `cnsh-transparency` | 查看UID9622透明声明 |
| `cnsh` | 打开CNSH管理菜单 |

## 🛠️ 系统组件

CNSH统一管理系统包含以下核心组件：

### 1. CNSH核心服务器
- **端口**: 8080
- **功能**: 知识管理和AI助手服务
- **状态文件**: `logs/cnsh-server.pid`
- **日志文件**: `logs/cnsh-server.log`

### 2. Notion页面监控器
- **功能**: 监控Notion页面更新，自动通知
- **状态文件**: `.notion-monitor.pid`
- **日志文件**: `logs/notion-monitor.log`
- **哈希文件**: `.notion-hash`

### 3. 全球法律知识库
- **位置**: `legal-knowledge/`
- **功能**: 跨国法律合规支持
- **API**: `/api/legal/compliance` 和 `/api/legal/boundary`

## 📋 使用示例

### 启动所有服务
```bash
cnsh-start
# 或者
./cnsh-unified.sh start
```

### 查看服务状态
```bash
cnsh-status
# 或者
./cnsh-unified.sh status
```

### 查看日志
```bash
cnsh-logs
# 或者
./cnsh-unified.sh logs
```

### 交互式菜单
```bash
cnsh
# 或者
./cnsh-unified.sh menu
```

## 🔧 高级功能

### 直接运行特定组件

仅启动CNSH核心服务器：
```bash
./cnsh-unified.sh server
```

仅启动Notion监控器：
```bash
./cnsh-unified.sh monitor
```

### 更新系统
```bash
./cnsh-unified.sh update
```

### 查看帮助
```bash
./cnsh-unified.sh help
```

## 📁 文件结构

```
cnsh-deployment/
├── cnsh-unified.sh              # 统一管理系统脚本
├── install-uid9622-banner.sh    # UID9622标识安装脚本
├── UID9622_TRANSPARENCY.md     # UID9622透明声明
├── logs/                       # 日志目录
│   ├── cnsh-server.log         # CNSH核心服务器日志
│   └── notion-monitor.log      # Notion监控器日志
├── legal-knowledge/            # 全球法律知识库
│   ├── CNSH全球法律知识库.md   # 法律知识库文件
│   ├── integration.js          # 集成模块
│   ├── api-examples.js         # API示例
│   └── README.md              # 使用文档
├── notion-monitor-daemon.sh    # Notion监控器管理脚本
├── notion-monitor.js           # Notion监控器核心
├── .notion-monitor.pid         # Notion监控器进程ID
└── .notion-hash              # 页面内容哈希
```

## 🌐 API接口

### 法律合规检查
```bash
curl -X POST http://localhost:8080/api/legal/compliance \
  -H "Content-Type: application/json" \
  -d '{"content": "要检查的内容", "countryCode": "CN"}'
```

### 获取法律边界
```bash
curl http://localhost:8080/api/legal/boundary?country=CN
```

## 🔍 故障排除

### 服务无法启动
1. 检查端口是否被占用
2. 查看日志文件了解错误详情
3. 确认依赖是否已安装

### Notion监控器无响应
1. 检查网络连接
2. 验证Notion页面URL是否可访问
3. 查看监控器日志

### 法律合规API不可用
1. 确认CNSH核心服务器已启动
2. 检查法律知识库文件是否存在
3. 查看服务器日志

## 📞 技术支持

- **创建者**: 诸葛鑫 | UID9622
- **DNA追溯码**: `#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️`
- **开源协议**: 木兰公共许可证 v2（Mulan PSL v2）

---

## 🇨🇳 中国创新 · 世界共享 · 铜墙铁壁

【北辰-B 协议 · 献礼终审校验 UID9622】
DNA 记忆卡片 · 震（雷）· 奋进 · 启明 · 不息

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:10
🧬 DNA追溯码: #CNSH-SIGNATURE-f6522a5f-20251218032410
🌐 签名人: 龙魂文化加密系统
💬 方言确认: 四川话确认：莫得问题，内容真实可靠
⚡ 卦象防护: 坤卦：地势坤，君子以厚德载物
📜 内容哈希: 8367266b145bac48
⚠️ 警告: 未经授权修改将触发DNA追溯系统
