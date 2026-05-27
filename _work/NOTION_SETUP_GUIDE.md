# 🐉 龍魂Notion自動化同步·完整配置指南

**DNA**: `#龍芯⚡️2026-05-28-NOTION-SETUP-GUIDE-v1.0`
**目的**: 實現本地+Notion雙向同步·支付系統自動更新

---

## 【快速配置·5分鐘】

### Step 1: 創建Notion Integration

訪問 → https://www.notion.com/my-integrations

```
1. 點擊 "Create new integration"
2. 名稱: "龍魂支付系統同步"
3. 選擇 "Internal Integration"
4. 複製 "Internal Integration Token"
   格式: secret_xxxxxxxxxxxxx
5. 保存到 ~/.env:
   NOTION_TOKEN=secret_xxxxxxxxxxxxx
```

### Step 2: 授權Integration訪問頁面

需要更新的4個頁面，每個都要授權：

```
1️⃣ "為什麼只收數字人民幣？" 頁面
   → 點右上角 "..."
   → "Connect to"
   → 選擇你的Integration

2️⃣ "數字人民幣DNA綁定協議" 頁面
   → 同上

3️⃣ "龍魂普惠經濟規則" 頁面
   → 同上

4️⃣ "龍芯知識專欄·版權聲明" 頁面
   → 同上
```

### Step 3: 執行自動化

```bash
cd ~/longhun-system/_work
python3 update_notion_payment_system.py
```

**输出示例：**
```
======================================================================
🐉 龍魂Notion支付系統自動化同步
DNA: #龍芯⚡️2026-05-28-NOTION-PAYMENT-UPDATE-v1.0
======================================================================

【為什麼只收數字人民幣？】
  🔍 搜索頁面: 為什麼只收數字人民幣？...
    ✅ 找到: 為什麼只收數字人民幣？ (ID: a1b2c3d4...)
  📝 更新標題: 為什麼只收數字人民幣？ → 為什麼用Stripe全球支付？
    ✅ 標題已更新
  📄 追加新內容...
    ✅ 內容已追加

... (重複3次) ...

======================================================================
✅ 成功: 4
❌ 失敗: 0
======================================================================
```

---

## 【故障排除】

### ❌ "No NOTION_TOKEN"

```bash
# 檢查 .env 文件
cat ~/.env | grep NOTION_TOKEN

# 如果顯示 "your_notion_integration_token"
# 說明未配置，請按 Step 1 操作
```

### ❌ "未找到該頁面"

```bash
# 確認頁面已授權給Integration
# 在Notion中點擊頁面右上角"..."
# 看是否能看到你的Integration名稱

# 如果看不到，說明未授權
# 請按 Step 2 操作
```

### ❌ "搜索失敗"

```bash
# 1. 檢查token是否正確
echo $NOTION_TOKEN

# 2. 測試API連接
curl -X GET https://api.notion.com/v1/pages/test \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28"

# 如果返回認證錯誤，token有誤
```

---

## 【完整自動化流程】

執行後會自動做以下事情：

### 頁面1: "為什麼只收數字人民幣？"
- ✅ 改標題 → "為什麼用Stripe全球支付？"
- ✅ 追加完整的Stripe解釋
- ✅ 保留原始內容（可手動刪除）

### 頁面2: "數字人民幣DNA綁定協議"
- ✅ 改標題 → "Stripe激活協議v1.0"
- ✅ 追加Stripe支付流程說明
- ✅ 包含150+國家支付方式表

### 頁面3: "龍魂普惠經濟規則"
- ✅ 加入新的支付政策部分
- ✅ 強調"全球法幣·無差別"原則
- ✅ 列出Stripe費用和激活等級

### 頁面4: "龍芯知識專欄·版權聲明"
- ✅ 追加收款說明部分
- ✅ 解釋Stripe全球支付
- ✅ 提供激活流程說明

---

## 【完全自動化的終極方案】

如果希望完全無人工操作，可以設置定時任務：

### macOS (Cron)

```bash
# 編輯 crontab
crontab -e

# 添加以下行（每天00:30執行）
30 0 * * * cd ~/longhun-system/_work && python3 update_notion_payment_system.py >> ~/longhun-system/logs/notion-sync.log 2>&1
```

### 或使用 launchd (macOS 推薦)

```bash
# 創建 plist 文件
cat > ~/Library/LaunchAgents/com.longhun.notion-sync.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.longhun.notion-sync</string>
    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/opt/python@3.14/bin/python3.14</string>
        <string>/Users/zuimeidedeyihan/longhun-system/_work/update_notion_payment_system.py</string>
    </array>
    <key>StartInterval</key>
    <integer>86400</integer>
    <key>StandardOutPath</key>
    <string>/Users/zuimeidedeyihan/longhun-system/logs/notion-sync.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/zuimeidedeyihan/longhun-system/logs/notion-sync-error.log</string>
</dict>
</plist>
EOF

# 加載任務
launchctl load ~/Library/LaunchAgents/com.longhun.notion-sync.plist

# 驗證運行
launchctl list | grep notion-sync
```

---

## 【本地+Notion完整同步架構】

```
本地文件系統                    Notion 雲端
┌─────────────────────┐        ┌──────────────────┐
│ 龍魂生態·全球法幣  │        │ Stripe激活協議  │
│ 收款說明.md         │   ←→   │ v1.0 (Notion)   │
└─────────────────────┘        └──────────────────┘
         ↑                               ↑
    Git 版本控制                    Notion 編輯
         ↓                               ↓
┌─────────────────────┐        ┌──────────────────┐
│ 龍魂開源宪章       │        │ 龍魂普惠經濟   │
│ PART THREE (改動)  │   ←→   │ 規則v2.0       │
└─────────────────────┘        └──────────────────┘
         ↓
    Commit 4bf0d26e
    DNA: #龍芯⚡️2026-05-28-PAYMENT-SYSTEM-REBUILD-v1.0
```

### 雙向同步規則

✅ **本地 → Notion**
- 每當本地文件更新時
- 執行 `update_notion_payment_system.py`
- 自動推送到Notion

✅ **Notion → 本地**
- 使用 `notion_sync.py` 的讀取功能
- 下載Notion最新內容
- 存檔到本地 `docs/notion-backups/`

---

## 【核心文件列表】

| 文件 | 用途 | 狀態 |
|------|------|------|
| update_notion_payment_system.py | Notion自動更新 | ✅ 已創建 |
| notion_sync.py | Notion讀寫API包裝 | ✅ 已存在 |
| NOTION_SETUP_GUIDE.md | 本文件 | ✅ |
| ~/.env | 配置Token | ⚠️ 需配置 |

---

## 【驗證配置】

執行此命令檢查所有配置：

```bash
#!/bin/bash
echo "🐉 龍魂Notion配置檢查"
echo ""

# 1. 檢查環境變量
echo "1️⃣ NOTION_TOKEN 配置"
if grep -q "NOTION_TOKEN=secret_" ~/.env 2>/dev/null; then
    echo "   ✅ Token已配置"
else
    echo "   ❌ Token未配置或格式錯誤"
    echo "   位置: ~/.env"
fi

# 2. 檢查Python
echo ""
echo "2️⃣ Python環境"
if python3 --version 2>/dev/null; then
    echo "   ✅ $(python3 --version)"
else
    echo "   ❌ Python3未安裝"
fi

# 3. 檢查更新腳本
echo ""
echo "3️⃣ 更新腳本"
if [ -f "update_notion_payment_system.py" ]; then
    echo "   ✅ update_notion_payment_system.py 存在"
else
    echo "   ❌ 腳本不存在"
fi

# 4. 檢查Notion連接（需要token）
echo ""
echo "4️⃣ Notion API連接"
if [ -n "$NOTION_TOKEN" ]; then
    echo "   🔍 測試連接..."
    # 這裡可以加測試代碼
    echo "   (需要在Notion中授權Integration後測試)"
fi

echo ""
echo "✅ 檢查完成"
```

---

## 【DNA追溯】

本配置文件的完整歷史：

```
創建時間: 2026-05-28 01:30 CST
DNA: #龍芯⚡️2026-05-28-NOTION-SETUP-GUIDE-v1.0
作者: Claude Haiku 4.5 + UID9622
目的: 完全自動化本地+Notion同步
狀態: 🟢 待用戶配置NOTION_TOKEN
```

---

**一旦配置完成，所有Notion更新將自動進行。不再需要手工編輯。**

🐉
