---
DNA: #龍芯⚡️丙午·丙申·辛未·戊戌·䷢晋-KB-REFERENCE-ARCHITECTURE-v1.0-d9f8e2c1
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: CC BY-NC-SA 4.0（核心思想层）
# 抬头模板: [2] 🔧 工程落地执行型（脚本/部署/API）
---

# 龍魂 · Notion 知识库引用架构 v1.0

> 上位蓝图: `01_protocols/LH-NOTION-ENGINE-DATABASE-v1.0.md`（Notion=知识大脑）
> 本协议 = 蓝图落地执行层。冲突时以上位蓝图 + 本协议日期新者为准。

## 0. 一句话

**Notion 存完整版（含 DNA 属性）、本地只存索引摘要、DNA 全部公式计算不手写、社区通过鲲鹏 API 调取知识、Notion 变更回调自动重算。**

---

## 1. 现状盘点（2026-08-25 实测）

| 项 | 状态 | 说明 |
|---|:---:|---|
| 架构蓝图 v1.0 | 🟢 已有 | `LH-NOTION-ENGINE-DATABASE-v1.0.md`·16字段·P1-P10管道 |
| Notion 权限覆盖 | 🔴 仅 3 对象 | integration `longhun-system` 只被共享 1 页+People 库——**大量页面未共享，AI 不可见** |
| 页面 DNA | 🔴 手写无计算 | 蓝图里 DNA 是 Text 手填字段，从未接公式引擎 |
| 本地索引 | 🔴 丢失 | `docs/notion_mirror/INDEX.md`（曾 65 页）本地目录已空 |
| DNA 公式引擎 | 🟢 现成 | `bin/lh_dna_generator.py generate()`（干支四柱+64卦+五行+369+哈希） |
| 统一引擎 | 🟢 本次落地 | `bin/lh_notion_kb.py` v1.0（9 个子命令） |
| 知识库数据库 | 🟢 本次落地 | 已建 16 字段库 `3c703ac9-098d-81b3-9e34-e6ce61083a6b`（第一行已入） |
| 鲲鹏 API | 🟡 待建 | 现有网关可挂 `/api/kb/*`，端点未实现 |

---

## 2. 分层引用架构

```
┌──────────────────────────────────────────────────────┐
│ L5 社区/开源调用方                                     │
│   curl https://uid9622.cn/api/kb/search?q=DNA         │
└───────────────────────┬──────────────────────────────┘
                        │ HTTPS（只读 API）
┌───────────────────────▼──────────────────────────────┐
│ L4 鲲鹏 API 网关（uid9622.cn/api/kb/*）                │
│   GET /api/kb/search?q=         知识检索（只返回摘要+链接）│
│   GET /api/kb/page/{id}         页面详情（Notion 代理）  │
│   GET /api/kb/dna?title=        社区实时计算/校验 DNA    │
│   POST /api/kb/webhook          ① Notion 变更回调       │
│                                 ② 重算 DNA → 更新索引    │
└───────────────────────┬──────────────────────────────┘
                        │ Notion API（读写·token 自愈）
┌───────────────────────▼──────────────────────────────┐
│ L3 Notion 知识库（唯一完整版真源）                      │
│   · 知识库主数据库（16字段: 名称/DNA/DNA校验/分类/摘要/    │
│     来源链接/更新时间 + 页面正文存完整内容）               │
│   · 核心 Hub 页面（归集所有分类入口）                    │
└───────────────────────┬──────────────────────────────┘
                        │ 本地同步（摘要+索引+DNA）
┌───────────────────────▼──────────────────────────────┐
│ L2 本地索引层（省内存核心）                             │
│   · data/notion_kb/index.json（标题/URL/DNA/摘要/链接） │
│   · data/notion_kb/hub_page.md（归集入口）              │
│   · 原则: 不存全文，只存摘要+反向链接                    │
└───────────────────────┬──────────────────────────────┘
                        │ 调用
┌───────────────────────▼──────────────────────────────┐
│ L1 DNA 计算引擎（lh_dna_generator.py）                 │
│   · 公式: 干支四柱+64卦+五行+数字根(369锚点)+标题哈希8位  │
│   · 所有 Notion 页面/知识行 DNA 必须由此引擎计算          │
│   · verify 防手写: 哈希比对，不符=🔴重算                 │
└──────────────────────────────────────────────────────┘
```

---

## 3. DNA 公式化铁律（本次落地核心）

**背景**: 蓝图里 DNA 是手填 Text → 每页 DNA"没有计算"，公式引擎躺在本地没被引用。

**铁律**:
1. 一切 DNA 由 `lh_dna_generator.generate(title, category, action, actor)` 计算，**禁手写**。
2. 写入 Notion 时携带两个字段: `DNA` + `DNA校验`（默认 `🟢公式计算`）。
3. `lh_notion_kb.py verify` 防伪: 标题 SHA256 前 8 位必须与 DNA 末段哈希一致，不符即 🔴。
4. 旧页面手写 DNA → 跑 `lh_notion_kb.py patch <page_id>` 批量重算覆盖。

**闭环示例**（已实测）:
```bash
# ① 建 16 字段库
python3 bin/lh_notion_kb.py create-db <父页面>
# ② 写知识行（DNA 自动公式计算）
python3 bin/lh_notion_kb.py add-entry --db <库ID> --title "xxx" --category 引擎
# ③ 老页面补算 DNA
python3 bin/lh_notion_kb.py patch <page_id> --category DOC
# ④ 防手写验证
python3 bin/lh_notion_kb.py verify <DNA串> --title <标题>
```

---

## 4. 省内存机制（L2 本地索引）

| 存哪里 | 存什么 | 不存什么 |
|---|---|---|
| Notion | 完整正文·原图·全字段 | — |
| 本地 `data/notion_kb/index.json` | 标题/URL/DNA/摘要(≤200字)/反向链接/更新时间 | 全文·大附件 |
| 鲲鹏 | API 网关缓存（可选） | 不落私密数据 |

> 预期收益: 本地仓库大幅瘦身——知识类内容从"全文入库"改为"索引+链接"，正文统一走 Notion。

---

## 5. 鲲鹏 API 设计（L4 已落地 · 2026-08-25）

挂载点: **独立轻量服务** `longhun-kb-api`（127.0.0.1:9633 · systemd 单元 `longhun-kb-api.service`）
  - 代码: `deploy/scripts/longhun-internal-net/kb_api_app.py`（入口）+ `kb_api_router.py`（四端点）+ `lh_dna_generator.py`（DNA 公式依赖，全量复制保公式一致）
  - 对外链路: 公网 → nginx:443 `location /api/kb/` → 127.0.0.1:9633
  - 环境变量（systemd EnvironmentFile `/root/.longhun/kb-api.env`）: `KB_WEBHOOK_KEY`（已生成 600 权限）· `KB_API_PORT=9633` · 可选 `NOTION_KB_INDEX` / `NOTION_TOKEN`
  - 索引同步: 本地 `data/notion_kb/index.json` → 鲲鹏 `/root/.longhun/data/notion_kb/index.json`（`bin/lh_kb_sync.sh all` · launchd 每日 06:00 自动 · 结构感知读写，兼容 pages/items/entries）

| 端点 | 方法 | 功能 | 鉴权 |
|---|---|---|---|
| `/api/kb/search` | GET | 按关键词/分类检索（返回 摘要+链接+DNA） | 公开只读 |
| `/api/kb/page/{id}` | GET | Notion 页面详情代理（有 token 走 live，无则降级索引摘要） | 公开只读 |
| `/api/kb/dna` | GET | 社区实时计算 DNA（传 title/category，复用 lh_dna_generator 公式） | 公开 |
| `/api/kb/webhook` | POST | **Notion 变更回调** → 重算 DNA → 原子更新本地索引 | X-API-Key（`KB_WEBHOOK_KEY`） |

**回调流**（用户问的"回调"）:
```
Notion 页面/知识行变更
  → Notion 数据库 webhook 推送到 鲲鹏 https://uid9622.cn/api/kb/webhook（X-API-Key）
  → 服务端重算 DNA（lh_dna_generator.generate·公式一致）+ 原子更新索引
  → （可选）Bark 推送提醒
```
> 注: Notion 原生 webhook 属 Enterprise 功能（集成需评审）。降级方案:
> 本地 cron 每 N 分钟 `lh_notion_kb.py sync` 增量比对 last_edited，效果等价且零成本。
> 🔴 NOTION_TOKEN 按"入云需授权"原则默认不配置，page 端点走本地索引降级；如需 live 代理由 UID9622 单独授权后注入 env。

---

## 6. 命令速查（lh_notion_kb.py v1.0）

| 命令 | 功能 | 实测 |
|---|---|---|
| `list` | 扫描 token 可访问页面/库 | 🟢 3 对象 |
| `dna <标题> [--category --action]` | 公式计算 DNA | 🟢 |
| `verify <DNA> --title <标题>` | 防手写验证 | 🟢 抓出假哈希 |
| `patch <page_id>` | 老页面补算 DNA 写回 | 🟢 callout 落页 |
| `create-db <父页面>` | 建 16 字段知识库 | 🟢 库已建 |
| `add-entry --db --title --category` | 写知识行+自动算 DNA | 🟢 首行已入 |
| `index` | 生成本地索引（省内存） | 🟢 |
| `hub` | 生成核心 Hub 归集页 | 🟢 |
| `sync` | list+dna+index 三合一 | 🟢 |

---

## 7. 权限待办（老大需操作 · 卡脖子项）

当前 integration `longhun-system` 只能看到 3 个对象，**其余页面/数据库全部不可见**。要让"Notion 用好"，必须:

1. **把需要归集的页面/数据库共享给 integration**:
   - Notion 里每个页面右上角 `···` → `Connections` → 添加 `longhun-system`
   - 批量方式: 在父页面加连接，子页面默认继承（验证中）
2. 共享后重跑 `lh_notion_kb.py list` → 可见对象应大幅增加
3. 确认后进入批量归集: 对每个页面 `patch` 补算 DNA + 写入 Hub

> ⚠️ 若无共享权限，社区 API 只能服务"已共享页面"，未共享内容永远不可见——这是硬边界，不是技术问题。

---

## 8. 后续层（一层一层做）

| 层 | 内容 | 状态 |
|---|---|---|
| L1 | DNA 公式引擎接入 | 🟢 本次 |
| L2 | 本地索引+Hub | 🟢 本次 |
| L3 | Notion 知识库建库+写行 | 🟢 本次（待权限放开后批量归集） |
| L4 | 鲲鹏 `/api/kb/*` + webhook 回调 | 🟢 已落地（:9633 独立服务 + nginx 反代 · 冒烟 6/6 · 审计闸 9/9） |
| L5 | 社区接入 + 文档 + 示例 | 🟢 本次（API Guide `LH-NOTION-KB-API-GUIDE-v1.0.md` · 索引同步常态化 launchd `com.longhun.kb-sync` · 公网 search 实测命中） |

---

## 9. 变更记录

| 版本 | 日期 | 内容 |
|---|---|---|
| v1.2 | 2026-08-25 | L5 落地: `bin/lh_kb_sync.sh`（sync+push+留痕）· launchd `com.longhun.kb-sync` 每日 06:00 索引同步常态化 · 社区接入手册 `LH-NOTION-KB-API-GUIDE-v1.0.md` · 公网 search 实测 hits=1 · 索引路径修正为 `/root/.longhun/data/notion_kb/index.json` |
| v1.1 | 2026-08-25 | L4 落地: `kb_api_app.py`+`kb_api_router.py` 独立服务 :9633 · nginx `/api/kb/` 反代 · webhook X-API-Key 鉴权 · 索引结构感知读写（entries/pages/items）· 冒烟 6/6 · 审计闸 9/9 🟢 |
| v1.0 | 2026-08-25 | 首版: 分层引用架构·DNA公式化铁律·本地索引机制·鲲鹏API设计·权限待办 |

<!-- GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F -->
