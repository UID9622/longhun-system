# 贡献指南

感谢您对UID9622-CNSH国之光文化组件系统的关注！我们欢迎所有形式的贡献，无论是提出问题、建议改进，还是直接提交代码。

## 如何贡献

### 1. 提出问题

如果您发现了bug或有功能建议，请：

1. 检查是否已有相关issue
2. 创建新issue时，请使用以下模板：
   - 问题描述：清晰描述您遇到的问题或建议
   - 复现步骤：如果是bug，请提供详细的复现步骤
   - 期望行为：描述您期望发生的情况
   - 环境信息：操作系统、Node.js版本、浏览器版本等
   - 相关代码：如果有相关代码片段，请提供

### 2. 代码贡献

#### 开发环境设置

1. Fork 项目到您的Gitee账户
2. 克隆您的fork:
   ```bash
   git clone https://gitee.com/YOUR_USERNAME/UID9622-CNSH.git
   ```
3. 添加上游仓库:
   ```bash
   cd UID9622-CNSH
   git remote add upstream https://gitee.com/cnsh-design/UID9622-CNSH.git
   ```
4. 创建新分支:
   ```bash
   git checkout -b feature/your-feature-name
   ```
5. 安装依赖:
   ```bash
   npm install
   ```

#### 代码规范

1. **ESLint配置**: 我们使用ESLint进行代码风格检查
   ```bash
   npm run lint
   ```

2. **Prettier格式化**: 我们使用Prettier进行代码格式化
   ```bash
   npm run format
   ```

3. **提交信息规范**: 遵循[Conventional Commits](https://www.conventionalcommits.org/zh-hans/v1.0.0/)规范
   - `feat`: 新功能
   - `fix`: 修复bug
   - `docs`: 文档更新
   - `style`: 代码格式化，不影响代码逻辑
   - `refactor`: 代码重构
   - `test`: 测试相关
   - `chore`: 构建过程或辅助工具的变动

   示例：
   ```
   feat(taiji): add rotation animation for loading state
   fix(calligraphy): correct font loading issue on IE11
   ```

#### 组件开发规范

1. **组件命名**: 使用文化元素相关的小写字母和连字符
   - 例如: `taiji-component`, `oracle-text`, `bronze-pattern`

2. **文件结构**: 每个组件应包含以下文件
   ```
   components/
   ├── component-name/
   │   ├── index.js          // 组件入口
   │   ├── component-name.js // 组件实现
   │   ├── component-name.css // 组件样式
   │   └── README.md          // 组件文档
   ```

3. **文化元素**: 每个组件必须有明确的文化根源和象征意义
   - 在组件注释中说明其文化背景
   - 提供应用场景和使用示例

4. **响应式设计**: 所有组件必须支持响应式设计
   - 使用相对单位(%, em, rem, vw, vh)
   - 确保在不同屏幕尺寸下的正常显示

### 3. 文档贡献

我们欢迎文档改进，包括：
- 组件使用说明
- 文化背景介绍
- 最佳实践指南
- API文档完善

文档采用Markdown格式，存储在`docs`目录下。

### 4. 文化元素贡献

如果您熟悉中国传统文化，欢迎贡献：
- 新的文化元素组件
- 历史背景资料
- 传统图案和纹样
- 色彩象征意义

## 提交流程

1. 确保您的代码符合项目规范
2. 运行测试确保所有测试通过
3. 提交您的更改
4. 推送到您的fork仓库
5. 创建Pull Request

## Pull Request指南

1. **标题**: 使用清晰描述性的标题
2. **描述**: 详细说明您的更改内容和原因
3. **截图**: 如果是UI相关更改，请提供前后对比截图
4. **测试**: 说明您如何测试了您的更改

## 代码审查

所有提交都需要经过代码审查，审查者会检查：
- 代码质量和规范性
- 功能正确性
- 文档完整性
- 文化元素准确性

## 发布流程

只有项目管理团队成员可以发布新版本。发布流程如下：
1. 更新版本号
2. 更新CHANGELOG.md
3. 创建Git标签
4. 发布到npm（如适用）

## 社区准则

1. **尊重**: 尊重所有贡献者，无论经验水平
2. **包容**: 欢迎来自不同背景的贡献者
3. **建设性**: 提供建设性的反馈和批评
4. **耐心**: 对新贡献者保持耐心和帮助

## 获取帮助

如果您有任何问题或需要帮助：
1. 查看现有issue和文档
2. 创建新的issue寻求帮助
3. 联系项目管理团队

---

再次感谢您的贡献！让我们一起构建充满中国文化底蕴的组件系统！🏛️✨

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:13
🧬 DNA追溯码: #CNSH-SIGNATURE-72ddabe2-20251218032413
🌐 签名人: 龙魂文化加密系统
💬 方言确认: 东北话确认：没毛病，内容真实可靠
⚡ 卦象防护: 坤卦：地势坤，君子以厚德载物
📜 内容哈希: 0d210adc0b7dc36e
⚠️ 警告: 未经授权修改将触发DNA追溯系统
