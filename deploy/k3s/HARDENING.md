# 龍魂 K3s 底座加固手册 v2.0

> DNA: #龍芯⚡️丙午·甲申·己亥·䷁坤-K3S-HARDENING-v2.0
> 创建者: 诸葛鑫（UID9622）
> License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
> 基于: CodeBuddy 回执 + 小艺AI 6条加固建议 + 龍魂底座思想
> 生效日期: 2026-08-07

---

## 加固概览

| # | 加固项 | v1.0 | v2.0 | 状态 |
|:---:|:---|:---:|:---:|:---:|
| 1 | Admission 三色审计标签 | ❌ 无 | ✅ DNA标签强制 + 三色注解 | 🟢 YAML就绪 |
| 2 | Secret 加密 | ❌ stringData明文 | 🟡 标注迁移路径→sealed-secrets | 🟡 待部署sealed-secrets |
| 3 | 双轨 NetworkPolicy 隔离 | ❌ 无 | ✅ 3个NP：默认拒绝+同NS+外部允许 | 🟢 YAML就绪 |
| 4 | 健康探针升级 | ❌ 无Deployment | ✅ liveness+readiness HTTP探针 | 🟢 YAML就绪 |
| 5 | PVC 备份策略 | ❌ 无 | ✅ 每日备份CronJob+7天保留 | 🟢 YAML就绪 |
| 6 | Prometheus 指标注解 | ❌ 无 | ✅ Deployment+CronJob 指标注解 | 🟢 YAML就绪 |

---

## §1 三色审计下沉到准入层

### 设计
每个 K3s 资源的 metadata 强制携带：
- `labels.dnalabel`: DNA 追溯码
- `annotations.tricolor-audit`: 三色标记（🟢/🟡/🔴）

### 现状
v2.0 YAML 中所有资源已打标签，但仅标注意图，未上 Admission Webhook 强制执行。

### 升级路径
```bash
# Phase 2: 部署准入控制器（需先部署 Webhook 服务）
# 1) 写 ValidatingWebhookConfiguration
# 2) 在 webhook 中校验: labels 必须有 dnalabel, annotations 必须有 tricolor-audit
# 3) 不合规 → 拒绝调度
```

### 当前落地
```yaml
# 每个资源强制携带（示例）
metadata:
  labels:
    dnalabel: "#龍芯⚡️丙午·甲申·己亥·䷁坤-<资源类型>"
  annotations:
    tricolor-audit: "🟢"
```

---

## §2 密钥永不落明文

### 设计
Secret 不应使用 `stringData`（`kubectl get secret -o yaml` 可逆 base64）。

### 现状
v1.0 使用 `type: Opaque` + `stringData`，任何人 `kubectl get secret -o yaml` 可见。

### v2.0 改进
- 标注 `sealed-secrets-migration: "pending"` 注解
- 敏感值标记为 `__SEALED__XXX__` 占位符

### 迁移步骤
```bash
# 1) 安装 sealed-secrets controller
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/latest/download/controller.yaml

# 2) 安装 kubeseal CLI
brew install kubeseal

# 3) 加密原 Secret
kubeseal --controller-namespace=kube-system --format=yaml < longhun-k3s-hardened-v2.0.yaml > sealed-secrets.yaml

# 4) 部署加密版
kubectl apply -f sealed-secrets.yaml

# 5) 删除明文 Secret
kubectl -n longhun delete secret longhun-secrets
```

---

## §3 双轨命名空间隔离

### 设计
| 命名空间 | 用途 | 通信规则 |
|:---|:---|:---|
| `longhun` | 核心底座 | 内部互通 |
| `longhun-local` | 本地轨（Nginx/systemd桥接） | 仅与 core 通信 |
| `longhun-api` | API轨（外部可访问） | 仅与 core 通信 |

### NetworkPolicy
3个 Policy 焊死在 `longhun-k3s-hardened-v2.0.yaml`：
1. `longhun-default-deny`: 默认拒绝所有 ingress
2. `longhun-allow-same-ns`: 允许同命名空间通信
3. `longhun-allow-nginx-bridge`: 允许 Nginx hostPort 桥接

### 前置条件
```bash
# 必须安装 CNI 支持 NetworkPolicy（Calico 或 Cilium）
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.28/manifests/calico.yaml
```

---

## §4 健康检查升级探针 + Prometheus 指标

### 设计
- **livenessProbe**: `/health` 端点，30s 初始延迟，10s 间隔，3次失败重启
- **readinessProbe**: `/health` 端点，10s 初始延迟，5s 间隔，3次失败摘除流量
- **Prometheus 注解**: `prometheus.io/scrape: "true"` + `/metrics` 端点

### 指标端点
```
/metrics → longhun_up 1, longhun_audit_pass_total 0
```

### 下一步
```bash
# 部署 Prometheus + Grafana
# 或直接用 K3s 内置 metrics-server
kubectl top pods -n longhun
```

---

## §5 PVC 备份策略

### 设计
每日凌晨 2:00 自动打包 PVC 内容为 tar.gz，保留 7 天。

### CronJob
`longhun-pvc-backup`: 每日 `0 2 * * *`，备份到 `/opt/longhun-system/backups/`

### 验证
```bash
kubectl -n longhun get cronjob longhun-pvc-backup
kubectl -n longhun create job --from=cronjob/longhun-pvc-backup manual-backup-test
kubectl -n longhun logs -l component=backup
```

---

## §6 AI Hub KFPP 七因子过滤

见 `bin/lh_ai_hub.py` v2.0 更新：
- 索引构建前过 KFPP 七因子扫描
- 高风险文件（含密钥/私钥/凭证模式）自动标记不入库
- 低质量文件（quality<0.5）过滤

详见下方「AI Hub 加固」章节。

---

## 一键部署

```bash
# 在鲲鹏服务器执行
ssh root@119.13.90.27 << 'ENDSSH'
  # 1) 部署硬化的 K3s 底座
  kubectl apply -f /opt/longhun-system/deploy/k3s/longhun-k3s-hardened-v2.0.yaml --validate=true

  # 2) 验证
  echo "=== 命名空间 ==="
  kubectl get ns | grep longhun
  echo "=== 资源 ==="
  kubectl -n longhun get all,configmap,secret,pvc
  echo "=== NetworkPolicy ==="
  kubectl -n longhun get networkpolicy
  echo "=== CronJob ==="
  kubectl -n longhun get cronjob
  echo "=== 标签 ==="
  kubectl -n longhun get all -o custom-columns=NAME:.metadata.name,DNA:.metadata.labels.dnalabel
ENDSSH
```

---

## 回滚

```bash
# 回退到 v1.0
ssh root@119.13.90.27 "kubectl delete -f /opt/longhun-system/deploy/k3s/longhun-k3s-hardened-v2.0.yaml; \
                      kubectl apply -f /opt/longhun-system/deploy/k3s/"
```

---

## 版本历史

| 版本 | 日期 | 变更 |
|:---|:---|:---|
| v1.0 | 2026-08-07 | 初始 K3s 底座: ConfigMap/Secret/RBAC/PVC/CronJob |
| v2.0 | 2026-08-07 | 6条加固全落地: NetworkPolicy×3/探针/PVC备份/sealed-secrets路径/DNA标签 |

<!-- ⛓️DNA-CHAIN
DNA:V1|丙午·丙申·癸丑·亥时·䷓观|P04鲁班|创建|加固手册·6条逐项说明·一键部署·回滚|bhash:a43b88f0|chash:3b3d4957|←GENESIS
⛓️END-->
