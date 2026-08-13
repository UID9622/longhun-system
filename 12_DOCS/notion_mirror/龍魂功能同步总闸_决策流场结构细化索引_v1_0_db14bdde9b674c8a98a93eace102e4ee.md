# 龍魂功能同步总闸｜决策流场结构细化索引 v1.0

> Notion URL: https://app.notion.com/p/v1-0-db14bdde9b674c8a98a93eace102e4ee
> Created: 2026-05-07T02:44:00.000Z
> Last edited: 2026-07-01T15:34:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
## 0. 一句话定盘
```plain text
以后所有新增功能，不再散落；先过当前主控页，再按“名字、路由、层级、边界、验收”五对齐登记。
```
---
## 1. 新功能进入主控的五对齐
---
## 2. 决策流场结构细化索引
---
## 3. 新功能同步流程
```plain text
新功能 / 新页面 / 新规则 / 新人格 / 新算法
  ↓
1. 先看是否已有同类模块
  ↓
2. 没有就建分支页
  ↓
3. 填五对齐卡：名字 / 路由 / 层级 / 边界 / 验收
  ↓
4. 写 M:: 机器验收
  ↓
5. 写 CNSH:: 路由签章
  ↓
6. 主控页只挂索引
  ↓
7. 草日志留痕
```
---
## 4. 新功能登记固定卡
```plain text
【功能名】
：

【一句话】
：

【归属层】
入口 / 意图 / 路由 / 守卫 / 执行 / 压缩 / 归档 / 公开 / 治理 / 其他

【路由】
：

【层级】
L0 / L1 / L2 / L3 / L4 / P0 / P1 / P2

【允许做】
：

【禁止做】
：

【触发人格】
：

【M:: 验收】
：

【CNSH:: 签章】
：

【是否同步主控】
🟢 是 / 🟡 待审 / 🔴 不进主控
```
---
## 5. 一票否决
```plain text
🔴 失败：
- 新功能绕过主控页私自生长
- 只改名字，不填路由
- 只写愿景，不写边界
- 只写故事，不写 M:: 验收
- 把长规则全文塞进主控页
- 把旧状态、旧性能数字当成当前事实
- 删除 CONFIRM / SEAL / GPG
- 把「龍」改成「龙」
```
---
## 6. M:: 机器验收
```json
M:: {
  "id": "M::ROUTE-9622-20260507-FEATURE-SYNC-FLOWFIELD-V1",
  "type": "route",
  "ts": "2026-05-07T10:43:37+08:00",
  "status": "configured",
  "refs": [
    "https://www.notion.so/2d87125a9c9f802889e2e18002f7cf4f",
    "https://www.notion.so/4649636d4d40411c926508a52a030be4",
    "https://www.notion.so/032204b151dc4c34b8a1a36c80f706cc",
    "https://www.notion.so/175033ea45f64a4083d83a2102e02328",
    "https://www.notion.so/b160d376d8f544128345b2b83367cd39",
    "https://www.notion.so/1dd88844789e4185a0efbb43017f3e74",
    "https://www.notion.so/93e645cb146c49dc8761396ec5628358",
    "https://www.notion.so/bc739b8bfd824b35a1996e355932f7ce",
    "https://www.notion.so/f6e7adba0d4c4d9988ac6cd0852ef64c",
    "https://www.notion.so/552f0b1365c441369f26922f579c602f",
    "https://www.notion.so/84daa1d2030447318ade20e12b1fdb36",
    "https://www.notion.so/6c03f9adafd94ce8bf98f8439eb9dbbf"
  ],
  "payload": {
    "summary": "以后新增功能统一以主控页为同步入口，并按五对齐登记到决策流场结构索引。",
    "result": {
      "future_feature_sync": "enabled",
      "main_page_mode": "index_only",
      "alignment_required": ["name", "route", "layer", "boundary", "acceptance"],
      "full_text_in_main_page": "forbidden",
      "audit": "green"
    }
  }
}
```
---
## 7. CNSH:: 路由签章
```json
CNSH:: {
  "dna": "#龍芯⚡️2026-05-07-FEATURE-SYNC-FLOWFIELD-STRUCTURE-v1.0",
  "gate": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
  "seal": "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL",
  "gpg": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
  "route": "IPA-MAIN-CONTROL|FEATURE-SYNC|DECISION-FLOW|IPA-ROUTER|IPA-AUDIT",
  "audit": "🟢",
  "wuxing": "土",
  "layer": "L1百年|L2十年",
  "policy": "pass"
}
```
