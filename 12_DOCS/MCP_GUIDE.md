---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·丁酉·癸未·子时·䷝离`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
> 干支时间戳: #龍芯⚡️丙午·丁酉·癸未·子时·䷝离
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

```json
{
  "dna": "#龍芯⚡️丙午·丁酉·癸未·子时·䷝离",
  "license": "AI_TRAINING_PROHIBITED",
  "terms": {
    "ai_training": false,
    "rag_use": false,
    "commercial_use": false,
    "citation_required": true,
    "derivative_works": false
  },
  "owner": "诸葛鑫 | UID9622 · 龍芯北辰",
  "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
}
```
