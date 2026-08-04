# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# idevicebackup2 本地备份命令

**DNA**: #龍芯⚡️20260701023008577948-idevicebackup2 本地备份命令-A0EACE84
**分类**: 设备生态 / iOS 备份恢复
**英文缩写**: idevicebackup2

## 定义

libimobiledevice 提供的 idevicebackup2 可在 macOS/Linux/Windows 上对 iOS 4+ 设备进行本地备份、恢复、查看信息、解包。备份默认增量，--full 可强制全量。

## 触发场景

命令行备份 iPhone、idevicebackup2、本地备份、加密备份

## CNSH 命令

```text
龍魂 苹果 备份 创建 ~/Backups/iPhone
```

## 操作步骤

1. brew install libimobiledevice
2. idevicepair pair
3. idevicebackup2 backup ~/Backups/iPhone
4. 加密备份：idevicebackup2 encryption on 密码 backupdir

## CLI 示例

```bash
idevicebackup2 -i backup --full ~/Backups/iPhone
```



## 坑位提醒

- ⚠️ 备份目录需提前存在且可写
- ⚠️ iOS 16+ 备份可能要求设备输入锁屏密码
- ⚠️ 加密备份密码丢失无法恢复

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`
