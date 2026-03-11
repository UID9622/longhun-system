# 🤝 贡献指南

## 🎯 协作原则

**核心理念**：自己认的不怕拿走，开放共享，但要守住底线

**确认码**：`#ZHUGEXIN⚡️2025-CODEBUDDY-COLLAB-RULES-V1.0`

---

## ✅ 可以贡献的内容

### 🎨 前端开发

- UI组件优化（按钮、卡片、导航栏）
- 响应式布局改进
- 数据可视化图表
- 用户体验优化

### 🔧 后端开发

- API接口扩展
- 数据处理逻辑
- 性能优化
- 错误处理机制

### 📚 文档贡献

- 技术文档完善
- 使用教程编写
- API文档补充
- 代码注释优化

### 🚀 工具和脚本

- 自动化部署脚本
- 开发工具配置
- 测试用例编写
- CI/CD流程

---

## 🚫 禁止提交的内容

### 个人隐私信息

- ❌ 真实姓名、身份证、地址
- ❌ 手机号、邮箱、微信等联系方式
- ❌ 家庭成员信息

### 敏感配置

- ❌ API密钥（Notion/OpenAI/Claude等）
- ❌ 数据库连接字符串
- ❌ 加密私钥、证书文件

### 商业机密

- ❌ 真实的业务数据
- ❌ 核心算法完整实现
- ❌ 战略规划细节

---

## 🔐 脱敏处理规则

### 环境变量

```typescript
// ❌ 错误写法
const API_URL = "https://secret-api.com";
const TOKEN = "secret_abc123";

// ✅ 正确写法
const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";
const TOKEN = process.env.API_TOKEN || "";
```

### 数据示例

```typescript
// ❌ 错误写法
const userData = {
  name: "诸葛鑫",
  phone: "138****8888",
  email: "lucky@example.com"
};

// ✅ 正确写法
const userData = {
  name: "示例用户",
  phone: "138****[已隐藏]",
  email: "example@domain.com"
};
```

---

## 🔄 贡献流程

### 1. Fork 仓库

点击 GitHub 页面右上角的 "Fork" 按钮

### 2. 创建分支

```bash
git checkout -b feature/your-feature-name
```

### 3. 开发和测试

- 确保代码符合项目规范
- 添加必要的测试用例
- 验证脱敏处理

### 4. 提交代码

```bash
git add .
git commit -m "feat: 添加新功能描述"
```

### 5. 推送和PR

```bash
git push origin feature/your-feature-name
```

在 GitHub 创建 Pull Request

---

## 📋 提交前检查清单

每次提交前，请确认以下项目：

- [ ] 代码中无个人信息（姓名、手机、地址）
- [ ] 代码中无API密钥（已用环境变量）
- [ ] 代码中无真实数据（已用示例数据）
- [ ] 文档中无商业机密（只有技术实现）
- [ ] 所有敏感内容已脱敏处理

**通过所有检查 → 可以提交 ✅**

---

## 🎨 代码规范

### TypeScript

```typescript
// ✅ 使用接口定义类型
interface SystemStatus {
  status: string;
  version: string;
  system_id: string;
}

// ✅ 使用函数组件
const Dashboard: React.FC = () => {
  // 组件逻辑
};
```

### React Hooks

```typescript
// ✅ 正确使用 useEffect
useEffect(() => {
  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/';
  // API调用
}, []);
```

### 样式规范

```tsx
// ✅ 使用 Ant Design 组件
import { Card, Row, Col } from 'antd';

// ✅ 内联样式对象
const cardStyle = {
  textAlign: 'center',
  padding: '16px'
};
```

---

## 📞 联系方式

- 技术问题：通过 GitHub Issues
- 代码审查：Maintainer 会及时响应
- 安全问题：请发送邮件至安全邮箱

---

## 💡 贡献者激励

- 🌟 贡献者会被添加到项目贡献者列表
- 🏆 优秀贡献有机会成为项目 Maintainer
- 📚 技术文章会被推荐到官方博客

---

**DNA追溯码**：`#ZHUGEXIN⚡️2025-CONTRIBUTION-GUIDELINES-V1.0`