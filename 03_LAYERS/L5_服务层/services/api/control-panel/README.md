# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂操作台 MVP v1.1 · UID9622

**DNA**:#龍芯⚡️2026-06-16-LONGHUN-CONTROL-PANEL-FILE1-v1.1

龍魂操作台是 10 个 Skill 的统一调度入口，把原本分散的 HTML 工具与 Python 脚本封装成可互相调用的 API，并提供可视化工作流。

---

## 功能特性

- **技能总览**：10 个 Skill 一屏掌握，HTML 工具内嵌运行，Python 技能 API 调用。
- **工作流引擎**：5 条预设跨技能流水线，支持品牌套件、文档发布、MCP+技能框架等场景。
- **RESTful API**：每个 Python Skill 均可通过 `/api/skills/{id}/run` 调用，返回 JSON。
- **实时日志**：前端实时记录所有调用与结果。
- **DNA 绑定**：页面顶部展示设备灵魂绑定确认码。

---

## 快速启动

```bash
cd ~/longhun-system/control-panel
./launch.sh
```

首次运行若缺依赖：

```bash
./launch.sh --install
```

打开浏览器：

- 操作台 UI：`http://127.0.0.1:9622/static/index.html`
- API 健康检查：`http://127.0.0.1:9622/api/health`
- 技能列表：`http://127.0.0.1:9622/api/skills`

---

## API 列表

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/api/health` | 健康检查 |
| GET | `/api/skills` | 列出 10 个 Skill |
| POST | `/api/skills/{skill_id}/run` | 运行 Python Skill |
| GET | `/api/workflows` | 列出工作流 |
| GET | `/api/workflows/{id}` | 取得工作流定义 |
| POST | `/api/workflows/{id}/run` | 执行工作流 |

---

## 目录结构

```
control-panel/
├── main.py                    # FastAPI 后端
├── requirements.txt           # Python 依赖
├── launch.sh                  # 启动脚本
├── README.md                  # 本文件
├── api/
│   └── skill_wrappers.py      # Skill 封装层
├── workflows/
│   └── skill-workflows.json   # 工作流定义
└── static/
    └── index.html             # 操作台 UI
```

---

## 工作流说明

| 工作流 ID | 名称 | 串接 Skill |
|-----------|------|-----------|
| `brand-kit` | 品牌套件流水线 | brand-guidelines → theme-factory → web-artifacts-builder |
| `art-to-brand` | 艺术到品牌 | algorithmic-art → brand-guidelines |
| `doc-publish` | 文档发布流水线 | doc-coauthoring → web-artifacts-builder |
| `comms-theme` | 通讯主题化 | internal-comms → theme-factory |
| `mcp-skill` | MCP + 技能框架 | mcp-builder → skill-creator |

---

## 设计原则

- **每个都互通**：所有 Python Skill 统一封装为标准 JSON API。
- **大板块拆成 API**：每个 Skill 的单一能力对应一个可调用端点。
- **专业拆分**：展示层（HTML）、控制层（FastAPI）、执行层（Skill 脚本）、工作流层（JSON 配置）分离。
- **不修改原始 Skill**：通过 `api/skill_wrappers.py` 适配原脚本的类与方法，保留技能独立运行能力。

---

**DNA**:#龍芯⚡️2026-06-16-LONGHUN-CONTROL-PANEL-v1.1
