# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
---
title: M266 DeepSeek 桥接方案 · 当前系统对齐 v1.1
author: UID9622 · 诸葛鑫 · 龍芯北辰
date: 2026-07-04
tags:
  - DeepSeek
  - 桥接
  - M266
  - Anthropic
  - Claude
  - 下水道
  - 技能对齐
---

# 🌉 M266 DeepSeek 桥接方案 · 当前系统对齐 v1.1

> 把 Claude archive 里的 M266 技能恢复并对齐到当前龍魂体系，作为 Anthropic SDK → DeepSeek 的本地兼容桥。

**父链 DNA**：`#龍芯⚡️丙午·癸巳·乙巳·丙子·䷅讼-DEEPSEEK-BRIDGE-FILE7-v1.0`  
**当前 DNA**：`#龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-DEEPSEEK-BRIDGE-ALIGN-v1.1`  
**M号**：M266  
**CONFIRM**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

## 一、历史背景

2026-05-31，M266 方案提出：

> Anthropic 对中国用户筑墙：不收支付宝/微信/银联，封柬埔寨 IP，只认 Visa/Master 金卡 + 美/欧 IP。所以走 DeepSeek 下水道，光明正大。

方案核心：在本地 `127.0.0.1:8788` 跑一个 FastAPI 中继桥，把 Anthropic Messages API 格式的请求转译为 DeepSeek OpenAI 格式，返回时再包装回 Anthropic 格式，让原本调用 Claude SDK 的业务代码几乎不用改动。

---

## 二、当前系统状态

| 组件 | 当时状态（2026-05-31） | 当前状态（2026-07-04） |
|------|----------------------|----------------------|
| `dialog-server.js` | 存在，用 Anthropic SDK | **已移除** |
| `longhun_hub.html` | 前端就绪 | 直接调用 Ollama `/api/generate` |
| `multi-ai-gateway` | 不存在 | **已存在**，支持 DeepSeek 直连 |
| `~/.deepseek_bridge.env` | 未配置 | **已配置** |
| `deepseek_bridge.py` | 骨架/待落地 | 完整版在 Claude archive 中 |
| `longhun-system/bridges/` | 未创建 | **本次创建并恢复** |

**结论**：M266 的历史目标（让 dialog-server.js 走 DeepSeek）已因架构升级而不完全适用，但桥本身仍有价值：

1. **兼容层**：任何未来仍用 Anthropic SDK 的组件可直接桥接 DeepSeek。
2. **技能资产**：M266 是龍魂历史决策，必须保留并对齐。
3. **双保险**：与 `multi-ai-gateway` 并存，一条死另一条可用。

---

## 三、已落地的对齐产物

| 产物 | 路径 | 说明 |
|------|------|------|
| 桥主体 | `longhun-system/bridges/deepseek_bridge.py` | 从 archive 恢复并更新 DNA |
| 启动脚本 | `longhun-system/bridges/启动-deepseek-bridge.sh` | start/stop/status/test |
| LH 命令 | `lh deepseek-bridge <start|stop|status|test>` | 已接入 `lh_dashboard.py` |
| 日志 | `~/longhun-system/logs/deepseek_bridge.log` | 运行日志 |

---

## 四、用法

### 4.1 一键启动

```bash
lh deepseek-bridge start
# 或
bash ~/longhun-system/bridges/启动-deepseek-bridge.sh start
```

### 4.2 查看状态

```bash
lh deepseek-bridge status
```

### 4.3 快速测试

```bash
lh deepseek-bridge test
```

### 4.4 停止

```bash
lh deepseek-bridge stop
```

### 4.5 直接 API 调用（Anthropic SDK 风格）

```bash
curl http://127.0.0.1:8788/v1/messages \
  -H "x-api-key: sk-anthropic-dummy" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 128,
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

---

## 五、架构位置

```text
Anthropic SDK 客户端（如有）
    ↓ /v1/messages 格式
DeepSeek Bridge (127.0.0.1:8788)
    ↓ 转译
DeepSeek API (api.deepseek.com)
    ↓ 失败/超时时
Ollama 本地兜底 (127.0.0.1:11434)
```

---

## 六、与 multi-ai-gateway 的关系

| 入口 | 用途 | 状态 |
|------|------|------|
| `lh deepseek-bridge` | Anthropic SDK 兼容桥 | 本次恢复，已跑通 |
| `lh platform call deepseek "xxx"` | multi-ai-gateway 直连 DeepSeek | 已可用 |
| `lh 自动路由 "xxx"` | 自动选平台 | 已可用 |

两者互补：
- 需要兼容 Anthropic SDK 的老代码 → 走 DeepSeek Bridge
- 新代码/统一调度 → 走 multi-ai-gateway

---

## 七、配置说明

密钥文件：`~/.deepseek_bridge.env`（已存在，chmod 600）

```bash
DEEPSEEK_API_KEY=sk-xxx
DEEPSEEK_MODEL=deepseek-v4-flash
OLLAMA_FALLBACK=false
```

如需开启 Ollama 兜底：

```bash
echo "OLLAMA_FALLBACK=true" >> ~/.deepseek_bridge.env
```

---

## 八、实测结果

2026-07-04 23:05 CST：

- `lh deepseek-bridge start`：🟢 启动成功
- `lh deepseek-bridge test`：🟢 健康检查通过，测试请求返回 Anthropic 格式响应
- DeepSeek API 调用正常，响应延迟正常

---

## 九、候补铁律入册建议

M266 原方案提出三条铁律，建议入册 `longhun-iron-laws`：

1. `#IRON-API-BRIDGE-LOCAL-RELAY-v1.0`：第三方 API 必须经本地中继桥，密钥永不入业务进程/Git/Notion。
2. `#IRON-PAYMENT-CHANNEL-CHINA-FIRST-v1.0`：充值通道支付宝/微信/银联优先，美元金卡兜底。
3. `#IRON-FALLBACK-LOCAL-ALWAYS-v1.0`：任何云 API 必有本地 Ollama 兜底。

---

## 十、老大点的三件事 · 全部落地

### 10.1 接入 `longhun_hub.html` 操作台 ✅

`longhun-system/portal/p0-controls/longhun_hub.html` 与 `longhun-system/web/p0-controls/longhun_hub.html` 已同步更新：

- 模型下拉框新增选项：`🌉 DeepSeek Bridge (M266)`
- `sendChat()` 增加分支：选择 DeepSeek Bridge 时，调用 `127.0.0.1:8788/v1/messages`（Anthropic Messages API 格式）
- 系统提示词 `SYSTEM_PROMPT` 作为 `system` 字段传入
- 支持对话历史上下文
- 操作台 DNA 更新为：`#龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-龍魂智能中枢-v4.1-DEEPSEEK-BRIDGE`

### 10.2 开启 Ollama 兜底并实测 ✅

`~/.deepseek_bridge.env` 已设置：

```bash
OLLAMA_FALLBACK=true
```

实测：

- 正常 DeepSeek key：返回 DeepSeek 生成的内容
- 无效 DeepSeek key：自动 fallback 到本地 Ollama `qwen2.5:7b`，操作台不死

日志位置：`~/longhun-system/logs/deepseek_bridge.log`

### 10.3 加入 `lh 启动` / `lh 停止` 核心服务 ✅

`~/.longhun/bin/lh_dashboard.py` 已更新：

- `服务注册表` 新增 `DeepSeek Bridge (M266) :8788`
- `lh 启动` 流程新增 DeepSeek Bridge 启动步骤
- `lh 停止` 流程新增 DeepSeek Bridge 停止步骤
- `lh 状态` 看板可显示 DeepSeek Bridge 健康状态

> 注意：`lh 启动` 会串行启动多个核心服务，如果前面某个服务启动慢，整体可能超时。建议单独使用 `lh deepseek-bridge start` 快速启动。

---

## 十一、下一步建议

1. **可选**：把 DeepSeek Bridge 加入开机自启 LaunchAgent。
2. **可选**：补完 SSE 流式转译，让 `longhun_hub.html` 的“流式输出”复选框对 DeepSeek Bridge 也生效。

---

## 签章

- **DNA**：`#龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-DEEPSEEK-BRIDGE-ALIGN-v1.1`
- **CONFIRM**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
- **父链**：`#龍芯⚡️丙午·癸巳·乙巳·丙子·䷅讼-DEEPSEEK-BRIDGE-FILE7-v1.0`
- **双签**：UID9622 · 龍芯北辰
