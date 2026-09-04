# 龍魂 K3s 底座架构

> DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-K3S-DEPLOY-v1.0
> 创建者: 诸葛鑫（UID9622）
> License: MulanPSL v2
> 安装日期: 2026-08-07

## 架构概览

```
┌─────────────────────────────────────────────────┐
│                 K3s v1.36.3+k3s1                 │
│                  (ecs-d428)                       │
├─────────────────────────────────────────────────┤
│  Namespace: longhun                               │
│  ┌─────────────┬──────────────┬────────────────┐ │
│  │ ConfigMap   │ Secret       │ PVC (5Gi)      │ │
│  │ 核心配置     │ 密钥引用     │ 共享存储        │ │
│  └─────────────┴──────────────┴────────────────┘ │
│  ┌─────────────────────────────────────────────┐ │
│  │ Deployments                                  │ │
│  │  ├─ health-checker    (健康巡检·每分钟)       │ │
│  │  └─ [future] dashboard / api / worker        │ │
│  ├─────────────────────────────────────────────┤ │
│  │ CronJobs                                     │ │
│  │  └─ daily-audit       (每6h自动审计)         │ │
│  └─────────────────────────────────────────────┘ │
│                                                    │
│  ←→ Nginx (hostPort 80/443) ←→ 35+ systemd服务  │
│  ←→ Ollama (hostPort 11434)                      │
└─────────────────────────────────────────────────┘
```

## 文件清单

| 文件 | 说明 |
|:---|:---|
| `longhun-k3s-base.yaml` | ConfigMap·Secret·RBAC（L0焊死配置） |
| `longhun-k3s-services.yaml` | Deployment·CronJob·PVC（运行时服务） |

## 部署命令

```bash
# 一键部署
ssh root@119.13.90.27 "kubectl apply -f /opt/longhun-system/deploy/k3s/"

# 查看状态
kubectl -n longhun get all,configmap,secret,pvc

# 日志
kubectl -n longhun logs -l component=health-checker -f
```

## 迁移路线图

| 阶段 | 内容 | 状态 |
|:---:|------|:---:|
| Phase 0 | K3s 安装 + 命名空间 + 底座配置 | ✅ 完成 |
| Phase 1 | 健康巡检 + 定时审计 | ✅ 完成 |
| Phase 2 | Dashboard 迁移到 K3s Pod | 📋 计划 |
| Phase 3 | 知识中枢迁移 | 📋 计划 |
| Phase 4 | 记忆 API 迁移 | 📋 计划 |
| Phase 5 | 全量 systemd → K3s | 🔮 远期 |

## 设计原则

1. **渐进迁移**：不一次性推翻 35+ systemd 服务，逐步迁移
2. **底座先行**：先搭 ConfigMap/Secret/RBAC，服务逐步接入
3. **配置集中**：所有配置靠 K3s ConfigMap，不再散落各处
4. **自愈能力**：K3s 自动重启崩溃 Pod，健康检查持续监控
5. **审计不断**：CronJob 每 6 小时自动跑德本审计
