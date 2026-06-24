# 🐉 龍魂编年史

> 把 Claude 记忆档升级为龍魂系统自己的项目记忆宇宙。

**DNA**: `#龍芯⚡️2026-06-18-LONGHUN-CHRONICLE-FILE1-v1.0`

---

## 为什么要做这个

原本项目历史存在 `~/.claude/.../MEMORY.md`，属于 Claude，不属于系统。

现在我们把它变成：

- **项目自有**：在 `project-memory/` 目录，Git 版本控制。
- **可执行**：用 `龍魂编年史.py` 添加、查询、生成页面。
- **可 DNA 追溯**：每条里程碑都有唯一签名。
- **普通人能看**：自动生成 `index.md`，结构清晰。

---

## 快速使用

```bash
# 从 Claude 记忆档初始化关键里程碑
python3 project-memory/龍魂编年史.py seed

# 添加新里程碑
python3 project-memory/龍魂编年史.py add \
  --title "新功能上线" \
  --content "完成了某项重要功能。" \
  --category "工具发布"

# 生成/更新页面
python3 project-memory/龍魂编年史.py generate

# 查看规范索引
python3 project-memory/龍魂编年史.py specs
```

---

## 文件说明

- `Claude_MEMORY_ARCHIVE.md`：原始 Claude 记忆档归档
- `chronicle.db`：里程碑 SQLite 数据库
- `index.md`：自动生成的可读页面
- `龍魂编年史.py`：核心引擎
