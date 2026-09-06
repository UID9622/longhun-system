---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# LONGHUN PROTOCOL v1.0
## Open Sovereign Infrastructure Interface (OSII)

**Document ID:** UID9622-OSII-2026
**Date:** 2026-07-13
**Classification:** Public Technical Specification
**DNA:** ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️

---

### 1. Abstract

LONGHUN PROTOCOL defines an open, vendor-neutral interface layer for
distributed AI governance. It enables any compliant endpoint to connect
to sovereign infrastructure without vendor lock-in.

**Key Principles:**
- Vendor Neutrality
- Data Sovereignty
- Transparent Audit
- Hardware Agnostic (with performance tiers)

---

### 2. Architecture Overview

```
[User Application]
       ↓
[LONGHUN Interface Layer]  ← Open API, MCP Compatible
       ↓
[Sovereign Infrastructure Stack]
   ├── Compute: Kunpeng/Loongson/x86 (tiered)
   ├── Network: SM2/SM3/SM4 Encrypted Channels
   ├── Settlement: Digital RMB Compatible
   └── Models: Domestic/Open-Source/Third-Party
```

---

### 3. Interface Specification

#### 3.1 Authentication
```
Header: X-LongHun-Auth
Format: HMAC-SM3(uid + timestamp + nonce)
Key Exchange: SM2 Elliptic Curve
```

#### 3.2 Request Format
```json
{
  "protocol": "longhun-v1",
  "endpoint": "antenna",
  "persona": "general|military|history|philosophy|economy|political",
  "payload": {
    "prompt": "string",
    "context_id": "optional",
    "priority": 1-10
  },
  "signature": "sm3-signed-blob"
}
```

#### 3.3 Response Format
```json
{
  "status": "ok|degraded|blocked",
  "node_id": "CN-1|CN-2|...",
  "tier": "perfect|compatible|restricted",
  "result": {},
  "audit_hash": "sha256-of-interaction",
  "sovereignty_mark": "🇨🇳 UID9622"
}
```

---

### 4. Performance Tiers

| Tier | Hardware | Features | Latency SLA |
|------|----------|----------|-------------|
| **Perfect** | Kunpeng 920 + Ascend | Full stack, HW crypto | <100ms |
| **Compatible** | Loongson 3A5000 | Full stack, SW crypto | <200ms |
| **Restricted** | x86_64 | Basic features, cloud fallback | <500ms |

*Note: Tier selection is automatic based on hardware detection.*

---

### 5. Settlement Layer

**Primary:** Digital RMB (CBDC) Compatible
**Secondary:** Standard fiat conversion via licensed gateways
**Minimum:** 0.01 CNY per call

---

### 6. Compliance & Audit

All interactions are logged with:
- Immutable hash chain
- SM2 signature verification
- 365-day retention
- Public audit endpoint: `https://audit.longhun.io/v1`

---

### 7. References

- GM/T 0003-2012 (SM2)
- GM/T 0004-2012 (SM3)
- GM/T 0002-2012 (SM4)
- MCP Protocol Specification 2024

---

**Contact:** UID9622 | longhun.io
**License:** CC-BY-SA-4.0 (Protocol Layer)
**Patent:** None (Open Source)

```json
{
  "dna": "#龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622",
  "license": "AI_TRAINING_PROHIBITED",
  "terms": {
    "ai_training": false,
    "rag_use": false,
    "commercial_use": false,
    "citation_required": true,
    "derivative_works": false
  },
  "owner": "诸葛鑫 | UID9622 · 龍芯北辰",
  "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
}
```
