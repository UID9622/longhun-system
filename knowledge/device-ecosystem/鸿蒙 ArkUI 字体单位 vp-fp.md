# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 鸿蒙 ArkUI 字体单位 vp/fp

**DNA**: #龍芯⚡️20260701023008579906-鸿蒙 ArkUI 字体单位 vp/fp-716556F5
**分类**: 设备生态 / HarmonyOS 开发对接
**英文缩写**: vp / fp

## 定义

鸿蒙 ArkUI 使用 vp（virtual pixel，1vp≈160dpi 下 1px）做屏幕无关尺寸，fp（font pixel）做字体尺寸并随系统字体大小变化。与 iOS 的 pt 类似，但基准密度不同。

## 触发场景

鸿蒙 vp fp、ArkUI 字体单位、HarmonyOS 适配

## CNSH 命令

```text
龍魂 华为 开发 字体单位
```

## 操作步骤

1. 布局尺寸用 vp，如 width('100vp')
2. 字体大小用 fp，如 fontSize('16fp')
3. 通过 display.getDefaultDisplaySync 获取密度换算

## CLI 示例

```bash
# hdc shell 获取屏幕密度
hdc shell hidumper -s WindowManagerService -a '-d'
```



## 坑位提醒

- ⚠️ fp 会跟随系统字体缩放，vp 不会
- ⚠️ 1vp 在不同设备像素不同
- ⚠️ 老版本 API 可能用 px 而非 vp

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`
