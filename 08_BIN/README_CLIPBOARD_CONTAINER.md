**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
# 🐉 龍魂·剪贴板容器部署指南

DNA: `#龍芯⚡️丙午·丙申·辛酉·辰时·䷖剥-CLIPBOARD-DEPLOY-V1.0-P1`

## 架构

```
用户复制内容
    ↓
本地代理 (macOS/Windows)
    ├─ pbpaste/pbcopy 或 win32clipboard 读取
    ├─ SM4-CBC 加密（密钥由 token 派生）
    └─ WebSocket 发送到容器中心
    ↓
容器中心 (lh_clipboard_hub.py)
    ├─ 启动时调用 reconcile 补齐 Neo4j 缺失索引
    ├─ 校验 token / 限流
    ├─ SM4 解密
    ├─ 调用 lh_clipboard_vault.save() 落盘（自动去重）
    └─ 同步 Neo4j 索引
```

## 依赖

```bash
pip install websockets gmssl pyyaml pyperclip
```

macOS 已内置 `pbpaste`/`pbcopy`，无需额外依赖。  
Windows 推荐安装 `pywin32`，否则使用 `pyperclip` 兜底。

## 1. 启动容器中心

```bash
cd /Users/zuimeidedeyihan/longhun-system

# 本地调试（无 token 时仅允许本地连接）
python3 08_BIN/lh_clipboard_hub.py

# 生产：配置 token + TLS 证书（启用 wss://）
export LONGHUN_CLIPBOARD_TOKENS="#龍芯⚡️...,#龍芯⚡️..."
export LONGHUN_CLIPBOARD_CERT=/path/to/fullchain.pem
export LONGHUN_CLIPBOARD_KEY=/path/to/privkey.pem
python3 08_BIN/lh_clipboard_hub.py --host 0.0.0.0 --port 8765

# 或显式传入证书路径
python3 08_BIN/lh_clipboard_hub.py --cert /path/to/fullchain.pem --key /path/to/privkey.pem

# 明文调试（不推荐生产）
python3 08_BIN/lh_clipboard_hub.py --no-encrypt
```

## 2. 启动本地代理

### macOS

```bash
# 连接鲲鹏生产环境（wss://）
export LONGHUN_CLIPBOARD_TOKEN="#龍芯⚡️..."
export LONGHUN_CLIPBOARD_HUB="wss://uid9622.cn:8765"
python3 08_BIN/lh_clipboard_agent_mac.py --placeholder

# 本地调试（ws://）
python3 08_BIN/lh_clipboard_agent_mac.py --hub ws://127.0.0.1:8765

# 自签名证书测试
python3 08_BIN/lh_clipboard_agent_mac.py --hub wss://127.0.0.1:8765 --insecure
```

### Windows

```powershell
$env:LONGHUN_CLIPBOARD_TOKEN="#龍芯⚡️..."
$env:LONGHUN_CLIPBOARD_HUB="wss://uid9622.cn:8765"
python3 08_BIN\lh_clipboard_agent_win.py --placeholder
```

### 跨平台入口

```bash
python3 08_BIN/lh_clipboard_agent.py --hub wss://uid9622.cn:8765 --placeholder
```

## 3. 验证

```bash
# 查看容器统计
curl -s http://localhost:8444/api/cn-innovation-kg/stats

# 直接查询 vault
python3 05_ENGINES/lh_clipboard_vault.py list
```

## 4. 离线缓存队列

代理离线时，会把已加密的 payload 暂存到 `~/.longhun/cache/clipboard_queue.db`（SQLite，仅保存密文，不存明文）。恢复连接后自动批量补发，超过 3 次重试失败的条目会被丢弃。

启动时、每 30 秒、以及代理退出前都会尝试补发。

## 5. 生产部署

### Linux systemd

```bash
sudo cp 08_BIN/clipboard-agent.service /etc/systemd/system/lh-clipboard-hub.service
# 编辑 token 等环境变量
sudo systemctl daemon-reload
sudo systemctl enable lh-clipboard-hub
sudo systemctl start lh-clipboard-hub
```

### macOS launchd

```bash
mkdir -p ~/.longhun/logs
sed -e "s|%USER%|$USER|g" -e "s|%LONGHUN_CLIPBOARD_TOKEN%|$LONGHUN_CLIPBOARD_TOKEN|g" \
    08_BIN/com.longhun.clipboard-agent.plist > ~/Library/LaunchAgents/com.longhun.clipboard-agent.plist
launchctl load ~/Library/LaunchAgents/com.longhun.clipboard-agent.plist
launchctl start com.longhun.clipboard-agent
```

## 安全说明

- 生产环境必须配置 `LONGHUN_CLIPBOARD_TOKENS`。
- 未配置 token 时，hub 仅允许本地连接调试，不校验身份。
- 占位替换模式会先把原文加密上传，再替换本地剪贴板，避免输入法读取原文。
- 所有文件均带 DNA 追溯与 GPG 签名。
