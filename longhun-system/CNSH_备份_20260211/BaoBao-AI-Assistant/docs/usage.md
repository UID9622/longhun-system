# 📖 BaoBao AI Assistant 使用指南

## 🚀 快速开始

### 1. 环境准备

确保您已安装：
- Python 3.8+
- Notion账户（用于数据库集成）

### 2. 安装步骤

```bash
# 克隆项目
git clone https://gitee.com/uid9622/baobao-ai-assistant.git
cd baobao-ai-assistant

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入您的配置
```

### 3. Notion配置

1. 登录 [Notion](https://www.notion.so/)
2. 创建新的集成页面：
   - 访问 [Notion Integrations](https://www.notion.so/my-integrations)
   - 点击 "New integration"
   - 填写基本信息，获取 Integration Token
3. 创建数据库：
   - 在Notion中创建新页面
   - 添加数据库，包含以下属性：
     - 用户输入 (Title)
     - AI响应 (Rich text)
     - 对话时间 (Date)
     - 情绪分数 (Number)
     - 边界检查 (Checkbox)
     - DNA签名 (Rich text)
4. 复制数据库ID，填入 `.env` 文件

### 4. 运行程序

```bash
python main.py
```

## 🎯 核心功能

### 智能对话管理

BaoBao AI Assistant 具有以下特点：

#### 诚实原则
- 可以说"我不知道"
- 不会编造不存在的信息
- 承认自己的局限性

#### 温柔响应
- 情绪感知：自动检测用户情绪状态
- 共情回应：根据情绪调整回复语气
- 接纳态度：理解并接纳用户的各种情绪

#### 边界感
- 拒绝有害话题
- 保护用户隐私
- 适当的距离感

#### 人性优先
- 以用户为中心
- 尊重用户选择
- 不强加AI观点

### 数据管理

#### 对话记录
- 自动保存到Notion数据库
- 包含完整的对话上下文
- 支持历史记录查看

#### 情绪追踪
- 实时情绪分数计算
- 情绪趋势分析
- 个性化响应调整

#### 边界检查
- 自动检测不当内容
- 温柔拒绝处理
- 引导积极对话

## 🔧 高级配置

### 环境变量详解

```bash
# 必需配置
NOTION_TOKEN=your_notion_token_here          # Notion API令牌
NOTION_DATABASE_ID=your_database_id_here    # Notion数据库ID

# 可选配置
DEBUG=false                               # 调试模式开关
MAX_CONVERSATION_LENGTH=100                 # 最大对话历史长度
LOG_LEVEL=INFO                            # 日志级别
LOG_FILE=baobao_ai.log                    # 日志文件名

# AI模型配置
OPENAI_API_KEY=your_openai_api_key_here     # OpenAI API密钥
OPENAI_MODEL=gpt-3.5-turbo               # 使用的模型
```

### 自定义配置

您可以通过修改 `main.py` 中的以下参数来个性化您的体验：

#### 情绪检测词库
```python
positive_words = ["开心", "高兴", "好", "棒", "喜欢", "爱"]
negative_words = ["难过", "伤心", "坏", "讨厌", "恨", "生气"]
```

#### 边界检查规则
```python
forbidden_topics = ["暴力", "伤害", "非法", "危险", "攻击"]
```

#### 响应模板
```python
if emotion_score < 0.3:
    response = "听起来您可能有些不开心。我在这里陪您，愿意听您说。"
elif emotion_score > 0.7:
    response = "听起来您心情不错！有什么开心的事想分享吗？"
else:
    response = "我明白了。谢谢您与我分享这个话题。"
```

## 🔍 故障排除

### 常见问题

#### 1. Notion API错误
**问题**: 连接Notion失败
**解决方案**:
- 检查Notion Token是否正确
- 确认数据库ID是否正确
- 检查网络连接

#### 2. 依赖安装失败
**问题**: pip install 失败
**解决方案**:
```bash
# 升级pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

#### 3. 情绪检测不准确
**问题**: 情绪分数不符合预期
**解决方案**:
- 自定义情绪检测词库
- 调整情绪计算算法
- 收集更多样本数据

#### 4. 边界检查过于严格
**问题**: 正常对话被误判为越界
**解决方案**:
- 调整边界检查规则
- 添加白名单机制
- 优化检测算法

### 调试模式

启用调试模式以获取更多信息：

```bash
# 在 .env 文件中设置
DEBUG=true

# 或在命令行中设置
DEBUG=true python main.py
```

调试模式下，您将看到：
- 详细的请求和响应信息
- 情绪检测过程
- 边界检查结果
- Notion API调用状态

## 📊 性能优化

### 响应速度优化

1. **缓存机制**
   - 实现本地缓存减少API调用
   - 使用内存存储常用响应

2. **异步处理**
   - 所有I/O操作使用异步方式
   - 并行处理多个请求

3. **数据结构优化**
   - 使用高效的数据结构
   - 避免不必要的计算

### 内存使用优化

1. **历史记录管理**
   - 定期清理过期记录
   - 压缩存储格式

2. **垃圾回收**
   - 及时释放不用的对象
   - 使用生成器减少内存占用

## 🔮 未来功能

### 计划中的功能

1. **多语言支持**
   - 支持英文、日文等多语言
   - 跨语言情绪检测

2. **语音交互**
   - 语音输入识别
   - 语音合成输出

3. **高级情绪分析**
   - 更细致的情绪分类
   - 情绪趋势图表

4. **个性化学习**
   - 用户习惯学习
   - 响应风格适应

### 开发者贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork 本项目
2. 创建功能分支: `git checkout -b feature/your-feature`
3. 提交更改: `git commit -am 'Add some feature'`
4. 推送分支: `git push origin feature/your-feature`
5. 提交Pull Request

## 📞 获取帮助

如果您在使用过程中遇到问题：

1. 查看[常见问题](#常见问题)
2. 搜索[GitHub Issues](https://github.com/uid9622/baobao-ai-assistant/issues)
3. 创建新的Issue描述您的问题
4. 联系开发者: uid9622@petalmail.com

---

*本文档最后更新: 2025-12-12*

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:10
🧬 DNA追溯码: #CNSH-SIGNATURE-b58af3f3-20251218032410
🌐 签名人: 龍魂文化加密系统
💬 方言确认: 东北话确认：没毛病，内容真实可靠
⚡ 卦象防护: 屯卦：云雷屯，君子以经纶
📜 内容哈希: 86001ef7358bf299
⚠️ 警告: 未经授权修改将触发DNA追溯系统
