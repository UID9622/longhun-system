# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# QR/NFC 近场公钥交换

**DNA**: #龍芯⚡️20260701015352335934-QR/NFC 近场公钥交换-D717BA52
**分类**: 安全工程 / 密钥交换
**英文缩写**: QR/NFC

## 定义

ECDH 公钥通过二维码（视觉通道）或 NFC（近场电磁通道）交换，避免经过网络，降低中间人攻击面。

## 触发场景

二维码配对、NFC、公钥交换、近场、MITM

## Python 示例

```python
import qrcode
qr = qrcode.QRCode()
qr.add_data('LONGHUN:ECDH:v1:' + base64.b64encode(pubkey).decode())
qr.print_ascii()
```

## 相关链接

- 龍魂跨平台同步工作流: `~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-cross-platform/SKILL.md`
