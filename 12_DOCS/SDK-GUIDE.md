---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·丙申·癸丑·申时·䷍大有-SDK-GUIDE-v1.0`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
<!-- DNA: #龍芯⚡️丙午·丙申·癸丑·申时·䷍大有-SDK-GUIDE-v1.0 -->

# 🐉 龍魂 SDK · 第三方对接指南

> **第三方如何 pip install / npm install 龍魂能力。**
> 本文档对应揭榜挂帅评估维度 5（可被第三方调用）。

---

## 1. 总览

| 语言 | 包名 | 版本 | 安装命令 | 状态 |
|:---|:---|:---|:---|:---|
| Python | `longhun-tricolor` | 1.1.0 | `pip install longhun-tricolor` | ✅ 已发布 |
| JavaScript | `@longhun/tricolor` | 1.1.0 | `npm install @longhun/tricolor` | 🟡 构建就绪 |

> JS 包发布到 npm 需：npm 账号 + `npm login` + `npm publish`。

---

## 2. Python SDK（推荐）

### 2.1 安装

```bash
pip install longhun-tricolor
# 或指定版本
pip install longhun-tricolor==1.1.0
```

### 2.2 核心 API

| 对象 | 说明 |
|:---|:---|
| `TricolorClient` | 客户端（鉴权 + 评估入口） |
| `Scores` | 六维评分（人权/公平/可控/透明/可溯/隐私） |
| `Verdict` | 判定结果（🟢🟡🔴 + R 分数 + DNA） |

### 2.3 完整示例

```python
from longhun_tricolor import TricolorClient, Scores, VerdictError

client = TricolorClient(token="sk-xxx")

# 单次评估
verdict = client.evaluate(
    action_id="order-2026-001",
    actor="order-service",
    action_type="data_export",
    scores=Scores(
        human_welfare=82, fairness=78, controllability=70,
        transparency=65, traceability=80, privacy=55,
    ),
)
print(verdict.emoji)      # 🟢
print(verdict.status)     # pass
print(verdict.r_score)    # 数字根分数
print(verdict.dna)        # 追溯码
```

### 2.4 错误处理

```python
try:
    verdict = client.evaluate(...)
except VerdictError as e:
    print(f"评估失败: {e.code} {e.message}")
```

---

## 3. JavaScript SDK

### 3.1 源码构建（当前可用方式）

```bash
cd sdk/javascript
npm install
npm run build
# 产物: dist/index.js + dist/index.mjs + dist/index.d.ts
```

### 3.2 使用

```javascript
// CommonJS
const { TricolorClient, Scores } = require("@longhun/tricolor");

// ES Module
import { TricolorClient, Scores } from "@longhun/tricolor";

const client = new TricolorClient({ token: "sk-xxx" });
const verdict = client.evaluate({
  action_id: "web-001",
  actor: "content-moderation",
  action_type: "ai_generate",
  scores: new Scores({
    human_welfare: 85, fairness: 80, controllability: 75,
    transparency: 90, traceability: 88, privacy: 70,
  }),
});
console.log(verdict.emoji, verdict.status, verdict.r_score);
```

### 3.3 发布到 npm（待执行）

```bash
cd sdk/javascript
npm login                    # 需要 npm 账号
npm publish --access public  # @longhun/tricolor
```

---

## 4. 配置项

| 配置 | 说明 | 默认 |
|:---|:---|:---|
| `token` | API 令牌 | 必填 |
| `base_url` | API 地址 | `https://uid9622.cn/api` |
| `timeout` | 超时（秒） | 30 |
| `retries` | 重试次数 | 3 |

---

## 5. 安全与合规

- **许可证**：MulanPSL-2.0（允许商业使用 · 署名）
- **数据主权**：SDK 不上传用户业务数据，仅提交评估分数
- **追溯**：每次评估返回 DNA 追溯码，可审计
- **熔断**：敏感字段自动 MELTDOWN，日志脱敏

---

## 6. 版本与支持

| 项 | 值 |
|:---|:---|
| Python 支持 | 3.8+ |
| Node 支持 | 14+ |
| 文档 | 本文件 + `sdk/python/README.md` |
| Issue | GitHub Issues（模板齐全） |
| 维护 | 高频提交 · CI 全绿 |

---

> 一行安装，三色审计能力即用。
> 复现验证见 [`docs/REPRODUCE.md`](./REPRODUCE.md)


---

## 💛 支持龍魂（纯自愿 · 零黑箱）

龍魂的一切免费开放。若你认可「让技术为人、为普通人生长」，可自愿支持——款项仅用于服务器与开发成本，不留一分私账。

- **收款方式**: SOL / USDC（Solana）
- **实时地址与二维码**: 见官网 [uid9622.cn](https://uid9622.cn) 底部「支持龍魂」区 — 地址由 `lh wallet` 统一管理（公司账户落地后自动切换 · 以官网为准）

> 龍魂不诱导、不施压、不道德绑架。捐与不捐，开放与尊重不变。

<!-- LH-WALLET-SUPPORT -->

```json
{
  "dna": "#龍芯⚡️丙午·丙申·癸丑·申时·䷍大有-SDK-GUIDE-v1.0",
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
