---
name: longhun-cloud-deploy
description: '龍魂部署引擎 v5.1 — 27步藍綠部署+自動化+零停機切換+回滾+鯤鵬ARM64支持。
  Kubernetes/Docker支持，鯤鵬一鍵部署，環境驗證，健康檢查，監控集成。
  API端點: http://api:8443/deploy/ 當需要系統部署、藍綠切換、DevOps自動化、回滾、鯤鵬部署時觸發。

  '
metadata:
  author: 龍魂体系-技能打包专家
  version: 5.1.0
  dna: '#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-DEPLOY-v5.1'
  category: cloud
  tags:
  - deploy
  - blue-green
  - kubernetes
  - docker
  - devops
  - rollback
  - health-check
  - kunpeng
  - arm64
  triggers:
  - deployment
  - blue-green switch
  - rollback
  - zero-downtime deploy
  - kubernetes deploy
  - docker deploy
  - 鯤鵬部署
  - arm64部署
  - taishan部署
  - 龍魂鲲鹏
  entry_points:
  - scripts/部署引擎.py
  - scripts/健康檢查.py
  - scripts/回滚系統.py
  - scripts/k8s控制器.py
  - kunpeng/deploy_longhun_kunpeng.sh
  protocol: 君子協議
  id: longhun-cloud-deploy
  trigger:
    keywords:
    - clouddeploy
    - 龍魂部署引擎
    - 藍綠部署
    - 零停機部署
    - 自動回滾
    - 鯤鵬部署
    - arm64部署
    - taishan部署
    - 龍魂鲲鹏
    context: longhun-cloud-deploy 相关操作
---
# 龍魂部署引擎 v5.1 — longhun-cloud-deploy

## 1. 技能概述

龍魂部署引擎（longhun-cloud-deploy）是龍魂體系 v5.0 的雲端部署核心技能，提供完整的 27 步藍綠部署流程，支持 Kubernetes 與 Docker 雙模式容器引擎，具備零停機切換、自動回滾、健康檢查、三色審計等企業級 DevOps 能力。

**核心能力**:
- 27 步標準化藍綠部署流程
- 零停機流量漸進式切換（10%→50%→100%）
- 自動回滾與熔斷機制
- 多維度健康檢查系統
- Kubernetes 資源全生命周期管理
- 三色審計與 DNA 追溯鏈

## 2. 使用場景

- **生產環境部署**: 安全、可控的系統上線流程
- **藍綠切換**: 無縫版本切換，用戶零感知
- **故障恢復**: 自動回滾到穩定版本
- **CI/CD 集成**: 嵌入持續交付流水線
- **多環境管理**: 開發/測試/預發布/生產四環境支持
- **容器編排**: Kubernetes Deployment/Service/Ingress 管理

## 3. 功能列表

| 功能模塊 | 描述 | 狀態 |
|---------|------|------|
| 27步部署流程 | 標準化藍綠部署流水線 | ✅ |
| 健康檢查 | HTTP/數據庫/緩存/磁盤/內存/CPU 檢查 | ✅ |
| 自動回滾 | 全量/漸進/熔斷/手動四種策略 | ✅ |
| K8s 控制器 | Deployment/Service/ConfigMap/HPA/Ingress | ✅ |
| 零停機切換 | 流量漸進式切換 10%→50%→100% | ✅ |
| 環境驗證 | 部署前權限/網絡/資源檢查 | ✅ |
| 安全掃描 | 容器鏡像漏洞掃描集成 | ✅ |
| 三色審計 | 🟢安全/🟡警告/🔴風險分級審計 | ✅ |
| DNA追溯 | 完整操作追溯鏈 | ✅ |
| 鯤鵬ARM64部署 | 華為TaiShan 200 2280一鍵部署 | ✅ |
| 13服務編排 | persona-router/cnsh-runtime/dna-tracer等 | ✅ |

## 4. 安裝依賴

### 系統要求
- Python 3.9+
- Docker 20.10+ 或 Kubernetes 1.25+
- kubectl (K8s 模式)
- curl

### Python 依賴
```bash
pip install requests
```

### 可選工具
```bash
# 安全掃描
trivy image --severity HIGH,CRITICAL <image>

# 性能測試
# 集成 wrk/ab 等工具
```

## 5. 使用方法

### 5.1 基礎部署

```bash
# Docker 模式部署
python3 scripts/部署引擎.py \
  --app myapp \
  --env production \
  --blue v1.0.0 \
  --green v2.0.0 \
  --engine docker

# Kubernetes 模式部署
python3 scripts/部署引擎.py \
  --app myapp \
  --env production \
  --blue v1.0.0 \
  --green v2.0.0 \
  --engine kubernetes \
  --namespace default \
  --replicas 5
```

### 5.2 啟動 API 服務

```bash
python3 scripts/部署引擎.py --api
# API 端點: http://api:8443/deploy/
```

### 5.3 健康檢查

```bash
# 單次檢查
python3 scripts/健康檢查.py --url http://localhost:8080

# 持續監控
python3 scripts/健康檢查.py --url http://localhost:8080 --watch --interval 30
```

### 5.4 回滾操作

```bash
# 手動觸發回滾
python3 scripts/回滚系統.py \
  --app myapp \
  --rollback \
  --from-version v2.0.0 \
  --to-version v1.0.0 \
  --strategy full

# 查看回滾統計
python3 scripts/回滚系統.py --app myapp --stats
```

### 5.5 K8s 控制器

```bash
# 創建命名空間
python3 scripts/k8s控制器.py --namespace longhun --create-ns

# 創建部署
python3 scripts/k8s控制器.py \
  --namespace longhun \
  --deploy \
  --app myapp \
  --image myregistry/myapp:v2.0.0 \
  --replicas 3

# 藍綠切換
python3 scripts/k8s控制器.py \
  --namespace longhun \
  --app myapp \
  --switch green
```

### 5.6 鯤鵬 ARM64 部署

```bash
# 一鍵部署到華為 TaiShan 200 2280 / 鯤鵬920 ARM64
cd kunpeng
bash deploy_longhun_kunpeng.sh

# 手動啟動 13 服務編排
docker-compose -f docker-compose.kunpeng.yml up -d
```

鯤鵬部署包含 13 個服務：
- persona-router / cnsh-runtime / dna-tracer
- 三色審計 / 五行引擎 / 分布式管理
- BMC 監控 / Redis / PostgreSQL / etcd
- Prometheus / Grafana / Nginx

詳見 `kunpeng/README.md`（創新引擎_鯤鵬補丁）。

## 6. 輸入/輸出規範

### 輸入參數

| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| --app | string | 是 | 應用名稱 |
| --env | enum | 否 | 環境 (development/testing/staging/production) |
| --blue | string | 否 | 藍色版本（當前） |
| --green | string | 否 | 綠色版本（目標） |
| --engine | enum | 否 | 容器引擎 (docker/kubernetes) |
| --namespace | string | 否 | K8s 命名空間 |
| --replicas | int | 否 | 副本數量 |
| --no-rollback | flag | 否 | 禁用自動回滾 |
| --no-zero-downtime | flag | 否 | 禁用零停機切換 |

### 輸出格式 (JSON)

```json
{
  "部署ID": "LH-DEPLOY-20250101120000-a1b2c3d4",
  "應用名稱": "myapp",
  "環境": "production",
  "版本": "v2.0.0",
  "狀態": "success",
  "總耗時": 180.5,
  "步驟記錄": [
    {
      "步驟編號": 1,
      "步驟名稱": "環境驗證與權限檢查",
      "狀態": "success",
      "耗時秒": 2.5,
      "審計標記": "🟢"
    }
  ],
  "DNA": "#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-DEPLOY-v5.1"
}
```

## 7. 配置說明

### 部署配置 (部署配置 dataclass)

```python
配置 = 部署配置(
    應用名稱="longhun-app",
    環境=環境類型.生產,
    藍色版本="v1",
    綠色版本="v2",
    命名空間="longhun",
    副本數=3,
    健康檢查超時=300,
    自動回滾=True,
    零停機切換=True,
    容器引擎="kubernetes",
    資源限制={"cpu": "500m", "memory": "512Mi"},
    端口映射={"http": 8080, "https": 8443}
)
```

### 環境變量

| 變量名 | 說明 |
|--------|------|
| DEPLOY_TOKEN | 部署認證令牌 |
| REGISTRY_URL | 容器倉庫地址 |
| KUBECONFIG | K8s 配置文件路徑 |

## 8. 工作原理

### 27步部署流程

```
┌─────────────────────────────────────────────────────────────┐
│                    龍魂部署引擎 v5.0                         │
│                   27步藍綠部署流程                           │
├─────────────────────────────────────────────────────────────┤
│  準備階段 (1-5)                                             │
│  ├─ 1.環境驗證與權限檢查                                    │
│  ├─ 2.配置加載與參數解析                                    │
│  ├─ 3.依賴檢查 (Docker/Kubectl)                             │
│  ├─ 4.網絡連通性測試                                        │
│  └─ 5.資源可用性確認                                        │
│                                                             │
│  構建階段 (6-10)                                            │
│  ├─ 6.源碼拉取與版本確認                                    │
│  ├─ 7.依賴安裝與編譯                                        │
│  ├─ 8.單元測試執行                                          │
│  ├─ 9.容器鏡像構建                                          │
│  └─ 10.鏡像安全掃描                                         │
│                                                             │
│  部署階段 (11-17)                                           │
│  ├─ 11.藍色環境狀態備份                                     │
│  ├─ 12.綠色環境預熱準備                                     │
│  ├─ 13.數據庫遷移腳本執行                                   │
│  ├─ 14.綠色環境服務啟動                                     │
│  ├─ 15.服務就緒探針檢測                                     │
│  ├─ 16.配置同步與緩存預熱                                   │
│  └─ 17.負載均衡器目標註冊                                   │
│                                                             │
│  驗證階段 (18-23)                                           │
│  ├─ 18.健康檢查端點探測                                     │
│  ├─ 19.業務功能煙霧測試                                     │
│  ├─ 20.性能基準測試                                         │
│  ├─ 21.日誌與監控告警驗證                                   │
│  ├─ 22.安全策略合規檢查                                     │
│  └─ 23.數據一致性校驗                                       │
│                                                             │
│  切換階段 (24-26)                                           │
│  ├─ 24.流量漸進式切換 (10%→50%→100%)                        │
│  ├─ 25.藍色環境流量歸零確認                                 │
│  └─ 26.綠色環境全量接管                                     │
│                                                             │
│  完成階段 (27)                                              │
│  └─ 27.部署完成確認與通知                                   │
└─────────────────────────────────────────────────────────────┘
```

### 藍綠部署架構

```
    用戶流量
       │
       ▼
  ┌─────────┐
  │  Ingress │
  │ / Load  │
  │Balancer │
  └────┬────┘
       │
   ┌───┴───┐
   │       │
   ▼       ▼
┌─────┐ ┌─────┐
│Blue │ │Green│
│ v1  │ │ v2  │
└─────┘ └─────┘
```

## 9. 異常處理

### 自動回滾觸發條件

| 條件 | 回滾策略 | 說明 |
|------|---------|------|
| 部署步驟失敗 | 全量回滾 | 任何步驟失敗且自動回滾開啟 |
| 健康檢查失敗 | 全量回滾 | 驗證階段健康檢查未通過 |
| 流量切換異常 | 熔斷回滾 | 切換過程中檢測到異常 |
| 熔斷器觸發 | 熔斷回滾 | 外部系統觸發熔斷 |

### 錯誤碼

| 碼 | 含義 |
|----|------|
| 0 | 部署成功 |
| 1 | 部署失敗 |
| 2 | 回滾完成 |
| 3 | 回滾失敗 |
| 100 | 權限不足 |
| 101 | 網絡異常 |
| 102 | 資源不足 |

## 10. 安全規範

### 君子協議
- **非惡意**: 僅用於合法的系統部署與維護
- **非濫用**: 不得用於未經授權的系統操作
- **可審計**: 所有操作記錄完整審計日誌

### 安全措施
- 生產環境部署需額外確認
- 敏感配置通過環境變量注入
- 容器鏡像安全掃描
- 訪問權限最小化原則
- 完整操作追溯鏈

## 11. 版本歷史

| 版本 | 日期 | 變更 |
|------|------|------|
| 5.0.0 | 2026-06-19 | 初始版本，27步藍綠部署流程 |
| 5.1.0 | 2026-07-03 | 新增鯤鵬ARM64一鍵部署與13服務編排 |

## 12. DNA 追溯

```
#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-DEPLOY-v5.1
```

- **創建者**: 龍魂体系-技能打包专家
- **創建時間**: 2026-06-19
- **版本**: v5.1.0
- **協議**: 君子協議
- **三色審計**: 🟢安全通過 / 🟡警告需審 / 🔴阻塞風險

---

*龍魂體系 © 2026 — 君子協議守護*


---

## 附录：龍魂协议与路由来源

本技能收录了来自 `/Users/zuimeidedeyihan/Downloads/Kimi_Agent_龍魂协议与路由` 的素材：

- **内容**：`deploy_longhun_kunpeng.sh`、`docker-compose.kunpeng.yml`、`創新引擎_鯤鵬補丁.md`、`鯤鵬服務器硬件對接.md`
- **中央整合 DNA**：`#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-PROTOCOL-ROUTE-INTEGRATION-v1.0`
- **处理方式**：保留原始文件作为 `references/龍魂协议与路由/`，嵌入 DNA 追溯链，与 `longhun-cloud-deploy` 部署能力联动。

---

## 附录：龍魂待整理来源

本技能收录了来自 `/Users/zuimeidedeyihan/龍魂待整理` 的素材：

- **内容**：06-工具脚本（长恨888网站搭建示例）
- **中央整合 DNA**：`#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-ARCHIVE-INTEGRATION-v1.0`
- **处理方式**：保留原始文件作为 references / examples / scripts，嵌入 DNA 追溯链，与现有能力联动。
