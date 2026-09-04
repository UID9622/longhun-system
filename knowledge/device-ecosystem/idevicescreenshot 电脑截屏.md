# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# idevicescreenshot 电脑截屏

**DNA**: #龍芯⚡️20260701023008578067-idevicescreenshot 电脑截屏-84D8D3B2
**分类**: 设备生态 / iOS 开发调试
**英文缩写**: screenshot

## 定义

idevicescreenshot 把 iPhone/iPad 当前屏幕截图直接保存到电脑，无需手动按 Home+Power。

## 触发场景

iPhone 截图到电脑、idevicescreenshot、批量截图

## CNSH 命令

```text
龍魂 苹果 截图 /tmp/iphone.png
```

## 操作步骤

1. 连接设备并信任
2. 运行 idevicescreenshot /tmp/iphone.png

## CLI 示例

```bash
idevicescreenshot /tmp/iphone_$(date +%s).png
```



## 坑位提醒

- ⚠️ 设备锁屏时无法截图
- ⚠️ 部分 DRM 内容会黑屏
- ⚠️ 保存路径需有写入权限

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`
