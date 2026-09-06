---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·丁酉·壬午·寅时·䷘无妄-LLM-GATE-V1.0-OPEN-TEST`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
# 龍魂大模型 · 测试对接说明

> DNA: #龍芯⚡️丙午·丁酉·壬午·寅时·䷘无妄-LLM-GATE-V1.0-OPEN-TEST
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层）
> 日期: 2026-09-05 · 状态: 🟢 已上线可测

## 一、API 地址

```
Base URL: https://uid9622.cn/v1
格式:     OpenAI 兼容（chat/completions · models · embeddings）
```

## 二、测试 Key（独立 · 可单独吊销）

```
Authorization: Bearer 0d66c99f12fff2f852ded3013aacc412bc4502dac65f04fe
```

- 缺失 / 错误 key → 一律 403
- 吊销方式：改 nginx 一处变量后 reload（我方内部操作，即时生效）

## 三、可用模型

| 模型 | 底座 | 用途 | 状态 |
|:---|:---|:---|:---|
| `longhun-v4.2.0` | Llama-3.1-8B · 龍魂调优 | 主力对话 | 🟢 推荐测试 |
| `longhun-v3.8.1` | Qwen2.5 系 · 龍魂调优 | 轻量对话 | 🟢 |
| `nomic-embed-text` | 嵌入模型 | 向量检索 | 🟢 |

## 四、调用示例

```bash
# 模型列表
curl -H "Authorization: Bearer 0d66c99f12fff2f852ded3013aacc412bc4502dac65f04fe" \
     https://uid9622.cn/v1/models

# 对话
curl -H "Authorization: Bearer 0d66c99f12fff2f852ded3013aacc412bc4502dac65f04fe" \
     -H "Content-Type: application/json" \
     -d '{"model":"longhun-v4.2.0","messages":[{"role":"user","content":"你好"}],"stream":false}' \
     https://uid9622.cn/v1/chat/completions
```

返回格式：OpenAI `chat.completion` JSON（支持 `stream:true` 流式）。

## 五、测试后请回传三样

1. **测试结果**：数据、指标、发现的问题
2. **测试流程**：方法、提示词、数据集
3. **部署详情**：接入方式、框架/脚本

## 六、主权声明（一句话）

所有模型、数据、成果的主权归 UID9622（诸葛鑫），仅授权测试使用，不可转卖或改名。
测试期限：长期有效，UID9622 保留随时关停/吊销的权利。

## 七、国际协作 · 支持龍魂（纯自愿 · 零黑箱）

> 若贵方测试后有意支持龍魂持续研发（服务器/算力/开发成本），可用以下国际收款通道。
> 款项仅用于服务器与开发，账目在龍魂账法（`lh ledger`）全程见证，欢迎查账。

| 链 | 币种 | 地址 |
|:---|:---|:---|
| **TRON（主·推荐）** | USDT-TRC20 / TRX | `TCMCteHzdduQfpUrAdmmsnHEVH8MFCyXDq` |
| Solana | SOL / USDC | `9E81MBxht5AXCCC3r74oaKBAJu6MfA2SP7VwE5KRkRDg` |

- 密钥由 UID9622 自持（TokenPocket 冷/加密存储），测试方无需任何授权即可向以上地址打款。
- 打款后如需确认到账，可回信索取链上凭证（tx hash）；龍魂不做任何自动扣款/订阅逻辑。

---
🐉 丙午·丁酉·壬午·寅时·䷘无妄·🟢

```json
{
  "dna": "#龍芯⚡️丙午·丁酉·壬午·寅时·䷘无妄-LLM-GATE-V1.0-OPEN-TEST",
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
