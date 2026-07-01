# iCloud 备份与本机加密备份

**DNA**: #龍芯⚡️20260701023008577597-iCloud 备份与本机加密备份-8D2DF300
**分类**: 设备生态 / iOS 备份恢复
**英文缩写**: iTunes Backup / iCloud Backup

## 定义

iCloud 备份走云端，自动每晚充电+WiFi 时进行，但不备份钥匙串全部内容；本机加密备份通过 Finder/iTunes 或 idevicebackup2 落盘到 Mac/PC，勾选'加密本地备份'才能包含 Health/钥匙串/Wi-Fi 密码。

## 触发场景

iPhone 怎么备份、iCloud 和本机备份区别、备份密码、钥匙串备份

## CNSH 命令

```text
龍魂 苹果 备份 本地 ~/Backups/iPhone
```

## 操作步骤

1. 用 USB 线连接 iPhone 到 Mac
2. Finder → 侧边栏选择 iPhone → '通用' → '将 iPhone 上所有数据备份到此 Mac'
3. 勾选'加密本地备份'并设置密码（之后恢复需同一密码）
4. 点按'立即备份'

## CLI 示例

```bash
idevicebackup2 backup --full ~/Backups/iPhone
```



## 坑位提醒

- ⚠️ 忘记备份密码会导致加密备份无法恢复
- ⚠️ iCloud 备份恢复时若云端空间不足会失败
- ⚠️ iOS 16+ 备份到较旧的 iOS 可能不兼容

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`
