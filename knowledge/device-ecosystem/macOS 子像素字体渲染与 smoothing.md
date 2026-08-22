# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# macOS 子像素字体渲染与 smoothing

**DNA**: #龍芯⚡️20260701023008578385-macOS 子像素字体渲染与 smoothing-C52DD2E9
**分类**: 设备生态 / 字体渲染
**英文缩写**: Font Smoothing

## 定义

macOS 的字体平滑（font smoothing）会改变非 Retina 屏上文字的粗细。Retina 屏通常建议关闭，部分用户迁移到 Apple Silicon 后发现外接显示器字体发虚，可调整 defaults -currentHost write -globalDomain AppleFontSmoothing。

## 触发场景

Mac 字体发虚、子像素渲染、font smoothing、外接显示器字体

## CNSH 命令

```text
龍魂 Mac 字体 平滑 关闭
```

## 操作步骤

1. defaults -currentHost write -globalDomain AppleFontSmoothing -int 0 关闭
2. 1 轻度、2 中度、3 重度
3. 注销或重启应用生效

## CLI 示例

```bash
defaults -currentHost read -globalDomain AppleFontSmoothing
```



## 坑位提醒

- ⚠️ Retina 屏关闭后可能更清晰
- ⚠️ 取值范围 0-3，超出可能无效
- ⚠️ 某些应用会忽略全局设置

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`
