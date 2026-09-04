# LH-TERMINOLOGY v1.0 · 技术术语中英对照表
DNA: #龍芯⚡️2026-08-31-LH-TERMINOLOGY-V1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: MulanPSL v2（工程实现层）

## 龍魂系统专有术语
| 术语 | 说明 |
|---|---|
| DNA追溯码 | 格式 `#龍芯⚡️YYYY-MM-DD-模块-版本-UID9622`，每个操作/版本的唯一标识 |
| 三色审计 | 🟢通过 / 🟡待审 / 🔴拒绝，系统健康状态的三色评级 |
| 主权协议 | 用户对自己数据和账号的完整控制权声明 |
| Kill Switch | 紧急停止机制，L0 级别不可绕过 |
| CNSH | 中文结构化AI交互语法，龍魂自研语言 |

## 基础设施术语
| 英文 | 中文 | 说明 |
|---|---|---|
| API Gateway | API 网关 | 统一入口，鉴权·限流·路由 |
| Rate Limiting | 速率限制 | 防止滥用，每IP每分钟最多N次请求 |
| Token Bucket | 令牌桶 | 一种限流算法，平滑处理突发流量 |
| Reverse Proxy | 反向代理 | 网关代理后端服务 |
| Load Balancer | 负载均衡 | 将流量分发到多个实例 |
| Circuit Breaker | 熔断器 | 服务异常时自动切断，防止雪崩 |
| Exponential Backoff | 指数退避 | 失败后等待时间指数增长再重试 |
| Rate Limit (429) | 限流响应 | HTTP 429 Too Many Requests |
| SBOM | 软件物料清单 | Software Bill of Materials，列出所有依赖 |

## 安全术语
| 英文 | 中文 | 说明 |
|---|---|---|
| Zero Trust | 零信任 | 默认不信任任何内部请求 |
| PoLP | 最小权限原则 | Principle of Least Privilege |
| mTLS | 双向TLS | 客户端和服务端互相验证证书 |
| Bearer Token | 持票人令牌 | HTTP Authorization 头中的认证令牌 |
| SAST | 静态应用安全测试 | 扫描源代码中的安全漏洞 |
| Supply Chain | 供应链 | 代码依赖的完整链条 |

## 云原生术语
| 英文 | 中文 | 说明 |
|---|---|---|
| Container | 容器 | 隔离的运行环境（Docker） |
| Orchestration | 编排 | 管理多个容器（Kubernetes） |
| Liveness Probe | 存活探针 | K8s 检测服务是否存活 |
| Readiness Probe | 就绪探针 | K8s 检测服务是否可接收流量 |
| Namespace | 命名空间 | K8s 资源隔离单位 |
| Deployment | 部署 | K8s 管理无状态应用的方式 |
| HPA | 水平自动扩展 | Horizontal Pod Autoscaler |

## 计费术语
| 术语 | 说明 |
|---|---|
| 按量计费 | Pay-as-you-go，用多少付多少 |
| 包年包月 | 预付固定时间，单价更低但需提前承诺 |
| 预付费 | Prepaid，先充值后使用 |
| 后付费 | Postpaid，月末结算（龍魂不推荐，容易欠费） |
| 免费层 | Free Tier，每月固定免费额度，超出再付费 |
