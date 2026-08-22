# CNSH 变更日志

> **DNA**: `#龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-CNSH-CHANGELOG-v1.0-UID9622`
> **创建者**: 诸葛鑫（UID9622）
> **协议**: MulanPSL v2（工程实现层）
> **确认码**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
> **三色**: 🟢 已定稿
> **约定**: 语义化版本 `主.次.补丁` · 变更按时间倒序 · 每个条目带 commit 与签名

---

## [2.0.0] - 2026-08-21

### 新增（补全包）

- **`docs/spec/parse_rules.md`**：CNSH 通用解析规范 v2.0
  - 解析失败四分类（P-AMB / P-DEP / P-BND / P-FMT）
  - 通用 10 条稳定写法 · 清坑规范表 · 说实话模式 · 固定写作约定
  - commit `46bf1f5` · 签名 ✅
- **`docs/spec/dual_perspective.md`**：CNSH 双视角封装协议 v1.0
  - `M::` 机器视角 vs `CNSH::` 路由视角 · 使用规则 · 禁忌词 · 输出结构示例
  - commit `46bf1f5` · 签名 ✅
- **`docs/architecture/README.md`**：CNSH 技术栈架构 v1.0
  - 六层全景图（L0 语言 → L5 主权）· 五阶段路线图
  - commit `91f388c` · 签名 ✅
- **`docs/architecture/runtime_spec.md`**：Algorithm Runtime 规格书 v1.1
  - Syntax Layer / Algorithm Router / Plugin Registry / Local Shield
  - commit `91f388c` · 签名 ✅
- **`docs/audit/ai_behavior_standard.md`**：AI 行为标准 v1.0
  - 接入六铁律 · 三次违规取消资格 · 标准指令模板
  - commit `91f388c` · 签名 ✅
- **`CONTRIBUTING.md`**：贡献指南 v1.0（流程 / 硬性规范 / 行为准则）
- **`docs/GLOSSARY.md`**：中英双语术语表（30+ 条）

## [1.0.0] - 2026-08-21

### 初始发布

- 16 章 CNSH 语言规范（intro 0-3 · reference 4-8 · audit 9-12 · shell 13-16）
- 附录 A-D · 示例 examples/ · 语法定义 `cnsh_grammar.bnf`
- 结构校验 `cnsh_schema.json` · 保留字 `reserved_keywords.txt`
- README / LICENSE / INDEX 全量落地 · 全文件 GPG 签名
- commit `1655f46` · `263de41`

---

**GPG**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
