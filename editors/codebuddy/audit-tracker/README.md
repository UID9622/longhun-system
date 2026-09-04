> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·壬戌·亥时·䷲震-AUDIT-TRACKER-v2.0-METHODOLOGY-WELD
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂审计追踪 v2.0

> AI生成代码自动审计追踪 — 启发式三家族·双层校准·哈希链·三色标记·责任追溯
> 龍魂系统 · 诸葛鑫(uid9622) · 中国自主可控工具链

![龍魂](images/icon.png)

---

[![龍魂](https://img.shields.io/badge/龍魂-v2.0.0-D4AF37?logo=visualstudiocode&labelColor=0a0514&logoColor=D4AF37)](https://marketplace.visualstudio.com/items?itemName=uid9622.longhun-audit-tracker)
[![License](https://img.shields.io/badge/License-MulanPSL--2.0-22c55e?labelColor=0a0514)](./LICENSE)
[![GPG](https://img.shields.io/badge/GPG-A2D0092CEE2E5BA87035600924C3704A8CC26D5F-c41e3a?labelColor=0a0514)](https://keys.openpgp.org/search?q=A2D0092CEE2E5BA87035600924C3704A8CC26D5F)
[![Made with ❤️ in China](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F%20%E4%B8%AD%E5%9B%BD-c41e3a?labelColor=0a0514)]()

---

## 功能

- **启发式三家族检测** — 关键词匹配 / 未明确判定 / 长度阈值，交叉判定而非单一信号
- **verdict 与 evidence 一致** — 每条记录带判定 + 触发证据，可追溯可复核
- **双层校准（Layer1+Layer2）** — 判定对齐（verdict 分布）+ 行为对齐（启发式家族分布）
- **哈希链防篡改** — 逐条 prevHash 链式校验，杜绝"计数掩盖替换"
- **三色标记** — 🟢已通过 / 🟡待审核·未判定 / 🔴已拒绝
- **Wilson 95% 置信区间** — 小样本统计附 CI，不做 ±12pp 级误判
- **逐条独立 DNA** — v∞ 干支/日期 DNA，批 DNA + 逐条 DNA 双锚
- **交互式审计面板** — WebView 内筛选 / 展开证据 / 直接标记通过或拒绝
- **责任追溯** — 谁生成 → 谁审核 → 何时通过，完整审计链

---

## 方法论来源（DeepSeek-V3 issue #1591 商讨共识）

> github.com/deepseek-ai/DeepSeek-V3/issues/1591

| 商讨人 | 共识 | 落地位置 |
|--------|------|----------|
| DanceNitra | verdict 必须与 rejection_reason 一致；未判定 ≠ 拒绝；三家族启发式 | `classifyVerdict` / `detectEvidence` |
| icophy | 双层校准 Layer1 判定对齐 + Layer2 行为对齐 | `verdict` / `behavior` 字段 + 报告两段分布 |
| baoqingkong66 | 计数掩盖替换陷阱；报告附数据版本哈希 | 哈希链 `prevHash` + 报告哈希校验 |
| UID9622 | 审计探针可验证；报告双示例 | `audit-report.md` 生成 + 复现命令注记 |

---

## 快速开始

1. 安装扩展后，自动在状态栏显示审计计数
2. 右键代码选中区域 → **`龍魂: 审计选中代码`**
3. 按 `Ctrl+Shift+P` 输入 **`龍魂: `** 查看所有命令
4. 打开审计面板后可直接在每条记录上点 ✅/🔴 标记

---

## 命令

| 命令 | 快捷键 | 说明 |
|------|--------|------|
| `龍魂: 查看审计日志` | — | 打开审计日志交互面板 |
| `龍魂: 审计选中代码` | `Ctrl+Shift+U` | 审计当前选中的代码 |
| `龍魂: 生成审计报告` | — | 导出审计报告 Markdown |
| `龍魂: 标记为已审核` | — | 手动标记代码为已通过 |
| `龍魂: 标记为已拒绝` | — | 手动标记代码为已拒绝 |

---

## 配置

在 `settings.json` 中搜索 `longhun-audit`：

```json
{
  "longhun-audit.auditLogPath": ".audit/log.json",
  "longhun-audit.minPasteChars": 300,
  "longhun-audit.minPasteLines": 15,
  "longhun-audit.autoAuditOnPaste": true,
  "longhun-audit.autoAuditOnSave": true,
  "longhun-audit.showStatusBar": true
}
```

---

## 判定模型（v2.0）

| 启发式命中 | verdict | 三色 | 置信度 | 含义 |
|-----------|---------|------|--------|------|
| ≥2 家族 | `confirmed` | 🔴 | 0.9 | 多信号交叉确认 |
| 1 家族 | `flagged` | 🟡 | 0.6 | 单信号提示 |
| 无命中·人工记录 | `unverified` | 🟡 | 0.3 | 未判定 ≠ 拒绝 |
| 人工复核通过 | `clean` | 🟢 | 1.0 | 已审核 |

---

## 标签

- **分类**: Other · Testing · Linters
- **标签**: 龍魂 · longhun · 审计 · audit · 追踪 · AI生成代码 · 提示词哈希 · 合规 · CNSH · 中国自主 · 诸葛鑫 · uid9622

---

## 贡献

欢迎提交 Issue / PR。
详见 [CONTRIBUTORS.md](./CONTRIBUTORS.md) 与 [CONTRIBUTING.md](./CONTRIBUTING.md)。

---

## 许可证

本扩展采用 **MulanPSL v2**（工程实现层·允许商业使用·署名·专利授权）。
思想层协议见 `01_protocols/LH-LAYERED-LICENSE-v1.0.md`。

---

> 🐉 **龍魂系统** — 替老百姓守住数字主权，把 AI 的根扎在中国土地上。
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> DNA: `#龍芯⚡️丙午·丙申·壬戌·亥时·䷲震-AUDIT-TRACKER-v2.0-METHODOLOGY-WELD`
