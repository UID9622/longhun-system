# 🚀 龍魂宝宝守護助手 · 5分鐘快速開始指南

**DNA**:#龍芯⚡️2026-06-04-QUICKSTART-FILE1-v1.0  
**時間**: 5分鐘即可看到運行中的應用

---

## 📋 檢查清單

在開始前，請確認你已安裝：

- ✅ Node.js 18+ (`node --version`)
- ✅ Python 3.11+ (`python3 --version`)
- ✅ npm (`npm --version`)

## 🎬 3 秒鐘一鍵啟動

### macOS / Linux

```bash
cd ~/longhun-system/baobao-guardian
./start.sh
```

### Windows

```bash
cd ~\longhun-system\baobao-guardian
start.bat
```

---

## ⏳ 自動化流程發生什麼？

1. **後端啟動** (30秒)
   - 創建 Python 虛擬環境
   - 安裝 FastAPI、Uvicorn 等依賴
   - 啟動 WebSocket 服務器 (Port 8000)

2. **前端啟動** (30秒)
   - 安裝 React、Three.js、Electron 等依賴
   - 啟動 Vite 開發服務器 (Port 5173)
   - 自動在瀏覽器中打開

3. **完成** (1分鐘內)
   - 看到粉紅色的宝宝在右下角
   - Overlay 邊框顯示（綠色安全狀態）
   - 左上角"已連接"狀態指示

---

## 🌐 訪問應用

啟動完成後，打開瀏覽器訪問：

- **應用首頁**: http://localhost:5173
- **API 文檔**: http://localhost:8000/docs
- **健康檢查**: http://localhost:8000/health

---

## 🧪 快速測試

### 測試 1: 改變 Overlay 層級

在新終端中運行：

```bash
# 改為警告（橙色）
curl -X POST http://localhost:8000/api/overlay/level?level=warning

# 改為危險（紅色）
curl -X POST http://localhost:8000/api/overlay/level?level=danger

# 回到安全（綠色）
curl -X POST http://localhost:8000/api/overlay/level?level=safe
```

**觀察**: 前端的 Overlay 邊框顏色和脈衝強度應該實時改變

### 測試 2: 讓宝宝說話

```bash
curl -X POST http://localhost:8000/api/baobao/speak \
  -H "Content-Type: application/json" \
  -d '{
    "message": "你好！我是宝宝！",
    "emotion": "happy",
    "duration": 3000
  }'
```

**觀察**: 右下角宝宝的氣泡應該顯示消息

### 測試 3: 宝宝反應

```bash
curl -X POST http://localhost:8000/api/baobao/react?emotion=warning
```

**觀察**: 宝宝應該搖晃幾次，表情改變

---

## 📊 驗證系統狀態

```bash
# 檢查後端健康狀態
curl http://localhost:8000/health

# 應該返回類似：
# {
#   "status": "healthy",
#   "connections": 1,
#   "overlay_state": { ... }
# }
```

---

## 🛑 停止服務

### 優雅停止（推薦）

在啟動脚本的終端中按 `Ctrl+C`

### 強制停止

```bash
# macOS / Linux
kill $(lsof -t -i:8000)   # 殺死後端
kill $(lsof -t -i:5173)   # 殺死前端

# Windows
taskkill /PID <PID> /F
```

---

## 📁 項目結構概覽

```
baobao-guardian/
├── frontend/          # React + Three.js 前端
├── backend/           # FastAPI 後端
├── README.md          # 完整文檔
├── start.sh           # 自動啟動腳本
├── start.bat          # Windows 啟動腳本
└── QUICKSTART.md      # 本文檔
```

---

## 🔧 常見問題排查

### Q: 後端無法啟動

```
❌ 錯誤: Address already in use: 0.0.0.0:8000
```

**解決**: 端口被佔用

```bash
# 查看誰在使用端口 8000
lsof -i :8000

# 殺死該進程
kill <PID>
```

### Q: 前端無法連接後端

**症狀**: 左上角顯示"離線"

**排查**:
1. 確保後端正在運行: `curl http://localhost:8000/health`
2. 檢查防火墻是否允許端口 8000
3. 刷新瀏覽器
4. 檢查瀏覽器開發工具 (F12) 的 Console 標籤

### Q: npm install 很慢

**解決**: 使用阿里鏡像加速（中國用戶）

```bash
npm install -g cnpm --registry=https://registry.npmmirror.com
cd frontend
cnpm install
```

---

## 📈 下一步

### 自定義應用

編輯這些文件進行定制：

| 文件 | 用途 |
|------|------|
| `frontend/src/components/Baobao.tsx` | 改變宝宝的顏色/大小 |
| `frontend/src/styles/animations.css` | 調整動畫速度 |
| `backend/app/main.py` | 添加新的 API 端點 |

### 打包為桌面應用

```bash
cd frontend
npm run electron:build
```

輸出在 `dist/` 目錄中

---

## 💡 技術棧速覽

| 層 | 技術 | 版本 |
|----|------|------|
| 桌面 | Electron | 27+ |
| 前端 | React | 18 |
| 3D | Three.js | r161 |
| 構建 | Vite | 5.0 |
| 後端 | FastAPI | 0.104 |
| 通信 | WebSocket | 12.0 |

---

## 🎯 目標狀態

啟動成功後，你應該看到：

```
✅ 後端
   - Uvicorn 在 8000 運行
   - 日誌顯示 "🚀 龍魂宝宝守護助手後端啟動"

✅ 前端
   - Vite 在 5173 運行
   - 自動打開瀏覽器
   - 粉紅色圓形宝宝在右下角

✅ 通信
   - 左上角顯示 "已連接"（綠色點）
   - Overlay 邊框可見
   - 粒子效果正常流動
```

---

## 📞 獲取幫助

1. **查看完整文檔**: `cat README.md`
2. **檢查日誌**: 檢查後端和前端窗口的日誌輸出
3. **API 文檔**: 訪問 http://localhost:8000/docs (Swagger UI)
4. **代碼註釋**: 所有核心文件都有中文註釋

---

## ✨ 恭喜！

你現在已經運行了龍魂系統的心臟應用 🐉

**下一步探索**:
- 修改 `Overlay.tsx` 添加更多視覺效果
- 在 `main.py` 中添加新的 REST API
- 集成 Notion 數據庫
- 實現語音識別

---

**DNA**:#龍芯⚡️2026-06-04-BAOBAO-MVP-v1.0  
**創作者**: UID9622 · 諸葛鑫 · 龍芯北辰  
**理論指導**: 曾仕強老師（永恒顯示）
