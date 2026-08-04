# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
---
name: longhun-multicurrency
description: 龍魂多币种直达系统 - 支持10种货币实时行情、汇率转换、e-CNY跨境支付、龍字规范化
metadata:
  display_name: 龍魂多币种直达系统
  version: "5.2.1"
  author: 龍魂工程師
  dna: "#龍芯⚡️2026-06-19-LONGHUN-MULTICURRENCY-v5.2"
  tags: [finance, currency, exchange, ecny, dragon]
compatibility: Python 3.8+, Linux/macOS/Windows
---

# 🐉 龍魂多币种直达系统 (longhun-multicurrency)

**DNA**: `#龍芯⚡️2026-06-19-LONGHUN-MULTICURRENCY-v5.2`

---

## 1. 技能概述 (Overview)

龍魂多币种直达系统是龍魂體系的金融核心模組，提供多币种實時行情、匯率轉換、龍字規範化等完整功能。支持 CNY/USD/EUR/GBP/JPY/KRW/HKD/SGD/BTC/ETH 共10種貨幣的實時匯率查詢與轉換，並特別支持 e-CNY 數字人民幣跨境支付通道。

---

## 2. 适用场景 (Use Cases)

| 场景 | 描述 |
|------|------|
| 跨境電商結算 | 多幣種實時匯率查詢與轉換 |
| 投資組合管理 | 加密貨幣與法幣價格監控 |
| e-CNY跨境支付 | 數字人民幣跨境通道支持 |
| 多語言金融應用 | 龍字繁簡規範化與幣種名稱標準化 |
| 金融數據分析 | 行情歷史記錄與趨勢分析 |
| CLI快速查詢 | 命令行直達查詢任意幣種匯率 |

---

## 3. 支持的币种 (Supported Currencies)

| 代碼 | 名稱 | 符號 | 類型 | 精度 |
|------|------|------|------|------|
| CNY | 人民幣 | ¥ | 法幣 | 2 |
| USD | 美元 | $ | 法幣 | 2 |
| EUR | 歐元 | € | 法幣 | 2 |
| GBP | 英鎊 | £ | 法幣 | 2 |
| JPY | 日元 | ¥ | 法幣 | 0 |
| KRW | 韓元 | ₩ | 法幣 | 0 |
| HKD | 港幣 | HK$ | 法幣 | 2 |
| SGD | 新加坡元 | S$ | 法幣 | 2 |
| BTC | 比特幣 | ₿ | 加密 | 8 |
| ETH | 以太坊 | Ξ | 加密 | 8 |

---

## 4. 文件清单 (File Inventory)

```
longhun-multicurrency/
├── SKILL.md                          # 本文件
├── scripts/
│   ├── 多币种行情中心.py              # C9-001 核心行情模組
│   ├── 汇率转换器.py                  # C9-002 匯率轉換模組
│   └── 龍字规范化器.py                # C9-003 字符編碼模組
```

---

## 5. 快速开始 (Quick Start)

### 5.1 更新全部匯率並顯示面板

```bash
python3 scripts/多币种行情中心.py --update --panel
```

### 5.2 查詢指定匯率

```bash
python3 scripts/多币种行情中心.py --query USD/CNY
python3 scripts/汇率转换器.py --rate USD CNY
```

### 5.3 執行匯率轉換

```bash
python3 scripts/汇率转换器.py --convert 100 USD CNY
python3 scripts/汇率转换器.py --convert 5000 CNY EUR
```

### 5.4 e-CNY 跨境轉換

```bash
python3 scripts/汇率转换器.py --ecny 10000 USD
```

### 5.5 龍字規範化

```bash
python3 scripts/龍字规范化器.py --normalize "龙魂多币种系统"
python3 scripts/龍字规范化器.py --panel
```

---

## 6. API 参考 (API Reference)

### 6.1 多幣種行情中心 (多币种行情中心.py)

```python
from scripts.多币种行情中心 import 多幣種行情中心

# 創建實例
中心 = 多幣種行情中心(數據目錄="~/.longhun", 緩存時間=300)

# 更新全部匯率
快照 = 中心.更新全部匯率(強制刷新=False)

# 獲取指定匯率
記錄 = 中心.獲取匯率("USD", "CNY")
print(f"1 USD = {記錄.中間價} CNY")

# 查詢幣種對（支持多種格式）
記錄 = 中心.查詢幣種對("USD/CNY")
記錄 = 中心.查詢幣種對("USDCNY")

# 獲取行情面板
print(中心.獲取行情面板())

# 健康檢查
健康, 描述 = 中心.健康檢查()
```

### 6.2 匯率轉換器 (汇率转换器.py)

```python
from scripts.汇率转换器 import 匯率轉換器, 數字人民幣跨境通道

# 創建轉換器
轉換器 = 匯率轉換器(默認手續費率=0.001)

# 單筆轉換
記錄 = 轉換器.轉換(金額=100, 來源幣種="USD", 目標幣種="CNY")
print(f"結果: {記錄.實際到賬} CNY")

# 批量轉換
結果 = 轉換器.批量轉換(1000, "CNY", ["USD", "EUR", "JPY"])

# 快速查詢匯率
匯率 = 轉換器.快速查詢("USD", "CNY")

# e-CNY 跨境
通道 = 數字人民幣跨境通道(轉換器)
通道.eCNY跨境轉換(10000, "USD")
```

### 6.3 龍字規範化器 (龍字规范化器.py)

```python
from scripts.龍字规范化器 import 龍字規範化器

# 創建實例
規範化器 = 龍字規範化器()

# 規範化文本（龍字統一為 U+9F8D）
結果 = 規範化器.規範化("龙魂体系")  # → "龍魂體系"

# 分析文本
分析 = 規範化器.分析文本("龙魂龙币")
print(f"發現 {len(分析.發現的龍字)} 個龍字")

# 容錯搜索
匹配 = 規範化器.容錯搜索("龍魂", "龙魂体系介绍")

# 生成DNA校驗碼
DNA = 規範化器.生成龍字DNA("龍魂多币种系统")
```

---

## 7. 命令行参数 (CLI Reference)

### 多币种行情中心

| 参数 | 说明 |
|------|------|
| `--update, -u` | 更新全部匯率 |
| `--query, -q` | 查詢指定匯率（如 USD/CNY） |
| `--panel, -p` | 顯示行情面板 |
| `--status, -s` | 查看系統狀態 |
| `--force, -f` | 強制刷新 |
| `--cache-dir` | 設置緩存目錄 |
| `--cache-time` | 設置緩存過期時間（秒） |

### 汇率转换器

| 参数 | 说明 |
|------|------|
| `--convert, -c` | 轉換金額（金額 來源 目標） |
| `--rate, -r` | 查詢匯率（來源 目標） |
| `--rates` | 列出基準幣對所有幣種匯率 |
| `--batch` | 批量轉換（金額 來源 目標1 目標2 ...） |
| `--ecny` | e-CNY 跨境轉換（金額 目標幣） |
| `--ecny-panel` | 顯示 e-CNY 面板 |
| `--history` | 查看轉換歷史 |
| `--panel, -p` | 顯示完整面板 |
| `--fee` | 自定義手續費率 |

### 龍字规范化器

| 参数 | 说明 |
|------|------|
| `--normalize, -n` | 規範化文本 |
| `--analyze, -a` | 分析文本中的龍字 |
| `--check` | 檢查規範性 |
| `--search` | 容錯搜索 |
| `--char` | 獲取字符 Unicode 信息 |
| `--terms, -t` | 列出龍魂術語 |
| `--currency, -c` | 獲取幣種信息 |
| `--panel, -p` | 顯示完整面板 |
| `--dna` | 生成 DNA 校驗碼 |

---

## 8. 数据说明 (Data Sources)

| 數據類型 | 數據源 | 更新頻率 | 備註 |
|----------|--------|----------|------|
| 法幣匯率 | exchangerate-api.com | 實時 | 免費API，無需密鑰 |
| 加密貨幣 | CoinGecko API | 實時 | 免費層，有限頻率 |
| 本地緩存 | JSON文件 | 5分鐘過期 | 默認路徑 ~/.longhun/multicurrency |
| 轉換歷史 | JSON文件 | 即時 | 保留最近1000條 |

---

## 9. 缓存与过期策略 (Caching)

```
默認緩存過期時間: 300秒 (5分鐘)
緩存目錄: ~/.longhun/multicurrency/
緩存文件: exchange_cache.json, conversion_history.json

過期策略:
  🟢 < 5分鐘: 數據新鮮，直接使用
  🟡 5-15分鐘: 緩存可用，後台更新
  🔴 > 15分鐘: 數據過期，強制刷新
```

---

## 10. 注意事项 (Cautions)

1. **免責聲明**: 本系統提供的匯率僅供參考，實際交易請以銀行或交易所牌價為準
2. **API限制**: 免費API有頻率限制，頻繁調用可能觸發限制
3. **網絡依賴**: 首次使用需要網絡連接，後續可使用緩存
4. **精度問題**: 加密貨幣精度為8位小數，法幣為2位
5. **合規提示**: e-CNY跨境支付需遵守相關法規，大額交易需申報
6. **君子協議**: 禁止用於洗錢、逃稅、非法跨境資金轉移

---

## 11. 版本历史 (Changelog)

| 版本 | 日期 | 变更 |
|------|------|------|
| v5.2.0 | 2026-06-19 | 初始版本，10幣種完整支持 |
| v5.2.1 | 2026-06-19 | 新增 e-CNY 跨境支付通道接口 |

---

## 12. 君子协议 (License)

```
龍魂開源誓約 (Dragon Soul Open Source Pledge)
═══════════════════════════════════════════════

本軟體遵循龍魂開源誓約發布：

1. 使用者可自由使用、修改、分發本軟體
2. 修改版本須保留原始DNA標識與審計追蹤
3. 禁止用於洗錢、逃稅、非法跨境資金轉移
4. 所有交易記錄留痕，可追溯可審計
5. 使用本軟體即表示同意以上條款

DNA: #龍芯⚡️2026-06-19-LONGHUN-MULTICURRENCY-v5.2
```

---

*🐉 龍魂體系 - 多币种直达系统 v5.2.1*
