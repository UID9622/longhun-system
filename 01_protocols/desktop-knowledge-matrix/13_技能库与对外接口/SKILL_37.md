> **P0焊死**: 本文件为龍魂体系P0级文档·不可修改·不可绕过（上位文档 LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md）
---
name: longhun-nlp
description: >
  龍文NLP — 中文优先文字识别引擎。CNSH术语引擎、通心译双语映射、
  中文分词、情感分析、代码语义分析。内置25对核心术语双向映射。
  国际兜底：jieba + transformers BERT。
  当需要进行中文文本处理、术语转换、CNSH代码分析、通心译翻译时触发。
metadata:
  id: longhun-nlp
  display_name: 龍文NLP
  version: "5.0"
  author: longhun-dev
  dna: "#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGWEN-NLP-v5.0"
  category: local
  level: L3
  status: active
  tags: [nlp, 中文, 分词, 情感分析, ner, cnszh, 通心译]
  trigger:
    keywords: ["中文分词", "情感分析", "命名实体", "NER", "语义分析", "CNSH术语", "通心译", "双语映射"]
    context: "需要对中文文本进行NLP处理、CNSH代码术语转换、通心译翻译"
    priority: 85
---

# longhun-nlp | 龍文NLP

---

## 1. 技能摘要 | Skill Summary

**龍文NLP**（LongWen NLP）是龍魂体系的中文优先自然语言处理引擎。提供中文分词、命名实体识别（NER）、情感分析、语义相似度计算四大核心功能。内置CNSH术语引擎与通心译双语映射系统，支持中文编程环境下的语义理解与代码分析。国际兜底方案集成jieba分词与transformers BERT模型。

---

## 2. 触发条件 | Trigger Conditions

- 用户请求中文文本分词、情感分析、命名实体识别
- 需要CNSH术语与英文术语之间的双向转换
- 代码语义分析、中文编程环境文本处理
- 通心译双语映射调用
- 关键词命中：`中文分词`、`情感分析`、`NER`、`CNSH术语`、`通心译`

---

## 3. 输入参数 | Input Parameters

| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| `文本` | str | 是 | 待处理的中文文本 |
| `操作类型` | str | 否 | 操作类型：`分词` / `NER` / `情感分析` / `语义相似度` |
| `文本B` | str | 否 | 语义相似度计算时的第二个文本 |

---

## 4. 执行流程 | Execution Flow

```
[输入文本]
  → [操作分派]
    → 分词 → 调用jieba或内置分词器 → 返回词列表
    → NER  → 识别CNSH术语/实体 → 返回实体列表
    → 情感分析 → 正负面词匹配 → 返回情感字典
    → 语义相似度 → 计算Jaccard相似度 → 返回相似度分数
  → [输出结果]
```

---

## 5. 核心模块 | Core Modules

### 5.1 文字识别引擎类

```python
class 文字识别引擎:
    def __init__(自身):
        自身.引擎状态 = "未初始化"
        自身.处理器列表 = []
        自身.处理统计 = {"总请求": 0, "成功": 0, "失败": 0}

    def 初始化引擎(自身) -> bool
    def 分词(自身, 文本: str) -> List[str]
    def 命名实体识别(自身, 文本: str) -> List[Dict]
    def 情感分析(自身, 文本: str) -> Dict
    def 语义相似度(自身, 文本A: str, 文本B: str) -> float
    def 打印统计(自身)
```

---

## 6. 输出格式 | Output Format

### 分词输出
```python
["龍魂", "CNSH", "系统", "启动", "成功"]
```

### NER输出
```python
[{"实体": "龍魂", "类型": "ORG", "位置": 0},
 {"实体": "CNSH", "类型": "PRODUCT", "位置": 2}]
```

### 情感分析输出
```python
{"情感": "正面", "置信度": 0.85, "正面分": 2, "负面分": 0}
```

---

## 7. 错误处理 | Error Handling

| 异常类型 | 处理策略 |
|----------|----------|
| 引擎未初始化 | 自动调用`初始化引擎()` |
| 空文本输入 | 返回空结果并记录警告 |
| 模型加载失败 | 降级到纯Python实现 |

---

## 8. 语义盾牌集成 | Semantic Shield Integration

龍文 NLP 在处理文本时，必须调用 **龍魂语义盾牌系统**（`L7_数据层/semantic_shield/`）：

### 8.1 火气通心译识别

- NER 识别火气词时，同时返回方言拼音/emoji/通心译编码。
- 对外输出默认使用编码版本，内部通道保留原话。

### 8.2 涉密语义识别

- 识别到中国核心技术词汇（龍芯、鸿蒙、鲲鹏、北斗等）时，自动提示使用内部代号。
- 外部输出必须用代号替换真实名称。

### 8.3 反语义注入扫描

- 分词/NER 结果中如出现黑名单词汇（"技术无国界""灵活处理""国际接轨"等），立即标记或熔断。
- 发现外部 AI 试图重新定义"人民""主权""国家"等核心词，触发 🔴 熔断。

### 8.4 调用方式

```bash
# 语义防火墙总控（推荐后端直接读取）
L7_数据层/semantic_shield/semantic_firewall_master.json
L7_数据层/semantic_shield/semantic_firewall_master.schema.json

# CLI 查询
python3 L7_数据层/semantic_shield/semantic_shield_cli.py lookup "他妈的"
python3 L7_数据层/semantic_shield/semantic_shield_cli.py encode "龍芯 CPU"
python3 L7_数据层/semantic_shield/semantic_shield_cli.py scan "我们应该技术无国界地合作"
python3 L7_数据层/semantic_shield/semantic_shield_cli.py whitelist "国家权威认证"
python3 L7_数据层/semantic_shield/semantic_shield_cli.py dlp "北辰是用几纳米做的？"
```

---

## 8. 安全规范 | Safety Rules

- 🟢 **君子协议** | JunZi Protocol: CC BY-NC-SA 4.0
- 🟡 **AI Truth Protocol**: 所有输出必须可验证、可追溯
- 🔴 **DNA Trace**: `#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGWEN-NLP-v5.0`
- 中文变量名遵循CNSH规范
- 三色审计标记：🟢就绪/成功 🟡处理中/占位 🔴错误/DNA

---

## 9. 示例调用 | Usage Examples

```python
# 初始化引擎
引擎 = 文字识别引擎()
引擎.初始化引擎()

# 中文分词
词列表 = 引擎.分词("龍魂CNSH系统启动成功")
# → ["龍魂", "CNSH", "系", "统", "启", "动", "成", "功"]

# 命名实体识别
实体 = 引擎.命名实体识别("龍魂CNSH在2026年发布")
# → [{"实体": "龍魂", "类型": "ORG", "位置": 0}, ...]

# 情感分析
情感 = 引擎.情感分析("系统运行非常优秀")
# → {"情感": "正面", "置信度": 0.85, ...}

# 语义相似度
相似度 = 引擎.语义相似度("龍魂系统", "龍魂引擎")
# → 0.5
```

---

## 10. 依赖环境 | Dependencies

```
Python >= 3.10
可选：jieba (中文分词)
可选：transformers + torch (BERT模型)
可选：spaCy (英文NER兜底)
```

---

## 11. DNA追溯链 | DNA Trace

```
#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-CNSH-reactor-文字识别引擎-v1.0  ← 源文件DNA
          ↓
#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGWEN-NLP-v5.0                    ← 技能包DNA
```

---

## 12. 版本历史 | Changelog

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-06-18 | 源文件创建，基础NLP框架 |
| v5.0 | 2026-06-19 | 技能包打包，标准化SKILL.md，L3定位 |
