# 🐉 龍魂系統 生產部署指南 v1.0

## 概述

本指南詳述如何使用 `production_deployment.py` 將龍魂系統部署至生產環境。

**DNA**: `#龍芯⚡️2026-06-08-PRODUCTION-DEPLOYMENT-GUIDE-v1.0`

---

## 系統需求

### 基礎設施
- **計算**: 最少 4 核 CPU、8GB RAM （推薦 8 核、16GB）
- **存儲**: 最少 100GB 可用磁盤空間
- **網絡**: 穩定的互聯網連接、HTTPS 支持
- **容器化**: Docker 20.10+ 或 Kubernetes 1.24+

### 外部服務
- **數據庫**: PostgreSQL 12+ 或 MySQL 8.0+
- **緩存**: Redis 6.0+ 或 Memcached
- **監控**: Datadog/New Relic/Prometheus
- **日誌**: Elasticsearch/Splunk/Cloudwatch
- **密鑰管理**: HashiCorp Vault 或 AWS Secrets Manager

### 軟件依賴
```bash
Python 3.11+
Docker 20.10+
kubectl 1.24+ (如使用 Kubernetes)
git 2.30+
```

---

## 部署前準備清單

### 1. 配置準備

- [ ] 準備生產數據庫憑證
- [ ] 配置 Redis/Memcached 端點
- [ ] 獲取有效的 SSL/TLS 證書
- [ ] 配置監控和日誌聚合服務
- [ ] 設置 API 密鑰和認證密鑰
- [ ] 準備備份和恢復計劃

### 2. 環境準備

- [ ] 配置防火牆規則
- [ ] 設置負載均衡器
- [ ] 配置 DNS 記錄
- [ ] 準備藍綠環境（兩套獨立的生產環境）
- [ ] 驗證網絡連接和延遲

### 3. 安全檢查

- [ ] 進行安全掃描（OWASP Top 10）
- [ ] 驗證 SSL/TLS 配置
- [ ] 測試認證和授權機制
- [ ] 配置日誌審計
- [ ] 準備應急事件響應計劃

### 4. 測試準備

- [ ] 準備煙霧測試清單
- [ ] 配置健康檢查端點
- [ ] 準備回滾計劃
- [ ] 進行壓力測試
- [ ] 驗證監控和告警

---

## 生產配置

### 配置模板

```python
prod_config = {
    # API 配置
    "environment": "production",
    "api_host": "api.longhun.example.com",
    "api_port": 8443,

    # 數據庫配置
    "db_host": "prod-postgresql.example.com",
    "db_port": 5432,
    "db_name": "longhun_production",
    "db_user": "longhun_app",
    "db_password": "***",  # 使用 Vault 注入

    # 緩存配置
    "redis_host": "prod-redis.example.com",
    "redis_port": 6379,

    # 監控和日誌
    "monitoring_service": "datadog",        # 或 new-relic, prometheus
    "log_aggregation": "elasticsearch",     # 或 splunk, cloudwatch

    # SSL/TLS 配置
    "ssl_cert_path": "/etc/ssl/certs/longhun-prod.crt",
    "ssl_key_path": "/etc/ssl/private/longhun-prod.key",

    # 備份配置
    "backup_location": "/var/backups/longhun",

    # 部署配置
    "deployment_strategy": "blue-green",    # 或 rolling, canary
    "canary_percentage": 5,                 # 金絲雀部署比例
    "max_concurrent_connections": 10000,

    # Skills 配置
    "skills_enabled": 10,
}
```

### 環境變量

```bash
export LONGHUN_ENV=production
export LONGHUN_DB_HOST=prod-postgresql.example.com
export LONGHUN_DB_PORT=5432
export LONGHUN_DB_NAME=longhun_production
export LONGHUN_DB_USER=longhun_app
export LONGHUN_DB_PASSWORD=<from-vault>
export LONGHUN_REDIS_HOST=prod-redis.example.com
export LONGHUN_REDIS_PORT=6379
export LONGHUN_API_HOST=api.longhun.example.com
export LONGHUN_API_PORT=8443
export LONGHUN_MONITORING=datadog
export LONGHUN_LOG_AGGREGATION=elasticsearch
```

---

## 部署步驟

### 第一階段：部署前準備 (15-30 分鐘)

```bash
# 1. 克隆倉庫
git clone https://github.com/UID9622/longhun-system.git
cd longhun-system

# 2. 檢查部署前條件
python3 deployment/production_deployment.py --pre-check

# 3. 備份現有環境
./deployment/backup.sh

# 4. 驗證配置
python3 deployment/production_deployment.py --validate-config
```

### 第二階段：藍綠部署 (30-60 分鐘)

```bash
# 1. 啟動部署
python3 deployment/production_deployment.py \
  --config=prod_config.json \
  --strategy=blue-green

# 2. 監控部署進度
tail -f /var/log/longhun/deployment.log

# 3. 驗證綠色環境
curl -k https://api.longhun.example.com:8443/health

# 4. 執行煙霧測試
bash deployment/smoke_tests.sh

# 5. 逐步遷移流量
# 10% → 25% → 50% → 75% → 100%
```

### 第三階段：驗證和監控 (24 小時)

```bash
# 1. 監控指標
# 打開 Grafana/Datadog 儀表板

# 2. 檢查日誌
curl https://elasticsearch.example.com/longhun/_search

# 3. 驗證所有端點
bash deployment/endpoint_verification.sh

# 4. 檢查性能基準
curl https://api.longhun.example.com:8443/api/v1/metrics
```

---

## 部署流程詳解

### 步驟 1: 部署前檢查 (3-5 分鐘)
```
✅ 配置驗證 - 檢查所有必要參數
✅ SSL 證書驗證 - 驗證證書有效性和有效期
✅ 密鑰管理檢查 - 確保所有密鑰已安全配置
✅ 檔案權限檢查 - 驗證所有文件權限正確
```

### 步驟 2: 數據庫遷移 (5-10 分鐘)
```
✅ 數據庫備份 - 完整備份現有數據
✅ 數據庫連接 - 驗證連接和權限
✅ 執行遷移 - 運行所有數據庫遷移指令碼
✅ 數據驗證 - 驗證數據完整性和一致性
```

### 步驟 3: 安全加固 (5-10 分鐘)
```
✅ 防火牆規則 - 配置入站和出站規則
✅ CORS 配置 - 限制允許的源
✅ 速率限制 - 配置 API 速率限制
✅ 審計日誌 - 啟用所有 API 調用日誌
```

### 步驟 4: 藍綠部署 (10-20 分鐘)
```
✅ 構建綠色環境 - 構建新 Docker 鏡像
✅ 啟動綠色實例 - 啟動 3 個綠色環境實例
✅ 烟霧測試 - 運行基本功能測試
✅ 流量遷移 - 逐步將流量轉移至綠色
✅ 藍色待命 - 保持藍色環境以備回滾
```

### 步驟 5: 健康驗證 (5-10 分鐘)
```
✅ 性能檢查 - 驗證響應時間、吞吐量、延遲
✅ 端點驗證 - 測試所有主要 API 端點
✅ 數據庫檢查 - 驗證數據庫連接和性能
✅ 快取檢查 - 驗證 Redis/Memcached 正常運行
```

### 步驟 6: 監控激活 (5-10 分鐘)
```
✅ 監控服務集成 - 連接 Datadog/Prometheus
✅ 告警規則配置 - 配置 6 個關鍵告警
✅ 日誌聚合 - 配置 Elasticsearch/Splunk
✅ 分布式追踪 - 啟用 APM (Jaeger)
✅ 實時儀表板 - 部署 Grafana 儀表板
```

### 步驟 7: 部署後處理 (5-10 分鐘)
```
✅ 部署記錄 - 記錄部署詳情和指標
✅ 通知利益相關者 - 發送 Slack 通知、更新 JIRA
✅ 文檔更新 - 更新 runbook 和文檔
```

---

## 性能期望

### 部署指標
| 指標 | 值 | 目標 |
| --- | --- | --- |
| 部署耗時 | 30-60 分鐘 | <90 分鐘 |
| 健康檢查通過率 | 100% | ≥95% |
| API 響應時間 | 15-20ms | <100ms |
| API 吞吐 | 77.8 req/s | ≥50 req/s |
| 可用性 | 99.95% | ≥99.9% |

### 資源消耗
| 資源 | 消耗 | 限制 |
| --- | --- | --- |
| CPU | 8-10% | <50% |
| 內存 | 35-40% | <80% |
| 磁盤 I/O | 低 | <70% |
| 網絡帶寬 | 低 | <50% |

---

## 回滾程序

### 快速回滾（<5 分鐘）
```bash
# 方法 1: Kubernetes 回滾
kubectl rollout undo deployment/longhun-prod

# 方法 2: 藍綠回滾
# 將流量從綠色環境轉回藍色環境
./deployment/switch_traffic_to_blue.sh

# 方法 3: 檢查回滾狀態
kubectl rollout status deployment/longhun-prod
```

### 完全回滾（數據庫）
```bash
# 1. 停止應用
kubectl scale deployment/longhun-prod --replicas=0

# 2. 恢復數據庫備份
mysql longhun_production < /var/backups/longhun/backup_2026-06-08.sql

# 3. 重啟應用
kubectl scale deployment/longhun-prod --replicas=3

# 4. 驗證
curl -k https://api.longhun.example.com:8443/health
```

---

## 監控和告警

### Grafana 儀表板
```
https://grafana.longhun.example.com/d/prod-overview
```

### 關鍵指標
- **API 響應時間** - P95 <100ms
- **錯誤率** - <1%
- **數據庫連接** - <80%
- **CPU 使用** - <50%
- **內存使用** - <80%
- **磁盤空間** - >10% 可用

### 告警規則
| 告警 | 閾值 | 動作 |
| --- | --- | --- |
| 錯誤率 | >1% | 立即通知運維 |
| 響應時間 | P95 >500ms | 通知 SRE 團隊 |
| DB 連接 | >80% | 警告 |
| 磁盤空間 | <10% | 警告 |
| SSL 證書 | 30 天內過期 | 通知 |

---

## 故障排查

### 部署失敗
```bash
# 1. 檢查日誌
tail -f /var/log/longhun/deployment.log

# 2. 驗證配置
python3 -c "import json; json.load(open('prod_config.json'))"

# 3. 檢查先決條件
ping prod-postgresql.example.com
redis-cli -h prod-redis.example.com ping

# 4. 回滾
kubectl rollout undo deployment/longhun-prod
```

### 高錯誤率
```bash
# 1. 檢查應用日誌
kubectl logs -f deployment/longhun-prod

# 2. 檢查數據庫連接
mysql -h prod-postgresql.example.com -u longhun_app -p

# 3. 檢查快取
redis-cli -h prod-redis.example.com INFO stats

# 4. 如需要，進行回滾
kubectl rollout undo deployment/longhun-prod
```

### 性能下降
```bash
# 1. 檢查 CPU/內存使用
kubectl top pods -l app=longhun-prod

# 2. 檢查數據庫性能
EXPLAIN SELECT ...;

# 3. 檢查快取命中率
redis-cli -h prod-redis.example.com INFO stats

# 4. 水平擴展
kubectl scale deployment/longhun-prod --replicas=5
```

---

## 最佳實踐

### 部署前
- ✅ 在 Staging 環境中完全測試部署流程
- ✅ 準備詳細的回滾計劃
- ✅ 通知所有利益相關者
- ✅ 安排在低流量時段進行部署

### 部署期間
- ✅ 持續監控關鍵指標
- ✅ 準備好立即回滾
- ✅ 與團隊保持溝通
- ✅ 遵循部署檢查清單

### 部署後
- ✅ 監控 24 小時
- ✅ 驗證所有功能
- ✅ 收集性能數據
- ✅ 更新文檔和 runbook

---

## 聯繫和支援

- **部署問題**: 聯繫 SRE 團隊
- **應用問題**: 聯繫開發團隊
- **安全問題**: 聯繫安全團隊
- **監控問題**: 聯繫運維團隊

---

## 相關文件

- `demo_staging_deployment.py` - Staging 部署引擎
- `production_deployment.py` - 生產部署引擎
- `backup.sh` - 備份指令碼
- `smoke_tests.sh` - 烟霧測試
- `endpoint_verification.sh` - 端點驗證

---

**DNA**: `#龍芯⚡️2026-06-08-PRODUCTION-DEPLOYMENT-GUIDE-v1.0`
**確認**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
