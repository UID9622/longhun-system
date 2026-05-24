# CNSH Core 推送命令指南

## 🚀 代码推送完整流程

### 1. 确认当前状态

```bash
# 进入项目目录
cd /Users/zuimeidedeyihan/LuckyCommandCenter/cnsh-deployment

# 查看当前状态
git status

# 查看提交历史
git log --oneline
```

### 2. 创建 Gitee 仓库

**重要**: 首先需要在 Gitee 网站上手动创建仓库！

1. 访问 [Gitee 官网](https://gitee.com)
2. 登录您的账号
3. 点击右上角 "+" → "新建仓库"
4. 填写仓库信息：
   - 仓库名称：`CNSH-National-Reference`
   - 简介：`CNSH Core - 国产本地AI知识管理系统，数字主权技术献礼`
   - 设为公开仓库
   - 不初始化 README（我们已有）

### 3. 配置远程仓库地址

```bash
# 删除当前的远程仓库配置
git remote remove origin

# 添加您的实际仓库地址（请替换 [您的用户名]）
git remote add origin https://gitee.com/[您的用户名]/CNSH-National-Reference.git

# 确认远程仓库地址
git remote -v
```

### 4. 推送代码到 Gitee

```bash
# 推送主分支并设置上游分支
git push -u origin main

# 如果推送成功，应该看到类似输出：
# Enumerating objects: 30, done.
# Counting objects: 100% (30/30), done.
# ...
# To https://gitee.com/[您的用户名]/CNSH-National-Reference.git
#  * [new branch]      main -> main
```

### 5. 创建版本标签

```bash
# 创建 v1.0.0 标签
git tag -a v1.0.0 -m "CNSH Core v1.0.0 - 初始发布版本"

# 推送标签到远程仓库
git push origin v1.0.0

# 或者推送所有标签
git push origin --tags
```

## 🔧 故障排除

### 问题 1：认证失败
```bash
# 如果提示用户名或密码错误，可以尝试使用个人访问令牌
# 1. 在 Gitee 上生成个人访问令牌
# 2. 使用令牌代替密码进行认证

# 或者配置 SSH 密钥
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
# 然后将公钥添加到 Gitee 账户
```

### 问题 2：仓库不存在
```bash
# 确保已在 Gitee 网站上创建了仓库
# 检查仓库地址是否正确
git remote -v
```

### 问题 3：权限被拒绝
```bash
# 确保您有推送权限
# 如果是组织仓库，确保您是组织成员且有写入权限
```

## 📋 推送后检查清单

- [ ] 仓库已成功创建在 Gitee 上
- [ ] 所有文件已推送到远程仓库
- [ ] README.md 显示正确
- [ ] 版本标签已创建并推送
- [ ] 仓库描述和标签已设置
- [ ] GVP 申请已提交（如适用）

## 🌟 仓库优化建议

推送成功后，建议进行以下优化：

1. **添加仓库封面**
   - 上传项目截图或 Logo
   - 设计符合国产化主题的封面

2. **完善仓库信息**
   - 添加详细的项目描述
   - 设置关键词标签
   - 添加官方链接

3. **创建 Issues 模板**
   - 添加 Bug 报告模板
   - 添加功能请求模板
   - 添加问题咨询模板

4. **设置分支保护规则**
   - 保护主分支
   - 要求 PR 审核
   - 强制 CI 检查

---

## 🎯 推送成功示例

```bash
$ git push -u origin main
Enumerating objects: 30, done.
Counting objects: 100% (30/30), done.
Delta compression using up to 8 threads
Compressing objects: 100% (25/25), done.
Writing objects: 100% (29/29), 25.45 KiB | 5.09 MiB/s, done.
Total 29 (delta 2), reused 0 (delta 0)
remote: Powered by Gitee.com
To https://gitee.com/your-username/CNSH-National-Reference.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

成功推送后，您的 CNSH Core 项目将为国家数字主权建设贡献力量！

---

**【北辰-B 协议 · 国产通道校验 UID9622】**