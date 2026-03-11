# 🤝 BaoBao AI Assistant 贡献指南

## 🌟 欢迎贡献

感谢您对 BaoBao AI Assistant 的关注！我们非常欢迎各种形式的贡献，包括但不限于：

- 🐛 Bug报告
- 💡 功能建议
- 📝 文档改进
- 🧪 测试用例
- 💻 代码贡献
- 🌐 翻译支持

## 🚀 快速开始

### 开发环境设置

1. **Fork 项目**
   ```bash
   # Gitee (推荐)
   git clone https://gitee.com/your-username/baobao-ai-assistant.git
   
   # 或 GitHub
   git clone https://github.com/your-username/baobao-ai-assistant.git
   ```

2. **安装依赖**
   ```bash
   cd baobao-ai-assistant
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或 venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # 开发依赖
   ```

3. **配置环境**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，填入您的配置
   ```

4. **运行测试**
   ```bash
   pytest
   ```

## 🎯 贡献类型

### 1. Bug 报告

在提交 Bug 报告前，请确保：

- [ ] 检查是否已存在相关 Issue
- [ ] 使用最新的代码版本
- [ ] 提供详细的复现步骤
- [ ] 包含相关的错误信息
- [ ] 说明您的运行环境

**Bug 报告模板：**

```markdown
## Bug 描述
简要描述遇到的问题

## 复现步骤
1. 执行 '...'
2. 点击 '....'
3. 滚动到 '....'
4. 看到错误

## 期望行为
描述您期望发生的行为

## 实际行为
描述实际发生的行为

## 环境信息
- 操作系统: [例如 Windows 11, macOS 13.0]
- Python 版本: [例如 3.9.0]
- 项目版本: [例如 v1.0.0]

## 附加信息
- 相关截图
- 错误日志
- 其他相关信息
```

### 2. 功能建议

在提交功能建议前，请考虑：

- [ ] 该功能是否符合项目目标
- [ ] 是否已有类似的 Issue
- [ ] 是否愿意参与实现

**功能建议模板：**

```markdown
## 功能描述
简要描述您希望添加的功能

## 使用场景
描述该功能的使用场景和价值

## 预期效果
描述该功能实现后的效果

## 实现建议
如果您有实现思路，请简要说明

## 附加信息
任何相关的参考资料或示例
```

### 3. 代码贡献

#### 代码规范

请遵循以下代码规范：

1. **Python 代码风格**
   - 使用 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 规范
   - 使用 [Black](https://black.readthedocs.io/) 进行格式化
   - 使用 [flake8](https://flake8.pycqa.org/) 进行检查

2. **命名规范**
   - 类名使用 PascalCase
   - 函数和变量使用 snake_case
   - 常量使用 UPPER_CASE

3. **文档字符串**
   - 所有公共函数和类必须有文档字符串
   - 使用 Google 风格的文档字符串
   - 包含参数类型和返回值说明

4. **类型提示**
   - 使用类型提示 (Type Hints)
   - 导入 `typing` 模块中的必要类型

#### 提交规范

1. **分支命名**
   - 功能分支: `feature/功能名称`
   - 修复分支: `fix/问题描述`
   - 文档分支: `docs/文档说明`

2. **提交信息**
   ```
   类型(范围): 简短描述
   
   详细描述（可选）
   
   Closes #Issue编号
   ```
   
   类型包括：
   - `feat`: 新功能
   - `fix`: Bug 修复
   - `docs`: 文档更新
   - `style`: 代码格式调整
   - `refactor`: 代码重构
   - `test`: 测试相关
   - `chore`: 构建或工具相关

3. **示例提交信息**
   ```
   feat(emotion): 增加情绪分析功能
   
   - 添加基础情绪检测算法
   - 支持中英文情绪分析
   - 增加相关测试用例
   
   Closes #123
   ```

#### Pull Request 流程

1. **创建 Pull Request**
   - 从您的功能分支向主分支提交 PR
   - 填写 PR 模板中的所有信息
   - 关联相关的 Issue

2. **代码审查**
   - 确保所有检查通过
   - 响应审查意见
   - 根据反馈进行修改

3. **合并**
   - 审查通过后，维护者会合并代码
   - 删除已合并的分支

### 4. 文档贡献

#### 文档类型

1. **API 文档**
   - 新增 API 的详细说明
   - 包含使用示例
   - 说明参数和返回值

2. **用户指南**
   - 功能使用说明
   - 配置指南
   - 故障排除

3. **开发者文档**
   - 架构说明
   - 开发指南
   - 贡献指南

#### 文档规范

1. **Markdown 格式**
   - 使用标准的 Markdown 语法
   - 合理使用标题层级
   - 添加目录（对于长文档）

2. **代码示例**
   - 提供完整可运行的示例
   - 包含必要的导入和配置
   - 添加适当的注释

3. **图片和图表**
   - 使用清晰有意义的图片
   - 提供图片的替代文本
   - 控制图片大小

### 5. 测试贡献

#### 测试类型

1. **单元测试**
   - 测试单个函数或方法
   - 覆盖正常和异常情况
   - 使用 mock 隔离依赖

2. **集成测试**
   - 测试多个组件的协作
   - 验证端到端功能
   - 使用真实的依赖

3. **性能测试**
   - 测试关键路径的性能
   - 验证资源使用情况
   - 对比优化前后的差异

#### 测试规范

1. **测试框架**
   - 使用 [pytest](https://pytest.org/) 框架
   - 遵循 pytest 的命名约定
   - 使用 fixtures 进行测试设置

2. **测试编写**
   - 每个测试只验证一个功能
   - 使用描述性的测试名称
   - 包含必要的断言和错误消息

3. **覆盖率要求**
   - 新代码的测试覆盖率不低于 80%
   - 关键路径的测试覆盖率为 100%
   - 定期检查覆盖率报告

## 🔧 开发工具

### 代码格式化

```bash
# 使用 Black 格式化代码
black .

# 检查格式是否符合规范
black --check .
```

### 代码检查

```bash
# 使用 flake8 检查代码质量
flake8 .

# 详细检查报告
flake8 --show-source --statistics .
```

### 测试运行

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_main.py

# 运行测试并生成覆盖率报告
pytest --cov=. --cov-report=html
```

### 文档构建

```bash
# 构建文档
mkdocs build

# 预览文档
mkdocs serve
```

## 🎖️ 贡献者认可

我们珍视每一位贡献者！您的贡献将在以下方式得到认可：

### 1. 贡献者列表

在 README.md 中维护贡献者列表，按贡献类型分类：

- 💻 代码贡献
- 📝 文档贡献
- 🐛 Bug 报告
- 💡 功能建议
- 🌐 翻译支持

### 2. 发布说明

在每个版本的发布说明中，感谢相应的贡献者：

```markdown
## v1.1.0 (2025-12-20)

### 新增功能
- 情绪分析功能 (感谢 @username)
- 边界检查机制 (感谢 @username)

### Bug 修复
- 修复 Notion API 连接问题 (感谢 @username)

### 文档更新
- 更新 API 文档 (感谢 @username)
```

### 3. 特殊徽章

对于重大贡献，我们会授予特殊徽章：

- 🏆 核心贡献者
- 🌟 活跃贡献者
- 🎯 问题解决专家
- 📚 文档大师

## 🌍 社区参与

### 讨论区

我们欢迎在各种渠道进行讨论：

- 🇨🇳 [Gitee Issues](https://gitee.com/uid9622/baobao-ai-assistant/issues)
- 🌍 [GitHub Issues](https://github.com/uid9622/baobao-ai-assistant/issues)
- 📧 邮箱: uid9622@petalmail.com

### 行为准则

我们致力于创建友好、包容的社区环境：

1. **尊重他人**
   - 尊重不同的观点和经验
   - 使用包容性的语言
   - 关注问题而非个人

2. **建设性交流**
   - 提供建设性的反馈
   - 承认自己的错误
   - 乐于学习和分享

3. **专业精神**
   - 遵循专业标准
   - 保护用户隐私
   - 维护项目声誉

## 📞 联系方式

如果您有任何问题或建议：

- 📧 邮箱: uid9622@petalmail.com
- 🇨🇳 Gitee: https://gitee.com/uid9622/baobao-ai-assistant
- 🌍 GitHub: https://github.com/uid9622/baobao-ai-assistant

---

**感谢您的贡献！让我们一起构建更好的人机交互体验！** 🎉

*贡献指南最后更新: 2025-12-12*

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:10
🧬 DNA追溯码: #CNSH-SIGNATURE-c3884966-20251218032410
🌐 签名人: 龙魂文化加密系统
💬 方言确认: 四川话确认：莫得问题，内容真实可靠
⚡ 卦象防护: 屯卦：云雷屯，君子以经纶
📜 内容哈希: 86f071c5caffd956
⚠️ 警告: 未经授权修改将触发DNA追溯系统
