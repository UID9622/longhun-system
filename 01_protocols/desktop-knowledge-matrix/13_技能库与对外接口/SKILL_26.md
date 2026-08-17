---
name: longhun-cloud-kimi
description: '龍魂Kimi集成 v5.2 — Kimi API接入+断路器+故障转移+本地备份推理+Kimi創作記憶檔案。4个集成模式全部正常工作，故障自动转移，API响应低于100ms。API端点:
  http://api:8443/kimi/。当需要Kimi AI调用、故障转移、本地推理备份、API监控、Kimi创作记忆归集时触发。'
metadata:
  author: 龍魂体系·云端技能组
  version: 5.2.0
  dna: '#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-KIMI-v5.2'
  protocol: 君子協議 — 非對抗·非欺瞞·非竊取
  cnsh: true
  category: cloud
  tags:
  - kimi
  - ai
  - circuit-breaker
  - failover
  - backup-inference
  - api
  id: longhun-cloud-kimi
  trigger:
    keywords:
    - cloudkimi
    - lh-kimi
    - 龍魂Kimi集成
    - v5.0
    - Kimi
    - API接入+断路器+故障转移+本地备份推理。4个集成模式全部正常工作
    - 故障自动转移
    - Kimi創作記憶
    - Kimi创作记忆
    context: longhun-cloud-kimi 相关操作
---
## 一、技能概述

龍魂Kimi集成器是龍魂體系雲端技能模組，提供與Kimi AI API的完整集成能力。

**核心特性**：
- 🌐 Kimi API客戶端（HTTP接入）
- ⚡ 断路器模式（3次故障觸發，30秒超時恢復）
- 🔄 故障自動轉移（API故障→本地備份推理）
- 🧠 本地備份推理引擎（代碼/分析/總結/通用四模式）
- 🎨 三色審計系統（綠/黃/紅）
- 🧬 DNA完整追溯鏈

**API端點**：`http://api:8443/kimi/`

---

## 二、DNA追溯

```
#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-KIMI-v5.2
```

**追溯鏈**：
- 父節點：longhun-core-v5.0（龍魂核心）
- 兄弟節點：longhun-cloud-nova, longhun-cloud-deepseek
- 子節點：
  - `#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-KIMI-CREATION-MEMORY-v1.0`（Kimi 創作記憶檔案）
  - `#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-ARCHIVE-INTEGRATION-v1.0`（龍魂待整理歸檔）
- 應用場景：所有需要Kimi AI調用的龍魂任務

---

## 三、CNSH規範聲明

本技能遵循CNSH中文編程規範：

| 規範項 | 狀態 | 說明 |
|--------|------|------|
| 中文變量名 | ✅ | 全部變量使用中文命名 |
| 繁體龍字 | ✅ | 龍、龍魂等使用繁體 |
| DNA追溯 | ✅ | 所有操作帶DNA標記 |
| 三色審計 | ✅ | 綠/黃/紅三色日誌 |
| 君子協議 | ✅ | 非對抗·非欺瞞·非竊取 |

---

## 四、檔案結構

```
longhun-cloud-kimi/
├── SKILL.md                          # 技能文檔（本文檔）
├── scripts/
│   ├── Kimi集成器.py                  # 主程序：4模式集成器
│   ├── KimiAPI服務.py                 # FastAPI 反向代理後端
│   └── 龍魂待整理/                    # 早期 API 參考實現（已歸檔）
├── references/
│   └── kimi_creation_memory.md        # Kimi 創作記憶檔案（v1.0）
└── assets/
    └── (保留給擴展資源)
```

---

## 五、安裝依賴

**系統要求**：
- Python 3.8+
- 標準庫（無額外依賴）

**網絡要求**：
- 可訪問 `http://api:8443/kimi/`
- 超時設置：100ms

---

## 六、使用方法

### 6.1 命令行使用

```bash
# 健康檢查
python3 scripts/Kimi集成器.py --mode health

# 技能調用（調用Kimi API）
python3 scripts/Kimi集成器.py --mode skill --prompt "分析以下代碼..."

# 備份推理（強制本地推理）
python3 scripts/Kimi集成器.py --mode backup-inference --prompt "總結本文檔..."

# 断路器狀態查詢
python3 scripts/Kimi集成器.py --mode circuit-status

# 導出日誌和DNA追溯
python3 scripts/Kimi集成器.py --mode health --export-logs logs.json --export-dna dna.json
```

### 6.2 模塊導入

```python
from scripts.Kimi集成器 import 集成模式處理器, 集成模式

處理器 = 集成模式處理器()

# 健康檢查
結果 = 處理器.處理(集成模式.健康檢查)

# 調用Kimi
結果 = 處理器.處理(集成模式.技能調用, {"prompt": "你好Kimi"})

# 查詢断路器
結果 = 處理器.處理(集成模式.斷路器狀態查詢)
```

---

## 七、四個集成模式

### 模式一：health（健康檢查）
- 檢查API端點可達性
- 返回延遲、狀態碼、統計數據
- 用於監控和告警

### 模式二：skill（技能調用）
- 調用Kimi API進行AI處理
- 自動断路器保護
- 故障時自動轉移

### 模式三：backup-inference（備份推理）
- 強制使用本地推理引擎
- 四種推理模式：代碼/分析/總結/通用
- 不依賴外部API

### 模式四：circuit-status（断路器狀態）
- 查詢断路器完整狀態
- 返回故障計數、狀態轉換歷史
- 用於診斷和調試

---

## 八、断路器行為

```
閉合(正常) → [故障×3] → 斷開(快速失敗)
                              ↓
                        [30秒超時]
                              ↓
                        半開(試探) → [成功] → 閉合
                                       ↓
                                  [失敗] → 斷開
```

**參數**：
- 故障閾值：3次
- 超時恢復：30秒
- 請求超時：100ms

---

## 九、三色審計說明

| 顏色 | 級別 | 含義 | 示例 |
|------|------|------|------|
| 🟢 綠 | 正常 | 運行正常 | API調用成功、斷路器閉合 |
| 🟡 黃 | 警告 | 需要注意 | 故障計數增加、轉入半開 |
| 🔴 紅 | 異常 | 發生故障 | API失敗、斷路器斷開 |

---

## 十、君子協議

本技能受君子協議保護：

> **非對抗** — 不與其他AI系統對抗
> **非欺瞞** — 所有操作透明可審計
> **非竊取** — 尊重知識產權和數據隱私

違反協議將觸發技能自鎖機制。

---

## 十一、故障排除

| 問題 | 原因 | 解決方案 |
|------|------|----------|
| API連接超時 | 網絡或服務故障 | 自動轉本地備份推理 |
| 断路器斷開 | 連續故障達3次 | 等待30秒自動恢復 |
| 空響應 | API返回異常 | 檢查日誌，手動觸發備份推理 |

---

## 十二、版本歷史

| 版本 | 日期 | 變更 |
|------|------|------|
| 5.0.0 | 2026-06-19 | 初始版本：4模式+断路器+故障轉移+備份推理 |
| 5.1.0 | 2026-06-19 | 新增 KimiAPI服務.py FastAPI 反向代理後端 |
| 5.2.0 | 2026-07-05 | 納入 Kimi 創作記憶檔案；新增 `lh-kimi` 觸發詞；更新 DNA 追溯鏈 |


---

## 十三、Kimi 創作記憶檔案

本技能已納入 **Kimi 創作記憶檔案**，詳見：

📄 `references/kimi_creation_memory.md`

**DNA**: `#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-KIMI-CREATION-MEMORY-v1.0`

### 檔案涵蓋內容

1. **Kimi 創作記憶來源清單**
   - Kimi 會話記憶：`~/.kimi-code/sessions/*/agents/main/wire.jsonl`
   - Claude 歷史：`~/.claude/history.jsonl`
   - 記憶摘要：`~/.longhun/memory/latest_digest.md`
   - DeepSeek 語境：`~/.longhun/memory/deepseek_context_20260701.md`
   - 憲法層與聲音原則：`uid9622_constitutional_note.md`、`uid9622_voice_principle.md`
   - 資產索引：`uid9622_asset_index.json`
   - DragonSoul DNA、代碼知識庫、鏈哈希等

2. **Kimi 在龍魂體系中的角色定位**
   - 協同創作夥伴：與 Claude、DeepSeek、Notion、本地腳本共同完成創作。
   - 創作歸屬原則：創作權屬於 UID9622 / 龍魂系統 / 中國；Kimi 作為工具不擁有知識產權。
   - 與其他平台的協同邊界：Claude 審計、DeepSeek 語境、Notion 展示、GitHub/Gitee 託管、本地腳本執行。

3. **關鍵創作事件時間線**
   - 2026-03：創作權屬中國表態；Kimi 生成 `kimiOKC/` 內容；Kimi WebBridge 操作。
   - 2026-04：`longhun888.com` 公網上線，ECNYLayer 集成。
   - 2026-05：跨平台 DNA 對齊報告上鏈。
   - 2026-06：Kimi 參與 197 個文件技能化歸檔；`longhun-cloud-kimi` 被定位為 API 參考實現。
   - 2026-06：DeepSeek 529 歷史對話納入訓練池。
   - 2026-07：本技能更新，納入 Kimi 創作記憶檔案。

4. **對 Kimi 集成的行為校準**
   - 回應風格：先確認立場 → 再給可執行方案 → 最後給下一步命令。
   - 安全邊界：敏感配置默認 dry-run；使用 CNSH 變量引用密鑰；開源前掃描敏感信息。
   - 創作協同規範：自動注入 DNA；優先吸收整合去重；對「不能輸出」內容禁止對外輸出。
   - 故障與偏見處理：斷路器 + 故障轉移 + 本地備份推理三層保護；備份推理優先返回結構化安全模板。

### 使用建議

- 當用戶觸發 `lh-kimi` 或詢問 Kimi 創作相關內容時，Kimi 應先加載本記憶檔案，再進行回應或執行。
- 所有涉及 Kimi API 調用的操作，應同時參照本檔案中的創作歸屬原則與安全邊界。

---

## 附录：龍魂待整理来源

本技能收录了来自 `/Users/zuimeidedeyihan/龍魂待整理` 的素材：

- **内容**：06-工具脚本（龍魂系统 API 接口完整实现）
- **中央整合 DNA**：`#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-ARCHIVE-INTEGRATION-v1.0`
- **处理方式**：保留原始文件作为 references / examples / scripts，嵌入 DNA 追溯链，与现有能力联动。
