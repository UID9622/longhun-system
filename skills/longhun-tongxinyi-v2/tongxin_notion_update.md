# 通心译 v2.0 | Tongxin Translation v2.0
## 逻辑哲学训练模型 | Logic-Philosophy Training Model

> **DNA**: `#龍芯⚡️2026-07-01-TONGXIN-TRANSLATION-FILE1-v2.0`
> **父DNA**: `#龍芯⚡️2026-06-19-LONGWEN-NLP-v5.0`
> **确认码**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
> **封印**: `#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL`

---

## 📌 一句话定位 | One-Line Positioning

通心译v2.0是**语义心意映射引擎**（Semantic Intention Mapping Engine），不是传统NMT。基于20条哲学观察构建七维可训练评估体系，实现"心意相通，而非字面镜像"。

---

## 🏗️ 三层语义传递 v2.0 | Tri-Layer Semantic Transfer

| 层级 | 英文名 | 功能 | 输出示例（画龍点睛）|
|------|--------|------|---------------------|
| 字面层 | Literal Layer | 术语对齐+语法映射 | to draw eyes on a dragon painting |
| 逻辑层 | Logical Layer | 语义蕴含+语篇连贯 | to add the crucial detail that brings life |
| 心意层 | Intentional Layer | 文化意图+意象映射 | to add the finishing touch [cultural annotation] |

### 层间约束 | Inter-Layer Constraints

```
字面 → 逻辑: 蕴含保持 (每個命题必须有逻辑对应)
逻辑 → 心意: 意图覆盖 (语义关系必须被文化意图覆盖)
心意 → 逻辑: 可行性检验 (文化映射必须在逻辑层可表达)
逻辑 → 字面: 可实现性 (语义结构必须找到词汇载体)
```

---

## 🔬 七维训练维度 | Seven Training Dimensions

### 维度总览

| 维度 | 英文名 | 权重 | 对应观察 | 核心指标 |
|------|--------|------|----------|----------|
| **D1** | 文化负载词 Culture Lexicon | 0.20 | #1, #2, #19 | CLS |
| **D2** | 语义-语法制约 Semantic-Syntax | 0.15 | #5, #7, #13 | SSC |
| **D3** | 古代汉语 Classical Chinese | 0.10 | #6, #14 | CCT |
| **D4** | 语篇完整性 Discourse Integrity | 0.20 | #3, #4, #8 | DIS |
| **D5** | 文明安全 Civilization Safety | 0.15 | #9, #10, #11 | CSS |
| **D6** | 创造性策略 Creative Strategy | 0.10 | #12, #17, #20 | CTS |
| **D7** | 语义精确性 Semantic Precision | 0.10 | #18 | SPC |

### 20条观察 → 七维映射

```
D1(文化负载词) ← 观察#1(文化特殊性) + #2(语义丰富性) + #19(文化差异系统性)
D2(语义-语法)  ← 观察#5(语义制约语法) + #7(语义蕴含) + #13(语义语法互作) + #15(蕴含处理)
D3(古代汉语)   ← 观察#6(古汉语复杂性) + #14(现代转换)
D4(语篇完整)   ← 观察#3(断章取义) + #4(文化适应) + #8(摘要差异) + #16(互补性)
D5(文明安全)   ← 观察#9(文化语境) + #10(综合性) + #11(译者意识)
D6(创造策略)   ← 观察#12(策略多样) + #17(实践性) + #20(创造性)
D7(语义精确)   ← 观察#18(语义精确性)
```

---

## 📊 R-Score 计算公式 | R-Score Formula

```
R = Σ(w_i × Dim_i) + α × Creativity_Bonus - β × Safety_Penalty

参数:
  w_i  = 维度权重 (见上表)
  α    = 0.1 (创造性奖励系数)
  β    = 0.5 (安全惩罚系数，高权重)
  
Creativity_Bonus = max(0, D6 - 0.8) × mean(all_dims)
Safety_Penalty   = max(0, 0.95 - D5) × 10   (D5<0.95时重罚)
```

### 质量等级

| 等级 | R-Score | 说明 | 行动 |
|------|---------|------|------|
| **S** | 0.95-1.00 | 卓越，心意完美传递 | 黄金样本 |
| **A** | 0.85-0.95 | 优秀，语义完整 | 直接使用 |
| **B** | 0.70-0.85 | 良好，有小瑕疵 | 人工审核 |
| **C** | 0.55-0.70 | 及格，明显问题 | 需修改 |
| **D** | <0.55 | 不及格，严重错误 | 重译 |

---

## 🔄 训练Pipeline | 5-Step Pipeline

```
[数据准备] → [语义标注] → [模型训练] → [七维评估] → [迭代优化]
   STEP 1      STEP 2       STEP 3       STEP 4       STEP 5
   
   语料收集     三层标注      分层训练      R-Score      哲学驱动
   知识图谱     七维评分      联合优化      质量报告      版本迭代
   质量控制     一致性校验    低算力适配    错误分析      术语更新
```

### 低算力配置

| 配置项 | 参数 |
|--------|------|
| 基础模型 | DistilBERT-small |
| 批次大小 | 16 |
| 学习率 | 2e-5(L) / 1e-5(G) / 5e-6(I) |
| 量化 | INT8 |
| 显存需求 | ≤4GB 或 CPU |

---

## 📝 训练数据格式 | Data Format

### JSON Schema (单条样本)

```json
{
  "sample_id": "TX-v2-0001",
  "source": {
    "text": "画龍点睛",
    "context": "...",
    "cultural_notes": "..."
  },
  "translation": {
    "literal_layer": {
      "text": "to draw eyes on the dragon",
      "terminology_mapping": [...],
      "confidence": 0.95
    },
    "logical_layer": {
      "text": "to add the crucial final detail",
      "semantic_entailments": [...],
      "confidence": 0.92
    },
    "intentional_layer": {
      "text": "to add the finishing touch",
      "cultural_intention": "...",
      "civilization_safety_score": 95,
      "confidence": 0.88
    }
  },
  "annotations": {
    "dimension_scores": {
      "D1": 0.95, "D2": 0.80, "D3": 0.70,
      "D4": 0.90, "D5": 0.90, "D6": 0.85, "D7": 0.90
    },
    "overall_score": 0.91
  }
}
```

---

## 🐍 Python 核心类 | Core Classes

```python
# 通心译评估器 - 可直接运行
class TongxinEvaluator:
    def __init__(self, weights=None, alpha=0.1, beta=0.5):
        self.weights = weights or DIMENSION_WEIGHTS
        self.alpha = alpha      # 创造性奖励
        self.beta = beta        # 安全惩罚
    
    def evaluate(self, output: TranslationOutput) -> TranslationOutput:
        """七维评估 + R-Score计算 + 等级判定"""
        scores = self._calculate_dimension_scores(output)
        output.r_score = self._calculate_r_score(scores)
        output.quality_grade = self._determine_grade(output.r_score)
        return output
    
    def generate_report(self, output) -> str:
        """生成质量报告（七维雷达 + 改进建议）"""
        ...
```

**完整代码**: `tongxin_evaluator.py`（可独立运行，零依赖除numpy）

---

## 📈 评估指标 | Evaluation Metrics

| 类别 | 指标 | 说明 |
|------|------|------|
| 基础NMT | BLEU, chrF, TER | 参考指标，权重0.25 |
| 七维评分 | CLS, SSC, CCT, DIS, CSS, CTS, SPC | 核心指标，权重0.75 |
| 综合指标 | **R-Score** | 最终质量分数 |
| 等级指标 | S/A/B/C/D | 质量分级 |

---

## 🔑 关键洞察 | Key Insights

**洞察A**: 所有20条观察指向一个核心问题——翻译中的"信息分层"问题。字面信息丢失最少，心意信息丢失最多。

**洞察B**: 语义制约语法（观察5、13）是中文特有的结构性挑战，必须作为独立训练维度(D2)。

**洞察C**: 95-5%文明安全定律（观察9）意味着翻译模型必须有文化风险评估机制(D5)。

**洞察D**: 古代汉语→现代汉语→外语的三跳转换（观察6、14）需要历史语义知识图谱支持(D3)。

---

## 📎 五大铁律 v2.0 | Five Translation Iron Laws

| 铁律 | v2.0实现 | 关联维度 |
|------|----------|----------|
| 中文活着 | 心意层优先，字面层校验 | D6 |
| 不是镜像 | 七维评分替代1:1对应 | D1, D4 |
| 比喻优先 | 意象映射模块 | D1, D6 |
| 古今打通 | 古汉语知识图谱+三跳转换 | D3 |
| 永远迭代 | 哲学输入驱动迭代优化 | 全部 |

---

## 📚 相关文件 | Related Files

| 文件 | 说明 |
|------|------|
| `tongxin_translation_v2_spec.md` | 完整模型规范（本文详细版） |
| `tongxin_train_template.json` | 20条训练样本（覆盖7维度） |
| `tongxin_evaluator.py` | Python评估器（可独立运行） |
| `tongxin_notion_update.md` | Notion格式更新（本文档） |

---

*通心译v2.0 — 心意相通，而非字面镜像*
*龍魂体系 · 诸葛芯 · 2026*

---

**DNA追溯链**:
```
本文件:    #龍芯⚡️2026-07-01-TONGXIN-TRANSLATION-v2.0
父文件:    #龍芯⚡️2026-06-19-LONGWEN-NLP-v5.0
确认码:    #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
封印:      #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
```
