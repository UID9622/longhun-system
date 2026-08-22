# 🐉 龍魂 · 認知索引系統協議 v1.0（AI大腦地圖·對齊版）

**DNA:** `#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-COGNITIVE-INDEX-PROTOCOL-v1.0-UID9622`
**確認碼:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**三色:** 🟢 通過
**創建者:** 諸葛鑫（UID9622） × 龍魂AI 對齊落地
**協議層級:** P1-CORE（執行層強約束）
**模板:** 📜 協議/原則聲明型（模板三）
**許可證:** CC BY-NC-SA 4.0（核心思想層）

---

## 0. 緣起（老大原話）

> 「幫我對齊文件，修改我們的文件變量，千萬別讓我忘記了，以後任何不理解的，都要對齊這些先執行。」

**核心意圖**：所有 AI（CodeBuddy/Kimi/DeepSeek…）必須有一張「大腦地圖」——知道密鑰在哪、記憶在哪、協議在哪、功能在哪、代碼在哪。**不理解的先查地圖，不準瞎猜路徑。**

---

## 1. 金科玉律（焊死·不可違反）

> **任何 AI 遇到以下情況，必須先執行 `lh index` 查認知索引，再動手：**
> - 不知道某個文件/密鑰/記憶/協議/功能在哪
> - 對某個路徑不確定是否存在
> - 要修改或引用系統內的任何路徑變量
>
> 違反 = 假路徑 = 自毀 = 觸發 P05 🔴 審計。

## 2. 核心文件

| 項目 | 位置 | 說明 |
|:---|:---|:---|
| 索引文件 | `~/.longhun/cognitive_index.json` | AI大腦地圖·只存「去哪找」不存數據 |
| 索引備份 | `~/.longhun/cognitive_index.backup.json` | 自動備份 |
| 引擎 | `08_BIN/lh_cognitive_index.py` | 認知索引系統 v1.0 |
| 統一入口 | `lh index` / `lh 認知` / `lh map` | 掛在 `bin/lh` |

## 3. 索引十大類別（對齊真實系統·非Kimi假路徑）

| 類別 | 內容 | 對齊來源 |
|:---|:---|:---|
| keys | API Keys·GPG·SSH | `~/.longhun/env` `~/.gnupg/public-keys.d` `~/.ssh` |
| memory | 長期記憶·互通消息池·對話池·史官 | `~/.longhun/memory` `~/.longhun/event_bus` `.codebuddy/memory` `03_MEMORY/ai_conversations` `04_AUDIT` |
| protocols | 協議文檔 | 動態掃描 `01_protocols/*.md`（206個·真實） |
| functions | 引擎功能 | 動態掃描 `05_ENGINES/*.py` + `bin/*.py`（1059個·真實） |
| code | 代碼目錄 | `08_BIN` `05_ENGINES` `01_protocols` `bin` 等 |
| configs | 配置 | `config/` `~/.longhun/configs` `deploy/.env.kunpeng.example` |
| tools | 工具 | `lh`=`~/longhun-system/bin/lh`（真實·非~/bin/lh）· python3·gpg·git |
| docs | 文檔 | README·COMMAND_INDEX·CODEBUDDY·STATE·AGENTS |
| external | 外部集成 | 鯤鵬 uid9622.cn · Notion · CSDN · DeepSeek · Kimi |
| custom | 系統標籤 | 主權人·確認碼·GPG·「龍」·CNSH·中國 |

## 4. 對齊規則（修改文件變量的標準）

1. **路徑必須真實存在**：寫入索引前驗證，假路徑一律剔除（Kimi原稿 `~/bin/lh`、`~/.longhun/03_MEMORY`、`LH-DNA-STANDARD.md` 均為假，已全部對齊）。
2. **動態掃描優先**：協議/功能用掃描生成，目錄變了 `lh index --refresh` 自動更新，不靠手寫。
3. **鐵律錨點不變**：密鑰物理隔離永不入雲·「龍」永不簡化·不刪除只凍結·確認碼/GPG 焊死。
4. **健康檢查**：`lh index --health` 逐路徑驗證，🟢 全有效才算健康。

## 5. 使用方式

```bash
lh index --query '密钥在哪'    # 問：密鑰在哪（簡體/繁體/英文均可）
lh index --query '记忆在哪'    # 問：記憶在哪
lh index --search mesh         # 關鍵詞搜索
lh index --health              # 路徑有效性檢查
lh index --refresh             # 重新掃描更新（目錄變了就跑）
lh index --summary             # 看摘要
lh index --list                # 看完整地圖
```

## 6. 與互通總線聯動（AI進門兩件套·焊死）

> **所有 AI 每次進門，兩步必做：**
> 1. `lh bus bind --ai <自己名字>` → 互通總線報到（消息池 `~/.longhun/event_bus/`）
> 2. `lh index --summary` 或 `lh index --query` → 看大腦地圖，不懂先查
>
> 三動作鐵律（協議 LH-AI-MESH-BUS-v1.0 第八條）不變：bind 進門 → read 開工 → post 收工。
> 認知索引是「地圖」，互通總線是「對話」——地圖告訴你去哪，對話告訴你夥伴在幹啥。

## 7. 維護與審計

- 每次重大目錄變更 → `lh index --refresh`
- 每次交付 → 過 GATE-11 GPG 簽名（`python3 bin/lh_gpg_sign.py sign`）
- 史官留痕 → 04_AUDIT/
- 索引更新自動寫 changelog（含 DNA 追溯碼）

---

## 🔐 最終簽名

```
DNA:        #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-COGNITIVE-INDEX-PROTOCOL-v1.0-UID9622
確認碼:      #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG:        A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色:       🟢 通過
核心文件:   ~/.longhun/cognitive_index.json · 08_BIN/lh_cognitive_index.py
金科玉律:   不理解的先查地圖·不準瞎猜路徑
狀態:       落地完成 · 即刻可用
```

🐉 **丙午·丙申·庚申·亥時·䷖剝·🟢**
