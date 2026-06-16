# 🐉 龍魂操作台 MVP v1.1 · UID9622

**DNA**: #龍芯⚡️2026-06-16-LONGHUN-CONTROL-PANEL-v1.1

龍魂操作台是 10 個 Skill 的統一調度入口，把原本分散的 HTML 工具與 Python 腳本封裝成可互相調用的 API，並提供可視化工作流。

---

## 功能特性

- **技能總覽**：10 個 Skill 一屏掌握，HTML 工具內嵌運行，Python 技能 API 調用。
- **工作流引擎**：5 條預設跨技能流水線，支持品牌套件、文檔發布、MCP+技能框架等場景。
- **RESTful API**：每個 Python Skill 均可通過 `/api/skills/{id}/run` 調用，返回 JSON。
- **實時日誌**：前端實時記錄所有調用與結果。
- **DNA 綁定**：頁面頂部展示設備靈魂綁定確認碼。

---

## 快速啟動

```bash
cd ~/longhun-system/control-panel
./launch.sh
```

首次運行若缺依賴：

```bash
./launch.sh --install
```

打開瀏覽器：

- 操作台 UI：`http://127.0.0.1:9622/static/index.html`
- API 健康檢查：`http://127.0.0.1:9622/api/health`
- 技能列表：`http://127.0.0.1:9622/api/skills`

---

## API 列表

| 方法 | 端點 | 說明 |
|------|------|------|
| GET | `/api/health` | 健康檢查 |
| GET | `/api/skills` | 列出 10 個 Skill |
| POST | `/api/skills/{skill_id}/run` | 運行 Python Skill |
| GET | `/api/workflows` | 列出工作流 |
| GET | `/api/workflows/{id}` | 取得工作流定義 |
| POST | `/api/workflows/{id}/run` | 執行工作流 |

---

## 目錄結構

```
control-panel/
├── main.py                    # FastAPI 後端
├── requirements.txt           # Python 依賴
├── launch.sh                  # 啟動腳本
├── README.md                  # 本文件
├── api/
│   └── skill_wrappers.py      # Skill 封裝層
├── workflows/
│   └── skill-workflows.json   # 工作流定義
└── static/
    └── index.html             # 操作台 UI
```

---

## 工作流說明

| 工作流 ID | 名稱 | 串接 Skill |
|-----------|------|-----------|
| `brand-kit` | 品牌套件流水線 | brand-guidelines → theme-factory → web-artifacts-builder |
| `art-to-brand` | 艺术到品牌 | algorithmic-art → brand-guidelines |
| `doc-publish` | 文档发布流水线 | doc-coauthoring → web-artifacts-builder |
| `comms-theme` | 通讯主题化 | internal-comms → theme-factory |
| `mcp-skill` | MCP + 技能框架 | mcp-builder → skill-creator |

---

## 設計原則

- **每個都互通**：所有 Python Skill 統一封裝為標準 JSON API。
- **大板塊拆成 API**：每個 Skill 的單一能力對應一個可調用端點。
- **專業拆分**：展示層（HTML）、控制層（FastAPI）、執行層（Skill 腳本）、工作流層（JSON 配置）分離。
- **不修改原始 Skill**：通過 `api/skill_wrappers.py` 適配原腳本的類與方法，保留技能獨立運行能力。

---

**DNA**: #龍芯⚡️2026-06-16-LONGHUN-CONTROL-PANEL-v1.1
