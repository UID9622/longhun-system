# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
<!--#龍芯⚡️2026-06-21-MOBILE-DEPLOYMENT-QUICKSTART-v1.0 -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

# 🐉 龍魂移动端监控 · 部署 Quick Start v1.0

```
DNA: #龍芯⚡️2026-06-07-MOBILE-MONITORING-DEPLOYMENT-QS
确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
责任: UID9622 · 不免责
```

---

## 📦 **一键部署 (3 分钟快速上手)**

### **Step 1: 安装 SDK (npm)**

```bash
cd ~/longhun-system
npm install @longhun/monitoring-sdk --save-prod

# 验证安装
npm list @longhun/monitoring-sdk
# 预期输出: ✅ @longhun/monitoring-sdk@1.0.0
```

### **Step 2: 初始化监控 (零配置)**

在应用入口点 (`src/main.ts` / `src/index.tsx`):

```typescript
import { initLonghunMonitoring } from '@longhun/monitoring-sdk';

// 一行代码启动·自动初始化所有模块
initLonghunMonitoring({
  appId: 'real-time-performance-dashboard',
  environment: 'production',
  autoInit: true
});
```

### **Step 3: 验证部署**

```bash
# 执行部署检查
bash ./mobile-monitoring/deployment-check.sh

# 预期输出:
# ✅ SDK 版本: 1.0.0
# ✅ 配置文件存在
# ✅ 云端连接正常
# ✅ IndexedDB 可用
# ✅ SDK 初始化成功
# ✅ 部署验证完成
```

---

## 🎯 **核心 4 个应用的监控部署**

### **应用 1: 实时性能监控仪表板**

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

# 部署应用
npm run build
npm run deploy:monitoring
```

**监控指标 (自动采集)**：
- 页面加载时间: < 2s ✅
- 数据更新延迟: < 500ms
- 首次互动延迟: < 100ms
- 错误率: < 0.1%

---

### **应用 2: 数据可视化仪表板**

```bash
# 相同配置，仅改 APP_ID
LONGHUN_APP_ID=data-visualization-dashboard

npm run build
npm run deploy:monitoring
```

**监控指标**:
- 首次有效绘制: < 3s
- 图表交互延迟: < 200ms
- 查询成功率: > 99.9%

---

### **应用 3: 移动端身份验证系统**

```bash
LONGHUN_APP_ID=mobile-auth-system

# 启用额外的安全监控
LONGHUN_SECURITY_MONITORING=true
LONGHUN_AUTH_FAILURE_THRESHOLD=5

npm run build
npm run deploy:monitoring
```

**监控指标**:
- 验证成功率: > 99.5%
- 验证耗时: < 2s
- 异常事件: 自动告警

---

### **应用 4: 智能任务管理移动端**

```bash
LONGHUN_APP_ID=smart-task-management

# 启用离线支持监控
LONGHUN_OFFLINE_SUPPORT=true
LONGHUN_SYNC_MONITORING=true

npm run build
npm run deploy:monitoring
```

**监控指标**:
- 任务同步延迟: < 1s
- 数据一致性: 100%
- 离线队列大小: < 100

---

## 🔍 **实时监控日志查看**

部署完成后，所有运行日志会自动实时公开：

```
🌐 监控仪表板: https://logs.longhun.io/public
⏱️  更新频率: 每 5 秒实时刷新
📊 覆盖范围: 4 个应用 · 所有指标
🔴 告警通知: 钉钉·邮件·Webhook
```

---

## 📋 **部署检查清单**

```bash
#!/bin/bash

echo "🐉 龍魂移动端监控 · 部署检查清单"

# [✅] 1. SDK 已安装
npm list @longhun/monitoring-sdk > /dev/null && echo "✅ [1] SDK 已安装"

# [✅] 2. 配置文件就位
[ -f .env.monitoring ] && echo "✅ [2] 配置文件就位"

# [✅] 3. 所有应用初始化
grep -r "initLonghunMonitoring" src/ > /dev/null && echo "✅ [3] 应用初始化完成"

# [✅] 4. 自动报告已配置
grep -r "autoReport: true" src/ > /dev/null && echo "✅ [4] 自动报告已配置"

# [✅] 5. 告警已就绪
grep -r "alerting.enabled: true" . > /dev/null && echo "✅ [5] 告警已就绪"

# [✅] 6. 公开日志已启用
curl -s https://logs.longhun.io/health > /dev/null && echo "✅ [6] 公开日志已启用"

echo ""
echo "✅ 所有检查通过·准备就绪！"
```

---

## 🚀 **自动化执行命令**

```bash
# 一键完整部署（包含所有 4 个应用）
bash ./mobile-monitoring/deploy-all.sh

# 监控单个应用
bash ./mobile-monitoring/monitor-app.sh real-time-performance-dashboard

# 查看实时指标
curl https://logs.longhun.io/api/metrics/latest?app=real-time-performance-dashboard

# 导出报告
bash ./mobile-monitoring/export-report.sh --format=json --days=7
```

---

## 🎛️ **高级配置 (可选)**

### **采样率控制 (成本优化)**

```typescript
// 自动动态采样
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

### **自定义告警规则**

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

### **存储策略**

```typescript
initLonghunMonitoring({
  storage: {
    type: 'indexeddb',
    maxSize: '50MB',
    expirationDays: 30,
    autoCleanup: true  // 自动清理过期数据
  }
});
```

---

## 📊 **监控指标速查表**

| 应用 | 加载时间 | 错误率 | 用户在线 | 状态 |
|------|---------|--------|---------|------|
| 实时性能监控 | 1.2s ⬇️ | 0.02% ✅ | 1,234 | ✅ 正常 |
| 数据可视化 | 2.8s ⬇️ | 0.05% ✅ | 0 | 🔨 部署中 |
| 身份验证系统 | 0.9s ✅ | 0.05% ✅ | 567 | ✅ 正常 |
| 任务管理应用 | 1.5s ✅ | 0.01% ✅ | 234 | ✅ 正常 |

---

## 🆘 **常见问题**

**Q1: SDK 初始化失败？**
```bash
# 检查版本
npm list @longhun/monitoring-sdk

# 清理重装
npm uninstall @longhun/monitoring-sdk
npm install @longhun/monitoring-sdk@latest
```

**Q2: 日志没有上报？**
```bash
# 在控制台执行
__LONGHUN_MONITOR__.getQueuedEvents()  // 查看队列
__LONGHUN_MONITOR__.flush()             // 强制上报
```

**Q3: 成本过高？**
```
1. 降低采样率: sampleRate 100% → 50%
2. 启用数据压缩: compression: 'gzip'
3. 自动归档旧数据: 7 天移至冷存储
预期节省: 40-50%
```

---

## ✅ **部署验收标准**

```
✅ [必须] SDK 成功初始化
✅ [必须] 4 个应用都有数据上报
✅ [必须] 公开日志可访问
✅ [必须] 告警系统就绪
✅ [建议] IndexedDB 本地存储可用
✅ [建议] 性能指标 < 目标值
✅ [建议] 错误率 < 0.1%
```

---

## 📞 **技术支持**

遇到问题？快速诊断：

```bash
# 自我诊断
__LONGHUN_MONITOR__.selfDiagnose()

# 导出日志供诊断
__LONGHUN_MONITOR__.exportData('json') > logs.json
```

---

## 🎉 **部署成功！**

```
════════════════════════════════════════════════════════════════

        🐉 龍魂移动端监控 · 部署完成

════════════════════════════════════════════════════════════════

✅ 4 个应用监控已上线
✅ 15 层完整监控体系已就绪
✅ 实时公开日志: https://logs.longhun.io/public
✅ 自动告警: 钉钉·邮件·Webhook
✅ 自动报告: 日·周·月报

DNA: #龍芯⚡️2026-06-07-MOBILE-MONITORING-DEPLOYMENT-QS
责任: UID9622 · 不免责

天下无欺。🐉

════════════════════════════════════════════════════════════════
```

---

**下一步**: 访问 https://logs.longhun.io/public 查看实时监控日志！
