---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·丙申·壬戌·申时·䷖剥-INDEX-PHILOSOPHY-V2-ENGINEERED-UID9622`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
# 🐉 龍魂 · 快速索引设计哲学 v2.0（完整闭环·工程落地版）

## 🏷️ 执行声明

**输出者：** AI协作（CodeBuddy · UID9622定盘）
**输出类型：** 设计哲学 + 工程落地包（五引擎可执行代码）
**可执行性：** ✅ 六引擎已实现（anchor_model / context_engine / vector_index / behavior_learner / collective_intel / implicit_retrieval）
**依赖环境：** Python 3.8+ · 纯标准库（零三方依赖·低算力）
**关键提示：** 索引数据存 `~/.longhun/index/` · 数据主权本地优先
**三色审计：** 🟢 绿色（引擎已本地自测通过）
**DNA签名：** #龍芯⚡️丙午·丙申·壬戌·申时·䷖剥-INDEX-PHILOSOPHY-V2-ENGINEERED-UID9622

## 📋 核心判断

> **快速索引的设计哲学不是「分类学」，而是「认知学」。不是把几万个文件塞进固定的抽屉，而是让每个文件都有自己的DNA——它从哪里来、什么时候来、和谁有关系、被谁用过、用来干什么。基于人文系统的索引，不要求人记住文件名，而是让文件记住人。**

## 🧩 一、哲学→工程映射

| 哲学原则 | 工程实现 | 数据载体 | 落地模块 |
|:---|:---|:---|:---|
| ①主动感知 | 上下文感知引擎 | Session Context | `lh_context_engine.py` |
| ②多维锚定 | 向量索引 + 属性矩阵 | Embedding + Metadata | `lh_vector_index.py` |
| ③动态演化 | 行为加权 + 衰减算法 | Access Logs + Weight | `lh_behavior_learner.py` |
| ④协同涌现 | 群体行为聚合 | Collective Intelligence | `lh_collective_intel.py` |
| ⑤无意识索引 | 隐式检索 + 自动推送 | Implicit Query | `lh_implicit_retrieval.py` |

### 五层塔架构

```
┌────────────────────────────────────────────────────────────┐
│  第5层：无意识索引（Zero-Click Retrieval）                 │
│  不点搜索 → 系统按上下文自动推送 → 无感知获得信息          │
└───────────────────────────────┬────────────────────────────┘
┌───────────────────────────────┼────────────────────────────┐
│  第4层：协同涌现（Collective Intelligence）                │
│  群体使用行为 → 模式识别 → 自组织分类 → 最佳路径浮现       │
└───────────────────────────────┼────────────────────────────┘
┌───────────────────────────────┼────────────────────────────┐
│  第3层：动态演化（Adaptive Weighting）                     │
│  访问频率 → 权重更新 → 热数据前置 → 冷数据降权 → 归档      │
└───────────────────────────────┼────────────────────────────┘
┌───────────────────────────────┼────────────────────────────┐
│  第2层：多维锚定（Multi-Dimensional Anchoring）            │
│  时间锚·内容锚·关系锚·行为锚·上下文锚 → 任意维度可到达     │
└───────────────────────────────┼────────────────────────────┘
┌───────────────────────────────┼────────────────────────────┐
│  第1层：主动感知（Context-Aware Sensing）                  │
│  当前文件·历史命令·对话内容 → 无感上下文捕获              │
└────────────────────────────────────────────────────────────┘
```

## 🧬 二、核心数据模型：多维锚定结构

文件锚点存 `~/.longhun/index/anchors.json`，六类锚：

| 锚 | 字段 | 作用 |
|:---|:---|:---|
| 时间锚 | created/modified/accessed | 什么时候来 |
| 内容锚 | title/keywords/summary/signature | 讲什么 |
| 关系锚 | references/referenced_by/version_chain | 和谁有关 |
| 行为锚 | access_count/weight | 被谁用·用多勤 |
| 上下文锚 | common_with/triggered_by | 什么情境被打开 |

### 锚点检索矩阵

| 想找什么 | 锚点路径 | 检索方式 | 引擎 |
|:---|:---|:---|:---|
| 昨天看过的 | 时间锚→过滤→按权重排序 | 无意识索引 | implicit |
| 关于"索引"的 | 内容锚→语义匹配→聚合 | 自然语言 | vector |
| 和"快速检索"有关 | 关系锚→引用链追溯 | 关联感知 | anchor |
| 和Kimi一起看的 | 行为锚→协作过滤→推荐 | 协同涌现 | collective |
| 写文档时打开的 | 上下文锚→情境匹配→联想 | 主动感知 | context |

## 🚀 三、实施路线图（已执行）

| 阶段 | 任务 | 交付物 | 状态 |
|:---|:---|:---|:---|
| P0 | 多维锚点数据结构+存储 | `bin/lh_anchor_model.py` | ✅ |
| P0 | 主动感知引擎 | `bin/lh_context_engine.py` | ✅ |
| P1 | 向量索引层（2-gram轻量） | `bin/lh_vector_index.py` | ✅ |
| P1 | 动态加权引擎 | `bin/lh_behavior_learner.py` | ✅ |
| P2 | 协同涌现层 | `bin/lh_collective_intel.py` | ✅ |
| P2 | 无意识检索 | `bin/lh_implicit_retrieval.py` | ✅ |
| P3 | 全量集成+`lh` 命令 | `lh idx` 命令族 | ✅ |

## 📦 交付物清单

| 文件 | 类型 | 说明 |
|:---|:---|:---|
| `bin/lh_anchor_model.py` | 数据模型 | 六类锚点·JSON存储·读写 |
| `bin/lh_context_engine.py` | 主动感知 | 当前文件/命令/对话上下文捕获 |
| `bin/lh_vector_index.py` | 向量索引 | 2-gram签名·余弦相似度·无三方依赖 |
| `bin/lh_behavior_learner.py` | 动态加权 | 访问加权·时间衰减·热冷数据 |
| `bin/lh_collective_intel.py` | 协同涌现 | 用户共现矩阵·协同推荐 |
| `bin/lh_implicit_retrieval.py` | 无意识检索 | 上下文驱动自动推送 |
| `bin/lh_index_pipeline.py` | 集成入口 | 一键全量索引+检索CLI |

## 🚀 执行命令

```bash
# 统一入口（已注册 lh 命令）
lh idx                    # 状态总览
lh idx build              # 全量构建索引
lh idx search "快速索引"  # 自然语言搜索
lh idx touch <file_id>    # 记录访问（动态演化）
lh idx suggest --context "写文档"  # 无意识推送
lh idx rank               # 热榜

# 直接调用
python3 bin/lh_index_pipeline.py build
python3 bin/lh_index_pipeline.py search "快速索引"
python3 bin/lh_index_pipeline.py suggest --context "写文档"
python3 bin/lh_index_pipeline.py touch F-20260816-001 --user UID9622

# 单引擎
python3 bin/lh_anchor_model.py init | add <path> | search <词>
python3 bin/lh_context_engine.py capture <path> | context
python3 bin/lh_vector_index.py index <path> | search <词>
python3 bin/lh_behavior_learner.py learn <fid> | rank | decay
python3 bin/lh_collective_intel.py record <fid> | recommend <user>
python3 bin/lh_implicit_retrieval.py suggest --context <词>
```

## ✅ 验收清单

- [x] 六引擎文件已创建到 `bin/`
- [x] `lh idx` 命令可运行
- [x] 自测通过（build/search/touch/suggest 闭环）
- [x] GPG 签名完成
- [x] 三色审计 🟢

## 📋 ROOT_CARD

【ROOT_CARD｜数学根审计】
Root: dr=8（2+0+2+6+0+8+1+6=25→2+5=7→7+1=8）
Wuxing: 木
TriColor: 🟢
Type: engineering
DNA: #龍芯⚡️丙午·丙申·壬戌·申时·䷖剥-INDEX-PHILOSOPHY-V2-ENGINEERED-UID9622

## 🔐 签章

**DNA：** #龍芯⚡️丙午·丙申·壬戌·申时·䷖剥-INDEX-PHILOSOPHY-V2-ENGINEERED-UID9622
**CONFIRM：** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**GPG：** A2D0092CEE2E5BA87035600924C3704A8CC26D5F
**审计：** P05 🟢 / P15 🟢
**三色：** 🟢 绿色（六引擎自测通过·可部署）

---
DNA: #龍芯⚡️丙午·丙申·壬戌·申时·䷖剥-INDEX-PHILOSOPHY-V2-ENGINEERED-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（思想层）· 代码引擎层 MulanPSL v2

```json
{
  "dna": "#龍芯⚡️丙午·丙申·壬戌·申时·䷖剥-INDEX-PHILOSOPHY-V2-ENGINEERED-UID9622",
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
