# HKDF-SHA256 密钥派生

**DNA**: #龍芯⚡️20260701015352332234-HKDF-SHA256 密钥派生-C25E9C03
**分类**: 密码学 / 密钥派生
**英文缩写**: HKDF

## 定义

从 ECDH 共享密钥派生固定长度会话密钥。龍魂默认派生 16 字节 SM4-128 密钥，盐值需两端一致。

## 触发场景

HKDF、SHA256、密钥派生、SM4 会话密钥

## Python 示例

```python
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
hkdf = HKDF(algorithm=hashes.SHA256(), length=16, salt=b'longhun-salt', info=b'session')
sm4_key = hkdf.derive(shared_secret)
```

## 相关链接

- 龍魂跨平台同步工作流: `~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-cross-platform/SKILL.md`
