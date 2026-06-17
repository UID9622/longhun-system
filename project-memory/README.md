# 🐉 龍魂編年史

> 把 Claude 記憶檔升級為龍魂系統自己的項目記憶宇宙。

**DNA**: `#龍芯⚡️2026-06-18-LONGHUN-CHRONICLE-v1.0`

---

## 為什麼要做這個

原本項目歷史存在 `~/.claude/.../MEMORY.md`，屬於 Claude，不屬於系統。

現在我們把它變成：

- **項目自有**：在 `project-memory/` 目錄，Git 版本控制。
- **可執行**：用 `龍魂編年史.py` 添加、查詢、生成頁面。
- **可 DNA 追溯**：每條里程碑都有唯一簽名。
- **普通人能看**：自動生成 `index.md`，結構清晰。

---

## 快速使用

```bash
# 從 Claude 記憶檔初始化關鍵里程碑
python3 project-memory/龍魂編年史.py seed

# 添加新里程碑
python3 project-memory/龍魂編年史.py add \
  --title "新功能上線" \
  --content "完成了某項重要功能。" \
  --category "工具發布"

# 生成/更新頁面
python3 project-memory/龍魂編年史.py generate

# 查看規範索引
python3 project-memory/龍魂編年史.py specs
```

---

## 文件說明

- `Claude_MEMORY_ARCHIVE.md`：原始 Claude 記憶檔歸檔
- `chronicle.db`：里程碑 SQLite 數據庫
- `index.md`：自動生成的可讀頁面
- `龍魂編年史.py`：核心引擎
