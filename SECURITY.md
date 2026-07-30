# 安全策略 / Security Policy

> DNA: #龍芯⚡️2026-07-30-LONGHUN-SECURITY-POLICY-v1.0  
> 项目: 龍魂系统 / LongHun System  
> 维护者: UID9622  
> 适用范围: 所有公开仓库、`longhun-system` 主仓库及其子模块

---

## 支持的版本 / Supported Versions

| 版本分支 | 状态 | 说明 |
|:---|:---:|:---|
| `orphan_main` | ✅  actively maintained | 当前默认分支，接收安全更新 |
| `release/v5.0.0-opensource` | ✅  maintained | 开源发布分支，仅接收关键安全修复 |
| `main` | ⚠️  legacy | 历史主分支，建议迁移到 `orphan_main` |
| 其他 feature 分支 | ❌ 不支持 | 请在合并到默认分支后再评估 |

---

## 如何报告漏洞 / Reporting a Vulnerability

如果你发现安全漏洞，请通过以下方式私密报告，**不要直接提交公开 Issue 或 PR**：

1. **GitHub Private Vulnerability Reporting**（推荐）  
   访问仓库 `Security → Advisories → Report a vulnerability` 提交。

2. **加密邮件**  
   发送邮件至 `security@uid9622.cn`，并使用下方 GPG 公钥加密邮件内容。

3. **龍魂安全闸入口**  
   本地运行 `bin/lh_kfpp_engine.py --inspect "<事件描述>"` 进行自检留痕。

请在报告中尽可能包含：
- 受影响的路径/文件/依赖
- 复现步骤或 PoC（如有）
- 建议的修复方案或参考链接
- 你的联系方式（可选，用于后续沟通）

---

## 披露政策 / Disclosure Policy

- **确认收到**: 我们通常在 7 个工作日内确认收到报告。
- **初步评估**: 30 个工作日内完成影响评估并给出修复计划或说明。
- **修复窗口**: 关键漏洞（critical/high）优先在 90 天内修复；上游无补丁的传递依赖会在 `SECURITY.md` 与 `.github/dependabot.yml` 中显式留痕。
- **公开披露**: 修复完成后，我们会发布安全公告（Security Advisory）并致谢报告者；未修复前不公开细节。

---

## 已知安全边界与上游限制 / Known Security Boundaries

以下问题属于**上游依赖无补丁**或**历史归档代码**，不在当前维护范围内：

| 依赖/路径 | 问题 | 原因 | 状态 |
|:---|:---|:---|:---|
| `babel-traverse@6.x` | Arbitrary code execution (CVE) | `miniprogram-ci` 传递依赖 Babel 6，微信官方未发布 Babel 7 版本 | 已显式忽略，等待上游更新 |
| `_archive/` | 历史归档中的 `torch`、`transformers` 旧版本 | 本地历史归档，未进默认分支，已整体备份并删除 | 2026-07-30 清理完成 |

---

## GPG 公钥 / GPG Public Key

如需加密安全邮件，可使用项目公开的 GPG 公钥：

- **Key ID**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
- **获取方式**: `gpg --recv-keys A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
- **本地文件**: `portal/pgp/uid9622-public-key.asc`

---

## 安全相关资源

- [龍魂安全加固 v1.1](STATE.md)
- [KFPP 知识流动纯净度协议](bin/lh_kfpp_engine.py)
- [Dependabot 配置](.github/dependabot.yml)

---

## 致谢 / Acknowledgments

感谢所有负责任地披露安全问题的贡献者。你的谨慎帮助了更多人。
