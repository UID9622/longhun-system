# 🐉 龍魂系统 生产部署指南 v1.0

## 概述

本指南详述如何使用 `production_deployment.py` 将龍魂系统部署至生产环境。

**DNA**: `#龍芯⚡️2026-06-08-PRODUCTION-DEPLOYMENT-GUIDE-v1.0`

---

## 系统需求

### 基础设施
- **计算**: 最少 4 核 CPU、8GB RAM （推荐 8 核、16GB）
- **存储**: 最少 100GB 可用磁盘空间
- **网络**: 稳定的互联网连接、HTTPS 支持
- **容器化**: Docker 20.10+ 或 Kubernetes 1.24+

### 外部服务
- **数据库**: PostgreSQL 12+ 或 MySQL 8.0+
- **缓存**: Redis 6.0+ 或 Memcached
- **监控**: Datadog/New Relic/Prometheus
- **日志**: Elasticsearch/Splunk/Cloudwatch
- **密钥管理**: HashiCorp Vault 或 AWS Secrets Manager

### 软件依赖
```bash
Python 3.11+
Docker 20.10+
kubectl 1.24+ (如使用 Kubernetes)
git 2.30+
```

---

## 部署前准备清单

### 1. 配置准备

- [ ] 准备生产数据库凭证
- [ ] 配置 Redis/Memcached 端点
- [ ] 获取有效的 SSL/TLS 证书
- [ ] 配置监控和日志聚合服务
- [ ] 设置 API 密钥和认证密钥
- [ ] 准备备份和恢复计划

### 2. 环境准备

- [ ] 配置防火墙规则
- [ ] 设置负载均衡器
- [ ] 配置 DNS 记录
- [ ] 准备蓝绿环境（两套独立的生产环境）
- [ ] 验证网络连接和延迟

### 3. 安全检查

- [ ] 进行安全扫描（OWASP Top 10）
- [ ] 验证 SSL/TLS 配置
- [ ] 测试认证和授权机制
- [ ] 配置日志审计
- [ ] 准备应急事件响应计划

### 4. 测试准备

- [ ] 准备烟雾测试清单
- [ ] 配置健康检查端点
- [ ] 准备回滚计划
- [ ] 进行压力测试
- [ ] 验证监控和告警

---

## 生产配置

### 配置模板

```python
prod_config = {
    # API 配置
    "environment": "production",
    "api_host": "api.longhun.example.com",
    "api_port": 8443,

    # 数据库配置
    "db_host": "prod-postgresql.example.com",
    "db_port": 5432,
    "db_name": "longhun_production",
    "db_user": "longhun_app",
    "db_password": "***",  # 使用 Vault 注入

    # 缓存配置
    "redis_host": "prod-redis.example.com",
    "redis_port": 6379,

    # 监控和日志
    "monitoring_service": "datadog",        # 或 new-relic, prometheus
    "log_aggregation": "elasticsearch",     # 或 splunk, cloudwatch

    # SSL/TLS 配置
    "ssl_cert_path": "/etc/ssl/certs/longhun-prod.crt",
    "ssl_key_path": "/etc/ssl/private/longhun-prod.key",

    # 备份配置
    "backup_location": "/var/backups/longhun",

    # 部署配置
    "deployment_strategy": "blue-green",    # 或 rolling, canary
    "canary_percentage": 5,                 # 金丝雀部署比例
    "max_concurrent_connections": 10000,

    # Skills 配置
    "skills_enabled": 10,
}
```

### 环境变量

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

## 部署步骤

### 第一阶段：部署前准备 (15-30 分钟)

```bash
# 1. 克隆仓库
git clone https://github.com/UID9622/longhun-system.git
cd longhun-system

# 2. 检查部署前条件
python3 deployment/production_deployment.py --pre-check

# 3. 备份现有环境
./deployment/backup.sh

# 4. 验证配置
python3 deployment/production_deployment.py --validate-config
```

### 第二阶段：蓝绿部署 (30-60 分钟)

```bash
# 1. 启动部署
python3 deployment/production_deployment.py \
  --config=prod_config.json \
  --strategy=blue-green

# 2. 监控部署进度
tail -f /var/log/longhun/deployment.log

# 3. 验证绿色环境
curl -k https://api.longhun.example.com:8443/health

# 4. 执行烟雾测试
bash deployment/smoke_tests.sh

# 5. 逐步迁移流量
# 10% → 25% → 50% → 75% → 100%
```

### 第三阶段：验证和监控 (24 小时)

```bash
# 1. 监控指标
# 打开 Grafana/Datadog 仪表板

# 2. 检查日志
curl https://elasticsearch.example.com/longhun/_search

# 3. 验证所有端点
bash deployment/endpoint_verification.sh

# 4. 检查性能基准
curl https://api.longhun.example.com:8443/api/v1/metrics
```

---

## 部署流程详解

### 步骤 1: 部署前检查 (3-5 分钟)
```
✅ 配置验证 - 检查所有必要参数
✅ SSL 证书验证 - 验证证书有效性和有效期
✅ 密钥管理检查 - 确保所有密钥已安全配置
✅ 档案权限检查 - 验证所有文件权限正确
```

### 步骤 2: 数据库迁移 (5-10 分钟)
```
✅ 数据库备份 - 完整备份现有数据
✅ 数据库连接 - 验证连接和权限
✅ 执行迁移 - 运行所有数据库迁移指令码
✅ 数据验证 - 验证数据完整性和一致性
```

### 步骤 3: 安全加固 (5-10 分钟)
```
✅ 防火墙规则 - 配置入站和出站规则
✅ CORS 配置 - 限制允许的源
✅ 速率限制 - 配置 API 速率限制
✅ 审计日志 - 启用所有 API 调用日志
```

### 步骤 4: 蓝绿部署 (10-20 分钟)
```
✅ 构建绿色环境 - 构建新 Docker 镜像
✅ 启动绿色实例 - 启动 3 个绿色环境实例
✅ 烟雾测试 - 运行基本功能测试
✅ 流量迁移 - 逐步将流量转移至绿色
✅ 蓝色待命 - 保持蓝色环境以备回滚
```

### 步骤 5: 健康验证 (5-10 分钟)
```
✅ 性能检查 - 验证响应时间、吞吐量、延迟
✅ 端点验证 - 测试所有主要 API 端点
✅ 数据库检查 - 验证数据库连接和性能
✅ 快取检查 - 验证 Redis/Memcached 正常运行
```

### 步骤 6: 监控激活 (5-10 分钟)
```
✅ 监控服务集成 - 连接 Datadog/Prometheus
✅ 告警规则配置 - 配置 6 个关键告警
✅ 日志聚合 - 配置 Elasticsearch/Splunk
✅ 分布式追踪 - 启用 APM (Jaeger)
✅ 实时仪表板 - 部署 Grafana 仪表板
```

### 步骤 7: 部署后处理 (5-10 分钟)
```
✅ 部署记录 - 记录部署详情和指标
✅ 通知利益相关者 - 发送 Slack 通知、更新 JIRA
✅ 文档更新 - 更新 runbook 和文档
```

---

## 性能期望

### 部署指标
| 指标 | 值 | 目标 |
| --- | --- | --- |
| 部署耗时 | 30-60 分钟 | <90 分钟 |
| 健康检查通过率 | 100% | ≥95% |
| API 响应时间 | 15-20ms | <100ms |
| API 吞吐 | 77.8 req/s | ≥50 req/s |
| 可用性 | 99.95% | ≥99.9% |

### 资源消耗
| 资源 | 消耗 | 限制 |
| --- | --- | --- |
| CPU | 8-10% | <50% |
| 内存 | 35-40% | <80% |
| 磁盘 I/O | 低 | <70% |
| 网络带宽 | 低 | <50% |

---

## 回滚程序

### 快速回滚（<5 分钟）
```bash
# 方法 1: Kubernetes 回滚
kubectl rollout undo deployment/longhun-prod

# 方法 2: 蓝绿回滚
# 将流量从绿色环境转回蓝色环境
./deployment/switch_traffic_to_blue.sh

# 方法 3: 检查回滚状态
kubectl rollout status deployment/longhun-prod
```

### 完全回滚（数据库）
```bash
# 1. 停止应用
kubectl scale deployment/longhun-prod --replicas=0

# 2. 恢复数据库备份
mysql longhun_production < /var/backups/longhun/backup_2026-06-08.sql

# 3. 重启应用
kubectl scale deployment/longhun-prod --replicas=3

# 4. 验证
curl -k https://api.longhun.example.com:8443/health
```

---

## 监控和告警

### Grafana 仪表板
```
https://grafana.longhun.example.com/d/prod-overview
```

### 关键指标
- **API 响应时间** - P95 <100ms
- **错误率** - <1%
- **数据库连接** - <80%
- **CPU 使用** - <50%
- **内存使用** - <80%
- **磁盘空间** - >10% 可用

### 告警规则
| 告警 | 阈值 | 动作 |
| --- | --- | --- |
| 错误率 | >1% | 立即通知运维 |
| 响应时间 | P95 >500ms | 通知 SRE 团队 |
| DB 连接 | >80% | 警告 |
| 磁盘空间 | <10% | 警告 |
| SSL 证书 | 30 天内过期 | 通知 |

---

## 故障排查

### 部署失败
```bash
# 1. 检查日志
tail -f /var/log/longhun/deployment.log

# 2. 验证配置
python3 -c "import json; json.load(open('prod_config.json'))"

# 3. 检查先决条件
ping prod-postgresql.example.com
redis-cli -h prod-redis.example.com ping

# 4. 回滚
kubectl rollout undo deployment/longhun-prod
```

### 高错误率
```bash
# 1. 检查应用日志
kubectl logs -f deployment/longhun-prod

# 2. 检查数据库连接
mysql -h prod-postgresql.example.com -u longhun_app -p

# 3. 检查快取
redis-cli -h prod-redis.example.com INFO stats

# 4. 如需要，进行回滚
kubectl rollout undo deployment/longhun-prod
```

### 性能下降
```bash
# 1. 检查 CPU/内存使用
kubectl top pods -l app=longhun-prod

# 2. 检查数据库性能
EXPLAIN SELECT ...;

# 3. 检查快取命中率
redis-cli -h prod-redis.example.com INFO stats

# 4. 水平扩展
kubectl scale deployment/longhun-prod --replicas=5
```

---

## 最佳实践

### 部署前
- ✅ 在 Staging 环境中完全测试部署流程
- ✅ 准备详细的回滚计划
- ✅ 通知所有利益相关者
- ✅ 安排在低流量时段进行部署

### 部署期间
- ✅ 持续监控关键指标
- ✅ 准备好立即回滚
- ✅ 与团队保持沟通
- ✅ 遵循部署检查清单

### 部署后
- ✅ 监控 24 小时
- ✅ 验证所有功能
- ✅ 收集性能数据
- ✅ 更新文档和 runbook

---

## 联系和支援

- **部署问题**: 联系 SRE 团队
- **应用问题**: 联系开发团队
- **安全问题**: 联系安全团队
- **监控问题**: 联系运维团队

---

## 相关文件

- `demo_staging_deployment.py` - Staging 部署引擎
- `production_deployment.py` - 生产部署引擎
- `backup.sh` - 备份指令码
- `smoke_tests.sh` - 烟雾测试
- `endpoint_verification.sh` - 端点验证

---

**DNA**: `#龍芯⚡️2026-06-08-PRODUCTION-DEPLOYMENT-GUIDE-v1.0`
**确认**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
