# iOS 开发者模式与设备信任

**DNA**: #龍芯⚡️20260701023008577883-iOS 开发者模式与设备信任-A89FD9F6
**分类**: 设备生态 / iOS 开发调试
**英文缩写**: Developer Mode / lockdownd

## 定义

iOS 16+ 需要在 设置 → 隐私与安全性 → 开发者模式 中开启；首次 USB 连接 Mac 时需在 iPhone 上点'信任'。libimobiledevice 的 idevicepair 可查看配对状态。

## 触发场景

iPhone 连接 Mac 不信任、开发者模式找不到、ideviceinfo 没反应

## CNSH 命令

```text
龍魂 苹果 设备 配对状态
```

## 操作步骤

1. iPhone 解锁并连接 USB
2. 在 iPhone 弹窗中点击'信任'
3. 设置 → 隐私与安全性 → 开发者模式 → 开启并重启
4. Mac 终端运行 idevicepair pair

## CLI 示例

```bash
idevicepair pair && ideviceinfo -s ProductType
```



## 坑位提醒

- ⚠️ 未开启开发者模式时 ideviceinfo 返回空
- ⚠️ 信任弹窗只出现一次，误点'不信任'需重置位置与隐私
- ⚠️ 网络连接设备需先 USB 配对

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`
