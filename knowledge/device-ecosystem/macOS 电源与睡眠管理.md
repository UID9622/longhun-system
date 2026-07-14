# macOS 电源与睡眠管理

**DNA**: #龍芯⚡️20260701023008578227-macOS 电源与睡眠管理-89B55A90
**分类**: 设备生态 / macOS 设置路径
**英文缩写**: pmset

## 定义

pmset 用于查看和设置 Mac 的电源管理：睡眠、唤醒、显示器关闭、UPS 行为。对笔记本电池健康和长时间任务很有用。

## 触发场景

macOS 防止睡眠、pmset、电池健康、合盖不休眠

## CNSH 命令

```text
龍魂 Mac 电源 状态
```

## 操作步骤

1. pmset -g batt 查看电池状态
2. pmset -g 查看当前电源配置
3. caffeinate -i 或 pmset noidle 临时阻止睡眠

## CLI 示例

```bash
pmset -g batt
```



## 坑位提醒

- ⚠️ 某些设置需要 sudo
- ⚠️ 合盖运行可能影响散热
- ⚠️ 禁用睡眠会加快电池消耗

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`
