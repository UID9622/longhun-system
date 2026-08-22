# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂系统·团队培训计划

**DNA**:#龍芯⚡️丙午·甲午·癸丑·戊午·䷨损-TEAM-TRAINING-v1.0
**确认**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**目标读者**: 运维团队 / SRE 工程师 / DevOps 工程师
**培训时长**: 4 小时（分 4 节课）

---

## 📋 课程大纲

| 课程 | 时长 | 讲师 | 目标 |
|------|------|------|------|
| 🎯 第 1 课：系统架构和部署概述 | 45 分钟 | Tech Lead | 全面了解系统设计 |
| 🚀 第 2 课：生产部署演练 | 60 分钟 | DevOps Lead | 掌握 27 步部署流程 |
| 📊 第 3 课：监控和告警运维 | 45 分钟 | SRE Lead | 使用监控仪表板 |
| 🔧 第 4 课：故障排查和应急 | 30 分钟 | Support Lead | 应对常见问题 |

---

## 🎯 第 1 课：系统架构和部署概述（45 分钟）

### 课程目标
- 理解龍魂系统的核心组件
- 了解 10 个 Skills 的功能
- 掌握蓝绿部署策略

### 课程内容

#### 1.1 系统架构概览（15 分钟）

```
龍魂系统架构图
═══════════════════════════════════════════════════════════════

  用户界面层
  ┌──────────────────────────────────────────────────────────┐
  │  Web UI / API Gateway / Kimi AI 集成                      │
  └──────────────────────────────────────────────────────────┘
                              ↓
  应用层 (10 Skills)
  ┌─────────────┬─────────────┬─────────────┬─────────────┐
  │ Skill-1     │ Skill-2     │ Skill-3     │ Skill-4     │
  │ 算法艺术    │ 品牌指南    │ Canvas设计  │ 文档协作    │
  ├─────────────┼─────────────┼─────────────┼─────────────┤
  │ Skill-5     │ Skill-6     │ Skill-7     │ Skill-8     │
  │ 内部沟通    │ MCP Builder │ Skill 创建  │ GIF 生成    │
  ├─────────────┼─────────────┼─────────────┼─────────────┤
  │ Skill-9     │ Skill-10    │             │             │
  │ 主题工厂    │ Web 构件    │             │             │
  └─────────────┴─────────────┴─────────────┴─────────────┘
                              ↓
  服务层
  ┌──────────────┬──────────────┬──────────────┬──────────────┐
  │ API 服务     │ 认证服务     │ 日志服务     │ 监控服务     │
  └──────────────┴──────────────┴──────────────┴──────────────┘
                              ↓
  基础设施层
  ┌──────────────┬──────────────┬──────────────┬──────────────┐
  │ PostgreSQL   │ Redis Cache  │ Elasticsearch│ Prometheus   │
  │ (持久化)     │ (加速)       │ (日志)       │ (监控)       │
  └──────────────┴──────────────┴──────────────┴──────────────┘
                              ↓
  特殊集成
  ┌──────────────┬──────────────┐
  │ Kimi AI      │ HashiCorp    │
  │ (推理)       │ Vault (密钥) │
  └──────────────┴──────────────┘
```

**关键数字**:
- 10 个 Skills（120 个规格块）
- 8 个核心监控指标
- 27 个部署步骤
- 4 个集成模式（Kimi）
- 99.95% 可用性 SLO

#### 1.2 部署策略（15 分钟）

**蓝绿部署流程**:

```
步骤 1: 准备绿色环境
  ┌─────────────────────────────────────────┐
  │ 构建新的 Docker 镜像                     │
  │ longhun:prod-2026-06-08-v1.0            │
  └─────────────────────────────────────────┘
                      ↓
步骤 2: 启动绿色实例
  ┌──────────┬──────────┬──────────┐
  │Green-1  │Green-2   │Green-3   │ (3 个副本)
  └──────────┴──────────┴──────────┘
                      ↓
步骤 3: 烟雾测试
  ✓ GET /health
  ✓ GET /api/v1/skills
  ✓ POST /api/v1/skills/1/execute
                      ↓
步骤 4: 流量迁移 (零停机)
  时间   蓝色流量    绿色流量
  ─────────────────────────
  T+0     100%        0%
  T+2     90%         10%
  T+4     75%         25%
  T+6     50%         50%
  T+8     25%         75%
  T+10    0%          100%
                      ↓
步骤 5: 蓝色待命
  ┌──────────┬──────────┬──────────┐
  │ Blue-1   │ Blue-2   │ Blue-3   │ (随时回滚)
  └──────────┴──────────┴──────────┘
```

**优势**:
- ✅ 零停机时间
- ✅ 快速回滚（1-2 分钟）
- ✅ A/B 测试可能性
- ✅ 资源效率高

#### 1.3 关键配置（15 分钟）

```bash
# 生产配置关键参数

## API 配置
API_HOST=api.longhun.example.com
API_PORT=8443
MAX_CONCURRENT_CONNECTIONS=10000
REQUEST_TIMEOUT=30s

## 数据库配置
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

## 监控配置
MONITORING_SERVICE=datadog
LOG_AGGREGATION=elasticsearch
APM_SERVICE=jaeger

## Kimi AI 集成
KIMI_API_KEY=${KIMI_API_KEY}  # 环境变数方式
KIMI_TIMEOUT=30s
KIMI_MAX_RETRIES=3
```

### 练习题
1. 蓝绿部署的流量迁移顺序是什么？
2. 如何在 10 秒内完成流量迁移？
3. 回滚时需要做什么？

---

## 🚀 第 2 课：生产部署演练（60 分钟）

### 课程目标
- 执行完整的 27 步部署流程
- 理解每个步骤的目的和检查点
- 学会从日志中识别问题

### 课程内容

#### 2.1 部署准备（10 分钟）

**部署前检查清单**:

```
□ T-72h: 计划阶段
  □ 选择部署窗口（低流量时段）
  □ 组建部署团队（4 个角色）
  □ 审查变更内容
  □ 准备回滚计划

□ T-24h: 准备阶段
  □ 验证配置
  □ 检查 SSL 证书
  □ 验证备份系统
  □ 通知相关人员

□ T-0: 部署阶段
  □ 最后确认所有检查
  □ 启动监控仪表板
  □ 准备快速通信渠道 (Slack)
  □ 宣布部署开始
```

#### 2.2 27 步部署流程（40 分钟）

**分为 7 个阶段，每个阶段 3-4 个步骤**:

**阶段 1: 部署前检查（4 步）**
```
✅ 步骤 1: 配置验证
   检查: 所有必要配置是否存在
   通过: 10/10 配置项 ✓

✅ 步骤 2: SSL 证书验证
   检查: 证书有效期
   通过: 证书有效直到 2027 年 ✓

✅ 步骤 3: 密钥管理检查
   检查: 密钥是否已配置
   通过: HashiCorp Vault 中 ✓

✅ 步骤 4: 文件权限检查
   检查: 所有路径的权限
   通过: 所有路径权限正确 ✓
```

**阶段 2: 数据库迁移（4 步）**
```
✅ 步骤 5: 数据库备份
   操作: 创建完整备份
   结果: /var/backups/longhun/longhun_prod_20260608_204930.sql

✅ 步骤 6: 数据库连接
   检查: 连接到生产数据库
   结果: 已连接到 longhun_app@prod-postgresql.example.com:5432

✅ 步骤 7: 执行迁移
   操作: 5 个迁移步骤
   ✓ 初始化 Skills 表
   ✓ 创建性能指标表
   ✓ 创建审计日志表
   ✓ 添加索引优化
   ✓ 启用复制和高可用

✅ 步骤 8: 数据完整性检查
   检查: 所有表和索引
   结果: 完整性验证通过 ✓
```

**阶段 3: 安全加固（4 步）**
```
✅ 步骤 9: 防火墙规则配置
   ✓ HTTP 80 → 重定向到 HTTPS
   ✓ HTTPS 443 → 主要 API 端口
   ✓ SSH 22 → 限制于特定 IP
   ✓ 禁止其他入站
   ✓ 允许出站到监控服务

✅ 步骤 10: CORS 配置
   设置: 只允许 https://longhun.example.com

✅ 步骤 11: 速率限制配置
   ✓ API: 1000 req/min per IP
   ✓ 登入: 10 attempts/15min
   ✓ Skill: 100 req/min per API key

✅ 步骤 12: 审计日志启用
   配置: 所有 API 调用都被记录
```

**阶段 4: 蓝绿部署（5 步）**
```
✅ 步骤 13: 构建绿色环境
   构建: Docker 镜像 longhun:prod-2026-06-08-v1.0
   结果: 镜像构建完成 (100%)

✅ 步骤 14: 启动绿色实例
   启动: 3 个副本 (prod-green-1, green-2, green-3)
   结果: 所有 3 个实例已启动 ✓

✅ 步骤 15: 烟雾测试
   测试:
   ✓ GET /health → 200 OK
   ✓ GET /api/v1/skills → 200 OK
   ✓ POST /api/v1/skills/1/execute → 202 Accepted

✅ 步骤 16: 流量迁移
   进度: 10% → 25% → 50% → 75% → 100%
   结果: 完全切换到绿色环境 (耗时 ~10 秒)

✅ 步骤 17: 蓝色待命
   状态: 旧环境保持运行，随时可回滚
```

**阶段 5: 健康验证（2 步）**
```
✅ 步骤 18: 执行健康检查
   检查:
   ✓ API 响应性 (avg 15.2ms)
   ✓ 数据库连接 (10/10)
   ✓ Redis 快取 (hit rate 92%)
   ✓ 所有 10 Skills (10/10)
   ✓ SSL/TLS 证书 (valid until 2027)
   ✓ 磁盘空间 (85% available)
   ✓ 内存使用 (<40%)
   ✓ CPU 使用 (<8%)
   结果: 8/8 检查通过 ✓

✅ 步骤 19: 端点验证
   验证:
   ✓ GET /health → 200
   ✓ GET /api/v1/skills → 200
   ✓ GET /api/v1/skills/1 → 200
   ✓ POST /api/v1/skills/1/execute → 202
   ✓ GET /api/v1/metrics → 200
   结果: 5/5 端点响应正常 ✓
```

**阶段 6: 监控启动（4 步）**
```
✅ 步骤 20: 监控服务集成
   连接: Datadog
   状态: 已连接 ✓

✅ 步骤 21: 告警规则配置
   启用:
   ✓ Error Rate > 1%
   ✓ Response Time P95 > 500ms
   ✓ Database Connection Pool Exhausted
   ✓ Memory > 80%
   ✓ Disk Space < 10%
   ✓ SSL Certificate Expiring

✅ 步骤 22: 日志聚合
   连接: Elasticsearch
   状态: 已连接 ✓

✅ 步骤 23: 分布式追踪
   启用: Jaeger APM
   状态: 已启用 ✓

✅ 步骤 24: 实时仪表板
   工具: Grafana
   状态: 已部署 ✓
```

**阶段 7: 部署后处理（3 步）**
```
✅ 步骤 25: 部署记录
   记录: 部署详情已记录

✅ 步骤 26: 通知利益相关者
   ✓ Slack 通知 (#deployments)
   ✓ JIRA 状态更新
   ✓ 报告发送至运营团队

✅ 步骤 27: 文档更新
   更新: 部署文档已更新
```

#### 2.3 实际演练（10 分钟）

```bash
# 运行完整部署演练
cd ~/longhun-system
python3 deployment/production_deployment.py

# 预期结果:
# ✅ 27/27 步骤通过
# ✅ 8/8 健康检查通过
# ✅ 部署耗时: ~8 秒 (演示模式)
# ✅ 部署报告已生成
```

### 练习题
1. 如果步骤 15（烟雾测试）失败怎么办？
2. 流量迁移耗时多久？
3. 回滚命令是什么？

---

## 📊 第 3 课：监控和告警运维（45 分钟）

### 课程目标
- 使用 Grafana 和 Datadog 监控系统
- 理解 8 个核心指标
- 响应告警并检查系统状态

### 课程内容

#### 3.1 监控仪表板使用（20 分钟）

**访问仪表板**:

```
Prometheus: http://prometheus:9090
Grafana:    http://grafana:3000 (admin / password)
Datadog:    https://app.datadoghq.com (SSO)
```

**仪表板上的 10 个面板**:

| # | 面板名称 | 类型 | 目标 |
|---|---------|------|------|
| 1 | API 响应时间 (P50/95/99) | Graph | P95 < 500ms |
| 2 | API 吞吐量 (req/s) | Gauge | 77.8 req/s |
| 3 | 错误率 (%) | Stat | < 0.1% |
| 4 | DB 连接池使用 | Gauge | < 90% |
| 5 | Redis 快取命中率 | Stat | > 92% |
| 6 | 服务器资源 (CPU/MEM/DISK) | Multi-Stat | < 80% |
| 7 | 10 个 Skills 状态 | Table | 全部 OK |
| 8 | Kimi AI 集成状态 | Card | Connected |
| 9 | 部署历史 | Table | 最新 3 个 |
| 10 | 告警活动 | Alert List | 实时 |

#### 3.2 8 个核心指标详解（15 分钟）

**指标 1: API 响应时间**
```
查询: histogram_quantile(0.95, api_response_time)
目标: P95 < 500ms
警告: P95 > 500ms (10 分钟)
临界: P95 > 1000ms (5 分钟)
行动: 检查慢查询，优化代码
```

**指标 2: API 吞吐量**
```
查询: rate(http_requests_total[5m])
基线: 77.8 req/s
警告: < 50 或 > 150 req/s
行动: 检查异常流量或服务故障
```

**指标 3-8: 其他指标**
(类似的格式，涵盖 DB、Cache、CPU、Memory、Disk、Kimi)

#### 3.3 告警响应流程（10 分钟）

**当告警触发时的操作**:

```
告警触发
  ↓
收到 Slack 通知
  ↓
打开仪表板 (Grafana 或 Datadog)
  ↓
识别问题类型:
  │
  ├─ 🔴 Critical (需要立即行动)
  │   └─ 高错误率 → 检查应用日志
  │   └─ DB 连接池满 → 检查连接泄漏
  │   └─ 磁盘满 → 清理日志，扩展磁盘
  │
  └─ 🟡 Warning (监控并计划修复)
      └─ 高延迟 → 优化查询
      └─ 高内存使用 → 检查泄漏
      └─ 快取命中率低 → 增加快取
  ↓
查询日志和追踪:
  kubectl logs -n longhun-prod <pod-name>
  Jaeger: http://jaeger:16686
  ↓
执行修复:
  - 若需要紧急回滚: kubectl rollout undo
  - 若需要重启: kubectl delete pod <pod-name>
  - 若需要调整配置: kubectl edit deployment
  ↓
确认恢复:
  - 告警清除
  - 指标恢复正常
  - 发送恢复通知
```

### 练习题
1. 如何打开 Grafana 仪表板？
2. 当 P95 延迟超过 500ms 时应该检查什么？
3. Kimi API 延迟高时的回退策略是什么？

---

## 🔧 第 4 课：故障排查和应急（30 分钟）

### 课程目标
- 快速诊断常见问题
- 执行应急操作
- 进行快速回滚

### 课程内容

#### 4.1 常见故障和诊断（15 分钟）

**问题 1: 部署后 API 无响应**

```
症状: GET /health → 连接超时

诊断步骤:
1. 检查 Pod 状态
   kubectl get pods -n longhun-prod
   结果: 检查是否都是 Running 且 Ready

2. 查看 Pod 日志
   kubectl logs -n longhun-prod <pod-name> --tail=100
   查找: panic, error, exception

3. 检查资源限制
   kubectl describe pod <pod-name>
   查找: OOMKilled, CrashLoopBackOff

4. 检查网络连接
   kubectl exec -it <pod-name> -- curl localhost:8443/health

修复方案:
  Option A: 重启 Pod
    kubectl delete pod <pod-name>
  Option B: 回滚部署
    kubectl rollout undo deployment/longhun-prod
```

**问题 2: 数据库连接失败**

```
症状: error: "failed to connect to database"

诊断步骤:
1. 检查数据库服务状态
   psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "SELECT 1;"

2. 检查连接池设置
   SELECT count(*) FROM pg_stat_activity;
   (检查是否达到 max_connections)

3. 检查防火墙规则
   nc -zv $DB_HOST 5432

修复方案:
  Option A: 增加连接池大小
    kubectl set env deployment/longhun-prod DB_POOL_SIZE=30
  Option B: 重启 DB 连接
    kubectl delete pod <db-pod-name>
```

**问题 3: 内存使用率突增**

```
症状: 内存使用 > 80%，应用变慢

诊断步骤:
1. 使用 Prometheus 查询
   node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes

2. 检查 Pod 内存使用
   kubectl top pods -n longhun-prod --sort-by=memory

3. 查看内存分配情况
   kubectl exec <pod-name> -- ps aux

修复方案:
  Option A: 重启消耗内存的 Pod
    kubectl delete pod <pod-name>
  Option B: 增加内存限制
    kubectl set resources deployment/longhun-prod \
      --limits=memory=8Gi
```

#### 4.2 应急回滚程序（15 分钟）

**场景: 部署 5 分钟后发现严重问题**

```
步骤 1: 决策 (< 1 分钟)
  确认问题的严重性
  检查告警仪表板
  与团队确认是否需要回滚

步骤 2: 执行回滚 (< 2 分钟)
  命令: kubectl rollout undo deployment/longhun-prod
  验证: kubectl rollout status deployment/longhun-prod

步骤 3: 验证恢复 (< 2 分钟)
  检查: GET /health → 200 OK
  检查: 所有 Pod 处于 Running 状态
  检查: 指标恢复正常

步骤 4: 通知和分析 (< 5 分钟)
  发送回滚通知至 Slack
  记录回滚原因
  安排事后分析会议

总耗时: < 10 分钟
```

**快速回滚命令参考**:

```bash
# 查看部署历史
kubectl rollout history deployment/longhun-prod

# 回滚到上一个版本
kubectl rollout undo deployment/longhun-prod

# 回滚到特定版本
kubectl rollout undo deployment/longhun-prod --to-revision=3

# 暂停部署以进行调查
kubectl rollout pause deployment/longhun-prod

# 恢复部署
kubectl rollout resume deployment/longhun-prod

# 监控回滚进度
kubectl rollout status deployment/longhun-prod --watch
```

### 练习题
1. 如果 Pod 处于 CrashLoopBackOff 状态怎么办？
2. 如何快速回滚到上一个工作版本？
3. 回滚需要多久时间？

---

## 📚 附录：快速参考

### A. 关键命令

```bash
# 部署管理
kubectl get deployment -n longhun-prod
kubectl describe deployment longhun-prod -n longhun-prod
kubectl set image deployment/longhun-prod longhun=<new-image>

# Pod 管理
kubectl get pods -n longhun-prod
kubectl logs -n longhun-prod <pod-name>
kubectl exec -it <pod-name> -n longhun-prod -- /bin/bash

# 监控
kubectl top nodes
kubectl top pods -n longhun-prod

# 故障排查
kubectl describe pod <pod-name> -n longhun-prod
kubectl get events -n longhun-prod --sort-by='.lastTimestamp'
```

### B. 关键联系方式

```
Deployment Lead:  [名称] [电话] [Slack]
Monitoring Lead:  [名称] [电话] [Slack]
Database Lead:    [名称] [电话] [Slack]
Support Lead:     [名称] [电话] [Slack]

Slack Channel:    #deployment-live
PagerDuty:        longhun-deployment-oncall
```

### C. 重要文档

- DEPLOYMENT_RUNBOOK_FOR_TEAM.md (1,238 行)
- PRODUCTION_DEPLOYMENT_GUIDE.md
- MONITORING_DEPLOYMENT_GUIDE.md
- KIMI_INTEGRATION_GUIDE.md

---

## 📋 评估和认证

### 培训评估 (40 分)

```
第 1 课 (10 分): 系统架构理解
  □ 能描述 10 个 Skills
  □ 理解蓝绿部署策略
  □ 知道 27 步部署流程

第 2 课 (15 分): 部署演练
  □ 能执行完整部署
  □ 理解每个阶段的检查点
  □ 知道如何验证部署结果

第 3 课 (10 分): 监控运维
  □ 能读懂 Grafana 仪表板
  □ 理解 8 个核心指标
  □ 能响应告警

第 4 课 (5 分):  故障排查
  □ 能诊断常见问题
  □ 知道回滚流程
```

### 认证资格

```
及格分数: 32/40 (80%)

通过后可获得:
  ✅ 龍魂系统部署认证
  ✅ 可独立执行部署操作
  ✅ 可作为部署团队成员参与生产部署
```

---

## 后续学习

- Kubernetes 进阶管理
- Prometheus/Grafana 自定义配置
- Disaster Recovery 演练
- 性能优化深度课程
- Kimi AI 集成进阶

---

**DNA**:#龍芯⚡️丙午·甲午·癸丑·戊午·䷨损-TEAM-TRAINING-v1.0
**最后更新**: 2026-06-08
**版本**: 1.0
**准备者**: Tech Lead
