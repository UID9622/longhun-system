# 🐉 龍魂系統·團隊培訓計劃

**DNA**: #龍芯⚡️2026-06-08-TEAM-TRAINING-v1.0
**確認**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**目標讀者**: 運維團隊 / SRE 工程師 / DevOps 工程師
**培訓時長**: 4 小時（分 4 節課）

---

## 📋 課程大綱

| 課程 | 時長 | 講師 | 目標 |
|------|------|------|------|
| 🎯 第 1 課：系統架構和部署概述 | 45 分鐘 | Tech Lead | 全面了解系統設計 |
| 🚀 第 2 課：生產部署演練 | 60 分鐘 | DevOps Lead | 掌握 27 步部署流程 |
| 📊 第 3 課：監控和告警運維 | 45 分鐘 | SRE Lead | 使用監控儀表板 |
| 🔧 第 4 課：故障排查和應急 | 30 分鐘 | Support Lead | 應對常見問題 |

---

## 🎯 第 1 課：系統架構和部署概述（45 分鐘）

### 課程目標
- 理解龍魂系統的核心組件
- 了解 10 個 Skills 的功能
- 掌握藍綠部署策略

### 課程內容

#### 1.1 系統架構概覽（15 分鐘）

```
龍魂系統架構圖
═══════════════════════════════════════════════════════════════

  用戶界面層
  ┌──────────────────────────────────────────────────────────┐
  │  Web UI / API Gateway / Kimi AI 集成                      │
  └──────────────────────────────────────────────────────────┘
                              ↓
  應用層 (10 Skills)
  ┌─────────────┬─────────────┬─────────────┬─────────────┐
  │ Skill-1     │ Skill-2     │ Skill-3     │ Skill-4     │
  │ 算法藝術    │ 品牌指南    │ Canvas設計  │ 文檔協作    │
  ├─────────────┼─────────────┼─────────────┼─────────────┤
  │ Skill-5     │ Skill-6     │ Skill-7     │ Skill-8     │
  │ 內部溝通    │ MCP Builder │ Skill 創建  │ GIF 生成    │
  ├─────────────┼─────────────┼─────────────┼─────────────┤
  │ Skill-9     │ Skill-10    │             │             │
  │ 主題工廠    │ Web 構件    │             │             │
  └─────────────┴─────────────┴─────────────┴─────────────┘
                              ↓
  服務層
  ┌──────────────┬──────────────┬──────────────┬──────────────┐
  │ API 服務     │ 認證服務     │ 日誌服務     │ 監控服務     │
  └──────────────┴──────────────┴──────────────┴──────────────┘
                              ↓
  基礎設施層
  ┌──────────────┬──────────────┬──────────────┬──────────────┐
  │ PostgreSQL   │ Redis Cache  │ Elasticsearch│ Prometheus   │
  │ (持久化)     │ (加速)       │ (日誌)       │ (監控)       │
  └──────────────┴──────────────┴──────────────┴──────────────┘
                              ↓
  特殊集成
  ┌──────────────┬──────────────┐
  │ Kimi AI      │ HashiCorp    │
  │ (推理)       │ Vault (密鑰) │
  └──────────────┴──────────────┘
```

**關鍵數字**:
- 10 個 Skills（120 個規格塊）
- 8 個核心監控指標
- 27 個部署步驟
- 4 個集成模式（Kimi）
- 99.95% 可用性 SLO

#### 1.2 部署策略（15 分鐘）

**藍綠部署流程**:

```
步驟 1: 準備綠色環境
  ┌─────────────────────────────────────────┐
  │ 構建新的 Docker 鏡像                     │
  │ longhun:prod-2026-06-08-v1.0            │
  └─────────────────────────────────────────┘
                      ↓
步驟 2: 啟動綠色實例
  ┌──────────┬──────────┬──────────┐
  │Green-1  │Green-2   │Green-3   │ (3 個副本)
  └──────────┴──────────┴──────────┘
                      ↓
步驟 3: 烟霧測試
  ✓ GET /health
  ✓ GET /api/v1/skills
  ✓ POST /api/v1/skills/1/execute
                      ↓
步驟 4: 流量遷移 (零停機)
  時間   藍色流量    綠色流量
  ─────────────────────────
  T+0     100%        0%
  T+2     90%         10%
  T+4     75%         25%
  T+6     50%         50%
  T+8     25%         75%
  T+10    0%          100%
                      ↓
步驟 5: 藍色待命
  ┌──────────┬──────────┬──────────┐
  │ Blue-1   │ Blue-2   │ Blue-3   │ (隨時回滾)
  └──────────┴──────────┴──────────┘
```

**優勢**:
- ✅ 零停機時間
- ✅ 快速回滾（1-2 分鐘）
- ✅ A/B 測試可能性
- ✅ 資源效率高

#### 1.3 關鍵配置（15 分鐘）

```bash
# 生產配置關鍵參數

## API 配置
API_HOST=api.longhun.example.com
API_PORT=8443
MAX_CONCURRENT_CONNECTIONS=10000
REQUEST_TIMEOUT=30s

## 數據庫配置
DB_TYPE=postgresql
DB_HOST=prod-postgresql.example.com
DB_PORT=5432
DB_NAME=longhun_production
DB_POOL_SIZE=20

## 快取配置
CACHE_TYPE=redis
REDIS_HOST=prod-redis.example.com
REDIS_PORT=6379
REDIS_POOL_SIZE=50
CACHE_TTL=3600s

## 監控配置
MONITORING_SERVICE=datadog
LOG_AGGREGATION=elasticsearch
APM_SERVICE=jaeger

## Kimi AI 集成
KIMI_API_KEY=${KIMI_API_KEY}  # 環境變數方式
KIMI_TIMEOUT=30s
KIMI_MAX_RETRIES=3
```

### 練習題
1. 藍綠部署的流量遷移順序是什麼？
2. 如何在 10 秒內完成流量遷移？
3. 回滾時需要做什麼？

---

## 🚀 第 2 課：生產部署演練（60 分鐘）

### 課程目標
- 執行完整的 27 步部署流程
- 理解每個步驟的目的和檢查點
- 學會從日誌中識別問題

### 課程內容

#### 2.1 部署準備（10 分鐘）

**部署前檢查清單**:

```
□ T-72h: 計劃階段
  □ 選擇部署窗口（低流量時段）
  □ 組建部署團隊（4 個角色）
  □ 審查變更內容
  □ 準備回滾計劃

□ T-24h: 準備階段
  □ 驗證配置
  □ 檢查 SSL 證書
  □ 驗證備份系統
  □ 通知相關人員

□ T-0: 部署階段
  □ 最後確認所有檢查
  □ 啟動監控儀表板
  □ 準備快速通信渠道 (Slack)
  □ 宣布部署開始
```

#### 2.2 27 步部署流程（40 分鐘）

**分為 7 個階段，每個階段 3-4 個步驟**:

**階段 1: 部署前檢查（4 步）**
```
✅ 步驟 1: 配置驗證
   檢查: 所有必要配置是否存在
   通過: 10/10 配置項 ✓

✅ 步驟 2: SSL 證書驗證
   檢查: 證書有效期
   通過: 證書有效直到 2027 年 ✓

✅ 步驟 3: 密鑰管理檢查
   檢查: 密鑰是否已配置
   通過: HashiCorp Vault 中 ✓

✅ 步驟 4: 文件權限檢查
   檢查: 所有路徑的權限
   通過: 所有路徑權限正確 ✓
```

**階段 2: 數據庫遷移（4 步）**
```
✅ 步驟 5: 數據庫備份
   操作: 創建完整備份
   結果: /var/backups/longhun/longhun_prod_20260608_204930.sql

✅ 步驟 6: 數據庫連接
   檢查: 連接到生產數據庫
   結果: 已連接到 longhun_app@prod-postgresql.example.com:5432

✅ 步驟 7: 執行遷移
   操作: 5 個遷移步驟
   ✓ 初始化 Skills 表
   ✓ 創建性能指標表
   ✓ 創建審計日誌表
   ✓ 添加索引優化
   ✓ 啟用複製和高可用

✅ 步驟 8: 數據完整性檢查
   檢查: 所有表和索引
   結果: 完整性驗證通過 ✓
```

**階段 3: 安全加固（4 步）**
```
✅ 步驟 9: 防火牆規則配置
   ✓ HTTP 80 → 重定向到 HTTPS
   ✓ HTTPS 443 → 主要 API 端口
   ✓ SSH 22 → 限制於特定 IP
   ✓ 禁止其他入站
   ✓ 允許出站到監控服務

✅ 步驟 10: CORS 配置
   設置: 只允許 https://longhun.example.com

✅ 步驟 11: 速率限制配置
   ✓ API: 1000 req/min per IP
   ✓ 登入: 10 attempts/15min
   ✓ Skill: 100 req/min per API key

✅ 步驟 12: 審計日誌啟用
   配置: 所有 API 調用都被記錄
```

**階段 4: 藍綠部署（5 步）**
```
✅ 步驟 13: 構建綠色環境
   構建: Docker 鏡像 longhun:prod-2026-06-08-v1.0
   結果: 鏡像構建完成 (100%)

✅ 步驟 14: 啟動綠色實例
   啟動: 3 個副本 (prod-green-1, green-2, green-3)
   結果: 所有 3 個實例已啟動 ✓

✅ 步驟 15: 烟霧測試
   測試:
   ✓ GET /health → 200 OK
   ✓ GET /api/v1/skills → 200 OK
   ✓ POST /api/v1/skills/1/execute → 202 Accepted

✅ 步驟 16: 流量遷移
   進度: 10% → 25% → 50% → 75% → 100%
   結果: 完全切換到綠色環境 (耗時 ~10 秒)

✅ 步驟 17: 藍色待命
   狀態: 舊環境保持運行，隨時可回滾
```

**階段 5: 健康驗證（2 步）**
```
✅ 步驟 18: 執行健康檢查
   檢查:
   ✓ API 響應性 (avg 15.2ms)
   ✓ 數據庫連接 (10/10)
   ✓ Redis 快取 (hit rate 92%)
   ✓ 所有 10 Skills (10/10)
   ✓ SSL/TLS 證書 (valid until 2027)
   ✓ 磁盤空間 (85% available)
   ✓ 內存使用 (<40%)
   ✓ CPU 使用 (<8%)
   結果: 8/8 檢查通過 ✓

✅ 步驟 19: 端點驗證
   驗證:
   ✓ GET /health → 200
   ✓ GET /api/v1/skills → 200
   ✓ GET /api/v1/skills/1 → 200
   ✓ POST /api/v1/skills/1/execute → 202
   ✓ GET /api/v1/metrics → 200
   結果: 5/5 端點響應正常 ✓
```

**階段 6: 監控啟動（4 步）**
```
✅ 步驟 20: 監控服務集成
   連接: Datadog
   狀態: 已連接 ✓

✅ 步驟 21: 告警規則配置
   啟用:
   ✓ Error Rate > 1%
   ✓ Response Time P95 > 500ms
   ✓ Database Connection Pool Exhausted
   ✓ Memory > 80%
   ✓ Disk Space < 10%
   ✓ SSL Certificate Expiring

✅ 步驟 22: 日誌聚合
   連接: Elasticsearch
   狀態: 已連接 ✓

✅ 步驟 23: 分布式追踪
   啟用: Jaeger APM
   狀態: 已啟用 ✓

✅ 步驟 24: 實時儀表板
   工具: Grafana
   狀態: 已部署 ✓
```

**階段 7: 部署後處理（3 步）**
```
✅ 步驟 25: 部署記錄
   記錄: 部署詳情已記錄

✅ 步驟 26: 通知利益相關者
   ✓ Slack 通知 (#deployments)
   ✓ JIRA 狀態更新
   ✓ 報告發送至運營團隊

✅ 步驟 27: 文檔更新
   更新: 部署文檔已更新
```

#### 2.3 實際演練（10 分鐘）

```bash
# 運行完整部署演練
cd ~/longhun-system
python3 deployment/production_deployment.py

# 預期結果:
# ✅ 27/27 步驟通過
# ✅ 8/8 健康檢查通過
# ✅ 部署耗時: ~8 秒 (演示模式)
# ✅ 部署報告已生成
```

### 練習題
1. 如果步驟 15（烟霧測試）失敗怎麼辦？
2. 流量遷移耗時多久？
3. 回滾命令是什麼？

---

## 📊 第 3 課：監控和告警運維（45 分鐘）

### 課程目標
- 使用 Grafana 和 Datadog 監控系統
- 理解 8 個核心指標
- 响應告警並檢查系統狀態

### 課程內容

#### 3.1 監控儀表板使用（20 分鐘）

**訪問儀表板**:

```
Prometheus: http://prometheus:9090
Grafana:    http://grafana:3000 (admin / password)
Datadog:    https://app.datadoghq.com (SSO)
```

**儀表板上的 10 個面板**:

| # | 面板名稱 | 類型 | 目標 |
|---|---------|------|------|
| 1 | API 響應時間 (P50/95/99) | Graph | P95 < 500ms |
| 2 | API 吞吐量 (req/s) | Gauge | 77.8 req/s |
| 3 | 錯誤率 (%) | Stat | < 0.1% |
| 4 | DB 連接池使用 | Gauge | < 90% |
| 5 | Redis 快取命中率 | Stat | > 92% |
| 6 | 服務器資源 (CPU/MEM/DISK) | Multi-Stat | < 80% |
| 7 | 10 個 Skills 狀態 | Table | 全部 OK |
| 8 | Kimi AI 集成狀態 | Card | Connected |
| 9 | 部署歷史 | Table | 最新 3 個 |
| 10 | 告警活動 | Alert List | 實時 |

#### 3.2 8 個核心指標詳解（15 分鐘）

**指標 1: API 響應時間**
```
查詢: histogram_quantile(0.95, api_response_time)
目標: P95 < 500ms
警告: P95 > 500ms (10 分鐘)
臨界: P95 > 1000ms (5 分鐘)
行動: 檢查慢查詢，優化代碼
```

**指標 2: API 吞吐量**
```
查詢: rate(http_requests_total[5m])
基線: 77.8 req/s
警告: < 50 或 > 150 req/s
行動: 檢查異常流量或服務故障
```

**指標 3-8: 其他指標**
(類似的格式，涵蓋 DB、Cache、CPU、Memory、Disk、Kimi)

#### 3.3 告警響應流程（10 分鐘）

**當告警觸發時的操作**:

```
告警觸發
  ↓
收到 Slack 通知
  ↓
打開儀表板 (Grafana 或 Datadog)
  ↓
識別問題類型:
  │
  ├─ 🔴 Critical (需要立即行動)
  │   └─ 高錯誤率 → 檢查應用日誌
  │   └─ DB 連接池滿 → 檢查連接洩漏
  │   └─ 磁盤滿 → 清理日誌，擴展磁盤
  │
  └─ 🟡 Warning (監控並計劃修復)
      └─ 高延遲 → 優化查詢
      └─ 高內存使用 → 檢查洩漏
      └─ 快取命中率低 → 增加快取
  ↓
查詢日誌和追踪:
  kubectl logs -n longhun-prod <pod-name>
  Jaeger: http://jaeger:16686
  ↓
執行修復:
  - 若需要緊急回滾: kubectl rollout undo
  - 若需要重啟: kubectl delete pod <pod-name>
  - 若需要調整配置: kubectl edit deployment
  ↓
確認恢復:
  - 告警清除
  - 指標恢復正常
  - 發送恢復通知
```

### 練習題
1. 如何打開 Grafana 儀表板？
2. 當 P95 延遲超過 500ms 時應該檢查什麼？
3. Kimi API 延遲高時的回退策略是什麼？

---

## 🔧 第 4 課：故障排查和應急（30 分鐘）

### 課程目標
- 快速診斷常見問題
- 執行應急操作
- 進行快速回滾

### 課程內容

#### 4.1 常見故障和診斷（15 分鐘）

**問題 1: 部署後 API 無響應**

```
症狀: GET /health → 連接超時

診斷步驟:
1. 檢查 Pod 狀態
   kubectl get pods -n longhun-prod
   結果: 檢查是否都是 Running 且 Ready

2. 查看 Pod 日誌
   kubectl logs -n longhun-prod <pod-name> --tail=100
   查找: panic, error, exception

3. 檢查資源限制
   kubectl describe pod <pod-name>
   查找: OOMKilled, CrashLoopBackOff

4. 檢查網絡連接
   kubectl exec -it <pod-name> -- curl localhost:8443/health

修復方案:
  Option A: 重啟 Pod
    kubectl delete pod <pod-name>
  Option B: 回滾部署
    kubectl rollout undo deployment/longhun-prod
```

**問題 2: 數據庫連接失敗**

```
症狀: error: "failed to connect to database"

診斷步驟:
1. 檢查數據庫服務狀態
   psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "SELECT 1;"

2. 檢查連接池設置
   SELECT count(*) FROM pg_stat_activity;
   (檢查是否達到 max_connections)

3. 檢查防火牆規則
   nc -zv $DB_HOST 5432

修復方案:
  Option A: 增加連接池大小
    kubectl set env deployment/longhun-prod DB_POOL_SIZE=30
  Option B: 重啟 DB 連接
    kubectl delete pod <db-pod-name>
```

**問題 3: 內存使用率突增**

```
症狀: 內存使用 > 80%，應用變慢

診斷步驟:
1. 使用 Prometheus 查詢
   node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes

2. 檢查 Pod 內存使用
   kubectl top pods -n longhun-prod --sort-by=memory

3. 查看內存分配情況
   kubectl exec <pod-name> -- ps aux

修復方案:
  Option A: 重啟消耗內存的 Pod
    kubectl delete pod <pod-name>
  Option B: 增加內存限制
    kubectl set resources deployment/longhun-prod \
      --limits=memory=8Gi
```

#### 4.2 應急回滾程序（15 分鐘）

**場景: 部署 5 分鐘後發現嚴重問題**

```
步驟 1: 決策 (< 1 分鐘)
  確認問題的嚴重性
  檢查告警儀表板
  與團隊確認是否需要回滾

步驟 2: 執行回滾 (< 2 分鐘)
  命令: kubectl rollout undo deployment/longhun-prod
  驗證: kubectl rollout status deployment/longhun-prod

步驟 3: 驗證恢復 (< 2 分鐘)
  檢查: GET /health → 200 OK
  檢查: 所有 Pod 處於 Running 狀態
  檢查: 指標恢復正常

步驟 4: 通知和分析 (< 5 分鐘)
  發送回滾通知至 Slack
  記錄回滾原因
  安排事後分析會議

總耗時: < 10 分鐘
```

**快速回滾命令參考**:

```bash
# 查看部署歷史
kubectl rollout history deployment/longhun-prod

# 回滾到上一個版本
kubectl rollout undo deployment/longhun-prod

# 回滾到特定版本
kubectl rollout undo deployment/longhun-prod --to-revision=3

# 暫停部署以進行調查
kubectl rollout pause deployment/longhun-prod

# 恢復部署
kubectl rollout resume deployment/longhun-prod

# 監控回滾進度
kubectl rollout status deployment/longhun-prod --watch
```

### 練習題
1. 如果 Pod 處於 CrashLoopBackOff 狀態怎麼辦？
2. 如何快速回滾到上一個工作版本？
3. 回滾需要多久時間？

---

## 📚 附錄：快速參考

### A. 關鍵命令

```bash
# 部署管理
kubectl get deployment -n longhun-prod
kubectl describe deployment longhun-prod -n longhun-prod
kubectl set image deployment/longhun-prod longhun=<new-image>

# Pod 管理
kubectl get pods -n longhun-prod
kubectl logs -n longhun-prod <pod-name>
kubectl exec -it <pod-name> -n longhun-prod -- /bin/bash

# 監控
kubectl top nodes
kubectl top pods -n longhun-prod

# 故障排查
kubectl describe pod <pod-name> -n longhun-prod
kubectl get events -n longhun-prod --sort-by='.lastTimestamp'
```

### B. 關鍵聯繫方式

```
Deployment Lead:  [名稱] [電話] [Slack]
Monitoring Lead:  [名稱] [電話] [Slack]
Database Lead:    [名稱] [電話] [Slack]
Support Lead:     [名稱] [電話] [Slack]

Slack Channel:    #deployment-live
PagerDuty:        longhun-deployment-oncall
```

### C. 重要文檔

- DEPLOYMENT_RUNBOOK_FOR_TEAM.md (1,238 行)
- PRODUCTION_DEPLOYMENT_GUIDE.md
- MONITORING_DEPLOYMENT_GUIDE.md
- KIMI_INTEGRATION_GUIDE.md

---

## 📋 評估和認證

### 培訓評估 (40 分)

```
第 1 課 (10 分): 系統架構理解
  □ 能描述 10 個 Skills
  □ 理解藍綠部署策略
  □ 知道 27 步部署流程

第 2 課 (15 分): 部署演練
  □ 能執行完整部署
  □ 理解每個階段的檢查點
  □ 知道如何驗證部署結果

第 3 課 (10 分): 監控運維
  □ 能讀懂 Grafana 儀表板
  □ 理解 8 個核心指標
  □ 能響應告警

第 4 課 (5 分):  故障排查
  □ 能診斷常見問題
  □ 知道回滾流程
```

### 認證資格

```
及格分數: 32/40 (80%)

通過後可獲得:
  ✅ 龍魂系統部署認證
  ✅ 可獨立執行部署操作
  ✅ 可作為部署團隊成員參與生產部署
```

---

## 後續學習

- Kubernetes 進階管理
- Prometheus/Grafana 自定義配置
- Disaster Recovery 演練
- 性能優化深度課程
- Kimi AI 集成進階

---

**DNA**: #龍芯⚡️2026-06-08-TEAM-TRAINING-v1.0
**最後更新**: 2026-06-08
**版本**: 1.0
**準備者**: Tech Lead
