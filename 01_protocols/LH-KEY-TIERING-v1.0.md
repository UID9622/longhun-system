# 龍魂·密钥分档与存储方案 v1.0

> 抬头模板: [3] 📜 协议/原则声明型 · 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> DNA: #龍芯⚡️20260828-KEY-TIERING-v1.0-VAULT-GOVERNANCE
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 创建者: 诸葛鑫（UID9622） · 协议: CC BY-NC-SA 4.0（核心思想层）· MulanPSL v2（工程实现层）
> 上位: `.codebuddy/rules/` 统一密钥库 v3.0 · 底座: `bin/lh_vault.py`（macOS Keychain · service=longhun-vault）
> 三色: 🟢 8条真实密钥已入库·注册表干净 · 🟡 高德/百度 key 待老大提供 · 🔴 无

---

## 一、为什么要有这份表

老大指令（8/28）：**所有密钥全部统一管理，什么时候用哪个储存方案也要定死**。
已有底座: `lh_vault.py` v3.0 = macOS Keychain（系统级 AES 加密·绑登录密码/指纹）+ 注册表 `~/.longhun/vault_registry.json`（只记名·不记值）。
本表把"密钥怎么分档、放哪、怎么读"焊死，AI 按表执行，不逐次请示。

## 二、密钥分档表（T1~T4 · 唯一裁决表）

| 档 | 内容 | 主存 | 读取方式 | 已入库实例 | 示例键名 |
|:---:|:---|:---|:---|:---|:---|
| **T1 高敏凭据** | 云 AK/SK·邮箱密码·GPG 口令·主密钥 | macOS Keychain (vault) | `lh_vault get/env` · 永不落盘 | 华为云 hcloud-aksk · MASTER_KEY_ENCRYPTED | `HUAWEI_AK/SK` · `LONGHUN_GPG_PASSPHRASE` |
| **T2 API 密钥** | 各平台 API Key / Token | macOS Keychain (vault) | `lh_vault get/env` | NOTION_TOKEN · KIMI · DEEPSEEK · GITHUB_PAT · TCA · BARK | `AMAP_KEY` · `FEISHU_APP_SECRET` · `TENCENT_SECRET_ID/KEY` · `MOONSHOT_API_KEY` |
| **T3 通知/低敏** | Webhook·Bark·DB URL·内部 JWT | `~/.env`（权限600·不进git）+ vault 兜底 | 服务启动时 vault `env` 导出 | BARK_KEY | `DINGTALK_WEBHOOK` · `REDIS_URL` · `DATABASE_URL` |
| **T4 标识符配置** | DB ID·端口·路径·模型名（非密钥） | 项目配置文件 | 直接读 | — | `NOTION_DATABASE_ID` · `LH_MEMORY_PORT` · `OLLAMA_MODEL` |

## 三、什么时候用哪个存储方案（决策树·硬规则）

```
新发现一个密钥值 →
  ├─ 是高敏/API Key? ──是──→ T1/T2: put 进 Keychain vault（唯一主存·值不落盘）
  │
  └─ 否（webhook/url/jwt 内部）→ T3: 写入 ~/.env（600 权限）+ vault put 兜底
                ↓
任何服务启动需要 env →
  ├─ 用 `lh_vault env` 导出（内存注入·不写死明文）✅ 首选
  ├─ 或读 ~/.env（T3 低敏）
  └─ ❌ 禁止：明文写死进代码/配置/git
```

**附加硬规则：**
1. **值永不落盘、永不打印、永不进 git、永不上传云**（Keychain 是唯一明文持有者）
2. **配置文件需要 token** → 从 vault `get` 注入，禁止复制粘贴明文
3. **密钥失效（401 等）** → AI 自动 `lh_vault archive --reason` · 值冻结保留（不删除只冻结 = P0 天条）
4. **检测到新密钥**（对话/CSV/.env/conf）→ AI 自动 `detect/put`，不等老大说"存"（v3.0 铁律）
5. **平台限制**：手机/非 Mac 端没有 Keychain → 走华为云 KMS 或鲲鹏加密存储（T2 以上不进）
6. **MCP/工具要 token**（如 mcp.json）→ 保留其运行必需的最小明文副本 + vault 留底；明文副本不入 git

## 四、现状台账（2026-08-28 · 已入库 8 条）

| 名称 | 档 | 用途 | 状态 |
|:---|:---:|:---|:---:|
| hcloud-aksk | T1 | 华为云 AK:SK · cn-north-4 | 🟢 active |
| MASTER_KEY_ENCRYPTED | T1 | 数据主密钥加密值 | 🟢 active |
| NOTION_TOKEN | T2 | Notion 集成 token（mcp.json 主用） | 🟢 active |
| KIMI_API_KEY | T2 | Kimi/月之暗面 | 🟢 active |
| DEEPSEEK_API_KEY | T2 | DeepSeek | 🟢 active |
| BARK_KEY | T2/T3 | Bark 推送（健康检查） | 🟢 active |
| GITHUB_PERSONAL_ACCESS_TOKEN | T2 | GitHub PAT（mcp.json） | 🟢 active |
| TCA_TOKEN | T2 | 腾讯云代码分析 | 🟢 active |

**待配置（有读取点·无值·等老大提供后 AI 自动 put）：**
- `AMAP_KEY`（高德地图 · `lh_map_api.py` 读取点已就绪）
- `BAIDU_API_KEY`（百度地图 · 同上）

**已知未入库的存量密钥（扫描发现 · 按需补入）：**
飞书 6 件套 · 钉钉 Webhook · 企业微信 Webhook · Telegram Bot · 腾讯云 SECRET_ID/KEY · SMTP 密码 · 邮箱密码 · Gmail AppPw · NEO4J/Redis/DB URL · 内部 JWT/Admin Token 等（都在 319 个 env 键名中，需要时用 `lh_vault detect <文件>` 或手工 put）

## 五、GPG 签名

```
DNA:    #龍芯⚡️20260828-KEY-TIERING-v1.0-VAULT-GOVERNANCE
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
GPG:    A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色:   🟢 8条已入库 · 🟡 高德/百度待配 · 🔴 0
v1.0 · 2026-08-28 · UID9622 + AI
