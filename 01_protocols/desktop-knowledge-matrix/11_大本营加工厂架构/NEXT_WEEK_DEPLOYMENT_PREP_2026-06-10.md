# 🚀 下周部署准备计划
# 日期: 2026-06-10 (周三)
# DNA:#龍芯⚡️丙午·丙申·庚申·亥时-NEXT-WEEK-DEPLOYMENT-PREP-v1.0
# 版本: 1.0·执行版

---

## 📋 下周日程 (06-11 ~ 06-15)

| 日期 | 任务 | 时间 | 状态 | 负责人 |
|------|------|------|------|--------|
| 周四 06-12 | **凭证收集 + 环境准备** | 2h | 📋 待执行 | UID9622 |
| 周五 06-13 | **团队培训** | 4-5h | 📋 待执行 | 团队 |
| 周六 06-14 | **部署演练** | 2-3h | 📋 待执行 | 团队 |
| 周日 06-15 | **生产部署 / 自动周检查** | 3-4h | 📋 待执行 | 团队 |

---

## 🔑 第 1 步：凭证收集 (周四 06-12)

### 需要的 3 个 API Key

#### 1️⃣ Datadog API Key
```
获取地址: https://app.datadoghq.com/account/settings#api_keys
需要:
  □ Datadog API Key (用于指标上报)
  □ Datadog App Key (用于仪表板创建)
格式:
  DATADOG_API_KEY=<YOUR_KEY>
  DATADOG_APP_KEY=<YOUR_KEY>
```

#### 2️⃣ Slack Webhook URL
```
获取地址: https://api.slack.com/messaging/webhooks
需要:
  □ Webhook URL (用于告警通知)
  □ 选择接收告警的频道
格式:
  SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
```

#### 3️⃣ PagerDuty API Key
```
获取地址: https://app.pagerduty.com/api_keys
需要:
  □ API Key (用于 Critical 告警触发)
  □ Service ID (龍魂系统对应的服务)
格式:
  PAGERDUTY_API_KEY=<YOUR_KEY>
  PAGERDUTY_SERVICE_ID=<YOUR_SERVICE_ID>
```

### 配置文件位置

将凭证配置到以下位置之一（推荐第一种）：

**方式 1：环境变量 (推荐·生产标准)**
```bash
# 编辑 ~/.bashrc 或 ~/.zshrc
export DATADOG_API_KEY="<YOUR_KEY>"
export DATADOG_APP_KEY="<YOUR_KEY>"
export SLACK_WEBHOOK_URL="<YOUR_URL>"
export PAGERDUTY_API_KEY="<YOUR_KEY>"
export PAGERDUTY_SERVICE_ID="<YOUR_SERVICE_ID>"

# 重新加载
source ~/.bashrc
```

**方式 2：Kubernetes Secret (K8s 部署)**
```bash
kubectl create secret generic monitoring-credentials \
  --from-literal=datadog-api-key=<YOUR_KEY> \
  --from-literal=slack-webhook=<YOUR_URL> \
  --from-literal=pagerduty-api-key=<YOUR_KEY> \
  -n monitoring
```

**方式 3：配置文件 (不推荐·安全风险)**
```
仅用于本地开发测试，生产环境禁止
```

### 验证凭证有效性

```bash
# 测试 Datadog
curl -X GET "https://api.datadoghq.com/api/v1/validate" \
  -H "DD-API-KEY: ${DATADOG_API_KEY}"

# 测试 Slack
curl -X POST "${SLACK_WEBHOOK_URL}" \
  -H 'Content-type: application/json' \
  -d '{"text":"Test from LongHun"}'

# 测试 PagerDuty
curl -X GET "https://api.pagerduty.com/users" \
  -H "Authorization: Token token=${PAGERDUTY_API_KEY}"
```

---

## 🏗️ 第 2 步：环境准备 (周四 06-12)

### 生产部署环境清单

#### 基础设施检查
```
□ Kubernetes 集群
  □ 版本: v1.24+
  □ 节点数: ≥3
  □ 可用 CPU: ≥8 cores
  □ 可用内存: ≥16 GB
  □ 可用存储: ≥100 GB

□ 网络配置
  □ DNS 就绪
  □ 负载均衡器 (LB) 就绪
  □ SSL/TLS 证书就绪
  □ VPC 网络隔离

□ 数据库
  □ PostgreSQL 12+ (连接串已备)
  □ Redis 6+ (连接串已备)
  □ 数据库备份策略已定义
  □ 备份文件可恢复 (测试过)
```

#### 监控系统准备
```
□ Prometheus
  □ 存储配置: ≥100GB
  □ 保留期: ≥30天
  □ 抓取间隔: 30s

□ Grafana
  □ 数据源已配置
  □ 仪表板 JSON 已导入
  □ 用户权限已配置

□ Datadog
  □ Organization 已创建
  □ Agent 版本: 最新
  □ 指标命名空间: longhun.*
```

#### 通知系统准备
```
□ Slack
  □ 工作区已创建
  □ 告警频道已创建 (#longhun-alerts)
  □ Webhook 已验证

□ PagerDuty
  □ Team 已创建
  □ Service 已创建
  □ Integration Key 已获取

□ Email
  □ 邮箱服务已配置
  □ 发件人地址已验证
  □ SMTP 服务可用
```

### 环境变量验证清单

```bash
# 验证所有必要的环境变量
ENV_VARS=(
  "KIMI_API_KEY"
  "DATADOG_API_KEY"
  "DATADOG_APP_KEY"
  "SLACK_WEBHOOK_URL"
  "PAGERDUTY_API_KEY"
  "PAGERDUTY_SERVICE_ID"
  "DATABASE_URL"
  "REDIS_URL"
)

for var in "${ENV_VARS[@]}"; do
  if [ -z "${!var}" ]; then
    echo "❌ $var 未设置"
  else
    echo "✅ $var 已设置"
  fi
done
```

---

## 👥 第 3 步：团队培训 (周五 06-13)

### 培训日程 (4-5 小时)

#### 上午 (09:00 - 12:00)
```
09:00 - 09:45  课程 1: 系统架构
  • 龍魂系统整体设计
  • 3 大关键组件 (Kimi/监控/部署)
  • 故障转移机制

09:45 - 10:45  课程 2: 27 步蓝绿部署流程
  • 部署架构说明
  • 逐步演练 (模拟环境)
  • 常见错误排查

10:45 - 11:30  课程 3: 监控系统使用
  • Prometheus/Grafana/Datadog 基本操作
  • 告警规则理解
  • 仪表板读取

11:30 - 12:00  课程 4: 故障排查·应急回滚
  • 故障模拟
  • 诊断步骤
  • 应急回滚流程 (5 分钟内完成)
```

#### 下午 (14:00 - 16:00+)
```
14:00 - 15:30  实践练习
  • 在 Staging 环境执行完整部署
  • 每个团队成员动手操作
  • 讲师现场指导

15:30 - 16:00+ 认证考试
  • 12 题选择题 (40 分)
  • 1 次完整部署演练
  • 通过分数: ≥32 分 (80%)
```

### 培训资料位置

```
完整培训计划: ~/longhun-system/training/TEAM_TRAINING_PROGRAM.md (4,500+ 字)
部署清单: ~/longhun-system/deployment/BLUE_GREEN_DEPLOYMENT_27_STEPS.md
故障排查: ~/longhun-system/deployment/BLUE_GREEN_DEPLOYMENT_27_STEPS.md 最后章节
认证系统: 内置于培训程序
```

### 培训准备清单

```
□ 讲师准备
  □ 讲师审核所有教材
  □ 准备演示环境 (Staging)
  □ 准备备份讲义

□ 学员准备
  □ 发送培训邀请和材料
  □ 准备好笔记本和实验环境账号
  □ 提前 1 天发送日程提醒

□ 环境准备
  □ Staging 集群清空 (清除上次测试数据)
  □ 所有 API Key 已配置
  □ 网络连接测试 (所有人可访问 Staging)

□ 考试准备
  □ 准备 12 题考题
  □ 准备 Staging 环境用于部署演练
  □ 准备评分表
```

---

## 🧪 第 4 步：部署演练 (周六 06-14)

### 演练目标

```
✅ 所有团队成员熟悉 27 步部署流程
✅ 能够在 10 分钟内从清单快速查找步骤
✅ 知道如何诊断故障
✅ 知道如何在 2-5 分钟内回滚
```

### 演练日程 (2-3 小时)

```
09:00 - 10:00  完整部署演练 (第 1 轮)
  • 按照 27 步清单逐步执行
  • 讲师观察和点评
  • 记录遇到的问题

10:00 - 11:00  故障模拟 + 应急回滚
  • 模拟 3 个常见故障场景
  • 团队成员诊断故障
  • 执行应急回滚

11:00 - 12:00  问题复盘 + 改进
  • 讨论遇到的问题
  • 更新清单和文档
  • 确认下周生产部署流程
```

### 演练清单

```
□ Staging 环境清空
□ 所有必要的 API Key 已配置
□ 部署清单已打印 (每人一份)
□ 故障模拟场景已准备
□ 回滚脚本已测试
□ 监控仪表板已就绪 (用于监控部署过程)
```

---

## 🚀 第 5 步：生产部署 (周日 06-15)

### 部署计划 (3-4 小时)

#### Phase 1: 部署前准备 (30 分钟)
```
□ 备份当前生产数据
□ 检查所有 API Key
□ 验证 SSL 证书有效性
□ 确认网络连接正常
□ 最后一次检查部署清单
```

#### Phase 2: 构建绿色环境 (30 分钟)
```
□ 构建 Docker 镜像
□ 推送镜像到仓库
□ 在生产环境拉取镜像
□ 验证镜像完整性
```

#### Phase 3: 启动绿色实例 (20 分钟)
```
□ 部署绿色实例 (3 个 Pod)
□ 验证实例启动成功
□ 运行烟雾测试 (3 个关键接口)
□ 确认实例健康
```

#### Phase 4: 流量转移 (30 分钟)
```
□ 10% 流量 → 绿色 (验证 5 分钟)
□ 25% 流量 → 绿色 (验证 5 分钟)
□ 50% 流量 → 绿色 (验证 5 分钟)
□ 75% 流量 → 绿色 (验证 5 分钟)
□ 100% 流量 → 绿色 (验证 5 分钟)
```

#### Phase 5: 验证和监控 (60 分钟)
```
□ 8 项健康检查全部通过
□ 所有关键指标正常
□ 告警系统工作正常
□ 部署历史已记录
```

#### Phase 6: 蓝色下线 (15 分钟)
```
□ 蓝色实例保留待命 (24 小时)
□ 监控蓝色实例内存占用 (防止被回收)
□ 记录蓝色实例版本信息 (用于快速回滚)
```

### 部署检查清单

```
✅ 部署前检查 (4/4)
  □ 数据备份: 完成
  □ SSL 证书: 有效
  □ API Key: 验证通过
  □ 网络连接: 正常

✅ 蓝绿部署 (5/5)
  □ 镜像构建: 完成
  □ 绿色实例: 就绪
  □ 烟雾测试: 通过
  □ 流量转移: 完成
  □ 蓝色待命: 保留

✅ 健康检查 (8/8)
  □ API 连接: ✅
  □ 数据库: ✅
  □ Redis: ✅
  □ Kimi API: ✅
  □ 磁盘空间: ✅
  □ 内存使用: ✅
  □ CPU 使用: ✅
  □ DNS 解析: ✅

✅ 监控激活 (4/4)
  □ Prometheus: 规则加载
  □ Grafana: 仪表板可见
  □ Datadog: 指标采集
  □ 告警通知: 工作正常
```

---

## 📋 凭证清单模板

创建文件 `~/.longhun/secrets.env` (仅本地·禁止提交 Git)

```bash
# ⚠️ 安全提醒: 此文件包含敏感信息，不要提交到 Git
# 龍魂/CNSH 主权变量规范 · UID9622

# Kimi AI
export KIMI_API_KEY="<YOUR_KIMI_API_KEY>"

# Notion 知识底座
export NOTION_TOKEN="<YOUR_NOTION_TOKEN>"
export DB_LU="<YOUR_BRAIN_DATABASE_ID>"
export DB_JQ="<YOUR_AUDIT_DATABASE_ID>"
export DB_AL="<YOUR_MULTICURRENCY_DATABASE_ID>"
export DB_PUB="<YOUR_PUBLIC_PAGE_ID>"
export DB_CLOUD="<YOUR_TEAM_DATABASE_ID>"

# 身份与加密
export GPG_FINGERPRINT="<YOUR_GPG_FINGERPRINT>"
export LONGHUN_CONFIRM_CODE="<YOUR_CONFIRM_CODE>"

# 大本营/工厂
export CAMP_IP="<YOUR_CAMP_IP>"
export LONGHUN_FACTORY_ID="<YOUR_FACTORY_ID>"

# Datadog (获取地址: https://app.datadoghq.com/account/settings)
export DATADOG_API_KEY="<YOUR_DATADOG_API_KEY>"
export DATADOG_APP_KEY="<YOUR_DATADOG_APP_KEY>"

# Slack (获取地址: https://api.slack.com/messaging/webhooks)
export SLACK_WEBHOOK_URL="<YOUR_SLACK_WEBHOOK_URL>"

# PagerDuty (获取地址: https://app.pagerduty.com/api_keys)
export PAGERDUTY_API_KEY="<YOUR_PAGERDUTY_API_KEY>"
export PAGERDUTY_SERVICE_ID="<YOUR_PAGERDUTY_SERVICE_ID>"

# 数据库
export DATABASE_URL="postgresql://user:pass@host:5432/longhun"
export LONGHUN_DB_PASSWORD="<YOUR_DB_PASSWORD>"
export LONGHUN_REDIS_PASSWORD="<YOUR_REDIS_PASSWORD>"
```

使用方式：
```bash
source ~/.longhun/secrets.env
# 现在所有环境变量都可用了
```

---

## ✅ 下周准备完成清单

### 周四 06-12 (凭证 + 环境准备)
```
□ 从 Datadog 获取 API Key
□ 从 Slack 获取 Webhook URL
□ 从 PagerDuty 获取 API Key
□ 验证所有凭证有效性
□ 配置环境变量 (方式 1: ~/.bashrc)
□ 检查 Kubernetes 集群状态
□ 验证数据库和 Redis 连接
□ 确认网络和防火墙配置
```

### 周五 06-13 (团队培训)
```
□ 全体团队成员参加 (4-5 小时)
□ 4 个课程全部讲授
□ 所有成员完成实践演练
□ 所有成员通过认证考试 (≥32 分)
□ 记录任何遇到的问题和改进建议
```

### 周六 06-14 (部署演练)
```
□ Staging 环境清空
□ 完成 3 次完整部署演练
□ 模拟 3 个故障场景
□ 验证应急回滚流程
□ 复盘遇到的问题
□ 更新部署文档
```

### 周日 06-15 (生产部署)
```
□ 早上 09:00 开始部署前检查
□ 10:00 开始构建绿色环境
□ 11:00 开始流量转移
□ 12:30 完成 100% 流量转移
□ 13:00 完成健康检查和监控激活
□ 保留蓝色实例 24 小时待命
□ 生成部署报告
□ 自动周检查 (晚上自动运行)
```

---

## 📞 关键联系方式

### 技术支持
- **Kimi 技术支持**: https://www.moonshot.cn/support
- **Datadog 文档**: https://docs.datadoghq.com/
- **Slack API**: https://api.slack.com/docs
- **PagerDuty 文档**: https://developer.pagerduty.com/

### 团队联系
```
部署负责人: (待定)
监控负责人: (待定)
备用负责人: (待定)

紧急联系电话: (待定)
```

---

## 🎯 成功标准

部署成功的定义：

```
✅ 没有 Critical 告警触发
✅ 所有 8 项健康检查通过
✅ API 响应时间 P95 < 500ms
✅ 错误率 < 0.1%
✅ 缓存命中率 > 80%
✅ 所有 10 个 Skill 正常工作
✅ Kimi API 连接成功
✅ 告警通知系统工作正常
✅ 部署历史正确记录
✅ 蓝色实例成功保留 (待命中)
```

---

## 📝 文档参考

| 文档 | 位置 | 用途 |
|------|------|------|
| Kimi 验证报告 | `KIMI_VERIFICATION_REPORT_2026-06-10_UPDATED.md` | 理解 Kimi 集成现状 |
| 监控验证报告 | `MONITORING_VERIFICATION_REPORT_2026-06-10.md` | 理解监控系统配置 |
| 生产就绪检查 | `PRODUCTION_READINESS_CHECKLIST.md` | 部署前完整检查 |
| 蓝绿部署流程 | `deployment/BLUE_GREEN_DEPLOYMENT_27_STEPS.md` | 部署执行步骤 |
| 部署指南 | `monitoring/MONITORING_DEPLOYMENT_GUIDE.md` | 监控系统部署 |
| 培训计划 | `training/TEAM_TRAINING_PROGRAM.md` | 团队培训资料 |

---

## ✅ 签署与确认

```
计划制定者: AI Agent (自动化系统)
制定时间: 2026-06-10 CST (周三)
计划版本: 1.0·执行版

下周日程: 周四-周日 (4 天完整准备)
总工作量: ~12-15 小时
人员需求: 1 个部署负责人 + 全体团队

预期成果:
  ✅ 所有凭证已获取和验证
  ✅ 团队全员认证通过
  ✅ 部署流程已演练 3 次
  ✅ 生产部署完成 (蓝绿无缝切换)
  ✅ 监控系统正常运作
  ✅ 告警通知系统就绪

下一步: 开始周四的凭证收集
```

---

**DNA**:#龍芯⚡️丙午·丙申·庚申·亥时-NEXT-WEEK-DEPLOYMENT-PREP-v1.0
**确认码**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**版本**: 1.0 (执行版)
**有效期**: 有效至 2026-06-17
