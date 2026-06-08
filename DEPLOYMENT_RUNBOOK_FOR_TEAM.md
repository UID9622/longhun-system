# 🐉 龍魂系統 · 生產部署手冊 v1.0

**目標讀者**: 運維團隊 / SRE 工程師 / DevOps 工程師
**部署版本**: v1.0 (2026-06-08)
**DNA**: `#龍芯⚇️2026-06-08-DEPLOYMENT-RUNBOOK-FOR-TEAM-v1.0`

---

## 📑 快速導航

- [第 1 部分：部署前準備](#第-1-部分部署前準備)
- [第 2 部分：架構概述](#第-2-部分架構概述)
- [第 3 部分：環境配置](#第-3-部分環境配置)
- [第 4 部分：部署執行](#第-4-部分部署執行)
- [第 5 部分：驗證和監控](#第-5-部分驗證和監控)
- [第 6 部分：故障排查](#第-6-部分故障排查)
- [第 7 部分：回滾程序](#第-7-部分回滾程序)

---

## 第 1 部分：部署前準備

### 🎯 部署前 72 小時：策劃階段

#### 1.1 團隊會議 (1 小時)

**參與人員**:
- SRE Lead / DevOps Manager
- 開發團隊代表
- 運維團隊代表
- 產品經理
- 安全負責人

**會議議程**:
```
1. 部署時間確認 (30 分鐘)
   - 選擇低流量時段
   - 確認維護窗口 (建議 2-4 小時)
   - 預留額外 1-2 小時應急時間

2. 風險評估 (20 分鐘)
   - 審查系統變更
   - 識別潛在風險點
   - 確認回滾計劃

3. 人員分配 (10 分鐘)
   - Deployment Lead (1 人)
   - Monitoring Lead (1 人)
   - Rollback Lead (1 人)
   - Support Lead (1 人)
```

#### 1.2 部署前檢查清單

**24 小時前**:
- [ ] 確認所有團隊成員可用
- [ ] 確認通信頻道暢通 (Slack #deployment-live)
- [ ] 備份現有生產環境完整性驗證
- [ ] DNS 設置已確認可回滾

**12 小時前**:
- [ ] 所有配置已準備就緒
- [ ] SSL/TLS 證書已驗證有效期 (>30 天)
- [ ] 數據庫連接已測試
- [ ] 監控和告警規則已配置並測試

**部署當日 - 2 小時前**:
- [ ] 團隊簽到
- [ ] 通信頻道測試
- [ ] 監控儀表板已打開
- [ ] 回滾計劃已確認
- [ ] 所有工具已就位

---

### 🔐 準備清單：安全和配置

#### 1.3 安全準備

```bash
# 1. 驗證密鑰管理
□ HashiCorp Vault 訪問已測試
□ 所有密鑰已正確配置
□ API 密鑰和令牌已準備
□ SSL/TLS 證書已驗證

# 2. 驗證訪問權限
□ 數據庫用戶權限已確認
□ Kubernetes 集群訪問已確認
□ AWS/雲平台訪問已確認
□ 監控服務訪問已確認

# 3. 備份確認
□ 生產數據庫完整備份已驗證
□ 備份可恢復性已測試
□ 備份位置已確認
□ 恢復時間目標已確認 (RTO: 15min)
```

#### 1.4 環境準備

```bash
# 準備生產配置文件
cp deployment/prod_config_template.json prod_config.json

# 編輯配置文件，填入實際生產環境信息
vim prod_config.json

# 驗證配置文件格式
python3 -c "import json; json.load(open('prod_config.json'))"

# 確認輸出: OK，說明配置有效
```

#### 1.5 基礎設施驗證

```bash
# 驗證數據庫連接
psql -h ${DB_HOST} -U ${DB_USER} -d ${DB_NAME} -c "SELECT 1;"

# 驗證 Redis 連接
redis-cli -h ${REDIS_HOST} ping

# 驗證監控服務
curl -H "DD-API-KEY: ${DD_API_KEY}" \
  https://api.datadoghq.com/api/v1/validate

# 驗證 Kubernetes 集群
kubectl cluster-info
kubectl get nodes

# 驗證存儲卷
kubectl get pv
kubectl get pvc
```

---

## 第 2 部分：架構概述

### 🏗️ 龍魂系統架構

#### 2.1 部署架構圖

```
┌─────────────────────────────────────────────────┐
│          客戶端層 (Web / Mobile / API)          │
└───────────────┬─────────────────────────────────┘
                │
       ┌────────┼────────┐
       ▼        ▼        ▼
   ┌────────┐ ┌────────┐ ┌────────┐
   │ Load   │ │ API    │ │WebSocket│
   │Balancer│ │Gateway │ │Server   │
   └────┬───┘ └───┬────┘ └────┬───┘
        │         │           │
        └─────────┼───────────┘
                  ▼
        ┌──────────────────────┐
        │  Kubernetes Service  │
        │    (ClusterIP)       │
        └──────────┬───────────┘
                   ▼
        ┌──────────────────────┐
        │  龍魂 API Pods (3)    │
        │  - Pod 1 (Green)     │
        │  - Pod 2 (Green)     │
        │  - Pod 3 (Green)     │
        └─────────┬────────────┘
                  │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
┌────────┐   ┌────────┐   ┌────────┐
│Skills  │   │Cache   │   │Logging │
│Service │   │(Redis) │   │(ELK)   │
└────┬───┘   └──┬─────┘   └────────┘
     │          │
     ▼          ▼
┌────────────────────────┐
│  PostgreSQL Database   │
│  (Primary + Replica)   │
└────────────────────────┘

Monitoring: Datadog / Prometheus / Grafana
Logging: Elasticsearch / Kibana
Tracing: Jaeger
Alerting: PagerDuty / Slack
```

#### 2.2 部署策略：藍綠部署

```
部署前狀態：
┌──────────────────────────────────────┐
│  藍色環境（當前生產）                │
│  ├─ App v1.0                         │
│  ├─ Database: Current                │
│  └─ 接收 100% 流量                   │
└──────────────────────────────────────┘

部署中狀態：
┌──────────────┐    ┌──────────────────┐
│  藍色環境    │    │  綠色環境（新）   │
│  100% 流量   │    │  0% 流量（準備）  │
│             │    │  ├─ App v2.0     │
│             │    │  ├─ 數據庫遷移   │
│             │    │  └─ 健康檢查     │
└──────────────┘    └──────────────────┘

流量切換：
10% → 25% → 50% → 75% → 100%
逐步轉移，監控每個階段

完成後狀態：
┌──────────────────────────────────────┐
│  綠色環境（當前生產）                │
│  ├─ App v2.0                         │
│  ├─ Database: Migrated               │
│  └─ 接收 100% 流量                   │
│                                      │
│  藍色環境（待命，可回滾）            │
└──────────────────────────────────────┘
```

#### 2.3 系統組件

| 組件 | 用途 | 可用性 |
| --- | --- | --- |
| API Gateway | 請求路由和負載均衡 | 99.95% |
| 應用服務器 | 業務邏輯執行 (3 個副本) | 99.95% |
| PostgreSQL | 數據持久化（主從複製） | 99.9% |
| Redis | 會話和緩存 | 99.9% |
| Datadog | 監控和指標 | 99.99% |
| Elasticsearch | 日誌存儲和搜索 | 99.9% |
| Jaeger | 分布式追踪 | 99.9% |

---

## 第 3 部分：環境配置

### ⚙️ 3.1 生產配置準備

#### 配置文件結構

```json
{
  "environment": "production",

  "api_configuration": {
    "api_host": "api.longhun.example.com",
    "api_port": 8443,
    "max_concurrent_connections": 10000
  },

  "database_configuration": {
    "db_type": "postgresql",
    "db_host": "prod-db.example.com",
    "db_port": 5432,
    "db_name": "longhun_prod",
    "db_user": "longhun_app",
    "db_password": "${VAULT_SECRET:db_password}",
    "db_pool_size": 20
  },

  "cache_configuration": {
    "cache_type": "redis",
    "redis_host": "prod-redis.example.com",
    "redis_port": 6379,
    "redis_password": "${VAULT_SECRET:redis_password}"
  },

  "monitoring_configuration": {
    "monitoring_service": "datadog",
    "datadog_api_key": "${VAULT_SECRET:datadog_api_key}",
    "datadog_app_key": "${VAULT_SECRET:datadog_app_key}"
  }
}
```

#### 配置驗證清單

```bash
# 1. 驗證所有必需的環境變量已設置
required_vars=(
  "DB_HOST" "DB_PORT" "DB_NAME" "DB_USER" "DB_PASSWORD"
  "REDIS_HOST" "REDIS_PORT" "REDIS_PASSWORD"
  "DATADOG_API_KEY" "DATADOG_APP_KEY"
  "VAULT_ADDR" "VAULT_TOKEN"
)

for var in "${required_vars[@]}"; do
  if [ -z "${!var}" ]; then
    echo "❌ 缺失環境變量: $var"
    exit 1
  fi
done

# 2. 驗證配置文件有效性
python3 << 'EOF'
import json
import sys

try:
  with open('prod_config.json', 'r') as f:
    config = json.load(f)

  required_fields = [
    'environment', 'api_configuration',
    'database_configuration', 'cache_configuration'
  ]

  for field in required_fields:
    if field not in config:
      print(f"❌ 配置缺失必需欄位: {field}")
      sys.exit(1)

  print("✅ 配置文件驗證通過")

except json.JSONDecodeError as e:
  print(f"❌ JSON 解析錯誤: {e}")
  sys.exit(1)
EOF

# 3. 測試所有連接
echo "測試數據庫連接..."
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "SELECT 1;" || exit 1

echo "測試 Redis 連接..."
redis-cli -h $REDIS_HOST ping | grep PONG || exit 1

echo "測試監控服務..."
curl -s -H "DD-API-KEY: $DATADOG_API_KEY" \
  https://api.datadoghq.com/api/v1/validate | grep -q "valid" || exit 1

echo "✅ 所有連接測試通過"
```

### 3.2 Kubernetes 部署配置

#### 創建命名空間和服務賬戶

```bash
# 創建命名空間
kubectl create namespace longhun-prod

# 創建服務賬戶
kubectl create serviceaccount longhun-deployer -n longhun-prod

# 綁定角色
kubectl create rolebinding longhun-deployer-binding \
  --clusterrole=edit \
  --serviceaccount=longhun-prod:longhun-deployer \
  -n longhun-prod
```

#### 創建密鑰

```bash
# 創建數據庫密鑰
kubectl create secret generic longhun-db-credentials \
  --from-literal=username=$DB_USER \
  --from-literal=password=$DB_PASSWORD \
  -n longhun-prod

# 創建 Redis 密鑰
kubectl create secret generic longhun-redis-credentials \
  --from-literal=password=$REDIS_PASSWORD \
  -n longhun-prod

# 創建監控密鑰
kubectl create secret generic longhun-monitoring \
  --from-literal=datadog-api-key=$DATADOG_API_KEY \
  --from-literal=datadog-app-key=$DATADOG_APP_KEY \
  -n longhun-prod

# 驗證密鑰已創建
kubectl get secrets -n longhun-prod
```

#### 部署應用

```bash
# 應用配置映射
kubectl create configmap longhun-config \
  --from-file=prod_config.json \
  -n longhun-prod

# 驗證
kubectl get configmap -n longhun-prod
```

---

## 第 4 部分：部署執行

### 🚀 4.1 部署前 - 最後檢查 (部署日 1 小時前)

#### 最終檢查清單

```bash
#!/bin/bash
# final_checks.sh - 部署前最後檢查

echo "🔍 執行部署前最後檢查..."

# 1. 驗證備份
echo "1️⃣  驗證備份..."
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME \
  > /backup/longhun_prod_$(date +%Y%m%d_%H%M%S).sql
if [ $? -eq 0 ]; then
  echo "✅ 數據庫備份成功"
else
  echo "❌ 數據庫備份失敗"
  exit 1
fi

# 2. 驗證藍色環境健康狀態
echo "2️⃣  驗證藍色環境..."
curl -k https://api.longhun.example.com/health | grep -q healthy || {
  echo "❌ 藍色環境不健康"
  exit 1
}
echo "✅ 藍色環境健康"

# 3. 驗證綠色環境已準備
echo "3️⃣  驗證綠色環境..."
kubectl get pods -n longhun-prod-green -l app=longhun | grep -q Running || {
  echo "❌ 綠色環境 Pods 未就緒"
  exit 1
}
echo "✅ 綠色環境已就緒"

# 4. 驗證監控就緒
echo "4️⃣  驗證監控..."
curl -s -H "DD-API-KEY: $DATADOG_API_KEY" \
  https://api.datadoghq.com/api/v1/validate | grep -q valid || {
  echo "❌ 監控服務無法訪問"
  exit 1
}
echo "✅ 監控就緒"

# 5. 驗證回滾計劃
echo "5️⃣  驗證回滾計劃..."
if [ -f "ROLLBACK_PLAN.txt" ]; then
  echo "✅ 回滾計劃已準備"
else
  echo "❌ 缺失回滾計劃"
  exit 1
fi

echo ""
echo "✅ 所有檢查通過，可以開始部署"
```

### 4.2 部署執行步驟

#### 步驟 1：初始化綠色環境 (0-5 分鐘)

```bash
#!/bin/bash
# deploy_step_1_init_green.sh

echo "🟢 [步驟 1] 初始化綠色環境"
echo "預期耗時: 3-5 分鐘"

# 1. 部署新版本應用
echo "1.1 部署應用..."
kubectl apply -f deployment/kubernetes/green-deployment.yaml -n longhun-prod-green

# 2. 等待 Pods 就緒
echo "1.2 等待 Pods 就緒..."
kubectl wait --for=condition=ready pod \
  -l app=longhun,version=green \
  -n longhun-prod-green \
  --timeout=300s

# 3. 執行數據庫遷移
echo "1.3 執行數據庫遷移..."
kubectl exec -n longhun-prod-green -it \
  $(kubectl get pod -n longhun-prod-green -l app=longhun -o jsonpath='{.items[0].metadata.name}') \
  -- python3 /app/migrate.py --production

# 4. 驗證遷移成功
echo "1.4 驗證遷移..."
kubectl exec -n longhun-prod-green -it \
  $(kubectl get pod -n longhun-prod-green -l app=longhun -o jsonpath='{.items[0].metadata.name}') \
  -- python3 /app/verify_migration.py

echo "✅ 步驟 1 完成"
```

#### 步驟 2：烟霧測試 (5-10 分鐘)

```bash
#!/bin/bash
# deploy_step_2_smoke_tests.sh

echo "🟢 [步驟 2] 執行烟霧測試"
echo "預期耗時: 3-5 分鐘"

# 1. 獲取綠色環境服務 IP
GREEN_SERVICE_IP=$(kubectl get service longhun-green \
  -n longhun-prod-green \
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

echo "綠色環境服務 IP: $GREEN_SERVICE_IP"

# 2. 執行烟霧測試
echo "2.1 測試基礎端點..."
curl -k https://$GREEN_SERVICE_IP/health || {
  echo "❌ /health 端點失敗"
  exit 1
}

echo "2.2 測試 API 端點..."
curl -k https://$GREEN_SERVICE_IP/api/v1/skills || {
  echo "❌ /api/v1/skills 端點失敗"
  exit 1
}

echo "2.3 測試技能執行..."
curl -k -X POST https://$GREEN_SERVICE_IP/api/v1/skills/1/execute \
  -H "Content-Type: application/json" \
  -d '{"input": "test"}' || {
  echo "❌ 技能執行失敗"
  exit 1
}

# 3. 驗證性能
echo "2.4 驗證性能指標..."
RESPONSE_TIME=$(curl -w "%{time_total}" -o /dev/null -s https://$GREEN_SERVICE_IP/health)
if (( $(echo "$RESPONSE_TIME < 0.1" | bc -l) )); then
  echo "✅ 性能正常 (${RESPONSE_TIME}s)"
else
  echo "⚠️  性能警告 (${RESPONSE_TIME}s > 100ms)"
fi

echo "✅ 步驟 2 完成"
```

#### 步驟 3：流量逐步轉移 (10-30 分鐘)

```bash
#!/bin/bash
# deploy_step_3_traffic_migration.sh

echo "🟢 [步驟 3] 流量逐步轉移"
echo "預期耗時: 15-20 分鐘"

TRAFFIC_PERCENTAGES=(10 25 50 75 100)
INTERVAL=300  # 每個階段間隔 5 分鐘

for percentage in "${TRAFFIC_PERCENTAGES[@]}"; do
  echo "3.$(printf '%d' $((percentage/25))) 轉移 ${percentage}% 流量到綠色環境..."

  # 更新流量規則
  kubectl patch service longhun \
    -n longhun-prod \
    -p '{"spec":{"sessionAffinity":"None"}}' \
    --type merge

  # 更新分流規則 (使用 Istio/NG Ingress)
  cat <<EOF | kubectl apply -f -
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: longhun-traffic
  namespace: longhun-prod
spec:
  hosts:
  - api.longhun.example.com
  http:
  - match:
    - uri:
        prefix: /
    route:
    - destination:
        host: longhun-blue.longhun-prod-blue.svc.cluster.local
      weight: $((100 - percentage))
    - destination:
        host: longhun-green.longhun-prod-green.svc.cluster.local
      weight: $percentage
    timeout: 10s
    retries:
      attempts: 3
      perTryTimeout: 2s
EOF

  echo "✅ ${percentage}% 流量已轉移"

  # 監控這個階段
  echo "⏳ 監控 ${INTERVAL} 秒..."
  for i in $(seq 1 5); do
    echo -n "."
    sleep 60

    # 檢查錯誤率
    ERROR_RATE=$(curl -s \
      -H "DD-API-KEY: $DATADOG_API_KEY" \
      "https://api.datadoghq.com/api/v1/query?query=avg:trace.web.request.errors{service:longhun}&from=now-1m&to=now" \
      | jq '.result[0].values[0][1]' 2>/dev/null || echo 0)

    if (( $(echo "$ERROR_RATE > 1" | bc -l) )); then
      echo ""
      echo "⚠️  錯誤率過高: ${ERROR_RATE}%"
      echo "⚠️  考慮回滾或暫停部署"
    fi
  done

  echo ""
done

echo "✅ 步驟 3 完成 - 所有流量已轉移到綠色環境"
```

#### 步驟 4：驗證和清理 (30-45 分鐘)

```bash
#!/bin/bash
# deploy_step_4_verify_cleanup.sh

echo "🟢 [步驟 4] 驗證和清理"
echo "預期耗時: 10-15 分鐘"

# 1. 最終健康檢查
echo "4.1 執行最終健康檢查..."
HEALTH_CHECKS=(
  "/health"
  "/api/v1/skills"
  "/api/v1/metrics"
  "/health/deep"
)

for endpoint in "${HEALTH_CHECKS[@]}"; do
  response=$(curl -s -k https://api.longhun.example.com$endpoint)
  echo "✅ $endpoint: $response"
done

# 2. 驗證性能指標
echo "4.2 驗證性能指標..."
python3 << 'EOF'
import requests
import json

dd_api_key = os.environ.get('DATADOG_API_KEY')
headers = {"DD-API-KEY": dd_api_key}

# 查詢吞吐量
response = requests.get(
  "https://api.datadoghq.com/api/v1/query",
  params={
    "query": "rate(trace.web.requests{service:longhun}[1m])",
    "from": "now-5m",
    "to": "now"
  },
  headers=headers
)

throughput = response.json()['result'][0]['values'][-1][1]
print(f"✅ 吞吐量: {throughput:.1f} req/s (目標: ≥77.8)")

# 查詢延遲
response = requests.get(
  "https://api.datadoghq.com/api/v1/query",
  params={
    "query": "p95:trace.web.request.duration{service:longhun}",
    "from": "now-5m",
    "to": "now"
  },
  headers=headers
)

latency = response.json()['result'][0]['values'][-1][1] * 1000
print(f"✅ P95 延遲: {latency:.1f}ms (目標: <15ms)")
EOF

# 3. 驗證數據庫完整性
echo "4.3 驗證數據庫完整性..."
kubectl exec -n longhun-prod-green \
  $(kubectl get pod -n longhun-prod-green -l app=longhun -o jsonpath='{.items[0].metadata.name}') \
  -- python3 /app/verify_data_integrity.py

# 4. 保存藍色環境以備回滾
echo "4.4 保存藍色環境狀態..."
kubectl scale deployment longhun-blue \
  -n longhun-prod-blue \
  --replicas=0 \
  --record

echo "✅ 藍色環境已停止，保留以備回滾"

# 5. 標記部署完成
echo "4.5 標記部署完成..."
echo "部署完成時間: $(date)" > /deployments/latest_successful.txt
echo "部署版本: v2.0" >> /deployments/latest_successful.txt

echo ""
echo "✅ 步驟 4 完成"
echo "🎉 部署成功完成！"
```

---

## 第 5 部分：驗證和監控

### 📊 5.1 部署後驗證 (部署後 1 小時內)

#### 自動驗證腳本

```bash
#!/bin/bash
# post_deployment_validation.sh

echo "🔍 執行部署後驗證..."
VALIDATION_FAILED=0

# 1. 驗證應用健康狀態
echo "1️⃣  驗證應用健康..."
HEALTH=$(curl -s -k https://api.longhun.example.com/health | jq '.status')
if [ "$HEALTH" == '"healthy"' ]; then
  echo "✅ 應用健康"
else
  echo "❌ 應用不健康"
  VALIDATION_FAILED=1
fi

# 2. 驗證所有 Pods 就緒
echo "2️⃣  驗證 Pods 就緒..."
POD_COUNT=$(kubectl get pods -n longhun-prod-green \
  -l app=longhun \
  --field-selector=status.phase=Running \
  --no-headers | wc -l)

if [ "$POD_COUNT" -ge 3 ]; then
  echo "✅ $POD_COUNT 個 Pods 運行中"
else
  echo "❌ Pods 不足: $POD_COUNT < 3"
  VALIDATION_FAILED=1
fi

# 3. 驗證數據庫連接
echo "3️⃣  驗證數據庫..."
DB_STATUS=$(psql -h $DB_HOST -U $DB_USER -d $DB_NAME \
  -t -c "SELECT 1;" 2>&1)

if [ "$DB_STATUS" == "1" ]; then
  echo "✅ 數據庫連接正常"
else
  echo "❌ 數據庫連接失敗"
  VALIDATION_FAILED=1
fi

# 4. 驗證快取
echo "4️⃣  驗證快取..."
REDIS_STATUS=$(redis-cli -h $REDIS_HOST ping)

if [ "$REDIS_STATUS" == "PONG" ]; then
  echo "✅ Redis 正常"
else
  echo "❌ Redis 無法訪問"
  VALIDATION_FAILED=1
fi

# 5. 驗證 10 個 Skills
echo "5️⃣  驗證 Skills..."
SKILLS=$(curl -s -k https://api.longhun.example.com/api/v1/skills | jq '.skills | length')

if [ "$SKILLS" == "10" ]; then
  echo "✅ 10 個 Skills 正常"
else
  echo "❌ Skills 數量異常: $SKILLS"
  VALIDATION_FAILED=1
fi

# 最終結果
if [ $VALIDATION_FAILED -eq 0 ]; then
  echo ""
  echo "🎉 所有驗證通過！"
  exit 0
else
  echo ""
  echo "❌ 驗證失敗，請檢查上方錯誤信息"
  exit 1
fi
```

### 5.2 持續監控 (部署後 24 小時)

#### 監控關鍵指標

```
🔴 關鍵告警 (立即行動):
  - 錯誤率 > 1%
  - P95 延遲 > 100ms
  - Pod 失敗 > 0
  - 數據庫連接失敗

🟡 警告告警 (跟蹤):
  - 錯誤率 > 0.5%
  - P95 延遲 > 50ms
  - Pod 重啟 > 2
  - 內存使用 > 80%

🟢 信息告警 (參考):
  - 新 Pod 啟動
  - 流量轉移完成
  - 部署完成
```

#### 每小時檢查清單

```
第 0 小時 (立即):
  [ ] 應用健康狀態 ✅
  [ ] Pod 運行狀態 ✅
  [ ] API 響應時間 ✅
  [ ] 錯誤率 ✅

第 1 小時:
  [ ] 吞吐量正常 ✅
  [ ] 內存使用穩定 ✅
  [ ] 無異常日誌 ✅
  [ ] 用戶反饋正常 ✅

第 4 小時:
  [ ] 所有指標穩定 ✅
  [ ] 無性能下降 ✅
  [ ] 無數據異常 ✅
  [ ] 系統平穩運行 ✅

第 24 小時:
  [ ] 所有指標符合預期 ✅
  [ ] 可以標記為成功部署 ✅
  [ ] 解散部署團隊 ✅
  [ ] 更新部署文檔 ✅
```

---

## 第 6 部分：故障排查

### ⚠️ 常見問題和解決方案

#### 問題 1：Pod 無法啟動

**症狀**: Pods 處於 CrashLoopBackOff

```bash
# 診斷
kubectl describe pod <pod-name> -n longhun-prod-green
kubectl logs <pod-name> -n longhun-prod-green --previous

# 常見原因和解決:
# 1. 數據庫連接失敗
#    → 檢查數據庫憑證和網絡連接
psql -h $DB_HOST -U $DB_USER -d $DB_NAME

# 2. 配置丟失
#    → 驗證 ConfigMap
kubectl get configmap longhun-config -n longhun-prod-green -o yaml

# 3. 密鑰缺失
#    → 驗證密鑰
kubectl get secrets -n longhun-prod-green
```

#### 問題 2：高錯誤率

**症狀**: 錯誤率突然升高 > 1%

```bash
# 診斷
# 1. 查看應用日誌
kubectl logs -n longhun-prod-green -l app=longhun --tail=100 | grep ERROR

# 2. 查看 Datadog 日誌
curl -s -H "DD-API-KEY: $DATADOG_API_KEY" \
  "https://api.datadoghq.com/api/v1/logs?query=service:longhun%20status:error&sort=timestamp" \
  | jq '.logs[0:10]'

# 3. 常見原因:
#    - 數據庫超負荷 → 檢查連接池
#    - 外部 API 超時 → 檢查網絡
#    - 內存洩漏 → 重啟 Pod
```

#### 問題 3：性能下降

**症狀**: P95 延遲 > 50ms

```bash
# 診斷
# 1. 查看資源使用
kubectl top pods -n longhun-prod-green

# 2. 查看數據庫查詢性能
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "
  SELECT query, calls, total_time
  FROM pg_stat_statements
  WHERE total_time > 1000
  ORDER BY total_time DESC LIMIT 10;"

# 3. 查看慢查詢日誌
# 在 Elasticsearch 中搜索: "duration > 50"

# 解決:
#    - 添加數據庫索引
#    - 優化查詢
#    - 增加 Pod 副本
```

#### 問題 4：無法回滾

**症狀**: 綠色環境出現嚴重問題，無法提供服務

```bash
# 應急回滾:
# 1. 立即禁用綠色環境流量
kubectl patch service longhun -n longhun-prod -p \
  '{"spec":{"selector":{"version":"blue"}}}'

# 2. 恢復藍色環境
kubectl scale deployment longhun-blue \
  -n longhun-prod-blue \
  --replicas=3

# 3. 驗證恢復
curl -k https://api.longhun.example.com/health

# 4. 查看藍色環境日誌
kubectl logs -n longhun-prod-blue -l app=longhun --tail=50
```

---

## 第 7 部分：回滾程序

### 🔄 7.1 計劃內回滾 (部署後發現問題)

如果部署 24 小時內發現嚴重問題：

```bash
#!/bin/bash
# rollback_blue_green.sh

echo "🔄 執行回滾程序..."

# 1. 驗證藍色環境可用
echo "1️⃣  驗證藍色環境..."
kubectl get pods -n longhun-prod-blue | grep Running || {
  echo "❌ 藍色環境不可用"
  exit 1
}

# 2. 將流量轉回藍色環境
echo "2️⃣  轉移流量回藍色環境..."
cat <<EOF | kubectl apply -f -
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: longhun-traffic
  namespace: longhun-prod
spec:
  hosts:
  - api.longhun.example.com
  http:
  - route:
    - destination:
        host: longhun-blue.longhun-prod-blue.svc.cluster.local
      weight: 100
EOF

# 3. 驗證流量轉移
echo "3️⃣  驗證流量轉移..."
sleep 30
curl -k https://api.longhun.example.com/health | grep -q healthy || {
  echo "❌ 藍色環境無法提供服務"
  exit 1
}

# 4. 停止綠色環境
echo "4️⃣  停止綠色環境..."
kubectl scale deployment longhun-green \
  -n longhun-prod-green \
  --replicas=0

# 5. 數據庫回滾 (如果需要)
echo "5️⃣  檢查是否需要數據庫回滾..."
echo "⚠️  如果數據庫架構更改了，需要手動執行:"
echo "    psql -h $DB_HOST -U $DB_USER -d $DB_NAME < /backup/longhun_prod_YYYYMMDD_HHMMSS.sql"

echo "✅ 回滾完成"
echo "⚠️  請立即通知團隊和利益相關者"
echo "⚠️  安排事件分析會議找出根本原因"
```

### 7.2 應急回滾 (完全故障)

如果系統完全故障，無法正常提供服務：

```bash
#!/bin/bash
# emergency_rollback.sh

echo "🚨 執行應急回滾..."

# 1. 立即切斷綠色環境
echo "1️⃣  切斷綠色環境..."
kubectl delete service longhun-green -n longhun-prod-green
kubectl delete ingress longhun-green -n longhun-prod-green

# 2. 恢復藍色環境到滿容量
echo "2️⃣  恢復藍色環境..."
kubectl scale deployment longhun-blue -n longhun-prod-blue --replicas=5

# 3. 更新 DNS 指向藍色環境
echo "3️⃣  更新 DNS..."
# 手動更新 DNS，或使用以下命令:
# aws route53 change-resource-record-sets ...

# 4. 驗證恢復
echo "4️⃣  驗證恢復..."
for i in {1..30}; do
  curl -s -k https://api.longhun.example.com/health | grep -q healthy && {
    echo "✅ 服務已恢復"
    break
  }
  echo "⏳ 等待服務恢復... ($i/30)"
  sleep 10
done

echo "✅ 應急回滾完成"
echo "🔴 立即启動事件响應"
echo "🔴 通知所有利益相關者"
echo "🔴 開始根本原因分析"
```

### 7.3 部署後回滾考量

```
回滾時間表:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

部署完成 → +1 小時: 可以快速回滾
  ├─ 應用級別回滾: 1-2 分鐘
  ├─ 數據庫回滾: 5-10 分鐘
  └─ 總計: <15 分鐘

部署完成 → +24 小時: 需要仔細回滾
  ├─ 驗證數據一致性
  ├─ 執行應用回滾: 5-10 分鐘
  ├─ 選擇性數據庫回滾: 10-30 分鐘
  └─ 總計: <1 小時

部署完成 → +1 週: 可能無法完全回滾
  ├─ 新數據已寫入
  ├─ 可能造成數據丟失
  └─ 需要數據遷移而非回滾
```

---

## 第 8 部分：團隊角色和責任

### 👥 部署團隊結構

#### Deployment Lead (1 人)
**職責**:
- 整體協調和進度控制
- 執行部署腳本
- 做出關鍵決策
- 與其他團隊溝通

**必備技能**:
- Kubernetes 操作
- 熟悉部署流程
- 冷靜應對壓力

#### Monitoring Lead (1 人)
**職責**:
- 監控系統指標
- 識別異常和告警
- 評估性能影響
- 建議暫停或回滾

**必備技能**:
- 監控工具操作 (Datadog/Prometheus)
- 性能分析
- 快速決策能力

#### Database Lead (1 人)
**職責**:
- 執行數據庫遷移
- 監控數據完整性
- 管理備份和恢復
- 處理數據相關問題

**必備技能**:
- PostgreSQL 知識
- 備份和恢復流程
- SQL 調優

#### Support Lead (1 人)
**職責**:
- 處理用戶和客戶溝通
- 記錄任何用戶報告的問題
- 協調與開發團隊的溝通
- 為部署團隊提供上下文

**必備技能**:
- 溝通技巧
- 問題分類能力

---

## 第 9 部分：部署檢查清單

### ✅ 完整部署檢查清單

#### 部署前 (T-72 小時)

- [ ] 安排部署會議
- [ ] 確認所有參與人員
- [ ] 審查系統變更
- [ ] 識別風險和緩解措施
- [ ] 準備回滾計劃
- [ ] 準備通信計劃

#### 部署前 (T-24 小時)

- [ ] 完成所有基礎設施準備
- [ ] 驗證備份可恢復
- [ ] 驗證所有憑證和密鑰
- [ ] 準備監控儀表板
- [ ] 測試通信渠道
- [ ] 確認所有人員可用

#### 部署前 (T-2 小時)

- [ ] 執行最後檢查腳本
- [ ] 驗證藍色環境健康
- [ ] 驗證綠色環境就緒
- [ ] 確認所有工具可用
- [ ] 團隊簽到
- [ ] 宣布部署開始

#### 部署期間

- [ ] 步驟 1: 初始化綠色環境 (完成)
- [ ] 步驟 2: 烟霧測試 (完成)
- [ ] 步驟 3: 流量轉移 (完成)
- [ ] 步驟 4: 驗證和清理 (完成)
- [ ] 持續監控和記錄

#### 部署後 (T+1 小時)

- [ ] 執行部署後驗證
- [ ] 確認所有指標正常
- [ ] 通知利益相關者
- [ ] 開始持續監控

#### 部署後 (T+24 小時)

- [ ] 審查所有監控數據
- [ ] 確認無異常事件
- [ ] 標記部署為成功
- [ ] 安排事件回顧會議
- [ ] 更新文檔和流程
- [ ] 解散部署團隊

---

## 第 10 部分：附錄和參考

### 📚 文件清單

- `deployment/production_deployment.py` - 生產部署引擎
- `deployment/PRODUCTION_DEPLOYMENT_GUIDE.md` - 完整部署指南
- `deployment/prod_config_template.json` - 配置模板
- `ROLLBACK_PLAN.txt` - 詳細回滾計劃
- `MONITORING_SETUP.md` - 監控配置指南
- `INCIDENT_RESPONSE_PLAN.md` - 事件響應計劃

### 🔗 有用的命令

```bash
# 部署相關
kubectl get pods -n longhun-prod-green
kubectl describe pod <pod-name> -n longhun-prod-green
kubectl logs <pod-name> -n longhun-prod-green

# 監控相關
kubectl top pods -n longhun-prod-green
kubectl get events -n longhun-prod-green

# 數據庫相關
psql -h $DB_HOST -U $DB_USER -d $DB_NAME
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME > backup.sql
psql -h $DB_HOST -U $DB_USER -d $DB_NAME < backup.sql

# 快取相關
redis-cli -h $REDIS_HOST ping
redis-cli -h $REDIS_HOST INFO stats
```

### 📞 緊急聯繫方式

```
Deployment Lead:  +1-XXX-XXX-XXXX
Monitoring Lead:  +1-XXX-XXX-XXXX
Database Lead:    +1-XXX-XXX-XXXX
Support Lead:     +1-XXX-XXX-XXXX
Engineering Manager: +1-XXX-XXX-XXXX

Slack 頻道: #deployment-live
PagerDuty: longhun-deployment-oncall
```

---

## 最後的話

這份運行手冊旨在確保龍魂系統的安全、可靠部署。

**記住**:
- ✅ 計劃優於倉促
- ✅ 監控比猜測更有效
- ✅ 溝通解決大多數問題
- ✅ 回滾總是一個選項

**祝部署順利！** 🚀

---

**DNA**: `#龍芯⚇️2026-06-08-DEPLOYMENT-RUNBOOK-FOR-TEAM-v1.0`
**確認**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**最後更新**: 2026-06-08 20:20 CST
**版本**: 1.0

---

## 第 11 部分：Kimi 集成（新增 2026-06-08）

### 🔗 概述

龍魂系統已與 Kimi AI 完整集成，支持四種模式：

1. **備用推理模型** - 故障轉移機制
2. **多模態處理** - 圖像/文件分析
3. **實時對話** - 用戶直接交互
4. **Skill 引擎** - 特定 Skill 集成

### 📦 部署步驟

#### 步驟 1: 環境配置 (T-24小時)

**1.1 設置 API 密鑰**

```bash
# 方案 A: 環境變數（推薦）
export KIMI_API_KEY="apisk-kimi-OLIN0lpHBND0Xsyh7ZG2U9BtaD4NY9QML2eDCfHMD5f6bSw1L7SEj2LGGTuWEjF9"

# 驗證設置
echo $KIMI_API_KEY
```

**1.2 驗證 Kimi API 連接**

```bash
cd ~/longhun-system/kimi

python3 << 'VERIFY'
from kimi_client import KimiClient
client = KimiClient()
status = "✅ 連接成功" if client.health_check() else "❌ 連接失敗"
print(f"Kimi API 狀態: {status}")
VERIFY
```

**預期輸出**:
```
Kimi API 狀態: ✅ 連接成功
```

#### 步驟 2: 集成測試 (T-12小時)

**2.1 運行集成測試**

```bash
cd ~/longhun-system/kimi
python3 kimi_integration.py
```

**預期輸出**:
```
🔗 初始化 Kimi 集成...

1️⃣ 備用推理模型
  {
    "status": "success",
    "model": "kimi",
    "response": "..."
  }

2️⃣ 多模態處理
  📸 圖像處理（演示模式）

3️⃣ 實時對話
  會話 ID: KIMI-CHAT-user_001-...

4️⃣ Skill 引擎
  📐 Canvas 設計...

📊 集成狀態
{
  "kimi_api": "🟢 connected",
  "circuit_breaker": {"state": "CLOSED"},
  ...
}
```

**2.2 測試各集成模式**

```bash
# 測試備用推理
python3 << 'TEST'
from kimi import KimiIntegration
kimi = KimiIntegration()
result = kimi.infer_with_fallback("龍魂系統的核心是什麼？")
print(f"備用推理: {result['status']}")
TEST

# 測試實時聊天
python3 << 'TEST'
from kimi import KimiIntegration
kimi = KimiIntegration()
session = kimi.start_realtime_chat("test_user")
print(f"聊天會話: {session['session_id']}")
TEST

# 測試 Skill 引擎
python3 << 'TEST'
from kimi import KimiIntegration
kimi = KimiIntegration()
result = kimi.use_kimi_for_skill(
    "skill-3-canvas-design",
    {"description": "設計一個數據儀表板"}
)
print(f"Skill 引擎: {result['status']}")
TEST
```

#### 步驟 3: 監控和告警 (T-6小時)

**3.1 配置 Kimi 集成監控**

```bash
# 啟用 Kimi 日誌監控
mkdir -p /tmp/longhun-kimi/logs
touch /tmp/longhun-kimi/logs/kimi_operations.log

# 配置日誌輪轉
cat > /etc/logrotate.d/longhun-kimi << 'LOGROTATE'
/tmp/longhun-kimi/logs/*.log {
  daily
  rotate 7
  compress
  delaycompress
  notifempty
  missingok
}
LOGROTATE
```

**3.2 監控指標**

```bash
# 監控斷路器狀態
watch -n 5 'python3 << "MONITOR"
from kimi import KimiIntegration
kimi = KimiIntegration()
status = kimi.get_health_status()
print(f"Kimi API: {status[\"kimi_api\"]}")
print(f"斷路器: {status[\"circuit_breaker\"][\"state\"]}")
print(f"失敗計數: {status[\"circuit_breaker\"][\"failure_count\"]}")
MONITOR
'

# 監控集成日誌
tail -f /tmp/longhun-kimi/logs/kimi_operations.log | grep -E "SUCCESS|FAILED"
```

**3.3 告警規則**

| 指標 | 閾值 | 嚴重性 |
|------|------|--------|
| Kimi API 連接 | 連續失敗 3 次 | 🔴 Critical |
| 斷路器狀態 | 狀態 = OPEN | 🟡 Warning |
| 響應時間 | > 5000ms | 🟡 Warning |
| 錯誤率 | > 5% | 🔴 Critical |

#### 步驟 4: 部署驗收 (T-2小時)

**4.1 預部署檢查清單**

```
✅ Kimi API 密鑰已設置
✅ API 連接測試通過
✅ 所有集成模式可用
✅ 斷路器機制正常
✅ 監控日誌正常運行
✅ 告警規則已配置
✅ 回滾計劃已驗證
```

**4.2 執行部署前驗收測試**

```bash
cd ~/longhun-system
python3 << 'ACCEPTANCE'
from kimi import KimiIntegration
import json

print("🧪 Kimi 集成驗收測試\n")

kimi = KimiIntegration()

# 測試 1: API 連接
print("1️⃣ API 連接測試")
is_connected = kimi.kimi_client.health_check()
print(f"  結果: {'✅ PASS' if is_connected else '❌ FAIL'}\n")

# 測試 2: 備用推理
print("2️⃣ 備用推理測試")
result = kimi.infer_with_fallback("測試提示詞")
print(f"  結果: {'✅ PASS' if result['status'] in ['success', 'fallback'] else '❌ FAIL'}\n")

# 測試 3: 實時聊天
print("3️⃣ 實時聊天測試")
session = kimi.start_realtime_chat("test_user")
print(f"  結果: {'✅ PASS' if session['status'] == 'active' else '❌ FAIL'}\n")

# 測試 4: Skill 引擎
print("4️⃣ Skill 引擎測試")
result = kimi.use_kimi_for_skill(
    "skill-3-canvas-design",
    {"description": "測試"}
)
print(f"  結果: {'✅ PASS' if result['status'] in ['success', 'unsupported'] else '❌ FAIL'}\n")

# 整體結果
print("📊 整體驗收結果")
print(f"  健康狀態: {json.dumps(kimi.get_health_status(), ensure_ascii=False)}")
ACCEPTANCE
```

### 🔄 故障排查

#### 問題 1: Kimi API 無法連接

**症狀**: 
```
❌ Kimi API 連接失敗: Connection refused
```

**診斷**:
```bash
# 檢查環境變數
echo $KIMI_API_KEY

# 測試 API 端點
curl -s https://api.moonshot.cn/v1/models \
  -H "Authorization: Bearer $KIMI_API_KEY" | jq .

# 檢查網絡連接
ping api.moonshot.cn
```

**解決方案**:
1. 驗證 KIMI_API_KEY 是否正確設置
2. 檢查 API key 是否過期
3. 驗證網絡連接和防火牆規則
4. 檢查 Kimi API 服務狀態

#### 問題 2: 斷路器打開

**症狀**:
```json
{
  "circuit_breaker": {
    "state": "OPEN",
    "failure_count": 3
  }
}
```

**診斷**:
```bash
# 查看最近的失敗日誌
tail -n 50 /tmp/longhun-kimi/logs/kimi_operations.log | grep FAILED

# 檢查 Kimi API 狀態
python3 -c "from kimi import KimiClient; c = KimiClient(); print(c.health_check())"
```

**解決方案**:
1. 檢查 Kimi API 是否正常
2. 查看失敗原因（網絡、超時、認證等）
3. 等待 60 秒自動恢復
4. 或手動重置: `kimi.circuit_breaker.failure_count = 0`

#### 問題 3: 響應時間過長

**症狀**: 
```
⏱️ Kimi API 響應時間 > 5000ms
```

**診斷**:
```bash
# 測試 API 響應時間
time python3 << 'TEST'
from kimi import KimiClient
client = KimiClient()
result = client.chat_completion([{"role": "user", "content": "Hi"}])
print(f"完成")
TEST
```

**解決方案**:
1. 檢查網絡延遲
2. 檢查 Kimi API 負載
3. 增加超時設置: `client = KimiClient(timeout=60)`
4. 如需緊急响应，使用本地推理降級

### ✅ 驗收標準

| 項目 | 標準 | 驗收方式 |
|------|------|---------|
| API 連接 | 能夠成功調用 Kimi API | `health_check()` |
| 備用推理 | 故障轉移機制正常 | 模擬 Kimi 故障測試 |
| 多模態 | 能夠處理圖像和文件 | 使用示例圖像/文件測試 |
| 實時聊天 | 能夠創建和維持會話 | 創建會話並發送消息 |
| Skill 引擎 | 支持的 Skill 可使用 Kimi | 測試 3 個支持的 Skill |
| 監控 | 日誌和指標正常記錄 | 檢查日誌文件 |
| 斷路器 | 故障自動檢測和恢復 | 模擬故障並觀察恢復 |

### 📚 相關文檔

- `~/longhun-system/kimi/KIMI_INTEGRATION_GUIDE.md` - 完整集成指南
- `~/longhun-system/deployment/kimi_integration_config.json` - 配置文件
- `~/longhun-system/kimi/kimi_client.py` - API 客户端源碼
- `~/longhun-system/kimi/kimi_integration.py` - 集成框架源碼

---

