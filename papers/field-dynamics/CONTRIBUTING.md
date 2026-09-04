# 贡献指南 · Field Dynamics

DNA: #龍芯⚡️丙午·丙申·乙丑·壬午·䷨损-FIELD-DYNAMICS-CONTRIBUTING-v1.0
创建者: 诸葛鑫（UID9622）
许可: CC BY-NC-SA 4.0（思想层）· MulanPSL v2（工程层）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

---

## 你能贡献什么

| 类型 | 说明 | 入口 |
|:---|:---|:---|
| 🗂️ **接入新框架** | 把你的框架日志按 schema 导出并跑评测 | `docs/VALIDATION-PROTOCOL.md` |
| 🏷️ **标注数据** | 为共享数据集标注崩溃点/前兆维度 | 提交标注后的 JSONL |
| 📐 **改进归一化** | U/D/A/H 代理指标的工程边界标定 | 提案 §9 + evaluator 源码 |
| 📊 **阈值扫描** | 为 H1 提供跨系统 0.3 检验数据 | evaluator `--threshold` |
| 🧪 **A=0 僵死实验** | 构造低对抗性系统验证 H2 | P3 阶段任务 |
| 📝 **方法论** | FHI 合成、维度归因的统计方法 | P4 阶段任务 |

## 接入新框架的验收标准（Checklist）

- [ ] 日志符合 `schema/field-dynamics-log.schema.json`（JSON Schema 校验通过）
- [ ] 公共字段齐全：`ts` / `input_hash` / `session_id` / `heads` / `blocked`
- [ ] 核心指标可从公共字段计算（不依赖私有扩展）
- [ ] 评测结果附维度归因（`precursor_dimension` 或 evaluator 归因输出）
- [ ] 私有扩展字段声明在 `extensions`，不污染公共口径
- [ ] 提交物含 `framework-info.json`（框架名/版本/指标口径/作者）

## 代码规范

- Python >= 3.9，标准库优先，零第三方依赖（evaluator 设计原则）
- 新代码通过 `python3 evaluator/evaluator.py --self-test`
- 工程文件头带 License 声明：`# License: MulanPSL v2`
- 文档文件头带 DNA / 创建者 / 许可 / GPG

## 提交流程

1. Fork 本仓库，新建分支 `feat/your-framework` 或 `fix/xxx`
2. 提交 PR，描述：改动内容 + 评测结果 + 与提案 §6 的对应关系
3. 维护者按三色审计（🟢通过 / 🟡待核 / 🔴红线）审阅
4. 涉及公共 schema 的改动需注明版本迁移说明

## 争议解决

- 指标口径争议 → 以"可从公共字段计算"为准绳，附复算步骤
- 维度归属争议 → 提交维度归因数据，H3 假设接受证伪
- 哲学边界（外部存储 vs 内部感知）→ 不统一，尊重实现自由
