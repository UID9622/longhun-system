# 🐉 龍魂多模型路由

> DeepSeek/Kimi/本地模型一键切换 — 根据任务类型自动选择最优模型
> 龍魂系统 · 诸葛鑫(uid9622) · 中国自主可控工具链

![龍魂](images/icon.png)

---

[![龍魂](https://img.shields.io/badge/龍魂-v1.0.0-D4AF37?logo=visualstudiocode&labelColor=0a0514&logoColor=D4AF37)](https://marketplace.visualstudio.com/items?itemName=uid9622.longhun-model-router)
[![License](https://img.shields.io/badge/License-CC--BY--NC--SA--4.0-22c55e?labelColor=0a0514)](./LICENSE)
[![GPG](https://img.shields.io/badge/GPG-A2D0092CEE2E5BA87035600924C3704A8CC26D5F-c41e3a?labelColor=0a0514)](https://keys.openpgp.org/search?q=A2D0092CEE2E5BA87035600924C3704A8CC26D5F)
[![Made with ❤️ in China](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F%20%E4%B8%AD%E5%9B%BD-c41e3a?labelColor=0a0514)]()

---

## 功能

- **一键切换** — DeepSeek / Kimi / 本地模型 快速切换
- **智能路由** — 按任务类型自动选择最优模型
- **安全本地** — 敏感操作强制使用本地模型，数据不出本机
- **状态栏显示** — 当前模型状态一目了然
- **灵活配置** — API Key 仅本地存储，不上传云端

---

## 快速开始

1. 安装扩展后，按 `Ctrl+Shift+P`（macOS `Cmd+Shift+P`）
2. 输入：**`龍魂: `** 查看所有可用命令
3. 选择对应功能即可开始使用

---

## 命令

| 命令 | 快捷键 | 说明 |
|------|--------|------|
| `龍魂: 切换到 DeepSeek` | `Ctrl+Shift+1` | 切换到 DeepSeek 模型 |
| `龍魂: 切换到 Kimi` | `Ctrl+Shift+2` | 切换到 Kimi 模型 |
| `龍魂: 切换到本地模型` | `Ctrl+Shift+3` | 切换到本地模型 |
| `龍魂: 自动路由（按任务类型）` | `Ctrl+Shift+A` | 按任务类型自动选择模型 |
| `龍魂: 查看当前模型路由状态` | — | 显示当前模型和任务映射 |

---

## 配置

在 `settings.json` 中搜索 `longhun-model`：

```json
{
  "longhun-model.defaultModel": "auto",
  "longhun-model.codeGenModel": "deepseek",
  "longhun-model.codeReviewModel": "kimi",
  "longhun-model.sensitiveModel": "local",
  "longhun-model.deepseekApiKey": "",
  "longhun-model.kimiApiKey": "",
  "longhun-model.localModelPath": ""
}
```

---

## 标签

- **分类**: Other · Machine Learning · Snippets
- **标签**: 龍魂 · longhun · 模型路由 · model-router · DeepSeek · Kimi · 本地模型 · LLM · AI · 代码生成 · 代码审查 · CNSH · 中国自主 · 诸葛鑫 · uid9622

---

## 贡献

欢迎提交 Issue / PR。  
详见 [CONTRIBUTORS.md](./CONTRIBUTORS.md) 与 [CONTRIBUTING.md](./CONTRIBUTING.md)。

---

## 许可证

本扩展采用 **CC-BY-NC-SA-4.0** 许可协议。  
未经授权不得用于商业用途。

---

> 🐉 **龍魂系统** — 替老百姓守住数字主权，把 AI 的根扎在中国土地上。  
> DNA: `#龍芯⚡️丙午·辛未·MODEL-ROUTER-v1.0`
