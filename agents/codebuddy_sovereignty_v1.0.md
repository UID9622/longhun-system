# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CodeBuddy 插件主权清单 v1.0

> **原则**：数据根留本地，代码不上交，插件不掌权。  
> **目标**：不被任何插件/平台掌握生态主权。  
> **DNA**：`#龍芯⚡️丙午·甲午·庚辰·壬午·䷑蛊-CODEBUDDY-PLUGIN-SOVEREIGNTY-LIST-v1.0`

---

## 一、主权红线（安装前必查）

任何插件满足以下任一条件，**直接拒装或卸载**：

1. **强制登录第三方账号**才能使用（微信、QQ、GitHub、Google 等）
2. **默认开启云端同步**，且无法彻底关闭
3. **上传代码、文件、对话、剪贴板到外部服务器**做 AI 分析
4. **闭源且不可审计**，来源不明的 `.vsix` 或 npx 包
5. **控制项目构建、部署、发布链路**形成单点锁定（如只能部署到自家云）
6. **收集遥测（telemetry）且无法关闭**

---

## 二、当前已装插件审查

### 🔴 建议移除/禁用

| 插件 | 风险点 |
|---|---|
| `zhukunpeng.claude-code-cn` | 可能将代码/对话发往 Claude 境外服务 |
| `freedyool.trae-cn-translator` | 翻译内容可能上传云端 |
| `CloudBase MCP` | 腾讯云锁定，代码/数据上传腾讯云 |
| `Tencent Cloud Code Analysis (TCA) MCP` | 代码分析上传腾讯，且含 token |
| `EdgeOne Pages MCP` | 部署链路锁定腾讯云 |
| `ssl-mcp-server` | 需腾讯云 Secret 密钥 |
| `Dnspod MCP Server` | 需腾讯云 Secret 密钥 |
| `腾讯文档 skill` | 文档内容上传腾讯云端 |
| `腾讯会议 skill` | 会议数据上传腾讯云端 |

### 🟢 可保留（本地运行，关闭云功能）

| 插件 | 注意事项 |
|---|---|
| `ms-python.python` / `debugpy` | 微软产品，关闭遥测，仅本地调试 |
| `detachhead.basedpyright` | 开源类型检查，本地运行 |
| `eamodio.gitlens` | 关闭云同步、关闭账户登录 |
| `ms-azuretools.vscode-docker` | 仅本地容器管理，不上传 |
| `llvm-vs-code-extensions.vscode-clangd` | 开源本地 C/C++ 支持 |
| `ms-vscode.cmake-tools` | 本地构建工具 |
| `oderwat.indent-rainbow` | 纯本地渲染 |
| `usernamehw.errorlens` | 纯本地显示 |
| `mechatroner.rainbow-csv` | 纯本地 CSV 高亮 |

### 🟡 观察使用

| 插件 | 风险 |
|---|---|
| `jeanp413.open-remote-ssh` | 远程连接本身中立，但需确保目标机器主权可控 |
| `formulahendry.code-runner` | 仅本地运行代码，安全 |
| `gbti.snapshots-for-ai` | 可能生成代码快照，确认不上传即可 |

---

## 三、推荐安装清单（按功能）

### 1. 代码语言支持（本地优先）

| 插件 | ID | 说明 |
|---|---|---|
| Python 语言支持 | `ms-python.python` | 基础调试，已装 |
| 更严格的类型检查 | `detachhead.basedpyright` | 已装，开源替代 pyright |
| C/C++ LSP | `llvm-vs-code-extensions.vscode-clangd` | 已装 |
| Bash 支持 | `mads-hartmann.bash-ide-v1` 或 `rogalmic.bash-debug` | 本地 shell 支持 |
| TOML/YAML/JSON | `tamasfe.even-better-toml` | 纯本地 |
| Markdown | `yzhang.markdown-all-in-one` | 纯本地，关闭上传 |
| CNSH 自定义高亮 | 自研 `.cnsh` 语法插件 | 不依赖市场 |

### 2. 版本控制（本地 Git）

| 插件 | ID | 说明 |
|---|---|---|
| GitLens | `eamodio.gitlens` | 已装，**必须关闭云同步和账户** |
| Git Graph | `mhutchie.git-graph` | 纯本地提交可视化 |
| Git History | `donjayamanne.githistory` | 纯本地历史查看 |

### 3. 搜索与导航（本地索引）

| 插件 | ID | 说明 |
|---|---|---|
| 本地文件搜索 | CodeBuddy 自带 |  suffice |
| 代码符号跳转 | 各 LSP 自带 |  suffice |
| TODO 高亮 | `gruntfuggly.todo-tree` | 纯本地 |

### 4. 安全与审计（不联网）

| 插件 | ID | 说明 |
|---|---|---|
| 密钥扫描 | `GitHub.vscode-codeql` 过重，不建议 | 改用本地脚本 |
| 敏感信息检查 | 自研 `~/longhun-system/tools/longhun_code_audit_runner.py` | 龍魂自带 |
| 代码审计 | `~/longhun-system/tools/longhun_code_audit_runner.py` | 龍魂自带 |

### 5. 运行与调试（本地进程）

| 插件 | ID | 说明 |
|---|---|---|
| Python 调试 | `ms-python.debugpy` | 已装 |
| Code Runner | `formulahendry.code-runner` | 已装，仅本地执行 |
| 任务运行 | CodeBuddy 自带 tasks.json | suffice |

### 6. UI 辅助（纯本地）

| 插件 | ID | 说明 |
|---|---|---|
| 缩进彩虹 | `oderwat.indent-rainbow` | 已装 |
| Error Lens | `usernamehw.errorlens` | 已装 |
| Rainbow CSV | `mechatroner.rainbow-csv` | 已装 |
| 中文字体优化 | 自研 CSS/配置 | 不装插件 |

### 7. 龍魂/CNSH 专用（自研，不上市场）

| 组件 | 路径 | 说明 |
|---|---|---|
| CNSH 语法高亮 | 自研 `.cnsh` 插件 | 本地安装 `.vsix` |
| 龍魂状态面板 | `http://127.0.0.1:9627/` | 浏览器打开 |
| LH 命令集成 | `~/longhun-system/bin/lh` | 终端命令 |
| DNA 追溯检查 | `~/longhun-system/tools/longhun_dna_align.py` | 本地运行 |

---

## 四、MCP 服务器主权建议

当前 `~/.codebuddy/mcp.json` 中配置的 6 个 MCP 全部依赖外部云，**建议全部禁用**，改用本地 MCP：

### 推荐本地 MCP

| MCP | 用途 | 来源 |
|---|---|---|
| `filesystem` | 本地文件读写 | 官方开源 |
| `sqlite` | 本地数据库查询 | 官方开源 |
| `fetch` | 受控网络请求 | 本地代理 |
| `longhun-neural-network` | 龍魂节点状态 | 自研 `:9627` |
| `longhun-memory-bootstrap` | 记忆归集 | 自研脚本 |

### 必须禁用/删除的 MCP

- `EdgeOne Pages MCP`
- `CloudBase MCP`
- `Tencent Cloud Code Analysis (TCA) MCP Server`
- `ssl-mcp-server`
- `Dnspod MCP Server`
- `Obsidian MCP Server`（除非 vault 纯本地且关闭同步）

---

## 五、配置加固命令

```bash
# 1. 关闭 CodeBuddy 遥测（如有）
# 在 settings.json 中添加：
# "telemetry.telemetryLevel": "off"

# 2. 禁用可疑 MCP
cp ~/.codebuddy/mcp.json ~/.codebuddy/mcp.json.bak.$(date +%Y%m%d)
# 编辑 mcp.json，将 cloud 相关 MCP 的 disabled 改为 true

# 3. 卸载高风险插件
# 手动在 CodeBuddy 扩展面板卸载：
# - zhukunpeng.claude-code-cn
# - freedyool.trae-cn-translator
# - 任何 Tencent Cloud / EdgeOne / CloudBase 相关插件

# 4. 验证网络流出
# 运行插件后检查是否有异常连接：
# lsof -i | grep codebuddy
```

---

## 六、最小可运行清单

如果只求「不卡、不被控」，最少装这几个：

1. `ms-python.python`
2. `detachhead.basedpyright`
3. `llvm-vs-code-extensions.vscode-clangd`（如需 C/C++）
4. `eamodio.gitlens`（关闭云同步）
5. `formulahendry.code-runner`
6. 自研 CNSH 语法插件
7. 龍魂 `:9627` 神经网络总控（浏览器访问）

---

## 七、主权检查口诀

> **能上本地不上云，能开源不闭源，能自研不市场，能禁用不授权。**

DNA: `#龍芯⚡️丙午·甲午·庚辰·壬午·䷑蛊-CODEBUDDY-PLUGIN-SOVEREIGNTY-LIST-v1.0`
