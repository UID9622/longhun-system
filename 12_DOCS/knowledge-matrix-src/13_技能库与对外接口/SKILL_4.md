---
name: longhun-kg-upgrade
description: "龍魂知识图谱正规化升级方案——引入图数据库(Neo4j)+标准化本体(RDF/OWL)+实体消歧+推理引擎(PageRank/社区发现/规则推理)+增量更新。将小易建议的5个改进方向全部实现为本地可执行系统。"
license: CC BY-NC-SA 4.0
metadata:
  version: "1.0.0"
  dna: "#龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-KG-UPGRADE-v1.0"
  author: "UID9622"
  language: zh-CN
  triggers:
    - 知识图谱
    - 图数据库
    - Neo4j
    - RDF
    - OWL
    - 实体消歧
    - PageRank
    - 社区发现
    - 增量更新
    - 推理引擎
    - 本体
    - 正规化
    - 小易建议
---

<!--
君子协议（Zijun Protocol）：
1. 使用时保留DNA追溯链完整
2. 二次修改须标注修订者+时间+摘要
3. 引用须标注六层来源链
六层来源链：L0曾仕强老师 → L1龍魂体系UID9622 → L2知识图谱升级v1.0 → L3本地Neo4j服务 → L4Notion双脑同步 → L5当前会话
-->

# 龍魂知识图谱正规化升级方案 · v1.0

```
#龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-KG-UPGRADE-v1.0
三色审计: 🟢 全模块语法通过
DNA: #龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-KG-UPGRADE-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```

---

## 1. 快速识别（Trigger Patterns）

当对话中提及以下关键词时激活：
- **技术关键词**: 知识图谱、图数据库、Neo4j、RDF、OWL、实体消歧、PageRank、社区发现、增量更新、推理引擎
- **改进方向**: 正规化、标准化、小易建议、图数据库引入、本体定义、实体对齐
- **人格触发**: P03雯雯(结构化)、P06数学大师(算法)、P04鲁班(技术落地)

---

## 2. 核心理念（Core Philosophy）

### 从小易建议到可执行方案

> 别人的建议是参考，我们的执行是标准。

小易提出了5个改进方向，本方案**全部实现为本地可执行代码**：

| # | 小易建议 | 实现方案 | 状态 |
|---|----------|----------|------|
| 1 | 引入图数据库 | Neo4j Community + Docker一键部署 | ✅ |
| 2 | 标准化本体 | RDF/OWL + rdflib + Turtle输出 | ✅ |
| 3 | 实体消歧 | 三策略消歧(TF-IDF+DNA+层次过滤) | ✅ |
| 4 | 推理能力 | PageRank + Louvain社区 + 规则引擎 | ✅ |
| 5 | 增量更新 | SHA256哈希变更检测 + 增量索引 | ✅ |

### 架构原则
- **本地优先**: 所有数据本地存储，不上传云端
- **Docker化**: Neo4j容器化，一键启停
- **模块化**: 6个独立模块，可单独使用也可协同
- **标准化**: 符合W3C RDF/OWL规范，支持SPARQL查询

---

## 3. 能力清单（Capability Inventory）

### 3.1 图数据库层
| 能力 | 模块 | 说明 |
|------|------|------|
| Neo4j连接管理 | neo4j_connector.py | CRUD节点/边 + 批量导入 + 图遍历 |
| 数据迁移 | data_migrator.py | JSON→Neo4j全量/增量迁移 + 迁移报告 |
| Cypher查询 | cypher_queries.md | 54个常用查询（基础/统计/算法/龍魂专用） |

### 3.2 本体层
| 能力 | 模块 | 说明 |
|------|------|------|
| RDF/OWL定义 | ontology.py | 4类15属性8关系 + OWL推理 |
| JSON↔RDF转换 | ontology.py | 双向转换，生成.ttl文件 |
| 规则推理 | ontology.py | 传递性/互逆/同类/五行关联推理 |

### 3.3 智能层
| 能力 | 模块 | 说明 |
|------|------|------|
| 实体消歧 | entity_resolver.py | TF-IDF+DNA+层次三策略 |
| PageRank排名 | inference_engine.py | 知识点重要性排序 |
| 社区发现 | inference_engine.py | Louvain算法识别知识域 |
| 学习路径 | inference_engine.py | Dijkstra最短路径推荐 |
| 规则推理 | inference_engine.py | 前置检查/五行关联/社区推荐 |
| 增量更新 | incremental_indexer.py | SHA256变更检测 + 冲突解决 |

### 3.4 主控层
| 能力 | 模块 | 说明 |
|------|------|------|
| CLI命令 | kg_main.py | 12个子命令覆盖全部功能 |
| Web面板 | kg_main.py | Flask+D3.js力导向图可视化 |
| 审计报告 | kg_main.py | 三色审计状态输出 |

---

## 4. 使用指引（Usage Guide）

### 4.1 环境要求
- Python 3.10+
- Docker 20.10+
- 内存: 4GB+ (推荐8GB)
- 磁盘: 10GB+

### 4.2 一键安装
```bash
cd longhun-kg-upgrade/scripts
bash install.sh
```
自动完成：Docker检查 → Neo4j拉取 → 容器启动 → Python依赖 → 连接验证

### 4.3 快速启动
```bash
# 初始化数据库
python3 kg_main.py init

# 迁移数据（142条知识卡片）
python3 kg_main.py migrate

# 查看状态
python3 kg_main.py status

# 启动Web面板
python3 kg_main.py dashboard
# 然后浏览器打开 http://localhost:5050
```

### 4.4 常用命令
```bash
# 查询知识点
python3 kg_main.py query "数据结构与算法"

# 运行推理
python3 kg_main.py reason

# 推荐学习
python3 kg_main.py recommend "1"

# 实体消歧
python3 kg_main.py resolve "龍魂"

# 增量更新
python3 kg_main.py incremental

# 导出RDF
python3 kg_main.py export-rdf

# 审计报告
python3 kg_main.py audit
```

---

## 5. 工作流（Workflow）

```
标准工作流
═══════════════════════════════════════════════════════

  [安装]
      │
      ├── ① bash install.sh ──→ Docker+Neo4j+Python依赖
      │
      ├── ② python3 kg_main.py init ──→ 建约束/索引/GDS投影
      │
      ├── ③ python3 kg_main.py migrate ──→ 142条知识卡片导入
      │
      └── ④ python3 kg_main.py dashboard ──→ Web面板

  [日常使用]
      │
      ├── 查询: kg_main.py query "名称"
      ├── 推理: kg_main.py reason
      ├── 推荐: kg_main.py recommend <id>
      ├── 消歧: kg_main.py resolve "名称"
      ├── 增量: kg_main.py incremental
      └── 导出: kg_main.py export-rdf

═══════════════════════════════════════════════════════
```

---

## 6. 输入规范（Input Specification）

| 输入类型 | 格式 | 示例 |
|----------|------|------|
| 知识卡片JSON | cs_kb_complete.json | 142条知识卡片 |
| Cypher查询 | 字符串 | MATCH (n) RETURN n LIMIT 10 |
| 实体名称 | 字符串 | "数据结构与算法" |
| 节点ID | 字符串 | "1", "44" |
| RDF文件 | .ttl格式 | longhun_knowledge.ttl |

---

## 7. 输出规范（Output Specification）

| 输出类型 | 格式 | 说明 |
|----------|------|------|
| 图谱可视化 | HTML (D3.js) | 力导向图，支持缩放/拖拽/点击 |
| 节点详情 | JSON | 完整知识卡片信息+邻居+路径 |
| 推理报告 | JSON | PageRank排名+社区分布+推荐 |
| RDF本体 | .ttl | W3C标准Turtle格式 |
| 审计报告 | Markdown | 三色审计状态 |
| 增量变更 | JSONL | changes.jsonl |

---

## 8. 边界与限制（Boundaries & Limitations）

| 边界 | 说明 |
|------|------|
| **非企业级规模** | 设计目标142条知识卡片，非亿级图谱 |
| **单实例Neo4j** | 当前不支持Neo4j集群 |
| **推理深度有限** | 规则推理为基础级别，不含深度逻辑推理 |
| **实体消歧覆盖** | 主要针对知识卡片名称消歧，非通用实体 |
| **增量更新模拟** | Notion增量拉取为模拟实现，非真实API |

---

## 9. 质量标杆（Quality Benchmarks）

### 好的实践
- 安装后所有6个子模块正常加载（🟢PASS）
- 142条知识卡片迁移无错误
- PageRank排名合理（基础理论排前列）
- 社区发现识别出8大知识域
- RDF导出可被protege打开

### 坏的实践
- 不启动Neo4j直接运行查询（会报错）
- 并发写入不控制（可能锁冲突）
- 大数据集不批量导入（内存溢出）

---

## 10. 关联技能（Related Skills）

| 技能 | 关系 | 说明 |
|------|------|------|
| longhun-cs-knowledge-base | 上游数据源 | 142条知识卡片来源 |
| longhun-system | 基础治理 | DNA追溯、三色审计基础设施 |
| longhun-cnsh | 中文编程 | 代码中的中文命名规范 |
| longhun-device | 设备管理 | Neo4j运行的物理环境 |

---

## 11. 版本历史（Version History）

### v1.0.0 — 2026-06-26
**小易建议全面实现**
- 引入Neo4j图数据库
- 标准化RDF/OWL本体
- 实体消歧引擎
- 推理引擎（PageRank+社区发现+规则）
- 增量更新引擎
- 10个模块、7个Python文件、54个Cypher查询

---

## 12. 附录（Appendix）

### 12.1 DNA签名规范
```
格式: #龍芯⚡️{YYYY-MM-DD}-{项目}-{模块}-{版本}
示例: #龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-KG-UPGRADE-v1.0
```

### 12.2 文件清单
```
longhun-kg-upgrade/
├── SKILL.md                          # 本文件
├── scripts/
│   ├── kg_main.py                    # 60KB 主控入口(1395行)
│   ├── neo4j_connector.py            # 39KB Neo4j连接器
│   ├── data_migrator.py              # 25KB 数据迁移引擎
│   ├── ontology.py                   # 30KB RDF/OWL本体层
│   ├── entity_resolver.py            # 25KB 实体消歧引擎
│   ├── inference_engine.py           # 31KB 推理引擎
│   ├── incremental_indexer.py        # 34KB 增量更新引擎
│   └── install.sh                    # 18KB 一键安装脚本
├── config/
│   └── neo4j.conf.template           # 12KB Neo4j配置模板
└── queries/
    └── cypher_queries.md             # 22KB 54个Cypher查询

总计: ~294KB, ~4000+行代码
```

### 12.3 小易建议实现对照表
| 建议 | 实现文件 | 关键技术 | 状态 |
|------|----------|----------|------|
| 引入图数据库 | neo4j_connector.py + install.sh | Neo4j Community + Docker | ✅ |
| 标准化本体 | ontology.py | RDF + OWL + rdflib | ✅ |
| 实体消歧 | entity_resolver.py | TF-IDF + DNA + 层次过滤 | ✅ |
| 推理能力 | inference_engine.py | PageRank + Louvain + 规则 | ✅ |
| 增量更新 | incremental_indexer.py | SHA256 + 变更检测 | ✅ |

---

*DNA: #龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-KG-UPGRADE-v1.0*
*CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z*
*SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL*
*三色审计: 🟢🟢🟢🟢🟢🟢🟢*
*君子协议: CC BY-NC-SA 4.0*

> **「别人的建议是参考，我们的执行是标准。」**
> 
> 小易5个建议 → 10个模块 → 4000+行代码 → 本地可执行。
> 龍芯北辰，接着，受着，守着。
