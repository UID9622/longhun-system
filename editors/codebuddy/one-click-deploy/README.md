# 🐉 龍魂一键部署

> 代码写完一键推送 GitHub/Gitee/华为云 — 自动签名、自动审计、自动归档
> 龍魂系统 · 诸葛鑫(uid9622) · 中国自主可控工具链

![龍魂](images/icon.png)

---

[![龍魂](https://img.shields.io/badge/龍魂-v1.0.0-D4AF37?logo=visualstudiocode&labelColor=0a0514&logoColor=D4AF37)](https://marketplace.visualstudio.com/items?itemName=uid9622.longhun-one-click-deploy)
[![License](https://img.shields.io/badge/License-CC--BY--NC--SA--4.0-22c55e?labelColor=0a0514)](./LICENSE)
[![GPG](https://img.shields.io/badge/GPG-A2D0092CEE2E5BA87035600924C3704A8CC26D5F-c41e3a?labelColor=0a0514)](https://keys.openpgp.org/search?q=A2D0092CEE2E5BA87035600924C3704A8CC26D5F)
[![Made with ❤️ in China](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F%20%E4%B8%AD%E5%9B%BD-c41e3a?labelColor=0a0514)]()

---

## 功能

- **一键推送** — `Ctrl+Shift+D` 自动 add → commit → push
- **多平台部署** — GitHub / Gitee / 华为云 一键切换
- **GPG签名** — 自动 GPG 签名所有提交
- **自动审计** — 推送前自动运行审计检查
- **自动归档** — 旧版本自动归档到 `_archive/`

---

## 快速开始

1. 安装扩展后，确保 Git 已配置
2. 按 `Ctrl+Shift+D` 一键推送
3. 或按 `Ctrl+Shift+P` → **`龍魂: 一键推送`**

---

## 命令

| 命令 | 快捷键 | 说明 |
|------|--------|------|
| `龍魂: 一键推送` | `Ctrl+Shift+D` | add+commit+push 一键完成 |
| `龍魂: 推送到 GitHub` | — | 仅推送到 GitHub |
| `龍魂: 推送到 Gitee` | — | 仅推送到 Gitee |
| `龍魂: 推送到华为云` | — | 仅推送到华为云 |
| `龍魂: GPG 签名 + 推送` | — | 带 GPG 签名的推送 |
| `龍魂: 查看 Git 状态` | — | 显示当前 Git 状态 |

---

## 配置

在 `settings.json` 中搜索 `longhun-deploy`：

```json
{
  "longhun-deploy.githubRemote": "github",
  "longhun-deploy.giteeRemote": "gitee",
  "longhun-deploy.huaweiRemote": "huawei",
  "longhun-deploy.enableGPG": true,
  "longhun-deploy.gpgKeyId": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
  "longhun-deploy.autoPullBeforePush": true,
  "longhun-deploy.commitTemplate": "{type}: {message}"
}
```

---

## 标签

- **分类**: Other · SCM · Deployment
- **标签**: 龍魂 · longhun · 一键部署 · one-click-deploy · Git · GPG · CNSH · 中国自主 · 多平台 · GitHub · Gitee · 华为云 · 诸葛鑫 · uid9622

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
> DNA: `#龍芯⚡️丙午·辛未·ONE-CLICK-DEPLOY-v1.0`
