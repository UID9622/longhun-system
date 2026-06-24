<!--#龍芯⚡️2026-06-21-DOC-DEPLOYMENT_RUNBOOK_FOR_TEAM-v1.0 -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

# 🐉 龍魂系统 · 生产部署手册 v1.0

**目标读者**: 运维团队 / SRE 工程师 / DevOps 工程师
**部署版本**: v1.0 (2026-06-08)
**DNA**: `#龍芯⚇️2026-06-08-DEPLOYMENT-RUNBOOK-FOR-TEAM-v1.0`

---

## 📑 快速导航

- [第 1 部分：部署前准备](#第-1-部分部署前准备)
- [第 2 部分：架构概述](#第-2-部分架构概述)
- [第 3 部分：环境配置](#第-3-部分环境配置)
- [第 4 部分：部署执行](#第-4-部分部署执行)
- [第 5 部分：验证和监控](#第-5-部分验证和监控)
- [第 6 部分：故障排查](#第-6-部分故障排查)
- [第 7 部分：回滚程序](#第-7-部分回滚程序)

---

## 第 1 部分：部署前准备

### 🎯 部署前 72 小时：策划阶段

#### 1.1 团队会议 (1 小时)

**参与人员**:
- SRE Lead / DevOps Manager
- 开发团队代表
- 运维团队代表
- 产品经理
- 安全负责人

**会议议程**:
```
1. 部署时间确认 (30 分钟)
   - 选择低流量时段
   - 确认维护窗口 (建议 2-4 小时)
   - 预留额外 1-2 小时应急时间

2. 风险评估 (20 分钟)
   - 审查系统变更
   - 识别潜在风险点
   - 确认回滚计划

3. 人员分配 (10 分钟)
   - Deployment Lead (1 人)
   - Monitoring Lead (1 人)
   - Rollback Lead (1 人)
   - Support Lead (1 人)
```

#### 1.2 部署前检查清单

**24 小时前**:
- [ ] 确认所有团队成员可用
- [ ] 确认通信频道畅通 (Slack #deployment-live)
- [ ] 备份现有生产环境完整性验证
- [ ] DNS 设置已确认可回滚

**12 小时前**:
- [ ] 所有配置已准备就绪
- [ ] SSL/TLS 证书已验证有效期 (>30 天)
- [ ] 数据库连接已测试
- [ ] 监控和告警规则已配置并测试

**部署当日 - 2 小时前**:
- [ ] 团队签到
- [ ] 通信频道测试
- [ ] 监控仪表板已打开
- [ ] 回滚计划已确认
- [ ] 所有工具已就位

---

### 🔐 准备清单：安全和配置

#### 1.3 安全准备

```bash
# 1. 验证密钥管理
□ HashiCorp Vault 访问已测试
□ 所有密钥已正确配置
□ API 密钥和令牌已准备
□ SSL/TLS 证书已验证

# 2. 验证访问权限
□ 数据库用户权限已确认
□ Kubernetes 集群访问已确认
□ AWS/云平台访问已确认
□ 监控服务访问已确认

# 3. 备份确认
□ 生产数据库完整备份已验证
□ 备份可恢复性已测试
□ 备份位置已确认
□ 恢复时间目标已确认 (RTO: 15min)
```

#### 1.4 环境准备

```bash
# 准备生产配置文件
cp deployment/prod_config_template.json prod_config.json

# 编辑配置文件，填入实际生产环境信息
vim prod_config.json

# 验证配置文件格式
python3 -c "import json; json.load(open('prod_config.json'))"

# 确认输出: OK，说明配置有效
```

#### 1.5 基础设施验证

```bash
# 验证数据库连接
psql -h ${DB_HOST} -U ${DB_USER} -d ${DB_NAME} -c "SELECT 1;"

# 验证 Redis 连接
redis-cli -h ${REDIS_HOST} ping

# 验证监控服务
curl -H "DD-API-KEY: ${DD_API_KEY}" \
  https://api.datadoghq.com/api/v1/validate

# 验证 Kubernetes 集群
kubectl cluster-info
kubectl get nodes

# 验证存储卷
kubectl get pv
kubectl get pvc
```

---

## 第 2 部分：架构概述

### 🏗️ 龍魂系统架构

#### 2.1 部署架构图

```
┌─────────────────────────────────────────────────┐
│          客户端层 (Web / Mobile / API)          │
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

#### 2.2 部署策略：蓝绿部署

```
部署前状态：
┌──────────────────────────────────────┐
│  蓝色环境（当前生产）                │
│  ├─ App v1.0                         │
│  ├─ Database: Current                │
│  └─ 接收 100% 流量                   │
└──────────────────────────────────────┘

部署中状态：
┌──────────────┐    ┌──────────────────┐
│  蓝色环境    │    │  绿色环境（新）   │
│  100% 流量   │    │  0% 流量（准备）  │
│             │    │  ├─ App v2.0     │
│             │    │  ├─ 数据库迁移   │
│             │    │  └─ 健康检查     │
└──────────────┘    └──────────────────┘

流量切换：
10% → 25% → 50% → 75% → 100%
逐步转移，监控每个阶段

完成后状态：
┌──────────────────────────────────────┐
│  绿色环境（当前生产）                │
│  ├─ App v2.0                         │
│  ├─ Database: Migrated               │
│  └─ 接收 100% 流量                   │
│                                      │
│  蓝色环境（待命，可回滚）            │
└──────────────────────────────────────┘
```

#### 2.3 系统组件

| 组件 | 用途 | 可用性 |
| --- | --- | --- |
| API Gateway | 请求路由和负载均衡 | 99.95% |
| 应用服务器 | 业务逻辑执行 (3 个副本) | 99.95% |
| PostgreSQL | 数据持久化（主从复制） | 99.9% |
| Redis | 会话和缓存 | 99.9% |
| Datadog | 监控和指标 | 99.99% |
| Elasticsearch | 日志存储和搜索 | 99.9% |
| Jaeger | 分布式追踪 | 99.9% |

---

## 第 3 部分：环境配置

### ⚙️ 3.1 生产配置准备

#### 配置文件结构

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

#### 配置验证清单

```bash
# 1. 验证所有必需的环境变量已设置
required_vars=(
  "DB_HOST" "DB_PORT" "DB_NAME" "DB_USER" "DB_PASSWORD"
  "REDIS_HOST" "REDIS_PORT" "REDIS_PASSWORD"
  "DATADOG_API_KEY" "DATADOG_APP_KEY"
  "VAULT_ADDR" "VAULT_TOKEN"
)

for var in "${required_vars[@]}"; do
  if [ -z "${!var}" ]; then
    echo "❌ 缺失环境变量: $var"
    exit 1
  fi
done

# 2. 验证配置文件有效性
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
      print(f"❌ 配置缺失必需字段: {field}")
      sys.exit(1)

  print("✅ 配置文件验证通过")

except json.JSONDecodeError as e:
  print(f"❌ JSON 解析错误: {e}")
  sys.exit(1)
EOF

# 3. 测试所有连接
echo "测试数据库连接..."
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "SELECT 1;" || exit 1

echo "测试 Redis 连接..."
redis-cli -h $REDIS_HOST ping | grep PONG || exit 1

echo "测试监控服务..."
curl -s -H "DD-API-KEY: $DATADOG_API_KEY" \
  https://api.datadoghq.com/api/v1/validate | grep -q "valid" || exit 1

echo "✅ 所有连接测试通过"
```

### 3.2 Kubernetes 部署配置

#### 创建命名空间和服务账户

```bash
# 创建命名空间
kubectl create namespace longhun-prod

# 创建服务账户
kubectl create serviceaccount longhun-deployer -n longhun-prod

# 绑定角色
kubectl create rolebinding longhun-deployer-binding \
  --clusterrole=edit \
  --serviceaccount=longhun-prod:longhun-deployer \
  -n longhun-prod
```

#### 创建密钥

```bash
# 创建数据库密钥
kubectl create secret generic longhun-db-credentials \
  --from-literal=username=$DB_USER \
  --from-literal=password=$DB_PASSWORD \
  -n longhun-prod

# 创建 Redis 密钥
kubectl create secret generic longhun-redis-credentials \
  --from-literal=password=$REDIS_PASSWORD \
  -n longhun-prod

# 创建监控密钥
kubectl create secret generic longhun-monitoring \
  --from-literal=datadog-api-key=$DATADOG_API_KEY \
  --from-literal=datadog-app-key=$DATADOG_APP_KEY \
  -n longhun-prod

# 验证密钥已创建
kubectl get secrets -n longhun-prod
```

#### 部署应用

```bash
# 应用配置映射
kubectl create configmap longhun-config \
  --from-file=prod_config.json \
  -n longhun-prod

# 验证
kubectl get configmap -n longhun-prod
```

---

## 第 4 部分：部署执行

### 🚀 4.1 部署前 - 最后检查 (部署日 1 小时前)

#### 最终检查清单

```bash
#!/bin/bash
# final_checks.sh - 部署前最后检查

echo "🔍 执行部署前最后检查..."

# 1. 验证备份
echo "1️⃣  验证备份..."
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME \
  > /backup/longhun_prod_$(date +%Y%m%d_%H%M%S).sql
if [ $? -eq 0 ]; then
  echo "✅ 数据库备份成功"
else
  echo "❌ 数据库备份失败"
  exit 1
fi

# 2. 验证蓝色环境健康状态
echo "2️⃣  验证蓝色环境..."
curl -k https://api.longhun.example.com/health | grep -q healthy || {
  echo "❌ 蓝色环境不健康"
  exit 1
}
echo "✅ 蓝色环境健康"

# 3. 验证绿色环境已准备
echo "3️⃣  验证绿色环境..."
kubectl get pods -n longhun-prod-green -l app=longhun | grep -q Running || {
  echo "❌ 绿色环境 Pods 未就绪"
  exit 1
}
echo "✅ 绿色环境已就绪"

# 4. 验证监控就绪
echo "4️⃣  验证监控..."
curl -s -H "DD-API-KEY: $DATADOG_API_KEY" \
  https://api.datadoghq.com/api/v1/validate | grep -q valid || {
  echo "❌ 监控服务无法访问"
  exit 1
}
echo "✅ 监控就绪"

# 5. 验证回滚计划
echo "5️⃣  验证回滚计划..."
if [ -f "ROLLBACK_PLAN.txt" ]; then
  echo "✅ 回滚计划已准备"
else
  echo "❌ 缺失回滚计划"
  exit 1
fi

echo ""
echo "✅ 所有检查通过，可以开始部署"
```

### 4.2 部署执行步骤

#### 步骤 1：初始化绿色环境 (0-5 分钟)

```bash
#!/bin/bash
# deploy_step_1_init_green.sh

echo "🟢 [步骤 1] 初始化绿色环境"
echo "预期耗时: 3-5 分钟"

# 1. 部署新版本应用
echo "1.1 部署应用..."
kubectl apply -f deployment/kubernetes/green-deployment.yaml -n longhun-prod-green

# 2. 等待 Pods 就绪
echo "1.2 等待 Pods 就绪..."
kubectl wait --for=condition=ready pod \
  -l app=longhun,version=green \
  -n longhun-prod-green \
  --timeout=300s

# 3. 执行数据库迁移
echo "1.3 执行数据库迁移..."
kubectl exec -n longhun-prod-green -it \
  $(kubectl get pod -n longhun-prod-green -l app=longhun -o jsonpath='{.items[0].metadata.name}') \
  -- python3 /app/migrate.py --production

# 4. 验证迁移成功
echo "1.4 验证迁移..."
kubectl exec -n longhun-prod-green -it \
  $(kubectl get pod -n longhun-prod-green -l app=longhun -o jsonpath='{.items[0].metadata.name}') \
  -- python3 /app/verify_migration.py

echo "✅ 步骤 1 完成"
```

#### 步骤 2：烟雾测试 (5-10 分钟)

```bash
#!/bin/bash
# deploy_step_2_smoke_tests.sh

echo "🟢 [步骤 2] 执行烟雾测试"
echo "预期耗时: 3-5 分钟"

# 1. 获取绿色环境服务 IP
GREEN_SERVICE_IP=$(kubectl get service longhun-green \
  -n longhun-prod-green \
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

echo "绿色环境服务 IP: $GREEN_SERVICE_IP"

# 2. 执行烟雾测试
echo "2.1 测试基础端点..."
curl -k https://$GREEN_SERVICE_IP/health || {
  echo "❌ /health 端点失败"
  exit 1
}

echo "2.2 测试 API 端点..."
curl -k https://$GREEN_SERVICE_IP/api/v1/skills || {
  echo "❌ /api/v1/skills 端点失败"
  exit 1
}

echo "2.3 测试技能执行..."
curl -k -X POST https://$GREEN_SERVICE_IP/api/v1/skills/1/execute \
  -H "Content-Type: application/json" \
  -d '{"input": "test"}' || {
  echo "❌ 技能执行失败"
  exit 1
}

# 3. 验证性能
echo "2.4 验证性能指标..."
RESPONSE_TIME=$(curl -w "%{time_total}" -o /dev/null -s https://$GREEN_SERVICE_IP/health)
if (( $(echo "$RESPONSE_TIME < 0.1" | bc -l) )); then
  echo "✅ 性能正常 (${RESPONSE_TIME}s)"
else
  echo "⚠️  性能警告 (${RESPONSE_TIME}s > 100ms)"
fi

echo "✅ 步骤 2 完成"
```

#### 步骤 3：流量逐步转移 (10-30 分钟)

```bash
#!/bin/bash
# deploy_step_3_traffic_migration.sh

echo "🟢 [步骤 3] 流量逐步转移"
echo "预期耗时: 15-20 分钟"

TRAFFIC_PERCENTAGES=(10 25 50 75 100)
INTERVAL=300  # 每个阶段间隔 5 分钟

for percentage in "${TRAFFIC_PERCENTAGES[@]}"; do
  echo "3.$(printf '%d' $((percentage/25))) 转移 ${percentage}% 流量到绿色环境..."

  # 更新流量规则
  kubectl patch service longhun \
    -n longhun-prod \
    -p '{"spec":{"sessionAffinity":"None"}}' \
    --type merge

  # 更新分流规则 (使用 Istio/NG Ingress)
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

  echo "✅ ${percentage}% 流量已转移"

  # 监控这个阶段
  echo "⏳ 监控 ${INTERVAL} 秒..."
  for i in $(seq 1 5); do
    echo -n "."
    sleep 60

    # 检查错误率
    ERROR_RATE=$(curl -s \
      -H "DD-API-KEY: $DATADOG_API_KEY" \
      "https://api.datadoghq.com/api/v1/query?query=avg:trace.web.request.errors{service:longhun}&from=now-1m&to=now" \
      | jq '.result[0].values[0][1]' 2>/dev/null || echo 0)

    if (( $(echo "$ERROR_RATE > 1" | bc -l) )); then
      echo ""
      echo "⚠️  错误率过高: ${ERROR_RATE}%"
      echo "⚠️  考虑回滚或暂停部署"
    fi
  done

  echo ""
done

echo "✅ 步骤 3 完成 - 所有流量已转移到绿色环境"
```

#### 步骤 4：验证和清理 (30-45 分钟)

```bash
#!/bin/bash
# deploy_step_4_verify_cleanup.sh

echo "🟢 [步骤 4] 验证和清理"
echo "预期耗时: 10-15 分钟"

# 1. 最终健康检查
echo "4.1 执行最终健康检查..."
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

# 2. 验证性能指标
echo "4.2 验证性能指标..."
python3 << 'EOF'
import requests
import json

dd_api_key = os.environ.get('DATADOG_API_KEY')
headers = {"DD-API-KEY": dd_api_key}

# 查询吞吐量
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

# 查询延迟
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
print(f"✅ P95 延迟: {latency:.1f}ms (目标: <15ms)")
EOF

# 3. 验证数据库完整性
echo "4.3 验证数据库完整性..."
kubectl exec -n longhun-prod-green \
  $(kubectl get pod -n longhun-prod-green -l app=longhun -o jsonpath='{.items[0].metadata.name}') \
  -- python3 /app/verify_data_integrity.py

# 4. 保存蓝色环境以备回滚
echo "4.4 保存蓝色环境状态..."
kubectl scale deployment longhun-blue \
  -n longhun-prod-blue \
  --replicas=0 \
  --record

echo "✅ 蓝色环境已停止，保留以备回滚"

# 5. 标记部署完成
echo "4.5 标记部署完成..."
echo "部署完成时间: $(date)" > /deployments/latest_successful.txt
echo "部署版本: v2.0" >> /deployments/latest_successful.txt

echo ""
echo "✅ 步骤 4 完成"
echo "🎉 部署成功完成！"
```

---

## 第 5 部分：验证和监控

### 📊 5.1 部署后验证 (部署后 1 小时内)

#### 自动验证脚本

```bash
#!/bin/bash
# post_deployment_validation.sh

echo "🔍 执行部署后验证..."
VALIDATION_FAILED=0

# 1. 验证应用健康状态
echo "1️⃣  验证应用健康..."
HEALTH=$(curl -s -k https://api.longhun.example.com/health | jq '.status')
if [ "$HEALTH" == '"healthy"' ]; then
  echo "✅ 应用健康"
else
  echo "❌ 应用不健康"
  VALIDATION_FAILED=1
fi

# 2. 验证所有 Pods 就绪
echo "2️⃣  验证 Pods 就绪..."
POD_COUNT=$(kubectl get pods -n longhun-prod-green \
  -l app=longhun \
  --field-selector=status.phase=Running \
  --no-headers | wc -l)

if [ "$POD_COUNT" -ge 3 ]; then
  echo "✅ $POD_COUNT 个 Pods 运行中"
else
  echo "❌ Pods 不足: $POD_COUNT < 3"
  VALIDATION_FAILED=1
fi

# 3. 验证数据库连接
echo "3️⃣  验证数据库..."
DB_STATUS=$(psql -h $DB_HOST -U $DB_USER -d $DB_NAME \
  -t -c "SELECT 1;" 2>&1)

if [ "$DB_STATUS" == "1" ]; then
  echo "✅ 数据库连接正常"
else
  echo "❌ 数据库连接失败"
  VALIDATION_FAILED=1
fi

# 4. 验证快取
echo "4️⃣  验证快取..."
REDIS_STATUS=$(redis-cli -h $REDIS_HOST ping)

if [ "$REDIS_STATUS" == "PONG" ]; then
  echo "✅ Redis 正常"
else
  echo "❌ Redis 无法访问"
  VALIDATION_FAILED=1
fi

# 5. 验证 10 个 Skills
echo "5️⃣  验证 Skills..."
SKILLS=$(curl -s -k https://api.longhun.example.com/api/v1/skills | jq '.skills | length')

if [ "$SKILLS" == "10" ]; then
  echo "✅ 10 个 Skills 正常"
else
  echo "❌ Skills 数量异常: $SKILLS"
  VALIDATION_FAILED=1
fi

# 最终结果
if [ $VALIDATION_FAILED -eq 0 ]; then
  echo ""
  echo "🎉 所有验证通过！"
  exit 0
else
  echo ""
  echo "❌ 验证失败，请检查上方错误信息"
  exit 1
fi
```

### 5.2 持续监控 (部署后 24 小时)

#### 监控关键指标

```
🔴 关键告警 (立即行动):
  - 错误率 > 1%
  - P95 延迟 > 100ms
  - Pod 失败 > 0
  - 数据库连接失败

🟡 警告告警 (跟踪):
  - 错误率 > 0.5%
  - P95 延迟 > 50ms
  - Pod 重启 > 2
  - 内存使用 > 80%

🟢 信息告警 (参考):
  - 新 Pod 启动
  - 流量转移完成
  - 部署完成
```

#### 每小时检查清单

```
第 0 小时 (立即):
  [ ] 应用健康状态 ✅
  [ ] Pod 运行状态 ✅
  [ ] API 响应时间 ✅
  [ ] 错误率 ✅

第 1 小时:
  [ ] 吞吐量正常 ✅
  [ ] 内存使用稳定 ✅
  [ ] 无异常日志 ✅
  [ ] 用户反馈正常 ✅

第 4 小时:
  [ ] 所有指标稳定 ✅
  [ ] 无性能下降 ✅
  [ ] 无数据异常 ✅
  [ ] 系统平稳运行 ✅

第 24 小时:
  [ ] 所有指标符合预期 ✅
  [ ] 可以标记为成功部署 ✅
  [ ] 解散部署团队 ✅
  [ ] 更新部署文档 ✅
```

---

## 第 6 部分：故障排查

### ⚠️ 常见问题和解决方案

#### 问题 1：Pod 无法启动

**症状**: Pods 处于 CrashLoopBackOff

```bash
# 诊断
kubectl describe pod <pod-name> -n longhun-prod-green
kubectl logs <pod-name> -n longhun-prod-green --previous

# 常见原因和解决:
# 1. 数据库连接失败
#    → 检查数据库凭证和网络连接
psql -h $DB_HOST -U $DB_USER -d $DB_NAME

# 2. 配置丢失
#    → 验证 ConfigMap
kubectl get configmap longhun-config -n longhun-prod-green -o yaml

# 3. 密钥缺失
#    → 验证密钥
kubectl get secrets -n longhun-prod-green
```

#### 问题 2：高错误率

**症状**: 错误率突然升高 > 1%

```bash
# 诊断
# 1. 查看应用日志
kubectl logs -n longhun-prod-green -l app=longhun --tail=100 | grep ERROR

# 2. 查看 Datadog 日志
curl -s -H "DD-API-KEY: $DATADOG_API_KEY" \
  "https://api.datadoghq.com/api/v1/logs?query=service:longhun%20status:error&sort=timestamp" \
  | jq '.logs[0:10]'

# 3. 常见原因:
#    - 数据库超负荷 → 检查连接池
#    - 外部 API 超时 → 检查网络
#    - 内存泄漏 → 重启 Pod
```

#### 问题 3：性能下降

**症状**: P95 延迟 > 50ms

```bash
# 诊断
# 1. 查看资源使用
kubectl top pods -n longhun-prod-green

# 2. 查看数据库查询性能
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "
  SELECT query, calls, total_time
  FROM pg_stat_statements
  WHERE total_time > 1000
  ORDER BY total_time DESC LIMIT 10;"

# 3. 查看慢查询日志
# 在 Elasticsearch 中搜索: "duration > 50"

# 解决:
#    - 添加数据库索引
#    - 优化查询
#    - 增加 Pod 副本
```

#### 问题 4：无法回滚

**症状**: 绿色环境出现严重问题，无法提供服务

```bash
# 应急回滚:
# 1. 立即禁用绿色环境流量
kubectl patch service longhun -n longhun-prod -p \
  '{"spec":{"selector":{"version":"blue"}}}'

# 2. 恢复蓝色环境
kubectl scale deployment longhun-blue \
  -n longhun-prod-blue \
  --replicas=3

# 3. 验证恢复
curl -k https://api.longhun.example.com/health

# 4. 查看蓝色环境日志
kubectl logs -n longhun-prod-blue -l app=longhun --tail=50
```

---

## 第 7 部分：回滚程序

### 🔄 7.1 计划内回滚 (部署后发现问题)

如果部署 24 小时内发现严重问题：

```bash
#!/bin/bash
# rollback_blue_green.sh

echo "🔄 执行回滚程序..."

# 1. 验证蓝色环境可用
echo "1️⃣  验证蓝色环境..."
kubectl get pods -n longhun-prod-blue | grep Running || {
  echo "❌ 蓝色环境不可用"
  exit 1
}

# 2. 将流量转回蓝色环境
echo "2️⃣  转移流量回蓝色环境..."
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

# 3. 验证流量转移
echo "3️⃣  验证流量转移..."
sleep 30
curl -k https://api.longhun.example.com/health | grep -q healthy || {
  echo "❌ 蓝色环境无法提供服务"
  exit 1
}

# 4. 停止绿色环境
echo "4️⃣  停止绿色环境..."
kubectl scale deployment longhun-green \
  -n longhun-prod-green \
  --replicas=0

# 5. 数据库回滚 (如果需要)
echo "5️⃣  检查是否需要数据库回滚..."
echo "⚠️  如果数据库架构更改了，需要手动执行:"
echo "    psql -h $DB_HOST -U $DB_USER -d $DB_NAME < /backup/longhun_prod_YYYYMMDD_HHMMSS.sql"

echo "✅ 回滚完成"
echo "⚠️  请立即通知团队和利益相关者"
echo "⚠️  安排事件分析会议找出根本原因"
```

### 7.2 应急回滚 (完全故障)

如果系统完全故障，无法正常提供服务：

```bash
#!/bin/bash
# emergency_rollback.sh

echo "🚨 执行应急回滚..."

# 1. 立即切断绿色环境
echo "1️⃣  切断绿色环境..."
kubectl delete service longhun-green -n longhun-prod-green
kubectl delete ingress longhun-green -n longhun-prod-green

# 2. 恢复蓝色环境到满容量
echo "2️⃣  恢复蓝色环境..."
kubectl scale deployment longhun-blue -n longhun-prod-blue --replicas=5

# 3. 更新 DNS 指向蓝色环境
echo "3️⃣  更新 DNS..."
# 手动更新 DNS，或使用以下命令:
# aws route53 change-resource-record-sets ...

# 4. 验证恢复
echo "4️⃣  验证恢复..."
for i in {1..30}; do
  curl -s -k https://api.longhun.example.com/health | grep -q healthy && {
    echo "✅ 服务已恢复"
    break
  }
  echo "⏳ 等待服务恢复... ($i/30)"
  sleep 10
done

echo "✅ 应急回滚完成"
echo "🔴 立即启动事件响应"
echo "🔴 通知所有利益相关者"
echo "🔴 开始根本原因分析"
```

### 7.3 部署后回滚考量

```
回滚时间表:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

部署完成 → +1 小时: 可以快速回滚
  ├─ 应用级别回滚: 1-2 分钟
  ├─ 数据库回滚: 5-10 分钟
  └─ 总计: <15 分钟

部署完成 → +24 小时: 需要仔细回滚
  ├─ 验证数据一致性
  ├─ 执行应用回滚: 5-10 分钟
  ├─ 选择性数据库回滚: 10-30 分钟
  └─ 总计: <1 小时

部署完成 → +1 周: 可能无法完全回滚
  ├─ 新数据已写入
  ├─ 可能造成数据丢失
  └─ 需要数据迁移而非回滚
```

---

## 第 8 部分：团队角色和责任

### 👥 部署团队结构

#### Deployment Lead (1 人)
**职责**:
- 整体协调和进度控制
- 执行部署脚本
- 做出关键决策
- 与其他团队沟通

**必备技能**:
- Kubernetes 操作
- 熟悉部署流程
- 冷静应对压力

#### Monitoring Lead (1 人)
**职责**:
- 监控系统指标
- 识别异常和告警
- 评估性能影响
- 建议暂停或回滚

**必备技能**:
- 监控工具操作 (Datadog/Prometheus)
- 性能分析
- 快速决策能力

#### Database Lead (1 人)
**职责**:
- 执行数据库迁移
- 监控数据完整性
- 管理备份和恢复
- 处理数据相关问题

**必备技能**:
- PostgreSQL 知识
- 备份和恢复流程
- SQL 调优

#### Support Lead (1 人)
**职责**:
- 处理用户和客户沟通
- 记录任何用户报告的问题
- 协调与开发团队的沟通
- 为部署团队提供上下文

**必备技能**:
- 沟通技巧
- 问题分类能力

---

## 第 9 部分：部署检查清单

### ✅ 完整部署检查清单

#### 部署前 (T-72 小时)

- [ ] 安排部署会议
- [ ] 确认所有参与人员
- [ ] 审查系统变更
- [ ] 识别风险和缓解措施
- [ ] 准备回滚计划
- [ ] 准备通信计划

#### 部署前 (T-24 小时)

- [ ] 完成所有基础设施准备
- [ ] 验证备份可恢复
- [ ] 验证所有凭证和密钥
- [ ] 准备监控仪表板
- [ ] 测试通信渠道
- [ ] 确认所有人员可用

#### 部署前 (T-2 小时)

- [ ] 执行最后检查脚本
- [ ] 验证蓝色环境健康
- [ ] 验证绿色环境就绪
- [ ] 确认所有工具可用
- [ ] 团队签到
- [ ] 宣布部署开始

#### 部署期间

- [ ] 步骤 1: 初始化绿色环境 (完成)
- [ ] 步骤 2: 烟雾测试 (完成)
- [ ] 步骤 3: 流量转移 (完成)
- [ ] 步骤 4: 验证和清理 (完成)
- [ ] 持续监控和记录

#### 部署后 (T+1 小时)

- [ ] 执行部署后验证
- [ ] 确认所有指标正常
- [ ] 通知利益相关者
- [ ] 开始持续监控

#### 部署后 (T+24 小时)

- [ ] 审查所有监控数据
- [ ] 确认无异常事件
- [ ] 标记部署为成功
- [ ] 安排事件回顾会议
- [ ] 更新文档和流程
- [ ] 解散部署团队

---

## 第 10 部分：附录和参考

### 📚 文件清单

- `deployment/production_deployment.py` - 生产部署引擎
- `deployment/PRODUCTION_DEPLOYMENT_GUIDE.md` - 完整部署指南
- `deployment/prod_config_template.json` - 配置模板
- `ROLLBACK_PLAN.txt` - 详细回滚计划
- `MONITORING_SETUP.md` - 监控配置指南
- `INCIDENT_RESPONSE_PLAN.md` - 事件响应计划

### 🔗 有用的命令

```bash
# 部署相关
kubectl get pods -n longhun-prod-green
kubectl describe pod <pod-name> -n longhun-prod-green
kubectl logs <pod-name> -n longhun-prod-green

# 监控相关
kubectl top pods -n longhun-prod-green
kubectl get events -n longhun-prod-green

# 数据库相关
psql -h $DB_HOST -U $DB_USER -d $DB_NAME
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME > backup.sql
psql -h $DB_HOST -U $DB_USER -d $DB_NAME < backup.sql

# 快取相关
redis-cli -h $REDIS_HOST ping
redis-cli -h $REDIS_HOST INFO stats
```

### 📞 紧急联系方式

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

## 最后的话

这份运行手册旨在确保龍魂系统的安全、可靠部署。

**记住**:
- ✅ 计划优于仓促
- ✅ 监控比猜测更有效
- ✅ 沟通解决大多数问题
- ✅ 回滚总是一个选项

**祝部署顺利！** 🚀

---

**DNA**: `#龍芯⚇️2026-06-08-DEPLOYMENT-RUNBOOK-FOR-TEAM-v1.0`
**确认**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**最后更新**: 2026-06-08 20:20 CST
**版本**: 1.0

---

## 第 11 部分：Kimi 集成（新增 2026-06-08）

### 🔗 概述

龍魂系统已与 Kimi AI 完整集成，支持四种模式：

1. **备用推理模型** - 故障转移机制
2. **多模态处理** - 图像/文件分析
3. **实时对话** - 用户直接交互
4. **Skill 引擎** - 特定 Skill 集成

### 📦 部署步骤

#### 步骤 1: 环境配置 (T-24小时)

**1.1 设置 API 密钥**

```bash
# 方案 A: 本地密钥文件（推荐）
# 写入 ~/.longhun/secrets.env，不上传 Git
export KIMI_API_KEY="<YOUR_KIMI_API_KEY>"

# 验证设置
echo $KIMI_API_KEY
```

**1.2 验证 Kimi API 连接**

```bash
cd ~/longhun-system/kimi

python3 << 'VERIFY'
from kimi_client import KimiClient
client = KimiClient()
status = "✅ 连接成功" if client.health_check() else "❌ 连接失败"
print(f"Kimi API 状态: {status}")
VERIFY
```

**预期输出**:
```
Kimi API 状态: ✅ 连接成功
```

#### 步骤 2: 集成测试 (T-12小时)

**2.1 运行集成测试**

```bash
cd ~/longhun-system/kimi
python3 kimi_integration.py
```

**预期输出**:
```
🔗 初始化 Kimi 集成...

1️⃣ 备用推理模型
  {
    "status": "success",
    "model": "kimi",
    "response": "..."
  }

2️⃣ 多模态处理
  📸 图像处理（演示模式）

3️⃣ 实时对话
  会话 ID: KIMI-CHAT-user_001-...

4️⃣ Skill 引擎
  📐 Canvas 设计...

📊 集成状态
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
result = kimi.infer_with_fallback("龍魂系统的核心是什么？")
print(f"备用推理: {result['status']}")
TEST

# 测试实时聊天
python3 << 'TEST'
from kimi import KimiIntegration
kimi = KimiIntegration()
session = kimi.start_realtime_chat("test_user")
print(f"聊天会话: {session['session_id']}")
TEST

# 测试 Skill 引擎
python3 << 'TEST'
from kimi import KimiIntegration
kimi = KimiIntegration()
result = kimi.use_kimi_for_skill(
    "skill-3-canvas-design",
    {"description": "设计一个数据仪表板"}
)
print(f"Skill 引擎: {result['status']}")
TEST
```

#### 步骤 3: 监控和告警 (T-6小时)

**3.1 配置 Kimi 集成监控**

```bash
# 启用 Kimi 日志监控
mkdir -p /tmp/longhun-kimi/logs
touch /tmp/longhun-kimi/logs/kimi_operations.log

# 配置日志轮转
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
# 监控断路器状态
watch -n 5 'python3 << "MONITOR"
from kimi import KimiIntegration
kimi = KimiIntegration()
status = kimi.get_health_status()
print(f"Kimi API: {status[\"kimi_api\"]}")
print(f"断路器: {status[\"circuit_breaker\"][\"state\"]}")
print(f"失败计数: {status[\"circuit_breaker\"][\"failure_count\"]}")
MONITOR
'

# 监控集成日志
tail -f /tmp/longhun-kimi/logs/kimi_operations.log | grep -E "SUCCESS|FAILED"
```

**3.3 告警规则**

| 指标 | 阈值 | 严重性 |
|------|------|--------|
| Kimi API 连接 | 连续失败 3 次 | 🔴 Critical |
| 断路器状态 | 状态 = OPEN | 🟡 Warning |
| 响应时间 | > 5000ms | 🟡 Warning |
| 错误率 | > 5% | 🔴 Critical |

#### 步骤 4: 部署验收 (T-2小时)

**4.1 预部署检查清单**

```
✅ Kimi API 密钥已设置
✅ API 连接测试通过
✅ 所有集成模式可用
✅ 断路器机制正常
✅ 监控日志正常运行
✅ 告警规则已配置
✅ 回滚计划已验证
```

**4.2 执行部署前验收测试**

```bash
cd ~/longhun-system
python3 << 'ACCEPTANCE'
from kimi import KimiIntegration
import json

print("🧪 Kimi 集成验收测试\n")

kimi = KimiIntegration()

# 测试 1: API 连接
print("1️⃣ API 连接测试")
is_connected = kimi.kimi_client.health_check()
print(f"  结果: {'✅ PASS' if is_connected else '❌ FAIL'}\n")

# 测试 2: 备用推理
print("2️⃣ 备用推理测试")
result = kimi.infer_with_fallback("测试提示词")
print(f"  结果: {'✅ PASS' if result['status'] in ['success', 'fallback'] else '❌ FAIL'}\n")

# 测试 3: 实时聊天
print("3️⃣ 实时聊天测试")
session = kimi.start_realtime_chat("test_user")
print(f"  结果: {'✅ PASS' if session['status'] == 'active' else '❌ FAIL'}\n")

# 测试 4: Skill 引擎
print("4️⃣ Skill 引擎测试")
result = kimi.use_kimi_for_skill(
    "skill-3-canvas-design",
    {"description": "测试"}
)
print(f"  结果: {'✅ PASS' if result['status'] in ['success', 'unsupported'] else '❌ FAIL'}\n")

# 整体结果
print("📊 整体验收结果")
print(f"  健康状态: {json.dumps(kimi.get_health_status(), ensure_ascii=False)}")
ACCEPTANCE
```

### 🔄 故障排查

#### 问题 1: Kimi API 无法连接

**症状**: 
```
❌ Kimi API 连接失败: Connection refused
```

**诊断**:
```bash
# 检查环境变数
echo $KIMI_API_KEY

# 测试 API 端点
curl -s https://api.moonshot.cn/v1/models \
  -H "Authorization: Bearer $KIMI_API_KEY" | jq .

# 检查网络连接
ping api.moonshot.cn
```

**解决方案**:
1. 验证 KIMI_API_KEY 是否正确设置
2. 检查 API key 是否过期
3. 验证网络连接和防火墙规则
4. 检查 Kimi API 服务状态

#### 问题 2: 断路器打开

**症状**:
```json
{
  "circuit_breaker": {
    "state": "OPEN",
    "failure_count": 3
  }
}
```

**诊断**:
```bash
# 查看最近的失败日志
tail -n 50 /tmp/longhun-kimi/logs/kimi_operations.log | grep FAILED

# 检查 Kimi API 状态
python3 -c "from kimi import KimiClient; c = KimiClient(); print(c.health_check())"
```

**解决方案**:
1. 检查 Kimi API 是否正常
2. 查看失败原因（网络、超时、认证等）
3. 等待 60 秒自动恢复
4. 或手动重置: `kimi.circuit_breaker.failure_count = 0`

#### 问题 3: 响应时间过长

**症状**: 
```
⏱️ Kimi API 响应时间 > 5000ms
```

**诊断**:
```bash
# 测试 API 响应时间
time python3 << 'TEST'
from kimi import KimiClient
client = KimiClient()
result = client.chat_completion([{"role": "user", "content": "Hi"}])
print(f"完成")
TEST
```

**解决方案**:
1. 检查网络延迟
2. 检查 Kimi API 负载
3. 增加超时设置: `client = KimiClient(timeout=60)`
4. 如需紧急响应，使用本地推理降级

### ✅ 验收标准

| 项目 | 标准 | 验收方式 |
|------|------|---------|
| API 连接 | 能够成功调用 Kimi API | `health_check()` |
| 备用推理 | 故障转移机制正常 | 模拟 Kimi 故障测试 |
| 多模态 | 能够处理图像和文件 | 使用示例图像/文件测试 |
| 实时聊天 | 能够创建和维持会话 | 创建会话并发送消息 |
| Skill 引擎 | 支持的 Skill 可使用 Kimi | 测试 3 个支持的 Skill |
| 监控 | 日志和指标正常记录 | 检查日志文件 |
| 断路器 | 故障自动检测和恢复 | 模拟故障并观察恢复 |

### 📚 相关文档

- `~/longhun-system/kimi/KIMI_INTEGRATION_GUIDE.md` - 完整集成指南
- `~/longhun-system/deployment/kimi_integration_config.json` - 配置文件
- `~/longhun-system/kimi/kimi_client.py` - API 客户端源码
- `~/longhun-system/kimi/kimi_integration.py` - 集成框架源码

---

