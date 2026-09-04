# 🔧 Notion Master MCP Server v1.0 · 使用指南

> DNA: #龍芯⚡️2026-09-04-NOTION-MASTER-MCP-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622）· 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层）
> 三色: 🟢 端到端实测通过 / 🟢 零三方依赖 / 🔴 0

---

## 一、它解决什么问题？

官方 `@notionhq/notion-mcp-server` 只能**按 ID 查**——AI 不知道 workspace 里有
哪些页面、看不到页面树、读不到评论（对话记录）、无法批量整理。

**Notion Master MCP** 用 15 个高层工具补上完整闭环：

```
发现    notion_search / notion_page_tree / notion_local_search
读取    notion_read_page / notion_query_database / notion_read_comments / notion_page_info
执行    notion_create_page / notion_append_blocks / notion_update_page
        notion_archive_page / notion_create_row / notion_update_row / notion_index_sync
体检    notion_health
```

## 二、文件与注册

| 项 | 值 |
|:---|:---|
| Server 源码 | `integrations/mcp/notion_master_mcp_server.py` |
| 注册名 | `Notion Master MCP`（`~/.codebuddy/mcp.json`） |
| 运行解释器 | `/Users/zuimeidedeyihan/.longhun/bin/python3`（零三方） |
| Token 来源 | env → `lh_vault` → mcp.json（自动选第一个有效者，不落盘） |
| 本地索引 | `~/.longhun/notion_index.db`（SQLite + FTS5·2001 页） |
| API 直连 | 官方 REST · 指数退避(429/5xx) · 全翻页 · 3 req/s 限速 |

> **生效**：修改 mcp.json 后重启 CodeBuddy 或重载 MCP 配置，即可看到
> `notion_master_*` 工具组。

## 三、常用操作示例（对 AI 说人话即可）

### 1. 摸清结构
> 「帮我把主控台下的页面树列出来，两层」

→ `notion_page_tree(page_id=2507125a..., max_depth=2)` → 返回缩进树 + JSON

### 2. 全文搜索
> 「搜一下工作区里跟'权限'相关的页面和数据库」

→ `notion_search(query="权限")` 或 秒搜 `notion_local_search(query="权限")`

### 3. 读整页
> 「把雯雯执行报告那页内容读出来」

→ 先 search 找 ID → `notion_read_page(page_id=...)` → 结构化文本

### 4. 读对话记录（评论）
> 「看看主控台上有什么讨论/评论」

→ `notion_read_comments(page_id=...)` → 返回全部评论=对话记录

### 5. 整理归类
> 「把这三页归档」 / 「把 X 页移到 Y 页下面」

→ `notion_archive_page(page_id=...)`（软删除·可恢复）
  移动=建新页+归档旧页两步（Notion API 不支持直接改父级）

### 6. 新建内容
> 「在数字资产管理中心下建一页'2026-09 资产快照'，内容用 markdown 给我」

→ `notion_create_page(parent_id=..., title=..., content=markdown, icon=emoji)`

### 7. 建/改数据库行
> 「在操作日志库加一条记录」 / 「把某行的状态改成已完成」

→ `notion_create_row(database_id=..., properties={...})`
→ `notion_update_row(row_id=..., properties={...})`

### 8. 刷新本地索引（让秒搜跟上云端）
> 「同步一下 Notion 本地索引」

→ `notion_index_sync(incremental=true)`（500页/次·未变跳过）

## 四、关键设计

1. **零三方**：只依赖 mcp SDK + 标准库 urllib，直连官方 REST（M77 无中间层）。
2. **data_source 兼容**：新 API 模型(2025-09-03)下数据库对象返回
   `object="data_source"`，search filter 传 `database` 会 400——server 已自动映射，
   对外统一显示 `database`。
3. **不删除只冻结**：归档=默认整理动作（软删除），`restore=true` 随时恢复。
4. **本地 FTS5**：`notion_local_search` 零 API 消耗秒搜标题+内容；
   `sqlite-longhun` MCP 的 db 正是同一 `notion_index.db`，也可 SQL 直查。
5. **写链路安全**：超长文本自动分页(≤100块/请求)；错误带 HTTP code + message；
   读操作无副作用。

## 五、实测记录（2026-09-04）

| 项 | 结果 |
|:---|:---|
| MCP 握手 initialize / tools/list | ✅ 15 工具 |
| notion_health | ✅ token 有效 · 索引 2001 页 |
| notion_search(database) | ✅ 100+ 库（太极协同/生态文档/操作日志/…） |
| notion_page_tree(主控台) | ✅ 57 直接子级树文本+JSON |
| 建页 → 读回 → 追加 → 改名 | ✅ 6块→6块→+2块→改名成功 |
| 归档 / 恢复 | ✅ archived true ↔ false 双向 |
| notion_read_comments | ✅ 接口通（主控台无评论=0 条真实返回） |

## 六、签名

```
DNA:    #龍芯⚡️2026-09-04-NOTION-MASTER-MCP-v1.0-UID9622
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
GPG:    A2D0092CEE2E5BA87035600924C3704A8CC26D5F
```
