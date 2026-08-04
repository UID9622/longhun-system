# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# macOS defaults 偏好设置命令

**DNA**: #龍芯⚡️20260701023008578120-macOS defaults 偏好设置命令-976BA4CA
**分类**: 设备生态 / macOS 设置路径
**英文缩写**: defaults

## 定义

macOS 的系统偏好与 App 配置大多存在 ~/Library/Preferences 的 plist 中，defaults 命令可读取、写入、删除。注意修改系统域需要谨慎，部分设置在重启或重新登录后生效。

## 触发场景

macOS 命令行改设置、defaults write、plist、系统偏好

## CNSH 命令

```text
龍魂 Mac 偏好 读取 NSGlobalDomain
```

## 操作步骤

1. defaults read NSGlobalDomain 查看全局设置
2. defaults read com.apple.dock 查看 Dock 设置
3. defaults write com.apple.dock autohide -bool true 后 killall Dock

## CLI 示例

```bash
defaults read com.apple.finder ShowPathBar
```



## 坑位提醒

- ⚠️ 写错域或键可能导致 App 行为异常
- ⚠️ SIP 保护的系统设置无法通过 defaults 修改
- ⚠️ 部分设置需重启 App 或系统

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`
