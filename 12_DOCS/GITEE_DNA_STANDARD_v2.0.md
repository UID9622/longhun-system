# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA追溯碼標準規範 v2.0

> 来源: Gitee uid9622/cnsh · DNA_STANDARD.md
> 作者: Lucky·UID9622 (諸葛鑫)
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
> 核心理念: "每一行代碼都有來源，每一次提交都有證明。帶證的磚，別人不敢碰。"

---

## 1. DNA追溯码格式

```
#ZHUGEXIN⚡️{YYYYMMDD}-{PROJECT}-{DESC}-v{MAJOR}.{MINOR}.{PATCH}
```

- 固定前缀 `#ZHUGEXIN⚡️` 不可修改
- 日期使用 UTC+8（中国标准时间），格式 `YYYYMMDD`
- 版本号遵循语义化版本规范

### 注意
> 本地系统已升级为 v∞ 干支格式: `#龍芯⚡️<年干支>·<月干支>·<日干支>·<时辰>·<卦名>-<模块>-<动作>-<哈希8位>`
> 本文件记录的是 Gitee 公开版的原始标准 (格里历格式)，供兼容性参考。

---

## 2. 时间戳规范（三条强制规则）

- **禁止未来时间**：代码日期不得超过当前日期+1天
- **禁止过早时间**：日期不得早于 2025-01-01（创世区块）
- **统一时区**：全部使用 UTC+8

---

## 3. 确认码格式

```
#CONFIRM🌌9622-ONLY-ONCE🧬{描述}-772Z
```

---

## 4. 文件头模板

### Python
```python
"""
DNA追溯码: #ZHUGEXIN⚡️{YYYYMMDD}-{PROJECT}-{DESC}-v{VER}
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬{DESC}-772Z
时间: {YYYY-MM-DD} {HH:MM:SS} UTC+8
作者: Lucky·UID9622
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
```

### JavaScript
```javascript
/**
 * DNA追溯码: #ZHUGEXIN⚡️{YYYYMMDD}-{PROJECT}-{DESC}-v{VER}
 * 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬{DESC}-772Z
 * 时间: {YYYY-MM-DD} {HH:MM:SS} UTC+8
 * 作者: Lucky·UID9622
 * GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
 */
```

---

## 5. GPG 签名标准

- 所有代码文件需生成分离签名（`.asc` 文件）
- 提交前检查清单：DNA头、签名文件、指纹匹配、时间戳、正体"龍"

---

## 6. 自动化校验

- Git pre-commit 钩子自动执行 DNA 校验、GPG 签名校验、龍字一致性检查、时间戳合规检查
- 提供 `validate_dna.py` 和 `validate_gpg.py` 脚本

---

## 7. 违规判定（"黑户代码"）

以下情况将被自动拒绝：
- 无 DNA 追溯码
- 时间戳为未来
- 使用简体"龍"（必须用正体"龍"）
- P0 常量被修改（永久封禁）

---

> 同步自: Gitee uid9622/cnsh · 2026-07-10
