# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 局域网 TCP 兜底通道

**DNA**: #龍芯⚡️20260701015352332037-局域网 TCP 兜底通道-F0B02AEC
**分类**: 网络协议 / 本地直连
**英文缩写**: TCP LAN

## 定义

当 WiFi Direct / BLE 不可用时，通过同 WiFi 下的标准 socket TCP 直连。数据带 4 字节长度前缀，便于流式解析。

## 触发场景

TCP LAN、局域网、socket、兜底通道

## Python 示例

```python
import struct, socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.1.x', 9622))
msg = b'hello'
sock.sendall(struct.pack('>I', len(msg)) + msg)
```

## 相关链接

- 龍魂跨平台同步工作流: `~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-cross-platform/SKILL.md`
