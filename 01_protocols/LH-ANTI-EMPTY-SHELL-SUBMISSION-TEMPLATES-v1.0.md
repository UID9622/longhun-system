# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 🛡️ 龍魂·防空壳提交模板体系 v1.0（设计文档）

> **一句话**：参考大模型开源标杆仓库（ollama/openai-python/huggingface 等）的提交模板实践，
> 把防空壳五关从"协议文档"升级成"GitHub 表单字段"——提交时逐项必填，空壳在入口被拦下。
> 上位: LH-ANTI-EMPTY-SHELL-STANDARD-v1.1.md · 适用: UID9622 名下全部 GitHub 仓

DNA: #龍芯⚡️2026-09-06-ANTI-EMPTY-SHELL-SUBMISSION-TEMPLATES-v1.0-UID9622
创建者: 诸葛鑫（UID9622 · 龍芯北辰）
协议: CC BY-NC-SA 4.0（思想层）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

---

## 一、为什么做（差距分析）

原狀：防空壳五关写在 `LH-ANTI-EMPTY-SHELL-STANDARD-v1.1.md`，但 GitHub 的 Issue/PR 表单
没有承载五关 → 贡献者提交时**看不到防空壳要求**，空壳质疑发生后才补材料（被动）。

参照标杆（实抓核验）：
- **ollama**：`.github/ISSUE_TEMPLATE/` 用数字前缀编号（`10_bug_report.yml` / `20_feature_request.md` / `30_model_request.md` + `config.yml`）→ 选择界面有序、类别清晰
- **openai-python**：PR 模板 = 一个**前置确认框** + 变更说明 + 补充链接 → 极简，先锁共识再写内容
- **huggingface**：PR checklist 自检式 → 逐条勾选，评审前置

龍魂模板 v1.0 → v2.0 整合：
| 改进 | v1.0（旧） | v2.0（新） |
|:---|:---|:---|
| 模板编号化 | 无（靠字母序） | `00_防空壳达标` 置顶 → `10_bug` → `20_feature` → `30_question` → `40_shame` |
| 防空壳字段 | 未内嵌 | Bug 加"真实日志必填+防空壳自查"· Feature 加"PoC 可选"· Question 加"已尝试+真实输出" |
| 防空壳达标模板 | 无 | **新增 `00_anti_empty_shell.yml`**：五关逐项表单 + 自查勾选 + 质疑回应指引 |
| PR 自检 | 无五关 | 五关证据栏 + 防空壳自查确认框（禁手写理想输出） |
| config.yml | 仅社区链接 | 防空壳达标模板置顶 + 防空壳标准文档直链 |

---

## 二、模板清单（本仓已落位）

```
.github/
├── ISSUE_TEMPLATE/
│   ├── 00_anti_empty_shell.yml   🛡️ 防空壳达标声明（提交物五关自检 · 质疑回应）
│   ├── 10_bug_report.yml         🐛 Bug 报告（关②真实日志必填 · 自查勾选）
│   ├── 20_feature_request.yml    ✨ 功能请求（关①PoC 可选）
│   ├── 30_question.yml           ❓ 使用咨询（已尝试 + 真实输出）
│   ├── 40_shame_report.yml       🚫 耻辱墙反馈（保留原版）
│   └── config.yml                blank 关闭 · 防空壳置顶
└── PULL_REQUEST_TEMPLATE.md      🛡️ 五关证据栏 + 自查确认框 + GPG 声明
```

---

## 三、五关字段如何落进表单（核心设计）

| 关 | 标准定义 | 模板落地字段 | 必填 |
|:---:|:---|:---|:---:|
| ① PoC | 有可运行代码 | `关① PoC：有可运行代码吗？`（代码块/仓库链接） | ✅ |
| ② 真实运行 | 有实际输出 | `关② 真实运行结果`（render: shell，禁"预期"） | ✅ |
| ③ 复现步骤 | ≤5 步独立复现 | `关③ 复现步骤（≤5 步）` | ✅ |
| ④ 数据样本 | ≥10 条标注清晰 | `关④ 数据样本：测试数据在哪？` | ✅ |
| ⑤ 完整性 | DNA+SHA+GPG+确认码 | `关⑤ 完整性证明`（四项逐行） | ✅ |

**防空壳自查下拉**（防手写理想输出——防空壳标准特别注意点）：
- 我已实际运行，输出与所贴一致 → 🟢
- 我有真实输出但未完全复现 → 🟡 待补
- 我还没跑，只有设计说明 → 🔴 未达标退回

---

## 四、落地范围与用法

1. **主仓 longhun-system**：已完整落位（上述清单）。
2. **其他 UID9622 仓**：按需复制（防空壳标准 v1.1 触发场景 = 对外提交/论文/数据集交付）——
   建议 `00_anti_empty_shell.yml` + `PULL_REQUEST_TEMPLATE.md` 两件起步，Bug/Feature 按仓库实际改字段。
3. **使用时机**：
   - 外部要提交代码/模型/论文 → 引导用防空壳达标模板（或直接跑标准内 PoC）
   - 被质疑空壳 → 粘贴五关证据回应，见模板底部 📌 指引
   - 非代码提交（文档/蓝图）→ 防空壳标准第六章套用表

---

## 五、评审联动

- P05 评审收到 Issue/PR → 先看防空壳自查勾选：🔴 → 打回补实；🟡 → 标待核；🟢 → 正常流程（GATE-01~11）
- 新增模板文件需 GPG 签名（`python3 bin/lh_gpg_sign.py sign .github/`）

---

## 签名

```
{
  "executor": "P15乔前辈 + P05上帝之眼 + P08仓颉(命名)",
  "trigger_time": "2026-09-06T11:4x:00+08:00",
  "audit_mark": "🟢",
  "risk_score": 0.0,
  "dna": "#龍芯⚡️2026-09-06-ANTI-EMPTY-SHELL-SUBMISSION-TEMPLATES-v1.0-UID9622"
}
```

---
> v1.0 · 2026-09-06 · 整合 ollama 编号表单 + openai PR 确认框 + huggingface checklist · 防空壳五关表单化落地
> #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
