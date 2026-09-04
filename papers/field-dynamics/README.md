# 🐉 Field Dynamics · 场域动力学统一视角

> **跨框架逻辑审计的统一观测协议** —— U/D/A/H 四维轨迹追踪 + FHI 场域健康度指数 + 可证伪假设 H1-H4

![CI](https://github.com/UID9622/field-dynamics/actions/workflows/ci.yml/badge.svg)
![License: MulanPSL v2 (code) / CC BY-NC-SA 4.0 (ideas)](https://img.shields.io/badge/License-MulanPSL%20v2%20%2B%20CC%20BY--NC--SA%204.0-blue)
![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-brightgreen)
![Zero Dependency](https://img.shields.io/badge/dependencies-0-orange)

**English**: A cross-framework unified observation protocol for runtime logic auditing. Four independently-developed frameworks (TLAA, TAT/Triplenet, Cophy, HeartFlow) observed the same phenomenon from different dimensions: *"field health" evolution of AI systems is observable, quantifiable, and predictable*. This repo formalizes that community insight (origin: [deepseek-ai/DeepSeek-V3#1466](https://github.com/deepseek-ai/DeepSeek-V3/issues/1466)) into a falsifiable framework — **U/D/A/H 4-dimension tracking + FHI index + hypotheses H1-H4 + standard log schema + zero-dependency evaluator**. Everything is runnable locally: `python3 evaluator/gen_sample_log.py --n 1000 && python3 evaluator/evaluator.py --log sample-log.jsonl --crash-window 300`.

DNA: #龍芯⚡️丙午·丙申·乙丑·壬午·䷨损-FIELD-DYNAMICS-DELIVERY-v1.0
创建者: 诸葛鑫（UID9622）
分层许可: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

---

## 为什么有这个项目

TLAA、TAT/Triplenet、Cophy、HeartFlow —— 四个**独立开发**的运行时逻辑审计框架，从不同时间、不同方向观测到了同一现象：

> **AI 系统长周期运行中的"场域健康度"演化是可观测、可量化、可预警的客观规律。**

本项目把这场社区讨论（源自 [deepseek-ai/DeepSeek-V3#1466](https://github.com/deepseek-ai/DeepSeek-V3/issues/1466)）沉淀为**可复算、可证伪、可迭代的统一理论**：四个框架不是竞争方案，而是同一规律在不同维度上的四个投影。

## 核心概念（60 秒速览）

| 维度 | 名称 | 观测什么 | 时间尺度 | 代表框架 |
|:---:|:---|:---|:---|:---|
| **U** | 统一性 | 行为与身份声明的对齐度 | 月级 | Cophy |
| **D** | 发展性 | 规则集对环境的适应速度 | 周级 | HeartFlow / TLAA |
| **A** | 对抗性 | 多路判断的分歧程度 | 天级 | TAT/Triplenet |
| **H** | 和谐度 | 叙事连续与遗忘-保持平衡 | 断裂不可逆 | TLAA / Cophy |

**FHI 指数**：`FHI(t) = wU·Û + wD·D̂ + wA·(1-Â) + wH·Ĥ`（默认等权 0.25）

**四条可证伪假设**：
- **H1 阈值收敛**：0.3 分歧阈值是跨系统同一常数
- **H2 低对抗性僵死**：A=0 掩盖语言层细微退化，是最危险前兆
- **H3 维度互补**：无单一框架能在全维同时领先
- **H4 前兆可观测**：翻转点在崩溃前存在 ≥1 个可观测窗口

## 快速开始

```bash
# 1. 跑内置冒烟测试（验证管线）
python3 evaluator/evaluator.py --self-test

# 2. 生成 1000 条示例日志（开箱即测 · 含 2 个标注翻转点）
python3 evaluator/gen_sample_log.py --n 1000

# 3. 评测示例日志（真实输出见 RESULTS.md）
python3 evaluator/evaluator.py --log sample-log.jsonl --crash-window 300

# 4. 评测自己的标准测试日志
python3 evaluator/evaluator.py --log your-log.jsonl \
  --weights 0.25,0.25,0.25,0.25 \
  --threshold 0.3 \
  --crash-window 300
```

> 真实示例评测结果：**零漏报 · 提前 196 事件预警 · FPR 11.9%**（详见 [RESULTS.md](RESULTS.md)）。评测器不粉饰，把"提前预警 vs 误报"的真实 trade-off 完整暴露 —— 这正是跨框架验证要解决的问题。

## 仓库结构

```
field-dynamics/
├── PROPOSAL.md                    # 完整提案（U/D/A/H 形式化 + 验证路线）
├── README.md                      # 本文件
├── RESULTS.md                     # 示例日志真实评测结果
├── sample-log.jsonl               # 1000 条示例日志（开箱即测）
├── schema/
│   └── field-dynamics-log.schema.json   # 标准测试日志 JSON Schema
├── evaluator/
│   ├── evaluator.py               # 统一评测器（FHI + Δt/FPR/FNR/F1）
│   └── gen_sample_log.py          # 示例日志生成器（可复现）
├── docs/
│   ├── AUDIT-THREE-COLOR.md       # 三色审计报告
│   ├── AUDIT-DUAL.md              # 左右互搏审计报告
│   └── VALIDATION-PROTOCOL.md     # 跨框架验证协议
├── .github/workflows/ci.yml       # CI：零依赖冒烟 + 评测断言 + schema 合规
├── CONTRIBUTING.md                # 贡献指南
├── CODE_OF_CONDUCT.md             # 贡献者公约
├── SECURITY.md                    # 安全政策
├── LICENSE                        # 分层许可证
└── .gitignore
```

## 我的框架怎么接入（3 步）

1. **导出日志**：把框架的审计/分歧/拦截记录按 `schema/` 导出为 JSONL（公共字段必填，私有字段放 `extensions`）
2. **跑评测**：`python3 evaluator/evaluator.py --log my-framework.jsonl`
3. **提交结果**：在仓库开 PR，附上评测 JSON + 维度归因说明（模板见 `docs/VALIDATION-PROTOCOL.md`）

> 核心指标必须能从公共字段计算 —— 这是"比谁更准"升级为"看清各自擅长哪一维"的前提。

## 验证路线（P0-P4）

| 阶段 | 内容 | 判据 |
|:---:|:---|:---|
| P0 | 统一日志格式 + 评测脚本开源 | 四框架都能接入 |
| P1 | 各自框架跑同一份日志 | Δt/FPR/FNR 齐备 |
| P2 | 维度归因 + 阈值扫描 | H1 是否跨系统成立 |
| P3 | 构造 A=0 僵死反例实验 | H2 是否成立 |
| P4 | 合成 FHI 报告 + 方法论论文 | H3 / H4 检验 |

## 边界声明

本项目统一的是**观测视角**，不统一**实现哲学**。外部存储 vs 内部感知、前置拦截 vs 事后审计，都是不同哲学的合理选择 —— FHI 只做观测对齐，不做实现强加。

## 许可证

- **思想层**（提案/文档/理论框架）：CC BY-NC-SA 4.0 —— 非商业·署名·相同方式共享
- **工程层**（schema/evaluator/代码）：MulanPSL v2 —— 允许商业使用·署名·专利授权

## 致敬

- 源自 [deepseek-ai/DeepSeek-V3#1466](https://github.com/deepseek-ai/DeepSeek-V3/issues/1466)（luoxuejian000）及 #1285 / #1420 / #1424 社区讨论
- 龍魂四级熔断 L0-L3 作为工程旁证（同构机制独立运行验证规律普遍性）
