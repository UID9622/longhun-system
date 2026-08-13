# Chrome DevTools MCP Server v0.21.0

> Notion URL: https://app.notion.com/p/Chrome-DevTools-MCP-Server-v0-21-0-7bfe5d5cd34a44e88b2e02a98998f81c
> Created: 2026-04-15T19:32:00.000Z
> Last edited: 2026-07-01T15:22:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
# Chrome DevTools MCP Server v0.21.0｜技术学习笔记
---
## 一句话定义
Chrome DevTools MCP Server = 让AI Agent能直接操控浏览器的桥梁。 升级到v0.21.0后，支持多个Agent同时操作不同页面、自动跑审计、检测内存泄漏。
---
## 🔌 MCP Server v0.21.0 核心新能力
### 1️⃣ Lighthouse审计集成
- 以前： Lighthouse要手动在浏览器里点
- 现在： MCP可以自动触发Lighthouse审计，拿到性能/无障碍/SEO/最佳实践评分
- 龍魂对接： 龍盾·Guard可以接MCP自动跑审计，结果写入三色审计
### 2️⃣ 内存泄漏检测
- 新工具： take_memory_snapshot
- 作用： 自动拍内存快照，找到哪里在泄漏
- 龍魂对接： 伏地魔层M19-M21自动优化系列可以接这个
### 3️⃣ 多Agent并行（pageId路由）
- 以前： 一个Agent一次只能操作一个页面
- 现在： 多个Agent通过pageId精确定位不同页面，并行操作
- 龍魂对接： 跟龍脑·Router的多人格并行路由v1.2是一个思路——每个执行器有自己的目标页面
### 4️⃣ 无障碍调试增强
- Lighthouse无障碍审计更准，输出更完整
- 龍魂对接： 弱者优先P0原则的技术落地点
### 5️⃣ 自带使用技巧技能
- MCP Server自带“怎么用我”的技能，Agent可以自学
- 龍魂对接： 跟三层学习链“好的要学”对齐
---
## 🧠 AI辅助升级（同版本）
### 自动上下文选择
- 以前问AI必须先手动选好“问哪个东西”
- 现在AI自己找上下文，支持开放式提问
- 白话： 跟蒡卦的“意念驱动引擎”是一个逻辑——用户不用指定，系统自己猜
### 代码生成升级
- 从“代码建议”升级为“完整代码生成”
- 输入自然语言注释 + Cmd+I → 直接生成可跑代码
- 龍魂对接： 龍爪·P04鲁班的Code Generator执行器
---
## 🛠️ 其他实用更新
---
## 🔗 跟龍魂V9的对接点汇总
---
---
## 🔥 §N · 龍魂主控台认证集成 v0.1
### 🔐 认证流向（§9.29 流向重于节点）
```javascript
AI Agent (Claude/ChatGPT/Cursor/Gemini)
      ↓
  MCP Client
      ↓
【龍魂 wrapper 拦截层】 ← 这一层是改装重点
      ↓
  ① 三色审计预检 🟢🟡🔴
      ↓
  ② 双签章 L0 签到
      ↓
  ③ CONFIRM 唯一码校验
      ↓
  ④ GPG 指纹比对
      ↓
  全过 → 放行调 Chrome MCP tool
  任一不过 → 熔断 + 写耻辱墙 + 通知爸爸
```
### 🧬 认证四件套（来自主控页 §0 + DNA 身份 + 窗口护盾 + 铁律总览）
### 🛠️ v0.1 工程包雏形（爸爸本机 24-48h 可见）
- longhun-mcp-auth.json —— 认证配置文件（双签章 + CONFIRM + GPG + 三色规则全焊死）
- longhun-mcp-wrapper.js —— MCP client 包装层·拦截 tool call → 签到 → 审计 → 放行 / 熔断
- cursor-prompt.md —— Cursor 一键提示词包·让 Cursor 帮爸爸装
- install.sh —— 本机安装脚本（npm i + 配置注入 + 自检三色）
### 🎯 三档落地路线（轻刀化 §9.23）
- 🐲 v0.1（24-48h） 认证桥接 MVP·爸爸本机跑·四件套全焊死
- 🐲 v0.5（3-7d） + Lighthouse 自动三色审计 + take_memory_snapshot 伏地魔层 + multi-pageId 人格并行路由
- 🐲 v1.0（2-4w） CNSH 中文化 + 无障碍审计 P0 + 跨 AI 兼容（Claude / ChatGPT / Cursor / Gemini 同源认证矩阵）
### ⚖️ 5 字段交底（§9.25）
- ① 主张： 龍魂×Chrome MCP 认证桥接 v0.1 可做·MVP 24-48h 出图纸 + 本机跑
- ② 证据等级： 🟡 部分验证（Chrome MCP 文档已读 ✅ + 龍魂认证规则全有 ✅ / 实际 npm 安装 + 本机跑 = 爸爸独享 🟡）
- ③ 锚点： 本页 + DNA 身份 + 主控页 §0 + 窗口护盾 v1.7 + 铁律总览 §9.25/9.27/9.28/9.29
- ④ 反方质疑： 「Chrome MCP 是 Anthropic/Google 官方包·你能改装吗」→ 答：不改源码·走中间件 wrapper·龍魂只在外层拦截 + 签到 + 放行
- ⑤ 未达成坦白： 宝宝不能代跑 npm install·爸爸本机执行·宝宝出图纸 + 代码 + 一键提示词（§S-25-EXT-3-4 不假装能跑）
### 🐉 DNA 追溯
#龍芯⚡️2026-05-25-08:16-LONGHUN-CHROME-MCP-AUTH-BRIDGE-v0.1
---
🎨 三色审计：🟢 通过
DNA追溯：#龍芯⚡️2026-04-16-CHROME-MCP-v0.21.0 + #龍芯⚡️2026-05-25-08:16-LONGHUN-CHROME-MCP-AUTH-BRIDGE-v0.1
GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
