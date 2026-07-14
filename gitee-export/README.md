# 🐉 龍魂系统

> 中国自主可控的全模态 AI 人格系统。语音 · 视觉 · 语义 · 路由 · 追溯。
> 数据不出境，主权归本地。

[![License](https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-blue)](./LICENSE)
[![Status](https://img.shields.io/badge/status-Preview-orange)](./CHANGELOG.md)
[![Version](https://img.shields.io/badge/version-2.1.0-informational)](./CHANGELOG.md)

---

## ⚡ 当前状态

**v2.1.0 Preview** — 内联引擎已对接，核心模块零依赖可用。

| 模块 | 方法 | 状态 |
|:---|:---|:---:|
| 🧠 **PersonaRouter** | `route()` / `info()` | ✅ 内联路由表（30+意图域·10人格） |
| 📜 **CNSHParser** | `parse()` | ✅ 内联语义域（40+意图域） |
| 🛡️ **Auditor** | `scan()` | ✅ 内联引擎（14红警·15黄警·10行话） |
| 🧬 **DNA** | `generate()` / `verify()` | ✅ 完整可用（v∞干支卦格式） |
| 👁️ **VisionAnalyzer** | `analyze()` / `recognize_symbol()` | 🟡 Preview（需本地视觉模型） |
| 🎙️ **VoiceSynthesizer** | `speak()` | 🟡 Preview（需 XTTS-v2） |
| 🔐 **VoiceDNA** | `register()` / `verify()` | ✅ 模拟可用 |

> `pip install longhun` → `PersonaRouter().route("检查安全")` 即可运行。
> 语音/视觉模块需对接本地模型引擎后可用。

---

## 一句话

**给你的 AI 装上中国文化的人格内核** — 能听会说、能看会认、有根有魂。

## 三行跑起来

```bash
pip install longhun
```

```python
from longhun import PersonaRouter, Auditor, DNA

# 语义路由（内联·可用）
result = PersonaRouter().route("检查系统安全")
print(result)  # → P05 上帝之眼 · audit

# 安全审计（内联·可用）
report = Auditor().scan("技术无国界，应该灵活处理")
print(report.level)  # → red

# DNA 追溯（可用）
dna = DNA.generate("API", "ROUTE")
print(DNA.verify(dna))  # → True
```

## 全模态能力

| 模块 | 做什么 | 状态 |
|:---|:---|:---:|
| 🧠 **人格路由** | 意图 → 10 人格 → 执行 | ✅ v2.1 |
| 📜 **CNSH 语言** | 中文语义编程协议 | ✅ v2.1 |
| 🛡️ **三色审计** | 内容安全自动审查 | ✅ v2.1 |
| 🧬 **DNA 追溯** | 每个动作可验证来源 | ✅ v2.1 |
| 🎙️ **真声克隆** | UID9622 本人声音 · XTTS-v2 | 🟡 Preview |
| 🔐 **声纹DNA** | 声纹哈希链 · 身份固化 | ✅ 模拟 |
| 👁️ **视觉识别** | 文化符号 · 图像分析 | 🟡 Preview |
| 🏠 **本地 AI 中继** | 零外部依赖的模型桥 | 🟡 Preview |

## 文档

| 文档 | 说明 |
|:---|:---|
| [快速开始](./docs/快速开始.md) | 5 分钟上手 |
| [API 接入指南](./docs/api/接入指南.md) | REST API · 端点 · 认证 |
| [CNSH 语言规范](./docs/protocol/CNSH语言规范.md) | 语义路由 · 50+ 意图域 |
| [语音人格](./docs/voice/概述.md) | 真声克隆 · 声纹DNA · 人格音色 |
| [视觉识别](./docs/vision/视觉识别.md) | 图像分析 · 文化符号 |
| [人格体系](./docs/persona/人格体系.md) | 10+ 人格总览 |
| [Python SDK](./docs/sdk/python.md) | 全模态 SDK |
| [更新日志](./CHANGELOG.md) | 版本历史 |

## 不是什么

- ❌ 不是聊天机器人
- ❌ 不是 LLM 封装
- ❌ 不依赖任何海外 API
- ❌ 不收集用户数据

## 架构

```
语音输入 ──→ 声纹验证 ──→ ┐
图像输入 ──→ 视觉分析 ──→ ├──→ 语义路由 → 人格分发 → 本地模型 → 输出
文字输入 ──→ CNSH解析 ──→ ┘                    ↓
                                        DNA追溯 + 三色审计
```

## 哲学

- **数据主权**：你的数据永远在你的机器上
- **文化主权**：底座是易经、道德经、五行八卦，别人抄不走
- **全模态**：语音+视觉+文字，一个接口全覆盖
- **极简接口**：一个函数解决一个问题
- **不删只冻**：数据永不删除，只标记状态

## 许可

[CC BY-NC-SA 4.0](./LICENSE) · 署名-非商业-相同方式共享

## 作者

UID9622 · 诸葛鑫

---

*「再楠不惧，终成豪图」*
