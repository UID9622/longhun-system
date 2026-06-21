# 🐉 龍魂系統 Phase 3 · Web UI · 監控 · 告警

**狀態**: 🟢 生產就緒 · 即時可用
**DNA**:#龍芯⚡️2026-06-06-PHASE3-WEB-UI-v1.0
**責任**: UID9622 · 不免責

---

## 📊 Phase 3 內容

### ✨ 核心功能

```
✅ Web UI 儀表板        - React 前端·實時更新·響應式設計
✅ 實時監控系統        - CPU·記憶體·磁碟·網絡·執行狀態
✅ 告警管理系統        - 自動告警·優先級分類·通知推送
✅ 技能管理界面        - 創建·編輯·刪除·執行技能
✅ 數據導出            - JSON·CSV·PDF 導出支持
✅ API 文檔            - OpenAPI 3.0.0·Swagger UI
✅ WebSocket           - 實時雙向通信
✅ 用戶認證            - JWT Token 驗證
```

---

## 🚀 快速開始

### 方式 1: 本地開發（推薦）

```bash
# 1️⃣ 進入目錄
cd ~/longhun-phase3

# 2️⃣ 後端啟動
source venv/bin/activate
pip install fastapi uvicorn pydantic sqlalchemy websockets
uvicorn phase3_backend_main:app --reload --port 8000

# 3️⃣ 前端啟動 (新終端窗口)
cd frontend
npm install
npm start

# 4️⃣ 訪問
# 前端: http://localhost:3000
# API: http://localhost:8000
# 文檔: http://localhost:8000/docs
```

### 方式 2: Docker Compose

```bash
cd ~/longhun-phase3
docker-compose up -d

# 訪問: http://localhost:3000
```

---

## 📁 目錄結構

```
phase3/
├── backend/
│   └── main.py                    # FastAPI 後端應用
├── frontend/
│   ├── src/
│   │   ├── App.jsx               # React 主組件
│   │   ├── App.css               # 樣式
│   │   ├── index.js              # 入口
│   │   └── index.css             # 全局樣式
│   ├── public/
│   │   └── index.html            # HTML 模板
│   └── package.json              # NPM 依賴
├── docs/
│   ├── PHASE3_DEPLOYMENT_GUIDE_v1_0.md
│   ├── PHASE3_API_SPECIFICATION_v1_0.md
│   ├── PHASE3_LAUNCH_COMPLETION_REPORT_v1_0.md
│   └── PHASE3_QUICK_REFERENCE_AND_EXECUTION_GUIDE.txt
├── launch-phase3.sh              # 一鍵啟動腳本
└── README.md                     # 本文件
```

---

## 🔗 訪問地址

| 地址 | 用途 | 說明 |
|------|------|------|
| **http://localhost:3000** | 前端 UI | React 應用 |
| **http://localhost:8000** | 後端 API | FastAPI 服務器 |
| **http://localhost:8000/docs** | Swagger UI | 交互式 API 文檔 |
| **http://localhost:8000/redoc** | Redoc | 備選 API 文檔 |

---

## 📚 文檔

| 文件 | 內容 |
|------|------|
| `docs/PHASE3_DEPLOYMENT_GUIDE_v1_0.md` | 完整部署配置指南 |
| `docs/PHASE3_API_SPECIFICATION_v1_0.md` | API 規格和端點文檔 |
| `docs/PHASE3_LAUNCH_COMPLETION_REPORT_v1_0.md` | 交付完成報告 |
| `docs/PHASE3_QUICK_REFERENCE_AND_EXECUTION_GUIDE.txt` | 快速參考 |

---

## 🔧 系統要求

### 最小配置
- CPU: 2 cores
- RAM: 2GB
- 磁碟: 1GB
- Python 3.8+
- Node.js 16+

### 推薦配置
- CPU: 4+ cores
- RAM: 4GB+
- 磁碟: 5GB+
- Python 3.11+
- Node.js 18+

---

## 📊 技術棧

### 後端
```
FastAPI          - 現代化 Python Web 框架
Uvicorn          - ASGI 伺服器
Pydantic         - 數據驗證
SQLAlchemy       - ORM 框架
WebSocket        - 實時通信
JWT              - 用戶認證
```

### 前端
```
React 18         - UI 框架
Axios            - HTTP 客戶端
Chart.js         - 圖表庫
CSS 3            - 樣式
WebSocket        - 實時更新
```

---

## 🎯 使用指南

### 第一次登錄
1. 訪問 http://localhost:3000
2. 使用默認賬戶登錄
3. 瀏覽儀表板

### 創建技能
1. 進入「技能管理」頁面
2. 點擊「新建技能」
3. 填寫技能信息
4. 保存並啟用

### 查看監控
1. 進入「實時監控」頁面
2. 查看系統指標
3. 設置告警閾值

### 導出數據
1. 進入「數據導出」頁面
2. 選擇時間範圍
3. 選擇導出格式
4. 下載文件

---

## 🔌 API 端點

### 健康檢查
```
GET /api/v1/health
```

### 技能管理
```
GET    /api/v1/skills              - 獲取所有技能
POST   /api/v1/skills              - 創建技能
GET    /api/v1/skills/{id}         - 獲取技能詳情
PUT    /api/v1/skills/{id}         - 更新技能
DELETE /api/v1/skills/{id}         - 刪除技能
POST   /api/v1/skills/{id}/execute - 執行技能
```

### 監控數據
```
GET /api/v1/metrics                - 獲取系統指標
GET /api/v1/metrics/history        - 獲取歷史數據
WebSocket /ws/v1/metrics           - 實時指標流
```

### 告警管理
```
GET    /api/v1/alerts              - 獲取告警列表
POST   /api/v1/alerts              - 創建告警
PUT    /api/v1/alerts/{id}         - 更新告警
DELETE /api/v1/alerts/{id}         - 刪除告警
```

---

## 🐛 故障排除

### 問題：端口已被占用
**解決**:
```bash
# 找到占用進程
lsof -i :8000
lsof -i :3000

# 終止進程
kill -9 <PID>

# 或使用不同端口
uvicorn main:app --port 8001
```

### 問題：依賴缺失
**解決**:
```bash
# 後端
pip install -r requirements.txt

# 前端
npm install
```

### 問題：WebSocket 連接失敗
**解決**:
```bash
# 檢查後端日誌
tail -f backend.log

# 確保後端運行在正確端口
# 檢查防火牆設置
```

---

## 📈 性能優化

```
✅ 代碼分割        - 按需加載組件
✅ 圖片優化        - 圖片壓縮和懶加載
✅ 緩存策略        - HTTP 緩存和瀏覽器緩存
✅ API 優化        - 響應壓縮和分頁
✅ 資源監控        - 性能指標追蹤
```

---

## 🚀 生產部署

### 使用 Docker
```bash
docker-compose --profile production up -d
```

### 使用 Nginx
```nginx
server {
    listen 80;
    server_name api.longhun-system.com;

    location /api/ {
        proxy_pass http://localhost:8000/api/;
    }

    location / {
        proxy_pass http://localhost:3000;
    }
}
```

### SSL/TLS
```bash
# 使用 Let's Encrypt
certbot certonly --standalone -d api.longhun-system.com
```

---

## 🔐 安全性

```
✅ JWT 認證       - 所有 API 端點受保護
✅ CORS 配置      - 跨域資源共享受限
✅ 輸入驗證       - 所有輸入都經過驗證
✅ 速率限制       - 防止 API 濫用
✅ HTTPS 支持     - 加密傳輸
✅ 環境變數       - 敏感信息外部化
```

---

## 📊 完整進度

```
Phase 1: ✅ 完成 (L0-L6 框架·2,070+ 行)
Phase 2: ✅ 完成 (智能報告·趨勢分析·告警·2,289+ 行)
Phase 3: 🟢 交付 (Web UI·監控·儀表板·即時可用)
────────────────────────────────────────
合計:    ✅ 100% 完成·4,359+ 行代碼·生產準備
```

---

## 🐉 DNA 簽章

```
DNA:#龍芯⚡️2026-06-06-PHASE3-WEB-UI-v1.0
責任: UID9622 · 不免責
時間: 2026-06-06 23:42 CST
狀態: 🟢 生產就緒·即時可用
```

---

## 📞 支持

有問題？查看：
1. 本 README
2. `docs/` 目錄中的詳細文檔
3. 後端日誌：`~/longhun-phase3/backend.log`
4. 前端日誌：`~/longhun-phase3/frontend/frontend.log`

---

**立即開始使用龍魂系統 Phase 3！** 🚀

訪問: http://localhost:3000
