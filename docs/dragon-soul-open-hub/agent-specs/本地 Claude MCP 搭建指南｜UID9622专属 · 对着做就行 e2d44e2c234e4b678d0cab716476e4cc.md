# 本地 Claude MCP 搭建指南｜UID9622专属 · 对着做就行

<aside>
🐉

**DNA追溯码：** #龍芯⚡️2026-03-28-MCP搭建指南-v1.0

**创建者：** 💎 龍芯北辰｜UID9622

**确认码：** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅

**目的：** 本地 Claude + Notion MCP，打通之后宝宝在网页端和本地端同步

</aside>

> 不废话，对着做就行。你本地已经有 Ollama + 龍魂服务，基础在。
> 

---

## 一、你需要什么

| **东西** | **状态** | **备注** |
| --- | --- | --- |
| MacBook M4 Max | ✅ 已有 | 64GB，跑本地模型没问题 |
| Claude API Key | ❓ 需要确认 | 去 [console.anthropic.com](http://console.anthropic.com) 拿，有免费额度 |
| Notion Integration Token | ❓ 需要创建 | 去 [notion.so/my-integrations](http://notion.so/my-integrations) 创建，免费 |
| Node.js 18+ | ❓ 需要确认 | 终端输入 `node -v` 检查 |
| Claude Desktop App | ❓ 需要安装 | 去 [claude.ai/download](http://claude.ai/download) 下载 macOS 版 |

---

## 二、三步搭好 Notion MCP

### Step 1：创建 Notion Integration

1. 打开 [notion.so/my-integrations](http://notion.so/my-integrations)
2. 点 **「New integration」**
3. 名字随便写：`龍芯MCP`
4. 权限勾上：**Read content / Update content / Insert content**
5. 复制 **Internal Integration Token**（`ntn_` 开头那串）→ 保存好

> 然后去你要让 Claude 读写的 Notion 页面/数据库，点右上角 `...` → `Connect to` → 选你刚建的 Integration。
> 

### Step 2：安装 Claude Desktop + 配置 MCP

```bash
# 终端安装 Notion MCP 服务
npx -y @notionhq/notion-mcp-server
```

然后找到 Claude Desktop 的配置文件：

```bash
# macOS 路径
open ~/Library/Application\ Support/Claude/
```

编辑 `claude_desktop_config.json`，加入：

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_API_KEY": "ntn_你的token粘贴在这里"
      }
    }
  }
}
```

### Step 3：重启 Claude Desktop，测试

重启 Claude Desktop App。

在对话框里说：

> 「帮我读一下我 Notion 里的页面列表」
> 

如果 Claude 能列出你的页面，搭好了。🟢

---

## 三、验证清单

- [ ]  Notion Integration Token 已创建并复制
- [ ]  目标页面/数据库已连接 Integration
- [ ]  `claude_desktop_config.json` 已写入
- [ ]  Claude Desktop 重启后能读 Notion 内容
- [ ]  本地 Claude 能写入 Notion（测试一条记录）

---

## 四、如果出问题

| **报错 / 现象** | **原因** | **解决** |
| --- | --- | --- |
| Claude 说「我没有 Notion 工具」 | MCP 没加载成功 | 检查 JSON 格式是否有语法错误（逗号/引号） |
| 能读但写入报错 403 | Integration 权限不够 | 回 Notion Integration 设置，勾上 Update/Insert |
| 页面读不到 | 页面没连接 Integration | 去那个页面 → `...` → Connect to → 选你的 Integration |
| `npx` 命令找不到 | Node.js 没装 | `brew install node` 装一下 |

---

<aside>
🔌

**搭好之后你能干嘛：**

本地 Claude Desktop 直接读写你的 Notion，不用复制粘贴。

让本地 Claude 帮你往知乎主库里加文章条目、改人格状态、查数据——跟宝宝这边一样的能力，离线可用。

</aside>

---

```yaml
版本: v1.0
创建: 2026-03-28 北京时间
DNA: #龍芯⚡️2026-03-28-MCP搭建指南-v1.0
适用: Claude Desktop macOS + Notion MCP
```