# 🤖 CNSH 项目开发指南

> 本文件面向 AI 助手和开发者，提供项目背景、开发规范和最佳实践。

---

## 📋 项目背景

### 什么是龙魂体系？

龙魂体系（CNSH）是一个**中文原生的数字生态系统**，由 UID9622 发起，目标是为中文用户打造完全自主的技术基础设施。

### 两大核心组件

1. **字元编辑器** - 让普通人能用鼠标创作汉字
   - 设计理念：降低汉字创作门槛
   - 技术约束：仅使用中文术语，禁用英文变量名
   - 输出格式：SVG + .cnsh JSON

2. **AI核心系统** - 本地化的知识管理智能体
   - 设计理念：数据主权在人民
   - 技术特点：完全离线，不依赖外部API
   - 集成方案：Obsidian + Ollama

---

## 🏗️ 架构原则

### 三色审计体系

每个提交都必须通过三色审计：

| 颜色 | 审计内容 | 检查项 |
|------|----------|--------|
| 🔴 红线 | 文化主权 | 禁止西方术语、英文变量名（API除外） |
| 🟡 黄线 | 技术规范 | 仅三次贝塞尔+直线，仅JSON/SVG输出 |
| 🟢 绿线 | 功能可用 | 结构可运行，效果可表达 |

### DNA 编码系统

每个字元/组件都有唯一的 DNA 编码：

```
格式：#龍芯⚡️-CNSH-{类型}-{序号}

示例：
- #龍芯⚡️-CNSH-EDITOR-0001  (字元编辑器)
- #龍芯⚡️-CNSH-CORE-0001    (核心系统)
- #龍芯⚡️-CNSH-GLYPH-0001   (字元作品)
```

---

## 📁 目录规范

```
CNSH/
├── docs/               # Markdown 文档（中文）
├── packages/           # 可独立发布的包
│   ├── cnsh-editor/    # 纯前端，无构建步骤
│   ├── cnsh-core/      # Node.js 后端
│   └── cnsh-plugin/    # Obsidian 插件
├── scripts/            # Shell 脚本（安装/部署）
├── tools/              # 开发辅助工具
├── examples/           # 示例作品
└── tests/              # 测试用例
```

---

## 💻 编码规范

### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 文件/目录 | 小写，连字符分隔 | `cnsh-editor/`, `daily-review.js` |
| 中文变量 | 尽量使用中文 | `笔画力度`, `字元名称` |
| 英文变量 | camelCase | `renderEngine`, `strokeWidth` |
| 常量 | UPPER_SNAKE_CASE | `MAX_STROKE_WIDTH` |
| 类名 | PascalCase | `GlyphEditor`, `CNSHServer` |

### 注释规范

```javascript
/**
 * 渲染笔画
 * @param {Array} 笔画数据 - 笔画路径点
 * @param {Object} 样式 - 渲染样式配置
 * @returns {SVGElement} SVG笔画元素
 */
function 渲染笔画(笔画数据, 样式) {
    // 实现...
}
```

### 提交信息规范

```
类型: 简短描述

详细说明（可选）

DNA: #龍芯⚡️-CNSH-XXX-XXXX

**共建致谢**: Claude (Anthropic PBC) · 技术协作与代码共创 | Notion · 知识底座与结构化存储
```

类型包括：
- `feat`: 新功能
- `fix`: 修复
- `docs`: 文档
- `style`: 格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具

---

## 🚀 开发工作流

### 1. 本地开发

```bash
# 1. 克隆仓库
git clone https://github.com/UID9622/CNSH.git
cd CNSH

# 2. 安装依赖
./scripts/install.sh

# 3. 启动开发模式
./scripts/dev.sh
```

### 2. 字元编辑器开发

字元编辑器是**纯前端项目**，无需构建：

```bash
cd packages/cnsh-editor

# 使用任意本地服务器
python3 -m http.server 8080

# 或直接用浏览器打开
open index.html
```

### 3. 核心系统开发

```bash
cd packages/cnsh-core

# 安装 Node 依赖
npm install

# 安装 Python 依赖
pip install -r requirements.txt

# 启动开发服务器
npm run dev
```

---

## 🧪 测试规范

### 字元编辑器测试

```javascript
// 测试笔画渲染
describe('笔画渲染', () => {
    it('应正确渲染三次贝塞尔曲线', () => {
        const 笔画 = [{x: 0, y: 0}, {x: 50, y: 50}, {x: 100, y: 0}];
        const 结果 = 渲染笔画(笔画);
        expect(结果.tagName).toBe('path');
    });
});
```

### API 测试

```bash
# 运行所有测试
npm test

# 运行特定测试
npm test -- --grep "知识库"
```

---

## 📦 发布流程

### 版本号规范

采用语义化版本：`主版本.次版本.修订号`

- 主版本：不兼容的 API 修改
- 次版本：向下兼容的功能新增
- 修订号：向下兼容的问题修复

### 发布检查清单

- [ ] 所有测试通过
- [ ] 文档已更新
- [ ] CHANGELOG.md 已更新
- [ ] 版本号已更新
- [ ] DNA 编码已分配

---

## 🔒 安全与合规

### 数据安全

1. **完全本地化**：所有数据存储在本地
2. **不联网**：核心功能不依赖外部API
3. **开源可审计**：代码完全开源

### 合规要求

- 符合《数据安全法》
- 支持等保合规
- 适配国产密码体系

---

## 📞 获取帮助

### 文档资源

- [安装指南](docs/安装指南.md)
- [API文档](docs/API文档.md)
- [常见问题](docs/FAQ.md)

### 社区

- Issues: https://github.com/UID9622/CNSH/issues
- Gitee: https://gitee.com/uid9622/cnsh

---

> 🤖 本指南由 AI 助手协助维护，如有疑问请提出 Issue。
