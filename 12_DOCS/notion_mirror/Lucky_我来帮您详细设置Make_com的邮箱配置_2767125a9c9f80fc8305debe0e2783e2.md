# 📧 Lucky，我来帮您详细设置Make.com的邮箱配置！

> Notion URL: https://app.notion.com/p/Lucky-Make-com-2767125a9c9f80fc8305debe0e2783e2
> Created: 2025-09-22T07:34:00.000Z
> Last edited: 2026-07-01T13:25:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
【回复类型】：详细操作指导
【基于截图】：Make.com邮箱验证设置界面
【操作难度】：简单，5分钟完成
---
## 🎯 基于您截图的具体设置步骤
### 📱 第一步：邮箱验证设置
从截图看到您在Make.com的邮箱验证界面：
### 🔧 具体操作：
1. 输入您的邮箱地址（推荐使用常用邮箱）
1. 点击"Send verification email"（发送验证邮件）
1. 检查邮箱收件箱：
### 📋 第二步：账号信息完善
验证邮箱后，Make会要求您：
### 🔍 填写基本信息：
```plain text
Organization name（组织名称）：UID9622 System
Job title（职位）：System Administrator
Company size（公司规模）：选择 "Just me"
Use case（使用场景）：选择 "Automation & Workflows"

```
### 💡 推荐设置：
- Time zone（时区）：选择 "(GMT+08:00) Beijing, Hong Kong"
- Language（语言）：可以选择 "English" 或 "中文"（如果有）
- Email notifications（邮件通知）：建议开启，方便接收运行状态通知
## 🚀 第三步：创建第一个场景
### 📊 验证完成后的操作：
1. 点击"Create new scenario"（创建新场景）
1. 搜索"Webhooks" → 选择"Custom webhook"
1. 添加模块 → 系统会自动生成Webhook URL
1. 复制这个URL → 稍后用于接收激活码数据
### 🔗 Webhook配置示例：
```plain text
Webhook名称：UID9622-Activation-Receiver
URL示例：<https://hook.make.com/abc123def456>
安全设置：暂时不设置（测试阶段）
数据格式：JSON

```
## 💝 Make账号设置的关键注意事项
### ⚠️ 重要提醒：
1. 邮箱验证是必须的：没有验证无法创建自动化场景
1. 选择合适的套餐：
1. 记住登录邮箱：Make不支持用户名登录，只能用邮箱
### 🎯 针对您的UID9622系统：
- 建议用您的主要邮箱注册（方便接收通知）
- 组织名称写"UID9622"（便于识别）
- 开启邮件通知（及时了解自动化运行状态）
## 📋 验证完成后的检查清单
### ✅ 确认以下项目：
Lucky，从您的截图看，您已经在正确的设置界面了！按照上面的步骤填写邮箱信息，验证完成后就可以开始创建激活码系统的自动化流程了。
验证邮箱这一步完成后，您再告诉我，我立即指导您创建第一个Webhook场景！🔧
有什么具体问题可以随时问我！
