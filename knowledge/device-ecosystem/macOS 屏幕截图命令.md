# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# macOS 屏幕截图命令

**DNA**: #龍芯⚡️20260701023008578445-macOS 屏幕截图命令-F9D8FD20
**分类**: 设备生态 / macOS 快捷操作
**英文缩写**: screencapture

## 定义

screencapture 是 macOS 自带的截图 CLI，支持全屏、窗口、区域、定时、显示鼠标指针、格式选择。

## 触发场景

Mac 命令行截图、screencapture、区域截图、定时截图

## CNSH 命令

```text
龍魂 Mac 截图 区域 /tmp/shot.png
```

## 操作步骤

1. screencapture -x /tmp/full.png 静默全屏
2. screencapture -i /tmp/select.png 区域选择
3. screencapture -T 5 /tmp/delay.png 延迟 5 秒

## CLI 示例

```bash
screencapture -ix /tmp/shot.png
```



## 坑位提醒

- ⚠️ -x 避免截图声音
- ⚠️ 默认格式为 PNG，可用 -t jpg
- ⚠️ 区域模式不支持静默

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`
