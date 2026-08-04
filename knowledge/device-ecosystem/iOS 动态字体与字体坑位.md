# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# iOS 动态字体与字体坑位

**DNA**: #龍芯⚡️20260701023008577818-iOS 动态字体与字体坑位-C35E3768
**分类**: 设备生态 / 字体渲染
**英文缩写**: Dynamic Type / CoreText

## 定义

iOS 使用 Dynamic Type 根据用户设置的'显示与亮度→文字大小'和'粗体文本'缩放字体。App 应使用 UIFont.preferredFont(forTextStyle:) 否则不会跟随系统缩放。自定义字体需注册到 Info.plist 的 UIAppFonts。

## 触发场景

iOS 字体大小、Dynamic Type、自定义字体不生效、文字截断

## CNSH 命令

```text
龍魂 苹果 字体 列表
```

## 操作步骤

1. 将 .ttf/.otf 加入 Xcode 工程并勾选 Target
2. 在 Info.plist 中添加 UIAppFonts 数组列出字体文件名
3. 代码中使用 UIFont(name:size:) 加载

## CLI 示例

```bash
# 列出 iOS 设备可用字体（需 ideviceinfo 等高级接口或 App 内脚本）
```



## 坑位提醒

- ⚠️ 未使用 preferredFont 导致辅助功能文字变大时 UI 截断
- ⚠️ 自定义字体文件名和 PostScript 名称不同会加载失败
- ⚠️ Apple 对中文字体回退到系统默认 PingFang SC

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`
