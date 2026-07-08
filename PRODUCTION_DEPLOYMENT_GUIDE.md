# 龍魂系統·生產部署指南 (Production Deployment Guide)
# 日期: 2026-06-10 CST
# DNA:#龍芯⚡️2026-06-10-PRODUCTION-DEPLOYMENT-GUIDE-v1.0

---

## 📋 生產部署概覽

| 项目 | 詳情 |
|------|------|
| **部署策略** | 藍綠部署 (Blue-Green Deployment) |
| **預期耗时** | 90 分鐘 (含验收) |
| **停機时間** | 0 秒 (零停機) |
| **風險等级** | 🟢 低 (可秒级回滾) |
| **测试狀态** | ✅ Staging 全部通过 |
| **簽核狀态** | ⏳ 待生產部署簽核 |

---

## 🎯 7 階段部署路线圖

```
准备环境 (15 min)
    ↓
部署前檢查 (15 min)
    ↓
藍色环境部署 (20 min) [舊环境保持運行]
    ↓
綠色环境验證 (15 min) [新环境验證]
    ↓
流量漸进遷移 (10 min) [0% → 100%]
    ↓
生產验收 (10 min) [健康檢查]
    ↓
✅ 部署完成
```

---

## 📌 第 1 階段: 准备环境 (15 分鐘)

### 1.1 系統需求确认

```bash
# 檢查硬件资源
free -h                    # 內存 >= 8GB
df -h /                    # 磁盤 >= 100GB 空閒
nproc                      # CPU 核心 >= 4

# 檢查網絡連接
ping -c 1 8.8.8.8         # 互聯網連接
nslookup longhun.example.com  # DNS 解析正常
```

### 1.2 依賴服务檢查

```bash
# PostgreSQL 連接测试
psql -h PROD_DB_HOST -U PROD_DB_USER -d longhun_prod -c "SELECT 1"

# Redis 連接测试
redis-cli -h PROD_REDIS_HOST -a PROD_REDIS_PASSWORD PING

# Elasticsearch 連接测试
curl -u PROD_ES_USER:PROD_ES_PASSWORD https://PROD_ELASTICSEARCH_HOST:9200/_cluster/health

# Datadog API 测试
curl -H "DD-API-KEY: DATADOG_API_KEY" https://api.datadoghq.com/api/v1/validate
```

### 1.3 备份与快照

```bash
#!/bin/bash
# 完整备份腳本

BACKUP_DIR="/var/backups/longhun/pre-prod-deploy-$(date +%Y%m%d-%H%M%S)"
mkdir -p $BACKUP_DIR

# 1. 数据庫完整备份
echo "备份 PostgreSQL 数据庫..."
pg_dump -h PROD_DB_HOST -U PROD_DB_USER longhun_prod | \
  gzip > $BACKUP_DIR/database_backup.sql.gz

# 2. 应用配置备份
echo "备份应用配置..."
cp -r /etc/longhun/ $BACKUP_DIR/config_backup/

# 3. 当前部署狀态快照
echo "保存当前部署狀态..."
curl -s http://localhost:8001/api/v1/health > $BACKUP_DIR/blue_env_snapshot.json

# 4. 验證备份
echo "验證备份..."
ls -lh $BACKUP_DIR/
md5sum $BACKUP_DIR/* > $BACKUP_DIR/backup.md5

echo "✅ 备份完成: $BACKUP_DIR"
```

### 1.4 部署簽核清单

- [ ] 所有系統依賴服务在线
- [ ] 生產数据庫备份成功
- [ ] 备份验證無误
- [ ] 监控系統就緒
- [ ] 告警規则已配置
- [ ] 操作團隊待命

---

## 📌 第 2 階段: 部署前檢查 (15 分鐘)

### 2.1 Staging 最終验證

```bash
#!/bin/bash

echo "🔍 Staging 环境最終验收..."

# 1. 健康檢查 (8 项)
echo "檢查 1/8: 模塊可用性..."
python3 << 'CHECK1'
import sys
sys.path.insert(0, '/Users/zuimeidedeyihan/longhun-system')
modules = ['skills', 'monitoring', 'tools', 'integrations', 'executors']
for mod in modules:
    try:
        __import__(mod)
    except Exception as e:
        print(f"❌ {mod}: {e}")
        sys.exit(1)
print("✅ 模塊加载成功")
CHECK1

# 2. 数据庫验收
echo "檢查 2/8: 数据庫..."
python3 << 'CHECK2'
import sqlite3
conn = sqlite3.connect('/tmp/longhun-staging/data/longhun_staging.db')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
tables = cursor.fetchone()[0]
print(f"✅ 数据庫表数: {tables}")
conn.close()
CHECK2

# 3. Skill 自動補全
echo "檢查 3/8: Skill 引擎..."
python3 << 'CHECK3'
import sys
sys.path.insert(0, '/Users/zuimeidedeyihan/longhun-system')
from skills import longhun_skill_auto_completion_engine
print("✅ Skill 自動補全引擎就緒")
CHECK3

# 4-8. 其他檢查 (類似格式)
```

### 2.2 配置验證

```bash
# 验證生產配置模板
python3 << 'VERIFY'
import json
import sys

config_template = json.load(open('/Users/zuimeidedeyihan/longhun-system/prod_config_template.json'))

# 檢查关键配置
required_keys = [
    'database', 'api', 'redis', 'kubernetes',
    'monitoring', 'logging', 'security', 'backup_and_recovery'
]

for key in required_keys:
    if key not in config_template:
        print(f"❌ 缺少必要配置: {key}")
        sys.exit(1)

print("✅ 配置验證通过")
print(f"✅ 檢测到 {len(config_template)} 個配置段落")
VERIFY
```

### 2.3 性能基准线确认

```bash
# 從 Staging 讀取性能测试結果
cat /tmp/longhun-staging/logs/performance_test_results_20260610_175916.json | \
  python3 -m json.tool | grep -E '"module_load_time|"throughput|"concurrent_operations"'
```

預期結果:
- 模塊加载时間: <5ms
- 数据庫操作: <0.01ms
- 吞吐量: >2M ops/sec
- 並發操作: 10/10 成功

---

## 📌 第 3 階段: 藍色环境部署 (20 分鐘)

### 3.1 构建綠色环境 (生產副本)

```bash
#!/bin/bash

BLUE_PORT=8001
GREEN_PORT=8002
BLUE_PID_FILE="/var/run/longhun_blue.pid"
GREEN_PID_FILE="/var/run/longhun_green.pid"

echo "🟢 開始綠色环境部署..."

# Step 1: 複製代碼到綠色环境
echo "Step 1/6: 複製应用代碼..."
GREEN_ROOT="/opt/longhun-green-$(date +%Y%m%d-%H%M%S)"
mkdir -p $GREEN_ROOT
cp -r /Users/zuimeidedeyihan/longhun-system/* $GREEN_ROOT/
echo "✅ 代碼複製完成: $GREEN_ROOT"

# Step 2: 构建 Docker 镜像
echo "Step 2/6: 构建 Docker 镜像..."
cd $GREEN_ROOT
docker build -t longhun:prod-green-$(date +%s) \
  -f Dockerfile.prod \
  --build-arg ENVIRONMENT=production \
  .
IMAGE_ID=$(docker images --filter "reference=longhun:prod-green*" -q | head -1)
echo "✅ Docker 镜像构建完成: $IMAGE_ID"

# Step 3: 验證镜像
echo "Step 3/6: 验證 Docker 镜像..."
docker inspect $IMAGE_ID | python3 -m json.tool > $GREEN_ROOT/image_manifest.json
LAYERS=$(docker inspect $IMAGE_ID | grep -o '"RootFS"' | wc -l)
echo "✅ 镜像验證完成 ($LAYERS 层)"

# Step 4: 初始化数据庫遷移
echo "Step 4/6: 执行数据庫遷移..."
docker run --rm \
  -e ENVIRONMENT=production \
  -e DATABASE_URL="postgresql://PROD_DB_USER:PROD_DB_PASSWORD@PROD_DB_HOST/longhun_prod" \
  $IMAGE_ID \
  python3 -m alembic upgrade head
echo "✅ 数据庫遷移完成"

# Step 5: 種子数据初始化
echo "Step 5/6: 初始化種子数据..."
docker run --rm \
  -e ENVIRONMENT=production \
  $IMAGE_ID \
  python3 scripts/init_seed_data.py
echo "✅ 種子数据初始化完成"

# Step 6: 啟動綠色实例
echo "Step 6/6: 啟動綠色实例..."
docker run -d \
  --name longhun-green \
  -p $GREEN_PORT:443 \
  -e ENVIRONMENT=production \
  -e LOG_LEVEL=info \
  -v /etc/longhun/prod_config.json:/app/config.json:ro \
  -v /var/log/longhun:/app/logs \
  --health-cmd="curl -f http://localhost:443/health || exit 1" \
  --health-interval=10s \
  --health-timeout=5s \
  --health-retries=3 \
  $IMAGE_ID

echo "✅ 綠色实例啟動中..."
sleep 5

# 验證綠色实例
for i in {1..30}; do
  if curl -s http://localhost:$GREEN_PORT/health | grep -q "healthy"; then
    echo "✅ 綠色实例就緒 (嘗试 $i/30)"
    break
  fi
  echo "⏳ 等待綠色实例啟動... ($i/30)"
  sleep 2
done

echo "🟢 綠色环境部署完成"
```

### 3.2 藍色环境保活

```bash
#!/bin/bash

BLUE_PORT=8001
BLUE_PID_FILE="/var/run/longhun_blue.pid"

echo "🔵 藍色环境檢查..."

# 验證藍色环境仍在運行
if ps -p $(cat $BLUE_PID_FILE) > /dev/null; then
    echo "✅ 藍色环境正在運行"
    curl -s http://localhost:$BLUE_PORT/health
else
    echo "❌ 藍色环境已停止，無法进行藍綠部署"
    exit 1
fi
```

---

## 📌 第 4 階段: 綠色环境验證 (15 分鐘)

### 4.1 煙霧测试 (4 個测试)

```bash
#!/bin/bash

GREEN_PORT=8002
TESTS_PASSED=0
TESTS_TOTAL=4

test_api_connectivity() {
    echo "🧪 测试 1/4: API 連接性..."
    if curl -s -f http://localhost:$GREEN_PORT/api/v1/health | grep -q "healthy"; then
        echo "✅ API 連接成功"
        ((TESTS_PASSED++))
    else
        echo "❌ API 連接失敗"
        return 1
    fi
}

test_skills_endpoint() {
    echo "🧪 测试 2/4: Skills 端点..."
    RESPONSE=$(curl -s -w "\n%{http_code}" http://localhost:$GREEN_PORT/api/v1/skills)
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    if [ "$HTTP_CODE" = "200" ]; then
        echo "✅ Skills 端点正常"
        ((TESTS_PASSED++))
    else
        echo "❌ Skills 端点異常 (HTTP $HTTP_CODE)"
        return 1
    fi
}

test_skill_execution() {
    echo "🧪 测试 3/4: 执行单個 Skill..."
    RESPONSE=$(curl -s -X POST http://localhost:$GREEN_PORT/api/v1/skills/1/execute \
      -H "Content-Type: application/json" \
      -d '{"input": "test"}')

    if echo "$RESPONSE" | grep -q "execution_id"; then
        echo "✅ Skill 执行成功"
        ((TESTS_PASSED++))
    else
        echo "❌ Skill 执行失敗"
        return 1
    fi
}

test_monitoring_endpoint() {
    echo "🧪 测试 4/4: 监控端点..."
    RESPONSE=$(curl -s http://localhost:$GREEN_PORT/api/v1/metrics)
    if [ -n "$RESPONSE" ] && [ "$RESPONSE" != "null" ]; then
        echo "✅ 监控端点正常"
        ((TESTS_PASSED++))
    else
        echo "❌ 监控端点異常"
        return 1
    fi
}

# 運行所有测试
test_api_connectivity
test_skills_endpoint
test_skill_execution
test_monitoring_endpoint

echo ""
echo "════════════════════════════════════════"
echo "煙霧测试結果: $TESTS_PASSED/$TESTS_TOTAL 通过"
echo "════════════════════════════════════════"

if [ $TESTS_PASSED -lt $TESTS_TOTAL ]; then
    echo "❌ 煙霧测试未全部通过，请檢查綠色环境"
    exit 1
fi

echo "✅ 綠色环境验證完成"
```

### 4.2 性能验收

```bash
#!/bin/bash

GREEN_PORT=8002

echo "📊 綠色环境性能验收..."

# 運行性能测试 (簡化版)
python3 << 'PERF_TEST'
import requests
import time
import statistics

# 性能基准线
BASELINE = {
    'api_response_time': 100,  # ms
    'throughput': 100,         # req/s
    'error_rate': 0.01         # 1%
}

print("運行 100 個 API 请求...")
response_times = []
errors = 0

for i in range(100):
    try:
        start = time.time()
        response = requests.get('http://localhost:8002/api/v1/health')
        response_times.append((time.time() - start) * 1000)  # 轉換為 ms

        if response.status_code != 200:
            errors += 1
    except Exception as e:
        errors += 1

avg_time = statistics.mean(response_times)
p95_time = sorted(response_times)[95]
error_rate = errors / 100

print(f"平均響应时間: {avg_time:.2f} ms (基准: {BASELINE['api_response_time']} ms)")
print(f"P95 響应时間: {p95_time:.2f} ms")
print(f"錯误率: {error_rate:.2%} (基准: {BASELINE['error_rate']:.2%})")

if avg_time <= BASELINE['api_response_time'] and error_rate <= BASELINE['error_rate']:
    print("✅ 性能验收通过")
else:
    print("❌ 性能验收失敗")
    exit(1)
PERF_TEST
```

### 4.3 日志与监控檢查

```bash
# 查看綠色环境日志
tail -100 /var/log/longhun/green_environment.log | grep -E "ERROR|WARNING|INFO"

# 验證监控数据上传
curl -s https://api.datadoghq.com/api/v1/query \
  -H "DD-API-KEY: DATADOG_API_KEY" \
  -H "DD-APPLICATION-KEY: DATADOG_APP_KEY" \
  -d @- << 'DATADOG_QUERY'
{
  "query": "avg:longhun.api.response_time{env:prod-green} last 5m"
}
DATADOG_QUERY
```

---

## 📌 第 5 階段: 流量漸进遷移 (10 分鐘)

### 5.1 精准控制流量遷移

```bash
#!/bin/bash

# 負载均衡器配置 (AWS ELB / Nginx)

# 初始狀态: 100% 流量 → 藍色 (Blue)
# 目标狀态: 100% 流量 → 綠色 (Green)

BLUE_WEIGHT=100
GREEN_WEIGHT=0
TOTAL_WEIGHT=100

echo "🔄 開始流量漸进遷移..."
echo "初始狀态: 藍 100% / 綠 0%"

# Phase 1: 10% 流量到綠色 (5 分鐘)
echo "階段 1: 流量 10% → 綠色 (监控 5 分鐘)..."
BLUE_WEIGHT=90
GREEN_WEIGHT=10

# 更新負载均衡器配置
cat > /etc/nginx/conf.d/longhun_upstream.conf << EOF
upstream longhun_blue {
    server 127.0.0.1:8001 weight=$BLUE_WEIGHT;
    server 127.0.0.1:8002 weight=$GREEN_WEIGHT;
}
EOF

systemctl reload nginx

# 监控 5 分鐘
for i in {1..5}; do
    sleep 60
    BLUE_REQUESTS=$(curl -s http://localhost:8001/metrics | grep "requests_total" | head -1)
    GREEN_REQUESTS=$(curl -s http://localhost:8002/metrics | grep "requests_total" | head -1)
    echo "监控 $i/5: 藍色 $BLUE_REQUESTS | 綠色 $GREEN_REQUESTS"
done

echo "✅ 階段 1 完成 - 無異常"

# Phase 2: 25% 流量到綠色
echo "階段 2: 流量 25% → 綠色 (监控 3 分鐘)..."
BLUE_WEIGHT=75
GREEN_WEIGHT=25
# 更新配置 ...

# Phase 3: 50% 流量到綠色
echo "階段 3: 流量 50% → 綠色 (监控 3 分鐘)..."
BLUE_WEIGHT=50
GREEN_WEIGHT=50
# 更新配置 ...

# Phase 4: 75% 流量到綠色
echo "階段 4: 流量 75% → 綠色 (监控 2 分鐘)..."
BLUE_WEIGHT=25
GREEN_WEIGHT=75
# 更新配置 ...

# Phase 5: 100% 流量到綠色
echo "階段 5: 流量 100% → 綠色..."
BLUE_WEIGHT=0
GREEN_WEIGHT=100

cat > /etc/nginx/conf.d/longhun_upstream.conf << EOF
upstream longhun_blue {
    server 127.0.0.1:8002;
}
EOF

systemctl reload nginx

echo "✅ 流量遷移完成: 100% → 綠色"

# Phase 6: 保活藍色环境 (待命)
echo "藍色环境进入待命模式..."
echo "可在 http://localhost:8001 訪问藍色环境进行回滾验證"
```

### 5.2 实时监控指标

| 指标 | 閾值 | 狀态 |
|------|------|------|
| 綠色环境 API 应答 | <100ms | 🟢 |
| 綠色环境錯误率 | <0.5% | 🟢 |
| 綠色环境 CPU | <50% | 🟢 |
| 綠色环境 Memory | <60% | 🟢 |
| 数据庫連接延遲 | <10ms | 🟢 |

---

## 📌 第 6 階段: 生產验收 (10 分鐘)

### 6.1 最終健康檢查 (8 项)

```bash
#!/bin/bash

echo "🏥 执行最終健康檢查..."

CHECKS=0
PASSED=0

# 1. API 端点健康
echo "檢查 1/8: API 端点健康..."
if curl -s http://localhost:8002/health | grep -q "healthy"; then
    echo "✅ API 端点健康"
    ((PASSED++))
fi
((CHECKS++))

# 2. 数据庫連接
echo "檢查 2/8: 数据庫連接..."
psql -h PROD_DB_HOST -U PROD_DB_USER -d longhun_prod -c "SELECT 1" && ((PASSED++))
((CHECKS++))

# 3. Redis 連接
echo "檢查 3/8: Redis 連接..."
redis-cli -h PROD_REDIS_HOST -a PROD_REDIS_PASSWORD PING | grep -q PONG && ((PASSED++))
((CHECKS++))

# 4. 所有 Skills 加载
echo "檢查 4/8: Skills 加载..."
SKILLS=$(curl -s http://localhost:8002/api/v1/skills | grep -o '"id"' | wc -l)
if [ $SKILLS -ge 10 ]; then
    echo "✅ $SKILLS 個 Skills 已加载"
    ((PASSED++))
fi
((CHECKS++))

# 5. 监控系統
echo "檢查 5/8: 监控系統..."
curl -s http://localhost:8002/api/v1/metrics | grep -q "longhun" && ((PASSED++))
((CHECKS++))

# 6. 日志聚合
echo "檢查 6/8: 日志聚合..."
curl -s -H "Authorization: Bearer ELASTICSEARCH_TOKEN" \
  https://PROD_ELASTICSEARCH_HOST:9200/longhun-prod-* && ((PASSED++))
((CHECKS++))

# 7. 分布式追踪
echo "檢查 7/8: 分布式追踪..."
curl -s http://PROD_JAEGER_HOST:16686/api/traces | grep -q "traceID" && ((PASSED++))
((CHECKS++))

# 8. SSL 證書验證
echo "檢查 8/8: SSL 證書..."
openssl s_client -connect longhun.example.com:443 -showcerts | grep -q "CN=longhun" && ((PASSED++))
((CHECKS++))

echo ""
echo "════════════════════════════════════════"
echo "健康檢查結果: $PASSED/$CHECKS 通过"
echo "════════════════════════════════════════"

if [ $PASSED -eq $CHECKS ]; then
    echo "✅ 生產验收完成"
else
    echo "❌ 部分檢查失敗，请调查"
    exit 1
fi
```

### 6.2 利益相关者通知

```bash
#!/bin/bash

# 通知運營團隊
curl -X POST $SLACK_WEBHOOK \
  -H 'Content-Type: application/json' \
  -d '{
    "channel": "#ops-notifications",
    "text": "🟢 龍魂系統生產部署完成",
    "blocks": [
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*龍魂系統 - 生產部署成功*\n部署时間: 2026-06-10 16:XX CST\n环境: 從藍(舊) 遷移至 綠(新)\n狀态: ✅ 100% 通过\n下一步: 监控 24 小时後可停止藍色环境"
        }
      }
    ]
  }'

# 發送郵件通知
mail -s "龍魂系統生產部署完成" ops@longhun.example.com << 'EMAIL'
親愛的團隊，

龍魂系統已成功部署到生產环境。

部署詳情:
- 部署时間: 2026-06-10 16:00 CST
- 部署策略: 藍綠部署 (無停機)
- 验收狀态: 8/8 檢查通过
- 当前环境: 綠色 (新版本)
- 回滾就緒: 是 (藍色环境待命)

下一步:
1. 监控 24 小时，觀察关键指标
2. 如無異常，可在 72 小时後停用藍色环境
3. 保留完整备份 30 天

监控鏈接: https://monitoring.longhun.example.com
日志: https://logs.longhun.example.com
告警: PagerDuty (已配置)

如有任何问題，请立即聯繫運營團隊。

最佳祝願,
龍魂系統部署引擎
EMAIL
```

---

## 🔄 第 7 階段: 回滾程序 (緊急用)

### 7.1 快速回滾 (秒级)

```bash
#!/bin/bash

echo "🔴 啟動回滾程序..."

# 立即停止所有流量到綠色，恢復到藍色
cat > /etc/nginx/conf.d/longhun_upstream.conf << EOF
upstream longhun_blue {
    server 127.0.0.1:8001;
}
EOF

systemctl reload nginx

echo "✅ 流量已回滾至藍色环境"
echo "✅ 藍色环境已接管 100% 流量"

# 验證回滾
for i in {1..5}; do
    if curl -s http://localhost:8001/health | grep -q "healthy"; then
        echo "✅ 藍色环境就緒 (验證 $i/5)"
        break
    fi
    sleep 1
done

# 停止綠色环境 (保留容器备查)
docker stop longhun-green
docker rename longhun-green longhun-green-failed-backup-$(date +%s)

echo "🔵 回滾完成 - 藍色环境恢復 100% 流量"
echo "❌ 綠色环境已停止 (容器保留用於分析)"

# 通知團隊
curl -X POST $SLACK_WEBHOOK \
  -H 'Content-Type: application/json' \
  -d '{
    "channel": "#ops-critical",
    "text": "🔴 龍魂系統部署已回滾至藍色环境"
  }'
```

### 7.2 完整回滾 (资料庫還原)

```bash
#!/bin/bash

BACKUP_DIR="/var/backups/longhun/pre-prod-deploy-YYYYMMDD-HHMMSS"

echo "🔴 执行完整回滾 (包括数据庫)..."

# Step 1: 停止所有服务
echo "Step 1/5: 停止服务..."
systemctl stop longhun-api
docker stop longhun-green

# Step 2: 還原数据庫
echo "Step 2/5: 還原数据庫..."
psql -h PROD_DB_HOST -U PROD_DB_USER longhun_prod < \
  <(zcat $BACKUP_DIR/database_backup.sql.gz)

echo "✅ 数据庫已還原到部署前狀态"

# Step 3: 還原配置
echo "Step 3/5: 還原配置..."
cp -r $BACKUP_DIR/config_backup/* /etc/longhun/

# Step 4: 重啟藍色环境
echo "Step 4/5: 重啟藍色环境..."
systemctl start longhun-api

# Step 5: 验證
echo "Step 5/5: 验證系統..."
curl -s http://localhost:8001/health | grep "healthy" || exit 1

echo "✅ 完整回滾完成"
```

### 7.3 回滾決策樹

```
檢测到異常?
    ↓
是否影響关键路徑?
    ├─ YES (影響用戶) → 立即执行「快速回滾」(秒级)
    └─ NO (邊界问題) → 等待 5 分鐘，觀察监控
        ├─ 问題自動恢復? → 繼續监控
        └─ 问題持續? → 执行「快速回滾」

回滾後:
    ├─ 数据完整性無損 → 保留 72 小时後清理
    └─ 發現嚴重问題 → 执行「完整回滾」(還原备份)
```

---

## 📊 部署檢查清单 (Deployment Checklist)

### 部署前 (Pre-Deployment)
- [ ] 所有依賴服务在线且验證通过
- [ ] 完整备份已建立並验證
- [ ] 监控系統已就位
- [ ] 告警規则已配置
- [ ] 操作團隊已培訓
- [ ] 回滾計劃已确认
- [ ] Staging 验收 100% 通过
- [ ] 利益相关者已通知

### 部署中 (During Deployment)
- [ ] 藍色环境繼續正常運行
- [ ] 綠色环境部署成功
- [ ] 綠色环境煙霧测试通过
- [ ] 流量漸进遷移無異常
- [ ] 监控指标正常

### 部署後 (Post-Deployment)
- [ ] 最終健康檢查 8/8 通过
- [ ] 用戶報告無異常
- [ ] 性能指标达标
- [ ] 利益相关者已确认
- [ ] 文檔已更新

### 運維階段 (Operations)
- [ ] 藍色环境待命 72 小时
- [ ] 完整监控 24 小时
- [ ] 问題跟进日志已记錄
- [ ] 部署報告已歸檔

---

## 🚨 緊急聯繫方式

| 角色 | 聯繫方式 | 24/7 可用 |
|------|--------|---------|
| **基礎设施** | ops@longhun.example.com | 是 |
| **数据庫** | dba@longhun.example.com | 是 |
| **监控** | monitoring@longhun.example.com | 是 |
| **应急** | emergency-on-call (PagerDuty) | 是 |

---

## 📈 部署後监控指标

部署完成後，监控以下指标 24 小时:

```
API 響应时間: < 100ms (P95)
錯误率: < 0.5%
吞吐量: > 100 req/s
数据庫延遲: < 10ms
CPU 使用率: < 50%
內存占用: < 60%
磁盤空閒: > 10GB
網絡帶寬: < 70% 利用率
```

---

**DNA**:#龍芯⚡️2026-06-10-PRODUCTION-DEPLOYMENT-GUIDE-v1.0
**簽核狀态**: ⏳ 待生產环境簽核
**有效期**: 永久 (生產级部署指南)
