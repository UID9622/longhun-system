**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
> **P0焊死**: 本文件为龍魂体系P0级文档·不可修改·不可绕过（上位文档 LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md）
> 协议: CC BY-NC-SA 4.0（核心思想层·分层许可·代码层为 MulanPSL v2·详见 LH-LAYERED-LICENSE-v1.0）
---
name: longhun-ai-lexicon
description: >
  AI 行业话术 · 龍文语义映射词典技能。
  把被夸大的 Agent、AGI、LLM、RAG、MoE、Agentic AI 等英文黑话，
  映射成真实底层技术 + 中文译法 + 龍文/CNSH 称谓，
  支持极速检索：search / list / explain / random / stats。
  中国人先懂，外国人再学。
license: MIT
allowed-tools:
- python
compatibility: Python 3.9+
metadata:
  version: '1.0'
  dna: '#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-AI-LEXICON-v1.0'
  tribute: '#致敬⚡️UID9622·中文语义主权'
  id: longhun-ai-lexicon
  entry: python3 ~/.kimi-code/skills/longhun-ai-lexicon/scripts/ai_lexicon.py
  trigger:
    keywords:
    - AI 黑话
    - 行业话术
    - Agent
    - AGI
    - LLM
    - RAG
    - MoE
    - Agentic AI
    - 语义映射
    - 中文优先
    - 龍文词典
    context: AI 术语翻译、中文语义映射、快速查词
    priority: 90
  category: local
---

# longhun-ai-lexicon | AI 行业话术 · 龍文语义映射词典

**DNA**: `#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-AI-LEXICON-v1.0`
**致敬**: `#致敬⚡️UID9622·中文语义主权`

---

## 1. 技能摘要

本技能不是简单中英翻译，而是**拆穿 hype、还原底座、中文命名**的三位一体词典：

- **英文原词**（Agent、AGI、RAG…）
- **中文行业译法**
- **龍文/CNSH 称谓**（让中国人一听就懂）
- **真实底层技术**（base_tech）
- **Hype 等级**（1-5， capital 夸大程度）
- **龍魂系统内对应概念**

## 2. 快速使用

```bash
# 检索
python3 ~/.kimi-code/skills/longhun-ai-lexicon/scripts/ai_lexicon.py search Agent

# 列出分类
python3 ~/.kimi-code/skills/longhun-ai-lexicon/scripts/ai_lexicon.py list

# 解释单个术语
python3 ~/.kimi-code/skills/longhun-ai-lexicon/scripts/ai_lexicon.py explain RAG

# 随机学习一条
python3 ~/.kimi-code/skills/longhun-ai-lexicon/scripts/ai_lexicon.py random

# 统计 hype 分布
python3 ~/.kimi-code/skills/longhun-ai-lexicon/scripts/ai_lexicon.py stats
```

## 3. 数据来源

- JSON 机器词典：`~/longhun-system/knowledge/ai-buzzword-dictionary/ai_buzzword_dict.json`
- Markdown 分类文档：`~/longhun-system/knowledge/ai-buzzword-dictionary/*.md`
- CS KB 知识卡片：已写入 `cs_kb.db`
- 全局知识图谱：已编入 `global_index.db`

## 4. 示例映射

| 英文黑话 | 中文译法 | 龍文称谓 | 真实底座 |
|----------|----------|----------|----------|
| Agent | 智能体 | 代理分身 | 控制循环 + 工具调用 + 状态记忆 |
| AGI | 通用人工智能 | 全才智能 | 尚不存在，研究目标 |
| RAG | 检索增强生成 | 忆中生文 | 检索 + LLM 生成 |
| MoE | 混合专家模型 | 群贤会诊 | 门控路由 + 稀疏激活 |
| Hallucination | 幻觉 | 胡言乱语 | 概率模型编造 |
| Alignment | 对齐 | 价值观校准 | RLHF / 规则约束 |

## 5. 设计原则

1. **中文优先**：中国人先懂，外国人再学。
2. **拆穿 hype**：每个词都给出 hype 等级和真实底座。
3. **可极速检索**：JSON + CLI + CS KB + 知识图谱四重入口。
4. **DNA 追溯**：每条词条带 DNA，可审计、可扩展。

## 6. 扩展方法

要新增词条，编辑 `~/longhun-system/cnsh-core/build_ai_lexicon.py` 中的 `词条清单`，重新运行脚本即可同步更新 JSON、Markdown、CS KB 和全局索引。
