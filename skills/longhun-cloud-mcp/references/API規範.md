**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
# 龍魂 MCP 服務 API 規範 v5.0

**DNA**: `#龍芯⚡️2026-06-19-LONGHUN-MCP-v5.0`

---

## 基礎信息

- **基礎URL**: `http://api:8443/mcp/`
- **協議**: HTTP REST
- **數據格式**: JSON
- **編碼**: UTF-8
- **響應頭**: `X-Longhun-DNA`, `X-MCP-Version`

---

## 端點詳細說明

### GET /mcp/

服務信息入口。

**響應示例**:
```json
{
  "服務": "longhun-mcp-server",
  "版本": "5.0.0",
  "DNA": "#龍芯⚡️2026-06-19-LONGHUN-MCP-v5.0",
  "端點": {
    "健康檢查": "GET /mcp/health",
    "工具列表": "GET /mcp/tools",
    "技能列表": "GET /mcp/skills",
    "DNA追溯": "GET /mcp/dna",
    "狀態": "GET /mcp/status",
    "審計日誌": "GET /mcp/audit/logs",
    "資源發現": "GET /mcp/resources",
    "工具調用": "POST /mcp/call"
  }
}
```

---

### GET /mcp/health

健康檢查端點。

**響應示例**:
```json
{
  "狀態": "健康",
  "服務": "longhun-mcp-server",
  "版本": "5.0.0",
  "DNA": "#龍芯⚡️2026-06-19-LONGHUN-MCP-v5.0",
  "時間戳": "2026-06-19T12:00:00",
  "組件": {
    "註冊中心": "正常",
    "審計系統": "正常",
    "DNA追溯": "正常"
  }
}
```

---

### GET /mcp/tools

獲取所有已註冊的 MCP 工具列表（MCP Schema 格式）。

**響應示例**:
```json
{
  "狀態": "成功",
  "工具": [
    {
      "name": "execute-skill",
      "description": "執行龍魂體系中的技能",
      "parameters": {
        "type": "object",
        "properties": {
          "技能ID": {"type": "string", "description": "技能標識符"},
          "參數": {"type": "object", "description": "技能執行參數"}
        },
        "required": ["技能ID"]
      }
    }
  ]
}
```

---

### GET /mcp/skills

列出所有龍魂技能，支持篩選。

**查詢參數**:
- `分類`: creative/devops/ai/intelligence/business/productivity
- `類型`: visualization/code-generation/automation/analytics/collaboration/communication

**響應示例**:
```json
{
  "狀態": "成功",
  "總數": 14,
  "技能": [
    {
      "ID": "algorithmic-art",
      "名稱": "算法藝術生成器",
      "描述": "Perlin噪聲·Flow Field·粒子系統·實時控制",
      "類型": "visualization",
      "分類": "creative"
    }
  ]
}
```

---

### GET /mcp/dna

查詢 DNA 追溯鏈。

**查詢參數**:
- `查詢`: 篩選關鍵詞

**響應示例**:
```json
{
  "狀態": "成功",
  "DNA": "#龍芯⚡️2026-06-19-LONGHUN-MCP-v5.0-NODE5",
  "節點數": 5,
  "追溯鏈": [
    {
      "節點ID": 0,
      "時間戳": "2026-06-19T12:00:00",
      "DNA": "#龍芯⚡️...",
      "操作": "MCP服務器初始化",
      "父節點": null,
      "簽章": "a1b2c3d4e5f67890"
    }
  ],
  "驗證結果": true
}
```

---

### GET /mcp/status

獲取服務運行狀態。

**響應示例**:
```json
{
  "狀態": "運行中",
  "服務名稱": "longhun-mcp-server",
  "版本": "5.0.0",
  "DNA": "#龍芯⚡️2026-06-19-LONGHUN-MCP-v5.0",
  "運行時間": "2026-06-19T12:00:00",
  "工具數": 11,
  "技能數": 14,
  "資源數": 5,
  "審計統計": {
    "🟢信息": 25,
    "🟡警告": 2,
    "🔴錯誤": 0,
    "💀致命": 0,
    "總計": 27
  }
}
```

---

### GET /mcp/audit/logs

獲取三色審計日誌。

**查詢參數**:
- `限制`: 返回記錄數（默認 100）
- `級別`: 篩選級別（信息/警告/錯誤/致命）

**響應示例**:
```json
{
  "狀態": "成功",
  "統計": {"🟢信息": 25, "🟡警告": 2, "🔴錯誤": 0, "總計": 27},
  "記錄數": 27,
  "最近記錄": [
    {
      "時間戳": "2026-06-19T12:00:00",
      "級別": "🟢",
      "級別名": "信息",
      "模塊": "MCP服務器",
      "消息": "服務器初始化完成",
      "詳情": {},
      "DNA": "#龍芯⚡️..."
    }
  ]
}
```

---

### GET /mcp/resources

發現所有已註冊的 MCP 資源。

**查詢參數**:
- `前綴`: URI 前綴篩選，如 `dna://`

---

### POST /mcp/call

調用已註冊的 MCP 工具。

**請求體**:
```json
{
  "工具名": "get-status",
  "工具參數": {}
}
```

**響應示例**:
```json
{
  "狀態": "成功",
  "...": "業務數據",
  "_dna": "#龍芯⚡️...",
  "_elapsed_ms": 2.5
}
```

---

### POST /mcp/tools/register

動態註冊一個新的 MCP 工具。

**請求體**:
```json
{
  "名稱": "my-tool",
  "描述": "我的自定義工具",
  "參數定義": [
    {"名稱": "輸入", "類型": "string", "描述": "輸入參數", "必需": true}
  ]
}
```

---

### POST /mcp/dockerfile

自動生成 Dockerfile。

**請求體**:
```json
{
  "語言": "python",
  "項目配置": {
    "基礎鏡像": "python:3.11-slim",
    "端口": 8000,
    "啟動命令": "python app.py",
    "額外步驟": "RUN apt-get install -y ffmpeg"
  }
}
```

**響應示例**:
```json
{
  "狀態": "成功",
  "語言": "python",
  "Dockerfile": "FROM python:3.11-slim\n...",
  "提示": "已生成 python Dockerfile..."
}
```

---

### POST /mcp/compose

自動生成 docker-compose.yml。

**請求體**:
```json
{
  "服務列表": [
    {
      "名稱": "mcp-server",
      "鏡像": "longhun-mcp-server:latest",
      "端口": "8443:8443",
      "環境": {"MCP_PORT": "8443"},
      "內部端口": 8443
    }
  ]
}
```

---

## 環境變量

| 變量 | 默認值 | 說明 |
|------|--------|------|
| MCP_PORT | 8443 | 服務端口 |
| MCP_HOST | 0.0.0.0 | 監聽地址 |
| MCP_DEBUG | false | 調試模式 |
| MCP_LOG_LEVEL | INFO | 日誌級別 |
| SKILL_DIR | /mnt/agents/output/longhun-v5-skills | 技能目錄 |
| MCP_AUDIT | true | 啟用審計 |

---

## 錯誤碼

| 狀態碼 | 含義 |
|--------|------|
| 200 | 成功 |
| 404 | 路徑未找到 |
| 500 | 服務器內部錯誤 |

---

**DNA**: `#龍芯⚡️2026-06-19-LONGHUN-MCP-v5.0`
