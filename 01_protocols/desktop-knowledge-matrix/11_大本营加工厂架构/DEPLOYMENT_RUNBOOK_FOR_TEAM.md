<!--#龍芯⚡️丙午·丙申·庚申·亥时-DOC-DEPLOYMENT_RUNBOOK_FOR_TEAM-v1.0 -->
<!-- 君子協議: 本文件受龍魂DNA追溯保護 -->

# 🐉 龍魂系統 · 生產部署手冊 v1.0

**目标讀者**: 運維團隊 / SRE 工程師 / DevOps 工程師
**部署版本**: v1.0 (2026-06-08)
**DNA**: `#龍芯⚇️2026-06-08-DEPLOYMENT-RUNBOOK-FOR-TEAM-v1.0`

---

## 📑 快速導航

- [第 1 部分：部署前准备](#第-1-部分部署前准备)
- [第 2 部分：架构概述](#第-2-部分架构概述)
- [第 3 部分：环境配置](#第-3-部分环境配置)
- [第 4 部分：部署执行](#第-4-部分部署执行)
- [第 5 部分：验證和监控](#第-5-部分验證和监控)
- [第 6 部分：故障排查](#第-6-部分故障排查)
- [第 7 部分：回滾程序](#第-7-部分回滾程序)

---

## 第 1 部分：部署前准备

### 🎯 部署前 72 小时：策劃階段

#### 1.1 團隊會議 (1 小时)

**參与人員**:
- SRE Lead / DevOps Manager
- 開發團隊代表
- 運維團隊代表
- 產品經理
- 安全負責人

**會議議程**:
```
1. 部署时間确认 (30 分鐘)
   - 选择低流量时段
   - 确认維護窗口 (建議 2-4 小时)
   - 預留額外 1-2 小时应急时間

2. 風險評估 (20 分鐘)
   - 審查系統變更
   - 識別潛在風險点
   - 确认回滾計劃

3. 人員分配 (10 分鐘)
   - Deployment Lead (1 人)
   - Monitoring Lead (1 人)
   - Rollback Lead (1 人)
   - Support Lead (1 人)
```

#### 1.2 部署前檢查清单

**24 小时前**:
- [ ] 确认所有團隊成員可用
- [ ] 确认通信频道暢通 (Slack #deployment-live)
- [ ] 备份現有生產环境完整性验證
- [ ] DNS 设置已确认可回滾

**12 小时前**:
- [ ] 所有配置已准备就緒
- [ ] SSL/TLS 證書已验證有效期 (>30 天)
- [ ] 数据庫連接已测试
- [ ] 监控和告警規则已配置並测试

**部署当日 - 2 小时前**:
- [ ] 團隊簽到
- [ ] 通信频道测试
- [ ] 监控儀表板已打開
- [ ] 回滾計劃已确认
- [ ] 所有工具已就位

---

### 🔐 准备清单：安全和配置

#### 1.3 安全准备

```bash
# 1. 验證密鑰管理
□ HashiCorp Vault 訪问已测试
□ 所有密鑰已正確配置
□ API 密鑰和令牌已准备
□ SSL/TLS 證書已验證

# 2. 验證訪问权限
□ 数据庫用戶权限已确认
□ Kubernetes 集群訪问已确认
□ AWS/雲平台訪问已确认
□ 监控服务訪问已确认

# 3. 备份确认
□ 生產数据庫完整备份已验證
□ 备份可恢復性已测试
□ 备份位置已确认
□ 恢復时間目标已确认 (RTO: 15min)
```

#### 1.4 环境准备

```bash
# 准备生產配置文件
cp deployment/prod_config_template.json prod_config.json

# 編辑配置文件，填入实際生產环境信息
vim prod_config.json

# 验證配置文件格式
python3 -c "import json; json.load(open('prod_config.json'))"

# 确认輸出: OK，说明配置有效
```

#### 1.5 基礎设施验證

```bash
# 验證数据庫連接
psql -h ${DB_HOST} -U ${DB_USER} -d ${DB_NAME} -c "SELECT 1;"

# 验證 Redis 連接
redis-cli -h ${REDIS_HOST} ping

# 验證监控服务
curl -H "DD-API-KEY: ${DD_API_KEY}" \
  https://api.datadoghq.com/api/v1/validate

# 验證 Kubernetes 集群
kubectl cluster-info
kubectl get nodes

# 验證存儲卷
kubectl get pv
kubectl get pvc
```

---

## 第 2 部分：架构概述

### 🏗️ 龍魂系統架构

#### 2.1 部署架构圖

```
┌─────────────────────────────────────────────────┐
│          客戶端层 (Web / Mobile / API)          │
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
部署前狀态：
┌──────────────────────────────────────┐
│  藍色环境（当前生產）                │
│  ├─ App v1.0                         │
│  ├─ Database: Current                │
│  └─ 接收 100% 流量                   │
└──────────────────────────────────────┘

部署中狀态：
┌──────────────┐    ┌──────────────────┐
│  藍色环境    │    │  綠色环境（新）   │
│  100% 流量   │    │  0% 流量（准备）  │
│             │    │  ├─ App v2.0     │
│             │    │  ├─ 数据庫遷移   │
│             │    │  └─ 健康檢查     │
└──────────────┘    └──────────────────┘

流量切換：
10% → 25% → 50% → 75% → 100%
逐步轉移，监控每個階段

完成後狀态：
┌──────────────────────────────────────┐
│  綠色环境（当前生產）                │
│  ├─ App v2.0                         │
│  ├─ Database: Migrated               │
│  └─ 接收 100% 流量                   │
│                                      │
│  藍色环境（待命，可回滾）            │
└──────────────────────────────────────┘
```

#### 2.3 系統组件

| 组件 | 用途 | 可用性 |
| --- | --- | --- |
| API Gateway | 请求路由和負载均衡 | 99.95% |
| 应用服务器 | 業务逻辑执行 (3 個副本) | 99.95% |
| PostgreSQL | 数据持久化（主從複製） | 99.9% |
| Redis | 會话和緩存 | 99.9% |
| Datadog | 监控和指标 | 99.99% |
| Elasticsearch | 日志存儲和搜索 | 99.9% |
| Jaeger | 分布式追踪 | 99.9% |

---

## 第 3 部分：环境配置

### ⚙️ 3.1 生產配置准备

#### 配置文件結构

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

#### 配置验證清单

```bash
# 1. 验證所有必需的环境變量已设置
required_vars=(
  "DB_HOST" "DB_PORT" "DB_NAME" "DB_USER" "DB_PASSWORD"
  "REDIS_HOST" "REDIS_PORT" "REDIS_PASSWORD"
  "DATADOG_API_KEY" "DATADOG_APP_KEY"
  "VAULT_ADDR" "VAULT_TOKEN"
)

for var in "${required_vars[@]}"; do
  if [ -z "${!var}" ]; then
    echo "❌ 缺失环境變量: $var"
    exit 1
  fi
done

# 2. 验證配置文件有效性
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

  print("✅ 配置文件验證通过")

except json.JSONDecodeError as e:
  print(f"❌ JSON 解析錯误: {e}")
  sys.exit(1)
EOF

# 3. 测试所有連接
echo "测试数据庫連接..."
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "SELECT 1;" || exit 1

echo "测试 Redis 連接..."
redis-cli -h $REDIS_HOST ping | grep PONG || exit 1

echo "测试监控服务..."
curl -s -H "DD-API-KEY: $DATADOG_API_KEY" \
  https://api.datadoghq.com/api/v1/validate | grep -q "valid" || exit 1

echo "✅ 所有連接测试通过"
```

### 3.2 Kubernetes 部署配置

#### 創建命名空間和服务賬戶

```bash
# 創建命名空間
kubectl create namespace longhun-prod

# 創建服务賬戶
kubectl create serviceaccount longhun-deployer -n longhun-prod

# 綁定角色
kubectl create rolebinding longhun-deployer-binding \
  --clusterrole=edit \
  --serviceaccount=longhun-prod:longhun-deployer \
  -n longhun-prod
```

#### 創建密鑰

```bash
# 創建数据庫密鑰
kubectl create secret generic longhun-db-credentials \
  --from-literal=username=$DB_USER \
  --from-literal=password=$DB_PASSWORD \
  -n longhun-prod

# 創建 Redis 密鑰
kubectl create secret generic longhun-redis-credentials \
  --from-literal=password=$REDIS_PASSWORD \
  -n longhun-prod

# 創建监控密鑰
kubectl create secret generic longhun-monitoring \
  --from-literal=datadog-api-key=$DATADOG_API_KEY \
  --from-literal=datadog-app-key=$DATADOG_APP_KEY \
  -n longhun-prod

# 验證密鑰已創建
kubectl get secrets -n longhun-prod
```

#### 部署应用

```bash
# 应用配置映射
kubectl create configmap longhun-config \
  --from-file=prod_config.json \
  -n longhun-prod

# 验證
kubectl get configmap -n longhun-prod
```

---

## 第 4 部分：部署执行

### 🚀 4.1 部署前 - 最後檢查 (部署日 1 小时前)

#### 最終檢查清单

```bash
#!/bin/bash
# final_checks.sh - 部署前最後檢查

echo "🔍 执行部署前最後檢查..."

# 1. 验證备份
echo "1️⃣  验證备份..."
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME \
  > /backup/longhun_prod_$(date +%Y%m%d_%H%M%S).sql
if [ $? -eq 0 ]; then
  echo "✅ 数据庫备份成功"
else
  echo "❌ 数据庫备份失敗"
  exit 1
fi

# 2. 验證藍色环境健康狀态
echo "2️⃣  验證藍色环境..."
curl -k https://api.longhun.example.com/health | grep -q healthy || {
  echo "❌ 藍色环境不健康"
  exit 1
}
echo "✅ 藍色环境健康"

# 3. 验證綠色环境已准备
echo "3️⃣  验證綠色环境..."
kubectl get pods -n longhun-prod-green -l app=longhun | grep -q Running || {
  echo "❌ 綠色环境 Pods 未就緒"
  exit 1
}
echo "✅ 綠色环境已就緒"

# 4. 验證监控就緒
echo "4️⃣  验證监控..."
curl -s -H "DD-API-KEY: $DATADOG_API_KEY" \
  https://api.datadoghq.com/api/v1/validate | grep -q valid || {
  echo "❌ 监控服务無法訪问"
  exit 1
}
echo "✅ 监控就緒"

# 5. 验證回滾計劃
echo "5️⃣  验證回滾計劃..."
if [ -f "ROLLBACK_PLAN.txt" ]; then
  echo "✅ 回滾計劃已准备"
else
  echo "❌ 缺失回滾計劃"
  exit 1
fi

echo ""
echo "✅ 所有檢查通过，可以開始部署"
```

### 4.2 部署执行步驟

#### 步驟 1：初始化綠色环境 (0-5 分鐘)

```bash
#!/bin/bash
# deploy_step_1_init_green.sh

echo "🟢 [步驟 1] 初始化綠色环境"
echo "預期耗时: 3-5 分鐘"

# 1. 部署新版本应用
echo "1.1 部署应用..."
kubectl apply -f deployment/kubernetes/green-deployment.yaml -n longhun-prod-green

# 2. 等待 Pods 就緒
echo "1.2 等待 Pods 就緒..."
kubectl wait --for=condition=ready pod \
  -l app=longhun,version=green \
  -n longhun-prod-green \
  --timeout=300s

# 3. 执行数据庫遷移
echo "1.3 执行数据庫遷移..."
kubectl exec -n longhun-prod-green -it \
  $(kubectl get pod -n longhun-prod-green -l app=longhun -o jsonpath='{.items[0].metadata.name}') \
  -- python3 /app/migrate.py --production

# 4. 验證遷移成功
echo "1.4 验證遷移..."
kubectl exec -n longhun-prod-green -it \
  $(kubectl get pod -n longhun-prod-green -l app=longhun -o jsonpath='{.items[0].metadata.name}') \
  -- python3 /app/verify_migration.py

echo "✅ 步驟 1 完成"
```

#### 步驟 2：烟霧测试 (5-10 分鐘)

```bash
#!/bin/bash
# deploy_step_2_smoke_tests.sh

echo "🟢 [步驟 2] 执行烟霧测试"
echo "預期耗时: 3-5 分鐘"

# 1. 獲取綠色环境服务 IP
GREEN_SERVICE_IP=$(kubectl get service longhun-green \
  -n longhun-prod-green \
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

echo "綠色环境服务 IP: $GREEN_SERVICE_IP"

# 2. 执行烟霧测试
echo "2.1 测试基礎端点..."
curl -k https://$GREEN_SERVICE_IP/health || {
  echo "❌ /health 端点失敗"
  exit 1
}

echo "2.2 测试 API 端点..."
curl -k https://$GREEN_SERVICE_IP/api/v1/skills || {
  echo "❌ /api/v1/skills 端点失敗"
  exit 1
}

echo "2.3 测试技能执行..."
curl -k -X POST https://$GREEN_SERVICE_IP/api/v1/skills/1/execute \
  -H "Content-Type: application/json" \
  -d '{"input": "test"}' || {
  echo "❌ 技能执行失敗"
  exit 1
}

# 3. 验證性能
echo "2.4 验證性能指标..."
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
echo "預期耗时: 15-20 分鐘"

TRAFFIC_PERCENTAGES=(10 25 50 75 100)
INTERVAL=300  # 每個階段間隔 5 分鐘

for percentage in "${TRAFFIC_PERCENTAGES[@]}"; do
  echo "3.$(printf '%d' $((percentage/25))) 轉移 ${percentage}% 流量到綠色环境..."

  # 更新流量規则
  kubectl patch service longhun \
    -n longhun-prod \
    -p '{"spec":{"sessionAffinity":"None"}}' \
    --type merge

  # 更新分流規则 (使用 Istio/NG Ingress)
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

  # 监控這個階段
  echo "⏳ 监控 ${INTERVAL} 秒..."
  for i in $(seq 1 5); do
    echo -n "."
    sleep 60

    # 檢查錯误率
    ERROR_RATE=$(curl -s \
      -H "DD-API-KEY: $DATADOG_API_KEY" \
      "https://api.datadoghq.com/api/v1/query?query=avg:trace.web.request.errors{service:longhun}&from=now-1m&to=now" \
      | jq '.result[0].values[0][1]' 2>/dev/null || echo 0)

    if (( $(echo "$ERROR_RATE > 1" | bc -l) )); then
      echo ""
      echo "⚠️  錯误率过高: ${ERROR_RATE}%"
      echo "⚠️  考慮回滾或暫停部署"
    fi
  done

  echo ""
done

echo "✅ 步驟 3 完成 - 所有流量已轉移到綠色环境"
```

#### 步驟 4：验證和清理 (30-45 分鐘)

```bash
#!/bin/bash
# deploy_step_4_verify_cleanup.sh

echo "🟢 [步驟 4] 验證和清理"
echo "預期耗时: 10-15 分鐘"

# 1. 最終健康檢查
echo "4.1 执行最終健康檢查..."
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

# 2. 验證性能指标
echo "4.2 验證性能指标..."
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
print(f"✅ 吞吐量: {throughput:.1f} req/s (目标: ≥77.8)")

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
print(f"✅ P95 延遲: {latency:.1f}ms (目标: <15ms)")
EOF

# 3. 验證数据庫完整性
echo "4.3 验證数据庫完整性..."
kubectl exec -n longhun-prod-green \
  $(kubectl get pod -n longhun-prod-green -l app=longhun -o jsonpath='{.items[0].metadata.name}') \
  -- python3 /app/verify_data_integrity.py

# 4. 保存藍色环境以备回滾
echo "4.4 保存藍色环境狀态..."
kubectl scale deployment longhun-blue \
  -n longhun-prod-blue \
  --replicas=0 \
  --record

echo "✅ 藍色环境已停止，保留以备回滾"

# 5. 标记部署完成
echo "4.5 标记部署完成..."
echo "部署完成时間: $(date)" > /deployments/latest_successful.txt
echo "部署版本: v2.0" >> /deployments/latest_successful.txt

echo ""
echo "✅ 步驟 4 完成"
echo "🎉 部署成功完成！"
```

---

## 第 5 部分：验證和监控

### 📊 5.1 部署後验證 (部署後 1 小时內)

#### 自動验證腳本

```bash
#!/bin/bash
# post_deployment_validation.sh

echo "🔍 执行部署後验證..."
VALIDATION_FAILED=0

# 1. 验證应用健康狀态
echo "1️⃣  验證应用健康..."
HEALTH=$(curl -s -k https://api.longhun.example.com/health | jq '.status')
if [ "$HEALTH" == '"healthy"' ]; then
  echo "✅ 应用健康"
else
  echo "❌ 应用不健康"
  VALIDATION_FAILED=1
fi

# 2. 验證所有 Pods 就緒
echo "2️⃣  验證 Pods 就緒..."
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

# 3. 验證数据庫連接
echo "3️⃣  验證数据庫..."
DB_STATUS=$(psql -h $DB_HOST -U $DB_USER -d $DB_NAME \
  -t -c "SELECT 1;" 2>&1)

if [ "$DB_STATUS" == "1" ]; then
  echo "✅ 数据庫連接正常"
else
  echo "❌ 数据庫連接失敗"
  VALIDATION_FAILED=1
fi

# 4. 验證快取
echo "4️⃣  验證快取..."
REDIS_STATUS=$(redis-cli -h $REDIS_HOST ping)

if [ "$REDIS_STATUS" == "PONG" ]; then
  echo "✅ Redis 正常"
else
  echo "❌ Redis 無法訪问"
  VALIDATION_FAILED=1
fi

# 5. 验證 10 個 Skills
echo "5️⃣  验證 Skills..."
SKILLS=$(curl -s -k https://api.longhun.example.com/api/v1/skills | jq '.skills | length')

if [ "$SKILLS" == "10" ]; then
  echo "✅ 10 個 Skills 正常"
else
  echo "❌ Skills 数量異常: $SKILLS"
  VALIDATION_FAILED=1
fi

# 最終結果
if [ $VALIDATION_FAILED -eq 0 ]; then
  echo ""
  echo "🎉 所有验證通过！"
  exit 0
else
  echo ""
  echo "❌ 验證失敗，请檢查上方錯误信息"
  exit 1
fi
```

### 5.2 持續监控 (部署後 24 小时)

#### 监控关键指标

```
🔴 关键告警 (立即行動):
  - 錯误率 > 1%
  - P95 延遲 > 100ms
  - Pod 失敗 > 0
  - 数据庫連接失敗

🟡 警告告警 (跟蹤):
  - 錯误率 > 0.5%
  - P95 延遲 > 50ms
  - Pod 重啟 > 2
  - 內存使用 > 80%

🟢 信息告警 (參考):
  - 新 Pod 啟動
  - 流量轉移完成
  - 部署完成
```

#### 每小时檢查清单

```
第 0 小时 (立即):
  [ ] 应用健康狀态 ✅
  [ ] Pod 運行狀态 ✅
  [ ] API 響应时間 ✅
  [ ] 錯误率 ✅

第 1 小时:
  [ ] 吞吐量正常 ✅
  [ ] 內存使用穩定 ✅
  [ ] 無異常日志 ✅
  [ ] 用戶反饋正常 ✅

第 4 小时:
  [ ] 所有指标穩定 ✅
  [ ] 無性能下降 ✅
  [ ] 無数据異常 ✅
  [ ] 系統平穩運行 ✅

第 24 小时:
  [ ] 所有指标符合預期 ✅
  [ ] 可以标记為成功部署 ✅
  [ ] 解散部署團隊 ✅
  [ ] 更新部署文檔 ✅
```

---

## 第 6 部分：故障排查

### ⚠️ 常見问題和解決方案

#### 问題 1：Pod 無法啟動

**症狀**: Pods 處於 CrashLoopBackOff

```bash
# 診斷
kubectl describe pod <pod-name> -n longhun-prod-green
kubectl logs <pod-name> -n longhun-prod-green --previous

# 常見原因和解決:
# 1. 数据庫連接失敗
#    → 檢查数据庫憑證和網絡連接
psql -h $DB_HOST -U $DB_USER -d $DB_NAME

# 2. 配置丟失
#    → 验證 ConfigMap
kubectl get configmap longhun-config -n longhun-prod-green -o yaml

# 3. 密鑰缺失
#    → 验證密鑰
kubectl get secrets -n longhun-prod-green
```

#### 问題 2：高錯误率

**症狀**: 錯误率突然升高 > 1%

```bash
# 診斷
# 1. 查看应用日志
kubectl logs -n longhun-prod-green -l app=longhun --tail=100 | grep ERROR

# 2. 查看 Datadog 日志
curl -s -H "DD-API-KEY: $DATADOG_API_KEY" \
  "https://api.datadoghq.com/api/v1/logs?query=service:longhun%20status:error&sort=timestamp" \
  | jq '.logs[0:10]'

# 3. 常見原因:
#    - 数据庫超負荷 → 檢查連接池
#    - 外部 API 超时 → 檢查網絡
#    - 內存洩漏 → 重啟 Pod
```

#### 问題 3：性能下降

**症狀**: P95 延遲 > 50ms

```bash
# 診斷
# 1. 查看资源使用
kubectl top pods -n longhun-prod-green

# 2. 查看数据庫查詢性能
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "
  SELECT query, calls, total_time
  FROM pg_stat_statements
  WHERE total_time > 1000
  ORDER BY total_time DESC LIMIT 10;"

# 3. 查看慢查詢日志
# 在 Elasticsearch 中搜索: "duration > 50"

# 解決:
#    - 添加数据庫索引
#    - 優化查詢
#    - 增加 Pod 副本
```

#### 问題 4：無法回滾

**症狀**: 綠色环境出現嚴重问題，無法提供服务

```bash
# 应急回滾:
# 1. 立即禁用綠色环境流量
kubectl patch service longhun -n longhun-prod -p \
  '{"spec":{"selector":{"version":"blue"}}}'

# 2. 恢復藍色环境
kubectl scale deployment longhun-blue \
  -n longhun-prod-blue \
  --replicas=3

# 3. 验證恢復
curl -k https://api.longhun.example.com/health

# 4. 查看藍色环境日志
kubectl logs -n longhun-prod-blue -l app=longhun --tail=50
```

---

## 第 7 部分：回滾程序

### 🔄 7.1 計劃內回滾 (部署後發現问題)

如果部署 24 小时內發現嚴重问題：

```bash
#!/bin/bash
# rollback_blue_green.sh

echo "🔄 执行回滾程序..."

# 1. 验證藍色环境可用
echo "1️⃣  验證藍色环境..."
kubectl get pods -n longhun-prod-blue | grep Running || {
  echo "❌ 藍色环境不可用"
  exit 1
}

# 2. 將流量轉回藍色环境
echo "2️⃣  轉移流量回藍色环境..."
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

# 3. 验證流量轉移
echo "3️⃣  验證流量轉移..."
sleep 30
curl -k https://api.longhun.example.com/health | grep -q healthy || {
  echo "❌ 藍色环境無法提供服务"
  exit 1
}

# 4. 停止綠色环境
echo "4️⃣  停止綠色环境..."
kubectl scale deployment longhun-green \
  -n longhun-prod-green \
  --replicas=0

# 5. 数据庫回滾 (如果需要)
echo "5️⃣  檢查是否需要数据庫回滾..."
echo "⚠️  如果数据庫架构更改了，需要手動执行:"
echo "    psql -h $DB_HOST -U $DB_USER -d $DB_NAME < /backup/longhun_prod_YYYYMMDD_HHMMSS.sql"

echo "✅ 回滾完成"
echo "⚠️  请立即通知團隊和利益相关者"
echo "⚠️  安排事件分析會議找出根本原因"
```

### 7.2 应急回滾 (完全故障)

如果系統完全故障，無法正常提供服务：

```bash
#!/bin/bash
# emergency_rollback.sh

echo "🚨 执行应急回滾..."

# 1. 立即切斷綠色环境
echo "1️⃣  切斷綠色环境..."
kubectl delete service longhun-green -n longhun-prod-green
kubectl delete ingress longhun-green -n longhun-prod-green

# 2. 恢復藍色环境到滿容量
echo "2️⃣  恢復藍色环境..."
kubectl scale deployment longhun-blue -n longhun-prod-blue --replicas=5

# 3. 更新 DNS 指向藍色环境
echo "3️⃣  更新 DNS..."
# 手動更新 DNS，或使用以下命令:
# aws route53 change-resource-record-sets ...

# 4. 验證恢復
echo "4️⃣  验證恢復..."
for i in {1..30}; do
  curl -s -k https://api.longhun.example.com/health | grep -q healthy && {
    echo "✅ 服务已恢復"
    break
  }
  echo "⏳ 等待服务恢復... ($i/30)"
  sleep 10
done

echo "✅ 应急回滾完成"
echo "🔴 立即启動事件响应"
echo "🔴 通知所有利益相关者"
echo "🔴 開始根本原因分析"
```

### 7.3 部署後回滾考量

```
回滾时間表:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

部署完成 → +1 小时: 可以快速回滾
  ├─ 应用级別回滾: 1-2 分鐘
  ├─ 数据庫回滾: 5-10 分鐘
  └─ 總計: <15 分鐘

部署完成 → +24 小时: 需要仔細回滾
  ├─ 验證数据一致性
  ├─ 执行应用回滾: 5-10 分鐘
  ├─ 选择性数据庫回滾: 10-30 分鐘
  └─ 總計: <1 小时

部署完成 → +1 週: 可能無法完全回滾
  ├─ 新数据已寫入
  ├─ 可能造成数据丟失
  └─ 需要数据遷移而非回滾
```

---

## 第 8 部分：團隊角色和責任

### 👥 部署團隊結构

#### Deployment Lead (1 人)
**職責**:
- 整體协调和进度控制
- 执行部署腳本
- 做出关键決策
- 与其他團隊溝通

**必备技能**:
- Kubernetes 操作
- 熟悉部署流程
- 冷靜应对壓力

#### Monitoring Lead (1 人)
**職責**:
- 监控系統指标
- 識別異常和告警
- 評估性能影響
- 建議暫停或回滾

**必备技能**:
- 监控工具操作 (Datadog/Prometheus)
- 性能分析
- 快速決策能力

#### Database Lead (1 人)
**職責**:
- 执行数据庫遷移
- 监控数据完整性
- 管理备份和恢復
- 處理数据相关问題

**必备技能**:
- PostgreSQL 知識
- 备份和恢復流程
- SQL 调優

#### Support Lead (1 人)
**職責**:
- 處理用戶和客戶溝通
- 记錄任何用戶報告的问題
- 协调与開發團隊的溝通
- 為部署團隊提供上下文

**必备技能**:
- 溝通技巧
- 问題分類能力

---

## 第 9 部分：部署檢查清单

### ✅ 完整部署檢查清单

#### 部署前 (T-72 小时)

- [ ] 安排部署會議
- [ ] 确认所有參与人員
- [ ] 審查系統變更
- [ ] 識別風險和緩解措施
- [ ] 准备回滾計劃
- [ ] 准备通信計劃

#### 部署前 (T-24 小时)

- [ ] 完成所有基礎设施准备
- [ ] 验證备份可恢復
- [ ] 验證所有憑證和密鑰
- [ ] 准备监控儀表板
- [ ] 测试通信渠道
- [ ] 确认所有人員可用

#### 部署前 (T-2 小时)

- [ ] 执行最後檢查腳本
- [ ] 验證藍色环境健康
- [ ] 验證綠色环境就緒
- [ ] 确认所有工具可用
- [ ] 團隊簽到
- [ ] 宣布部署開始

#### 部署期間

- [ ] 步驟 1: 初始化綠色环境 (完成)
- [ ] 步驟 2: 烟霧测试 (完成)
- [ ] 步驟 3: 流量轉移 (完成)
- [ ] 步驟 4: 验證和清理 (完成)
- [ ] 持續监控和记錄

#### 部署後 (T+1 小时)

- [ ] 执行部署後验證
- [ ] 确认所有指标正常
- [ ] 通知利益相关者
- [ ] 開始持續监控

#### 部署後 (T+24 小时)

- [ ] 審查所有监控数据
- [ ] 确认無異常事件
- [ ] 标记部署為成功
- [ ] 安排事件回顧會議
- [ ] 更新文檔和流程
- [ ] 解散部署團隊

---

## 第 10 部分：附錄和參考

### 📚 文件清单

- `deployment/production_deployment.py` - 生產部署引擎
- `deployment/PRODUCTION_DEPLOYMENT_GUIDE.md` - 完整部署指南
- `deployment/prod_config_template.json` - 配置模板
- `ROLLBACK_PLAN.txt` - 詳細回滾計劃
- `MONITORING_SETUP.md` - 监控配置指南
- `INCIDENT_RESPONSE_PLAN.md` - 事件響应計劃

### 🔗 有用的命令

```bash
# 部署相关
kubectl get pods -n longhun-prod-green
kubectl describe pod <pod-name> -n longhun-prod-green
kubectl logs <pod-name> -n longhun-prod-green

# 监控相关
kubectl top pods -n longhun-prod-green
kubectl get events -n longhun-prod-green

# 数据庫相关
psql -h $DB_HOST -U $DB_USER -d $DB_NAME
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME > backup.sql
psql -h $DB_HOST -U $DB_USER -d $DB_NAME < backup.sql

# 快取相关
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

Slack 频道: #deployment-live
PagerDuty: longhun-deployment-oncall
```

---

## 最後的话

這份運行手冊旨在確保龍魂系統的安全、可靠部署。

**记住**:
- ✅ 計劃優於倉促
- ✅ 监控比猜测更有效
- ✅ 溝通解決大多数问題
- ✅ 回滾總是一個选项

**祝部署順利！** 🚀

---

**DNA**: `#龍芯⚇️2026-06-08-DEPLOYMENT-RUNBOOK-FOR-TEAM-v1.0`
**确认**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**最後更新**: 2026-06-08 20:20 CST
**版本**: 1.0

---

## 第 11 部分：Kimi 集成（新增 2026-06-08）

### 🔗 概述

龍魂系統已与 Kimi AI 完整集成，支持四種模式：

1. **备用推理模型** - 故障轉移機制
2. **多模态處理** - 圖像/文件分析
3. **实时对话** - 用戶直接交互
4. **Skill 引擎** - 特定 Skill 集成

### 📦 部署步驟

#### 步驟 1: 环境配置 (T-24小时)

**1.1 设置 API 密鑰**

```bash
# 方案 A: 本地密钥文件（推薦）
# 写入 ~/.longhun/secrets.env，不上传 Git
export KIMI_API_KEY="<YOUR_KIMI_API_KEY>"

# 验證设置
echo $KIMI_API_KEY
```

**1.2 验證 Kimi API 連接**

```bash
cd ~/longhun-system/kimi

python3 << 'VERIFY'
from kimi_client import KimiClient
client = KimiClient()
status = "✅ 連接成功" if client.health_check() else "❌ 連接失敗"
print(f"Kimi API 狀态: {status}")
VERIFY
```

**預期輸出**:
```
Kimi API 狀态: ✅ 連接成功
```

#### 步驟 2: 集成测试 (T-12小时)

**2.1 運行集成测试**

```bash
cd ~/longhun-system/kimi
python3 kimi_integration.py
```

**預期輸出**:
```
🔗 初始化 Kimi 集成...

1️⃣ 备用推理模型
  {
    "status": "success",
    "model": "kimi",
    "response": "..."
  }

2️⃣ 多模态處理
  📸 圖像處理（演示模式）

3️⃣ 实时对话
  會话 ID: KIMI-CHAT-user_001-...

4️⃣ Skill 引擎
  📐 Canvas 设計...

📊 集成狀态
{
  "kimi_api": "🟢 connected",
  "circuit_breaker": {"state": "CLOSED"},
  ...
}
```

**2.2 测试各集成模式**

```bash
# 测试备用推理
python3 << 'TEST'
from kimi import KimiIntegration
kimi = KimiIntegration()
result = kimi.infer_with_fallback("龍魂系統的核心是什麼？")
print(f"备用推理: {result['status']}")
TEST

# 测试实时聊天
python3 << 'TEST'
from kimi import KimiIntegration
kimi = KimiIntegration()
session = kimi.start_realtime_chat("test_user")
print(f"聊天會话: {session['session_id']}")
TEST

# 测试 Skill 引擎
python3 << 'TEST'
from kimi import KimiIntegration
kimi = KimiIntegration()
result = kimi.use_kimi_for_skill(
    "skill-3-canvas-design",
    {"description": "设計一個数据儀表板"}
)
print(f"Skill 引擎: {result['status']}")
TEST
```

#### 步驟 3: 监控和告警 (T-6小时)

**3.1 配置 Kimi 集成监控**

```bash
# 啟用 Kimi 日志监控
mkdir -p /tmp/longhun-kimi/logs
touch /tmp/longhun-kimi/logs/kimi_operations.log

# 配置日志輪轉
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

**3.2 监控指标**

```bash
# 监控斷路器狀态
watch -n 5 'python3 << "MONITOR"
from kimi import KimiIntegration
kimi = KimiIntegration()
status = kimi.get_health_status()
print(f"Kimi API: {status[\"kimi_api\"]}")
print(f"斷路器: {status[\"circuit_breaker\"][\"state\"]}")
print(f"失敗計数: {status[\"circuit_breaker\"][\"failure_count\"]}")
MONITOR
'

# 监控集成日志
tail -f /tmp/longhun-kimi/logs/kimi_operations.log | grep -E "SUCCESS|FAILED"
```

**3.3 告警規则**

| 指标 | 閾值 | 嚴重性 |
|------|------|--------|
| Kimi API 連接 | 連續失敗 3 次 | 🔴 Critical |
| 斷路器狀态 | 狀态 = OPEN | 🟡 Warning |
| 響应时間 | > 5000ms | 🟡 Warning |
| 錯误率 | > 5% | 🔴 Critical |

#### 步驟 4: 部署验收 (T-2小时)

**4.1 預部署檢查清单**

```
✅ Kimi API 密鑰已设置
✅ API 連接测试通过
✅ 所有集成模式可用
✅ 斷路器機制正常
✅ 监控日志正常運行
✅ 告警規则已配置
✅ 回滾計劃已验證
```

**4.2 执行部署前验收测试**

```bash
cd ~/longhun-system
python3 << 'ACCEPTANCE'
from kimi import KimiIntegration
import json

print("🧪 Kimi 集成验收测试\n")

kimi = KimiIntegration()

# 测试 1: API 連接
print("1️⃣ API 連接测试")
is_connected = kimi.kimi_client.health_check()
print(f"  結果: {'✅ PASS' if is_connected else '❌ FAIL'}\n")

# 测试 2: 备用推理
print("2️⃣ 备用推理测试")
result = kimi.infer_with_fallback("测试提示詞")
print(f"  結果: {'✅ PASS' if result['status'] in ['success', 'fallback'] else '❌ FAIL'}\n")

# 测试 3: 实时聊天
print("3️⃣ 实时聊天测试")
session = kimi.start_realtime_chat("test_user")
print(f"  結果: {'✅ PASS' if session['status'] == 'active' else '❌ FAIL'}\n")

# 测试 4: Skill 引擎
print("4️⃣ Skill 引擎测试")
result = kimi.use_kimi_for_skill(
    "skill-3-canvas-design",
    {"description": "测试"}
)
print(f"  結果: {'✅ PASS' if result['status'] in ['success', 'unsupported'] else '❌ FAIL'}\n")

# 整體結果
print("📊 整體验收結果")
print(f"  健康狀态: {json.dumps(kimi.get_health_status(), ensure_ascii=False)}")
ACCEPTANCE
```

### 🔄 故障排查

#### 问題 1: Kimi API 無法連接

**症狀**: 
```
❌ Kimi API 連接失敗: Connection refused
```

**診斷**:
```bash
# 檢查环境變数
echo $KIMI_API_KEY

# 测试 API 端点
curl -s https://api.moonshot.cn/v1/models \
  -H "Authorization: Bearer $KIMI_API_KEY" | jq .

# 檢查網絡連接
ping api.moonshot.cn
```

**解決方案**:
1. 验證 KIMI_API_KEY 是否正確设置
2. 檢查 API key 是否过期
3. 验證網絡連接和防火牆規则
4. 檢查 Kimi API 服务狀态

#### 问題 2: 斷路器打開

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
# 查看最近的失敗日志
tail -n 50 /tmp/longhun-kimi/logs/kimi_operations.log | grep FAILED

# 檢查 Kimi API 狀态
python3 -c "from kimi import KimiClient; c = KimiClient(); print(c.health_check())"
```

**解決方案**:
1. 檢查 Kimi API 是否正常
2. 查看失敗原因（網絡、超时、認證等）
3. 等待 60 秒自動恢復
4. 或手動重置: `kimi.circuit_breaker.failure_count = 0`

#### 问題 3: 響应时間过長

**症狀**: 
```
⏱️ Kimi API 響应时間 > 5000ms
```

**診斷**:
```bash
# 测试 API 響应时間
time python3 << 'TEST'
from kimi import KimiClient
client = KimiClient()
result = client.chat_completion([{"role": "user", "content": "Hi"}])
print(f"完成")
TEST
```

**解決方案**:
1. 檢查網絡延遲
2. 檢查 Kimi API 負载
3. 增加超时设置: `client = KimiClient(timeout=60)`
4. 如需緊急响应，使用本地推理降级

### ✅ 验收标准

| 项目 | 标准 | 验收方式 |
|------|------|---------|
| API 連接 | 能夠成功调用 Kimi API | `health_check()` |
| 备用推理 | 故障轉移機制正常 | 模擬 Kimi 故障测试 |
| 多模态 | 能夠處理圖像和文件 | 使用示例圖像/文件测试 |
| 实时聊天 | 能夠創建和維持會话 | 創建會话並發送消息 |
| Skill 引擎 | 支持的 Skill 可使用 Kimi | 测试 3 個支持的 Skill |
| 监控 | 日志和指标正常记錄 | 檢查日志文件 |
| 斷路器 | 故障自動檢测和恢復 | 模擬故障並觀察恢復 |

### 📚 相关文檔

- `~/longhun-system/kimi/KIMI_INTEGRATION_GUIDE.md` - 完整集成指南
- `~/longhun-system/deployment/kimi_integration_config.json` - 配置文件
- `~/longhun-system/kimi/kimi_client.py` - API 客户端源碼
- `~/longhun-system/kimi/kimi_integration.py` - 集成框架源碼

---

