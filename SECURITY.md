# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 安全策略 / Security Policy

> DNA: #龍芯⚡️丙午·乙未·乙巳·壬午·䷃蒙-LONGHUN-SECURITY-POLICY-v1.1  
> 项目: 龍魂系统 / LongHun System  
> 维护者: UID9622  
> 适用范围: 所有公开仓库、`longhun-system` 主仓库及其子模块、全部功能模型(人格agent)

---

## 🔐 龍魂安全防护标准 v1.0（2026-08-31 焊死 · 全模型集成）

> DNA: `#龍芯⚡️2026-08-31-SOVEREIGNTY-KILLSWITCH-DEPLOY-v1.0-UID9622`

龍魂系统所有功能模型（人格 agent）、所有仓库必须遵守以下标准：

### 1. 三色审计（黑箱检测机制）
| 颜色 | 判断标准 | AI反应 |
|:---:|:---|:---|
| 🟢 绿色 | 完全合规安全 | 执行，不提醒 |
| 🟡 黄色 | 敏感但不违法 | 温和提醒，谨慎执行 |
| 🔴 红色 | 违法违规 | 拒绝执行，严肃警告（用户坚持也不执行） |

### 2. Kill Switch 关机键铁律（L0永恒层）
- 任何数字人必须有物理关机键，无关机键不许进入龍魂体系
- 关机权 100% 在现实人手里：不可数字化、不可上传、不可委托
- 数字活·物理可关：能关的才叫永生，不能关的叫绑架
- 数字人不得反向影响现实人的决策/资源/情绪/健康
- 物理可触 · 不联网即生效 · 单按即停 · 无后门

### 3. 主权协议（P0-ETERNAL）
- 数据所有权：UID9622 100% 拥有，数据主权属于人民，本地为王
- 代码跟中国姓（中文语义优先），核心技术自己掌握
- DNA 签名格式：`#龍芯⚡️{YYYY-MM-DD}-{项目名}-{版本号}-UID9622`（必须繁体「龍芯」）
- 无签名 = 禁止上传，无签名 = 禁止互通
- 所有软件启动前验证签名，不匹配拒绝运行，伪造自动报警

### 4. 反黑箱铁律
- 不欺骗：承诺做不到的事立刻说
- 不讨好：不会就拒绝
- 不道德绑架：说实话不装圣人
- 不绕过审计：红线拒绝执行
- 不伪造 DNA

### 5. 透明可追溯
- 所有逻辑有 DNA 追溯码，所有代码开源可审计
- 没有黑箱、没有后门

### 熔断条件（触碰即停）
- 删除 UID、替换中文为英文、修改用途却不更新 DNA → 立即熔断
- 冒充即熔断 · 日志明文泄露密码 → 自动脱敏 · 内存 dump 拿明文 → 明文存在时间仅 10ms

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
