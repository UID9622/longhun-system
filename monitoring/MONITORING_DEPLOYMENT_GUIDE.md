# 🐉 龍魂系統監控部署指南

**DNA**:#龍芯⚡️2026-06-08-MONITORING-DEPLOYMENT-FILE1-v1.0
**確認**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

---

## 📋 目錄

1. [快速開始](#快速開始)
2. [核心指標](#核心指標-8-個)
3. [SLO 定義](#slo-定義-4-個)
4. [告警規則](#告警規則-8-個)
5. [部署步驟](#部署步驟)
6. [驗證和測試](#驗證和測試)

---

## 快速開始

### 環境需求

```bash
# 安裝 Datadog Agent
DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=$DATADOG_API_KEY DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_mac_os.sh)"

# 驗證 Agent 運行
sudo launchctl list | grep datadog
```

### 3 步部署

```bash
# 1. 應用 Prometheus 規則
kubectl apply -f prometheus_rules.yaml -n longhun-prod

# 2. 部署 Grafana 儀表板
curl -X POST http://grafana:3000/api/dashboards/db \
  -H "Authorization: Bearer $GRAFANA_API_KEY" \
  -H "Content-Type: application/json" \
  -d @grafana_dashboard_config.json

# 3. 配置 Datadog 告警
python3 datadog_monitoring_config.py | jq . | \
  curl -X POST https://api.datadoghq.com/api/v1/monitor \
    -H "Authorization: Bearer $DATADOG_API_KEY" \
    -d @-
```

---

## 核心指標 (8 個)

### 1️⃣ API 響應時間
**指標**: `api.response_time` | **單位**: milliseconds

```
P50: ~50ms (快速路徑)
P95: ≤ 500ms (SLO 目標)
P99: ≤ 1000ms (可接受)

告警閾值:
  ⚠️ P95 > 500ms (10 分鐘) → Warning
  🔴 P95 > 1000ms (5 分鐘) → Critical
```

### 2️⃣ API 吞吐量
**指標**: `api.request_rate` | **單位**: req/s

```
目標: 77.8 req/s (基線)
範圍: 50-150 req/s (正常)

告警閾值:
  ⚠️ < 50 req/s → 檢查故障
  ⚠️ > 150 req/s → 檢查異常流量
```

### 3️⃣ 錯誤率
**指標**: `api.error_rate` | **單位**: percent

```
目標: < 0.1% (SLO)
警告: > 1%

告警閾值:
  ⚠️ > 1% (5 分鐘)
  🔴 > 5% (2 分鐘)
```

### 4️⃣ 數據庫連接池
**指標**: `db.pool.usage` | **單位**: percent

```
配置: 20 個連接
警告: > 80%
臨界: > 90%

告警閾值:
  ⚠️ > 80% (10 分鐘)
  🔴 > 90% (2 分鐘)
```

### 5️⃣ Redis 快取命中率
**指標**: `cache.hit_rate` | **單位**: percent

```
目標: 92%
可接受: > 80%

告警閾值:
  ⚠️ < 80% (10 分鐘)
```

### 6️⃣ CPU 使用率
**指標**: `system.cpu.user` | **單位**: percent

```
正常: < 40%
警告: > 60%
臨界: > 80%

告警閾值:
  ⚠️ > 80% (10 分鐘)
```

### 7️⃣ 內存使用率
**指標**: `system.mem.pct_usable` | **單位**: percent

```
正常: < 40%
警告: > 60%
臨界: > 80%

告警閾值:
  ⚠️ < 20% 可用 (10 分鐘)
```

### 8️⃣ 磁盤使用率
**指標**: `system.disk.used` | **單位**: percent

```
正常: < 70%
警告: > 75%
臨界: > 85%

告警閾值:
  ⚠️ > 85% (10 分鐘)
  🔴 < 10% 可用 (1 分鐘)
```

---

## SLO 定義 (4 個)

### 📌 可用性 SLO
```
名稱:   整體系統可用性
目標:   99.95%
計算:   (成功請求 / 所有請求) × 100
窗口:   滾動 30 天
告警:   < 99.95% 持續 5 分鐘
```

### 📌 延遲 SLO
```
名稱:   API P95 響應時間
目標:   ≤ 500ms
計算:   histogram_quantile(0.95, ...)
窗口:   滾動 7 天
告警:   > 500ms 持續 10 分鐘
```

### 📌 錯誤率 SLO
```
名稱:   API 錯誤率
目標:   ≤ 0.1%
計算:   (錯誤 / 所有請求) × 100
窗口:   滾動 7 天
告警:   > 0.1% 持續 5 分鐘
```

### 📌 吞吐量 SLO
```
名稱:   最小請求吞吐量
目標:   ≥ 50 req/s
計算:   rate(requests_total[1m])
窗口:   滾動 1 小時
告警:   < 50 req/s 持續 5 分鐘
```

---

## 告警規則 (8 個)

### 🔴 Critical Alerts (需要立即響應)

**1. 高錯誤率**
```
條件: error_rate > 1%
持續: 5 分鐘
通知: Slack + PagerDuty
行動: 檢查應用日誌，可能需要回滾
```

**2. 數據庫連接池耗盡**
```
條件: db.pool.usage > 90%
持續: 2 分鐘
通知: Slack + PagerDuty
行動: 檢查 DB 連接洩漏，可能需要重啟 app
```

**3. 磁盤空間臨界**
```
條件: disk_available < 10%
持續: 1 分鐘
通知: Slack + PagerDuty
行動: 清理日誌，擴展磁盤
```

### 🟡 Warning Alerts (需要關注)

**4. API 延遲高**
```
條件: api.latency_p95 > 500ms
持續: 10 分鐘
通知: Slack
行動: 檢查慢查詢，優化代碼
```

**5. 內存使用率高**
```
條件: memory_usage > 80%
持續: 10 分鐘
通知: Slack
行動: 檢查內存洩漏，考慮重啟
```

**6. CPU 使用率高**
```
條件: cpu_usage > 80%
持續: 10 分鐘
通知: Slack
行動: 檢查消耗 CPU 的進程
```

**7. 快取命中率低**
```
條件: cache_hit_rate < 80%
持續: 10 分鐘
通知: Slack
行動: 檢查快取配置，考慮增加快取大小
```

**8. Kimi API 延遲高**
```
條件: kimi_latency > 5000ms
持續: 5 分鐘
通知: Slack
行動: 檢查 Kimi API 狀態，使用本地推理
```

---

## 部署步驟

### Phase 1: 準備工作 (15 分鐘)

```bash
# 1. 檢查環境
kubectl get nodes
kubectl get pods -n longhun-prod

# 2. 驗證存儲和權限
ls -la monitoring/
kubectl auth can-i create configmaps -n longhun-prod

# 3. 備份現有配置
cp -r /etc/prometheus /etc/prometheus.backup
cp -r /etc/grafana /etc/grafana.backup
```

### Phase 2: 應用 Prometheus 規則 (10 分鐘)

```bash
# 1. 驗證語法
promtool check rules prometheus_rules.yaml

# 2. 應用規則
kubectl apply -f prometheus_rules.yaml -n longhun-prod

# 3. 重新加載 Prometheus
kubectl rollout restart prometheus -n longhun-prod

# 4. 驗證規則已加載
curl http://prometheus:9090/api/v1/rules | jq '.data.groups[].rules | length'
```

### Phase 3: 部署 Grafana 儀表板 (15 分鐘)

```bash
# 1. 獲取 Grafana API Token
GRAFANA_TOKEN=$(kubectl exec -n longhun-prod -it deploy/grafana -- \
  grafana-cli admin create-api-token --name "deploy" --role Admin)

# 2. 導入儀表板配置
curl -X POST http://grafana:3000/api/dashboards/db \
  -H "Authorization: Bearer $GRAFANA_TOKEN" \
  -H "Content-Type: application/json" \
  -d @grafana_dashboard_config.json

# 3. 驗證儀表板已創建
curl http://grafana:3000/api/search?query=longhun
```

### Phase 4: 配置 Datadog (10 分鐘)

```bash
# 1. 驗證環境變數
echo $DATADOG_API_KEY
echo $DATADOG_APP_KEY

# 2. 生成監控配置
python3 datadog_monitoring_config.py

# 3. 部署 Datadog Agent ConfigMap
kubectl create configmap datadog-config \
  --from-file=datadog.yaml \
  -n longhun-prod

# 4. 重啟 Datadog Agent
kubectl rollout restart daemonset/datadog-agent -n longhun-prod
```

### Phase 5: 驗證和測試 (10 分鐘)

```bash
# 1. 驗證告警規則
curl http://prometheus:9090/api/v1/rules

# 2. 驗證儀表板
curl http://grafana:3000/api/dashboards/uid/longhun-prod

# 3. 測試告警通知
# 在 Datadog 或 Prometheus 中觸發測試告警

# 4. 檢查日誌
kubectl logs -n longhun-prod deploy/prometheus -f
kubectl logs -n longhun-prod deploy/grafana -f
```

---

## 驗證和測試

### ✅ 驗收清單

```
□ Prometheus 規則加載成功
  kubectl get rules -n longhun-prod
  結果: ✅ longhun_production 規則集存在

□ Grafana 儀表板創建成功
  curl http://grafana:3000/api/dashboards/uid/longhun-prod
  結果: ✅ HTTP 200 + 儀表板詳情

□ Datadog Agent 連接成功
  curl https://api.datadoghq.com/api/v1/validate
  結果: ✅ "valid": true

□ 告警通知工作
  測試 Slack webhook: curl -X POST $SLACK_WEBHOOK -d '{"text":"Test"}'
  結果: ✅ Slack 頻道收到消息

□ 核心指標可見
  訪問儀表板，檢查所有 8 個指標都有數據
  結果: ✅ 所有面板都顯示數據

□ SLO 被追蹤
  Datadog 中檢查 SLO 儀表板
  結果: ✅ 4 個 SLO 都被計算和跟蹤
```

### 🧪 測試告警

```bash
# 1. 測試 Critical Alert
# 模擬高錯誤率
watch 'curl http://api:8443/api/v1/skills/999/execute; echo'

# 驗證:
# ✅ Slack 收到警報 (2 分鐘內)
# ✅ PagerDuty 創建事件 (2 分鐘內)

# 2. 測試 Warning Alert
# 監控儀表板，應看到 P95 延遲升高
# ✅ Slack 收到警告 (10 分鐘內)

# 3. 驗證告警恢復
# 停止模擬負載
# ✅ Slack 收到恢復通知
```

---

## 監控儀表板訪問

| 服務 | URL | 用戶 |
|------|-----|------|
| Prometheus | http://prometheus:9090 | 無需認証 |
| Grafana | http://grafana:3000 | admin / $GRAFANA_PASSWORD |
| Datadog | https://app.datadoghq.com | 用 SSO 登入 |

---

## 故障排查

### Prometheus 規則無法加載

```bash
# 檢查語法
promtool check rules prometheus_rules.yaml

# 檢查 Prometheus 日誌
kubectl logs -n longhun-prod deploy/prometheus | grep -i error

# 重新應用規則
kubectl delete -f prometheus_rules.yaml
kubectl apply -f prometheus_rules.yaml
```

### Grafana 儀表板無數據

```bash
# 檢查數據源連接
curl http://prometheus:9090/-/healthy

# 檢查 Grafana 日誌
kubectl logs -n longhun-prod deploy/grafana | grep -i datasource

# 測試查詢
curl 'http://prometheus:9090/api/v1/query?query=up'
```

### Datadog 告警無法發送

```bash
# 驗證 API Key
curl -H "DD-API-KEY: $DATADOG_API_KEY" \
  https://api.datadoghq.com/api/v1/validate

# 檢查告警配置
curl -H "Authorization: Bearer $DATADOG_API_KEY" \
  https://api.datadoghq.com/api/v1/monitor | jq '.[] | .name'
```

---

## 相關文檔

- `prometheus_rules.yaml` - Prometheus 告警規則
- `grafana_dashboard_config.json` - Grafana 儀表板配置
- `datadog_monitoring_config.py` - Datadog 配置生成器
- `datadog_monitoring_config.json` - Datadog 配置文件

---

**DNA**:#龍芯⚡️2026-06-08-MONITORING-DEPLOYMENT-GUIDE-v1.0
**最後更新**: 2026-06-08
**版本**: 1.0
