# 每日复盘系统 - 龍魂价值内核与场景化人格调用地图

## 🎯 概述

此系统专为每日自动复盘以下核心内容而设计：

- 🐉 **UID9622龍魂价值内核**
- 🗺️ **场景化人格调用地图**
- 📋 **快速协作指南**
- 🌐 **全局监控中枢**

系统会自动与您的Notion数据库（ID: `49f7125a-9c9f-81ec-9db8-00035916bff5`）同步，确保内容始终保持最新。

## 🚀 快速开始

### 1. 手动执行每日复盘

```bash
# 进入项目目录
cd /Users/zuimeidedeyihan/LuckyCommandCenter/cnsh-deployment

# 执行每日复盘
./scripts/daily-review.sh
```

### 2. 设置自动定时任务

```bash
# 创建每天上午9点执行的定时任务
./crontab-setup.sh create 09:00

# 查看定时任务状态
./crontab-setup.sh status

# 删除定时任务
./crontab-setup.sh remove
```

### 3. 测试系统

```bash
# 测试复盘脚本
./scripts/daily-review.sh --help

# 测试定时任务配置
./crontab-setup.sh test
```

## 📊 系统架构

```
每日复盘系统
├── src/services/
│   ├── notionSync.js      # Notion同步服务
│   └── dailyReview.js     # 每日复盘服务
├── src/commands/
│   └── daily-review.js    # 复盘命令行工具
├── scripts/
│   └── daily-review.sh    # 复盘执行脚本
├── crontab-setup.sh       # 定时任务配置脚本
└── .cache/daily-reviews/  # 复盘报告存储
```

## 🐉 龍魂价值内核复盘

系统会深度分析：

### 核心价值观
- 人民为本
- 透明公正
- 自省进化
- 传承创新
- 协同责任

### DNA战略执行
- DNA本地化主权战略
- 中文系统完整性
- 自产自销生态

### 系统健康度
- 价值观对齐度
- 执行效率
- 适应性指标

## 🗺️ 场景化人格调用地图复盘

系统会全面评估：

### 人格结构
- 总人格数（71个）
- 核心人格（12个）
- 支持人格（59个）

### 场景覆盖
- 场景数量统计
- 覆盖完整性分析
- 缺失场景识别

### 协作效率
- 人格间协作机制
- 切换逻辑评估
- 响应时间分析

## 📝 Notion集成

### 同步内容
- 场景化人格调用地图更新
- 快速协作指南变更
- UID9622龍魂价值内核调整
- 全局监控中枢状态

### 同步机制
- 每日自动检查更新
- 增量同步优化
- 冲突解决策略
- 版本历史管理

## 📊 复盘报告

### 报告类型
1. **JSON格式** - 结构化数据，便于程序处理
2. **Markdown格式** - 可读性强，便于人工审查

### 报告内容
- 📊 复盘概览
- 🐉 龍魂价值内核状态
- 🗺️ 场景化人格调用地图状态
- 🔄 系统协调性评分
- 📋 可执行建议

### 报告位置
```
.cache/daily-reviews/
├── review_2025-12-12.json  # JSON格式报告
├── review_2025-12-12.md    # Markdown格式报告
└── ...
```

## 🔧 高级配置

### 环境变量

```bash
# 复盘模式
export REVIEW_MODE=full  # full|quick

# Notion数据库ID
export NOTION_ID=49f7125a-9c9f-81ec-9db8-00035916bff5

# 强制模式
export FORCE_MODE=true
```

### 自定义定时任务

```bash
# 创建自定义时间的定时任务
./crontab-setup.sh create 08:30  # 每天8:30
./crontab-setup.sh create 14:00  # 每天14:00
./crontab-setup.sh create 20:30  # 每天20:30

# 每周复盘（编辑定时任务后）
0 9 * * 1 /path/to/daily-review.sh  # 每周一9点
```

## 📋 监控与日志

### 日志文件

```bash
# 复盘执行日志
tail -f logs/daily-review.log

# 定时任务日志
tail -f logs/daily-review-cron.log

# 定时任务配置日志
tail -f logs/crontab-setup.log
```

### 状态检查

```bash
# 查看定时任务状态
./crontab-setup.sh status

# 查看最新复盘报告
ls -la .cache/daily-reviews/ | head -10

# 快速查看今日复盘摘要
./scripts/daily-review.sh | grep -E "^(🎯|🐉|🗺️|🔄|📝)"
```

## ⚠️ 故障排除

### 常见问题

1. **权限问题**
   ```bash
   chmod +x scripts/daily-review.sh
   chmod +x crontab-setup.sh
   ```

2. **Node.js依赖缺失**
   ```bash
   cd /Users/zuimeidedeyihan/LuckyCommandCenter/cnsh-deployment
   npm install
   ```

3. **定时任务不执行**
   ```bash
   # 检查定时任务服务状态
   sudo launchctl list | grep cron
   
   # 重启定时任务服务
   sudo launchctl unload /Library/LaunchDaemons/com.vix.cron.plist
   sudo launchctl load /Library/LaunchDaemons/com.vix.cron.plist
   ```

4. **Notion同步失败**
   - 检查网络连接
   - 验证Notion ID是否正确
   - 查看Notion API权限

### 调试模式

```bash
# 详细调试输出
DEBUG=* ./scripts/daily-review.sh

# 单独测试Notion同步
node -e "require('./src/services/notionSync').new().performDailySync()"

# 单独测试复盘服务
node -e "require('./src/services/dailyReview').new().performDailyReview()"
```

## 🔮 未来规划

- [ ] 添加Web界面监控
- [ ] 集成更多Notion数据库
- [ ] 增加异常通知机制
- [ ] 支持多用户配置
- [ ] 添加复盘趋势分析

## 📞 支持

如有问题或建议，请：

1. 查看日志文件获取详细错误信息
2. 检查 `.cache/daily-reviews/` 中的最新报告
3. 确认所有依赖已正确安装
4. 验证定时任务配置正确

---

*系统专为UID9622龍魂系统设计，确保每日对核心内容进行深度复盘和分析。*