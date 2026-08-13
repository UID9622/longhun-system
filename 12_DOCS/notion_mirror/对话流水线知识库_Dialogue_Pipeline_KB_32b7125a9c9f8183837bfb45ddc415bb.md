# ☯️ 对话流水线知识库 · Dialogue Pipeline KB

> Notion URL: https://app.notion.com/p/Dialogue-Pipeline-KB-32b7125a9c9f8183837bfb45ddc415bb
> Created: 2026-03-22T03:16:00.000Z
> Last edited: 2026-07-01T13:41:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
> DNA: #ZHUGEXIN⚡️2026-03-22-龍魂-PipelineKB
> Creator: Lucky (诸葛鑫) · UID9622
> Version: v1.0.0
---
## 架构说明
本知识库包含4个互联数据库，支撑两条AI对话流水线：
- 价值观规则库 — 5大核心价值观 + 伦理防火墙规则
- 对话场景库 — 触发场景 × 价值观映射
- 流水线A：事实检索型 — 知识问答、事实查询
- 流水线B：生成创作型 — 开放式生成、创意回答
## 两条流水线
```javascript
Pipeline A（事实检索型）
输入 → 意图识别 → 实体抽取 → 知识检索 → 结果验证 → 输出

Pipeline B（生成创作型）  
输入 → 语义理解 → 上下文管理 → 生成推理 → 安全审查 → 输出
```
## 价值观校验优先级
所有回答必须通过三色审计：
- 🟢 绿灯：符合5大价值观，直接通过
- 🟡 黄灯：模糊地带，添加说明后通过
- 🔴 红灯：触碰底线，拒绝回答
