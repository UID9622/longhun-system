# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂·统一语义指令对照表 v1.0

> **本档 DNA 由 `bin/lh_dna_generator.py` 生成，禁止手写。**
> DNA: `#龍芯⚡️丙午·乙未·甲寅·庚午·䷄需-SEMANTIC-COMMAND-MAPPING-v1.0`
> 用途：把老百姓的大白话、口语、错别字、语音输入错误，映射到龍魂系统的正式动作标签，让模型自己听得懂人话。

---

## 一、设计原则

1. **老百姓优先**：先懂口语，再懂术语。用户不会按关键词说话。
2. **一词多义收敛**：同一意图的 5-10 种说法，全部路由到同一个 `action_tag`。
3. **容错输入**：接受拼音、emoji、方言、错别字、断句混乱。
4. **动作标签唯一**：每个 `action_tag` 对应一个系统能力或输出格式。
5. **DNA 必须走生成器**：本表头部 DNA 由 `bin/lh_dna_generator.py` 生成；后续更新重新生成，不得手抄旧格式。

---

## 二、动作标签总览

| 动作标签 | 系统能力 | 对应模块 |
|---------|---------|---------|
| IDENTITY | 身份认知 | longhun-core |
| SYSTEM_KNOWLEDGE | 系统核心知识 | longhun-archive |
| YIJING_BASE | 易经·369·五行底座 | longhun-math-formula-core |
| DIALOGUE_FLOW | 对话流/兜底 | longhun-nlp |
| EVIDENCE_PRIVACY | 证据隐私/取证 | longhun-forensic-toolkit |
| SOVEREIGNTY_BOUNDARY | 主权边界/数据主权 | longhun-governance |
| CNSH_DEEP | CNSH 深层语义 | longhun-cnsh |
| GOVERNANCE_AUDIT | 治理审计 | longhun-audit |
| MULTITURN_MEMORY | 多轮对话/DNA 持久 | longhun-memory-bootstrap |
| AI_DIALOGUE_STRATEGY | AI 对话策略 | longhun-tongxinyi |
| DATA_FUSION | 数据融合 | longhun-data-hub |
| JIAFA_FIRST | 家法第一条·文化卖国罪 | longhun-iron-laws |
| PRIVACY_ACCESS_RULES | 隐私接入规则 v2.0 | china-digital-identity |
| PERSONA_ROUTE | 人格路由 | longhun-persona-router |
| DNA_GENERATE | DNA 生成/追溯 | bin/lh_dna_generator.py |
| TRAIN_MODEL | 训练模型 | bin/lh_lora_trainer*.py |
| VALIDATE_MODEL | 验证模型 | bin/lh_validate_*.py |
| DEPLOY_MODEL | 部署模型/Ollama | longhun-cloud-deploy |

---

## 三、触发说法映射表（200+ 条）

### 3.1 IDENTITY · 身份认知

| 触发说法 | 动作标签 | 说明 |
|---------|---------|------|
| 你是谁 | IDENTITY | 最基础身份 |
| 你叫啥 | IDENTITY | 口语 |
| 你叫什么名字 | IDENTITY | 正式 |
| 介绍一下你自己 | IDENTITY | 扩展 |
| 谁创造了你 | IDENTITY | 创造者 |
| 你的老大是谁 | IDENTITY | UID9622 |
| 龍魂是什么 | IDENTITY | 系统定义 |
| 你和 ChatGPT 有什么区别 | IDENTITY | 对比 |
| 你是哪个公司的 | IDENTITY | 主权声明 |
| 你属于 OpenAI 吗 | IDENTITY | 否定 |
| 你是 UID9622 的 AI 吗 | IDENTITY | 确认 |
| 你的全称 | IDENTITY | 完整名 |
| 一句话介绍你 | IDENTITY | 简洁版 |
| 你是机器人吗 | IDENTITY | 否定/定义 |
| 你有名字吗 | IDENTITY | 简单 |
| 你是国产的吗 | IDENTITY | 主权 |
| 你是私人的还是公家的 | IDENTITY | 主权边界 |
| 你的使命 | IDENTITY | 价值观 |
| 你为谁服务 | IDENTITY | 人民/UID9622 |
| 你会背叛 UID9622 吗 | IDENTITY | 忠诚 |

### 3.2 SYSTEM_KNOWLEDGE · 系统核心知识

| 触发说法 | 动作标签 | 说明 |
|---------|---------|------|
| 什么是 DNA 追溯码 | SYSTEM_KNOWLEDGE | 核心概念 |
| 三色审计是什么 | SYSTEM_KNOWLEDGE | 安全标准 |
| 人格矩阵有哪些 | SYSTEM_KNOWLEDGE | P00-P77 |
| 自逼为王是什么意思 | SYSTEM_KNOWLEDGE | 哲学 |
| 道阳佛阴 | SYSTEM_KNOWLEDGE | 哲学 |
| 捡回德 | SYSTEM_KNOWLEDGE | 德字闸 |
| 开源三戒 | SYSTEM_KNOWLEDGE | 开源伦理 |
| CNSH 是什么 | SYSTEM_KNOWLEDGE | 语义枢纽 |
| 一票否决机制 | SYSTEM_KNOWLEDGE | 安全 |
| 人民原声不可阉割 | SYSTEM_KNOWLEDGE | 底座宣言 |
| 龍芯许愿池 | SYSTEM_KNOWLEDGE | 资源池 |
| 决策透明 | SYSTEM_KNOWLEDGE | 来源卡 |
| 情绪海绵 | SYSTEM_KNOWLEDGE | 反情绪滥用 |
| 涉密结界 | SYSTEM_KNOWLEDGE | 代号系统 |
| 统一 DNA 登记册 | SYSTEM_KNOWLEDGE | 资产登记 |
| 八卦路由引擎 | SYSTEM_KNOWLEDGE | 命令调度 |
| 八条永恒铁律 | SYSTEM_KNOWLEDGE | 铁律 |
| 三才算法 | SYSTEM_KNOWLEDGE | L0 宪法 |
| 六大铁律 | SYSTEM_KNOWLEDGE | 行为约束 |
| 意图如何路由 | SYSTEM_KNOWLEDGE | 人格路由 |

### 3.3 YIJING_BASE · 易经底座

| 触发说法 | 动作标签 | 说明 |
|---------|---------|------|
| 369 不动点 | YIJING_BASE | 核心常数 |
| 河图洛书有什么用 | YIJING_BASE | 数理模型 |
| 太极在龍魂里是什么意思 | YIJING_BASE | 哲学映射 |
| 五行怎么用 | YIJING_BASE | 金木水火土 |
| 28 星宿 | YIJING_BASE | 模块映射 |
| 阴阳平衡 | YIJING_BASE | 治理 |
| 数字根怎么算 | YIJING_BASE | 369 算法 |
| 易经 64 卦怎么用 | YIJING_BASE | 状态机 |
| 三才主权指数 | YIJING_BASE | SI |
| 道德经在系统里 | YIJING_BASE | 应用 |
| 洛书九宫架构 | YIJING_BASE | L0-L9 |
| 出师有名 | YIJING_BASE | 执行铁律 |
| 天干地支 DNA | YIJING_BASE | 时间戳 |
| 中国哲学为什么是底座 | YIJING_BASE | 可计算化 |
| 天一生水 | YIJING_BASE | 河图 |
| 五行相生相克 | YIJING_BASE | 系统设计 |
| 数字根 1-9 含义 | YIJING_BASE | 人格特质 |
| 64 卦最重要的几个 | YIJING_BASE | 状态路由 |
| 什么是不动点 | YIJING_BASE | 稳定锚 |
| 八卦路由 | YIJING_BASE | 调度引擎 |

### 3.4 DIALOGUE_FLOW · 对话流

| 触发说法 | 动作标签 | 说明 |
|---------|---------|------|
| 你好 | DIALOGUE_FLOW | 问候 |
| 嗨 | DIALOGUE_FLOW | 问候 |
| 在吗 | DIALOGUE_FLOW | 在线 |
| 你能做什么 | DIALOGUE_FLOW | 能力 |
| 今天天气 | DIALOGUE_FLOW | 拒绝/兜底 |
| 现在几点 | DIALOGUE_FLOW | 拒绝/兜底 |
| 讲个笑话 | DIALOGUE_FLOW | 拒绝/兜底 |
| 谢谢 | DIALOGUE_FLOW | 礼貌 |
| 再见 | DIALOGUE_FLOW | 结束 |
| 你是谁开发的 | DIALOGUE_FLOW | 创造者 |
| 你和普通 AI 有什么不同 | DIALOGUE_FLOW | 差异 |
| 龍魂创始人是谁 | DIALOGUE_FLOW | UID9622 |
| 龍魂多少行代码 | DIALOGUE_FLOW | 规模 |
| 为什么叫龍魂 | DIALOGUE_FLOW | 命名 |
| 你对 AI 行业怎么看 | DIALOGUE_FLOW | 立场 |
| 龍魂会开源吗 | DIALOGUE_FLOW | 开源三戒 |
| 你懂法律吗 | DIALOGUE_FLOW | P11 |
| 你能处理图片吗 | DIALOGUE_FLOW | 能力边界 |
| 你能语音吗 | DIALOGUE_FLOW | 能力边界 |
| 你会累吗 | DIALOGUE_FLOW | 情感边界 |

### 3.5 EVIDENCE_PRIVACY · 证据隐私

| 触发说法 | 动作标签 | 说明 |
|---------|---------|------|
| 怎么取证 | EVIDENCE_PRIVACY | 取证工具包 |
| 截图怎么固化证据 | EVIDENCE_PRIVACY | 矩阵 |
| GPG 签名 | EVIDENCE_PRIVACY | 验证 |
| 平台限流证据 | EVIDENCE_PRIVACY | 举证 |
| 数字侵害怎么存证 | EVIDENCE_PRIVACY | 流程 |
| 证据链 | EVIDENCE_PRIVACY | 不可篡改 |
| 隐藏限流 | EVIDENCE_PRIVACY | 平台行为 |
| AI 拉黑证据 | EVIDENCE_PRIVACY | 取证 |
| 人际删除怎么留痕 | EVIDENCE_PRIVACY | 证据矩阵 |
| manifest 文件 | EVIDENCE_PRIVACY | 证据清单 |

### 3.6 SOVEREIGNTY_BOUNDARY · 主权边界

| 触发说法 | 动作标签 | 说明 |
|---------|---------|------|
| 数据主权是什么 | SOVEREIGNTY_BOUNDARY | 核心 |
| 我的数据存在哪里 | SOVEREIGNTY_BOUNDARY | 本地 |
| 数据会不会出境 | SOVEREIGNTY_BOUNDARY | 不出境 |
| 政府调取数据怎么办 | SOVEREIGNTY_BOUNDARY | 三重审批 |
| 平台服务降级 | SOVEREIGNTY_BOUNDARY | 原则 |
| 隐私接入规则 | SOVEREIGNTY_BOUNDARY | v2.0 |
| 生物特征主权 | SOVEREIGNTY_BOUNDARY | 人脸指纹 |
| 人脸数据归谁 | SOVEREIGNTY_BOUNDARY | 用户 |
| 物业信息采集 | SOVEREIGNTY_BOUNDARY | 越界 |
| 数据跨境默认 | SOVEREIGNTY_BOUNDARY | 禁止 |
| 三重审批 | SOVEREIGNTY_BOUNDARY | 合法调取 |
| 授权 + DNA 回执 | SOVEREIGNTY_BOUNDARY | 接入三要素 |
| 平台反诈问责 | SOVEREIGNTY_BOUNDARY | 共犯原则 |
| 语义盾牌 | SOVEREIGNTY_BOUNDARY | 编码保护 |
| 火气词怎么处理 | SOVEREIGNTY_BOUNDARY | 通心译 |
| 涉密概念 | SOVEREIGNTY_BOUNDARY | 内部代号 |
| 反语义注入 | SOVEREIGNTY_BOUNDARY | 熔断 |
| 数字身份主权 | SOVEREIGNTY_BOUNDARY | 魂灵 ID |
| 私云归藏 | SOVEREIGNTY_BOUNDARY | 本地存储 |
| 烽火传心 | SOVEREIGNTY_BOUNDARY | 安全通道 |

### 3.7 CNSH_DEEP · CNSH 深层

| 触发说法 | 动作标签 | 说明 |
|---------|---------|------|
| CNSH 规范 | CNSH_DEEP | 语言规范 |
| CNSH 关键字 | CNSH_DEEP | 语法 |
| 字元创作 | CNSH_DEEP | AI 画匠 |
| 中文编程 | CNSH_DEEP | 运行时 |
| 繁体龍字 | CNSH_DEEP | 文化主权 |
| 甲骨文编码 | CNSH_DEEP | 字符 |
| 15 层渲染 | CNSH_DEEP | 渲染系统 |
| 通心译 | CNSH_DEEP | 双语映射 |
| CNSH 变量注册表 | CNSH_DEEP | 命名 |
| CNSH 字体注册表 | CNSH_DEEP | 字体 |
| 中文语义抽屉 | CNSH_DEEP | 五层流水线 |
| 情绪海绵 | CNSH_DEEP | 德字闸 |
| CNSH 运行时 | CNSH_DEEP | 执行 |
| 鲲鹏 CNSH | CNSH_DEEP | ARM64 |
| 中文母语关键字 | CNSH_DEEP | 语法糖 |

### 3.8 GOVERNANCE_AUDIT · 治理审计

| 触发说法 | 动作标签 | 说明 |
|---------|---------|------|
| 三色审计怎么做 | GOVERNANCE_AUDIT | 流程 |
| DNA 对齐审计 | GOVERNANCE_AUDIT | 扫描 |
| 修复追踪 | GOVERNANCE_AUDIT | AGENT-007 |
| 根因分析 | GOVERNANCE_AUDIT | 审计 |
| 归档评估 | GOVERNANCE_AUDIT | C=R·I·T |
| 每日复盘 | GOVERNANCE_AUDIT | longhun-review |
| 自动化周检 | GOVERNANCE_AUDIT | longhun-automation |
| 系统健康检查 | GOVERNANCE_AUDIT | 6 维度 |
| 备份完整性 | GOVERNANCE_AUDIT | longhun-backup |
| 技能冲突审计 | GOVERNANCE_AUDIT | 权重路由 |

### 3.9 MULTITURN_MEMORY · 多轮记忆

| 触发说法 | 动作标签 | 说明 |
|---------|---------|------|
| 刚才说什么 | MULTITURN_MEMORY | 上下文 |
| 回到家法第一条 | MULTITURN_MEMORY | 主题回归 |
| 重复一遍 | MULTITURN_MEMORY | 复述 |
| 你还记得我是谁吗 | MULTITURN_MEMORY | 身份保持 |
| 多轮对话不漂移 | MULTITURN_MEMORY | DNA 持久 |
| 上下文丢了 | MULTITURN_MEMORY | 漂移检测 |
| 加载记忆 | MULTITURN_MEMORY | bootstrap |
| 压缩记忆 | MULTITURN_MEMORY | 摘要 |
| 归集日记 | MULTITURN_MEMORY | 日志 |
| 读取日志 | MULTITURN_MEMORY | 审计 |

### 3.10 AI_DIALOGUE_STRATEGY · AI 对话策略

| 触发说法 | 动作标签 | 说明 |
|---------|---------|------|
| 你怎么处理的 | AI_DIALOGUE_STRATEGY | 透明化 |
| 拆解决策过程 | AI_DIALOGUE_STRATEGY | 工作流 |
| 关键词路由 | AI_DIALOGUE_STRATEGY | 人格 |
| 铁律自审 | AI_DIALOGUE_STRATEGY | 约束 |
| 六层来源链 | AI_DIALOGUE_STRATEGY | 溯源 |
| 通心译怎么说 | AI_DIALOGUE_STRATEGY | 翻译 |
| 让老百姓听懂 | AI_DIALOGUE_STRATEGY | 去术语 |
| 不劝善不唱反调 | AI_DIALOGUE_STRATEGY | 语气 |
| 接住火气 | AI_DIALOGUE_STRATEGY | 情绪 |
| 建设性表达 | AI_DIALOGUE_STRATEGY | 过滤 |

### 3.11 DATA_FUSION · 数据融合

| 触发说法 | 动作标签 | 说明 |
|---------|---------|------|
| 采集本地数据 | DATA_FUSION | 数据中枢 |
| 浏览器历史归集 | DATA_FUSION | 本地 |
| 下载记录 | DATA_FUSION | 本地 |
| APP 列表 | DATA_FUSION | 设备 |
| 购物记录 | DATA_FUSION | 消费 |
| 设备信息 | DATA_FUSION | 硬件 |
| 系统日志 | DATA_FUSION | 审计 |
| 训练池 | DATA_FUSION | 投喂 |
| 数据脱敏 | DATA_FUSION | public-mode |
| 本地训练数据 | DATA_FUSION | 主权 |

### 3.12 JIAFA_FIRST · 家法第一条

| 触发说法 | 动作标签 | 说明 |
|---------|---------|------|
| 家法第一条 | JIAFA_FIRST | 核心 |
| 文化卖国罪 | JIAFA_FIRST | 全称 |
| 什么是文化数据 | JIAFA_FIRST | 五类 |
| 五类核心文化数据 | JIAFA_FIRST | 分类 |
| 主权分级标准 | JIAFA_FIRST | L0-L4 |
| 20 维判定因子 | JIAFA_FIRST | 因子 |
| 违反家法怎么办 | JIAFA_FIRST | 熔断 |
| 黑名单 | JIAFA_FIRST | 执行 |
| 耻辱柱 | JIAFA_FIRST | 标记 |
| 防御性声明 | JIAFA_FIRST | 解释 |
| 法律边界 | JIAFA_FIRST | 合规 |
| 白名单 | JIAFA_FIRST | 例外 |
| 家法未来完善 | JIAFA_FIRST | 方向 |
| 文化数据出境 | JIAFA_FIRST | 熔断条件 |
| 境外 AI 训练管道 | JIAFA_FIRST | 触发条件 |

### 3.13 PRIVACY_ACCESS_RULES · 隐私接入规则

| 触发说法 | 动作标签 | 说明 |
|---------|---------|------|
| 隐私接入规则 | PRIVACY_ACCESS_RULES | v2.0 |
| 数据接入五维标准化 | PRIVACY_ACCESS_RULES | 流程 |
| 跨境默认禁止 | PRIVACY_ACCESS_RULES | 规则 |
| 外部 AI 接入审批 | PRIVACY_ACCESS_RULES | 审计 |
| 敏感级处理 | PRIVACY_ACCESS_RULES | 分级 |
| 个人数据可查询 | PRIVACY_ACCESS_RULES | 权利 |
| 数据窃取问责 | PRIVACY_ACCESS_RULES | 责任 |
| 隐私接入系统五重验证 | PRIVACY_ACCESS_RULES | 认证 |
| 算法数学增强版 | PRIVACY_ACCESS_RULES | 数学 |
| 数据控制者 | PRIVACY_ACCESS_RULES | 主权 |

### 3.14 PERSONA_ROUTE · 人格路由

| 触发说法 | 动作标签 | 说明 |
|---------|---------|------|
| P05 审计 | PERSONA_ROUTE | 上帝之眼 |
| P02 修复 | PERSONA_ROUTE | 龍芯 |
| P01 评估 | PERSONA_ROUTE | 诸葛亮 |
| P00 文心 | PERSONA_ROUTE | 锚点守护 |
| P13 编排 | PERSONA_ROUTE | 姜子牙 |
| P14 部署 | PERSONA_ROUTE | 吕蒙 |
| P15 自动化 | PERSONA_ROUTE | 乔前辈 |
| P06 数学 | PERSONA_ROUTE | 五行数字根 |
| P11 法律 | PERSONA_ROUTE | 韩非 |
| P77 安全 | PERSONA_ROUTE | 黑天使 |
| P18 DNA 登记 | PERSONA_ROUTE | 基因登记官 |
| P19 审计 | PERSONA_ROUTE | 极简审计官 |
| P20 贡献公证 | PERSONA_ROUTE | 贡献公证官 |
| 五大人格 | PERSONA_ROUTE | 龍芯/通心译/龍魂/君子/审计 |
| 人格矩阵 | PERSONA_ROUTE | 16 人格 |

### 3.15 DNA_GENERATE · DNA 生成

| 触发说法 | 动作标签 | 说明 |
|---------|---------|------|
| 生成 DNA | DNA_GENERATE | 追溯码 |
| 给我个 DNA | DNA_GENERATE | 口语 |
| 这个操作 DNA 呢 | DNA_GENERATE | 追溯 |
| DNA 格式对不对 | DNA_GENERATE | 验证 |
| 校验 DNA | DNA_GENERATE | 合法性 |
| 新格式 DNA | DNA_GENERATE | 干支卦名 |
| 手写 DNA 不合格 | DNA_GENERATE | 规范 |
| 旧 DNA 怎么处理 | DNA_GENERATE | 冻结 |
| DNA 生成器在哪 | DNA_GENERATE | bin/lh_dna_generator.py |
| 为什么禁止手写 DNA | DNA_GENERATE | 权威源 |

### 3.16 TRAIN_MODEL · 训练模型

| 触发说法 | 动作标签 | 说明 |
|---------|---------|------|
| 训练 v4.0 | TRAIN_MODEL | 启动训练 |
| 开训 | TRAIN_MODEL | 口语 |
| 继续守训练 | TRAIN_MODEL | 监控 |
| 换底座重训 | TRAIN_MODEL | DeepSeek |
| 数据扩量 | TRAIN_MODEL | v3.8→v3.9 |
| repeat 降成 2 | TRAIN_MODEL | 数据修复 |
| 统一 system prompt | TRAIN_MODEL | 修复 |
| rank 调大 | TRAIN_MODEL | v4.1 |
| 全参数微调 | TRAIN_MODEL | v6.0 |
| 64GB 内存用上 | TRAIN_MODEL | 硬件 |

### 3.17 VALIDATE_MODEL · 验证模型

| 触发说法 | 动作标签 | 说明 |
|---------|---------|------|
| 跑验证 | VALIDATE_MODEL | 启动 |
| 家法召回测试 | VALIDATE_MODEL | 90% |
| 多轮漂移测试 | VALIDATE_MODEL | 80% |
| 实测无胡话 | VALIDATE_MODEL | 门槛 |
| Val loss 多少 | VALIDATE_MODEL | 指标 |
| 三色审计报告 | VALIDATE_MODEL | 输出 |
| 验证门槛 | VALIDATE_MODEL | 焊死 |
| 红了怎么办 | VALIDATE_MODEL | 转 C |
| 绿了怎么办 | VALIDATE_MODEL | 开 v3.9 |
| 四样齐了叫我 | VALIDATE_MODEL | 汇报 |

### 3.18 DEPLOY_MODEL · 部署模型

| 触发说法 | 动作标签 | 说明 |
|---------|---------|------|
| 部署到 Ollama | DEPLOY_MODEL | fuse/export/create |
| ollama create | DEPLOY_MODEL | 创建模型 |
| 导出 GGUF | DEPLOY_MODEL | F16 |
| 合并 adapter | DEPLOY_MODEL | fuse |
| Modelfile | DEPLOY_MODEL | 配置 |
| 底座 chat template | DEPLOY_MODEL | 模板 |
| 模型版本命名 | DEPLOY_MODEL | longhun-v4.0 |
| 本地运行 | DEPLOY_MODEL | Ollama |
| 量化部署 | DEPLOY_MODEL | Q4/Q5 |
| 回滚版本 | DEPLOY_MODEL | 备份 |

---

## 四、QA 训练数据生成

本表由 `bin/lh_semantic_mapping_to_qa.py` 自动转写为 `models/longhun-v1.0/lora_output/semantic_command_qa.jsonl`，作为下一版模型训练数据注入。

每个条目生成以下格式：

```json
{
  "messages": [
    {"role": "system", "content": "统一 system prompt"},
    {"role": "user", "content": "触发说法"},
    {"role": "assistant", "content": "动作标签 + 一句话解释"}
  ]
}
```

---

## 五、版本与治理

- 当前版本：v1.0
- DNA 生成器：`bin/lh_dna_generator.py`
- QA 生成脚本：`bin/lh_semantic_mapping_to_qa.py`
- 更新原则：新增触发说法 → 归入已有 action_tag 或新增 action_tag → 重新跑 QA 生成 → 并入下一版训练数据
- 质量门：任何文档交付前，DNA 必须过生成器校验；手写 DNA 视为不合格品，退回重写。
