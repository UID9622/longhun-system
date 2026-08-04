# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# iOS SwiftUI/UIKit 动态字号适配

**DNA**: #龍芯⚡️20260701023008579836-iOS SwiftUI/UIKit 动态字号适配-142FC4D8
**分类**: 设备生态 / iOS/macOS 开发对接
**英文缩写**: Dynamic Type Size

## 定义

SwiftUI 的 @Environment(\.dynamicTypeSize) 和 UIKit 的 UIContentSizeCategory 可监听系统字号变化。适配时应用 Size Categories 做断点，避免最大字号时布局崩溃。

## 触发场景

SwiftUI 动态字体、Dynamic Type、辅助功能字体、大号字体适配

## CNSH 命令

```text
龍魂 苹果 开发 动态字体
```

## 操作步骤

1. SwiftUI 用 .dynamicTypeSize(...) 限制最大字号
2. UIKit 用 UIFontMetrics(forTextStyle:).scaledFont(for:)
3. 在 Accessibility Inspector 中测试超大字号

## CLI 示例

```bash
# 无 CLI；建议 Xcode 预览或模拟器测试
```



## 坑位提醒

- ⚠️ 固定 frame 会在大字体下截断
- ⚠️ 自定义字体需配合 UIFontMetrics
- ⚠️ macOS 的 Dynamic Type 支持较晚

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`
