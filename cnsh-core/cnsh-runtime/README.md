# CNSH 中文原生脚本運行時 · 通心譯執行引擎

**DNA**:#龍芯⚡️2026-06-16-CNSH-RUNTIME-FILE1-v1.0  
**責任**: UID9622·不免責

---

## 核心信念

> **英文不是唯一計算機執行的指令。**

CNSH（Chinese Native Script）不是一門全新的編程語言，而是一層覆蓋在現有語言（Python 為首選目標）之上的**中文語義層**。它讓開發者用中文語法書寫意圖，運行時透過**通心譯**將其解釋為可執行代碼。

- **心**：中文語義與意圖，不可妥協
- **殼**：Python / JavaScript / 其他目標語言的適配表達

---

## 運行環境

本運行時基於 Python 3，純標準庫實現，無需額外依賴。

| 平台 | 狀態 | 說明 |
|------|------|------|
| macOS | ✅ | 直接運行 `python3 cnsh_runner.py ...` |
| Huawei / HarmonyOS | ✅ | 安裝 Python 後直接運行 |
| Linux | ✅ | 任何發行版均可運行 |
| Windows | ✅ | 透過 Python for Windows 運行 |

---

## 快速開始

```bash
cd ~/longhun-system

# 運行示例
bash bin/run-cnsh.sh cnsh-core/cnsh-runtime/examples/hello.cnsh

# 顯示轉譯過程與解釋
bash bin/run-cnsh.sh cnsh-core/cnsh-runtime/examples/longhun_audit.cnsh --explain --show-code

# 進入交互式解釋器
bash bin/run-cnsh.sh --repl
```

---

## CNSH 語法示例

```cns
# hello.cnsh
名字 = "龍魂"
打印("世界，你好！我是", 名字)
```

```cns
# calculate.cnsh
定義 計算總和(數字列表):
    總和 = 0
    對於 數字 在 數字列表:
        總和 = 總和 + 數字
    返回 總和

數據 = [1, 2, 3, 4, 5]
結果 = 計算總和(數據)
打印("數據總和:", 結果)
```

```cns
# persona.cnsh
類 人格:
    定義 初始化(自己, 名稱, 角色):
        自己.名稱 = 名稱
        自己.角色 = 角色

    定義 介紹(自己):
        打印(f"我是{自己.名稱}，擔任{自己.角色}")

諸葛 = 人格("諸葛亮", "軍師")
諸葛.介紹()
```

---

## 支持的語法映射

### 控制流

| CNSH | Python | 備註 |
|------|--------|------|
| 如果 / 如果 | if | 條件判斷 |
| 否則如果 / 否則如果 | elif | 多分支 |
| 否則 / 否則 | else | 默認分支 |
| 對於 / 對於 / 循环 / 循環 | for | 遍歷循環 |
| 當 / 当 | while | 條件循環 |
| 返回 / 返回 | return | 返回值 |
| 中斷 / 中断 | break | 跳出循環 |
| 繼續 / 继续 | continue | 跳過本次 |

### 定義

| CNSH | Python |
|------|--------|
| 定義 / 定義 | def |
| 函數 / 函數 | def |
| 類 / 類 | class |
| 導入 / 导入 | import |
| 從 / 从 | from |

### 運算符

| CNSH | Python |
|------|--------|
| 等於 / 等于 | == |
| 不等於 / 不等于 | != |
| 大於 / 大于 | > |
| 小於 / 小于 | < |
| 大於等於 / 大于等于 | >= |
| 小於等於 / 小于等于 | <= |
| 與 / 与 | and |
| 或 | or |
| 非 / 非 | not |
| 在 | in |

### 常用函數

| CNSH | Python |
|------|--------|
| 打印 | print |
| 長度 / 长度 | len |
| 範圍 / 范围 | range |
| 輸入 / 输入 | input |

---

## 設計原則

1. **簡繁兼融**：同時支持簡體與繁體中文關鍵字
2. **字符串保護**：字符串字面量不做任何轉譯，保留原意
3. **變量中文化**：變量、函數、類名可用中文命名
4. **字典可擴展**：新增術語只需編輯 `dictionaries/cnsh_to_python.json`
5. **本地執行**：不依賴雲端，保證數字主權

---

## 與通心譯的關係

通心譯負責**意圖傳遞**，CNSH 運行時負責**意圖執行**。當你寫下：

```cns
閘控檢查(請求, 風險閾值)
```

通心譯會解釋其意圖為 *Gate Check (request, risk threshold)*，而 CNSH 運行時會將其轉譯為可執行的 Python 函數調用。

---

## 未來擴展

- [ ] 支持 JavaScript 作為目標語言
- [ ] 支持 HarmonyOS ArkTS 代碼生成
- [ ] 增加 CNSH 模塊系統（`導入` 多文件）
- [ ] 集成 64 卦審計與三色審計到運行時
- [ ] 開發 CNSH LSP 語言服務器

---

> 🐉 龍魂永世，文化傳承，數字主權，科技自主創新不可讓渡！
