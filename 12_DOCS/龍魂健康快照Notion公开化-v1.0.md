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
# 🏥 龍魂健康快照 Notion 公开化 · 落地文档 v1.0

> DNA: #龍芯⚡️2026-09-06-HEALTH-NOTION-PUBLIC-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层）· 代码: MulanPSL v2
> 日期: 2026-09-06 · 状态: 🟢 本地→Notion 全链已通 · 🟡 公开 Publish 待手动一步

---

## 一、总体架构（已落地 ✅）

```
lh health snapshot（本地快照 · 每日 07:00/21:00 launchd）
        ↓
lh health sync（同步引擎 · 快照后自动执行）
        ↓
Notion Database ×3（公开数据库）
        ↓
公开页面/iframe（对外展示 · 待 Publish 一步）
```

- 快照照常生成（`~/.longhun/health_snapshots/YYYY-MM-DD/07|21.json`）
- 同步引擎自动把新快照/拓扑事件/周报推送到 Notion（幂等·失败不阻塞快照）
- 配置: `~/.longhun/health_sync_config.json`

## 二、三个数据库（已建 ✅ · 父页 🐉 龍魂·系统核心）

| 库 | 名称 | database_id | 记录 |
|:---|:---|:---|:---|
| 主库 | 🏥 龍魂健康快照 | `3d27125a-9c9f-814a-9d11-d96c60f07517` | 每快照一行(14列: 快照时间/类型/健康状态/异常项数/节点/边/根哈希/一致/DNA/GPG…) |
| 关联库 | 🧩 拓扑变更事件 | `3d27125a-9c9f-81d9-89fd-ed1a227162ac` | 快照携带的变更事件逐条成行(7列·relation关联快照) |
| 关联库 | 📋 一周健康报告 | `3d27125a-9c9f-8142-aade-d72b258a13cf` | 每周日 report 一行(9列·状态分布/结论·relation) |

> 注: 曾用新版 Notion header(2025-09-03)建库导致属性丢失 → 已冻结废弃库重建；
> 该 workspace 为 data_source 模型，引擎固用 `Notion-Version: 2022-06-28`(实测建库带属性/建行/查询全兼容)。

## 三、同步引擎（已落地 ✅）

`08_BIN/lh_health_sync.py` · 注册 `lh health sync*`

| 命令 | 动作 |
|:---|:---|
| `lh health sync` | 推送未同步快照/拓扑事件/周报到 Notion（幂等·按 DNA 追溯码去重） |
| `lh health sync-init` | 初始化三库（幂等·已存在跳过） |
| `lh health status` | 库链接/本地与 Notion 已同步计数 |
| `lh health list` | 本地快照清单 + 同步状态 |

Token 链: env `NOTION_TOKEN` → `lh_vault get NOTION_TOKEN` → `~/.codebuddy/mcp.json`。
直连官方 REST · 禁代理 · 指数退避(429/5xx 重试 4 次)。

### launchd 集成（已改 ✅）
- `08_BIN/lh_health_snapshot_daily.sh` v1.1: 快照(重试3) → 自动 `sync --quiet`（失败不阻塞）
- `08_BIN/lh_health_snapshot_weekly.sh` v1.1: 周报 → 自动 `sync --quiet`
- 任务 `com.longhun.health-snapshot`(07:00/21:00) + `com.longhun.health-weekly`(周日23:00) 已 load

## 四、公开分享（🟡 手动一步 · API 无 publish 能力）

> Notion API 无法自动公开页面，需人工在浏览器点一次。步骤:

1. 打开数据库页面（任意一个，如主库）：
   `https://www.notion.so/3d27125a9c9f814a9d11d96c60f07517`
2. 右上角 **Share** → 若弹窗提示 workspace 权限，选 **Publish to web** →
   **Allow anyone with the link to view** → 复制公开链接（形如 `https://xxx.notion.site/龍魂健康快照-xxxx`）
3. 对另外两个库重复；想嵌文档站则把三个公开链接发给 AI 填 iframe

## 五、文档站嵌入模板（Publish 后可用）

在 `docs-site/docs/` 新增页 + mkdocs.yml nav，iframe 填公开链接:

```html
<iframe src="https://<workspace>.notion.site/<slug>" width="100%"
        height="800" frameborder="0" allowfullscreen></iframe>
```

## 六、API 端点（增强项 · 待 P14 部署轮）

鲲鹏 `uid9622.cn/api/health/snapshots|latest` 需服务器侧引擎+systemd，属部署轮，
非本次本地落地区域。数据源已齐（Notion 库/本地 JSON/周报 md）。

## 七、验证记录（2026-09-06）

```
✅ init 三库(14/7/9 列全含 relation)
✅ sync: 快照1 · 事件3 · 报告1 全部落库(二次 sync 幂等跳过)
✅ launchd wrapper 快照+同步一体 exit=0
✅ lh health sync / sync-init / status 全链 exit=0
🟡 公开 Publish: 待手动一步(见§四)
```

---
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰 · GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

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
