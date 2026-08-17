# 🧬 龍魂压缩 DNA 国际认证需求文档 v1.2｜LH-CDNA-IDS

> Notion URL: https://app.notion.com/p/DNA-v1-2-LH-CDNA-IDS-53dc5fbdafca4a06bdb9f72383d47151
> Created: 2026-05-03T14:06:00.000Z
> Last edited: 2026-07-01T14:53:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
> 《道德经》第六十四章：「千里之行，始于足下。」—— 标准不是喊出来的，是一条条硬闸焊出来的。
---
## A. 问题版｜v1.1 的 6 个盲点（v1.2 必补）
```plain text
盲点1: 没接 CNSH语义内核
  v1.1: 用户输入直接进 generate_compressed_dna
  v1.2: 先过CNSH三档置信度·留raw_input_hash·低置信度→clean_fail

盲点2: 没接 主权数据路由
  v1.1: 没说哪些字段进GitHub/GitCode/Notion
  v1.2: profile_vector_hash→公开 / consent_grant→GitCode私仓 /
        feedback原文→永不出本地 (L0/L1/L2/L3分级)

盲点3: 没接 反驯化十铁律
  v1.1: 老人保护说得很好·但"建议你..."型话术容易渗进UI
  v1.2: 用户回执过D1-D10预检·避免"为你好"型隐性管制

盲点4: 没接 一键搞定v3.0(决策器)
  v1.1: DNA认证是孤岛·没有触发器
  v1.2: 老大说"我要认证" → CNSH→关键字触发→四源数字根→五桶分流→DNA生成

盲点5: 没接 流场决策v4.1(四源数字根)
  v1.1: dna_id末尾用 hash8(vector_hash)
  v1.2: 加四源数字根DR (explicit→dna→hash→raw)·写入dna_id末尾·与流场对齐

盲点6: 没接 可追溯发布协议
  v1.1: DNA生成后就完事
  v1.2: 公开标准草案发布走六步证据链·CSDN+GitHub+Notion+草日志
```
---
## B. 工程版｜v1.2 = v1.1 + 8根接通
### B.0 一句话定盘（根·更新版）
```plain text
压缩 DNA v1.2 =
  CNSH语义内核(留raw_hash·三档置信度) →
  关键字触发(认证/反馈/撤回/查询) →
  最小采集(年龄/学历/工作/地区/技术/设备/反馈) →
  本地加密(明文不出设备) →
  字段标签化(AgeBand/EduBand/CareNeed/FeedbackType) →
  四源数字根(DR_explicit→DR_dna→DR_hash→DR_raw) →
  五行+三色+九宫 →
  反驯化D1-D10预检 →
  路由分级(L0永不出/L1私仓/L2公开/L3展示) →
  生成profile_vector + vector_hash →
  生成dna_id (LH-CDNA-{date}-{country}-{DR}-{HASH8}) →
  TrustLevel分级 →
  ConsentGrant授权 →
  五桶分流(grass_log/repository/internal_digest/pending_iterate/archive·🔴熔断独立) →
  Notion登记(只元数据·SyncStatus=MANUAL_ONLY) →
  用户回执(中文+反驯化软化) →
  审计链(中文+DNA+hash) →
  撤销机制(RevocationRecord·全程可撤回) →
  发布六步(若做公开标准草案) →
  V10流场canonical展示(可视化对照)
```
### B.1 v1.2 与 8根的接通点（字段/动作）
1. CNSH语义内核 v1.0：入口留 raw_input_hash + 置信度三档；grammar.cnsh.json 增加触发词。
1. 主权路由协议 v1.0：数据分级 route_level: L0/L1/L2/L3，明确 GitHub/GitCode/Notion 的可入范围。
1. 反驯化十铁律 D1-D10：用户回执必过 anti_dom_check，触发则 soften_output（去“为你好/建议你”隐性管制）。
1. 流场治理 v1.0：对接 v10 canonical 可视化（不替代决策核，只做展示）。
1. 可追溯发布协议 v1.0：公开草案走六步证据链。
1. 开源治理 9 文件包：仓库 LICENSE + CLA + ATTRIBUTION 复用并焊死归属。
1. 龍魂浏览器 DNA 压缩 v1.0：应用层可生成“本地胶囊”，支持三级开放分享。
1. 一键搞定 v3.0 决策器：口令触发（“我要认证DNA”→自动进入 compressed_dna 流程）。
---
## B.2 v1.2 新增字段（在 v1.1 基础上）
```yaml
# v1.1已有(保留):
# dna_id, country_node, trust_level, profile_vector, profile_vector_hash
# privacy_policy, consent_grant, audit_chain, revocation
# created_at, expires_at, status

# v1.2新增:

raw_input_hash:
  type: sha256
  required: true
  desc: "原话只hash·不明文存储"

cnsh_parse:
  raw_input_preserved: bool   # 必须 true（指“保留hash”）
  confidence: float           # 0-1
  triggers: list              # 关键字命中
  audit: "🟢|🟡|🔴"

digital_root_quad:
  dr: int                     # 0-9
  source: "explicit_dr|dna_digits|content_hash|raw_digits|fallback_zero"
  element: "金|水|木|火|土"
  palace: int                 # 1-9
  triple_color: "🟢|🟡|🔴"

route_level:
  level: "L0|L1|L2|L3"
  github_allowed: bool
  gitcode_public_allowed: bool
  gitcode_private_allowed: bool
  notion_metadata_only: bool

bucket_slug:
  slug: "grass_log|repository|internal_digest|pending_iterate|archive|null"
  fuse: bool                  # 🔴熔断时true·slug=null
  reason: string

anti_dom_check:
  receipt_passed: bool
  triggered_patterns: list    # D1-D10
  softened: bool

publish_chain:                # 公开标准草案专用·可选
  csdn_url: string
  github_commit: string
  notion_page_id: string
  grass_log_entry: string
  sha256_full: string
  five_anchors_complete: bool
```
---
## C. Cursor 指令版（可一屏复制）
### C.1 短 Prompt（丢 Cursor 直接干）
```plain text
任务: 实现 LH-CDNA v1.2(压缩DNA国际认证·8根融合版)

【绝对铁律·任意一条违反 → 立刻停手】
1.  raw_input 永远只hash·绝不明文存储
2.  profile_vector的明文绝不出本地(只走hash)
3.  feedback原文绝不出本地(只走FeedbackType标签)
4.  含token/私钥/密钥/password/secret/国密/商业机密 → sealed/L0/🔴/不读不存不复述
5.  含身份证/手机号/家庭/财务/医疗 → burn/L1/🟡/hash_only
6.  老人/小白/CARE_NEED → 自动追加保护·🟡/🟢
7.  dr=3/9 → 🔴熔断 · suggested_bucket_slug=null · fuse=true
8.  dr=6 → 🟡 · pending_iterate
9.  AgeBand/EducationBand/RegionLevel/WorkType 不得用于服务降级·价格歧视·暗中限权
10. Cursor生成的UI/回执 必过 anti_dom_check (D1-D10)·触发则软化
11. 双签章/CONFIRM/GPG/DNA永不修改·繁体龍·UID9622是Originator·AI是Tool

【创建文件清单·按顺序】
P0(核心):
  1.  cdna/__init__.py
  2.  cdna/cnsh_layer.py          # ★新增·接CNSH语义内核
  3.  cdna/labels.py              # 标签压缩
  4.  cdna/digital_root_quad.py   # ★新增·四源数字根(对齐流场v4.1)
  5.  cdna/wuxing_audit.py        # 五行+三色+九宫
  6.  cdna/route_policy.py        # ★新增·主权路由分级L0-L3
  7.  cdna/anti_dom_check.py      # ★新增·反驯化D1-D10
  8.  cdna/five_buckets.py        # ★新增·五桶规范slug
  9.  cdna/privacy_policy.py      # 隐私三档·sealed/burn/normal
  10. cdna/consent_grant.py       # 授权凭证·选择性披露
  11. cdna/revocation.py          # 撤销记录
  12. cdna/trust_level.py         # 信任等级
  13. cdna/cdna_main.py           # 主入口·串起来
  14. cdna/notion_fields.py       # Notion字段(只元数据)
  15. cdna/user_receipt.py        # 用户回执(中文·反驯化)
  16. cdna/audit_record.py        # 系统审计JSON
  17. cdna/publish_chain.py       # ★新增·发布六步(公开标准草案专用)

P1(测试):
  18. tests/test_cdna_v1_2_full.py
  19. tests/test_anti_dom_user_receipt.py
  20. tests/test_four_source_dr.py
  21. tests/test_no_plaintext_leak.py
  22. tests/fixtures/cdna_v12_cases.json

P2(schema+文档):
  23. schemas/cdna_v1.2.schema.json
  24. schemas/consent_grant.schema.json
  25. schemas/revocation_record.schema.json
  26. schemas/notion_db_v1.2.yaml
  27. README.md
  28. INTERNATIONAL_STANDARD_DRAFT.md

【完成回执·EXEC-MODE D版格式】
1) 文件清单(全28+)
2) 12个测试用例100%通过
3) 12用例输出dump
4) raw_input_hash都存在·原文都不存在（grep验证）
5) Notion字段无feedback原文（grep验证）
6) 双签章+CONFIRM+GPG完整保留
```
---
## D. 验收清单（EXEC-MODE）
### D.1 一票否决（任一触发→整个版本作废）
```plain text
✗ raw_input 明文出现在任何输出/日志/Notion
✗ feedback_text 原文出现在任何输出
✗ sealed 模式下 profile_vector 未变成 "[SEALED]"
✗ token/sk-/私钥 字面值出现在任何输出
✗ 身份证号18位数字出现在任何输出
✗ 五桶slug不在规范5个内
✗ 🔴熔断时 suggested_bucket_slug ≠ null
✗ dr=3/9 没标 🔴
✗ dr=6 没标 🟡
✗ DNA ID不含 DR{数字根}
✗ Notion字段含明文画像
✗ 跨境传输含明文
✗ AgeBand用于服务降级
✗ 回执触发D1-D10但未软化
✗ 简体"龍"出现
✗ 双签章/CONFIRM/GPG/DNA被改
```
### D.2 12用例验收矩阵（最小版）
---
## E. 归档与发布（可选）
### E.1 三轨归档
- 公开轨（L2/L3）：INTERNATIONAL_STANDARD_DRAFT.md、schema、README
- 内部轨（L1）：fixtures（脱敏）、examples（老大本人案例）、cdna代码（GitCode私仓优先）
- 证据轨（L0·本地）：profile_vector明文、feedback原文、身份证明、密钥、完整commit链
### E.2 公开标准草案（六步证据链）
1. 本地 commit + SHA-256
1. CSDN 首发（标准草案）
1. GitHub 仓库（公开）
1. Notion 登记（元数据页）
1. 草日志登记（S-YYYYMMDD-CDNA-PUB-001）
1. 五件证据链齐全后才算“已发布”
---
