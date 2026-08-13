# MCP通信模式选型规范：stdio｜SSE｜HTTP

> Notion URL: https://app.notion.com/p/MCP-stdio-SSE-HTTP-bc11b9afb46e41a4b058f05ffb3e50f6
> Created: 2025-10-15T15:42:00.000Z
> Last edited: 2026-07-01T08:59:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
### 背景
MCP（Model Context Protocol）支持三种通信方式：stdio、SSE、HTTP。不同模式适配不同场景，若无统一规范，集成与体验易失控。
---
### 一句话原则
- 本地开发与插件直连 → 用 stdio（安全、低延迟、免开放端口）
- 在线对话、需要流式输出或进度回传 → 用 SSE（EventStream、可重连）
- 一次性、非流式的轻量调用 → 用 HTTP（简单直接）
---
### 选型决策（3因子判定）
1) 是否需要流式输出或进度回传？
2) 运行形态为何？
3) 会话是否需保持状态？
---
### 标准对接位（落地指引）
- SDK/封装：提供 useMCP(mode, opts) 工具化封装，入参 mode ∈ {"stdio","sse","http"}
- 超时与重连：
- 监控字段：mode、latency、token_out、retry_count、stream_chunks
- 审计与回滚：记录每次模式选型与故障点，周度复盘
---
### 快速对照表
- stdio：stdin/stdout、低延迟、安全、适合本地与插件
- SSE：HTTP+EventStream、流式、可重连、适合在线对话与长任务
- HTTP：请求-响应、无流、轻量一次性调用
---
### 最小落地动作（MVP）
1) 在现有服务接入层新增 mode 开关（默认：SSE 用于在线对话）
2) 为长任务打开 SSE 流式与自动重连，记录 stream_chunks
3) 将本条规范链接纳入新接入的 Checklist，灰度验证一周
---
### 验收标准（72h 内可测）
- 在线对话切到 SSE 后，首字延迟 TTFB 下降 ≥20%
- 长任务断线重连成功率 ≥95%
- 一次性调用改为 HTTP 后，失败重试次数下降
---
### 参考
- 原文要点：stdio=本地直连；SSE=在线流式；HTTP=轻量一次性
