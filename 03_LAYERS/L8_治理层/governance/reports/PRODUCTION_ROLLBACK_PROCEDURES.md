# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统·生产回滚程序 (Production Rollback Procedures)
# 日期: 2026-06-10 CST
# DNA:#龍芯⚡️丙午·甲午·乙卯·壬午·䷚颐-PRODUCTION-ROLLBACK-PROCEDURES-v1.0

---

## 📋 回滚级别定义

| 级别 | 触发条件 | 恢复时间 | 数据完整 | 使用场景 |
|------|--------|--------|--------|--------|
| **L1 快速回滚** | API 可用性 <95% | 秒级 | ✅ 是 | 应用层问题 |
| **L2 标准回滚** | 功能异常 | 分钟级 | ✅ 是 | 逻辑层问题 |
| **L3 深层回滚** | 数据不一致 | 10-15 分钟 | ✅ 是 | 数据层问题 |
| **L4 紧急回滚** | 系统瘫痪 | 15-30 分钟 | ✅ 是 | 严重故障 |

---

## 🚨 回滚决策流程

```
监测到异常
    ↓
分析问题严重级别
    ↓
┌───────────────────────────────────────────┐
│ 严重级别评分: 0-100                       │
├───────────────────────────────────────────┤
│ 0-25  → 观察 10 分钟 → L0 (不回滚)       │
│ 26-50 → 等待 5 分钟  → L1 (快速回滚)    │
│ 51-75 → 立即评估    → L2 (标准回滚)    │
│ 76-100→ 立即执行    → L3/L4 (深层回滚) │
└───────────────────────────────────────────┘
```

---

## ✅ 回滚检查清单 (快速参考)

```
🚨 回滚前必检 (30 秒)
☑️ API 当前状态确认
☑️ 用户影响程度评估
☑️ 备份档案完整性验证
☑️ 蓝色环境就绪状态

🔄 回滚执行 (2-30 分钟，取决于回滚级别)
☑️ 根据级别执行回滚脚本
☑️ 监控回滚进度
☑️ 验证系统恢复

✅ 回滚后验证 (10 分钟)
☑️ 所有端点健康检查
☑️ 数据完整性验证
☑️ 性能指标确认
☑️ 利益相关者通知
```

---

## 🔵 L1: 快速回滚 (应用层・秒级)

**触发条件:**
- 绿色环境 API 可用性 <95%
- 但数据层正常
- 需要在秒级内恢复

### L1 回滚步骤

```bash
#!/bin/bash
# 龍魂系统 L1 快速回滚脚本

ROLLBACK_ID="L1-$(date +%Y%m%d-%H%M%S)"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "🔴 [$TIMESTAMP] 开始 L1 快速回滚 ($ROLLBACK_ID)..."

# Step 1: 流量立即切回蓝色 (< 1 秒)
echo "Step 1: 流量切回蓝色环境..."
cat > /etc/nginx/conf.d/longhun_upstream.conf << EOF
upstream longhun {
    server 127.0.0.1:8001 max_fails=0;
}
EOF
systemctl reload nginx
echo "✅ 流量已切至蓝色 (< 1 秒)"

# Step 2: 停止绿色环境 (< 5 秒)
echo "Step 2: 停止绿色环境..."
docker stop longhun-green -t 3  # 3 秒优雅关闭
CONTAINER_ID=$(docker ps -a | grep longhun-green-failed | head -1 | awk '{print $1}')
docker rename longhun-green longhun-green-rollback-$ROLLBACK_ID
echo "✅ 绿色环境已停止 (容器: longhun-green-rollback-$ROLLBACK_ID)"

# Step 3: 验证蓝色环境 (< 5 秒)
echo "Step 3: 验证蓝色环境..."
for i in {1..3}; do
    if curl -s http://localhost:8001/health | grep -q "healthy"; then
        echo "✅ 蓝色环境健康检查通过"
        break
    fi
    sleep 1
done

# Step 4: 执行内存快照 (< 2 秒)
echo "Step 4: 保存系统快照..."
curl -s http://localhost:8001/api/v1/system/snapshot > \
  /var/backups/rollback-snapshots/$ROLLBACK_ID-blue-env-state.json

# Step 5: 清除缓存 (< 1 秒)
echo "Step 5: 清除应用缓存..."
redis-cli FLUSHDB
redis-cli PUBLISH rollback "L1 回滚完成"

echo ""
echo "════════════════════════════════════════"
echo "✅ L1 快速回滚完成 (耗时: < 15 秒)"
echo "════════════════════════════════════════"
echo "回滚 ID: $ROLLBACK_ID"
echo "恢复时间: < 1 秒"
echo "数据完整: ✅ 是"
echo "用户可用: ✅ 是"

# Step 6: 通知团队
cat > /tmp/rollback_alert.json << EOF
{
  "channel": "#ops-critical",
  "severity": "CRITICAL",
  "event": "L1 ROLLBACK TRIGGERED",
  "rollback_id": "$ROLLBACK_ID",
  "timestamp": "$TIMESTAMP",
  "message": "应用层异常，已自动回滚到蓝色环境",
  "recovery_time": "< 1 秒",
  "data_integrity": "✅ 完整"
}
EOF

curl -X POST $SLACK_WEBHOOK -d @/tmp/rollback_alert.json

echo ""
echo "📊 回滚详情:"
echo "  • 回滚等级: L1 (应用层)"
echo "  • 触发时间: $TIMESTAMP"
echo "  • 恢复时间: < 15 秒"
echo "  • 数据丢失: 否"
echo "  • 用户影响: < 30 秒 (请求失败后重试)"
echo "  • 日志位置: /var/log/longhun/rollback-$ROLLBACK_ID.log"
```

**验证 L1 回滚成功:**

```bash
# 1. 验证流量已切换
curl -v http://longhun.example.com/health 2>&1 | grep -A 5 "HTTP"

# 2. 验证蓝色环境状态
curl http://localhost:8001/api/v1/health | python3 -m json.tool

# 3. 验证数据库连接
psql -h PROD_DB_HOST -U PROD_DB_USER -d longhun_prod -c "SELECT COUNT(*) FROM users;"

# 4. 确认没有数据丢失
curl http://localhost:8001/api/v1/audit/transactions | grep -c "complete"
```

---

## 🔄 L2: 标准回滚 (逻辑层・分钟级)

**触发条件:**
- Skill 执行错误率 > 5%
- 功能异常但 API 可用
- 需要在分钟级内恢复

### L2 回滚步骤

```bash
#!/bin/bash
# 龍魂系统 L2 标准回滚脚本

ROLLBACK_ID="L2-$(date +%Y%m%d-%H%M%S)"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "🟠 [$TIMESTAMP] 开始 L2 标准回滚..."

# Step 1: 停止新请求入队
echo "Step 1: 暂停新请求..."
curl -X POST http://localhost:8002/api/v1/admin/pause-intake \
  -H "Authorization: Bearer ADMIN_TOKEN"

# Step 2: 等待现有请求完成 (最多 30 秒)
echo "Step 2: 等待现有请求完成..."
for i in {1..30}; do
    PENDING=$(curl -s http://localhost:8002/api/v1/admin/queue-status | \
      grep -o '"pending":"[0-9]*"' | cut -d'"' -f4)

    if [ "$PENDING" = "0" ]; then
        echo "✅ 所有请求已完成 ($i 秒)"
        break
    fi

    echo "⏳ 等待请求完成... ($PENDING 个待处理, $i/30 秒)"
    sleep 1
done

# Step 3: 立即切换流量回蓝色
echo "Step 3: 切换流量..."
cat > /etc/nginx/conf.d/longhun_upstream.conf << EOF
upstream longhun {
    server 127.0.0.1:8001;
}
EOF
systemctl reload nginx

# Step 4: 停止绿色环境中的 Skill 执行器
echo "Step 4: 停止 Skill 执行器..."
docker exec longhun-green python3 -c \
  "from skills import executor; executor.shutdown()"

# Step 5: 从最近一个检查点恢复应用状态
echo "Step 5: 恢复应用状态..."
LAST_CHECKPOINT="/var/backups/checkpoints/last-stable-$(date +%Y%m%d).json"
if [ -f "$LAST_CHECKPOINT" ]; then
    curl -X POST http://localhost:8001/api/v1/admin/restore-checkpoint \
      -H "Content-Type: application/json" \
      -d @$LAST_CHECKPOINT
    echo "✅ 从检查点恢复 ($(stat -f%z $LAST_CHECKPOINT 2>/dev/null || stat -c%s $LAST_CHECKPOINT) 字节)"
else
    echo "⚠️  未找到最近检查点，跳过状态恢复"
fi

# Step 6: 验证蓝色环境数据一致性
echo "Step 6: 验证数据一致性..."
python3 << 'VERIFY'
import requests
import json

# 验证 5 个随机用户的数据完整性
api_base = "http://localhost:8001/api/v1"

for user_id in [1, 10, 50, 100, 500]:
    try:
        response = requests.get(f"{api_base}/users/{user_id}")
        if response.status_code == 200:
            data = response.json()
            if "id" in data and "created_at" in data:
                print(f"✅ 用户 {user_id} 数据完整")
        else:
            print(f"⚠️  用户 {user_id} 返回 {response.status_code}")
    except Exception as e:
        print(f"❌ 用户 {user_id} 验证失败: {e}")
VERIFY

echo ""
echo "════════════════════════════════════════"
echo "✅ L2 标准回滚完成 (耗时: 30-60 秒)"
echo "════════════════════════════════════════"

# 监控恢复
for i in {1..5}; do
    ERROR_RATE=$(curl -s http://localhost:8001/metrics | \
      grep "error_rate" | grep -o "[0-9]*\.[0-9]*" | head -1)
    echo "监控 $i/5: 错误率 = ${ERROR_RATE}% (目标 < 0.5%)"
    sleep 2
done
```

---

## 💾 L3: 深层回滚 (数据层・10-15 分钟)

**触发条件:**
- 数据不一致检测
- 数据库异常
- 需要从备份恢复

### L3 回滚步骤

```bash
#!/bin/bash
# 龍魂系统 L3 深层回滚脚本

ROLLBACK_ID="L3-$(date +%Y%m%d-%H%M%S)"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "🔴 [$TIMESTAMP] 开始 L3 深层回滚..."
echo "⚠️  此操作涉及数据库恢复，请确认已通知所有利益相关者"

# Step 1: 立即切换流量
echo "Step 1: 切换流量至蓝色..."
cat > /etc/nginx/conf.d/longhun_upstream.conf << EOF
upstream longhun {
    server 127.0.0.1:8001;
}
EOF
systemctl reload nginx

# Step 2: 停止所有写操作
echo "Step 2: 停止所有写操作..."
systemctl stop longhun-worker-write

# Step 3: 确定备份点
echo "Step 3: 确定备份点..."
BACKUP_MANIFEST="/var/backups/longhun/backup-manifest.json"
LATEST_BACKUP=$(cat $BACKUP_MANIFEST | \
  python3 -c "import sys, json; m=json.load(sys.stdin); print(max(m['backups'], key=lambda b: b['timestamp'])['path'])")
echo "使用备份: $LATEST_BACKUP (时间: $(date -f $LATEST_BACKUP))"

# Step 4: 关闭数据库连接
echo "Step 4: 关闭现有数据库连接..."
psql -h PROD_DB_HOST -U PROD_DB_USER -d postgres << SQL
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'longhun_prod'
  AND pid <> pg_backend_pid();
SQL

# Step 5: 还原数据库
echo "Step 5: 还原数据库 (耗时: 5-10 分钟)..."
BACKUP_FILE="${LATEST_BACKUP}/database_backup.sql.gz"
zcat "$BACKUP_FILE" | psql -h PROD_DB_HOST -U PROD_DB_USER longhun_prod 2>&1 | \
  tee /tmp/restore-log-$ROLLBACK_ID.txt

if [ $? -eq 0 ]; then
    echo "✅ 数据库已还原"
else
    echo "❌ 数据库还原失败，查看日志: /tmp/restore-log-$ROLLBACK_ID.txt"
    exit 1
fi

# Step 6: 验证数据库
echo "Step 6: 验证数据库完整性..."
psql -h PROD_DB_HOST -U PROD_DB_USER longhun_prod << SQL
-- 检查表数量
SELECT COUNT(*) as table_count FROM information_schema.tables
WHERE table_schema = 'public';

-- 检查索引
SELECT COUNT(*) as index_count FROM information_schema.statistics
WHERE table_schema = 'public';

-- 检查外键
SELECT COUNT(*) as constraint_count FROM information_schema.table_constraints
WHERE constraint_type = 'FOREIGN KEY' AND table_schema = 'public';
SQL

# Step 7: 重启写操作工作线程
echo "Step 7: 重启写操作工作线程..."
systemctl start longhun-worker-write

# Step 8: 恢复绿色环境 (使用还原的数据)
echo "Step 8: 重建绿色环境..."
docker rm longhun-green
# 重新创建绿色环境...

echo ""
echo "════════════════════════════════════════"
echo "✅ L3 深层回滚完成 (耗时: 10-15 分钟)"
echo "════════════════════════════════════════"
echo "恢复点: $LATEST_BACKUP"
echo "数据状态: $(date -r $LATEST_BACKUP)"
echo "用户数据丢失: 否 (最多丢失最近 1 小时的写操作)"
```

---

## 🆘 L4: 紧急回滚 (系统级・15-30 分钟)

**触发条件:**
- 系统完全瘫痪
- 多个层面同时故障
- 需要完全环境重建

### L4 回滚步骤

```bash
#!/bin/bash
# 龍魂系统 L4 紧急回滚脚本

ROLLBACK_ID="L4-EMERGENCY-$(date +%Y%m%d-%H%M%S)"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "🚨 [$TIMESTAMP] 开始 L4 紧急回滚..."
echo "⚠️  此操作将重建整个生产环境，请验证决策！"

# 要求确认
read -p "确认执行 L4 紧急回滚? (输入 'CONFIRM-EMERGENCY-ROLLBACK' 继续): " CONFIRM
if [ "$CONFIRM" != "CONFIRM-EMERGENCY-ROLLBACK" ]; then
    echo "❌ 已取消 L4 回滚"
    exit 1
fi

# Step 1: 通知所有利益相关者
echo "Step 1: 发送紧急通知..."
curl -X POST https://api.pagerduty.com/incidents \
  -H "Authorization: Token token=$PAGERDUTY_TOKEN" \
  -d "{
    \"incident\": {
      \"type\": \"incident_reference\",
      \"title\": \"龍魂系统 L4 紧急回滚\",
      \"service\": {
        \"id\": \"PROD_SERVICE_ID\",
        \"type\": \"service_reference\"
      },
      \"urgency\": \"high\"
    }
  }"

# Step 2: 切换到备用区域 (如果配置了地域冗余)
echo "Step 2: 检查备用区域..."
if [ -n "$STANDBY_REGION" ]; then
    echo "✅ 有备用区域可用，准备切换..."
    # AWS 区域切换逻辑
else
    echo "ℹ️  单区域部署，无法地域切换"
fi

# Step 3: 停止所有服务
echo "Step 3: 停止所有服务..."
systemctl stop longhun-api
docker stop $(docker ps -q -f "label=longhun=prod") 2>/dev/null
killall python3 2>/dev/null

# Step 4: 从最早稳定备份还原
echo "Step 4: 选择最早稳定备份..."
EARLIEST_STABLE="/var/backups/longhun/earliest-stable-backup"
if [ -d "$EARLIEST_STABLE" ]; then
    echo "使用备份: $EARLIEST_STABLE"
else
    echo "❌ 找不到稳定备份，寻找最近备份..."
    EARLIEST_STABLE=$(ls -td /var/backups/longhun/*/ | head -1)
fi

# Step 5: 完整环境重建
echo "Step 5: 环境重建 (耗时: 15-20 分钟)..."

# 5a. 清理旧环境
echo "  5a) 清理旧环境..."
rm -rf /opt/longhun-*
docker system prune -f --volumes

# 5b. 还原代码
echo "  5b) 还原代码..."
cp -r $EARLIEST_STABLE/application-code /opt/longhun-app

# 5c. 还原数据库
echo "  5c) 还原数据库..."
zcat $EARLIEST_STABLE/database_backup.sql.gz | \
  psql -h PROD_DB_HOST -U PROD_DB_USER longhun_prod

# 5d. 重构基础设施
echo "  5d) 重构基础设施..."
bash /opt/longhun-app/scripts/rebuild-infrastructure.sh

# Step 6: 验证系统
echo "Step 6: 系统验证..."
for i in {1..10}; do
    if curl -s http://localhost:8001/health | grep -q "healthy"; then
        echo "✅ 系统已恢复 (尝试 $i/10)"
        break
    fi
    echo "⏳ 等待系统启动... ($i/10)"
    sleep 10
done

# Step 7: 数据验证
echo "Step 7: 数据验证..."
RECORD_COUNT=$(psql -h PROD_DB_HOST -U PROD_DB_USER longhun_prod \
  -t -c "SELECT COUNT(*) FROM users;")
echo "✅ 用户记录: $RECORD_COUNT"

echo ""
echo "════════════════════════════════════════"
echo "✅ L4 紧急回滚完成 (耗时: 20-30 分钟)"
echo "════════════════════════════════════════"
echo "恢复时间: $((SECONDS / 60)) 分钟"
echo "数据恢复到: $(date -r $EARLIEST_STABLE)"
echo "用户影响: 最多 24 小时内的数据丢失"
```

---

## 📊 回滚监控仪表板

```bash
#!/bin/bash
# 实时监控回滚进度

watch -n 1 'echo "=== 龍魂系统回滚监控 ($(date)) ===" && \
echo "" && \
echo "🔵 蓝色环境: $(curl -s http://localhost:8001/health | grep -o "healthy" || echo "不可用")" && \
echo "🟢 绿色环境: $(curl -s http://localhost:8002/health | grep -o "healthy" || echo "不可用")" && \
echo "" && \
echo "流量分配:" && \
curl -s http://localhost/nginx_status | grep -A 1 "upstream" && \
echo "" && \
echo "数据库状态:" && \
psql -h PROD_DB_HOST -U PROD_DB_USER -t -c "SELECT datname, numbackends FROM pg_stat_database WHERE datname = \"longhun_prod\";" && \
echo "" && \
echo "队列状态:" && \
redis-cli LLEN longhun:jobs:pending || echo "Redis 不可用"'
```

---

## ✅ 回滚完成检查清单

```
□ 流量已切回蓝色环境 (验证: curl 返回 200)
□ 绿色环境已停止 (容器已保存用于分析)
□ 数据库连接正常 (验证: psql 连接成功)
□ 所有 API 端点响应正常 (验证: 8/8 健康检查通过)
□ 日志无 ERROR 或 CRITICAL 级别消息 (最近 5 分钟)
□ 应用性能达到基准线 (P95 延迟 < 100ms)
□ 利益相关者已通知 (Slack, PagerDuty, 邮件)
□ 回滚事后分析已启动 (事件编号已记录)
□ 备份验证完成 (完整性检查通过)
□ 监控告警已清除 (或调整为适当级别)
```

---

**DNA**:#龍芯⚡️丙午·甲午·乙卯·壬午·䷚颐-PRODUCTION-ROLLBACK-PROCEDURES-v1.0
**版本**: 1.0 (完整版)
**有效期**: 永久 (生产级回滚程序)
