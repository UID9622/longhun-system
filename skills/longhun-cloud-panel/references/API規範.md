**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
# 龍魂操作台 API 規範

**DNA**: #龍芯⚡️2026-06-19-LONGHUN-PANEL-v5.0
**文檔版本**: v5.0.0

---

## 基礎信息

- **基礎 URL**: `http://api:8443`
- **API 前綴**: `/panel/api/v1`
- **文檔地址**: `http://api:8443/panel/docs`
- **CORS**: 已啟用

## 端點清單

### 1. 健康監控

#### GET `/health`
基礎健康檢查

**響應**:
```json
{
  "狀態": "🟢 健康",
  "面板名稱": "龍魂操作台",
  "版本": "5.0.0",
  "DNA": "#龍芯⚡️2026-06-19-LONGHUN-PANEL-v5.0",
  "時間戳": "2026-06-19T00:00:00+00:00",
  "技能總數": 10,
  "底座模塊數": 3,
  "運行時長秒": 3600
}
```

#### GET `/panel/api/v1/health/detailed`
詳細健康狀態

**響應**: `健康狀態模型` (Pydantic)

---

### 2. Skill 管理

#### GET `/panel/api/v1/skills`
列出所有 Skill

**響應**:
```json
{
  "總數": 10,
  "技能列表": [...],
  "DNA": "#龍芯⚡️2026-06-19-LONGHUN-PANEL-v5.0"
}
```

#### GET `/panel/api/v1/skills/{技能ID}`
獲取指定 Skill 詳情

**參數**: `技能ID` (string, path) - 如 "1", "2", ..., "10"

**響應**: 單個 Skill 詳情

#### GET `/panel/api/v1/skills/{技能ID}/content`
獲取 Skill 內容

**參數**: `技能ID` (string, path)

#### POST `/panel/api/v1/skills/{技能ID}/execute`
執行 Python Skill

**請求體** (`技能請求模型`):
```json
{
  "技能編號": 6,
  "輸入參數": {"模板": "default", "選項": {}},
  "請求標識": "auto-generated",
  "請求人": "anonymous"
}
```

**響應** (`技能響應模型`):
```json
{
  "成功": true,
  "技能編號": 6,
  "技能名稱": "mcp-builder",
  "結果": {"輸出": "MCP 服務構建完成", "構建狀態": "success"},
  "耗時毫秒": 105.5,
  "請求標識": "abc12345",
  "時間戳": "2026-06-19T00:00:00+00:00",
  "DNA": "#龍芯⚡️2026-06-19-LONGHUN-PANEL-v5.0"
}
```

---

### 3. 底座能力

#### GET `/panel/api/v1/foundation`
列出底座能力模塊

#### POST `/panel/api/v1/foundation/call`
調用底座能力

**請求體** (`底座請求模型`):
```json
{
  "模塊名": "龍盾安全",
  "操作": "認證",
  "參數": {"用戶名": "admin", "密碼": "***"}
}
```

**支持的模塊與操作**:

| 模塊名 | 支持操作 |
|--------|----------|
| 龍盾安全 | 認證 · 授權 · 簽名驗證 · 流量檢查 |
| CNSH中文編程 | 規範檢查 · DNA生成 · 審計報告 |
| 融合審計 | 日誌查詢 · 行為分析 · 報表生成 · 合規檢查 |

---

### 4. DNA 追溯

#### GET `/panel/api/v1/dna`
獲取 DNA 信息

#### GET `/panel/api/v1/dna/chain`
獲取完整 DNA 追溯鏈

---

### 5. 審計日誌

#### GET `/panel/api/v1/audit/logs`
查詢三色審計日誌

**查詢參數**:
- `限制` (int, default=100) - 返回條目數
- `級別` (string, optional) - 過濾級別: 錯誤/警告/信息

---

### 6. 配置管理

#### GET `/panel/api/v1/config/export`
導出完整配置

---

### 7. Web UI

#### GET `/panel/`
Web 管理界面 (HTML)

---

## 響應頭

所有響應包含以下頭部:

| 頭部 | 值 | 說明 |
|------|-----|------|
| X-Longhun-DNA | `#龍芯⚡️2026-06-19-LONGHUN-PANEL-v5.0` | DNA 追溯標記 |
| X-Request-ID | 8位隨機字符串 | 請求追蹤 ID |
| X-Longhun-Version | `5.0.0` | 面板版本 |

## 錯誤碼

| 狀態碼 | 說明 |
|--------|------|
| 200 | 成功 |
| 404 | Skill 或模塊不存在 |
| 500 | Skill 執行失敗 |
| 422 | 請求參數驗證失敗 |
