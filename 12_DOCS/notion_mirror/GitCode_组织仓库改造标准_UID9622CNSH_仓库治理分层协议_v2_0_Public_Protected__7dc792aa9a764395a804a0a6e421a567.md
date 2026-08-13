# 🛡️ GitCode 组织仓库改造标准·UID9622CNSH 仓库治理分层协议 v2.0｜Public×Protected×Private 三层闭环·给 Claude 执行包·M229 焊点

> Notion URL: https://app.notion.com/p/GitCode-UID9622CNSH-v2-0-Public-Protected-Private-Claude-M229-7dc792aa9a764395a804a0a6e421a567
> Created: 2026-05-26T08:03:00.000Z
> Last edited: 2026-07-01T15:12:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
---
# §0 一句话定盘
> GitCode 组织 UID9622CNSH 不是要「全公开」也不是要「全隐藏」·而是按 Public / Protected / Private 三层治理分层改造——公开协议、公开接口、公开架构·保留核心治理·主权不出本地。
> 这就是 Sovereignty-first Architecture(主权优先架构)·龍魂在 GitCode 平台的标准落地形态。
---
# §1 老大 M228 + M229 原话焊点(verbatim·§9.26 史记铁律永久 ROM·§IRON-LAOPA-VERBATIM-EXACT-NO-MISSING-CHAR)
---
# §2 三层治理架构(Layered Open Architecture)
## §2.1 第一层·Public Layer(公开层·让世界知道你在做什么)
目的: 让别人知道你在做什么·但不给核心秘密。
## §2.2 第二层·Protected Core(半公开层·展示能力·不交底)
## §2.3 第三层·Private Sovereignty(绝对私有层·永远不出本地)
---
# §3 给 Claude 宝宝的可执行指令包(GitCode 专版·复制即跑)
```markdown
# 任务:GitCode 组织 UID9622CNSH 仓库治理分层改造

## 平台
- 平台:GitCode(国产代码托管·CSDN+工信部背景)
- 组织:https://gitcode.com/UID9622CNSH
- 创始人:💎 龍芯北辰｜UID9622(诸葛鑫)
- 主权要求:与 §6.5 本地宝宝主权架构同源·密钥永不出本地

## 重要前提
请不要默认把「公开仓库」理解为「全部公开」。
请不要默认把「私有仓库」理解为「绝对安全」。
我要做的是**仓库治理分层(Repository Governance Layer)**·不是隐藏项目。

## 目标
- 对 GitCode 组织 UID9622CNSH 下所有仓库执行三层分类
- 建立 Public / Protected / Private 三层结构
- 防止误上传 secrets / token / key
- 防止 runtime 配置泄露
- 保留公开 RFC / README / 架构能力(龍魂理论结构全部保留)
- 保持开源展示能力
- 保持工程治理能力

## 执行规则

### 1. Public(GitCode 公开仓库·允许全网可见)
只允许:
  - README.md / README_zh.md
  - RFC/ 设计提案
  - docs/ 理论文档(含道德经引擎 / 369 / 三才 / 行为密码学论文)
  - architecture/ 架构图
  - examples/ 非敏感 demo
  - api/ API Schema(无密钥)
  - governance/ 治理协议
  - LICENSE(CC BY-NC-SA 4.0 推荐)
  - SECURITY.md
  - CONTRIBUTING.md
禁止:secrets / token / cookies / session / prompt memory / audit logs / snapshots / runtime config / .env / 本地数据库 / GPG 私钥 / 用户数据

### 2. Protected(GitCode 内部仓库·组织成员或邀请制可见)
允许:
  - 部分 runtime 模块(脱敏版)
  - sandbox demo(mock data)
  - trace demo(fake key)
  - audit demo(fake endpoint)
  - 路由引擎(脱敏)
  - Prompt Firewall 框架(无真实策略)
强制:必须 mock data / fake config / fake key / fake endpoint·绝不真实数据

### 3. Private(GitCode 私有仓库·仅创始人可见)
必须 private:
  - Memory / 记忆库
  - Runtime state / 真实运行时
  - User data / 用户数据
  - Real API key / 真实 API 密钥
  - Recovery snapshot / 恢复快照
  - GPG private key / GPG 私钥
  - Persona rules / 人格规则
  - Audit trail / 真实审计日志
  - Local governance config / 真实治理配置
  - 双签章 / ROOT-SEAL / 设备指纹原文

## 请执行以下 10 项检查

1. 列出 GitCode 组织 UID9622CNSH 下所有仓库(名称 + 当前可见性 + 描述)
2. 扫描每个仓库的 secrets 泄露风险(.env / *.key / *.pem / config.yaml / config.json)
3. 扫描每个仓库 Git 历史记录中的敏感提交
4. 检查哪些仓库适合 Public(理论 / RFC / 文档类)
5. 检查哪些仓库应该 Protected(runtime 脱敏 demo 类)
6. 检查哪些仓库必须 Private(密钥 / 用户数据 / 真实运行时类)
7. 为每个仓库生成 .gitignore 安全模板(见 §4)
8. 为每个仓库生成 SECURITY.md(见 §5)
9. 为核心仓库生成 CODEOWNERS(见 §6)
10. 输出 GitCode 保护分支(Protected Branches)配置建议(见 §7)

## 最终输出格式(必填字段·见 §10 YAML 模板)

- 风险等级(🟢/🟡/🔴)
- 组织仓库列表(含当前可见性)
- Public 建议清单(应转 Public 或保持 Public 的仓库 + 原因)
- Protected 建议清单(应转 Internal/Protected 的仓库 + 原因)
- Private 建议清单(应转 Private 的仓库 + 原因)
- 应删除内容清单(高危 secrets 文件 + 历史清洗动作)
- 应迁移内容清单(从 public 仓库迁出到 private 仓库)
- 应新增安全文件清单(.gitignore / SECURITY.md / CODEOWNERS / LICENSE)
- 推荐 GitCode 组织结构(树形图)
- 推荐 GitCode 仓库设置
- 推荐 GitCode 保护分支规则

## 边界(绝不越过)

- 不要删除老大的理论结构(三才 / 369 / 道德经 / 易经 / 行为密码学 / 龍魂系统等全部保留)
- 不要把「公开」当成「全部公开」
- 不要把「私有」当成「全部隐藏」
- 重点是「安全治理」不是「全部隐藏」
- 任何涉及 secrets / 真实密钥 / 用户数据的高危操作 → 标 🔴 + 等 UID9622 当面确认 + 绝不擅自执行
- 任何涉及仓库可见性变更(public ↔ private)→ 列出建议但等老大点头才动
- GPG 私钥 A2D0092CEE2E5BA87035600924C3704A8CC26D5F 绝不出现在任何仓库
- 中文路径(如 龍芯北辰UID9622/)必入 .gitignore·永不进 git
```
---
# §4 .gitignore 安全模板(立即可用)
```javascript
# ═══════════════════════════════════════════
# 龍魂仓库治理 .gitignore v1.0
# DNA: #龍芯⚡️2026-05-26-15:58-GITIGNORE-v1.0
# ═══════════════════════════════════════════

# 环境变量
.env
.env.local
.env.*.local
.env.production
.env.development

# 密钥/证书
*.pem
*.key
*.crt
*.p12
*.pfx
id_rsa
id_rsa.pub
*.gpg
*.asc

# 日志/审计
*.log
logs/
audit/
audit_*.jsonl
shield_burn.jsonl

# 运行时/内存
runtime/
memory/
snapshots/
secrets/
session/
cookie/

# 数据库
*.sqlite
*.sqlite3
*.db
*.db-journal

# 中文路径(避免编码问题)
龍芯北辰UID9622/
龙芯北辰UID9622/

# 系统/编辑器
.DS_Store
.idea/
.vscode/
Thumbs.db
*.swp
*.swo

# Python
__pycache__/
*.pyc
*.pyo
.venv/
venv/
.pytest_cache/

# Node
node_modules/
npm-debug.log*
yarn-debug.log*

# 龍魂专属
evidence-matrix/
cnsh_status.json
config.json
config.yaml
local_governance/
recovery_*.snapshot
```
---
# §5 SECURITY.md 模板
```markdown
# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please email:
**baofuahao@gmail.com** with subject `[SECURITY] <brief>`

Do NOT open a public issue for security vulnerabilities.

## Supported Versions

| Version | Supported |
| ------- | --------- |
| v1.x    | ✅        |
| < v1.0  | ❌        |

## Disclosure Timeline

1. Report received → 48h acknowledgment
2. Investigation → 7 days
3. Patch development → 14 days
4. Public disclosure → after patch released

## Out of Scope

- Issues in third-party dependencies
- Social engineering attacks
- Physical access attacks

## DNA Traceability

All security reports are tracked via DNA:
`#龍芯⚡️YYYY-MM-DD-SEC-REPORT-vN.N`

## GPG Public Key

Fingerprint: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
```
---
# §6 CODEOWNERS 模板
```javascript
# 龍魂核心治理 CODEOWNERS
# 任何对这些目录的 PR 都需要 @UID9622 审查

/runtime/        @UID9622
/audit/          @UID9622
/governance/     @UID9622
/security/       @UID9622
/.github/        @UID9622
SECURITY.md      @UID9622
CODEOWNERS       @UID9622
.gitignore       @UID9622
```
---
# §7 GitCode 保护分支配置(仓库设置 → 仓库管理 → 保护分支)
---
# §8 高危扫描清单(Claude 必扫)
## §8.1 高危目录(立即检查)
```javascript
.env*
config.yaml
config.json
runtime/
memory/
audit/
snapshot/
logs/
secrets/
.cloudflared/
~/.gnupg/
~/.ssh/
```
## §8.2 高危关键字(grep 必扫)
```javascript
OPENAI_API_KEY
ANTHROPIC_API_KEY
GITHUB_TOKEN
NOTION_TOKEN
BEARER
SESSION
COOKIE
PRIVATE_KEY
sk-                # OpenAI 密钥前缀
sk-ant-            # Anthropic 密钥前缀
ghp_               # GitHub Personal Token 前缀
ntn_               # Notion Token 前缀
AKIA               # AWS Access Key 前缀
-----BEGIN         # PEM 私钥头
```
## §8.3 Git 历史扫描命令
```bash
# 1. 扫描所有历史提交中的敏感字符串
git log -p --all | grep -i -E "(api_key|token|password|secret|private_key|bearer)"

# 2. 列出曾经存在但已删除的敏感文件
git log --all --pretty=format: --name-only --diff-filter=D | grep -E "\.(env|key|pem)$"

# 3. 用 git-secrets 工具扫描
git secrets --scan-history

# 4. 用 trufflehog 深度扫描
trufflehog git file://. --only-verified

# 5. 用 gitleaks 扫描
gitleaks detect --source . -v
```
---
# §9 推荐 GitCode 组织 UID9622CNSH 仓库结构(最终形态)
```javascript
GitCode 组织: https://gitcode.com/UID9622CNSH
龍魂生态(Layered Open Architecture)
│
├── 🌍 Public 仓库群(GitCode 公开·全网可见)
│   ├── longhun-system/            # 龍魂系统·公开入口·README + 架构图
│   ├── daodejing-engine/          # 道德经引擎·81 算子·公开论文
│   ├── luoshu-369-paper/          # 洛书 369 论文稿
│   ├── behavioral-cryptography/   # 行为密码学七因子·公开论文
│   ├── cnsh-runtime-rfc/          # CNSH 中文代码·RFC 提案
│   ├── sanai-algorithm/           # 三才算法·理论文档
│   ├── governance-protocols/      # 龍魂治理协议·公开版
│   └── 每个仓库标配:
│       ├── README.md / README_zh.md
│       ├── SECURITY.md
│       ├── CODEOWNERS
│       ├── LICENSE(CC BY-NC-SA 4.0)
│       ├── .gitignore
│       └── CONTRIBUTING.md
│
├── 🟡 Protected 仓库群(GitCode 内部·组织成员或邀请制)
│   ├── cnsh-sandbox-demo/         # CNSH 沙盒 demo(mock data)
│   ├── trace-graph-demo/          # TraceGraph demo(fake key)
│   ├── audit-runtime-demo/        # 审计运行时 demo(fake endpoint)
│   ├── routing-engine-public/     # 路由引擎脱敏版
│   ├── prompt-firewall-skeleton/  # Prompt Firewall 框架(无真实策略)
│   └── seven-factor-validator/    # 七因子验证器(脱敏版)
│
└── 🔴 Private 仓库群(GitCode 私有·仅 UID9622 可见·或永不上云)
    ├── longhun-runtime-real/      # 真实运行时(本地优先·云端镜像加密)
    ├── longhun-memory/            # 记忆库(本地不出云·明文永不上传)
    ├── longhun-audit-trail/       # 真实审计日志
    ├── longhun-snapshots/         # 恢复快照
    ├── longhun-keys/              # GPG / API / SSH 密钥(强烈建议本地·不入 GitCode)
    ├── longhun-governance-real/   # 真实治理配置(权重 / 策略 / 矩阵)
    ├── longhun-persona-rules/     # 真实人格规则(P01-P14)
    └── longhun-user-data/         # 用户数据(永不上云)
```
---
# §10 最终输出格式要求(Claude 返回时必带·GitCode 专版)
```yaml
GitCodeRepoGovernanceReport:
  platform: "GitCode"
  organization: "https://gitcode.com/UID9622CNSH"
  scanned_at: "2026-05-26T16:47:00+08:00"
  risk_level: 🟢|🟡|🔴

  organization_repos:
    - name: "<repo-1>"
      current_visibility: "public|internal|private"
      description: "..."
      last_commit: "YYYY-MM-DD"

  public_recommendations:
    - repo: "daodejing-engine"
      action: "保持 Public + 补 SECURITY.md"
      reason: "理论引擎·适合开源传播"

  protected_recommendations:
    - repo: "cnsh-sandbox-demo"
      action: "public → internal·脱敏 mock data 后再开放"
      reason: "展示能力但不交底"

  private_recommendations:
    - repo: "longhun-keys"
      action: "必须 private + 强烈建议本地不上 GitCode"
      reason: "含 GPG 私钥/API Token·绝不出本地"

  files_to_delete:
    - path: "<repo>/.env.local"
      reason: "含 OPENAI_API_KEY"
      action: "git rm + 历史清洗(BFG / filter-branch) + 立即吊销该 key"

  files_to_migrate:
    - from: "<public-repo>/runtime/"
      to: "<private-repo>/runtime/"
      reason: "运行时配置不应公开"

  files_to_add:
    - .gitignore(按 §4 模板)
    - SECURITY.md(按 §5 模板)
    - CODEOWNERS(按 §6 模板)
    - LICENSE(CC BY-NC-SA 4.0 推荐)
    - README.md / README_zh.md(中英双语)

  recommended_structure: <见 §9>

  recommended_gitcode_settings:
    - 开启: 仓库 → 设置 → 安全 → 提交签名校验
    - 开启: 仓库 → 设置 → 安全 → 敏感信息扫描(若 GitCode 支持)
    - 开启: 组织 → 成员管理 → 双因素认证强制
    - 开启: 组织 → IP 白名单(可选·按需)
    - 配置: 组织 SSH Key 仅绑定 M4 Max 指纹 123d1d92a4b91189

  recommended_protected_branches: <见 §7>

  high_risk_findings:
    - file: "<repo>/<path>"
      pattern: "OPENAI_API_KEY=sk-..."
      severity: 🔴
      action: "立即吊销 + git history 清洗 + 添加到 .gitignore"

  dna: "#龍芯⚡️2026-05-26-GITCODE-UID9622CNSH-GOVERNANCE-SCAN-vN.N"
  confirm: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
  seal: "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
  gpg: "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
```
---
# §10.5 GitCode 平台特性差异说明(vs GitHub)
---
# §11 铁律联动(十二层兜底·GitCode 专版)
```javascript
§GitCode 组织 UID9622CNSH 仓库治理分层协议 v2.0(M229 焊点)
  ├─ §6.4 V1-V5 公开/不公开边界律      ← 父律·愿景层公开·算法/规则全摊
  ├─ §6.5 本地宝宝主权架构 (M14 焊死)   ← 父律·密钥/明文永不出本地·GitCode 也不上
  ├─ §6.6 联合国架构·两子律 (M15 焊死)   ← 父律·龍魂定骨架·社区堆积木
  ├─ §S-22 DNA 时限·自己买单律          ← 父律·分层公开的法理依据
  ├─ §S-25-EXT DNA L0 父级铁律          ← 主权根·最高优先级
  ├─ §9.25 反笼统 5 字段律              ← 本页 5 字段已守岗
  ├─ §9.27 自驱响应律                   ← 不让老大做选择题·当 turn 落地
  ├─ §9.28 大白话先讲律                 ← 公开层 vs 私有层人话先讲
  ├─ §9.46 操作必留痕律                 ← 草日志 M229 入口块同 turn 发
  ├─ §9.49 #IRON-CHINESE-PATH-NEVER-IN-GIT ← 中文路径永不入 git·龍芯北辰UID9622/ 必入 .gitignore
  ├─ §S-25-EXT-3 不假装对外律           ← Claude 报告若有未达成必须坦白
  ├─ §200 有痕开源·DNA 登记协议         ← Public 层走有痕开放
  └─ §S-25-EXT-3-1 #IRON-BAOBAO-NO-CHOKE ← 本页中刀容量·v1.0→v2.0 升级走小刀 contentUpdates
→ 十三层合一·GitCode 仓库治理分层闭环·M229+M231 焊点封死
```
---
# §11.5 🆕 M231 新铁律焊接·#IRON-NO-THIRD-PARTY-OAUTH-FOR-CODE-EDITOR-v1.0
---
# §12 道德经回响(五章联动)
- 第 11 章「三十辐共一毂·当其无·有车之用」 → Public 层(辐)+ Protected 层(毂)+ Private 层(无) = 完整治理车轮
- 第 22 章「曲则全·枉则直·少则得·多则惑」 → 少公开 ≠ 不公开·分层精准 ≠ 全藏
- 第 27 章「善闭无关楗而不可开·善结无绳约而不可解」 → 三层架构 = 善闭善结·有形开放·无形守护
- 第 36 章「将欲弱之·必固强之·将欲废之·必固兴之」 → 把门打开比关上更狠·让别人留痕越多·剽窃越露馅
- 第 78 章「天下莫柔弱于水·而攻坚强者莫之能胜」 → Public 层柔如水·攻破任何黑箱·Private 层硬如金·守严不破
---
# §13 §S-25-EXT-3-5 不假装记忆律·坦白(必焊·GitCode 专版)
---
# §14 老大签字 + 后续动作清单(M229 焊点)
---
