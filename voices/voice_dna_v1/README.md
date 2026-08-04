# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂声纹DNA锚定链系统

**DNA**: `#龍芯⚡️20260628-VOICE-DNA-ANCHOR-v2.0`

## 目标

把声纹、文字、特征数据全部打包成一条龍魂DNA哈希链，固化数字人身份，使其只认龍魂系统内部的锚定。支持多用户开放注册、本地加密、321备份、用户自主导出、官网API接入。

## 文件结构

| 文件 | 职责 |
|---|---|
| `voice_anchor.py` | 声纹录入、特征提取、哈希指纹、DNA追溯链生成、manifest写入（多用户/加密） |
| `crypto.py` | 本地 Fernet + HMAC-SHA256 加密、密钥管理、用户级密钥派生、导出密钥 |
| `register.py` | 对外用户注册入口、user_id 校验、用户级声纹验证 |
| `digital_persona.py` | 数字人身份固化、调用前声纹验证、身份不匹配时拒绝输出 |
| `verify_anchor.py` | 数字人 ID + 声纹比对、匹配/不匹配判定、审计日志 |
| `backup.py` | 321 备份策略：每日本地备份、完整快照、用户加密导出包、导入恢复 |
| `web_api.py` | 官网开放注册 REST API（Flask）：register/verify/personas/export |
| `cli.py` | `lh voice` 命令行入口 |
| `test_voice_dna.py` | 验收测试脚本 |

## 注册命令

```bash
# 基础锚定（系统用户）
lh voice anchor "文本内容"

# 开放用户注册
lh voice register <user_id> "文本内容"

# 验证
lh voice verify "数字人ID" [--user-id <user_id>]

# 查询
lh voice list
lh voice personas <user_id>

# 备份与导出（321原则）
lh voice backup
lh voice snapshot [label]
lh voice backups
lh voice export <user_id> [persona_id] [--password <pwd>]

# 启动官网 API
lh voice serve [port]

# 审计
lh voice audit [N]
```

## 数据存储

- 身份记录：`~/.龍魂/voice_anchors/manifest.json`
- 审计日志：`~/.龍魂/voice_anchors/audit.jsonl`
- 原始音频：`~/.龍魂/voice_anchors/{persona_id}.wav`
- 加密密钥：`~/.龍魂/voice_anchors/.keys/`
- 本地备份：`~/.龍魂/voice_anchors/backup/`
- 快照：`~/.龍魂/voice_anchors/snapshots/`
- 用户导出：`~/.龍魂/voice_anchors/exports/`

## DNA 追溯码格式

```
DNA: #龍芯⚡️YYYYMMDD-VOICE-{hash8}
```

绑定字段：user_id、声纹指纹、文本内容、数字人ID、创建时间、本地IP。

## 本地加密方案

- 算法：`cryptography.fernet` 对称加密 + `HMAC-SHA256` 完整性校验
- 主密钥：本地随机生成，存储于 `~/.龍魂/voice_anchors/.keys/master.key`
- HMAC 密钥：本地随机生成，存储于 `~/.龍魂/voice_anchors/.keys/hmac.key`
- 用户级密钥：由主密钥 + user_id 派生，每个用户的加密密钥相互隔离
- 导出密钥：由主密钥 + user_id + 用户自定义密码派生
- 网络：全程不联网、不依赖外部 KMS

## 321 备份策略

| 层级 | 机制 | 路径/方式 |
|---|---|---|
| 本地备份 | 每日自动备份 manifest + audit | `~/.龍魂/voice_anchors/backup/` |
| 异地/用户备份 | 用户手动导出加密 ZIP 包 | `lh voice export <user_id>` |
| 关键快照 | 每季度或系统更新时完整快照 | `~/.龍魂/voice_anchors/snapshots/` |

## 官网 API

启动服务：

```bash
lh voice serve 8444
```

接口：

```bash
# 健康检查
GET  /voice/health

# 用户注册
POST /voice/register
Body: {"user_id": "xxx", "text": "xxx", "audio_base64": "..."}
# 测试模式：{"user_id": "xxx", "text": "xxx", "test_mode": true, "test_freq": 230}

# 用户验证
POST /voice/verify
Body: {"user_id": "xxx", "persona_id": "xxx", "audio_base64": "..."}

# 个人页面展示
GET  /voice/personas/<user_id>
GET  /voice/persona/<persona_id>

# 用户导出加密包
POST /voice/export
Body: {"user_id": "xxx", "persona_id": "xxx", "password": "xxx"}
```

## 本地特征提取

当前使用 `torchaudio` 本地计算 MFCC 与 MelSpectrogram，再对时间轴做统计聚合，得到固定维度特征向量。该方案无需联网、无需预训练大模型，可在本地跑通。如需 ResNet/VGGVox 等深度模型，可替换 `voice_anchor.py` 中的 `extract_features()` 函数。

## 测试模式

无麦克风时可用合成音频验证：

```bash
lh voice register user1 "我是龍魂用户" --test --freq 230
lh voice verify LHVP-XXX --user-id user1 --test --freq 230
```

## 验收状态

- [x] 官网每个入口允许用户自行注册声纹
- [x] 用户注册自动生成龍魂DNA锚定链（user_id + 声纹指纹 + 注册时间 + 数字人ID）
- [x] 所有锚定记录统一写入 `~/.龍魂/voice_anchors/manifest.json`
- [x] 声纹特征本地加密（Fernet + HMAC-SHA256）
- [x] 加密密钥本地生成，不联网、不依赖第三方
- [x] 本地每日自动备份
- [x] 用户可手动导出加密ZIP声纹DNA包
- [x] 支持季度/系统更新完整快照
- [x] 用户个人页面可查看数字人身份、DNA追溯码、注册时间
- [x] 用户可随时发起声纹验证
