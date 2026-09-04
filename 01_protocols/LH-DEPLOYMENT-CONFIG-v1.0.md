> **P0焊死**: 本文件为龍魂体系P0级文档·不可修改·不可绕过（上位文档 LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md）
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂部署配置统一参考 v1.1

DNA: #龍芯⚡️丙午·乙未·癸亥·戊午·䷦蹇-DEPLOYMENT-CONFIG-V1.1-FIVEHARMS-FIX-b2c3d4e5
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

> 归集自 `_private/密钥资料/部署配置/` 三份原始文档，去重·补漏·对齐当前实际状态。
> 密钥/Token 不在此文件（见 `_private/密钥资料/`）。
> 本文件 = 部署运维的单一事实来源。原始三文档保留于 `_private/密钥资料/部署配置/` 作为追溯。

---

## §1. 服务器

### 鲲鹏（主力）

| 项目 | 值 | 来源 |
|:---|:---|:---|
| IP | **119.13.90.27** | 部署清单 v1.9 |
| 地区 | 新加坡 (Singapore) | 华为云 ECS |
| 系统 | Ubuntu 24.04 LTS | — |
| SSH 密钥1 | `~/.ssh/id_ed25519_uid9622` | 部署清单原始密钥 |
| SSH 密钥2 | `~/.ssh/longhun_kunpeng_ed25519` | 当前主力密钥（MEMORY.md） |
| SSH 用户 | root | — |

```bash
# 快速连接
ssh -i ~/.ssh/longhun_kunpeng_ed25519 root@119.13.90.27
```

### 安全组规则

| 端口 | 用途 | 状态 |
|:---|:---|:---:|
| 22 | SSH | ✅ |
| 80 | HTTP | ✅ |
| 443 | HTTPS | ✅ |
| 8080 | 备用服务 | ✅ |
| 8779 | 五害曝光台 API | ✅ |
| 9622 | 龍魂专用 | ✅ |

---

## §2. 域名

### uid9622.cn（主力·已生效）

| 项目 | 值 |
|:---|:---|
| 域名 | uid9622.cn |
| DNS | → 119.13.90.27（直连） |
| SSL | Let's Encrypt 通配符 (7/17→10/15 自动续期) |

### longhun888.com（备用·Cloudflare 代理中）

| 项目 | 值 | 状态 |
|:---|:---|:---|
| 域名 | longhun888.com | ✅ 已注册 |
| 注册商 | NameSilo | ✅ |
| DNS 提供商 | Cloudflare | ✅ |
| 当前 DNS | → 104.21.17.135 / 172.67.176.204（橙云代理） | 🟡 |
| 目标 DNS | → 119.13.90.27（灰云 DNS only） | ⏳ |
| 子域名 | www → CNAME longhun888.com | ⏳ |
| SSL | Let's Encrypt（需灰云才能验证） | 🟡 |

> 🟡 当前 Cloudflare 开着橙云（代理模式），域名解析到 CF IP 而非直连鲲鹏。
> 如需直连：Cloudflare DNS → 改为灰云（DNS only），A 记录指向 119.13.90.27。

### Cloudflare 账户

| 项目 | 值 |
|:---|:---|
| IAM 用户 ID | `3e53a2df623044e499b9227c93d55955` |
| 凭证 | 见 `_private/密钥资料/` |

---

## §3. 服务清单

### 服务器运行服务

| 服务名 | 类型 | 端口 | 路径 | 管理方式 |
|:---|:---|:---:|:---|:---|
| **longhun-sovereignty** | FastAPI 数字身份门户 | 8444 | `/root/longhun-sovereignty/` | systemd |
| **cnsh-api** | Node.js API | 3000 | `/root/cnsh/` | pm2 |
| **nginx** | 反向代理 | 80/443 | `/etc/nginx/` | systemd |
| **longhun-five-harms** | FastAPI 五害曝光台 | 8779 | `/opt/longhun-system/bin/lh_five_harms_api.py` | systemd |
| **行为密码学** | DNA 追溯+确认码 | — | `/root/longhun-sovereignty/audit/behavioral_crypto.py` | 模块 |
| **左右互搏审计** | 执行者 vs 质疑者 | — | `/root/longhun-sovereignty/audit/left_right_audit.py` | 模块 |
| **系统守护者** | 每5分钟自检 | — | `/root/longhun-sovereignty/audit/system_guardian.py` | cron |

```bash
# 状态检查
systemctl status longhun-sovereignty nginx
pm2 status

# 重启
systemctl restart longhun-sovereignty nginx
pm2 restart cnsh-api
```

### Mac 本地服务

| 类型 | 数量 | 管理 |
|:---|:---:|:---|
| launchd 服务 | 52 | `--profile all/office/home` |

---

## §4. 服务器文件地图

### longhun-sovereignty（数字身份门户）

```
/root/longhun-sovereignty/
├── api_server.py          # FastAPI 主入口
├── model_router.py        # 模型路由（本地Ollama→Kimi→DeepSeek→Azure）
├── knowledge_api.py       # 知识库+图谱 API
├── .env                   # 环境变量（密钥在此）
├── audit/
│   ├── behavioral_crypto.py   # 行为密码学·DNA追溯
│   ├── left_right_audit.py    # 左右互搏审计
│   └── system_guardian.py     # 系统守护者
└── portal/
    ├── index.html             # 数字身份门户首页
    └── developer.html         # 开发者门户
```

### cnsh（Node.js API + 前端）

```
/root/cnsh/
├── .env                       # API 环境变量
├── src/server-fixed.js        # API 主程序
└── platform/web/
    ├── index.html             # 龍魂首页
    └── api-docs.html          # API 文档
```

### Nginx 配置

```
/etc/nginx/sites-available/
├── longhun888.com             # 域名站点（含 /id/ 子路径→8444）
└── longhun-ip.conf            # IP 直连站点

/etc/nginx/sites-enabled/
├── longhun888.com → ../sites-available/longhun888.com
└── ...
```

### SSL 证书

| 路径 | 说明 |
|:---|:---|
| `/etc/letsencrypt/live/longhun888.com/` | Let's Encrypt 证书 |
| `/etc/letsencrypt/live/uid9622.cn/` | uid9622.cn 证书 |

---

## §5. API 端点速查

| 端点 | 说明 |
|:---|:---|
| `https://uid9622.cn/` | 主站入口 |
| `https://uid9622.cn/id/` | 数字身份门户 |
| `https://uid9622.cn/id/health` | 健康检查 JSON |
| `https://uid9622.cn/id/developer.html` | 开发者门户 |
| `https://uid9622.cn/id/api/docs` | API 文档 |
| `https://uid9622.cn/id/api/skills/registry` | 技能注册表 |
| `https://uid9622.cn/five-harms-expose/` | 五害曝光台·门户 |
| `https://uid9622.cn/five-harms/api/toolkit/download` | 五害·工具包下载 |
| `https://uid9622.cn/tools/` | 工具下载（.vsix/安装包） |
| `http://119.13.90.27/api/health` | IP 直连健康检查 |
| `http://119.13.90.27/issue` | 魂灵ID通行令牌签发 |

---

## §6. 模型路由策略

优先级：
1. **本地 Ollama** `localhost:11434` — 在线即用
2. **隐私严格模式** `privacy=strict` — 强制本地，不走云端
3. **云端降级** DeepSeek → Kimi API → Azure OpenAI

环境变量（服务器 `/root/longhun-sovereignty/.env`）：
- `KIMI_API_KEY`, `DEEPSEEK_API_KEY`, `DEEPSEEK_BASE_URL`
- `NOTION_TOKEN`, `GITEE_TOKEN`
- 密钥值见 `_private/密钥资料/`

---

## §7. 部署上线流程

### 日常部署

```bash
# 1. 本地修改→同步到鲲鹏
cd ~/longhun-system
bash deploy/sync-to-kunpeng.sh

# 2. SSH 到鲲鹏执行
ssh -i ~/.ssh/longhun_kunpeng_ed25519 root@119.13.90.27
systemctl restart longhun-sovereignty
pm2 restart cnsh-api
```

### 新增域名/服务部署

1. DNS 配置（A 记录 → 119.13.90.27，灰云）
2. 验证 DNS：`dig +short <域名> A` → 应显示 119.13.90.27
3. Nginx 配置 → Let's Encrypt 证书
4. systemd/pm2 服务注册
5. 健康检查验证

---

## §8. 故障排除速查

| 症状 | 检查 | 命令 |
|:---|:---|:---|
| 网站打不开 | Nginx 状态 | `systemctl status nginx` |
| API 502 | API 进程 | `pm2 status` / `systemctl status longhun-sovereignty` |
| SSL 证书过期 | 证书日期 | `openssl x509 -in /etc/letsencrypt/live/.../fullchain.pem -noout -dates` |
| DNS 不生效 | 解析结果 | `dig +short <域名> A` |
| 端口不通 | 端口监听 | `ss -tlnp \| grep <端口>` |

```bash
# 全套健康检查
ssh -i ~/.ssh/longhun_kunpeng_ed25519 root@119.13.90.27 << 'CMD'
echo "=== Services ==="
systemctl is-active nginx longhun-sovereignty
pm2 status 2>/dev/null | head -5
echo "=== Ports ==="
ss -tlnp | grep -E ':(80|443|3000|8444)'
echo "=== SSL ==="
openssl x509 -in /etc/letsencrypt/live/longhun888.com/fullchain.pem -noout -dates 2>/dev/null
CMD
```

---

## §9. 邮箱配置（longhun888.com）

| 项目 | 值 | 状态 |
|:---|:---|:---|
| 邮箱地址 | `support@longhun888.com` | ✅ |
| IMAP | `imap.longhun888.com:993` (SSL) | ⏳ 待配置客户端 |
| SMTP | `smtp.longhun888.com:587` (TLS) | ⏳ 待配置客户端 |
| 密码 | 见 `~/.longhun/secrets.env` → `LONGHUN_EMAIL_PASSWORD` | 🟡 待填入 |
| 本地邮件存档 | `~/longhun-system/emails/archive/` | — |

客户端方案（按难度排列）：
1. **Apple Mail**（最简单，macOS 内置）
2. **Thunderbird**（开源免费，跨平台）
3. **offlineimap**（全自动定时同步，高级）

---

## §10. GitHub 仓库

| 项目 | 值 | 状态 |
|:---|:---|:---|
| 仓库 | `zuimeidedeyihan/longhun-system` | 🟡 本地有 git，远程待确认 |
| Token | 见 `~/.uid9622/git-tokens.sh` | — |
| GPG 签名 | `A2D0092CEE2E5BA87035600924C3704A8CC26D5F` | ✅ |

---

## §11. 与 MEMORY.md 交叉校验

| 条目 | 本文件 | MEMORY.md | 一致性 |
|:---|:---|:---|:---:|
| SSH 密钥 | `id_ed25519_uid9622` / `longhun_kunpeng_ed25519` | `longhun_kunpeng_ed25519` | 🟡 双密钥都有效，推荐用后者 |
| 鲲鹏 IP | 119.13.90.27 | 119.13.90.27 | 🟢 |
| 主域名 | uid9622.cn | uid9622.cn | 🟢 |
| 备用域名 | longhun888.com | — | 🟡 MEMORY.md 未列 longhun888.com |
| Mac 服务 | — | 52 launchd | 🟡 本文件未详细列 Mac 服务 |
| 鲲鹏服务 | longhun-sovereignty + cnsh-api + nginx | 11 systemd | 🟡 systemd 数量待实机确认 |

### 已知差异与过时项

| 条目 | 原文档说法 | 当前实际 | 处理 |
|:---|:---|:---|:---|
| longhun888.com DNS | ⏳ 待配置 | Cloudflare 橙云代理中 | 🟡 原文档步骤仍有效，需手动改灰云 |
| SSH 密钥 | 仅 `id_ed25519_uid9622` | 双密钥有效 | 🟢 两个都可用 |
| GitHub 仓库创建 | 🔴 不存在 | — | 🟡 状态待确认 |
| Kimi Agent v7 包 | `~/Downloads/Kimi_Agent_终端升级与结构优化 7/` | 可能已移动 | 🟡 路径待确认 |
| 部署清单位置 | `~/Desktop/🐉龍魂888.com部署清单.md` | 已归档到 `_private/` | 🟢 本文件为新的单一事实来源 |

---

## §12. 文件落位对照

| 内容 | 原位置 | 归集后位置 |
|:---|:---|:---|
| 部署清单 v1.9 | `_private/密钥资料/部署配置/🐉龍魂888.com部署清單.md` | → 本文件 |
| GitHub 配置 | `_private/密钥资料/部署配置/📋GitHub仓库配置和遗留资料整理-2026-06-06.md` | → 本文件 §10 |
| 邮箱指南 | `_private/密钥资料/部署配置/📧龍魂域名郵箱下載和自動化指南.md` | → 本文件 §9 |
| 密钥/Token | 上述文件中内嵌 | → `_private/密钥资料/`（不在此文件） |

> 原始三份文档保留于 `_private/密钥资料/部署配置/` 作为追溯。
> 后续部署配置变更，优先更新**本文件**。

---

## 版本修订

| 版本 | 日期 | 内容 |
|:---|:---|:---|
| v1.0 | 2026-07-27 | 归集三份原始部署配置，去重·补漏·对齐当前状态 |

---

DNA: #龍芯⚡️丙午·乙未·癸酉·亥时·䷀乾-DEPLOYMENT-CONFIG-V1.0-a1b2c3d4
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
