# ② Inbox Automation 触发链 · 规格书 v1.0

> Notion URL: https://app.notion.com/p/Inbox-Automation-v1-0-34d7125a9c9f81fc818edff6d5ac61c5
> Created: 2026-04-25T16:23:00.000Z
> Last edited: 2026-07-01T14:38:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
DNA: #龍芯⚡️2026-04-26-INBOX-AUTOMATION-SPEC-v1.0
---
> ⚠️ 操作说明
> 
> 这份文档是你在 Notion 里配置 Automation 的操作手册。
> 按第五节“Notion Automation 配置步骤”一步一步操作。
---
## 总体流程
```javascript
[谷歌浏览器插件 / cnsh-chrome-plugin]
    ↓ Cmd+Shift+L 一键抓取
    ↓ 写入 Notion Inbox 数据库（新Page创建）
    ↓
[Notion Automation · 触发器]
    ↓ 条件满足 → 调用通心译 Agent (@龍慧·通心译)
    ↓
[Agent 处理]
    ↓ 路由判断 → 翻译/提炼/分类/保护
    ↓ 写回目标数据库 + 打DNA标签
    ↓
[DNA链记录]（append-only · 永不删改）
```
---
## 第一节 · 触发器配置
触发数据库： Inbox（主工作区·UID9622）
触发事件： Page Created（新页面创建时）
触发条件（AND 逻辑，全满足才触发）：
---
## 第二节 · 执行动作链
Step 1 · 锁定页面（防并发）
```javascript
Action: Edit property
  Agent锁（Checkbox）= ✅ true
```
Step 2 · 更新状态
```javascript
Action: Edit property
  状态（Select）= 🔄 处理中
```
Step 3 · 调用通心译 Agent
```javascript
Action: Add comment
  @龍慧·通心译
  [INBOX_AUTO_TRIGGER]
  页面ID: {{page.id}}
  创建时间: {{page.created_time}}
  内容摘要: {{prop.内容前100字}}
  来源标签: {{prop.来源}}

  请按通心译路由规则处理，写回对应库。
```
Step 4 · 打时间戳
```javascript
Action: Edit property
  触发时间（Date）= Now()
```
---
## 第三节 · Agent 内部执行逻辑
收到 [INBOX_AUTO_TRIGGER] 指令后，Agent 按以下顺序执行：
1. 读取完整页面内容
1. 启动输入路由（第四模块）：黑话/保护/灵感/外文
1. 判断输出库：灵感库/知识库/DNA库/任务库
1. 生成DNA码：#龍芯⚡️{date}-通心译-{类型标签}-P14
1. 在 Inbox 页面追加处理结果摘要
1. 将完整输出写入目标数据库
1. 更新 Inbox 页面状态 → 已处理
1. 释放 Agent锁（置 false）
---
## 第四节 · 错误回退方案
错误 A · Agent 未响应（超时3分钟）
- 状态 → ⚠️ 超时待处理
- Agent锁 → false（释放锁）
- 追加 Comment：⚠️ 通心译超时，请手动 @龍慧·通心译 重新触发
错误 B · 保护内容拦截
- Agent 输出标准拒绝格式（第三模块）
- 状态 → 🔴 需人工审核
- 不写入任何目标库
错误 C · 写入目标库失败
- 状态 → ⚠️ 写入失败
- 在 Inbox 页面内直接保留处理结果全文（不丢失）
- 写 DNA 链日志：op_type = ALERT
错误 D · 空内容页面
- 状态 → ⏭️ 跳过（空页面）
- Agent锁 → false
- 不调用 Agent，不消耗配额
---
## 第五节 · Notion Automation 配置步骤
### 主触发链
1. 进入 Inbox 数据库 → … 菜单 → Automate
1. 点击 + New automation
1. 配置触发器：Trigger: Page Created in [Inbox]
1. 添加 Filter（AND逻辑）：状态/Agent锁/内容 三条条件
1. 添加 Action 链（按顺序）：锁 → 状态 → 论价 → 时间戳
1. 命名：通心译自动触发链 v1.0
1. 启用
### 超时监控链
1. 新建第二条 Automation
1. 触发器：状态 is 🔄 处理中 + 触发时间 before now-3min
1. 动作：状态 = ⚠️超时 / Agent锁 = false / 追加提醒Comment
1. 命名：超时监控·通心译 v1.0
---
## 第六节 · Inbox 数据库必要字段清单
---
DNA: #龍芯⚡️2026-04-26-INBOX-AUTOMATION-SPEC-v1.0
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬 LK9X-772Z
