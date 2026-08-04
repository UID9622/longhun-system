# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🌐 龍魂统一门户 longhun888.com

> 龍魂系统对外官网入口：能力展示 + API 文档 + 控制台 + Notion/CSDN/论文导航。  
> **DNA:** `#龍芯⚡️2026-07-04-LONGHUN888-PORTAL-v1.0`

---

## 目录结构

```
longhun-system/portal/
├── index.html                  # 官网首页
├── console.html                # v3 统一操作台
├── docker-compose.yml          # 生产编排
├── nginx/longhun888.conf       # Nginx 入口配置
├── deploy_huawei_cloud_portal.sh  # 华为云一键部署
├── data/
│   ├── notion_nav.json         # Notion 导航索引
│   ├── csdn_articles.json      # CSDN 已同步文章
│   ├── papers.json             # 论文/协议分类
│   └── cnsh_openapi.json       # CNSH API OpenAPI 规范
└── README.md                   # 本文件
```

---

## 本地预览

```bash
lh 门户
```

或手动：

```bash
cd ~/longhun-system/portal
python3 -m http.server 8777
```

访问：`http://127.0.0.1:8777/`

---

## 华为云部署

### 前置条件

- 华为云 ECS（推荐鲲鹏 ARM64），安全组放行 `80`、`443`、`22`。
- 已安装 Docker、Docker Compose。
- 配置环境变量：

```bash
export HW_ACCESS_KEY_ID=你的AK
export HW_SECRET_ACCESS_KEY=你的SK
export HW_REGION=cn-southwest-2
export HW_ECS_IP=你的弹性公网IP
export HW_ECS_USER=root
export HW_SWR_SERVER=swr.cn-southwest-2.myhuaweicloud.com
export HW_SWR_ORGANIZATION=你的组织名
```

### 执行部署

```bash
cd ~/longhun-system/portal
./deploy_huawei_cloud_portal.sh
```

部署完成后：

- 门户：`http://<HW_ECS_IP>/`
- CNSH 编辑器：`http://<HW_ECS_IP>/editor/`
- API 文档：`http://<HW_ECS_IP>/docs`

### 域名与 HTTPS

1. 在 DNS 解析中将 `longhun888.com` 指向 `HW_ECS_IP`。
2. 配置 SSL 证书（华为云 SSL / certbot）。
3. 更新 `nginx/longhun888.conf` 的 `server_name` 并启用 443。

---

## 数据更新

### Notion 导航

```bash
cp ~/.kimi-code/skills/longhun-notion-portal/scripts/notion_portal.json \
   ~/longhun-system/portal/data/notion_nav.json
```

### CSDN 文章

启动 csdn-sync 服务后：

```bash
curl http://127.0.0.1:9528/api/published > ~/longhun-system/portal/data/csdn_articles.json
```

### 论文/协议

```bash
curl http://127.0.0.1:8088/api/knowledge/classify > ~/longhun-system/portal/data/papers.json
```

### OpenAPI

```bash
curl http://127.0.0.1:18000/openapi.json > ~/longhun-system/portal/data/cnsh_openapi.json
```

---

## 架构

```
用户 → 华为云公网 IP :80/:443
         ↓
      Nginx（统一入口）
         ├── /            → 静态门户
         ├── /editor/     → CNSH Editor API
         ├── /a../     → CNSH Editor API
         └── /docs        → Swagger UI
```

---

**龍魂系统 · 中国自主可控 · 数据主权归人民**  
**CONFIRM:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z` ✅
