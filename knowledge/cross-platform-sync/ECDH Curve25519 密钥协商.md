# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ECDH Curve25519 密钥协商

**DNA**: #龍芯⚡️20260701015352332163-ECDH Curve25519 密钥协商-181B14B7
**分类**: 密码学 / 密钥交换
**英文缩写**: ECDH X25519

## 定义

双方各自生成临时 X25519 密钥对，仅交换公钥即可计算相同共享密钥。私钥永不离设备，每次会话换新密钥对可实现前向安全。

## 触发场景

ECDH、Curve25519、密钥协商、前向安全、公钥交换

## Python 示例

```python
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
priv = X25519PrivateKey.generate()
pub = priv.public_key()
shared = priv.exchange(peer_pub_key)
```

## 相关链接

- 龍魂跨平台同步工作流: `~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-cross-platform/SKILL.md`
