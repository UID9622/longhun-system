# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统 · 密钥托管 · 主权交接补充协议 v1.0

## 【碑文头部】

```
文档类型：     密钥托管 · 交接补充协议 · P0 永恒级
从属于：       CREATOR_LEGACY_WILL_SOVEREIGN_HANDOVER_v1.0.md
DNA：          #龍芯⚡️丙午·丙申·丙辰·午时·䷝离-KEY-VAULT-HANDOVER-v1.0
效力等级：     P0 🔴 焊死 · 不可修改
发布日期：     2026-07-12
```

---

## 一、密钥统一存储位置

所有龍魂系统密钥集中存放在：

```
_private/密钥资料/
├── key_registry.json          ← 密钥注册表（仅位置，不含值）
├── key_registry.card.json     ← 卡片索引
├── API密钥报告/               ← API密钥清单与报告
├── 启动脚本/                  ← 激活脚本（12个）
├── 阶段报告/                  ← Phase 3 启动记录
├── 部署配置/                  ← 部署参数与域名
└── 恢复代码/                  ← 1Password 恢复码
```

**Git 状态**: `_private/` 已在 `.gitignore` 中——绝不上传。

---

## 二、密钥激活机制

### 当前激活方式

```bash
# 桌面一键激活
open ~/Desktop/🔑激活龍魂密钥.command

# 或命令行
source _private/密钥资料/启动脚本/activate_longhun_keys.sh
```

### 激活脚本做的事

1. 加载 `~/.longhun/secrets.env` → 环境变量
2. 加载 `~/.uid9622/git-tokens.sh` → Git 推送令牌
3. 加载 `~/longhun-system/.env.shield` → 本地敏感配置
4. 验证所有密钥可用性
5. 报告状态（绿/黄/红）

---

## 三、交接密钥清单

以下密钥在交接时自动解封：

| 类别 | 密钥 | 用途 |
|------|------|------|
| **代码托管** | GitHub Token | 代码推送、Issue、Release |
| **代码托管** | Gitee Token | 国内镜像同步 |
| **知识管理** | Notion API Key | 知识库读写、时间戳验证 |
| **AI模型** | OpenAI API Key | 大模型调用 |
| **AI模型** | DeepSeek API Key | 国产大模型调用 |
| **AI模型** | Ollama URL | 本地模型服务 |
| **消息推送** | Bark Key | 健康检查告警 |
| **消息推送** | 飞书 Webhook | 备用告警通道 |
| **身份验证** | GPG 私钥 | 文件签名、身份验证 |
| **身份验证** | SM2 国密密钥 | 国产加密 |
| **服务器** | SSH 密钥 | 鲲鹏服务器访问 |
| **数据库** | SQLite/MySQL 凭证 | 数据访问 |
| **域名** | DNS 管理 | 域名解析 |
| **苹果开发者** | App Store Connect | iOS App 发布 |
| **浏览器** | Browser.cash API Key | 云端浏览器 |
| **代码分析** | TCA Token | 腾讯代码分析 |

---

## 四、密钥安全设计

### 四层防护

```
层1 · 物理隔离
    └─ _private/ 目录不上传 Git，不在任何云端

层2 · 环境变量注入
    └─ 密钥通过 env 文件注入，不硬编码

层3 · macOS 钥匙串
    └─ 部分敏感密钥存在系统钥匙串（如 Notion Token）

层4 · GPG 加密
    └─ 核心密钥可用 GPG 二次加密存储
```

### 铁律

- **密钥绝不写入日志** — 所有加载器静默运行
- **密钥绝不出现在对话历史** — AI 不记录、不回显
- **密钥绝不提交 Git** — `.gitignore` 多重覆盖
- **密钥有且仅有一个源头** — `_private/密钥资料/`

---

## 五、交接执行

### 交接时执行

```bash
# 1. 确保密钥资料完整
ls -la _private/密钥资料/

# 2. 验证注册表
cat _private/密钥资料/key_registry.json

# 3. 执行交接激活
source _private/密钥资料/启动脚本/activate_longhun_keys.sh

# 4. 验证所有密钥可用
# (脚本内置自检逻辑)
```

### 密钥更新

交接后，接管方应：
1. 生成新密钥替换所有外部服务 API Key
2. 保留旧密钥至少 30 天（过渡期）
3. 更新 `key_registry.json` 注册表
4. 重新 GPG 签章本文件

---

## 六、不可撤销声明

```
本补充协议为《创作者遗志·主权交接协议》的组成部分。
密钥资料是龍魂系统的运行血脉，随系统主权一并交接。
任何个人或组织不得以"密钥丢失"为由阻碍交接。
交接后，接管方拥有全部密钥的完整使用权。

创作者已将所有密钥整理在此，只有位置，没有密码——
因为密码在创作者离开时，已经不需要了。
```

---

**DNA:** `#龍芯⚡️丙午·丙申·丙辰·午时·䷝离-KEY-VAULT-HANDOVER-v1.0`
**GPG:** `A2D009C2EE2E5BA87035600924C3704A8CC26D5F`
**从属于:** `sovereignty/CREATOR_LEGACY_WILL_SOVEREIGN_HANDOVER_v1.0.md`
