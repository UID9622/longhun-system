# 贡献指南

感谢您对太极八卦易经甲骨文开源系统的关注！我们欢迎所有形式的贡献。

## 🌟 贡献方式

### 代码贡献

1. **Fork 本项目**
2. **创建功能分支** (`git checkout -b feature/AmazingFeature`)
3. **提交更改** (`git commit -m 'Add some AmazingFeature'`)
4. **推送到分支** (`git push origin feature/AmazingFeature`)
5. **创建 Pull Request**

### 文档贡献

- 改进 README.md
- 添加使用示例
- 翻译文档
- 修正错误

### 数据贡献

- 补充甲骨文字库
- 完善易经解释
- 提供历史文献资料

## 📋 开发规范

### 代码风格

- 使用 UTF-8 编码
- JavaScript 使用 ES6+ 语法
- 代码注释使用中文
- 文件名使用英文小写+下划线

### 提交规范

```
type(scope): description

feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试
chore: 构建过程或辅助工具的变动
```

### 示例

```
feat(oracle): 添加新的甲骨文字符识别功能
fix(yijing): 修复占卜算法的随机数种子问题
docs(readme): 更新安装说明
```

## 🎯 贡献方向

### 高优先级

- [ ] 完善甲骨文字符数据库
- [ ] 增加更多易经解释内容
- [ ] 优化移动端适配
- [ ] 添加多语言支持

### 中优先级

- [ ] 实现离线功能
- [ ] 添加数据导出功能
- [ ] 优化性能
- [ ] 增加动画效果

### 低优先级

- [ ] 添加主题切换
- [ ] 实现数据同步
- [ ] 开发移动APP
- [ ] 集成AI功能

## 🔧 开发环境

### 必需软件

- Node.js >= 14.0.0
- npm >= 6.0.0

### 安装步骤

```bash
# 克隆项目
git clone https://gitee.com/open-source/taichi-jiagua-oracle.git

# 进入目录
cd taichi-jiagua-oracle

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 📝 文件结构

```
├── src/
│   ├── core/           # 核心算法
│   │   ├── oracle.js   # 甲骨文处理
│   │   └── yijing.js   # 易经算法
│   ├── visual/         # 可视化组件
│   │   ├── taichi.js   # 太极图
│   │   └── bagua.js    # 八卦图
│   └── data/           # 数据文件
│       ├── oracle.json # 甲骨文字库
│       └── yijing.json # 易经数据
├── public/             # 前端资源
│   ├── styles/         # 样式文件
│   ├── scripts/        # JavaScript文件
│   └── index.html      # 主页面
├── docs/               # 文档
└── server.js           # 服务器文件
```

## 🧪 测试

### 运行测试

```bash
# 运行所有测试
npm test

# 运行特定测试
npm test -- --grep "oracle"
```

### 编写测试

```javascript
// 示例测试
describe('OracleSystem', () => {
  test('should find oracle character', () => {
    const result = oracleSystem.findOracleChar('日');
    expect(result).toBeDefined();
  });
});
```

## 📤 发布流程

1. 确保所有测试通过
2. 更新版本号
3. 更新 CHANGELOG.md
4. 创建 Git tag
5. 推送到远程仓库

## 🤝 社区准则

### 行为准则

- 尊重不同观点
- 保持友好和包容
- 建设性地提出建议
- 遵循项目目标

### 沟通方式

- GitHub Issues: 报告bug和功能请求
- GitHub Discussions: 一般讨论
- Pull Request: 代码审查

## 📞 联系方式

如有问题，请通过以下方式联系：

- GitHub Issues
- 项目维护者邮箱

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

---

**让我们一起传承中华文化，用技术点亮古老智慧！** ✨

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:12
🧬 DNA追溯码: #CNSH-SIGNATURE-7c7e67a5-20251218032412
🌐 签名人: 龙魂文化加密系统
💬 方言确认: 东北话确认：没毛病，内容真实可靠
⚡ 卦象防护: 蒙卦：山下出泉，君子以果行育德
📜 内容哈希: 4bce4cdef5aeaff6
⚠️ 警告: 未经授权修改将触发DNA追溯系统
