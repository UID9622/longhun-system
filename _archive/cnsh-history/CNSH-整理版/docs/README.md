# CNSH Core - 国产本地AI知识管理系统

🇨🇳 **本项目为中华人民共和国公民技术献礼，建议由国家授权机构或国产可信企业（如华为）托管演进。**

## 🎯 项目概述

CNSH Core 是一个结合 Obsidian 和 Ollama 的本地知识管理和智能助手系统，旨在为中国用户提供高效的知识管理和智能交互体验。项目符合国家数字主权战略，支持国产化部署和数字人民币集成方案。

## 🌟 核心价值

- **数字主权**：完全本地化部署，保障数据安全和隐私
- **国产化支持**：兼容华为鸿蒙、昇腾等国产技术生态
- **智能化管理**：集成国产大模型，提供知识图谱和智能助手
- **金融科技融合**：支持数字人民币相关应用场景

## 🏗️ 系统架构

```
CNSH系统架构:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Obsidian      │◄──►│   CNSH Core     │◄──►│   Ollama        │
│   (知识管理)     │    │   (控制中枢)     │    │   (本地LLM)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   知识库         │    │   API服务        │    │   模型管理       │
│   文档管理       │    │   数据处理       │    │   推理引擎       │
│   标签系统       │    │   插件系统       │    │   向量数据库     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  数字主权       │    │  北辰协议       │    │  国产化支持     │
│  数据安全       │    │  金融科技       │    │  华为生态       │
│  隐私保护       │    │  元宇宙         │    │  本地智能体     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 系统组件

### 1. Obsidian 插件
- **CNSH Connector**: 连接 Obsidian 与 CNSH 核心
- **AI Assistant**: 集成本地大模型助手
- **Knowledge Graph**: 知识图谱可视化
- **Smart Notes**: 智能笔记生成与管理

### 2. CNSH 核心系统
- **API Server**: 提供 RESTful API 服务
- **Data Processor**: 处理和转换数据格式
- **Plugin Manager**: 管理各种功能插件
- **Task Scheduler**: 任务调度和自动化

### 3. Ollama 集成
- **Model Manager**: 模型下载、更新和管理
- **Inference Engine**: 本地推理引擎
- **Vector Database**: 向量数据库集成
- **Fine-tuning Tools**: 微调工具集

## 🚀 快速安装

### 前置要求
- Node.js (v18+)
- Python (3.8+)
- Ollama (v0.1.0+)
- Obsidian (v1.0.0+)

### 一键安装
```bash
# 进入项目目录
cd /Users/zuimeidedeyihan/LuckyCommandCenter/cnsh-deployment

# 运行安装脚本
./install.sh
```

### 手动安装
#### 1. 安装 Ollama
```bash
# macOS
curl -fsSL https://ollama.ai/install.sh | sh

# 验证安装
ollama --version
```

#### 2. 下载 CNSH 模型
```bash
# 下载中文模型
ollama pull qwen:7b-chat
ollama pull chatglm3:6b

# 验证模型
ollama list
```

#### 3. 安装 CNSH 核心
```bash
# 克隆仓库
git clone https://gitee.com/cnsh-national/CNSH-National-Reference.git
cd CNSH-National-Reference

# 安装依赖
npm install
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，添加必要的配置
```

#### 4. 启动 CNSH 服务
```bash
# 启动 CNSH 核心服务
npm start

# 启动 Ollama 服务 (如果尚未运行)
ollama serve
```

#### 5. 安装 Obsidian 插件
1. 打开 Obsidian
2. 进入设置 → 第三方插件 → 浏览社区插件
3. 搜索 "CNSH Connector" 并安装
4. 在插件设置中配置 CNSH 服务器地址

## 📖 使用指南

### 1. 知识管理
- 在 Obsidian 中创建和管理笔记
- 使用 CNSH AI 助手生成内容摘要
- 自动分类和标签系统
- 知识图谱可视化

### 2. 智能交互
- 在 Obsidian 中直接与本地大模型对话
- 基于知识库的问答系统
- 智能笔记生成和内容扩展
- 文档相似性搜索

### 3. 数据处理
- 文档格式转换和标准化
- 内容提取和结构化
- 向量化处理和存储
- 知识关联和链接

## ⚙️ 配置选项

### .env 文件配置
```env
# CNSH 核心配置
CNSH_PORT=3000
CNSH_HOST=localhost
CNSH_LOG_LEVEL=info

# Ollama 配置
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen:7b-chat
OLLAMA_TIMEOUT=30

# Obsidian 插件配置
OBSIDIAN_VAULT_PATH=/path/to/your/vault
OBSIDIAN_API_KEY=your_api_key

# 数据库配置
DB_TYPE=sqlite
DB_PATH=./data/cnsh.db

# 数字主权配置
ENABLE_DIGITAL_SOVEREIGNTY=true
SUPPORTED_PLATFORMS=hongmeng,kunpeng,ascend
FINANCIAL_TECH_INTEGRATION=true
E_CNY_SUPPORT=true
```

### 插件配置
```json
{
  "cnsh_server": "http://localhost:3000",
  "api_key": "your_api_key",
  "model": "qwen:7b-chat",
  "vault_path": "/path/to/your/vault",
  "auto_tag": true,
  "smart_notes": true,
  "knowledge_graph": true,
  "digital_sovereignty": true,
  "e_cny_integration": true
}
```

## 🛠️ 故障排除

### 常见问题

1. **CNSH 服务无法启动**
   - 检查端口是否被占用
   - 确认所有依赖已正确安装
   - 查看 logs 文件夹中的错误日志

2. **Ollama 连接失败**
   - 确认 Ollama 服务正在运行
   - 检查网络连接和防火墙设置
   - 验证模型是否正确下载

3. **Obsidian 插件无法连接**
   - 检查 CNSH 服务器地址和端口
   - 确认 API 密钥是否正确
   - 查看浏览器控制台错误信息

### 日志查看
```bash
# CNSH 日志
tail -f logs/cnsh.log

# Ollama 日志
ollama logs
```

## 🔧 高级配置

### 1. 自定义模型
```bash
# 下载自定义模型
ollama pull your-custom-model

# 在 .env 文件中指定
OLLAMA_MODEL=your-custom-model
```

### 2. 插件开发
创建自定义插件扩展 CNSH 功能：
```javascript
// 示例插件结构
const plugin = {
  name: "My Custom Plugin",
  version: "1.0.0",
  initialize: function() {
    // 初始化代码
  },
  process: function(data) {
    // 处理数据
    return processedData;
  }
};

module.exports = plugin;
```

### 3. 数据备份
```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
tar -czf "cnsh-backup-$DATE.tar.gz" ./data ./logs
```

## 📈 性能优化

### 1. 模型优化
- 使用量化模型减少内存占用
- 调整上下文窗口大小
- 启用模型缓存

### 2. 数据库优化
- 创建适当的索引
- 定期清理无用数据
- 使用连接池

### 3. 网络优化
- 启用 GZIP 压缩
- 使用 CDN 加速静态资源
- 优化 API 请求

## 🌐 国产化支持

### 华为生态兼容
- 鸿蒙系统客户端支持
- 昇腾芯片模型加速
- 华为云服务集成
- 华为应用市场上架

### 国产硬件适配
- 鲲鹏处理器支持
- 国产操作系统兼容
- 国产数据库支持
- 国产加密算法集成

### 数字人民币集成
- e-CNY 支付场景支持
- 数字钱包接口
- 交易记录智能分析
- 金融知识图谱

## 🔒 安全与合规

### 数据安全
- 本地化部署保障数据主权
- 端到端加密保护隐私
- 符合《数据安全法》要求
- 通过国家信息安全认证

### 合规支持
- 遵循国家技术标准
- 支持等保合规要求
- 适配国产密码体系
- 符合金融监管要求

## 📞 社区资源

- [Gitee 主仓库](https://gitee.com/cnsh-national/CNSH-National-Reference)
- [GitHub 镜像](https://github.com/your-username/cnsh-deployment) (主版本与法律效力以 Gitee 为准)
- [官方文档](https://cnsh-docs.example.com)
- [社区论坛](https://forum.cnsh.example.com)
- [视频教程](https://bilibili.com/playlist?list=cnsh-tutorials)

## 📜 许可证

本项目采用 MIT 许可证。详细信息请参阅 [LICENSE](LICENSE) 文件。

## 🏆 致谢

感谢所有为国产化技术进步做出贡献的开发者和企业，特别是华为在国产技术生态建设中的引领作用。

---

**🇨🇳 本项目为中华人民共和国公民技术献礼，建议由国家授权机构或华为等国产可信企业托管演进。**

此项目为公民技术献礼，为国家数字主权建设贡献力量。

---

**【北辰-B 协议 · 国产通道校验 UID9622】**
**DNA 记忆卡片 · 坤（地）· 承载 · 归中 · 顺天**