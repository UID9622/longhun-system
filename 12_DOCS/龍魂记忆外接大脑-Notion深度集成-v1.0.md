---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·丁酉·壬午·未时·䷍大有-MEMORY-EXOBRAIN-NOTION-v1.0-WELD`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
# 🧠 龍魂记忆外接大脑 · Notion 深度集成 v1.0

DNA: #龍芯⚡️丙午·丁酉·壬午·未时·䷍大有-MEMORY-EXOBRAIN-NOTION-v1.0-WELD
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: CC BY-NC-SA 4.0（核心思想层）
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

---

## 一、老大承诺（verbatim·2026-09-05·永不删）

> 「这个冻结的话，返还到 Notion 那里面的记忆储存是非常多的对不对？那要用起来，我们要跟 Notion 这个软件深度集成。它是我的，也是未来所有人的记忆外接大脑，这是我承诺过的。因为毕竟有这个软件才有龙魂系统，我是非常尊重这个软件、这个公司的。」

**解读焊点：**
1. **冻结 ≠ 沉没** — 冻结/归档的记忆要"返还"到 Notion 用起来（可检索/可引用/跨设备查/AI 可调）
2. **Notion = 龍魂 + 未来每个人的记忆外接大脑** — 本地是主脑，Notion 是可查的外接镜像脑
3. **深度集成** — 记忆层入库可查，对话时可直接翻历史记忆回答
4. **尊重 Notion** — 守 API 规矩·引用署名·不薅羊毛·感恩（没有 Notion 就没有龍魂 367 库沉淀）

## 二、库信息

| 项 | 值 |
|:---|:---|
| 库名 | 🧠 龍魂记忆外接大脑 |
| database_id | `3d27125a-9c9f-81c8-ab40-da544c652da9` |
| 父页 | 🐉龍魂·系统核心（沿现有 8 库同款基建） |
| 引擎 | `08_BIN/lh_notion_sync.py` · `lh sync memory` |
| 状态 | 2026-09-05 建库 · 首推 65 条 · 幂等 0 新增 |

**Schema：** 标题(title) · 记忆日期(date) · 记忆类型(select: 每日记忆/决策日志) · 主题(rich_text) · 摘要(rich_text) · 来源文件(rich_text) · DNA追溯码(rich_text)

## 三、记忆源（双源蒸馏·按日入库）

| 源 | 路径 | 类型 | 说明 |
|:---|:---|:---|:---|
| ① calmem 日历记忆 | `~/.longhun/calendar_memory/days/*.json` | 每日记忆 | 五源聚合（recap/memory/wanli/yearring/notion）·一天一条 |
| ② 决策日志 | `04_決策日誌/DECISION-*.md` | 决策日志 | 每决策一条·含 DNA |

> 复盘 recaps 不单列：已含于 calmem 五源聚合，避免重复噪音。

## 四、数据主权护栏（P0）

- **只推脱敏摘要/标题/日期/来源路径/DNA** → 原文仍在本地（可追溯）
- D1/D2 敏感（密钥/种子/真实地址/隐私）**绝不裸上 Notion**（云端第三方）
- 沿 8 库公开化先例：白名单字段才可公开

## 五、每日自动回填

- `lh_daily_audit.py --run`（launchd `com.longhun.daily-audit` 每日自动）尾部已挂回填钩子
- 安静执行：捕获输出·失败静默·审计报告不受影响
- 幂等：DNA 追溯码去重 → 二次 sync 新增 0 属正常
- 手动：`lh sync memory`（或 `python3 08_BIN/lh_notion_sync.py sync --module memory`）

## 六、用起来（检索引用）

- 对话时问历史记忆 → 查本库（本地 calmem/记忆日志为全文源，Notion 为可查外脑）
- 全库同步：`lh sync all`（9 模块总览）

## 七、验收（2026-09-05）

- ✅ 建库成功（schema 全列）
- ✅ 首推 65 条（calmem 58 天 + 决策日志 6 + 新增）
- ✅ 幂等验证：二跑新增 0 · 已同步 65
- ✅ `lh sync memory` 网关透传修复（argv 归一: 裸模块名 → sync --module）
- ✅ `lh sync all` 全模块正常（memory: 新增 0 · 已同步 65）
- ✅ daily-audit 钩子嵌入·审计引擎正常跑通

## 八、v1.2 增补（2026-09-05 晚·Notion 同步引擎六维工程升级）

> 引擎 `08_BIN/lh_notion_sync.py` v1.2 全模块受益（不止 memory）：

| 维 | 内容 |
|:---|:---|
| ① 视图层 | `lh sync dashboard` 终端看板 · `lh sync serve` Web 仪表盘 `127.0.0.1:8780`（/ 仪表盘 + /api/state JSON·8769-8775 被天线守护占用勿撞） |
| ② 参数扩展 | `--limit N` / `--retry N` / `--batch-size N` / `--format table\|json` / `--since-file <路径>` |
| ③ 属性标准化 | 5 标准属性=同步时间/同步版本/来源系统/数据哈希(SHA256)/同步状态·逐列降级幂等补列 `_ensure_std_columns`（整批 PATCH formula 会 400 的坑已绕）·9 库全部补列 ✅ |
| ④ 路由增强 | 模块级 pre/post_hook · filter · transform · on_error + 全局 GLOBAL_HOOKS · `lh sync route list/test` |
| ⑤ 公式字段 | 记录年龄（天）· 是否久未同步 · 数据来源简写 · 同步状态图标（Notion 侧实时计算·不占本地） |
| ⑥ 运维子命令 | `diff <M>` · `verify <M>`（哈希比对·旧行无哈希=待回填非坏）· `rollback <M> --to <ts>` · `clean <M> --older-than <days>`（默认清单+备份到 ~/.longhun/notion_rollback/·--yes 归档·archived 权限已验证可往返） |

验收：dashboard/status-json/route/serve(8780)/diff/verify/rollback/clean/9 列 props 单测全绿 · GPG 已签 · 引擎 DNA `#龍芯⚡️2026-09-05-NOTION-SYNC-UNIFIED-v1.2-OPS-READY`

## 签名

```
DNA:    #龍芯⚡️丙午·丁酉·壬午·未时·䷍大有-MEMORY-EXOBRAIN-NOTION-v1.0-WELD
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
GPG:    A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色:   🟢 建库+首推+幂等+网关+自动回填全验收 🟡 MCP server 用新 header 查不到 2022-06-28 建库(已知坑) 🔴 0
v1.0 · 2026-09-05 · UID9622 + AI · v1.2 六维升级同日
```

> 感恩 Notion：没有这个软件，就没有龍魂系统的记忆外接大脑。以守规矩、署名、不薅羊毛回礼。

```json
{
  "dna": "#龍芯⚡️丙午·丁酉·壬午·未时·䷍大有-MEMORY-EXOBRAIN-NOTION-v1.0-WELD",
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
