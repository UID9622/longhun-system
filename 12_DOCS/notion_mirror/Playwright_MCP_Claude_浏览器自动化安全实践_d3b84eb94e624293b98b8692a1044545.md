# Playwright MCP × Claude 浏览器自动化安全实践

> Notion URL: https://app.notion.com/p/Playwright-MCP-Claude-d3b84eb94e624293b98b8692a1044545
> Created: 2025-10-15T15:54:00.000Z
> Last edited: 2026-07-01T09:01:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
### 要点
- 能力：navigate、click、fill、extract、持久会话
- 风险：提示注入、账户与隐私、越权操作
### 安全基线
- 最小命令白名单+域名白名单
- 敏感词与凭据掩码
- 操作录像与DOM快照写回Evidence
### MVP
- 针对学术抓取场景制作两条预置工作流（检索→筛选→提取→入库）
### 验收（72h）
- 任务首成功率≥90% 复跑成功≥95%
### 后续迭代
- 集成Chrome DevTools Protocol实现更细粒度的网络拦截与性能监控
- 探索Headless模式下的验证码自动识别方案（OCR + 规则引擎）
- 建立跨站操作的Context隔离机制，防止Cookie与Storage泄漏
