# 🔐 声纹DNA锚定链

> 声纹特征 → SHA256 哈希链 → 数字人身份固化

---

## 目标

把声纹、文字、特征数据打包成一条 DNA 哈希链，固化数字人身份。只认系统内部锚定，防伪造、防冒充。

## 文件结构

| 模块 | 职责 |
|:---|:---|
| `voice_anchor.py` | 声纹录入、特征提取、哈希指纹、DNA 链生成 |
| `crypto.py` | Fernet + HMAC-SHA256 本地加密 |
| `register.py` | 用户注册入口 |
| `digital_persona.py` | 数字人身份固化、调用前验证 |
| `verify_anchor.py` | ID + 声纹比对、审计日志 |
| `backup.py` | 321 备份策略 |

## 注册

```bash
lh voice register <user_id> "验证文本"
```

## 验证

```bash
lh voice verify <user_id> <audio_file>
```

## 开放API

```python
from longhun.voice import VoiceDNA

vdna = VoiceDNA()

# 注册声纹
result = vdna.register(
    user_id="UID9622",
    text="龍魂系统启动",
    audio_file="enroll.wav"
)
# → {dna: "#龍芯⚡️...", fingerprint: "sha256:..."}

# 验证身份
result = vdna.verify(
    user_id="UID9622",
    audio_file="verify.wav"
)
# → {match: True, confidence: 0.97}

# 导出
vdna.export(user_id="UID9622", output="backup.enc")
```

## 安全

- 🔒 Fernet 本地加密 — 密钥不出主机
- 📊 HMAC-SHA256 完整性校验
- 🧬 每次操作绑定 DNA 追溯码
- 📦 321 备份：3 份副本、2 种介质、1 份异地
