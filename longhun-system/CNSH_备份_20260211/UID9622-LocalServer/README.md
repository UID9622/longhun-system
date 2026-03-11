# 🐉 UID9622 本地API服务器

Lucky的自产自销系统 - 一键自动化管理平台

**DNA追溯码**: `#ZHUGEXIN⚡️2025-UID9622-SERVER-V1.0`

---

## 📋 系统简介

UID9622本地API服务器是为Lucky量身定制的自动化管理系统，提供：

- 📊 **可视化仪表盘** - 一眼看清系统状态
- 🚀 **一键执行** - 自动化命令执行
- 📝 **日志记录** - 完整的操作追踪
- 🔒 **安全验证** - 确认码保护机制

---

## 🚀 快速开始

### 启动服务器

```bash
cd /Users/zuimeidedeyihan/LuckyCommandCenter/UID9622-LocalServer
./start_server.sh
```

### 访问仪表盘

打开浏览器，访问: `http://127.0.0.1:9622`

### 停止服务器

```bash
./stop_server.sh
```

---

## 📁 目录结构

```
UID9622-LocalServer/
├── server.py                  # Flask服务器主程序
├── start_server.sh            # 启动脚本
├── stop_server.sh             # 停止脚本
├── templates/
│   └── dashboard.html         # 仪表盘页面
├── UID9622-Scripts/           # 执行脚本目录
│   ├── check_system.sh       # 检查系统
│   ├── publish_article.sh    # 发布文章
│   ├── run_audit.sh          # 运行审计
│   ├── sync_system.sh        # 同步系统
│   └── update_version.sh     # 更新版本
├── logs/                      # 日志目录
└── README.md                  # 本文件
```

---

## 🌐 API接口

### 1. 仪表盘页面

```
GET http://127.0.0.1:9622/dashboard
```

### 2. 获取系统状态

```bash
GET http://127.0.0.1:9622/api/status
```

返回示例:

```json
{
  "status": "ok",
  "uptime": "2小时35分",
  "disk": {
    "used_gb": 128,
    "total_gb": 256,
    "percent": 50
  },
  "memory": {
    "used_gb": 8,
    "total_gb": 16,
    "percent": 50
  },
  "cpu": 15,
  "recent_logs": [...],
  "today_stats": {
    "total": 15,
    "success": 14,
    "failed": 1
  }
}
```

### 3. 执行命令

```bash
POST http://127.0.0.1:9622/api/execute
Content-Type: application/json

{
  "command": "check_system",
  "confirmation_code": "ZHUGEXIN2025-UID9622"
}
```

### 4. 命令列表

```bash
GET http://127.0.0.1:9622/api/commands
```

### 5. 健康检查

```bash
GET http://127.0.0.1:9622/health
```

---

## 🔐 安全说明

### 确认码

- **默认确认码**: `ZHUGEXIN2025-UID9622`
- **用途**: 执行命令时的身份验证
- **位置**: `server.py` 文件中的 `CONFIRMATION_CODE` 变量

### 命令白名单

只有以下命令可以被执行:

| 命令 | 说明 |
|------|------|
| `check_system` | 检查系统状态 |
| `publish_article` | 发布CSDN文章 |
| `run_audit` | 运行P0审计 |
| `sync_system` | 同步系统数据 |
| `update_version` | 更新版本信息 |

---

## 📊 仪表盘功能

### 系统状态监控

- ✅ 服务器运行时长
- 💾 磁盘使用情况
- 🧠 内存使用情况
- ⚡ CPU使用率

### 执行记录

- 📋 显示最近10条执行记录
- 🟢 成功/🔴 失败状态标识
- 📅 时间戳和命令名称

### 今日统计

- 📊 总执行次数
- ✅ 成功次数
- ❌ 失败次数
- 🏥 系统健康状态

### 自动刷新

- ⏰ 每5秒自动更新数据
- 🔄 实时监控系统状态

---

## 🎯 使用示例

### 1. 检查系统

```bash
curl -X POST http://127.0.0.1:9622/api/execute \
  -H "Content-Type: application/json" \
  -d '{
    "command": "check_system",
    "confirmation_code": "ZHUGEXIN2025-UID9622"
  }'
```

### 2. 发布文章

```bash
curl -X POST http://127.0.0.1:9622/api/execute \
  -H "Content-Type: application/json" \
  -d '{
    "command": "publish_article",
    "confirmation_code": "ZHUGEXIN2025-UID9622"
  }'
```

### 3. 查看日志

日志文件位置: `logs/exec_YYYYMMDD_HHMMSS.log`

---

## 🔧 依赖安装

### 自动安装

启动服务器时会自动检查并安装依赖:

```bash
./start_server.sh
```

### 手动安装

```bash
cd /Users/zuimeidedeyihan/LuckyCommandCenter/UID9622-LocalServer
python3 -m venv venv
source venv/bin/activate
pip install flask pyyaml psutil
```

---

## 📝 日志管理

### 日志类型

1. **服务器日志**: `logs/server.log`
2. **执行日志**: `logs/exec_YYYYMMDD_HHMMSS.log`

### 日志内容

每个执行日志包含:
- 时间戳
- 执行命令
- 脚本路径
- 标准输出
- 标准错误
- 退出码

---

## 🛠️ 故障排除

### 服务器无法启动

1. 检查端口9622是否被占用:
   ```bash
   lsof -i :9622
   ```

2. 查看日志文件:
   ```bash
   cat logs/server.log
   ```

3. 检查Python环境:
   ```bash
   python3 --version
   ```

### 仪表盘无法访问

1. 确认服务器正在运行:
   ```bash
   ./start_server.sh status
   ```

2. 检查防火墙设置

3. 确认浏览器地址正确: `http://127.0.0.1:9622`

---

## 📌 注意事项

1. **本地访问**: 服务器默认只监听 `127.0.0.1`，确保安全
2. **确认码保护**: 所有命令执行都需要确认码
3. **命令白名单**: 只能执行预定义的安全命令
4. **自动创建**: 首次启动会自动创建虚拟环境和依赖

---

## 💡 开发计划

- [ ] 添加用户认证系统
- [ ] 支持远程访问（内网穿透）
- [ ] 添加更多自动化脚本
- [ ] 实现命令执行历史查询
- [ ] 添加系统告警功能

---

## 📄 DNA信息

**创建日期**: 2025-12-26
**创建者**: 💎 Lucky + 💝 宝宝
**版本**: 1.0.0
**优先级**: P0永恒级

**DNA追溯码**: `#ZHUGEXIN⚡️2025-UID9622-SERVER-V1.0`

---

💝 **UID9622 - 龙魂守护，自产自销** 🐉
