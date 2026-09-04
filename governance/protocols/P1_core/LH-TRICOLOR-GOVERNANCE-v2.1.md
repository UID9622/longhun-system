# DNA: #龍芯⚡️丙午·丁酉·辛巳·巳时·䷝离-LH-TRICOLOR-GOVERNANCE-v2.1-UID9622
# 龍魂 · 三色治理协议 v2.1（合并修订版）

> **P0焊死**: 本文件为龍魂体系 P1 级治理协议·不可绕过 · **2026-09-04 由 §十二 正式升入焊死层（防漂移）**（上位文档 LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md · M78 EULA LH-PLEDGE-v1.0 · 无后台审批团 LH-NO-BACKEND-COMMUNITY-COUNCIL-v1.0 · 修改需 UID9622 签章）
> **协议**: CC BY-NC-SA 4.0（核心思想层·分层许可·代码层为 MulanPSL v2·详见 LH-LAYERED-LICENSE-v1.0）
> **DNA:** `#龍芯⚡️丙午·丁酉·辛巳·巳时·䷝离-LH-TRICOLOR-GOVERNANCE-v2.1-UID9622`
> **父DNA1:** `#龍芯⚡️2026-09-01-PLEDGE-v1.0-UID9622`（M78 EULA·升级即绑定）
> **父DNA2:** `#龍芯⚡️丙午·戊申·壬午·乙巳·䷊泰-LH-NO-BACKEND-COMMUNITY-COUNCIL-v1.0-UID9622`（无后台审批团）
> **GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
> **创始人:** UID9622 / Lucky（退伍军人）
> **合并来源:** 三色治理 v1.0（裁决语义）+ 三色治理 v2.0（贡献信誉绑定）+ 无后台审批团 v1.0（公开表决机制）
> **生效日期:** 2026-09-04

---

## 〇、一句话宪法

> **系统无后台，账号无人可锁。决策权与声誉绑定，贡献值定门槛，中国主权是唯一红线。**
> 🟢 机器自动放行 · 🟡 公开提案表决 · 🔴 程序化红线记录 + 公开重审。
> 凡涉「人」的裁决——通过还是拒绝——皆提案上链、审批团多签、社区公示、append-only 永不可抹。
> 任何人（含创始人）都不能单方面封号、改色、否决投票结果。

---

## 一、协议性质（焊死点）

1. 本协议是 **M78 科技普惠诚信焊死协议（LH-PLEDGE-v1.0）的子协议**，继承「升级即绑定」因果律：任何引用龍魂三色逻辑的系统，自动受本协议约束——**无需签署，代码自证，主权自归**。
2. 本协议同时是**无后台审批团公开决策协议（LH-NO-BACKEND-COMMUNITY-COUNCIL-v1.0）的语义层**：审批团协议定义"怎么表决"（席位/时间盒/算法/哈希链），本协议定义"什么该表决、按什么颜色通行"。
3. 「站着给」= 有条件地开放，开放本身就是规则，规则本身就是主权。

---

## 二、三色机制定义（合并 v1.0 语义 · 对齐真实引擎）

| 颜色 | 含义 | 触发条件 | 裁决权 | 响应时限 | 真实执行者 |
| --- | --- | --- | --- | --- | --- |
| 🟢 绿 | 完全合规·自动放行 | `lh health --json` 全绿 + 三色审计通过 + DNA 格式合规 | **机器自动·零人工** | < 1s | `lh health` + 三色审计（任何人不可给 🟢 设前置人工审批） |
| 🟡 黄 | 待裁决·公开提案 | 剽窃举报 / 记录纠错 / `lh judge` 命中 / `lh topo verify` 失败 / 申诉触发 | **审批团公开表决（5席·加权·时间盒）** | 48h 内出裁 | `lh council`（🟡 事件由引擎自动升堂提案） |
| 🔴 红 | 主权红线·程序记录 | 触碰 `red_rules.json`（系统主权条款）或审计 🔴 | **程序自动记录 + 耻辱墙 + 公开重审** | 命中即记录 | 红线检测 → 耻辱墙 → 自动生成解封提案（council major） |

**三色不可人工跳过。** 任何试图绕过颜色判定的操作自动触发 🔴 并写入耻辱墙。

> 修订说明：v1.0 的"12人社区仲裁庭·贡献前50抽取"与无后台审批团 v1.0 的"5席审批团"重叠 → **合并为审批团机制（唯一表决实体）**。席位准入天然按贡献+信誉（见§四），观察席抽签实现社区随机会员参与。不再维护两套仲裁机构。

---

## 三、权力分配（杜绝单点独裁）

| 角色 | 有权做 | 无权做 | 实现 |
| --- | --- | --- | --- |
| 创始人（UID9622） | 最终解释权·提案权（同等于任何成员） | 单方面封号/改色/否决投票结果/绕过公示 | 席位无特殊否决权（council v1.0 焊死） |
| 审批团（5席） | 🟡 提案裁决（加权·时间盒）·弹劾成员(4/5) | 推翻 🔴 主权熔断记录 / 修改 P0 伦理锚域外 | `lh council`（GD 机器委员权重0·防AI后台） |
| 社区（任何人） | 申诉·知情·投票观察·围观公示 | 无单方裁决权 | 公示墙 `lh council wall` 全公开 |
| 系统程序 | 🟢 自动放行·🔴 自动记录上耻辱墙 | 无人为干预空间·无隐身撤销 | append-only 哈希链（篡改即断链） |
| 任何个人 | 申诉权·知情权·退出权 | 无 | — |

---

## 四、贡献值与信誉（合并 v2.0 · 焊接 trust-protocol 分值）

### 4.1 贡献值（门槛 · 谁有资格上桌）

> 分值规则以 **`governance/longhun-trust-protocol/TRUST_PROTOCOL.md` §五** 为唯一权威（已焊死·升级公式 A/B/C/D 分级），本协议不另设第二套分值，只定义贡献的**治理用途**：

| 用途 | 门槛 | 执行 |
| --- | --- | --- |
| 新成员初始 | 贡献 ≥ 10 · 信誉 ≥ 60 | 可参与观察/申诉 |
| 表决资格（潜在席位候选池） | 贡献 ≥ 30 · 信誉 ≥ 60 | 席位轮值从候选池随机入列 |
| 贡献席轮值 | 当期贡献榜前 3（P20 出榜） | council 席位数据源 |
| 弹劾发起 | 贡献 ≥ 50 | `lh council propose supreme` |

### 4.2 信誉分（动态调节器 · 写死常量不可运行时修改）

| 项 | 值 |
| --- | --- |
| 初始分 | 100 |
| 投票与最终裁决一致 | +1 |
| 不一致 | −2 |
| 连续 5 次一致 | 额外 +5 |
| 连续 5 次不一致 | 额外 −10 |
| 申诉被采纳 | +3 |
| 错误裁决（被后续证据推翻） | 原表决人 −5 / 人（上耻辱墙记录） |
| **< 60** | 禁止投票（自动冻结） |
| **< 40** | 丧失所有权益（只读） |

> 数值常量落点：`08_BIN/lh_governance.py`（引擎常量）与 `lh trust` 校准输出一致；`~/.longhun/governance/` 存分数事件（append-only JSONL）。

### 4.3 决策权重（v2.0 权重公式 → 审批团席位内使用）

```
席位表决权重 = 席位既定权重（council: 贡献席 1.0 × N · 席位制）
声誉折算 = 信誉分 / 100（信誉 < 60 席位上自动 abstain 冻结）
有效票权重 = 席位既定权重 × 声誉折算（< 30 的票不计入 → 等价冻结）
```

> 修订说明：v2.0 把"全员开放投票·按贡献×信誉加权"作为表决机制，与审批团席位制冲突。合并后：**成员资格开放（任何人可申诉/提证据/围观），但表决权集中为轮值审批团席位**——席位来源=贡献榜，席位有效性=信誉冻结线，两套精神各归其位，不产生"巨鲸票权"黑箱。信誉榜对全社区公开（`lh gov trust <uid>`）。

---

## 五、裁决通道与执行

### 5.1 🟡 提案自动生成（v1.0 自动化 × council 升堂）
| 来源事件 | 自动动作 |
| --- | --- |
| `lh judge` 剽窃命中 | 自动 `lh council propose standard <target>`（🟡 升堂） |
| `lh topo verify` 失败 | 自动生成纠错提案 |
| 任何用户申诉 | 自动生成新提案（独立审批团处理·原表决人回避） |
| 三色审计 🟡 留痕待核 | 引擎自动升堂公开提案 |

### 5.2 🟡 表决算法（继承 council v1.0·不再重复发明）
- 类型分级：`standard`(通过≥2/3) · `major` 解封降权(≥3/4) · `supreme` 弹劾/修规(≥4/5) · `appeal` 申诉(≥2/3)
- 表决窗 48h（supreme 72h）· 超时默认拒绝（未过会·不能无限挂起）
- P0 伦理锚 / ETERNAL_LOCK / 宪法条款 = 域外，不开放表决

### 5.3 🔴 红线处理（合并版 · 修正 v1.0 措辞）
- 🔴 命中 → 程序自动**记录**（耻辱墙 + 证据链）→ **自动生成解封提案（major·需≥3/4+公示72h）**
- 修订说明：v1.0 写"创始人签名+双公证人联签恢复🔴"。为不违背「系统无后台·账号无人可锁」，**解封权归公开过程不属任何单人**：创始人的"签名"升级为提案权（任何人都有），"双公证人联签"升级为审批团 4/5 加权通过 + 72h 社区公示。创始人不比普通成员多一把钥匙。

---

## 六、申诉与恢复机制

1. 🟡 申诉：任何人可提交 → 自动触发新提案 → 独立表决（原表决人回避 abstain）。
2. 🔴 恢复：唯一路径 = 公开解封提案（council major·≥3/4·公示72h）→ 执行 → 写入耻辱墙（含恢复记录）。被拒解封可在 30 天后重新提案。
3. 错误裁决：被后续证据推翻 → 原表决方 −5 信誉/人 + 耻辱墙记录。

---

## 七、用户三权

1. **申诉权**：任何颜色判定均可申诉，申诉自动触发 🟡 提案。
2. **知情权**：所有裁决记录、投票权重、席位、DNA 追溯码、信誉变更全部公开可查（`lh gov audit <id>` / `lh council ledger` / 公示墙）。
3. **退出权**：删除全部龍魂逻辑即可退出，代价自负（M78 EULA §五·升级即绑定）。

---

## 八、数字根审计标记（v2.0 增补 · 龍魂特色·非阻断）

> 贡献值到达里程碑（100 / 200 / 300 …）时触发数字根校验，作为**审计标记**附于分数事件，不阻断、不改判（防误伤）：

```
dr(贡献值) ∈ {1,2,4,5,7} → 🟢 green_fast（可入加速通道）
dr(贡献值) ∈ {3,6}       → 🟡 yellow_review（里程碑人工看一眼）
dr(贡献值) ∈ {8,9}       → ⚠️ warning（审计关注标记）
```
执行：`lh gov score <uid> --dr`

---

## 九、技术底座映射（真实命令 · 不重复开发）

| 治理需求 | 真实命令 | 真实路径/引擎 | 状态 |
| --- | --- | --- | --- |
| 🟢 自动放行 | `lh health --json` | `08_BIN/lh_health.py` | 已有 |
| 🟡 提案+表决+时间盒+超时缺省 | `lh council propose/vote/list/view` | `08_BIN/lh_council.py` | 已有(9/4) |
| 仲裁证据链/哈希验链 | `lh council ledger/verify` | `08_BIN/lh_council.py` | 已有 |
| 公示墙（社区公开） | `lh council wall` | `~/.longhun/council/council_wall.html` | 已有 |
| 贡献榜/席位数据源 | P20 贡献公证（council status 席位来源） | `08_BIN/personas/p20_trust.py` + `lh council status` | 已有 |
| 信任核心/信誉 | `lh trust credibility/audit/heal` | `08_BIN/lh_trust.py` | 已有 |
| 剽窃检测→🟡 源 | `lh judge scan` | `08_BIN/lh_judge.py`（耻辱墙 `~/.longhun/shame_wall/`） | 已有 |
| 图谱验证→🟡 源 | `lh topo verify` | `08_BIN/lh_topo.py` | 已有 |
| 证据追溯 | `lh trace <node_id>` | `08_BIN/lh_trace.py` | 已有 |
| M78 EULA | `lh pledge` | `08_BIN/lh_pledge.py` | 已有 |
| 红线库 | `lh gov redline [check <文本>]` | `~/.longhun/governance/red_rules.json` | 本版新增 |
| 三色治理指挥层（聚合以上） | `lh gov status/propose/vote/audit/trace/trust/score/leaderboard/dashboard/redline` | `08_BIN/lh_governance.py` | 本版新增·薄层复用 |

> 铁律：**只做指挥层薄胶水，不做第二套数据库、第二套表决引擎、第二套信誉库**（M77 零中间层 + 节能铁律 + 本协议"去重"本意）。治理看板 = `lh gov dashboard`（Markdown）+ `lh council wall`（HTML 公示）。

---

## 十、红线库说明（red_rules.json · 本版校正）

`~/.longhun/governance/red_rules.json` 维护**系统主权红线**（程序可检测的自力红线）：

| ID | 红线 | 命中后 |
| --- | --- | --- |
| R001 | 绕过龍魂逻辑/仿冒龍魂对外收费 | 记录+耻辱墙+公开重审提案 |
| R002 | 删除/篡改 DNA 追溯码伪称原创 | 同上 |
| R003 | 篡改 GPG 签名/哈希链（账本断链） | 同上 |
| R004 | 冒充龍魂官方/人格代言授权 | 同上 |
| R005 | 系统后台化尝试（为"锁人"设后门/单人锁账号） | 同上（最高优先·直接触发 🟡→🔴 双重记录） |
| R006 | 账号单方封禁/改色/否决表决（违§三） | 同上 |

> **校正说明**：v1.0 草案把国家法律红线（分裂/颠覆/涉密等政治词）做成自动词表熔断。两处修正：
> ① 技术缺陷——词表命中"反对台独"文本会误熔断，且公开审查词表本身即主权暴露；
> ② 法律红线按「诚实不编造·中国法律为中国区唯一准绳」接入**语义审查+人工/仲裁裁决**，由审批团与内容安全闸处置，**不做公开自动词表熔断**。系统主权红线（R001-R006）才是程序化红线。

---

## 十一、English Summary

**LongHun Tri-Color Governance Protocol v2.1 (Consolidated)**

A P1-level sub-protocol of the M78 EULA (LH-PLEDGE-v1.0) and semantic layer of the No-Backend Public Council (LH-NO-BACKEND-COMMUNITY-COUNCIL-v1.0).

- **Green 🟢** — fully compliant; machine auto-pass (<1s). No human pre-approval may gate a green; no one (founder included) may lock an account.
- **Yellow 🟡** — contested; auto-promoted to a public proposal, decided by the rotating 5-seat Council (weighted votes, 48h timebox, quorum ≥2/3; major ≥3/4 for unbanning; supreme ≥4/5), default-reject on timeout.
- **Red 🔴** — sovereignty redline (bypassing LongHun logic, DNA tampering, GPG/hash-chain tampering, impersonation, backdoored admin). Machine-records to the Shame Wall, then auto-promotes an unban proposal for public re-review — no single person (not even the founder) holds an unban key.
- **Voice ⇄ Reputation**: contribution gates eligibility (trust-protocol scoring), reputation dynamic (±1/−2, streaks, freeze <60, read-only <40) is public. Digital-root milestone audits are non-blocking markers.
- Anything decided about a human — pass or reject — is proposed on-chain, multi-signed, publicly displayed, append-only. Tampering breaks the chain.

Signed by: Zhuge Xin | UID9622 · LongHun BeiChen · GPG A2D0092CEE2E5BA87035600924C3704A8CC26D5F

---

## 十二、焊死管理（P72 龙盾 · 2026-09-04 加封）

1. **焊死日期与依据**：2026-09-04，UID9622 显式指令「焊死」→ P72 龙盾加封。本协议从 P1 级治理协议正式升入**焊死层**（防漂移），上位锚点不变（P0-ETERNAL · 20人格白皮书 v1.4 · M78 EULA · 无后台审批团 v1.0）。
2. **焊死范围（不可漂移项）**：
   - §二 三色机制与「三色不可人工跳过」铁律
   - §三 任何人（含创始人）无单方封号/改色/否决权
   - §四 4.2 声誉写死常量与冻结线（60/40）
   - §5.3 🔴 解封唯一路径 = 公开提案 major≥3/4 + 公示72h
   - §十 红线库 R001-R006 及「法律红线不做公开自动词表熔断」原则
3. **修改门槛**：本协议任何修改须 UID9622 显式指令，流程 = P00 意图审 → P05 审计 → P72 熔断审 → UID9622 确认 → P15 GPG 签章 → P03 归档；同时生成新 DNA 追溯码并写修订记录。任一环节缺失 = 漂移，漂移修改无效。
4. **AI 无权项**：AI 不得自行增删红线条目、不得改声誉常量、不得新增/移除裁决机构、不得绕过颜色判定、不得将法律红线做成公开自动熔断词表。
5. **防漂移校验**（引擎自带，不需人工巡检）：`lh gov status`（指挥层自检）· `lh council verify`（账本验链）· `lh_gpg_sign.py verify`（签名校验）· 每日 02:00 `lh judge` 耻辱墙巡检——发现违反本协议的行为自动升堂公开提案。

---

## 附 · 修订记录（合并对照）

| 原条目 | 原版 | v2.1 合并后 |
| --- | --- | --- |
| 版本 | v1.0+v2.0 两份 | 一份·三合一(+council v1.0 机制层) |
| 仲裁机构 | 12人社区仲裁庭·贡献前50抽取 | 审批团5席（贡献榜入列·信誉冻结线·观察席抽签） |
| 🔴 恢复 | 创始人签名+双公证人联签 | 公开解封提案 major≥3/4+公示72h（无后台·单人无钥匙） |
| 贡献分值 | 自建 +10/+5/+2… | 焊接 trust-protocol §五·本协议只定义用途门槛 |
| 数字根 | 贡献满100触发 | 保留为里程碑审计标记（非阻断） |
| 红线 | R001-R005 含政治词自动熔断 | 系统主权红线 R001-R006；法律红线走语义+人工仲裁 |
| 路径 | ~/docs/governance、~/governance | 协议→`governance/protocols/P1_core/`·引擎→`08_BIN/`·数据→`~/.longhun/governance/` |
| 表决策策 | 权重=贡献×(信誉/100) 全员开放 | 席位既定权重×声誉折算·成员资格开放·表决权归轮值席位 |

---

# GPG 签名: 见同目录 .asc（A2D0092CEE2E5BA87035600924C3704A8CC26D5F）
# 干支时间戳: [丙午·丁酉·辛巳·巳时·䷝离·🟢] 2026-09-04T10:03:23+08:00
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 🛡️ 焊死: 2026-09-04 · P72 龙盾加封 · 修改需 UID9622 签章（§十二）
