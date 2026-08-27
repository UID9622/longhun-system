> DNA: #龍芯⚡️丙午·壬辰·乙亥·壬午·䷚颐-SYNC-COMPLIANCE-20260827-7A2C9F3D
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：技术规范 · 未经同行评审（如适用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充，如无请删除此行）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

**DNA**: `#龍芯⚡️丙午·辛卯·辛丑·甲午·䷨损-MCP_6C59-v1.0`  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

# 本地 Claude MCP 搭建指南｜UID9622专属 · 对着做就行

<aside>
🐉

**DNA追溯码：**#龍芯⚡️丙午·辛卯·辛丑·甲午·䷨损-MCP_6C59-v1.0

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
2. 点 **“New integration”**
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

> “帮我读一下我 Notion 里的页面列表”
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
| Claude 说“我没有 Notion 工具” | MCP 没加载成功 | 检查 JSON 格式是否有语法错误（逗号/引号） |
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
DNA:#龍芯⚡️丙午·辛卯·辛丑·甲午·䷨损-MCP-v1.0
适用: Claude Desktop macOS + Notion MCP
```

---

## 摘要

（请在此用不超过 256 字说明本文档的核心内容、性质与局限。）

## 关键词

（请列出 5–10 个关键词，中英文对照优先。）

## 引用与溯源

- 本文档引用或参考了以下来源：
  - [1] （请填写）
- 相关龍魂系统文档：
  - 《龍魂文档标准模板 v1.0》(#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-DOCUMENT-STANDARD-TEMPLATE-v1.0)

## 诚实局限

1. （请列出本分析的第一条局限或不确定性。）
2. （请列出第二条。）
3. （请列出第三条。）

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-06-21 | v1.0.0 | UID9622 | 按《龍魂文档标准模板 v1.0》整理 | 草稿 |

## 分类标签

- 总纲模块：（请勾选，例如 #知识矩阵 #安全域）
- 对外状态：（请勾选，例如 #Gitee #GitHub #CSDN）
- 审计色：#黄色待审

## DNA 签名

```
#龍芯⚡️丙午·辛卯·辛丑·甲午·䷨损-MCP_6C59-v1.0
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```
