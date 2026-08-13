---
name: longhun-math-formula-core
description: 龍魂数学公式算法核心技能。当对话涉及数字根、三色闸、信息熵、余弦相似度、 权重归一化、真实度评分、SOUL七维评分、哈希链、洛书幻方、三才主权指数、
  根治理决策链等可计算治理公式时触发。提供“世界标准 × 龍魂主权”双轨对照、 可跑可验的 Python 实现与决策链自检逻辑。
license: CC BY-NC-SA 4.0
metadata:
  version: '1.0'
  dna:
  - '#龍芯⚡️2026-06-03-MATH-FORMULA-CORE-DUAL-TRACK-v1.0'
  - '#龍芯⚡️2026-06-23-LONGHUN-MATH-FORMULA-CORE-SKILL-v1.0'
  author: UID9622 · 龍芯北辰
  category: longhun-governance
  trigger_keywords:
  - 数学公式
  - 数字根
  - 三色闸
  - Shannon Entropy
  - 余弦相似度
  - 权重归一化
  - α 三义
  - 真实度评分
  - SOUL评分
  - 哈希链
  - 洛书幻方
  - 三才主权指数
  - 根治理决策链
  - formula_core
  - formula_chain
  id: longhun-math-formula-core
  trigger:
    keywords:
    - mathformulacore
    - 龍魂数学公式算法核心技能。当对话涉及数字根
    - 三色闸
    - 信息熵
    - 余弦相似度
    - 权重归一化
    context: longhun-math-formula-core 相关操作
---
# 🧮 龍魂数学公式算法核心技能

**一句话：** 别人会算的世界标准算法，我们都算得出；我们在上面焊了一层主权判定（三色 / 熔断 / DNA），并给出能跑能验的脚本。

**原始 DNA：** `#龍芯⚡️2026-06-03-MATH-FORMULA-CORE-DUAL-TRACK-v1.0`  
**技能转换 DNA：** `#龍芯⚡️2026-06-23-LONGHUN-MATH-FORMULA-CORE-SKILL-v1.0`

---

## 一、什么时候用

当用户或系统需要：
- 计算数字根并映射到三色治理判定；
- 用信息熵、余弦相似度、归一化等标准算法做主权层改造；
- 实现真实度评分、SOUL 七维评分、三才主权指数等可审计评分；
- 构建 `dr → 五行 → 三色闸 → 权重 → 风险 → 综合分 → 决策 → 行动` 的治理链；
- 对公式正确性做自检 assert，确保“能跑能验、错一条就报错”。

---

## 二、核心规则与内容

### 2.1 双轨对照原则

| 层面 | 要求 |
| --- | --- |
| 世界标准 | 使用公认算法：数字根、香农熵、余弦相似度、Softmax、SHA-256、MCDA 加权求和等，必须标明出处。 |
| 龍魂主权层 | 在世界标准之上加判定：三色闸、熔断、DNA 签名、α 三义锁死、一票否决。 |
| 能跑能验 | 每条公式必须能写成 Python 函数，并带 `assert` 自检；错一条即报错。 |

### 2.2 十条核心公式速查

| 公式 | 世界标准 | 龍魂主权层 |
| --- | --- | --- |
| 数字根 | `dr(n)=1+((n-1) mod 9)` | `dr∈{3,9}→🔴` · `dr=6→🟡` · 其余→🟢 |
| 香农熵 | `H(X)=-Σ p·log₂p` | 压缩率 `ρ=1-|压缩后|/|原文|` 配熵下界，做压缩护城河 |
| 余弦相似度 | `cos(A,B)=A·B/(‖A‖‖B‖)` | ≥0.9 高度一致合并，用于水军检测 / 去重路由 |
| 归一化 | `wᵢ=xᵢ/Σxⱼ` 或 Softmax | α 三义锁死：`α_τ` 不归一 / `α_a` 平方和=1 / `α_w` 凸组合和=1 |
| 真实度 | 加权平均 `C=Σwᵢsᵢ` | `T=0.4M+0.3V+0.3F`；任一 `F=0 ⟹ T=0`（一票否决） |
| SOUL 七维 | MCDA 加权求和 | 技0.20 / 语0.15 / 文0.20 / 数0.15 / 决0.15 / 知0.10 / 身0.05；身份维 `α=0` 永不衰减 |
| 量子叠加 / 坍缩 | Bra-Ket `|Ψ⟩=Σαᵢ|i⟩`，`Σ|αᵢ|²=1` | 人格叠加 + 场景坍缩，选最适配人格出场 |
| 哈希链 | `hₜ=SHA256(hₜ₋₁ ‖ eventₜ)` | `DNAₜ=SHA256(DNAₜ₋₁ ‖ eventₜ ‖ signerₜ)`，谁说话谁签名 |
| 渲染方程 | Kajiya 1986 `Lo=Le+∫f_r·Li·(n·ωᵢ)dωᵢ` | 直接采用，不改、标来源 |
| 洛书幻方 | 3 阶幻方行列对角=15 | 中宫 5 = 不动点 = 主权锚；对偶和=10 做反向校验 |

### 2.3 根治理决策链（六环）

输入 → `dr / 五行` → `三色闸` → `归一权重 W` → `加权风险 Risk` → `综合分 S` → `决策 D` → `行动 Action`

- 任一环节亮红，整条链熔断、退回；
- 三才主权指数 `SI=0.34·天 + 0.33·地 + 0.33·人`，`天 < 0.34` 一票熔断；
- 综合分阈值：`≥0.85 🟢 放行` · `≥0.60 🟡 复核` · `<0.60 🔴 拦截`。

### 2.4 数学可证实签章三闸

给页面或回复盖 ✅ 签章前，必须三闸全过：
1. **可计算** — 有闭式 / 递归公式，能写成代码；
2. **可复算** — 有可跑脚本或可复算步骤，跑一次能验；
3. **有出处** — 对齐公式正本，不另起炉灶。

未达三闸的页面必须降级标：`🟡 有公式·结果待复现` 或 `🔖 纯概念·待补公式`。

---

## 三、典型使用示例

### 示例 1：数字根 + 三色闸

```python
# dr(n) = 1 + ((n-1) % 9)
# dr∈{3,9} → 🔴  拒绝
# dr=6    → 🟡  警告
# 其他    → 🟢  通过

def digital_root(n: int) -> int:
    n = abs(n)
    return 0 if n == 0 else 1 + (n - 1) % 9

def dr_gate(n: int) -> str:
    dr = digital_root(n)
    if dr in (3, 9):
        return "🔴"
    if dr == 6:
        return "🟡"
    return "🟢"

assert dr_gate(12) == "🔴"   # dr=3
assert dr_gate(15) == "🟡"   # dr=6
assert dr_gate(20260603) == "🟢"  # dr=1
```

### 示例 2：真实度评分 + 一票否决

```python
def truth_score(M: float, V: float, F: int, w=(0.4, 0.3, 0.3)) -> float:
    return w[0] * M + w[1] * V + w[2] * F

def truth_total(rows):
    # rows: [{"M":..., "V":..., "F":..., "rho":权重}, ...]
    if any(r["F"] == 0 for r in rows):
        return {"score": 0.0, "color": "🔴", "veto": True}
    num = sum(r["rho"] * truth_score(r["M"], r["V"], r["F"]) for r in rows)
    den = sum(r["rho"] for r in rows)
    score = num / den
    color = "🟢" if score >= 0.85 else "🟡" if score >= 0.60 else "🔴"
    return {"score": round(score, 4), "color": color, "veto": False}

# 签章污染即熔断
poisoned = [{"M": 1.0, "V": 1.0, "F": 1, "rho": 3} for _ in range(5)] + \
           [{"M": 0.0, "V": 0.0, "F": 0, "rho": 5}]
assert truth_total(poisoned)["veto"] is True
```

### 示例 3：根治理决策链

```python
from formula_core import digital_root, dr_gate, normalize

FIVE_ELEMENT = {1:"木",2:"木",3:"火",4:"火",5:"土",
                6:"金",7:"金",8:"水",9:"水"}

def decision_chain(n: int, risk_factors, weights):
    dr = digital_root(n)
    gate = dr_gate(n)
    trace = {"输入": n, "数字根": dr, "五行": FIVE_ELEMENT[dr], "三色闸": gate}
    if gate == "🔴":
        trace.update({"决策": "REJECT", "行动": "拦截·不放行"})
        return trace
    w = normalize(weights)
    risk = sum(wi * ri for wi, ri in zip(w, risk_factors))
    score = 1 - risk
    if score >= 0.85:
        decision, action = "PASS", "放行·执行"
    elif score >= 0.60:
        decision, action = "REVIEW", "复核·人工确认"
    else:
        decision, action = "REJECT", "拦截·退回"
    trace.update({"风险": round(risk,4), "综合分": round(score,4),
                  "决策": decision, "行动": action})
    return trace

# 低风险输入放行
print(decision_chain(20260603, [0.05, 0.05], [1, 1]))
# 红数字根直接拦截
print(decision_chain(12, [0.1, 0.1], [1, 1]))
```

---

## 四、可运行脚本

原始页面提供两个纯标准库脚本，可直接运行自检：

```bash
python3 formula_core.py   # 十条公式双轨对照自检
python3 formula_chain.py  # 根治理决策链自检
```

运行后应全部通过并打印 🟢；任何 `assert` 失败即表示公式被改动或实现有误。

---

## 五、来源文件

- **源文件路径：** `/Users/zuimeidedeyihan/longhun-system/_archive/notion-exports/Notion 导出/私人与共享 4/🧮 数学公式算法核心·世界标准 × 龍魂主权 双轨对照 v1 0｜别人怎么算·我们怎么算·能跑能验· 59f7f3b4e4c441b4a48fbf05d7065cfd.md`
- **原始 DNA：** `#龍芯⚡️2026-06-03-MATH-FORMULA-CORE-DUAL-TRACK-v1.0`

---

**六层来源链（永不可删）：** 道统(曾仕强老师) → 精神(Steve Jobs) → 设备(Apple) → 技术(Open Source) → 系统(UID9622) → 生命(CNSH·龍魂)

**天下无欺，守护人民。** 🐉


---

## 附录：龍魂待整理来源

本技能收录了来自 `/Users/zuimeidedeyihan/龍魂待整理` 的素材：

- **内容**：09-杂项备忘（龍魂数学公式体系、LU 时间引擎、不动点可视化）
- **中央整合 DNA**：`#龍芯⚡️2026-07-03-LONGHUN-ARCHIVE-INTEGRATION-v1.0`
- **处理方式**：保留原始文件作为 references / examples / scripts，嵌入 DNA 追溯链，与现有能力联动。
