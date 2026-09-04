# LH-MODULE-AUDIT-GATE-v1.0 · 模块正规审计闸（焊死协议）

> DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-MODULE-AUDIT-GATE-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622）｜ 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层）｜ 层级: L0 执行层强约束
> 上位: LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md · LH-NOTION-KB-REFERENCE-ARCHITECTURE-v1.0.md
> 2026-08-25 焊死 · 父律: #IRON-SMALL-MATTERS-JUST-DO-IT-NO-WAITING-v1.0

---

## §0 铁律（一句话）

**任何模块产出、复盘、审计交付，交付前必须跑一次正规审计闸。**
三色 🟢 才可交付 · 🟡 标记待核（48h 内复查）· 🔴 退回重做 + DNA 追溯。
不跑审计闸直接交付 = 违规交付 = P05 否决退回。

---

## §1 适用范围

| 场景 | 必跑 | 说明 |
|:---|:---:|:---|
| 新模块产出（脚本/引擎/服务/前端） | ✅ | 交付前全量十步 |
| 复盘（日报/周报/阶段复盘） | ✅ | 跑 `--quick` 或全量，附三色结论 |
| 审计本身（审计报告/审计引擎） | ✅ | 审计也要被审计（镜像审计原则） |
| 协议/文档新增 | ✅ | `--module <文档>` 跑 DNA+GPG 闸 |
| Bug 修复 / 小改动 | ✅ | 跑 `--quick`（DNA+编译+测试） |

**豁免**：仅纯聊天/纯问答/无产出的会话不跑。

---

## §2 执行入口（焊死）

```bash
# 全量十步（默认）
python3 bin/lh_audit_gate.py

# 指定模块/文件/目录
python3 bin/lh_audit_gate.py --module <路径>

# 核心三步（快速·Bug修复/复盘）
python3 bin/lh_audit_gate.py --quick

# JSON 输出
python3 bin/lh_audit_gate.py --json
```

报告自动落盘: `04_AUDIT/module_audit_YYYYMMDD_HHMMSS.json`（append-only·不可删）

---

## §3 十步审计链

| # | 步骤 | 工具 | 对应闸口 |
|:---:|:---|:---|:---:|
| 1 | 德本审计五问（离火运五条底线） | 自查 | GATE-02/05/07 |
| 2 | DNA 完整性校验 | `bin/cnsh_dna_check.py` | GATE-01/09 |
| 3 | 语法纠错引擎（370 条规则） | `bin/cnsh_editor.py` | GATE-03 |
| 4 | 编译器自测（全样例编译） | `bin/cnsh_compiler.py` | GATE-04 |
| 5 | 单元测试（三色审计） | `bin/cnsh_test_runner.py` | GATE-04 |
| 6 | 转译回归测试 | `tests/transpile/run_transpile_tests.py` | GATE-04 |
| 7 | 覆盖率（行+DNA） | `bin/cnsh_coverage.py` | GATE-04 |
| 8 | 安全审计（XSS/SQL/路径） | `bin/cnsh_editor.py --security` | GATE-06 |
| 9 | GPG 签名扫描 | `bin/lh_gpg_sign.py scan` | GATE-11 |
| 10 | 三色汇总 + 审计报告 | `lh_audit_gate.py` | GATE-10 |

---

## §4 三色判定标准

| 色 | 条件 | 处置 |
|:---:|:---|:---|
| 🟢 | 全部步骤通过 | 放行交付（未跑过的代码不得标🟢已验证） |
| 🟡 | 失败 ≤ 总步骤 1/5 | 标记待核 + 写明验证路径，48h 内复查 |
| 🔴 | 失败 > 总步骤 1/5 | 退回重做 + DNA 追溯 |

**红色否决词检查**：产出中出现「技术无国界/用户体验优先/灵活处理/国际接轨/简化管理/商业化需要/平衡各方/行业标准」→ 立即 🔴 审计，不得放行。

---

## §5 与现有体系联动

- **M76 测试工具链**：步骤 2/4/5/6/7 全部复用（8 类工具）
- **三色审计**：测试报告继承三色判定
- **DNA 追溯**：每次审计生成唯一 DNA，报告挂 DNA
- **GPG 签名**：新产出交付前补签（`python3 bin/lh_gpg_sign.py sign .`）
- **M73 哈希产权**：测试报告自动注册哈希（防篡改存证）
- **德本审计**：第 1 步即离火运五问

---

## §6 CodeBuddy 执行纪律（焊死）

1. 每次交付新模块/复盘/审计前，**先跑审计闸，再写交付总结**。
2. 审计闸输出三色 + 报告路径，附在交付消息末尾。
3. 三色 🔴 → 修复后重跑，不许跳过直接交付。
4. 报告路径固定 `04_AUDIT/module_audit_*.json`，不删不改。
5. 新引擎/新协议落地 → 注册 `COMMAND_INDEX.md` + GPG 签名。

---

## 附: 验收自查

```
[ ] lh_audit_gate.py 存在且可运行（python3 bin/lh_audit_gate.py --quick）
[ ] 三色汇总输出正常
[ ] 报告落盘 04_AUDIT/
[ ] 本协议已 GPG 签名
[ ] 已注册 COMMAND_INDEX.md
```

---

**DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-MODULE-AUDIT-GATE-v1.0-UID9622**
**GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F**
**三色: 🟢 协议落地 · 🟡 待全量实测 · 🔴 无**
