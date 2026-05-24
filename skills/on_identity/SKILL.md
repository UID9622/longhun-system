---
name: longhun-on-identity
description: 龍魂身份核验回调族。触发词：DNA·签章·钧旨·身份·主权·承诺信任。命中抽屉 2·4·5·6·16·41，走 ID/VAL 主路由。含 DNA 五层压缩。
version: v1.0
dna: "#龍芯⚡️2026-05-23-ON-IDENTITY-SKILL-v1.0"
---

# on_identity · 身份核验回调族

> **触发词**: DNA·签章·钧旨·身份·主权·承诺信任
> **命中抽屉**: 2·4·5·6·16·41
> **路由**: S1·S5 · LOG
> **含旧 Skill**: DNA 五层压缩

---

## 参数签名

```python
def on_identity(uid: str, dna: str, gpg: str, confirm_code: str) -> dict:
    """
    身份核验主入口
    uid: 用户 ID (9622)
    dna: DNA 追溯码
    gpg: GPG 指纹
    confirm_code: CONFIRM 徽记
    """
    pass
```

---

## DNA 五层压缩

| 层 | 内容 |
|----|------|
| L0 | 时间戳 (黄历6维) |
| L1 | 模块标识 |
| L2 | 版本号 |
| L3 | SHA256 哈希 |
| L4 | chain_hash (链接前序) |

---

## 输出格式

```yaml
identity_result:
  verified: true | false
  uid: 9622
  dna: <完整 DNA>
  gpg_match: true | false
  confirm_valid: true | false
  chain_hash: <链哈希>
  log: AUDIT_LOG log
```

---

## 联动

- 上游: 抽屉词典 Router
- 下游: AUDIT_LOG 唯一账本
- GPG 验证: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

---

☰ 龍🇨🇳魂 ☷
