# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# iCloud 钥匙串与备份密码区别

**DNA**: #龍芯⚡️20260701023008579009-iCloud 钥匙串与备份密码区别-B602D575
**分类**: 设备生态 / 操作坑位
**英文缩写**: Keychain / Backup Password

## 定义

iCloud 钥匙串密码用于解锁同步的账号密码；iTunes/本地加密备份密码是另一个独立密码，用于加密备份文件。忘记备份密码无法从加密备份恢复，但可在设备上重置备份密码（旧备份仍无法解密）。

## 触发场景

备份密码忘了、iCloud 钥匙串密码、加密备份密码

## CNSH 命令

```text
龍魂 坑位 备份密码
```

## 操作步骤

1. 备份时勾选加密并牢记密码
2. 将密码存入密码管理器
3. 若忘记，可在设备上重置后重新备份

## CLI 示例

```bash
idevicebackup2 encryption on MyBackupPass ~/Backups/iPhone
```



## 坑位提醒

- ⚠️ 备份密码不可找回
- ⚠️ Apple ID 密码不能解密本地备份
- ⚠️ 重置备份密码不会解密旧备份

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`
