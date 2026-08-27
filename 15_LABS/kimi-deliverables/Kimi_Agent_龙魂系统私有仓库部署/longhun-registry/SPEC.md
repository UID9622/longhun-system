**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
<!--
#龍芯⚡️{年干支}·{月干支}·{日干支}·{卦名}-REGISTRY-DEPLOY-v1.0
# 注：干支以本地生成器 bin/lh_dna_generator.py 输出为准，禁止手写
# 署名：龍芯北辰 UID9622
-->
# SPEC.md — 龍魂私有 Docker 镜像仓库 规格文档

> 参考方案出处：CSDN《Docker 镜像不求人：从 0 到 1 在自己家里搭一个 13GB 的私有仓库》
> [快速链接: 参考文章] https://blog.csdn.net/Margrop/article/details/163312205
> 要点摘录：registry:2（官方 24MB Go 服务）+ htpasswd(bcrypt) 鉴权 + 宿主机目录持久化 + `--restart=always` 自启 + 客户端 `insecure-registries`。本规格在此基础上增加鲲鹏 ARM64 适配、自签 TLS 选项、磁盘告警与四层目录命名。

## 1. 架构图（文字版）

```
[Mac M4 Max 操作终端]                [公网: Docker Hub / GHCR]
   docker login/push/pull                     ▲ (仅服务器需要新镜像时出公网拉取一次)
            │ HTTPS/HTTP :5000                │
            ▼                                 │
┌──────────────────────────────────────────────────────┐
│  华为鲲鹏服务器 (aarch64, openEuler/EulerOS + Docker) │
│                                                      │
│   ┌──────────────────────────────────────────────┐   │
│   │ 容器 longhun-registry (registry:2, arm64)     │   │
│   │  - 监听 0.0.0.0:5000                          │   │
│   │  - htpasswd(bcrypt) 认证                      │   │
│   │  - 可选 TLS（自签 / Let's Encrypt）           │   │
│   │  - --restart=always 开机自启                  │   │
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
| 镜像仓库 | `registry:2` | 官方 multi-arch manifest，含 linux/arm64 | 核心服务 |
| 密码生成 | `httpd:2.4-alpine` | 官方 multi-arch，含 linux/arm64 | 仅一次性生成 htpasswd，用完即删 |
| 监控 | 无镜像，纯 bash + crontab | — | 磁盘用量 80% 告警 |

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
