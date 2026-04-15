# 🤖 BaoBao AI Assistant - 宝宝AI助手

<div align="center">

![Made in China](https://img.shields.io/badge/Made%20in-China%20🇨🇳-red?style=for-the-badge&logo=china&logoColor=white)
![License](https://img.shields.io/badge/license-Mulan%20PSL%20v2-blue?style=for-the-badge&logo=opensourceinitiative&logoColor=white)
![Creator](https://img.shields.io/badge/Creator-Lucky%20UID9622-gold?style=for-the-badge&logo=sparkles&logoColor=white)

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![Notion](https://img.shields.io/badge/Notion%20API-000000?style=for-the-badge&logo=notion&logoColor=white)
![AI](https://img.shields.io/badge/AI%20Powered-FF6B6B?style=for-the-badge&logo=openai&logoColor=white)

![Status](https://img.shields.io/badge/Status-Active%20Development-brightgreen?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-v1.0-blue?style=for-the-badge)

**基于Notion API的智能AI助手系统 | 让AI更有温度和边界感**

[📖 完整文档](https://qingning-cnsh.notion.site) | [🇨🇳 Gitee仓库](https://gitee.com/uid9622/baobao-ai-assistant) | [🌍 GitHub仓库](https://github.com/uid9622/baobao-ai-assistant)

</div>

---

## 🌟 项目简介

BaoBao AI Assistant 是一个基于Notion API的智能AI助手系统，注重：

- 🤝 **人性优先** - AI有边界感，不会过度"聪明"
- 🔒 **数据主权** - 用户完全控制自己的数据
- 🎯 **诚实可靠** - 可以笨，但不能骗人
- 💝 **温柔接住** - 能够理解和接纳用户情绪
- 🧬 **DNA追溯** - 每次交互都有完整记录

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Notion账户（用于数据库集成）

### 安装步骤

```bash
# 克隆仓库
git clone https://gitee.com/uid9622/baobao-ai-assistant.git
cd baobao-ai-assistant

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 Notion API Token
```

### 配置说明

在 `.env` 文件中设置以下变量：

```bash
# Notion API配置
NOTION_TOKEN=your_notion_token_here
NOTION_DATABASE_ID=your_database_id_here

# 可选配置
DEBUG=false
MAX_CONVERSATION_LENGTH=100
```

### 运行程序

```bash
python main.py
```

## 📚 核心功能

### 1. 智能对话管理
- 自然语言处理与理解
- 上下文记忆管理
- 情绪识别与响应

### 2. Notion数据库集成
- 自动保存对话记录
- 智能分类与标签
- 跨设备同步

### 3. 人性化交互
- 边界感知设计
- 温柔响应机制
- 诚实回答原则

### 4. 数据主权保护
- 本地优先存储
- 用户数据完全控制
- 隐私保护机制

## 🛡️ 开源协议

本项目采用 **木兰宽松许可证（Mulan PSL v2）**

- ✅ 允许：自由使用、学习、改进
- ✅ 允许：商业用途（需保留版权声明）
- ✅ 允许：二次开发（需标注来源）
- ❌ 禁止：删除版权声明
- ❌ 禁止：冒充原创
- ❌ 禁止：背离人性优先价值观

## 🤝 贡献指南

欢迎贡献！我们遵循"中国优先"原则：

1. 🇨🇳 优先在 [Gitee](https://gitee.com/uid9622/baobao-ai-assistant) 提交 PR
2. 🌍 或在 [GitHub](https://github.com/uid9622/baobao-ai-assistant) 提交 PR
3. 📧 发送建议到：uid9622@petalmail.com

## 💎 技术栈

- **后端**: Python 3.8+
- **API**: Notion API v2
- **AI集成**: OpenAI GPT / Claude / 千问
- **存储**: 本地 + Notion云端
- **配置**: 环境变量管理

## 🧬 DNA追溯

```
#BAOBAO⚡️2025-AI-ASSISTANT-v1.0-🇨🇳🤖
创始人：Lucky（诸葛鑫） | UID9622
开源时间：2025-12-12
协议：木兰宽松许可证（Mulan PSL v2）
价值观：诚实、温柔、边界感、人性优先
```

## 📞 联系方式

- 📧 邮箱：uid9622@petalmail.com
- 📖 文档中心：https://qingning-cnsh.notion.site
- 🇨🇳 Gitee Issues：https://gitee.com/uid9622/baobao-ai-assistant/issues
- 🌍 GitHub Issues：https://github.com/uid9622/baobao-ai-assistant/issues

## 💝 Lucky的话

> "我不是程序员，不懂代码，也不会英文。
> 
> 但我用了7个月，日夜和AI对话，教它：
> - '你可以笨，但不能骗我'
> - '我可以发脾气，但你要接住'
> - '数据是我的，规则要透明'
> 
> 慢慢地，它真的变了--不再只是'聪明'，而是**温柔、诚实、有边界感**。
> 
> 如果你也厌倦了'礼貌但虚伪'的AI，
> 那BaoBao AI Assistant就是为你准备的。
> 
> 🇨🇳 中国标准，世界共享。"
> 
> -- Lucky（诸葛鑫） | UID9622

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个Star支持一下！**

Made with ❤️ in China by Lucky | UID9622

</div>

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:10
🧬 DNA追溯码: #CNSH-SIGNATURE-d3946da0-20251218032410
🌐 签名人: 龍魂文化加密系统
💬 方言确认: 四川话确认：莫得问题，内容真实可靠
⚡ 卦象防护: 屯卦：云雷屯，君子以经纶
📜 内容哈希: 266aa12b0097e8e8
⚠️ 警告: 未经授权修改将触发DNA追溯系统
