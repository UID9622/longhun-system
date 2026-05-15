# 护盾后台防御 v1.0（吸收 Notion · 只防不攻）

M::
  dna: "#龍芯⚡️2026-05-15-DEFENSE-BACKGROUND-v1.0"
  notion: "https://www.notion.so/3c32eba91be64ebd86ed8ec07de8ced7"
  qps: "[IPA-QPS-LOCAL-SOVEREIGN-v1.1]"
  code: "engine/defense/"

---

## 立场

- **防御不是攻击**：不对外扫描、不主动打别人 API。
- **防御可以强**：`strong` 档出口也拦；默认 **`normal` 松紧适度**（你说太强时用 `loose`）。
- **别人接你的**：护盾跑在 9625 进程里，入站 `/api/defense/*`。

## QPS 五律（焊接摘要）

见 `engine/defense/qps_core.py` · 正本见 Notion 护盾页 §QPS。

## 三档

| 档 | 行为 |
|----|------|
| loose | 只记日志，不拦 |
| normal | 入口盾拦截，出口只记 |
| strong | 入口+出口都拦 + Q4  violation 硬熔断 |

## API

- `GET /api/defense/status`
- `POST /api/defense/scan` `{"text":"...","direction":"in|out"}`
- `POST /api/defense/mode` `{"mode":"loose|normal|strong"}`

## 后台

9625 启动时自动 `start_background()`（30s 心跳 · 扫 `sandbox/defense/inbox/*.txt`）。

## flow_port 全链（已接）

每条 `flow_port()` 消息自动：

1. `gate_v3` 闸门  
2. **护盾入站** `defense_scan(..., direction=in)`  
3. 流场决策 + 民主门 + 95/5  
4. **护盾出站** `defense_scan(draft, direction=out)`  

返回里带 `defense.inbound` / `defense.outbound`（无黑箱）。  
跳过：`tags.skip_defense=true`（仅测试用）。

改档（复制）：

```bash
curl -s -X POST http://127.0.0.1:9625/api/defense/mode -H 'Content-Type: application/json' -d '{"mode":"loose"}'
```
