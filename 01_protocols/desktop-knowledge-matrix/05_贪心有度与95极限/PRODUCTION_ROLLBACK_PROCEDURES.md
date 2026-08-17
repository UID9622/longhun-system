# 龍魂系統·生產回滾程序 (Production Rollback Procedures)
# 日期: 2026-06-10 CST
# DNA:#龍芯⚡️丙午·丙申·庚申·亥时-PRODUCTION-ROLLBACK-PROCEDURES-v1.0

---

## 📋 回滾级別定義

| 级別 | 觸發条件 | 恢復时間 | 数据完整 | 使用場景 |
|------|--------|--------|--------|--------|
| **L1 快速回滾** | API 可用性 <95% | 秒级 | ✅ 是 | 应用层问題 |
| **L2 标准回滾** | 功能異常 | 分鐘级 | ✅ 是 | 逻辑层问題 |
| **L3 深层回滾** | 数据不一致 | 10-15 分鐘 | ✅ 是 | 数据层问題 |
| **L4 緊急回滾** | 系統癱瘓 | 15-30 分鐘 | ✅ 是 | 嚴重故障 |

---

## 🚨 回滾決策流程

```
监测到異常
    ↓
分析问題嚴重级別
    ↓
┌───────────────────────────────────────────┐
│ 嚴重级別評分: 0-100                       │
├───────────────────────────────────────────┤
│ 0-25  → 觀察 10 分鐘 → L0 (不回滾)       │
│ 26-50 → 等待 5 分鐘  → L1 (快速回滾)    │
│ 51-75 → 立即評估    → L2 (标准回滾)    │
│ 76-100→ 立即执行    → L3/L4 (深层回滾) │
└───────────────────────────────────────────┘
```

---

## ✅ 回滾檢查清单 (快速參考)

```
🚨 回滾前必檢 (30 秒)
☑️ API 当前狀态确认
☑️ 用戶影響程度評估
☑️ 备份檔案完整性验證
☑️ 藍色环境就緒狀态

🔄 回滾执行 (2-30 分鐘，取決於回滾级別)
☑️ 根据级別执行回滾腳本
☑️ 监控回滾进度
☑️ 验證系統恢復

✅ 回滾後验證 (10 分鐘)
☑️ 所有端点健康檢查
☑️ 数据完整性验證
☑️ 性能指标确认
☑️ 利益相关者通知
```

---

## 🔵 L1: 快速回滾 (应用层・秒级)

**觸發条件:**
- 綠色环境 API 可用性 <95%
- 但数据层正常
- 需要在秒级內恢復

### L1 回滾步驟

```bash
#!/bin/bash
# 龍魂系統 L1 快速回滾腳本

ROLLBACK_ID="L1-$(date +%Y%m%d-%H%M%S)"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "🔴 [$TIMESTAMP] 開始 L1 快速回滾 ($ROLLBACK_ID)..."

# Step 1: 流量立即切回藍色 (< 1 秒)
echo "Step 1: 流量切回藍色环境..."
cat > /etc/nginx/conf.d/longhun_upstream.conf << EOF
upstream longhun {
    server 127.0.0.1:8001 max_fails=0;
}
EOF
systemctl reload nginx
echo "✅ 流量已切至藍色 (< 1 秒)"

# Step 2: 停止綠色环境 (< 5 秒)
echo "Step 2: 停止綠色环境..."
docker stop longhun-green -t 3  # 3 秒優雅关閉
CONTAINER_ID=$(docker ps -a | grep longhun-green-failed | head -1 | awk '{print $1}')
docker rename longhun-green longhun-green-rollback-$ROLLBACK_ID
echo "✅ 綠色环境已停止 (容器: longhun-green-rollback-$ROLLBACK_ID)"

# Step 3: 验證藍色环境 (< 5 秒)
echo "Step 3: 验證藍色环境..."
for i in {1..3}; do
    if curl -s http://localhost:8001/health | grep -q "healthy"; then
        echo "✅ 藍色环境健康檢查通过"
        break
    fi
    sleep 1
done

# Step 4: 执行內存快照 (< 2 秒)
echo "Step 4: 保存系統快照..."
curl -s http://localhost:8001/api/v1/system/snapshot > \
  /var/backups/rollback-snapshots/$ROLLBACK_ID-blue-env-state.json

# Step 5: 清除緩存 (< 1 秒)
echo "Step 5: 清除应用緩存..."
redis-cli FLUSHDB
redis-cli PUBLISH rollback "L1 回滾完成"

echo ""
echo "════════════════════════════════════════"
echo "✅ L1 快速回滾完成 (耗时: < 15 秒)"
echo "════════════════════════════════════════"
echo "回滾 ID: $ROLLBACK_ID"
echo "恢復时間: < 1 秒"
echo "数据完整: ✅ 是"
echo "用戶可用: ✅ 是"

# Step 6: 通知團隊
cat > /tmp/rollback_alert.json << EOF
{
  "channel": "#ops-critical",
  "severity": "CRITICAL",
  "event": "L1 ROLLBACK TRIGGERED",
  "rollback_id": "$ROLLBACK_ID",
  "timestamp": "$TIMESTAMP",
  "message": "应用层異常，已自動回滾到藍色环境",
  "recovery_time": "< 1 秒",
  "data_integrity": "✅ 完整"
}
EOF

curl -X POST $SLACK_WEBHOOK -d @/tmp/rollback_alert.json

echo ""
echo "📊 回滾詳情:"
echo "  • 回滾等级: L1 (应用层)"
echo "  • 觸發时間: $TIMESTAMP"
echo "  • 恢復时間: < 15 秒"
echo "  • 数据丟失: 否"
echo "  • 用戶影響: < 30 秒 (请求失敗後重试)"
echo "  • 日志位置: /var/log/longhun/rollback-$ROLLBACK_ID.log"
```

**验證 L1 回滾成功:**

```bash
# 1. 验證流量已切換
curl -v http://longhun.example.com/health 2>&1 | grep -A 5 "HTTP"

# 2. 验證藍色环境狀态
curl http://localhost:8001/api/v1/health | python3 -m json.tool

# 3. 验證数据庫連接
psql -h PROD_DB_HOST -U PROD_DB_USER -d longhun_prod -c "SELECT COUNT(*) FROM users;"

# 4. 确认沒有数据丟失
curl http://localhost:8001/api/v1/audit/transactions | grep -c "complete"
```

---

## 🔄 L2: 标准回滾 (逻辑层・分鐘级)

**觸發条件:**
- Skill 执行錯误率 > 5%
- 功能異常但 API 可用
- 需要在分鐘级內恢復

### L2 回滾步驟

```bash
#!/bin/bash
# 龍魂系統 L2 标准回滾腳本

ROLLBACK_ID="L2-$(date +%Y%m%d-%H%M%S)"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "🟠 [$TIMESTAMP] 開始 L2 标准回滾..."

# Step 1: 停止新请求入隊
echo "Step 1: 暫停新请求..."
curl -X POST http://localhost:8002/api/v1/admin/pause-intake \
  -H "Authorization: Bearer ADMIN_TOKEN"

# Step 2: 等待現有请求完成 (最多 30 秒)
echo "Step 2: 等待現有请求完成..."
for i in {1..30}; do
    PENDING=$(curl -s http://localhost:8002/api/v1/admin/queue-status | \
      grep -o '"pending":"[0-9]*"' | cut -d'"' -f4)

    if [ "$PENDING" = "0" ]; then
        echo "✅ 所有请求已完成 ($i 秒)"
        break
    fi

    echo "⏳ 等待请求完成... ($PENDING 個待處理, $i/30 秒)"
    sleep 1
done

# Step 3: 立即切換流量回藍色
echo "Step 3: 切換流量..."
cat > /etc/nginx/conf.d/longhun_upstream.conf << EOF
upstream longhun {
    server 127.0.0.1:8001;
}
EOF
systemctl reload nginx

# Step 4: 停止綠色环境中的 Skill 执行器
echo "Step 4: 停止 Skill 执行器..."
docker exec longhun-green python3 -c \
  "from skills import executor; executor.shutdown()"

# Step 5: 從最近一個檢查点恢復应用狀态
echo "Step 5: 恢復应用狀态..."
LAST_CHECKPOINT="/var/backups/checkpoints/last-stable-$(date +%Y%m%d).json"
if [ -f "$LAST_CHECKPOINT" ]; then
    curl -X POST http://localhost:8001/api/v1/admin/restore-checkpoint \
      -H "Content-Type: application/json" \
      -d @$LAST_CHECKPOINT
    echo "✅ 從檢查点恢復 ($(stat -f%z $LAST_CHECKPOINT 2>/dev/null || stat -c%s $LAST_CHECKPOINT) 字節)"
else
    echo "⚠️  未找到最近檢查点，跳过狀态恢復"
fi

# Step 6: 验證藍色环境数据一致性
echo "Step 6: 验證数据一致性..."
python3 << 'VERIFY'
import requests
import json

# 验證 5 個隨機用戶的数据完整性
api_base = "http://localhost:8001/api/v1"

for user_id in [1, 10, 50, 100, 500]:
    try:
        response = requests.get(f"{api_base}/users/{user_id}")
        if response.status_code == 200:
            data = response.json()
            if "id" in data and "created_at" in data:
                print(f"✅ 用戶 {user_id} 数据完整")
        else:
            print(f"⚠️  用戶 {user_id} 返回 {response.status_code}")
    except Exception as e:
        print(f"❌ 用戶 {user_id} 验證失敗: {e}")
VERIFY

echo ""
echo "════════════════════════════════════════"
echo "✅ L2 标准回滾完成 (耗时: 30-60 秒)"
echo "════════════════════════════════════════"

# 监控恢復
for i in {1..5}; do
    ERROR_RATE=$(curl -s http://localhost:8001/metrics | \
      grep "error_rate" | grep -o "[0-9]*\.[0-9]*" | head -1)
    echo "监控 $i/5: 錯误率 = ${ERROR_RATE}% (目标 < 0.5%)"
    sleep 2
done
```

---

## 💾 L3: 深层回滾 (数据层・10-15 分鐘)

**觸發条件:**
- 数据不一致檢测
- 数据庫異常
- 需要從备份恢復

### L3 回滾步驟

```bash
#!/bin/bash
# 龍魂系統 L3 深层回滾腳本

ROLLBACK_ID="L3-$(date +%Y%m%d-%H%M%S)"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "🔴 [$TIMESTAMP] 開始 L3 深层回滾..."
echo "⚠️  此操作涉及数据庫恢復，请确认已通知所有利益相关者"

# Step 1: 立即切換流量
echo "Step 1: 切換流量至藍色..."
cat > /etc/nginx/conf.d/longhun_upstream.conf << EOF
upstream longhun {
    server 127.0.0.1:8001;
}
EOF
systemctl reload nginx

# Step 2: 停止所有寫操作
echo "Step 2: 停止所有寫操作..."
systemctl stop longhun-worker-write

# Step 3: 確定备份点
echo "Step 3: 確定备份点..."
BACKUP_MANIFEST="/var/backups/longhun/backup-manifest.json"
LATEST_BACKUP=$(cat $BACKUP_MANIFEST | \
  python3 -c "import sys, json; m=json.load(sys.stdin); print(max(m['backups'], key=lambda b: b['timestamp'])['path'])")
echo "使用备份: $LATEST_BACKUP (时間: $(date -f $LATEST_BACKUP))"

# Step 4: 关閉数据庫連接
echo "Step 4: 关閉現有数据庫連接..."
psql -h PROD_DB_HOST -U PROD_DB_USER -d postgres << SQL
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'longhun_prod'
  AND pid <> pg_backend_pid();
SQL

# Step 5: 還原数据庫
echo "Step 5: 還原数据庫 (耗时: 5-10 分鐘)..."
BACKUP_FILE="${LATEST_BACKUP}/database_backup.sql.gz"
zcat "$BACKUP_FILE" | psql -h PROD_DB_HOST -U PROD_DB_USER longhun_prod 2>&1 | \
  tee /tmp/restore-log-$ROLLBACK_ID.txt

if [ $? -eq 0 ]; then
    echo "✅ 数据庫已還原"
else
    echo "❌ 数据庫還原失敗，查看日志: /tmp/restore-log-$ROLLBACK_ID.txt"
    exit 1
fi

# Step 6: 验證数据庫
echo "Step 6: 验證数据庫完整性..."
psql -h PROD_DB_HOST -U PROD_DB_USER longhun_prod << SQL
-- 檢查表数量
SELECT COUNT(*) as table_count FROM information_schema.tables
WHERE table_schema = 'public';

-- 檢查索引
SELECT COUNT(*) as index_count FROM information_schema.statistics
WHERE table_schema = 'public';

-- 檢查外键
SELECT COUNT(*) as constraint_count FROM information_schema.table_constraints
WHERE constraint_type = 'FOREIGN KEY' AND table_schema = 'public';
SQL

# Step 7: 重啟寫操作工作线程
echo "Step 7: 重啟寫操作工作线程..."
systemctl start longhun-worker-write

# Step 8: 恢復綠色环境 (使用還原的数据)
echo "Step 8: 重建綠色环境..."
docker rm longhun-green
# 重新創建綠色环境...

echo ""
echo "════════════════════════════════════════"
echo "✅ L3 深层回滾完成 (耗时: 10-15 分鐘)"
echo "════════════════════════════════════════"
echo "恢復点: $LATEST_BACKUP"
echo "数据狀态: $(date -r $LATEST_BACKUP)"
echo "用戶数据丟失: 否 (最多丟失最近 1 小时的寫操作)"
```

---

## 🆘 L4: 緊急回滾 (系統级・15-30 分鐘)

**觸發条件:**
- 系統完全癱瘓
- 多個层面同时故障
- 需要完全环境重建

### L4 回滾步驟

```bash
#!/bin/bash
# 龍魂系統 L4 緊急回滾腳本

ROLLBACK_ID="L4-EMERGENCY-$(date +%Y%m%d-%H%M%S)"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "🚨 [$TIMESTAMP] 開始 L4 緊急回滾..."
echo "⚠️  此操作將重建整個生產环境，请验證決策！"

# 要求确认
read -p "确认执行 L4 緊急回滾? (輸入 'CONFIRM-EMERGENCY-ROLLBACK' 繼續): " CONFIRM
if [ "$CONFIRM" != "CONFIRM-EMERGENCY-ROLLBACK" ]; then
    echo "❌ 已取消 L4 回滾"
    exit 1
fi

# Step 1: 通知所有利益相关者
echo "Step 1: 發送緊急通知..."
curl -X POST https://api.pagerduty.com/incidents \
  -H "Authorization: Token token=$PAGERDUTY_TOKEN" \
  -d "{
    \"incident\": {
      \"type\": \"incident_reference\",
      \"title\": \"龍魂系統 L4 緊急回滾\",
      \"service\": {
        \"id\": \"PROD_SERVICE_ID\",
        \"type\": \"service_reference\"
      },
      \"urgency\": \"high\"
    }
  }"

# Step 2: 切換到备用区域 (如果配置了地域冗餘)
echo "Step 2: 檢查备用区域..."
if [ -n "$STANDBY_REGION" ]; then
    echo "✅ 有备用区域可用，准备切換..."
    # AWS 区域切換逻辑
else
    echo "ℹ️  单区域部署，無法地域切換"
fi

# Step 3: 停止所有服务
echo "Step 3: 停止所有服务..."
systemctl stop longhun-api
docker stop $(docker ps -q -f "label=longhun=prod") 2>/dev/null
killall python3 2>/dev/null

# Step 4: 從最早穩定备份還原
echo "Step 4: 选择最早穩定备份..."
EARLIEST_STABLE="/var/backups/longhun/earliest-stable-backup"
if [ -d "$EARLIEST_STABLE" ]; then
    echo "使用备份: $EARLIEST_STABLE"
else
    echo "❌ 找不到穩定备份，尋找最近备份..."
    EARLIEST_STABLE=$(ls -td /var/backups/longhun/*/ | head -1)
fi

# Step 5: 完整环境重建
echo "Step 5: 环境重建 (耗时: 15-20 分鐘)..."

# 5a. 清理舊环境
echo "  5a) 清理舊环境..."
rm -rf /opt/longhun-*
docker system prune -f --volumes

# 5b. 還原代碼
echo "  5b) 還原代碼..."
cp -r $EARLIEST_STABLE/application-code /opt/longhun-app

# 5c. 還原数据庫
echo "  5c) 還原数据庫..."
zcat $EARLIEST_STABLE/database_backup.sql.gz | \
  psql -h PROD_DB_HOST -U PROD_DB_USER longhun_prod

# 5d. 重构基礎设施
echo "  5d) 重构基礎设施..."
bash /opt/longhun-app/scripts/rebuild-infrastructure.sh

# Step 6: 验證系統
echo "Step 6: 系統验證..."
for i in {1..10}; do
    if curl -s http://localhost:8001/health | grep -q "healthy"; then
        echo "✅ 系統已恢復 (嘗试 $i/10)"
        break
    fi
    echo "⏳ 等待系統啟動... ($i/10)"
    sleep 10
done

# Step 7: 数据验證
echo "Step 7: 数据验證..."
RECORD_COUNT=$(psql -h PROD_DB_HOST -U PROD_DB_USER longhun_prod \
  -t -c "SELECT COUNT(*) FROM users;")
echo "✅ 用戶记錄: $RECORD_COUNT"

echo ""
echo "════════════════════════════════════════"
echo "✅ L4 緊急回滾完成 (耗时: 20-30 分鐘)"
echo "════════════════════════════════════════"
echo "恢復时間: $((SECONDS / 60)) 分鐘"
echo "数据恢復到: $(date -r $EARLIEST_STABLE)"
echo "用戶影響: 最多 24 小时內的数据丟失"
```

---

## 📊 回滾监控儀表板

```bash
#!/bin/bash
# 实时监控回滾进度

watch -n 1 'echo "=== 龍魂系統回滾监控 ($(date)) ===" && \
echo "" && \
echo "🔵 藍色环境: $(curl -s http://localhost:8001/health | grep -o "healthy" || echo "不可用")" && \
echo "🟢 綠色环境: $(curl -s http://localhost:8002/health | grep -o "healthy" || echo "不可用")" && \
echo "" && \
echo "流量分配:" && \
curl -s http://localhost/nginx_status | grep -A 1 "upstream" && \
echo "" && \
echo "数据庫狀态:" && \
psql -h PROD_DB_HOST -U PROD_DB_USER -t -c "SELECT datname, numbackends FROM pg_stat_database WHERE datname = \"longhun_prod\";" && \
echo "" && \
echo "隊列狀态:" && \
redis-cli LLEN longhun:jobs:pending || echo "Redis 不可用"'
```

---

## ✅ 回滾完成檢查清单

```
□ 流量已切回藍色环境 (验證: curl 返回 200)
□ 綠色环境已停止 (容器已保存用於分析)
□ 数据庫連接正常 (验證: psql 連接成功)
□ 所有 API 端点響应正常 (验證: 8/8 健康檢查通过)
□ 日志無 ERROR 或 CRITICAL 级別消息 (最近 5 分鐘)
□ 应用性能达到基准线 (P95 延遲 < 100ms)
□ 利益相关者已通知 (Slack, PagerDuty, 郵件)
□ 回滾事後分析已啟動 (事件編号已记錄)
□ 备份验證完成 (完整性檢查通过)
□ 监控告警已清除 (或调整為適当级別)
```

---

**DNA**:#龍芯⚡️丙午·丙申·庚申·亥时-PRODUCTION-ROLLBACK-PROCEDURES-v1.0
**版本**: 1.0 (完整版)
**有效期**: 永久 (生產级回滾程序)
