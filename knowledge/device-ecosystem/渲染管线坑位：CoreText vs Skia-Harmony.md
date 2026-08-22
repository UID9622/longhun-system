# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 渲染管线坑位：CoreText vs Skia/Harmony

**DNA**: #龍芯⚡️20260701023008578899-渲染管线坑位：CoreText vs Skia/Harmony-861D31F4
**分类**: 设备生态 / 字体渲染
**英文缩写**: CoreText / Skia

## 定义

iOS/macOS 用 CoreText + CoreGraphics 做文本布局和光栅化；鸿蒙 ArkUI 基于自研渲染管线，字距、hinting、抗锯齿策略不同。同样的字号和行高在不同平台视觉高度会不同。

## 触发场景

文字渲染差异、行高不一致、hinting、anti-aliasing、跨平台 UI 对不齐

## CNSH 命令

```text
龍魂 渲染 差异 说明
```

## 操作步骤

1. 设计稿使用相对单位（dp/vp/pt）而非绝对像素
2. 分别在各平台实测行高和字距
3. 对关键文字做平台专属微调

## CLI 示例

```bash
# 无通用命令，建议在真机/模拟器截图对比
```



## 坑位提醒

- ⚠️ CoreText 的 lineHeightMultiple 与 CSS/Skia 计算不同
- ⚠️ 鸿蒙的 vp 在 160dpi 基准下换算
- ⚠️ 小字号下的 hinting 差异最明显

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`
