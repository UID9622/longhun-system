# AIClaw (小龙虾) 系统分析报告与扩展设计方案

> 分析日期: 2026-06-27
> 基于 OpenHub AIClaw API 文档截图分析

---

## 一、现有系统全景分析

### 1.1 系统定位

AIClaw 是一个 **AI 平台浏览器自动化控制中间件**，它通过浏览器扩展（aiClaw Extension）捕获 AI 平台的标签页，暴露 REST API 供外部调用，实现对多个 AI 平台的统一程序化操作。

**核心价值**：让 Bot/脚本能够以编程方式与 ChatGPT、Gemini、Grok 等 AI 平台交互，无需直接调用各平台的官方 API。

### 1.2 当前架构

```
┌─────────────────────────────────────────────────────────────┐
│                     调用方 (Bot/脚本)                         │
│              curl / HTTP Client / SDK                        │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP REST API
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              OpenHub Server (localhost:10088)               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐  │
│  │  /ai/docs   │ │ /ai/status  │ │    /ai/message      │  │
│  │  /ai/new_...│ │ /ai/navigate│ │                     │  │
│  └──────┬──────┘ └──────┬──────┘ └──────────┬──────────┘  │
│         └─────────────────┴───────────────────┘             │
│                        │                                    │
│              aiClaw Extension                              │
│         (浏览器扩展 - DOM 操作引擎)                          │
└────────────────────────┬────────────────────────────────────┘
                         │ 标签页注入/控制
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
   ┌──────────┐   ┌──────────┐   ┌──────────┐
   │ ChatGPT  │   │  Gemini  │   │   Grok   │
   │chatgpt.co│   │gemini.goo│   │ grok.com │
   └──────────┘   └──────────┘   └──────────┘
```

### 1.3 现有 API 端点详解

| 端点 | 方法 | 功能 | 关键参数 |
|------|------|------|----------|
| `/api/v1/ai/docs` | GET | 获取完整 API 文档 | 无 |
| `/api/v1/ai/status` | GET | 获取所有 AI 平台标签页状态 | 无 |
| `/api/v1/ai/message` | POST | 向指定 AI 平台发送消息 | `platform`, `prompt`, `conversationId` |
| `/api/v1/ai/new_conversation` | POST | 创建新对话 | `platform` |
| `/api/v1/ai/navigate` | POST | 导航到平台首页 | `platform` |

### 1.4 技术实现原理

**消息发送流程 (`/ai/message`)**：
1. 接收 `platform` + `prompt` + 可选 `conversationId`
2. 通过 aiClaw 浏览器扩展定位对应平台的标签页
3. **DOM 操作**：自动找到输入框 → 填入消息 → 触发提交
4. **等待响应**：监听 DOM 变化，捕获 AI 的完整回复
5. 透传返回原始文本，不做任何数据处理或格式化

**状态检测流程 (`/ai/status`)**：
1. 扫描所有由 aiClaw 扩展捕获的 AI 平台标签页
2. 返回每个标签页的：tabId、URL、是否活动、登录状态等

### 1.5 支持平台清单

| 平台标识 | 平台名称 | 首页 URL | 状态 |
|----------|----------|----------|------|
| `chatgpt` | ChatGPT | https://chatgpt.com | 已支持 |
| `gemini` | Google Gemini | https://gemini.google.com | 已支持 |
| `grok` | xAI Grok | https://grok.com | 已支持 |
| `kimi` | **Kimi 智能助手** | **https://kimi.moonshot.cn** | **⚠️ 待接入** |

---

## 二、扩展设计方案：接入 Kimi + 终端 CLI + 通用 APP 控制

### 2.1 目标架构（扩展后）

```
┌─────────────────────────────────────────────────────────────────────┐
│                         调用层                                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │ Terminal │  │ Kimi APP │  │ Kimi Web │  │   Other Bots     │  │
│  │   CLI    │  │  Native  │  │ Browser  │  │                  │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────────┬─────────┘  │
└───────┼─────────────┼─────────────┼─────────────────┼────────────┘
        │             │             │                 │
        └─────────────┴──────┬──────┴─────────────────┘
                             │
                    ┌────────▼────────┐
                    │  OpenHub Server │
                    │  (port 10088)   │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┬──────────────┐
              ▼              ▼              ▼              ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐
        │ ChatGPT  │ │  Gemini  │   Grok    │ │   Kimi           │
        │          │ │          │ │          │ │  (Moonshot AI)   │
        └──────────┘ └──────────┘ └──────────┘ └──────────────────┘
        ┌──────────────────────────────────────────────────────────┐
        │              通用 APP 控制框架 (未来扩展)                   │
        │   ┌────────┐ ┌────────┐ ┌────────┐ ┌────────────────┐  │
        │   │ Notion │ │  Slack │ │ Discord│ │  任意 Web App   │  │
        │   └────────┘ └────────┘ └────────┘ └────────────────┘  │
        └──────────────────────────────────────────────────────────┘
```

### 2.2 Kimi 平台接入方案

#### 2.2.1 Kimi Web 端接入

**目标 URL**: https://kimi.moonshot.cn

**DOM 操作映射**：

| 操作 | Kimi 页面元素定位策略 |
|------|----------------------|
| 找到输入框 | `[contenteditable="true"]` 或 `.chat-input textarea` |
| 填入消息 | `element.textContent = prompt` + 触发 `input` 事件 |
| 触发发送 | 点击发送按钮 或 触发 `Enter` 键盘事件 |
| 获取回复 | 监听 `.chat-message.ai` 新元素出现 |
| 新对话 | 点击 "新对话" 按钮（侧边栏顶部） |
| 检测登录 | 检查是否存在登录弹窗或特定未登录标志 |

**新增 API 调用示例**：

```bash
# 向 Kimi 发送消息
curl -X POST http://127.0.0.1:10088/api/v1/ai/message \
    -H "Content-Type: application/json" \
    -d '{"platform":"kimi", "prompt":"你好，请介绍一下自己"}'

# 创建 Kimi 新对话
curl -X POST http://127.0.0.1:10088/api/v1/ai/new_conversation \
    -H "Content-Type: application/json" \
    -d '{"platform":"kimi"}'

# 导航 Kimi 到首页
curl -X POST http://127.0.0.1:10088/api/v1/ai/navigate \
    -H "Content-Type: application/json" \
    -d '{"platform":"kimi"}'
```

#### 2.2.2 Kimi APP 端接入（进阶）

Kimi APP 的接入需要不同的技术路线：

| 方案 | 技术实现 | 难度 | 稳定性 |
|------|----------|------|--------|
| A. Android Accessibility | 无障碍服务模拟点击/输入 | 中 | 高 |
| B. ADB 命令 | 通过 `adb shell input` 发送点击和文本 | 低 | 中 |
| C. 模拟器方案 | 在模拟器中运行 + 截图OCR + 点击 | 中 | 中 |
| D. 逆向 API | 抓包分析 Kimi APP 的私有 API | 高 | 低（易被封） |

**推荐方案 B（ADB）作为 MVP**：

```bash
# 启动 Kimi APP
adb shell am start -n com.moonshot.kimi/.MainActivity

# 模拟点击输入框（坐标需根据设备适配）
adb shell input tap 500 1800

# 输入文本
adb shell input text "Hello%20Kimi"

# 模拟点击发送
adb shell input tap 950 1800

# 截图获取回复
adb shell screencap -p /sdcard/reply.png
adb pull /sdcard/reply.png .
```

### 2.3 终端 CLI 工具设计

#### 2.3.1 命令结构

```bash
# ========== 基础命令 ==========

# 查看所有平台状态
ai-claw status

# 查看特定平台状态
ai-claw status --platform kimi

# 发送消息
ai-claw ask "你好，请总结一下量子计算" --platform kimi

# 发送消息并保存到文件
ai-claw ask "写一首关于夏天的诗" --platform chatgpt --output poem.txt

# 创建新对话
ai-claw new --platform kimi

# 导航到首页
ai-claw home --platform kimi

# 同时向多个平台提问（对比模式）
ai-claw ask "解释区块链" --platform kimi,chatgpt,gemini --compare

# ========== 高级命令 ==========

# 流式输出（SSE 实时打印）
ai-claw ask "写一段Python代码" --platform kimi --stream

# 带系统提示词
ai-claw ask "分析这段代码" --platform kimi --system "你是一位资深Python工程师"

# 对话续接（指定 conversationId）
ai-claw ask "继续" --platform kimi --conversation conv_abc123

# 批量提问（从文件读取）
ai-claw batch questions.txt --platform kimi --output answers.json

# 查看 API 文档
ai-claw docs

# 交互模式（REPL）
ai-claw interactive --platform kimi
```

#### 2.3.2 CLI 安装与配置

```bash
# 安装
npm install -g @openhub/ai-claw-cli

# 配置服务端点
ai-claw config set endpoint http://127.0.0.1:10088

# 查看配置
ai-claw config get

# 添加平台快捷别名
ai-claw alias set k kimi
ai-claw alias set c chatgpt
ai-claw alias set g gemini

# 使用别名
ai-claw ask "你好" -p k
```

#### 2.3.3 CLI 实现代码（Node.js 示例）

```javascript
#!/usr/bin/env node
// ai-claw-cli

const { program } = require('commander');
const axios = require('axios');
const chalk = require('chalk');
const ora = require('ora');

const API_BASE = process.env.AICLAW_ENDPOINT || 'http://127.0.0.1:10088';

program
  .name('ai-claw')
  .description('AIClaw CLI - 控制多个 AI 平台的终端工具')
  .version('1.0.0');

// status 命令
program
  .command('status')
  .description('查看 AI 平台状态')
  .option('-p, --platform <platform>', '指定平台 (kimi/chatgpt/gemini/grok)')
  .action(async (options) => {
    const spinner = ora('获取状态中...').start();
    try {
      const res = await axios.get(`${API_BASE}/api/v1/ai/status`);
      spinner.stop();
      
      const platforms = options.platform 
        ? res.data.filter(p => p.platform === options.platform)
        : res.data;
      
      console.log('\n' + chalk.bold('🦞 AIClaw 平台状态\n'));
      platforms.forEach(p => {
        const status = p.active ? chalk.green('● 在线') : chalk.red('● 离线');
        const login = p.loggedIn ? chalk.green('已登录') : chalk.yellow('未登录');
        console.log(`  ${chalk.bold(p.platform.padEnd(10))} ${status}  ${login}  ${p.url}`);
      });
      console.log('');
    } catch (err) {
      spinner.fail(`错误: ${err.message}`);
    }
  });

// ask 命令
program
  .command('ask <prompt>')
  .description('向 AI 平台发送消息')
  .option('-p, --platform <platform>', '目标平台', 'kimi')
  .option('-o, --output <file>', '保存回复到文件')
  .option('-s, --stream', '流式输出')
  .option('-c, --conversation <id>', '续接对话 ID')
  .action(async (prompt, options) => {
    const spinner = ora(`正在询问 ${options.platform}...`).start();
    try {
      const payload = {
        platform: options.platform,
        prompt: prompt
      };
      if (options.conversation) payload.conversationId = options.conversation;
      
      const res = await axios.post(`${API_BASE}/api/v1/ai/message`, payload);
      spinner.stop();
      
      const reply = res.data.response;
      
      if (options.output) {
        require('fs').writeFileSync(options.output, reply);
        console.log(chalk.green(`✓ 回复已保存到 ${options.output}`));
      }
      
      console.log('\n' + chalk.cyan('━━ 回复 ━━'));
      console.log(reply);
      console.log(chalk.cyan('━━━━━━━━━\n'));
    } catch (err) {
      spinner.fail(`错误: ${err.message}`);
    }
  });

// new 命令
program
  .command('new')
  .description('创建新对话')
  .option('-p, --platform <platform>', '目标平台', 'kimi')
  .action(async (options) => {
    const spinner = ora('创建新对话...').start();
    try {
      await axios.post(`${API_BASE}/api/v1/ai/new_conversation`, {
        platform: options.platform
      });
      spinner.succeed(`${options.platform} 新对话已创建`);
    } catch (err) {
      spinner.fail(`错误: ${err.message}`);
    }
  });

// interactive 命令
program
  .command('interactive')
  .description('交互模式 (REPL)')
  .option('-p, --platform <platform>', '目标平台', 'kimi')
  .action(async (options) => {
    const readline = require('readline');
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
    
    console.log(chalk.cyan(`🦞 AIClaw 交互模式 - ${options.platform}\n`));
    console.log('输入 /quit 退出，/new 创建新对话\n');
    
    const ask = () => {
      rl.question(chalk.bold('你 > '), async (prompt) => {
        if (prompt === '/quit') { rl.close(); return; }
        if (prompt === '/new') {
          await axios.post(`${API_BASE}/api/v1/ai/new_conversation`, {
            platform: options.platform
          });
          console.log(chalk.yellow('新对话已创建\n'));
          ask();
          return;
        }
        
        try {
          const res = await axios.post(`${API_BASE}/api/v1/ai/message`, {
            platform: options.platform,
            prompt: prompt
          });
          console.log(chalk.green(`${options.platform} > `) + res.data.response + '\n');
        } catch (err) {
          console.log(chalk.red('错误: ' + err.message + '\n'));
        }
        ask();
      });
    };
    ask();
  });

program.parse();
```

### 2.4 通用 APP 控制框架设计

不只是 AI 平台，未来可以扩展到任意 Web APP：

```javascript
// 通用 APP 控制配置
const appRegistry = {
  // AI 平台
  'kimi': {
    name: 'Kimi 智能助手',
    url: 'https://kimi.moonshot.cn',
    selectors: {
      inputBox: '.chat-input textarea, [contenteditable="true"]',
      sendButton: '.send-btn, button[type="submit"]',
      replyContainer: '.chat-message.ai',
      newChatButton: '.new-chat-btn',
      loginIndicator: '.user-avatar'
    }
  },
  'chatgpt': { /* ... */ },
  'gemini': { /* ... */ },
  'grok': { /* ... */ },
  
  // 通用 APP（未来扩展）
  'notion': {
    name: 'Notion',
    url: 'https://notion.so',
    selectors: { /* ... */ }
  },
  'github': {
    name: 'GitHub',
    url: 'https://github.com',
    selectors: { /* ... */ }
  }
};
```

---

## 三、API 变更建议

### 3.1 现有端点增强

**`/api/v1/ai/status` 返回增强**：

```json
{
  "platforms": [
    {
      "platform": "kimi",
      "name": "Kimi 智能助手",
      "url": "https://kimi.moonshot.cn",
      "tabId": 123,
      "active": true,
      "loggedIn": true,
      "unreadCount": 0,
      "currentConversation": "conv_xxx"
    }
  ],
  "total": 4,
  "online": 3
}
```

### 3.2 建议新增端点

| 端点 | 方法 | 功能 | 使用场景 |
|------|------|------|----------|
| `/api/v1/ai/conversations` | GET | 获取对话列表 | 查看历史对话 |
| `/api/v1/ai/conversations/:id` | DELETE | 删除指定对话 | 清理历史 |
| `/api/v1/ai/stream` | POST | SSE 流式消息 | 实时打字效果 |
| `/api/v1/ai/compare` | POST | 多平台对比提问 | 一次提问，多个平台回答 |
| `/api/v1/ai/platforms` | GET | 获取支持的平台列表 | 动态发现 |
| `/api/v1/ai/upload` | POST | 上传文件到平台 | 发送图片/文档 |

---

## 四、实施路线图

### Phase 1: Kimi Web 接入（1-2 天）
- [ ] 分析 Kimi Web 端 DOM 结构
- [ ] 添加 `kimi` 到平台注册表
- [ ] 实现 Kimi 专用的 DOM 操作适配器
- [ ] 测试消息发送/接收
- [ ] 测试新对话/导航功能

### Phase 2: CLI 工具开发（2-3 天）
- [ ] 初始化 Node.js CLI 项目
- [ ] 实现 core 命令（status/ask/new/navigate）
- [ ] 实现高级功能（stream/compare/batch/interactive）
- [ ] 发布到 npm

### Phase 3: Kimi APP 接入（3-5 天）
- [ ] 调研 Kimi APP 的包名和 Activity
- [ ] 实现 ADB 控制桥
- [ ] 坐标适配（不同分辨率）
- [ ] 截图 OCR 提取回复文本

### Phase 4: 通用框架（1-2 周）
- [ ] 抽象通用 APP 控制接口
- [ ] 插件化平台注册机制
- [ ] 社区平台适配器市场

---

## 五、快速启动脚本

```bash
#!/bin/bash
# quick-start-kimi.sh

echo "🦞 AIClaw - Kimi 快速启动"

# 1. 检查 OpenHub 服务
echo "→ 检查 OpenHub 服务..."
if ! curl -s http://127.0.0.1:10088/api/v1/ai/status > /dev/null; then
    echo "✗ OpenHub 未启动，请先启动服务"
    exit 1
fi
echo "✓ OpenHub 运行中"

# 2. 检查 Kimi 标签页
echo "→ 检查 Kimi 标签页..."
STATUS=$(curl -s http://127.0.0.1:10088/api/v1/ai/status)
if echo "$STATUS" | grep -q '"platform":"kimi".*"active":true'; then
    echo "✓ Kimi 已就绪"
else
    echo "⚠ Kimi 标签页未激活，请打开 https://kimi.moonshot.cn"
fi

# 3. 发送测试消息
echo "→ 发送测试消息..."
curl -s -X POST http://127.0.0.1:10088/api/v1/ai/message \
    -H "Content-Type: application/json" \
    -d '{"platform":"kimi","prompt":"你好，Kimi！"}' | jq -r '.response'

echo ""
echo "✓ Kimi 接入完成！"
```

---

## 六、总结

| 维度 | 现状 | 扩展后 |
|------|------|--------|
| 支持平台 | 3 (ChatGPT/Gemini/Grok) | 4+ (增加 Kimi + 可扩展) |
| 调用方式 | HTTP API only | API + CLI + SDK |
| 覆盖终端 | 浏览器 | 浏览器 + APP + 终端 |
| 扩展性 | 硬编码 | 插件化注册 |

**AIClaw 的核心价值**在于它提供了一种 **"通用 AI 平台遥控器"** 的能力，通过浏览器扩展作为桥梁，让任何外部系统都能以统一的方式控制各种 AI 平台。接入 Kimi 后，它将成为覆盖国内外主流 AI 平台的统一控制中枢。
