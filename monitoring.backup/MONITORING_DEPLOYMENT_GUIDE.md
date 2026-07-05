# 🐉 龍魂系统监控部署指南

**DNA**:#龍芯⚡️2026-06-08-MONITORING-DEPLOYMENT-v1.0
**确认**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

---

## 📋 目录

1. [快速开始](#快速开始)
2. [核心指标](#核心指标-8-个)
3. [SLO 定义](#slo-定义-4-个)
4. [告警规则](#告警规则-8-个)
5. [部署步骤](#部署步骤)
6. [验证和测试](#验证和测试)

---

## 快速开始

### 环境需求

```bash
# 安装 Datadog Agent
DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=$DATADOG_API_KEY DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_mac_os.sh)"

# 验证 Agent 运行
sudo launchctl list | grep datadog
```

### 3 步部署

```bash
# 1. 应用 Prometheus 规则
kubectl apply -f prometheus_rules.yaml -n longhun-prod

# 2. 部署 Grafana 仪表板
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

## 核心指标 (8 个)

### 1️⃣ API 响应时间
**指标**: `api.response_time` | **单位**: milliseconds

```
P50: ~50ms (快速路径)
P95: ≤ 500ms (SLO 目标)
P99: ≤ 1000ms (可接受)

告警阈值:
  ⚠️ P95 > 500ms (10 分钟) → Warning
  🔴 P95 > 1000ms (5 分钟) → Critical
```

### 2️⃣ API 吞吐量
**指标**: `api.request_rate` | **单位**: req/s

```
目标: 77.8 req/s (基线)
范围: 50-150 req/s (正常)

告警阈值:
  ⚠️ < 50 req/s → 检查故障
  ⚠️ > 150 req/s → 检查异常流量
```

### 3️⃣ 错误率
**指标**: `api.error_rate` | **单位**: percent

```
目标: < 0.1% (SLO)
警告: > 1%

告警阈值:
  ⚠️ > 1% (5 分钟)
  🔴 > 5% (2 分钟)
```

### 4️⃣ 数据库连接池
**指标**: `db.pool.usage` | **单位**: percent

```
配置: 20 个连接
警告: > 80%
临界: > 90%

告警阈值:
  ⚠️ > 80% (10 分钟)
  🔴 > 90% (2 分钟)
```

### 5️⃣ Redis 快取命中率
**指标**: `cache.hit_rate` | **单位**: percent

```
目标: 92%
可接受: > 80%

告警阈值:
  ⚠️ < 80% (10 分钟)
```

### 6️⃣ CPU 使用率
**指标**: `system.cpu.user` | **单位**: percent

```
正常: < 40%
警告: > 60%
临界: > 80%

告警阈值:
  ⚠️ > 80% (10 分钟)
```

### 7️⃣ 内存使用率
**指标**: `system.mem.pct_usable` | **单位**: percent

```
正常: < 40%
警告: > 60%
临界: > 80%

告警阈值:
  ⚠️ < 20% 可用 (10 分钟)
```

### 8️⃣ 磁盘使用率
**指标**: `system.disk.used` | **单位**: percent

```
正常: < 70%
警告: > 75%
临界: > 85%

告警阈值:
  ⚠️ > 85% (10 分钟)
  🔴 < 10% 可用 (1 分钟)
```

---

## SLO 定义 (4 个)

### 📌 可用性 SLO
```
名称:   整体系统可用性
目标:   99.95%
计算:   (成功请求 / 所有请求) × 100
窗口:   滚动 30 天
告警:   < 99.95% 持续 5 分钟
```

### 📌 延迟 SLO
```
名称:   API P95 响应时间
目标:   ≤ 500ms
计算:   histogram_quantile(0.95, ...)
窗口:   滚动 7 天
告警:   > 500ms 持续 10 分钟
```

### 📌 错误率 SLO
```
名称:   API 错误率
目标:   ≤ 0.1%
计算:   (错误 / 所有请求) × 100
窗口:   滚动 7 天
告警:   > 0.1% 持续 5 分钟
```

### 📌 吞吐量 SLO
```
名称:   最小请求吞吐量
目标:   ≥ 50 req/s
计算:   rate(requests_total[1m])
窗口:   滚动 1 小时
告警:   < 50 req/s 持续 5 分钟
```

---

## 告警规则 (8 个)

### 🔴 Critical Alerts (需要立即响应)

**1. 高错误率**
```
条件: error_rate > 1%
持续: 5 分钟
通知: Slack + PagerDuty
行动: 检查应用日志，可能需要回滚
```

**2. 数据库连接池耗尽**
```
条件: db.pool.usage > 90%
持续: 2 分钟
通知: Slack + PagerDuty
行动: 检查 DB 连接泄漏，可能需要重启 app
```

**3. 磁盘空间临界**
```
条件: disk_available < 10%
持续: 1 分钟
通知: Slack + PagerDuty
行动: 清理日志，扩展磁盘
```

### 🟡 Warning Alerts (需要关注)

**4. API 延迟高**
```
条件: api.latency_p95 > 500ms
持续: 10 分钟
通知: Slack
行动: 检查慢查询，优化代码
```

**5. 内存使用率高**
```
条件: memory_usage > 80%
持续: 10 分钟
通知: Slack
行动: 检查内存泄漏，考虑重启
```

**6. CPU 使用率高**
```
条件: cpu_usage > 80%
持续: 10 分钟
通知: Slack
行动: 检查消耗 CPU 的进程
```

**7. 快取命中率低**
```
条件: cache_hit_rate < 80%
持续: 10 分钟
通知: Slack
行动: 检查快取配置，考虑增加快取大小
```

**8. Kimi API 延迟高**
```
条件: kimi_latency > 5000ms
持续: 5 分钟
通知: Slack
行动: 检查 Kimi API 状态，使用本地推理
```

---

## 部署步骤

### Phase 1: 准备工作 (15 分钟)

```bash
# 1. 检查环境
kubectl get nodes
kubectl get pods -n longhun-prod

# 2. 验证存储和权限
ls -la monitoring/
kubectl auth can-i create configmaps -n longhun-prod

# 3. 备份现有配置
cp -r /etc/prometheus /etc/prometheus.backup
cp -r /etc/grafana /etc/grafana.backup
```

### Phase 2: 应用 Prometheus 规则 (10 分钟)

```bash
# 1. 验证语法
promtool check rules prometheus_rules.yaml

# 2. 应用规则
kubectl apply -f prometheus_rules.yaml -n longhun-prod

# 3. 重新加载 Prometheus
kubectl rollout restart prometheus -n longhun-prod

# 4. 验证规则已加载
curl http://prometheus:9090/api/v1/rules | jq '.data.groups[].rules | length'
```

### Phase 3: 部署 Grafana 仪表板 (15 分钟)

```bash
# 1. 获取 Grafana API Token
GRAFANA_TOKEN=$(kubectl exec -n longhun-prod -it deploy/grafana -- \
  grafana-cli admin create-api-token --name "deploy" --role Admin)

# 2. 导入仪表板配置
curl -X POST http://grafana:3000/api/dashboards/db \
  -H "Authorization: Bearer $GRAFANA_TOKEN" \
  -H "Content-Type: application/json" \
  -d @grafana_dashboard_config.json

# 3. 验证仪表板已创建
curl http://grafana:3000/api/search?query=longhun
```

### Phase 4: 配置 Datadog (10 分钟)

```bash
# 1. 验证环境变数
echo $DATADOG_API_KEY
echo $DATADOG_APP_KEY

# 2. 生成监控配置
python3 datadog_monitoring_config.py

# 3. 部署 Datadog Agent ConfigMap
kubectl create configmap datadog-config \
  --from-file=datadog.yaml \
  -n longhun-prod

# 4. 重启 Datadog Agent
kubectl rollout restart daemonset/datadog-agent -n longhun-prod
```

### Phase 5: 验证和测试 (10 分钟)

```bash
# 1. 验证告警规则
curl http://prometheus:9090/api/v1/rules

# 2. 验证仪表板
curl http://grafana:3000/api/dashboards/uid/longhun-prod

# 3. 测试告警通知
# 在 Datadog 或 Prometheus 中触发测试告警

# 4. 检查日志
kubectl logs -n longhun-prod deploy/prometheus -f
kubectl logs -n longhun-prod deploy/grafana -f
```

---

## 验证和测试

### ✅ 验收清单

```
□ Prometheus 规则加载成功
  kubectl get rules -n longhun-prod
  结果: ✅ longhun_production 规则集存在

□ Grafana 仪表板创建成功
  curl http://grafana:3000/api/dashboards/uid/longhun-prod
  结果: ✅ HTTP 200 + 仪表板详情

□ Datadog Agent 连接成功
  curl https://api.datadoghq.com/api/v1/validate
  结果: ✅ "valid": true

□ 告警通知工作
  测试 Slack webhook: curl -X POST $SLACK_WEBHOOK -d '{"text":"Test"}'
  结果: ✅ Slack 频道收到消息

□ 核心指标可见
  访问仪表板，检查所有 8 个指标都有数据
  结果: ✅ 所有面板都显示数据

□ SLO 被追踪
  Datadog 中检查 SLO 仪表板
  结果: ✅ 4 个 SLO 都被计算和跟踪
```

### 🧪 测试告警

```bash
# 1. 测试 Critical Alert
# 模拟高错误率
watch 'curl http://api:8443/api/v1/skills/999/execute; echo'

# 验证:
# ✅ Slack 收到警报 (2 分钟内)
# ✅ PagerDuty 创建事件 (2 分钟内)

# 2. 测试 Warning Alert
# 监控仪表板，应看到 P95 延迟升高
# ✅ Slack 收到警告 (10 分钟内)

# 3. 验证告警恢复
# 停止模拟负载
# ✅ Slack 收到恢复通知
```

---

## 监控仪表板访问

| 服务 | URL | 用户 |
|------|-----|------|
| Prometheus | http://prometheus:9090 | 无需认证 |
| Grafana | http://grafana:3000 | admin / $GRAFANA_PASSWORD |
| Datadog | https://app.datadoghq.com | 用 SSO 登入 |

---

## 故障排查

### Prometheus 规则无法加载

```bash
# 检查语法
promtool check rules prometheus_rules.yaml

# 检查 Prometheus 日志
kubectl logs -n longhun-prod deploy/prometheus | grep -i error

# 重新应用规则
kubectl delete -f prometheus_rules.yaml
kubectl apply -f prometheus_rules.yaml
```

### Grafana 仪表板无数据

```bash
# 检查数据源连接
curl http://prometheus:9090/-/healthy

# 检查 Grafana 日志
kubectl logs -n longhun-prod deploy/grafana | grep -i datasource

# 测试查询
curl 'http://prometheus:9090/api/v1/query?query=up'
```

### Datadog 告警无法发送

```bash
# 验证 API Key
curl -H "DD-API-KEY: $DATADOG_API_KEY" \
  https://api.datadoghq.com/api/v1/validate

# 检查告警配置
curl -H "Authorization: Bearer $DATADOG_API_KEY" \
  https://api.datadoghq.com/api/v1/monitor | jq '.[] | .name'
```

---

## 相关文档

- `prometheus_rules.yaml` - Prometheus 告警规则
- `grafana_dashboard_config.json` - Grafana 仪表板配置
- `datadog_monitoring_config.py` - Datadog 配置生成器
- `datadog_monitoring_config.json` - Datadog 配置文件

---

**DNA**:#龍芯⚡️2026-06-08-MONITORING-DEPLOYMENT-GUIDE-v1.0
**最后更新**: 2026-06-08
**版本**: 1.0
