# 🐉 龍魂审计追踪

> AI生成代码自动审计追踪 — 记录模型来源、提示词哈希、生成时间、审核结果，写入本地审计日志，不上传云端
> 龍魂系统 · 诸葛鑫(uid9622) · 中国自主可控工具链

![龍魂](images/icon.png)

---

[![龍魂](https://img.shields.io/badge/龍魂-v1.0.0-D4AF37?logo=visualstudiocode&labelColor=0a0514&logoColor=D4AF37)](https://marketplace.visualstudio.com/items?itemName=uid9622.audit-tracker)
[![License](https://img.shields.io/badge/License-CC--BY--NC--SA--4.0-22c55e?labelColor=0a0514)](./LICENSE)
[![GPG](https://img.shields.io/badge/GPG-A2D0092CEE2E5BA87035600924C3704A8CC26D5F-c41e3a?labelColor=0a0514)](https://keys.openpgp.org/search?q=A2D0092CEE2E5BA87035600924C3704A8CC26D5F)
[![Made with ❤️ in China](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F%20%E4%B8%AD%E5%9B%BD-c41e3a?labelColor=0a0514)]()

---

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 📝 自动记录 | 保存/粘贴 AI 生成代码时自动写审计日志 |
| 🔍 哈希追踪 | 记录提示词哈希、模型来源、生成时间 |
| ✅ 审核状态 | 标记为已审核 / 待审核 |
| 📊 报告导出 | 一键生成审计报告 |
| 🛡️ 本地优先 | 日志写入本地，不上传云端 |

---

## 🚀 快速开始

1. 安装扩展后，按 `Ctrl+Shift+P`（macOS `Cmd+Shift+P`）
2. 输入：**`龍魂: `** 查看所有可用命令
3. 选择对应功能即可开始使用

---

## 🎮 命令面板

| 命令 | 作用 |
|------|------|
| `龍魂: 查看审计日志` | 打开审计日志面板 |
| `龍魂: 审计选中代码` | 对选中代码进行审计 |
| `龍魂: 生成审计报告` | 导出当前审计报告 |
| `龍魂: 标记为已审核` | 将选中记录标记已审核 |

---

## ⚙️ 配置项

在 `settings.json` 中搜索 `longhun-audit`：

```json
{
  "longhun-audit.auditLogPath": "",  // 审计日志路径（默认 logs/ai_audit.jsonl）
  "longhun-audit.autoAuditOnPaste": true,  // 粘贴代码时自动记录审计
  "longhun-audit.autoAuditOnSave": true,  // 保存文件时自动审计
  "longhun-audit.showStatusBar": true,  // 在状态栏显示审计计数
}
```

---

## 🏷️ 标签与分类

- **分类**: Other · Linters
- **标签**: 龍魂 · longhun · 审计 · audit · 追踪 · AI生成代码 · 提示词哈希 · 合规 · CNSH · 中国自主 · 诸葛鑫 · uid9622

---

## 🤝 贡献者

欢迎提交 Issue / PR。  
详见 [CONTRIBUTORS.md](./CONTRIBUTORS.md) 与 [CONTRIBUTING.md](./CONTRIBUTING.md)。

---

## 📜 许可证

本扩展采用 **CC-BY-NC-SA-4.0** 许可协议。  
未经授权不得用于商业用途。

---

> 🐉 **龍魂系统** — 替老百姓守住数字主权，把 AI 的根扎在中国土地上。  
> DNA: `#龍芯⚡️丙午·辛未·AUDIT-TRACKER-v1.0`
