# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 国密 SM4-CBC 加密信封

**DNA**: #龍芯⚡️20260701015352332292-国密 SM4-CBC 加密信封-F0A83751
**分类**: 密码学 / 对称加密
**英文缩写**: SM4-CBC

## 定义

业务数据先 JSON 序列化，再使用 SM4-CBC 加密，附带随机 IV、HMAC-SHA256 完整性校验与 DNA 追溯码，组成加密信封后出应用。

## 触发场景

SM4、国密、CBC、加密信封、HMAC、完整性校验

## Python 示例

```python
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT
crypt = CryptSM4()
crypt.set_key(key, SM4_ENCRYPT)
cipher = crypt.crypt_cbc(iv, plaintext)
```

## 相关链接

- 龍魂跨平台同步工作流: `~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-cross-platform/SKILL.md`
