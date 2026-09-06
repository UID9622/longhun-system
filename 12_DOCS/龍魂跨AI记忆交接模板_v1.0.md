# 龍魂跨AI记忆交接模板 v1.0

> 干支时间戳: 🐉丙午·丁酉·癸未·卯时·䷚颐·🟢
> DNA: #龍芯⚡️丙午·丁酉·癸未·卯时·䷚颐-HANDOFF-TEMPLATE-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层）
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

## 使用场景：CodeBuddy→龍魂NotionAI / Kimi / 任何新AI冷启动

---

## STEP 1：CodeBuddy 发出端（切换前执行）

```bash
lh session save --task "当前任务名" --decision
lh brain remember "交接摘要·当前状态·待续任务·[干支时间]"
lh memory-hub push  # 推送最新记忆到共享总线
lh sync memory      # 蒸馏至Notion外接大脑
cat ~/.longhun/session_context.json > /tmp/handoff_context.json
```

## STEP 2：新AI 接收端（粘贴以下块启动）

```text
[MEMORY_HANDOFF_BLOCK]
- 系统：龍魂·UID9622·丙午年
- 权威记忆：.codebuddy/memory/MEMORY.md（L6·精简版）
- 当前任务：{从session_context.json读active_task}
- 最近决策：{从memory-hub pull --limit 3}
- 干支时间：{lh_time_engine.py --stamp-full}
- 人格路由：P00→P04→P05→P06→P15→P03（P72仅🔴）
- 焊死规则：判据④·先实机·不凭文本·GPG签名·三色闭环
[/MEMORY_HANDOFF_BLOCK]
```

## STEP 3：验证交接完整性

```bash
lh session status
lh memory-hub pull --limit 5
lh brain search "[最近关键词]"
```

---

> 三明治防御焊入：`lh autofill fill --file <本文档> --stamp --tail --attr --sov --sign --relay`
> （--file 单文件精确模式: 干支头戳+文尾戳+GPG签名+接力签名+hub登记·单文件不误伤目录）

🐉AI协作输出时间戳: 🐉丙午·丁酉·癸未·卯时·䷚颐·🟢

---
## 🧬 AI 协作接力签名

> 本条记录本次交付的 AI 人格协作链路（谁做了什么·怎么接力·可追溯）。
> 接力铁律：执行→审计→验证→签章→归档；🔴 才升级 P72 熔断，平时 P72 不占位。

| 序号 | 人格(职能) | 本步操作 | 干支触发时间 |
|:---:|:---|:---|:---|
| 1 | P00意图路由(协作执行) | 按链执行 → 接力下一环 | #龍芯⚡️丙午·丁酉·癸未·卯时·䷚颐 |
| 2 | P04鲁班执行(技术执行) | 写码/改文件/修 bug → fill 自动填充/写正文 → 执行完 → 接力 P05 | #龍芯⚡️丙午·丁酉·癸未·卯时·䷚颐 |
| 3 | P05上帝之眼审计(审计) | 三色审计（时间戳干支✓/署名✓/主权声明✓）→ 出差异清单 → 🟢 过 → P06 复算；🔴 → P72 | #龍芯⚡️丙午·丁酉·癸未·卯时·䷚颐 |
| 4 | P06数学大师验证(验证) | 数字根/DNA 追溯码复算 → 一致🟢 偏差🟡 → 过 → P15 | #龍芯⚡️丙午·丁酉·癸未·卯时·䷚颐 |
| 5 | P15乔前辈签章(签章) | GPG 分离签名 + DNA 盖章（fill --sign） → 签后 → P03 | #龍芯⚡️丙午·丁酉·癸未·卯时·䷚颐 |
| 6 | P03雯雯归档(归档) | 四签验证·落位正确目录·复盘留痕 → 收口 | #龍芯⚡️丙午·丁酉·癸未·卯时·䷚颐 |

**协作链**: P00意图路由→P04鲁班执行→P05上帝之眼审计→P06数学大师验证→P15乔前辈签章→P03雯雯归档
**文档**: /Users/zuimeidedeyihan/longhun-system/12_DOCS/龍魂跨AI记忆交接模板_v1.0.md
**确认码**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**归属名**: 诸葛鑫 | UID9622 · 龍芯北辰
**GPG**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
