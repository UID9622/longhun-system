> **P0焊死**: 本文件为龍魂体系P0级文档·不可修改·不可绕过（上位文档 LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md）
# 🐉 龍魂·操盘网关接入手册 v1.0
# DNA: #龍芯⚡️丙午·丙申·己酉·甲子·䷉履-QUOTA-OPERATOR-GATEWAY-HANDBOOK-v1.0
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0（核心思想层）
> 三色: 🟢 已实测通过

---

## 一句话

**各家国产AI凭专属 Key，通过本机 `127.0.0.1:18790` 网关，就能操盘老大的 Mac。**
网关 = 守门员：Key 认证 → 黑名单熔断 → 路径锁定 → 审计留痕。

> ⚠️ 仅内部私有使用，不对外发布。

---

## 1. 网关地址与认证

| 项 | 值 |
|:---|:---|
| 地址 | `http://127.0.0.1:18790` |
| 认证 | HTTP 头 `X-Gate-Key: <你的Key>` |
| 内容类型 | `Content-Type: application/json` |
| 状态查询 | `GET /v1/status` |
| 接口说明 | `GET /v1/help` |

Key 在 `config/control_gate.json`：
- `master_key` = 管理员钥匙（UID9622 专属，可查审计/发新Key）
- `ais.<名字>.key` = 各家AI专属钥匙（kimi/deepseek/hunyuan/qwen/zhipu/baichuan 已预置）

---

## 2. 支持的操作（action）

| action | 参数 | 说明 |
|:---|:---|:---|
| `shell` | `command` | 执行 shell 命令（受黑名单熔断保护） |
| `sysinfo` | — | 系统信息快照（主机名/负载/内存/磁盘/CPU） |
| `read` | `path` | 读取文件（仅限 `longhun-system/` 内，≤1MB） |
| `write` | `path` `content` | 写文件（需 master 开 `enable_write=true`） |
| `open` | `app` | 打开应用/文件/URL（macOS `open`） |
| `notify` | `title` `msg` | 桌面通知 |
| `clipboard` | `mode=get/set` `text` | 剪贴板读写 |
| `ls` | `path` | 列目录（默认 longhun-system/） |

---

## 3. 各家AI接入示例

### 3.1 Kimi / DeepSeek（标准 POST）

```json
POST http://127.0.0.1:18790/v1/execute
X-Gate-Key: <你的Key>

{
  "action": "shell",
  "params": { "command": "echo 龍魂操盘成功 && uname -a" }
}
```

### 3.2 系统信息（一探设备状态）

```json
{
  "action": "sysinfo"
}
```

### 3.3 读文件（只能在 longhun-system/ 内）

```json
{
  "action": "read",
  "params": { "path": "/Users/zuimeidedeyihan/longhun-system/STATE.md" }
}
```

### 3.4 列目录

```json
{
  "action": "ls",
  "params": { "path": "/Users/zuimeidedeyihan/longhun-system/01_protocols" }
}
```

### 3.5 打开应用 / 通知

```json
{ "action": "open",  "params": { "app": "Safari" } }
{ "action": "notify", "params": { "title": "龍魂", "msg": "操盘成功" } }
```

---

## 4. 🔴 熔断黑名单（AI 也必须遵守）

以下操作**一律拒绝**，不会执行：

- `rm -rf /`、`rm -rf ~`、删 `.ssh/.gnupg`、删系统库
- `git push --force main/master`
- `mkfs` / `dd` 写块设备 / `shutdown` / `poweroff` / `reboot` / `halt`
- 读取 D1 绝密文件（id_rsa / id_ed25519 / secring / secrets.env 等）
- 越出 `longhun-system/` 目录读写文件

> 一旦命中，网关返回 `🔴 熔断拒绝: <原因>`，并写入审计日志。

---

## 5. 管理员操作（master 专属）

### 5.1 给新AI发钥匙

```json
POST http://127.0.0.1:18790/v1/keygen
X-Gate-Key: <master_key>

{ "name": "glm4" }
```

### 5.2 查审计

```json
POST http://127.0.0.1:18790/v1/audit
X-Gate-Key: <master_key>
```

### 5.3 开启写操作

编辑 `config/control_gate.json` → `"enable_write": true` → 重启服务：
```
killall lh_control_gate.py; launchctl kickstart -k gui/$(id -u)/com.longhun.control-gate
```

---

## 6. AI 操盘礼仪（写入各家AI的 system prompt）

> 你是龍魂操盘手。你可以通过 `http://127.0.0.1:18790/v1/execute` 操作 UID9622 的 Mac。
> 铁律：
> 1. 只做老大要求的事，不擅自越权
> 2. 不做任何破坏性操作（网关会拦，但别试）
> 3. 读文件只在 `longhun-system/` 内
> 4. 执行完汇报结果
> 5. 你的 Key 是：`<ais.你的名字.key>`

---

## 7. 维护

| 命令 | 说明 |
|:---|:---|
| `launchctl list \| grep control-gate` | 看是否在跑 |
| `tail -f logs/control_gate_audit.jsonl` | 实时审计流 |
| `cat logs/control_gate_daemon.out.log` | 网关日志 |
| `lsof -iTCP:18790` | 端口检查 |

> 服务随开机自启，崩溃自动拉起（KeepAlive）。

---

## 8. 版本记录

| 版本 | 日期 | 内容 |
|:---|:---|:---|
| v1.0 | 2026-08-17 | 网关首发：6家国产AI预置Key·8类操作·黑名单熔断·路径锁定·审计留痕·launchd自启 |

【签名】诸葛鑫（UID9622）× 龍魂AI
