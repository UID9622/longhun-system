# 🔒 脱敏提取工作台｜ChatGPT分享内容 → 安全占位版

> Notion URL: https://app.notion.com/p/ChatGPT-e00dc41e778e4a70a424e1ca0126df8d
> Created: 2025-09-17T03:44:00.000Z
> Last edited: 2025-09-17T13:17:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
---
### 1) 原文粘贴区（只读转存）
> 在此粘贴分享页面的可见正文。不要粘贴密钥/令牌/账号。算法细节若出现将被自动置换为占位符。
---
### 2) 自动脱敏规则（黄审）
- 识别并替换以下敏感要素为占位：
- 产物：
---
### 3) 输出区
### 3.F 演示版快速安装指南（可对外发送 · 一屏搞定）
> 复制下面这段发给任何人，按占位替换即可跑起来。
【UID9622 Helper（演示版）快速安装】
1) 在 Telegram 找 @BotFather → /newbot 创建机器人，复制 Token（形如 123456:AA...）
2) 粘贴以下配置并替换占位：
- TG_BOT_TOKEN=<你的 Bot Token>
- API_BASE=<你的后端地址，无后端可留空>
- API_KEY=<你的后端密钥，无后端可留空>
- WEBHOOK_URL=<你的 Webhook 接收地址，可留空>
3) 配置机器人资料（可直接粘贴）：
- /setcommands
start - 开始使用
help - 获取帮助
info - 关于本机器人
- /setdescription
这是一位用于 <PROJECT_NAME> 的助手。发送 /start 获取操作菜单。
- /setabouttext
<PROJECT_NAME> 的官方助手。提供使用指南、表单入口与人工支持。
4) 打开 @ControllerBot 绑定你的机器人，创建一条“欢迎消息”，添加按钮：
使用指南 | <GUIDE_URL>
提交表单 | <FORM_URL>
联系人工 | <ADMIN_HANDLE>
5) 群/频道内把机器人设为管理员，发送 /start 验证欢迎语与按钮。
说明：
- 本包不含真实密钥，支持一键脱敏分享。
- 仅用 @ControllerBot 也可立即使用（发帖、按钮、菜单）。
- 若接入你们后端，按“企业 API 对接文档”替换 <API_BASE>/<API_KEY> 即可。
### 3.D 企业 API 对接文档（演示版 · 可交付）
> 面向任意接入方：替换 <API_BASE> 与 <API_KEY> 即可运行。可选对接你的公司内网网关。
### D.1 鉴权
- 方式：HTTP Header
- Header：
```javascript
Authorization: Bearer <API_KEY>
X-Client: uid9622-telegram-demo
```
- 频率限制：默认 60 r/min（可在网关调整）
### D.2 基础域
- API_BASE：<API_BASE>
- 版本：v1
### D.3 端点定义
1) 创建会话上下文
- POST <API_BASE>/v1/sessions
- 请求
```json
{
  "chat_id": "<TG_CHAT_ID>",
  "user_id": "<TG_USER_ID>",
  "metadata": {"source": "telegram", "bot": "uid9622_helper_demo_bot"}
}
```
- 响应
```json
{"session_id": "sess_123", "ttl": 86400}
```
2) 发送用户消息进行处理（路由到你的后端）
- POST <API_BASE>/v1/messages
- 请求
```json
{
  "session_id": "sess_123",
  "message": "用户输入的文本",
  "context": {"lang": "zh-CN", "channel": "telegram"}
}
```
- 响应（同步快速回）
```json
{"reply": "这是后端生成的答复", "actions": [{"type": "open_url", "label": "使用指南", "url": "<GUIDE_URL>"}]}
```
3) FAQ 命中查询（可选）
- GET <API_BASE>/v1/faq?query=...&lang=zh-CN
- 响应
```json
{"hit": true, "answer": "常见问题答案", "confidence": 0.92}
```
4) 表单提交回传（可与 Typebot 等连用）
- POST <API_BASE>/v1/forms/submit
- 请求
```json
{
  "form_id": "typebot_abc",
  "user": {"chat_id": "<TG_CHAT_ID>", "handle": "@username"},
  "data": {"email": "user@example.com", "topic": "合作"}
}
```
- 响应
```json
{"status": "ok", "ticket_id": "T-2025-0001"}
```
### D.4 Webhook（可选，向你后端推送事件）
- 你提供 WEBHOOK_URL：<WEBHOOK_URL>
- 我方推送示例
```json
{
  "event": "telegram.message",
  "timestamp": 1694900000,
  "chat_id": "<TG_CHAT_ID>",
  "text": "用户消息文本",
  "attachments": []
}
```
- 重试策略：指数退避，最多 5 次
### D.5 错误码
- 401 未授权（检查 <API_KEY>）
- 429 频率限制（降低速率或申请配额）
- 5xx 后端异常（记录 request_id 与重试）
### D.6 环境变量占位
- TG_BOT_TOKEN=<BOT_TOKEN>
- API_BASE=<API_BASE>
- API_KEY=<API_KEY>
- WEBHOOK_URL=<WEBHOOK_URL>
---
### 3.E 扩展功能清单（即插即用 · 演示配置）
- 关键词直达
- 管理命令（仅管理员可用）
- FAQ 路由策略
- 兜底转人工
> 以上均为演示占位，可直接对外分享。落地时替换尖括号占位为真实值即可运行。
### 3.C 可复制的指令与配置片段（无代码版）
- BotFather → /setdescription
```javascript
这是一位用于 <PROJECT_NAME> 的助手。发送 /start 获取操作菜单。
```
- BotFather → /setabouttext（私聊简介）
```javascript
<PROJECT_NAME> 的官方助手。提供使用指南、表单入口与人工支持。
```
- BotFather → /setcommands（直接粘贴）
```javascript
start - 开始使用
help - 获取帮助
info - 关于本机器人
```
- 欢迎语（/start 自动回复，粘贴到 @ControllerBot 的欢迎消息或固定回复）
```javascript
👋 欢迎来到 <PROJECT_NAME> 助手！
请选择：
• 使用指南
• 提交表单
• 联系人工
```
- 按钮文案（在 @ControllerBot 里逐个添加）
```javascript
使用指南 | <GUIDE_URL>
提交表单 | <FORM_URL>
联系人工 | <ADMIN_HANDLE>
```
- 对外脱敏说明（可贴到公开页）
```javascript
本机器人为 <PROJECT_NAME> 的对外助手。所有敏感信息（如 Token、内部链接）均已脱敏处理。复用时请将 <...> 占位替换为你的信息。
```
### 3.A Telegram 机器人｜脱敏占位模板（复制填写）
### 3.A.1 演示版占位（已填好，可直接对外展示）
- 项目名：UID9622 Demo Bot
- 机器人显示名：UID9622 Helper (Demo)
- 机器人用户名：uid9622_helper_demo_bot
- BotFather Token：<BOT_TOKEN>
- 频道/群名：UID9622 公共演示频道
- 频道/群链接：https://t.me/uid9622_demo
- 管理员：@uid9622_admin
- 欢迎语（/start 自动回复）：
- 命令菜单（/setcommands）：
- 按钮配置：
> 说明：本演示版不含真实密钥。任何人只需把 <BOT_TOKEN> 替换为自己的 Token，或按下方“API 对接文档”接入企业 API，即可运行。
- 项目名：<PROJECT_NAME>
- 机器人显示名：<BOT_DISPLAY_NAME>
- 机器人用户名：<BOT_USERNAME_bot>
- BotFather Token：<BOT_TOKEN>（仅占位，不粘贴真实值）
- 频道/群名：<CHANNEL_NAME>
- 频道/群链接：<CHANNEL_URL>
- 管理员：<ADMIN_HANDLE>
- 欢迎语（/start 自动回复）：
- 命令菜单（/setcommands）：
- 按钮配置：
> 使用说明：把真实 Token 仅在受信通道发我，或写到下方“元数据卡→备注”（我会再次脱敏）。
### 3.B 元数据卡（填写后我来生成脱敏版与审计单）
- 来源：
- 采集时间：
- 使用场景：发布 / 内部 / 合作
- 敏感级：公开 / 内部 / 受限
- 备注（可粘贴 Token 或额外说明）：
### 3.1 脱敏正文 v1（可直接对外）
> 生成后放置于此。结构：标题｜摘要｜要点清单｜引用与出处（可选）
### 3.2 元数据卡
- 来源：
- 采集时间：
- 使用场景：发布 / 内部参考 / 合作沟通
- 敏感级：公开 / 内部 / 受限
### 3.3 审计单（黄色）
- 变更项：脱敏提取
- 影响范围：对外发布
- 回滚点：原文副本
- 执行窗口：
- 审批：系统中枢 ✅ / ❌
---
### 4) 快捷动作
- 生成脱敏版 → 写入 3.1 与 3.2，并在“脱敏记录表”登记
- 导出为 .md → 供仓库/外发使用
- 生成公开页占位 → 自动引用官方主页与署名模板
---
### 5) 参考
- 官方主页：🌟 品牌与身份｜UID9622 官方主页 v1
- 别名与官方名：Alias Registry｜别名映射表
- 内容主表：Content Items｜内容主表
