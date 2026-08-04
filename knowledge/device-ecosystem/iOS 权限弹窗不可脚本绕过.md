# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# iOS 权限弹窗不可脚本绕过

**DNA**: #龍芯⚡️20260701023008578952-iOS 权限弹窗不可脚本绕过-298C2521
**分类**: 设备生态 / 操作坑位
**英文缩写**: TCC

## 定义

iOS 的 TCC（Transparency, Consent, and Control）框架禁止任何应用、脚本或 Xcode 自动同意权限弹窗。自动化测试需先通过 settings app 或 Apple Configurator 预配置描述文件。

## 触发场景

自动点权限弹窗、iOS 自动化测试权限、TCC

## CNSH 命令

```text
龍魂 坑位 权限弹窗
```

## 操作步骤

1. 测试前在设置中手动授权
2. 或使用 Apple Configurator 下发隐私描述文件
3. Xcode UI 测试只能点击应用内元素，无法点系统弹窗

## CLI 示例

```bash
# 无法通过 CLI 自动授权
```



## 坑位提醒

- ⚠️ 私有 API 绕过会被 App Store 拒绝
- ⚠️ 越狱设备风险高且不稳定
- ⚠️ iOS 更新可能改变弹窗结构

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`
