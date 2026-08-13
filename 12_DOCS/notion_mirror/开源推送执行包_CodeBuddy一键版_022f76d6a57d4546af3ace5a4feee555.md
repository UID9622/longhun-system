# 🚀 开源推送执行包（CodeBuddy一键版）

> Notion URL: https://app.notion.com/p/CodeBuddy-022f76d6a57d4546af3ace5a4feee555
> Created: 2025-12-25T21:41:00.000Z
> Last edited: 2026-07-01T15:11:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
### 使用方式（只需复制给 CodeBuddy）
> 目标：把“龙魂系统”相关开源内容按统一规则发布，同时不被轻易抹掉归属。
### 0) 固定前提（不可更改）
- 开源协议：Mulan PSL v2（木兰 2）
- 作者签名锚点：使用你提供的 GPG 指纹 + 身份指纹 + 网络身份证
- 发布口径：尊重专家，欢迎审阅，争议回到“可验证案例”。
---
### 1) 发布前检查清单（P0）
---
### 2) 每个公开页面必须粘贴的 5 块
1. 🔐 创作者数字身份认证（可验真）模板
1. 📌 开源引用与反剽窃声明（固定口径）
1. 🛡️ 争议处理与专家友好口径（统一回复）
1. 💴 随缘打赏声明（数字人民币/支付宝）
1. 🧱 龙魂终端·不可篡改归属权代码模板（嵌入块）
---
### 3) 版本与追溯规则（最简可跑）
- 每次对外发布视为一个版本：vMAJOR.MINOR
- 版本升级必须写“变更摘要”（3行）：
---
### 4) CodeBuddy 执行指令（复制整段给 CodeBuddy）
```yaml
task: open_source_release
license: "Mulan PSL v2"

# Required blocks to inject
required_blocks:
  - "CREATOR-IDENTITY-BLOCK"
  - "OPEN-SOURCE-ATTRIBUTION-BLOCK"
  - "BOUNDARY-AND-EXPERTS-FRIENDLY-BLOCK"
  - "DONATION-BLOCK"
  - "DRAGONSOUL-OWNERSHIP-BLOCK"

author:
  name: "Lucky"
  uid: "UID9622"
  gpg_fingerprint: "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
  network_id: "T38C89R75U"
  identity_fingerprint: "b83c74d108660082581f9ebbb9506f65849d9d48d21d328daf13f7c4d66cf6c1"

release_policy:
  attribution_required: true
  must_include_original_link: true
  avoid_flamewar: true
funding:
  enabled: true

  note: "自愿赞助，不影响许可证授权，不构成付费许可"
outputs:
  - "

```
- README.md: "insert required blocks at top"
- NOTICE.md: "insert ownership + attribution blocks"
- LICENSE: "Mulan PSL v2"
- CONTRIBUTING.md: "contribution rules"
- CHANGELOG.md: "3-line change summary per version"
