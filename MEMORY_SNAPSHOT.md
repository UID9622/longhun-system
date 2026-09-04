**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
# 系统记忆快照（MEMORY_SNAPSHOT）

> 星型同步·三件套之一（唯一真源 Notion → 三件套 → 各方开工先读）
> 生成时间: 2026-08-20（UTC+8）
> DNA: `#龍芯⚡️丙午·丙申·癸亥·戊午·䷚颐-3PIECE-MEMORY-SNAPSHOT-v1.0`

---

## 一、四节点星型同步模型（已定）

| 节点 | 角色 | 进出规则 |
|:---|:---|:---|
| **Notion** (uid9622.notion.site) | 唯一真源 | 设计哲学/协议/铁律/人格定义在此定稿，其他节点只读不写 |
| **Git仓库** (longhun-system) | 代码与配置物化层 | 从 Notion 拉设计落地为代码/配置；脚本/部署/HTML存此 |
| **unified_kg.db** | 知识图谱存储 | 结构化关系（节点-边-权重），由 Notion 内容生成，只读不手动改 |
| **CSDN** (uid9622-01.blog.csdn.net) | 对外发布镜像 | 只进不出，不反向同步 |
| **本地未审原料** | 暂存区 | 未归入 Notion 的资料一律"待审原料"，不进生产链 |

> 统一启动协议：任何工作开始前，人类/CodeBuddy/Kimi 先读同三个文件：
> `MEMORY_SNAPSHOT.md` · `DB_REGISTRY.md`（12_DOCS/） · `ALIGN_LEDGER.csv`

## 二、CSDN 文章状态（2026-08-20 实测）

> ⚠️ CSDN 反爬实况：`uid9622.blog.csdn.net`（Kimi 所用）与 `uid9622-01.blog.csdn.net`（正确域名）均 521。
> **本地已有全部正文草稿**（`12_DOCS/dragon-soul-open-hub/academic/csdn_drafts/`），不需要 CSDN 正文即可完成差异分析。

| CSDN 疑似已发布 | 本地对应文件 | 本地版本状态 |
|:---|:---|:---|
| 龍魂权重算法 v3.1-optimized (08-04) | `03_LAYERS/L8_治理层/governance/tech-docs/LONGHUN-WEIGHT-ALGO-v3.1.md` | ✅ 本地已有 v3.1-optimized |
| 图生三维引擎协议 v1.0 (07-28) | `01_protocols/visual-engine/LH-VISUAL-ENGINE-PROTOCOL-v1.0.md` | ✅ 本地已有（可视化引擎协议 v1.0） |
| 锚点优先推演范式 + P0永恒锁 + 369不变量v3.0 | `P0_ETERNAL_LOCK.md` · 洛书369统一版v3.0 | ✅ 本地全有 |

> 结论：Kimi 所称"本地是旧版"**不成立**，v3.1/可视化引擎/P0永恒锁/369v3.0 本地均已存在。
> 待办：CSDN 正文不可达时，以本地 csdn_drafts 为准做差异分析。

## 三、版本快照（2026-08-20）

### 人格
- 花名册 schema: v3.0 (2026-08-01) · 活跃 28 人格（20实战+扩展）
- 人格定义: `personas/`（16份 Markdown）+ `bin/personas/`（执行器）
- 分工矩阵: `20_CONFIG/persona-duty-matrix.json`

### 铁律（IRONLAWS）
- 44 条 · `01_protocols/` + `03_LAYERS/L8_治理层/记错本.md`
- GPG 签名焊死: `bin/lh_gpg_sign.py` · 密钥 `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`

### 引擎/服务
- 192 引擎 · 45 技能 · 7 数字人 · 16 注册服务
- 天眼3D: `https://uid9622.cn/tianyan/tianyan-3d.html`（v1.7·已修复黑屏路径bug）
- 时间戳引擎: `bin/lh_time_engine.py`（LU-Time v4.0·天干地支+64卦）

## 四、数据源

| 数据源 | 类型 | 访问路径 | 最后同步 | 记录数 |
|:---|:---|:---|:---|:---|
| Notion | API | uid9622.notion.site | 2026-08-20 | 367库 |
| unified_kg.db | SQLite | 见 DB_REGISTRY.md | 2026-08-20 | 见 DB_REGISTRY.md |
| 本地台账 | CSV | 根目录 ALIGN_LEDGER.csv | 2026-08-20 | 见 ALIGN_LEDGER.csv |
| CSDN | HTTP | uid9622-01.blog.csdn.net | 未同步（反爬521） | N/A |

## 五、三件套位置

| 文件 | 路径 |
|:---|:---|
| MEMORY_SNAPSHOT.md | 本文件（仓库根目录） |
| DB_REGISTRY.md | `12_DOCS/DB_REGISTRY.md` |
| ALIGN_LEDGER.csv | 仓库根目录 |

---
> 创建: 2026-08-20 · UID9622 × CodeBuddy
> 协议: CC BY-NC-SA 4.0（核心思想层）
