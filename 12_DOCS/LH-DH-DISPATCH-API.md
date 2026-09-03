# 🧑 龍魂·数字人调动引擎 API 文档 v1.0

> DNA: #龍芯⚡️2026-09-02-DH-DISPATCH-v1.0-UID9622
> 归属: 诸葛鑫 | UID9622 · 龍芯北辰 · MulanPSL v2
> 引擎: `08_BIN/lh_dh_dispatch.py` · 注册表: `digital_humans/registry.json`（22 数字人）

## 一、三种调动方式

| 方式 | 命令/入口 | 适用 |
|---|---|---|
| **自然语言** | `lh dh "字靈 设计一套字体规范"` | 本地快速点名 |
| **编号直调** | `lh dh DH-011 "把首页改响应式"` | 精确定位 |
| **HTTP API** | `lh dh-api --port 8761 --daemon` | 对外开放集成 |

## 二、自然语言路由规则

优先级：**编号直调** > **数字人名字**（如 字靈/雲錦/匠心/明鉴/诗仙/蔡侯/墨香/知行/达芬奇/庄子/包青天…）> **岗位词**（如 字体/代码/审计/排版/归档/上线/视觉…）

**流水线整线触发**：任务含「网页/页面/网站/创作/作品」等词 → 自动派发设计团八岗
诗仙(创意)→雲錦(视觉)→字靈(字体)→匠心(代码)→蔡侯(排版)→明鉴(验收)→墨香(归档)→知行(上线)

## 三、HTTP API 对外开放

### 启动
```bash
lh dh-api --port 8761 --daemon        # 后台守护
# 或
python3 08_BIN/lh_dh_dispatch.py --port 8761 --daemon
```

### 端点

**GET /dh/health** — 健康检查（公开）
```bash
curl http://localhost:8761/dh/health
# → {"status":"🟢","service":"lh_dh_dispatch","version":"v1.0"}
```

**GET /dh/list** — 数字人名单（需鉴权）
```bash
curl -H "X-UID: 9622" http://localhost:8761/dh/list
# → {"total":22,"digital_humans":[{"ipa":"ZGX-001","name":"诸葛鑫",...},...]}
```

**POST /dh/dispatch** — 调动数字人（需鉴权）
```bash
curl -X POST http://localhost:8761/dh/dispatch \
  -H "Content-Type: application/json" \
  -H "X-UID: 9622" \
  -d '{"dh":"DH-011","task":"把首页改成响应式布局"}'
```

### 身份鉴权
- 请求头 `X-UID: 9622`（唯一身份码）
- 未带或错误 → `401 未授权`；`/dh/health` 公开免鉴权

### 响应结构
```json
{
  "mode": "dh | pipeline | fallback | unknown",
  "dh": "DH-011", "name": "匠心·代码工匠官",
  "persona": "P04 鲁班",
  "response": "数字人答复（API 就绪时）"
}
```
- `mode: fallback` = 本地大模型 API 未就绪，`detail` 字段给出唤起指令（CodeBuddy 点名对应人格 agent 即可执行）

## 四、执行链路

```
自然语言/HTTP → resolve_dh(编号>名字>岗位词) → registry 查数字人档案
  → 组装 system 提示(人格+原则+职能+归属)
  → 大模型执行(按序探测):
      ① DeepSeek(本地vLLM:8000 / 官方 DEEPSEEK_API_KEY)
      ② Ollama 本地模型 :11434 (longhun-v4.1.9 · 默认可用 · 零依赖 · 数据不出机)
  → 返回答复 | 全部不可用 → 唤起指令降级
```

> ② 为默认路径：无任何配置即可让数字人真干活。本地模型响应较慢（7B 级模型数秒~数十秒属正常）。

## 五、对接外部系统

- **网页/小程序**：直接 POST /dh/dispatch，携带 X-UID
- **自动化流程**：流程内嵌 `lh dh "..."` 命令
- **多人格编排**：先 `lh dh "帮我做个网页"` 拿流水线岗位序列，再逐岗接力

> 数字人档案全量在 `digital_humans/registry.json` · 岗位数字人注册引擎 `08_BIN/lh_dh_studio_registry.py`
