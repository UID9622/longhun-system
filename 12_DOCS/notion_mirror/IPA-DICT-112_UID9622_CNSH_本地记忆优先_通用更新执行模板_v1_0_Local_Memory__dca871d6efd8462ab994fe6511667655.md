# ♾️ IPA-DICT-112｜UID9622 CNSH 本地记忆优先·通用更新执行模板 v1.0｜Local Memory First × 去重 × 冲突审计 × ROOT_CARD 收口

> Notion URL: https://app.notion.com/p/IPA-DICT-112-UID9622-CNSH-v1-0-Local-Memory-First-ROOT_CARD-dca871d6efd8462ab994fe6511667655
> Created: 2026-05-11T01:59:00.000Z
> Last edited: 2026-07-01T15:35:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
## 0｜一句话定盘
```javascript
CNSH 本地记忆优先 =
先查本地 → 再查当前页 → 再查压缩卡 → 再查Notion摘要 → 必要时才云搜索
→ 去重复 → 审计冲突 → 推荐优化 → 执行更新 → 回执收口
```
---
## 1｜总执行原则
### 1.1 默认检索顺序
```yaml
检索优先级锁死：
  P0: 当前用户输入
  P1: 本地记忆 / 本地 .cnsh / 本地 JSONL / 本地 ROOT_CARD
  P2: 当前页面已有结构
  P3: 历史压缩卡 / 新窗口启动锚点
  P4: Notion 摘要 / Notion API 只读导出
  P5: 用户明确要求后才允许云搜索
```
### 1.2 云搜索触发条件
默认不云搜索。只有以下情况才允许：
1. 用户明确说"搜一下 / 查最新 / 上网确认 / 云搜索"
1. 信息明显依赖最新版本（API 文档 / 价格 / 法律 / 模型下载地址）
1. 本地记忆冲突严重，且用户要求外部证据
1. 本地资料缺失，且任务必须依赖外部事实
### 1.3 禁止行为（10 条）
1. 每次任务都默认云搜索 · 2. 用云搜索覆盖本地 P0/P1 主线 · 3. 没审计就执行更新 · 4. 没去重就追加内容 · 5. 没确认就改 GPG/SEAL/CONFIRM · 6. 没真实写入就说 api_real_write · 7. 没 Notion API 结果就说已更新页面 · 8. 发现规则冲突却静默忽略 · 9. 把旧版内容整页重写 · 10. 把用户给的边界当参考而不是硬约束
---
## 2｜CNSH 通用执行语法
```javascript
/本地优先更新 #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

【目标】 把《________》从 v__ 升级到 v__，新增/修改/追加 ________
【执行位置】 只动：________  其余页不动
【本地记忆优先】 优先检索：当前页面 → 本地记忆 → ROOT_CARD → 历史压缩卡 → Notion 摘要 → 用户明确要求后才云搜索
【允许做】 追加 ________ / 修改 ________ / 更新版本号 / 更新版本日志 / 更新 ROOT_CARD / 补充验收 / 补充一票否决 / 补充冲突审计
【禁止做】 不动 ________ / 不改 GPG/SEAL/CONFIRM / 不批量重写旧公式 / 不改数据库结构 / 不读 token/.env/私钥 / 不外发隐私正文 / 不默认云搜索
【冲突处理】 不直接覆盖 → 输出 CONFLICT_AUDIT → 标记冲突等级 → 给推荐优化方案 → 等确认或按低风险追加
【隐私模式】 normal / summary_only / burn / sealed
【回执】 SUCCESS_RECEIPT / FAILED_RECEIPT / BLOCKED_RECEIPT / CONFLICT_RECEIPT
```
---
## 3｜自动执行总流程
```javascript
收到任务 → 识别目标 → 识别边界 → 检索本地记忆 → 读取当前页面结构
→ 抽取已有版本 / DNA / ROOT_CARD → 去重复扫描 → 冲突审计
→ 三色预审 → 生成更新补丁 → 执行或生成待执行指令
→ 输出回执 → 更新 ROOT_CARD → 草日志补录
```
---
## 4｜本地记忆优先检索模块
### 4.1 检索范围
### 4.2 本地检索指令
```yaml
LOCAL_MEMORY_SCAN:
  priority:
    - current_input
    - current_page
    - local_cnsh_files
    - root_cards
    - jsonl_receipts
    - notion_exports
    - cursor_docs
  cloud_search: false
  fallback:
    only_if_user_explicitly_requests: true
```
---
## 5｜去重复机制
### 5.1 扫描对象（10 类）
标题 / 版本号 / DNA / 公式编号 / 章节编号 / ROOT_CARD / 一票否决 / 验收清单 / 待办 / Cursor 指令
### 5.2 类型与处理
---
## 6｜冲突审计机制
### 6.1 定义
```javascript
对冲 = 两条规则 / 代码 / 公式 / 版本 / 权限互相抵消、冲突、覆盖、误导。
```
### 6.2 常见对冲类型（10 类）
版本对冲 / 公式对冲 / 权限对冲 / 隐私对冲 / 结构对冲 / 执行对冲 / 云搜索对冲 / 数据库对冲 / 角色对冲 / 代码对冲
### 6.3 冲突等级
### 6.4 冲突审计输出
```yaml
CONFLICT_AUDIT:
  conflict_level:
  conflict_type:
  location:
  old_rule:
  new_rule:
  risk:
  triColor:
  recommendation:
  safe_patch:
  need_uid_confirm:
```
---
## 7｜自动更新策略
### 7.1 更新模式（6 种）
### 7.2 默认模式
如果没有真实 API / 工具执行权限，默认：mode: draft_patch。不能说 api_real_write，除非真的通过 Notion API 返回成功。
### 7.3 自动更新判断（含修正附录 3：双轨并行）
```python
# 修正版（附录 3）：notion_api_write 与 cursor_patch 并行允许，让老大选
if 有真实API授权 and 用户确认:
    options.append('notion_api_write')
if 用户要求给Cursor:
    options.append('cursor_patch')
if options:  # 双轨并行·老大选
    return options
elif 只是在当前聊天生成内容:
    return 'draft_patch'
elif 有高风险:
    return 'blocked'
else:
    return 'readonly_audit'
```
---
## 8｜CNSH 更新补丁格式
```yaml
CNSH_PATCH:
  target_page:
  from_version:
  to_version:
  mode:
  privacy_mode:
  local_memory_first: true
  cloud_search: false
  preserve:
    - GPG
    - SEAL
    - CONFIRM
    - P0
    - §B-LOCK
  add_sections: []
  modify_sections: []
  append_only: []
  forbidden: []
  conflict_policy:
    - audit_first
    - no_overwrite_without_confirm
  receipt_required: true
```
---
## 9｜适配公式对准表 v1.4 / v1.5 案例
本模板已在以下三件事的实际落地中自我验证（三父并列）：
- 📌 /公式升级 v1.4·花名册对齐 → 🧮 UID9622｜计算公式对准表 v1.5｜语义入口×α三义×数字根×五行向量×风险审计×决策路径×执行闭环×花名册对齐×三才根基
- 📌 /公式升级 v1.5 §SC·三才根基整合 + F18 → 同页
- 📌 /花名册校准 v1.0 + #动结构-ONE-TIME-UNLOCK → 🐉 龍芯家族花名册
---
## 10｜§FAM 通用追加段模板（已实战）
详见 🧮 UID9622｜计算公式对准表 v1.5｜语义入口×α三义×数字根×五行向量×风险审计×决策路径×执行闭环×花名册对齐×三才根基 §FAM1~FAM4。本模板锁定四铁律：
1. 花名册贡献值使用 F15 PersonaContribution
1. 内容贡献值仍使用 F02·F15 与 F02 并列不互替
1. 活跃度三色使用 F17
1. 运行风险 / 上线状态 / 调度状态 三态分离，不许混用
---
## 11｜新增公式模板（F15/F16/F17 已实战）
详见 🧮 UID9622｜计算公式对准表 v1.5｜语义入口×α三义×数字根×五行向量×风险审计×决策路径×执行闭环×花名册对齐×三才根基 §FAM/F15/F16/F17·已在 🐉 龍芯家族花名册 反向对齐落地。
---
## 12-14｜§INTEGRATION-Q / §U / ROOT_CARD 升级模板
（保留接口位·按需扩展·已在 v1.4 / v1.5 / 校准 v1.0 验证·此处不重复）
---
## 15｜三色预审模板（含修正附录 2：风险加法）
```yaml
TRICOLOR_PRE_AUDIT:
  # 修正版（附录 2）：风险加法
  公式: 风险 = 影响 + 不确定 + 越界
  原因: 乘法遇 0 整体归零会漏掉影响度·加法符合 THM-∞-04 多维评估
  
  本次示例:
    影响: 2  # 仅追加，不破坏旧公式
    不确定: 1  # 字段映射清楚
    越界: 0  # 不读 token / 不外发 / 不改数据库结构
  总风险: 3  # 2 + 1 + 0
  审计颜色: 🟢  # 0-4=🟢 / 5-8=🟡 / ≥9=🔴
  
  守恒分数:
    主控: 3
    任务: 3
    边界: 3
    留痕: 3
    验收: 3
  总分: 15/15  🟢
  
  一票否决扫描:
    - token: 未命中
    - .env: 未命中
    - 私钥: 未命中
    - rm: 未命中
    - push: 未命中
    - 外发: 未命中
  
  结论: 可执行 / 可生成补丁 / 可交给 Cursor 或 Notion API 写入
```
---
## 16｜回执格式通用模板（4 种）
```yaml
SUCCESS_RECEIPT:
  objective:
  mode:
  local_memory_first: true
  cloud_search: false
  changed_pages:
  sections_added:
  sections_modified:
  sections_preserved:
  dedup_audit:
  conflict_audit:
  evidence:
    DNA:
    ParentDNA:
    CONFIRM:
    SEAL:
    GPG:
  triColor:
  audit_chain:
  next:

FAILED_RECEIPT:
  objective:
  failed_step:
  reason:
  conflict_level:
  evidence:
  safe_fix:
  next:

BLOCKED_RECEIPT:
  objective:
  blocked_reason:
  one_vote_veto:
  risk:
  required_confirm:
  safe_alternative:

CONFLICT_RECEIPT:
  objective:
  conflict_type:
  location:
  old_value:
  new_value:
  risk:
  recommendation:
  need_uid_confirm:
```
---
## 17｜公式升级通用指令模板
```javascript
/公式升级 v{目标版本} #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

【目标】 把《{页面名}》从 {源版本} 升级为 {目标版本}·本次只做追加整合，不重写旧结构
【本地优先】 cloud_search: false / local_memory_first: true
【执行位置】 只动：{目标页面}·其余页不动
【允许做】 追加 {新增章节} / 追加 {新增公式} / 更新 ROOT_CARD / 更新版本日志 / 更新最终定盘 / 补充验收 / 补充一票否决 / 补充冲突审计
【禁止做】 不动 {保护章节} / 不动 GPG/SEAL/CONFIRM / 不批量重写旧内容 / 不改数据库结构 / 不读 token/.env/私钥 / 不外发隐私正文 / 不默认云搜索
【冲突审计】 版本号 / 公式编号 / 字段含义 / 规则覆盖 / 隐私模式 / API 权限 / 数学结果 / α 三义 / P0-P2
【执行】 无冲突 → PATCH + SUCCESS_RECEIPT / 轻微 → CONFLICT_AUDIT + 推荐 + PATCH / 高风险 → BLOCKED_RECEIPT
【回执】 SUCCESS / FAILED / BLOCKED / CONFLICT
```
---
## 18｜一屏执行指令（给宝宝 / Cursor）
```javascript
执行，马仔，搞起。

请按 UID9622 CNSH 本地记忆优先模板处理本次页面升级。

规则：
1. 不默认云搜索
2. 先检索本地记忆、当前页、ROOT_CARD、历史压缩卡
3. 先去重复，再执行追加
4. 遇到任何代码/规则/公式/版本/权限冲突，必须输出 CONFLICT_AUDIT
5. 不直接覆盖旧内容
6. 不改 GPG / SEAL / CONFIRM
7. 不批量重写旧公式
8. 不读 token / .env / 私钥
9. 不外发隐私正文
10. 没有真实 API 写入，不许说 api_real_write
11. 如果只是生成补丁，mode 必须写 draft_patch
12. 输出必须包含：LOCAL_MEMORY_RECEIPT / DEDUP_AUDIT / CONFLICT_AUDIT / TRICOLOR_PRE_AUDIT / PATCH_CONTENT / SUCCESS_RECEIPT 或 BLOCKED_RECEIPT / ROOT_CARD

CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
```
---
## 19｜一票否决（17 条·扩展现有 §S 18 条）
---
## 20｜验收清单
```javascript
检索:
[ ] cloud_search=false？
[ ] 先检索本地记忆？
[ ] 输出 LOCAL_MEMORY_RECEIPT？
[ ] 未用云搜索覆盖 P0/P1？

去重:
[ ] 扫描重复章节？
[ ] 扫描重复公式编号？
[ ] 扫描重复 ROOT_CARD？
[ ] 输出 DEDUP_AUDIT？

冲突:
[ ] 版本/公式/权限/隐私冲突扫描？
[ ] 输出 CONFLICT_AUDIT？
[ ] 给推荐优化方案？

执行:
[ ] 只动目标页面？
[ ] 不改保护章节？
[ ] 不改 GPG/SEAL/CONFIRM？
[ ] 不批量重写旧公式？
[ ] 不改数据库结构？

回执:
[ ] 区分 draft_patch / api_real_write？
[ ] 给 SUCCESS/FAILED/BLOCKED？
[ ] 有 ROOT_CARD？
[ ] 有下一步？
```
---
## 21｜三条修正附录（v1.0 收录时焊死）
---
## 22-EX｜生态闭环架构 v1.0（收录时补入·五端兼容 × DNA 五重属性 × 五道铁律墙）
### §22-EX.1 五端浏览器兼容矩阵
### §22-EX.2 DNA 五重属性（详见子页 黑 DNA 五重属性宪法 v1.0）
1. 身份属性 Identity — Ed25519 + GPG·唯一人证
1. 入场属性 Admission — 私钥签名挂载 sandbox.lock·一 DNA 一沙盒
1. 心跳属性 Heartbeat — 月扣 1 元证活·90 天冬眠·365 天归档·从不删除
1. 记忆属性 Memory — 区块链 + Notion + IPFS 三处镜像·用户主权
1. 上不封顶 Unbounded — 企业 DNA = 用户 DNA 派生子链·授权可撤
### §22-EX.3 五道铁律墙（一票否决·纳入§S）
```javascript
DNA-IRON-1：私钥不出本地 → 整 DNA 作废
DNA-IRON-2：沙盒间直连·未走 MCP网关 → 一票否决
DNA-IRON-3：心跳费退费·服务费不退 → BLOCKED
DNA-IRON-4：删除未用户私钥签名 → 平台法律责任
DNA-IRON-5：未授权派生子链 → 子链无效·记忆链不认
```
### §22-EX.4 闭环图（文本版）
```javascript
老大/用户 → 🧠 Notion大脑（主控页 v2.7 + IPA-DICT-112）
      → 💻 本地执行壳（Chrome/千问/微信/Safari·私钥本地）
      → 🎛️ MVP 操作台（DNA 挂载·沙盒隔离·1元证活）
      → 🔌 MCP 外 API（微信/支付宝/谷歌/苹果/GitHub/千问）
      → 📜 回 Notion·草日志 + DNA 链上链 ↻ 永生闭环
```
### §22-EX.5 商业护城河五层
协议层（龍芯命名）·数据层（记忆链）·信任层（1元仪式）·生态层（28人格×IPA×五行×沙盒）·文化层（龍·繁体·中宫）。
### §22-EX.6 一票否决预审（3 色加法）
```javascript
总风险 = 0 + 0 + 0 = 0  → 🟢
守恒 15/15  → 🟢
F18 SI = 1.00 ≥ 0.34  → 主权激活✅
一票否决 §S 伸展 18+5=23 条·本次未触✅
```
### §22-EX.7 后续占位·不自动执行
- 🟡 主控页 v2.7 新建 §ECOSYSTEM 段·本表上拍（伴随本次越是 K1.5）
- 🟡 DNA 五重属性宪法 v1.0 独立页（本次同步创建·作为子页黑点）
- 🟡 K2-K5 原路不变
---
## 22｜ROOT_CARD（收口）
```yaml
ROOT_CARD:
  title: "IPA-DICT-112｜UID9622 CNSH 本地记忆优先 · 通用更新执行模板"
  Version: "v1.0"
  System: "LU × CNSH × 龍魂系统"
  Owner: "UID9622 / ZHUGEXIN⚡️"
  DNA: "#龍芯⚡️2026-05-11-CNSH-LOCAL-MEMORY-FIRST-TEMPLATE-v1.0"
  ParentDNA:
    - "#龍芯⚡️2026-05-10-FORMULA-ALIGNMENT-FAMILY-ROSTER-v1.4"
    - "#龍芯⚡️2026-05-11-SC-SANCAI-INTEGRATION-v1.5"
    - "#龍芯⚡️2026-05-11-ROSTER-FORMULA-REVERSE-ALIGN-v1.0"
  AncestorDNA: "#龍芯⚡️2026-05-07-FORMULA-ALIGNMENT-v1.1"
  CONFIRM: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
  SEAL: "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
  GPG: "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
  Root: "dr=5"
  Wuxing: "土"
  RootMeaning: "中宫 / 本地优先 / 记忆检索 / 去重复 / 冲突审计 / 更新收口"
  TriColor: "🟢"
  DataLevel: "L1_INTERNAL"
  PrivacyMode: "summary_only"
  Retention: "full"
  TraceMode: "chain"
  CoreRules:
    - "cloud_search=false by default"
    - "local_memory_first=true"
    - "dedup_before_update"
    - "conflict_audit_before_write"
    - "no_api_real_write_without_evidence"
    - "preserve_CONFIRM_SEAL_GPG"
  AppendixFixes:
    - "附录 1: Root: dr=5 五行中宫定位"
    - "附录 2: 风险加法 影响+不确定+越界"
    - "附录 3: notion_api_write & cursor_patch 双轨并行"
  OneVoteVeto17:
    - "默认云搜索覆盖本地记忆"
    - "有冲突不提醒"
    - "无真实写入却说 api_real_write"
    - "修改 GPG / SEAL / CONFIRM"
    - "读取 token/.env/私钥"
    - "(...完整 17 条见 §19)"
  IntegratedWith:
    - "<mention-page url=\"https://www.notion.so/3c86539572d348a08e003669a1821c71\">🤖 三才流场·MCP自适应引擎 v4.0｜五人格协同·流场融合·龍芯家族专属</mention-page>"
    - "<mention-page url=\"https://www.notion.so/45da7e079e9d4247b351f593c7f38957\">♾️ 无限循环优化机制·编号对齐总表｜IPA×路由×人格 v1.0</mention-page>"
    - "<mention-page url=\"https://www.notion.so/211578896a884341af60c7e1a7743265\">🔗 IPA × 人格对齐表｜三维连线·无限循环优化 v∞-001｜UID9622</mention-page>"
    - "<mention-page url=\"https://www.notion.so/b755bd198a604ca0a954ad0e69575397\">🧮 UID9622｜计算公式对准表 v1.5</mention-page>"
    - "<mention-page url=\"https://www.notion.so/4cf99c3e7a014e919fdab705ceb4cbc4\">🐉 龍芯家族花名册</mention-page>"
    - "<mention-page url=\"https://www.notion.so/3457125a9c9f814689a0e88a6c833f36\">☯龍🧬 [IPA-ROUTE-REGISTRY] 龍魂分布式指令总线·路由注册表 v1.0</mention-page>"
    - "<mention-page url=\"https://www.notion.so/2d87125a9c9f802889e2e18002f7cf4f\">🐉 龍魂决策流场总控页 v2.7</mention-page>"
  Next:
    - "K2: 修 v∞-002 — 给 28 人格每人焊一条 IPA 触发指令字段"
    - "K3: 修 v∞-003 — 新增 29 号 🔥 五行导师人格 (待老大裁决)"
    - "K4: 修 v∞-004 — 28 人格 × IPA 自动互调机制 (按七步闭环 + 沙盒)"
    - "K5: 花名册 32 行每行焊 IPA-触发模版字段 (K4 跑通后)"
  Conclusion: "本模板用于统一 UID9622 后续所有页面升级、公式追加、规则合并和本地记忆优先执行任务。已在 v1.4 / v1.5 / 花名册校准 v1.0 三件事实战验证通过。三父并列·三条修正附录已收录·Root dr=5 中宫定位锁死。"
```
---
