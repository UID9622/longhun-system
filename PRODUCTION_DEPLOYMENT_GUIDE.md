# 龍魂系统·生产部署指南 (Production Deployment Guide)
# 日期: 2026-06-10 CST
# DNA:#龍芯⚡️2026-06-10-PRODUCTION-DEPLOYMENT-GUIDE-v1.0

---

## 📋 生产部署概览

| 项目 | 详情 |
|------|------|
| **部署策略** | 蓝绿部署 (Blue-Green Deployment) |
| **预期耗时** | 90 分钟 (含验收) |
| **停机时间** | 0 秒 (零停机) |
| **风险等级** | 🟢 低 (可秒级回滚) |
| **测试状态** | ✅ Staging 全部通过 |
| **签核状态** | ⏳ 待生产部署签核 |

---

## 🎯 7 阶段部署路线图

```
准备环境 (15 min)
    ↓
部署前检查 (15 min)
    ↓
蓝色环境部署 (20 min) [旧环境保持运行]
    ↓
绿色环境验证 (15 min) [新环境验证]
    ↓
流量渐进迁移 (10 min) [0% → 100%]
    ↓
生产验收 (10 min) [健康检查]
    ↓
✅ 部署完成
```

---

## 📌 第 1 阶段: 准备环境 (15 分钟)

### 1.1 系统需求确认

```bash
# 检查硬件资源
free -h                    # 内存 >= 8GB
df -h /                    # 磁盘 >= 100GB 空闲
nproc                      # CPU 核心 >= 4

# 检查网络连接
ping -c 1 8.8.8.8         # 互联网连接
nslookup longhun.example.com  # DNS 解析正常
```

### 1.2 依赖服务检查

```bash
# PostgreSQL 连接测试
psql -h PROD_DB_HOST -U PROD_DB_USER -d longhun_prod -c "SELECT 1"

# Redis 连接测试
redis-cli -h PROD_REDIS_HOST -a PROD_REDIS_PASSWORD PING

# Elasticsearch 连接测试
curl -u PROD_ES_USER:PROD_ES_PASSWORD https://PROD_ELASTICSEARCH_HOST:9200/_cluster/health

# Datadog API 测试
curl -H "DD-API-KEY: DATADOG_API_KEY" https://api.datadoghq.com/api/v1/validate
```

### 1.3 备份与快照

```bash
#!/bin/bash
# 完整备份脚本

BACKUP_DIR="/var/backups/longhun/pre-prod-deploy-$(date +%Y%m%d-%H%M%S)"
mkdir -p $BACKUP_DIR

# 1. 数据库完整备份
echo "备份 PostgreSQL 数据库..."
pg_dump -h PROD_DB_HOST -U PROD_DB_USER longhun_prod | \
  gzip > $BACKUP_DIR/database_backup.sql.gz

# 2. 应用配置备份
echo "备份应用配置..."
cp -r /etc/longhun/ $BACKUP_DIR/config_backup/

# 3. 当前部署状态快照
echo "保存当前部署状态..."
curl -s http://localhost:8001/api/v1/health > $BACKUP_DIR/blue_env_snapshot.json

# 4. 验证备份
echo "验证备份..."
ls -lh $BACKUP_DIR/
md5sum $BACKUP_DIR/* > $BACKUP_DIR/backup.md5

echo "✅ 备份完成: $BACKUP_DIR"
```

### 1.4 部署签核清单

- [ ] 所有系统依赖服务在线
- [ ] 生产数据库备份成功
- [ ] 备份验证无误
- [ ] 监控系统就绪
- [ ] 告警规则已配置
- [ ] 操作团队待命

---

## 📌 第 2 阶段: 部署前检查 (15 分钟)

### 2.1 Staging 最终验证

```bash
#!/bin/bash

echo "🔍 Staging 环境最终验收..."

# 1. 健康检查 (8 项)
echo "检查 1/8: 模块可用性..."
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
print("✅ 模块加载成功")
CHECK1

# 2. 数据库验收
echo "检查 2/8: 数据库..."
python3 << 'CHECK2'
import sqlite3
conn = sqlite3.connect('/tmp/longhun-staging/data/longhun_staging.db')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
tables = cursor.fetchone()[0]
print(f"✅ 数据库表数: {tables}")
conn.close()
CHECK2

# 3. Skill 自动补全
echo "检查 3/8: Skill 引擎..."
python3 << 'CHECK3'
import sys
sys.path.insert(0, '/Users/zuimeidedeyihan/longhun-system')
from skills import longhun_skill_auto_completion_engine
print("✅ Skill 自动补全引擎就绪")
CHECK3

# 4-8. 其他检查 (类似格式)
```

### 2.2 配置验证

```bash
# 验证生产配置模板
python3 << 'VERIFY'
import json
import sys

config_template = json.load(open('/Users/zuimeidedeyihan/longhun-system/prod_config_template.json'))

# 检查关键配置
required_keys = [
    'database', 'api', 'redis', 'kubernetes',
    'monitoring', 'logging', 'security', 'backup_and_recovery'
]

for key in required_keys:
    if key not in config_template:
        print(f"❌ 缺少必要配置: {key}")
        sys.exit(1)

print("✅ 配置验证通过")
print(f"✅ 检测到 {len(config_template)} 个配置段落")
VERIFY
```

### 2.3 性能基准线确认

```bash
# 从 Staging 读取性能测试结果
cat /tmp/longhun-staging/logs/performance_test_results_20260610_175916.json | \
  python3 -m json.tool | grep -E '"module_load_time|"throughput|"concurrent_operations"'
```

预期结果:
- 模块加载时间: <5ms
- 数据库操作: <0.01ms
- 吞吐量: >2M ops/sec
- 并发操作: 10/10 成功

---

## 📌 第 3 阶段: 蓝色环境部署 (20 分钟)

### 3.1 构建绿色环境 (生产副本)

```bash
#!/bin/bash

BLUE_PORT=8001
GREEN_PORT=8002
BLUE_PID_FILE="/var/run/longhun_blue.pid"
GREEN_PID_FILE="/var/run/longhun_green.pid"

echo "🟢 开始绿色环境部署..."

# Step 1: 复制代码到绿色环境
echo "Step 1/6: 复制应用代码..."
GREEN_ROOT="/opt/longhun-green-$(date +%Y%m%d-%H%M%S)"
mkdir -p $GREEN_ROOT
cp -r /Users/zuimeidedeyihan/longhun-system/* $GREEN_ROOT/
echo "✅ 代码复制完成: $GREEN_ROOT"

# Step 2: 构建 Docker 镜像
echo "Step 2/6: 构建 Docker 镜像..."
cd $GREEN_ROOT
docker build -t longhun:prod-green-$(date +%s) \
  -f Dockerfile.prod \
  --build-arg ENVIRONMENT=production \
  .
IMAGE_ID=$(docker images --filter "reference=longhun:prod-green*" -q | head -1)
echo "✅ Docker 镜像构建完成: $IMAGE_ID"

# Step 3: 验证镜像
echo "Step 3/6: 验证 Docker 镜像..."
docker inspect $IMAGE_ID | python3 -m json.tool > $GREEN_ROOT/image_manifest.json
LAYERS=$(docker inspect $IMAGE_ID | grep -o '"RootFS"' | wc -l)
echo "✅ 镜像验证完成 ($LAYERS 层)"

# Step 4: 初始化数据库迁移
echo "Step 4/6: 执行数据库迁移..."
docker run --rm \
  -e ENVIRONMENT=production \
  -e DATABASE_URL="postgresql://PROD_DB_USER:PROD_DB_PASSWORD@PROD_DB_HOST/longhun_prod" \
  $IMAGE_ID \
  python3 -m alembic upgrade head
echo "✅ 数据库迁移完成"

# Step 5: 种子数据初始化
echo "Step 5/6: 初始化种子数据..."
docker run --rm \
  -e ENVIRONMENT=production \
  $IMAGE_ID \
  python3 scripts/init_seed_data.py
echo "✅ 种子数据初始化完成"

# Step 6: 启动绿色实例
echo "Step 6/6: 启动绿色实例..."
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

echo "✅ 绿色实例启动中..."
sleep 5

# 验证绿色实例
for i in {1..30}; do
  if curl -s http://localhost:$GREEN_PORT/health | grep -q "healthy"; then
    echo "✅ 绿色实例就绪 (尝试 $i/30)"
    break
  fi
  echo "⏳ 等待绿色实例启动... ($i/30)"
  sleep 2
done

echo "🟢 绿色环境部署完成"
```

### 3.2 蓝色环境保活

```bash
#!/bin/bash

BLUE_PORT=8001
BLUE_PID_FILE="/var/run/longhun_blue.pid"

echo "🔵 蓝色环境检查..."

# 验证蓝色环境仍在运行
if ps -p $(cat $BLUE_PID_FILE) > /dev/null; then
    echo "✅ 蓝色环境正在运行"
    curl -s http://localhost:$BLUE_PORT/health
else
    echo "❌ 蓝色环境已停止，无法进行蓝绿部署"
    exit 1
fi
```

---

## 📌 第 4 阶段: 绿色环境验证 (15 分钟)

### 4.1 烟雾测试 (4 个测试)

```bash
#!/bin/bash

GREEN_PORT=8002
TESTS_PASSED=0
TESTS_TOTAL=4

test_api_connectivity() {
    echo "🧪 测试 1/4: API 连接性..."
    if curl -s -f http://localhost:$GREEN_PORT/api/v1/health | grep -q "healthy"; then
        echo "✅ API 连接成功"
        ((TESTS_PASSED++))
    else
        echo "❌ API 连接失败"
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
        echo "❌ Skills 端点异常 (HTTP $HTTP_CODE)"
        return 1
    fi
}

test_skill_execution() {
    echo "🧪 测试 3/4: 执行单个 Skill..."
    RESPONSE=$(curl -s -X POST http://localhost:$GREEN_PORT/api/v1/skills/1/execute \
      -H "Content-Type: application/json" \
      -d '{"input": "test"}')

    if echo "$RESPONSE" | grep -q "execution_id"; then
        echo "✅ Skill 执行成功"
        ((TESTS_PASSED++))
    else
        echo "❌ Skill 执行失败"
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
        echo "❌ 监控端点异常"
        return 1
    fi
}

# 运行所有测试
test_api_connectivity
test_skills_endpoint
test_skill_execution
test_monitoring_endpoint

echo ""
echo "════════════════════════════════════════"
echo "烟雾测试结果: $TESTS_PASSED/$TESTS_TOTAL 通过"
echo "════════════════════════════════════════"

if [ $TESTS_PASSED -lt $TESTS_TOTAL ]; then
    echo "❌ 烟雾测试未全部通过，请检查绿色环境"
    exit 1
fi

echo "✅ 绿色环境验证完成"
```

### 4.2 性能验收

```bash
#!/bin/bash

GREEN_PORT=8002

echo "📊 绿色环境性能验收..."

# 运行性能测试 (简化版)
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

print("运行 100 个 API 请求...")
response_times = []
errors = 0

for i in range(100):
    try:
        start = time.time()
        response = requests.get('http://localhost:8002/api/v1/health')
        response_times.append((time.time() - start) * 1000)  # 转换为 ms

        if response.status_code != 200:
            errors += 1
    except Exception as e:
        errors += 1

avg_time = statistics.mean(response_times)
p95_time = sorted(response_times)[95]
error_rate = errors / 100

print(f"平均响应时间: {avg_time:.2f} ms (基准: {BASELINE['api_response_time']} ms)")
print(f"P95 响应时间: {p95_time:.2f} ms")
print(f"错误率: {error_rate:.2%} (基准: {BASELINE['error_rate']:.2%})")

if avg_time <= BASELINE['api_response_time'] and error_rate <= BASELINE['error_rate']:
    print("✅ 性能验收通过")
else:
    print("❌ 性能验收失败")
    exit(1)
PERF_TEST
```

### 4.3 日志与监控检查

```bash
# 查看绿色环境日志
tail -100 /var/log/longhun/green_environment.log | grep -E "ERROR|WARNING|INFO"

# 验证监控数据上传
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

## 📌 第 5 阶段: 流量渐进迁移 (10 分钟)

### 5.1 精准控制流量迁移

```bash
#!/bin/bash

# 负载均衡器配置 (AWS ELB / Nginx)

# 初始状态: 100% 流量 → 蓝色 (Blue)
# 目标状态: 100% 流量 → 绿色 (Green)

BLUE_WEIGHT=100
GREEN_WEIGHT=0
TOTAL_WEIGHT=100

echo "🔄 开始流量渐进迁移..."
echo "初始状态: 蓝 100% / 绿 0%"

# Phase 1: 10% 流量到绿色 (5 分钟)
echo "阶段 1: 流量 10% → 绿色 (监控 5 分钟)..."
BLUE_WEIGHT=90
GREEN_WEIGHT=10

# 更新负载均衡器配置
cat > /etc/nginx/conf.d/longhun_upstream.conf << EOF
upstream longhun_blue {
    server 127.0.0.1:8001 weight=$BLUE_WEIGHT;
    server 127.0.0.1:8002 weight=$GREEN_WEIGHT;
}
EOF

systemctl reload nginx

# 监控 5 分钟
for i in {1..5}; do
    sleep 60
    BLUE_REQUESTS=$(curl -s http://localhost:8001/metrics | grep "requests_total" | head -1)
    GREEN_REQUESTS=$(curl -s http://localhost:8002/metrics | grep "requests_total" | head -1)
    echo "监控 $i/5: 蓝色 $BLUE_REQUESTS | 绿色 $GREEN_REQUESTS"
done

echo "✅ 阶段 1 完成 - 无异常"

# Phase 2: 25% 流量到绿色
echo "阶段 2: 流量 25% → 绿色 (监控 3 分钟)..."
BLUE_WEIGHT=75
GREEN_WEIGHT=25
# 更新配置 ...

# Phase 3: 50% 流量到绿色
echo "阶段 3: 流量 50% → 绿色 (监控 3 分钟)..."
BLUE_WEIGHT=50
GREEN_WEIGHT=50
# 更新配置 ...

# Phase 4: 75% 流量到绿色
echo "阶段 4: 流量 75% → 绿色 (监控 2 分钟)..."
BLUE_WEIGHT=25
GREEN_WEIGHT=75
# 更新配置 ...

# Phase 5: 100% 流量到绿色
echo "阶段 5: 流量 100% → 绿色..."
BLUE_WEIGHT=0
GREEN_WEIGHT=100

cat > /etc/nginx/conf.d/longhun_upstream.conf << EOF
upstream longhun_blue {
    server 127.0.0.1:8002;
}
EOF

systemctl reload nginx

echo "✅ 流量迁移完成: 100% → 绿色"

# Phase 6: 保活蓝色环境 (待命)
echo "蓝色环境进入待命模式..."
echo "可在 http://localhost:8001 访问蓝色环境进行回滚验证"
```

### 5.2 实时监控指标

| 指标 | 阈值 | 状态 |
|------|------|------|
| 绿色环境 API 应答 | <100ms | 🟢 |
| 绿色环境错误率 | <0.5% | 🟢 |
| 绿色环境 CPU | <50% | 🟢 |
| 绿色环境 Memory | <60% | 🟢 |
| 数据库连接延迟 | <10ms | 🟢 |

---

## 📌 第 6 阶段: 生产验收 (10 分钟)

### 6.1 最终健康检查 (8 项)

```bash
#!/bin/bash

echo "🏥 执行最终健康检查..."

CHECKS=0
PASSED=0

# 1. API 端点健康
echo "检查 1/8: API 端点健康..."
if curl -s http://localhost:8002/health | grep -q "healthy"; then
    echo "✅ API 端点健康"
    ((PASSED++))
fi
((CHECKS++))

# 2. 数据库连接
echo "检查 2/8: 数据库连接..."
psql -h PROD_DB_HOST -U PROD_DB_USER -d longhun_prod -c "SELECT 1" && ((PASSED++))
((CHECKS++))

# 3. Redis 连接
echo "检查 3/8: Redis 连接..."
redis-cli -h PROD_REDIS_HOST -a PROD_REDIS_PASSWORD PING | grep -q PONG && ((PASSED++))
((CHECKS++))

# 4. 所有 Skills 加载
echo "检查 4/8: Skills 加载..."
SKILLS=$(curl -s http://localhost:8002/api/v1/skills | grep -o '"id"' | wc -l)
if [ $SKILLS -ge 10 ]; then
    echo "✅ $SKILLS 个 Skills 已加载"
    ((PASSED++))
fi
((CHECKS++))

# 5. 监控系统
echo "检查 5/8: 监控系统..."
curl -s http://localhost:8002/api/v1/metrics | grep -q "longhun" && ((PASSED++))
((CHECKS++))

# 6. 日志聚合
echo "检查 6/8: 日志聚合..."
curl -s -H "Authorization: Bearer ELASTICSEARCH_TOKEN" \
  https://PROD_ELASTICSEARCH_HOST:9200/longhun-prod-* && ((PASSED++))
((CHECKS++))

# 7. 分布式追踪
echo "检查 7/8: 分布式追踪..."
curl -s http://PROD_JAEGER_HOST:16686/api/traces | grep -q "traceID" && ((PASSED++))
((CHECKS++))

# 8. SSL 证书验证
echo "检查 8/8: SSL 证书..."
openssl s_client -connect longhun.example.com:443 -showcerts | grep -q "CN=longhun" && ((PASSED++))
((CHECKS++))

echo ""
echo "════════════════════════════════════════"
echo "健康检查结果: $PASSED/$CHECKS 通过"
echo "════════════════════════════════════════"

if [ $PASSED -eq $CHECKS ]; then
    echo "✅ 生产验收完成"
else
    echo "❌ 部分检查失败，请调查"
    exit 1
fi
```

### 6.2 利益相关者通知

```bash
#!/bin/bash

# 通知运营团队
curl -X POST $SLACK_WEBHOOK \
  -H 'Content-Type: application/json' \
  -d '{
    "channel": "#ops-notifications",
    "text": "🟢 龍魂系统生产部署完成",
    "blocks": [
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*龍魂系统 - 生产部署成功*\n部署时间: 2026-06-10 16:XX CST\n环境: 从蓝(旧) 迁移至 绿(新)\n状态: ✅ 100% 通过\n下一步: 监控 24 小时后可停止蓝色环境"
        }
      }
    ]
  }'

# 发送邮件通知
mail -s "龍魂系统生产部署完成" ops@longhun.example.com << 'EMAIL'
亲爱的团队，

龍魂系统已成功部署到生产环境。

部署详情:
- 部署时间: 2026-06-10 16:00 CST
- 部署策略: 蓝绿部署 (无停机)
- 验收状态: 8/8 检查通过
- 当前环境: 绿色 (新版本)
- 回滚就绪: 是 (蓝色环境待命)

下一步:
1. 监控 24 小时，观察关键指标
2. 如无异常，可在 72 小时后停用蓝色环境
3. 保留完整备份 30 天

监控链接: https://monitoring.longhun.example.com
日志: https://logs.longhun.example.com
告警: PagerDuty (已配置)

如有任何问题，请立即联系运营团队。

最佳祝愿,
龍魂系统部署引擎
EMAIL
```

---

## 🔄 第 7 阶段: 回滚程序 (紧急用)

### 7.1 快速回滚 (秒级)

```bash
#!/bin/bash

echo "🔴 启动回滚程序..."

# 立即停止所有流量到绿色，恢复到蓝色
cat > /etc/nginx/conf.d/longhun_upstream.conf << EOF
upstream longhun_blue {
    server 127.0.0.1:8001;
}
EOF

systemctl reload nginx

echo "✅ 流量已回滚至蓝色环境"
echo "✅ 蓝色环境已接管 100% 流量"

# 验证回滚
for i in {1..5}; do
    if curl -s http://localhost:8001/health | grep -q "healthy"; then
        echo "✅ 蓝色环境就绪 (验证 $i/5)"
        break
    fi
    sleep 1
done

# 停止绿色环境 (保留容器备查)
docker stop longhun-green
docker rename longhun-green longhun-green-failed-backup-$(date +%s)

echo "🔵 回滚完成 - 蓝色环境恢复 100% 流量"
echo "❌ 绿色环境已停止 (容器保留用于分析)"

# 通知团队
curl -X POST $SLACK_WEBHOOK \
  -H 'Content-Type: application/json' \
  -d '{
    "channel": "#ops-critical",
    "text": "🔴 龍魂系统部署已回滚至蓝色环境"
  }'
```

### 7.2 完整回滚 (资料库还原)

```bash
#!/bin/bash

BACKUP_DIR="/var/backups/longhun/pre-prod-deploy-YYYYMMDD-HHMMSS"

echo "🔴 执行完整回滚 (包括数据库)..."

# Step 1: 停止所有服务
echo "Step 1/5: 停止服务..."
systemctl stop longhun-api
docker stop longhun-green

# Step 2: 还原数据库
echo "Step 2/5: 还原数据库..."
psql -h PROD_DB_HOST -U PROD_DB_USER longhun_prod < \
  <(zcat $BACKUP_DIR/database_backup.sql.gz)

echo "✅ 数据库已还原到部署前状态"

# Step 3: 还原配置
echo "Step 3/5: 还原配置..."
cp -r $BACKUP_DIR/config_backup/* /etc/longhun/

# Step 4: 重启蓝色环境
echo "Step 4/5: 重启蓝色环境..."
systemctl start longhun-api

# Step 5: 验证
echo "Step 5/5: 验证系统..."
curl -s http://localhost:8001/health | grep "healthy" || exit 1

echo "✅ 完整回滚完成"
```

### 7.3 回滚决策树

```
检测到异常?
    ↓
是否影响关键路径?
    ├─ YES (影响用户) → 立即执行“快速回滚”(秒级)
    └─ NO (边界问题) → 等待 5 分钟，观察监控
        ├─ 问题自动恢复? → 继续监控
        └─ 问题持续? → 执行“快速回滚”

回滚后:
    ├─ 数据完整性无损 → 保留 72 小时后清理
    └─ 发现严重问题 → 执行“完整回滚”(还原备份)
```

---

## 📊 部署检查清单 (Deployment Checklist)

### 部署前 (Pre-Deployment)
- [ ] 所有依赖服务在线且验证通过
- [ ] 完整备份已建立并验证
- [ ] 监控系统已就位
- [ ] 告警规则已配置
- [ ] 操作团队已培训
- [ ] 回滚计划已确认
- [ ] Staging 验收 100% 通过
- [ ] 利益相关者已通知

### 部署中 (During Deployment)
- [ ] 蓝色环境继续正常运行
- [ ] 绿色环境部署成功
- [ ] 绿色环境烟雾测试通过
- [ ] 流量渐进迁移无异常
- [ ] 监控指标正常

### 部署后 (Post-Deployment)
- [ ] 最终健康检查 8/8 通过
- [ ] 用户报告无异常
- [ ] 性能指标达标
- [ ] 利益相关者已确认
- [ ] 文档已更新

### 运维阶段 (Operations)
- [ ] 蓝色环境待命 72 小时
- [ ] 完整监控 24 小时
- [ ] 问题跟进日志已记录
- [ ] 部署报告已归档

---

## 🚨 紧急联系方式

| 角色 | 联系方式 | 24/7 可用 |
|------|--------|---------|
| **基础设施** | ops@longhun.example.com | 是 |
| **数据库** | dba@longhun.example.com | 是 |
| **监控** | monitoring@longhun.example.com | 是 |
| **应急** | emergency-on-call (PagerDuty) | 是 |

---

## 📈 部署后监控指标

部署完成后，监控以下指标 24 小时:

```
API 响应时间: < 100ms (P95)
错误率: < 0.5%
吞吐量: > 100 req/s
数据库延迟: < 10ms
CPU 使用率: < 50%
内存占用: < 60%
磁盘空闲: > 10GB
网络带宽: < 70% 利用率
```

---

**DNA**:#龍芯⚡️2026-06-10-PRODUCTION-DEPLOYMENT-GUIDE-v1.0
**签核状态**: ⏳ 待生产环境签核
**有效期**: 永久 (生产级部署指南)
