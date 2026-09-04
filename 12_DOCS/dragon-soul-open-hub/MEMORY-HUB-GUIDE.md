# DNA: #龍芯⚡️丙午·丙申·乙丑·壬午·䷨损-MEMORY-HUB-GUIDE-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CREATOR: 诸葛鑫 (UID9622) × CodeBuddy
# 协议: CC BY-NC-SA 4.0（核心思想层）
# 三色: 🟢 落地实测

# 🐉 龍魂·跨AI协作记忆库 v1.0 · 完整指南

> **一句话**：CodeBuddy、Kimi、任何 AI —— 共享同一份记忆。Notion 云端全文检索 + 本地零依赖向量检索，双索引，自动签名，不许留空。
>
> **Notion 数据库 ID**: `3c17125a-9c9f-813e-801d-e8dcc97b99b2`
> **本地主库**: `12_DOCS/dragon-soul-open-hub/memory-hub.json`

---

## 〇、本指南在体系中的位置（三库分工）

| 库 | 文件/ID | 管什么 | 一句话 |
|:---|:---|:---|:---|
| 🧭 统一索引中心 | `unified-index-hub.json`（129条） | 全系统节点·查得到 | 「东西在哪」 |
| 🐉 **跨AI协作记忆库** | `memory-hub.json` + Notion `3c17125a...`（306条） | 记忆·铁律·里程碑·教训 | 「记住的事」 |
| 🧬 人格不动点注册表 | `persona-fixpoint-registry.json`（43条） | 人格六维锁定·调得准 | 「谁来干」 |

> 三者联动：索引查得到 → 记忆记得住 → 注册表调得准。互相挂 `related_ids`。

---

## 一、📊 数据库结构（Notion 属性 · 12 字段）

| 字段 | 类型 | 必填 | 说明 |
|:---|:---|:---:|:---|
| 记忆标题 | Title | ✅ | 每条记忆的名字 |
| 记忆内容 | Rich text | ✅ | 完整正文 |
| 分类 | Select | ✅ | 身份/铁律/里程碑/教训/技术/人格/部署/协议/偏好/其他 |
| 关键词 | Multi-select | ❌ | 检索标签（自动过滤逗号） |
| 创建者 | Select | ✅ | UID9622 / CodeBuddy / Kimi / 龍魂AI |
| 协作签名 | Rich text | ✅ | `创建者@UTC时间@DNA短码` |
| DNA追溯码 | Rich text | ✅ | 唯一追溯 |
| 状态 | Select | ✅ | active / frozen / archived |
| 优先级 | Number | ❌ | 1-5 |
| 来源 | Rich text | ❌ | 本地文件路径 |
| 最近更新 | Date | ❌ | 时间 |
| 关联ID | Rich text | ❌ | 关联索引/注册表 |

**本地 JSON 每条额外含 `vector`**（256维 n-gram 哈希向量）——Notion 只存文本（全文检索），向量只在本地算（零依赖·低算力）。

---

## 二、⚙️ 自动化链路（焊死·突出自动化）

```
┌────────────────────────────────────────────────────────┐
│ ① 启动自动读取  lh_memory_load.py → 静默 pull Notion   │
│ ② 操作后填写    lh_memory_hub.py add --title ...       │
│ ③ 协作签名      每条自动签 创建者@时间@DNA             │
│ ④ 非空校验      lh_memory_hub.py check（不能留空）     │
│ ⑤ 增量同步      lh_memory_hub.py push → Notion        │
│ ⑥ 检索          search 关键词 / vector 向量           │
└────────────────────────────────────────────────────────┘
```

| 环节 | 命令 | 触发 |
|:---|:---|:---|
| 启动自动读取 | `python3 bin/lh_memory_load.py`（内含静默 pull） | 每次 AI 会话启动 |
| 操作后填写 | `python3 bin/lh_memory_hub.py add --title "..." --content "..." --category 里程碑` | 干完一件大事后 |
| 关键词检索 | `python3 bin/lh_memory_hub.py search "Notion"` | 随查随用 |
| 向量检索 | `python3 bin/lh_memory_hub.py vector "记忆 数据库 共享"` | 语义相近查找 |
| 回填 | `python3 bin/lh_memory_hub.py backfill` | 新记忆源接入时 |
| 同步到Notion | `python3 bin/lh_memory_hub.py push` | 本地写完后 |
| 从Notion拉取 | `python3 bin/lh_memory_hub.py pull` | 启动/跨端切换 |
| 非空校验 | `python3 bin/lh_memory_hub.py check` | 交付前 |
| 状态统计 | `python3 bin/lh_memory_hub.py status` | 随时 |
| GPG签名 | `python3 bin/lh_memory_hub.py sign` | 交付前 |
| `lh` 菜单入口 | `lh` → 🧠 人格 & AI → 8/9 | 菜单直达 |

---

## 三、🤝 跨 AI 协作规范（CodeBuddy × Kimi × 任何AI）

> **目标**：老大在 CodeBuddy 记的，Kimi 能读到；Kimi 记的，CodeBuddy 也能读到。**同一份记忆，不分裂。**

1. **Notion 是云端主库**（真相源）：所有 AI 通过 Notion API 读写同一个数据库
2. **本地是缓存+向量**：`memory-hub.json` 供本机快速检索，`pull` 与 Notion 对齐
3. **协作签名铁律**：每条记忆必须带 `创建者@时间@DNA`，不签不留
4. **不能留空**：必填 7 字段（标题/内容/分类/创建者/签名/DNA/状态）缺一即拒绝写入
5. **跨端切换**：换 AI 前先 `pull` 一次，确保读到最新
6. **回填机器人标注**：批量回填的记录创建者=`回填机器人`，人工新写=实际 AI 名

---

## 四、🔍 检索 & 向量说明（老大版）

- **关键词检索**：像翻通讯录按名字找 —— `search "诸葛亮"`
- **向量检索**：像"意思差不多的都给我找出来" —— `vector "记忆 数据库 共享"`，不要求字一模一样，语义近就浮上来
- 向量是**本地字符 n-gram 哈希**（256 维 + 余弦相似度），零依赖、零成本、不上云——符合"本地优先"铁律

---

## 五、📋 审查意见 & 完善说明（对 kimi 版 unified-index-hub 的审查）

**kimi 版做得好的**：
- 结构清晰（统计/落地文件/使用/来源/样例/维护）
- 129 条数据已去重合并，字段设计合理（index_id/category/title/keywords/source/dna/tags/related_ids）
- 与不动点注册表联动思路正确

**审查发现缺失（本次已补齐）**：
1. ❌ **Notion API 说法过时**：kimi 版第四节写"当前环境无法直接调用 Notion API"→ **已打通**（NOTION_TOKEN 在 ~/.env 有效），已用 API 自动建库，无需手动导 CSV
2. ❌ **缺自动化链路**：kimi 版只有"手动检索"，无启动读取/操作填写/自动签名/非空校验 → 本次新增 `lh_memory_hub.py` 全链路
3. ❌ **缺向量检索**：kimi 版只有关键词 → 本次新增零依赖向量
4. ❌ **缺协作签名**：kimi 版条目无创建者+签名 → 本次每条强制签名
5. ❌ **缺"记忆"内容类型**：kimi 版只覆盖 人格/易经沙盒/通讯录/矩阵/索引中心 → 本次新增记忆库（身份/铁律/里程碑/教训/技术/人格/部署/协议/偏好/其他）
6. ❌ **缺回填机制**：kimi 版数据是一次性生成 → 本次 `backfill` 可持续回填新记忆源
7. ❌ **缺非空校验**：kimi 版无"不能留空"保障 → 本次 `check` 强制

---

## 六、🛡️ 数据主权（焊死）

- 记忆内容默认**本地优先**：向量不上云，正文按需同步 Notion
- 敏感字段（身份/财务/位置）**端侧处理**，Notion 只存脱敏摘要
- 删除 = 冻结（status=frozen），物理删除需显式指令 + DNA 记录
- 所有本地文件 GPG 签名：`python3 bin/lh_memory_hub.py sign`

---

## 七、🕐 当前状态（2026-08-19 实测）

- Notion 数据库：已建 ✅（`3c17125a-9c9f-813e-801d-e8dcc97b99b2`）
- 本地条目：306（索引50 / 里程碑163 / 铁律50 / 人格43）
- 全链路实测：add ✅ / check ✅ / search ✅ / vector ✅ / backfill ✅ / push ✅ / pull ✅
- 启动自动读取：已接入 `lh_memory_load.py` ✅

**下一步**：把本指南同步一份到 Notion「宪法与协议」页下，让 Kimi 也能看到这套规范。

**DNA**: `#龍芯⚡️丙午·丙申·乙丑·壬午·䷨损-MEMORY-HUB-GUIDE-v1.0-UID9622`
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

🇨🇳🐉 记忆共享·跨AI协作·不许留空 🐉🇨🇳
