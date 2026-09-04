# 龍魂系统·MCP 接入指南 / Longhun System · MCP Integration Guide

> DNA: #龍芯⚡️2026-09-05-MCP接入指南-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层）· 代码: MulanPSL v2
> 文档版本: v5.2.0
> 三色: 🟢 MCP 集群 2026-09-05 ss/netstat 实测

---

## [中文] MCP 接入指南

### 一、龍魂 MCP 集群（实测）

| 端口 | 服务 | 权限层 | 说明 |
|---|---|---|---|
| 8763 | readonly MCP | 🔍 只读（health/topo/billing 查询） | 鲲鹏回环·外部审计者 |
| 8764 | audit MCP | 🛡 审计层（+judge/reconcile） | 鲲鹏回环·合作开发者 |
| 8765 | cal MCP | 📅 日历能力 | 鲲鹏回环 |
| 8766 | knowledge-hub MCP | 🧠 知识中心 | 鲲鹏回环 |
| 8767 | admin MCP | ⚔ 管理员（UID9622 专属·按需启动） | 非常驻 |
| 8768 | Notion 只读镜像 MCP | 🔗 Notion 层 | 本机 127.0.0.1 |

> 安全：除 8768（本机）外全部绑 127.0.0.1 回环——MCP 不对外网暴露（零攻击面 P0）。

### 二、逻辑三层权限（与端口映射）

| 权限层 | 能力 | 适用角色 | 端口 |
|---|---|---|---|
| 只读层 | 查询 health/ledger/calmem/billing 状态 | 外部审计者 | 8763 |
| 审计层 | 只读 + judge/reconcile/gov | 合作开发者 | 8764 |
| 管理员层 | 全功能（含 payment/admin） | UID9622 专属 | 8767(按需) |

### 三、CodeBuddy / IDE 接入（示例）

```json
// .codebuddy/mcp.json（片段）
{
  "mcpServers": {
    "memory-longhun":     { "command": "python3", "args": ["...memory server..."] },
    "notion-longhun":     { "command": "python3", "args": ["...notion mirror 8768..."] },
    "longhun-readonly":   { "command": "python3", "args": ["/opt/longhun-system/mcp/...", "--port", "8763"] }
  }
}
```

### 四、探活验证

```bash
# 鲲鹏 MCP 回环（服务器本机）
ssh root@<鲲鹏IP> 'ss -tlnp | grep -E "8763|8764|8765|8766"'
# → LISTEN 127.0.0.1:8763/8764/8765/8766 (python3) = 集群在线

# 本机 Notion 镜像
curl -s http://127.0.0.1:8768/health   # 在线时返回服务信息
```

### 五、离线模式

```bash
LONGHUN_OFFLINE_MODE=1
# 所有需要联网的 MCP 自动降级：本地 Markdown / 本地数据文件
# 联网后 lh workspace-sync 补齐远端
```

---

## [English] MCP Integration Guide

**Cluster (verified 2026-09-05)**: 8763 readonly · 8764 audit · 8765 cal · 8766 knowledge-hub — all on Kunpeng loopback (127.0.0.1, not internet-exposed, zero attack surface). 8767 admin = on-demand, UID9622 only. 8768 Notion mirror on localhost.

**Permission layers**: readonly (8763, external auditors) → audit (8764, collaborators, +judge/reconcile) → admin (8767, UID9622, on-demand).

**Offline**: `LONGHUN_OFFLINE_MODE=1` degrades all internet-dependent MCPs to local Markdown / local data.

---
🐉 2026-09-05 · 丙午年·壬申月·庚戌日 · UID9622 · 🟢
