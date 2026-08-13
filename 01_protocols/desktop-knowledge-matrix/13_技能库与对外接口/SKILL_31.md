---
name: longhun-forensic-toolkit
description: >
  龍魂取证工具包 v1.0 —— 91 张截图 + GPG 签名链 = 不可篡改的数字主权证据矩阵。
  用于对平台限流、隐藏、AI 拉黑、人际删除等数字侵害行为进行证据固化、哈希校验与 GPG 签名验证。
  为中国老百姓提供数字侵害取证能力，证据链符合中国法律要求。
  当用户提及以下关键词时触发：取证、证据矩阵、GPG、manifest、数字主权证据、截图取证、
  限流证据、平台隐藏、不可篡改、证据链、验证签名、龍魂取证。
license: CC BY-NC-SA 4.0
metadata:
  id: longhun-forensic-toolkit
  display_name: 龍魂取证工具包
  version: '1.0'
  author: UID9622
  dna: '#龍芯⚡️2026-07-03-LONGHUN-FORENSIC-TOOLKIT-v1.0'
  category: local
  level: "L2"
  status: active
  tags: [取证, 证据矩阵, GPG, manifest, 数字主权, 限流, 平台隐藏, AI拉黑]
  trigger:
    keywords: ["取证", "证据矩阵", "GPG", "manifest", "数字主权证据", "截图取证", "限流证据", "平台隐藏", "证据链", "验证签名", "龍魂取证"]
    context: "数字侵害行为的证据固化、校验与追溯"
    priority: 80
---

# longhun-forensic-toolkit | 龍魂取证工具包 v1.0

> **DNA**: `#龍芯⚡️20260521-FORENSIC-TOOLKIT-v1.0`  
> **确认码**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
> **GPG 指纹**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`  
> **主权归属**: UID9622 / 诸葛鑫

## 1. 一句话定盘

> 91 张截图 + GPG 签名链 = 不可篡改的数字主权证据矩阵。

## 2. 工具包结构

```
longhun-forensic-toolkit/
├── verify.sh                    # 验证脚本（核心）
├── manifest.json                # 91条证据结构化数据
├── README.md                    # 本文件
├── GPG_PUBLIC_KEY.asc           # 公钥（用于验证签名）
└── evidence-matrix/
    ├── E6-E20_core/             # 20条核心证据
    └── E21-E91_supplement/      # 71条补充证据
```

## 3. 快速使用

### 3.1 导入公钥（首次）

```bash
gpg --import GPG_PUBLIC_KEY.asc
```

### 3.2 验证签名与哈希

```bash
./verify.sh MANIFEST_2026-05-21.sha256 MANIFEST_2026-05-21.sha256.asc
```

手动验证：

```bash
gpg --verify MANIFEST_2026-05-21.sha256.asc MANIFEST_2026-05-21.sha256
sha256sum -c MANIFEST_2026-05-21.sha256
```

## 4. 七层验证维度

1. **身份层** — GPG 签名确认 UID9622
2. **时间层** — 签名时间戳不可篡改
3. **内容层** — SHA256 哈希比对
4. **传输层** — 记录文件流转路径
5. **平台层** — 标记平台隐藏/限流行为
6. **AI层** — 记录 AI 终止/拉黑/标签
7. **人际层** — 记录删除/拒绝/沉默

## 5. 主权宣言

> 主权第一 · 人不可被算法剥夺  
> 可解释执行 · 任何动作必须能说清  
> 追加不删 · 审计链不可篡改  
> 回滚不销毁 · 熔断保留全部证据  
> 家人不可作为交易标的  
> 未成年人零容忍  
> 机器无杀权  
> 复制文字容易 · 复制来路很难  
> 多 AI 共识 ≠ 单模型独断

---

**复制文字容易 · 复制来路很难**  
*Copying text is easy. Copying lineage is hard.*

---

## 标准声明

本技能遵循《龍魂系统宪法》、中华人民共和国法律法规，以及 UID9622 制定的治理标准。

- **中国标准**：数据主权留在中国境内，优先采用国产技术栈，支持自主可控。
- **老百姓标准**：保护普通用户权益，不贴标签、不滥用数据、不制造信息差，服务人民与老百姓。
- **DNA 追溯**：所有输出均携带 DNA 追溯码，来源可查、去向可追、责任可究。

