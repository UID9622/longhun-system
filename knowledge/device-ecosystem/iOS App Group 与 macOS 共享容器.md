# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# iOS App Group 与 macOS 共享容器

**DNA**: #龍芯⚡️20260701023008579708-iOS App Group 与 macOS 共享容器-1BDA7B58
**分类**: 设备生态 / iOS/macOS 开发对接
**英文缩写**: App Group

## 定义

iOS/macOS 的 App Group（com.apple.security.application-groups）让同一开发者的多个 App 或 App 与 Extension 共享一个容器目录，适合共享账号状态、数据库、缓存。

## 触发场景

iOS 扩展共享数据、App Group、共享容器、UserDefaults 共享

## CNSH 命令

```text
龍魂 苹果 开发 共享容器
```

## 操作步骤

1. 在 Apple Developer 创建 App Group ID
2. Xcode Signing & Capabilities 中开启 App Groups
3. 代码中用 FileManager.default.containerURL(forSecurityApplicationGroupIdentifier:) 访问

## CLI 示例

```bash
# 查看已启用 group 的应用容器
ls ~/Library/Containers/<group-id>/
```



## 坑位提醒

- ⚠️ App Group 需要重新签名和 Provisioning Profile
- ⚠️ 沙盒路径在不同设备不同
- ⚠️  watchOS 和 macOS Catalyst 也支持但需分别配置

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`
