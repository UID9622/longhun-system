# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂跨平台同步专业知识库

DNA: #龍芯⚡️20260701015352331716-cross-platform-sync-overview-773C31F8

本目录汇总 iOS / 鸿蒙 / macOS / Linux 本地网络直连、端到端加密、冲突解决等专业知识，
对应可执行实现位于 `~/.kimi-code/skills/longhun-cross-platform/scripts/`。

## 核心原则

1. 数据根留中国，不经过外网。
2. 先加密再出应用：SM4-CBC + HMAC-SHA256。
3. 密钥不离设备：ECDH Curve25519 + HKDF-SHA256。
4. 本地网络直连：mDNS / WiFi Direct / BLE / TCP LAN。

## 关键命令

```bash
# 单机端到端演示
python3 ~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py demo

# mDNS 发现
python3 ~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py discover

# 生成/扫描二维码配对
python3 .../xsync_workflow.py pair-qr --text-out /tmp/server_pub.txt
python3 .../xsync_workflow.py pair-scan --input /tmp/server_pub.txt
```
