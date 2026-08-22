# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂 MCP Server 套件

> DNA: `#龍芯⚡️丙午·乙未·戊子·戊午·䷙大畜-LONGHUN-MCP-SUITES-v2.0`
> 总工具数: **67** · 5 个 Server · 全系统覆盖

龍魂系统提供 5 个 MCP Server，覆盖从底层编译到高层语义的全部能力：

| # | Server | 文件 | 工具数 | 核心能力 |
|---|--------|------|:---:|------|
| 1 | **longhun** | `longhun_mcp_server.py` | 16 | 主系统桥接：健康/DNA/审计/语义/五行/知识图谱/视觉/音频/人格 |
| 2 | **cnsh-core** | `cnsh_mcp_server.py` | 13 | CNSH 块管理：写入/查询/审计/溯源/同步/事件 |
| 3 | **cnsh-syntax** | `cnsh_syntax_mcp_server.py` | 13 | CNSH 语法工具链：词法/AST/编译/红线/DNA/数字根/诊断 |
| 4 | **cnsh-var-sandbox** | `cnsh_var_sandbox_mcp_server.py` | 10 | 变量沙箱：7语言映射/校验/隔离执行/金融数据 |
| 5 | **longhun-v4** | `v4_mcp_server.py` | 15 | 流场+状态：流场变异/人格矩阵/聚合审计/系统拓扑/编译/变量桥接 |
| | **总计** | | **67** | |

---

## 快速配置

复制 `mcp_config.json` 到 IDE 的 MCP 配置文件，或手动添加需要的 Server。

### CodeBuddy / Claude Desktop / Cursor

```json
{
  "mcpServers": {
    "longhun": {
      "command": "python3",
      "args": ["/Users/zuimeidedeyihan/longhun-system/integrations/mcp/longhun_mcp_server.py"],
      "env": {"PYTHONUNBUFFERED": "1"}
    }
  }
}
```

---

## Server 详情

### 1. longhun — 主系统桥接 (16工具)

```
❤️ longhun_health        — 系统健康检查
🧬 longhun_dna_gen        — 生成 DNA 追溯码
🛡️ longhun_audit          — 三色审计扫描
🪪 longhun_identity       — 身份核验+系统拓扑
🧠 longhun_semantic       — 中英语义路由
☯️ longhun_wuxing         — 五行数字根
📡 longhun_kb_search       — 知识图谱搜索
🔗 longhun_api_list        — API 端点列表
👁️ longhun_vision_parse   — 视觉解析桥接
🎤 longhun_audio_parse     — 音频解析桥接
💬 longhun_semantic_parse  — 语义解析桥接
🚀 longhun_cannon          — 全自动机枪
🧹 longhun_self_heal       — 系统自愈
🔄 longhun_auto_sync       — 自动同步
📋 longhun_persona_list    — 人格列表
🎭 longhun_persona_status  — 人格状态
```

### 2. cnsh-core — CNSH 块管理 (13工具)

```
📝 cnsh_write        — 写入CNSH块(三AI流程)
🔍 cnsh_query        — 查询CNSH块
🛡️ cnsh_audit        — 分级审计
🧬 cnsh_dna_generate  — 生成DNA
✅ cnsh_dna_validate  — 校验DNA
🛑 cnsh_redline_check — 红线熔断
📋 cnsh_redline_list  — 红线清单
🔢 cnsh_digital_root  — 数字根+五行
📊 cnsh_block_stats   — 块统计
🔗 cnsh_block_chain   — 块溯源
🔄 cnsh_sync_state    — 同步状态
📡 cnsh_event_watch   — 事件监听
❤️ cnsh_health        — 健康检查
```

### 3. cnsh-syntax — 语法工具链 (13工具)

```
📝 cnsh_lex          — 词法分析
🌳 cnsh_parse        — 语法分析(AST)
🔄 cnsh_translate    — CNSH→Python
⚙️ cnsh_compile      — CNSH→7语言
📖 cnsh_keywords     — 关键字查询
🛑 cnsh_redline_check— 红线熔断
📋 cnsh_redline_list — 红线清单
🧬 cnsh_dna_generate — DNA生成
✅ cnsh_dna_validate — DNA校验
🔢 cnsh_digital_root — 数字根
🎨 cnsh_audit        — 三色审计
🔍 cnsh_diagnostics  — 四合一诊断
❤️ cnsh_health       — 健康检查
```

### 4. cnsh-var-sandbox — 变量沙箱 (10工具)

```
📦 cnsh_var_register     — 变量注册(7语言映射)
✅ cnsh_var_validate     — 映射完整性校验
🔄 cnsh_var_translate    — 变量翻译
🔒 cnsh_var_sandbox_exec — 隔离执行
📋 cnsh_var_audit        — 审计报告
📝 cnsh_var_generate     — 代码生成
⚖️ cnsh_var_compare     — 外部对比
💰 cnsh_finance_ingest   — 金融摄取
📡 cnsh_finance_watch    — 金融监控
❤️ cnsh_health           — 健康检查
```

### 5. longhun-v4 — 流场+状态 (15工具)

```
🌊 flow_query           — 流场查询(天/地/人场)
✏️ flow_mutate          — 流场变异
🎭 persona_status       — 人格状态
🎯 persona_activate     — 激活人格
📋 persona_list_all      — 16人格矩阵
🌐 routing_status       — 路由层状态
🛡️ audit_aggregate      — 聚合审计
🧬 dna_batch_gen        — 批量DNA
📊 system_topology      — 系统拓扑
🔗 cns_bridge_compile   — CNSH编译桥接
📦 var_bridge_query     — 变量查询桥接
📄 var_bridge_register  — 变量注册桥接
📈 stats_snapshot       — 快照统计
🧹 health_aggregate     — 聚合健康
❤️ cnsh_health          — 健康检查
```

---

## 安装

```bash
cd integrations/mcp
pip install -r requirements.txt
```

## 架构

```
外部 AI 客户端 (Claude/Cursor/CodeBuddy)
  │
  ├── longhun (主桥接) ──→ 龍魂全部子系统
  ├── cnsh-core (块管理) ──→ CNSH API (localhost:9000)
  ├── cnsh-syntax (语法) ──→ CNSH v2.1 编译器
  ├── cnsh-var-sandbox (变量) ──→ 变量沙箱 + 金融API
  └── longhun-v4 (流场) ──→ 流场引擎 + 人格矩阵
```

---

## DNA

- 套件 DNA: `#龍芯⚡️丙午·乙未·戊子·戊午·䷙大畜-LONGHUN-MCP-SUITES-v2.0`
- GPG: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
- 创建者: UID9622（诸葛鑫·Lucky）
- 三色审计: 🟢 通过
