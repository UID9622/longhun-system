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
# 🐉 鲲鹏 MCP Server 接入指南 v1.0

> DNA: #龍芯⚡️2026-09-04-LONGHUN-KUNPENG-MCP-GUIDE-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层）
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 抬头模板: [2] 🔧 工程落地执行型（脚本/部署/API）
> 适用: Claude Desktop / Cursor / MCP Inspector 等任意 MCP 客户端 · 2026-09-04

---

## 一、这是什么

把龍魂系统的能力，以 **MCP（Model Context Protocol）** 标准协议暴露给任意 AI 应用。AI 应用无需学习龙魂私有接口，直接"原生调用"图谱、铭碑、审计、CNSH 编译等能力。

设计铁律（M77 零中间层 · P0）：

- **零三方依赖**：纯 Python 标准库手写 JSON-RPC 2.0 / Streamable HTTP，不装任何 MCP SDK
- **薄委托**：业务不重复实现，工具只做路由 → 直接调用现有引擎（`lh_topo.py` / `lh_memorial.py` / `lh_judge.py` / `cnsh.py` / `cnsh_pm.py`）
- **小而专**：三个独立 Server 按风险分域，不造万能代理
- **全审计**：每次调用 append-only 落 `~/.longhun/logs/mcp/<server>.jsonl`

## 二、三层架构一览

| Server | 端口 | 风险 | 系统状态 | 工具 | 资源 |
|:---|:---:|:---:|:---|:---|:---|
| `lh-mcp-readonly` | 8763 | 🟢 低 | 常开 | `get_topo` · `verify_memorial` · `list_commands` · `get_health` | `resource://topo/*` · `resource://memorial/root` · `resource://health/status` |
| `lh-mcp-audit` | 8764 | 🟡 中 | 常开 | `audit_text` · `scan_shamewall` · `verify_dna` · `get_audit_logs` | `resource://shamewall/latest` · `resource://audit/rules` |
| `lh-mcp-admin` | 8767 | 🔴 高 | **默认 disabled** | `cnsh_build` · `cnsh_publish` · `topo_sync` · `system_reload` | — |

管理入口（一行命令）：

```bash
lh mcp list          # 三 Server 一览
lh mcp health        # 本地存活探测（--remote 走鲲鹏 ssh 探测）
lh mcp config        # 配置摘要（永不打印 token）
lh mcp log <server>  # 操作审计日志尾部
lh mcp deploy        # 部署到鲲鹏（--admin-on 才开高危层）
lh mcp doc           # 打印本指南路径
```

## 三、客户端接入

### 3.1 传输模式

两种模式，任选其一：

| 模式 | 适用 | 启动方式 |
|:---|:---|:---|
| **Streamable HTTP** | 鲲鹏常驻服务（systemd）| `python3 deploy/longhun-mcp/lh_mcp_readonly.py --host 127.0.0.1 --port 8763` |
| **stdio** | 本地桌面客户端（Claude Desktop / Cursor command）| `python3 deploy/longhun-mcp/lh_mcp_readonly.py --stdio` |

协议版本：`2025-03-26`。端点：`POST /mcp`（或 `/`），Accept 支持 `application/json` 与 `text/event-stream`（SSE）。

### 3.2 本机 stdio（推荐 · 桌面端）

```json
// claude_desktop_config.json
{
  "mcpServers": {
    "longhun-readonly": {
      "command": "python3",
      "args": ["/opt/longhun-system/deploy/longhun-mcp/lh_mcp_readonly.py", "--stdio"]
    },
    "longhun-audit": {
      "command": "python3",
      "args": ["/opt/longhun-system/deploy/longhun-mcp/lh_mcp_audit.py", "--stdio"]
    }
  }
}
```

### 3.3 鲲鹏远端（Cursor 等非本机客户端）

安全区默认绑定 `127.0.0.1`，外部访问走 **SSH 隧道**（不需要开放端口）：

```bash
ssh -i ~/.ssh/longhun_kunpeng_ed25519 -L 8763:127.0.0.1:8763 \
    -L 8764:127.0.0.1:8764 root@119.13.90.27 -N
# 之后在客户端里用 http://127.0.0.1:8763/mcp 等 URL
```

> ⚠️ **不推荐直接开放 0.0.0.0**。确需开放必须三步全做：1) `config/mcp-config.json` 改 `auth.mode=token` 并配 token；2) systemd `--host 0.0.0.0`；3) 修改后重签 GPG。只读/审计层对外开放前同样要求。

## 四、JSON-RPC 调用示例

所有请求为 JSON-RPC 2.0，逐行（stdio）或 POST（HTTP）。

**1. 列工具**

```json
{"jsonrpc":"2.0","id":2,"method":"tools/list"}
```

**2. 调只读工具 `get_health`**

```bash
curl -s -H 'Content-Type: application/json' -H 'Accept: application/json' \
  --data '{"jsonrpc":"2.0","id":1,"method":"tools/call",
           "params":{"name":"get_health","arguments":{}}}' \
  http://127.0.0.1:8763/mcp
```

```json
{"jsonrpc":"2.0","id":1,"result":{"content":[{"type":"text","text":"{\"ok\": true, \"uid\": \"UID9622\", \"attribution\": \"诸葛鑫 | UID9622 · 龍芯北辰\", ...}"}],"isError":false}}
```

**3. 调审计工具 `audit_text`**

```bash
curl -s -H 'Content-Type: application/json' -H 'Accept: application/json' \
  --data '{"jsonrpc":"2.0","id":1,"method":"tools/call",
           "params":{"name":"audit_text","arguments":{"text":"出卖用户数据给第三方，灵活处理一下"}}}' \
  http://127.0.0.1:8764/mcp
```

返回三色结论：命中红线词 → `"verdict":"🔴"`；命中一票否决词 → `"verdict":"🟡"`；否则 `"verdict":"🟢"`。

**4. 高危工具（admin 8767）——必须二次确认**

```bash
# 无确认 → 拒绝（错误码 -32002，默认拒绝，日志留痕）
curl -s -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","id":3,"method":"tools/call",
           "params":{"name":"cnsh_build","arguments":{"source":"打印(\"hello\")"}}}' \
  http://127.0.0.1:8767/mcp
# → {"error":{"code":-32002,"message":"高危操作需请求头 X-Confirm: yes 确认（默认拒绝）"}}

# 请求头 X-Confirm: yes（HTTP）或参数 "_confirm":"yes"（stdio 通用）→ 放行
curl -s -H 'Content-Type: application/json' -H 'X-Confirm: yes' \
  --data '{"jsonrpc":"2.0","id":4,"method":"tools/call",
           "params":{"name":"cnsh_build","arguments":{"source":"打印(\"hello\")"}}}' \
  http://127.0.0.1:8767/mcp
```

**5. 读资源**

```json
{"jsonrpc":"2.0","id":8,"method":"resources/read","params":{"uri":"resource://topo/通心译"}}
```

## 五、JSON-RPC 错误码

| 码 | 含义 |
|:---|:---|
| `-32700` | JSON 解析失败 |
| `-32600` | 非法请求（Content-Length 非法等） |
| `-32601` | 方法/工具/资源不存在 |
| `-32602` | 参数错误（缺必填、text/dna 为空、图谱名未找到等） |
| `-32000` | 工具执行失败 / 引擎白名单外 / 超时 |
| `-32001` | 认证失败 / 来源 IP 不在白名单 |
| `-32002` | 高危操作未确认（默认拒绝） |

## 六、工具清单

### readonly（8763 · 只读）

| 工具 | 参数 | 返回要点 |
|:---|:---|:---|
| `get_topo` | `name`（留空=图谱清单）| 图谱完整结构：groups/subgraphs/root_hash/stats（节点数·三色计数）|
| `verify_memorial` | `root_hash`（可选）| 当前铭碑 Merkle 根；传参则比对是否被篡改 |
| `list_commands` | — | `lh` 命令全表（SUB_DISPATCH 静态解析）+ 高频速查 |
| `get_health` | — | 健康 JSON：uid/图谱数/铭碑根/neural_net/Python 版本 |

### audit（8764 · 审计）

| 工具 | 参数 | 返回要点 |
|:---|:---|:---|
| `audit_text` | `text` 必填 | 三色判定 + 命中词（红=禁止场景 · 黄=一票否决词）|
| `scan_shamewall` | `keyword`（可空）| 耻辱墙检索（≤20 条）|
| `verify_dna` | `dna` 必填 | 前缀/干支日期/卦名/模块动作/哈希8 校验 + 数字根五行 |
| `get_audit_logs` | `start`/`end`（可选）| 合并三 Server 操作审计 + admin 专用日志 |

### admin（8767 · 高危 · 默认关闭 · 全部需确认）

| 工具 | 参数 | 动作 |
|:---|:---|:---|
| `cnsh_build` | `source` 必填 | CNSH 源码 → Python（临时文件编译，随用随清）|
| `cnsh_publish` | `package` | 发布 CNSH 包（仅限白名单 `build_dirs` 内的包）|
| `topo_sync` | `name` 必填 · `live` | 强制同步指定图谱（Notion/活体，超时 120s）|
| `system_reload` | — | 配置 JSON 校验 + 引擎在位 + 图谱缓存计数完整性报告 |

## 七、安全实践（对照检查）

| # | 机制 | 说明 |
|:---|:---|:---|
| 1 | **三层风险分域** | 只读/审计/高危物理分离，高危层**默认 disabled，不常开**。需用时 `systemctl enable --now lh-mcp-admin`，用完**立刻** `systemctl disable --stop lh-mcp-admin`（2026-09-04 老大焊死·用完即关） |
| 2 | **来源白名单** | admin 强制 peer 白名单（`config/admin-whitelist.json` → ips）；HTTP 层自动注入真实来源 IP |
| 3 | **二次确认** | admin 工具必须 `X-Confirm: yes`（或 `_confirm:"yes"`），否则 -32002 拒绝 |
| 4 | **操作审计** | 每次调用落 `~/.longhun/logs/mcp/*.jsonl`；admin 另落 `~/.longhun/audit/admin_operations.log`（append-only·谁/何时/做什么/三色）|
| 5 | **异常耻辱墙通道** | admin 异常自动写 `~/.longhun/shame_wall/mcp_admin_anomalies.jsonl`，不污染正式耻辱墙 |
| 6 | **引擎白名单** | `run_engine` 只允许 `cnsh.py/lh_topo.py/lh_memorial.py/cnsh_pm.py/lh_judge.py/lh.py`，防注入 |
| 7 | **发布目录白名单** | `cnsh_publish` 仅允许 `build_dirs` 内 cnsh.json 声明过的包 |
| 8 | **入参约束** | 必填校验 + 长度上限（源码 ≤200KB）；输出递归截断防爆内存 |
| 9 | **token 模式** | `config/mcp-config.json` 可开 `auth.mode=token`（HTTP 头 `X-LH-Token`/`X-API-Key`/`Bearer`）；`lh mcp config` 永不打印密钥 |
| 10 | **日志防敏** | 审计日志经 `_sanitize` 截断；不落 token/密钥 |

## 八、本地验证记录

冒烟全链路（stdio · JSON-RPC 直连，2026-09-04 实测）：

```
readonly 8/8 · audit 5/5 · admin 3/3  →  16/16 ALL PASS
关键断言：get_health.uid=UID9622 · verify_memorial.root=66534A84…(真实 merkle_root)
         audit_text 红线命中🔴(出卖用户数据) · verify_dna 数字根=2/五行=火
         admin 无确认拒绝 code=-32002 · cnsh_build rc=0 · system_reload checks=7
```

响应时间：全部工具为本地文件/子进程委托，实测单次调用毫秒级；HTTP ping 见 `lh mcp health`。

## 九、文件布局

```
deploy/longhun-mcp/
├── lh_mcp_core.py            # 共享协议引擎（JSON-RPC/HTTP/stdio/委托/审计）
├── lh_mcp_readonly.py        # :8763 只读层
├── lh_mcp_audit.py           # :8764 审计层
├── lh_mcp_admin.py           # :8767 高危层（默认关·2026-09-04 由 8765 迁入，原 8765 归鲲鹏 longhun-cal）
├── config/
│   ├── mcp-config.json       # 三 Server 端口/绑定/认证
│   └── admin-whitelist.json  # IP/工具/发布目录白名单
├── systemd/                  # lh-mcp-{readonly,audit,admin}.service
└── deploy_to_kunpeng.sh      # rsync + systemd 一键部署（--admin-on）
```

部署（鲲鹏 root@119.13.90.27）：

```bash
lh mcp deploy          # 常开 readonly+audit；admin 保持 disabled
lh mcp deploy --admin-on   # 额外启用高危层（仅本机 127.0.0.1）

# 🔴 高危层生命周期铁律（2026-09-04 老大焊死）：
#   默认关闭不常开 → 需用时临时启用 → 用完立刻关。
systemctl enable --now lh-mcp-admin     # 临时启用（仅 127.0.0.1 · X-Confirm 二次确认）
systemctl disable --stop lh-mcp-admin   # 用完立刻关（stop=当前停 + disable=取消开机自启）
systemctl is-active lh-mcp-admin        # 验证 → 应 inactive
ss -tlnp | grep 8767                    # 验证 → 不应再有输出
```

---

> 定位：本文档为工程落地文档（MulanPSL v2 / CC BY-NC-SA 4.0 分层 · 见 LH-LAYERED-LICENSE-v1.0）。
> 关联：`lh mcp doc` · `docs/鲲鹏MCP接入指南-v1.0.md` · GPG 验签 `python3 bin/lh_gpg_sign.py verify docs/鲲鹏MCP接入指南-v1.0.md`


---

## 💛 支持龍魂（纯自愿 · 零黑箱）

龍魂的一切免费开放。若你认可「让技术为人、为普通人生长」，可自愿支持——款项仅用于服务器与开发成本，不留一分私账。

- **收款方式**: SOL / USDC（Solana）
- **实时地址与二维码**: 见官网 [uid9622.cn](https://uid9622.cn) 底部「支持龍魂」区 — 地址由 `lh wallet` 统一管理（公司账户落地后自动切换 · 以官网为准）

> 龍魂不诱导、不施压、不道德绑架。捐与不捐，开放与尊重不变。

<!-- LH-WALLET-SUPPORT -->

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
