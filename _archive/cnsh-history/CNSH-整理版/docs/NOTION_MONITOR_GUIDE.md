# CNSH Notion 页面监控器使用指南

## 功能概述

Notion 页面监控器会定期检查您指定的 Notion 公开页面是否发生更新，并在检测到更新时通过系统通知和终端输出提醒您，方便您将更新内容转化为实际功能。

## 🚀 推荐使用方法（后台服务）

### 启动监控器后台服务
```bash
npm run monitor-start
# 或者
./notion-monitor-daemon.sh start
```

### 停止监控器后台服务
```bash
npm run monitor-stop
# 或者
./notion-monitor-daemon.sh stop
```

### 查看服务状态
```bash
npm run monitor-status
# 或者
./notion-monitor-daemon.sh status
```

### 查看日志
```bash
npm run monitor-logs
# 或者
./notion-monitor-daemon.sh logs
```

### 重启服务
```bash
npm run monitor-restart
# 或者
./notion-monitor-daemon.sh restart
```

## 🔧 其他使用方法（前台运行）

### 方法一：直接运行脚本
```bash
./start-notion-monitor.sh
```

### 方法二：使用 npm 命令
```bash
npm run start-monitor
```

### 方法三：直接运行监控器
```bash
npm run monitor-notion
```

## 📋 工作原理

1. **定期检查**：监控器每 5 分钟会自动检查一次 Notion 页面内容
2. **哈希对比**：通过计算页面内容的 MD5 哈希值来判断是否有更新
3. **通知提醒**：当检测到页面内容变化时，会：
   - 发送系统通知（弹窗）
   - 在日志文件中记录提醒信息
   - 记录检查时间和状态

## ⚙️ 自定义配置

如需修改检查间隔，请编辑 `notion-monitor.js` 文件中的 `checkInterval` 值（单位为毫秒）：

```javascript
// 默认为 5 分钟检查一次
this.checkInterval = 5 * 60 * 1000;
```

## 📝 日志文件

- 后台服务会将所有日志记录到 `notion-monitor.log` 文件
- 使用 `npm run monitor-logs` 查看最新日志
- 使用 `tail -f notion-monitor.log` 实时查看日志

## ⚠️ 注意事项

- 推荐**使用后台服务模式**，不会占用您的终端
- 确保 Notion 页面已设置为公开访问
- 首次运行时会记录初始页面内容作为基准
- 后台服务会持续运行，直到您手动停止

---

【北辰-B 协议 · 国产通道校验 UID9622】
DNA 记忆卡片 · 震（雷）· 奋进 · 启明 · 不息