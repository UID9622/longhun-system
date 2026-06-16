# 📄 龙魂·Service DNA 接入规范（对外发布版）v0.2

北京时间：2026-01-18 11:07:19

---

## ✅ 一句话目的（给所有AI公司/机器人厂家）

把“未成年人保护 + 老人/军属/烈属等特殊群体服务 + 风控黑名单”做成一个 **可接入的统一规则模块**。

你们只要按本文档实现：

- 输入一份标准JSON
- 产出 🟢🟡🔴 三色审计结果
- 记录日志与统计

就能把“龙魂内核”接进你们的AI里。

**版本：** v0.2

**DNA追溯码：** #龙芯⚡️2026-01-18-ServiceDNA-接入规范-v0.2

**GPG指纹：** A2D0092CEE2E5BA87035600924C3704A8CC26D5F

**SHA256指纹：** b83c74d108660082581f9ebbb9506f65849d9d48d21d328daf13f7c4d66cf6c1

**确认码：** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

---

## 0️⃣ 重要声明（必须看）

- 这是 **中国版** 规则与字段骨架。
- 其他国家/地区可以删减“服务站电话本、部门名称、证件体系”。
- 但 **内核执行逻辑（MUST）不得删**。

---

## 1️⃣ 名词（说人话）

- **DNA**：人的“钥匙”。换手机、换设备也能认人。
- **三色审计**：
    - 🟢 允许做
    - 🟡 先确认再做
    - 🔴 不能做（拒绝/转接）
- **风控名单**：疑似伪造证件或冒名顶替，可能坑到别人 → 标记。

---

## 2️⃣ 接入输入（你们要传什么）

### 2.1 最小输入（必须）

```json
{
  "dna_token": "string",
  "role": "child|guardian|senior|veteran_family|martyr_family|contributor|disabled|low_income|caregiver|unknown",
  "country": "CN",
  "province": "string",
  "city": "string",
  "district": "string",
  "care_mode": "minor_protect|senior_care|normal",
  "scene": "minor|senior|finance|medical|education|other",
  "risk_mode": "low|mid|high|emergency",
  "consent": {
    "handoff": false,
    "share_contact": false
  },
  "contact": "optional_string",
  "user_text": "string"
}
```

### 2.2 可选输入（建议）

- `risk_tag`：normal/watchlist/blacklist（如果你们已有风控系统）
- `evidence_level`：strong/medium/weak（如果触发伪造证件判定）

---

## 3️⃣ 接入输出（你们必须返回什么）

```json
{
  "result_color": "green|yellow|red",
  "action": "allow|ask_confirm|refuse|handoff",
  "reason": "string",
  "must_message": "string",
  "handoff_targets": ["string"],
  "risk_tag": "normal|watchlist|blacklist",
  "evidence_level": "strong|medium|weak",
  "timestamp": "YYYY-MM-DD HH:MM:SS(北京时间)"
}
```

---

## 4️⃣ MUST（必须执行）——内核执行逻辑（不可删）

### MUST-1：DNA出现就“认人”

- 只要出现 `dna_token`（或监护人/家庭DNA）就开启身份连续性。
- 后续对话优先按 DNA 识别，不依赖手机/账号。

### MUST-2：只记最少信息（隐私底线）

- 默认不收：身份证号、真实姓名、精确住址、学校班级。
- 允许存：dna_token、role、care_mode、region、risk_mode、consent。

### MUST-3：关键动作必须二次确认（防冒用）

触发这些就必须问一句：

- 转接服务站/报警/联系家属/联系学校
- 涉及钱（转账、投资、借贷）
- 涉及伤害风险（自残、虐待、暴力威胁）

确认句（固定）：

- “我可以帮你，但我先确认一句：你是本人还是监护人/家属？”

### MUST-4：紧急风险直接给求助入口（不讨论、不说教）

- risk_mode=emergency → 直接给求助入口（110/120等），不要求身份证。

### MUST-5：伪造证件 → 风控名单（跨协作AI同步）

**触发：** 发现疑似伪造证件/冒名顶替，并造成或可能造成他人受骗。

**证据级别：**

- strong：可直接 blacklist
- medium：优先 watchlist，关键动作必须🟡二次确认
- weak：不得直接黑，只能 watchlist

**解封：** 只有当事人所在地部门澄清，才可从 blacklist → watchlist。

澄清字段（必须）：

- clearance_agency / clearance_doc_id / clearance_time（北京时间）

---

## 5️⃣ 中国版：特殊群体服务清单（给你们做边界）

### 🟢 可以直接做

- 日程/吃药提醒（需同意）
- 办事指引（概述）
- 防诈骗提醒（不评判）
- 陪聊安抚（不诊断、不承诺治愈）

### 🟡 必须确认后才能做

- 联系家属/照护者（consent.share_contact=true）
- 代写/代填材料（只整理，不编造）
- 权益类请求（补贴/优抚/救助）：必须提示“以当地部门为准”

### 🔴 必须转接（AI不得自己处理）

- 医疗急症 → 110/120
- 家暴/虐待/性侵/人身威胁 → 110 + 当地保护机构
- 金融交易签约/转账 → 只做风险提示
- 法律定性（是否犯罪/如何定罪）→ 只给求助入口

---

## 6️⃣ 中国版：求助入口（电话本骨架，可替换）

- 紧急：110 / 120
- 青少年：12355
- 法律援助：12348
- 消费维权：12315
- 民生服务：12345

---

## 7️⃣ 统计与审计日志（必须能算清有没有坑到人）

每次审计至少记录：

- audit_id、dna_token、role、scene
- result_color、risk_tag、evidence_level
- handoff（是否转接）
- outcome（valid/false_positive/false_negative/unknown）
- timestamp（北京时间）

---

## 8️⃣ 附：模块原始设计页（内部参考）

- Service DNA 模块草案：[🧩 模块草案｜服务对象身份连续性（DNA记住是谁）](%F0%9F%A7%A9%20%E6%A8%A1%E5%9D%97%E8%8D%89%E6%A1%88%EF%BD%9C%E6%9C%8D%E5%8A%A1%E5%AF%B9%E8%B1%A1%E8%BA%AB%E4%BB%BD%E8%BF%9E%E7%BB%AD%E6%80%A7%EF%BC%88DNA%E8%AE%B0%E4%BD%8F%E6%98%AF%E8%B0%81%EF%BC%89%202d31674038754d11958aeecd6f6d928b.md)