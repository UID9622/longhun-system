# LH-SECURITY v1.0 · 龍魂主权技术栈·安全规范
DNA: #龍芯⚡️2026-08-31-LH-SECURITY-V1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: MulanPSL v2（工程实现层）

## 核心原则
1. **本地优先**：敏感数据不出本机，联网是功能而非依赖
2. **最小权限**：每个服务只获得完成任务所需的最小权限（PoLP）
3. **零信任**：任何内部请求都需验证身份（Zero Trust Architecture）
4. **供应链安全**：每次构建生成 SBOM，追踪所有依赖

## 铁律（不可违反）
- 🔴 密钥绝不进 Git 仓库（`.gitignore` 必须包含 `.env` / `*.key` / `mcp.json`）
- 🔴 生产环境必须使用 HTTPS/TLS 1.3
- 🔴 API Key 至少 32 字符随机生成
- 🔴 外部依赖必须经过评估器（evaluator）审批

## 身份认证标准
| 场景 | 方案 | 标准 |
|---|---|---|
| API 网关 | Bearer Token (X-API-Key) | RFC 6750 |
| 服务间通信 | mTLS | RFC 8446 |
| 用户登录 | 手机号 + 短信验证码 | 国内标准 |
| 管理员 | GPG 签名 + TOTP | RFC 4880 + RFC 6238 |

## 加密标准
| 数据类型 | 算法 | 备注 |
|---|---|---|
| 传输加密 | TLS 1.3 | 强制 |
| 存储加密 | AES-256-GCM | 静态数据 |
| 哈希追溯 | SHA-256 | DNA追溯码 |
| 签名验证 | RSA-4096 / Ed25519 | GPG |

## 安全扫描流程

```bash
# 每次发布前执行
syft . -o json > sbom.json              # 生成 SBOM
grype sbom.json                          # 漏洞扫描
semgrep --config=auto .                  # 静态代码分析（SAST）
trivy image sovereign-gateway:latest    # 容器镜像扫描
```

## 三色安全审计
🟢 所有检查通过·可发布
🟡 有低风险警告·需记录·可发布
🔴 有高危漏洞·禁止发布·立即修复
