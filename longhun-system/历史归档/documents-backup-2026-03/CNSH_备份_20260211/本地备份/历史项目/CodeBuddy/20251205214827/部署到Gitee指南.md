# 部署到Gitee指南

本指南将帮助您将UID9622-CNSH项目部署到Gitee平台。

## 📋 准备工作

1. **Gitee账户**: 确保您已注册Gitee账户
2. **Git配置**: 确保您的Git已正确配置用户信息
   ```bash
   git config --global user.name "您的用户名"
   git config --global user.email "您的邮箱"
   ```

## 🚀 部署步骤

### 1. 在Gitee创建新仓库

1. 登录您的Gitee账户
2. 点击右上角的"+"号，选择"新建仓库"
3. 填写仓库信息：
   - **仓库名称**: `UID9622-CNSH`
   - **路径**: `UID9622-CNSH`
   - **简介**: `UID9622-CNSH 国之光文化组件系统 - 基于五千年中华文明的文化组件库`
   - **是否公开**: 选择"公开"或"私有"
   - **初始化仓库**: **不要**勾选任何初始化选项（README、.gitignore等）

### 2. 关联本地仓库与远程仓库

创建仓库后，Gitee会显示仓库地址。执行以下命令关联远程仓库：

```bash
# 方法1: 使用SSH（推荐，如果您已配置SSH密钥）
git remote add origin git@gitee.com:您的用户名/UID9622-CNSH.git

# 方法2: 使用HTTPS
git remote add origin https://gitee.com/您的用户名/UID9622-CNSH.git
```

### 3. 推送代码到Gitee

```bash
# 推送本地main分支到远程origin仓库
git push -u origin main
```

### 4. 验证部署

1. 访问您的Gitee仓库页面
2. 确认所有文件已成功上传
3. 检查README.md是否正确显示

## 🛠️ 高级配置

### 设置Gitee Pages

如果您想启用Gitee Pages来部署项目文档：

1. 在仓库页面点击"服务" → "Gitee Pages"
2. 选择"部署分支": `main`
3. 选择"部署目录": `/`（根目录）
4. 点击"启动"或"更新"
5. 部署成功后，可通过 `https://您的用户名.gitee.io/UID9622-CNSH` 访问

### 配置协作者

1. 在仓库页面点击"设置" → "仓库成员管理"
2. 点击"添加仓库成员"
3. 输入协作者的Gitee用户名
4. 设置适当的权限（开发者/管理者）

### 设置保护分支

1. 在仓库页面点击"设置" → "分支管理"
2. 添加分支保护规则
3. 选择`main`分支
4. 配置保护规则（如需要审查才能合并）

## 🔄 持续更新

### 日常开发流程

```bash
# 1. 拉取最新更改
git pull origin main

# 2. 创建新分支进行开发
git checkout -b feature/新功能名称

# 3. 开发完成后，提交更改
git add .
git commit -m "feat: 添加新功能描述"

# 4. 推送分支到远程
git push origin feature/新功能名称

# 5. 在Gitee上创建Pull Request
# 6. 合并到main分支后，拉取最新代码
git checkout main
git pull origin main
```

### 版本发布

```bash
# 1. 创建版本标签
git tag -a v1.0.0 -m "发布第一个正式版本"

# 2. 推送标签到远程
git push origin v1.0.0

# 3. 在Gitee上创建Release
# 访问仓库 → 发行版 → 创建发行版
# 选择对应标签，填写发行说明
```

## 📝 团队协作最佳实践

### 提交信息规范

我们遵循[Conventional Commits](https://www.conventionalcommits.org/zh-hans/v1.0.0/)规范：

```
feat(taiji): 添加太极组件旋转动画效果
fix(calligraphy): 修复甲骨文组件在IE11上的兼容性问题
docs(readme): 更新安装说明
```

### 分支管理

- `main`: 主分支，始终保持稳定可发布状态
- `develop`: 开发分支，用于集成新功能
- `feature/*`: 功能分支，用于开发新功能
- `bugfix/*`: 修复分支，用于修复bug
- `release/*`: 发布分支，用于发布准备

### 代码审查

所有合并到`main`分支的代码都需要经过代码审查：

1. 创建Pull Request
2. 至少需要一位团队成员审查
3. 通过所有自动化测试
4. 审查者批准后才能合并

## 🔗 相关链接

- [Gitee官方文档](https://gitee.com/help/)
- [Git使用教程](https://git-scm.com/book/zh/v2)
- [Conventional Commits规范](https://www.conventionalcommits.org/zh-hans/v1.0.0/)
- [项目仓库地址](https://gitee.com/您的用户名/UID9622-CNSH)

---

如有任何问题，请在项目Issues中提出，我们会及时回复和帮助解决。

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:13
🧬 DNA追溯码: #CNSH-SIGNATURE-f0e1e53f-20251218032413
🌐 签名人: 龍魂文化加密系统
💬 方言确认: 四川话确认：莫得问题，内容真实可靠
⚡ 卦象防护: 蒙卦：山下出泉，君子以果行育德
📜 内容哈希: 497d3adfe1e0986c
⚠️ 警告: 未经授权修改将触发DNA追溯系统
