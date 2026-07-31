<!--
DNA: #龍芯⚡️丙午·乙未·乙丑·兑-REGISTRY-DEPLOY-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
-->
# SPEC.md — 龍魂私有 Docker 镜像仓库 规格文档

> 参考方案出处：CSDN《Docker 镜像不求人：从 0 到 1 在自己家里搭一个 13GB 的私有仓库》
> [快速链接: 参考文章] https://blog.csdn.net/Margrop/article/details/163312205
> 要点摘录：registry:2（官方 24MB Go 服务）+ htpasswd(bcrypt) 鉴权 + 宿主机目录持久化 + `--restart=always` 自启 + 客户端 `insecure-registries`。
>
> **关于"13GB"**：参考文章标题的"13GB"是作者仓库**运行后缓存的累计数据量**，不是 registry:2 本身的大小。registry:2 镜像仅 24MB，部署时无需准备 13GB 存储空间，数据量随使用慢慢增长。
>
> 本规格在此基础上增加：多架构自适应（x86_64/aarch64）、自签 TLS 选项、磁盘告警、华为云扣费监控提示、四层目录命名、DNA 追溯签章。

## 0. 方案选型（为什么选 registry:2 而不是 Harbor）

> 这是 SPEC 的第一个决策节点。在 ARM64/鲲鹏环境下，两者部署难度天壤之别。

| 对比维度 | registry:2（轻量版·✅ 已选） | Harbor（企业版） |
|:---|:---|:---|
| 镜像大小 | 24 MB | 10+ 组件镜像（几百 MB） |
| ARM64 支持 | 官方 multi-arch，直接 `docker pull` | **官方不支持 ARM64**，需社区方案或自行编译 |
| 部署复杂度 | 1 条命令 | docker-compose + 多配置文件 |
| 鉴权方式 | htpasswd 文件（bcrypt） | LDAP/AD + RBAC |
| 图形界面 | ❌ 无（API only） | ✅ 有 Web UI |
| 镜像漏洞扫描 | ❌ 无 | ✅ Trivy/Clair |
| 仓库级 ACL | ❌ 不支持 | ✅ 项目级权限 |
| 适合场景 | 个人/小团队，快速私有化 | 企业多团队，需审批+治理 |
| 本仓库选型 | **✅ 第一阶段落地** | 后续评估升级 |

**选型理由**：
1. **鲲鹏 ARM64 落地优先** — Harbor 官方明确"harbor 官方不支持 arm"，社区 ARM64 方案需要额外准备预编译镜像包，风险高。registry:2 官方 multi-arch manifest 直接支持，零编译成本。
2. **用户需求匹配** — 龍魂当前场景是个人私有仓库（Mac ↔ 鲲鹏），不需要多团队 RBAC、镜像扫描等企业功能。htpasswd 认证够用。
3. **渐进式演进** — registry:2 先跑起来，后续若需要企业级功能，Harbor 可直接从 registry:2 导入数据，不丢已有镜像。

## 1. 架构图（文字版）

```
[Mac M4 Max 操作终端]                [公网: Docker Hub / GHCR]
   docker login/push/pull                     ▲ (仅服务器需要新镜像时出公网拉取一次)
            │ HTTPS/HTTP :5000                │
            ▼                                 │
┌──────────────────────────────────────────────────────┐
│  龍魂服务器 (x86_64 或 aarch64, Ubuntu/openEuler + Docker) │
│                                                      │
│   ┌──────────────────────────────────────────────┐   │
│   │ 容器 longhun-registry (registry:2, multi-arch)│   │
│   │  - 监听 0.0.0.0:5000                          │   │
│   │  - htpasswd(bcrypt) 认证                      │   │
│   │  - 可选 TLS（自签 / Let's Encrypt）           │   │
│   │  - --restart=always + systemd 双保险自启      │   │
│   └──────────────┬───────────────────────────────┘   │
│                  │ volume                             │
│   /data/longhun-registry/                            │
│     ├─ 01-physical/   物理层：blob 数据 + 备份        │
│     ├─ 02-identity/   身份层：htpasswd + TLS 证书     │
│     ├─ 03-sovereign/  主权层：config.yml + systemd    │
│     └─ 04-execution/  执行层：监控/运维脚本 + 日志    │
└──────────────────────────────────────────────────────┘
```

## 2. 组件

| 组件 | 镜像 | 架构 | 说明 |
|---|---|---|---|
| 镜像仓库 | `registry:2` | 官方 multi-arch（linux/amd64 + linux/arm64 + …） | 核心服务，24MB，脚本自动检测架构拉对应平台 |
| 密码生成 | `httpd:2.4-alpine` | 官方 multi-arch（linux/amd64 + linux/arm64） | 仅一次性借 htpasswd 命令生成 bcrypt 密码，用完即删 |
| 监控 | 无镜像，纯 bash + crontab | — | 磁盘用量 80% 告警 + GC 回收 |

## 3. 端口

| 端口 | 协议 | 绑定 | 用途 |
|---|---|---|---|
| 5000 | TCP | 0.0.0.0（部署脚本可改） | Registry HTTP/HTTPS API（push/pull/catalog） |

## 4. 数据卷与目录（四层命名）

```
/data/longhun-registry/
├── 01-physical/                  # 物理层：真实数据落盘
│   ├── registry-data/            #   → 挂到容器 /var/lib/registry（所有镜像 blob）
│   └── backups/                  #   → 备份 tar 包存放处
├── 02-identity/                  # 身份层：认证与证书
│   ├── auth/htpasswd             #   → 挂到容器 /auth/htpasswd
│   └── certs/                    #   → 自签证书 domain.crt / domain.key
├── 03-sovereign/                 # 主权层：配置即主权
│   ├── config.yml                #   → 挂到容器 /etc/docker/registry/config.yml
│   └── longhun-registry.service  #   → systemd 兜底自启单元（脚本默认强制安装并 enable）
└── 04-execution/                 # 执行层：运维脚本与日志
    ├── bin/disk_alert.sh         #   → 磁盘 80% 告警脚本（cron 每小时跑）
    ├── bin/gc.sh                 #   → 垃圾回收脚本
    └── logs/                     #   → 告警与运维日志
```

## 5. 安全边界

1. **网络边界**：5000 端口只对家庭/车载内网开放；禁止在路由器/安全组上对公网映射。华为云安全组若使用该服务器，仅放行内网 CIDR。
2. **认证边界**：htpasswd + bcrypt（`-B`），禁用 md5/sha1。默认账号 `longhun`，密码部署时由脚本随机生成并打印一次。
3. **传输边界**：默认 HTTP + 客户端 `insecure-registries`（内网场景，参考文章同款方案）；可选自签 TLS，证书导入 Mac 钥匙串后即 HTTPS。
4. **数据边界**：`/data/longhun-registry/02-identity/` 权限 700；htpasswd 权限 600。镜像 blob 可被任何通过认证的用户推拉，不设仓库级 ACL（registry:2 本身不支持，需要 ACL 请上 Harbor，超出本规格）。
5. **删除保护**：镜像删除通过 `03-sovereign/config.yml` 中的 `storage.delete.enabled: true` 开启（部署脚本写入 config.yml 时默认开启并配套 gc.sh，知悉风险）；不需要删除功能时把该值改为 `false` 并重启容器即可。
