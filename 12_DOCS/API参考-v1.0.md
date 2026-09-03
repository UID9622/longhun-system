# 🐉 longhun-cli API 参考 v1.0

> 协议母本: `docs/对外接口协议-v1.0.md` · 所有输出为标准 **Node JSON**（`{"node_id": ..., "audit": ..., ...}`），可解析、可追溯、可审计。

---

## 1. 调用形态

longhun-cli 提供三种调用形态，输出格式完全一致：

| 形态 | 入口 | 适用场景 |
|:---|:---|:---|
| CLI 命令 | `lh <cmd> [args] [--json]` | 终端 · 脚本 · CI |
| HTTP 网关 | `POST http://127.0.0.1:9622/v1/lh` | 远程调用 · 微服务 · 前端 |
| Python 模块 | `from longhun_cli.core import flow, bazi` | 程序内嵌 |

---

## 2. 请求格式

### 2.1 CLI

```
lh <command> [options]
lh <command> [options] --json     # 输出标准 JSON（机器可解析）
```

### 2.2 HTTP 网关

```
POST /v1/lh
Content-Type: application/json
Host: 127.0.0.1:9622

{ "command": "flow 龙魂对外首发 --json" }
```

| 字段 | 类型 | 必填 | 说明 |
|:---|:---|:---:|:---|
| `command` | string | ✅ | 完整 lh 命令行（含子命令与参数） |
| `cwd` | string | ❌ | 执行目录（默认网关工作目录） |

### 2.3 Python

```python
from longhun_cli.core import flow, bazi, health_basic
node = flow("龙魂对外首发")     # 流场
chart = bazi("1990-01-01", "08:00")  # 八字
health = health_basic()        # 基础自检
```

---

## 3. 响应格式

### 3.1 成功响应（HTTP 200）

CLI / Python 直接返回 Node JSON；HTTP 网关包装为执行结果:

```json
{
  "result": {
    "code": 0,
    "stdout": "{ \"node_id\": \"FLOW-9622-FE92BD84\", ... }",
    "stderr": ""
  }
}
```

### 3.2 Node JSON 公共字段（全部命令）

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `node_id` | string | 节点 ID（`<CMD>-9622-<sha256前8>`，全链路追溯） |
| `digital_root` | int | 数字根（1-9，洛书算法） |
| `element` | string | 五行（水火木金土） |
| `gua` | string | 八卦（乾坤兑离震巽坎艮） |
| `audit` | string | 三色审计（🟢 放行 / 🟡 待核 / 🔴 红线） |
| `action` | string | 行为建议（`enter` / `stay`） |
| `timestamp` | string | ISO 时间戳 |

### 3.3 命令专属字段

| 命令 | 追加字段 |
|:---|:---|
| `flow` | —（公共字段即全部） |
| `bazi` | `bazi`(四柱串) · `pillars`(年月日时) · `wuxing_score`(五行权重) · `dominant` · `weakest` |
| `health` | `status` · `service` · `version` · `python` · `platform` · `root_detected` · `mode` |

### 3.4 错误响应

```json
{ "result": { "code": 127, "stdout": "", "stderr": "lh: 'xxx' 不是子命令" } }
```

### 3.5 健康检查端点 `GET /health`

网关存活自检（无参数，无鉴权，供负载均衡 / Docker healthcheck / 监控使用）。

```json
{
  "status": "ok",
  "version": "v4.0",
  "uptime": "1h 2m 30s",
  "service": "lh-api",
  "dna": "#龍芯⚡️丙午·丁酉·乙亥·巳时·䷝离-CIL-API-GATEWAY-v2.0"
}
```

| 字段 | 说明 |
|:---|:---|
| `status` | 恒为 `ok`（进程存活即返回 200） |
| `version` | 网关版本 `v4.0` |
| `uptime` | 进程已运行时长（`Xh Ym Zs` 格式） |

> Docker 健康检查直接使用该端点：`curl -f http://localhost:9622/health || exit 1`（见 `packaging/docker/docker-compose.yml`）。

---

## 4. 错误码

| code | 含义 | 处理 |
|:---:|:---|:---|
| `0` | 成功 | 解析 `stdout` 为 Node JSON |
| `1` | 命令执行失败（运行时错误） | 读 `stderr` 定位 |
| `2` | 参数错误（argparse 解析失败） | 检查参数格式 |
| `126` | 命令不可执行（文件权限） | 检查 `bin/lh.py` 可执行位 |
| `127` | 子命令不存在 | `lh --help` 查看命令表 |
| `130` | 用户中断（Ctrl+C） | 重试 |
| `400` | HTTP 请求体非法（非 JSON / 缺 command） | 检查请求格式 |
| `404` | HTTP 路径不存在（非 /v1/lh） | 检查 URL |
| `500` | 网关内部错误 | 查网关日志 `logs/lh_api.log` |

---

## 5. curl 示例

```bash
# 流场
curl -s -X POST http://127.0.0.1:9622/v1/lh \
  -H "Content-Type: application/json" \
  -d '{"command": "flow 龙魂对外首发 --json"}'

# 健康检查
curl -s -X POST http://127.0.0.1:9622/v1/lh \
  -H "Content-Type: application/json" \
  -d '{"command": "health --json"}'

# 八字排盘
curl -s -X POST http://127.0.0.1:9622/v1/lh \
  -H "Content-Type: application/json" \
  -d '{"command": "bazi --date 1990-01-01 --time 08:00 --json"}'

# 网关存活探测
curl -s http://127.0.0.1:9622/health
# {"status": "ok", "service": "longhun-cil-gateway", "version": "4.0.0"}

# 错误样例（子命令不存在）
curl -s -X POST http://127.0.0.1:9622/v1/lh \
  -H "Content-Type: application/json" \
  -d '{"command": "nosuch"}'
```

---

## 6. Python 示例

### 6.1 HTTP 调用（标准库 urllib，零依赖）

```python
import json
import urllib.request

def lh_call(command: str, host: str = "127.0.0.1", port: int = 9622) -> dict:
    req = urllib.request.Request(
        f"http://{host}:{port}/v1/lh",
        data=json.dumps({"command": command}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        body = json.loads(r.read().decode())
    return json.loads(body["result"]["stdout"])  # Node JSON


node = lh_call("flow 龙魂对外首发 --json")
print(node["node_id"], node["digital_root"], node["element"])
# FLOW-9622-FE92BD84 7 火

chart = lh_call("bazi --date 1990-01-01 --time 08:00 --json")
print(chart["bazi"], chart["dominant"])
# 庚午 戊寅 丙寅 壬辰 火
```

### 6.2 模块内嵌调用

```python
from longhun_cli.core import bazi, flow, health_basic

# 流场
n = flow("龙魂对外首发")
assert n["digital_root"] == 7 and n["element"] == "火"

# 八字
c = bazi("1990-01-01", "08:00")
assert c["status"] == "ok" and len(c["bazi"]) == 11  # "庚午 戊寅 丙寅 壬辰"

# 健康
h = health_basic()
assert h["status"] == "ok"

print("✅ 全部调用通过")
```

---

## 7. 幂等与安全

- 所有计算**纯本地**，数据不出设备（P0 数据主权）
- 命令透传仅限 `lh` 子命令集（网关做白名单校验，拒绝 shell 注入）
- 网关只绑定 `127.0.0.1`，不暴露公网（如需外网请前置反向代理 + 鉴权）
- 每次输出携带 `node_id` + `audit`，可全链路审计追溯

---

*龍魂 · 文化主权 · 接口即主权声明* 🐉
