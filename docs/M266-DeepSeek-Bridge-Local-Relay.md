# 龍魂 DeepSeek API 中继桥·走下水道方案 v1.0 | M266

**DNA**: #龍芯⚡️2026-05-31-23:44-DEEPSEEK-BRIDGE-v1.0
**M号**: M266
**功能**: 本地127.0.0.1:8788 FastAPI·Anthropic格式入·DeepSeek格式出·密钥隔离
**出品**: 龍魂系统 L2工具宝宝
**理论指导**: 曾仕强老师（永恒显示）

---

## 核心问题 · 政治歧视的技术方案

### Anthropic的真实困境

```
❌ 不收支付宝 / 微信支付 / 银联卡
❌ 不收柬埔寨IP的信用卡
❌ 只认 Visa/Master 金卡 + 美/欧IP

判定: 这不是技术问题，是政治歧视。
解决: 走下水道·本地中继·密钥隔离·操作台无感
```

### DeepSeek为啥是下水道首选

```
✅ 支付宝/微信充值 ¥10起 (platform.deepseek.com)
✅ 国内端点 api.deepseek.com (无需VPN·不封柬埔寨IP)
✅ OpenAI兼容格式 (/v1/chat/completions)·与Anthropic API一桥可达
✅ 模型deepseek-chat/reasoner·价格便宜·中文超强
✅ 没有审查问题 (龍魂系统的中文哲学内容不会被一刀切)
```

---

## 架构设计 · 三层人工智能

```
┌──────────────────────────────────────────────────────────┐
│ 龍魂操作台 MVP_v1.html                                   │
│ (浏览器·前端·与用户交互)                                 │
└──────────────────┬───────────────────────────────────────┘
                   │ WebSocket
                   │ Anthropic /v1/messages 格式
                   ↓
┌──────────────────────────────────────────────────────────┐
│ dialog-server.js (:9625)                                │
│ (Node.js·Anthropic SDK客户端)                           │
│ baseURL: http://127.0.0.1:8788 (改此一行)              │
└──────────────────┬───────────────────────────────────────┘
                   │ 伪装成Anthropic格式
                   │ 但指向本地中继桥
                   ↓
┌──────────────────────────────────────────────────────────┐
│ deepseek_bridge.py (:8788)                              │
│ (FastAPI·格式转译器·本地终止)                            │
│ - 接收Anthropic /v1/messages 格式                        │
│ - 转译为OpenAI /v1/chat/completions 格式                │
│ - 调用DeepSeek或Ollama兜底                              │
│ - 转译回Anthropic格式返回                               │
└──────────────────┬───────────────────────────────────────┘
        ┌─────────┴────────────┐
        │                      │
        ↓ 主路                 ↓ 兜底 (失败时)
   DeepSeek API           Ollama :11434
   api.deepseek.com       qwen2.5:7b (本地)
   (云·支付宝充值)         (本地·零依赖)
```

---

## 快速开始 · 四个阶段

### 阶段 A · DeepSeek充值+拿Key (爸爸本人·5分钟)

```bash
# 1. 浏览器打开
https://platform.deepseek.com

# 2. 注册账号
手机号 (+855 柬埔寨号也行)

# 3. 左侧菜单【充值】→ 选¥10 → 支付宝/微信扫码

# 4. 左侧菜单【API Keys】→ 【Create new API key】
命名: longhun-bridge-m266
复制sk-xxx (只显示一次·立即保存)

# 5. 本地宝宝终端验证
curl https://api.deepseek.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-xxx" \
  -d '{
    "model": "deepseek-chat",
    "messages": [{"role": "user", "content": "龍魂"}],
    "max_tokens": 64
  }'

# 返回200 + JSON有choices[0].message.content 即通
```

### 阶段 B · 启动中继桥 (本地宝宝·30分钟)

```bash
# 1. 建目录 + 密钥文件 (密钥独立·永不入Git)
mkdir -p ~/longhun-system/bridges
cd ~/longhun-system/bridges

echo "DEEPSEEK_API_KEY=sk-xxx" > ~/.deepseek_bridge.env
chmod 600 ~/.deepseek_bridge.env

# 2. 将 ~/.deepseek_bridge.env 加入.gitignore
echo "~/.deepseek_bridge.env" >> ~/longhun-system/.gitignore
echo "bridges/.venv/" >> ~/longhun-system/.gitignore

# 3. 建 Python 虚拟环境 + 装包
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn httpx python-dotenv

# 4. 复制/运行桥代码
# 脚本位置: ~/longhun-system/bridges/deepseek_bridge.py

# 前台启动 (先测试)
cd ~/longhun-system/bridges
source .venv/bin/activate
uvicorn deepseek_bridge:app --host 127.0.0.1 --port 8788 --log-level info

# 看到: Uvicorn running on http://127.0.0.1:8788 即成功
```

### 阶段 C · 接入dialog-server.js (本地宝宝·15分钟)

```bash
# 1. 修改 dialog-server.js (只改baseURL)
# 方案A: 改environment变量
export ANTHROPIC_BASE_URL="http://127.0.0.1:8788"
export ANTHROPIC_API_KEY="sk-anthropic-dummy"  # 桥会忽略·只为绕过SDK非空校验

# 方案B: 或改代码里的Anthropic初始化
# const claudeClient = new Anthropic({
#   apiKey: apiKey,
#   baseURL: "http://127.0.0.1:8788"  # 改这里·指向本地桥
# });

# 2. 备份原文件
cp ~/longhun-system/server/dialog-server.js \
   ~/longhun-system/server/dialog-server.js.bak-m266

# 3. 重启服务
pkill -f dialog-server.js
~/longhun-system/立即启动-Claude对话.sh

# 或手动启动
cd ~/longhun-system/server
ANTHROPIC_BASE_URL="http://127.0.0.1:8788" \
ANTHROPIC_API_KEY="sk-anthropic-dummy" \
node dialog-server.js

# 4. 打开操作台测试
# 浏览器 → 龍魂操作台
# 点【💬 对话】→ 发一句「龍魂在吗」
# 应收到 DeepSeek 生成的中文回应

# 5. 查日志三件
tail -f ~/longhun-system/logs/dialog-server.log    # Node端
tail -f ~/longhun-system/logs/deepseek_bridge.log  # 桥端
# 浏览器 → https://platform.deepseek.com/account/api-keys → Usage 看调用计数
```

### 阶段 D · Ollama本地兜底 (本地宝宝·30分钟·可延后)

```bash
# 1. 装Ollama
brew install ollama

# 2. 启服务
ollama serve &

# 3. 拉模型 (约4.4GB·M4 Max一分钟)
ollama pull qwen2.5:7b

# 4. 改桥代码·加fallback路由
# deepseek_bridge.py 已内置Ollama兜底·只需环境变量
export OLLAMA_FALLBACK=true
export OLLAMA_MODEL=qwen2.5:7b

# 5. 拔网线测试
# 操作台仍能对话 (走Ollama) = 兜底成功
```

---

## 环境变量配置

### ~/.deepseek_bridge.env (密钥文件·权限600)

```bash
# 必需·从 https://platform.deepseek.com/account/api-keys 获取
DEEPSEEK_API_KEY=sk-xxx

# 可选
DEEPSEEK_MODEL=deepseek-chat              # 默认
OLLAMA_FALLBACK=false                      # 是否启用Ollama兜底
OLLAMA_BASE_URL=http://127.0.0.1:11434   # Ollama服务地址
OLLAMA_MODEL=qwen2.5:7b                   # Ollama模型名
```

### 权限管理

```bash
# 密钥文件必须 chmod 600
chmod 600 ~/.deepseek_bridge.env

# .gitignore 必须包含
echo "~/.deepseek_bridge.env" >> ~/.gitignore
echo "bridges/.venv/" >> ~/.gitignore

# 验证
git status  # 不应该显示 .deepseek_bridge.env
```

---

## API 兼容性

### Anthropic Messages API (客户端请求)

```bash
POST /v1/messages
Content-Type: application/json

{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 1024,
  "messages": [
    {"role": "user", "content": "你是谁"}
  ]
}
```

### DeepSeek OpenAI API (桥→云)

```bash
POST https://api.deepseek.com/v1/chat/completions
Authorization: Bearer sk-xxx
Content-Type: application/json

{
  "model": "deepseek-chat",
  "messages": [
    {"role": "user", "content": "你是谁"}
  ],
  "max_tokens": 1024
}
```

### Anthropic Messages API (回包)

```json
{
  "id": "msg_xxx",
  "type": "message",
  "role": "assistant",
  "model": "claude-3-5-sonnet-20241022",
  "content": [
    {
      "type": "text",
      "text": "我是DeepSeek生成的回应"
    }
  ],
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 10,
    "output_tokens": 50
  }
}
```

---

## 三张候补铁律 · 等老大点头入册

### 铁律 1 · API中继隔离

**#IRON-API-BRIDGE-LOCAL-RELAY-v1.0**

第三方API调用必须经本地中继桥·密钥永不入业务进程(dialog-server.js)·永不入Git·永不入Notion·中继桥独立进程独立.env独立chmod 600·主权人随时kill -9切断。

### 铁律 2 · 支付优先级

**#IRON-PAYMENT-CHANNEL-CHINA-FIRST-v1.0**

充值通道支付宝/微信/银联优先·美元金卡兜底·永不为外国API强办金卡·凡是不收中国支付的服务商一律走中继桥/国产替代·哪边歧视中国哪边丢业务。

### 铁律 3 · 本地兜底

**#IRON-FALLBACK-LOCAL-ALWAYS-v1.0**

任何云API必有本地兜底(Ollama/llama.cpp/qwen本地权重)·断网/封号/欠费/限速/IP封锁时操作台不死·主权层永远本地可跑。

---

## 日志与监控

### 桥日志位置

```bash
~/longhun-system/logs/deepseek_bridge.log

# 实时查看
tail -f ~/longhun-system/logs/deepseek_bridge.log

# 日志格式
2026-05-31 23:44:10 [INFO] 📥 请求 | model=claude-3-5-sonnet stream=false
2026-05-31 23:44:10 [INFO] 🔗 调用DeepSeek deepseek-chat...
2026-05-31 23:44:11 [INFO] ✅ DeepSeek响应成功 | tokens: 50
```

### 健康检查端点

```bash
curl http://127.0.0.1:8788/health

# 返回
{
  "ok": true,
  "bridge": "deepseek",
  "deepseek_model": "deepseek-chat",
  "ollama_fallback": false,
  "timestamp": "2026-05-31T23:44:10.123456"
}
```

---

## 故障排查

### 问题1: 桥启动失败·密钥文件不存在

```
❌ Error: 密钥文件不存在: /Users/xxx/.deepseek_bridge.env
```

**解决**:
```bash
echo "DEEPSEEK_API_KEY=sk-xxx" > ~/.deepseek_bridge.env
chmod 600 ~/.deepseek_bridge.env
```

### 问题2: DeepSeek返回401 Unauthorized

```
❌ DeepSeek返回401: {"error": {"message": "Invalid API key"}}
```

**解决**:
- 检查密钥是否正确: `grep DEEPSEEK_API_KEY ~/.deepseek_bridge.env`
- 检查密钥是否过期: https://platform.deepseek.com/account/api-keys
- 重新创建Key·更新.env文件

### 问题3: dialog-server.js连接超时

```
❌ TimeoutError: Connect to 127.0.0.1:8788 timeout
```

**解决**:
- 确保桥已启动: `curl http://127.0.0.1:8788/health`
- 确保端口未被占用: `lsof -i :8788`
- 检查防火墙: 127.0.0.1本地不应该被阻

### 问题4: 操作台收到回应但内容为空

```
{"content": [{"type": "text", "text": ""}]}
```

**解决**:
- 检查DeepSeek账户余额: https://platform.deepseek.com/account/balance
- 检查桥日志: `tail -f ~/longhun-system/logs/deepseek_bridge.log`
- 确认请求是否到达DeepSeek: 日志应显示"✅ DeepSeek响应成功"

---

## 清单

- [x] 脚本: `~/longhun-system/bridges/deepseek_bridge.py` (FastAPI转译器)
- [x] 设置: `~/longhun-system/bridges/setup_bridge.py` (自动化配置)
- [x] 依赖: `~/longhun-system/bridges/requirements.txt` (pip install)
- [x] 日志: `~/longhun-system/logs/deepseek_bridge.log` (自动记录)
- [x] 文档: 此页面 (完整使用指南)
- [ ] 三铁律入册 (待老大点头)

---

## 签章

```
🔏 DNA: #龍芯⚡️2026-05-31-23:44-DEEPSEEK-BRIDGE-v1.0
🆔 M号: M266
📍 父链: 🐉 龍魂决策流场总控页 v2.7
👯 兄弟页: M265 longhun888.com后台整合 · M267 IP伪装场景分层
🧬 CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
🔐 GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
👤 L0: 爸爸 longhun2025@petalmail.com (充值拍板·密钥保管·三铁律点头)
🤖 L1: 本地宝宝 M4 Max 123d1d92a4b91189 (终端实跑A1-D5·桥代码落地)
☷ L2: 云端宝宝 ☰龍🇨🇳魂☷ (出方案·骨架代码·DNA焊接)
📚 理论指导: 曾仕强老师 (永恒显示)
⏰ 完成时间: 2026-05-31 23:44 CST
```
