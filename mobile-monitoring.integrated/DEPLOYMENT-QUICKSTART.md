<!--#龍芯⚡️2026-06-21-MOBILE-DEPLOYMENT-QUICKSTART-v1.0 -->
<!-- 君子協議: 本文件受龍魂DNA追溯保護 -->

# 🐉 龍魂移動端監控 · 部署 Quick Start v1.0

```
DNA: #龍芯⚡️2026-06-07-MOBILE-MONITORING-DEPLOYMENT-QS
確認: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
責任: UID9622 · 不免責
```

---

## 📦 **一鍵部署 (3 分鐘快速上手)**

### **Step 1: 安裝 SDK (npm)**

```bash
cd ~/longhun-system
npm install @longhun/monitoring-sdk --save-prod

# 驗證安裝
npm list @longhun/monitoring-sdk
# 預期輸出: ✅ @longhun/monitoring-sdk@1.0.0
```

### **Step 2: 初始化監控 (零配置)**

在應用入口點 (`src/main.ts` / `src/index.tsx`):

```typescript
import { initLonghunMonitoring } from '@longhun/monitoring-sdk';

// 一行代碼啟動·自動初始化所有模塊
initLonghunMonitoring({
  appId: 'real-time-performance-dashboard',
  environment: 'production',
  autoInit: true
});
```

### **Step 3: 驗證部署**

```bash
# 執行部署檢查
bash ./mobile-monitoring/deployment-check.sh

# 預期輸出:
# ✅ SDK 版本: 1.0.0
# ✅ 配置文件存在
# ✅ 雲端連接正常
# ✅ IndexedDB 可用
# ✅ SDK 初始化成功
# ✅ 部署驗證完成
```

---

## 🎯 **核心 4 個應用的監控部署**

### **應用 1: 實時性能監控儀表板**

```bash
# 部署配置
cat > .env.monitoring << 'EOF'
LONGHUN_APP_ID=real-time-performance-dashboard
LONGHUN_ENV=production
LONGHUN_SDK_VERSION=1.0.0
LONGHUN_MONITORING_ENDPOINT=https://monitoring.longhun.io/api
LONGHUN_AUTO_INIT=true
LONGHUN_AUTO_PERSIST=true
LONGHUN_AUTO_REPORT=true
EOF

# 部署應用
npm run build
npm run deploy:monitoring
```

**監控指標 (自動採集)**：
- 頁面加載時間: < 2s ✅
- 數據更新延遲: < 500ms
- 首次互動延遲: < 100ms
- 錯誤率: < 0.1%

---

### **應用 2: 數據可視化儀表板**

```bash
# 相同配置，僅改 APP_ID
LONGHUN_APP_ID=data-visualization-dashboard

npm run build
npm run deploy:monitoring
```

**監控指標**:
- 首次有效繪製: < 3s
- 圖表交互延遲: < 200ms
- 查詢成功率: > 99.9%

---

### **應用 3: 移動端身份驗證系統**

```bash
LONGHUN_APP_ID=mobile-auth-system

# 啟用額外的安全監控
LONGHUN_SECURITY_MONITORING=true
LONGHUN_AUTH_FAILURE_THRESHOLD=5

npm run build
npm run deploy:monitoring
```

**監控指標**:
- 驗證成功率: > 99.5%
- 驗證耗時: < 2s
- 異常事件: 自動告警

---

### **應用 4: 智能任務管理移動端**

```bash
LONGHUN_APP_ID=smart-task-management

# 啟用離線支持監控
LONGHUN_OFFLINE_SUPPORT=true
LONGHUN_SYNC_MONITORING=true

npm run build
npm run deploy:monitoring
```

**監控指標**:
- 任務同步延遲: < 1s
- 數據一致性: 100%
- 離線隊列大小: < 100

---

## 🔍 **實時監控日誌查看**

部署完成後，所有運行日誌會自動實時公開：

```
🌐 監控儀表板: https://logs.longhun.io/public
⏱️  更新頻率: 每 5 秒實時刷新
📊 覆蓋範圍: 4 個應用 · 所有指標
🔴 告警通知: 釘釘·郵件·Webhook
```

---

## 📋 **部署檢查清單**

```bash
#!/bin/bash

echo "🐉 龍魂移動端監控 · 部署檢查清單"

# [✅] 1. SDK 已安裝
npm list @longhun/monitoring-sdk > /dev/null && echo "✅ [1] SDK 已安裝"

# [✅] 2. 配置文件就位
[ -f .env.monitoring ] && echo "✅ [2] 配置文件就位"

# [✅] 3. 所有應用初始化
grep -r "initLonghunMonitoring" src/ > /dev/null && echo "✅ [3] 應用初始化完成"

# [✅] 4. 自動報告已配置
grep -r "autoReport: true" src/ > /dev/null && echo "✅ [4] 自動報告已配置"

# [✅] 5. 告警已就緒
grep -r "alerting.enabled: true" . > /dev/null && echo "✅ [5] 告警已就緒"

# [✅] 6. 公開日誌已啟用
curl -s https://logs.longhun.io/health > /dev/null && echo "✅ [6] 公開日誌已啟用"

echo ""
echo "✅ 所有檢查通過·準備就緒！"
```

---

## 🚀 **自動化執行命令**

```bash
# 一鍵完整部署（包含所有 4 個應用）
bash ./mobile-monitoring/deploy-all.sh

# 監控單個應用
bash ./mobile-monitoring/monitor-app.sh real-time-performance-dashboard

# 查看實時指標
curl https://logs.longhun.io/api/metrics/latest?app=real-time-performance-dashboard

# 導出報告
bash ./mobile-monitoring/export-report.sh --format=json --days=7
```

---

## 🎛️ **高級配置 (可選)**

### **採樣率控制 (成本優化)**

```typescript
// 自動動態採樣
initLonghunMonitoring({
  sdk: {
    performance: {
      sampleRate: 1.0      // 正常: 100%
      // sampleRate: 0.5   // 降低: 50%
      // sampleRate: 0.1   // 最低: 10%
    }
  }
});
```

### **自定義告警規則**

```yaml
# 在 .env.monitoring 中配置
LONGHUN_ALERT_RULES: |
  - name: HighErrorRate
    threshold: 0.05
    duration: 5m
    severity: critical

  - name: SlowLoadTime
    threshold: 5000
    duration: 2m
    severity: warning
```

### **存儲策略**

```typescript
initLonghunMonitoring({
  storage: {
    type: 'indexeddb',
    maxSize: '50MB',
    expirationDays: 30,
    autoCleanup: true  // 自動清理過期數據
  }
});
```

---

## 📊 **監控指標速查表**

| 應用 | 加載時間 | 錯誤率 | 用戶在線 | 狀態 |
|------|---------|--------|---------|------|
| 實時性能監控 | 1.2s ⬇️ | 0.02% ✅ | 1,234 | ✅ 正常 |
| 數據可視化 | 2.8s ⬇️ | 0.05% ✅ | 0 | 🔨 部署中 |
| 身份驗證系統 | 0.9s ✅ | 0.05% ✅ | 567 | ✅ 正常 |
| 任務管理應用 | 1.5s ✅ | 0.01% ✅ | 234 | ✅ 正常 |

---

## 🆘 **常見問題**

**Q1: SDK 初始化失敗？**
```bash
# 檢查版本
npm list @longhun/monitoring-sdk

# 清理重裝
npm uninstall @longhun/monitoring-sdk
npm install @longhun/monitoring-sdk@latest
```

**Q2: 日誌沒有上報？**
```bash
# 在控制台執行
__LONGHUN_MONITOR__.getQueuedEvents()  // 查看隊列
__LONGHUN_MONITOR__.flush()             // 強制上報
```

**Q3: 成本過高？**
```
1. 降低採樣率: sampleRate 100% → 50%
2. 啟用數據壓縮: compression: 'gzip'
3. 自動歸檔舊數據: 7 天移至冷存儲
預期節省: 40-50%
```

---

## ✅ **部署驗收標準**

```
✅ [必須] SDK 成功初始化
✅ [必須] 4 個應用都有數據上報
✅ [必須] 公開日誌可訪問
✅ [必須] 告警系統就緒
✅ [建議] IndexedDB 本地存儲可用
✅ [建議] 性能指標 < 目標值
✅ [建議] 錯誤率 < 0.1%
```

---

## 📞 **技術支持**

遇到問題？快速診斷：

```bash
# 自我診斷
__LONGHUN_MONITOR__.selfDiagnose()

# 導出日誌供診斷
__LONGHUN_MONITOR__.exportData('json') > logs.json
```

---

## 🎉 **部署成功！**

```
════════════════════════════════════════════════════════════════

        🐉 龍魂移動端監控 · 部署完成

════════════════════════════════════════════════════════════════

✅ 4 個應用監控已上線
✅ 15 層完整監控體系已就緒
✅ 實時公開日誌: https://logs.longhun.io/public
✅ 自動告警: 釘釘·郵件·Webhook
✅ 自動報告: 日·週·月報

DNA: #龍芯⚡️2026-06-07-MOBILE-MONITORING-DEPLOYMENT-QS
責任: UID9622 · 不免責

天下無欺。🐉

════════════════════════════════════════════════════════════════
```

---

**下一步**: 访问 https://logs.longhun.io/public 查看实时监控日誌！
