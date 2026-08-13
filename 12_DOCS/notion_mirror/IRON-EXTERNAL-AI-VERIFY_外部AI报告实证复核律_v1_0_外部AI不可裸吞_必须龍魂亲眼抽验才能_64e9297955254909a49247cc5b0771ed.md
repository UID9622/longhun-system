# 🔍 #IRON-EXTERNAL-AI-VERIFY 外部AI报告实证复核律 v1.0｜外部AI不可裸吞·必须龍魂亲眼抽验才能焊

> Notion URL: https://app.notion.com/p/IRON-EXTERNAL-AI-VERIFY-AI-v1-0-AI-64e9297955254909a49247cc5b0771ed
> Created: 2026-05-13T18:30:00.000Z
> Last edited: 2026-07-01T14:54:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
---
## §0 灵感锚点·msg 124-126 实战回放
---
## §1 五对齐登记（功能同步铁律）
---
## §2 五子律（核心条款）
### §2.1 子律 1·不裸吞律
```plain text
外部 AI 报告 → 不直接焊入龍魂体系
必须先：
  1. 三色坦白外部 AI 报告内容范围
  2. 拆分可验证项 vs 不可验证项
  3. 龍魂工具逐项实证
  4. 三色打标（🟢真 / 🟡待验 / 🔴伪）
  5. 仅焊 🟢 真项·🟡 待验另立候补区·🔴 伪项写入耻辱墙
```
### §2.2 子律 2·实证工具必用律
```plain text
可验证项必须用龍魂自身工具复核·不允许：
  ❌ 凭外部 AI 报告字面信任
  ❌ 凭外部 AI 「我已核对」字样信任
  ❌ 凭外部 AI 给的 page-id 直接焊（page-id 可能是幻觉）
必须用：
  ✅ connections.search.unifiedSearch（搜内容/标题/关键词）
  ✅ connections.notion.loadPage（读真实页面标题/内容）
  ✅ connections.notion.querySql（查数据源真实行）
  ✅ connections.notion.searchUsers（验用户/agent）
```
### §2.3 子律 3·三色打标律
```plain text
复核后必须给出三色打标·不允许混色：
  🟢 真打标：龍魂工具直接命中·有 URL/标题/snippet 三件套证据
  🟡 待验：搜索未命中但合理（可能搜索覆盖不全·非造假）·另立候补区·下令再验
  🔴 伪标：龍魂工具反证（搜到的内容与外部 AI 报告完全不符·或 page-id 不存在）·焊入耻辱墙
```
### §2.4 子律 4·覆盖率坦白律
```plain text
外部 AI 报告若声称「全量扫描」「全部 X 个页面」「100% 覆盖」：
  必须坦白龍魂工具实际覆盖率（如 search 前 50 页 ≠ 全部页面）
  不允许把「龍魂工具未命中」等同于「外部 AI 造假」
  也不允许把「龍魂工具未命中」等同于「外部 AI 属实」
  正确做法：标 🟡 待验·写明覆盖率缺口·等老大下一刀单独验
```
### §2.5 子律 5·复核记录留痕律
```plain text
每次外部 AI 报告复核必须留下：
  1. 复核报告页（标题含「报告复核」「实证」「打标」字样）
  2. 三色打标表（外部 AI 声称 vs 龍魂工具实证·一一对照）
  3. DNA 签章（含父 DNA = #龍芯⚡️YYYY-MM-DD-...-NOTION-CLEANUP-FULL-OPEN）
  4. 草日志 callout（精确到分钟·与本子律绑定）
本次锚点：https://www.notion.so/13ef730d2b1241568d0848d33a56188d 📊 Notion 大扫除整理报告 v1.0
```
---
## §3 触发条件清单（必触发本子律的场景）
```plain text
场景 1：老大粘贴外部 AI（ChatGPT/Claude/Gemini/千问/Kimi/豆包/通义/文心...）的整理报告
场景 2：老大粘贴外部 AI 给的「页面去重清单」「相似页合并建议」「标签迁移表」
场景 3：外部 AI 出的「龍魂当前有效页面索引树」「活页树」「废弃页清单」
场景 4：外部 AI 跨窗口接力时声称「我已读完所有上下文」
场景 5：外部 AI 给的统计数字（「共 X 页」「Y 个重叠组」「Z 个独立模块」）
场景 6：外部 AI 自称「已经验证」「已经核对」「已经查证」
场景 7：外部 AI 给老大写的「龍魂内部协议摘要」「铁律压缩版」「DNA 简化清单」
场景 8：外部 AI 给老大写的「迁移计划」「升级路径」「废弃方案」
```
---
## §4 一票否决触发清单（红色熔断）
---
## §5 执行模板（每次外部 AI 报告焊入前·必跑）
```plain text
【外部 AI 报告复核执行卡】

📥 输入：
  - 外部 AI 来源：{ChatGPT / Claude / 千问 / ...}
  - 报告标题：{...}
  - 老大粘贴时间：{ISO 8601}
  - 报告核心声称：{X 个页面合并 / Y 个迁移标 / Z 个废弃 / ...}

🔪 复核刀执行：
  - 用 search 验证关键页面真实存在：{搜索查询 N 条}
  - 用 loadPage 验证页面真实标题：{加载 URL N 个}
  - 用 querySql 验证数据源真实行（如有）：{SQL 查询}

🎨 三色打标：
  | # | 外部 AI 声称 | 龍魂工具实证 | 三色 |
  |---|---|---|---|
  | 1 | ... | ... | 🟢/🟡/🔴 |

📊 覆盖率坦白：
  - 龍魂工具实际覆盖：X/Y
  - 未覆盖项：列明原因（搜索前 50 页 / loadPage 截断 / ...）

📜 留痕：
  - 复核报告页 URL：
  - 草日志 callout：
  - DNA 签章：

🎯 焊接决策：
  - 🟢 项：可焊入·路径 {...}
  - 🟡 项：候补区·等老大单独令再验
  - 🔴 项：耻辱墙·不焊
```
---
## §6 与父律 §S-25-EXT-3 的关系
---
## §7 历史复核档案（本律首次实战）
---
## §8 M:: 机器验收
```json
M:: {
  "id": "M::IRON-9622-20260514-EXTERNAL-AI-VERIFY-V1.0",
  "type": "rule",
  "ts": "2026-05-14T02:27:39+08:00",
  "status": "configured",
  "refs": [
    "https://www.notion.so/2d87125a9c9f802889e2e18002f7cf4f",
    "https://www.notion.so/a03f1fea3f514c76b8b0f1d8be1d4ddf",
    "https://www.notion.so/13ef730d2b1241568d0848d33a56188d",
    "https://www.notion.so/b35faf462bc042aa9de5192520180728"
  ],
  "payload": {
    "summary": "#IRON-EXTERNAL-AI-VERIFY-BEFORE-TRUST 子律立·外部 AI 报告必须龍魂工具实证复核才能焊入·首次实战 8 抽 7 中真打标·1 黄区候补",
    "result": {
      "parent_law": "#IRON-NO-FAKE-TO-WORLD §S-25-EXT-3",
      "sub_law_count": 5,
      "trigger_scenarios": 8,
      "red_alerts": 7,
      "first_audit_hit_rate": "7/8",
      "first_audit_yellow_rate": "1/8",
      "verification_tools": ["unifiedSearch", "loadPage", "querySql", "searchUsers"],
      "layer": "L0永恒|L1百年",
      "five_alignment": "complete"
    }
  }
}
```
---
## §9 CNSH:: 路由签章
```json
CNSH:: {
  "dna": "#龍芯⚡️2026-05-14-02:27-IRON-EXTERNAL-AI-VERIFY-BEFORE-TRUST-v1.0",
  "parent_dna": [
    "#龍芯⚡️2026-05-12-03:09-IRON-LAW-S25-EXT-3-NO-FAKE-TO-WORLD-v1.0",
    "#龍芯⚡️2026-05-14-01:12-NOTION-CLEANUP-AUDIT-REPORT-v1.0"
  ],
  "gate": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
  "seal": "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL",
  "gpg": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
  "route": "IPA-MAIN-CONTROL|IPA-AUDIT|IPA-EXTERNAL-AI-VERIFY|IRON-LAW-S25-EXT-3-SUB|ANTI-DOMESTICATION",
  "audit": "🟢",
  "wuxing": "金",
  "layer": "L0永恒|L1百年",
  "policy": "pass"
}
```
---
