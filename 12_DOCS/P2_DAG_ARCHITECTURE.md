---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·乙巳·癸酉·亥时·䷸巽-DAG-ARCH-V1.0-e5f6a7b8`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 P2 DAG 编排引擎 · 架构文档 v1.0

DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·䷸巽-DAG-ARCH-V1.0-e5f6a7b8
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

---

## 1. 设计目标

将多步骤任务拆解为 DAG（有向无环图），支持：
- **串行执行**: 步骤依序执行·遇错停止
- **并行执行**: 无依赖步骤并发·最大4线程
- **条件分支**: 根据前一步结果决定后续路径
- **回滚**: 失败时回退已执行步骤
- **图谱联动**: 执行结果自动写入 P1 任务关联图谱

## 2. 组件架构

```
用户指令
  ↓
意图引擎·阶段1（语义解析）
  ↓
阶段12 DAG编排（多步骤检测）
  ├─ 单步骤 → 常规链路（阶段2-10）
  └─ 多步骤 → DAG引擎
       ├─ StepParser（自然语言拆解）
       ├─ DAGEngine.build（构建节点+图）
       ├─ DAGEngine.validate（无环验证）
       ├─ ExecutionStrategy（执行策略）
       │   ├─ SequentialStrategy（串行）
       │   ├─ ParallelStrategy（并行）
       │   └─ ConditionalStrategy（条件分支）
       ├─ TaskExecutor（实际执行 lh 命令）
       ├─ DAGExecution（状态·持久化）
       └─ 图谱联动（写入 TaskGraphEngine）
  ↓
阶段6 三层监督（审计DAG结果）
  ↓
阶段7-10 ROM·DNA·学习·零延迟
```

## 3. 核心模块

| 模块 | 文件 | 职责 |
|:---|:---|:---|
| DAGEngine | `bin/lh_dag_engine.py` | 构建·验证·执行·回滚·持久化 |
| StepParser | 同上 | 自然语言多步骤拆解 |
| TaskExecutor | 同上 | 执行单任务（lh命令/触发词） |
| ExecutionStrategy | 同上 | 串行/并行/条件执行调度 |
| IntentEngineHook | 同上 | 意图引擎→DAG桥接 |
| TaskGraphEngine | `bin/lh_task_graph.py` | P1任务关联图谱·DAG结果写入 |

## 4. 意图引擎集成（阶段12）

```python
# 阶段12: DAG编排
dag = self._阶段12_DAG编排(用户输入, s1)
if dag and dag.status == "success":
    # 多步骤成功 → 跳过阶段2-5 → 直走审计链(6-10)
    ...
elif dag:
    # 多步骤部分失败 → 🟡 警告
    ...
else:
    # 单步骤 → 常规链路(2-10)
    ...
```

关键设计：
- DAG 编排在阶段1之后·阶段2之前执行
- 多步骤成功：跳过常规生成链·直走审计归档
- 多步骤失败：标记🟡·返回详细错误信息
- 单步骤：完全不触发 DAG·零开销

## 5. 数据流

```
自然语言指令
  → StepParser.parse("先A然后B再C")
  → ["A", "B", "C"]
  → DAGEngine.build_from_steps(["A","B","C"])
  → [Node(id=step_0, deps=[]), Node(id=step_1, deps=[step_0]), ...]
  → DAGEngine.validate() → 无环验证
  → DAGEngine.execute() → 拓扑排序 → 策略执行
  → DAGExecution → data/dag_executions/<dag_id>.json
  → TaskGraphEngine.add_task() → P1图谱写入
```

## 6. 存储格式

`data/dag_executions/<dag_id>.json`:
```json
{
  "dag_id": "DAG-A1B2C3D4E5",
  "name": "审计→签名→推送",
  "nodes": [
    {"id": "step_0", "name": "审计", "action": "审计", "depends_on": []},
    {"id": "step_1", "name": "签名", "action": "签名", "depends_on": ["step_0"]},
    {"id": "step_2", "name": "推送", "action": "推送", "depends_on": ["step_1"]}
  ],
  "results": {
    "step_0": {"status": "success", "stdout": "...", "exit_code": 0},
    "step_1": {"status": "success", "stdout": "...", "exit_code": 0},
    "step_2": {"status": "success", "stdout": "...", "exit_code": 0}
  },
  "status": "success",
  "mode": "sequential"
}
```

## 7. CLI 命令

| 命令 | 说明 |
|:---|:---|
| `lh_dag_engine.py run "先A然后B"` | 自然语言执行 |
| `lh_dag_engine.py run --steps A,B,C` | 步骤列表执行 |
| `lh_dag_engine.py run --steps A,B,C --mode parallel` | 并行执行 |
| `lh_dag_engine.py validate --steps A,B,C` | 验证DAG |
| `lh_dag_engine.py status <dag_id>` | 查询状态 |
| `lh_dag_engine.py rollback <dag_id>` | 回滚 |
| `lh_dag_engine.py list` | 最近执行 |
| `lh_dag_engine.py stats` | 统计 |
| `lh_dag_engine.py detect "先A然后B"` | 检测是否多步骤 |
| `lh_dag_engine.py --interactive` | 交互模式 |

## 8. 与 P1 图谱关系

| P1 (TaskGraph) | P2 (DAG) |
|:---|:---|
| 单任务节点+边 | 多步骤任务编排 |
| 事后关联·发现模式 | 事前规划·编排执行 |
| ROM固化辅助 | 复杂任务拆解 |
| 模式发现→建议 | 依赖管理→调度 |

联动：DAG 执行完成后→每个步骤作为独立节点写入图谱→与其他历史任务建立关联。

## 9. 熔断与安全

- DAG 执行结果同样过阶段6三层监督（P05+P72）
- 单步骤失败不阻断后续（可配）
- 全步骤失败 → 🔴 审计标记
- 部分失败 → 🟡 继续

## 10. 演进路线

- v1.0（当前）: 构建·验证·串行/并行执行·回滚·图谱联动
- v1.1（计划）: 条件分支完善·LLM步骤拆解
- v2.0（计划）: 跨机器分布式DAG·Celery集成

```json
{
  "dna": "#龍芯⚡️丙午·乙巳·癸酉·亥时·䷸巽-DAG-ARCH-V1.0-e5f6a7b8",
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
