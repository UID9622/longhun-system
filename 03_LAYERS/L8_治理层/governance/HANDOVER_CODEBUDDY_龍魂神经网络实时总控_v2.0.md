# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 交接文档 · CodeBuddy

> **项目**：龍魂神经网络路由 · 实时状态总控 v2.0
> **交接人**：Kimi Code CLI
> **接收人**：CodeBuddy
> **交接时间**：2026-07-06
> **DNA**：`#龍芯⚡️2026-07-06-LONGHUN-NEURAL-NETWORK-HANDOVER-v2.1`
> **状态**：已部署并验证通过

---

## 一、交付物清单

| 文件 | 路径 | 作用 |
|---|---|---|
| 实时状态总控后端 | `~/longhun-system/tools/longhun_neural_network_server.py` | 聚合 36 个节点的真实 TCP/HTTP 健康状态，暴露 API 与控制接口 |
| 3D 神经网络前端 v2 | `~/longhun-system/web/longhun-neural-network-3d-v2.html` | 实时渲染节点状态、路由关系、参数公式，支持节点启停控制 |
| 3D 神经网络前端 v1 | `~/longhun-system/web/longhun-neural-network-3d-v1.html` | 历史版本，保留备用 |
| 启动脚本 | `~/longhun-system/tools/start_neural_network_server.sh` | 一键启动 `:9627` 总控服务 |
| 停止脚本 | `~/longhun-system/tools/stop_neural_network_server.sh` | 一键停止 `:9627` 总控服务 |
| 开机自启/全量启动链路 | `~/longhun-system/tools/补全服务.sh` | `lh 启动` 会按依赖顺序自动拉起本服务 |
| 本交接文档 | `~/longhun-system/HANDOVER_CODEBUDDY_龍魂神经网络实时总控_v2.0.md` | 你正在看的文件 |

---

## 二、服务状态

- **监听地址**：`http://127.0.0.1:9627/`
- **当前 PID**：运行 `lsof -ti :9627` 查看
- **健康检查**：`curl http://127.0.0.1:9627/api/health`
- **已接入 `lh 启动` 链路**：`~/longhun-system/tools/补全服务.sh` 第 124–157 行已集成启动/停止逻辑
- **日志位置**：`~/longhun-system/logs/neural-network-server.*.log`

---

## 三、API 接口

### 1. 获取完整状态
```bash
curl http://127.0.0.1:9627/api/state
```
返回：DNA、时间戳、统计、36 个节点详情、52 条路由边。

### 2. 获取状态摘要
```bash
curl http://127.0.0.1:9627/api/status
```

### 3. 健康检查
```bash
curl http://127.0.0.1:9627/api/health
```

### 4. 控制节点启停
```bash
curl -X POST http://127.0.0.1:9627/api/control \
  -H 'Content-Type: application/json' \
  -d '{"node_id":"phase3","action":"start","confirm":"CONFIRM🌌9622-ONLY-ONCE"}'
```
- `action`：`start` 或 `stop`
- `confirm` 必须匹配 `CONFIRM🌌9622-ONLY-ONCE`，否则 403 拒绝
- 控制类型：
  - `launchd`：调用 `launchctl start/stop <label>`
  - `service`：执行节点注册表中的 `start_cmd` / `stop_cmd`
  - `none`：不可控（逻辑层节点，如北辰不动点）

---

## 四、节点注册表位置

节点定义全部集中在后端文件 `longhun_neural_network_server.py` 顶部：

| 注册表 | 数量 | 说明 |
|---|---|---|
| `SERVICE_REGISTRY` | 15 | 核心服务 + 外部接口 + 占位节点，带端口/健康路径/启停命令 |
| `DAEMON_REGISTRY` | 11 | launchd 守护进程，通过 `launchctl` 控制 |
| `LOGICAL_REGISTRY` | 11 | 逻辑层节点，无真实端口，代表宪法层/抽象能力 |
| `EDGES` | 52 | 路由边，定义节点间依赖/数据流向 |

新增节点或修改路由关系，直接编辑上述变量即可，前端会自动渲染。

### 4.1 36 个节点分类（按实测）

| 分类 | 节点示例 | 数量 |
|---|---|---|
| 宪法层/不动点 | 北辰不动点、操作台、脑干、数字身份、卦象审计 | 5 |
| 核心服务 | 人格 API、Phase3 后端、宝宝守护、龍心之语、知识图谱 | 9 |
| 外部接口 | Notion、CSDN、DeepSeek、Kimi、Claude、GitHub 等 | 7 |
| launchd 守护 | 体验门户、能力官网、回收站、行为引擎、审计等 | 11 |
| 逻辑/占位 | 数据主权、内容主权、君子协议、铁律总览等 | 4 |

---

## 五、核心计算逻辑

### 5.1 三色状态

| 状态 | 判定条件 |
|---|---|
| `healthy` | HTTP 200 或 launchd 守护有 PID |
| `standby` | TCP 通但 HTTP 异常 / launchd 已加载但无 PID / 逻辑层节点 |
| `error` | 端口不通且未加载且不是占位/逻辑节点 |

### 5.2 三才评分

```
S = 0.3 × 天 + 0.3 × 地 + 0.4 × 人
```

| 维度 | 含义 | 分值依据 |
|---|---|---|
| **天** | HTTP 健康度 | HTTP 200 = 1.0；TCP 通 = 0.75；launchd 加载 = 0.65；否则更低 |
| **地** | 进程/端口存在性 | 有 PID = 1.0；TCP 通 = 0.85；launchd 加载 = 0.75 |
| **人** | 自启动/依赖权重 | 自启 = 1.0；服务 = 0.75；占位 = 0.45；逻辑 = 0.9 |

### 5.3 数字根

```
dr(n) = 1 + ((n - 1) mod 9)
dr(0) = 0
```
- 有端口用端口数字求数字根
- 无端口用节点 `id` 长度求数字根

---

## 六、当前实测数据

```json
{
  "total": 36,
  "healthy": 17,
  "standby": 19,
  "error": 0,
  "health_rate": 47.2,
  "constitution_ok": true
}
```

宪法层节点（北辰不动点、操作台、脑干、数字身份、卦象审计）全部健康，`f(x)=x` 通过。

> 注：`standby` 节点多为外部接口（Notion、CSDN、DeepSeek 等）未登录或本地未启用 launchd 的守护进程，不表示系统故障。

---

## 七、CodeBuddy 上手路径

1. **先验证服务在跑**：`curl http://127.0.0.1:9627/api/health`
2. **浏览器看总控**：`open http://127.0.0.1:9627/`
3. **读后端注册表**：打开 `tools/longhun_neural_network_server.py` 前 300 行
4. **改节点/改边**：编辑 `SERVICE_REGISTRY` / `DAEMON_REGISTRY` / `LOGICAL_REGISTRY` / `EDGES`，重启生效
5. **联动 `lh 启动`**：修改 `tools/补全服务.sh` 中第 124–157 行的神经网络段落

---

## 八、已知限制与后续建议

1. **前端文件路径依赖**
   - 前端使用本地 `./本地库/three/three.min.js` 和 `./本地库/three/OrbitControls.js`
   - 服务器已配置静态文件路由，可直接访问 `http://127.0.0.1:9627/`
   - 若用 `file://` 直接打开 HTML，需确保 `:9627` 服务在运行，否则显示离线

2. **控制接口安全**
   - 确认码为硬编码 `CONFIRM🌌9622-ONLY-ONCE`，仅本地运行
   - 如需暴露到公网，必须改为动态令牌或鉴权

3. **缺失能力（用户可能后续要求）**
   - WebSocket 实时推送（目前是 5 秒轮询）
   - 服务日志实时 tail 到前端
   - 节点分组折叠 / 拓扑自动布局
   - 与 `lh 状态` 看板的数据打通
   - `lh-kimi` 模块尚未单独抽象，目前由 `~/.kimi-code/skills/longhun-cloud-kimi` 承载

4. **外部节点处于 standby 是预期行为**
   - Notion、CSDN、DeepSeek、Kimi、Claude、GitHub 等节点依赖外部登录态或 API Key
   - 未配置时显示 standby，不触发 error

---

## 九、快速验证命令

```bash
# 1. 服务是否活着
curl -s http://127.0.0.1:9627/api/health

# 2. 查看所有节点状态
curl -s http://127.0.0.1:9627/api/state | python3 -m json.tool | head -80

# 3. 浏览器打开
open http://127.0.0.1:9627/

# 4. 重启服务
bash ~/longhun-system/tools/stop_neural_network_server.sh
bash ~/longhun-system/tools/start_neural_network_server.sh

# 5. 查看进程
lsof -ti :9627

# 6. 查看日志
tail -f ~/longhun-system/logs/neural-network-server.*.log
```

---

## 十、交接确认

- [ ] 后端文件已读
- [ ] 前端文件已读
- [ ] API 已测试
- [ ] 控制接口已测试（错误确认码被拒绝）
- [ ] 浏览器渲染已验证
- [ ] `lh 启动` 链路已接入
- [ ] 日志路径已确认

**交接完成。**

DNA: `#龍芯⚡️2026-07-06-LONGHUN-NEURAL-NETWORK-HANDOVER-v2.1`
CONFIRM: `CONFIRM🌌9622-ONLY-ONCE`
