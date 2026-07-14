# 🐉 龍魂一键部署

> 代码写完一键推送 GitHub / Gitee / 华为云 — 自动 `git add commit push`，附带 GPG 签名。  
> 龍魂系统 · 诸葛鑫(uid9622) · 中国自主可控工具链

![龍魂](images/icon.png)

---

[![龍魂](https://img.shields.io/badge/龍魂-v1.0.0-D4AF37?logo=visualstudiocode&labelColor=0a0514&logoColor=D4AF37)](https://marketplace.visualstudio.com/items?itemName=uid9622.longhun-one-click-deploy)
[![License](https://img.shields.io/badge/License-CC--BY--NC--SA--4.0-22c55e?labelColor=0a0514)](./LICENSE)
[![GPG](https://img.shields.io/badge/GPG-A2D0092CEE2E...6D5F-c41e3a?labelColor=0a0514)](https://keys.openpgp.org/search?q=A2D0092CEE2E5BA87035600924C3704A8CC26D5F)
[![Platform](https://img.shields.io/badge/Platform-GitHub%20%C2%B7%20Gitee%20%C2%B7%20%E5%8D%8E%E4%B8%BA%E4%BA%91-3b82f6?labelColor=0a0514)]()
[![Contributors](https://img.shields.io/badge/Contributors-Welcome-22c55e?labelColor=0a0514)](./CONTRIBUTORS.md)
[![Made with ❤️ in China](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F%20%E4%B8%AD%E5%9B%BD-c41e3a?labelColor=0a0514)]()

---

## ✨ 为什么用龍魂一键部署

| 特性 | 说明 |
|------|------|
| 🐉 **一键三连** | `git add -A` → `git commit` → `git push` 一条命令完成 |
| 🔐 **GPG 签名** | 默认启用 `-S` 签名，守护代码血统与真实身份 |
| 🌐 **多平台推送** | 同时/分别推送到 GitHub、Gitee、华为云 |
| 🛡️ **安全流水线** | 推送前自动 `pull --rebase`，避免冲突覆盖 |
| 📊 **状态栏实时** | 右下角显示分支、待提交数、变更状态 |
| 🧠 **龍魂风格** | 中文界面、国潮设计、个人 IP 可识别 |

---

## 🚀 快速开始

1. 安装扩展后，按 `Ctrl+Shift+P`（macOS `Cmd+Shift+P`）
2. 输入：**`龍魂: 一键推送`**
3. 填写提交信息 → 选择提交类型 → 确认
4. 坐下，看终端输出完成 ✅

---

## 🎮 命令面板

| 命令 | 作用 |
|------|------|
| `龍魂: 一键推送 (add+commit+push)` | 完整流水线 |
| `龍魂: 推送到 GitHub` | 仅推送 GitHub 远程 |
| `龍魂: 推送到 Gitee` | 仅推送 Gitee 远程 |
| `龍魂: 推送到华为云` | 仅推送华为云远程 |
| `龍魂: GPG 签名 + 推送` | 指定 GPG Key 提交 |
| `龍魂: 查看 Git 状态` | 打开可视化 Git 面板 |

---

## ⚙️ 配置项

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

## 🏷️ 标签与分类

- **分类**: `SCM` · `Other`
- **标签**: `龍魂` · `一键部署` · `Git` · `GPG` · `CNSH` · `中国自主` · `GitHub` · `Gitee` · `华为云` · `诸葛鑫` · `uid9622`

---

## 🤝 贡献者

欢迎提交 Issue / PR。  
详见 [CONTRIBUTORS.md](./CONTRIBUTORS.md) 与 [CONTRIBUTING.md](./CONTRIBUTING.md)。

[![Contributors](https://img.shields.io/badge/Contributors-Welcome-22c55e?labelColor=0a0514)](./CONTRIBUTORS.md)

---

## 📜 许可证

本扩展采用 **CC-BY-NC-SA-4.0** 许可协议。  
未经授权不得用于商业用途。

---

> 🐉 **龍魂系统** — 替老百姓守住数字主权，把 AI 的根扎在中国土地上。  
> DNA: `#龍芯⚡️丙午·辛未·ONE-CLICK-DEPLOY-v1.0`
