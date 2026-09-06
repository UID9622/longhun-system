---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·丙申·戊申·午时·䷗复-DB-REGISTRY-UID9622-v1.0`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
# 🗄 龍魂 · 数据库统一注册表 DB_REGISTRY v1.0

**DNA:** `#龍芯⚡️丙午·丙申·戊申·午时·䷗复-DB-REGISTRY-UID9622-v1.0`
**创建者:** 诸葛鑫（UID9622）
**协议:** CC BY-NC-SA 4.0（核心思想层）
**License:** MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
**三色:** 🟡 待核（23 库已盘点 · 2 空壳 · 1 疑似重复 · 待 UID9622 裁定）

> **为什么建这张表**：2026-08-20 执行包三大欠账之一——「20+ SQLite 无管理」。
> 数据库散落各层、无统一登记、无职责说明、部分库空壳或重复。本表为**唯一注册真相源**：
> 新增 SQLite 必须登记后使用；访问一律只读 URI（`?mode=ro`）；敏感字段端侧加密后才入库。

---

## 一、总览（2026-08-20 实测）

| 指标 | 值 |
|:---|:---|
| 登记库数 | **23**（全部只读可访问 ✅） |
| 总占用 | **≈1.9 GB**（大头：workspace_index 1.37G + notion_archive 390M + vectors 97M） |
| 表数合计 | 92 张 |
| 🚨 空壳库 | 2（`data/knowledge_sources.db` 0表 · `brain/unified_kg.db` 6表空） |
| ⚠️ 疑似重复 | 2（DNA 账本两处同构） |
| 未登记 | 第三方库（browser_profile / ComfyUI 等，已 gitignore） |

---

## 二、注册表全表

### A. 知识 & 索引（3）

| 路径 | 大小 | 表数 | 职责 | 状态 |
|:---|:---|:---:|:---|:---|
| `12_DOCS/workspace_index.db` | 1.37 GB | 13 | 工作区文件索引 + FTS 全文检索 + DNA/GPG 签名记录 | 🟢 活跃 |
| `.state/vector_index/vectors.sqlite` | 97 MB | 1 | 语义向量索引（`lh idx` 认知索引） | 🟢 活跃 |
| `brain/unified_kg.db` | 4 KB | 6 | 统一知识图谱（sources/nodes/edges/node_vectors/sync_log） | 🟡 **空库**·P1 引擎已回退 graph_data.json |

### B. Notion 镜像 & 同步（3）

| 路径 | 大小 | 表数 | 职责 | 状态 |
|:---|:---|:---:|:---|:---|
| `12_DOCS/notion_mirror/notion_archive.db` | 390 MB | 4 | Notion 全库镜像归档（pages/blocks） | 🟢 活跃 |
| `data/notion_sync.db` | 60 KB | 14 | Notion 增量同步 + pages/blocks FTS | 🟢 活跃 |
| `data/notion_chat_history.db` | 20 KB | 3 | Notion 对话历史（chat_history/chat_sessions） | 🟢 活跃 |

### C. 审计 & 治理（6）

| 路径 | 大小 | 表数 | 职责 | 状态 |
|:---|:---|:---:|:---|:---|
| `07_AUDIT/dna_ledger.db` | 24 KB | 4 | DNA 资产账本（assets/chain_breaks/forensic_log） | 🟡 **疑重复** |
| `governance/audit/dna_ledger.db` | 24 KB | 4 | 同上（inode 不同·两套账本） | 🟡 **疑重复**·待裁定主库 |
| `07_AUDIT/ai_hub_audit.db` | 28 KB | 2 | AI 归集 Hub 审计日志 | 🟢 活跃 |
| `logs/transparent_audit.db` | 32 KB | 3 | 透明审计（结果/历史/yearring·中文表名） | 🟢 活跃 |
| `cnsh/data/logs/audit.db` | 16 KB | 3 | CNSH 审计日志（audit_log/call_stats） | 🟢 活跃 |
| `25_TASK_ENGINE/tasks.db` | 28 KB | 3 | 任务引擎（tasks/task_steps/execution_logs） | 🟢 活跃 |

### D. 记忆 & 人格（3）

| 路径 | 大小 | 表数 | 职责 | 状态 |
|:---|:---|:---:|:---|:---|
| `brain/memories.db` | 20 KB | 3 | 长期记忆（memories/chain_anchor） | 🟢 活跃 |
| `data/persona_runtime.db` | 40 KB | 4 | 人格运行时（personas/sessions/persona_memory） | 🟢 活跃 |
| `data/think_pipeline/pipeline.db` | 24 KB | 2 | 思维管道审计（pipeline_audit） | 🟢 活跃 |

### E. 生态 & 经济（2）

| 路径 | 大小 | 表数 | 职责 | 状态 |
|:---|:---|:---:|:---|:---|
| `longhun-dev-ecosystem/data/developers.db` | 45 KB | 5 | 开发者生态（developers/code_dna/contributions/payment_orders/monthly_fee_records） | 🟢 活跃 |
| `data/flow_fusion.db` | 28 KB | 4 | 流场融合（fusion_events/engine_heartbeats/fusion_state） | 🟢 活跃 |

### F. 状态机 & 学习器（5）

| 路径 | 大小 | 表数 | 职责 | 状态 |
|:---|:---|:---:|:---|:---|
| `.state/collective_intel/collective.sqlite` | 20 KB | 2 | 集体智能（cooccurrence/sessions） | 🟢 活跃 |
| `.state/terminal_writer/writer.sqlite` | 16 KB | 3 | 终端写作（writer_logs/shame_wall） | 🟢 活跃 |
| `.state/industry_governance/governance.sqlite` | 45 KB | 6 | 行业治理（governance_events/honor_wall/unauthorized_ai 等） | 🟢 活跃 |
| `.state/behavior_learner/behavior.sqlite` | 28 KB | 1 | 行为学习器（behavior） | 🟢 活跃 |
| `03_LAYERS/L7_数据层/qwen_hallucination_db/qwen_audit_scores.sqlite3` | 40 KB | 4 | Qwen 幻觉审计分（model/persona/skill_scores） | 🟢 活跃 |

### G. 空壳 & 待建（2）

| 路径 | 大小 | 表数 | 职责 | 状态 |
|:---|:---|:---:|:---|:---|
| `data/knowledge_sources.db` | 4 KB | **0** | 知识源注册（骨架已建·未建表） | 🔴 空壳·待 P3 接入 |
| `brain/unified_kg.db` | 4 KB | 6 | 统一知识图谱 | 🟡 表结构在·无数据·引擎已回退文件源 |

---

## 三、告警与待办（待 UID9622 裁定）

| # | 级别 | 事项 | 建议 |
|:---:|:---:|:---|:---|
| 1 | 🟡 | `07_AUDIT/dna_ledger.db` 与 `governance/audit/dna_ledger.db` 同构两套账本 | 冻结一套·裁定主库·另一套只读归档 |
| 2 | 🔴 | `data/knowledge_sources.db` 空壳 0 表 | P3 Notion 接入时建表落地 |
| 3 | 🟡 | `brain/unified_kg.db` 空库 | 待知识矩阵写入引擎接入（引擎已回退文件源，不报 0） |
| 4 | 🟡 | `logs/transparent_audit.db` 中文表名 | 兼容性风险·建议加英文视图别名 |

---

## 四、治理规则（焊死）

1. **新增 SQLite 必登记**：建库即填本表（路径/职责/负责人），禁裸建。
2. **只读访问**：AI/脚本一律 `sqlite3.connect("file:<path>?mode=ro", uri=True)`，禁直接写核心库。
3. **敏感字段**：手机号/身份证/画像等端侧加密后入库（第五层 5.3 铁律）。
4. **空库不报 0**：铁律 #IRON-MISSING-SOURCE-NEVER-REPORT-ZERO-v1.0——扫不到报「数据源缺失」。
5. **重复即冻结**：发现同构库 → 冻结一套 → 登记 → 裁定 → 归档，禁直接删除。

---

## 五、扫描方法（可复现）

```bash
find . -name "*.db" -not -path "*/.venv*" -not -path "*/node_modules/*" \
  -not -path "*/11_DATA/*" -not -path "*/_work/*" -not -path "*/dist/*" \
  -not -path "*/models/*" -not -path "*/archive*" -not -path "*/backups*" \
  -not -path "*/backup*" -not -path "*/_QUARANTINE/*" -not -path "*/__pycache__/*"
```

> 2026-08-20 实测 23 库 · 全部只读可访问 · 2 空壳 · 1 疑似重复

```json
{
  "dna": "#龍芯⚡️丙午·丙申·戊申·午时·䷗复-DB-REGISTRY-UID9622-v1.0",
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
