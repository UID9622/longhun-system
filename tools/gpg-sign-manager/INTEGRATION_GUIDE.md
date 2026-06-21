# 🐉 GPG簽署管理工具 · 整合指南

**DNA**: #龍芯⚡️2026-06-08-GPG-SIGN-MANAGER-INTEGRATION
**時間**: 2026-06-08 CST
**來源**: 桌面 CNSH_v2.0_SIGN → 融入主干 longhun-system

---

## 目錄結構

```
~/longhun-system/tools/gpg-sign-manager/
├── gpg_sign_manager.py              # 統一GPG簽署管理工具（新建）
├── CNSH_v2.0_SIGNATURE.md           # CNSH v2.0協議簽署聲明
├── CNSH_v2.0_FULL_PROTOCOL_SIGNATURE.md  # 完整協議簽署
├── cnsh_gateway.py                  # CNSH Gateway v2.0入口
├── cnsh.py                          # CNSH編程引擎基礎
├── CNSH_v2.0_SIGN_README.md         # 原始說明文檔
└── INTEGRATION_GUIDE.md             # 本文件
```

---

## 功能說明

### 1. GPG簽署管理工具 (`gpg_sign_manager.py`)

**用途**: 統一管理CNSH核心文檔與代碼的GPG簽名

**命令**：
```bash
# 簽署所有文件
python3 gpg_sign_manager.py --sign

# 驗證現有簽名
python3 gpg_sign_manager.py --verify

# 指定工作目錄
python3 gpg_sign_manager.py --sign --dir /path/to/work
```

**特性**：
- ✅ 自動檢查GPG密鑰可用性
- ✅ 批量簽署協議與代碼文件
- ✅ JSON日誌記錄（gpg_sign_log.json）
- ✅ 簽名驗證功能
- ✅ 詳細的執行日誌

### 2. CNSH協議文檔

- `CNSH_v2.0_SIGNATURE.md`: Claude的正式簽署聲明（包含7層約束）
- `CNSH_v2.0_FULL_PROTOCOL_SIGNATURE.md`: 完整協議簽署

### 3. 核心代碼

- `cnsh_gateway.py`: CNSH v2.0統一入口（22KB）
  - 三色審計、SQLite日誌、Flask HTTP、Ollama代理

- `cnsh.py`: CNSH中文編程引擎基礎（7KB）
  - Notion接入、指令解析、頁面操作

---

## 使用示例

### 快速簽署

```bash
cd ~/longhun-system/tools/gpg-sign-manager/
python3 gpg_sign_manager.py --sign
```

### 驗證簽名

```bash
python3 gpg_sign_manager.py --verify
```

### 查看日誌

```bash
cat gpg_sign_log.json | python3 -m json.tool
```

---

## 整合亮點

| 原文件夾結構 | 新整合結構 | 改進 |
| --- | --- | --- |
| bash shell腳本 | Python工具 | 跨平台·更易維護 |
| 單個簽署命令 | 管理工具 | 日誌追溯·批量操作 |
| 手動驗證 | 自動驗證 | 內建驗證功能 |
| 無日誌 | JSON日誌 | 完整審計追蹤 |

---

## DNA簽署

```
簽署者: UID9622 · 誠葛鑫
時間: 2026-06-08 18:57 CST
目的: 桌面CNSH_v2.0_SIGN融入主干·GPG簽署管理統一化
DNA:#龍芯⚡️2026-06-08-GPG-SIGN-MANAGER-INTEGRATION-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
確認: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
```

---

## 下一步

1. ✅ 複製文件到主干 → **完成**
2. ✅ 創建Python管理工具 → **完成**
3. ⏳ 執行 `python3 gpg_sign_manager.py --sign` 簽署所有文檔
4. ⏳ Git提交integration完成
5. ⏳ 刪除桌面原文件夾

---

天下無欺·龍魂永恆。🐉
