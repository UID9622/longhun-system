# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# iOS 设置 URL Scheme

**DNA**: #龍芯⚡️20260701023008577680-iOS 设置 URL Scheme-E6C2F69A
**分类**: 设备生态 / iOS 设置路径
**英文缩写**: prefs:

## 定义

iOS 的 prefs:root= 与 settings-navigation:// URL 可被快捷指令、Siri 捷径或 App 调用，直接跳转到具体设置页。注意部分 URL 在 iOS 18+ 已改名或失效。

## 触发场景

iOS 设置快捷方式、Settings URL、快捷指令跳转设置、找不到设置项

## CNSH 命令

```text
龍魂 苹果 设置 跳转 无线局域网
```

## 操作步骤

1. 在'快捷指令'中添加'打开 URL'动作
2. 输入对应的 prefs:root= URL
3. 运行即可直达设置页

## CLI 示例

```bash
open 'prefs:root=WIFI'  # 仅在 iOS 真机/模拟器内生效
```

## 常用 URL

- **无线局域网**: `prefs:root=WIFI`
- **蓝牙**: `prefs:root=Bluetooth`
- **蜂窝网络**: `prefs:root=MOBILE_DATA_SETTINGS_ID`
- **隐私与安全性**: `prefs:root=Privacy`
- **定位服务**: `prefs:root=Privacy&path=LOCATION`
- **屏幕使用时间**: `prefs:root=SCREEN_TIME`
- **辅助功能**: `prefs:root=ACCESSIBILITY`
- **iCloud**: `prefs:root=CASTLE`
- **iCloud 备份**: `prefs:root=CASTLE&path=BACKUP`

## 坑位提醒

- ⚠️ Apple 不保证 URL Scheme 长期稳定
- ⚠️ 上架 App 使用私有 URL 可能被拒
- ⚠️ 部分页面需要设备已解锁

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`
