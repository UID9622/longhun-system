# Agent架构与Context Engineering要点（Prompt→Context）

> Notion URL: https://app.notion.com/p/Agent-Context-Engineering-Prompt-Context-db5fac571541466192702c2bf5ffbcc3
> Created: 2025-10-15T15:54:00.000Z
> Last edited: 2026-07-01T09:02:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
### 要点
- 范式：Prompt Engineering ⊂ Context Engineering（检索、记忆、工具、路由、压缩、编排）
- RAG升级：重排序、压缩（摘要）、Self/Agentic RAG、路由与记忆
- 关键限制：Lost-in-the-Middle → 重要信息放窗口两端+压缩
- 编排：LangGraph等图式编排，ReAct循环（思考→行动→观察→再思考）
### MVP落地
1) 为学习流水线增加“召回→重排→压缩→格式化”四段
2) 在模板中固定证据写回与失败重试位
### 验收（72h）
- 召回Top-N→Top-K重排后命中率↑
- 回答引用率↑ 幻觉率↓
