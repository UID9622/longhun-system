# 龍魂数学公式体系 v2.0 · 接入说明

**系列 DNA：** `#龍芯⚡️20260510-MATH-FORMULA-SERIES-v2.0-UPGRADED`  
**工程接入 DNA：** `#龍芯⚡️2026-05-16-MATH-FORMULA-SERIES-ENGINE-BRIDGE-v1.0`

## 能不能用？

**可以。** 这是 UID9622 自有材料，可进龍魂生态。但：

| 层级 | 路径 | 角色 |
|------|------|------|
| **运行真源** | `engines/公式对准引擎.py` · `cnsh/gate_v3/` · `engines/dna_generator_v2.py` | 线上决策、skill、闸门 |
| **对齐表** | `cnsh-core/规范/算法公式IPA对齐总表_v1.0.md` | 公式↔IPA↔skill |
| **六公式流水线** | `cnsh/math_formula_series/pipeline.py` | 把 HTML 第六篇「LonghunEngine」接到真源 |
| **HTML 展示页** | `docs/math-formula-series/龍魂数学公式体系_v2.0.html` | **教学·对照**；与 `pipeline.py` 真源并行，见下节差异 |
| **下载源同步** | `~/Downloads/龍魂数学公式体系 · 升级版 v2.0 _ UID9622.html` | 更新展示页时覆盖拷入上格路径即可 |

## 与 HTML 的差异（必知·防叠坑）

### 1. 五行映射（第二篇）

HTML 用的是 **洛书宫位表**（如 dr1→水、dr2→木…）。

仓库 **语义真源**（公式对准表 P4、`wuxing-check` skill）是：

| dr | 真源五行 |
|----|----------|
| 1,2 | 木 |
| 3,4 | 火 |
| 5 | 土 |
| 6,7 | 金 |
| 8,9 | 水 |

`pipeline.py` 默认走 **真源**；需要宫位叙事时用参数 `mapping="luoshu_palace"`（仅展示/洛书专题，不与 skill 混用）。

### 2. 决策分 D（第四篇）

| 来源 | 公式 |
|------|------|
| HTML | `D = R × I × (1 − 0.3·risk − 0.2·bias)`，0–1，≥0.8 🟢 |
| 龍魂公式12（真源） | `D = 可执行+安全+主线+验证 − 风险 − H`，约 0–15 量纲 |

引擎里 **公式12** 走 `执行最小链()`；HTML 版 D 仅作 `decision_card_html()` 可选输出。

### 3. 数字根三色（第一篇）

与 `cnsh/gate_v3/engine.py` **一致**：dr∈{3,9}🔴 · dr=6🟡 · 其余🟢。

### 4. DNA（第五篇）

与 `engines/dna_generator_v2.py` **一致**（双视角 M:: / CNSH::）；优先调 v2，不用 HTML 里的简化 `generate_dna()`。

## 怎么用

```bash
# 六公式一条龍（真源）
python3 -m cnsh.math_formula_series.pipeline --n 9622 --content "UID9622系统自检"

# 自测
python3 -m cnsh.math_formula_series.pipeline --selftest
```

```python
from cnsh.math_formula_series.pipeline import analyze

r = analyze(9622, "行为密码学压缩真源升级", risk=0.1, bias=0.0)
print(r["dna"], r["tricolor"], r["formula12_D"])
```

## 与时间轮 / 行为密码学

- **F2 时间锚** · **E=R×I×T^(-α)** · **柱⑥ 共生时间 v2：** [`01_protocols/cnsh/PROTOCOL__SYMBIOTIC-TIME-BRIDGE-v2.0.local.md`](../../01_protocols/cnsh/PROTOCOL__SYMBIOTIC-TIME-BRIDGE-v2.0.local.md) · Notion https://www.notion.so/9c3946bfd10346ccab90fa600b49fc6e  
- **L5 分层 α 与叙事对齐：** [`01_protocols/cnsh/PROTOCOL__DNA-L5-ARCHITECTURE-v1.4.local.md`](../../01_protocols/cnsh/PROTOCOL__DNA-L5-ARCHITECTURE-v1.4.local.md)（Notion headline DNA v1.5）  
- **道德经 81 章→算法节点（叙事根）：** [`01_protocols/cnsh/PROTOCOL__DAODEJING-81-ENGINE-v1.0.local.md`](../../01_protocols/cnsh/PROTOCOL__DAODEJING-81-ENGINE-v1.0.local.md)  
- **女娲五彩石 · 主权终端 UI（五色 BSI）：** [`01_protocols/cnsh/PROTOCOL__NUWA-COLOR-TERMINAL-v1.0.local.md`](../../01_protocols/cnsh/PROTOCOL__NUWA-COLOR-TERMINAL-v1.0.local.md)  
- **公式全文 HTML v2：** [`龍魂数学公式体系_v2.0.html`](./龍魂数学公式体系_v2.0.html)（与 `pipeline.py` 差异见上）
- **压缩/展开**：`BehavCrypto_v1.0/tools/behavcrypto_dna_editor.py`  
- **十字段回执**：`public/transparent-demo/decision_receipt.example.json`

## HTML 落盘

- **仓内 canonical：** `docs/math-formula-series/龍魂数学公式体系_v2.0.html`（浏览器直接打开）。
- **从本机 Downloads 再同步（一行）：**  
  `cp "/Users/zuimeidedeyihan/Downloads/龍魂数学公式体系 · 升级版 v2.0 _ UID9622.html" "/Users/zuimeidedeyihan/longhun-system/docs/math-formula-series/龍魂数学公式体系_v2.0.html"`

**改公式只改 Python 真源 + 本 README**，再按需同步 HTML 文案（避免两套漂移）。
