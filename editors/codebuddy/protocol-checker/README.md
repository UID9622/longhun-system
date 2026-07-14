# 🐉 龍魂协议校验

> 保存文件时自动扫描 — 检查DNA签名、P0合规、SM3哈希完整性
> 龍魂系统 · 诸葛鑫(uid9622) · 中国自主可控工具链

![龍魂](images/icon.png)

---

[![龍魂](https://img.shields.io/badge/龍魂-v1.0.0-D4AF37?logo=visualstudiocode&labelColor=0a0514&logoColor=D4AF37)](https://marketplace.visualstudio.com/items?itemName=uid9622.longhun-protocol-checker)
[![License](https://img.shields.io/badge/License-CC--BY--NC--SA--4.0-22c55e?labelColor=0a0514)](./LICENSE)
[![GPG](https://img.shields.io/badge/GPG-A2D0092CEE2E5BA87035600924C3704A8CC26D5F-c41e3a?labelColor=0a0514)](https://keys.openpgp.org/search?q=A2D0092CEE2E5BA87035600924C3704A8CC26D5F)
[![Made with ❤️ in China](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F%20%E4%B8%AD%E5%9B%BD-c41e3a?labelColor=0a0514)]()

---

## 功能

- **DNA锚定检查** — 文件是否包含龍魂DNA签名
- **P0合规扫描** — 检测境外API导入、云端上传、敏感库引用
- **SM3哈希完整性** — 验证文件内容哈希匹配
- **敏感信息泄露** — 检测密钥/Token/密码/私钥
- **一键修复** — 违规项自动修复（可配置）

---

## 快速开始

1. 安装扩展后，保存文件时自动触发扫描
2. 右键文件 → **`龍魂: 协议校验当前文件`**
3. 或按 `Ctrl+Shift+P` → **`龍魂: 协议校验整个工作区`**

---

## 命令

| 命令 | 快捷键 | 说明 |
|------|--------|------|
| `龍魂: 协议校验当前文件` | `Ctrl+Shift+P` | 校验当前打开的文件 |
| `龍魂: 协议校验整个工作区` | — | 校验整个工作区所有文件 |
| `龍魂: 一键修复当前文件` | — | 自动修复违规项 |

---

## 配置

在 `settings.json` 中搜索 `longhun-protocol`：

```json
{
  "longhun-protocol.enableDNA": true,
  "longhun-protocol.enableAncestors": true,
  "longhun-protocol.enableSensitive": true,
  "longhun-protocol.autoFixOnSave": false,
  "longhun-protocol.ignoredFiles": [
    "node_modules/**",
    "venv/**",
    ".git/**"
  ]
}
```

---

## 标签

- **分类**: Other · Linters · Testing
- **标签**: 龍魂 · longhun · 协议校验 · protocol-checker · DNA锚定 · 老祖宗规则 · 敏感信息 · 安全 · 合规 · CNSH · 中国自主 · 诸葛鑫 · uid9622

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
> DNA: `#龍芯⚡️丙午·辛未·PROTOCOL-CHECKER-v1.0`
