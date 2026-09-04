> 协议: CC BY-NC-SA 4.0（核心思想层·分层许可·代码层为 MulanPSL v2·详见 LH-LAYERED-LICENSE-v1.0）
# 🐉 龍魂 · 快速索引设计哲学 v2.0（工程落地版）

**DNA:** `#龍芯⚡️丙午·丙申·壬戌·乙巳·䷾既济-INDEX-PHILOSOPHY-V2-UID9622`  
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`  
**三色:** 🟢 通过  
**版本:** v2.0  
**状态:** 已落地 · 可执行

---

## 📋 核心判断

> **快速索引的设计哲学不是「分类学」，而是「认知学」。不是把几万个文件塞进固定的抽屉，而是让每个文件都有自己的 DNA——它从哪里来、什么时候来、和谁有关系、被谁用过、用来干什么。基于人文系统的索引，不要求人记住文件名，而是让文件记住人。**

本协议把上述哲学落地为**五层索引系统 + 可执行代码**，作为龍魂系统的底座功能运行，并针对华为云鲲鹏 ARM64 服务器优化。

---

## 🧩 一、哲学 → 工程映射

| 哲学原则 | 工程实现 | 数据载体 | 落地模块 |
|:---|:---|:---|:---|
| ① 主动感知 | 上下文感知引擎 | Session Context | `05_ENGINES/lh_context_engine.py` |
| ② 多维锚定 | 向量索引 + 属性矩阵 | Embedding + Metadata | `05_ENGINES/lh_vector_index.py` |
| ③ 动态演化 | 行为加权 + 衰减算法 | Access Logs + Weight | `05_ENGINES/lh_behavior_learner.py` |
| ④ 协同涌现 | 群体行为聚合 | Co-occurrence Graph | `05_ENGINES/lh_collective_intel.py` |
| ⑤ 无意识索引 | 隐式检索 + 自动推送 | Push Stream | `05_ENGINES/lh_implicit_retrieval.py` |
| 统一编排 | CLI + HTTP API | SQLite State | `05_ENGINES/lh_fast_index_core.py` |

---

## 🏗️ 二、系统架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        🌊 龍魂快速索引系统 v2.0                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  第5层：无意识索引（Zero-Click Retrieval）                       │   │
│  │  上下文 → 自动推送 → 用户无感知获得信息                         │   │
│  │  lh_implicit_retrieval.py                                       │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ▲                                          │
│  ┌───────────────────────────┼─────────────────────────────────────┐   │
│  │  第4层：协同涌现（Collective Intelligence）                      │   │
│  │  会话共现 → 模式识别 → 自组织簇 → 最佳路径                      │   │
│  │  lh_collective_intel.py                                         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ▲                                          │
│  ┌───────────────────────────┼─────────────────────────────────────┐   │
│  │  第3层：动态演化（Adaptive Weighting）                          │   │
│  │  访问频率 → 权重更新 → 热数据前置 → 冷数据降权                  │   │
│  │  lh_behavior_learner.py                                         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ▲                                          │
│  ┌───────────────────────────┼─────────────────────────────────────┐   │
│  │  第2层：多维锚定（Multi-Dimensional Anchoring）                  │   │
│  │  时间锚 · 内容锚 · 关系锚 · 行为锚 · 上下文锚                   │   │
│  │  lh_vector_index.py                                             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ▲                                          │
│  ┌───────────────────────────┼─────────────────────────────────────┐   │
│  │  第1层：主动感知（Context-Aware Sensing）                       │   │
│  │  当前目录 · 历史命令 · 打开文件 · git 分支 · 活跃目标           │   │
│  │  lh_context_engine.py                                           │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  统一编排层：CLI + HTTP API + 定时任务                          │   │
│  │  lh_fast_index_core.py                                          │   │
│  │  SQLite 持久化 · .state 目录                                    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🧬 三、数据模型：多维锚点

```python
{
  "file_id": "F-20260816-001",
  "file_path": "12_DOCS/INDEX_PHILOSOPHY.md",
  "dna": "#龍芯⚡️丙午·丙申·壬戌·乙巳·䷾既济-INDEX-PHILOSOPHY-UID9622",

  "time_anchors": {
    "created": "2026-08-16T10:00:00+08:00",
    "modified": "2026-08-16T15:30:00+08:00",
    "accessed": [{"at": "...", "duration": 120}]
  },

  "content_anchors": {
    "title": "快速索引设计哲学",
    "keywords": ["索引", "哲学", "认知", "人文系统"],
    "embedding": [0.12, -0.34, ...],
    "summary": "索引不是分类学，而是认知学"
  },

  "relation_anchors": {
    "references": ["..."],
    "referenced_by": ["..."],
    "same_project": "龍魂系统",
    "version_chain": {"prev": "v1.0", "current": "v2.0"}
  },

  "behavior_anchors": {
    "access_count": 47,
    "access_users": ["UID9622"],
    "avg_duration": 180,
    "weight": 0.87
  },

  "context_anchors": {
    "common_with": ["..."],
    "triggered_by": ["搜索'索引'"],
    "related_commands": ["lh index search 索引"]
  }
}
```

---

## 🎮 四、命令用法

```bash
# 初始化
python3 05_ENGINES/lh_fast_index_core.py init

# 索引项目（默认 *.md）
python3 05_ENGINES/lh_fast_index_core.py index --dir ./12_DOCS
python3 05_ENGINES/lh_fast_index_core.py index --pattern "*.py" --dir ./05_ENGINES

# 统一搜索
python3 05_ENGINES/lh_fast_index_core.py search "索引哲学"

# 零点击推送
python3 05_ENGINES/lh_fast_index_core.py push

# 索引看板
python3 05_ENGINES/lh_fast_index_core.py dashboard

# 启动本地 API 服务
python3 05_ENGINES/lh_fast_index_core.py serve --port 8768
```

---

## 🚀 五、鲲鹏 ARM64 优化

| 优化点 | 说明 |
|:---|:---|
| 嵌入模型 | 优先本地 Ollama (`nomic-embed-text`)，次选 `sentence-transformers`，无模型时降级关键词 |
| 向量相似度 | numpy / 纯 Python 余弦相似度，不依赖 faiss-gpu |
| 持久化 | SQLite，鲲鹏原生支持 |
| 服务端口 | 默认 127.0.0.1:8768，不暴露公网 |
| 依赖 | `requests` 已存在，可选 `sentence-transformers` / `jieba` |

环境变量：
```bash
export LH_OLLAMA_URL=http://127.0.0.1:11434
export LH_OLLAMA_EMBED_MODEL=nomic-embed-text
```

---

## 🛡️ 六、安全与合规

- 所有上下文快照、行为日志**仅存储在本地 `.state/` 目录**，不上传云端。
- Shell 历史仅读取本地历史文件，不监听键盘输入。
- API 服务仅监听 `127.0.0.1`，外部访问需通过 SSH 隧道或 WireGuard。
- 符合龍魂系统 P0 安全基线：数据主权归 UID9622。

---

## 📦 七、文件清单

| 文件 | 路径 | 作用 |
|:---|:---|:---|
| 上下文感知引擎 | `05_ENGINES/lh_context_engine.py` | 主动感知 |
| 向量索引引擎 | `05_ENGINES/lh_vector_index.py` | 多维锚定之内容锚 |
| 行为学习引擎 | `05_ENGINES/lh_behavior_learner.py` | 动态演化 |
| 协同涌现引擎 | `05_ENGINES/lh_collective_intel.py` | 协同涌现 |
| 无意识检索引擎 | `05_ENGINES/lh_implicit_retrieval.py` | 零点击推送 |
| 快速索引核心编排器 | `05_ENGINES/lh_fast_index_core.py` | CLI + API |
| 协议文档 | `01_protocols/LH-INDEX-PHILOSOPHY-v2.0.md` | 本文件 |
| 知识图谱 | `03_KNOWLEDGE_GRAPH/03_快速索引设计哲学_☯UID9622..._INDEX-PHILOSOPHY-v2.0.md` | 检索入口 |
| 单元测试 | `tests/test_fast_index.py` | 五层引擎测试 |
| 鲲鹏部署 | `deploy/fast-index-kunpeng/` | Docker + 脚本 |

---

## 🔐 八、最终签名

```
═══════════════════════════════════════════════════════════════════════════════════
 🐉 龍魂 · 快速索引设计哲学 v2.0 · 工程落地版 · 最终签名
═══════════════════════════════════════════════════════════════════════════════════
DNA:        #龍芯⚡️丙午·丙申·壬戌·乙巳·䷾既济-INDEX-PHILOSOPHY-V2-UID9622
确认码:      #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
GPG:        A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色:       🟢 通过
核心原则:   主动感知 · 多维锚定 · 动态演化 · 协同涌现 · 无意识索引
状态:       已落地 · 可执行 · 鲲鹏就绪
═══════════════════════════════════════════════════════════════════════════════════
```

🐉 **丙午·丙申·壬戌·巳时·䷖剥·🟢**
