# CNSH本地引擎 - 完全离线版

## 🔥 特点

- **纯标准库实现** - 不依赖任何外部Python包
- **完全离线运行** - 无需网络连接
- **易经八卦推理** - 基于传统文化的智能推理
- **MCP身份认证** - 本地化身份验证系统
- **双击启动** - 创建Mac应用程序，双击即可运行

## 🚀 快速开始

### 方法1：直接运行Python脚本

```bash
cd /Users/zuimeidedeyihan/CodeBuddy/20251207144453/MulanNotion
python3 cnsh_local_server.py
```

### 方法2：使用启动脚本

```bash
cd /Users/zuimeidedeyihan/CodeBuddy/20251207144453/MulanNotion
./start_cnsh.sh
```

### 方法3：创建Mac应用程序（推荐）

```bash
cd /Users/zuimeidedeyihan/CodeBuddy/20251207144453/MulanNotion
./create_app.sh

# 然后将CNSH本地引擎.app复制到Applications目录
# 从Launchpad或Finder双击启动
```

## 🔧 系统要求

- macOS 10.12 或更高版本
- Python 3.6 或更高版本（系统自带）

## 📱 使用流程

1. **启动系统** - 使用上述任一方法启动
2. **访问界面** - 浏览器打开显示的URL
3. **身份认证** - 在"身份认证"标签页点击"请求认证"
4. **扫描二维码** - 使用微信扫描生成的二维码
5. **输入密码** - 认证页面输入密码（默认：CNSH2025）
6. **易经推理** - 在"易经推理"标签页输入文本进行推理

## 🎯 功能详解

### 易经八卦推理

- 根据输入文本关键词匹配对应卦象
- 推荐合适的人格进行分析
- 引用相关文化片段
- 所有推理记录保存在本地审计日志

### MCP身份认证

- 生成认证令牌和二维码
- 设备授权管理（7天有效）
- 本地化认证状态存储
- 完全离线的认证流程

## 🔒 数据存储位置

- **认证配置**: `~/.codebuddy/mcp_config/`
- **认证日志**: `~/.codebuddy/mcp_config/auth.db`
- **设备列表**: `~/.codebuddy/mcp_config/devices.json`
- **审计日志**: `./audit.log`

## 📋 故障排除

### 问题：Python命令未找到

```bash
# 检查Python版本
python3 --version

# 如果未安装，安装Xcode命令行工具
xcode-select --install
```

### 问题：无法创建Mac应用

```bash
# 检查脚本权限
chmod +x create_app.sh

# 手动运行
./create_app.sh
```

### 问题：浏览器无法访问

```bash
# 检查服务器是否启动
ps aux | grep cnsh_local_server

# 检查端口是否被占用
lsof -i :8000
```

## 🛠️ 高级配置

### 修改认证密码

编辑 `cnsh_local_server.py` 文件中的 `AUTH_PASSWORD` 变量：

```python
# 找到这行
self.auth_password = "CNSH2025"

# 修改为您的密码
self.auth_password = "您的密码"
```

### 修改认证有效期

编辑 `cnsh_local_server.py` 文件中的设备有效期检查：

```python
# 找到这行
if datetime.datetime.now() - last_auth > datetime.timedelta(days=7):

# 修改为其他天数，如30天
if datetime.datetime.now() - last_auth > datetime.timedelta(days=30):
```

## 🌟 优势对比

| 特性 | 在线版本 | 离线版本 |
|------|---------|---------|
| 网络依赖 | 需要 | 无需 |
| 数据隐私 | 云端存储 | 仅本地 |
| 启动速度 | 依赖网络 | 即时启动 |
| 系统要求 | Docker/Pip | 仅Python |
| 离线使用 | 不支持 | 完全支持 |

## 📜 版本历史

- v1.0.0 - 初始版本
  - 纯Python标准库实现
  - 易经八卦推理引擎
  - MCP身份认证系统
  - Mac应用程序支持

## 📞 技术支持

如遇问题，请：

1. 查看终端输出信息
2. 检查audit.log文件内容
3. 确认Python3版本符合要求
4. 验证文件权限正确设置

---

**CNSH本地引擎** - 让传统文化与现代科技在您的设备上融合，完全离线，完全自主！

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:12
🧬 DNA追溯码: #CNSH-SIGNATURE-671cead0-20251218032412
🌐 签名人: 龍魂文化加密系统
💬 方言确认: 东北话确认：没毛病，内容真实可靠
⚡ 卦象防护: 蒙卦：山下出泉，君子以果行育德
📜 内容哈希: e2ec52c371199633
⚠️ 警告: 未经授权修改将触发DNA追溯系统
