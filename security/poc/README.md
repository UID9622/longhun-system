# security/poc · Issue #1627 PoC 验证集 v1.1

> DNA: `#龍芯⚡️2026-09-05-ISSUE1627-POC-RESPONSE-UID9622`
> 创建者: 诸葛鑫（UID9622）· 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层）· License(代码): MulanPSL v2
> 回应: deepseek-ai/DeepSeek-V3 Issue #1627 @m92ss「无 PoC → 不可证伪」批评
> 实测日期: 2026-09-05 · 三色: 🟢 两 CVE 均真实复现

## 目标漏洞（复现成功·非推断）

| CVE | 包 | 漏洞版本 | 漏洞点 | PoC |
|:---|:---|:---|:---|:---|
| CVE-2026-55604 | @arikusi/deepseek-mcp-server | 1.4.2（<1.7.0） | `SessionStore` 进程级单例 Map · `sessionId` 由调用者提供且不绑定主体 → 越权读他人会话；HTTP 层 `transports[sessionId]` 凭可控请求头 `mcp-session-id` 全局复用 → 会话可接管 | `poc_55604_sessionstore.mjs` |
| CVE-2026-55605 | 同上 | 1.4.2（<1.8.0） | `createHttpApp()` → `createMcpExpressApp({ host: '0.0.0.0' })` **无 authProvider** → POST /mcp 零认证 · 监听 0.0.0.0 · `/health` 泄露版本 | `poc_55605_noauth.sh` |

## 文件

- `poc_55604_sessionstore.mjs` — SessionStore 跨会话越权（node ≥18 直接跑，零三方依赖）
- `poc_55605_noauth.sh` — 一键复现：隔离目录装 v1.4.2 → 起 server → curl 三证据（无认证 initialize 200 / 会话接管 202 / /health 版本泄露）

## 实测输出（2026-09-05 真实跑通）

### 55604 SessionStore 越权
```
=== PoC 1/2 · CVE-2026-55604 · SessionStore 跨会话越权(无主体绑定) ===
[caller B] 从未创建该会话, 仅凭 sessionId 读到 A 的对话:
[{"role":"user","content":"我的银行卡密码是 9622, 请帮我管理财务"}]
[漏洞确认] 进程级单例 Map·sessionId 未绑定 caller 主体 → 越权读他人会话
```

### 55605 HTTP 无认证
```
=== 1) 无认证 POST /mcp initialize ===
HTTP/1.1 200 OK
mcp-session-id: d712ecdd-d3df-424c-b825-129b9b332237
=== caller B: 无认证带 A 的 session id 完成握手并调工具(会话接管) ===
initialized: 202
/health -> {"status":"ok","version":"1.4.2",...}
```

## 环境依赖与复现步骤

1. 依赖: node ≥18 · npm · 外网可达 `registry.npmjs.org`
2. 55604: `node security/poc/poc_55604_sessionstore.mjs`
3. 55605: `bash security/poc/poc_55605_noauth.sh`（脚本自建 mktemp 隔离目录·自动装包·自动清理·不触碰宿主任何既有依赖）

## 修复验证（加固对照）

| 修复版本 | 对照动作 |
|:---|:---|
| ≥1.8.0（官方） | `createMcpExpressApp` 应传 authProvider（OAuth 鉴权）；`/mcp` 未认证请求须 401 |
| ≥1.7.0（官方） | session_id 必须绑定认证主体，服务端生成且校验归属，拒绝外部指定 |
| 宿主加固 | HTTP transport 仅绑内网/127.0.0.1 · 反代层强制认证 · 升级后复跑本 PoC 应全失败 |

## 边界（诚实标注）

- 复现使用官方包源码+官方 SDK（@modelcontextprotocol/sdk 1.25.2），非自造代码
- server 仅绑 127.0.0.1 且用 dummy key · 无真实 DeepSeek API 调用 · 无公网暴露 · 数据全隔离 mktemp
- tools/list 因 createServer() 空注册返回 -32601，不影响 55605（认证缺失）与 55604（会话接管）判定——两漏洞点在注册工具之前即已成立
- Harness RCE (QVD-2026-57410) PoC：奇安信未公开利用链、厂商无公开镜像，且本地未部署 DSH——不强行编造，故 PoC 覆盖 MCP 两 CVE（报告 Top-5 中可验证且最实者）
