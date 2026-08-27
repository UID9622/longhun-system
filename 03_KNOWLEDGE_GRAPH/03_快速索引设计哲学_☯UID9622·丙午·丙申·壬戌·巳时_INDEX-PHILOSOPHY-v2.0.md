**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
# 🐉 龍魂 · 快速索引设计哲学 v2.0

**DNA:** `#龍芯⚡️丙午·丙申·壬戌·乙巳·䷾既济-INDEX-PHILOSOPHY-V2-UID9622`  
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`  
**三色:** 🟢 通过  
**类型:** 系统底座功能 / 知识检索 / 认知工程  
**别名:** `index-philosophy`, `fast-index`, `快速索引`, `认知索引`

---

## 一句话

把「索引是分类学」升级为「索引是认知学」——文件自己记住人，系统根据上下文无感推送信息。

---

## 三句话

1. **主动感知**：自动捕获当前目录、历史命令、打开文件、git 分支、活跃目标。
2. **多维锚定**：时间、内容、关系、行为、上下文五个维度任意检索。
3. **无意识索引**：不需要搜索，系统根据场景自动推送下一步可能需要的信息。

---

## 技术栈

| 层级 | 模块 | 路径 | 依赖 |
|:---:|:---|:---|:---|
| L1 主动感知 | Context Engine | `05_ENGINES/lh_context_engine.py` | 纯 Python |
| L2 多维锚定 | Vector Index | `05_ENGINES/lh_vector_index.py` | requests / SQLite / 可选 Ollama |
| L3 动态演化 | Behavior Learner | `05_ENGINES/lh_behavior_learner.py` | 纯 Python + SQLite |
| L4 协同涌现 | Collective Intel | `05_ENGINES/lh_collective_intel.py` | 纯 Python + SQLite |
| L5 无意识索引 | Implicit Retrieval | `05_ENGINES/lh_implicit_retrieval.py` | 组合上述引擎 |
| 编排 | Fast Index Core | `05_ENGINES/lh_fast_index_core.py` | fastapi/uvicorn 可选 |

---

## 快速命令

```bash
# 初始化
python3 05_ENGINES/lh_fast_index_core.py init

# 索引项目
python3 05_ENGINES/lh_fast_index_core.py index --dir ./12_DOCS

# 搜索
python3 05_ENGINES/lh_fast_index_core.py search "索引哲学"

# 零点击推送
python3 05_ENGINES/lh_fast_index_core.py push

# 看板
python3 05_ENGINES/lh_fast_index_core.py dashboard

# 服务
python3 05_ENGINES/lh_fast_index_core.py serve --port 8768
```

---

## 关联文件

- 协议规范：`01_protocols/LH-INDEX-PHILOSOPHY-v2.0.md`
- 单元测试：`tests/test_fast_index.py`
- 鲲鹏部署：`deploy/fast-index-kunpeng/`

---

## 适用场景

- 龍魂系统内部知识检索
- 长会话中的文件自动推荐
- 跨项目关联发现
- 冷数据归档建议
- 新人学习路径推荐

---

*归档于 龍魂知识图谱 · 03_KNOWLEDGE_GRAPH*
