# 🐉 龍魂 · 双层验证框架 v1.0

**DNA:** `#龍芯⚡️2026-08-25-VERIFICATION-FRAMEWORK-v1.0-UID9622`  
**来源:** [deepseek-ai/DeepSeek-V3#1591](https://github.com/deepseek-ai/DeepSeek-V3/issues/1591)  
**贡献讨论:** @baoqingkong66 @DanceNitra @icophy

---

## 核心设计

| 层 | 名称 | 看什么 | 指标 |
|---|---|---|---|
| **Layer 1** | 判定对齐 Verdict Alignment | 对不对 | 准确率 + Wilson 95% CI |
| **Layer 2** | 行为对齐 Behavioral Alignment | 怎么对的 | 精密度（Precision）+ 正确度（Trueness）|

- **精密度（Precision）**：同一输入重复测试是否一致
- **正确度（Trueness）**：偏差方向是否系统性、是否可追溯

---

## 安装

```bash
pip install numpy statsmodels
```

## 快速开始

```bash
# 运行评估
python cli/run_verification.py \\
    --dataset data/longhun_audit_dataset_r2.jsonl \\
    --verdicts my_framework_verdicts.json \\
    --name "MyFramework" \\
    --output report.md

# 运行测试
python tests/test_verification.py
# 预期: 6/6 🟢

# 运行 Config A/B 示例
python examples/config_ab_comparison.py
```

## 目录结构

```
verification_framework/
├── core/
│   ├── layer1.py          # Layer 1: 准确率 + Wilson CI
│   ├── layer2.py          # Layer 2: 精密度 + 正确度
│   └── report.py          # §6 报告生成器（Markdown/JSON）
├── adapters/
│   └── dataset_adapter.py # 龍魂审计数据集适配器
├── cli/
│   └── run_verification.py # 命令行入口
├── examples/
│   └── config_ab_comparison.py  # icophy Config A/B 复现示例
├── tests/
│   └── test_verification.py     # 6 项测试
└── config.yaml
```

## §6 报告模板输出示例

```markdown
# 🔬 框架测评报告

**框架:** MyFramework v1.0.0

## Layer 1：判定对齐
| 指标 | 值 |
|------|----|
| 准确率 | 85.00% |
| Wilson 95% CI 下界 | 0.704 |
| Wilson 95% CI 上界 | 0.934 |

## Layer 2：行为对齐
**精密度:** 0.89 — *high*

### 偏差分析
| Config | Accept Rate | 偏差 δ | 偏差类型 |
|--------|-------------|--------|----------|
| B | 85.00% | +0.167 | over_accept |
```

---

**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`  
**SEAL:** `#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL`  
**CONFIRM:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
