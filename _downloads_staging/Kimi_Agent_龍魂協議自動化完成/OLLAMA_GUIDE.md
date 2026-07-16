# Ollama 安装与启动指南（龍魂系统集成版）

> **适用对象**：宝宝（P72） | **编制**：龍芯北辰·诸葛鑫（UID9622） | **用途**：本地 AI 模型部署与龍魂系统对接
>
> 本指南覆盖 Ollama 在 macOS 上的完整安装流程，以及与龍魂系统 v4.0 的集成配置。

---

## 一、Mac 安装步骤

### 前置要求

- **操作系统**：macOS 12 (Monterey) 或更高版本
- **内存**：建议 8GB+，运行 7B 模型需要至少 4GB 空闲内存
- **磁盘**：至少 5GB 可用空间（7B 模型约 4.7GB）
- **网络**：需联网下载模型

### 方式一：Homebrew 安装（推荐）

```bash
brew install ollama
```

**预期输出**：

```
==> Downloading https://ghcr.io/v2/homebrew/core/ollama/manifests/...
==> Pouring ollama--*.arm64_monterey.bottle.tar.gz
🍺  ollama was poured from a bottle! (45MB)
```

### 方式二：官方安装包

若 Homebrew 不可用，访问 [https://ollama.com/download](https://ollama.com/download) 下载 `.dmg` 安装包，双击按向导完成安装。

### 验证安装

```bash
ollama --version
```

**预期输出**：

```
ollama version 0.6.x
```

---

## 二、拉取模型

龍魂系统推荐使用 `qwen2.5:7b` 作为默认本地模型，中文理解能力强、体积适中。

### 拉取 Qwen2.5 7B 模型

```bash
ollama pull qwen2.5:7b
```

**说明**：
- 首次下载约 4.7GB，根据网速可能需要 5-30 分钟
- 模型下载后存储在 `~/.ollama/models/`
- 该命令可重复执行，会自动跳过已下载的部分（断点续传）

**预期输出**：

```
pulling manifest
pulling 26bd607a4f2e... 100% ▕██████████████████▏ 4.7 GB
pulling 9660c1e38a29... 100% ▕██████████████████▏ 1.4 KB
pulling fcc5a6bec1da... 100% ▕██████████████████▏ 7.7 KB
pulling a4dd1760e81e... 100% ▕██████████████████▏ 485 B
verifying sha256 digest
writing manifest
removing any unused layers
success
```

### （可选）拉取其他推荐模型

```bash
# 轻量级模型（Mac 内存紧张时选用）
ollama pull qwen2.5:1.8b

# 更强的代码能力
ollama pull qwen2.5-coder:7b

# 多模态（支持图片理解）
ollama pull llava:7b
```

---

## 三、启动服务

### 前台启动（调试用）

```bash
ollama serve
```

**预期输出**：

```
2025/06/09 10:00:00 routes.go:1234: Listening on 127.0.0.1:11434 (version 0.6.x)
```

保持终端窗口开启，按 `Ctrl+C` 停止服务。

### 后台启动（日常使用）

```bash
# macOS 安装后会自动注册为后台服务
brew services start ollama
```

**预期输出**：

```
==> Successfully started `ollama` (label: homebrew.mxcl.ollama)
```

### 检查服务状态

```bash
brew services list | grep ollama
```

**预期输出**：

```
ollama started user@localhost:11434 ...
```

### 停止服务

```bash
brew services stop ollama
```

---

## 四、验证测试

### 测试1：HTTP API 连通性

```bash
curl http://localhost:11434/api/tags
```

**预期输出**（已拉取模型时）：

```json
{
  "models": [
    {
      "name": "qwen2.5:7b",
      "model": "qwen2.5:7b",
      "size": 4683075294,
      "digest": "26bd607a4f2e...",
      "details": {
        "family": "qwen2",
        "parameter_size": "7.6B",
        "quantization_level": "Q4_K_M"
      }
    }
  ]
}
```

### 测试2：对话 API 测试

```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5:7b",
    "prompt": "你好，请用一句话介绍自己",
    "stream": false
  }'
```

**预期输出**：

```json
{
  "model": "qwen2.5:7b",
  "response": "你好！我是通义千问，一个由阿里云开发的人工智能助手。",
  "done": true
}
```

### 测试3：流式对话测试

```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5:7b",
    "prompt": "龍魂系统是什么",
    "stream": true
  }'
```

流式输出会逐字返回，以 `{"done":true}` 结束。

### 测试4：交互式对话

```bash
ollama run qwen2.5:7b
```

进入交互模式后可直接对话，输入 `/bye` 退出。

---

## 五、龍魂系统集成配置

将 Ollama 配置为龍魂系统 v4.0 的本地 AI 后端，供五大人格代理调用。

### 第1步：编辑龍魂配置文件

```bash
nano ~/.longhun/secrets.env
```

在文件末尾追加以下配置：

```env
# Ollama 本地模型配置
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b
OLLAMA_TIMEOUT=60
```

### 第2步：验证集成

```bash
python3 -c "
import os, json, urllib.request
from urllib.request import urlopen

# 读取配置
cfg = {}
with open(os.path.expanduser('~/.longhun/secrets.env')) as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            k, v = line.strip().split('=', 1)
            cfg[k] = v

# 测试连通
req = urllib.request.Request(
    f'{cfg[\"OLLAMA_URL\"]}/api/tags',
    headers={'Content-Type': 'application/json'}
)
resp = urlopen(req, timeout=10)
data = json.loads(resp.read())
models = [m['name'] for m in data.get('models', [])]
print(f'✅ Ollama 连接成功')
print(f'可用模型: {models}')
print(f'当前配置模型: {cfg[\"OLLAMA_MODEL\"]}')
if cfg['OLLAMA_MODEL'] in models:
    print('✅ 配置模型已就绪')
else:
    print('⚠️ 配置模型未下载，请执行: ollama pull ' + cfg['OLLAMA_MODEL'])
"
```

**预期输出**：

```
✅ Ollama 连接成功
可用模型: ['qwen2.5:7b']
当前配置模型: qwen2.5:7b
✅ 配置模型已就绪
```

### 第3步：重启同步服务加载配置

```bash
python3 longhun_sync.py --stop
python3 longhun_sync.py --all
```

### 人格代理调用说明

五大人格在需要 AI 推理时，自动通过以下接口调用本地 Ollama：

```
POST http://localhost:11434/api/generate
Content-Type: application/json

{
  "model": "qwen2.5:7b",
  "prompt": "<人格上下文>\n<任务描述>",
  "stream": false
}
```

**M56 训令提醒**：AI 模型优先走本地 Ollama，数据不出本机，确保龍魂体系信息安全。

---

## 六、开机自启动设置

配置 Ollama 在 macOS 开机时自动启动，确保龍魂系统随时可调用本地 AI。

### 方式一：Homebrew 服务（推荐）

如果之前使用了 `brew services start ollama`，则已自动设置为开机自启，无需额外操作。

验证：

```bash
brew services list | grep ollama
# 显示 started 即表示开机自启已启用
```

### 方式二：Launchd Plist 文件

如需手动配置，创建以下 plist 文件：

```bash
mkdir -p ~/Library/LaunchAgents
```

创建文件 `~/Library/LaunchAgents/com.ollama.ollama.plist`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- 服务标识 -->
    <key>Label</key>
    <string>com.ollama.ollama</string>

    <!-- 可执行程序路径 -->
    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/bin/ollama</string>
        <string>serve</string>
    </array>

    <!-- 工作目录 -->
    <key>WorkingDirectory</key>
    <string>/Users/YOUR_USERNAME</string>

    <!-- 环境变量 -->
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
        <key>HOME</key>
        <string>/Users/YOUR_USERNAME</string>
    </dict>

    <!-- 开机启动 + 崩溃自动重启 -->
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>

    <!-- 标准输出/错误日志 -->
    <key>StandardOutPath</key>
    <string>/Users/YOUR_USERNAME/.ollama/ollama.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/YOUR_USERNAME/.ollama/ollama.error.log</string>
</dict>
</plist>
```

**替换占位符**：将 `YOUR_USERNAME` 替换为你的 macOS 用户名。

### 加载 Plist 配置

```bash
# 加载 plist 文件
launchctl load ~/Library/LaunchAgents/com.ollama.ollama.plist

# 启动服务
launchctl start com.ollama.ollama

# 验证服务运行
launchctl list | grep ollama
```

**预期输出**：

```
-   0   com.ollama.ollama
```

第二列为 `0` 表示正常运行。

### 卸载自启动

如需取消开机自启：

```bash
launchctl stop com.ollama.ollama
launchctl unload ~/Library/LaunchAgents/com.ollama.ollama.plist
rm ~/Library/LaunchAgents/com.ollama.ollama.plist
```

### 日志查看

```bash
# 服务输出日志
tail -f ~/.ollama/ollama.log

# 错误日志
tail -f ~/.ollama/ollama.error.log
```

---

## 七、常用命令速查表

| 命令 | 说明 |
|------|------|
| `ollama --version` | 查看版本 |
| `ollama serve` | 前台启动服务 |
| `ollama pull qwen2.5:7b` | 下载模型 |
| `ollama run qwen2.5:7b` | 交互式对话 |
| `ollama list` | 列出已下载模型 |
| `ollama rm qwen2.5:7b` | 删除模型释放空间 |
| `ollama ps` | 查看正在运行的模型 |
| `ollama stop qwen2.5:7b` | 停止运行中的模型 |
| `brew services start ollama` | 后台启动（开机自启） |
| `brew services stop ollama` | 停止后台服务 |
| `brew services restart ollama` | 重启服务 |
| `brew services list` | 查看 Homebrew 服务状态 |

### API 端点速查

| 端点 | 说明 |
|------|------|
| `GET /api/tags` | 列出可用模型 |
| `POST /api/generate` | 生成文本（单次） |
| `POST /api/chat` | 多轮对话 |
| `POST /api/embeddings` | 获取文本向量 |
| `GET /api/ps` | 查看运行中的模型 |

---

## 八、故障排查

### 问题1：`ollama: command not found`

**解决方案**：

```bash
# 确认 Homebrew 路径已加载
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc

# 验证安装
which ollama
# 应输出 /opt/homebrew/bin/ollama
```

### 问题2：模型下载速度慢

**解决方案**：

```bash
# 设置镜像加速（可选）
export OLLAMA_HOST=0.0.0.0
# 或使用代理下载
HTTP_PROXY=socks5://127.0.0.1:7890 ollama pull qwen2.5:7b
```

### 问题3：`Error: listen tcp 127.0.0.1:11434: bind: address already in use`

**解决方案**：

```bash
# 查找已有进程
lsof -i :11434

# 停止已有进程
kill $(lsof -t -i :11434)

# 或重启服务
brew services restart ollama
```

### 问题4：内存不足导致模型加载失败

**解决方案**：

```bash
# 检查可用内存
vm_stat | head -5

# 关闭其他应用释放内存
# 或换用更小模型
ollama pull qwen2.5:1.8b
ollama run qwen2.5:1.8b
```

### 问题5：龍魂系统连接 Ollama 超时

**解决方案**：

```bash
# 检查 Ollama 是否运行
curl http://localhost:11434/api/tags

# 检查防火墙设置（确保 11434 端口允许本地访问）
sudo lsof -i :11434

# 检查 secrets.env 中的 URL 是否正确
grep OLLAMA_URL ~/.longhun/secrets.env
```

---

## 附录：模型占用参考

| 模型 | 大小 | 建议内存 | 适用场景 |
|------|:----:|:--------:|----------|
| `qwen2.5:1.8b` | ~1.1GB | 4GB | Mac 内存紧张时的轻量选择 |
| `qwen2.5:7b` | ~4.7GB | 8GB | **龍魂默认推荐**，平衡性能与资源 |
| `qwen2.5:14b` | ~9.0GB | 16GB | 需要更强推理能力时选用 |
| `qwen2.5:32b` | ~18GB | 32GB | 高端 Mac，最强推理 |

---

*本指南由龍芯北辰·诸葛鑫（UID9622）编制，确保宝宝在 P72 设备上可独立完成 Ollama 安装与龍魂系统集成。*

---
DNA: #龍芯⚡️2026-06-09-README-v4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅
