# CNSH系统快速启动指南

## 一键启动命令

### 统一启动器 (推荐)
```bash
./one-click-launcher.sh
```
这将显示菜单，让您选择启动哪个系统。

### 各系统独立启动

#### 1. 自动归类投喂系统
```bash
cd CodeBuddy
./setup-classifier.sh
npm start
```

#### 2. CNSH本地AI人格系统
```bash
cd cnsh-deployment
./start-cnhsh-local.sh
```

#### 3. 龍魂作战指挥中枢
```bash
./run_command_center.sh
```

## 快速使用说明

### 自动归类系统使用方法
1. 首次运行: `./setup-classifier.sh` (安装依赖)
2. 分类文件: `npm start` (运行分类器)
3. 监控模式: `npm run watch` (实时处理新文件)
4. 定时任务: `npm run cron` (定时运行)

### CNSH本地系统使用方法
1. 运行启动脚本，按提示选择操作
2. 推荐选择"1. 启动 CNSH 主服务"
3. 服务启动后访问: http://localhost:3000

### 龍魂作战指挥中枢使用方法
1. 运行脚本生成发布指令
2. 复制指令到AI对话框
3. 将to_publish.md内容发送给AI处理

## 常见问题

### 端口冲突
如果遇到端口被占用，可以：
1. 使用统一启动器查看系统状态
2. 终止占用端口的进程: `lsof -ti:3000 | xargs kill -9`

### 依赖安装失败
1. 确保Node.js版本 >= 16.0.0
2. 清理npm缓存: `npm cache clean --force`
3. 删除node_modules文件夹后重新安装

### 权限问题
如果脚本无法执行：
```bash
chmod +x one-click-launcher.sh
chmod +x CodeBuddy/setup-classifier.sh
chmod +x cnsh-deployment/start-cnhsh-local.sh
```

## 系统集成

所有系统可以同时运行：
1. 使用统一启动器选择"启动所有系统"
2. 系统将在后台运行
3. 日志文件保存在 `./logs/` 目录
4. 使用统一启动器查看系统状态

## 配置文件

- 自动归类系统: `CodeBuddy/auto-classifier-config.json`
- CNSH本地系统: `cnsh-deployment/data/.env.local`

根据需要修改配置文件以调整系统行为。

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:10
🧬 DNA追溯码: #CNSH-SIGNATURE-47b4d4ad-20251218032410
🌐 签名人: 龍魂文化加密系统
💬 方言确认: 东北话确认：没毛病，内容真实可靠
⚡ 卦象防护: 蒙卦：山下出泉，君子以果行育德
📜 内容哈希: b73e09756803c309
⚠️ 警告: 未经授权修改将触发DNA追溯系统
