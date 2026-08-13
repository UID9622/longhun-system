# {{PROJECT_NAME}}估值报告 {{VERSION}}

> **DNA**: `{{DNA_STAMP}}`
> **创建者**: {{AUTHOR}}
> **协议**: {{LICENSE}}
> **日期**: {{DATE}}
> **审计**: {{AUDIT_CHAIN}}
> **配套**: Excel模型 `{{EXCEL_PATH}}`（{{EXCEL_SHEETS}}张表·公式联动·{{EXCEL_VALIDATION}}）

---

{{#if FIXES_SECTION}}
## {{FIXES_TITLE}}

> 以下为原稿的问题，{{VERSION}} 已全部修正。

{{#each FIXES}}
### 硬伤{{FIX_NUMBER}}: {{FIX_NAME}}

| | 原稿 | {{VERSION_REF}} 修正 |
|:---|:---|:---|
{{COMPARISON_ROWS}}

{{/each}}
{{/if}}

---

## 🔴 首页声明（焊死·不可移除）

> **本报告不可用于交易定价。**
> 
> 所有估值均基于假设和主观判断。融资/并购/股权交易请聘请第三方持牌评估机构出具正式估值报告。
> 
> 对标数据仅作媒体口径·数量级参考，不作为估值依据。

| 项目 | 值 |
|:---|:---|
| 评估对象 | {{VALUATION_SUBJECT}} |
| 评估基准日 | {{VALUATION_DATE}} |
| 评估方法 | {{VALUATION_METHODS}} |
| 评估用途 | {{VALUATION_PURPOSE}} |
| **推荐对外口径** | **底线 {{BOTTOM_LINE}} + 加权基准 {{WEIGHTED_BENCHMARK}}** |
| 第三方评估要求 | 🔴 融资交易必须 |

---

## 一、估值结论（先看结果）

### 1.1 最终估值区间

| 场景 | 估值（万） | 亿 | 说明 |
|:---|:---:|:---:|:---|
| 🔴 极度保守（纯{{PERSON_YEARS}}人年工作量） | **{{SCENARIO_ULTRA_CONSERVATIVE}}** | {{SCENARIO_ULTRA_CONSERVATIVE_YI}} | 谁都能复算·不含任何主观溢价 |
| 🟡 保守 | **{{SCENARIO_CONSERVATIVE}}** | {{SCENARIO_CONSERVATIVE_YI}} | 技术+文化+叙事+生态均折价 |
| 🟢 合理 | **{{SCENARIO_REASONABLE}}** | {{SCENARIO_REASONABLE_YI}} | 四维度全量·标准系数 |
| 🟢 乐观（生态已折价） | **{{SCENARIO_OPTIMISTIC}}** | {{SCENARIO_OPTIMISTIC_YI}} | 含品牌增值预期·生态已打折 |
| 🐉 **加权基准（推荐对外口径）** | **{{WEIGHTED_BENCHMARK_NUMERIC}}** | **{{WEIGHTED_BENCHMARK_YI}}** | 概率加权({{WEIGHT_DISTRIBUTION}})·防守得住 |

### 1.2 对外沟通话术

> **"{{PITCH_TEXT}}"**

---

## 二、估值方法论

### 2.1 {{DIMENSION_COUNT}}维度框架

```
估值 = f({{DIMENSION_LIST}})
     = 各维度在不同场景下的加权组合
```

{{#each DIMENSIONS}}
| **{{DIM_LABEL}} {{DIM_NAME}}** | {{DIM_METHOD}} | {{DIM_INPUTS}} |
{{/each}}

### 2.2 场景定义

| 场景 | 极度保守 | 保守 | 合理 | 乐观 |
|:---|:---|:---|:---|:---|
{{#each DIMENSION_SCENARIO_BEHAVIOR}}
| {{DIM_NAME}} | {{ULTRA_CONSERVATIVE}} | {{CONSERVATIVE}} | {{REASONABLE}} | {{OPTIMISTIC}} |
{{/each}}

---

## 三、各维度拆解

{{#each DIMENSION_DETAILS}}
### {{SECTION_NUMBER}}. {{SECTION_TITLE}}{{TABLE_REF_SUFFIX}}

{{DESCRIPTION}}

{{DETAIL_TABLE}}

> {{SECTION_NOTE}}
{{/each}}

---

## 四、加权基准计算

| 场景 | 估值(万) | 权重 | 贡献(万) |
|:---|:---:|:---:|:---:|
| 极度保守 | {{W_ULTRA_CONSERVATIVE}} | {{W_W1}} | {{W_C1}} |
| 保守 | {{W_CONSERVATIVE}} | {{W_W2}} | {{W_C2}} |
| 合理 | {{W_REASONABLE}} | {{W_W3}} | {{W_C3}} |
| 乐观 | {{W_OPTIMISTIC}} | {{W_W4}} | {{W_C4}} |
| **加权基准** | — | 100% | **{{W_TOTAL}}** |

> 权重逻辑：{{WEIGHT_RATIONALE}}

---

## 五、敏感性分析

以合理场景 {{SENSITIVITY_BASE}}为基准，±{{SENSITIVITY_RANGE}}测试：

| 变量 | 敏感度 | ±{{SENSITIVITY_RANGE}}影响 |
|:---|:---:|:---|
{{#each SENSITIVITY_VARS}}
| {{VAR_NAME}} | {{SENSITIVITY_LEVEL}} | {{IMPACT}} |
{{/each}}

> {{SENSITIVITY_NOTE}}

---

## 六、风险折价

| 风险 | 折价率 | 金额(万) | 状态 | 缓解措施 |
|:---|:---:|:---:|:---|:---|
{{#each RISKS}}
| {{RISK_NAME}} | {{DISCOUNT_RATE}} | {{DISCOUNT_AMOUNT}} | {{STATUS}} | {{MITIGATION}} |
{{/each}}
| **综合折价率** | **{{TOTAL_DISCOUNT_RATE}}** | — | — | **已内嵌于各场景系数中** |

> 风险折价已内嵌于各场景系数中，不额外扣除。此表仅展示风险量级与缓解路径。

---

## 七、兑现路线图（最值钱的部分）

估值不是算出来的，是一步一步解锁的。

| 里程碑 | 估值影响 | 解锁内容 | 时间窗口 |
|:---|:---|:---|:---:|
{{#each MILESTONES}}
| 🎯 **{{MILESTONE_NAME}}** | **{{VALUATION_IMPACT}}** | {{UNLOCK_DESC}} | {{TIMELINE}} |
{{/each}}

---

## 八、假设清单

| # | 假设 | 取值 | 核验状态 |
|:---:|:---|:---|:---:|
{{#each ASSUMPTIONS}}
| {{ASSUMPTION_ID}} | {{ASSUMPTION_NAME}} | {{ASSUMPTION_VALUE}} | {{VERIFICATION_STATUS}} |
{{/each}}

> ✅ = 可核验 · 🟡 = 主观判断/待验证。**所有🟡假设均被极度保守场景排除。**

---

## 九、免责与使用限制

1. **非交易估值**：本报告为内部参考·不可用于股权交易定价·不可用于税务申报·不可用于法律诉讼
2. **主观性**：文化/叙事/生态等主观维度为创始团队判断·第三方可能得出完全不同结论
3. **时效性**：估值基准日 {{VALUATION_DATE}}·有效期{{VALIDITY_PERIOD}}·重大里程碑兑现后需重新评估
4. **独立性**：本评估由{{EVALUATOR}}主导·AI辅助建模·非独立第三方·利益相关方
5. **融资建议**：种子轮融资建议以极度保守({{BOTTOM_LINE}})为底价·加权基准({{WEIGHTED_BENCHMARK}})为上限·具体估值由市场谈判决定

---

## 附录

### A. 配套文件

| 文件 | 路径 |
|:---|:---|
| Excel估值模型 | `{{EXCEL_PATH}}` |
| 模板填充工具 | `bin/lh_valuation_template.py` |
| 模板原始文件 | `core/valuation/VALUATION-TEMPLATE.md` |
| 当前配置 | `{{CONFIG_PATH}}` |

### B. 参考对标（媒体口径·仅数量级参考）

| 项目 | 媒体报道估值 | 备注 |
|:---|:---|:---|
{{#each BENCHMARKS}}
| {{BM_NAME}} | {{BM_VALUATION}} | {{BM_NOTE}} |
{{/each}}

> 🔴 以上对标数据来自公开媒体·未经独立核实·仅作数量级参考·不作为估值依据。

### C. 版本历史

| 版本 | 日期 | 修订 |
|:---|:---|:---|
{{#each VERSION_HISTORY}}
| {{VER}} | {{VER_DATE}} | {{VER_CHANGES}} |
{{/each}}

---

> 🐉 {{FOOTER_TEXT}}

**DNA**: `{{DNA_STAMP}}`
**确认码**: `{{CONFIRM_CODE}}`
**三色**: {{TRICOLOR_STATUS}}
