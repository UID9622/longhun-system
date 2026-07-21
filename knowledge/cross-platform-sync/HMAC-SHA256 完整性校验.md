# HMAC-SHA256 完整性校验

**DNA**: #龍芯⚡️20260701015352332351-HMAC-SHA256 完整性校验-FCEA5792
**分类**: 密码学 / 消息认证
**英文缩写**: HMAC

## 定义

在 SM4 密文上计算 HMAC-SHA256，防止中间人篡改。接收方使用 compare_digest 常量时间比较，避免时序攻击。

## 触发场景

HMAC、SHA256、完整性、防篡改、时序攻击

## Python 示例

```python
import hmac, hashlib
mac = hmac.new(key, iv + ciphertext, hashlib.sha256).digest()
if not hmac.compare_digest(mac, received_mac): raise ValueError('tampered')
```

## 相关链接

- 龍魂跨平台同步工作流: `~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-cross-platform/SKILL.md`
