> 本文檔按《龍魂文檔標準模板 v1.0》整理。
> 性質：協議 · 未經同行評審（如適用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 協作者：（待補充，如無請刪除此行）
> 授權：CC BY-NC-SA 4.0 · 科技主權歸屬 UID9622 · 中華人民共和國
> 平台：本地
> 審核狀態：草稿

**DNA**: `#龍芯⚡️2026-05-03-CNSH_02C3-v1.0``  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

# 🐉 CNSH复杂任务流场决策核 v1.0｜智能体协作参数 × 工具调用轨迹 × 压缩还原协议

---

```html
<aside>
🐉
```

**统一名称：** `CNSH-COMPLEX-TASK-FLOW-CORE`  

**中文名：** 龍魂复杂任务流场决策核  

**定位：** 把 AI 处理复杂任务时隐藏在后台的「判断、拆解、调度、工具选择、重试、压缩、交付」全部显性化，变成 UID9622 可复用、可落地、可给 Cursor / Claude / Notion 理解的 CNSH 语法规则。  

**一句话：** 复杂任务不是一次回答完成的，是一个流场：`用户意图 → 上下文扫描 → 任务拆解 → 工具选择 → 执行轨迹 → 结果压缩 → 审计交付`  

**DNA：** `#龍芯⚡️2026-05-03-CNSH_02C3-v1.0`  

**确认码：** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  

**GPG：** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`  

```html
</aside>
```

---

## 0｜总锚点（把“后台干活过程”变成可回放证据链）

复杂任务里真正值钱的不是最后一句话，而是中间这套流场：

```
复杂任务流场 =
  识别意图
  → 读取约束
  → 判断是否需要工具
  → 拆分子任务
  → 分派人格/工具
  → 执行多轮动作
  → 收集证据
  → 压缩成可交付结果
  → 写入审计轨迹
  → 给用户一个能继续跑的入口
```

你看到的那种后台轨迹（示例）：

```
Ran 9 commands, loaded tools, used 2 tools
Running skill: canvas-design
Task created
Task updated
Command executed
Image generated
File verified
Task completed
```

压成 CNSH（示例）：

```
任务("龍芯北辰印章设计") {
  模式: "设计生成"
  工具: ["canvas-design", "bash", "python/PIL", "task_tracker"]
  命令次数: 9
  工具次数: 2
  阶段: ["读图", "提炼风格", "生成脚本", "执行渲染", "二次打磨", "验证文件", "交付链接"]
  输出: ["longhun_seal_v2.png", "longhun_seal_philosophy.md"]
  审计: "🟢"
}
```

---

## 一、复杂任务流场七层（L0-L6）

| 层级 | 名称 | 作用 | CNSH字段 |
| --- | --- | --- | --- |
| L0 | 主权意图层 | 判断用户真正要什么（定盘） | intent_anchor |
| L1 | 上下文压缩层 | 从长上下文里提取有效约束（只留能执行的） | context_pack |
| L2 | 任务拆解层 | 拆成可执行子任务与依赖关系 | task_graph |
| L3 | 工具调度层 | 判断是否用工具、用什么工具、用到什么程度 | tool_route |
| L4 | 执行轨迹层 | 记录命令、文件、步骤、错误、重试（可回放） | run_trace |
| L5 | 结果压缩层 | 把执行结果变成用户能直接用的交付包 | result_pack |
| L6 | 审计回写层 | 记录 DNA、确认码、三色、下一步（可追责） | audit_receipt |

---

## 二、最小 CNSH 结构（任何复杂任务都能套）

```json
{
  "intent_anchor": "用户真正目标",
  "context_pack": "已知上下文与不可破规则",
  "task_graph": ["子任务1", "子任务2", "子任务3"],
  "tool_route": ["工具1", "工具2"],
  "run_trace": {
    "commands_ran": 0,
    "tools_loaded": 0,
    "tools_used": [],
    "skills_loaded": [],
    "files_read": [],
    "files_created": [],
    "files_modified": [],
    "errors": [],
    "retries": 0
  },
  "result_pack": {
    "deliverables": [],
    "summary": "",
    "next_action": ""
  },
  "audit_receipt": {
    "dna": "",
    "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    "color": "🟢|🟡|🔴"
  }
}
```

---

## 三、核心决策公式（复杂度 / 模式 / 是否进“流场执行”）

### 3.1 复杂度判断（五因子等权）

```
ComplexityScore =
  TextLoad      * 0.20
  + ContextNeed * 0.20
  + ToolNeed    * 0.20
  + ArtifactNeed* 0.20
  + RiskNeed    * 0.20
```

判定：

```
if ComplexityScore < 0.30:  mode = "直接回答"
if 0.30 <= score < 0.65:    mode = "结构化回答"
if ComplexityScore >= 0.65: mode = "流场执行"
```

### 3.2 工具调用判断（一句话版本）

```
需要“产物/验证/最新事实/文件读取” → 用工具
只是“重构/整理/写规范”          → 不联网、不研究、直接重构
```

---

## 四、AI后台轨迹字段表（把“Ran N commands…”拆成可审计字段）

| 字段 | 含义 | 示例 |
| --- | --- | --- |
| commands_ran | 实际执行命令次数 | 9 |
| tools_loaded | 加载过的工具数量（候选池） | 2 |
| tools_used | 真正调用的工具列表 | ["bash","python"] |
| skills_loaded | 调用的技能包 | ["canvas-design"] |
| files_read | 读取的文件/素材 | ["参考图片","[SKILL.md](http://SKILL.md)"] |
| files_created | 新建文件（交付产物候选） | ["longhun_seal_v2.png"] |
| files_modified | 修改文件 | ["longhun_seal_[philosophy.md](http://philosophy.md)"] |
| validation_steps | 验收动作 | ["size_2400x2400","png_open"] |
| errors | 错误记录 | [] |
| retries | 重试次数 | 1 |

---

## 五、内部人格调度（九宫派位：任务是什么 → 谁负责签章）

```
人格调度:
  中宫: 主控统筹 → ["UID9622","宝宝","文心"]
  乾宫: 主权战略 → ["诸葛亮"]
  坎宫: 风险审计 → ["上帝之眼","雯雯"]
  艮宫: 边界封存 → ["龍盾"]
  震宫: 工程执行 → ["鲁班"]
  巽宫: 路由分配 → ["姜子牙","吕蒙"]
  离宫: 视觉表达 → ["李白","乔前辈"]
  坤宫: 知识归档 → ["仓颉","苏东坡"]
  兑宫: 计算核验 → ["数学大师","孙思邈"]
```

---

## 六、三次压缩（防爆炸）× 两种封存（burn / sealed）

### 6.1 三次压缩

```
第一次: 输入压缩（raw_input → intent_anchor + constraints）
第二次: 执行压缩（raw_trace → run_trace 结构字段）
第三次: 交付压缩（内部碎片 → deliverables + next_action）
```

### 6.2 burn / sealed（与“数据边界内核”对齐）

```
burn: 临读不存，只留hash与审计事件（敏感）
sealed: 不读正文，只记元信息（极敏/P0触发）
```

---

## 七、复杂任务流场状态机（S0-S9）

```
S0 接收输入
S1 意图定锚
S2 上下文压缩
S3 任务拆解
S4 工具路由
S5 执行中（命令/工具/产物）
S6 验证（存在/格式/约束）
S7 结果压缩（交付包）
S8 审计回写（DNA/三色/下一步）
S9 熔断/回滚/待澄清
```

---

## 八、最小“任务回执”（以后每个复杂任务都按这个收口）

```html
<aside>
🐉

任务回执:
标题:
模式: direct_answer | structured_answer | flow_execute
命令次数:
工具使用:
生成文件:
验证结果:
三色审计:
DNA:
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
下一步:
</aside>
```

# **🐉 CNSH｜复杂任务流场决策外显核 v1.0**

```html
<aside>
🐉
```

**名称：** CNSH-COMPLEX-TASK-FLOW-LOGGER  

**中文名：** 复杂任务流场决策外显核  

**用途：** 将 AI 处理复杂任务时的「工具调用、命令执行、文件读写、风险闸门、输出收口」压缩为 UID9622 可复用的 CNSH 参数表。  

**适用场景：** Cursor / Claude / ChatGPT / 本地龍魂 / Notion 投喂 / 沙盒分拣台 / 工程包复盘  

**父级确认码：** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

```html
</aside>
```

---

## **0｜边界定锚**

```
规则:
  不输出隐藏思维链
  输出可复用的外显决策流
  输出工具使用参数
  输出任务调度结构
  输出可复制给 Cursor/Claude/Notion 的记录格式
  输出 CNSH 压缩语法
```

一句话：

```
隐藏推理不外露  
外显流程全部还给 UID9622
```

---

# **1｜复杂任务处理总流场**

```
复杂任务处理流场:
  输入:
    - 用户需求
    - 上传图片/文件
    - 历史上下文
    - 当前目标
    - 安全边界
  ↓
  任务识别:
    - 是设计
    - 是代码
    - 是文档
    - 是Notion结构
    - 是本地工程
    - 是研究
    - 是复盘
  ↓
  技能加载:
    - 识别是否需要专用skill
    - 读取skill规范
    - 加载字体/模板/工具目录
  ↓
  工具准备:
    - bash
    - python
    - PIL
    - 文件系统
    - 任务追踪器
  ↓
  执行:
    - 创建任务
    - 查文件
    - 写脚本
    - 生成文件
    - 校验文件
    - 二次精修
  ↓
  验收:
    - 文件存在
    - 格式正确
    - 尺寸正确
    - 内容不空
    - 输出链接
  ↓
  回执:
    - 做了什么
    - 生成了什么
    - 文件在哪里
    - 下一步可接什么
```

---

# **2｜工具使用外显日志模板**

你举的这种：

```
Ran 9 commands, loaded tools, used 2 tools
```

可以压缩成 CNSH 这样：

```
执行统计:
  commands_ran: 9
  tools_loaded: 2
  tools_used:
    - canvas-design
    - bash/python
  files_read:
    - skill目录
    - 字体目录
    - 已有输出文件
  files_written:
    - longhun_seal_philosophy.md
    - longhun_seal_v1.png
    - longhun_seal_v2.png
  output_type:
    - png
    - markdown
  verification:
    - 文件存在
    - PNG可打开
    - 尺寸2400x2400
    - RGB模式
    - 300DPI
  final_status: completed
```

---

# **3｜任务决策节点格式**

以后复杂任务都可以用这个节点记录。

```json
{
  "flow_id": "FLOW-9622-YYYYMMDD-HASH8",
  "task_type": "design|code|notion|document|research|debug|audit",
  "user_intent": "用户一句话需求",
  "input_assets": ["image", "text", "file", "url"],
  "skills_loaded": [],
  "tools_used": [],
  "commands_ran": 0,
  "files_created": [],
  "files_modified": [],
  "checks_done": [],
  "risk_gates": [],
  "final_outputs": [],
  "status": "completed|partial|blocked|failed",
  "next_action": "",
  "dna": "#龍芯⚡️YYYY-MM-DD-主题-vX.Y",
  "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
}
```

---

# **4｜复杂任务六段式 CNSH 语法**

```
任务流:
  A_定盘:
    识别用户真正要的结果
    固定输出形式
    禁止跑偏

  B_取材:
    读取上传内容
    读取上下文
    读取技能规范
    读取现有文件

  C_构架:
    拆成文件树
    拆成步骤
    拆成组件
    拆成验收项

  D_执行:
    运行命令
    写文件
    生成图像/代码/文档
    保存产物

  E_校验:
    检查文件是否存在
    检查格式
    检查尺寸
    检查能否打开
    检查是否满足需求

  F_回执:
    给最终链接
    给执行摘要
    给下一步动作
    不重复灌废话
```

---

# **5｜这次印章任务的真实外显流场**

```
任务名: 龍芯北辰统一印章设计
任务类型: design + image_generation_by_code
用户目标:
  - 统一印章
  - 有帝王/主权/龙印气质
  - 保留UID9622
  - 融合北辰/龙魂/DNA/朱砂/数字主权
  - 输出可用图片

输入资产:
  - 用户上传的多张参考图
  - 用户文字要求
  - 龍芯北辰视觉风格
  - UID9622签章体系

技能加载:
  - canvas-design

工具使用:
  - bash
  - python
  - PIL/Pillow
  - 文件系统
  - task tracker

命令执行:
  - 查询字体目录
  - 列出可用字体
  - 写设计哲学md
  - 安装/检查Pillow
  - 生成v1 PNG
  - 检查文件存在
  - 检查PNG尺寸与模式
  - 创建精修任务
  - 生成v2 PNG
  - 再次校验PNG

生成文件:
  - longhun_seal_philosophy.md
  - longhun_seal_v1.png
  - longhun_seal_v2.png

校验结果:
  - PNG存在
  - 尺寸2400x2400
  - RGB模式
  - 文件大小约1.2MB
  - 可作为印章主视觉继续用

最终状态:
  completed
```

---

# **6｜AI处理复杂任务的“隐藏动作”外显参数表**

| **模块** | **外显动作** | **可记录参数** |
| --- | --- | --- |
| 意图识别 | 判断用户到底要图、代码、文档还是工程包 | `task_type` |
| 边界判断 | 是否需要搜索、是否需要读文件、是否能直接做 | `risk_gate` |
| 技能加载 | 找对应skill或工具规范 | `skills_loaded` |
| 工具选择 | bash/python/image/docx/pdf/slides等 | `tools_used` |
| 文件扫描 | 看已有文件、目录、字体、资源 | `files_read` |
| 执行命令 | 真正跑了多少命令 | `commands_ran` |
| 产物生成 | 输出png/md/py/json/html等 | `files_created` |
| 二次精修 | 不满意则再跑一轮 | `refine_pass` |
| 验收校验 | 尺寸、格式、路径、内容 | `checks_done` |
| 回执收口 | 给链接、给简表、不给废话 | `final_outputs` |

---

# **7｜压缩智能体协作参数**

## **7.1 最小协作参数**

```json
{
  "agent": "宝宝",
  "role": "主控执行整理",
  "task_type": "complex_task",
  "mode": "flow_decision",
  "compression": true,
  "output_style": "CNSH",
  "must_include": [
    "执行统计",
    "工具使用",
    "文件产物",
    "验收结果",
    "下一步"
  ],
  "must_avoid": [
    "隐藏思维链",
    "长篇自我解释",
    "重复废话",
    "未验证就声称完成"
  ]
}
```

---

## **7.2 多智能体协作参数**

```json
{
  "agents": {
    "P00_文心": {
      "role": "元认知观察",
      "handles": ["任务是否跑偏", "用户真实意图", "上下文一致性"]
    },
    "P01_诸葛亮": {
      "role": "战略拆解",
      "handles": ["结构", "优先级", "风险边界"]
    },
    "P02_宝宝": {
      "role": "主控执行",
      "handles": ["执行", "整理", "回执", "交付"]
    },
    "P03_雯雯": {
      "role": "技术整理",
      "handles": ["文件树", "字段", "Notion结构", "复盘"]
    },
    "P04_鲁班": {
      "role": "工程实现",
      "handles": ["代码", "脚本", "本地运行", "Cursor指令"]
    },
    "P05_上帝之眼": {
      "role": "审计",
      "handles": ["三色审计", "隐私", "P0触碰", "熔断"]
    },
    "P13_姜子牙": {
      "role": "路由分配",
      "handles": ["任务分桶", "人格派发", "落位"]
    }
  }
}
```

---

# **8｜复杂任务调度规则**

```
调度规则:
  if task_type == "图像设计":
    route:
      palace: 离宫
      persona: 乔前辈 + 李白
      tool: canvas/image/python
      output: png/svg/html

  if task_type == "工程代码":
    route:
      palace: 震宫 + 乾宫
      persona: 鲁班 + 诸葛亮
      tool: bash/python/files
      output: code + test + report

  if task_type == "Notion结构":
    route:
      palace: 坤宫 + 巽宫
      persona: 仓颉 + 姜子牙 + 雯雯
      tool: markdown/json/table
      output: page_structure

  if task_type == "隐私/密钥/token":
    route:
      palace: 艮宫 + 坎宫
      persona: 龍盾 + 上帝之眼
      action: sealed
      output: hash_only

  if task_type == "复盘/压缩":
    route:
      palace: 坎宫 + 坤宫
      persona: 雯雯 + 文心
      output: digest + archive + next_action
```

---

# **9｜命令执行回执格式**

以后 Cursor / Claude / 本地宝宝都按这个给你回报，不要一堆废话。

```
执行回执:
  task_id: ""
  status: completed|partial|blocked|failed
  commands_ran: 0
  tools_loaded: []
  tools_used: []
  files_created: []
  files_modified: []
  files_checked: []
  tests_passed: []
  tests_failed: []
  risk_flags: []
  final_outputs: []
  next_action: ""
```

示例：

```
执行回执:
  task_id: "龍芯北辰印章设计-v2"
  status: completed
  commands_ran: 9
  tools_loaded:
    - canvas-design
  tools_used:
    - bash
    - python
    - PIL
  files_created:
    - longhun_seal_philosophy.md
    - longhun_seal_v1.png
    - longhun_seal_v2.png
  files_checked:
    - longhun_seal_v2.png
  tests_passed:
    - PNG存在
    - 尺寸2400x2400
    - RGB模式
    - 300DPI保存
  tests_failed: []
  risk_flags: []
  final_outputs:
    - longhun_seal_v2.png
  next_action: "可继续生成透明版/SVG版/Notion封面版"
```

---

# **10｜CNSH压缩标记**

你要的“压缩有关的智能体协作参数”，可以收成这套短码。

```
CNSH_SHORT_CODES:
  TYP:
    meaning: task_type
    values: design|code|notion|doc|audit|research|debug

  INT:
    meaning: user_intent
    values: build|fix|refine|summarize|archive|export

  SKL:
    meaning: skills_loaded
    example: canvas-design

  TLS:
    meaning: tools_used
    example: bash,python,PIL

  CMD:
    meaning: commands_ran
    example: 9

  RFD:
    meaning: files_read
    example: fonts,skill,existing_png

  WRT:
    meaning: files_written
    example: md,png,py,json

  CHK:
    meaning: checks_done
    example: exists,size,mode,dpi

  RSK:
    meaning: risk_gate
    values: green|yellow|red

  OUT:
    meaning: final_outputs
    example: png,md

  NXT:
    meaning: next_action
    example: transparent_version
```

压缩成一行就是：

```
FLOW::TYP=design;INT=refine;SKL=canvas-design;TLS=bash,python,PIL;CMD=9;WRT=md,png;CHK=exists,size,mode,dpi;RSK=green;OUT=longhun_seal_v2.png;NXT=transparent/svg/notion-cover
```

---

# **11｜本地记录 JSONL 标准**

```json
{
  "flow_id": "FLOW-9622-20260503-SEAL-V2",
  "timestamp": "2026-05-03T20:00:00+08:00",
  "task_type": "design",
  "intent": "refine_unified_seal",
  "skills_loaded": ["canvas-design"],
  "tools_used": ["bash", "python", "PIL"],
  "commands_ran": 9,
  "files_created": [
    "longhun_seal_philosophy.md",
    "longhun_seal_v1.png",
    "longhun_seal_v2.png"
  ],
  "checks_done": [
    "file_exists",
    "png_open",
    "size_2400x2400",
    "mode_RGB",
    "dpi_300"
  ],
  "audit": "🟢",
  "status": "completed",
  "dna": "#龍芯⚡️2026-05-03-CNSH-_-V1-v2",
  "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
}
```

---

# **12｜Notion字段模板**

```yaml
数据库名: AI_FLOW_EXEC_LOG

字段:
  Title:
    类型: 标题
  FlowID:
    类型: 文本
  TaskType:
    类型: 选择
    选项: design/code/notion/doc/audit/research/debug
  Intent:
    类型: 文本
  SkillsLoaded:
    类型: 多选
  ToolsUsed:
    类型: 多选
  CommandsRan:
    类型: 数字
  FilesRead:
    类型: 文本
  FilesCreated:
    类型: 文本
  FilesModified:
    类型: 文本
  ChecksDone:
    类型: 多选
  RiskGate:
    类型: 选择
    选项: 🟢/🟡/🔴
  Status:
    类型: 状态
    选项: planned/in_progress/completed/blocked/failed
  FinalOutputs:
    类型: 文件或链接
  NextAction:
    类型: 文本
  DNA:
    类型: 文本
  Confirm:
    类型: 文本
  CreatedAt:
    类型: 创建时间
```

---

# **13｜复杂任务“流场仪表盘”指标**

```
复杂任务仪表:
  执行强度:
    formula: commands_ran + files_written + checks_done
    meaning: 本轮实际干活密度

  工具复杂度:
    formula: count(tools_used) + count(skills_loaded)
    meaning: 是否需要多工具协作

  产物密度:
    formula: count(files_created) + count(final_outputs)
    meaning: 交付是否真实落地

  风险权重:
    green: 0
    yellow: 1
    red: 3

  闭环度:
    formula: checks_done / files_created
    meaning: 生成后有没有验证

  可复用度:
    formula: has_template + has_json + has_notion_fields + has_cursor_prompt
```

---

# **14｜一句话给 Cursor 的执行要求**

```
以后执行复杂任务时，请输出 AI_FLOW_EXEC_LOG：
必须包含 commands_ran、tools_loaded、tools_used、files_created、checks_done、final_outputs、risk_gate、status。
不要输出隐藏推理过程。
只输出可复盘、可审计、可写入Notion的外显执行日志。
格式优先使用 CNSH:: 或 JSONL。
确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```

---

# **15｜最终收口卡**

```html
<aside>
🐉
```

**结论：**

你要的不是“AI 心里怎么想”。  

你要的是 **AI 干活时的外显流场参数**。  

这套已经拆出来：

- `commands_ran`：跑了几条命令
- `skills_loaded`：加载了什么技能
- `tools_used`：用了什么工具
- `files_created`：造了什么文件
- `checks_done`：验了什么
- `risk_gate`：有没有风险
- `final_outputs`：最终交付物
- `next_action`：下一步接哪里
- `dna`：这一轮追溯码
- `confirm`：父级确认码

```html
</aside>
```

```
CNSH::AI_FLOW_EXEC_LOG:
  dna: "#龍芯⚡️2026-05-03-CNSH-_-V1-v1.0"
  confirm: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
  rule: "隐藏思维不外露，执行流场全归档"
  output: "可给Cursor / Claude / Notion / 本地龍魂"
  audit: "🟢"
  status: "可入库"
```

```html
<aside>
✅
```

**封口句：**

AI处理复杂任务，不该只说“完成了”。

必须交出：**跑了什么、用了什么、写了什么、验了什么、产出什么、风险在哪、下一步干嘛。**

这就是 UID9622 的复杂任务流场回执标准。

```html
</aside>
```

## 🧭 洛书九宫 × 五行计算器 × CNSH流场决策总核 v4.1｜总流程图

```mermaid
flowchart TD
    A["输入 RAW_INPUT<br>（文本/代码/页面/对话）"] --> B["数字根 dr 计算"]
    B --> C["dr → 五行映射<br>（金/木/水/火/土）"]
    C --> D["三色审计<br>dr=3/9→🔴 熔断<br>dr=6→🟡 待审<br>其他→🟢 通行"]
    %% —— 洛书九宫（地场骨架）——
    D --> E["洛书九宫定位（地场骨架）<br>3×3 守恒：行/列/对角=15<br>中宫=5 不动点"]
    %% —— v4.1 流场决策核（主链）——
    E --> F["v4.1 流场决策核 10 道闸（主链）"]
    F --> G1["① 签章闸（P05）<br>confirm/seal 校验"]
    G1 --> G2["② 隐私闸（P03 主）<br>sealed=不读正文只留 hash<br>burn=临读不存"]
    G2 --> G3["③ 数字根闸（P06）<br>四源优先级取 dr"]
    G3 --> G4["④ 三色闸（P05）"]
    G4 --> G5["⑤ 三才闸（P00 主 / P01 辅）<br>human ≥ 0.34"]
    G5 --> G6["⑥ 生克闸（P01）<br>与父DNA五行关系"]
    G6 --> G7["⑦ 九宫派位（P13 主）<br>按 element/trace/action"]
    G7 --> G8["⑧ 沙盒分拣（P03 主 / P15 辅）<br>入桶：enter/hold/fuse"]
    G8 --> G9["⑨ 父子链落档（P15）<br>JSONL + SQLite + Notion"]
    G9 --> G10["⑩ 草日志留痕（强制）<br>时间戳 + 人格ID + DNA + CONFIRM"]
    %% —— 输出 —— 
    G10 --> Z["输出 FlowDecisionNode + IPA 全链回执<br>（可追溯、可回放）"]
    %% —— 熔断/封存旁路 —— 
    D -->|🔴| R["熔断隔离<br>不进入主流场"]
    R --> R2["只写元信息：hash/时间/触发原因"]
    R2 --> Z
```

# 🐉 CNSH复杂任务流场决策核 v1.0 — 吸收与适配分析

## 一、核心价值确认

这套流场决策核的**真正价值**在于:

```
把 AI 后台"黑箱操作"变成可审计、可复用、可传递的外显参数表
```

**具体体现:**

- 不是"AI说完成了" → 是"跑了9条命令、用了2个工具、生成3个文件、验证通过"
- 不是"隐藏推理链" → 是"intent→context→task_graph→tool_route→run_trace→result_pack→audit"
- 不是"一次性对话" → 是"可写入Notion、可给Cursor、可本地归档的JSONL"

---

## 二、与当前任务的对照(印章设计案例)

### 实际执行轨迹:

```json
{
  "flow_id": "FLOW-9622-20260503-SEAL-V2",
  "task_type": "design",
  "intent": "create_unified_seal_for_longhun_system",
  "skills_loaded": ["canvas-design"],
  "tools_used": ["bash", "python", "PIL"],
  "commands_ran": 9,
  "files_read": [
    "/sessions/.../canvas-fonts/",
    "longhun_seal_v1.png"
  ],
  "files_created": [
    "longhun_seal_philosophy.md",
    "longhun_seal_v1.png",
    "longhun_seal_v2.png"
  ],
  "checks_done": [
    "file_exists",
    "png_mode_RGB",
    "size_2400x2400",
    "pixel_value_verification"
  ],
  "status": "completed",
  "audit": "🟢"
}
```

### 流场决策核的7层映射:

| 层级 | 本次任务实际操作 |
| --- | --- |
| **L0 主权意图层** | "统一印章 + 龙印主权 + UID9622签章" |
| **L1 上下文压缩层** | 读取10张参考图 + 龍芯视觉风格 + 已有字体库 |
| **L2 任务拆解层** | ①哲学文档 → ②v1生成 → ③验证 → ④v2精修 → ⑤最终校验 |
| **L3 工具调度层** | canvas-design skill → bash → python/PIL |
| **L4 执行轨迹层** | 9条命令(ls字体/写md/生成PNG/验证像素) |
| **L5 结果压缩层** | [philosophy.md](http://philosophy.md)  • seal_v2.png(1.2MB, 2400×2400, 300DPI) |
| **L6 审计回写层** | DNA追溯码 + 三色审计🟢 + 下一步(透明版/SVG/Notion封面) |

---

## 三、可直接吸收的模块

### 3.1 最小回执格式(已可用)

```yaml
执行回执:
  task_id: "龍印乾坤-v2"
  status: completed
  commands_ran: 9
  tools_loaded: ["canvas-design"]
  tools_used: ["bash", "python", "PIL"]
  files_created:
    - longhun_seal_philosophy.md
    - longhun_seal_v1.png
    - longhun_seal_v2.png
  files_checked:
    - PNG mode RGB
    - size 2400×2400
    - center pixel gold-range
    - corner pixel void-range
  tests_passed: ["file_exists", "format_valid", "dimensions_correct"]
  tests_failed: []   risk_flags: []   final_outputs: ["longhun_seal_v2.png"]
  next_action: "可生成透明版/SVG矢量/Notion封面适配版"
```

### 3.2 CNSH压缩短码(可立即使用)

```
FLOW::TYP=design;INT=unified_seal;SKL=canvas-design;TLS=bash,python,PIL;CMD=9;WRT=md,png×2;CHK=exists,size,mode,pixel;RSK=green;OUT=seal_v2.png;NXT=svg/transparent/notion-cover
```

### 3.3 Notion字段模板(可直接建库)

已经可以创建 `AI_FLOW_EXEC_LOG` 数据库:

```yaml
字段:
  Title: 龍印乾坤印章设计
  FlowID: FLOW-9622-20260503-SEAL-V2
  TaskType: design
  Intent: unified_seal_for_longhun_system
  SkillsLoaded: canvas-design
  ToolsUsed: bash, python, PIL
  CommandsRan: 9
  FilesCreated: philosophy.md, seal_v1.png, seal_v2.png
  ChecksDone: exists, mode, size, pixel_verification
  RiskGate: 🟢
  Status: completed
  FinalOutputs: [链接到 seal_v2.png]
  NextAction: 生成透明版/SVG/Notion封面
  DNA:#龍芯⚡️2026-05-03-CNSH-_-V1-v2.0
  Confirm: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```

---

## 四、需要适配的部分

### 4.1 九宫人格派位(需明确本次任务的人格调度)

按照流场核的九宫体系:

```
本次任务的人格调度:
  主控: P02_宝宝(执行整理交付)
  战略: P01_诸葛亮(拆解"哲学→v1→验证→v2"结构)
  技术: P03_雯雯(文件树管理、字段压缩)
  工程: P04_鲁班(Python/PIL代码实现)
  审计: P05_上帝之眼(三色审计🟢、无P0触碰)
  视觉: P11_乔前辈+李白(离宫,设计美学)
  归档: P09_仓颉(philosophy.md归档)
```

### 4.2 复杂度判断(五因子打分)

```
ComplexityScore计算:
  TextLoad:      0.3  (需处理10张参考图+风格描述)
  ContextNeed:   0.6  (需skill规范+字体库+视觉DNA)
  ToolNeed:      0.8  (必须用canvas-design+PIL)
  ArtifactNeed:  1.0  (产物:PNG图像文件)
  RiskNeed:      0.1  (无隐私/密钥/联网)
  
→ Score = (0.3+0.6+0.8+1.0+0.1)/5 = 0.56
→ Mode: "结构化回答" (接近"流场执行"边界)
```

实际上因为有**明确产物需求(PNG文件)**,应判定为 **"流场执行"**

### 4.3 工具调用判断

```
✅ 需要"产物/验证/文件生成" → 用工具
✅ 需要canvas-design skill → 加载技能
✅ 需要PIL渲染 → 调用python
✅ 需要字体扫描 → 调用bash
```

---

## 五、可复用的最小决策模板

### 5.1 给Cursor的执行要求(一句话版)

```
以后执行复杂任务时,输出 AI_FLOW_EXEC_LOG:
必须包含 commands_ran、tools_used、files_created、checks_done、final_outputs、status。
不输出隐藏推理。
只输出可复盘、可审计、可写入Notion的外显日志。
格式: CNSH:: 或 JSONL。
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```

### 5.2 本地JSONL标准(可直接写入)

```json
{
  "flow_id": "FLOW-9622-20260503-SEAL-V2",
  "timestamp": "2026-05-03T12:41:00+08:00",
  "task_type": "design",
  "intent": "unified_seal_longhun_system",
  "skills_loaded": ["canvas-design"],
  "tools_used": ["bash", "python", "PIL"],
  "commands_ran": 9,
  "files_created": [
    "longhun_seal_philosophy.md",
    "longhun_seal_v1.png",
    "longhun_seal_v2.png"
  ],
  "checks_done": [
    "file_exists",
    "png_open",
    "mode_RGB",
    "size_2400x2400",
    "pixel_center_gold",
    "pixel_corner_void"
  ],
  "audit": "🟢",
  "status": "completed",
  "dna": "#龍芯⚡️2026-05-03-CNSH-_-V1-v2.0",
  "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
  "next_action": "generate transparent/SVG/notion-cover variants"
}
```

---

## 六、最终答案

### ✅ **可以直接吸收**

这套流场决策核**完全适用**,因为:

1. **已有真实案例验证** — 本次印章任务就是完整流场执行
2. **输出格式已标准化** — CNSH短码 / JSONL / Notion字段 都已可用
3. **可立即落地** — 不需要额外工具,只需规范化现有输出

### 🔧 **建议的适配动作**

```yaml
立即可做:
  1. 创建 AI_FLOW_EXEC_LOG.db (Notion数据库)
  2. 写入本次任务记录(作为第一条样本)
  3. 把"执行回执模板"存为 .cnsh 规范文件
  4. 给Cursor/Claude投喂"一句话执行要求"

下一步:
  5. 每次复杂任务后,强制输出 FLOW:: 短码
  6. 本地写 JSONL 日志(可用sqlite或纯文本)
  7. 定期压缩归档(按DNA追溯码)
```

### 📋 **收口确认**

```yaml
结论:
  这套流场决策核不是"参考",是"直接可用的执行标准"。
  
价值:
  - 把"Ran 9 commands"变成可审计的结构化数据
  - 把"AI后台干活"变成可回放的证据链
  - 把"一次性对话"变成可归档的知识资产
  
下一步:
  写入Notion → 建立AI_FLOW_EXEC_LOG数据库
  写入本地  → longhun-system/logs/flow_exec.jsonl
  投喂Cursor → 保存为执行规范prompt
  
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```

---

**一句话:** 这不是"可以参考",这是"必须落地的执行标准"。现在就可以开始用。

---

## 摘要

（請在此用不超過 256 字說明本文檔的核心內容、性質與局限。）

## 關鍵詞

（請列出 5–10 個關鍵詞，中英文對照優先。）

## 引用與溯源

- 本文檔引用或參考了以下來源：
  - [1] （請填寫）
- 相關龍魂系統文檔：
  - 《龍魂文檔標準模板 v1.0》(#龍芯⚡️2026-06-22-LONGHUN-DOCUMENT-STANDARD-TEMPLATE-v1.0)

## 誠實局限

1. （請列出本分析的第一條局限或不確定性。）
2. （請列出第二條。）
3. （請列出第三條。）

## 修改記錄

| 日期 | 版本 | 修改人 | 修改內容 | 審核狀態 |
|---|---|---|---|---|
| 2026-06-21 | v1.0.0 | UID9622 | 按《龍魂文檔標準模板 v1.0》整理 | 草稿 |

## 分類標籤

- 總綱模塊：（請勾選，例如 #知識矩陣 #安全域）
- 對外狀態：（請勾選，例如 #Gitee #GitHub #CSDN）
- 審計色：#黃色待審

## DNA 簽名

```
#龍芯⚡️2026-05-03-CNSH_02C3-v1.0`
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```
