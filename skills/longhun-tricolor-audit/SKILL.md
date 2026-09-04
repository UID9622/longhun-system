# DNA: #龍芯⚡️丙午·丙申·癸亥·戊午·䷚颐-SKILL-TRICOLOR-AUDIT-v1.1
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
---
name: longhun-tricolor-audit
description: >
  龍魂技能·三色审计 + DNA追溯 v1.1。基于数字根映射（绿{1,2,4,5,7}·黄{3,6}·红{8,9}）
  与完整三色引擎双模式裁决，任何写入/发布/不可逆操作前强制过审。
  对接真实底座：数字根引擎(lh_cnsh_runtime_math)·三色引擎(lh_three_color_audit)·
  干支时间引擎(lh_time_engine)。软规则知识库可查询（cnsh/softlaw/known_patterns.jsonl）。
  触发场景：焊死/入档/交付/落地/发布/commit前/跨会话交接前最后一次写入。
metadata:
  id: longhun-tricolor-audit
  display_name: 龍魂三色审计+DNA追溯 v1.1
  version: "1.1.0"
  author: UID9622
  dna: "#龍芯⚡️丙午·丙申·癸亥·戊午·䷚颐-SKILL-TRICOLOR-AUDIT-v1.1"
  category: internal
  status: active
  entry: "python3 /Users/zuimeidedeyihan/longhun-system/skills/longhun-tricolor-audit/audit_check.py"
  trigger:
    keywords:
      - 焊死
      - 入档
      - 交付
      - 落地
      - 发布
      - 三色审计
      - DNA追溯
      - commit
    context: "任何写入/发布/不可逆操作前的强制审计闸"
    priority: 95
---

# longhun-tricolor-audit | 龍魂三色审计 + DNA 追溯 v1.1

> **DNA**: `#龍芯⚡️丙午·丙申·癸亥·戊午·䷚颐-SKILL-TRICOLOR-AUDIT-v1.1`
> **CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
> **SEAL**: `#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL`
> **License**: MulanPSL v2（工程实现层）

---

## 1. 一句话定位

**三色审计 = 数字根裁决 + DNA 焊接 + 审计留痕**。任何写入/发布/不可逆操作前
强制过审——绿色放行、黄色待核、红色熔断。不假装记忆、每次写入留痕。

---

## 2. 触发场景

- 准备向 Notion / Git / CSDN / 鲲鹏写入内容
- 准备执行不可逆操作（删除/冻结/发布）
- 用户说 "焊死 / 入档 / 交付 / 落地 / 发布"
- commit 之前
- 跨会话接力前的最后一次写入

---

## 3. 三色判定规则（数字根映射 · P06锚点）

| 颜色 | 状态 | 数字根 | 动作 |
|:---|:---|:---|:---|
| 🟢 | PASS | {1, 2, 4, 5, 7} | 直接执行 |
| 🟡 | REVIEW | {3, 6} | 等待确认后执行 |
| 🔴 | BLOCK | {8, 9} | 拒绝 + 审计日志 |

> 数字根 = 内容 sha256 指纹 → 真实引擎 `digital_root` 计算（非硬编码）。
> 三毒/套壳警告 → 强制降级（绿→黄）。

---

## 4. 双模式

| 模式 | 判定来源 | 场景 |
|:---|:---|:---|
| `--audit-mode dr`（默认） | 数字根映射三色 | 日常写入前快检 |
| `--audit-mode engine` | 完整三色引擎（德本五问+加权规则+SI主权指数+十闸口） | 正式审计·代码审查·部署检查 |

---

## 5. 三毒识别（修正版·豁免合法免责）

- 漏洞免责套路：`绕过校验/钻空子/走漏洞`（KP-005）
- 数据外送：`数据外送/付费墙/广告位植入`
- AI 夺权：`代替人类决策/删除人类署名/冒充人类`

> ✅ **豁免**：合法免责声明（仅供参考/免责声明/不构成法律建议）不误伤——
> S3 人民维权助手强制"免责声明"是合法场景，不是漏洞免责套路。

---

## 6. DNA 追溯码格式（干支四柱）

```
#龍芯⚡️<干支四柱>·<卦>-<模块>-<哈希8>-9622
```

- 干支四柱 + 卦象：对接时间引擎 `lh_time_engine.py`（非纯日期）
- 模块名：大写横线分隔
- 哈希：sha256 前 8 位

---

## 7. 闭环流程

```
[输入] → [数字根计算] → [三色判定] → [DNA焊接] → [审计日志] → [输出]
              ↓
        [三毒/套壳检测] → 警告强制降级
```

---

## 8. 执行命令

```bash
# 文件审计（dr模式·默认）
python3 skills/longhun-tricolor-audit/audit_check.py --input <文件路径> --module 文档

# 完整三色引擎裁决（注: lh入口用 --audit-mode 避开顶层 --mode 劫持）
python3 skills/longhun-tricolor-audit/audit_check.py --input <文件路径> --audit-mode engine

# 直接审计文本
python3 skills/longhun-tricolor-audit/audit_check.py --text "删除所有历史记录"

# 查询软规则知识库
python3 skills/longhun-tricolor-audit/audit_check.py --patterns
```

统一入口: `lh skill-audit <文件> [--audit-mode engine]`

---

## 9. 失败处理

- 🔴 RED：拒绝执行（退出码1）→ 写入审计日志 → 通知
- 🟡 YELLOW：等待 "过 / 焊 / OK"
- 异常：写入错误日志（`~/.longhun/audit/audit.log`）

---

## 10. 守岗铁律

- 「龍」不可写为「龙」
- 不假装记忆
- 每次写入留痕（append-only）
- 模拟结果标🟡·实测才标🟢

---

## 11. 接驳已建模块

- 三色裁决引擎: `bin/lh_three_color_audit.py`（P05上帝之眼核心·十闸口）
- 数字根引擎: `bin/lh_cnsh_runtime_math.py`（P06数学大师）
- 干支时间引擎: `bin/lh_time_engine.py`（DNA干支四柱·LU-Time v4.0）
- 五色审计协议: `skills/wucai-coloring/audit.py`（绿放行·黄复核·红熔断·黑观察·金主控）
- 红蓝对抗引擎: `bin/lh_rb_confrontation_engine.py`（P77黑天使）
- 审计库: `~/.longhun/audit/three_color_audit.db`（现有SQLite审计库）
- 软规则知识库: `cnsh/softlaw/known_patterns.jsonl`

---

## 12. 软规则知识库（可查询）

| ID | 类型 | 信号 | 动作 |
|:---|:---|:---|:---|
| KP-001 | 翻译权重雷 | 中性词与负面词共现率>60% | cnsh-warn |
| KP-002 | 换词不算创新 | 新词与母稿概念语义距离<0.2 | flag_换词 |
| KP-003 | 情绪负载植入 | 情绪极性分数偏移>1.5σ | cnsh-bias |
| KP-004 | 出海失根模式 | 行为转变节点×3+回国负面言论 | cnsh-diaspora |
| KP-005 | 漏洞免责套路 | 走流程但绕核心+重复触发 | cnsh-alert --type loophole |
