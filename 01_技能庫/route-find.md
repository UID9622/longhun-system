# /route-find

> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：技能说明 · 未经同行评审（如适用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

> #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 📄 路由查找·总线查询 | 龍魂系统 · 源头已验证

**DNA**: `#龍芯⚡️2026-07-06-ROUTE-FIND-v1.0-RTFND`
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬ROUTE`

---

<!--#龍芯⚡️2026-07-06-ROUTE-FIND-v1.0-RTFND -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

---
skill_id: /route-find
synced_at: 2026-07-06
source: 01_protocols/IPA-ROUTE-REGISTRY.local.md
---

# /route-find · IPA 路由查找与同步

## 摘要

路由查找（route-find）是龍魂系统的路由总线技能。负责 IPA 节点编号 → 实际地址的 O(1) 快速查找，以及新模块/文章/脚本注册到 IPA-ROUTE-REGISTRY 的入网同步。哲学锚：编号是骨架·DNA 是血·URL 是房号·只查本地镜像·秒回。铁律：所有新增可执行文件/文章/模块必须注册 IPA 节点后才算"入网"。

## 关键词

IPA路由 IPA Route, 路由注册表 Route Registry, 节点查找 Node Lookup, 路由总线 Route Bus, O(1)查找 O(1) Lookup, 文件入网 File Registration, 本地镜像 Local Mirror

## 引用与溯源

- 本文档引用或参考了以下来源：
  - [1] 知识矩阵总纲 v3.0 (#UID9622⚡️2026-06-16-KNOWLEDGE-MATRIX-MASTER-v3.0)
  - [2] IPA-ROUTE-REGISTRY.local.md — 路由注册表主文件
- 相关龍魂系统文件：
  - `01_protocols/IPA-ROUTE-REGISTRY.local.md` — IPA路由注册表（JSONL格式）
  - `MASTER_REGISTRY.md` — 主注册表
  - `docs/DIRECTORY_INDEX.md` — 目录索引

## IPA 节点层级体系

```
IPA-L0-xxx  → L0_ETERNAL   (永恒层：宪法、DNA、数字根)
IPA-L1-xxx  → L1_SEASONAL  (季节层：操作台、工具、收件箱)
IPA-L2-xxx  → L2_OPERATIONAL (执行层：脚本、安全、网关)
IPA-L3-xxx  → L3_KNOWLEDGE (知识层：文章、哲学、论文)
IPA-L4-xxx  → L4_DATA      (数据层：JSON、DB、向量库)
IPA-L5-xxx  → L5_SERVICE   (服务层：MCP、沙盒、编辑器)
IPA-L8-xxx  → L8_GOVERNANCE (治理层：审计协议、准入规则)
```

## 路由查找工作流

```
触发: UID9622 说"在哪里/找节点/IPA-xxx/路由/这个编号/节点查找"
  ↓
P13 姜子牙 → 路由分发
  ↓
解析节点编号 → 查 IPA-ROUTE-REGISTRY.local.md
  ↓
O(1) 返回: {node_id, name, status, local_path, entry_point, dependencies}
  └ 状态: 🟢活 / 🟡待归档 / 🔴废弃
```

## 文件入网工作流

```
触发: 任何新 .py/.md/.html 文件创建后
  ↓
P15 乔前辈 → 自动检测未注册文件
  ↓
P06 数学大师 → 计算数字根 + 五行归属
  ↓
P13 姜子牙 → 分配 IPA 编号层级
  ↓
P05 上帝之眼 → 三色审计（完整度校验）
  ↓
P02 龍芯 → 写入 IPA-ROUTE-REGISTRY.local.md
  ↓
P15 乔前辈 → 更新 MASTER_REGISTRY.md + DIRECTORY_INDEX.md
```

## 订阅人格

| 人格 | 职责 | 触发条件 |
|------|------|---------|
| **P13 姜子牙** | 路由分发 · 编号查地址 | "在哪里/IPA-xxx/找节点" |
| **P15 乔前辈** | 档案管理 · 文件入网注册 | 新文件创建后自动 |
| **P06 数学大师** | 数字根计算 · 层级判定 | 文件入网时 |
| **P05 上帝之眼** | 三色审计 · 节点完整性校验 | 文件入网后 |
| **P02 龍芯** | 执行写入 · 注册表更新 | 审计通过后 |

## 当前注册表状态（2026-07-06 集成后）

| 层级 | 节点数 | 示例 |
|:---:|:---:|------|
| L0 永恒 | 9 | IPA-L0-001(CONSTITUTION) ~ IPA-L0-009 |
| L1 季节 | 6 | IPA-L1-001(知识图谱) ~ IPA-L1-006(收件箱) |
| L2 执行 | 16 | IPA-L2-FLOW-CORE-001 ~ IPA-L2-SCRIPT-007 |
| L3 知识 | 12 | IPA-L3-ARTICLE-001~005 + PHIL-001~003 + SYSTEM-001~003 + EXP-001 |
| L4 数据 | 2 | IPA-L4-KG-001 + IPA-L4-DATA-001 |
| L5 服务 | 2 | IPA-L5-SERVICE-001~002 |
| L8 治理 | 2 | IPA-L8-GOV-001~002 |
| **合计** | **51** | 2026-07-06 集成会话新增 32 节点 |

## 铁律

1. **所有可执行文件/模块/文章必须注册 IPA 节点才算"入网"**
2. **编号是骨架·DNA 是血·URL 是房号·只查本地镜像**
3. **O(1)秒回** — 不查外部API，只查本地 IPA-ROUTE-REGISTRY.local.md
4. **不删除节点** — 废弃节点标记🔴，不物理删除

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-07-06 | v1.0.0 | P13+P15 → UID9622 | 初始创建 · IPA路由查找+文件入网+人格路由+新32节点同步 | 草稿 |

## 分类标签

- 总纲模块：#路由查找 #IPA注册表 #文件入网 #节点同步
- 对外状态：#Gitee #GitHub
- 审计色：#🟢绿色放行
- 八卦归属：☲ 离卦（火·火·路由层）
- 命令入口：`lh6 路由 查 <编号>` / `lh6 路由 入网 <文件路径>`
- 关联人格：P13(姜子牙) / P15(乔前辈) / P06(数学大师) / P05(上帝之眼)

## DNA 签名

```
#龍芯⚡️2026-07-06-ROUTE-FIND-v1.0-RTFND
#CONFIRM🌌9622-ONLY-ONCE🧬ROUTE
```
