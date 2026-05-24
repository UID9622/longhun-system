# 🐉 龍魂9625·本地引擎

> Chrome 扩展 × FastAPI 引擎 × MVP × MCP × Notion 一体化
> DNA: `#龍芯⚡️2026-04-19-LOCAL-ENGINE-9625-v1.0`

## 为什么是 9625，不是 9622

`:9622` 已被现有 CNSH-64 治理引擎占用，旁路到 `:9625`，两者并存不冲突。
切回 9622：`main.py` 里 `port=9625` → `port=9622`，扩展 `background.js` 里 `ENGINE` 同改。

## 目录

```
~/longhun-system/
├── chrome-ext/               # Chrome 扩展（MV3）
│   ├── manifest.json
│   ├── background.js         # 右键菜单·引擎调用
│   ├── content.js            # 页面悬浮侧边栏
│   ├── popup.html/.js/.css   # 工具栏弹窗+对话窗
│   └── icons/16/48/128.png
└── engine/                   # FastAPI 引擎
    ├── main.py               # 主入口·端口 9625
    ├── chat.py               # 对话窗·三重记忆·三大脑路由
    ├── notion_sync.py        # 记错本 Notion 回写
    ├── mcp_bridge.py         # MCP 桥占位
    ├── mvps/                 # MVP 脚本（软链）
    ├── memory/               # 本地记忆 sqlite
    ├── .env.example          # 密钥模板
    ├── requirements.txt
    ├── install.sh
    └── README.md
```

## 装

```bash
bash ~/longhun-system/engine/install.sh
```

## 跑

```bash
# 手动跑（看日志）
python3 ~/longhun-system/engine/main.py

# 开机自启
launchctl load ~/Library/LaunchAgents/com.longhun.9625.plist

# 健康检查
curl http://127.0.0.1:9625/api/health
```

## 装 Chrome 扩展

1. Chrome 打开 `chrome://extensions`
2. 右上角开「开发者模式」
3. 点「加载已解压的扩展程序」→ 选 `~/longhun-system/chrome-ext/`
4. 固定到工具栏 📌
5. 任何网页选中文字 → 右键 → 看到「⚖️ 伦理 / 🟡 通心译 / 🔥 五行 / 📓 记错本 / 🔌 MCP」

## 测试流

```bash
# 1. 健康
curl http://127.0.0.1:9625/api/health

# 2. 伦理审查
curl -X POST http://127.0.0.1:9625/api/ethics/review \
  -H "Content-Type: application/json" \
  -d '{"text":"测试文本","url":"","title":""}'

# 3. 对话窗（需先填 .env 里的 DEEPSEEK_API_KEY）
curl -X POST http://127.0.0.1:9625/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"你好","mode":"auto"}'

# 4. 历史
curl http://127.0.0.1:9625/api/chat/history

# 5. 全量导出（主权归你·随时走人）
curl -X POST http://127.0.0.1:9625/api/chat/export
```

## 主权铁律

- 数据只在 `~/longhun-system/engine/memory/memory.db`
- API Key 只读 `.env`，`.gitignore` 拦死
- 每次调用都有 DNA 签章
- `launchctl unload com.longhun.9625` → 引擎立即断电
- `/api/chat/export` → 一键全量打包走人

## 端点一览

| 方法 | 端点 | 功能 |
|------|------|------|
| GET  | `/` | 服务信息 + 端点清单 |
| GET  | `/api/health` | 健康检查 |
| POST | `/api/ethics/review` | 伦理审查（调 MVP 脚本） |
| POST | `/api/tongxin/translate` | 通心译（占位） |
| POST | `/api/wuxing/analyze` | 五行分析 |
| POST | `/api/errata/submit` | 上报记错本 → Notion |
| GET  | `/api/mcp/list` | MCP 工具清单 |
| POST | `/api/mcp/call` | MCP 工具调用 |
| POST | `/api/chat` | 对话窗（三重记忆+三大脑） |
| GET  | `/api/chat/history` | 对话历史 |
| POST | `/api/chat/export` | 全量导出 |

---

**UID9622 · 诸葛鑫 · 龍芯北辰**
确认码: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
