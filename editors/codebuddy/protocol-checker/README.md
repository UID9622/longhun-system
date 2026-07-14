# 🐉 龍魂协议校验

> 保存文件时自动扫描 — 检查DNA锚定、老祖宗规则、敏感信息泄露。违规弹窗警告，一键修复
> 龍魂系统 · 诸葛鑫(uid9622) · 中国自主可控工具链

![龍魂](images/icon.png)

---

[![龍魂](https://img.shields.io/badge/龍魂-v1.0.0-D4AF37?logo=visualstudiocode&labelColor=0a0514&logoColor=D4AF37)](https://marketplace.visualstudio.com/items?itemName=uid9622.protocol-checker)
[![License](https://img.shields.io/badge/License-CC--BY--NC--SA--4.0-22c55e?labelColor=0a0514)](./LICENSE)
[![GPG](https://img.shields.io/badge/GPG-A2D0092CEE2E5BA87035600924C3704A8CC26D5F-c41e3a?labelColor=0a0514)](https://keys.openpgp.org/search?q=A2D0092CEE2E5BA87035600924C3704A8CC26D5F)
[![Made with ❤️ in China](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F%20%E4%B8%AD%E5%9B%BD-c41e3a?labelColor=0a0514)]()

---

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🛡️ DNA 校验 | 检查文件是否包含 DNA 锚定码 |
| 🏛️ 老祖宗规则 | 检查境外 API 导入、云端上传、敏感库 |
| 🔐 敏感信息 | 检测密钥、Token、密码、私钥泄露 |
| ⚠️ 即时警告 | 违规时弹窗提示并定位到行 |
| 🔧 一键修复 | 自动修复可修复的违规项 |

---

## 🚀 快速开始

1. 安装扩展后，按 `Ctrl+Shift+P`（macOS `Cmd+Shift+P`）
2. 输入：**`龍魂: `** 查看所有可用命令
3. 选择对应功能即可开始使用

---

## 🎮 命令面板

| 命令 | 作用 |
|------|------|
| `龍魂: 协议校验当前文件` | 扫描当前文件 |
| `龍魂: 协议校验整个工作区` | 扫描整个工作区 |
| `龍魂: 一键修复当前文件` | 自动修复当前文件 |

---

## ⚙️ 配置项

在 `settings.json` 中搜索 `longhun-protocol`：

```json
{
  "longhun-protocol.enableDNA": true,  // 检查 DNA 锚定码
  "longhun-protocol.enableAncestors": true,  // 检查老祖宗规则
  "longhun-protocol.enableSensitive": true,  // 检查敏感信息泄露
  "longhun-protocol.autoFixOnSave": false,  // 保存时自动修复（谨慎开启）
  "longhun-protocol.ignoredFiles": [...],  // 忽略的文件模式
}
```

---

## 🏷️ 标签与分类

- **分类**: Linters · Other
- **标签**: 龍魂 · longhun · 协议校验 · protocol-checker · DNA锚定 · 老祖宗规则 · 敏感信息 · 安全 · 合规 · CNSH · 中国自主 · 诸葛鑫 · uid9622

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
> DNA: `#龍芯⚡️丙午·辛未·PROTOCOL-CHECKER-v1.0`
