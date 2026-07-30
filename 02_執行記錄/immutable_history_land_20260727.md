> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：执行记录 · 落地报告
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：🟢 已验证

**DNA**: `#龍芯⚡️2026-07-27-LONGHUN-IMMUTABLE-HISTORY-LAND-v1.0`  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

# 龍魂不可篡改历史引擎落地报告

## 一、设计来源：宪法 + 协议 + Notion 镜像

### 1.1 《龍魂系统宪法》§6.2 审计日志不可篡改

> 龍魂系统内置**追加式审计日志**，记录每一次关键操作。审计日志必须存储于中华人民共和国境内的物理设备或受中国法律管辖的加密存储空间中，不得以任何形式出境或托管于境外服务器。

本引擎将主账本置于 `~/.longhun/ledger/immutable_history.jsonl`，完全符合“本地、追加、不出境”的宪法要求。

### 1.2 《龍魂创作者保护协议 · 不可篡改条款》

- **核心铁律**：龍魂系统每个时间戳不可覆盖、篡改、删除。
- **允许的操作**：
  - 🟢 **追加**：历史只被补充，不被修改。
  - 🟢 **修正**：追加“勘误”记录，原记录保留。
- **核心原则**：
  > **错就错了，改就改了——但不能假装没发生过。**

本引擎的 `--record`、`--feed`、`--correct` 三个 CLI 入口，分别对应“追加系统真实历史”“追加外部投喂”“追加勘误”，没有任何删除或覆盖接口。

### 1.3 《审计协议 v2.0》§6 审计留痕格式

- 审计日志是“证据链”，不是普通记录。
- 每条记录必须携带 `dna`、`gpg_fingerprint`、`immutable: true`。
- 关键记录需 GPG 签章。

本引擎每条记录均含 DNA 追溯码，关键记录使用 UID9622 GPG 指纹 `A2D0092CEE2E5BA87035600924C3704A8CC26D5F` 进行分离签名。

### 1.4 Notion 镜像中的 L0 留痕不阻断律

- **L0 留痕不阻断**：任何输入先留痕，再处理；不因来源可疑就直接丢弃，也不因来源可信就跳过留痕。
- **投喂 verbatim 焊死**：外部投喂必须原文保存，不得改写、不得混入系统真实历史。

本引擎对外部投喂强制标记 `source: external_feed`、`contamination_risk: unverified`、三色 🟡，物理上与 `system`/`user_action` 记录隔离来源字段。

---

## 二、实现原理

### 2.1 文件位置

```
引擎：             longhun-system/bin/lh_immutable_history.py
主账本：           ~/.longhun/ledger/immutable_history.jsonl
签名目录：         ~/.longhun/ledger/signatures/
威胁行为体索引：    ~/.longhun/ledger/threat_actors.json
守护状态：         ~/.longhun/ledger/immutable_history_watchdog_state.json
本地锚定快照：     ~/.longhun/ledger/anchors/
```

环境变量覆盖（仅用于测试与灾备）：

```bash
export LH_LEDGER_DIR=...
export LH_LEDGER_FILE=...
export LH_SIG_DIR=...
export LH_THREAT_ACTOR_FILE=...
```

### 2.2 哈希链结构

单条记录哈希：

```python
hash = SHA256(id + timestamp + action + source + actor
              + payload_hash + prev_hash + dna)
```

`payload_hash` 单独对 payload 内容做 SHA256，确保**payload 级篡改**也能被定位。

### 2.3 三层完整性校验

`--verify` / `--report` 会同时执行：

1. **payload 校验**：重新计算 payload_hash，与记录值比对。
2. **哈希链校验**：重新计算记录 hash，与前一条 prev_hash 链接比对。
3. **GPG 签名校验**：对含 `gpg_signature` 的记录验证签名。

任一失败即 🔴 失败，并指出被篡改记录的 `id` 与位置。

### 2.4 来源类型与三色映射

| 来源 | 含义 | 三色 | 是否可覆盖系统历史 |
|:---|:---|:---|:---|
| `system` | 系统真实历史 | 🟢 | — |
| `user_action` | 用户真实操作 | 🟢 | — |
| `external_feed` | 外部投喂 | 🟡 | ❌ 绝对禁止 |
| `correction` | 勘误记录 | 🟢 | 仅追加，不删除原记录 |
| `audit` | 审计标记 | 🟢/🟡/🔴 | 仅追加 |

### 2.5 来源溯源与威胁行为体追踪

#### 2.5.1 自动采集的 provenance 字段

每条记录均附带 `provenance` 对象：

| 字段 | 说明 | 来源 |
|:---|:---|:---|
| `ip` | IP 地址（传入优先，否则取本机局域网 IP） | 传入 / 自动 |
| `device_fingerprint` | 设备指纹（基于 MAC + hostname + username） | 传入优先 / 自动 |
| `hostname` | 本机主机名 | 自动 |
| `username` | 当前系统用户 | 自动 |
| `user_agent` | User-Agent | 传入 |
| `session_id` | 会话 ID | 传入 |
| `collected_at` | 采集时间 | 自动 |

#### 2.5.2 威胁行为体叠加原则

- **指纹优先**：`device_fingerprint` 相同即视为同一行为体，IP 变化也会叠加到同一 actor。
- **证据累积**：同一 actor 的 `ips`、`hostnames`、`incidents` 会自动去重并追加。
- **永不删除**：行为体索引只追加，不删除、不覆盖。

#### 2.5.3 索引文件

`~/.longhun/ledger/threat_actors.json`

结构：

```json
{
  "actors": {
    "<actor_id>": {
      "actor_id": "...",
      "first_seen": "...",
      "last_seen": "...",
      "incident_count": 2,
      "fingerprints": ["fp-xxx"],
      "ips": ["119.13.90.27", "119.13.90.28"],
      "hostnames": ["..."],
      "incidents": [...]
    }
  }
}
```

---

## 三、CLI 用法

### 3.1 记录系统真实历史

```bash
python3 bin/lh_immutable_history.py \
  --record "system_config_change" \
  --payload '{"key":"theme","old":"dark","new":"light"}' \
  --source system --sign
```

### 3.2 接收外部投喂（原文保存，标记风险，带溯源）

```bash
python3 bin/lh_immutable_history.py \
  --feed "japan-history-claim-001" \
  --feed-content '{"claim":"否认南京大屠杀","source":"external_textbook_v2025","risk":"high"}' \
  --ip "119.13.90.27" \
  --device-fingerprint "fp-revisionist-node-a1b2" \
  --user-agent "Mozilla/5.0 (历史修正主义爬虫)"
```

### 3.3 追加勘误（原记录保留）

```bash
python3 bin/lh_immutable_history.py \
  --correct <原记录id> \
  --reason "补充变更者信息" \
  --payload '{"key":"theme","old":"dark","new":"light","changed_by":"UID9622","approved":true}' \
  --sign
```

### 3.4 验证完整性

```bash
python3 bin/lh_immutable_history.py --verify
python3 bin/lh_immutable_history.py --report
```

### 3.5 列出最近记录

```bash
python3 bin/lh_immutable_history.py --list --limit 10
```

### 3.6 查询威胁行为体

```bash
python3 bin/lh_immutable_history.py --threat-actors
```

---

## 四、防投喂污染规则

1. **来源隔离**：外部投喂必须使用 `source: external_feed`，系统历史使用 `system` / `user_action`。
2. **风险标记**：每条外部投喂自动写入 `metadata.contamination_risk: unverified`。
3. **不可覆盖规则**：写入 `metadata.immutable_rule: external_feed_cannot_overwrite_system_truth`。
4. **原文追加**：`processing_rule: verbatim_append_only`，外部内容一个字不改地进入账本。
5. **三色警示**：外部投喂一律 🟡，直至人工审计确认或驳斥。

> 例如日本右翼势力通过教材、数据集、API 等形式投喂“否认侵略历史”的内容，系统不会删除它，但会原文保存、标记为 🟡 外部投喂，并使其永远无法覆盖系统已确认的 `system` 历史记录。

---

## 五、与现有 DNA / 三色审计的对接

| 现有机制 | 对接方式 |
|:---|:---|
| DNA 追溯码 | 每条记录生成 `#龍芯⚡️丙午·乙未·丁酉·午时·既济-{action}-{hash8}` |
| 三色审计 | `tricolor` 字段写入 🟢/🟡/🔴，CLI `--verify` 输出三色结果 |
| GPG 签章 | 关键记录使用 UID9622 指纹分离签名，存 `signatures/{id}.asc` |
| 审计总账 | 可向 `~/.longhun/audit/dragon_ledger.jsonl` 同步关键事件 |
| 铁律自审闸 | 检测到篡改时返回 exit code 1，可被守护进程捕获触发告警 |

---

## 六、测试结果

### 6.1 正常流程

```bash
python3 bin/lh_immutable_history.py --record "system_config_change" ... --sign
python3 bin/lh_immutable_history.py --feed "japan-history-claim-001" ...
python3 bin/lh_immutable_history.py --correct <id> ... --sign
python3 bin/lh_immutable_history.py --verify
```

输出：

```
完整性: 🟢 通过
  🟢 全部 3 条记录哈希链与 payload 完整
```

### 6.2 篡改检测

#### 场景 A：修改 payload 内容（模拟外部势力改历史）

将 `external_feed` 的 claim 从“否认南京大屠杀”改为“承认南京大屠杀”，未改 `payload_hash`。

```
完整性: 🔴 失败
  🔴 记录 #1 (id=3fb98c25-...) payload 被篡改
```

#### 场景 B：修改记录 hash

将第一条记录的 `hash` 改为 `a...a`，导致链式断裂。

```
完整性: 🔴 失败
  🔴 记录 #0 (id=efced4a8-...) 哈希链断裂
  🟡 记录 #0 GPG 签名验证失败
  🔴 记录 #1 (id=3fb98c25-...) 哈希链断裂
```

### 6.3 主账本验证

```bash
python3 bin/lh_immutable_history.py --verify
```

输出：🟢 通过，主账本 8 条记录完整。

### 6.4 威胁行为体叠加测试

#### 测试设计

使用同一 `device_fingerprint`、不同 IP 进行两次外部投喂：

```bash
# 第一次
python3 bin/lh_immutable_history.py --feed "claim-002" ... --ip "119.13.90.27" --device-fingerprint "fp-revisionist-node-a1b2"

# 第二次
python3 bin/lh_immutable_history.py --feed "claim-003" ... --ip "119.13.90.28" --device-fingerprint "fp-revisionist-node-a1b2"
```

#### 预期结果

两次投喂被识别为同一行为体，IP 列表累积：

```json
{
  "total_actors": 1,
  "total_incidents": 2,
  "top_actors": [
    {
      "actor_id": "ecd3ff3fa01b27bdfd302586",
      "incident_count": 2,
      "fingerprints": ["fp-revisionist-node-a1b2"],
      "ips": ["119.13.90.27", "119.13.90.28"],
      "incidents": [...]
    }
  ]
}
```

实际验证：🟢 通过，同一 fingerprint 不同 IP 成功叠加。

---

## 七、守护进程：定时巡检 + 篡改即告警 + 篡改即留痕

### 7.1 脚本

`longhun-system/bin/lh_immutable_history_daemon.py`

### 7.2 能力

- **定时巡检**：默认每 10 分钟调用引擎 `--report` 验证账本完整性。
- **篡改即告警**：发现异常立即终端输出 + Bark 推送。
- **篡改即留痕**：把“发现篡改”这件事本身追加为 `audit` 来源的不可篡改记录。
- **状态持久化**：`~/.longhun/ledger/immutable_history_watchdog_state.json`

### 7.3 CLI

```bash
# 单次巡检
python3 bin/lh_immutable_history_daemon.py

# 守护模式
python3 bin/lh_immutable_history_daemon.py --daemon

# 查看状态
python3 bin/lh_immutable_history_daemon.py --status
```

### 7.4 验证结果

篡改账本测试：

```
🔴 龍魂不可篡改历史 — 篡改告警
  记录 #1 (id=3fb98c25-...) payload 被篡改
```

守护进程自动追加 `tamper_detected` 记录到账本。

---

## 八、锚定备份：本地 WORM 快照 + 异地 OBS 锚定

### 8.1 脚本

`longhun-system/bin/lh_immutable_history_anchor.py`

### 8.2 能力

- **本地 WORM 快照**：打包账本 + 签名目录，生成 tar.gz 并设为只读。
- **Merkle 根**：对快照内所有文件计算 Merkle 根，用于后续验证。
- **GPG 签名清单**：对清单文件分离签名。
- **OBS 双区锚定**：若配置 `~/.longhun/huawei-credentials.json`，自动上传到北京主区 + 广州灾备区。
- **锚定亦留痕**：每次锚定操作追加到不可篡改历史账本。

### 8.3 CLI

```bash
# 本地 + OBS 锚定
python3 bin/lh_immutable_history_anchor.py anchor

# 仅本地
python3 bin/lh_immutable_history_anchor.py anchor --local-only

# 验证最近一次锚定
python3 bin/lh_immutable_history_anchor.py verify

# 锚定报告
python3 bin/lh_immutable_history_anchor.py report
```

### 8.4 验证结果

```
⚓ 开始不可篡改历史锚定: IHA-20260727-035737-5f9b4389
✅ 本地 WORM 快照: .../IHA-20260727-035737-5f9b4389.tar.gz
📦 tar SHA256: dc3d952eec72723e...
🌳 Merkle Root: f6b21b2f8723439e...
🔏 GPG 签名: 是
✅ 锚定事件已写入不可篡改历史账本
```

锚定验证：🟢 通过。

---

## 九、健康检查集成

### 9.1 集成点

`longhun-system/bin/lh_health_alert_daemon.py` 新增 `immutable_history` 模块，权重 0.15。

### 9.2 验证结果

```
🏥 龍魂健康报告
得分: 100.0/100 [GREEN]
...
✅ 不可篡改历史: 100/100 — 账本完整: 8 条 | 行为体: 1 | 事件: 2
```

---

## 十、综合测试结论

| 组件 | 命令 | 结果 |
|:---|:---|:---|
| 历史引擎 | `python3 bin/lh_immutable_history.py --verify` | 🟢 通过 |
| 篡改检测 | 改 payload / 改 hash | 🔴 均被捕获 |
| 来源溯源 | `--ip` / `--device-fingerprint` / `--user-agent` | 🟢 自动写入 provenance |
| 威胁叠加 | 同一 fingerprint + 不同 IP 多次投喂 | 🟢 合并为同一 actor，IP 累积 |
| 守护进程 | `python3 bin/lh_immutable_history_daemon.py` | 🟢 通过，篡改告警正常 |
| 锚定备份 | `python3 bin/lh_immutable_history_anchor.py anchor --local-only` | 🟢 通过，WORM + Merkle |
| 健康检查 | `python3 bin/lh_health_alert_daemon.py` | 🟢 100/100 GREEN |

---

## 十一、诚实局限

1. **本地单点存储（已部分缓解）**：主账本仍为单机 JSONL，但已通过 `lh_immutable_history_anchor.py` 生成本地 WORM 快照；OBS 双区锚定需要配置华为云凭证。完整 Layer 2 分布式节点与 Layer 3 区块链锚定尚未接入。
2. **GPG 私钥安全**：签名依赖本地 GPG 私钥；若私钥泄露，攻击者可伪造新记录（但无法篡改旧记录）。
3. **管理员权限风险**：获得 root 权限的攻击者可以删除整个账本文件或 WORM 快照；本引擎能“发现”篡改，但不能阻止物理删除。建议配合硬件安全模块（HSM）或只读存储介质。
4. **OBS 凭证依赖**：异地锚定依赖 `~/.longhun/huawei-credentials.json`，未配置时仅保留本地快照。
5. **指纹可伪造**：外部传入的 `device_fingerprint`、`ip`、`user_agent` 可被伪造；系统优先采信指纹用于行为体关联，但高安全场景需结合多因素验证。
6. **内网 IP 局限**：本机自动采集的 IP 为局域网 IP，公网 IP 需由接入层（网关 / API）传入。

---

## 十二、修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-07-27 | v1.0.0 | UID9622 | 实现不可篡改历史引擎并落地 | 🟢 已验证 |
| 2026-07-27 | v1.0.1 | UID9622 | 补 payload_hash 校验，堵住 payload 级篡改绕过 | 🟢 已验证 |
| 2026-07-27 | v1.1.0 | UID9622 | 增加守护进程、WORM 锚定、健康检查集成 | 🟢 已验证 |
| 2026-07-27 | v1.2.0 | UID9622 | 增加 IP/设备指纹溯源与威胁行为体叠加索引 | 🟢 已验证 |

---

## 十三、分类标签

- 总纲模块：#安全域 #审计 #DNA追溯 #数据主权
- 对外状态：#本地
- 审计色：#绿色确认

---

## DNA 签名

```
#龍芯⚡️2026-07-27-LONGHUN-IMMUTABLE-HISTORY-LAND-v1.0
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```
