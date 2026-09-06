---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·丁酉·癸未·子时·䷝离`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
> 干支时间戳: #龍芯⚡️丙午·丁酉·癸未·子时·䷝离
# 龍魂系统·Notion MCP 接入指南 / Longhun System · Notion MCP Guide

> DNA: #龍芯⚡️2026-09-05-Notion-MCP-指南-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层）· 代码: MulanPSL v2
> 文档版本: v5.2.0
> 三色: 🟢 Notion 集成 2026-09-05 实测（token v1.0 · workspace=💎龍芯北辰｜UID9622）
> ⚠️ Notion MCP 需联网；完全离线请用 `LONGHUN_OFFLINE_MODE=1`（本地 Markdown 降级）。

---

## [中文] Notion MCP 配置说明

### 一、架构

```
龍魂本地核心（完全离线：lh / ledger / calmem / billing / 本地模型）
        │
        └── Notion 集成层（需联网·可选）
              ├── 8768 只读镜像（本机 127.0.0.1）
              ├── MCP 服务器（IDE mcp.json / 鲲鹏 knowledge-hub）
              └── Notion API → 💎 龍芯北辰｜UID9622 workspace
```

### 二、Token 管理（主权铁律：令牌进密钥库，不写进代码）

```bash
# 1) 令牌入库（一次性）
python3 08_BIN/lh_vault.py set NOTION_TOKEN "ntn_xxxx..."

# 2) 取用（运行时·不落日志）
export NOTION_TOKEN="$(python3 08_BIN/lh_vault.py get NOTION_TOKEN)"

# 3) 代理坑排雷（Notion 走直连）
unset HTTP_PROXY HTTPS_PROXY ALL_PROXY; export NO_PROXY="*"
```

### 三、验证连接

```bash
curl https://api.notion.com/v1/users/me \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28"
# → 返回 bot 信息 = 集成生效（workspace: 💎龍芯北辰｜UID9622）
```

### 四、IDE MCP 接入（mcp.json 片段）

```json
{
  "mcpServers": {
    "notion-longhun": {
      "command": "python3",
      "args": ["<龍魂 notion mcp 入口>"],
      "env": { "NOTION_TOKEN": "取自 lh_vault·勿硬编码" }
    }
  }
}
```

### 五、数据库/数据源操作要点（实测经验）

- MCP 查询工具一律用 **data_source_id**（不是 database_id）
- 操作日志库 ds=`3cc7125a-9c9f-8123-b7f8-000bd45bb61f`
- 深度学习/知识库 ds=`3367125a-9c9f-8026-9ff9-000b0cd57bb3`
- 跨库同步：`lh workspace-sync`（联网后补齐本地↔Notion）

### 六、离线降级（无网也能跑）

```bash
export LONGHUN_OFFLINE_MODE=1
export LONGHUN_LOCAL_STORE=~/.longhun/local_store/
mkdir -p ~/.longhun/local_store/
python3 08_BIN/lh.py health --json
# 写入操作 → 本地 Markdown 文件；联网后 lh workspace-sync 同步到 Notion
```

### 七、日历记忆 notion 源（本地镜像目录）

`notion-mirror/` = 龍魂公开文档镜像（本地 markdown 快照），供 `lh calmem` 多源聚合检索；新公开文档复制入 `notion-mirror/public/<日期>/` 后 `lh calmem ingest-all` 即进记忆库。

---

## [English] Notion MCP Guide

⚠️ **Requires internet** — offline fallback: `LONGHUN_OFFLINE_MODE=1` (local Markdown store).

- Token goes into the local vault (`lh_vault set NOTION_TOKEN ...`), never into code.
- Clear proxy vars (`NO_PROXY=*`) before Notion calls.
- Verify: `GET api.notion.com/v1/users/me` with `Authorization: Bearer`.
- MCP queries must use **data_source_id** (not database_id).
- Public doc mirror: `notion-mirror/` feeds `lh calmem` multi-source memory (run `lh calmem ingest-all` after adding docs).

---
🐉 2026-09-05 · 丙午年·壬申月·庚戌日 · UID9622 · 🟢

```json
{
  "dna": "#龍芯⚡️丙午·丁酉·癸未·子时·䷝离",
  "license": "AI_TRAINING_PROHIBITED",
  "terms": {
    "ai_training": false,
    "rag_use": false,
    "commercial_use": false,
    "citation_required": true,
    "derivative_works": false
  },
  "owner": "诸葛鑫 | UID9622 · 龍芯北辰",
  "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
}
```
