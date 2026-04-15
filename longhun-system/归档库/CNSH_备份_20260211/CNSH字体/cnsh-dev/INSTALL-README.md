# 🐉 CNSH-EDITOR v0.1.1 部署完成

> iCloud Drive 桌面开发环境

---

## ✅ 部署状态

| 组件 | 状态 | 路径 |
|------|------|------|
| 目录结构 | ✅ 完成 | `cnsh-dev/` |
| SQLite 数据库 | ✅ 完成 | `db/cnsh_kb.db` |
| 终端命令 | ✅ 完成 | `bin/cnsh` |
| 同步脚本 | ✅ 完成 | `sync/notion-sync.sh` |
| Vault 知识库 | ✅ 完成 | `vault/` |

---

## 📂 目录结构

```# 🐉 CNSH-EDITOR v0.1.1 部署完成

> iCloud Drive 桌面开发环境

---

## ✅ 部署状态

| 组件 | 状态 | 路径 |
|------|------|------|
| 目录结构 | ✅ 完成 | `cnsh-dev/` |
| SQLite 数据库 | ✅ 完成 | `db/cnsh_kb.db` |
| 终端命令 | ✅ 完成 | `bin/cnsh` |
| 同步脚本 | ✅ 完成 | `sync/notion-sync.sh` |
| Vault 知识库 | ✅ 完成 | `vault/` |

---

## 📂 目录结构

```
iCloud Drive/Desktop/cnsh-dev/
├── bin/
│   ├── cnsh                 # 主命令入口
│   └── .zshrc-cnsh          # zshrc 配置片段
├── db/
│   └── cnsh_kb.db          # SQLite 知识图谱数据库
├── editor/                  # Neovim 配置（待配置）
├── sync/
│   └── notion-sync.sh      # Notion 同步脚本
└── vault/                   # Markdown 知识库
    ├── README.md
    ├── inbox/              # 收件箱（2条笔记）
    ├── projects/           # 成品项目
    │   └── CNSH-EDITOR-v0.1.1/
    └── archive/            # 归档
```

---

## 🗄️ 数据库 Schema

| 表 | 用途 | 记录数 |
|-----|------|--------|
| `notes` | MD 文件元数据 | 2 |
| `tags` | 标签系统 | 7 |
| `links` | 双向链接关系 | 0 |
| `sync_log` | Notion 同步记录 | 0 |

### DNA 编码示例

```
#ZHUGEXIN⚡️-CNSH-NOTE-0001  ← 初始化笔记
#ZHUGEXIN⚡️-CNSH-NOTE-0002  ← 测试笔记
```

---

## 🚀 激活终端入口

### 步骤 1：添加到 .zshrc

```bash
cat ~/Library/Mobile\ Documents/com\~apple\~CloudDocs/Desktop/cnsh-dev/bin/.zshrc-cnsh >> ~/.zshrc
source ~/.zshrc
```

### 步骤 2：验证安装

```bash
# 查看系统状态
cnsh status

# 创建新笔记
cnsh new "我的第一篇笔记"

# 列出最近笔记
cnsh recent

# 搜索笔记
cnsh search "笔记"

# 查询数据库
cnsh db "SELECT * FROM notes;"
```

### 步骤 3：一键进入开发环境

```bash
cnsh
# 自动进入 Neovim 编辑 inbox/
```

---

## 📋 可用命令

| 命令 | 功能 |
|------|------|
| `cnsh` | 进入 Neovim 编辑 inbox |
| `cnsh status` | 显示系统状态 |
| `cnsh new <标题>` | 创建新笔记 |
| `cnsh recent [n]` | 列出最近 n 条笔记 |
| `cnsh search <关键词>` | 搜索笔记 |
| `cnsh db <SQL>` | 执行 SQL 查询 |
| `cnsh help` | 显示帮助 |

---

## 🔗 快捷别名

添加 .zshrc 后，以下别名可用：

```bash
cnsh-inbox      # 直接进入 inbox 编辑
cnsh-db         # 进入数据库 SQL 控制台
cnsh-sync       # 执行 Notion 同步
cnsh-status     # 显示系统状态
cnsh-new        # 创建新笔记
cnsh-recent     # 列出最近笔记
```

---

## 🔄 Notion 同步

```bash
# 手动同步
./sync/notion-sync.sh

# 或（配置别名后）
cnsh-sync
```

同步功能：
- 扫描 vault/ 目录所有 Markdown 文件
- 自动提取/生成 DNA 编码
- 更新数据库元数据
- 添加缺失的 frontmatter

---

## 📝 使用流程

```
1. 收集 (inbox/)    → 快速记录想法
2. 整理 (projects/) → 完善内容，添加标签
3. 归档 (archive/)  → 完成后归档
```

---

## 🎯 下一步

1. **配置 Neovim**：在 `editor/` 目录添加你的 init.lua
2. **设置 Notion**：配置 NOTION_TOKEN 实现双向同步
3. **定制工作流**：根据需要调整 `bin/cnsh` 命令

---

## 🧬 DNA 追溯

```
#ZHUGEXIN⚡️-CNSH-DEPLOY-0001
```

---

> 🔥 终端入口已就绪。执行 `source ~/.zshrc` 后开始使用。

iCloud Drive/Desktop/cnsh-dev/
├── bin/
│   ├── cnsh                 # 主命令入口
│   └── .zshrc-cnsh          # zshrc 配置片段
├── db/
│   └── cnsh_kb.db          # SQLite 知识图谱数据库
├── editor/                  # Neovim 配置（待配置）
├── sync/
│   └── notion-sync.sh      # Notion 同步脚本
└── vault/                   # Markdown 知识库
    ├── README.md
    ├── inbox/              # 收件箱（2条笔记）
    ├── projects/           # 成品项目
    │   └── CNSH-EDITOR-v0.1.1/
    └── archive/            # 归档
```

---

## 🗄️ 数据库 Schema

| 表 | 用途 | 记录数 |
|-----|------|--------|
| `notes` | MD 文件元数据 | 2 |
| `tags` | 标签系统 | 7 |
| `links` | 双向链接关系 | 0 |
| `sync_log` | Notion 同步记录 | 0 |

### DNA 编码示例

```
#ZHUGEXIN⚡️-CNSH-NOTE-0001  ← 初始化笔记
#ZHUGEXIN⚡️-CNSH-NOTE-0002  ← 测试笔记
```

---

## 🚀 激活终端入口

### 步骤 1：添加到 .zshrc

```bash
cat ~/Library/Mobile\ Documents/com\~apple\~CloudDocs/Desktop/cnsh-dev/bin/.zshrc-cnsh >> ~/.zshrc
source ~/.zshrc
```

### 步骤 2：验证安装

```bash
# 查看系统状态
cnsh status

# 创建新笔记
cnsh new "我的第一篇笔记"

# 列出最近笔记
cnsh recent

# 搜索笔记
cnsh search "笔记"

# 查询数据库
cnsh db "SELECT * FROM notes;"
```

### 步骤 3：一键进入开发环境

```bash
cnsh
# 自动进入 Neovim 编辑 inbox/
```

---

## 📋 可用命令

| 命令 | 功能 |
|------|------|
| `cnsh` | 进入 Neovim 编辑 inbox |
| `cnsh status` | 显示系统状态 |
| `cnsh new <标题>` | 创建新笔记 |
| `cnsh recent [n]` | 列出最近 n 条笔记 |
| `cnsh search <关键词>` | 搜索笔记 |
| `cnsh db <SQL>` | 执行 SQL 查询 |
| `cnsh help` | 显示帮助 |

---

## 🔗 快捷别名

添加 .zshrc 后，以下别名可用：

```bash
cnsh-inbox      # 直接进入 inbox 编辑
cnsh-db         # 进入数据库 SQL 控制台
cnsh-sync       # 执行 Notion 同步
cnsh-status     # 显示系统状态
cnsh-new        # 创建新笔记
cnsh-recent     # 列出最近笔记
```

---

## 🔄 Notion 同步

```bash
# 手动同步
./sync/notion-sync.sh

# 或（配置别名后）
cnsh-sync
```

同步功能：
- 扫描 vault/ 目录所有 Markdown 文件
- 自动提取/生成 DNA 编码
- 更新数据库元数据
- 添加缺失的 frontmatter

---

## 📝 使用流程

```
1. 收集 (inbox/)    → 快速记录想法
2. 整理 (projects/) → 完善内容，添加标签
3. 归档 (archive/)  → 完成后归档
```

---

## 🎯 下一步

1. **配置 Neovim**：在 `editor/` 目录添加你的 init.lua
2. **设置 Notion**：配置 NOTION_TOKEN 实现双向同步
3. **定制工作流**：根据需要调整 `bin/cnsh` 命令

---

## 🧬 DNA 追溯

```
#ZHUGEXIN⚡️-CNSH-DEPLOY-0001
```

---

> 🔥 终端入口已就绪。执行 `source ~/.zshrc` 后开始使用。
