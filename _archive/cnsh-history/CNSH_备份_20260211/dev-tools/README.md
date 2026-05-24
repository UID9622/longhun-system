# UID9622 开发工具包

**DNA追溯码：** #ZHUGEXIN⚡️2025-DEV-TOOLS-V1.0
**更新时间：** 2025-12-27
**版本：** v1.0.0

---

## 📦 包含内容

### 🔧 插件和配置
1. **插件推荐清单.md** - VS Code 插件推荐列表
2. **插件拆解指南.md** - 插件拆解和本地化指南
3. **install_vscode_extensions.sh** - VS Code 插件安装脚本
4. **custom-settings.json** - 自定义 VS Code 设置
5. **uid9622.code-snippets** - UID9622 代码片段

### 🛠️ 本地工具
6. **local_plugin_manager.py** - 本地插件管理器
7. **quick_start.sh** - 快速启动开发环境

### 📚 文档
8. **README.md** - 本文档

---

## 🚀 快速开始

### 1. 安装 VS Code 插件

#### 自动安装（推荐）
```bash
cd /Users/zuimeidedeyihan/LuckyCommandCenter/dev-tools
bash install_vscode_extensions.sh
```

#### 手动安装核心插件
```bash
# 检查 VS Code CLI
code --version

# 安装核心插件
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension dbaeumer.vscode-eslint
code --install-extension esbenp.prettier-vscode
code --install-extension eamodio.gitlens
code --install-extension PKief.material-icon-theme
```

### 2. 配置 VS Code

#### 复制自定义设置
```bash
# 复制设置到 .vscode 目录
cp custom-settings.json /Users/zuimeidedeyihan/LuckyCommandCenter/.vscode/settings.json
```

#### 复制代码片段
```bash
# 复制代码片段到 .vscode 目录
cp uid9622.code-snippets /Users/zuimeidedeyihan/LuckyCommandCenter/.vscode/uid9622.code-snippets
```

### 3. 启动开发环境

#### 启动所有服务
```bash
cd /Users/zuimeidedeyihan/LuckyCommandCenter/dev-tools
bash quick_start.sh --all
```

#### 交互式启动
```bash
bash quick_start.sh
```

### 4. 测试本地插件

```bash
cd /Users/zuimeidedeyihan/LuckyCommandCenter/dev-tools
python3 local_plugin_manager.py
```

---

## 📋 插件清单

### 必装插件（P0）

#### Python 开发
- **ms-python.python** - Python 官方扩展
- **ms-python.vscode-pylance** - Python 语言服务器

#### Web 开发
- **dbaeumer.vscode-eslint** - JavaScript 代码检查
- **esbenp.prettier-vscode** - 代码格式化

#### Git 工具
- **eamodio.gitlens** - Git 超级工具

#### 实用工具
- **PKief.material-icon-theme** - Material 文件图标
- **usernamehw.errorlens** - 内联错误显示

### 推荐插件（P1）

- **ms-python.black-formatter** - Python 格式化
- **ms-python.flake8** - Python 代码检查
- **yzhang.markdown-all-in-one** - Markdown 编辑器
- **timonwong.shellcheck** - Shell 脚本检查

### 可选插件（P2）

- **github.copilot** - AI 编程助手（需订阅）
- **Continue.continue** - 开源 AI 助手
- **Codeium.codeium** - 免费 AI 助手

---

## 🔧 本地插件

### DNA 标签生成器

```python
from dev-tools.local_plugin_manager import LocalDNATagPlugin

# 生成 DNA 标签
dna_tag = LocalDNATagPlugin.generate_tag("CODE", "FUNCTION", "P0")
print(dna_tag)  # #DNA-CODE-FUNCTION-P0-20251227-ABC12345-V1.0

# 生成确认码
confirm = LocalDNATagPlugin.generate_confirmation("PROJECT", "V1.0")
print(confirm)  # #ZHUGEXIN⚡️2025-PROJECT-V1.0
```

### Git Blame 工具

```python
from dev-tools.local_plugin_manager import LocalGitBlamePlugin

# 获取 blame 信息
blame = LocalGitBlamePlugin.get_blame("file.py", 10)
print(blame)

# 获取日志
logs = LocalGitBlamePlugin.get_log("file.py", limit=5)
print(logs)
```

### 代码分析器

```python
from dev-tools.local_plugin_manager import LocalCodeAnalyzerPlugin

# 分析 Python 文件
analysis = LocalCodeAnalyzerPlugin.analyze_python("file.py")
print(analysis)
```

### 审计日志记录器

```python
from dev-tools.local_plugin_manager import LocalAuditLoggerPlugin

logger = LocalAuditLoggerPlugin('logs/audit.log')

# 记录操作
logger.log('CREATE', 'User', 'user_001', {'name': 'Alice'})

# 获取历史
history = logger.get_history('user_001')
print(history)
```

---

## 🎨 自定义配置

### VS Code 设置

自定义设置包含：
- Python 配置（解释器、格式化、测试）
- JavaScript/TypeScript 配置（ESLint、Prettier）
- Git 和 GitLens 设置
- 编辑器通用设置
- UID9622 系统特定设置

### 代码片段

包含以下代码片段：
- `dna-tag` - DNA 标签生成
- `confirm-code` - 确认码生成
- `uid-header` - UID9622 文件头
- `class-dna` - Python 类定义（带 DNA）
- `func-audit` - Python 函数（带审计）
- `flask-route` - Flask 路由
- `shell-header` - Shell 脚本头
- `git-commit` - Git 提交信息
- `json-response` - JSON 响应
- `error-handler` - 错误处理
- `db-query` - 数据库查询
- `api-endpoint` - API 端点

---

## 🔍 插件拆解

### 支持的插件拆解

1. **GitLens** - Git 历史可视化
   - Git blame 信息获取
   - 提交历史浏览
   - 文件差异对比

2. **Pylance** - Python 语言服务器
   - 基于 AST 的代码分析
   - 类型推断
   - 智能补全

3. **ESLint** - JavaScript 代码检查
   - 语法错误检测
   - 代码风格检查
   - 自动修复

### 拆解方法

1. 分析插件核心功能
2. 提取关键代码
3. 本地化重构
4. 性能优化
5. 集成测试

详见 **插件拆解指南.md**

---

## 📊 快速参考

### 常用命令

```bash
# 安装插件
bash install_vscode_extensions.sh

# 启动开发环境
bash quick_start.sh --all

# 测试本地插件
python3 local_plugin_manager.py

# 查看 UID9622 日志
tail -f /Users/zuimeidedeyihan/LuckyCommandCenter/UID9622-LocalServer/logs/server.log
```

### 访问地址

- **UID9622 Dashboard**: http://127.0.0.1:9622
- **UID9622 API**: http://127.0.0.1:9622/api/
- **Ollama**: http://127.0.0.1:11434 (如果已安装)

---

## 🔒 安全和隐私

- ✅ 所有工具本地运行
- ✅ 无网络依赖（可选）
- ✅ 代码完全可控
- ✅ 审计日志完整

---

## 📝 开发规范

### 代码风格

- Python: Black (100 字符/行)
- JavaScript: Prettier
- Shell: ShellCheck

### 提交信息格式

```
type: description

DNA: #ZHUGEXIN⚡️YEAR-NAME-VERSION

- detail 1
- detail 2
```

### DNA 标签格式

```
#DNA-CATEGORY-SUBTYPE-PRIORITY-YYYYMMDD-IDENTIFIER-VERSION
```

---

## 🆘 故障排除

### VS Code CLI 未找到

```bash
# 在 VS Code 中
Cmd+Shift+P -> "Shell Command: Install 'code' command in PATH"
```

### 插件安装失败

```bash
# 检查网络连接
# 尝试手动安装
code --install-extension <extension-id>
```

### 服务器启动失败

```bash
# 检查端口占用
lsof -i :9622

# 查看日志
tail -f logs/server.log

# 停止服务器
bash quick_start.sh
# 选择 6) 停止服务器
```

---

## 📚 相关文档

- **UID9622-LocalServer/** - UID9622 服务器文档
- **插件推荐清单.md** - 完整插件推荐列表
- **插件拆解指南.md** - 插件拆解和本地化指南

---

## ✅ 检查清单

开发环境配置完成后，请检查：

- [ ] VS Code 已安装并配置
- [ ] 核心插件已安装
- [ ] 自定义设置已应用
- [ ] 代码片段已导入
- [ ] UID9622 服务器运行正常
- [ ] Dashboard 可访问
- [ ] 本地插件测试通过

---

## 🎯 下一步

1. ✅ 完成插件安装
2. ✅ 配置自定义设置
3. ✅ 启动开发环境
4. ✅ 测试本地插件
5. ✅ 开始开发

---

**版本：** v1.0.0
**状态：** Active
**DNA追溯码：** #ZHUGEXIN⚡️2025-DEV-TOOLS-V1.0
