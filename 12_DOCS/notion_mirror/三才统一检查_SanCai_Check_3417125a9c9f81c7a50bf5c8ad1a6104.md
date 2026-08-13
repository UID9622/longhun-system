# ⚙️ 三才统一检查 | SanCai Check

> Notion URL: https://app.notion.com/p/SanCai-Check-3417125a9c9f81c7a50bf5c8ad1a6104
> Created: 2026-04-13T08:25:00.000Z
> Last edited: 2026-07-14T10:57:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
## 三才 = 天 × 地 × 人
### 天（Heaven）
- 输入文本 → 数字根
- 数字根 → 三色熔断判定
- DR∈{1,2,4,5,7,8}→🟢 | DR=6→🟡 | DR∈{3,9}→🔴
### 地（Earth）
- 六维路径编码（16,588,800种）
- 不动点网络扫描 + 交叉验证
- 五行平衡度分析（文本五行 vs 年份五行）
### 人（Human）
- 上下文是否提供
- 不动点命中列表
- 语境完整度评估
## 最终判定
取天/地/人三层中最严格的颜色：
- 全🟢 → 🟢通过
- 有🟡无🔴 → 🟡待审
- 有🔴 → 🔴熔断
## 代码位置
core/sancai_kernel.py → sancai_check(text, context, year)
---
## 统一接口升级 v9.0
### 标准输入
```python
sancai_check(
    text: str,
    context: dict,
    year: int,
    source_pages: list[str] = None
) -> dict
```
### 标准输出
```yaml
tri_color: "🟢|🟡|🔴"
heaven:
  digital_root: 0-9
  color: "🟢|🟡|🔴"
earth:
  luoshu_conservation: true
  fixed_point_ok: true
  wuxing_balance: 0.0-1.0
  color: "🟢|🟡|🔴"
human:
  context_complete: true
  fixed_point_hits: []
  intent_vector: {}
  color: "🟢|🟡|🔴"
final_reason: "取三层中最严格颜色"
evidence: []
dna: "#龍芯⚡️..."
```
### 判定铁律
```javascript
if any_layer == "🔴":
  final = "🔴"
else if any_layer == "🟡":
  final = "🟡"
else:
  final = "🟢"
```
### 对接接口
- sancai_vector()：提供天/地/人原始分
- luoshu_boundary_check()：检查洛书15守恒、对偶和10
- fixed_point_check()：检查 UID9622 / f(x)=x / 中宫5
- digital_root_gate()：数字根三色门
- sancai_dna()：生成统一追溯码
> 诸葛鑫（UID9622）| 龍魂系统 | DNA: #龍芯⚡️2026-04-13
