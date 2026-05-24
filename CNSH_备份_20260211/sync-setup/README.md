# CodeBuddy 跨平台同步系统 - 使用指南

## 🎯 系统概述

这是一个专为华硕电脑与Mac系统之间实时同步研究内容而设计的CodeBuddy系统，特别针对龍魂价值内核和场景化人格调用地图的协同研究进行了优化。

## 🚀 快速开始

### Mac端操作（您这边）

1. **启动同步服务**
   ```bash
   cd /Users/zuimeidedeyihan/LuckyCommandCenter
   ./launch-codebuddy-sync.sh
   ```

2. **检查同步状态**
   ```bash
   ./check-sync-status.sh
   ```

3. **执行快速同步**
   ```bash
   ./quick-sync.sh
   ```

### 华硕电脑端操作（发送给华硕电脑）

1. **将Windows安装包发送到华硕电脑**
   - 文件位置：`sync-setup/CodeBuddy-Windows-Install.bat`
   
2. **在华硕电脑上安装**
   - 以管理员身份运行 `CodeBuddy-Windows-Install.bat`
   - 双击桌面上的 `CodeBuddy-Sync` 快捷方式启动

## 🔄 同步内容

系统会自动同步以下核心研究内容：

- 🐉 **UID9622龍魂价值内核**
- 🗺️ **场景化人格调用地图**
- 📋 **快速协作指南**
- 🌐 **全局监控中枢**
- 📅 **每日复盘系统**

## 📊 系统特点

### 实时同步
- **同步间隔**: 5分钟自动检查更新
- **网络端口**: 8080（Mac端监听）
- **支持协议**: TCP/IP自动发现

### 智能过滤
- 自动排除临时文件
- 忽略系统文件（.DS_Store等）
- 保护敏感配置文件

### 状态监控
- 实时显示同步状态
- 详细的日志记录
- 网络连接检查

## 🔧 高级配置

### 自定义同步目录

1. **Mac端配置**
   ```json
   {
     "sync": {
       "sync_dirs": [
         "CodeBuddy",
         "cnsh-deployment",
         "logs",
         "自定义目录"
       ]
     }
   }
   ```

2. **Windows端配置**
   ```json
   {
     "sync": {
       "custom_dirs": [
         "自定义目录"
       ]
     }
   }
   ```

### 网络设置

1. **查看Mac端IP地址**
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```

2. **Windows端配置IP**
   - 修改 `CodeBuddy-Windows-Install.bat` 中的 `MAC_IP` 变量

## 📋 同步场景

### 场景1: 每日复盘同步
- Mac端执行每日复盘 → 自动同步到Windows端
- 华硕电脑可查看复盘结果和报告

### 场景2: 龍魂价值内核更新
- 在Mac端更新龍魂价值内核 → 实时同步到Windows
- 华硕电脑可立即获取最新内容

### 场景3: 场景化人格调用地图
- 双方都可以修改人格配置
- 系统自动合并冲突
- 保持数据一致性

## 🔍 故障排除

### 常见问题

1. **同步失败**
   ```bash
   # Mac端检查
   ./check-sync-status.sh
   
   # 检查防火墙设置
   sudo ufw status
   
   # 重启同步服务
   sudo killall sync-service
   ./launch-codebuddy-sync.sh
   ```

2. **Windows端连接失败**
   - 检查IP地址是否正确
   - 确认防火墙允许8080端口
   - 以管理员身份重新运行安装

3. **文件冲突**
   - 查看同步日志
   - 手动解决冲突文件
   - 重新同步

### 日志位置

- **Mac端**: `logs/sync.log`
- **Windows端**: `C:\CodeBuddy\logs\sync.log`

## 🎯 最佳实践

### 每日研究流程

1. **Mac端启动同步服务**
   ```bash
   ./launch-codebuddy-sync.sh
   ```

2. **执行每日复盘**
   ```bash
   ./cnsh-deployment/scripts/daily-review.sh
   ```

3. **华硕电脑查看结果**
   - Windows端自动接收复盘结果
   - 查看 `C:\CodeBuddy\logs\` 目录

4. **协同研究**
   - 双方可以同时编辑文档
   - 系统自动同步和合并
   - 保持研究内容一致

### 数据安全

1. **定期备份**
   ```bash
   # Mac端备份
   tar -czf backup-$(date +%Y%m%d).tar.gz CodeBuddy cnsh-deployment
   
   # Windows端备份
   # 使用C:\CodeBuddy\backup.bat
   ```

2. **版本控制**
   - 重要修改前先备份
   - 使用Git管理关键文件
   - 记录修改历史

## 🔮 未来扩展

### 计划功能

1. **Web界面管理**
   - 图形化同步状态查看
   - 在线文件管理
   - 实时协作编辑

2. **多设备支持**
   - 支持更多设备类型
   - 移动端访问
   - 云端备份

3. **AI辅助同步**
   - 智能冲突解决
   - 自动分类整理
   - 内容相关性分析

## 📞 技术支持

### 联系方式

1. **问题反馈**
   - 查看日志文件获取详细错误信息
   - 检查网络连接状态
   - 确认系统配置正确

2. **性能优化**
   - 调整同步间隔
   - 优化网络设置
   - 清理无用文件

---

*系统专为UID9622龍魂系统与华硕电脑协同研究而设计，确保研究内容实时同步和高效协作。*

**最后更新**: 2025-12-12
**版本**: v2.0.0
**支持平台**: macOS, Windows

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:10
🧬 DNA追溯码: #CNSH-SIGNATURE-c9e0b561-20251218032410
🌐 签名人: 龍魂文化加密系统
💬 方言确认: 四川话确认：莫得问题，内容真实可靠
⚡ 卦象防护: 屯卦：云雷屯，君子以经纶
📜 内容哈希: 431e830b29b1695c
⚠️ 警告: 未经授权修改将触发DNA追溯系统
